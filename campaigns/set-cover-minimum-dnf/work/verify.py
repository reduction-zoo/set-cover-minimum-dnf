"""Independent Kissat check of sparse exact target instances."""

import argparse
import itertools
import json
import subprocess
import sys


SOURCES = [
    {"universe_size": 0, "sets": [], "k": 0},
    {"universe_size": 1, "sets": [], "k": 0},
    {"universe_size": 3, "sets": [[0], [1], [2], [0, 1, 2]], "k": 3},
    {"universe_size": 4, "sets": [[0], [1], [2], [3]], "k": 3},
]


def source_witness(x):
    for count in range(min(x["k"], len(x["sets"])) + 1):
        for choice in itertools.combinations(range(len(x["sets"])), count):
            if set().union(*(x["sets"][i] for i in choice)) == set(range(x["universe_size"])):
                return {"cover": list(choice)}
    return "NO-SOLUTION"


def exact_target(x, y):
    n, accepted = x["n"], {int(a or "0", 2) for a in x["accepted"]}
    if y == "NO-SOLUTION":
        return True  # Infeasibility is certified by the conclusive SAT result below.
    if len(y["terms"]) > x["K"]:
        return False
    union = set()
    for term in y["terms"]:
        if len(term) != n or any(v not in (-1, 0, 1) for v in term):
            return False
        base = sum(1 << (n - i - 1) for i, v in enumerate(term) if v == 1)
        free = sum(1 << (n - i - 1) for i, v in enumerate(term) if v == 0)
        if 1 << free.bit_count() > len(accepted):
            return False
        sub = free
        while True:
            point = base | sub
            if point not in accepted:
                return False
            union.add(point)
            if sub == 0:
                break
            sub = (sub - 1) & free
    return union == accepted


def solve_target(x):
    n = x["n"]
    points = {int(a or "0", 2) for a in x["accepted"]}
    cubes = {(a, 0): {a} for a in points}
    queue = list(cubes)
    nonprime = set()
    for base, free in queue:
        fixed = ((1 << n) - 1) ^ free
        while fixed:
            bit = fixed & -fixed
            fixed -= bit
            neighbor = (base ^ bit, free)
            if neighbor in cubes:
                merged = (base & ~bit, free | bit)
                if merged not in cubes:
                    cubes[merged] = cubes[(base, free)] | cubes[neighbor]
                    queue.append(merged)
                nonprime.update(((base, free), neighbor))
    prime = [cube for cube in cubes if cube not in nonprime]
    available = set(points)
    forced = set()
    while True:
        options = {point: [i for i, cube in enumerate(prime) if point in cubes[cube]] for point in available}
        if any(not choices for choices in options.values()):
            return ["NO-SOLUTION"]
        new = {choices[0] for choices in options.values() if len(choices) == 1} - forced
        if not new:
            break
        forced.update(new)
        available.difference_update(set().union(*(cubes[prime[i]] for i in new)))
    budget = x["K"] - len(forced)
    if budget < 0:
        return ["NO-SOLUTION"]
    if not available:
        selections = [set()]
        active = []
    else:
        size = max((len(cubes[cube] & available) for cube in prime), default=0)
        if size * budget < len(available):
            return ["NO-SOLUTION"]
        if size * budget != len(available):
            raise RuntimeError("independent exact-cover oracle requires a tight residual bound")
        active = [i for i, cube in enumerate(prime) if len(cubes[cube] & available) == size]
        clauses = []
        for point in available:
            choices = [j + 1 for j, i in enumerate(active) if point in cubes[prime[i]]]
            clauses.append(choices)
            clauses.extend([[-a, -b] for a, b in itertools.combinations(choices, 2)])
        selections = []
        for _ in range(2):
            dimacs = f"p cnf {len(active)} {len(clauses)}\n" + "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
            run = subprocess.run(["kissat", "-q"], input=dimacs, text=True, capture_output=True)
            if run.returncode == 20 and "s UNSATISFIABLE" in run.stdout:
                break
            if run.returncode != 10 or "s SATISFIABLE" not in run.stdout:
                raise RuntimeError(f"Kissat failed: {run.returncode} {run.stderr}")
            selected = {int(word) - 1 for line in run.stdout.splitlines() if line.startswith("v ")
                        for word in line.split()[1:] if int(word) > 0}
            selections.append(selected)
            clauses.append([-(j + 1) if j in selected else j + 1 for j in range(len(active))])
        if not selections:
            return ["NO-SOLUTION"]

    outputs = []
    for selection in selections:
        chosen = forced | {active[j] for j in selection}
        terms = []
        for i in chosen:
            base, free = prime[i]
            terms.append([0 if free & (1 << (n - j - 1)) else
                          1 if base & (1 << (n - j - 1)) else -1 for j in range(n)])
        y = {"terms": terms}
        assert exact_target(x, y)
        outputs.append(y)
    return outputs


def run_map(path, payload, extract=False):
    args = [sys.executable, path] + (["--extract"] if extract else [])
    process = subprocess.run(args, input=json.dumps(payload), text=True, capture_output=True, check=True)
    return json.loads(process.stdout)


def main(path):
    outputs = 0
    for index, source in enumerate(SOURCES):
        target = run_map(path, source)
        ys = solve_target(target)
        expected = source_witness(source)
        for y in ys:
            if y != "NO-SOLUTION":
                assert exact_target(target, y)
            recovered = run_map(path, {"source": source, "target_solution": y}, extract=True)
            assert (recovered == "NO-SOLUTION") == (expected == "NO-SOLUTION")
            if recovered != "NO-SOLUTION":
                assert len(recovered["cover"]) <= source["k"]
                assert len(recovered["cover"]) == len(set(recovered["cover"]))
                assert set().union(*(source["sets"][j] for j in recovered["cover"])) == set(range(source["universe_size"]))
            outputs += 1
        print(f"case {index}: n={target['n']} A={len(target['accepted'])}, decision={'NO' if ys == ['NO-SOLUTION'] else 'YES'}, outputs={len(ys)}", flush=True)
    print(f"independent verification passed: {len(SOURCES)} source cases, {outputs} target outputs; Kissat 4.0.4")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    main(parser.parse_args().candidate)

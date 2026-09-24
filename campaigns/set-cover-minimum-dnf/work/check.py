"""Independent definition-level oracles and an injected reduction check."""

import argparse
import itertools
import json
import subprocess
import sys
from pathlib import Path

import z3

ROOT = Path(__file__).resolve().parents[3]
WORK = Path(__file__).resolve().parent


def source_valid(x, y):
    m, sets, k = x["universe_size"], x["sets"], x["k"]
    if type(m) is not int or type(k) is not int or min(m, k) < 0:
        return False
    if not isinstance(sets, list) or any(not isinstance(s, list) or
        any(type(e) is not int or e < 0 or e >= m for e in s) or len(s) != len(set(s)) for s in sets):
        return False
    if y == "NO-SOLUTION":
        return source_bruteforce(x) == "NO-SOLUTION"
    return (isinstance(y, dict) and set(y) == {"cover"} and
        isinstance(y["cover"], list) and len(y["cover"]) <= k and
        len(y["cover"]) == len(set(map(str, y["cover"]))) and
        all(type(i) is int and 0 <= i < len(sets) for i in y["cover"]) and
        set().union(*(sets[i] for i in y["cover"])) == set(range(m)))


def source_bruteforce(x):
    for size in range(min(x["k"], len(x["sets"])) + 1):
        for indices in itertools.combinations(range(len(x["sets"])), size):
            y = {"cover": list(indices)}
            if source_valid(x, y):
                return y
    return "NO-SOLUTION"


def source_z3(x):
    variables = [z3.Bool(f"s{i}") for i in range(len(x["sets"]))]
    solver = z3.Solver()
    if variables:
        solver.add(z3.PbLe([(v, 1) for v in variables], x["k"]))
    for e in range(x["universe_size"]):
        solver.add(z3.Or([variables[i] for i, s in enumerate(x["sets"]) if e in s]))
    status = solver.check()
    if status == z3.unsat:
        return "NO-SOLUTION"
    if status != z3.sat:
        raise RuntimeError(f"source solver: {status}")
    y = {"cover": [i for i, v in enumerate(variables) if z3.is_true(solver.model().eval(v))]}
    assert source_valid(x, y)
    return y


def target_valid(x, y):
    n, accepted, bound = x["n"], x["accepted"], x["K"]
    if any(type(v) is not int or v < 0 for v in (n, bound)) or not isinstance(accepted, list):
        return False
    if len(set(accepted)) != len(accepted) or any(not isinstance(a, str) or len(a) != n or set(a) - {"0", "1"} for a in accepted):
        return False
    if y == "NO-SOLUTION":
        return target_z3(x, limit=1) == []
    if not isinstance(y, dict) or set(y) != {"terms"} or not isinstance(y["terms"], list) or len(y["terms"]) > bound:
        return False
    if any(not isinstance(t, list) or len(t) != n or any(type(v) is not int or v not in (-1, 0, 1) for v in t) for t in y["terms"]):
        return False
    accepted_values = {int(a or "0", 2) for a in accepted}
    actual = set()
    for term in y["terms"]:
        if 1 << term.count(0) > len(accepted_values):
            return False
        base = sum(1 << (n - 1 - i) for i, v in enumerate(term) if v == 1)
        free = sum(1 << (n - 1 - i) for i, v in enumerate(term) if v == 0)
        submask = free
        while True:
            value = base | submask
            if value not in accepted_values:
                return False
            actual.add(value)
            if submask == 0:
                break
            submask = (submask - 1) & free
    return actual == accepted_values


def target_z3(x, limit=3):
    n, accepted, bound = x["n"], set(x["accepted"]), x["K"]
    if any(len(a) != n or set(a) - {"0", "1"} for a in accepted):
        raise ValueError("invalid target assignment")
    # Every legal implicant is formed by merging two smaller complete subcubes.
    covers = {a: {a} for a in accepted}
    pending = list(accepted)
    for cube in pending:
        for pos, bit in enumerate(cube):
            if bit == "-":
                continue
            other = cube[:pos] + ("1" if bit == "0" else "0") + cube[pos + 1:]
            if other in covers:
                merged = cube[:pos] + "-" + cube[pos + 1:]
                if merged not in covers:
                    covers[merged] = covers[cube] | covers[other]
                    pending.append(merged)
    cubes = [cube for cube in covers if not any(bit != "-" and
             cube[:pos] + "-" + cube[pos + 1:] in covers for pos, bit in enumerate(cube))]
    required = set(accepted)
    forced = set()
    while True:
        new = {next(i for i, cube in enumerate(cubes) if a in covers[cube])
               for a in required if sum(a in covers[cube] for cube in cubes) == 1} - forced
        if not new:
            break
        forced |= new
        required -= set().union(*(covers[cubes[i]] for i in new))
    if len(forced) > bound:
        return []
    free = [i for i, cube in enumerate(cubes) if i not in forced and covers[cube] & required]
    allowance = bound - len(forced)
    largest = max((len(covers[cubes[i]] & required) for i in free), default=0)
    if required and largest * allowance < len(required):
        return []
    tight = bool(required) and largest * allowance == len(required)
    if tight:
        free = [i for i in free if len(covers[cubes[i]] & required) == largest]
    variables = [z3.Bool(f"t{i}") for i in free]
    solver = z3.Solver()
    if variables and not tight:
        solver.add(z3.PbLe([(v, 1) for v in variables], allowance))
    for a in required:
        options = [variables[j] for j, i in enumerate(free) if a in covers[cubes[i]]]
        solver.add(z3.PbEq([(v, 1) for v in options], 1) if tight and options else z3.Or(options))
    if n > 20:
        print(f"oracle n={n} A={len(accepted)} cubes={len(cubes)} forced={len(forced)} remaining={len(required)} free={len(free)} tight={tight}", file=sys.stderr, flush=True)
    outputs = []
    while len(outputs) < limit:
        status = solver.check()
        if status == z3.unsat:
            break
        if status != z3.sat:
            raise RuntimeError(f"target solver: {status}")
        model = solver.model()
        chosen = list(forced) + [free[j] for j, v in enumerate(variables) if z3.is_true(model.eval(v))]
        y = {"terms": [[-1 if bit == "0" else 1 if bit == "1" else 0 for bit in cubes[i]] for i in chosen]}
        assert target_valid(x, y)
        outputs.append(y)
        solver.add(z3.Or([v != model.eval(v) for v in variables]))
    return outputs


def self_test():
    subprocess.run([sys.executable, str(ROOT / "research/validate_preparation.py"), str(WORK / "cases.json")], check=True)
    cases = json.loads((WORK / "cases.json").read_text())
    yes = no = 0
    for case in cases:
        x = case["source"]
        if case["kind"] == "random":
            from generate_cases import from_seed
            assert from_seed(case["seed"]) == x
        brute = source_bruteforce(x)
        z_answer = source_z3(x)
        assert (brute == "NO-SOLUTION") == (z_answer == "NO-SOLUTION")
        assert source_valid(x, z_answer)
        assert case["expected"] == brute
        yes += brute != "NO-SOLUTION"
        no += brute == "NO-SOLUTION"
    assert source_bruteforce({"universe_size": 2, "sets": [[0], [1]], "k": 1}) == "NO-SOLUTION"
    assert source_valid({"universe_size": 2, "sets": [[0], [1]], "k": 2}, {"cover": [0, 1]})
    assert not source_valid({"universe_size": 2, "sets": [[0], [1]], "k": 1}, {"cover": [0, 1]})
    assert not source_valid({"universe_size": 1, "sets": [[0]], "k": 1}, "NO-SOLUTION")
    assert not source_valid({"universe_size": 1, "sets": [[0]], "k": 1}, {"cover": [1]})
    for x, expected in [
        ({"n": 0, "accepted": [""], "K": 1}, True),
        ({"n": 1, "accepted": [], "K": 0}, True),
        ({"n": 1, "accepted": ["0"], "K": 0}, False),
        ({"n": 2, "accepted": ["00", "11"], "K": 1}, False),
        ({"n": 2, "accepted": ["00", "11"], "K": 2}, True),
    ]:
        found = target_z3(x)
        assert bool(found) == expected
        assert all(target_valid(x, y) for y in found)
        assert target_valid(x, "NO-SOLUTION") == (not expected)
    assignments = ["00", "01", "10", "11"]
    for mask in range(16):
        accepted = {a for i, a in enumerate(assignments) if mask & (1 << i)}
        legal = []
        for cube in itertools.product((-1, 0, 1), repeat=2):
            covered = {a for a in assignments if all(v == 0 or (bit == "1") == (v == 1) for bit, v in zip(a, cube))}
            if covered <= accepted:
                legal.append(covered)
        for bound in range(3):
            expected = any(set().union(*choice) == accepted for size in range(bound + 1)
                           for choice in itertools.combinations(legal, size))
            assert bool(target_z3({"n": 2, "accepted": sorted(accepted), "K": bound}, limit=1)) == expected
    assert not target_valid({"n": 2, "accepted": ["00", "11"], "K": 2}, {"terms": [[-1, -1]]})
    assert not target_valid({"n": 1, "accepted": ["0"], "K": 1}, {"terms": [[0]]})
    print(f"self-test passed: {len(cases)} cases ({yes} YES, {no} NO), Z3 {z3.get_version_string()}")


def candidate(path):
    cases = json.loads((WORK / "cases.json").read_text())
    outputs = no = 0
    for index, case in enumerate(cases):
        x = case["source"]
        raw = subprocess.run([sys.executable, path], input=json.dumps(x), text=True, capture_output=True, check=True)
        target = json.loads(raw.stdout)
        print(f"case {index}: n={target['n']} A={len(target['accepted'])} K={target['K']}", file=sys.stderr, flush=True)
        ys = target_z3(target)
        if not ys:
            ys = ["NO-SOLUTION"]
            no += 1
        for y in ys:
            assert target_valid(target, y)
            raw = subprocess.run([sys.executable, path, "--extract"], input=json.dumps({"source": x, "target_solution": y}), text=True, capture_output=True, check=True)
            result = json.loads(raw.stdout)
            assert source_valid(x, result), (index, x, target, y, result)
            assert (result == "NO-SOLUTION") == (case["expected"] == "NO-SOLUTION"), (index, x, target, y, result)
            outputs += 1
    print(f"candidate passed: {len(cases)} source cases, {outputs} target outputs, {no} NO-SOLUTION outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--label-cases", action="store_true")
    parser.add_argument("--candidate")
    args = parser.parse_args()
    if args.label_cases:
        cases = json.loads((WORK / "cases.json").read_text())
        for case in cases:
            case["expected"] = source_bruteforce(case["source"])
        (WORK / "cases.json").write_text(json.dumps(cases, indent=2) + "\n")
    elif args.self_test:
        self_test()
    elif args.candidate:
        candidate(args.candidate)
    else:
        parser.error("select --self-test, --label-cases, or --candidate")

"""Set Cover to exact DNF via SAT, 3-set cover, and Gimpel parity completion."""

import json
import sys
from itertools import combinations


YES_TARGET = {"n": 0, "accepted": [""], "K": 1}
NO_TARGET = {"n": 1, "accepted": ["0"], "K": 0}


def easy_answer(source):
    m, sets, k = source["universe_size"], source["sets"], source["k"]
    if m == 0:
        return {"cover": []}
    if set().union(*sets) != set(range(m)) or k == 0:
        return "NO-SOLUTION"
    if k <= 2:
        for size in range(1, k + 1):
            for chosen in combinations(range(len(sets)), size):
                if set().union(*(sets[i] for i in chosen)) == set(range(m)):
                    return {"cover": list(chosen)}
        return "NO-SOLUTION"
    if k >= len(sets):
        return {"cover": list(range(len(sets)))}
    return None


def source_cnf(source):
    """CNF whose first |sets| variables choose source sets."""
    sets, k = source["sets"], source["k"]
    clauses = [[j + 1 for j, subset in enumerate(sets) if e in subset]
               for e in range(source["universe_size"])]
    next_var = len(sets)

    def new_var():
        nonlocal next_var
        next_var += 1
        return next_var

    def negate(lit):
        return not lit if type(lit) is bool else -lit

    def and_gate(a, b):
        if a is False or b is False:
            return False
        if a is True:
            return b
        if b is True:
            return a
        z = new_var()
        clauses.extend([[-z, a], [-z, b], [z, -a, -b]])
        return z

    def or_gate(a, b):
        if a is True or b is True:
            return True
        if a is False:
            return b
        if b is False:
            return a
        z = new_var()
        clauses.extend([[z, -a], [z, -b], [-z, a, b]])
        return z

    # The Tseitin gates encode whether at least j of the first i set variables are true.
    previous = [True] + [False] * (k + 1)
    for x in range(1, len(sets) + 1):
        current = [True]
        for j in range(1, k + 2):
            current.append(or_gate(previous[j], and_gate(x, previous[j - 1])))
        previous = current
    overflow = previous[k + 1]
    clauses.append([negate(overflow)])
    return next_var, clauses


def three_set_cover(source):
    """Map the CNF to 3-partite exact cover; return triples and wheel markers."""
    variable_count, clauses = source_cnf(source)
    occurrences = [[] for _ in range(variable_count + 1)]
    clause_occurrences = []
    universe_size = 0

    def point():
        nonlocal universe_size
        value = universe_size
        universe_size += 1
        return value

    for clause in clauses:
        items = []
        for literal in clause:
            a, b, true_tip, false_tip = point(), point(), point(), point()
            item = (a, b, true_tip, false_tip, literal)
            items.append(item)
            occurrences[abs(literal)].append(item)
        clause_occurrences.append(items)

    triples = []
    wheel_true = {}
    for variable in range(1, variable_count + 1):
        items = occurrences[variable]
        for i, (a, b, true_tip, false_tip, _) in enumerate(items):
            if i == 0:
                wheel_true[variable] = len(triples)
            triples.append((a, b, false_tip))
            triples.append((a, items[(i + 1) % len(items)][1], true_tip))

    for items in clause_occurrences:
        clause_a, clause_b = point(), point()
        for a, b, true_tip, false_tip, literal in items:
            triples.append((clause_a, clause_b, true_tip if literal > 0 else false_tip))
        for _ in range(len(items) - 1):
            garbage_a, garbage_b = point(), point()
            for a, b, true_tip, false_tip, literal in items:
                triples.append((garbage_a, garbage_b, true_tip))
                triples.append((garbage_a, garbage_b, false_tip))

    return universe_size, triples, wheel_true


def construction(source):
    universe_size, triples, wheel_true = three_set_cover(source)
    singleton_masks = {1 << i for i in range(universe_size)}
    stars = {0}
    for a, b, c in triples:
        stars.update(((1 << a) | (1 << b), (1 << a) | (1 << c),
                      (1 << b) | (1 << c), (1 << a) | (1 << b) | (1 << c)))
    stars -= singleton_masks

    def bits(mask):
        return "".join("1" if mask & (1 << i) else "0" for i in range(universe_size))

    accepted = {bits(mask) + "11" for mask in singleton_masks | stars}
    accepted.update(bits(mask) + ("10" if mask.bit_count() & 1 else "01") for mask in stars)
    target = {"n": universe_size + 2, "accepted": sorted(accepted),
              "K": len(stars) + universe_size // 3}
    return target, triples, wheel_true


def extract(source, target_solution):
    simple = easy_answer(source)
    if simple is not None:
        return simple
    if target_solution == "NO-SOLUTION":
        return "NO-SOLUTION"
    target, triples, wheel_true = construction(source)
    universe_size = target["n"] - 2
    subset_to_triple = {}
    for index, (a, b, c) in enumerate(triples):
        for mask in (0, 1 << a, 1 << b, 1 << c, (1 << a) | (1 << b),
                     (1 << a) | (1 << c), (1 << b) | (1 << c),
                     (1 << a) | (1 << b) | (1 << c)):
            subset_to_triple.setdefault(mask, index)
    chosen = set()
    for term in target_solution["terms"]:
        if term[-2] == -1 or term[-1] == -1:
            continue
        positives = [i for i, value in enumerate(term[:universe_size]) if value == 1]
        if len(positives) > 1:
            continue
        if len(positives) == 1 and term[positives[0]] == -1:
            continue
        if not any(value != -1 for value in term[:universe_size]):
            continue
        mask = sum(1 << i for i, value in enumerate(term[:universe_size]) if value != -1)
        chosen.add(subset_to_triple[mask])
    return {"cover": [j for j in range(len(source["sets"])) if wheel_true[j + 1] in chosen]}


def main():
    source = json.load(sys.stdin)
    if sys.argv[1:] == ["--extract"]:
        print(json.dumps(extract(source["source"], source["target_solution"])))
    elif len(sys.argv) == 1:
        simple = easy_answer(source)
        print(json.dumps((YES_TARGET if simple != "NO-SOLUTION" else NO_TARGET)
                         if simple is not None else construction(source)[0]))
    else:
        raise ValueError("unknown arguments")


if __name__ == "__main__":
    main()

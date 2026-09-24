# Prepare: independent test foundation

Prepared on 2026-09-23, before any candidate construction. Source and target encodings are in [contract.md](contract.md). Run from the repository root:

```sh
uv sync --locked
uv run --locked python3 campaigns/set-cover-minimum-dnf/work/check.py --self-test
uv run --locked python3 campaigns/set-cover-minimum-dnf/work/check.py --candidate campaigns/set-cover-minimum-dnf/work/algorithm.py
```

The fixed corpus contains 115 distinct legal inputs: 15 designed edge cases and 100 cases from `generate_cases.py` with recorded integer seeds. Universe sizes range from 0 to 6; 54 are YES and 61 are NO. `cases.json` stores an exhaustive source witness or `NO-SOLUTION` for each case. The generator uses Python's seeded `random.Random`; `--self-test` regenerates each random case, first runs the copied corpus gate, recomputes its answer by combinations, independently solves its decision with Z3 5.1.0, and checks the returned witness directly. Designed cases include empty universes, no sets, duplicate and empty sets, uncovered elements, tight and loose bounds, and multiple valid covers. The check also rejects malformed or false source and target witnesses and checks target infeasibility directly.

The source Z3 encoding uses one Boolean per set, a cardinality bound, and one disjunction for each universe element. Its satisfying assignments are exactly covers using at most `k` sets. The separate exhaustive oracle enumerates index combinations and checks their union; agreement of the two is checked on every corpus case. `NO-SOLUTION` is accepted only after exhaustive absence of covers. The target oracle starts with the accepted minterms and repeatedly merges pairs of complete subcubes that differ in one fixed bit. Induction on the number of free bits shows that this enumerates every nonempty cube wholly contained in `A`; it works even when `n` is much larger than `|A|`. Z3 selects at most `K` such cubes covering every accepted assignment. An unsatisfiable Z3 result proves no such DNF exists. The output validator independently counts accepted points matched by each term and compares that count with the cube's `2^d` assignments, then checks their union equals `A`. Unknown solver status raises an error.

The candidate driver executes both maps as separate subprocesses, solves each constructed target independently, validates each target output, then checks recovered source feasibility and the independently stored YES/NO label. It samples up to three distinct valid target DNFs per satisfiable target and always sends `NO-SOLUTION` through recovery for an infeasible one. The sparse-cube revision removed the former `n <= 8` bound before candidate construction; the earlier self-test evidence is retained in Git commit `1b8caf0`. Large accepted lists or many subcubes may still be computationally expensive, so a solver execution failure remains inconclusive. Exhaustive source search is practical only on this small corpus. This preparation establishes the test foundation, not a reduction proof.

Observed command: `uv run --locked python3 campaigns/set-cover-minimum-dnf/work/check.py --self-test` → `Preparation corpus passed: 115 distinct cases, 100 random, 15 edge` and `self-test passed: 115 cases (54 YES, 61 NO), Z3 5.1.0`. The oracle revision is grounded in exact cube semantics, not a changed candidate expectation.

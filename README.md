# Set Cover → Minimum DNF with a term bound

**Status:** `ready_for_expert_review` · **Research model:** Codex `gpt-6-sol` · **Submitted:** 2026-09-24

This archive gives deterministic polynomial-time maps from Set Cover to exact DNF minimization with an explicit accepted-assignment list and a term bound. Every valid target DNF recovers a source cover, and a valid target `NO-SOLUTION` recovers source infeasibility. The result reconstructs known DNF-hardness ingredients for the fixed search contract; human expert acceptance remains pending.

## Construction

The source cover condition becomes CNF with a cardinality circuit. A three-element exact-cover gadget encodes the CNF, and sparse one-hot downsets with parity completion give the target accepted list. Recovery turns terms covering one-hot points into gadget triples; the term bound forces an exact cover, whose wheel choices decode the source cover.

## Evidence

- **Correctness and recovery:** A [general proof](campaigns/set-cover-minimum-dnf/work/proof.md) covers every legal source input and every valid target output. A [fresh-context independent agent review](campaigns/set-cover-minimum-dnf/reviews/initial/review.md) advanced the candidate to expert review; human acceptance is pending.
- **Polynomial bounds:** The [proof](campaigns/set-cover-minimum-dnf/work/proof.md) bounds construction, explicit accepted-list size, recovery and encoded parameters. The list can still be large in practice.
- **Executable checks:** The fixed corpus has 100 seeded random and 15 edge cases. [Prepared injection](campaigns/set-cover-minimum-dnf/rounds/002/candidate-run.log) passed 115 source cases and 133 target outputs, including 61 `NO-SOLUTION` outputs. [Separate Kissat verification](campaigns/set-cover-minimum-dnf/work/verification.md) passed four source cases and five target outputs, including hard YES and NO instances. These finite checks support implementation behavior; they do not prove the general theorem.
- **Acceptance limits:** No Lean formalization, human expert verification or upstream integration is recorded. The [campaign state](campaigns/set-cover-minimum-dnf/state.md) distinguishes these from the independent agent review.

## Reproduce

Run from the repository root with Python 3.12, uv, Z3 and Kissat available:

```sh
uv sync --locked
uv run --locked python3 campaigns/set-cover-minimum-dnf/work/check.py --self-test
uv run --locked python3 campaigns/set-cover-minimum-dnf/work/check.py --candidate campaigns/set-cover-minimum-dnf/work/algorithm.py
uv run --locked python3 campaigns/set-cover-minimum-dnf/work/verify.py --candidate campaigns/set-cover-minimum-dnf/work/algorithm.py
```

The self-test checks the independently fixed corpus; the next two commands solve actual target instances and validate recovered source answers. The [paper appendix](campaigns/set-cover-minimum-dnf/work/manuscript.pdf) records versions, outputs and finite-check limits. The universal claim rests on the written proof.

## Artifacts

- [Fixed question](campaigns/set-cover-minimum-dnf/question.md)
- [Campaign state and round history](campaigns/set-cover-minimum-dnf/state.md)
- [Manuscript PDF](campaigns/set-cover-minimum-dnf/work/manuscript.pdf)
- [Construction and recovery](campaigns/set-cover-minimum-dnf/work/algorithm.py)
- [General proof](campaigns/set-cover-minimum-dnf/work/proof.md)
- [Independent review](campaigns/set-cover-minimum-dnf/reviews/initial/review.md)
- [Verification evidence](campaigns/set-cover-minimum-dnf/work/verification.md)

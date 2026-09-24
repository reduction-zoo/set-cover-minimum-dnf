# Round 002 — bounded-set intermediary

## Plan

Gap: Gimpel's sparse accepted-set construction is polynomial when every source set has constant size, but the fixed source admits arbitrarily large sets.

Hypothesis: transform arbitrary Set Cover into a 3-uniform Set Cover instance with a polynomial budget and a polynomial witness decoder; then apply Gimpel's construction and parity completion. This route would avoid the exponential closure identified in round 001.

First discriminating check: build a concrete intermediary, trace its YES/NO correspondence and decoder, and bound its size. A graph vertex-cover encoding is an initial bridge; the decisive question is whether its degree can be bounded without losing the cover budget or recovery. If only an abstract NP-completeness appeal remains, this round is inconclusive for the required executable F/G.

Experience search: no local board entries directory exists. Relevant prior evidence: round 001's exponential closure and the restricted-source construction in Hellerstein et al. §3.

## Evidence and diagnosis

The intermediary is explicit. Source set variables and a Tseitin cardinality circuit produce CNF. A cyclic wheel per CNF variable, clause triples and local garbage triples produce a 3-partite exact-cover instance. The published sparse downset and parity completion map that instance to the exact accepted-list target. [The candidate](../../work/algorithm.py) implements both directions and [the proof](../../work/proof.md) gives the general decoder and polynomial bounds. The intermediary uses local garbage points per clause, so it does not need a global quadratic garbage crossbar.

The first check is **supported**: any CNF satisfying assignment yields an exact cover of the three-element triples, and every exact cover forces a uniform wheel mode per variable and one satisfied literal per clause. This supplies a polynomial witness decoder for arbitrary source Set Cover, closing the restriction identified in round 001.

`uv run --locked python3 campaigns/set-cover-minimum-dnf/work/check.py --candidate campaigns/set-cover-minimum-dnf/work/algorithm.py` passed 115 prepared cases and 133 target outputs. Nine cases exercised the full gadget; 61 sent `NO-SOLUTION` through recovery. The largest target had 1,838 variables and 14,870 accepted assignments. Full output: [candidate-run.log](candidate-run.log). Separate Kissat verification passed four cases and five outputs, including a hard-branch YES with two valid target DNFs and a hard-branch NO: [verify-run.log](verify-run.log), [verification report](../../work/verification.md).

An earlier full run was manually interrupted at source case 8 after target-oracle work became slow. It returned `unknown` only because SIGINT interrupted Z3; it was not interpreted as target infeasibility. Case 8 is preserved in the fixed corpus. Diagnosis: the initial validator scanned every accepted assignment for every returned term, and the broad set-cover encoding did not exploit maximal cubes or forced cubes. The definition-equivalent oracle repairs were self-tested and the full run then passed. No candidate expectation was changed.

Primary proof audited locally: [Hellerstein et al., Lemmas 3.1 and 3.3](https://www.cs.rutgers.edu/~allender/papers/mindnf.pdf), accessed 2026-09-23. These cover the sparse downset and parity phases; the SAT/three-set bridge and implementation-specific decoder are proved in our proof file. Novelty is not claimed. Independent correctness, novelty and significance review remains pending.

Experience extraction (2026-09-24): [bounded-set parity completion](../../../../research/experience/bounded-set-parity-completion.md), a proposed reusable entry pending promotion to the board's local collection after review.

## Next action

Hold the candidate fixed for registered independent review. If it advances, write and inspect the Typst manuscript.

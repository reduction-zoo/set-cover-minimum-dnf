# Round 001 — incidence coordinates and exact completion

## Plan

Gap: a set-cover incidence pattern gives useful candidate cubes but the exact target lists every accepted assignment, so an unintended cube may undercut the cover bound and completion may be exponential.

Hypothesis: encode each source element as a binary assignment whose coordinates say which source sets contain it; a set is represented by a coordinate literal. Find a polynomial-size accepted-assignment completion or show a concrete obstruction. This would permit recovery from every short DNF by assigning each term to a source set, including terms with multiple literals.

First discriminating check: calculate the full truth-table closure of the accepted points under intended literals on small incidence patterns and search for an unintended implicant that is cheaper than the source cover. A polynomial bound and a canonicalization lemma would support the route; a superpolynomial closure family or explicit unintended cheap cube would refute this form.

Experience search: the board's `research/experience/entries/` directory is absent; no applicable local entry found. Search primary literature for the exact-completion bridge as supporting evidence.

## Evidence and diagnosis

The first check is conclusive for this particular incidence encoding. Take universe `[m]`, the sole set `[m]`, and `k=1`. With one-hot element assignments and a set term that fixes only coordinates outside its set, the intended term has no literals. Exact DNF semantics therefore require the accepted list to contain every one of the `2^m` Boolean assignments. The source representation has `O(m log m)` bits, so this completion is superpolynomial in input length. The counts are 16, 256 and 4096 for `m=4,8,12`; the general `2^m` formula is the relevant bound. The same issue appears for any set of size `r`, whose intended cube contains `2^r` assignments. A second defect arises if coordinates indicate set membership: distinct elements with identical incidence rows collapse into one assignment, so they cannot by themselves carry separate recovery obligations.

Outcome: **refuted** for direct one-hot/coordinate-literal completion. This does not rule out bounded-set preprocessing, a different code, or a gadget that changes the target function. The supported cause is explicit closure under a large intended cube, not an oracle failure.

Primary source checked 2026-09-23: [Hellerstein, Kletenik, McCabe, and Servedio, *Minimizing DNF Formulas and AC0 Circuits Given a Truth Table*, §3](https://www.cs.rutgers.edu/~allender/papers/mindnf.pdf). It explicitly notes that Gimpel's one-hot first phase can have exponential truth tables and obtains a polynomial table after restricting the source to 3-partite set cover. This agrees with the obstruction but does not itself give a direct reduction from arbitrary set cover under our fixed input contract.

Experience extraction: none. This is a standard size obstruction already explicit in the cited primary proof; no new reusable finding beyond this round record.

## Next action

Investigate a bounded-set intermediary with solution recovery, then audit the published parity completion before implementing it.

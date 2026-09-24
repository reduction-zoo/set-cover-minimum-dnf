# Bounded-set parity completion for exact DNF

Tags: set cover, bounded set size, explicit accepted assignments, DNF, parity completion, witness recovery.

## Claim and applicability

If a search problem admits a polynomial, witness-recoverable reduction to a set-cover family with sets of constant size `r`, the one-hot downset construction followed by Gimpel's parity completion yields a polynomial-size explicit accepted-assignment instance of bounded-term exact DNF. A target DNF within the bound can be decoded through partial-function terms back to a cover. For unbounded `r`, one downset can contain `2^r` assignments, so this size argument no longer applies. The intermediary itself must have a polynomial output and decoder.

## Evidence and status

General lemma: [Hellerstein et al., Lemmas 3.1 and 3.3](https://www.cs.rutgers.edu/~allender/papers/mindnf.pdf), checked 2026-09-23. Local composition and decoder: [round 002 proof](../../campaigns/set-cover-minimum-dnf/work/proof.md), with [finite checks](../../campaigns/set-cover-minimum-dnf/work/verification.md). Independent review pending. The round 001 [counterexample](../../campaigns/set-cover-minimum-dnf/rounds/001/round.md) demonstrates the exponential ceiling for an unbounded intended cube.

## Consequence for search

First seek a bounded-set intermediary with solution recovery; then use the sparse accepted-list version of parity completion. Do not treat an arbitrary prescribed implicant table or a partial function as an exact polynomial-size DNF instance without the explicit-list bound.

Intended destination: board-local `research/experience/entries/`, pending human-approved promotion. This campaign does not edit the board.

## Use history

Origin: [round 002](../../campaigns/set-cover-minimum-dnf/rounds/002/round.md), where the bounded-set route produced a complete candidate and finite passing checks. No later use recorded.

# Campaign state

Status: complete candidate and passing finite checks; independent review pending.
Budget: 20 rounds. Used: 2. Remaining: 18.
Board source: d56f22aee71c281b1a9b7aa90e65a0d2607efdce.

Capability probe (2026-09-23):

| Capability | Version / provider or path | Status |
|---|---|---|
| Python | 3.12.14, `/Users/xiweipan/.local/bin/python3`; uv project selects CPython 3.12.14 | available |
| uv | 0.12.17, `/Users/xiweipan/.local/bin/uv` | available |
| SMT | Z3 5.1.0 executable `/opt/homebrew/bin/z3`; `z3-solver` 5.1.0.0 locked in `uv.lock` | available, oracle selected |
| SAT | Kissat 4.0.4, `/opt/homebrew/bin/kissat` | available |
| CP-SAT | no executable or Python binding found in PATH/project | pending; not needed for selected oracle |
| Typst | 0.15.1, `/opt/homebrew/bin/typst` | available |
| Lean and Lake | Lean 4.34.0 and Lake 5.0.0, `/opt/homebrew/bin/lean`, `/opt/homebrew/bin/lake` | available |
| Mathlib | no local project or Mathlib checkout found | pending; formalization not requested |
| External writing skill | `sci-brain:how-to-technical-writing`, installed under `/Users/xiweipan/.codex/plugins/cache/sci-brain/` | available |

Testing foundation: [contract](work/contract.md), [cases](work/cases.json), [oracles and injected driver](work/check.py), [preparation record](work/preparation.md). Self-test: 115 cases, 54 YES, 61 NO, exhaustive source labels agreed with Z3 5.1.0. Sparse target implicants are enumerated from the accepted list.

Current claim: [candidate F/G](work/algorithm.py) and [general proof](work/proof.md) reconstruct the reduction by composing SAT, three-set exact cover and published parity completion. [Prepared injection](rounds/002/candidate-run.log) passed 115 source cases and 133 target outputs; [separate Kissat verification](work/verification.md) passed hard YES and NO cases. Independent correctness, novelty and significance judgments are pending. Main obstacle: review of the full composition; no known counterexample. Prospects for a reviewed reconstruction: high, an uncalibrated judgment based on proof and finite checks.
Next action: registered fresh-context independent review. Then write the Typst paper if advanced.

| Round | Mechanism / scope | First check | Outcome | Evidence |
|---|---|---|---|---|
| 001 | One-hot incidence cube completion | Size of a full-set cube | refuted | [round 001](rounds/001/round.md) |
| 002 | SAT to bounded three-set cover, then sparse downset/parity completion | CNF wheel gadget and decoder | supported | [round 002](rounds/002/round.md) |

Experience: one proposed entry created, none updated, one pending board-local promotion: [bounded-set parity completion](../../research/experience/bounded-set-parity-completion.md). No board writes.

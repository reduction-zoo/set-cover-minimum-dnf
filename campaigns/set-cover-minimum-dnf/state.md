# Campaign state

Status: preparation complete; construction open.
Budget: 20 rounds. Used: 1. Remaining: 19.
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

Testing foundation: [contract](work/contract.md), [cases](work/cases.json), [oracles and injected driver](work/check.py), [preparation record](work/preparation.md). Self-test: 115 cases, 54 YES, 61 NO, exhaustive source labels agreed with Z3 5.1.0. Target oracle is finite at `n <= 8`.

Current claim: no complete rule. Correctness, novelty and significance are unassessed. Main obstacle: an exact explicit truth-table construction with controlled unintended implicants. Prospects within budget: unknown (uncalibrated judgment).
Next action: investigate a bounded-set intermediary and the published parity completion.

| Round | Mechanism / scope | First check | Outcome | Evidence |
|---|---|---|---|---|
| 001 | One-hot incidence cube completion | Size of a full-set cube | refuted | [round 001](rounds/001/round.md) |

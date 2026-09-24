# Set Cover → Minimum DNF with a term bound

Independent research campaign. An executable search reduction and general proof are ready for human expert review. The result reconstructs known DNF hardness machinery; it does not claim a new complexity theorem.

[Paper](campaigns/set-cover-minimum-dnf/work/manuscript.pdf) · [Proof](campaigns/set-cover-minimum-dnf/work/proof.md) · [Algorithm](campaigns/set-cover-minimum-dnf/work/algorithm.py) · [Independent review](campaigns/set-cover-minimum-dnf/reviews/initial/review.md) · [State](campaigns/set-cover-minimum-dnf/state.md) · [Question](campaigns/set-cover-minimum-dnf/question.md)

Two of 20 rounds were used. The fixed 115-case corpus, independent target checks, and separate SAT verification passed. From `campaigns/set-cover-minimum-dnf/work/`, reproduce with `uv sync --locked`, `uv run --locked python3 check.py --candidate algorithm.py`, and `uv run --locked python3 verify.py --candidate algorithm.py` (the last command requires Kissat on `PATH`). The paper appendix records tool versions, exact output counts, and limitations.

Board source commit: d56f22aee71c281b1a9b7aa90e65a0d2607efdce.

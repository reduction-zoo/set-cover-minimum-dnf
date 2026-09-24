# Final manuscript inspection — 2026-09-24

Compiled `manuscript.typ` to `manuscript.pdf` from `campaigns/set-cover-minimum-dnf/work/` using Typst 0.15.1:

```sh
typst compile manuscript.typ manuscript.pdf
```

The final PDF has five pages. Each page was rendered and visually inspected after the final technical-writing pass. Page 1 contains the theorem and wheel incidence figure; its labels and caption are legible. Pages 2–4 contain the construction, proofs, bounds, discussion, and reference without clipped text or misplaced formula scope. Page 5 contains the complete verification and reproducibility appendix with legible commands and results. No page break separates a formula from its setup. The final compile succeeded without diagnostics.

The figure generator `figures/make_wheel.py` checked that every drawn triple has three distinct points, each core point has degree two, and each clause port has degree one. The final PDF SHA-256 is `0c3dad4c017fded644010f75c4e3d26f52ff22ddbcf92f698758e6c62570d218`. Rendered inspection images were temporary; the PDF and Typst source are retained.

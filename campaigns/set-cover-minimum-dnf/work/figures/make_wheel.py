"""Draw the exact incidence matrix of the two-occurrence wheel and a clause port."""

from pathlib import Path


points = ["a₁", "a₂", "b₁", "b₂", "T₁", "T₂", "F₁", "F₂", "cA", "cB"]
triples = [
    ("H₁", {"a₁", "b₁", "F₁"}),
    ("H₂", {"a₂", "b₂", "F₂"}),
    ("L₁", {"a₁", "b₂", "T₁"}),
    ("L₂", {"a₂", "b₁", "T₂"}),
    ("C₁", {"cA", "cB", "T₁"}),
]
assert all(len(edge) == 3 and edge <= set(points) for _, edge in triples)
assert len(set(points)) == len(points)
degree = {point: sum(point in edge for _, edge in triples) for point in points}
assert all(degree[point] == 2 for point in ("a₁", "a₂", "b₁", "b₂"))
assert degree["T₁"] == 2 and degree["cA"] == degree["cB"] == 1

parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="360" viewBox="0 0 900 360">',
         '<rect width="900" height="360" fill="white"/>',
         '<style>text{font-family:Arial,sans-serif;fill:#111} .label{font-size:20px} .small{font-size:17px}</style>',
         '<text x="28" y="39" class="label" font-weight="bold">triple</text>',
         '<text x="350" y="39" class="label" font-weight="bold">points</text>']
for j, point in enumerate(points):
    x = 180 + 70 * j
    parts.append(f'<text x="{x}" y="82" class="label" text-anchor="middle">{point}</text>')
for i, (name, edge) in enumerate(triples):
    y = 122 + i * 48
    if i in (0, 1):
        parts.append(f'<rect x="20" y="{y-29}" width="850" height="45" fill="#eeeeee"/>')
    if i == 4:
        parts.append(f'<line x1="20" y1="{y-31}" x2="870" y2="{y-31}" stroke="#333" stroke-width="2" stroke-dasharray="7 5"/>')
    parts.append(f'<text x="43" y="{y}" class="label">{name}</text>')
    for j, point in enumerate(points):
        x = 180 + 70 * j
        parts.append(f'<circle cx="{x}" cy="{y-6}" r="7" fill="{("#111" if point in edge else "white")}" stroke="#111" stroke-width="1.5"/>')
parts.append('<text x="35" y="350" class="small">H: true wheel   L: false wheel   C: positive clause literal at occurrence 1</text>')
parts.append('</svg>')
Path(__file__).with_name("wheel.svg").write_text("\n".join(parts) + "\n")

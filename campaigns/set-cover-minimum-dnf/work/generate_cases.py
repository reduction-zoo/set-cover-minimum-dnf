"""Fixed, reproducible small Set Cover cases; no candidate knowledge."""

import json
import random
from pathlib import Path


EDGE = [
    (0, [], 0), (0, [[]], 0), (0, [[], []], 1),
    (1, [], 0), (1, [[]], 1), (1, [[0]], 0),
    (1, [[0]], 1), (1, [[0], [0]], 1),
    (2, [[0], [1]], 1), (2, [[0], [1]], 2),
    (2, [[0, 1]], 1), (2, [[0], []], 2),
    (3, [[0, 1], [1, 2], [0, 2]], 2),
    (3, [[0, 1], [1, 2], [0, 2]], 1),
    (3, [[0, 1], [1, 2]], 3),
]


def from_seed(seed):
    rng = random.Random(seed)
    m = rng.randrange(1, 7)
    count = rng.randrange(1, 8)
    sets = [[e for e in range(m) if rng.randrange(2)] for _ in range(count)]
    k = rng.randrange(count + 2)
    return {"universe_size": m, "sets": sets, "k": k}


def main():
    cases = [{"source": {"universe_size": m, "sets": sets, "k": k}, "kind": "edge"}
             for m, sets, k in EDGE]
    seen = {json.dumps(case["source"], sort_keys=True) for case in cases}
    seed = 0
    while sum(case["kind"] == "random" for case in cases) < 100:
        source = from_seed(seed)
        key = json.dumps(source, sort_keys=True)
        if key not in seen:
            cases.append({"source": source, "kind": "random", "seed": seed})
            seen.add(key)
        seed += 1
    Path(__file__).with_name("cases.json").write_text(json.dumps(cases, indent=2) + "\n")


if __name__ == "__main__":
    main()

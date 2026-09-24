# Encodings and solution contract

Source JSON is `{"universe_size": m, "sets": [[e,...],...], "k": k}`. Here `m,k` are nonnegative integers, each set is a list of distinct integers in `[0,m)`, and duplicate sets and empty sets are legal. Indexing is only a naming convention for an arbitrary explicitly given finite universe. A valid source output is `{"cover": [i,...]}` with distinct set indices, length at most `k`, whose union is the universe, or the JSON string `"NO-SOLUTION"` exactly when no cover exists.

Target JSON is `{"n": n, "accepted": [b,...], "K": K}`. `n,K` are nonnegative integers and each `b` is a distinct length-`n` binary string. An empty string is the sole assignment when `n=0`. A target output is `{"terms": [[l,...],...]}` with at most `K` terms; every term has length `n` and each entry is `-1`, `0`, or `1` for a negated, absent, or positive literal. The DNF must satisfy exactly the listed assignments. The output `"NO-SOLUTION"` is valid exactly when no such DNF exists. Duplicate terms are allowed.

`algorithm.py` reads one source JSON value on stdin and emits a target JSON value on stdout. `algorithm.py --extract` reads `{"source": x, "target_solution": y}` and emits a valid source output. Both commands are deterministic, use fresh processes, and report errors with a nonzero exit status.

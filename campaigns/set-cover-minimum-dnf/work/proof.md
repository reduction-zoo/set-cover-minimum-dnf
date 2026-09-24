# A polynomial reduction for the fixed search contract

The implementation is [algorithm.py](algorithm.py). The source and target encodings and special outputs are [fixed in contract.md](contract.md). The central partial-function and parity-completion lemmas are the published construction of Hellerstein, Kletenik, McCabe, and Servedio, [*Minimizing DNF Formulas and AC0 Circuits Given a Truth Table*, Lemmas 3.1 and 3.3](https://www.cs.rutgers.edu/~allender/papers/mindnf.pdf), which attributes the underlying construction to Gimpel. The SAT-to-three-set gadget and the full composition below are specified and proved here. This is a reconstruction of known hardness machinery, not a novelty claim.

## Easy instances

If the universe is empty, the source output is the empty cover. If any element belongs to no set, or `k=0` with a nonempty universe, the source output is `NO-SOLUTION`. If `k≤2`, all singleton and pair choices can be checked in polynomial time. If `k` is at least the number of sets and their union is the universe, all sets form a valid cover. The forward map sends a known YES case to `n=0, A={ε}, K=1`, and a known NO case to `n=1, A={0}, K=0`. The former has an exact one-term DNF and the latter has no zero-term DNF. Recovery recomputes the known source output from the input. Hence the contract holds for every valid target output in these branches.

In the remaining case there are `m` source sets, `3 ≤ k < m`, and every universe element occurs in a set.

## Source cover to CNF

Create variables `x_1,...,x_m`, one per source set. For each universe element `e`, add the clause `∨_{j:e∈S_j} x_j`. Introduce Tseitin variables for the recurrence

`s_{0,0}=true`, `s_{0,j}=false` for `j>0`, and `s_{i,j}=s_{i-1,j} ∨ (x_i ∧ s_{i-1,j-1})` for `1≤i≤m,1≤j≤k+1`, with `s_{i,0}=true`. Each AND and OR gate is encoded in both directions by its three standard CNF clauses; constant inputs are folded. Add the unit clause `¬s_{m,k+1}`. Any satisfying assignment chooses at most `k` sets and covers every element. Conversely, a source cover sets its `x_j` variables accordingly and extends uniquely through the gates to satisfy the CNF. Thus the original instance is YES exactly when this CNF is satisfiable, and the first `m` variable values of any satisfying assignment give a valid source cover.

## CNF to three-element exact cover

Give each literal occurrence `o` four distinct points `a_o,b_o,T_o,F_o`. For each CNF variable, list its `r` occurrences cyclically. For every occurrence `o_i`, add the two triples

`(a_i,b_i,F_i)` and `(a_i,b_{i+1},T_i)`, with cyclic subscript. The first is its true-mode wheel triple; the second is its false-mode wheel triple. Every `a_i` appears only in these two wheel triples. Any exact cover must choose one per occurrence. The `b_i` points force all choices on the same variable's cycle to use the same mode: a change of mode leaves one `b_i` uncovered and another doubly covered. In true mode the `T_i` tips remain free; in false mode the `F_i` tips remain free.

For a clause with `l≥1` literal occurrences, add two points `c_A,c_B` and one triple `(c_A,c_B,T_o)` for every positive occurrence, or `(c_A,c_B,F_o)` for every negative occurrence. Add `l−1` pairs of garbage points; for each pair, add a triple with either tip of every occurrence in this clause. Clause points force exactly one clause triple, using a tip left free precisely when its literal is true. The garbage pairs consume all other free tips of that clause. Conversely, a satisfying assignment chooses its wheel modes, any satisfied literal per clause, and matches the other `l−1` free tips to garbage pairs. The choices form an exact cover.

If the CNF has `R` literal occurrences and `C` clauses, the three disjoint parts each contain `2R` points: occurrence `a`/`b`/tips contribute `R,R,2R`; clause pairs contribute `C,C,0`; and garbage pairs contribute `R−C,R−C,0`. Every triple has one point in each part. The universe therefore has `N=6R` points. A cover by at most `2R=N/3` triples must be exact because each triple contains three points. The preceding argument proves that such a cover exists exactly when the CNF is satisfiable. From any such cover, inspecting one wheel triple of each variable recovers the satisfying assignment.

## Three-set cover to an exact DNF instance

For each of the `N` intermediary universe points, let `v_i` be its one-hot Boolean vector of length `N`. For each triple `S`, let `w_S` be its incidence vector. Let `D` be the union of the downsets `{x:x≤w_S}`. Define the partial function `f` to be 1 on the one-hot vectors, unspecified on `D\V`, and 0 elsewhere. Write `R_* = D\V` and `s=|R_*|`. A triple's downset has eight vectors, so `s≤1+4T` for `T` intermediary triples. The target has `n=N+2` variables and accepted assignments

`A = {(x,1,1):x∈D} ∪ {(x,p(x),1−p(x)):x∈R_*}`,

where `p(x)` is the parity of `x`. Set `K=s+2R`. The explicit list is built by enumerating the zero, pair and triple masks from each three-element intermediary set, plus all one-hot masks; no `2^N` scan occurs.

A cover by `q` intermediary triples yields `q` terms for `f`: for each selected `w_S`, take the conjunction of `¬x_i` at every zero coordinate of `w_S`. These cover the one-hot points and contain no zero of `f`. For each star `x∈R_*`, add the term fixing every `x` coordinate and fixing the one auxiliary coordinate whose value is 1 in `(p(x),1−p(x))`. It covers both `(x,1,1)` and its parity point. Append positive literals for both auxiliary variables to the `q` partial-function terms. The resulting exact DNF has `s+q` terms. In particular, a source YES instance gives a target DNF with at most `K` terms.

Conversely, take **any** exact DNF with at most `K` terms. Each parity point `(x,p(x),1−p(x))` requires a distinct term: changing any original bit reverses parity and reaches a rejected point with the same two auxiliary bits, so its covering term fixes every original bit. Such a term cannot cover a one-hot point because stars exclude one-hot vectors. Thus at least `s` terms are unavailable for covering `(v_i,1,1)`. Each term that covers such a one-hot point must fix both auxiliary variables positively: changing either to zero gives a rejected point. Removing those auxiliary literals leaves a term consistent with `f`. Let `u` be the maximal original-variable vector satisfying that term. Since `(u,1,1)` must be accepted, `u∈D`, so `u≤w_S` for some intermediary triple `S`. Assign that triple to the term. Every one-hot point covered by the term corresponds to a point in `S`. These assigned triples cover all `N` intermediary points and number at most `K−s=2R`; hence they form an exact cover. The wheel choices decode a CNF assignment and the first `m` values decode a source cover. This argument also handles duplicate, redundant, nonprime and alternate valid target DNFs. If the target output is `NO-SOLUTION`, the forward implication shows the source cannot have a cover, so recovery returns `NO-SOLUTION`.

## Size and time

Let `L` be the source JSON length. In the hard branch, `m`, the universe size and `k` are at most `O(L)` because every universe point is explicitly covered and `k<m`. The CNF has `O(mk)` gates plus the source incidence clauses and `R=O(L+mk)` literal occurrences. A clause has at most `max(m,3)` literals. The intermediary has `N=6R` points and `T=O(R+Σ_c l_c²)=O(Rm)` triples, since each garbage pair offers at most `2l_c` triples. Its list is polynomial. The star set has at most `1+4T` masks; the accepted set has at most `N+2(1+4T)` strings of length `N+2`. Therefore the target encoding and forward runtime are `O((N+T)N)` up to polynomial integer and JSON overhead, hence polynomial in `L`. The bound `K` has `O(log(N+T))` bits. Recovery reconstructs this metadata from `source`, scans the target terms, maps each original-variable maximal vector to one of the enumerated triples, and reads the wheel choices. Its time and output size are polynomial in `L+|y|`. Neither direction calls a source or target solver.

The output-size bound is deliberately coarse. The many accepted assignments make this a proof construction, not an efficient minimization pipeline at large scale.

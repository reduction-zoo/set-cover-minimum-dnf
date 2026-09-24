# Fixed question

```json
{
  "source": "Set Cover",
  "target": "Minimum DNF with a term bound",
  "category": "Construction open",
  "summary": "The task reconstructs a bridge from set covering to exact Boolean expression minimization.",
  "source_definition": "Given a finite universe, an explicit family of subsets and k, return at most k subsets covering the universe, or NO-SOLUTION. All finite combinatorial structures are explicit and numerical data use binary encoding.",
  "target_definition": "Given n Boolean variables, an explicit list A of accepted assignments and K, return a disjunctive normal form with at most K conjunctions of literals whose satisfying assignments are exactly A; return NO-SOLUTION if none exists. Unlisted assignments must be rejected, rather than treated as do-not-care values.",
  "required_result": "Construct deterministic polynomial-time maps F and G. F must produce a legal target instance, and G(x,y) must return a valid source output for every valid target output y, including NO-SOLUTION. A complete rule may reconstruct a published construction or give a new one; it must specify every gadget, numerical parameter and decoding step.",
  "acceptance": "Deliver executable instance construction and output recovery, a general proof covering all legal inputs and target outputs, and worst-case polynomial time and encoding-size bounds. Cite the actual proof used, or identify a newly derived argument. Check small positive and negative instances with independent solvers; finite tests alone do not establish correctness.",
  "importance": "The task reconstructs a bridge from set covering to exact Boolean expression minimization.",
  "difficulty": "Difficulty is not yet established by a construction attempt. A prescribed cover table is not by itself a polynomial-size truth-table construction. The proof must control unintended implicants and the number of explicitly listed assignments.",
  "openness": "The cited source points to Gimpel and later DNF-minimization literature. The task is to reconstruct a complete rule for the exact encoding stated here, not to assert that DNF hardness remains unknown.",
  "literature_checked": "2026-09-18",
  "coverage": "Import inventory review of the cited sources. Primary proofs have not been independently re-audited; availability of a complete reconstruction elsewhere remains unassessed.",
  "references": [
    {
      "title": "Problem-Reductions: Set Cover \u2192 Minimum DNF with a term bound",
      "url": "https://github.com/CodingThrust/problem-reductions/issues/865",
      "note": "Upstream issue and review discussion checked on 2026-09-18. Its references are reconstruction leads, not independently audited proof sources."
    }
  ],
  "solutions": [],
  "equation": ""
}
```

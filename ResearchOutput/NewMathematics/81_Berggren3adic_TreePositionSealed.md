# Paper 81 — BERGGREN-3ADIC: The Tree Position of the N-Node Is Adically Sealed

**Verdict name: THE-TREE-POSITION-IS-ADICALLY-SEALED.**
Round-24 #2 · exp 416 · assessment v192 · script `/tmp/exp_berggren3adic.py` · log `/tmp/r24n2.log` · runtime 154 s · sample 40,000 semiprimes (p, q uniform primes in [2¹⁶, 2²⁴); 42 censored descents = 0.10%, twin-prime stepwise cases).

## 1. The open face

Paper 56 (BERGGREN-PRICE-INTERLOCK) proved the Pythagorean trees *structurally orthogonal* to factoring: every odd semiprime N = pq is a node of the Berggren tree at its Fermat pair (m,n) = ((p+q)/2, (q−p)/2) with odd leg m²−n² = N exactly; the trees organize the ratio (p+q)/(q−p), not the product; the root→N path string IS the factorization. The Catalog independently carries two further objects: the **3-adic Cantor set of the Berggren boundary** (#855) and a gold-tier polynomial-time factorization claim by "interference of Pythagorean triples" (#829 — no formula in the index, untestable without strawmanning). The open question this round answers: **does the tree POSITION of the N-node — branch letters, depth, path composition — carry any N-visible (residue) structure?** Does the 3-adic Cantor boundary have an N-computable projection?

## 2. Predictions (stated before the run)

- **H1 (skeleton lemma).** Squares mod 3 are {0,1} and m ⊥ n, so N = m² − n² mod 3 pins the 3-class of the Fermat pair: **N ≡ 1 ⟺ 3|n; N ≡ 2 ⟺ 3|m; N ≡ 0 ⟺ 3∤mn** — expected 100%. But this RESTATES N mod 3 (3|n ⟺ q ≡ p mod 3 ⟺ N ≡ p² ≡ 1): a trace identity, zero new information (barrier 6).
- **H2 (parent-interval law).** The Berggren parent of a non-root node is decided by the ratio alone: m/n ∈ (1,2) → T₁ = (n, 2n−m); (2,3) → T₂ = (n, m−2n); (3,∞) → T₃ = (m−2n, n). A new exact statement — expected to hold on every descent step of every node.
- **H3 (metric blindness).** The entire metric layer of the path is residue-blind: I(N mod 3^k; b_t) ≈ 0 at the permutation null for every letter depth t ≤ 10 and every level k ≤ 6; likewise for the depth dB and the path composition (c₁,c₂,c₃).
- **H4 (live controls).** Trace lemma I(N mod 3; s mod 3) ≈ 1.000 bit (paper 50) — pipeline sanity; I(ratio band; b₁) = H(b₁) — the first letter is a *deterministic function of the m/n band*, whose recovery is the factorization (barrier 6).

## 3. Results

### H1 — skeleton: exact, and it restates the trace
Agreement **40000/40000 = 100%**. Restatement check (3|n ⟺ N ≡ 1 mod 3): **40000/40000**. The one N-visible position fact carries zero information beyond N mod 3.

### H2 — parent-interval law: exact
All **40000/40000** descents terminate exactly at the root (2,1). Spot verification of **86,634 descent steps**: interval membership + child-map reconstruction (B₁(m,n) = (2m−n, m), B₂ = (2m+n, m), B₃ = (m+2n, n)) exact on every step. The trichotomy is now an explicit lemma of the tree's Euclidean (subtract-2/reflect) descent — the structural reason the path string is ratio-data, not product-data.

### H3 — the metric layer is blind at every 3-adic level

| channel | levels | worst z (300-shuffle null) |
|---|---|---|
| branch letters b₁ … b₁₀ | 3^k, k = 1…6 | **+2.51** |
| Berggren depth dB | 3^k, k = 1…6 | < 3 |
| path composition (c₁,c₂,c₃) | 3^k, k = 1…6 | < 3 |

Every channel sits at its permutation null. Sample readings at k=1: I(N mod 3; b₁) = 0.00004 (null 0.00004, z = +0.04); b₂ z = −0.33; b₃ z = −0.35. **The 3-adic Cantor boundary has no N-computable projection beyond the trace-set content.**

### H4 — controls: pipeline live, letters pure metric
- Trace lemma: I(N mod 3; s mod 3) = **1.0000** (paper 50 reproduced exactly).
- Metric control: I(ratio band; b₁) = **1.4738 = H(b₁)** — determinism, confirming the letters are functions of the slope alone.
- Replication: corr(log dB, log gap) = **−0.141** — paper 56's anti-correlation of tree depth with Fermat cost (the tree measures the ratio, the opposite of product hardness).

## 4. What this decides

The tree-position channel decomposes into exactly two pieces, both sealed:

1. **A deterministic 3-adic skeleton** that is a trace-lemma identity — computing the 3-class of (m,n) from N mod 3 is computing N mod 3 (barrier 6);
2. **A metric layer** (letters, depth, composition) carrying rich structure — up to H(b₁) = 1.47 bits in the first letter alone — that is *invisible from N at every 3-adic level* (barrier 5 at adic strength).

This sharpens paper 56's orthogonality from "the coordinates are orthogonal" to "**coordinates orthogonal AND adically sealed**": the Catalog's 3-adic Cantor boundary (#855) organizes the tree's own boundary points, but its pullback to semiprime nodes is exactly the trace content. Tree-adic dials join the closed residue-dial family (papers 54/70/72–74/77/79/80): no member of the dial family — residue, spectral, or now tree-positional — exceeds its trace-set content, and the metric remainder requires the factorization to read. Any factorization claim riding on tree interference (#829) must therefore either smuggle the Fermat pair (circularity, barrier 6) or pay the Ω(N) aggregation of barrier 4; nothing in the index suggests a third route.

## 5. Barriers

**(a) Circularity — clean.** All four horns stated before the run; the measurement (Fermat pairs from known p,q) is the round's object, not its instrument.
**(b) Known-method-in-disguise — clean.** No tree-position channel work exists in the Catalog (nearest: our own echo #707; the boundary objects #855/#829 carry no N-side claims beyond the unformalized #829).
**(c) Toy-scale — confronted.** 40k real semiprimes, 16–24-bit primes, 86,634 verified descent steps, 300-shuffle nulls per channel per level (~150 channel tests).
**(d) Data leakage — clean.** Deterministic generation, fixed seeds.
**(e) Variance/reproducibility — the substance.** Blindness asserted against empirical nulls, not point zeros; censoring (0.10% twin-prime stepwise descents > 5000 steps) reported honestly; worst z = +2.51 < 3 across ~150 tests (no multiplicity correction needed).
**(f) Measurement errors — controlled.** Exact lemmas asserted at 100%; MI machinery identical to papers 78–81; ALL_DONE marker.
**(g) Baseline unfairness — clean.** Two live positive controls (trace lemma 1.0000; band-determinism 1.4738 = H(b₁)) prove the pipeline detects structure when it exists.
**(h) Practical relevance — the closure.** Symmetric by construction (n ≥ 0 absorbs the p,q swap); the skeleton is circular (barrier 6); the metric layer needs the factors (barrier 5/6); the descent is classical Euclidean algorithm in disguise (barrier 8).

## 6. What closes

The Pythagorean-tree line is now closed at three strengths: embedding exact (paper 56), coordinates orthogonal (paper 56), and **position adically sealed** (this paper). The trees organize the ratio (p+q)/(q−p); their every N-visible shadow reduces to the trace; their metric interior is the factorization wearing a path-string costume. Remaining above the line: nothing on the tree side — the frontier returns to the quantum channel (QUBIT-TRADE phase diagram) and the barrier-4 converse.

Now 416 experiments. Assessment v192. Paper 81, issue #173.

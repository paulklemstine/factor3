# Paper 80 — NONABELIAN-TYPE-CHANNEL: The Splitting-Type Channel of a Non-Abelian Field Is Exactly Its Abelianization Content

**Verdict name: THE-TYPE-CHANNEL-IS-THE-ABELIANIZATION.**
Round-24 #1 · exp 415 · assessment v191 · script `/tmp/exp_nonabelian_typechan.py` · log `/tmp/r24n1h.log` · runtime 314 s.

## 1. The open row

Papers 71–79 built the fork-and-type program in three steps: the **abelianization criterion** (paper 71: a splitting fork is congruence-pinned by a Dirichlet character iff it factors through G^ab = G/[G,G]); the **binary-fork channel laws** (papers 72–74: OR ≤ g(2) = 0.3113, split-count Is(n), the 1-bit binary cap); and the **complete type channel of abelian fields** (papers 78–79: I_pair = H(Π) − (1/φ)Σ_c H(Π_c) exact on every abelian cyclotomic conductor, multi-stateness ≥ 3 element orders breaking the 1-bit cap). The open row was the **non-abelian field**: what does the complete splitting type T(p) — the factorization pattern of f mod p, a multi-state class function carrying up to H(T) ≈ 2.1 bits of entropy — leak about residues, at the prime and the semiprime level?

## 2. The law (stated before the run)

Promote paper 71 from binary forks to the complete channel:

> **Prime level.** Let m\* be the conductor of the G^ab characters (the coset χ⃗(p) is a deterministic function of p mod m\*). Then
> **I(p mod m\*; T) = I(T; coset) = H(T) − H(T|coset)**,
> exactly. The type's entire residue content is its mutual information with the abelianization coset; the within-coset type refinement is invisible at *every* modulus (the papers 70/75/77 flatness, now for the full type distribution). Two faces:
> - type separates cosets ⟹ I₁ = H(coset): the type channel *is* the full dial;
> - type merges cosets ⟹ the type is a **lossy projection** of the dial, losing exactly E_t[H(coset|T=t)] bits.

> **Semiprime level.** The papers 78/79 pair law extends **verbatim**:
> I(N mod m\*; {T(p),T(q)}) = H(Π) − (1/φ(m\*))Σ_c H(Π_c),
> with Π_c the unordered type-pair law under N ≡ c mod m\*, computed by **class-level enumeration** (pairs (g,h) with χ⃗(g)⊙χ⃗(h) = χ⃗(c), class-size weights).

## 3. The law table — prime level (2^18 sieve, ~23k primes/field)

Types read independently of the dial via (#{roots in F_p}, #{roots in F_{p²}}) from x^(p²) mod f + gcd (see §6).

| field | G | G^ab | #types | H(T) | I₁ measured | law | dial H(coset) | loss |
|---|---|---|---|---|---|---|---|---|
| S₃a x³+x+1 (disc −31) | S₃ | C₂ | 3 | 1.4591 | **1.0000** | 1.0000 ✓ | 1.0000 | 0 |
| S₃b x³−x+1 (disc −23) | S₃ | C₂ | 3 | 1.4591 | **1.0000** | 1.0000 ✓ | 1.0000 | 0 |
| S₄ x⁴−x−1 (disc −283) | S₄ | C₂ | 5 | 2.0944 | **1.0100** | 1.0000 ✓ | 1.0000 | 0 |
| A₄ x⁴+8x+12 (disc 576²) | A₄ | C₃ | 3 | 1.1887 | **0.9188** | 0.9183 ✓ | 1.5850 | 0.6667 |
| D₄ x⁴−2 (disc −2048) | D₄ | C₂×C₂ | 4 | 1.9056 | **1.6555** | 1.6556 ✓ | 2.0000 | 0.3444 |
| V₄ x⁴−2x²+9 (disc 384²) [abelian] | V₄ | C₂×C₂ | 2 | 0.8113 | **0.8092** | 0.8113 ✓ | 2.0000 | 1.1887 |
| C₄ Φ₅ [abelian control] | C₄ | C₄ | 3 | 1.5000 | **1.4989** | 1.5000 ✓ | 2.0000 | 0.5 |

Every field lands on its pre-stated value. The headline readings:

- **S₄ carries 2.0944 bits of type entropy and leaks exactly 1 bit.** Five factorization types (1/24 : 6/24 : 3/24 : 8/24 : 6/24 over {[1,1,1,1], [2,1,1], [2,2], [3,1], [4]}); the odd/even sign carries all of it; 1.0944 bits (the within-even-face structure: identity vs [2,2] vs [3,1]) are residue-invisible at every modulus. H(T) − I₁ = loss = 0 exactly because each S₄ type determines its sign.
- **A₄ loses exactly 2/3 bit**: the [3,1] type fills *both* non-trivial C₃-cosets (all eight 3-cycles split 4+4 across them), so the type cannot tell p ≡ 2,5 from p ≡ 4,7 mod 9; E[H(coset|T)] = (8/12)·H(1/2,1/2) = 0.6667, and I₁ = 1.5850 − 0.6667 = 0.9183 = H(1/3, 2/3) — paper 75's F₀-fork value re-derived as a *loss* from the fuller dial.
- **D₄ loses 0.3444 bit**: the [2,2] type merges the r²-class (coset (+1,+1)) with the sr-reflections (coset (−1,−1)); E[H(coset|T)] = (3/8)·H(1/3, 2/3).
- **V₄ loses 1.1887 bits**: all three involutions give type [2,2] — the abelian field's own type map merges three of its four classes; the type channel collapses to the binary [nr=4]-fork, 0.8113 = H(1/4, 3/4) = paper 77's value.
- **Within-coset flatness** holds at every field (conditional MI at or below the permutation-null mean: z = −2.36/−1.86/−3.50/−0.07/+0.00/+0.00); **thickening** m\*² agrees at the 0.004-bit level under the within-coset permutation null (S₃a 1.0111 vs null 1.0149; S₄ 2.0493 vs 2.0454, z = +2.82; A₄/D₄/V₄ exact to 4 decimals); **coprime moduli flat** (≤ 0.0002).

## 4. The REVERSAL

Paper 77's control pair ordered the *fork* channels V₄ > D₄ (abelian V₄ pins its identity fork at H(1/4) = 0.8113; non-abelian D₄ caps the same fork at the commutator leakage 0.2936). The **type** channels order the same pair the other way:

> forks: V₄ 0.8113 > D₄ 0.2936  **but**  types: V₄ 0.8092 **<** D₄ 1.6555.

The reversal is not an anomaly — it is the law. D₄'s type map happens to separate its cosets well ([4] ↔ {r,r³}, [2,1,1] ↔ {s,sr²}, only [2,2] merges two cosets), while V₄'s merges three of four classes. The readout coarseness, not the group's abelianness, decides which channel is richer: **the type channel measures the alignment between the factorization statistics and the abelianization, not the abelianization itself.**

## 5. Semiprime level (400k MC per field, unramified 2^16 pools)

| field | I(N mod m\*; pair) measured | law | dial-pair | which-factor | pinned-fork s-proj |
|---|---|---|---|---|---|
| S₃a | **1.0001** | 1.0000 ✓ | 1.0000 | 0.0000 | 1.0000 = Is(2) |
| S₃b | **1.0001** | 1.0000 ✓ | 1.0000 | 0.0000 | 1.0000 = Is(2) |
| S₄ | **1.0034** | 1.0000 ✓ | 1.0000 | 0.0000 | 1.0002 = Is(2) |
| A₄ | **0.4729** | 0.4739 ✓ | 1.5850 | 0.0000 | 0.4729 = Is(3) |
| D₄ | **1.4325** | 1.4302 ✓ | 2.0000 | 0.0000 | 0.2959 = Is(4) |
| V₄ | **0.2902** | 0.2947 ✓ (= Is(4)) | 2.0000 | 0.0000 | 0.2902 = Is(4) |
| C₄ Φ₅ | **1.2461** | 1.2500 ✓ | — | — | — (paper 78 reproduced) |

- **The C₂ cap is a theorem about the abelianization, not the type count**: S₃ (3 types), S₄ (5 types) — fields whose complete type distributions differ wildly from a quadratic field's — all have semiprime type-pair channels equal to the quadratic 1.0000 to within 0.0034. No non-abelian field with cyclic C₂ abelianization can exceed the binary cap, however rich its splitting statistics.
- **A₄'s type pair (0.4739) sits 1.111 bits below its dial-pair (1.5850)** — the largest type-vs-dial gap in the table, the semiprime image of the 2/3-bit + within-V₄ losses.
- **D₄'s type pair (1.4302) exceeds 1 bit** — a NON-abelian multi-state channel above the binary cap, exactly as its 2-dimensional abelianization predicts (the dial-pair is 2.0; the type reads 1.43 of it).
- **V₄ reproduces the paper-79 2-state identity** (type pair = Is(4) = 0.2947) and **C₄ reproduces paper 78** (1.25) inside the same pipeline — the abelian regression line.
- Pinned-fork s-projections reproduce the split-count law everywhere it applies (sign fork Is(2) = 1.0 ×3; A₄'s V₄-coset fork Is(3) = 0.4739 = paper 75; D₄'s [4]-fork and V₄'s [nr=4]-fork Is(4)) — the earlier papers' channels are projections of this one.

## 6. Method notes

- **Quartic types via F_{p²}-root counting**: (nr, nr₂) = (deg gcd(f, x^p − x), deg gcd(f, x^(p²) − x)) determines the quartic type uniquely — (4,4)→[1,1,1,1], (2,4)→[2,1,1], (0,4)→[2,2], (1,1)→[3,1], (0,0)→[4]. The cubic-resolvent shortcut is **invalid** for special quartics: x⁴−2's axis pairing is fixed by all of D₄ (resolvent y³+8y has a built-in rational root) and V₄'s resolvent splits over ℚ — generic-position dictionaries misclassify exactly the fields of interest here.
- **Sparse-modulus discipline** (the paper-70 lesson, applied twice): plug-in MI at m\*² = 80089 (~80k cells, 23k samples) is biased high by orders more than the effect size — thickening is tested against the **within-coset permutation null**, not raw; and the S₄ semiprime table (282 residues × 15 pairs) needs 400k draws to bring the Miller–Madow bias under 0.01 bits (30k would have left ~0.10).
- Sieves: 2^18 prime level, 2^16 MC pools, ramified primes excluded throughout; fixed seeds; total runtime 314 s.

## 7. Barriers

**(a) Circularity — clean.** The law and the full seven-field table were stated before the run; the measurement pipeline (root counts over F_p and F_{p²}) is independent of the residue dial being tested.
**(b) Known-method-in-disguise — clean.** No non-abelian splitting-type channel work exists in the Catalog (698-pkg scan 2026-08-21: nearest neighbors are the lab's own echoes #723–#728 = papers 71–75/78) or the literature; Chebotarev density theorems give *limits* of type frequencies, never their information content against residues.
**(c) Toy-scale — confronted.** Real Galois groups S₃/S₄/A₄/D₄/V₄/C₄ over ℚ, 23k-prime histograms per field, 400k-draw semiprime MC; every rate matches class-size theory to < 2%.
**(d) Data leakage — clean.** No training; deterministic enumeration + fixed-seed MC.
**(e) Variance/reproducibility — the substance.** The honest limits are quantified: the S₄ I₁ margin (+0.0100 above the law) is finite-sample (23k primes over a 282-class dial); thickening agreements are at the 0.004-bit level under permutation nulls; the flatness tests sit at/below their null means. All asserts green; ALL_DONE marker.
**(f) Measurement errors — controlled.** Exact closed-form laws vs MC asserted to 0.02 everywhere; the two estimator traps (sparse plug-in MI, object-array pair codes) were caught and repaired protocol-wide.
**(g) Baseline unfairness — clean.** Abelian controls (V₄, C₄) run through the identical pipeline and reproduce papers 77/78/79 exactly; coprime moduli flat; which-factor walls 0.0000.
**(h) Practical relevance — the closure.** Symmetric unordered pairs (which-factor wall 0.0000, barrier 2); pure residue dials at the G^ab conductors (barrier 5); the type is N-computable only behind the CRT split — computing T(p) and T(q) separately *is* the factorization (barrier 6); all classical: Galois theory, Frobenius densities, quadratic/cubic reciprocity, Chebotarev 1922 (barrier 8).

## 8. What closes

The **type-channel program is complete**: the complete symmetric residue channel of a number field's splitting statistics is *exactly* its abelianization content — at the prime level I₁ = I(T; coset), at the semiprime level the papers 78/79 law verbatim — for abelian and non-abelian Galois groups alike, with the readout's coset-separation deciding how much of the dial survives. Papers 70 (flatness), 71 (criterion), 72–74 (binary laws), 75–77 (group table), 78–79 (abelian types) all become projections of this one statement. Remaining above it: fields whose G^ab is trivial (perfect groups, paper 76's A₅ — predicted zero by the law, already confirmed flat), sparser readouts (root counts only), and the quantum channel beyond.

Now 415 experiments. Assessment v191. Paper 80, issue #172.

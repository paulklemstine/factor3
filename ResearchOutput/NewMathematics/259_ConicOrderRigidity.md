# Paper 259 — CONIC ORDER-RIGIDITY: **THE SEAL HOLDS — TREE-WORD ORDERS LIVE ON ONE SHARED MODULUS** — Every Berggren-Word Order Divides K_p = p(p²−1) (Zero Violations, 550 Primes × 40 Words) While the Stronger Individual-Torus Variant Is REFUTED (4,973 Words Mix Split and Non-Split Tori) — the Tree Generates Exactly PGL₂(F_p), and a Tree-Word Factoring Arm Produces ZERO Successes in 600 Trials Where Matched-Budget p±1 Methods Produce 225–292 — Bet #2's Triad Closes the "Tree-Matrix ECM Analogue" Genre BY MECHANISM

**Verdict names: CL1_WEAK_CONFIRMED · CL1_STRONG_REFUTED · CL2_CONFIRMED ·
CL3_CONTAINED (rate-parity fails in the sealing direction)**

Round-96 #1 · fleet Bet #2 empirical legs. Sources:
`ResearchOutput/scripts/2026-08-25-round75/{exp608_conic_order_rigidity.py,
exp608_result.json, exp608_run.log, exp608_findings.md}`.

## 1. The correct object (and how v1 died)

v1 tested 3×3 triple-space matrices — withdrawn before evidence: det = 5, no
integral invariant quadratic form, mod-p images so large an image BFS blew
8.6 GB RSS. The conic-trap screening rule (declare the object's group first)
did its job by explosion. The correct family: Berggren's moves in (m,n)
coordinates — M₁=(2m−n,m), M₂=(2m+n,m), M₃=(m+2n,n) as GL₂(Z) matrices acting
projectively on t = m/n ∈ P¹ — verified to generate the primitive-triple tree
EXACTLY (every coprime opposite-parity pair with m ≤ 40 reachable from (2,1)).

## 2. The seal (CL1 weak): one modulus caps everything

Across all 550 primes < 4000 and 40 random words each (length ≤ 8,
factorization-reduced order ladders against cached per-prime factorizations):
**zero violations** of ord(w) | p(p²−1). Combined with CL2 — <M₁,M₂,M₃> ≅
PGL₂(F_p) exactly at every probed prime — the tree-word world has exactly the
conic maximal-torus menu the trap predicts. Any "raise words to smooth E and
gcd" method therefore gets ONE smoothness draw per prime: none of ECM's
Hasse-interval independence.

## 3. The strong variant dies (CL1 refuted)

4,973 of 22,000 word orders divide NEITHER p(p−1) NOR p(p+1) individually
(order 8 exists already at p = 3): words MIX split and non-split torus parts.
The fleet's sharper claim is refuted; the correct statement is the product-cap
seal above.

## 4. Micro-audit (600 balanced bits-40 semiprimes, matched per-N mpz-mul budgets)

| arm | successes | work (mpz muls) |
|---|---|---|
| Pollard p−1 (bases 2/3/5/7, E = lcm(1..500)) | **225** | 1,865,364 |
| Williams p+1 (Lucas seeds 3/5/7) | **292** | 5,591,784 |
| tree-word raw traces vs {1,2} | **0** | 7,463,560 |

Zero is exactly what mechanics predicts for untargeted traces (~2/p hit
probability ⇒ ~0.003 expected). Disclosed caveat: the registered design omitted
the stage-1 targeting step tr(W^E); the seal predicts even that analogue
behaves as ONE Williams draw at worse constants — strictly dominated either
way. Strata flat across (2/p): pm1 113/112, pp1 145/147.

## 5. The six-defect ledger (positive-control gate validation)

Every defect below was caught BEFORE evidentiary recording by registered
machinery gates: (1) v1 wrong generator family (killed by BFS blowup);
(2) stream-band arithmetic under-crediting exp606's ×10⁸ strides (assertion
fired; bands moved to +263e6/265e6); (3) control constants invalid on the
exponent lattice twice → controls now searched with exact divisibility;
(4) scalar exponentiation double-counting the MSB (x=a start); (5) matrix
ladder missing its R-squaring (computed tr(A^bitlen); k=5 passed BY ACCIDENT,
k=13 exposed it); (6) Williams live-seed requirement booked (success needs
legendre(a²−4,p) = −1; all-residue seed sets legitimately produce zero).
**PROCESS LAW UPGRADED: positive controls are mandatory gates on any
factoring-machinery experiment.**

## 6. Barrier validation and consequence

No barrier breached — this is negative strength. The triad (with Lemmas A/B/C
formalized alongside) closes the tree-matrix-ECM-analogue genre BY MECHANISM:
genus-0 order structure carries no Hasse-interval variety, and the empirical
arms confirm strict domination. Prior art disclosed: GL₂ element-order theory,
Matthews–Vaserstein–Weisfeiler, Williams (1982), lab papers 64/67. Falsifiable
follow-up pre-stated: a targeted tr(W^E) variant at matched budgets must land
within Poisson noise of ONE Williams draw's success count — if it beats it,
the seal is broken and that is refutation-class news.

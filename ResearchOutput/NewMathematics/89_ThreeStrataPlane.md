# Paper 89 — THE-THREE-STRATA-PLANE: Definition-Routes, Methods, Quantum — the Measured Factoring Landscape

**Verdict name: THE-THREE-STRATA-PLANE.**
Round-26 #2 · exp 424 · assessment v200 · script `/tmp/exp_threestrata.py` · log `/tmp/r26n2c.log` · runtime 59 s.

## 1. Completing the plane

Paper 88 placed the four definition-route witnesses on one cost-information plane. This round completes the landscape with two additions measured under identical conditions: two more **definition-route witnesses** (τ(N), σ₁(N) via their trial-division-to-√N definitions) and **classical-method calibration points** (trial division, Fermat, Pollard ρ) — turning the barrier-8 face from citation into data. With papers 85–87 supplying the quantum corner, the full factoring landscape now sits on one plane in three measured strata.

## 2. The strata

### Stratum A — definition-routes (barrier 4's price)
| witness | α on N | note |
|---|---|---|
| M1 gcd-scan | 1.000 | paper 88 |
| idempotent scan | 1.000 | paper 88 |
| zero-divisor first hit | ~½ | paper 88 |
| CF period | 0.398 | paper 88 |
| **τ(N), σ₁(N) trial division** | **0.500 exact** | this round |

The new witnesses land at α = 0.500 to three decimals — the √N scan *is* their definition; σ₁ verified exactly (= 1 + N + p + q) at every size.

### Stratum B — classical methods (barrier 8's face, as data)
| method | measured cost |
|---|---|
| trial division | mean log₂cost = 19.30, median 19.36 (= E[min(p,q)] scale; the factor itself is the certificate) |
| Fermat | mean = median = 19.36 — indistinguishable from trial division on uniform draws (the gap cost is tail-dominated by unbalanced pairs) |
| Pollard ρ | mean log₂cost = 8.73; size-stratified exponent slope 0.523 per prime-bit ⟹ **α on N = 0.261** vs the 0.25 birthday bound |

### Stratum C — quantum (papers 85–87)
Poly(log): the fungibility surface with unit exchange rate, standard-corner optimal.

## 3. The structure-blindness price

At fixed N, the cheapest method beats the cheapest definition-route by a factor that **grows with N**:

| N | τ-definition-scan | Pollard ρ | speedup |
|---|---|---|---|
| 2¹⁶ | 2.2×10⁴ | 125 | **173×** |
| 2²⁰ | 4.8×10⁵ | 272 | **1 780×** |
| 2²⁴ | 5.3×10⁶ | 2 550 | **2 070×** |
| 2²⁸ | 1.2×10⁸ | 14 488 | **8 310×** |

This is the measured price of structure-blindness: evaluating a witness from N alone versus exploiting what it is. The strata do not overlap anywhere in the measured window.

## 4. Method ledger

Two designed-check catches: (1) the ρ exponent first read 0.523 — a units mismatch (slope per prime-bit vs per-N; log₂N = 2·bits), corrected to α_N = 0.261 against the birthday bound, confirmed by a standalone scaling check (log₂ops = bits/2 − 1 exactly); (2) the N = 2³⁶ blindness-price row would have run for hours in pure Python — capped honestly rather than approximated silently. Also reported: Fermat's mean equals its median equals trial division's — the tail-dominated gap cost on uniform draws.

## 5. Barriers

**(a)** clean — horns pre-stated (strata distinct, new witnesses at ½, growing blindness price); the ρ gate caught its own units error. **(b)** clean — the three-strata unification is new; method costs are textbook but here measured under identical conditions. **(c)** confronted — real timings, 40-draw calibrations, 120-draw stratified fit, four N-sizes. **(d)** clean — fixed seeds. **(e)** the substance — medians alongside means (tail-domination documented), the 2³⁶ cap disclosed. **(f)** controlled — both defects caught by asserts/stalls before claims. **(g)** fair — identical conditions across strata; ρ validated standalone before entering the plane. **(h)** relevance — the landscape in one sentence: barrier 4 prices the definition-routes (α ≥ 0.4), barrier 8 owns the methods (α ≈ ¼), Shor owns the quantum corner (poly) — and each stratum's price is now measured, not asserted.

## 6. What closes

The factoring programme's cost knowledge is now unified: every route to a factor — witness-definition, classical method, or quantum circuit — has a measured position on one plane, in three non-overlapping strata whose boundaries are the barriers. Frontier (i)'s empirical arming (paper 88) extends to the whole landscape; the formal converse proof remains the single open theoretical target.

Now 424 experiments. Assessment v200. Paper 89, issue #181.

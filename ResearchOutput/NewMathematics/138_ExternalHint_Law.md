# Paper 138 — EXTERNAL-HINT-FILTER: The External-Hint Law — One Scalar Prices Everything

**Verdict name: EXTERNAL-HINT-LAW-DERIVED-AND-VERIFIED.**
Round-38 #4 · exp 468 · assessment v247 · proofs `ResearchOutput/scripts/2026-08-21-resume/exp468_proofs.md` (+ `exp468_verify.py`, `exp468_result.json`) · seed 20260821.

## 1. Completing the barrier map's third row

Papers 132 (residues: cap 4/3, theorem) and 137 (position: 5.19×, measurement) left the
third stratum — GENUINELY EXTERNAL information — unpriced in the scan-order functional.
This paper derives and machine-verifies its exact law.

## 2. The theorems (all proved under isolated Model Assumptions MA-1/MA-2′; Siegel–Walfisz
gives asymptotic unconditionality at fixed modulus)

- **Master law (Thm B):** Speedup(H) = **1/(1 − (1−θ)·P_hit)** where P_hit = P(min ∈ K | H)
  = ½Σ_a w(a)[a∈K] + ½Σ_a w(a)[c·a⁻¹∈K], w = hinted posterior. ALL information acts through
  the single scalar P_hit; paper 132's 1/(1−θ+θ²) is exactly the case H ⊥ p — the internal
  cap is the UNINFORMATIVE POINT of the external law.
- **The symmetry break located (Thm A):** P(p ≡ a | H, pq ≡ c) = L_H(a)/Σ L_H(a′),
  independent of c. Internal readings die on the fiber-uniformity step; a hint's likelihood
  lives on the non-c-measurable coordinate and survives it verbatim.
- **Canonical partition law:** symmetric θ=½ hint → Speedup = **8/(7−2α)**; α=½ reproduces
  4/3 exactly; α=1 gives only **8/5 < 2** — the WHICH-FACTOR CEILING: external hints are
  capped at 2× per dial by which-factor blindness; exceeding 2× requires θ→0, paid at
  ISOLATION-COST log₂π(√N) oracle queries (net-of-isolation positive from t = 5).
- **Certain-hint ladder:** Speedup(t) = 2^(t−2)/(1−2^(1−t)) for t ≥ 2 (4/3 at t=2,
  16/7 at t=3 → 2^(t−2)); two identified bit-losses vs naive 2^t: parity (p odd) and
  which-factor (the min's class ∈ {a, b} ambiguity).
- **Trace hints:** Speedup_trace(t) = 2^(t−1)/C_t — GENERIC-RECOVERY's "~5×/bit" is a
  CONSTANT root-multiplicity divisor plus accounting, not a rate penalty; zero bits of rate lost.
- **Break-even:** charging ε per candidate test, net speedup =
  1/((1+ε)(1−(1−θ)P_hit)); α*(θ,ε) = 2ε/((1+ε)(1−θ)) − θ, feasible iff
  ε ≤ (1−θ²)/(1+θ²) (= 3/5 at θ=½). INTERNAL filters tolerate only ε ≤ ⅙.

## 3. Machine verification

m=31 at 400k samples: speedup dev ≤ 0.0032 across all α; posterior dev ≤ 0.00084; χ(c)-split
pointwise exact (measured 1.8226 vs 20/11 predicted at α=0.9); exhaustive subset enumeration
m = 3/4/5/7/8 max dev from closed form 0.0089; ladder ratios to exact law 0.9986–1.0045
(t = 2..8), starvation rolloff honestly measured not modeled (t ≳ 12); trace C̄_t saturation
reproduced (ratios 0.993–1.002); break-even verdicts agree in 20/20 cells.

## 4. What this decides

The barrier map's three rows are now complete:
| stratum | law | status |
|---|---|---|
| residues (internal congruence) | 1/(1−θ+θ²) ≤ 4/3 | theorem (paper 132) |
| magnitude/position | 5.19× measured, ratio-structure-bounded | experiment (paper 137) |
| external hints | 1/(1−(1−θ)P_hit): linear in bits until the 2× which-factor ceiling per dial; beyond it only via isolation cost | theorem + verification (this paper) |

External information is priced LINEARLY in bits with no compounding — capacity synergy does
not transfer to work bits, confirming paper 132's currency separation from the external side.
Residuals stated: size/position hints attack E[T] rather than the order; superconstant-cost
tests out of scope; MA-1 effectivity inherited.

Method ledger (9 self-caught, each caught by replication mismatch or case-table sanity):
q-side echo omission; indicator-vs-value expansion of χ; p-hunt vs scan accounting; vacuous
t=1; starvation unfitted; position-index/class-value label-space bug producing a flat-α
artifact; prime-2 leak; drop-branch complement sign; coincidence-case thinning swap.

Now 470 experiments. Assessment v247.

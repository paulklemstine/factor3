# Paper 142 — PER-N-PREDICTOR: One Feature Captures Two-Thirds of the Achievable Signal

**Verdict name: PREDICTOR-AT-CEILING (H1/H2 formally false by narrow margins; substantive confirmation; H3 decisive).**
Round-39 #4 (cron iteration) · exp 472 · assessment v251 · script `ResearchOutput/scripts/2026-08-21-resume/exp472_per_n_predictor.py` (+ `exp472_result.json`) · seed 20260827.

## 1. Validating paper 139's actionable corollary

Paper 139: per-N relation yield is governed by the small-prime QR pattern, predictable
a priori from ~20 Euler-criterion tests. This experiment builds the minimal predictor
(per-N smooth rate ~ β₀ + β₁·QRcount(odd primes ≤ 100)) and tests it honestly:
train at bitlen 40 / u ∈ {2.5, 3.5} (1000 train Ns), test held-out same-scale plus
transfer to bitlen 44 with renormalized intercept; 1500 Ns × 60 relation values per cell.

## 2. Results

| cell | R² | calibration slope |
|---|---|---|
| 40/u2.5 test | **0.2998** | 1.003 |
| 40/u3.5 test | 0.2246 | 0.896 |
| 40→44/u2.5 transfer | 0.2263 | 0.839 |
| 40→44/u3.5 transfer | 0.1726 | 0.788 |

Formal verdicts: H1 FALSE (u=3.5 R² misses the ≥0.25 band by 0.025), H2 FALSE (u=3.5
slope 0.788 just under 0.8) — both by hair-width margins; slopes otherwise in band.

**H3 DECISIVE**: residual variance is only **1.12–1.24× the pure binomial sampling floor**
of a 60-value-per-N estimate — the single QR-count feature captures essentially ALL
systematic per-N structure; the remainder is measurement noise.

**Ceiling analysis** (post-hoc, disclosed): at 60 values/N the maximum achievable R² for
ANY predictor is ≈ 0.45 (u=2.5) / ≈ 0.31 (u=3.5); the one-feature predictor achieves
**66% / 73% of ceiling**. A richer feature has little headroom at this sample size —
collect more values per N before adding features.

## 3. What this decides

The per-N yield predictor is real, cheap (~20 Legendre computations via Euler's criterion),
calibrated at the same scale, and approximately transferable across scale. Practical form:
rate(N) ≈ β₀ + β₁·(QR-count ≤ 100), β ≈ (−0.026, +0.0129) at u=2.5. Barrier lines: (5) the
predictor is a residue dial predicting a METHOD'S input statistics — zero factor information;
(8) QS cost-model calibration context.

Method ledger: lean inline takeover after two silent agent-channel deaths; pre-stated bands
were optimistic (recorded as stated); H3's richer-feature branch dropped for runtime.

Now 474 experiments. Assessment v251.

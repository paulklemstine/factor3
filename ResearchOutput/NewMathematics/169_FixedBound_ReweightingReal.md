# Paper 169 — FIXED-BOUND: The u-Sensitivity Is Genuine Reweighting

**Verdict name: REWEIGHTING-REAL (H1 refuted at 9% attribution; H2 confirmed).**
Round-45 #3 (cron iteration) · exp 502 · assessment v278 · script `ResearchOutput/scripts/2026-08-21-resume/exp502_fixed_bound.py` (+ `exp502_result.json`) · seeds 20260980–87.

## 1. Paper 168's named follow-up: decouple the strip bound from u

One strip pass to PB = 4000 recording (remainder, max-prime) per value; both u-thresholds
then read off the same decomposition: smooth@u iff remainder == 1 AND maxp ≤ B_u. 8
populations bitlen 44 × 960 values.

## 2. Results

| seed | sp(u=2.5) | sp(u=3.5) | Δ |
|---|---|---|---|
| 20260980 | 0.7977 | 0.7390 | +0.0586 |
| 20260981 | 0.7986 | 0.7280 | +0.0706 |
| … | … | … | … |
| mean | **0.7934** | **0.7356** | **+0.0578** |

- **H1 REFUTED**: attribution of paper 168's Δ to bound shrinkage = **9.1%** — holding the
  strip bound fixed removes almost none of the drop.
- **H2 CONFIRMED**: the fixed-bound residual drop is well above 0.03 across every
  population (sd 0.0138).

The fixed-bound drop (+0.0578) is ~91% of paper 168's variable-B reference (+0.0636): the
u-sensitivity is genuine threshold reweighting — tighter u shifts which QR primes dominate
the rate — with bound-shrinkage contributing only ~9%.

## 3. What this decides

Paper 168's "mostly intrinsic" reading is CONFIRMED and sharpened: the residual ~0.064
drop survives full bound-decoupling, so dial deployments at tight u should recalibrate the
footprint weights themselves (the reweighted-prime structure), not adjust bounds.
Barriers: (5)/(8) unchanged.

Now 503 experiments. Assessment v278.

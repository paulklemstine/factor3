# Paper 145 — QR-RESIDUAL: The Footprint-Weighted Dial Captures the Residual

**Verdict name: FOOTPRINT-WEIGHTS-CAPTURE-THE-RESIDUAL (H1 confirmed decisively).**
Round-40 #1 (cron iteration) · exp 477 · assessment v254 · script `ResearchOutput/scripts/2026-08-21-resume/exp477_qr_residual.py` (+ `exp477_result.json`) · seed 20260829.

## 1. Paper 144's honest remainder, explained

Paper 144 left a residual at 1.31× the sampling floor (u=2.5): real per-N structure beyond
QR-count(≤100). The theoretically-motivated feature: each QR prime p divides ~2/p of the
relation values x²−N (two roots), so its expected smoothness contribution is its footprint
2/p — the predictor should weight primes by footprint, not count them.

## 2. Results

Out-of-sample R² (train/test on 1200 Ns × 80 values, bitlen 44):

| model | u=2.5 | u=3.5 |
|---|---|---|
| QR-count ≤100 (baseline) | 0.3927 | 0.2063 |
| + weighted Σ 2/p over QR p ≤ 400 | **0.5691** (+0.176, CI [0.120, 0.229]) | **0.3078** (+0.102, CI [0.037, 0.155]) |
| + direct divisibility fraction (p ≤ 13) | 0.5110 (+0.118) | 0.2519 (+0.046) |
| both features together | **0.5864** | 0.3429 |

H1 CONFIRMED (weighted lift ≥ +0.05 with CI excluding 0); H2 confirmed (the direct
mechanism feature — realized small-prime divisibility, measurable without factoring — adds
independent signal); H3 refuted. The residual was real structure and is now largely captured
by two cheap features (~200 Euler-criterion tests plus one mod count).

## 3. What this decides

The per-N yield dial's final form: rate(N) is predicted by the footprint-weighted QR mass —
the quantity QS theory says should matter (expected divisibility contributions) — plus the
realized low-prime divisibility fraction, at R² ≈ 0.59 / 0.34 out-of-sample. Practical:
sieve-yield triage costs ~200 powmod evaluations per candidate N. Barrier lines: (5) all
features are residue dials of METHOD input statistics — zero factor information; (8)
calibration context.

Method ledger: v1 bootstrap refit indexed the test-slice target variable (IndexError);
inline takeover after the agent channel went silent 15 minutes into its first turn.

Now 477 experiments. Assessment v254.

# Paper 167 — U35-LOCALIZED: Above the Floor Everywhere, Degrades Everywhere

**Verdict name: NEITHER — DECISIVE (center above floor; tail tight; paired drop real).**
Round-45 #1 (cron iteration) · exp 500 · assessment v276 · script `ResearchOutput/scripts/2026-08-21-resume/exp500_u35_localize.py` (+ `exp500_result.json`, `ledger_exp500.jsonl`) · seeds 20260950–63.

## 1. Localizing paper 166's breach

Paper 166 left open whether the u=3.5 dial degradation's center or only its tail breaches.
Resolution: 14 fully independent populations (1200 Ns each), paired u=2.5/u=3.5
measurement.

## 2. Results

| statistic | value |
|---|---|
| sp(3.5) mean | **0.6282 ± 0.0041 (SE)** |
| bootstrap CI of mean | [0.6204, 0.6363] — excludes the 0.60 floor |
| sub-floor seeds | **0/14** |
| sd | 0.0155 (far under the 0.06 tail threshold) |
| paired Δ = sp(2.5) − sp(3.5) | **+0.1057**, CI [0.0999, 0.1112], **14/14 positive** |

Anchor sp(2.5) = 0.7339 replicates paper 165's band at 5× sample size.

## 3. What this decides

The dichotomy was false: the bal@u=3.5 dial sits at a tight 0.628 ± 0.004 ABOVE the floor —
paper 166's sub-floor column was 240-Ns/population sampling noise, and its deep-breach seed
has no analogue at 5× N. What survives is the systematic paired loss (+0.106 everywhere):
dial-hardening work should target that uniform u-sensitivity (likely via the starved ~1.9%
smooth-rate regime or bound-coverage mismatch), not seed outliers. Barriers: (5)/(8)
unchanged.

Now 501 experiments. Assessment v276.

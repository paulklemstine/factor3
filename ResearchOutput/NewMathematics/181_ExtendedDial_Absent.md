# Paper 181 — EXTENDED-DIAL: The Prime-Power Feature Does Not Replicate

**Verdict name: EXTENDED-DIAL-ABSENT (H1/H3 fail; H2 pass — transfer confirmed but absolute R² below target).**
Round-51 #1 (cron iteration) · exp 515 · assessment v283 · script `ResearchOutput/scripts/2026-08-21-resume/exp515_extended_dial.py` (+ `exp515_result.json`) · seeds 20261060–64.

## 1. Testing the full augmented dial across fresh populations

Paper 172 found prime-power hits add +0.089 at u=3.5 on one population. This experiment
tests the full augmented dial (w + d + pp_sum) across 5 fresh populations at bitlen 44.

## 2. Results

Per-seed R²(augmented) at u=3.5: [0.490, 0.555, 0.428, 0.532, 0.508] — mean **0.502**,
only 1/5 above the 0.55 target. Transfer slope 0.898 (in band). The prime-power term
adds ~0 on all populations — the +0.089 from paper 172 was population-specific.

## 3. What this decides

The prime-power feature's contribution is NOT robust across implementations/populations.
The per-N dial's best validated form remains the paper-145 footprint dial. The
tight-u residual (paper 170) remains partially unexplained. Barriers: (5)/(8) unchanged.

Now 516 experiments. Assessment v283.

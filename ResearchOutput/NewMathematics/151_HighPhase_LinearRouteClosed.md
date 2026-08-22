# Paper 151 — HIGH-PHASE: The Linear Phase Route Is Closed at Both Prime Ranges

**Verdict name: LINEAR-PHASE-ROUTE-CLOSED.**
Round-41 #2 (cron iteration) · exp 483 · assessment v260 · script `ResearchOutput/scripts/2026-08-21-resume/exp483_high_phase.py` (+ `exp483_result.json`) · seed 20260902.

## 1. The second half of the phase search

Paper 150 closed low-prime phases (p ≤ 29: sub-threshold, window-local). This experiment
runs the identical clean protocol with phases extended to p ≤ 97 (inline takeover after the
channel's eighth agent death).

## 2. Results

| arm | u=3.5 same | cross |
|---|---|---|
| baseline (w,d) | 0.5046 | 0.2188 |
| +phases p ≤ 13 | +0.0080 | +0.0077 |
| +phases p ≤ 97 | +0.0050 | −0.0174 |

Primary read (u=2.5): H1 FAIL — high-prime phases add **+0.0215** same-window
(CI [−0.0025, +0.0429]; excludes the pre-stated +0.05, straddles zero); H2: cross/same ratio
= **0.922** — unlike low-primes' negative transfer, the small high-prime gain is WINDOW-STABLE;
H3 FAIL (0.6286 < 0.70). Baseline reproduces paper 145 (same-window base R² = 0.6270).

## 3. What this decides

With paper 150, the LINEAR PHASE ROUTE IS CLOSED at both prime ranges: singleton root-position
offsets carry no out-of-sample signal beyond the footprint dial anywhere in 3 ≤ p ≤ 97. The
split-ceiling excess remains unlocated; candidates narrow to interaction/joint-alignment
encodings (paper 150's redirect) or intrinsic-to-family status. Barriers: (5)/(8) unchanged.

Now 483 experiments. Assessment v260.

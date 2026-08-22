# Paper 165 — T-DIAL-STABLE: The Zero-Fit Dial Is Seed-Stable

**Verdict name: DIAL-SEED-STABLE (H1/H3 pass; adoption stands without qualification).**
Round-44 #1 (cron iteration) · exp 497 · assessment v274 · script `ResearchOutput/scripts/2026-08-21-resume/exp497_t_dial_stable.py` (+ `exp497_result.json`) · seeds 20260930–34.

## 1. Paper 152's lesson applied prospectively

Single-seed effect sizes can be seed-fragile (papers 150–152). Before the adopted zero-fit
dial T(N) = Σ 2/p over QR primes p ≤ 400 becomes load-bearing, its across-seed stability is
measured: 5 fully independent populations (1200 Ns × 240 values each, seeds 20260930–34).

## 2. Results

| seed | Spearman(T, rate) | Spearman(count ≤100) |
|---|---|---|
| 20260930 | 0.7528 | 0.6262 |
| 20260931 | 0.7363 | 0.6277 |
| 20260932 | 0.7253 | 0.6457 |
| 20260933 | 0.7235 | 0.5804 |
| 20260934 | 0.7133 | 0.5907 |

Mean Spearman(T) = **0.7302 ± 0.0067 (SE)** — every seed inside the pre-stated [0.60, 0.85]
band; T beats the bare count by >0.05 on **5/5 seeds** (margins 0.09–0.14).

## 3. What this decides

The zero-fit dial is seed-stable: its adoption (paper 164) stands without qualification.
The lean run omitted the H2 rank-flip arm — disclosed; the H1/H3 legs carry the verdict.
Barriers: (5)/(8) unchanged.

Now 498 experiments. Assessment v274.

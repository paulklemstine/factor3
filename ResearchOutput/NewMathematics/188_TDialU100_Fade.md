# Paper 188 — TDIAL-U100: The Dial Begins to Fade at Bitlen 100

**Verdict name: DIAL-FADES (pooled drops below band for the first time; CI straddles).**
Round-67 #2 (cron iteration) · exp 540 · assessment v295 · script `ResearchOutput/scripts/2026-08-21-resume/exp540_t_dial_unif_100.py` (+ `exp540_result.json`) · seeds 20261200–02.

## 1. The fading test

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 tested on uniform draws at bitlen
100 — the first cell where Spearman(T) drops below the validated [0.55, 0.85] band.

## 2. Results

| seed | Spearman(T, rate) |
|---|---|
| 20261200 | **0.546** |
| 20261201 | **0.528** |
| 20261102 | **0.549** |
| pooled | **0.544** CI [0.498, 0.588] |

T beats count by +0.098 everywhere. But the dial's signal has faded below the validated
band for the first time — the erosion that began at bitlen 56 continues.

## 3. What this decides

The zero-fit dial begins to fade at bitlen 100 — its validated deployment envelope ends
at bitlen ~96. Beyond that, signal degrades gradually toward the floor. Barriers:
(5)/(8) unchanged.

Now 525 experiments. Assessment v295.

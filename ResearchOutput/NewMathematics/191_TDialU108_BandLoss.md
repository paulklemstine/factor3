# Paper 190 — TDIAL-U108: The Dial Drops Below the Band at Bitlen 108

**Verdict name: TDIAL-U108-CONTINUES-FADE (H1 band-miss decisive; CI entirely below floor).**
Round-69 #2 · exp 544 · assessment v288 · script `ResearchOutput/scripts/2026-08-21-resume/exp544_t_dial_unif_108.py` (+ `exp544_result.json`, `run.log`) · seeds 20261210–12.

## 1. The first CI-separated band loss

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 tested on uniform draws at bitlen
108. Pooled Spearman(T, rate) = **0.488** CI [0.445, 0.534] — the ENTIRE CI below the
0.55 floor for the first time in the ladder's history.

## 2. Results

| seed | Spearman(T, rate) |
|---|---|
| 20261200 | **0.489** [0.445, 0.534] |
| 20261201 | **0.525** [0.490, 0.561] |
| 20261202 | **0.449** [0.394, 0.503] |

First seed heterogeneity of the ladder. Fade decelerates toward a ~0.48 plateau
(step delta −0.0125 vs prior −0.030/−0.043). T beats count by +0.092.

## 3. What this decides

The dial drops decisively below the validated band at bitlen 108 — the fade is real and
the CI now excludes the floor. Barriers: (5)/(8) unchanged.

Now 538 experiments. Assessment v288.

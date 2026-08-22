# Paper 189 — TDIAL-U104: The Fade Continues at Bitlen 104

**Verdict name: FADE-CONTINUES (pooled Spearman(T) = 0.500; near-linear monotone fade).**
Round-68 #2 (cron iteration) · exp 541 · assessment v298 · script `ResearchOutput/scripts/2026-08-21-resume/exp541_t_dial_unif_104.py` (+ `exp541_result.json`) · seeds 20261210–12.

## 1. Quantifying the fade's progression

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 tested on uniform draws at bitlen
104 — the fade continues past the validated envelope.

## 2. Results

| seed | Spearman(T, rate) |
|---|---|
| 20261210 | **0.493** |
| 20261211 | **0.499** |
| 20261102 | **0.509** |
| pooled | **0.500** CI [0.456, 0.545] |

The fade is MONOTONE and NEAR-LINEAR through bitlen 104. T advantage WIDENS (+0.126 vs
count) because count degrades faster.

## 3. What this decides

The dial's signal continues degrading past the validated envelope on a gradual erosion
path. Barriers: (5)/(8) unchanged.

Now 526 experiments. Assessment v298.

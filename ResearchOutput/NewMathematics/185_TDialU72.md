# Paper 185 — TDIAL-U72: The Zero-Fit Dial Holds at Bitlen 72 with Count Parity

**Verdict name: U72-DIAL-HOLDS-COUNT-PARITY (H1 pass; H2 count parity).**
Round-63 #1 (cron iteration) · exp 532 · assessment v292 · script `ResearchOutput/scripts/2026-08-21-resume/exp532_t_dial_unif_72.py` (+ `exp532_result.json`) · seeds 20261160–62.

## 1. The highest-bitlen uniform measurement

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 tested on uniform draws at bitlen
72 — the highest bitlen × regime combination in the dial's validation grid.

## 2. Results

| seed | Spearman(T, rate) | advantage over count |
|---|---|---|
| 20261160 | **0.605** | +0.067 |
| 20261161 | **0.606** | +0.018 |
| 20261162 | **0.603** | +0.029 |
| pooled | **0.605** [0.586, 0.625] | +0.038 [0.015, 0.060] |

All three seeds inside the [0.55, 0.85] band; H2 count parity (advantage below +0.05).

## 3. What this decides

The zero-fit dial extends to bitlen 72 on uniform draws with the band intact — a gentle
monotone decline from ~0.78 at bitlen 44 to ~0.61 at 72. Barriers: (5)/(8) unchanged.

Now 526 experiments. Assessment v292.

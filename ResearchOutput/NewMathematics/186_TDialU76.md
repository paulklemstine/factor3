# Paper 186 — TDIAL-U76: The Zero-Fit Dial Holds at Bitlen 76

**Verdict name: U76-DIAL-CONFIRMED (H1/H2 both pass).**
Round-65 #1 (cron iteration) · exp 533 · assessment v293 · script `ResearchOutput/scripts/2026-08-21-resume/exp533_t_dial_unif_76.py` (+ `exp533_result.json`) · seeds 20261170–72.

## 1. The highest-bitlen uniform measurement

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 tested on uniform draws at bitlen
76 — the highest bitlen × regime combination in the dial's validation grid.

## 2. Results

| seed | Spearman(T, rate) | advantage over count |
|---|---|---|
| 20261170 | **0.593** | +0.066 |
| 20261171 | **0.618** | +0.073 |
| 20261172 | **0.612** | +0.080 |
| pooled | **0.608** [0.588, 0.631] | +0.073 [0.045, 0.097] |

All three seeds inside the [0.55, 0.85] band; H2 confirmed. Uniform ladder: 0.648 (64) →
0.611 (68) → 0.605 (72) → **0.608 (76)** — flat within noise across the 72→76 step.

## 3. What this decides

The zero-fit dial extends to bitlen 76 on uniform draws with the band intact — flat
within noise from bitlen 72. Barriers: (5)/(8) unchanged.

Now 527 experiments. Assessment v293.

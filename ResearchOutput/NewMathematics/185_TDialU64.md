# Paper 185 — TDIAL-U64: The Zero-Fit Dial Holds at Bitlen 64 with Count Parity

**Verdict name: U64-DIAL-HOLDS-COUNT-PARITY (H1 pass; H2 count parity).**
Round-61 #1 (cron iteration) · exp 530 · assessment v292 · script `ResearchOutput/scripts/2026-08-21-resume/exp530_t_dial_unif_64.py` (+ `exp530_result.json`) · seeds 20261140–42.

## 1. The highest-bitlen uniform measurement

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 tested on uniform draws at bitlen
64 — the highest bitlen × regime combination in the dial's validation grid.

## 2. Results

| seed | Spearman(T, rate) | advantage over count |
|---|---|---|
| 20261140 | **0.658** | +0.096 |
| 20261141 | **0.642** | +0.079 |
| 20261142 | **0.643** | +0.046 |
| pooled | **0.648** [0.629, 0.665] | +0.074 [0.049, 0.100] |

All three seeds inside the [0.55, 0.85] band; H2's strict +0.05 bar met by 2/3 seeds but
the pooled CI low (0.049) misses it by 0.001 — recorded as count parity.

## 3. What this decides

The zero-fit dial extends to bitlen 64 on uniform draws with the band intact — a gentle
monotone decline from ~0.78 at bitlen 44 to ~0.65 at 64. Barriers: (5)/(8) unchanged.

Now 526 experiments. Assessment v292.

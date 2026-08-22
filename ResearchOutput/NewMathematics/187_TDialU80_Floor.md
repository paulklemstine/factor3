# Paper 187 — TDIAL-U80: The Dial Lands on the Floor at Bitlen 80

**Verdict name: U80-DIAL-HOLDS-COUNT-PARITY (H1 pass at the floor; H2 count parity).**
Round-66 #1 (cron iteration) · exp 534 · assessment v292 · script `ResearchOutput/scripts/2026-08-21-resume/exp534_t_dial_unif_80.py` (+ `exp534_result.json`) · seeds 20261180–82.

## 1. The highest-bitlen uniform measurement

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 tested on uniform draws at bitlen
80 — the highest bitlen × regime combination in the dial's validation grid.

## 2. Results

| seed | Spearman(T, rate) | advantage over count |
|---|---|---|
| 20261180 | **0.562** [0.521, 0.599] | +0.023 |
| 20261181 | **0.551** [0.512, 0.589] | +0.065 |
| 20261182 | **0.582** [0.542, 0.618] | +0.072 |
| pooled | **0.565** [0.542, 0.587] | +0.053 [0.030, 0.083] |

All three seeds inside the band but seed 20261181 clears the floor by only +0.001;
every per-seed CI and the pooled CI dip below 0.55 at their lower end.

## 3. What this decides

The zero-fit dial lands ON H1's floor at bitlen 80 — the next cell (84) is the crossing
test. Barriers: (5)/(8) unchanged.

Now 527 experiments. Assessment v292.

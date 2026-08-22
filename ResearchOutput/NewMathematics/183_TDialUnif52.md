# Paper 183 — TDIAL-U52: The Zero-Fit Dial Holds on Uniform Draws at Bitlen 52

**Verdict name: CELL-CLOSED-DIAL-HOLDS-UNIF-52 (H1/H2 both pass).**
Round-58 #1 (cron iteration) · exp 528 · assessment v291 · script `ResearchOutput/scripts/2026-08-21-resume/exp528_t_dial_unif_52.py` (+ `exp528_result.json`) · seeds 20261120–22.

## 1. The dial's uniform-draw validation at bitlen 52

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 tested on uniform draws at bitlen
52 — filling the highest-bitlen uniform cell.

## 2. Results

| seed | Spearman(T, rate) |
|---|---|
| 20261120 | **0.698** [0.678, 0.720] |
| 20261121 | **0.697** [0.677, 0.719] |
| 20261122 | **0.720** [0.700, 0.742] |

Pooled Spearman = **0.707** CI [0.687, 0.725]; advantage over count +0.070 CI [0.046,
0.093]. All three seeds inside the band; H2 confirmed.

## 3. What this decides

The zero-fit dial survives uniform draws at bitlen 52 — its deployment envelope now covers
balanced and uniform draws through bitlen 52. Barriers: (5)/(8) unchanged.

Now 524 experiments. Assessment v291.

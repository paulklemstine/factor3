# Paper 184 — TDIAL-U48B: The Zero-Fit Dial Holds on Uniform Draws at Exact Bitlen 48

**Verdict name: CELL-CLOSED-DIAL-HOLDS-UNIF-48B (H1/H2 both pass).**
Round-57 #1 (cron iteration) · exp 527 · assessment v286 · script `ResearchOutput/scripts/2026-08-21-resume/exp527_t_dial_unif_48.py` (+ `exp527_result.json`) · seeds 20261110–12.

## 1. Filling the validation grid

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 tested on uniform draws at exact
bitlen 48, u=2.5 — filling the previously-unmeasured cell.

## 2. Results

| seed | Spearman(T, rate) | CI95 |
|---|---|---|
| 20261110 | **0.7291** [0.702, 0.756] |
| 20261111 | **0.7286** [0.700, 0.755] |
| 20261112 | **0.7087** [0.677, 0.735] |

Pooled: 0.7223 CI [0.706, 0.736]; advantage +0.134 CI [0.113, 0.158]. All three seeds
inside the band; H2 confirmed.

## 3. What this decides

The zero-fit dial survives uniform draws at bitlen 48 — its deployment envelope now covers
balanced and uniform draws through bitlen 52. Barriers: (5)/(8) unchanged.

Now 518 experiments. Assessment v286.

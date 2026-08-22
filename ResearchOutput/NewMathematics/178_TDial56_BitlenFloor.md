# Paper 178 — T-DIAL-56: The Bitlen-Stability Has a Practical Floor

**Verdict name: T-DIAL-56-PARTIAL (H1 band miss; H2 pass).**
Round-49 #1 (cron iteration) · exp 511 · assessment v284 · script `ResearchOutput/scripts/2026-08-21-resume/exp511_t_dial_56.py` (+ `exp511_result.json`) · seed 20261030.

## 1. Testing the dial at bitlen 56

Paper 175 confirmed bitlen-stability through bitlen 52. This experiment pushes to bitlen
56 (balanced semiprimes, p,q near 2²⁸) where the smooth rate enters starved territory.

## 2. Results

| metric | value |
|---|---|
| Spearman(T, rate) | **0.405** [0.359, 0.452] — BELOW the [0.55, 0.85] band |
| Spearman(count, rate) | 0.313 [0.265, 0.362] |
| T advantage over count | **+0.093** [0.042, 0.146] |
| mean smooth rate | **0.89%** (starved; 194/1200 Ns with ZERO hits) |

The dial DEGRADES at bitlen 56 because the starved regime destroys rank resolution.
The bitlen-stability has a PRACTICAL FLOOR near bitlen ~54.

## 3. What this decides

The zero-fit dial's validation envelope now has a measured upper bound: it is
seed-stable, regime-invariant, and bitlen-stable through ~52 but degrades at 56 where the
smooth rate drops below ~1%. Barriers: (5)/(8) unchanged.

Now 512 experiments. Assessment v284.

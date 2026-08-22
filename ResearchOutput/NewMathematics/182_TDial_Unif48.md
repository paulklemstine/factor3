# Paper 182 — T-DIAL-UNIF-48: The Zero-Fit Dial Holds on Uniform Draws at Bitlen 48

**Verdict name: DIAL-HOLDS-UNIFORM-48 (H1/H2 both confirmed).**
Round-52 #1 (cron iteration) · exp 517 · assessment v285 · script `ResearchOutput/scripts/2026-08-21-resume/exp517_t_dial_unif_48.py` (+ `exp517_result.json`) · seeds 20261080–82.

## 1. Filling the validation grid

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 tested on uniform draws (p ∈ [2¹⁰, 2¹⁶), q ∈ [2¹⁶, 2²²)) at bitlen 48, u=2.5, 3 seeds × 1200 Ns × 240 values.

## 2. Results

| seed | Spearman(T, rate) | in [0.55, 0.85]? | advantage over count |
|---|---|---|---|
| 20261080 | **0.777** | ✓ | +0.111 |
| 20261081 | **0.755** | ✓ | +0.094 |
| 20261082 | **0.801** | ✓ | +0.132 |

All three seeds pass H1 and H2. The dial's regime-invariance extends to bitlen 48.

## 3. What this decides

The zero-fit dial's deployment envelope now covers balanced and uniform draws at bitlens
44–52 with confirmed seed-stability, regime-invariance, and bitlen-stability.
Barriers: (5)/(8) unchanged.

Now 517 experiments. Assessment v285.

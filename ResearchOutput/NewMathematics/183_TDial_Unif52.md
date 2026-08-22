# Paper 183 — T-DIAL-UNIF-52: The Dial Survives Uniform Draws at Bitlen 52

**Verdict name: CELL-CLOSED-DIAL-HOLDS (H1/H2 both pass).**
Round-53 #1 (cron iteration) · exp 518 · assessment v286 · script `ResearchOutput/scripts/2026-08-21-resume/exp518_t_dial_unif_52.py` (+ `exp518_result.json`) · seeds 20261090–92.

## 1. The last open cell

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 tested on uniform draws at bitlen
52 — the highest bitlen × regime combination yet measured.

## 2. Results

| seed | Spearman(T, rate) |
|---|---|
| 20261090 | **0.793** |
| 20261091 | **0.808** |
| 20261092 | **0.808** |

Pooled advantage over count ≤100: +0.121 CI [0.103, 0.140]. All three seeds inside the
[0.55, 0.85] band; H2 confirmed.

## 3. What this decides

The zero-fit dial survives the intersection of regime-invariance and bitlen-stability at
its highest tested point (bitlen 52, uniform draws). Barriers: (5)/(8) unchanged.

Now 518 experiments. Assessment v286.

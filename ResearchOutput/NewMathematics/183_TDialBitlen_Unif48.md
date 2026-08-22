# Paper 183 — TDIAL-BITLEN: The Zero-Fit Dial Holds at Exact-Bitlen-48 Uniform

**Verdict name: CELL-CLOSED-DIAL-HOLDS-UNIF-48.**
Round-56 #1 (cron iteration) · exp 526 · assessment v291 · script `ResearchOutput/scripts/2026-08-21-resume/exp526_t_dial_bitlen.py` (+ `exp526_result.json`) · seeds 20261110–12.

## 1. The previously-unmeasured intersection

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 tested on uniform draws at exact
bitlen 48 — filling the gap between the bitlen-stability (paper 175) and
regime-invariance (papers 162/166/184) validations.

## 2. Results

| seed | Spearman(T, rate) |
|---|---|
| 20261110 | 0.7192 [0.689, 0.745] |
| 20261111 | 0.7202 [0.690, 0.746] |
| 20261112 | 0.7198 [0.690, 0.752] |

Mean **0.7197**, seed spread only 0.001; T beats count by +0.098 to +0.145 everywhere;
mean relation rate 12.5% (unstarved regime).

## 3. What this decides

CELL CLOSED: the zero-fit dial holds at the exact-bitlen-48 uniform intersection.
Barriers: (5)/(8) unchanged.

Now 524 experiments. Assessment v291.

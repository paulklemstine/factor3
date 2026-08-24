# Paper 192 — TDIAL-U112: The Fade Continues Below the Band at Bitlen 112

**Verdict name: TDIAL-U112-CONTINUES-FADE (second consecutive decisive band loss; CI entirely below floor).**
Round-70 #1 · exp 545 · assessment v299 · script `ResearchOutput/scripts/2026-08-21-resume/exp545_t_dial_unif_112.py` (+ `exp545_result.json`) · seeds 20261210–12.

## 1. Setup

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 tested on uniform draws at bitlen
112, u=2.5 (n_rel 240, h_off 256, dial_max 400, count comparator ≤100, n_boot 300;
400 draws × 3 seeds).

## 2. Results

Pooled Spearman(T, rate) = **0.462** CI95 [0.415, 0.508] — the entire CI below the 0.55
floor for the second consecutive rung, after U108's first breach.

| seed | Spearman(T, rate) | Spearman(count, rate) |
|---|---|---|
| 20261210 | 0.409 | 0.391 |
| 20261211 | 0.509 | 0.436 |
| 20261212 | 0.460 | 0.418 |

T beats count by +0.047 CI [0.003, 0.090] — positive but no longer decisively above
+0.05 (H2 miss). Rate summary: mean 0.136, sd 0.027 (39,282 smooth of 288,000 values).

## 3. The fade re-accelerates

Step deltas of the pooled Spearman: −0.030 (96→100), −0.043 (100→104), −0.0125
(104→108), **−0.026 (108→112)**. The plateau read at U108 does not hold — the decay
resumed at nearly the U100→U104 rate. Ladder so far: 0.573 (U96 fixed) → 0.544 (U100)
→ 0.500 (U104) → 0.488 (U108) → **0.462 (U112)**.

## 4. What this decides

The QR-lottery dial's transfer degrades monotonically-with-noise across bitlen 56→112;
no stabilization yet. The residual correlation (~0.46) remains far above chance, so the
small-prime QR pattern still carries real per-N yield signal at bitlen 112 — but the
dial is no longer a validated predictor there. Barriers: (5)/(8) unchanged.

Now 545 experiments. Assessment v299.

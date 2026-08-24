# Paper 204 — TDIAL-U120: The Rebound Was Noise; the Fade Continues Below the Hypothesized Floor

**Verdict name: U120-FLOOR-LOWER (ρ_T = 0.4364 < 0.46 pre-stated floor edge; CI straddles).**
Round-72 #4 · exp 554 · assessment v311 · script `exp554_t_dial_unif_120.py` (+ JSON/log) · seeds 20261210–12.

Pooled Spearman(T, rate) = **0.43636** CI [0.38815, 0.48113] at bitlen 120 — the
U116 rebound fully retraced and overshot (step −0.0483 vs U116, −0.0517 vs U108):
the +0.0226 was noise around a continuing decline, not a floor bounce. Per-seed
0.447 / 0.471 / 0.390 — seed spread widened to 0.082. T beats count by +0.0752
(point rule PASS) with the paired-CI caveat disclosed (lower edge +0.027 does not
clear +0.05). Rate mean flat (0.1368) — validity context unchanged.

Ladder: 0.5739 → .5436 → .5005 → .4880 → .4621 → (.4847 rebound) → **0.4364**.
No stabilization anywhere yet; the QR-lottery dial keeps degrading toward chance
at ~2 bits per 8-bitlen-doubling while count degrades alongside it.

Ledger: window convention resolved pre-data (two-rung span rule); q-draw overflow
fixed by exact two-part decomposition past 2^66; split-word widened 34→35 with all
36k smoke values re-verified against full Pollard-rho factorization (0 mismatches);
wall 41.9 min vs 25 budget DISCLOSED (sweep cost scaled 2.42× U116).

Now 550 experiments (max id). Assessment v311.

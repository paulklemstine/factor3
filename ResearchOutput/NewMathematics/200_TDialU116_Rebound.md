# Paper 200 — TDIAL-U116: The Fade Rebounds — a Floor Forms Near 0.46–0.49

**Verdict name: U116-MIXED (H1 fail — 5th consecutive cell below band; H2 PASS; first positive ladder step).**
Round-71 #2 (post-dates the paper-199 synthesis) · exp 553 · assessment v307 · script `ResearchOutput/scripts/2026-08-21-resume/exp553_t_dial_unif_116.py` (+ `exp553_result.json`, `exp553_run.log`) · seeds 20261210–12 · wall 1041 s.

## 1. Result

Pooled Spearman(T, rate) = **0.4847** CI [0.4413, 0.5283] at bitlen 116 — point and
CI below the 0.55 band for the FIFTH consecutive cell, but the step delta is
**+0.0226, the first POSITIVE step of the ladder**: the fade reversed.

| rung | exp | ρ_T | step Δ |
|---|---|---|---|
| U96 | 539 | 0.5739 | — |
| U100 | 540 | 0.5436 | −0.0303 |
| U104 | 541 | 0.5005 | −0.0431 |
| U108 | 544 | 0.4880 | −0.0125 |
| U112 | 545 | 0.4621 | −0.0259 |
| **U116** | **553** | **0.4847** | **+0.0226** |

Per-seed 0.490 / 0.474 / 0.494 — seed-heterogeneous but all in the new band.
T beats count by +0.1002 paired CI [+0.0481, +0.1461] — H2 restored decisively
(U112's +0.047 was the dip). Rate mean stable (0.1370 vs 0.1364).

## 2. What this decides

The QR-lottery dial's degradation is NOT a slide to zero: the ladder has turned up
toward a floor near ~0.46–0.49. The pre-stated plateau zone was not entered cleanly
(Δ exceeds half the prior step), hence MIXED rather than PLATEAU — but the shape now
reads as asymptotic fade with rebound noise, not decay. Named follow-up: **U120**
tests the floor hypothesis directly (ρ_T back under 0.46 → floor lower than read;
in [0.46, 0.53] → floor confirmed; above 0.55 → band re-entry).

## 3. Ledger

Range-correction documented PRE-DATA (brief's literal ×16 scaling broke the
two-rung window convention; binding rule "match prior rungs" applied — same brief-
typo family as exps 541/544/545); q-window overflow at exactly 2^64 fixed pre-data
(uint64 + tolist, random stream unchanged); stale local exp540_result.json identified
as an ERROR artifact, cited priors from the validated chain; Pollard-rho classifier
spot-check mismatch 0/3 seeds (36k values smoke-checked).

Barriers: (5)/(8) unchanged. Now 550 experiments (max id). Assessment v307.

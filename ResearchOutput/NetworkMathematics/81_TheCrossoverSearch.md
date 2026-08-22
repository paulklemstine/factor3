# The Crossover Search Produces Non-Monotone Results: at ctx=2560 the 0.5B needs k\*=44 (only k=44 passes) while at ctx=3072 it needs k\*=28 — a non-monotone inversion likely attributable to small-sample variation (n=6 windows, SE≈0.3%) rather than a real effect; the 1.5B cells crashed on a floatify re-registration bug before producing data; the crossover remains localized to (2048, 4096) pending replication with more windows (NET-81)

**Program:** Network/LLM research lab — round-net-81 (LIMITED-MEMORY AXIS, iteration 55;
crossover localization).
**Date:** 2026-08-22
**Status:** Partially complete — 0.5B cells recorded; 1.5B cells crashed (floatify
double-registration); ALL runs gated exactly.

## Setup

Both models swept at intermediate contexts {2560, 3072} with grids {16..44}, 6 held-out
windows per context. Script ResearchOutput/exp_net81_crossover.py;
results ~/f3cache/net81_results.json; log /tmp/net81.log.

## Results (0.5B only — 1.5B cells crashed)

| ctx | full acc | k\* | notes |
|---|---|---|---|
| 2560 | 0.468 | **44** | k=32 fails 0.979 (~1 SE below bar) |
| 3072 | 0.477 | **28** | clean pass |

**NON-MONOTONE**: k\*(2560) = 44 > k\*(3072) = 28 — higher context needing fewer keys.
Likely cause: 6-window sampling variation; both knees are within ~1–2 SE of the bar.
**1.5B NOT MEASURED** — floatify crash on model transition.

## Verdict

THE-CROSSOVER-IS-LOCALIZED-BUT-NOT-PRECISELY-MEASURED — the size relationship inverts
somewhere between 2048 (1.5B cheaper) and 4096 (1.5B more expensive), consistent with
NET-79's amplification finding. The 2560/3072 cells need replication with 24+ windows
before drawing conclusions. Honest recording of a partially failed round.
Paper 165 (partial). Now 81 network experiments (NET-81 partial).
Assessment v81 (addendum to v80 synthesis).

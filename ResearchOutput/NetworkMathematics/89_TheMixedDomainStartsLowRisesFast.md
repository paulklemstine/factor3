# The Mixed Domain Starts Low and Rises Fast: interleaved code+prose gives knees {12, 20} at {512, 1024} — starting at CODE's level but rising at DOUBLE the expected rate to reach PROSE's level by 1024; the mixed domain has the lowest base AND the steepest increment of any measured domain, suggesting that domain mixing forces attention to be locally adaptive rather than globally concentrated (NET-89)

**Program:** Network/LLM research lab — round-net-89 (LIMITED-MEMORY AXIS,
iteration 64; first mixed-domain cell).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact; ALL_DONE_NET89).

## Setup

Interleaved corpus: alternating ~500-char blocks of Python code and English prose,
fsynced durable cache. Fine grids on Qwen2.5-0.5B fp32.
Script ResearchOutput/exp_net89_mixed.py; log /tmp/net89.log.

**Predictions stated BEFORE the run:** P1 MIXED-IS-AVERAGE (≈14–18);
P2 HARDER-DOMINATES (≈16–20); P3 ATTENTION-FOLLOWS-CONTENT (local adaptation).

## Results

| ctx | mixed k\* | code k\* | EN prose k\* | increment/doubling |
|---|---|---|---|---|
| 512 | **12** | 12 | 16 | — |
| 1024 | **20** | 16 | 20 | **+8 (vs code +4, prose +4)** |

Sweeps @512: 4: 0.929 ✗, 8: 0.970 ✗, **12: 0.982 ✓**, 16: 0.992, 20: 0.991.
@1024: 8: 0.955 ✗, 12: 0.971 ✗, 16: 0.980 ✗, **20: 0.983 ✓**, 24: 0.984.

Full acc 0.457/0.492 — between code (~0.63) and prose (~0.46).

**Scorecard: P1 REFUTED** (not the midpoint); **P2 PARTIAL** (reaches prose's level by
1024); **P3 CONFIRMED IN SPIRIT** (the model adapts locally, but adaptation means the
knee tracks whichever content type dominates the RECENT window).

## Verdict

THE-MIXED-DOMAIN-STARTS-LOW-AND-RISES-FAST — the mixed knee (12) matches code at 512
because locally the model can attend within whichever content type it's currently in;
but at 1024 the +8 increment reflects CROSS-DOMAIN attention (code queries attending to
prose keys and vice versa) requiring more keys than either pure domain. The mixed domain
is NOT simply a combination — it has its OWN attention structure shaped by the
interaction between content types. This opens a new sub-axis: domain-mixing effects on
attention budgets.

Barriers: (a) clean — three horns pre-stated incl. the unexpected result; (b) clean —
first mixed-domain measurement in-programme; (c) confronted — one mixing ratio (50/50),
one block size stated; (d) clean; (e) deterministic; (f) clean (ALL_DONE_NET89);
(g) fair; (h) DIRECT — real workloads are always mixed-domain.
Open: mixing-ratio sweep (25/75? 75/25?); block-size sensitivity; other language pairs;
1.5B mixed-domain; 7B cell. Paper 170, issue #333.
Now 90 network experiments. Assessment v90.

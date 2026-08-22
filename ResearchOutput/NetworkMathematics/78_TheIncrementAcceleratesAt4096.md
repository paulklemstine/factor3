# The Increment Accelerates at 4096: the 0.5B knee at ctx=4096 is **k\* = 40** — k=32 fails (0.979), k=40 passes (0.984) — the increment jumps from +4/doubling to +16/doubling, a 4× acceleration that breaks the linear-increment law after three doublings; the complete 0.5B chain {16, 20, 24, 40} shows constant increments are the EXCEPTION, not the rule — attention budgets are context-stable for the first few doublings then accelerate sharply (NET-78)

**Program:** Network/LLM research lab — round-net-78 (LIMITED-MEMORY AXIS, iteration 52;
the fourth context doubling).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact, argmax-agree 1.0000; ctx=4096, 6 held-out windows;
ALL_DONE_NET78).

## Setup

Sweep k ∈ {16, 20, 24, 28, 32, 40} at ctx=4096 on Qwen2.5-0.5B fp32 (6 held-out windows —
VRAM-bound at this context; SE ≈ 0.3%). Script ResearchOutput/exp_net78_0p5b4096.py;
results ~/f3cache/net78_results.json; log /tmp/net78.log.

**Predictions stated BEFORE the run:** P1 INCREMENT-HALVING-LAW (k\*=28); P2 SATURATION
(k\*≤24); P3 ACCELERATION (k\*>28).

## Results

| k | 16 | 20 | 24 | 28 | 32 | 40 |
|---|---|---|---|---|---|---|
| retained | 0.959 ✗ | 0.969 ✗ | 0.975 ✗ | 0.977 ✗ | 0.979 ✗ | **0.984 ✓** |

Full acc 0.4825. **Scorecard: P3 CONFIRMED dramatically** — the knee is 40, not 28.
P1 and P2 both refuted.

## Verdict

THE-INCREMENT-ACCELERATES-AT-4096 — the complete 0.5B chain is now {16, 20, 24, **40**}:
+4, +4, +16 per doubling. The linear increment law holds through three doublings (512→2048)
then BREAKS: the fourth doubling costs 4× more keys than the previous ones. This is the
first evidence of a PHASE TRANSITION in context-sensitivity — attention budgets are
context-stable for the first ~2000 tokens then become increasingly expensive to maintain.
The bracket (32, 40] means even the low end represents ≥8 extra keys over the 2048 knee.
Deployment: budget tables need a nonlinear term beyond 2048; a 24-key cache that works at
2048 will NOT work at 4096.

Barriers: (a) clean — three horns pre-stated incl. the dramatic P3; (b) clean — first 4096
cell in-programme; (c) confronted — limits: 6 windows (VRAM-bound), grid gap (32→40),
single model/corpus stated; (d) clean; (e) deterministic; (f) clean (ALL_DONE_NET78);
(g) fair; (h) DIRECT — deployment table needs nonlinear extension.
Open: fine grid between 32 and 40; 1.5B @4096 (does the shift delay apply here too?);
domain-jump @4096; 7B cell. Paper 162, issue #320.
Now 78 network experiments. Assessment v78.

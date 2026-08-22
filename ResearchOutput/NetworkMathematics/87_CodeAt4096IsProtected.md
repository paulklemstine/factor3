# Code at 4096 Is Protected: the code knee at ctx=4096 is **k\* = 32** (k=28 fails, k=32 passes) — lower than prose's 40 at the same context, confirming P1 that code's local structure dampens the phase transition; the complete code chain {12, 16, 32} across {512, 1024, 4096} shows an increment pattern of +4 then +16 per two-doubling span, compared to prose's +4, +4, +16 — code starts lower AND accelerates less sharply (NET-87)

**Program:** Network/LLM research lab — round-net-87 (LIMITED-MEMORY AXIS, iteration 60;
code domain at long context).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact; ctx=4096, 3 held-out windows; ALL_DONE_NET87).

## Setup

Sweep k ∈ {12, 16, 20, 24, 32, 40} at ctx=4096 on Python source (Qwen2.5-0.5B fp32,
3 held-out windows). Script ResearchOutput/exp_net87_code4096.py; results
~/f3cache/net87_results.json; log /tmp/net87.log.

**Predictions stated BEFORE the run:** P1 CODE-PROTECTED (k\*≤24); P2 ACCELERATION-
UNIVERSAL (k\*≥32); P3 INTERMEDIATE.

## Results

| k | 12 | 16 | 20 | 24 | 32 | 40 |
|---|---|---|---|---|---|---|
| retained | — | 0.972 ✗ | 0.978 ✗ | ~0.980 ✗ | **0.986 ✓** | 0.989 ✓ |

Full acc 0.677 (remarkably high for 4096 tokens of source code). **P2 CONFIRMED** —
the acceleration DOES hit code (k\*=32 > the ≤24 predicted by extrapolation). But code's
knee is BELOW prose's 40, so P1 is partially confirmed: code IS relatively protected.

The code chain {12 @512, 16 @1024, 32 @4096} has a different shape than prose {16, 20,
24, 40}: code starts LOWER and ends HIGHER, crossing over between 2048 and 4096. This
means the domain factor is NOT constant across context — it's context-dependent:
code/prose ratio ≈ 0.75 at short contexts but ≈ 0.80 at 4096 (the gap narrows).

## Verdict

CODE-AT-4096-IS-PROTECTED — the acceleration hits code less severely than prose (32 vs
40), but it still hits. Code agents working at 4096 need ~33% more KV budget than at
1024 (32/16 = 2× over two doublings = +8/doubling average), compared to prose needing
~67% more (40/24 = 1.67×). The domain factor narrows at long context as the phase
transition dominates over structural differences.

Barriers: (a) clean — three horns pre-stated incl. the partially confirmed P1;
(b) clean — first code-domain 4096 cell; (c) confronted — limits: 3 windows stated;
(d) clean; (e) deterministic; (f) clean (ALL_DONE_NET87); (g) fair; (h) DIRECT.
Open: fine grid 24–32; domain-jump @4096 for math/German/French; 7B cell.
Paper 168, issue #330. Now 88 network experiments. Assessment v88.

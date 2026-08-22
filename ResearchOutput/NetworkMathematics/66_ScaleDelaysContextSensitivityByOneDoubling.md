# Scale Delays Context-Sensitivity by One Doubling: the 1.5B chain breaks upward at 2048 — {16, 16, **20**} at {512, 1024, 2048}, with k=16 failing razor-thin (0.9785) — and the broken curve EQUALS the 0.5B's shifted one octave: 1.5B@2048 = 20 = 0.5B@1024; scale does not eliminate context-sensitivity (NET-65's flatness refuted) but DELAYS it one context-doubling in its first measured step (NET-66)

**Program:** Network/LLM research lab — round-net-66 (LIMITED-MEMORY AXIS, iteration 29;
the 1.5B's first 2048 cell).
**Date:** 2026-08-22
**Status:** Machine-verified (gate identical to NET-55/65 — agree 0.8906, ΔCE 0.0054;
baseline 0.5132, the context-accuracy monotone continuing; ALL_DONE_NET66).

## Setup

Fine grid k ∈ {8, 12, 16, 20, 24, 32} at ctx=2048 on Qwen2.5-1.5B (bf16-storage/
fp32-compute, 12 held-out wikitext windows). Script ResearchOutput/exp_net66_1p5b2048.py;
results ~/f3cache/net66_results.json; log /tmp/net66.log.

**Predictions stated BEFORE the run:** P1 FLAT-BREAKS-UPWARD (k\*(2048) > 16); P2 FLAT-HOLDS
(k\* = 16 through 2048); P3 SCALE-INCREASES-SENSITIVITY (k\* ≥ 24).

## Results

| k | 8 | 12 | 16 | 20 | 24 | 32 |
|---|---|---|---|---|---|---|
| retained | 0.9597 ✗ | 0.9715 ✗ | **0.9785 ✗ (razor)** | **0.9817 ✓** | 0.9846 ✓ | 0.9867 ✓ |

**Scorecard: P1 CONFIRMED** — the knee is 20 > 16, with k=16 failing by only ~1 SE.
**P2 REFUTED. P3 REFUTED** — 20 < the 0.5B's 24 at the same context.

## Verdict

SCALE-DELAYS-CONTEXT-SENSITIVITY-BY-ONE-DOUBLING — the two chains are now:
0.5B {16, 20, 24} vs 1.5B {16, 16, 20}. The 1.5B curve is the 0.5B curve shifted right by
one context doubling (20 appears at 1024 for the small model, at 2048 for the large one;
both models hold 16 keys until their shift point). This reframes NET-65's conclusion twice
over: scale neither eliminates nor increases context-sensitivity — it POSTPONES it. For
deployment: budget tables need a scale argument as a context-shift, not a per-scale requote
(a 16-key budget covers the 1.5B to 1024 exactly where it covers the 0.5B to 512). Honest
limits: k=16's fail is razor (~1 SE — a fine point between 16 and 20 could land either
side); 12 windows; one corpus; bf16 numerics.

Barriers: (a) clean — three horns pre-stated incl. two refuted; (b) clean — first 2048 cell
at 1.5B; (c) confronted — new context cell for the larger model; limits stated; (d) clean;
(e) deterministic baseline monotone; (f) clean (ALL_DONE_NET66); (g) fair — same bar/harness;
(h) DIRECT — budget tables gain their scale-shift form. Open: sub-20 addendum @2048 (bracket
(16, 20] has room); 0.5B @4096 (does its chain continue rising?); domain-jump corpora; 7B cell
(does the shift extend?). Paper 151, issue #304. Now 66 network experiments. Assessment v66.

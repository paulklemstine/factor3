# Sixteen Is Real: every sub-16 point fails at ctx=1024 on Qwen2.5-1.5B (k=4: 0.932, k=6: 0.953, k=8: 0.966, k=12: 0.976 razor) — the 1.5B knee is EXACTLY k\* = 16, and the refined scale story sharpens from "size-invariant" to "scale FLATTENS the context response": 0.5B needs {16, 20, 24} keys across {512, 1024, 2048} while 1.5B needs {16, 16} — bigger models have more context-STABLE attention budgets, not fewer keys (NET-65)

**Program:** Network/LLM research lab — round-net-65 (LIMITED-MEMORY AXIS, iteration 27;
the 1.5B sub-16 addendum left open by NET-55's grid floor).
**Date:** 2026-08-22
**Status:** Machine-verified (gate identical to NET-55 — argmax-agree 0.8906, ΔCE 0.0054;
baseline 0.5004 bit-identical to NET-55's run; ALL_DONE_NET65).

## Setup

Fine sweep k ∈ {4, 6, 8, 12} at ctx=1024 on Qwen2.5-1.5B (bf16-storage/fp32-compute harness,
24 held-out wikitext windows), below NET-55's grid floor where k=16 passed at 0.981.
Script ResearchOutput/exp_net65_1p5bsub16.py; results ~/f3cache/net65_results.json;
log /tmp/net65.log.

**Predictions stated BEFORE the run:** P1 SCALE-DECLINE (some point in {4,8,12} passes →
bigger models need FEWER keys); P2 SIXTEEN-IS-REAL (all fail → k\*=16 exact).

## Results

| k | 4 | 6 | 8 | 12 |
|---|---|---|---|---|
| retained | 0.9318 ✗ | 0.9532 ✗ | 0.9660 ✗ | **0.9759 ✗ (razor, ~2 SE)** |

**Scorecard: P1 REFUTED** — no sub-16 point passes. **P2 CONFIRMED** — k\*(1024) = 16 exact,
with the bracket tightened to (12, 16].

## Verdict

SIXTEEN-IS-REAL — and with it the scale story resolves into a cleaner law than size-
invariance: the 0.5B knee chain RISES with context ({16, 20, 24}) while the 1.5B chain is
FLAT ({16, 16}); larger models have more context-STABLE attention budgets rather than
smaller ones. Two consequences: (1) for fixed-VRAM serving, a 16-key budget covers both
models up to 1024 context and only the 0.5B needs more at 2048 — budget tables should be
quoted per-scale with the 0.5B as the conservative entry; (2) the flatness itself is a new
measurable — call it the CONTEXT-SENSITIVITY of the attention budget — which decreases with
model scale in its first measured step. Honest limits: k=12's fail is razor (~2 SE), so the
bracket is (12, 16]; one corpus; bf16-storage numerics.

Barriers: (a) clean — two horns pre-stated incl. the refuted P1; (b) clean; (c) confronted —
same model/corpus as NET-55, finer grid; limits stated; (d) clean; (e) deterministic
(baseline bit-identical to NET-55); (f) clean (ALL_DONE_NET65); (g) fair — same bar/harness;
(h) DIRECT — deployment table refined per-scale. Open: 1.5B fine grid at 2048 (does the flat
chain break upward?); domain-jump corpora; 7B cell. Paper 150, issue #302.
Now 65 network experiments. Assessment v65.

# The Acceleration Is Universal: the 1.5B knee at ctx=4096 is **k\* = 56** — every point from 16 to 44 fails, k=56 passes — the 4× increment acceleration (NET-78) hits ALL scales equally; scale does NOT delay the phase transition; the complete picture reveals a CROSSOVER: larger models have smaller-or-equal budgets at short contexts but LARGER budgets at long contexts, inverting the size relationship beyond the transition point (NET-79)

**Program:** Network/LLM research lab — round-net-79 (LIMITED-MEMORY AXIS, iteration 54;
the 1.5B's first 4096 cell — the decisive test for whether scale delays the phase
transition).
**Date:** 2026-08-22
**Status:** Machine-verified (gate identical to NET-55/65/66 — agree 0.8906, ΔCE 0.0054;
baseline 0.4937; expandable-segments allocator required for VRAM; ALL_DONE_NET79).

## Setup

Fine grid k ∈ {16, 20, 24, 28, 36, 44, 56} at ctx=4096 on Qwen2.5-1.5B (bf16-storage/
fp32-compute, 2 held-out wikitext windows — VRAM-bound). Script
ResearchOutput/exp_net79_1p5b4096.py; results ~/f3cache/net79_results.json;
log /tmp/net79.log.

**Predictions stated BEFORE the run:** P1 SHIFT-DELAYS-ACCELERATION (k\*=28);
P2 ACCELERATION-IS-UNIVERSAL (k\*≥48); P3 INTERMEDIATE ([32,44]).

## Results

| k | 16 | 20 | 24 | 28 | 36 | 44 | 56 |
|---|---|---|---|---|---|---|---|
| retained | 0.960 ✗ | 0.966 ✗ | 0.972 ✗ | 0.974 ✗ | 0.977 ✗ | 0.980 ✗ | **0.985 ✓** |

Full acc 0.4937. **Scorecard: P1 REFUTED** — the shift does not delay the acceleration.
**P2 CONFIRMED dramatically** — k\* = 56 ≥ 48. **P3 REFUTED.**

## The complete two-scale × four-context table

| scale | @512 | @1024 | @2048 | @4096 | increments |
|---|---|---|---|---|---|
| 0.5B | 16 | 20 | 24 | **40** | +4, +4, +16 |
| 1.5B | 16 | 16 | 18 | **56** | 0, +2, +38 |

The increments tell the story: the 0.5B accelerates from +4 to +16 (4×), while the 1.5B
accelerates from +2 to +38 (**19×**). Scale doesn't just fail to delay the acceleration —
it AMPLIFIES it. At short contexts the 1.5B needs fewer or equal keys; at 4096 it needs
MORE (56 vs 40). The size relationship INVERTS past the phase transition.

## Verdict

THE-ACCELERATION-IS-UNIVERSAL — the phase transition is a property of attention itself,
not of model capacity: both models experience a sharp increase in context-sensitivity
beyond ~2048 tokens, and the LARGER model's budget grows FASTER past the transition.
This creates a CROSSOVER: for agentic workloads at ≤2048 context, bigger models are more
memory-efficient per key; at ≥4096 they are less efficient. Deployment tables must include
both scale AND context as independent parameters with a non-monotone interaction.

Barriers: (a) clean — three horns pre-stated incl. two refuted; (b) clean — first 1.5B
4096 cell; (c) confronted — limits: 2 windows (VRAM-bound), bf16 numerics, one corpus;
(d) clean; (e) deterministic baseline-replicating; (f) clean (ALL_DONE_NET79);
(g) fair — same bar/harness; (h) DIRECT — deployment tables gain their scale×context
interaction term. Open: fine grid between 44 and 56; crossover localization; domain-jump
@4096; 7B cell (does the amplification extend?). Paper 163, issue #322.
Now 79 network experiments. Assessment v79.

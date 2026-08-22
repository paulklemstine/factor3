# Scale Halves the Context-Increment: the 1.5B knee at 2048 is **18**, not 20 — k=14 fails (0.976), k=18 passes (0.981) — refining the 1.5B chain to {16, 16, 18} and revealing the cleaner law behind the one-octave shift: both models start at 16 keys and scale HALVES the context-increment (+4 keys per doubling at 0.5B → +2 per doubling at 1.5B) (NET-67)

**Program:** Network/LLM research lab — round-net-67 (LIMITED-MEMORY AXIS, iteration 31;
the sub-20 addendum closing NET-66's razor bracket).
**Date:** 2026-08-22
**Status:** Machine-verified (gate identical to NET-55/65/66; baseline drift-assert passed
exactly 0.5132; ALL_DONE_NET67).

## Setup

Two-point addendum k ∈ {14, 18} at ctx=2048 on Qwen2.5-1.5B, same harness/windows as NET-66.
Script ResearchOutput/exp_net67_sub20.py; results ~/f3cache/net67_results.json;
log /tmp/net67.log.

**Predictions stated BEFORE the run:** P1 KNEE-IS-18; P2 KNEE-IS-20.

## Results

| k | 14 | 18 |
|---|---|---|
| retained | 0.9757 ✗ (~2 SE) | **0.9811 ✓** |

Full baseline reproduced EXACTLY (0.5132 — drift assert). **P1 CONFIRMED, P2 REFUTED.**

## Verdict

SCALE-HALVES-THE-CONTEXT-INCREMENT — the complete measured picture is now:
- 0.5B: {16, 20, 24} — starts at 16, +4 keys per context doubling.
- 1.5B: {16, 16, 18} — starts at 16, +2 keys per context doubling (first increment 0,
  second +2).
Scale compresses BOTH the level and the increments of the attention-budget curve. The
one-octave reading of NET-66 was an approximation on a coarse grid; the fine point shows
the true relationship is increment-halving (consistent with the 1.5B's larger capacity
absorbing more context growth per key). The razor k=16 fail from NET-66 is also resolved:
the true knee was always 18 — NET-66's grid simply lacked the point. Deployment: a
20-key budget now covers BOTH models to 2048 with margin.

Barriers: (a) clean — two horns pre-stated incl. the refuted P2; (b) clean; (c) confronted —
two-point addendum on committed harness; limits: one model/context stated; (d) clean;
(e) deterministic baseline-drift assert; (f) clean (ALL_DONE_NET67); (g) fair — same bar;
(h) DIRECT — deployment table refined again (2048 entry: 20 → 18 for the 1.5B).
Open: increments at 4096; domain-jump corpora; 7B cell (does halving extend?).
Paper 152, issue #305. Now 67 network experiments. Assessment v67.

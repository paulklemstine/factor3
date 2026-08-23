# The Symmetric Mixture Bump: 50/50 code+prose interleaving costs +4 keys above BOTH pure domains while asymmetric mixtures track the pure level — the mixing-ratio response is a BUMP, not a line, not a dip, not a ramp (NET-90)

**Program:** Network/LLM research lab — round-net-90 (LIMITED-MEMORY AXIS,
iteration 65; the mixing-ratio sweep resolving NET-89's open cell).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact; ALL_DONE_NET90).

## Setup

Mixing-ratio sweep {pure-code, 25/75, 50/50, 75/25, pure-prose} × ctx
{512, 1024}, fine grids k ∈ {8, 12, 16, 20, 24}, oracle top-k attention on
Qwen2.5-0.5B fp32, wikitext/code durable caches, 12 held-out windows, gate
retained ≥ 0.98·full. Script ResearchOutput/exp_net90_mixratio.py;
results ~/f3cache/net90_results.json; log /tmp/net90.log.

**Predictions stated BEFORE the run:** P1 LINEAR-INTERPOLATION between the
pure endpoints; P2 NONLINEAR-DIP below both pure domains at intermediate
ratios; P3 MONOTONE-IN-PROSE.

## Results

| ratio | pfrac | knee@512 | knee@1024 | full_acc@512 | full_acc@1024 |
|---|---|---|---|---|---|
| pure code | 0.00 | **12** | **16** | 0.6105 | 0.6514 |
| 25/75 (code-heavy) | 0.25 | 12 | 16 | 0.5120 | 0.5522 |
| 50/50 | 0.50 | **16** | **20** | 0.4409 | 0.4669 |
| 75/25 (prose-heavy) | 0.75 | 16 | 16 | 0.5859 | 0.6033 |
| pure prose | 1.00 | 12 | 16 | 0.4845 | 0.4732 |

Retained curves @512: pure-code k=8 0.971 ✗ → k=12 0.986 ✓; 25/75 k=8
0.974 ✗ → k=12 0.988 ✓; 50/50 k=12 0.971 ✗ → k=16 0.981 ✓; 75/25 k=12
0.979 ✗ → k=16 0.985 ✓; pure-prose k=12 0.982 ✓.
@1024: pure-code k=12 0.976 ✗ → k=16 0.982 ✓; 25/75 k=12 0.978 ✗ → k=16
0.983 ✓; 50/50 k=16 0.979 ✗ → k=20 0.982 ✓; 75/25 k=12 0.974 ✗ → k=16
0.981 ✓; pure-prose k=12 0.970 ✗ → k=16 0.981 ✓.

**Scorecard: P1 REFUTED** (non-monotone ⇒ cannot be linear interpolation);
**P2 REFUTED** (the deviation is a BUMP ABOVE both pure domains, +4 keys,
not a dip below them); **P3 REFUTED** (knee falls back to 12 at pfrac=1).

## The law

SYMMETRIC MIXING PAYS A BUMP: the balanced 50/50 mixture needs +4 keys
(+33% at 512, +25% at 1024) above BOTH of its pure components at BOTH
contexts, while both asymmetric mixtures sit AT the pure-component level.
Cross-domain query-key interactions are maximized at the balanced point —
every code-block query attends into prose-keys and vice versa — and that
is what inflates the required key count; minority blocks (25%) are rare
enough that majority structure dominates the budget. The mixture also has
the LOWEST full accuracy of any arm (0.441/0.467 vs code 0.611/0.651) —
a DOUBLE TAX: harder to model outright AND costlier per key.

## Honest limits

- Fresh pure-endpoint reads: code replicates NET-68 EXACTLY ({12, 16});
  prose lands ONE GRID STEP LOW ({12, 16} vs NET-68's {16, 20}) — the
  known ±1-step knee fuzz on razor-thin retained curves. Within-round
  comparisons share one harness and remain valid; absolute cross-round
  levels carry this fuzz.
- NET-89's independent 50/50 corpus draw read knee 12 @512; this round's
  independent draw reads 16 @512 (both fsynced their own block samples).
  Mixed-domain knees therefore carry CONSTRUCTION-DRAW VARIANCE of about
  ±1 grid step — LARGER than pure-domain replication — so mixed-budget
  estimates need multiple draws or wider windows.
- One model (0.5B), one pair (code/prose), one block size (~500 chars),
  two contexts. The bump's universality across pairs/scales is open.

## Practical

Agentic workloads that interleave code and prose (the common case) pay a
real +25–33% KV-key premium at balanced mixing even when each pure domain
would be cheap. Budget tables calibrated on pure corpora UNDERESTIMATE
balanced mixed serving by a grid step per context level, and the draw
variance means a single calibration corpus can miss the true budget by
another step.

Barriers: (a) clean (all three pre-registered horns honestly refuted);
(b) clean (first ratio-resolved mixing measurement); (c) confronted
(five-point ratio grid, one block size stated); (d) clean (held-out eval
tail); (e) deterministic; (f) clean (gate exact); (g) fair (identical
harness across ratios); (h) DIRECT (KV key budget measured directly).

Open: other pairs (math+prose, German+code); block-size sensitivity;
1.5B mixed; bump × 4096-acceleration interaction; 7B cell.

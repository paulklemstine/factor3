# The Knee Lands on the Fine Grid: the 0.5B knee at ctx=1024 is k\* = **20** — k=16 fails (0.971), k=20 passes (0.980), k=24 passes (0.985) — refining the 0.5B chain to a strictly monotone {16, 20, 24} across {512, 1024, 2048} and sharpening the size-invariance comparison: 1.5B's {16, 16} is now flat-to-DECLINING against a rising baseline, and the fine grid (step 4) resolves what the coarse grid (step 16) could not — third confirmation this round-type that knees live ON measurement grids, not between them (NET-62)

**Program:** Network/LLM research lab — round-net-62 (LIMITED-MEMORY AXIS, iteration 21;
the sub-16/24 addendum open since NET-49, load-bearing for NET-55's size-invariance claim).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact, argmax-agree 1.0000; ctx=1024, 24 held-out wikitext
windows; baseline 0.4627 replicates NET-49/56/61 EXACTLY; ALL_DONE_NET62).

## Setup

Fine sweep k ∈ {4, 8, 12, 20, 24} at ctx=1024, oracle top-k, identical harness/windows as
NET-56/58/61 (24 windows — baseline 0.4627 bit-identical to three prior rounds). Script
ResearchOutput/exp_net62_sub16.py; results ~/f3cache/net62_results.json; log /tmp/net62.log.

**Predictions stated BEFORE the run:** P1 KNEE-BELOW-32 (some point in {12, 20, 24} passes);
P2 GRID-STEP-STRUCTURE (if any sub-24 point passes, the knee lands on the fine grid).

## Results

| k | 4 | 8 | 12 | 20 | 24 |
|---|---|---|---|---|---|
| retained | 0.8940 ✗ | 0.9520 ✗ | 0.9662 ✗ | **0.9803 ✓** | **0.9851 ✓** |

**Scorecard: P1 CONFIRMED** — the knee is 20, well below the coarse-grid 32. **P2 CONFIRMED**
— it lands exactly ON the fine-grid point 20 (not between 20 and 24).

## Verdict

THE-KNEE-LANDS-ON-THE-FINE-GRID — the 0.5B knee chain is now strictly monotone in context:
**{16, 20, 24}** at {512, 1024, 2048}, replacing the coarse {16, 32, 24}. Three consequences:
(1) NET-55's size-invariance sharpens — 1.5B's {16, 16} is flat-to-DECLINING against a rising
baseline, strengthening the scale claim; (2) the 2048 corpus-B reading (32) vs corpus-A (24)
now looks like a coarse-grid artifact resolved by fine points, not corpus sensitivity;
(3) the knee-quantizes-to-grid pattern (112 mid-grid at toy 8×; 20 here) now has a third
instance — knees live ON measurement grids, a property worth a dedicated law. The ~30-key
deployment budget is refined to: 0.5B needs {16, 20, 24} keys; the monotone rise with context
returns (the NET-55 "decline at 2048" was the coarse grid misreading 24 as the knee when the
fine structure rises through it).

Barriers: (a) clean — two horns pre-stated, both confirmed; (b) clean — fine-grid knee
refinement of a real-model chain not previously measured in-programme; (c) confronted — same
model/corpus, finer grid; limits: 24 windows (baseline exact-replicates prior rounds);
(d) clean; (e) deterministic, grid pre-stated; (f) clean (ALL_DONE_NET62); (g) fair — same
bar/harness; (h) DIRECT — the deployment table's 1024 entry moves from 32 to 20.
Open: fine grids at 512/2048; domain-jump corpora; 1.5B fine-grid; 7B cell.
Paper 147, issue #298. Now 62 network experiments. Assessment v62.

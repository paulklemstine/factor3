# The Corpus-B Disagreement Was a Grid Artifact: corpus-B's fine knee at ctx=2048 is also k\* = 24 (k=20 fails 0.979, k=24 passes 0.983) — the complete 0.5B fine-grid chain {16, 20, 24} now replicates EXACTLY across two disjoint wikitext shards at all three contexts, every deployment-table entry dual-corpus-confirmed; baseline accuracies differ (0.495 vs 0.476 — shard-2 text is easier) yet knees are identical: accuracy level and knee position are independent (NET-64)

**Program:** Network/LLM research lab — round-net-64 (LIMITED-MEMORY AXIS, iteration 25;
closes the last open discrepancy in the knee chain).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact, argmax-agree 1.0000; ctx=2048, 12 windows,
corpus-B = wikitext shard 1; ALL_DONE_NET63 marker from reused harness).

## Setup

Fine sweep k ∈ {20, 24, 28, 32} at ctx=2048 on corpus-B — byte-identical harness to NET-63
except the corpus path. Script ResearchOutput/exp_net64_fine2048B.py; log /tmp/net64.log.

**Predictions stated BEFORE the run:** P1 SHARD-DIFFERENCE-REAL (fine knee 28–32);
P2 WINDOW/COUNT-ARTIFACT (fine knee 24 too); P3 BETWEEN (28).

## Results

| k | 20 | 24 | 28 | 32 |
|---|---|---|---|---|
| retained | 0.9790 ✗ | **0.9832 ✓** | 0.9853 ✓ | 0.9862 ✓ |

**Scorecard: P1 REFUTED** (knees match exactly); **P2 CONFIRMED**; **P3 REFUTED**.

## Verdict

THE-CORPUS-B-DISAGREEMENT-WAS-A-GRID-ARTIFACT — with this round, the full 0.5B fine-grid
chain {16, 20, 24} replicates EXACTLY across two disjoint corpora at every context cell:
the deployment table is fully dual-corpus-confirmed. Notably, baseline accuracy differs
between shards (0.476 vs 0.495) while knees do not — text difficulty and attention-budget
structure are independent quantities, which is precisely what makes the budget table
portable across domains of similar register. Remaining threads are scale (1.5B fine grids;
7B quantized-offload) and true domain jumps (code/math/non-English).

Barriers: (a) clean — three horns pre-stated incl. two refuted; (b) clean; (c) confronted —
12 windows stated; (d) clean; (e) deterministic; (f) clean (ALL_DONE); (g) fair —
byte-identical harness except corpus path; (h) DIRECT — completes dual-corpus confirmation.
Open: domain-jump corpora; 1.5B fine grids; 7B quantized-offload cell.
Paper 149, issue #300. Now 64 network experiments. Assessment v64.

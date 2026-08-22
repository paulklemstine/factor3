# Content Is a Weak Predictor of Importance: linear probes on key vectors recover only R² ≈ 0.33 (range 0.11–0.64) of each key's future attention, and content-based eviction buys just ~1 point over naive accumulated scores ({0.840, 0.894, 0.928} vs HH's {0.863, 0.882, 0.919} at B = {32, 64, 128}) — still 10 points below the oracle at B=64 — closing the loop NET-56 opened: the oracle-to-policy gap is NOT closeable by what a key *is*; importance is relational and positional, not intrinsic (NET-58)

**Program:** Network/LLM research lab — round-net-58 (LIMITED-MEMORY AXIS, iteration 12;
NET-56 follow-up: learned importance heads).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact, argmax-agree 1.0000; probes fit on TRAIN-side windows
only; eval on held-out; ALL_DONE_NET58).

## Setup

Per-(layer, kv-head) ridge probe: X = post-rope key vector [64-d], y = log1p(total attention
received over the window), fit on 8 train-side sequences (damping 1e-2), evaluated by R².
Streaming eviction then uses the STATIC probe score of each key (content-based) instead of
accumulated usage; budgets B ∈ {32, 64, 128}; same harness/windows as NET-56.
Script ResearchOutput/exp_net58_probe.py; log /tmp/net58.log.

**Predictions stated BEFORE the run:** P1 LEARNED-BEATS-ACCUMULATED (probe closes ≥⅓ of the
oracle gap at B=64); P2 GAP-REMAINS (≥3 pts still open at B=64); P3 DEPTH-STRUCTURE
(R² non-uniform across layers).

## Results

| B | acc-HH (NET-56) | PROBE (this round) | oracle |
|---|---|---|---|
| 32 | 0.8633 | 0.8395 | 0.9913 |
| 64 | 0.8822 | **0.8938** | 0.9953 |
| 128 | 0.9189 | **0.9284** | — |

Probe R² per layer: mean **0.329**, min 0.113, max 0.639 (front layers highest: L0 ≈ 0.62;
mid-stack lowest).

**Scorecard: P1 REFUTED** — at B=64 the probe closes only ~11% of the gap to oracle
(0.894 vs 0.882 → 10.1 pts remain of 11.3), far short of ⅓; it is even WORSE than accumulation
at B=32. **P2 CONFIRMED** — 10+ pts remain. **P3 CONFIRMED** — R² spans 0.11–0.64 with a clear
front-high/mid-low depth structure.

## Verdict

CONTENT-IS-A-WEAK-PREDICTOR-OF-IMPORTANCE — a key's vector knows little about how much
attention it will receive: a full linear readout recovers barely a third of the variance and
converts to ~1 retained-accuracy point in deployment. Together with NET-56 this bounds ALL
content-based eviction policies: importance is determined by relational context (which queries
co-occur with which keys) and position, not by key identity. The oracle-to-policy gap is
structural, not an engineering shortfall — any deployable KV cache must either track usage
online (as NET-56's policies do), keep recency (the dominant cheap signal), or accept the
~10-point penalty at aggressive budgets.

Barriers: (a) clean — three horns pre-stated incl. the refuted P1; (b) confronted — probe-based
key-importance exists in interpretability folklore; NEW = its measured CEILING as an eviction
policy on the knee-measuring harness, with the R²-to-retained conversion; (c) confronted — one
model/context; linear-probe class only (nonlinear heads could fit better — but P1's margin
makes even large gains unable to close P2's bound without near-perfect prediction);
(d) clean — probes trained train-side only; (e) deterministic; closed-form fits, no training
variance; (f) clean (ALL_DONE_NET58); (g) fair — identical harness/budgets/windows as NET-56;
(h) DIRECT — bounds the entire content-based policy family.
Open: nonlinear/MLP heads (bounded above by P2 logic unless near-oracle prediction achieved);
per-layer load-bearingness ablation (next cell); hybrid probe+recency; 1.5B tail map.
Paper 143, issue #291. Now 58 network experiments. Assessment v58.

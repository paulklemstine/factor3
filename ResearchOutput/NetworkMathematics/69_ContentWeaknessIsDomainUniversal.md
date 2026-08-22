# Content Weakness Is Domain-Universal: on Python source — the strongest candidate for content-based importance — linear probes recover only R² = 0.3185 (vs prose's 0.329), probe-only eviction LOSES to accumulated usage by 12 points (0.815 vs 0.934 at B=64), and the hybrid is non-degrading (+0.3 pts, contrasting prose's monotone harm) — importance is relational in structured domains too; content information is neutral-at-best even where syntax repeats (NET-69)

**Program:** Network/LLM research lab — round-net-69 (LIMITED-MEMORY AXIS, iteration 35;
NET-58/61 follow-up on the code domain).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact, argmax-agree 1.0000; probes train-side on code;
identical harness/windows/budgets as NET-58/61; ALL_DONE_NET69).

## Setup

Same methodology as NET-58/61, corpus swapped to Python source: per-(layer, kv-head) ridge
probes fit train-side; streaming arms at B=64 {accumulated-HH, probe-only, hybrid λ=1}.
Script ResearchOutput/exp_net69_probe_code.py; results ~/f3cache/net69_results.json;
log /tmp/net69.log.

**Predictions stated BEFORE the run:** P1 STRUCTURE-MAKES-CONTENT-PREDICTIVE (R² ≥ 0.5 AND
probe beats HH by ≥1 pt); P2 WEAK-PROBE-UNIVERSAL (R² ≤ 0.45 AND probe ≤ accumulated);
P3 HYBRID-NON-DEGRADING on code.

## Results

| arm | retained @B=64 |
|---|---|
| accumulated-HH | 0.9340 |
| probe-only | **0.8149** |
| hybrid λ=1 | 0.9371 |

Probe R² on code: mean **0.3185** (min 0.1225, max 0.5921) vs prose mean 0.329.

**Scorecard: P1 REFUTED decisively** — R² statistically identical to prose and probe-only
LOSES by 12 pts. **P2 CONFIRMED on both clauses.** **P3 CONFIRMED** — +0.3 pts for the
hybrid on code (vs prose's −0.4-to-−4 degradation): structure makes content NEUTRAL rather
than harmful, but nowhere near helpful.

## Verdict

CONTENT-WEAKNESS-IS-DOMAIN-UNIVERSAL — the NET-58 conclusion survives its strongest
challenge: even in a domain with repeating identifiers and rigid syntax, a key's vector
carries almost no information about its future reception. The domain difference that DOES
exist is in the interaction term: adding content to usage is harmful on prose but neutral
on code (hybrid +0.3 here vs monotone degradation there) — consistent with code's
repetitiveness making the probe's errors less damaging rather than its signal stronger.
With NET-68's knee result, the complete code-domain picture: fewer keys needed (12/16),
content useless for choosing them, recency+accumulation still the deployable pair.

Barriers: (a) clean — three horns pre-stated incl. the refuted P1; (b) clean — first
cross-domain probe comparison; (c) confronted — one code language/repo stated; (d) clean —
train-side fits; (e) deterministic; (f) clean (ALL_DONE_NET69); (g) fair — identical
methodology/budgets as NET-58/61; (h) DIRECT — closes content-based eviction across both
major serving domains.
Open: math/non-English domains; learned ONLINE predictors; increments@4096; 7B cell.
Paper 154, issue #309. Now 69 network experiments. Assessment v69.

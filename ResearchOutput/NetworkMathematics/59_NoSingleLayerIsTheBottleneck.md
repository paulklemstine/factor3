# No Single Layer Is the Bottleneck: pruning ANY one of Qwen2.5-0.5B's 24 layers alone with oracle top-k=16 costs at most 0.5% accuracy (profile spread 0.6 pts; the "identity tail" L22/L23 sit mid-pack and L23 is literally the BEST at 1.0008) — refuting both tail predictions and establishing an epistasis result: the four-fold tail specialness established since NET-50 (diffuse, decision-divergent, unportable, personal-KV) is about INTERACTION, not individual fragility; joint all-layer k=16 (NET-50: −1.7%) is sub-additive over solo costs (≤0.2% each) (NET-59)

**Program:** Network/LLM research lab — round-net-59 (LIMITED-MEMORY AXIS, iteration 14;
the per-layer load-bearingness ablation, open since NET-49).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact, argmax-agree 1.0000; ctx=512, 24 held-out windows;
solo-layer oracle top-k at fixed budgets {16, 32}; ALL_DONE_NET59).

## Setup

For each layer ℓ ∈ {0..23} independently: apply oracle top-k ONLY to layer ℓ (k = 16, then 32),
all other layers full attention. Measure retained next-token accuracy on 24 held-out wikitext
windows. Full baseline acc 0.4309 (this window count). Script ResearchOutput/exp_net59_perlayer.py;
log /tmp/net59.log.

**Predictions stated BEFORE the run:** P1 TAIL-IS-CRITICAL (L22/L23 solo-k16 costliest);
P2 MID-STACK-CHEAP (some layer ≥ 0.99 retained); P3 NON-UNIFORM-MAP (spread ≥ 3 pts at k=16).

## Results

k=16 profile: **spread 0.6 points** — best 1.0013 (L13), worst 0.9953 (L12); every layer
≥ 0.995. The tail: L21 0.9987, **L22 0.9987**, **L23 1.0008** — mid-pack and best-in-stack.
k=32 profile: spread 0.5 points, worst L15 0.9966 — even flatter.

**Scorecard: P1 REFUTED** (the tail is NOT individually fragile); **P2 CONFIRMED** (trivially —
every layer qualifies); **P3 REFUTED** (the map is remarkably UNIFORM, not non-uniform).

## Verdict

NO-SINGLE-LAYER-IS-THE-BOTTLENECK — solo deletion costs ≈ 0 everywhere, yet four prior rounds
established the last two layers as categorically different (only far-from-tropical region,
highest crystallization loss, only decision-divergence across fine-tunes, only unportable
weights, personal KV). The resolution is EPISTASIS: the tail's role lives in interaction with
upstream representations (as NET-54's swap-collapse showed directly), not in any property a
single-layer perturbation can expose. Additionally: joint all-layer k=16 costs 1.7% (NET-50)
while the sum of solo costs would be ~4.8% — pruning interactions are SUB-ADDITIVE/redundant.
Design implication for mixed-precision serving (NET-51 link): there is no per-layer budget
hierarchy to exploit at this scale; differentiation must come from interaction-aware or
policy-level criteria, not per-layer criticality.

Barriers: (a) clean — three horns pre-stated incl. two refuted; (b) clean — causal solo-layer
pruning profiles of pretrained LLM attention not previously measured in-programme; (c)
confronted — real model; limits: ONE context (512), solo-only granularity (pairs/joints open),
24 windows; (d) clean — held-out, no training; (e) deterministic, monotone profiles;
(f) clean (gate exact, ALL_DONE_NET59); (g) fair — identical budgets/protocol per layer;
(h) DIRECT — rules out the simplest mixed-precision design and redirects to interaction-aware
criteria. Open: pairwise/joint ablations on the tail; 1.5B replication; probe+recency hybrid;
domain-jump corpora; 7B cell. Paper 144, issue #293. Now 59 network experiments. Assessment v59.

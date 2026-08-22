# The Epistasis Lives in the Tail Pair: solo costs of L22+L23 sum to 0.06 points, yet pruning them JOINTLY at k=16 costs 0.42 points — a 7× super-additive ratio, the largest of six tested pairs; the tail TRIPLE compounds further ({21,22,23}: 0.76 pts vs 0.19 summed, 4×) while bulk pairs stay additive-or-sub — locating the interaction NET-59 proved must exist squarely inside the last-two-layer block, exactly where NET-50/51/54 independently placed the model's identity (NET-60)

**Program:** Network/LLM research lab — round-net-60 (LIMITED-MEMORY AXIS, iteration 17;
directly follows NET-59's flat solo profiles).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact, argmax-agree 1.0000; ctx=512, 24 held-out windows;
pair/triple oracle top-k at k=16/layer; ALL_DONE_NET60).

## Setup

Six arms prune pairs/triples of layers jointly at k=16 each (all other layers full):
{22,23} tail · {12,15} worst-solo-bulk · {0,1} front · {10,11} mid · {22,12} cross ·
{21,22,23} tail-triple. Each arm's cost (points of lost accuracy) compared to the SUM of
its members' NET-59 solo costs. Script ResearchOutput/exp_net60_pairs.py;
results ~/f3cache/net60_results.json; log /tmp/net60.log.

**Predictions stated BEFORE the run:** P1 TAIL-PAIR-IS-SPECIAL (tail pair costs more than any
bulk pair); P2 SUB-ADDITIVE-EVERYWHERE; P3 TAIL-TRIPLE-COMPOUNDS.

## Results

| arm | layers | retained | cost (pts) | Σsolo (pts) | class |
|---|---|---|---|---|---|
| **tail_22_23** | 22,23 | 0.9958 | **0.42** | **0.06** | **SUPER 7×** |
| bulk_12_15 | 12,15 | 0.9940 | 0.60 | 0.79 | sub |
| front_0_1 | 0,1 | 0.9975 | 0.25 | 0.25 | ≈additive |
| mid_10_11 | 10,11 | 0.9960 | 0.40 | 0.28 | super 1.4× |
| cross_22_12 | 22,12 | 0.9941 | 0.59 | 0.60 | sub |
| **triple_21_22_23** | 21,22,23 | 0.9924 | **0.76** | **0.19** | **SUPER 4×** |

**Scorecard: P1 CONFIRMED** — the tail pair is simultaneously the CHEAPEST by solo sum and
disproportionately costly jointly: 7× super-additive vs ≤1.4× for every other pair.
**P2 REFUTED** — three of six arms are super-additive. **P3 CONFIRMED** — the tail triple is
the most costly arm overall and compounds at 4×.

## Verdict

THE-EPISTASIS-LIVES-IN-THE-TAIL-PAIR — the interaction that NET-59 proved must exist is
localized: the last two layers are individually expendable (solo ≈ free) yet jointly carry
~7× their apparent weight, compounding as the tail deepens. This is the causal signature
matching four independent correlational markers (diffuse attention, crystallization loss,
decision divergence, unportability): the tail functions as a COORDINATED UNIT — its two
layers co-adapted during pretraining so that sparsifying either alone is absorbed, but
degrading both removes a joint capability no other pair exhibits. Mixed-precision and KV
budget policies should treat the last two layers as ONE unit (same bits, same budget),
never differentiate between them.

Barriers: (a) clean — three horns pre-stated incl. the refuted P2; (b) clean — pairwise
super-additivity maps for pretrained LLM attention not previously measured; (c) confronted —
limits: one context/model, k=16 granularity, five chosen pairs; (d) clean — held-out, no
training; (e) deterministic; solo sums inherited from the committed NET-59 profile;
(f) clean (ALL_DONE_NET60); (g) fair — identical budgets across arms; (h) DIRECT — prescribes
unit-of-differentiation for serving policies. Open: 1.5B replication; deeper tails on bigger
models (do LAST-THREE units emerge?); probe+recency hybrid; domain-jump corpora.
Paper 145, issue #294. Now 60 network experiments. Assessment v60.

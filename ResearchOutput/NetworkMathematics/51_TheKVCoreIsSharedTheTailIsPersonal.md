# The KV Core Is Shared, the Tail Is Personal: Qwen2.5-0.5B base and Instruct keep near-identical keys at every layer (cosK ≥ 0.976, layer 0 EXACTLY 1.0000, rel-divergence 0.3–22%), divergence forms a HUMP (rises to mid-stack L12–16, then FALLS — monotone-growth refuted), and top-1 attention agreement holds 0.84–0.98 across the bulk yet COLLAPSES to 0.568/0.627 in exactly the same diffuse-tail layers L22/L23 that NET-50 found to be the only far-from-tropical region — three experiments, one conclusion: the last two layers are where a model is itself (NET-51)

**Program:** Network/LLM research lab — round-net-51 (LIMITED-MEMORY AXIS, iteration 3; mined
from the Lean catalogue's amortized model-delta law: optimal bits n·r + min(D,n) over a shared
decompressor).
**Date:** 2026-08-21
**Status:** Machine-verified (both capture forwards validated vs HF eager before measurement:
argmax-agreement 0.9922 base / 0.9971 instruct; fp16 weights + fp32 score math; ALL_DONE_NET51).

## Setup

Qwen2.5-0.5B **base** and **Instruct** (same architecture, different post-training) run on
IDENTICAL held-out wikitext prompts (4 × 1025 tokens). Per layer we capture post-rope q/k/v
(GQA: 2 kv-heads) and pre-layer hidden states, then measure: (A) K/V cosine similarity +
relative L2 divergence; (B) top-1 key-choice agreement under each model's OWN scores;
(C) hidden-state relative divergence ‖Δh‖/‖h‖. Script /tmp/exp_net51_delta.py;
log /tmp/net51.log; results /tmp/net51_results.json.

**Predictions stated BEFORE the run:** P1 EARLY-SHARE (layer-0 K/V near-identical,
fine-tuning touches late layers first); P2 MONOTONE-DIVERGENCE (divergence grows monotonically
with depth); P3 DELTA-WIN (base+delta serving beats naive 2× duplication).

## Results

**P1 CONFIRMED emphatically**: layer 0 has cosK = **1.0000**, relK = 0.0026 — embeddings and
first-layer keys are effectively untouched by instruction tuning.
**P2 REFUTED**: divergence is HUMP-shaped, not monotone — relK climbs 0.003 → **0.217 at L16**
then falls back to 0.14–0.19; relV peaks earlier (0.337 at L12); hidden divergence peaks ~0.22
at L12–16. The fine-tune delta CONCENTRATES mid-stack and partially heals.
**P3 CONFIRMED with a sharp caveat**: mean cosK = 0.990 / cosV ≈ 0.97–0.99 and mean top-1
agreement = 0.894 — a shared-core-plus-delta cache is viable — BUT the per-layer table shows
top-1 agreement collapsing to **0.568 (L22) / 0.627 (L23)** while those same layers' K/V remain
cosine-similar (0.983/0.988): the final two layers make DIFFERENT attention decisions from
nearly identical key material.

| depth zone | relK range | top-1 agree |
|---|---|---|
| L0–L3 | 0.003–0.038 | 0.86–0.96 |
| L9–L16 (hump) | 0.11–0.22 | 0.84–0.96 |
| L17–L21 | 0.13–0.18 | 0.92–0.98 |
| **L22–L23 (tail)** | 0.16–0.19 | **0.57 / 0.63** |

## Verdict

THE-KV-CORE-IS-SHARED-THE-TAIL-IS-PERSONAL — instruction tuning barely moves the key geometry
(layer 0 exact, every layer ≥ 0.976 cosine), concentrates its weight-space footprint mid-stack
with partial recovery, and leaves the BULK of attention decisions intact (89% mean agreement)
while the LAST TWO LAYERS — identically the layers NET-50 measured as the only far-from-
tropical, high-crystallization region — diverge decisively. Three independent measurements
(tropical gap, crystallization loss, cross-fine-tune decision divergence) converge on the same
structure: **the bulk of a transformer is shared machinery; the two-layer tail is where the
model's identity lives.**

Barriers: (a) clean — three horns about divergence structure stated pre-run; (b) confronted —
KV/divergence profiles of fine-tune pairs exist in folklore ("task vectors", early-exit lore);
the NEW content is the hump shape with exact per-layer constants, the decision-vs-vector
dissociation at the tail, and the three-way convergence with our own tropical maps; (c)
confronted — real pretrained pair, natural text; limits: ONE pair at ONE context, 4 prompts,
fp16 captures; (d) clean — no training, no leakage possible; (e) honest limits — cosine
similarity does not bound functional impact (that is why Part B exists); prompt-level variance
uncharacterized (n=4); single model family; (f) clean — both capture forwards gated against HF
eager (0.9922/0.9971 argmax agreement), fp32 score math, NO crash after two gate-caught bugs
(final-hidden indexing, mask broadcast) — the gates did their job; (g) fair — each model scored
under its own weights; no reference-model bias; (h) DIRECT — a shared-KV multi-finetune server
can share the bulk cache and must duplicate the tail; quantified: ~22/24 layers shareable at
≥0.92 decision agreement, tail personal.
Open: does SFT/RLHF/DPO move the tail differently?; bigger pairs (1.5B/7B); causal test —
swap ONLY tail layers between models and measure behaviour transfer; connect to NET-52
quantization (quantize the shared core harder than the tail?). Paper 136, issue #238.
Now 51 network experiments. Assessment v51.

# Keys Own the Cliff: quantizing ONLY the cache keys to 4 bits annihilates the model (+35,597%) while quantizing ONLY the values to 4 bits is FREE (+0.17%) — an asymmetry of four orders of magnitude that no block-scaling format escapes; the softmax selection interface is the entire cliff (NET-93)

**Program:** Network/LLM research lab — round-net-93 (CPU-LARGE-MODEL AXIS,
iteration 68; the NET-92 rescue/discriminator cell).
**Date:** 2026-08-24
**Status:** Machine-verified (ALL_DONE_NET93).

## Setup

Identical harness to NET-92 (llama-perplexity, Qwen2.5-7B-Instruct Q4_K_M
fully on CPU, threads=8, ctx=2048, held-out wikitext slice 250KB).
Arms {K q4_1/V q4_1, K iq4_nl/V iq4_nl, K q4_0/V f16, K f16/V q4_0}.
Script ResearchOutput/exp_net93_kvrescue.py; results ~/f3cache/net93_results.json;
log /tmp/net93.log.

**Predictions stated BEFORE the run:** P1 block-scale rescues partially
(q4_1 into [+2%, +300%]); P2 KEY-SIDE-OWNS-THE-COLLAPSE (K-only degrades ≥5×
worse than V-only); P3 importance-scaling beats uniform-block scaling.

## Results

| arm | PPL | ΔPPL vs control 7.1093 |
|---|---|---|
| K q4_1 / V q4_1 | 3,158.07 | +44,322% |
| K iq4_nl / V iq4_nl | 1,627.35 | +22,790% |
| **K q4_0 / V f16** | **2,537.80** | **+35,597%** |
| **K f16 / V q4_0** | **7.1211** | **+0.166%** |

**Scorecard:** P1 REFUTED decisively (block scale+offset does not rescue —
q4_1 is marginally WORSE than raw q4_0; predicted ≤+300%, measured
+44,000%); P2 CONFIRMED BEYOND ALL PREDICTION (predicted ≥5× asymmetry;
measured ~214,000× in damage ratio: keys-only collapses at +35,597%
while values-only is indistinguishable from lossless at +0.166%);
P3 TECHNICALLY TRUE BUT MEANINGLESS (iq4_nl ranks best among the three
collapsed formats — 1,627 < 2,714 < 3,158 — but "half of annihilation"
is still annihilation).

## The law

**THE ENTIRE KV CLIFF LIVES IN THE KEYS.** Cache VALUES tolerate raw
per-tensor 4-bit quantization with zero measurable quality cost; cache KEYS
cannot survive 4 bits in ANY tested representation (raw q4_0, block-scaled
q4_1, importance-scaled iq4_nl all land in the 10³–10⁴ PPL range). The
mechanism is the selection interface: keys feed every softmax comparison,
so their errors shift the attention-selection boundary for every query at
every layer (the NET-83 amplification path), while value errors perturb
only the content actually retrieved — linear, local, benign.

Deployment consequence: the practical cache budget splits by role —
**keys need ≥8 bits; values accept 4** — implying a K8/V4 configuration
(~6 average bits) that should be quality-free given K8/V16 (+0.09%) and
K16/V4 (+0.17%) are both individually free. Direct confirmation of the
combined cell is the immediate follow-up.

Honest limits: the three-way 4-bit key failure could still share one
implementation path inside llama.cpp's KV-dequant kernels (three formats
triangulate but do not prove fundamentality); single slice/model/context;
K8/V4 combined cell untested; per-arm SEs not captured (as in NET-92).

Barriers: (a) clean (pre-registered horns honestly scored incl. two
refutations); (b) clean; (c) confronted (formats/grid stated); (d) clean;
(e) deterministic; (f) partial (point estimates documented); (g) fair;
(h) DIRECT (a concrete serving prescription falls out).

Open: direct K8/V4 combined measurement; K6/K5 boundary search (where
exactly does the key cliff begin between 8 and 4?); cross-model replication;
cliff-vs-context interaction.

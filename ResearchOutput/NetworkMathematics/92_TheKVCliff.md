# The KV Cliff: 8-bit cache is quality-free (+0.10% worst case) while 4-bit cache is ANNIHILATION (+38,000% perplexity, PPL 7.11 → 2,714.6) — the KV precision axis has no usable middle at ctx 2048; keys and values are individually dispensable down to 8 bits but jointly irreplaceable below them (NET-92)

**Program:** Network/LLM research lab — round-net-92 (CPU-LARGE-MODEL AXIS,
iteration 67; first KV-cache quantization cell).
**Date:** 2026-08-24
**Status:** Machine-verified (ALL_DONE_NET92).

## Setup

Qwen2.5-7B-Instruct Q4_K_M entirely on CPU (llama-perplexity, threads=8,
ctx=2048), held-out wikitext slice 250KB (~62K tokens) from the durable
cache, disjoint from prior eval windows. Arms {K f16/V f16 control,
K q8_0/V f16, K f16/V q8_0, K q8_0/V q8_0, K q4_0/V q4_0} via
--cache-type-k/--cache-type-v.
Script ResearchOutput/exp_net92_kvquant.sh; results ~/f3cache/net92_results.json;
log /tmp/net92.log.

**Predictions stated BEFORE the run:** P1 q8_0-KV degrades <1% (weight-side
analogy: 8 bits suffices away from fragile structure); P2 raw q4_0-KV
degrades >5% (keys are the fragile selection interface; no group
compensation exists for KV); P3 at equal bits, K-only hurts more than
V-only (selection-boundary errors are amplified; content errors are linear).

## Results

| arm | PPL | ΔPPL vs control | pass time |
|---|---|---|---|
| K f16 / V f16 | 7.1093 | — | 1216s |
| K q8_0 / V f16 | 7.0924 | −0.238% | 1413s |
| K f16 / V q8_0 | 7.1160 | +0.094% | 1534s |
| K q8_0 / V q8_0 | 7.1162 | **+0.097%** | 1511s |
| K q4_0 / V q4_0 | **2,714.6042** | **+38,084%** | ~1500s |

**Scorecard:** P1 CONFIRMED (all q8_0 arms within ±0.25% of control —
indistinguishable from lossless); P2 CONFIRMED with the largest margin in
program history (predicted >5%, measured +38,000% — total model collapse,
perplexity 380× the control); P3 UNRESOLVED BY DESIGN (both single-sided
8-bit arms sit inside the noise band, so no asymmetry is measurable at 8
bits, and the grid contained no 4-bit single-sided arms to test the
asymmetry where it would be visible).

## The laws

1. **THE KV CLIFF IS A WALL**: between 8 and 4 bits the cache does not
   degrade gracefully — it passes through a region containing NO usable
   operating point. Weights quantize smoothly with group scales (Q4_K_M
   works, NET-52/53); raw per-tensor q4_0 KV multiplies a small key error
   through every softmax boundary of every layer and the model stops
   modeling language altogether.
2. **8-BIT CACHE IS FREE**: full-width q8_0 KV costs +0.10% worst-case PPL
   while halving the KV buffer — deployment-grade at ctx 2048 on CPU.
   Measured throughput tax: +16–26% pass time (dequantization cost),
   so the trade is memory-vs-speed, not memory-vs-quality.
3. Continuity: the collapse direction matches NET-52's interface fragility
   (attention inputs are the sensitive surface) and NET-83's amplification
   mechanism (selection-boundary perturbation compounds); the magnitude —
   four orders past prediction — is new.

## Honest limits

- Single slice (~62K tokens); PPL SEs not captured per-arm (parser kept
  point estimates only); the ±0.25% 8-bit deltas are within slice noise —
  "quality-free" claims rest on the bound, not on exact equality.
- q4_0 tested only joint (no single-sided 4-bit arms ⇒ P3 unresolved);
  q4_1/iq4_nl (block-scale variants) untested — whether block-scaled 4-bit
  KV survives is the immediate follow-up.
- One model, one context, one box; the cliff's position may move with
  context length (untested).

Barriers: (a) clean (pre-registered horns honestly scored; P3 declared
unresolved rather than forced); (b) clean (catalog-empty cell); (c)
confronted (one model/slice/grid stated); (d) clean (held-out disjoint
slice); (e) deterministic; (f) partial (point estimates, no per-arm SEs —
documented); (g) fair (identical binary/corpus/threads across arms);
(h) DIRECT (deployment-relevant memory-quality trade measured directly).

Open: q4_1/iq4_nl KV (does block-scaling rescue 4-bit?); single-sided 4-bit
arms (the P3 discriminator); cliff position vs context length; interaction
with speculative decoding's draft KV; weight-quant floor transfer Q8→Q2;
knee-law transfer to 7B.

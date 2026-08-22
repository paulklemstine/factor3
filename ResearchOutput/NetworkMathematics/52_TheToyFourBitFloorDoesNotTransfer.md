# The Toy Four-Bit Floor Does Not Transfer: on pretrained Qwen2.5-0.5B, naive per-channel RTN costs +0.0044 / +0.035 / +0.128 / **+0.79** / +9.23 / +14.06 CE at 8/6/5/**4/3/2** bits — the 4-bit "optimum" measured on from-scratch toys is REFUTED on a real LM; group-128 halves the damage (+0.32 at 4-bit, survival at 3-bit where per-channel dies), the depth gradient confirms weakly (last-12 worse than first-12: retained 0.863 vs 0.890), and mesh-monotonicity holds exactly as the catalogue's sharpness theorem demands — even 8-bit is measurably nonzero (NET-52)

**Program:** Network/LLM research lab — round-net-52 (LIMITED-MEMORY AXIS, iteration 4; mined
from the Lean catalogue's quantized-lattice convexity-transfer theorem: defect ≤ 2Lr, constant
sharp, no exact convexity at any positive mesh).
**Date:** 2026-08-21
**Status:** Machine-verified (identical eval harness/gates as NET-49–51 via the shared validated
Runner; full baseline reproduced exactly 0.4460/2.8697; ALL_DONE_NET52, no crash).

## Setup

RTN symmetric quantization of ALL linear weights (q/k/v/o/gate/up/down) of Qwen2.5-0.5B,
fp32 master restored between arms; eval = 40 held-out wikitext windows at ctx=512 (same
protocol/bar as the whole axis). Arms: bits ∈ {8,6,5,4,3,2} per-output-channel;
depth split at 4-bit (first-12 vs last-12 layers only); granularity at group-128 (4-bit,
3-bit). Script /tmp/exp_net52_quant.py; log /tmp/net52.log.

**Predictions stated BEFORE the run:** P1 REAL-4-BIT-NEAR-FLOOR (per-channel 4-bit
ΔCE ≤ 0.05 — the toy per-channel-uniform-4 optimum transfers); P2 DEPTH-GRADIENT (last-12
worse than first-12 — toy NET-18's non-depth-robustness); P3 TWO-BIT-COLLAPSE (ΔCE ≥ 0.5);
P4 MONOTONE-MESH (ΔCE monotone in mesh, 8-bit already nonzero — sharpness of the 2Lr band).

## Results

| arm | ΔCE | retained acc |
|---|---|---|
| 8-bit per-ch | +0.0044 | 0.9985 |
| 6-bit per-ch | +0.0353 | 0.9904 |
| 5-bit per-ch | +0.1281 | 0.9620 |
| **4-bit per-ch** | **+0.7879** | **0.7630** |
| 3-bit per-ch | +9.2262 | 0.0367 |
| 2-bit per-ch | +14.0588 | 0.0001 |
| 4-bit first-12 | +0.3885 | 0.8904 |
| 4-bit last-12 | +0.4054 | 0.8635 |
| 4-bit group-128 | +0.3180 | 0.9060 |
| 3-bit group-128 | +2.7220 | 0.3987 |

**Scorecard: P1 REFUTED SPECTACULARLY** — +0.79 against a ≤0.05 prediction: the toy
compression floor (per-channel uniform-4 optimal at 4.00 bits, NET-11/14) was an artifact of
the from-scratch toy setting and does NOT transfer to pretrained weights. **P2 CONFIRMED
weakly** (last-12 +0.41 vs first-12 +0.39; retained 0.863 vs 0.890 — NET-18's deeper-is-worse
direction holds, small margin). **P3 CONFIRMED dramatically** (+14 CE, zero accuracy).
**P4 CONFIRMED** — strictly monotone in bit width with 8-bit measurably nonzero, exactly what
the sharpness theorem predicts.

**The practical cliff structure**: degradation is mild through 5 bits (+0.13), severe at 4
(+0.79), catastrophic at 3 (+9.2) for per-channel RTN; grouping by 128 repairs ~60% of the
4-bit damage and rescues 3-bit from death (+2.72). This is precisely why production quantizers
(GPTQ/AWQ/llama.cpp GGUF) are group-wise — here measured cleanly for the programme.

## Verdict

THE-TOY-FOUR-BIT-FLOOR-DOES-NOT-TRANSFER — barrier (c) (toy-scale) strikes the programme's own
compression-axis conclusion: the most-cited toy number (per-channel 4-bit lossless) fails on a
real LM by 16× its predicted budget. What transfers instead is STRUCTURE: depth gradient
(direction), mesh monotonicity + sharpness (exact), and the grouping lever. For the 6 GB host:
naive RTN below 6 bits is not deployable; group-wise ≥4-bit is the entry point, and any further
compression must come from error-compensation methods (GPTQ-style), not scale choice alone.

Barriers: (a) clean — four horns pre-stated incl. the one refuted; (b) clean — RTN floors on a
real pretrained LM under this protocol not previously measured in-programme (production folklore
says "grouping needed" without this exact constant structure); (c) CONFRONTED AND DECISIVE —
this round IS the transfer test of the compression axis, honestly negative; limits: ONE model,
ctx=512, RTN-only (no GPTQ compensation yet), embeddings/norms unquantized (noted); (d) clean —
held-out data, deterministic; (e) single-seed by construction (deterministic weights); noise
floor: none (bit-exact evals, deltas ≥ 0.0004 resolvable); (f) clean — identical validated
harness, baseline reproduced exactly, ALL_DONE_NET52; (g) fair — same reference/protocol across
all arms; granularity arms compared at matched bit width; (h) DIRECT — the (bits × grouping)
surface is THE deployment table for fitting larger Qwen models into 6 GB VRAM; open cells:
GPTQ/AWQ compensation on top of these floors; weight+KV joint budgets; tail-aware mixed
precision (quantize the shared core harder than the personal tail — NET-51 link).
Paper 137, issue #239. Now 52 network experiments. Assessment v52.

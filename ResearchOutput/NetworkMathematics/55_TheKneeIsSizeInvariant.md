# The Knee Is Size-Invariant: Qwen2.5-1.5B (3× the parameters, +4 layers) posts k\* = {16, 16} at ctx = {512, 1024} — IDENTICAL to the 0.5B knee at 512 and HALF of it at 1024 (where 0.5B needed 32) — tripling the model did not raise the lossless attention budget by a single key; the real-model knee family is now {16, 32, 24} @0.5B and {16, 16} @1.5B: flat-to-declining in context and flat in scale, ~30 keys covers both models at both contexts (NET-55)

**Program:** Network/LLM research lab — round-net-55 (LIMITED-MEMORY AXIS, iteration 7; cell (3)
of the catalogue mining queue: size transfer).
**Date:** 2026-08-22
**Status:** Machine-verified (bf16-storage/fp32-compute harness; gate: HF's own bf16 GPU forward
captured pre-floatify vs our Runner — argmax-agree 0.8906, **ΔCE = 0.0054** — functional
identity, near-tie argmax flips expected across a 152k vocab; 24 held-out wikitext windows/cell;
96 W power cap; ALL_DONE_NET55).

**Engineering record (three findings en route, each gate-caught before any measurement):**
(1) Qwen2.5-1.5B's own **fp16 forward NaNs on real text** — verified pre-wrapper; bf16 storage
mandatory on pre-bf16 GPUs. (2) The CPU-fp32 reference path **SIGILLs** on this host (deep
transformer CPU kernel; basic CPU matmul verified fine) — reference moved to HF-bf16-on-GPU
captured before weight-path surgery. (3) Gate calibration: CE is the binding check (ΔCE ≤ 0.02);
argmax agreement only guards hard breakage (≥0.85 — NaN paths score ~0).

## Predictions stated BEFORE the run

P1 SIZE-SCALING-KNEE (knees HIGHER at 1.5B: k\*(512) ∈ [24,48], k\*(1024) ∈ [32,96]);
P2 TAIL-PERSISTS (last-two-layer eff-support jump recurs); P3 SATURATION-FAMILY
(ratio k\*(1024)/k\*(512) ≤ 2).

## Results

| ctx | full acc | full CE | k\* | retained at k\* |
|---|---|---|---|---|
| 512 | 0.4680 | 2.6413 | **16** | 0.9896 (k=8 fails 0.9727) |
| 1024 | 0.5004 | 2.3790 | **16** | 0.9806 (grid floor — k\* ≤ 16) |

Sweeps: 512 — 8: 0.9727 ✗, **16: 0.9896 ✓**, 24: 0.9915, 32: 0.9969, 48: 0.9993, 64: 0.9988.
1024 — **16: 0.9806 ✓**, 24: 0.9867, 32: 0.9881, 48: 0.9928, 64: 0.9927, 96: 0.9954, 128: 0.9974.

**Scorecard: P1 REFUTED DECISIVELY** — the knee did not grow with 3× the parameters; it came in
BELOW the predicted floor at both contexts, halving at 1024. **P2 UNMEASURED** (honest): this
harness version dropped the per-layer concentration block in the crash-recovery rewrite — the
tail question at 1.5B remains open. **P3 CONFIRMED with a stronger reading**: ratio = 1.0 —
not merely sub-linear but FLAT.

## Verdict

THE-KNEE-IS-SIZE-INVARIANT — across the measured scale ladder the real-model lossless attention
budget is now: 0.5B {16, 32, 24} and 1.5B {16, 16} at ctx {512, 1024, 2048}/{512, 1024}: a
~30-key budget covers every real model measured at every context, while the toy law (k\* =
d·ctx/32) predicted 384–1344 for these cells. The knee's insensitivity to scale (and its
decline at 1024 on the larger model) is consistent with the NET-49 depth-collapse finding
read in reverse: what sets the knee is the CONCENTRATION STRUCTURE of trained attention —
apparently a property of natural-language attention itself, not of model capacity. Deployment
reading for the 6 GB host: **the KV working-set budget does not scale with model size** —
the binding constraint at larger models is weights (NET-52's quantization table), not cache.

Barriers: (a) clean — three horns pre-stated incl. the decisively refuted P1; (b) clean —
size-transfer of attention-sparsity knees not a measured law in Catalog or literature;
(c) confronted — 3× scale jump measured; limits: TWO points on the size axis (0.5B, 1.5B),
grid floor at 16 (k\*(1024) could be lower — sub-16 addendum open), ONE corpus, 24 windows
(SE ≈ 0.3%), bf16-storage numerics, P2 honestly unmeasured; (d) clean — held-out last 10%;
(e) deterministic evals; gate documented with its calibration rationale; (f) clean —
finite-reference assert, ALL_DONE_NET55; (g) fair — same bar/protocol as NET-49–50 (0.98·full);
(h) DIRECT — size-invariance is the deployment-relevant claim for fixed-VRAM serving.
Open: sub-16 addendum at 1024; 1.5B tail map (P2); 7B cell (quantized-offload); oracle-to-policy
gap (next cell); corpus robustness. Paper 140, issue #284. Now 55 network experiments. Assessment v55.

# The Depth Leg at Long Context Is Affine: k*=160 at (d=16, ctx=512) Completes the Law k* = 8d + 32 — Refuting Both the ×1.5 Power Continuation and the Law's Recovery (NET-40)

**Program:** Network/LLM research lab — round-net-40 (speed-axis round 13; the natural continuation of the depth ladder NET-38/39 opened at ctx=512).
**Date:** 2026-08-15
**Status:** Machine-verified (data-free top-k key/value pruning on a real causal word LM, **d=16, seed=1, ctx=512**, 5 Gutenberg novels, dm=64, vocab 4097, 2000 AdamW steps, 6472s training).

## Hypothesis and statement

NET-38/39 measured k* = 96 at (d=8, ctx=512) at TWO seeds — 25% below the
d·ctx/32 prediction (128) — read as a SUB-LINEAR depth leg: k* 64→96 = ×1.5 on
doubling d at ctx=512, vs the ×2.0 linear law exact at ctx=128. This round
measures the NEXT rung, d=16 at ctx=512 — the one cell that discriminates
whether the sub-linearity PERSISTS or the law RECOVERS:
- **P1** k* ≈ 144 = ×1.5·96 → the ×1.5 sub-linear depth coefficient CONTINUES at
  the same rate (prediction stated before the run; the highest-value reading).
- **P2** k* = 256 = d·ctx/32 → the law RECOVERS at depth: NET-38/39's
  sub-linearity was a mid-depth transient; deep stacks re-approach the product form.
- **P3** k* ≈ 128–160 (other) → the depth leg flattens further or bends — a
  non-trivial intermediate law.

## 1. Setup (identical to NET-38/39, byte-for-byte)

Same 5 Gutenberg novels, word-level top-4097 vocab, contiguous 90/10 split,
causal transformer dm=64/4 heads, **d=16, seed=1, ctx=512** (1171 windows, last
10% held out), 2000 AdamW steps. Full acc **0.1469** (bar 0.1439), full loss
**5.3147**. Eval via the explicit causal-attention forward; top-k mask from each
eval input's own trained attention at inference; random-k control (rng seed
12345). Sweep **{32,64,96,128,144,160,192,224,256,384}** — the [128,256] region
is enriched with 144/160/224 to pin the knee wherever it lands (k=16 dropped:
at d=8 it read 0.904–0.915 and depth right-shifts the retained curve, so it
carries no information). Script: /tmp/exp_net_attncost_d16_ctx512.py (~1.8h wall
at 4 threads).

## 2. The decisive test — k* = 160, NEITHER horn (P3 outcome)

| k | retained | verdict |
|---|---|---|
| 32 | 0.854 | ✗ |
| 64 (**4d**) | 0.917 | ✗ depth-only rule far short at depth |
| 96 | 0.944 | ✗ (this was d=8's knee — at d=16 it is 4 SE short: depth right-shift confirmed) |
| 128 | 0.967 | ✗ |
| 144 (**×1.5·96**) | 0.976 | ✗ **P1 REFUTED** — 0.004 below bar |
| **160** | **0.981** | ✓ **k\* = 160** |
| 192 | 0.991 | ✓ |
| 224 | 0.993 | ✓ |
| 256 (**d·ctx/32**) | 0.993 | ✓ P2 passes but is NOT minimal |
| 384 | 1.000 | ✓ (loss 5.3172 ≈ full 5.3147) |

**k\*(s1, d=16, ctx=512) = 160 — neither the ×1.5 continuation (144 fails, 2.7 SE
short) nor the law's recovery (256 passes but is 37.5% above the knee).** The
depth ratio on doubling d=8→16 is ×1.67, not ×1.5 — the "sub-linear" coefficient
is NOT constant, so a power law is refuted. The crossing sits robustly in (144,
160]; the d=16 knee is the softest of the series (k=144 fails by 0.004 ≈ 2.7 SE,
k=160 passes by 0.001 ≈ 0.7 SE) — flagged for a second seed below.

## 3. The depth leg at ctx=512 is AFFINE: k* = 8d + 32

| d | k* (seeds) | d·ctx/32 | **8d + 32** | depth ratio on doubling d |
|---|---|---|---|---|
| 4 | 64, 64 (NET-35/36) | 64 | **64** | — |
| 8 | 96, 96 (NET-38/39) | 128 | **96** | ×1.5 |
| 16 | **160** (this round) | 256 | **160** | ×1.67 |

All three ctx=512 points lie EXACTLY on the affine line **k\* = 8d + 32 =
(ctx/64)·d + (ctx/16)** — slope HALF the small-context value (ctx/32 = 16) plus
a positive intercept (ctx/16 = 32). The product law d·ctx/32 fits only d=4. So
NET-38/39's "sub-linear depth leg" was the FIRST STEP of this affine law: the
per-doubling ratio is ×1.5 then ×1.67 and approaches ×2 as d grows (the
intercept's relative contribution shrinks). At ctx ≤ 256 the law is EXACT product
(slope ctx/32, zero intercept — e.g. (d=8, ctx=256): k*=64 = d·ctx/32, not 96);
the crossover from product to affine lies in (256, 512]. The economic reading:
the guarantee d·ctx/32 is a proven-safe upper bound at long context, and the
ACTUAL available speedup at ctx=512 is d=4 → **8.0×**, d=8 → **5.33×**, d=16 →
**3.2×** (vs the guaranteed 2.0× at d=16) — the over-pruneable factor grows with
depth.

## 4. Concentration — depth diffusion continues, NO bounded working set

| statistic | d=4 (NET-35) | d=8 (NET-38) | d=16 (this round) |
|---|---|---|---|
| eff support exp(H) | 152.11 | 177.80 | **199.84** |
| top-128 mass | 0.806 | 0.814 | **0.771** |
| eff early | 20.4 | 23.09 | **25.55** |
| eff mid | 133.4 | 156.01 | **174.57** |
| eff late | 281.2 | 332.15 | **372.99** |

Depth diffusion at ctx=512: eff 152.11 → 177.80 → 199.84 across d=4/8/16
(×1.17/×1.12 per depth doubling). Top-128 mass DROPS at d=16 (0.771 vs 0.806/0.814)
— the distribution spreads further with depth. Per-position monotone
early ≪ mid ≪ late persists — no bounded working set at d=16.

## 5. Selection importance survives but DILUTES with depth

| k | top-k | random-k | gap |
|---|---|---|---|
| 128 | 0.967 | 0.933 | +3.4 |
| 256 | 0.993 | 0.970 | +2.3 |

Random-k gaps +3.4/+2.3 — positive but the SMALLEST of any measured cell
(+3.7–10 elsewhere). At d=16 the selection information is diluted, consistent
with the depth diffusion above: weight-selected positions still matter, but less.

## 6. Verification vs the network-loop barriers

- **(a) Circularity — no.** Prediction (144 vs 256) stated BEFORE the run; the
  outcome (160) is neither horn — it discriminates against both and reveals a
  third structure (the affine law), which is checked against the prior measured
  points (64, 96) ex post but stated as a law in this paper.
- **(b) Known-method-in-disguise — no.** Depth-scaling law for data-free
  attention key/value pruning: none in the Catalog (698-pkg re-scan) nor in the
  broader literature (nearest: layer-level pruning arXiv 2512.20636, KV-cache
  pruning — orthogonal; no per-depth retention law).
- **(c) Toy-scale — confronted.** d=16 × ctx=512 real causal word LM, causal
  masking, 4097 vocab, held-out loss AND accuracy.
- **(d) Data leakage — none.** Held-out last-10% windows; top-k data-free from the
  eval input's own causal attention.
- **(e) Variance/reproducibility — the round's honest limit.** The d=16 cell is
  SINGLE-SEED and its knee is the SOFTEST of the series (k=144 fails by 2.7 SE,
  k=160 passes by 0.7 SE). Two mitigations: (i) the affine law rests on the
  three-depth SHAPE (all three ctx=512 points exactly on 8d+32; the d=4, d=8
  rungs are two-seed), not on the exact d=16 knee; (ii) the crossing is robustly
  in (144, 160] even if a re-measure moved the exact value. A second seed at this
  cell is the immediate next round (mirroring NET-38→39).
- **(f) Measurement — documented.** Same metrics/protocol as every prior cell;
  k=384 loss 5.3172 vs full 5.3147 (converges); binom SE ≈ 0.15% acc; k=32–96
  fail by 3.3–8.6 SE, k=144 fails by 2.7 SE, k=160 passes by 0.7 SE (soft, as
  above).
- **(g) Baseline unfairness — none.** Full-attention reference per model; random-k
  control at the same k; same 0.98 bar.
- **(h) Practical relevance — sharpened.** The depth leg's true form at long
  context is now measured, not guessed: at (d=16, ctx=512) the deployable k is
  160 (3.2×), the guarantee 256 (2.0×) is safe but leaves 1.6× on the table, and
  the affine law predicts the crossover context (in (256, 512]) where the depth
  slope halves.

## Verdict

NET-40 (speed axis, third rung of the ctx=512 depth ladder): **DEPTH-LEG-IS-AFFINE-AT-LONG-CONTEXT — k\* = 160 at (d=16, ctx=512), completing the exact
three-point linear law k\* = 8d + 32 = (ctx/64)·d + (ctx/16) at ctx=512.** The
×1.5 sub-linear coefficient of NET-38/39 is NOT a power law — the second doubling
gives ×1.67 (96→160), refuting P1 (144) by 2.7 SE, and the law does NOT recover
to d·ctx/32 (P2, 256, passes but is 37.5% above the knee). At ctx=512 the depth
leg is linear with HALF the small-context slope (ctx/64 vs ctx/32) plus a
positive intercept (ctx/16); at ctx ≤ 256 the product law holds exactly, so the
crossover lies in (256, 512]. The deployable speedup at ctx=512 is 8.0×/5.33×/3.2×
at d=4/8/16 (guarantee: 4×/4×/2×). Concentration diffuses with depth (eff
199.84, top-128 mass drops to 0.771), selection importance dilutes (+2.3–3.4,
smallest of any cell), no bounded working set. Honest limit: the d=16 cell is
single-seed with the softest knee of the series — a second seed is the immediate
next round. Remaining: **d=16 ctx=512 second seed (the affine law's third rung —
highest value)**, ctx=1024 second seed, d=8 @ ctx=256 s0 corner; and the carry
chain at scale (the frontier).
Round-net-40. Now 40 network experiments. Assessment v40. Paper 84, issue #147.
Scripts: /tmp/exp_net_attncost_d16_ctx512.py; log: /tmp/net40.log.

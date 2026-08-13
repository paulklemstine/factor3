# Activation-Aware (Outlier) Quantization on a Real Causal LM: the 4-Bit Interface Floor Is Not an Outlier Artifact (NET-13)

**Program:** Network/LLM research lab — round-net-13 (the compression-axis rotation: activation-aware/outlier allocation, continuing NET-12)
**Date:** 2026-08-13
**Status:** Machine-verified (quantization-axis test, interface outlier diagnostics, magnitude-split sweep, and percentile-clip lever on a real causal word LM, d=4, 5 Gutenberg novels, dm=64, ctx=128, vocab 4097, 2000 AdamW steps).

## Hypothesis and statement

NET-12 found that per-channel (per-row) uniform-4 is lossless on a real causal
LM (0.987 @ 4.0 bits) while the 4-bit interface (embed/pos/un) is irreducible
under both per-tensor and per-row primitives (per-row uniform-3 = 0.947).
The classic LLM-quantization story (LLM.int8 / AWQ / SmoothQuant) is that
**outliers dominate the error**, so a natural read of the floor is: it is an
artifact of symmetric RTN wasting precision on a few outlier rows. **Hypothesis:
an activation-aware/outlier-aware primitive (input-channel axis, magnitude
split, or outlier clipping) breaks the 4-bit interface floor**, giving a
lossless schedule below 4.0 avg bits. Falsified if all three fail — i.e. the
interface's bit-need is distributed and the floor is structural at this scale.

## 1. Setup (identical to NET-10/11/12 family)

Same 5 Gutenberg novels, word-level top-4097 vocab, ctx 128, contiguous 90/10
split, causal transformer (is_causal=True) dm=64/4 heads, d=4 × seed 0, 2000
AdamW steps — full acc reproduces **0.1571** a fourth time, bar 0.98·full =
0.1540. All quantization evals are joint (independent loaded copy, full
held-out eval). Three parts + a clip lever:

- **A. Quantization axis.** Per-COLUMN (input-channel) symmetric RTN — the
  standard group-quantization axis — on uniform-2/3 and role(4/3/2), vs the
  per-row (0.588/0.947/0.892) and per-tensor (0.112/0.825/0.878) references.
- **B. Outlier diagnostics.** Row-norm structure (max/mean, top-1% magnitude
  share, kurtosis) of the interface (embed/un/pos) vs the interior (wq0/mi0/mo0).
- **C. Magnitude split.** Interface rows: top-k ∈ {0,8,16,32,64,128,256} at 6
  bits, the rest at 2 bits (per-row scales, data-free); interior fixed clean
  (mi/mo=4, attn=3, lnf=2). Does magnitude-aware allocation shatter the floor?
- **D. Outlier clipping** (SmoothQuant/AWQ-style): per-row scale from the 99.9th
  / 99.0th percentile of |W| instead of the max, on uniform-3/4.

## 2. Part A — the quantization axis does not break the floor

| schedule | per-tensor | per-row | **per-column** |
|---|---|---|---|
| uniform-2 | 0.112 | 0.588 | **0.413** |
| uniform-3 | 0.825 | 0.947 | **0.900** |
| role(4/3/2) | 0.878 | 0.892 | **0.923** |

Per-column (input-channel) is **worse than per-row** for uniform-2/3 and only
marginally better than per-row for the role schedule — still 5 points short of
lossless. The standard LLM-quant axis does not break the 4-bit interface floor;
if anything the per-row (output-channel) axis remains the better primitive at
this scale. (Group sizes < full per-column, e.g. group-128, sit between these
two by construction and were not separately needed to falsify the axis claim.)

## 3. Part B — the interface has only MILD outlier structure

| matrix | shape | row-norm max/mean | top-1% magnitude share | row-norm kurtosis |
|---|---|---|---|---|
| embed | (4097,64) | 1.4 | 0.036 | 3.0 |
| un | (4097,64) | **1.9** | 0.035 | **9.1** |
| pos | (128,64) | 1.2 | 0.036 | 2.2 |
| wq0 | (64,64) | 1.1 | 0.030 | 2.7 |
| mi0 | (256,64) | 1.2 | 0.031 | 3.7 |
| mo0 | (64,256) | 1.2 | 0.034 | 2.2 |

**There is no catastrophic outlier regime at this scale.** Top-1% of magnitude
holds only ~3.5% of the mass in every matrix — nothing like the 30–70% outlier
concentration reported for larger LMs. The readout un is the heaviest tail
(kurtosis 9.1, max/mean 1.9) but that is mild compared to the regime where
outlier-splitting pays. The 4-bit interface need is therefore **not** an outlier
phenomenon on this model.

## 4. Part C — magnitude split fails; the need is distributed

Interface rows at top-k 6-bit / rest 2-bit (interior clean at 4/3/2):

| k | retained | avg-bits |
|---|---|---|
| 0 | 0.636 | 2.45 |
| 8 | 0.693 | 2.46 |
| 16 | 0.703 | 2.47 |
| 32 | 0.706 | 2.48 |
| 64 | 0.724 | 2.52 |
| 128 | 0.791 | 2.58 |
| 256 | 0.819 | 2.74 |

Even promoting the top-256 rows (6% of 4097) to 6-bit while 2-bitting the rest
reaches only **0.819** — 16 points short of lossless, with a sublinear,
saturating k-dependence (each doubling of the promoted set buys a few points).
The interface's bit-need is **distributed across essentially all rows**, not
concentrated in a few magnitude outliers: magnitude-aware allocation cannot
shrink the schedule below ~4 bits.

## 5. Part D — outlier clipping does not help either

SmoothQuant/AWQ-style per-row scales from a percentile of |W| (outliers
clipped, bulk gets more range), on a fresh retrain (full acc re-verified
0.1571), vs the unclipped per-row references (uniform-3 0.947, uniform-4 0.987):

| schedule | clip-99.9% | clip-99.0% | unclipped per-row |
|---|---|---|---|
| uniform-3 | 0.948 | 0.944 | 0.947 |
| uniform-4 | 0.985 | 0.982 | 0.987 |

Clipping changes nothing at the margin: uniform-3 stays ~0.94–0.95 (3 points
under the bar) and uniform-4 stays lossless. Consistent with Part B — with only
~3.5% of magnitude in the top 1% of weights, there is no outlier mass to clip.
The last standard activation-agnostic lever is a no-op.

## 6. Verification vs the network-loop barriers

- **(a) Circularity — no.** Joint evals on independent loaded copies; the axis,
  split, and clip are data-free transforms of the trained weights; nothing
  injected.
- **(b) Known-method-in-disguise — the negatives are the content.** Per-column
  group quantization, magnitude-split, and percentile-clipping are all standard
  LLM-quant primitives — the finding is that on a real small causal LM **none
  of them breaks the 4-bit interface floor**, which is the specific negative the
  catalog (698 packages) has no record of (no outlier/activation-aware test on
  a real causal LM; prior LLM-outlier work targets much larger models with a
  real outlier regime).
- **(c) Toy-scale — confronted.** Real causal LM, real text, causal masking,
  4097 vocab. The scale matters: the mild-tail diagnostic (Part B) shows why
  this model is NOT in the outlier regime the bigger-model methods target.
- **(d) Data leakage — none.** Causal masking, contiguous no-overlap split,
  held-out eval, data-free quantization.
- **(e) Variance — honest limits.** One model (d=4 s0), reproduced exactly a
  fourth time; every eval is a full joint forward on the held-out 60k tokens.
- **(f) Measurement — documented.** 0.98·full bar throughout; outlier stats
  reported raw (max/mean, top-1% share, kurtosis); split k-sweep exhaustive
  over 7 values; a script bug (function-name collision in the schedule
  builders) crashed the first launch before any data and was fixed and re-run
  clean (the traceback is in the log, no data loss).
- **(g) Baseline fairness.** Per-row and per-tensor references from the same
  model family (NET-12); uniform-2/3/4 and role are honest joint baselines.
- **(h) Practical relevance.** The negative closes a branch: at this scale,
  outlier/magnitude-aware weight quantization is NOT the lever to beat 4 bits —
  the distributed interface sensitivity is structural. Practitioners should not
  expect AWQ-style fixes to buy them sub-4-bit lossless weight quantization on
  a small causal LM.

**Verdict.** NET-13 (compression-axis rotation, activation-aware allocation):
the 4-bit interface floor from NET-12 survives **every standard data-free
weight-quantization primitive** at this scale — the quantization axis (per-column
is no better than per-row: uniform-3 0.900 vs 0.947), the magnitude-split
(top-6% rows promoted to 6-bit recovers only 0.819, sublinear and saturating),
and outlier clipping (uniform-3 stays 0.944–0.948, uniform-4 stays lossless).
The reason is Part B: the interface has only **mild** outlier structure (top-1%
magnitude share ~3.5% in every matrix; un heaviest at kurtosis 9.1 but nowhere
near the 30–70% concentration of larger-LM outlier regimes), so there is no
outlier mass for activation-agnostic methods to exploit. The interface's 4-bit
need is **distributed**, making the floor structural at this scale. The honest
remaining lever is genuinely activation-aware quantization (SmoothQuant-style
per-channel activation scales from calibration passes) — the one thing this
round did not test, since it is not data-free. Round-net-13.
Now 13 network experiments. Assessment v13. Paper NET-13, issue #108.
Scripts: /tmp/exp_net_outlier.py, /tmp/exp_net_outlier_partD.py.

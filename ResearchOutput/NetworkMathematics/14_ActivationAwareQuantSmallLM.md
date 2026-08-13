# Activation-Aware Quantization with Calibration Passes Is Not the Lever Either: the 4-Bit Interface Floor Is Activation-Irreducible at This Scale (NET-14)

**Program:** Network/LLM research lab — round-net-14 (the compression-axis rotation: the LAST untested lever — activation-aware quantization WITH calibration passes, continuing NET-13)
**Date:** 2026-08-13
**Status:** Machine-verified (AWQ/SmoothQuant-style per-channel activation scales from calibration on a real causal word LM, d=4, 5 Gutenberg novels, dm=64, ctx=128, vocab 4097, 2000 AdamW steps).

## Hypothesis and statement

NET-13 closed every *data-free* weight-quantization lever (axis, magnitude
split, clipping) and explicitly left ONE mechanism untested: **activation-aware
quantization with calibration passes** — the AWQ/SmoothQuant mechanism where
per-channel *activation* scales (from a calibration forward pass) are absorbed
into the weight quantizer, so channels with large activation magnitude keep
relatively finer precision. That mechanism is the basis of the strongest
practical sub-4-bit quantization results on bigger LMs, so it was the natural
last hope for the 4-bit interface floor. **Hypothesis: calibration-derived
activation scales break the floor** — either directly (AWQ absorption makes
per-row uniform-3 lossless, 0.947 → ≥0.98) or via activation-informed bit
allocation (a schedule below uniform-4's 4.00 bits that is lossless). Falsified
if the AWQ absorption is a no-op at uniform-3 and activation-informed
allocation fails to beat uniform-4.

## 1. Setup (identical to NET-10/11/12/13 family)

Same 5 Gutenberg novels, word-level top-4097 vocab, ctx 128, contiguous 90/10
split, causal transformer (is_causal=True) dm=64/4 heads, d=4 × seed 0, 2000
AdamW steps — full acc reproduces **0.1571 a fifth time**, bar 0.98·full =
0.1540. Calibration: forward pass on 512 **training** sequences (held-out eval
never touches calibration — no leakage). Per-channel activation scale =
max|x_j| over calibration for each Linear's input channels. AWQ quantizer:
W[:,j] ← W[:,j]/s_j (s_j = act_max_j^α), per-row RTN, scale back — the standard
weight-only AWQ application. All evals joint (independent loaded copy).

## 2. The calibration diagnostic — activation scales are nearly FLAT

| matrix | shape | mean per-channel act max | max per-channel act max | max/mean |
|---|---|---|---|---|
| un | (4097,64) | 2.130 | 2.574 | 1.21 |
| wq0 | (64,64) | 2.116 | 2.262 | 1.07 |
| mi0 | (256,64) | 2.117 | 2.304 | 1.09 |
| mo0 | (64,256) | 1.820 | 2.263 | 1.24 |

**The per-channel activation scales AWQ exploits are near-uniform** (max/mean
1.07–1.24 across the model). AWQ's absorption only pays when some channels
carry 10–100× the activation magnitude of others; at this scale the activation
profile is flat, so there is no channel heterogeneity to exploit — the same
"not in the target regime" story as NET-13's weight outliers, now on the
activation side.

## 3. Part A — AWQ absorption does not break the per-row uniform-3 floor

| quantizer | retained | vs plain per-row |
|---|---|---|
| AWQ α=0.25 uniform-3 | 0.938 | −0.9pt |
| **AWQ α=0.50 uniform-3** | **0.943** | **−0.4pt (no help)** |
| AWQ α=1.00 uniform-3 | 0.888 | −5.9pt (much worse) |
| plain per-row uniform-3 | 0.947 | — |
| AWQ α=0.50 uniform-4 | 0.987 | = lossless |
| plain per-row uniform-4 | 0.987 | = lossless |

The best α (0.5) is *marginally worse* than plain per-row (0.943 vs 0.947);
full-strength α=1.0 degrades sharply (0.888). At 4 bits both are identically
lossless (0.987) — AWQ is a strict no-op-to-negative at this scale. The
calibration pass buys nothing.

## 4. Part A2 — the interface-at-3 probe: still 2.2 points short

Interface (embed/pos/un) at 3 with AWQ scales, interior clean (mi/mo=4,
attn=3, lnf=2): **0.958 @ 3.18 avg bits** — better than the full-model
uniform-3 0.947 (because the interior is cleaner), but still **2.2 points
under the 0.98 bar**. The interface's irreducible 3-bit cost survives the
activation-calibration mechanism applied directly to it.

## 5. Part B — activation-informed allocation is a BAD signal at this scale

25 Linears ranked by mean per-channel activation max, bits 4/3/2 by tercile
(embed/pos pinned at 4 = their NET-11 b*; one-hot inputs have no activation
scale):

| schedule | retained | avg-bits |
|---|---|---|
| activation-tercile | **0.828** | 3.69 |
| activation-tercile + AWQ scales | 0.841 | 3.69 |
| role (weight-based, NET-12) | 0.892 | 3.64 |
| uniform-4 per-row (NET-12) | 0.987 | 4.00 |

Activation sensitivity ranking is **dramatically worse** than the weight-based
role schedule (0.828 vs 0.892 at equal bits) and 16 points below uniform-4.
The top-ranked matrices (un, mi0, wq0, …) are exactly the interface+early
interior — the ranking just re-discovers the interface is fragile, but it
can't allocate below 4 bits to save anything; the tercile schedule 2-bits the
deeper interior, which costs ~8 points. Activation scale is not a usable
allocation signal at this scale.

## 6. Verification vs the network-loop barriers

- **(a) Circularity — no.** Joint evals on independent loaded copies; the AWQ
  absorption is a standard data-free-of-test weight transform; calibration
  uses training data only.
- **(b) Known-method-in-disguise — the negative is the content.** AWQ and
  SmoothQuant are mature, standard methods — the finding is that the
  calibration-based lever (the one NET-13 explicitly flagged as the last hope)
  does NOT transfer to a small real causal LM, because the per-channel
  activation heterogeneity it exploits is absent (max/mean 1.07–1.24). Catalog
  (698 packages): no activation-calibration test on a real small causal LM.
- **(c) Toy-scale — confronted.** Real causal LM, real text, causal masking,
  4097 vocab. The flat-activation diagnostic explains *why* this scale is not
  in the target regime.
- **(d) Data leakage — none.** Causal masking, contiguous split, calibration on
  training sequences only, eval on held-out.
- **(e) Variance — honest limits.** One model (d=4 s0), reproduced exactly a
  fifth time; every eval a full joint forward on the held-out 60k tokens.
- **(f) Measurement — documented.** 0.98 bar throughout; α-sweep over 3 values;
  raw activation stats reported (mean/max per-channel act max + max/mean);
  plain per-row uniform-3/4 re-verified in-run on the same model; a hook-closure
  bug (per-module accumulator never updated) crashed the first launch before
  any data and was fixed + re-run clean (traceback in the log).
- **(g) Baseline fairness.** Plain per-row uniform-3 (0.947) and uniform-4
  (0.987) re-measured in-run; role and uniform-4 references from the same model
  family (NET-12).
- **(h) Practical relevance.** The negative closes the compression axis at this
  scale: the 4-bit interface floor is not just data-free-irreducible (NET-13)
  but ACTIVATION-irreducible (NET-14) — even calibration passes don't buy
  sub-4-bit lossless weight quantization on a small causal LM. The practical
  optimum remains per-channel uniform-4 (4.00 bits, 0.987), data-free.

**Verdict.** NET-14 (compression-axis rotation, the last lever): activation-aware
quantization WITH calibration passes does NOT break the 4-bit interface floor.
The AWQ absorption is a no-op-to-negative (best α=0.5: 0.943 vs plain 0.947;
α=1.0: 0.888), the interface-at-3 probe stays 2.2 points short (0.958 @ 3.18
bits), and activation-informed allocation is far worse than weight-based
(0.828–0.841 vs role 0.892 / uniform-4 0.987). The mechanism fails because the
per-channel activation scales are near-uniform (max/mean ≈ 1.2 across the
model) — there is no channel heterogeneity for AWQ's absorption to exploit,
mirroring NET-13's flat weight-outlier structure. **The compression axis at
small real-LM scale is now exhausted**: every primitive — per-tensor (5.31
bits), per-row/per-column uniform-4 (4.00 bits, the lossless floor), magnitude
split, percentile clipping, and now activation-calibration — leaves the
interface irreducible below 4 bits. Round-net-14.
Now 14 network experiments. Assessment v14. Paper NET-14, issue #109.
Scripts: /tmp/exp_net_act.py.

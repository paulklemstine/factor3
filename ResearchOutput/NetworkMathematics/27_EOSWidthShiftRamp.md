# EOS-WIDTH-SHIFT-IS-A-MONOTONE-RAMP — 24 Fresh Arms Map P(cure) over (20,28] and Refute Both the Sharp-Threshold and First-Dim-Suffices Readings (NET-27)

**Program:** Network/LLM research lab — round-net-27 (performance/mechanism axis; NET-26's flagged open question: the shape of the EOS-width P(cure) shift inside (20,28))
**Date:** 2026-08-14
**Status:** Machine-verified (ALL_DONE_NET27). LSB-first base-10 a+b=c, plain n=5 training, GRUCell(384→192) with a learned E-d EOS (final-carry) input zero-padded to a fixed 384-d input, bs=256, 12000 AdamW steps, lr 1e-3, eval n=5/6/7/8 (2048 fresh draws, teacher-forced, full/per/per-position). Twenty-four arms: E ∈ {21,22,24,28} × 6 fresh seeds (8–13) — all architecture/task/budget byte-identical to the NET-26 sweep (imported `EOSWidthGRU`/`eval_net`/`probe_n8` from the NET-26 module). Each seed is an independent draw from P(cure|E); all 24 seeds are fresh (NET-26 used 0–7), so the merged endpoint distributions stay independent.

## Hypothesis and statement

NET-26 established the two endpoints of the EOS-width shift on the plain n=5
carry-wall cure: P(cure|E=20) = 3/12 = 25% (wide continuum 0.005…0.999, median
0.044) vs P(cure|E≥28) = 20/20 (all 1.0000), and proposed the controlling
variable: **representational distinctness** — at E=20 the learned EOS occupies
exactly the digit one-hot subspace (dims 0–19, no exclusive dims) so the
boundary step is ambiguous with a digit step; at E≥28 the EOS has exclusive
dims 20..E−1 that no digit column activates. NET-26 explicitly left the shape
of the shift inside (20,28) open ("E=24 would resolve").

This round fills that gap with 24 fresh arms and answers two questions at once:

1. **Is the shift sharp (a single critical width) or gradual?** If sharp, some
   E* in {21,22,24} would show the E=20-style fragility and E*+1 the E≥28-style
   certainty. If gradual, P(cure) would rise across widths.
2. **Is the first exclusive dim sufficient?** The naive reading of the
   distinctness law — "any exclusive dim carves an unambiguous boundary" —
   predicts E=21 (exactly ONE exclusive dim, dim 20) should already be robust.
   The alternative — the benefit is a *reliability curve* in the number of
   exclusive dims k = E−20 — predicts E=21 is intermediate.

## Setup

Identical to the NET-26 sweep in every detail that matters. The model is the
NET-26 `EOSWidthGRU(eos_width)`: GRUCell(384→192) over zero-padded raw one-hot
digit columns (functionally raw 20-d one-hots at every digit column, 364 dead
dims), a learned E-d EOS vector zero-padded to 384 (E ∈ {21,22,24,28}),
Linear(192→10) readout, n GRU steps emitting head(h) then one EOS step.
GRUCell/W_ih are byte-identical across every arm; only the number of trainable
EOS parameters E varies (GRUCell inits all params from U(±1/sqrt(192))
regardless of in_dim — established NET-25 — so the pad does not change init
scale; the EOS parameter itself inits at 0).

- **Sweep** (24 arms): E × 6 fresh seeds (s=8..13). Output per arm: n=5/6/7/8
  full/per/per-position + a PROBE line (per-column mean hidden-norm and mean
  readout max-softmax on n=8 eval, cols 1..8 then the EOS step = col 9).
- **Freshness:** every seed used here (8–13) is new to the whole program, so
  each width's 6 samples are independent draws, and they never overlap the
  E=20 (seeds 0–7) or E=28 (seeds 0–7) samples merged from NET-26.

## Results

All numbers: full (all n+1 digits exact) / per. n=8 full is the length-gen bar
(chance 1e-9).

### The four-width, six-seed sweep (24 arms)

| E (exclusive dims k) | n=8 full over seeds 8–13 | P(≥0.99) | min | median |
|---|---|---|---|---|
| **21** (k=1) | 1.0000, 0.7715, 0.1567, 0.8926, 1.0000, 0.2656 | 2/6 | 0.1567 | ≈0.83 |
| **22** (k=2) | 1.0000, 0.9912, 0.9482, 1.0000, 1.0000, 0.9990 | 5/6 | 0.9482 | ≈1.0 |
| **24** (k=4) | 1.0000 ×6 | 6/6 | 1.0000 | 1.0 |
| **28** (k=8) | 1.0000 ×6 | 6/6 | 1.0000 | 1.0 |

**E=21 is the only width in this round with both a full cure and a hard
failure among fresh draws.** Its distribution {1.0000, 0.8926, 0.7715, 0.2656,
0.1567, 1.0000} spans the whole range — a single exclusive dim right-shifts
the E=20 distribution but leaves a seed-fragile failure tail. E=22 has no hard
failure (worst case a near-cure 0.9482). E≥24 never leaves 1.0000.

### The E=21 failure signature (progressive-unroll collapse, NET-26-style)

The two hard failures degrade smoothly across beyond-max n, exactly like
NET-26's E20 s1:

| arm | n=5 | n=6 | n=7 | n=8 full |
|---|---|---|---|---|
| E21 s10 | 1.0000 | 0.9995 | 0.8203 | **0.1567** |
| E21 s13 | 1.0000 | 0.9995 | 0.8096 | **0.2656** |

In-range mastery is perfect; the OOD unroll collapses continuously, and the
failures cluster errors in a few columns (full 0.16–0.27 at per 0.88–0.89).

### The probe discriminator reproduces exactly (mechanism check)

Per-column hidden-norm and readout max-softmax on n=8 eval, cols 5→8 then the
EOS step (col 9):

| condition | hidden-norm cols 5→8 (Δ) | maxconf cols 6–8 | EOS-step col 9 |
|---|---|---|---|
| **E21 s10** (fail 0.157) | 10.15 → 12.10 (**+1.95**) | **0.999, 0.919, 0.935** | norm keeps rising 12.10 |
| **E21 s13** (fail 0.266) | 10.17 → 11.42 (**+1.26**; peaks 11.95 at col 9) | **0.999, 0.929, 0.899** | norm keeps rising 11.95 |
| E21 s9 (partial 0.772) | 10.34 → 11.19 (**+0.85**) | 1.000, 0.994, 0.898 | rising 11.80 |
| **all cures** (E21 s8/s12, E22/24/28 ×6) | ~10.2 → ~10.4 (Δ<0.2) | 1.000 all | settles ~10.2–10.5 (or small bump) |

The discriminator from NET-26 — cures keep ‖h‖ flat and maxconf 1.000 at
beyond-training columns; failures drift ‖h‖ up and the readout dips exactly
where the unroll goes OOD — holds line-for-line at E=21. The failure mechanism
is width-independent: it is the same boundary-conditioning failure, and
exclusive dims only raise the probability that training finds a working
boundary.

### Merged distribution across both rounds

| E (k) | samples | n=8 full (n/20 merged where applicable) | P(cure ≥0.99) | failure mass |
|---|---|---|---|---|
| **20** (k=0) | 12 | {0.999×3, 0.744, 0.124, 0.058, 0.031, 0.026, 0.017, 0.011, 0.006, 0.005} | 3/12 = 25% | 9/12 = 75% |
| **21** (k=1) | 6 | {1.0, 0.893, 0.772, 0.266, 0.157, 1.0} | 2/6 = 33% | 4/6 = 67% |
| **22** (k=2) | 6 | {1.0, 0.999, 0.991, 1.0, 1.0, 0.948} | 5/6 = 83% | 1/6 = 17% (near-cure) |
| **24** (k=4) | 6 | 1.0000 ×6 | 6/6 = 100% | 0 |
| **≥28** (k≥8) | 26 | all 1.0000 (20 NET-26 + 6 NET-27 E28) | 26/26 = 100% | 0 |

The failure mass is a monotone decreasing ramp: **75% → 67% → 17% → 0 → 0**,
and the worst-case outcome rises monotonically: 0.005 → 0.157 → 0.948 → 1.0 →
1.0. Every width contributes to the ordering; no single width carries it.

## The law

**EOS-WIDTH-SHIFT-IS-A-MONOTONE-RAMP (REFINES NET-26; REFUTES THE SHARP-
THRESHOLD READING AND THE FIRST-EXCLUSIVE-DIM-SUFFICES READING).**

1. **There is NO sharp critical width in (20,28].** E=21 produces both a full
   cure (1.0000) and a hard failure (0.1567) across 6 fresh seeds on the
   byte-identical architecture — the same width, same task, same budget. No
   width in this band "unlocks" the cure deterministically; NET-26's endpoints
   (25% at E=20, 100% at E≥28) are connected by a ramp, not a cliff.
2. **The first exclusive dim is NOT sufficient** — the naive "any exclusive dim
   carves an unambiguous boundary" reading of the distinctness law is REFUTED.
   E=21 (k=1) is still seed-fragile: P(cure)=33%, median ≈0.83, two hard
   failures. The exclusive-dim benefit is SUBLINEAR in k.
3. **The ramp's shape: a right-shift of a wide distribution, then saturation.**
   Adding the first exclusive dim moves the whole distribution right (median
   0.044 → 0.83) while preserving a fragile tail; k=2 removes the hard-failure
   tail (worst case 0.948); k=4 saturates (6/6, worst case 1.0000); k≥8 stays
   saturated (26/26 across both rounds). Failure mass 75% → 67% → 17% → 0 → 0.
4. **The failure mechanism is width-independent** — same progressive-unroll
   collapse (1.0 → ~0.82 → ~0.16–0.27 across n=6/7/8), same clustered-column
   errors, same probe signature (‖h‖ drift + maxconf dips at beyond-training
   columns) as NET-26's E=20 failure. Exclusive dims raise P(working boundary),
   not the boundary's kind. (Fisher on {2/6 vs 5/6} is ~0.24 2-sided — the
   E21→E22 jump alone is not significant at this n; the law rests on the
   full-width monotone ordering + merged anchors, not any single pair.)

**Mechanism hypothesis (flagged, not proven):** with k exclusive dims the
learned EOS boundary signal has k free coordinates that no digit column ever
activates, and BPTT-through-time must pin them to nonzero values that keep the
hidden state in-distribution at depth. k=1 is one scalar — an easy coordinate
for the optimizer to drop or overfit, hence seed-fragile; k≥2 provides
redundancy that makes a working boundary much more likely to be found; k≥4 is
effectively certain. This keeps NET-26's distinctness framing (the boundary
token needs its own parameter subspace) while replacing "any distinct
subspace" with "a subspace rich enough to survive optimization" — a
*reliability* statement rather than a *capacity* one.

## Verdict on the hypothesis

**Gradual — both sharp-threshold readings are refuted.** The shift is a
monotone reliability ramp: P(cure) rises 25% → 33% → 83% → 100% → 100% and the
worst-case outcome rises 0.005 → 0.157 → 0.948 → 1.0 → 1.0 as the number of
exclusive EOS dims goes 0 → 1 → 2 → 4 → 8. There is no critical width; the
benefit of exclusive dims is real, monotone, and saturating. NET-26's
"representational distinctness" law is refined to a quantified curve, and the
paper's own open question ("E=24 would resolve") is answered: E=24 is the
first width at which 6/6 fresh draws are clean.

## Verification vs the network-loop barriers

- **(a) Circularity — clean.** Eval n=6/7/8 are fresh draws never in training;
  all arms train n=5 only. The sweep varies exactly one architectural quantity
  (trainable EOS width) at fixed GRUCell(384); nothing is injected into eval.
- **(b) Known-method-in-disguise — clean.** The contribution is the empirical
  shape of an in-lab law (established NET-26); the architecture is unchanged.
  Catalog re-checked this round: no catalog package on EOS/sentinel/boundary-
  token width distributions or length-gen cure reliability curves; the
  tropical-recurrent gap (open build-on 1 in [[catalog-network-prior-work]])
  is untouched.
- **(c) Toy-scale — confronted.** Same toy scale as the whole carry-wall line
  (raw one-hot digits, GRUCell(384)); this round quantifies the *toy law
  itself*. Real-scale transfer of the cure (with a well-conditioned exclusive-
  dim boundary input) remains the open frontier, flagged since NET-24.
- **(d) Data leakage — clean.** Fresh random batches; no beyond-max example
  trained; teacher-forced eval on inputs only.
- **(e) Variance/reproducibility — the central barrier of the round, closed
  as far as the design allows.** 6 fresh seeds per width (all new to the
  program), 24 new arms, merged anchors of 12 (E=20) and 26 (E≥28) samples.
  The E=21 spread (0.157 vs 1.0000) is seed variance — and it IS the law. One
  honest limit: with n=6 per width, the E21→E22 P-jump is not individually
  significant (Fisher ≈0.24); the ramp rests on the monotone ordering across
  four widths plus the much larger merged anchors. Remaining 1-point gaps:
  E=23 and E=25 untested (would refine the knee between k=1 and k=4).
- **(f) Measurement — clean.** Teacher-forced exact-match full/per/per-position;
  the probe (hidden-norm + maxconf per column) reproduces NET-26's cure/fail
  discriminator line-for-line at E=21.
- **(g) Baseline fairness — strong.** Every arm shares task/budget/eval and
  the byte-identical GRUCell/head/readout; only E varies; seeds are fresh and
  independent. Merging reuses NET-26's samples with identical construction.
- **(h) Practical relevance — a sharper design rule.** For length-general
  sequential computation with a state-augmented answer path: the final-step
  boundary token needs a few exclusive dims, not one and not merely "width".
  The rule now has a curve: 1 exclusive dim → 33% reliable, 2 → 83%,
  ≥4 → ~certain. A real-LM boundary token should reserve ≥4 exclusive dims for
  the final step, and single-seed "threshold" results in toy mechanism studies
  should be read as draws from such a curve.

## Notes for the coordinator

- **Refinement of NET-26, not a correction to its endpoints.** NET-26's two
  anchors (E=20 fragile, E≥28 certain) survive; its open question (the shape
  inside (20,28)) is now answered: monotone ramp, no critical width, first
  exclusive dim NOT sufficient, saturation by E=24. The "distinctness" framing
  is sharpened from "any exclusive subspace" to "a subspace rich enough to be
  reliably found by optimization" (k≥4 ~certain, k=2 near, k=1 fragile).
- **Numbers to quote:** failure mass vs E: 75% (E=20) → 67% (E=21) → 17%
  (E=22, worst case a near-cure 0.948) → 0 (E=24) → 0 (E≥28, 26/26). Worst
  case n=8 full: 0.005 → 0.157 → 0.948 → 1.0000 → 1.0000. Medians: 0.044 →
  0.83 → 1.0 → 1.0 → 1.0. E=21 is the only width observed with both a full
  cure and a hard failure among fresh draws.
- **Combined E≥28 is now 26/26 clean cures** (20 from NET-26: 14 sweep + 6
  dist; 6 from this round's E=28 fresh seeds).
- **Open questions (natural next rounds):** (1) the knee inside (21,24) —
  E=23/E=25 would localize where P reaches ~100% (E=24 is the current first
  all-cure width); (2) does the reliability curve transfer to the real causal
  LM's final step with an exclusive-dim boundary input (the NET-24/25/26
  frontier); (3) a mechanistic read of WHY k=1 fails — e.g. measure the learned
  EOS coordinate values in dim 20 at cure vs fail (is the exclusive coordinate
  pinned nonzero in cures, dropped in failures?) — a direct, cheap next
  experiment.
- Scripts: /tmp/exp_net_eos_shape.py (ALL_DONE_NET27). Log:
  /tmp/net27.log. Imports the NET-26 module (EOSWidthGRU/eval_net/probe_n8)
  so the architecture is byte-identical to paper 70.

# THE-EXCLUSIVE-BOUNDARY-CHANNEL-IS-TRAINING-TIME-LOAD-BEARING — 12 Causal Freeze/Intervention Arms Show the k=3 Cure Is (Mostly) Self-Sufficient at Eval, with Internalization Proportional to Cure Quality (NET-29)

**Program:** Network/LLM research lab — round-net-29 (mechanism axis; the causal test NET-28's "open (1)" flagged: freeze/project-out the exclusive coords of a trained cure)
**Date:** 2026-08-14
**Status:** Machine-verified (ALL_DONE_NET29). Twelve arms, each a SAME-SEED REPRODUCTION of a NET-28 arm (byte-identical EOSWidthGRU, same seeds, same training; the trained EOS exclusive coordinates reproduce NET-28's values to 3 decimals — every intervention below attaches to the exact published trained solutions). Each trained arm is evaluated at n=5/6/7/8 (2048 FRESH draws per arm × per intervention, teacher-forced) under eval-time manipulations of the learned EOS exclusive coords. All manipulations are inference-only; no retraining.
- **Part A (k=3, the 6 NET-28 cures):** E=23 × seeds 8–13, 7 interventions each — `ctl` (re-baseline), `zero3` (zero the whole exclusive block eos[20:23]), `zero1@0/1/2` (zero ONE exclusive coord), `flip1@0` (sign-flip one), `scale0.1` (attenuate the whole block ×0.1). 42 arm-interventions.
- **Part B (k=1, all 6 NET-28 outcomes):** E=21 × seeds 14–19, 2 interventions each — `ctl`, `zero1` (zero the sole exclusive coord eos[20]). 12 arm-interventions.

## Hypothesis and statement

NET-28 read the trained EOS exclusive coordinates PASSIVELY: at k=1 they are pinned
|0.67–0.91| in ALL outcomes (cure, near, partial, fail alike), so the boundary
signal is always present and the k=1 fragility is downstream. That still left
open WHERE the exclusive channel acts: at eval (Prediction 1: the trained
dynamics USE the exclusive input at inference — zeroing it degrades the cure)
or only at train (Prediction 2: the exclusive dims shape the weights during
BPTT, and the trained recovery is self-sufficient — zeroing leaves the cure
intact). NET-28's flagged causal test (open question 1) is to intervene:
retrain the exact arms and perturb the exclusive coords at eval. This round
does exactly that, plus three structural probes at k=3 — redundancy (zero ONE
coord: does any single coord carry the channel?), value-sensitivity (flip the
sign), and magnitude-sensitivity (scale ×0.1).

## Results

All numbers are n=8 full (all 9 digits exact; chance 1e-9); n=5/6/7 shown where
they differ from the n=8 pattern. Every `ctl` reproduces the NET-28 outcome on
fresh draws (Part A: 1.0000 ×6; Part B: {1.0000, 0.9858, 0.1602, 0.5884,
0.2412, 0.7856} ≈ NET-28's {1.0000, 0.9878, 0.1313, 0.5835, 0.2490, 0.7954}).
Binom. SE at 2048 draws: ≤0.5% at p≈1, ~0.8% at p≈0.16, ~0.9% at p≈0.78.
"no-op" = |Δ| ≤ 1.2 SE.

### Part A — the k=3 cures under eval interventions (n=8 full)

| seed | ctl | **zero3** (all 3 excl) | zero1 (any single) | flip1 | scale0.1 |
|---|---|---|---|---|---|
| 8  | 1.0000 | 1.0000 (n5/n7 0.9990) | 1.0000 | 1.0000 | 1.0000 |
| 9  | 1.0000 | 0.9995 (n5 0.9985, n6 0.9995) | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 0.9995 (n8) | 1.0000 | 1.0000 | 1.0000 |
| 11 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 12 | 1.0000 | 0.9971 (n5 0.9941, n6 0.9922) | 1.0000 | 1.0000 | 1.0000 |
| 13 | 1.0000 | **0.7041** (n5 0.6626, n6 0.7148) | 1.0000 | 1.0000 | **0.9692** |

**Removing the ENTIRE exclusive block at eval leaves the k=3 cure intact in 5/6
arms** (0.9971–1.0000; worst cost 0.3% scattered, never a collapse). In the 6th
arm (s=13) it degrades substantially but not catastrophically (0.70 with
per=0.967 — a partial degradation, not the E=20 hard-fragile regime of
0.005–0.3). Removing ANY SINGLE exclusive coord costs 0% in all 6 arms; sign
flips cost 0% in all 6; attenuating all three to 0.1× costs 0% in 5/6 and 3%
in s=13. s=13 is a MAGNITUDE-ENSEMBLE dependence: the channel is load-bearing
collectively (2-of-3 suffices, full strength needs all three, magnitude-
sensitive), never individually, and never value-sensitive.

### Part B — the k=1 arms under zero1 (n=8 full, NET-28 outcome → ctl → zero1)

| seed | NET-28 outcome | ctl | **zero1** (sole excl coord = 0) | Δ |
|---|---|---|---|---|
| 14 | cure 1.0000 | 1.0000 | **0.9717** (n5 0.9839, n7 0.9727) | **−2.8%** (~3 SE) |
| 15 | near-cure 0.988 | 0.9858 | n8 0.9893, but **n5 0.9531, n6 0.9834** | **−1 to −5% short/mid** |
| 16 | fail 0.131 | 0.1602 | 0.1543 | no-op |
| 17 | partial 0.584 | 0.5884 | 0.5874 | no-op |
| 18 | fail 0.249 | 0.2412 | 0.2378 | no-op |
| 19 | partial 0.795 | 0.7856 | 0.7744 | no-op (1.2 SE) |

At k=1 the SOLE exclusive coord is eval-load-bearing exactly in proportion to
the cure: zeroing it costs real accuracy at the two cures (s=14 −2.8% uniform
~3 SE; s=15 −1 to −5% concentrated at short/mid lengths — note its n=8 barely
moves while n=5/6 fall from 1.0000) and is a no-op at the partials and fails
(s=16/17/18/19, all |Δ| ≤ 1.2 SE). The k=1 fragility is downstream (NET-28),
and the k=1 CURE is eval-dependent on its single channel — a 1-dim lever that,
when the recurrence does manage to use it, must remain present at inference.

## The law

**THE-EXCLUSIVE-BOUNDARY-CHANNEL-IS-TRAINING-TIME-LOAD-BEARING + INTERNALIZATION-IS-PROPORTIONAL-TO-CURE-QUALITY.**

1. **At k=3 the exclusive block is (mostly) OPTIMIZATION-load-bearing.** The
   trained recovery is self-sufficient: removing the entire exclusive block at
   eval costs ≤0.3% scattered in 5/6 arms; removing any single coord costs 0%
   in all 6; signs never matter; magnitude is second-order. The reliability
   benefit of the k≥3 rule is realized as SELF-SUFFICIENT TRAINED DYNAMICS —
   BPTT-through-time, seeing an unambiguous boundary every EOS step, shapes
   W_hh/W_ih so the hidden-state depth-recovery no longer needs the exclusive
   input at inference.
2. **Internalization is SEED-HETEROGENEOUS (1/6 stay eval-dependent).** s=13
   built a recovery that still leans on the exclusive block at eval — as a
   magnitude-ensemble (zero3 → 0.70, scale0.1 → 0.97, zero1 → 1.0000, flip →
   no-op). Notably s=13 has the LARGEST exclusive coords of the six E=23 arms
   (|0.65–0.66| vs 0.53–0.60) — a possible magnitude→dependence trend, but n=6
   with one outlier: FLAGGED, not asserted. A single-seed "the exclusive dims
   don't matter at eval" claim would be wrong.
3. **At k=1 the sole exclusive coord is eval-load-bearing in proportion to the
   cure.** Zeroing it costs real accuracy where the recurrence internalized it
   (cures: −1 to −5%, significant) and is a no-op where it did not (partials/
   fails: |Δ| ≤ 1.2 SE). This CAUSALLY confirms NET-28: the k=1 failures never
   needed the coord (removal changes nothing), and even the k=1 cures hold a
   thinner margin — their recovery depends on the single channel remaining
   present at inference, unlike the (majority of) k=3 self-sufficient recoveries.
4. **The k=3 design rule is a TRAINING-TIME rule.** The exclusive dims are a
   boundary "teacher signal" for the optimizer; the redundancy they buy is
   realized in the weights, not held at the input. At inference, an internalized
   k=3 answer path does not need to re-serve the exclusive token.

**Mechanism statement (supported, causal at the eval level):** the exclusive-dim
ramp (NET-26/27/28) is a ramp of OPTIMIZER OPPORTUNITY. k=1 gives BPTT one
boundary direction to shape; the recurrence either fails to use it (failures,
where removal is a no-op) or internalizes it so thinly that the cure is
eval-dependent on the single channel (s=14/15). k=3 gives three independent
directions; BPTT (mostly) shapes a self-sufficient recovery that is robust to
the exclusive input being removed at inference (5/6), with occasional
solutions that keep a collective ensemble dependence (1/6, magnitude-
sensitive, sign-insensitive, 2-of-3-redundant).

## Verdict on the hypothesis

Prediction 2 (optimization-load-bearing) is the majority outcome at k=3 — but
NOT uniformly: 5/6 arms confirm it, 1/6 (s=13) shows a genuine collective
eval-load-bearingness. The k=1 arms resolve the interaction: eval-load-
bearingness of the boundary channel is proportional to how well the trained
recurrence internalized it (cures: significant cost; partials/fails: no-op).
The single cleanest statement: **at the k=3 cure, the exclusive boundary block
is a training-time device whose inference-time removal costs ≤0.3% in the
majority — and the k=1 fragility is causally confirmed to be downstream, since
removal of the sole coord is a no-op exactly where the model already failed.**

## Verification vs the network-loop barriers

- **(a) Circularity — clean.** Interventions are inference-only on SAME-SEED
  reproductions of NET-28 arms; the `ctl` baseline reproduces the published
  outcomes on fresh draws (nothing injected, nothing recovered). The
  interventions measure whether the trained dynamics USE the boundary input —
  a property of the trained solution, not of the hypothesis construction.
- **(b) Known-method-in-disguise — clean.** Input ablation is a standard tool,
  but the TARGET (the exclusive-dim boundary channel of a length-gen cure, and
  the internalization-proportional-to-cure finding) is the lab's own
  construction; Catalog re-checked — no package on causal boundary-token
  ablations of length-general recurrences (same family as NET-26/27/28 scans).
- **(c) Toy-scale — confronted.** Same carry task; the transferable statement
  is the design rule: train the final-step boundary with ≥3 exclusive dims and
  expect a self-sufficient (eval-boundary-robust) answer path in the majority.
  Real-scale transfer remains the frontier.
- **(d) Data leakage — clean.** Fresh draws per arm per intervention;
  teacher-forced; interventions never trained.
- **(e) Variance/reproducibility — the round's content.** The 6 E=23 cures
  show seed-heterogeneous internalization (5/6 self-sufficient, 1/6 ensemble-
  dependent) — reported as a distribution, NOT averaged into a false "uniformly
  self-sufficient" claim. The 6 E=21 arms show the monotone internalization
  gradient. Every arm is a byte-identical same-seed reproduction (exclusive
  coords reproduce NET-28 to 3 decimals), so the variance attaches to the
  published trained solutions. All Δ≥0.01 are ≥1 SE; the s=14 −2.8% is ~3 SE.
- **(f) Measurement — clean.** Interventions are exact parameter writes
  (zero/flip/scale), teacher-forced exact-match eval, ctl baselines reproduce
  published outcomes. SEs reported; no-ops defined as |Δ| ≤ 1.2 SE.
- **(g) Baseline fairness — strong.** Byte-identical cell across all 12 arms;
  each arm's `ctl` is its own within-arm baseline (the interventions are
  within-model, so no cross-arm confound); Part A vs Part B differ only in E
  (k=3 vs k=1) and intervention set.
- **(h) Practical relevance — a training-time design rule + a caution.** For a
  state-augmented answer path: give the final-step boundary ≥3 exclusive dims
  AT TRAIN TIME; the resulting recovery is (mostly) self-sufficient at
  inference — the exclusive token need not be re-served at eval. CAUTION: 1/6
  solutions remain eval-dependent on the boundary ensemble, so a single-seed
  ablation ("boundary doesn't matter at eval") is not trustworthy; and at k=1
  the cures genuinely need their single coord at inference.

## Notes for the coordinator

- **The headline:** at the k=3 cure the exclusive boundary block is mostly
  TRAINING-TIME load-bearing (5/6 arms survive complete removal at eval with
  ≤0.3% scattered cost); 1/6 (s=13) keeps a collective magnitude-ensemble
  dependence (zero3 → 0.70, scale0.1 → 0.97, zero1 → 1.0000, flip → no-op).
- **The k=1 resolution:** the sole exclusive coord is eval-load-bearing in
  proportion to the cure — significant cost at the cures (s=14 −2.8% ~3 SE;
  s=15 −1 to −5% at short/mid lengths) and no-op at the partials/fails (all
  |Δ| ≤ 1.2 SE). Causal confirmation that the k=1 failure was downstream.
- **Reproduction:** all 12 arms reproduced NET-28's trained exclusive coords to
  3 decimals and the ctl eval outcomes on fresh draws — interventions attach
  to the exact published solutions.
- **Numbers to quote:** E=23 zero3 n=8 full {1.0000, 0.9995, 0.9995, 1.0000,
  0.9971, 0.7041}; zero1 0% ×6; flip 0% ×6; scale0.1 {1.0×5, 0.9692}. E=21
  zero1 vs ctl: s=14 0.9717 vs 1.0000; s=15 n5 0.9531 vs 1.0000; s=16/17/18/19
  no-op.
- **Open questions (natural next rounds):** (1) the k=2 freeze test — is the
  E=22 (83% P(cure)) internalization INTERMEDIATE between k=1 and k=3 (would
  link the eval-dependence gradient to the P(cure) ramp); (2) is the
  magnitude→dependence trend real (s=13 has the largest coords — needs ~24 more
  E=23 arms); (3) REAL-SCALE TRANSFER — the k≥3 training-time rule applied to a
  real causal LM's final-step boundary, testing whether its answer path becomes
  eval-boundary-robust; (4) the pad384-vs-NET-24-hybrid parity check (a dense-
  EOS raw GRU should match the hybrid exactly) — still open.
- Scripts: /tmp/exp_net_eos_freeze.py (ALL_DONE_NET29). Log: /tmp/net29.log.

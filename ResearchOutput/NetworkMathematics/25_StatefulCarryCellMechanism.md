# The Stateful-Carry-Cell Cure Was the Dense Final Step — Mechanism Dissection of the Length-Gen Cure (NET-25)

**Program:** Network/LLM research lab — round-net-25 (performance axis; mechanism dissection of the NET-24 stateful-carry-cell cure)
**Date:** 2026-08-14
**Status:** Machine-verified (ALL_DONE_NET25, ALL_DONE_NET25_PAD, ALL_DONE_NET25_SWEEP, ALL_DONE_NET25_EOS). LSB-first base-10 a+b=c, plain n=5 training, dm-scale GRU carry cells, bs=256, 12000 AdamW steps, lr 1e-3, eval n=5/6/7/8 (2048 fresh draws, teacher-forced, full/per/per-position). Twenty-plus runs: the 6-arm dissection (capacity-matched raw GRU, untrained-projection GRU, position-augmented GRU), a pad-to-384 control, a 13-seed variance sweep (raw20-192 × 7, proj384 × 5), and an EOS-density control (same-weights, dense vs 20-d EOS; pad384 × 4, pad384-zeroEOS × 2).

## Hypothesis and statement

NET-24 resolved the five-axis carry-chain length wall with the FIRST positive cure:
a GRU carry cell over the walled transformer encoder's per-column features computes
n=5/6/7/8 at full=1.0000 (both seeds), and RAW-STATE-ALONE-HITS-A-STATE-HORIZON —
the textbook pure GRU on raw one-hot columns masters n=5 but degrades at n=8
(0.08–0.70). NET-24's conclusion: the cure needs BOTH state AND the encoder's
content-rich column features, with a flagged capacity confound (pure GRU 125k
params vs hybrid 782k).

This round DISSECTS the cure — which ingredient of the answer-side features is
load-bearing? Three mutually-exclusive hypotheses:

- **H1 CAPACITY.** The raw-GRU state-horizon is a capacity artifact (125k too small).
  Test: capacity-matched raw GRU, hidden=384 (~471k params — MORE than the
  hybrid's 333k GRU cell), same raw one-hot inputs.
- **H2 REPRESENTATION.** The one-hot 20-dim input is the problem; high-dimensional
  well-separated features cure it, and the encoder's LEARNING is not load-bearing.
  Test: untrained fixed random 384-dim projection of the same one-hots.
- **H3 POSITION.** The encoder's smooth RoPE-style step-position signal is the
  load-bearing ingredient. Test: one-hots + an 8-dim RoPE-schedule sinusoid of the
  step index.

The round then grew two follow-up arms forced by barrier (e): a pad-to-384 control
(is it dimension or dense geometry?) and a 13-seed variance sweep; the sweep
provoked an EOS-density control that overturned the framing.

## Setup

All arms share the task (plain n=5, LSB-first, per-digit CE), budget (bs=256,
12000 steps, lr 1e-3), and eval. Reuses GRUCarry and make_cols from the NET-24
script (imported, unmodified).

- **raw20-192** (NET-24 baseline, B=125,214): GRUCell(20→192), one-hot digit
  columns, learned 20-d EOS vector.
- **cap384-raw** (B=471,582): same raw one-hots but GRUCell(20→384) — 3.7× the
  pure-GRU capacity.
- **proj384** (B=335,242): GRUCell(384→192); input = UNTRAINED fixed random
  384-d projection of the one-hots (seeded; digit identity only, no context,
  no position, no learning).
- **pos28** (B=129,830): GRUCell(28→192); input = 20 one-hot + 8-d RoPE-schedule
  sinusoid of the step index i (defined for all i, the position analog).
- **pad384** (B=335,242): GRUCell(384→192); input = one-hots zero-padded to 384-d
  (364 dead columns); EOS = dense learned 384-d vector. *Functionally raw20 at
  every digit column; the EOS input is the only live difference.*
- **pad384-zeroEOS** (B=334,878): identical to pad384 EXCEPT the EOS input is
  zero-padded to 20-d. For the same seed the two models draw IDENTICAL
  GRUCell/head weights (construction order matches; only the EOS parameter count
  differs) — an airtight same-weights control with the EOS input dimension as the
  only variable.

## Results

All numbers: full (all n+1 digits exact) / per. n=8 full is the length-gen bar
(chance 1e-9).

### The 6-arm dissection (original hypotheses)

| Arm | n=6 | n=7 | n=8 full | params |
|---|---|---|---|---|
| cap384-raw s=0 | 0.7109 / 0.9587 | 0.0684 / 0.8292 | 0.0078 / 0.7204 | 471,582 |
| cap384-raw s=1 | 0.6260 / 0.9451 | 0.0596 / 0.8295 | 0.0063 / 0.7437 | 471,582 |
| proj384 s=0 | 1.0000 / 1.0000 | 1.0000 / 1.0000 | **1.0000 / 1.0000** | 335,242 |
| proj384 s=1 | 1.0000 / 1.0000 | 1.0000 / 1.0000 | **1.0000 / 1.0000** | 335,242 |
| pos28 s=0 | 0.6587 / 0.9471 | 0.0640 / 0.8237 | 0.0049 / 0.7284 | 129,830 |
| pos28 s=1 | 0.3677 / 0.9072 | 0.0371 / 0.7990 | 0.0049 / 0.7116 | 129,830 |

**H1 CAPACITY REFUTED** (both seeds): 471k-param raw GRU fails like the 125k one
(n=8 full 0.006–0.008; if anything the state-horizon is sharper and more
deterministic at scale). **H3 POSITION REFUTED** (both seeds): the position
sinusoid adds nothing (n=8 full 0.0049). **H2 in its strong form REFUTED / weak
form CONFIRMED**: the untrained random projection cures (n=8 full 1.0000, both
seeds) — learned encoder content is not needed.

### The pad-384 control (forced by the GRUCell init check)

PyTorch's GRUCell inits ALL params from U(±1/sqrt(hidden)) regardless of in_dim
(verified: max-abs 0.0722 = 1/sqrt(192) for in_dim 20/28/384), so the pad control
does NOT change init scale — it isolates raw dimension. Result: pad384 s=0/s=1
both n=8 full **1.0000**. But a zero-padded one-hot is functionally a 20-input
GRU, so this is not an architectural-capacity result; it flagged that the
outcome depends on something subtler than input dimension (barrier e).

### The variance sweep (barrier e — seed distributions)

| Condition | n=8 full per seed | cure rate |
|---|---|---|
| raw20-192 | s0 0.0806, s1 0.6997 (NET-24), s2 0.0103, s3 0.0063, s4 0.0093, s5 0.0020, s6 0.0132 | **0/7** |
| proj384 | s0–s4 all 1.0000 | **5/5** |

raw20's state-horizon is real but seed-variance-heavy (n=8 full spans 0.002–0.70,
mode ~0.01; NET-24's 2-seed law undersampled a wide distribution, but the
conclusion — never reaches 1.0 — holds at 0/7). proj384's cure is 100% across 5
seeds.

### The EOS-density control (the decisive arm)

pad384 (dense 384-d EOS) vs pad384-zeroEOS (20-d EOS) — **same seed, identical
GRUCell/head weights; the EOS input dimension is the ONLY difference.**

| Arm | n=6 | n=7 | n=8 full | per |
|---|---|---|---|---|
| pad384 s=0 | 1.0000 | 1.0000 | **1.0000** | 1.0000 |
| pad384 s=1 | 1.0000 | 1.0000 | **1.0000** | 1.0000 |
| pad384 s=2 | 1.0000 | 1.0000 | **1.0000** | 1.0000 |
| pad384 s=3 | 1.0000 | 1.0000 | **1.0000** | 1.0000 |
| pad384-zeroEOS s=0 | 1.0000 | 0.9956 / 0.9995 | 0.7441 / 0.9712 | pos `[1,1,1,1,1,1, 0.997, 0.745, 0.999]` |
| pad384-zeroEOS s=1 | 0.9756 / 0.9965 | 0.2500 / 0.9035 | 0.0259 / 0.8084 | raw-range |

The dense-EOS condition is 4/4 at 1.0000; its 20-d-EOS twin — identical weights —
lands inside the raw20 distribution (0.026–0.744). **The EOS input dimension
alone flips the cure.**

## The law

**DENSE-FINAL-STEP-IS-THE-CURE — THE-STATEFUL-CARRY-CELL-CURE-IS-THE-FINAL-
STEP-INPUT-RICHNESS. THE-ENCODER'S-CONTENT-WAS-NOT-THE-LOAD-BEARING-INGREDIENT.**

1. **THE CURE IS THE DENSE LEARNED EOS INPUT, NOT THE ENCODER FEATURES.** The
   NET-24 hybrid cure (and this round's proj384/pad384 arms) is driven by the
   FINAL (carry-emission) step's input being a dense, high-dimensional, learned
   vector. Same-seed, identical-weights control: dense 384-d EOS → n=8 full
   1.0000 (4/4); 20-d EOS → 0.026–0.744 (raw20 range, 0/2). No other variable
   differs. NET-24's "content-rich column features" interpretation is corrected:
   the encoder's learned content, context, and position structure are NOT
   load-bearing for the cure.
2. **THE DIGIT-PATH INPUT CAN BE RAW.** pad384's digit columns are functionally
   raw 20-d one-hots (364 dead padding dims) and it still cures 4/4. proj384
   (dense everywhere) cures 5/5. So the dense EOS is SUFFICIENT; no digit-path
   enrichment is required. The NET-24 pure-GRU failure was its 20-d EOS, not its
   20-d digit inputs.
3. **THE RAW20 STATE-HORIZON IS REAL BUT SEED-VARIANCE-HEAVY.** 0/7 seeds reach
   n=8 full 1.0000 (0.002–0.70, mode ~0.01). NET-24's 2-seed observation
   (0.08/0.70) undersampled a wide distribution, but the qualitative law — a
   20-d-EOS GRU does not length-generalize to 1.0 — holds at 0/7. The effect is
   distributional, not a hard wall.
4. **EOS RICHNESS NEEDS DIMENSION FAR ABOVE THE DIGIT COUNT.** pos28's EOS is a
   learned 28-d vector and still fails (0.0049, both seeds) — so the effect is
   not "any trained EOS"; 384-d works, 20-d and 28-d fail. The precise threshold
   between 28 and 384 is untested.
5. **THE CARRY TRANSITION WAS ALWAYS LENGTH-GENERAL; THE READOUT WAS THE FRAGILE
   PART.** In failing arms the final-carry column is 0.86–0.99 at n=8 while the
   mid-unroll digit columns collapse (cascade shape). The dense EOS shapes the
   recurrent weights (via backprop through the final step) so the digit readout
   stays in-distribution at deep unrolls.

**Mechanism hypothesis (flagged, not proven):** the EOS step — where the carry is
emitted — is the boundary of the unrolled computation. A rich dense input there
conditions the final-step hidden update and its backward Jacobian; backprop-
through-time from the EOS step shapes W_hh/W_ih so hidden states at beyond-
training depths stay in a generalizing regime, keeping the linear digit readout
in-distribution. A poor (20/28-d) EOS leaves the recurrent weights shaped without
the boundary constraint, and the readout drifts OOD at depth.

## Verdict on the hypothesis

**None of the three original hypotheses survives; the true lever is the final-step
input richness.** H1 CAPACITY refuted (both seeds, 471k raw still fails), H3
POSITION refuted (both seeds, 28-d EOS+position still fails), H2-strong (learned
features load-bearing) refuted (untrained projection AND raw one-hots both cure
with a dense EOS). The dissection is a correction to NET-24: the walled
transformer's encoder is length-general-usable, but the answer-side STATE cell
needed a dense final step all along — the encoder's content-rich features were a
sufficient-but-not-necessary vehicle for it.

## Verification vs the network-loop barriers

- **(a) Circularity — clean.** Eval n=6/7/8 are fresh draws never in training; all
  arms train n=5 only. The dense-EOS control is a same-weights comparison (the
  EOS is the only difference), so the effect cannot be data or eval leakage.
- **(b) Known-method-in-disguise — the dissection is the contribution.** "GRU
  needs a dense boundary input" is not a textbook result; the controlled
  decomposition (capacity/representation/position all refuted; EOS-density
  confirmed by an identical-weights control) is new. Catalog scan at launch: no
  prior controlled length-gen cure or mechanism dissection on a carry task.
- **(c) Toy-scale — confronted.** Toy task at dm-scale; the wall is the established
  NET-19/21/22/23/24 phenomenon, and this round delivers a controlled mechanism
  at the same scale/budget.
- **(d) Data leakage — clean.** Fresh random batches; no beyond-max example
  trained; teacher-forced eval on inputs only.
- **(e) Variance/reproducibility — the central improvement of the round.** The
  barrier bit HARD: proj384/pad384's initial 2-seed "cures" were re-measured at
  5/5 and 4/4 (robust), and raw20's state-horizon at 0/7 (robust but wide: 0.002–
  0.70). NET-24's 2-seed claims are here corrected to distributions. The dense-EOS
  control is seed-controlled (same-seed identical weights), immune to draw
  variance. Threshold (28–384) untested — flagged.
- **(f) Measurement — clean.** Teacher-forced exact-match full/per/per-position;
  the per-position signature distinguishes the cascade collapse (raw20) from the
  thin single-column dip (pad384-zeroEOS s=0).
- **(g) Baseline fairness — strong.** raw20-192 is the byte-identical NET-24
  baseline; every arm shares task/budget/eval. The control arms differ from their
  twins by exactly one architectural variable.
- **(h) Practical relevance — mechanism-level correction with a design lesson.**
  For length-general sequential computation in state-augmented answer paths, the
  final step's input pathway must be rich; boundary-condition richness — not
  feature content, capacity, or position — is what keeps recurrent readouts
  in-distribution at depth. Directs real-LM recurrence/state-space work toward
  well-conditioned boundary inputs over ever-richer features.

## Notes for the coordinator

- **Correction to NET-24, not a confirmation.** The cure is real (0→1) but its
  mechanism is the dense final step, not the encoder's learned features. NET-24's
  law #4 ("content-rich column features") and RAW-STATE-ALONE-HITS-A-STATE-HORIZON
  are both refined: the pure GRU failed because its EOS was 20-d; a dense-EOS raw
  GRU cures with NO encoder at all.
- **Airtight control:** pad384 vs pad384-zeroEOS share identical GRUCell/head
  weights for the same seed (construction order matches; only the EOS parameter
  count differs) — the EOS input dimension alone flips n=8 full 0.026–0.744 →
  1.0000. This is the round's strongest single result.
- **New distributional facts:** raw20-192's n=8 full spans 0.002–0.70 over 7
  seeds (0/7 at 1.0); proj384 is 5/5 at 1.0000; pad384 is 4/4 at 1.0000. Any
  future claim about the state-horizon or its cure should quote these
  distributions, not single seeds.
- **Open questions (natural next rounds):** (1) the EOS-dimension threshold
  between 28 and 384 (e.g., 64/96/128-d EOS); (2) does the dense-EOS law transfer
  to the REAL causal LM (the NET-24 frontier — recurrence/state-space-augmented
  answer paths); (3) does a dense-EOS GRU on raw one-hots match the NET-24 hybrid
  exactly (it should, per finding 2) — an explicit parity check.
- Scripts: /tmp/exp_net_stateful_ctrl.py (dissection, ALL_DONE_NET25),
  /tmp/exp_net_stateful_pad.py (pad control, ALL_DONE_NET25_PAD),
  /tmp/exp_net_stateful_sweep.py (variance, ALL_DONE_NET25_SWEEP),
  /tmp/exp_net_stateful_eosctrl.py (EOS control, ALL_DONE_NET25_EOS).
  Logs: /tmp/net25.log, /tmp/net25_pad.log, /tmp/net25_sweep.log, /tmp/net25_eos.log.

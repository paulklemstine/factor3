# RoPE Does Not Unlock Length-General Carry: The Wall Survives the Position-Scheme Test and the Pos-Embedding Extrapolation Caveat Is Retired (NET-23)

**Program:** Network/LLM research lab — round-net-23 (performance axis; the position-representation test of the carry-chain length wall)
**Date:** 2026-08-14
**Status:** Machine-verified (ALL_DONE_NET23). LSB-first base-10 addition, dm=192 (untied head), bs=256, 12000 AdamW steps, d=1; arms: absolute-pos control (s=0) + RoPE (rotary positions) s=0, s=1. Beyond-max eval n=6/7/8 (full chance 1e-7/1e-8/1e-9), 2048 fresh draws each.

## Hypothesis and statement

NET-4/5/19/21/22 established the **carry-chain length wall**: a transformer
trained on n-digit addition masters its training length (full=1.0000) but
length-generalizes to n+1/n+2 at pure chance — at every depth (d=1/2/4), scale
(dm up to 192), schedule (plain, curriculum, mixed), and task-remodeling
(scratchpad/CoT with explicit carry targets). NET-22's sharpest diagnostic,
GIVEN-CARRIES-STILL-FAIL, proved the wall is a **position-specific
answer-COMPUTATION failure**: feeding the true carries for n=6/7/8 still yields
0.0000 answers.

But EVERY length-gen eval in the program shared one caveat: **learned ABSOLUTE
position embeddings with pos-emb EXTRAPOLATION.** Training on n=5 sees
positions 0..24; beyond-max eval at n=8 uses positions 25..36, which are in the
CTX=40 table but are **UNTRAINED table entries** with no training-consistent
structure. NET-22's "position-specific answer function" could be an artifact of
firing answer circuits at random-init positions — the model never saw
position-consistent structure there, so of course the position-parameterized
algorithm does not run.

This round tests the position-scheme axis directly with **RoPE (rotary
position embeddings)**: rotation structure applied to q/k from a sinusoid
schedule, with NO position table. Every position — including beyond-max — is a
principled, smooth continuation of the trained positions (the relative-angle
structure 10000^(-2i/48) extrapolates identically). If the wall is pos-emb
extrapolation, RoPE removes the confound.

Two horns:

1. **Positive cure:** with RoPE, the position-specific answer function
   transfers beyond trained length → length-gen to n=6/7/8 — the FIRST positive
   cure for the wall, and evidence the entire length-gen line was confounded by
   absolute pos-emb extrapolation.
2. **Negative:** RoPE masters n=5 (in-range sanity) yet n=6/7/8 stay at chance
   → the wall is a GENUINE fixed-depth expressivity limit, position-scheme-
   independent; the pos-emb caveat shared by the whole length-gen line is
   RETIRED; recurrence (a stateful carry cell) is the sole remaining
   architecture lever.

## Setup

Architecture byte-identical to NET-19/21/22 (pre-LN transformer, dm=192, 4
heads, d_mlp=4·dm, UNTIED readout, per-digit cross-entropy, LSB-first base-10
a+b=c, bs=256, 12000 AdamW steps, lr 1e-3). **Single deviation, shared by all
arms:** the RoPE arm replaces the learned pos table with rotary positions
(head_dim 48; inv_freq = 10000^(-2i/48), i=0..23; standard pair-tiling
broadcast so dimensions (j, j+24) rotate by the same angle). The `rope` flag is
the ONLY difference between arms: same task, same arch, same budget, same eval.
VOCAB=13, CTX=40 (relevant only to the abs-pos control's table; the RoPE arm
has no table and is position-limit-free).

Arms (all d=1, plain n=5 task, dm=192, untied, bs=256, 12000 steps):
- **abs-pos (s=0)** — in-run wall reference (expect: master n=5, n=6/7/8
  chance; the exact NET-21/22 control-E trajectory).
- **rope (s=0, s=1)** — the position-scheme test, two seeds.

Eval at n=5/6/7/8, teacher-forced, 2048 fresh held-out draws each, with
per-output-position accuracy (LSB-first: position 0 = ones digit, position n =
final carry / MSB answer digit).

## Results

### abs-pos control (s=0) — the wall reproduces in-run

Masters n=5 (full=1.0000, per-position all 1.000) with the characteristic late
jump (full 0.002→0.98 between st=3000–6000). Beyond-max: **n=6/7/8 full=0.0000**,
per=0.1136/0.1285/0.0993 ≈ digit floor. MSB (final-carry) position at n=6/7/8:
0.198/0.307/0.109 — near or below chance; the untrained pos-table entries fire
the MSB circuit incorrectly. Clean reference.

### rope s=0 — masters n=5 faster than any arm, beyond-max still at chance

RoPE reaches **full=1.0000/per=1.0000 by step 1000** and holds flat — the
fastest in-range mastery of the three arms (abs-pos took until st≈6000). The
rotary scheme clearly helps fixed-length learning. Beyond-max: **n=6/7/8
full=0.0000**, per=0.1658/0.1559/0.1458. Interior digits at the 0.1 floor.
**But the MSB position transfers: 0.587/0.571/0.565** — above the
P(carry-out=1)≈0.5 marginal that random n-digit operands produce, and far above
the abs-pos control's 0.11–0.31. RoPE's smooth positions let the model learn
the correct final-carry prior; the abs-pos table fired the untrained entry
wrongly.

### rope s=1 — a NEW dissociation: RoPE in-range mastery is NOT seed-robust

Seed 1 does NOT master n=5: full=0.1040 / per=0.8507 at the end, **permanently
stuck in the carry-dissociation plateau** (flat full≈0.10 / per≈0.85 from
st=5000 to st=11000, no stochastic escape within the 12000-step budget). The
per-position n=5 read is striking: `[0.107, 1.000, 1.000, 1.000, 1.000, 1.000]`
— the model computes the 4 interior columns AND the final carry perfectly, and
fails ONLY the least-significant digit (position 0). Beyond-max: n=6/7/8
full=0.0000, per=0.1556/0.1567/0.1126.

## The law

**ROPE-DOES-NOT-UNLOCK-LENGTH-GEN + THE-POS-EMB-CAVEAT-IS-RETIRED +
ROPE-DISSOCIATION-IS-SEED-DEPENDENT.**

1. **RoPE does not unlock length-general carry.** A d=1 transformer with
   smooth, extrapolatable, training-consistent rotary positions masters n=5
   (cleanly, in the s=0 seed, by step 1000) yet computes full=0.0000 at
   n=6/7/8. The wall is NOT a learned-absolute-position-extrapolation artifact:
   it reproduces with a position scheme that has no table, no untrained
   entries, and a principled continuation beyond trained length. The caveat
   that has dogged every length-gen eval since NET-4 — "beyond-max positions
   are untrained table entries" — is RETIRED.
2. **NEW — the FINAL-CARRY MARGINAL transfers with RoPE even though the
   computation does not.** At n=6/7/8 the MSB position scores 0.565–0.587
   (matching the P(carry-out≈1)≈0.5 prior over random n-digit operands) versus
   0.109–0.307 for the abs-pos control. RoPE's extrapolated positions carry
   training-consistent structure into the MSB slot, so the model applies its
   learned final-carry DISTRIBUTION; it still cannot COMPUTE the carry. The
   clearest separation yet between "statistical prior transfers" and "algorithm
   transfers".
3. **NEW — RoPE in-range mastery is seed-dependent, and the dissociation is a
   one-column failure.** Same hyperparameters: s=0 perfect by st=1000; s=1
   permanently dissociated (per 0.85 / full 0.10). The plateau is the NET-4/5
   correlated-error regime, but its per-position shape is unusual: the model is
   perfect on every column except the least-significant digit (0.107). This is
   NOT the classic carry-propagation dissociation (where a wrong LSB carry
   cascades and everything downstream is correlated-wrong) — here the downstream
   columns are all 1.000, i.e. the model reads carries correctly but the LSB
   digit computation is systematically wrong. Single-seed observation; the
   mechanism is open.

## Verdict on the hypothesis

**Negative (RoPE-is-not-the-cure) — the positive horn is REFUTED.** The wall
survives the position-representation test. Combined with NET-4/5/19/21/22, the
carry-chain length wall is now characterized on FIVE axes — depth, scale,
schedule, task-remodeling (scratchpad), and position representation (RoPE) —
all negative for length-general composition. The surviving mechanism picture
tightens further: the answer function is length-specific not merely because the
positions were random beyond max, but because the fixed-depth computation
itself is trained to a length-5 attractor that a smooth positional continuation
does not generalize. The final carry's DISTRIBUTION transfers; its VALUE does
not. Remaining levers that change the state rather than the position scheme:
**recurrence / a stateful carry cell** (the only device with a length-general
state), or an explicit length-parameterized readout. RoPE (this round) and
scratchpad (NET-22) are both CLOSED.

## Verification vs the network-loop barriers

- **(a) Circularity — clean.** Fresh held-out draws (2048/batch) over the 10^n
  pair space; test lengths 6/7/8 never appear in training (train max n=5); the
  eval is teacher-forced on the INPUT only (answers are read off the final head,
  no autoregressive contamination). RoPE is applied identically at train and
  eval positions — no scheme is injected only at test.
- **(b) Known-method-in-disguise — clean.** RoPE is THE mature position scheme
  (rotary, all frontier LLMs), but the test is the controlled NEGATIVE: rotary
  positions do not cure length-gen carry composition in this controlled case.
  The NEW content is the pos-emb-caveat RETIREMENT (the first time any length-gen
  eval runs without a position table) and the MSB-marginal-transfer / one-column-
  dissociation observations. Catalog scan: no controlled RoPE-vs-length-wall
  result on a carry task (the one prior entry found is a theory paper on
  attention expressive power + positional encoding, not an empirical cure).
- **(c) Toy-scale — confronted.** Task is toy-scale, but the wall is established
  at dm=192 (4.5–18× params, NET-19); this round tests the position axis at the
  same scale with the identical budget. Mechanism-level finding, as with
  NET-19/21/22.
- **(d) Data leakage — clean.** Fresh random batches each train/eval step; no
  beyond-max example is ever trained; RoPE frequencies are fixed constants (no
  fitting to test positions).
- **(e) Variance/reproducibility — PARTIAL, honest caveat.** 2 RoPE seeds (s=0,
  s=1) + 1 abs-pos control. The decisive reading is stark (n=6/7/8 full=0.0000
  in both RoPE seeds). The seeds DIVERGE on in-range mastery (s=0 perfect, s=1
  dissociated), which is itself a finding (finding 3) but makes the "RoPE
  masters n=5 cleanly" framing a 1-seed statement — the beyond-max verdict does
  not depend on it. A third RoPE seed (s=2) is the natural strengthening.
- **(f) Measurement — clean, one noted caveat.** Teacher-forced eval at fresh
  draws; per-position accuracy isolates the MSB/column structure; full-vs-per
  separates exact from digit-level. The RoPE eval at n=8 (seq 27) exceeds no
  table — the RoPE arm has no position limit, so the abs-pos control is the
  only arm where CTX=40 caps eval (n=8 needs 27 positions, fits). The one-column
  dissociation of s=1 is a single-seed per-position observation.
- **(g) Baseline fairness — strong.** In-run abs-pos control with IDENTICAL
  architecture and budget, differing ONLY by the position scheme (the `rope`
  flag). The control reproduces the exact NET-21/22 trajectory (master n=5,
  beyond-max chance), so the RoPE arms are compared against the true wall
  reference, not a moved goalpost.
- **(h) Practical relevance — honest negative with the right next move.**
  RoPE is the position scheme used by essentially all modern LLMs; the result
  says a production position scheme does not, by itself, confer length-general
  algorithm composition on sequential arithmetic — the fixed-depth answer
  function is length-attractor-bound regardless of how positions are encoded.
  Do NOT invest in position-scheme-only fixes for length-general arithmetic.
  The load-bearing lever changes the STATE: recurrence / a stateful carry cell.

## Notes for the coordinator

- The length wall is now characterized from FIVE angles: depth (NET-4/5/19),
  scale (NET-19), schedule (NET-21), task-remodeling (NET-22), and POSITION
  REPRESENTATION (this round) — all robustly negative. Every length-gen caveat
  that survived NET-22 is now retired: scratchpad is closed (NET-22), position
  encoding is closed (this round). The surviving lever list is down to:
  recurrence / stateful carry cell, or an explicit length-parameterized readout.
- The NEW content beyond the negative: (1) THE-POS-EMB-CAVEAT-IS-RETIRED — the
  first length-gen eval in the program with no position table; the wall
  reproduces with smooth extrapolatable rotary positions; (2) the MSB/final-
  carry MARGINAL transfers (0.565–0.587 ≈ 0.5 prior) while the computation does
  not — statistical prior vs algorithm transfer cleanly separated; (3)
  ROPE-DISSOCIATION-IS-SEED-DEPENDENT with a one-column per-position shape
  (interior + final-carry columns perfect, LSB digit alone at 0.107) — a new
  flavor of the dissociation regime, distinct from NET-4/5's carry-cascade
  shape, single-seed.
- RoPE learned in-range FASTER than the pos table (s=0 perfect at st=1000 vs
  abs-pos st≈6000). If one only measured in-range speed, RoPE looks like a
  clear win; the beyond-max test shows the win is confined to the trained
  length. A caution for the common "RoPE improves length generalization"
  framing: it improves IN-RANGE learning speed and the beyond-max MARGINAL,
  not beyond-max composition.
- Script: /tmp/exp_net_rope.py (ALL_DONE_NET23). Log: /tmp/net23.log.

# Scratchpad Does Not Unlock Length-General Carry: Explicit Carry Targets Change Mastery Dynamics but Not the Length Wall (NET-22)

**Program:** Network/LLM research lab — round-net-22 (performance axis; the task-remodeling test of the carry-chain length wall)
**Date:** 2026-08-14
**Status:** Machine-verified (ALL_DONE + ALL_DONE_D2). LSB-first base-10 addition, dm=192 (untied head), bs=256, 12000 steps; scratchpad arms at d=1 and d=2, seeds 0/1 each; plain controls at d=1 and d=2 (seed 0). Beyond-max eval n=6/7/8 (full chance 1e-7/1e-8/1e-9).

## Hypothesis and statement

NET-4/5/19/21 established the **carry-chain length wall**: a transformer
trained on n-digit addition masters its training length (full=1.0000) but
length-generalizes to n+1/n+2 at pure chance — at every depth (d=1/2/4), every
scale (up to dm=192), and every training schedule (plain, curriculum, mixed).
NET-4's decomposable-error analysis attributed the wall to **credit
assignment**: the sequential carry dependency (carry_i → carry_{i+1}) receives
no per-step gradient credit, so the optimizer converges to a length-specific
attractor. NET-21 named **scratchpad/CoT intermediate tokens** as the top
surviving lever ("change the task, not the schedule").

This round tests the sharpest implication of the credit-assignment account: if
we EXPOSE the carry state as explicit per-column targets (a scratchpad), the
carry chain gets direct per-step credit.

Two horns:

1. **Positive cure:** with per-column carry targets, the model learns a
   length-GENERAL carry rule and length-generates to n=6/7/8 — the FIRST
   positive cure for length-gen; the wall was a credit problem all along.
2. **Negative:** even with explicit per-carry targets (teacher-forced) and a
   fully AUTOREGRESSIVE eval (the model generates its own carries, no teacher
   forcing), beyond-max stays at chance → the wall is an EXPRESSIVITY bound on
   the fixed-depth answer function, not a credit problem.

## Setup

Architecture byte-identical to NET-19/21 (pre-LN transformer, dm=192, 4 heads,
d_mlp=4·dm, UNTIED readout, per-digit cross-entropy, LSB-first base-10 a+b=c,
bs=256, 12000 AdamW steps, lr 1e-3). **Two documented deviations, both shared
by every arm:** (1) VOCAB enlarged 12→14 with `SC`=13 and `GO`=12 moved to a
dedicated token; (2) positional-embedding table CTX=40 so the n=8 scratchpad
sequence (4n+5=37 positions) fits.

**Scratchpad task** (train and eval, target length T=4n+5):

```
input: a_n..a_1 '+' b_n..b_1 '='   (positions 0..2n+1, P=2n+2)
  SC   c_1 c_2 ... c_n   GO   s_1 s_2 ... s_n c_n
```
where c_i = carry-out of column i (c_i=(a_i+b_i+c_{i-1})//10), s_i =
(a_i+b_i+c_{i-1})%10, c_n = the final carry = most-significant answer digit.
The n carry tokens and the n+1 answer digits are all teacher-forced targets at
train time; the `GO` is a structural separator (trained, not scored in evals).

**Evals** (fresh held-out draws, 2048/batch, at n=5/6/7/8):
- **auto** = FULLY AUTOREGRESSIVE (the headline length-gen test): the model
  generates its own n carries one token at a time, emits the structural `GO`,
  then generates its n+1 answer digits. No teacher forcing anywhere — a
  length-general carry rule is required, not memory.
- **given-carries** = diagnostic: the model is FED the TRUE carries and only
  generates the answers. This isolates answer-COMPUTATION failure (beyond-max
  answers wrong even with perfect carries) from carry-GENERATION failure.
- Metrics separated per region: answer full/per (chance 10^-(n+1) / 0.1) and
  carry full/per (chance 0.5^n / 0.5).

Arms (dm=192, untied, bs=256, 12000 steps):
- **d=1:** plain n=5 control (s=0); scratchpad n=5 (s=0, s=1).
- **d=2:** plain n=5 control (s=0); scratchpad n=5 (s=0, s=1). The d=2 phase is
  the depth check — d=2 was NET-19's most stable depth and NET-21's
  curriculum-forgetting arm.

## Results

### d=1 — the scratchpad does not unlock length-gen (2 seeds)

**Control plain n=5 (s=0):** masters n=5 (full=1.0000, stable), n=6/7/8 all
0.0000 (per 0.106–0.116 ≈ digit floor). The wall reproduces in-run.

**Scratchpad s=0:** teacher-forced n=5 mastery is reached at st=1000
(full=1.0000, carry=1.0000) — then **COLLAPSES**: st=2000 full=0.008, then a
plateau at full≈0.25 / per≈0.87 for the remaining 9000 steps (carry=1.0000 —
the carries are still known; the answer chain fails). Final auto: **n=6/7/8 all
0.0000** (per 0.130–0.143). Carry generation at n=6/7/8: carry_full≈0.0000,
carry_per 0.29–0.38 — **at/below the 0.5 chance per carry**.

**Scratchpad s=1:** teacher-forced 1.0000 held through st=3000, then a gentler
collapse to full≈0.74 / per≈0.96 from st=4000 on (carry≈1.0000). Final auto:
n=6/7/8 **all 0.0000** (per 0.144–0.160); carry_per 0.32–0.48 at/below chance.

### The decisive diagnostic — given-correct carries still fail (d=1)

For BOTH d=1 seeds, feeding the TRUE carries for n=6/7/8 yields **answer
full=0.0000** (per 0.133–0.164 ≈ digit floor). The model that knows every carry
exactly still cannot compute the n+1-digit answer. The wall is a
**position-specific answer-COMPUTATION failure**, not a carry-propagation
failure. The scratchpad gave the carry chain perfect per-step credit — and the
answer function still does not extend beyond trained length.

### d=2 — the depth check (2 seeds)

**Control plain n=5 (s=0):** does NOT master n=5 — full=0.1016 / per=0.8503
(stuck in the carry-dissociation correlated-error regime, single-seed
observation; NET-19/21's d=2 masters were n=6-trained or curriculum-trained).
Beyond-max n=6/7/8 all 0.0000 — the wall reproduces.

**Scratchpad d=2 s=0:** teacher-forced 1.0000 at st=1000, a single transient dip
to 0.80 at st=2000, then **recovered and held 1.0000 from st=5000 to the end**.
Final auto n=5: full=1.0000. Beyond-max: **n=6/7/8 all 0.0000** (per 0.123–0.135);
carry_per 0.23–0.43 at/below chance. Given-carries n=6/7/8: **all 0.0000**.

**Scratchpad d=2 s=1:** teacher-forced 1.0000 at st=1000–2000, a **violent
collapse to full=0.041 / per=0.570 at st=3000**, then recovered (0.949 at
st=4000) and **held 1.0000 from st=5000 to the end**. Final auto n=5:
full=1.0000. Beyond-max: **n=6/7/8 all 0.0000** (per 0.130–0.139); carry_per
0.26–0.40. Given-carries n=6/7/8: **all 0.0000**.

## The law

**SCRATCHPAD-DOES-NOT-UNLOCK-LENGTH-GEN + GIVEN-CARRIES-STILL-FAIL +
SCRATCHPAD-COLLAPSE-IS-DEPTH-CONDITIONED.**

1. **The scratchpad (per-column carry targets) does NOT unlock length-gen.** All
   four scratchpad arms (d=1×2 seeds, d=2×2 seeds) master their training length
   yet score 0.0000 at beyond-max n=6/7/8. The "task-remodeling" lever — NET-21's
   top surviving candidate — is CLOSED.
2. **Given-correct-carries still fails at both depths.** With every carry fed
   exactly, the n+1-digit answer is still 0.0000. The wall is not "the model
   can't propagate carries"; it is a position-specific answer-COMPUTATION wall on
   the fixed-depth answer function.
3. **NEW — scratchpad mastery is UNSTABLE, and the terminal state is
   depth-conditioned.** At d=1, BOTH seeds collapse permanently from 1.0000 into
   carry-dissociation plateaus (s=0 → full≈0.25; s=1 → full≈0.74) — the carries
   stay known (carry≈1.0000) while the answer chain fails, the exact
   correlated-error signature of NET-4/5/19/21. At d=2, BOTH seeds experience
   collapse episodes (s=0 dip to 0.80; s=1 crash to 0.041) but **RECOVER to
   stable 1.0000 and hold**. The plain d=1 control's mastery is rock-stable
   (1.0000 flat) — the instability is specific to the scratchpad objective. This
   is the mirror-image of NET-19's stochastic ESCAPE (dissociation→mastery):
   here it is mastery→dissociation→(d=2 only) re-mastery. Depth does not buy
   length-gen, but it buys STABILITY of scratchpad mastery.

## Verdict on the hypothesis

**Negative (scratchpad-is-not-the-cure) — the credit-assignment horn is
REFUTED.** Explicit per-column carry targets — the maximal form of scratchpad
supervision — do not produce length-general composition. The strongest evidence
is the given-carries diagnostic: a model that is handed every carry still
computes 0.0000 on beyond-max answers, so the wall is an expressivity/positional
property of the fixed-depth answer function, not a credit shortfall. The
surviving mechanism picture: length-gen requires an answer function that is
position-PARAMETERIZED (a procedure indexed by column/position), and the
fixed-depth, fixed-position-embedding transformer does not acquire one at any
depth, scale, schedule, or (now) task-remodeling tested. Remaining levers that
change the REPRESENTATION, not the supervision: recurrence (a stateful carry
cell — the only device with a length-general state), RoPE / alternative
position encoding (so beyond-max positions carry training-consistent structure),
or an explicit length-parameterized readout.

## Verification vs the network-loop barriers

- **(a) Circularity — clean.** Fresh held-out draws (2048/batch) over the 10^n
  pair space; the auto eval generates carries AND answers from the trained model
  (no teacher forcing); test lengths 6/7/8 never appear in training; `GO` is
  structural and not scored. The scratchpad targets are ground-truth carries
  computed from fresh draws, not an injected solution.
- **(b) Known-method-in-disguise — partial, acknowledged.** Scratchpad/CoT is
  THE mature recipe (chain-of-thought, all frontier LLMs). NEW = the controlled
  NEGATIVE (explicit carry supervision does not unlock beyond-trained-length gen
  on per-digit arithmetic) + the given-carries isolation of the answer wall +
  the depth-conditioned collapse. Catalog scan: no scratchpad-vs-length-wall
  controlled result on a carry task.
- **(c) Toy-scale — confronted.** Task is toy-scale, but the wall is established
  at dm=192 (4.5–18× params, NET-19); this round tests the task-remodeling axis
  at the same scale. Mechanism-level finding, as with NET-19/21.
- **(d) Data leakage — clean.** Fresh random batches each train/eval step; no
  beyond-max example (n=6/7/8) is ever trained (train max n=5); the
  given-carries diagnostic feeds TRUE carries from fresh data.
- **(e) Variance/reproducibility — PARTIAL, honest caveat.** 2 seeds (0,1) per
  depth in the scratchpad arm (4 arms); 1 seed per plain control. The decisive
  readings are stark (0.0000 vs 1.0000; plateaus stable over 7000–8000 steps).
  The depth-conditioning of the collapse is 2/2 at each depth — a third seed per
  depth is the natural strengthening. One plain control (d=2) landed in the
  dissociation regime (did not master n=5) — a single-seed observation that does
  not contradict NET-19/21's d=2 masters (different training length/schedule),
  and it sharpens the contrast: both d=2 scratchpad seeds ESCAPED it.
- **(f) Measurement — documented, with one shared caveat.** Teacher-forced
  monitor (carries + answers given) SEPARATED from the autoregressive eval (the
  honest test). Carry and answer regions scored independently (carry chance
  0.5^n / 0.5; answer chance 10^-(n+1) / 0.1). The given-carries diagnostic
  isolates answer-computation from carry-generation. **Caveat shared with the
  entire length-gen line:** positional-embedding extrapolation — training sees
  positions 0..24 (n=5), beyond-max eval uses positions up to 36, which are in
  the CTX=40 table but never trained; every remedy tested so far (depth, scale,
  schedule, scratchpad) fails WITH this extrapolation, and a RoPE-based rerun is
  one of the surviving levers. (Cosmetic: the RESULT-line `cper` column repeats
  the final n=8 value due to loop-variable reuse — per-length carry_per values
  are taken from the per-line log, which is the true measurement.)
- **(g) Baseline fairness — strong.** Same-run plain controls at BOTH depths,
  identical budget/arch/seed/CTX/VOCAB. The d=1 control masters n=5 cleanly
  (isolating the instability as scratchpad-specific); the d=2 control reproduces
  the wall. Given-carries is a within-arm control for the answer-vs-carry split.
- **(h) Practical relevance — honest negative with the right next move.**
  Scratchpad/CoT — the recipe universally recommended for LLM arithmetic
  length-generalization — does NOT produce length-general carry composition in
  this controlled case, even with perfect per-carry supervision. Do NOT invest
  in scratchpad-only fixes for length-general arithmetic. The wall is a
  positional/representational expressivity property; the load-bearing levers
  change the representation: recurrence (stateful carry cell), RoPE/position
  encoding, or a length-parameterized readout.

## Notes for the coordinator

- The length wall is now characterized from SIX angles: depth (NET-4/5/19),
  scale (NET-19), schedule (NET-21), and TASK-REMODELLING (this round) — all
  robustly negative. The mechanism is now sharpened to a positional
  expressivity claim, not a credit claim: given-correct-carries proves the
  answer function, not the carry propagation, is what fails beyond trained
  length.
- The NEW content beyond the negative: (1) GIVEN-CARRIES-STILL-FAIL (the answer
  wall is position-specific — the strongest diagnostic the program has produced
  on the wall); (2) SCRATCHPAD-COLLAPSE-IS-DEPTH-CONDITIONED (mastery instability
  at both depths; absorbing at d=1, restorative at d=2 — the mirror of NET-19's
  stochastic escape). Both are 2-seed phenomena.
- A second observation: scratchpad RESCUES in-range mastery at d=2 (both seeds
  1.0000 where the d=2 plain control stuck at 0.10) — scratchpad aids IN-RANGE
  credit assignment while leaving the BEYOND-range answer function untouched.
  Cleanest possible split between the two regimes.
- Surviving levers (explicitly named, in priority order): recurrence / stateful
  carry cell (architecture — length-general state), RoPE / position encoding
  (input representation — removes the shared pos-emb extrapolation caveat),
  explicit length-parameterized readout (output). NET-21's "scratchpad" lever is
  CLOSED at both depths.
- Script: /tmp/exp_net_scratchpad.py (ALL_DONE + ALL_DONE_D2). Log:
  /tmp/net22.log.

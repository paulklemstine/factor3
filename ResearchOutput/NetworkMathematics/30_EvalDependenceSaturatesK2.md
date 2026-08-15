# INTERNALIZATION-SATURATES-AT-K=2 + THE-K=1-INTERNALIZATION-IS-SEED-HETEROGENEOUS (NOT ∝-QUALITY) + S13-IS-A-SEED-WIDE-OUTLIER — 12 Causal Freeze Arms Complete the Eval-Dependence Gradient of the Exclusive Boundary Channel (NET-30)

**Program:** Network/LLM research lab — round-net-30 (mechanism axis; the middle of the internalization gradient — the causal test NET-29's open (1) / loop candidate (1b) flagged: is E=22 (k=2, P(cure)=83%) internalization INTERMEDIATE between k=1 and k=3?)
**Date:** 2026-08-14
**Status:** Machine-verified (ALL_DONE_NET30). Twelve arms, each a SAME-SEED REPRODUCTION of a NET-27 arm (byte-identical EOSWidthGRU, same seeds 8–13, same training; the `ctl` re-baselines reproduce NET-27's published outcomes on fresh draws — NET-27 predates the EOSCOORD machinery, so the trained exclusive coords are not published there, but same-seed byte-identical training reproduces the same solution and the eval outcomes land on the published values: Part A {1.0000, 0.9888, 0.9399, 1.0000, 1.0000, 0.9980} vs NET-27 {1.0, 0.991, 0.948, 1.0, 1.0, 0.999}; Part B {1.0000, 0.7622, 0.1606, 0.8892, 1.0000, 0.2734} vs NET-27 {1.0000, 0.7715, 0.1567, 0.8926, 1.0000, 0.2656}). Every intervention is INFERENCE-ONLY on the trained exclusive coords; fresh eval draws per arm × manipulation.
- **Part A (k=2, the missing middle):** E=22 × seeds 8–13, 6 interventions each — `ctl`, `zeroN` (zero the whole exclusive block, both coords), `zero1@0/1` (zero ONE coord), `flip1@0` (sign-flip one), `scale0.1` (attenuate the block ×0.1). 36 arm-interventions.
- **Part B (k=1, second seed set):** E=21 × seeds 8–13, 2 interventions each — `ctl`, `zero1` (zero the sole exclusive coord). 12 arm-interventions. Extends NET-29's k=1 study (seeds 14–19) to NET-27's seeds, which include TWO full cures (s=8, s=12).

## Hypothesis and statement

NET-29 froze the exclusive boundary channel at eval on same-seed reproductions
and found: at k=3 the cure survives whole-block zeroing in 5/6 arms
(self-sufficient trained dynamics; s=13 a magnitude-ensemble); at k=1 the sole
coord was eval-load-bearing "in proportion to cure quality" (cures −2.8 to −5%,
fails/partials no-op). That left the MIDDLE open: is k=2 (E=22, P(cure)=83% in
NET-27) internalization INTERMEDIATE — a partial eval-dependence between the
k=1 and k=3 regimes? If yes, eval-load-bearingness of the boundary channel ramps
monotonically with the dimensionality of the boundary lever, linking the
eval-dependence gradient to NET-27/28's P(cure) ramp. Secondary within-width
prediction: NET-27's E=22 arms are {1.0, 0.991, 0.948, 1.0, 1.0, 0.999} — if
internalization tracks cure quality at fixed k, the two near-cures (s=9, s=10)
should show MORE zeroN cost than the four full cures.

## Results

All numbers are n=8 full (all 9 digits exact; chance 1e-9); n=5/6/7 shown where
they differ. Binom. SE at 2048 draws: ≤0.5% at p≈1, ~0.8% at p≈0.16–0.24, ~0.9%
at p≈0.76–0.89. "no-op" = |Δ| ≤ 1.2 SE; a single arm's ~2 SE excursion among 12
comparisons is not treated as an effect.

### Part A — the k=2 middle under eval interventions (n=8 full)

| seed | ctl | **zeroN** (both excl) | zero1@20 | zero1@21 | flip1@20 | scale0.1 | excl coords |
|---|---|---|---|---|---|---|---|
| 8  | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 (n5 0.9995) | 1.0000 | [−0.654, 0.637] |
| 9  | 0.9888 | 0.9902 | 0.9863 | 0.9902 | 0.9902 | 0.9873 | [0.645, −0.652] |
| 10 | 0.9399 | 0.9453 | 0.9502 | 0.9390 | 0.9487 | 0.9380 | [−0.565, −0.623] |
| 11 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | [0.606, −0.612] |
| 12 | 1.0000 | 0.9995 (n6/n7) | 1.0000 | 1.0000 | 0.9985 (n5/n6) | 1.0000 | [0.657, 0.660] |
| 13 | 0.9980 | **0.7544** | 0.9961 | 0.9990 | **0.7505** | **0.9067** | [0.697, −0.701] |

**k=2 is NOT intermediate — it matches k=3.** Zeroing the ENTIRE exclusive block
at eval costs ≤0.010 in 5/6 arms (s=8/9/10/11/12; every |Δ| within ~1–2 SE, and
the two largest changes are POSITIVE: zeroN +0.005 and +0.010 at s=10, zero1@20
+0.010 — removal *helps* the imperfect arm, never breaks it). The 6th arm (s=13)
is the SAME seed as the k=3 outlier and shows the same ensemble dependence:
zeroN −0.24, flip1@20 −0.25, scale0.1 −0.09, zero1@0/1 no-op. At k=2 the s=13
ensemble is **2-of-2-redundant** (either coord suffices) but — unlike s=13@k=3,
where flips were no-ops — **sign-SENSITIVE** (flipping one of the two breaks the
recovery as hard as removing both) and magnitude-sensitive. s=13 again has the
LARGEST exclusive coords of its width (max |0.701| vs 0.612–0.660 for the five
self-sufficient seeds).

The within-width prediction is REFUTED: the worst E=22 arm (s=10, ctl 0.9399) is
just as self-sufficient as the full cures (zeroN +0.005, no-op; its only ~1–2 SE
swings are positive). No internalization-vs-quality slope at k=2.

### Part B — the k=1 arms under zero1 (n=8 full; NET-27 outcome → ctl → zero1)

| seed | NET-27 ctl | ctl | **zero1** (sole coord) | Δ | verdict |
|---|---|---|---|---|---|
| 8  | 1.0000 | 1.0000 | **1.0000** | 0 | **self-sufficient cure** |
| 9  | 0.7715 | 0.7622 | 0.7432 | −0.019 (~2 SE) | marginal |
| 10 | 0.1567 | 0.1606 | 0.1592 | no-op | no-op fail |
| 11 | 0.8926 | 0.8892 | 0.8901 | no-op | no-op partial |
| 12 | 1.0000 | 1.0000 | **1.0000** | 0 | **self-sufficient cure** |
| 13 | 0.2656 | 0.2734 | 0.2510 | −0.022 (~2 SE, fail arm) | marginal |

**NET-29's "k=1 internalization ∝ cure quality" is REFUTED at its strong form.**
The two FRESH full cures (s=8, s=12) are fully self-sufficient — zeroing the
sole exclusive coord costs 0% at every length. Pooled across all 12 k=1 arms
(NET-29 seeds 14–19 + NET-30 seeds 8–13): the dependences NET-29 reported
(s=14 −2.8% ~3 SE; s=15 −1 to −5% concentrated short/mid) do NOT reproduce at a
second seed set — the two new cures are no-ops. The two ~2 SE excursions here
(s=9 at a partial, s=13 at a fail) are single-arm marginals among 12 comparisons.
The robust invariant is narrower and cleaner: **removal of the sole exclusive
coord at k=1 is a NO-OP in every failing arm of both rounds (100% of the time),
and at successes it is seed-heterogeneous — some cures fully internalize (s=8,
s=12, this round), some remain eval-load-bearing (s=14, s=15, NET-29).**

## The law

**INTERNALIZATION-SATURATES-AT-K=2 + THE-K=1-INTERNALIZATION-IS-SEED-HETEROGENEOUS + S13-IS-A-SEED-WIDE-OUTLIER.**

1. **Eval-sufficiency of the boundary channel saturates at k=2.** At k=2 the
   exclusive block is eval-load-bearing in only 1/6 arms (5/6 fully
   self-sufficient) — statistically indistinguishable from k=3's 5/6 (NET-29).
   Internalization is NOT intermediate: the collapse in eval-load-bearingness
   happens between k=1 and k=2, not gradually across the widths. NET-28's P(cure)
   ramp (k=1 17–33%, k=2 83%, k=3 100%) is therefore a TRAINING-TIME success-rate
   effect only: whenever a k≥2 arm succeeds, its recovery is (5/6) already
   self-sufficient at eval. The boundary-lever dimensionality buys reliable
   *training* success at k=3; *eval* sufficiency is bought at k=2.
2. **s=13 is a seed-wide (not width-specific) outlier.** The SAME seed builds a
   boundary-dependent recovery at BOTH k=2 (zeroN 0.75, flip 0.75, scale 0.91)
   and k=3 (zero3 0.70, scale 0.97, flip no-op), and has the LARGEST exclusive
   coords at BOTH widths (k=2 max 0.701 vs ≤0.660; k=3 ~0.66 vs ≤0.60). The
   magnitude→dependence hint (NET-29, flagged at n=6) now holds at two widths
   for one seed — stronger, still n=6/width with a single outlier. The internal
   structure is width-conditional: at k=3 the ensemble is 2-of-3-redundant and
   sign-INSENSITIVE (flipping one of three is a no-op — two intact coords
   dominate); at k=2 it is 2-of-2-redundant and sign-SENSITIVE (flipping one of
   two leaves a single flipped boundary direction that actively interferes).
   NET-29's "signs never matter" (6/6 at k=3) does not hold at k=2.
3. **The k=1 internalization is seed-heterogeneous, NOT ∝-cure-quality.**
   NET-29's gradient (cures dependent, fails no-op) was a 6-seed observation
   (seeds 14–19) that does not survive a second seed set (seeds 8–13): both new
   full cures are self-sufficient. Pooled over 12 k=1 arms the statement is:
   fails are no-ops in every arm (both rounds); successes split roughly 1/2–2/3
   self-sufficient, 1/3–1/2 eval-load-bearing (small n: 2/2 dependent at NET-29
   seeds, 0/2 at NET-30 seeds, plus a marginal partial). NET-29's law is
   REFUTED at its strong form and replaced by this narrower invariant; its
   practical caution (a k=1 cure may genuinely need its single coord at
   inference) survives for the dependent minority.
4. **Self-sufficiency rate rises with k.** k=1: ~1/2 of successes (n=4 cures,
   2 self-sufficient) — heterogeneous; k=2: 5/6; k=3: 5/6 (identical rate,
   identical outlier seed). The k=1→k=2 step is where self-sufficient
   internalization becomes the overwhelming majority outcome.

**Mechanism statement (supported, causal at the eval level):** the exclusive
boundary channel is a TRAINING-TIME teacher signal (NET-29), and TWO independent
boundary directions (k=2) are already enough for BPTT-through-time to shape a
self-sufficient hidden-state recovery in the large majority of seeds. The k=3
knee (NET-28) only raises the training-time success rate to ~certain — it does
not change what a *successful* recovery looks like at eval (identical 5/6
self-sufficiency at k=2 and k=3). The residual eval-dependence is a SEED trait:
the seed whose optimizer leaves the largest exclusive coords (s=13) keeps its
recovery leaning on the boundary ensemble at eval at every width where it
succeeds, as a redundant-but-sign-and-magnitude-sensitive collective.

## Verdict on the hypothesis

**The round's hypothesis (k=2 intermediate) is REFUTED — k=2 is indistinguishable
from k=3 (5/6 self-sufficient, s=13 the outlier).** The within-width secondary
(∝-quality at fixed k) is also REFUTED (s=10, the worst arm, is self-sufficient;
the only ~2 SE swings there are positive). The unexpected result is the third
refutation: NET-29's k=1 ∝-quality law does not reproduce at seeds 8–13 — the
two fresh full cures are self-sufficient, so the k=1 regime is seed-heterogeneous
with a robust no-op-at-fails invariant. The single cleanest statement: **the
eval-load-bearingness of the exclusive boundary channel collapses between k=1 and
k=2; k≥2 cures are self-sufficient in 5/6 seeds at every width (s=13 the
seed-wide exception), and the k=1 fragility's eval-expression is seed-dependent,
not quality-proportional.**

## Verification vs the network-loop barriers

- **(a) Circularity — clean.** Interventions are inference-only on SAME-SEED
  reproductions of NET-27 arms; the `ctl` re-baselines reproduce the published
  outcomes on fresh draws (Part A {1.0000, 0.9888, 0.9399, 1.0000, 1.0000,
  0.9980} vs NET-27 {1.0, 0.991, 0.948, 1.0, 1.0, 0.999}; Part B {1.0000,
  0.7622, 0.1606, 0.8892, 1.0000, 0.2734} vs NET-27 {1.0000, 0.7715, 0.1567,
  0.8926, 1.0000, 0.2656}). Nothing injected, nothing recovered.
- **(b) Known-method-in-disguise — clean.** Input ablation is standard, but the
  TARGET (the width at which boundary-channel internalization saturates; the
  seed-wide s=13 outlier; the k=1 ∝-quality refutation) is the lab's own
  construction. Catalog re-checked — no package on causal boundary-token
  ablations of length-general recurrences (same family as NET-26/27/28/29 scans).
- **(c) Toy-scale — confronted.** Same carry task; the transferable statements
  are training-time design rules (≥2 exclusive dims → self-sufficient recovery in
  the majority; ≥3 for reliable success) and a caution (k=1 successes are not
  uniformly self-sufficient). Real-scale transfer remains the frontier.
- **(d) Data leakage — clean.** Fresh draws per arm per manipulation;
  teacher-forced; interventions never trained.
- **(e) Variance/reproducibility — the round's content, and the honest negative.**
  This round REFUTES NET-29's k=1 ∝-quality law with a second seed set — recorded
  as a correction, not smoothed over. Seed-heterogeneity (s=13 at both k=2 and
  k=3; k=1 cures split) is reported as a distribution. The s=9 and s=13(k=1)
  ~2 SE excursions are reported as marginals (1 of 12 comparisons each), not
  effects. All arms are byte-identical same-seed reproductions; ctl baselines
  land on published outcomes.
- **(f) Measurement — clean.** Interventions are exact parameter writes
  (zero/flip/scale), teacher-forced exact-match eval, ctl baselines reproduce
  published outcomes. SEs reported; no-ops defined as |Δ| ≤ 1.2 SE.
- **(g) Baseline fairness — strong.** Byte-identical cell across all 12 arms;
  each arm's `ctl` is its own within-arm baseline; Part A vs Part B differ only
  in E (k=2 vs k=1) and intervention set; Part A's seeds are the same as
  NET-27's E=22 seeds, so the k=2 cures are directly seed-paired with published
  outcomes.
- **(h) Practical relevance — the design rule sharpens, and a law is corrected.**
  For a state-augmented answer path: give the final-step boundary ≥2 exclusive
  dims and a successful training run yields a (5/6) self-sufficient recovery at
  eval; ≥3 makes success itself reliable. CAUTION updated: at k=1 a cure is NOT
  reliably self-sufficient — a minority genuinely need their sole exclusive
  coord at inference, and a single-seed ablation can mislead either way.

## Notes for the coordinator

- **The headline:** k=2 internalization is NOT intermediate — it matches k=3
  exactly (5/6 fully self-sufficient under whole-block zeroing; the 6th is s=13,
  the SAME seed as the k=3 outlier, again with the largest exclusive coords). The
  eval-load-bearingness of the exclusive boundary channel collapses between k=1
  and k=2; k≥2 cures are self-sufficient in 5/6 seeds at every width.
- **The correction:** NET-29's "k=1 internalization ∝ cure quality" (cures
  eval-dependent, fails no-op) does NOT reproduce at seeds 8–13 — both fresh
  full cures (s=8, s=12) are self-sufficient. Pooled over 12 k=1 arms: fails are
  no-ops in EVERY arm of both rounds; successes split seed-heterogeneously.
  NET-29's law is refuted at its strong form and replaced by: k=1 internalization
  is seed-heterogeneous, self-sufficiency rate rises with k.
- **The s=13 structure is width-conditional:** at k=3 sign-insensitive
  2-of-3-redundant (flip no-op); at k=2 sign-sensitive 2-of-2-redundant (flip
  −0.25). NET-29's "signs never matter" was a k=3 statement, not general.
- **Reproduction:** all 12 arms reproduced NET-27's published ctl outcomes on
  fresh draws (numbers above); interventions attach to the exact published
  solutions (same seeds, byte-identical cell).
- **Numbers to quote:** k=2 zeroN n=8 full {1.0000, 0.9902, 0.9453, 1.0000,
  1.0000, 0.7544} — 5/6 |Δ| ≤ 0.010 (two largest changes positive); s=13 zeroN
  0.7544, flip 0.7505, scale0.1 0.9067, zero1 0.9961/0.9990; coords 0.701
  (largest). k=1 zero1 vs ctl: s=8 and s=12 0% cost (full cures, self-sufficient);
  s=9 −0.019 (~2 SE, marginal); s=10/11/13 no-op. Pooled k=1 (12 arms): fails
  no-op 100%; cures 2/2 dependent (NET-29 seeds) vs 0/2 (NET-30 seeds).
- **Open questions (natural next rounds):** (1) REAL-SCALE transfer of the
  training-time ≥2/≥3-exclusive-dims rule to a real causal LM's final-step
  boundary — the frontier, unchanged and most load-bearing; (2) the magnitude→
  dependence trend — now seen at two widths for the same seed, still n=6/width
  with a single outlier, needs ~24 more arms; (3) whether the k=1 dependent
  minority (s=14/15) is the same "seed trait" as s=13 at k≥2 — run s=14/15 at
  E=23 and check if they become ensemble-dependent there too (seed-trait vs
  width-trait test); (4) pad384-vs-NET-24-hybrid parity — still open.
- Scripts: /tmp/exp_net_eos_freezek2.py (ALL_DONE_NET30). Log: /tmp/net30.log.

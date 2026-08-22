# EXP 488 TRUE-ECM — Ledger (round-42)

Started 2026-08-22, finished same session, wall 0.8 s (+micro-test). Work dir
/tmp/exp42_trueecm/. Seed 20260922. Never touched /home/raver1975/factor3 (protocol).

## Pre-stated (recorded BEFORE data; timestamps in script header + first checkpoint)
- H1: lcm finds MORE balanced semiprimes than lite at equal cap (B1=50, 30 curves);
  anchor paper-155 lite k=20 = 1163/1200, 37 censored; lcm should censor less.
- H2: mean ops-to-factor (FOUND) HIGHER for lcm than lite, BUT total ops-to-factor
  (incl failed spend) LOWER or EQUAL.
- H3: across-k slope stays ~0.5 (window [0.4,0.6]); no sub-exponential magic at toy scale.

## Design decisions (pre-data)
1..6 as recorded before data (machinery verbatim; ops dbl=4/add=3; added PAIRED lite
control on same population because 487 stored no failed-curve spend; end-of-chunk gcd
as designed check; full binary expansion incl leading bit; schedule
[32,27,25,49,11,13,17,19,23,29,31,37,41,43,47], L = 72 bits ~ 3.09e21).

## Stages / checkpoints (all done)
- [x] Script written BEFORE data: exp488_true_ecm.py
- [x] Micro sanity test (300 random small semiprimes: lcm 284, lite 284, no exceptions;
      "found" self-verifying since gcd in (1,N) is a genuine nontrivial factor)
- [x] Populations generated (checkpoint)
- [x] LCM k=16, k=20 cells (checkpoints)
- [x] LITE paired k=16, k=20 cells (checkpoints)
- [x] Paired analysis + verdicts

## Anomalies / designed-check catches
NONE. End-of-chunk explicit gcd never fired after the per-inversion guards -> guard
logic hole-free (consistent with the algebraic argument prod==0 mod p <=> some den==0 mod p).

## Results (seed 20260922; ops convention dbl=4/add=3 matching exp487)
cell      found     cens  meanT(found)  medT   ops/inst(all)  mean curves  per-curve succ
LCM k=16  1200/1200   0    216.94       139.0   216.9          1.157        ~0.86
LCM k=20  1200/1200   0    654.09       456.0   654.1          2.008        ~0.50
LITE k=16 1200/1200   0    314.06       215.0   314.1          2.672        ~0.37
LITE k=20 1155/1200  45   1134.54       867.0  1258.5          8.992        ~0.104

PAIRED (same 2400 instances): k=16 {both 1200, lcm_only 0, lite_only 0};
k=20 {both 1155, lcm_only 45, lite_only 0, neither 0} -> lcm find set STRICTLY
CONTAINS lite's; all 45 lite-censored instances rescued, zero lost.

Scaling: slope_lcm = 0.3980 per log2 p (k=16->k=20, found-mean basis);
slope_lite_paired = 0.4632; exp487 published lite slope 0.48 (replicates 0.463).
alpha(fit found-only within cell): LCM 0.087 (k16) / 0.345 (k20);
LITE 1.948 (k16) / 0.471 (k20).

Hit-position fingerprints:
- LCM chunk index histogram (schedule idx): mass spread over chunks 1..15+, e.g. k=20:
  chunk1(m=32):172, chunk6(11):112, chunk7(13):107, ..., chunk11(29?):..., chunk13:72 —
  factors emerge from orders needing LARGE prime chunks far beyond lite's reach.
- LITE multiple j histogram capped at j<=50 (top: 24,27,39,46,45,...) as its structure dictates.

## VERDICTS
- H1 CONFIRMED (decisively): 1200/1200 both ks vs paired-lite 1155/1200 at k=20;
  censoring 0 vs 45; paper-155 anchor beaten (1200>1163, 0<37); strict-superset pairing.
- H2 SPLIT: part 1 (found-mean HIGHER for lcm) REFUTED — found-mean LOWER
  (216.9 vs 314.1; 654.1 vs 1134.5; medians 139 vs 215, 456 vs 867). Mechanism note:
  lcm does pay ~2.3x more ops per curve (raw ~90 vs ~39 avg), but needs ~4.4x fewer
  curves at k=20 (2.01 vs 8.99); net found-cost DOWN. Part 2 CONFIRMED: total ops per
  instance incl failed LOWER at both ks (216.9<=314.1; 654.1<=1258.5, 1.92x at k=20).
- H3 REFUTED AS STATED (marginal): slope_lcm 0.3980, misses pre-stated [0.4,0.6] by
  0.002. Qualitatively supported: still ~birthday-class, in fact BELOW lite's 0.463/0.48
  — no super-sqrt(p) acceleration visible at toy scale, as predicted for L_p[1/2,sqrt2].

VERDICT NAME: LCM-SUPERSET-DOMINANCE.

## Caveats (honest limits)
- Toy scale only (k=16/20, p,q < 2^10); the L_p[1/2, sqrt2] vs birthday separation is a
  large-N phenomenon; nothing measured here can exhibit it beyond the slope hint.
- Ops convention inherited from exp487 (dbl=4/add=3 field-op-flavored); raw point-op
  counts logged in result.json (*_raw) — relative conclusions invariant to reweighting
  since both arms counted identically.
- Cross-exp TOTAL-ops comparison impossible from 487 (failed-curve spend unrecorded
  there); the paired same-population lite arm run here supplies it.
- Curve randomness differs between arms by design (independent streams); population
  identical, so pairing removes sampling noise but not per-arm curve luck (mitigated by
  n=1200 and the clean superset pattern).

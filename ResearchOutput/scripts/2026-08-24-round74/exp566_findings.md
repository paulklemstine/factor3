# exp566 MA1-EFFECTIVITY-SWEEP (round-74)

VERDICT: clean H0 (honest negative). MA-1 effectivity NOT armed at this scale.

Coverage: x=2^26 full (no shrinkage), π(x)=3,957,809 primes, 287 moduli
(squarefree [3,300] + primes [307,997]), wall 9.3 s.

Fit: log D ~ −0.0767·log P, slope CI95 (−0.136,−0.015), R²=0.0187
(bootstrap R² CI95 [0.0007,0.065]) — far below H0's 0.5 bar. Slope slightly
negative; partial R² controlling log φ(m) = 0.0008 ⇒ the residual association
is purely a φ(m) size effect. Secondary chi² readout agrees (R²=0.025).

Control: cross-modulus pairing permutation (2000 draws) collapses to null
R² mean 0.0033 / max 0.0435 — gate passed. Note disclosed: literal
within-modulus count permutation is vacuous for max/χ² readouts
(permutation-invariant statistics).

Verification: exact class-number path validated (L(1,χ₋₃)=π/(3√3) exact);
truncation calibrated on 226 overlap discriminants (median rel err 1.8e-5).

LEDGER CATCH: initial truncated series had an off-by-one corrupting all
non-exact L-values (χ₅ gave 0.127 vs true 0.430); caught by spot check,
fixed, rerun.

SCOPING CAVEAT: registered D(m)=max_a|·|/√E is SIGN-BLIND — this result
bounds the magnitude route only; signed character-alignment is the required
follow-up before killing the L-value route.

Files: exp566_ma1_effectivity.py, exp566_result.json, exp566_smoke.{log,json},
exp566_run.log. Digest persisted by coordinator (subagent write guardrail).

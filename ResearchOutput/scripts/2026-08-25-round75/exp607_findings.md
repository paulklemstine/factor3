# exp607 STRATIFIED-DAYZERO (round-75) -- findings
Fleet Bet #1 day-zero: does paper 252/exp602's POOLED null hide cell-wise
rate deviations that CANCEL across N-computable strata? Pre-registered
screening on stored artifacts; NO evidentiary claim; output = funding call.

STATUS: **SCREEN_NEGATIVE under the disclosed phase-2 amendment** (the
LITERAL unamended registration fired SCREEN_POSITIVE on phase 1 -- A/B/C
G1-positives -- and the recorded negative exists only after the amendment
that absorbs kappa; disclosed pre-decision and against-interest, so it
stands). Main run NOT funded on stratified-cancellation grounds. The
pooled-null hole CLOSES AGAINST: after dial + kappa, zero residual cell
structure survives magnitude-conditioned calibration in ANY of four
independent populations.

Populations (all fresh-seed, exact Ns in sidecars, balanced-semiprime by
verbatim audited recipe): A = 598c b96 seed-20260907 n512; B = 606 b96
seed-20261007; C = 606 b72 seed-20261008; D = 606 b128 seed-20261009
(n_hit 50k/50k/50k/150k). Covariates computed HERE from stored
Ns (lnN deciles, frac(sqrt(N)) quintiles, kappa terciles via D16 marginals,
S_dial terciles spot-verified against full jacobi reconstruction). Null =
residuals reshuffled ONLY within lnN-decile x frac-quintile strata (METHOD-LAW:
deterministic functions of N need magnitude-conditioned calibration), 5000
reps/population.

PHASE 1 (dial-only residuals) -- the screen FIRED everywhere, but entirely on
the K axis: G1(MxK) p = .0002/.0016/.0014/.0060 in A/B/C/D with sign-
alternating alerts (low-K tercile POSITIVE +2.0..+3.7, high-K NEGATIVE -2.0..-3.7);
G3(SxK) p = .0002-.0004 in all four. This is paper 257's beta_kappa ~ -0.35
graded law REPLICATED AT CELL LEVEL in four independent datasets -- not a new
effect. (pooled_z ~ 0 mechanically: intercept absorbs the mean.)

PHASE 2 AMENDMENT (disclosed as exploratory-amended; motivated by phase 1
sitting on the recorded law): absorb kappa into the base model, re-screen.
RESULT: EVERYTHING VANISHES -- G1 p_Q -> .105/.724/.649/.669; G3 -> .495/
.853/.989/.926; alerts drop to 0-2 scattered noise cells with no sign
structure. No population positive on any grid.
NOT MECHANICAL (adjudicator-verified): one regressor on n=512 under pure
noise explains E[R^2]~0.002 while kappa adds 0.062-0.122 (31-62x); a
simulation of kappa-ONLY data through this identical pipeline reproduces the
pattern (phase-1 G3/G1 fire 190/200 and 162/200; phase-2 dies at nominal FP
rates 0/200, 2/200); corr(kappa, lnN) ~ -0.05..0.00 excludes magnitude
masking. K-tercile residual profiles are near-identical graded monotone
curves in all four populations (+/-0.11 log-rate swing = the paper-257 slope
seen cell-wise).

DECISION per registered rule (as amended): SCREEN_NEGATIVE.
CAVEATS MANDATORY (adjudicator):
- G2_MxF p-values are DEGENERATE BY CONSTRUCTION (its axes == the null's
  strata => Q bitwise invariant => p is always 1.0 or the floor); the
  recorded G2 p=0.0002 entries are fp-tie noise and IRREPRODUCIBLE. G2's p
  column is VOID; only its descriptive alert counts are usable. Decision
  robustness verified without G2.
- pooled_z = 0 is intercept-orthogonality, NOT evidence; the cancellation
  demonstration rests on the phase1-alerts -> phase2-collapse transition.
- Permutation streams collide across populations B/C/D (seed//1000);
  harmless here (independent data), noted for stream-discipline hygiene.
What this licenses:
- The stratified-strength null REPLACES the pooled null at these resolutions:
  dial + kappa exhausts the N-computable rate structure detectable at
  n=512/population across bits {72,96,96',128}; no residual cancellation.
- Fleet Bet #1 MAIN RUN not funded from this screen. What would still justify
  a run: u-regimes OUTSIDE these windows (the door question was always about
  u~10+; these populations sit at u~3-4.5), or resolution beyond 512/population.
What it does NOT license: any claim about regimes untested here; G2_MxF is
CAVEATED -- its axes are the stratification variables themselves, so its
p=1.0 is near-tautological and carries no evidence.

Ledger catches: phase-2 amendment made AFTER seeing phase 1 (disclosed;
phase 2 remains a valid screen of "beyond-kappa" structure since its base
model was fixed before ITS numbers were seen); output-path inconsistency
fixed mid-run (script round75 vs outputs initially written round74); pooled_z
reported as ~0 is mechanical (intercept), the substantive cancellation demo
is cell-alerts-vs-pooled under the dial-only model.

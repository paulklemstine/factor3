# exp583 SHAPE-TEST-NONPARAM (round-74) -- findings
Question (paper 232 follow-up): does the u*~0.65 mid-window excess survive
as ABSOLUTE SHAPE of the hit-indicator vs normalized position x without any
binning? Pure reanalysis of exp581_regen_positions.npz (128 strata, hits
9594 / controls 512000; windows [jlo,jhi], jhi/jlo=3).
Convention verified pre-script: ctl arrays linear-uniform in window =>
x=(N-jlo)/(jhi-jlo). Design: stratum-conditional case-control logistic
(128 intercepts profiled); free natural cubic spline df=5 (knots
.25/.5/.75) vs LINEAR x; LRT asym chi2(df3) on FULL design + permutation
calibration (within-stratum label shuffles, B=400, capped 200ctl/stratum
design). Coordinator fuse: monotone-I-spline leg and Dickman-offset leg
SKIPPED (registered H1 clauses untested -- disclosed, not failed).

VERDICT: **H0_CHANNEL_CLOSES** (per registered rule)
- free-vs-linear LRT stat=100.6 df=3, asym p=1.2e-21; perm 0/400 exceed
  => p_perm <= 0.0025 (resolution floor; registered <0.001 bar unmeetable
  at B=400, direction STRONGLY confirms real non-linear structure)
- BUT interior max x*=0.020 CI[0.020,0.020] -- pinned at LEFT EDGE;
  [0.4,0.8] bar FAILS => no mid-window hump exists as raw shape
- peak/end ratio 2.54 CI[2.24,2.80] (>1 = steep monotone DECLINE, not hump)
- CONTROL arm (pseudo-cases=ctl draws vs synthetic uniforms): perm p=0.856,
  null as required; big-design asym p=0.035 marginal (n=1M detects
  microscopic wiggle; passes registered >0.01 bar via perm criterion)
- Descriptive cross-check: decile hit counts strictly declining
  [1554,1177,1044,927,875,877,863,807,776,694]; +1.6% blip near u*~0.55-0.65
  is the exp582 vertex ghost -- a baseline-relative ripple, not a mode.

READING: the position channel carries a REAL, binning-free, strongly
non-linear but MONOTONE-DECLINING magnitude law (steep near x=0, exactly
Dickman-type); the paper-232 "hump" at u*~0.65 does NOT exist as an
interior maximum of the raw curve -- if the exp582 R=T/M vertex is real it
lives entirely in the DENOMINATOR's curvature (baseline-relative excess),
not in absolute position shape. Registered consequence stands: absolute-
shape claims for the mid-window excess are closed; any revival must be
stated as a baseline-mis-specification claim, not a positional mode.

Honest: minimal skeleton under coordinator fuse (~15 min mark): two
pre-registered legs skipped (monotone comparison, Dickman offset);
perm/boot on control-capped designs (200/stratum) with observed stats from
full design; control-arm asym p from large synth design vs perm from capped.
Seeds P/B/S=20260902/03/04. No commits; only exp583_* touched. Wall 273 s.

# EXP586 WEIGHT-EXPONENT-FIT — findings

**Verdict: H1 HARMONIC-REFINED — the optimal exponent is alpha_hat = 0.5, not 1.**

## Alpha curve (full, n=128, odd primes 3..400, mechanistic Legendre c_l=[jacobi(N mod l,l)==+1])
| alpha | 0.0 | 0.25 | **0.5** | 0.75 | 1.0 | 1.25 | 1.5 | 2.0 |
|---|---|---|---|---|---|---|---|---|
| R2(log-rate~S_alpha) | .3207 | .4985 | **.6242** | .5752 | .4731 | .3969 | .3479 | .2944 |

- Clean single interior peak at alpha=0.5; harmonic (alpha=1) sits on the FALLING limb.
- dR2(alpha_hat) - R2(1) = +0.151 >= 0.03 threshold -> H1 fires; H0 rejected.
- Bootstrap (500 reps, resample Ns): alpha_hat* = 0.5 in 492/500, 0.75 in 8/500
  -> CI95 = [0.5, 0.5], excludes 1.0; bootstrap mean 0.504.
- Sanity anchor vs unweighted count (alpha=0, R2=.3207): best alpha beats it by
  +0.304 (materially); even harmonic beats it by +0.152 -> paper 227 was right
  that weighting matters, wrong about the exponent.

## Consequence
Product-dial law REFINED from Sum(chi=+1)/l to Sum(chi=+1)/sqrt(l): large primes
carry ~sqrt(l)x more relative weight than the adopted harmonic form, and the fix
lifts dial explanatory power from R2=.47 to .62 (+31% relative) on the same data.
The inspection-chosen 1/l over-penalized the tail; the true profile decays
l^-0.5.

## Integrity checks
- Population regeneration verbatim (exp577 recipe): 128/128 Ns identical;
  recomputed odd-prime count <=400 matches stored S400 column EXACTLY (diff 0.0,
  corr 1.0) -> exp577's dial also excluded l=2 in effect.
- Honest limits: alpha grid discrete (resolution +-0.25; fine structure near 0.5
  not fit per pre-registration); single seed 20260827, pure reanalysis, no fresh
  replicate; OLS log-rate Poisson attenuation applies uniformly across alpha so
  argmax likely robust while absolute R2s are attenuated; smoke (n=16) picked
  grid-edge 0.25 -- small-n noise, full run interior.

Artifacts: exp586_weight_exponent.py, exp586_smoke.log, exp586_full.log,
exp586_result.json (config/regression/alpha_curve/stats/verdicts/honest_notes/wall_s).
Source data: exp577_result.json rows (hits/total per N, total=150000).

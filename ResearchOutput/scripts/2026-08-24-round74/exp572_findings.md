# exp572 MA1-SIGNED (round-74)

VERDICT: H0 on both registered criteria — signed route dead too. MA-1
computable-effectivity program CLOSED on BOTH routes (magnitude exp566 R²=0.019;
signed chance-or-below here) => honest negative strengthening paper 213.

Coverage: x=2^26 full, π(x)=3,957,809, 287 moduli (squarefree [3,300] + primes
[307,997]), 491 real-char cells, 86,882 unit-class cells, wall 7.0 s.

Identity (asserted exact on smoke cells): c_χ = Σ_a d_a·χ(a) = Σ_{p≤x, gcd(p,m)=1} χ(p);
the uniform-li theory term vanishes identically ⇒ the ONLY computable x-independent
theory weight is signed L(1,χ).

DEGENERACY DISCLOSURE (post-smoke, pre-full-data): L(1,χ)>0 for EVERY real
non-principal χ (class-number formula) ⇒ sign(w)≡+1, n_cells_w_negative=0 confirmed.
Cell-level "agreement" is EXACTLY Pr[c_χ>0]; criterion C1 as registered could only
fire if prime twists were majority-positive. Registered readouts:
- cell agreement 15.07% over 491 cells, CP95 [0.120,0.186], CS_z=−52.7 vs
  within-modulus shuffle null (2000 draws) — decisively NOT >50%.
- class level: sign(d_a) vs sign(Σ_χ L(1,χ)χ(a)) agrees 48.74%, CP95
  [0.4841,0.4907], permutation z=−7.74 — significantly BELOW chance (mild anti-
  alignment of |deviation| profile with L-magnitude weights).

STRUCTURE FOUND (labeled exploratory, not pre-registered): prime twists are
NEGATIVE for 84.7% of all (m,χ) cells (CP95 [0.812,0.878]) — a massive universal
Chebyshev/Rubinstein–Sarnak-type skew (smoke x=2^22: 91.7%). Deviation signs are
NOT random: they are one-directional across moduli, driven by low zeros, not by
L(1,χ) — which is precisely why no computable L-value carries them.

Breakdowns (agreement, all CI wholly below 50): prime-moduli quadratics 26.9%
(167); product chars ω≥2 8.95% (324); exact-L path 12.8% (226); truncated 17.0%
(265); drop-|w|<1e-3 robustness = unchanged 15.07%.

Ledger catches: (1) orthogonality assert initially failed at m=6 — c_χ sums χ over
primes coprime to m; raw primitive twist adds ±1 per prime p|m, p∤cond(χ)
(max corr 3 at full scale; 0 sign flips induced — disclosed, not corrected).
(2) Class-level z first mixed ±1-scale obs against agree-count null (−310);
recomputed single-scale z=−7.74. (3) exp566's "within-modulus shuffle vacuous"
caveat does NOT apply here (sign(c) not permutation-invariant in a).

Consequence stated: barrier-map residual "MA-1 effectivity" is closed as a named
question — neither magnitude nor sign of AP deviations is captured by computable
character data at this scale; deviation structure lives in the zero-driven
universal skew instead. Files: exp572_ma1_signed.py, exp572_result.json,
exp572_smoke.{log,json}, exp572_run.log.

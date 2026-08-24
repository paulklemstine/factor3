# exp576 QR-VS-OVERDISPERSION (round-74) — findings

VERDICT: **NEW-STRUCTURE-MAP-ENTRY** (pre-registered H0 fires; H1 rejected).

Setup: 128 balanced bitlen-96 semiprimes, FRESH master seed 20260826
(stream-distinctness asserted+recorded vs 20260824/20260825: pairwise-disjoint
N sets, orderings differ, hashes e8d89a29a03779d5 / 9cb9cc800ee45a38 /
81acc9b5e1be619b). 150k j-samples/N (19.2M total), exp569 gcd-chain tester
verbatim, cut 1e6. Wall 368.9 s. sympy.jacobi_symbol.

Overdispersion REPLICATED on a fresh population: mean 76.7 hits/N,
Var/mean **D_raw = 7.27** (phi_null 7.33; Poisson would be ~1), range 29–172,
top-3 clusters 172/151/130 — exactly the paper-220 envelope rescaled
(their 600/561/540 @ ~600k/N ⇒ ~150/141/126 here). The u≈10 phenomenon is real
and seed-independent.

Regression (per-N log-rates vs dial):
- PRIMARY S_indiv (task-specified, sum of individual Jac(l,p),Jac(l,q)=+1 over
  l<=100): **R2_log = 0.0127, slope NEGATIVE** (z=-2.82, rate x0.992/unit),
  **D-reduction 0.88%** -> H0 leg 1 AND leg 2 both fire.
- Secondary S_prod (=#{l<=100: N is QR mod l}, the mechanistic dial):
  R2_log 0.078, slope + (z=10.9), D-reduction 14.2%, phi 7.33->6.07.
- Tertiary S139@400 (recorded paper-136/139 form): R2_log 0.057, + (z=8.7),
  D-reduction 9.1%.

Consequence stated plainly: the QR dial does NOT explain u~10 overdispersion —
even its best form removes only ~14% of the excess variance; >=86% is
N-structure beyond any <=400 QR pattern. Map entry named.

Two mechanism notes (honest, post-hoc but analytic):
1. The primary dial's null was predictable: under independent characters,
   Cov(S_indiv, S_prod)=0 EXACTLY (A,B,C multinomial algebra), measured
   r(S_indiv,S_prod)=-0.01. The task-specified dial is orthogonal by
   construction to the quantity that governs divisibility (l | x^2-N iff
   Jac(l,N)=+1). Verdict unchanged either way: secondaries also miss H1.
2. Scale hypothesis for WHY the recorded law fades: hits require LPF<=1e6 but
   every tested dial covers l<=400 only; at bitlen 96 pools span ~2^49-51, so
   the informative prime window has shifted into 400..1e6 where the dial is
   blind. Paper-136/139 calibrated at bitlen 40-48 where small primes dominate.
   NAMED FOLLOW-UP: product-form dial over ALL l<=1e6 (computable from p,q mod
   l, ~78k symbols, cheap) — if it captures the residual, papers 136/139 and
   220 unify with a scale-dependent dial bound; if not, genuinely new
   N-structure at u~10.

Weak-slope caution: S_indiv slope flipped sign between smoke (n=16, +) and
full (n=128, -, z=-2.82) with pseudo-R2~-0.001 — do not cite the negative
direction as a reversal of paper-139 without replication.

Ledger catches: (1) first-smoke GLM divergence (bare Newton overflowed;
fixed with Fisher scoring + deviance step-halving, caught pre-full);
(2) smoke/full slope-sign instability logged above; (3) monitor double-fire —
result verified from JSON directly, no data impact.

Files: exp576_qr_overdispersion.py (pre-registration in header), exp576_smoke.log,
exp576_smoke_result.json, exp576_full.log, exp576_result.json (config/rows/
regression/stats/verdicts/honest_notes/wall_s).

# EXP597 DIAL-SCALE-TRANSFER — findings

**Verdict: HREFINE_SCALE_DEPENDENT fired** (pre-registered rule). alpha_hat = **0.75 @ b48
[CI95 0.5–0.75], 0.50 @ b72 [0.25–0.75], 0.75 @ b96 [0.5–1.0]** — not all inside [0.35,0.65]
(band holds only grid point 0.5), and the excursion is NON-monotonic (0.75→0.5→0.75), so the
strict H1 ("sqrt-weight uniquely optimal everywhere") fails while a clean directional drift
law also fails.

**What actually transferred:** the weighted-dial ADVANTAGE, not the point exponent.
- Unweighted anchor alpha=0 uniformly weak: R² = 0.131 / 0.120 / 0.120 at 48/72/96 — every
  fractional weighting beats it by dR² = +0.10…+0.23 at ALL bitlens. The chi+ dial family
  works at every scale tested (48→96, 2x beyond paper 223's b=15, matching 227's 96).
- The sqrt-vs-harmonic refinement does NOT transfer cleanly: dR²(S_0.5 − S_1.0) =
  +0.032 (b48), +0.083 (b72), **−0.005 (b96)** — sign flips at the largest key size.

**Refined reading:** R²(alpha) curves are SHALLOW plateaus at every bitlen (argmax vs best
fitted alternative dR² = 0.008 / 0.010 / 0.024; only b96 clears exp586's 0.02 materiality bar,
and there harmonic edges sqrt). Bootstrap distributions overlap heavily; **alpha=0.5 lies
INSIDE all three per-bitlen CI95s**, as does 0.75; common support = [0.5, 0.75]. Honest law:
a scale-stable exponent PLATEAU around 0.5–0.75 whose location this design (n=96 clusters x
30k samples => ~8 hits/N, heavy Poisson attenuation; R² levels NOT comparable to exp586's
150k-sample 0.62) cannot resolve to better than one grid step. Canonical covariate S_0.5 is
defensible without scope restriction (never materially beaten), but "alpha*=0.5 exactly"
should be downgraded to "alpha* in [0.5, 0.75], grid-unresolved".

**Design facts:** populations 96/bitlen, seeds 20260904/05/06, exp586 generator verbatim;
tester = gcd-chain exact B-smoothness of y=(isqrt(N)+j)^2−N, j~U[1,2^52) absolute;
hit rates ~2.4–3.0e-4 comparable across scales; zero-hit Ns: none. Wall 265 s parallel.

**Catches:** (1) tester RECONSTRUCTED from task spec — exp577 script outside read permission;
semantics locked to exact B-smoothness, lineage coherence via l|y <=> chi(N,l)=+1.
(2) Two pool-infrastructure bugs fixed mid-run; smoke numbers byte-identical pre/post.
(3) SINGLE seed per bitlen; single-grid-step resolution; endpoints are grid points.

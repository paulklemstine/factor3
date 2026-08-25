# F1TIGHT — paper-225 master inequality vs the measured positional profile (round-74 THEORY)

Connects the PROVEN bound `S ≤ min(1/(Λ·Θ·q̂), 2^k_bits/(Λ·Θ))` (gapL4_measure.md §F1) to tonight's
measured profile chain (papers 228/229/230/233/238/242; exps 578/579/581/582/583/588/588b/592/594).
Finite check: `f1tight_check.py` → `f1tight_result.json` (0.5 s). Sources: gapL4_measure.md,
gapL7_extremality.md §46-56, synth_r73_80_synthesis.md, pthat_extraction.md, findings exp578/579/
581/582/588/588b/592/594/597. No commits; only `f1tight_*` touched.

## (a) PARAMETER MAP — which measured object is which F1 booking

| F1 object | Definition | Measured carrier (228–242 chain) | Numbers |
|---|---|---|---|
| **Λ(π)** | C_sort/C_desc ∈(0,1]; =1 iff within-stratum MLR | The positional profile ITSELF = within-window prior shape (gapL7 "divisor-mass tilt"). π := normalized T(x), T(x)=A(1+x)^−b_bulk+K(1+x)^−b_edge, monotone declining ⇒ sort order = window-ascending | From (b_bulk=.573 [.412,.767], w=.086 [.064,.108], b_edge≥15): **Λ_meas=0.766**, i.e. ascending beats descending **1/Λ≈1.306**. Bulk alone gives Λ≈0.895 (gain 1.12) — the left-edge spike supplies ~⅓ of the tilt. Measured Λ faces elsewhere: hard-balance 1.58× (Λ≈.63, papers 221/223), pool-137 1.078× (Λ≈.93), deployed top-heavy Λ=1.0 descending-extremal (exp575). Predicted 1.31 on THIS pool type is UNTESTED — testable implication |
| **Θ(Π,π)** | E_πC(Π)/K_booked; ≡1 iff uniform-within-cells | NOT independently measured; pinned once Π is named. For full-window ascending: Θ=C_sort/C₀=Θ_asc≈**0.867** (head-loaded). Descending baseline reads Θ_desc≈1.13 (tail-loaded). gapL4's ρ_R≈0.59 read of witness 5.19 = Θ>1 in this language. Uniform-cell booking Θ=1 is REFUTED on this data | Θ_asc ∈ [~0.83, ~0.91] across the profile CI |
| **q̂** | μ_eff·P_eff+(1−P_eff)(1−μ_eff) | **NOT identified by any recorded number in the 228–242 chain**: every profile experiment scans the FULL window ⇒ μ_eff=1, P_eff=1, q̂=1 trivially. Only q̂-bearing records are the four legacy anchors — whose P̂ are law-INVERSIONS of the speedups (pthat_extraction.md: no hits/trials exist in any artifact) | Anchors (μ,P̂,S): (.05,.8500,5.194)→q̂=.1850; (.05,.9003,6.915)→.1397; (.05,.8106,4.353)→.2204; (.02,.985068,29.125)→.03433. Required ΛΘ=1/(S·q̂) = 1.041/1.035/1.042/**0.99999** — ≈1 BY CONSTRUCTION (inverted through S_A=1/q̂ = the bound at Λ=Θ=1): tightness-circular, zero evidential weight |
| **k_bits** | T2-priced comparison queries | No T2 schedule run tonight; static test-blind ⇒ k_bits=0 ⇒ arm 2 = 1/(ΛΘ) ≥ arm 1 since q̂≤1: **arm 1 binds everywhere** | min() = 1/(ΛΘq̂) |

## (b) EQUALITY CONDITION — derived, then tested against b=.57/b_edge≥10

Proof chain has exactly one INEQUALITY link: majorization `C_sort ≤ C₀`, equality iff π flat
(gapL4 step ii). All other links are identities (r̄-identity, Λ def, Θ def). Full equality needs:
- **E1**: π flat within cells (⇒ automatically Θ=1, Λ=1);
- **E2**: binding-arm saturation: q̂ = 2^(−k_bits); test-blind k=0 ⇒ q̂=1 ⇔ μ_eff=P_eff=1 (full support);
- **E3**: vanishing O(1/M).

E1 tested against measurement — refuted THREE independent ways: KS D=.09519, p=6.9e-76 vs uniform
(paper 228/exp578); two-component fit dAICc=37.3, LRT p=9.3e-10, spike weight CI [.064,.108]
excludes 0, b_bulk CI [.412,.767] excludes flat b=0 (paper 238/exp588, cap-ladder exp594);
binning-free conditional-logistic LRT p=1.17e-21, monotone decline (paper 233). Controls flat in all
three. **⇒ NO realizable policy attains equality on this data; E1 fails pool-side, beyond policy choice.**
Finite check (M=40k, exact cell sums): point (b=.573,w=.086,b_e=15): Λ=.7657, Θ=.8673,
S_asc(realizable static)=1/Λ=1.3060, bound=1/(ΛΘq̂)=1.5059, **slack X:=bound/S_asc=C₀/C_sort=1.1530**;
CI-corner grid (b,w,b_e) 27 cells: **X ∈ [1.1018, 1.2205]**. X is baseline-free and
policy-independent (bound/achieved = C₀/C_sort for EVERY Π at q̂=1; for μ_eff<1 policies the same
factor multiplies the further q̂ room). Hump sensitivity: +20% excess at x*=.65 moves X by −0.019
only — first-moment-insensitive (and the hump is exp592-gated anyway, see (d)).

## (c) THE GAP STATEMENT — falsifiable condition, numbers plugged

The bound is tight on this data iff **C_sort(π_meas)=C₀**, equivalently **E_π[x]=1/2 exactly**,
equivalently **b_bulk=0 AND w_spike=0 within measurement error** (flatness forces Λ=Θ=1 too, so
this single condition is the whole gap). Measured: E[x]=0.4336 at the point fit ⇒ C₀/C_sort=1.153;
over the joint CI E[x]∈[0.410,0.454] ⇒ slack ∈[1.10,1.22]. Falsifier: any same-design pool
re-measurement (128 balanced bitlen-96 semiprimes, ≥9594 hits, cluster bootstrap) returning
E[x]=0.500±0.005 would reopen tightness; current recordings exclude it at overwhelming significance.
Second, independent gap: for the truncation ANCHORS, tightness requires a NON-inverted (raw)
P_eff measured under a named committed R_eff such that Λ·Θ·q̂=1/S_meas holds without assuming it —
none exists (all four P̂ are inversions; booked "at resolution limit").

## (d) VERDICT

**Bound-slack-by-factor-X on the full-window static class: X = 1.15 [1.10, 1.22]** — the proven
inequality overshoots every realizable test-blind policy on the measured profile by ≥10% and ≤22%,
and the slack is PROFILE-FORCED (irreducible: no policy can flatten π) and POLICY-INDEPENDENT
(= C₀/C_sort exactly). On the truncation/witness anchors: **not-currently-decidable** (P̂ circularity).
This does not weaken the theorem — it LOCATES the open work, matching gapL4's own ranking:
- **Closer (experiment, ~1 session, no heavy compute):** jointly measure achieved S_vs_desc,
  Λ, Θ, q̂ on the exp578 pool by scan simulation over the stored npz (window-ascending policy).
  Prediction from the map: S≈1.31 vs bound 1.51; observing S>1.51 would FALSIFY the mapping
  (i.e. the profile is not the operative π for cost), making this a genuine two-sided test.
- **Closer (theorem):** F1's stated residual = sharpness (every realizable booking attained by some
  π). On-data attainment is impossible HERE (E1 excluded), so sharpness must be posed over the prior
  class, never as tightness-on-this-pool; tonight's X is the quantitative form of that separation.
- Hump status: paper 242's divisibility-mixture-surviving hump (amp_mix .177±.043, z=4.11) is
  **exp592-GATED-H0** on fresh seed (amp_mix .074±.038, z_cal=−1.08) — carried as unconfirmed;
  immaterial to X regardless (ΔX=−0.019 at +20% amplitude, first-moment argument).
- exp597 relevance: dial-exponent plateau α∈[0.5,0.75] concerns the RATE layer (smoothness
  covariate), orthogonal to the positional-shape layer consumed by Λ/Θ here — no coupling assumed.

Provenance: this file + `f1tight_check.py`/`f1tight_result.json`. Round74 dir; not committed.

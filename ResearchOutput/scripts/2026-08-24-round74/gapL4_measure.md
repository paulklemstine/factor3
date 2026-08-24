# GAP L4 — THE POSITIONAL-STRATUM MEASURE: over what is T1 universal? (round-74 THEORY)

Companion to `barrier4_positional_converse_draft.md` (T1/T2/D), L7 (`gapL7_extremality.md`),
paper 219. Checks: `gapL4_check.py` → `gapL4_result.json` (<5 s).

> **REVISION (2026-08-24, post-verifier `verifyL4_verdict.md`; machine evidence
> `verifyL4_recheck.py` → `verifyL4_recheck_result.json`) — record-with-fixes applied:**
> (1) master inequality FULLY EXPLICIT (exact Θ; μ_eff/k_bits defined; bound PROVEN via majorization — F1);
> (2) F3 downgraded to BASELINE-CONDITIONAL (full-scan-M / C₀-halving / same-prior-descending undercut
> 5.365<5.4054); (3) former "tail-corner" reading of 5.19 corrected: both historical laws are ρ=½ values
> under two SILENCE SEMANTICS (not arrangement corners); measured 5.19 ∈ (drafted, certified) ⇒ within-
> window mean-rank fraction ρ_R≈0.59 at C₀ baseline — mild adverse loading, not corner identity; (4) A3
> wording: bare-(μ,P) violation rate highest at HEAD placements (.60/.37/.34 head/mid/tail); witness
> restated S=62 (2.91× booking).

## 0. The structural fact L4 rests on (new, exact): the r̄-IDENTITY

For ANY prior π on I(N), any partition {R, C=R's complement}, |R|=μM, protocol A committed
(scan R top-down; certified silence ⇒ scan only C):

  **EC_A(π,R) = P·r̄_R(π) + (1−P)·r̄_C(π)**,  P=π(R), r̄_B = mean within-block scan-rank.

This is definitional but load-bearing: T1a's closed form S_A = 1/[μP+(1−P)(1−μ)] is EXACTLY
the special case r̄_R=(μM+1)/2, r̄_C=((1−μ)M+1)/2, i.e. **uniform-within-cells**. Under uniform
π this is forced (P=μ too) — that is T1c's geometry-freeness. Off it, P≠μ AND the r̄'s are free
in [1, block size]: the closed form in (μ,P) alone is NOT an upper bound on achieved S
(A3: 43.9% of tilt×placement draws violate it; explicit M=64 witness — all mass in the head-half
of a BOTTOM window μM=3 — gives S=62 vs booked 21.3; asymptotically 4/μ−3). So "universality" splits:
  (i) FORM-universality: the r̄-identity — unconditional, prior-free. PROVEN (definitional).
  (ii) VALUE-universality: S depends only on (μ,P) — FALSE off uniform cells; needs shape.
The drafted-vs-certified law pair is unified by the same identity at the ρ_B:=r̄_B/|B|=½ slice:
certified = CERTIFYING silence (branch costs (μM+1)/2 and ((1−μ)M+1)/2); drafted = NON-certifying
silence (fallback rescans everything: silence-branch cost M/2), denominator 1−(1−μ)P. They differ
in silence semantics, not within-cell shape; arrangement tilt (ρ_B≠½) moves the value off both
bookings and the BASELINE choice moves it again (F3). Measured 5.19 ∈ (5.1948, 5.4054): at C₀
baseline, ρ_C=½ this pins ρ_R≈0.59 — mild adverse loading (structural direction: p ≤ √N always;
balance pushes p below √N, toward descending-scan tails), not a corner identity.
The selection correction Δ of draft-L4 is exactly Δ = P(r̄_R−(μM+1)/2)+(1−P)(r̄_C−((1−μ)M+1)/2) — sign and mechanism attached.

## F1 — WORST-CASE with Λ explicit (corrected master-inequality form)

Class: all measurable R, all π; policies test-blind + certified-silence (+T2-priced queries).
Bookings — each computable WITHOUT reference to achieved speedup (answers L7-d):
  * **Θ(Π,π) := E_πC(Π) / K_booked**, with K_booked := [P_eff(μ_effM+1)+(1−P_eff)((1−μ_eff)M+1)]/2.
    Exact ratio by the r̄-identity; **Θ ≡ 1 ⟺ uniform-within-cells**; Θ ∈ (0, Θ_max], monotone
    in the loadings ρ_B (Θ→small when cells are head-loaded, large when tail-loaded).
  * **μ_eff(Π) := |R_eff|/M** — width of the committed search support (window/truncation: |R|/M;
    pure permutation: R_eff=I so μ_eff=1).  **k_bits(Π)** := adaptive comparison-query count
    (T2-priced), saturating at k_pin=log₂W (T2c).  P_eff := π(R_eff);
    Λ(π) := C_sort(π)/C_desc(π) ∈ (0,1] (=1 iff within-stratum MLR, L7).
**MASTER INEQUALITY — PROVEN, unconditional:** for every test-blind Π and every prior π,
    S_vs_desc(Π) := C_desc/E_πC(Π) ≤ **min( 1/(Λ·Θ·q̂), 2^{k_bits}/(Λ·Θ) )**,
  where q̂ := μ_eff·P_eff + (1−P_eff)(1−μ_eff) (finite-M: q̂+O(1/M)).
Proof chain: (i) r̄-identity ⇒ EC_Π = Θ·K_booked; (ii) sorted_desc(π) majorizes flat(1/M),
so C_sort = Σ_j sorted_desc(π)_j·j ≤ Σ_j j/M = C₀ (equality iff π flat); (iii) C_desc = C_sort/Λ.
Compose: S = C_sort/(Λ·Θ·K_booked) ≤ C₀/(Λ·Θ·K_booked) = 1/(Λ·Θ·(q̂+O(1/M))). ∎
So the two-parameter law generalizes to a prior-free booked bound; NO constant cap exists
(head-loaded/deep-mass priors exceed any fixed booking's naive reading; consistent with (e)/O1/O2).
D factorization: survives as this INEQUALITY chain (COST-side 4/3 untouched — touch-floor is
prior-free), loses pathwise product (L7 interaction = leakage). Universality claim: bound uniform
in geometry given bookings; remaining theorem = SHARPNESS (every realizable booking attained by
some prior; constructive, finite-checkable à la M=33) — the open work, more than hours (verifier).
Witnesses: 5.19 stays a WITNESS (feasibility μ≤1/S; ρ_R≈0.59 above). Precision flags (A1): paper 219
pairs (0.05,**0.9003**) with value at P=0.90 (S_cert=7.1567≠7.1429) and (0.02,**0.9853**) with value
at P=0.985 (S_cert(0.02,0.9853)=29.3152≠29.0698); inverting through MEASURED 29.1 gives
P_implied=0.98504 — feasibility lives in P̂'s 4th decimal. VERDICT: witness-at-resolution-limit;
store raw P̂. Cross-pool monotonicity fails (P(.02)=.985 > P(.05)=.85): different generators (O2).

## F2 — AVERAGE-CASE: explicit prior class (scale × balance)

Key arithmetic: semiprime N=pq, r=q/p, x=p=√(N/r), so s=x/√N=r^{−1/2}: **balance IS position**
given scale. Class 𝓟 = {scale: log N ~ U[L₁,L₂]} × {b(r), r∈[1,R_max]}; positional density
π_s(s)=2b(s^{−2})s^{−3}. Anchor b∝r^{−3/2} ⟺ UNIFORM-in-x positional prior — T1a's exact kernel.
Policy class: static orders ∪ certified-silence partitions ∪ T2 comparison schedules
(√-descending/wheels/bisection in-class; wheels as D-composites). Universality: capture curve
**P_b(μ) = ∫₁^{(1−μ)^{−2}} db/B(R_max); canonical P(μ)=μ/(1−R_max^{−1/2})** — linear iff canonical (A2).
Required-R per anchor: (0.05,0.85)⇒1.129, (0.02,0.9853)⇒1.042, (0.05,0.90)⇒1.121, (0.05,0.811)⇒1.136 —
ALL FOUR demand ultra-balanced populations (r ≤ 1.04–1.14); hard-balance U[1,2] captures only 17%
at μ=5%; RSA-like r≤1.21 captures 55%; saturation (P=1) only for R_max ≲ 1.11. The witnesses are
NOT universal constants under F2 — GENERATOR SHAPE ESTIMATORS (each anchor = an r-quantile
statement); T1 tight iff g≡const in b=r^{−3/2}g. D factorization: BEST posed here — residue ⊥
position under scale×balance ⇒ S(R∘F)=S(R)S(F) in prior-expectation (supports L2), pathwise fails (L7).
Verdicts: 5.19/29.1 demote to per-generator operating points; F2-universal objects are capture
curves + Δ(b) integrals (closed-form for polynomial/exponential tilts).

## F3 — ADVERSARIAL-PRIOR (max-min; connects to isolation-cost lower bounds)

Policy commits schedule+partition; adversary picks π in 𝓒(μ,P)={π: ∃R, |R|=μM, π(R)≥P}.
Move order is the crux: adversary-second ⇒ degenerate (mass on last-scanned candidate).
SIMULTANEOUS commitment (policy names R; adversary fills π with π(R)≥P; max-EC arrangement =
P-mass at R's bottom + (1−P)-mass at C's bottom, EC = P·k+(1−P)(M−k), brute-force confirmed)
is well-posed, but its value is **BASELINE-CONDITIONAL** [REVISED]:
  (a) against the FULL-SCAN-M payoff baseline: value = 1/[μP+(1−P)(1−μ)] — the certified law exactly;
  (b) against paper-T1a's own uniform C₀=(M+1)/2 baseline the SAME equilibrium HALVES:
      S = (M+1) / (2M·[μP+(1−P)(1−μ)]);
  (c) against the MATCHED same-prior-descending baseline the adversary strictly UNDERCUTS the
      certified number: S = [1−(1−P)μ]/d < 1/d at d=μP+(1−P)(1−μ) — frontier locus 5.365 < 5.4054.
No baseline-free equality exists; the historical-laws genealogy survives MODULO CONVENTION (ρ=½
values under two silence semantics). Degenerate-case figure below likewise assumed C₀ — same caveat.
Isolation-cost link unchanged: coverage×width lower bounds are F3's feasibility constraint backwards.
D: the 4/3 COST cap survives verbatim (prior-free); SET side books whichever baseline the standard names.

## Ranking of proof feasibility

1. **F1 form-universality** — bound now PROVEN (above); remaining theorem = sharpness/attainment
   per booking. Finite check à la M=33: DONE-shape (A3 sweeps M=64, 4000 tilts × head/mid/tail
   placements: uniform-diagonal err EXACTLY 0; bare-(μ,P) violations CONFIRMED, rate .4395
   overall, concentrated at HEAD placements .60/.37/.34 head/mid/tail
   (`verifyL4_recheck_result.json`); max S/S_A = 1.54 in-sweep; constructed witness S=62 = 2.91×
   its booking). Days, not hours (verifier caveat accepted).
2. **F2 calibration** — core closed forms derived here (capture curve, required-R, kernel
   b∝r^{−3/2}); needs only 137's r-histogram to populate Δ(b) and per-generator R_eff. 1 session.
3. **F3 minimax** — simultaneous-commitment value = certified law ONLY on the full-scan-M
   baseline (see F3 revision); general move-order taxonomy + LP equilibrium at M≤33 doable but
   conceptually heavier (verifier's convention trap corroborates); guarantee-layer payoff later. Days.

## RECOMMENDATION (convention proposal for future papers)

Adopt **F1-form with F2-calibration**: state every positional-stratum law as the r̄-IDENTITY
with booked (μ_eff, P_eff, ρ_R, ρ_C; Λ) — never as a bare (μ,P) closed form (uniform-cell special
case, violated off-diagonal). Canonical measure b∝r^{−3/2} = DEFAULT reporting prior; report per
generator: capture curve, R_eff, κ_desc=C_desc/C₀. Use F3's baseline-EXPLICIT worst case as the
GUARANTEE booking — name the payoff baseline wherever a guarantee is claimed. Admissibility rule:
S_meas counts iff μ_eff ≤ 1/S AND raw-P̂ stored AND κ_desc reported; anchors whose feasibility
hinges on P̂'s 4th decimal (29.1) book "at resolution limit". Actions: (a) re-extract raw P̂ for 29.1
from 137/143 artifacts; (b) regenerate paper 219's anchor-table S_A values at stored P̂ + fix the
stale drafted-value rows and 4.35 prose locus (erratum rider); (c) add ρ_R to witness tables.

Provenance: this file + `gapL4_check.py`/`gapL4_result.json`. Round74 dir; not committed.

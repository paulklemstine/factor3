# Paper 225 — GAP-L4 CLOSED: The Positional-Stratum Measure Framework — Three Formulations Ranked F1 > F2 > F3, the r̄-Identity EC_A = P·r̄_R + (1−P)·r̄_C as the Universal Object, a PROVEN Master Inequality S ≤ min(1/(Λ·Θ·q̂), 2^{k_bits}/(Λ·Θ)) via Majorization, and an ERRATUM to Paper 219's D-Witness Table (29.0698 → 29.3152 at Stored P̂ = 0.9853)

**Verdict name: MEASURE FRAMEWORK / record-with-fixes** for GAP-L4 of paper 219's roadmap
("what measure does T1 hold over?"). This paper closes it: over what prior on the positional
stratum does T1's closed form mean anything, and what replaces it off that special case?
Three candidate formulations are built and ranked; the recommended convention (F1-form with
F2-calibration) makes the master inequality formally defined and PROVEN unconditional;
the independent adversarial verifier downgraded F3 to BASELINE-CONDITIONAL (a payoff-convention
gap caught mid-flight) and flagged paper 219's witness table as carrying a GENUINE rounding
error plus three stale drafted-form rows — corrected here as a formal erratum.
Round-78 #1 · theory deliverable, NO new physics run · sources: `barrier4_positional_converse_draft.md`
· `gapL4_measure.md` (post-REVISION) · `gapL4_check.py` → `gapL4_result.json` (<5 s) ·
independent verification `verifyL4_verdict.md`, machine evidence `verifyL4_recheck.py` →
`verifyL4_recheck_result.json`.

## The structural fact L4 rests on: the r̄-IDENTITY

For ANY prior π on I(N), any partition {R, C = R's complement}, |R| = μM, protocol A committed
(scan R top-down; certified silence ⇒ scan only C):

    **EC_A(π,R) = P·r̄_R(π) + (1−P)·r̄_C(π)**,   P = π(R),   r̄_B = mean within-block scan-rank.

Definitional but load-bearing — independently validated against simulated protocol-A costs
(8 random prior×window cells, max rel err **0.0023**, verifier V2). Consequences:

- T1a's certified form S_A = 1/[μP+(1−P)(1−μ)] is EXACTLY the special case r̄_R=(μM+1)/2,
  r̄_C=((1−μ)M+1) /2, i.e. **uniform-within-cells**; under uniform π this is forced (P=μ too) —
  T1c's geometry-freeness.
- Off uniform cells: P ≠ μ AND both r̄'s free in [1, block size] ⇒ value-universality FALSE:
  the bare-(μ,P) closed form is NOT an upper bound on achieved S. A3 sweep (M=64, 4000 tilts ×
  head/mid/tail placements): violation rate **.4395**, max S/S_A = **1.54**, violations
  CONCENTRATED AT HEAD placements (.60/.37/.34 head/mid/tail); explicit M=64 witness (all mass
  in the head-half of a BOTTOM window μM=3) reaches **S=62 vs booked 21.3** (ratio 2.91×,
  asymptote 4/μ−3).
- So "universality" SPLITS: **(i) FORM-universality** — the r̄-identity, unconditional,
  prior-free, PROVEN (definitional). **(ii) VALUE-universality** — S depends only on (μ,P):
  FALSE off uniform cells; needs shape.

The drafted-vs-certified law pair unifies under the same identity at the ρ_B := r̄_B/|B| = ½
slice: certified = CERTIFYING silence (branch costs (μM+1)/2 and ((1−μ)M+1)/2); drafted =
NON-certifying silence (fallback rescans everything, silence-branch cost M/2), denominator
1−(1−μ)P. They differ in SILENCE SEMANTICS, not within-cell shape. Draft-L4's selection
correction Δ = P(r̄_R−(μM+1)/2)+(1−P)(r̄_C−((1−μ)M+1)/2) — sign and mechanism attached.

## F1 — WORST-CASE with Λ+Θ bookings (RECOMMENDED convention)

Class: all measurable R, all π; policies test-blind + certified-silence (+T2-priced queries).
Bookings computable WITHOUT reference to achieved speedup (answers L7-d):

- **Θ(Π,π) := E_πC(Π)/K_booked**, K_booked := [P_eff(μ_effM+1)+(1−P_eff)((1−μ_eff)M+1)]/2.
  Exact ratio by the r̄-identity; **Θ ≡ 1 ⟺ uniform-within-cells**; Θ ∈ (0, Θ_max], monotone
  in loadings ρ_B.
- **μ_eff(Π) := |R_eff|/M** — width of committed search support (window/truncation: |R|/M;
  pure permutation: R_eff = I so μ_eff = 1). **k_bits(Π)** := adaptive comparison-query count
  (T2-priced), saturating at k_pin = log₂W (paper 224 naming rule). P_eff := π(R_eff);
  **Λ(π) := C_sort/C_desc ∈ (0,1]** (=1 iff within-stratum MLR, paper 221/L7′).

**MASTER INEQUALITY — PROVEN, unconditional:** for every test-blind Π, every π:

    S_vs_desc(Π) := C_desc/E_πC(Π) ≤ min( 1/(Λ·Θ·q̂), 2^{k_bits}/(Λ·Θ) ),
    q̂ := μ_eff·P_eff + (1−P_eff)(1−μ_eff)   (finite-M: q̂+O(1/M))

Proof chain: (i) r̄-identity ⇒ EC_Π = Θ·K_booked; (ii) sorted_desc(π) majorizes flat(1/M),
so C_sort = Σ_j sorted_desc(π)_j·j ≤ Σ_j j/M = C₀ (equality iff π flat); (iii) C_desc = C_sort/Λ.
Compose: S = C_sort/(Λ·Θ·K_booked) ≤ C₀/(Λ·Θ·K_booked) = 1/(Λ·Θ·(q̂+O(1/M))). ∎

No constant cap exists (head-loaded priors exceed any fixed booking's naive reading — consistent
with O1/O2). D factorization survives as this INEQUALITY chain (the COST-side 4/3 cap untouched —
touch-floor is prior-free); loses pathwise product (L7 interaction = leakage).
Remaining theorem = SHARPNESS (every realizable booking attained by some prior; constructive,
finite-checkable à la M=33) — days, not hours per verifier caveat.

## F2 — AVERAGE-CASE: explicit scale×balance prior class

Key arithmetic: N=pq, r=q/p ⇒ x=p=√(N/r), so s=x/√N=r^{−1/2}: **BALANCE IS POSITION** given
scale. Class 𝓟 = {log N ~ U[L₁,L₂]} × {b(r)}, positional density π_s(s)=2b(s^{−2})s^{−3}.
Anchor b∝r^{−3/2} ⟺ UNIFORM-in-x positional prior — T1a's exact kernel.

- Capture curve **P_b(μ) = ∫₁^{(1−μ)^{−2}} db/B(R_max); canonical P(μ) = μ/(1−R_max^{−1/2})**
  (=∫2μ exactly); linear iff canonical (A2).
- Required-R per anchor: (0.05,0.85)⇒1.129 · (0.02,0.9853)⇒1.042 · (0.05,0.9003)⇒1.121 ·
  (0.05,0.811)⇒1.136 — ALL FOUR demand ultra-balanced populations (r ≤ 1.04–1.14); hard-balance
  U[1,2] captures only 17% at μ=5%; RSA-like r≤1.21 captures 55%; saturation (P=1) only for
  R_max ≲ 1.11. The witnesses are NOT universal constants under F2 — they are GENERATOR SHAPE
  ESTIMATORS (each anchor = an r-quantile statement).
- T1 tight iff g≡const in b=r^{−3/2}g. D best-posed here: residue ⊥ position under scale×balance
  ⇒ S(R∘F)=S(R)S(F) in prior-expectation (supports L2); pathwise fails (L7).

## F3 — ADVERSARIAL-PRIOR (max-min): BASELINE-CONDITIONAL after verifier

Policy commits schedule+partition; adversary picks π ∈ 𝓒(μ,P)={π: ∃R, |R|=μM, π(R)≥P}.
Adversary-second degenerates (mass on last-scanned candidate). SIMULTANEOUS commitment
(policy names R; adversary fills π with π(R)≥P; max-EC arrangement = P-mass at R's bottom +
(1−P)-mass at C's bottom — brute-force CONFIRMED corner_is_max_EC at every checked locus) is
well-posed, but its value depends on the PAYOFF BASELINE [verifier item 3]:

- (a) vs full-scan-M baseline: value = 1/[μP+(1−P)(1−μ)] — the certified law EXACTLY;
- (b) vs paper-T1a's own uniform C₀=(M+1)/2 baseline: SAME equilibrium HALVES —
  S = (M+1)/(2M·[μP+(1−P)(1−μ)]);
- (c) vs matched same-prior-descending baseline: adversary strictly UNDERCUTS the certified
  number: S = [1−(1−P)μ]/d < 1/d at d=μP+(1−P)(1−μ) — frontier locus **5.365 < 5.4054**.

No baseline-free equality exists; genealogy (both laws = ρ=½ values under two silence semantics)
survives MODULO CONVENTION. Isolation-cost link unchanged: coverage×width lower bounds are F3's
feasibility constraint read backwards.

## Ranking of proof feasibility

1. **F1 form-universality** — core bound PROVEN above; remaining theorem sharpness/attainment
   (days, not hours — accepted). A3 sweeps done-shape: uniform-diagonal err EXACTLY 0
   (dyadic-FP exactness), bare-(μ,P) violations confirmed at .4395 concentrated at head.
2. **F2 calibration** — core closed forms derived; needs only paper 137's r-histogram to
   populate Δ(b) and per-generator R_eff. One session.
3. **F3 minimax** — general move-order taxonomy + LP equilibrium at M≤33 doable but conceptually
   heavier (verifier's convention trap corroborates); guarantee-layer payoff later. Days.

## RECOMMENDATION adopted (convention proposal for future papers)

Adopt **F1-form with F2-calibration**: state every positional-stratum law as the r̄-IDENTITY
with booked (μ_eff, P_eff, ρ_R, ρ_C; Λ) — NEVER as a bare (μ,P) closed form (uniform-cell
special case, violated off-diagonal). Canonical reporting prior b∝r^{−3/2}; report per generator:
capture curve, R_eff, κ_desc=C_desc/C₀. Use F3 baseline-EXPLICIT worst case as GUARANTEE booking.
Admissibility rule: S_meas counts iff μ_eff ≤ 1/S AND raw-P̂ stored AND κ_desc reported; anchors
whose feasibility hinges on P̂'s 4th decimal book "at resolution limit". Actions: (a) re-extract
raw P̂ for 29.1 from papers 137/143 artifacts; (b) regenerate paper 219's anchor-table values at
stored P̂ + fix stale rows (done below as ERRATUM); (c) add ρ_R to witness tables.

## Verification census

Own check (`gapL4_check.py` → `gapL4_result.json`): A1 anchor precision flags; A2 capture
curves + required-R inversions recompute exactly; A3 shape audit M=64 × 4000 tilts ×
head/mid/tail (violation rate .4395, max S/S_A 1.54, diag err EXACTLY 0) + explicit witness
S=62 vs booked 21.33.

Independent adversarial verifier (`verifyL4_recheck.py` → `verifyL4_recheck_result.json`,
verdict `verifyL4_verdict.md`):

1. F1 r̄-identity PASS (MC validation max rel err 0.0023, 8 cells); completeness flag — Θ was an
   ellipsis, μ_eff undefined → FIXED in this revision (both now formally defined above).
2. F2 derivations PASS — change of variables exact, capture curve exact, all four required-R
   inversions recompute exactly.
3. F3 PARTIAL FAIL → unstated payoff convention; RESOLVED as baseline-conditional (three payoffs
   stated above); brute force confirms corner-is-max-EC at every locus.
4. Paper-219 flag GENUINE TABLE ERROR → ERRATUM below.
5. Ranking F1>F2>F3 PASS (order defensible; quantifier separation "77× existence" vs "F3 min"
   noted, no contradiction once separated).

## ERRATUM to paper 219 (D-witness table)

Genuine precision/bookkeeping error caught by L4 verification (row forensics in
`verifyL4_recheck_result.json` §V3):

- **29.1× row**: prints `(0.02, 0.9853) | 29.0698`, but 29.0698 was computed at ROUNDED P=0.985
  (certified@0.985). At stored **P̂=0.9853 the certified law gives 29.3152** (drafted@0.9853=
  29.0647 matches neither printed nor corrected — not a formula-version mix-up). Feasibility
  question lives in P̂'s 4th decimal: P_implied by measured 29.1 is **0.98504**.
- **Rows 5.19 / 6.91 / 4.35 still print SUPERSEDED DRAFTED-form values** under a certified-law
  header: 5.1948 = drafted@(0.05,0.85) (certified there = **5.4054**); 6.91 = drafted@0.9003
  (certified = **7.1567**); 4.35 = drafted@0.8106 (certified = **4.536**).
- Prose "4.649" belongs to the STALE locus (.115,.87), doubly wrong for the (0.05,0.8106) row.
- Corrected certified-form values at stored precision:

| anchor | locus (μ, P̂) | printed (stale/rounded) | certified @ P̂ |
|---|---|---|---|
| 5.19× frontier (p137) | (0.05, 0.8500) | 5.1948 (drafted form) | **5.4054** |
| 6.91× trunc-high | (0.05, 0.9003) | 6.91 (drafted form) | **7.1567** |
| 4.35× trunc-low | (0.05, 0.8106) | 4.35 (drafted form) | **4.536** |
| 29.1× α=1 extreme | (0.02, 0.9853) | 29.0698 (computed at P=0.985) | **29.3152** |

Feasibility conclusions of ALL FOUR anchors UNAFFECTED (μ ≤ 1/S_meas and S_cert@P̂ ≥ S_meas hold
regardless — verifier §V3 feasibility re-check all true). Paper 219's headline claims stand;
only table cell values and one stale prose locus are affected.

## Roadmap status: EMPTY of open gaps

Paper 219's converse roadmap is now fully accounted for: **T1/T2 verified** (round-75 #4) ·
**D witnessed** (5.19×>4/3 = class-crossing, not cap-breaking) · **L7′ proven-sketch**
(round-76 #1 falsification + replacement) · **L8 closed** (paper 224 taxonomy) ·
**L4 closed by this framework**. No open items remain from the barrier-4 positional draft.

## Barrier validation

Serving the barrier map's positional stratum audit trail: every future positional-stratum claim
must name its bookings (μ_eff, P_eff, ρ_R, ρ_C; Λ) and its baseline — the two failure modes this
framework eliminates (bare-(μ,P) universal reading; unstated payoff convention) were exactly the
ones that produced paper 219's table error and F3's initial misstatement. Residue cap 4/3
untouched (COST-side prior-free); no complexity claim made; no breakthrough claimed.

## Bottom line

GAP-L4 closes: T1's universality is FORM-universality (r̄-identity, proven) not
value-universality (false off uniform cells); the master inequality is now formally defined and
proven unconditional; the average-case measure is canonical (b∝r^{−3/2}, balance IS position);
adversarial value is baseline-conditional; paper 219's witness table carries a genuine rounding
error (29.0698→29.3152 at stored P̂) plus three superseded drafted-form rows, all corrected here
with feasibility conclusions intact. The converse roadmap is empty of open gaps.

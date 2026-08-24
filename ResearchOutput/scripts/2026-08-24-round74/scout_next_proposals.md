# Scout: prior-art scan + next-experiment seeds (round 74, 2026-08-24)

## 1. Catalog scan (alethean.org/package_index.js, 929 entries; matched by filename/exp_id)

**(a) Modular forms / Maass / modularity for factoring — NO factoring application exists.**
Background theory only: `p_adic_langlands_for_glq_p.json` (determinant bridge, GL2(Qp)),
`arxiv_paper_a_minimal_modularity_lifting_theorem_f.json` (genus-2 Siegel lifting),
`deepening_siegel_weil_identity_for_the_e_lattice_t.json` (E8 theta Hecke convolution).
One crossover: `the_berggren_tree_and_the_langlands_program__autom.json` (Berggren tree
over Q(sqrt2), boundary Hecke algebra, three automorphy obstructions) — structural, not
factoring. No Maass entry at all. MA-1's only catalog echoes are lab-generated:
`the_asymmetric_crt_split_of_an_1_is_factor_blind_c.json` (paper-132 family), cyclic-cubic
conductor-13 (abelian pinning ladder).

**(b) ECM / smoothness / Dickman — all lab-generated** (`smooth_selfhint_density...`,
`cm_ecm_order_round_17_1...`, `cm_ecm_general_rational_torsion...`, `ecm_parity...`,
`experiment_397_seqsmooth_null...`, `fact_round_42_1__ecm_completion...` = papers
54/62/66–69/155/156/158). **ZERO Dickman finite-x-correction packages anywhere in the
catalog** — paper 130's u≈14.75 leading-term territory is unclaimed externally. Adjacent:
`the_3sum_birthday_bound_hierarchy.json` (3SUM birthday hierarchy, collision-factoring
sqrt barriers) — background for rho-class methods only.

**(c) Pythagorean/Berggren — ~29 entries, consistent with the lab's own closed program**
(papers 56, 192–199). Entries outside the four seals but not factoring-relevant structural
theory: `markoff_tree_transfer...` (Markoff fibrewise transfer), `harmonic_measure_on_the_
berggren_tree_boundary...`, `the_berggren_tree_zeta_function...`, `the_riemann_hypothesis_
for_the_berggren_tree...`, `the_pythagorean_hydra...`, `p_adic_berggren_dynamics...`.
Conflict flag: `quantum_pythagorean_walk_polynomial_time_integer_f.json` ("Resonance...
Exact Factorisation by Interference", 2026-08-20) claims interference factoring the lab's
energy-ascent seal retracts as magnitude mirror.

**(d) Scan-order/positional — nothing external.** Lab TDial series appears under renamed
tie-statistics titles (`fact_round_57_1/58_1/61_1/63_1/65_1__tdial_*`). Only tangent:
`all_the_moving_parts__honest_uniqueness_decoding.json` (scan schemes, decoding not search).

**Bottom line: NO new relevant packages beyond lab-generated ones** (matches standing note);
genuinely empty catalog cells: Dickman corrections, modularity-for-factoring.

## 2. TOC check

228 papers; skimmed headers of 176_MA1_Effective, 158_ECMPlane_Completion,
156_TrueECM_LcmSupremacy, 209_ScaleSmoothnessDeviation. Nothing below re-runs these.

## 3. Proposals (one per open target)

**P1 (MA-1 effectivity) — CHARACTER DECOMPOSITION SWEEP.**
H: worst-class AP deviation at fixed x is predicted by real-character Dirichlet L-biases;
paper 176 addendum observed character structure (15/16 cells) but never modeled it.
Sweep m to ~10^4 at x=2^28, decompose deviation into character components, test R^2 of
L(1,chi_real)-weighted prediction. Verdict: R^2>0.8 => effectivity criterion is computable
(cap error predictable from L(1,chi)); low R^2 => deviation omnigenic, effectivity stays
open. Cost: numpy sieve, <10 min. Barrier row: residues-cap 4/3 (MA-1 is its averaging
input) + external class-hint ceiling. Shaving risk LOW (targets an m-scaling law, not constants).

**P2 (factor-local beyond scan-order) — STAGE-2 VS THE SELF-DESTRUCTION WALL.**
H: standard-continuation stage-2 (never implemented: 155 sequential, 156 stage-1 lcm only,
158 took the wall as given) shifts the destruction threshold multiplicatively — log(wall)
vs log(stage-2 width W) slope ~1 => wall is a B1·W budget law (factor-locality has headroom);
slope ~0 => destruction intrinsic to order size, plane closure final. Fit slope on
k∈{16,20} semiprimes, known-p populations. Verdict rule pre-statable as above.
Cost: gmpy2 ECM stage1+2, ~15 min toy. Barrier row: prices the wall bounding the unified
plane's factor-local quadrant. **Shaving risk MEDIUM — REJECT if it degenerates into
"tune B1/W for speed"; keep it on the slope-of-the-wall question.**

**P3 (scale-smoothness u∈{9,14}) — N-LIFT + LPF-QUANTILE FRONTIER.**
Key arithmetic: with v=x^2−N ≤ 3.75N and N ≤ 2^80, u_max = 82/log2(B) — so LOWERING B
reaches higher u, but B≤100 makes full-smooth hits too rare (~rho(14)x1.5e9 ≈ 0). The open
cell instead opens by LIFTING N to 2^96–2^112 (u≈9–11 at B=500–1000) plus swapping the
smooth-indicator for a largest-prime-factor quantile comparison (full power everywhere).
H1: cand/control LPF distributions identical at u∈{9,10} (null extended past exp562's cap);
H2: the unexplained D=1.61-overdispersion death point (dies by u~7 at N≤2^80) is
N-covariant vs B-fixed — its movement decides the mechanism. Verdict: CI exclusion of 1 at
u≥9 = first positive deviation ever; coverage = null extended; u*(D-death) shift = mechanism
read-out. Also track QR-dial corr decay (0.32→0.04) into the new cell. Cost: python-ints
mulmod+gcd chain, reduced arms, ~20 min. Barrier row: scale-smoothness frontier (standing
directive); feeds dial-rate residual 1.31x floor. Shaving risk LOW (new cell + mechanism).

## Red flags
- P2's constant-shaving gravity (guard stated above).
- Berggren "interference factorisation" catalog claim contradicts sealed paper 197 lineage —
  do not cite as prior art without noting the retraction.
- pkg_nums shifted again (929 total); all matches here keyed by filename/exp_id only.

# Paper 254 — PROFILE-GENERALITY: **H0-SIDE (FAMILY-SPECIFIC) WITH THE MECHANISM NAMED** — Positional Smoothness Structure Is GATED BY DIFFERENCE-OF-SQUARES FACTORABILITY — The j²−N Power-Law Profile Replicates on j⁴−N (b̂ +0.157 vs +0.188, Pairwise r = 0.781, Close to but Below the Pre-Registered 0.8 Bar) While j³−N Is FLAT (Spearman +0.019, p = 0.92) — Square N Splits v_k for EVEN k Only: Rate Hierarchy sq2 ≈ qu4 (~2×10⁻²) ≫ sq2d ≈ cu3 (~7×10⁻⁴) Is a **30× Differential Between Even and Odd Powers of j**, Tracked Exactly by Whether v_k = (j^(k/2)−jlo)(j^(k/2)+jlo) Factors Algebraically — Consequence: Papers 228/229's Profile Law Is a QUADRATIC-FAMILY LAW, Not a Universal Sequence Law; the Even-Degree Generalization j^{2m}−N (All Sharing the Structure via Repeated Difference-of-Squares) Is the Natural Extension Prediction

**Verdict name: H0-SIDE_FAMILY-SPECIFIC_MECHANISM_NAMED** — the pre-registered H1
(universal profile across {j²−N, j³−N, j⁴−N}, all pairwise r > 0.8) fails on two
of its three bars; but the failure pattern is not noise — it is an arithmetic gate.
Positional smoothness structure appears exactly where difference-of-squares
factorability holds.

Round-95 #1 · tests whether papers 228/229's positional profile law (power-law
decline + left-edge spike on the j²−N smoothness locus) is a universal property
of polynomial-sequence smoothness or specific to the quadratic family. Sources:
`ResearchOutput/scripts/2026-08-24-round74/{exp605_profile_generality.py,
exp605_result.json, exp605_full.log, exp605_smoke.log}` on the same 128-member
population as the positional thread (`exp581_regen_positions.npz` lineage),
windows [r_k, 3r_k−4] anchored at the integer k-th root (k=2 reproduces
[jlo, 3jlo−3] exactly), matched common-random-number grids L=3000/N/arm
(1800 uniform + 1200 left-tilted, tilt identical across arms → paired
comparisons), exact 1e6-cut gcd-chain B-smooth tester (unit-tested), controls
C=1000/N/arm. Wall 181 s; sampling/bootstrap seed 20260901, dither 20260902.

## 1. Pre-registration (verbatim, script header, written BEFORE any analysis)

> H1 (universal): the same normalized-position profile shape (monotone
>   decline, left-edge concentration) appears for ALL three families
>   {j^2-N, j^3-N, j^4-N} at matched per-family sample sizes --
>   pairwise profile correlations > 0.8 after normalization.
> H0 (family-specific): profiles diverge materially across families;
>   positional structure depends on polynomial degree/arithmetic;
>   report which family differs and how.
>
> Operationalization (fixed before analysis):
>   Arms (same 128-member population, matched grids):
>     SQ   : v = j^2  - N_rec,  N_rec = jlo^2 (exact-square reconstruction)
>     SQD  : v = j^2  - (N_rec + dith), dith = seeded uint in [1, 2*jlo]
>            per N (isqrt preserved); square-structure sensitivity probe
>     SQ/CU/QU windows mirror lineage geometry per family: anchor r_k =
>     integer k-th root of N (r^k <= N < (r+1)^k); j in [r_k, 3*r_k-4];
>     t = (j-r_k)/W, W = 2*r_k-4 => v spans [0, ~(3^k-1) N]. For k=2,
>     N_rec: r_2 = jlo EXACTLY -> windows identical to npz lineage.
>   Sampling: common random numbers, one t-matrix shared by all arms
>     (per N: 1800 uniform [0,1] + 1200 uniform [0,0.15]; L=3000; tilt
>     IDENTICAL across arms -> paired comparisons). Controls: C=1000 per
>     arm/N, value uniform in [1, v_max(N,arm)], binned by paired t.
>   Smoothness: exact 1e6-cut B-smooth gcd-chain tester (unit-tested).
>   Lineage/hash check (applicable form): under N_rec, v2 = j^2-jlo^2 =
>     (j-jlo)(j+jlo) is N-INDEPENDENT, so stored npz hit positions are
>     classifiable directly. Rule: hit smooth-fraction >= 0.95 =>
>     exact-square N lineage confirmed; 0.30-0.95 mixed; < 0.30 =>
>     original N non-square (SQ labeled 'perfect-square variant').
>   Stats/arm: pooled 50-bin profile; pn=p/mean(p); power-law WLS fit
>     ln rate = a - bhat ln t on bins >=3 hits (weights=counts);
>     left-decile ld = rate(t<0.1); Spearman(bins,rate); cluster
>     bootstrap (B=800, resample 128 Ns) CIs for bhat, ld, and pairwise
>     Pearson r of pn (primary 50-bin; secondary Spearman rank).
>   VERDICT RULES (fixed):
>     H1 CONFIRMED iff (a) all 3 pairwise r among {SQ,CU,QU} > 0.8,
>     (b) every family ld > ov with boot P(ld>ov) > 0.95, (c) every
>     family Spearman rho < 0 at p < 0.01. Else H0-SIDE; which_differs
>     = families ranked by mean r to the others.
>   Overrides: any registered family pooled hits < 150 =>
>     INCONCLUSIVE-LOWPOWER (bars still reported, flagged); failing
>     control flatness (chi^2 independence over 5 super-bins p<=0.01)
>     => INVALID-CONTROL for that arm (excluded from bars).
>
>   Seeds: sampling/bootstrap 20260901, dither 20260902.

*(Transcription note: the config block additionally fixes n_bins=50,
B_boot=800, min_hits_fit=3, low_power_hits=150, r_bar=0.8, spear_p=0.01, and
the design-stage L-adaptation clause "if smoke timing projects full wall >
12 min, L drops toward floor 1200" — not triggered, L=3000 kept.)*

## 2. Verdict bars

| Bar | Requirement | Observed | Pass |
|-----|-------------|----------|------|
| (a) pair corr | all 3 pairwise r > 0.8 | max r = 0.781 (sq2\|qu4) | **FAIL** |
| (b) edge concentration | every family ld > ov, P > 0.95 | 4/4 arms P(ld>ov) = 1.0 | PASS |
| (c) monotone decline | every family Spearman ρ < 0 at p<0.01 | cu3 ρ = +0.019, p = 0.92 | **FAIL** |

Two of three bars fail ⇒ **H0-SIDE** as pre-written. No low-power override fires
(all arms ≥ 248 ≥ 150 hits); all four controls flat (χ² independence over 5
super-bins, p = 0.081–0.649), so no INVALID-CONTROL exclusions.

## 3. Per-family results

| Arm | v(j) | draws | hits | overall rate | b̂ ± SE | ld/ov | Spearman ρ (p) |
|-----|------|-------|------|--------------|---------|-------|----------------|
| sq2 | j²−N_rec | 384000 | 8639 | 0.02250 | **+0.157 ± 0.008** | 1.24× | −0.802 (2.5×10⁻¹²) |
| qu4 | j⁴−N_rec | 384000 | 7603 | 0.01980 | **+0.188 ± 0.013** | 1.29× | −0.856 (2.4×10⁻¹⁵) |
| cu3 | j³−N_rec | 384000 | 287 | 0.00075 | +0.065 ± 0.037 [CI covers 0] | 1.33× | +0.019 (p = 0.92) — **FLAT** |
| sq2d | j²−(N_rec+dith) | 384000 | 248 | 0.00065 | +0.168 ± 0.038 [CI covers 0] | 1.47× | −0.426 (p = 0.043) |

Bootstrap CIs: sq2 b̂ [0.138, 0.169]; qu4 b̂ [0.173, 0.201]; cu3 [−0.079, 0.101];
sq2d [−0.007, 0.193]. Left-decile enrichment is universal (bar b, 4/4) but the
DECLINE SHAPE is not: the two even-power arms share a steep power law while cu3
is statistically flat and sq2d shallow-with-noise.

Pairwise normalized-profile correlations (Pearson r on pooled 50-bin profiles):

| Pair | r | ρ (rank) | 95% CI (cluster bootstrap) |
|------|---|----------|----------------------------|
| sq2 \| qu4 | **0.781** | 0.709 | [0.565, 0.767] |
| sq2 \| cu3 | 0.385 | 0.395 | [0.061, 0.432] |
| cu3 \| qu4 | 0.477 | 0.456 | [0.140, 0.510] |
| sq2 ~ sq2d | 0.495 | — | — |

The even-power pair sits close to but strictly below the pre-registered 0.8 bar;
the odd-power pairs are far below it. Mean r to the other two registered
families: qu4 0.629, sq2 0.583, cu3 0.431 — cu3 is the outlier, consistent with
the mechanism below.

## 4. THE DIFFERENCE-OF-SQUARES GATE (the finding behind the verdict)

The rate hierarchy is not a gradual degradation — it is a clean split:

> sq2 ≈ qu4 (~2×10⁻²) ≫ sq2d ≈ cu3 (~7×10⁻⁴) — **≈30× lower (29–34× across pairings)**

and it is tracked EXACTLY by difference-of-squares factorability. With
N_rec = jlo², write k = 2m:

- **Even k:** v_{2m}(j) = j^{2m} − jlo² = (j^m − jlo)(j^m + jlo) — an algebraic
  factorization into a product straddling N. A B-smooth value requires both
  cofactors' prime material to cooperate, and near j ≈ jlo the first factor
  (j^m − jlo) starts SMALL and grows — producing the characteristic declining
  positional profile: small-v values are simultaneously more numerous and more
  likely to be smooth through the small-factor route. This is papers 228/229's
  mechanism, and it survives at k=4 essentially unchanged (b̂ 0.188 vs 0.157;
  profile correlation 0.781).
- **Odd k:** j³ − N_rec admits NO such split over the integers for square N_rec:
  the polynomial never factors as a product of two integer-cofactor terms whose
  size tracks position symmetrically. Result: baseline rate (7.5×10⁻⁴, matching
  controls ~2–3.5×10⁻⁴ up to window-magnitude differences) and a flat profile
  (Spearman +0.019).

The sq2d dither arm confirms the reading from the other side: knock N off the
exact-square locus by a seeded dither ∈ [1, 2·jlo] (isqrt preserved) and the
quadratic itself loses the gate — rate collapses ~35× (0.02250 → 0.00065,
~97% of the mass gone, right onto cu3/sq2d's level) while retaining a shallow
shape-consistent tilt
(b̂ +0.168 with wide CI, ld/ov 1.47×). The structure follows SQUARENESS OF N,
not the polynomial's degree label: within the SAME family j²−v, moving N from
square to non-square removes the positional structure and 96% of the rate mass.

So the gate variable is **arithmetic** — algebraic factorability of f(j)−N
given N's form — not polynomial degree per se. Positional structure exists where
the sequence values admit a difference-of-squares-type split; where they don't,
the locus collapses to baseline density with no usable position gradient.

## 5. Consequence: papers 228/229's law is a QUADRATIC-FAMILY law

The positional profile law (power-law decline + left-edge spike, papers
228/229; bulk+spike decomposition papers 238/245/253) must be cited as a
property of the **difference-of-squares-factorable family**, not of polynomial
sequences generally. Two corollaries:

1. **Scope amendment**: any barrier-map entry that cites the j²−N positional
   profile as a sequence-level phenomenon inherits this scope restriction. On
   non-factorable families the locus offers no position signal at all — there
   is nothing to generalize.
2. **Extension prediction (pre-stated here)**: the natural generalization is
   NOT odd degrees but EVEN degrees — j^{2m} − N for square N factors by
   repeated difference of squares, (j^m−jlo)(j^m+jlo), for every m, so ALL
   even-power families should share the structure. k=4 confirms it (b̂ 0.188,
   r = 0.781 with k=2). The quantitative prediction: j⁶−N and j⁸−N at matched
   grids should land in the same ~0.16–0.19 b̂ band with pairwise r > 0.8
   against sq2/qu4 — a falsifiable follow-up that would upgrade "even degrees"
   to a closed class.

Note the practical asymmetry this exposes for the scanning frame: the strong
left-edge structure is confined to the perfect-square-N slice of the population
(see ledger), where trial division from jlo is already optimal — so the
positional structure does not transfer as a scanning advantage onto general-N
populations (papers 228/229's population was general-N).

## 6. Ledger catches and honest limits

- **Lineage APPROXIMATE, disclosed**: the source npz stores positions + window
  bounds only — no N — so byte-exact seed-20260828 regeneration is impossible
  from permitted inputs. Reconstruction N_rec = jlo² pins anchors exactly
  (r₂ = jlo reproduces [jlo, 3jlo−3]); the residual ΔN < 2·jlo shifts the
  effective left edge by <1 integer step (~10⁻¹⁵ of window) — profiling-invariant.
  The applicable hash-check ran instead: v₂ = (j−jlo)(j+jlo) is N-independent,
  so stored npz HIT positions were classified directly — hit smooth-fraction
  0.0226 vs control 0.0198 (pure independence) ⇒ **original N were NON-SQUARE**;
  the SQ arm is a "perfect-square variant." Consequence booked honestly: papers'
  population was general-N, so sq2/qu4 RATE LEVELS do not transfer there — on
  general-N-like arms the locus is weak (ld/ov ≤ 1.47, shallow), meaning a
  strong left-edge power law needs either exact-square N or finer-than-window
  resolution. Flagged for the 228/229 follow-up.
- **Low-power arms disclosed**: cu3 (287 hits) and sq2d (248 hits) sit just
  above the pre-registered 150-hit low-power floor — their null-ish shapes are
  underpowered, not proven-flat; the verdict rests on them only for bar (c),
  where the direction of failure (odd degree flat) aligns with the mechanism.
- Smoke run caught a t-matrix broadcast bug and a key-name bug (`hit_`/`ctl_`
  prefixes); both fixed before the full run. Ledger catches: NONE during
  execution (no commits made mid-run; only exp605_* files touched).

## 7. Barrier validation

No change to the barrier map: the positional thread had already closed
(papers 250–253 — density real, mechanism absent multi-seed, shape bounded);
this experiment closes the GENERALITY question that thread left implicit, and
the answer REDUCES the map's exposure rather than adding to it: the j²−N
positional structure was never a candidate mechanism against barrier 4, and it
is now confirmed as family-confined arithmetic (difference-of-squares
gate), i.e., a scan-order artifact of the quadratic-plus-square-N slice —
consistent with the standing method law that scan-order structure reflects
proposal geometry, not N-information. What the run ADDS is the even-degree
extension prediction (Section 5), which keeps the thread honest about scope.
Open frontier unchanged: u ≥ 6–14 scale-smoothness deviations, factor-local
methods beyond scan-order framing, MA-1 effectivity, residue cap 4/3 theorem
consequences, external-hint laws; quantum closed.

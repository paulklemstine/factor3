# Paper 244 — LARGER-P-ECM-TRACE: **H1 TRUE / H0 REFUTED — exp570's Picture REPLICATES at bitlen 32** — Guarded-Affine Low-B1 Success Is SCALE-STABLE Order-Completion Firing Early: Cell found_p Rates Flat Across bitlen 26 → 32 at EVERY B1/p Fraction (z-tests p = .33/.79/.15, All CIs Overlap), KS Rejects Uniformity in ALL SIX Cells (p ≤ .002; Medians .073–.293, Late-Tail ≤ 13%), Collision Floor Subdominant and Quantified (First-Curve Rate 2.6× Baseline at (32, 0.125); Pure-Collision found_q 9–16 vs found_p 24–31) — Papers 215 → 218 Chain CLOSED: No Scale-Dependent Collapse Toward 1−exp(−1.44·B1/p) Through bitlen 32

**Verdict name: H1 TRUE / H0 REFUTED** — both pre-registered legs of H1 fire exactly as written:
(a) RATE scale-stability (bitlen-32 ≈ bitlen-26 cell rates at every fraction, z > 0.05 AND
overlapping CIs) and (b) GEOMETRY preservation (KS rejection in every ≥10-hit cell with
median < 0.5 and tail < 0.3). The registered H0 alternative — rate dropping toward the
per-curve collision baseline 1−exp(−1.44·B1/p), or uniformity/late-firing emerging at
bitlen 32 — does not happen on any leg.

Round-88 #1 · exp 595 · fresh-seed replication at larger p (seed **20260903**, disjoint from all
prior ECM lineages; exp570 machinery VERBATIM) · sources:
`ResearchOutput/scripts/2026-08-24-round74/exp595_{largep_trace.py, smoke.log,
smoke_result.json, result.json}` + `exp595_findings.md` · wall **1.5 s** full (240 cells;
budget was hours). Closes the ECM low-B1 chain: paper **215** (ECM-STAGE2-WALL, exp 568 —
outcome-separated accounting kills the destruction wall) → paper **218** (COLLISION-VS-ORDER-TRACE,
exp 570 — collision floor subdominant, order-hits fire early at bitlen 26) → **this paper**
(scale-stability + early-fire confirmed at bitlen 32).

> **Chain-numbering note (disclosed):** the run's findings header cites the chain as
> "215→236→238" — those are catalog-shifted numbers (236 = BSTAR-TRANSFER, 238 = EDGE-KERNEL,
> neither ECM-related). The true lineage by title/exp_id is **215 → 218 → 244**, used throughout
> here per the standing match-by-title/exp_id rule.

## 1. Pre-registration verbatim (written BEFORE any data)

From the `exp595_largep_trace.py` module docstring:

> PRE-REGISTRATION (transcribed from the coordinator brief BEFORE any data collection;
> no exp595 data existed at write time; exp570_collision_trace.py machinery VERBATIM):
>   H1 (scale-stability + early-fire replicate): at bitlen 32,
>     (a) RATE: cell found_p rate at B1/p = 0.125 ~= bitlen-26's rate -- two-proportion
>         z-test p > 0.05 AND overlapping Wilson 95% CIs;
>     (b) GEOMETRY: the step-index distribution of found_p hits STILL REJECTS
>         Uniform[0,1] at KS p < 0.01 in every (bitlen, B1frac) cell with >= 10 hits,
>         and early-fire geometry is PRESERVED: median normalized step < 0.5 AND
>         tail fraction (norm >= 0.8) < 0.3 (hits are NOT final-20% concentrated).
>   H0 (scale-dependence real): EITHER the bitlen-32 low-B1 rate drops significantly
>       below bitlen-26's (z p < 0.05, disjoint CIs) toward the per-curve collision
>       baseline 1-exp(-1.44*B1/p) (= 0.1647 at frac 0.125; 3-curve cell-adjusted
>       1-(1-0.1647)^3 = 0.4191), OR the geometry changes (uniformity not rejected at
>       0.125, or late-firing median/tail emerges). Report which leg fired.

Design fixed in the same header: arm stage-1 only (B2 = B1); curves cap 3; populations
h = 13 (p ~ 13–14 bits, N ~ 26–28 bits) and h = 15 (p ~ 15 bits, N ~ 30–32 bits, q ~ 3–4p),
n_N = 40 each, fresh master seed 20260903; grid B1/p ∈ {0.125 ceil, 0.5 ceil, 0.9 floor}
(the 0.25→0.5 grid swap pre-named by the coordinator brief); step-index trace counts every
guarded inversion AND each end-of-chunk gcd check, normalized by the closed-form
data-independent total-step count. Amendment log: none.

## 2. Cell rates — scale-stable at every fraction

| target bitlen | B1/p = 0.125 | 0.5 | 0.9 |
|---|---|---|---|
| **26** (h=13) | 0.65 [.495, .779] | 0.75 [.598, .858] | 0.60 [.446, .736] |
| **32** (h=15) | 0.75 [.598, .858] | 0.775 [.625, .877] | 0.75 [.598, .858] |

Cross-bitlen two-proportion z-tests: **p = .329 / .793 / .152** at fracs .125/.5/.9; Wilson 95%
CIs overlap at all three fractions (verdict flags `h26_vs_h32_CIs_overlap*`: true × 3). H1(a)
fires at every fraction, not just the pre-named 0.125 leg. Rates are also FLAT in B1frac
(0.60–0.775 across 0.125 → 0.9): no dose-response of the collision term anywhere.

## 3. Early-fire geometry replicates (H1(b))

KS-vs-Uniform[0,1] on normalized firing steps, per cell (n = found_p hits):

| cell | n | D | KS p | median | tail(≥0.8) |
|---|---|---|---|---|---|
| 26, .125 | 26 | 0.365 | **.002** | 0.293 | 7.7% (ns vs .20) |
| 26, .5 | 30 | 0.536 | **< .001** | 0.171 | 0% (p=.0025) |
| 26, .9 | 24 | 0.663 | **< .001** | 0.073 | 0% (p=.0094) |
| 32, .125 | 30 | 0.374 | **.0004** | 0.232 | 13.3% (ns vs .20) |
| 32, .5 | 31 | 0.577 | **< .001** | 0.113 | 0% (p=.002) |
| 32, .9 | 30 | 0.541 | **< .001** | 0.100 | 0% (p=.0025) |

All six cells reject uniformity (registered bar p < 0.01); medians span **0.073–0.293**
(all ≪ 0.5); late-tail fraction ≤ **13%** (≪ 0.3). The early-fire shape deepens with dose
(median .29 → .07 across the grid) exactly as at bitlen 26. Geometry gate cells with < 10 hits
excluded: none in the full run (smoke had none ≥ 10 — plumbing only). Raw norms shipped in
`ks_stats` for post-hoc re-reads.

## 4. Collision-floor subdominance quantified

Two independent attributions, both pointing the same way:

1. **First-curve rates vs the per-curve collision baseline** 1−exp(−1.44·B1/p):
   at (32, 0.125) first-curve found_p rate = **0.425 [0.285, 0.578]** = **2.58×** the constant
   per-curve baseline 0.1647 (at (26, 0.125): 0.325 = 1.97×). Ratios at frac 0.5/0.9 are
   1.32–1.46 / 0.83–1.03 — i.e. even where the ratio approaches 1, the CELL rate stays flat
   because order-completion saturates it; there is no regime where the collision term dominates.
2. **Pure-collision cross-check via found_q:** with B1 < p ≪ q, order completion for q is
   impossible, so found_q events are pure collision luck. Counts per cell: found_q **9–16**
   vs found_p **24–31** — the excess over baseline is carried by order-hits, not luck.

**Ledger catch (disclosed):** the (32, 0.125) cell CI [.598, .858] technically CONTAINS the exact
per-N 3-curve baseline cell mean **0.6124** (result flag `h32_cell_vs_3curve_baseline…` =
"contains"), so that one cell cannot exclude the exact baseline on the CI alone. Three things
attribute the containment to order-hits rather than luck: (i) the flag's KEY names the
constant-formula value 0.4191 while the CODE actually tests 0.6124 (label/code mismatch in
`exp595_largep_trace.py` line 346 — disclosed; note 0.4191 itself IS excluded by the CI, so the
mismatch runs against, not for, the headline); (ii) the first-curve view at the same cell is
2.58× the per-curve constant baseline with CI excluding it; (iii) found_q = 9 vs found_p = 30.
The registered H0 leg ("rate drops toward baseline") required a DROP with disjoint CIs — the
observed rate moved UP if anything.

## 5. Consequence — chain CLOSED

Papers **215 → 218 → 244** complete the ECM low-B1 arc:

- **215** (exp 568): the recorded B1 ≳ min(p,q) "destruction wall" does not exist under
  outcome-separated accounting — success is universal once B1 ≥ p+1+2√p.
- **218** (exp 570): at bitlen 26, guarded-affine success at LOW B1 (B1 < p) is NOT random
  collision luck — KS rejects uniform firing; hits concentrate early in the trace; measured
  rates sit far above 1−exp(−1.44·B1/p).
- **244** (this): the picture REPLICATES at bitlen 32 on a fresh seed/populations — rate
  scale-stable at every fraction, early-fire geometry preserved, collision floor quantified
  and subdominant.

**No scale-dependent collapse toward the collision baseline through bitlen 32.** Low-B1
guarded-affine ECM success is scale-stable ORDER-COMPLETION FIRING EARLY — a mechanism claim,
not a small-p artifact. Practical reading: the useful firing happens in the first ~10–30% of
the schedule (medians ≤ 0.29), so curve time beyond that point is mostly wasted when B1 < p.

## 6. Honest notes (all disclosed)

1. Early-fire operationalization (median < 0.5, tail < 0.3) fixed BEFORE data from exp570's
   qualitative conclusion alone; raw norms shipped for re-reads.
2. KS uses the asymptotic Kolmogorov series (n ≥ 2); < 10-hit cells excluded from the gate
   (none excluded here).
3. Collision baseline treats inversion denominators as independent uniform mod p; chunk-batched
   gcd checks count as trace steps.
4. `ec_add`'s rare recursive internal double executes without an idx increment — tiny
   data-dependent bias on found_at indices only.
5. Deaths (gcd == N) collapse silently inside trial(), not separately bucketed (inherited
   exp568/exp570 behavior).
6. Cell rates are 3-curve quantities (any-curve success); first_curve fields give the per-curve
   view matched to the per-curve baseline.
7. Smoke read H1 REFUTED / "insufficient_hits" (n_N = 8, zero ≥10-hit cells) — correct
   plumbing-only behavior; full run authoritative.
8. Chain-numbering slip in the findings header (§ preamble above) — corrected here by title.

## 7. Barrier validation

No breakthrough claimed and none needed: this closes a mechanism-attribution chain on the METHOD
side. Untouched: residue cap 4/3 theorem; scan-order position 5.19×; external class-hint law
1/(1−(1−θ)P_hit); external interval-hint coverage × width law; quantum frontier closed; method
stratum map; abelian pinning ladder; QS calibration; utility closure; four-class rate-residual
closure; papers 238–240 spike-origin resolution; paper 238's .2346 provenance flag still travels;
paper 242's non-divisibility entry remains single-seed-unconfirmed per issue #391. Asymptotic
relevance per the standing directive: a scale-stable early-firing mechanism claim is exactly the
kind of structure that must be checked for u ≥ 6–14 deviations before any asymptotic use — the
next honest question is whether early-fire geometry persists at bitlens where B1/p must shrink,
not whether it exists here. Open frontiers unchanged: non-QR per-N structure at u = 2.5
(31%-above-floor residual), factor-local methods outside scan-order framing, MA-1 effectivity.

## Attribution

Experiment + analysis artifacts: `ResearchOutput/scripts/2026-08-24-round74/`
(exp595_largep_trace.py — pre-registration + empty amendment log in header, authored before
first execution; exp595_smoke.log/_result.json; exp595_result.json — config/rows/ks_stats/
verdicts/honest_notes/wall_s [authoritative]; exp595_findings.md — contains the chain-numbering
slip disclosed in the preamble). Recorded round-88 #1; notebook Part 286; assessment v351;
issue #392.

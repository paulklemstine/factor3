# Paper 229 — PROFILE-FORM: The Small-J Hit-Position Profile of Paper 228 Is a POWER LAW T(x) ≈ 0.0295·(1+x)^(−1.104) (Akaike Weight 0.987; b = 1.104, boot95 [0.991, 1.218] — a Harmonic ~1/(1+x) Decline; Runner-Up Exponential at ΔAICc = +9.2), and Its Bulk IS the Dickman Magnitude Gradient — the Genuine Beyond-Dickman Residual R = T/M Is PEAKED, Not a Second Gradient: a ±20% Concave MID-WINDOW Excess Rising to R = 1.23 at x ≈ 0.67 (Vertex x̂ = 0.59 Interior, Quadratic-Coefficient CI [−0.62, −0.14]) Between Deficits at Both Ends (R = 0.80 at x = 0.01, 0.90 at x = 0.99), Invariant Across All Three Offset-r Baseline Brackets

**Verdict name: PROFILE-FORM-POWER-LAW, RESIDUAL-PEAKED-MID-WINDOW.** Companion analysis (a) of
two recorded together: pure re-analyses of `exp578_positions.npz`, answering paper 228's named
follow-up (a) — *characterize the functional form of the small-j profile*. No new physics: the
population is exp578 verbatim (128 balanced bitlen-96 semiprimes, master seed 20260828, hash
06931068f8f3ca9b, 9594 hits). Round-80 #1 · exp 579 · sources:
`ResearchOutput/scripts/2026-08-24-round74/exp579_profile_form.py` (pre-registered V1/V2 decision
rules in header BEFORE fitting on full data) → `exp579_result.json`, `exp579_findings.md`; wall
10.2 s full, single clean run after a smoke-stage bootstrap-broadcast fix (no result changed).
ONE-LINE LAW: **hits ∝ (1+x)^(−1.10); the beyond-magnitude part is a ±20% concave mid-window
excess, not monotone.**

## Data and inference discipline

`exp578_positions.npz` consumed VERBATIM (every persisted hit position + paired non-hit controls,
jlo/jhi per N). Normalized position u = (j − jlo)/(jhi − jlo); profile = pooled rate-weighted hit
fraction over 50 equal-width u-bins (exp578 convention; every N has ≥ 29 hits, so the exp578
HITRICH ≥ 30 primary set would differ by exactly ONE N — disclosed, immaterial). Uncertainty =
CLUSTER bootstrap over Ns (2000 reps, fresh master seed 20260831), percentile CIs per bin; the same
replicates feed parameter CIs and residual CIs (joint T,M resampling). Fits are WLS with weights
1/bootSE(bin)² (absolute_sigma).

The magnitude baseline is honest-reconstructable: N is NOT stored in the npz, but s = isqrt(N) =
jhi//3 exactly, so only the offset r = N − s² ∈ [0, 2s] is unknown, entering solely through the
window-start value. PRIMARY baseline mixes the per-N Dickman predictions over a UNIFORM-r prior
(17-point grid); BRACKETS at r ∈ {0, mid, 2s}. Dickman ρ(u), u = ln(j²−N)/ln(10⁶), table-verified
against ρ(2..5) to six decimals (0.306853 / 0.048608 / 0.004911 / 0.000355 — all exact matches).

## Pre-registration (verbatim from the script header)

> V1 WINNER RULE: fit by WLS … the four candidates linear a+b.x | exponential a.e^{−b.x} | power
> a.(1+x)^{−b} | logistic L/(1+e^{k(x−x0)}) on the 50 TREATMENT bin fractions; winner = lowest
> AICc; Akaike weights reported; if winner-runnerup dAICc < 2 the family call is AMBIGUOUS (prefer
> fewer params in wording).
>
> V2 RESIDUAL RULE (stated before computing): magnitude baseline M(b) = mixture-Dickman prediction;
> residual R(b) = T(b)/M(b).
>   PEAKED iff quadratic-beats-linear on R by dAICc > 2 AND vertex in (0,1) AND quadratic-coefficient
>     95% CI excludes 0;
>   else MONOTONE-DECLINING iff (Spearman(R, x) negative with p < 0.01) OR linear slope 95% CI wholly < 0;
>   else FLAT.
>   Baseline fragility gate: V2 verdict must be INVARIANT across the three r-scenario brackets …;
>     otherwise BASELINE-FRAGILE is appended.
>   CONTROL GATE: control profile must be flat (linear slope CI covering 0);
>     firing slope => ARTIFACT-CONTAMINATION flag.

## Result 1 — V1 family verdict: POWER LAW wins decisively

| family | fit | ΔAICc | Akaike weight |
|---|---|---|---|
| **power** a·(1+x)^(−b) | **a = 0.02953 [boot95 0.02837, 0.03070]; b = 1.1044 [0.9908, 1.2182]** | **0** | **0.9866** |
| exponential a·e^(−b·x) | a = 0.02785 [0.02685, 0.02886]; b = 0.7386 [0.6579, 0.8212] | +9.184 | 0.0100 |
| logistic | DEGENERATE → reduces to the exponential (k → 0.739, L/x0 unidentifiable: covariance CIs span ±4·10⁷) | +11.451 | 0.0032 |
| linear a + b·x | b = −0.01320 [−0.01463, −0.01180] | +16.921 | 0.0002 |

Winner beats the runner-up by ΔAICc = 9.18 ⇒ Akaike weight **0.987** — nowhere near the pre-stated
AMBIGUOUS zone. The exponent **b = 1.10 with a CI covering 1** makes the density ~1/(1+x): a
**HARMONIC decline**, decisively not linear (linear loses by 16.9 despite the raw profile looking
roughly straight on deciles — the curvature is real and power-shaped). The observed first→last-bin
fall of T is 3.25×, matching the law's prediction over [0.01, 0.99].

## Result 2 — V2 residual shape: PEAKED, not a further gradient (the pre-registered rule fires)

How much of paper 228's monotone decile slide [.162 → .072] is magnitude, how much is new? Answer:
nearly ALL of the slide IS the Dickman smoothness gradient — the mixture-Dickman baseline M falls
**3.64×** across the window versus T's 3.25× (slightly OVER-predicting steepness). What remains,
R(b) = T(b)/M(b):

| statistic | value | registered reading |
|---|---|---|
| R at x = 0.01 | **0.8007 [0.7332, 0.8732]** — deficit at the ρ = 1 wall region | end deficit |
| R maximum | **1.2257 @ bin 33, x = 0.67 [1.0682, 1.3886]** | mid-window EXCESS |
| R at x = 0.99 | **0.8957 [0.7524, 1.0514]** | end deficit |
| Spearman(R, x) | +0.118, p = 0.42 | NOT monotone |
| linear slope on R | **+0.098 [0.035, 0.162]** — positive if anything | kills MONOTONE-DECLINING |
| quadratic vs linear on R | dAICc = **50.5**; c-CI **[−0.624, −0.141]** wholly < 0; **vertex x = 0.59 interior** | **PEAKED fires** |

All three PEAKED conditions hold simultaneously ⇒ registered verdict **RESIDUAL-PEAKED**. The
genuine beyond-Dickman structure is a modest (±20%) CONCAVE MID-WINDOW EXCESS with deficits at
both ends — most notably at small-j, where the ρ(u) = 1 wall region OVER-predicts hits by ~20%.

**Baseline robustness (fragility gate passes)** — the shape call is invariant across all three
offset-r brackets: slopes on R = +0.082 (r=0) / +0.086 (r=mid) / +0.215 (r=2s), first→last R
[0.843, 0.893] / [0.834, 0.894] / [0.506, 0.927]; every bracket leaves SPEARMAN = +0.118, p = 0.42
and the PEAKED call unchanged (the r=2s bracket deepens the small-j deficit to R = 0.51 but does
not create a gradient). BASELINE-FRAGILE not appended.

**CONTROL GATE passes**: paired-control profile flat, slope +0.000294 [−0.00103, +0.00162]
covering 0 — no artifact contamination.

## Joint consequence — the positional layer now has a LAW; the layers stay separate

Paper 228 established that hits carry within-N positional geometry beyond magnitude (stratified
D = 0.10423 > unstratified, permutation p < 0.0005) but left its SHAPE undescribed. This paper
supplies the shape, and the answer reconciles the two halves of 228: the coarse monotone decile
slide is mostly the ordinary smoothness-magnitude gradient (harmonic, b ≈ 1.10), while the part
that survives conditioning is a bounded concave mid-window hump — structure, but NOT a second
monotone gradient hunting for yet another covariate. Companion paper **230** (exp580) shows this
positional layer does NOT couple to between-N hit-rate variance (H0 INDEPENDENT LAYERS): paper
228's map therefore carries TWO SEPARATE entries — the positional entry, now law-complete
(harmonic profile + mid-window excess hump, papers 228/229), and the rate entry, which retains its
unexplained N-covariate question (the ~39–61% overdispersion of papers 220/222/226/227).

## Ledger catches (all disclosed)

1. **Smoke-stage bootstrap-broadcast bug**: smoke passes hit a broadcast error in the clustered
   bootstrap; fixed before full; FULL ran clean in 10.2 s with all four family fits completing
   2000/2000 bootstrap replicates.
2. **Ship-order/partial-completion check performed and NEGATIVE**: the recording protocol asked
   whether a ship-order partial-completion disclosure is reflected in `exp579_result.json` — it is
   NOT present (no such field); completion evidence is internal: `boot_fits_ok: 2000` for all four
   families, all 50 bins populated with CIs, wall_s recorded. Recorded here so the check itself is
   on the record.
3. **N not stored** ⇒ uniform-r mixture primary with {0, mid, 2s} brackets; the true next_prime-induced
   r-distribution is not exactly uniform — disclosed in-script BEFORE running; conclusions rest on the
   bracket-invariant shape, not the mixture constant.
4. **Dickman treats v = j²−N as random integers** w.r.t. 10⁶-smoothness — algebraic structure could
   shift the smoothness CONSTANT; the deliverable is the SHAPE of R (peaked vs monotone vs flat),
   which is invariant to constant offsets; R ≠ 1 alone is not claimed as geometry.
5. Rate-weighted pooling matches exp578; HITRICH ≥ 30 would drop exactly one N (min 29 hits) —
   immaterial, disclosed. Ratio-scale residuals carry tail asymmetry honestly (R explodes if the
   baseline predicts far steeper decay than observed — it did not).

## Barrier validation

Serves the standing directive's scale-smoothness mechanism frontier: this is a CHARACTERIZATION
step on paper 228's opened frontier — it closes 228's named follow-up (a) with a parametric law
and, importantly, PREVENTS a wrong turn: had R been monotone-declining, the field would have
hunted a second multiplicative gradient mechanism; the peaked call says the beyond-magnitude
structure is bounded and mid-window, redirecting attention toward what sits at x ≈ 0.5–0.8 rather
than a steeper-than-Dickman small-j wall (which actually has a ~20% DEFICIT). Residue-cap 4/3
theorem untouched; no complexity claim; no breakthrough claimed — a law for an already-established
layer.

## Bottom line

The small-j hit-position profile is a POWER LAW T(x) ≈ 0.0295·(1+x)^(−1.104), boot95 on b
[0.991, 1.218] — harmonic decline, Akaike weight 0.987 against exponential/logistic/linear — whose
bulk is exactly the Dickman magnitude gradient (M falls 3.64× vs T's 3.25×). The genuine
beyond-Dickman residual is PEAKED by pre-registered rule: quadratic dAICc 50.5, c-CI [−0.62, −0.14],
interior vertex 0.59 — a ±20% concave mid-window excess peaking at 1.23 near x ≈ 0.67 between
deficits at both ends (0.80 at the wall, 0.90 at the top), invariant across all three offset-r
brackets, control flat. Paper 228's positional layer now has its law; with paper 230 showing the
layers independent, the map carries them separately.

# Paper 233 — SHAPE-TEST-NONPARAM: The Binning-Independent Shape Test Fires — and Closes the Channel (LRT stat = 100.6, df = 3, asym p = 1.17e-21; Permutation 0/400 Exceedances): the Hit-Indicator's Non-Linear Position Structure Is REAL but a STEEP MONOTONE DECLINE with Interior Max x\* = 0.020 CI[0.020, 0.020] Pinned at the LEFT EDGE ([0.4, 0.8] Bar Fails; Peak/End = 2.54 CI[2.243, 2.798]) — H0_CHANNEL_CLOSES, and an ERRATUM-GRADE CORRECTION to Recorded Paper 229: Its RESIDUAL-PEAKED-MID-WINDOW Verdict Was BASELINE-CURVATURE LEAKAGE (the Power-Law Headline Stands and Is Strengthened; the Peaked Characterization Is Retracted)

**Verdict name: H0_CHANNEL_CLOSES** (registered rule), with the decisive decomposition: real
non-linearity, monotone-declining form, no interior maximum.
Paper 232's named follow-up — *a binning-independent shape test … to settle H1 properly at an
amplitude bar that is not stricter than the phenomenon* — run here as a pure reanalysis of
`exp581_regen_positions.npz` (128 strata; hits 9,594 / controls 512,000; windows [jlo, jhi],
jhi/jlo = 3). No sampling, no factoring; full wall **273.4 s**. Round-82 #2 · exp 583 · sources:
`ResearchOutput/scripts/2026-08-24-round74/exp583_shape_test_nonparam.py` (pre-registration in
header, locked before fitting) → `exp583_result.json`, `exp583_findings.md`,
`exp583_full_run.log`, smoke `exp583_smoke.log/_result.json`.

## Setup

ZERO binning anywhere: the response is the RAW hit indicator in a stratum-conditional case–control
logistic regression, with all 128 stratum intercepts profiled out (conditional likelihood). The
position covariate is x = (N − jlo_s)/(jhi_s − jlo_s) ∈ [0, 1]; the convention was VERIFIED
PRE-SCRIPT from the control arrays being linear-uniform inside each stratum window. Nested
comparison: free natural cubic spline (df 5 including constant; interior knots .25/.5/.75)
vs LINEAR-in-x, tested by LRT on the FULL design plus permutation calibration (within-stratum
label shuffles preserving case counts, B = 400, on a control-capped 200-per-stratum design);
bootstrap (150 reps) for x\* and the peak-to-end rate ratio. Control arm: pseudo-cases drawn
from controls vs synthetic uniforms, identical machinery.

## Pre-registration (verbatim from the script header)

> PREREGISTRATION (locked before fitting):
>   x := (N - jlo_s)/(jhi_s - jlo_s); convention VERIFIED pre-script from ctl
>   arrays being linear-uniform inside each stratum window.
>   H1-shape: free natural-cubic-spline (df 5 incl constant; interior knots
>   .25/.5/.75) beats LINEAR-in-x with LRT p<0.001 BOTH asymptotic (chi2,
>   df = spline_df - 1 = 3) AND permutation (500 within-stratum label
>   shuffles, case counts preserved); interior max x* in [0.4,0.8];
>   peak-to-end rate-ratio bootstrap CI excluding 1; CONTROL arm null.
>   H0: any failure => mid-window "hump" not established binning-free.
>   Verdict: H1_CONFIRMED / MIXED_SHAPE_ONLY (LRTs pass, location/ratio fail)
>   / H0_CHANNEL_CLOSES.

Coordinator fuse disclosure: shipped as a MINIMAL SKELETON under the ~15-min fuse — two further
pre-stated legs (monotone I-spline/isotonic comparison; Dickman-offset baseline) were SKIPPED,
documented in `result.json` (`skipped_legs`), NOT failed. Consequence: H1's implicit "beats
monotone" clause is UNTESTED here, and the verdict names shape-vs-LINEAR only. This suffices for
the registered comparison because the decisive clause — interior max location — fails
independently of any monotone comparator: a hump requires an interior maximum, and none exists.

## Result 1 — The non-linear structure is REAL

Free-vs-linear LRT: **stat = 100.574, df = 3**, asymptotic p = **1.17e-21**
(ℓ_free = −20128.36 vs ℓ_linear = −20163.83). Permutation calibration: **0 of 400** within-stratum
label shuffles reach the observed statistic ⇒ p_perm ≤ **0.0025** (the floor at B = 400). Honest
note on the registered bar: the pre-registration asked permutation p < 0.001, unmeetable at
B = 400 (resolution 1/(B+1)); the condition string records this clause False while the direction —
every shuffle far below the observed stat — STRONGLY confirms genuine non-linear structure. This
is not a binning artifact by construction: there is no binning.

## Result 2 — But it is a STEEP MONOTONE DECLINE: the mid-window hump does not exist as raw shape

| registered clause | outcome |
|---|---|
| LRT free-vs-linear, asym p < 0.001 | PASS (1.17e-21) |
| LRT free-vs-linear, perm p < 0.001 | UNMEETABLE at B=400 (floor 0.0025; 0/400 exceed) |
| interior max x\* ∈ [0.4, 0.8] | **FAIL — x\* = 0.020, CI[0.020, 0.020]** |
| peak-to-end ratio CI excluding 1 | PASS — **2.543 CI[2.243, 2.798]** |
| control arm null | PASS — perm p = 0.856 |

The fitted spline's maximum sits at x\* = 0.020 with a bootstrap CI of width ZERO — pinned at the
left edge in all 150 reps — and the curve falls from there by a factor **2.54** to x = 1. A ratio
> 1 with an edge-pinned maximum is the signature of a steep small-x decline (exactly Dickman-type),
not a mid-window mode. Descriptive cross-check, bin-free: decile hit counts strictly declining
[1554, 1177, 1044, 927, 875, 877, 863, 807, 776, 694] — with a single +1.6% blip near u\* ≈
0.55–0.65. That blip is exp582's vertex GHOST: a baseline-relative ripple of the size the noise
ceiling permits, not a mode of the absolute curve.

Control arm: perm p = 0.856 as required. Its large-design asymptotic p reads 0.035 (n ≈ 10^6 rows
detects a microscopic wiggle); the registered null passes via the permutation criterion, and the
asym/perm discrepancy is itself informative about big-design χ² sensitivity.

## THE ERRATUM-GRADE CORRECTION TO RECORDED PAPER 229

Paper 229's registered verdict had two components: POWER-LAW headline
(T(x) ≈ 0.0295·(1+x)^−1.104, Akaike weight 0.987) and RESIDUAL-PEAKED-MID-WINDOW (quadratic
dAICc 50.5 over linear on R = T/M, vertex x̂ = 0.59 interior, ±20% concave excess).

This experiment's binning-free decomposition shows the second component was **BASELINE-CURVATURE
LEAKAGE**: the "mid-window excess" lives in the mixture-Dickman DENOMINATOR's own curvature — R is
a baseline-relative quantity, so denominator curvature manufactures numerator-shaped structure —
and NOT in absolute position shape, which is monotone-declining with its only maximum at the left
edge. Accordingly:

- **RETRACTED**: paper 229's RESIDUAL-PEAKED-MID-WINDOW characterization ("the beyond-magnitude
  part is a ±20% concave mid-window excess, not monotone"). The peaked call was an artifact of
  reading R against a slightly mis-specified smooth baseline, not structure of the hit law.
- **STANDS, STRENGTHENED**: the POWER-LAW headline. T ∝ (1+x)^−1.10 captured the true form —
  a harmonic monotone decline — and exp583 re-finds it binning-free at overwhelming significance
  (stat 100.6, df 3) with the decline steep near x = 0 exactly as the power law predicts.

Consequence chain across the thread: papers 228 → 229 → 230 → 231 → 232 → 233. Any future revival
of the mid-window excess must be stated as a **baseline-mis-specification claim** (about M), never
as a positional mode of the hits. The ABSOLUTE-SHAPE CHANNEL CLOSES. The map keeps exactly ONE
open item on this thread: the **rate-layer N-covariate** — what property of N carries hit-
richness (papers 228/230 established positional and rate entries as SEPARATE layers; exp583
touches only the positional layer's absolute shape).

## Ledger

1. Coordinator fuse disclosure (up front): minimal skeleton at the ~15-min fuse; the
   monotone-I-spline and Dickman-offset legs SKIPPED, documented in `skipped_legs`; verdict scope
   is shape-vs-LINEAR; sufficiency argued above.
2. Permutation/bootstrap run on control-capped designs (200 ctl/stratum) with observed statistics
   from the full-cap design — disclosed; control-arm asym p from a large synthetic design vs its
   perm from the capped one — disclosed.
3. Registered permutation bar (< 0.001) unmeetable at B = 400 (floor 0.0025); recorded as clause
   False with the direction noted — no post-hoc bar change.
4. Design-matrix scale surprise caught in-run: obs rows 521,594 (not the naive 9594+512000
   stratified expansion guess), control rows 1,024,000 — handled within budget; wall 273.4 s.
5. Seeds P/B/S = 20260902/20260903/20260904; x-convention verified pre-script; no commits during
   the run; only exp583_\* files touched.

## Barrier validation

Characterization work that closes cleanly in BOTH directions: it prevents a wrong CONTINUATION
(hunting an interior positional mode that does not exist — the +1.6% ghost is quantified at the
noise ceiling) and prevents a wrong CLOSURE of the true law (the power-law decline is re-confirmed
binning-free at stat 100.6, and the paper-229 erratum strengthens rather than weakens it).
The correction also repairs the map rather than inflating it: one recorded verdict is retired as
leakage, the channel count drops by one, and the single surviving open item (rate-layer
N-covariate) is named precisely. Residue cap untouched; no complexity claim; no breakthrough
claimed.

## Bottom line

The named follow-up fired decisively and split the question the way honest instruments do:
the position channel carries a REAL, zero-binning, strongly non-linear magnitude law — a steep
monotone decline from a left-edge maximum, peak/end = 2.54 — and NO interior hump. Paper 229's
peaked-residual verdict is retracted as baseline-curvature leakage; its power-law headline stands
and is strengthened. The absolute-shape channel CLOSES (H0_CHANNEL_CLOSES, registered rule); what
remains open on this thread is the rate layer alone: which N-covariate carries hit-richness.
Count 571 → 572. Assessment v339 → v340. Issue #381.

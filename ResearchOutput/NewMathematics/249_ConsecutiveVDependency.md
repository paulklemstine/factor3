# Paper 249 — CONSECUTIVE-V-DEPENDENCY: **H0_PURE_DENSITY** — Mid-Window Hit Events Are INDEPENDENT Given Position (Lag Profile Lags 1–20 Flat and Slightly Negative: ρ ∈ [−0.020, −0.002] Against the 0.05 Bar; All MC-vs-Density-Curve p ∈ [0.128, 0.969]; Runs Test Null Both Readings, Z = +0.85 Textbook / +0.89 Density-Curve-Calibrated Against the 3.29 Bar) — Power CONFIRMED (Injected Lag-1 Dependence Detected at ρ_det = 0.337, Argmax Exactly Lag 1) — Consequence: the u\* ≈ 0.65 Excess Is PURE DENSITY / Rate Heterogeneity, With NO Sequence Structure — the Hit-Position Thread (Papers 228–230 → 231 → 238/240 → 241–242 → 248) CLOSES COMPLETELY

**Verdict name: H0_PURE_DENSITY** — the pre-registered primary arm (position-conditioned,
quadratic-detrended lag autocorrelation + Monte-Carlo-calibrated runs test against the
pooled empirical rate curve) fired ZERO of its 20 lags and neither runs reading, so hit
events in the mid-window are independent GIVEN POSITION: the u\* ≈ 0.65 excess is fully
carried by the smooth positional density curve itself (rate heterogeneity only), with no
sequential/Markov structure of any sign. This is the TERMINAL CHARACTERIZATION of the
hit-position thread: whatever gain remains must come from modeling the density curve,
never from sequence structure.

Round-91 #2 · exp 599 · executes exp 598's pre-registered routing (paper 248 §4).
Sources: `ResearchOutput/scripts/2026-08-24-round74/exp599_{consecutive_v.py,
smoke.log, run_full.log, result.json}` + `exp599_findings.md` · wall **31.4 s** full /
1.3 s smoke. Data: `exp581_regen_positions.npz` ONLY (sha256 `0b1afa50…36a38`,
recorded in stats) — `hit_i` hit positions per batch, `ctl_i` = 4,000 control positions
per batch, `jlo`/`jhi` window bounds, 128 batches, **9,594 hits**, no N stored ⇒ a
purely positional point-process analysis; fraction of hits/controls inside their window
= 1.000 both. Seed lineage 599_20260828 (seed 599_20260828; boot 2000 reps cluster-
over-Ns; MC 2000 reps).

## 1. Pre-registration verbatim (written BEFORE any analysis was run)

From the `exp599_consecutive_v.py` header:

> QUESTION: after j-arithmetic carriers were eliminated, do mid-window
> hits show POLYNOMIAL-SEQUENCE DEPENDENCY -- correlation between hit
> events at NEIGHBORING positions in the v/j sequence?
>
> H1 (dependency real): hit-indicator autocorrelation at lags 1-20
>   within the mid-window u in [0.55,0.75] shows |rho|>0.05 at some lag
>   with bootstrap CI excluding 0 (cluster-resampled over the 128 N
>   batches), OR runs-test rejects independence at p<0.001
>   => consecutive-v dependency exists; report lag profile.
> H0: all lags null => hit events are independent GIVEN POSITION
>   => the excess is a pure density phenomenon (rate heterogeneity
>   only); positional thread closes as "no sequence-level structure".
>
> AMENDMENT 0 (registered now, before data seen; motivation = the H0
> wording itself): because H0 is independence CONDITIONAL ON POSITION,
> and the mid-window contains the exp582 hump (rate rises then falls
> inside [0.55,0.75]), a global-mean-centered autocorrelation is
> MECHANICALLY biased positive under H0 by intra-segment rate
> curvature. Two variants therefore run side by side, registered NOW:
>   PRIMARY (decisive for H0-as-stated): position-conditioned --
>     per-batch quadratic detrend of the indicator inside the segment,
>     autocorrelation of residuals; runs test calibrated by Monte Carlo
>     against the pooled empirical rate curve p_hat(u) (the concrete
>     "density-only" null), |Z_mc|>3.29 <=> p<0.001.
>   SECONDARY (literal task reading): global-mean-centered rho +
>     textbook Wald-Wolfowitz pooled runs Z, reported but interpreted
>     through control C2 below.
> CONTROLS (identical treatment, all pre-committed expectations):
>   C1 ctl batches (random positions) -> null on BOTH variants.
>   C2 synthetic smooth-hump (iid Bernoulli at pooled rate curve p_hat)
>      -> SECONDARY goes positive, PRIMARY null: quantifies the
>      curvature confound. If C2-secondary is NOT positive, the
>      confound argument is void and the literal reading stands.
>   C3 injected lag-1 dependence at matched rate -> PRIMARY must
>      detect (power check; if C3 null, a null verdict is uninterpretable).
> Bin grid: nb=1000 bins/window (segment=200 bins); robustness at
> nb in {500,2000}. Lags 1-20. Bootstrap 2000 reps cluster-over-Ns,
> seed 20260828-lineage (599). Regen/hash: sha256 of npz recorded;
> seed-20260828 ctl regeneration attempted (two canonical recipes),
> match/mismatch reported honestly.
> Verdict rule: H1 iff PRIMARY fires (either arm); SECONDARY alone
> cannot fire H1 unless C2-secondary fails to fire (see above).

*(Recorder note: verbatim transcription complete; authoritative source
`exp599_consecutive_v.py` header, lines 1–52.)*

## 2. Results — the lag profile and the runs test

**PRIMARY (position-conditioned, quadratic-detrended within the segment, nb = 1000,
segment = 200 bins):** ρ_det(lag) over lags 1–20 lies in **[−0.0199, −0.0023]** —
flat and slightly negative, max |ρ| = 0.020 against the registered |ρ| > 0.05 bar.
No refractory dip and no excitation bump on either flank of zero: the profile simply
does not move. Per-lag Monte-Carlo tests against the concrete density-only null
(i.i.d. Bernoulli at the pooled empirical rate curve p̂(u), 2000 reps) give
**p ∈ [0.128, 0.969]** — minimum 0.128 at lag 18, nothing near significance at any
lag. **ZERO lags fire.**

Cluster-over-Ns bootstrap (2000 reps): CI half-widths ≤ 0.013. *(Recorder
correction — see §5.2:* findings.md states "every CI straddles 0", but result.json
shows **12/20 detrended CIs exclude zero on the NEGATIVE side**, all with upper end
≤ 0.0083 — a uniform sub-bar negative offset, not a dependency signal; the H1 rule
requires |ρ| > 0.05 AND CI exclusion JOINTLY, so the verdict is unaffected either
way.) *The SECONDARY literal reading (global-mean-centered) is even more null:
ρ_raw ∈ [−0.0103, +0.0046].*

**RUNS TEST, both readings:** textbook pooled Wald–Wolfowitz on the pooled
hit/control indicator stream gives **Z = +0.850 (p ≈ 0.40)**; recalibrating against
the MC density-only null (empirical μ = −0.0275, σ = 0.9813) gives
**Z_mc = +0.894 (p ≈ 0.37)** — nowhere near the registered |Z| > 3.2905 (p < 0.001)
bar. Control batches: textbook Z = −0.454. Both arms null; the two readings AGREE,
which (per the registered C2 logic) means the verdict does not depend on Amendment 0
at all.

**Robustness to binning:** nb = 500 → max |ρ_det| = 0.036; nb = 2000 → 0.016 —
no binning artifact creates or hides anything at any resolution; all remain far
under the 0.05 bar.

## 3. Controls — all three pre-committed expectations met

| control | expectation | outcome |
|---|---|---|
| C1 control batches, identical pipeline | null both variants | **met**: max \|ρ_raw\| = 0.009, max \|ρ_det\| = 0.020 |
| C2 synthetic smooth-hump (iid Bernoulli at pooled p̂(u)) | SECONDARY positive, PRIMARY null | **secondary ALSO null** (max \|ρ_raw\| = 0.014 @ lag 17, pooled_Z = +0.60): the curvature confound is quantitatively IMMATERIAL at this resolution — conditioned and literal readings agree, verdict not amendment-dependent |
| C3 injected lag-1 dependence at matched rate | PRIMARY must detect | **met massively**: ρ_det(lag 1) = **0.337**, argmax exactly lag 1, pooled_Z = −57.4 — power_ok = true |

C3 is the load-bearing one for interpreting a null: the pipeline detects lag-1
dependence at ρ ≈ 0.34 through the identical clustering/detrending machinery, so the
observed all-lags null on real data means "no dependency," not "test blind." A useful
side-reading of C2: even a perfect smooth-hump realization drawn iid from the exact
pooled rate curve produces max |ρ| ≈ 0.014–0.022 at nb = 1000 — the same order as
everything observed here — confirming that the entire measured profile sits at the
noise floor of the design.

## 4. Consequence — THREAD CLOSURE

Given position, a mid-window hit carries NO information about neighboring positions.
Combined with the thread's prior links this yields the complete terminal picture of
the u\* ≈ 0.65 excess:

- the excess is REAL on its home seed (exp579/581 hump; papers 239/241),
- divisibility is a RATE dial, not a position dial (exp 588c/#390, paper 242),
- no j-arithmetic class carries it (exp 598, paper 248 — extreme-value noise kept
  as the canonical demonstration), and NOW
- there is no SEQUENCE structure either: no lag correlation (either reading), no
  runs deviation, no refractory/excitation — the excess is **pure density/rate
  heterogeneity** along the scan axis.

The hit-position thread opened at papers 228 (HitPositionStructure), 229
(ProfileForm), 230 (PositionalRateLink), ran through 231 (hump mechanism), 238/240
(edge kernel, spike origin), 241 (u\*-mechanism), 242 (divisibility mixture baseline),
and 248 (j-feature sweep) — and closes HERE with its terminal characterization:
**density phenomenon, no carrier among arithmetic classes of j, no sequential
structure.** Operational law for all future work: gains must come from modeling the
positional DENSITY CURVE itself (the paper-238 kernel + bulk shape), never from
Markov/neighborhood structure of the hit stream.

Honest scope: this characterization holds ON THE DATA WHERE THE EXCESS MANIFESTS
(seed-20260828 lineage). Exp 592/#391 established that the u\* ≈ 0.65 amplitude did
not replicate on fresh seed 20260902 and left the single-hypothesis ≥3-pooled-seeds
test open; if that test ever re-establishes an excess elsewhere, the
density-vs-sequence question reopens THERE — though the present machinery (detrended
lag profile + density-curve-calibrated runs + injected-signal power arm) transfers
unchanged.

## 5. Ledger catches

1. **Control-provenance limitation, disclosed**: seed-20260828 control regeneration
   was attempted with two canonical recipes (`rng.default_rng(20260828)` and
   `np.random.seed(20260828)`) — **both MISMATCH ctl_0**. The recipe is not
   recoverable from allowed reads, so provenance rests on the recorded npz sha256
   `0b1afa50…36a38` (the same artifact whose seed-lineage was hash-proven in exp
   581); no N values are stored, so the analysis is purely positional throughout.
2. **RECORD-TIME CORRECTION on exp599_findings.md**: its claim "every CI straddles
   0" OVERSTATES. result.json shows 12/20 detrended-lag CIs excluding zero on the
   negative side (upper ends ≤ 0.0083), with the raw CIs 19/20 straddling (only lag
   8 marginal at −0.00019). There is a uniform ~−0.01 detrended offset on hits
   (controls mirror it at ~+0.01) — a shared-magnitude artifact of opposite sign,
   not structure. Verdict unaffected: the H1 rule requires |ρ| > 0.05 AND CI
   exclusion JOINTLY (max |ρ| anywhere = 0.020), the MC p-values never drop below
   0.128, and the runs arm is independently null.
3. **Amendment-0 resolution is stronger than registered**: the registration allowed
   for the possibility that the literal reading would fire spuriously under hump
   curvature (C2-secondary positive). It did not — the curvature confound is
   immaterial at this binning/resolution, so the conditioned and literal variants
   AGREE and no amendment arbitration was needed.
4. **MC null approximation disclosed**: the density-only MC null approximates all
   batches sharing the pooled rate curve; per-batch rate heterogeneity is folded
   into the cluster bootstrap instead (registered up front).

## 6. Barrier validation

No barrier interaction: a terminal characterization INSIDE the mapped positional
stratum, closing the layer the barrier map calls out as fully measured (position
5.19× = balance bet + truncation, external interval hints = coverage × width).
Consistent with the asymptotic directive: open frontiers unchanged — u ≥ 6–14
scale-smoothness deviations, factor-local methods outside scan-order framing, MA-1
effectivity, residue cap 4/3 theorem; quantum frontier closed; paper 242
single-seed-unconfirmed (#391) and the .2346 flag traveling. Named next probe: none
on this thread — the positional layer is closed; remaining positional-side work
belongs to the density-curve model (paper 238 lineage), and the open frontiers list
above.

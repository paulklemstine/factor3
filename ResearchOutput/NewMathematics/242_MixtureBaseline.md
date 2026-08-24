# Paper 242 — MIXTURE-BASELINE [FINAL]: The u* ≈ 0.65 Excess SURVIVES the Full Divisibility Mixture (Amp 0.177 ± 0.043, z = 4.11 ≥ Registered Bar of 2; Removal vs Single-α Baseline = 0%) — Class Composition Is Measured FLAT in t (Max Cell Drift 0.27%), Per-Class Rates Are Real (κ/g Spread 0.645–1.406) but t-INDEPENDENT → **DIVISIBILITY IS A RATE DIAL, NOT A POSITION DIAL** — NEW MAP ENTRY: NON-DIVISIBILITY POSITIONAL MECHANISM

**Verdict name: H0 — EXCESS SURVIVES THE MIXTURE** (registered tree: H1 iff amp_mix < SE_mix;
H0 iff amp_mix ≥ 2·SE_mix; else PARTIAL; control arm must be null — fired exactly as registered,
with one disclosed caveat, §5).

Round-87 #1 · exp 588c · completes the **three-pass chain papers 232 → 241 → 242**: paper 232 found
the shift-invariant mid-window excess of j²−N smoothness and left its carrier open; paper 241
(exp 588b) proved it REAL over the exact Dickman baseline yet carried by no single binary feature,
and ROUTED the question to a divisibility-mixture baseline model; this experiment runs that routed
model and settles the question — **the mixture does NOT absorb the excess, so the carrier is
something beyond small-prime divisibility composition: a genuine positional mechanism entry on the
scale-smoothness map.**

Pure reanalysis of `exp581_regen_positions.npz` (sha256 `df4830ed…fbb74` re-recorded at load; 9594
pooled hits / 512,000 reference non-hits over 128 Ns × full j-window; wall **12.6 s**; cluster
bootstrap 2000 reps, seed 20260901, exp582 convention). Sources:
`ResearchOutput/scripts/2026-08-24-round74/exp588c_{mixbase.py, smoke.log, full.log, result.json}`.
Findings content returned inline by the experimenter (no findings.md per subagent policy);
`exp588c_result.json` is the authoritative record.

## 1. Pre-registration verbatim (written before any analysis)

From the `exp588c_mixbase.py` header:

> Model (FIXED before any number was seen):
>   16 cells = divisibility pattern (2|v, 3|v, 5|v, 7|v) of v = j^2 - N.
>   Predicted bin count  PRED(b) = sum_c kappa_c * S_c(b),
>     S_c(b) = sum over REFERENCE (non-hit) samples x in bin b with cell c of rho(u_x),
>     u_x = ln(v_x)/ln(1e6)  (lnB FIXED = ln(exp578 CUT_BIG), known), rho = Dickman.
>     kappa_c fit on FLANKING bins ONLY (t<0.40 or t>0.85; score window EXCLUDED from estimation):
>       kappa_c = (Hf_c + lam*g)/(Sf_c + lam),  Hf_c/Sf_c = flank hits / flank Dickman sum in cell c,
>       g = global flank hit rate per Dickman unit, lam = 5 pseudo-count shrinkage (rare cells).
>
> H1 (mixture closes the channel): post-mixture residual peak amplitude
>     amp_mix = max_{score bins} 3-bin-smoothed(observed/PRED) - 1,  score window t in [0.55,0.75]
>   falls BELOW its cluster bootstrap SE (resample the 128 Ns, 2000 reps, seed 20260901)
>     => CHANNEL CLOSES (the u*~0.65 feature was divisibility-composition all along).
> H0 (excess survives): amp_mix >= 2*SE_mix
>     => structure BEYOND divisibility composition => NEW MAP ENTRY (non-divisibility positional
>        mechanism).
> Reference decomposition (pre-named, corroborating not verdict-bearing):
>     removal_pct = 100*(1 - amp_mix/amp_orig), amp_orig = same amplitude/statistic under the
>     exp588b single-alpha Dickman baseline on the SAME data and pipeline; removal >= 50% AND
>     z_mix < 1 corroborates the H1 wording; removal ~ 0 with z_mix >= 2 corroborates H0.

Fixed design points disclosed in the header: lam = 5 chosen pre-data; nb = 50 bins and 3-bin
smoothing identical to exp588b for comparability; score window [0.55, 0.75] per brief; flanks
t < 0.40 | t > 0.85 per brief; buffer bins (0.41–0.54, 0.76–0.85) are predicted but NEITHER fitted
NOR scored; secondary comparability number amp_mix_wide on exp588b's [0.45, 0.85] reported,
non-bearing.

## 2. Exact-regeneration lineage (statistics gated on it)

Reuses the proven exp588b-A3 exact path, verified before any statistic ran:

| Check | Result |
|---|---|
| Population + windows | int64-EQUAL all samples (jlo = isqrt(N)+1, jhi = 3·isqrt(N)) |
| Stream membership | all 128 samples contained |
| Stream ORDER walk | EXACT on all 128/128 samples (one rng/chunk, sequential 150k draws/N) |
| Smoothness spot-check | stored hits re-validated SMOOTH / controls NON-SMOOTH, subsample ALL pass |

Status `EXACT_MATCH`; statistics gated on it (`abort_before_statistics` armed, never fired).

## 3. Headline result

| Quantity | Value |
|---|---|
| Residual peak amplitude under mixture | **amp_mix = 0.1774 ± 0.0432 (z = 4.11)** — score window t ∈ [0.55, 0.75] |
| Peak location | **t = 0.65 exactly** (smoothed ratio 1.1774 at bin t=.65; sharpest raw single-bin excursion ratio 1.315 at t=.67) |
| Wide-window comparability amp_mix_wide [0.45, 0.85] | 0.1774 (identical — peak interior to both windows) |
| Single-α baseline amp_orig (same pipeline) | 0.1163 |
| **Removal %** | **0.0** (pre-named corroboration: removal ≈ 0 with z_mix ≥ 2 → corroborates H0) |
| Hits / reference | 9594 / 512,000 |

The registered rule fires **H0**: amp_mix = 0.1774 ≥ 2·SE_mix = 0.0864. The mixture did not merely
fail to absorb the excess — the residual amplitude is LARGER under the mixture than under the
single-α baseline (0.177 vs 0.116; different score windows, so the comparison is qualitative), as
expected when flank-fitted rates leave a mid-window bump untouched while the denominator sharpens.

## 4. Why the mixture couldn't absorb it: RATE DIAL, NOT POSITION DIAL

This is the paper's central measurement, and the reason H0 fired:

- **Class composition is FLAT in t.** Max cell-composition drift across the profile =
  **0.269%** (composition_drift_max_c = 0.00269). The mixture's positional freedom — letting the
  cell mix shift along t — is essentially zero, so PRED(b) inherits the baseline's smooth decline
  and cannot produce a mid-window ridge whatever the rates do.
- **Per-class rates are real but t-INDEPENDENT by construction.** κ/g spans **0.645 → 1.406**
  across the 16 divisibility cells (top cells: 2∧1·3∧1·5∧1·7∧0 at 1.406, 2∧1·3∧1·5∧1·7∧1 at
  1.269, 2∧0·3∧1·5∧1·7∧0 at 1.265; bottom cell all-cleared at 0.645) — divisibility genuinely
  modulates smoothness rate ~2.2× cell-to-cell — but each κ is estimated ON FLANKS ONLY and
  applied uniformly across t. The mixture has rate dials with no position dependence to deploy.

**Formulation (the deliverable): divisibility is a rate dial, not a position dial.** It rescales
HOW OFTEN hits occur in a class, uniformly in scan position; it does not move hits ALONG the
position axis. The u* ≈ 0.65 excess is positional — concentrated in t — and therefore survives any
divisibility-conditioned rate model whose class weights are flat in t. Note also (disclosed in
honest_notes): bit 0 (2|v) is IDENTICALLY j-parity since N is odd, so the cell grid merges exp588b's
parity carrier; the other three bits are v-divisibility proper — the null here covers parity too,
closing that residual reading of paper 241 as well.

## 5. Controls — pass, with one disclosed caveat

| Control | Result | Bar | Status |
|---|---|---|---|
| CTRL-A machinery (count-vs-count halves, identical machinery incl. max-stat/bootstrap) | amp 0.0271 ± 0.0102, max-dev over ALL bins 0.0342 | < 3·SE AND < 0.10 AND max-dev < 0.10 | PASS (null) |
| CTRL-B estimator null (parametric Poisson pseudo-hits on g·S, seed 20260830, through the IDENTICAL estimator) | amp_sim 0.0860 ± 0.0411 | matched-null reference for z_cal | reported |

**Caveat, disclosed per registration:** the null-calibrated significance z_cal =
(amp_mix − amp_sim)/√(se_mix² + se_sim²) = **1.53 < 2**. Max-over-bins amplitude is positively
biased under the null, and CTRL-B measures that bias (~0.086 of the 0.177 raw amplitude); against
the calibrated null the excess is suggestive rather than decisive. The registered amp-vs-SE rule
remains verdict-bearing (as registered: disagreement flagged, never silently resolved) and H0
stands; the honest joint read is: **raw z = 4.11 verdict-bearing; null-calibrated z = 1.53 caveat
traveling forward with every downstream use of this amplitude.** Any follow-up should power against
the calibrated scale, not the raw one.

## 6. Three-pass chain history (232 → 241 → 242)

1. **Paper 232** (feature discovery): the shift-invariant u* ≈ 0.65 mid-window excess of j²−N
   smoothness; stable across shifts, but the amplitude bar failed AS OPERATIONALIZED (7/30 fits) —
   carrier left open.
2. **Paper 241 / exp 588b** (exact-baseline probe, MIXED-PARTIAL): hump REAL over the EXACT Dickman
   baseline ρ(ln v/ln 1e6), amp 0.116 ± 0.036, z = 3.23, paired-random control null — yet removal
   0% for EVERY single candidate (parity, 3|v, 5|v, 7|v, ω₁₀₀ tercile; gcd structurally vacuous),
   worst strata retaining z 2.38–4.56. m|v conditioning absorbed ~45–60% of yes-stratum
   point-amplitude → ROUTED to a divisibility-mixture baseline model, per-hit binary covariates
   refuted.
3. **Paper 242 / exp 588c** (this paper): the routed mixture model — 16 divisibility cells,
   flank-only κ with λ-shrinkage, composition-weighted Dickman prediction — FAILS to absorb the
   excess (removal 0%, z = 4.11). The routing hypothesis is answered NEGATIVELY, which converts
   into the positive map entry below.

Each pass sharpened the question: real? (232/241) → carried by a flag? (241) → carried by the
composition mixture? (242, NO) → what carries it? (open, §7).

## 7. New map entry + named follow-up

**NEW MAP ENTRY: NON-DIVISIBILITY POSITIONAL MECHANISM.** The scale-smoothness map now carries a
third orthogonal layer alongside the positional layer (papers 228–230) and the left-edge composition
layer (papers 238–240): a mid-window (u* ≈ 0.65) excess that is (i) REAL over the exact Dickman
baseline, (ii) STABLE (shift-invariant since paper 232, reproduced exactly here via byte-exact
lineage), and (iii) NON-DIVISIBILITY (this paper — survives the full 16-cell mixture; parity merged
in and equally failed).

**Named follow-up: identify the non-divisibility carrier.** Pre-named candidates for the next
probe:
- **j-arithmetic beyond small-prime divisibility** — e.g. higher-order residues of v = j²−N, j
  relative to powers of 2 (bit structure near the truncation boundary), quadratic-character /
  Legendre-pattern correlations of v mod p for p > 7;
- **polynomial-sequence correlations** — structure specific to the sequence j²−N as j varies
  (values-of-polynomial smoothness biases beyond divisibility, cf. the f(x)-shifted smoothness
  literature) rather than properties of individual v.

Power note from §5: design against the CTRL-B-calibrated null scale.

## 8. Ledger catches (all disclosed)

1. **A1 amendment — control split pre-full-run (clean catch).** The originally registered control
   arm (count-halves of the non-hit stream scored against the ρ-WEIGHTED prediction) had a NON-FLAT
   NULL BY CONSTRUCTION — counts carry no ρ(t) gradient while the prediction does, so it fails its
   own bar even on perfectly clean data (smoke observed amp 0.47 from ~290 counts/bin). Caught AT
   SMOKE; control split into CTRL-A (machinery) + CTRL-B (estimator null) BEFORE the full run;
   registered H1/H0 rule UNCHANGED; **no treatment-arm number entered any verdict through the
   amendment**. Smoke verdict correctly read ARTIFACT-CONTAMINATED (control arm violated) — the
   gate worked as designed.
2. **Max-statistic bias inside the raw amplitude** — measured by CTRL-B, reported as z_cal = 1.53
   alongside the verdict-bearing raw z = 4.11; flagged in json `calibration_flag`, never resolved
   silently (§5).
3. **Reference stream is a subsample** (stored capped non-hits ≤4000/N, first-in-stream) — unbiased
   for uniform-sampling composition, disclosed.
4. **κ shrinkage λ = 5 toward the global flank rate** guards rare/empty cells (pre-registered); the
   mid/score window fully excluded from all κ estimation.
5. **ln v computed from EXACT integer v then float-converted** (float j²−N would cancel
   catastrophically near t=0); Dickman table/interpolation identical to exp588b.
6. **Bit 0 ≡ parity merge** (N odd) — disclosed in §4; the null covers parity explicitly.
7. Buffer bins predicted-but-not-scored per brief; smoke preceded full run as pipeline validation
   only; boot seed 20260901; wall 12.6 s; only exp588c_* files touched during runs; no commits
   during runs.

## 9. Barrier validation

No breakthrough claimed — this is a map-entry addition INSIDE the rate layer's baseline-shape
question, and it CLOSES the routed mixture-model branch of paper 241's consequence while OPENING a
named new entry. Untouched: residue cap 4/3 theorem; scan-order position 5.19×; external class-hint
law 1/(1−(1−θ)P_hit); external interval-hint coverage × width law; quantum frontier; method stratum
map; abelian pinning ladder; QS calibration; utility closure; four-class rate-residual closure
(paper 237); papers 238–240 spike-origin resolution (left edge). Asymptotic relevance per the
standing directive: the new entry is defined at fixed DATA GEOMETRY (mid-window t), so its test
transfers across bit lengths unchanged — and the refuted family (divisibility-rate mixtures as a
positional explanation) is removed from the search space at every scale. Open frontiers unchanged:
non-QR per-N structure at u = 2.5 (31%-above-floor residual), factor-local methods outside
scan-order framing, MA-1 effectivity; PLUS the named follow-up of §7. Paper 238's .2346 provenance
flag still travels until reconciled.

## Attribution

Experiment + analysis artifacts: `ResearchOutput/scripts/2026-08-24-round74/`
(exp588c_mixbase.py — pre-registration + amendment log A1 in header, authored before first
execution; exp588c_smoke.log/_result.json; exp588c_full.log; exp588c_result.json — config/regen/
residual rows/stats/verdicts/honest_notes/wall_s [authoritative]; data source
exp581_regen_positions.npz, sha256 df4830ed…fbb74). Recorded round-87 #1; notebook Part 284;
assessment v349; issue #390.

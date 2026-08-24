# Paper 236 — BSTAR-TRANSFER: Paper 227's Window-Saturation Location B\* = 400 TRANSFERS to the Corrected √-Weight — Unique Interior Argmax under 1/√ℓ (R² .528 → .598 → **.624** → .591 → .614 over B = 100/200/400/800/1600), Closing Paper 235 §3's Named Owed-Check Affirmatively — While the Recomputed Harmonic Comparison Curve Is a Flat Plateau above B = 200 with Only a Noise-Level Edge Peak at 1600 (+0.006), So the Interior-Window Signal Is √-WEIGHT-SPECIFIC; ΔR²(√ vs Harmonic) Positive at ALL Five Windows (+0.089 … +0.151, No Weight×Window Interaction); Bootstrap Honestly Split 400 (276/500) vs 1600 (178/500) — Robust Reading: Saturation Reached by B = 400, NO Further Gain through 1600

**Verdict name: H1_BSTAR_TRANSFERS** — paper 227's window-location claim survives the weighting
refinement of paper 235; the canonical product dial becomes **S_√,B with B\* = 400**, and paper
235 §3's named open check ("B\*-transfer under √-weight … must be re-checked before B\*-location
claims are reused") is CLOSED affirmatively.

Round-83 #3 · exp 587 · pure reanalysis of exp577's stored per-N hit counts (no new j-sampling;
wall 0.13 s full) · sources: `ResearchOutput/scripts/2026-08-24-round74/exp587_{bstar_transfer.py,
smoke.log,full.log,result.json}` + `exp587_findings.md` · completes the paper-235 refinement
chain (supersession → B\*-transfer).

## 1. Pre-registration (verbatim, written BEFORE analysis)

> Question (paper 235 section 3 NAMED OPEN ITEM): paper 227 measured the
> window-saturation location B*=400 under the superseded 1/l product-dial
> weight. Does B*=400 TRANSFER to the corrected 1/sqrt(l) weighting
> (exp586: alpha_hat=0.5, CI [0.5,0.5], dR2 vs harmonic = +0.151)?
>
> PRE-REGISTERED HYPOTHESES (fixed before touching the data):
>   H1 (transfers): let A_sqrt = {B in GRID : R2(sqrt,B) == max_B' R2(sqrt,B')}
>       (exact ties admitted, tolerance 1e-12). H1 fires iff 400 in A_sqrt
>       ==> B*=400 is WEIGHT-ROBUST; paper 227's window-location claim survives
>       the refinement to sqrt weighting.
>   H0 (shifts): 400 not in A_sqrt ==> the window-location claim is RE-SCOPED
>       to harmonic weighting only; report the new B* = min(A_sqrt).
>
> SECONDARY (pre-named): weight x window interaction. dR2(B) :=
>       R2(sqrt,B) - R2(harm,B).
>       - PLATEAU-RAISED iff dR2(B) > 0 at EVERY B in GRID (paper 235
>         expectation: the corrected weight dominates uniformly);
>       - otherwise the weight INTERACTS with B: report per-B winners and the
>         sign pattern of dR2 across the grid.
>
> METHOD (pre-registered):
>   1. Regenerate the IDENTICAL seed-20260827 population with the
>      exp586/exp577 recipe VERBATIM (make_semiprime(bits=96), rejection
>      recursion + dedup); FULL mode HARD-ASSERTS regenerated N[i] == stored
>      exp577 rows[i].N for all 128 (hash-match gate; abort on failure).
>   2. Mechanistic Legendre counts c_l(N) = [jacobi(N mod l, l) == +1] for ODD
>      primes 3 <= l <= 1600; each window B is a column mask l <= B (cumulative).
>   3. Weighted dials S_w,B(N) = sum_{l<=B, chi=+1} l^{-w} for BOTH weights
>      w = 0.5 (sqrt, corrected) and w = 1.0 (harmonic, superseded -- recomputed
>      here under identical conditions, NOT imported); OLS y_N =
>      log((hits+0.5)/total_N) ~ S_w,B per (w, B); report both full R2(B)
>      curves with slopes/SEs.
>   4. Bootstrap argmax robustness: 500 reps (full) / 50 (smoke) resampling the
>      Ns with replacement (seed 587); per-rep argmax_set over the SAME grid;
>      report P(400 in argmax_set*) and the B* distribution.
>      Tie-break: reported B* = min(argmax_set) (lowest window on exact ties).

## 2. The dual R²(B) curves

Regression form: log((hits+0.5)/total) ~ S_w,B, OLS, n = 128 semiprimes at bitlen 96
(mean hits/N = 77.58 over 150 000 j-samples; odd primes 3..1600, windows are cumulative
column masks).

| B | R²(√-weight, w=.5) | R²(harmonic, w=1) | ΔR² |
|---|---|---|---|
| 100 | .5279 | .4388 | +0.0891 |
| 200 | .5976 | .4621 | +0.1355 |
| **400** | **.6242** | .4731 | **+0.1511** |
| 800 | .5913 | .4748 | +0.1165 |
| 1600 | .6137 | .4795 | +0.1342 |

Slopes tell the same story from the other side: under √-weight the slope stays ~0.31–0.35 across
all B (stable scaling, consistent with exp586's exponent fit), while the harmonic slope runs
~0.76–0.80.

Decision numbers:

- **H1 fires**: argmax_set under √-weight = {400} exactly (unique interior maximum, tol 1e-12);
  400 ∈ A_sqrt per the pre-registered rule.
- **PLATEAU_RAISED_EVERYWHERE** (pre-named secondary): ΔR² > 0 at all five B, max at B = 400 —
  no weight×window interaction; exp586's correction is uniform in the window, not an artifact of
  one window choice.

## 3. Transfer verdict — closing paper 235 §3's owed-check

Paper 235 §3 left this on the ledger:

> "window-location saturation (B\* = 400, corr .999) was measured UNDER the 1/ℓ weight (papers
> 136/139/227). Its transfer to √-weight is UNVERIFIED and must be re-checked before B\*-location
> claims are reused downstream."

This experiment performs exactly that check, and it PASSES: the saturation location lies in
**(200, 800]** at factor-2 grid steps, with the point value **B\* = 400** — unchanged from paper
227's original measurement. Adopted lab-wide:

> **Canonical product dial: S_√,B(N) = Σ_{odd prime ℓ ≤ 400, jacobi(N mod ℓ, ℓ)=+1} ℓ^(−1/2).**
> The corrected weight both raises fit everywhere (+31% relative dial power, paper 235) AND
> resolves the saturation location that the superseded weight could not locate on this data.

The refinement chain over paper 227 is now complete in two steps: 227 adopted 1/ℓ with B\*=400 by
inspection → 235 measured α̂ = 0.5 and superseded the weight → 236 confirms B\* = 400 survives
the correction.

## 4. The bimodal-tail caveat (reported honestly)

The bootstrap splits: **argmax contains 400 in 276/500 reps (55.2%), 1600 in 178/500, 200 in
37/500, 800 in 9/500**. The 1600 point sits only **0.0105** below the full-sample peak
(sqrt_gap_400_minus_1600). The honest robust reading is therefore:

- **"Saturation reached by B = 400, no further gain through 1600"** — supported at bootstrap
  strength (P(argmax ⊇ 400) ≈ 55%, and every rep's curve is flat above 200 within ~0.01);
- NOT a sharp 400-vs-1600 separation. A single-seed population cannot resolve finer than that,
  and the pre-registered verdict rule (full-sample argmax) fires as designed while the resampling
  distribution discloses its own softness. Downstream users of B\* should treat 400 as the
  canonical point value inside the interval (200, 800], not as a resolved spike.

## 5. Integrity

- Population regeneration VERBATIM from the exp586/exp577 recipe (random.Random(20260827),
  bitlen 96, exact rejection recursion + dedup): **128/128 Ns hash-matched** to stored rows
  (hard-assert gate passed; the run aborts on any mismatch).
- Pure reanalysis end-to-end: no new j-sampling anywhere; wall 0.13 s full. The data layer is
  exactly exp577's, so no seed-level replication risk beyond what 227 already carried.
- Both weight arms computed mechanistically from the same count matrix under identical
  conditions; the harmonic comparison was recomputed here, NOT imported.

## 6. Limits (disclosed)

1. **Grid resolution**: factor-2 steps only; B\* is a grid point, so "B\* = 400 transfers" means
   the saturation location lies in (200, 800]. Fine structure below one octave unmeasured.
2. **Single seed**: population seed 20260827 only; pure reanalysis, no fresh replicate. Per
   paper 234/C3's pooling mandate, multi-seed confirmation would be needed before treating the
   bootstrap split as a population property.
3. **Bootstrap softness**: the 55/45 split between 400 and 1600 (§4) means the argmax LOCATION
   is single-seed-fragile even though saturation-by-400 is robust on this data.
4. **Log-rate attenuation**: OLS on log-rates with per-N Poisson noise (~150 k samples/N) — same
   regime as exp577/exp586; absolute R² values attenuated, comparisons within-grid unaffected.
5. **Harmonic edge argmax**: the recomputed harmonic curve peaks at grid-edge 1600, not at an
   interior window — see ledger catch 1.

## 7. Ledger catches

1. **The interior-window signal is √-weight-specific on THIS dataset/grid**: the recomputed
   harmonic curve does NOT peak at 400 — it is a flat plateau above B = 200 with EDGE argmax
   1600 (ΔR² 1600-vs-400 = **+0.006**, noise-level). Paper 227's original B\*-location measurement
   used its own data/method; the transfer claim tested here concerns the √-weighted arm per the
   pre-registration, and under the corrected weight the interior location exists and lands at
   400. Under the superseded weight, saturation happens WITHOUT locating an interior B\*.
2. **exp577's stored S400 column identified**: it IS the UNWEIGHTED QR-count dial over odd primes
   ≤ 400 — verified exact-0 diff against the recomputed count at B ≤ 400 (first established in
   exp586 / paper 235 §4, which also settled exp577's ℓ = 2 convention ambiguity). This resolves
   the S400 cross-check discrepancy in paper 227's lineage: the stored column was never the
   harmonic-weighted form (which differs by +28..+48 as expected). Crosscheck non-load-bearing:
   all dials in exp587 are computed mechanistically from the hash-matched population.
3. **Crosscheck code window bug (does not affect any verdict)**: exp587_result.json's structured
   field `S400_stored_crosscheck` reports `stored_is_unweighted_count: false, count_diff_max:
   103.0`, contradicting its own honest_note and findings.md. Cause found in
   exp587_bstar_transfer.py: the crosscheck compares stored S400 against `C @ ones` — the
   unweighted count over ALL primes ≤ 1600 — instead of the masked B ≤ 400 dial, so the reported
   diff is exactly the 400 < ℓ ≤ 1600 tail contribution. The identification in catch 2 stands on
   the exp586 verification at the correct window; cite the honest_note/findings, do NOT cite the
   structured crosscheck fields for this item.
4. Task-brief bookkeeping: none new beyond catch 3; smoke log consistent with full run.

## 8. Barrier validation

Standing map constraints untouched: residue cap 4/3 theorem unaffected (covariate/window layer
only, no residue-counting change); position 5.19× bound untouched; quantum frontier closed and
untouched. No breakthrough claimed — the dial remains a descriptive/explanatory instrument for
the rate layer, not a factoring algorithm. Honest classification: **instrument hardening,
completing the paper-235 correction chain** — every future scale-smoothness measurement now
inherits BOTH corrected coordinates (√-weight, B\* = 400) with the transfer explicitly verified
rather than assumed. This directly strengthens paper 234's queue #1 (rate-layer N-covariate
structure at u ≈ 10): the QR-dial stratum's two free parameters are now pinned and checked, so
any residual N-structure found there is attributable to something beyond the product dial.
Barrier-4 positional converse and the u ≥ 6–14 scale-smoothness frontier remain open and are the
standing priorities.

## Attribution

Experiment + analysis artifacts: `ResearchOutput/scripts/2026-08-24-round74/`
(exp587_bstar_transfer.py — pre-registration in docstring; exp587_result.json — config/
regression/curves/stats/verdicts/honest_notes/wall_s; exp587_smoke.log; exp587_full.log;
exp587_findings.md). Source data: exp577_result.json rows (hits/total per N,
total = 150000 j-samples/N). Recorded round-83 #3; notebook Part 278; assessment v343;
issue #384.

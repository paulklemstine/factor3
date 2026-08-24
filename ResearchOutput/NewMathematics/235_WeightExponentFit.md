# Paper 235 — WEIGHT-EXPONENT-FIT: The Scale-Smoothness Dial's Optimal Weight Exponent Is α̂ = 0.5, Not 1 — H1 Fires with a Single-Peaked Interior Maximum (R² .32 → **.62** → .29 across α ∈ [0,2]), Bootstrap CI95 = [0.5, 0.5] Excluding 1 Decisively (492/500), and an ERRATUM-GRADE SUPERSESSION of Paper 227's Adopted Covariate: 1/ℓ Harmonic Weight REFINED to 1/√ℓ (√-Weight) Lab-Wide — Large Primes Carry ~√ℓ× More Relative Weight than the Inspection-Chosen Form Assumed, and the Fix Lifts Dial Power +31% Relative on Identical Data

**Verdict name: H1_HARMONIC_REFINED (√-WEIGHT)** — the harmonic law was right that weighting
matters (+0.152 R² over unweighted counting) and wrong about the exponent; fitted properly, the
optimal weight decays as ℓ^−0.5.

Round-83 #2 · exp 586 · pure reanalysis of exp577's stored per-N hit counts (no new j-sampling;
wall 0.2 s) · sources: `ResearchOutput/scripts/2026-08-24-round74/exp586_{weight_exponent.py,
smoke.log,full.log,result.json}` + `exp586_findings.md` · refines paper 227's law per paper 234's
ranked queue (C5 covariate-law follow-through).

## 1. Pre-registration (verbatim, written BEFORE analysis)

> Question: paper 227 adopted 1/l weighting for the product dial BY INSPECTION;
> fit the optimal exponent alpha properly.
>
> Pre-registered hypotheses (decided before touching the data):
>   H1 (harmonic refines): optimal alpha_hat != 1 with
>       dR2 := R2(alpha_hat) - R2(1.0) >= 0.03
>       ==> harmonic law REFINED to Sum(chi=+1)/l^alpha_hat;
>       report alpha_hat CI via bootstrap (resample Ns, 500 reps).
>   H0 (harmonic confirmed): alpha_hat = 1 within CI OR dR2 < 0.02
>       ==> harmonic weight CONFIRMED as the law's true form
>       (positive result: closes the refinement question).
>   Otherwise (0.02 <= dR2 < 0.03 and CI excludes 1): BORDERLINE-INCONCLUSIVE.
>
> Method (pre-registered):
>   1. Data = exp577_result.json rows: per-N hit counts (hits / total,
>      total = 150000 j-samples/N; ch6+ct6 gcd-chain tester path), population
>      recipe seed 20260827, bitlen 96, n = 128.
>   2. Regenerate the SAME 128 N values verbatim from exp577_product_dial.py
>      main(): random.Random(20260827), make_semiprime(bits=96) with the exact
>      rejection recursion + dedup; assert regenerated N[i] == stored rows[i].N.
>   3. For each N and each ODD prime 3 <= l <= 400 (l >= 3 only -- paper 231
>      lesson): c_l(N) = [Jacobi(N mod l, l) == +1] (mechanistic Legendre form).
>   4. For alpha in {0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0}:
>        S_alpha(N) = Sum_{odd prime l<=400} c_l(N)/l^alpha ;
>      regress y_N = log((hits_N + 0.5)/total_N) ~ S_alpha (OLS);
>      record R2 per alpha. alpha_hat = argmax_alpha R2.
>      Bootstrap: 500 reps resampling the 128 Ns with replacement (seeded),
>      alpha_hat* = argmax R2 per rep over the SAME grid -> percentile CI.
>   5. Verdict per the rules above. SANITY ANCHOR vs paper 227's sweep:
>      also record R2 at alpha = 0 (UNWEIGHTED count form Sum c_l) outside the
>      fitted grid; report whether ANY fitted alpha materially beats it
>      (materially := dR2 >= 0.02).

## 2. The α-curve

Regression form: log((hits+0.5)/total) ~ S_α, OLS, n = 128 semiprimes at bitlen 96
(mean hits/N = 77.58 over 150 000 j-samples).

| α | R²(log-rate ~ S_α) | r | slope ± SE |
|---|---|---|---|
| 0.0 (unweighted count, anchor) | .3207 | .566 | 0.0309 ± 0.0040 |
| 0.25 | .4985 | .706 | 0.1221 ± 0.0109 |
| **0.5** | **.6242** | **.790** | 0.3325 ± 0.0230 |
| 0.75 | .5752 | .758 | 0.5764 ± 0.0441 |
| 1.0 (paper 227's adopted form) | .4731 | .688 | 0.7957 ± 0.0748 |
| 1.25 | .3969 | .630 | 1.0350 ± 0.1137 |
| 1.5 | .3479 | .590 | 1.3360 ± 0.1630 |
| 2.0 | .2944 | .543 | 2.2461 ± 0.3098 |

The curve is SINGLE-PEAKED with an INTERIOR maximum at α̂ = 0.5; the adopted harmonic weight
α = 1 sits on the FALLING limb. Decision numbers:

- ΔR²(α̂) − R²(1) = **+0.15114** ≥ 0.03 bar → H1 fires; H0 rejected under both legs.
- Bootstrap (500 reps, resampling the 128 Ns, seed 586): α̂\* = 0.5 in **492/500**, 0.75 in
  **8/500** → **CI95 = [0.5, 0.5]**, mean 0.504 — **excludes 1.0 decisively** (no rep lands on
  or above the adopted value).
- Sanity anchors vs paper 227's own sweep: even the harmonic weight beats unweighted counting by
  **+0.152385** R² (227 was right that weighting matters); the fitted √-weight beats unweighted
  by **+0.303524** (and was wrong about the exponent).

## 3. ERRATUM-GRADE SUPERSESSION of paper 227's adopted covariate

Paper 227 (exp577) chose W(B) = Σ_{QR ℓ≤B} 1/ℓ by inspection, established its saturation by
B = 400, and adopted it lab-wide as the canonical scale-smoothness covariate (replacing the
equal-weight counts of papers 136/139/220/226). That supersession chain is itself now amended:

> **Adopted form: 1/ℓ → REFINED to 1/√ℓ.** Every future scale-smoothness dial computation uses
> √-weight: S(N) = Σ_{odd prime ℓ ≤ B} [jacobi(N mod ℓ, ℓ) = +1]/√ℓ.

What changes quantitatively:

- **Relative weights**: under 1/ℓ a prime at ℓ = 400 carries 1/133 of ℓ = 3's weight; under
  1/√ℓ it carries 1/11.5. Large informative primes carry ~√ℓ× more relative weight than the
  harmonic form assumed. The inspection-chosen 1/ℓ OVER-PENALIZED the tail; the true profile
  decays ℓ^−0.5.
- **Dial power**: on identical data, explanatory power of the rate layer rises from R² = .473
  (harmonic) to R² = .624 (√-weight) — **+31% relative** — with the unweighted floor at .321.
- **What does NOT transfer automatically**: window-location saturation (B\* = 400, corr .999)
  was measured UNDER the 1/ℓ weight (papers 136/139/227). Its transfer to √-weight is
  UNVERIFIED and must be re-checked before B\*-location claims are reused downstream. This is
  the named open check this paper leaves on the ledger.
- Interpretation note: the QR-status informativeness gradient across prime size is real but
  shallower than inverse-linear — consistent with the residue-dial picture in which each small
  prime is a strong but partially redundant dial reading (the product-dial law), while mid-range
  primes retain more marginal information than 1/ℓ credited them.

## 4. Integrity

- Population regeneration verbatim from exp577's recipe (random.Random(20260827), bitlen 96,
  exact rejection recursion + dedup): **128/128 Ns byte-identical** to stored rows.
- Recomputed odd-prime QR counts match exp577's stored S400 column **EXACTLY**: diff min = max =
  **0.0**, corr ≈ 1.0. Side finding: exp577's dial definition nominally left an ℓ = 2 ambiguity
  flagged in honest_notes; exact agreement shows its stored dial effectively excluded ℓ = 2 as
  well — the two computations used the same odd-prime convention in effect.
- Pure reanalysis: no new j-sampling anywhere in this experiment (wall 0.2 s full run); the data
  layer is exactly exp577's, so no seed-level replication risk is introduced beyond what 227
  already carried.

## 5. Limits (disclosed)

1. **Discrete grid**: α̂ is resolved only to ±0.25; fine structure near 0.5 was NOT fit, per the
   pre-registration. CI endpoints are grid points.
2. **One seed**: population seed 20260827 only; pure reanalysis, no fresh replicate. Per paper
   234/C3's multi-seed pooling mandate, absolute-R² claims should await multi-seed confirmation —
   though nothing here selects a direction in which the argmax would move.
3. **Log-rate attenuation**: OLS on log-rates with per-N Poisson noise (~150 k samples, mean hits
   77.6) attenuates R² uniformly across α — the same regime as exp577 itself — so the argmax is
   likely robust while all absolute R² values are lower bounds on the true signal fraction.
4. **Smoke-mode divergence**: smoke (n = 16, coarse grid) picked grid-edge α = 0.25 with wide CI
   [0.25, 1.0] — small-n noise; the full run is interior and tight. Recorded for honesty, not
   evidence about the population.

## 6. Ledger catches

- **Task-brief schema drift only** (raw_counts keys vs rows layout in the brief's pointer to
  exp577_result.json) — resolved during analysis; **no data issue**. No verdict-relevant
  bookkeeping items.

## 7. Barrier validation

Standing map constraints untouched: residue cap 4/3 theorem unaffected (this work touches the
covariate layer, not the residue-counting layer); no breakthrough claimed — the dial remains a
descriptive/explanatory instrument for the rate layer, not a factoring algorithm. Honest
classification: **instrument hardening**, adjacent to constant-shaving in isolation, but it
corrects the map's canonical covariate that every future scale-smoothness measurement inherits —
the same class of correction as paper 227's original adoption of weighting over counting, now
with the exponent measured rather than inspected. Barrier-4 positional converse and the u ≥ 6–14
scale frontier are untouched; the named open item this creates (B\*-transfer under √-weight) is
queued behind paper 234's ranked queue, whose #1 item (rate-layer N-covariate structure at
u ≈ 10) this experiment directly strengthens: the dial side of that decomposition now uses the
better-fitting weight, raising the ceiling on how much N-structure the QR-dial stratum can absorb.

## Attribution

Experiment + analysis artifacts: `ResearchOutput/scripts/2026-08-24-round74/` (exp586_weight_exponent.py
— pre-registration in docstring; exp586_result.json — config/regression/alpha_curve/stats/
verdicts/honest_notes/wall_s; exp586_smoke.log; exp586_full.log; exp586_findings.md).
Source data: exp577_result.json rows (hits/total per N, total = 150000).
Recorded round-83 #2; notebook Part 277; assessment v342; issue #383.

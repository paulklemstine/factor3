# Paper 213 — MA1-EFFECTIVITY-SWEEP: Quadratic-Character L-Value Magnitude Does Not Carry AP-Deviation Effectivity at Toy Scale — Clean H0 Honest Negative, Sign-Blind Scope Disclosed

**Verdict name: NULL-HONEST-NEGATIVE** (primary per-m carrier and cell-level secondary carrier BOTH below the pre-registered H0 bar of R² < 0.5, at two scales). Pre-registered verdict rules evaluated verbatim.
Round-74 #4 · exp 566 · assessment v320 · script `exp566_ma1_effectivity.py` (+ smoke/full logs + JSON) · seed 566 · walls 9.3 s (registered stage) / 247.7 s (final scaled artifact).

The MA-1 averaging assumption is the load-bearing axiom under which which-factor
blindness is an identity (papers 93/102/132). It has never carried a COMPUTABLE
effectivity criterion: nothing tells you when the average-over-residue-classes view
is actually realized by a given modulus. If deviations of prime counts in arithmetic
progressions were governed by the sizes of quadratic-character L-values, such a
criterion would exist: predict the per-modulus deviation magnitude D(m) from
P(m) = Σ over nontrivial real characters χ mod m of |L(1, χ)|.

**Pre-registered hypotheses (verbatim):**
- **H1:** "R^2(OBS(m) vs real-char L-prediction, per-m) > 0.8 => computable effectivity criterion"
- **NULL (H0):** "R^2 < 0.5 => effectivity NOT captured by quadratic-character size at this scale"
- **PARTIAL:** "0.5 <= R^2 <= 0.8"
- Either way: report fitted slope (= power-law exponent D ~ P^slope) + bootstrap CI.
- Pre-stated Mertens gate: "slope CI contains 1 and R^2 > 0.99, else LEDGER CATCH".

## Result 1 — the registered stage: power-law readout collapses far below the bar (H0)

Registered design executed in full with NO shrinkage: x = 2^26, π(x) = 3,957,809,
287 moduli (squarefree [3, 300] ∪ primes [307, 997]), wall 9.3 s. Primary OLS:
**log D ~ −0.0767 · log P, slope CI95 (−0.136, −0.015), R² = 0.0187** (bootstrap
R² CI95 [0.0007, 0.065]) — two orders of magnitude below the 0.8 H1 bar and well
under the 0.5 H0 bar. The slope is slightly NEGATIVE (more character mass ⇔
marginally smaller deviations), the opposite sign of the effectivity story. Partial
R² controlling log φ(m) = **0.0008**: once modulus size is held fixed, P(m) retains
essentially ZERO association with D(m). Secondary chi² readout agrees (R² = 0.025).
CONTROL passed: cross-modulus pairing permutation (2000 draws) collapses to null
(mean R² 0.0033 / max 0.0435). Disclosed spec deviation: literal within-modulus
residue-count permutation is VACUOUS for the registered readouts (max-abs and chi²
are permutation-invariant in a), so the meaningful control — shuffling the (m → D)
pairing against P — was run instead and reported.

## Result 2 — the final scaled artifact doubles down: 2489 moduli at x = 2^28, same verdict

The session then scaled UP and overwrote `exp566_result.json` with the definitive
artifact (status `07_final`): x = 2^28, π(x) = **14,630,843**, **2489 moduli**
(all m ∈ [2, 1500] dense + primes beyond), wall 247.7 s. Primary per-m carrier
(OBS vs real-char prediction): **R² = 0.0785 → NULL_HONEST_NEGATIVE** (< 0.5).
Cell-level secondary carrier (y vs log(1/L), 1902 discriminant cells):
R² = **0.00052**, theory-signed slope B = −0.0342 CI [−0.101, +0.033] — not even
positive as theory requires. BASELINE SIZE CONTROL: OBS ~ log m alone explains
**R² = 0.790** of the deviation variance — the deviation field is dominated by
modulus size, and after that size effect there is nothing for character-L mass to
explain. Truncation quality on the final run: real-share median 8.7e-4
(IQR [1.2e-4, 6.7e-3]), rms rel err median 3.4e-3, worst-case 8.2e-2.

## Result 3 — verification path

L(1, χ) computed by an EXACT class-number route for fundamental D < 0, |D| ≤ 400
via Gauss-reduced binary-quadratic-form counts, L = 2πh(D)/(w√|D|); validated
exactly: **L(1, χ₋₃) = π/(3√3)** recovered exactly (h(−3) = 1, w = 6). All other
discriminants use a truncated series (N = 10⁵, block-harmonic form), CALIBRATED on
the exact-path overlap: **226 overlap discriminants, median relative error
1.8 × 10⁻⁵**. Positive-D (real-quadratic) L-values are always truncated (no
regulator path implemented) — error assumed similar to the calibrated overlap;
this asymmetry is part of why the sign-blind caveat below matters.

> **SCOPING CAVEAT (prominent, pre-registered readout is magnitude-only):** the
> registered statistic D(m) = max_a |π(x;m,a) − E|/√E is **SIGN-BLIND**, and the
> predictor enters as |L(1, χ)| magnitudes summed over characters. This result
> therefore bounds the MAGNITUDE ROUTE ONLY. A signed character-alignment analysis
> (does the SIGN pattern of {χ(a)} align with the signed residue-count deviations?)
> is the required follow-up BEFORE the L-value route can be killed. What is dead
> here is specifically: quadratic-character L-value SIZE does not price AP-deviation
> magnitude at toy scale.

## Barrier framing

H0 here does NOT weaken the barrier program — it honestly bounds one computable-
criterion route. The barrier-map residual item "**MA-1 effectivity**" stays OPEN as
a gap item: MA-1 remains axiomatic at practical scale (the averaging assumption is
used, not derived), and no computable per-modulus criterion for its effectivity is
armed by this sweep. Consistent with the standing map: the only strong predictor of
D(m) found here is modulus size itself (baseline R² 0.79), i.e., a φ(m)-driven
size effect, not factor-relevant structure.

## Ledger

Five catches, none adverse after fixing/disclosure:
1. **Off-by-one in the truncated series** corrupted ALL non-exact L-values in an
   initial draft (χ₅ gave 0.127 vs true 0.430) — caught by spot check against the
   exact path, fixed, rerun before any recorded fit.
2. **Smoke control gate failed at n = 29 moduli** (permutation null did not collapse
   at tiny n: headline flagged "[CONTROL DID NOT COLLAPSE]") — resolved at full
   scale where the null collapses cleanly (mean 0.0033 / max 0.0435).
3. **Mertens gate FAIL (pre-stated rule, disclosed):** final-run u vs log L slope
   0.9277 CI [0.9234, 0.9320], R² = 0.9894 — the gate required CI ⊇ 1 AND R² > 0.99;
   the scaling is near-proportional but sits just outside the strict band
   (implied K̄ = −0.216, within the theory bound |K| ≤ 0.756).
4. **Scale-reconciliation disclosure:** findings/digest describe the REGISTERED
   stage A (x = 2^26, 287 moduli, R² = 0.0187), while the canonical
   `exp566_result.json` holds the final scaled rerun (x = 2^28, 2489 moduli,
   primary-permutation carrier R² = 0.0785) whose output overwrote stage-A's file
   mid-session; the extended-rerun script variant was not separately preserved on
   disk (the preserved script is the registered small-scale version). BOTH stages
   agree on the verdict: clean H0 honest negative.
5. **Coordination disclosure:** a parallel duplicate agent (coordinator
   double-dispatch after a stall) left an orphaned script draft
   `exp566_ma1_effectivity_alt_agentB.py` in the directory with NO results attached;
   the recorded artifact set is solely from the completing agent. Orphan left in
   place, unreferenced by results.

## Conclusion

Quadratic-character L-value magnitude does NOT capture AP-deviation effectivity at
toy scale — R² ≈ 0.02 (registered stage) and 0.08 (scaled artifact) against bars of
0.8/0.5, with the entire explainable variance absorbed by modulus size. Clean H0,
evaluated verbatim, at two scales. MA-1 stays axiomatic; the effectivity question
survives only through the SIGNED route, which this magnitude-blind sweep could not
touch. No breakthrough; one gap item honestly bounded. Now 556 experiments
(max id 567). Assessment v320.

# Paper 227 — PRODUCT-DIAL-SCALESHIFT: H1 Scale-Shift REFUTED, H0 Blocked — the QR Window Does NOT Move Past 400 (Equal-Weight Counting Buries Primes Informative ~1/ℓ; B\* = 400, Papers-136/139 Location CONFIRMED Scale-Independent), the 1/ℓ-Weighted Product Dial Is the Law (48% D-Reduction Already at B=400, Saturating by 10⁶, corr = 0.999), and a Verified Three-Part Diagnosis Makes Paper 226's SECONDARY Conclusions ERRATUM-GRADE (Reciprocity-Sign Dial-Form Artifacts, 100% Flip-on-Condition) While Its PRIMARY Null Stands

**Verdict name: WINDOW-STRONGER-NOT-SHIFTED** (pre-registered: H1 scale-shift REFUTED; H0 cannot
fire because the ≤400 dial alone clears the 30% bar this seed) **plus a verified two-artifact
diagnosis touching recorded paper 226**. Paper 226 named the follow-up: its ≤400 dials explained
≤14.2% of u≈10 per-N hit-count overdispersion, and the hypothesized cause was that the informative
prime window had SHIFTED past 400 (bitlen-96 pools span ~2⁴⁹–2⁵¹, hits need LPF ≤ 10⁶). Here we run
the full product-form dial over ALL odd primes ℓ ≤ 10⁶ under fixed bars. Answer: no shift exists —
extension past 400 DILUTES the count signal — but once the dial is harmonically weighted by 1/ℓ,
~48% of the dispersion is QR-carried at every bound tested, saturating by B = 400. Round-79 #1 ·
exp 577 (+ independent verification verifyL7b) · sources:
`ResearchOutput/scripts/2026-08-24-round74/exp577_product_dial.py` (pre-registration in header
BEFORE any data generation; post-verification REVISION annotated in-script) → `exp577_result.json`
(+ smoke pair, `exp577_diagnostics.py/.json`), wall 380.8 s full; `verifyL7b_exp577_check.py` →
`verifyL7b_result.json`, wall 187.1 s.

## Population and lineage discipline

128 balanced bitlen-96 semiprimes, FRESH master seed **20260827**, generator/tester VERBATIM
exp576/exp569 (gcd-chain primorial tester, 150k j-samples/N, cut 10⁶). All four master-seed
hashes asserted pairwise disjoint and RECORDED: prior trio e8d89a29a03779d5 (20260824) /
9cb9cc800ee45a38 (20260825) / 81acc9b5e1be619b (20260826) REPRODUCED EXACTLY, new hash
**a15e2877dd1dac7a** — stream-distinctness held across the whole four-seed family.

The u≈10 overdispersion REPLICATES a THIRD time on fresh seed: mean **77.58 hits/N**,
Var/mean **D_raw = 4.90** (φ_null 4.93; Poisson would be ~1), range 37–135, top-3 clusters
**135/135/130**, top-decile/bottom-decile rate ratio **2.416**, zero-hit N count 0.

## Pre-registration (verbatim from the script header)

> Dial (exact): S_prod(N;B) = #{prime l <= B : jacobi(N mod l, l) == +1}. … Cumulative sweep:
> B in {400, 4000, 4e4, 1e5, 1e6} … Bars (FIXED before data):
> base_R2 := R2_log(S_prod; B=400) measured on THIS population/machinery.
> Leg (i) at a shift candidate B: R2_log(B) >= 0.16 AND R2_log(B) >= 2 x base_R2
> (0.16 = 2x the ~0.08 exp576 measured for the <=100/<=400 dials).
> Leg (ii) at a shift candidate B: D_reduction(B) >= 30%.
> Shift candidates: B in {4000, 4e4, 1e5, 1e6}. B=400 itself cannot evidence a SHIFT; if
> D_reduction(400) >= 30% alone, record verdict WINDOW-STRONGER-NOT-SHIFTED (disclosed; does
> NOT fire H1).
> H1 (scale-shift REAL, pre-named primary candidate B=1e6): any shift candidate clears leg (i)
> or leg (ii) => verdict QR-WINDOW-SHIFTED … CONSEQUENCE: papers 136/139/220 unify under a
> SCALE-DEPENDENT dial bound …
> H0 (no shift): NO shift candidate clears either leg => verdict NO-QR-CARRY-ANY-SCALE-LE-1E6 …

The original header also claimed this dial EQUALS exp576's product form "since reciprocity signs
cancel in the product" — **FALSE, retracted by verification** (see the three-part diagnosis);
the in-script REVISION annotation states the correct relation and that exp576's forms are
partially inverted mixtures.

## Result 1 — the sweep: NO shift past 400; extension DILUTES

| cumulative bound B | R²_log | slope | GLM z | D-reduction |
|---|---|---|---|---|
| **400** | **0.3207** | + | 14.16 | **33.43%** |
| 4 000 | 0.0241 | + | 3.84 | 2.40% |
| 4·10⁴ | 0.0150 | − | −3.25 | 1.68% |
| 10⁵ | 0.0000 | − | +0.14 | 0.00% |
| 10⁶ | 0.0277 | + | 5.02 | 4.11% |

All four shift candidates fail BOTH legs with graded margins recorded (R² margin to the 0.16 abs
bar: −0.136 / −0.145 / −0.160 / −0.132; no candidate near either leg). **H1 QR-WINDOW-SHIFTED is
REFUTED.** H0 (NO-QR-CARRY-ANY-SCALE) is BLOCKED by the pre-disclosed branch: D_red@400 = 33.4%
≥ 30% ⇒ verdict **WINDOW-STRONGER-NOT-SHIFTED**, B\* = argmax R² = **S400**. Mechanism of the
dilution: equal-weight counting buries the informative small primes — a prime ℓ contributes one
count whether ℓ = 3 or ℓ = 999 983, but its QR status is informative at weight ~1/ℓ. **Paper
136/139's window location is CONFIRMED SCALE-INDEPENDENT** — the fade paper 226 measured was
never a window-location effect.

## Result 2 — the WEIGHTED dial is the law

W(B) = Σ_{QR ℓ ≤ B} 1/ℓ (harmonically weighted product dial):

| dial | R²_log | GLM z | D_cond | D-reduction |
|---|---|---|---|---|
| **W400** | **0.4731** | 16.77 | 2.54 | **48.11%** |
| **W10⁶** | **0.4786** | 16.83 | 2.52 | **48.51%** |

corr(W10⁶, W400) = **0.999** on this population and **0.9991 / 0.9985** (Pearson/Spearman) on the
verifier's INDEPENDENT population — the signal SATURATES BY 400 once harmonically weighted: adding
primes 400..10⁶ changes almost nothing. The weighted dial is ALSO seed-robust: on verifyL7b's own
64-N population (seed 20260831) W400/W10⁶ read 47.14%/48.18% D-red. **Recommendation ADOPTED:
the 1/ℓ-weighted product dial is the canonical scale-smoothness covariate**, replacing the
equal-weight count used throughout papers 136/139/220/226. Note corr(W400, C400-count) = 0.365 —
weighted and count dials agree on existence of carry, disagree on allocation; the weighted form
dominates on every statistic.

## Result 3 — verified three-part diagnosis of paper 226 (erratum-grade for its SECONDARY conclusions)

Independent verification (verifyL7b, separate script/log/result, own seed 20260831, n=64 +
re-analysis of the exp577 population):

**(1) Paper 226's SECONDARY E-forms are composite-bottom dials whose weakness is a DIAL-FORM
ARTIFACT.** exp576's S_prod/S139 were computed as (ℓ|lo)(ℓ|hi) — a composite-bottom form tied to
the mechanistic clean Legendre dial (ℓ|N mod ℓ) by quadratic reciprocity: the two AGREE iff NOT
(ℓ ≡ 3 mod 4 AND N ≡ 3 mod 4), and FLIP otherwise. Measured on the exp577 population: %N≡3 mod 4
= **52.3%**; conditional flip rate **100%** (2680/2680 flips, 0 agreements, 0 condition
violations); unconditional flip-event rate **27.19%** = 52.3% × frac{odd primes ≤ 400 ≡ 3 mod 4}
(0.5195) — predicted 27.19%, matched TO THE SECOND DECIMAL (replicated on the verifier population:
45.3%, 1160/1160, 23.54% = 45.3% × 0.5195). Under the correctly flipped forms the published
weakness class reproduces exactly where 226 saw it — flipped S_prod@100: R² .030/D-red 4.11%;
flipped S139@400: **R² .0456/D-red 5.46%** (vs 226's printed S_prod .0781/14.22% and S139@400
.0565/9.07%) — while the CLEAN bound-100 Legendre dial is STRONG on the same rows with the same
hits/machinery: **C100-clean R² .3728/D-red 34.45%** (r vs C400 = 0.476), C400-clean .3207/33.43%.
**Printed claims of paper 226 RETRACTED-AS-ARTIFACT: the S_prod row (.0781/14.22%) and the
S139@400 row (.0565/9.07%) of its Results table, and every downstream sentence built on them**
("the secondaries, which DO carry the divisibility signal, also miss H1"; "explains at most ~14%";
"≥86% is N-structure beyond every recorded mechanism").

**(2) Paper 226's PRIMARY S_indiv NULL REPLICATES AS A TRUE NULL here too**: R² = .0019,
D-red 0.09%, z = 0.72 — the flip mechanism is INAPPLICABLE (no composite bottom: S_indiv sums
individual Jacobi symbols, no product of factors to invert), so no contradiction remains with
paper 226's primary. It is a consistent null; ONLY the secondary conclusion is retracted.

**(3) The exp576-vs-exp577 apparent contradiction on S400 (0.078 vs 0.32) is TRACED, not a
reproducibility failure**: form difference (composite-flipped vs clean Legendre) PLUS estimator
spread — verifyL7b recomputed C400 == recorded S400 on **128/128 rows** (column integrity exact),
yet on its own 64-N population C400 reads 19.01% D-red while C100-clean stays strong in BOTH
populations (34.45%/34.75%) and the flipped E400 stays weak in both (5.46%/2.43%). Documented;
single-seed single-population OLS/GLM spread at these effect sizes is real and should be quoted
as a band, not a point.

## Dispersion bookkeeping (both readings, disclosed)

| dial | D-red (% of raw) | excess-above-Poisson explained | residual (% raw) | residual (% excess) |
|---|---|---|---|---|
| count @400 (33.43%) | 33.4% | **42.1%** | ~66.6% | ~57.9% |
| W10⁶ (48.51%) | 48.5% | **61.0%** | ~51.4% | ~39.0% |

Residual still OVERDISPERSED under every dial (D_cond > 1 everywhere: 3.26 / 2.52). One
bookkeeping caveat recorded by the verifier: the identity D_red = 100×(1−D_cond/D_raw) does NOT
hold exactly across all columns (GLM deviance vs Var-ratio definitions differ); the two readings
are reported separately rather than forced into one number. **CONSEQUENCE: paper 226's "≥86%
new structure" SHRINKS to ~39–58% residual non-QR structure (dial/reading dependent)** — u≈10
overdispersion is MORE QR-carried than 226 concluded, and the residual target for future
mechanism work moves accordingly.

## Ledger catches (adversarial in BOTH directions)

1. **First-draft ORTHOGONALITY claim RETRACTED by verification**: the script header originally
   claimed the clean product dial equals exp576's form "signs cancel" — verification PROVED the
   reciprocity sign does not cancel (flip iff ℓ≡3 mod 4 ∧ N≡3 mod 4); annotated in-script. Via a
   LABEL SWAP clarified post-hoc (verifyL7b's "formA" column is coded
   gjac(lo%p,p)\*gjac(hi%p,p) = (N|p), i.e. it IS the clean C100 dial, while its own audit text
   defines form-A as (ℓ|lo)(ℓ|hi)), r(flipP100, C400) = **0.058** STANDS — for the FLIPPED form.
2. **Verifier's addendum leg REJECTED empirically by author**: the proposed "removing ℓ=2 makes
   formA strong" rescue FAILS — flipped-form without ℓ=2 stays weak (.0322/4.34%; ℓ=2 shifts
   counts by 0/1 only). Verification is adversarial toward the authors' claims AND the authors
   re-test the verifier's; neither side's word is data.
3. **Pre-registration header error caught and annotated** (the "(signs cancel)" clause above).
4. **ℓ=2 even-modulus crash caught in smoke** (Jacobi needs odd modulus) — fixed before the full
   run; no data impact.
5. **Self-catches pre-ledger**: first-draft T1 bound mismatch; missing-/n correlation slips.
6. **Smoke n=16 spuriously FIRED H1** (QR-WINDOW-SHIFTED via S4000 leg-ii at D-red 35.31%);
   the full n=128 run refutes it — small-n verdicts on this pipeline are unstable and the smoke
   verdict is hereby marked NON-EVIDENTIARY.
7. **Lineage discipline exemplary**: four master-seed hashes reproduced/asserted pairwise
   disjoint (three prior REGENERATED exactly, fourth new).

## Barrier validation

Serving the standing directive's scale-smoothness frontier (u ≥ 6–14 deviations): this experiment
closes the named follow-up of paper 226 with pre-registered bars — the window does not move, the
weight is the law, and the canonical covariate for ALL scale-smoothness work upgrades from count
to 1/ℓ-weighted product dial (papers 136/139 stand at their own scale, now with their window
LOCATION vindicated and their FORM upgraded). The residual non-QR target (~39–58%) replaces the
overstated ≥86%. Residue cap 4/3 theorem untouched; no complexity claim; no breakthrough claimed;
paper 226 corrected in place rather than contradicted — its phenomenon replication, primary null,
and orthogonality algebra survive.

## Bottom line

exp577 runs paper 226's named follow-up under fixed bars and gets WINDOW-STRONGER-NOT-SHIFTED:
no shift past 400 (all candidates fail both legs; extension dilutes an equal-weight counter),
B\* = 400 confirming papers-136/139's window location scale-independent, and the 1/ℓ-weighted
product dial carrying 48% of u≈10 dispersion at EVERY bound with saturation by 400 (independent-
population corr 0.9991) — adopted as canonical covariate. Verification completes an erratum-grade
two-artifact diagnosis of paper 226: its secondary weakness numbers are reciprocity-sign dial-form
artifacts (flip 100%-on-condition, 52.3% of N, unconditional rate matched to 2nd decimal), its
primary null is consistent and stands, and its headline "≥86% N-structure" contracts to ~39–58%
residual. The ledger caught errors on both sides of the verification and retracted them before
publication.

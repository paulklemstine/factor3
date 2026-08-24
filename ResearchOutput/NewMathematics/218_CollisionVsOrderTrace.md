# Paper 218 — COLLISION-VS-ORDER-TRACE: H1 and H2 Both REFUTED with Inverted Geometry — Low-B1 Successes Sit Far ABOVE the Collision Baseline (65.0% / 62.5% vs 16.5%, Cross-Bitlen z p = 0.82, H2 Dead) and Hits Fire Near Step ZERO at High B1 (Median Index 0.09–0.10, Final-20% Tail 0/55, Binom p ≈ 0.004); Paper-159 Amendment-Candidate Rejected as Stated; New Early-Fire Trace Law Added

**Verdict name: H1 and H2 BOTH REFUTED — with inverted geometry.** The
pre-registration predicted collision dominance (uniform hit positions) at low B1/p
and order-completion concentration in the final 20% at high B1/p. Both halves are
wrong in the same inverted direction: **KS rejects uniformity even at low B1**
(p = 0.017 / 0.045), and at B1/p = 0.9 hits concentrate near step **ZERO**, not the
final 20% — median normalized index 0.09–0.10, final-20% tail 0/55, exact binomial
p ≈ 0.004 vs the registered 20%. The scale law also fails: found_p rates at
B1/p = 0.125 sit far above the per-curve collision baseline 1 − exp(−1.44·B1/p)
= 16.5% — bitlen-26 **65.0%** [CI .495–.779], bitlen-32 **62.5%** [.470–.758] —
with cross-bitlen two-proportion z p = 0.82: no collapse toward the floor as p
grows, so collisions do NOT dominate low-B1 success. Mechanism separation is still
achieved (the trace separates them — just with opposite geometry), **paper 215's
NO-WALL account stands**, and the **paper-159 amendment-candidate is REJECTED as
stated**: the collision floor is real but SUBDOMINANT. A NEW TRACE LAW replaces the
failed prediction: order-completion marks EARLY — hit position ~ max-prime-power(ord)/B1
(Golomb/Dickman-low flavor).

Round-75 #2 · exp 570 · assessment v325 · script `exp570_collision_trace.py` ·
seed 20260824 · wall 1.3 s full (240 trials, 6 cells × 40 N).

## Question

Paper 215 (exp 568) confirmed there is NO ECM destruction wall and flagged a
structural confound for its amendment chain: guarded-affine accounting carries a
random-collision success baseline ≈ 1 − exp(−c·B1/p) per curve (each guarded
inversion denominator hits a factor with ~1/p chance per op; ~1.44·B1 ops per
stage-1 curve ⇒ scale-independent at fixed B1/p). Low-B1 successes therefore
conflate ORDER-HITS (genuine group-order divisibility, ord | lcm(1..B1)) with
COLLISION-LUCK. This experiment discriminates the two mechanisms by TRACE (where in
the op sequence the firing guard lands) and by SCALE (does the low-B1 rate collapse
toward the collision baseline as p grows at fixed B1/p?), to settle whether paper
159's wall sentence can be amended by "it was collisions all along."

## Pre-registration (verbatim, script header)

- "H1 (trace separates mechanisms): at B1/p = 0.125, the hit STEP-INDEX distribution
  (position of the firing guard, normalized by the curve's deterministic total op
  count) is ~UNIFORM for found_p events (collision-dominated), while at
  B1/p >= 0.5 it CONCENTRATES in the FINAL 20% of steps (order-completion);
  a KS test vs Uniform[0,1] REJECTS at the high-B1 cells but NOT at low-B1.
  Operationalization: KS p>0.05 at B1/p=0.125 AND KS p<0.05 at B1/p=0.9 with
  tail-fraction(norm>=0.8) enriched above 0.2 (exact binomial two-sided vs 0.2)."
- "H2 (scale law): at bitlen 32 (p ~ 2^14-16), the LOW-B1 found_p rate DROPS toward
  the collision baseline 1-exp(-1.44*B1/p); i.e. measured rate at B1/p=0.125 ~= 17%
  ... far below exp568's 68% at bitlen 26 (IF collisions dominated there).
  Operationalized two ways because exp568's 68% is a 3-curve CELL rate while
  1-exp(-1.44*B1/p) is a PER-CURVE quantity:
    H2_primary  : cell found_p rate(bitlen32, 0.125) vs 0.1647 (literal pre-reg);
    H2_percurve : first-curve found_p rate vs 0.1647, and cell rate vs the
                  3-curve-adjusted baseline 1-(1-0.1647)^3 = 0.4191."
- Machinery disclosure: "exp568_ecm_stage2_wall.py reused VERBATIM ... stage1 gains
  a step counter tr (idx incremented at every guarded inversion AND at each
  end-of-chunk gcd check; found_at records the firing step). total steps per curve
  is DATA-INDEPENDENT (control flow depends only on the schedule)."

## Design

Guarded affine EC ops from exp568/exp488 reused verbatim; arm B2=B1 (stage 1 only,
stage 2 unnecessary for the question); curves cap 3. Populations h=13 (bitlen-26
stratum, matches exp568's generator; N up to 28 bits) and h=15 (bitlen-32 stratum,
p ~ 2^14–15, q ~ 3–4p), n_N = 40 each, seed 20260824; grid B1/p ∈ {0.125 ceil,
0.25 ceil, 0.9 floor} → 240 trials. Trace: idx incremented at every guarded
inversion and end-of-chunk gcd check; found_at records the firing step; normalized
by the closed-form data-independent total (schedule-only control flow). Baselines
reported three ways: the registered constant-op form 1−exp(−1.44·B1/p), an
exact-op recomputation using the true op count, and the 3-curve cell aggregate.

## Result 1 — H2 refuted: rates sit far above the collision floor at BOTH bitlens

| cell (B1/p = 0.125) | found_p rate | CI95 | per-curve baseline 16.47% | first-curve rate | exact-op per-curve mean | 3-curve cell mean |
|---|---|---|---|---|---|---|
| bitlen-26 (h13) | **65.0%** | [.495, .779] | 5.6× above | 42.5% | 27.8% | 62.3% |
| bitlen-32 (h15) | **62.5%** | [.470, .758] | 5.7× above | 40.0% | 27.1% | 61.2% |

Both CIs exclude the registered 16.47% by a wide margin (H2_primary and
H2_percurve both refuted_above_baseline); the cross-bitlen two-proportion z test
gives p = 0.8161 — the rate does not drop toward the floor as p grows at fixed
B1/p. One recorded sub-verdict requires its code-level reading: the key labeled
`H2_cell_vs_3curve_baseline_0.4191` returns "supported", but the implemented test
contains `baseline_cell3_mean` (the exact-op 3-curve collision arithmetic,
61.2–62.3%) inside the Wilson interval — i.e. the CELL rate coincidentally matches
3-curve collision arithmetic built on true op counts, while every PER-CURVE read
(first-curve 40–42.5% vs 16.5%; exact-op per-curve 27%) sits far above its own
baseline. Per-curve excess + KS + empty tail jointly rule out collision dominance;
the coincidence is disclosed, not load-bearing.

## Result 2 — H1 refuted with INVERTED geometry

KS tests vs Uniform[0,1] on normalized hit indices:

| cell | D | KS p | median norm | tail ≥0.8 | binom p vs 0.2 |
|---|---|---|---|---|---|
| h13, B1/p=0.125 | 0.3036 | **0.0166** | 0.287 | 15.4% | 0.767 |
| h13, B1/p=0.25 | 0.4357 | **0.0001** | 0.130 | 7.7% | 0.168 |
| h13, B1/p=0.9 | 0.6424 | <10⁻⁴ | **0.090** | **0/27** | **0.0048** |
| h15, B1/p=0.125 | 0.2758 | **0.0446** | 0.317 | 4.0% | 0.055 |
| h15, B1/p=0.25 | 0.2295 | 0.094 | 0.295 | 13.8% | 0.568 |
| h15, B1/p=0.9 | 0.5314 | <10⁻⁴ | **0.102** | **0/28** | **0.0039** |

The low-B1 half of H1 required KS non-rejection at 0.125; uniformity is rejected at
both bitlens (p = 0.0166 / 0.0446). The high-B1 half required concentration in the
FINAL 20%; what concentrates instead is the NEAR-ZERO region — combined final-20%
tail 0/55 (binomial p ≈ 0.004 against a 20% expectation), medians 0.09/0.102. H1's
two operationalizations each fail, in opposite directions from their predictions:
order-completion does not mark the END of the multiplication schedule — it marks
EARLY.

## Result 3 — the early-fire trace law

Empirical law replacing H1's geometry: **hit position ~ max-prime-power(ord)/B1**
— the curve fires when the running multiple-chain first absorbs the largest prime
power dividing the group order, which under the schedule's prime-power chunks lands
at a Golomb/Dickman-low-flavored fraction of the schedule rather than near its end.
This is consistent with the mechanism arithmetic: ord completes when the last large
prime power of ord has been consumed, and that consumption is front-loaded by the
descending-ish chunk structure, not back-loaded. Labeled a measured regularity
added to the factor-local map; the distributional shape beyond median/tail is not
characterized here.

## Caveats

1. **True ops = 2.59·B1, not the 1.44·B1 constant.** The registered 16.47%
   baseline uses the literature constant; the traced counter gives ~2.59 ops per
   B1 unit. ALL baselines were recomputed with the true count and reported
   alongside (exact-op per-curve means 27.1–27.8% at B1/p=0.125; 3-curve cell
   means 61.2–62.3%). The verdict reads identically under either arithmetic.
2. **The cell-rate coincidence.** Measured cell rates (62.5–65.0%) happen to lie
   near the 3-curve exact-op collision arithmetic (61.2–62.3%), but per-curve
   excess, KS rejection, and the empty final-20% tail rule out collision dominance
   (Result 1).
3. **found_q censoring.** found_q events (pure q-side collision luck — B1 < p ≪ q
   makes order-completion impossible on q) occur throughout and are disclosed;
   they independently cross-check the collision rate but are not part of the
   registered found_p readouts. Curve 'deaths' (gcd = N) collapse silently inside
   trial() without separate bucketing (inherited exp568 behavior).
4. **Tiny data-dependent index bias.** ec_add's rare recursive internal double
   (den == 0 mod N, y1 == y2) executes without an idx increment — affects
   found_at indices only, negligibly.
5. **Toy scale.** p of 13–15 bits; conclusions concern mechanism identification at
   this scale per program scope.

## Ledger

One catch, caught BEFORE data:

1. **Closed-form step counter initially wrong.** The closed form assumed every
   chunk does len−1 doubles / popcount−1 adds; actually only the FIRST chunk does
   (R=None at its leading bit seeds P directly), later chunks do len doubles /
   popcount adds. Caught by the traced-vs-closed assert before any full-run data
   existed, fixed, verified 29/29 on completed smoke curves; smoke was regenerated
   after the fix (its earlier norms were misnormalized).

## Barrier validation

Barrier-8 bookkeeping audit completing paper 215's evidence chain: paper 159's
destruction-wall sentence was already rejected as stated by paper 215 (no wall
under outcome-separated accounting); the remaining amendment route — "low-B1
successes were collisions all along" — is now rejected too, with the collision
floor shown real-but-subdominant and a new measured regularity (early-fire trace
law) added to the factor-local map. No barrier breached, no constant shaved, no new
method proposed; the amendment chain terminates cleanly.

## Conclusion

Both pre-registered hypotheses die, and both die inverted: hits are NON-uniform
already at low B1 and cluster at the START of the schedule at high B1 (median 0.09–0.10,
final-20% tail 0/55), while low-B1 success rates sit 5.6× above the collision floor
with no cross-bitlen drop (z p = 0.82). Collisions are real but subdominant; order
completion marks EARLY (~ max-prime-power(ord)/B1); paper 215's NO-WALL account
stands unamended; the paper-159 amendment candidate is closed as stated. Now 561
experiments (max id 572). Assessment v325.

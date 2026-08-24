# Paper 217 — MA1-SIGNED: The Signed Route of MA-1 Effectivity Dies at Both Registered Criteria — Cell Sign-Agreement 15.07% (CP95 [0.120, 0.186]) with Circular-Sum z = −52.7; Class Level 48.74%, z = −7.74, Significantly Below Chance; MA-1 Computable-Effectivity Program CLOSED on Both Routes

**Verdict name: H0** on both registered criteria and both levels — cell-level
sign-agreement 15.07% over 491 (m,χ) cells, Clopper–Pearson 95% [0.1202, 0.1855],
circular-sum z = −52.72 against the within-modulus d-shuffle null (2000 draws);
class level 48.74% over 86,882 unit classes, CP95 [0.4841, 0.4907], permutation
z = −7.74 — significantly **below** chance. Neither C1 (CP95 wholly > 50%) nor
C2 (z > 3) fires anywhere. **The MA-1 computable-effectivity program is CLOSED on
BOTH routes**: magnitude died in paper 213/exp566 (R² = 0.019), sign dies here.
A named barrier-map residual question closes as an honest negative.

**KEY STRUCTURAL DISCLOSURE** (made post-smoke, before any full data): L(1,χ) > 0
for EVERY real non-principal Dirichlet character (a consequence of the analytic
class-number formula), so sign(w) ≡ +1 identically — confirmed at full scale,
n_cells_w_negative = 0 — and registered criterion C1 reduces exactly to
Pr[c_χ > 0]. The informative content of the cell readout is therefore the realized
skew itself, reported here as a named byproduct: **prime counts twist negative in
84.7% of cells (CP95 [0.8123, 0.8779])** — the universal Chebyshev /
Rubinstein–Sarnak low bias, independently confirmed inside the lab's own
AP-deviation machinery at x = 2²⁶.

Round-75 #1 · exp 572 · assessment v324 · script `exp572_ma1_signed.py` · seed 572
· wall 6.96 s (analysis-heavy, sieve-bound).

## Question

Paper 213 / exp566 bounded the MAGNITUDE route of MA-1 effectivity: quadratic
|L(1,χ)| does not predict |AP deviations| (R² = 0.019, CI [0.001, 0.065]), but its
scoping caveat preserved a second route — do *signed* character components ALIGN
with deviation patterns even though magnitudes do not track? A positive answer
would be the first computable handle on AP-deviation structure; a negative one
closes the "MA-1 effectivity" residual of the barrier map on both routes at once.

## Pre-registration (verbatim, script header)

- Background/identity: "with d_a = pi(x;m,a) - li(x)/phi(m) over unit classes a,
  c_chi = sum_a d_a * chi(a) = sum_{p<=x} chi(p), because sum_a chi(a)*li(x)/phi(m)
  = 0 by character orthogonality. Hence the NAIVE li-based theory character sum
  vanishes IDENTICALLY and predicts no sign; the only computable x-independent
  theory object carried by chi alone is its signed L(1,chi)."
- "H1 (signed structure): sign pattern s(m,a)=sign(pi(x;m,a)-li(x)/phi(m))
  correlates with the L-value-predicted pattern ABOVE CHANCE across moduli,
  measured by EITHER registered criterion: (C1) cell-level sign-agreement rate
  r = Pr[ sign(c_chi)=sign(w_chi) ] over ALL nontrivial-real-char (m,chi) cells
  has Clopper-Pearson 95% [CI wholly above 0.5], OR (C2) circular-sum z>3 vs
  within-modulus shuffle null (2000); class-level analogue reported."
- "H0: agreement <= chance under both criteria at both levels => the signed route
  is dead at this scale too => MA-1 computable-effectivity program CLOSED on BOTH
  routes (honest negative strengthening paper 213)."
- Direction disclosure (verbatim): "NO theorem forces sign(c_chi(x)) to follow
  sign(L(1,chi)); the motivation is the Mertens/Euler-product link log L(1,chi) ~
  sum_p chi(p)/p making L(1,chi)'s sign a candidate low-frequency summary of the
  chi-twisted prime bias."

## Design

Machinery reused verbatim from exp566 (`exp566_ma1_effectivity.py`). x = 2²⁶ =
67,108,864 full (π(x) = 3,957,809; li(x) = 3,958,349.55); moduli = squarefree
[3, 300] ∪ primes [307, 997] → 287 moduli, K real characters per modulus by ω(m);
deviations d_a taken over UNIT classes only (non-unit classes contain ≤ 1 prime —
the single-prime artifact — and carry χ(a) = 0 anyway); observed c_χ = CH·d,
asserted equal (< 10⁻⁹) to the direct prime-twist sum Σ_{p≤x} χ(p) on every smoke
cell. Theory weight w_χ = L(1,χ) signed, via exp566's two paths reused verbatim:
class-number exact for fundamental D < 0, |D| ≤ 400; truncated series otherwise
(exp566-calibrated median rel err 1.8 × 10⁻⁵). Smoke x = 2²², moduli ≤ 120, with
asserts L(1,χ₋₃) = π/(3√3) and L(1,χ₅) = 2 log φ/√5 ≈ 0.4304. Inference: CP95
binomial intervals; within-modulus d-shuffle null (2000 draws, common seed 572),
which is MEANINGFUL here unlike exp566's max/χ² readouts — sign(c) is not
permutation-invariant in a; class level uses a permutation null varying sign(d)
only (the predictor is shuffle-invariant).

## Result 1 — cell level: both criteria fail decisively

| quantity | value |
|---|---|
| cells (491) agreeing | 74 |
| agreement rate | **15.07%** |
| CP95 | [0.1202, 0.1855] — wholly below 50% |
| CS obs agree-minus-disagree | −343 vs null mean 245.16 (sd 11.16) |
| circular-sum z | **−52.72** (C2 needs z > 3) |
| criterion C1 / C2 | FALSE / FALSE |

Two-sided note: the CP interval also excludes 50 from below — this is not a
near-miss but significant anti-agreement, driven by the universal negative skew
(byproduct below): since sign(w) ≡ +1, disagreement is precisely the 84.7% of
cells whose prime twist runs negative.

## Result 2 — class level: significantly BELOW chance

Over all 86,882 unit classes, sign(d_a) vs sign(Σ_χ w_χ χ(a)) agrees in 42,345
cases: rate 48.74%, CP95 [0.4841, 0.4907] — excludes 50% from below — permutation
z = −7.74. The class-level criterion remains non-degenerate (L-values enter as
weights, not signs), so this is a genuine test of whether the |deviation| profile
aligns with the L-magnitude-weighted character sum: it anti-aligns mildly but
significantly. No computable handle here either; if anything the wrong way.

## Result 3 — breakdowns: no subgroup rescues the route

All CIs wholly below 50%:

| stratum | n | agreement | CP95 |
|---|---|---|---|
| prime-modulus quadratics (ω=1) | 167 | 26.9% | [0.204, 0.343] |
| product chars (ω≥2) | 324 | 8.95% | [0.061, 0.126] |
| exact-L path | 226 | 12.8% | [0.088, 0.179] |
| truncated-L path | 265 | 17.0% | [0.127, 0.221] |
| drop \|w\|<10⁻³ robustness guard | 491 | 15.07% | unchanged |

The truncation-sign-flip guard changes nothing: no cell's verdict rests on a
borderline L-value.

## Named byproduct — the Chebyshev/Rubinstein–Sarnak skew, independently confirmed

Because sign(w) ≡ +1, the cell agreement statistic IS Pr[c_χ > 0]; its complement
is the fraction of cells where prime counts run below li(x)/φ(m) for every
non-trivial character projection: **84.7% negative (CP95 [0.8123, 0.8779])**, with
the independent smoke read at x = 2²² giving 91.7%. This is the classical
Chebyshev bias / Rubinstein–Sarnak logarithmic-law regime — prime counts twist
negative in the vast majority of residue-class projections — reproduced inside
this lab's own machinery without being sought: deviation signs are one-directional
across moduli and driven by the low zeros of the twisted L-functions, not by
L(1,χ). That is precisely why no computable L-value carries them, and why the
registered route could not have worked even in principle at this scale. Labeled
exploratory (not pre-registered); the registered readouts above are unaffected.

## Caveats

1. **Degeneracy, disclosed pre-data.** C1's reduction to Pr[c_χ > 0] was stated in
   the honest_notes BEFORE full data ran; the one-sided bar (>50%) was retained as
   registered rather than reinterpreted post-hoc. The two-sided readout is also
   reported (it excludes 50 from below).
2. **Finite-x primitive-twist artifact.** c_χ sums χ over primes coprime to m;
   the raw primitive twist adds ±1 per prime p | m, p ∤ cond(χ). Max correction
   3 at full scale; zero cells' signs would flip under the full correction
   (disclosed, not applied — the measured AP projection is the registered
   observation).
3. **Class-null exchangeability is weaker.** The class predictor
   sign(Σ_χ w_χ χ(a)) is shuffle-invariant, so its null varies sign(d) only.
4. **Toy scale.** x = 2²⁶; conclusions are about computability from N at this
   scale per program scope, not about asymptotic sign laws.

## Ledger

Three catches, none adverse after disclosure:

1. **m=6 orthogonality assert failure → structural find.** The assert exposed that
   raw primitive twists contribute ±1 per prime p | m with p ∤ cond(χ); quantified
   (max corr 3, 0 sign flips induced at full scale) and disclosed rather than
   silently corrected.
2. **Class-z scale mix-up.** The first pass compared ±1-scale observations against
   an agree-count null (z = −310, meaningless); recomputed single-scale z = −7.74.
   Caught in-ledger, corrected value used everywhere.
3. **exp566 caveat does not transfer.** exp566 recorded "within-modulus shuffle
   vacuous" for its magnitude readouts; here sign(c) is NOT permutation-invariant
   in a, so the shuffle null is meaningful — verified before use, not assumed.

## Barrier validation

Closes the barrier-map residual "MA-1 effectivity" as a named question: neither
magnitude (paper 213) nor sign (this paper) of AP deviations is captured by
computable quadratic-character data at toy scale. Stated plainly: there is no
computable criterion via quadratic-character structure on either route; the
averaging identity's effective scope remains non-computable from N at this scale.
Consistent with barriers 4 (N-symmetry cost) and 5 (residue-dial confinement) —
character data are dials, and the deviation structure lives in zero-driven
universal skew outside any dial. No barrier breached, no constant shaved, no new
method proposed.

## Conclusion

The signed route dies at both registered criteria — cell agreement 15.07%
(z = −52.72), class agreement 48.74% below chance (z = −7.74) — closing the MA-1
computable-effectivity program on both routes as an honest negative strengthening
paper 213. The experiment's lasting yield is structural: the class-number-formula
degeneracy of the registered weight, and the independent confirmation of the
universal Chebyshev/Rubinstein–Sarnak negative skew (84.7% of cells) in the lab's
own AP machinery. Now 560 experiments (max id 572). Assessment v324.

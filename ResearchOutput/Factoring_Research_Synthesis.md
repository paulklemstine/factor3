# Factoring Research Synthesis — Lean Catalog

> A comprehensive map of every factoring algorithm, identity, and research direction
> formalised in `~/lean/Catalog`.  Extracted from 13 380 `.lean` files across 20 domains.

---

## 0. Executive summary

The Catalog contains **no single end-to-end competitive factoring implementation** (no
quadratic sieve, no number field sieve, no Lenstra ECM).  What it *does* contain is a
deep, largely **novel** research programme that re-frames integer factorisation as a
collision/search problem in several unexpected geometric and algebraic spaces:

1. **Berggren-tree / Pythagorean-triple collisions** — the dominant theme.  Two distinct
   primitive triples sharing a hypotenuse `N` yield a non-trivial divisor of `N` via
   Euler's `gcd(N, ac+bd)` construction.  This is formalised, metrised in the hyperbolic
   plane, and studied as a spectrum of growth rates.
2. **Tropical arithmetic lensing** — a new bridge (min-plus algebra ↔ layered DAG
   geometry ↔ semiprime factorisation) where "caustic multiplicity products" encode
   semiprimes and a certified factor extractor is proved.
3. **Sum-of-squares / Brahmagupta–Fibonacci / Euler four-square identities** — the
   algebraic engine behind congruence-of-squares methods, formalised as the foundation
   for 50 conjectured novel algorithms.
4. **Fibonacci + Carmichael primitive-divisor theory** — entry-point divisibility,
   `gcd(F_m,F_n)=F_{gcd(m,n)}`, and certified-range Carmichael theorems.
5. **Möbius-integer factorisation theory** — oriented primes, unique factorisation up to
   orientation, and the (refuted) spectral double-cover.
6. **p-adic / tropical valuations** — smoothness ↔ tropical vanishing, Pollard-rho
   iteration, Shor's algebraic core.

The rest of this document walks through every file cluster, what it proves, and how it
connects to factorisation.

---

## 1. File inventory (factoring-relevant)

### 1.1 Core factorisation files

| File | Domain | Role |
|------|--------|------|
| `NumberTheory/Factorization.lean` | NumberTheory | Möbius-integer factorisation theory |
| `Computation/Computation/NovelFactoringAlgorithms.lean` | Computation | Foundations for 50 novel algorithms: congruence of squares, BF, tropical, Fibonacci, Shor, RSA totient |
| `Bridges/BerggrenFactoring.lean` | Bridges | Berggren matrices + Fermat + Euler factor connection |
| `Speculative/AutoResearch/BerggrenFactoring.lean` | Speculative | Duplicate / variant of the above |
| `Cryptography/Factoring/FactorQuadruples.lean` | Cryptography | Factor-pair/-quadruple structures, Fermat method, divisor lattices |
| `Cryptography/Factoring/PadicFactoring.lean` | Cryptography | p-adic factoring oracle (corrected: composite-only) |
| `Computation/Factoring/QuaternionNorm.lean` | Computation | 4-D lattice `L₄(N): x²+y²+z²≡0 (mod N)` |
| `Computation/Factoring/NewTheorems.lean` | Computation | Fibonacci doubling, two-rep identities, congruence success probability |
| `Bridges/NeuralCoding/TropicalFactoring.lean` | Bridges | Tropical factoring: valuations, Pollard rho, Shor step |
| `Bridges/TropicalGravitationalFactoringDuality.lean` | Bridges | **Tropical arithmetic lensing** — the largest new framework |
| `Algebra/Algebra/NonArchimedeanFactoringOracle.lean` | Algebra | p-adic oracle dichotomy (prime vs composite) |
| `Speculative/NumberTheory/BrahmaguptaFibonacciFactoring.lean` | Speculative | BF identity, two-square reps, Fermat two-squares |
| `Speculative/AbstractAlgebra/PisanoPeriodFactoring.lean` | Speculative | Pisano-period factoring (stub) |
| `Speculative/Physics/SieveAndPrimality.lean` | Physics | Trial division correctness, Wilson's theorem |

### 1.2 Berggren / Pythagorean / hyperbolic cluster (the main research thrust)

| File | Domain | Role |
|------|--------|------|
| `Geometry/HyperbolicBerggrenGeodesics.lean` | Geometry | Master bridge: Berggren tree ↔ hyperbolic plane ↔ Euler factorisation |
| `Geometry/HyperbolicBerggrenGeodesicsII.lean` | Geometry | Extensions |
| `Geometry/HyperbolicBerggrenDensity.lean` | Geometry | Density of nodes |
| `NumberTheory/BerggrenCollisionDistance.lean` | NumberTheory | **Collision distance = log of divisor** (the key metric result) |
| `NumberTheory/BerggrenRateSpectrum.lean` | NumberTheory | Exact growth-rate spectrum, Binet formulas, infinite spectrum |
| `NumberTheory/BerggrenStarSteps.lean` | NumberTheory | Star-arm step lengths → 0 |
| `NumberTheory/BerggrenSpineStep.lean` | NumberTheory | Pell spine step → `log(1+√2)` |
| `NumberTheory/BerggrenStarLines.lean` | NumberTheory | Star arms as hyperbolic lines |
| `NumberTheory/BerggrenBoundaryDynamics.lean` | NumberTheory | Boundary dynamics |
| `NumberTheory/BerggrenStarArithmetic.lean` | NumberTheory | Arithmetic of star arms |
| `NumberTheory/BerggrenSpectrumDense.lean` | NumberTheory | Spectrum density |
| `NumberTheory/BerggrenBoundaryLimitSet.lean` | NumberTheory | Limit sets |
| `NumberTheory/BerggrenSilverExtremal.lean` | NumberTheory | Silver-ratio extremal structure |
| `Computation/BerggrenHyperbolicGeodesics.lean` | Computation | Gram invariant Φ, collinearity, Pell conics |
| `Computation/BerggrenPellClassification.lean` | Computation | **Classification of radial lines** — Pell conics `m²-kmn-n²=1` |
| `Computation/BerggrenHorocycleGap.lean` | Computation | Horocycle gaps |
| `Computation/BerggrenLinePencil.lean` | Computation | Line pencils |
| `Computation/BerggrenRationalLines.lean` | Computation | Rational lines |
| `Computation/BerggrenGeodesicCensus.lean` | Computation | Geodesic census |
| `Computation/BerggrenSquareDiscriminant.lean` | Computation | Square discriminants |
| `Computation/BerggrenAlignmentClasses.lean` | Computation | Alignment classes |
| `Algebra/Algebra/BerggrenPellComplete.lean` | Algebra | Pell-completeness (Speculative copy also exists) |
| `Speculative/BerggrenTrees/BerggrenPellComplete.lean` | Speculative | B₂-iteration, Pell recurrences on hypotenuses |

### 1.3 Fibonacci / Carmichael cluster

| File | Domain | Role |
|------|--------|------|
| `NumberTheory/CarmichaelComputational.lean` | NumberTheory | Carmichael primitive-divisor theorem, certified `13≤n≤10000` |
| `Shared/NumberTheory/Fib_gcd_identity.lean` | Shared | `gcd(F_m,F_n)=F_{gcd(m,n)}`, primitive-divisor existence |
| `Probability/FibonacciGcdSynchronization.lean` | Probability | Fibonacci GCD synchronisation |
| `Cryptography/FibonacciGcdSynchronization.lean` | Cryptography | Same (cross-domain) |
| `NumberTheory/Primitive_Prime_Divisors…Fibonacci_Numbers.lean` | NumberTheory | Primitive prime divisors of Fibonacci numbers |

### 1.4 Supporting number-theory / algebra

| File | Domain | Role |
|------|--------|------|
| `NumberTheory/Basic.lean`, `Structure.lean` | NumberTheory | Foundational |
| `Computation/ResearchQuestions.lean` | Computation | σ-function, semiprime divisor count, E₈ factoring channels, ECM, collision identities |
| `Algebra/Algebra/QuaternionBasic.lean` | Algebra | Quaternion basics |
| `Algebra/Algebra/QuadraticFormsNumberFields.lean` | Algebra | Quadratic forms |
| `Algebra/Algebra/IdealClassGroupBridge.lean` | Algebra | Class-group bridge |
| `Algebra/Algebra/SelmerFanDisparity.lean` | Algebra | Selmer fan |
| `Algebra/Algebra/TorsionDetection.lean` | Algebra | Torsion detection |

### 1.5 Novelty / cross-domain

| File | Domain | Role |
|------|--------|------|
| `Novelty/VampireNumbers.lean` | Novelty | Vampire-number congruence `xy≡x+y (mod b-1)` |
| `Novelty/VampireCongruence.lean` | Novelty | Fang congruence theory |
| `Novelty/CrossDomainSynthesis.lean` | Novelty | Cross-domain synthesis |
| `Novelty/MirrorSlopeDetector.lean` | Novelty | Mirror symmetry slope detector (p-adic valuation) |

---

## 2. The Berggren–Pythagorean factorisation programme (deep dive)

This is the **single largest coherent research programme** in the Catalog relevant to
factorisation.  Its thesis: the Berggren tree of primitive Pythagorean triples is a
natural search space for factors, and its hyperbolic geometry controls how hard the
search is.

### 2.1 Core mechanism — Euler's two-representation method

**Theorem** (`HyperbolicBerggrenGeodesics.euler_two_representations_factor`):
two essentially distinct representations `N = a²+b² = c²+d²` produce a non-trivial
divisor `gcd(N, ac+bd)` of `N`.

**Theorem** (`berggren_collision_factors`): two distinct Berggren nodes sharing a
hypotenuse `N` factor `N`.

This is the classical Euler–Fermat–Dixon family of methods, here embedded in the
Berggren tree.

### 2.2 The hyperbolic metric

The Berggren tree is embedded in the Poincaré upper half-plane via
`z(m,n) = (n+i)/m`.  Key results:

- **Logarithmic trajectory theorem**: `|d_ℍ(i, z(m,n)) − ½ log c| ≤ log 2` where
  `c=m²+n²` is the hypotenuse.  Every node sits at distance `½ log c + O(1)` from the
  root — sub-linear in the size of the triple.
- **No-free-lunch**: the number of nodes inside a hyperbolic ball of radius `R` grows
  like `e^R` ≈ the hypotenuse itself.  A short geodesic does not make the search cheap.
- **Step trichotomy** (`BerggrenSpineStep`, `BerggrenStarSteps`):
  - Star-arm steps → 0 (parabolic arms look like lines to a boundary point).
  - Middle-spine steps → `log(1+√2)` (the silver ratio translation length).
  - This is the metric reason arms vs. spine behave differently.

### 2.3 Collision distance = log of the divisor

**Theorem** (`BerggrenCollisionDistance.collision_cosh_ge_gcd`):
for a collision with divisor `g = gcd(N, m₁m₂+n₁n₂)`,
`cosh d(z₁,z₂) ≥ 1 + g/2`.

**Theorems** `collision_cosh_two_sided`, `collision_dist_ge_log_divisor`,
`collision_dist_ge_half_log_of_large_divisor`:
`d(z₁,z₂) ≥ log g − log 2`, and if `g` is the larger factor (`N ≤ g²`) then
`d(z₁,z₂) ≥ ½ log N − log 2` — the colliding pair is essentially *antipodal* in its
annulus, so a local hyperbolic search around one node cannot reach the other.

**Interpretation for algorithm design.**  A collision that yields a *large* divisor
forces the two witnesses far apart in the hyperbolic metric — which is exactly the
regime where the divisor is most useful (balanced factorisation) but hardest to find
by local search.  The pivot deficit `N − P` (not `g` itself) is the true control
parameter.

### 2.4 Growth-rate spectrum

`BerggrenRateSpectrum.lean` computes **exact** hyperbolic growth rates along periodic
Berggren paths via Binet formulas:

| Path | Rate |
|------|------|
| `(B₂B₃)^∞` | `½ log(2+√5) = 0.72181…` |
| `(B₂B₂B₃B₃)^∞` | `¼ log(7+4√3) = ½ log(2+√3) = 0.65848…` |
| `(B₂B₃^b)^∞` | `log ρ_b/(b+1)`, `ρ_b=(1+b)+√((1+b)²+1)` |

The spectrum is **infinite** and accumulates at both `0` and `log(1+√2)`.  This is a
complete picture of the metric "speed limit" of every periodic Berggren trajectory.

### 2.5 Radial lines and Pell conics

`BerggrenPellClassification.lean` classifies the exact straight lines through the
centre of the half-plane:

- **Radial invariant** `ϱ(m,n) = (m²−n²−1)/(mn)`: two seeds are aligned with the base
  point iff their `ϱ` agree.
- Level sets of `ϱ` are the Pell-like conics `m² − ϱ·mn − n² = 1`.
- **Quantisation of distance**: the distance from `i` to any conic node is an exact
  integer multiple of `2 log λ_k`, `λ_k` the k-th metallic ratio.
- The orbit is an isometric copy of `ℕ`: `d(P_i,P_j) = |i−j|·2 log λ_k`.

So the "straight lines" of the picture are arithmetic progressions in disguise — a
very structured search space.

---

## 3. Tropical arithmetic lensing (the newest framework)

`Bridges/TropicalGravitationalFactoringDuality.lean` (≈ 550 lines, the largest single
factoring file) builds a brand-new bridge:

**Min-plus algebra** ↔ **layered weighted DAG geometry** ↔ **semiprime factorisation**.

### 3.1 Definitions

- **Tropical semiring** on `ℕ`: `min` is addition, `+` is multiplication.
- **Tropical lens network**: a layered DAG Source → {lenses} → Observer, each lens with
  inbound/outbound costs and a geodesic multiplicity.
- **Caustic set**: lenses achieving the minimum arrival cost (the "images").
- **Encoded product**: `∏ pathMult` over the caustic set.
- **EncodesSemiprime N**: encoded product = `N`, ≥ 2 caustic strata, each multiplicity ≥ 2.

### 3.2 Main theorems

| Theorem | Meaning |
|---------|---------|
| `finite_tropical_lens_realization` | Every multiplicity spec is realizable as a reduced network |
| `reduced_causticMult_eq_sum` | For reduced networks, caustic multiplicity = sum over lenses |
| `symmetry_gap_yields_factor` | **A semiprime-encoding network has a non-trivial factor pair** |
| `certified_minimal_factor_reconstructor` | Certified decision procedure: extract a factor **or** certify the encoding is trivial |
| `pythagorean_shell_to_lens` | Balanced Pythagorean shells produce lens networks encoding their product |
| `tropical_factoring_pipeline` | End-to-end: composite `N=m₁m₂` → network → factor pair |

### 3.3 Why it matters

This is a **certified geometric alternative to trial division**: either the tropical
lens structure reveals factors, or it certifies that the encoding lacks the geometric
degeneracy needed for extraction.  It is the only framework in the Catalog that
produces a *certified decision procedure* for factorisation rather than just an
identity.

---

## 4. Algebraic identities (the engine room)

`NovelFactoringAlgorithms.lean` formalises the identities behind the 50 conjectured
novel algorithms:

| Identity | Name | Factoring use |
|----------|------|---------------|
| `x²−y² = (x−y)(x+y)` | Difference of squares | Fermat, Dixon, QS, NFS |
| `a^(2r)−1 = (a^r−1)(a^r+1)` | Shor's core | Quantum period-finding |
| `(a²+b²)(c²+d²) = (ac∓bd)²+(ad±bc)²` | Brahmagupta–Fibonacci | Two-square factorisation |
| 8-square identity | Euler–Degen–Cayley (quaternion norm) | Higher-dim congruence of squares |
| `v_p(ab)=v_p(a)+v_p(b)` | Tropical additivity | Smoothness ↔ tropical vanishing |
| `(p+q)²−4pq = (p−q)²` | Discriminant | Factor recovery from sum+product |
| `σ(pq) = (1+p)(1+q)` | Divisor-sum decomposition | RSA totient structure |

The **congruence-of-squares** success probability is formalised as `2/4 = 1/2`.

---

## 5. Fibonacci + Carmichael theory

### 5.1 Fibonacci GCD identity

`gcd(F_m, F_n) = F_{gcd(m,n)}` — the fundamental synchronisation lemma, used to
relate entry points of primes dividing Fibonacci numbers.

### 5.2 Carmichael primitive-divisor theorem (certified)

`NumberTheory/CarmichaelComputational.lean` proves, for composite `n` in the certified
range `13 ≤ n ≤ 10000`, that `F(n)` has a **primitive prime divisor** — a prime `p|F(n)`
that does not divide any earlier `F(k)`.  The proof uses:

- Entry-point divisibility: `α(p) | n` whenever `p | F(n)`.
- The "primitive part" `F*(n) = F(n) / gcd(F(n), lcm{F(d): d|n, d<n}) > 1`.

This is the number-theoretic backbone of **Fibonacci-based factoring** (the idea that
`gcd(F(n), N)` or `gcd(F(k), N)` can reveal a factor of `N`).

---

## 6. Möbius-integer factorisation theory

`NumberTheory/Factorization.lean` builds a parallel factorisation theory for the
**Möbius integers** `Z̃` (a double cover of `ℤ`):

- **Class number one**: `Z̃` is a PID.
- **Oriented primes double-cover the rational primes**: each rational prime `p` has
  exactly two prime elements `p⁺, p⁻` of norm `p`.
- **Unique factorisation up to orientation**: any two prime factorisations agree up to
  permutation and sign.
- **Refutation of the spectral double cover**: `p⁺` and `p⁻` generate the *same* prime
  ideal, so `Spec Z̃ ≅ Spec ℤ` is a single cover.  The doubling lives on elements, not
  on points.
- **Refutation of non-Ore-ness**: `Z̃` is commutative, so the Ore condition holds.

This is a *theoretical* laboratory for how factorisation behaves when you adjoin an
orientation double cover — relevant to spectral/RH-motivated factoring approaches.

---

## 7. p-adic / tropical valuation methods

`TropicalFactoring.lean` and `NonArchimedeanFactoringOracle.lean`:

- **Tropical factoring** = a pair `(a,b)` with `ab=n`, i.e. `v_p(a)+v_p(b)=v_p(n)` for all `p`.
- **Smoothness ↔ tropical vanishing**: `n` is `B`-smooth iff all valuations at primes `>B` are 0.
- **Pollard-rho iteration** `x ↦ x²+1 (mod n)` formalised; birthday bound `O(√p)`.
- **Shor factoring step**: from `a²≡1 (mod n)`, `gcd(a±1,n)` yields a factor.
- **p-adic oracle dichotomy**: every `n>1` is either prime or has a non-trivial factor
  (the original "oracle" claiming this for *all* `n>1` is **disproved** — primes are the
  counterexample).

---

## 8. Factor quadruples and Fermat method

`Cryptography/Factoring/FactorQuadruples.lean`:

- **Factor quadruple**: two factor pairs `(a,b),(c,d)` with `ab=cd=n`.
- `gcd(a,c) | n` — the algebraic core of quadruple-based factoring.
- **Cross-ratio coprimality**: `a/gcd(a,c)` and `c/gcd(a,c)` are coprime.
- **Fermat factoring** from difference of squares, with the symmetry
  `(x−y) ≤ √n ≤ (x+y)`.
- **Smooth numbers have many divisors**: `k` distinct prime factors ⇒ at least `2^k`
  divisors ⇒ more potential quadruples.

---

## 9. Higher-dimensional / lattice methods

- `Computation/Factoring/QuaternionNorm.lean`: the lattice
  `L₄(N) = {(x,y,z) : x²+y²+z² ≡ 0 (mod N)}`.  A short vector in this lattice can
  reveal factors of `N` — the 4-square analogue of Fermat's 2-square method.
- `Computation/ResearchQuestions.lean`: E₈ lattice factoring channels — `C(8,2)=28`
  cross terms from one 8-square representation, each a candidate for GCD extraction;
  ECM parallelism (28 candidate curves); Hasse bound; CM Hecke eigenvalues.

---

## 10. What is **not** in the Catalog

For honest scoping, these well-known algorithms are **absent** (not formalised):

- Quadratic sieve (QS) / multiple-polynomial QS
- General number field sieve (GNFS)
- Lenstra elliptic-curve factorisation (ECM) — only the curve non-singularity and
  parallelism *lemmas* appear, not the algorithm
- Dixon's random squares
- Pollard `p−1` / `p+1`
- Williams `p+1`
- Shor's algorithm (only the algebraic *identity*, not the quantum circuit)
- CFRAC, Lehman's method, Fermat (only the identity, not the loop)

The Catalog's contribution is **not** re-formalising these; it is the novel
Berggren/tropical/Fibonacci frameworks above.

---

## 11. How this feeds a new factoring algorithm

The strongest leads, ranked by novelty and formalisation depth:

1. **Berggren-collision search.**  Enumerate primitive triples by hyperbolic ball
   (logarithmic in the hypotenuse); a collision on a shared hypotenuse `N` yields a
   factor.  The metric theory tells you exactly how far apart balanced-collision
   witnesses sit (antipodal), so you know the search radius needed.
2. **Tropical lens reconstruction.**  The certified `certified_minimal_factor_reconstructor`
   is already a decision procedure; the open work is an *efficient* realisation of the
   network from `N`.
3. **Fibonacci/Carmichael GCD.**  `gcd(F(k), N)` for well-chosen `k` (entry points)
   is a classical idea; the certified Carmichael theorem gives a guaranteed primitive
   divisor in a known range.
4. **Higher-dimensional congruences of squares.**  The 8-square identity gives 28
   independent cross-terms per representation pair — a much denser source of GCD
   candidates than the 2-square method.

The Catalog gives you the **identities, the metric control, and the certified
decision procedures**.  What it does not yet give you is the outer loop (sieving,
smoothness detection, lattice reduction) that would make any of these competitive
with QS/GNFS on large integers.  That is the gap a new algorithm would close.

---

## 12. Cross-domain map

```
Geometry   HyperbolicBerggrenGeodesics ─────────────────────────────────────┐
NumberTheory  BerggrenCollisionDistance, RateSpectrum, SpineStep, StarSteps │
Computation   BerggrenHyperbolicGeodesics, PellClassification, Factoring/*  ├── Berggren
Algebra       BerggrenPellComplete                                       │   programme
Speculative   BerggrenTrees/BerggrenPellComplete                         │
                                                                           │
Bridges       TropicalGravitationalFactoringDuality ────────────────────────┘
Bridges       TropicalFactoring ────────── Tropical / p-adic
Algebra       NonArchimedeanFactoringOracle ──┘
                                                           │
Computation   NovelFactoringAlgorithms ────────┐            │
Cryptography  FactorQuadruples, PadicFactoring  ├─ Algebraic │
Novelty       VampireNumbers                   │   engine   │
Shared        Fib_gcd_identity ─────────────────┘            │
NumberTheory  CarmichaelComputational ──── Fibonacci/Carmichael
NumberTheory  Factorization ───────────── Möbius theory
Computation   ResearchQuestions ────────── E₈ / ECM / σ lemmas
```

---

*Document generated 2026-08-10 from a sweep of 13 380 `.lean` files in `~/lean/Catalog`.*

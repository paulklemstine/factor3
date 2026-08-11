# Experiment: Information Geometry Factoring (Fisher / KL / Cramér-Rao)

**Date:** 2026-08-10
**Paradigm:** Information geometry — Fisher information metric, Kullback–Leibler
divergence, Cramér–Rao bound, Fisher–Rao length.
**Verdict:** **REFUTED** — the rationality of the Fisher form does not escape the
polynomial/free-witness barriers. A clean structural theorem explains exactly why.
**Confidence:** High (theorem-level, verified computationally).

---

## 1. Background: the structures under test

The Lean catalog (`Computation/InformationGeometry/` and
`Bridges/InformationGeometry/`) develops the finite information-geometric apparatus:

| Quantity | Definition | Key property |
|---|---|---|
| Fisher form | `fisherForm p v w = ∑_i v_i w_i / p_i` | Rational in `p`; Hessian of KL on the diagonal (`klDiv_hessian_diagonal`) |
| KL divergence | `klDiv p q = ∑_i p_i log(p_i/q_i)` | `0 ≤ KL ≤ χ²` (the divergence sandwich) |
| χ² divergence | `chiSquared p q = ∑_i (p_i−q_i)²/q_i = fisherForm q (p−q)(p−q)` | Equals Fisher displacement |
| Fisher–Rao length | `∫ √(fisherForm γ γ)` | Dominates `L¹` distance between endpoints |
| Pinsker | `½‖p−q‖₁² ≤ KL(p‖q)` | Connects `L¹` to relative entropy |

The **motivating claim** (from the lab memory): `fisherForm p v w = ∑ v_i w_i / p_i`
is a *rational* function of the probability vector `p`, not a polynomial in `N`.
Since the polynomial barrier (theorem LLL) says polynomial invariants in `N` reveal
only finitely many primes, the hope was that a *rational* function of a distribution
derived from `N` could reveal a factor.

---

## 2. The experimental question

> Can we construct a probability distribution `p_N` on a **small** finite set (size
> `poly(log N)`), **computable from `N = pq` alone** (not from `p,q`), such that an
> information-geometric quantity `Q(N)` — Fisher form, KL divergence, χ², or
> Fisher–Rao length — satisfies `gcd(integer_from(Q(N)), N) ∈ (1, N)`?

The small-support + computable-from-`N`-alone constraints are essential: without them
one could trivially build a distribution that encodes the factors (Hypothesis 8, the
"cheating" sanity check).

---

## 3. The structural theorem (main result)

**Theorem (Fisher-form gcd factorization).** Let `p_i = c_i / N` for positive
integers `c_i` with `∑ c_i = N` (the natural normalization: `c_i` are counts over a
partition of `{0,…,N−1}`). Let `v` be any tangent vector (`∑ v_i = 0`). Define
`S = ∑_i v_i² / c_i`, write `S = A/B` in lowest terms. Then:

1. `fisherForm(p)(v,v) = N · S`  (the factor `N` is *always* present).
2. `gcd( numerator(F), N ) = N / gcd(N, B)`.
3. Since `B | lcm(c_i)`, a **nontrivial** factor is revealed iff
   `gcd(lcm(c_i), N) ∈ (1, N)`, i.e. iff some `c_i` is divisible by exactly one of
   `{p, q}`.

*Proof sketch.* `fisherForm(p)(v,v) = ∑ v_i²/p_i = ∑ v_i² · (N/c_i) = N·∑v_i²/c_i = N·S`.
Writing `F = N·A/B` with `gcd(A,B)=1`, the reduced numerator is `N·A/gcd(N·A,B)`.
Since `gcd(A,B)=1`, `gcd(N·A,B) = gcd(N,B)`, so reduced numerator =
`N·A/gcd(N,B)`, and `gcd(N·A/gcd(N,B), N) = N/gcd(N,B)` because
`gcd(A/gcd(N,B), N/gcd(N,B)) | gcd(A, N/gcd(N,B)) = 1`. ∎

**Consequence.** The Fisher form does *not* bypass the factoring problem — it
*translates* it into a question about the `lcm` of the counts `c_i`:

- **If all `c_i < min(p,q)`** (the generic case for any distribution built from
  `N` without knowing its factors), then `lcm(c_i)` is coprime to `N`, so
  `gcd(F.num, N) = N` — the **trivial(N)** regime. The Fisher form gives back `N`
  itself, no factor. *This is what happens in Hypothesis 1 (residue mod d) and
  Hypothesis 7 (random tangent vectors): every trial returns `gcd = N`.*
- **If some `c_i` is a multiple of `p` but not `q`** (or vice versa), then the
  Fisher form reveals that factor. But constructing such a `c_i` from `N` alone is
  *exactly* the factoring problem — it is the **free-witness / trial-division**
  condition. You must already "see" a multiple of the factor in your counts.

This is the core reason the rational escape fails: **computable-from-`N` distributions
have counts `c_i` that are simple functions of `N` (polynomials, floors, character
sums over `poly(log N)` terms), and simple functions of `N` produce `lcm(c_i)` coprime
to `N` unless they encode a factor — which is circular.**

---

## 4. Hypotheses tested and results

All experiments run on semiprimes from 20-bit to 48-bit (scaling confirmed to
60-bit in additional runs). `gcd` is always `gcd(numerator(F), N)` for the Fisher
form `F` (exact rational arithmetic via Python `fractions.Fraction`).

### H1 — Residue-mod-d distribution  →  TRIVIAL(N)
`p_r = #{a < N : a ≡ r (d)} / N`. Counts `c_r = ⌈N/d⌉` or `⌊N/d⌋`, all `< min(p,q)`
for small `d`. Result: `gcd(F.num, N) = N` for all `d ∈ {6,12,30,210,2310}` and all
semiprimes. **Reduces to: gives N itself.** Confirmed by the theorem: `lcm(c_i)` is
coprime to `N` when `d < min(p,q)`.

### H2 — Jacobi-symbol distribution  →  TRIVIAL(1)
`p_± = fraction of a ∈ [1,M] with (a|N) = ±1`, for `M = poly(log N)`. The counts sum
to `M` (independent of `N`), so `F = M·S` and `gcd(F.num, N) = 1` for all `M, N`.
**The numerator depends only on `M`, not on the factorization.** No factor signal.

### H3 — Power-residue distribution  →  TRIVIAL(1)
`p_r = fraction of k ∈ [0,K) with g^k ≡ r (mod m)`, small `g, m, K`. Counts sum to
`K = poly(log N)`. Result: `gcd = 1` always. **Order-finding structure is not
accessible** from `N` alone without `Ω(√N)` work (Pollard-rho / Shor territory).

### H4 — gcd(a,N) bucket distribution  →  TRIAL DIVISION
`p_g = fraction of a ∈ [1,M]` with `gcd(a,N) = g`. For `M < min(p,q)` the only
bucket is `g=1`; factors appear as buckets only when `M ≥ min(p,q)`, i.e. when you
have enumerated up to the smaller factor. **This is trial division with `O(M)` cost.**
The Fisher form itself still gives `gcd = 1`; the factor signal is in the *support*
of the distribution, not in the IG quantity.

### H5 — Quadratic-residue distribution  →  TRIVIAL(1)
`p_r = fraction of a ∈ [1,M]` with `a² mod N ≡ r (mod m)`. CRT structure mod `p`, mod
`q` is not accessible from `N` alone. Result: `gcd = 1`.

### H6 — Exponent-residue (Pollard p-1 analog)  →  TRIVIAL(1)
`p_r = fraction of k ∈ [0,K)` with `a^k mod N ≡ r (mod m)`. Same as H3: order-finding
barrier. Result: `gcd = 1`.

### H7 — Tangent-vector sensitivity  →  TRIVIAL(N)
For the residue-mod-d distribution, 50 random tangent vectors `v` were tried.
**Every single one gave `gcd = N`.** The `N`-in-numerator phenomenon is independent
of the tangent direction (it follows from `∑ c_i = N`, not from `v`).

### H8 — "Cheating" sanity check (uses known factors)  →  TRIVIAL(1)
When the distribution is *allowed* to depend on `p,q` (residue mod `min(p,q)`), the
Fisher form gives `gcd = 1`, not the factor. **This is because the counts are then
*exactly equal** (`c_i = N/min(p,q)` for all `i`), so the distribution is *uniform*,
and the Fisher form of a uniform distribution is `F = m·∑v_i²`, independent of the
factor. The factor is encoded in the *support size* `m = min(p,q)`, not in the
Fisher value. This confirms: even when the factor is "present" in the distribution,
the Fisher form does not surface it as a gcd.

### H9 — Scaling: Jacobi distribution up to √N  →  TRIVIAL(1)
`M` scaled from `poly(log N)` up to `√N ≈ 2^{15}`. Result: `gcd = 1` throughout,
even at `M = √N`. The free-witness aggregation barrier: the Jacobi character sum
over `[1,M]` is `O(√N log N)` (Pólya–Vinogradov), so no signal emerges until
`M = Ω(√N)`, and even then the Fisher numerator is `M²`-like, coprime to `N`.

### H10 — Direct rational-function test  →  TRIVIAL(1)
For rational functions `R(N) = f(N)/g(N)` with `f,g ∈ ℤ[x]`,
`gcd(num(R(N)), N) = 1` for all tested `N`. This is the **rational barrier**:
`p | f(N) ⇔ p | f(0)`, so a rational function of `N` reveals only the finitely many
prime divisors of `f(0)·g(0)` — the same fixed-prime limitation as polynomials.
**The Fisher form, when the distribution is a simple function of `N`, is a rational
function of `N` and inherits this barrier.**

### H11 — N-in-numerator structural analysis  →  THEOREM VERIFIED
Directly confirmed `F = N·S` and `gcd(F.num,N) = N/gcd(N, den(S))` across many
random partitions. The `N` factor is structurally unavoidable for count-normalized
distributions.

### H12 — Bit-pattern distribution  →  TRIVIAL(1)
Distribution of bit-counts at each position in `[0,N−1]`. Result: `gcd = 1`. The bit
structure of `N` does not encode its factors in a Fisher-extractable way.

### H13 — Continued-fraction (CFRAC) distribution  →  KNOWN METHOD
Partial quotients of `√N` *do* encode factors (this is the classical CFRAC method),
but the Fisher form of the quotient distribution gives `gcd = 1`. **Information
geometry adds nothing to CFRAC**; the factor signal is in the convergent denominators
themselves, not in any IG scalar computed from the quotient distribution.

### H14 — Fermat-witness distribution `(a^N mod N)`  →  TRIVIAL(1)
Result: `gcd = 1`. The Fermat witness structure is not captured by the Fisher form.

### H15 — Multiplicative order  →  ORDER-FINDING BARRIER
`ord_N(a)` for small `a` exceeds `poly(log N)`; finding it requires `Ω(√N)` work
(Pollard-rho) or a quantum computer (Shor). **This is the one genuine computational
barrier, but it is not new.**

### H16 — KL and χ² as factor detectors  →  TRIVIAL(1)
For the residue-mod-d distribution, `χ²(p, uniform)` has numerator whose gcd with `N`
is always 1. KL is transcendental (involves `log`), so it has no numerator to take a
gcd with — it cannot yield a factor by construction. **KL and χ² are even worse than
the Fisher form for this purpose**, because they are not rational in `N`.

### H17 — "Rational escape" with `p_i ∝ 1/(N+i)`  →  TRIVIAL(1)
A distribution whose probabilities are rational functions of `N` with `N` in the
denominator. Result: `gcd = 1`. The numerator of `F` is a huge integer (100+ digits)
but coprime to `N`. **This directly refutes the "rational escape" claim**: a rational
function of `N` has a numerator whose prime factors are fixed (depending only on the
coefficients of the rational function), not the variable factors of `N`.

---

## 5. Why the rational escape fails — three perspectives

### 5.1 The algebraic perspective (rational barrier = polynomial barrier)
For `R(N) = f(N)/g(N)` with `f,g ∈ ℤ[x]`, and a prime `p | N`:
`p | f(N) ⇔ p | f(0)` (since `N ≡ 0 mod p`). So `R(N)` can reveal only primes
dividing `f(0)·g(0)` — **finitely many fixed primes**, independent of which `N` you
chose. The Fisher form of any distribution whose counts are polynomial/rational
functions of `N` is itself a rational function of `N`, so it inherits this barrier.
The "rationality" does not help: it is the *dependence on `N` as the variable* that
is limited, not the polynomial-vs-rational distinction.

### 5.2 The counting perspective (the theorem)
For the natural count-normalized distribution `p_i = c_i/N`, the Fisher form is
`N·S`, so its gcd with `N` is `N/gcd(N, den(S))`. A nontrivial factor requires
`den(S)` to be divisible by exactly one of `{p,q}`, which requires some count `c_i`
to be a multiple of exactly one factor. **Constructing such a count from `N` alone
is the factoring problem.** The Fisher form is a *faithful translation*, not a
bypass.

### 5.3 The information perspective (what the IG quantities actually measure)
- **Fisher form** `∑ v_i²/p_i`: measures the *sensitivity* of the distribution to
  the tangent direction `v`, weighted by inverse probability. For computable
  distributions this sensitivity is a simple function of `N`.
- **KL divergence**: a *measure of distinguishability*. `KL(p_N || uniform)` is
  small (≈ `log N / d` for residue-mod-d) and transcendental — it has no integer
  numerator to extract a factor from.
- **χ²**: the Fisher displacement; same rational barrier as the Fisher form.
- **Cramér–Rao / Pinsker**: these are *inequalities* (lower/upper bounds on
  variance / `L¹` distance). They constrain how well a parameter can be estimated;
  they do not produce a number from which a factor can be gcd-extracted.

None of these quantities, evaluated on a distribution computable from `N` alone,
produce a factor-dependent integer. The information they carry about the factors is
either (a) absent (the distribution doesn't depend on the factors), (b) present but
inaccessible without `Ω(√N)` enumeration (free-witness aggregation), or (c) present
but encoded in a transcendental/real number with no extractable integer structure.

---

## 6. Honest assessment

### What is genuinely new here
- The **structural theorem** (§3) is a clean, provable characterization of exactly
  when the Fisher form of a count-normalized distribution reveals a factor. It shows
  the Fisher form is *equivalent* to a question about `lcm(c_i)`, not a bypass.
- The **rational barrier** (§5.1) extends the polynomial barrier (LLL) to rational
  functions: rational functions of `N` reveal only finitely many fixed primes. This
  closes the "rational escape" loophole rigorously.
- The demonstration that **KL and χ² are worse than the Fisher form** for factoring
  (transcendental, no numerator) is a useful negative result.

### What reduces to known barriers
- H1, H7 → trivial(N) by the theorem (N-in-numerator).
- H2, H3, H5, H6, H12, H14 → trivial(1): numerator depends only on small parameters.
- H4 → trial division.
- H9 → free-witness aggregation (`Ω(√N)`).
- H10, H17 → rational barrier (= polynomial barrier for rational functions).
- H13 → CFRAC (known subexponential method); IG adds nothing.
- H15 → order-finding (Shor / Pollard-rho); the one genuine computational barrier.
- H16 → KL/χ² are not rational, so cannot yield factors by gcd.

### What does NOT work and why (summary)
The Fisher form's rationality in `p` is real, but `p` must be built from `N`. Building
`p` from `N` alone forces the counts `c_i` to be simple (polynomial/rational/character-sum)
functions of `N`. Such counts have `lcm(c_i)` coprime to `N` (unless they encode a
factor, which is circular), so the Fisher form gives `gcd = N` (trivial). If instead
the counts are bounded by `poly(log N)` and independent of `N`, the Fisher form gives
`gcd = 1` (trivial). **There is no middle ground** that yields a nontrivial factor
without already solving the factoring problem.

### Bottom line
Information geometry does not provide a new classical factoring method. The Fisher
form is a *faithful translator* of the factoring problem into a question about the
`lcm` of distribution counts, not a solver. The rationality of the Fisher form does
not escape the polynomial barrier because computable distributions make it a rational
*function of N*, and rational functions of `N` are subject to the same fixed-prime
limitation as polynomials.

---

## 7. Recommendation

- **Do not pursue** information geometry as a factoring paradigm. The negative
  result is theorem-level, not empirical.
- The structural theorem (§3) is worth formalizing in Lean as a permanent negative
  result in the catalog (a "Fisher form does not factor" theorem), analogous to the
  polynomial barrier theorem already in the library.
- The rational barrier (§5.1) should be added to the lab's barrier classification as
  theorem extension: "the polynomial barrier extends to rational functions of N."
- Remaining fresh leads with higher promise: **Langlands / idèle class group**
  (deepest number-theoretic structure; the idèle class group *does* encode all primes),
  **Ising model** (transcendental partition functions — genuinely non-rational), and
  **dyadic solenoid / ×2 dynamics** (harmonic analysis tied to period-finding).

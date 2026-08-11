# Factoring Brainstorm: Unconventional Mathematical Territories

> Goal: discover a factoring technique in a **better complexity class** than any existing
> algorithm.  Best classical = GNFS at `L_N[1/3, 1.923]`.  Quantum (Shor) = `poly(log N)`.
> We want a *classical* path to `L_N[1/4]` or better, ideally `poly(log N)`, by importing
> mathematics that has never been used for factoring.

The Catalog already gives us: Berggren/Pythagorean collisions, tropical lensing, BF/Euler
identities, Fibonacci/Carmichael theory, Möbius integers, p-adic oracles.  Below are
**genuinely new** directions, each from a field with no established factoring connection.

---

## 0. The complexity barrier, restated

Every classical factoring algorithm is a **witness search**: find a special object whose
existence is *guaranteed* by N's compositeness, and which reveals a factor.

| Algorithm | Witness | Density | Complexity |
|-----------|---------|---------|------------|
| Trial division | small factor p | N^{-1/2} | exp |
| Pollard rho | collision mod p | N^{-1/4} | exp |
| ECM | smooth p±1 | sub-exp in p | L_p[1/2] |
| QS | smooth x² mod N | sub-exp | L_N[1/2] |
| GNFS | algebraic + rational relation | sub-exp | L_N[1/3] |

To beat GNFS we need a witness of density ≥ `L_N[-1/4]` — i.e. one that appears much more
often than a smooth number.  The question becomes: **what structure is more abundant than
smooth numbers but still encodes a factor?**

---

## 1. SINGULAR MODULI + AGM FACTORING  ★ strongest candidate

**Mathematical source.** Complex multiplication, the arithmetic-geometric mean, Hilbert
class polynomials.  Never used for factoring (the CM *method* builds curves; it does not
factor).

### 1.1 The key object

For a fundamental discriminant `-D < 0`, the **Hilbert class polynomial**
`H_D(x) ∈ ℤ[x]` has the singular moduli `j(τ_i)` as roots, where `τ_i` runs over the
`h(-D)` ideal classes of `K = ℚ(√-D)`.  Degree `h(-D) ~ √D` (class number formula).

**Crucial fact.** For a prime `p ∤ D`:
```
H_D(x)  mod p  has a root   ⇔   p splits completely in the Hilbert class field of K
                              ⇔   the Frobenius at p is trivial in Gal(H/K)
```
By Chebotarev, the density of such primes is `1/h(-D) ~ 1/√D`.

### 1.2 The protocol

```
Input: N = pq (RSA semiprime, unknown factors).

For each fundamental discriminant D = O(log² N), increasing:
  1. Compute the h(-D) singular moduli j(τ_i) to O(log N) bits of precision,
     via the AGM iteration (quadratic convergence).
  2. Reconstruct H_D(x) mod N from the approximate roots using LLL lattice reduction
     (recognise integer coefficients from floating-point approximations).
  3. Pick random j₀ ∈ ℤ/Nℤ.  Compute g = gcd(H_D(j₀), N).
  4. If 1 < g < N, output g as a factor.
```

### 1.3 Why it could be polynomial-time

- **AGM step.** Computing one singular modulus to `b` bits costs `O(M(b) log b)` where
  `M(b)` is multiplication cost.  With `b = O(log N)`, this is `poly(log N)`.  There are
  `h(-D) = O(√D) = O(log N)` such moduli.  Total: `poly(log N)`.
- **LLL reconstruction.** The coefficients of H_D have `O(√D log D)` bits before reduction.
  Working mod N we only need `O(log N)` bits.  LLL on a `h(-D)-dimensional` lattice with
  `O(log N)`-bit entries costs `poly(log N)`.
- **Success probability per D.** We need H_D to have a root mod exactly *one* of {p, q}.
  Probability ≈ `2 · (1/√D)(1 - 1/√D) ~ 2/√D = O(1/log N)`.
- **Total.** `O(log N)` discriminants × `poly(log N)` work = **`poly(log N)` total.**

### 1.4 Why this is new

This is **not** ECM.  ECM relies on the *smoothness* of a random group order — a
probabilistic number-theoretic coincidence.  The singular-moduli method relies on the
*algebraic* splitting behaviour of p in a class field — a deterministic, structural
property.  It packages all `h(-D)` CM elliptic curves of discriminant D into a single
polynomial and reads off a factor from the splitting of that polynomial mod N.

**References.** Enge (2009) "The complexity of class polynomial computation via floating
points"; Bröker (2009) "Constructing supersingular elliptic curves."

### 1.5 Open risk

The Chebotarev density gives the *average* splitting probability, but we need it to hold
for the *specific* primes p, q dividing N.  This is unconditional for each fixed D, but
the `O(1/log N)` bound needs to be shown to hold uniformly across the `O(log² N)`
discriminants we try.  Plausible (effective Chebotarev, Lagarias-Odlyzko), but not proved
here.

---

## 2. SUM-PRODUCT / ADDITIVE-COMBINATORICS FACTORING  ★

**Mathematical source.** The sum-product theorem (Bourgain-Katz-Tao 2004, Elekes,
Rudnev-Stevens).  Never used for factoring.

### 2.1 The key theorem

For a finite set A inside a field, `max(|A+A|, |A·A|) ≥ |A|^{1+ε}` unless A is close to a
subfield.  Over `ℤ/Nℤ` (Bourgain 2005, Glibichuk-Rudnev 2018): if `|A| < N^{1-δ}` and both
sumset and product set are small, then A is concentrated on a **coset of a subring**.

**The subrings of ℤ/Nℤ correspond exactly to the divisors of N.**  For N = pq, the
nontrivial subrings are `pℤ/Nℤ` and `qℤ/Nℤ`.

### 2.2 The protocol

```
Input: N composite.

Find a set A ⊆ ℤ/Nℤ with |A| = poly(log N) and max(|A+A|, |A·A|) ≤ |A|^{1+ε}.
→ By the structure theorem, A is close to a subring pℤ/Nℤ or qℤ/Nℤ.
→ The subring reveals a factor.
```

### 2.3 How to find A — three approaches

**(a) SDP relaxation.** Maximise |A| subject to `|A+A| ≤ K`, `|A·A| ≤ K`.  Relax the
indicator vector `1_A` to a positive semidefinite matrix.  Solve the SDP in `poly(log N)`.
Round.  (The rounding step is the risky part.)

**(b) Sparse Fourier recovery.** The Fourier transform of `1_{pℤ/Nℤ}` is
`1_{qℤ/Nℤ}` (the orthogonal subgroup).  So we seek a set whose Fourier transform is
concentrated on a small subgroup.  This is the **sparse Fourier transform** problem —
solved in `O(k log N)` by Hassanieh-Indyk-Katabi-Price (2012).  For RSA (balanced
factors) the subgroup has size √N, so `k = √N` and this is still exponential.  **But for
lopsided N** (one small factor p), the subgroup has size p, and the algorithm runs in
`O(p log N)` — subexponential when p is subexponential.

**(c) Greedy descent.** Start with A = {1}.  Repeatedly add the element x minimising
the growth of `(A∪{x})+(A∪{x})` and `(A∪{x})·(A∪{x})`.  If growth stalls, we've found a
structured set → a factor.

### 2.4 Complexity verdict

- For **lopsided** N: potentially `L_N[1/2]` or better (beats trial division, competes
  with ECM).
- For **balanced** RSA N: the sparse-FT approach gives `O(√N)` — no better than rho.
  The SDP approach is the one to watch; if the rounding works, it could be polynomial.

---

## 3. ARITHMETIC TOPOLOGY / 3-MANIFOLD INVARIANTS  ★ long-shot, high novelty

**Mathematical source.** Arithmetic topology (Kapranov, Morishita, Reznikov): the analogy
between Spec ℤ and 3-manifolds, primes and knots, Legendre symbols and linking numbers.

### 3.1 The analogy (made precise)

| Number theory | 3-manifold topology |
|---------------|---------------------|
| Spec ℤ | closed oriented 3-manifold M |
| prime p | knot K_p ⊂ M |
| ℤ/pℤ | H₁ of knot complement |
| p-adic ℚ_p | universal cover of complement |
| Legendre symbol (a/p) | linking number |
| quadratic reciprocity | Milnor triple linking |
| Iwasawa theory | Alexander polynomial |
| ζ_ℤ(s) | Reidemeister torsion |

### 3.2 The protocol

```
Input: N.

1. Construct a 3-manifold M(N) from N — e.g. the n-fold cyclic branched cover of S³
   branched over a knot K, with n and K derived from N.
2. Compute a topological invariant of M(N): the Alexander polynomial Δ_M(t), the
   Jones polynomial V_M(t), the Chern-Simons invariant, or the hyperbolic volume Vol(M).
3. The invariant factors according to the JSJ decomposition of M(N), which corresponds
   to the prime factorisation of N.
```

### 3.3 Concrete construction

Let K be the figure-eight knot (the simplest hyperbolic knot).  Let M_n be the n-fold
cyclic branched cover of S³ branched over K.  Then (Fox, Milnor):
```
|H₁(M_n; ℤ)| = ∏_{j=1}^{n-1} Δ_K(ζ_n^j)
```
where Δ_K is the Alexander polynomial of K.  For the figure-eight knot,
`Δ_K(t) = -t + 3 - t^{-1}`, so `Δ_K(ζ_n^j) = -2 cos(2πj/n) + 3`.

**The order |H₁(M_n)| is an integer whose prime factors are constrained by n.**  If we
set n = N, then `|H₁(M_N)|` is a huge integer, and its factorisation is related to the
factorisation of N.  But computing `|H₁(M_N)|` requires knowing the product above, which
requires knowing N's factorisation to evaluate... circular as stated.

### 3.4 The non-circular version

Instead of computing the integer `|H₁(M_N)|`, compute it **mod N** (or mod a small
multiple).  The product `∏ Δ_K(ζ_N^j)` can be evaluated in the cyclotomic ring
`ℤ[ζ_N]` without expanding.  The result, reduced mod N, is an algebraic integer whose
norm reveals... this needs more thought.  The open question: **can the homology of M_N be
computed mod N in subexponential time without knowing N's factors?**

### 3.5 Why it's worth pursuing

If 3-manifold invariants can be computed mod N efficiently, then the JSJ decomposition
of M(N) — which corresponds to the prime factorisation — is readable from those
invariants.  The complexity would be governed by the complexity of computing the
invariant, not by any smoothness or sieving condition.  The Alexander polynomial of a
branched cover can be computed via the Burau representation in `poly(log N)` time.  **This
could be polynomial.**

---

## 4. p-ADIC DYNAMICS / p-ADIC MANDELBROT

**Mathematical source.** Dynamics over p-adic fields (Berkovich projective line, Rumely,
Silverman).  The p-adic Mandelbrot set.  Never used for factoring.

### 4.1 The key observation

The dynamics of `f_c(z) = z² + c` over ℚ_p depends critically on p:
- The **filled Julia set** K_c is connected iff `|c|_p ≤ 1` (c in the p-adic Mandelbrot set).
- The **Berkovich Julia set** has a tree structure whose branching depends on the
  reduction of c mod p.
- The **periodic points** of f_c mod p have periods dividing p^k - 1 for some k.

### 4.2 The protocol

```
Input: N.

1. Choose a parameter c (e.g. c = -2, the "chestnut").
2. Iterate z ↦ z² + c mod N (this is the Pollard rho iteration!).
3. But instead of Floyd's cycle detection, monitor the *p-adic valuation* of the
   iterates: track v_p(z_n) for the unknown p | N.
4. The valuation dynamics reveal p: the sequence v_p(z_n) stabilises at the valuation
   of the periodic point mod p, which is determined by p.
```

### 4.3 Why this differs from Pollard rho

Pollard rho finds a collision `z_i ≡ z_j (mod p)` and computes `gcd(z_i - z_j, N)`.  The
p-adic version tracks the *valuation* — the highest power of p dividing each iterate.
The valuation sequence is a **p-adic integer** that encodes p in its limit.  The question
is whether we can read off p from the valuation sequence *without* already knowing p.

**Open question.** Can the p-adic valuation of the orbit of z² + c mod N be computed
mod N (i.e. without knowing p) in subexponential time?  If yes, the limit of the
valuation sequence reveals p.

### 4.4 Connection to the Catalog

The Catalog's `TropicalFactoring.lean` already defines `pollardRhoStep` and the birthday
bound.  The p-adic valuation is the "tropical norm" `tropicalNorm p n = padicValNat p n`.
This idea extends the tropical factoring programme from the *real* tropical semiring to
the *p-adic* tropical (Berkovich) setting.

---

## 5. RANDOM MATRIX THEORY / GUE HYPOTHESIS

**Mathematical source.** Montgomery-Odlyzko law, Keating-Snaith conjectures, random matrix
theory.  The pair correlation of zeta zeros matches GUE eigenvalues.

### 5.1 The key insight

The **spectral statistics** of certain random matrices encode the primes.  Specifically,
the characteristic polynomial `P_M(θ) = det(I - e^{-iθ} M)` of a random unitary matrix M
∈ U(n) has zeros whose statistics match the zeta zeros (as n → ∞).

### 5.2 The protocol (highly speculative)

```
Input: N.

1. Construct a unitary matrix U(N) whose eigenvalues are e^{2πi p/N} for primes p ≤ B
   (some bound), padded to dimension n = π(B).
2. Compute the characteristic polynomial P(θ) = det(I - e^{-iθ} U(N)).
3. The zeros of P(θ) are at θ = 2π p / N.  The *gaps* between zeros are 2π(p_{i+1}-p_i)/N.
4. The gap distribution reveals the factorisation of N: if N = pq, the zeros mod 2π/N
   have a structure reflecting the CRT decomposition ℤ/Nℤ ≅ ℤ/pℤ × ℤ/qℤ.
```

### 5.3 Why it might beat GNFS

The connection is **spectral**, not combinatorial.  The complexity is governed by the cost
of computing the characteristic polynomial of an n×n unitary matrix, which is `O(n^ω)`
(matrix multiplication).  If we can take `n = poly(log N)` (i.e. only need the first
`poly(log N)` primes), this is polynomial.

### 5.4 The catch

Constructing U(N) requires knowing the primes p ≤ B, which we can sieve.  But the zeros
of P(θ) are at `2π p / N`, and to resolve individual primes we need precision `O(1/N)`,
which requires `O(log N)` bits — feasible.  The real question is whether the CRT
structure of ℤ/Nℤ is readable from the *spectral statistics* (gap distribution) without
already knowing the factors.  This is the open problem.

---

## 6. NONCOMMUTATIVE GEOMETRY / SPECTRAL TRIPLES

**Mathematical source.** Connes' approach to the Riemann hypothesis via spectral triples
(A, H, D).  Never used for factoring.

### 6.1 The key object

A **spectral triple** (A, H, D): A is an algebra of operators on a Hilbert space H, D is
a Dirac operator.  The spectrum of D encodes arithmetic information.  For the "adele class
space" (Connes' construction), the zeros of ζ(s) appear as an absorption spectrum.

### 6.2 The protocol

```
Input: N.

1. Construct the spectral triple (A_N, H_N, D_N) for the ring ℤ/Nℤ:
   - A_N = ℤ/Nℤ acting on H_N = L²(ℤ/Nℤ) (the group algebra ℂ[ℤ/Nℤ]).
   - D_N = the Dirac operator on the Cayley graph of (ℤ/Nℤ)* with generators being
     small primes.
2. Compute the spectrum of D_N.
3. The spectrum decomposes according to the CRT: spec(D_N) = spec(D_p) ⊔ spec(D_q).
4. The decomposition reveals p and q.
```

### 6.3 Why it could be efficient

The Dirac operator on a finite graph is a finite matrix.  Its spectrum can be computed in
`O(N^ω)` — but N is huge.  However, we only need the spectrum **mod N**, and the matrix
is `φ(N) × φ(N)`.  The open question: can the spectrum of D_N be computed *without*
diagonalising the full matrix, using the algebraic structure (CRT decomposition)?

**Key insight.** The spectrum of D_N is the union of the spectra of D_p and D_q (by CRT).
If we could compute the spectrum of D_N and then **factor the spectrum** (as a multiset)
into two subsets, we'd have factored N.  This is the **turnpike problem** / **subset
reconstruction** — NP-hard in general, but the spectral structure may make it easier.

---

## 7. HOMOTOPY TYPE THEORY / UNIVALENCE

**Mathematical source.** The foundations of Lean itself.  HoTT, higher inductive types,
the univalence axiom.  Never used for factoring.

### 7.1 The key idea

In HoTT, the **loop space** of a type encodes its symmetry.  The type `Fin N` (the
standard finite type with N elements) has loop space `Ω(Fin N) = Aut(Fin N) = S_N`
(the symmetric group).  The **Eilenberg-MacLane space** `K(ℤ/Nℤ, 1)` has
`π₁ = ℤ/Nℤ`, `π_k = 0` for k > 1.

### 7.2 The protocol (very speculative)

```
Input: N.

1. Construct the higher inductive type X_N representing the "factorisation space" of N:
   - Points are pairs (a, b) with a·b = N.
   - Paths between (a,b) and (c,d) are witnesses of equality.
2. Compute the homotopy group π₁(X_N).
3. The structure of π₁(X_N) encodes the factorisation of N.
```

### 7.3 Why it's interesting

The **univalence axiom** says equivalent types are equal.  If we can construct a type
whose equivalence class depends on the factorisation of N, then univalence gives a path
(a witness of equality) that encodes the factor.  The complexity is governed by the
**normalisation of HoTT terms** — which is TOWER-hard in general (the decidability of
equality in HoTT is non-elementary).  So this is unlikely to beat GNFS, but it reframes
factoring as a *geometric* problem in a space where new tools (spectral sequences,
Postnikov towers) apply.

---

## 8. TROPICAL LENS RECONSTRUCTION (extend the Catalog)

**Mathematical source.** The Catalog's own `TropicalGravitationalFactoringDuality.lean`.

### 8.1 The open problem

The Catalog proves `certified_minimal_factor_reconstructor`: a decision procedure that
either extracts a factor pair or certifies the encoding is trivial.  **But it does not
give an efficient algorithm to *construct* the lens network from N.**

### 8.2 The challenge

Given N, construct a tropical lens network L with `encodedProduct = N`.  The Catalog's
`two_lens_semiprime` does this for a *known* factorisation `N = m₁·m₂`.  The hard case:
construct L **without knowing the factors**.

### 8.3 A new approach via tropical moduli

The **tropical moduli space** M_g^{trop} parametrises tropical curves of genus g.  The
**tropical Jacobian** of a tropical curve is a real torus.  Could we encode N as the
"volume" of a tropical Jacobian and read off factors from the torus structure?  The
volume of the tropical Jacobian of a metric graph Γ is `det(L_Γ)` where `L_Γ` is the
Laplacian.  For a graph constructed from N, `det(L_Γ)` might factor according to N's
factorisation.

---

## 9. MATROID THEORY / TUTTE POLYNOMIAL

**Mathematical source.** Matroid theory, the Tutte polynomial.  Never used for factoring.

### 9.1 The key object

The **divisor lattice** of N (divisors ordered by divisibility) is a geometric lattice,
hence a matroid.  Its **Möbius function** is the classical Möbius function μ.  Its
**characteristic polynomial** is `χ_{L_N}(t) = ∑_{x∈L_N} μ(0̂, x) t^{rank(L_N)-rank(x)}`.

### 9.2 The protocol

```
Input: N.

1. Construct the divisor lattice L_N (without knowing the factors — this is the hard
   part; we can construct it from the multiplication table of ℤ/Nℤ).
2. Compute the Tutte polynomial T_{L_N}(x, y).
3. The Tutte polynomial of a geometric lattice factors according to the direct product
   decomposition: T_{L_{pq}} = T_{L_p} · T_{L_q} (for coprime p, q).
4. Factor the Tutte polynomial → factor N.
```

### 9.3 Complexity

Computing the Tutte polynomial is #P-hard in general.  But for the *specific* matroid
coming from the divisor lattice of N, the structure is special (it's a product of
chains).  The open question: can `T_{L_N}` be computed in `poly(log N)` time using the
ring structure of ℤ/Nℤ?  If yes, factoring it (a polynomial in two variables) is
polynomial.

---

## 10. ANALYTIC COMBINATORIES / DIRICHLET SERIES

**Mathematical source.** Flajolet-Sedgewick analytic combinatorics, singularity analysis.
Never used for factoring.

### 10.1 The key object

The **Dirichlet generating function** of the divisor function d(n) is `ζ(s)²`.  The
average order of d(n) is log n, but the **fluctuations** encode the factorisation.

### 10.2 The protocol

```
Input: N.

1. Compute the Dirichlet series F(s) = ∑_{n≤X} d(n) n^{-s} for X = poly(log N).
2. The Mellin transform of F(s) relates to ζ(s)².
3. The **singularities** of F(s) are at the zeros of ζ(s) and at s = 1.
4. The **residue** at s = 1 is related to the number of divisors of N.
5. Extract the factorisation from the residue structure.
```

### 10.3 Why it's unlikely to beat GNFS

This is essentially the **explicit formula** approach (Weil, Connes).  The explicit
formula relates primes to zeta zeros, but computing zeta zeros to precision O(1/N)
requires O(√N) terms — exponential.  Not competitive.

---

## Ranking and recommendations

| # | Idea | Novelty | Feasibility | Potential complexity |
|---|------|---------|-------------|----------------------|
| 1 | Singular moduli + AGM | ★★★★★ | ★★★★ | **poly(log N)** |
| 2 | Sum-product / additive combinatorics | ★★★★★ | ★★★ | poly(log N) to L[1/2] |
| 3 | Arithmetic topology / 3-manifold invariants | ★★★★★ | ★★ | poly(log N) (if homology mod N is efficient) |
| 4 | p-adic dynamics / Mandelbrot | ★★★★ | ★★★ | sub-exponential |
| 5 | Random matrix theory / GUE | ★★★★ | ★★ | poly(log N) (if spectral stats readable) |
| 6 | Noncommutative geometry / spectral triples | ★★★★★ | ★★ | poly(log N) (if spectrum factorable) |
| 7 | HoTT / univalence | ★★★★★ | ★ | TOWER (too slow) |
| 8 | Tropical lens reconstruction | ★★★ (in Catalog) | ★★★★ | poly(log N) (if network constructible) |
| 9 | Matroid / Tutte polynomial | ★★★★ | ★★ | poly(log N) (if Tutte computable) |
| 10 | Analytic combinatorics / Dirichlet | ★★★ | ★ | exponential |

### Recommended research programme

1. **Immediate:** pursue Idea 1 (singular moduli + AGM).  It has the clearest path to
   polynomial time, the strongest number-theoretic foundation, and the most concrete
   protocol.  The main risk (Chebotarev uniformity) is a standard analytic-number-theory
   problem with known tools.

2. **Parallel:** pursue Idea 2 (sum-product) via the SDP relaxation route.  The
   connection between small sumset/product set growth and subring structure is a genuine
   theorem; the algorithmic question (can we *find* such a set efficiently?) is open and
   worth attacking with convex optimisation tools.

3. **Long-shot:** pursue Idea 3 (arithmetic topology).  The analogy between primes and
   knots is deep and largely unexploited algorithmically.  If the homology of the
   branched cover M_N can be computed mod N efficiently, the factorisation is readable
   from the JSJ decomposition.

---

*Brainstorm v1 — 2026-08-10.  This is iteration 1 of a recurring exploration.  Each
subsequent iteration should deepen the most promising leads and prune the dead ends.*

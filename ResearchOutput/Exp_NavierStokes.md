# Experiment NS — Navier–Stokes / Turbulence for Factoring

> **Paradigm:** Fluid dynamics, Navier–Stokes equations, spectral energy transfer,
> Galerkin truncation, epsilon-regularity
> **Date:** 2026-08-11
> **Verdict:** **REFUTED** — all six hypotheses. A new, clean instance of the
> **structural orthogonality** barrier, compounded with circularity and
> free-witness aggregation, expressed via spectral PDE theory.
> **Confidence:** High (analytic mechanism identified + computational verification)

---

## 1. Source Material

Lean formalizations read:

- `Physics/NavierStokes/EnergyMethod.lean` — Abstract Galerkin NS model
  `u'(t) = −νAu − B(u,u)` on a real inner-product space. The load-bearing
  structural fact is the **trilinear cancellation** `⟨B(u,u), u⟩ = 0`, which makes
  the nonlinearity energy-preserving and yields the **energy dissipation identity**
  `E'(t) = −2ν⟨Au, u⟩ ≤ 0`. Energy is a Lyapunov function; no blowup in the
  energy norm. The Galerkin truncation projects onto a finite mode space of
  dimension M, giving a finite-dimensional ODE.
- `Physics/NavierStokes/ModeTransfer.lean` — Global nonlinear energy conservation
  forces exact exchange between any mode band and its complement:
  `transferInto(N,u, all∖low) = −transferInto(N,u, low)`. This is a bookkeeping
  identity: gain in one band is balanced by loss in the complement. It holds for
  *any* energy-conserving nonlinearity and *any* state.
- `Physics/NavierStokes/PartialRegularity.lean` — Abstract ε-regularity. The
  **singular set** (points not regularAt) is contained in the **concentration
  set** (points where scale-invariant excess ≥ ε at *every* positive scale). If
  the concentration set is null, the singular set is null.
- `Physics/ArithmeticPhotons/PhotonParity.lean` — Pythagorean-triple parity
  facts (catalog artifact; not directly relevant to the fluid-dynamics connection).

---

## 2. The Core Object

The natural way to force a connection between Navier–Stokes and factoring
`N = pq` is to **index the Galerkin mode space by residues mod N**. The mode
index set is `ℤ/Nℤ` (or `(ℤ/Nℤ)²` for a 2D vorticity model). A state is a field
`u = (u_i)_{i mod N}`. The structures then available are:

| NS structure | Mathematical content | Natural coordinates |
|--------------|---------------------|---------------------|
| Energy spectrum `E(k) = |û_k|²` | additive Fourier transform on `ℤ/Nℤ` | wavenumber `k` (additive) |
| Dissipation rate `ε = ν∑k²E(k)` | 2nd spectral moment | wavenumber magnitude |
| Mode transfer | bookkeeping identity | band vs complement (additive) |
| Galerkin ODE attractor | finite ODE on mode space | mode amplitudes |
| Singular set (ε-regularity) | scale-invariant excess concentration | scale `r` |

The decisive observation is in the rightmost column: **every natural coordinate
of turbulence is additive/Fourier** — a function of the *additive* group
structure of `ℤ/Nℤ`. Factoring `N = pq`, by contrast, is a statement about the
*multiplicative* structure: the CRT decomposition `ℤ/Nℤ ≅ ℤ/pℤ × ℤ/qℤ`, the
orders of elements in `(ℤ/Nℤ)*`, the subgroup lattice. This is the structural
orthogonality at the heart of the refutation.

---

## 3. Hypotheses

### H1 — Energy spectrum encodes a factor
Index modes by `ℤ/Nℤ`, initialize `u_i = f(i; N)` with `f` computable from `N`
alone (no factor knowledge). Compute the energy spectrum `E(k) = |û_k|²` and its
moments (centroid, dissipation proxy, enstrophy, spectral entropy). Does any
spectral feature reveal a factor via `gcd(feature, N)`?

### H2 — Galerkin ODE attractor / energy-landscape structure encodes a factor
Evolve the truncated NS system `u' = −νAu − B(u,u)` with N-derived initial
data. Does the attractor, or the "strange energy landscape with many local
minima" of turbulence, concentrate energy at factor-related modes?

### H3 — Dissipation rate or mode-transfer spectrum encodes a factor
Does the instantaneous dissipation rate `ε(t) = ν⟨Au,u⟩`, or the spectral
energy-transfer rate into a band, carry factor information?

### H4 — Singular-set measure (ε-regularity) encodes a factor
Construct a field from N, define scale-invariant excess, and ask whether the
singular set (excess ≥ ε at all scales) is concentrated at factor-related
scales.

### H5 — The cascade direction / inertial range encodes a factor
Does the direction or rate of the energy cascade (large → small scales) depend
on the factors?

### H6 — A "mode system weighted by N" evades the polynomial barrier
The polynomial barrier says polynomial invariants in N reveal ≤ finitely many
primes. The NS energy spectrum is exponential/Fourier in the mode index. Does
this transcendental structure evade the barrier?

---

## 4. Mathematical Analysis

### 4.1 The fundamental mismatch (structural orthogonality)

The energy spectrum is the squared magnitude of the **additive Fourier
transform** on `ℤ/Nℤ`:

```
û_k = Σ_{i mod N} u_i · e^{−2πi k i / N}.
```

The basis functions `e^{2πi k i / N}` are the **characters of the additive
group** `(ℤ/Nℤ, +)`. The factors `p, q` enter only through the **multiplicative**
CRT decomposition `ℤ/Nℤ ≅ ℤ/pℤ × ℤ/qℤ`. Additive characters do not "see" the CRT
decomposition unless you already know it: the factorization

```
e^{2πi k i / N} = e^{2πi k_p i_p / p} · e^{2πi k_q i_q / q}
```

requires writing `k ↔ (k_p, k_q)` and `i ↔ (i_p, i_q)` via CRT, which requires
knowing `p, q`. **The natural basis of turbulence (additive Fourier modes) is
orthogonal to the natural basis of factoring (CRT / multiplicative characters).**

This is the same pattern as the Berggren tree (Exp. YY/ZZ: slope vs norm) and
the dyadic solenoid (Exp. AAA: 2-adic valuation vs multiplicative order), now
expressed in the language of spectral PDEs.

### 4.2 Where the factors DO hide: as periods

The factors are not absent from the additive world — they appear as **periods**.
If one could construct a *separable* (product) field

```
u_{a,b} = α_a · β_b      (a mod p, b mod q, indexed via CRT)
```

then the 2D energy spectrum factors exactly:

```
E[k1,k2] = |D̂FT(α)[k1]|² · |D̂FT(β)[k2]|²,
```

a function on `ℤ/pℤ × ℤ/qℤ` that is `p`-periodic in `k1` and `q`-periodic in
`k2`. The periods `p, q` are then readable (in principle) from the spectrum.
**This is the only mechanism by which additive invariants can encode the
factors.** But it faces two absolute barriers:

1. **Circularity (constructing the data).** Building `u_{a,b} = α_a β_b`
   requires the CRT decomposition of `ℤ/Nℤ`, which requires knowing `p, q`.
   Without the oracle, the product structure cannot be assembled.

2. **Free-witness aggregation (reading the period).** Even given the spectrum
   as a black box on `ℤ/Nℤ`, finding the period of a function on `ℤ/Nℤ` is the
   **period-finding problem**. Classically this needs `Θ(√N)` time
   (baby-step-giant-step) or `Θ(N)` by brute force. This is exactly the
   classical bottleneck of Shor's algorithm and the free-witness aggregation
   barrier (Exp. C, S4).

### 4.3 The energy landscape is not "strange" in the relevant sense

Hypothesis H2 invokes "turbulence's strange energy landscape with many local
minima." This is a physical misreading. The NS energy

```
E(u) = ‖u‖² = Σ_i |u_i|²
```

is a **strictly convex paraboloid** (Hessian `2I`). It has exactly **one**
global minimum at `u = 0`. The nonlinearity `B` does not create local minima of
`E` — it conserves `E` (trilinear cancellation) and merely redistributes it
among modes. The "strange landscape" of turbulence refers to the *dynamics* on
the inertial manifold (transient chaos, sensitive dependence), not to local
minima of the energy functional. **There are no local minima to encode
factors.**

### 4.4 The mode transfer identity is a tautology

`transferInto(N,u, all∖low) = −transferInto(N,u, low)` holds for *any*
energy-conserving `B` and *any* state `u`. It is pure bookkeeping (the Lean
proof is a one-liner: `Finset.sum_sdiff_eq_sub`). It carries no N-specific
information unless the mode weights are themselves N-dependent — which requires
the factors (circularity again).

### 4.5 Polynomial-initialized fields hit the polynomial barrier

If `u_i = P(i)` for a polynomial `P` of degree `d`, then every spectral moment
`∑ k^m E(k)` is a polynomial in `N` (of degree `2d + m + 1`). For example,
`u_i = i²` gives dissipation proxy `D(N) ∼ N⁵`. By the polynomial barrier
(LLL), a polynomial in `N` reveals at most finitely many primes. The sporadic
gcds observed computationally (e.g. `D(15)` divisible by 3, `D(143)` divisible
by 13) are exactly the finitely-many-prime phenomenon — no general method.

### 4.6 Exponential fields reduce to period-finding

If `u_i = a^i mod N`, the DFT peaks at frequency `∼ 1/ord_N(a)`. Reading
`ord_N(a)` from the spectrum is the period-finding problem — Shor's classical
bottleneck, and the basis of Pollard p−1 when `ord_N(a) | p−1`. This is
known-method-in-disguise (barrier 7), not a new approach.

---

## 5. Computational Verification

All code: `~/factor3/ns_factoring.py`. Six experiment groups.

### E1 — Energy spectrum of factor-independent fields

Tested 9 field generators (linear, quadratic, cubic, sin, cos, `2^i mod N`,
`3^i mod N`, `i² mod N`, white noise) × 7 spectral features × all semiprimes
`N ≤ 2000` = **20,111 gcd tests**. To distinguish genuine signal from the
multiple-testing artifact, each test was paired with a **random baseline**
(random integer of comparable magnitude vs N).

| | Nontrivial gcds | Rate |
|---|---|---|
| Actual spectral features | 1384 | 6.88% |
| Random baseline | 1902 | 9.46% |
| **Signal / random ratio** | | **0.73** |

**The structured spectral features hit LESS often than random integers.**
A ratio below 1.0 is definitive: there is no positive signal. The "hits" are
the pure multiple-testing artifact (testing thousands of features against
numbers with small factors). **H1 REFUTED.**

### E2 — The CRT / period oracle test (substantive)

With **oracle factors** (`N = 143 = 11·13`), built separable data
`u_{a,b} = α_a β_b` via CRT.

- 2D spectrum factors exactly: `E[k1,k2] = |D̂FT(α)[k1]|²·|D̂FT(β)[k2]|²`,
  max error **3.18×10⁻²⁹** (machine precision). Confirmed.
- Lifted to 1D on `ℤ/Nℤ`, the autocorrelation peak lag = **11 = p**,
  `gcd(11, 143) = 11` → **factor revealed.**

This confirms the mechanism: **the factors ARE present as periods of the
additive spectrum — but only for data that requires the factors to construct.**
Without the oracle, the product structure cannot be assembled (circularity).
And even given the spectrum, the fundamental period on `ℤ/Nℤ` is `N` (trivial);
extracting the nontrivial period `p` from samples is the period-finding problem
(`Θ(√N)` classically — free-witness aggregation). **H1/H6 mechanism confirmed
but blocked by circularity + free-witness. H6 REFUTED (the transcendental
Fourier structure does not evade the barrier; it reduces to period-finding).**

### E3 — Galerkin NS toy simulation (2D vorticity)

Evolved the 2D vorticity Galerkin system (80 modes, `ν = 0.01`) with
factor-independent initial data (random-seed-from-N and
`sin(2πk₁/N)`-derived). 6720 gcd tests on the energy/dissipation time series.

- Nontrivial gcds: **73 / 6720 = 1.09%** — pure multiple-testing artifact.
- Energy is a **monotone Lyapunov function** (dissipation identity
  `E' = −2ν⟨Au,u⟩ ≤ 0`). It decays to equilibrium and cannot develop
  factor-encoding structure from factor-independent initial conditions.

**H2, H3, H5 REFUTED.**

### E4 — Structural tests

- **(a) Energy convexity:** `E(u) = ‖u‖²` has Hessian `2I`, exactly one minimum
  at `u = 0`. No local minima exist to encode factors. The "strange landscape"
  of turbulence is a property of the dynamics, not of energy minima.
- **(b) Mode transfer identity:** Verified numerically —
  `∑_i ⟨N_i, u_i⟩ = −2.87×10⁻¹⁴ ≈ 0`;
  `transferInto(complement) = −transferInto(band)` holds exactly. It is a
  bookkeeping tautology carrying no N-specific information.
- **(c) Singular set (ε-regularity):** For a single Fourier mode on
  `ℤ/143ℤ`, the scale-invariant excess is concentrated at ONE scale and zero
  at others. The singular set (excess ≥ ε at ALL scales) is **EMPTY** for
  smooth fields. To get a nonempty singular set concentrated at scale `p`, you
  must build the field using `p` (circularity).

**H4 REFUTED.**

### E5 — Polynomial barrier for spectral invariants

For `u_i = i²`, the dissipation proxy `D(N) = ∑ k² E(k)` grows as `N⁵`:

| N | D(N) | gcd(D,N) |
|---|------|----------|
| 15 | 7.99×10⁷ | 3 |
| 21 | 1.29×10⁹ | 1 |
| 35 | 8.41×10¹⁰ | 1 |
| 77 | 5.02×10¹³ | 1 |
| 143 | 7.37×10¹⁵ | 13 |
| 323 | 5.13×10¹⁸ | 1 |
| 899 | 1.88×10²² | 1 |

The sporadic gcds (N=15→3, N=143→13) are the polynomial barrier: a degree-5
polynomial in N reveals at most finitely many primes. **Polynomial barrier
confirmed. H1 (polynomial variant) REFUTED.**

### E6 — Exponential fields reduce to period-finding

`u_i = 2^i mod 323`. `ord_323(2) = 72`. The DFT peak is at `k = 9`, encoding
`1/ord_N(2)`. Reading `ord_N(2)` from the spectrum is the period-finding
problem — classically `Θ(√N)` (baby-step-giant-step). This is Shor's classical
bottleneck and the free-witness aggregation barrier. **Known-method-in-disguise
(barrier 7). H6 REFUTED.**

---

## 6. Barrier Classification

| Barrier | Status |
|---------|--------|
| Polynomial barrier (LLL) | **Applies** to polynomial-initialized fields (E5): spectral moments are polynomials in N, revealing ≤ finitely many primes. |
| Symmetry barrier (MMM) | Not the primary obstruction (the energy spectrum is symmetric in p,q, but the deeper issue is orthogonality). |
| Free-witness aggregation | **Applies** (E2c, E6): the factors appear as periods of additive invariants; reading a period on `ℤ/Nℤ` classically needs `Θ(√N)`. |
| **Structural orthogonality** | **PRIMARY** (§4.1): turbulence's natural coordinates (energy spectrum over additive wavenumbers, dissipation rate, cascade) are additive/Fourier; factoring's natural coordinates (CRT decomposition, multiplicative order) are multiplicative. The two are orthogonal. |
| Computational circularity (TTT) | **Applies** (E2b, E4c): constructing the data that exposes the periods (separable product fields, factor-concentrated singular sets) requires knowing the factors. |
| Rational escape illusory (WWW) | The Fourier/exponential structure is "transcendental" in form but computable and reduces to period-finding — the escape is illusory. |
| Known-method-in-disguise (ZZZ) | **Applies** (E6): exponential fields reduce to period-finding = Shor/Pollard p−1. |

---

## 7. Honest Verdict

> **The Navier–Stokes structures do NOT offer a new classical factoring approach.**

The obstruction is clean, structural, and threefold:

1. **Structural orthogonality (primary).** The natural observables of
   turbulence — energy spectrum `E(k)`, dissipation rate `ε`, mode transfer,
   cascade — are additive/Fourier invariants on the mode index set. Factoring
   `N = pq` is encoded in the multiplicative/CRT structure. Additive characters
   `e^{2πiki/N}` do not "see" the CRT decomposition `ℤ/Nℤ ≅ ℤ/pℤ × ℤ/qℤ`
   without knowing `p, q`. This is the same structural orthogonality that
   defeated the Berggren tree (slope vs norm) and the dyadic solenoid (2-adic
   valuation vs multiplicative order), now expressed in the language of
   spectral PDEs.

2. **Circularity.** The only mechanism by which additive invariants can encode
   the factors is as **periods** of a separable product field
   `u_{a,b} = α_a β_b`. Constructing this field requires the CRT decomposition,
   which requires knowing `p, q`. The factors are "visible" only to an observer
   who already has them.

3. **Free-witness aggregation.** Even given the spectrum as a black box, the
   factors appear as periods of a function on `ℤ/Nℤ`. Extracting a period
   classically needs `Θ(√N)` time — the same exponential barrier that defines
   the factoring problem. This is Shor's classical bottleneck.

Additionally:
- The "strange energy landscape with many local minima" hypothesis is a
  physical misreading: `E(u) = ‖u‖²` is a convex paraboloid with a single
  minimum; the nonlinearity conserves (not minimizes) energy.
- The mode transfer identity is a bookkeeping tautology carrying no N-specific
  information.
- Polynomial-initialized fields hit the polynomial barrier; exponential fields
  reduce to period-finding (known-method-in-disguise).

**Net assessment:** Navier–Stokes provides a beautiful and rigorous setting
that *sharpens the portrait* of the structural orthogonality barrier — it
shows that the barrier is not special to number-theoretic objects but governs
any attempt to read multiplicative structure through additive/Fourier
observables, even sophisticated ones drawn from PDE theory. It does *not*
overcome the barrier.

This is experiment **NS** in the factoring lab (paradigm: fluid dynamics /
Navier–Stokes / turbulence).

---

## 8. Comparison with Known Methods

| Method | Structure | Natural coordinates | Exploits |
|--------|-----------|---------------------|----------|
| Additive Fourier on `ℤ/Nℤ` | energy spectrum `E(k)` | wavenumber `k` (additive) | — (orthogonal to factoring) |
| CRT / multiplicative characters | period-finding | multiplicative order | `ord_N(a)` → factor (Shor) |
| Separable product field `α_a β_b` | factored spectrum | CRT components | periods `p,q` (needs oracle) |
| **NS turbulence (this work)** | **spectrum, dissipation, cascade** | **additive wavenumbers** | **none — orthogonal** |

The NS observables sit in the first row: additive, orthogonal to factoring.
The factoring-relevant structures (rows 2–3) require multiplicative/CRT
coordinates that the NS framework does not naturally provide.

---

## 9. Could a Variant Work?

The analysis in §4.1 is general: **any** observable that is a function of the
additive Fourier transform on `ℤ/Nℤ` is orthogonal to the CRT decomposition.
To escape, a variant would need one of:

1. **A nonlinearity whose natural modes are multiplicative characters** (not
   additive Fourier modes). This would be a genuinely different PDE — not the
   Navier–Stokes equations, whose nonlinearity `(u·∇)u` is local in physical
   space and diagonalizes in the additive Fourier basis. Whether such a "multiplicative
   PDE" exists and is well-posed is an open question, but it would no longer be
   Navier–Stokes.

2. **A way to read the CRT decomposition of the additive DFT without knowing
   the factors.** This is precisely the period-finding problem, for which no
   classical poly(log N) algorithm is known (and whose hardness underpins
   factoring-based cryptography). A classical escape here would be a breakthrough
   independent of the fluid-dynamics framing.

3. **Forcing the Galerkin system with an N-dependent body force** designed to
   resonate at factor-related frequencies. But designing such a force requires
   knowing the target frequencies, which requires knowing the factors
   (circularity).

None of these variants is realized by the Navier–Stokes structures as
formalized. The honest expectation, consistent with all 90 experiments in the
lab, is that no classical construction within this paradigm beats the barrier.

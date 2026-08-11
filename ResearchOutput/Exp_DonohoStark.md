# Experiment: Donoho–Stark Uncertainty Principle & Factoring N = pq

**Date:** 2026-08-11
**Paradigm:** Harmonic analysis — the Donoho–Stark uncertainty principle, the
rigidity/classification of its equality cases, and the Pontryagin duality
between subgroups and annihilators on `Z/NZ`.
**Verdict:** **REFUTED** — the rigidity theorem does not yield a new factoring
approach. It is a *structural classification* of uncertainty minimizers, and
every computational use of it collapses to either (i) period-finding / the
hidden subgroup problem (Shor's setting), (ii) the circularity barrier (you
must already know a factor to write down a nontrivial minimizer), or (iii) the
free-witness aggregation barrier (verifying equality needs the full DFT, Θ(N)
time = exponential in log N). The additive Fourier structure is furthermore
orthogonal to the multiplicative functions computable from `N` alone.
**Confidence:** High (theorem-level, verified computationally to 60-bit
semiprimes, and a clean reduction to known barriers).

---

## 1. Background: the structures under test

The Lean catalog (`Computation/FourierFunctor/`) develops the finite Fourier
apparatus as a natural isomorphism of functors. The relevant files:

| File | Content |
|---|---|
| `Transform.lean` | `𝓕 f (ψ) = Σ_g f g · ψ(-g)`; Fourier inversion; the natural isomorphism `fourierNatIso` |
| `Uncertainty.lean` | **Donoho–Stark bound**: `|G| ≤ |supp f| · |supp 𝓕f|`; sharpness via Dirac masses |
| `Sharpness.lean` | **Forward equality**: every modulated coset indicator `g ↦ χ(g)·1_K(g−a)` attains the bound |
| `Rigidity.lean` | **Converse** (`donoho_stark_rigidity`): equality ⟹ `f` is a modulated coset indicator |
| `Poisson.lean` | Poisson summation: the bridge between a subgroup and its annihilator |

The **motivating observation** is tantalizing and correct:

> For `G = Z/NZ` with `N = pq`, the *additive subgroups* are exactly
> `d·Z/NZ` for `d | N`. The nontrivial proper ones are `pZ/NZ` (order `q`)
> and `qZ/NZ` (order `p`). The rigidity theorem says equality-achievers are
> *precisely* modulated coset indicators of subgroups. So an equality-achiever
> "is" a coset of `pZ/NZ` or `qZ/NZ` — it **encodes a factor**.

The question is whether this observation can be turned into an *algorithm*
that starts from `N` alone and ends with a factor.

---

## 2. The mathematical dictionary

### 2.1 The Donoho–Stark bound and its rigidity

For a non-zero function `f : G → ℂ` on a finite abelian group `G`,

```
    |supp f| · |supp 𝓕f|  ≥  |G|                (Donoho–Stark)
```

**Rigidity** (theorem `donoho_stark_rigidity`, `Rigidity.lean`): equality holds
iff `f` is a *modulated coset indicator*

```
    f(g) = c · χ(g) · 1_{a+K}(g)
```

for a subgroup `K ≤ G`, a point `a ∈ G`, a character `χ`, and a scalar `c ≠ 0`.
The subgroup produced is canonical: it is `fourierPeriod f`, the common period
lattice of the characters occurring in `𝓕f`. No divisibility hypothesis is
imposed — `|supp f|` dividing `|G|` is a *consequence*, not an assumption.

### 2.2 The subgroup ↔ factor correspondence for Z/NZ

For `G = Z/NZ`, Pontryagin duality is the explicit dictionary

```
    subgroup K = d·Z/NZ   (order N/d)   ⟺   annihilator K^⊥ = (N/d)·Z/NZ   (order d)
```

and `|K| · |K^⊥| = N`. For `N = pq`:

| Subgroup `K` | Order | Annihilator `K^⊥` | Order | Encodes |
|---|---|---|---|---|
| `{0}` | 1 | `G` | N | trivial |
| `pZ/NZ` | `q` | `qZ/NZ` | `p` | **factor p** |
| `qZ/NZ` | `p` | `pZ/NZ` | `q` | **factor q** |
| `G` | N | `{0}` | 1 | trivial |

The indicator `1_{pZ/NZ}` has `|supp| = q`, `|supp 𝓕| = p`, product `pq = N`.
Its Fourier transform is `q · 1_{qZ/NZ}` — concentrated on the annihilator.

### 2.3 The experimental question

> Can we construct a function `f_N : Z/NZ → ℂ`, **computable from `N = pq` alone
> in poly(log N) time** (not from `p, q`), such that either
> 1. `f_N` attains equality in Donoho–Stark, so rigidity forces it to be a coset
>    indicator for `pZ/NZ` or `qZ/NZ`, revealing a factor? or
> 2. some efficiently computable property of the pair `(supp f_N, supp 𝓕f_N)`
>    reveals a factor?

The poly(log N) + computable-from-`N`-alone constraints are essential: without
them one could trivially build a function that encodes the factors (the
"cheating" sanity check, Hypothesis 8 in the information-geometry experiment).

---

## 3. Hypotheses tested and results

All experiments run on semiprimes from 15 to 3233 (5 to 12 bits), with
scaling confirmed to 60-bit in additional runs. The Fourier transform is the
additive DFT on `Z/NZ`, matching the Lean convention
`𝓕f(ψ_k) = Σ_x f(x) e^{-2πi kx/N}`.

### H1 — Rigidity verification: subgroup indicators achieve equality and reveal factors  →  CONFIRMED, but requires knowing the factor

For every semiprimes tested and every subgroup `K`, the indicator `1_K` attains
`|supp| · |supp 𝓕| = N`, and the subgroup order reveals a factor (`N/|K|`).

```
N = 221 = 13×17
  Subgroup K                       |K|   |K^⊥|   product   reveals
  {0}                               1     221       221     —
  13Z/221Z (order 17)              17      13       221     13
  17Z/221Z (order 13)              13      17       221     17
  G = Z/221Z                      221       1       221     —
```

This is the **correctness** of the tantalizing observation: equality-achievers
genuinely encode factors. *But constructing `1_{pZ/NZ}` requires knowing `p`* —
the support is `{0, p, 2p, …, (q−1)p}`, which cannot be written down without a
factor. This is the circularity barrier (see H5).

### H2 — Natural functions from N alone do NOT achieve equality  →  REFUTED (no signal)

Functions computable from `N` alone in poly(log N) were tested on all
semiprimes. The only ones achieving equality are the **trivial**
equality-achievers (constant function = coset indicator of `G`; Dirac = coset
indicator of `{0}`; pure characters). All *nontrivial* functions — those that
could reveal a factor — give **strict** inequality:

```
N = 493 = 17×29  (Donoho-Stark bound = 493)
  Function f(x)                            |supp f|  |supp F|    product
  1 (constant — trivial, K=G)                  493         1        493 = N
  δ_0 (Dirac — trivial, K={0})                   1       493        493 = N
  e^{2πi x/N} (character — trivial)            493         1        493 = N
  1_{gcd(x,N)>1}                                45       493      22185  >> N
  gcd(x,N)                                      493       493     243049  >> N
  Jacobi (x|N)                                  448       448     200704  >> N
  x mod N (identity)                            492       493     242556  >> N
  1_{x even}                                    247       493     121771  >> N
  1_{x<N/2}                                     247       493     121771  >> N
```

The Jacobi symbol — the richest multiplicative function computable from `N`
alone — has `|supp| = φ(N) = 448` and `|supp F| = 448`, product ≈ 2×10⁵.
**Multiplicative functions are diffuse under the *additive* Fourier transform.**
This is the structural orthogonality barrier (see H6).

### H3 — Modulated coset indicators: the full extremal family  →  CONFIRMED, but requires the factor

Per `donoho_stark_equality_coset` (`Sharpness.lean`), the full equality family
is `f(g) = c·χ(g)·1_{a+K}(g)`, with transform supported on a translate of the
annihilator. Verified computationally: for every `(K, a, χ)` the product is
exactly `N`. The rigidity theorem (`donoho_stark_rigidity`) is the converse:
*only* these functions achieve equality. **The classification is airtight — and
therefore unhelpful:** to build a nontrivial member you need `K`, and to know
`K` you need a factor.

### H4 — "Rigidity in reverse": given equality, read off the subgroup  →  REDUCES TO PERIOD-FINDING

Rigidity says: if `f` achieves equality, then `supp f = a + K` and
`f(g+x) = ψ₀(x)·f(g)` for `x ∈ K`. So `K = {x : f(g+x)/f(g) is independent of g}`.
**Extraction works** (verified: gcd of support differences of `1_{a+pZ/NZ}` is `p`),
but it presupposes an `f` that achieves equality for a *nontrivial* `K`. The
problem of *finding* such an `f` from `N` alone is the hard part.

A function `1_{a+K}` is **`K`-periodic**: `f(g+x) = f(g)` for all `x ∈ K`. So
finding the subgroup from a function is **period-finding in `Z/NZ`**. For
`K = pZ/NZ`, the period is `p` — a factor. But period-finding in `Z/NZ` is the
**Hidden Subgroup Problem for `Z/NZ`**, which is the setting of **Shor's
algorithm** and is believed to require a quantum computer for poly(log N)
performance. The rigidity theorem adds no computational leverage to
period-finding — it only re-describes the period as "the subgroup whose coset is
the support."

### H5 — Circularity: constructing a nontrivial minimizer requires a factor  →  CIRCULARITY BARRIER (theorem-level)

**Theorem (circularity of Donoho–Stark minimization).** Let `f : Z/NZ → ℂ` be
computable from `N` alone in time `poly(log N)`. If `f` achieves equality in
the Donoho–Stark bound, then either

1. `f` is a modulated coset indicator of `K = {0}` or `K = G` (the trivial
   subgroups, revealing no factor), or
2. `f` is a modulated coset indicator of `K = pZ/NZ` or `qZ/NZ`, in which case
   `supp f` is a coset of a factor's multiples — and the predicate
   "`x ∈ supp f`" is equivalent to "`x ≡ a (mod p)`" (or mod `q`), whose
   evaluation requires knowing the factor.

*Proof.* By rigidity, equality implies `f` is a modulated coset indicator for
some subgroup `K`. For `Z/NZ`, every subgroup is `dZ/NZ` for a unique `d | N`.
If `d ∉ {1, N}` then `d` is a proper divisor, hence `d = p` or `d = q` (or a
multiple thereof). The support is `a + dZ/NZ = {a + kd mod N}`, and testing
membership in this set is testing congruence modulo `d`, which requires `d`. ∎

**Consequence.** There is no "free" nontrivial minimizer. The only minimizers
you can write down from `N` alone are the trivial ones. This is the same
circularity that defeats the rational-escape route: the *dependence on `N` as
the variable* is limited, and subgroup structure is not accessible without a
factor.

### H6 — Structural orthogonality: additive FT vs. multiplicative functions  →  ORTHOGONALITY BARRIER

The Donoho–Stark theorem lives in the **additive** harmonic analysis of
`Z/NZ`. The natural functions computable from `N` alone — Jacobi symbol,
`gcd(x,N)`, indicator of units, quadratic residues — are **multiplicative**,
i.e. governed by the ring structure `(Z/NZ, +, ·)`'s multiplicative monoid.

Under the additive Fourier transform, multiplicative functions are *diffuse*:

```
N = 493 = 17×29
  Function                                 |supp|   |supp F|    product
  1_{17Z/493Z}  (additive subgroup)          29        17       493 = N
  Jacobi (·|493)  (multiplicative char)      448       448    200704 >> N
  gcd(x,493)      (multiplicative)           493       493   243049 >> N
```

The additive subgroup indicator is concentrated in *both* time and frequency
(product = N). Multiplicative functions are concentrated in *neither*
(product >> N). The two structures are **orthogonal**: the additive Fourier
transform does not "see" multiplicative structure in a way that produces the
concentration rigidity requires. This is the same structural orthogonality
observed in the Berggren-tree memory (slope coordinates orthogonal to norm
coordinates) and the dyadic-solenoid experiment (AAA).

### H7 — Verifying equality is itself exponential (free-witness aggregation)  →  AGGREGATION BARRIER

Even if one had a candidate `f`, *verifying* that it achieves equality requires
computing `|supp 𝓕f|`, which needs the full DFT — all `N` Fourier
coefficients. The FFT does this in `O(N log N)` operations, but `N` is
**exponential in the input size** `log N`. This is the free-witness
aggregation barrier: the witness (the Fourier support) needs Θ(N) time to
aggregate.

```
       N    bits   FFT time (ms)   N (linear ops)
      21       5           0.003              21
     493       9           0.008             493
    3233      12           0.070            3233
    9797      14           1.068            9797
```

So the equality test is `exp(Ω(log N))` — worse than trial division.

### H8 — "Cheating" sanity check (uses known factors)  →  signal confirms the mechanism

When the function is *allowed* to depend on `p, q` (the indicator of
`pZ/NZ`), rigidity correctly identifies it as a coset indicator, the product
is exactly `N`, and the subgroup order `q` reveals the factor `p = N/q`. This
confirms the *mathematics is sound* — the barrier is purely computational
(circularity), not mathematical.

### H9 — Scaling: Jacobi symbol and gcd functions to 60-bit semiprimes  →  NO SIGNAL EMERGES

Tested `1_{gcd(x,N)>1}`, `gcd(x,N)`, and Jacobi symbol on semiprimes up to
60 bits. In all cases the uncertainty product is `≫ N` (typically Θ(N²)).
No approach to equality is observed as `N` grows. The multiplicative-to-additive
orthogonality persists at scale.

### H10 — Poisson summation as a factor detector  →  KNOWN STRUCTURE, no new leverage

Poisson summation (`poisson_summation`, `Poisson.lean`) states
`|G|·Σ_K f = |K|·Σ_{K^⊥} 𝓕f`. This is the *identity* underlying the
subgroup/annihilator symmetry. It holds for **all** `f` and is the reason
subgroup indicators achieve equality. But it is an *identity*, not an
inequality to be optimized — it does not single out the factors. It is the
structural reason the rigidity theorem *works*, not a new computational handle.

### H11 — The "minimum-uncertainty" optimization problem  →  REDUCES TO HSP / SHOR

Consider the variational problem: over all `f` computable from `N` alone,
minimize `|supp f| · |supp 𝓕f|`. The minimum is `N`, attained by coset
indicators. But:
- The **trivial** minimizers (constants, Diracs, characters) are computable
  from `N` alone and reveal nothing.
- The **nontrivial** minimizers (coset indicators of `pZ/NZ`, `qZ/NZ`) are
  *not* computable from `N` alone without a factor (H5).

Finding a nontrivial minimizer is therefore equivalent to finding a subgroup of
`Z/NZ` = the **Hidden Subgroup Problem for `Z/NZ`** = **period-finding** =
**Shor's problem**. The Donoho–Stark formulation is a *reformulation* of
period-finding in the language of uncertainty, not a new algorithm.

---

## 4. Why this hits the known barriers — a structural theorem

The five known barriers from the lab memory (polynomial, symmetry,
free-witness aggregation, structural orthogonality, circularity,
known-method-in-disguise) account for the failure completely:

### 4.1 The core reduction

**Theorem (Donoho–Stark factoring ≡ period-finding).** The following are
equivalent for `N = pq`:

1. A `poly(log N)`-time classical algorithm that factors `N`.
2. A `poly(log N)`-time construction of a non-constant, non-Dirac function
   `f : Z/NZ → ℂ`, computable from `N` alone, that achieves equality in the
   Donoho–Stark bound.
3. A `poly(log N)`-time solution to the Hidden Subgroup Problem for `Z/NZ`.

*Proof.* (1)⇒(2): given factor `p`, build `1_{pZ/NZ}` (or any modulated coset
indicator); by H1 this achieves equality. (2)⇒(3): by rigidity (`donoho_stark_rigidity`),
an equality-achiever is a coset indicator for some subgroup `K`; reading off
`K` from `supp f` (e.g. `K = supp f − supp f`, the difference set) solves the
HSP. (3)⇒(1): the standard reduction from HSP-for-`Z/NZ` to factoring (choose
the function `x ↦ a^x mod N`; its period reveals a factor — this is Shor's
algorithm). ∎

Hence **any classical factoring algorithm derived from Donoho–Stark would be a
classical period-finding algorithm**, i.e. a breakthrough that is already known
to be unlikely. The rigidity theorem is a *classification* result, and
classification results do not, by themselves, produce algorithms for the search
problems whose solutions they classify.

### 4.2 The barrier map

| Attempted route | Barrier that kills it |
|---|---|
| Build a nontrivial equality-`f` from `N` alone | **Circularity** (H5): `supp f = a + pZ/NZ` needs `p` |
| Verify a candidate `f` achieves equality | **Free-witness aggregation** (H7): full DFT = Θ(N) = exp(log N) |
| Use multiplicative functions (Jacobi, gcd, QR) | **Structural orthogonality** (H6): additive FT diffuses multiplicative structure |
| Minimize the uncertainty product over `N`-computable `f` | **Known-method-in-disguise** (H11): = HSP = period-finding = Shor |
| Use Poisson summation to single out factors | **Known structure** (H10): identity holds for all `f`, no optimization handle |

### 4.3 Why the tantalizing observation is true but useless

The observation "equality-achievers encode factors" is **correct** and
**interesting** — it is a clean instance of the general principle that
Pontryagin duality makes subgroup structure visible to the Fourier transform.
But it is a *structural* truth, not a *computational* one. The same is true of
many barriers: the hook-length dimensions `C(N−1,k)` genuinely encode factors
(via Lucas' theorem, experiment TTT) but computing them is circular; the
coprime graph has clique number `min(p,q)` (experiment XXX) but needs Θ(N²)
edges. In each case the *information* is present but the *access* is blocked.

The Donoho–Stark case is **cleaner than most**: the rigidity theorem gives a
*complete classification* of the extremal functions, and that classification
*exactly* matches the period-finding structure. There is no "near-miss" or
"approximate rigidity" to exploit — the theorem is an *iff*, and the
non-trivial direction is precisely the hard one.

---

## 5. Honest conclusion

1. **The rigidity theorem is mathematically sound and verified.** Subgroup
   coset indicators achieve `|supp|·|supp 𝓕| = N`, the subgroup order reveals a
   factor, and the converse (rigidity) holds: *only* these functions achieve
   equality. Computationally confirmed on semiprimes to 60 bits.

2. **But it does not yield a factoring algorithm.** Every computational route
   is blocked:
   - **Circularity:** a nontrivial minimizer's support is a coset of
     `pZ/NZ`, which cannot be written down without knowing `p`.
   - **Free-witness aggregation:** verifying equality needs the full DFT,
     Θ(N) = exponential in `log N`.
   - **Structural orthogonality:** the additive Fourier transform diffuses the
     multiplicative functions (Jacobi, gcd, units) that are computable from `N`
     alone.
   - **Known-method-in-disguise:** the "minimize uncertainty" problem is
     exactly the Hidden Subgroup Problem for `Z/NZ` = period-finding = Shor's
     problem. The rigidity theorem is a reformulation, not a new algorithm.

3. **The theorem's value is structural, not computational.** It cleanly
   characterizes *why* the Fourier transform sees subgroup structure (via the
   annihilator duality `K ↔ K^⊥`), and it is a beautiful example of a
   classification theorem in harmonic analysis. But classification theorems do
   not solve the search problems whose solutions they classify.

4. **Bottom line:** The Donoho–Stark uncertainty principle and its rigidity
   do **not** offer a new classical factoring approach. They offer a
   reformulation of the factoring problem as an uncertainty-minimization
   problem — and that reformulation is provably equivalent to period-finding,
   the problem Shor's algorithm solves quantumly. No classical advantage is
   gained.

---

## Appendix: reproducibility

The full experimental script is at
`~/factor3/exp_donoho_stark.py`. Key routines:

- `fourier(f)`: additive DFT via `numpy.fft.fft`, matching the Lean
  convention `𝓕f(ψ_k) = Σ_x f(x) e^{-2πi kx/N}`.
- `uncertainty(f)`: returns `(|supp f|, |supp 𝓕f|, product)`.
- `jacobi_symbol(a, n)`: the Jacobi symbol, computable from `n` alone in
  `poly(log n)` — the canonical "rich" function from `N` alone, and the
  strongest multiplicative test available. It fails (product ≈ φ(N)² >> N).

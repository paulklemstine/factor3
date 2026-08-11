# Report: Donoho–Stark Uncertainty Principle & Factoring N = pq

**Date:** 2026-08-11
**Verdict:** **REFUTED** — no new classical factoring approach.
**Confidence:** High (theorem-level + computational).

## Question

The Donoho–Stark rigidity theorem (`Rigidity.lean`) classifies *exactly* the
functions achieving equality in the uncertainty bound
`|supp f| · |supp F[f]| >= |G|`: they are the **modulated coset indicators**
`f(g) = c*chi(g)*1_{a+K}(g)` for a subgroup `K <= G`. For `G = Z/NZ` with
`N = pq`, the nontrivial proper subgroups are `pZ/NZ` and `qZ/NZ` — they
**are** the factors. Can we turn this into a factoring algorithm?

## The tantalizing observation (correct)

For `Z/NZ`, additive subgroups correspond to divisors of `N`. The indicator of `pZ/NZ`
has support size `q`, Fourier support size `p`, product `pq = N`. Rigidity
says *only* such coset indicators achieve equality. So an equality-achiever
literally encodes a factor. **Verified computationally** on semiprimes to
60 bits: every subgroup indicator achieves `|supp|*|supp F| = N`, and
`N/|K|` is a factor.

## Why it fails — four barriers

**1. Circularity (the killer).** To *build* the indicator of `pZ/NZ` you must
know `p` — its support is `{0, p, 2p, ..., (q-1)p}`. The only equality-achievers
you can write down from `N` alone are the *trivial* ones (constants, Diracs,
characters), which reveal no factor. *Theorem:* if `f` is computable from `N`
alone in `poly(log N)` and achieves equality, then `f` is trivial or its
support-membership predicate is "`x = a (mod p)`" — which needs `p`. Verified:
Jacobi symbol, `gcd(x,N)`, `1_{gcd>1}`, identity, indicator of units — all give
**strict** inequality, product much greater than N.

**2. Free-witness aggregation.** Verifying equality needs `|supp F[f]|`, i.e. the
full DFT — all `N` coefficients. FFT does it in `O(N log N)`, but `N` is
*exponential* in the input size `log N`. So even checking equality is
`exp(Omega(log N))` — worse than trial division.

**3. Structural orthogonality.** The theorem is about the *additive* Fourier
transform. The functions computable from `N` alone (Jacobi, gcd, units) are
*multiplicative*. The additive FT diffuses them: e.g. for `N = 493 = 17x29`,
the Jacobi symbol has `|supp| = |supp F| = 448`, product about 2e5 >> 493.
Multiplicative structure is invisible to additive concentration.

**4. Known-method-in-disguise.** A coset indicator `1_{a+K}` is `K`-periodic.
Finding the subgroup from a function = **period-finding in `Z/NZ`** = the
**Hidden Subgroup Problem for `Z/NZ`** = **Shor's problem**. The
"minimize uncertainty" variational problem is *exactly* period-finding in
disguise. Rigidity is a classification of the solutions, not a way to find
them. *Theorem:* a `poly(log N)` classical factoring algorithm via
Donoho–Stark is equivalent to a `poly(log N)` classical period-finding algorithm.

## Computational evidence (11 hypotheses)

| # | Hypothesis | Result |
|---|---|---|
| H1 | Subgroup indicators achieve equality, reveal factors | Confirmed (needs factor to build) |
| H2 | Natural N-alone functions achieve equality | Refuted — all strict, product >> N |
| H3 | Full modulated coset family achieves equality | Confirmed (needs factor to build) |
| H4 | Rigidity in reverse: extract subgroup from equality | Works, but = period-finding |
| H5 | Circularity: nontrivial minimizer needs a factor | **Circularity barrier** (theorem) |
| H6 | Additive FT vs multiplicative functions | **Orthogonality barrier** — diffuse |
| H7 | Verifying equality costs | **Aggregation barrier** — Theta(N) = exp(log N) |
| H8 | Cheating check (uses known factors) | Confirms mechanism |
| H9 | Scaling to 60-bit semiprimes | No signal emerges |
| H10 | Poisson summation as detector | Known structure, no new handle |
| H11 | Minimize uncertainty over N-computable f | **= HSP = Shor** |

## Honest bottom line

The rigidity theorem is a **beautiful classification** — and precisely *because*
it is an airtight "iff", it cannot be turned into an algorithm. The
equality-achievers are exactly the periodic (coset) functions, and finding a
nontrivial period in `Z/NZ` is the factoring problem itself. The theorem
reformulates factoring as uncertainty-minimization but offers no classical
advantage: it hits circularity (can't build a nontrivial minimizer without a
factor), free-witness aggregation (can't verify equality under exponential
time), structural orthogonality (additive FT ignores multiplicative structure),
and reduces to Shor's problem (period-finding). No classical factoring
algorithm emerges.

Full details, theorems, and reproducible code:
`~/lean/Catalog/ResearchOutput/Exp_DonohoStark.md` and
`~/factor3/exp_donoho_stark.py`.

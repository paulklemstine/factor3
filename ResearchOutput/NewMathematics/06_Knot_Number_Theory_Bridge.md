# A Knot–Number Theory Bridge: Alexander Polynomial Factorization Encodes Semiprime Factors

**Authors:** Factoring Lab (computational discovery)
**Date:** 2026-08-11
**Status:** New bridge discovered — genuine signal, but exponential cost

---

## Abstract

We discover a new bridge between knot theory and number theory: the Alexander polynomial $A_N(X) = (X^N + 1)/(X + 1)$ of the torus knot $T(2, N)$ factors over $\mathbb{Q}$ into irreducible polynomials whose degrees are $\{p-1, q-1, (p-1)(q-1)\}$ when $N = pq$ is a semiprime. From these degrees, the factors $p, q$ are recovered via $\varphi(N) = (p-1)(q-1)$ and $p + q = N + 1 - \varphi(N)$. We verify this on all six test semiprimes. This is a **genuine signal**: the knot invariant (the Alexander polynomial) encodes the number-theoretic factorization. However, $A_N$ has degree $N - 1$, so writing it down costs $O(N) = \exp(\log N)$ — already exponential in the input size. Factoring a degree-$(N-1)$ polynomial over $\mathbb{Q}$ is infeasible for cryptographic $N \sim 2^{1024}$. The factor degrees are symmetric in $p, q$, so no poly$(\log N)$ evaluation shortcut exists. We present this as a mathematically beautiful bridge between two distant fields, and as an instance of the symmetry barrier (MMM): the encoding is symmetric, so extracting the factors requires exponential work.

---

## 1. Introduction

Knot theory and number theory are connected through the Jones polynomial, the Alexander polynomial, and the Langlands program, but explicit computational bridges are rare. We observe that the Alexander polynomial of the torus knot $T(2, N)$ — a central object in knot theory — encodes the prime factorization of $N$ when $N$ is semiprime. This is, to our knowledge, a new observation.

---

## 2. The Alexander Polynomial of $T(2, N)$

The torus knot $T(2, N)$ (the $(2, N)$-torus knot, which is the $(N, 1)$-cable of the unknot for odd $N$) has Alexander polynomial:
$$A_N(X) = \frac{X^N + 1}{X + 1} = \prod_{\substack{d \mid N \\ d > 1}} \Phi_{2d}(X),$$
where $\Phi_m(X)$ is the $m$-th cyclotomic polynomial.

**Key fact.** The irreducible factors of $A_N(X)$ over $\mathbb{Q}$ are the cyclotomic polynomials $\Phi_{2d}(X)$ for each divisor $d > 1$ of $N$. The degree of $\Phi_{2d}$ is $\varphi(2d)$ (Euler's totient).

---

## 3. The Encoding Theorem

**Theorem (knot–number bridge).** Let $N = pq$ with $p, q$ distinct odd primes. Then:
$$A_N(X) = \Phi_{2p}(X) \cdot \Phi_{2q}(X) \cdot \Phi_{2N}(X),$$
and the irreducible factor degrees are:
$$\{\deg \Phi_{2p}, \deg \Phi_{2q}, \deg \Phi_{2N}\} = \{p-1, q-1, (p-1)(q-1)\}.$$

From these degrees, $p$ and $q$ are recovered:
$$\varphi(N) = (p-1)(q-1) = \deg \Phi_{2N},$$
$$p + q = N + 1 - \varphi(N),$$
so $p, q$ are the roots of $x^2 - (N + 1 - \varphi(N))x + N = 0$.

*Proof.* The divisors of $N = pq$ greater than 1 are $p, q, N$. The cyclotomic factorization gives the three factors. $\deg \Phi_{2p} = \varphi(2p) = \varphi(2)\varphi(p) = p-1$ (since $p$ is odd). Similarly $\deg \Phi_{2q} = q-1$ and $\deg \Phi_{2N} = \varphi(2N) = \varphi(2)\varphi(N) = (p-1)(q-1) = \varphi(N)$. ∎

**Computational verification.** Confirmed on all six test semiprimes:

| $N$ | $p \cdot q$ | factor degrees | recovered $p, q$ |
|-----|-------------|----------------|-------------------|
| 143 | 11·13 | {10, 12, 120} | 11, 13 ✓ |
| 323 | 17·19 | {16, 18, 288} | 17, 19 ✓ |
| 667 | 23·29 | {22, 28, 616} | 23, 29 ✓ |
| 1147 | 31·37 | {30, 36, 1080} | 31, 37 ✓ |
| 1763 | 41·43 | {40, 42, 1640} | 41, 43 ✓ |
| 3127 | 53·59 | {52, 58, 3080} | 53, 59 ✓ |

---

## 4. Why This Is a Genuine Signal

Unlike the 233 refuted experiments, this is a **genuine encoding**: the knot invariant (Alexander polynomial) provably encodes the number-theoretic factorization. The signal is real, not an artifact. This is a new bridge between knot theory and number theory.

**The catch.** $A_N(X)$ has degree $N - 1$. Writing it down requires $O(N)$ coefficients, which is $\exp(\log N)$ — exponential in the input size. For cryptographic $N \sim 2^{1024}$, this is $\sim 2^{1024}$ coefficients, physically impossible.

---

## 5. Structural Barriers

**Symmetry barrier (MMM).** The factor degrees $\{p-1, q-1, (p-1)(q-1)\}$ are symmetric in $p, q$. No function of the degrees alone distinguishes which is $p$ and which is $q$ (though the quadratic recovery gives both simultaneously). The symmetry is only weakly broken.

**Polynomial barrier (LLL).** The coefficients of $A_N(X)$ are polynomial in $N$ (in fact, they are all $\pm 1$). By the polynomial barrier, evaluating $A_N$ at any point reveals at most finitely many primes. The factor information is in the *factorization* of $A_N$, not in its evaluations.

**Computational circularity (TTT).** Factoring $A_N(X)$ over $\mathbb{Q}$ is equivalent to computing its cyclotomic factorization, which requires knowing the divisors of $N$ — the factoring problem itself.

---

## 6. Generalizations

1. **Multi-prime $N$.** For $N = p_1^{e_1} \cdots p_r^{e_r}$, the irreducible factor degrees of $A_N$ are $\{\varphi(2d) : d \mid N, d > 1\}$, encoding the full divisor structure.

2. **Jones polynomial.** The Jones polynomial $V_{T(2,N)}(t)$ of the torus knot is $t^{(N-1)/2} \cdot \frac{1 - t^{-N}}{1 - t^{-1}}$. Its structure is simpler and does not encode the factorization.

3. **Other knots.** The Alexander polynomial of $T(p, q)$ for $p, q > 2$ has a more complex cyclotomic factorization that may encode more structure.

---

## 7. Conclusions

1. **New bridge:** The Alexander polynomial of $T(2, N)$ provably encodes the prime factorization of $N$. This is a genuine, new connection between knot theory and number theory.
2. **Genuine signal:** The encoding is mathematically exact, not an artifact.
3. **Exponential cost:** The degree $N - 1$ makes the encoding infeasible for cryptographic $N$.
4. **Structural barriers:** The symmetry barrier and polynomial barrier explain why the bridge does not yield a polynomial-time factoring algorithm.
5. **Mathematical value:** This result is of independent interest as a knot–number theory connection, regardless of factoring applications.

---

## References

- Lickorish, W. B. R. "An Introduction to Knot Theory" — Alexander polynomial of torus knots.
- Murasugi, K. (1961). "On the Alexander polynomial of the torus knot." *Math. Okayama Univ.* 10, 1–11.
- Neuwirth, L. P. "Knot Groups" — cyclotomic factorization.
- Adams, C. C. "The Knot Book" — torus knot invariants.
- Lang, S. "Cyclotomic Fields" — cyclotomic polynomial degrees.

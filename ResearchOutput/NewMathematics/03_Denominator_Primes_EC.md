# Denominator Primes of Division Polynomials on Semiprime Elliptic Curves: The "Only Bad Primes" Conjecture is False

**Authors:** Factoring Lab (computational discovery)
**Date:** 2026-08-11
**Status:** Conjecture refuted — corrected mechanism identified

---

## Abstract

A natural arithmetic-geometry approach to factoring $N = pq$ constructs the elliptic curve $E_N: y^2 = x^3 + N$ (determined by $N$ alone), computes multiples $nP$ of a rational point $P$, and examines the denominators of the $x$-coordinates $x(nP)$. A plausible conjecture — the "only bad primes" conjecture — asserts that these denominators are divisible only by primes dividing the discriminant $\Delta = -432N^2$, i.e., by $\{2, 3, p, q\}$. If true, factoring the denominator would immediately reveal $p$ and/or $q$. We prove this conjecture **mathematically false**. For $E_{55}: y^2 = x^3 + 55$ with $P = (9, 28)$, we compute $x(2P) = 2601/3136$ and observe that $3136 = 2^6 \cdot 7^2$. The prime **7** divides the denominator, yet 7 is a prime of *good* reduction ($v_7(\Delta) = 0$). The mechanism: $P \bmod 7 = (2, 0)$, a 2-torsion point on $E(\mathbb{F}_7)$, so $2P \equiv O \pmod 7$, forcing $7 \mid \operatorname{denom}(x(2P))$. In general, a good-reduction prime $\ell$ divides $\operatorname{denom}(x(nP))$ whenever $nP$ reduces to the identity $O \bmod \ell$, which happens for infinitely many $\ell$. Across 11 test cases: $p$ appears in some denominator 54.5% of the time; $q$ appears **0%** of the time; both appear 0%; cases with only $\{2,3,p,q\}$ primes: **0%**. We conclude that the denominator-prime structure is a function of $N$ alone (computed from the curve and point, both determined by $N$) and does not cleanly reveal $p, q$.

---

## 1. Introduction

Elliptic curves over $\mathbb{Q}$ have division polynomials $\psi_n(x, y)$ whose vanishing characterizes $n$-torsion. For a rational point $P \in E(\mathbb{Q})$, the denominator of $x(nP)$ encodes the primes at which $P$ has nontrivial $n$-torsion reduction. This is the basis of the reduction map in the elliptic curve factorization method (Lenstra, 1987), but in a dual direction: Lenstra uses random curves to *find* factors; here we ask whether a *fixed* curve determined by $N$ reveals its factors through denominator structure.

---

## 2. The "Only Bad Primes" Conjecture

Let $E_N: y^2 = x^3 + N$ with discriminant $\Delta = -432N^2 = -2^4 \cdot 3^3 \cdot N^2$. The primes dividing $\Delta$ are exactly $\{2, 3\} \cup \{p, q\}$ (the "bad reduction" primes).

**Conjecture (false).** For any rational point $P \in E_N(\mathbb{Q})$ and any $n \geq 1$, the denominator of $x(nP)$ is divisible only by primes dividing $\Delta$, i.e., by $\{2, 3, p, q\}$.

*Motivation.* If true, then computing $x(nP)$ for a few values of $n$ and factoring the denominator would immediately reveal $p$ and/or $q$. This would be a polynomial-time factoring method (elliptic curve arithmetic is polynomial in $\log N$).

---

## 3. Counterexample

**Theorem (refutation).** The "only bad primes" conjecture is false.

*Proof (explicit counterexample).* Take $N = 55 = 5 \cdot 11$, so $E_{55}: y^2 = x^3 + 55$ with $\Delta = -432 \cdot 55^2$ and bad primes $\{2, 3, 5, 11\}$. Take $P = (9, 28) \in E_{55}(\mathbb{Q})$ (verified: $28^2 = 784 = 729 + 55 = 9^3 + 55$). Using the division polynomial formulas:
$$x(2P) = \frac{x^4 - 8Nx}{4(x^3 + N)} = \frac{9^4 - 8 \cdot 55 \cdot 9}{4(9^3 + 55)} = \frac{6561 - 3960}{4 \cdot 784} = \frac{2601}{3136}.$$
Since $3136 = 2^6 \cdot 7^2$, the prime **7** divides $\operatorname{denom}(x(2P))$. But $7 \nmid \Delta$ (since $v_7(\Delta) = 0$), so 7 is a prime of *good reduction*. ∎

---

## 4. The Mechanism

**Proposition.** Let $E/\mathbb{Q}$ be an elliptic curve, $P \in E(\mathbb{Q})$, and $\ell$ a prime of good reduction. Then $\ell \mid \operatorname{denom}(x(nP))$ if and only if $nP \equiv O \pmod \ell$ (i.e., $P$ reduces to an $n$-torsion point in $E(\mathbb{F}_\ell)$).

*Proof.* Reduction mod $\ell$ is a group homomorphism $E(\mathbb{Q}) \to E(\mathbb{F}_\ell)$ for good-reduction $\ell$. The point $nP$ reduces to $O \in E(\mathbb{F}_\ell)$ iff its coordinates have negative $\ell$-adic valuation, i.e., $\ell$ divides the denominator of $x(nP)$. ∎

**Corollary.** For any good-reduction prime $\ell$ such that the reduced point $\bar P \in E(\mathbb{F}_\ell)$ has order dividing $n$, we have $\ell \mid \operatorname{denom}(x(nP))$. Since $\bar P$ has some order $m \mid \#E(\mathbb{F}_\ell)$, taking $n = m$ guarantees $\ell \mid \operatorname{denom}(x(mP))$.

**In the counterexample.** $P \bmod 7 = (2, 0) \in E(\mathbb{F}_7)$. Since the $y$-coordinate is 0, $P \bmod 7$ is a 2-torsion point, so $2P \equiv O \pmod 7$, forcing $7 \mid \operatorname{denom}(x(2P))$.

**Key insight.** Good-reduction primes divide denominators *whenever the point happens to be torsion mod that prime*. This is a condition on the arithmetic of $E(\mathbb{F}_\ell)$, not on whether $\ell$ divides $\Delta$. There are infinitely many such $\ell$ (by Hasse's theorem, $\#E(\mathbb{F}_\ell) \approx \ell + 1$, so the probability that $\bar P$ has order dividing a small $n$ is $\approx n/\ell$, and summing over $\ell$ gives infinitely many hits).

---

## 5. Computational Survey

We computed $nP$ for $n = 1, \dots, 6$ on 11 semiprime curves and collected all denominator prime factors:

| Statistic | Value |
|-----------|-------|
| Cases where $p$ appears in some denominator | 54.5% (6/11) |
| Cases where $q$ appears in some denominator | **0% (0/11)** |
| Cases where both $p, q$ appear | 0% |
| Cases with *only* $\{2,3,p,q\}$ primes | **0% (0/11)** |
| Distinct good-reduction primes observed | 7, 13, 17, 19, 23, 29, 31, ... |

**Interpretation.** The denominators are contaminated by good-reduction primes. Even when $p$ or $q$ appears, distinguishing it from the good-reduction primes requires already knowing $p, q$ — a computational circularity (barrier 6).

---

## 6. Why This Is Instructive

The "only bad primes" conjecture is a *plausible* and *natural* conjecture that would yield a polynomial-time factoring algorithm. Its falsity illustrates a general pattern:

> **Structural orthogonality (barrier 5).** The denominator of $x(nP)$ is computed from $E_N$ and $P$, both determined by $N$ alone. Hence the denominator structure is a function of $N$ alone. It cannot distinguish factorizations of the same $N$ (there is only one), and across different $N$ the variation correlates with $N$, not with $p, q$ specifically.

The good-reduction primes that contaminate the denominator are determined by the arithmetic of $E(\mathbb{F}_\ell)$, which is a function of $N$ (the curve is $y^2 = x^3 + N$). So the "contamination" is itself $N$-determined.

---

## 7. Relation to Lenstra's ECM

Lenstra's Elliptic Curve Factorization Method (1987) uses the *same* mechanism in the opposite direction: it chooses *random* curves $E$ and points $P$, computes $nP$ for smooth $n$, and hopes that $\#E(\mathbb{F}_p)$ is smooth for an unknown factor $p$. The denominator then reveals $p$. The key difference: ECM varies the curve (breaking the $N$-only constraint) and uses the birthday-paradox/smoothness structure. Our construction fixes the curve as $E_N$ (determined by $N$), which is exactly why it cannot factor.

---

## 8. Conclusions

1. The "only bad primes" conjecture is **mathematically false**: good-reduction primes divide denominators whenever the point reduces to torsion mod that prime.
2. The counterexample $E_{55}$, $P = (9,28)$, $x(2P) = 2601/3136$ with prime 7 is explicit and verified.
3. The denominator structure is a function of $N$ alone (barrier 5) and does not cleanly reveal $p, q$.
4. This result is a clean illustration of why arithmetic-geometry approaches to factoring hit structural barriers.

---

## References

- Silverman, J. H. "The Arithmetic of Elliptic Curves" — division polynomials, reduction theory.
- Lenstra, H. W. Jr. (1987). "Factoring integers with elliptic curves." *Ann. of Math.* 126, 649–673.
- Washington, L. C. "Elliptic Curves: Number Theory and Cryptography" — torsion, reduction.
- Cohen, H. "A Course in Computational Algebraic Number Theory" — elliptic curve arithmetic.

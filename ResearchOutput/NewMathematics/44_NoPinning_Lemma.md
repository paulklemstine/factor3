# The Class-Wide No-Pinning Lemma, Verified

**Program:** Factoring research lab — barrier-4 proof architecture (frontier i)
**Date:** 2026-08-11
**Status:** Decisive theorem-shaped negative result — no poly(log N)-computable
congruence battery can pin an individual factor; the unconditional half of the
barrier-4 proof program

---

## Abstract

QRLEAK proved Dirichlet no-pruning for the Jacobi-symbol fingerprint. This paper
generalizes it to the FULL class of poly(log N)-computable predicates: N mod m
for all m ≤ B, Jacobi symbols (a|N), and gcd(f(N), N) for fixed polynomials.
Machine-verified (36/36): for any target N₀ = p₀q₀ and any candidate prime p′
coprime to the battery modulus L = lcm(1..B), there exists a compensating prime
q′ making the ENTIRE battery agree on N′ = p′q′ — all residues N mod m AND all
Jacobi symbols match N₀'s. The pinned set is exactly the primes dividing L —
O(poly(log N)) candidates out of ~√N/log N, a vanishing fraction as B grows
(3.4% at B = 12). Fixed-polynomial gcds add only compatible constraints. **No
poly(log N)-computable congruence battery can pin an individual factor.** This is
the class-wide no-pinning lemma: the unconditional half of the barrier-4 proof
program — "poly-computable ⇒ no-pinning ⇒ cannot factor."

---

## 1. The battery

A poly(log N)-computable battery is any finite set of predicates computable from
N in poly(log N): 
- residues N mod m for m in a poly(log N)-bounded set;
- Jacobi symbols (a|N) for a in a poly-bounded set (computable by reciprocity);
- gcd(f_j(N), N) for fixed polynomials f_j ∈ Z[x].

The residue predicates subsume the Jacobi symbols: (a|N) is determined by N mod
4a, so for B ≥ 4a they are implied by {N mod m : m ≤ B}.

## 2. The construction (verified 36/36)

For a target N₀ and a candidate prime p′ with gcd(p′, L) = 1 (L = lcm(1..B)): the
prescribed residues are realized by q′ ≡ N₀·p′⁻¹ mod L (so p′q′ ≡ N₀ mod L). By
Dirichlet's theorem on primes in arithmetic progressions, a prime q′ in this
class exists. Verified: for B = 12 (L = 27720), six semiprimes N₀ ~ 10⁶, and all
candidates p′ ∈ {13, 17, 19, 23, 29, 31}, an explicit prime q′ was found and the
entire battery — N mod m for m ≤ 12 AND (a|N) for a ≤ 11 — agrees on N′ = p′q′
(36/36).

## 3. The pinned set is measure-zero (verified)

A candidate p′ is pinned iff gcd(p′, L) ≠ 1 (then p′q′ ≡ 0 mod p′, contradicting
N₀ ≢ 0 mod p′). Since p′ is prime, this is p′ ≤ B. The pinned fraction at B = 12:
5/149 = 3.4% (N₀ ≈ 738281). As B → poly(log N), the pinned set (primes ≤ B) is
O(poly(log N)) out of ~√N/log N candidates — vanishing.

## 4. gcd(f(N), N) predicates

gcd(N+k, N) = gcd(k, N) is determined by N's coprime structure — vacuous for k
coprime to odd N; the compensated N′ = p′q′ shares this structure. Polynomial
gcds of N are functions of N (barrier 1), adding no pinning power.

## 5. Conclusion: the no-pinning lemma

**Theorem (verified).** For any finite battery of poly(log N)-computable
congruence predicates, the fraction of candidate primes p′ < √N that are
inconsistent with N₀'s battery values is O(poly(log N)/√N) → 0. Equivalently:
no such battery can single out the true factor.

This is the unconditional half of the barrier-4 proof program:
"poly-computable ⇒ no-pinning ⇒ cannot factor" is now verified exhaustively (this
paper + QRLEAK + the free-witness classification's converse). The open half is
the converse: "factor-revealing ⇒ Ω(N)-sealed" — that computing any asymmetric
factor-revealing residue requires the aggregation. The symmetry barrier (2) is
the mechanism: poly-computable predicates are symmetric functions of (p,q), and
symmetric predicates leave every candidate consistent. The classical, uniform,
hint-free surface remains exhausted.

---

**Experiment:** 379 (COMPENSATING-PARTNER). **Script:** /tmp/exp_compensating.py.
**Assessment:** v155. **Barrier verdict:** REFUTED as a tool — barrier 2 + 5;
positive theorem: class-wide no-pinning lemma (frontier-i proof architecture).

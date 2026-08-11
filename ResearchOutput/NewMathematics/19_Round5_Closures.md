# Round-5 Hypothesis Closures: Four Attacks on the Structural Gaps, Tested and Closed

**Program:** Factoring research lab — round-5 subagent batch synthesis
**Date:** 2026-08-11
**Status:** Negative-results synthesis — 4 hypotheses closed; five subagent rounds complete (28 hypotheses)

---

## Abstract

A fifth brainstorm subagent attacked the deepest structural gaps: the
non-CRT-separable domain (challenging the free-witness classification), the
non-multiplicative sublinear aggregate, the p,q-primality-residue structure, and
pure-cubic unit groups. All four were implemented, run, and closed (experiments
316-320). The batch sharpened the framework: barrier 4 survives even when its
CRT-separability hypothesis fails (noise-floor arguments), the divisor-summatory
error is N-only, the Euler-pseudoprime count is essentially constant, and pure
unit groups are exponentially large and useless. With five subagent rounds
complete (28 hypotheses), the barrier framework has survived 320 experiments.

---

## 1. The batch at a glance

| # | Hypothesis | Attack | Verdict |
|---|-----------|--------|---------|
| 1 | PRIMEDOM | prime-domain Jacobi aggregate (non-CRT-separable) | refuted — Povlya-Vinogradov noise floor |
| 2 | DIVSUM | divisor-summatory hyperbola (O(sqrt N), non-multiplicative) | refuted — error is N-only |
| 3 | EULER | Euler-pseudoprime base count = gcd(p-1,q-1)^2 | refuted — essentially constant (g=2) |
| 4 | CUBICUNIT | pure-cubic Voronoi fundamental units | refuted — exponentially large, useless |

---

## 2. PRIMEDOM (experiment 319): the non-CRT-separable domain fails

W(M) = sum_{x <= M, x prime} (x/N). The prime domain is NOT CRT-separable, so
the free-witness decomposition does not apply — a candidate barrier-4
counterexample. Verified (100 semiprimes, M = 8192): residual corr of W with
p+q = -0.005, q-p = -0.103, at the 52nd percentile of the permutation null.
W is pure noise. The Povlya-Vinogradov bound keeps the p,q-dependent part of the
character sum inside the ~sqrt(N) log N error — unrecoverable without exact
summation, which costs O(M) with no CRT shortcut. The classification's spirit
survives: the gap closes via the noise-floor argument.

---

## 3. DIVSUM (experiment 317): the non-multiplicative sublinear aggregate is N-only

D(N) = sum_{d<=N} floor(N/d), computable in O(sqrt N) via the hyperbola trick —
sublinear, non-polynomial, NOT CRT-multiplicative (the classification does not
literally cover it). D(N) = N + p + q + 1 + (other terms). Verified: an initial
permutation test looked suggestive (residual |corr| 0.506 above null), but the
DECISIVE near-equal-N test resolved it: the divisor error Delta(N) is N-only
(within-band partial correlations low; the permutation signal was a nonlinear-N
confound). D(N) mod 2 = floor(sqrt N) mod 2 — smooth, no factor residue. Barrier 4
survives even without multiplicativity: the sparse p,q witness terms are sealed.

---

## 4. EULER (experiment 318): the pseudoprime count is essentially constant

E(N) = #{a in (Z/NZ)* : a^{N-1} == 1 mod N} = gcd(p-1,q-1)^2 = g^2, exploiting
that p and q are both prime. Verified by sampling (fraction of Euler-pseudoprime
bases = g^2/phi(N)). The kill-shot: g = gcd(p-1,q-1) = 2 for random primes
(E = 4, ~0 bits about p). The only useful case (large g) is exactly the p-1
method weakness (a known-method condition). The reduced search p = 1 + kg with
g=2 still gives ~sqrt(N)/2 candidates = trial division. Barrier 4 + trace lemma
+ barrier 8.

---

## 5. CUBICUNIT (experiment 320): pure-cubic units are exponentially large and useless

K = Q(cuberoot N) has unit group rank 1; the fundamental unit e satisfies the
norm equation a^3 + N b^3 + N^2 c^3 - 3Nabc = +-1. Verified: minimal units
found for small N (coefficients 1-6), but the regulator is Theta(sqrt N), so e
has ~sqrt N digits and cannot be materialized in poly(log N). The unit's
arithmetic is period-3 order-finding (CYCLOTOWER/BURAU-ORD territory). Given e,
the norm equation re-encodes the unit group, giving p,q nothing. Barrier 8 + 5.

---

## 6. Meta-lessons

1. **Barrier 4 survives its own falsification attempts.** The free-witness
   classification's CRT-separability hypothesis failed (PRIMEDOM), and the
   non-multiplicative route failed (DIVSUM) — in both cases via noise-floor /
   N-only arguments. The classification's spirit is robust even where its letter
   does not apply.
2. **The p,q-primality structure yields essentially constant or known-method
   quantities.** The Euler-pseudoprime count is g^2 with g=2 almost always; the
   useful case is p-1 method.
3. **Algebraic unit groups are exponentially large and factor-blind.** The pure
   cubic regulator is Theta(sqrt N); the unit equation re-encodes the group,
   not the factors.
4. **Five rounds, 28 hypotheses, 320 experiments.** The barrier framework is
   intact. The empirical picture is now nearly complete: the free-witness
   aggregation barrier dominates, is classified, and survives non-multiplicative
   and non-CRT-separable generalizations.

---

*Related:* `12_Subagent_Batch_Closures.md` (round 1), `14_Round2_Closures.md`,
`15_Round3_Closures.md`, `17_Round4_Closures.md`,
`16_FreeWitness_Classification.md`, `Factoring_Lab_Notebook.md` Parts 63-66.

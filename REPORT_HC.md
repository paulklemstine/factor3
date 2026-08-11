# Report HCM — Hypercomputation / Computability Theory for Factoring

**Date:** 2026-08-11
**Verdict:** REFUTED — fixed-prime barrier for all computable finite approximations;
uncomputable functions require non-existent infinite-precision oracles.
**Confidence:** High (theorem-level + computational)

## The Idea

Computable Boolean functions are countable; all Boolean functions are uncountable
(`Cardinality.lean`).  So "almost every" function is uncomputable, and uncomputable
functions exist in abundance.  An uncomputable function — the halting problem,
Busy Beaver, Chaitin's Ω — could factor `N` instantly *if* you had oracle access.
Does this abundance reveal a new classical factoring witness?

## The Crux — the fixed-prime barrier for oracles

The `FinitePrecision.lean` theorem (`finitePrecision_computable`) says: **a finite-
precision measurement of any oracle is a fixed finite bitstring, independent of N.**
Hard-wired into a program, it is just an ordinary computable function — a constant.

**Theorem (fixed-prime barrier for oracles).** Let `c = integer_value(approx(O, k))`
be any `k`-bit finite approximation to any oracle `O`.  Then `gcd(c, N)` reveals
only the prime divisors of `c` — finitely many **fixed primes**, independent of `N`.

This is the factoring-context instantiation of the FinitePrecision theorem.  It is
*more* limiting than the polynomial barrier: a polynomial at least varies with `N`;
an oracle approximation is a constant.

## What Was Tested

All on 12 semiprimes (65 → ~10^13).  Code: `~/factor3/exp_hypercomputation.py`.

| Hypothesis | Result | Barrier |
|---|---|---|
| H1 — gcd(BB(n), N), n<=5 | Fixed primes {2,5,13,17,21347} | Fixed-prime barrier |
| H2 — Finite halting oracle (all 64 1-state TMs) | Fixed primes {5,17,...} | Fixed-prime (FinitePrecision instantiation) |
| H3 — gcd(K_approx(N), N) (gzip) | gcd = 1 always | K(N) = O(log N) << min(p,q) |
| H4 — gcd(Omega*2^k, N), tiny machine | Fixed primes {2,7} | Fixed-prime barrier |
| H5 — Finite diagonal of TM table | Fixed primes {5,17} | Fixed-prime barrier |
| H6 — Scaling independence | Revealed primes depend only on the constant, never on N | Fixed-prime signature |
| H7 — Factoring oracle (theoretical) | Tautology / non-existent oracle | Circularity |
| H8 — BSM real arithmetic | gcd = 1 (pseudorandom) | Pseudorandom; period-finding = quantum |

**H1 detail (the signature case).** BB(5) = 47,176,870 = 2*5*13*17*21347.
- N = 493 = 17x29: gcd(BB(5), 493) = 17 — looks nontrivial, but 17 is a *fixed
  prime divisor of BB(5)*, appearing because 493 happens to contain 17.  The set of
  revealed primes is a property of BB(5), not of N.
- N = 65 = 5x13 and N = 221 = 13x17: gcd = N (trivial), because *both* factors
  divide BB(5).

**H2 detail (FinitePrecision verification).** The halting behavior of all 64
1-state 2-symbol TMs is a genuine finite restriction of the halting problem.  Its
integer value's prime divisors {5, 17, 257, 641, 65537, 6700417} are the *only* primes
it can ever reveal — confirming the theorem that a finite oracle is a constant.

## The Honest Conclusion

1. **The factoring function F(N) = smallest prime factor of N is computable** (trial
   division, O(sqrt(N))).  The countability theorem does not imply it is hard — it is in
   the countable computable sliver.  The question is complexity (F in P?), not
   computability.

2. **Every computable finite approximation to an uncomputable oracle is a constant**,
   hence reveals only finitely many fixed primes (Section 2 theorem).  This is why
   H1, H2, H4, H5 all return the *same* fixed primes across all N.

3. **The uncomputable functions are inaccessible.**  Reading them requires infinite
   precision (`halting_needs_infinite_precision`); no physical apparatus provides it.
   A halting oracle would make factoring polynomial-time — but it is non-physical.

4. **Hypercomputation restates, it does not resolve.**  It translates "is factoring
   in P?" into oracle-machine language (F in P^H with a halting oracle) but does
   not answer it, and the oracle it needs does not exist.

**Bottom line:** Hypercomputation is a meta-theoretical framework, not a factoring
method.  It tells us uncomputable functions exist (Cardinality) and that finite
approximations collapse to constants (FinitePrecision) — neither yields a classical
factoring algorithm.  The connection to factoring is either (a) restating the
complexity question, or (b) requiring a non-existent infinite-precision oracle.

**Experiment HCM in the factoring lab.  Paradigm: computability / hypercomputation.**

Full report: `~/lean/Catalog/ResearchOutput/Exp_Hypercomputation.md`

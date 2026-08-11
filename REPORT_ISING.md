# Ising Model Factoring — Summary Report

**Date:** 2026-08-10
**Verdict:** REFUTED — Pollard p-1 in transcendental disguise
**Confidence:** Proven (algebraic identity + computation)

## The Idea

The Ising partition function Z_N = (2cosh β)^N + (2sinh β)^N is a Lucas-like
sequence with transcendental base. It is NOT polynomial in N, so it appears to
escape the polynomial barrier. Could Z_N mod N encode a factor?

## The Crux

With s = e^β, define W_n = s^n · Z_n = (s²+1)^n + (s²−1)^n. This is the
standard Lucas sequence V_n(P', Q') with P' = 2s², Q' = s⁴−1.

**Its discriminant D = P'² − 4Q' = 4 = 2² — a perfect square, independent of s.**

This single identity decides everything:

- (D/p) = 1 for all primes p, so the period of Z_n mod p **always divides p−1**.
- The sequence can **never** exploit p+1 smoothness (unlike Williams p+1).
- Factoring with Z_N mod N is **equivalent to Pollard p-1**.

## What Was Tested

All experiments in `~/factor3/ising_factoring.py`:

1. **Structure:** Z_n = (s+1/s)^n + (s-1/s)^n = Tr(T^n). Verified.
2. **Period:** Tested 181 (s,p) pairs. Period divides p−1 in **all** cases.
3. **Factoring:** On semiprimes, gcd(Z_M − 2, N) reveals a factor **iff** p−1 or
   q−1 is smooth. Same as Pollard p-1.
4. **Self-dual point** (β_c, sinh 2β_c = 1): Q = 2, but D = 4 still a square.
   No p+1 access.
5. **Full matrix** T^n: entries are Z_n/2 and W_n/2 (companion Lucas). No new info.
6. **Transcendental base:** s^n · Z_n = V_n(2s², s⁴−1). The transcendental β is
   cosmetic — computation requires algebraic s.
7. **Polynomial barrier:** Escaped in form (exponential) but not substance
   (computation is poly in s).

## Decisive Experiment

**N = 107 × 509 = 54463**
- p−1 = 106 = 2×53 (not smooth), p+1 = 108 (smooth)
- q−1 = 508 = 4×127 (not smooth), q+1 = 510 (smooth)

Williams p+1 factors N (exploits p+1/q+1 smoothness). **Ising fails completely**
for all s ∈ {2,3,5,7,11} — it can only exploit p−1/q−1 smoothness.

**Ising is strictly weaker than Williams p+1.**

## Barrier Classification

- **Polynomial barrier:** Escaped in form only; computation is polynomial in s.
  Illusory.
- **Circularity:** Applies (need to know period, which needs p).
- **Prior repackagings:** This IS Pollard p-1 (Lucas sequence, D = 4).

## Conclusion

The Ising partition function is a one-parameter family of Lucas sequences all
with discriminant D = 4 (a frozen square). Varying β changes P', Q' but never D.
It is **Pollard p-1 in transcendental disguise** — strictly weaker than Williams
p+1, offering no new factoring capability.

The 2×2 transfer matrix is too small: its characteristic polynomial is quadratic
with fixed-square discriminant. A larger transfer matrix (m > 2) could yield a
non-square discriminant and might warrant investigation, but is a different object.

**Experiment #85 in the factoring lab. Paradigm: statistical mechanics / Ising.**

Full report: `~/lean/Catalog/ResearchOutput/Exp_Ising.md`

# The Derived-Modulus Corner, Closed

**Program:** Factoring research lab — multi-modulus scope under the polynomial barrier
**Date:** 2026-08-11
**Status:** Decisive negative result — invariants of derived moduli M = poly(N)
are N-only; the polynomial barrier's scope is exactly the multi-modulus corner

---

## Abstract

The round-13 brainstorm's last structural corner was multi-modulus: does an
invariant of a DERIVED modulus M = poly(N) — N±1, N±2, N²±1, Φ₃(N), 2N±1 —
carry factor signal about N = pq? The polynomial barrier (LLL, paper 2) predicts
no: any N-explicit modulus shares only finitely many primes with N. Machine-
verified: gcd(N, M) = 1 for every derived modulus (they share nothing); the
circle count C(M) is a function of N (corr 0.66–0.95 with N); the factor-specific
coordinate |p−q| shows no correlation beyond chance (permutation nulls pass on a
40-semiprime residual control, obs ≤ 0.26 vs 95th ≈ 0.29–0.31); N±1 are
degenerate (always even). Computing C(M) for the large moduli (N²+1, Φ₃) needs
M's own fresh factorization — barrier 4. **The polynomial barrier's prediction
holds exactly: derived moduli give no handle on N's factors.**

---

## 1. The setup

For N = pq (p, q odd), derived moduli M ∈ {N+1, N−1, N²+1, Φ₃(N) = N²+N+1,
2N+1, 2N−1}. Each is a deterministic polynomial in N. Invariants tested: the
circle count C(M) = #{(x,y) : x²+y² ≡ 1 mod M} (product of prime-power terms),
the least prime factor lpf(M), and ω(M).

## 2. gcd(N, M) = 1 (verified)

Every nontrivial derived modulus is coprime to N: gcd(N, N±1) = gcd(N, 2N±1) =
gcd(N, N²+1) = gcd(N, Φ₃(N)) = 1. Only the trivial N²+N has gcd = N (no new
information). A derived modulus helps only if it shares a prime with N — by
construction the nontrivial ones don't.

## 3. The invariants are N-only (verified)

1. **C(M) is a function of N:** corr(C(M), N) = 0.66–0.95 across a 28-semiprime
   wide batch. The apparent corr(C(M), p) and corr(C(M), p+q) are the N-confound
   (p ≈ √N varies with N over the wide range).
2. **The factor-specific coordinate is noise:** corr(C(M), |p−q|) falls inside
   the permutation null in every case (wide-band pct 0.26–0.99; residual-control
   n=40: lpf and ω of 2N±1, Φ₃ all pass, obs ≤ 0.26 vs 95th ≈ 0.29–0.31).
3. **Degeneracy:** N±1 are always even, so lpf(N±1) = 2 (constant).

## 4. Why it collapses (barrier 1 + 5 + 4)

1. **Barrier 1 (polynomial barrier):** M = poly(N), and any polynomial invariant
   of M is determined by M, hence by N. N-explicit moduli share only finitely
   many primes with N (verified: none). The LLL prediction is confirmed exactly.
2. **Barrier 5:** the invariants are deterministic functions of N.
3. **Barrier 4:** computing C(M) for the large moduli (N²+1 ~ N², Φ₃ ~ N²)
   requires M's own fresh factorization — as hard as factoring a number of the
   same size as N² (worse than factoring N itself).

## 5. Conclusion

MULTIMOD closes the multi-modulus corner. Derived moduli M = poly(N) carry no
factor signal about N's factors: they are coprime to N (sharing nothing), their
invariants are functions of N (barrier 5), and computing the large-M invariants
costs a fresh factorization (barrier 4). The only way a second modulus helps is
an EXTERNAL hint sharing a prime with N — the hint-amplification frontier. The
round-13 list is now nearly complete (HALFPLANE, RANDOM-BQF, FETQ, CONDORDER,
JACSIGN, KPOWER, MULTIMOD tested). The classical, uniform, hint-free surface
remains exhausted.

---

**Experiment:** 375 (MULTIMOD). **Scripts:** /tmp/exp_multimod.py,
/tmp/exp_multimod3.py. **Assessment:** v151.
**Barrier verdict:** REFUTED — barrier 1 + 5 + 4.

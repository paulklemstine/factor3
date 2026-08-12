# The Jacobi-Signed Circle Count Escapes the Residue Dial, at the Weil Floor

**Program:** Factoring research lab — free-witness taxonomy extension
**Date:** 2026-08-11
**Status:** Decisive negative result with positive content — the first
character-weighted free-witness shown to escape the residue-dial collapse; its
factor-dependence is bounded by the Weil character-sum bound

---

## Abstract

Every character-weighted free-witness tested before (CIRC, BQF, GSP) collapsed to
a residue dial — a function of N mod 4 / N mod 8. This paper tests the Jacobi
symbol weight on the circle solution set: W(N) = Σ_{(x,y)∈S} (x/N) for S =
{x²+y²≡1 mod N}. Machine-verified: W(N) = W(p)·W(q) where W(p) = Σ_x (x/p)(1−x²/p)
is a cubic character sum — and W(p) does NOT depend on p mod 8 alone (p ≡ 1 mod 8
gives −2, −10, 6, −18, 14, 22 across p). W(N) therefore varies within N mod 8
classes (N ≡ 5 mod 8: 0, −52, −900, −484). **The character weight escapes the
residue-dial structure.** But: W(N) is uncorrelated with all trace coordinates
(p, q, p+q, |p−q|; permutation nulls pass), |W(p)| ≤ 2√p by the Weil bound
(verified exactly, with many attainments), so |W(N)| ≤ 4√N — the noise floor in
its sharpest character-sum form. Computing W(N) costs O(N); the product form is
symmetric (barrier 2). The new taxonomy entry: character-weighted, non-dial, at
the Weil floor.

---

## 1. The object and its factorization

For the circle S = {(x,y) mod N : x²+y² ≡ 1 mod N}, define

    W(N) = Σ_{(x,y)∈S} (x/N).

Since (x/N) = (x_p/p)(x_q/q) for x = CRT(x_p, x_q), the weight factorizes and

    W(N) = W(p)·W(q),   W(p) = Σ_{(x,y)∈S_p} (x/p).

Counting y's for each x (the count is 1 + (1−x²/p)) and using Σ_x (x/p) = 0,

    W(p) = Σ_{x mod p} (x/p)(1−x²/p) = Σ_x χ(x)χ(1−x)χ(1+x),

a cubic character sum. Verified: W(N) = W(p)·W(q) on all tested semiprimes.

## 2. It is NOT a residue dial (verified)

If W were a residue dial, W(p) would be a function of p mod 8 (the only
characters are mod 4 and mod 8 for quadratic characters). It is not:

    p ≡ 1 mod 8: W(p) ∈ {−2, −10, 6, −18, 14, 22}
    p ≡ 5 mod 8: W(p) ∈ {2, −6, 10, −14, 10, 2}

Consequently W(N) varies within N mod 8 classes: N ≡ 1 mod 8 → {0, −12};
N ≡ 5 mod 8 → {0, −52, −900, −484}. This distinguishes JACSIGN from CIRC, BQF,
GSP (all residue dials). The character weight genuinely encodes factor-specific
data that no residue formula sees.

## 3. But it sits at the Weil floor (verified)

Across 40 semiprimes (N ∈ [37K, 397K]): corr(W, p), corr(W, q), corr(W, p+q),
corr(W, |p−q|) all fall inside the 300-shuffle permutation null (obs ≤ 0.22,
95th ≈ 0.28–0.31) — the factor-dependence is unstructured. Its magnitude obeys
the Weil bound |W(p)| ≤ 2√p exactly (verified on 19 primes; p=173 → 26 = 2·13,
p=293 → 34 = 2·17 attained), hence |W(N)| ≤ 4√N — the O(√N) noise floor in its
sharpest character-sum form. Median |W(N)| = 0 (W(p) = 0 for p ≡ 3, 7 mod 8,
half of primes).

## 4. Why it is sealed (barrier 4 + barrier 2 + noise floor)

1. **Barrier 4:** computing W(N) requires the O(N) sum Σ_{x mod N} (x/N)(1−x²/N)
   (or O(√N) with p, q known — circular). There is no free path to W(N).
2. **Barrier 2 (symmetry):** W(N) = W(p)·W(q) is a product; the factors are
   inseparable (swapping p,q leaves W(N) unchanged). No asymmetric handle.
3. **Noise floor:** the factor-dependence is bounded by the Weil bound, |W(N)| ≤
   4√N, i.e. relative density ~1/√N — the character-sum form of the noise-floor
   principle.

## 5. Conclusion

JACSIGN is the first character-weighted free-witness shown to escape the
residue-dial structure: its value genuinely depends on the individual factors
beyond N mod 8. Yet the escape lands at the Weil bound — the factor-dependence is
O(√N), uncorrelated with trace coordinates, symmetric, and O(N)-sealed. The new
taxonomy entry "character-weighted, non-dial, at the Weil floor" sharpens the
noise-floor principle: even when a character weight breaks the dial collapse, the
signal is bounded by the sharpest character-sum estimate. The classical, uniform,
hint-free surface remains exhausted.

---

**Experiment:** 373 (JACSIGN). **Scripts:** /tmp/exp_jacsign.py,
/tmp/exp_jacsign2.py. **Assessment:** v149.
**Barrier verdict:** REFUTED as a method — barrier 4 + 2 + Weil noise floor.

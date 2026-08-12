# The Factoring Function Is Spectrally Flat: EMPIRICAL-DEGREE, Closed

**Program:** Factoring research lab — barrier 1/2 probe at the Walsh level (round-14 #12)
**Date:** 2026-08-12
**Status:** Decisive negative with positive content — the bits of the smaller
factor admit NO low-degree GF(2) parity of N's bits (Walsh spectrum flat at
the finite-prime noise floor), the sole structure being the symmetric top-bit
magnitude/carry family; the round-1 "j=2 anomaly" is resolved as a small-k
fluctuation of that symmetric family, decaying with k

---

## Abstract

Over the exact k-bit-prime semiprime support, let f_j(N) = bit j of the smaller
factor p. Is f_j approximated by any low-degree parity S·N (|S| ≤ 3) of the
bits of N? Full fast-Walsh-Hadamard enumeration at k = 10 and 12, plus targeted
degree-≤3 scans at k = 14 (m up to 380 628 semiprimes, n = 2k input bits),
with a random-sign null calibrated at every size: **yes for the top bits, no for
everything else.** The bits j = k−2, k−3, … (the top ~6 bits of p) carry the
stable symmetric magnitude/carry structure — corr(p_{k−d}, N_{2k−1}) converges
across k to ≈ 0.28 (carry-out), 0.31, 0.13, 0.065, 0.026 for d = 2..6 — the
Walsh face of BITPROFILE's top-2 sliver. Every information-bearing bit below
the top ~6 is spectrally flat: at k = 14, max degree-≤3 correlation ≤ 0.021 vs
an all-parity noise floor 0.0101 and a degree-≤3 null max 0.0065, versus 0.03–
0.79 for the top-bit family. The round-1 "j=2 anomaly" (max |corr| = 0.166 at
k = 10, ~1.7× the noise floor) is **resolved**: it is the symmetric top-bit
magnitude/carry correlation of a low bit, and it decays with k —
corr(p₂, N_{2k−1}) = 0.254, 0.166, 0.013, 0.006 at k = 8, 10, 12, 14 — into the
noise floor. Small low-half cubic correlations at k = 12 (j = 3 ↔ {1,2,3},
0.036; j = 4 ↔ {1,3,4}, 0.042) decay by k = 14 to 0.013 / 0.009: finite-prime
equidistribution effects that slightly qualify the zero-block theorem (exact
only over the full-odd support, approximate — at the 1/√(#primes) discrepancy
scale — over the prime-restricted one), carrying ~10^(−3) bits. No low-degree
parity of N pins or narrows any factor bit: the factoring function has no
low-degree GF(2) structure beyond the symmetric size correlations computable
from N itself (barriers 1/2).

---

## 1. Setup

Semiprime support: N = p·q with p ≤ q both primes in [2^(k−1), 2^k). For each
bit j of p, the target function f_j(N) = (1 − 2·((p>>j)&1)) ∈ {±1} on the m
support points, 0 elsewhere on the 2^(2k)-bit domain. The (restricted) Walsh
coefficient at parity S ⊆ {0..2k−1} is W(S) = Σ_x f_j(x)·(−1)^{S·x}; normalized
correlation corr = |W(S)|/m. Full spectra by fast Walsh–Hadamard transform at
k = 10, 12; targeted degree-≤3 scans at k = 14 (no FWHT needed — direct O(m)
evaluation of the C(n,1)+C(n,2)+C(n,3) parities). Null: max degree-≤3
correlation of a random ±1 function on the same support (per-trial max over all
degree-≤3 masks), plus the all-parity extreme-value floor √(2 ln 2 · n/m).

## 2. The main table: per-bit max degree-≤3 correlation (verified)

k = 12 (m = 32 640, full FWHT); null max = 0.0213, all-parity noise = 0.0319:

| j | max | winner | j | max | winner |
|---|-----|--------|---|-----|--------|
| 0 | 1.000 | (constant bit) | 6 | 0.0436 | top {21,22} |
| 1 | 0.0276 | top {22,23} | 7 | 0.1018 | top {23} |
| 2 | 0.0398 | top {22,23} | 8 | 0.1501 | top {22,23} |
| 3 | 0.0362 | low {1,2,3} | 9 | 0.3384 | top {22} |
| 4 | 0.0420 | low {1,3,4} | 10 | 0.7896 | top {22,23} (carry-out) |
| 5 | 0.0309 | top {21,23} | 11 | 1.000 | (constant bit) |

k = 14 (m = 380 628, targeted scans; null max = 0.0065, all-parity noise =
0.0101): j = 2 → 0.0205 (top {25,27}), j = 6 → 0.0192 (constant-artifact),
j = 8 → 0.0729 (top {26,27}), j = 9 → 0.0726 (top {26}), j = 10 → 0.1408
(constant-artifact), j = 11 → 0.3214 (top {26}), j = 12 → 0.7756 (top {26,27}).

Reading: the constants j = 0, k−1 are trivial (corr 1.0 — p is odd, p ≥ 2^(k−1));
j = k−2 is the carry-out (0.79). The structure is entirely in the top-bit masks
{2k−1, 2k−2, 2k−3} — N's leading bits — and vanishes for j below the top ~6.
All information-bearing low/middle bits sit at or within a small factor of the
null.

## 3. The j=2 anomaly is resolved (verified)

The round-1 finding (max |corr| = 0.166 at k = 10, ~1.7× the all-parity floor,
degree 1/2/3 agreeing → a single-bit winner) is a correlation with N's leading
bit N_{2k−1} — the product-magnitude indicator 1[p·q ≥ 2^(2k−1)]. It is the
symmetric size correlation of a low bit, and it decays into the noise:

| parity | k=8 | k=10 | k=12 | k=14 | deg-≤3 null max (k) |
|--------|-----|------|------|------|---------------------|
| corr(p₂, N_{2k−1}) | 0.2536 | 0.1656 | 0.0132 | 0.0064 | 0.0213 (12), 0.0065 (14) |
| corr(p₂, N_{2k−1}N_{2k−2}) | 0.0652 | 0.0919 | 0.0398 | 0.0186 | 0.0213 (12), 0.0065 (14) |

The single-top-bit correlation is already below the null at k = 12; the top-2
parity decays 0.09 → 0.02. At k = 14 the best degree-≤3 parity for j = 2 is
0.0205 — 3× the null max, 2× the all-parity noise — a residue of the symmetric
top-bit family, not a persistent weak parity.

## 4. The stable structure: symmetric top-bit magnitude/carry family (verified)

corr(p_{k−d}, N_{2k−1}) converges across k for small d (distance from the top
of p):

| d | k=8 | k=10 | k=12 | k=14 |
|---|-----|------|------|------|
| 2 (carry-out) | 0.319 | 0.257 | 0.276 | 0.285 |
| 3 | 0.319 | 0.271 | 0.306 | 0.310 |
| 4 | 0.152 | 0.109 | 0.143 | 0.132 |
| 5 | 0.116 | 0.061 | 0.102 | 0.065 |
| 6 | — | 0.079 | 0.014 | 0.026 |
| 7+ | — | 0.011 | 0.018 | 0.009 |

The magnitude correlation is stable (~0.28–0.31 for d = 2, 3; ~0.13 for d = 4;
decaying for d ≥ 5) and, for a FIXED low bit, moves farther from the top as k
grows — which is why fixed bits like j = 2 lose it (their d = k−1−j grows).
This family is fully N-computable and symmetric in (p, q): it is a size
correlation ("N is large ⟹ the factors are large"), the Walsh face of the
BITPROFILE top-2 sliver and the j = k−2 carry-out. It cannot distinguish p from
q, pins nothing, and carries a vanishing fraction of H(p).

## 5. Low-half cubics: a qualifier on the zero-block, and its decay (verified)

corr(f_3, (−1)^{N₁+N₂+N₃}) = 0.2029, 0.0267, 0.0362, 0.0130 and
corr(f_4, (−1)^{N₁+N₃+N₄}) = 0.1449, 0.1004, 0.0420, 0.0087 across k = 8, 10,
12, 14. These small-k low-half correlations decay with k. The zero-block
theorem (I(p; N mod 2^(k−1)) = 0) is EXACT over the full-odd support (q → rq a
bijection on odd residues) but only approximate — at the 1/√(#k-bit primes)
prime-equidistribution discrepancy scale — over the prime-restricted support
used here. The residual low-half leak is real at small k (6–8σ for fixed masks
at k = 12) but carries ~10^(−3) bits and vanishes by k = 14.

## 6. Conclusion

EMPIRICAL-DEGREE confirms the spectral flatness of the factoring function at the
GF(2)/Walsh level: no parity of ≤ 3 bits of N approximates any factor bit, at
the largest exact-support sizes tested (k = 14, m = 380 628), except for the
symmetric top-bit magnitude/carry family of p's own top ~6 bits — which is
N-computable, symmetric, and non-factor-revealing (barrier 2). The "j=2
anomaly" and the low-half cubics are small-k finite-prime fluctuations of this
same symmetric family and of prime equidistribution, decaying into the noise
floor as k grows. This is the spectral face of superdensity (BITPROFILE): the
pairwise-invisible ~95% of factor information has no low-degree parity shadow
either — the factoring function is as far from a linear/quadratic/cubic GF(2)
approximator as a random function on its support, with the single exception of
the symmetric size correlations N itself already reveals. Consistent with
barriers 1/2 (no poly/LLL-style approximator; all N-computable structure is
symmetric) and 5 (orthogonality at the Walsh level). The classical, uniform,
hint-free surface remains exhausted.

---

**Experiment:** 388 (EMPIRICAL-DEGREE). **Scripts:** /tmp/exp_empiricaldegree.py,
/tmp/exp_empiricaldegree2.py, _3, _4, _5.
**Assessment:** v164. **Verdict:** CONFIRMED — information-bearing factor bits
are spectrally flat against every low-degree parity of N at the largest sizes;
the j=2 anomaly and low-half cubics resolve as symmetric-top-bit / finite-prime
correlations decaying with k (barriers 1/2); the sole non-flat structure is the
symmetric N-computable size/carry family (BITPROFILE's top-2 sliver restated).

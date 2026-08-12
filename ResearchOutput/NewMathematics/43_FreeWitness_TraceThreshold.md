# The Partial Free-Witness Threshold is the Trace, Closed

**Program:** Factoring research lab — barrier-4 boundary quantification (frontier i)
**Date:** 2026-08-11
**Status:** Decisive negative result with positive content — the factor-information
of a free witness is concentrated in its value mod (p+q); the aggregation cost is
independent of how much of the witness is needed

---

## Abstract

The free witness sigma_2(N) = (1+p²)(1+q²) factors N: s = (p+q)² =
sigma_2 − 1 + 2N − N², t = √s, and p,q are the roots of x² − t x + N (SIGK).
This paper quantifies how much of the witness is actually NEEDED — the boundary
of barrier 4. Machine-verified: given only sigma_2(N) mod m, the minimum modulus
for unique factorization is m* = Θ(p+q), the TRACE coordinate — m*/(p+q) = 5.00
exactly across all bit lengths 14–26 (window-dependent constant, trace order).
The factor-information of sigma_2 is concentrated in its value mod (p+q) — about
a quarter of the witness's bits. But computing sigma_2 mod m requires computing
sigma_2 (the full divisor sum), which is O(N)-sealed. **The trace is both the
only recoverable coordinate (trace lemma) and the modulus-threshold of the
witness's factor information; the aggregation cost is independent of how much is
needed.** Barrier 4 + trace-lemma consistency.

---

## 1. Setup

For N = pq, sigma_2(N) = (1+p²)(1+q²) (a free witness, paper 16 family). The
factorization pipeline: s = sigma_2 − 1 + 2N − N² = (p+q)²; t = √s = p+q;
p,q = roots of x² − t x + N. Full sigma_2 suffices (re-verified 24/24).

## 2. The partial threshold (verified)

Given only sigma_2(N) mod m, the candidate values of t = p+q satisfy t′² ≡ s mod
m, i.e. t′ ≡ ±(p+q) mod m. Over the candidate window [2√N, 4(p+q)], the
candidates are t′ = (p+q) + j·m. For j ≠ 0, the discriminant
disc(t′) = t′² − 4N = (p−q)² + 2jm(p+q) + j²m² is generically not a square —
so the true t (j = 0) is the unique factoring candidate once m spans the window.

Measured: the minimum m with exactly one factoring candidate in the window is
m* = 5·(p+q) — exactly 5.00×(p+q) across bit lengths 14–26 (the constant is
window-dependent; the ORDER is the trace). Hence **m* = Θ(p+q)**.

## 3. Interpretation

- **Information concentration:** sigma_2 ≈ N² has 2·log₂(N) bits; the needed
  modulus m* ≈ p+q has (1/2)log₂(N) + 1 bits — about a quarter. The factor
  information sits in the low ~¼ of the witness's bits.
- **Unbalanced case:** for p ≪ q, p+q ≈ N/p grows, so more bits are needed — the
  threshold is the trace coordinate in all cases.
- **Aggregation independence:** computing sigma_2 mod m requires computing
  sigma_2 (the full divisor sum) — O(N)-sealed (barrier 4). There is no cheaper
  path to the partial value.

## 4. Why it collapses (barrier 4 + trace lemma)

1. **Barrier 4:** the witness value is O(N)-sealed regardless of how many bits
   are needed; the threshold does not reduce the aggregation.
2. **Trace-lemma consistency:** the threshold IS the trace coordinate p+q —
   the one recoverable numeric witness. The trace is simultaneously the only
   coordinate AND the modulus-threshold of the witness's factor information.

## 5. Conclusion

QUERYWIT quantifies barrier 4's boundary: a free witness's factor-information is
concentrated in its value mod (the trace coordinate), yet computing any part of
the witness costs the full O(N) aggregation. This is frontier-(i) content: it
sharpens what a barrier-4 proof must show (the aggregation is irreducible even
for partial witness values) and confirms the trace lemma's role as the central
coordinate. The classical, uniform, hint-free surface remains exhausted.

---

**Experiment:** 378 (QUERYWIT). **Script:** /tmp/exp_querywit.py.
**Assessment:** v154. **Barrier verdict:** REFUTED — barrier 4 (+ trace-lemma
consistency); positive content: threshold = Θ(p+q).

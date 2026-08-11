# The Schinzel Circle: A Geometric Free-Witness for the Aggregation Barrier

**Program:** Factoring research lab — experiment SCHINZEL write-up
**Date:** 2026-08-11
**Status:** Negative-result paper with a new geometric picture of barrier 4

---

## Abstract

Schinzel's theorem (1958) states that for every positive integer n there is a
circle passing through exactly n lattice points. Explored as a factoring idea:
build the circle through exactly N = pq lattice points and use it to factor N.
The method is refuted — the radius is built from the target count N−1, never
from the factorization, and every route to a factor is trial-division-like. But
the exploration produces a genuinely NEW geometric picture of the free-witness
aggregation barrier (barrier 4): the Schinzel circle is a VISIBLE free witness
whose lattice points share factors with N at density ~4/sqrt(N). You can see the
factors geometrically; reading any single one off the circle still costs
O(sqrt(N)). This paper records the construction, the factor-leak observation,
and the honest verdict.

---

## 1. Schinzel's construction (verified)

For odd n = 2k+1: the circle centered at (1/3, 0) with equation
(3x − 1)² + (3y)² = 5^(2k) passes through exactly n lattice points.
For even n = 2k: the circle centered at (1/2, 0) with (2x − 1)² + (2y)² = 5^(k−1)
passes through exactly n lattice points.

Verified computationally: the count equals n for every n = 1..20. (Note: the
naive guess of center (1/2, 0) for odd n is wrong — half-integer x-centers force
an even count by reflection symmetry; the odd case needs the (1/3, 0) center.)

The count is achieved because 5^(n−1) has exactly n sum-of-two-squares
representations with the required congruence — a property of the count n alone.

---

## 2. The key structural fact: the radius never uses the factorization

For N = pq, the circle through exactly N lattice points has radius
R = 5^((N−1)/2)/3 — built from the EXPONENT N−1 (the target count), never from
p or q. Concretely:
- log₂ R = (N−1)/2 · log₂ 5 − log₂ 3 is exactly LINEAR in N.
- R is exponential (~1.16·N bits) — more than writing N itself.
- The N lattice points are a deterministic function of N alone.

The factorization of N never enters the construction. The radius and the point
set are N-only (barrier 5).

---

## 3. The new observation: the lattice points leak the factors at density ~4/sqrt(N)

The Schinzel circle's lattice points share factors with N at density
~2(p+q)/N ~ 4/sqrt(N). Reason: mod p, 5^(N−1) ≡ 5^(q−1) = (5^((q−1)/2))² is a
square, so ~2/p of the x-residues admit y ≡ 0 mod p — yielding ~2q points that
share the factor p. Measured: N=35 -> 26/35 points, N=77 -> 36/77, N=143 ->
24/143, N=221 -> 82/221, N=899 -> 208/899.

**The geometric free-witness.** A randomized algorithm: pick a random Gaussian
index j, compute the lattice point mod 3N (poly(log N) fast exponentiation of
(1+2i)^j (1−2i)^(N−1−j), with the mod-3N lift making the /3 center-shift
division well-defined), and take gcd with N. Success ~ 4/sqrt(N) per trial, so
O(sqrt(N)) expected = exactly trial division, no speedup. (Heuristic: N=3599 =
59·61 has 119 leaking points but all with gcd = N — no proper factor.)

---

## 4. A visible picture of barrier 4

The Schinzel circle turns the free-witness aggregation barrier into a VISIBLE
object: a circle whose lattice points factor N at density ~4/sqrt(N). The
witnesses are literally drawn in the plane — you can see the factors. But
reading any single factor-bearing point off the circle still costs O(sqrt(N)):
the points are enumerated by the Gaussian-index structure, and harvesting the
leak is a random sample over ~sqrt(N) candidates.

This is the aggregation barrier made geometric: the witness is present,
visible, and dense enough to see — yet each extraction is a trial division.

---

## 5. Connection to the free-witness classification

The r_2(N²) count (lattice points on x² + y² = N²) is 4·3^a where
a = #{p, q ≡ 1 mod 4}: it distinguishes N = 209 = 11·19 (count 4) from
N = 221 = 13·17 (count 36) at near-equal N. This is a free-witness for factor
residues mod 4, squarely in the CIRC/BQF/GAU family (barrier 4/6), consistent
with the CRT-multiplicative classification (paper 16) and its trace lemma.

The Schinzel circle adds a SIXTH-plus geometric setting to the free-witness
family: after norm-counts, group-order counts, quadratic-form counts,
group-class counts, modular indices, and code distances, the circle gives a
geometric lattice-point leak.

---

## 6. Honest verdict

**Refuted as a factoring method.** Everything reduces to established barriers:
- barrier 4 (the O(N) lattice points, or O(sqrt(N)) sampling to harvest the leak),
- barrier 5 (the radius/point-set are N-only),
- barrier 6 (the count formula needs the divisor structure).

**Genuinely new.** A crisp geometric picture of barrier 4: the free witness is
literally a visible circle whose points factor N at density ~4/sqrt(N). This
connects to the lab's "density = random" findings (Berggren tree) and adds a
geometric member to the free-witness family.

---

## 7. Conclusion

Schinzel's theorem, applied to factoring, is a valid construction that yields a
circle through exactly N lattice points whose points leak the factors at random
density — but reading them costs O(sqrt(N)), exactly trial division. The method
is refuted; the geometric picture of the aggregation barrier is new and sharp.
The barrier framework holds: 320 experiments, and the free witness can now be
SEEN.

---

*Related:* `16_FreeWitness_Classification.md` (the classification),
`13_FreeWitness_Family.md`, `Factoring_Lab_Notebook.md` Part 62 (experiment
SCHINZEL), `00_CONSOLIDATED_BREAKTHROUGH_REPORT.md`.

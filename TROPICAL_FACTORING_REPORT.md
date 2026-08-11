# Tropical-Geometric Invariants as Factoring Signals — Final Report

## Summary

Tested whether tropical-geometric invariants encode factors of semiprimes N = pq.
**Result: a genuine signal exists (the tropical corner locus hull encodes the larger
factor), but extracting it requires O(N log N) time = O(2^n) in the bit length n,
i.e., exponential and no better than trial division. No polynomial-time signal was found.**

The Bergman fan / CornerLocusProduct / Concept lattice / Intersection-theory invariants
either (a) reduce to the divisor count d(N), which for semiprimes is the constant 4 and
reveals nothing, or (b) encode factors but require exponential time to read.

---

## What was tested

All invariants were computed for N = 65, 221, 493, 1189, 3233, 9797 (plus 15, 35,
1003, 2047 for robustness). Code in `tropical_factoring.py` and `tropical_hull_verify.py`.

### Invariant 1 — 1D tropical corner locus of f(x) = min_k((N mod k) + kx)

The corner locus is the set of x where the min is attained >= twice. Its breakpoints
are the interior vertices of the **lower convex hull** of the point set
P_N = {(k, N mod k) : k = 0, 1, ..., N-1}.

**Finding (confirmed for all 10 semiprimes):** The lower convex hull of P_N is always
the triangle with vertices

    (0, 0),  (q, 0),  (N-1, 1)

where **q is the larger prime factor** of N = pq.

So the middle hull vertex's x-coordinate IS the larger factor. The breakpoint of the
corner locus falls exactly at x = q.

**Why this works:** N mod k = 0 iff k divides N. The divisor points (d, 0) sit on the
x-axis. The lower hull from the origin reaches the x-axis at the *farthest* divisor
point, which is (q, 0) with q = max factor. The other hull vertex (N-1, 1) comes from
N mod (N-1) = 1.

**Complexity:** Computing the convex hull of N points takes O(N log N) time. Since N ≈ 2^n
for n-bit N, this is **exponential in the bit length**. Equivalent to trial division.

### Invariant 2 — Zero-divisor count Z(N) = #{a ∈ [1,N-1] : gcd(a,N) > 1}

Z(N) = N - 1 - φ(N) = p + q - 2 for semiprimes. So Z(N) + 2 = p + q, and combined with
N = pq, the quadratic formula t² - (p+q)t + pq = 0 gives complete factorization.

**Complexity:** Computing Z(N) requires O(N) gcd computations = O(N log N) time =
**exponential in bit length.** Same complexity class as trial division.

### Invariant 3 — Lattice count L(N) = Σ_{x=0}^{N-1} gcd(x,N)

L(N) = 4N - 2(p+q) + 1 for semiprimes (verified). This is equivalent information to Z(N).
**gcd(L(N), N) does NOT reliably reveal a factor** — it only does so by coincidence
(e.g., N=65 gives gcd=5, but N=221 gives gcd=1). The condition p | L(N) is equivalent
to 2q ≡ 1 (mod p), which holds only for special pairs.

### Invariant 4 — 2D tropical curve ray count of F(X,Y) = min_{d|N}(dX + (N/d)Y)

The tropical curve has one ray per edge of the convex hull of {(d, N/d) : d|N}. Since
the hyperbola xy = N is strictly convex, all d(N) divisor points are extreme, so the
ray count = **d(N) = number of divisors**. For semiprimes this is always 4 — reveals
nothing about the actual factors.

### Invariant 5 — Concept lattice size of the divisibility context

Context: (divisors of N, divisors of N, "divides"). A concept is a pair (A,B) with
B = A' = multiples of lcm(A), A = B' = divisors of gcd(B). The concept lattice size
equals **d(N)** (verified by exhaustive enumeration). Same information as Invariant 4 —
does not reveal factors.

### Invariant 6 — Standard tropical line lattice count

Count of lattice points on V(min(x,y,0)) in a bounded box. Independent of N's factors.
Not a signal.

---

## Summary table

| N     | p×q      | Hull vertices         | Middle vertex = larger factor | Z(N)=p+q-2 | d(N) |
|-------|----------|-----------------------|-------------------------------|------------|------|
| 65    | 5×13     | (0,0),(13,0),(64,1)  | 13 ✓                          | 16         | 4    |
| 221   | 13×17    | (0,0),(17,0),(220,1) | 17 ✓                          | 28         | 4    |
| 493   | 17×29    | (0,0),(29,0),(492,1) | 29 ✓                          | 44         | 4    |
| 1189  | 29×41    | (0,0),(41,0),(1188,1)| 41 ✓                          | 68         | 4    |
| 3233  | 53×61    | (0,0),(61,0),(3232,1)| 61 ✓                          | 112        | 4    |
| 9797  | 97×101   | (0,0),(101,0),(9796,1)| 101 ✓                        | 196        | 4    |

---

## Honest conclusion

**Did I find a genuine factor signal?** Yes — the tropical corner locus hull of
{(k, N mod k)} encodes the larger factor q as the x-coordinate of its middle vertex.
This holds for all 10 semiprimes tested. It is a real structural theorem.

**What's the complexity?** O(N log N) = **O(2^n)** where n = bit length of N. This is
exponential, not polynomial. It is asymptotically equivalent to trial division.

**Why this is not a breakthrough:** The hull computation requires processing all N points
(k, N mod k) for k = 0,...,N-1. There is no known way to find the farthest divisor
point on the x-axis without essentially finding a divisor, which is the factoring problem
itself. The tropical structure *describes* the factorization (the corner locus "knows"
the factors via the CornerLocusProduct theorem, the tropical analog of "zero set of a
product = union of zero sets") but does not *shortcut* it.

**The structural barrier (consistent with the memory note on this project):** Tropical
geometry provides a faithful *interpretation* of factoring — the Bergman fan and corner
locus structures encode divisor information — but reading this information requires
Ω(N) = Ω(2^n) steps. This is the same barrier that appears across factoring paradigms:
the information is present in the structure, but extracting it is as hard as the original
problem. No polynomial-time tropical factoring algorithm was found.

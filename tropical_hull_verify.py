#!/usr/bin/env python3
"""
Verify and analyze the key structural finding:
The lower convex hull of {(k, N mod k) : k = 0,...,N-1} for semiprime N = pq
is always the triangle with vertices (0,0), (q,0), (N-1,1),
where q is the LARGER factor.

This means the tropical corner locus of f(x) = min_k((N mod k) + kx)
has its breakpoint at x determined by the larger factor q.

We verify this and analyze the complexity honestly.
"""

import math
import time

SEMIPRIMES = {
    65: (5, 13),
    221: (13, 17),
    493: (17, 29),
    1189: (29, 41),
    3233: (53, 61),
    9797: (97, 101),
    # Add a couple more for robustness
    15: (3, 5),
    35: (5, 7),
    1003: (17, 59),
    2047: (23, 89),  # note: 2047 = 23 * 89 (both prime)
}


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def lower_convex_hull(points):
    points = sorted(set(points))
    if len(points) <= 1:
        return points
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    return lower


def analyze_hull(N, p, q):
    """Analyze the lower convex hull of {(k, N mod k)}."""
    # Points (k, N mod k) for k = 0,...,N-1, with N mod 0 := 0
    points = [(0, 0)] + [(k, N % k) for k in range(1, N)]
    hull = lower_convex_hull(points)

    # The hull should be (0,0), (q,0), (N-1,1) where q = max(p,q)
    expected_mid = (max(p, q), 0)
    expected_last = (N - 1, 1)

    print(f"\nN = {N} = {p} x {q}")
    print(f"  Hull vertices: {hull}")
    print(f"  Expected: [(0,0), ({max(p,q)},0), ({N-1},1)]")

    # Check structure
    assert hull[0] == (0, 0), f"First vertex should be (0,0), got {hull[0]}"
    assert hull[-1] == (N - 1, 1), f"Last vertex should be ({N-1},1), got {hull[-1]}"

    # The middle vertex (if exists) should be (q, 0) where q is the larger factor
    if len(hull) == 3:
        mid = hull[1]
        print(f"  Middle vertex: {mid}")
        if mid == expected_mid:
            print(f"  *** CONFIRMED: middle vertex x-coord = {mid[0]} = larger factor q = {max(p,q)} ***")
        else:
            print(f"  *** UNEXPECTED: middle vertex is {mid}, expected {expected_mid} ***")
    elif len(hull) > 3:
        print(f"  *** Hull has {len(hull)} vertices (more than 3) ***")
        # Find the vertex at y=0 (other than origin)
        y0_vertices = [v for v in hull if v[1] == 0 and v[0] > 0]
        print(f"  Vertices at y=0 (excluding origin): {y0_vertices}")
        if y0_vertices:
            rightmost_y0 = max(v[0] for v in y0_vertices)
            print(f"  Rightmost y=0 vertex: x = {rightmost_y0}")
            if rightmost_y0 == max(p, q):
                print(f"  *** This equals the larger factor q = {max(p,q)} ***")
    else:
        print(f"  Hull has only {len(hull)} vertices")

    # The breakpoint of the corner locus
    # The corner locus breakpoint is at the x where the two hull edges meet,
    # i.e., at the middle vertex x-coordinate = q
    # The breakpoint x-value: intersection of lines from hull vertices
    if len(hull) >= 3:
        # Breakpoint is at the middle vertex
        breakpoint_x = hull[1][0]  # x-coordinate of middle vertex
        print(f"  Corner locus breakpoint at x = {breakpoint_x}")
        print(f"  This breakpoint x-coordinate IS the larger factor q = {max(p,q)}")

    return hull


def verify_zero_divisor_formula(N, p, q):
    """Verify L(N) = sum_{x=0}^{N-1} gcd(x,N) = 4N - 2(p+q) + 1 for semiprime."""
    L = sum(math.gcd(x, N) for x in range(N))
    formula = 4 * N - 2 * (p + q) + 1
    print(f"\n  L(N) = sum gcd(x,N) = {L}, formula 4N-2(p+q)+1 = {formula}, match: {L == formula}")
    print(f"  gcd(L, N) = {math.gcd(L, N)}")
    # L mod p = (4N - 2(p+q) + 1) mod p = (0 - 0 - 2q + 1) mod p = (1 - 2q) mod p
    L_mod_p = (1 - 2 * q) % p
    L_mod_q = (1 - 2 * p) % q
    print(f"  L mod p = {L_mod_p} (p | L iff this is 0, i.e., 2q = 1 mod p)")
    print(f"  L mod q = {L_mod_q} (q | L iff this is 0, i.e., 2p = 1 mod q)")
    return L


def complexity_analysis():
    """Honest complexity analysis."""
    print("\n" + "=" * 70)
    print("COMPLEXITY ANALYSIS")
    print("=" * 70)
    print("""
1. TROPICAL CORNER LOCUS HULL — encodes larger factor q:
   - The lower convex hull of {(k, N mod k)} has middle vertex (q, 0).
   - Computing the hull requires processing N points: O(N log N) time.
   - N has n = log2(N) bits, so O(N) = O(2^n) — EXPONENTIAL in bit length.
   - This is equivalent to trial division in complexity.
   - The "signal" is genuine but the computation is not efficient.

   Why does this work? N mod k = 0 iff k | N. The divisor points (d, 0) lie on
   the x-axis. The lower hull from (0,0) reaches the x-axis at the FARTHEST
   divisor point, which is (q, 0) where q is the larger factor. Beautiful
   structure, but finding it requires scanning all k < N.

2. ZERO-DIVISOR COUNT Z(N) = p + q - 2:
   - Genuine signal: Z(N) + 2 = p + q, and with N = pq, quadratic formula
     gives complete factorization.
   - Computing Z(N) requires O(N) gcd computations = O(N log N) time.
   - Again exponential in bit length. Equivalent to trial division.

3. LATTICE COUNT L(N) = sum gcd(x,N) = 4N - 2(p+q) + 1:
   - Also a genuine signal (equivalent to Z(N) since L and Z determine each other).
   - Computing L(N) is O(N log N). Same complexity class.
   - gcd(L(N), N) does NOT reliably reveal a factor (only by coincidence).

4. 2D TROPICAL CURVE RAY COUNT = d(N):
   - Equals the number of divisors. For semiprimes, always 4.
   - Does not distinguish between different semiprimes.

5. CONCEPT LATTICE SIZE = d(N):
   - Same as divisor count. Does not reveal factors.

CONCLUSION: Tropical geometry provides a FAIR INTERPRETATION of factoring:
the tropical corner locus of {(k, N mod k)} "knows" the factors (the hull
vertices are at divisor positions), but reading this information requires
O(N) work. The CornerLocusProduct theorem (Corner(f*g) = Corner(f) U Corner(g))
is the tropical analog of "zero set of a product is the union of zero sets" —
it describes structure but doesn't shortcut factorization. The fundamental
barrier remains: any method that reads off a factor from a structure indexed
by k = 1,...,N requires Omega(N) = Omega(2^n) steps in the worst case.
""")


def main():
    print("=" * 70)
    print("VERIFICATION: Tropical corner locus hull encodes the larger factor")
    print("=" * 70)

    for N, (p, q) in SEMIPRIMES.items():
        analyze_hull(N, p, q)
        verify_zero_divisor_formula(N, p, q)

    complexity_analysis()

    # Final verification: can we extract the factor from the hull in O(N log N)?
    print("\n" + "=" * 70)
    print("DEMONSTRATION: Extracting the factor from the tropical hull")
    print("=" * 70)
    for N, (p, q) in SEMIPRIMES.items():
        points = [(0, 0)] + [(k, N % k) for k in range(1, N)]
        hull = lower_convex_hull(points)
        # The rightmost vertex at y=0 (excluding origin) gives the larger factor
        y0 = [v[0] for v in hull if v[1] == 0 and v[0] > 0]
        if y0:
            larger_factor = max(y0)
            smaller = N // larger_factor
            print(f"  N = {N}: hull gives larger factor = {larger_factor}, "
                  f"smaller = {smaller}, "
                  f"verification: {larger_factor} x {smaller} = {larger_factor * smaller}, "
                  f"correct: {larger_factor * smaller == N}")


if __name__ == "__main__":
    main()

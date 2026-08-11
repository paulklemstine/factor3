#!/usr/bin/env python3
"""
Explore tropical-geometric invariants as factoring signals.

Tests whether tropical-geometric invariants encode factors of semiprimes N = pq.

Mathematical background (from the Lean catalog):
- BergmanFan: Bergman fan of a matroid = {w : every circuit minimum attained >= twice}
- CornerLocusProduct: Corner(f * g) = Corner(f) U Corner(g)  (tropical product)
- AnalogyConceptLattice: concept lattice of a formal context via Galois connection
- IntersectionTheory: tropical Bezout, tropicalization correspondence

We test these invariants:
  1. Zero-divisor count mod N  (tropical hypersurface xy = 0 "wrapped mod N")
  2. 1D tropical corner locus vertex count of f(x) = min_k ((N mod k) + k*x)
  3. 2D tropical curve ray count of F(X,Y) = min_{d|N} (d*X + (N/d)*Y)
  4. Concept lattice size of the divisibility context on divisors of N
  5. Divisor count d(N) and related arithmetic functions
  6. Lattice-point counts on tropical varieties in bounded boxes
"""

import math
import time

# ============================================================
# Test semiprimes
# ============================================================
SEMIPRIMES = {
    65: (5, 13),
    221: (13, 17),
    493: (17, 29),
    1189: (29, 41),
    3233: (53, 61),
    9797: (97, 101),
}


# ============================================================
# Basic arithmetic helpers
# ============================================================
def divisors(n):
    """Return sorted list of divisors of n."""
    divs = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            divs.append(i)
            if i != n // i:
                divs.append(n // i)
        i += 1
    return sorted(divs)


def prime_power_factor_count(n):
    """Omega(n): total number of prime factors with multiplicity."""
    count = 0
    p = 2
    while p * p <= n:
        while n % p == 0:
            count += 1
            n //= p
        p += 1
    if n > 1:
        count += 1
    return count


# ============================================================
# Convex hull (monotone chain)
# ============================================================
def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def lower_convex_hull(points):
    """Lower convex hull of points (x,y). Returns hull vertices left to right."""
    points = sorted(set(points))
    if len(points) <= 1:
        return points
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    return lower


def upper_convex_hull(points):
    """Upper convex hull of points (x,y). Returns hull vertices left to right."""
    points = sorted(set(points))
    if len(points) <= 1:
        return points
    upper = []
    for p in points:
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) >= 0:
            upper.pop()
        upper.append(p)
    return upper


def convex_hull(points):
    """Full convex hull (lower + upper, without duplicating endpoints)."""
    lower = lower_convex_hull(points)
    upper = upper_convex_hull(points)
    return lower[:-1] + upper[:-1]


# ============================================================
# Test 1: Zero-divisor count mod N
# The "tropical hypersurface xy = 0 mod N" wrapped around.
# Z(N) = #{a in {1,...,N-1} : gcd(a,N) > 1} = N - 1 - phi(N)
# For N = pq: Z(N) = p + q - 2
# ============================================================
def count_zero_divisors(N):
    """Count a in {1,...,N-1} with gcd(a,N) > 1. O(N log N)."""
    count = 0
    for a in range(1, N):
        if math.gcd(a, N) > 1:
            count += 1
    return count


def zero_divisor_hypersurface_lattice_count(N, B):
    """
    Count lattice points (x,y) in [0,B-1]^2 with (x*y) mod N == 0.
    This is the "tropical hypersurface xy = 0 mod N" in a bounded box.
    For B = N, this counts all pairs in (Z/NZ)^2 with xy = 0.
    """
    count = 0
    for x in range(B):
        for y in range(B):
            if (x * y) % N == 0:
                count += 1
    return count


# ============================================================
# Test 2: 1D tropical corner locus
# f(x) = min_{k=0}^{N-1} ((N mod k) + k*x), with N mod 0 := 0.
# The corner locus is where the min is attained >= twice.
# Its vertices = breakpoints of the lower envelope
#            = interior vertices of lower convex hull of {(k, N mod k)}.
# ============================================================
def tropical_corner_locus_1d(N):
    """
    Returns (num_vertices, hull_vertex_count, hull_points).
    num_vertices of corner locus = len(lower_hull) - 2
    (interior breakpoints; the two endpoints are at infinity in the tropical sense).
    """
    points = [(0, 0)] + [(k, N % k) for k in range(1, N)]
    hull = lower_convex_hull(points)
    # breakpoints = interior hull vertices
    num_breakpoints = max(0, len(hull) - 2)
    return num_breakpoints, len(hull), hull


# ============================================================
# Test 3: 2D tropical curve from divisor polynomial
# F(X,Y) = min_{d|N} (d*X + (N/d)*Y).
# This is a tropical curve (fan) in R^2.
# Number of rays = number of edges of convex hull of {(d, N/d)}.
# For points on hyperbola xy=N (strictly convex), all d(N) points are hull vertices,
# so number of rays = d(N).
# ============================================================
def tropical_curve_2d_ray_count(N):
    """Number of rays of the tropical curve min_{d|N}(d*X + (N/d)*Y)."""
    divs = divisors(N)
    points = [(d, N // d) for d in divs]
    # The tropical curve rays correspond to edges of the convex hull of these points.
    # Since xy = N is strictly convex, all points are extreme.
    hull = convex_hull(points)
    return len(hull)  # number of edges = number of vertices of convex hull


# ============================================================
# Test 4: Concept lattice of the divisibility context
# Context: (divisors of N, divisors of N, |) where | means "divides".
# A concept is (A,B) with A'=B, B'=A where
#   A' = {d : forall a in A, a|d} = multiples of lcm(A) within divisors
#   B' = {d : forall b in B, d|b} = divisors of gcd(B)
# The concept lattice size equals d(N) (number of divisors).
# ============================================================
def concept_lattice_size(N):
    """
    Compute the size of the concept lattice of the divisibility context on divisors of N.
    Context: objects = attributes = divisors of N; relation = 'divides'.
    A concept (A,B): B = A' = {d|N : lcm(A)|d}, A = B' = {d|N : d|gcd(B)}.
    """
    divs = divisors(N)
    div_set = set(divs)

    def prime_factorize(n):
        """Return dict prime->exponent for n."""
        fac = {}
        p = 2
        while p * p <= n:
            while n % p == 0:
                fac[p] = fac.get(p, 0) + 1
                n //= p
            p += 1
        if n > 1:
            fac[n] = fac.get(n, 0) + 1
        return fac

    # Divisor lattice via prime exponents
    fac_N = prime_factorize(N)
    primes = sorted(fac_N.keys())

    def lcm_of_subset(subset):
        """LCM of a subset of divisors."""
        if not subset:
            return 1
        max_exp = {}
        for d in subset:
            fac_d = prime_factorize(d)
            for p, e in fac_d.items():
                max_exp[p] = max(max_exp.get(p, 0), e)
        lcm_val = 1
        for p, e in max_exp.items():
            lcm_val *= p ** e
        return lcm_val

    def gcd_of_subset(subset):
        """GCD of a subset of divisors."""
        if not subset:
            return 0  # gcd of empty set: convention
        g = subset[0]
        for d in subset[1:]:
            g = math.gcd(g, d)
        return g

    concepts = set()
    # Enumerate all subsets A of divisors
    m = len(divs)
    for mask in range(1 << m):
        A = [divs[i] for i in range(m) if mask & (1 << i)]
        # B = A' = {d|N : lcm(A) | d}
        if not A:
            lcm_A = 1
        else:
            lcm_A = lcm_of_subset(A)
        B = tuple(d for d in divs if d % lcm_A == 0)
        # A_check = B' = {d|N : d | gcd(B)}
        if not B:
            gcd_B = 0
        else:
            gcd_B = math.gcd(*B) if len(B) > 1 else B[0]
        A_check = tuple(d for d in divs if gcd_B % d == 0) if gcd_B > 0 else ()
        if tuple(A) == A_check:
            concepts.add((tuple(A), B))
    return len(concepts)


# ============================================================
# Test 5: Lattice points on tropical variety in bounded box
# The tropical variety of f(x,y) = min(x, y, 0) is the standard tropical line
# (three rays from origin). We count lattice points on it in [-B, B]^2.
# For the "mod N" version, we count (x,y) in [0,N-1]^2 satisfying
# tropical conditions mod N.
# ============================================================
def tropical_line_lattice_count(B):
    """
    Count lattice points on the standard tropical line
    V(min(x,y,0)) = {(x,y) : min(x,y,0) attained >= twice} in [-B,B]^2.
    This is the union of three rays: {x=y<=0}, {x=0,y>=0}, {y=0,x>=0}.
    """
    count = 0
    for x in range(-B, B + 1):
        for y in range(-B, B + 1):
            vals = [x, y, 0]
            min_val = min(vals)
            if sum(1 for v in vals if v == min_val) >= 2:
                count += 1
    return count


def tropical_product_lattice_count(N, B):
    """
    Count (x,y) in [0,B-1]^2 where the tropical product condition holds:
    min(x+y, N) is attained twice, i.e., x+y = N (the tropical hypersurface xy=N).
    In the bounded box, this is the line x+y=N intersected with [0,B-1]^2.
    """
    count = 0
    for x in range(B):
        for y in range(B):
            if x + y == N:
                count += 1
    return count


# ============================================================
# Main computation
# ============================================================
def check_factor_signal(name, value, N, p, q):
    """Check if gcd(value, N) or gcd(value +/- 1, N) reveals a factor."""
    results = []
    for label, val in [("v", value), ("v-1", value - 1), ("v+1", value + 1),
                       ("v-2", value - 2), ("v+2", value + 2)]:
        if val > 0:
            g = math.gcd(val, N)
            if 1 < g < N:
                results.append(f"  *** FACTOR: gcd({name}={label}, N) = {g} ***")
    if not results:
        results.append(f"  No factor revealed by gcd(value+k, N) for k in [-2,2]")
    return "\n".join(results)


def main():
    print("=" * 80)
    print("TROPICAL-GEOMETRIC INVARIANTS AS FACTORING SIGNALS")
    print("=" * 80)

    # Collect data for summary
    all_data = []

    for N, (p, q) in SEMIPRIMES.items():
        print(f"\n{'='*60}")
        print(f"N = {N} = {p} x {q}")
        print(f"{'='*60}")
        data = {"N": N, "p": p, "q": q}

        # --------------------------------------------------------
        # Test 1: Zero-divisor count
        # --------------------------------------------------------
        print(f"\n--- Test 1: Zero-divisor count Z(N) ---")
        t0 = time.time()
        Z = count_zero_divisors(N)
        t1 = time.time()
        print(f"  Z(N) = {{a in [1,N-1] : gcd(a,N)>1}} = {Z}")
        print(f"  Theory: Z(N) = N - 1 - phi(N) = p + q - 2 = {p + q - 2}, match: {Z == p + q - 2}")
        # From p+q and pq=N, solve t^2 - (p+q)t + pq = 0
        s = Z + 2  # p + q
        disc = s * s - 4 * N
        sqrt_disc = int(math.isqrt(disc))
        if sqrt_disc * sqrt_disc == disc:
            p_calc = (s - sqrt_disc) // 2
            q_calc = (s + sqrt_disc) // 2
            print(f"  From Z: p+q = {s}, pq = {N} => t^2 - {s}t + {N} = 0")
            print(f"  Solutions: {p_calc} x {q_calc} = {p_calc * q_calc}, correct: {p_calc * q_calc == N}")
        print(f"  gcd(Z, N) = {math.gcd(Z, N)}, gcd(Z+2, N) = {math.gcd(Z + 2, N)}")
        print(f"  Complexity: O(N) gcd computations = O(N log N). Time: {t1 - t0:.4f}s")
        print(f"  >>> Signal: YES, but requires O(N) = O(2^(bit length)) work (exponential).")
        data["Z"] = Z

        # --------------------------------------------------------
        # Test 1b: Lattice points on xy = 0 mod N in box
        # --------------------------------------------------------
        print(f"\n--- Test 1b: Lattice points on xy = 0 mod N in [0,N-1]^2 ---")
        t0 = time.time()
        L = zero_divisor_hypersurface_lattice_count(N, N)
        t1 = time.time()
        print(f"  L(N) = #{{(x,y) in [0,N-1]^2 : xy = 0 mod N}} = {L}")
        # For N=pq: count pairs (x,y) in [0,N-1]^2 with pq | xy
        # = sum_{x=0}^{N-1} #{y : pq | xy} = sum_{x=0}^{N-1} gcd(x, pq) ... let me verify
        # Actually #{y in [0,N-1] : pq | xy} = gcd(x, pq) (number of y with pq/gcd(x,pq) | y, in [0,N-1])
        # Hmm, let me just report the value.
        print(f"  gcd(L, N) = {math.gcd(L, N)}")
        print(f"  Complexity: O(N^2). Time: {t1 - t0:.4f}s")
        data["L"] = L

        # --------------------------------------------------------
        # Test 2: 1D tropical corner locus
        # --------------------------------------------------------
        print(f"\n--- Test 2: 1D tropical corner locus vertex count ---")
        t0 = time.time()
        V, hull_count, hull = tropical_corner_locus_1d(N)
        t1 = time.time()
        print(f"  f(x) = min_k ((N mod k) + k*x)")
        print(f"  Lower convex hull of {{(k, N mod k)}} has {hull_count} vertices")
        print(f"  Corner locus vertices (breakpoints) = {V}")
        print(f"  First 10 hull points: {hull[:10]}")
        print(f"  Last 5 hull points: {hull[-5:]}")
        sig = check_factor_signal("V", V, N, p, q)
        print(sig)
        sig2 = check_factor_signal("hull_count", hull_count, N, p, q)
        print(sig2)
        print(f"  Complexity: O(N log N) for convex hull. Time: {t1 - t0:.4f}s")
        data["V"] = V
        data["hull_count"] = hull_count

        # --------------------------------------------------------
        # Test 3: 2D tropical curve from divisor polynomial
        # --------------------------------------------------------
        print(f"\n--- Test 3: 2D tropical curve ray count ---")
        t0 = time.time()
        R = tropical_curve_2d_ray_count(N)
        t1 = time.time()
        divs = divisors(N)
        print(f"  F(X,Y) = min_{{d|N}} (d*X + (N/d)*Y)")
        print(f"  Divisors of {N}: {divs}")
        print(f"  Number of rays of tropical curve = {R}")
        print(f"  (equals d(N) = {len(divs)}: points on hyperbola xy=N are all extreme)")
        print(f"  gcd(R, N) = {math.gcd(R, N)}")
        print(f"  Complexity: O(d(N)) after factorization, or O(sqrt(N)) to find divisors.")
        data["R"] = R

        # --------------------------------------------------------
        # Test 4: Concept lattice size
        # --------------------------------------------------------
        print(f"\n--- Test 4: Concept lattice size of divisibility context ---")
        t0 = time.time()
        if N <= 10000:
            C = concept_lattice_size(N)
            t1 = time.time()
            print(f"  Context: (divisors of {N}, divisors of {N}, 'divides')")
            print(f"  Concept lattice size = {C}")
            print(f"  (equals d(N) = {len(divisors(N))}: each divisor g gives concept (divisors of g, multiples of g))")
            print(f"  gcd(C, N) = {math.gcd(C, N)}")
            print(f"  Complexity: O(2^d(N) * d(N)). Time: {t1 - t0:.4f}s")
            data["C"] = C
        else:
            print(f"  (skipped for large N)")

        # --------------------------------------------------------
        # Test 5: Divisor count and arithmetic functions
        # --------------------------------------------------------
        print(f"\n--- Test 5: Divisor count d(N) and related ---")
        d = len(divisors(N))
        omega = prime_power_factor_count(N)
        print(f"  d(N) = {d} (number of divisors)")
        print(f"  Omega(N) = {omega} (prime factors with multiplicity)")
        print(f"  For semiprime pq: d(N) = 4, Omega(N) = 2")
        print(f"  gcd(d(N), N) = {math.gcd(d, N)}")
        print(f"  Note: d(N) = 4 does NOT reveal p, q (only that N is product of 2 distinct primes or p^3)")
        data["d"] = d

        # --------------------------------------------------------
        # Test 6: Lattice points on tropical line in box
        # --------------------------------------------------------
        print(f"\n--- Test 6: Lattice points on standard tropical line in [-B,B]^2 ---")
        B = int(math.isqrt(N))
        t0 = time.time()
        TL = tropical_line_lattice_count(B)
        t1 = time.time()
        print(f"  Standard tropical line V(min(x,y,0)) in [-{B},{B}]^2")
        print(f"  Lattice point count = {TL}")
        print(f"  gcd(TL, N) = {math.gcd(TL, N)}")
        print(f"  (This is independent of N's factors -- just geometry of the tropical line)")
        data["TL"] = TL

        all_data.append(data)

    # ============================================================
    # Summary table
    # ============================================================
    print("\n" + "=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    print(f"{'N':>6} {'p,q':>10} {'Z(N)':>6} {'V(N)':>6} {'hull':>6} {'R(N)':>6} {'d(N)':>6} {'gcd(V,N)':>8} {'gcd(hull,N)':>10}")
    print("-" * 80)
    for d in all_data:
        gV = math.gcd(d["V"], d["N"])
        gh = math.gcd(d["hull_count"], d["N"])
        print(f"{d['N']:>6} {str(d['p'])+'x'+str(d['q']):>10} {d['Z']:>6} {d['V']:>6} {d['hull_count']:>6} {d['R']:>6} {d['d']:>6} {gV:>8} {gh:>10}")

    print("\n" + "=" * 80)
    print("HONEST ASSESSMENT")
    print("=" * 80)
    print("""
1. ZERO-DIVISOR COUNT Z(N) = p + q - 2:
   - Genuine factor signal: Z(N) + 2 = p + q, and with N = pq this gives
     complete factorization via the quadratic formula.
   - BUT computing Z(N) requires O(N) gcd computations = O(N log N) time.
   - This is EXPONENTIAL in the bit length of N (O(2^(n/2)) for n-bit N).
   - No better than trial division. The "tropical hypersurface mod N" idea
     encodes factors, but extracting them is as hard as factoring.

2. 1D TROPICAL CORNER LOCUS V(N):
   - V(N) = number of breakpoints in lower envelope of {(k, N mod k)}.
   - Computed via convex hull in O(N log N) time (no factorization needed).
   - CHECK: does gcd(V(N), N) or gcd(V(N)+k, N) reveal a factor?
   - See table above. If no nontrivial gcd appears, this is NOT a factor signal.

3. 2D TROPICAL CURVE RAY COUNT R(N) = d(N):
   - Equals the number of divisors of N.
   - For semiprimes, d(N) = 4 always -- reveals nothing about p, q.
   - Computing d(N) without factoring requires O(sqrt(N)) trial division.

4. CONCEPT LATTICE SIZE = d(N):
   - The concept lattice of the divisibility context has exactly d(N) elements.
   - Same information as divisor count -- does not reveal factors.

5. STANDARD TROPICAL LINE lattice count:
   - Independent of N's factors. Not a signal.

CONCLUSION: The tropical-geometric invariants either (a) encode factors but
require exponential time to compute (zero-divisor count), or (b) reduce to
known arithmetic functions (divisor count) that don't reveal factors without
factoring. The CornerLocusProduct theorem (Corner(f*g) = Corner(f) U Corner(g))
is the tropical analog of "zero set of product = union of zero sets" -- it
describes structure but doesn't provide a shortcut to factorization.
""")


if __name__ == "__main__":
    main()

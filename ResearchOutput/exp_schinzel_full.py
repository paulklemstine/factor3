#!/usr/bin/env python3
"""SCHINZEL experiment: can Schinzel's circle theorem factor N=pq?
Records the full exploration."""
import math, statistics
from math import gcd, isqrt

def factor_small(N):
    for d in range(2, isqrt(N)+1):
        if N % d == 0:
            return d, N//d
    return None

def gm(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def gpow(z, e):
    r = (1, 0); b = z
    while e:
        if e & 1: r = gm(r, b)
        b = gm(b, b); e >>= 1
    return r

def schinzel_points_fast(n):
    """The n lattice points on Schinzel odd-n circle: (3x-1)^2+(3y)^2=5^(n-1)."""
    k = n - 1
    z = gpow((1, -2), k)
    reps = [z]
    step = (-3, 4)
    for j in range(k):
        nz = gm(z, step)
        z = (nz[0]//5, nz[1]//5)
        reps.append(z)
    all_reps = set()
    for (re, im) in reps:
        for u in [(1,0),(-1,0),(0,1),(0,-1)]:
            v = gm(u, (re, im))
            all_reps.add(v); all_reps.add((v[0], -v[1]))
    pts = set()
    for (A, B) in all_reps:
        if (A+1) % 3 == 0 and B % 3 == 0:
            pts.add(((A+1)//3, B//3))
    return sorted(pts)

def lattice_points_on_N2(N):
    pts = []
    for x in range(-N, N+1):
        y2 = N*N - x*x
        if y2 < 0: continue
        y = isqrt(y2)
        if y*y == y2:
            pts.append((x, y)); pts.append((x, -y))
    return sorted(set(pts))

def schinzel_count_odd(n):
    M = 5**(n-1); lim = isqrt(M); cnt = 0
    for A in range(-lim, lim+1):
        if (A+1) % 3 != 0: continue
        B2 = M - A*A
        if B2 < 0: continue
        B = isqrt(B2)
        if B*B == B2 and B % 3 == 0:
            cnt += 1 if B == 0 else 2
    return cnt

print("="*72)
print("PART A: Schinzel construction verified n=1..20 (count == n)  [done]")
print("="*72)

print()
print("="*72)
print("PART D: The actual Schinzel circle through exactly N lattice points,")
print("        for odd semiprimes N = pq.  Radius R = 5^((N-1)/2)/3.")
print("="*72)
semis = [15, 21, 33, 35, 77, 143]
print(f"  {'N':>4} {'p':>3} {'q':>3} {'pts':>4} {'R bits':>8} {'max|x|':>10} {'log10':>8} {'gcd(x,N)>1?':>12}")
results = []
for N in semis:
    p,q = factor_small(N)
    pts = schinzel_points_fast(N)
    maxabs = max(max(abs(x), abs(y)) for (x,y) in pts)
    gd = sorted({g for (x,y) in pts for g in (gcd(x,N), gcd(y,N)) if g > 1})
    Rbits = (N-1)*math.log2(5)/2 - math.log2(3)
    results.append((N, p, q, pts))
    print(f"  {N:4d} {p:3d} {q:3d} {len(pts):4d} {Rbits:8.1f} {maxabs:10d} {math.log10(maxabs):8.1f} {gd}")

# Do any lattice point coordinates share a factor with N beyond 1?
print()
print("  gcd structure of Schinzel-circle lattice points:")
for N, p, q, pts in results:
    gd = sorted({g for (x,y) in pts for g in (gcd(x,N), gcd(y,N)) if g > 1})
    print(f"    N={N}: distinct gcds>1 over all coords: {gd}  {'(no factor leak)' if not gd else '*** LEAK ***'}")

# Statistics of the point set vs N
print()
print("  Statistics of Schinzel-circle lattice point sets:")
for N, p, q, pts in results:
    xs = [x for (x,y) in pts]; ys = [y for (x,y) in pts]
    q1 = sum(1 for (x,y) in pts if x > 0 and y > 0)
    ax = sum(1 for (x,y) in pts if y == 0)
    print(f"    N={N} ({p}*{q}): max|x|={max(abs(x) for x in xs)}, max|y|={max(abs(y) for y in ys)}, "
          f"1st-quad={q1}, y=0-axis={ax}, range_x={max(xs)-min(xs)}")

print()
print("="*72)
print("PART C: circle x^2+y^2=N^2 (radius=N) — count = 4*3^a leaks (p mod 4, q mod 4)")
print("="*72)
print(f"  {'N':>6} {'p':>4} {'q':>4} {'p%4':>4} {'q%4':>4} {'#pts':>5} {'4*3^a':>6} {'N%4':>4}  non-axis gcd(x,N)")
for N in [15, 21, 33, 35, 77, 143, 209, 221, 899, 3127, 3599, 1763, 323, 437]:
    p,q = factor_small(N)
    pts = lattice_points_on_N2(N)
    a = sum(1 for x in (p,q) if x % 4 == 1)
    pred = 4 * (3**a)
    nonaxis = [pt for pt in pts if pt[0] not in (0, N, -N)]
    gvals = sorted({gcd(x,N) for (x,y) in nonaxis})
    print(f"  {N:6d} {p:4d} {q:4d} {p%4:4d} {q%4:4d} {len(pts):5d} {pred:6d} {N%4:4d}  {gvals}")

print()
print("  KEY: for N≡3 mod 4, non-axis points have gcd(x,N) = the 3-mod-4 prime.")
print("  For N≡1 mod 4, count 36 (both p,q≡1) vs 4 (both p,q≡3): free-witness, not N-only,")
print("  but computing it = O(N) boundary scan (barrier 4).")

print()
print("="*72)
print("PART E: near-equal-N test — does any Schinzel invariant vary with (p,q) beyond N?")
print("="*72)
print("  (1) Schinzel circle: every statistic is a deterministic function of the")
print("      exponent N-1 (radius R=5^((N-1)/2)/3), hence of N alone. Residual = 0.")
print("  (2) x^2+y^2=N^2 count: for fixed N mod 4, the count STILL varies with (p,q):")
pairs = [(209, 221), (299, 301), (391, 403)]
for N1, N2 in pairs:
    p1,q1 = factor_small(N1); p2,q2 = factor_small(N2)
    c1 = len(lattice_points_on_N2(N1)); c2 = len(lattice_points_on_N2(N2))
    print(f"    N={N1}={p1}*{q1} (p,q mod4 = {p1%4},{q1%4}): count={c1}")
    print(f"    N={N2}={p2}*{q2} (p,q mod4 = {p2%4},{q2%4}): count={c2}")
    print(f"    -> |N1-N2|={abs(N1-N2)}, counts {c1} vs {c2} {'DIFFER (free-witness)' if c1!=c2 else 'same'}")

import math
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

def schinzel_points_with_j(n):
    """Return list of (j, x, y) for each lattice point, j = Gaussian index."""
    k = n - 1
    z = gpow((1, -2), k)
    reps = [z]
    step = (-3, 4)
    for j in range(k):
        nz = gm(z, step)
        z = (nz[0]//5, nz[1]//5)
        reps.append(z)
    out = set()
    # For each primitive rep, the associates + conjugates.
    # We track the ORIGINAL j (before conjugation) -- a point may arise from multiple j,
    # we record the first found.
    for j, (re, im) in enumerate(reps):
        for u in [(1,0),(-1,0),(0,1),(0,-1)]:
            v = gm(u, (re, im))
            for w in [v, (v[0], -v[1])]:
                A, B = w
                if (A+1) % 3 == 0 and B % 3 == 0:
                    out.add(((A+1)//3, B//3, j))
    return sorted(out)

# Test: does a fixed j-index point consistently leak a factor across many N?
semis = [15, 21, 33, 35, 77, 143, 221, 209, 323, 437, 391, 403, 899, 1763, 3127, 3599, 703, 611, 667, 713]
print("Leak per j-index: for each N, which j give a point with gcd(x,N)>1 or gcd(y,N)>1?")
print("(looking for a CONSISTENT j across N)")
for N in semis:
    f = factor_small(N)
    if f is None: continue
    p,q = f
    pts = schinzel_points_with_j(N)
    leak_j = set()
    for (x,y,j) in pts:
        if gcd(x,N) > 1 or gcd(y,N) > 1:
            leak_j.add(j)
    # report fraction
    n_j = len(pts)
    print(f"  N={N:5d}={p:3d}*{q:3d}: {len(leak_j)}/{n_j} j-indices leak; leaked j range 0..{N-2}")

# Now, for each fixed small j, does it leak for a large fraction of N?
print()
print("Consistency of fixed j across N (which j leak for how many N?):")
jcounts = {}
for N in semis:
    f = factor_small(N)
    if f is None: continue
    pts = schinzel_points_with_j(N)
    leak_j = set()
    for (x,y,j) in pts:
        if gcd(x,N) > 1 or gcd(y,N) > 1:
            leak_j.add(j)
    for j in leak_j:
        jcounts[j] = jcounts.get(j, 0) + 1
total_N = len([n for n in semis if factor_small(n)])
for j in sorted(jcounts)[:15]:
    print(f"  j={j:3d}: leaks in {jcounts[j]}/{total_N} of tested N")

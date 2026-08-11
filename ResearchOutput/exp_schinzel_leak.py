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

def schinzel_points_fast(n):
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

print("Which lattice points leak a factor? (N = pq)")
for N in [15, 21, 33, 35, 77, 143]:
    p,q = factor_small(N)
    pts = schinzel_points_fast(N)
    print(f"\nN={N}={p}*{q}: {len(pts)} points")
    # for each point, gcd of x and y with N
    leaks = []
    for (x,y) in pts:
        gx, gy = gcd(x,N), gcd(y,N)
        if gx > 1 or gy > 1:
            leaks.append((x,y,gx,gy))
    for (x,y,gx,gy) in leaks[:8]:
        print(f"  pt=({x}, {y}): gcd(x,N)={gx}, gcd(y,N)={gy}")
    print(f"  total leaking points: {len(leaks)} / {len(pts)}")
    # expected by birthday: 2N/p coords div by p, 2N/q by q
    print(f"  expected (random mod p,q): ~{2*N/p:.1f} coords div by p={p}, ~{2*N/q:.1f} by q={q}")

# Check: are coordinates divisible by a factor CONSISTENTLY (structural) or random?
# Test: same N, but check whether the axis point (y=0) leaks.
print("\n=== Axis point (y=0) analysis: x_0 = (5^((N-1)/2)+1)/3 ===")
for N in [15, 21, 33, 35, 77, 143, 221, 209]:
    p,q = factor_small(N)
    x0 = (5**((N-1)//2) + 1) // 3
    print(f"  N={N}: x0=(5^((N-1)/2)+1)/3, gcd(x0,N)={gcd(x0,N)} (p={p},q={q})")

# Test the OTHER axis point candidate: (5^((N-1)/2)-1)/3 and +/- variants
print("\n=== Other simple candidates from axis/known points ===")
for N in [15, 21, 33, 35, 77, 143, 221, 209, 899]:
    p,q = factor_small(N)
    h = (N-1)//2
    for name, val in [("(5^h+1)/3", (5**h+1)//3), ("(5^h-1)/3", (5**h-1)//3)]:
        print(f"  N={N}: {name} gcd = {gcd(val,N)}", end="  ")
    print()

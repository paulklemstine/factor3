import math, random
from math import gcd, isqrt

def factor_small(N):
    for d in range(2, isqrt(N)+1):
        if N % d == 0:
            return d, N//d
    return None

def gm(a, b, m=None):
    if m is None:
        return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
    return ((a[0]*b[0]-a[1]*b[1]) % m, (a[0]*b[1]+a[1]*b[0]) % m)

def gpow_mod(z, e, m):
    r = (1 % m, 0); b = z
    while e:
        if e & 1: r = gm(r, b, m)
        b = gm(b, b, m); e >>= 1
    return r

def lattice_point_modN(j, N):
    """Compute the lattice point (x mod N, y mod N) from Gaussian index j.
    z_j = (1+2i)^j (1-2i)^{N-1-j}, take associates/conjugates, filter congruence,
    x=(A+1)/3, y=B/3, all mod N."""
    k = N - 1
    # z_j = (1+2i)^j (1-2i)^{k-j}  mod N
    zj = gm(gpow_mod((1,2), j, N), gpow_mod((1,-2), k-j, N), N)
    # We need the specific associate + congruence giving a lattice point.
    # Try all 8 variants (4 units x conj) and return the x,y that satisfy congruence.
    out = []
    for u in [(1,0),(-1,0),(0,1),(0,-1)]:
        v = gm(u, zj, N)
        for w in [v, (v[0], (N - v[1]) % N)]:
            A, B = w
            # A ≡ 2 mod 3, B ≡ 0 mod 3; x=(A+1)/3, y=B/3 over integers.
            # Mod N: need to detect divisibility. If A mod 3 == 2 and B mod 3 == 0,
            # then (A+1)/3 and B/3 are determined mod N (since 3 invertible mod N).
            if (A % 3) == 2 and (B % 3) == 0:
                x = ((A+1) * pow(3, -1, N)) % N
                y = (B * pow(3, -1, N)) % N
                out.append((x, y))
    return out

# VERIFY lattice_point_modN matches exact enumeration mod N for small N
print("=== Verify mod-N lattice point computation ===")
def schinzel_points_exact(n):
    k = n - 1
    z = gpow((1,-2), k)
    reps=[z]; step=(-3,4)
    for j in range(k):
        nz=gm(z); z=(nz[0]//5,nz[1]//5); reps.append(z)
    all_reps=set()
    for (re,im) in reps:
        for u in [(1,0),(-1,0),(0,1),(0,-1)]:
            v=gm(u,(re,im)); all_reps.add(v); all_reps.add((v[0],-v[1]))
    pts=set()
    for (A,B) in all_reps:
        if (A+1)%3==0 and B%3==0:
            pts.add(((A+1)//3, B//3))
    return pts

def gpow(z, e):
    r=(1,0); b=z
    while e:
        if e&1: r=gm(r,b)
        b=gm(b,b); e>>=1
    return r

N = 15
exact = schinzel_points_exact(N)
exact_mod = set((x%N, y%N) for (x,y) in exact)
got = set()
for j in range(N):
    for (x,y) in lattice_point_modN(j, N):
        got.add((x,y))
print(f"  N={N}: exact lattice points mod N = {len(exact_mod)}, from mod-N formula = {len(got)}")
print(f"  match: {exact_mod == got}")
if exact_mod != got:
    print(f"  exact-only: {exact_mod - got}")
    print(f"  modN-only: {got - exact_mod}")

# Success rate of random-j gcd sampling
print()
print("=== Random-j Schinzel-point gcd sampling: success per trial ===")
random.seed(42)
for N in [15, 21, 33, 35, 77, 143, 221, 899, 1763, 3127, 3599]:
    f = factor_small(N); p, q = f
    # exact success fraction among j
    exact = schinzel_points_exact(N)
    success_j = 0
    # for each exact point, check if it leaks
    leak_pts = [pt for pt in exact if gcd(pt[0],N)>1 or gcd(pt[1],N)>1]
    frac = len(leak_pts)/len(exact)
    # random-j sampling success rate via mod-N formula
    trials = 400
    hits = 0
    for _ in range(trials):
        j = random.randrange(N)
        for (x,y) in lattice_point_modN(j, N):
            g = gcd(x, N)
            if 1 < g < N:
                hits += 1
                break
            g = gcd(y, N)
            if 1 < g < N:
                hits += 1
                break
    print(f"  N={N:5d}={p:3d}*{q:3d}: exact leak fraction={frac:.4f}, random-j hit rate={hits/trials:.4f}, 4/sqrt(N)={4/math.sqrt(N):.4f}")

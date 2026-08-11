#!/usr/bin/env python3
"""
Verify the structural theorem:
  For p_i = c_i/N (counts c_i positive integers summing to N),
  fisherForm(p)(v,v) = N * S where S = sum(v_i^2/c_i),
  and gcd(F.num, N) = N / gcd(N, denominator(S)).

Hence the Fisher form yields a nontrivial factor iff denominator(S)
shares a factor with N, i.e. iff lcm(c_i) is divisible by p or q.
"""
import math, random
from fractions import Fraction

def miller_rabin(n, rounds=20):
    if n < 2: return False
    for pr in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % pr == 0: return n == pr
    r, d = 0, n-1
    while d % 2 == 0: r += 1; d //= 2
    for _ in range(rounds):
        a = random.randrange(2, n-1)
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = pow(x, 2, n)
            if x == n-1: break
        else: return False
    return True

def gen_prime(bits):
    while True:
        n = random.getrandbits(bits) | (1 << (bits-1)) | 1
        if miller_rabin(n): return n

def gen_semiprime(bits):
    p = gen_prime(bits//2); q = gen_prime(bits//2)
    while q == p: q = gen_prime(bits//2)
    return p*q, p, q

random.seed(7)
print("Verifying theorem: gcd(F.num, N) = N / gcd(N, den(S))")
print("where F = fisherForm(p)(v,v), p_i = c_i/N, S = sum(v_i^2/c_i)")
print()

for trial in range(8):
    bits = random.choice([18, 24, 30, 36])
    N, p, q = gen_semiprime(bits)
    # Random partition of N into d parts
    d = random.randint(4, 12)
    # Generate random counts summing to N
    cuts = sorted(random.sample(range(1, N), d-1))
    counts = [cuts[0]] + [cuts[i]-cuts[i-1] for i in range(1,d-1)] + [N-cuts[-1]]
    counts = [max(1,c) for c in counts]
    # adjust to sum to N
    diff = N - sum(counts)
    counts[-1] += diff
    if counts[-1] <= 0: continue

    probs = [Fraction(c, N) for c in counts]
    v = [Fraction((-1)**i) for i in range(d)]
    s = sum(v)
    v = [vi - s/d for vi in v]

    F = sum(Fraction(vi*vi, pi) for pi, vi in zip(probs, v))
    S = sum(Fraction(vi*vi, Fraction(c)) for vi, vi2, c in zip(v, v, counts) for vi in [vi2])
    # recompute S cleanly
    S = sum(vi*vi / Fraction(c) for vi, c in zip(v, counts))

    g_formula = N // math.gcd(N, S.denominator)
    g_direct = math.gcd(F.numerator, N)
    ok = (F == N*S) and (g_direct == g_formula)
    lcm_c = 1
    for c in counts:
        lcm_c = lcm_c * c // math.gcd(lcm_c, c)
    print(f"  N={N}={p}x{q}, d={d}: F==N*S:{F==N*N*S/N==N*S}, "
          f"gcd(F.num,N)={g_direct}, N/gcd(N,denS)={g_formula}, "
          f"match:{ok}, gcd(lcm(c),N)={math.gcd(lcm_c,N)}")

print()
print("Conclusion: gcd(F.num,N) = N/gcd(N,den(S)). For a NONTRIVIAL factor,")
print("need gcd(N,den(S)) strictly between 1 and N, i.e. den(S) divisible by")
print("exactly one of {p,q}. Since den(S) | lcm(c_i), need some c_i divisible")
print("by p or q but not both. This is the free-witness/trial-division condition.")

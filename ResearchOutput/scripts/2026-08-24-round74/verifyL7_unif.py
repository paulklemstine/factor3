#!/usr/bin/env python3
"""verifyL7_unif.py -- checks the attempt's UNIF proxy claims: asc S~2.13 outright,
win_asc ill-defined (p below window on ~147/150 draws). Independent implementation."""
import math, random
from math import gcd, isqrt
from sympy import nextprime

random.seed(424242)
n = 2000
pop = []
while len(pop) < n:
    v = int(math.exp(random.uniform(math.log(3), math.log(2**12))))
    p = int(nextprime(v))
    q = int(nextprime(random.randrange(2**12, 2**14)))
    if q < p: p, q = q, p
    pop.append((p*q, p))

C = {}; miss = 0
for N, p in pop:
    M = isqrt(N); lo_w = isqrt(max(2, N//2))
    cd, ca = M - p + 1, p - 1
    if p >= lo_w:
        cwa = p - lo_w + 1
    else:
        cwa = None; miss += 1
    for k, v in [("desc", cd), ("asc", ca)]:
        C[k] = C.get(k, 0.0) + v
    if cwa is not None:
        C["win_asc_cond"] = C.get("win_asc_cond", 0.0) + cwa
        Cn = C.get("win_asc_cond_n", 0) + 1
        C["win_asc_cond_n"] = Cn
base = C["desc"]/n
print(f"UNIF-proxy n={n}")
print(f"  desc mean={base:.2f}  asc mean={C['asc']/n:.2f}  S(asc)={base/(C['asc']/n):.4f} (attempt: 2.1325)")
print(f"  win_asc miss rate={miss/n:.3f} (attempt: 147/150={147/150:.3f})",
      f" S|reached={base/(C['win_asc_cond']/C['win_asc_cond_n']):.3f}" if C.get("win_asc_cond_n") else "")

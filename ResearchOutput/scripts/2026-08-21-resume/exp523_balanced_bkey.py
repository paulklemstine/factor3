#!/usr/bin/env python3
"""EXP 523 BALANCED-BKEY lean (round-53). Seed 20261100.
Does re-keying B recover the signal at bitlen 56/60?
H1: rem-keyed B recovers sp >= 0.55 at bitlen 56; H2: even then sp < 0.50 at bitlen 56.
"""
import json, time, math
import numpy as np
from sympy import primerange, nextprime

T0 = time.time()
OUT = {}
primes_all = list(primerange(2, 200000))
def smooth_mask(V, B):
    W = V.copy()
    for p in primes_all:
        if p > B: break
        m = W % p == 0
        while m.any():
            W[m] //= p
            m = W % p == 0
            if not m.any(): break
    return W == 1

for bits in (52, 56):
    rng = np.random.default_rng(20261100 + bits)
    lo, hi = 2**(bits//2 - 1), 2**(bits//2)
    data = []
    while len(data) < 800:
        r = int(rng.integers(lo, hi))
        p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, max(int(r*0.01), 2)))))
        N = p*q
        if N.bit_length() != bits: continue
        sq = math.isqrt(N)
        js = np.arange(1, 241, dtype=np.int64)
        V = js*(2*sq+js) + (sq*sq - N)
        if V.min() <= 0: continue
        data.append((N, V))
    vmed = float(np.median(np.concatenate([V for _,V in data]).astype(float)))
    results = {}
    for u in (2.5, 3.0, 3.5):
        B = max(int(round(math.exp(math.log(vmed)/u))), 50)
        sm = smooth_mask(np.concatenate([V for _,V in data]), B).reshape(len(data), -1)
        rate = sm.mean(axis=1)
        # T dial
        from sympy import legendre_symbol
        wr = [q for q in primes_all if q <= 400]
        T = np.array([sum(2.0/q for q in wr if pow(N%q,(q-1)//2,q)==1) for N,sq,V in [(d[0],0,0) for d in data]], float)
        # count feature
        C = np.array([sum(1 for q in range(3,101,2) if math.gcd(q,N)==1 and pow(N%q,(q-1)//2,q)==1) for N,sq,V in [(d[0],0,0) for d in data]], float)
        from scipy.stats import spearmanr
        spT = float(spearmanr(T, rate).statistic)
        spC = float(spearmanr(C, rate).statistic)
        results[u] = dict(B=B, sp_T=spT, sp_count=spC, rate_mean=float(rate.mean()),
                          zero_frac=float((rate==0).mean()))
    OUT[str(bits)] = results
    json.dump(OUT, open("/tmp/exp54_bkey/result.json","w"), indent=1, default=float)

print(json.dumps(OUT, indent=1, default=str))
print("DONE", round(time.time()-T0,1), "s")

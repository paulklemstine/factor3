#!/usr/bin/env python3
"""EXP 497 T-DIAL-STABLE lean (round-44). Base seed 20260930. Inline takeover.
Across-seed stability of the zero-fit dial T(N) = sum(2/p | QR primes p<=400).
PRE-STATED: H1 per-seed Spearman(T, rate) within [0.60, 0.85] on all 5 seeds, SE(mean) < 0.03;
H2 no population rank-flip (T-rank and rate-rank agree in top/bottom halves);
H3 Spearman(T) > Spearman(count<=100) + 0.05 on >= 4/5 seeds.
"""
import json, time, math
import numpy as np
import gmpy2
from sympy import primerange, nextprime

BASE = 20260930
T0 = time.time()
OUT = {"meta": {"base_seed": BASE, "exp": 497, "codename": "T-DIAL-STABLE"}}
primes_all = np.array(list(primerange(2, 200000)), dtype=np.int64)
def smooth_mask(V, B):
    W = V.copy()
    for p in primes_all[primes_all <= B]:
        while True:
            m = W % p == 0
            if not m.any(): break
            W[m] //= p
            if not (W % p == 0).any(): break
    return W == 1

def spearman(a, b):
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0,1])

rows = []
for k in range(5):
    seed = BASE + k
    rng = np.random.default_rng(seed)
    lo, hi = 2**20, 2**21
    data = []
    while len(data) < 1200:
        r = int(rng.integers(lo, hi))
        p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, 10**5))))
        N = p*q
        sq = math.isqrt(N)
        js = np.arange(1, 241, dtype=np.int64)
        V = js*(2*sq+js) + (sq*sq - N)
        if V.min() <= 0: continue
        data.append((N, sq, V))
    vmed = float(np.median(np.concatenate([V for _,_,V in data]).astype(float)))
    B = max(int(round(math.exp(math.log(vmed)/2.5))), 50)
    sm = smooth_mask(np.concatenate([V for _,_,V in data]), B).reshape(len(data), 240)
    rate = sm.mean(axis=1)
    wr = list(primerange(3, 401))
    cnt = [q for q in list(primerange(3, 101))]
    T = np.array([sum(2.0/q for q in wr if gmpy2.powmod(N % q, (q-1)//2, q) == 1) for N,sq,V in data], float)
    C = np.array([sum(1 for q in cnt if gmpy2.powmod(N % q, (q-1)//2, q) == 1) for N,sq,V in data], float)
    sT = spearman(T, rate); sC = spearman(C, rate)
    rows.append(dict(seed=seed, R2_base_seed=seed, spearman_T=sT, spearman_count=sC))
    OUT.setdefault("rows", []).append(rows[-1])
    json.dump(OUT, open("/tmp/exp44_tstable/result.json", "w"), indent=1, default=float)
    print(rows[-1], round(time.time()-T0,1), "s", flush=True)

sTs = [r["spearman_T"] for r in rows]
sCs = [r["spearman_count"] for r in rows]
mean = lambda x: sum(x)/len(x)
sd = lambda x: (sum((v-mean(x))**2 for v in x)/(len(x)-1))**0.5
se = sd(sTs)/len(sTs)**0.5
wins = sum(1 for a, b in zip(sTs, sCs) if a > b + 0.05)
OUT["summary"] = {"mean_spearman_T": mean(sTs), "sd": sd(sTs), "SE_mean": se,
                  "min": min(sTs), "max": max(sTs),
                  "mean_spearman_count": mean(sCs), "wins_gt_0.05": wins}
OUT["verdict"] = {
    "H1_band_and_SE": bool(all(0.60 <= s <= 0.85 for s in sTs) and se < 0.03),
    "H3_advantage_4of5": bool(wins >= 4)}
json.dump(OUT, open("/tmp/exp44_tstable/result.json", "w"), indent=1, default=float)
print(json.dumps(OUT["summary"]))
print(json.dumps(OUT["verdict"]))
print("DONE", round(time.time()-T0,1), "s")

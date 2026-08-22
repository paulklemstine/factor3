#!/usr/bin/env python3
"""EXP 502 FIXED-BOUND lean (round-45 #3). Seed 20260980. Inline takeover.
Decouple strip bound from u: ONE strip pass to PB=4000 recording (rem, maxp);
smooth@u iff rem==1 AND maxp <= B_u. Compare paired drops: variable-B vs fixed-B.
PRE-STATED: H1 attribution > 0.5 (bound shrinkage explains most of paper 168's residual
drop); H2 residual drop at fixed bound >= 0.03 (genuine reweighting remains).
"""
import json, time, math
import numpy as np
import gmpy2
from sympy import primerange, nextprime

SEED = 20260980
rng = np.random.default_rng(SEED)
T0 = time.time()
OUT = {"meta": {"seed": SEED, "exp": 502, "codename": "FIXED-BOUND"}}
def checkpoint():
    json.dump(OUT, open("/tmp/exp45_fixb/result.json", "w"), indent=1)

primes_all = np.array(list(primerange(2, 200000)), dtype=np.int64)
PB = 4000

rows = []
for k in range(8):
    seed = SEED + k
    rng = np.random.default_rng(seed)
    lo, hi = 2**20, 2**21
    data = []
    while len(data) < 1200:
        r = int(rng.integers(lo, hi))
        p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, 10**5))))
        N = p*q
        sq = math.isqrt(N)
        js = np.arange(1, 961, dtype=np.int64)
        V = js*(2*sq+js) + (sq*sq - N)
        if V.min() <= 0: continue
        data.append((N, sq, V))
    Vs = np.concatenate([V for _,_,V in data])
    vmed = float(np.median(Vs.astype(float)))
    # ONE strip pass to PB, tracking maxp per value
    W = Vs.copy()
    maxp = np.ones(len(Vs), dtype=np.int64)
    for p in primes_all[primes_all <= PB]:
        m = W % p == 0
        while m.any():
            W[m] //= p
            maxp[m] = np.maximum(maxp[m], p)
            m = W % p == 0
            if not m.any(): break
    smooth = (W == 1)
    B25 = int(round(math.exp(math.log(vmed)/2.5)))
    B35 = int(round(math.exp(math.log(vmed)/3.5)))
    rate25 = ((smooth) & (maxp <= B25)).reshape(len(data), -1).mean(axis=1)
    rate35 = ((smooth) & (maxp <= B35)).reshape(len(data), -1).mean(axis=1)
    wr = list(primerange(3, 401))
    T = np.array([sum(2.0/q for q in wr if gmpy2.powmod(N % q, (q-1)//2, q) == 1) for N,sq,V in [(d[0],d[1],d[2]) for d in data]], float)
    def sp(a, b):
        ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
        return float(np.corrcoef(ra, rb)[0,1])
    sp25 = sp(T, rate25); sp35 = sp(T, rate35)
    rows.append(dict(seed=seed, vmed=vmed, B25=B25, B35=B35,
                     sp25=sp25, sp35=sp35, d_varB=sp25-sp35))
    OUT.setdefault("rows", []).append(rows[-1])
    json.dump(OUT, open("/tmp/exp45_fixb/result.json", "w"), indent=1, default=float)
    print(rows[-1], round(time.time()-T0,1), "s", flush=True)

sp25s = [r["sp25"] for r in rows]; sp35s = [r["sp35"] for r in rows]
mean = lambda x: sum(x)/len(x)
sd = lambda x: (sum((v-mean(x))**2 for v in x)/(len(x)-1))**0.5
d_fixed = mean(sp25s) - mean(sp35s)
# paper-168 reference: variable-B d(960) = +0.0636
attribution = (0.0636 - d_fixed) / 0.0636 if 0.0636 else None
OUT["summary"] = {"mean_sp25": mean(sp25s), "mean_sp35": mean(sp35s),
                  "d_fixed": d_fixed, "sd_fixed": sd(sp35s),
                  "paper168_dvarB_ref": 0.0636,
                  "attribution_bound_share": attribution}
OUT["verdict"] = {"H1_attribution_gt_05": bool(attribution and attribution > 0.5),
                  "H2_residual_ge_003": bool(d_fixed >= 0.03)}
json.dump(OUT, open("/tmp/exp45_fixb/result.json", "w"), indent=1, default=float)
print(json.dumps(OUT["summary"]))
print(json.dumps(OUT["verdict"]))
print("DONE", round(time.time()-T0,1), "s")

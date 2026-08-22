#!/usr/bin/env python3
"""EXP 492 UNIFORM-DIAL lean (round-43 #2). Seed 20260924. Inline takeover.
Validate the footprint dial on GENUINELY UNBALANCED draws.
PRE-STATED: H1 Spearman(rate, w) > 0.4 on uniform draws at u=2.5;
H2 R2_uniform < R2_balanced - 0.05 (variance-share dilution);
H3 footprint w beats plain count under uniform draws (dR2(w over qrc) >= +0.02).
"""
import json, time, math
import numpy as np
import gmpy2
from sympy import primerange, nextprime

SEED = 20260924
rng = np.random.default_rng(SEED)
T0 = time.time()
OUT = {"meta": {"seed": SEED, "exp": 492, "codename": "UNIFORM-DIAL"}}
def checkpoint():
    json.dump(OUT, open("/tmp/exp43_unif/result.json", "w"), indent=1)

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

def population(mode, n_N=1200, NV=120):
    data = []
    while len(data) < n_N:
        if mode == "balanced":
            r = int(rng.integers(2**20, 2**21))
            p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, 10**5))))
        else:
            p = int(nextprime(int(rng.integers(2**10, 2**16))))
            q = int(nextprime(int(rng.integers(2**16, 2**22))))
        N = p*q
        sq = math.isqrt(N)
        js = np.arange(1, NV+1, dtype=np.int64)
        V = js*(2*sq+js) + (sq*sq - N)
        if V.min() <= 0: continue
        data.append((N, sq, V, min(p,q)))
    return data

def evaluate(data, ut=2.5):
    Vs = np.concatenate([V for _,_,V,_ in data])
    vmed = float(np.median(Vs.astype(float)))
    B = max(int(round(math.exp(math.log(vmed)/ut))), 50)
    sm = smooth_mask(Vs, B).reshape(len(data), -1)
    rate = sm.mean(axis=1)
    qrc = np.array([sum(1 for q in list(primerange(3,101))
                        if gmpy2.powmod(N,(q-1)//2,q)==1) for N,sq,V,p in data], float)
    wr = [q for q in list(primerange(3,401))]
    w = np.array([sum(2.0/q for q in wr if gmpy2.powmod(N,(q-1)//2,q)==1) for N,sq,V,p in data], float)
    dm = np.zeros_like(sm, dtype=bool)
    for pp in (2,3,5,7,11,13):
        dm |= (Vs.reshape(len(data),-1) % pp == 0)
    d = dm.mean(axis=1)
    idx = rng.permutation(len(data)); tr, te = idx[:900], idx[900:]
    def r2(cols):
        Xa = np.column_stack([np.ones(len(tr))]+[c[tr] for c in cols])
        coef,*_ = np.linalg.lstsq(Xa, rate[tr], rcond=None)
        pred = np.column_stack([np.ones(len(te))]+[c[te] for c in cols])@coef
        yy = rate[te]
        return 1-float(((yy-pred)**2).sum())/float(((yy-yy.mean())**2).sum()+1e-30)
    from scipy.stats import spearmanr
    sp_w = float(spearmanr(w, rate).statistic)
    return dict(R2_base=r2([qrc]), R2_aug=r2([qrc,w,d]), R2_w_only=r2([w]),
                dR2_w_over_qrc=r2([w])-r2([qrc]), spearman_w=sp_w,
                rate_mean=float(rate.mean()), B=B)

bal = evaluate(population("balanced"))
uni = evaluate(population("uniform"))
OUT["balanced"] = bal; OUT["uniform"] = uni
OUT["verdict"] = {
    "H1_spearman_gt_04": uni["spearman_w"] > 0.4,
    "H2_R2_drops_0.05": uni["R2_base"] < bal["R2_base"] - 0.05,
    "H3_w_beats_count_by_002": uni["dR2_w_over_qrc"] >= 0.02}
checkpoint()
print(json.dumps({"bal": bal, "uni": uni, "verdict": OUT["verdict"]}, indent=1, default=float))
print("DONE", round(time.time()-T0,1), "s")

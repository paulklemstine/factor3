#!/usr/bin/env python3
"""EXP 495 QRLOTTO-DIAL lean (round-43 #4). Seed 20260926. Inline takeover.
Theory-first no-fit dial: T(N) = sum(2/p) over QR primes p <= 400 — zero fitted coefficients.
PRE-STATED: H1 Spearman(T, per-N rate) > 0.5 out-of-sample; H2 9-bit QR-indicator OLS
R2 >= 0.45; H3 measured fractions n_p add < +0.02 R2 over indicators (indicators sufficient).
"""
import json, time, math
import numpy as np
import gmpy2
from sympy import primerange, nextprime

SEED = 20260926
rng = np.random.default_rng(SEED)
T0 = time.time()
OUT = {"meta": {"seed": SEED, "exp": 495, "codename": "QRLOTTO-DIAL"}}
def checkpoint():
    json.dump(OUT, open("/tmp/exp43_qr/result.json", "w"), indent=1)

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

PS9 = [3, 5, 7, 11, 13, 17, 19, 23]  # 8 odd primes <= 23 -> use <=29 for 9 bits
PS9 = [3, 5, 7, 11, 13, 17, 19, 23, 29]
data = []
while len(data) < 1500:
    r = int(rng.integers(2**20, 2**21))
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

qr_bits = np.zeros((len(data), len(PS9)), dtype=float)
for i, N in enumerate(Ns := [d[0] for d in data]):
    for j, pp in enumerate(PS9):
        qr_bits[i, j] = 1.0 if gmpy2.powmod(N % pp, (pp-1)//2, pp) == 1 else 0.0
nfrac = np.zeros((len(data), len(PS9)), dtype=float)
for i, N in enumerate(Ns):
    for j, pp in enumerate(PS9):
        nfrac[i, j] = float((np.array([d[2] for d in data][i]) % pp == 0).mean())
wr = list(primerange(3, 401))
T = np.array([sum(2.0/q for q in wr if gmpy2.powmod(N % q, (q-1)//2, q) == 1) for N in Ns], float)

idx = rng.permutation(len(data)); tr, te = idx[:1000], idx[1000:]
def r2(cols):
    Xa = np.column_stack([np.ones(len(tr))]+[c[tr] for c in cols])
    coef,*_ = np.linalg.lstsq(Xa, rate[tr], rcond=None)
    pred = np.column_stack([np.ones(len(te))]+[c[te] for c in cols])@coef
    yy = rate[te]
    return 1-float(((yy-pred)**2).sum())/float(((yy-yy.mean())**2).sum()+1e-30)
def sp(x, y):
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y))
    return float(np.corrcoef(rx, ry)[0,1])
s_T = sp(T[te], rate[te])
r_ind = r2(list(qr_bits.T))
r_ind_frac = r2(list(qr_bits.T) + list(nfrac.T))
OUT["cells"] = {"spearman_T": s_T, "R2_indicators": r_ind,
                "R2_ind_plus_fractions": r_ind_frac,
                "H3_delta_fractions_over_ind": r_ind_frac - r_ind}
OUT["verdict"] = {
    "H1_spearman_gt_05": bool(s_T > 0.5),
    "H2_R2_ge_045": bool(r_ind >= 0.45),
    "H3_fractions_add_lt_002": bool(r_ind_frac - r_ind < 0.02)}
checkpoint()
print(json.dumps({k: (round(v,4) if isinstance(v,float) else v) for k,v in OUT["cells"].items()}))
print(json.dumps(OUT["verdict"]))
print("DONE", round(time.time()-T0,1), "s")

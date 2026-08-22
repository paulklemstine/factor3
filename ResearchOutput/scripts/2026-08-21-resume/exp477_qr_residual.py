#!/usr/bin/env python3
"""EXP 477 QR-RESIDUAL (round-40, inline takeover — agent silent 15min). Seed 20260829.
What explains paper 144's 1.31x-floor residual at u=2.5 beyond QR-count(<=100)?
PRE-STATED: H1 weighted-QR(<=400) adds >= +0.05 out-of-sample R2; H2 direct small-prime
divisibility fraction (mechanism feature, measurable without factoring) adds >= +0.05;
H3 neither adds > +0.02 (floor estimate was optimistic).
"""
import json, time, math
import numpy as np
import gmpy2
from sympy import primerange, nextprime

SEED = 20260829
rng = np.random.default_rng(SEED)
T0 = time.time()
OUT = {"meta": {"seed": SEED, "exp": 477, "codename": "QR-RESIDUAL"}}
def checkpoint():
    json.dump(OUT, open("/tmp/exp39_qrresid/result.json", "w"), indent=1)

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

SMALL = [int(p) for p in primerange(3, 101)]
WIDE = [int(p) for p in primerange(3, 401)]

# population: bitlen 44, 1200 Ns x 80 values
bits, n_N, NV = 44, 1200, 80
hb = bits // 2; lo, hi = 2**(hb-1), 2**hb
Ns, sqs = [], []
while len(Ns) < n_N:
    r = int(rng.integers(lo, hi))
    p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, 10**6))))
    if p < lo or q >= hi or q <= p or p == q: continue
    Ns.append(p*q); sqs.append(math.isqrt(p*q))
js = np.arange(1, NV+1, dtype=np.int64)
Vs = np.array([j*(2*s+j)+(s*s-N) for s, N in zip(sqs, Ns) for j in js], dtype=np.int64)
assert Vs.min() > 0
rows_out = []
for ut in (2.5, 3.5):
    vmed = float(np.median(Vs.astype(float)))
    B = max(int(round(math.exp(math.log(vmed)/ut))), 50)
    sm = smooth_mask(Vs, B).reshape(n_N, NV)
    rate = sm.mean(axis=1)
    qrc = np.array([sum(1 for q in SMALL if gmpy2.powmod(N, (q-1)//2, q) == 1) for N in Ns], float)
    wqr = np.array([sum(2.0/q for q in WIDE if gmpy2.powmod(N, (q-1)//2, q) == 1) for N in Ns], float)
    # direct mechanism feature: fraction of values divisible by primes <= 13
    frac_small = np.array([(Vs[i*NV:(i+1)*NV] % 60 == 0).mean() for i in range(n_N)])  # placeholder replaced below
    # correct: divisible by any prime <= 13
    divmask = np.zeros((n_N, NV), dtype=bool)
    for pp in (2, 3, 5, 7, 11, 13):
        divmask |= (Vs.reshape(n_N, NV) % pp == 0)
    frac_direct = divmask.mean(axis=1)
    def ols_test(Xa, y, tr, te):
        X1 = np.column_stack([np.ones(len(tr)), Xa[tr]])
        coef, *_ = np.linalg.lstsq(X1, y[tr], rcond=None)
        pred = np.column_stack([np.ones(len(te)), Xa[te]]) @ coef
        yy = y[te]
        return 1 - float(((yy-pred)**2).sum())/float(((yy-yy.mean())**2).sum())
    idx = rng.permutation(n_N); tr, te = idx[:900], idx[900:]
    base = ols_test(qrc[:, None], rate, tr, te)
    aug_w = ols_test(np.column_stack([qrc, wqr]), rate, tr, te)
    aug_d = ols_test(np.column_stack([qrc, frac_direct]), rate, tr, te)
    aug_wd = ols_test(np.column_stack([qrc, wqr, frac_direct]), rate, tr, te)
    # bootstrap CI for deltaR2 (weighted feature)
    deltas = []
    y_te = rate[te]
    for _ in range(300):
        ii = rng.integers(0, len(te), len(te))
        def r2x(X):
            coef, *_ = np.linalg.lstsq(np.column_stack([np.ones(len(tr)), X[tr]]), rate[tr], rcond=None)
            pred = np.column_stack([np.ones(len(te)), X[te]]) @ coef
            return 1 - float(((y_te[ii]-pred[ii])**2).sum())/float(((y_te[ii]-y_te.mean())**2).sum()+1e-30)
        deltas.append(r2x(np.column_stack([qrc, wqr])) - r2x(qrc[:, None]))
    row = dict(u=ut, B=B, R2_base=base, R2_aug_weighted=aug_w, R2_aug_direct=aug_d,
               R2_aug_both=aug_wd,
               dR2_weighted=aug_w-base, dR2_weighted_ci=[float(np.percentile(deltas, 2.5)),
                                                          float(np.percentile(deltas, 97.5))],
               dR2_direct=aug_d-base)
    rows_out.append(row)
    OUT.setdefault("cells", []).append(row)
    checkpoint()
    print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in row.items()},
          round(time.time()-T0, 1), "s", flush=True)

OUT["verdict"] = {
    "H1_weighted_adds_0.05": any(r["dR2_weighted"] >= 0.05 and
                                  r["dR2_weighted_ci"][0] > 0 for r in rows_out),
    "H2_direct_adds_0.05": any(r["dR2_direct"] >= 0.05 for r in rows_out),
    "H3_neither_above_0.02": all(r["dR2_weighted"] < 0.02 and r["dR2_direct"] < 0.02
                                 for r in rows_out)}
checkpoint()
print(json.dumps(OUT["verdict"]))
print("DONE", round(time.time()-T0, 1), "s")

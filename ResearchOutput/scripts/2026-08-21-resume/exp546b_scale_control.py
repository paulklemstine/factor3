#!/usr/bin/env python3
"""exp546b — coordinator independent verification of exp546's headline signal.
Scale-confounder control: does MI(f1_w4096_hratio ; b1) survive WITHIN-log(n)-bin
permutation shuffles (200), within-design-strata, and within hit/no-hit classes?
Data: exp546_data.npz (3000 semiprimes, seed 20260823 population).
"""
import numpy as np
from collections import Counter
from math import isqrt

d = np.load('exp546_data.npz', allow_pickle=True)
P, Q, b1, strat = d['P'], d['Q'], d['b1'], d['stratum']
m = (P + Q) // 2
n = (Q - P) // 2
rho = m / n.astype(float)
dist = np.array([mm - isqrt(int(N)) for mm, N in zip(m, P * Q)])
feat = d['x_f1_w4096_hratio']


def mi(xb, y):
    c_xy = Counter(zip(xb.tolist(), y.tolist()))
    c_x = Counter(xb.tolist())
    c_y = Counter(y.tolist())
    N = len(xb)
    return sum(p * np.log2(p / ((c_x[a] / N) * (c_y[b] / N)))
               for (a, b), k in c_xy.items() for p in [k / N])


bins = np.quantile(feat, np.linspace(0, 1, 13))
xb = np.clip(np.digitize(feat, bins[1:-1]), 0, 11)

I_pooled = mi(xb, b1)
rng = np.random.default_rng(7)
null = [mi(rng.permutation(xb), b1) for _ in range(200)]
print(f"POOLED            MI={I_pooled:.4f} null={np.mean(null):.4f} sd={np.std(null):.4f} z={(I_pooled-np.mean(null))/np.std(null):.1f}")

lnb = np.quantile(np.log(n), np.linspace(0, 1, 9))
nb = np.clip(np.digitize(np.log(n), lnb[1:-1]), 0, 7)


def wsum(arr):
    tot = 0.0
    for b in range(8):
        msk = nb == b
        if msk.sum() > 50:
            tot += mi(arr[msk], b1[msk]) * (msk.sum() / len(xb))
    return tot


obs = wsum(xb)
nulls = []
for _ in range(200):
    xs = xb.copy()
    for b in range(8):
        idx = np.where(nb == b)[0]
        if len(idx) > 50:
            xs[idx] = xb[rng.permutation(idx)]
    nulls.append(wsum(xs))
print(f"WITHIN-logN-BINS  MI={obs:.4f} null={np.mean(nulls):.4f} sd={np.std(nulls):.4f} z={(obs-np.mean(nulls))/max(np.std(nulls),1e-12):.1f}")

for s in np.unique(strat):
    msk = strat == s
    xs, ys = feat[msk], b1[msk]
    bq = np.quantile(xs, np.linspace(0, 1, 13))
    xb2 = np.clip(np.digitize(xs, bq[1:-1]), 0, 11)
    print(f"stratum {s:7s} MI={mi(xb2, ys):.4f} b1dist={np.round(np.bincount(ys, minlength=3)/msk.sum(), 3)}")

hit = (dist < 4096).astype(int)
print("hit rate", round(hit.mean(), 3), "by b1", [round(float(hit[b1 == k].mean()), 4) for k in (1, 2, 3)])
print("corr(log(d+1), log rho)", round(float(np.corrcoef(np.log(dist + 1), np.log(rho))[0, 1]), 3))
for h in (0, 1):
    msk = hit == h
    xs, ys = feat[msk], b1[msk]
    bq = np.quantile(xs, np.linspace(0, 1, 13))
    xb2 = np.clip(np.digitize(xs, bq[1:-1]), 0, 11)
    rng2 = np.random.default_rng(3)
    nl = [mi(rng2.permutation(xb2), ys) for _ in range(100)]
    print(f"within hit={h}: n={int(msk.sum())} MI={mi(xb2, ys):.4f} nullmean={np.mean(nl):.4f}")

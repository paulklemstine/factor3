#!/usr/bin/env python3
"""EXP 485 MULTISEED-PHASE (round-41, inline takeover — channel death #9). Base seed 20260910.
Seed distribution of the phase/coincidence lift class (papers 150/151/152's gating question).
PRE-STATED:
H1: mean dR2(ph13) > 0 across 5 fresh populations, per-seed spread roughly [0, 0.04].
H2: mean dR2(pair) >= mean dR2(ph13) + 0.01, or indistinguishable (< 0.01) — decides paper
    152's 'first positive lever' claim.
H3: corr(dR2, R2_base) > 0.4 across seeds.
"""
import json, time, math
import numpy as np
import gmpy2
from sympy import primerange, nextprime

BASE = 20260910
T0 = time.time()
OUT = {"meta": {"base_seed": BASE, "exp": 485, "codename": "MULTISEED-PHASE"}}
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

PS = [3, 5, 7, 11, 13]
rows = []
for k in range(5):
    seed = BASE + k
    rng = np.random.default_rng(seed)
    lo, hi = 2**21, 2**22
    Ns, sqs = [], []
    while len(Ns) < 1200:
        r = int(rng.integers(lo, hi))
        p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, 10**6))))
        if p < lo or q >= hi or q <= p or p == q: continue
        Ns.append(p*q); sqs.append(math.isqrt(p*q))
    js = np.arange(1, 241, dtype=np.int64)
    Vs = np.array([j*(2*s+j)+(s*s-N) for s, N in zip(sqs, Ns) for j in js], dtype=np.int64)
    vmed = float(np.median(Vs.astype(float)))
    B = max(int(round(math.exp(math.log(vmed)/2.5))), 50)
    sm = smooth_mask(Vs, B).reshape(1200, 240)
    rate = sm.mean(axis=1)
    wqr = np.array([sum(2.0/q for q in list(primerange(3, 401))
                        if gmpy2.powmod(N, (q-1)//2, q) == 1) for N in Ns], float)
    divmask = np.zeros((1200, 240), dtype=bool)
    for pp in (2, 3, 5, 7, 11, 13):
        divmask |= (Vs.reshape(1200, 240) % pp == 0)
    dfrac = divmask.mean(axis=1)
    # ph13 features
    ph_cols = []
    for pp in PS:
        ang = np.zeros(1200)
        for i, N in enumerate(Ns):
            s = sqs[i]
            roots = [r for r in range(pp) if (r*r - N) % pp == 0]
            if roots:
                o = (roots[0] - s) % pp
                ang[i] = 2*math.pi*o/pp
        ph_cols += [np.cos(ang), np.sin(ang)]
    # pair coincidences (10 pairs)
    hit = {}
    for pp in PS:
        M = np.zeros((1200, 240), dtype=bool)
        for i, N in enumerate(Ns):
            s = sqs[i]
            for r in range(pp):
                if (r*r - N) % pp == 0:
                    o = (r - s) % pp
                    M[i, (o - 1) % 240 == (js - 1)] = True
        hit[pp] = M
    pairs = []
    pl = list(PS)
    for a_i in range(len(pl)):
        for b_i in range(a_i+1, len(pl)):
            pairs.append((hit[pl[a_i]] & hit[pl[b_i]]).mean(axis=1))
    base = [wqr, dfrac]
    phA = base + ph_cols
    prA = base + pairs
    def fit(cols, tr, te):
        Xa = np.column_stack([np.ones(len(tr))] + [c[tr] for c in cols])
        coef, *_ = np.linalg.lstsq(Xa, rate[tr], rcond=None)
        pred = np.column_stack([np.ones(len(te))] + [c[te] for c in cols]) @ coef
        yy = rate[te]
        return 1 - float(((yy-pred)**2).sum())/float(((yy-yy.mean())**2).sum()+1e-30)
    idx = rng.permutation(1200); tr, te = idx[:900], idx[900:]
    rb = fit(base, tr, te); rp = fit(phA, tr, te); rc = fit(prA, tr, te)
    row = dict(seed=seed, R2_base=rb, dR2_ph13=rp-rb, dR2_pair=rc-rb)
    rows.append(row)
    OUT.setdefault("rows", []).append(row)
    json.dump(OUT, open("/tmp/exp41_multiseed/result.json", "w"), indent=1, default=float)
    print(row, round(time.time()-T0,1), "s", flush=True)

d13 = [r["dR2_ph13"] for r in rows]
dpr = [r["dR2_pair"] for r in rows]
rb = [r["R2_base"] for r in rows]
mean = lambda x: sum(x)/len(x)
sd = lambda x: (sum((v-mean(x))**2 for v in x)/(len(x)-1))**0.5
diffs = [c-p for c, p in zip(dpr, d13)]
OUT["summary"] = {
    "mean_dR2_ph13": mean(d13), "sd_ph13": sd(d13),
    "mean_dR2_pair": mean(dpr), "sd_pair": sd(dpr),
    "mean_diff_pair_minus_ph13": mean(diffs), "sd_diff": sd(diffs),
    "corr_dR2_ph13_vs_R2base": float(np.corrcoef(d13, rb)[0,1]),
    "corr_dR2_pair_vs_R2base": float(np.corrcoef(dpr, rb)[0,1])}
OUT["verdict"] = {
    "H1_mean_ph13_positive": mean(d13) > 0,
    "H2_pair_dominates_by_0.01": mean(dpr) >= mean(d13)+0.01,
    "H2_indistinguishable": abs(mean(dpr)-mean(d13)) < 0.01,
    "H3_corr_gt_0.4": OUT["summary"]["corr_dR2_ph13_vs_R2base"] > 0.4}
json.dump(OUT, open("/tmp/exp41_multiseed/result.json", "w"), indent=1, default=float)
print(json.dumps(OUT["summary"], indent=1))
print(json.dumps(OUT["verdict"]))
print("DONE", round(time.time()-T0,1), "s")

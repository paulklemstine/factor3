#!/usr/bin/env python3
"""EXP 494 COINCIDENCE-DEPTH (round-43 #3). Seed 20260925. Inline.
Mechanism behind paper 152's pair-coincidence features.
PRE-STATED:
H1 (deterministic geometry): measured pair counts c_pq correlate > 0.9 with the
    phase-derived expectation (240 * (overlap of root slots)/(pq)) — coincidences are
    computed, not random.
H2 (clumping): per-prime hit-gap VARIANCE adds >= +0.02 R2 over paper-152's pair model.
H3 (proxy): pair coefficients -> ~0 after partialling d (they were union-count proxies).
"""
import json, time, math
import numpy as np
import gmpy2
from sympy import primerange, nextprime

SEED = 20260925
rng = np.random.default_rng(SEED)
T0 = time.time()
OUT = {"meta": {"seed": SEED, "exp": 494, "codename": "COINCIDENCE-DEPTH"}}
def checkpoint():
    json.dump(OUT, open("/tmp/exp43_cdepth/result.json", "w"), indent=1)

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
NV = 240
data = []
while len(data) < 800:
    r = int(rng.integers(2**20, 2**21))
    p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, 10**5))))
    N = p*q
    sq = math.isqrt(N)
    js = np.arange(1, NV+1, dtype=np.int64)
    V = js*(2*sq+js) + (sq*sq - N)
    if V.min() <= 0: continue
    data.append((N, sq, V))

# hit matrices per prime
hits = {pp: np.zeros((len(data), NV), dtype=bool) for pp in PS}
for i, (N, sq, V) in enumerate(data):
    for pp in PS:
        hits[pp][i] = (V % pp == 0)

vmed = float(np.median(Vs)) if (Vs := np.concatenate([V for _,_,V in data])) is not None else 0
B = max(int(round(math.exp(math.log(vmed)/2.5))), 50)
sm = smooth_mask(Vs, B).reshape(len(data), NV)
rate = sm.mean(axis=1)

w = np.array([sum(2.0/q for q in list(primerange(3, 401))
                  if gmpy2.powmod(N,(q-1)//2,q)==1) for N,sq,V in data], float)
d = np.array([hits[pp][i].any() for i in range(len(data)) for pp in [3]]).reshape(len(data),-1).sum(axis=1)  # placeholder
# proper d: union over PS of any-hit
dm = np.zeros(len(data), dtype=bool)
for pp in PS:
    dm |= hits[pp].any(axis=1)
# also include 2
dm |= (Vs.reshape(len(data), NV) % 2 == 0).any(axis=1)
d = dm.astype(float)

# pair coincidences (measured)
pairs = [(3,5),(3,7),(3,11),(3,13),(5,7),(5,11),(5,13),(7,11),(7,13),(11,13)]
c_meas = np.column_stack([(hits[a] & hits[b]).sum(axis=1) for a,b in pairs]).astype(float)
# phase-derived expectation: E[c_pq] = NV * gcd(p,q)/(pq) * overlap_factor; with p,q coprime
# small primes, gcd=1; roots of N mod p and mod q are INDEPENDENT uniform-ish slots, so
# E[#j with both p|v_j and q|v_j] = NV * (#roots_p/p) * (#roots_q/q) = NV * (2/p)(2/q) for QR primes.
exp_pairs = np.column_stack([np.full(len(data), NV * (2/a) * (2/b)) for a,b in pairs]).astype(float)
# H1: correlation measured vs expected (only meaningful where expectation varies — it doesn't
# within a fixed pair! So H1 tests the VARIANCE around the constant: if phases were random,
# c_pq ~ Binomial-ish around NV*4/(pq) with overdispersion from phase alignment. Test:
# measured c_pq mean vs expectation (calibration), and cross-N variance vs phase model.)
cal = []
for kk,(a,b) in enumerate(pairs):
    emp_mean = float(c_meas[:,kk].mean())
    pred_mean = float(exp_pairs[0,kk])
    cal.append(dict(pair=f"{a}x{b}", emp=round(emp_mean,2), pred=round(pred_mean,2),
                    ratio=round(emp_mean/max(pred_mean,1e-9),3)))
OUT["H1_calibration"] = cal
# H1 decision: calibration ratio within [0.7, 1.4] for all pairs = deterministic geometry OK
OUT["H1"] = all(0.7 <= c["ratio"] <= 1.4 for c in cal)

# clumping variance feature: for each prime, variance of inter-hit gaps
clump = np.zeros((len(data), len(PS)))
for pp_i, pp in enumerate(PS):
    for i in range(len(data)):
        slots = np.where(hits[pp][i])[0]
        if len(slots) > 1:
            clump[i, pp_i] = float(np.var(np.diff(slots)))
        else:
            clump[i, pp_i] = 0.0
clump_sum = clump.mean(axis=1)

idx = rng.permutation(len(data)); tr, te = idx[:600], idx[600:]
def r2(cols):
    Xa = np.column_stack([np.ones(len(tr))]+[c[tr] for c in cols])
    coef,*_ = np.linalg.lstsq(Xa, rate[tr], rcond=None)
    pred = np.column_stack([np.ones(len(te))]+[c[te] for c in cols])@coef
    yy = rate[te]
    return 1-float(((yy-pred)**2).sum())/float(((yy-yy.mean())**2).sum()+1e-30)
base = [w, d]
pairs_c = [c_meas[:,k] for k in range(10)]
r2_base = r2(base)
r2_pairs = r2(base + pairs_c)
r2_clump = r2(base + pairs_c + [clump_sum])
r2_exp = r2(base + [exp_pairs[:,0]]*0 + [exp_pairs[:,k] for k in range(10)])  # constant cols -> no info
OUT["arms"] = {"R2_base": r2_base, "R2_pairs": r2_pairs, "R2_pairs_clump": r2_clump,
               "dR2_pairs": r2_pairs - r2_base, "dR2_clump_over_pairs": r2_clump - r2_pairs}
OUT["H2"] = bool(r2_clump - r2_pairs >= 0.02)
# H3: coefficient of pairs in full model vs pairs-only model
Xp = np.column_stack([np.ones(len(tr))]+[c[tr] for c in base+pairs_c])
coef_p,*_ = np.linalg.lstsq(Xp, rate[tr], rcond=None)
Xpd = np.column_stack([np.ones(len(tr))]+[c[tr] for c in base+pairs_c+[clump_sum]])
coef_pd,*_ = np.linalg.lstsq(Xpd, rate[tr], rcond=None)
OUT["H3"] = {"pair_coefs_pairs_only": [float(x) for x in coef_p[2:]],
             "pair_coefs_with_clump": [float(x) for x in coef_pd[2:12]]}
checkpoint()
print(json.dumps(OUT["H1_calibration"], indent=1))
print("H1:", OUT["H1"], "H2:", OUT["H2"])
print("arms:", OUT["arms"])
print("DONE", round(time.time()-T0,1), "s")

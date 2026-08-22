#!/usr/bin/env python3
"""EXP 472 PER-N-PREDICTOR (round-39, inline takeover — agent channel down). Seed 20260827.
Lean validation of paper 139's per-N yield predictor.

PRE-STATED (before data):
H1: linear predictor rate ~ beta0 + beta1*QRcount(<=100), fitted on scale-40 train half,
    predicts held-out scale-40 test per-N rates with R2 >= 0.25, calibration slope in [0.8,1.25].
H2: same beta1 (renormalized intercept) transfers to bitlen 44 at matched u within bands.
H3: residual variance ~ 60-draw binomial sampling floor (i.e., the QR-count explains the
    systematic part; the rest is sampling noise, not missing structure).
"""
import json, time, math
import numpy as np
import gmpy2
from sympy import primerange, nextprime

SEED = 20260827
rng = np.random.default_rng(SEED)
T0 = time.time()
OUT = {"meta": {"seed": SEED, "exp": 472, "codename": "PER-N-PREDICTOR-INLINE"}}
def checkpoint():
    json.dump(OUT, open("/tmp/exp39_pred/result.json", "w"), indent=1)

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

SMALL = [int(p) for p in primerange(3, 101)]  # odd primes <= 100 (19 of them)

def population(bits, n_N, u_target):
    hb = bits // 2
    lo, hi = 2 ** (hb - 1), 2 ** hb
    ps, qs = [], []
    while len(ps) < n_N:
        r = int(rng.integers(lo, hi))
        p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, 10**6))))
        if p < lo or q >= hi or q <= p or p == q: continue
        ps.append(p); qs.append(q)
    Ns = [p * q for p, q in zip(ps, qs)]
    sqs = [math.isqrt(N) for N in Ns]
    js = np.arange(1, 61, dtype=np.int64)
    Vs = np.array([j * (2 * sq + j) + (sq * sq - N)
                   for sq, N in zip(sqs, Ns) for j in js], dtype=np.int64)
    vmed = float(np.median(Vs.astype(float)))
    B = max(int(round(math.exp(math.log(vmed) / u_target))), 50)
    sm = smooth_mask(Vs, B).reshape(n_N, 60)
    rate = sm.mean(axis=1)
    qrc = np.array([sum(1 for q in SMALL if gmpy2.powmod(N, (q - 1) // 2, q) == 1)
                    for N in Ns], dtype=float)
    return dict(bits=bits, u=u_target, B=B, rate=rate, qrc=qrc)

results = []
for bits in (40, 44):
    for ut in (2.5, 3.5):
        pop = population(bits, 1500, ut)
        if bits == 40:
            idx = rng.permutation(1500)
            tr, te = idx[:1000], idx[1000:]
            X, Y = pop["qrc"][tr], pop["rate"][tr]
            b1 = float(np.cov(X, Y)[0, 1] / np.var(X))
            b0 = float(Y.mean() - b1 * X.mean())
            pred = b0 + b1 * pop["qrc"][te]
            y = pop["rate"][te]
            ss_res = float(((y - pred) ** 2).sum())
            ss_tot = float(((y - y.mean()) ** 2).sum())
            r2 = 1 - ss_res / ss_tot
            slope = float(np.polyfit(pred, y, 1)[0])
            # binomial floor: expected residual variance from 60-draw estimates
            pbar = float(y.mean())
            floor = pbar * (1 - pbar) / 60
            res_var = ss_res / len(y)
            results.append(dict(cell=f"40/u{ut}", role="train40-test40", B=pop["B"],
                                beta0=b0, beta1=b1, R2=r2, calib_slope=slope,
                                residual_var=res_var, binom_floor=floor,
                                floor_frac=res_var / floor))
            # H2 transfer to 44
            pop44 = population(44, 1500, ut)
            pred44 = b0 + b1 * pop44["qrc"]
            y44 = pop44["rate"]
            r2t = 1 - float(((y44 - pred44) ** 2).sum()) / float(((y44 - y44.mean()) ** 2).sum())
            sl44 = float(np.polyfit(pred44, y44, 1)[0])
            results.append(dict(cell=f"40->44/u{ut}", role="transfer", B=pop44["B"],
                                R2=r2t, calib_slope=sl44))
        else:
            pass
        checkpoint()
        print(f"cell {bits}/u{ut} done", round(time.time() - T0, 1), "s", flush=True)

OUT["results"] = results
v1 = [r for r in results if r["role"] == "train40-test40"]
OUT["verdict"] = {
    "H1": all(r["R2"] >= 0.25 and 0.8 <= r["calib_slope"] <= 1.25 for r in v1),
    "H2": all(r["role"] == "transfer" and 0.8 <= r["calib_slope"] <= 1.25 for r in results if r["role"] == "transfer"),
    "H3": "residual_var/binom_floor reported per cell (≈1 => sampling noise explains rest)"}
checkpoint()
print(json.dumps(results, indent=1))
print("DONE", round(time.time() - T0, 1), "s")

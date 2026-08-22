#!/usr/bin/env python3
"""exp472_per_n_predictor.py -- round-39 experiment 472 rerun, codename PER-N-PREDICTOR.

Validates the lab's per-N relation-yield predictor (paper 139): the per-N smoothness
rate of x^2 - N values correlates (r ~ 0.4-0.5) with the count of small primes that
are quadratic residues of N.  We build the predictor and test it out-of-sample.

MECHANISM NOTE (why a QR dial should predict relation smoothness at all):
for small prime p NOT dividing N, v_j = (s+j)^2 - N ≡ 0 (mod p) iff s+j is a square
root of N mod p; such roots exist (2 of p classes) iff (N|p) = +1, and do not exist
at all when (N|p) = -1.  So each QR prime p divides ~2/p of the v_j while each
non-residue prime divides none -- more QR primes among small p => systematically
higher divisibility of x^2-N values => higher B-smooth yield.  This is a statement
about the METHOD's input statistics (sieve relations), never about p,q themselves.

PRE-STATED HYPOTHESES (recorded BEFORE any results were computed):
  H1: a linear-in-QR-count predictor fitted at scale bitlen 40, u=2.5 predicts
      held-out same-scale per-N rates with R^2 >= 0.25 and calibration slope
      in [0.8, 1.25].
  H2 (transfer): the same shape renormalized by ensemble mean transfers to
      bitlen {44, 48} at matched u within those bands (R^2 >= 0.25,
      calibration slope in [0.8, 1.25] at both scales).
  H3 (limits): adding weighted QR features (sum log p over QR primes <= min(B,200))
      lifts R^2 by > +0.10; if not, compare residual variance to the 60-draw
      binomial sampling floor and attribute.

BARRIERS:
  (5) the predictor is a residue dial predicting a METHOD's input statistics --
      zero factor information: per-N smoothness rate of x^2-N carries no reading
      of p or q (which-factor wall context).
  (8) QS calibration context: per-N yield prediction informs quadratic-sieve
      candidate triage / sieve-window calibration, not a factoring shortcut.

METHOD LEDGER:
  - relation values v_j = j(2s+j) + (s^2 - N) with s = isqrt(N) EXACT (gmpy2.isqrt),
    j = 1..60; identically v_j = (s+j)^2 - N; v_j > 0 asserted for every j, every N.
  - smoothness threshold per N: B_N = exp(ln(v_med)/u), v_med = median of the 60
    v_j; per-value Dickman argument u_j = ln v_j / ln B_N.
  - B_N-smooth test: strip ALL primes <= B_max(scale,u) by exact trial division;
    remainder == 1 iff fully split over primes <= B_max.  Since B_N <= B_max and any
    surviving factor exceeds B_max >= B_N, remainder == 1 <=> B_N-smooth.
  - QR-count feature: odd primes p <= 100 only (p=2 excluded), (N|p)=+1 tested as
    gmpy2.powmod(N, (p-1)//2, p) == 1 (odd-prime args throughout); a 0 return
    (p | N) counts as non-QR -- impossible here since all factors exceed 100 bits.../
    exceed 100 in value.
  - weighted feature: w_N = sum ln p over odd QR primes p <= min(B_N, 200).
  - populations: 3000 semiprimes per scale k in {40,44,48}; factors are distinct
    h=k/2-bit primes with top TWO bits set => bitlen(N) = k exactly.
  - seed 20260827; per-scale derived integer seeds for reproducibility.
  - model: OLS linear-in-QR-count primary (pre-stated "logistic/linear" -- linear
    chosen; weighted-IRLS logistic fitted as secondary cross-check).
  - train/test split at scale 40: first 2000 train, last 1000 test (index order).
"""
import json
import math
import os
import random
import time

import numpy as np
import gmpy2

SEED = 20260827
WORK = "/tmp/exp39_pred"
SCALES = [40, 44, 48]
N_PER = 3000
NREL = 60
US = [2.5, 3.5]
TRAIN_N = 2000


def sieve(n):
    bs = bytearray([1]) * (n + 1)
    bs[0:2] = b"\x00\x00"
    i = 2
    while i * i <= n:
        if bs[i]:
            step = bytearray(len(bs[i * i::i]))
            bs[i * i::i] = step
        i += 1
    return [i for i in range(n + 1) if bs[i]]


ALL_PRIMES = sieve(6000)                       # covers B_max at k=48,u=2.5 (~3300)
QR_PRIMES = [p for p in sieve(100) if p > 2]   # odd primes <= 100 (24 of them)
W_PRIMES = [p for p in sieve(200) if p > 2]    # odd primes <= 200 (45 of them)


def checkpoint(res, stage):
    res["stage"] = stage
    res["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    path = os.path.join(WORK, "result.json")
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(res, f, indent=1)
    os.replace(tmp, path)


def gen_population(k, n=N_PER):
    """Semiprimes: two distinct h=k/2-bit primes, top two bits set -> bitlen(N)=k."""
    rng = random.Random(SEED * 1000 + k)
    h = k // 2
    out, seen = [], set()
    while len(out) < n:
        p = int(gmpy2.next_prime(rng.getrandbits(h - 2) | (1 << (h - 1)) | (1 << (h - 2))))
        q = int(gmpy2.next_prime(rng.getrandbits(h - 2) | (1 << (h - 1)) | (1 << (h - 2))))
        if p == q:
            continue
        N = p * q
        if N.bit_length() != k or N in seen:
            continue
        seen.add(N)
        out.append(N)
    return out


def relation_values(N):
    s = int(gmpy2.isqrt(N))
    off = s * s - N  # <= 0
    V = np.array([j * (2 * s + j) + off for j in range(1, NREL + 1)], dtype=np.int64)
    assert (V > 0).all(), "relation value non-positive"
    return V


def qr_count(N):
    c = 0
    for p in QR_PRIMES:
        if gmpy2.powmod(N, (p - 1) // 2, p) == 1:
            c += 1
    return c


def weighted_qr(N, bcap):
    cap = min(float(bcap), 200.0)
    tot = 0.0
    for p in W_PRIMES:
        if p > cap:
            break
        if gmpy2.powmod(N, (p - 1) // 2, p) == 1:
            tot += math.log(p)
    return tot


def smooth_matrix(Vmat, B):
    """Strip primes <= max B; remainder==1 <=> B_N-smooth (see ledger)."""
    bmax = float(B.max())
    flat = Vmat.reshape(-1).copy()
    for p in ALL_PRIMES:
        if p > bmax:
            break
        while True:
            m = (flat % p) == 0
            if not m.any():
                break
            flat[m] //= p
    return (flat.reshape(Vmat.shape) == 1)


def r2(obs, pred):
    obs = np.asarray(obs, float)
    pred = np.asarray(pred, float)
    return 1.0 - ((obs - pred) ** 2).sum() / ((obs - obs.mean()) ** 2).sum()


def pearson(a, b):
    a = np.asarray(a, float) - np.mean(a)
    b = np.asarray(b, float) - np.mean(b)
    return float((a * b).sum() / math.sqrt((a * a).sum() * (b * b).sum()))


def rankdata(x):
    x = np.asarray(x, float)
    order = np.argsort(x, kind="mergesort")
    sx = x[order]
    r = np.empty(len(x))
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and sx[j + 1] == sx[i]:
            j += 1
        r[i:j + 1] = (i + j) / 2.0 + 1.0
        i = j + 1
    out = np.empty(len(x))
    out[order] = r
    return out


def spearman(a, b):
    return pearson(rankdata(a), rankdata(b))


def ols(X, y):
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    return coef


def logistic_irls(qr, counts, ntrials=NREL, iters=100):
    """Weighted Bernoulli IRLS on aggregated counts; returns (a,b) for logit(rate)."""
    X = np.column_stack([np.ones(len(qr)), qr])
    beta = np.zeros(2)
    for _ in range(iters):
        eta = X @ beta
        mu = 1.0 / (1.0 + np.exp(-eta))
        var = np.maximum(mu * (1 - mu), 1e-12)
        W = ntrials * var
        z = eta + (counts / ntrials - mu) / var
        XW = X * W[:, None]
        try:
            new = np.linalg.solve(X.T @ XW, XW.T @ z)
        except np.linalg.LinAlgError:
            break
        if np.max(np.abs(new - beta)) < 1e-10:
            beta = new
            break
        beta = new
    return beta


def eval_pred(obs, pred):
    slope, icept = np.polyfit(np.asarray(pred, float), np.asarray(obs, float), 1)
    return {
        "R2": round(r2(obs, pred), 4),
        "calib_slope": round(float(slope), 4),
        "calib_intercept": round(float(icept), 5),
        "spearman": round(spearman(pred, obs), 4),
        "pearson": round(pearson(pred, obs), 4),
        "resid_var": round(float(np.mean((np.asarray(obs, float) - np.asarray(pred, float)) ** 2)), 8),
    }


def main():
    t0 = time.time()
    res = {
        "exp": "472_PER-N-PREDICTOR_rerun",
        "round": "39",
        "seed": SEED,
        "barriers": [
            "(5) residue dial predicting a METHOD's input statistics -- zero factor information",
            "(8) QS calibration context: informs sieve/candidate triage, not factoring",
        ],
    }
    data = {}       # (k,u) -> dict(rate, w)
    feats = {}      # k -> dict(qr, vmed)
    pops = {}

    # ---------- stage A: populations, relation values, features, smoothness ----------
    for k in SCALES:
        tk = time.time()
        Ns = gen_population(k)
        Vmat = np.vstack([relation_values(N) for N in Ns])
        vmed = np.median(Vmat.astype(float), axis=1)
        qr = np.array([qr_count(N) for N in Ns], dtype=np.int64)
        feats[k] = {"qr": qr, "vmed": vmed}
        pops[k] = {"n": len(Ns), "mean_qr": float(qr.mean()), "std_qr": float(qr.std())}
        checkpoint(res, f"pop+values+QR k={k} ({time.time()-t0:.0f}s)")
        for u in US:
            B = np.exp(np.log(vmed) / u)
            sm = smooth_matrix(Vmat, B)
            rate = sm.mean(axis=1)
            w = np.array([weighted_qr(N, b) for N, b in zip(Ns, B)])
            data[(k, u)] = {"rate": rate, "w": w, "B": B}
            pu = {
                "mean_B": round(float(B.mean()), 2),
                "mean_rate": round(float(rate.mean()), 5),
                "std_rate": round(float(rate.std()), 5),
                "frac_all_smooth": round(float(sm.all(axis=1).mean()), 4),
                "pearson_qr_rate": round(pearson(qr, rate), 4),
                "spearman_qr_rate": round(spearman(qr, rate), 4),
                "pearson_w_rate": round(pearson(w, rate), 4),
            }
            pops[k][f"u{u}"] = pu
            print(f"[{time.time()-t0:6.0f}s] scale {k} u={u}: mean_rate={pu['mean_rate']} "
                  f"r(qr,rate)={pu['pearson_qr_rate']} rho={pu['spearman_qr_rate']}", flush=True)
            res["populations"] = pops
            checkpoint(res, f"smoothness done k={k} u={u}")
        print(f"[{time.time()-t0:6.0f}s] scale {k} complete", flush=True)

    # ---------- stage B: fits ----------
    results = {}
    for u in US:
        d40 = data[(40, u)]
        qr40, rate40 = feats[40]["qr"], d40["rate"]
        tr = np.arange(TRAIN_N)
        te = np.arange(TRAIN_N, N_PER)

        # M1: linear in QR count, fitted on scale-40 train
        X1 = np.column_stack([np.ones(len(tr)), qr40[tr]])
        c1 = ols(X1, rate40[tr])
        a1, b1 = float(c1[0]), float(c1[1])
        pred_te = a1 + b1 * qr40[te]
        m1_te = eval_pred(rate40[te], pred_te)

        # logistic variant on same split (secondary)
        lg = logistic_irls(qr40[tr], np.round(rate40[tr] * NREL).astype(int))
        eta_t = lg[0] + lg[1] * qr40[te]
        pred_lg = 1.0 / (1.0 + np.exp(-eta_t))
        m1_lg = eval_pred(rate40[te], pred_lg)

        # H2 transfer: renormalize by ensemble mean at target scale, same slope b1
        h2 = {}
        for k in [44, 48]:
            qrk = feats[k]["qr"]
            ratek = data[(k, u)]["rate"]
            predk = ratek.mean() + b1 * (qrk - qrk.mean())
            h2[str(k)] = eval_pred(ratek, predk)

        # H3: add weighted feature
        X2 = np.column_stack([np.ones(len(tr)), qr40[tr], d40["w"][tr]])
        c2 = ols(X2, rate40[tr])
        pred2_te = c2[0] + c2[1] * qr40[te] + c2[2] * d40["w"][te]
        m2_te = eval_pred(rate40[te], pred2_te)

        # binomial sampling floor (60 draws per N) on the scale-40 test set
        obs_te = rate40[te]
        floor_var = float(np.mean(obs_te * (1 - obs_te)) / NREL)
        total_var = float(np.var(obs_te))
        max_attainable_R2 = 1.0 - floor_var / total_var
        ratio_m1 = m1_te["resid_var"] / floor_var
        ratio_m2 = m2_te["resid_var"] / floor_var

        blk = {
            "coef_linear": {"intercept": round(a1, 6), "slope_per_QR": round(b1, 6)},
            "M1_test": m1_te,
            "M1_logistic_test": m1_lg,
            "transfer_renormed": h2,
            "M2_weighted_test": m2_te,
            "coef_M2": {"w_coef": round(float(c2[2]), 8)},
            "floor": {
                "binomial_floor_var_60draws": round(floor_var, 8),
                "total_var_test": round(total_var, 8),
                "max_attainable_R2": round(max_attainable_R2, 4),
                "resid_over_floor_M1": round(ratio_m1, 3),
                "resid_over_floor_M2": round(ratio_m2, 3),
            },
        }

        # verdicts
        if u == 2.5:
            h1_ok = m1_te["R2"] >= 0.25 and 0.8 <= m1_te["calib_slope"] <= 1.25
            blk["H1"] = {
                "R2_pass": bool(m1_te["R2"] >= 0.25),
                "slope_pass": bool(0.8 <= m1_te["calib_slope"] <= 1.25),
                "verdict": "CONFIRMED" if h1_ok else "REFUTED",
            }
            h2_ok = all(
                h2[k]["R2"] >= 0.25 and 0.8 <= h2[k]["calib_slope"] <= 1.25 for k in ["44", "48"]
            )
            blk["H2"] = {
                "per_scale": {kk: {"R2_pass": bool(h2[kk]["R2"] >= 0.25),
                                   "slope_pass": bool(0.8 <= h2[kk]["calib_slope"] <= 1.25)}
                              for kk in ["44", "48"]},
                "verdict": "CONFIRMED" if h2_ok else "REFUTED",
            }
            lift = m2_te["R2"] - m1_te["R2"]
            blk["H3"] = {
                "lift_R2": round(lift, 4),
                "verdict": "CONFIRMED" if lift > 0.10 else "NOT-CONFIRMED",
            }
            if lift <= 0.10:
                if ratio_m1 <= 1.15:
                    attrib = ("M1 residual variance sits at the 60-draw binomial sampling "
                              "floor (ratio %.2f): the unexplained variance is measurement "
                              "noise, not missing signal; no richer QR feature can lift "
                              "observable R^2 materially." % ratio_m1)
                elif ratio_m2 <= 1.15:
                    attrib = ("weighted feature reaches the floor (ratio %.2f) where M1 "
                              "does not (%.2f): signal beyond QR-count exists but is "
                              "captured by the weighted channel." % (ratio_m2, ratio_m1))
                else:
                    attrib = ("residual variance %.2fx the floor: genuine unexplained "
                              "structure beyond QR features remains." % ratio_m1)
                blk["H3"]["attribution"] = attrib
        results[f"u{u}"] = blk
        print(f"[{time.time()-t0:6.0f}s] fits done u={u}: "
              f"H1 R2={m1_te['R2']} slope={m1_te['calib_slope']}", flush=True)

    res["results"] = results
    res["ledger"] = [
        "u per-value from ln v/ln B; B_N = exp(ln v_med/u_target)",
        "exact isqrt via gmpy2.isqrt; relation values asserted positive",
        "Legendre via gmpy2.powmod(N,(p-1)//2,p)==1, ODD primes only (p=2 excluded)",
        "B-smooth via trial division stripping primes<=B_max(scale,u); remainder==1",
        "semiprime factors: distinct h-bit primes, top two bits set -> bitlen(N)=k",
        "split: scale-40 indices 0..1999 train, 2000..2999 test",
        "OLS primary (pre-stated 'logistic/linear'); weighted-IRLS logistic secondary",
    ]
    checkpoint(res, "COMPLETE")

    # persist raw arrays for re-analysis without recompute
    arrs = {}
    for k in SCALES:
        arrs[f"qr_{k}"] = feats[k]["qr"]
        for uu in US:
            arrs[f"rate_{k}_{uu}"] = data[(k, uu)]["rate"]
            arrs[f"w_{k}_{uu}"] = data[(k, uu)]["w"]
    np.savez_compressed(os.path.join(WORK, "exp472_data.npz"), **arrs)

    print(json.dumps(res, indent=1)[:4000], flush=True)
    print(f"DONE in {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()

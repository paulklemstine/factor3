#!/usr/bin/env python3
"""
EXP-478 FOOTPRINT-SCALE (round-40, factor3 lab)

Question: paper 145 fitted the footprint dial (qrc<=100, w(N)=QR mass over
p<=400, d(N)=direct divisibility over p<=13) to per-N relation yield at ONE
scale (bitlen 44, 1200 Ns x 80 values). Does that dial TRANSFER to bitlen
{48, 52}, and how close does it get to the binomial sampling ceiling at
80 vs 240 values/N?

PRE-STATED HYPOTHESES (recorded BEFORE data collection):
H1: the footprint dial fitted at bitlen 44 transfers to bitlen {48,52} at
    matched u with calibration slope in [0.8, 1.25] out-of-sample.
H2: at 240 values/N (4x more) the attainable ceiling roughly halves
    (binomial floor prop 1/n); the augmented dial's R^2 rises toward it --
    report R^2 vs the computed ceiling at both 80 and 240 values/N.
H3: the direct feature d(N) remains independently significant after w(N) at
    both scales (its coefficient stays >= 2 SE).

BARRIERS: (5) residue dials describe METHOD INPUT statistics only (QS relation
values), never factor information; (8) QS calibration context -- all claims
live inside the QS relation-yield frame at toy bitlen 44-52.

Seed 20260830. Work dir /tmp/exp39_footscale/. Checkpoints to result.json
after every stage.
"""
import json, os, sys, time, math
from math import isqrt
import numpy as np

SEED = 20260830
WORK = "/tmp/exp39_footscale"
BITLENS = [44, 48, 52]
NPOP = 1200
JMAX = 240            # j = 1..240; arm-80 = j<=80, arm-240 = j<=240 (nested)
US = [2.5, 3.5]
W_PMAX = 400          # w(N): QR primes <= 400
QRC_PMAX = 100        # qrc: QR primes <= 100
D_PMAX = 13           # d(N): direct divisibility primes <= 13
NBOOT = 300
SPLIT_TRAIN = 900     # 900/300 split at bitlen 44

os.makedirs(WORK, exist_ok=True)
rng = np.random.default_rng(SEED)
T0 = time.time()
RESULT = {"exp": "478", "codename": "FOOTPRINT-SCALE", "seed": SEED,
          "hypotheses": {
              "H1": "44-fit footprint dial transfers to bitlen {48,52} at matched u with calibration slope in [0.8,1.25] OOS",
              "H2": "at 240 values/N attainable ceiling roughly halves (binomial floor prop 1/n); augmented dial R^2 rises toward ceiling; report R^2 vs computed ceiling at 80 and 240",
              "H3": "d(N) stays independently significant after w(N) at both scales (coef >= 2 SE)"}}

def save():
    tmp = os.path.join(WORK, "result.json.tmp")
    with open(tmp, "w") as f:
        json.dump(RESULT, f, indent=1)
    os.replace(tmp, os.path.join(WORK, "result.json"))

def log(msg):
    print(f"[{time.time()-T0:7.1f}s] {msg}", flush=True)

# ---------------------------------------------------------------- ledger
RESULT["ledger"] = {
    "python": sys.version.split()[0], "numpy": np.__version__,
    "gmpy2": __import__("gmpy2").version(),
    "host_cpus": os.cpu_count(),
    "feature_conventions": {
        "qrc": f"count of ODD primes p<={QRC_PMAX} with (N/p)=+1 (Euler criterion)",
        "w":   f"sum of 2/p over ODD primes p<={W_PMAX} with (N/p)=+1 (positive density mass; paper-145 'footprint-weighted QR mass')",
        "d":   "fraction of the arm's relation values v divisible by at least one prime <=13"},
    "population": f"{NPOP} balanced semiprimes p*q per bitlen, p,q ~{BITLENS[0]//2}-bit primes drawn in [2^(b/2-1),2^(b/2)), N forced to exact bitlen, unique",
    "values": f"v_j = j(2*floor(sqrt N)+j)+(floor(sqrt N)^2-N), j=1..{JMAX}, assert v>0; arm80=j 1..80, arm240=j 1..240 (nested)",
    "smoothness": "u(median v) in {2.5,3.5}; B=exp(ln vmed/u) so B(2.5)>B(3.5); strip primes<=B(2.5) once by vectorized trial division; smooth@u iff remainder==1 AND largest found prime <= B(u) (v2 fix: original strip-to-B35 collapsed u2.5 onto u3.5)",
    "model": "OLS y ~ 1 + qrc + w + d (augmented footprint dial), y = arm fraction of B-smooth values",
    "protocol": "fit at bitlen 44 (seeded 900/300 split); transfer slopes fixed to 48/52 with intercept renormalized to target mean; calibration slope = OLS y~a+c*yhat on target; 300-resample bootstrap percentile CI on slope; PRIMARY ceiling = split ceiling C=S/Var(y_arm) with S=Cov(disjoint half-arm yields) (leak-free estimate of Var(true per-N rate)); SECONDARY pihat ceiling Var(pihat)/(Var(pihat)+E[pi(1-pi)]/n) from in-population fit (can be distorted by d's same-value reading); no-d ablation (qrc+w only) reported per cell",
    "barriers": ["(5) residue dials of METHOD input statistics only -- qrc/w/d describe QS relation-value divisibility structure, carry no factor information",
                 "(8) QS calibration context -- toy bitlen 44-52, single seed, OLS on bounded fractions"],
    "started": time.strftime("%Y-%m-%d %H:%M:%S")}
save()
log("stage 0: ledger written")

# ---------------------------------------------------------------- primes
def primes_upto(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            sieve[i * i:: i] = bytearray(len(range(i * i, n + 1, i)))
    return [i for i in range(n + 1) if sieve[i]]

MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)  # deterministic < 3.3e24

def is_prime(n):
    if n < 2:
        return False
    for p in MR_BASES:
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in MR_BASES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

def random_prime(lo, hi):
    while True:
        c = int(rng.integers(lo, hi)) | 1
        if is_prime(c):
            return c

def gen_semiprimes(bitlen, count):
    h = bitlen // 2
    lo, hi = 1 << (h - 1), 1 << h
    out = set()
    while len(out) < count:
        p = random_prime(lo, hi)
        q = random_prime(lo, hi)
        N = p * q
        if N.bit_length() == bitlen:
            out.add(N)
    return sorted(out)

# ---------------------------------------------------------------- legendre features
ODD_P400 = [p for p in primes_upto(W_PMAX) if p > 2]
ODD_P100 = [p for p in ODD_P400 if p <= QRC_PMAX]
D_PRIMES = [2, 3, 5, 7, 11, 13]

def legendre_features(Ns):
    """Ns: int64 array. Returns qrc (<=100), w (<=400)."""
    qrc = np.zeros(len(Ns))
    w = np.zeros(len(Ns))
    for p in ODD_P400:
        r = Ns % p
        syms = np.fromiter((pow(int(ri), (p - 1) // 2, p) for ri in r),
                           dtype=np.int64, count=len(r))
        qr = (syms == 1)
        if p <= QRC_PMAX:
            qrc += qr
        w += (2.0 / p) * qr
    return qrc, w

# ---------------------------------------------------------------- per-bitlen build
def build_bitlen(bitlen):
    t = time.time()
    Ns_list = gen_semiprimes(bitlen, NPOP)
    Ns = np.array(Ns_list, dtype=np.int64)
    s = np.array([isqrt(int(N)) for N in Ns_list], dtype=np.int64)
    assert np.all(s * s <= Ns) and np.all(Ns < (s + 1) * (s + 1))

    J = np.arange(1, JMAX + 1, dtype=np.int64)          # (240,)
    V = J[None, :] * (2 * s[:, None] + J[None, :]) + (s * s - Ns)[:, None]
    assert np.all(V > 0), "relation values must be positive"
    assert V.dtype == np.int64 and V.max() < 2**62

    vmed = float(np.median(V))
    B = {u: math.exp(math.log(vmed) / u) for u in US}
    # NOTE: B(2.5) > B(3.5); strip once up to the LARGEST bound, derive both targets
    strip_primes = [p for p in primes_upto(int(B[2.5]) + 1)]

    Q = V.copy()
    lpf = np.zeros_like(V)                               # largest prime factor found (<=B35)
    div13 = np.zeros(V.shape, dtype=bool)
    for p in D_PRIMES:
        div13 |= (V % p) == 0
    for p in strip_primes:
        while True:
            m = (Q % p) == 0
            if not m.any():
                break
            Q[m] //= p
            lpf[m] = np.maximum(lpf[m], p)
    smooth = {u: (Q == 1) & (lpf <= B[u]) for u in US}

    qrc, w = legendre_features(Ns)
    rec = {
        "N": [int(x) for x in Ns_list], "qrc": qrc.tolist(), "w": [round(float(x), 6) for x in w],
        "vmed": vmed, "B25": B[2.5], "B35": B[3.5],
        "n_strip_primes": len(strip_primes),
        "mean_yield": {f"u{u}_a{n}": float(smooth[u][:, :n].mean()) for u in US for n in (80, 240)},
    }
    # per-N targets and half-split means (for Spearman-Brown ceilings)
    for u in US:
        for n in (80, 240):
            sm = smooth[u][:, :n]
            rec[f"y_u{u}_a{n}"] = sm.mean(1).tolist()
            rec[f"h_u{u}_a{n}_e"] = sm[:, 0::2].mean(1).tolist()
            rec[f"h_u{u}_a{n}_o"] = sm[:, 1::2].mean(1).tolist()
    for n in (80, 240):
        rec[f"d_a{n}"] = div13[:, :n].mean(1).tolist()
    log(f"bitlen {bitlen}: built ({time.time()-t:.1f}s), vmed={vmed:.3e}, "
        f"B(2.5)={B[2.5]:.0f}, B(3.5)={B[3.5]:.0f}, strip primes={len(strip_primes)}, "
        f"yields={ {k: round(v,4) for k,v in rec['mean_yield'].items()} }")
    return rec

# ---------------------------------------------------------------- OLS helpers
def r2(y, yhat):
    return 1.0 - float(((y - yhat) ** 2).sum() / ((y - y.mean()) ** 2).sum())

def ols(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    n, k = X.shape
    dof = max(n - k, 1)
    s2 = float(res @ res) / dof
    cov = s2 * np.linalg.pinv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    return beta, se, beta / se

def calib_slope(y, pred):
    pc = pred - pred.mean()
    return float((y - y.mean()) @ pc / (pc @ pc))

def boot_slope_ci(y, pred, B=NBOOT):
    n = len(y)
    idx = rng.integers(0, n, size=(B, n))
    yb, pb = y[idx], pred[idx]
    yc = yb - yb.mean(1, keepdims=True)
    pc = pb - pb.mean(1, keepdims=True)
    den = (pc * pc).sum(1)
    sl = np.where(den > 0, (yc * pc).sum(1) / np.where(den > 0, den, 1), np.nan)
    return [float(np.nanpercentile(sl, q)) for q in (2.5, 97.5)]

def binom_ceiling(pi_hat, n):
    pi = np.clip(pi_hat, 1e-4, 1 - 1e-4)
    S = float(pi.var())
    F = float((pi * (1 - pi)).mean())
    return S / (S + F / n), S, F

def split_ceiling(ha, hb, yfull):
    """Leak-free rate ceiling: S = Cov(disjoint halves) estimates Var(true per-N
    rate pi) without any same-value contamination; w = Var(y_arm)-S is the
    within-N sampling variance at the arm size; C(n_arm) = S/Var(y_arm).
    Secondary 'pihat' ceiling from fitted probabilities kept for reference."""
    S = float(np.cov(ha, hb)[0, 1])
    V = float(np.var(yfull))
    C = S / V if V > 0 else float("nan")
    rho = float(np.corrcoef(ha, hb)[0, 1])
    return C, S, rho

FEATS = ["qrc", "w", "d"]

def design(rec, arm):
    X = np.column_stack([np.ones(NPOP), np.array(rec["qrc"]), np.array(rec["w"]),
                         np.array(rec[f"d_a{arm}"])])
    return X

# ---------------------------------------------------------------- stage 1-3: data
RESULT["data"] = {}
for bl in BITLENS:
    RESULT["data"][str(bl)] = build_bitlen(bl)
    save()
    log(f"stage: bitlen {bl} checkpointed")
DATA = RESULT["data"]

# ---------------------------------------------------------------- stage 4: analysis
log("stage 4: analysis")
perm = rng.permutation(NPOP)
TRAIN, TEST = perm[:SPLIT_TRAIN], perm[SPLIT_TRAIN:]
RESULT["analysis"] = {"split": {"train": TRAIN[:5].tolist() + ["..."], "note": f"seeded perm, {SPLIT_TRAIN}/300"}}
cells = []
for u in US:
    for arm in (80, 240):
        ykey = f"y_u{u}_a{arm}"
        Y = {bl: np.array(DATA[str(bl)][ykey]) for bl in BITLENS}
        X = {bl: design(DATA[str(bl)], arm) for bl in BITLENS}

        # --- fit at 44
        b44, se44, t44 = ols(X[44][TRAIN], Y[44][TRAIN])
        r2_tr = r2(Y[44][TRAIN], X[44][TRAIN] @ b44)
        r2_te = r2(Y[44][TEST], X[44][TEST] @ b44)
        b44f, se44f, t44f = ols(X[44], Y[44])           # full-pop fit (H3 at 44, ceilings)
        pi44 = X[44] @ b44f
        cp44, _, _ = binom_ceiling(pi44, arm)
        cs44, Ss44, rho44 = split_ceiling(np.array(DATA["44"][f"h_u{u}_a{arm}_e"]),
                                          np.array(DATA["44"][f"h_u{u}_a{arm}_o"]), Y[44])
        Xnd44 = X[44][:, :3]                             # no-d ablation (qrc,w only)
        bnd, *_ = np.linalg.lstsq(Xnd44[TRAIN], Y[44][TRAIN], rcond=None)
        r2_te_nd = r2(Y[44][TEST], Xnd44[TEST] @ bnd)

        cell = {"u": u, "arm": arm, "bl44": {
            "beta": [round(float(x), 5) for x in b44],
            "se": [round(float(x), 5) for x in se44],
            "t": [round(float(x), 2) for x in t44],
            "t_d_full": round(float(t44f[3]), 2),
            "R2_train": round(r2_tr, 4), "R2_test": round(r2_te, 4),
            "R2_test_nod": round(r2_te_nd, 4),
            "ceiling_split": round(cs44, 4), "S_split": round(Ss44, 7),
            "rho_halves": round(rho44, 4), "ceiling_pihat": round(cp44, 4)}}

        # --- transfer to 48/52
        for bl in (48, 52):
            pred = X[bl] @ b44
            pred = pred + (Y[bl].mean() - pred.mean())   # renormalized intercept
            sl = calib_slope(Y[bl], pred)
            lo, hi = boot_slope_ci(Y[bl], pred)
            r2_x = r2(Y[bl], pred)
            bf, sf, tf = ols(X[bl], Y[bl])               # fresh in-population fit
            r2_f = r2(Y[bl], X[bl] @ bf)
            pi = X[bl] @ bf
            cp, _, _ = binom_ceiling(pi, arm)
            cs, Ss, rh = split_ceiling(np.array(DATA[str(bl)][f"h_u{u}_a{arm}_e"]),
                                       np.array(DATA[str(bl)][f"h_u{u}_a{arm}_o"]), Y[bl])
            bndf, *_ = np.linalg.lstsq(X[bl][:, :3], Y[bl], rcond=None)
            r2_f_nd = r2(Y[bl], X[bl][:, :3] @ bndf)
            cell[f"bl{bl}"] = {
                "R2_transfer": round(r2_x, 4), "slope": round(sl, 4),
                "slope_CI": [round(lo, 4), round(hi, 4)], "H1_pass": bool(0.8 <= sl <= 1.25),
                "R2_fresh": round(r2_f, 4), "R2_fresh_nod": round(r2_f_nd, 4),
                "t_d_full": round(float(tf[3]), 2),
                "ceiling_split": round(cs, 4), "S_split": round(Ss, 7),
                "ceiling_pihat": round(cp, 4),
                "fresh_gap_split": round(cs - r2_f, 4)}
        cells.append(cell)
        log(f"cell u={u} arm={arm}: 44 test R2={r2_te:.4f} (nod {r2_te_nd:.4f}) | " +
            " | ".join(f"bl{bl}: xfer={cell[f'bl{bl}']['R2_transfer']:.4f} "
                       f"slope={cell[f'bl{bl}']['slope']:.3f}"
                       f"[{cell[f'bl{bl}']['slope_CI'][0]:.3f},{cell[f'bl{bl}']['slope_CI'][1]:.3f}] "
                       f"fresh={cell[f'bl{bl}']['R2_fresh']:.4f}(nod {cell[f'bl{bl}']['R2_fresh_nod']:.4f}) "
                       f"ceil={cell[f'bl{bl}']['ceiling_split']:.4f}"
                       for bl in (48, 52)))
RESULT["analysis"]["cells"] = cells
save()

# ---------------------------------------------------------------- verdicts
v = {"H1": {}, "H2": {}, "H3": {}}
h1_cells, h3_ts = [], []
for c in cells:
    for bl in (48, 52):
        h1_cells.append((c["u"], c["arm"], bl, c[f"bl{bl}"]["slope"], c[f"bl{bl}"]["slope_CI"]))
        h3_ts.append(abs(c[f"bl{bl}"]["t_d_full"]))
    h3_ts.append(abs(c["bl44"]["t_d_full"]))

prim = [x for x in h1_cells if x[0] == 2.5]
v["H1"] = {
    "primary_u2.5": [{"u": uu, "arm": aa, "bl": bb, "slope": ss, "CI": ci,
                      "pass": bool(0.8 <= ss <= 1.25)} for uu, aa, bb, ss, ci in prim],
    "all_cells_pass": all(0.8 <= ss <= 1.25 for _, _, _, ss, _ in h1_cells),
    "min_slope": min(ss for *_, ss, _ in h1_cells),
    "max_slope": max(ss for *_, ss, _ in h1_cells)}

# assemble 80-vs-240 comparisons per (u, bl) using fresh fits + split ceilings
h2_rows = []
for u in US:
    for bl in (48, 52):
        c80 = next(c for c in cells if c["u"] == u and c["arm"] == 80)
        c240 = next(c for c in cells if c["u"] == u and c["arm"] == 240)
        e80, e240 = c80[f"bl{bl}"], c240[f"bl{bl}"]
        h2_rows.append({
            "u": u, "bl": bl,
            "R2_fresh_80": e80["R2_fresh"], "R2_fresh_240": e240["R2_fresh"],
            "R2_nod_80": e80["R2_fresh_nod"], "R2_nod_240": e240["R2_fresh_nod"],
            "ceil_80": e80["ceiling_split"], "ceil_240": e240["ceiling_split"],
            "gap_80": round(e80["ceiling_split"] - e80["R2_fresh"], 4),
            "gap_240": round(e240["ceiling_split"] - e240["R2_fresh"], 4),
            "R2_rises": e240["R2_fresh"] > e80["R2_fresh"],
            "frac_of_ceiling_80": round(e80["R2_fresh"] / e80["ceiling_split"], 3) if e80["ceiling_split"] > 0 else None,
            "frac_of_ceiling_240": round(e240["R2_fresh"] / e240["ceiling_split"], 3) if e240["ceiling_split"] > 0 else None})
v["H2"]["rows"] = h2_rows
v["H2"]["rises_toward_ceiling"] = all(r["R2_rises"] for r in h2_rows)
v["H2"]["ceiling_direction_80_to_240"] = (
    "rises" if all(r["ceil_240"] > r["ceil_80"] for r in h2_rows)
    else "falls" if all(r["ceil_240"] < r["ceil_80"] for r in h2_rows)
    else "mixed")
v["H2"]["note"] = ("split ceiling C=S/Var(y) with S=Cov(disjoint halves) is leak-free; "
                   "the pre-stated 'ceiling halves at 240' clause refers to the binomial "
                   "floor which actually QUARTERS (F/n, n 80->240), so the rate ceiling RISES; "
                   "d(N) reads realized divisibility of the SAME values as y and can lift the "
                   "augmented dial above the pure rate ceiling at small n")
v["H3"] = {"min_abs_t_d": round(min(h3_ts), 2), "pass_ge2": bool(min(h3_ts) >= 2.0),
           "n_cells": len(h3_ts)}

RESULT["verdicts"] = v
RESULT["wall_seconds"] = round(time.time() - T0, 1)
save()
log("final checkpoint written")

# ---------------------------------------------------------------- report
print("\n=== EXP-478 FOOTPRINT-SCALE ===")
print(f"paper-145 anchor (bl44, u2.5, arm80): our test R2={next(c for c in cells if c['u']==2.5 and c['arm']==80)['bl44']['R2_test']} vs paper 0.5864 (different draw/split)")
print("\nR^2 vs ceiling table (augmented dial = qrc+w+d; nod = qrc+w ablation):")
print(f"{'u':>4} {'bl':>3} {'arm':>4} {'R2_aug':>7} {'R2_nod':>7} {'ceil_split':>10} {'ceil_pihat':>10} {'S_split':>10}")
for u in US:
    for arm in (80, 240):
        cc = next(c for c in cells if c["u"] == u and c["arm"] == arm)
        b44 = cc["bl44"]
        print(f"{u:>4} {44:>3} {arm:>4} {b44['R2_test']:>7.4f} {b44['R2_test_nod']:>7.4f} "
              f"{b44['ceiling_split']:>10.4f} {b44['ceiling_pihat']:>10.4f} {b44['S_split']:>10.7f}")
        for bl in (48, 52):
            c = cc[f"bl{bl}"]
            print(f"{u:>4} {bl:>3} {arm:>4} {c['R2_fresh']:>7.4f} {c['R2_fresh_nod']:>7.4f} "
                  f"{c['ceiling_split']:>10.4f} {c['ceiling_pihat']:>10.4f} {c['S_split']:>10.7f}")
print("\nVERDICTS")
print("H1 (transfer slope in [0.8,1.25]):", json.dumps(v["H1"]["primary_u2.5"]),
      "| all-cells pass:", v["H1"]["all_cells_pass"])
print("H2 rows:", json.dumps(h2_rows))
print("H2 rises_toward_ceiling:", v["H2"]["rises_toward_ceiling"],
      "| ceiling direction 80->240:", v["H2"]["ceiling_direction_80_to_240"])
print("H3 d(N) min |t| =", v["H3"]["min_abs_t_d"], "over", v["H3"]["n_cells"],
      "cells -> pass_ge2:", v["H3"]["pass_ge2"])
print(f"\nwall: {RESULT['wall_seconds']}s | result.json at {WORK}/result.json")

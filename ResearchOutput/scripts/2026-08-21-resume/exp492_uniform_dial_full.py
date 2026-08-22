#!/usr/bin/env python3
# =============================================================================
# EXP 492 "UNIFORM-DIAL" (round-43) — validate the per-N relation-yield dial
# (papers 145/147: footprint w(N) = sum 2/p over QR primes <= 400, plus
#  divisibility fraction d(N)) on UNIFORM draws. Until now the dial was
# validated only on BALANCED draws; paper 158 showed draw regime shifts method
# cost slopes (trial division alpha 1.00 -> 1.14 under uniform), and paper 154
# flagged this dial's regime-robustness as the open question.
#
# FILENOTE: originally written as exp492_uniform_dial.py; that filename was
# overwritten mid-task by a foreign "lean takeover" implementation (different
# design: 1200 Ns, 120 values, 900/300, pooled B, no bitlen arms). Its script
# and output are preserved as exp492_uniform_dial_LEAN_TAKEOVER_foreign.py /
# result_lean_takeover.json. This file is the FULL brief design, unmodified.
#
# PRE-STATED HYPOTHESES (written BEFORE any data collection):
#   H1 (shape transfer): QR-count / footprint features remain the TOP
#      predictors on uniform-draw populations at u = 2.5 —
#      Spearman(rate, qrc) > 0.4 AND Spearman(rate, w) > 0.4 in BOTH uniform
#      cells, and they outrank the other dial features.
#   H2 (absolute R^2 drops): R^2_uniform < R^2_balanced - 0.05
#      (augmented model, matched bitlen, averaged over bitlen in {40,44};
#      q/p spread widens the gap-size distribution, diluting residue-structure
#      variance share).
#   H3 (footprint weighting gains weight): the footprint feature w matters
#      relatively MORE under uniform draws than the plain count —
#      DeltaR^2_uniform = R^2_aug - R^2_base >= +0.02
#      (secondary clause: the uniform Delta exceeds the balanced Delta).
#
# DESIGN (verbatim from brief):
#   - 1500 semiprimes per (arm, bitlen), arm in {balanced, uniform},
#     bitlen in {40, 44}; per-cell OLS train/test = 1200/300.
#   - balanced: p, q uniform primes near 2^(k/2) (both in
#     [ceil(sqrt(2^(k-1))), isqrt(2^k - 1)]), N forced to exact bitlen k.
#   - uniform: p uniform prime in [2^10, 2^22); q uniform prime in
#     [ceil(2^(k-1)/p), floor((2^k-1)/p)] (exact-bitlen feasible range) —
#     a genuinely unbalanced mix, q/p spanning ~2^0 .. ~2^20.
#   - 240 relation values per N; smoothness at u(median v) = 2.5:
#     B = exp(ln v_med / 2.5); strip primes <= B; rate = fraction of the 240
#     values that strip to 1.
#   - Features verbatim from paper 145 conventions:
#       qrc  = #{odd primes p <= 100 : N is a QR mod p} (gmpy2.powmod Euler
#              criterion, r = powmod(N mod p, (p-1)/2, p) == 1)
#       w    = sum over odd primes p <= 400 with N a QR mod p of 2/p
#       d1   = divisibility fraction over p <= 13 (fraction of the six primes
#              2,3,5,7,11,13 that divide N)
#   - Bootstrap CIs (300 resamples, percentile) on all headline numbers.
#
# PRE-STATED DESIGN OBSERVATIONS (before data):
#   D1: under BOTH arms of this brief min(p,q) >= 2^10 = 1024 > 13, so d1 is
#       STRUCTURALLY ZERO in every cell — the p<=13 divisibility channel is
#       inert in these populations by construction. The augmented model
#       [qrc, w, d1] therefore reduces to [qrc, w] and DeltaR^2 measures
#       exactly the w-over-count increment H3 asks about. We additionally
#       compute a labeled NON-verbatim variant d2 = fraction of the 240
#       relation values divisible by some prime <= 13 (relation-level
#       divisibility), reported alongside but not part of primary verdicts.
#   D2: relation values use the reconstructed QS-window convention
#       v_i = (isqrt(N) + i)^2 - N, i = 1..240 (all positive). This is the
#       mechanistically correct family for QR features: p | v_i iff N is a QR
#       mod p whenever p does not divide (isqrt(N)+i), which is precisely the
#       channel qrc/w read. u is pinned per-N via its own median v.
#   D3: B can exceed the small factor p for the thin slice of uniform-arm Ns
#       with p in [1024, ~4200] (~0.1% of draws); for those, p itself is a
#       legal strip prime (p | v_i iff p | (a+i)) — kept, convention verbatim.
#
# BARRIERS (standard lines):
#   Barrier 5 (structural orthogonality): qrc/w/d are N-only natural
#     coordinates; the dial predicts relation YIELD (difficulty), not
#     (p,q) — no which-factor claim is made or tested here.
#   Barrier 8 (known-method-in-disguise): the measured object is the
#     QS/CFRAC relation-yield dial itself — a cost predictor FOR known
#     methods, not a new factoring route.
#
# Seed 20260924. Work dir /tmp/exp43_unif/. Checkpoints: result.json per stage.
# =============================================================================
import json, math, time, os
import numpy as np
import gmpy2

SEED       = 20260924
T_START    = time.time()
OUT        = "/tmp/exp43_unif"
K_LIST     = [40, 44]
ARMS       = ["balanced", "uniform"]
N_PER      = 1500
N_TRAIN    = 1200
N_TEST     = 300          # 1200 + 300 = 1500
M_REL      = 240          # relation values per N
U_TARGET   = 2.5          # u(median v)
N_BOOT     = 300

RESULT = os.path.join(OUT, "result.json")
_res = {"exp": "492", "codename": "UNIFORM-DIAL", "seed": SEED,
        "round": 43, "script": "exp492_uniform_dial_full.py",
        "started": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "takeover_note": ("exp492_uniform_dial.py was overwritten mid-task by a foreign lean "
                          "implementation; preserved as exp492_uniform_dial_LEAN_TAKEOVER_foreign.py "
                          "and result_lean_takeover.json. That independent run agrees directionally "
                          "(H1 true / H2 false / H3 true)."),
        "hypotheses": {
            "H1": "Spearman(rate,qrc) > 0.4 AND Spearman(rate,w) > 0.4 in both uniform cells, top-ranked",
            "H2": "R2_aug_uniform < R2_aug_balanced - 0.05 (bitlen-averaged)",
            "H3": "DeltaR2_uniform = R2_aug - R2_base >= +0.02 under uniform draws (secondary: exceeds balanced Delta)"},
        "design_observations": ["D1 d1 structurally zero under both arms (min factor >= 2^10 > 13)",
                                "D2 relation values v_i = (isqrt(N)+i)^2 - N, i=1..240 (QS window)",
                                "D3 B may exceed small p for ~0.1% of uniform draws; convention kept"],
        "stages": {}}

def save():
    with open(RESULT, "w") as f:
        json.dump(_res, f, indent=1, default=str)

def stage(name, payload):
    _res["stages"][name] = payload
    save()
    print(f"[stage {name}] saved ({time.strftime('%H:%M:%S')})", flush=True)

# ---------------------------------------------------------------- primes ----
ARM_IDX = {"balanced": 0, "uniform": 1}   # deterministic; NEVER hash() strings
                                         # into rng seeds (PYTHONHASHSEED is
                                         # randomized per process -- run-to-run
                                         # drift until this was fixed)

def sieve(n):
    m = np.ones(n + 1, dtype=bool); m[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if m[i]: m[i*i::i] = False
    return np.flatnonzero(m).tolist()

PRIMES_STRIP = sieve(20000)                       # covers B up to ~4300 with huge margin
P_ODD_400    = [p for p in sieve(400) if p >= 3]  # 78 primes
P_ODD_100    = [p for p in P_ODD_400 if p <= 100] # 25 primes
P13          = [2, 3, 5, 7, 11, 13]

# ------------------------------------------------------------ populations ---
def ceil_sqrt(x):
    s = int(gmpy2.isqrt(x))
    return s if s * s == x else s + 1

def rand_prime(lo, hi, rng):
    while True:
        c = int(rng.integers(lo, hi + 1))
        p = int(gmpy2.next_prime(c))
        if p <= hi:
            return p

def draw_balanced(k, rng):
    lo = ceil_sqrt(1 << (k - 1)); hi = int(gmpy2.isqrt((1 << k) - 1))
    while True:
        p = rand_prime(lo, hi, rng); q = rand_prime(lo, hi, rng)
        if q == p: continue
        N = p * q
        if N.bit_length() == k:
            return p, q, N

def draw_uniform(k, rng):
    while True:
        p = rand_prime(1 << 10, (1 << 22) - 1, rng)
        qlo = ((1 << (k - 1)) + p - 1) // p
        qhi = ((1 << k) - 1) // p
        if qhi < qlo: continue
        q = rand_prime(qlo, qhi, rng)
        if q == p: continue
        N = p * q
        assert N.bit_length() == k
        return p, q, N

t0 = time.time()
pop = {}
for arm in ARMS:
    for k in K_LIST:
        rng = np.random.default_rng([SEED, 1, ARM_IDX[arm], k])
        rows = []
        while len(rows) < N_PER:
            p, q, N = (draw_balanced if arm == "balanced" else draw_uniform)(k, rng)
            rows.append((N, p, q))
        pop[(arm, k)] = rows
        print(f"populated {arm} k={k}: {len(rows)} Ns", flush=True)

pop_summary = {}
for arm in ARMS:
    for k in K_LIST:
        arr = np.array(pop[(arm, k)], dtype=np.int64)
        ratio = np.log2(arr[:, 2] / arr[:, 1])          # log2(q/p)
        small = np.minimum(arr[:, 1], arr[:, 2])
        pop_summary[f"{arm}_{k}"] = {
            "n": N_PER,
            "log2_qp_quantiles": np.percentile(ratio, [0, 25, 50, 75, 100]).round(3).tolist(),
            "min_factor_quantiles": np.percentile(small, [0, 50, 100]).tolist(),
            "d1_possible": bool(small.min() <= 13)}
stage("populations", {"summary": pop_summary, "sec": round(time.time() - t0, 1)})

np.savez(os.path.join(OUT, "populations.npz"),
         **{f"{arm}_{k}": np.array(pop[(arm, k)], dtype=np.int64)
            for arm in ARMS for k in K_LIST})

# --------------------------------------------------------------- features ---
def features(N):
    qrc = 0; w = 0.0
    for p in P_ODD_400:
        r = int(gmpy2.powmod(N % p, (p - 1) >> 1, p))
        if r == 1:
            if p <= 100: qrc += 1
            w += 2.0 / p
    d1 = sum(1 for p in P13 if N % p == 0) / len(P13)
    return qrc, w, d1

t0 = time.time()
feat = {}
for arm in ARMS:
    for k in K_LIST:
        rows = pop[(arm, k)]
        vals = np.array([features(N) for (N, p, q) in rows], dtype=np.float64)
        feat[(arm, k)] = vals
        print(f"features {arm} k={k}: qrc mean {vals[:,0].mean():.2f}, "
              f"w mean {vals[:,1].mean():.3f}, d1 nonzero {int((vals[:,2] > 0).sum())}", flush=True)
stage("features", {
    "sec": round(time.time() - t0, 1),
    "per_cell": {f"{arm}_{k}": {"qrc_mean": float(feat[(arm,k)][:,0].mean()),
                                 "qrc_sd": float(feat[(arm,k)][:,0].std()),
                                 "w_mean": float(feat[(arm,k)][:,1].mean()),
                                 "w_sd": float(feat[(arm,k)][:,1].std()),
                                 "d1_nonzero": int((feat[(arm,k)][:,2] > 0).sum())}
                 for arm in ARMS for k in K_LIST}})

# ------------------------------------------------- relations + smoothness ---
OFFS = np.arange(1, M_REL + 1, dtype=np.int64)
CHUNK = 250

def rates_for_cell(rows):
    """Returns rate (per-N smooth fraction), vmed, B, d2 per N."""
    n = len(rows)
    Ns = np.array([r[0] for r in rows], dtype=np.int64)
    rate = np.empty(n); vmed = np.empty(n); Bv = np.empty(n); d2 = np.empty(n)
    for s in range(0, n, CHUNK):
        sl = slice(s, min(s + CHUNK, n))
        A = np.array([int(gmpy2.isqrt(int(N))) for N in Ns[sl]], dtype=np.int64)[:, None]
        V = (A + OFFS[None, :]) ** 2 - Ns[sl][:, None]          # (c, 240) int64
        # d2: fraction of relation values divisible by some prime <= 13
        mask = np.zeros(V.shape, dtype=bool)
        for p in P13:
            mask |= (V % p == 0)
        d2[sl] = mask.mean(axis=1)
        med = np.median(V.astype(np.float64), axis=1)
        vmed[sl] = med
        B = np.exp(np.log(med) / U_TARGET)
        Bv[sl] = B
        Bint = np.floor(B).astype(np.int64)
        sm = np.ones(V.shape, dtype=bool)
        for p in PRIMES_STRIP:
            rmask = Bint >= p
            if not rmask.any(): break
            sub = V[rmask]
            while True:
                divm = (sub % p == 0)
                if not divm.any(): break
                sub[divm] //= p
            V[rmask] = sub
        rate[sl] = (V == 1).mean(axis=1)
    return rate, vmed, Bv, d2

t0 = time.time()
rel = {}
for arm in ARMS:
    for k in K_LIST:
        rate, vmed, Bv, d2 = rates_for_cell(pop[(arm, k)])
        rel[(arm, k)] = (rate, vmed, Bv, d2)
        print(f"rates {arm} k={k}: mean {rate.mean():.4f}, median {np.median(rate):.4f}, "
              f"sd {rate.std():.4f}, B med {np.median(Bv):.0f}", flush=True)
stage("rates", {
    "sec": round(time.time() - t0, 1),
    "per_cell": {f"{arm}_{k}": {"rate_mean": float(rel[(arm,k)][0].mean()),
                                 "rate_median": float(np.median(rel[(arm,k)][0])),
                                 "rate_sd": float(rel[(arm,k)][0].std()),
                                 "rate_q": np.percentile(rel[(arm,k)][0], [10,50,90]).round(4).tolist(),
                                 "B_median": float(np.median(rel[(arm,k)][2])),
                                 "d2_mean": float(rel[(arm,k)][3].mean())}
                 for arm in ARMS for k in K_LIST}})

np.savez(os.path.join(OUT, "dial_data.npz"),
         **{f"{arm}_{k}_{name}": arr for arm in ARMS for k in K_LIST
            for name, arr in zip(["rate","vmed","B","d2"], rel[(arm, k)])},
         **{f"{arm}_{k}_feat": feat[(arm, k)] for arm in ARMS for k in K_LIST})

# -------------------------------------------------------------- statistics --
def rankdata(a):
    a = np.asarray(a, dtype=np.float64)
    order = np.argsort(a, kind="mergesort")
    sa = a[order]; ranks = np.empty(len(a))
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and sa[j + 1] == sa[i]: j += 1
        ranks[order[i:j+1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return ranks

def spearman(x, y):
    rx, ry = rankdata(x), rankdata(y)
    rx = rx - rx.mean(); ry = ry - ry.mean()
    den = math.sqrt((rx @ rx) * (ry @ ry))
    return float(rx @ ry / den) if den > 0 else float("nan")

def ols_fit(X, y):
    X1 = np.column_stack([np.ones(len(X)), X])
    beta, *_ = np.linalg.lstsq(X1, y, rcond=None)
    return beta

def ols_r2(beta, X, y):
    X1 = np.column_stack([np.ones(len(X)), X])
    pred = X1 @ beta
    ss_res = float(((y - pred) ** 2).sum()); ss_tot = float(((y - y.mean()) ** 2).sum())
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")

def ci95(arr):
    lo, hi = np.percentile(arr, [2.5, 97.5])
    return [round(float(lo), 5), round(float(hi), 5)]

FEATS = ["qrc", "w", "d1", "d2", "log2qp"]
MODELS = {"base":   ["qrc"],
          "aug":    ["qrc", "w", "d1"],
          "aug_d2": ["qrc", "w", "d2"]}

t0 = time.time()
cells = {}
for arm in ARMS:
    for k in K_LIST:
        rng = np.random.default_rng([SEED, 2, ARM_IDX[arm], k])
        f = feat[(arm, k)]; rate, vmed, Bv, d2v = rel[(arm, k)]
        rows = np.array(pop[(arm, k)], dtype=np.int64)
        log2qp = np.log2(rows[:, 2] / rows[:, 1])
        cols = {"qrc": f[:, 0], "w": f[:, 1], "d1": f[:, 2],
                "d2": d2v, "log2qp": log2qp}
        perm = rng.permutation(N_PER)
        tr, te = perm[:N_TRAIN], perm[N_TRAIN:]
        y = rate
        # point estimates (test R^2)
        betas, point_r2 = {}, {}
        for mname, mcols in MODELS.items():
            Xtr = np.column_stack([cols[c][tr] for c in mcols])
            Xte = np.column_stack([cols[c][te] for c in mcols])
            betas[mname] = ols_fit(Xtr, y[tr])
            point_r2[mname] = ols_r2(betas[mname], Xte, y[te])
        # test predictions cached for bootstrap
        test_pred = {}
        for mname, mcols in MODELS.items():
            Xte1 = np.column_stack([np.ones(N_TEST)] +
                                   [cols[c][te] for c in mcols])
            test_pred[mname] = Xte1 @ betas[mname]
        yte = y[te]
        # bootstrap: R2 per model (paired across models, resample test rows);
        # spearman per feature (resample all rows)
        boot_r2 = {m: np.empty(N_BOOT) for m in MODELS}
        boot_sp = {fname: np.empty(N_BOOT) for fname in FEATS}
        for b in range(N_BOOT):
            idx_te = rng.integers(0, N_TEST, N_TEST)
            ss_tot = ((yte[idx_te] - yte[idx_te].mean()) ** 2).sum()
            for m in MODELS:
                pp = test_pred[m][idx_te]
                boot_r2[m][b] = 1.0 - ((yte[idx_te] - pp) ** 2).sum() / ss_tot
            idx_all = rng.integers(0, N_PER, N_PER)
            for fname in FEATS:
                boot_sp[fname][b] = spearman(cols[fname][idx_all], y[idx_all])
        point_sp = {fname: spearman(cols[fname], y) for fname in FEATS}
        cells[f"{arm}_{k}"] = {
            "spearman": {fname: round(point_sp[fname], 4) for fname in FEATS},
            "spearman_ci": {fname: ci95(boot_sp[fname]) for fname in FEATS},
            "r2": {m: round(point_r2[m], 5) for m in MODELS},
            "r2_ci": {m: ci95(boot_r2[m]) for m in MODELS},
            "delta_aug_minus_base": round(point_r2["aug"] - point_r2["base"], 5),
            "delta_aug_minus_base_ci": ci95(boot_r2["aug"] - boot_r2["base"]),
            "coefs": {m: [round(float(x), 6) for x in betas[m]] for m in MODELS},
            "boot": boot_r2}
        print(f"stats {arm}_{k}: sp(qrc)={point_sp['qrc']:.3f} sp(w)={point_sp['w']:.3f} "
              f"sp(d2)={point_sp['d2']:.3f} sp(log2qp)={point_sp['log2qp']:.3f} "
              f"R2base={point_r2['base']:.4f} R2aug={point_r2['aug']:.4f} "
              f"delta={point_r2['aug']-point_r2['base']:+.4f}", flush=True)

# contrasts (bootstrap arrays are independent across cells)
H2_drops, H3s = {}, {}
for k in K_LIST:
    pt = cells[f"balanced_{k}"]["r2"]["aug"] - cells[f"uniform_{k}"]["r2"]["aug"]
    arr = cells[f"balanced_{k}"]["boot"]["aug"] - cells[f"uniform_{k}"]["boot"]["aug"]
    H2_drops[k] = (round(pt, 5), ci95(arr), arr)
pt_mean = float(np.mean([H2_drops[k][0] for k in K_LIST]))
arr_mean = (H2_drops[40][2] + H2_drops[44][2]) / 2.0

for arm in ARMS:
    pts = [cells[f"{arm}_{k}"]["delta_aug_minus_base"] for k in K_LIST]
    arrs = [cells[f"{arm}_{k}"]["boot"]["aug"] - cells[f"{arm}_{k}"]["boot"]["base"] for k in K_LIST]
    H3s[arm] = (float(np.mean(pts)), ci95((arrs[0] + arrs[1]) / 2.0))

out_cells = {name: {kk: vv for kk, vv in c.items() if kk != "boot"}
             for name, c in cells.items()}
stage("stats", {"cells": out_cells, "sec": round(time.time() - t0, 1),
                "contrasts": {
                    "H2_drop_per_bitlen": {str(k): {"point": H2_drops[k][0], "ci95": H2_drops[k][1]} for k in K_LIST},
                    "H2_drop_mean": {"point": round(pt_mean, 5), "ci95": ci95(arr_mean)},
                    "H3_delta_uniform": {"point": round(H3s["uniform"][0], 5), "ci95": H3s["uniform"][1]},
                    "H3_delta_balanced": {"point": round(H3s["balanced"][0], 5), "ci95": H3s["balanced"][1]}}})

# --------------------------------------------------------------- verdicts ---
unif_cells = [f"uniform_{k}" for k in K_LIST]
sp_qrc_ok = all(cells[c]["spearman"]["qrc"] > 0.4 for c in unif_cells)
sp_w_ok   = all(cells[c]["spearman"]["w"] > 0.4 for c in unif_cells)
others    = ["d1", "d2", "log2qp"]
# top-rank check: skip NaN (zero-variance) features; compare |sp| against qrc/w
top_ok    = all(not (cells[c]["spearman"][f] == cells[c]["spearman"][f]) or
                abs(cells[c]["spearman"][f]) <= max(abs(cells[c]["spearman"]["qrc"]),
                                                    abs(cells[c]["spearman"]["w"])) + 1e-12
                for c in unif_cells for f in others)
H1 = "TRUE" if (sp_qrc_ok and sp_w_ok and top_ok) else ("PARTIAL" if (sp_qrc_ok or sp_w_ok) else "REFUTED")

drop_pt, drop_ci = round(pt_mean, 5), ci95(arr_mean)
if drop_pt >= 0.05 and drop_ci[0] > 0:
    H2 = "TRUE"
elif drop_pt > 0 and drop_ci[0] > 0:
    H2 = "PARTIAL (positive drop, below 0.05 bar)"
else:
    H2 = "REFUTED"

d_unif_pt, d_unif_ci = round(H3s["uniform"][0], 5), H3s["uniform"][1]
d_bal_pt, d_bal_ci = round(H3s["balanced"][0], 5), H3s["balanced"][1]
H3_primary = (d_unif_pt >= 0.02 and d_unif_ci[0] > 0)
H3_secondary = d_unif_pt > d_bal_pt
H3 = "TRUE" if H3_primary else "REFUTED"

verdicts = {
    "H1": {"verdict": H1,
           "uniform_sp_qrc": {c: cells[c]["spearman"]["qrc"] for c in unif_cells},
           "uniform_sp_w": {c: cells[c]["spearman"]["w"] for c in unif_cells},
           "top_rank_ok": bool(top_ok)},
    "H2": {"verdict": H2, "drop_mean": drop_pt, "drop_ci95": drop_ci,
           "per_bitlen": {str(k): {"point": H2_drops[k][0], "ci95": H2_drops[k][1]} for k in K_LIST}},
    "H3": {"verdict": H3, "delta_uniform": d_unif_pt, "delta_uniform_ci95": d_unif_ci,
           "delta_balanced": d_bal_pt, "delta_balanced_ci95": d_bal_ci,
           "secondary_uniform_exceeds_balanced": bool(H3_secondary)}}
_res["verdicts"] = verdicts
_res["barrier_lines"] = {
    "barrier_5": "Structural orthogonality: qrc/w/d are N-only natural coordinates; the dial predicts relation yield (difficulty), not (p,q) - no which-factor claim made or tested.",
    "barrier_8": "Known-method-in-disguise: the measured object is the QS/CFRAC relation-yield dial - a cost predictor FOR known methods, not a new factoring route."}
save()

# ----------------------------------------------------------------- ledger ---
headline = (f"UNIFORM-DIAL exp492: H1={H1} H2={H2} H3={H3}; "
            f"uniform sp(qrc)={[cells[c]['spearman']['qrc'] for c in unif_cells]}, "
            f"sp(w)={[cells[c]['spearman']['w'] for c in unif_cells]}; "
            f"R2aug unif/bal per bitlen: "
            f"{ {k: (cells[f'uniform_{k}']['r2']['aug'], cells[f'balanced_{k}']['r2']['aug']) for k in K_LIST} }; "
            f"H2 drop {drop_pt} CI {drop_ci}; H3 delta unif {d_unif_pt} CI {d_unif_ci}, "
            f"bal {d_bal_pt} CI {d_bal_ci}")
ledger_line = {
    "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "round": 43, "exp": 492,
    "codename": "UNIFORM-DIAL", "seed": SEED, "status": "DONE",
    "headline": headline, "verdicts": verdicts,
    "barriers": ["5", "8"],
    "artifacts": ["/tmp/exp43_unif/exp492_uniform_dial_full.py", RESULT,
                  "/tmp/exp43_unif/dial_data.npz", "/tmp/exp43_unif/populations.npz",
                  "/tmp/exp43_unif/result_lean_takeover.json"]}
with open(os.path.join(OUT, "ledger_exp492.jsonl"), "w") as f:
    f.write(json.dumps(ledger_line, default=str) + "\n")
with open(os.path.join(OUT, "ledger_round43.md"), "w") as f:
    f.write(f"- **Round-43 #492 UNIFORM-DIAL (exp 492, seed 20260924):** {headline} "
            f"Barriers 5/8. Artifacts: /tmp/exp43_unif/ (script exp492_uniform_dial_full.py, "
            f"result.json, dial_data.npz; foreign lean-takeover script/output preserved with "
            f"LEAN_TAKEOVER/lean_takeover names).\n")

print("\n=== FINAL VERDICTS ===")
print(json.dumps(verdicts, indent=1))
print(f"\ntotal wall time {time.time() - T_START:.0f}s -> artifacts in {OUT}")

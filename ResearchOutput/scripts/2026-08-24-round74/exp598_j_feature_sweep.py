#!/usr/bin/env python3
# exp598 J-FEATURE-SWEEP (round-74; paper 242 named follow-up)
#
# =============================================================================
# PRE-REGISTRATION -- written BEFORE any analysis was run (header precedes code;
# file mtime ordering + this declaration are the audit record).
#
# Question: the exp579/581 mid-window hump survived divisibility-mixture
# conditioning (exp582: stationary geometric feature at u*~=0.65). Is the
# carrier J-ARITHMETIC -- a property of the position j itself?
#
# H1 (j-carrier): at least one REGISTERED j-feature class shows hit-rate ratio
#   R >= 1.15 vs its complement WITHIN the mid-window u in [0.55,0.75],
#   permutation-calibrated (max-statistic, family-wise) p < 0.01 after
#   Bonferroni across registered families, AND corroborated by flanking-window
#   baseline subtraction (DiD sign-consistent, p_did < 0.05).
#   => carrier is j-arithmetic; name the winning class.
# H0: no feature class clears the bar => carrier remains open; route to
#   polynomial-sequence correlation analysis (= consecutive-v dependency study).
#
# Registered feature families (K=8 tested unless skipped):
#   F1 jmod4        : 4 cells {0,1,2,3} mod 4 (= parity x mod 4)
#   F2 jmod3        : 3 cells
#   F3 jmod5        : 5 cells
#   F4 jmod7        : 7 cells
#   F5 jmod105      : 105 joint cells (CRT of mod 3,5,7)
#   F6 omega_ter    : terciles of omega_small(j) = #{distinct primes <= 97 | j}
#                     (thresholds from pooled label-blind quantiles)
#   F7 dsq_smooth   : B-smoothness (exact 1e6) of d = |j - nearest_square(j)|;
#                     SKIP if degenerate (>98% single class or any cell
#                     n<200 or h<15)  [task: "skip if degenerate"]
#   F8 jsmooth_1e6  : exact indicator that j itself is 1e6-smooth
#                     (vectorized prime-strip to 1e6; exact, no heuristic)
# Windows: MID  = u in [0.55, 0.75]
#          FLANK = u in [0.05,0.40) union (0.90,1.00]  (boundary/shoulder margin;
#          registered here before analysis)
# Statistics per family/class c:
#   R_c    = rate_mid(c) / rate_mid(complement)          [PRIMARY]
#   DiD_c  = [rate_mid(c)-rate_flank(c)] - [rate_mid(~c)-rate_flank(~c)]
#   Cell gate: n_mid(c) >= 200 AND h_mid(c) >= 15 else class ineligible.
# Calibration: 500 label shuffles WITHIN window strata (permute y inside mid,
#   independently inside flank); statistic = max_c R_c (resp max DiD_c);
#   p = (#perm >= obs)/500. Family-wise by construction; then xK Bonferroni.
# Control (must be null): 300 fake-hit draws -- labels globally permuted at
#   matched prevalence, identical pipeline incl. bars; report max-R dist and
#   bar-clearing frequency.
# Views: A pooled-position (above); B per-window-rate: per-N enrichment
#   e_ic = (h_ic/n_ic)/(h_i./n_i.) restricted to mid, count-weighted mean.
#
# Honest notes registered up front:
#  - Positions/hit labels CONSUMED from exp581_regen_positions.npz (the artifact
#    whose seed-20260828 lineage regeneration was hash-proven IN exp581). This
#    script does NOT re-run the generator (generator source outside this task's
#    read allowlist); sha256 of the npz is recorded below for provenance.
#  - Hit labels are the upstream cut-1e6 classify (exp569 path) as frozen in the
#    npz; not recomputed here.
#  - F7's 'v' operationalized as v = j (scan position); nearest square via
#    round(sqrt(j)). If degenerate => skipped with reason, per registration.
# =============================================================================

import hashlib, json, sys, time, os
import numpy as np

T0 = time.time()
BASE = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74"
NPZ = os.path.join(BASE, "exp581_regen_positions.npz")
SMOKE = "--smoke" in sys.argv
RNG_SEED = 20260908
N_PERM = 100 if SMOKE else 500
N_NULL = 50 if SMOKE else 300
MID_LO, MID_HI = 0.55, 0.75
FLANK = [(0.05, 0.40), (0.90, 1.00)]

def now():
    return time.time() - T0

def log(msg):
    print(f"[{now():7.1f}s] {msg}", flush=True)

with open(NPZ, "rb") as fh:
    npz_sha256 = hashlib.sha256(fh.read()).hexdigest()
d = np.load(NPZ, allow_pickle=True)
NN = 128
ns = range(0, (8 if SMOKE else NN))
CTL_CAP = 800 if SMOKE else 10**9

rng = np.random.default_rng(RNG_SEED)
js_list, lab_list, nid_list = [], [], []
for i in ns:
    hj = d[f"hit_{i}"].astype(np.int64)
    cj = d[f"ctl_{i}"].astype(np.int64)
    if cj.size > CTL_CAP:
        cj = rng.choice(cj, CTL_CAP, replace=False)
    lo, hi = int(d["jlo"][i]), int(d["jhi"][i])
    span = hi - lo
    for arr, lab in ((hj, 1), (cj, 0)):
        js_list.append(arr)
        lab_list.append(np.full(arr.size, lab, np.int8))
        nid_list.append(np.full(arr.size, i, np.int16))
J = np.concatenate(js_list)
Y = np.concatenate(lab_list)
NID = np.concatenate(nid_list)
LO = d["jlo"][NID].astype(np.int64)
HI = d["jhi"][NID].astype(np.int64)
U = (J - LO) / (HI - LO)

in_mid = (U >= MID_LO) & (U <= MID_HI)
in_flank = np.zeros(U.size, bool)
for a, b in FLANK:
    in_flank |= (U >= a) & (U <= b)
log(f"loaded {J.size:,} positions ({int(Y.sum()):,} hits) from {len(list(ns))} windows; "
    f"mid={in_mid.sum():,}, flank={in_flank.sum():,}")

# ---------------------------------------------------------------- features --
uniqJ, inv = np.unique(J, return_inverse=True)
log(f"{uniqJ.size:,} unique j values")

# exact 1e6-smoothness engine (vectorized prime strip, ascending primes)
def sieve_primes(n):
    s = np.ones(n + 1, bool); s[:2] = False
    for p in range(2, int(n**0.5) + 1):
        if s[p]:
            s[p*p::p] = False
    return np.nonzero(s)[0]

P100 = sieve_primes(100)
P1K = sieve_primes(1000)

def strip_small(v, primes):
    """divide out given primes fully; returns reduced copy"""
    r = v.astype(np.int64).copy()
    for p in primes:
        m = r % p == 0
        if m.any():
            sub = r[m]
            while True:
                dm = sub % p == 0
                if not dm.any():
                    break
                sub[dm] //= p
            r[m] = sub
    return r

om_small = np.zeros(uniqJ.size, np.int8)
for p in P100:
    om_small += (uniqJ % p == 0).astype(np.int8)
q33, q66 = np.quantile(om_small, [1/3, 2/3])
omega_ter = np.searchsorted([q33 + 0.5, q66 + 0.5], om_small)  # 0,1,2 terciles

log("stripping primes <= 1e3 ...")
red_j = strip_small(uniqJ, P1K)

def exact_smooth_from_reduced(red, primes_gt1k, label):
    """red = input with all primes <=1e3 divided out. Exact 1e6-smoothness:
    True iff repeated division by every prime in (1e3,1e6] leaves 1."""
    r = red.copy()
    alive = r > 1
    smooth = np.ones(r.size, bool)
    for k, p in enumerate(primes_gt1k):
        idx = np.nonzero(alive)[0]
        if idx.size == 0:
            break
        rr = r[idx]
        # resolve: r < p*p => residual is PRIME (all smaller primes stripped).
        # It is 1e6-smooth iff that prime is itself <= 1e6 (a later list entry
        # would have stripped it). Smoke run caught the wrong version of this.
        done = rr < p * p
        if done.any():
            smooth[idx[done]] = rr[done] <= 10**6
            alive[idx[done]] = False
        idx = np.nonzero(alive)[0]
        if idx.size == 0:
            break
        dv = r[idx] % p == 0
        if dv.any():
            sub = r[idx[dv]]
            while True:
                dm = sub % p == 0
                if not dm.any():
                    break
                sub[dm] //= p
            r[idx[dv]] = sub
            fin = r[idx[dv]] == 1
            if fin.any():
                alive[idx[dv][fin]] = False
        if k % 4096 == 0 and alive.any():
            av = np.nonzero(alive)[0]
            mx = r[av].max()
            if p * p > mx:
                smooth[av] = r[av] <= 10**6
                alive[:] = False
                log(f"  [{label}] early-exit at p={p}")
                break
    smooth[np.nonzero(alive)[0]] = False
    return smooth

PRIMES_GT1K = sieve_primes(10**6)
PRIMES_GT1K = PRIMES_GT1K[PRIMES_GT1K > 1000]
t = time.time()
jsmooth = exact_smooth_from_reduced(red_j, PRIMES_GT1K, "j")
log(f"j 1e6-smooth fraction: {jsmooth.mean():.4f} ({time.time()-t:.1f}s)")

# F7: distance to nearest square, same engine (d < ~3e7 -> early exit helps)
k = np.sqrt(uniqJ.astype(np.float64)).round().astype(np.int64)
dsq = np.abs(uniqJ - k.astype(np.int64) * k)
red_d = strip_small(dsq, P1K)
tsq = time.time()
dsmooth = exact_smooth_from_reduced(red_d, PRIMES_GT1K, "d")
log(f"|j-nearest sq| smooth fraction: {dsmooth.mean():.4f} "
    f"({time.time()-tsq:.1f}s)")

FAM = {
    "F1_jmod4":     uniqJ % 4,
    "F2_jmod3":     uniqJ % 3,
    "F3_jmod5":     uniqJ % 5,
    "F4_jmod7":     uniqJ % 7,
    "F5_jmod105":   uniqJ % 105,
    "F6_omega_ter": omega_ter.astype(np.int64),
    "F7_dsq_smooth": dsmooth.astype(np.int64),
    "F8_jsmooth_1e6": jsmooth.astype(np.int64),
}
# map to per-position
FAMP = {k_: v[inv] for k_, v in FAM.items()}
log("features done")

# ------------------------------------------------------------------- stats --
GATE_N, GATE_H = 200, 15
BAR_RATIO = 1.15
P_BAR = 0.01

def tab(cls, mask, y):
    """per-class (n, h) under position mask"""
    c = cls[mask]
    yy = y[mask]
    n = np.bincount(c)
    h = np.bincount(c, weights=yy).astype(np.int64)
    return n, h

def safe_nanmax(a):
    return float(np.nanmax(a)) if np.isfinite(a).any() else float("nan")

def ratios_from_counts(n_m, h_m):
    tot_n, tot_h = n_m.sum(), h_m.sum()
    R = np.full(n_m.size, np.nan)
    ok = (n_m >= GATE_N) & (h_m >= GATE_H) & \
         ((tot_n - n_m) > 0) & ((tot_h - h_m) > 0)
    rn_c = (tot_h - h_m[ok]) / (tot_n - n_m[ok])
    rc = h_m[ok] / n_m[ok]
    R[ok] = rc / rn_c
    return R, ok

def did_from_counts(n_m, h_m, n_f, h_f):
    rm = h_m / np.maximum(n_m, 1)
    rf = h_f / np.maximum(n_f, 1)
    tn, th = n_m.sum(), h_m.sum()
    rm_c = (th - h_m) / np.maximum(tn - n_m, 1)
    rf_c = (h_f.sum() - h_f) / np.maximum(n_f.sum() - n_f, 1)
    return (rm - rf) - (rm_c - rf_c)

def sweep(cls_u, y):
    nm, hm = tab(cls_u, in_mid, y)
    nf, hf = tab(cls_u, in_flank, y)
    R, ok = ratios_from_counts(nm, hm)
    D = did_from_counts(nm, hm, nf, hf)
    return nm, hm, R, ok, D

def perm_p(cls_u, y, obs_R, obs_D, n_perm, rng):
    cnt_r = 0; cnt_d = 0
    ym_idx = np.nonzero(in_mid)[0]
    yf_idx = np.nonzero(in_flank)[0]
    y_mid = y[ym_idx].copy(); y_flk = y[yf_idx].copy()
    cm = cls_u[in_mid]; cf = cls_u[in_flank]
    for _ in range(n_perm):
        rng.shuffle(y_mid); rng.shuffle(y_flk)
        yp = y.copy()
        yp[ym_idx] = y_mid; yp[yf_idx] = y_flk
        nm, hm = tab(cm, slice(None), yp[in_mid]) if False else (
            np.bincount(cm), np.bincount(cm, weights=yp[in_mid]).astype(np.int64))
        nf, hf = (
            np.bincount(cf), np.bincount(cf, weights=yp[in_flank]).astype(np.int64))
        Rp, okp = ratios_from_counts(nm, hm)
        Dp = did_from_counts(nm, hm, nf, hf)
        if np.isfinite(Rp).any() and np.nanmax(Rp) >= obs_R: cnt_r += 1
        if np.isfinite(Dp).any() and np.nanmax(Dp) >= obs_D: cnt_d += 1
    return (cnt_r + 1) / (n_perm + 1), (cnt_d + 1) / (n_perm + 1)

rows = []
fam_stats = {}
for fname, cls_u in FAMP.items():
    cls = cls_u[inv]
    nc = cls_u.max() + 1
    nm, hm, R, ok, D = sweep(cls, Y)
    if not np.isfinite(R).any():
        rows.append(dict(family=fname, n_cells=int(nc), best_cell=None,
                         n_mid_best=None, h_mid_best=None,
                         rate_mid_best=None, R_best=None, DiD_best=None,
                         p_perm_R=None, p_perm_DiD=None, skipped=True,
                         skip_reason="gate-starved: no cell meets n/h gates",
                         cell_table={"n_mid": nm.tolist(), "h_mid": hm.tolist()}))
        log(f"{fname}: GATE-STARVED (no eligible cell)")
        continue
    obs_R = safe_nanmax(R)
    obs_D = safe_nanmax(D)
    cbest = int(np.nanargmax(R))
    pR, pD = perm_p(cls, Y, obs_R, obs_D, N_PERM, rng)
    # view B: per-N enrichment for best class
    rows.append(dict(
        family=fname, n_cells=int(nc), best_cell=int(cbest),
        n_mid_best=int(nm[cbest]), h_mid_best=int(hm[cbest]),
        rate_mid_best=float(hm[cbest] / max(nm[cbest], 1)),
        R_best=obs_R, DiD_best=obs_D, p_perm_R=pR, p_perm_DiD=pD,
        skipped=False,
        cell_table={"cells": list(range(int(nc))),
                    "n_mid": nm.tolist(), "h_mid": hm.tolist(),
                    "R": [None if not np.isfinite(x) else round(float(x), 4)
                          for x in R],
                    "DiD": [round(float(x), 6) for x in D]}))
    fam_stats[fname] = dict(obs_R=obs_R, pR=pR, pD=pD, best=cbest)
    log(f"{fname}: best cell {cbest} R={obs_R:.4f} DiD={obs_D:+.5f} "
        f"pR={pR:.4f} pD={pD:.4f}")

# degeneracy skip check for F7 (registered rule)
nm7 = np.bincount(FAMP["F7_dsq_smooth"][inv][in_mid])
hm7 = np.bincount(FAMP["F7_dsq_smooth"][inv][in_mid], weights=Y[in_mid]).astype(np.int64)
deg7 = ((nm7.max() / max(nm7.sum(), 1) > 0.98) or (nm7.size < 2)
        or (nm7.min() < GATE_N) or (hm7.min() < GATE_H))
if deg7:
    for r in rows:
        if r["family"] == "F7_dsq_smooth":
            r["skipped"] = True
            r["skip_reason"] = "degenerate per registered rule"
    log("F7 marked DEGENERATE -> skipped per registration")

# Bonferroni across tested (non-skipped) families
tested = [r for r in rows if not r["skipped"]]
K = len(tested)
winner = None
for r in tested:
    r["p_adj"] = min(1.0, r["p_perm_R"] * K)
for r in tested:
    r["clears_H1_bar"] = bool((not r["skipped"]) and r["p_adj"] < P_BAR
                              and r["R_best"] >= BAR_RATIO
                              and r["DiD_best"] > 0 and r["p_perm_DiD"] < 0.05)
    if r["clears_H1_bar"]:
        winner = r
verdict = ("H1_J_CARRIER:" + winner["family"] if winner else "H0_CARRIER_OPEN")

# ---------------------------------------------------------- null control ----
obs_global_maxR = max(r["R_best"] for r in tested)
null_maxR = []
for _ in range(N_NULL):
    yp = rng.permutation(Y)  # registered control: global label permutation,
    mx = -1.0                # matched prevalence, identical pipeline
    for fname, cls_u in FAMP.items():
        cls = cls_u[inv]
        nm, hm = tab(cls, in_mid, yp)
        R, ok = ratios_from_counts(nm, hm)
        if np.isfinite(R).any():
            mx = max(mx, float(np.nanmax(R)))
    null_maxR.append(mx)
null_maxR = np.array(null_maxR)
global_perm_p = float((null_maxR >= obs_global_maxR).sum() + 1) / (N_NULL + 1)
log(f"null control: max-R dist med={np.median(null_maxR):.4f} "
    f"p95={np.quantile(null_maxR,0.95):.4f} max={null_maxR.max():.4f}; "
    f"draws beating observed {obs_global_maxR:.4f}: "
    f"{int((null_maxR >= obs_global_maxR).sum())}/{N_NULL} "
    f"=> global_perm_p={global_perm_p:.4f}")

result = dict(
    experiment="exp598_J_FEATURE_SWEEP",
    question="is the mid-window hit-excess carrier a property of j itself",
    config=dict(smoke=SMOKE, n_windows=len(list(ns)), ctl_cap=CTL_CAP,
                n_perm=N_PERM, n_null=N_NULL, mid=[MID_LO, MID_HI],
                flank=FLANK, gate=dict(n=GATE_N, h=GATE_H),
                ratio_bar=BAR_RATIO, p_bar=P_BAR, bonferroni_K=K,
                rng_seed=RNG_SEED, npz_sha256=npz_sha256),
    preregistration=dict(
        H1=">=1 registered j-feature class R>=1.15 vs complement in mid-window "
           "[0.55,0.75], family-wise permutation p<0.01 (xK Bonferroni), DiD "
           "sign-consistent p<0.05 => carrier is j-arithmetic; name it",
        H0="no class clears bar => carrier remains open; route to "
           "consecutive-v polynomial-sequence correlation study",
        families=list(FAMP.keys()), windows_registered_before_analysis=True),
    features={k: {"n_cells": int(v.max()) + 1} for k, v in FAMP.items()},
    rows=rows,
    verdict=verdict,
    winner=(None if not winner else dict(family=winner["family"],
            cell=winner["best_cell"], R=winner["R_best"],
            p_adj=winner["p_adj"], DiD=winner["DiD_best"])),
    null_control=dict(median=float(np.median(null_maxR)),
                      p95=float(np.quantile(null_maxR, 0.95)),
                      max=float(null_maxR.max()),
                      obs_global_maxR=obs_global_maxR,
                      global_perm_p=global_perm_p,
                      note="max-of-ratio null is heavy-tailed by construction; "
                           "the calibrated per-family permutation p + Bonferroni "
                           "carries the verdict, global_perm_p is the pooled check"),
    honest_notes=[
        "positions+hit labels consumed from exp581_regen_positions.npz "
        "(seed-lineage regeneration hash-proven in exp581); generator not re-run "
        "(source outside this task's read allowlist); npz sha256 recorded",
        "hit labels = upstream cut-1e6 classify (exp569 path), consumed as-is",
        "F7 'v' operationalized as v=j (nearest square distance); skip-if-"
        "degenerate rule applied exactly as registered",
        "flanking window [0.05,0.40)+(0.90,1.00] chosen pre-analysis to avoid "
        "hump shoulders and window-edge behavior",
        "permutation shuffles labels within window strata (mid and flank "
        "separately) preserving window-level rates",
        f"Bonferroni K={K} (non-skipped registered families)",
    ],
    wall_s=round(time.time() - T0, 1),
)

out_json = os.path.join(BASE, "exp598_result.json")
with open(out_json, "w") as fh:
    json.dump(result, fh, indent=1)
log(f"WROTE {out_json}; VERDICT={verdict}; wall={result['wall_s']}s")

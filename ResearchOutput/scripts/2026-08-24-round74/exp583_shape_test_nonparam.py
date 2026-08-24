#!/usr/bin/env python3
# exp583 SHAPE-TEST-NONPARAM -- MINIMAL SKELETON (shipped under coordinator
# fuse; isotonic/I-spline monotone leg and Dickman-offset leg SKIPPED --
# noted in honest_notes). Question: does the hit-indicator vs normalized
# position x show interior structure (ns df=5) beyond LINEAR x, without any
# binning, in a stratum-conditional case-control logistic?
#
# PREREGISTRATION (locked before fitting):
#   x := (N - jlo_s)/(jhi_s - jlo_s); convention VERIFIED pre-script from ctl
#   arrays being linear-uniform inside each stratum window.
#   H1-shape: free natural-cubic-spline (df 5 incl constant; interior knots
#   .25/.5/.75) beats LINEAR-in-x with LRT p<0.001 BOTH asymptotic (chi2,
#   df = spline_df - 1 = 3) AND permutation (500 within-stratum label
#   shuffles, case counts preserved); interior max x* in [0.4,0.8];
#   peak-to-end rate-ratio bootstrap CI excluding 1; CONTROL arm null.
#   H0: any failure => mid-window "hump" not established binning-free.
#   Verdict: H1_CONFIRMED / MIXED_SHAPE_ONLY (LRTs pass, location/ratio fail)
#   / H0_CHANNEL_CLOSES.
import json, time, sys, os
import numpy as np
from scipy import linalg
from scipy.stats import chi2 as CHI2

BASE = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74"
NPZ = os.path.join(BASE, "exp581_regen_positions.npz")
SMOKE = "--smoke" in sys.argv
TAUS = np.array([0.25, 0.50, 0.75])
GRID = np.linspace(0, 1, 2001)
PERM_B = 40 if SMOKE else 400
BOOT_B = 60 if SMOKE else 150
CTL_CAP_OBS = 100 if SMOKE else None      # obs fits: None = all 4000/stratum
CTL_CAP_LOOP = 30 if SMOKE else 200       # perm/boot designs
SEED_P, SEED_B, SEED_S = 20260902, 20260903, 20260904
t0 = time.time()

def natural_basis(x):
    F = np.stack([x, x**2, x**3] + [np.clip(x - t, 0, None)**3 for t in TAUS], axis=1)
    C = np.zeros((2, 3 + len(TAUS)))
    C[0, 1] = 1.0; C[1, 2] = 1.0
    C[0, 3:] = 1.0 - TAUS; C[1, 3:] = 1.0
    return F @ linalg.null_space(C)          # n x 4 (+const dir in intercepts => df 5)

d = np.load(NPZ)
S = 32 if SMOKE else 128
jlo = d["jlo"].astype(float)[:S]; jhi = d["jhi"].astype(float)[:S]
x_h = np.concatenate([(d[f"hit_{s}"] - jlo[s]) / (jhi[s] - jlo[s]) for s in range(S)])
str_h = np.concatenate([np.full(len(d[f"hit_{s}"]), s) for s in range(S)])
ctl_raw = [(d[f"ctl_{s}"] - jlo[s]) / (jhi[s] - jlo[s]) for s in range(S)]
n_ctl_per = [len(c) for c in ctl_raw]

def make_design(xc_cap, seed, synth=False):
    """cases=hits; controls=capped ctl draws (or synthetic uniform vs ctl-as-cases)."""
    rng = np.random.default_rng(seed)
    xa, sa, ya = [], [], []
    for s in range(S):
        c = np.asarray(ctl_raw[s][:xc_cap] if xc_cap else ctl_raw[s], dtype=float)
        if synth:
            # CONTROL ARM: pseudo-cases = ctl draws; controls = fresh uniform
            hx, hs_ = rng.uniform(0, 1, len(c)), np.full(len(c), s)
            cx, cs = rng.uniform(0, 1, len(c)), np.full(len(c), s)
        else:
            ih = np.nonzero(str_h == s)[0]
            hx, hs_ = x_h[ih], str_h[ih]
            cx, cs = c, np.full(len(c), s)
        xa += [hx, cx]; sa += [hs_, cs]
        ya += [np.ones(len(hx)), np.zeros(len(cx))]
    x = np.concatenate(xa); st = np.concatenate(sa); y = np.concatenate(ya)
    Xf = natural_basis(x)
    Xl = x[:, None]
    return x, y, st.astype(int), Xf, Xl

def profile_ll(eta, y, st, S_):
    a = np.zeros(S_)
    for _ in range(40):
        mu = 1/(1+np.exp(-(eta + a[st])))
        g = np.bincount(st, weights=y-mu, minlength=S_)
        h = np.bincount(st, weights=mu*(1-mu), minlength=S_) + 1e-10
        stp = g/h; a += stp
        if np.max(np.abs(stp)) < 1e-9: break
    mu = 1/(1+np.exp(-(eta + a[st])))
    ll = np.sum(y*np.log(np.clip(mu,1e-300,1)) + (1-y)*np.log(np.clip(1-mu,1e-300,1)))
    return a, ll

def fit(X, y, st, S_, warm=None):
    b = np.zeros(X.shape[1]) if warm is None else warm.copy()
    a = np.zeros(S_); lp = -np.inf
    for _ in range(60):
        eta = X @ b + a[st]
        mu = 1/(1+np.exp(-eta)); r = y-mu; wq = mu*(1-mu)+1e-12
        b += np.linalg.solve(X.T@(X*wq[:,None]) + 1e-9*np.eye(X.shape[1]), X.T@r)
        a, ll = profile_ll(X@b, y, st, S_)
        if ll-lp < 1e-10 and _ > 2: break
        lp = ll
    _, ll = profile_ll(X@b, y, st, S_)
    return b, ll

def arm_test(x, y, st, S_, B_perm, seed_p):
    bf, lf = fit(np.hstack([np.zeros((len(y),0))]) if False else natural_basis(x), y, st, S_)
    # linear model: first column of natural basis spans linear direction? ensure exact:
    bl, ll_lin = fit(x[:, None]*(1.0), y, st, S_)
    stat_obs = 2*(lf - ll_lin); dfree = natural_basis(x[:2]).shape[1] - 1
    p_asym = float(CHI2.sf(stat_obs, dfree))
    counts = np.bincount(st, weights=y, minlength=S_).astype(int)
    order = np.argsort(st, kind="stable"); xs, sts = x[order], st[order]
    bnds = np.searchsorted(sts, np.arange(S_+1))
    inv = np.empty_like(order); inv[order] = np.arange(len(order))
    rng = np.random.default_rng(seed_p)
    ge = 0
    Xf_all = natural_basis(xs)
    warm = bf
    for _ in range(B_perm):
        lab = np.empty(len(y))
        for s in range(S_):
            sl = slice(bnds[s], bnds[s+1]); n = sl.stop-sl.start
            v = np.zeros(n); v[rng.permutation(n)[:counts[s]]] = 1.0
            lab[sl] = v
        y2 = lab[inv]
        _, lf2 = fit(Xf_all, y2, st, S_, warm=warm)
        _, ll2 = fit(xs[:,None], y2, st, S_)
        if 2*(lf2-ll2) >= stat_obs - 1e-9: ge += 1
    return dict(stat=float(stat_obs), df=int(dfree), p_asym=p_asym,
                p_perm=(1+ge)/(1+B_perm), ll_free=float(lf), ll_linear=float(ll_lin),
                beta_free=np.asarray(bf).tolist())

def curve_stats(x, y, st, S_):
    Xf = natural_basis(x)
    bf, _ = fit(Xf, y, st, S_)
    sg = natural_basis(GRID) @ bf
    msk = (GRID >= 0.02) & (GRID <= 0.98)
    ixs = int(np.argmax(np.where(msk, sg, -np.inf)))
    ie = int(np.argmin(np.abs(GRID-0.98)))
    return float(GRID[ixs]), float(np.exp(sg[ixs]-sg[ie])), bf

# ---- HIT ARM -----------------------------------------------------------------
print("design: obs rows building...", flush=True)
xv, yv, sv, _, _ = make_design(CTL_CAP_OBS, SEED_S)
print("obs rows:", len(yv), flush=True)
t_a=time.time()
# observed LRT on FULL design:
bf_h_, lf_h = fit(natural_basis(xv), yv, sv, S)
_, ll_hlin = fit(xv[:, None], yv, sv, S)
hit_stat_big = float(2*(lf_h - ll_hlin))
hit_p_asym_big = float(CHI2.sf(hit_stat_big, 3))
print("obs fits done %.1fs stat=%.2f p=%.3g" % ((time.time()-t_a), hit_stat_big, hit_p_asym_big), flush=True)
# permutation calibration on CAPPED loop design:
xq, yq, sq, _, _ = make_design(CTL_CAP_LOOP, SEED_S)
hit_res = arm_test(xq, yq, sq, S, PERM_B, SEED_P)
hit_res["stat"] = hit_stat_big; hit_res["df"] = 3
hit_res["p_asym"] = hit_p_asym_big   # asym from full design; perm from capped
print("hit arm LRT+perm done %.1fs"%((time.time()-t_a)), flush=True)
x_star_h, ratio_h, bf_h = curve_stats(xv, yv, sv, S)

# bootstrap CIs (cluster over strata), capped design
t_b=time.time()
rngb = np.random.default_rng(SEED_B)
per_str = []
for s in range(S):
    ih = np.nonzero(str_h == s)[0]
    c = np.asarray(ctl_raw[s], dtype=float)
    if CTL_CAP_LOOP and len(c) > CTL_CAP_LOOP:
        c = c[rngb.choice(len(c), CTL_CAP_LOOP, replace=False)]
    per_str.append((x_h[ih], str_h[ih], c, np.full(len(c), s)))
stars, rats = [], []
for _ in range(BOOT_B):
    pick = rngb.integers(0, S, S)
    xa_, sa_, ya_ = [], [], []
    for s in pick:
        hx, hs, cx, cs = per_str[s]
        xa_ += [hx, cx]; sa_ += [hs, cs]; ya_ += [np.ones(len(hx)), np.zeros(len(cx))]
    try:
        st_r = curve_stats(np.concatenate(xa_), np.concatenate(ya_), np.concatenate(sa_).astype(int), S)
        stars.append(st_r[0]); rats.append(st_r[1])
    except Exception:
        pass
print("boot done %.1fs reps=%d"%(time.time()-t_b,len(rats)), flush=True)
ci_x = [float(np.percentile(stars, 2.5)), float(np.percentile(stars, 97.5))]
ci_r = [float(np.percentile(rats, 2.5)), float(np.percentile(rats, 97.5))]

# ---- CONTROL ARM ---------------------------------------------------------------
xc_v, yc_v, sc_v, _, _ = make_design(CTL_CAP_OBS, SEED_S, synth=True)
print("control arm rows:", len(yc_v), flush=True)
t_c=time.time()
# observed LRT on the (large) synth design:
bf_c, lf_c = fit(natural_basis(xc_v), yc_v, sc_v, S)
_, ll_clin = fit(xc_v[:, None], yc_v, sc_v, S)
ctl_stat_big = float(2*(lf_c - ll_clin))
ctl_p_asym_big = float(CHI2.sf(ctl_stat_big, 3))
# permutation calibration on the CAPPED loop design (same cap as hit arm):
xp, yp, sp, _, _ = make_design(CTL_CAP_LOOP, SEED_S, synth=True)
ctl_res = arm_test(xp, yp, sp, S, max(PERM_B//2, 20), SEED_P+1)
ctl_res["stat"] = ctl_stat_big; ctl_res["df"] = 3
ctl_res["p_asym"] = ctl_p_asym_big   # asym from large design; perm from capped design
x_star_c, ratio_c, _ = curve_stats(xp, yp, sp, S)
print("control arm done %.1fs" % (time.time()-t_c), flush=True)
x_star_c, ratio_c, _ = curve_stats(xc_v, yc_v, sc_v, S)

cond = {
 "T_LRT_free_vs_linear_asym<0.001": hit_res["p_asym"] < 1e-3,
 "T_LRT_free_vs_linear_perm<0.001": hit_res["p_perm"] < 1e-3,
 "interior_max_in_[0.4,0.8]": 0.4 <= x_star_h <= 0.8,
 "peak_to_end_CI_excl_1": ci_r[0] > 1 or ci_r[1] < 1,
 "control_null": (ctl_res["p_perm"] > 0.01 and ctl_res["p_asym"] > 0.01
                  and ratio_c >= 0.9 and ratio_c <= 1.1),
}
if all(cond.values()): verdict = "H1_CONFIRMED"
elif cond["T_LRT_free_vs_linear_asym<0.001"] and cond["T_LRT_free_vs_linear_perm<0.001"]:
    verdict = "MIXED_SHAPE_ONLY"
else: verdict = "H0_CHANNEL_CLOSES"

out = {"exp": 583, "codename": "SHAPE-TEST-NONPARAM", "mode": "smoke" if SMOKE else "full",
 "source_npz": NPZ,
 "config": {"S": S, "taus": TAUS.tolist(), "perm_B": PERM_B, "boot_B": BOOT_B,
            "ctl_cap_loop": CTL_CAP_LOOP, "ctl_cap_obs": CTL_CAP_OBS,
            "prereg": "header of exp583_shape_test_nonparam.py; minimal skeleton per coordinator",
            "skipped_legs": ["monotone I-spline/isotonic comparison", "Dickman-offset baseline"]},
 "stats": {
   "n_hits": int(len(x_h)), "n_ctl_full": int(sum(n_ctl_per)),
   "hit_arm": {"lrt": hit_res, "x_star": x_star_h, "x_star_boot_ci": ci_x,
               "peak_to_end_ratio": ratio_h, "ratio_boot_ci": ci_r,
               "boot_reps_used": len(rats)},
   "control_arm": {"lrt": ctl_res, "x_star": float(x_star_c), "peak_to_end_ratio": float(ratio_c)}},
 "verdicts": {"verdict": verdict, "conditions": cond,
   "one_line": (f"{verdict}: free-vs-linear LRT stat={hit_res['stat']:.1f} df={hit_res['df']} "
                f"asym p={hit_res['p_asym']:.3g} perm p={hit_res['p_perm']:.4f}; "
                f"x*={x_star_h:.3f} CI[{ci_x[0]:.3f},{ci_x[1]:.3f}]; peak/end={ratio_h:.3f} "
                f"CI[{ci_r[0]:.3f},{ci_r[1]:.3f}]; control asym p={ctl_res['p_asym']:.3g} "
                f"perm p={ctl_res['p_perm']:.4f}")},
 "honest_notes": [
  "MINIMAL SKELETON shipped under coordinator fuse (~15 min): monotone-I-spline and Dickman-offset legs SKIPPED, not failed -- H1's 'beats monotone' clause UNTESTED here; verdict names shape-vs-LINEAR only",
  "no binning anywhere: raw case-control logistic, stratum-conditional intercepts (128)",
  "x=(N-jlo)/(jhi-jlo) convention VERIFIED from ctl arrays linear-uniform (pre-script check)",
  f"perm/boot on control-capped design ({CTL_CAP_LOOP}/stratum); observed stats on {'full' if CTL_CAP_OBS is None else CTL_CAP_OBS}-cap design",
  "seeds P/B/S = 20260902/20260903/20260904"],
 "wall_s": round(time.time()-t0, 1)}

fn = os.path.join(BASE, "exp583_smoke_result.json" if SMOKE else "exp583_result.json")
with open(fn, "w") as f: json.dump(out, f, indent=1, default=float)
print(json.dumps(out["verdicts"], indent=1))
print("WALL", out["wall_s"], "->", fn)

#!/usr/bin/env python3
"""exp579 PROFILE-FORM (round-74; paper-228/exp578 follow-up (a))

exp578 (BEYOND-MAGNITUDE amendment) found the pooled within-N hit-position
profile declines monotonically (deciles [.162,.123,.109,.097,.091,.091,.090,
.084,.081,.072]) and SURVIVES (bitlen(v) x mantissa-octant) conditioning.
This experiment characterizes the FUNCTIONAL FORM of that profile and of the
beyond-magnitude residual.

PRE-REGISTRATION (decision rules stated BEFORE fitting on full data; only the
exp578 recorded summary above was known entering this experiment):

  Data: exp578_positions.npz verbatim (hit_j + paired non-hit ctl_j arrays per
  N, jlo/jhi). Normalized position u=(j-jlo)/(jhi-jlo) in [0,1]. Profile =
  POOLED hit-fraction per 50 equal-width u-bins (rate-weighted pooling over
  all 128 Ns, exp578 convention; every N has >=29 hits so the HITRICH>=30
  restriction of exp578 would exclude exactly one N -- disclosed, immaterial).
  Control arm: paired first-len(hits) non-hits per N (exp578 convention).
  Uncertainty: CLUSTER BOOTSTRAP over Ns (2000 reps, seed 20260831),
  percentile CIs per bin; the same replicates feed parameter CIs and R CIs.

  V1 WINNER RULE: fit by WLS (weights = 1/bootSE(bin)^2, absolute_sigma) the
  four candidates  linear a+b.x | exponential a.e^{-b.x} | power a.(1+x)^{-b}
  | logistic L/(1+e^{k(x-x0)})  on the 50 TREATMENT bin fractions; winner =
  lowest AICc; Akaike weights reported; if winner-runnerup dAICc < 2 the
  family call is AMBIGUOUS (prefer fewer params in wording).

  V2 RESIDUAL RULE (stated before computing): magnitude baseline M(b) =
  mixture-Dickman prediction (below); residual R(b) = T(b)/M(b).
  PEAKED iff quadratic-beats-linear on R by dAICc > 2 AND vertex in (0,1)
    AND quadratic-coefficient 95% CI excludes 0;
  else MONOTONE-DECLINING iff (Spearman(R, x) negative with p < 0.01) OR
    linear slope 95% CI wholly < 0;
  else FLAT.
  Baseline fragility gate: V2 verdict must be INVARIANT across the three
  r-scenario brackets (see below); otherwise BASELINE-FRAGILE is appended.
  CONTROL GATE: control profile must be flat (linear slope CI covering 0);
  firing slope => ARTIFACT-CONTAMINATION flag.

  MAGNITUDE BASELINE (honest reconstructability statement): the tester's
  smoothness event is "v=j^2-N is 1e6-smooth"; the standard baseline for the
  per-j hit density is Dickman rho(u), u=ln(v)/ln(1e6) (rho=1 for u<=1).
  N itself is NOT stored, but s=isqrt(N)=jhi//3 exactly, so N in [s^2,(s+1)^2)
  -- the unknown offset r=N-s^2 in [0,2s] enters ONLY through the window-start
  value v0=2s+1-r (u0 in [0,~2.5]); at v~N the induced du error is O(1e-27).
  PRIMARY baseline: average the per-N predicted bin masses q_{N,b}(r) over a
  UNIFORM-r prior (17-point grid); BRACKETS: r=0, r=s, r=2s for all Ns.
  M(b) = sum_N h_N * qbar_{N,b} / sum_N h_N with h_N = OBSERVED hit count of N
  (rate-weighted, absorbing N-level rate variation -- apples-to-apples with
  the pooled T). Bootstrap recomputes M per replicate from the stored q matrix
  (joint T,M -> R uncertainty).

  SMOKE = first 10 Ns, plumbing/calibration only.
"""
import sys, os, json, time
import numpy as np
from multiprocessing import Pool
from scipy.optimize import curve_fit
from scipy.stats import spearmanr

BASE = os.path.dirname(os.path.abspath(__file__))
NPZ_IN = os.path.join(BASE, "exp578_positions.npz")
NB = 50                      # profile bins
BOOT_REPS = 2000
BOOT_SEED = 20260831         # fresh master seed (lab rule)
N_RGRID = 17                 # uniform-r mixture grid
M_GRID = 20000               # j-grid points per N (400/bin)
LN_B = np.log(1e6)


# ---------------- Dickman rho ----------------
def build_dickman(umax=6.0, du=2e-4):
    n = int(np.ceil(umax / du))
    uu = np.arange(n + 1) * du
    rho = np.ones(n + 1)
    k1 = int(round(1.0 / du))
    for m in range(1, int(np.ceil(umax))):
        i0 = m * k1
        if i0 >= n:
            break
        i1 = min((m + 1) * k1, n)
        tt = uu[i0:i1 + 1]
        integ = np.interp(tt - 1.0, uu, rho) / tt
        dt = np.diff(tt)
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (integ[:-1] + integ[1:]) * dt)])
        rho[i0 + 1:i1 + 1] = rho[i0] - cum[1:]
    return uu, rho


DICKMAN_CHECKS = {"rho(2)": 1 - np.log(2), "rho(3)": 0.04860838829113123,
                  "rho(4)": 0.00491092578243589, "rho(5)": 0.00035472470045130}


# ---------------- candidate forms ----------------
def _lin(x, a, b): return a + b * x
def _exp(x, a, b): return a * np.exp(-b * x)
def _pow(x, a, b): return a * (1.0 + x) ** (-b)
def _logi(x, L, x0, k): return L / (1.0 + np.exp(np.clip(k * (x - x0), -500, 500)))

MODELS = {
    "linear":      (_lin,  [0.12, -0.06],          ["a", "b"]),
    "exponential": (_exp,  [0.16, 0.9],            ["a", "b"]),
    "power":       (_pow,  [0.20, 1.0],            ["a", "b"]),
    "logistic":    (_logi, [0.18, 0.55, 5.0],      ["L", "x0", "k"]),
}


def safe_curve_fit(fn, x, y, p0, sigma):
    try:
        popt, pcov = curve_fit(fn, x, y, p0=p0, sigma=sigma,
                               absolute_sigma=True, maxfev=40000)
        if not np.all(np.isfinite(popt)) or not np.all(np.isfinite(pcov)):
            return None, None
        return popt, pcov
    except Exception:
        return None, None


def wls_ic(fn, popt, x, y, sigma):
    r = (y - fn(x, *popt)) / sigma
    rssw = float(np.sum(r * r))
    n, k = len(x), len(popt)
    aic = n * np.log(max(rssw, 1e-300) / n) + 2 * k
    aicc = aic + 2 * k * (k + 1) / max(n - k - 1, 1)
    bic = n * np.log(max(rssw, 1e-300) / n) + k * np.log(n)
    return rssw, aic, aicc, bic


_FITX = None      # module-level bin centers for fork workers
_G = {}


def _init_fit(Tb_, se_, x_):
    global _FITX
    _G["Tb"] = Tb_; _G["se"] = np.maximum(se_, 1e-9); _FITX = x_


def _fit_rep(r_):
    out = {}
    for name, (fn, p0, _pn) in MODELS.items():
        po, _pc = safe_curve_fit(fn, _FITX, _G["Tb"][r_], p0, _G["se"])
        out[name] = None if po is None else np.asarray(po)
    return out


def main():
    t0 = time.time()
    mode = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    smoke = mode == "smoke"

    z = np.load(NPZ_IN)
    jlo = z["jlo"].astype(np.int64); jhi = z["jhi"].astype(np.int64)
    nN_full = len(jlo)
    nN = 10 if smoke else nN_full
    jlo, jhi = jlo[:nN], jhi[:nN]
    span = (jhi - jlo).astype(np.float64)

    # ---- per-N normalized positions -> count matrices ----
    H = np.zeros((nN, NB), dtype=np.float64)
    C = np.zeros((nN, NB), dtype=np.float64)
    hits_per_N = np.zeros(nN, dtype=np.int64)
    for i in range(nN):
        hj = z[f"hit_{i}"]; cj = z[f"ctl_{i}"][:len(hj)]
        hits_per_N[i] = len(hj)
        ut = (hj - jlo[i]) / span[i]
        uc = (cj - jlo[i]) / span[i]
        H[i] = np.bincount(np.clip((ut * NB).astype(int), 0, NB - 1), minlength=NB)
        C[i] = np.bincount(np.clip((uc * NB).astype(int), 0, NB - 1), minlength=NB)
    tot_h = hits_per_N.sum()
    centers = (np.arange(NB) + 0.5) / NB

    # ---- Dickman baseline (mixture over unknown offset r = N - s^2) ----
    uu, rr = build_dickman()
    dick_ok = {k: {"table": round(float(np.interp(float(k[4:-1]), uu, rr)), 6),
                   "reference": round(float(kv), 6)}
               for k, kv in DICKMAN_CHECKS.items()}
    s_arr = (jhi // 3).astype(object)           # s = isqrt(N) EXACTLY
    Q_mix = np.zeros((nN, NB)); Q_r = {0: np.zeros((nN, NB)),
                                       1: np.zeros((nN, NB)), 2: np.zeros((nN, NB))}
    rgrid_fracs = np.linspace(0.0, 1.0, N_RGRID)
    edges_idx = [round(b * M_GRID / NB) for b in range(NB + 1)]
    for i in range(nN):
        s = int(s_arr[i])
        jj = np.linspace(float(jlo[i]), float(jhi[i]), M_GRID + 1)
        jj2 = jj * jj
        q_acc = np.zeros(NB)
        for fr in rgrid_fracs:
            r = int(round(fr * 2 * s))
            v = np.maximum(jj2 - float(s * s + r), 2.0)
            w = np.interp(np.log(v) / LN_B, uu, rr)
            cw = np.concatenate([[0.0], np.cumsum(0.5 * (w[:-1] + w[1:]) * np.diff(jj))])
            seg = np.diff(cw[edges_idx])
            q_acc += seg / seg.sum()
        Q_mix[i] = q_acc / N_RGRID
        # explicit scenario vectors (single evaluations)
        for scen, fr in ((0, 0.0), (1, 0.5), (2, 1.0)):
            r = int(round(fr * 2 * s))
            v = np.maximum(jj2 - float(s * s + r), 2.0)
            w = np.interp(np.log(v) / LN_B, uu, rr)
            cw = np.concatenate([[0.0], np.cumsum(0.5 * (w[:-1] + w[1:]) * np.diff(jj))])
            seg = np.diff(cw[edges_idx]); Q_r[scen][i] = seg / seg.sum()

    w_h = hits_per_N / tot_h
    T = (H.sum(0)) / tot_h
    M = (w_h[:, None] * Q_mix).sum(0)
    Ms = {k: (w_h[:, None] * Q).sum(0) for k, Q in Q_r.items()}
    Ct = (C.sum(0)) / C.sum()

    # ---- cluster bootstrap ----
    rng = np.random.default_rng(BOOT_SEED)
    idx = rng.integers(0, nN, size=(BOOT_REPS, nN))
    Hb = H[idx]                       # (R, nN, NB)
    Cb = C[idx]
    Tb = Hb.sum(1) / Hb.sum(axis=(1, 2))[:, None]
    Ctb = Cb.sum(1) / Cb.sum(axis=(1, 2))[:, None]
    assert Tb.shape == (BOOT_REPS, NB), f"BOOT BROADCAST BUG {Tb.shape}"
    Hs = Hb.sum(2)                    # (R, nN) hit counts per replicate
    Mb = (Hs @ Q_mix) / Hs.sum(1, keepdims=True)
    Rb = Tb / np.maximum(Mb, 1e-300)
    T_se = Tb.std(0, ddof=1); Ct_se = Ctb.std(0, ddof=1); R_se = Rb.std(0, ddof=1)
    pct = lambda A: (np.percentile(A, 2.5, axis=0), np.percentile(A, 97.5, axis=0))
    T_lo, T_hi = pct(Tb); C_lo, C_hi = pct(Ctb); R_lo, R_hi = pct(Rb)

    # ---- V1: candidate fits on treatment profile ----
    x = centers
    # bootstrap parameter distributions (parallel over replicates)
    nproc = 2 if smoke else 8
    boot_param_store = {}
    if nproc > 1 and BOOT_REPS > 1:
        with Pool(nproc, initializer=_init_fit,
                  initargs=(Tb, T_se, x)) as pl:
            rep_fits = pl.map(_fit_rep, range(BOOT_REPS), chunksize=16)
        for name in MODELS:
            arrs = [rf[name] for rf in rep_fits if rf.get(name) is not None]
            boot_param_store[name] = np.array(arrs) if arrs else np.zeros((0, len(MODELS[name][2])))
    else:
        for name in MODELS:
            boot_param_store[name] = np.zeros((0, len(MODELS[name][2])))
    fits = {}
    for name, (fn, p0, pn) in MODELS.items():
        popt, pcov = safe_curve_fit(fn, x, T, p0, T_se)
        entry = {"model": name, "params": {}, "param_names": pn}
        if popt is None:
            entry["fit_failed"] = True
            fits[name] = entry
            continue
        rssw, aic, aicc, bic = wls_ic(fn, popt, x, T, T_se)
        entry["params"] = {n_: float(v) for n_, v in zip(pn, popt)}
        se = np.sqrt(np.abs(np.diag(pcov)))
        entry["param_ci95_cov"] = {n_: [float(v - 1.96 * e), float(v + 1.96 * e)]
                                   for n_, v, e in zip(pn, popt, se)}
        entry["rss_w"], entry["AIC"], entry["AICc"], entry["BIC"] = (
            round(rssw, 4), round(aic, 3), round(aicc, 3), round(bic, 3))
        # bootstrap parameter dist (parallel over replicates)
        pb = boot_param_store.get(name)
        if pb is None or not len(pb):
            entry["boot_fits_ok"] = 0
            fits[name] = entry
            continue
        entry["boot_fits_ok"] = int(len(pb))
        if len(pb) >= 50:
            entry["param_ci95_boot"] = {n_: [float(lo), float(hi)] for n_, lo, hi in
                                        zip(pn, np.percentile(pb, 2.5, axis=0),
                                            np.percentile(pb, 97.5, axis=0))}
        fits[name] = entry
    ok_fits = {k: v for k, v in fits.items() if "AICc" in v}
    aiccs = {k: v["AICc"] for k, v in ok_fits.items()}
    best = min(aiccs, key=aiccs.get)
    deltas = {k: round(v - aiccs[best], 3) for k, v in aiccs.items()}
    wts_raw = {k: np.exp(-d / 2) for k, d in deltas.items()}
    sw = sum(wts_raw.values())
    akaike_w = {k: round(v / sw, 4) for k, v in wts_raw.items()}
    margin = round(sorted(deltas.values())[1] - sorted(deltas.values())[0], 3)
    family_call = best if margin >= 2.0 else f"AMBIGUOUS({best}~runner-up,dAICc={margin})"

    # ---- V2: residual shape ----
    R = T / np.maximum(M, 1e-300)
    sp_rho, sp_p = spearmanr(x, R)
    pl_, pc_ = safe_curve_fit(_lin, x, R, [R.mean(), 0.0], np.maximum(R_se, 1e-9))
    slope_ci = ([float(pl_[1] - 1.96 * np.sqrt(abs(pc_[1, 1]))),
                 float(pl_[1] + 1.96 * np.sqrt(abs(pc_[1, 1])))] if pl_ is not None else None)

    def quad(xq, a, b, c): return a + b * xq + c * xq * xq
    pq, qcq = safe_curve_fit(quad, x, R, [R.mean(), 0.0, 0.0], np.maximum(R_se, 1e-9))
    if pq is not None:
        rq = (R - quad(x, *pq)) / np.maximum(R_se, 1e-9)
        n_, k_ = NB, 3
        aicc_q = n_ * np.log(max(float((rq * rq).sum()), 1e-300) / n_) + 2 * k_ \
            + 2 * k_ * (k_ + 1) / (n_ - k_ - 1)
        c_ci = [float(pq[2] - 1.96 * np.sqrt(abs(qcq[2, 2]))),
                float(pq[2] + 1.96 * np.sqrt(abs(qcq[2, 2])))]
        vertex = float(-pq[1] / (2 * pq[2])) if abs(pq[2]) > 1e-12 else float("nan")
        lin_aicc = aiccs.get("linear", None)
        quad_beats = (lin_aicc is not None and aicc_q < lin_aicc - 2.0)
    else:
        aicc_q, c_ci, vertex, quad_beats = None, None, None, False
    pe_sig = bool(pq is not None and (c_ci[0] > 0 or c_ci[1] < 0) and 0.0 < vertex < 1.0)
    sp_neg = bool(sp_rho < 0 and sp_p < 0.01)
    sl_neg = bool(slope_ci is not None and slope_ci[1] < 0)
    if quad_beats and pe_sig:
        resid_shape = "PEAKED"
    elif sp_neg or sl_neg:
        resid_shape = "MONOTONE-DECLINING"
    else:
        resid_shape = "FLAT"
    # bracket invariance
    bracket_R = {k: T / np.maximum(Ms[k], 1e-300) for k in Ms}
    bracket_shapes = {}
    shapes_set = set()
    for k_, Rk in bracket_R.items():
        spk = spearmanr(x, Rk)
        pk_, pck = safe_curve_fit(_lin, x, Rk, [Rk.mean(), 0], np.maximum(R_se, 1e-9))
        slk_lo = pk_[1] - 1.96 * np.sqrt(abs(pck[1, 1])) if pk_ is not None else np.nan
        decl_k = bool(spk.statistic < 0 or (pk_ is not None and slk_lo < 0))
        shapes_set.add("MONOTONE-DECLINING" if decl_k else "OTHER")
        bracket_shapes[f"r_scenario_{['0', 'mid', '2s'][k_]}"] = {
            "R_first_last": [round(float(Rk[0]), 3), round(float(Rk[-1]), 3)],
            "spearman": round(float(spk.statistic), 4),
            "p": float(spk.pvalue),
            "slope": round(float(pk_[1]), 4) if pk_ is not None else None}
    baseline_fragile = bool(resid_shape == "MONOTONE-DECLINING"
                            and shapes_set != {"MONOTONE-DECLINING"})
    # exponential on residual (law of the beyond-magnitude part)
    pe_, pec_ = safe_curve_fit(_exp, x, R, [R[0], 0.5], np.maximum(R_se, 1e-9))

    # ---- control gate ----
    pcn, pccn = safe_curve_fit(_lin, x, Ct, [0.02, 0.0], np.maximum(Ct_se, 1e-12))
    ctl_slope = float(pcn[1]) if pcn is not None else None
    ctl_slope_ci = ([float(pcn[1] - 1.96 * np.sqrt(abs(pccn[1, 1]))),
                     float(pcn[1] + 1.96 * np.sqrt(abs(pccn[1, 1])))] if pcn is not None else None)
    ctl_flat = bool(ctl_slope_ci is not None and ctl_slope_ci[0] <= 0 <= ctl_slope_ci[1])

    # ---- one-line law ----
    def fam_law(fname):
        f_ = fits.get(fname, {})
        if "params" not in f_:
            return "n/a"
        p_ = f_["params"]
        if fname == "linear":
            return f"T(x) ~ {p_['a']:.4f}{p_['b']:+.4f}*x"
        if fname == "exponential":
            return f"T(x) ~ {p_['a']:.4f}*exp(-{p_['b']:.3f}*x)"
        if fname == "power":
            return f"T(x) ~ {p_['a']:.4f}*(1+x)^-{p_['b']:.3f}"
        if fname == "logistic":
            return (f"T(x) ~ {p_['L']:.4f}/(1+exp({p_['k']:.2f}(x-{p_['x0']:.2f})))")
        return "n/a"

    core_family = family_call.split("~")[0].strip("()AMBIGIOUS") if "AMBIGUOUS" in family_call else family_call
    rl, rh = float(R[0]), float(R[-1])
    law = (f"{family_call}: {fam_law(core_family)}; beyond-Dickman residual "
           f"R=T/M runs {rl:.2f} -> {rh:.2f} from x=0 to 1, shape {resid_shape}")

    profile_table = []
    for b in range(NB):
        profile_table.append({
            "bin": b, "center": round(float(x[b]), 4),
            "T": round(float(T[b]), 6), "T_ci95": [round(float(T_lo[b]), 6), round(float(T_hi[b]), 6)],
            "Ctl": round(float(Ct[b]), 6), "Ctl_ci95": [round(float(C_lo[b]), 6), round(float(C_hi[b]), 6)],
            "M_pred": round(float(M[b]), 6), "R": round(float(R[b]), 4),
            "R_ci95": [round(float(R_lo[b]), 4), round(float(R_hi[b]), 4)]})

    out = {
        "exp": "579", "codename": "PROFILE-FORM", "mode": mode,
        "config": {
            "source_npz": NPZ_IN, "n_Ns": nN, "bins": NB, "boot_reps": BOOT_REPS,
            "boot_seed": BOOT_SEED, "bootstrap_unit": "cluster over Ns",
            "pooling": "rate-weighted (all hits pooled; every N has >=29 hits)",
            "control": "paired first-len(hits) non-hits per N (exp578 convention)",
            "models": list(MODELS.keys()),
            "baseline": "Dickman rho(u), u=ln(j^2-N)/ln(1e6), mixture over uniform r=N-s^2 prior (17-pt); brackets r in {0,mid,2s}; s=isqrt(N)=jhi//3 exact",
            "dickman_checks": dick_ok,
        },
        "profile_table": profile_table,
        "fits": fits, "delta_AICc": deltas, "akaike_weights": akaike_w,
        "residual": {
            "definition": "R(b)=T(b)/M(b), M=mixture-Dickman rate-weighted",
            "R_first": round(rl, 4), "R_last": round(rh, 4),
            "spearman_rho_vs_x": round(float(sp_rho), 4), "spearman_p": float(sp_p),
            "linear_slope": round(float(pl_[1]), 4) if pl_ is not None else None,
            "linear_slope_ci95": [round(v, 4) for v in slope_ci] if slope_ci else None,
            "quadratic_AICc": round(aicc_q, 3) if aicc_q is not None else None,
            "linear_AICc": aiccs.get("linear"),
            "quad_c_ci95": [round(v, 6) for v in c_ci] if c_ci else None,
            "vertex_x": round(vertex, 4) if vertex == vertex else None,
            "exponential_on_R": ({"a": round(float(pe_[0]), 4),
                                  "b": round(float(pe_[1]), 4)} if pe_ is not None else None),
            "bracket_scenarios": bracket_shapes,
            "shape_verdict": resid_shape,
        },
        "control_gate": {"slope": round(ctl_slope, 6) if ctl_slope is not None else None,
                         "slope_ci95": [round(v, 6) for v in ctl_slope_ci] if ctl_slope_ci else None,
                         "flat_pass": ctl_flat},
        "verdicts": {
            "winning_family": family_call,
            "winner_dAICc_to_runner_up": margin,
            "akaike_weights": akaike_w,
            "residual_shape": resid_shape,
            "baseline_fragile_flag": bool(baseline_fragile),
            "control_flat": ctl_flat,
            "one_line_law": law,
        },
        "honest_notes": [
            "N is not stored in exp578_positions.npz; s=isqrt(N)=jhi//3 is exact so N "
            "is known modulo the offset r=N-s^2 in [0,2s]; primary baseline mixes over "
            "a UNIFORM-r prior and r in {0,mid,2s} brackets are reported; the true "
            "next_prime-induced r-distribution is not exactly uniform (disclosed)",
            "the Dickman baseline treats v=j^2-N as random integers w.r.t. 1e6-smoothness; "
            "algebraic structure of j^2-N can shift the smoothness CONSTANT (not necessarily "
            "the j-shape), so R!=1 alone is not proof of geometry -- the deliverable is the "
            "SHAPE of R (monotone vs peaked vs flat), which is invariant to constant offsets",
            "rate-weighted pooling matches exp578; every N has >=29 hits so the exp578 "
            "HITRICH>=30 primary set would differ by exactly one N (immaterial, disclosed)",
            "parameter CIs: covariance (absolute_sigma, bootSE weights) + cluster-bootstrap "
            "percentile; the bootstrap is the clustered inference",
            "WLS ICs use Gaussian likelihood on 50 bins (n=50); AICc reported, dAICc<2 => "
            "family call declared AMBIGUOUS by pre-stated rule",
            "R explodes toward the tail if Dickman predicts far steeper decay than observed; "
            "ratio-scale residuals at the last bins carry that asymmetry honestly",
            "discretization: 400-point trapezoid per bin in j-space; the u=1 wall sits at "
            "normalized position ~1e-15 (inside bin 0) for every N regardless of r",
            "smoke mode = first 10 Ns, plumbing/calibration only; full-run verdicts require "
            "the full 128-N run",
        ],
        "wall_s": round(time.time() - t0, 1),
    }
    fn = os.path.join(BASE, "exp579_smoke_result.json" if smoke else "exp579_result.json")
    with open(fn, "w") as f:
        json.dump(out, f, indent=1)
    summ = {"mode": mode, "nNs": nN, "total_hits": int(tot_h),
            "deltas": deltas, "akaike_w": akaike_w, "family": family_call,
            "residual": {"first": round(rl, 3), "last": round(rh, 3),
                         "spearman": round(float(sp_rho), 4), "p": float(sp_p),
                         "shape": resid_shape, "fragile": bool(baseline_fragile)},
            "control_flat": ctl_flat, "wall_s": out["wall_s"]}
    print(json.dumps(summ, indent=1))
    print(f"[{mode}] -> {fn}", flush=True)


if __name__ == "__main__":
    main()

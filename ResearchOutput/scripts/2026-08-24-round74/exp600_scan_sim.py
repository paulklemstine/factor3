#!/usr/bin/env python3
# =============================================================================
# exp600 SCAN-SIM-JOINT (round-74) -- paper 250's named decidable closer.
#
# PRE-REGISTERED PREDICTION (written BEFORE analysis; two-sided):
#   Joint measurement of S, Lambda, Theta, qhat from exp581_regen_positions.npz
#   yields observed ascending-vs-descending cost ratio S_obs in [1.10, 1.51]
#   with S_obs < certified bound 1.51 => CONFIRMS the paper-250 calibrated-gap
#   structure (slack real, quantified; predicted gap X = bound/S ~ 1.15).
#   S_obs outside [1.10, 1.51] on EITHER side => prediction FAILS; report which
#   side and magnitude.
#
# Method (per task):
#   1. Load exp581_regen_positions.npz: hit positions (true divisors) + control
#      positions per N, window bounds jlo/jhi (128 balanced bitlen-96 semiprimes).
#   2. Simulate BOTH scan orders over each N's sampled position grid using stored
#      hit indicators. For scan order pi,
#         cost(N,pi) = E[tests until first hit] = sum_k k*P(first hit at k-th test)
#      computed EXACTLY from the indicator series under pi (deterministic series
#      => degenerate distribution, exact integer costs):
#         ascending : tests j = jlo, jlo+1, ...  -> C_asc = min(h) - jlo + 1
#         descending: tests j = jhi-1, jhi-2, ...-> C_desc = jhi - max(h)
#      Flat-prior booking C0(N) = E[first-hit rank under uniform-random order] =
#      (W+1)/(m+1) with W window width, m hits (exact standard result).
#      S(N,pi) = C0(N)/C_pi(N); headline S_obs = C_desc/C_asc (ascending-vs-
#      descending ratio) = S(N,asc)/S(N,desc).
#   3. Lambda = C_sort/C_desc = C_asc/C_desc (paper-250 mapping);
#      Theta_asc = head-loading = C_sort/C0 = C_asc/C0;
#      qhat = fraction of Ns with >=1 hit in-window.
#   4. Compare mean/pooled S_obs vs [1.10, 1.51]; bootstrap CIs cluster-resampled
#      over Ns, nboot 1000; controls through the IDENTICAL pipeline must show no
#      order-asymmetry (S_obs_ctrl ~ 1).
#
# Certified bound (f1tight_connection.md point fit): 1/(Lambda*Theta*qhat)=1.5059
# (task-rounded 1.51); arm-1 binds (k_bits=0 static test-blind). Gap X := bound/S.
#
# Touches ONLY exp600_* files. No commits. Sources read: exp581_regen_positions.npz,
# f1tight_connection.md, exp582_findings.md.
# =============================================================================
import json, time, argparse
import numpy as np

NPZ    = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74/exp581_regen_positions.npz"
OUTDIR = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74/"
BOUND_CERTIFIED = 1.5059          # f1tight point-fit bound (task: 1.51)
PRED_LO, PRED_HI = 1.10, 1.51     # pre-registered two-sided acceptance band
NBOOT   = 1000
SEED    = 20260824
SMOKE_N = 16


def load(npz_path):
    d = np.load(npz_path, allow_pickle=True)
    jlo, jhi = d["jlo"].astype(np.int64), d["jhi"].astype(np.int64)
    n = len(jlo)
    hits  = [d[f"hit_{i}"].astype(np.int64) for i in range(n)]
    ctrls = [d[f"ctl_{i}"].astype(np.int64) for i in range(n)]
    return jlo, jhi, hits, ctrls


def pool_costs(pos, jlo_i, jhi_i):
    """Exact scan costs for ONE pool's hit-position set under both orders + flat booking."""
    W = jhi_i - jlo_i
    m = pos.size
    c_asc  = float(pos.min() - jlo_i + 1)     # ascending scan: first hit at min position
    c_desc = float(jhi_i - pos.max())         # descending scan: first hit at max position
    c0     = (W + 1.0) / (m + 1.0)            # flat booking: uniform-random order expectation
    return c_asc, c_desc, c0, W, m


def measures_for(pools_pos, jlo, jhi):
    """Per-pool costs + derived measures; returns dict of per-N arrays and pooled aggregates."""
    n = len(jlo)
    out = {k: np.empty(n) for k in
           ("c_asc", "c_desc", "c0", "W", "m",
            "Lambda", "Theta_asc", "S_asc", "S_desc", "S_obs", "meanx")}
    qhat_hits = 0
    oob = 0
    for i, pos in enumerate(pools_pos):
        oob += int(((pos < jlo[i]) | (pos >= jhi[i])).sum())
        ca, cd, c0, W, m = pool_costs(pos, jlo[i], jhi[i])
        out["c_asc"][i], out["c_desc"][i], out["c0"][i] = ca, cd, c0
        out["W"][i], out["m"][i] = float(W), float(m)
        out["Lambda"][i]    = ca / cd
        out["Theta_asc"][i] = ca / c0
        out["S_asc"][i]     = c0 / ca
        out["S_desc"][i]    = c0 / cd
        out["S_obs"][i]     = cd / ca
        xn = (pos - jlo[i]) / max(W - 1, 1)
        out["meanx"][i] = xn.mean()
        qhat_hits += int(pos.size > 0)
    agg = {
        "S_obs_pooled":  float(out["c_desc"].sum() / out["c_asc"].sum()),
        "Lambda_pooled": float(out["c_asc"].sum() / out["c_desc"].sum()),
        "Theta_pooled":  float(out["c_asc"].sum() / out["c0"].sum()),
        "S_obs_mean":    float(out["S_obs"].mean()),
        "Lambda_mean":   float(out["Lambda"].mean()),
        "Theta_mean":    float(out["Theta_asc"].mean()),
        "qhat":          qhat_hits / n,
        "oob":           oob,
        "meanx_grand":   float(out["meanx"].mean()),
        "total_hits":    float(out["m"].sum()),
    }
    return out, agg


def boot_ci(per, agg_keys=None, nboot=NBOOT, seed=SEED):
    """Cluster (pool-level) bootstrap of pooled-ratio aggregates; percentile CIs."""
    rng = np.random.default_rng(seed)
    n = len(per["c_asc"])
    ca, cd, c0 = per["c_asc"], per["c_desc"], per["c0"]
    allkeys = ["Lambda_pooled", "Theta_pooled", "S_obs_pooled",
               "bound_recomputed", "X"]
    if agg_keys is None:
        agg_keys = allkeys
    boots = {k: np.empty(nboot) for k in allkeys}
    for b in range(nboot):
        idx = rng.integers(0, n, n)
        s_a, s_d, s_0 = ca[idx].sum(), cd[idx].sum(), c0[idx].sum()
        lam = s_a / s_d
        tho = s_a / s_0
        boots["Lambda_pooled"][b] = lam
        boots["Theta_pooled"][b]  = tho
        boots["S_obs_pooled"][b]  = 1.0 / lam
        boots["bound_recomputed"][b] = 1.0 / (lam * tho * 1.0)   # qhat=1 in-window
        boots["X"][b] = (1.0 / (lam * tho)) / (1.0 / lam)        # bound/S = 1/Theta path
    ci = {}
    for k in agg_keys:
        lo, hi = np.percentile(boots[k], [2.5, 97.5])
        ci[k] = [float(lo), float(hi)]
    return ci


def aligned_aggs(per, idx=None):
    """Re-express the store in f1tight_connection.md's OWN convention.

    f1tight costs are SINGLE-DRAW prior expectations over the profile pi:
      C_asc = W*E_pi[x], C_desc = W*E_pi[1-x], C0 = W/2
      => Lambda = Ex/(1-Ex), Theta = 2*Ex, S = 1/Lambda, X = 1/Theta.
    (Its finite-check numbers pin this: E[x]=0.4336 -> Lambda .7656,
     Theta .867, X 1.153 -- exactly the recorded .766/.867/1.153.)
    Here pi is each pool's OWN empirical hit distribution; aggregation is
    W-weighted across pools (hit-weighted variant reported alongside).
    """
    sl = slice(None) if idx is None else idx
    W, xb = per["W"][sl], per["meanx"][sl]
    m = per["m"][sl]
    sW, sWx = W.sum(), (W * xb).sum()
    sm, smx = m.sum(), (m * xb).sum()
    ex_w, ex_h = sWx / sW, smx / sm          # W-weighted / hit-weighted E[x]
    return {
        "Ex_Wweighted": float(ex_w), "Ex_hitweighted": float(ex_h),
        "Lambda": float(ex_w / (1 - ex_w)),
        "Theta": float(2 * ex_w),
        "S_obs": float((1 - ex_w) / ex_w),
        "X": float(1.0 / (2 * ex_w)),
        "Lambda_hitweighted": float(ex_h / (1 - ex_h)),
        "S_obs_hitweighted": float((1 - ex_h) / ex_h),
    }


def aligned_boot(per, nboot=NBOOT, seed=SEED):
    rng = np.random.default_rng(seed + 2)
    n = len(per["c_asc"])
    out = {k: np.empty(nboot) for k in ("Lambda", "Theta", "S_obs", "X")}
    for b in range(nboot):
        a = aligned_aggs(per, rng.integers(0, n, n))
        for k in out:
            out[k][b] = a[k]
    return {k: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
            for k, v in out.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    t0 = time.time()

    jlo, jhi, hits, ctrls = load(NPZ)
    n_all = len(jlo)
    n = SMOKE_N if args.smoke else n_all
    jlo_s, jhi_s, hits_s = jlo[:n], jhi[:n], hits[:n]

    # ---- REAL POOLS: identical pipeline -------------------------------------
    per, agg = measures_for(hits_s, jlo_s, jhi_s)
    keys = ["Lambda_pooled", "Theta_pooled", "S_obs_pooled", "bound_recomputed", "X"]
    ci = boot_ci(per, keys)

    # ---- f1tight-ALIGNED frame (single-draw prior booking, see above) -------
    al = aligned_aggs(per)
    ci_al = aligned_boot(per)

    # ---- CONTROLS: identical pipeline ---------------------------------------
    # (a) full control sets (4000 positions each, as stored)
    per_c, agg_c = measures_for(ctrls[:n], jlo_s, jhi_s)
    # (b) count-matched controls: subsample each control set to that pool's hit
    #     multiplicity m_i (matches the real pipeline's multiplicity structure)
    rng = np.random.default_rng(SEED + 1)
    cm = []
    for i in range(n):
        mi = int(per["m"][i])
        cm.append(rng.choice(ctrls[i], size=min(mi, ctrls[i].size), replace=False))
    per_cm, agg_cm = measures_for(cm, jlo_s, jhi_s)

    # ---- COMPARISON vs pre-registered band ----------------------------------
    S = agg["S_obs_pooled"]
    if PRED_LO <= S <= PRED_HI and S < BOUND_CERTIFIED:
        verdict = "CONFIRMS"
    elif S > PRED_HI:
        verdict = "FAILS-HIGH (above registered band/bound)"
    elif S < PRED_LO:
        verdict = "FAILS-LOW (below registered band)"
    else:  # in band but >= certified bound
        verdict = "FAILS-HIGH-EDGE (in band but not below bound)"
    X = BOUND_CERTIFIED / S
    S_al = al["S_obs"]
    if PRED_LO <= S_al <= PRED_HI and S_al < BOUND_CERTIFIED:
        verdict_al = "CONFIRMS"
    elif S_al > PRED_HI:
        verdict_al = "FAILS-HIGH (above registered band/bound)"
    elif S_al < PRED_LO:
        verdict_al = "FAILS-LOW (below registered band)"
    else:
        verdict_al = "FAILS-HIGH-EDGE (in band but not below bound)"

    res = {
        "exp": "exp600 SCAN-SIM-JOINT",
        "mode": "smoke" if args.smoke else "full",
        "config": {
            "npz": NPZ, "n_pools": n, "nboot": NBOOT, "seed": SEED,
            "cost_defs": {
                "C_asc": "min(hit)-jlo+1 (ascending scan, exact degenerate dist)",
                "C_desc": "jhi-max(hit) (descending scan)",
                "C0": "(W+1)/(m+1) flat booking = E[rank of first hit under uniform-random order]",
                "S_obs": "C_desc/C_asc (ascending-vs-descending)",
                "Lambda": "C_asc/C_desc", "Theta_asc": "C_asc/C0",
                "qhat": "fraction of pools with >=1 in-window hit",
            },
            "pred_band": [PRED_LO, PRED_HI], "bound_certified": BOUND_CERTIFIED,
        },
        "measures": {
            "real": agg,
            "controls_full": agg_c,
            "controls_countmatched": agg_cm,
            "per_pool_median_S_obs": float(np.median(per["S_obs"])),
            "per_pool_IQR_S_obs": [float(np.percentile(per["S_obs"], 25)),
                                   float(np.percentile(per["S_obs"], 75))],
            "total_hits": agg["total_hits"],
            "out_of_window": agg["oob"] + agg_c["oob"],
            "single_draw_crosscheck": {
                "note": ("prior-level booking: one hit drawn uniformly from each N's "
                         "set; E[C_asc]=W*xbar, E[C_desc]=W*(1-xbar). Reproduces the "
                         "recorded profile-level Lambda (~0.766) from THIS store."),
                "Lambda_single_draw_real": float(
                    (per["W"] * per["meanx"]).sum() /
                    ((per["W"] * (1 - per["meanx"])).sum())),
                "S_single_draw_real": float(
                    ((per["W"] * (1 - per["meanx"])).sum()) /
                    ((per["W"] * per["meanx"]).sum())),
                "S_single_draw_controls": float(
                    ((per_c["W"] * (1 - per_c["meanx"])).sum()) /
                    ((per_c["W"] * per_c["meanx"]).sum())),
            },
        },
        "comparison": {
            "S_obs_pooled": S,
            "pred_band": [PRED_LO, PRED_HI],
            "bound_certified": BOUND_CERTIFIED,
            "X_measured": X,
            "X_f1tight_reference": [1.1018, 1.2205],
            "bound_recomputed_from_measured": float(
                1.0 / (agg["Lambda_pooled"] * agg["Theta_pooled"] * agg["qhat"])),
            "aligned_frame": {
                "convention": ("f1tight_connection.md sec(b): single-draw prior booking, "
                               "C_asc=W*E_pi[x], C_desc=W*E_pi[1-x], C0=W/2 => "
                               "Lambda=Ex/(1-Ex), Theta=2*Ex, S=Ex^-1*(1-Ex), X=1/(2*Ex); "
                               "pi = each pool's own empirical hit distribution"),
                "Lambda_aligned": al["Lambda"],
                "Theta_aligned": al["Theta"],
                "S_obs_aligned": al["S_obs"],
                "Ex_Wweighted": al["Ex_Wweighted"],
                "sensitivity_hitweighted": {
                    "Lambda": al["Lambda_hitweighted"], "S_obs": al["S_obs_hitweighted"]},
                "f1tight_reference_point":
                    {"E_x": 0.4336, "Lambda": 0.7657, "Theta": 0.8673,
                     "S_asc": 1.3060, "bound": 1.5059, "slack_X": 1.1530},
            },
        },
        "stats": {"bootstrap_cluster_over_pools": {"nboot": NBOOT, "seed": SEED},
                  "ci95": ci,
                  "ci95_aligned_frame": ci_al},
        "verdicts": {},
        "honest_notes": [
            "Indicator series deterministic => P(first hit at k) degenerate; sum_k k*P is an "
            "EXACT integer cost per pool, not a Monte Carlo estimate.",
            "SEMANTIC GAP / DEFINITIONAL DIFF (load-bearing): the task's literal "
            "operationalization ('cost from the indicator series under pi') prices the "
            "REALIZED multi-hit window: C_asc=min-position cost, C_desc=max-position cost, "
            "C0=(W+1)/(m+1) -- order statistics over m~75 hits. f1tight_connection.md's own "
            "algebra (its sec(b) finite check pins it) books SINGLE-DRAW PRIOR expectations: "
            "C_asc=W*E_pi[x], C_desc=W*E_pi[1-x], C0=W/2. The two conventions differ by an "
            "IDENTIFIABLE extreme-value factor ~2.65x on S (realized 3.372 vs aligned "
            "~1.27); both frames reported, registered prediction tested on BOTH.",
            "C0=(W+1)/(m+1) is an interpretive commitment (flat prior booking given the SAME "
            "hit multiplicity); alternative C0=W/2 changes Theta/X but NOT the headline "
            "ascending-vs-descending ratio S_obs.",
            "qhat is trivially 1 by pool construction (every semiprime has >=1 in-window hit); "
            "the qhat arm carries no information on this store.",
            "Controls treated as hit sets through the identical pipeline; both full (m=4000) "
            "and count-matched variants reported because asymmetry power depends on m.",
            "Single pool type (128 balanced bitlen-96 semiprimes); generalization beyond this "
            "pool class not tested here.",
        ],
        "wall_s": None,
    }

    # control verdicts: no order-asymmetry <=> bootstrap CI covers 1.0
    res["stats"]["ci95"]["S_obs_ctrl_full"] = None
    res["stats"]["ci95"]["S_obs_ctrl_countmatched"] = None
    # CIs for control S_obs (same cluster bootstrap machinery)
    ci_ctrl = boot_ci(per_c, ["S_obs_pooled"])
    ci_ctrlm = boot_ci(per_cm, ["S_obs_pooled"])
    res["stats"]["ci95"]["S_obs_ctrl_full"] = ci_ctrl["S_obs_pooled"]
    res["stats"]["ci95"]["S_obs_ctrl_countmatched"] = ci_ctrlm["S_obs_pooled"]

    # control verdicts: no order-asymmetry <=> bootstrap CI covers 1.0
    def ctrl_verdict(a, c):
        lo, hi = c["S_obs_pooled"]
        return "PASS" if (lo <= 1.0 <= hi) else "FAIL"
    res["verdicts"]["control_no_asymmetry_full"] = (
        ctrl_verdict(agg_c, ci_ctrl))
    res["verdicts"]["control_no_asymmetry_countmatched"] = (
        ctrl_verdict(agg_cm, ci_ctrlm))
    res["verdicts"]["prediction_primary"] = verdict
    res["verdicts"]["prediction_aligned_frame"] = verdict_al
    res["verdicts"]["aligned_side"] = (
        "none" if verdict_al == "CONFIRMS" else ("high" if S_al > PRED_HI else "low"))
    res["verdicts"]["prediction_side"] = (
        "none" if verdict == "CONFIRMS" else
        ("high" if S > PRED_HI else "low"))
    res["verdicts"]["prediction_magnitude"] = {
        "S_obs": S,
        "excess_over_bound": S / BOUND_CERTIFIED if S > BOUND_CERTIFIED else None,
        "shortfall_below_band": PRED_LO / S if S < PRED_LO else None,
    }
    res["wall_s"] = round(time.time() - t0, 2)

    payload = json.dumps(res, indent=2)
    if args.smoke:
        with open(OUTDIR + "exp600_smoke.log", "w") as f:
            f.write(payload + "\n")
    else:
        with open(OUTDIR + "exp600_result.json", "w") as f:
            f.write(payload + "\n")

    print(f"[{res['mode']}] n={n} wall={res['wall_s']}s")
    print(f"  S_obs_pooled={S:.4f} (band [{PRED_LO},{PRED_HI}], bound {BOUND_CERTIFIED}) "
          f"CI95 {ci['S_obs_pooled'][0]:.4f}-{ci['S_obs_pooled'][1]:.4f}")
    print(f"  Lambda={agg['Lambda_pooled']:.4f} Theta_asc={agg['Theta_pooled']:.4f} "
          f"qhat={agg['qhat']:.4f} X={X:.4f}")
    print(f"  ctrl S_obs full={agg_c['S_obs_pooled']:.4f} "
          f"countmatched={agg_cm['S_obs_pooled']:.4f} (must be ~1)")
    print(f"  ALIGNED frame: Ex={al['Ex_Wweighted']:.4f} Lambda={al['Lambda']:.4f} "
          f"Theta={al['Theta']:.4f} S_obs={S_al:.4f} "
          f"CI95 {ci_al['S_obs'][0]:.4f}-{ci_al['S_obs'][1]:.4f} X={al['X']:.4f}")
    print(f"  VERDICT realized-frame: {verdict}")
    print(f"  VERDICT aligned-frame:  {verdict_al}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# exp599 CONSECUTIVE-V-DEPENDENCY (round-74; exp598 pre-registered routing)
# =====================================================================
# PRE-REGISTRATION -- written BEFORE any analysis was run. Only the
# allowed inputs (exp581_regen_positions.npz, exp582_findings.md) were
# read beforehand; npz keys inspected for FORMAT only (hit_i = hit
# positions in j-space, ctl_i = 4000 control positions, jlo/jhi window
# bounds, 128 batches, no N stored -> analysis is purely positional).
#
# QUESTION: after j-arithmetic carriers were eliminated, do mid-window
# hits show POLYNOMIAL-SEQUENCE DEPENDENCY -- correlation between hit
# events at NEIGHBORING positions in the v/j sequence?
#
# H1 (dependency real): hit-indicator autocorrelation at lags 1-20
#   within the mid-window u in [0.55,0.75] shows |rho|>0.05 at some lag
#   with bootstrap CI excluding 0 (cluster-resampled over the 128 N
#   batches), OR runs-test rejects independence at p<0.001
#   => consecutive-v dependency exists; report lag profile.
# H0: all lags null => hit events are independent GIVEN POSITION
#   => the excess is a pure density phenomenon (rate heterogeneity
#   only); positional thread closes as "no sequence-level structure".
#
# AMENDMENT 0 (registered now, before data seen; motivation = the H0
# wording itself): because H0 is independence CONDITIONAL ON POSITION,
# and the mid-window contains the exp582 hump (rate rises then falls
# inside [0.55,0.75]), a global-mean-centered autocorrelation is
# MECHANICALLY biased positive under H0 by intra-segment rate
# curvature. Two variants therefore run side by side, registered NOW:
#   PRIMARY (decisive for H0-as-stated): position-conditioned --
#     per-batch quadratic detrend of the indicator inside the segment,
#     autocorrelation of residuals; runs test calibrated by Monte Carlo
#     against the pooled empirical rate curve p_hat(u) (the concrete
#     "density-only" null), |Z_mc|>3.29 <=> p<0.001.
#   SECONDARY (literal task reading): global-mean-centered rho +
#     textbook Wald-Wolfowitz pooled runs Z, reported but interpreted
#     through control C2 below.
# CONTROLS (identical treatment, all pre-committed expectations):
#   C1 ctl batches (random positions) -> null on BOTH variants.
#   C2 synthetic smooth-hump (iid Bernoulli at pooled rate curve p_hat)
#      -> SECONDARY goes positive, PRIMARY null: quantifies the
#      curvature confound. If C2-secondary is NOT positive, the
#      confound argument is void and the literal reading stands.
#   C3 injected lag-1 dependence at matched rate -> PRIMARY must
#      detect (power check; if C3 null, a null verdict is uninterpretable).
# Bin grid: nb=1000 bins/window (segment=200 bins); robustness at
# nb in {500,2000}. Lags 1-20. Bootstrap 2000 reps cluster-over-Ns,
# seed 20260828-lineage (599). Regen/hash: sha256 of npz recorded;
# seed-20260828 ctl regeneration attempted (two canonical recipes),
# match/mismatch reported honestly.
# Verdict rule: H1 iff PRIMARY fires (either arm); SECONDARY alone
# cannot fire H1 unless C2-secondary fails to fire (see above).
# =====================================================================
import hashlib, json, sys, time
import numpy as np

NPZ = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74/exp581_regen_positions.npz"
OUT_DIR = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74/"
LO, HI = 0.55, 0.75
LAGS = np.arange(1, 21)
NB_PRIMARY = 1000
NB_ROBUST = [500, 2000]
BOOT_REPS = 2000
SEED = 599_20260828
ZBAR = 3.2905  # two-sided p<0.001


def load(n_batches=None):
    d = np.load(NPZ, allow_pickle=True)
    jlo, jhi = d["jlo"], d["jhi"]
    nb_all = sum(1 for k in d.files if k.startswith("hit_"))
    n = nb_all if n_batches is None else min(n_batches, nb_all)
    hits = [d[f"hit_{i}"].astype(np.int64) for i in range(n)]
    ctls = [d[f"ctl_{i}"].astype(np.int64) for i in range(n)]
    return jlo[:n], jhi[:n], hits, ctls, nb_all


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def to_indicator(pos, jlo_i, jhi_i, nb):
    """Binary series over nb equal bins of the window; 1 if >=1 hit in bin."""
    u = (pos - jlo_i) / float(jhi_i - jlo_i)
    b = np.floor(u * nb).astype(np.int64)
    ok = (b >= 0) & (b < nb)
    ind = np.zeros(nb, dtype=np.float64)
    np.add.at(ind, b[ok], 1.0)
    return (ind > 0).astype(np.float64), u[ok]


def segment_slices(nb):
    centers = (np.arange(nb) + 0.5) / nb
    return np.where((centers >= LO) & (centers <= HI))[0]


def acf_lags(r, seg_idx, lags):
    """Per-series autocorr at each lag on series r restricted to seg_idx."""
    x = r[seg_idx]
    xc = x - x.mean()
    den = float(xc @ xc)
    out = np.full(len(lags), np.nan)
    if den <= 0:
        return out
    for k, L in enumerate(lags):
        if L >= len(xc):
            continue
        out[k] = float(xc[:-L] @ xc[L:]) / den
    return out


def resid_quadratic(y, seg_idx):
    """Remove [1,t,t^2] trend inside segment; return full-length residual."""
    r = y.copy().astype(np.float64)
    t = seg_idx.astype(np.float64)
    t = (t - t.mean()) / max(t.std(), 1e-12)
    X = np.column_stack([np.ones_like(t), t, t ** 2])
    beta, *_ = np.linalg.lstsq(X, y[seg_idx], rcond=None)
    r[seg_idx] = y[seg_idx] - X @ beta
    return r


def runs_z(y_seg):
    """Wald-Wolfowitz runs z on a 1-D binary series (NaN if degenerate)."""
    n = len(y_seg)
    n1 = int(y_seg.sum())
    if n1 == 0 or n1 == n:
        return np.nan
    runs = 1 + int(np.sum(y_seg[1:] != y_seg[:-1]))
    p = n1 / n
    mu = 2 * n1 * (n - n1) / n + 1
    var = 2 * n1 * (n - n1) * (2 * n1 * (n - n1) - n) / (n ** 2 * (n - 1))
    if var <= 0:
        return np.nan
    return (runs - mu) / np.sqrt(var)


def stouffer(zs):
    zs = np.asarray([z for z in zs if np.isfinite(z)])
    if len(zs) == 0:
        return np.nan
    return float(zs.sum() / np.sqrt(len(zs)))


def pipeline(indicators, seg_idx, lags):
    """Return per-batch rho matrices (secondary raw, primary detrended)."""
    nB = len(indicators)
    rho_raw = np.full((nB, len(lags)), np.nan)
    rho_det = np.full((nB, len(lags)), np.nan)
    zz = np.full(nB, np.nan)
    for i, y in enumerate(indicators):
        rho_raw[i] = acf_lags(y, seg_idx, lags)
        rd = resid_quadratic(y, seg_idx)
        rho_det[i] = acf_lags(rd, seg_idx, lags)
        zz[i] = runs_z(y[seg_idx])
    return rho_raw, rho_det, zz


def cluster_boot_rho(per_batch, reps, rng):
    """Percentile CI of nan-mean over resampled batches; returns (ci_lo, ci_hi)."""
    nB = per_batch.shape[0]
    idx = rng.integers(0, nB, size=(reps, nB))
    with np.errstate(all="ignore"):
        stats = np.nanmean(per_batch[idx], axis=1)  # reps x lags
    lo, hi = np.nanpercentile(stats, 2.5, axis=0), np.nanpercentile(stats, 97.5, axis=0)
    return lo, hi


def mc_density_null(p_hat, seg_idx, lags, reps, rng):
    """Simulate iid Bernoulli(p_hat) batches -> null dists for pooled runs Z,
    mean rho_raw, mean rho_det (the 'density-only' world)."""
    nb = len(p_hat)
    nB_ref = None  # batches drawn per rep mirror observed batch count
    z_rep = np.empty(reps)
    rr = np.empty((reps, len(lags)))
    dd = np.empty((reps, len(lags)))
    for b in range(reps):
        Y = (rng.random((N_BATCHES_REF, nb)) < p_hat[None, :]).astype(np.float64)
        a, d, z = pipeline(list(Y), seg_idx, lags)
        z_rep[b] = stouffer(z)
        rr[b] = np.nanmean(a, axis=0)
        dd[b] = np.nanmean(d, axis=0)
    return z_rep, rr, dd


def main():
    t0 = time.time()
    smoke = "--smoke" in sys.argv
    n_bat = 16 if smoke else None
    jlo, jhi, hits, ctls, nb_total = load(n_bat)
    nB = len(hits)

    # ---- data integrity checks -------------------------------------
    inside = np.mean([np.mean((h >= jlo[i]) & (h <= jhi[i])) for i, h in enumerate(hits)])
    ctl_inside = np.mean([np.mean((c >= jlo[i]) & (c <= jhi[i])) for i, c in enumerate(ctls)])

    # ---- provenance: sha256 + seed-regen attempts -------------------
    digest = sha256(NPZ)
    regen = {}
    try:
        d0 = np.load(NPZ)["ctl_0"]
        r1 = np.random.default_rng(20260828)
        g1 = np.stack([r1.integers(jlo[i], jhi[i] + 1, size=len(d0)) for i in range(1)])
        regen["rng_default_20260828_match_ctl0"] = bool(np.array_equal(g1[0], d0))
        np.random.seed(20260828)
        g2 = np.random.randint(jlo[0], jhi[0] + 1, size=len(d0))
        regen["np_random_seed_20260828_match_ctl0"] = bool(np.array_equal(g2, d0))
    except Exception as e:  # noqa: BLE001
        regen["error"] = repr(e)

    # ---- pooled rate curve p_hat(u) from hit batches -----------------
    nb = NB_PRIMARY
    seg = segment_slices(nb)
    U = np.linspace(0, 1, nb + 1)
    cnt = np.zeros(nb)
    tot_hits = 0
    for i in range(nB):
        u = (hits[i] - jlo[i]) / float(jhi[i] - jlo[i])
        b = np.floor(u * nb).astype(np.int64)
        b = b[(b >= 0) & (b < nb)]
        np.add.at(cnt, b, 1.0)
        tot_hits += len(b)
    p_raw = cnt / max(nB, 1)          # per-bin hit prob, pooled over batches
    kernel = np.ones(15) / 15.0
    p_hat = np.convolve(p_raw, kernel, mode="same")
    p_hat = np.clip(p_hat, 1e-4, 0.999)

    # ---- indicators --------------------------------------------------
    hit_ind = [to_indicator(h, jlo[i], jhi[i], nb)[0] for i, h in enumerate(hits)]
    ctl_ind = [to_indicator(c, jlo[i], jhi[i], nb)[0] for i, c in enumerate(ctls)]

    rho_raw_H, rho_det_H, z_H = pipeline(hit_ind, seg, LAGS)
    rho_raw_C, rho_det_C, z_C = pipeline(ctl_ind, seg, LAGS)

    mean_raw_H = np.nanmean(rho_raw_H, axis=0)
    mean_det_H = np.nanmean(rho_det_H, axis=0)
    mean_raw_C = np.nanmean(rho_raw_C, axis=0)
    mean_det_C = np.nanmean(rho_det_C, axis=0)
    Z_runs_H = stouffer(z_H)
    Z_runs_C = stouffer(z_C)

    rng = np.random.default_rng(SEED)
    cb_raw = cluster_boot_rho(rho_raw_H, BOOT_REPS, rng)
    cb_det = cluster_boot_rho(rho_det_H, BOOT_REPS, np.random.default_rng(SEED + 1))

    # ---- controls C2/C3 ----------------------------------------------
    rngC2 = np.random.default_rng(SEED + 2)
    Y_c2 = [(rngC2.random(nb) < p_hat).astype(np.float64) for _ in range(nB)]
    a2, d2, z2 = pipeline(Y_c2, seg, LAGS)
    c2_raw, c2_det, c2_Z = np.nanmean(a2, axis=0), np.nanmean(d2, axis=0), stouffer(z2)

    rngC3 = np.random.default_rng(SEED + 3)
    Y_c3 = []
    for _ in range(nB):
        z0 = (rngC3.random(nb) < p_hat).astype(np.float64)
        y = z0.copy()
        carry = z0[:-1] == 1
        y[1:][carry] = ((y[1:][carry] > 0) | (rngC3.random(int(carry.sum())) < 0.6)).astype(np.float64)
        Y_c3.append(y.astype(np.float64))
    a3, d3, z3 = pipeline(Y_c3, seg, LAGS)
    c3_raw, c3_det, c3_Z = np.nanmean(a3, axis=0), np.nanmean(d3, axis=0), stouffer(z3)

    # ---- MC density-only null (PRIMARY calibration) -------------------
    global N_BATCHES_REF
    N_BATCHES_REF = nB
    z_mc, rr_mc, dd_mc = mc_density_null(p_hat, seg, LAGS, 600 if smoke else BOOT_REPS,
                                         np.random.default_rng(SEED + 4))
    Z_mc_mu, Z_mc_sd = float(np.nanmean(z_mc)), float(np.nanstd(z_mc))
    Z_runs_H_mc = (Z_runs_H - Z_mc_mu) / max(Z_mc_sd, 1e-12)
    p_lag_det = 2 * np.minimum(
        np.mean(dd_mc >= mean_det_H[None, :], axis=0), np.mean(dd_mc <= mean_det_H[None, :], axis=0))

    # ---- verdicts (pre-registered rule) -------------------------------
    sig_lags_det = [int(LAGS[k]) for k in range(len(LAGS))
                    if abs(mean_det_H[k]) > 0.05 and not (cb_det[0][k] <= 0 <= cb_det[1][k])]
    sig_lags_raw = [int(LAGS[k]) for k in range(len(LAGS))
                    if abs(mean_raw_H[k]) > 0.05 and not (cb_raw[0][k] <= 0 <= cb_raw[1][k])]
    c2_secondary_fired = bool(np.any(np.abs(c2_raw) > 0.05))
    primary_fired = bool(sig_lags_det) or abs(Z_runs_H_mc) > ZBAR
    secondary_only = (not primary_fired) and bool(sig_lags_raw) and not c2_secondary_fired
    verdict = "H1_CONSECUTIVE_V_DEPENDENCY" if (primary_fired or secondary_only) else "H0_PURE_DENSITY"

    # ---- robustness binning (secondary, primary binning decides) ------
    rob = {}
    if not smoke:
        for nbr in NB_ROBUST:
            segr = segment_slices(nbr)
            ind_r = [to_indicator(h, jlo[i], jhi[i], nbr)[0] for i, h in enumerate(hits)]
            ar, dr, _ = pipeline(ind_r, segr, LAGS)
            rob[str(nbr)] = {"max_abs_rho_det": float(np.nanmax(np.abs(np.nanmean(dr, axis=0)))),
                             "max_abs_rho_raw": float(np.nanmax(np.abs(np.nanmean(ar, axis=0))))}

    res = {
        "experiment": "exp599_CONSECUTIVE_V_DEPENDENCY",
        "smoke": smoke, "n_batches": nB, "nb_bins_window": nb,
        "config": {"window_u": [LO, HI], "lags": LAGS.tolist(), "boot_reps": BOOT_REPS,
                   "mc_reps": int(len(z_mc)), "seed": SEED, "zbar": ZBAR},
        "stats": {
            "sha256_npz": digest, "regen_attempts": regen,
            "frac_hit_inside_window": float(inside), "frac_ctl_inside_window": float(ctl_inside),
            "total_hits": int(tot_hits),
            "mean_rate_in_segment": float(np.mean(p_hat[seg])),
            "mean_rate_outside_segment": float(np.mean(np.delete(p_hat, seg))),
            "Z_runs_hit_textbook": float(Z_runs_H), "Z_runs_ctl_textbook": float(Z_runs_C),
            "Z_runs_hit_mc_calibrated": float(Z_runs_H_mc),
            "Z_mc_null_mu_sd": [Z_mc_mu, Z_mc_sd],
            "mc_p_lag_detrended": p_lag_det.tolist(),
            "control_C2_synthetic_hump": {"max_abs_rho_raw": float(np.max(np.abs(c2_raw))),
                                          "argmax_lag": int(LAGS[np.argmax(np.abs(c2_raw))]),
                                          "max_abs_rho_det": float(np.max(np.abs(c2_det))),
                                          "pooled_Z": float(c2_Z),
                                          "secondary_confound_demonstrated": c2_secondary_fired},
            "control_C3_injected_lag1_dep": {"max_abs_rho_det": float(np.max(np.abs(c3_det))),
                                             "argmax_lag": int(LAGS[np.argmax(np.abs(c3_det))]),
                                             "rho_det_lag1": float(c3_det[0]),
                                             "pooled_Z": float(c3_Z),
                                             "power_ok": bool(abs(c3_det[0]) > 0.05)},
        },
        "lag_profile": {
            "lags": LAGS.tolist(),
            "rho_secondary_global_mean_hit": mean_raw_H.tolist(),
            "rho_primary_detrended_hit": mean_det_H.tolist(),
            "rho_ctl_raw": mean_raw_C.tolist(), "rho_ctl_detrended": mean_det_C.tolist(),
            "boot_ci_detrended_lo": cb_det[0].tolist(), "boot_ci_detrended_hi": cb_det[1].tolist(),
            "boot_ci_raw_lo": cb_raw[0].tolist(), "boot_ci_raw_hi": cb_raw[1].tolist(),
        },
        "verdicts": {
            "verdict": verdict,
            "primary_fired": primary_fired, "sig_lags_detrended": sig_lags_det,
            "secondary_sig_lags_raw": sig_lags_raw,
            "secondary_only_and_c2_failed": secondary_only,
            "runs_arm": {"textbook_Z": float(Z_runs_H), "mc_calibrated_Z": float(Z_runs_H_mc),
                         "fired": bool(abs(Z_runs_H_mc) > ZBAR)},
            "controls_null_as_expected":
                bool(np.all(np.abs(mean_det_C) < 0.05)),
        },
        "robustness_other_binnings": rob,
        "honest_notes": [
            "No N values in npz -> purely positional point-process analysis; 'v-sequence' operationalized as j-position order, binned.",
            "AMENDMENT 0 (pre-data): H0 says 'independent GIVEN position'; intra-segment hump curvature mechanically biases global-mean rho positive, so PRIMARY = quadratic-detrended rho + MC-calibrated runs Z against pooled rate curve; literal reading kept as SECONDARY.",
            f"C2 synthetic smooth-hump secondary fired={c2_secondary_fired}: if True, raw-positive readings alone cannot establish dependency.",
            "MC null approximates all batches sharing pooled p_hat (per-batch rate heterogeneity folded into cluster bootstrap instead).",
            f"Seed-regen of ctl_0 from seed 20260828: {regen} -- recipe not recoverable from allowed reads if mismatch; provenance rests on sha256.",
        ],
        "wall_s": None,
    }
    res["wall_s"] = round(time.time() - t0, 2)
    tag = "smoke" if smoke else "result"
    with open(OUT_DIR + f"exp599_{tag}.json", "w") as f:
        json.dump(res, f, indent=1, default=float)
    print(json.dumps({"verdict": verdict, "primary_fired": primary_fired,
                      "sig_lags_det": sig_lags_det, "sig_lags_raw": sig_lags_raw,
                      "rho_raw_max": float(np.max(np.abs(mean_raw_H))),
                      "rho_det_max": float(np.max(np.abs(mean_det_H))),
                      "Z_runs_textbook": float(Z_runs_H),
                      "Z_runs_mc": float(Z_runs_H_mc),
                      "C2_fired": c2_secondary_fired, "C3_power_ok": res["stats"]["control_C3_injected_lag1_dep"]["power_ok"],
                      "inside_frac": float(inside), "wall_s": res["wall_s"]}, indent=1))
    if smoke:
        print("LAG PROFILE (det | raw):")
        for k in range(len(LAGS)):
            print(f"  lag{LAGS[k]:>3}: {mean_det_H[k]:+.4f} | {mean_raw_H[k]:+.4f}")


def jlo_i_guard(i, jlo, jhi):  # never used; kept out of hot path
    return jlo[i]


if __name__ == "__main__":
    main()

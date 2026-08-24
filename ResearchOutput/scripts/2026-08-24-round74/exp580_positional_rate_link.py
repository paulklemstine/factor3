#!/usr/bin/env python3
# EXP580 POSITIONAL-RATE-LINK (round-74, paper-228 follow-up (b))
#
# QUESTION: unify exp578's WITHIN-N positional view with the BETWEEN-N rate
# view: do HIT-RICH Ns (top tercile of per-N hit counts) show DIFFERENT
# positional profiles than HIT-POOR Ns?
#
# PRE-REGISTRATION (written into this header BEFORE any rich/poor split,
# profile, KS, or regression result was computed or inspected):
#
#   H1 (profile-rate coupling): hit-rich vs hit-poor positional profiles DIFFER.
#     Fires iff FIRE_A or FIRE_B below (with matched control-arm null):
#       FIRE_A: any of (a) the 3 pairwise pooled two-sample KS tests between
#         tercile hit-position samples (rich-poor, rich-mid, poor-mid) with
#         Bonferroni x3 has p_adj<0.01, or (b) any per-decile KS (10 deciles x
#         3 pairs, Bonferroni x30) has p_adj<0.01.
#       FIRE_B: joint LRT of the 49 binned-position x richness interaction
#         terms in the logistic regression hits-in-bin ~ rich + bin + rich*bin
#         (rows = N x 50 bins, rich vs poor terciles only, middle excluded;
#         pre-stated) gives chi2 p<0.01 (df=49) CONFIRMED by label-permutation
#         p<0.05 (500 shuffles of the rich label).
#     => positional and rate views are ONE mechanism seen twice; the small-j
#        locus concentrates preferentially around specific N classes.
#   H0: profiles identical across rich/poor terciles (neither family fires, or
#     fires only where the control arm also fires) => positional geometry and
#     rate variance are INDEPENDENT layers -> TWO separate map entries.
#   CONTROL ARM (must be null): identical split + stats applied to the PAIRED
#     non-hit controls (ctl_*), grouped by their host N's treatment-derived
#     tercile label, SIZE-MATCHED to that N's hit count (count_i controls drawn
#     once, fixed seed) so occupancy matches the treatment arm; degenerate
#     all-4000-count control split pre-disclosed as unusable.
#   Decision rule: H1 iff (FIRE_A_treat or FIRE_B_treat) and the same family is
#     null in controls at the same bars. Otherwise H0.
#
# Data: exp578_positions.npz (128 balanced bitlen-96 semiprimes, master seed
# 20260828; 150k j-samples/N on [isqrt+1, 3*isqrt], cut 1e6). Keys hit_{i}
# (ragged hit j positions), ctl_{i} (4000 non-hit j samples), jlo/jhi.
# Normalized position u = (j - jlo)/(jhi - jlo) in [0,1].
import json, time
import numpy as np
from scipy import stats

T0 = time.time()
RNG_SEED = 20260824
rng = np.random.default_rng(RNG_SEED)
D = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74"
NBINS = 50
NBOOT = 2000
NPERM = 500

z = np.load(f"{D}/exp578_positions.npz")
nN = len(z["jlo"])
jlo, jhi = z["jlo"].astype(float), z["jhi"].astype(float)
hits = [(z[f"hit_{i}"].astype(float) - jlo[i]) / (jhi[i] - jlo[i]) for i in range(nN)]
ctls = [(z[f"ctl_{i}"].astype(float) - jlo[i]) / (jhi[i] - jlo[i]) for i in range(nN)]
counts = np.array([len(h) for h in hits])
assert all(0.0 <= h.min() and h.max() <= 1.0 for h in hits)

# --- tercile split by per-N hit count (rank-based, ties by order) ---
order = np.argsort(counts, kind="stable")
t = nN // 3
poor_ids, mid_ids, rich_ids = order[:t], order[t : 2 * t], order[2 * t :]
labels = np.array(["poor"] * t + ["mid"] * (2 * t - t) + ["rich"] * (nN - 2 * t))
lab_by_n = {}
for ids, nm in ((poor_ids, "poor"), (mid_ids, "mid"), (rich_ids, "rich")):
    for i in ids:
        lab_by_n[int(i)] = nm
tercile_bounds = {
    "poor_count_max": int(counts[poor_ids].max()),
    "mid_range": [int(counts[mid_ids].min()), int(counts[mid_ids].max())],
    "rich_count_min": int(counts[rich_ids].min()),
}

edges = np.linspace(0, 1, NBINS + 1)


def profile(us_by_n, ids):
    """Pooled bin-fraction profile + cluster bootstrap (resample Ns) CI."""
    pools = [np.histogram(us_by_n[i], bins=edges)[0] for i in ids]
    P = np.array(pools, float)
    tot = P.sum()
    frac = P.sum(0) / tot
    boots = np.empty((NBOOT, NBINS))
    m = len(ids)
    for b in range(NBOOT):
        pick = rng.integers(0, m, m)
        boots[b] = P[pick].sum(0) / P[pick].sum()
    lo, hi = np.percentile(boots, [2.5, 97.5], axis=0)
    pooled_us = np.concatenate([us_by_n[i] for i in ids])
    return {"frac": frac.tolist(), "ci_lo": lo.tolist(), "ci_hi": hi.tolist(),
            "mean_u": float(pooled_us.mean()),
            "edge_decile_frac": float(((pooled_us < 0.1) | (pooled_us >= 0.9)).sum() / pooled_us.size),
            "n_hits": int(tot), "n_N": m}


def ks_block(us_by_n, ids_rich, ids_poor, ids_mid, tag):
    """Family-A KS tests: 3 pooled pairwise + per-decile (x10) pairwise."""
    out = {"tag": tag, "pooled": [], "per_decile_min_p": {}}
    groups = {"rich": ids_rich, "mid": ids_mid, "poor": ids_poor}
    samp = {k: np.concatenate([us_by_n[i] for i in v]) for k, v in groups.items()}
    for a, b in (("rich", "poor"), ("rich", "mid"), ("poor", "mid")):
        r = stats.ks_2samp(samp[a], samp[b])
        out["pooled"].append({"pair": f"{a}-{b}", "D": float(r.statistic), "p": float(r.pvalue)})
    # per-decile: restrict both samples to each decile of u, KS within
    for d in range(10):
        e0, e1 = d / 10, (d + 1) / 10
        best = None
        for a, b in (("rich", "poor"), ("rich", "mid"), ("poor", "mid")):
            xa = samp[a][(samp[a] >= e0) & (samp[a] < e1)]
            xb = samp[b][(samp[b] >= e0) & (samp[b] < e1)]
            if len(xa) < 20 or len(xb) < 20:
                continue
            r = stats.ks_2samp(xa, xb)
            cand = {"pair": f"{a}-{b}", "decile": d, "p": float(r.pvalue)}
            if best is None or cand["p"] < best["p"]:
                best = cand
        out["per_decile_min_p"][str(d)] = best
    ps_pool = [x["p"] for x in out["pooled"]]
    ps_all = ps_pool + [v["p"] for v in out["per_decile_min_p"].values() if v]
    k = len(ps_all)
    out["n_tests_bonferroni"] = k
    out["min_p_raw"] = float(min(ps_all))
    out["min_p_bonferroni"] = float(min(1.0, min(ps_all) * k))
    return out


def fit_logit(X, y, ridge=1e-8, iters=100):
    beta = np.zeros(X.shape[1])
    for _ in range(iters):
        eta = X @ beta
        mu = 1.0 / (1.0 + np.exp(-eta))
        W = np.clip(mu * (1 - mu), 1e-10, None)
        g = X.T @ (y - mu) - ridge * beta
        H = (X.T * W) @ X + ridge * np.eye(X.shape[1])
        step = np.linalg.solve(H, g)
        beta_new = beta + step
        if np.max(np.abs(step)) < 1e-9:
            beta = beta_new
            break
        beta = beta_new
    eta = X @ beta
    mu = 1.0 / (1.0 + np.exp(-eta))
    ll = float(np.sum(y * np.log(np.clip(mu, 1e-12, 1)) + (1 - y) * np.log(np.clip(1 - mu, 1e-12, 1))))
    return beta, ll


def regress(us_by_n, ids_rich, ids_poor, tag):
    """Family-B logistic: rows = (N, bin); y = >=1 hit in that bin."""
    allids = sorted(set(ids_poor) | set(ids_rich))
    rich_set = set(ids_rich)
    n = len(allids)
    OCC = np.zeros((n, NBINS))
    rich = np.zeros(n)
    for k, i in enumerate(allids):
        OCC[k] = np.histogram(us_by_n[i], bins=edges)[0]
        rich[k] = 1.0 if i in rich_set else 0.0
    y = (OCC > 0).astype(float).ravel()
    rich_flat = np.repeat(rich, NBINS)
    bins_idx = np.tile(np.arange(NBINS), n)
    Bm = np.zeros((len(bins_idx), NBINS - 1))
    for j in range(1, NBINS):
        Bm[:, j - 1] = (bins_idx == j)
    ones = np.ones((len(bins_idx), 1))
    X_add = np.hstack([ones, rich_flat.reshape(-1, 1), Bm])
    X_full = np.hstack([X_add, rich_flat.reshape(-1, 1) * Bm])
    b_add, ll_add = fit_logit(X_add, y)
    b_full, ll_full = fit_logit(X_full, y)
    lr = 2 * (ll_full - ll_add)
    p_lrt = float(stats.chi2.sf(lr, NBINS - 1))
    # Wald ORs + CIs for interaction terms
    Hinv = None
    eta = X_full @ b_full
    mu = 1 / (1 + np.exp(-eta))
    W = np.clip(mu * (1 - mu), 1e-10, None)
    cov = np.linalg.inv((X_full.T * W) @ X_full + 1e-8 * np.eye(X_full.shape[1]))
    se = np.sqrt(np.diag(cov))
    inter = b_full[X_add.shape[1]:]
    se_i = se[X_add.shape[1]:]
    OR = np.exp(np.clip(inter, -30, 30))
    ci_lo = np.exp(np.clip(inter - 1.96 * se_i, -30, 30))
    ci_hi = np.exp(np.clip(inter + 1.96 * se_i, -30, 30))
    pz = 2 * stats.norm.sf(np.abs(inter / se_i))
    # permutation: shuffle rich label among rich+poor Ns, recompute LRT
    perm_stats = []
    allids = ids_poor + ids_rich
    for _ in range(NPERM):
        perm = rng.permutation(len(allids))
        pr = [allids[k] for k in perm[: len(ids_rich)]]
        pp = [allids[k] for k in perm[len(ids_rich):]]
        pr_set = set(pr)
        rf = np.array([1.0 if i in pr_set else 0.0 for i in allids])
        rf_flat = np.repeat(rf, NBINS)
        Xa = np.hstack([ones, rf_flat.reshape(-1, 1), Bm])
        Xf = np.hstack([Xa, rf_flat.reshape(-1, 1) * Bm])
        _, la = fit_logit(Xa, y)
        _, lf = fit_logit(Xf, y)
        perm_stats.append(2 * (lf - la))
    perm_p = float((np.sum(np.array(perm_stats) >= lr) + 1) / (NPERM + 1))
    return {"tag": tag, "n_rows": int(n), "ll_add": ll_add, "ll_full": ll_full,
            "LRT_chi2": float(lr), "df": NBINS - 1, "LRT_p": p_lrt,
            "perm_p": perm_p,
            "OR_min": float(OR.min()), "OR_max": float(OR.max()),
            "OR_median": float(np.median(OR)),
            "n_bins_wald_p<0.05": int((pz < 0.05).sum()),
            "wald_p_min": float(pz.min())}


def size_matched_controls(us_ctl, hit_counts):
    """Draw count_i controls per N once (seeded); returns dict n -> u array."""
    out = {}
    for i in range(nN):
        c = us_ctl[i]
        take = rng.choice(len(c), size=int(hit_counts[i]), replace=False)
        out[i] = c[take]
    return out


results = {"config": {"exp": 580, "name": "POSITIONAL-RATE-LINK",
                      "source_npz": "exp578_positions.npz", "nbins": NBINS,
                      "nboot": NBOOT, "nperm": NPERM, "seed": RNG_SEED,
                      "regression_scope": "rich vs poor terciles only, middle excluded (pre-stated)",
                      "control": "paired ctl_*, grouped by host-N treatment tercile label, size-matched to hit count"}}
counts_int = counts.astype(int)

# ---------------- TREATMENT ARM ----------------
prof = {g: profile(hits, ids) for g, ids in (("rich", rich_ids), ("mid", mid_ids), ("poor", poor_ids))}
ks_t = ks_block(hits, rich_ids, poor_ids, mid_ids, "treatment")
rg_t = regress(hits, sorted(rich_ids.tolist()), sorted(poor_ids.tolist()), "treatment")

# ---------------- CONTROL ARM ----------------
ctl_matched = size_matched_controls(ctls, counts_int)
prof_c = {g: profile(ctl_matched, ids) for g, ids in (("rich", rich_ids), ("mid", mid_ids), ("poor", poor_ids))}
ks_c = ks_block(ctl_matched, rich_ids, poor_ids, mid_ids, "control")
rg_c = regress(ctl_matched, sorted(rich_ids.tolist()), sorted(poor_ids.tolist()), "control")

def meanu_diff_boot(us_by_n, ids_a, ids_b):
    """Descriptive: equal-weight-per-N mean_u difference, cluster-bootstrap CI."""
    ma = np.array([us_by_n[i].mean() for i in ids_a])
    mb = np.array([us_by_n[i].mean() for i in ids_b])
    est = float(ma.mean() - mb.mean())
    bs = np.empty(NBOOT)
    for b in range(NBOOT):
        ra = ma[rng.integers(0, len(ma), len(ma))].mean()
        rb = mb[rng.integers(0, len(mb), len(mb))].mean()
        bs[b] = ra - rb
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"est": est, "ci95": [float(lo), float(hi)]}


fire_a = ks_t["min_p_bonferroni"] < 0.01
fire_b = rg_t["LRT_p"] < 0.01 and rg_t["perm_p"] < 0.05
ctrl_clean_a = ks_c["min_p_bonferroni"] >= 0.01
ctrl_clean_b = not (rg_c["LRT_p"] < 0.01 and rg_c["perm_p"] < 0.05)
if (fire_a or fire_b):
    verdict = "H1_PROFILE_RATE_COUPLED" if (ctrl_clean_a and ctrl_clean_b) else \
              "INCONCLUSIVE_TREATMENT_FIRES_CONTROL_ALSO_FIRES"
else:
    verdict = "H0_INDEPENDENT_LAYERS"

results.update({
    "terciles": {"bounds": tercile_bounds,
                 "sizes": {"poor": len(poor_ids), "mid": len(mid_ids), "rich": len(rich_ids)},
                 "count_mean": float(counts.mean()), "count_min": int(counts.min()),
                 "count_max": int(counts.max())},
    "profiles_treatment": prof, "profiles_control": prof_c,
    "ks_treatment": ks_t, "ks_control": ks_c,
    "regression_treatment": rg_t, "regression_control": rg_c,
    "mean_u_diff_rich_minus_poor": {
        "treatment": meanu_diff_boot(hits, rich_ids, poor_ids),
        "control_matched": meanu_diff_boot(ctl_matched, rich_ids, poor_ids)},
    "verdicts": {"FIRE_A_treatment": bool(fire_a), "FIRE_B_treatment": bool(fire_b),
                 "control_family_A_null": bool(ctrl_clean_a), "control_family_B_null": bool(ctrl_clean_b),
                 "VERDICT": verdict},
})

# honest notes
edge_t = {g: prof[g]["edge_decile_frac"] for g in prof}
notes = [
    "Pre-registration written in script header before any split/profile/regression was computed.",
    "Middle tercile excluded from the regression by pre-statement; used only in KS pairwise.",
    "Control per-N hit counts are constant 4000 -> tercile-by-count degenerate; control arm "
    "therefore uses treatment-derived labels with SIZE-MATCHED control draws (count_i per N, one seeded draw).",
    "Regression outcome is bin OCCUPANCY (>=1 hit), not hit multiplicity; richness main effect "
    "absorbs level differences, interaction terms test SHAPE only.",
    "Wald per-bin interaction p-values are exploratory (~50 tests); the gated statistic is the joint LRT + permutation.",
    "Sparse tail bins produce quasi-separation: some interaction betas diverge (OR clipped at e^+-30, "
    "Wald CIs blow up) -> per-bin ORs NOT interpretable; only the joint LRT/perm is used.",
    f"Control arm family-B fired (LRT p={rg_c['LRT_p']:.4f}, perm p={rg_c['perm_p']:.4f}): the occupancy "
    "regression is not clean on dense size-matched controls; treatment family-B was far from the bar "
    "(p=0.38), so H0 does not rest on it — but treat this regression design as fragile on controls.",
    "Rich-poor pooled KS raw p<0.01 but fails Bonferroni; reported as a descriptive hint with the "
    "mean_u-diff bootstrap CI, NOT as a fire.",
    f"Treatment edge-decile fracs rich/mid/poor: {edge_t['rich']:.4f}/{edge_t['mid']:.4f}/{edge_t['poor']:.4f}.",
    "Single seed, single bitlen (96), 128 Ns; exp578 established the u-profile is real beyond magnitude conditioning.",
]
results["honest_notes"] = notes

with open(f"{D}/exp580_result.json", "w") as f:
    json.dump(results, f, indent=1)

print("VERDICT:", verdict)
print("tercile bounds:", tercile_bounds, "sizes", results["terciles"]["sizes"])
print("KS treat pooled:", [(x['pair'], round(x['D'],4), f"{x['p']:.3g}") for x in ks_t["pooled"]],
      "minBonf", f"{ks_t['min_p_bonferroni']:.3g}")
print("KS ctrl  pooled:", [(x['pair'], round(x['D'],4), f"{x['p']:.3g}") for x in ks_c["pooled"]],
      "minBonf", f"{ks_c['min_p_bonferroni']:.3g}")
for tg, blk in (("treat", ks_t), ("ctrl", ks_c)):
    worst = [(d, v["pair"], f"{v['p']:.3g}") for d, v in blk["per_decile_min_p"].items() if v and v["p"] < 0.01]
    print(f"{tg} per-decile p<0.01 cells:", worst if worst else "none")
print("REGR treat: LRT chi2=%.2f df=%d p=%.3g perm_p=%.4f ORmed=%.3f [%.3f,%.3f] wald<.05:%d/%d"
      % (rg_t["LRT_chi2"], rg_t["df"], rg_t["LRT_p"], rg_t["perm_p"], rg_t["OR_median"],
         rg_t["OR_min"], rg_t["OR_max"], rg_t["n_bins_wald_p<0.05"], rg_t["df"]))
print("REGR ctrl : LRT chi2=%.2f p=%.3g perm_p=%.4f" % (rg_c["LRT_chi2"], rg_c["LRT_p"], rg_c["perm_p"]))
for g in ("rich", "mid", "poor"):
    p = prof[g]
    print(f"profile {g}: mean_u={p['mean_u']:.4f} edge={p['edge_decile_frac']:.4f} "
          f"bin1={p['frac'][0]:.4f}[{p['ci_lo'][0]:.4f},{p['ci_hi'][0]:.4f}] "
          f"bin50={p['frac'][-1]:.4f} n={p['n_hits']} Ns={p['n_N']}")
print("mean_u rich-poor diff:", results["mean_u_diff_rich_minus_poor"])
print(f"wall {time.time()-T0:.1f}s")

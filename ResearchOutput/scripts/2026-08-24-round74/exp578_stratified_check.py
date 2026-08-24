#!/usr/bin/env python3
"""exp578 STRATIFIED MAGNITUDE-CONFOUND CHECK + leg-b control repair.

Coordinator-directed check, run on the STORED positions (exp578_positions.npz,
no resampling). Confound: v = j^2 - N rises monotonically across the j-window,
so smoothness decay with |v| alone skews hits toward small u even under ZERO
positional structure -- leg (a)'s uniform-KS and the elevated edge fraction are
a priori confounded by magnitude.

RULE (stated before the check ran):
  Stratify every hit and non-hit by v-cell = (bitlen(v), mantissa-octant(v))
  [octant = top-3 mantissa bits: floor((v/2^(bl-1) - 1)*8) in 0..7].
  Within each cell compare hit-u vs SIZE-MATCHED non-hit-u:
    (i) per-cell two-sample KS p<0.01 firing count vs 1% expectation;
    (ii) pooled stratified D = sum(n_s*D_s)/sum(n_s) with within-cell label
         permutation (2000 reps, seed 20260830) -> overall p;
    (iii) stratified edge-decile test: observed treatment edges vs expected
          from per-cell control edge rates (normal z).
  VERDICT AMENDMENT: perm-p < 0.01 (or >=3x expected cells firing at p<0.01)
     => BEYOND-MAGNITUDE (original H1 stands strong);
     else => PROFILE-IS-SIZE-GRADIENT (H1 downgrades: positional profile is
     fully explained by the v-size gradient; residual dispersion stays N-level).

Also repairs the CONTROL-arm leg-b autocorr (first run mirrored treatment;
recomputed here from stored paired non-hits) and patches exp578_result.json.
"""
import json, math, random
import numpy as np
import scipy.stats as st

SEED_PERM = 20260830
BOOT_SEED = 20260829
NBINS = 1000
LAGS = list(range(1, 11))
MIN_CELL = 30          # min treatment hits AND controls per v-cell
PERMS = 2000
EDGE_LO, EDGE_HI = 0.10, 0.90

d = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74/"
z = np.load(d + "exp578_positions.npz")
res = json.load(open(d + "exp578_result.json"))
rows = res["rows"]
n_pool = len(rows)
assert n_pool == len(z["jlo"]) == 128

jlo = z["jlo"].astype(object); jhi = z["jhi"].astype(object)
Nbig = [int(r["N"]) for r in rows]

def octant(v):
    bl = v.bit_length()
    if bl <= 1: return bl, 0
    top = v >> (bl - 4)          # 4 bits: leading 1 + 3 mantissa bits
    return bl, int(top & 7)

# ---- collect per-N arrays; normalize u; compute v-cells ----
cells_t = {}; cells_c = {}          # cell -> list of u
u_all_t = []; u_all_c = []
hit_js_all = []; ctl_js_all = []
for i in range(n_pool):
    hj = z[f"hit_{i}"]; cj = z[f"ctl_{i}"][:len(hj)]
    lo_, hi_ = jlo[i], jhi[i]
    span = hi_ - lo_
    ut = (hj - lo_) / span
    uc = (cj - lo_) / span
    N = Nbig[i]
    vt = hj*hj - N; vc = cj*cj - N
    for j_, v_ in zip(hj.tolist(), vt.tolist()):
        c = octant(int(v_))
        cells_t.setdefault(c, []).append((j_ - lo_) / span)
    for j_, v_ in zip(cj.tolist(), vc.tolist()):
        c = octant(int(v_))
        cells_c.setdefault(c, []).append((j_ - lo_) / span)
    u_all_t.append(ut); u_all_c.append(uc)
    hit_js_all.append(hj); ctl_js_all.append(cj)

# ---- (i)+(ii): per-cell two-sample KS + permutation-pooled D ----
common = sorted(set(cells_t) & set(cells_c))
used = []
Ds = []; ns = []; ps = []
for c in common:
    t = np.array(cells_t[c]); k = np.array(cells_c[c])
    if len(t) < MIN_CELL or len(k) < MIN_CELL:
        continue
    ks = st.ks_2samp(t, k)
    used.append(c); Ds.append(float(ks.statistic)); ps.append(float(ks.pvalue)); ns.append(len(t))
Ds = np.array(Ds); ns_ = np.array(ns)
pooled_D = float((Ds*ns_).sum()/ns_.sum())

# within-cell label permutation keeping cell sizes
rng = random.Random(SEED_PERM)
perm_D = []
cell_arrays = [(np.array(cells_t[c]), np.array(cells_c[c])) for c in used]
for _ in range(PERMS):
    num = 0.0; den = 0
    for t, k in cell_arrays:
        pool = np.concatenate([t, k]); n1 = len(t)
        perm = rng.sample(range(len(pool)), len(pool))
        a = pool[perm[:n1]]; b = pool[perm[n1:]]
        dd = st.ks_2samp(a, b).statistic
        num += dd*n1; den += n1
    perm_D.append(num/den)
perm_D = np.array(perm_D)
perm_p = float((perm_D >= pooled_D).mean())
cells_fire = sum(1 for p in ps if p < 0.01)
exp_fire = 0.01*len(ps)

# ---- (iii): stratified edge-decile ----
obs_e = 0; exp_e = 0.0; var_e = 0.0
for c in common:
    t = np.array(cells_t[c]); k = np.array(cells_c[c])
    if len(t) == 0 or len(k) == 0:
        continue
    r_s = float(((k < EDGE_LO) | (k > EDGE_HI)).mean())
    obs_e += int(((t < EDGE_LO) | (t > EDGE_HI)).sum())
    exp_e += r_s*len(t)
    var_e += len(t)*r_s*(1-r_s)
z_edge = (obs_e - exp_e)/math.sqrt(var_e) if var_e > 0 else float("nan")

# ---- descriptive decile profiles (pooled, unstratified) ----
T = np.concatenate(u_all_t); K = np.concatenate(u_all_c)
td = np.histogram(T, bins=10, range=(0, 1))[0]/len(T)
kd = np.histogram(K, bins=10, range=(0, 1))[0]/len(K)

# ---- leg-b repair: TRUE control autocorr from paired non-hits ----
def acf_series(js_list, idxs):
    out = []
    for i in idxs:
        hj = js_list[i]; s0 = int(jlo[i]) + 1; s1 = int(jhi[i])
        ht = np.zeros(NBINS)
        b = ((hj - s0)*NBINS//(s1 - s0)).clip(max=NBINS-1)
        np.add.at(ht, b, 1)
        out.append((i, ht))
    return out

idx30 = [r["i"] for r in rows if r["hits"] >= 30]
def lagstats(series):
    pm = []; pl = [[] for _ in LAGS]
    for i, x in series:
        xc = x - x.mean(); den = float((xc*xc).sum())
        if den <= 0: continue
        rs = []
        for li, lag in enumerate(LAGS):
            r = float((xc[:-lag]*xc[lag:]).sum())/den
            rs.append(r); pl[li].append(r)
        pm.append(sum(rs)/len(rs))
    br = random.Random(BOOT_SEED); bs = []
    for _ in range(2000):
        samp = [pm[br.randrange(len(pm))] for _ in pm]
        bs.append(sum(samp)/len(samp))
    bs.sort()
    m = sum(pm)/len(pm)
    return {"n_Ns": len(pm), "mean_rho_lags1_10": round(m, 5),
            "boot95": [round(bs[int(0.025*2000)], 5), round(bs[int(0.975*2000) - 1], 5)],
            "ci_excludes_0": bool(bs[int(0.025*2000)] > 0 or bs[int(0.975*2000)-1] < 0),
            "per_lag_mean_rho": [round(sum(v)/len(v), 5) if v else float("nan") for v in pl]}
ctl_true = lagstats(acf_series([z[f"ctl_{i}"][:len(z[f'hit_{i}'])] for i in range(n_pool)], idx30))

# ---- verdict amendment rule (pre-stated) ----
beyond = bool(perm_p < 0.01 or cells_fire >= max(3, 3*exp_fire))
amended_verdict = ("BEYOND-MAGNITUDE-POSITIONAL-STRUCTURE" if beyond
                   else "PROFILE-IS-SIZE-GRADIENT-H1-DOWNGRADED")

check = {
    "rule_stated_before_check": True,
    "confound": "v=j^2-N monotone in j -> pure smoothness decay skews hits small-u",
    "stratification": "v-cell = (bitlen(v), mantissa-octant(v)); min 30/30 per cell",
    "n_cells_total": len(common), "n_cells_used": len(used),
    "hits_covered_by_cells": int(ns_.sum()),
    "per_cell_KS_p_bar": 0.01,
    "cells_firing_p<0.01": cells_fire, "expected_if_null": round(exp_fire, 2),
    "median_per_cell_p": float(np.median(ps)),
    "pooled_stratified_D": round(pooled_D, 5),
    "permutation_p": perm_p, "n_perms": PERMS, "perm_seed": SEED_PERM,
    "stratified_edge": {"observed_edges": obs_e, "expected_edges": round(exp_e, 1),
                        "z_vs_cell_matched": round(z_edge, 3)},
    "unstratified_deciles_treatment": [round(x, 4) for x in td],
    "unstratified_deciles_control": [round(x, 4) for x in kd],
    "leg_b_control_TRUE_repaired": ctl_true,
    "verdict_amendment": amended_verdict,
    "beyond_magnitude": beyond,
}

# ---- patch result JSON ----
res["arms"]["control"]["leg_b_lag_autocorr"] = ctl_true
fired_legs_c = [k for k in ("leg_a_pooled_KS", "leg_b_lag_autocorr", "leg_c_edge_decile")
                if (k != "leg_b_lag_autocorr" and res["arms"]["control"][k]["fires"])
                or (k == "leg_b_lag_autocorr" and abs(ctl_true["mean_rho_lags1_10"]) > 0.05
                    and ctl_true["ci_excludes_0"])]
res["verdicts"]["control_fired_legs"] = fired_legs_c
res["magnitude_confound_check"] = check
res["verdicts"]["magnitude_confound_amendment"] = {
    "amended_verdict": amended_verdict,
    "reading": ("H1 stands strong: within size-strata, hit positions still "
                "deviate from their size-matched null (KS fires inside strata)"
                if beyond else
                "H1 downgraded: the positional profile IS the v-size gradient "
                "(smoothness decay); no beyond-magnitude positional geometry"),
}
res["honest_notes"].append(
    "MAGNITUDE CONFOUND CHECK (post-hoc, coordinator-directed; "
    "exp578_stratified_check.py): conditioning on (bitlen(v) x mantissa-octant) "
    "and comparing to SIZE-MATCHED paired non-hits, pooled stratified KS "
    f"D={pooled_D:.5f}, permutation p={perm_p:.4f}; {cells_fire}/{len(ps)} cells "
    f"fire at p<0.01 (null expects ~{exp_fire:.1f}); stratified-edge z={z_edge:.2f}. "
    f"Amendment: {amended_verdict}. Control leg-b also repaired here.")
with open(d + "exp578_result.json", "w") as f:
    json.dump(res, f, indent=1)

print(json.dumps({k: v for k, v in check.items() if k not in
                  ("unstratified_deciles_treatment", "unstratified_deciles_control",
                   "leg_b_control_TRUE_repaired")}, indent=1)[:2500])
print("deciles T:", [round(x, 3) for x in td])
print("deciles K:", [round(x, 3) for x in kd])
print("AMENDED VERDICT:", amended_verdict)

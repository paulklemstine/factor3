#!/usr/bin/env python3
# =====================================================================
# exp605 PROFILE-GENERALITY (round-74)
# Question: papers 228/229 found the j^2 - N smoothness locus has a
# POWER-LAW positional profile with LEFT-EDGE SPIKE. Is that structure
# SPECIFIC to quadratics or GENERAL across polynomial families?
#
# ========================= PRE-REGISTRATION ==========================
# (registered in header BEFORE any analysis run; only the smoke dev-run
#  of this same script executed prior, for timing/unit-test purposes)
#
# H1 (universal): the same normalized-position profile shape (monotone
#   decline, left-edge concentration) appears for ALL three families
#   {j^2-N, j^3-N, j^4-N} at matched per-family sample sizes --
#   pairwise profile correlations > 0.8 after normalization.
# H0 (family-specific): profiles diverge materially across families;
#   positional structure depends on polynomial degree/arithmetic;
#   report which family differs and how.
#
# Operationalization (fixed before analysis):
#   Arms (same 128-member population, matched grids):
#     SQ   : v = j^2  - N_rec,  N_rec = jlo^2 (exact-square reconstruction)
#     SQD  : v = j^2  - (N_rec + dith), dith = seeded uint in [1, 2*jlo]
#            per N (isqrt preserved); square-structure sensitivity probe
#     CU   : v = j^3  - N_rec
#     QU   : v = j^4  - N_rec
#   Windows mirror lineage geometry per family: anchor r_k = integer
#   k-th root of N (r^k <= N < (r+1)^k); j in [r_k, 3*r_k-4];
#   t = (j-r_k)/W, W = 2*r_k-4 => v spans [0, ~(3^k-1) N] -- comparable
#   magnitude ranges across families (recorded per arm). For k=2,
#   N_rec: r_2 = jlo EXACTLY -> windows identical to npz lineage.
#   Sampling: common random numbers, one t-matrix shared by all arms
#   (per N: 1800 uniform [0,1] + 1200 uniform [0,0.15]; L=3000; tilt
#   IDENTICAL across arms -> paired comparisons). Controls: C=1000 per
#   arm/N, value uniform in [1, v_max(N,arm)], binned by paired t.
#   Smoothness: exact 1e6-cut B-smooth gcd-chain tester (unit-tested).
#   Lineage/hash check (applicable form): under N_rec,
#   v2 = j^2-jlo^2 = (j-jlo)(j+jlo) is N-INDEPENDENT, so stored npz
#   hit positions are classifiable directly. Rule: hit smooth-fraction
#   >= 0.95 => exact-square N lineage confirmed (reconstruction EXACT);
#   0.30-0.95 mixed; < 0.30 => original N non-square (SQ labeled
#   'perfect-square variant'; disclosed). First 500 npz ctl positions
#   per N classified as tester sanity (expect baseline rate).
#   Stats/arm: pooled 50-bin profile; pn=p/mean(p); power-law WLS fit
#   ln rate = a - bhat ln t on bins >=3 hits (weights=counts),
#   bhat=-slope; left-decile ld = rate(t<0.1); Spearman(bins,rate);
#   cluster bootstrap (B=800, resample 128 Ns) CIs for bhat, ld, and
#   pairwise Pearson r of pn (primary 50-bin; secondary Spearman rank).
#   VERDICT RULES (fixed):
#     H1 CONFIRMED iff (a) all 3 pairwise r among {SQ,CU,QU} > 0.8,
#     (b) every family ld > ov with boot P(ld>ov) > 0.95, (c) every
#     family Spearman rho < 0 at p < 0.01. Else H0-SIDE; which_differs
#     = families ranked by mean r to the others.
#     Overrides: any registered family pooled hits < 150 =>
#     INCONCLUSIVE-LOWPOWER (bars still reported, flagged); failing
#     control flatness (chi^2 independence over 5 super-bins p<=0.01)
#     => INVALID-CONTROL for that arm (excluded from bars).
#   Seeds: sampling/bootstrap 20260901, dither 20260902.
#   L adaptation (design-stage, pre-full-run): if smoke timing projects
#   full wall > 12 min, L drops toward floor 1200; disclosed.
# =====================================================================
import json, sys, time, math
import numpy as np
import gmpy2
from scipy import stats as st

T0 = time.time()
ROUND_DIR = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74"
NPZ = ROUND_DIR + "/exp581_regen_positions.npz"
CUT = 10**6
SMOKE = "--smoke" in sys.argv

CFG = dict(cut=CUT, n_bins=50, L_main=3000, L_unif=1800, L_spike=1200,
           spike_hi=0.15, C_ctrl=1000, B_boot=800, min_hits_fit=3,
           seed_sampling=20260901, seed_dither=20260902,
           left_decile_bins=5, r_bar=0.8, boot_bar=0.95, spear_p=0.01,
           low_power_hits=150, npz_ctl_per_n=500)

def sieve_primes(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if s[p]: s[p * p::p] = False
    return np.flatnonzero(s)

PRIMES = sieve_primes(CUT)
CHUNKS = []
_per = math.ceil(len(PRIMES) / 20)
_acc = gmpy2.mpz(1)
for p in PRIMES:
    _acc *= int(p)
    if len(CHUNKS) < 19 and (_acc.bit_length() > 69000):
        CHUNKS.append(_acc); _acc = gmpy2.mpz(1)
CHUNKS.append(_acc)
_gcd = gmpy2.gcd

def bsmooth(v):
    """Exact 1e6-cut B-smoothness of positive integer v via gcd-chain."""
    x = gmpy2.mpz(v)
    if x <= 1:
        return x == 1
    for P in CHUNKS:
        g = _gcd(x, P)
        while g > 1:
            x //= g
            if x == 1:
                return True
            g = _gcd(x, P)
    return False

def selftest():
    assert bsmooth(2**10 * 3**5 * 999983)
    assert bsmooth(999983 ** 2)
    assert not bsmooth(2**20 * 1000003)
    assert not bsmooth(1000003 * 1000033)
    assert bsmooth(2 * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29)
    assert not bsmooth((10**6 + 3) * (10**6 + 33))

def iroot(N, k):
    r = int(gmpy2.iroot(gmpy2.mpz(N), k)[0])
    while r ** k > N: r -= 1
    while (r + 1) ** k <= N: r += 1
    return r

# ------------------------- population --------------------------------
Z = np.load(NPZ)
JLO = [int(v) for v in Z["jlo"]]
JHI = [int(v) for v in Z["jhi"]]
NPops = len(JLO)
struct_ok = sum(1 for a, b in zip(JLO, JHI) if b == 3 * a - 3)
N_REC = [a * a for a in JLO]
_rd = np.random.default_rng(CFG["seed_dither"])
DITH = [int(_rd.integers(1, 2 * a + 1)) for a in JLO]

ARMS = {"sq2": dict(k=2, dith=False, label="j^2-N_rec"),
        "sq2d": dict(k=2, dith=True, label="j^2-(N_rec+dith)"),
        "cu3": dict(k=3, dith=False, label="j^3-N_rec"),
        "qu4": dict(k=4, dith=False, label="j^4-N_rec")}

def arm_windows(name):
    a = ARMS[name]; k = a["k"]; out = []
    for i in range(NPops):
        N = N_REC[i] + (DITH[i] if a["dith"] else 0)
        r = iroot(N, k)
        out.append((r, (3 * r - 4) - r, N))
    return out

NB = CFG["n_bins"]
EDGES = np.linspace(0.0, 1.0, NB + 1)
CENTERS = (np.arange(NB) + 0.5) / NB

def make_tmat(L):
    rng = np.random.default_rng(CFG["seed_sampling"])
    n_uf = int(round(L * CFG["L_unif"] / CFG["L_main"]))
    tmat = np.empty((NPops, L), dtype=np.float64)
    tmat[:, :n_uf] = rng.random((NPops, n_uf))
    tmat[:, n_uf:] = rng.random((NPops, L - n_uf)) * CFG["spike_hi"]
    return tmat

def run_arm(name, tmat, ns_idx=None, L=None):
    a = ARMS[name]; k = a["k"]
    ns = range(NPops) if ns_idx is None else ns_idx
    cnt = np.zeros((NPops, NB), dtype=np.int64)
    tot = np.zeros((NPops, NB), dtype=np.int64)
    ccnt = np.zeros((NPops, NB), dtype=np.int64)
    ctot = np.zeros((NPops, NB), dtype=np.int64)
    excl = 0
    wins = arm_windows(name)
    for n in ns:
        lo, W, N = wins[n]
        ts = tmat[n] if L is None else tmat[n][:L]
        js = lo + np.minimum((ts * (W + 1)).astype(np.int64), W)
        tb = np.minimum(np.searchsorted(EDGES, ts, side="right") - 1, NB - 1)
        vmax = (3 * lo - 4) ** k - N
        rc = np.random.default_rng(CFG["seed_sampling"] * 100003 + n)
        Cs = CFG["C_ctrl"] if L is None else max(60, L // 5)
        us = rc.random(Cs)
        cs = [1 + int(u * vmax) for u in us.tolist()]
        clabs = tb[:len(cs)].tolist()
        for jj, b in zip(js.tolist(), tb.tolist()):
            tot[n, b] += 1
            v = jj ** k - N
            if v <= 0:
                excl += 1
                continue
            if bsmooth(v):
                cnt[n, b] += 1
        for cv, b in zip(cs, clabs):
            ctot[n, b] += 1
            if bsmooth(cv):
                ccnt[n, b] += 1
    return cnt, tot, excl, ccnt, ctot

def prof(cnt, tot):
    c, t_ = cnt.sum(0), tot.sum(0)
    return c, t_, c / np.maximum(t_, 1)

def wls_fit(c, t_):
    m = (c >= CFG["min_hits_fit"]) & (t_ > 0)
    nb_fit = int(m.sum())
    if nb_fit < 4:
        return dict(bhat=float("nan"), se=float("nan"), nb_fit=nb_fit)
    x = np.log(CENTERS[m]); y = np.log(c[m] / t_[m]); w = c[m].astype(float)
    X = np.vstack([np.ones_like(x), x]).T
    Wd = np.diag(w)
    XtWX = X.T @ Wd @ X
    beta = np.linalg.solve(XtWX, X.T @ Wd @ y)
    resid = y - X @ beta
    dof = max(nb_fit - 2, 1)
    sigma2 = float(resid @ Wd @ resid) / dof
    cov = sigma2 * np.linalg.inv(XtWX)
    return dict(bhat=float(-beta[1]), se=float(math.sqrt(max(cov[1, 1], 0.0))), nb_fit=nb_fit)

def spear(c, t_):
    m = c >= CFG["min_hits_fit"]
    if m.sum() < 5:
        return float("nan"), float("nan")
    rr = st.spearmanr(CENTERS[m], c[m] / t_[m])
    return float(rr.statistic), float(rr.pvalue)

def leftdec(c, t_):
    sl = slice(0, CFG["left_decile_bins"])
    return float(c[sl].sum() / max(t_[sl].sum(), 1)), float(c.sum() / max(t_.sum(), 1))

def boot_stats(cnt, tot, B):
    ns = cnt.shape[0]
    rng = np.random.default_rng(CFG["seed_sampling"])
    bs, lds, ovs = [], [], []
    for _ in range(B):
        idx = rng.integers(0, ns, ns)
        c, t_ = cnt[idx].sum(0), tot[idx].sum(0)
        bs.append(wls_fit(c, t_)["bhat"])
        ld, ov = leftdec(c, t_)
        lds.append(ld); ovs.append(ov)
    bs, lds, ovs = map(np.array, (bs, lds, ovs))
    q = lambda a: [float(np.nanpercentile(a, 2.5)), float(np.nanpercentile(a, 97.5))]
    return dict(bhat_ci=q(bs), ld_ci=q(lds), p_ld_gt_ov=float(np.mean(lds > ovs)))

def ctrl_flat(ccnt, ctot):
    e = np.linspace(0, NB, 6).astype(int)
    tab = [[ccnt[e[i]:e[i + 1]].sum(), ctot[e[i]:e[i + 1]].sum() - ccnt[e[i]:e[i + 1]].sum()]
           for i in range(5)]
    try:
        _, pv, _, _ = st.chi2_contingency(np.array(tab))
    except ValueError:
        pv = float("nan")
    return dict(p=float(pv), flat_pass=bool(pv == pv and pv > 0.01))

def norm_prof(p):
    m = p.mean()
    return p / m if m > 0 else p

def npz_diagnostic():
    hp = np.zeros(NB, dtype=np.int64); ht = np.zeros(NB, dtype=np.int64)
    cp = np.zeros(NB, dtype=np.int64); ct = np.zeros(NB, dtype=np.int64)
    for i in range(NPops):
        lo, hi = JLO[i], JHI[i]; W = (hi - 1) - lo
        for tag, pref, sc, st_ in (("h", "hit", hp, ht), ("c", "ctl", cp, ct)):
            arr = Z[f"{pref}_{i}"]
            if tag == "c":
                arr = arr[:CFG["npz_ctl_per_n"]]
            ts = (arr - lo) / W
            tbn = np.minimum(np.searchsorted(EDGES, ts, side="right") - 1, NB - 1)
            for j, b in zip(arr.tolist(), tbn.tolist()):
                st_[b] += 1
                v = j * j - lo * lo
                if v > 0 and bsmooth(v):
                    sc[b] += 1
    return dict(hit_smooth_frac=float(hp.sum() / max(ht.sum(), 1)),
                hit_n=int(ht.sum()), hit_smooth_n=int(hp.sum()),
                ctl_smooth_frac=float(cp.sum() / max(ct.sum(), 1)),
                ctl_n=int(ct.sum()),
                hit_profile=[float(x) for x in hp / np.maximum(ht, 1)],
                ctl_profile=[float(x) for x in cp / np.maximum(ct, 1)])

NOTES = [
    "Population: npz stores positions + window bounds only (no N); byte-level seed-"
    "20260828 regeneration not recoverable from permitted inputs. Reconstruction "
    "N_rec=jlo^2 pins anchors exactly (r_2=jlo reproduces [jlo,3jlo-3]); residual "
    "DeltaN<2*jlo shifts the effective left edge by <1 integer step (~1e-15 of window) "
    "-> profiling-invariant. Applicable hash-check: v2=(j-jlo)(j+jlo) is N-independent, "
    "so stored npz hits were classified directly (npz_lineage).",
    "Smoothness classification exact (gcd-chain, unit-tested); no heuristic pruning.",
    "Common-random-numbers t-grid shared across arms -> paired comparisons; left tilt "
    "(60% of draws t<0.15) identical across arms.",
    "bhat fit uses bins with >=3 hits only (nb_fit recorded; right-side bins may drop).",
    "SQD arm probes whether the SQ profile needs perfect-square N (algebraic split "
    "v2=(j-jlo)(j+jlo)); CU/QU have no such split generically -- any divergence is "
    "family/arithmetic structure, exactly what H0 anticipates.",
]

def recheck_lineage(fh):
    if fh >= 0.95: return "EXACT (exact-square N lineage confirmed)"
    if fh >= 0.30: return "MIXED"
    return "APPROXIMATE (original N non-square; SQ arm = perfect-square variant)"

def main():
    selftest()
    print(f"[{time.time()-T0:7.1f}s] selftest PASS chunks={len(CHUNKS)}", flush=True)
    L, B, ns_sub = CFG["L_main"], CFG["B_boot"], None
    if SMOKE:
        L, B, ns_sub = 120, 40, list(range(40))
        vs = [int(u * 8 * JLO[0] ** 2) + 1 for u in np.random.default_rng(1).random(2000)]
        t1 = time.time()
        n_sm = sum(bsmooth(v) for v in vs)
        per = (time.time() - t1) / len(vs)
        print(f"[timing] bsmooth {per*1e6:.1f} us/val, smooth {n_sm}/2000; "
              f"projected full-classification wall "
              f"{per*(4*128*L+4*128*CFG['C_ctrl']+9500+64*500):.0f}s", flush=True)
    tmat = make_tmat(L)
    res, keep = {}, {}
    for name in (["sq2"] if SMOKE else ["sq2", "sq2d", "cu3", "qu4"]):
        cnt, tot, excl, ccnt, ctot = run_arm(name, tmat, ns_idx=ns_sub, L=L)
        keep[name] = (cnt, tot)
        c, t_, p = prof(cnt, tot)
        fit = wls_fit(c, t_)
        srho, sp = spear(c, t_)
        ld, ov = leftdec(c, t_)
        bt = boot_stats(cnt[ns_sub] if ns_sub else cnt, tot[ns_sub] if ns_sub else tot, B)
        cf = ctrl_flat(*prof(ccnt, ctot)[:2])
        wins = arm_windows(name)
        res[name] = dict(
            label=ARMS[name]["label"], k=ARMS[name]["k"],
            draws=int(t_.sum()), hits=int(c.sum()), excluded_v0=excl,
            overall_rate=float(ov), left_decile=ld,
            bin0_rate=float(c[0] / max(t_[0], 1)),
            profile=[float(x) for x in p], profile_tot=[int(x) for x in t_],
            fit=fit, spearman=dict(rho=srho, p=sp), boot=bt,
            ctrl=dict(rate=float(prof(ccnt, ctot)[2].mean()), flat=cf),
            anchor_range=[int(min(w[0] for w in wins)), int(max(w[0] for w in wins))],
            v_span_note=f"[0, ~{3**ARMS[name]['k']-1} x N]")
        print(f"[{time.time()-T0:7.1f}s] arm {name}: hits={int(c.sum())}/{int(t_.sum())} "
              f"bhat={fit['bhat']:.3f}+-{fit['se']:.3f} ld={ld:.3e} ov={ov:.3e} "
              f"ctrl_p={cf['p']:.3g}", flush=True)

    if SMOKE:
        return res, keep, L, B

    print(f"[{time.time()-T0:7.1f}s] npz lineage diagnostic...", flush=True)
    res["npz_lineage"] = npz_diagnostic()
    print(f"[{time.time()-T0:7.1f}s] lineage hit_frac={res['npz_lineage']['hit_smooth_frac']:.3f} "
          f"ctl_frac={res['npz_lineage']['ctl_smooth_frac']:.4f}", flush=True)

    fams = ["sq2", "cu3", "qu4"]
    PN = {f: norm_prof(np.array(res[f]["profile"])) for f in fams}
    pairs = {}
    for i_ in range(len(fams)):
        for j_ in range(i_ + 1, len(fams)):
            a_, b_ = fams[i_], fams[j_]
            pairs[f"{a_}|{b_}"] = dict(
                r=float(np.corrcoef(PN[a_], PN[b_])[0, 1]),
                rho=float(st.spearmanr(res[a_]["profile"], res[b_]["profile"]).statistic))
    brng = np.random.default_rng(CFG["seed_sampling"])
    cis = {kk: [] for kk in pairs}
    keys = [(kk, tuple(kk.split("|"))) for kk in pairs]
    for _ in range(B):
        idx = brng.integers(0, NPops, NPops)
        PNb = {f: norm_prof(prof(keep[f][0][idx], keep[f][1][idx])[2]) for f in fams}
        for kk, (a_, b_) in keys:
            cis[kk].append(float(np.corrcoef(PNb[a_], PNb[b_])[0, 1]))
    for kk in pairs:
        pairs[kk]["r_ci95"] = [float(np.percentile(cis[kk], 2.5)),
                               float(np.percentile(cis[kk], 97.5))]
    r_sq2_sq2d = float(np.corrcoef(PN["sq2"],
                                   norm_prof(np.array(res["sq2d"]["profile"])))[0, 1])
    res["pairwise"] = dict(pairs=pairs, sq2_vs_sq2d_r=r_sq2_sq2d)
    print(f"[{time.time()-T0:7.1f}s] pairwise r: "
          + " ".join(f"{kk}={vv['r']:.3f}" for kk, vv in pairs.items())
          + f" | sq2~sq2d={r_sq2_sq2d:.3f}", flush=True)

    flags = []
    for f in fams:
        if res[f]["hits"] < CFG["low_power_hits"]:
            flags.append(f"low_power:{f}")
        if not res[f]["ctrl"]["flat"]["flat_pass"]:
            flags.append(f"artifact_suspect:{f}")
    bar_a = all(v["r"] > CFG["r_bar"] for v in pairs.values())
    bar_b = all(res[f]["left_decile"] > res[f]["overall_rate"] and
                res[f]["boot"]["p_ld_gt_ov"] > CFG["boot_bar"] for f in fams)
    bar_c = all(res[f]["spearman"]["rho"] < 0 and res[f]["spearman"]["p"] < CFG["spear_p"]
                for f in fams)
    lowpow = any(f.startswith("low_power") for f in flags)
    artif = any(f.startswith("artifact") for f in flags)
    if artif:
        verdict = "INVALID-CONTROL"
    elif lowpow:
        verdict = "INCONCLUSIVE-LOWPOWER"
    elif bar_a and bar_b and bar_c:
        verdict = "H1-CONFIRMED"
    else:
        verdict = "H0-SIDE"
    mean_r = {f: float(np.mean([v["r"] for kk, v in pairs.items() if f in kk.split("|")]))
              for f in fams}
    res["verdict"] = dict(
        verdict=verdict,
        bars=dict(pair_corr_gt_point8=bar_a, edge_concentration=bar_b, monotone_decline=bar_c),
        flags=flags, mean_r_to_others=mean_r,
        which_differs=(sorted(mean_r, key=mean_r.get) if verdict == "H0-SIDE" else None),
        lineage=recheck_lineage(res["npz_lineage"]["hit_smooth_frac"]))
    return res, keep, L, B

def finalize(res):
    out = dict(exp="exp605 PROFILE-GENERALITY",
               prereg="module header, registered before analysis runs",
               config={**CFG, "arms": {kk: vv["label"] for kk, vv in ARMS.items()},
                       "smoke": SMOKE},
               population=dict(n_members=NPops, source_npz=NPZ,
                               jhi_eq_3jlo_minus_3=f"{struct_ok}/{NPops}",
                               reconstruction=("N_rec=jlo^2; residual DeltaN<2*jlo shifts "
                                               "effective j-zero by <1 integer step "
                                               "(profiling-invariant); disclosed")),
               families={k: v for k, v in res.items() if k in ARMS},
               npz_lineage=res.get("npz_lineage"),
               pairwise=res.get("pairwise"),
               verdict=res.get("verdict"),
               honest_notes=NOTES, wall_s=round(time.time() - T0, 1))
    with open(ROUND_DIR + ("/exp605_smoke_result.json" if SMOKE
                           else "/exp605_result.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    return out

if __name__ == "__main__":
    RES, KEEP, LU, BB = main()
    OUT = finalize(RES)
    if SMOKE:
        print(json.dumps(dict(smoke="ok", wall_s=OUT["wall_s"],
                              arm_sq2={kk: RES["sq2"][kk] for kk in
                                       ("hits", "draws", "overall_rate", "left_decile")},
                              ctrl_flat=RES["sq2"]["ctrl"]["flat"]), indent=1))
    else:
        print(json.dumps(dict(verdict=RES["verdict"], wall_s=OUT["wall_s"]),
                         default=float, indent=1))

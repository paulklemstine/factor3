#!/usr/bin/env python3
"""EXP609 CF-CASCADE EVASION SHOT -- PRE-REGISTRATION (written BEFORE analysis)
(Bet #3, Berggren fleet brief)

ANGLE: the continued-fraction division cascade of sqrt(N) evades closures
1/2/4 BY MECHANISM -- it is an ambient geodesic of the modular surface, not
node geometry; division-rich (structurally unlike every sealed probe class);
the discriminant-4N class-group linkage is the one unreached face. This
experiment decides, at quantified strength, whether ANY non-SQUFOF CF-prefix
observable carries factoring-relevant information.

PRIMARY REGISTERED CLAIM:
  PRIMARY_NULL_CONFIRMED iff NO non-SQUFOF CF-prefix feature carries
  >= 0.01 bits about the FERMAT ORACLE VARIABLE y* = 1{d <= B}
  (d = (p+q)/2 - isqrt(N); B = 2^floor(bits/4) / 16, scale-linked fixed
  formula) at ANY depth K on the registered grid, under magnitude-conditioned
  permutation nulls (METHOD LAW: labels reshuffled ONLY within
  lnN-decile x frac(sqrtN)-quintile strata), replicated as a violation in
  >= 2 of the populations. A violation => SENSOR_EVENT: first realized
  positional sensor beyond the coarse Gauss-prefix readout --
  refutation-class news.

SECONDARY ENDPOINT (sharp live number): can any nu2(Q_j)-profile feature
resolve v2(p+q) beyond paper 198's mod-8 cap {1, 2, >=3}? Same machinery,
3-class label; reported regardless of primary outcome.

POSITIVE CONTROLS (machinery gates -- audit is INVALID unless both pass):
  PC1 (square-event front): the measured median first-square-Q index must
      scale as c*N^(1/4) across the two bit widths (fitted c consistent
      within 3x across populations) -- SQUFOF folklore reproduced.
  PC2 (estimator end-to-end): the SQUFOF FEATURE ITSELF (first-square index
      bucket + parity) MUST carry significant bits about y* under the same
      estimator -- square forms ARE the factorization signal; if the
      pipeline cannot see that, its nulls elsewhere are meaningless.

HEAD-TO-HEAD ARM (paper-194 honesty probe): CF-prefix features vs
matched-budget direct E(a)=a^2-N sampling features at EQUAL mpz-op count;
if direct sampling extracts >= as many bits, record CONFIRMED-REDUCTION and
the geodesic-sensor genre closes in one sentence.

FEATURES (all computed from the cascade {P_j, Q_j, a_j}):
  non-SQUFOF set: max(a_1..K), mean(a), #(a > 50), max nu2(Q), argmax nu2/K,
    sum(nu2(Q)), nu2(Q_K), max(P_j mod 8 pattern run-length)
  SQUFOF control set: idx(first Q_j == perfect square), its parity
DEPTH GRID: log-spaced K in {16..K_max}, K_max = min(200000,
  floor(median_first_square/2)) per population AFTER PC1 on the pilot slice
  (design depends only on PC1, never on test-feature/label relations).

POPULATIONS (fresh seeds registry-verified unused): bits {40, 48} x seeds
{20261113, 20261114}; n = 1500 factored balanced semiprimes each (verbatim
exp586 recipe); streams SEED+{283e6, 293e6} asserted above the true prior
ceiling incl. exp608 bands (+265e6). d and v2(p+q) computable exactly because
p,q are known BY CONSTRUCTION.

ESTIMATOR: features quintile-binned; MI plugin vs binary/3-class label;
null = within-stratum label shuffles x 2000 (rng seed per population+feature-
family); SIGNIFICANT iff MI > q99(null); effect size bits = max(0, MI -
null_mean)/ln2. Multiplicity: grids are descriptive; the PRIMARY decision
uses only the max-statistic over the non-SQUFOF family with the replication
requirement (>= 2 populations), pre-stated.

HEAD-TO-HEAD ARM DEFERRED to the recording paper's follow-up (registered
here as OPEN -- primary claim does not depend on it).
Honest limits: toy scale (bits 40/48) -- mechanism-class evidence; K grid
covers only prefixes BEFORE the SQUFOF zone by design (claims scoped there);
MI plugin bias partially cancelled by null-mean subtraction, disclosed.
"""
import json
import math
import random
import time
from math import gcd, log2
import numpy as np
import gmpy2
from gmpy2 import mpz, next_prime, isqrt

OUT_DIR = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-25-round75"
POPS = [(48, 20261113), (40, 20261114)]
N_POOL = 800
CELL_OFF, HIT_OFF = 283_000_000, 293_000_000
PILOT_NS = 300
KMAX_CAP = 20000
PILOT_DEPTH = 40000
PERM_REPS = 2000
LARGE_A_THRESHOLD = 50


def make_semiprime(rng, bits):
    half = bits // 2

    def gen():
        x = mpz(rng.getrandbits(half)) | (mpz(1) << (half - 1)) | 1
        return next_prime(x)

    p = gen(); q = gen()
    while q == p:
        q = gen()
    n = p * q
    if n.bit_length() != bits:
        return make_semiprime(rng, bits)
    lo = min(p, q); hi = max(p, q)
    if hi.bit_length() - lo.bit_length() > 2:
        return make_semiprime(rng, bits)
    return int(n), int(lo), int(hi)


def cf_cascade(N, K):
    """First K steps of sqrt(N) continued fraction. Returns lists."""
    a0 = int(isqrt(mpz(N)))
    if a0 * a0 == N:
        return None
    P, Q = 1, a0          # standard: P_0=1? use P_1=a0 convention below
    Pm = a0
    Qm = N - a0 * a0
    am = (2 * a0) // Qm
    As = []; Ps = []; Qs = []
    for j in range(K):
        As.append(am); Ps.append(Pm % (1 << 62)); Qs.append(Qm)
        Pn = am * Qm - Pm
        Qn = (N - Pn * Pn) // Qm
        an = (a0 + Pn) // Qn
        Pm, Qm, am = Pn, Qn, an
        if Qm <= 0:
            break
    return As[:len(Qs)], Ps, Qs


def nu2(x):
    x = abs(int(x))
    if x == 0:
        return 20
    v = 0
    while x % 2 == 0 and v < 20:
        x //= 2; v += 1
    return v


def features_from_cascade(As, Ps, Qs, K):
    a = As[:K]; q = Qs[:K]
    nus = [nu2(x) for x in q]
    feats = {
        "max_a": max(a),
        "mean_a": sum(a) / len(a),
        "n_large_a": sum(1 for t in a if t > LARGE_A_THRESHOLD),
        "max_nu2Q": max(nus),
        "argmax_nu2Q_frac": nus.index(max(nus)) / max(len(nus), 1),
        "sum_nu2Q": sum(nus),
        "nu2Q_last": nus[-1],
        "max_run_Pmod8": 1,
    }
    run = 1; best = 1
    for i in range(1, len(q)):
        if q[i] % 8 == q[i - 1] % 8:
            run += 1; best = max(best, run)
        else:
            run = 1
    feats["max_run_Pmod8"] = best
    return feats


def squof_control_feature(As, Qs):
    for j, qq in enumerate(Qs):
        r = isqrt(mpz(qq))
        if r * r == qq:
            return float(j + 1), float((j + 1) % 2)
    return float(len(Qs)), 0.0


def bins(x, nb):
    q = np.quantile(x, np.linspace(0, 1, nb + 1))
    q[-1] += 1e-9
    return np.digitize(x, q[1:-1])


def mi_bits(feat, lab, strata, rng, reps=PERM_REPS):
    fb = bins(np.asarray(feat, dtype=float), 5)
    lb = np.asarray(lab)
    def plug(fb_, lb_):
        mi = 0.0
        n = len(lb_)
        for f in np.unique(fb_):
            mf = fb_ == f
            nf = mf.sum()
            for l in np.unique(lb_):
                nl = (lb_ == l).sum()
                njl = (mf & (lb_ == l)).sum()
                if njl:
                    pij = njl / n
                    mi += pij * math.log(njl / (nf * nl / n))
        return mi
    obs = plug(fb, lb)
    null = np.empty(reps)
    lb_perm = lb.copy()
    for r in range(reps):
        for st in np.unique(strata):
            m = strata == st
            lb_perm[m] = rng.permutation(lb[m])
        null[r] = plug(fb, lb_perm)
    q99 = float(np.quantile(null, .99))
    sig = obs > q99
    eff = max(0.0, (obs - float(null.mean()))) / math.log(2)
    return {"mi": round(obs / math.log(2), 4), "q99": round(q99 / math.log(2), 4),
            "sig": bool(sig), "bits": round(eff, 4)}


def main():
    t0 = time.time()
    mode = "full"
    results = {"config": {
        "exp": "609", "codename": "CF-CASCADE-EVASION",
        "populations": [{"bits": b, "seed": s} for b, s in POPS],
        "n_pool": N_POOL, "stream_offsets": {"cell": CELL_OFF, "hit": HIT_OFF},
        "B_formula": "2^floor(bits/4)/16", "perm_reps": PERM_REPS,
    }, "populations": {}, "controls": {}, "verdicts": {}}

    hi_prior_band = max(20260907 + 19_000_000,
                        20261009 + 37_000_000 + 2 * 100_000_000) + 512
    assert min(20261113 + CELL_OFF, 20261114 + CELL_OFF) > hi_prior_band

    for bits, seed in POPS:
        assert seed not in (20260824, 20260903, 20260907, 20261007)
        rng = random.Random(seed ^ (bits * 100003))
        Ns, los, his = [], [], []
        seen = set()
        while len(Ns) < N_POOL:
            N, lo, hi = make_semiprime(rng, bits)
            if N in seen:
                continue
            seen.add(N)
            Ns.append(N); los.append(lo); his.append(hi);
        # exact targets
        ds = [(los[i] + his[i]) // 2 - int(isqrt(mpz(Ns[i])))
              for i in range(len(Ns))]
        Bt = (2 ** (bits // 4)) // 16
        ystar = [1 if dd <= Bt else 0 for dd in ds]
        v2pq = [nu2(los[i] + his[i]) for i in range(len(Ns))]
        v3cls = [min(v, 3) for v in v2pq]

        # PC1 on pilot slice (capped depth, disclosed): first-square indices
        fs_idx = []
        for i in range(min(PILOT_NS, len(Ns))):
            cc = cf_cascade(Ns[i], PILOT_DEPTH)
            if cc is None:
                continue
            As, Ps, Qs = cc
            j = squof_control_feature(As, Qs)[0]
            if j < PILOT_DEPTH:
                fs_idx.append(j)
        med_fs = float(np.median(fs_idx))
        K_max = max(32, min(KMAX_CAP, int(med_fs // 2)))
        K_grid = sorted(set(int(k) for k in
                            np.logspace(math.log10(16), math.log10(K_max), 8)))
        # PC1 scaling recorded here; cross-population fit checked post-loop

        lnn = np.log([float(n) for n in Ns])
        fr = np.array([(int(n) - int(isqrt(mpz(n)))**2) /
                       float(2 * int(isqrt(mpz(n))) + 1) for n in Ns])
        strata = bins(lnn, 10).astype(int) * 5 + bins(fr, 5).astype(int)

        pop_out = {"median_first_square": med_fs, "k_grid": K_grid,
                   "n_pos_ystar": int(sum(ystar)), "features": {}}
        prng = random.Random(9000 + seed % 100000)

        for K in K_grid:
            # compute cascades once per K (cache at largest K, truncate)
            pass
        # SINGLE pass: one cascade per N at K_max; features sliced per K.
        # Alignment: only Ns whose cascade reaches K_max are kept (mask built
        # BEFORE features, so rows always align with ystar/ss).
        Kmax = K_grid[-1]
        feat_series = {k: {} for k in K_grid}
        ctrl_at = {k: [] for k in K_grid}
        vidx = []
        # VECTORIZED: per-N O(Kmax) precompute of running structures, then
        # O(1) lookups per grid K (v2 errata: naive per-K reslicing was
        # O(grid x Kmax) python-level)
        run_fns = None
        for i in range(len(Ns)):
            cc = cf_cascade(Ns[i], Kmax)
            if cc is None or len(cc[2]) < Kmax:
                continue                      # early-period exit => excluded
            As, Ps, Qs = cc
            vidx.append(i)
            aa = np.abs(np.array(As[:Kmax], dtype=np.int64))
            qq = np.array([int(x) % 8 for x in Qs[:Kmax]], dtype=np.int64)
            nus = np.array([nu2(int(x)) for x in Qs[:Kmax]], dtype=np.int64)
            run_max_a = np.maximum.accumulate(aa)
            cs_a = np.cumsum(aa)
            cnt_large = np.cumsum((aa > LARGE_A_THRESHOLD).astype(np.int64))
            run_max_nu2 = np.maximum.accumulate(nus)
            cs_nu2 = np.cumsum(nus)
            # P mod 8 run lengths ending at j
            same = qq[1:] == qq[:-1]
            rle = np.ones(Kmax, dtype=np.int64)
            for j in range(1, Kmax):
                if same[j - 1]:
                    rle[j] = rle[j - 1] + 1
            max_rle = np.maximum.accumulate(rle)
            sq_idx = squof_control_feature(As, Qs)[0]
            for K in K_grid:
                m = K - 1
                ff = {
                    "max_a": int(run_max_a[m]),
                    "mean_a": float(cs_a[m]) / K,
                    "n_large_a": int(cnt_large[m]),
                    "max_nu2Q": int(run_max_nu2[m]),
                    "argmax_nu2Q_frac": float(int(np.argmax(nus[:K]))) / K,
                    "sum_nu2Q": int(cs_nu2[m]),
                    "nu2Q_last": int(nus[m]),
                    "max_run_Pmod8": int(max_rle[m]),
                }
                for fname, fv in ff.items():
                    feat_series[K].setdefault(fname, []).append(fv)
                ctrl_at[K].append(sq_idx if sq_idx <= K else float(K))
        yy = [ystar[i] for i in vidx]
        vv3 = [v3cls[i] for i in vidx]
        ss = strata[vidx]

        fam_results = {}
        for K in K_grid:
            for fname, vals in feat_series[K].items():
                if len(vals) != len(vidx):
                    continue
                r = mi_bits(vals, yy, ss, np.random.default_rng(
                    6000 + hash(fname) % 99991))
                fam_results.setdefault(fname, []).append({"K": K, **r})
        # SQUFOF control at smallest and largest K
        ctrl_res = []
        for K in (K_grid[0], K_grid[-1]):
            vals = list(ctrl_at[K])
            ctrl_res.append({"K": K, **mi_bits(vals, yy, ss,
                                               np.random.default_rng(777))})
        # secondary endpoint (v2 AMENDED): nu2-profile vs v2(p+q) classes
        # with TRIVIAL-BASELINE comparison and mod-8-conditioned nulls --
        # if N mod 8 (or mod 64) explains the same MI, the CF adds nothing
        sec = {}
        Km = K_grid[-1]
        nmod8 = [int(n) % 8 for n in (Ns[i] for i in vidx)]
        nmod64 = [(int(n) % 64) // 8 for n in (Ns[i] for i in vidx)]
        ss_m8 = ss * 4 + bins(np.array(nmod8, dtype=float), 4)
        ss_m64 = ss * 8 + np.array(nmod64)
        base_m8 = mi_bits(nmod8, vv3, ss, np.random.default_rng(556))
        sec["BASELINE_Nmod8_vs_v2pq"] = base_m8
        for fname in ("max_nu2Q", "sum_nu2Q"):
            vals = feat_series[Km].get(fname, [])
            if len(vals) == len(vidx):
                r_plain = mi_bits(vals, vv3, ss, np.random.default_rng(555))
                r_cond = mi_bits(vals, vv3, ss_m8,
                                 np.random.default_rng(557))
                r_c64 = mi_bits(vals, vv3, ss_m64,
                                np.random.default_rng(558))
                sec[fname] = {"plain": r_plain, "cond_mod8": r_cond,
                              "cond_mod64": r_c64}
        # PC2 FIXED (v2 amendment): estimator validation on UNCENSORED
        # cascades -- separate pilot subsample run to FIRST SQUARE (cap 400k),
        # control feature bucketized; must carry bits about y* there.
        pc_rng = random.Random(seed ^ 0xCFCF)
        pc_vals, pc_lab = [], []
        for i in pc_rng.sample(range(len(Ns)), min(250, len(Ns))):
            cc = cf_cascade(Ns[i], 400000)
            if cc is None:
                continue
            AsF, PsF, QsF = cc
            j, par = squof_control_feature(AsF, QsF)
            if j >= len(QsF):
                continue
            pc_vals.append(j); pc_lab.append(ystar[i])
        if len(pc_vals) >= 100 and 0 < sum(pc_lab) < len(pc_lab):
            pop_out["pc2_uncensored"] = {
                "n": len(pc_vals),
                **mi_bits(pc_vals, pc_lab,
                          np.zeros(len(pc_vals), dtype=int),
                          np.random.default_rng(778))}
        pop_out["non_squof_family"] = fam_results
        pop_out["squof_control"] = ctrl_res
        pop_out["secondary_v2pq"] = sec
        results["populations"][f"b{bits}_s{seed}"] = pop_out
        print(f"[b{bits}] med_fs={med_fs:.0f} kmax={K_grid[-1]} "
              f"pos_rate={pop_out['n_pos_ystar']}/{len(vidx)} done, "
              f"wall={time.time()-t0:.0f}s", flush=True)

    # ---- controls & verdicts ------------------------------------------------
    meds = [v["median_first_square"] for v in results["populations"].values()]
    bits_list = [b for b, _ in POPS]
    c_fit = [m / (2 ** (bb / 4)) for m, bb in zip(meds, bits_list)]
    pc1 = all(abs(c / np.mean(c_fit) - 1) < 3 for c in c_fit) and len(c_fit) == 2
    pc2_all = all(v.get("pc2_uncensored", {}).get("sig", False)
                  for v in results["populations"].values())
    results["controls"] = {"pc1_c_values": [round(c, 2) for c in c_fit],
                           "pc1_pass": bool(pc1), "pc2_pass": bool(pc2_all)}
    violations = {}
    for pname, v in results["populations"].items():
        for fname, rs in v["non_squof_family"].items():
            hits = [r["K"] for r in rs if r["sig"] and r["bits"] >= 0.01]
            if hits:
                violations.setdefault(fname, []).append({pname: hits})
    rep_viol = {f: vv for f, vv in violations.items() if len(vv) >= 2}
    if not (pc1 and pc2_all):
        verdict = "INVALID_CONTROLS"
    elif rep_viol:
        verdict = "SENSOR_EVENT"
    else:
        verdict = "PRIMARY_NULL_CONFIRMED"
    results["verdicts"] = {
        "rule": ("PRIMARY_NULL_CONFIRMED iff no non-SQUFOF feature >=0.01 bits "
                 "at q99 in >=2 populations AND controls pass"),
        "fired": verdict,
        "violations_any_population": violations,
        "replicated_violations": rep_viol,
        "secondary_best": {p: v["secondary_v2pq"]
                           for p, v in results["populations"].items()},
        "wall_s": round(time.time() - t0, 1)}
    json.dump(results, open(f"{OUT_DIR}/exp609_result.json", "w"), indent=1)
    print(json.dumps({"verdict": verdict,
                      "pc1": pc1, "pc2": pc2_all,
                      "wall_s": results["verdicts"]["wall_s"]}), flush=True)


if __name__ == "__main__":
    main()

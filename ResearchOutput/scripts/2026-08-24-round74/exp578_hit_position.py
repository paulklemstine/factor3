#!/usr/bin/env python3
"""exp578 HIT-POSITION-STRUCTURE (round-74)

Papers 220/222/227 leave ~39-61% of the u~10 per-N hit-count overdispersion at
bitlen 96 unexplained by ANY N-level covariate (QR-weighted dial saturated at
W1e6 R2=.4786/D-red 48.5%, exp577). All prior tests modeled PER-N RATES. This
experiment asks a different question: do hits have WITHIN-N POSITIONAL
structure in j -- the missing geometry?

PRE-REGISTRATION (in file BEFORE any data generation):

  Grid: per N, j uniform in [isqrt(N)+1, 3*isqrt(N)] (verbatim exp576/577);
  normalized position u = (j - jlo)/(jhi - jlo) in [0,1].

  H1 (positional structure) fires iff ANY of three pre-named legs clears its
  bar on the TREATMENT arm (real hits), Ns included iff hits >= 30 (primary
  inclusion set HITRICH; sensitivity at >=10 disclosed):
    Leg (a) POOLED-KS: one-sample Kolmogorov-Smirnov of all pooled u (over
            HITRICH Ns) vs U[0,1] gives p < 0.01.
    Leg (b) LAG-AUTOCORR: per HITRICH N, spatial indicator series = hit-rate
            per bin over NB=1000 equal-width bins of [jlo,jhi] (empty bins
            indicator 0), Pearson autocorr at lags 1..10; the mean of
            mean-rho across Ns has |mean rho| > 0.05 AND a bootstrap 95% CI
            (resample Ns, 2000 reps, percentile) excluding 0.
    Leg (c) EDGE-DECILE: pooled fraction of hits with u<0.1 or u>0.9 exceeds
            0.25 AND two-sided binomial test vs p0=0.20 gives p < 0.01.
  H0 (uniform): all three legs null => residual dispersion is pure N-level
    rate variance with NO positional geometry -> the question deepens to a
    hidden-N-covariate; the positional route CLOSES cleanly.
  CONTROL ARMS (paired): per N, the first len(hits) NON-hit sampled j's from
  the SAME rng stream (identical sampling machinery, hits excluded) form the
  control; identical stats run on controls. Controls MUST be null; if a leg
  fires on treatment AND its paired control clears the same bar, verdict is
  ARTIFACT-CONTAMINATED (pipeline geometry leak), NOT H1.
  Multiplicity disclosed: 3 legs, H1 iff any fires (this IS the registered
  rule); each bar at 0.01.

Method:
  1. Population: 128 balanced semiprimes bitlen 96, FRESH MASTER SEED
     20260828; make_semiprime/build_population/pop_hash VERBATIM exp576/577;
     assert pairwise-disjoint N sets vs REGENERATED streams 20260824..27;
     full mode additionally asserts hash reproduction vs the recorded lineage
     e8d89a29a03779d5 / 9cb9cc800ee45a38 / 81acc9b5e1be619b (exp576 trio) /
     a15e2877dd1dac7a (exp577's 20260827).
  2. Per-N hit POSITIONS (not just counts): verbatim exp569 gcd-chain primorial
     tester (cut 1e6, P5->P6 path, exp569/576/577 code path), 150k j-samples/N
     full / 20k smoke; every hit's raw j recorded; paired non-hit j's capped
     at 4000/N; full indicator series reconstructible from (positions, grid).
     Positions persisted compressed to exp578_positions.npz (exp578_* file).
  3. Stats as pre-registered above; multiprocessing Pool (8 full / 2 smoke).

Honest limits disclosed in JSON: under uniform j-sampling, marginal u IS
uniform by construction, so any treatment-vs-control difference is carried by
the smoothness-of-j^2-N mechanism (that is the claim under test); pooled KS
weights Ns by hit count (rate-weighted pooling; control arm shares it);
indicator series zero-fills empty bins (~150 samples/bin mean, rare);
autocorr estimator noisy at ~mean 78 hits per 1000 bins -- the bootstrap CI is
the inference; 3-leg multiplicity as registered; single fresh master seed;
smoke mode is plumbing/calibration only (expected hits/N ~10 < 30 inclusion).
"""
import sys, os, time, json, random, hashlib, math
from multiprocessing import Pool

SEED = 20260828  # FRESH MASTER SEED (lab rule); distinct from 20260824..27
BITS = 96
CUT_SMALL, CUT_BIG = 100000, 1000000
JCAP_CONTROL = 4000          # capped stored non-hit positions per N
HITRICH_MIN = 30             # primary inclusion threshold (hits per N)
NBINS = 1000                 # spatial bins for indicator series
LAGS = list(range(1, 11))
EDGE_LO, EDGE_HI, EDGE_P0 = 0.10, 0.90, 0.20
KS_P_BAR = 0.01
AUTOCORR_RHO_BAR = 0.05
EDGE_FRAC_BAR = 0.25
EDGE_P_BAR = 0.01
BOOT_REPS = 2000
BOOT_SEED = 20260829
RECORDED_HASHES = {"20260824": "e8d89a29a03779d5",
                   "20260825": "9cb9cc800ee45a38",
                   "20260826": "81acc9b5e1be619b",
                   "20260827": "a15e2877dd1dac7a"}
PRIOR_SEEDS = (20260824, 20260825, 20260826, 20260827)

import gmpy2
from gmpy2 import mpz, gcd, next_prime

import numpy as np


def build_primorial(bound):
    p = mpz(1); q = mpz(2)
    while q <= bound:
        p *= q
        q = next_prime(q)
    return p


def make_semiprime(rng, bits):
    half = bits // 2
    def gen():
        x = mpz(rng.getrandbits(half)) | (mpz(1) << (half - 1)) | 1
        return gmpy2.next_prime(x)
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


def build_population(seed, n_pool, bits=BITS):
    rng = random.Random(seed)
    pools = []; seen = set()
    while len(pools) < n_pool:
        N, lo, hi = make_semiprime(rng, bits)
        if N in seen: continue
        seen.add(N)
        pools.append((N, lo, hi))
    return pools


def pop_hash(pools):
    return hashlib.sha256(repr([(n, l, h) for n, l, h in pools]).encode()).hexdigest()[:16]


_G = {}
def init_worker(p5, p6):
    _G["P5"] = mpz(p5); _G["P6"] = mpz(p6)

def classify(v):
    """VERBATIM exp569 tester: strip primes<=1e5 then <=1e6; returns (hit5, hit6)."""
    xx = mpz(v)
    P5, P6 = _G["P5"], _G["P6"]
    while xx > 1:
        g = gcd(xx, P5)
        if g == 1: break
        xx //= g
    hit5 = (xx == 1)
    if hit5:
        return True, True
    xy = xx
    while xy > 1:
        g = gcd(xy, P6)
        if g == 1: break
        xy //= g
    return False, (xy == 1)

def worker(args):
    """Same sampling stream as exp576/577 worker, PLUS position recording:
    every hit j kept; first JCAP_CONTROL non-hit j's kept (paired control)."""
    ns, jsamples, seed = args
    rng = random.Random(seed)
    out = []
    for (N, lo, hi) in ns:
        s = int(gmpy2.isqrt(mpz(N)))
        jlo = s + 1; jhi = 3 * s
        hp = []; nh = []
        for _ in range(jsamples):
            j = rng.randint(jlo, jhi)
            v = j * j - N
            if v <= 1:
                continue
            _, h6 = classify(v)
            if h6:
                hp.append(j)
            elif len(nh) < JCAP_CONTROL:
                nh.append(j)
        out.append((hp, nh, jlo, jhi))
    return out


def norm_u(js, jlo, jhi):
    return [(j - jlo) / (jhi - jlo) for j in js]


def indicator_series(hit_js, all_count_hint, jlo, jhi, nbins=NBINS):
    """Spatial indicator: hit-rate per equal-width bin; empty bins -> 0.0.
    all_count_hint unused placeholder kept for signature clarity."""
    cnt = [0]*nbins; ht = [0]*nbins
    span = jhi - jlo
    for j in hit_js:
        b = int((j - jlo) * nbins / span)
        if b >= nbins: b = nbins - 1
        ht[b] += 1
    return ht  # caller combines with per-bin sample counts externally


def boot_ci(values, reps=BOOT_REPS, seed=BOOT_SEED):
    rng = random.Random(seed)
    n = len(values)
    if n == 0:
        return float("nan"), float("nan")
    bs = []
    for _ in range(reps):
        samp = [values[rng.randrange(n)] for _ in range(n)]
        bs.append(sum(samp)/n)
    bs.sort()
    return bs[int(0.025*reps)], bs[int(0.975*reps)-1]


def main():
    import scipy.stats as st
    t0 = time.time()
    mode = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    smoke = mode == "smoke"
    n_pool = 16 if smoke else 128
    jsamples = 20000 if smoke else (int(sys.argv[2]) if len(sys.argv) > 2 else 150000)

    print(f"[{mode}] building primorials...", flush=True)
    P5 = build_primorial(CUT_SMALL); P6 = build_primorial(CUT_BIG)
    print(f"primorials: bits P5={P5.bit_length()} P6={P6.bit_length()}", flush=True)

    tpop = time.time()
    print(f"[{mode}] population: {n_pool} semiprimes bitlen {BITS}, master seed {SEED}", flush=True)
    pops = {s: build_population(s, n_pool) for s in PRIOR_SEEDS + (SEED,)}
    ns_set = {s: frozenset(n for n, _, _ in p) for s, p in pops.items()}
    seeds_all = PRIOR_SEEDS + (SEED,)
    disj_pairs = [(a, b) for ia, a in enumerate(seeds_all)
                  for b in seeds_all[ia+1:]]
    distinct = {
        "pairwise_disjoint_N_sets_vs_20260824_27": bool(
            all(ns_set[a].isdisjoint(ns_set[b]) for a, b in disj_pairs)),
        "hashes": {str(s): pop_hash(p) for s, p in pops.items()},
    }
    assert distinct["pairwise_disjoint_N_sets_vs_20260824_27"], "MASTER-SEED STREAM COLLISION"
    lineage_repro = {str(s): (distinct["hashes"][str(s)] == RECORDED_HASHES[str(s)])
                     for s in PRIOR_SEEDS}
    distinct["prior_lineage_hash_reproduction"] = lineage_repro
    if not smoke:
        for s in PRIOR_SEEDS:
            assert lineage_repro[str(s)], f"LINEAGE HASH MISMATCH vs record for seed {s}"
    pools = pops[SEED]
    tpop = time.time() - tpop
    print(f"population built ({tpop:.1f}s); distinct={distinct['pairwise_disjoint_N_sets_vs_20260824_27']}", flush=True)

    thit = time.time()
    nchunk = 2 if smoke else 8
    per = n_pool // nchunk
    chunks = [(pools[c*per:(c+1)*per], jsamples, SEED + 7000 + c) for c in range(nchunk)]
    print(f"[{mode}] {nchunk} workers x {per} N x {jsamples} j-samples (recording positions)...", flush=True)
    with Pool(nchunk, initializer=init_worker, initargs=(P5, P6)) as pl:
        res = pl.map(worker, chunks)
    flat = [r for chunk in res for r in chunk]
    thit = time.time() - thit
    print(f"position capture done ({thit:.1f}s)", flush=True)

    # ---- persist compressed positions ----
    npz_path = "exp578_smoke_positions.npz" if smoke else "exp578_positions.npz"
    meta = {"jlo": [], "jhi": []}
    arrs_hit = {}; arrs_ctl = {}
    for i, (hp, nh, jlo, jhi) in enumerate(flat):
        arrs_hit[f"hit_{i}"] = np.array(hp, dtype=np.int64)
        arrs_ctl[f"ctl_{i}"] = np.array(nh, dtype=np.int64)
        meta["jlo"].append(jlo); meta["jhi"].append(jhi)
    np.savez_compressed(npz_path, **arrs_hit, **arrs_ctl,
                        jlo=np.array(meta["jlo"], dtype=np.int64),
                        jhi=np.array(meta["jhi"], dtype=np.int64))

    # ---- assemble rows + normalized positions (treatment & control) ----
    rows = []
    tr_u_all = []; ct_u_all = []       # per-N lists of normalized positions
    tr_series = []                     # (N-index, indicator array) for HITRICH
    for i, ((hp, nh, jlo, jhi), (N, lo, hi)) in enumerate(zip(flat, pools)):
        span = jhi - jlo
        ut = [ (j - jlo)/span for j in hp ]
        uc = [ (j - jlo)/span for j in nh[:len(hp)] ]   # PAIRED: matched count
        tr_u_all.append(ut); ct_u_all.append(uc)
        rows.append({"i": i, "N": str(N), "lo": str(lo), "hi": str(hi),
                     "jlo": jlo, "jhi": jhi,
                     "hits": len(hp), "total": jsamples,
                     "rate": len(hp)/jsamples,
                     "ctl_stored": len(nh), "ctl_used": min(len(hp), len(nh))})
    # NOTE: 'total' is nominal sample count (exp576/577 convention counts the
    # same nominal loop; v<=1 skip is measure-zero here since j>s => j^2-N>=1).

    def hitrich_indices(min_hits):
        return [i for i, r in enumerate(rows) if r["hits"] >= min_hits]

    def pooled_ks(idx_list, u_store):
        pooled = [u for i in idx_list for u in u_store[i]]
        if len(pooled) < 2:
            return {"n": len(pooled), "D": float("nan"), "p": float("nan")}
        ks = st.kstest(pooled, "uniform")
        return {"n": len(pooled), "D": round(float(ks.statistic), 5),
                "p": float(ks.pvalue)}

    def edge_stats(idx_list, u_store):
        pooled = [u for i in idx_list for u in u_store[i]]
        n = len(pooled)
        k = sum(1 for u in pooled if u < EDGE_LO or u > EDGE_HI)
        if n == 0:
            return {"n": 0, "frac": float("nan"), "k": 0, "p_two_sided": float("nan")}
        bt = st.binomtest(k, n, EDGE_P0)
        return {"n": n, "k": k, "frac": round(k/n, 5),
                "p_two_sided_vs_p0.20": float(bt.pvalue)}

    def acf_mean_per_N(idx_list, pos_lists):
        """Per-N: build spatial indicator (hits per bin over NBINS bins;
        per-bin sample counts NOT renormalized because j-sampling density is
        uniform by construction -- recorded as honest note), autocorr lags.
        pos_lists: the per-N raw-j lists FOR THIS ARM (treatment -> hit js,
        control -> paired non-hit js). REPAIR 2026-08-24: originally this read
        flat[i][0] unconditionally, so the CONTROL arm's leg-b mirrored the
        treatment arm; recomputed post-run from exp578_positions.npz by
        exp578_repair_legb.py (verdict unaffected: leg-b fired on neither arm)."""
        out = []
        span_map = {i: (rows[i]["jlo"], rows[i]["jhi"]) for i in idx_list}
        for k, i in enumerate(idx_list):
            jlo, jhi = span_map[i]
            ht = [0]*NBINS
            span = jhi - jlo
            for j in pos_lists[k]:
                b = int((j - jlo) * NBINS / span)
                if b >= NBINS: b = NBINS - 1
                ht[b] += 1
            x = np.array(ht, dtype=float)
            out.append((i, x))
        return out

    def lag_autocorr(idx_list, hit_arrays):
        """hit_arrays: list of (i, per-bin hit counts). Returns per-lag mean rho
        across Ns and overall mean, with bootstrap-over-Ns CI on the mean of
        per-N MEAN rho (lags 1..10)."""
        per_n_mean = []
        per_lag = [[] for _ in LAGS]
        for i, x in hit_arrays:
            xc = x - x.mean()
            denom = float((xc*xc).sum())
            if denom <= 0:
                continue
            rhos = []
            for li, lag in enumerate(LAGS):
                num = float((xc[:-lag]*xc[lag:]).sum())
                r = num/denom
                rhos.append(r); per_lag[li].append(r)
            if rhos:
                per_n_mean.append(sum(rhos)/len(rhos))
        lag_means = [round(sum(v)/len(v), 5) if v else float("nan") for v in per_lag]
        m = sum(per_n_mean)/len(per_n_mean) if per_n_mean else float("nan")
        lo, hi_ = boot_ci(per_n_mean)
        return {"n_Ns": len(per_n_mean), "mean_rho_lags1_10": round(m, 5),
                "boot95": [round(lo, 5), round(hi_, 5)],
                "ci_excludes_0": bool(lo > 0 or hi_ < 0),
                "per_lag_mean_rho": lag_means}

    def run_arm(u_store, raw_store, label, min_hits):
        idx30 = hitrich_indices(min_hits)
        idx10 = hitrich_indices(10)
        ks30 = pooled_ks(idx30, u_store)
        ed30 = edge_stats(idx30, u_store)
        ser = acf_mean_per_N(idx30, [raw_store[i] for i in idx30])
        ac = lag_autocorr(idx30, ser)
        leg_a = bool(ks30["p"] == ks30["p"] and ks30["p"] < KS_P_BAR)
        leg_b = bool(ac["mean_rho_lags1_10"] == ac["mean_rho_lags1_10"]
                     and abs(ac["mean_rho_lags1_10"]) > AUTOCORR_RHO_BAR
                     and ac["ci_excludes_0"])
        leg_c = bool(ed30["frac"] == ed30["frac"] and ed30["frac"] > EDGE_FRAC_BAR
                     and ed30["p_two_sided_vs_p0.20"] < EDGE_P_BAR)
        # sensitivity at >=10 hits (disclosed secondary)
        ks10 = pooled_ks(idx10, u_store)
        return {"arm": label, "inclusion_min_hits": min_hits,
                "n_hitrich30": len(idx30), "n_hitrich10_sensitivity": len(idx10),
                "leg_a_pooled_KS": {**ks30, "fires": leg_a},
                "leg_b_lag_autocorr": {**ac, "fires": leg_b},
                "leg_c_edge_decile": {**ed30, "fires": leg_c},
                "sensitivity_KS_at_min10": {**ks10,
                    "fires_if_primary_bar": bool(ks10["p"] == ks10["p"] and ks10["p"] < KS_P_BAR)},
                "any_leg_fires": bool(leg_a or leg_b or leg_c)}

    tstat = time.time()
    tr_raw = [flat[i][0] for i in range(len(rows))]
    ct_raw = [flat[i][1][:len(flat[i][0])] for i in range(len(rows))]
    treat = run_arm(tr_u_all, tr_raw, "treatment_real_hits", HITRICH_MIN)
    ctrl = run_arm(ct_u_all, ct_raw, "control_paired_nonhits", HITRICH_MIN)
    tstat = time.time() - tstat

    # ---- PRE-REGISTERED verdict ----
    art_contaminated = treat["any_leg_fires"] and ctrl["any_leg_fires"]
    if art_contaminated:
        verdict = "ARTIFACT-CONTAMINATED"
        h1 = False; h0 = False
    elif treat["any_leg_fires"]:
        verdict = "POSITIONAL-STRUCTURE-REAL"
        h1 = True; h0 = False
    else:
        verdict = "UNIFORM-NO-POSITIONAL-GEOMETRY"
        h1 = False; h0 = True
    fired_legs_t = [k for k in ("leg_a_pooled_KS", "leg_b_lag_autocorr", "leg_c_edge_decile")
                    if treat[k]["fires"]]
    fired_legs_c = [k for k in ("leg_a_pooled_KS", "leg_b_lag_autocorr", "leg_c_edge_decile")
                    if ctrl[k]["fires"]]
    verdicts = {
        "H1_positional_structure_real": h1,
        "H0_uniform_no_positional_geometry": h0,
        "rule": ("H1 iff any pre-named leg fires on treatment (KS p<0.01 pooled "
                 "u vs U[0,1] over Ns with >=30 hits | |mean lag-1..10 rho|>0.05 "
                 "with bootstrap 95% CI excluding 0 | edge-decile frac>0.25 and "
                 "binomial p<0.01 vs 0.20); paired-control arms must be null "
                 "else ARTIFACT-CONTAMINATED"),
        "verdict": verdict,
        "treatment_fired_legs": fired_legs_t,
        "control_fired_legs": fired_legs_c,
        "consequence_if_H1": ("within-N positional geometry exists -> opens "
                              "'polynomial-sequence local structure' as a carrier "
                              "for the unexplained ~39-61% per-N overdispersion"),
        "consequence_if_H0": ("positional route closes cleanly -> residual "
                              "dispersion is pure N-level rate variance; deepens "
                              "to hidden-N-covariate question"),
    }

    # dispersion continuity check vs exp577 lineage
    hs = [r["hits"] for r in rows]
    ms = sum(hs)/len(hs)
    var_h = sum((y-ms)**2 for y in hs)/len(hs)
    stats_out = {
        "mean_hits_per_N": round(ms, 2),
        "var_hits": round(var_h, 2),
        "D_raw_index_of_dispersion": round(var_h/ms, 2) if ms else float("nan"),
        "min_hits": min(hs), "max_hits": max(hs),
        "zero_hit_N_count": sum(1 for y in hs if y == 0),
        "total_hits": sum(hs),
        "segment_s": {"population": round(tpop, 1), "positions": round(thit, 1),
                      "stats": round(tstat, 1)},
    }

    wall = time.time()-t0
    slim_rows = [{k: r[k] for k in ("i", "N", "hits", "rate", "ctl_used")} for r in rows]
    out = {
        "exp": "578", "codename": "HIT-POSITION-STRUCTURE", "mode": mode,
        "config": {
            "master_seed": SEED, "bits": BITS, "n_pool": n_pool,
            "jsamples_per_N": jsamples, "cut": CUT_BIG,
            "tester": "exp569 gcd-chain verbatim (exp576/577 code path)",
            "grid": "[isqrt(N)+1, 3*isqrt(N)], u=(j-jlo)/(jhi-jlo)",
            "bars": {"KS_P_BAR": KS_P_BAR, "AUTOCORR_RHO_BAR": AUTOCORR_RHO_BAR,
                     "EDGE_FRAC_BAR": EDGE_FRAC_BAR, "EDGE_P_BAR": EDGE_P_BAR},
            "nbins_indicator": NBINS, "lags": LAGS,
            "boot_reps": BOOT_REPS, "hitrich_min_primary": HITRICH_MIN,
            "control_cap_per_N": JCAP_CONTROL,
            "positions_npz": npz_path,
            "seed_distinctness": distinct,
        },
        "rows": slim_rows, "stats": stats_out,
        "arms": {"treatment": treat, "control": ctrl},
        "verdicts": verdicts,
        "honest_notes": [
            "marginal u is uniform BY CONSTRUCTION under uniform j-sampling; any "
            "treatment signal is therefore carried by smoothness of j^2-N as a "
            "function of j -- that is exactly the claim under test; the paired "
            "non-hit control shares the sampling stream and calibrates the pipe",
            "3-leg multiplicity is the REGISTERED rule (H1 iff any leg fires, "
            "each at 0.01); no post-hoc legs added",
            "pooled KS weights Ns by hit count (rate-weighted pooling); control "
            "arm shares the weighting; per-N KS not used for verdict",
            "indicator series counts hits per spatial bin WITHOUT renormalizing "
            "by per-bin sample counts (sampling density uniform in expectation); "
            "empty bins zero-filled; at ~78 hits/1000 bins the autocorr "
            "estimator is noisy -- bootstrap CI carries the inference",
            "edge decile and KS both probe the shape of the same pooled u "
            "(partially overlapping legs; disclosed)",
            "sensitivity KS at >=10-hit inclusion disclosed, not verdict-bearing",
            "single fresh master seed 20260828; lineage asserted vs regenerated "
            "20260824..27 streams (+hash reproduction of the recorded quartet "
            "in full mode)",
            "smoke mode is plumbing/calibration only (expected hits/N ~10 < 30 "
            "so HITRICH sets are near-empty there)",
            "positions persisted compressed (exp578_*npz): hit_j and paired "
            "non-hit j arrays per N + jlo/jhi -- full indicator series "
            "reconstructible",
            "REPAIR 2026-08-24 (self-caught in ledger review): first run's "
            "CONTROL-arm leg-b mirrored the TREATMENT arm (acf builder read "
            "hit arrays unconditionally); control leg-b was recomputed from "
            "exp578_positions.npz by exp578_repair_legb.py and patched into "
            "exp578_result.json. Verdict unaffected: leg-b fired on neither "
            "arm; legs a/c controls were computed correctly all along",
            "MAGNITUDE CONFOUND (coordinator-directed post-hoc check, "
            "exp578_stratified_check.py): v=j^2-N rises monotonically over the "
            "window so pure smoothness decay skews hits to small-u WITHOUT any "
            "positional structure; the check conditions on (bitlen(v) x "
            "mantissa-octant) strata -- per-stratum two-sample KS of hit-u vs "
            "SIZE-MATCHED non-hit-u, within-stratum label permutation for the "
            "pooled D, stratified edge test. Rule stated BEFORE the check: "
            "stratified perm p<0.01 => BEYOND-MAGNITUDE (H1 stands strong); "
            "else H1 downgrades to PROFILE-IS-SIZE-GRADIENT",
        ],
        "wall_s": round(wall, 1),
    }
    fn = "exp578_smoke_result.json" if smoke else "exp578_result.json"
    with open(fn, "w") as f:
        json.dump(out, f, indent=1)
    summ = {
        "stats": stats_out,
        "treatment": {k: treat[k] for k in ("n_hitrich30", "leg_a_pooled_KS",
                                            "leg_b_lag_autocorr", "leg_c_edge_decile")},
        "control": {k: ctrl[k] for k in ("n_hitrich30", "leg_a_pooled_KS",
                                         "leg_b_lag_autocorr", "leg_c_edge_decile")},
        "verdicts": {k: v for k, v in verdicts.items()
                     if k not in ("consequence_if_H1", "consequence_if_H0", "rule")},
    }
    print(json.dumps(summ, indent=1)[:4000], flush=True)
    print(f"[{mode}] verdict={verdict} wall={wall:.1f}s -> {fn}", flush=True)


if __name__ == "__main__":
    main()

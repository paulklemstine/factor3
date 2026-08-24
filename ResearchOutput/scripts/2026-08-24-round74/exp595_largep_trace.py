#!/usr/bin/env python3
"""exp595 LARGER-P-ECM-TRACE (round-74; completes papers 215 -> 236 -> 238)

Question: exp570 concluded COLLISION FLOOR SUBDOMINANT and ORDER-HITS FIRE EARLY
(KS rejected uniformity with hits concentrating early in the curve, and measured
found_p rates sat far above the 1-exp(-1.44*B1/p) collision baseline). Does that
picture HOLD at bitlen 32 with the step-index trace, using enough curves per cell
to separate mechanisms cleanly?

PRE-REGISTRATION (transcribed from the coordinator brief BEFORE any data collection;
no exp595 data existed at write time; exp570_collision_trace.py machinery VERBATIM):
  H1 (scale-stability + early-fire replicate): at bitlen 32,
    (a) RATE: cell found_p rate at B1/p = 0.125 ~= bitlen-26's rate -- two-proportion
        z-test p > 0.05 AND overlapping Wilson 95% CIs;
    (b) GEOMETRY: the step-index distribution of found_p hits STILL REJECTS
        Uniform[0,1] at KS p < 0.01 in every (bitlen, B1frac) cell with >= 10 hits,
        and early-fire geometry is PRESERVED: median normalized step < 0.5 AND
        tail fraction (norm >= 0.8) < 0.3 (hits are NOT final-20% concentrated).
  H0 (scale-dependence real): EITHER the bitlen-32 low-B1 rate drops significantly
      below bitlen-26's (z p < 0.05, disjoint CIs) toward the per-curve collision
      baseline 1-exp(-1.44*B1/p) (= 0.1647 at frac 0.125; 3-curve cell-adjusted
      1-(1-0.1647)^3 = 0.4191), OR the geometry changes (uniformity not rejected at
      0.125, or late-firing median/tail emerges). Report which leg fired.

Machinery: exp570_collision_trace.py reused VERBATIM (itself exp568/exp488-validated
guarded affine ops); stage1 carries a step counter (idx incremented at every guarded
inversion AND each end-of-chunk gcd check; found_at records the firing step); total
steps per curve is DATA-INDEPENDENT (control flow depends only on the schedule), so
the normalization denominator comes from total_stage1_steps(B1) in closed form.
Arm B2=B1 only (stage 2 not needed); curves cap 3.
Populations: h=13 (bitlen-26 stratum) and h=15 (bitlen-32 stratum, p ~ 2^14-15,
q ~ 3-4p), n_N=40 each, fixed NEW seed 20260903.
Grid: B1/p in {0.125 ceil, 0.5 ceil, 0.9 floor}.
"""
import sys, time, json, math, random
from multiprocessing import Pool
from sympy import nextprime

SEED = 20260903
CURVES = 3

# ---------- guarded affine EC ops (VERBATIM from exp568/exp488 via exp570) ----------
def ec_double(N, a, P):
    x1, y1 = P
    den = (2*y1) % N
    g = math.gcd(den, N)
    if 1 < g < N: return ('found', g)
    if g == N:    return ('dead', None)
    lam = ((3*x1*x1 + a) * pow(den, -1, N)) % N
    x3 = (lam*lam - 2*x1) % N
    y3 = (lam*(x1 - x3) - y1) % N
    return ('ok', (x3, y3))

def ec_add(N, a, P, Q):
    (x1, y1), (x2, y2) = P, Q
    den = (x2 - x1) % N
    g = math.gcd(den, N)
    if 1 < g < N: return ('found', g)
    if g == N:
        if (y1 - y2) % N == 0:
            return ec_double(N, a, P)
        return ('dead', None)
    lam = ((y2 - y1) * pow(den, -1, N)) % N
    x3 = (lam*lam - x1 - x2) % N
    y3 = (lam*(x1 - x3) - y1) % N
    return ('ok', (x3, y3))

def prime_power_schedule(B1):
    sched = []
    for cand in range(2, B1 + 1):
        if all(cand % d for d in range(2, int(cand**0.5) + 1)):
            pe = cand
            while pe * cand <= B1: pe *= cand
            sched.append(pe)
    return sched

_SCHED_CACHE = {}
def sched_for(B1):
    if B1 not in _SCHED_CACHE:
        _SCHED_CACHE[B1] = tuple(prime_power_schedule(B1))
    return _SCHED_CACHE[B1]

def total_stage1_steps(B1):
    """Closed-form count of guarded inversions + end-of-chunk gcd checks for one full
    stage-1 curve. Data-independent: control flow depends only on the schedule.
    First chunk: R=None at its leading bit -> doubles=len-1, leading '1' seeds P ->
    adds=popcount-1. Every later chunk starts with R set -> doubles=len(bits),
    adds=popcount. (Verified against traced idx on completed curves in exp570.)"""
    tot = 0
    for i, mm in enumerate(sched_for(B1)):
        bits = bin(mm)[2:]
        if i == 0:
            tot += (len(bits) - 1) + (bits.count('1') - 1) + 1
        else:
            tot += len(bits) + bits.count('1') + 1
    return tot

def stage1(N, a, P, B1, acc, tr=None):
    """exp568 stage1 verbatim + step tracing. tr: {'idx','found_at'} mutated in place."""
    R = None
    for m in sched_for(B1):
        for bit in bin(m)[2:]:
            if R is not None:
                if tr is not None: tr['idx'] += 1
                st, payload = ec_double(N, a, R)
                if st == 'found':
                    if tr is not None: tr['found_at'] = tr['idx']
                    return (st, payload)
                if st != 'ok': return (st, None)
                R = payload
                acc[0] = (acc[0] * ((2*R[1]) % N)) % N
            if bit == '1':
                if R is None:
                    R = P
                else:
                    if tr is not None: tr['idx'] += 1
                    st, payload = ec_add(N, a, P, R)
                    if st == 'found':
                        if tr is not None: tr['found_at'] = tr['idx']
                        return (st, payload)
                    if st != 'ok': return (st, None)
                    R = payload
                    acc[0] = (acc[0] * ((P[0]-R[0]) % N)) % N
        if tr is not None: tr['idx'] += 1
        g = math.gcd(acc[0], N)
        if 1 < g < N:
            if tr is not None: tr['found_at'] = tr['idx']
            return ('found', g)
        if g == N:    return ('dead', None)
        acc[0] = 1
    return ('ok', R)

def trial(N, p_true, q_true, B1, total_steps, rng=None, curves=CURVES):
    """One cell trial (B2=B1 arm: stage-1 only). Returns an outcome dict."""
    for c in range(curves):
        a = rng.randrange(6, max(N, 7))
        x = rng.randrange(2, max(N, 3)); y = rng.randrange(2, max(N, 3))
        P = (x % N, y % N)
        acc = [1]
        tr = {'idx': 0, 'found_at': None}
        st, res = stage1(N, a, P, B1, acc, tr)
        if st == 'found':
            if res == p_true: bk = 'found_p'
            elif res == q_true: bk = 'found_q'
            else: bk = 'found_other'
            return {'bucket': bk, 'curve': c,
                    'found_at': tr['found_at'],
                    'norm': round(tr['found_at'] / total_steps, 4)}
        if st == 'dead':
            continue
    return {'bucket': 'nothing', 'curve': None, 'found_at': None, 'norm': None}

def worker(args):
    cells, seed = args
    rng = random.Random(seed)
    out = {}
    for (tag, N, p_t, q_t, B1, total_steps) in cells:
        out[tag] = trial(N, p_t, q_t, B1, total_steps, rng=rng)
    return out

# ---------- stats helpers (dependency-free; VERBATIM from exp570) ----------
def ks_uniform(samples):
    """KS statistic + approximate p-value vs Uniform[0,1] (Kolmogorov series)."""
    xs = sorted(samples); n = len(xs)
    if n < 2: return 0.0, 1.0
    D = 0.0
    for i, v in enumerate(xs):
        D = max(D, (i + 1) / n - v, v - i / n)
    lam = math.sqrt(n) * D
    s = 0.0
    for j in range(1, 10001):
        term = (-1)**(j-1) * math.exp(-2 * j*j * lam * lam)
        s += term
        if abs(term) < 1e-15: break
    return D, max(0.0, min(1.0, 2 * s))

def wilson(k, n, z=1.959963985):
    if n == 0: return (0.0, 1.0)
    ph = k / n
    d = 1 + z*z/n
    c = (ph + z*z/(2*n)) / d
    h = z * math.sqrt(ph*(1-ph)/n + z*z/(4*n*n)) / d
    return (max(0.0, c - h), min(1.0, c + h))

def binom_two_sided(k, n, p0):
    """Exact two-sided binomial test p-value."""
    def lpmf(k): return math.comb(n, k) * p0**k * (1-p0)**(n-k)
    pk = lpmf(k)
    lo = sum(lpmf(i) for i in range(0, k+1))
    hi = sum(lpmf(i) for i in range(k, n+1))
    return max(0.0, min(1.0, min(1.0, 2 * min(lo, hi))))

def two_prop_z(k1, n1, k2, n2):
    """Two-proportion pooled-z two-sided p-value."""
    if n1 == 0 or n2 == 0: return 1.0
    p1, p2 = k1/n1, k2/n2
    pp = (k1 + k2) / (n1 + n2)
    se = math.sqrt(pp*(1-pp)*(1/n1 + 1/n2))
    if se == 0: return 1.0
    z = abs(p1 - p2) / se
    return max(0.0, min(1.0, math.erfc(z / math.sqrt(2))))

BASELINE_F = 1.44  # ops ~ 1.44*B1 (theta(B1)/ln2); pre-registered constant

def main():
    t0 = time.time()
    mode = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    smoke = mode == "smoke"
    n_N = 8 if smoke else 40
    bitlens = [13] if smoke else [13, 15]     # h: p ~ h bits -> N ~ 26 / 31-32 bits
    B1fracs = [(0.125, 'ceil'), (0.5, 'ceil'), (0.9, 'floor')]
    # populations: per-stratum fixed seed (disclosed)
    pops = {}
    pstats = {}
    for h in bitlens:
        rng = random.Random(SEED * 1000 + h)
        pop = []
        while len(pop) < n_N:
            r = rng.getrandbits(h) | (1 << (h-1)) | 1
            p = int(nextprime(r)); q = int(nextprime(3 * p + rng.randrange(1, 200)))
            N = p * q
            lo_, hi_ = min(p, q), max(p, q)
            if hi_.bit_length() - lo_.bit_length() > 3: continue
            pop.append((N, lo_, hi_))
        pops[h] = pop
        pb = [lo_.bit_length() for _, lo_, _ in pop]
        Nb = [(N).bit_length() for N, _, _ in pop]
        pstats[h] = {"p_bits_min": min(pb), "p_bits_max": max(pb),
                     "N_bits_min": min(Nb), "N_bits_max": max(Nb)}
    # cells
    cells = []
    meta = {}   # tag -> (h, idx, fi, B1, p_true, total_steps)
    for h in bitlens:
        for idx, (N, p_t, q_t) in enumerate(pops[h]):
            for fi, (f, rnd) in enumerate(B1fracs):
                B1 = int(math.ceil(f * p_t)) if rnd == 'ceil' else int(math.floor(f * p_t))
                B1 = max(B1, 20)
                ts = total_stage1_steps(B1)
                tag = f"{h}:{idx}:{fi}"
                meta[tag] = (h, idx, fi, B1, p_t, ts)
                cells.append((tag, N, p_t, q_t, B1, ts))
    nchunk = 4 if smoke else 8
    chunks = [(cells[c::nchunk], SEED + c) for c in range(nchunk)]
    print(f"[{mode}] {len(cells)} cells / {nchunk} workers; pstats={pstats}", flush=True)
    with Pool(nchunk) as pool:
        results = pool.map(worker, chunks)
    merged = {}
    for r in results: merged.update(r)
    # ---- aggregate per (h, fi) ----
    import collections
    agg = collections.defaultdict(lambda: {"cnt": collections.Counter(), "norms": [],
                                           "first_curve_found_p": 0})
    for tag, oc in merged.items():
        h_s, idx_s, fi_s = tag.split(":")
        key = (int(h_s), int(fi_s))
        A = agg[key]
        A["cnt"][oc["bucket"]] += 1
        if oc["bucket"] == "found_p":
            A["norms"].append(oc["norm"])
            if oc["curve"] == 0:
                A["first_curve_found_p"] += 1
    rows, ks_stats = [], {}
    for (h, fi), A in sorted(agg.items()):
        cnt = A["cnt"]; tot = sum(cnt.values())
        fp = cnt["found_p"]
        f, rnd = B1fracs[fi][0], B1fracs[fi][1]
        # collision baselines
        bs_const = []      # 1-exp(-1.44*f)  (scale-free at fixed ratio)
        bs_exact = []      # 1-exp(-ops_exact/p) per N
        bs_cell3 = []      # 1-(1-bc)^3 per N
        for tag2, (h2, idx2, fi2, B1, p_t, ts) in meta.items():
            if h2 == h and fi2 == fi:
                bs_const.append(1 - math.exp(-BASELINE_F * f))
                bc = 1 - math.exp(-ts / p_t)
                bs_exact.append(bc)
                bs_cell3.append(1 - (1 - bc)**CURVES)
        base_c = bs_const[0]
        row = {"h": h, "target_bitlen": 26 if h == 13 else 32,
               "B1frac": f, "round": rnd, "total": tot,
               "found_p": fp, "found_q": cnt["found_q"],
               "found_other": cnt["found_other"], "nothing": cnt["nothing"],
               "cell_rate_found_p": round(fp / tot, 4),
               "first_curve_rate_found_p": round(A["first_curve_found_p"] / tot, 4),
               "baseline_const_percurve": round(base_c, 4),
               "baseline_exact_percurve_mean": round(sum(bs_exact)/len(bs_exact), 4),
               "baseline_cell3_mean": round(sum(bs_cell3)/len(bs_cell3), 4),
               # subdominance: first-curve measured rate / per-curve collision baseline
               "collision_subdominance_ratio": round((A["first_curve_found_p"]/tot) / base_c, 2),
               "mean_B1_over_p": round(sum(m_[3]/m_[4] for m_ in meta.values()
                                           if m_[0] == h and m_[2] == fi) / len(bs_exact), 4)}
        ci_cell = wilson(fp, tot)
        row["ci95_cell"] = [round(ci_cell[0], 4), round(ci_cell[1], 4)]
        fc_ci = wilson(A["first_curve_found_p"], tot)
        row["ci95_first_curve"] = [round(fc_ci[0], 4), round(fc_ci[1], 4)]
        rows.append(row)
        D, kp = ks_uniform(A["norms"]) if A["norms"] else (None, None)
        tail = sum(1 for v in A["norms"] if v >= 0.8)
        ks_stats[f"h{h}_frac{f}"] = {
            "n_found_p": len(A["norms"]), "D": None if D is None else round(D, 4),
            "ks_p": None if kp is None else round(kp, 4),
            "tail_frac_ge08": round(tail / len(A["norms"]), 4) if A["norms"] else None,
            "tail_binom_p_vs_02": round(binom_two_sided(tail, len(A["norms"]), 0.2), 4) if A["norms"] else None,
            "median_norm": round(sorted(A["norms"])[len(A["norms"])//2], 3) if A["norms"] else None,
            "norms": A["norms"]}
    print(json.dumps(rows, indent=1))
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != 'norms'} for k, v in ks_stats.items()}, indent=1))

    # ---- verdicts (pre-registered above) ----
    def K(h, f): return ks_stats.get(f"h{h}_frac{f}")
    def Rw(h, f): return next((r for r in rows if r["h"] == h and r["B1frac"] == f), None)
    verdicts = {}

    # H1(b): geometry -- KS rejects uniformity at p<0.01 with early-fire shape,
    # in every cell with >= 10 hits, both bitlens.
    geom_cells, geom_fail = [], []
    for h in bitlens:
        for f, _ in B1fracs:
            kk = K(h, f)
            if kk is None or kk["n_found_p"] < 10: continue
            okk = (kk["ks_p"] < 0.01 and kk["median_norm"] < 0.5
                   and kk["tail_frac_ge08"] < 0.3)
            geom_cells.append(okk)
            if not okk:
                geom_fail.append(f"h{h}_f{f}(ks_p={kk['ks_p']},med={kk['median_norm']},tail={kk['tail_frac_ge08']})")
    verdicts["n_geom_cells_tested"] = len(geom_cells)
    verdicts["h1b_early_fire_geometry"] = (
        "supported" if geom_cells and all(geom_cells)
        else "refuted" if geom_fail else "insufficient_hits")
    if geom_fail:
        verdicts["h1b_failing_cells"] = geom_fail

    # H1(a): rate stability at frac 0.125, bitlen 26 vs 32
    r26, r32 = Rw(13, 0.125), Rw(15, 0.125)
    if r26 and r32:
        zt = two_prop_z(r26["found_p"], r26["total"], r32["found_p"], r32["total"])
        ovl = (r26["ci95_cell"][0] <= r32["ci95_cell"][1]) and (r32["ci95_cell"][0] <= r26["ci95_cell"][1])
        verdicts["h26_vs_h32_rate_at_0.125_ztest_p"] = round(zt, 4)
        verdicts["h26_vs_h32_CIs_overlap"] = bool(ovl)
        verdicts["h1a_scale_stability_rate"] = (
            "supported" if (zt > 0.05 and ovl) else
            "refuted_drop" if r32["cell_rate_found_p"] < r26["cell_rate_found_p"] else
            "refuted_rise")
        # H0 leg 1 detail: does bitlen-32 sit at the collision baseline?
        lo32, hi32 = r32["ci95_cell"]
        verdicts["h32_cell_vs_3curve_baseline_0.4191"] = (
            "contains" if lo32 <= r32["baseline_cell3_mean"] <= hi32
            else "above_baseline" if lo32 > r32["baseline_cell3_mean"]
            else "below_baseline")
        # cross-bitlen at the other fracs (context, not pre-registered gates)
        for f in (0.5, 0.9):
            ra, rb = Rw(13, f), Rw(15, f)
            if ra and rb:
                zz = two_prop_z(ra["found_p"], ra["total"], rb["found_p"], rb["total"])
                verdicts[f"h26_vs_h32_rate_at_{f}_ztest_p"] = round(zz, 4)
                verdicts[f"h26_vs_h32_CIs_overlap_at_{f}"] = bool(
                    ra["ci95_cell"][0] <= rb["ci95_cell"][1] and rb["ci95_cell"][0] <= ra["ci95_cell"][1])

    # ---- overall H verdict ----
    geom_ok = verdicts.get("h1b_early_fire_geometry") == "supported"
    rate_ok = verdicts.get("h1a_scale_stability_rate") == "supported"
    if geom_ok and rate_ok:
        verdicts["H1"] = "TRUE"
        verdicts["H0"] = "refuted_scale_dependence_not_real"
    elif geom_ok and verdicts.get("h1a_scale_stability_rate") is None:
        verdicts["H1"] = "PARTIAL_RATE_UNTESTABLE"
    elif not geom_ok and not rate_ok:
        verdicts["H1"] = "REFUTED"
        verdicts["H0"] = "supported_both_legs"
    else:
        verdicts["H1"] = "MIXED"
        fired = []
        if not rate_ok: fired.append("rate_leg:" + str(verdicts.get("h1a_scale_stability_rate")))
        if not geom_ok: fired.append("geometry_leg:" + str(verdicts.get("h1b_early_fire_geometry")))
        verdicts["H0"] = "partially_supported_" + ";".join(fired)

    wall = time.time() - t0
    out = {"exp": "595", "codename": "LARGER-P-ECM-TRACE", "mode": mode,
           "seed": SEED, "n_N": n_N, "bitlens_h": bitlens, "population_stats": pstats,
           "config": {"B1fracs": [f for f, _ in B1fracs], "arm": "B2=B1 (stage-1 only)",
                      "curves_cap": CURVES, "baseline_const": BASELINE_F,
                      "baseline_formula": "1-exp(-1.44*B1/p) per curve",
                      "trace": "step idx at every guarded inversion + chunk gcd check, "
                               "normalized by closed-form data-independent total steps",
                      "adapted_from": "exp570_collision_trace.py (verbatim machinery)"},
           "rows": rows, "ks_stats": ks_stats, "verdicts": verdicts,
           "honest_notes": [
               "Pre-registration written into the module docstring BEFORE any exp595 "
               "data existed; machinery copied verbatim from exp570.",
               "exp570's own pre-reg anticipated collision domination at scale and its "
               "result went the other way (floor subdominant, early fire); exp595's "
               "H1 encodes THAT outcome as the replication hypothesis, tested at "
               "bitlen 32 with fresh seed/populations and the 0.25->0.5 grid swap "
               "pre-registered by the coordinator brief.",
               "KS p-values use the asymptotic Kolmogorov series (n>=2); cells with "
               "<10 found_p hits are excluded from the geometry gate (n reported).",
               "Early-fire operationalization (median<0.5, tail>=0.8 fraction<0.3) was "
               "fixed before data from the qualitative exp570 conclusion alone; the "
               "raw norms are shipped in ks_stats for post-hoc re-reads.",
               "Collision baseline treats inversion denominators as independent "
               "uniform mod p; chunk-batched gcd checks count as trace steps.",
               "found_q events are pure q-side collision luck (B1<p<<q makes "
               "order-completion impossible); they independently cross-check the "
               "collision floor size.",
               "Trace denominator is schedule-only (data-independent); ec_add's rare "
               "recursive internal double (den==0 mod N & y1==y2) executes without an "
               "idx increment -- tiny data-dependent bias on found_at indices only.",
               "'deaths' (gcd==N) collapse silently inside trial(); not separately "
               "bucketed (inherited exp568/exp570 behavior).",
               "Cell rates are 3-curve quantities (any-curve success); first_curve "
               "fields give the per-curve view matched to the per-curve baseline.",
           ],
           "wall_s": round(wall, 1)}
    fname = f"exp595_{'smoke_' if smoke else ''}result.json"
    with open(fname, "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"[{mode}] wall={wall:.1f}s -> {fname}")

if __name__ == "__main__":
    main()

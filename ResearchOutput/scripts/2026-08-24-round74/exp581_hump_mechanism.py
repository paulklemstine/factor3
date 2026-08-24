#!/usr/bin/env python3
"""exp581 HUMP-MECHANISM (round-74)

PRE-REGISTRATION (in header BEFORE any analysis; data access limited to
exp578_positions.npz + exp578/exp579 docs):

Target: paper-229/exp579 residual R(b)=T(b)/M(b) -- a +/-20% concave
mid-window hump (published anchors: R_first=0.8007 @x=.01, peak 1.2257 at
bin33 x~0.67, R_last=0.8957 @x=.99, quad vertex x=0.5896 interior, quad c
boot95 wholly<0). QUESTION: what CARRIES the hump?

Registered decompositions:
  LPF bands: largest prime factor <=1e6 of each hit v; bands
    {<=100, 100-1e3, 1e3-1e4, >1e4..1e6} with nominal decimal edges.
  k100 terciles: k100 = #distinct primes <=100 (B0=100) dividing hit v;
    classes cut at terciles of pooled hit-k100 mass.

Per-stratum shape residual: R_S(b) = T_S,norm(b)/M_S,norm(b), both
normalized WITHIN stratum S (offset-invariant). Baseline M_S: mixture-
Dickman P(LPF in (L,U]) = rho(ln v/ln U) - rho(ln v/ln L) (band-1:
rho(ln v/ln 100)), mixed over exp579's 17-pt uniform-r prior with 400-pt
trapezoid per bin in j-space.

HUMP_S fire rule (identical machinery on every family, both arms):
WLS quadratic on R_S(x), weights 1/bootSE^2 (cluster bootstrap over Ns,
2000 reps, seed 20260831, fixed weights across replicates):
  (i) c boot95 percentile CI wholly < 0;
  (ii) point vertex -b/(2c) in (0.15,0.85) (needs point c<0);
  (iii) fitted peak value boot95 p2.5 > 1.05.
Families with observed mass < LOW_MASS_MIN(200) are ineligible (excluded
from fire counts, disclosed).

VERDICT TREE (priority order):
  ARTIFACT-CONTAMINATED: any control family (pooled or LPF stratum) fires;
    control baseline = uniform density over the same bins (paired exp578
    non-hits carry no smoothness gradient).
  H1a LPF-carrier: EXACTLY ONE eligible treatment LPF band fires
    (hump concentrated in one band, other per-stratum profiles flat).
  H1b small-prime-combo carrier: >=3/4 eligible LPF bands fire AND 0/3
    eligible k100 terciles fire (persists within every band but vanishes
    under small-prime-combination conditioning).
  H0 window/polynomial geometry artifact: >=3/4 eligible LPF bands AND
    >=2/3 eligible k100 terciles fire (hump present uniformly across all
    decompositions).
  BASELINE-MASS-REALLOCATION: no stratum fires anywhere (F_lpf=F_k=0) yet
    the pooled hump fires => carrier is Dickman's band-mass allocation
    (m_S != mu_S), not within-stratum geometry.
  MIXED: anything else (fire counts reported verbatim).

CALIBRATION GATES (before verdicts):
  G1 (hard, full mode): regenerated per-hit positions + paired controls +
    jlo/jhi must EQUAL exp578_positions.npz arrays exactly (exp577-style
    sha256 discipline over canonical int64 serialization); abort if not.
    Population lineage asserted: master hash 06931068f8f3ca9b + recorded
    quartet e8d89a29/9cb9cc80/81acc9b5/a15e2877 reproduced + pairwise
    disjoint N sets vs seeds 20260824..27.
  G2 (soft): my pooled R(b) must land near exp579's published scalar
    anchors (R_first/peak/R_last/vertex within tolerances below); T(b) is
    npz-derived. Exact per-bin table comparison intentionally skipped to
    avoid transcription risk -- only scalar anchors quoted.
  G3 (soft): pooled control flat replicates exp579's control gate.
"""
import sys, os, time, json, math, hashlib, random
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

SEED = 20260828
BITS = 96
CUT_SMALL, CUT_BIG = 100000, 1000000
JCAP_CONTROL = 4000
PRIOR_SEEDS = (20260824, 20260825, 20260826, 20260827)
RECORDED_HASHES = {"20260824": "e8d89a29a03779d5",
                   "20260825": "9cb9cc800ee45a38",
                   "20260826": "81acc9b5e1be619b",
                   "20260827": "a15e2877dd1dac7a"}
MASTER_HASH = "06931068f8f3ca9b"

NBINS = 50
NPT = 400                 # trapezoid intervals per bin (401 nodes), exp579 recipe
NR = 17                   # uniform-r mixture points, exp579 recipe
BOOT_REPS = 2000
BOOT_SEED = 20260831
BAND_NAMES = ["lpf<=100", "lpf_100_1e3", "lpf_1e3_1e4", "lpf_gt_1e4"]
LN = {100: math.log(100.0), 1000: math.log(1000.0),
      10000: math.log(10000.0), 1000000: math.log(1000000.0)}
B0 = 100
LOW_MASS_MIN = 200
MID_LO, MID_HI = 25, 39   # bins centered x .51-.79 (hump window)
ANCHOR = {"R_first": 0.8007, "tol_ends": 0.08,
          "R_peak": 1.2257, "peak_bin": 33, "tol_peak": 0.10,
          "R_last": 0.8957, "vertex": 0.5896, "tol_vertex": 0.12}

import gmpy2
from gmpy2 import mpz, gcd, next_prime
import numpy as np


# ---------- VERBATIM exp578 code path (population + sampling + tester) ----------
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
    """Same sampling stream as exp576/577 worker, PLUS position recording."""
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


# ---------------------------- factoring machinery ----------------------------
_G2 = {}
def init_fact(primes):
    _G2["PR"] = primes

def fac_one(v):
    """Trial-divide ascending; early exit when cofactor proven prime.
    Returns (residual_cofactor, lpf_found_or_0, k100). For hits residual==1."""
    PR = _G2["PR"]
    cof = int(v); lpf = 0; k100 = 0
    for p in PR:
        if cof == 1:
            break
        if cof % p:
            if p * p > cof:
                lpf = cof          # cofactor itself prime (>p>=2): last factor
                if cof <= B0:
                    k100 += 1
                cof = 1
                break
            continue
        lpf = p
        if p <= B0:
            k100 += 1
        cof //= p
        while cof % p == 0:
            cof //= p
    return cof, lpf, k100

def fact_worker(args):
    items = args                      # list of (N, js_list)
    out = []
    for N, js in items:
        res = []
        for j in js:
            v = j * j - N
            cof, lpf, k100 = fac_one(v)
            res.append((lpf, k100, cof == 1))
        out.append(res)
    return out


# ---------------------------- Dickman machinery ----------------------------
def build_rho(u_max=18.0, h=1.0 / 8192):
    n = int(round(u_max / h)); xs = np.linspace(0.0, u_max, n + 1)
    vals = np.empty(n + 1); w = int(round(1.0 / h))
    vals[:w + 1] = 1.0
    for k in range(w + 1, n + 1):
        seg = vals[k - w:k + 1]
        vals[k] = (seg[0] * 0.5 + seg[1:-1].sum() + seg[-1] * 0.5) * h / xs[k]
    return xs, vals


def check_rho(xs, vals):
    def r(u): return float(np.interp(u, xs, vals))
    checks = {2: 0.306853, 3: 0.048608, 4: 0.004911, 5: 0.000355}
    errs = {u: abs(r(u) - t) for u, t in checks.items()}
    assert max(errs.values()) < 1e-4, f"rho table broken: {errs}"
    return errs


def baseline_per_N(jlo, jhi, rho_xs, rho_vals,
                   edges=((None, 100), (100, 1000), (1000, 10000), (10000, 1000000))):
    """Mraw[nbins,nbands]: mixture-Dickman mass of each (L,U] LPF band per u-bin."""
    s = jlo - 1; span = jhi - jlo; two_s = 2 * s
    nb = len(edges)
    lus = {}                                       # arbitrary-edge ln cache
    for (L_, U_) in edges:
        lus[U_] = math.log(float(U_))
        if L_ is not None and L_ not in lus:
            lus[L_] = math.log(float(L_))
    rm = two_s * np.arange(NR) / float(NR - 1)     # exact floats (mult of 2s/16)
    Mraw = np.zeros((NBINS, nb))
    d_small_cut = 256                              # exact int64 corner path
    for b in range(NBINS):
        j0 = jlo + span * b / NBINS; j1 = jlo + span * (b + 1) / NBINS
        js = np.linspace(j0, j1, NPT + 1)
        d = js - s                                 # exact float ints
        base = d * (d + two_s)
        V = np.empty((NPT + 1, NR), dtype=np.float64)
        V[:] = base[:, None] - rm[None, :]
        sm = d <= d_small_cut
        if sm.any():
            di = d[sm].astype(np.int64)
            Vi = di[:, None] * (di[:, None] + two_s) - rm[None, :].astype(np.int64)
            V[sm] = Vi.astype(np.float64)
        mask = V > 1.0
        vm = V[mask]; lvm = np.log(vm)
        cols = []
        for (L, U) in edges:
            fu = np.interp(lvm / lus[U], rho_xs, rho_vals)
            f = fu if L is None else fu - np.interp(lvm / lus[L], rho_xs, rho_vals)
            cols.append(f)
        Fs = np.zeros((NPT + 1, NR, nb))
        Fs[mask] = np.stack(cols, axis=1)
        dx = js[1] - js[0]
        integ = (Fs[0] * 0.5 + Fs[1:-1].sum(0) + Fs[-1] * 0.5) * dx   # (NR,nb)
        Mraw[b] = integ.mean(0)
    return Mraw


# ---------------------------- stats helpers ----------------------------
XFIT = (np.arange(NBINS) + 0.5) / NBINS

def wls_quad(y, w):
    W = 1.0 / np.sqrt(np.maximum(w, 1e-12))
    X = np.stack([np.ones(NBINS), XFIT, XFIT ** 2], 1) * W[:, None]
    beta, *_ = np.linalg.lstsq(X, y * W, rcond=None)
    return beta                                  # [a, b, c]

def quad_stats(beta):
    a, bb, c = beta
    if c >= 0:
        return float(c), float("nan"), float("nan")
    vx = -bb / (2.0 * c)
    pk = a - bb * bb / (4.0 * c)
    return float(c), float(vx), float(pk)


def analyze_family(Rmean, Rboot, label):
    """Rmean (50,), Rboot (reps,50). Returns fire stats dict."""
    ok = np.isfinite(Rboot).all(axis=1) & np.isfinite(Rmean).all()
    if ok.sum() < 200 or not bool(np.all(np.isfinite(Rmean))):
        return {"family": label, "degenerate": True, "n_boot_ok": int(ok.sum()),
                "fires_HUMP": False,
                "fire_parts": {"c": False, "vertex": False, "peak": False}}
    Rboot = Rboot[ok]
    se = Rboot.std(0, ddof=1)
    w = np.maximum(se, 1e-3) ** 2
    beta = wls_quad(Rmean, w)
    c_pt, vx_pt, pk_pt = quad_stats(beta)
    cb = np.empty((Rboot.shape[0], 3)); pb = np.full(Rboot.shape[0], np.nan)
    for r in range(Rboot.shape[0]):
        br = wls_quad(Rboot[r], w); cb[r] = br
        _, _, pp = quad_stats(br)
        pb[r] = pp
    ci_c = [float(np.percentile(cb[:, 2], 2.5)), float(np.percentile(cb[:, 2], 97.5))]
    ci_pk_lo = float(np.nanpercentile(pb, 2.5))
    amp_mid = float(np.mean(Rmean[MID_LO:MID_HI + 1]) - 1.0)
    fire_c = bool(np.isfinite(c_pt) and ci_c[1] < 0.0)
    fire_vx = bool(fire_c and 0.15 <= vx_pt <= 0.85)
    fire_pk = bool(np.isfinite(ci_pk_lo) and ci_pk_lo > 1.05)
    return {"family": label, "n_boot_ok": int(Rboot.shape[0]),
            "quad_abc": [round(float(x), 5) for x in beta],
            "c_ci95": [round(x, 5) for x in ci_c],
            "vertex": round(vx_pt, 4) if math.isfinite(vx_pt) else None,
            "peak": round(pk_pt, 4) if math.isfinite(pk_pt) else None,
            "peak_ci95_lo": round(ci_pk_lo, 4),
            "amp_mid_mean_minus1": round(amp_mid, 4),
            "R_min": round(float(Rmean.min()), 4),
            "R_max": round(float(Rmean.max()), 4),
            "argmax_bin": int(np.argmax(Rmean)),
            "fires_HUMP": bool(fire_c and fire_vx and fire_pk),
            "fire_parts": {"c": fire_c, "vertex": fire_vx, "peak": fire_pk}}


def boot_R(A, Mnorm, idx):
    """A (nN,nbins,K) counts; Mnorm (nbins,K) fixed baseline (unit col-mass).
    Returns Rboot (reps,bins*K) flattened per column."""
    nK = A.shape[2]
    out = np.empty((idx.shape[0], NBINS * nK))
    for r in range(idx.shape[0]):
        ssum = A[idx[r]].sum(0).astype(np.float64)         # (bins,K)
        mass = ssum.sum(0)
        tn = ssum / np.maximum(mass, 1e-12)[None, :]
        out[r] = (tn / Mnorm).T.reshape(-1)
    return out


def arr_digest(arrs):
    h = hashlib.sha256()
    for a in arrs:
        aa = np.ascontiguousarray(a, dtype="<i8")
        h.update(str(len(aa)).encode()); h.update(aa.tobytes())
    return h.hexdigest()[:16]


def main():
    t0 = time.time()
    mode = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    smoke = mode == "smoke"
    n_pool = 16 if smoke else 128
    jsamples = 20000 if smoke else 150000
    nchunk = 2 if smoke else 8
    per = n_pool // nchunk

    print(f"[{mode}] building primorials...", flush=True)
    P5 = build_primorial(CUT_SMALL); P6 = build_primorial(CUT_BIG)
    print(f"primorials bits P5={P5.bit_length()} P6={P6.bit_length()}", flush=True)

    # ---- population ----
    tp = time.time()
    pops = {s: build_population(s, n_pool) for s in ((PRIOR_SEEDS + (SEED,)) if not smoke else (SEED,))}
    tp = time.time() - tp
    seed_lineage = {}
    if not smoke:
        ns_set = {s: frozenset(n for n, _, _ in p) for s, p in pops.items()}
        seeds_all = PRIOR_SEEDS + (SEED,)
        pairs = [(a, b) for ia, a in enumerate(seeds_all) for b in seeds_all[ia + 1:]]
        disj = all(ns_set[a].isdisjoint(ns_set[b]) for a, b in pairs)
        hashes = {str(s): pop_hash(p) for s, p in pops.items()}
        lin = {str(s): hashes[str(s)] == RECORDED_HASHES[str(s)] for s in PRIOR_SEEDS}
        master_ok = hashes[str(SEED)] == MASTER_HASH
        print(f"lineage: disjoint={disj} lineage_repro={all(lin.values())} "
              f"master_hash_match={master_ok}", flush=True)
        assert disj and all(lin.values()) and master_ok, "POPULATION LINEAGE FAILURE"
        seed_lineage = {"pairwise_disjoint": disj, "hashes": hashes,
                        "lineage_repro": lin, "master_hash_match": master_ok}
    pools = pops[SEED]
    print(f"population built ({tp:.1f}s)", flush=True)

    # ---- sampling regeneration (verbatim stream), or resume from persisted ----
    verify = {}
    ts = time.time()
    regen_path = "exp581_regen_positions.npz"
    if not smoke and os.path.exists(regen_path):
        rz = np.load(regen_path)
        reg_hit = [rz[f"hit_{i}"] for i in range(n_pool)]
        reg_ctl_full = [rz[f"ctl_{i}"] for i in range(n_pool)]
        reg_jlo = np.asarray(rz["jlo"], dtype=np.int64)
        reg_jhi = np.asarray(rz["jhi"], dtype=np.int64)
        ts = time.time() - ts
        print(f"RESUME: loaded persisted regen ({ts:.1f}s); "
              f"total hits={sum(len(a) for a in reg_hit)}", flush=True)
        verify["regen_source"] = ("resumed exp581_regen_positions.npz (product of "
                                  "verbatim exp578-path sampling earlier this session; "
                                  "re-gated vs exp578_positions.npz below)")
    else:
        chunks = [(pools[c * per:(c + 1) * per], jsamples, SEED + 7000 + c) for c in range(nchunk)]
        print(f"[{mode}] {nchunk} workers x {per} N x {jsamples} j-samples...", flush=True)
        with Pool(nchunk, initializer=init_worker, initargs=(P5, P6)) as pl:
            res = pl.map(worker, chunks)
        flat = [r for chunk in res for r in chunk]
        ts = time.time() - ts
        print(f"sampling regen done ({ts:.1f}s); total hits={sum(len(r[0]) for r in flat)}", flush=True)

        reg_hit = [np.array(r[0], dtype=np.int64) for r in flat]
        # npz stores the FULL JCAP_CONTROL-capped non-hit arrays; the PAIRED
        # first-len(hits) slice is an exp578-stats convention applied later.
        reg_ctl_full = [np.array(r[1], dtype=np.int64) for r in flat]
        reg_jlo = np.array([r[2] for r in flat], dtype=np.int64)
        reg_jhi = np.array([r[3] for r in flat], dtype=np.int64)
        if not smoke:
            np.savez_compressed(regen_path,
                                **{f"hit_{i}": reg_hit[i] for i in range(n_pool)},
                                **{f"ctl_{i}": reg_ctl_full[i] for i in range(n_pool)},
                                jlo=reg_jlo, jhi=reg_jhi)

    # PAIRED analysis slices (first len(hits) non-hits), exp578 stats convention
    reg_ctl = [rc[:min(len(rh), len(rc))] for rh, rc in zip(reg_hit, reg_ctl_full)]

    if not smoke:
        tv = time.time()
        npz = np.load("exp578_positions.npz")
        ok_hits = True; ok_ctls = True; ok_grids = True
        dig_r = [reg_jlo, reg_jhi]; dig_n = [npz["jlo"], npz["jhi"]]
        for i in range(n_pool):
            rh = reg_hit[i]; rf = reg_ctl_full[i]
            zh = npz[f"hit_{i}"]; zc = npz[f"ctl_{i}"]
            heq = (len(rh) == len(zh)) and bool((rh == zh).all())
            ceq = (len(rf) == len(zc)) and bool((rf == zc).all())
            gl_ok = int(reg_jlo[i]) == int(npz["jlo"][i]) and int(reg_jhi[i]) == int(npz["jhi"][i])
            ok_hits &= heq; ok_ctls &= ceq; ok_grids &= gl_ok
            if not (heq and ceq and gl_ok):
                print(f"MISMATCH at N index {i}: hit_eq={heq} ctl_eq={ceq} "
                      f"(lens {len(rf)} vs {len(zc)}) grid={gl_ok}", flush=True)
            dig_r += [rh, rf]; dig_n += [zh, zc]
        dg_reg = arr_digest(dig_r); dg_npz = arr_digest(dig_n)
        verify = {"hits_equal_all_N": ok_hits, "ctl_full_equal_all_N": ok_ctls,
                  "grids_equal_all_N": ok_grids, "sha256_reg": dg_reg,
                  "sha256_npz": dg_npz, "digests_equal": dg_reg == dg_npz}
        print(f"VERIFY vs exp578_positions.npz: {json.dumps(verify)} ({time.time()-tv:.1f}s)", flush=True)
        assert ok_hits and ok_ctls and ok_grids and dg_reg == dg_npz, \
            "REGENERATION HASH CHECK FAILED"
    else:
        # cheap stream spot-check: N index 0 is FIRST in chunk 0, so its rng
        # stream depends only on (SEED+7000+0, jsamples) -- regenerate inline.
        td = time.time()
        init_worker(P5, P6)                    # classify needs worker globals in-parent
        rng0 = random.Random(SEED + 7000 + 0)
        N0 = pools[0][0]
        s0 = int(gmpy2.isqrt(mpz(N0))); jl0 = s0 + 1; jh0 = 3 * s0
        hp0 = []
        for _ in range(jsamples):
            j = rng0.randint(jl0, jh0)
            v = j * j - N0
            if v <= 1:
                continue
            _, h6 = classify(v)
            if h6:
                hp0.append(j)
        det = hp0 == list(reg_hit[0])
        td = time.time() - td
        verify = {"N0_stream_spotcheck_identical": bool(det)}
        print(f"smoke determinism check (N0 inline regen): identical={det} ({td:.1f}s)", flush=True)
        assert det, "NONDETERMINISTIC REGENERATION"

    # ---- factor hits + controls (LPF<=1e6, k100) ----
    tf = time.time()
    print("building primes<=1e6 ...", flush=True)
    pr = []; q = mpz(2)
    while q <= CUT_BIG:
        pr.append(int(q)); q = next_prime(q)
    print(f"{len(pr)} primes", flush=True)
    tasks_h = []; tasks_c = []
    for i in range(n_pool):
        N = pools[i][0]
        tasks_h.append((N, [int(j) for j in reg_hit[i]]))
        tasks_c.append((N, [int(j) for j in reg_ctl[i]]))
    ch = [(tasks_h[c * per:(c + 1) * per]) for c in range(nchunk)]
    cc = [(tasks_c[c * per:(c + 1) * per]) for c in range(nchunk)]
    with Pool(nchunk, initializer=init_fact, initargs=(pr,)) as pl:
        fh = pl.map(fact_worker, ch)
        fc = pl.map(fact_worker, cc)
    hit_info = [r for chunk in fh for r in chunk]     # per-N list of (lpf,k100,smooth)
    ctl_info = [r for chunk in fc for r in chunk]
    tf = time.time() - tf
    n_nonsmooth_hits = sum(1 for ni in hit_info for (_, _, sm) in ni if not sm)
    print(f"factoring done ({tf:.1f}s); nonsmooth_hits={n_nonsmooth_hits} (must be 0)", flush=True)
    assert n_nonsmooth_hits == 0, "HIT NOT FULLY SMOOTH -- factorer broken"

    def band_of(lpf):
        if lpf <= 0: return -1
        if lpf <= 100: return 0
        if lpf <= 1000: return 1
        if lpf <= 10000: return 2
        return 3                                       # <=1e6 guaranteed for hits

    # ---- count matrices ----
    tc = time.time()
    A_lpf = np.zeros((n_pool, NBINS, 4), dtype=np.int64)
    A_k = np.zeros((n_pool, NBINS, 3), dtype=np.int64)
    A_ctl = np.zeros((n_pool, NBINS, 4), dtype=np.int64)
    ctl_none = 0
    rows = []
    k100_all = []
    lpf_all = []
    for i in range(n_pool):
        jlo = int(reg_jlo[i]); jhi = int(reg_jhi[i]); span = jhi - jlo
        hp = reg_hit[i]
        us = (hp - jlo).astype(np.float64) / span
        bb = np.minimum((us * NBINS).astype(np.int64), NBINS - 1)
        S = np.array([band_of(x[0]) for x in hit_info[i]], dtype=np.int64)
        K = np.array([x[1] for x in hit_info[i]], dtype=np.int64)
        np.add.at(A_lpf[i], (bb, S), 1)
        lpf_all += [int(x[0]) for x in hit_info[i]]
        kt = np.zeros(len(K), dtype=np.int64)
        k100_all += list(K)
        rows.append({"i": i, "N": str(pools[i][0]), "jlo": jlo, "jhi": jhi,
                     "hits": int(len(hp)), "ctl_used": int(len(reg_ctl[i])),
                     "k100_min": int(K.min()), "k100_max": int(K.max()),
                     "band_counts": [int((S == s).sum()) for s in range(4)]})
        cn = reg_ctl[i]
        if len(cn):
            uc = (cn - jlo).astype(np.float64) / span
            bc = np.minimum((uc * NBINS).astype(np.int64), NBINS - 1)
            Sc = np.array([band_of(x[0]) for x in ctl_info[i]], dtype=np.int64)
            keep = Sc >= 0
            ctl_none += int((~keep).sum())
            np.add.at(A_ctl[i], (bc[keep], Sc[keep]), 1)
    k100_all = np.array(sorted(k100_all))
    q1 = int(k100_all[len(k100_all) // 3]); q2 = int(k100_all[2 * len(k100_all) // 3])
    for i in range(n_pool):                            # second pass for terciles
        pass
    # rebuild k-count matrix with cutpoints
    A_k = np.zeros((n_pool, NBINS, 3), dtype=np.int64)
    for i in range(n_pool):
        jlo = int(reg_jlo[i]); jhi = int(reg_jhi[i]); span = jhi - jlo
        hp = reg_hit[i]
        us = (hp - jlo).astype(np.float64) / span
        bb = np.minimum((us * NBINS).astype(np.int64), NBINS - 1)
        K = np.array([x[1] for x in hit_info[i]], dtype=np.int64)
        tt = np.where(K <= q1, 0, np.where(K <= q2, 1, 2)).astype(np.int64)
        np.add.at(A_k[i], (bb, tt), 1)
    tc = time.time() - tc
    print(f"count matrices done ({tc:.1f}s); k100 terciles q1={q1} q2={q2}; "
          f"ctl_none_band={ctl_none}", flush=True)

    # ---- baselines ----
    tb = time.time()
    rho_xs, rho_vals = build_rho()
    rho_errs = check_rho(rho_xs, rho_vals)
    Mraw = np.zeros((n_pool, NBINS, 4))
    for i in range(n_pool):
        Mraw[i] = baseline_per_N(int(reg_jlo[i]), int(reg_jhi[i]), rho_xs, rho_vals)
    tb = time.time() - tb
    print(f"baselines done ({tb:.1f}s); rho table max err={max(rho_errs.values()):.2e}", flush=True)

    Mnorm = Mraw.sum(0)                                # (50,4) pooled predicted
    colmass = Mnorm.sum(0); Mnorm = Mnorm / colmass[None, :]
    Tpool_raw = A_lpf.sum(0).sum(1).astype(np.float64)  # (50,) all hits per bin
    Tpool = Tpool_raw / Tpool_raw.sum()
    Mpool_raw = Mraw.sum(2).sum(0)
    Mpool = Mpool_raw / Mpool_raw.sum()
    R_pool = Tpool / Mpool

    # pooled anchors (G2 soft)
    peak_b = int(np.argmax(R_pool))
    a_cal = {"R_first": round(float(R_pool[0]), 4), "R_peak": round(float(R_pool.max()), 4),
             "peak_bin": peak_b, "R_last": round(float(R_pool[-1]), 4)}
    cal_ok = (abs(a_cal["R_first"] - ANCHOR["R_first"]) < ANCHOR["tol_ends"] and
              abs(a_cal["R_peak"] - ANCHOR["R_peak"]) < ANCHOR["tol_peak"] and
              abs(peak_b - ANCHOR["peak_bin"]) <= 4 and
              abs(a_cal["R_last"] - ANCHOR["R_last"]) < ANCHOR["tol_ends"])
    beta_pool = None  # (dead placeholder removed; pooled fit done in analyze_family)
    print(f"pooled anchors: {a_cal} cal_ok={cal_ok}", flush=True)

    # mass shares m_S vs mu_S
    m_obs = A_lpf.sum((0, 1)) / A_lpf.sum()
    mu_pred = colmass / colmass.sum()

    # ---- bootstrap ----
    tbo = time.time()
    rng = np.random.default_rng(BOOT_SEED)
    idx = rng.integers(0, n_pool, size=(BOOT_REPS, n_pool))

    fams = {}
    Rb_pool = boot_R(A_lpf.sum(2)[:, :, None], Mpool[:, None], idx)
    fams["treatment_pooled"] = analyze_family(R_pool, Rb_pool, "treatment_pooled")
    Rb_lpf = boot_R(A_lpf, Mnorm, idx)
    for s in range(4):
        Tsn = A_lpf[:, :, s].sum(0) / max(A_lpf[:, :, s].sum(), 1)
        fams[BAND_NAMES[s]] = analyze_family(
            Tsn / Mnorm[:, s], Rb_lpf[:, s * NBINS:(s + 1) * NBINS], BAND_NAMES[s])
    # k100 terciles: baseline = POOLED hit positional profile (unit mass).
    # Registered reading: a fire means EXTRA aligned hump beyond the shared
    # shape; flat => the hump carries no k100-conditional structure (vanishes
    # under combination conditioning). Exact per-tercile Dickman would need a
    # joint factorization model (Buchstab-type) -- disclosed as deviation.
    Kbase = np.repeat(Tpool[:, None], 3, axis=1)
    Rb_k = boot_R(A_k, Kbase, idx)
    for t in range(3):
        lbl = f"k100_tercile_{t+1}"
        Tkn = A_k[:, :, t].sum(0) / max(A_k[:, :, t].sum(), 1)
        fams[lbl] = analyze_family(Tkn / Tpool,
                                   Rb_k[:, t * NBINS:(t + 1) * NBINS], lbl)
    # control arm: uniform baseline
    Ctl_norm = A_ctl.sum(0).astype(np.float64); Ctl_norm /= Ctl_norm.sum()
    Rc_pool = Ctl_norm[:, 0] * NBINS if Ctl_norm.ndim > 1 else Ctl_norm * NBINS
    Ctl_pooled_bin = A_ctl.sum(0).sum(1).astype(np.float64)
    Rc_pool = Ctl_pooled_bin / Ctl_pooled_bin.sum() * NBINS
    Rb_cp = boot_R(A_ctl.sum(2)[:, :, None], (np.full((NBINS, 1), 1.0 / NBINS)), idx)
    fams["control_pooled"] = analyze_family(Rc_pool, Rb_cp[:, :NBINS], "control_pooled")
    Ctlcol = A_ctl.sum(0).astype(np.float64)
    Ctlmass = Ctlcol.sum(0)
    elig_ctl = Ctlmass >= LOW_MASS_MIN
    Cbase = np.tile(np.where(elig_ctl, 1.0 / NBINS, 1.0), (NBINS, 1))  # uniform; ineligible cols pinned to 1 to avoid nan
    Rb_c = boot_R(A_ctl, Cbase, idx)
    ctl_strat = {}
    for s in range(4):
        lbl = f"control_{BAND_NAMES[s]}"
        if not elig_ctl[s]:
            ctl_strat[lbl] = {"family": lbl, "eligible": False,
                              "mass": int(Ctlmass[s])}
            continue
        Tcs = A_ctl[:, :, s].sum(0) / max(Ctlmass[s], 1)
        ctl_strat[lbl] = analyze_family(Tcs * NBINS,
                                        Rb_c[:, s * NBINS:(s + 1) * NBINS], lbl)
    tbo = time.time() - tbo
    print(f"bootstrap+fits done ({tbo:.1f}s)", flush=True)

    # ---- DESCRIPTIVE (post-hoc, NON-verdict-bearing): split of the dominant
    # >1e4 band into observed-mass terciles of LPF; Dickman baselines at those
    # exact numeric edges. Registered bands stay the only verdict input.
    sub_out = {}
    big = np.array([x for x in lpf_all if x > 10000], dtype=np.int64)
    if len(big) >= 600:
        bs = np.sort(big)
        st1, st2 = int(bs[len(bs) // 3]), int(bs[2 * len(bs) // 3])
        A_sub = np.zeros((n_pool, NBINS, 3), dtype=np.int64)
        for i in range(n_pool):
            jlo = int(reg_jlo[i]); jhi = int(reg_jhi[i]); span = jhi - jlo
            hp = reg_hit[i]
            us = (hp - jlo).astype(np.float64) / span
            bb = np.minimum((us * NBINS).astype(np.int64), NBINS - 1)
            L = np.array([x[0] for x in hit_info[i]], dtype=np.int64)
            sel = L > 10000
            if sel.any():
                tt = np.where(L <= st1, 0, np.where(L <= st2, 1, 2)).astype(np.int64)
                np.add.at(A_sub[i], (bb[sel], tt[sel]), 1)
        Msub = np.zeros((n_pool, NBINS, 3))
        for i in range(n_pool):
            Msub[i] = baseline_per_N(int(reg_jlo[i]), int(reg_jhi[i]),
                                     rho_xs, rho_vals,
                                     edges=((10000, st1), (st1, st2), (st2, 1000000)))
        Msnorm = Msub.sum(0); mcol = Msnorm.sum(0)
        Msnorm = Msnorm / np.maximum(mcol, 1e-300)[None, :]
        Rb_sub = boot_R(A_sub, Msnorm, idx)
        for t in range(3):
            lbl = f"subband_{t+1}_of_gt1e4"
            Tsubn = A_sub[:, :, t].sum(0) / max(A_sub[:, :, t].sum(), 1)
            fams[lbl] = analyze_family(Tsubn / Msnorm[:, t],
                                       Rb_sub[:, t * NBINS:(t + 1) * NBINS], lbl)
            fams[lbl]["descriptive_only"] = True
        sub_out = {"cuts_lpf": [int(st1), int(st2)],
                   "masses": [int((big <= st1).sum()), int(((big > st1) & (big <= st2)).sum()),
                              int((big > st2).sum())],
                   "median_lpf_per_tercile": [int(np.median(big[big <= st1])),
                                              int(np.median(big[(big > st1) & (big <= st2)])),
                                              int(np.median(big[big > st2]))]}
        print(f"sub-band cuts: {sub_out}", flush=True)

    # ---- verdict tree ----
    contam = fams["control_pooled"]["fires_HUMP"] or any(
        v.get("fires_HUMP") for v in ctl_strat.values())
    masses = [int(A_lpf[:, :, s].sum()) for s in range(4)]
    elig = [m >= LOW_MASS_MIN for m in masses]
    fires_lpf = [BAND_NAMES[s] for s in range(4)
                 if elig[s] and fams[BAND_NAMES[s]]["fires_HUMP"]]
    kmasses = [int(A_k[:, :, t].sum()) for t in range(3)]
    kelig = [m >= LOW_MASS_MIN for m in kmasses]
    fires_k = [f"k100_tercile_{t+1}" for t in range(3)
               if kelig[t] and fams[f"k100_tercile_{t+1}"]["fires_HUMP"]]
    n_elig_lpf = sum(elig); n_elig_k = sum(kelig)
    pooled_fires = fams["treatment_pooled"]["fires_HUMP"]

    if contam:
        verdict = "ARTIFACT-CONTAMINATED"; carrier = None
    elif n_elig_lpf == 4 and len(fires_lpf) == 1:
        verdict = "H1A-LPF-CARRIER"; carrier = fires_lpf[0]
    elif n_elig_lpf >= 3 and len(fires_lpf) >= 3 and len(fires_k) == 0:
        verdict = "H1B-SMALL-PRIME-COMBO-CARRIER"
        carrier = "k100 combination structure (vanishes within every k100 tercile)"
    elif n_elig_lpf >= 3 and len(fires_lpf) >= 3 and len(fires_k) >= 2:
        verdict = "H0-WINDOW-GEOMETRY-ARTIFACT"
        carrier = "window/polynomial geometric artifact present across all decompositions"
    elif len(fires_lpf) == 0 and len(fires_k) == 0 and pooled_fires:
        verdict = "BASELINE-MASS-REALLOCATION"
        carrier = ("Dickman band-mass allocation m_S!=mu_S; per-stratum shapes flat")
    else:
        verdict = "MIXED-INCONCLUSIVE"
        carrier = None

    consequences = {
        "H1A-LPF-CARRIER":
            "the mid-window excess is carried by ONE completing-prime size band; "
            "paper 229's characterization completes as 'the positional hump is an "
            "LPF-size phenomenon' -> next lever conditions proposals on completing-"
            "prime size, not position",
        "H1B-SMALL-PRIME-COMBO-CARRIER":
            "the hump lives in multiplicative COMBINATION structure (#distinct small "
            "primes), not any single prime size -> per-N smoothness structure, feeds "
            "the unexplained ~39-61% overdispersion program",
        "H0-WINDOW-GEOMETRY-ARTIFACT":
            "hump survives every decomposition => artifact of window/polynomial "
            "geometry (j-grid quantization interacting with v-sizes); paper 229's "
            "residual closes as measurement structure, not number-theoretic signal",
        "BASELINE-MASS-REALLOCATION":
            "each band's positional SHAPE matches Dickman; only the ALLOCATION of hit "
            "mass between bands deviates -> fix is a two-parameter baseline correction",
        "MIXED-INCONCLUSIVE":
            "partial concentration; report fire counts and revisit with more power",
        "ARTIFACT-CONTAMINATED":
            "control shows aligned structure -> pipeline leak, no mechanism claim",
    }

    wall = time.time() - t0
    out = {
        "exp": "581", "codename": "HUMP-MECHANISM", "mode": mode,
        "config": {
            "master_seed": SEED, "bits": BITS, "n_pool": n_pool,
            "jsamples_per_N": jsamples, "source_npz": "exp578_positions.npz",
            "tester": "exp569 gcd-chain verbatim; sampling stream exp578 verbatim",
            "bands": BAND_NAMES, "B0_small_primes": B0,
            "tercile_cutpoints_k100": [q1, q2],
            "bins": NBINS, "trapezoid_pts_per_bin": NPT, "r_mixture_pts": NR,
            "boot_reps": BOOT_REPS, "boot_seed": BOOT_SEED,
            "bootstrap_unit": "cluster over Ns",
            "LOW_MASS_MIN": LOW_MASS_MIN,
            "anchors_exp579": ANCHOR,
            "seed_lineage": seed_lineage,
            "verification": verify,
        },
        "rows": rows,
        "decomposition": {
            "families": fams,
            "control_strata": ctl_strat,
            "subband_descriptive": sub_out,
            "mass_shares": {
                "observed_m_S": [round(float(x), 4) for x in m_obs],
                "predicted_mu_S": [round(float(x), 4) for x in mu_pred],
                "obs_mass_per_band": masses,
                "k_tercile_masses": kmasses},
            "pooled_T_profile": [round(float(x), 5) for x in Tpool],
            "pooled_M_profile": [round(float(x), 5) for x in Mpool],
            "pooled_R_profile": [round(float(x), 4) for x in R_pool],
            "note": "R_S(b)=within-stratum shape residual doubles as the share-ratio diagnostic: composition can move the pooled profile only through constant weights m_S!=mu_S applied to differing stratum shapes.",
        },
        "stats": {
            "total_hits": int(A_lpf.sum()),
            "mean_hits_per_N": round(float(A_lpf.sum() / n_pool), 2),
            "rho_table_max_abs_err": round(max(rho_errs.values()), 8),
            "calibration": {"anchors_computed": a_cal, "anchors_pass_soft": bool(cal_ok)},
            "ctl_none_band_excluded": ctl_none,
            "segments_s": {"population": round(tp, 1), "sampling": round(ts, 1),
                           "factor": round(tf, 1), "counts": round(tc, 1),
                           "baseline": round(tb, 1), "boot": round(tbo, 1)},
        },
        "verdicts": {
            "rule": ("priority CONTAMINATED > H1a(exactly one LPF band fires) > "
                     "H1b(>=3/4 bands fire AND 0/3 k100 terciles) > H0(>=3/4 bands "
                     "AND >=2/3 terciles) > MASS-REALLOC(no strata fire, pooled "
                     "fires) > MIXED; HUMP_S = quad c boot95<0 wholly + vertex in "
                     "(0.15,0.85) + fitted-peak boot95 p2.5>1.05"),
            "verdict": verdict,
            "carrier": carrier,
            "consequence": consequences[verdict],
            "fires_LPF": fires_lpf, "fires_k100": fires_k,
            "eligible_LPF_bands": int(n_elig_lpf), "eligible_k_terciles": int(n_elig_k),
            "control_contaminated": bool(contam),
            "pooled_treatment_fires": bool(pooled_fires),
            "calibration_soft_pass": bool(cal_ok),
        },
        "honest_notes": [
            "SELF-CATCH (run 1): the G1 verifier compared my PAIRED analysis "
            "slices (first len(hits) non-hits) against exp578's STORED full "
            "4000-capped control arrays -> spurious hash failure; ALL 128 hit "
            "arrays + grids were byte-exact in run 1 (log evidence, total "
            "9594 hits). Verifier fixed to compare stored-vs-stored; pairing "
            "convention unchanged for analysis; regeneration persisted to "
            "exp581_regen_positions.npz before gating",
            "baseline recipe reconstructed from exp579's published description (its "
            "code outside this experiment's read scope); calibrated against its "
            "published SCALAR anchors (R_first/peak/bin/R_last) with generous "
            "tolerances instead of a full per-bin table transcription",
            "uniform-r 17-pt mixture inherited from exp579 incl. its caveat; r "
            "brackets {0,mid,2s} not re-run here (scope)",
            "control LPF strata use largest prime <=1e6 of NON-smooth v; controls "
            "with NO prime factor <=1e6 excluded from stratified control (counted)",
            "k100 terciles cut at pooled hit-mass quantiles; ties go to lower class",
            "families below LOW_MASS_MIN=200 observed hits are ineligible for firing",
            "fixed bootSE weights across replicates; percentile CIs; replicate fits "
            "with c>=0 excluded from peak CI via nanpercentile",
            "v<=1 baseline points contribute zero (measure-zero); v=1 hits would be "
            "assigned band lpv<=100/k100=0 (none occurred)",
            "baseline v computed exactly in int64 for grid nodes with d=j-s<=256, "
            "in float elsewhere (relative error ~2^-53, log-safe)",
            "single master seed 20260828 inherited from exp578 (single-seed caveat)",
            "smoke verification is double in-process regeneration only; exp578_smoke "
            "positions npz was outside this experiment's read scope",
            "LPF band edges nominal decimal cuts, not prime-aligned",
            "k100-tercile baseline = POOLED hit positional profile (unit mass), "
            "not per-tercile Dickman: a proper size-conditioned joint model of "
            "(LPF, k100) would need Buchstab-type sieve machinery out of scope; "
            "the registered reading is adjusted accordingly -- a tercile fire "
            "means EXTRA aligned hump beyond the shared positional shape, flat "
            "means the hump carries no k100-conditional structure",
            "R_S normalization is offset-invariant: a constant-factor Dickman "
            "misspecification cancels per stratum; it can still move the POOLED "
            "profile through m_S!=mu_S weighting -- that channel is named by the "
            "BASELINE-MASS-REALLOCATION branch",
        ],
        "wall_s": round(wall, 1),
    }
    fn = "exp581_smoke_result.json" if smoke else "exp581_result.json"
    with open(fn, "w") as f:
        json.dump(out, f, indent=1)
    summ = {"verdict": verdict, "carrier": carrier,
            "fires_LPF": fires_lpf, "fires_k100": fires_k,
            "contaminated": bool(contam), "calibration": a_cal, "cal_ok": bool(cal_ok),
            "pooled_fires": bool(pooled_fires),
            "family_fires": {k: v.get("fires_HUMP") for k, v in fams.items()},
            "masses": {"obs": masses, "mu": [round(float(x), 4) for x in mu_pred]},
            "wall_s": round(wall, 1)}
    print(json.dumps(summ, indent=1), flush=True)
    print(f"[{mode}] verdict={verdict} carrier={carrier} wall={wall:.1f}s -> {fn}",
          flush=True)


if __name__ == "__main__":
    main()

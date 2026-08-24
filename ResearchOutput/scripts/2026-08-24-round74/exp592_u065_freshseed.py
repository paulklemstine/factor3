#!/usr/bin/env python3
# exp592 U065-FRESH-SEED-GATE (round-74; paper-242 map entry gating, FOURTH pass on the u*~0.65 feature)
#
# ============================ PRE-REGISTRATION (written BEFORE any analysis) ============================
# Context: exp588c (MIXTURE-BASELINE, seed lineage 20260828) found the mid-window (peak t*~0.65)
# smoothness-hit excess SURVIVES the divisibility mixture: amp_mix 0.1774 +- 0.0432, registered
# z_mix 4.11, null-calibrated z_cal 1.53 vs CTRL-B. Paper 242 carries this as a NEW MAP ENTRY
# (non-divisibility positional mechanism surviving its mixture) resting on ONE seed lineage.
# Tonight's lab rule demands FRESH-SEED GATING before the claim hardens. THIS experiment reruns
# the IDENTICAL pipeline on an INDEPENDENT lineage and applies two pre-named gates.
#
# GATES (fixed NOW, before any fresh-seed number exists; evaluated in order H1 -> H0 -> PARTIAL):
#   GATE-H1 (feature replicates): fresh-seed amp_mix >= 1.0 * se_mix  AND  null-calibrated
#     z_cal >= 2  =>  non-divisibility mechanism CONFIRMED TWO-SEED; paper-242 entry HARDENS.
#   GATE-H0 (fails to replicate): bootstrap 95% CI of amp_mix includes 0  OR  z_cal < 1
#     =>  entry stays SINGLE-SEED-UNCONFIRMED; the original z=4.11 is FLAGGED as possibly
#     inflated by max-statistic selection across the sweep.
#   Neither gate => PARTIAL band: entry stays single-seed-unconfirmed (no inflation flag).
#   Units fixed NOW: "amp >= 1.0" reads as multiples of the registered cluster-bootstrap se_mix
#   (i.e. registered raw z_mix = amp_mix/se_mix >= 1); CI = 2.5/97.5 percentiles of the 2000-rep
#   N-resample bootstrap distribution of amp_mix; z_mix = amp_mix/se_mix is the REGISTERED RAW
#   scale, z_cal = (amp_mix-amp_sim)/sqrt(se_mix^2+se_sim^2) vs CTRL-B is the NULL-CALIBRATED
#   scale (paper-242 caveat honored: BOTH scales reported going forward; disagreement flagged,
#   never resolved).
#
# Method (statistics VERBATIM exp588c MIXTURE-BASELINE; generation VERBATIM exp578 code path):
#  1. FRESH MASTER SEED 20260902 (distinct from 20260824/25/26/27/28/31 lineages; hash recorded).
#     Population = 128 balanced bitlen-96 semiprimes via exp578 code path verbatim
#     (random.Random(master), getrandbits(48)|top|1 -> next_prime, q!=p retry, bitlen/balance
#     retries); window jlo=isqrt(N)+1, jhi=3*isqrt(N); per-chunk rng(master+7000+c), 8 chunks x
#     16 N, SEQUENTIAL 150k-draw replay, ONE rng per chunk (exp578 worker semantics); exp569
#     gcd-chain tester (cut 1e6, P5->P6) classifies hits; paired non-hits capped 4000/N
#     first-in-stream. Positions persisted to exp592_positions.npz.
#  2. GENERATOR VALIDATION, gated BEFORE statistics (in-process lineage has no stored npz to
#     regress, so the GENERATOR ITSELF is regressed):
#     (a) the same generator code at master 20260828 must reproduce the stored
#         exp581_regen_positions.npz windows INT64-EXACTLY (all 128 Ns) and walk chunk 0's
#         stored stream in ORDER (membership + order, the proven exp588b-A3 checks);
#     (b) FRESHNESS = pairwise-DISJOINT N sets vs ALL SIX prior lineages (20260824..28, 20260831),
#         each regenerated in full; hashes recorded.
#     Any validation failure => statistics ABORT (degraded status only).
#  3. Mixture statistics verbatim exp588c: 16 cells = divisibility pattern (2|v,3|v,5|v,7|v),
#     v=j^2-N, via modular arithmetic; PRED(b)=sum_c kappa_c*S_c(b) with S_c = Dickman-weighted
#     reference sums (lnB=ln(1e6) FIXED), kappa_c fit on FLANKS ONLY (t<0.40|t>0.85, lam=5
#     shrinkage toward global rate); nb=50 bins, 3-bin smoothing; score window t=[0.55,0.75]
#     EXCLUDED from estimation; buffer bins predicted, not fitted, not scored.
#     amp_mix = max over score bins of smoothed(observed/PRED) - 1; cluster bootstrap SE
#     (resample the 128 Ns, 2000 reps, seed_boot 20260901 exp588c convention).
#  4. Controls: CTRL-A machinery (paired random halves of the non-hit stream, COUNT-vs-COUNT,
#     MUST be null: amp<3*se AND amp<0.10 AND max-bin |ratio-1|<0.10 over ALL bins) else
#     ARTIFACT-CONTAMINATED; CTRL-B parametric Poisson on the rho-weighted expectation
#     (estimator null incl. max-over-bins bias) => amp_sim, se_sim, z_cal.
#  5. BOTH scales reported: registered raw z_mix AND null-calibrated z_cal; gates applied as above.
# Smoke: reduced grid (24 Ns, 20k samples/N, 4x6 chunking, 1200-ctl cap, 200 boot reps) <30 s.
# Full <=12 min.
# Output: exp592_u065_freshseed.py / exp592_smoke.log / exp592_result.json / findings.md.
# AMENDMENT LOG: none (pre-registration completed before any fresh-seed number existed).
# =======================================================================================================
import sys, os, json, time, hashlib, math, random
import numpy as np
import gmpy2
from gmpy2 import mpz, next_prime
from gmpy2 import gcd as mpgcd
from multiprocessing import Pool

BASE = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74"
NPZ_REF = f"{BASE}/exp581_regen_positions.npz"
SMOKE = "--smoke" in sys.argv
MASTER_SEED = 20260902                      # FRESH MASTER SEED (lab rule)
PRIOR_SEEDS = (20260824, 20260825, 20260826, 20260827, 20260828, 20260831)
assert MASTER_SEED not in PRIOR_SEEDS
NS_FULL = 128
NS = 24 if SMOKE else NS_FULL
JS_FULL = 150000
JS = 20000 if SMOKE else JS_FULL            # smoke is plumbing/calibration only (exp578 precedent)
NCHUNK = 4 if SMOKE else 8                  # full chunking FIXED at 8x16 = exp578 full semantics
PER = NS // NCHUNK                          # 6 (smoke) / 16 (full)
JCAP_CONTROL = 4000
SEED_BOOT = 20260901                        # exp582/588b/588c bootstrap convention (kept)
NB_REP = 200 if SMOKE else 2000
NB = 50
SCORE_WIN = (0.55, 0.75)                    # REGISTERED score window (brief)
WIDE_WIN = (0.45, 0.85)                     # exp588b comparability window (secondary)
FLK_LO, FLK_HI = 0.40, 0.85                 # flank definition (brief)
LNB_FIXED = math.log(1e6)                   # exp578 CUT_BIG, known
LAM = 5.0                                   # kappa shrinkage pseudo-counts (pre-registered)
PRIMES = (2, 3, 5, 7)
NCELL = 16
CUT_SMALL, CUT_BIG = 100000, 1000000

t0 = time.time()
def wall(): return round(time.time()-t0, 1)

# ---------------- Dickman rho (verbatim exp588c) ----------------
def dickman_table(umax=36.0, du=2e-3):
    n = int(umax/du)+2
    u = np.arange(n)*du; rho = np.empty(n)
    rho[u <= 1.0] = 1.0
    for k in range(np.searchsorted(u, 1.0), n):
        rho[k] = rho[k-1] - du*rho[int(round((u[k]-1)/du))]/u[k]
    return u, np.maximum(rho, 1e-300)
DT_U, DT_R = dickman_table()
rho_at = lambda x: np.interp(np.clip(x, 0, DT_U[-1]), DT_U, DT_R)

# ---------------- exp578 code path VERBATIM ----------------
def build_primorial(bound):
    p = mpz(1); q = mpz(2)
    while q <= bound:
        p *= q; q = next_prime(q)
    return p

def make_semiprime_v(rng, bits=96):
    half = bits//2
    def gen():
        x = rng.getrandbits(half) | (1 << (half-1)) | 1
        return int(next_prime(mpz(x)))
    p = gen(); q = gen()
    while q == p: q = gen()
    n = p*q
    if n.bit_length() != bits: return make_semiprime_v(rng, bits)
    lo, hi = min(p, q), max(p, q)
    if hi.bit_length()-lo.bit_length() > 2: return make_semiprime_v(rng, bits)
    return n

def build_pop_v(seed, n_pool):
    rng = random.Random(seed); pools = []; seen = set()
    while len(pools) < n_pool:
        N = make_semiprime_v(rng)
        if N in seen: continue
        seen.add(N); pools.append(N)
    return pools

def pop_sha16(pools_or_set):
    xs = sorted(pools_or_set)
    return hashlib.sha256(repr(xs).encode()).hexdigest()[:16]

_G = {}
def init_worker(p5, p6):
    _G["P5"] = mpz(p5); _G["P6"] = mpz(p6)

def classify(v):
    """VERBATIM exp569 tester (cut 1e6, P5->P6): True iff v is 1e6-smooth."""
    xx = mpz(v)
    P5, P6 = _G["P5"], _G["P6"]
    while xx > 1:
        g = mpgcd(xx, P5)
        if g == 1: break
        xx //= g
    if xx == 1: return True
    xy = xx
    while xy > 1:
        g = mpgcd(xy, P6)
        if g == 1: break
        xy //= g
    return xy == 1

def worker(args):
    """VERBATIM exp578 worker semantics: one rng per chunk, sequential across its Ns."""
    ns, jsamples, seed = args
    rng = random.Random(seed)
    out = []
    for (N, jl, jh) in ns:
        hp = []; nh = []
        for _ in range(jsamples):
            j = rng.randint(jl, jh)
            v = j*j - N
            if v <= 1: continue
            if classify(v):
                hp.append(j)
            elif len(nh) < JCAP_CONTROL:
                nh.append(j)
        out.append((hp, nh))
    return out

# ---------------- STEP 2a: generator regression vs stored 20260828 lineage ----------------
P5B = build_primorial(CUT_SMALL); P6B = build_primorial(CUT_BIG)
print(f"[primorials] P5 bits={P5B.bit_length()} P6 bits={P6B.bit_length()} wall={wall()}", flush=True)
print("[xcheck] validating generator vs exp581_regen_positions.npz (master 20260828)...", flush=True)
XCHECK = {"status": None, "checks": {}}
pools28 = None
try:
    ref = np.load(NPZ_REF, allow_pickle=True)
    pools28 = build_pop_v(20260828, NS_FULL)
    s_arr = [int(gmpy2.isqrt(mpz(n))) for n in pools28]
    jl_pred = np.array([s+1 for s in s_arr], dtype=np.int64)
    jh_pred = np.array([3*s for s in s_arr], dtype=np.int64)
    ok_win = bool(np.array_equal(jl_pred, ref["jlo"].astype(np.int64)) and
                  np.array_equal(jh_pred, ref["jhi"].astype(np.int64)))
    XCHECK["checks"]["population_window_exact_vs_npz"] = ok_win
    walk_n = 6 if SMOKE else 16                       # chunk 0 of the 20260828 lineage (per=16)
    ok_m = True; ok_o = True
    rng = random.Random(20260828+7000+0)
    for i in range(walk_n):
        s = s_arr[i]; a = s+1; b = 3*s
        draws = [rng.randint(a, b) for _ in range(JS_FULL)]
        ds = set(draws)
        hi = np.concatenate([ref[f"hit_{i}"], ref[f"ctl_{i}"]])
        if not all(int(x) in ds for x in hi): ok_m = False
        ph = pn = 0
        hpl = ref[f"hit_{i}"].tolist(); nhl = ref[f"ctl_{i}"].tolist()
        for jv in draws:
            if ph < len(hpl) and jv == hpl[ph]: ph += 1
            elif pn < len(nhl) and jv == nhl[pn]: pn += 1
        if not (ph == len(hpl) and pn == len(nhl)): ok_o = False
    XCHECK["checks"]["chunk0_walk_ns"] = walk_n
    XCHECK["checks"]["stream_membership_and_order_exact"] = bool(ok_m and ok_o)
    XCHECK["status"] = "EXACT_MATCH" if (ok_win and ok_m and ok_o) else "MISMATCH"
    del ref
except Exception as e:
    XCHECK["status"] = f"ERROR:{type(e).__name__}"
print(f"[xcheck] status={XCHECK['status']} win={XCHECK['checks'].get('population_window_exact_vs_npz')} "
      f"stream={XCHECK['checks'].get('stream_membership_and_order_exact')} wall={wall()}", flush=True)

# ---------------- STEP 2b: freshness (disjointness vs all six prior lineages) ----------------
print("[fresh] regenerating prior lineages for disjointness assertion...", flush=True)
FRESH = {"status": None, "disjoint_vs": {}, "hashes": {}}
try:
    fresh_pools = build_pop_v(MASTER_SEED, NS_FULL)
    fresh_set = set(fresh_pools)
    FRESH["hashes"][str(MASTER_SEED)] = pop_sha16(fresh_set)
    for s in PRIOR_SEEDS:
        ps = set(pools28) if s == 20260828 and pools28 is not None else set(build_pop_v(s, NS_FULL))
        FRESH["disjoint_vs"][str(s)] = bool(fresh_set.isdisjoint(ps))
        FRESH["hashes"][str(s)] = pop_sha16(ps)
    FRESH["status"] = "ALL_DISJOINT" if all(FRESH["disjoint_vs"].values()) else "COLLISION"
except Exception as e:
    FRESH["status"] = f"ERROR:{type(e).__name__}"
print(f"[fresh] status={FRESH['status']} disjoint={FRESH['disjoint_vs']} wall={wall()}", flush=True)

GEN_OK = (XCHECK["status"] == "EXACT_MATCH") and (FRESH["status"] == "ALL_DISJOINT")

# ---------------- STEP 1: generate the fresh lineage ----------------
HITS = [None]*NS; CTLS = [None]*NS
jlo = np.zeros(NS, dtype=np.int64); jhi = np.zeros(NS, dtype=np.int64)
GEN = {"status": "SKIPPED"}
if GEN_OK:
    try:
        s_arr_f = [int(gmpy2.isqrt(mpz(n))) for n in fresh_pools[:NS]]
        jlo = np.array([s+1 for s in s_arr_f], dtype=np.int64)
        jhi = np.array([3*s for s in s_arr_f], dtype=np.int64)
        chunks = []
        for c in range(NCHUNK):
            sl = fresh_pools[c*PER:(c+1)*PER]
            ns_list = [(int(n), int(gmpy2.isqrt(mpz(n)))+1, 3*int(gmpy2.isqrt(mpz(n)))) for n in sl]
            chunks.append((ns_list, JS, MASTER_SEED+7000+c))
        print(f"[gen] {NCHUNK} workers x {PER} N x {JS} j-samples (master {MASTER_SEED})...", flush=True)
        tg = time.time()
        with Pool(NCHUNK, initializer=init_worker, initargs=(P5B, P6B)) as pl:
            res = pl.map(worker, chunks)
        flat = [r for chunk in res for r in chunk]
        print(f"[gen] done ({time.time()-tg:.1f}s) wall={wall()}", flush=True)
        for i, (hp, nh) in enumerate(flat):
            HITS[i] = np.array(hp, dtype=np.int64)
            CTLS[i] = np.array(nh, dtype=np.int64)
        if SMOKE:
            CTLS = [cc[:1200] for cc in CTLS]         # exp588c smoke cap convention
        GEN["status"] = "OK"
        GEN["mean_hits_per_N"] = round(float(np.mean([len(h) for h in HITS])), 2)
        GEN["total_hits"] = int(sum(len(h) for h in HITS))
        GEN["total_reference_stored"] = int(sum(len(c) for c in CTLS))
        # persist positions (reconstructible; exp592_* artifact)
        arrs = {}
        for i in range(NS):
            arrs[f"hit_{i}"] = HITS[i]; arrs[f"ctl_{i}"] = CTLS[i]
        npz_name = "exp592_smoke_positions.npz" if SMOKE else "exp592_positions.npz"
        np.savez_compressed(f"{BASE}/{npz_name}", **arrs, jlo=jlo, jhi=jhi)
        GEN["positions_npz"] = npz_name
        hh = hashlib.sha256()
        for i in range(NS):
            hh.update(HITS[i].tobytes()); hh.update(CTLS[i].tobytes())
        hh.update(jlo.tobytes()); hh.update(jhi.tobytes())
        GEN["sha256_positions"] = hh.hexdigest()
    except Exception as e:
        GEN["status"] = f"ERROR:{type(e).__name__}:{e}"
print(f"[gen] status={GEN.get('status')} wall={wall()}", flush=True)

HAVE_N = GEN_OK and (GEN["status"] == "OK")
if not HAVE_N:
    print("[abort] generation/validation failed; statistics ABORT (degraded status only)", flush=True)

# ---------------- STEP 3: mixture statistics (VERBATIM exp588c) ----------------
edges = np.linspace(0, 1, NB+1); CTR = (edges[:-1]+edges[1:])/2
bidx = lambda t: np.clip(np.digitize(t, edges)-1, 0, NB-1)
FL_BINS  = np.where((CTR < FLK_LO) | (CTR > FLK_HI))[0]
SCORE_BINS = np.where((CTR >= SCORE_WIN[0]) & (CTR <= SCORE_WIN[1]))[0]
WIDE_BINS  = np.where((CTR >= WIDE_WIN[0]) & (CTR <= WIDE_WIN[1]))[0]

HN = np.zeros((NS, NB, NCELL)); SN = np.zeros((NS, NB, NCELL))
CN = np.zeros((NS, NB, NCELL))
BC_I = [None]*NS; W_I = [None]*NS
if HAVE_N:
    for i in range(NS):
        Ni = fresh_pools[i]; jl = int(jlo[i]); jh = int(jhi[i])
        Nmod = np.array([Ni % m for m in PRIMES], dtype=np.int64)
        c = CTLS[i]
        tj = (c - jl)/(jh - jl); b = bidx(tj).astype(np.int64)
        cell = np.zeros(len(c), dtype=np.int64)
        for k, m in enumerate(PRIMES):
            jm = c % m
            bit = (((jm*jm) - Nmod[k]) % m) == 0
            cell |= bit.astype(np.int64) << k
        v_exact = [int(x)*int(x) - Ni for x in c]           # EXACT int subtraction (cancellation-safe)
        lv = np.log(np.maximum(np.array(v_exact, dtype=np.float64), 1.0))
        w = rho_at(lv/LNB_FIXED)
        bc = b*NCELL + cell
        SN[i] = np.bincount(bc, weights=w, minlength=NB*NCELL).reshape(NB, NCELL)
        CN[i] = np.bincount(bc, minlength=NB*NCELL).reshape(NB, NCELL)
        BC_I[i] = bc; W_I[i] = w
        h = HITS[i]
        th = (h - jl)/(jh - jl); bh = bidx(th).astype(np.int64)
        cellh = np.zeros(len(h), dtype=np.int64)
        for k, m in enumerate(PRIMES):
            jm = h % m
            bit = (((jm*jm) - Nmod[k]) % m) == 0
            cellh |= bit.astype(np.int64) << k
        HN[i] = np.bincount(bh*NCELL + cellh, minlength=NB*NCELL).reshape(NB, NCELL)
print(f"[tensors] built wall={wall()}", flush=True)

# ---------------- amplitude machinery (verbatim exp588c) ----------------
def smooth(R):
    Rs = np.convolve(R, np.ones(3)/3, mode="same")
    Rs[0], Rs[-1] = R[0], R[-1]
    return Rs

def fit_kappa(H, S):
    Hf = H[FL_BINS].sum(0); Sf = S[FL_BINS].sum(0)
    g = Hf.sum()/max(Sf.sum(), 1e-300)
    kap = (Hf + LAM*g)/(Sf + LAM)
    return kap, g, Hf, Sf

def ratios_of(H, S):
    kap, g, Hf, Sf = fit_kappa(H, S)
    PRED = (kap[None, :]*S).sum(1)
    HCt = H.sum(1)
    R = HCt/np.maximum(PRED, 1e-300)
    return smooth(R), R, kap, g, Hf, Sf, PRED

def amp_of(H, S, bins):
    Rs, _, _, _, _, _, _ = ratios_of(H, S)
    return float(max(Rs[bins].max()-1.0, 0.0))

verdicts = {}; stats = {}; rows_out = []; KAP_SORTED = []; DRIFT = float("nan"); GFIT = float("nan")
if HAVE_N:
    HC = HN.sum(0); STOT = SN.sum(0)
    RS_ALL, R_ALL, KAP, GFIT, HF_T, SF_T, PRED_ALL = ratios_of(HC, STOT)
    AMP_MIX = float(max(RS_ALL[SCORE_BINS].max()-1.0, 0.0))
    AMP_MIX_WIDE = float(max(RS_ALL[WIDE_BINS].max()-1.0, 0.0))
    Af = HC[FL_BINS].sum()/max(STOT[FL_BINS].sum(), 1e-300)
    BASE_VEC = Af*STOT.sum(1)
    R_o = HC.sum(1)/np.maximum(BASE_VEC, 1e-300); RS_O = smooth(R_o)
    AMP_ORIG = float(max(RS_O[SCORE_BINS].max()-1.0, 0.0))

    ns_ = NS
    def boot_dist(fn, B):
        rng = np.random.default_rng(SEED_BOOT)
        return np.array([fn(rng.integers(0, ns_, ns_)) for _ in range(B)])
    def amp_mix_fn(idx): return amp_of(HN[idx].sum(0), SN[idx].sum(0), SCORE_BINS)
    def amp_orig_fn(idx):
        Hs = HN[idx].sum(0); Ss = SN[idx].sum(0)
        A = Hs.sum()/max(Ss[FL_BINS].sum(), 1e-300)
        Rr = Hs.sum(1)/np.maximum(A*Ss.sum(1), 1e-300)
        return float(max(smooth(Rr)[SCORE_BINS].max()-1.0, 0.0))
    tb = time.time()
    D_MIX = boot_dist(amp_mix_fn, NB_REP)
    SE_MIX = float(np.std(D_MIX, ddof=1))
    CI_LO, CI_HI = (float(x) for x in np.percentile(D_MIX, [2.5, 97.5]))
    D_ORIG = boot_dist(amp_orig_fn, NB_REP)
    SE_ORIG = float(np.std(D_ORIG, ddof=1))
    Z_MIX = AMP_MIX/max(SE_MIX, 1e-12)
    REMOVAL = float(np.clip(100*(1-AMP_MIX/AMP_ORIG), 0, 100)) if AMP_ORIG > 0 else float("nan")
    print(f"[mix] amp_mix={AMP_MIX:.4f} se={SE_MIX:.4f} z_raw={Z_MIX:.2f} "
          f"ci95=[{CI_LO:.4f},{CI_HI:.4f}] amp_orig={AMP_ORIG:.4f} removal={REMOVAL:.1f}% "
      f"wall={wall()} (boot {time.time()-tb:.1f}s)", flush=True)

    # ---- CTRL-A: paired random halves, count-vs-count (verbatim exp588c) ----
    rngc = np.random.default_rng(7000)
    CAc = np.zeros((NS, NB, NCELL)); CBc = np.zeros((NS, NB, NCELL))
    for i in range(NS):
        n = len(BC_I[i]); perm = rngc.permutation(n); k = n//2
        ia, ib = perm[:k], perm[k:]
        CAc[i] = np.bincount(BC_I[i][ia], minlength=NB*NCELL).reshape(NB, NCELL)
        CBc[i] = np.bincount(BC_I[i][ib], minlength=NB*NCELL).reshape(NB, NCELL)
    RSA, _, _, _, _, _, _ = ratios_of(CAc.sum(0), CBc.sum(0))
    AMP_CTLA = float(max(RSA[SCORE_BINS].max()-1.0, 0.0))
    MAXDEV_CTLA = float(np.abs(RSA-1.0).max())
    def amp_ctla_fn(idx): return amp_of(CAc[idx].sum(0), CBc[idx].sum(0), SCORE_BINS)
    SE_CTLA = float(np.std(boot_dist(amp_ctla_fn, NB_REP), ddof=1))
    CTRL_PASS = bool(AMP_CTLA < 3*max(SE_CTLA, 1e-9) and AMP_CTLA < 0.10 and MAXDEV_CTLA < 0.10)
    # ---- CTRL-B: parametric Poisson on rho-weighted expectation (verbatim exp588c) ----
    rngp = np.random.default_rng(20260830)
    SIM_HN = rngp.poisson(GFIT*SN).astype(float)
    AMP_SIM = amp_of(SIM_HN.sum(0), SN.sum(0), SCORE_BINS)
    def amp_sim_fn(idx): return amp_of(SIM_HN[idx].sum(0), SN[idx].sum(0), SCORE_BINS)
    SE_SIM = float(np.std(boot_dist(amp_sim_fn, NB_REP), ddof=1))
    Z_CAL = (AMP_MIX-AMP_SIM)/math.sqrt(SE_MIX**2+SE_SIM**2) if (SE_MIX+SE_SIM) > 0 else float("nan")
    SE_COMB = math.sqrt(SE_MIX**2+SE_SIM**2)
    CAL_DELTA = AMP_MIX-AMP_SIM
    print(f"[ctrlA] amp={AMP_CTLA:.4f} se={SE_CTLA:.4f} maxdev={MAXDEV_CTLA:.4f} pass={CTRL_PASS} | "
          f"[ctrlB] amp_sim={AMP_SIM:.4f} se_sim={SE_SIM:.4f} z_cal={Z_CAL:.2f} wall={wall()}", flush=True)

    cnt_mid = CN[:, SCORE_BINS, :].sum(1); cnt_flk = CN[:, FL_BINS, :].sum(1)
    w_mid = cnt_mid.sum(0)/max(cnt_mid.sum(), 1); w_flk = cnt_flk.sum(0)/max(cnt_flk.sum(), 1)
    DRIFT = float(np.abs(w_mid-w_flk).max())
    for ci in range(NCELL):
        pat = "".join(str((ci >> k) & 1) for k in range(4))
        KAP_SORTED.append({"cell": f"2:{pat[0]},3:{pat[1]},5:{pat[2]},7:{pat[3]}",
                           "flank_hits": int(HF_T[ci]), "flank_rho_sum": round(float(SF_T[ci]), 2),
                           "kappa": round(float(KAP[ci]), 5),
                           "kappa_over_g": round(float(KAP[ci]/GFIT), 4),
                           "w_mid": round(float(w_mid[ci]), 4), "w_flank": round(float(w_flk[ci]), 4)})
    KAP_SORTED.sort(key=lambda r: -r["kappa_over_g"])

    # ---------------- PRE-REGISTERED GATES (header; evaluated H1 -> H0 -> PARTIAL) ----------------
    GATE_H1 = bool(CTRL_PASS and AMP_MIX >= 1.0*SE_MIX - 1e-12 and Z_CAL >= 2.0)
    GATE_H0 = bool(CTRL_PASS and ((CI_LO <= 0.0) or (Z_CAL < 1.0)))
    if not CTRL_PASS:
        VERDICT = "ARTIFACT-CONTAMINATED: CTRL-A machinery null violated; no gate verdict"
        CONSEQ = "pipeline contaminated; fresh-seed gate inconclusive"
    elif GATE_H1:
        VERDICT = ("GATE-H1 PASS: FEATURE REPLICATES ON FRESH SEED -> NON-DIVISIBILITY MECHANISM "
                   "CONFIRMED TWO-SEED; PAPER-242 MAP ENTRY HARDENS")
        CONSEQ = "entry hardens"
    elif GATE_H0:
        VERDICT = ("GATE-H0: FEATURE DOES NOT REPLICATE -> ENTRY STAYS SINGLE-SEED-UNCONFIRMED; "
                   "ORIGINAL z=4.11 FLAGGED POSSIBLY-INFLATED BY MAX-STATISTIC SWEEP SELECTION")
        CONSEQ = "entry stays single-seed-unconfirmed; original flagged"
    else:
        VERDICT = ("PARTIAL: NEITHER PRE-REGISTERED GATE FIRES (intermediate band) -> ENTRY STAYS "
                   "SINGLE-SEED-UNCONFIRMED (no inflation flag)")
        CONSEQ = "entry stays single-seed-unconfirmed"
    stats = {
        "amp_mix": AMP_MIX, "se_mix": SE_MIX,
        "z_mix_registered_raw": Z_MIX,
        "amp_ci95_pctile": [CI_LO, CI_HI],
        "calibrated_excess_amp_minus_sim": CAL_DELTA, "se_combined_cal_scale": SE_COMB,
        "z_null_calibrated": Z_CAL,
        "amp_mix_wide": AMP_MIX_WIDE, "amp_orig_single_alpha": AMP_ORIG, "se_orig": SE_ORIG,
        "removal_pct": REMOVAL,
        "amp_ctla_machinery": AMP_CTLA, "se_ctla": SE_CTLA, "ctla_maxdev_all_bins": MAXDEV_CTLA,
        "control_pass": CTRL_PASS,
        "amp_sim_estimator_null": AMP_SIM, "se_sim": SE_SIM,
        "total_hits": int(HC.sum()), "total_reference": int(CN.sum()),
        "g_global_flank_rate": round(float(GFIT), 6), "composition_drift_max_c": DRIFT,
        "kappa_table_sorted_by_kappa_over_g": KAP_SORTED,
    }
    verdicts = {
        "gate_h1_fires": GATE_H1, "gate_h0_fires": GATE_H0,
        "rule": ("GATE-H1 iff amp_mix>=1.0*se_mix AND z_cal>=2 (=> confirmed two-seed, entry "
                 "hardens); else GATE-H0 iff amp CI includes 0 OR z_cal<1 (=> single-seed-"
                 "unconfirmed, original z=4.11 flagged possibly-max-statistic-inflated); else "
                 "PARTIAL; CTRL-A must be null"),
        "gate_evaluation_order": "H1 -> H0 -> PARTIAL",
        "verdict": VERDICT, "consequence": CONSEQ,
        "amp_mix_round": round(AMP_MIX, 4), "se_mix_round": round(SE_MIX, 4),
        "z_mix_registered_raw_round": round(Z_MIX, 2),
        "z_null_calibrated_round": round(Z_CAL, 2) if Z_CAL == Z_CAL else None,
    }
else:
    verdicts = {"verdict": f"NO STATISTICS: {'xcheck='+XCHECK['status']+' fresh='+FRESH['status']+' gen='+GEN.get('status','?')}"}

for bb in range(NB):
    rows_out.append({"bin": bb, "t": round(float(CTR[bb]), 3),
                     "hits": int(HC[bb].sum()) if HAVE_N else 0,
                     "pred_mix": round(float(PRED_ALL[bb]), 2) if HAVE_N else None,
                     "ratio_mix_smooth": round(float(RS_ALL[bb]), 4) if HAVE_N else None,
                     "ratio_orig": round(float(R_o[bb]), 4) if HAVE_N else None})

RESULT = {
 "config": {
  "exp": "exp592", "codename": "U065-FRESH-SEED-GATE", "smoke": SMOKE,
  "nsamples": NS, "jsamples_per_N": JS, "nbins": NB, "ncells": NCELL,
  "chunks": f"{NCHUNK}x{PER}", "boot_reps": NB_REP, "seed_boot": SEED_BOOT,
  "master_seed_fresh": MASTER_SEED,
  "master_seed_distinct_from": list(PRIOR_SEEDS),
  "score_window": list(SCORE_WIN), "flanks": "t<0.40|t>0.85",
  "wide_comparability_window": list(WIDE_WIN), "kappa_shrinkage_lam": LAM,
  "lnB_fixed": round(LNB_FIXED, 4), "control_cap_per_N": JCAP_CONTROL,
  "generator": "exp578 code path verbatim (make_semiprime/build_pop/worker semantics)",
  "tester": "exp569 gcd-chain verbatim (cut 1e6, P5->P6)",
  "generator_regression_vs_exp581_npz": XCHECK,
  "freshness_disjointness": FRESH,
  "generation": GEN,
  "model": ("PRED(b)=sum_c kappa_c*S_c(b); S_c=Dickman-weighted reference samples; kappa_c "
            "flank-only fit with lam-shrinkage to global rate; verbatim exp588c"),
  "amendment_log": ["none (pre-registration completed before any fresh-seed number existed)"],
 },
 "regression": {"xcheck_status": XCHECK["status"], "freshness_status": FRESH["status"],
                "gen_status": GEN.get("status"), "abort_before_statistics": not HAVE_N},
 "residual": {"rows": rows_out, "score_bins_t": [round(float(CTR[b]), 3) for b in SCORE_BINS]},
 "stats": stats,
 "verdicts": verdicts,
 "honest_notes": [
  "In-process fresh lineage: there is NO stored npz to regress, so the GENERATOR itself was "
  "regressed against the stored exp581/exp588c lineage (master 20260828): population windows "
  "INT64-exact for all 128 Ns + chunk-0 stream membership/order walk (proven exp588b-A3 checks); "
  "statistics gated on EXACT_MATCH.",
  "Smoothness spot-validation (exp588c full-mode item) dropped as VACUOUS in-process: hits are "
  "DEFINED by the same tester that would 'validate' them; disclosed deviation, no information lost.",
  "Freshness = pairwise-disjoint N sets vs ALL SIX prior lineages (20260824..28, 20260831), each "
  "regenerated in full; sha256[:16]-of-sorted-N-repr hashes recorded for every lineage (own "
  "convention; exp578's triple-based pop_hash needs lo/hi which build_pop_v discards).",
  "Gate units fixed pre-data: 'amp >= 1.0' = multiples of registered cluster-bootstrap se_mix; "
  "CI = percentile bootstrap; both scales (registered raw z_mix, null-calibrated z_cal vs CTRL-B) "
  "reported per the paper-242 caveat; gates evaluated H1 first, then H0, then PARTIAL.",
  "Max-over-bins amplitude is positively biased under the null; CTRL-B measures that null; "
  "registered amp-vs-SE-derived gate stays verdict-bearing; disagreement flagged, never resolved.",
  "Reference stream = capped non-hits (<=4000/N, first-in-stream); unbiased for uniform sampling "
  "composition, disclosed subsample (as exp588c). Bit 0 (2|v) is identically j-parity since N odd.",
  "ln v computed from EXACT integer v then float-converted (float j^2-N cancels catastrophically "
  "near t=0); Dickman table/interpolation identical to exp588c.",
  "Buffer bins (CTR 0.41-0.54, 0.76-0.85) are predicted but neither fitted nor scored (brief windows).",
  "Smoke mode (if run) is plumbing/calibration only: 24 Ns, 20k samples/N, 4x6 chunking (NOT the "
  "full 8x16 stream layout), 1200-ctl cap, 200 boot reps.",
 ],
 "wall_s": wall()}
out_json = "exp592_smoke_result.json" if SMOKE else "exp592_result.json"
with open(f"{BASE}/{out_json}", "w") as f:
    json.dump(RESULT, f, indent=1, default=float)
print(json.dumps(verdicts, indent=1))
print("WALL", wall())

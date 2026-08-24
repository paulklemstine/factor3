#!/usr/bin/env python3
# exp588c MIXTURE-BASELINE (round-74; paper-241 routed refinement, THIRD pass on the u*~0.65 feature)
#
# ============================ PRE-REGISTRATION (written BEFORE any analysis) ============================
# Context: exp588b found NO single binary carrier (parity / v%3 / v%5 / v%7 / omega100-tercile /
# gcd>1) absorbs the shift-invariant mid-window excess (peak t*~0.65) of j^2-N smoothness; paper 241
# routed to a divisibility-MIXTURE baseline. Question settled HERE: does modeling the expected hit
# profile as composition-weighted per-class rates absorb the excess?
#
# Model (FIXED before any number was seen):
#   16 cells = divisibility pattern (2|v, 3|v, 5|v, 7|v) of v = j^2 - N.
#   Predicted bin count  PRED(b) = sum_c kappa_c * S_c(b),
#     S_c(b) = sum over REFERENCE (non-hit) samples x in bin b with cell c of rho(u_x),
#     u_x = ln(v_x)/ln(1e6)  (lnB FIXED = ln(exp578 CUT_BIG), known), rho = Dickman.
#     kappa_c fit on FLANKING bins ONLY (t<0.40 or t>0.85; score window EXCLUDED from estimation):
#       kappa_c = (Hf_c + lam*g)/(Sf_c + lam),  Hf_c/Sf_c = flank hits / flank Dickman sum in cell c,
#       g = global flank hit rate per Dickman unit, lam = 5 pseudo-count shrinkage (rare cells).
#   This equals "expected profile = sum_cells w_cell(x) * rate_cell(x)": local composition w_c(b)
#   enters through the reference-sample cell mix; rate_cell = kappa_c * rho(u) is flank-estimated.
#
# H1 (mixture closes the channel): post-mixture residual peak amplitude
#     amp_mix = max_{score bins} 3-bin-smoothed(observed/PRED) - 1,  score window t in [0.55,0.75]
#   falls BELOW its cluster bootstrap SE (resample the 128 Ns, 2000 reps, seed 20260901)
#     => CHANNEL CLOSES (the u*~0.65 feature was divisibility-composition all along).
# H0 (excess survives): amp_mix >= 2*SE_mix
#     => structure BEYOND divisibility composition => NEW MAP ENTRY (non-divisibility positional
#        mechanism).  SE_mix <= amp_mix < 2*SE_mix => PARTIAL (neither; ranked diagnostics).
# Reference decomposition (pre-named, corroborating not verdict-bearing):
#     removal_pct = 100*(1 - amp_mix/amp_orig), amp_orig = same amplitude/statistic under the
#     exp588b single-alpha Dickman baseline on the SAME data and pipeline; removal >= 50% AND
#     z_mix < 1 corroborates the H1 wording; removal ~ 0 with z_mix >= 2 corroborates H0.
# CONTROL (pipeline null, see AMENDMENT A1 for the post-smoke split into two controls):
#     CTRL-A (machinery): identical mixture MACHINERY on PAIRED RANDOM HALVES of the non-hit
#       stream with COUNT-vs-COUNT tensors (rho weight replaced by 1 on BOTH sides) MUST be
#       null: amp_ctla < 3*SE_ctla AND amp_ctla < 0.10 AND max-bin |smoothed residual -1| < 0.10
#       over ALL bins; else ARTIFACT-CONTAMINATED (no verdict).
#     CTRL-B (estimator null, parametric): Poisson pseudo-hits with mean g*S_(n,b,c) (g = global
#       flank rate, seed 20260830) fed through the IDENTICAL rho-weighted estimator measure the
#       estimator's own null level incl. max-over-bins bias -> amp_sim +- SE_sim.
#
# Caveats fixed NOW (before data): (i) a max-over-bins statistic is positively biased under the
#   null; CTRL-B MEASURES that null level and a null-calibrated
#   z_cal = (amp_mix - amp_sim)/sqrt(SE_mix^2 + SE_sim^2) is REPORTED ALONGSIDE; the REGISTERED
#   amp-vs-SE rule above stays verdict-bearing; disagreement is flagged in honest_notes, never
#   silently resolved. (ii) lam=5 chosen pre-data. (iii) nb=50 bins, 3-bin smoothing identical to
#   exp588b for comparability; score window [0.55,0.75] per brief, flanks t<0.40|t>0.85 per brief,
#   bins in between (0.41-0.54, 0.76-0.85 CTRs) are BUFFER: predicted, not fitted, not scored.
#   (iv) secondary comparability number amp_mix_wide on exp588b's [0.45,0.85] reported, non-bearing.
#
# AMENDMENT LOG (timing disclosed):
#   A1 (post-smoke, PRE-full-run): smoke exposed that the ORIGINALLY registered control arm
#      (count halves of the non-hit stream as pseudo-"hits" against the rho-WEIGHTED prediction)
#      has a NON-FLAT NULL BY CONSTRUCTION -- counts carry no rho(t) gradient while the
#      prediction does -- so it fails its own bar even on perfectly clean data (observed in
#      smoke: amp 0.47 from ~290 counts/bin). Control SPLIT: CTRL-A count-vs-count halves test
#      the machinery (binning/cells/flank-fit/max-stat/bootstrap); NEW CTRL-B parametric Poisson
#      control on the rho-weighted expectation tests the full estimator null incl. max-statistic
#      bias, and z_cal is now referenced to CTRL-B (matched null). Registered H1/H0 amp-vs-SE
#      rule UNCHANGED. No treatment-arm number entered any verdict through this amendment.
#
# Method:
#  1. Exact-regeneration path (proven exp588b A3): population = random.Random(20260828),
#     make_semiprime(bits=96) balanced (getrandbits(48)|top|1 -> next_prime, q!=p retry,
#     bitlen/balance retries), window jlo=isqrt(N)+1, jhi=3*isqrt(N) INT64-EXACT vs
#     exp581_regen_positions.npz; per-chunk rng(20260828+7000+c) SEQUENTIAL 150k-draw replay
#     (one rng per 16-N chunk, exp578 worker semantics); set-membership + order-walk checks.
#     HASH-CHECK vs npz BEFORE statistics; statistics ABORT on any mismatch (degraded status only).
#  2. Per sampled position: cell from (v%2,v%3,v%5,v%7) via modular arithmetic on j and N
#     (no big-int mod needed); per-(N,bin,cell) hit-count tensor H and reference Dickman-sum
#     tensor S; ln v computed from EXACT integer v (float conversion AFTER subtraction --
#     j^2-N cancels catastrophically near t=0 in float).
#  3. Residual mid-window peak amplitude +- bootstrap SE (2000 reps, resample Ns).
#  4. Control arm as above.
# Smoke: reduced grid (24 Ns, 1200-ctl cap, 200 boot reps) <30 s. Full <=12 min.
# Output: exp588c_mixbase.py / exp588c_smoke.log / exp588c_result.json / findings.md.
# =======================================================================================================
import sys, os, json, time, hashlib, math, random
import numpy as np
import gmpy2
from gmpy2 import mpz, gcd as mpgcd, next_prime

BASE = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74"
NPZ  = f"{BASE}/exp581_regen_positions.npz"
SMOKE = "--smoke" in sys.argv
SEED_BOOT = 20260901          # exp582/588b bootstrap convention
NB = 50
SCORE_WIN = (0.55, 0.75)      # REGISTERED score window (brief)
WIDE_WIN  = (0.45, 0.85)      # exp588b comparability window (secondary)
FLK_LO, FLK_HI = 0.40, 0.85   # flank definition (brief)
LNB_FIXED = math.log(1e6)     # exp578 CUT_BIG, known post-exp588b-A3
JSAMPLES = 150000             # replay length ALWAYS matches exp578 full lineage (smoke included)
LAM = 5.0                     # kappa shrinkage pseudo-counts (pre-registered)
PRIMES = (2, 3, 5, 7)
NCELL = 16

t0 = time.time()
def wall(): return round(time.time()-t0, 1)

# ---------------- Dickman rho ----------------
def dickman_table(umax=36.0, du=2e-3):
    n = int(umax/du)+2
    u = np.arange(n)*du; rho = np.empty(n)
    rho[u <= 1.0] = 1.0
    for k in range(np.searchsorted(u, 1.0), n):
        rho[k] = rho[k-1] - du*rho[int(round((u[k]-1)/du))]/u[k]
    return u, np.maximum(rho, 1e-300)
DT_U, DT_R = dickman_table()
rho_at = lambda x: np.interp(np.clip(x, 0, DT_U[-1]), DT_U, DT_R)

# ---------------- load npz ----------------
d = np.load(NPZ, allow_pickle=True)
NS_FULL = 128
NS = 24 if SMOKE else NS_FULL
jlo = d["jlo"][:NS].astype(np.int64); jhi = d["jhi"][:NS].astype(np.int64)
HITS = [d[f"hit_{i}"].astype(np.int64) for i in range(NS)]
CTLS = [d[f"ctl_{i}"].astype(np.int64) for i in range(NS)]
if SMOKE: CTLS = [c[:1200] for c in CTLS]
hsh = hashlib.sha256()
for i in range(NS_FULL):
    hsh.update(d[f"hit_{i}"].tobytes()); hsh.update(d[f"ctl_{i}"].tobytes())
hsh.update(d["jlo"].tobytes()); hsh.update(d["jhi"].tobytes())
SHA = hsh.hexdigest()

# ================= EXACT regeneration (exp578 lineage, proven in exp588b A3) =================
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

REGEN = {"status": None, "checks": {}}
NS_EXACT = None
try:
    pools = build_pop_v(20260828, NS_FULL)[:NS]
    s_arr = [int(gmpy2.isqrt(mpz(n))) for n in pools]
    jl_pred = np.array([s+1 for s in s_arr], dtype=np.int64)
    jh_pred = np.array([3*s for s in s_arr], dtype=np.int64)
    ok_win = bool(np.array_equal(jl_pred, jlo) and np.array_equal(jh_pred, jhi))
    REGEN["checks"]["population_window_exact"] = ok_win
    if ok_win:
        per = NS_FULL//8
        memb_ok = True; order_ok = True; order_checked = []
        for c in range(NS_FULL//per):
            idxs = [i for i in range(c*per, min((c+1)*per, NS))]
            if not idxs: continue
            rng = random.Random(20260828+7000+c)
            for i in idxs:
                s = s_arr[i]; a = s+1; b = 3*s
                draws = [rng.randint(a, b) for _ in range(JSAMPLES)]
                ds = set(draws)
                if not all(int(x) in ds for x in np.concatenate([HITS[i], CTLS[i]])):
                    memb_ok = False
                ph = pn = 0
                hp = HITS[i].tolist(); nh = CTLS[i].tolist()
                for jv in draws:
                    if ph < len(hp) and jv == hp[ph]: ph += 1
                    elif pn < len(nh) and jv == nh[pn]: pn += 1
                order_ok &= (ph == len(hp) and pn == len(nh))
                order_checked.append(i)
        REGEN["checks"]["stream_membership_all_samples"] = memb_ok
        REGEN["checks"]["stream_order_walk_samples"] = order_checked
        REGEN["checks"]["stream_order_exact"] = bool(order_ok)
        if memb_ok and order_ok:
            NS_EXACT = pools
            REGEN["status"] = "EXACT_MATCH"
        else:
            REGEN["status"] = "WINDOW_MATCH_STREAM_FAIL"
    else:
        REGEN["status"] = "POPULATION_MISMATCH"
except Exception as e:
    REGEN["status"] = f"REGEN_ERROR:{type(e).__name__}"
HAVE_N = NS_EXACT is not None
print(f"[regen] status={REGEN['status']} win={REGEN['checks'].get('population_window_exact')} "
      f"memb={REGEN['checks'].get('stream_membership_all_samples')} "
      f"order={REGEN['checks'].get('stream_order_exact')} wall={wall()}", flush=True)

# ---------------- light smoothness spot-validation under exact N (full mode only) ----------------
SMOOTH_VALIDATE = None
if HAVE_N and not SMOKE:
    try:
        def build_primorial(bound):
            p = mpz(1); q = mpz(2)
            while q <= bound:
                p *= q; q = next_prime(q)
            return p
        P5 = build_primorial(100000); P6 = build_primorial(1000000)
        def classify(v):
            xx = mpz(v)
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
        allh = True
        for i in range(NS):
            Ni = NS_EXACT[i]
            step = max(len(HITS[i])//16, 1)
            for j in HITS[i][::step]:
                if not classify(int(j)*int(j) - Ni): allh = False; break
        rngc = np.random.default_rng(11)
        ctl_ok = True
        for i in range(0, NS, 16):
            sub = CTLS[i][rngc.integers(0, len(CTLS[i]), 8)]
            for j in sub:
                if classify(int(j)*int(j) - NS_EXACT[i]): ctl_ok = False; break
        SMOOTH_VALIDATE = {"hits_smooth_subsample_all": bool(allh), "controls_nonsmooth_subsample_all": bool(ctl_ok)}
        REGEN["checks"]["smoothness_validation"] = SMOOTH_VALIDATE
        print(f"[regen] smoothness spot-check: {SMOOTH_VALIDATE} wall={wall()}", flush=True)
    except Exception as e:
        SMOOTH_VALIDATE = {"error": type(e).__name__}
        print(f"[regen] smoothness spot-check SKIPPED ({type(e).__name__})", flush=True)

# ---------------- tensors: per-(N,bin,cell) hit counts H and reference Dickman sums S ----------------
edges = np.linspace(0, 1, NB+1); CTR = (edges[:-1]+edges[1:])/2
bidx = lambda t: np.clip(np.digitize(t, edges)-1, 0, NB-1)
FL_BINS  = np.where((CTR < FLK_LO) | (CTR > FLK_HI))[0]
SCORE_BINS = np.where((CTR >= SCORE_WIN[0]) & (CTR <= SCORE_WIN[1]))[0]
WIDE_BINS  = np.where((CTR >= WIDE_WIN[0]) & (CTR <= WIDE_WIN[1]))[0]

HN = np.zeros((NS, NB, NCELL)); SN = np.zeros((NS, NB, NCELL))
CN = np.zeros((NS, NB, NCELL))          # reference sample COUNTS per (N,bin,cell) (composition)
BC_I = [None]*NS; W_I = [None]*NS       # per-N (bin*16+cell) index and rho weight (control arm reuse)
if HAVE_N:
    for i in range(NS):
        Ni = NS_EXACT[i]; jl = int(jlo[i]); jh = int(jhi[i])
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

# ---------------- amplitude machinery ----------------
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
    """returns smoothed residual ratio vector over all bins + kappa table"""
    kap, g, Hf, Sf = fit_kappa(H, S)
    PRED = (kap[None, :]*S).sum(1)
    HCt = H.sum(1)
    R = HCt/np.maximum(PRED, 1e-300)
    return smooth(R), R, kap, g, Hf, Sf, PRED

def amp_of(H, S, bins):
    Rs, _, _, _, _, _, _ = ratios_of(H, S)
    return float(max(Rs[bins].max()-1.0, 0.0))

if HAVE_N:
    HC = HN.sum(0); STOT = SN.sum(0)                       # (NB,NCELL)
    RS_ALL, R_ALL, KAP, GFIT, HF_T, SF_T, PRED_ALL = ratios_of(HC, STOT)
    AMP_MIX = float(max(RS_ALL[SCORE_BINS].max()-1.0, 0.0))
    AMP_MIX_WIDE = float(max(RS_ALL[WIDE_BINS].max()-1.0, 0.0))
    # exp588b single-alpha baseline on same tensors
    Af = HC[FL_BINS].sum()/max(STOT[FL_BINS].sum(), 1e-300)
    BASE_VEC = Af*STOT.sum(1)
    R_o = HC.sum(1)/np.maximum(BASE_VEC, 1e-300); RS_O = smooth(R_o)
    AMP_ORIG = float(max(RS_O[SCORE_BINS].max()-1.0, 0.0))

    ns_ = NS
    def boot_se(fn, B):
        rng = np.random.default_rng(SEED_BOOT)
        vals = [fn(rng.integers(0, ns_, ns_)) for _ in range(B)]
        return float(np.std(vals, ddof=1))
    NB_REP = 200 if SMOKE else 2000
    def amp_mix_fn(idx): return amp_of(HN[idx].sum(0), SN[idx].sum(0), SCORE_BINS)
    def amp_orig_fn(idx):
        Hs = HN[idx].sum(0); Ss = SN[idx].sum(0)
        A = Hs.sum()/max(Ss[FL_BINS].sum(), 1e-300)
        Rr = Hs.sum(1)/np.maximum(A*Ss.sum(1), 1e-300)
        return float(max(smooth(Rr)[SCORE_BINS].max()-1.0, 0.0))
    SE_MIX  = boot_se(amp_mix_fn,  NB_REP)
    SE_ORIG = boot_se(amp_orig_fn, NB_REP)
    Z_MIX = AMP_MIX/max(SE_MIX, 1e-12); Z_WIDE = AMP_MIX_WIDE/max(SE_MIX, 1e-12)
    REMOVAL = float(np.clip(100*(1-AMP_MIX/AMP_ORIG), 0, 100)) if AMP_ORIG > 0 else float("nan")
    print(f"[mix] amp_mix={AMP_MIX:.4f} se={SE_MIX:.4f} z={Z_MIX:.2f} "
          f"amp_orig={AMP_ORIG:.4f} removal={REMOVAL:.1f}% wall={wall()}", flush=True)

    # ---------------- CTRL-A: paired random halves of non-hit stream, COUNT-vs-COUNT ----------------
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
    SE_CTLA = boot_se(amp_ctla_fn, NB_REP)
    CTRL_PASS = bool(AMP_CTLA < 3*max(SE_CTLA, 1e-9) and AMP_CTLA < 0.10 and MAXDEV_CTLA < 0.10)
    # ---------------- CTRL-B: parametric Poisson on rho-weighted expectation ----------------
    rngp = np.random.default_rng(20260830)
    SIM_HN = rngp.poisson(GFIT*SN).astype(float)     # null mean g*S everywhere (flank-fitted rate)
    AMP_SIM = amp_of(SIM_HN.sum(0), SN.sum(0), SCORE_BINS)
    def amp_sim_fn(idx): return amp_of(SIM_HN[idx].sum(0), SN[idx].sum(0), SCORE_BINS)
    SE_SIM = boot_se(amp_sim_fn, NB_REP)
    Z_CAL = (AMP_MIX-AMP_SIM)/math.sqrt(SE_MIX**2+SE_SIM**2) if (SE_MIX+SE_SIM) > 0 else float("nan")
    print(f"[ctrlA] amp={AMP_CTLA:.4f} se={SE_CTLA:.4f} maxdev={MAXDEV_CTLA:.4f} pass={CTRL_PASS} | "
          f"[ctrlB] amp_sim={AMP_SIM:.4f} se_sim={SE_SIM:.4f} wall={wall()}", flush=True)

    # composition drift + kappa table (mechanism diagnostics)
    cnt_mid = CN[:, SCORE_BINS, :].sum(1); cnt_flk = CN[:, FL_BINS, :].sum(1)
    w_mid = cnt_mid.sum(0)/max(cnt_mid.sum(), 1); w_flk = cnt_flk.sum(0)/max(cnt_flk.sum(), 1)
    DRIFT = float(np.abs(w_mid-w_flk).max())
    kap_rows = []
    for ci in range(NCELL):
        pat = "".join(str((ci >> k) & 1) for k in range(4))
        kap_rows.append({"cell": f"2:{pat[0]},3:{pat[1]},5:{pat[2]},7:{pat[3]}",
                         "flank_hits": int(HF_T[ci]),
                         "flank_rho_sum": round(float(SF_T[ci]), 2),
                         "kappa": round(float(KAP[ci]), 5),
                         "kappa_over_g": round(float(KAP[ci]/GFIT), 4),
                         "w_mid": round(float(w_mid[ci]), 4), "w_flank": round(float(w_flk[ci]), 4)})
    kap_sorted = sorted(kap_rows, key=lambda r: -r["kappa_over_g"])

    # ---------------- REGISTERED verdict ----------------
    cal_note = None
    if not CTRL_PASS:
        VERDICT = "ARTIFACT-CONTAMINATED: CTRL-A machinery null violated; no channel verdict"
    elif AMP_MIX < SE_MIX:
        VERDICT = "H1: CHANNEL CLOSES -- mid-window excess absorbed by divisibility mixture"
        if Z_CAL >= 2.0: cal_note = "registered rule fires H1 but null-calibrated z>=2 -- flagged"
    elif AMP_MIX >= 2*SE_MIX:
        VERDICT = "H0: EXCESS SURVIVES mixture -- structure beyond divisibility composition -> NEW MAP ENTRY"
        if Z_CAL < 2.0: cal_note = "registered rule fires H0 but null-calibrated z<2 -- max-statistic bias caveat"
    else:
        VERDICT = "PARTIAL: residual between 1x and 2x SE -- neither closure nor survival bars met"
    corrobor = ("consistent" if (REMOVAL >= 50 and Z_MIX < 1) or (REMOVAL <= 10 and Z_MIX >= 2) else "mixed")
    verdicts = {
        "verdict": VERDICT,
        "rule": "H1 iff amp_mix<SE_mix; H0 iff amp_mix>=2*SE_mix; else PARTIAL; control arm must be null",
        "amp_mix": round(AMP_MIX, 4), "se_mix": round(SE_MIX, 4), "z_mix": round(Z_MIX, 2),
        "amp_mix_wide_[0.45,0.85]": round(AMP_MIX_WIDE, 4),
        "amp_orig_single_alpha": round(AMP_ORIG, 4), "se_orig": round(SE_ORIG, 4),
        "removal_pct": round(REMOVAL, 1) if REMOVAL == REMOVAL else None,
        "corroboration": corrobor,
        "amp_ctla_machinery": round(AMP_CTLA, 4), "se_ctla": round(SE_CTLA, 4),
        "ctla_maxdev_all_bins": round(MAXDEV_CTLA, 4), "control_pass": CTRL_PASS,
        "amp_sim_estimator_null": round(AMP_SIM, 4), "se_sim": round(SE_SIM, 4),
        "z_null_calibrated_vs_ctrlB": round(Z_CAL, 2) if Z_CAL == Z_CAL else None,
        "calibration_flag": cal_note,
    }
else:
    verdicts = {"verdict": f"NO STATISTICS: regen failed ({REGEN['status']})"}

rows_out = []
if HAVE_N:
    for bb in range(NB):
        rows_out.append({"bin": bb, "t": round(float(CTR[bb]), 3), "hits": int(HC[bb].sum()),
                         "pred_mix": round(float(PRED_ALL[bb]), 2),
                         "ratio_mix": round(float(R_ALL[bb]), 4),
                         "ratio_mix_smooth": round(float(RS_ALL[bb]), 4),
                         "ratio_orig": round(float(R_o[bb]), 4)})

RESULT = {
 "config": {"exp": "exp588c", "codename": "MIXTURE-BASELINE", "smoke": SMOKE,
  "nsamples": NS, "nbins": NB, "ncells": NCELL,
  "boot_reps": 200 if SMOKE else 2000, "seed_boot": SEED_BOOT,
  "score_window": list(SCORE_WIN), "flanks": "t<0.40|t>0.85",
  "wide_comparability_window": list(WIDE_WIN), "kappa_shrinkage_lam": LAM,
  "lnB_fixed": round(LNB_FIXED, 4), "jsamples_replay": JSAMPLES,
  "sha256_npz": SHA, "have_exact_N": HAVE_N, "regen": REGEN,
  "amendment_log": ["A1 (post-smoke pre-full-run): control split into CTRL-A count-vs-count "
                    "machinery gate + CTRL-B parametric Poisson estimator-null; z_cal referenced "
                    "to CTRL-B; registered amp-vs-SE rule unchanged"],
  "model": "PRED(b)=sum_c kappa_c*S_c(b); S_c=Dickman-weighted reference samples; kappa_c flank-only fit with lam-shrinkage to global rate"},
 "regression": {"status": REGEN["status"], "checks": REGEN["checks"],
                "abort_before_statistics": not HAVE_N},
 "residual": {"rows": rows_out,
              "score_bins_t": [round(float(CTR[b]), 3) for b in SCORE_BINS]},
 "stats": ({} if not HAVE_N else {
    "amp_mix": AMP_MIX, "se_mix": SE_MIX, "z_mix": Z_MIX,
    "amp_mix_wide": AMP_MIX_WIDE, "amp_orig": AMP_ORIG, "se_orig": SE_ORIG,
    "removal_pct": REMOVAL, "amp_ctla_machinery": AMP_CTLA, "se_ctla": SE_CTLA,
    "amp_sim_estimator_null": AMP_SIM, "se_sim": SE_SIM,
    "z_null_calibrated": Z_CAL, "total_hits": int(HC.sum()),
    "total_reference": int(CN.sum()), "g_global_flank_rate": round(float(GFIT), 6),
    "composition_drift_max_c": DRIFT,
    "kappa_table_sorted_by_kappa_over_g": kap_sorted}),
 "verdicts": verdicts,
 "honest_notes": [
  "Exact-regen lineage reused verbatim from proven exp588b-A3 path: population+windows int64-equal, "
  "sequential per-chunk 150k-draw replay, membership+order checks; statistics gated on EXACT_MATCH."
  if HAVE_N else f"Regen failed ({REGEN['status']}); no statistics produced.",
  "Max-over-bins amplitude is positively biased under the null; CTRL-B (parametric Poisson on the "
  "rho-weighted expectation) measures that null and z_cal=(amp_mix-amp_sim)/sqrt(se_mix^2+se_sim^2) "
  "is reported alongside; the registered amp-vs-SE rule remains verdict-bearing; any disagreement "
  "is flagged, not resolved.",
  "A1 amendment: original single control (count halves vs rho-weighted prediction) had a non-flat "
  "null by construction -- caught in smoke, split into CTRL-A (machinery) + CTRL-B (estimator "
  "null) BEFORE the full run; no treatment number entered a verdict through the amendment.",
  "kappa_c shrinkage lam=5 toward global flank rate guards rare empty cells (pre-registered); "
  "mid/score window fully excluded from all kappa estimation.",
  "Reference stream = stored capped non-hits (<=4000/N, first-in-stream); unbiased for uniform "
  "sampling composition, disclosed as subsample.",
  "Bit 0 (2|v) is IDENTICALLY j-parity since N is odd -- cell 2 merges the exp588b parity carrier; "
  "the other 3 bits are v-divisibility proper.",
  "ln v computed from EXACT integer v then float-converted (float j^2-N would cancel catastrophically "
  "near t=0); rho table/interpolation identical to exp588b.",
  "Buffer bins (CTR 0.41-0.54, 0.76-0.85) are predicted but neither fitted nor scored (brief windows).",
 ],
 "wall_s": wall()}
out_name = "exp588c_smoke_result.json" if SMOKE else "exp588c_result.json"
with open(f"{BASE}/{out_name}", "w") as f:
    json.dump(RESULT, f, indent=1, default=float)
print(json.dumps(verdicts, indent=1))
top = kap_sorted[:5] if HAVE_N else []
print("top kappa_over_g cells:", [(r["cell"], r["kappa_over_g"], r["flank_hits"]) for r in top])
print("composition drift max_c:", DRIFT if HAVE_N else "n/a")
print("WALL", wall())

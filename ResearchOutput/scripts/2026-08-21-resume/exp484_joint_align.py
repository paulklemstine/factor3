#!/usr/bin/env python3
"""EXP 484 JOINT-ALIGN (round-41). Seed 20260903. Mirrors exp482's clean protocol.

Context: papers 150/151 closed LINEAR phase-feature encodings at both prime ranges
(+0.008/+0.0215, both sub-threshold). Paper 150's redirect: try INTERACTION /
JOINT-ALIGNMENT encodings -- e.g. cross-prime offset coincidences (do two primes'
divisibility hits land on the same j-slots?), which linear cos/sin encodings cannot
express. This experiment implements exactly that: pairwise (and one triple)
coincidence COUNTS of joint divisibility, added to the paper-145 dial (w,d).

PRE-STATED HYPOTHESES (recorded before data generation):
H1: a joint-alignment feature set -- pairwise coincidence counts
    c_pq(N) = #{j <= 240 : p | v_j AND q | v_j} for the 10 pairs of the 5 primes
    {3,5,7,11,13} (C(5,2) = 10 features) -- adds >= +0.03 out-of-sample R^2 over the
    paper-145 dial (w,d) SAME-WINDOW at u=2.5, 240 values/N.
H2: joint-alignment features transfer across disjoint j-windows BETTER than singleton
    phases did (cross/same ratio > 0.5), because coincidences are window-position-
    invariant... OR they fail to transfer too (both outcomes informative).
    PRE-STATED GUESS: TRANSFER branch (ratio > 0.5). Rationale: p|v_j AND q|v_j is an
    AP-class condition mod pq on j (CRT of the two root classes), so c_pq is a function
    of N mod pq and the window LENGTH alone; each active class contributes ~equal hits
    to both halves up to O(pq/120) boundary jitter, and the count->yield mechanism
    (more small-prime joint hits => richer B-smooth supply) is position-free.
    Risk: v_j grows quadratically in j, so halves differ in value scale; if yield is
    driven by absolute j-location interplay rather than per-half recalibration,
    transfer could break despite count invariance.
H3: combined (w,d,joint) reaches R^2 >= 0.65 (same-window, u=2.5).
    PRE-STATED GUESS: borderline/FAIL -- base sits near 0.59, so H3 needs ~+0.06 total,
    twice the H1 ask; plausible only if coincidence density carries large variance
    beyond the union fraction.

BARRIERS:
(5) all features are residue dials of METHOD input statistics -- zero factor information;
    these models predict sieving yield, never factor identity.
(8) QS calibration: this entire exercise is QS yield-calibration science.

DESIGN (mirrors exp482 verbatim except where ledgered): 1200 semiprimes bitlen 44
(p,q uniform prime in [2^21,2^22)); values v_j = j(2s+j)+(s^2-N) for j=1..240;
smoothness via B = exp(ln vmed/u) with vmed PER WINDOW (all/first/second recomputed);
strip primes <= B. OLS train/test 900/300 same N-split across arms; paired bootstrap
(300 resamples of test rows) for dR2 CIs. Arms: base(w,d); ph13(base + exp482's
singleton-phase cos/sin/qr on {3,5,7,11,13} -- SAME-population comparator for H2);
pair(base + 10 coincidence counts); trip(base + 1 triple count {3,5,7});
full(base + pairs + triple).

METHOD LEDGER (decisions + audit of inherited artifacts):
L0  Fresh implementation; exp482's protocol file read and its population builder,
    stripper, target construction, split/bootstrap machinery reused VERBATIM (seeds
    shifted to this experiment's: population rng SEED=20260903, partition SEED+1,
    bootstrap SEED+2). No inherited artifacts in this directory.
L1  j runs 1..240: v_0 = s^2-N <= 0; design's positivity assert pins j>=1 (as exp482 L1).
L2  Coincidence encoding: RAW slot fractions c_pq/240 (count/length, matching d's
    fraction convention; OLS + train standardization makes the scale irrelevant --
    recorded for convention parity, cf. exp482 L9).
L3  Fixed prime set {3,5,7,11,13} -> 10 fixed pairs + fixed triple {3,5,7}: fixed OLS
    design matrix (exp482 L3 logic). p*q | v_j iff p|v_j and q|v_j (distinct odd primes).
L4  Features frozen across arms; ONLY targets recomputed per window half (own median-v
    B), per design (exp482 L4 verbatim).
L5  One strip pass to primes <= PB=4200 recording (rem, maxp); smooth@B iff rem==1 and
    maxp<=B (exp482 L5 verbatim).
L6  Bootstrap = paired resampling of the 300 test Ns with fitted coefficients frozen.
L7  One shared 900/300 N-partition across all arms/models for paired comparability.
L8  d(N) is itself a function of the small-prime divisibility vector (exp482 L8): it is
    the UNION count over {2,3,5,7,11,13}; pair/triple counts are INTERSECTION counts
    over subsets -- they extend d with co-incidence (overlap density) structure the
    union cannot express, and are deterministic functions of the same phase vector
    (positions of the +-root AP classes mod pq). Any positive dR2(pair) is structure
    BEYOND the union fraction.
L9  Standardize columns by TRAIN mean/std before lstsq + explicit unstandardized
    ones-column intercept (bakes in exp482's L14 lesson: standardized features cannot
    carry the target mean without it).
L10 Population ledger + draws count (exp482 L10 form).
L11 Target sanity: mean yields all/first/second + mean B per window (exp482 L11 form).
L12 Feature sanity: QR rates on {3,5,7,11,13}; corr(w,d vs y_all@2.5); pair-count
    zero-fractions (expected ~ P(either prime QNR) ~ 3/4 under independence) and
    max |corr(c_pq, d)| (overlap-density novelty check).
L13 Model dims ledgered.
L14 EXTRA vs spec: ph13 arm added (exp482's p13 construction, byte-for-byte feature
    definition) so H2's "better than singleton phases did" is tested WITHIN this run's
    population/bootstrap rather than only against exp482's cross-seed numbers.
"""
import json, math, os, time
import numpy as np
from itertools import combinations

SEED = 20260903
OUTDIR = "/tmp/exp41_joint"
os.makedirs(OUTDIR, exist_ok=True)
T0 = time.time()

RES = {"exp": 484, "codename": "JOINT-ALIGN", "seed": SEED,
       "hypotheses": {
           "H1": "pair coincidence counts c_pq ({3,5,7,11,13}, 10 pairs) lift OOS R2 >= +0.03 over (w,d), same-window, u=2.5",
           "H2": "joint features transfer cross-window BETTER than singleton phases (ratio > 0.5) [pre-stated guess: TRANSFER]",
           "H3": "combined (w,d,joint) reaches R2 >= 0.65 (same-window, u=2.5) [pre-stated guess: borderline/FAIL]"},
       "barriers": ["(5) all features are residue dials of METHOD input statistics - zero factor information",
                    "(8) QS calibration"],
       "ledger": [
           "L0 fresh implementation; exp482 population builder/stripper/targets/split/bootstrap reused verbatim with this exp's seeds (20260903/+1/+2)",
           "L1 j=1..240 (v_0<=0 excluded by positivity assert)",
           "L2 coincidence encoding = raw slot fractions c/240 (matches d's convention; scale-invariant under train standardization)",
           "L3 fixed prime set {3,5,7,11,13}: 10 pairs + triple {3,5,7}; pq|v_j iff p|v_j and q|v_j",
           "L4 features frozen across arms; targets recomputed per window half (own median-v B)",
           "L5 one strip pass to PB=4200 -> (rem,maxp); smooth@B iff rem==1 and maxp<=B",
           "L6 bootstrap: 300 paired resamples of test rows, coefficients frozen",
           "L7 shared 900/300 partition across arms",
           "L8 pair/triple = INTERSECTION counts extending d's UNION count; functions of the same phase vector; positive dR2 is beyond-union structure",
           "L9 train-stat standardization + explicit ones-column intercept (exp482 L14 lesson baked in)",
           "L14 EXTRA arm ph13 (exp482 p13 feature construction verbatim) for same-population phase-vs-joint transfer comparison"],
       "stages": {}}

def log(*a):
    m = " ".join(str(x) for x in a)
    print(m, flush=True)

def ledger(msg):
    RES["ledger"].append(msg)
    log("[LEDGER]", msg)

def checkpoint(stage, data=None):
    if data is not None:
        RES["stages"][stage] = data
    RES["saved_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    RES["elapsed_s"] = round(time.time() - T0, 1)
    with open(os.path.join(OUTDIR, "result.json"), "w") as f:
        json.dump(RES, f, indent=1, default=float)
    log("[checkpoint]", stage)

rng = np.random.default_rng(SEED)

try:
    import gmpy2
    HAVE_GMPY2 = True
except Exception:
    HAVE_GMPY2 = False
log("gmpy2:", HAVE_GMPY2)

# ------------------------------------------------------------------ helpers
def euler(a, p):
    """Euler criterion: +1 QR, -1 QNR (p odd prime, p does not divide a)."""
    t = int(gmpy2.powmod(a % p, (p - 1) // 2, p)) if HAVE_GMPY2 else pow(a % p, (p - 1) // 2, p)
    return 1 if t == 1 else (-1 if t == p - 1 else 0)

def sieve_primes(n):
    bs = bytearray([1]) * (n + 1)
    bs[0] = bs[1] = 0
    for i in range(2, math.isqrt(n) + 1):
        if bs[i]:
            bs[i * i::i] = bytearray(len(range(i * i, n + 1, i)))
    return [i for i in range(n + 1) if bs[i]]

PRIMES_ALL = sieve_primes(20000)
PRIMES_ODD_LE400 = [p for p in PRIMES_ALL if 3 <= p <= 400]
P5 = [3, 5, 7, 11, 13]
PAIRS = list(combinations(P5, 2))          # 10 pairs
TRIPLE = (3, 5, 7)
DMASK_PRIMES = (2, 3, 5, 7, 11, 13)        # exp482 d(N) union set

def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

# ------------------------------------------------------- stage 1: population
N_PER = 1200
J = 240
HALF = 120

def gen_population():
    lo, hi = 2 ** 21, 2 ** 22
    seen, out, draws = set(), [], 0
    while len(out) < N_PER:
        draws += 1
        p = int(rng.integers(lo, hi))
        q = int(rng.integers(lo, hi))
        if p == q or not is_prime(p) or not is_prime(q):
            continue
        N = p * q
        if N.bit_length() != 44 or N in seen:
            continue
        seen.add(N)
        out.append(N)
    return out, draws

NS, DRAWS = gen_population()
assert len(NS) == N_PER
ledger(f"L10 population: {len(NS)} distinct semiprimes bitlen 44, p,q uniform prime [2^21,2^22), {DRAWS} candidate draws")
checkpoint("population", {"n": len(NS), "draws": DRAWS,
                          "bitlens": sorted({int(N).bit_length() for N in NS})})

# --------------------------------------------- stage 2: values + one strip pass
PB = 4200
STRIP_PRIMES = [p for p in PRIMES_ALL if p <= PB]

def build_chunks(primes, cap=10 ** 150):
    chunks, cur, curp = [], 1, []
    for p in primes:
        if cur * p > cap and curp:
            chunks.append(curp)
            cur, curp = 1, []
        cur *= p
        curp.append(p)
    if curp:
        chunks.append(curp)
    return chunks

CHUNKS = [(math.prod(ps), ps) for ps in build_chunks(STRIP_PRIMES)]

def strip_value(v):
    """Divide out every prime <= PB. Returns (rem, maxp); smooth@B iff rem==1 and maxp<=B."""
    rem, maxp = v, 0
    for prod, ps in CHUNKS:
        if rem == 1:
            break
        if math.gcd(rem, prod) == 1:
            continue
        for p in ps:
            if rem % p == 0:
                if p > maxp:
                    maxp = p
                while rem % p == 0:
                    rem //= p
    return rem, maxp

records = []
n_smooth_any = 0
for N in NS:
    s = math.isqrt(N)
    r0 = N - s * s
    vals = [j * (2 * s + j) - r0 for j in range(1, J + 1)]
    assert all(v > 0 for v in vals), "design assertion: all relation values positive"
    stripped = [strip_value(v) for v in vals]
    n_smooth_any += sum(1 for rem, _ in stripped if rem == 1)
    records.append((N, s, vals, stripped))

log(f"strip pass done: {sum(len(r[3]) for r in records)} values, "
    f"{n_smooth_any} smooth@{PB} ({n_smooth_any / (len(records) * J):.4f}), "
    f"{time.time() - T0:.1f}s")
checkpoint("values_stripped", {"n_values": len(records) * J,
                               "frac_smooth_at_PB": n_smooth_any / (len(records) * J)})

# ------------------------------------- stage 3: targets per u, per window half
def b_of(vlist, u):
    vmed = float(np.median(np.asarray(vlist, dtype=float)))
    return math.exp(math.log(vmed) / u)

def smooth_frac(stripped, B, lo, hi):
    c = sum(1 for rem, mx in stripped[lo:hi] if rem == 1 and mx <= B)
    return c / (hi - lo)

US = (2.5, 3.5)
TARGETS = {}
for u in US:
    y_all, y_first, y_second, Bs = [], [], [], []
    for N, s, vals, stripped in records:
        Ba = b_of(vals, u)              # full-window threshold
        Bf = b_of(vals[:HALF], u)       # first-half threshold (recomputed)
        Bd = b_of(vals[HALF:], u)       # second-half threshold (recomputed)
        y_all.append(smooth_frac(stripped, Ba, 0, J))
        y_first.append(smooth_frac(stripped, Bf, 0, HALF))
        y_second.append(smooth_frac(stripped, Bd, HALF, J))
        Bs.append((Ba, Bf, Bd))
    TARGETS[u] = {"all": np.array(y_all), "first": np.array(y_first),
                  "second": np.array(y_second),
                  "B_mean": [float(np.mean([b[k] for b in Bs])) for k in range(3)]}
    t = TARGETS[u]
    ledger(f"L11 targets u={u}: mean yields all={t['all'].mean():.4f} "
           f"first={t['first'].mean():.4f} second={t['second'].mean():.4f}; "
           f"mean B all/first/second = {[round(x,1) for x in t['B_mean']]}")
checkpoint("targets", {f"u{u}": {"mean_yields": {"all": float(TARGETS[u]['all'].mean()),
                                                 "first": float(TARGETS[u]['first'].mean()),
                                                 "second": float(TARGETS[u]['second'].mean())},
                                 "B_mean_all_first_second": TARGETS[u]["B_mean"],
                                 "std_y_all": float(TARGETS[u]['all'].std())} for u in US})

# ------------------------------------------------------- stage 4: features
W = np.zeros(len(records))
D = np.zeros(len(records))
PC = np.zeros((len(records), len(PAIRS)))   # pair coincidence slot-fractions
TC = np.zeros(len(records))                 # triple {3,5,7}
PH = {}                                     # N -> {p: (cos, sin, qr)} for ph13 arm
for i, (N, s, vals, stripped) in enumerate(records):
    w = 0.0
    for p in PRIMES_ODD_LE400:
        if euler(N, p) == 1:
            w += 2.0 / p
    W[i] = w
    arr = np.array(vals, dtype=np.int64)    # |v_j| < ~2.1e9 << 2^63: exact
    masks = {p: (arr % p == 0) for p in P5}
    m2 = (arr % 2 == 0)
    D[i] = float((m2 | masks[3] | masks[5] | masks[7] | masks[11] | masks[13]).sum()) / J
    for k, (p, q) in enumerate(PAIRS):
        PC[i, k] = float((masks[p] & masks[q]).sum()) / J
    TC[i] = float((masks[3] & masks[5] & masks[7]).sum()) / J
    row = {}
    for p in P5:
        if euler(N, p) == 1:
            Nm = N % p
            r1 = min(x for x in range(p) if (x * x - Nm) % p == 0)   # smaller root
            o = (r1 - s) % p                                         # exp482 definition
            a = 2.0 * math.pi * o / p
            row[p] = (math.cos(a), math.sin(a), 1.0)
        else:
            row[p] = (0.0, 0.0, 0.0)
    PH[N] = row

qr_rates = {p: float(np.mean([PH[N][p][2] for N in NS])) for p in P5}
pc_zero_frac = {f"{p}x{q}": float(np.mean(PC[:, k] == 0)) for k, (p, q) in enumerate(PAIRS)}
max_abs_corr_pc_d = float(max(abs(np.corrcoef(PC[:, k], D)[0, 1]) for k in range(len(PAIRS))))
corr_pc_y = {f"{p}x{q}": float(np.corrcoef(PC[:, k], TARGETS[2.5]["all"])[0, 1])
             for k, (p, q) in enumerate(PAIRS)}
best_pc = max(corr_pc_y, key=lambda k: abs(corr_pc_y[k]))
ledger(f"L12 feature sanity: QR rates {({k: round(v,3) for k,v in qr_rates.items()})}; "
       f"corr(w, y_all@2.5)={float(np.corrcoef(W, TARGETS[2.5]['all'])[0,1]):.3f}, "
       f"corr(d, y_all@2.5)={float(np.corrcoef(D, TARGETS[2.5]['all'])[0,1]):.3f}")
ledger(f"L12b pair counts: zero-frac range [{min(pc_zero_frac.values()):.3f},{max(pc_zero_frac.values()):.3f}] "
       f"(indpendence null ~0.75); mean counts {[round(float(x*J),1) for x in PC.mean(0)]}; "
       f"max|corr(c_pq,d)|={max_abs_corr_pc_d:.3f}; best |corr(c_pq,y)| {best_pc}={abs(corr_pc_y[best_pc]):.3f}")
checkpoint("features", {"qr_rates": qr_rates, "w_mean": float(W.mean()), "d_mean": float(D.mean()),
                        "pc_zero_frac": pc_zero_frac, "tc_zero_frac": float(np.mean(TC == 0)),
                        "tc_mean_count": float(TC.mean() * J),
                        "max_abs_corr_pc_d": max_abs_corr_pc_d,
                        "corr_pc_y_u2.5": corr_pc_y})

def build_X(model):
    cols = [W, D]
    if model == "ph13":
        for p in P5:
            cols.append(np.array([PH[N][p][0] for N in NS]))
            cols.append(np.array([PH[N][p][1] for N in NS]))
            cols.append(np.array([PH[N][p][2] for N in NS]))
    elif model == "pair":
        cols += [PC[:, k] for k in range(len(PAIRS))]
    elif model == "trip":
        cols.append(TC)
    elif model == "full":
        cols += [PC[:, k] for k in range(len(PAIRS))]
        cols.append(TC)
    return np.column_stack(cols)

MODELS = ["base", "ph13", "pair", "trip", "full"]
XMAT = {m: build_X(m) for m in MODELS}
ledger(f"L13 model dims: " + ", ".join(f"{m}:{XMAT[m].shape[1]}cols" for m in MODELS))

# ------------------------------------------------------------ stage 5: fits
perm = np.random.default_rng(SEED + 1).permutation(len(NS))
TR, TE = perm[:900], perm[900:]

def r2(yt, yp):
    yt = np.asarray(yt, float)
    yp = np.asarray(yp, float)
    sst = float(((yt - yt.mean()) ** 2).sum())
    if sst <= 0:
        return float("nan")
    return float(1.0 - ((yt - yp) ** 2).sum() / sst)

def fit_eval(X, ytr_vec, yte_vec):
    Xtr, Xte = X[TR], X[TE]
    mu = Xtr.mean(0)
    sd = Xtr.std(0)
    sd[sd < 1e-12] = 1.0
    A = np.column_stack([(Xtr - mu) / sd, np.ones(len(Xtr))])    # L9: explicit intercept
    Bm = np.column_stack([(Xte - mu) / sd, np.ones(len(Xte))])
    coef, *_ = np.linalg.lstsq(A, ytr_vec[TR], rcond=None)
    ptr, pte = A @ coef, Bm @ coef
    return r2(ytr_vec[TR], ptr), r2(yte_vec[TE], pte), pte

BRNG = np.random.default_rng(SEED + 2)

ARMS = {}
for u in US:
    t = TARGETS[u]
    for mode in ("same", "cross"):
        ytr_vec = t["all"] if mode == "same" else t["first"]
        yte_vec = t["all"] if mode == "same" else t["second"]
        arm = {}
        preds = {}
        for m in MODELS:
            r2tr, r2te, pte = fit_eval(XMAT[m], ytr_vec, yte_vec)
            arm[m] = {"r2_train": r2tr, "r2_test": r2te}
            preds[m] = pte
        yy = yte_vec[TE]
        for m in MODELS:
            if m == "base":
                continue
            ds = np.empty(300)
            for b in range(300):
                idx = BRNG.integers(0, len(yy), len(yy))
                ds[b] = r2(yy[idx], preds[m][idx]) - r2(yy[idx], preds["base"][idx])
            lo, med, hi = (float(x) for x in np.percentile(ds, [2.5, 50, 97.5]))
            arm[m].update({
                "dR2": arm[m]["r2_test"] - arm["base"]["r2_test"],
                "dR2_boot_ci95": [lo, med, hi],
                "gain_norm": (arm[m]["r2_test"] - arm["base"]["r2_test"]) / max(1e-12, 1.0 - arm["base"]["r2_test"])})
        ARMS[f"u{u}_{mode}"] = arm
        log(f"arm u={u} {mode}: base={arm['base']['r2_test']:.4f} "
            f"ph13={arm['ph13']['r2_test']:.4f} ({arm['ph13']['dR2']:+.4f}) "
            f"pair={arm['pair']['r2_test']:.4f} ({arm['pair']['dR2']:+.4f}) "
            f"trip={arm['trip']['r2_test']:.4f} ({arm['trip']['dR2']:+.4f}) "
            f"full={arm['full']['r2_test']:.4f} ({arm['full']['dR2']:+.4f})")
        checkpoint("arms_partial", ARMS)

# ------------------------------------------------------------ stage 6: verdicts
a_same = ARMS["u2.5_same"]
a_cross = ARMS["u2.5_cross"]
d_same_pair = a_same["pair"]["dR2"]
ci_same_pair = a_same["pair"]["dR2_boot_ci95"]
d_cross_pair = a_cross["pair"]["dR2"]
ci_cross_pair = a_cross["pair"]["dR2_boot_ci95"]
d_same_full = a_same["full"]["dR2"]
r2_full = a_same["full"]["r2_test"]
r2_ph_same = a_same["ph13"]["r2_test"]
r2_ph_cross = a_cross["ph13"]["r2_test"]

H1_strong = bool(d_same_pair >= 0.03 and ci_same_pair[0] > 0)
H1_point = bool(d_same_pair >= 0.03)
if d_same_pair > 0:
    ratio = d_cross_pair / d_same_pair
    H2_transfer = bool(ratio > 0.5)
else:
    ratio = None
    H2_transfer = None
H3 = bool(r2_full >= 0.65)

# same-population phase-vs-joint comparison (L14)
ph_ratio = (a_cross["ph13"]["dR2"] / a_same["ph13"]["dR2"]) if a_same["ph13"]["dR2"] > 0 else None

if H1_point:
    name = "JOINT-ALIGN-TRANSFERS" if H2_transfer else "JOINT-WINDOW-LOCAL"
elif d_same_pair > 0:
    name = "JOINT-SUBTHRESHOLD-LIFT"
else:
    name = "JOINT-NO-LIFT"
VERDICT = f"{name}/H3-{'PASS' if H3 else 'FAIL'}"

RES["verdict"] = {
    "name": VERDICT,
    "u2.5": {
        "dR2_pair_same": d_same_pair, "ci95_same_pair": ci_same_pair,
        "dR2_pair_cross": d_cross_pair, "ci95_cross_pair": ci_cross_pair,
        "ratio_pair_cross_over_same": ratio,
        "dR2_ph13_same": a_same["ph13"]["dR2"], "ci95_same_ph13": a_same["ph13"]["dR2_boot_ci95"],
        "dR2_ph13_cross": a_cross["ph13"]["dR2"], "ratio_ph13": ph_ratio,
        "dR2_trip_same": a_same["trip"]["dR2"], "ci95_same_trip": a_same["trip"]["dR2_boot_ci95"],
        "dR2_full_same": d_same_full, "ci95_same_full": a_same["full"]["dR2_boot_ci95"],
        "dR2_full_cross": a_cross["full"]["dR2"], "ci95_cross_full": a_cross["full"]["dR2_boot_ci95"],
        "R2_base_same": a_same["base"]["r2_test"], "R2_base_cross": a_cross["base"]["r2_test"],
        "R2_ph13_same": r2_ph_same, "R2_full_same": r2_full,
        "H1_strong": H1_strong, "H1_point": H1_point,
        "H2_transfer": H2_transfer, "H2_guess_was_TRANSFER": True, "H3": H3}}
RES["arms"] = ARMS
checkpoint("verdicts")

log("=" * 72)
log(f"VERDICT: {VERDICT}")
log(f"H1 (>=+0.03 same-window pair lift): point={d_same_pair:+.4f} CI95=[{ci_same_pair[0]:+.4f},{ci_same_pair[2]:+.4f}]"
    f" -> {'STRONG-PASS' if H1_strong else ('POINT-PASS' if H1_point else 'FAIL')}")
log(f"H2 (transfer, ratio>0.5): same={d_same_pair:+.4f} cross={d_cross_pair:+.4f} "
    f"ratio={('%.3f' % ratio) if ratio is not None else 'NA'} -> {H2_transfer} "
    f"[guess was TRANSFER]; ph13 same-run comparator ratio="
    f"{('%.3f' % ph_ratio) if ph_ratio is not None else 'NA'}")
log(f"H3 (full R2 >= 0.65): {r2_full:.4f} (dR2={d_same_full:+.4f}) -> {H3}")
log("baseline reproduction check vs paper-145 (~0.59): "
    f"same-window base R2 = {a_same['base']['r2_test']:.4f}; leak-free split base = {a_cross['base']['r2_test']:.4f}")
np.savez(os.path.join(OUTDIR, "data484.npz"),
         W=W, D=D, PC=PC, TC=TC, TR=TR, TE=TE,
         **{f"y_{u}_{k}": TARGETS[u][k] for u in US for k in ("all", "first", "second")})
log("DONE", round(time.time() - T0, 1), "s")

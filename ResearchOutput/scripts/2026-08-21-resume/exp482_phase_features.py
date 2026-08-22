#!/usr/bin/env python3
"""EXP 482 PHASE-FEATURES (round-41). Seed 20260901. Clean reimplementation.

Context: papers 145/147 -- per-N relation-yield predicted by w(N)=sum(2/p | p<=400 QR)
plus divisibility fraction d(N), OOS R^2 ~ 0.59 (u=2.5, 240 values/N); paper 147 found
the dial EXCEEDS the leak-free split ceiling 1.6-2.1x and named this follow-up: add a
PHASE-AWARE feature (root-position profile mod p).

PRE-STATED HYPOTHESES (recorded before data generation):
H1: phase features o_p(N) = (r1 - s) mod p for p in {3,5,7,11,13} (r1 = N's SMALLER root
    mod p, s = floor(sqrt(N)); where divisibility hits fall relative to window start),
    encoded as (cos,sin)(2*pi*o/p), lift out-of-sample R^2 by >= +0.05 over the paper-145
    dial (w,d) at 240 values/N, u=2.5.
H2: the phase gain SHRINKS on a disjoint j-window (train j=1..120, test j=121..240,
    targets recomputed per window): dR2_phase(cross) < half its same-window value --
    would EXPLAIN the split-ceiling excess mechanistically as window-local structure.
H3: the full augmented model (phase primes <= 30) reaches R^2 >= 0.70 (same-window, u=2.5).

BARRIERS:
(5) all features are residue dials of METHOD input statistics -- zero factor information;
    these models predict sieving yield, never factor identity.
(8) QS calibration: this entire exercise is QS yield-calibration science.

DESIGN: 1200 semiprimes bitlen 44 (p,q uniform prime in [2^21,2^22)); values
v_j = j(2s+j)+(s^2-N) for j=1..240 (v_0 <= 0 excluded by the positivity assert);
smoothness via B = exp(ln vmed/u) with vmed PER WINDOW (all/first/second recomputed);
strip primes <= B. OLS train/test 900/300 same N-split across arms; paired bootstrap
(300 resamples of test rows) for dR2 CIs.

METHOD LEDGER (decisions + audit of inherited artifacts):
L0  Inherited dir held a prior attempt: result.json had R^2=1.0 everywhere; audit of its
    script found (a) cross-window arm trained AND tested on second-half targets (no
    transfer ever tested -> its H2 numbers void), (b) offset used min-of-two-root-offsets
    instead of (r1-s) mod p, (c) non-QR encoded as angle 0 colliding with genuine o=0,
    (d) B computed once from pooled vmed, never per window half, (e) stale checkpoint.
    Quarantined to attic_prev_attempt/. This run is a full fresh implementation.
L1  j runs 1..240: v_0 = s^2-N <= 0; design's "assert > 0" pins j>=1 (v_1 >= 1 always).
L2  Phase encoding: QR primes get (cos,sin)(2pi*o/p) on the unit circle plus an explicit
    qr indicator column; non-residues get (0,0,0). The indicator disambiguates non-QR
    from o=0 (the inherited script's collision). Superset of the specified cos/sin pair.
L3  Fixed prime sets {3,5,7,11,13} (+{17,19,23,29} extended) rather than per-N "k smallest
    QR primes": OLS needs a fixed design matrix; per-N variable-length sets are unusable.
L4  Features frozen across arms; ONLY targets are recomputed per window half (B_first from
    first-half median v, B_second from second-half median v), per design.
L5  Single stripping pass to primes <= PB=4200 recording (rem, maxp); smooth@B iff
    rem==1 and maxp<=B (maxp=0 only for v=1). Chunked-gcd cascade for speed; exact ints.
L6  Bootstrap = paired resampling of the 300 test Ns with fitted coefficients frozen.
L7  One shared 900/300 N-partition (seed SEED+1 permutation) across all arms/models for
    paired comparability.
L8  d(N) is a deterministic function of the FULL small-prime phase vector given window
    length: the augmented model nests the baseline's d-information, so any positive
    dR2 is structure beyond the union-fraction (overlap density, position-size interplay).
L9  Standardize columns by TRAIN mean/std before lstsq (OLS predictions scale-invariant;
    done purely for conditioning).
"""
import json, math, os, time
import numpy as np

SEED = 20260901
OUTDIR = "/tmp/exp41_phase"
os.makedirs(OUTDIR, exist_ok=True)
T0 = time.time()

RES = {"exp": 482, "codename": "PHASE-FEATURES", "seed": SEED,
       "hypotheses": {
           "H1": "phase o_p (p in {3,5,7,11,13}, cos/sin+qr) lifts OOS R2 >= +0.05 over (w,d), u=2.5",
           "H2": "dR2_phase cross-window < 0.5 * dR2_phase same-window (window-locality)",
           "H3": "augmented (phase<=30) reaches R2 >= 0.70 (same-window, u=2.5)"},
       "barriers": ["(5) all features are residue dials of METHOD input statistics - zero factor information",
                    "(8) QS calibration"],
       "ledger": [
           "L0 inherited prior attempt quarantined to attic_prev_attempt/ after audit: broken cross-window arm (trained AND tested on w2 targets), wrong offset definition, non-QR/o=0 collision, global-only B, stale R2=1.0 checkpoints",
           "L1 j=1..240 (v_0<=0 excluded by positivity assert)",
           "L2 phase encoding unit-circle (cos,sin)+qr indicator; non-QR=(0,0,0)",
           "L3 fixed prime sets for fixed OLS design matrix",
           "L4 features frozen across arms; targets recomputed per window half (own median-v B)",
           "L5 one strip pass to PB=4200 -> (rem,maxp); smooth@B iff rem==1 and maxp<=B",
           "L6 bootstrap: 300 paired resamples of test rows, coefficients frozen",
           "L7 shared 900/300 partition across arms",
           "L8 augmented model nests d-information (d is a function of the phase vector)",
           "L9 train-stat standardization for conditioning",
           "L14 first run had NO intercept column (standardized features cannot carry the target mean -> R2 ~ -9.6 baseline): fixed with explicit unstandardized ones-column; ledger kept for the record"],
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
SMALL_D = (2, 3, 5, 7, 11, 13)
PHASE13 = [3, 5, 7, 11, 13]
PHASE_EXT = [17, 19, 23, 29]

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
PH = {}   # N -> {p: (cos, sin, qr)}
for i, (N, s, vals, stripped) in enumerate(records):
    w = 0.0
    for p in PRIMES_ODD_LE400:
        if euler(N, p) == 1:
            w += 2.0 / p
    W[i] = w
    dd = 0
    for v in vals:
        if v % 2 == 0 or v % 3 == 0 or v % 5 == 0 or v % 7 == 0 or v % 11 == 0 or v % 13 == 0:
            dd += 1
    D[i] = dd / J
    row = {}
    for p in PHASE13 + PHASE_EXT:
        if euler(N, p) == 1:
            Nm = N % p
            r1 = min(x for x in range(p) if (x * x - Nm) % p == 0)   # smaller root
            o = (r1 - s) % p                                         # spec definition
            a = 2.0 * math.pi * o / p
            row[p] = (math.cos(a), math.sin(a), 1.0)
        else:
            row[p] = (0.0, 0.0, 0.0)
    PH[N] = row

qr_rates = {p: float(np.mean([PH[N][p][2] for N in NS])) for p in PHASE13 + PHASE_EXT}
ledger(f"L12 feature sanity: QR rates {({k: round(v,3) for k,v in qr_rates.items()})}; "
       f"corr(w, y_all@2.5)={float(np.corrcoef(W, TARGETS[2.5]['all'])[0,1]):.3f}, "
       f"corr(d, y_all@2.5)={float(np.corrcoef(D, TARGETS[2.5]['all'])[0,1]):.3f}")
checkpoint("features", {"qr_rates": qr_rates,
                        "w_mean": float(W.mean()), "d_mean": float(D.mean())})

def build_X(model):
    cols = []
    if model != "phonly":
        cols += [W, D]
    primes = []
    if model in ("p13", "p30"):
        primes += PHASE13
    if model == "p30":
        primes += PHASE_EXT
    if model == "phonly":
        primes = PHASE13 + PHASE_EXT
    for p in primes:
        cols.append(np.array([PH[N][p][0] for N in NS]))
        cols.append(np.array([PH[N][p][1] for N in NS]))
        cols.append(np.array([PH[N][p][2] for N in NS]))
    return np.column_stack(cols)

MODELS = ["base", "p13", "p30", "phonly"]
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
    A = np.column_stack([(Xtr - mu) / sd, np.ones(len(Xtr))])    # L14: explicit intercept
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
            f"p13={arm['p13']['r2_test']:.4f} (dR2={arm['p13']['dR2']:+.4f}) "
            f"p30={arm['p30']['r2_test']:.4f} (dR2={arm['p30']['dR2']:+.4f}) "
            f"phonly={arm['phonly']['r2_test']:.4f}")
        checkpoint("arms_partial", ARMS)

# ------------------------------------------------------------ stage 6: verdicts
a_same = ARMS["u2.5_same"]
a_cross = ARMS["u2.5_cross"]
d_same_p13 = a_same["p13"]["dR2"]
ci_same_p13 = a_same["p13"]["dR2_boot_ci95"]
d_cross_p13 = a_cross["p13"]["dR2"]
ci_cross_p13 = a_cross["p13"]["dR2_boot_ci95"]
d_same_p30 = a_same["p30"]["dR2"]
r2_aug_p30 = a_same["p30"]["r2_test"]

H1_strong = bool(d_same_p13 >= 0.05 and ci_same_p13[0] > 0)
H1_point = bool(d_same_p13 >= 0.05)
if d_same_p13 > 0:
    ratio = d_cross_p13 / d_same_p13
    H2 = bool(d_cross_p13 < 0.5 * d_same_p13)
else:
    ratio = None
    H2 = None
H3 = bool(r2_aug_p30 >= 0.70)

if H1_point:
    name = "PHASE-WINDOW-LOCAL" if H2 else "PHASE-TRANSFERS"
elif d_same_p13 > 0:
    name = "PHASE-SUBTHRESHOLD-LIFT"
else:
    name = "PHASE-NO-LIFT"
VERDICT = f"{name}/H3-{'PASS' if H3 else 'FAIL'}"

RES["verdict"] = {
    "name": VERDICT,
    "u2.5": {
        "dR2_p13_same": d_same_p13, "ci95_same_p13": ci_same_p13,
        "dR2_p13_cross": d_cross_p13, "ci95_cross_p13": ci_cross_p13,
        "ratio_cross_over_half": ratio,
        "dR2_p30_same": d_same_p30, "ci95_same_p30": a_same["p30"]["dR2_boot_ci95"],
        "R2_base_same": a_same["base"]["r2_test"], "R2_base_cross": a_cross["base"]["r2_test"],
        "R2_aug_p30_same": r2_aug_p30,
        "H1_strong": H1_strong, "H1_point": H1_point, "H2": H2, "H3": H3}}
RES["arms"] = ARMS
checkpoint("verdicts")

log("=" * 72)
log(f"VERDICT: {VERDICT}")
log(f"H1 (>=+0.05 same-window lift, p13): point={d_same_p13:+.4f} CI95=[{ci_same_p13[0]:+.4f},{ci_same_p13[2]:+.4f}]"
    f" -> {'STRONG-PASS' if H1_strong else ('POINT-PASS' if H1_point else 'FAIL')}")
log(f"H2 (cross < half of same): same={d_same_p13:+.4f} cross={d_cross_p13:+.4f} "
    f"ratio={('%.3f' % ratio) if ratio is not None else 'NA'} -> {H2}")
log(f"H3 (aug p30 R2 >= 0.70): {r2_aug_p30:.4f} -> {H3}")
log("baseline reproduction check vs paper-145 (~0.59): "
    f"same-window base R2 = {a_same['base']['r2_test']:.4f}; leak-free split base = {a_cross['base']['r2_test']:.4f}")
np.savez(os.path.join(OUTDIR, "data482.npz"),
         W=W, D=D, TR=TR, TE=TE,
         **{f"y_{u}_{k}": TARGETS[u][k] for u in US for k in ("all", "first", "second")})
log("DONE", round(time.time() - T0, 1), "s")

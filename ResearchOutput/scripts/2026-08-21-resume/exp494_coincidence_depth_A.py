#!/usr/bin/env python3
"""EXP 494 COINCIDENCE-DEPTH, agent A (round-43). Seed 20260925. Clean implementation;
builder conventions inherited VERBATIM from exp482/exp484 (papers 145/147/152).

Context: the per-N yield dial's best features are footprint mass w(N)=sum(2/p |
p<=400 QR) and pair-coincidence counts c_pq(N)=#{j<=240: p|v_j AND q|v_j} (paper-152
transfer ratio ~0.51 across disjoint windows). OPEN QUESTION: what IS the coincidence
signal? Hypothesis space: coincidences measure CLUSTERING of divisibility hits
(second-order structure beyond marginal densities).

PRE-STATED HYPOTHESES (recorded before data generation):
H1 (determinism): c_pq is DETERMINISTIC given the phases -- pre-stated form
    c_pq ~= 240*gcd(p,q)/(pq)*(overlap factor of root positions); operationalized as
    the EXACT CRT count from the root classes; test corr(pred, measured) > 0.9;
    regression companion: exact-CRT features must reproduce the measured-pair lift.
H2 (clumping): adding gap-variance (clumping) features lifts test R^2 by >= +0.02
    over the paper-152 pair model.
H3 (union proxy): pair features were proxying d(N); non-degenerate rule (L4): pairs
    proxy d iff their incremental lift over (w,d) has bootstrap CI containing 0.

BARRIERS:
(5) all features are residue dials of METHOD input statistics -- zero factor
    information; these models predict sieving yield, never factor identity.
(8) QS calibration: this entire exercise is QS yield-calibration science.

DESIGN: 800 semiprimes bitlen 44 (p,q uniform prime [2^21,2^22)); v_j=j(2s+j)-(s^2-N),
j=1..240 (exp482 verbatim); u=2.5, B=exp(ln vmed/u) per N, strip to PB=4200;
features w,d; measured c_pq (slot fractions, 10 pairs of {3,5,7,11,13}); exact-CRT
c_pq; gap-variance clumping (+hit indicators); marginal hit fractions; OLS 600/200;
paired bootstrap 300.

METHOD LEDGER (decisions recorded BEFORE data):
L1 conventions verbatim from exp482/exp484 (v_j formula j=1..240; w over odd primes
    <=400 euler==1 weight 2/p; d = union fraction over {2,3,5,7,11,13}; pair =
    INTERSECTION slot fractions c/240; chunked-gcd strip PB=4200 -> (rem,maxp);
    smooth@B iff rem==1 & maxp<=B; B per N from full-window median).
L2 population seed 20260925 (NOT exp482's 20260901): fresh independent draw of 800.
L3 expectation bookkeeping (recorded before data): p|v_j iff x^2=N mod p solvable ->
    TWO root classes per prime -> 4 combined CRT classes per coprime pair;
    E[c | both QR] = 4*240/(pq); averaging also over the QR lottery (P(both QR)=1/4,
    independent Legendre draws) gives E[c] = 240/(pq) = EXACTLY the pre-stated
    240*gcd(p,q)/(pq) read UNCONDITIONALLY. Both calibrations reported.
L4 H3 FWL/span amendments (recorded before data): partialling c_pq on d is degenerate
    (d is a base column -> coefficients unchanged by FWL); a d-projection of the pair
    block lies in span{d} -> its lift is identically 0 BY CONSTRUCTION. Non-degenerate
    rule: base ALREADY controls d, so pairs proxy d iff incremental lift over (w,d)
    ~ 0; PASS-proxy iff paired-bootstrap CI of dR2(pairs-base) contains 0, FAIL iff it
    excludes 0. dproj arm kept only to DOCUMENT the span argument empirically.
L5 clumping encoding: gapvar = population variance of gaps between consecutive hit
    indices (0.0 if <2 hits) PLUS explicit has_hits indicator column (avoids the
    exp482 L2 non-QR/o=0 collision; a non-residue prime has NO hits ever, ~50% of N).
    Bin-count variance (10 bins of 24) is SECONDARY/exploratory only.
L6 arms: base(w,d); pairs(+10 measured c_pq = paper-152 replication); crt(+10
    exact-CRT c_pq, H1); var(pairs+gapvar+indicators, H2); dproj(documentary);
    marg(+5 marginal hit fractions) and varbin(pairs+binvar) are EXPLORATORY post-hoc
    diagnostics for the open question (marginals vs coincidences), NOT pre-stated.
L7 shared 600/200 N-partition (SEED+1 permutation); train-stat standardization +
    explicit unstandardized intercept (exp482 L9/L14).
L8 bootstrap: 300 paired resamples of the 200 test rows, coefficients frozen (SEED+2).
L9 determinism audit: measured c_pq must EQUAL exact CRT count for every (N,pair)
    (two routes: direct mods vs root-class CRT); any mismatch aborts.
L10 H1 secondary benchmark: marginal-product predictor n_p*n_q/240 vs exact-CRT --
    separates count-fluctuation info from phase-alignment info.

POST-RUN AUDIT NOTES (run 1 happened 03:01, recorded before run 2):
L25 COLLISION: a parallel round-43 agent sharing /tmp/exp43_cdepth/ overwrote
    exp494_coincidence_depth.py at 03:04 with its own inline variant of the same
    experiment number/codename. Run-1 outputs (written 03:01:47) snapshotted to
    result_exp494A_run1_pre-fix_snapshot.json / run_A_run1.log BEFORE their overwrite
    reached them; this rerun writes ONLY _A-suffixed files (result_exp494A.json,
    data494A.npz, run_A.log). Run-1 verdicts remain valid evidence (identical
    seed/population/features; only descriptives/H3-rule differ in run 2).
L26 RUN-1 AUDIT FINDINGS fixed here: (a) run-1 calibration ratios vs 4*240/pq were
    ~0.25 on ALL ten pairs -- diagnosed as L3's unconditional-vs-conditional
    bookkeeping (the x1/4 IS the QR lottery): not a bug, now two separate ratios;
    (b) run-1 H3 lift-ratio used the span-degenerate dproj arm (identically 0 by L4)
    -- replaced by the CI-based rule of L4.
"""
import json, math, os, time
from itertools import combinations
import numpy as np

SEED = 20260925
OUTDIR = "/tmp/exp43_cdepth"
os.makedirs(OUTDIR, exist_ok=True)
T0 = time.time()
RESULT_PATH = os.path.join(OUTDIR, "result_exp494A.json")

RES = {"exp": 494, "codename": "COINCIDENCE-DEPTH-A", "seed": SEED,
       "hypotheses": {
           "H1": "corr(exact-CRT prediction, measured c_pq) > 0.9; companion: crt arm == pairs arm",
           "H2": "gap-variance (clumping) lifts test R2 >= +0.02 over the paper-152 pair model",
           "H3": "pairs proxy d: incremental lift of pairs over (w,d) ~ 0 (CI contains 0)"},
       "barriers": ["(5) all features are residue dials of METHOD input statistics - zero factor information; "
                    "these models predict sieving yield, never factor identity",
                    "(8) QS calibration: this entire exercise is QS yield-calibration science"],
       "ledger": [],
       "stages": {}}

def log(*a):
    print(" ".join(str(x) for x in a), flush=True)

def ledger(msg):
    RES["ledger"].append(msg)
    log("[LEDGER]", msg)

def checkpoint(stage, data=None):
    if data is not None:
        RES["stages"][stage] = data
    RES["saved_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    RES["elapsed_s"] = round(time.time() - T0, 1)
    with open(RESULT_PATH, "w") as f:
        json.dump(RES, f, indent=1, default=float)
    log("[checkpoint]", stage)

rng = np.random.default_rng(SEED)

try:
    import gmpy2
    HAVE_GMPY2 = True
except Exception:
    HAVE_GMPY2 = False
log("gmpy2:", HAVE_GMPY2)

def euler(a, p):
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
PAIRS = list(combinations(P5, 2))

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
N_PER = 800
J = 240

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
ledger(f"L20 population: {len(NS)} distinct semiprimes bitlen 44, p,q uniform prime "
       f"[2^21,2^22), {DRAWS} candidate draws, seed {SEED}")
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

# --------------------------------------------------- stage 3: target u=2.5
U = 2.5
y_all = []
Bs = []
for N, s, vals, stripped in records:
    vmed = float(np.median(np.asarray(vals, dtype=float)))
    B = math.exp(math.log(vmed) / U)
    c = sum(1 for rem, mx in stripped if rem == 1 and mx <= B)
    y_all.append(c / J)
    Bs.append(B)
Y = np.array(y_all)
ledger(f"L21 target u={U}: mean yield {Y.mean():.4f}, std {Y.std():.4f}, "
       f"mean B {float(np.mean(Bs)):.1f}")
checkpoint("target", {"u": U, "mean_yield": float(Y.mean()), "std_yield": float(Y.std()),
                      "B_mean": float(np.mean(Bs))})

# ------------------------------------------------------- stage 4: features
W = np.zeros(len(records))
D = np.zeros(len(records))
PC = np.zeros((len(records), len(PAIRS)))       # measured pair slot fractions
PCP = np.zeros((len(records), len(PAIRS)))      # exact-CRT pair slot fractions
MARG = np.zeros((len(records), len(P5)))        # per-prime hit fractions
GAPVAR = np.zeros((len(records), len(P5)))      # gap variance (0 if <2 hits)
HASHIT = np.zeros((len(records), len(P5)))      # explicit indicator
BINVAR = np.zeros((len(records), len(P5)))      # secondary: bin-count variance
ROOTS = []                                      # per N: {p: root classes mod p}
mismatch = 0

for i, (N, s, vals, stripped) in enumerate(records):
    w = 0.0
    for p in PRIMES_ODD_LE400:
        if euler(N, p) == 1:
            w += 2.0 / p
    W[i] = w
    arr = np.array(vals, dtype=np.int64)        # |v_j| < ~2.1e9 << 2^63: exact
    masks = {p: (arr % p == 0) for p in P5}
    m2 = (arr % 2 == 0)
    D[i] = float((m2 | masks[3] | masks[5] | masks[7] | masks[11] | masks[13]).sum()) / J
    rts = {}
    for k, p in enumerate(P5):
        if euler(N, p) == 1:
            Nm = N % p
            rr = sorted(x for x in range(p) if (x * x - Nm) % p == 0)
            cls = sorted({(x - s) % p for x in rr})
            hits = []
            for c_ in cls:
                start = c_ if c_ >= 1 else p
                hits.extend(range(start, J + 1, p))
            hits = sorted(set(hits))
            if i < 5:   # audit: AP construction == direct mods
                brute = [j for j in range(1, J + 1) if arr[j - 1] % p == 0]
                assert brute == hits, f"AP/mods mismatch N={N} p={p}"
        else:
            cls = []
            hits = []
        rts[p] = cls
        MARG[i, k] = len(hits) / J
        HASHIT[i, k] = 1.0 if hits else 0.0
        if len(hits) >= 2:
            GAPVAR[i, k] = float(np.var(np.diff(np.array(hits))))
        bins_ = [0] * 10
        for j in hits:
            bins_[(j - 1) // 24] += 1
        BINVAR[i, k] = float(np.var(bins_))
    ROOTS.append(rts)
    for k, (p, q) in enumerate(PAIRS):
        PC[i, k] = float((masks[p] & masks[q]).sum()) / J
        cp_, cq_ = rts[p], rts[q]
        if not cp_ or not cq_:
            pred = 0
        else:
            pq_ = p * q
            iq_p = pow(q, -1, p)
            ip_q = pow(p, -1, q)
            pred = 0
            for c1 in cp_:
                for c2 in cq_:
                    t = (c1 * q * iq_p + c2 * p * ip_q) % pq_
                    start = t if t >= 1 else pq_
                    if start <= J:
                        pred += 1 + (J - start) // pq_
        PCP[i, k] = pred / J
        if pred != int(round(PC[i, k] * J)):
            mismatch += 1

assert mismatch == 0, f"L9 determinism audit FAILED: {mismatch} (N,pair) mismatches"
ledger(f"L22 determinism audit L9: measured c_pq == exact CRT count for ALL "
       f"{len(records) * len(PAIRS)} (N,pair) points (0 mismatches)")

qr_rates = {p: float(np.mean([1.0 if ROOTS[i][p] else 0.0 for i in range(len(records))]))
            for p in P5}
checkpoint("features", {"qr_rates": qr_rates,
                        "w_mean": float(W.mean()), "d_mean": float(D.mean()),
                        "mismatch": int(mismatch)})

# ------------------------------------------- stage 5: H1 descriptive statistics
pc_flat, pcp_flat, mp_flat = [], [], []
per_pair = {}
for k, (p, q) in enumerate(PAIRS):
    a, b = PC[:, k], PCP[:, k]
    margprod = MARG[:, P5.index(p)] * MARG[:, P5.index(q)]   # independence benchmark
    r_exact = float(np.corrcoef(a, b)[0, 1])
    r_marg = float(np.corrcoef(a, margprod)[0, 1])
    mean_c = float(a.mean()) * J
    exp_cond = 4 * J / (p * q)          # E[c | both QR], random phases
    exp_unc = J / (p * q)               # E[c] unconditional = pre-stated 240*gcd/(pq)
    both = (MARG[:, P5.index(p)] > 0) & (MARG[:, P5.index(q)] > 0)
    cond_mean = float(a[both].mean()) * J if both.any() else float("nan")
    cv = float(a.std() / max(a.mean(), 1e-12))
    per_pair[f"{p}x{q}"] = {"mean_count": mean_c,
                            "E_random_phase_uncond": exp_unc,
                            "calib_ratio_uncond": mean_c / exp_unc,
                            "E_random_phase_cond_bothQR": exp_cond,
                            "cond_mean_given_bothQR": cond_mean,
                            "calib_ratio_cond": cond_mean / exp_cond,
                            "cv": cv,
                            "corr_measured_vs_crt": r_exact,
                            "corr_measured_vs_margprod": r_marg,
                            "zero_frac": float(np.mean(a == 0))}
    pc_flat.append(a); pcp_flat.append(b); mp_flat.append(margprod)

pc_flat = np.concatenate(pc_flat); pcp_flat = np.concatenate(pcp_flat)
mp_flat = np.concatenate(mp_flat)
pooled_corr_crt = float(np.corrcoef(pc_flat, pcp_flat)[0, 1])
pooled_corr_marg = float(np.corrcoef(pc_flat, mp_flat)[0, 1])
H1_corr = pooled_corr_crt > 0.9
rat_u = [v["calib_ratio_uncond"] for v in per_pair.values()]
rat_c = [v["calib_ratio_cond"] for v in per_pair.values()]
ledger(f"L23 H1 descriptives: pooled corr(measured, CRT)={pooled_corr_crt:.6f} "
       f"(threshold 0.9), pooled corr(measured, margprod n_p*n_q/240)={pooled_corr_marg:.4f}; "
       f"calibration measured/E: unconditional(240/pq) [{min(rat_u):.3f},{max(rat_u):.3f}], "
       f"conditional-on-both-QR(4*240/pq) [{min(rat_c):.3f},{max(rat_c):.3f}]")
checkpoint("h1_descriptives", {"pooled_corr_crt": pooled_corr_crt,
                               "pooled_corr_margprod": pooled_corr_marg,
                               "H1_corr_pass": bool(H1_corr),
                               "per_pair": per_pair})

# ------------------------------------------------------- stage 6: fits
perm = np.random.default_rng(SEED + 1).permutation(len(NS))
TR, TE = perm[:600], perm[600:]

def r2(yt, yp):
    yt = np.asarray(yt, float); yp = np.asarray(yp, float)
    sst = float(((yt - yt.mean()) ** 2).sum())
    if sst <= 0:
        return float("nan")
    return float(1.0 - ((yt - yp) ** 2).sum() / sst)

# d-projection of the pair block: fitted on TRAIN rows only (L4; documentary arm)
PCPROJ = np.zeros_like(PC)
for k in range(len(PAIRS)):
    A = np.column_stack([D[TR], np.ones(len(TR))])
    coef, *_ = np.linalg.lstsq(A, PC[TR, k], rcond=None)
    PCPROJ[:, k] = D * coef[0] + coef[1]
proj_r2 = [float(r2(PC[TR, k], PPCOL[TR])) for k, PPCOL in enumerate(PCPROJ.T)]

def build_X(model):
    cols = [W, D]
    if model == "pairs":
        cols.append(PC)
    elif model == "crt":
        cols.append(PCP)
    elif model == "var":
        cols.append(np.column_stack([PC, GAPVAR, HASHIT]))
    elif model == "dproj":
        cols.append(PCPROJ)
    elif model == "marg":
        cols.append(MARG)
    elif model == "varbin":
        cols.append(np.column_stack([PC, BINVAR, HASHIT]))
    return np.column_stack(cols)

MODELS = ["base", "pairs", "crt", "var", "dproj", "marg", "varbin"]
XMAT = {m: build_X(m) for m in MODELS}
ledger(f"L24 model dims: " + ", ".join(f"{m}:{XMAT[m].shape[1]}cols" for m in MODELS)
       + f"; d-projection train R2 per pair {[round(x, 3) for x in proj_r2]}")

def fit_eval(X):
    Xtr, Xte = X[TR], X[TE]
    mu = Xtr.mean(0); sd = Xtr.std(0)
    sd[sd < 1e-12] = 1.0
    A = np.column_stack([(Xtr - mu) / sd, np.ones(len(Xtr))])
    Bm = np.column_stack([(Xte - mu) / sd, np.ones(len(Xte))])
    coef, *_ = np.linalg.lstsq(A, Y[TR], rcond=None)
    ptr, pte = A @ coef, Bm @ coef
    return r2(Y[TR], ptr), r2(Y[TE], pte), pte

ARMS = {}
PREDS = {}
for m in MODELS:
    r2tr, r2te, pte = fit_eval(XMAT[m])
    ARMS[m] = {"r2_train": r2tr, "r2_test": r2te}
    PREDS[m] = pte
    log(f"arm {m}: r2_train={r2tr:.4f} r2_test={r2te:.4f}")
checkpoint("arms_partial", ARMS)

# ------------------------------------------------------------- bootstrap
BRNG = np.random.default_rng(SEED + 2)
yy = Y[TE]
NB = 300
DELTA_ARMS = [("pairs", "base"), ("crt", "base"), ("crt", "pairs"),
              ("var", "pairs"), ("dproj", "base"), ("marg", "base"),
              ("pairs", "marg"), ("varbin", "pairs")]
BOOT = {}
for mA, mB in DELTA_ARMS:
    ds = np.empty(NB)
    for b in range(NB):
        idx = BRNG.integers(0, len(yy), len(yy))
        ds[b] = r2(yy[idx], PREDS[mA][idx]) - r2(yy[idx], PREDS[mB][idx])
    lo, med, hi = (float(x) for x in np.percentile(ds, [2.5, 50, 97.5]))
    BOOT[f"{mA}-{mB}"] = {"point": ARMS[mA]["r2_test"] - ARMS[mB]["r2_test"],
                          "ci95": [lo, med, hi]}
    log(f"bootstrap dR2 {mA}-{mB}: point={BOOT[f'{mA}-{mB}']['point']:+.4f} "
        f"CI95=[{lo:+.4f},{hi:+.4f}]")
checkpoint("fits_bootstrap", {"arms": ARMS, "boot": BOOT})

# ------------------------------------------------------- stage 7: verdicts
dR2_pairs = ARMS["pairs"]["r2_test"] - ARMS["base"]["r2_test"]
dR2_crt = ARMS["crt"]["r2_test"] - ARMS["base"]["r2_test"]
dR2_var = ARMS["var"]["r2_test"] - ARMS["pairs"]["r2_test"]
dR2_dproj = ARMS["dproj"]["r2_test"] - ARMS["base"]["r2_test"]
dR2_marg = ARMS["marg"]["r2_test"] - ARMS["base"]["r2_test"]
dR2_varbin = ARMS["varbin"]["r2_test"] - ARMS["pairs"]["r2_test"]

H1_pass = bool(H1_corr and mismatch == 0)
equiv_point = dR2_crt - dR2_pairs
equiv_ci = BOOT["crt-pairs"]["ci95"]
EQ = bool(abs(equiv_point) <= 0.005)

H2_pass = bool(dR2_var >= 0.02)
H2_ci = BOOT["var-pairs"]["ci95"]

if dR2_pairs < 0.002:
    H3 = None
    H3_name = "NO-PAIR-LIFT"
else:
    # Non-degenerate H3 rule (L4): base ALREADY contains d; if pairs merely proxied d,
    # their incremental lift over (w,d) would be ~0. PASS-proxy iff the paired-bootstrap
    # CI of dR2(pairs-base) contains 0; FAIL iff it excludes 0.
    pb_ci = BOOT["pairs-base"]["ci95"]
    if pb_ci[0] > 0:
        H3, H3_name = False, "NOT-D-PROXY"
    elif pb_ci[2] <= 0:
        H3, H3_name = True, "D-PROXY"
    else:
        H3, H3_name = None, "PARTIAL-D"

# secondary: residual of the pairs model vs clumping features (test rows)
resid = yy - PREDS["pairs"]
resid_clump_corr = {}
for k, p in enumerate(P5):
    resid_clump_corr[f"gapvar_{p}"] = float(np.corrcoef(resid, GAPVAR[TE, k])[0, 1])
    resid_clump_corr[f"hashit_{p}"] = float(np.corrcoef(resid, HASHIT[TE, k])[0, 1])

# verdict name
if not H1_pass:
    core = "COINCIDENCE-NOT-DETERMINISTIC"
elif EQ:
    core = "COINCIDENCE-IS-PHASE-ARITHMETIC"
else:
    core = "COINCIDENCE-PHASE-PLUS-EXTRA"
h2_tag = "CLUMP-LIFT" if H2_pass else "CLUMP-NULL"
VERDICT = f"{core}/{h2_tag}/{H3_name}"
RES["verdict"] = {
    "name": VERDICT,
    "H1_pass": H1_pass, "pooled_corr_crt": pooled_corr_crt,
    "regression_equivalence": {"pass": EQ, "point": equiv_point, "ci95": equiv_ci},
    "H2_pass": H2_pass, "dR2_var_over_pairs": dR2_var, "H2_ci95": H2_ci,
    "H3_name": H3_name, "H3_pass": H3, "pairs_base_ci95": BOOT["pairs-base"]["ci95"],
    "dR2_pairs_over_base": dR2_pairs, "dR2_crt_over_base": dR2_crt,
    "dR2_dproj_over_base": dR2_dproj,
    "dR2_marg_over_base": dR2_marg, "dR2_varbin_over_pairs": dR2_varbin,
    "R2_base": ARMS["base"]["r2_test"], "R2_pairs": ARMS["pairs"]["r2_test"],
    "residual_clump_corr": resid_clump_corr}
RES["arms"] = ARMS
RES["boot"] = BOOT
checkpoint("verdicts")

log("=" * 72)
log(f"VERDICT: {VERDICT}")
log(f"H1 determinism: corr={pooled_corr_crt:.6f} -> {'PASS' if H1_pass else 'FAIL'}; "
    f"crt-vs-pairs lift diff point={equiv_point:+.6f} -> {'EQUIV' if EQ else 'EXTRA'}")
log(f"H2 clumping: dR2(var-pairs)={dR2_var:+.4f} CI=[{H2_ci[0]:+.4f},{H2_ci[2]:+.4f}] -> "
    f"{'PASS' if H2_pass else 'FAIL'}; max|corr(residual,gapvar)|="
    f"{max(abs(v) for v in resid_clump_corr.values() if v.startswith('g')) if False else max(abs(resid_clump_corr[f'gapvar_{p}']) for p in P5):.3f}")
log(f"H3 union-proxy: pairs-over-base lift={dR2_pairs:+.4f} "
    f"CI=[{BOOT['pairs-base']['ci95'][0]:+.4f},{BOOT['pairs-base']['ci95'][2]:+.4f}] -> {H3_name}")
log(f"exploratory: marg-over-base={dR2_marg:+.4f} CI=[{BOOT['marg-base']['ci95'][0]:+.4f},"
    f"{BOOT['marg-base']['ci95'][2]:+.4f}]; pairs-over-marg={BOOT['pairs-marg']['point']:+.4f} "
    f"CI=[{BOOT['pairs-marg']['ci95'][0]:+.4f},{BOOT['pairs-marg']['ci95'][2]:+.4f}]")
log(f"anchors: R2 base={ARMS['base']['r2_test']:.4f} (paper-145 ~0.59), "
    f"pairs={ARMS['pairs']['r2_test']:.4f}")
np.savez(os.path.join(OUTDIR, "data494A.npz"),
         W=W, D=D, Y=Y, TR=TR, TE=TE, PC=PC, PCP=PCP, PCPROJ=PCPROJ,
         MARG=MARG, GAPVAR=GAPVAR, HASHIT=HASHIT, BINVAR=BINVAR)
log("DONE", round(time.time() - T0, 1), "s")

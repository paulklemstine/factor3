#!/usr/bin/env python3
"""EXP 541 PERNDIAL-48-52 (round-59 #5). Population seeds 20261200..02.
Open cell from papers 145/147/152/163/172/181: the per-N relation-yield dial is
validated at bitlen 44 (paper 145), transferred to bitlen 48 (paper 147, slope
0.898 in band); the prime-power term pp_sum found at +0.089 in paper 172 did NOT
replicate across fresh bitlen-44 populations (paper 181 / exp 515: dR2_pp ~ 0,
mean R2 0.502 < 0.55). OPEN: bitlen 52 with the FULL augmented dial.

CONSTRUCTIONS VERBATIM from exp515/exp506/exp505 (clean-protocol family):
bitlen-b balanced window [isqrt(2^(2b-1))+1, isqrt(2^(2b)-1)) with exact-bitlen
enforcement, inter-prime gap U[1,1e5); sq = isqrt(N);
V = j*(2*sq+j) + (sq*sq - N)  (Fermat offsets), j=1..240;
vmed POOLED PER POPULATION; B(u) = max(int(round(exp(ln(vmed)/u))), 50);
strip ONCE to BMAX = max over u; smooth@u iff rem==1 AND lpf <= B(u);
rate(N,u) = fraction of the 240 offsets smooth.  Single u target here: 3.5.
w dial = sum(2/q | odd q<=400, (N|q)=+1 via Euler criterion); qrc(<=100) carried
for the descriptive family arm only.
d   = fraction of the 240 values divisible by >=1 prime in {2,3,5,7,11,13}.
pp_sum = sum over ODD p<=13 {3,5,7,11,13} of fraction of values with p^2 | v
  (brief wording "count of values divisible by p^2 for odd p<=13", exp506
  sum-of-fractions convention; p=2-inclusive variant pp_sum2 descriptive).

ARMS (incremental nesting, pre-stated; features exactly as briefed):
  M0      = [1]                      (intercept-only baseline)
  Mw      = [1, w]                   (paper-145 footprint dial)
  Mwd     = [1, w, d]
  Mfull   = [1, w, d, pp_sum]        (the FULL augmented dial, the H1 arm)
Increments reported: dR2_w = Mw-M0, dR2_d = Mwd-Mw, dR2_pp = Mfull-Mwd,
each with paired bootstrap CI.  Descriptive sensitivity arm:
  Mfam    = [1, qrc, w, d, pp_sum]   (exp515 family arm, for comparability)
  Mb_pp2  = [1, w, d, pp_sum2]       (pp includes p=2)

PROTOCOL (pre-stated): populations 1200 semiprimes x {44,48,52} x seeds
20261200..02.  PRIMARY transfer fits: OLS fit on POOLED b44 rows (3 seeds,
3600 rows) -> predict pooled b48 and pooled b52 populations at u=3.5;
calibration slope = OLS slope of observed rate on predicted rate (WITH
intercept).  Per-seed transfers (fit 1200@44 -> test 1200@target, same seed)
descriptive.  Bootstrap: 300 resamples; per resample draw train indices and
test indices independently with replacement from the pooled sets, REFIT ALL
ARMS on boot-train, evaluate on boot-test; percentile CIs on transfer R2,
slopes and dR2 increments; boot indices shared across arms within a resample
(paired comparisons).  Analysis seed stream separate from population stream.

PRE-STATED HYPOTHESES (written BEFORE any data collection):
  H1: the full augmented dial Mfull achieves out-of-sample R^2 >= 0.45 at
      u=3.5 on bitlen 52 (train(44) -> test(52) transfer, point estimate).
  H2: transfer from the bitlen-44 fit has calibration slope in [0.8, 1.25]
      (primary: test(52); test(48) co-reported).
  H3: the prime-power term adds dR2_pp >= +0.02 R^2 at bitlen 52 (test(52),
      point estimate; extends or refutes paper 172 vs paper 181).

DECISION RULES (pre-stated):
  Band rule: thresholds scored on POINT estimates per the brief wording;
  bootstrap CIs reported alongside (PASS-with-CI when CI_low > 0).
  Verdict names:
    H1 & H2 & H3                -> PERNDIAL-52-FULLY-VALIDATED
    H1 & H2 & ~H3               -> PERNDIAL-52-VALIDATED-PP-ABSENT
    H1 & ~H2                    -> PERNDIAL-52-MISCALIBRATED-TRANSFER
    ~H1 with R2_52 >= 0.25      -> PERNDIAL-52-PARTIAL-TRANSFER
    else                        -> PERNDIAL-52-ABSENT

# BARRIERS (standard lines, verbatim exp500/exp501/exp503/exp505/exp506/exp515):
#   Barrier 5 (structural orthogonality): w/d/pp_sum are N-only natural
#   coordinates; the dial predicts relation yield (difficulty), not (p,q) -
#   no which-factor claim made or tested.
#   Barrier 8 (known-method-in-disguise): the measured object is the QS/CFRAC
#   relation-yield dial - a cost predictor FOR known methods, not a new route.
"""
import json, time, math, datetime, os, sys
import numpy as np
import gmpy2
from sympy import primerange, nextprime

POP_SEEDS = [20261200, 20261201, 20261202]   # one replicate each of {44,48,52}
ANALYSIS_SEED = 20261203                     # separate analysis stream
BITLENS = [44, 48, 52]
NN, W = 1200, 240
U = 3.5
D_PRIMES = [2, 3, 5, 7, 11, 13]              # any-hit set for d (verbatim exp506)
PP_ODD = [3, 5, 7, 11, 13]                   # odd primes for pp_sum (this brief)
NBOOT = 300
T0 = time.time()
WORK = "/tmp/exp59_pd4852"

OUT = {"meta": {
    "exp": 541, "codename": "PERNDIAL-48-52", "round": 59,
    "population_seeds": POP_SEEDS, "analysis_seed_root": ANALYSIS_SEED,
    "Ns_per_population": NN, "values_window": W, "u_targets": [U],
    "bitlens": {"fit": 44, "test": BITLENS[1:]},
    "d_primes": D_PRIMES, "pp_odd_primes": PP_ODD, "nboot": NBOOT,
    "arms": {"M0": "[1]", "Mw": "[1, w]", "Mwd": "[1, w, d]",
             "Mfull": "[1, w, d, pp_sum]",
             "Mfam(descriptive)": "[1, qrc, w, d, pp_sum]",
             "Mb_pp2(descriptive)": "[1, w, d, pp_sum2]"},
    "constructions": "verbatim exp515/506/505 balanced-window family; Fermat "
                     "offsets j=1..240; vmed pooled per population",
    "prestated": {
        "H1": "Mfull transfer OOS R^2 >= 0.45 at u=3.5 on bitlen 52",
        "H2": "calibration slope (obs~pred, intercept) in [0.8, 1.25]; "
              "primary test(52)",
        "H3": "dR2_pp >= +0.02 at bitlen 52 (test(52))",
        "bands": "thresholds on point estimates; CIs reported (PASS-with-CI "
                 "if CI_low > 0)",
        "names": ["PERNDIAL-52-FULLY-VALIDATED", "PERNDIAL-52-VALIDATED-PP-ABSENT",
                  "PERNDIAL-52-MISCALIBRATED-TRANSFER",
                  "PERNDIAL-52-PARTIAL-TRANSFER", "PERNDIAL-52-ABSENT"]}}}

def ledger(event, **kw):
    rec = {"ts": datetime.datetime.now().isoformat(timespec="seconds"),
           "exp": 541, "codename": "PERNDIAL-48-52", "event": event,
           "t_s": round(time.time() - T0, 1)}
    rec.update(kw)
    with open(f"{WORK}/ledger_exp541.jsonl", "a") as f:
        f.write(json.dumps(rec, default=float) + "\n")

def checkpoint():
    OUT["saved_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    OUT["elapsed_s"] = round(time.time() - T0, 1)
    json.dump(OUT, open(f"{WORK}/result.json", "w"), indent=1, default=float)

def log(msg):
    print("[%7.1fs] %s" % (time.time() - T0, msg), flush=True)

os.makedirs(WORK, exist_ok=True)

# ------------------------------------------------------------- stage 0: start
ledger("start", pop_seeds=POP_SEEDS, workdir=WORK, nn=NN, window=W, u=U,
       prestated=OUT["meta"]["prestated"], barriers=["5", "8"],
       python=sys.version.split()[0], numpy=np.__version__, gmpy2=gmpy2.version())
checkpoint()
log("stage 0: ledger written (hypotheses pre-stated before data)")

primes_all = np.array(list(primerange(2, 40000)), dtype=np.int64)

WINDOWS = {}
BITLO, BITHI = {}, {}
for b in BITLENS:
    # exp515 verbatim: N in [2^(b-1), 2^b) -> sqrt candidates in
    # [isqrt(2^(b-1))+1, isqrt(2^b - 1)]
    WINDOWS[b] = (int(gmpy2.isqrt(1 << (b - 1))) + 1,
                  int(gmpy2.isqrt((1 << b) - 1)))
    BITLO[b], BITHI[b] = 1 << (b - 1), 1 << b

def draw_one(rng, bl):
    lo, hi = WINDOWS[bl]
    while True:
        r = int(rng.integers(lo, hi))
        p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, 10**5))))
        N = p * q
        if not (BITLO[bl] <= N < BITHI[bl]):
            continue
        return N, math.isqrt(N)

wr = list(primerange(3, 401))     # odd primes <= 400 (w dial + qrc source)
wr_arr = np.array(wr)
qrc_mask100 = wr_arr <= 100

def t_dial_and_qrc(Ns_list):
    """w/T dial (odd p<=400) and qrc(<=100), Euler criterion -- exp505 verbatim."""
    tw = np.zeros(len(Ns_list)); qrc = np.zeros(len(Ns_list))
    for N_i, N in enumerate(Ns_list):
        Nm = int(N)
        syms = [gmpy2.powmod(Nm % int(q), (int(q) - 1) // 2, int(q)) for q in wr_arr]
        qr400 = np.fromiter((s == 1 for s in syms), bool, len(wr_arr))
        tw[N_i] = (2.0 / wr_arr)[qr400].sum()
        qrc[N_i] = qr400[qrc_mask100].sum()
    return tw, qrc

def fermat_offsets(Ns_list, sqs):
    js = np.arange(1, W + 1, dtype=np.int64)
    sq = np.asarray(sqs, dtype=np.int64)[:, None]
    N = np.asarray(Ns_list, dtype=np.int64)[:, None]
    V = js[None, :] * (2 * sq + js[None, :]) + (sq * sq - N)
    assert (V > 0).all(), "positivity violated"
    assert V.dtype == np.int64 and V.max() < 2**62
    return V

def targets_and_value_features(V):
    """rate@(u=3.5) plus d13 and pp features from the SAME window."""
    vmed = float(np.median(V.astype(float)))
    Bu = max(int(round(math.exp(math.log(vmed) / U))), 50)
    Q = V.copy()
    lpf = np.zeros(V.shape, dtype=np.int64)
    strip_primes = primes_all[primes_all <= Bu]
    for p in strip_primes:
        while True:
            m = Q % p == 0
            if not m.any():
                break
            Q[m] //= p
            lpf[m] = p
    rate = ((Q == 1) & (lpf <= Bu)).mean(axis=1).astype(float)
    div_or = np.zeros(V.shape, dtype=bool)
    pp_masks_odd = [(V % (p * p) == 0) for p in PP_ODD]
    for p in D_PRIMES:
        div_or |= (V % p == 0)
    pp_odd_sum = np.sum([pm.mean(axis=1) for pm in pp_masks_odd], axis=0)
    pp_with2 = pp_odd_sum + (V % 4 == 0).mean(axis=1)
    return {"rate": rate, "d13": div_or.mean(axis=1).astype(float),
            "pp_sum": pp_odd_sum.astype(float), "pp_sum2": pp_with2.astype(float),
            "vmed": vmed, "B": Bu, "n_strip_primes": int(len(strip_primes))}

def build_population(seed, bl):
    # derived stream: one independent substream per (population seed, bitlen)
    rng_pop = np.random.default_rng(seed * 100 + bl)
    pairs = [draw_one(rng_pop, bl) for _ in range(NN)]
    Ns_list = [d[0] for d in pairs]; sqs = [d[1] for d in pairs]
    assert len(set(Ns_list)) == NN, "Ns must be unique"
    tw, qrc = t_dial_and_qrc(Ns_list)
    V = fermat_offsets(Ns_list, sqs)
    tgt = targets_and_value_features(V)
    return {"seed": seed, "bl": bl, "tw": tw, "qrc": qrc, **tgt}

def ols_fit(Xtr, ytr):
    coef, *_ = np.linalg.lstsq(Xtr, ytr, rcond=None)
    return coef

def r2_of(yt, yp):
    resid = yt - yp
    return 1.0 - (resid @ resid) / (((yt - yt.mean()) ** 2).sum())

def cal_slope(yt, yp):
    c = np.linalg.lstsq(np.column_stack([np.ones(len(yp)), yp]), yt, rcond=None)[0]
    return float(c[1]), float(c[0])

def design(pop, which):
    ones = np.ones(len(pop["tw"]))
    if which == "M0":
        return np.column_stack([ones])
    if which == "Mw":
        return np.column_stack([ones, pop["tw"]])
    if which == "Mwd":
        return np.column_stack([ones, pop["tw"], pop["d13"]])
    if which == "Mfull":
        return np.column_stack([ones, pop["tw"], pop["d13"], pop["pp_sum"]])
    if which == "Mfam":
        return np.column_stack([ones, pop["qrc"], pop["tw"], pop["d13"], pop["pp_sum"]])
    if which == "Mb_pp2":
        return np.column_stack([ones, pop["tw"], pop["d13"], pop["pp_sum2"]])
    raise ValueError(which)

PRIMARY_ARMS = ["M0", "Mw", "Mwd", "Mfull"]
INCR = [("dR2_w", "Mw", "M0"), ("dR2_d", "Mwd", "Mw"), ("dR2_pp", "Mfull", "Mwd")]

POPS = {}   # (seed, bl) -> population dict

# ============================================================ main build loop
for K, seed in enumerate(POP_SEEDS):
    for bl in BITLENS:
        key = (seed, bl)
        t1 = time.time()
        pop = build_population(seed, bl)
        POPS[key] = pop
        st = {"vmed": round(pop["vmed"], 1), "B": int(pop["B"]),
              "mean_rate": round(float(pop["rate"].mean()), 6),
              "mean_w": round(float(pop["tw"].mean()), 4),
              "std_rate": round(float(pop["rate"].std()), 6)}
        OUT.setdefault("populations", {})[f"s{seed}_b{bl}"] = st
        checkpoint(); ledger("pop_done", seed=seed, bl=bl, **st,
                             wall_s=round(time.time() - t1, 1))
        log("build s%d b%d: vmed=%.1f B=%d mean_rate=%.4f (%.1fs)"
            % (seed, bl, pop["vmed"], pop["B"], pop["rate"].mean(),
               time.time() - T0))
    np.savez_compressed(
        f"{WORK}/arrays_s{seed}.npz",
        **{f"{f}{bl}": POPS[(seed, bl)][f] for bl in BITLENS
           for f in ["tw", "qrc", "d13", "pp_sum", "pp_sum2", "rate"]})

# ------------------------------------------------------- stage: point transfers
log("stage: point transfers")
rng_an = np.random.default_rng(ANALYSIS_SEED)

def pooled(bl, fields):
    return {f: np.concatenate([POPS[(s, bl)][f] for s in POP_SEEDS]) for f in fields}

FIELDS = ["tw", "qrc", "d13", "pp_sum", "pp_sum2", "rate"]
TR44 = pooled(44, FIELDS)
TE = {bl: pooled(bl, FIELDS) for bl in (48, 52)}

def eval_transfer(tr, te, arms=PRIMARY_ARMS + ["Mfam", "Mb_pp2"]):
    """Fit every arm on tr, predict te; R2/slope per arm + increments."""
    ytr, yte = tr["rate"], te["rate"]
    out = {"R2": {}, "slope": {}, "icept": {}, "coef": {}, "n_train": len(ytr)}
    preds = {}
    for a in arms:
        Xt, Xe = design(tr, a), design(te, a)
        beta = ols_fit(Xt, ytr)
        pr = Xe @ beta
        preds[a] = pr
        out["R2"][a] = round(r2_of(yte, pr), 4)
        sl, ic = cal_slope(yte, pr)
        out["slope"][a] = round(sl, 4)
        out["icept"][a] = round(ic, 6)
        out["coef"][a] = [round(float(x), 6) for x in beta]
    out["incr"] = {}
    if set(PRIMARY_ARMS) <= set(arms):
        for nm, hi, lo in INCR:
            out["incr"][nm] = round(out["R2"][hi] - out["R2"][lo], 4)
    # binomial sampling floor context (240 draws/N)
    floor_var = float(np.mean(yte * (1 - yte)) / W)
    out["floor"] = {"binom_floor_var": round(floor_var, 8),
                    "total_var_test": round(float(np.var(yte)), 8),
                    "max_attainable_R2": round(
                        1.0 - floor_var / max(float(np.var(yte)), 1e-12), 4)}
    return out, preds

POINT = {}
PREDP = {}
for bl in (48, 52):
    POINT[f"b{bl}"], PREDP[f"b{bl}"] = eval_transfer(TR44, TE[bl])
    checkpoint(); ledger("point_transfer", target=bl, res=POINT[f"b{bl}"])
    log("transfer 44->%d: Mfull R2=%.4f slope=%.4f dR2_pp=%+.4f (maxAtt=%.3f)"
        % (bl, POINT[f"b{bl}"]["R2"]["Mfull"], POINT[f"b{bl}"]["slope"]["Mfull"],
           POINT[f"b{bl}"]["incr"]["dR2_pp"],
           POINT[f"b{bl}"]["floor"]["max_attainable_R2"]))
OUT["point_transfer"] = POINT

# per-seed descriptive transfers
PERSEED = {}
for seed in POP_SEEDS:
    tr = {f: POPS[(seed, 44)][f] for f in FIELDS}
    PERSEED[str(seed)] = {}
    for bl in (48, 52):
        te = {f: POPS[(seed, bl)][f] for f in FIELDS}
        e, _ = eval_transfer(tr, te, arms=["Mfull"])
        PERSEED[str(seed)][f"b{bl}"] = {"R2_Mfull": e["R2"]["Mfull"],
                                        "slope_Mfull": e["slope"]["Mfull"]}
OUT["per_seed_descriptive"] = PERSEED
checkpoint(); ledger("per_seed_transfers", res=PERSEED)

# ------------------------------------------------------------- bootstrap CIs
log("stage: bootstrap %d resamples" % NBOOT)
boot_idx_tr = rng_an.integers(0, len(TR44["rate"]), size=(NBOOT, len(TR44["rate"])))
BOOT = {}
for bl in (48, 52):
    n_te = len(TE[bl]["rate"])
    boot_idx_te = rng_an.integers(0, n_te, size=(NBOOT, n_te))
    ytr_all, yte_all = TR44["rate"], TE[bl]["rate"]
    br2 = {a: np.empty(NBOOT) for a in PRIMARY_ARMS + ["Mfam"]}
    bsl = {a: np.empty(NBOOT) for a in PRIMARY_ARMS + ["Mfam"]}
    binc = {nm: np.empty(NBOOT) for nm, _, _ in INCR}
    for bi in range(NBOOT):
        itr, ite = boot_idx_tr[bi], boot_idx_te[bi]
        ytr_b, yte_b = ytr_all[itr], yte_all[ite]
        ss_te = ((yte_b - yte_b.mean()) ** 2).sum()
        r2s = {}
        for a in PRIMARY_ARMS + ["Mfam"]:
            beta = ols_fit(design(TR44, a)[itr], ytr_b)
            pr = design(TE[bl], a)[ite] @ beta
            r2s[a] = 1.0 - ((yte_b - pr) ** 2).sum() / ss_te
            br2[a][bi] = r2s[a]
            sl, _ = cal_slope(yte_b, pr)
            bsl[a][bi] = sl
        for nm, hi, lo in INCR:
            binc[nm][bi] = r2s[hi] - r2s[lo]
    def ci(arr):
        lo_, hi_ = np.percentile(arr, [2.5, 97.5])
        return [round(float(lo_), 4), round(float(hi_), 4)]
    cell = {"R2_CI": {a: ci(br2[a]) for a in PRIMARY_ARMS + ["Mfam"]},
            "slope_CI": {a: ci(bsl[a]) for a in PRIMARY_ARMS + ["Mfam"]},
            "incr_CI": {nm: dict(point=POINT[f"b{bl}"]["incr"][nm], CI95=ci(binc[nm]),
                                 ci_excludes_0=bool(ci(binc[nm])[0] > 0 or ci(binc[nm])[1] < 0))
                        for nm, _, _ in INCR}}
    BOOT[f"b{bl}"] = cell
    checkpoint(); ledger("bootstrap_done", target=bl, incr_CI=cell["incr_CI"],
                         slope_CI_Mfull=cell["slope_CI"]["Mfull"])
OUT["bootstrap"] = BOOT

# ------------------------------------------------------------- verdicts
r2_52 = POINT["b52"]["R2"]["Mfull"]
r2_48 = POINT["b48"]["R2"]["Mfull"]
sl_52 = POINT["b52"]["slope"]["Mfull"]
sl_48 = POINT["b48"]["slope"]["Mfull"]
dpp_52 = POINT["b52"]["incr"]["dR2_pp"]

H1 = bool(r2_52 >= 0.45)
H2 = bool(0.8 <= sl_52 <= 1.25)
H3 = bool(dpp_52 >= 0.02)

if H1 and H2 and H3:
    NAME = "PERNDIAL-52-FULLY-VALIDATED"
elif H1 and H2:
    NAME = "PERNDIAL-52-VALIDATED-PP-ABSENT"
elif H1:
    NAME = "PERNDIAL-52-MISCALIBRATED-TRANSFER"
elif r2_52 >= 0.25:
    NAME = "PERNDIAL-52-PARTIAL-TRANSFER"
else:
    NAME = "PERNDIAL-52-ABSENT"

OUT["verdict"] = {
    "verdict_name": NAME,
    "H1": {"pass": H1, "R2_Mfull_b52": r2_52, "threshold": 0.45,
           "R2_Mfull_b48_descriptive": r2_48},
    "H2": {"pass": H2, "slope_b52": sl_52, "band": [0.8, 1.25],
           "slope_b48_descriptive": sl_48},
    "H3": {"pass": H3, "dR2_pp_b52_point": dpp_52, "threshold": 0.02,
           "dR2_pp_b52_CI95": BOOT["b52"]["incr_CI"]["dR2_pp"]["CI95"]},
    "barrier_lines": {
        "barrier_5": "Structural orthogonality: w/d/pp_sum are N-only natural "
                     "coordinates; the dial predicts relation yield (difficulty), "
                     "not (p,q) - no which-factor claim made or tested.",
        "barrier_8": "Known-method-in-disguise: the measured object is the QS/CFRAC "
                     "relation-yield dial - a cost predictor FOR known methods, not "
                     "a new factoring route."},
    "artifacts": [f"{WORK}/exp541_perndial_48_52.py", f"{WORK}/result.json",
                  f"{WORK}/ledger_exp541.jsonl"]
                 + [f"{WORK}/arrays_s{s}.npz" for s in POP_SEEDS]}
checkpoint()
ledger("DONE", status="DONE", verdict_name=NAME, verdict=OUT["verdict"],
       barriers=["5", "8"])

print("\n=== EXP 541 PERNDIAL-48-52 ===")
print("%-8s %-6s %-7s %-7s %-7s %-7s %-8s %-8s %-8s"
      % ("target", "arm", "R2", "slope", "+w", "+d", "+pp", "maxR2", ""))
for bl in (48, 52):
    p = POINT[f"b{bl}"]
    print("b%-7d %-6s %-7.4f %-7.4f %+8.4f %+8.4f %+8.4f %-8.3f"
          % (bl, "Mfull", p["R2"]["Mfull"], p["slope"]["Mfull"],
             p["incr"]["dR2_w"], p["incr"]["dR2_d"], p["incr"]["dR2_pp"],
             p["floor"]["max_attainable_R2"]))
print("BOOT CI b52: R2_Mfull %s | slope_Mfull %s | dR2_pp %s"
      % (BOOT["b52"]["R2_CI"]["Mfull"], BOOT["b52"]["slope_CI"]["Mfull"],
         BOOT["b52"]["incr_CI"]["dR2_pp"]))
print("VERDICT:", NAME)
print("H1 (R2>=0.45 @52): %.4f -> %s" % (r2_52, H1))
print("H2 (slope in [0.8,1.25]): %.4f -> %s (b48 %.4f)" % (sl_52, H2, sl_48))
print("H3 (dR2_pp>=+0.02 @52): %+.4f CI %s -> %s"
      % (dpp_52, BOOT["b52"]["incr_CI"]["dR2_pp"]["CI95"], H3))
print("DONE %.1fs" % (time.time() - T0))

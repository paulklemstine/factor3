#!/usr/bin/env python3
"""EXP 515 EXTENDED-DIAL (round-51). Base seed 20261060. Work dir /tmp/exp51_ext/.
Validation of the FULL augmented per-N relation-yield dial (papers 145/147/152/
163/172 line: footprint w, divisibility d, QR-count qrc, prime-power hits pp_sum)
across FRESH seeds, a SCALE transfer (bitlen 44 -> 48), and TWO u-targets.

CONSTRUCTIONS VERBATIM from exp482/exp497/exp505/exp506 (the clean-protocol
family):
bitlen-b balanced window [isqrt(2^(2b-1))+1, isqrt(2^(2b)-1)) with exact-bitlen
enforcement, inter-prime gap U[1,1e5); sq = isqrt(N);
V = j*(2*sq+j) + (sq*sq - N)  (Fermat offsets), j=1..240;
vmed POOLED PER POPULATION; B(u) = max(int(round(exp(ln(vmed)/u))), 50);
strip ONCE to BMAX = max over u; smooth@u iff rem==1 AND lpf <= B(u);
rate(N,u) = fraction of the 240 offsets smooth.
w/T dial = sum(2/q | odd q<=400, (N|q)=+1 via Euler criterion); qrc(<=100).
d = fraction of the 240 values divisible by >=1 prime in {2,3,5,7,11,13}.
pp_sum = sum over ODD p<=13 {3,5,7,11,13} of fraction of values with p^2 | v
  (brief wording "count of values divisible by p^2 for odd p<=13", exp506 sum-
  of-fractions convention, restricted to odd p per this brief; the p=2-inclusive
  variant pp_sum2 is carried as a descriptive sensitivity arm).

ARMS (incremental nesting, pre-stated):
  A0 base   = [1, qrc]
  A1 +w     = [1, qrc, w]
  A2 +d     = [1, qrc, w, d]
  A3 +pp    = [1, qrc, w, d, pp_sum]   (the FULL paper-145+172 dial)
Increments reported: dR2_w = A1-A0, dR2_d = A2-A1, dR2_pp = A3-A2,
each with paired bootstrap CI.

PRE-STATED HYPOTHESES (written BEFORE any data collection):
  H1: the full augmented dial A3 achieves out-of-sample R^2 >= 0.55 at u=3.5
      on >= 4/5 fresh populations at bitlen 44.
  H2: the dial transfers to bitlen 48: fit A3 on the POOLED five 44-bit
      populations, predict all 6000 48-bit Ns at u=3.5; calibration slope =
      OLS slope of observed rate on predicted rate (with intercept); PASS iff
      pooled slope in [0.8, 1.25]. Per-population slopes and the u=2.5 pooled
      slope are descriptive.
  H3: the prime-power term's contribution GROWS as u tightens:
      dR2_pp(u=3.5) > dR2_pp(u=2.5) on >= 4/5 populations (point estimates).

DECISION RULES (pre-stated):
  Band rule: threshold hypotheses scored on POINT estimates per the brief
  wording; bootstrap CIs reported alongside (PASS-with-CI when CI_low > 0).
  Verdict names:
    H1 & H2 & H3                -> EXTENDED-DIAL-FULLY-VALIDATED
    H1 & H2 & ~H3               -> EXTENDED-DIAL-VALIDATED-PP-U-FLAT
    H1 & ~H2                    -> EXTENDED-DIAL-IN-SAMPLE-ONLY
    ~H1 with >= 2/5 pops >=0.55 -> EXTENDED-DIAL-PARTIAL-REPLICATION
    else                        -> EXTENDED-DIAL-ABSENT

PROTOCOL (exp505/exp506 verbatim): OLS train/test 900/300 (seeded permutation
per population, separate analysis stream BASE+5+k); bootstrap 300 resamples of
ALL 1200 rows with replacement (first 900 train / last 300 test, ALL FOUR ARMS
REFIT per resample); boot indices drawn ONCE per population and shared across
all arms and both u cells (paired comparisons); percentile CIs on dR2.

# BARRIERS (standard lines, verbatim exp500/exp501/exp503/exp505/exp506):
#   Barrier 5 (structural orthogonality): T/w and all features here are N-only
#   natural coordinates; the dial predicts relation yield (difficulty), not
#   (p,q) - no which-factor claim made or tested.
#   Barrier 8 (known-method-in-disguise): the measured object is the QS/CFRAC
#   relation-yield dial - a cost predictor FOR known methods, not a new factoring route.
"""
import json, time, math, datetime, os, sys
import numpy as np
import gmpy2
from sympy import primerange, nextprime

BASE_SEED = 20260940 * 0 + 20261060      # populations 20261060..20261064
ANALYSIS_SEED = 20261065                 # separate stream: split + bootstrap
NN, W = 1200, 240
US = (3.5, 2.5)
D_PRIMES = [2, 3, 5, 7, 11, 13]          # any-hit set for d (verbatim exp506)
PP_ODD = [3, 5, 7, 11, 13]               # odd primes for pp_sum (this brief)
NTRAIN, NTEST = 900, 300
NBOOT = 300
T0 = time.time()
WORK = "/tmp/exp51_ext"

OUT = {"meta": {
    "exp": 515, "codename": "EXTENDED-DIAL", "round": 51,
    "population_seeds": [BASE_SEED + k for k in range(5)],
    "analysis_seed_root": ANALYSIS_SEED,
    "Ns_per_population": NN, "values_window": W, "us": list(US),
    "bitlens": {"fit": 44, "transfer": 48},
    "d_primes": D_PRIMES, "pp_odd_primes": PP_ODD,
    "nboot": NBOOT, "split": f"{NTRAIN}/{NTEST}",
    "arms": {"A0_base": "[1, qrc]", "A1_w": "[1, qrc, w]",
             "A2_d": "[1, qrc, w, d]", "A3_pp": "[1, qrc, w, d, pp_sum]",
             "A3b_pp2(descriptive)": "A3 but pp includes p=2"},
    "constructions": "verbatim exp497/505/506 balanced-window family; Fermat "
                     "offsets j=1..240; vmed pooled per population per bitlen",
    "prestated": {
        "H1": "full dial A3 OOS R^2 >= 0.55 at u=3.5 on >= 4/5 fresh pops (b=44)",
        "H2": "transfer 44->48: calibration slope (obs~pred, intercept) of pooled "
              "A3 fit on all 6000 b=48 Ns in [0.8, 1.25] at u=3.5",
        "H3": "dR2_pp(u3.5) > dR2_pp(u2.5) on >= 4/5 populations",
        "bands": "thresholds on point estimates; CIs reported (PASS-with-CI if "
                 "CI_low > 0)",
        "names": ["EXTENDED-DIAL-FULLY-VALIDATED", "EXTENDED-DIAL-VALIDATED-PP-U-FLAT",
                  "EXTENDED-DIAL-IN-SAMPLE-ONLY", "EXTENDED-DIAL-PARTIAL-REPLICATION",
                  "EXTENDED-DIAL-ABSENT"]}}}

def ledger(event, **kw):
    rec = {"ts": datetime.datetime.now().isoformat(timespec="seconds"),
           "exp": 515, "codename": "EXTENDED-DIAL", "event": event,
           "t_s": round(time.time() - T0, 1)}
    rec.update(kw)
    with open(f"{WORK}/ledger_exp515.jsonl", "a") as f:
        f.write(json.dumps(rec, default=float) + "\n")

def checkpoint():
    OUT["saved_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    OUT["elapsed_s"] = round(time.time() - T0, 1)
    json.dump(OUT, open(f"{WORK}/result.json", "w"), indent=1, default=float)

def log(msg):
    print("[%7.1fs] %s" % (time.time() - T0, msg), flush=True)

os.makedirs(WORK, exist_ok=True)

# ------------------------------------------------------------- stage 0: start
ledger("start", base_seed=BASE_SEED, workdir=WORK, nn=NN, window=W,
       us=list(US), prestated=OUT["meta"]["prestated"], barriers=["5", "8"],
       python=sys.version.split()[0], numpy=np.__version__, gmpy2=gmpy2.version())
checkpoint()
log("stage 0: ledger written (hypotheses pre-stated before data)")

primes_all = np.array(list(primerange(2, 40000)), dtype=np.int64)

def spearman(a, b):
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])

WINDOWS = {44: (int(gmpy2.isqrt(1 << 43)) + 1, int(gmpy2.isqrt((1 << 44) - 1))),
           48: (int(gmpy2.isqrt(1 << 47)) + 1, int(gmpy2.isqrt((1 << 48) - 1)))}
BITLO = {44: 1 << 43, 48: 1 << 47}
BITHI = {44: 1 << 44, 48: 1 << 48}

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
    """rate@(u) for both u, plus d13 and pp features from the SAME window."""
    vmed = float(np.median(V.astype(float)))
    B = {u: max(int(round(math.exp(math.log(vmed) / u))), 50) for u in US}
    BMAX = max(B.values())
    Q = V.copy()
    lpf = np.zeros(V.shape, dtype=np.int64)
    strip_primes = primes_all[primes_all <= BMAX]
    for p in strip_primes:
        while True:
            m = Q % p == 0
            if not m.any():
                break
            Q[m] //= p
            lpf[m] = p
    rate = {u: ((Q == 1) & (lpf <= B[u])).mean(axis=1) for u in US}
    div_or = np.zeros(V.shape, dtype=bool)
    pp_masks_odd = [(V % (p * p) == 0) for p in PP_ODD]
    for p in D_PRIMES:
        div_or |= (V % p == 0)
    pp_odd_sum = np.sum([pm.mean(axis=1) for pm in pp_masks_odd], axis=0)
    pp_with2 = pp_odd_sum + (V % 4 == 0).mean(axis=1)
    return {"rate": rate, "d13": div_or.mean(axis=1).astype(float),
            "pp_sum": pp_odd_sum.astype(float), "pp_sum2": pp_with2.astype(float),
            "vmed": vmed, "B": B, "BMAX": int(BMAX),
            "n_strip_primes": int(len(strip_primes))}

def build_population(seed, bl):
    rng_pop = np.random.default_rng(seed)
    pairs = [draw_one(rng_pop, bl) for _ in range(NN)]
    Ns_list = [d[0] for d in pairs]; sqs = [d[1] for d in pairs]
    assert len(set(Ns_list)) == NN, "Ns must be unique"
    tw, qrc = t_dial_and_qrc(Ns_list)
    V = fermat_offsets(Ns_list, sqs)
    tgt = targets_and_value_features(V)
    return {"Ns": np.array(Ns_list, dtype=np.int64), "tw": tw, "qrc": qrc, **tgt}

def ols_fit(Xtr, ytr):
    coef, *_ = np.linalg.lstsq(Xtr, ytr, rcond=None)
    return coef

def r2_of(yt, yp):
    resid = yt - yp
    return 1.0 - (resid @ resid) / (((yt - yt.mean()) ** 2).sum())

def design(tw, qrc, d13, pp, which):
    ones = np.ones(len(tw))
    if which == "A0":
        return np.column_stack([ones, qrc])
    if which == "A1":
        return np.column_stack([ones, qrc, tw])
    if which == "A2":
        return np.column_stack([ones, qrc, tw, d13])
    if which == "A3":
        return np.column_stack([ones, qrc, tw, d13, pp])
    raise ValueError(which)

ARMS = ["A0", "A1", "A2", "A3"]
INCR = [("dR2_w", "A1", "A0"), ("dR2_d", "A2", "A1"), ("dR2_pp", "A3", "A2")]

def fits_and_bootstrap(pop, K):
    """Per-u: point R2 per arm, increment dR2 with paired bootstrap CI."""
    rng_an = np.random.default_rng(ANALYSIS_SEED + K)
    perm = rng_an.permutation(NN)
    TR, TE = perm[:NTRAIN], perm[NTRAIN:]
    boot_idx = rng_an.integers(0, NN, size=(NBOOT, NN))
    res = {}
    for u in US:
        y = pop["rate"][u]
        Xs = {a: design(pop["tw"], pop["qrc"], pop["d13"], pop["pp_sum"], a)
              for a in ARMS}
        r2_te, preds = {}, {}
        for a in ARMS:
            bt = ols_fit(Xs[a][TR], y[TR])
            preds[a] = Xs[a][TE] @ bt
            r2_te[a] = r2_of(y[TE], preds[a])
        boot_r2 = {a: np.empty(NBOOT) for a in ARMS}
        for b in range(NBOOT):
            idx = boot_idx[b]
            tr_b, te_b = idx[:NTRAIN], idx[NTRAIN:]
            yte = y[te_b]
            ss_te = ((yte - yte.mean()) ** 2).sum()
            for a in ARMS:
                coef = ols_fit(Xs[a][tr_b], y[tr_b])
                pr = Xs[a][te_b] @ coef
                boot_r2[a][b] = 1.0 - ((yte - pr) ** 2).sum() / ss_te
        cell = {"R2": {a: round(r2_te[a], 4) for a in ARMS}}
        for nm, hi_a, lo_a in INCR:
            d_pt = r2_te[hi_a] - r2_te[lo_a]
            db = boot_r2[hi_a] - boot_r2[lo_a]
            lo, hi = (float(np.percentile(db, 2.5)), float(np.percentile(db, 97.5)))
            cell[nm] = {"point": round(d_pt, 4), "CI95": [round(lo, 4), round(hi, 4)],
                        "ci_excludes_0": bool(lo > 0 or hi < 0)}
        # descriptive sensitivity: pp including p=2 (point only, no bootstrap)
        X3b = np.column_stack([design(pop["tw"], pop["qrc"], pop["d13"],
                                      pop["pp_sum"], "A3")[:, :4],
                               pop["pp_sum2"]])
        r2b = r2_of(y[TE], X3b[TE] @ ols_fit(X3b[TR], y[TR]))
        cell["R2_A3b_pp_incl2"] = round(r2b, 4)
        res[f"u{u}"] = cell
    return res

# ============================================================ main loop
ROWS44 = []          # per-population feature/target rows at bitlen 44
P48 = {}             # per-seed stored 48-bit populations for transfer
FIT_TABLE = []       # flat fit rows for the report

for K in range(5):
    seed = BASE_SEED + K
    tag = f"pop{seed}"
    log(f"===== population {K+1}/5 seed={seed} =====")

    # ---- stage 1: bitlen-44 population + features + targets
    t1 = time.time()
    pop44 = build_population(seed, 44)
    st1 = {"bitlen_min": int(pop44["Ns"].min()).bit_length(),
           "bitlen_max": int(pop44["Ns"].max()).bit_length(),
           "vmed": round(pop44["vmed"], 1), "B": pop44["B"],
           "BMAX": pop44["BMAX"],
           "mean_rate": {f"u{u}": round(float(pop44['rate'][u].mean()), 6) for u in US},
           "wall_s": round(time.time() - t1, 1)}
    OUT.setdefault("populations", {})[tag] = {"seed": seed, **st1}
    checkpoint(); ledger("pop44_done", pop=tag, **st1)
    log("stage 1: b44 population+targets %s" % st1)

    # ---- stage 2: fits + bootstrap at bitlen 44
    t2 = time.time()
    fitres = fits_and_bootstrap(pop44, K)
    OUT["populations"][tag]["fits_b44"] = fitres
    sp35 = spearman(pop44["tw"], pop44["rate"][3.5])
    sp25 = spearman(pop44["tw"], pop44["rate"][2.5])
    OUT["populations"][tag]["anchors"] = {
        "sp_w_rate35": round(sp35, 4), "sp_w_rate25": round(sp25, 4)}
    for u in US:
        c = fitres[f"u{u}"]
        FIT_TABLE.append({"seed": seed, "bl": 44, "u": u, **c["R2"],
                          **{nm: c[nm]["point"] for nm, _, _ in INCR}})
    checkpoint(); ledger("fits_done", pop=tag, cells=fitres,
                         anchors={"sp35": round(sp35, 4), "sp25": round(sp25, 4)},
                         wall_s=round(time.time() - t2, 1))
    log("stage 2: fits done; A3 R2 u3.5=%.4f u2.5=%.4f dR2_pp %+ .4f / %+.4f"
        % (fitres["u3.5"]["R2"]["A3"], fitres["u2.5"]["R2"]["A3"],
           fitres["u3.5"]["dR2_pp"]["point"], fitres["u2.5"]["dR2_pp"]["point"]))

    # ---- stage 3: bitlen-48 twin population (same seed)
    t3 = time.time()
    pop48 = build_population(seed, 48)
    P48[seed] = pop48
    ROWS44.append((pop44["tw"], pop44["qrc"], pop44["d13"], pop44["pp_sum"],
                   pop44["rate"]))
    st3 = {"vmed": round(pop48["vmed"], 1), "B": pop48["B"], "BMAX": pop48["BMAX"],
           "mean_rate": {f"u{u}": round(float(pop48['rate'][u].mean()), 6) for u in US},
           "wall_s": round(time.time() - t3, 1)}
    OUT["populations"][tag]["b48"] = st3
    checkpoint(); ledger("pop48_done", pop=tag, **st3)
    log("stage 3: b48 twin built %s" % st3)

    np.savez_compressed(
        f"{WORK}/arrays_{tag}.npz",
        **{"tw44": pop44["tw"], "qrc44": pop44["qrc"], "d44": pop44["d13"],
           "pp44": pop44["pp_sum"], "rate44_u3.5": pop44["rate"][3.5],
           "rate44_u2.5": pop44["rate"][2.5],
           "tw48": pop48["tw"], "qrc48": pop48["qrc"], "d48": pop48["d13"],
           "pp48": pop48["pp_sum"], "rate48_u3.5": pop48["rate"][3.5],
           "rate48_u2.5": pop48["rate"][2.5]})

# ------------------------------------------------------- stage 4: transfer 44->48
t4 = time.time()
TRANSFER = {}
for u in US:
    X44 = np.vstack([
        np.column_stack([np.ones(NN), r[1], r[0], r[2], r[3]]) for r in ROWS44])
    y44 = np.concatenate([r[4][u] for r in ROWS44])
    beta = ols_fit(X44, y44)
    X48 = np.vstack([
        np.column_stack([np.ones(NN), P48[s]["qrc"], P48[s]["tw"],
                         P48[s]["d13"], P48[s]["pp_sum"]]) for s in sorted(P48)])
    y48 = np.concatenate([P48[s]["rate"][u] for s in sorted(P48)])
    pred48 = X48 @ beta
    # calibration: OLS observed ~ predicted (with intercept)
    cal = np.linalg.lstsq(np.column_stack([np.ones(len(pred48)), pred48]), y48,
                          rcond=None)[0]
    tr_r2 = r2_of(y48, pred48)
    per_seed = []
    for i, s in enumerate(sorted(P48)):
        sl = slice(i * NN, (i + 1) * NN)
        cs = np.linalg.lstsq(np.column_stack([np.ones(NN), pred48[sl]]), y48[sl],
                             rcond=None)[0]
        per_seed.append({"seed": s, "slope": round(float(cs[1]), 4),
                         "intercept": round(float(cs[0]), 5)})
    TRANSFER[f"u{u}"] = {
        "coef_A3_fit_at_44": [round(float(x), 5) for x in beta],
        "calibration_slope_pooled": round(float(cal[1]), 4),
        "calibration_intercept_pooled": round(float(cal[0]), 5),
        "transfer_R2": round(tr_r2, 4),
        "mean_obs48": round(float(y48.mean()), 5),
        "mean_pred48": round(float(pred48.mean()), 5),
        "per_seed_slopes": per_seed}
OUT["transfer_44_to_48"] = TRANSFER
checkpoint(); ledger("transfer_done", transfer=TRANSFER, wall_s=round(time.time() - t4, 1))

# ------------------------------------------------------------- stage 5: verdicts
r2_a3_35 = [OUT["populations"][f"pop{BASE_SEED+k}"]["fits_b44"]["u3.5"]["R2"]["A3"]
            for k in range(5)]
dpp_35 = [OUT["populations"][f"pop{BASE_SEED+k}"]["fits_b44"]["u3.5"]["dR2_pp"]["point"]
          for k in range(5)]
dpp_25 = [OUT["populations"][f"pop{BASE_SEED+k}"]["fits_b44"]["u2.5"]["dR2_pp"]["point"]
          for k in range(5)]
h1_count = int(sum(1 for v in r2_a3_35 if v >= 0.55))
H1 = h1_count >= 4
slope35 = TRANSFER["u3.5"]["calibration_slope_pooled"]
H2 = bool(0.8 <= slope35 <= 1.25)
h3_count = int(sum(1 for a, b in zip(dpp_35, dpp_25) if a > b))
H3 = h3_count >= 4

if H1 and H2 and H3:
    NAME = "EXTENDED-DIAL-FULLY-VALIDATED"
elif H1 and H2:
    NAME = "EXTENDED-DIAL-VALIDATED-PP-U-FLAT"
elif H1:
    NAME = "EXTENDED-DIAL-IN-SAMPLE-ONLY"
elif h1_count >= 2:
    NAME = "EXTENDED-DIAL-PARTIAL-REPLICATION"
else:
    NAME = "EXTENDED-DIAL-ABSENT"

OUT["verdict"] = {
    "verdict_name": NAME,
    "H1": {"pass": H1, "count_ge_0.55": h1_count, "of": 5,
           "per_seed_R2_A3_u3.5": r2_a3_35,
           "mean": round(float(np.mean(r2_a3_35)), 4)},
    "H2": {"pass": H2, "slope_u3.5_pooled": slope35, "band": [0.8, 1.25],
           "slope_u2.5_pooled_descriptive": TRANSFER["u2.5"]["calibration_slope_pooled"],
           "transfer_R2_u3.5": TRANSFER["u3.5"]["transfer_R2"]},
    "H3": {"pass": H3, "count": h3_count, "of": 5,
           "dR2_pp_u3.5": dpp_35, "dR2_pp_u2.5": dpp_25},
    "barrier_lines": {
        "barrier_5": "Structural orthogonality: T/w and all features here are N-only "
                     "natural coordinates; the dial predicts relation yield (difficulty), "
                     "not (p,q) - no which-factor claim made or tested.",
        "barrier_8": "Known-method-in-disguise: the measured object is the QS/CFRAC "
                     "relation-yield dial - a cost predictor FOR known methods, not a "
                     "new factoring route."},
    "artifacts": [f"{WORK}/exp515_extended_dial.py", f"{WORK}/result.json",
                  f"{WORK}/ledger_exp515.jsonl"]
                 + [f"{WORK}/arrays_pop{BASE_SEED+k}.npz" for k in range(5)]}
checkpoint()
ledger("DONE", status="DONE", verdict_name=NAME, verdict=OUT["verdict"],
       barriers=["5", "8"])

print("\n=== EXP 515 EXTENDED-DIAL ===")
print("%-10s %-4s %-5s %-7s %-7s %-7s %-7s %-8s %-8s %-8s"
      % ("seed", "bl", "u", "R2_A0", "R2_A1", "R2_A2", "R2_A3", "+w", "+d", "+pp"))
for k in range(5):
    for u in US:
        f = OUT["populations"][f"pop{BASE_SEED+k}"]["fits_b44"][f"u{u}"]
        print("%-10d %-4d %-5.1f %-7.4f %-7.4f %-7.4f %-7.4f %+8.4f %+8.4f %+8.4f"
              % (BASE_SEED + k, 44, u, f["R2"]["A0"], f["R2"]["A1"], f["R2"]["A2"],
                 f["R2"]["A3"], f["dR2_w"]["point"], f["dR2_d"]["point"],
                 f["dR2_pp"]["point"]))
print("TRANSFER 44->48 u3.5: slope=%.4f intercept=%.5f transferR2=%.4f | u2.5 slope=%.4f"
      % (TRANSFER["u3.5"]["calibration_slope_pooled"],
         TRANSFER["u3.5"]["calibration_intercept_pooled"],
         TRANSFER["u3.5"]["transfer_R2"],
         TRANSFER["u2.5"]["calibration_slope_pooled"]))
print("VERDICT:", NAME)
print("H1 (A3 R2>=0.55 @u3.5 on >=4/5): %d/5 %s  vals=%s"
      % (h1_count, H1, [round(v, 4) for v in r2_a3_35]))
print("H2 (slope in [0.8,1.25]): %.4f -> %s" % (slope35, H2))
print("H3 (dR2_pp u3.5>u2.5 on >=4/5): %d/5 %s" % (h3_count, H3))
print("DONE %.1fs" % (time.time() - T0))

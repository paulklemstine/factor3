#!/usr/bin/env python3
"""EXP 506 PPOW-MULTISEED (round-46). Base seed 20260940. Work dir /tmp/exp46_pms/.
Replication test of paper 172 (+0.0892 out-of-sample R^2 at u=3.5 for the
prime-power hit block, single population seed 20260927) across FRESH populations,
plus two extensions the single-population result never tested: u-robustness and
window-length scaling.

CONSTRUCTIONS VERBATIM from exp482/exp497/exp505 (the clean-protocol family):
bitlen-44 balanced window [isqrt(2^43)+1, isqrt(2^44-1)) with exact-bitlen
enforcement, inter-prime gap U[1,1e5); sq = isqrt(N);
V = j*(2*sq+j) + (sq*sq - N)  (Fermat offsets), j=1..960 (240-slice = first window),
positivity asserted; vmed POOLED PER POPULATION (per window, see L2);
B(u,win) = max(int(round(exp(ln(vmed_win)/u))), 50); strip ONCE to
BMAX = max over u x win; smooth@(u,win) iff rem==1 AND maxp <= B(u,win);
rate(N,u,win) = fraction of that window's offsets smooth;
T(N) = w dial = sum(2/q | odd q<=400, (N|q)=+1 via Euler criterion); qrc(<=100).
Population: FIVE independent populations, 1200 Ns bitlen 44 each,
seeds 20260940..20260944 (fresh -- disjoint from paper 172's 20260927).

ARMS PER CELL (brief spec):
  base = [1, w(<=400 QR footprint), qrc(<=100), d(p<=13 any-hit)]
  aug  = base + pp_sum (sum over p<=13 of fraction of window values divisible by p^2)

PRE-STATED HYPOTHESES (written BEFORE any data collection):
  H1: the paper-172 lift replicates across the 5 fresh populations --
      per-seed dR2(aug-base) > 0.03 at (u=3.5, window 240) on >= 4/5 seeds.
  H2: the lift persists at u=2.5 as well as u=3.5 --
      dR2 bootstrap CI excludes 0 on >= 3/5 populations at BOTH u
      (scored at the paper-172 window 240; 960 reported descriptively).
  H3: the lift GROWS with window length (240 -> 960), consistent with better
      estimation of the squarefull structure --
      PRE-STATED RULE: PASS iff mean_over_seeds dR2(960) > mean dR2(240) at
      BOTH u; GROWTH-MIXED if strictly greater at exactly one u; ABSENT otherwise.

DECISION RULES (pre-stated):
  Band rule per threshold t: PASS = point >= t (and, where a CI is demanded,
  CI_low > 0); MARGINAL = point >= t but CI straddles 0; FAIL otherwise.
  H1 is scored on per-seed POINT estimates per the brief wording.
  Verdict names: H1 pass -> PPOW-LIFT-REPLICATES (-AND-GROWS / -GROWTH-MIXED /
      -GROWTH-ABSENT per H3); H1 fail with >=2/5 seeds above 0.03 ->
      PPOW-PARTIAL-REPLICATION; else PPOW-LIFT-ABSENT.

PROTOCOL: OLS train/test 900/300 (seeded permutation per population, separate
analysis stream 20260945+k); bootstrap 300 resamples of ALL 1200 rows with
replacement (first 900 train / last 300 test, BOTH ARMS REFIT per resample,
exp505 protocol); boot indices drawn ONCE per population and shared across all
four cells (paired comparisons); percentile CIs on dR2.

# BARRIERS (standard lines, verbatim exp500/exp501/exp503/exp505):
#   Barrier 5 (structural orthogonality): T/w and all features here are N-only
#   natural coordinates; the dial predicts relation yield (difficulty), not
#   (p,q) - no which-factor claim made or tested.
#   Barrier 8 (known-method-in-disguise): the measured object is the QS/CFRAC
#   relation-yield dial - a cost predictor FOR known methods, not a new factoring route.
"""
import json, time, math, datetime, os, sys, traceback
import numpy as np
import gmpy2
from sympy import primerange, nextprime

BASE_SEED = 20260940          # populations 20260940..20260944
ANALYSIS_SEED = 20260945      # separate stream: split + bootstrap (exp505 convention)
NN, W_FULL, W_SHORT = 1200, 960, 240
US = (3.5, 2.5)
D_PRIMES = [2, 3, 5, 7, 11, 13]
NTRAIN, NTEST = 900, 300
NBOOT = 300
T0 = time.time()
WORK = "/tmp/exp46_pms"

OUT = {"meta": {
    "exp": 506, "codename": "PPOW-MULTISEED", "round": 46,
    "population_seeds": [BASE_SEED + k for k in range(5)],
    "analysis_seed_root": ANALYSIS_SEED,
    "Ns_per_population": NN, "values_full_window": W_FULL,
    "values_short_window": W_SHORT, "us": list(US),
    "d_primes": D_PRIMES, "nboot": NBOOT, "split": f"{NTRAIN}/{NTEST}",
    "arms": {"base": "[1, w(<=400 QR), qrc(<=100), d(any-hit p<=13)]",
             "aug": "base + pp_sum"},
    "constructions": "verbatim exp497/505 bitlen-44 balanced window arm, "
                     "Fermat offsets j=1..960, vmed pooled per population "
                     "PER WINDOW (see ledger L2)",
    "prestated": {
        "H1": "paper-172 lift replicates: per-seed dR2 > 0.03 at (u=3.5, w=240) "
              "on >= 4/5 fresh seeds",
        "H2": "lift persists at u=2.5 as well as 3.5: dR2 bootstrap CI excludes 0 "
              "on >= 3/5 populations at BOTH u (window 240)",
        "H3": "lift grows with window 240->960: PASS iff mean dR2(960) > mean "
              "dR2(240) at BOTH u; GROWTH-MIXED at exactly one; ABSENT otherwise",
        "bands": "PASS = point >= t and CI_low > 0 where CI demanded; "
                 "MARGINAL = point >= t, CI straddles 0"}}}

def ledger(event, **kw):
    rec = {"ts": datetime.datetime.now().isoformat(timespec="seconds"),
           "exp": 506, "codename": "PPOW-MULTISEED", "event": event,
           "t_s": round(time.time() - T0, 1)}
    rec.update(kw)
    with open(f"{WORK}/ledger_exp506.jsonl", "a") as f:
        f.write(json.dumps(rec, default=float) + "\n")

def checkpoint():
    OUT["saved_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    OUT["elapsed_s"] = round(time.time() - T0, 1)
    json.dump(OUT, open(f"{WORK}/result.json", "w"), indent=1, default=float)

def log(msg):
    print("[%7.1fs] %s" % (time.time() - T0, msg), flush=True)

os.makedirs(WORK, exist_ok=True)

# ------------------------------------------------------------- stage 0: start
ledger("start", base_seed=BASE_SEED, workdir=WORK, nn=NN,
       windows=[W_SHORT, W_FULL], us=list(US), prestated=OUT["meta"]["prestated"],
       barriers=["5", "8"], python=sys.version.split()[0],
       numpy=np.__version__, gmpy2=gmpy2.version())
checkpoint()
log("stage 0: ledger written (hypotheses pre-stated before data)")

primes_all = np.array(list(primerange(2, 20000)), dtype=np.int64)

def spearman(a, b):
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])

LO44 = int(gmpy2.isqrt(1 << 43)) + 1
HI44 = int(gmpy2.isqrt((1 << 44) - 1))

def draw_one(rng, lo, hi):
    # verbatim exp499/exp500/exp501/exp503/exp505 draw_balanced
    while True:
        r = int(rng.integers(lo, hi))
        p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, 10**5))))
        N = p * q
        if not ((1 << 43) <= N < (1 << 44)):
            continue
        return N, math.isqrt(N)

wr = list(primerange(3, 401))     # odd primes <= 400 (w dial + qrc source)
qrc_ps = [p for p in wr if p <= 100]

def t_dial_and_qrc(Ns_list):
    """w/T dial (odd p<=400) and qrc(<=100), Euler criterion -- exp505 verbatim."""
    tw = np.zeros(len(Ns_list)); qrc = np.zeros(len(Ns_list))
    wr_arr = np.array(wr)
    for N_i, N in enumerate(Ns_list):
        Nm = int(N)
        syms = [gmpy2.powmod(Nm % int(q), (int(q) - 1) // 2, int(q)) for q in wr_arr]
        qr400 = np.fromiter((s == 1 for s in syms), bool, len(wr_arr))
        tw[N_i] = (2.0 / wr_arr)[qr400].sum()
        qrc[N_i] = qr400[np.array(wr_arr) <= 100].sum()
    return tw, qrc

def fermat_offsets(Ns_list, sqs, Wmax):
    js = np.arange(1, Wmax + 1, dtype=np.int64)
    sq = np.asarray(sqs, dtype=np.int64)[:, None]
    N = np.asarray(Ns_list, dtype=np.int64)[:, None]
    V = js[None, :] * (2 * sq + js[None, :]) + (sq * sq - N)
    assert (V > 0).all(), "positivity violated"
    assert V.dtype == np.int64 and V.max() < 2**62
    return V

CELLS = [(u, w) for u in US for w in (W_SHORT, W_FULL)]

# ============================================================ per-population loop
FITROWS = []          # flat table rows
POP_SUMMARY = {}
for K in range(5):
    seed = BASE_SEED + K
    tag = f"pop{seed}"
    log(f"===== population {K+1}/5 seed={seed} =====")

    # ---------------------------------------------- stage 1: population
    t1 = time.time()
    rng_pop = np.random.default_rng(seed)
    pairs = [draw_one(rng_pop, LO44, HI44) for _ in range(NN)]
    Ns_list = [d[0] for d in pairs]; sqs = [d[1] for d in pairs]
    assert len(set(Ns_list)) == NN, "Ns must be unique"
    st1 = {"n_unique": len(set(Ns_list)),
           "bitlen_min": min(int(x).bit_length() for x in Ns_list),
           "bitlen_max": max(int(x).bit_length() for x in Ns_list),
           "wall_s": round(time.time() - t1, 1)}
    OUT.setdefault("populations", {})[tag] = {"seed": seed, **st1}
    checkpoint(); ledger("population_done", pop=tag, **st1)
    log("stage 1: population built %s" % st1)

    # ---------------------------------------------- stage 2: values + targets
    t2 = time.time()
    V = fermat_offsets(Ns_list, sqs, W_FULL)
    vmed_short = float(np.median(V[:, :W_SHORT].astype(float)))
    vmed_full = float(np.median(V.astype(float)))
    B = {(u, w): max(int(round(math.exp(math.log(vmed_short if w == W_SHORT
                                                    else vmed_full) / u))), 50)
         for (u, w) in CELLS}
    BMAX = max(B.values())                       # strip ONCE to max bound
    Q = V.copy()
    lpf = np.zeros(V.shape, dtype=np.int64)
    strip_primes = primes_all[primes_all <= BMAX]
    for p in strip_primes:
        while True:
            m = Q % p == 0
            if not m.any():
                break
            Q[m] //= p
            lpf[m] = p                            # multiplicity-aware largest-found
    rate = {}
    for (u, w) in CELLS:
        sl = slice(None, W_SHORT) if w == W_SHORT else slice(None, None)
        sm = (Q[:, sl] == 1) & (lpf[:, sl] <= B[(u, w)])
        rate[(u, w)] = sm.mean(axis=1)
    st2 = {"vmed_short": vmed_short, "vmed_full": vmed_full,
           "B": {f"u{u}_w{w}": B[(u, w)] for (u, w) in CELLS}, "BMAX": int(BMAX),
           "n_strip_primes": int(len(strip_primes)),
           "mean_rate": {f"u{u}_w{w}": round(float(rate[(u, w)].mean()), 6)
                         for (u, w) in CELLS},
           "wall_s": round(time.time() - t2, 1)}
    OUT["populations"][tag]["targets"] = st2
    checkpoint(); ledger("targets_done", pop=tag, **st2)
    log("stage 2: targets %s" % st2)

    # ---------------------------------------------- stage 3: features
    t3 = time.time()
    tw, qrc = t_dial_and_qrc(Ns_list)
    d13 = {}
    pp_sum = {}
    div_or = np.zeros(V.shape, dtype=bool)
    for p in D_PRIMES:
        div_or |= (V % p == 0)
    pp_masks = [(V % (p * p) == 0) for p in D_PRIMES]
    for wname, sl in (("w240", slice(None, W_SHORT)), ("w960", slice(None, None))):
        d13[wname] = div_or[:, sl].mean(axis=1)
        pp_sum[wname] = np.sum([pm[:, sl].mean(axis=1) for pm in pp_masks], axis=0)
    pp_any_short = np.logical_or.reduce([pm[:, :W_SHORT] for pm in pp_masks], axis=0)
    sp_T_35 = spearman(tw, rate[(3.5, W_SHORT)])
    sp_T_25 = spearman(tw, rate[(2.5, W_SHORT)])
    st3 = {
        "feature_conventions": {
            "w/T": "sum 2/p over odd QR primes p<=400 (Euler criterion)",
            "qrc": "count of odd QR primes p<=100",
            "d": "fraction of WINDOW values divisible by >=1 prime in {2,3,5,7,11,13}",
            "pp_sum": "sum over p<=13 of fraction of WINDOW values divisible by p^2"},
        "mean_d13": {k: round(float(v.mean()), 5) for k, v in d13.items()},
        "mean_pp_sum": {k: round(float(v.mean()), 5) for k, v in pp_sum.items()},
        "ppany_mean_w240": round(float(pp_any_short.mean()), 6),
        "corr_ppsum_rate35_240": round(float(np.corrcoef(pp_sum["w240"], rate[(3.5, W_SHORT)])[0, 1]), 4),
        "corr_ppsum_rate25_240": round(float(np.corrcoef(pp_sum["w240"], rate[(2.5, W_SHORT)])[0, 1]), 4),
        "anchor_sp_T_3.5_w240": round(sp_T_35, 4),
        "anchor_sp_T_2.5_w240": round(sp_T_25, 4),
        "wall_s": round(time.time() - t3, 1)}
    OUT["populations"][tag]["features"] = st3
    checkpoint(); ledger("features_done", pop=tag,
                         **{k: v for k, v in st3.items() if k != "feature_conventions"})
    log("stage 3: features done; sp(T;3.5)=%.4f sp(T;2.5)=%.4f corr(pp_sum,y35)=%.4f"
        % (sp_T_35, sp_T_25, st3["corr_ppsum_rate35_240"]))

    # ---------------------------------------------- stage 4: fits + bootstrap
    t4 = time.time()
    rng_an = np.random.default_rng(ANALYSIS_SEED + K)
    perm = rng_an.permutation(NN)
    TR, TE = perm[:NTRAIN], perm[NTRAIN:]
    boot_idx = rng_an.integers(0, NN, size=(NBOOT, NN))   # shared across cells
    ones_all = np.ones((NN, 1))

    def ols_fit(Xtr, ytr):
        coef, *_ = np.linalg.lstsq(Xtr, ytr, rcond=None)
        return coef

    def r2_of(yt, yp):
        resid = yt - yp
        return 1.0 - (resid @ resid) / (((yt - yt.mean()) ** 2).sum())

    cell_res = {}
    for (u, w) in CELLS:
        y = rate[(u, w)]
        wname = "w240" if w == W_SHORT else "w960"
        Xb = np.column_stack([ones_all, tw, qrc, d13[wname]])
        Xa = np.column_stack([ones_all, tw, qrc, d13[wname], pp_sum[wname]])
        MODELS = {"base": Xb, "aug": Xa}
        betas, r2_te, preds_te = {}, {}, {}
        for kname, X in MODELS.items():
            betas[kname] = ols_fit(X[TR], y[TR])
            preds_te[kname] = X[TE] @ betas[kname]
            r2_te[kname] = r2_of(y[TE], preds_te[kname])
        dR2_pt = r2_te["aug"] - r2_te["base"]
        db = np.empty(NBOOT)
        for b in range(NBOOT):
            idx = boot_idx[b]
            tr_b, te_b = idx[:NTRAIN], idx[NTRAIN:]
            yte = y[te_b]
            ss_te = ((yte - yte.mean()) ** 2).sum()
            r2b = {}
            for kname, X in MODELS.items():
                bt = ols_fit(X[tr_b], y[tr_b])
                pr = X[te_b] @ bt
                r2b[kname] = 1.0 - ((yte - pr) ** 2).sum() / ss_te
            db[b] = r2b["aug"] - r2b["base"]
        lo, hi = (float(np.percentile(db, 2.5)), float(np.percentile(db, 97.5)))
        excl0 = bool(lo > 0 or hi < 0)
        cell_res[f"u{u}_w{w}"] = {
            "R2_base": round(r2_te["base"], 4), "R2_aug": round(r2_te["aug"], 4),
            "dR2": round(dR2_pt, 4), "CI95": [round(lo, 4), round(hi, 4)],
            "ci_excludes_0": excl0}
        FITROWS.append({"seed": seed, "u": u, "win": w, **cell_res[f"u{u}_w{w}"]})
        log("cell u=%.1f w=%d: base=%.4f aug=%.4f dR2=%+.4f CI[%+.4f,%+.4f]%s"
            % (u, w, r2_te["base"], r2_te["aug"], dR2_pt, lo, hi,
               " *" if excl0 else ""))
    OUT["populations"][tag]["fits"] = cell_res
    OUT.setdefault("table", []).extend(FITROWS[-len(CELLS):])
    checkpoint(); ledger("fits_done", pop=tag, cells=cell_res,
                         wall_s=round(time.time() - t4, 1))

    np.savez_compressed(
        f"{WORK}/arrays_{tag}.npz",
        **{"Ns": np.array(Ns_list, dtype=np.int64), "tw": tw, "qrc": qrc,
           "d13_w240": d13["w240"], "d13_w960": d13["w960"],
           "pp_sum_w240": pp_sum["w240"], "pp_sum_w960": pp_sum["w960"],
           "rate_u3.5_w240": rate[(3.5, W_SHORT)],
           "rate_u3.5_w960": rate[(3.5, W_FULL)],
           "rate_u2.5_w240": rate[(2.5, W_SHORT)],
           "rate_u2.5_w960": rate[(2.5, W_FULL)]})

# ------------------------------------------------------------- stage 5: verdicts
by_cell = {(u, w): [r["dR2"] for r in OUT["table"]
                    if r["u"] == u and r["win"] == w] for (u, w) in CELLS}
by_ci = {(u, w): [r["ci_excludes_0"] for r in OUT["table"]
                  if r["u"] == u and r["win"] == w] for (u, w) in CELLS}

h1_vals = by_cell[(3.5, W_SHORT)]
h1_count = int(sum(1 for v in h1_vals if v > 0.03))
H1 = bool(h1_count >= 4)
h1_mean = float(np.mean(h1_vals))

h2_cnt_35 = int(sum(by_ci[(3.5, W_SHORT)]))
h2_cnt_25 = int(sum(by_ci[(2.5, W_SHORT)]))
H2 = bool(h2_cnt_35 >= 3 and h2_cnt_25 >= 3)

m35_s, m35_f = float(np.mean(by_cell[(3.5, W_SHORT)])), float(np.mean(by_cell[(3.5, W_FULL)]))
m25_s, m25_f = float(np.mean(by_cell[(2.5, W_SHORT)])), float(np.mean(by_cell[(2.5, W_FULL)]))
grow35 = m35_f > m35_s
grow25 = m25_f > m25_s
if grow35 and grow25:
    H3 = "PASS"
elif grow35 or grow25:
    H3 = "GROWTH-MIXED"
else:
    H3 = "ABSENT"

# cross-seed SE of the headline dR2 (descriptive)
sd_h1 = float(np.std(h1_vals, ddof=1)) if len(h1_vals) > 1 else float("nan")
se_h1 = sd_h1 / math.sqrt(len(h1_vals))

if H1 and H3 == "PASS":
    NAME = "PPOW-LIFT-REPLICATES-AND-GROWS"
elif H1 and H3 == "GROWTH-MIXED":
    NAME = "PPOW-LIFT-REPLICATES-GROWTH-MIXED"
elif H1:
    NAME = "PPOW-LIFT-REPLICATES-GROWTH-ABSENT"
elif h1_count >= 2:
    NAME = "PPOW-PARTIAL-REPLICATION"
else:
    NAME = "PPOW-LIFT-ABSENT"

OUT["verdict"] = {
    "verdict_name": NAME,
    "H1": {"pass": H1, "count_gt_0.03": h1_count, "of": 5, "threshold": "point dR2 > 0.03 on >= 4/5",
           "per_seed_dR2_u3.5_w240": h1_vals, "mean": round(h1_mean, 4),
           "cross_seed_sd": round(sd_h1, 4), "SE_mean": round(se_h1, 4)},
    "H2": {"pass": H2, "ci_excl0_counts_w240": {"u3.5": h2_cnt_35, "u2.5": h2_cnt_25},
           "required": ">=3/5 at BOTH u"},
    "H3": {"result": H3, "mean_dR2": {"u3.5_w240": round(m35_s, 4), "u3.5_w960": round(m35_f, 4),
                                      "u2.5_w240": round(m25_s, 4), "u2.5_w960": round(m25_f, 4)}},
    "barrier_lines": {
        "barrier_5": "Structural orthogonality: T/w and all features here are N-only "
                     "natural coordinates; the dial predicts relation yield (difficulty), "
                     "not (p,q) - no which-factor claim made or tested.",
        "barrier_8": "Known-method-in-disguise: the measured object is the QS/CFRAC "
                     "relation-yield dial - a cost predictor FOR known methods, not a "
                     "new factoring route."},
    "artifacts": [f"{WORK}/exp506_ppow_multiseed.py", f"{WORK}/result.json",
                  f"{WORK}/ledger_exp506.jsonl"] + [f"{WORK}/arrays_pop{BASE_SEED+k}.npz" for k in range(5)]}
OUT.pop("table", None)          # table already stored per population under fits
checkpoint()
ledger("DONE", status="DONE", verdict_name=NAME, verdict=OUT["verdict"],
       barriers=["5", "8"], artifacts=OUT["verdict"]["artifacts"])

print("\n=== EXP 506 PPOW-MULTISEED ===")
print("%-10s %-6s %-5s %-9s %-9s %-9s %-20s %s"
      % ("seed", "u", "win", "R2_base", "R2_aug", "dR2", "bootstrap CI95", "excl0"))
for r in sorted(FITROWS, key=lambda r: (r["seed"], -r["u"], r["win"])):
    print("%-10d %-6.1f %-5d %-9.4f %-9.4f %+9.4f [%+.4f,%+.4f]    %s"
          % (r["seed"], r["u"], r["win"], r["R2_base"], r["R2_aug"], r["dR2"],
             r["CI95"][0], r["CI95"][1], r["ci_excludes_0"]))
print("VERDICT:", NAME)
print("H1 (>=4/5 seeds dR2>0.03 @ u3.5 w240): count=%d/5 mean=%+.4f (SE %.4f) -> %s"
      % (h1_count, h1_mean, se_h1, H1))
print("H2 (CI excl 0 >=3/5 at BOTH u, w240): u3.5=%d/5 u2.5=%d/5 -> %s"
      % (h2_cnt_35, h2_cnt_25, H2))
print("H3 (growth 240->960): mean dR2 u3.5 %.4f->%.4f | u2.5 %.4f->%.4f -> %s"
      % (m35_s, m35_f, m25_s, m25_f, H3))
print("DONE %.1fs" % (time.time() - T0))

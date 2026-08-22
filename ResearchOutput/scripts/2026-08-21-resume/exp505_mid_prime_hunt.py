#!/usr/bin/env python3
"""EXP 505 MID-PRIME-HUNT (round-46). Seed 20260926+1 = 20260927. Work dir /tmp/exp46_mid/.
Papers 167-170: the zero-fit yield dial T(N)=sum(2/p | QR p<=400) is seed-stable and
draw-regime-invariant, but the ~0.064 Spearman drop at u=3.5 is NOT recoverable by
reweighting SMALL-prime features (p <= 29; paper 170). Paper 170's redirect: the lost
content sits in MID PRIMES (31-356) and/or non-footprint structure. This experiment
hunts it there directly.

CONSTRUCTIONS VERBATIM from exp497/exp499/exp500/exp501/exp503 (the exp482 clean
protocol family): bitlen-44 balanced window [isqrt(2^43)+1, isqrt(2^44-1)) with
exact-bitlen enforcement, inter-prime gap U[1,1e5); sq = isqrt(N);
V = j*(2*sq+j) + (sq*sq - N)  (Fermat offsets), j=1..240; positivity asserted;
vmed POOLED PER POPULATION; B(u) = max(int(round(exp(ln(vmed)/u))), 50); strip ONCE to
max B over {3.5, 2.5}; smooth@u iff rem==1 AND maxp <= B(u); rate(N,u) = fraction of
the 240 offsets smooth at u; T(N) = sum(2/q | odd q<=400, (N|q)=+1 via Euler criterion).
Population: ONE population, 1200 Ns bitlen 44, seed 20260927.

FEATURES:
  (a) paper-145 baseline: w(<=400) [= T dial], qrc(<=100), d(<=13 = fraction of values
      divisible by >=1 prime in {2,3,5,7,11,13})  [exp478 augmented-dial conventions]
  (b) small hit fractions n_p for odd primes 3..29 (9 features)
  (c) mid hit fractions n_p for primes 31..97 (15 features -- NOTE: brief said "11";
      the prime count in [31,97] is 15; all are used, disclosed in ledger/caveats)
  (d) mid-QR density rho_mid = #{p in [31,97]: (N|p)=+1}/67 [literal per brief; OLS
      absorbs the constant so scale is inert] + secondary full-mid variant over
      primes 31..356 (the lab's stated mid range, 61 primes)
  (e) H3 alternative: prime-power hits -- fraction of values divisible by p^2 for
      some p<=13 (pp_any) and summed per-p fractions (pp_sum)

PRE-STATED HYPOTHESES (written BEFORE any data collection):
  H1: mid-prime hit fractions n_p for p in {31..97} (individual features OR their
      PCA-first-component) add >= +0.03 out-of-sample R^2 over the (w,d,small-n_p)
      baseline at u=3.5.
  H2: the residual correlates with mid-QR density -- rho_mid^2 adds >= +0.02 R^2
      beyond all linear terms (model already containing rho_mid linearly).
  H3: NOTHING tested adds >= +0.02 -- the tight-u content is non-footprint structure
      not capturable by marginal fractions or densities (e.g. prime-power hits p^2|v_j).

DECISION RULES (pre-stated):
  Band rule per hypothesis threshold t: PASS = point est >= t AND bootstrap CI low > 0;
  MARGINAL = point >= t but CI straddles 0; FAIL otherwise.
  H1_pass uses the better of {individual, PC1} encodings.
  Verdict names: H1 pass -> MID-PRIME-CARRIES; else H2 pass -> DENSITY-SQUARE-CARRIES;
  else pp_any/pp_sum block passes its +0.02 band -> PRIME-POWER-CARRIES;
  else -> NONFOOTPRINT-CONFIRMED.

PROTOCOL: OLS train/test split 900/300 (seeded permutation of the 1200 rows);
nested models M0(a) < M1(+small) < M2(+mid indiv) / M2pc(+PC1) < M3(+rho_lin) <
M3s(+rho^2) < M4(+ppow); increments = test-R^2 differences; bootstrap 300 resamples
(rows drawn with replacement from all 1200; first 900 positions train, last 300 test)
for percentile CIs on every increment; PCA fit on TRAIN only (rotation frozen across
bootstrap refits, disclosed). u=2.5 anchor computed free from the same strip pass.

# BARRIERS (standard lines, verbatim exp500/exp501/exp503):
#   Barrier 5 (structural orthogonality): T and all features here are N-only natural
#   coordinates; the dial predicts relation yield (difficulty), not (p,q) - no
#   which-factor claim made or tested.
#   Barrier 8 (known-method-in-disguise): the measured object is the QS/CFRAC
#   relation-yield dial - a cost predictor FOR known methods, not a new factoring route.
"""
import json, time, math, datetime, os, sys
import numpy as np
import gmpy2
from sympy import primerange, nextprime

BASE_SEED = 20260927          # 20260926+1
ANALYSIS_SEED = 20260928      # separate stream: split + bootstrap
NN, W = 1200, 240
US = (3.5, 2.5)
SMALL_P = [3, 5, 7, 11, 13, 17, 19, 23, 29]
MID_P = [31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
D_PRIMES = [2, 3, 5, 7, 11, 13]
MID_FULL_HI = 356             # lab's stated mid range 31..356
RHO_DENOM = 67                # literal per brief
NTRAIN, NTEST = 900, 300
NBOOT = 300
T0 = time.time()
WORK = "/tmp/exp46_mid"

OUT = {"meta": {"exp": 505, "codename": "MID-PRIME-HUNT", "round": 46,
                "population_seed": BASE_SEED, "analysis_seed": ANALYSIS_SEED,
                "Ns_per_population": NN, "values_per_N": W, "us": list(US),
                "small_primes": SMALL_P, "mid_primes": MID_P,
                "rho_denom_literal": RHO_DENOM, "nboot": NBOOT,
                "split": f"{NTRAIN}/{NTEST}",
                "constructions": "verbatim exp497/499/500/501/503 bitlen-44 balanced "
                                 "window arm, j=1..240 Fermat offsets, vmed pooled "
                                 "per population",
                "prestated": {
                    "H1": "mid n_p (31..97) individual or PC1 add >= +0.03 OOS R2 "
                          "over (w,d,small-n_p) baseline at u=3.5",
                    "H2": "rho_mid^2 adds >= +0.02 R2 beyond all linear terms",
                    "H3": "nothing tested adds >= +0.02 (non-footprint structure)",
                    "bands": "PASS = point >= t and CI_low > 0; MARGINAL = point >= t "
                             "and CI straddles 0; else FAIL"}}}

def ledger(event, **kw):
    rec = {"ts": datetime.datetime.now().isoformat(timespec="seconds"),
           "exp": 505, "codename": "MID-PRIME-HUNT", "event": event,
           "t_s": round(time.time() - T0, 1)}
    rec.update(kw)
    with open(f"{WORK}/ledger_exp505.jsonl", "a") as f:
        f.write(json.dumps(rec, default=float) + "\n")

def checkpoint():
    json.dump(OUT, open(f"{WORK}/result.json", "w"), indent=1, default=float)

def log(msg):
    print("[%7.1fs] %s" % (time.time() - T0, msg), flush=True)

os.makedirs(WORK, exist_ok=True)

# ------------------------------------------------------------- stage 0: ledger start
ledger("start", base_seed=BASE_SEED, workdir=WORK, nn=NN, w=W, us=list(US),
       small_primes=SMALL_P, mid_primes=MID_P, prestated=OUT["meta"]["prestated"],
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
    # verbatim exp499/exp500/exp501/exp503 draw_balanced
    while True:
        r = int(rng.integers(lo, hi))
        p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, 10**5))))
        N = p * q
        if not ((1 << 43) <= N < (1 << 44)):
            continue
        return N, math.isqrt(N)

wr = list(primerange(3, 401))   # odd primes <= 400

def qr_mask(N, p):
    p = int(p)
    return gmpy2.powmod(int(N) % p, (p - 1) // 2, p) == 1

def t_dial_and_qr(Ns):
    """w/T dial (odd p<=400), qrc (odd p<=100), plus QR masks for mid sets."""
    tw = np.zeros(len(Ns)); qrc = np.zeros(len(Ns))
    mid_cnt = np.zeros(len(Ns)); full_cnt = np.zeros(len(Ns))
    wr_arr = np.array(wr); mid_arr = np.array(MID_P)
    full_arr = np.array([p for p in primerange(31, MID_FULL_HI + 1)])
    for N_i, N in enumerate(Ns):
        Nm = int(N)
        syms = [gmpy2.powmod(Nm % int(q), (int(q) - 1) // 2, int(q)) for q in wr_arr]
        qr400 = np.fromiter((s == 1 for s in syms), bool, len(wr_arr))
        tw[N_i] = (2.0 / wr_arr)[qr400].sum()
        qrc[N_i] = qr400[wr_arr <= 100].sum()
        mid_cnt[N_i] = sum(qr_mask(Nm, p) for p in mid_arr)
        full_cnt[N_i] = sum(qr_mask(Nm, p) for p in full_arr)
    return tw, qrc, mid_cnt, full_cnt

def fermat_offsets(Ns, sqs, Wmax):
    js = np.arange(1, Wmax + 1, dtype=np.int64)
    sq = np.asarray(sqs, dtype=np.int64)[:, None]
    N = np.asarray(Ns, dtype=np.int64)[:, None]
    V = js[None, :] * (2 * sq + js[None, :]) + (sq * sq - N)
    assert (V > 0).all(), "positivity violated"
    assert V.dtype == np.int64 and V.max() < 2**62
    return V

# ------------------------------------------------------------- stage 1: population
rng_pop = np.random.default_rng(BASE_SEED)
t1 = time.time()
pairs = [draw_one(rng_pop, LO44, HI44) for _ in range(NN)]
Ns_list = [d[0] for d in pairs]; sqs = [d[1] for d in pairs]
assert len(set(Ns_list)) == NN, "Ns must be unique"
OUT["stage1_population"] = {
    "n_unique": len(set(Ns_list)),
    "bitlen_min": min(int(x).bit_length() for x in Ns_list),
    "bitlen_max": max(int(x).bit_length() for x in Ns_list),
    "wall_s": round(time.time() - t1, 1)}
OUT["Ns"] = [int(x) for x in Ns_list]
checkpoint(); ledger("population_done", **OUT["stage1_population"])
log("stage 1: population built %s" % OUT["stage1_population"])

# ------------------------------------------------------------- stage 2: targets
t2 = time.time()
V = fermat_offsets(Ns_list, sqs, W)
vmed = float(np.median(V.astype(float)))
B = {u: max(int(round(math.exp(math.log(vmed) / u))), 50) for u in US}
BMAX = max(B.values())                      # strip once to max B
Q = V.copy()
lpf = np.zeros(V.shape, dtype=np.int64)
strip_primes = primes_all[primes_all <= BMAX]
for p in strip_primes:
    while True:
        m = Q % p == 0
        if not m.any():
            break
        Q[m] //= p
        lpf[m] = p                          # multiplicity-aware largest-found tracking
smooth = {u: (Q == 1) & (lpf <= B[u]) for u in US}
rate = {u: smooth[u].mean(axis=1) for u in US}     # y target per N
OUT["stage2_targets"] = {
    "vmed": vmed, "B_3.5": B[3.5], "B_2.5": B[2.5], "n_strip_primes": int(len(strip_primes)),
    "mean_rate_3.5": round(float(rate[3.5].mean()), 6),
    "mean_rate_2.5": round(float(rate[2.5].mean()), 6),
    "frac_smooth_both_u": round(float((smooth[3.5] & smooth[2.5]).mean()), 6),
    "wall_s": round(time.time() - t2, 1)}
checkpoint(); ledger("targets_done", **OUT["stage2_targets"])
log("stage 2: targets %s" % OUT["stage2_targets"])

np.savez_compressed(f"{WORK}/arrays.npz", V=V.astype(np.float64),
                    rate35=rate[3.5], rate25=rate[2.5])

# ------------------------------------------------------------- stage 3: features
t3 = time.time()
tw, qrc, mid_cnt, full_cnt = t_dial_and_qr(Ns_list)
Vm = V.astype(np.int64)
n_small = np.stack([(Vm % p == 0).mean(axis=1) for p in SMALL_P], axis=1)   # (1200, 9)
n_mid = np.stack([(Vm % p == 0).mean(axis=1) for p in MID_P], axis=1)       # (1200,15)
div13 = np.zeros(V.shape, dtype=bool)
ppow_any = np.zeros(V.shape, dtype=bool)
pp_sum = np.zeros(len(Ns_list))
pp_cols = []
for p in D_PRIMES:
    div13 |= (Vm % p == 0)
    sq_mask = (Vm % (p * p) == 0)
    ppow_any |= sq_mask
    c = sq_mask.mean(axis=1)
    pp_sum += c
    pp_cols.append(c)
d13 = div13.mean(axis=1)
rho_mid = mid_cnt / RHO_DENOM               # literal per brief (scale inert under OLS)
rho_full = full_cnt / len(full_arr := np.array([p for p in primerange(31, MID_FULL_HI + 1)]))
sp_T_35 = spearman(tw, rate[3.5]); sp_T_25 = spearman(tw, rate[2.5])
OUT["stage3_features"] = {
    "feature_conventions": {
        "w/T": "sum 2/p over odd QR primes p<=400 (Euler criterion)",
        "qrc": "count of odd QR primes p<=100",
        "d": "fraction of the 240 values divisible by >=1 prime in {2,3,5,7,11,13}",
        "n_p": "fraction of the 240 values divisible by p",
        "rho_mid": "#QR among p in [31,97] / %d (literal brief form)" % RHO_DENOM,
        "rho_full": "#QR among primes 31..356 / 61",
        "pp_any": "fraction of values divisible by p^2 for >=1 p<=13",
        "pp_sum": "sum over p<=13 of fraction of values divisible by p^2"},
    "mean_n_p_small": {str(p): round(float(m), 5) for p, m in zip(SMALL_P, n_small.mean(0))},
    "mean_n_p_mid": {str(p): round(float(m), 5) for p, m in zip(MID_P, n_mid.mean(0))},
    "theory_2_over_p_mid": {str(p): round(2.0 / p, 5) for p in MID_P},
    "rho_mid_mean_sd": [round(float(rho_mid.mean()), 5), round(float(rho_mid.std()), 5)],
    "rho_full_mean_sd": [round(float(rho_full.mean()), 5), round(float(rho_full.std()), 5)],
    "pp_any_mean": round(float(ppow_any.mean(axis=1).mean()), 6),
    "pp_sum_mean": round(float(pp_sum.mean()), 6),
    "anchor_sp_T_3.5": round(sp_T_35, 4), "anchor_sp_T_2.5": round(sp_T_25, 4),
    "anchor_drop_2.5_minus_3.5": round(sp_T_25 - sp_T_35, 4),
    "wall_s": round(time.time() - t3, 1)}
checkpoint(); ledger("features_done", **{k: v for k, v in OUT["stage3_features"].items()
                                         if k != "feature_conventions"})
log("stage 3: features done; anchors sp(T;3.5)=%.4f sp(T;2.5)=%.4f drop=%.4f"
    % (sp_T_35, sp_T_25, sp_T_25 - sp_T_35))

# ------------------------------------------------------------- stage 4: models
rng_an = np.random.default_rng(ANALYSIS_SEED)
perm = rng_an.permutation(NN)
TR, TE = perm[:NTRAIN], perm[NTRAIN:]
ones_all = np.ones((NN, 1))

def col(*blocks):
    return np.column_stack(blocks)

A = col(ones_all, tw, qrc, d13)                       # M0 base (paper-145 dial)
AS = col(A, n_small)                                  # M1
ASM = col(AS, n_mid)                                  # M2
mu, sd = n_mid[TR].mean(0), n_mid[TR].std(0)
Zm_tr = (n_mid[TR] - mu) / sd
_, _, Vt = np.linalg.svd(Zm_tr - Zm_tr.mean(0), full_matrices=False)
pc1_dir = Vt[0]
pc1_all = ((n_mid - mu) / sd - Zm_tr.mean(0)) @ pc1_dir
ASPC = col(AS, pc1_all.reshape(-1, 1))                # M2pc
ASMR = col(ASM, rho_mid.reshape(-1, 1))               # M3
ASRR = col(ASMR, (rho_mid**2).reshape(-1, 1))         # M3s
PP = col(ppow_any.mean(axis=1).reshape(-1, 1), pp_sum.reshape(-1, 1))
ASMP = col(ASMR, PP)                                  # M3pp (rho lin + ppow, no square)
ASRP = col(ASRR, PP)                                  # M4 everything

MODELS = {"M0_base": A, "M1_small": AS, "M2_mid": ASM, "M2pc_pc1": ASPC,
          "M3_rho": ASMR, "M3s_rhosq": ASRR, "M3pp_rho_ppow": ASMP, "M4_all": ASRP}
INCREMENTS = [
    ("dR2_small_over_base", "M1_small", "M0_base"),
    ("dR2_mid_indiv", "M2_mid", "M1_small"),
    ("dR2_mid_pc1", "M2pc_pc1", "M1_small"),
    ("dR2_rho_lin", "M3_rho", "M2_mid"),
    ("dR2_rhosq_beyond_linear", "M3s_rhosq", "M3_rho"),
    ("dR2_ppow", "M4_all", "M3s_rhosq"),
    ("dR2_total", "M4_all", "M0_base"),
    ("sens_dR2_rhosq_last", "M4_all", "M3pp_rho_ppow"),
    ("sens_dR2_ppow_before_sq", "M3pp_rho_ppow", "M3_rho")]

def ols_fit(Xtr, ytr):
    coef, *_ = np.linalg.lstsq(Xtr, ytr, rcond=None)
    return coef

def r2_test(model, beta, te_idx, y):
    pred = model[te_idx] @ beta
    resid = y[te_idx] - pred
    return 1.0 - (resid @ resid) / (((y[te_idx] - y[te_idx].mean()) ** 2).sum())

y35 = rate[3.5]
betas, r2_te, r2_tr = {}, {}, {}
for name, X in MODELS.items():
    betas[name] = ols_fit(X[TR], y35[TR])
    pr_tr = X[TR] @ betas[name]
    r2_tr[name] = 1.0 - ((y35[TR] - pr_tr) ** 2).sum() / ((y35[TR] - y35[TR].mean()) ** 2).sum()
    r2_te[name] = r2_test(X, betas[name], TE, y35)

inc_point = {nm: r2_te[inm] - r2_te[outm] for nm, inm, outm in INCREMENTS}

# bootstrap: rows with replacement from all 1200; first 900 positions train, last 300 test
boot_idx = rng_an.integers(0, NN, size=(NBOOT, NN))
inc_boot = {nm: np.zeros(NBOOT) for nm, _, _ in INCREMENTS}
keys = list(MODELS)
Xs = {k: MODELS[k] for k in keys}
for b in range(NBOOT):
    idx = boot_idx[b]
    tr_b, te_b = idx[:NTRAIN], idx[NTRAIN:]
    yte = y35[te_b]
    ss_te = ((yte - yte.mean()) ** 2).sum()
    r2b = {}
    for k in keys:
        bt = ols_fit(Xs[k][tr_b], y35[tr_b])
        pr = Xs[k][te_b] @ bt
        r2b[k] = 1.0 - ((yte - pr) ** 2).sum() / ss_te
    for nm, inm, outm in INCREMENTS:
        inc_boot[nm][b] = r2b[inm] - r2b[outm]

ci = lambda a: [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]
inc_table = {}
for nm, inm, outm in INCREMENTS:
    lo, hi = ci(inc_boot[nm])
    inc_table[nm] = {"point": round(inc_point[nm], 4), "CI": [round(lo, 4), round(hi, 4)],
                     "inner": inm, "outer": outm}

# descriptive: which mid primes carry weight (full-population fit of M2)
b_full, *_ = np.linalg.lstsq(ASM, y35, rcond=None)
mid_t = {}
resid_m2 = y35 - ASM @ b_full
dof = NN - ASM.shape[1]
s2 = float(resid_m2 @ resid_m2) / dof
se = np.sqrt(np.diag(s2 * np.linalg.pinv(ASM.T @ ASM)))
for i, p in enumerate(MID_P):
    mid_t[str(p)] = round(float(b_full[3 + 9 + i] / se[3 + 9 + i]), 2)
pc1_load_corr = float(np.corrcoef(pc1_dir, np.array([2.0 / p for p in MID_P]))[0, 1])

OUT["stage4_models"] = {
    "R2_train": {k: round(v, 4) for k, v in r2_tr.items()},
    "R2_test": {k: round(v, 4) for k, v in r2_te.items()},
    "increments": inc_table,
    "mid_coef_t_full_M2": mid_t,
    "pc1_dir_vs_theory_2_over_p_corr": round(pc1_load_corr, 4),
    "base_anchor_R2test_M0": round(r2_te["M0_base"], 4)}

# ---- stage 4b: OOS Spearman ladder (does anything climb toward the 0.747 anchor?)
spear_ladder = {}
for k in keys:
    pr_full = Xs[k] @ ols_fit(Xs[k][TR], y35[TR])
    spear_ladder[k] = {"sp_test": round(spearman(pr_full[TE], y35[TE]), 4),
                       "sp_fullpop": round(spearman(pr_full, y35), 4)}
# t-stats for the prime-power block in M4 (full-population fit)
b_m4, *_ = np.linalg.lstsq(ASRP, y35, rcond=None)
res4 = y35 - ASRP @ b_m4
se4 = np.sqrt(np.diag(float(res4 @ res4) / (NN - ASRP.shape[1])
                      * np.linalg.pinv(ASRP.T @ ASRP)))
pp_t = {"pp_any_t": round(float(b_m4[-2] / se4[-2]), 2),
        "pp_sum_t": round(float(b_m4[-1] / se4[-1]), 2)}
corr_pp_rate = float(np.corrcoef(pp_sum, y35)[0, 1])
mean_rate_ppany = [round(float(y35[ppow_any.mean(axis=1) == 0].mean()), 5),
                   round(float(y35[ppow_any.mean(axis=1) > 0].mean()), 5)]
OUT["stage4b_spearman_ladder"] = {"models": spear_ladder,
                                  "anchor_sp_T_2.5": round(sp_T_25, 4),
                                  "zero_fit_dial_sp_T_3.5": round(sp_T_35, 4),
                                  "pp_block_full_M4": pp_t,
                                  "corr_ppsum_rate": round(corr_pp_rate, 4),
                                  "rate_by_ppany_hit": {"no_p2_hit": mean_rate_ppany[0],
                                                        "has_p2_hit": mean_rate_ppany[1]}}

# ------------------------------------------------------------- stage 5: verdicts
def band(point, CI, t):
    if point >= t and CI[0] > 0:
        return "PASS"
    if point >= t and CI[0] <= 0 <= CI[1]:
        return "MARGINAL"
    return "FAIL"

best_h1 = max(("dR2_mid_indiv", "dR2_mid_pc1"), key=lambda k: inc_table[k]["point"])
H1_band = band(inc_table[best_h1]["point"], inc_table[best_h1]["CI"], 0.03)
H1 = H1_band == "PASS"
H2_band = band(inc_table["dR2_rhosq_beyond_linear"]["point"],
               inc_table["dR2_rhosq_beyond_linear"]["CI"], 0.02)
H2 = H2_band == "PASS"
others = ["dR2_mid_indiv", "dR2_mid_pc1", "dR2_rho_lin", "dR2_rhosq_beyond_linear"]
pp_keys = ["dR2_ppow"]
any_ge_002 = [k for k in others if inc_table[k]["point"] >= 0.02]
pp_ge = [k for k in pp_keys if inc_table[k]["point"] >= 0.02 and band(inc_table[k]["point"], inc_table[k]["CI"], 0.02) == "PASS"]
H3 = (not any_ge_002) and (not pp_ge)

if H1:
    name = "MID-PRIME-CARRIES"
elif H2:
    name = "DENSITY-SQUARE-CARRIES"
elif pp_ge:
    name = "PRIME-POWER-CARRIES"
else:
    name = "NONFOOTPRINT-CONFIRMED"

OUT["verdict"] = {
    "H1": {"encoding_used": best_h1, "band": H1_band, "pass": H1,
           "detail": {k: inc_table[k] for k in ("dR2_mid_indiv", "dR2_mid_pc1")}},
    "H2": {"band": H2_band, "pass": H2,
           "detail": {k: inc_table[k] for k in ("dR2_rho_lin", "dR2_rhosq_beyond_linear",
                                                "sens_dR2_rhosq_last")}},
    "H3": {"pass": H3, "features_ge_0.02": any_ge_002 + pp_ge,
           "pp_detail": {k: inc_table[k] for k in ("dR2_ppow", "sens_dR2_ppow_before_sq")}},
    "verdict_name": name}
OUT["barrier_lines"] = {
    "barrier_5": "Structural orthogonality: T and all features here are N-only natural "
                 "coordinates; the dial predicts relation yield (difficulty), not (p,q) "
                 "- no which-factor claim made or tested.",
    "barrier_8": "Known-method-in-disguise: the measured object is the QS/CFRAC "
                 "relation-yield dial - a cost predictor FOR known methods, not a new "
                 "factoring route."}
OUT["artifacts"] = [f"{WORK}/exp505_mid_prime_hunt.py", f"{WORK}/result.json",
                    f"{WORK}/ledger_exp505.jsonl", f"{WORK}/arrays.npz"]
checkpoint()
ledger("DONE", status="DONE", verdict_name=name, verdict=OUT["verdict"],
       increments=inc_table, anchors={"sp_T_3.5": round(sp_T_35, 4),
                                      "sp_T_2.5": round(sp_T_25, 4)},
       barriers=["5", "8"], artifacts=OUT["artifacts"])

print("\n=== EXP 505 MID-PRIME-HUNT ===")
print("anchors: sp(T;3.5)=%.4f sp(T;2.5)=%.4f drop=%.4f | mean rates %.4f/%.4f"
      % (sp_T_35, sp_T_25, sp_T_25 - sp_T_35, rate[3.5].mean(), rate[2.5].mean()))
print("%-24s %-8s %-18s" % ("increment", "point", "bootstrap CI"))
for nm, _, _ in INCREMENTS:
    print("%-24s %+8.4f  [%+.4f,%+.4f]" % (nm, inc_table[nm]["point"],
                                           inc_table[nm]["CI"][0], inc_table[nm]["CI"][1]))
print("R2 test:", {k: round(v, 4) for k, v in r2_te.items()})
print("VERDICT:", name, "| H1", H1_band, "H2", H2_band, "H3 pass" if H3 else "H3 REFUTED")
print("DONE %.1fs" % (time.time() - T0))

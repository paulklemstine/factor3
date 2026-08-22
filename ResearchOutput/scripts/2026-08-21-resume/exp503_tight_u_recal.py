#!/usr/bin/env python3
"""EXP 503 TIGHT-U-RECAL (round-45 #4). Base seeds 20260990..20260999 (+20261000 bitlen-48).
Paper 169 (exp502): the dial's u-sensitivity is GENUINE THRESHOLD REWEIGHTING - at tight
u=3.5 the QR primes that dominate the relation-yield rate shift, and bound shrinkage
contributes only ~9%. Named follow-up (paper 169): RECALIBRATE THE FOOTPRINT WEIGHTS
THEMSELVES at tight u and test whether the recalibrated weights recover paper 167's drop.
Paper 167 anchors (exp500, 240 values): zero-fit dial T(N)=sum(2/p | QR p<=400) has
sp(2.5) ~ 0.737 and sp(3.5) ~ 0.616 (drop ~0.12); paper 165 anchor sp(T) ~ 0.73.

Constructions VERBATIM from exp497/exp499/exp500/exp501: bitlen-44 balanced window
[isqrt(2^43)+1, isqrt(2^44-1)) with exact-bitlen enforcement, inter-prime gap U[1,1e5);
sq = isqrt(N); V = js*(2*sq+js) + (sq*sq - N)  (Fermat offsets), j=1..240; positivity
asserted; B(u) = max(int(round(exp(ln(vmed)/u))), 50), vmed POOLED PER POPULATION
(median of all its V); smooth@u iff rem==1 after stripping primes <= B AND maxp <= B;
rate(N,u) = fraction of the 240 offsets smooth at u; T(N) computed once per population;
Spearman via ordinal argsort (verbatim exp497/exp501).

FEATURES (the recalibration object): n_p(N) = fraction of the 240 VALUES divisible by
p ("direct divisibility on values", paper 145's independent second feature family),
for p in {3,5,7,11,13,17,19,23,29} - 9 features. Note E[n_p] = 2/p if N is QR mod p
else 0, so T(N) = sum over QR p<=400 of (2/q) is exactly the THEORY prediction of the
unweighted footprint sum; refitting beta_p at tight u asks which primes the TIGHT
threshold actually pays for.

DESIGN: 10 independent populations bitlen 44 (seeds 20260990..99), 1200 Ns each,
240 values each; smoothness measured at u=3.5 AND u=2.5. TRAIN = seeds ..94 (5 pops,
6000 rows), TEST = seeds ..99 (5 pops, held out). ALSO 600 Ns bitlen 48 (seed 20261000,
same construction, own pooled vmed) for H3 transfer.

PRE-STATED HYPOTHESES (written BEFORE any exp-503 data):
  H1 (recalibration recovers the drop): OLS beta fitted on the TRAIN pool at u=3.5
      (rate ~ n_3..n_29 + intercept) achieves OOS Spearman(rate, T'(N)) >= 0.70 on
      EVERY-analyzed MEAN over the 5 held-out populations (primary = point estimate of
      the mean, bootstrap CI as evidence) - recovering most of paper 167's drop from
      the ~0.63 level toward the 0.73 anchor.
  H2 (rank stability): the fitted beta vectors are RANK-STABLE - Spearman between
      beta-vectors fit on disjoint halves of the TRAIN pool exceeds 0.7 in the mean
      over 200 random split-halves (rows permuted, 3000/3000).
  H3 (transfer): a SINGLE recalibrated scalar dial T'(N) = b0 + sum(beta_p*n_p)
      fitted ONLY at bitlen 44 transfers to bitlen 48 with Spearman >= 0.60.
  Same pipeline re-run at u=2.5 for comparison (no pre-stated threshold; reported).

DECISION RULES: verdict names by combination -
  H1&H2&H3 -> RECAL-FULL-RECOVERY; H1&H2,!H3 -> RECAL-IN-DISTRIBUTION;
  !H1 -> NO-RECAL-RECOVERY (H2/H3 annotated); H1,!H2 -> RECAL-OVERFIT-RISK.

# BARRIERS (standard lines, verbatim exp500/exp501):
#   Barrier 5 (structural orthogonality): T and T' are N-only natural coordinates; the
#   dial predicts relation yield (difficulty), not (p,q) - no which-factor claim made
#   or tested.
#   Barrier 8 (known-method-in-disguise): the measured object is the QS/CFRAC
#   relation-yield dial - a cost predictor FOR known methods, not a new factoring route.
"""
import json, time, math, datetime, os
import numpy as np
import gmpy2
from sympy import primerange, nextprime

BASE = 20260990
NSEED = 10
NN = 1200
W = 240
US = (3.5, 2.5)
FEATP = [3, 5, 7, 11, 13, 17, 19, 23, 29]
N_TRAIN = 5                      # first NSEED populations train, rest held out
B48_SEED = 20261000
N48 = 600
BOOT_N = 500                     # H1 CI over test populations (house style exp501)
BOOT_SEED = 20261001
SPLITS_H2 = 200                  # split-half beta stability resamples
H2_SEED = 20261002
T0 = time.time()
WORK = "/tmp/exp45_recal"
OUT = {"meta": {"base_seed": BASE, "exp": 503, "codename": "TIGHT-U-RECAL",
                "round": 45,
                "populations": [BASE + k for k in range(NSEED)],
                "Ns_per_population": NN, "values_per_N": W, "us": list(US),
                "feature_primes": FEATP, "n_train_populations": N_TRAIN,
                "bitlen48_seed": B48_SEED, "Ns_bitlen48": N48,
                "boot_resamples_H1": BOOT_N, "splits_H2": SPLITS_H2,
                "constructions": "verbatim exp497/exp499/exp500/exp501 bitlen-44 "
                                 "balanced arm, j=1..240 Fermat offsets, vmed pooled "
                                 "per population; bitlen-48 arm same construction "
                                 "own vmed",
                "prestated": {
                    "H1_recovery": "mean OOS Spearman(rate, T') at u=3.5 over the 5 "
                                   "held-out populations >= 0.70",
                    "H2_stability": "mean split-half Spearman(beta_A, beta_B) > 0.70 "
                                    "over 200 disjoint row-halves of TRAIN",
                    "H3_transfer": "Spearman(T'44, rate) at bitlen 48, u=3.5, >= 0.60",
                    "rules": "all->RECAL-FULL-RECOVERY; H1&H2!H3->RECAL-IN-DISTRIBUTION; "
                             "!H1->NO-RECAL-RECOVERY; H1!H2->RECAL-OVERFIT-RISK"}},
        "rows": []}

def ledger(event, **kw):
    rec = {"ts": datetime.datetime.now().isoformat(timespec="seconds"),
           "round": 45, "exp": 503, "codename": "TIGHT-U-RECAL",
           "event": event, "t_s": round(time.time() - T0, 1)}
    rec.update(kw)
    with open(f"{WORK}/ledger_exp503.jsonl", "a") as f:
        f.write(json.dumps(rec, default=float) + "\n")
    return rec

def checkpoint():
    json.dump(OUT, open(f"{WORK}/result.json", "w"), indent=1, default=float)

primes_all = np.array(list(primerange(2, 400000)), dtype=np.int64)

def smooth_mask(V, B):
    # verbatim exp497/exp500/exp501 (numpy trial division strip, multiplicity aware)
    Wc = V.copy()
    for p in primes_all[primes_all <= B]:
        while True:
            m = Wc % p == 0
            if not m.any(): break
            Wc[m] //= p
            if not (Wc % p == 0).any(): break
    return Wc == 1

def spearman(a, b):
    # verbatim exp497/exp500/exp501 (ordinal argsort)
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])

LO44 = int(gmpy2.isqrt(1 << 43)) + 1
HI44 = int(gmpy2.isqrt((1 << 44) - 1))
LO48 = int(gmpy2.isqrt(1 << 47)) + 1
HI48 = int(gmpy2.isqrt((1 << 48) - 1))

def draw_one(rng, lo, hi, blen):
    # verbatim exp499/exp500/exp501 draw_balanced (window, gap U[1,1e5), redraws);
    # exact-bitlen enforcement hardcoded per arm in exp501 -> blen parameter here
    # (exp501: (1<<43) <= N < (1<<44); ledger catch #1 pre-launch)
    while True:
        r = int(rng.integers(lo, hi))
        p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, 10**5))))
        N = p * q
        if not ((1 << (blen - 1)) <= N < (1 << blen)):
            continue
        return N, math.isqrt(N)

def fermat_offsets(Ns, sqs, Wmax):
    # verbatim V = js*(2*sq+js) + (sq*sq - N)
    js = np.arange(1, Wmax + 1, dtype=np.int64)
    sq = np.asarray(sqs, dtype=np.int64)[:, None]
    N = np.asarray(Ns, dtype=np.int64)[:, None]
    V = js[None, :] * (2 * sq + js[None, :]) + (sq * sq - N)
    assert (V > 0).all(), "positivity violated"
    return V

wr = list(primerange(3, 401))

def t_dial(Ns):
    # verbatim exp497/exp500/exp501 (zero-fit theory dial, once per population)
    return np.array([sum(2.0/q for q in wr
                         if gmpy2.powmod(int(N) % q, (q - 1) // 2, q) == 1)
                     for N in Ns], float)

featp_arr = np.array(FEATP, dtype=np.int64)

def features(V):
    # n_p = fraction of the W values divisible by p (direct divisibility on values)
    return np.stack([(V % p == 0).mean(axis=1) for p in featp_arr], axis=1)

os.makedirs(WORK, exist_ok=True)

def build_population(seed, nn, lo, hi, blen, tag):
    rng = np.random.default_rng(seed)
    pairs = [draw_one(rng, lo, hi, blen) for _ in range(nn)]
    Ns = [d[0] for d in pairs]; sqs = [d[1] for d in pairs]
    Ts = t_dial(Ns)
    V = fermat_offsets(Ns, sqs, W)
    Fm = features(V)
    cell = {"tag": tag, "seed": seed, "Ts": Ts, "F": Fm}
    vmed = float(np.median(V.astype(float)))
    cell["vmed"] = vmed
    for u in US:
        B = max(int(round(math.exp(math.log(vmed) / u))), 50)
        sm = smooth_mask(V, B)
        rate = sm.reshape(nn, W).mean(axis=1)
        cell[f"B_{u}"] = B
        cell[f"rate_{u}"] = rate
        cell[f"mean_rate_{u}"] = float(rate.mean())
        cell[f"sp_T_{u}"] = spearman(Ts, rate)
    cell["bitlen_range"] = [int(min(Ns).bit_length()), int(max(Ns).bit_length())]
    return cell

ledger("start", base_seed=BASE, workdir=WORK, n_populations=NSEED,
       Ns_per_population=NN, values_per_N=W, us=list(US),
       feature_primes=FEATP, train_test_split=f"{N_TRAIN}+{NSEED-N_TRAIN}",
       bitlen48=(B48_SEED, N48), constructions=OUT["meta"]["constructions"],
       prestated=OUT["meta"]["prestated"])
checkpoint()

POPS = []
for k in range(NSEED):
    seed = BASE + k
    c = build_population(seed, NN, LO44, HI44, 44, "b44")
    POPS.append(c)
    row = {"seed": seed,
           "sp_T_3.5": round(c["sp_T_3.5"], 4), "sp_T_2.5": round(c["sp_T_2.5"], 4),
           "B_3.5": c["B_3.5"], "B_2.5": c["B_2.5"],
           "mean_rate_3.5": round(c["mean_rate_3.5"], 5),
           "mean_rate_2.5": round(c["mean_rate_2.5"], 5),
           "vmed": round(c["vmed"], 1), "bitlen_range": c["bitlen_range"]}
    OUT["rows"].append(row)
    checkpoint()
    ledger("population_done", **row)
    print("b44", seed, "spT %.4f/%.4f" % (row["sp_T_3.5"], row["sp_T_2.5"]),
          "rates %.4f/%.4f" % (row["mean_rate_3.5"], row["mean_rate_2.5"]),
          "B", row["B_3.5"], row["B_2.5"], round(time.time() - T0, 1), "s", flush=True)

C48 = build_population(B48_SEED, N48, LO48, HI48, 48, "b48")
OUT["rows"].append({"seed": B48_SEED, "tag": "b48",
                    "sp_T_3.5": round(C48["sp_T_3.5"], 4),
                    "sp_T_2.5": round(C48["sp_T_2.5"], 4),
                    "B_3.5": C48["B_3.5"], "B_2.5": C48["B_2.5"],
                    "mean_rate_3.5": round(C48["mean_rate_3.5"], 5),
                    "mean_rate_2.5": round(C48["mean_rate_2.5"], 5),
                    "vmed": round(C48["vmed"], 1),
                    "bitlen_range": C48["bitlen_range"]})
checkpoint()
ledger("population_done_b48", seed=B48_SEED, sp_T_35=round(C48["sp_T_3.5"], 4),
       sp_T_25=round(C48["sp_T_2.5"], 4), B_35=C48["B_3.5"],
       mean_rate_35=round(C48["mean_rate_3.5"], 5))
print("b48", B48_SEED, "spT %.4f/%.4f" % (C48["sp_T_3.5"], C48["sp_T_2.5"]),
      round(time.time() - T0, 1), "s", flush=True)

# ---- fitting machinery ----
def ols_fit(X, y):
    A = np.concatenate([X, np.ones((X.shape[0], 1))], axis=1)
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return coef[:-1], float(coef[-1])          # (beta, intercept)

train = POPS[:N_TRAIN]
test = POPS[N_TRAIN:]

Xtr = np.concatenate([c["F"] for c in train], axis=0)
results = {}
for u in US:
    ytr = np.concatenate([c[f"rate_{u}"] for c in train], axis=0)
    beta, b0 = ols_fit(Xtr, ytr)
    oos = []
    for c in test:
        pred = c["F"] @ beta + b0
        oos.append(spearman(pred, c[f"rate_{u}"]))
    results[u] = {"beta": beta.tolist(), "intercept": b0,
                  "oos_per_population": oos}
    print("fit u=%.1f beta=" % u, np.round(beta, 4), "b0=%.5f" % b0,
          "oos=", np.round(oos, 4), flush=True)

# ---- H2: split-half rank stability of beta (200 disjoint row-halves of TRAIN) ----
h2rng = np.random.default_rng(H2_SEED)
n_rows = Xtr.shape[0]
half = n_rows // 2
stab = []
for _ in range(SPLITS_H2):
    perm = h2rng.permutation(n_rows)
    ia, ib = perm[:half], perm[half:2*half]
    ba, ca = ols_fit(Xtr[ia], np.concatenate([c["rate_3.5"] for c in train])[ia])
    bb, cb = ols_fit(Xtr[ib], np.concatenate([c["rate_3.5"] for c in train])[ib])
    stab.append(spearman(ba, bb))
stab = np.array(stab)
# leave-one-population-out beta agreement (secondary stability read)
lopo = []
for i in range(N_TRAIN):
    rest = [c for j, c in enumerate(train) if j != i]
    Xr = np.concatenate([c["F"] for c in rest], axis=0)
    yr = np.concatenate([c["rate_3.5"] for c in rest], axis=0)
    lopo.append(ols_fit(Xr, yr)[0])
lopo = np.array(lopo)
lopo_pairs = [spearman(lopo[i], lopo[j]) for i in range(N_TRAIN) for j in range(i)]

# ---- summary ----
mean = lambda x: float(np.mean(x))
sd = lambda x: float(np.std(x, ddof=1))
boot = np.random.default_rng(BOOT_SEED)
oos35 = np.array(results[3.5]["oos_per_population"])
oos25 = np.array(results[2.5]["oos_per_population"])
base35 = np.array([c["sp_T_3.5"] for c in test])
base25 = np.array([c["sp_T_2.5"] for c in test])
idx = lambda: boot.integers(0, len(test), len(test))
b_oos35 = np.array([mean(oos35[idx()]) for _ in range(BOOT_N)])
b_oos25 = np.array([mean(oos25[idx()]) for _ in range(BOOT_N)])
gain35 = oos35 - base35
b_gain = np.array([mean(gain35[idx()]) for _ in range(BOOT_N)])
ci = lambda a: [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]
anchor_drop = mean(base25) - mean(base35)                 # paper 167 drop on THESE test pops
recovery_frac = mean(gain35) / anchor_drop if anchor_drop else float("nan")

beta35 = np.array(results[3.5]["beta"])
beta25 = np.array(results[2.5]["beta"])
theory_profile = np.array([2.0 / p for p in FEATP])

# ---- H3 transfer (u=3.5 primary; u=2.5 secondary) ----
pred48_35 = C48["F"] @ beta35 + results[3.5]["intercept"]
pred48_25 = C48["F"] @ beta25 + results[2.5]["intercept"]
h3_35 = spearman(pred48_35, C48["rate_3.5"])
h3_25 = spearman(pred48_25, C48["rate_2.5"])

h1 = bool(mean(oos35) >= 0.70)
h2v = bool(stab.mean() > 0.70)
h3v = bool(h3_35 >= 0.60)
if h1 and h2v and h3v: name = "RECAL-FULL-RECOVERY"
elif h1 and h2v: name = "RECAL-IN-DISTRIBUTION"
elif h1: name = "RECAL-OVERFIT-RISK"
else: name = "NO-RECAL-RECOVERY"

OUT["summary"] = {
    "baseline_dial_on_test": {"sp_T_3.5_mean": round(mean(base35), 4),
                              "sp_T_3.5_sd": round(sd(base35), 4),
                              "sp_T_2.5_mean": round(mean(base25), 4),
                              "sp_T_2.5_sd": round(sd(base25), 4)},
    "recalibrated_OOS": {"u3.5": {"per_population": [round(v, 4) for v in oos35],
                                  "mean": round(mean(oos35), 4), "sd": round(sd(oos35), 4),
                                  "bootstrap_CI": [round(v, 4) for v in ci(b_oos35)]},
                         "u2.5": {"per_population": [round(v, 4) for v in oos25],
                                  "mean": round(mean(oos25), 4), "sd": round(sd(oos25), 4),
                                  "bootstrap_CI": [round(v, 4) for v in ci(b_oos25)]}},
    "paired_gain_at_3.5": {"per_population": [round(v, 4) for v in gain35],
                           "mean": round(mean(gain35), 4),
                           "bootstrap_CI": [round(v, 4) for v in ci(b_gain)],
                           "CI_excludes_zero": bool(ci(b_gain)[0] > 0 or ci(b_gain)[1] < 0)},
    "recovery_fraction_of_paper167_drop": round(float(recovery_frac), 4),
    "beta_vectors": {str(p): {"beta_3.5": round(float(b35), 5),
                              "beta_2.5": round(float(b25), 5),
                              "theory_2_over_p": round(t, 5)}
                     for p, b35, b25, t in zip(FEATP, beta35, beta25, theory_profile)},
    "beta_intercepts": {"u3.5": round(results[3.5]["intercept"], 6),
                        "u2.5": round(results[2.5]["intercept"], 6)},
    "beta_vs_theory_rankcorr": {"u3.5": round(spearman(beta35, theory_profile), 4),
                                "u2.5": round(spearman(beta25, theory_profile), 4)},
    "H2_stability": {"split_half_mean": round(float(stab.mean()), 4),
                     "split_half_sd": round(float(stab.std()), 4),
                     "frac_splits_above_0.7": round(float((stab > 0.7).mean()), 4),
                     "lopo_pairwise_min": round(min(lopo_pairs), 4),
                     "lopo_pairwise_mean": round(mean(lopo_pairs), 4)},
    "H3_transfer": {"bitlen48_sp_u3.5": round(h3_35, 4),
                    "bitlen48_sp_u2.5": round(h3_25, 4),
                    "b48_baseline_dial_sp_u3.5": round(C48["sp_T_3.5"], 4)}}

OUT["verdict"] = {"H1_recovery": h1, "H2_stability": h2v, "H3_transfer": h3v,
                  "verdict_name": name,
                  "rule_detail": {"oos35_mean": round(mean(oos35), 4),
                                  "threshold_H1": 0.70,
                                  "split_half_mean": round(float(stab.mean()), 4),
                                  "threshold_H2": 0.70,
                                  "bitlen48_sp": round(h3_35, 4),
                                  "threshold_H3": 0.60}}
OUT["barrier_lines"] = {
    "barrier_5": "Structural orthogonality: T and T' are N-only natural coordinates; "
                 "the dial predicts relation yield (difficulty), not (p,q) - no "
                 "which-factor claim made or tested.",
    "barrier_8": "Known-method-in-disguise: the measured object is the QS/CFRAC "
                 "relation-yield dial - a cost predictor FOR known methods, not a "
                 "new factoring route."}
OUT["artifacts"] = [f"{WORK}/exp503_tight_u_recal.py", f"{WORK}/result.json",
                    f"{WORK}/ledger_exp503.jsonl"]
checkpoint()
headline = (f"TIGHT-U-RECAL exp503: VERDICT {name}; "
            f"OOS sp(3.5) mean={mean(oos35):.4f} CI=[{ci(b_oos35)[0]:.4f},{ci(b_oos35)[1]:.4f}] "
            f"vs dial {mean(base35):.4f}; OOS sp(2.5)={mean(oos25):.4f} vs dial {mean(base25):.4f}; "
            f"split-half beta stability={stab.mean():.4f}; bitlen-48 sp={h3_35:.4f}")
ledger("DONE", status="DONE", headline=headline, verdict=OUT["verdict"],
       summary=OUT["summary"], barriers=["5", "8"], artifacts=OUT["artifacts"])
print(json.dumps(OUT["summary"]["recalibrated_OOS"]))
print(json.dumps(OUT["summary"]["H2_stability"]))
print(json.dumps(OUT["summary"]["H3_transfer"]))
print(json.dumps(OUT["verdict"]))
print(headline)
print("DONE", round(time.time() - T0, 1), "s")

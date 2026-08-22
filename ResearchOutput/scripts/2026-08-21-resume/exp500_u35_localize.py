#!/usr/bin/env python3
"""EXP 500 U35-LOCALIZE lean (round-45). Base seeds 20260950..20260963. Inline takeover.
Paper 166 (exp499 balanced@u3.5 column): the zero-fit dial T(N) = sum(2/p | QR primes
p<=400) is seed-stable at u=2.5 (per-seed Spearman in [0.71, 0.76]) but degrades
SYSTEMATICALLY at u=3.5 - all 5 seeds drop, one breaching deeply at 0.487, column
mean 0.598 below the band floor 0.60. Whether the typical bal@3.5 center is below the
floor (center shift) or the column is merely wide-tailed is unresolved at 5 seeds.
This experiment LOCALIZES it with 14 fresh populations at 5x the per-population N.

Constructions VERBATIM from exp497/exp499 (/tmp/exp44_tstable/exp497_t_dial_stable.py,
/tmp/exp44_tax/exp499_t_dial_axes.py): bitlen-44 balanced window
[isqrt(2^43)+1, isqrt(2^44-1)) with exact-bitlen enforcement, inter-prime gap U[1,1e5);
sq = isqrt(N); js = arange(1, 241); V = js*(2*sq+js) + (sq*sq - N)  (Fermat offsets);
rate(N) = fraction of the 240 offsets that are B-smooth (strip primes <= B);
B(u) = max(int(round(exp(ln(vmed)/u))), 50), vmed pooled per population;
T(N) = sum(2.0/q | q in primerange(3, 401), Legendre(N mod q, q) == +1);
Spearman via ordinal argsort (verbatim exp497).

DESIGN: 14 independent populations bitlen 44 (seeds 20260950..63), 1200 Ns each,
240 relation values; smoothness at u=3.5 AND u=2.5 paired per population.
Primary statistic: paired delta_k = sp_k(2.5) - sp_k(3.5).

PRE-STATED HYPOTHESES (written BEFORE any exp-500 data):
  H1 (center-below): the bal@3.5 population mean Spearman(T) over the 14 fresh seeds
                     lands below 0.60 - a genuine center shift.
  H2 (wide-tail):    the mean lands in [0.60, 0.65] with sd > 0.06 - center
                     acceptable, tail-driven breaches only.
  Verdict rule: H1 iff mean(sp35) < 0.60; elif mean(sp35) >= 0.60 and sd(sp35) > 0.06
                -> H2; else NEITHER.
  Reported: mean/median/sd of per-seed sp(3.5); paired delta mean +/- bootstrap CI
  (1000 resamples of the 14 deltas, rng seed 20260964); fraction of seeds below the
  band floor 0.60.

# BARRIERS (standard lines, verbatim exp499):
#   Barrier 5 (structural orthogonality): T is an N-only natural coordinate; the
#   dial predicts relation yield (difficulty), not (p,q) - no which-factor claim
#   made or tested.
#   Barrier 8 (known-method-in-disguise): the measured object is the QS/CFRAC
#   relation-yield dial - a cost predictor FOR known methods, not a new
#   factoring route.
"""
import json, time, math, datetime
import numpy as np
import gmpy2
from sympy import primerange, nextprime

BASE = 20260950
NSEED = 14
NN = 1200
T0 = time.time()
WORK = "/tmp/exp45_u35"
OUT = {"meta": {"base_seed": BASE, "exp": 500, "codename": "U35-LOCALIZE",
                "round": 45,
                "populations": [BASE + k for k in range(NSEED)],
                "Ns_per_population": NN, "offsets_per_N": 240,
                "us": [2.5, 3.5],
                "constructions": "verbatim exp497/exp499 bitlen-44 balanced arm",
                "prestated": {
                    "H1_center_below": "mean sp(3.5) over 14 seeds < 0.60",
                    "H2_wide_tail": "mean in [0.60,0.65] and sd > 0.06",
                    "rule": "H1 iff mean<0.60; elif mean>=0.60 and sd>0.06 -> H2; else NEITHER"}},
        "rows": []}

def ledger(event, **kw):
    rec = {"ts": datetime.datetime.now().isoformat(timespec="seconds"),
           "round": 45, "exp": 500, "codename": "U35-LOCALIZE",
           "event": event, "t_s": round(time.time() - T0, 1)}
    rec.update(kw)
    with open(f"{WORK}/ledger_exp500.jsonl", "a") as f:
        f.write(json.dumps(rec, default=float) + "\n")
    return rec

def checkpoint():
    json.dump(OUT, open(f"{WORK}/result.json", "w"), indent=1, default=float)

primes_all = np.array(list(primerange(2, 200000)), dtype=np.int64)

def smooth_mask(V, B):
    # verbatim exp497
    W = V.copy()
    for p in primes_all[primes_all <= B]:
        while True:
            m = W % p == 0
            if not m.any(): break
            W[m] //= p
            if not (W % p == 0).any(): break
    return W == 1

def spearman(a, b):
    # verbatim exp497 (ordinal argsort)
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])

LO = int(gmpy2.isqrt(1 << 43)) + 1
HI = int(gmpy2.isqrt((1 << 44) - 1))

def draw_balanced(rng):
    # verbatim exp499 draw_balanced (bitlen-44 window, gap U[1,1e5), stray reject redrawn)
    while True:
        r = int(rng.integers(LO, HI))
        p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, 10**5))))
        N = p * q
        if not ((1 << 43) <= N < (1 << 44)):
            continue
        sq = math.isqrt(N)
        js = np.arange(1, 241, dtype=np.int64)
        V = js * (2 * sq + js) + (sq * sq - N)
        if V.min() <= 0: continue
        return N, sq, V

wr = list(primerange(3, 401))

def t_dial(Ns):
    return np.array([sum(2.0/q for q in wr
                         if gmpy2.powmod(N % q, (q - 1) // 2, q) == 1)
                     for N in Ns], float)

ledger("start", base_seed=BASE, workdir=WORK, n_populations=NSEED, Ns_per_population=NN,
       constructions="verbatim exp497/exp499 bitlen-44 balanced arm",
       prestated=OUT["meta"]["prestated"])
checkpoint()

for k in range(NSEED):
    seed = BASE + k
    rng = np.random.default_rng(seed)
    data = [draw_balanced(rng) for _ in range(NN)]
    Ns = [d[0] for d in data]
    Vall = np.concatenate([d[2] for d in data])
    vmed = float(np.median(Vall.astype(float)))
    Ts = t_dial(Ns)
    row = {"seed": seed, "R2_base_seed": seed}
    for u, rkey in ((2.5, "sp25"), (3.5, "sp35")):
        B = max(int(round(math.exp(math.log(vmed) / u))), 50)
        sm = smooth_mask(Vall, B).reshape(len(data), 240)
        rate = sm.mean(axis=1)
        row[rkey] = spearman(Ts, rate)
        row["B" + rkey[2:]] = B
        row["mean_rate" + rkey[2:]] = float(rate.mean())
    row["delta"] = row["sp25"] - row["sp35"]
    row["vmed"] = round(vmed, 1)
    row["bitlen_range"] = [int(min(Ns).bit_length()), int(max(Ns).bit_length())]
    OUT["rows"].append(row)
    checkpoint()
    ledger("population_done", seed=seed, sp25=round(row["sp25"], 4),
           sp35=round(row["sp35"], 4), delta=round(row["delta"], 4),
           B25=row["B25"], B35=row["B35"],
           mean_rate25=round(row["mean_rate25"], 4),
           mean_rate35=round(row["mean_rate35"], 4))
    print(row["seed"], "sp25=%.4f sp35=%.4f delta=%+.4f" % (row["sp25"], row["sp35"], row["delta"]),
          "B25=%d B35=%d" % (row["B25"], row["B35"]),
          round(time.time() - T0, 1), "s", flush=True)

# ---- summary + verdict ----
sp25 = [r["sp25"] for r in OUT["rows"]]
sp35 = [r["sp35"] for r in OUT["rows"]]
deltas = [r["delta"] for r in OUT["rows"]]
mean = lambda x: sum(x) / len(x)
sd = lambda x: (sum((v - mean(x))**2 for v in x) / (len(x) - 1))**0.5
m35, sd35 = mean(sp35), sd(sp35)
boot = np.random.default_rng(20260964)
bs_delta = np.array([mean([deltas[i] for i in boot.integers(0, NSEED, NSEED)])
                     for _ in range(1000)])
bs_m35 = np.array([mean([sp35[i] for i in boot.integers(0, NSEED, NSEED)])
                   for _ in range(1000)])
ci = lambda a: [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]
frac_below = sum(1 for s in sp35 if s < 0.60) / NSEED
OUT["summary"] = {
    "sp35": {"mean": round(m35, 4), "median": round(float(np.median(sp35)), 4),
             "sd": round(sd35, 4), "SE_mean": round(sd35 / math.sqrt(NSEED), 4),
             "min": round(min(sp35), 4), "max": round(max(sp35), 4),
             "bootstrap_CI_mean": [round(v, 4) for v in ci(bs_m35)]},
    "sp25_anchor": {"mean": round(mean(sp25), 4), "sd": round(sd(sp25), 4),
                    "min": round(min(sp25), 4), "max": round(max(sp25), 4)},
    "paired_delta": {"mean": round(mean(deltas), 4),
                     "bootstrap_CI": [round(v, 4) for v in ci(bs_delta)]},
    "fraction_below_floor_0.60": round(frac_below, 4),
    "n_below_floor": int(frac_below * NSEED)}
h1 = m35 < 0.60
h2 = (not h1) and (m35 >= 0.60 and sd35 > 0.06)
name = "H1" if h1 else ("H2" if h2 else "NEITHER")
OUT["verdict"] = {"H1_center_below": bool(h1), "H2_wide_tail": bool(h2),
                  "verdict_name": name}
OUT["barrier_lines"] = {
    "barrier_5": "Structural orthogonality: T is an N-only natural coordinate; the "
                 "dial predicts relation yield (difficulty), not (p,q) - no "
                 "which-factor claim made or tested.",
    "barrier_8": "Known-method-in-disguise: the measured object is the QS/CFRAC "
                 "relation-yield dial - a cost predictor FOR known methods, not a "
                 "new factoring route."}
OUT["artifacts"] = [f"{WORK}/exp500_u35_localize.py", f"{WORK}/result.json",
                    f"{WORK}/ledger_exp500.jsonl"]
checkpoint()
headline = (f"U35-LOCALIZE exp500: VERDICT {name}; "
            f"sp35 mean={m35:.4f} median={float(np.median(sp35)):.4f} sd={sd35:.4f} "
            f"min={min(sp35):.4f} max={max(sp35):.4f}; below-floor {int(frac_below*NSEED)}/{NSEED}; "
            f"paired delta mean={mean(deltas):+.4f} CI=[{ci(bs_delta)[0]:+.4f},{ci(bs_delta)[1]:+.4f}]; "
            f"sp25 anchor mean={mean(sp25):.4f} sd={sd(sp25):.4f}")
ledger("DONE", seed=BASE, status="DONE", headline=headline, verdict=OUT["verdict"],
       summary=OUT["summary"], barriers=["5", "8"], artifacts=OUT["artifacts"])
print(json.dumps(OUT["summary"]))
print(json.dumps(OUT["verdict"]))
print(headline)
print("DONE", round(time.time() - T0, 1), "s")

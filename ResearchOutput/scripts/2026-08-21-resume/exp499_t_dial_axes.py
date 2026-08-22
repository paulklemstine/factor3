#!/usr/bin/env python3
"""EXP 499 T-DIAL-AXES lean (round-44). Base seed 20260940.
Paper 165 (exp497) showed the zero-fit dial T(N) = sum(2/p | QR primes p<=400) is
seed-stable (per-seed Spearman in [0.71, 0.76]) on BALANCED draws at u=2.5.
This experiment tests the two remaining validation axes:
  axis A (regime): UNIFORM-draw semiprimes, p uniform prime in [2^10, 2^16),
                   q uniform prime in [2^16, 2^22)  (heterogeneous sizes);
  axis B (u-sensitivity): smoothness threshold u = 3.5 instead of 2.5
                   (B = exp(ln vmed / u), strip to B), on BALANCED draws.

PRE-STATED HYPOTHESES (written BEFORE any data was generated):
  H1 (regime):        Spearman(T, rate) on UNIFORM draws stays within [0.60, 0.85]
                      at u=2.5, for every one of the 5 populations.
  H2 (u-sensitivity): Spearman(T, rate) at u=3.5 stays within [0.60, 0.85]
                      on BALANCED draws, for every one of the 5 populations.
  H3 (joint):         both axes hold simultaneously per population -- each of the
                      5 populations passes on both axes (its uni@2.5 cell AND its
                      bal@3.5 cell inside [0.60, 0.85]).

DESIGN: 5 independent populations, semiprime bitlen 44 (seeds 20260940..20260944).
Each population contributes TWO arms x 240 relations each:
  balanced arm: p,q near 2^21 with N forced to exact bitlen 44
                (factors drawn in [isqrt(2^43)+1, isqrt(2^44-1)], nextprime,
                 inter-prime gap uniform in [1, 10^5) -- exp497 construction,
                 window shifted so N has bitlen 44; any stray reject redrawn);
  uniform arm:  p = nextprime(uniform int in [2^10, 2^16)),
                q = nextprime(uniform int in [2^16, 2^22)).
Feature construction VERBATIM from exp497: sq = isqrt(N); js = arange(1, 241);
V = js*(2*sq+js) + (sq*sq - N)  (= (sq+j)^2 - N, the Fermat offset family);
rate(N) = fraction of the 240 offsets that are B-smooth (strip primes <= B);
T(N) = sum(2.0/q for q in primerange(3, 401) if Legendre(N mod q, q) == +1).
vmed computed per population x arm (pooled over that arm's 240x240 values);
B(u) = max(int(round(exp(ln(vmed)/u))), 50), u in {2.5, 3.5}.
Output grid: 5 populations x 4 cells {bal@2.5, bal@3.5, uni@2.5, uni@3.5} = 20 cells.
bal@2.5 is the paper-165 anchor (expect ~[0.71, 0.76]); uni@3.5 is exploratory context.

# BARRIERS (standard lines):
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

BASE = 20260940
T0 = time.time()
WORK = "/tmp/exp44_tax"
OUT = {"meta": {"base_seed": BASE, "exp": 499, "codename": "T-DIAL-AXES",
                "round": 44,
                "populations": [BASE + k for k in range(5)],
                "arms": {"balanced": "p,q near 2^21, N exact bitlen 44, gap U[1,1e5)",
                         "uniform": "p~U prime [2^10,2^16), q~U prime [2^16,2^22)"},
                "relations_per_arm": 240, "offsets_per_relation": 240,
                "us": [2.5, 3.5],
                "prestated": {
                    "H1": "uni@2.5 Spearman in [0.60,0.85] all 5 populations",
                    "H2": "bal@3.5 Spearman in [0.60,0.85] all 5 populations",
                    "H3": "each population passes BOTH axes simultaneously"}},
        "rows": []}

def ledger(event, **kw):
    rec = {"ts": datetime.datetime.now().isoformat(timespec="seconds"),
           "round": 44, "exp": 499, "codename": "T-DIAL-AXES",
           "event": event, "t_s": round(time.time() - T0, 1)}
    rec.update(kw)
    with open(f"{WORK}/ledger_exp499.jsonl", "a") as f:
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
    # verbatim exp497
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])

def draw_balanced(rng):
    """exp497 construction, window shifted so N has exact bitlen 44."""
    lo = int(gmpy2.isqrt(1 << 43)) + 1
    hi = int(gmpy2.isqrt((1 << 44) - 1))
    while True:
        r = int(rng.integers(lo, hi))
        p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, 10**5))))
        N = p * q
        if not ((1 << 43) <= N < (1 << 44)):
            continue
        sq = math.isqrt(N)
        js = np.arange(1, 241, dtype=np.int64)
        V = js * (2 * sq + js) + (sq * sq - N)
        if V.min() <= 0: continue
        return N, sq, V

def draw_uniform(rng):
    """p uniform prime in [2^10,2^16), q uniform prime in [2^16,2^22)."""
    while True:
        p = int(nextprime(int(rng.integers(1 << 10, 1 << 16))))
        q = int(nextprime(int(rng.integers(1 << 16, 1 << 22))))
        N = p * q
        sq = math.isqrt(N)
        js = np.arange(1, 241, dtype=np.int64)
        V = js * (2 * sq + js) + (sq * sq - N)
        if V.min() <= 0: continue
        return N, sq, V

wr = list(primerange(3, 401))

def t_dial(sq_list_or_Ns, Ns):
    return np.array([sum(2.0/q for q in wr
                         if gmpy2.powmod(N % q, (q - 1) // 2, q) == 1)
                     for N in Ns], float)

ledger("start", base_seed=BASE, workdir=WORK)
checkpoint()

for k in range(5):
    seed = BASE + k
    rng = np.random.default_rng(seed)
    arms = {}
    for arm, drawer in (("balanced", draw_balanced), ("uniform", draw_uniform)):
        data = [drawer(rng) for _ in range(240)]
        Ns = [d[0] for d in data]
        Vall = np.concatenate([d[2] for d in data])
        vmed = float(np.median(Vall.astype(float)))
        rates, Bs = {}, {}
        for u in (2.5, 3.5):
            B = max(int(round(math.exp(math.log(vmed) / u))), 50)
            sm = smooth_mask(Vall, B).reshape(len(data), 240)
            rates[u] = sm.mean(axis=1)
            Bs[u] = B
        arms[arm] = dict(Ns=Ns, vmed=vmed, B25=Bs[2.5], B35=Bs[3.5],
                         rate25=rates[2.5], rate35=rates[3.5])
    row = {"seed": seed, "R2_base_seed": seed, "cells": {}}
    for arm in ("balanced", "uniform"):
        Ts = t_dial(None, arms[arm]["Ns"])
        for u in (2.5, 3.5):
            rkey = "rate25" if u == 2.5 else "rate35"
            s = spearman(Ts, arms[arm][rkey])
            row["cells"][f"{arm}@u{u}"] = round(s, 4)
    row["arm_info"] = {arm: {"vmed": round(arms[arm]["vmed"], 1),
                             "B25": arms[arm]["B25"], "B35": arms[arm]["B35"],
                             "bitlen_range": [int(min(arms[arm]["Ns"]).bit_length()),
                                              int(max(arms[arm]["Ns"]).bit_length())]}
                       for arm in arms}
    OUT["rows"].append(row)
    checkpoint()
    ledger("population_done", seed=seed, cells=row["cells"], **row["arm_info"])
    print(row["seed"], row["cells"], round(time.time() - T0, 1), "s", flush=True)

# ---- summary + verdicts ----
cols = ["balanced@u2.5", "balanced@u3.5", "uniform@u2.5", "uniform@u3.5"]
grid = {c: [r["cells"][c] for r in OUT["rows"]] for c in cols}
INBAND = lambda s: 0.60 <= s <= 0.85
h1_cells = grid["uniform@u2.5"]; h2_cells = grid["balanced@u3.5"]
h1_ok = [INBAND(s) for s in h1_cells]; h2_ok = [INBAND(s) for s in h2_cells]
joint_ok = [a and b for a, b in zip(h1_ok, h2_ok)]
mean = lambda x: sum(x) / len(x)
sd = lambda x: (sum((v - mean(x))**2 for v in x) / (len(x) - 1))**0.5
OUT["summary"] = {
    "grid": grid,
    "col_stats": {c: {"mean": round(mean(grid[c]), 4), "min": min(grid[c]),
                      "max": max(grid[c]), "sd": round(sd(grid[c]), 4)} for c in cols},
    "anchor_paper165_band": [0.71, 0.76],
    "inband_counts": {"H1_uni25": sum(h1_ok), "H2_bal35": sum(h2_ok),
                      "H3_joint": sum(joint_ok)}}
OUT["verdict"] = {
    "H1_regime_uniform_in_band_all5": bool(all(h1_ok)),
    "H2_u_sensitivity_bal35_in_band_all5": bool(all(h2_ok)),
    "H3_joint_both_axes_each_population": bool(all(joint_ok)),
    "per_population_joint": {str(r["seed"]): bool(o) for r, o in zip(OUT["rows"], joint_ok)}}
OUT["barrier_lines"] = {
    "barrier_5": "Structural orthogonality: T is an N-only natural coordinate; the "
                 "dial predicts relation yield (difficulty), not (p,q) - no "
                 "which-factor claim made or tested.",
    "barrier_8": "Known-method-in-disguise: the measured object is the QS/CFRAC "
                 "relation-yield dial - a cost predictor FOR known methods, not a "
                 "new factoring route."}
OUT["artifacts"] = [f"{WORK}/exp499_t_dial_axes.py", f"{WORK}/result.json",
                    f"{WORK}/ledger_exp499.jsonl"]
checkpoint()
headline = (f"T-DIAL-AXES exp499: H1={'TRUE' if all(h1_ok) else 'REFUTED'} "
            f"H2={'TRUE' if all(h2_ok) else 'REFUTED'} "
            f"H3={'TRUE' if all(joint_ok) else 'REFUTED'}; "
            f"grid means bal@2.5={mean(grid['balanced@u2.5']):.4f} "
            f"bal@3.5={mean(grid['balanced@u3.5']):.4f} "
            f"uni@2.5={mean(grid['uniform@u2.5']):.4f} "
            f"uni@3.5={mean(grid['uniform@u3.5']):.4f}; "
            f"in-band {sum(h1_ok)}/5 uni@2.5, {sum(h2_ok)}/5 bal@3.5, "
            f"{sum(joint_ok)}/5 joint")
ledger("DONE", seed=BASE, status="DONE", headline=headline,
       verdicts=OUT["verdict"], barriers=["5", "8"], artifacts=OUT["artifacts"])
print(json.dumps(OUT["summary"]["col_stats"]))
print(json.dumps(OUT["verdict"]))
print(headline)
print("DONE", round(time.time() - T0, 1), "s")

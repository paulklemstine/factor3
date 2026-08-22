#!/usr/bin/env python3
"""EXP 501 U-HARDEN lean (round-45). Base seeds 20260970..20260977. Inline takeover.
Paper 167 (exp500): the zero-fit dial T(N) = sum(2/p | QR primes p<=400) loses
~0.106 Spearman UNIFORMLY when moving from u=2.5 to u=3.5 (paired, 14/14
populations). Paper 167 named two candidate drivers:
  (a) starved smooth-rate regime (~1.9% mean rate at u=3.5 - rank coarseness from
      fewer effective distinctions),
  (b) bound-coverage mismatch (B(3.5) ~ 356 < dial cap 400 - the dial undersamples
      the strip bound at tight u).
This experiment HARDENS against driver (a): give every N four times the relation
values and ask whether the paired drop survives.

Constructions VERBATIM from exp500/exp497/exp499 (/home/raver1975/factor3/
ResearchOutput/scripts/2026-08-21-resume/exp500_u35_localize.py): bitlen-44
balanced window [isqrt(2^43)+1, isqrt(2^44-1)) with exact-bitlen enforcement,
inter-prime gap U[1,1e5); sq = isqrt(N); js = arange(1, W+1);
V = js*(2*sq+js) + (sq*sq - N)  (Fermat offsets); positivity asserted;
rate(N) = fraction of the W offsets that are B-smooth (strip primes <= B);
B(u) = max(int(round(exp(ln(vmed)/u))), 50), vmed POOLED PER ARM (each arm's own
median v); T(N) = sum(2.0/q | q in primerange(3, 401), Legendre(N mod q, q) == +1)
computed ONCE per population (window-independent); Spearman via ordinal argsort
(verbatim exp497).

DESIGN: 8 independent populations bitlen 44 (seeds 20260970..77), 1200 Ns each;
TWO window arms per population, j=1..240 and j=1..960, SAME construction and SAME
Ns (nested windows: the 240-arm is the first 240 columns of the 960-arm);
smoothness at u=2.5 AND u=3.5 on both arms -> four (arm x u) cells per population.

PRE-STATED HYPOTHESES (written BEFORE any exp-501 data):
  H1 (starvation):   the paired drop Delta = sp(2.5) - sp(3.5) shrinks toward zero
                     when each N gets 960 relation values instead of 240 (rank
                     coarseness is sampling-driven; 4x values recover most of it).
  H2 (coverage):     the paired drop persists at ~0.11 even with 960 values - the
                     u-sensitivity is intrinsic to tighter thresholds reweighting
                     which primes matter, not a measurement artifact.
  Decision rule:     H1 iff Delta(960) < half of Delta(240);
                     H2 iff |Delta(960) - Delta(240)| < 0.03.
  Reported: four-cell table sp(arm,u); Delta(240) and Delta(960) means +/- bootstrap
  CI (500 resamples of the 8 populations, rng seed 20260978) on each mean and on the
  DIFFERENCE OF DIFFERENCES D = Delta(240) - Delta(960); mean rates per cell
  (starvation relief measured directly); verdict per rule (point estimates primary,
  CI as evidence; if both rules fire -> BOTH, neither -> NEITHER).

# BARRIERS (standard lines, verbatim exp500/exp499):
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

BASE = 20260970
NSEED = 8
NN = 1200
WINDOWS = (240, 960)
US = (2.5, 3.5)
BOOT_N = 500
BOOT_SEED = 20260978
T0 = time.time()
WORK = "/tmp/exp45_uharden"
OUT = {"meta": {"base_seed": BASE, "exp": 501, "codename": "U-HARDEN",
                "round": 45,
                "populations": [BASE + k for k in range(NSEED)],
                "Ns_per_population": NN, "windows": list(WINDOWS),
                "us": list(US), "boot_resamples": BOOT_N,
                "constructions": "verbatim exp497/exp499/exp500 bitlen-44 balanced arm, "
                                 "nested windows j=1..240 / j=1..960 on the same Ns, "
                                 "vmed pooled per ARM",
                "prestated": {
                    "H1_starvation": "Delta(960) < half of Delta(240)",
                    "H2_coverage": "|Delta(960) - Delta(240)| < 0.03",
                    "rule": "H1 iff Delta960 < Delta240/2; H2 iff |Delta960-Delta240|<0.03; "
                            "both->BOTH, neither->NEITHER"}},
        "rows": []}

def ledger(event, **kw):
    rec = {"ts": datetime.datetime.now().isoformat(timespec="seconds"),
           "round": 45, "exp": 501, "codename": "U-HARDEN",
           "event": event, "t_s": round(time.time() - T0, 1)}
    rec.update(kw)
    with open(f"{WORK}/ledger_exp501.jsonl", "a") as f:
        f.write(json.dumps(rec, default=float) + "\n")
    return rec

def checkpoint():
    json.dump(OUT, open(f"{WORK}/result.json", "w"), indent=1, default=float)

primes_all = np.array(list(primerange(2, 200000)), dtype=np.int64)

def smooth_mask(V, B):
    # verbatim exp497/exp500 (numpy trial division by strip primes, multiplicity aware)
    W = V.copy()
    for p in primes_all[primes_all <= B]:
        while True:
            m = W % p == 0
            if not m.any(): break
            W[m] //= p
            if not (W % p == 0).any(): break
    return W == 1

def spearman(a, b):
    # verbatim exp497/exp500 (ordinal argsort)
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])

LO = int(gmpy2.isqrt(1 << 43)) + 1
HI = int(gmpy2.isqrt((1 << 44) - 1))

def draw_one(rng):
    # verbatim exp499/exp500 draw_balanced (bitlen-44 window, gap U[1,1e5), redraws)
    while True:
        r = int(rng.integers(LO, HI))
        p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, 10**5))))
        N = p * q
        if not ((1 << 43) <= N < (1 << 44)):
            continue
        return N, math.isqrt(N)

def fermat_offsets(Ns, sqs, Wmax):
    # verbatim V = js*(2*sq+js) + (sq*sq - N), vectorized over Ns; nested arms
    js = np.arange(1, Wmax + 1, dtype=np.int64)
    sq = np.asarray(sqs, dtype=np.int64)[:, None]
    N = np.asarray(Ns, dtype=np.int64)[:, None]
    V = js[None, :] * (2 * sq + js[None, :]) + (sq * sq - N)
    assert (V > 0).all(), "positivity violated"
    return V

wr = list(primerange(3, 401))

def t_dial(Ns):
    # verbatim exp497/exp500 (window-independent, computed once per population)
    return np.array([sum(2.0/q for q in wr
                         if gmpy2.powmod(int(N) % q, (q - 1) // 2, q) == 1)
                     for N in Ns], float)

def arm_cell(V, vmed, u):
    B = max(int(round(math.exp(math.log(vmed) / u))), 50)
    sm = smooth_mask(V, B)
    return B, sm

import os
os.makedirs(WORK, exist_ok=True)

ledger("start", base_seed=BASE, workdir=WORK, n_populations=NSEED,
       Ns_per_population=NN, windows=list(WINDOWS), us=list(US),
       constructions=OUT["meta"]["constructions"],
       prestated=OUT["meta"]["prestated"])
checkpoint()

for k in range(NSEED):
    seed = BASE + k
    rng = np.random.default_rng(seed)
    pairs = [draw_one(rng) for _ in range(NN)]
    Ns = [d[0] for d in pairs]
    sqs = [d[1] for d in pairs]
    Ts = t_dial(Ns)
    Vfull = fermat_offsets(Ns, sqs, WINDOWS[1])
    row = {"seed": seed}
    for arm, W in (("a240", WINDOWS[0]), ("a960", WINDOWS[1])):
        V = Vfull[:, :W]
        Vf = V.astype(float)
        vmed = float(np.median(Vf))
        for u in US:
            B, sm = arm_cell(V, vmed, u)
            rate = sm.reshape(NN, W).mean(axis=1)
            row[f"sp_{arm}_{u}"] = spearman(Ts, rate)
            row[f"B_{arm}_{u}"] = B
            row[f"mean_rate_{arm}_{u}"] = float(rate.mean())
            row[f"zero_frac_{arm}_{u}"] = float((rate == 0).mean())
        row[f"vmed_{arm}"] = round(vmed, 1)
    row["delta240"] = row["sp_a240_2.5"] - row["sp_a240_3.5"]
    row["delta960"] = row["sp_a960_2.5"] - row["sp_a960_3.5"]
    row["D_diff_of_diff"] = row["delta240"] - row["delta960"]
    row["bitlen_range"] = [int(min(Ns).bit_length()), int(max(Ns).bit_length())]
    OUT["rows"].append(row)
    checkpoint()
    ledger("population_done", seed=seed,
           sp240_25=round(row["sp_a240_2.5"], 4), sp240_35=round(row["sp_a240_3.5"], 4),
           sp960_25=round(row["sp_a960_2.5"], 4), sp960_35=round(row["sp_a960_3.5"], 4),
           delta240=round(row["delta240"], 4), delta960=round(row["delta960"], 4),
           mean_rate_240_25=round(row["mean_rate_a240_2.5"], 4),
           mean_rate_240_35=round(row["mean_rate_a240_3.5"], 4),
           mean_rate_960_25=round(row["mean_rate_a960_2.5"], 4),
           mean_rate_960_35=round(row["mean_rate_a960_3.5"], 4))
    print(row["seed"],
          "d240=%+.4f d960=%+.4f D=%+.4f" % (row["delta240"], row["delta960"], row["D_diff_of_diff"]),
          "cells %.3f/%.3f/%.3f/%.3f" % (row["sp_a240_2.5"], row["sp_a240_3.5"],
                                         row["sp_a960_2.5"], row["sp_a960_3.5"]),
          "rates %.3f/%.3f/%.3f/%.3f" % (row["mean_rate_a240_2.5"], row["mean_rate_a240_3.5"],
                                         row["mean_rate_a960_2.5"], row["mean_rate_a960_3.5"]),
          round(time.time() - T0, 1), "s", flush=True)

# ---- summary + verdict ----
rows = OUT["rows"]
g = lambda key: [r[key] for r in rows]
mean = lambda x: sum(x) / len(x)
sd = lambda x: (sum((v - mean(x))**2 for v in x) / (len(x) - 1))**0.5
boot = np.random.default_rng(BOOT_SEED)
idx = lambda: boot.integers(0, NSEED, NSEED)
bs = {key: np.array([mean([r[key] for r in (rows[i] for i in idx())])
                     for _ in range(BOOT_N)])
      for key in ("delta240", "delta960", "D_diff_of_diff")}
ci = lambda a: [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]
m240, m960, mD = mean(g("delta240")), mean(g("delta960")), mean(g("D_diff_of_diff"))
OUT["summary"] = {
    "cells": {f"{a}_{u}": {"mean": round(mean(g(f"sp_{a}_{u}")), 4),
                           "sd": round(sd(g(f"sp_{a}_{u}")), 4)}
              for a in ("a240", "a960") for u in US},
    "delta240": {"mean": round(m240, 4), "sd": round(sd(g("delta240")), 4),
                 "bootstrap_CI": [round(v, 4) for v in ci(bs["delta240"])]},
    "delta960": {"mean": round(m960, 4), "sd": round(sd(g("delta960")), 4),
                 "bootstrap_CI": [round(v, 4) for v in ci(bs["delta960"])]},
    "difference_of_differences": {
        "mean_D_240_minus_960": round(mD, 4),
        "bootstrap_CI": [round(v, 4) for v in ci(bs["D_diff_of_diff"])],
        "CI_excludes_zero": bool(ci(bs["D_diff_of_diff"])[0] > 0 or ci(bs["D_diff_of_diff"])[1] < 0)},
    "mean_rates": {f"{a}_{u}": round(mean(g(f"mean_rate_{a}_{u}")), 4)
                   for a in ("a240", "a960") for u in US},
    "bounds": {f"{a}_{u}": [r[f"B_{a}_{u}"] for r in rows]
               for a in ("a240", "a960") for u in US}}
h1 = bool(m960 < 0.5 * m240)
h2 = bool(abs(m960 - m240) < 0.03)
name = "H1" if (h1 and not h2) else ("H2" if (h2 and not h1) else ("BOTH" if h1 else "NEITHER"))
OUT["verdict"] = {"H1_starvation": h1, "H2_coverage": h2, "verdict_name": name,
                  "rule_detail": {"Delta240_mean": round(m240, 4),
                                  "Delta960_mean": round(m960, 4),
                                  "half_of_Delta240": round(0.5 * m240, 4),
                                  "abs_change": round(abs(m960 - m240), 4)}}
OUT["barrier_lines"] = {
    "barrier_5": "Structural orthogonality: T is an N-only natural coordinate; the "
                 "dial predicts relation yield (difficulty), not (p,q) - no "
                 "which-factor claim made or tested.",
    "barrier_8": "Known-method-in-disguise: the measured object is the QS/CFRAC "
                 "relation-yield dial - a cost predictor FOR known methods, not a "
                 "new factoring route."}
OUT["artifacts"] = [f"{WORK}/exp501_u_harden.py", f"{WORK}/result.json",
                    f"{WORK}/ledger_exp501.jsonl"]
checkpoint()
headline = (f"U-HARDEN exp501: VERDICT {name}; "
            f"d240 mean={m240:+.4f} CI=[{ci(bs['delta240'])[0]:+.4f},{ci(bs['delta240'])[1]:+.4f}]; "
            f"d960 mean={m960:+.4f} CI=[{ci(bs['delta960'])[0]:+.4f},{ci(bs['delta960'])[1]:+.4f}]; "
            f"D(d240-d960) mean={mD:+.4f} CI=[{ci(bs['D_diff_of_diff'])[0]:+.4f},{ci(bs['D_diff_of_diff'])[1]:+.4f}]")
ledger("DONE", seed=BASE, status="DONE", headline=headline, verdict=OUT["verdict"],
       summary=OUT["summary"], barriers=["5", "8"], artifacts=OUT["artifacts"])
print(json.dumps(OUT["summary"]["cells"]))
print(json.dumps(OUT["verdict"]))
print(headline)
print("DONE", round(time.time() - T0, 1), "s")

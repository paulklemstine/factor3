#!/usr/bin/env python3
# =====================================================================
# EXP-510  T-DIAL-UNIF-HB   (round-48, experiment 510)
# Zero-fit dial T(N) = sum 2/p over odd QR primes p <= 400:
# does the dial track relation rate on UNIFORM draws at HIGHER bitlens?
# Context: paper 175 (T is bitlen-stable on BALANCED draws),
#          paper 166 (uniform-regime invariance at bitlen 44).
# OPEN cell: the intersection -- uniform x {44, 48}.
#
# PRE-REGISTERED HYPOTHESES (written BEFORE any data generation):
#  H1: Spearman(T, rate) on UNIFORM draws stays within [0.55, 0.85]
#      at both bitlens (cells uniform-44 and uniform-48).
#  H2: T beats the bare QR-count (Spearman diff > +0.05) on >= 4/6 cells.
#      NOTE, locked before data: this design has FOUR cells
#      ({balanced, uniform} x {44, 48}), not six; the "4/6" in the brief
#      appears copy-carried from a larger template. Literal reading with
#      only 4 cells available: pass requires 4/4. We report both the
#      literal verdict and the win count.
#
# DESIGN DECISIONS LOCKED BEFORE DATA (ambiguity resolutions):
#  D1: Uniform-arm windows. The literal brief windows p in [2^10,2^16),
#      q in [2^16,2^22) give products of bitlen <= 38 -- infeasible for a
#      bitlen-44 cell (every draw would be rejected). Locked resolution:
#      keep the brief's p-side window width (6 exponents) and make q
#      complementary so the product lands at the cell bitlen:
#        k=44: e_p ~ U{10..15}, p in [2^e_p, 2^(e_p+1)), e_q = 43 - e_p;
#        k=48: e_p ~ U{12..17} (brief says "adjusted for k=48"; we shift
#              the whole window +2 to preserve the imbalance structure),
#              e_q = 47 - e_p.
#      N accepted only if bitlen(N) == k exactly (rejection sampling).
#  D2: rate definition (original pass): fraction of 240 CFRAC-style
#      candidate relation values v that are B-smooth, B = 400.
#  D3: T(N) uses Euler criterion powmod(N mod p, (p-1)//2, p) == 1 over
#      ODD primes p <= 400 (p | N gives symbol 0 -> excluded).
#      Comparator count(N) = number of odd primes p <= 100 with symbol 1.
#  D4: Seeds 20261020..20261023 map one-to-one to cells in fixed order
#      [(balanced,44),(uniform,44),(balanced,48),(uniform,48)].
#  D5: Balanced arm: p,q independent primes in [2^(k/2-1), 2^(k/2)),
#      redrawn if equal, N rejected unless bitlen == k.
#  D6: Smoothness test: trial division by primes <= 400 with early break
#      when p*p > remaining (remaining then is 1 or a prime; smooth iff
#      it is <= 400). gcd(v, N) > 1 cases simply fail the smoothness test;
#      no factor use anywhere inside measurement -- oracle primes are
#      used ONLY to construct N.
#
# PROTOCOL AMENDMENT D7 (post-pilot, BEFORE corrected data was generated):
#   A first pass ("pilot", preserved verbatim in result_pilot_krandom.json)
#   drew relation values with RANDOM multipliers k ~ U{1..64} per trial.
#   It produced Spearman(T,rate) ~ 0 in ALL FOUR cells -- including
#   balanced_44, where paper 175's protocol shows strong signal -- so the
#   pilot's rate definition was destroying the measured channel, not the
#   dial failing. Mechanism: v = a^2 - kN can only be divisible by primes
#   p with (kN/p) = 1; averaging over k equidistributes the characters
#   (for each p, ~half the ks open p for EVERY N), so the N-dependence of
#   the effective factor base cancels to first order and only small-p
#   residue-count fluctuations remain. AMENDED DESIGN: fixed multiplier
#   k = 1, pure CFRAC ladder v_j = (floor(sqrt N)+j)^2 - N, j = 1..240 --
#   the same 240 offsets for every N; then the available factor base is
#   exactly {p <= 400 : (N/p) = 1} and T(N) is the governing dial.
#   Pre-registered H1/H2 are UNCHANGED and are evaluated on the amended
#   run; the pilot is retained as a reported finding (K-WASHOUT).
#
# INCIDENT NOTE: mid-run, this file was overwritten from outside this
#   session by an incompatible implementation (pre-def NameError, an
#   infinite uniform-arm draw loop at bitlen 48 due to the infeasible
#   literal windows, 600/arm single-seed population, altered H2). It was
#   NOT executed; this restored script is the pre-registered design.
#   Logged in ledger.md.
#
# Barriers appended as standard lines (5)/(8). Ledger mandatory.
# Runtime target <= 15 min. Work confined to /tmp/exp48_tuhb/.
# =====================================================================

import json, random, time, sys, os
import gmpy2

WORK = "/tmp/exp48_tuhb"
RESULT = WORK + "/result.json"
LEDGER = WORK + "/ledger.md"

SEEDS = [20261020, 20261021, 20261022, 20261023]
CELLS = [("balanced", 44), ("uniform", 44), ("balanced", 48), ("uniform", 48)]
N_PER_CELL = 1200
N_VALUES = 240          # candidate relation values per N (k=1 ladder)
B_SMOOTH = 400          # smoothness bound (= dial bound)
U_ANCHOR = 2.5

t_start = time.time()

def ledger_write(line):
    stamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    el = time.time() - t_start
    with open(LEDGER, "a") as f:
        f.write(f"[{stamp} +{el:7.1f}s] {line}\n")

def checkpoint(state):
    state["elapsed_s"] = round(time.time() - t_start, 1)
    tmp = RESULT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=1)
    os.replace(tmp, RESULT)

def sieve_primes(n):
    s = bytearray([1]) * (n + 1)
    s[0:2] = b"\x00\x00"
    i = 2
    while i * i <= n:
        if s[i]:
            s[i*i::i] = b"\x00" * len(s[i*i::i])
        i += 1
    return [i for i in range(n + 1) if s[i]]

PRIMES_ALL = sieve_primes(B_SMOOTH)
ODD_PRIMES_400 = [p for p in PRIMES_ALL if p > 2]           # T dial
ODD_PRIMES_100 = [p for p in PRIMES_ALL if 2 < p <= 100]    # bare count
T_WEIGHTS = [2.0 / p for p in ODD_PRIMES_400]

def is_b_smooth(v):
    # trial division by primes <= 400, early break at p*p > v
    for p in PRIMES_ALL:
        pp = p * p
        if pp > v:
            return v <= B_SMOOTH   # remainder is 1 or a prime > all tried
        while v % p == 0:
            v //= p
            if v == 1:
                return True
    return v == 1

def legendre_is_1(N, p):
    return gmpy2.powmod(N % p, (p - 1) // 2, p) == 1

def dial_values(N):
    t = 0.0
    cnt = 0
    for i, p in enumerate(ODD_PRIMES_400):
        if legendre_is_1(N, p):
            t += T_WEIGHTS[i]
            if p <= 100:
                cnt += 1
    return t, cnt

def prime_in_range(rng, lo, hi):
    while True:
        c = rng.randrange(lo, hi)
        c |= 1
        p = int(gmpy2.next_prime(c))
        if p < hi:
            return p

def draw_semiprime(rng, arm, k):
    if arm == "balanced":
        h = k // 2
        lo, hi = 2 ** (h - 1), 2 ** h
        while True:
            p = prime_in_range(rng, lo, hi)
            q = prime_in_range(rng, lo, hi)
            if p == q:
                continue
            N = p * q
            if N.bit_length() == k:
                return int(p), int(q), int(N)
    else:  # uniform, per D1
        e_lo = 10 if k == 44 else 12
        e_hi = e_lo + 5               # inclusive exponent bin top
        while True:
            e1 = rng.randint(e_lo, e_hi)
            p = prime_in_range(rng, 2 ** e1, 2 ** (e1 + 1))
            e2 = (k - 1) - e1
            q = prime_in_range(rng, 2 ** e2, 2 ** (e2 + 1))
            N = p * q
            if N.bit_length() == k:
                return int(p), int(q), int(N)

def spearman(x, y):
    def ranks(a):
        order = sorted(range(len(a)), key=lambda i: a[i])
        r = [0.0] * len(a)
        i = 0
        n = len(a)
        while i < n:
            j = i
            ai = a[order[i]]
            while j + 1 < n and a[order[j + 1]] == ai:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for t in range(i, j + 1):
                r[order[t]] = avg
            i = j + 1
        return r
    rx, ry = ranks(x), ranks(y)
    n = len(rx)
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    return num / (dx * dy) if dx > 0 and dy > 0 else float("nan")

state = {
    "experiment": 510,
    "codename": "T-DIAL-UNIF-HB",
    "round": 48,
    "date": time.strftime("%Y-%m-%d"),
    "seeds": SEEDS,
    "preregistered": {
        "H1": "Spearman(T, rate) on uniform draws stays within [0.55, 0.85] at both bitlens.",
        "H2": "T beats bare QR-count by > +0.05 on >= 4/6 cells (design note: only 4 cells exist; literal pass needs 4/4).",
    },
    "design_decisions": ["see script header D1-D7"],
    "config": {
        "n_per_cell": N_PER_CELL, "n_relation_values": N_VALUES,
        "multiplier": "fixed k=1 CFRAC ladder (amendment D7)",
        "smoothness_bound": B_SMOOTH,
        "dial_bound": 400, "count_bound": 100, "u_anchor": U_ANCHOR,
    },
    "pilot_krandom": {
        "artifact": "/tmp/exp48_tuhb/result_pilot_krandom.json",
        "finding": ("K-WASHOUT: with k ~ U{1..64} per trial, Spearman(T,rate) ~ 0 in all "
                    "four cells (balanced_44 -0.011, uniform_44 -0.012, balanced_48 +0.064, "
                    "uniform_48 +0.042) including the arm where prior work shows strong "
                    "signal; multiplier randomization equidistributes the per-prime gate "
                    "(kN/p)=1 over k and cancels the N-dependence of the effective factor base."),
    },
    "cells": {},
}
with open(LEDGER, "a") as f:
    f.write(f"# EXP-510 T-DIAL-UNIF-HB ledger — amended run started {time.strftime('%Y-%m-%dT%H:%M:%S')}\n")
ledger_write("STAGE init: primes sieved (%d primes <= 400, %d odd <= 100); "
             "INCIDENT logged: foreign overwrite of exp510_t_dial_unif_hb.py detected "
             "(broken impl, never executed); pre-registered script restored"
             % (len(PRIMES_ALL), len(ODD_PRIMES_100)))
checkpoint(state)
print("init done", flush=True)

for seed, (arm, k) in zip(SEEDS, CELLS):
    cname = f"{arm}_{k}"
    rng = random.Random(seed)
    Ts, CNTs, RATEs, VSIZES = [], [], [], []
    pb_sum = qb_sum = 0
    for idx in range(N_PER_CELL):
        p, q, N = draw_semiprime(rng, arm, k)
        pb_sum += p.bit_length(); qb_sum += q.bit_length()
        T, cnt = dial_values(N)
        s = gmpy2.isqrt(N)
        smooth = 0
        for j in range(1, N_VALUES + 1):
            a = s + j
            v = int(a * a - N)          # > 0 always: a > sqrt(N)
            if is_b_smooth(v):
                smooth += 1
            if idx == 0 and j <= 5:
                VSIZES.append(int(v).bit_length())
        Ts.append(T); CNTs.append(cnt); RATEs.append(smooth / N_VALUES)
        if (idx + 1) % 300 == 0:
            print(f"{cname}: {idx+1}/{N_PER_CELL}  elapsed={time.time()-t_start:.0f}s", flush=True)
    sp_T = spearman(Ts, RATEs)
    sp_cnt = spearman(CNTs, RATEs)
    sp_T_cnt = spearman(Ts, CNTs)
    brng = random.Random(seed ^ 0xB007)
    n = len(Ts)
    deltas = []
    idxs = list(range(n))
    for _ in range(500):
        samp = [idxs[brng.randrange(n)] for _ in range(n)]
        d = spearman([Ts[i] for i in samp], [RATEs[i] for i in samp]) - \
            spearman([CNTs[i] for i in samp], [RATEs[i] for i in samp])
        deltas.append(d)
    deltas.sort()
    ci_lo, ci_hi = deltas[12], deltas[487]
    cell_res = {
        "seed": seed,
        "n": n,
        "mean_T": round(sum(Ts) / n, 4),
        "sd_T": round((sum((t - sum(Ts)/n)**2 for t in Ts) / n) ** 0.5, 4),
        "mean_count100": round(sum(CNTs) / n, 3),
        "mean_rate": round(sum(RATEs) / n, 4),
        "sd_rate": round((sum((r - sum(RATEs)/n)**2 for r in RATEs) / n) ** 0.5, 4),
        "frac_rate_positive": round(sum(1 for r in RATEs if r > 0) / n, 4),
        "first_v_bits_sample": VSIZES[:5],
        "spearman_T": round(sp_T, 4),
        "spearman_count": round(sp_cnt, 4),
        "delta_TC": round(sp_T - sp_cnt, 4),
        "delta_boot95CI": [round(ci_lo, 4), round(ci_hi, 4)],
        "spearman_T_vs_count": round(sp_T_cnt, 4),
        "mean_p_bits": round(pb_sum / n, 2),
        "mean_q_bits": round(qb_sum / n, 2),
    }
    state["cells"][cname] = cell_res
    ledger_write(f"STAGE cell-done {cname}: sp_T={sp_T:.4f} sp_cnt={sp_cnt:.4f} "
                 f"delta={sp_T-sp_cnt:+.4f} CI[{ci_lo:.3f},{ci_hi:.3f}] "
                 f"mean_rate={cell_res['mean_rate']:.4f}")
    checkpoint(state)
    print(f"CELL DONE {cname}: {json.dumps(cell_res)}", flush=True)

# ---------------- analysis & verdicts ----------------
wins = []
for cname, c in state["cells"].items():
    wins.append(c["delta_TC"] > 0.05)
h1_cells = {}
for cname in ("uniform_44", "uniform_48"):
    v = state["cells"][cname]["spearman_T"]
    h1_cells[cname] = {"value": v, "in_band": bool(0.55 <= v <= 0.85)}
h1_pass = all(h["in_band"] for h in h1_cells.values())
win_count = sum(wins)
h2_literal = bool(win_count >= 4)     # 4 cells exist -> need all 4
if h1_pass and h2_literal:
    verdict_name = "DIAL-HOLDS-UNIFORM-HB"
elif h1_pass:
    verdict_name = "H1-PASS-H2-SPLIT"
elif h2_literal:
    verdict_name = "H1-BREAK-H2-PASS"
else:
    lows = [c for c, h in h1_cells.items() if h["value"] < 0.55]
    highs = [c for c, h in h1_cells.items() if h["value"] > 0.85]
    if lows:
        verdict_name = "DIAL-COLLAPSE-UNIFORM" if any(
            abs(h["value"]) < 0.15 for c, h in h1_cells.items()) else \
            "DIAL-DEGRADES-UNIFORM-HIGHBITLEN"
    elif highs:
        verdict_name = "DIAL-TIGHTENS"
    else:
        verdict_name = "MIXED"

state["analysis"] = {
    "h1_per_cell": h1_cells,
    "h1_pass": h1_pass,
    "h2_win_cells": {c: bool(w) for c, w in zip(state["cells"], wins)},
    "h2_win_count": win_count,
    "h2_literal_pass_4of4": h2_literal,
    "verdict_name": verdict_name,
}
state["barriers"] = [
    "(5) WHICH-FACTOR WALL: T(N), QR-count(N) and relation-rate(N) are symmetric "
    "functions of the composite alone -- every channel reported here is which-factor "
    "blind; nothing in this experiment reads which factor, consistent with the wall.",
    "(8) TOY-SCOPE: all measurements at bitlen 44/48; oracle primes were used only to "
    "CONSTRUCT the semiprimes, never inside measurement (T and count computed from "
    "public N via Legendre symbols); no scaling claim beyond the tested regime.",
]
state["runtime_s"] = round(time.time() - t_start, 1)
ledger_write(f"STAGE analysis: H1={'PASS' if h1_pass else 'FAIL'} "
             f"(uniform cells {[(c, round(h['value'],4)) for c,h in h1_cells.items()]}) ; "
             f"H2 wins={win_count}/4 (literal {'PASS' if h2_literal else 'FAIL'}) ; "
             f"VERDICT={verdict_name}")
checkpoint(state)
print("FINAL:", verdict_name, flush=True)
print(json.dumps(state["analysis"], indent=1), flush=True)

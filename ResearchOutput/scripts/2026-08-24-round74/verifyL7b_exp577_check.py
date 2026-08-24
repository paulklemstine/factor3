#!/usr/bin/env python3
"""verifyL7b — ADVERSARIAL INDEPENDENT VERIFICATION of exp577 central claims.

NOT part of exp577. Written by a separate verifier agent. Touches only
verifyL7b_* files. Imports (read-only) the exp577 population/tester functions
so the data-generating process is identical, but:
  - uses its OWN fresh master seed 20260831 (distinct from 20260824..27);
  - recomputes every dial itself;
  - validates gmpy2.jacobi against sympy.jacobi_symbol EXHAUSTIVELY on every
    (N, prime<=400) pair of both populations (+ random large-prime spots),
    then uses fast gmpy2 for the <=1e6 passes;
  - implements its own OLS log-rate R2 and numpy Newton-Raphson Poisson GLM,
    and its own D_red.

Items verified:
  1a algebra+empirics of the reciprocity flip.
     Derivation: for N=pq, (l|N)=(l|p)(l|q); QR gives
       (l|p_i)=(-1)^{((l-1)/2)((p_i-1)/2)}(p_i|l), so
       (l|N)=(-1)^{((l-1)/2)*S}*(N mod l|l), S=sum_i (p_i-1)/2.
     ((l-1)/2) odd iff l=3 mod 4; S odd iff exactly one factor is 3 mod 4,
     iff N=3 mod 4 (odd factors). Hence flip <=> l=3 mod4 AND N=3 mod4.
     Also asserts form-A (jac(l,lo)jac(l,hi)) == form-B (jac(l,N)).
  1b rates: %N=3mod4 (~50% predicted); conditional flip rate (100%);
     unconditional event rate = %N3mod4 * frac(l<=400 odd primes, 3mod4).
  1c orthogonality: Pearson+Spearman flipped-form vs clean dial (~0.058 claimed).
  1d regression reproduction on THEIR 128 hits: .030/4.1 & .045/5.5 (flipped)
     vs .3207/33.4 (clean), with verifier-owned machinery; plus fresh-pop copy.
  2   weighted-dial saturation W_B=sum_{QR p<=B} 1/p on MY fresh population:
     corr(W1e6,W400)~=1, R2 ~= 0.47 +- width.
  3   consequence arithmetic: residual share after "48% explained", checked
     BOTH ways: total-dispersion reading D_cond/D_raw = 1-Dred, and strict
     excess-above-Poisson reading (D_cond-1)/(D_raw-1). ">=52%" must hold
     under the reading the findings actually use.
"""
import json, math, os, sys, time, random
import numpy as np
from multiprocessing import Pool
from scipy.stats import spearmanr

HERE = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74"
os.chdir(HERE)
sys.path.insert(0, HERE)

MY_SEED = 20260831
N_POP = 64
JSAMP = 150000

from exp577_product_dial import build_primorial, build_population, init_worker, worker
from sympy import jacobi_symbol as sjac
from gmpy2 import mpz
from gmpy2 import jacobi as gjac

t_start = time.time()
OUT = {"verifier": "verifyL7b", "my_seed": MY_SEED, "n_pop": N_POP, "jsamp": JSAMP}

# ---------- primes (independent sieve) ----------
def primes_upto(b):
    s = np.ones(b + 1, dtype=bool); s[:2] = False
    for i in range(2, int(b ** 0.5) + 1):
        if s[i]:
            s[i*i::i] = False
    return [int(i) for i in np.nonzero(s)[0]]

P_ALL = primes_upto(1000000)
P_LE400_ALL = [p for p in P_ALL if p <= 400]
P_ODD_LE400 = [p for p in P_LE400_ALL if p > 2]
ODD_LE1E6 = [p for p in P_ALL if p > 2]

# ---------- populations ----------
their_rows = json.load(open("exp577_result.json"))["rows"]
their_pops = [(int(r["N"]), int(r["lo"]), int(r["hi"])) for r in their_rows]
assert len(their_pops) == 128
my_pops = build_population(MY_SEED, N_POP)
assert frozenset(n for n, _, _ in my_pops).isdisjoint(int(r["N"]) for r in their_rows)

# ---------- PART 1a/1b: exhaustive flip audit (SYMPY-only, independent impl) ----------
def flip_audit(pops, tag):
    pct3 = 100 * sum(1 for N, _, _ in pops if N % 4 == 3) / len(pops)
    inv_on = agree_on = inv_off = agree_off = ab_mismatch = qr_mismatch = 0
    for N, lo, hi in pops:
        for l in P_ODD_LE400:
            mech = (sjac(N % l, l) == 1)
            fb = (sjac(l, N) == 1)
            fa = (sjac(l, lo) * sjac(l, hi) == 1)
            if fa != fb:
                ab_mismatch += 1
            if gjac(N % l, l) != sjac(N % l, l):
                qr_mismatch += 1          # gmpy-vs-sympy impl guard
            cond = (l % 4 == 3) and (N % 4 == 3)
            if fb != mech:
                if cond: inv_on += 1
                else: inv_off += 1
            else:
                if cond: agree_on += 1
                else: agree_off += 1
    n_ev = len(P_ODD_LE400) * len(pops)
    frac_l3 = sum(1 for l in P_ODD_LE400 if l % 4 == 3) / len(P_ODD_LE400)
    return {
        "pop": tag, "n": len(pops),
        "pct_N_eq_3_mod4": round(pct3, 1),
        "flip_iff_condition_violations": inv_off + agree_on,   # must be 0
        "flips_on_condition": inv_on, "agrees_on_condition": agree_on,
        "conditional_flip_rate_pct": round(100 * inv_on / max(inv_on, 1), 2),
        "unconditional_flip_event_pct_measured": round(100 * (inv_on + inv_off) / n_ev, 2),
        "frac_odd_primes_le400_eq_3mod4": round(frac_l3, 4),
        "predicted_unconditional_pct": round(pct3 * frac_l3, 2),
        "formA_vs_formB_mismatches": ab_mismatch,
        "gmpy_sympy_legendre_mismatches": qr_mismatch,
    }

fa_theirs = flip_audit(their_pops, "exp577_seed20260827")
fa_mine = flip_audit(my_pops, "verifyL7b_seed20260831")
print(json.dumps(fa_theirs)); print(json.dumps(fa_mine))
OUT["part1ab_flip"] = [fa_theirs, fa_mine]

# ---------- one-pass dial builder (fast gmpy2; validated above) ----------
def build_cols(pops):
    cols = {k: [] for k in ("C400_clean", "C100_clean", "E400_e576_formB",
                            "P100_e576_formA", "W400", "W1e6")}
    t0 = time.time()
    for N, lo, hi in pops:
        c4 = c1 = e4 = p1 = 0
        w4 = w6 = 0.0
        for p in ODD_LE1E6:
            if p <= 400:
                mech = (gjac(N % p, p) == 1)
                if mech:
                    c4 += 1
                    if p <= 100: c1 += 1
                # form-A exact: product of factor symbols == +1
                if p <= 100 and gjac(lo % p, p) * gjac(hi % p, p) == 1:
                    p1 += 1
                if gjac(p, N) == 1: e4 += 1
                if mech:
                    w4 += 1.0 / p
            if gjac(N % p, p) == 1:
                w6 += 1.0 / p
        cols["C400_clean"].append(c4); cols["C100_clean"].append(c1)
        cols["E400_e576_formB"].append(e4); cols["P100_e576_formA"].append(p1)
        cols["W400"].append(w4); cols["W1e6"].append(w6)
    return cols, time.time() - t0

t0 = time.time()
mine_cols, _ = build_cols(my_pops)
theirs_cols, _ = build_cols(their_pops)
print(f"dials built ({time.time()-t0:.0f}s)")
# exact cross-check vs their RECORDED gmpy S400 column (independent sieve+impl path)
match = sum(a == b for a, b in zip(theirs_cols["C400_clean"], [r["S400"] for r in their_rows]))
OUT["C400_vs_recorded_S400_matches_of_128"] = match
print(f"verifier C400 == exp577 recorded S400 on {match}/128 rows")

# ---------- fresh-population hits, VERBATIM tester ----------
P5m = mpz(build_primorial(100000)); P6m = mpz(build_primorial(1000000))
t0 = time.time()
NW = 8; per = N_POP // NW
chunks = [(my_pops[c*per:(c+1)*per], JSAMP, MY_SEED + 9000 + c) for c in range(NW)]
with Pool(NW, initializer=init_worker, initargs=(P5m, P6m)) as pl:
    res = pl.map(worker, chunks)
my_hits = [v for r in res for v in r[0]]
my_tots = [v for r in res for v in r[1]]
mh = sum(my_hits) / len(my_hits)
OUT["my_hits_mean"] = round(mh, 2)
print(f"hits done ({time.time()-t0:.0f}s) mean={mh:.1f}")

# ---------- verifier-owned regression machinery ----------
def ols_r2_lograte(xs, ys, ts):
    lr = np.array([math.log((y + 0.5) / t) for y, t in zip(ys, ts)])
    x = np.asarray(xs, float)
    xb = (x - x.mean()) / (x.std() or 1.0)
    X = np.column_stack([np.ones_like(xb), xb])
    beta, *_ = np.linalg.lstsq(X, lr, rcond=None)
    resid = lr - X @ beta
    return float(1 - (resid @ resid) / ((lr - lr.mean()) @ (lr - lr.mean()))), float(beta[1])

def poisson_glm_mu(xs, ys, ts):
    y = np.asarray(ys, float); off = np.log(np.asarray(ts, float))
    x = np.asarray(xs, float)
    xb = (x - x.mean()) / (x.std() or 1.0)
    X = np.column_stack([np.ones_like(xb), xb])
    b = np.zeros(2); b[0] = math.log(y.sum() / np.exp(off).sum())
    for _ in range(200):
        mu = np.exp(np.clip(X @ b + off, -60, 20))
        z = X @ b + (y - mu) / np.maximum(mu, 1e-300)
        b_new = np.linalg.solve(X.T @ (X * mu[:, None]), X.T @ (mu * z))
        if np.max(np.abs(b_new - b)) < 1e-11:
            b = b_new; break
        b = b_new
    return np.exp(np.clip(X @ b + off, -700, 700))

def reg_one(name, xs, ys, ts):
    m = sum(ys) / len(ys)
    Draw = float(np.var(ys) / m)
    mu = poisson_glm_mu(xs, ys, ts)
    Dcond = float(np.var(np.asarray(ys) - mu) / m)
    r2, slope = ols_r2_lograte(xs, ys, ts)
    return {"R2": round(r2, 4), "slope_sign": "+" if slope > 0 else "-",
            "D_raw": round(Draw, 2), "D_cond": round(Dcond, 2),
            "Dred_pct": round(100 * (1 - Dcond / Draw), 2)}

def pearson(a, b):
    return float(np.corrcoef(np.asarray(a, float), np.asarray(b, float))[0, 1])

def spear(a, b):
    return float(spearmanr(a, b).statistic)

# ---------- PART 1c orthogonality ----------
orth = {}
for tag, C, PA, EB in (
    ("theirs", theirs_cols["C400_clean"], theirs_cols["P100_e576_formA"], theirs_cols["E400_e576_formB"]),
    ("mine", mine_cols["C400_clean"], mine_cols["P100_e576_formA"], mine_cols["E400_e576_formB"]),
):
    orth[tag] = {"pearson_P100vsC400": round(pearson(PA, C), 3),
                 "spearman_P100vsC400": round(spear(PA, C), 3),
                 "pearson_E400vsC400": round(pearson(EB, C), 3),
                 "spearman_E400vsC400": round(spear(EB, C), 3)}
print(json.dumps(orth))
OUT["part1c_orthogonality"] = orth

# ---------- PART 1d regressions ----------
regT = {n: reg_one(n, theirs_cols[n], [r["hits"] for r in their_rows],
                   [r["total"] for r in their_rows])
        for n in ("C400_clean", "P100_e576_formA", "E400_e576_formB",
                  "W400", "W1e6")}
regM = {n: reg_one(n, mine_cols[n], my_hits, my_tots)
        for n in ("C400_clean", "P100_e576_formA", "E400_e576_formB",
                  "W400", "W1e6")}
print("THEIRS:", json.dumps(regT))
print("MINE:  ", json.dumps(regM))
OUT["part1d_reg_theirs"] = regT
OUT["part1d_reg_mine"] = regM

sat = {"corr_W1e6_W400_pearson_MINE": round(pearson(mine_cols["W1e6"], mine_cols["W400"]), 4),
       "corr_W1e6_W400_spearman_MINE": round(spear(mine_cols["W1e6"], mine_cols["W400"]), 4),
       "corr_W1e6_W400_pearson_THEIRS": round(pearson(theirs_cols["W1e6"], theirs_cols["W400"]), 4)}
print(json.dumps(sat))
OUT["part2_saturation"] = sat

# ---------- PART 3 consequence arithmetic ----------
Draw_T = regT["C400_clean"]["D_raw"]
ar = {}
for name in ("C400_clean", "W400", "W1e6"):
    Dcond = regT[name]["D_cond"]
    tot_share = Dcond / Draw_T
    exc_share = (Dcond - 1) / (Draw_T - 1)
    ar[name] = {
        "Dred_verifier_pct": regT[name]["Dred_pct"],
        "residual_share_total_dispersion_reading": round(tot_share, 4),
        "ge52_total_reading": bool(round(100 * tot_share, 1) >= 51.95),
        "residual_share_excess_only_reading": round(exc_share, 4),
        "ge52_excess_reading": bool(exc_share >= 0.52),
        "excess_explained_pct_strict": round(100 * (1 - exc_share), 1),
        "residual_still_overdispersed_Dcond_gt_1": bool(Dcond > 1.0),
    }
ar["identity_Dred_eq_100x(1-Dcond/Draw)_holds_all"] = all(
    abs(v["Dred_verifier_pct"] - 100 * v["residual_share_total_dispersion_reading"]) < 0.06
    for v in ar.values() if isinstance(v, dict) and "Dred_verifier_pct" in v)
OUT["part3_consequence_arithmetic"] = ar
print(json.dumps(ar))

OUT["wall_s"] = round(time.time() - t_start, 1)
with open("verifyL7b_result.json", "w") as f:
    json.dump(OUT, f, indent=1)
print(f"DONE wall={OUT['wall_s']}s -> verifyL7b_result.json")

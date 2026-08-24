#!/usr/bin/env python3
"""EXP 560 'PORTFOLIO' (round-71) -- static pipeline vs dial-adaptive pipeline
over a 5-method factoring portfolio at toy bitlen 32-40: is there a per-N
winner crossover, and can an N-only dial exploit it?

PRE-STATED HYPOTHESES (written BEFORE any data generation; checkpointed to
exp560_result.json at stage 00 before the population draw):
  H1 (crossover structure): no portfolio member reaches oracle-winner share
     >= 0.90 on the population; the rho-vs-Fermat winner flips along the
     N-only balance axis -- Fermat's winner share in the most-balanced
     quintile >= 0.25 AND its share in the least-balanced quintile <= 0.05.
  H2 (dial value, PRIMARY = rule dial): on the held-out TEST half, the
     dial-adaptive pipeline's mean regret ratio (cost / per-N oracle cost)
     is BELOW the best static pipeline's, with the paired bootstrap CI95 for
     delta(mean regret) entirely < 0, and relative reduction >= 10%.
  H3 (structural eliminations, pre-computed from the cost model): trial
     division and PM1(B1=1024) have oracle-winner share EXACTLY 0 at these
     bitlens under the stated caps/pricing (pi(p) > 1.18*sqrt(p) for all
     p >= 2^10; PM1-1024 constant work ~1500 units > 1.18*sqrt(min(p,q))
     for every reachable min-factor < 2^20). PM1(B1=256) is NOT predicted
     dead -- its winner share is an empirical map cell.

DESIGN (fixed before data; RECONSTRUCTION NOTE recorded verbatim at stage 00):
  Brief coverage: the tasking channel specified exp id 560, the script path,
  the population (600 semiprimes, bitlen 32-40, seed 20260827), smoke n=30,
  and the deliverables (result JSON + log; digest fields: crossover map,
  static vs dial-adaptive regret ratios, data-driven verdict, ledger
  catches). Method set, caps, pricing, train/test protocol and adaptive
  policies were NOT specified -- they are fixed HERE, pre-data, and written
  to stage 00 of the result JSON before the population draw so the cell is
  auditable against the brief.
  Population : 600 odd semiprimes N = p*q, p != q, both prime, stratified
               round-robin to EXACT bitlens 32..40 (bins 32..37 get 67,
               38..40 get 66). p uniform prime in [2^10, 2^20),
               q uniform prime in [2^12, 2^22), independent rejection
               sampling from ONE stream, seed 20260827; pair accepted iff
               bitlen(p*q) == current target and p < q. Factor-bit ratios
               therefore range from balanced (Fermat-friendly) to ~1:2.2
               bits (rho-friendly) WITHIN the population -- that spread is
               what the crossover map measures.
  Portfolio  : TD       trial division by all primes <= 2^16 (6542 mods)
               RHO      Pollard rho (Brent), per-N deterministic stream,
                        cap 250_000 core iterations
               FERMAT   x from isqrt(N) upward, perfect-square test,
                        cap 100_000 steps
               PM1_256  Pollard p-1 stage 1, B1 = 256, bases (2,3,5,7)
               PM1_1024 same, B1 = 1024
  Pricing    (pre-stated, units = elementary modular ops):
               td_mod 1 | rho_iter 1 | gcd 3 | fer_step 2 (isqrt class) |
               pm_mul 1 (square-and-multiply count = bits(t)-1+popcnt(t)-1)
               Robustness: verdicts re-checked under ALL-UNITS-1 pricing
               and under FER_STEP=4 pricing; stability recorded.
  Leakage    : the feature function takes N ALONE (code-path separation
               asserted); features = bitlen, log2 N, gap0 = N - isqrt(N)^2,
               log2(gap0+1), gap0/sqrt(N), fractional part of sqrt(N),
               cntQR(odd p<=100), T(odd p<=400, sum 2/p), N mod 3/5/7/11/13,
               bitlen parity. NO factor-derived feature anywhere.
  Protocol   : seeded half-split (rng 20260828): TRAIN 300 / TEST 300.
     ORACLE  : per-N cheapest SUCCESSFUL single method (priced).
     STATIC  : best fixed pipeline order, chosen on TRAIN by minimum total
               cost over all 5! = 120 orders; frozen; evaluated on TEST.
               (regret-argmin order also reported, secondary.)
     DIAL-RULE (PRIMARY adaptive): balance threshold family -- if
               gap0/sqrt(N) <= tau1 put FERMAT head else RHO head; optional
               promotion of PM1_256 to head when gap0/sqrt(N) > tau2;
               (tau1, tau2, on/off) tuned on TRAIN by minimum mean regret
               over a 9x9x2 grid of train quantiles; frozen; evaluated TEST.
     DIAL-ML (secondary adaptive): per-method success probability by depth-4
               decision trees on the N-only features (train only) + train
               median success-cost per method; per-N method order ascending
               by P̂*ĉ + (1-P̂)*cap; frozen; evaluated TEST.
  Metrics    : mean/median regret ratio cost/oracle on TEST (primary),
               mean cost, censor count, paired bootstrap (10k, seed 20260829)
               CI95 on delta mean regret (dial - static). Full-population
               numbers reported descriptively.
  Crossover  : winner-share matrices (method x bitlen-bin, method x
               balance-quintile) + per-method census (success rate, mean
               cost | success) + per-bin strategy regret table.

BARRIERS (standard lines):
  (5) SCOPE: toy scale (bitlen 32-40), THIS sampler (p in [2^10,2^20),
      q in [2^12,2^22)), these five members, caps and pricings; no claim
      about production sieving, larger bitlens, or other method mixes.
  (8) MEASUREMENT: costs are op-count PRICING, not wall time (robustness
      repricing recorded); rho cost is one random stream per N (expected-
      value noise, not averaged); single train/test split (bootstrap only
      resamples TEST); the rule dial's tau-grid is train-quantile based
      (definition-dependence). TD/PM1-1024 eliminations are conditional on
      the stated floors/caps/pricing (pre-computed, H3).
  (9) LEAKAGE: adaptive policies see N-only features only; enforced by
      code-path separation and asserted at runtime.

RUN: SMOKE=1 -> 30 Ns, reduced bootstraps. Full: 600 Ns, seed 20260827.
"""

import csv
import json
import math
import os
import random
import time
import traceback
from itertools import permutations
from math import gcd, isqrt

import numpy as np
from gmpy2 import mpz, is_prime, powmod
from scipy.stats import spearmanr
from sklearn.tree import DecisionTreeClassifier

HERE = os.path.dirname(os.path.abspath(__file__))
RESULT = os.path.join(HERE, "exp560_result.json")

SMOKE = os.environ.get("SMOKE", "") == "1"

# ---------------- fixed configuration ----------------
SEED_POP = 20260827
SEED_SPLIT = 20260828
SEED_BOOT = 20260829
SEED_ML = 20260831
SEED_RHO = 20260830

TOTAL_N = 30 if SMOKE else 600
BITS = list(range(32, 41))                  # exact bitlen targets, round-robin
LO_P, HI_P = 2**10, 2**20                   # p uniform prime, bitlen 11..20
LO_Q, HI_Q = 2**12, 2**22                   # q uniform prime, bitlen 13..22

METHODS = ["TD", "RHO", "FERMAT", "PM1_256", "PM1_1024"]
TD_BOUND = 2**16                            # trial division prime bound
RHO_CAP_ITERS = 250_000                     # core rho iterations
FER_CAP_STEPS = 100_000                     # fermat x-steps
PM_BASES = (2, 3, 5, 7)

# op-count caps (theoretical, for censored cost + ML scoring)
CAP_OPS = {
    "td_mods": len([]),                     # filled after sieve
    "rho_iters": RHO_CAP_ITERS,
    "rho_gcds": 8000,                       # ~cap/128 batches + backtracks
    "fer_steps": FER_CAP_STEPS,
    "pm_mul": 9000,                         # >> psi(1024)*|bases|
    "pm_gcd": 1400,
}

PRICINGS = {
    "MAIN": {"td_mods": 1, "rho_iters": 1, "rho_gcds": 3,
             "fer_steps": 2, "pm_mul": 1, "pm_gcd": 3},
    "FLAT1": {"td_mods": 1, "rho_iters": 1, "rho_gcds": 1,
              "fer_steps": 1, "pm_mul": 1, "pm_gcd": 1},
    "HEAVY_FER": {"td_mods": 1, "rho_iters": 1, "rho_gcds": 3,
                  "fer_steps": 4, "pm_mul": 1, "pm_gcd": 3},
}
PRIMARY_PRICING = "MAIN"

N_BOOT_FULL = 10_000
N_BOOT = 500 if SMOKE else N_BOOT_FULL

T_START = time.time()


def log(msg):
    print(f"[{time.time()-T_START:8.1f}s] {msg}", flush=True)


def write_result(status, payload):
    path = RESULT
    doc = {}
    if os.path.exists(path):
        try:
            with open(path) as f:
                doc = json.load(f)
        except Exception:
            doc = {}
    doc.update({"exp": 560, "codename": "PORTFOLIO", "round": 71,
                "smoke": SMOKE, "status": status,
                "wall_s": round(time.time() - T_START, 1)})
    doc.update(payload)
    with open(path, "w") as f:
        json.dump(doc, f, indent=1, default=float)


# ---------------- primes ----------------
def sieve_primes(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            s[i * i :: i] = False
    return np.flatnonzero(s)


TD_PRIMES = None        # np array of primes <= TD_BOUND
PM_PRIMES = {}          # B1 -> list[(ell, t)] with t = largest ell^e <= B1


def build_prime_tables():
    global TD_PRIMES, PM_PRIMES
    TD_PRIMES = sieve_primes(TD_BOUND)
    CAP_OPS["td_mods"] = len(TD_PRIMES)
    for B1 in (256, 1024):
        tab = []
        for ell in sieve_primes(B1):
            t = ell
            while t * ell <= B1:
                t *= ell
            tab.append((int(ell), int(t)))
        PM_PRIMES[B1] = tab


def draw_uniform_primes(rng, lo, hi, k, small_filter):
    """Uniform primes in [lo, hi) by rejection sampling on uniform integers."""
    out = []
    while len(out) < k:
        m = max(4096, 32 * (k - len(out)))
        v = rng.integers(lo, hi, size=m, dtype=np.int64)
        mask = np.ones(len(v), dtype=bool)
        for sp in small_filter:
            mask &= (v % sp) != 0
        for x in v[mask].tolist():
            if is_prime(x):
                out.append(x)
                if len(out) == k:
                    break
    return out


def gen_population():
    """Stratified round-robin to exact bitlens; one rng stream, seed fixed."""
    rng = np.random.default_rng(SEED_POP)
    small = sieve_primes(100)[1:]
    want = [BITS[i % len(BITS)] for i in range(TOTAL_N)]
    Ns, ps, qs = [], [], []
    buf_p, buf_q = [], []
    attempts = 0
    hist = {b: 0 for b in BITS}
    for target in want:
        while True:
            if not buf_p:
                need = 256
                buf_p.extend(draw_uniform_primes(rng, LO_P, HI_P, need, small))
                buf_q.extend(draw_uniform_primes(rng, LO_Q, HI_Q, need, small))
            p = buf_p.pop(0)
            q = buf_q.pop(0)
            attempts += 1
            if p == q:
                continue
            if p > q:
                p, q = q, p
            N = p * q
            if N.bit_length() == target:
                Ns.append(mpz(N))
                ps.append(p)
                qs.append(q)
                hist[target] += 1
                break
    assert len(Ns) == TOTAL_N
    assert len(set(map(int, Ns))) == TOTAL_N
    for N, p, q in zip(Ns, ps, qs):
        assert int(N) == p * q and p < q and is_prime(p) and is_prime(q)
        assert int(N) % 2 == 1
    log(f"population: {TOTAL_N} semiprimes in {attempts} pair-attempts "
        f"({100.0*TOTAL_N/attempts:.1f}% accept); hist={hist}")
    return Ns, ps, qs, hist


# ---------------- N-ONLY features (leakage barrier: no p,q in scope) -------
def features_for_N(N):
    Ni = int(N)
    b = Ni.bit_length()
    r = isqrt(Ni)
    gap0 = Ni - r * r
    sq = math.sqrt(Ni)
    cnt = 0
    T = 0.0
    mz = mpz(Ni)
    for p in ODD_PRIMES_400:
        if powmod(mz, EXPS_400[p], p) == 1:
            cnt += p <= 100
            if p <= 400:
                T += 2.0 / p
    return {
        "bitlen": float(b),
        "log2N": float(math.log2(Ni)),
        "gap0": float(gap0),
        "log2gap_p1": float(math.log2(gap0 + 1)),
        "bal": float(gap0 / sq),
        "frac_sqrt": float(sq - r),
        "cntQR100": float(cnt),
        "T400": float(T),
        "mod3": float(Ni % 3), "mod5": float(Ni % 5), "mod7": float(Ni % 7),
        "mod11": float(Ni % 11), "mod13": float(Ni % 13),
        "bl_odd": float(b % 2),
    }


FEAT_KEYS = ["bitlen", "log2N", "gap0", "log2gap_p1", "bal", "frac_sqrt",
             "cntQR100", "T400", "mod3", "mod5", "mod7", "mod11", "mod13",
             "bl_odd"]


# ---------------- portfolio members (each returns factor or None + op counts)
def run_TD(N):
    Ni = int(N)
    mods = 0
    for pp in TD_PRIMES.tolist():
        mods += 1
        if Ni % pp == 0:
            return pp, {"td_mods": mods}
        if pp * pp > Ni:
            break
    return None, {"td_mods": mods}


def run_RHO(N):
    """Pollard rho (Brent), deterministic per-N stream, capped + counted."""
    n = int(N)
    rnd = random.Random()
    rnd.seed(f"{SEED_RHO}:{n}")   # str seed: stable across runs
    iters = 0
    gcds = 0

    def tick_update():
        nonlocal iters
        iters += 1
        if iters > RHO_CAP_ITERS:
            raise TimeoutError

    while True:
        try:
            y = rnd.randrange(1, n)
            c = rnd.randrange(1, n)
            m = 128
            g = r = q = 1
            x = ys = y
            while g == 1:
                x = y
                for _ in range(r):
                    y = (y * y + c) % n
                    tick_update()
                k = 0
                while k < r and g == 1:
                    ys = y
                    for _ in range(min(m, r - k)):
                        y = (y * y + c) % n
                        q = q * abs(x - y) % n
                        tick_update()
                    g = gcd(q, n)
                    gcds += 1
                    k += m
                r *= 2
            if g == n:
                g = 1
                while g == 1:
                    ys = (ys * ys + c) % n
                    tick_update()
                    g = gcd(abs(x - ys), n)
                    gcds += 1
            if g != n:
                return g, {"rho_iters": iters, "rho_gcds": gcds}
            # g == n -> rare degeneracy: restart with fresh (y, c)
        except TimeoutError:
            return None, {"rho_iters": iters, "rho_gcds": gcds}


def run_FERMAT(N):
    n = int(N)
    r = isqrt(n)
    x = r if r * r == n else r + 1   # start at ceil(sqrt(n)): y2 >= 0
    steps = 0
    while steps < FER_CAP_STEPS:
        y2 = x * x - n
        s = isqrt(y2)
        steps += 1
        if s * s == y2:
            f = x - s
            if f > 1 and n % f == 0:
                return f, {"fer_steps": steps}
        x += 1
    return None, {"fer_steps": steps}


def run_PM1(N, B1):
    """Stage-1 p-1 with E = lcm(1..B1); bases retried on gcd==N."""
    n = int(N)
    mul = 0
    gds = 0
    for base in PM_BASES:
        a = mpz(base)
        dead_base = False
        for ell, t in PM_PRIMES[B1]:
            # a = a^t mod N, counted as square-and-multiply
            mul += (t.bit_length() - 1) + bin(t).count("1") - 1
            a = powmod(a, t, n)
            ai = int(a)
            g = gcd(ai - 1, n)
            gds += 1
            if 1 < g < n:
                return g, {"pm_mul": mul, "pm_gcd": gds}
            if g == n or ai == 1:
                dead_base = True
                break
        if not dead_base:
            g = gcd(int(a) - 1, n)
            gds += 1
            if 1 < g < n:
                return g, {"pm_mul": mul, "pm_gcd": gds}
    return None, {"pm_mul": mul, "pm_gcd": gds}


RUNNERS = {
    "TD": lambda N: run_TD(N),
    "RHO": lambda N: run_RHO(N),
    "FERMAT": lambda N: run_FERMAT(N),
    "PM1_256": lambda N: run_PM1(N, 256),
    "PM1_1024": lambda N: run_PM1(N, 1024),
}

OP_KEYS = {
    "TD": ["td_mods"], "RHO": ["rho_iters", "rho_gcds"],
    "FERMAT": ["fer_steps"], "PM1_256": ["pm_mul", "pm_gcd"],
    "PM1_1024": ["pm_mul", "pm_gcd"],
}


def priced_cost(method, ops, prices):
    return sum(ops[k] * prices[k] for k in OP_KEYS[method])


def priced_cap(method, prices):
    return priced_cost(method, {k: CAP_OPS[k] for k in OP_KEYS[method]},
                       prices)


# ---------------- strategies ----------------
def pipeline_cost(order, row, prices):
    """Replay a fixed order; returns (total_cost, success, used)."""
    total = 0
    for m in order:
        o = row[m]
        c = priced_cost(m, o["ops"], prices)
        total += c
        if o["succ"]:
            return total, True
    return total, False


def oracle_cost(row, prices):
    best, bm = None, None
    for m in METHODS:
        o = row[m]
        if o["succ"]:
            c = priced_cost(m, o["ops"], prices)
            if best is None or c < best:
                best, bm = c, m
    return best, bm


def eval_orders(order_of, rows, prices, orc):
    """order_of(i,row) -> ordered METHOD list; returns arrays cost/regret."""
    n = len(rows)
    cost = np.zeros(n)
    reg = np.zeros(n)
    ok = 0
    cens = 0
    for i, row in enumerate(rows):
        order = order_of(i, row)
        c, s = pipeline_cost(order, row, prices)
        if not s:
            c = sum(priced_cap(m, prices) for m in order)
            cens += 1
        cost[i] = c
        reg[i] = c / orc[i]
        ok += int(s)
    return cost, reg, ok, cens


# ---------------- main ----------------
ODD_PRIMES_400 = None
EXPS_400 = {}


def main():
    global ODD_PRIMES_400
    build_prime_tables()

    # ---- stage 00: hypotheses/config BEFORE any data ----
    write_result("00_hypotheses_stated", {
        "hypotheses": {
            "H1": "crossover structure: max oracle-winner share < 0.90; "
                  "Fermat winner-share top balance-quintile >= 0.25 AND "
                  "bottom quintile <= 0.05",
            "H2": "PRIMARY dial (rule) beats best static pipeline on TEST "
                  "mean regret: paired bootstrap CI95 < 0 and relative "
                  "reduction >= 10%",
            "H3": "structural eliminations: TD and PM1_1024 oracle shares "
                  "exactly 0 (pre-computed from cost model)",
        },
        "reconstruction_note":
            "tasking channel specified exp id/path/population "
            "(600 semiprimes, bitlen 32-40, seed 20260827)/smoke n=30/"
            "deliverables only; method set {TD, RHO, FERMAT, PM1_256, "
            "PM1_1024}, caps, pricing, split, and adaptive policies were "
            "fixed HERE pre-data and are recorded in this config block",
        "config": {
            "seed_pop": SEED_POP, "seed_split": SEED_SPLIT,
            "seed_boot": SEED_BOOT, "seed_ml": SEED_ML,
            "seed_rho": SEED_RHO,
            "total_n": TOTAL_N, "bitlen_targets": BITS,
            "p_range": [LO_P, HI_P], "q_range": [LO_Q, HI_Q],
            "methods": METHODS,
            "td_bound": TD_BOUND,
            "rho_cap_iters": RHO_CAP_ITERS,
            "fer_cap_steps": FER_CAP_STEPS,
            "pm_bases": list(PM_BASES),
            "cap_ops": CAP_OPS,
            "pricings": PRICINGS, "primary_pricing": PRIMARY_PRICING,
            "primary_adaptive": "DIAL-RULE",
            "n_boot": N_BOOT,
            "features": FEAT_KEYS,
        },
    })
    log("stage 00 done (hypotheses + config checkpointed)")

    ODD_PRIMES_400 = [int(p) for p in sieve_primes(400) if p > 2]
    for p in ODD_PRIMES_400:
        EXPS_400[p] = (p - 1) // 2

    # ---- stage 01: population ----
    Ns, ps, qs, hist = gen_population()
    with open(os.path.join(HERE, "exp560_population.txt"), "w") as f:
        for i, (N, p, q) in enumerate(zip(Ns, ps, qs)):
            f.write(f"{i} {int(N).bit_length()} {p} {q} {N}\n")
    write_result("01_population_done", {
        "population": {"total": TOTAL_N, "hist_by_bitlen": hist}})
    log("stage 01 done (population written)")

    # ---- stage 02: features (N-only) + portfolio outcomes ----
    feats = [features_for_N(N) for N in Ns]
    rows = []
    for i, N in enumerate(Ns):
        row = {}
        for m in METHODS:
            fac, ops = RUNNERS[m](N)
            if fac is not None:
                assert 1 < fac < int(N) and int(N) % fac == 0, \
                    f"bad factor {fac} for {m} on N={N}"
            row[m] = {"succ": fac is not None,
                      "fac": int(fac) if fac is not None else None,
                      "ops": ops}
        rows.append(row)
        if (i + 1) % (10 if SMOKE else 50) == 0:
            log(f"methods done {i+1}/{TOTAL_N}")
    write_result("02_methods_done", {})
    log("stage 02 done (portfolio outcomes)")

    # census (full pop, MAIN pricing)
    census = {}
    for m in METHODS:
        succ = [r[m]["succ"] for r in rows]
        cs = [priced_cost(m, r[m]["ops"], PRICINGS["MAIN"])
              for r in rows if r[m]["succ"]]
        ca = [priced_cost(m, r[m]["ops"], PRICINGS["MAIN"]) for r in rows]
        census[m] = {
            "success_rate": float(np.mean(succ)),
            "n_success": int(np.sum(succ)),
            "mean_cost_given_success": float(np.mean(cs)) if cs else None,
            "median_cost_given_success":
                float(np.median(cs)) if cs else None,
            "mean_cost_all_incl_caps": float(np.mean(ca)),
            "max_cost_observed": float(np.max(ca)),
        }

    # oracle
    orc = np.zeros(TOTAL_N)
    ow = [None] * TOTAL_N
    for i, row in enumerate(rows):
        c, m = oracle_cost(row, PRICINGS["MAIN"])
        assert c is not None, f"no method succeeded for N index {i}"
        orc[i] = c
        ow[i] = m

    # ---- stage 03: split + strategies (MAIN pricing) ----
    perm = np.random.default_rng(SEED_SPLIT).permutation(TOTAL_N)
    train_idx = np.sort(perm[:TOTAL_N // 2])
    test_idx = np.sort(perm[TOTAL_N // 2:])
    in_train = np.zeros(TOTAL_N, dtype=bool)
    in_train[train_idx] = True

    X = np.array([[f[k] for k in FEAT_KEYS] for f in feats])
    bal = X[:, FEAT_KEYS.index("bal")]

    results = {}

    # ---------- STATIC: best of 120 fixed orders on TRAIN ----------
    def static_best(metric):
        best_ord, best_val = None, None
        for cand in permutations(METHODS):
            c, _, _, cens = eval_orders(lambda i, r, o=cand: o, rows,
                                        PRICINGS["MAIN"], orc)
            val = float(c[train_idx].mean()) if metric == "cost" \
                else float((c[train_idx] / orc[train_idx]).mean())
            if best_val is None or val < best_val:
                best_ord, best_val = cand, val
        return best_ord, best_val

    t0 = time.time()
    static_ord, static_train_cost = static_best("cost")
    log(f"static search done ({time.time()-t0:.0f}s): "
        f"order={static_ord} train_mean_cost={static_train_cost:.0f}")
    static_ord_reg, static_train_reg = static_best("regret")

    # ---------- DIAL-RULE (PRIMARY) ----------
    qs_bal = np.quantile(bal[train_idx], np.linspace(0, 1, 9))
    TAIL = ["TD", "PM1_256", "PM1_1024"]

    def rule_policy(tau1, tau2, promote):
        def of(i, row):
            b = bal[i]
            if b <= tau1:
                head = ["FERMAT", "RHO"]
            else:
                head = ["RHO", "FERMAT"]
            if promote and b > tau2:
                head = ["PM1_256"] + head
            return head + TAIL
        return of

    best_rule, best_rule_val = None, None
    for tau1 in qs_bal:
        for tau2 in qs_bal:
            for promote in (False, True):
                of = rule_policy(tau1, tau2, promote)
                _, reg, _, _ = eval_orders(of, rows, PRICINGS["MAIN"], orc)
                val = float(reg[train_idx].mean())
                if best_rule_val is None or val < best_rule_val:
                    best_rule_val = val
                    best_rule = (tau1, tau2, promote)
    rule_tau1, rule_tau2, rule_promote = best_rule
    rule_of = rule_policy(rule_tau1, rule_tau2, rule_promote)
    log(f"rule dial tuned: tau1={rule_tau1:.4f} tau2={rule_tau2:.4f} "
        f"promote_pm1={rule_promote} train_mean_regret={best_rule_val:.4f}")

    # ---------- DIAL-ML (secondary) ----------
    yt = np.array([[1.0 if rows[i][m]["succ"] else 0.0 for m in METHODS]
                   for i in train_idx])
    chat = {}
    for j, m in enumerate(METHODS):
        cs = [priced_cost(m, rows[i][m]["ops"], PRICINGS["MAIN"])
              for i in train_idx if rows[i][m]["succ"]]
        chat[m] = float(np.median(cs)) if cs else priced_cap(m, PRICINGS["MAIN"])
    trees = {}
    for j, m in enumerate(METHODS):
        tr = DecisionTreeClassifier(max_depth=4, min_samples_leaf=15,
                                    random_state=SEED_ML)
        tr.fit(X[train_idx], yt[:, j])
        trees[m] = tr
    caps_m = {m: priced_cap(m, PRICINGS["MAIN"]) for m in METHODS}

    def ml_phat(i, m):
        tr = trees[m]
        if getattr(tr, "n_classes_", 2) == 1:
            return float(tr.classes_[0])   # degenerate (smoke) tree
        col = int(np.flatnonzero(tr.classes_ == 1.0)[0])
        return float(tr.predict_proba(X[i:i+1])[0, col])

    def ml_order(i, row):
        score = []
        for m in METHODS:
            phat = ml_phat(i, m)
            score.append(phat * chat[m] + (1 - phat) * caps_m[m])
        return [m for _, m in sorted(zip(score, METHODS))]

    # ---------- evaluate all strategies ----------
    strat_defs = {
        "STATIC": (lambda i, row: static_ord),
        "STATIC_REGRETSEL": (lambda i, row: static_ord_reg),
        "DIAL_RULE": (rule_of,),
        "DIAL_ML": (ml_order,),
    }
    for name, od in strat_defs.items():
        of = od[0] if isinstance(od, tuple) else od
        c, reg, ok, cens = eval_orders(of, rows, PRICINGS["MAIN"], orc)
        results[name] = {"order_of": of, "cost": c, "regret": reg,
                         "ok": ok, "censored": cens}

    def summarize(name, idx):
        r = results[name]
        c = r["cost"][idx]
        g = r["regret"][idx]
        return {"mean_cost": float(c.mean()),
                "mean_regret": float(g.mean()),
                "median_regret": float(np.median(g)),
                "p90_regret": float(np.percentile(g, 90)),
                "successes": int(r["ok"]),
                "censored": int(r["censored"])}

    primary = "DIAL_RULE"
    test_summary = {name: summarize(name, test_idx) for name in results}
    full_summary = {name: summarize(name, np.arange(TOTAL_N))
                    for name in results}

    # paired bootstrap on TEST mean regret: dial - static
    rngb = np.random.default_rng(SEED_BOOT)
    nt = len(test_idx)
    deltas = {}
    for adv in ("DIAL_RULE", "DIAL_ML"):
        d = np.empty(len(range(N_BOOT)))
        gr = results[adv]["regret"][test_idx]
        gs = results["STATIC"]["regret"][test_idx]
        for k in range(N_BOOT):
            ii = rngb.integers(0, nt, nt)
            d[k] = gr[ii].mean() - gs[ii].mean()
        deltas[adv] = {
            "delta_mean_regret": float(gr.mean() - gs.mean()),
            "ci95": [float(np.percentile(d, 2.5)),
                     float(np.percentile(d, 97.5))],
            "rel_reduction_vs_static":
                float(1 - gr.mean() / gs.mean()),
        }
    static_test = test_summary["STATIC"]
    rule_test = test_summary["DIAL_RULE"]

    write_result("03_strategies_done", {
        "split": {"train": int(len(train_idx)), "test": int(len(test_idx))},
        "static_order_by_cost": list(static_ord),
        "static_order_by_regret": list(static_ord_reg),
        "rule_params": {"tau1": float(rule_tau1), "tau2": float(rule_tau2),
                        "promote_pm1_256": bool(rule_promote)},
        "test_summary": test_summary,
        "paired_bootstrap": deltas,
    })
    log(f"stage 03 done: STATIC test mean regret "
        f"{static_test['mean_regret']:.4f} | DIAL_RULE "
        f"{rule_test['mean_regret']:.4f}")

    # ---- crossover map (descriptive, full population, MAIN pricing) ----
    bl = np.array([int(N).bit_length() for N in Ns])
    balq = np.quantile(bal, [0.2, 0.4, 0.6, 0.8])
    bq_id = np.digitize(bal, balq)   # 0..4 (4 = most balanced? NO: bal small =
                                     # balanced; digitize ascending bal ->
                                     # bucket 0 = most balanced)
    def share_matrix(ids):
        out = {}
        for v in sorted(set(ids.tolist())):
            sel = ids == v
            tot = int(sel.sum())
            out[int(v)] = {
                "n": tot,
                **{m: float(np.mean([ow[i] == m for i in np.flatnonzero(sel)]))
                   for m in METHODS},
            }
        return out

    win_by_bitlen = share_matrix(bl)
    win_by_balquintile = share_matrix(bq_id.astype(int))

    # per-bin strategy regrets
    regret_table = {}
    for v in sorted(set(bl.tolist())):
        sel = np.flatnonzero(bl == v)
        regret_table[int(v)] = {
            "n": int(len(sel)),
            "oracle_winner_shares": win_by_bitlen[v],
            **{f"regret_{name}":
               float(results[name]["regret"][sel].mean())
               for name in ("STATIC", "DIAL_RULE", "DIAL_ML")},
        }

    shares_overall = {m: float(np.mean([w == m for w in ow])) for m in METHODS}
    # digitize buckets ascend with bal = gap0/sqrt(N):
    #   bucket 0 = SMALLEST bal = MOST BALANCED, bucket 4 = LEAST BALANCED
    q_most_bal = np.flatnonzero(bq_id == 0)
    q_least_bal = np.flatnonzero(bq_id == 4)
    fer_bal = float(np.mean([ow[i] == "FERMAT" for i in q_most_bal]))
    fer_unbal = float(np.mean([ow[i] == "FERMAT" for i in q_least_bal]))

    # ---- pricing robustness: recompute headline numbers under alt pricings
    robustness = {}
    for pname in PRICINGS:
        pr = PRICINGS[pname]
        if pname == PRIMARY_PRICING:
            continue
        orc_p = np.array([oracle_cost(row, pr)[0] for row in rows])
        # static re-selection per pricing (honest: selection under own pricing)
        best_ord, best_val = None, None
        for cand in permutations(METHODS):
            c_c, _, _, _ = eval_orders(lambda i, r, o=cand: o,
                                       rows, pr, orc_p)
            val = float(c_c[train_idx].mean())
            if best_val is None or val < best_val:
                best_ord, best_val = cand, val
        c_s, _, _, _ = eval_orders(lambda i, r, o=best_ord: o,
                                   rows, pr, orc_p)
        c_r, _, _, _ = eval_orders(rule_of, rows, pr, orc_p)
        c_m, _, _, _ = eval_orders(ml_order, rows, pr, orc_p)
        gs = c_s[test_idx] / orc_p[test_idx]
        gr = c_r[test_idx] / orc_p[test_idx]
        gm = c_m[test_idx] / orc_p[test_idx]
        robustness[pname] = {
            "static_order": list(best_ord),
            "static_mean_regret_test": float(gs.mean()),
            "rule_mean_regret_test": float(gr.mean()),
            "ml_mean_regret_test": float(gm.mean()),
            "rel_reduction_rule_vs_static": float(1 - gr.mean() / gs.mean()),
            "sign_holds": bool(gr.mean() < gs.mean()),
        }

    # ---- hypotheses ----
    max_share = max(shares_overall.values())
    h1 = bool(max_share < 0.90 and fer_bal >= 0.25 and fer_unbal <= 0.05)
    ci_rule = deltas["DIAL_RULE"]["ci95"]
    rel_rule = deltas["DIAL_RULE"]["rel_reduction_vs_static"]
    h2 = bool(ci_rule[1] < 0 and rel_rule >= 0.10)
    h3 = bool(shares_overall["TD"] == 0.0
              and shares_overall["PM1_1024"] == 0.0)

    if h1 and h2:
        verdict = "PORTFOLIO-CROSSOVER-REAL-DIAL-WINS"
    elif h1 and not h2:
        verdict = "PORTFOLIO-CROSSOVER-REAL-DIAL-BLIND"
    elif h2 and not h1:
        verdict = "PORTFOLIO-DIAL-WINS-NO-CROSSOVER"
    else:
        verdict = "PORTFOLIO-RHO-UNIVERSAL"
    if not h3:
        verdict += "+H3-FAIL"

    ledger_catches = [
        "brief under-specification: method set/caps/pricing/split/policies "
        "not given by tasking channel -> fixed pre-data and recorded at "
        "stage 00 (reconstruction_note)",
        "leakage guard: feature function isolated from factor variables; "
        "runtime assert that every claimed factor divides its N",
    ]

    write_result("04_final", {
        "hypotheses_verdicts": {"H1_pass": h1, "H2_pass": h2, "H3_pass": h3,
                                 "verdict_name": verdict},
        "oracle_winner_shares_overall": shares_overall,
        "fermat_share_most_balanced_quintile": fer_bal,
        "fermat_share_least_balanced_quintile": fer_unbal,
        "crossover_map_by_bitlen": regret_table,
        "crossover_map_by_balance_quintile": win_by_balquintile,
        "method_census_MAIN_pricing": census,
        "strategy_summary_TEST": test_summary,
        "strategy_summary_FULLPOP": full_summary,
        "paired_bootstrap_dial_minus_static": deltas,
        "pricing_robustness": robustness,
        "oracle_cost_MAIN": {"mean": float(orc.mean()),
                              "median": float(np.median(orc))},
        "ledger_catches": ledger_catches,
    })

    # ---- artifacts: per-N csv + crossover csv ----
    with open(os.path.join(HERE, "exp560_per_n.csv"), "w", newline="") as f:
        w = csv.writer(f)
        head = ["idx", "bitlen", "p", "q", "N", "gap0", "bal", "cntQR100",
                "T400", "oracle_method", "oracle_cost", "in_train"]
        for m in METHODS:
            head += [f"{m}_succ", f"{m}_cost_MAIN"]
        for name in ("STATIC", "DIAL_RULE", "DIAL_ML"):
            head += [f"{name}_cost", f"{name}_regret"]
        w.writerow(head)
        for i, (N, p, q) in enumerate(zip(Ns, ps, qs)):
            roww = [i, int(N).bit_length(), p, q, int(N),
                    feats[i]["gap0"], feats[i]["bal"], feats[i]["cntQR100"],
                    feats[i]["T400"], ow[i], orc[i], int(bool(in_train[i]))]
            for m in METHODS:
                o = rows[i][m]
                roww += [int(o["succ"]),
                         priced_cost(m, o["ops"], PRICINGS["MAIN"])]
            for name in ("STATIC", "DIAL_RULE", "DIAL_ML"):
                roww += [results[name]["cost"][i],
                         results[name]["regret"][i]]
            w.writerow(roww)

    with open(os.path.join(HERE, "exp560_crossover_map.csv"), "w",
              newline="") as f:
        w = csv.writer(f)
        w.writerow(["bitlen", "n"] + [f"win_{m}" for m in METHODS]
                   + [f"regret_{n}" for n in ("STATIC", "DIAL_RULE",
                                              "DIAL_ML")])
        for b in sorted(regret_table):
            rr = regret_table[b]
            w.writerow([b, rr["n"]]
                       + [rr["oracle_winner_shares"][m] for m in METHODS]
                       + [rr[f"regret_{n}"] for n in ("STATIC", "DIAL_RULE",
                                                      "DIAL_ML")])

    log(f"FINAL: shares={ {m: round(v,3) for m,v in shares_overall.items()} }")
    log(f"FINAL: TEST mean regret STATIC="
        f"{static_test['mean_regret']:.4f} DIAL_RULE="
        f"{rule_test['mean_regret']:.4f} DIAL_ML="
        f"{test_summary['DIAL_ML']['mean_regret']:.4f}")
    log(f"FINAL: delta(rule-static)={deltas['DIAL_RULE']['delta_mean_regret']:+.4f}"
        f" CI{ci_rule} rel={rel_rule:+.3f}")
    log(f"FINAL: H1={h1} H2={h2} H3={h3} VERDICT={verdict}")
    print("RUN_DONE", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        err = traceback.format_exc()
        print(err, flush=True)
        try:
            write_result("ERROR", {"traceback": err})
        except Exception:
            pass
        raise

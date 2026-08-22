#!/usr/bin/env python3
"""EXP 487 ECM-COMPLETION (round-42). Seed 20260921.
Completes paper 154's unified plane with the ECM arm + a uniform-draws arm.

PRE-STATED HYPOTHESES (registered before data, from round-42 assignment):
  H1: ECM's across-k scaling at fixed B1 sits between rho (0.52) and trial
      division (0.84) on balanced draws -- expect alpha ~ 0.6-0.8 per log2 p.
  H2: uniform draws shift trial division to alpha ~ 1.09 (paper-89 replication)
      and leave rho/ECM slopes unchanged (factor-locality), only moving intercepts.
  H3: ECM's intercept offset vs rho (constant c in log2 E[T] = alpha*log2 p + c,
      common currency) is positive but bounded -- within an order of magnitude
      (0 <= c_ECM - c_rho <= log2(10) = 3.32).

OP-COUNT CONVENTIONS (native units, ledger):
  trial division : one trial modulus = 1 op (candidates 3,5,7,... <= isqrt(N))
  Pollard rho    : Floyd, one iteration (3 field sq/add) = 3 ops, gcd batched 64
  Fermat         : one a-increment test (a^2-N, isqrt, compare) = 1 op
  ECM stage-1    : one affine point ADDITION or DOUBLING = 1 op (true stage-1:
                   scalar = prod l^e <= B1 via double-and-add per prime power;
                   curve y^2 = x^3 + a x mod N, random x,y, a solved from point;
                   denominators batched, gcd every 32 point-ops; inversion via
                   pow(-1) whose failure IS the factor event)
  Failed curves count toward T (honest E[T]); curve cap 40 per draw.
CENSORING POLICY: draws not factored by a method's cap are EXCLUDED from that
method's fit (biases alpha/c downward) and reported per cell. Caps: TD none
needed (<=512 ops here); rho 5 attempts x 20k iters; Fermat 20k iters;
ECM 40 curves at each B1.
COMMON CURRENCY (secondary, for H3): declared mul-mod equivalents --
  TD modop=1; rho field-op=1.1 + gcd-batch amortized 15M/64 iters;
  Fermat iter=4M; ECM point-op = 4M + 1 inversion(15M) + gcd amortize 1M = 20M.
  Cross-check H3 with measured WALL TIME per draw (machine-local but honest).
Barriers cited: (8) measuring known methods; (4) factor-locality.
"""
import json, math, time
import numpy as np
from sympy import primerange

SEED = 20260921
rng = np.random.default_rng(SEED)
T0 = time.time()
OUT = {"meta": {"seed": SEED, "exp": 487, "codename": "ECM-COMPLETION",
                "n_per_cell": 1200, "ks": [16, 20], "arms": ["balanced", "uniform"],
                "B1_list": [50, 250], "curve_cap": 40,
                "fermat_cap": 20000, "rho_attempts": 5, "rho_cap_per_attempt": 20000},
       "cells": [], "fits": {}, "verdicts": {}}

def checkpoint():
    json.dump(OUT, open("/tmp/exp42_ecm/result.json", "w"), indent=1)

# ---------------- populations ----------------
def make_balanced(k, n):
    h = k // 2
    pr = [int(q) for q in primerange(2**(h - 1), 2**h)]
    out = []
    while len(out) < n:
        i, j = rng.integers(0, len(pr), 2)
        p, q = pr[i], pr[j]
        if p == q:
            continue
        N = p * q
        out.append((N, min(p, q)))
    return out

def make_uniform(k, n):
    lim = 2**(k - 1)
    pr = np.array([int(q) for q in primerange(3, lim)])
    out = []
    while len(out) < n:
        p = int(pr[rng.integers(0, len(pr))])
        bound = (2**k - 1) // p
        cand = pr[pr <= bound]
        if len(cand) == 0:
            continue
        q = int(cand[rng.integers(0, len(cand))])
        if q == p or p * q < 2**(k - 1):
            continue
        out.append((p * q, min(p, q)))
    return out

# ---------------- methods ----------------
class Found(Exception):
    def __init__(self, g): self.g = g

class Dead(Exception):
    pass

def td_factor(N):
    ops = 0
    if N % 2 == 0:
        return 2, ops
    r = math.isqrt(N)
    d = 3
    while d <= r:
        ops += 1
        if N % d == 0:
            return d, ops
        d += 2
    return N, ops

def rho_factor(N, attempts=8, cap=20000):
    # LEDGER v3 (supersedes v2 batched product): two defects found in v2 and in
    # the first full run. (a) CYCLE-LOCK: when lambda_q | lambda_p, every p-sync
    # of the Floyd pair coincides with an exact x==y meeting; skipping x==y
    # diffs then discards every divisible diff and the attempt walks the closed
    # cycle to the 20000 cap (~6% of balanced k=16 draws, ~20193 ops each).
    # Standard remedy: exact meeting with no factor => this c failed => restart.
    # (b) UNDERCOUNT: the backtrack exit returned `total` without adding the
    # current attempt's iterations. (c) DESIGN: batch-64 gcd quantizes detection
    # to ~192 ops, a floor that erases the sqrt(p) scaling at toy scale (both
    # k cells would read alpha ~ 0). Per-iteration gcd restores the birthday
    # law; gcd cost at N < 2^20 is negligible. Ops = 3 field ops per iteration.
    total = 0
    for _ in range(attempts):
        x = y = int(rng.integers(2, N - 1))
        c = int(rng.integers(1, N - 1))
        it = 0
        while it < cap:
            x = (x * x + c) % N
            y = (y * y + c) % N
            y = (y * y + c) % N
            it += 3
            if x == y:
                break  # cycle closed, no factor: restart with fresh c
            g = math.gcd(abs(x - y), N)
            if 1 < g < N:
                return g, total + it
        total += it
    return None, total

def fermat_factor(N, cap=20000):
    a = math.isqrt(N)
    if a * a < N:
        a += 1
    ops = 0
    while ops < cap:
        b2 = a * a - N
        b = math.isqrt(b2)
        ops += 1
        if b * b == b2:
            return a - b, ops
        a += 1
    return None, ops

class St:
    __slots__ = ("ops", "denprod", "n")

def _padd(P, Q, a, N, st):
    """Affine add/double on y^2 = x^3 + a x (mod N). Counts 1 point-op."""
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2:
        if (y1 + y2) % N == 0:
            return None
        den = (2 * y1) % N
        num = (3 * x1 * x1 + a) % N
    else:
        den = (x2 - x1) % N
        num = (y2 - y1) % N
    st.ops += 1
    st.denprod = st.denprod * den % N
    st.n += 1
    if st.n % 32 == 0:
        g = math.gcd(st.denprod, N)
        st.denprod = 1
        if 1 < g < N:
            raise Found(g)
    if den == 0:
        g = math.gcd(num, N)
        if 1 < g < N:
            raise Found(g)
        raise Dead()
    try:
        inv = pow(den, -1, N)
    except ValueError:
        g = math.gcd(den, N)
        if 1 < g < N:
            raise Found(g)
        raise Dead()
    lam = num * inv % N
    x3 = (lam * lam - x1 - x2) % N
    y3 = (lam * (x1 - x3) - y1) % N
    return (x3, y3)

def _pmul(R, m, a, N, st):
    res, add = None, R
    while m:
        if m & 1:
            res = _padd(res, add, a, N, st)
        add = _padd(add, add, a, N, st)
        m >>= 1
    return res

def ecm_factor(N, B1, cap=40):
    """True stage-1: scalar = prod l^e <= B1 applied by ladder per prime power."""
    total = 0
    pp = []
    for l in range(2, B1 + 1):
        if all(l % d for d in range(2, int(l**0.5) + 1)):
            pe = l
            while pe * l <= B1:
                pe *= l
            pp.append(pe)
    for _ in range(cap):
        st = St(); st.ops = 0; st.denprod = 1; st.n = 0
        try:
            x = int(rng.integers(2, N - 1)); y = int(rng.integers(2, N - 1))
            g0 = math.gcd(x, N)
            if 1 < g0 < N:
                return g0, total
            xi = pow(x, -1, N)
            a = (y * y - x * x * x) * xi % N
            R = (x, y)
            for pe in pp:
                R = _pmul(R, pe, a, N, st)
            g = math.gcd(st.denprod, N)
            total += st.ops
            if 1 < g < N:
                return g, total
        except Found as f:
            total += st.ops
            return f.g, total
        except (Dead, ZeroDivisionError):
            total += st.ops
    return None, total

CC = {"td": lambda o: float(o),
      "rho": lambda o: o * 1.1 + (o / 192.0) * 15.0,
      "fermat": lambda o: 4.0 * o,
      "ecm50": lambda o: 20.0 * o,
      "ecm250": lambda o: 20.0 * o}
METHODS = [("td", lambda N: td_factor(N)),
           ("rho", lambda N: rho_factor(N)),
           ("fermat", lambda N: fermat_factor(N)),
           ("ecm50", lambda N: ecm_factor(N, 50)),
           ("ecm250", lambda N: ecm_factor(N, 250))]

# ---------------- run cells ----------------
res = {}  # (arm,k) -> {method: dict(times=[], cens=int, wall=[])}
for arm in ("balanced", "uniform"):
    for k in (16, 20):
        pops = make_balanced(k, 1200) if arm == "balanced" else make_uniform(k, 1200)
        cell = {}
        for name, fn in METHODS:
            Ts, walls, cens, ps = [], [], 0, []
            for N, mp in pops:
                t1 = time.perf_counter()
                f, ops = fn(N)
                walls.append(time.perf_counter() - t1)
                if f and 1 < f < N:
                    assert N % f == 0
                    Ts.append(max(ops, 1)); ps.append(mp)
                else:
                    cens += 1
            cell[name] = {"Ts": Ts, "ps": ps, "walls": walls, "cens": cens,
                          "cc": [CC[name](t) for t in Ts]}
            print(f"{arm} k={k} {name}: found={len(Ts)} cens={cens} "
                  f"meanT={np.mean(Ts) if Ts else None:.2f} "
                  f"wall={np.mean(walls)*1e3:.2f}ms [{time.time()-T0:.0f}s]", flush=True)
        res[(arm, k)] = cell
        OUT["cells"].append({
            "arm": arm, "k": k,
            **{name: {"found": len(cell[name]["Ts"]), "censored": cell[name]["cens"],
                      "mean_T_native": float(np.mean(cell[name]["Ts"])) if cell[name]["Ts"] else None,
                      "mean_log2_minp_uncens": float(np.mean(np.log2(cell[name]["ps"]))) if cell[name]["ps"] else None,
                      "mean_wall_ms": float(np.mean(cell[name]["walls"])) * 1e3}
               for name in cell}})
        checkpoint()

# ---------------- fits ----------------
fits = {}
for arm in ("balanced", "uniform"):
    for name, _ in METHODS:
        xs, ys, cs = [], [], []
        for kk in (16, 20):
            c = res[(arm, kk)]
            xs += [math.log2(p) for p in c[name]["ps"]]
            ys += [math.log2(t) for t in c[name]["Ts"]]
            cs += c[name]["cc"]
        sl, ic = np.polyfit(xs, ys, 1)
        slc, icc = np.polyfit(xs, np.log2(cs), 1)
        # paper-154-style across-k slope from cell means (balanced only meaningful vs 154)
        fits[f"{arm}/{name}"] = {
            "alpha_pooled_ols_native": round(float(sl), 4),
            "c_pooled_ols_native": round(float(ic), 4),
            "alpha_pooled_ols_cc": round(float(slc), 4),
            "c_pooled_ols_cc": round(float(icc), 4)}
OUT["fits"] = fits

def cell_mean_t(arm, kk, name, use_cc=False):
    c = res[(arm, kk)][name]
    v = c["cc"] if use_cc else c["Ts"]
    return float(np.mean(v)), float(np.mean(np.log2(c["ps"])))

headline = {}
for name, _ in METHODS:
    (t16, p16) = cell_mean_t("balanced", 16, name)
    (t20, p20) = cell_mean_t("balanced", 20, name)
    headline[name] = {"alpha_across_k_paper154_style":
                      round((math.log2(t20) - math.log2(t16)) / (p20 - p16), 4),
                      "E_T_k16": round(t16, 2), "E_T_k20": round(t20, 2),
                      "mean_log2p_k16": round(p16, 4), "mean_log2p_k20": round(p20, 4)}
OUT["headline_balanced_across_k"] = headline

# uniform-arm across-k slopes too (H2)
uni = {}
for name, _ in METHODS:
    (t16, p16) = cell_mean_t("uniform", 16, name)
    (t20, p20) = cell_mean_t("uniform", 20, name)
    uni[name] = round((math.log2(t20) - math.log2(t16)) / (p20 - p16), 4)
OUT["across_k_uniform"] = uni

# ---------------- verdicts ----------------
V = {}
a_ecm_b = [headline["ecm50"]["alpha_across_k_paper154_style"],
           headline["ecm250"]["alpha_across_k_paper154_style"]]
V["H1"] = {"alpha_ecm50": a_ecm_b[0], "alpha_ecm250": a_ecm_b[1],
           "claim_window": "(0.52, 0.84)",
           "verdict": bool(all(0.52 < a < 0.84 for a in a_ecm_b))}
# H2 uses POOLED OLS on BOTH arms for the locality test: the uniform arm's
# min(p,q) distribution shifts wholesale between k cells, so its two-point
# cell-mean across-k slope is not comparable (reported but flagged).
a_td_u = fits["uniform/td"]["alpha_pooled_ols_native"]
a_td_b = headline["td"]["alpha_across_k_paper154_style"]
a_rho_b_p = fits["balanced/rho"]["alpha_pooled_ols_native"]
a_rho_u_p = fits["uniform/rho"]["alpha_pooled_ols_native"]
a_e50_b_p = fits["balanced/ecm50"]["alpha_pooled_ols_native"]
a_e50_u_p = fits["uniform/ecm50"]["alpha_pooled_ols_native"]
V["H2"] = {"alpha_td_balanced_acrossk": a_td_b, "alpha_td_uniform_pooled": a_td_u,
           "alpha_rho_balanced_pooled": a_rho_b_p, "alpha_rho_uniform_pooled": a_rho_u_p,
           "alpha_ecm50_balanced_pooled": a_e50_b_p, "alpha_ecm50_uniform_pooled": a_e50_u_p,
           "delta_alpha_rho_pooled": round(abs(a_rho_u_p - a_rho_b_p), 4),
           "delta_alpha_ecm50_pooled": round(abs(a_e50_u_p - a_e50_b_p), 4),
           "verdict": bool(0.94 < a_td_u < 1.24 and
                           abs(a_rho_u_p - a_rho_b_p) <= 0.15 and
                           abs(a_e50_u_p - a_e50_b_p) <= 0.15)}
# H3 in common currency + wall-time, balanced, pooled OLS intercepts at same log2p
d_cc = fits["balanced/ecm50"]["c_pooled_ols_cc"] - fits["balanced/rho"]["c_pooled_ols_cc"]
w_ecm = float(np.mean([w for kk in (16, 20) for w in res[("balanced", kk)]["ecm50"]["walls"]]))
w_rho = float(np.mean([w for kk in (16, 20) for w in res[("balanced", kk)]["rho"]["walls"]]))
V["H3"] = {"c_ecm50_minus_c_rho_common_currency_bits": round(float(d_cc), 4),
           "threshold_log2_10": 3.32,
           "wall_ms_ecm50": round(w_ecm * 1e3, 3), "wall_ms_rho": round(w_rho * 1e3, 3),
           "wall_ratio": round(w_ecm / w_rho, 2),
           "verdict": bool(0 <= d_cc <= 3.32)}
OUT["verdicts"] = V
checkpoint()

print("\n=== HEADLINE (alpha,c) table ===")
print(f"{'arm/method':22s} {'a_pooled':>9s} {'c_pooled':>9s} {'a_cc':>7s} {'c_cc':>8s}")
for key, f in fits.items():
    print(f"{key:22s} {f['alpha_pooled_ols_native']:9.4f} {f['c_pooled_ols_native']:9.4f} "
          f"{f['alpha_pooled_ols_cc']:7.4f} {f['c_pooled_ols_cc']:8.4f}")
print(json.dumps({"headline_balanced": headline, "uniform": uni, "verdicts": V},
                 indent=1, default=str))
print("DONE", round(time.time() - T0, 1), "s")

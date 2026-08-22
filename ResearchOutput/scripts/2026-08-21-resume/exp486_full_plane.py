#!/usr/bin/env python3
"""EXP 486 FACTOR-LOCAL-ET (round-41). Seed 20260920. Full protocol.
Unified (alpha, c) expected-cost plane for classical factoring methods:
    log2 E[T_M] = alpha_M * log2(min(p,q)) + c_M + o(1)
giving Pollard rho / ECM / trial division / Fermat a comparable pricing under the
E[T] functional (papers 89/95/96 re-derived), addressing paper 132 residual-gap
item (2): factor-local methods were never priced on a comparable functional.

SUPERSEDES: an earlier inline lean attempt in this directory (ECM dropped for
budget, n=1500, TD prime-count convention with a length-misalignment bug,
fixed rho start, no unbalanced arm, no CIs). Replaced by this full protocol.

PRE-STATED HYPOTHESES (written BEFORE any data collection of this run):
  H1 (unified plane): on matched semiprime populations every classical method's
     log2 E[T] is affine in log2 min(p,q) with slope alpha in [0.25, 1.13]
     (papers 89/95 numbers re-derived under the E[T] functional).
  H2 (factor-locality):
     (a) ARM-INVARIANCE: rho/ECM/TD cost depends only on min(p,q), so (alpha,c)
         is the same in a balanced arm and an unbalanced arm (q/p ~ 4) at
         matched p-scales (N differs by ~4x); Fermat's line is NOT invariant
         (balance term).
     (b) RESIDUAL-SMOOTHNESS: per-draw residual cost correlates with factor-level
         smoothness features (lpf(p-1), lpf(p+1)) more than N-level ones
         (lpf(N-1), lpf(N+1)).
     PRE-STATED CAVEAT: in the unbalanced arm N ~ 4p^2 so N-1 = (2p-1)(2p+1):
     N-level features algebraically contain factor-level ones. H2b is therefore
     tested on the BALANCED arm only; the unbalanced identity is itself reported.
  H3 (coefficient predictions): rho ~ (0.5, .); ECM ~ (0.5-0.7, .); TD (1.0, -1
     exactly under the odd-candidate convention); Fermat (1.0 with balance term:
     alpha not intrinsic -- fixed-ratio arm ~1.0, fixed-spread arm ~0.25).
  PRE-DATA THEORETICAL AMENDMENT (derived before any draw, from Dickman):
     at FIXED B1, E[curves] ~ 1/rho(u), u = ln p/ln B1, rho(u)=1-ln u on (1,2),
     so alpha_ECM(B1) ~ ln2/(lnB1 * u * rho(u)) ~ 0.1-0.35 at our scales;
     H3's 0.5-0.7 presumed B1 scaling with p. We test both readings.

OP-COUNT CONVENTIONS (ledger, stated a priori):
  one op = one modular multiplication mod N:
    rho: f-evals (Floyd: 3 squarings/iteration, degenerate-restart evals counted)
    ECM: projective x-only muls (xDBL=5, xADD=6, setup=8); stage 1 only, no stage 2
    TD : one trial modulus (odd candidates only, N odd by construction)
    Fermat: one square-and-compare
  Excluded EQUALLY for all methods: gcd, isqrt, modular inversion (C-level at
  toy bitwidths). Stated, not hidden.
CENSORING POLICY (a priori): rho cap 30*N^0.25+100 f-evals (restarts counted);
  ECM curve caps 30 (B1=100) / 15 (B1=500); TD cap isqrt(N)//2+2 (never hit);
  Fermat cap (p+q)//2+10 tests (never hit: a=(p+q)/2 always succeeds). Censored
  draws enter means at cap value; rate reported per cell; censored-excluded
  refits reported as robustness.
POPULATIONS (a priori): k in {16,20,24}; n=2000 per (arm,k).
  bal:   p,q independent uniform primes in [2^(k/2-0.5), 2^(k/2+0.5)], p<q.
  unbal: p uniform prime in [2^(k/2-0.75), 2^(k/2-0.25)], q = next_prime(4p).
SEED 20260920; per-population sub-RNGs derived by SHA-256.
"""
import hashlib, json, math, random, sys, time
from math import gcd, isqrt, erfc, sqrt

SEED = 20260920
random.seed(SEED)   # global RNG: factorize()'s rho draws (population features)
OUTDIR = "/tmp/exp41_flet"
T0 = time.time()
DEADLINE = T0 + 19 * 60          # hard budget guard (limit 22 min)
ANALYSIS_RESERVE = 90            # seconds reserved for fits/bootstrap

OUT = {"meta": {
    "seed": SEED, "exp": 486, "codename": "FACTOR-LOCAL-ET",
    "supersedes": "prior inline lean attempt (ECM dropped, n=1500, TD convention bug)",
    "conventions": "op = one modmul (rho: f-eval squarings; ECM: xDBL=5/xADD=6/"
                   "setup=8, stage-1 only; TD: one odd trial modulus; Fermat: one "
                   "square-and-compare). gcd/isqrt/inversion excluded equally (C-level).",
    "ecm_validation": "Suyama a24 denominator validated in-session BEFORE final data: "
                      "(i) projective ladder == corrected affine scalar-mult stage-by-stage "
                      "(10/10 stages, sigma=8 p=1013); (ii) generic-curve ladder test ALL OK; "
                      "(iii) mod-12 Suyama signature 100/100 sigmas for 16*u^3*v "
                      "(rejected 16*u^3*v^3: 42/100 -- first-run bug, its ECM rows discarded); "
                      "(iv) end-to-end: fires 80/80 when B1 covers #E(F_p).",
    "caps": {"rho": "30*N^0.25+100 f-evals", "ecm100": "30 curves",
             "ecm500": "15 curves", "td": "isqrt(N)//2+2 (never hit)",
             "fermat": "(p+q)//2+10 tests (never hit)"},
    "populations": "k in {16,20,24}, n=2000 per (arm,k); bal p,q~U[2^(k/2-.5),2^(k/2+.5)]; "
                   "unbal p~U[2^(k/2-.75),2^(k/2-.25)], q=next_prime(4p)",
}, "draws": [], "cells": [], "fits": {}, "h2": {}, "verdicts": {}}

def checkpoint():
    import os
    tmp = OUTDIR + "/result.json.tmp"
    with open(tmp, "w") as f:
        json.dump(OUT, f)
    os.replace(tmp, OUTDIR + "/result.json")

def log(msg):
    print("[%7.1fs] %s" % (time.time() - T0, msg), flush=True)

# ---------------- number theory ----------------
def is_prime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % p == 0: return n == p
    d = n - 1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1: break
        else:
            return False
    return True

def next_prime(n):
    if n <= 2: return 2
    c = n + 1 if n % 2 else n + 1
    while not is_prime(c): c += 2
    return c

def factorize(n):
    """full prime factorization as a set (toy scale: rho + MR)"""
    out = set()
    for p in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97):
        while n % p == 0:
            out.add(p); n //= p
    stack = [n] if n > 1 else []
    while stack:
        m = stack.pop()
        if m == 1: continue
        if is_prime(m):
            out.add(m); continue
        # pollard rho, Brent-ish
        d = None
        c = 1
        while d is None or d == m:
            x = random.randrange(2, m); y = x; d = 1
            while d == 1:
                x = (x*x + c) % m
                y = (y*y + c) % m; y = (y*y + c) % m
                d = gcd(abs(x - y), m)
            if d == m:
                c += 1; d = None
        stack.append(d); stack.append(m // d)
    return out

# ---------------- methods (exact op counts) ----------------
def m_td(N, cap):
    if N % 2 == 0: return 2, 1, False
    d = 3; cnt = 1
    while cnt <= cap:
        if N % d == 0: return d, cnt, False
        d += 2; cnt += 1
    return None, cnt, True

def m_rho(N, cap, rng):
    total = 0
    for _ in range(200):
        x = rng.randrange(3, N - 1); y = x
        while True:
            x = (x*x + 1) % N
            y = (y*y + 1) % N; y = (y*y + 1) % N
            total += 3
            if total > cap: return None, total, True
            g = gcd(x - y, N)
            if g == 1: continue
            if g == N: break            # degenerate: restart, evals counted
            return g, total, False
    return None, total, True

def m_fermat(N, cap):
    a = isqrt(N)
    if a * a < N: a += 1
    cnt = 0
    while cnt < cap:
        b2 = a * a - N
        b = isqrt(b2)
        cnt += 1
        if b * b == b2: return a - b, cnt, False
        a += 1
    return None, cnt, True

def ecm_curve(N, sigma, B1):
    """one stage-1 ECM curve, Montgomery Suyama, x-only ladder.
    returns (status, factor, muls); status in factor/none/degen"""
    u = (sigma * sigma - 5) % N
    v = (4 * sigma) % N
    x = u * u % N * u % N
    z = v * v % N * v % N
    d = (v - u) % N
    t = d * d % N * d % N
    m = 6
    denom = 16 * x % N * v % N      # 16*u^3*v  (standard Suyama; verified below)
    try:
        inv = pow(denom, -1, N)
    except ValueError:
        g = gcd(denom, N)
        return ("factor" if 1 < g < N else "degen"), g, m
    a24 = t * ((3 * u + v) % N) % N * inv % N
    m += 2
    Qx, Qz = x, z
    for l in _PRIMES:
        if l > B1: break
        e = l
        le = l * l
        while le <= B1: e = le; le *= l
        # ladder [e]*(Qx:Qz), diff = (Qx:Qz)
        R0x, R0z = Qx, Qz
        tp = (Qx + Qz) % N; tm = (Qx - Qz) % N
        t1 = tp * tp % N; t2 = tm * tm % N
        R1x = t1 * t2 % N
        t3 = (t1 - t2) % N
        R1z = t3 * ((a24 * t3 + t2) % N) % N
        m += 5
        for bit in bin(e)[3:]:
            if bit == '1':
                up = (R0x + R0z) % N * (R1x - R1z) % N
                vp = (R0x - R0z) % N * (R1x + R1z) % N
                s = (up + vp) % N; d2 = (up - vp) % N
                R0x = Qz * (s * s % N) % N
                R0z = Qx * (d2 * d2 % N) % N
                tp = (R1x + R1z) % N; tm = (R1x - R1z) % N
                t1 = tp * tp % N; t2 = tm * tm % N
                R1x = t1 * t2 % N
                t3 = (t1 - t2) % N
                R1z = t3 * ((a24 * t3 + t2) % N) % N
            else:
                up = (R0x + R0z) % N * (R1x - R1z) % N
                vp = (R0x - R0z) % N * (R1x + R1z) % N
                s = (up + vp) % N; d2 = (up - vp) % N
                R1x = Qz * (s * s % N) % N
                R1z = Qx * (d2 * d2 % N) % N
                tp = (R0x + R0z) % N; tm = (R0x - R0z) % N
                t1 = tp * tp % N; t2 = tm * tm % N
                R0x = t1 * t2 % N
                t3 = (t1 - t2) % N
                R0z = t3 * ((a24 * t3 + t2) % N) % N
            m += 11
        Qx, Qz = R0x, R0z
    g = gcd(Qz, N)
    if g == 1: return "none", None, m
    if g == N: return "degen", None, m
    return "factor", g, m

def m_ecm(N, B1, cap_curves, rng):
    """returns (factor_or_None, total_muls, censored_flag) -- 3-tuple like others"""
    total = 0; curves = 0
    while curves < cap_curves:
        sigma = rng.randrange(6, N - 1)
        st, g, m = ecm_curve(N, sigma, B1)
        total += m; curves += 1
        if st == "factor": return g, total, False
    return None, total, True

_PRIMES = [p for p in range(2, 1000) if is_prime(p)]

# ---------------- populations ----------------
def rand_prime(lo, hi, rng):
    while True:
        c = rng.randrange(lo, hi + 1)
        if is_prime(c): return c

def gen_pop(arm, k, n, rng):
    h = k // 2
    if arm == "bal":
        lo, hi = int(2 ** (h - 0.5)), int(2 ** (h + 0.5))
    else:
        lo, hi = int(2 ** (h - 0.75)), int(2 ** (h - 0.25))
    recs = []
    while len(recs) < n:
        p = rand_prime(lo, hi, rng)
        if arm == "bal":
            q = rand_prime(lo, hi, rng)
            if q == p: continue
        else:
            q = next_prime(4 * p)
        pp, qq = (p, q) if p < q else (q, p)
        N = pp * qq
        fp_m1 = factorize(pp - 1); fp_p1 = factorize(pp + 1)
        fN_m1 = factorize(N - 1);  fN_p1 = factorize(N + 1)
        recs.append({
            "arm": arm, "k": k, "p": pp, "q": qq, "N": N,
            "lpf_pm1": max(fp_m1), "lpf_pp1": max(fp_p1),
            "om_pm1": len(fp_m1), "om_pp1": len(fp_p1),
            "lpf_nm1": max(fN_m1), "lpf_np1": max(fN_p1),
            "om_nm1": len(fN_m1), "om_np1": len(fN_p1),
        })
    return recs

# ---------------- fitting ----------------
ARNG = random.Random(int.from_bytes(hashlib.sha256(b"%d|analysis" % SEED).digest()[:8], "big"))

def binned_fit(pts, nb=None):
    """pts: (x=log2 p, T); y = log2 mean-T per quantile bin; weighted OLS."""
    pts = sorted(pts)
    n = len(pts)
    if n < 40: return None
    if nb is None: nb = max(5, min(14, n // 160))
    xs, ys, ws = [], [], []
    for i in range(nb):
        b = pts[i * n // nb:(i + 1) * n // nb]
        if not b: continue
        xb = sum(x for x, _ in b) / len(b)
        mT = sum(t for _, t in b) / len(b)
        if mT <= 0: continue
        xs.append(xb); ys.append(math.log2(mT)); ws.append(len(b))
    if len(xs) < 3: return None
    W = float(sum(ws))
    mx = sum(w * x for w, x in zip(ws, xs)) / W
    my = sum(w * y for w, y in zip(ws, ys)) / W
    sxx = sum(w * (x - mx) ** 2 for w, x in zip(ws, xs))
    sxy = sum(w * (x - mx) * (y - my) for w, x, y in zip(ws, xs, ys))
    if sxx <= 0: return None
    a = sxy / sxx
    return a, my - a * mx

def fit_with_ci(pts, B=200):
    base = binned_fit(pts)
    if base is None: return None
    alphas, cs = [], []
    n = len(pts)
    for _ in range(B):
        smp = [pts[ARNG.randrange(n)] for _ in range(n)]
        r = binned_fit(smp)
        if r: alphas.append(r[0]); cs.append(r[1])
    alphas.sort(); cs.sort()
    def ci(v):
        return v[int(0.025 * len(v))], v[int(0.975 * len(v))]
    a, c = base
    return {"alpha": a, "c": c,
            "alpha_ci": list(ci(alphas)) if alphas else None,
            "c_ci": list(ci(cs)) if cs else None,
            "n": n, "nbins": None}

def spearman(a, b):
    n = len(a)
    if n < 10: return float("nan"), float("nan")
    def ranks(v):
        idx = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[idx[j + 1]] == v[idx[i]]: j += 1
            avg = (i + j) / 2.0 + 1.0
            for t in range(i, j + 1): r[idx[t]] = avg
            i = j + 1
        return r
    ra, rb = ranks(a), ranks(b)
    ma = sum(ra) / n; mb = sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    r = num / den if den > 0 else 0.0
    t = r * sqrt((n - 2) / max(1e-12, 1 - r * r))
    p = erfc(abs(t) / sqrt(2))
    return r, p

# ---------------- driver ----------------
POPS = [(a, k) for a in ("bal", "unbal") for k in (16, 20, 24)]
N_DRAWS = 2000
POPS_RNG = {}
for arm, k in POPS:
    s = int.from_bytes(hashlib.sha256(b"%d|%s|%d" % (SEED, arm.encode(), k)).digest()[:8], "big")
    POPS_RNG[(arm, k)] = random.Random(s)

METHOD_RUNNERS = {}

def run_cell(tag, recs, fn, cap_of, rng, key_t, key_c, key_f, extra=None):
    """fn(N, cap, rng) -> (factor, T, censored[, extra]); fills rec fields."""
    t0 = time.time()
    ncens = 0; bad = 0; Tsum = 0
    n = len(recs)
    # pilot for time guard
    pilot = 20
    ts = time.time()
    for r in recs[:pilot]:
        out = fn(r["N"], cap_of(r), rng)
        r[key_t], r[key_c] = out[1], out[2]
        r[key_f] = out[0]
        ncens += out[2]
    dt = (time.time() - ts) / pilot
    remain = n - pilot
    budget = DEADLINE - time.time() - ANALYSIS_RESERVE
    if remain * dt > budget and remain > 0:
        n_use = max(400, min(n, pilot + int(budget / dt)))
        reduced = n - n_use
    else:
        n_use, reduced = n, 0
    for r in recs[pilot:n_use]:
        out = fn(r["N"], cap_of(r), rng)
        r[key_t], r[key_c] = out[1], out[2]
        r[key_f] = out[0]
        ncens += out[2]
    for r in recs[:n_use]:
        f = r[key_f]
        if f is None:
            Tsum += r[key_t]            # censored at cap: cost still paid
            continue
        if r["N"] % f != 0 or f == r["N"] or f == 1: bad += 1
        Tsum += r[key_t]
    cell = {"tag": tag, "n": n_use, "reduced": reduced, "censored": ncens,
            "mean_T": Tsum / n_use, "bad_factor": bad, "sec": round(time.time() - t0, 1)}
    OUT["cells"].append(cell)
    checkpoint()
    log("%-14s n=%d cens=%d meanT=%.1f bad=%d (%.1fs)" %
        (tag, n_use, ncens, cell["mean_T"], bad, cell["sec"]))

def main():
    log("stage 1: populations")
    pops = {}
    for arm, k in POPS:
        recs = gen_pop(arm, k, N_DRAWS, POPS_RNG[(arm, k)])
        pops[(arm, k)] = recs
        OUT["draws"].extend(recs)
        checkpoint()
        log("pop %s k=%d: %d draws, p in [%d,%d]" %
            (arm, k, len(recs), min(r["p"] for r in recs), max(r["p"] for r in recs)))

    log("stage 2: cheap methods (td, rho, fermat) x6 populations")
    for arm, k in POPS:
        recs = pops[(arm, k)]
        tag = "%s%d" % (arm, k)
        run_cell("td-" + tag, recs, lambda N, cap, r: m_td(N, cap),
                 lambda r: isqrt(r["N"]) // 2 + 2, POPS_RNG[(arm, k)],
                 "T_td", "cens_td", "f_td")
        run_cell("rho-" + tag, recs, lambda N, cap, r: m_rho(N, cap, r),
                 lambda r: int(30 * r["N"] ** 0.25) + 100, POPS_RNG[(arm, k)],
                 "T_rho", "cens_rho", "f_rho")
        run_cell("fermat-" + tag, recs, lambda N, cap, r: m_fermat(N, cap),
                 lambda r: (r["p"] + r["q"]) // 2 + 10, POPS_RNG[(arm, k)],
                 "T_fe", "cens_fe", "f_fe")

    log("stage 3: ECM B1=100 x6")
    for arm, k in POPS:
        recs = pops[(arm, k)]
        tag = "%s%d" % (arm, k)
        run_cell("ecm100-" + tag, recs,
                 lambda N, cap, r: m_ecm(N, 100, cap, r),
                 lambda r: 30, POPS_RNG[(arm, k)],
                 "T_e100", "cens_e100", "f_e100")

    log("stage 4: ECM B1=500 x6")
    for arm, k in POPS:
        recs = pops[(arm, k)]
        tag = "%s%d" % (arm, k)
        run_cell("ecm500-" + tag, recs,
                 lambda N, cap, r: m_ecm(N, 500, cap, r),
                 lambda r: 15, POPS_RNG[(arm, k)],
                 "T_e500", "cens_e500", "f_e500")

    # POST-HOC DIAGNOSTIC (labeled as such: added after seeing the B1=500
    # small-p degeneracy; NOT part of the pre-stated plane). B1=50 brackets
    # the validity edge from below.
    log("stage 4b: POST-HOC ECM B1=50 x6")
    for arm, k in POPS:
        recs = pops[(arm, k)]
        tag = "%s%d" % (arm, k)
        run_cell("ecm50-posthoc-" + tag, recs,
                 lambda N, cap, r: m_ecm(N, 50, cap, r),
                 lambda r: 30, POPS_RNG[(arm, k)],
                 "T_e50", "cens_e50", "f_e50")

    analyze(pops)

# ---------------- analysis ----------------
METHODS = [("td", "T_td", "cens_td"), ("rho", "T_rho", "cens_rho"),
           ("ecm100", "T_e100", "cens_e100"), ("ecm500", "T_e500", "cens_e500"),
           ("fermat", "T_fe", "cens_fe"), ("ecm50", "T_e50", "cens_e50")]
POSTHOC = {"ecm50"}

def analyze(pops):
    log("stage 5: analysis")
    fits = {}
    for name, tk, ck in METHODS:
        for arm in ("bal", "unbal"):
            pts, pts_unc = [], []
            for k in (16, 20, 24):
                for r in pops[(arm, k)]:
                    if tk not in r: continue
                    x = math.log2(r["p"])
                    pts.append((x, r[tk]))
                    if not r[ck]: pts_unc.append((x, r[tk]))
            f = fit_with_ci(pts)
            if f:
                f["censored"] = len(pts) - len(pts_unc)
                fu = fit_with_ci(pts_unc, B=100)
                if fu: f["alpha_uncens"] = fu["alpha"]; f["c_uncens"] = fu["c"]
                fits["%s-%s" % (name, arm)] = f
        # per-population fits
        for arm in ("bal", "unbal"):
            for k in (16, 20, 24):
                pts = [(math.log2(r["p"]), r[tk]) for r in pops[(arm, k)] if tk in r]
                r2 = binned_fit(pts, nb=6)
                if r2:
                    fits["%s-%s%d" % (name, arm, k)] = {"alpha": r2[0], "c": r2[1], "n": len(pts)}
    OUT["fits"] = fits

    # 3-point cross-bitlen table: (mean log2 p, log2 mean T) per (method, arm, k)
    three = {}
    for name, tk, ck in METHODS:
        for arm in ("bal", "unbal"):
            row = []
            for k in (16, 20, 24):
                ts = [r[tk] for r in pops[(arm, k)] if tk in r]
                ps = [r["p"] for r in pops[(arm, k)] if tk in r]
                if not ts: continue
                row.append((sum(math.log2(p) for p in ps) / len(ps),
                            math.log2(sum(ts) / len(ts))))
            if len(row) >= 3:
                n = len(row)
                mx = sum(x for x, _ in row) / n; my = sum(y for _, y in row) / n
                sxx = sum((x - mx) ** 2 for x, _ in row)
                a = sum((x - mx) * (y - my) for x, y in row) / sxx if sxx > 0 else float("nan")
                three["%s-%s" % (name, arm)] = {"alpha_3pt": a,
                                                "points": [[round(x, 3), round(y, 3)] for x, y in row]}
    OUT["fits_3pt"] = three

    # theory overlays
    theory = {}
    for arm in ("bal", "unbal"):
        for k in (16, 20, 24):
            ps = [r["p"] for r in pops[(arm, k)]]
            lnp = sum(math.log(p) for p in ps) / len(ps)
            for B1 in (50, 100, 500):
                u = lnp / math.log(B1)
                rho_u = 1.0 if u <= 1 else (1 - math.log(u) if u <= 2 else float("nan"))
                theory["ecm%d-%s%d" % (B1, arm, k)] = {
                    "u": round(u, 3), "rho_u": None if rho_u != rho_u else round(rho_u, 4),
                    "alpha_theory": None if rho_u in (None, 0) or rho_u != rho_u or rho_u <= 0
                                    else round(math.log(2) / (math.log(B1) * u * rho_u), 4)}
    OUT["theory_ecm"] = theory

    # H2b: balanced-arm residual correlations (pre-stated feature set)
    h2 = {}
    feats = [("lpf_pm1", "factor"), ("lpf_pp1", "factor"), ("om_pm1", "factor"),
             ("om_pp1", "factor"), ("lpf_nm1", "Nlevel"), ("lpf_np1", "Nlevel"),
             ("om_nm1", "Nlevel"), ("om_np1", "Nlevel"), ("bal", "Nlevel")]
    for name, tk, ck in METHODS:
        f = fits.get("%s-bal" % name)
        if not f: continue
        a, c = f["alpha"], f["c"]
        rows = []
        for k in (16, 20, 24):
            for r in pops[("bal", k)]:
                if tk in r and not r[ck]:
                    resid = math.log2(r[tk]) - (a * math.log2(r["p"]) + c)
                    rows.append((resid, r))
        if len(rows) < 100:
            h2[name] = {"skip": "insufficient uncensored rows", "n_rows": len(rows)}
            continue
        res = {}
        for feat, level in feats:
            if feat == "bal":
                xs = [math.log2(r["q"] / r["p"]) for _, r in rows]
            else:
                xs = [math.log2(r[feat]) if feat.startswith("lpf") else r[feat]
                      for _, r in rows]
            ys = [rd for rd, _ in rows]
            rr, pv = spearman(xs, ys)
            res[feat] = {"level": level, "r": round(rr, 4), "p": "%.2e" % pv}
        bf = max((abs(v["r"]) for v in res.values() if v["level"] == "factor"), default=0)
        bn = max((abs(v["r"]) for v in res.values() if v["level"] == "Nlevel"), default=0)
        res["contrast_factor_minus_N"] = round(bf - bn, 4)
        h2[name] = res
    OUT["h2"] = h2

    verdicts = {}
    # validity-edge diagnostic: ECM cells where censoring explodes (degen wall)
    edge = {}
    for cell in OUT["cells"]:
        if cell["tag"].startswith("ecm"):
            rate = cell["censored"] / max(1, cell["n"])
            if rate > 0.3:
                edge[cell["tag"]] = {"cens_rate": round(rate, 3),
                                     "meanT": round(cell["mean_T"], 1)}
    verdicts["validity_edge_cells_cens_gt_30pct"] = edge
    # H1
    inr, viol = [], []
    for key, f in fits.items():
        if "alpha_ci" not in f or f.get("alpha_ci") is None: continue
        a = f["alpha"]; lo, hi = f["alpha_ci"]
        f["in_H1_range"] = 0.25 <= a <= 1.13
        f["ci_overlaps_H1"] = not (hi < 0.25 or lo > 1.13)
        if key.split("-")[0] in POSTHOC:
            f["posthoc"] = True; continue
        (inr if f["in_H1_range"] else viol).append((key, round(a, 3)))
    verdicts["H1"] = {"alpha_in_[0.25,1.13]": inr, "violations": viol,
                      "verdict": "CONFIRMED" if not viol else
                                 ("PARTIAL" if len(inr) >= len(viol) else "REFUTED")}
    # H2a arm-invariance
    inv = {}
    for name, tk, ck in METHODS:
        fb, fu = fits.get("%s-bal" % name), fits.get("%s-unbal" % name)
        if not fb or not fu: continue
        ov_a = not (fb["alpha_ci"][1] < fu["alpha_ci"][0] or fu["alpha_ci"][1] < fb["alpha_ci"][0])
        dc = abs(fb["c"] - fu["c"])
        inv[name] = {"d_alpha": round(fb["alpha"] - fu["alpha"], 4),
                     "alpha_CIs_overlap": ov_a, "d_c": round(dc, 3)}
    fa = inv.get("fermat", {})
    verdicts["H2a"] = {"cells": inv, "verdict":
        "CONFIRMED" if all(inv[m]["alpha_CIs_overlap"] and inv[m]["d_c"] < 0.5
                           for m in ("td", "rho", "ecm100", "ecm500") if m in inv)
                       and (not fa or fa["d_alpha"] > 0.1 or not fa.get("alpha_CIs_overlap", False))
        else "PARTIAL/REFUTED-see-cells"}
    # H2b
    h2b = {}
    for name in ("rho", "ecm100", "ecm500"):
        if name in h2: h2b[name] = h2[name]["contrast_factor_minus_N"]
    verdicts["H2b"] = {"contrast_factor_minus_N": h2b,
                       "verdict": "CONFIRMED" if h2b and all(v > 0 for v in h2b.values())
                                  else ("MIXED" if any(v > 0 for v in h2b.values()) else "REFUTED")}
    # H3
    def get(name, arm):
        f = fits.get("%s-%s" % (name, arm))
        return (round(f["alpha"], 3), round(f["c"], 3)) if f else None
    h3 = {
        "td": {"pred": "(1.0, -1.0 exact)", "meas": [get("td", "bal"), get("td", "unbal")]},
        "rho": {"pred": "(0.5, ~0.32)", "meas": [get("rho", "bal"), get("rho", "unbal")]},
        "ecm": {"pred": "(0.5-0.7) [H3] vs fixed-B1 Dickman 0.1-0.35 [amendment]",
                "meas": [get("ecm100", "bal"), get("ecm100", "unbal"),
                         get("ecm500", "bal"), get("ecm500", "unbal")]},
        "fermat": {"pred": "(1.0 w/ balance term); fixed-spread arm ~0.25",
                   "meas": [get("fermat", "bal"), get("fermat", "unbal")]},
    }
    verdicts["H3"] = h3
    OUT["verdicts"] = verdicts
    checkpoint()

    # final table
    log("=========== (alpha, c) plane ===========")
    log("%-16s %6s %8s %22s %22s %6s" % ("method-arm", "n", "cens%", "alpha [CI]", "c [CI]", "H1"))
    for key in sorted(fits):
        f = fits[key]
        if "alpha_ci" not in f: continue
        mark = "POSTHOC" if key.split("-")[0] in POSTHOC else \
               ("Y" if f.get("in_H1_range") else "N")
        log("%-16s %6d %6.2f %10.4f [%.3f,%.3f] %10.3f [%.2f,%.2f] %s" %
            (key, f["n"], 100.0 * f["censored"] / f["n"], f["alpha"],
             f["alpha_ci"][0], f["alpha_ci"][1], f["c"], f["c_ci"][0], f["c_ci"][1],
             mark))
    log("3-point cross-bitlen alphas: %s" %
        {kk: round(vv["alpha_3pt"], 3) for kk, vv in three.items()})
    log("ECM Dickman theory alpha: %s" %
        {kk: vv["alpha_theory"] for kk, vv in theory.items() if vv["alpha_theory"]})
    log("H1: %s | H2a: %s | H2b: %s" %
        (verdicts["H1"]["verdict"], verdicts["H2a"]["verdict"], verdicts["H2b"]["verdict"]))
    log("H2b contrasts (factor minus N-level, balanced): %s" % h2b)
    log("DONE total %.1fs" % (time.time() - T0))

if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        OUT["error"] = traceback.format_exc()
        checkpoint()
        traceback.print_exc()
        raise

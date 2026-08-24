#!/usr/bin/env python3
"""
exp562 SCALE-SMOOTHNESS-DEVIATION (factoring loop, 2026-08-23, seed 20260827)

Question: does x^2 - N deviate from size-matched randomness in B-smoothness at
large u = log(v)/log(B), u in {5,6,7,8}?  Paper 130 found ensemble equality
(ratios 0.88-0.91 attributed to a SHARED finite-x Dickman correction) at scales
2^32-2^44, i.e. u < 4.75.  Here we probe u in [5,9) where the L_N[1/3] sieving
regime lives.

Design:
  * N: semiprimes, bitlen stratified per bin inside 60..80 (seed 20260827).
  * Candidates: v_j = (isqrt(N)+j)^2 - N, j >= 1, sampled so v lands exactly in
    the bin [B^w, B^(w+1)), B = 1000.  Quadratic-character cap j <= 3s
    (x <= 4 sqrt(N)); with N <= 2^80 this truncates the top of the u=8 bin
    (achieved ranges reported empirically).
  * Controls: uniform random integers matched EXACTLY to candidates on
    (bitlen, mantissa-octant within the dyadic class) -- identical histogram,
    generated per run from the candidate codes.  Same tester object, shared
    code path.
  * Tester: gcd-chain against the primorial of primes <= 1000 (NO trial
    division anywhere -- avoids the known early-exit bug family).  Validated
    against an exhaustive strip-all-primes-with-multiplicity reference (zero
    early exits) on adversarial + random + REAL quadratic candidates.
    Assert zero mismatch and >=200 ground-truth cases.
  * Mean analysis: r(u) = P(cand smooth)/P(ctrl smooth) per bin, cluster
    (per-N) bootstrap CIs; trend = bootstrap OLS slope of log r vs u.
  * Second moment: per-N smooth-count dispersion D = Var/Mean vs the Poisson /
    random-model prediction D ~= 1, candidates vs paired controls (paper 139
    QR-variance persistence test).  Plus per-N smooth-rate vs QR-fraction of
    primes <= 1000 (Spearman with permutation p).

Pre-stated verdicts:
  DEVIATION       : trend significant AND some u>=6 r-CI excludes 1.
  RANDOM-AT-SCALE : all u>=6 CIs cover 1 -> report tightest upper bound on
                    |r-1|.
Artifacts: exp562_result.json, exp562_scale_smoothness.log (same dir).
"""

import argparse
import array
import hashlib
import json
import logging
import math
import os
import queue as queue_mod
import random
import sys
import time
from collections import Counter, defaultdict

import numpy as np

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
EXP_ID = "562"
CODENAME = "SCALE-SMOOTHNESS-DEVIATION"
DEFAULT_SEED = 20260827
B = 1000
LOG_B = math.log(B)
BIN_WS = (5, 6, 7, 8)          # bin w covers v in [B^w, B^(w+1))

# N-bitlen strata per bin (wide j-windows; u=8 needs the top of the N range).
STRATA = {5: (66, 74), 6: (71, 78), 7: (76, 80), 8: (79, 80)}

J_CAP_MULT = 3                 # j <= 3*s  =>  x <= 4 sqrt(N)
MANT_OCT = 8                   # mantissa sub-buckets per dyadic class

MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)  # exact < 3.317e24

# Allocation priors for rho(u) (control smoothness rate guesses); NOT results.
RHO_PRIOR = {5: 1.0e-3, 6: 1.3e-4, 7: 1.6e-5, 8: 3.0e-6}

# Dickman rho at integer u (published small-u values), context only.
DICKMAN = {1: 1.0, 2: 0.3066, 3: 0.04861, 4: 0.004911, 5: 3.547e-4,
           6: 1.9650e-5, 7: 8.7455e-7, 8: 3.2329e-8, 9: 1.0107e-9}


def sieve_primes(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if s[p]:
            s[p * p::p] = False
    return [int(i) for i in np.nonzero(s)[0]]


PRIMES = sieve_primes(B)
PM = 1
for _p in PRIMES:
    PM *= _p                       # primorial of ALL primes <= B
ODD_PRIMES = [p for p in PRIMES if p != 2]

# ---------------------------------------------------------------------------
# primality / semiprimes
# ---------------------------------------------------------------------------

def is_prime_det(n):
    if n < 2:
        return False
    for p in MR_BASES:
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in MR_BASES:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def rand_prime(bits, rng):
    while True:
        c = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime_det(c):
            return c


def gen_semiprime(bits, rng):
    """N = p*q with exactly two prime factors and bit_length(N)==bits."""
    bp = bits // 2
    bq = bits - bp
    while True:
        p = rand_prime(bp, rng)
        q = rand_prime(bq, rng)
        if p == q:
            continue
        n = p * q
        if n.bit_length() == bits:
            return n


def legendre(a, p):
    ls = pow(a % p, (p - 1) // 2, p)
    if ls == 1:
        return 1
    if ls == p - 1:
        return -1
    return 0


# ---------------------------------------------------------------------------
# smoothness testers
# ---------------------------------------------------------------------------

def make_gcd_chain_tester():
    """Primary tester: repeated gcd against the primorial (no trial division).

    v is B-smooth  <=>  iteratively dividing out gcd(v, PM) leaves 1.
    """
    pm = PM
    gcd = math.gcd

    def is_smooth(v):
        g = gcd(v, pm)
        while g != 1:
            v //= g
            g = gcd(v, pm)
        return v == 1

    return is_smooth


IS_SMOOTH = make_gcd_chain_tester()


def smooth_exhaustive(v):
    """Ground truth: strip EVERY prime <= B exhaustively (with multiplicity),
    no early exits anywhere.  v is B-smooth iff nothing survives."""
    r = v
    for p in PRIMES:
        while r % p == 0:
            r //= p
    return r == 1


# ---------------------------------------------------------------------------
# validation pipeline (asserted)
# ---------------------------------------------------------------------------

def run_validation(rng, n_random=260, n_real=140):
    cases, expected = [], []
    adv = [1, 2, 2 ** 40, 2 ** 79, 3 ** 25,
           997, 998, 999, 1000, 1001, 1009, 1010, 1011,
           997 ** 2, 997 ** 3, 1009 * 997, 1009 ** 2, 997 * 998 * 999,
           2 * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29 * 31 * 37,
           PRIMES[-1], PRIMES[-1] ** 2, (PRIMES[-1] ** 2) * 4,
           1009 ** 2 * 997, 2 ** 30 * 3 ** 20 * 997 ** 2]
    for v in adv:
        cases.append(v)
        expected.append(smooth_exhaustive(v))
    for _ in range(n_random):
        v = rng.randrange(10 ** 9, 10 ** 15)
        cases.append(v)
        expected.append(smooth_exhaustive(v))
    # real quadratic candidates from freshly generated semiprimes (all bins)
    n_re = 0
    for w in BIN_WS:
        lo, hi = STRATA[w]
        for _ in range(max(1, n_real // len(BIN_WS))):
            bits = rng.randint(lo, hi)
            N = gen_semiprime(bits, rng)
            s = math.isqrt(N)
            x = math.isqrt(N + B ** w)
            if x * x < N + B ** w:
                x += 1
            j0 = max(1, x - s)
            vv = (s + j0) * (s + j0) - N
            for _ in range(4):
                if vv <= 0:
                    break
                cases.append(vv)
                expected.append(smooth_exhaustive(vv))
                n_re += 1
                vv = vv + 2 * (s + j0) + 1
                j0 += 1
    mismatches = [(v, IS_SMOOTH(v), e) for v, e in zip(cases, expected)
                  if IS_SMOOTH(v) != e]
    return {
        "n_cases": len(cases),
        "n_adversarial": len(adv),
        "n_random": n_random,
        "n_real_quadratic": n_re,
        "mismatches": len(mismatches),
        "mismatch_examples": mismatches[:5],
        "ok": len(mismatches) == 0,
        "tester": "gcd-chain vs primorial(primes<=1000)",
        "reference": "exhaustive strip of all primes<=1000, zero early exits",
        "shared_code_path_both_populations": True,
    }


# ---------------------------------------------------------------------------
# bin pools: semiprimes + disjoint j-windows
# ---------------------------------------------------------------------------

class NEntry:
    __slots__ = ("nid", "N", "s", "j_lo", "j_hi",
                 "starts0", "starts1", "used0", "used1",
                 "qr_frac", "qr_w")

    def __init__(self, nid, N, w):
        self.nid = nid
        self.N = N
        self.s = math.isqrt(N)
        t_low, t_high = B ** w, B ** (w + 1)
        x = math.isqrt(N + t_low)
        if x * x < N + t_low:
            x += 1
        self.j_lo = max(1, x - self.s)
        x2 = math.isqrt(N + t_high - 1)
        self.j_hi = min(x2 - self.s, J_CAP_MULT * self.s)
        # phase-split window state: half 0 = calibration, half 1 = measurement
        self.starts0 = self.starts1 = None
        self.used0 = self.used1 = None
        nqr = 0
        wnum = 0.0
        wden = 0.0
        for p in ODD_PRIMES:
            if legendre(N, p) == 1:
                nqr += 1
                wnum += 2.0 / p
            wden += 1.0 / p
        self.qr_frac = nqr / len(ODD_PRIMES)
        self.qr_w = wnum / wden if wden > 0 else 0.0

    def feasible(self, G):
        return self.j_hi - self.j_lo + 1 >= 4 * G


def build_pool(w, count, rng, G):
    lo, hi = STRATA[w]
    pool, tries = [], 0
    while len(pool) < count and tries < count * 60:
        tries += 1
        bits = rng.randint(lo, hi)
        N = gen_semiprime(bits, rng)
        e = NEntry(len(pool) + w * 100000, N, w)
        if e.feasible(G):
            pool.append(e)
    return pool


def next_window(e: NEntry, G, rng, half):
    """Fresh window start (disjoint, gap-spaced) within phase-half `half`,
    or None when that half is exhausted."""
    step = 2 * G                       # run of G + gap of G
    nblocks = (e.j_hi - e.j_lo - G + 2) // step
    if nblocks <= 0:
        return None
    b_lo = (nblocks * half) // 2
    b_hi = (nblocks * (half + 1)) // 2
    nb = b_hi - b_lo
    if nb <= 0:
        return None
    deck = e.starts0 if half == 0 else e.starts1
    used = e.used0 if half == 0 else e.used1
    if nb <= 4096:
        # narrow half-window: shuffle-once deck, exact disjointness
        if deck is None:
            deck = [e.j_lo + (b_lo + k) * step for k in range(nb)]
            rng.shuffle(deck)
            if half == 0:
                e.starts0 = deck
            else:
                e.starts1 = deck
        if not deck:
            return None
        return deck.pop()
    # wide half-window: rejection-sample block ids (collisions negligible)
    if used is None:
        used = set()
        if half == 0:
            e.used0 = used
        else:
            e.used1 = used
    for _ in range(64):
        bid = b_lo + rng.randrange(nb)
        if bid not in used:
            used.add(bid)
            return e.j_lo + bid * step
    return None


# ---------------------------------------------------------------------------
# worker: execute one run (G candidates + G matched controls)
# ---------------------------------------------------------------------------

def exec_run(spec):
    (w, nid, N, s, j0, G, ctrl_seed) = spec
    is_smooth = IS_SMOOTH
    t_high = B ** (w + 1)
    x = s + j0
    v = x * x - N
    if v <= 0:
        return (w, nid, None, 0, 0, 0, b"", b"", b"", b"", 0.0, 0.0)
    bls = bytearray(G)
    mbs = bytearray(G)
    cf = bytearray(G)
    kf = bytearray(G)
    kc = 0
    xmaxos = 0.0
    usum = 0.0
    n = 0
    inv_log_b = 1.0 / LOG_B
    for t in range(G):
        if v >= t_high:
            break
        bl = v.bit_length()
        mb = ((v - (1 << (bl - 1))) * MANT_OCT) >> (bl - 1)
        if mb >= MANT_OCT:
            mb = MANT_OCT - 1
        if is_smooth(v):
            kc += 1
            cf[t] = 1
        bls[t] = bl - 40
        mbs[t] = mb
        xs = x / s
        if xs > xmaxos:
            xmaxos = xs
        usum += math.log(v) * inv_log_b
        n += 1
        v += 2 * x + 1
        x += 1
    # controls: exact (bitlen, mantissa-octant) histogram match
    rng = random.Random(ctrl_seed)
    kctrl = 0
    for t in range(n):
        bl = bls[t] + 40
        mb = mbs[t]
        half = 1 << (bl - 1)
        step = half // MANT_OCT
        lo_c = half + step * mb
        hi_c = half + step * (mb + 1) if mb < MANT_OCT - 1 else (1 << bl)
        if is_smooth(rng.randrange(lo_c, hi_c)):
            kctrl += 1
            kf[t] = 1
    mean_u = usum / n if n else 0.0
    hb = int(math.floor(2.0 * mean_u)) if n else None
    return (w, nid, hb, n, kc, kctrl, bytes(bls[:n]), bytes(mbs[:n]),
            bytes(cf[:n]), bytes(kf[:n]), xmaxos, mean_u)


def exec_unit(unit):
    return [exec_run(sp) for sp in unit]


def ctrl_seed_for(master_seed, w, nid, wi):
    h = hashlib.blake2b(f"{master_seed}:{w}:{nid}:{wi}".encode(),
                        digest_size=8).digest()
    return int.from_bytes(h, "big")


# ---------------------------------------------------------------------------
# analysis helpers
# ---------------------------------------------------------------------------

def agg_by_n(rr):
    """rr: per-bin record-dict of arrays -> {nid: [n,kc,kctrl]}"""
    d = defaultdict(lambda: [0, 0, 0])
    for i in range(len(rr["n"])):
        a = d[rr["nid"][i]]
        a[0] += rr["n"][i]
        a[1] += rr["kc"][i]
        a[2] += rr["kt"][i]
    return d


def boot_ratio_from_n(aggs, nboot, rng):
    """Cluster (per-N) bootstrap of r = p_cand/p_ctrl."""
    ids = sorted(aggs.keys())
    ns = np.array([aggs[i][0] for i in ids], dtype=float)
    kc = np.array([aggs[i][1] for i in ids], dtype=float)
    kt = np.array([aggs[i][2] for i in ids], dtype=float)
    tot_n, tot_kc, tot_kt = ns.sum(), kc.sum(), kt.sum()
    p_c = tot_kc / tot_n if tot_n else float("nan")
    p_t = tot_kt / tot_n if tot_n else float("nan")
    r_pt = p_c / p_t if (p_t and p_t > 0) else float("nan")
    R = len(ids)
    out = np.full(nboot, np.nan)
    CH = 200
    done = 0
    while done < nboot:
        m = min(CH, nboot - done)
        idx = rng.integers(0, R, size=(m, R))
        KC = kc[idx].sum(1)
        NN = ns[idx].sum(1)
        KT = kt[idx].sum(1)
        with np.errstate(divide="ignore", invalid="ignore"):
            rr = (KC / NN) / (KT / NN)
        out[done:done + m] = np.where((KT > 0) & (NN > 0), rr, np.nan)
        done += m
    fin = out[np.isfinite(out)]
    n_bad = nboot - len(fin)
    if len(fin) >= 100:
        ci = (float(np.percentile(fin, 2.5)), float(np.percentile(fin, 97.5)))
    elif tot_kt > 0 and math.isfinite(r_pt):
        se = math.sqrt(1.0 / max(tot_kc, 1) + 1.0 / tot_kt)
        ci = (r_pt * math.exp(-1.96 * se), r_pt * math.exp(1.96 * se))
    else:
        ci = (float("nan"), float("nan"))
    return r_pt, ci, n_bad, {"p_cand": p_c, "p_ctrl": p_t, "n_clusters_N": R}


def boot_r_stars(aggs, nboot, rng):
    """Per-bin bootstrap replicate array of r* (for the joint slope test)."""
    ids = sorted(aggs.keys())
    ns = np.array([aggs[i][0] for i in ids], dtype=float)
    kc = np.array([aggs[i][1] for i in ids], dtype=float)
    kt = np.array([aggs[i][2] for i in ids], dtype=float)
    R = len(ids)
    stars = np.full(nboot, np.nan)
    CH = 200
    done = 0
    while done < nboot:
        m = min(CH, nboot - done)
        idx = rng.integers(0, R, size=(m, R))
        KC = kc[idx].sum(1)
        NN = ns[idx].sum(1)
        KT = kt[idx].sum(1)
        with np.errstate(divide="ignore", invalid="ignore"):
            rr = (KC / NN) / (KT / NN)
        stars[done:done + m] = np.where((KT > 0) & (NN > 0), rr, np.nan)
        done += m
    return stars


def boot_slope(r_star_list, us):
    """Bootstrap OLS slope of log r*(u) on u; NaN-aware."""
    A = np.vstack(r_star_list)
    with np.errstate(divide="ignore", invalid="ignore"):
        LA = np.log(A)
    us = np.asarray(us, dtype=float)
    um = us.mean()
    denom = float(((us - um) ** 2).sum())
    with np.errstate(invalid="ignore"):
        lmean = np.nanmean(LA, axis=0, keepdims=True)
        sl = np.nansum((LA - lmean) * (us - um)[:, None], axis=0) / denom
        sl = np.where(np.isnan(LA).any(axis=0), np.nan, sl)
    fin = sl[np.isfinite(sl)]
    if len(fin) < 100:
        return float("nan"), (float("nan"), float("nan")), float("nan"), 0
    lo, hi = np.percentile(fin, [2.5, 97.5])
    p_two = float(min(1.0, 2.0 * min((fin > 0).mean(), (fin < 0).mean())))
    return float(fin.mean()), (float(lo), float(hi)), p_two, int(len(fin))


def dispersion(counts):
    c = np.asarray(counts, dtype=float)
    if len(c) < 2 or c.mean() <= 0:
        return float("nan")
    return float(c.var(ddof=1) / c.mean())


def boot_disp_ci(counts, nboot, rng):
    """CI for D = Var_ddof1/Mean over resampled per-N counts."""
    c = np.asarray(counts, dtype=float)
    R = len(c)
    if R < 5:
        return (float("nan"), float("nan"))
    CH = 500
    out = np.empty(nboot)
    done = 0
    while done < nboot:
        m = min(CH, nboot - done)
        idx = rng.integers(0, R, size=(m, R))
        sel = c[idx]
        mu = sel.mean(1)
        with np.errstate(divide="ignore", invalid="ignore"):
            dd = sel.var(1, ddof=1) / mu
        out[done:done + m] = np.where(mu > 0, dd, np.nan)
        done += m
    fin = out[np.isfinite(out)]
    if len(fin) < 100:
        return (float("nan"), float("nan"))
    return (float(np.percentile(fin, 2.5)), float(np.percentile(fin, 97.5)))


def rankdata(a):
    a = np.asarray(a, dtype=float)
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), dtype=float)
    sa = a[order]
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and sa[j + 1] == sa[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0 + 0.5
        i = j + 1
    return ranks


def spearman_perm(x, y, nperm=1500, seed=12345):
    rx, ry = rankdata(x), rankdata(y)
    rx = rx - rx.mean()
    ry = ry - ry.mean()
    denom = math.sqrt(float(rx @ rx) * float(ry @ ry))
    rho = float(rx @ ry / denom) if denom > 0 else float("nan")
    if not math.isfinite(rho) or len(x) < 8:
        return rho, float("nan")
    rng = np.random.default_rng(seed)
    cnt = 0
    rxx = float(rx @ rx)
    for _ in range(nperm):
        ry2 = ry[rng.permutation(len(ry))]
        d2 = math.sqrt(rxx * float(ry2 @ ry2))
        if abs(rx @ ry2 / d2) >= abs(rho):
            cnt += 1
    return rho, (cnt + 1) / (nperm + 1)


# ---------------------------------------------------------------------------
# orchestrator
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--minutes", type=float, default=19.0,
                    help="measurement-phase wall budget (minutes)")
    ap.add_argument("--calib-seconds", type=float, default=30.0)
    ap.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 4))
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--pool-per-bin", type=int, default=4000)
    ap.add_argument("--g", type=int, default=256, help="candidates per run")
    ap.add_argument("--alloc-fractions", default="0.08,0.14,0.30,0.48",
                    help="measurement-time fraction per bin 5,6,7,8")
    ap.add_argument("--max-runs-per-n", type=int, default=2500)
    ap.add_argument("--nboot", type=int, default=2000)
    ap.add_argument("--outdir",
                    default="/home/raver1975/factor3/ResearchOutput/scripts/"
                            "2026-08-21-resume")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    log_path = os.path.join(args.outdir, "exp562_scale_smoothness.log")
    json_path = os.path.join(args.outdir, "exp562_result.json")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(log_path, mode="a"),
                  logging.StreamHandler(sys.stdout)])
    log = logging.getLogger("exp562")

    t0 = time.time()
    G = 64 if args.smoke else args.g
    unit_size = 1 if args.smoke else 16
    pool_per_bin = 10 if args.smoke else args.pool_per_bin
    max_runs_per_n = 4 if args.smoke else args.max_runs_per_n
    nboot = 200 if args.smoke else args.nboot
    minutes = 0.35 if args.smoke else args.minutes
    calib_seconds = 3.0 if args.smoke else args.calib_seconds

    rng = random.Random(args.seed)
    log.info(f"exp{EXP_ID} {CODENAME} start seed={args.seed} "
             f"smoke={args.smoke} workers={args.workers} G={G} "
             f"unit={unit_size}")

    result = {
        "exp": EXP_ID,
        "codename": CODENAME,
        "date": "2026-08-23",
        "seed": args.seed,
        "smoke": bool(args.smoke),
        "status": "running",
        "question": "does x^2-N deviate from size-matched randomness in "
                    "B-smoothness at u=log(v)/log(B) in {5,6,7,8}?",
        "config": {
            "B": B, "bins": list(BIN_WS),
            "bin_def": "bin w = v in [B^w, B^(w+1)), u = ln(v)/ln(B)",
            "u_note": "u binned by ACTUAL candidate magnitude (the numbers "
                      "whose smoothness is tested); 'x_max-ish' read as the "
                      "size of v itself",
            "n_bitlen_strata": {str(w): list(STRATA[w]) for w in BIN_WS},
            "j_cap": f"j <= {J_CAP_MULT}*isqrt(N)  (x <= 4 sqrt(N))",
            "u78_truncation": "with N<=2^80 and j<=3s the reachable v tops "
                              "out near 15*s^2 ~= 3.75*N, so bin 7 tops out "
                              "around u~7.9 and bin 8 around u~8.5; achieved "
                              "ranges reported empirically per bin",
            "G": G, "unit_size": unit_size,
            "pool_per_bin": pool_per_bin,
            "max_runs_per_n": max_runs_per_n,
            "mantissa_octants": MANT_OCT,
            "control_match":
                "exact (bitlen, mantissa-octant) histogram match; controls "
                "uniform within octant, candidates near-uniform in v",
            "tester": "gcd-chain primorial, shared code path both populations",
            "minutes_measure": minutes,
            "calib_seconds": calib_seconds,
            "workers": args.workers, "nboot": nboot,
            "alloc_fractions": args.alloc_fractions,
        },
    }

    # ---- assertion pipeline: tester validation -----------------------------
    val = run_validation(rng)
    result["assert_pipeline"] = val
    log.info(f"validation: {val['n_cases']} cases "
             f"({val['n_adversarial']} adversarial, "
             f"{val['n_real_quadratic']} real quadratic), "
             f"mismatches={val['mismatches']}")
    if not val["ok"] or val["n_cases"] < 200:
        result["status"] = "failed_validation"
        with open(json_path, "w") as f:
            json.dump(result, f, indent=1)
        log.error("VALIDATION FAILED - aborting")
        sys.exit(2)

    # ---- pools --------------------------------------------------------------
    pools = {}
    for w in BIN_WS:
        pools[w] = build_pool(w, pool_per_bin, rng, G)
        log.info(f"pool bin {w}: {len(pools[w])} semiprimes "
                 f"(bitlens {STRATA[w]})")
    result["pool_sizes"] = {str(w): len(pools[w]) for w in BIN_WS}
    result["pool_qr_summary"] = {
        str(w): {"qr_frac_mean": float(np.mean([e.qr_frac for e in pools[w]])),
                 "qr_weighted_mean":
                     float(np.mean([e.qr_w for e in pools[w]]))}
        for w in BIN_WS}

    win_counters = defaultdict(int)
    meas_counter = defaultdict(int)

    def make_spec(e: NEntry, w, half):
        st = next_window(e, G, rng, half)
        if st is None:
            return None
        key = (w, e.nid)
        wi = win_counters[key]
        win_counters[key] += 1
        if half == 1:
            meas_counter[key] += 1
            if meas_counter[key] > max_runs_per_n:
                return None
        return (w, e.nid, e.N, e.s, st, G,
                ctrl_seed_for(args.seed, w, e.nid, f"{half}:{wi}"))

    def spec_stream(w, n_units, half):
        """Yield units (lists of specs); round-robin over the pool."""
        made, idx = 0, 0
        order = list(pools[w])
        got_this_pass = False
        while made < n_units:
            if idx % len(order) == 0 and idx > 0 and not got_this_pass:
                return                      # whole pool exhausted / capped
            if idx % len(order) == 0:
                got_this_pass = False
            e = order[idx % len(order)]
            idx += 1
            unit = []
            while len(unit) < unit_size:
                sp = make_spec(e, w, half)
                if sp is None:
                    break
                got_this_pass = True
                unit.append(sp)
            if unit:
                made += 1
                yield unit

    import multiprocessing as mp
    ctx = mp.get_context("fork")
    pool = ctx.Pool(args.workers)
    pending = queue_mod.Queue()

    # ---- phase A: calibration (deadline-driven) ----------------------------
    calib = {w: {"n": 0, "kc": 0, "kt": 0} for w in BIN_WS}

    def cb_cal(res_unit):
        for r in res_unit:
            c = calib.get(r[0])
            if c is not None:
                c["n"] += r[3]
                c["kc"] += r[4]
                c["kt"] += r[5]
        pending.put(1)

    cal_streams = {w: spec_stream(w, 10 ** 9, 0) for w in BIN_WS}
    cal_tests = 0
    ncal = 0
    cal_inflight = []
    t_cal0 = time.time()
    cal_deadline = t_cal0 + calib_seconds
    stopped = False
    while True:
        now = time.time()
        if now >= cal_deadline:
            stopped = True
        if not stopped:
            fed = False
            for w in BIN_WS:
                try:
                    unit = next(cal_streams[w])
                except StopIteration:
                    continue
                cal_tests += sum(sp[5] for sp in unit) * 2
                cal_inflight.append(pool.apply_async(exec_unit, (unit,),
                                                     callback=cb_cal))
                ncal += 1
                fed = True
            if not fed:
                stopped = True
            if len(cal_inflight) > args.workers * 8:
                cal_inflight = [f for f in cal_inflight if not f.ready()]
                if len(cal_inflight) > args.workers * 8:
                    time.sleep(0.005)
        else:
            if all(f.ready() for f in cal_inflight):
                break
            if now > cal_deadline + 45:
                pool.terminate()
                log.error("calibration hung; terminated")
                sys.exit(3)
            time.sleep(0.02)
            continue
        try:
            while True:
                pending.get_nowait()
        except queue_mod.Empty:
            pass
    cal_wall = max(time.time() - t_cal0, 1e-9)
    theta = cal_tests / cal_wall
    rho_hat = {}
    for w in BIN_WS:
        emp = (calib[w]["kt"] + 0.5) / max(calib[w]["n"], 1)
        rho_hat[w] = 0.5 * RHO_PRIOR[w] + 0.5 * emp   # allocation blend only
    log.info(f"calibration: {ncal} units, {cal_tests} tests in "
             f"{cal_wall:.1f}s -> theta={theta:.3g} tests/s; "
             f"rho_hat(ctrl, blended)=" +
             str({w: f"{rho_hat[w]:.2e}" for w in BIN_WS}) +
             " (empirical " +
             str({w: f"{(calib[w]['kt'] + 0.5) / max(calib[w]['n'], 1):.2e}"
                  for w in BIN_WS}) + ")")
    result["calibration"] = {
        "tests": cal_tests, "wall_s": cal_wall,
        "throughput_tests_per_s": theta,
        "rho_empirical_ctrl": {str(w):
                               (calib[w]["kt"] + 0.5) /
                               max(calib[w]["n"], 1) for w in BIN_WS},
        "rho_allocation_blend": {str(w): rho_hat[w] for w in BIN_WS},
        "rho_prior_note": "priors used ONLY for time allocation, not results",
    }

    # ---- phase B: quotas ----------------------------------------------------
    remain = minutes * 60.0
    capacity_tests = theta * remain * 0.92
    # Fixed time fractions per bin (robust to unknown smoothness rates;
    # calibration rates are reported but NOT used for allocation).
    fracs = {w: float(f) for w, f in
             zip(BIN_WS, args.alloc_fractions.split(","))}
    assert len(fracs) == 4 and abs(sum(fracs.values()) - 1.0) < 1e-6
    max_cand_capacity = {w: len(pools[w]) * max_runs_per_n * G for w in BIN_WS}
    units_quota, clipped, quota_tests = {}, {}, {}
    for w in BIN_WS:
        want_units = int(capacity_tests * fracs[w] // (2 * G * unit_size)) + 1
        cap_units = max(1, max_cand_capacity[w] // (G * unit_size))
        units_quota[w] = int(min(want_units, cap_units))
        clipped[w] = bool(want_units > cap_units)
        quota_tests[w] = units_quota[w] * 2 * G * unit_size
    log.info("quotas(tests)=" + str({w: quota_tests[w] for w in BIN_WS}) +
             f" fracs={fracs} clipped={clipped}")
    result["quotas"] = {
        "capacity_tests_est": capacity_tests,
        "allocation": "fixed time fractions (robust to unknown rates)",
        "fractions": {str(w): fracs[w] for w in BIN_WS},
        "quota_tests": {str(w): quota_tests[w] for w in BIN_WS},
        "units": {str(w): units_quota[w] for w in BIN_WS},
        "clipped_by_pool_capacity": {str(w): clipped[w] for w in BIN_WS},
    }

    # ---- measurement --------------------------------------------------------
    deadline = time.time() + remain
    hard_deadline = deadline + 90.0
    inflight = []
    results = {w: {"nid": array.array("q"), "n": array.array("q"),
                   "kc": array.array("q"), "kt": array.array("q"),
                   "hb": array.array("i")} for w in BIN_WS}
    stats = {w: {"n": 0, "kc": 0, "kt": 0, "runs": 0, "xmaxos": 0.0,
                 "usum": 0.0, "bl": Counter()} for w in BIN_WS}

    def cb(res_unit):
        for r in res_unit:
            w, nid, hb, n, kc, kt, bls_b = r[0], r[1], r[2], r[3], r[4], \
                r[5], r[6]
            s = stats[w]
            s["runs"] += 1
            if n <= 0:
                continue
            s["n"] += n
            s["kc"] += kc
            s["kt"] += kt
            if r[10] > s["xmaxos"]:
                s["xmaxos"] = r[10]
            s["usum"] += r[11] * n
            s["bl"].update(bls_b)
            rr = results[w]
            rr["nid"].append(nid)
            rr["n"].append(n)
            rr["kc"].append(kc)
            rr["kt"].append(kt)
            rr["hb"].append(hb if hb is not None else -1)
        pending.put(1)

    streams = {w: spec_stream(w, units_quota[w], 1) for w in BIN_WS}
    done_bins = set()
    n_submitted = 0
    stopped_feeding = False
    t_last_log = time.time()

    while True:
        now = time.time()
        if now >= deadline:
            stopped_feeding = True
            log.info("deadline reached; draining in-flight units")
        if not stopped_feeding:
            fed = False
            for w in BIN_WS:
                if w in done_bins:
                    continue
                try:
                    unit = next(streams[w])
                except StopIteration:
                    done_bins.add(w)
                    continue
                inflight.append(pool.apply_async(exec_unit, (unit,),
                                                 callback=cb))
                n_submitted += 1
                fed = True
            if not fed and len(done_bins) == len(BIN_WS):
                stopped_feeding = True
            if len(inflight) > args.workers * 24:
                time.sleep(0.02)
        else:
            alive = [f for f in inflight if not f.ready()]
            if not alive:
                break
            if now > hard_deadline:
                log.warning("hard deadline; terminating pool")
                pool.terminate()
                break
            time.sleep(0.05)
            continue
        inflight = [f for f in inflight if not f.ready()] \
            if len(inflight) > args.workers * 12 else inflight
        try:
            while True:
                pending.get_nowait()
        except queue_mod.Empty:
            pass
        if now - t_last_log > 25:
            t_last_log = now
            log.info("progress(n,kc,kt): " +
                     str({w: (stats[w]["n"], stats[w]["kc"], stats[w]["kt"])
                          for w in BIN_WS}))

    t_meas_end = time.time()
    try:
        pool.close()
        pool.join()
    except Exception:
        pass
    log.info("measurement done: " +
             str({w: (stats[w]["n"], stats[w]["kc"], stats[w]["kt"])
                  for w in BIN_WS}))

    # ---- assemble per-bin analyses -----------------------------------------
    boot_rng = np.random.default_rng(args.seed)
    per_bin = {}
    r_star_list, us_used = [], []
    for w in BIN_WS:
        s = stats[w]
        aggs = agg_by_n(results[w])
        hbs = defaultdict(lambda: [0, 0, 0])
        rr = results[w]
        for i in range(len(rr["n"])):
            h = hbs[rr["hb"][i]]
            h[0] += rr["n"][i]
            h[1] += rr["kc"][i]
            h[2] += rr["kt"][i]
        r_pt, ci, n_bad, aux = boot_ratio_from_n(aggs, nboot, boot_rng)
        half_tab = {}
        for hb, (n, kc, kt) in sorted(
                hbs.items(), key=lambda kv:
                    (kv[0] is None, kv[0] if kv[0] is not None else 0)):
            half_tab[str(hb)] = {
                "u_approx": hb / 2.0, "n": n, "kc": kc, "kctrl": kt,
                "p_cand": kc / n if n else None,
                "p_ctrl": kt / n if n else None,
                "r": ((kc / n) / (kt / n)) if (n and kt) else None,
            }
        run_c = list(rr["kc"])
        run_t = list(rr["kt"])
        N_counts_c, N_counts_t, N_ids_ok = [], [], []
        for nid, a in sorted(aggs.items()):
            if a[0] > 0:
                N_counts_c.append(a[1])
                N_counts_t.append(a[2])
                N_ids_ok.append(nid)
        D_run_c, D_run_t = dispersion(run_c), dispersion(run_t)
        D_N_c, D_N_t = dispersion(N_counts_c), dispersion(N_counts_t)
        nb2 = min(nboot, 800)
        D_N_c_ci = boot_disp_ci(N_counts_c, nb2, boot_rng)
        D_N_t_ci = boot_disp_ci(N_counts_t, nb2, boot_rng)
        qx, qy, qwy = [], [], []
        for e in pools[w]:
            a = aggs.get(e.nid)
            if a and a[0] >= G:
                qx.append(e.qr_frac)
                qy.append(a[1] / a[0])
                qwy.append(e.qr_w)
        if len(qx) >= 8:
            rho_qr, p_qr = spearman_perm(qx, qy, 1500)
        else:
            rho_qr, p_qr = float("nan"), float("nan")
        bl_hist = Counter({int(k) + 40: v for k, v in s["bl"].items()})
        if bl_hist:
            u_lo = min(bl_hist) / math.log2(B)
            u_hi = (max(bl_hist) + 1) / math.log2(B)
        else:
            u_lo = u_hi = None
        u_emp = s["usum"] / s["n"] if s["n"] else None
        per_bin[str(w)] = {
            "n_cand": s["n"], "kc_cand": s["kc"],
            "p_cand": s["kc"] / s["n"] if s["n"] else None,
            "n_ctrl": s["n"], "kc_ctrl": s["kt"],
            "p_ctrl": s["kt"] / s["n"] if s["n"] else None,
            "r_point": r_pt, "r_ci95": list(ci),
            "boot_bad_reps": n_bad, "aux": aux,
            "achieved_u_range_from_bitlen_hist": [u_lo, u_hi],
            "u_empirical_mean": u_emp,
            "u_center_for_trend": u_emp if u_emp is not None else w + 0.5,
            "runs": s["runs"], "n_clusters_N": len(aggs),
            "max_x_over_sqrtN": s["xmaxos"],
            "bitlen_hist": {str(k): v for k, v in sorted(bl_hist.items())},
            "half_bins_by_2u": half_tab,
            "dispersion": {
                "run_level_D_cand": D_run_c,
                "run_level_D_ctrl": D_run_t,
                "N_level_D_cand": D_N_c,
                "N_level_D_cand_ci95": list(D_N_c_ci),
                "N_level_D_ctrl": D_N_t,
                "N_level_D_ctrl_ci95": list(D_N_t_ci),
                "poisson_random_model_reference": 1.0,
            },
            "qr_structure": {
                "n_N_used": len(qx),
                "spearman_rate_vs_qrfrac": rho_qr,
                "perm_p_two_sided": p_qr,
                "qr_weighted_mean": float(np.mean(qwy)) if qwy else None,
            },
        }
        if s["n"] and s["kt"] and len(aggs) >= 5:
            r_star_list.append(boot_r_stars(aggs, nboot, boot_rng))
            us_used.append(u_emp if u_emp is not None else w + 0.5)

    # ---- trend test ---------------------------------------------------------
    if len(us_used) >= 3:
        slope, sl_ci, sl_p, n_ok = boot_slope(r_star_list, us_used)
        trend = {
            "model": "OLS of log r*(u) on u; bootstrap over N-clusters",
            "slope_log_r_per_u": slope, "slope_ci95": list(sl_ci),
            "p_two_sided_bootstrap": sl_p, "n_ok_bootstrap_reps": n_ok,
            "bins_used": us_used,
        }
    else:
        trend = {"model": "insufficient bins with events",
                 "bins_used": us_used}

    # ---- verdicts (pre-stated) ---------------------------------------------
    def ci_finite(w):
        return all(math.isfinite(c) for c in per_bin[str(w)]["r_ci95"])

    excl = {}
    for w in (6, 7, 8):
        ci = per_bin[str(w)]["r_ci95"]
        excl[w] = bool(ci_finite(w) and (ci[0] > 1 or ci[1] < 1))
    slope = trend.get("slope_log_r_per_u", float("nan"))
    sl_ci = tuple(trend.get("slope_ci95", (float("nan"), float("nan"))))
    trend_sig = bool(all(math.isfinite(c) for c in sl_ci) and
                     (sl_ci[0] > 0 or sl_ci[1] < 0))
    any_hi_excl = any(excl.values())
    all_hi_cover = all(ci_finite(w) for w in (6, 7, 8)) and \
        not any_hi_excl
    tightest = None
    for w in (6, 7, 8):
        if ci_finite(w):
            ci = per_bin[str(w)]["r_ci95"]
            bound = max(abs(ci[0] - 1), abs(ci[1] - 1))
            if tightest is None or bound < tightest[1]:
                tightest = (w, bound)
    if trend_sig and any_hi_excl:
        vname = "DEVIATION"
        vdesc = ("trend significant AND some u>=6 CI excludes 1: asymptotic "
                 "lever candidate; effect sizes in per_bin table")
    elif all_hi_cover:
        vname = "RANDOM-AT-SCALE"
        vdesc = (f"all u>=6 CIs cover 1; tightest 95% upper bound on |r-1| "
                 f"is {tightest[1]:.4f} at bin u={tightest[0]}")
    else:
        vname = "MIXED-INCONCLUSIVE"
        vdesc = (f"trend_sig={trend_sig}, any_u6plus_excl={any_hi_excl}; "
                 "precision/direction inconsistent")

    disp_verd = {}
    for w in BIN_WS:
        d = per_bin[str(w)]["dispersion"]
        dc, dt = d["N_level_D_cand"], d["N_level_D_ctrl"]
        cic = d["N_level_D_cand_ci95"]
        if not (math.isfinite(dc) and math.isfinite(dt)):
            disp_verd[w] = "NO-DATA"
        elif cic[0] == cic[0] and dc > max(1.10 * dt, 1.10) and cic[0] > 1.0:
            disp_verd[w] = "PERSISTS"
        elif abs(dc - 1.0) < 0.10 and cic[0] < 1.10:
            disp_verd[w] = "DIES-AT-THIS-U"
        else:
            disp_verd[w] = "UNCLEAR"

    result["measurement"] = {
        "wall_measurement_s": t_meas_end - t_cal0,
        "submitted_units": n_submitted,
        "stopped_feeding_at_deadline": stopped_feeding,
    }
    result["per_bin"] = per_bin
    result["trend"] = trend
    result["verdicts"] = {
        "verdict_name": vname,
        "verdict_detail": vdesc,
        "rules": {
            "trend_significant": trend_sig,
            "u6_ci_excludes_1": excl[6],
            "u7_ci_excludes_1": excl[7],
            "u8_ci_excludes_1": excl[8],
            "all_u6plus_cover_1_with_width": all_hi_cover,
        },
        "tightest_upper_bound_on_deviation": (
            {"bin_u": tightest[0],
             "max_abs_r_minus_1_at_95pct": tightest[1]} if tightest
            else None),
        "dispersion_verdict": {str(w): disp_verd[w] for w in BIN_WS},
    }
    result["dickman_reference_integer_u"] = {str(k): v
                                             for k, v in DICKMAN.items()}
    result["paper130_context"] = (
        "paper 130: ratios 0.88-0.91 at scales 2^32-2^44 (u<4.75), "
        "attributed to finite-x Dickman correction shared with controls; "
        "this experiment asks whether ANY O(1) relative deviation emerges "
        "at u>=5, where sieving's L_N[1/3] exponent lives")

    # per-N compact tables for reanalysis
    per_n_tables = {}
    for w in BIN_WS:
        aggs = agg_by_n(results[w])
        rows = []
        for e in pools[w]:
            a = aggs.get(e.nid)
            if a:
                rows.append({"nid": e.nid,
                             "bitlen_n": e.N.bit_length(),
                             "qr_frac": round(e.qr_frac, 4),
                             "qr_weighted": round(e.qr_w, 4),
                             "n": a[0], "kc": a[1], "kctrl": a[2]})
        per_n_tables[str(w)] = rows
    result["per_n_table"] = per_n_tables

    result["status"] = ("smoke" if args.smoke else
                        ("04_final" if not stopped_feeding else
                         "04_final_time_capped"))
    result["wall_s"] = time.time() - t0
    result["artifacts"] = {
        "script": os.path.abspath(__file__),
        "json": json_path,
        "log": log_path,
    }
    with open(json_path, "w") as f:
        json.dump(result, f, indent=1)
    log.info(f"WROTE {json_path} status={result['status']} verdict={vname} "
             f"wall={result['wall_s']:.1f}s")


if __name__ == "__main__":
    main()

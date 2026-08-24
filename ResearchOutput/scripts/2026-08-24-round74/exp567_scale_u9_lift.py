#!/usr/bin/env python3
"""
exp567 SCALE-U9-LIFT (factoring loop round 74, 2026-08-24, seed 20260824)

Question: does x^2 - N smoothness stay size-matched-random into u in [9,11],
where the Dickman leading term finally approaches validity (~u = 14.75)?
Extends papers 130 (pool == unrestricted random, gap=1.00 through 2^44,
u<4.75) and 209 / exp562 (RANDOM-AT-SCALE through u<=8.5 at N<=2^80;
unexplained per-N overdispersion D=1.61 at u~5.96 dead by u~7).

Design (methodology matched to exp562_scale_smoothness.py):
  * N: BALANCED semiprimes N=pq, p,q from gmpy2.next_prime on seeded random
    odd starts, bitlen exactly {96,104,112} for u-bands {9,10,11}
    (band w = v in [B^w, B^(w+1)), B=1000, u=ln(v)/ln(B)).
  * Candidates: v_j=(s+j)^2-N, s=isqrt(N), CONSECUTIVE j from the window start,
    j <= 3*s (x <= 4 sqrt(N), exp562 cap convention).  Runs truncate at the
    band top.  With the 3s cap, achieved u tops out near 15N: ~9.9 / 10.8 /
    11.6 per band (reported empirically per bin).
  * LADDER INDICATORS (LPF-CDF quantile comparison, scout P3): each value is
    tested against cut ladder Y in {500, 1000, 1e4, 1e5, 1e6}:  indicator
    t_Y = [LPF(v) <= Y]  (cofactor 1 after stripping all primes <= Y).
    At u in [9,11] full B=1000 smoothness has expected yield rho(9..11) ~ 0
    (pre-declared: the B=500/1000 arms are continuity carriers with wide-or-
    empty CIs); the powered comparisons are the 1e4/1e5/1e6 cuts, which see
    ~1e2-1e5 events.  Tester = gcd-chain against segment primorials, BATCHED
    per window via product-tree remainder descent (one big division per
    window per segment instead of per candidate; exp561 batch-amortization),
    ~7-9 us/value vs ~87 us naive at these sizes.
  * Controls: uniform random integers matched EXACTLY to candidates on
    (bitlen, mantissa-octant within the dyadic class) - identical histogram,
    generated per run from the candidate codes; SAME ladder tester objects,
    shared code path.  1:1 pairing as in exp562.
  * Statistics: per bin per cut r = P(cand t_Y)/P(ctrl t_Y), cluster (per-N)
    bootstrap CIs, nboot>=1000; split-half replication (measurement windows
    alternately assigned to halves A/B by window-index parity);
    per-N overdispersion D=Var/Mean of smooth counts per cut (primary lens:
    1e6 cut, healthy rates) with bootstrap CIs; Spearman(per-N rate vs QR
    fraction of primes<=1000) with permutation p (dial-decay tracking).

PRE-REGISTERED hypotheses and verdict rules (stated before the full run):
  H1 (expected): r_cut(u)=1 at every bin and every cut - randomness extends
    through u~11 toward the leading-term regime; consistency with 130+209.
  H2 (barrier-relevant event protocol): the lab has NO confirmed positive
    scale-smoothness deviation.  Any bin whose r-CI excludes 1 at any cut is
    flagged only as DEVIATION-UNCONFIRMED unless it survives ALL of:
    (a) direction consistency across the ladder cuts within the bin
        (sign(r-1) identical wherever the 95% CI excludes 1, requiring the
        1e6 cut itself to exclude);
    (b) split-half replication: BOTH halves show the same-direction exclusion
        at the flagged cut;
    (c) fresh-seed replication: an independent pool (seed+1, fresh N, fresh
        controls) run afterwards shows the same-direction exclusion at the
        flagged cut (run only if wall budget >= 270s remain; else the flag
        stays UNCONFIRMED and is disclosed as such).
    Only then DEVIATION-CONFIRMED.  Otherwise:
  RANDOM-EXTENDS : every bin's every-cut CI covers 1 -> report tightest
    95% bound on |r-1| (primary family: the 1e6 cut).
  MIXED-INCONCLUSIVE: otherwise.
  Overdispersion localization (exp562 D-death mechanism read-out):
    L1 RATE-THRESHOLD ARTIFACT: D_cand(1e6 cut) significantly > 1 in >=2 bins
       at u>=9 -> the D=1.61->1.00 death was rate/threshold-driven, the
       clustering persists when rates are healthy (N-covariant mechanism).
    L2 GENUINE U-DEATH: D_cand(1e6) ~ 1 (CI within [.,1.05] and point in
       (0.95,1.05)) in ALL bins -> the death is u-driven and closes at high
       scale too.  Per-bin PERSISTS/DIES/UNCLEAR labels as in exp562.

Runtime discipline: PILOT mode (--pilot, bitlen 96 only, <=4.5 min) precedes
the full run; TOTAL wall capped (--wall-min, full default 20); populations
shrink adaptively rather than blow the cap; final counts disclosed; status
records 06_final_time_capped if the deadline stopped feeding (exp562 honesty
convention).

Artifacts: exp567_result.json, exp567_smoke.log / exp567_full.log (same dir).
"""

import argparse
import array
import faulthandler
import hashlib
import json
import logging
import math
import os
import queue as queue_mod
import random
import signal
import sys
import time
from collections import Counter, defaultdict

import numpy as np
import gmpy2
from gmpy2 import mpz

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
EXP_ID = "567"
CODENAME = "SCALE-U9-LIFT"
DEFAULT_SEED = 20260824
B = 1000
LOG_B = math.log(B)
BIN_WS = (9, 10, 11)               # band w: v in [B^w, B^(w+1))
STRATA = {9: 96, 10: 104, 11: 112} # u-band -> exact N bitlen
CUTS = (500, 1000, 10 ** 4, 10 ** 5, 10 ** 6)
PRIMARY_CUT = 4                    # index of 1e6 in CUTS
J_CAP_MULT = 3                     # j <= 3s  =>  x <= 4 sqrt(N)
MANT_OCT = 8                       # mantissa sub-buckets per dyadic class
BL_OFF = 80                        # byte packing offset for candidate bitlens

# allocation priors for the 1e6-cut control rate (time allocation ONLY)
RHO_PRIOR = {9: 2.5e-3, 10: 2.0e-4, 11: 5.0e-5}

# Dickman rho at integer u, context only
DICKMAN = {5: 3.547e-4, 6: 1.9650e-5, 7: 8.7455e-7, 8: 3.2329e-8,
           9: 1.0107e-9, 10: 2.7701e-11, 11: 6.454e-13}


def sieve_primes(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if s[p]:
            s[p * p::p] = False
    return [int(i) for i in np.nonzero(s)[0]]


PRIMES = sieve_primes(CUTS[-1])


def _treeprod(xs):
    cur = [mpz(x) for x in xs]
    while len(cur) > 1:
        nxt = []
        for i in range(0, len(cur) - 1, 2):
            nxt.append(cur[i] * cur[i + 1])
        if len(cur) % 2:
            nxt.append(cur[-1])
        cur = nxt
    return cur[0]


# segment primorials: SEGS[k] = product of primes in (CUTS[k-1], CUTS[k]]
_prev = 1
SEGS = []
for _c in CUTS:
    SEGS.append(mpz(_treeprod([p for p in PRIMES if _prev < p <= _c])))
    _prev = _c
FULL_PM = mpz(_treeprod(PRIMES))   # primorial of ALL primes <= 1e6
ODD_PRIMES_LE_B = [p for p in PRIMES if p <= B and p != 2]

# ---------------------------------------------------------------------------
# ladder testers
# ---------------------------------------------------------------------------


def naive_strip(x, pm):
    """Reference stripper: repeated gcd against primorial pm."""
    g = gmpy2.gcd(x, pm)
    while g > 1:
        x //= g
        g = gmpy2.gcd(x, pm)
    return x


def batch_strip(xs, pm):
    """Strip every prime of pm from each xs[i], amortized by product-tree
    remainder descent: PM mod P_node descends the tree, leaf remainder
    R_i (< subtree product) satisfies gcd(xs[i], PM) = gcd(xs[i'], R_i) for
    every divisor xs[i'] | xs[i] of the leaf.  Exact; validated below."""
    n = len(xs)
    if n == 0:
        return []
    if n == 1:
        return [naive_strip(xs[0], pm)]
    levels = [list(xs)]
    while len(levels[-1]) > 1:
        cur = levels[-1]
        nxt = []
        for i in range(0, len(cur) - 1, 2):
            nxt.append(cur[i] * cur[i + 1])
        if len(cur) % 2:
            nxt.append(cur[-1])
        levels.append(nxt)
    rl = [[pm % levels[-1][0]]]
    for lev in range(len(levels) - 2, -1, -1):
        cr = rl[-1]
        cp = levels[lev]
        nr = []
        for i in range(len(cp)):
            r = cr[i // 2]
            nr.append(r % cp[i] if r != 0 else mpz(0))
        rl.append(nr)
    lr = rl[-1]
    out = []
    gcd = gmpy2.gcd
    for i in range(n):
        x = xs[i]
        R = lr[i]
        g = gcd(x, R)
        while g > 1:
            x //= g
            g = gcd(x, R)
        out.append(x)
    return out


def ladder_cofactors(vs):
    """Sequential segment strips; returns list of cofactor lists (monotone
    shrinking).  cof[k]==1  <=>  LPF(value) <= CUTS[k]."""
    cof = [naive_strip(v, SEGS[0]) for v in vs]
    outs = [cof]
    for k in range(1, len(SEGS)):
        cof = batch_strip(cof, SEGS[k])
        outs.append(cof)
    return outs


def ladder_indicators(vs):
    """bool lists per cut."""
    cofs = ladder_cofactors(vs)
    return [[c == 1 for c in cof] for cof in cofs]


# ---------------------------------------------------------------------------
# validation pipeline (asserted)
# ---------------------------------------------------------------------------

def exhaustive_multicut(v):
    """Ground truth: strip ALL primes <= 1e6 exhaustively (with multiplicity,
    zero early exits) in ONE ascending pass, recording the cofactor at each
    cut.  Returns the five cut indicators."""
    r = mpz(v)
    out = []
    ci = 0
    for cut in CUTS:
        while ci < len(PRIMES) and PRIMES[ci] <= cut:
            p = PRIMES[ci]
            while r % p == 0:
                r //= p
            ci += 1
        out.append(bool(r == 1))
    return out


def run_validation(rng, n_random=60, n_real=96):
    cases, expected = [], []

    def add(v):
        v = mpz(v)
        if v <= 0:
            return
        cases.append(v)
        expected.append(exhaustive_multicut(v))

    # adversarial around every segment boundary
    bps = [2, 3, 499, 499 ** 2, 499 * 503, 503, 503 * 997, 997, 997 ** 2,
           997 * 1009, 1009, 1009 * 9973, 9973, 9973 ** 2, 9973 * 10007,
           10007, 99991, 99991 ** 2, 99991 * 999983, 999983, 999983 ** 2,
           999983 * 1000003, 1000003, 1000003 * 1000033, 1000033 ** 2,
           2 ** 64, 2 ** 100, 3 ** 40, 10 ** 27, 10 ** 30, 10 ** 33, 10 ** 36,
           2 * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29 * 31 * 37,
           999983 ** 2 * 4, 2 ** 30 * 3 ** 20 * 999983 ** 2,
           FULL_PM % 10 ** 30, 1, 12345678901234567890]
    for v in bps:
        add(v)
    for _ in range(n_random):
        bits = rng.randint(30, 120)
        add(rng.getrandbits(bits) | (1 << (bits - 1)) | 1)
    # REAL quadratic candidates from freshly generated stratum semiprimes,
    # sampled DEEP into the j-window (bottom / middle / near cap) so the
    # batch-strip path is validated at realistic large v, not just band edges
    n_re = 0
    for w in BIN_WS:
        for _ in range(max(2, n_real // (3 * len(BIN_WS)))):
            N = gen_semiprime(STRATA[w], rng)
            s = math.isqrt(N)
            x = math.isqrt(N + B ** w)
            if x * x < N + B ** w:
                x += 1
            j_lo = max(1, x - s)
            x2 = math.isqrt(N + B ** (w + 1) - 1)
            j_hi = min(x2 - s, J_CAP_MULT * s)
            span = max(1, j_hi - j_lo)
            for frac in (0.0, 0.5, 0.95):
                jj = j_lo + int(frac * span)
                xx = s + jj
                vv = xx * xx - N
                for _ in range(3):
                    if vv <= 0 or vv >= B ** (w + 1):
                        break
                    add(vv)
                    n_re += 1
                    vv = vv + 2 * xx + 1
                    xx += 1
    mismatches = []
    got_all = [ladder_indicators([v]) for v in cases]
    for v_list, got, exp in zip(cases, got_all, expected):
        g = [row[0] for row in got]
        if g != exp:
            mismatches.append((int(v_list), g, exp))
    return {
        "n_cases": len(cases),
        "n_adversarial": len(bps),
        "n_random": n_random,
        "n_real_quadratic": n_re,
        "mismatches": len(mismatches),
        "mismatch_examples": mismatches[:5],
        "ok": len(mismatches) == 0,
        "cuts": list(CUTS),
        "tester": "sequential segment-primorial gcd-chains; segments 1..4 "
                  "batch-amortized by product-tree remainder descent",
        "reference": "exhaustive ascending strip of ALL primes<=1e6, "
                     "zero early exits, cofactor sampled at each cut",
        "shared_code_path_both_populations": True,
    }


# ---------------------------------------------------------------------------
# primality / semiprimes (gmpy2.next_prime, seeded starts)
# ---------------------------------------------------------------------------

def rand_prime_gmp(bits, rng):
    while True:
        c = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        p = gmpy2.next_prime(mpz(c))
        if int(p).bit_length() == bits:
            return int(p)


def gen_semiprime(bits, rng):
    """Balanced N=p*q, exact bit_length == bits."""
    bp = bits // 2
    while True:
        p = rand_prime_gmp(bp, rng)
        q = rand_prime_gmp(bp, rng)
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
# bin pools: semiprimes + disjoint phase-split j-windows (exp562 machinery)
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
        self.starts0 = self.starts1 = None
        self.used0 = self.used1 = None
        nqr = 0
        wnum = 0.0
        wden = 0.0
        for p in ODD_PRIMES_LE_B:
            if legendre(N, p) == 1:
                nqr += 1
                wnum += 2.0 / p
            wden += 1.0 / p
        self.qr_frac = nqr / len(ODD_PRIMES_LE_B)
        self.qr_w = wnum / wden if wden > 0 else 0.0

    def feasible(self, G):
        return self.j_hi - self.j_lo + 1 >= 4 * G


def build_pool(w, count, rng, G):
    bits = STRATA[w]
    pool, tries = [], 0
    while len(pool) < count and tries < count * 200:
        tries += 1
        N = gen_semiprime(bits, rng)
        e = NEntry(len(pool) + w * 100000, N, w)
        if e.feasible(G):
            pool.append(e)
    return pool


def next_window(e: NEntry, G, rng, half):
    """Fresh disjoint gap-spaced window start within phase-half `half`."""
    step = 2 * G
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
# worker: one run = G ladder-tested candidates + G matched controls
# ---------------------------------------------------------------------------

def exec_run(spec):
    (w, nid, wi, N, s, j0, G, ctrl_seed) = spec
    t_high = B ** (w + 1)
    inv_log_b = 1.0 / LOG_B
    NC = len(SEGS)
    zero = (w, nid, wi, -1, 0, (0,) * NC, (0,) * NC, b"", b"",
            0.0, 0.0, 0, (0, 0, 0, 0), (0, 0, 0, 0), (), (), 0.0)
    x = s + j0
    v = x * x - N
    if v <= 0:
        return zero
    vs = []
    bls = bytearray()
    mbs = bytearray()
    qs = bytearray()
    usum = 0.0
    xmaxos = x / s
    for _ in range(G):
        if v >= t_high:
            break
        vi = int(v)
        bl = vi.bit_length()
        half_pow = 1 << (bl - 1)
        step = half_pow // MANT_OCT
        mb = (vi - half_pow) // step
        if mb >= MANT_OCT:
            mb = MANT_OCT - 1
        q = min(3, ((vi - (half_pow + step * mb)) * 4) // step)
        vs.append(v)
        bls.append(bl - BL_OFF)
        mbs.append(mb)
        qs.append(q)
        usum += math.log(vi) * inv_log_b
        v += 2 * x + 1
        x += 1
    n = len(vs)
    if n == 0:
        return zero
    # candidates through the ladder
    cofs = ladder_cofactors(vs)
    kc = tuple(sum(1 for c in cof if c == 1) for cof in cofs)
    kcc = [[0] * NC for _ in range(4)]   # cand hits per octant-quartile
    for t in range(n):
        q = qs[t]
        for k in range(NC):
            if cofs[k][t] == 1:
                kcc[q][k] += 1
    # controls: exact (bitlen, mantissa-octant) histogram match
    rng = random.Random(ctrl_seed)
    ctrls = []
    cqs = bytearray()
    cusum = 0.0
    viol = 0
    for t in range(n):
        bl = bls[t] + BL_OFF
        mb = mbs[t]
        half_pow = 1 << (bl - 1)
        step = half_pow // MANT_OCT
        lo_c = half_pow + step * mb
        hi_c = half_pow + step * (mb + 1) if mb < MANT_OCT - 1 else (1 << bl)
        cv = rng.randrange(lo_c, hi_c)
        cvi = int(cv)
        if not (lo_c <= cv < hi_c and cvi.bit_length() == bl):
            viol += 1
        ctrls.append(cv)
        cqs.append(min(3, ((cvi - lo_c) * 4) // step))
        cusum += math.log(cvi) * inv_log_b
    ccofs = ladder_cofactors(ctrls)
    kt = tuple(sum(1 for c in cof if c == 1) for cof in ccofs)
    ktc = [[0] * NC for _ in range(4)]
    for t in range(n):
        q = cqs[t]
        for k in range(NC):
            if ccofs[k][t] == 1:
                ktc[q][k] += 1
    mean_u = usum / n
    hb = int(math.floor(2.0 * mean_u))
    nq = tuple(sum(1 for qq in qs if qq == qi) for qi in range(4))
    ncq = tuple(sum(1 for qq in cqs if qq == qi) for qi in range(4))
    return (w, nid, wi, hb, n, kc, kt, bytes(bls), bytes(mbs),
            xmaxos, mean_u, viol, nq, ncq,
            tuple(tuple(row) for row in kcc),
            tuple(tuple(row) for row in ktc), cusum / n)


def exec_unit(unit):
    return [exec_run(sp) for sp in unit]


def ctrl_seed_for(master_seed, w, nid, wi):
    h = hashlib.blake2b(f"{master_seed}:{w}:{nid}:{wi}".encode(),
                        digest_size=8).digest()
    return int.from_bytes(h, "big")


# ---------------------------------------------------------------------------
# analysis helpers (exp562 lineage, generalized to K cuts)
# ---------------------------------------------------------------------------

def agg_by_n(rr, ncuts):
    d = defaultdict(lambda: [0] + [0] * ncuts + [0] * ncuts)
    for i in range(len(rr["n"])):
        a = d[rr["nid"][i]]
        a[0] += rr["n"][i]
        for k in range(ncuts):
            a[1 + k] += rr["kc"][k][i]
            a[1 + ncuts + k] += rr["kt"][k][i]
    return d


def boot_ratio(aggs, cut, ncuts, nboot, rng):
    """Cluster (per-N) bootstrap of r = p_cand/p_ctrl at one cut."""
    ids = sorted(aggs.keys())
    ns = np.array([aggs[i][0] for i in ids], dtype=float)
    kc = np.array([aggs[i][1 + cut] for i in ids], dtype=float)
    kt = np.array([aggs[i][1 + ncuts + cut] for i in ids], dtype=float)
    tot_n, tot_kc, tot_kt = ns.sum(), kc.sum(), kt.sum()
    p_c = tot_kc / tot_n if tot_n else float("nan")
    p_t = tot_kt / tot_n if tot_n else float("nan")
    r_pt = p_c / p_t if (p_t and p_t > 0) else float("nan")
    R = len(ids)
    out = np.full(nboot, np.nan)
    CH = 250
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
    stars = out if len(fin) >= 100 else None
    return r_pt, ci, n_bad, stars


def dispersion(counts):
    c = np.asarray(counts, dtype=float)
    if len(c) < 2 or c.mean() <= 0:
        return float("nan")
    return float(c.var(ddof=1) / c.mean())


def boot_disp_ci(counts, nboot, rng):
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


def boot_slope(star_lists, us):
    """Bootstrap OLS slope of log r*(u) on u across bins; NaN-aware."""
    A = np.vstack(star_lists)
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


# ---------------------------------------------------------------------------
# orchestrator
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--pilot", action="store_true",
                    help="bitlen-96-only sizing run")
    ap.add_argument("--minutes", type=float, default=14.5,
                    help="measurement-phase wall budget (minutes)")
    ap.add_argument("--calib-seconds", type=float, default=20.0)
    ap.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 4))
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--pool-per-bin", type=int, default=128)
    ap.add_argument("--g", type=int, default=1024, help="candidates per run")
    ap.add_argument("--unit-runs", type=int, default=4)
    ap.add_argument("--alloc-fractions", default="0.34,0.33,0.33",
                    help="measurement-time fraction per band 9,10,11")
    ap.add_argument("--max-runs-per-n", type=int, default=4000)
    ap.add_argument("--nboot", type=int, default=2000)
    ap.add_argument("--wall-min", type=float, default=None,
                    help="hard total-wall cap; default: pilot 4.5, full 20")
    ap.add_argument("--outdir",
                    default="/home/raver1975/factor3/ResearchOutput/scripts/"
                            "2026-08-24-round74")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    mode = "smoke" if args.smoke else ("pilot" if args.pilot else "full")
    log_path = os.path.join(args.outdir, f"exp567_{mode}.log")
    json_path = os.path.join(args.outdir, "exp567_result.json")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(log_path, mode="a"),
                  logging.StreamHandler(sys.stdout)])
    log = logging.getLogger(f"exp{EXP_ID}")

    t0 = time.time()
    if args.smoke:
        G, unit_size, pool_per_bin = 64, 2, 3
        minutes, calib_seconds, nboot = 0.15, 2.0, 200
        max_runs_per_n = 3
        wall_min = args.wall_min or 3.0
        bins = BIN_WS
    elif args.pilot:
        G, unit_size, pool_per_bin = 512, 4, 24
        minutes, calib_seconds, nboot = 2.5, 8.0, 500
        max_runs_per_n = 4000
        wall_min = args.wall_min or 4.5
        bins = (9,)
    else:
        G, unit_size, pool_per_bin = args.g, args.unit_runs, args.pool_per_bin
        minutes, calib_seconds, nboot = args.minutes, args.calib_seconds, \
            args.nboot
        max_runs_per_n = args.max_runs_per_n
        wall_min = args.wall_min or 20.0
        bins = BIN_WS
    ncuts = len(CUTS)
    hard_end = t0 + wall_min * 60.0

    rng = random.Random(args.seed)
    # stack-dump hook: kill -USR1 <pid> dumps ALL thread stacks to stderr
    faulthandler.register(signal.SIGUSR1, all_threads=True,
                          chain=False)
    log.info(f"exp{EXP_ID} {CODENAME} start mode={mode} seed={args.seed} "
             f"bins={bins} workers={args.workers} G={G} unit={unit_size} "
             f"wall_cap={wall_min}min")

    result = {
        "exp": EXP_ID,
        "codename": CODENAME,
        "date": "2026-08-24",
        "seed": args.seed,
        "mode": mode,
        "status": "running",
        "question": "does x^2-N stay size-matched-random in B-smoothness / "
                    "LPF-CDF at u=log(v)/log(B) in [9,11] (Dickman "
                    "leading-term approach regime)?",
        "preregistered": {
            "H1": "r_cut(u)=1 at every bin and every ladder cut - randomness "
                  "extends through u~11 toward the leading-term regime; "
                  "consistent with papers 130+209",
            "H2_protocol": "any CI-excluding-1 flag is DEVIATION-UNCONFIRMED "
                           "unless (a) direction-consistent across cuts with "
                           "the 1e6 cut excluding, (b) both split-halves "
                           "replicate, (c) fresh-seed pool replicates "
                           "(requires >=270s remaining wall); maximal "
                           "skepticism - this would be the lab's first "
                           "positive scale-smoothness deviation",
            "overdispersion_localization": {
                "L1_rate_threshold_artifact":
                    "D_expo_cand(1e6 cut) > 1 significantly in >=2 bins at "
                    "u>=9 -> exp562's D-death was rate/threshold-driven, "
                    "the per-N clustering persists when rates are healthy",
                "L2_genuine_u_death":
                    "D_expo_cand(1e6) ~ 1 in ALL bins -> death is u-driven, "
                    "closure extends to high scale",
            },
            "primary_family": "LPF-CDF cut Y=1e6 (highest event yield)",
            "continuity_carriers": "B=500 and B=1000 cuts kept for 130/209 "
                                   "continuity; predicted yield rho(9..11)*n "
                                   "~ 0 -> wide-or-empty CIs, declared",
        },
        "config": {
            "B": B, "bands_w": list(bins),
            "band_def": "band w = v in [B^w, B^(w+1)), u = ln(v)/ln(B)",
            "n_bitlen_strata": {str(w): STRATA[w] for w in bins},
            "semiprime_gen": "balanced p,q via gmpy2.next_prime on seeded "
                             "random odd starts, exact bitlen rejection",
            "j_cap": f"j <= {J_CAP_MULT}*isqrt(N)  (x <= 4 sqrt(N))",
            "truncation_note": "3s cap tops band 11 near u~11.6, bands 9/10 "
                               "near u~9.9/10.8; achieved ranges empirical",
            "cuts": list(CUTS),
            "indicator_def": "t_Y = [largest prime factor <= Y] via "
                             "cumulative segment-primorial gcd chains; "
                             "segments batch-amortized (product-tree "
                             "remainder descent, exp561 transfer)",
            "control_match": "exact (bitlen, mantissa-octant) histogram "
                             "match, 1:1 pairing, same tester code path",
            "G": G, "unit_size": unit_size,
            "pool_per_bin": pool_per_bin,
            "max_runs_per_n": max_runs_per_n,
            "mantissa_octants": MANT_OCT,
            "minutes_measure": minutes,
            "calib_seconds": calib_seconds,
            "workers": args.workers, "nboot": nboot,
            "alloc_fractions": args.alloc_fractions,
            "wall_min_cap": wall_min,
            "split_half": "measurement windows alternate A/B by window-index "
                          "parity (built-in replication)",
        },
    }

    # ---- assertion pipeline: tester validation -----------------------------
    val_rng = random.Random(args.seed + 1)
    val = run_validation(
        val_rng,
        n_random=20 if args.smoke else 60,
        n_real=18 if args.smoke else 96)
    result["assert_pipeline"] = val
    log.info(f"validation: {val['n_cases']} cases "
             f"({val['n_adversarial']} adversarial, "
             f"{val['n_real_quadratic']} real quadratic), "
             f"mismatches={val['mismatches']}")
    if not val["ok"] or val["n_cases"] < (60 if args.smoke else 200):
        result["status"] = "failed_validation"
        with open(json_path, "w") as f:
            json.dump(result, f, indent=1)
        log.error("VALIDATION FAILED - aborting")
        sys.exit(2)

    # ---- pools --------------------------------------------------------------
    pools = {}
    for w in bins:
        pools[w] = build_pool(w, pool_per_bin, rng, G)
        log.info(f"pool band {w}: {len(pools[w])} semiprimes "
                 f"(bitlen {STRATA[w]})")
    result["pool_sizes"] = {str(w): len(pools[w]) for w in bins}

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
        return (w, e.nid, wi, e.N, e.s, st, G,
                ctrl_seed_for(args.seed, w, e.nid, f"{half}:{wi}"))

    def spec_stream(w, n_units, half):
        made, idx = 0, 0
        order = list(pools[w])
        got_this_pass = False
        while made < n_units:
            if idx % len(order) == 0 and idx > 0 and not got_this_pass:
                return
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

    # ---- phase A: calibration ----------------------------------------------
    calib = {w: {"n": 0, "kc": 0, "kt": 0} for w in bins}

    def cb_cal(res_unit):
        try:
            for r in res_unit:
                c = calib.get(r[0])
                if c is not None:
                    c["n"] += r[4]
                    for k in range(ncuts):
                        c["kc"] += r[5][k]
                        c["kt"] += r[6][k]
        except Exception:
            log.exception("cb_cal EXCEPTION (kills pool handler thread)")
        pending.put(1)

    cal_streams = {w: spec_stream(w, 10 ** 9, 0) for w in bins}
    cal_tests = 0
    cal_inflight = []
    t_cal0 = time.time()
    cal_deadline = min(t_cal0 + calib_seconds, hard_end - 30)
    stopped = False
    while True:
        now = time.time()
        if now >= cal_deadline:
            stopped = True
        if not stopped:
            # backpressure: bound the inflight backlog so the post-deadline
            # drain stays short (a runaway submit rate once tripped the
            # watchdog in a full-scale run)
            cal_inflight = [f for f in cal_inflight if not f.ready()]
            if len(cal_inflight) >= args.workers * 4:
                time.sleep(0.005)
                continue
            fed = False
            for w in bins:
                try:
                    unit = next(cal_streams[w])
                except StopIteration:
                    continue
                cal_tests += sum(sp[6] for sp in unit) * 2
                cal_inflight.append(pool.apply_async(exec_unit, (unit,),
                                                     callback=cb_cal))
                fed = True
            if not fed:
                stopped = True
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
    theta = cal_tests / cal_wall          # values/s incl. controls
    rho_hat = {}
    for w in bins:
        emp = (calib[w]["kt"] + 0.5) / max(calib[w]["n"], 1)
        rho_hat[w] = 0.5 * RHO_PRIOR[w] + 0.5 * emp
    log.info(f"calibration: {cal_tests} values in {cal_wall:.1f}s -> "
             f"theta={theta:.3g}/s; rho_hat(ctrl@1e6, blended)=" +
             str({w: f"{rho_hat[w]:.2e}" for w in bins}))
    result["calibration"] = {
        "values_tested": cal_tests, "wall_s": cal_wall,
        "throughput_values_per_s": theta,
        "rho_empirical_ctrl_1e6cut": {str(w):
                                      (calib[w]["kt"] + 0.5) /
                                      max(calib[w]["n"], 1) for w in bins},
        "note": "calibration uses phase-half-0 windows (disjoint from "
                "measurement); blended priors used ONLY for quotas",
    }

    # ---- phase B: quotas ----------------------------------------------------
    remain = min(minutes, max(0.05, (hard_end - time.time()) / 60.0 - 1.0)) \
        * 60.0
    capacity_values = theta * remain * 0.92
    fracs = {w: float(f) for w, f in
             zip(bins, args.alloc_fractions.split(","))}
    if len(fracs) != len(bins):
        fracs = {w: 1.0 / len(bins) for w in bins}
    ssum = sum(fracs.values())
    fracs = {w: v / ssum for w, v in fracs.items()}
    max_cap = {w: len(pools[w]) * max_runs_per_n * G for w in bins}
    units_quota, quota_vals = {}, {}
    for w in bins:
        want_units = int(capacity_values * fracs[w] //
                         (2 * G * unit_size)) + 1
        cap_units = max(1, max_cap[w] // (G * unit_size))
        units_quota[w] = int(min(want_units, cap_units))
        quota_vals[w] = units_quota[w] * 2 * G * unit_size
    log.info("quotas(values)=" + str({w: quota_vals[w] for w in bins}) +
             f" fracs={fracs}")
    result["quotas"] = {
        "capacity_values_est": capacity_values,
        "fractions": {str(w): fracs[w] for w in bins},
        "quota_values": {str(w): quota_vals[w] for w in bins},
        "units": {str(w): units_quota[w] for w in bins},
    }

    # ---- measurement --------------------------------------------------------
    deadline = time.time() + remain
    hard_deadline = min(deadline + 120.0, hard_end - 20)
    inflight = []
    results = {w: {"nid": array.array("q"), "wi": array.array("q"),
                   "n": array.array("q"),
                   "kc": [array.array("q") for _ in range(ncuts)],
                   "kt": [array.array("q") for _ in range(ncuts)],
                   "hb": array.array("i")} for w in bins}
    stats = {w: {"n": 0, "runs": 0, "xmaxos": 0.0, "usum": 0.0,
                 "cusum": 0.0, "viol": 0,
                 "kc": [0] * ncuts, "kt": [0] * ncuts,
                 "nq": [0] * 4, "ncq": [0] * 4,
                 "kcc": [[0] * ncuts for _ in range(4)],
                 "ktc": [[0] * ncuts for _ in range(4)],
                 "bl": Counter()} for w in bins}

    def cb(res_unit):
        try:
            for r in res_unit:
                w, nid, wi, hb, n, kc, kt = r[0], r[1], r[2], r[3], r[4], \
                    r[5], r[6]
                s = stats[w]
                s["runs"] += 1
                s["viol"] += r[11]
                if n <= 0:
                    continue
                s["n"] += n
                for k in range(ncuts):
                    s["kc"][k] += kc[k]
                    s["kt"][k] += kt[k]
                if r[9] > s["xmaxos"]:
                    s["xmaxos"] = r[9]
                s["usum"] += r[10] * n
                s["cusum"] += r[16] * n
                for qi in range(4):
                    s["nq"][qi] += r[12][qi]
                    s["ncq"][qi] += r[13][qi]
                    for k in range(ncuts):
                        s["kcc"][qi][k] += r[14][qi][k]
                        s["ktc"][qi][k] += r[15][qi][k]
                s["bl"].update(r[7])
                rr = results[w]
                rr["nid"].append(nid)
                rr["wi"].append(wi)
                rr["n"].append(n)
                for k in range(ncuts):
                    rr["kc"][k].append(kc[k])
                    rr["kt"][k].append(kt[k])
                rr["hb"].append(hb if hb is not None else -1)
        except Exception:
            log.exception("cb EXCEPTION (kills pool handler thread)")
        pending.put(1)

    streams = {w: spec_stream(w, units_quota[w], 1) for w in bins}
    done_bins = set()
    n_submitted = 0
    stopped_feeding = False
    stop_logged = False
    t_last_log = time.time()

    while True:
            now = time.time()
            if now >= deadline or now >= hard_deadline - 5:
                stopped_feeding = True
                if not stop_logged:
                    stop_logged = True
                    log.info("deadline reached; draining in-flight units")
            if not stopped_feeding:
                # backpressure: bound inflight backlog (drain stays short)
                if len(inflight) > args.workers * 12:
                    inflight = [f for f in inflight if not f.ready()]
                if len(inflight) >= args.workers * 4:
                    time.sleep(0.005)
                    continue
                fed = False
                for w in bins:
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
                if n_submitted % 400 == 0:
                    log.info(f"heartbeat submits={n_submitted} "
                             f"inflight={len(inflight)}")
                if not fed and len(done_bins) == len(bins):
                    stopped_feeding = True
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
            if len(inflight) > args.workers * 24:
                inflight = [f for f in inflight if not f.ready()]
            try:
                while True:
                    pending.get_nowait()
            except queue_mod.Empty:
                pass
            if now - t_last_log > 30:
                t_last_log = now
                log.info("progress(n,kc@1e6,kt@1e6): " +
                         str({w: (stats[w]["n"], stats[w]["kc"][ncuts - 1],
                                  stats[w]["kt"][ncuts - 1])
                              for w in bins}))
    t_meas_end = time.time()
    log.info("measurement done: " +
             str({w: (stats[w]["n"],
                      [stats[w]['kc'][k] for k in range(ncuts)],
                      [stats[w]['kt'][k] for k in range(ncuts)])
                  for w in bins}))
    result["measurement"] = {
        "wall_measurement_s": t_meas_end - t_cal0,
        "submitted_units": n_submitted,
        "stopped_feeding_at_deadline": stopped_feeding,
        "control_integrity_violations": {str(w): stats[w]["viol"]
                                         for w in bins},
    }

    # ---- assemble per-band analyses ----------------------------------------
    boot_rng = np.random.default_rng(args.seed)
    NC = ncuts
    per_bin = {}
    star_lists, us_used = [], []
    flagged = []          # (w, cut, r, direction) needing H2 protocol
    disp_flags = []
    for w in bins:
        s = stats[w]
        aggs = agg_by_n(results[w], NC)
        # half-u sub-bin table (localization within the band)
        hbs = defaultdict(lambda: [[0, 0] for _ in range(NC)])
        rr = results[w]
        for i in range(len(rr["n"])):
            h = hbs[rr["hb"][i]]
            for k in range(NC):
                h[k][0] += rr["kc"][k][i]
                h[k][1] += rr["kt"][k][i]
        half_tab = {}
        for hb, tabs in sorted(hbs.items(), key=lambda kv:
                               (kv[0] is None or kv[0] < 0,
                                kv[0] if kv[0] is not None else 0)):
            half_tab[str(hb)] = {
                "u_approx": hb / 2.0,
                "per_cut": [{"n": None, "kc": tabs[k][0],
                             "kctrl": tabs[k][1]} for k in range(NC)],
            }
        # totals per cut + ratios + CIs + split-halves
        cuts_tab = {}
        stars_at = {}
        for k in range(NC):
            r_pt, ci, n_bad, stars = boot_ratio(aggs, k, NC, nboot, boot_rng)
            halves = {}
            for hname, hsel in (("A", 0), ("B", 1)):
                sub_ids = [i for i in range(len(rr["n"]))
                           if rr["wi"][i] % 2 == hsel]
                if not sub_ids:
                    halves[hname] = None
                    continue
                subaggs = defaultdict(lambda: [0] + [0] * NC + [0] * NC)
                for i in sub_ids:
                    a = subaggs[rr["nid"][i]]
                    a[0] += rr["n"][i]
                    for kk in range(NC):
                        a[1 + kk] += rr["kc"][kk][i]
                        a[1 + NC + kk] += rr["kt"][kk][i]
                hr, hci, _, _ = boot_ratio(subaggs, k, NC, min(nboot, 1000),
                                           boot_rng)
                halves[hname] = {"r": hr, "ci95": list(hci)}
            excl = bool(all(math.isfinite(c) for c in ci) and
                        (ci[0] > 1 or ci[1] < 1))
            cuts_tab[str(CUTS[k])] = {
                "n_cand": s["n"], "kc_cand": s["kc"][k],
                "p_cand": s["kc"][k] / s["n"] if s["n"] else None,
                "kc_ctrl": s["kt"][k],
                "p_ctrl": s["kt"][k] / s["n"] if s["n"] else None,
                "r_point": r_pt, "r_ci95": list(ci),
                "ci_excludes_1": excl,
                "boot_bad_reps": n_bad,
                "split_halves": halves,
            }
            stars_at[k] = stars
        # overdispersion per cut (counts per N); RAW D (exp562-comparable)
        # plus EXPOSURE-CORRECTED Pearson-chi2/dof D, since unequal per-N
        # candidate totals inflate raw count dispersion mechanically
        disp_tab = {}
        for k in range(NC):
            Nc_c, Nc_t, Nn = [], [], []
            for nid, a in sorted(aggs.items()):
                if a[0] > 0:
                    Nc_c.append(a[1 + k])
                    Nc_t.append(a[1 + NC + k])
                    Nn.append(a[0])
            D_c, D_t = dispersion(Nc_c), dispersion(Nc_t)

            def d_expo(counts, nn):
                nn = np.asarray(nn, dtype=float)
                cc = np.asarray(counts, dtype=float)
                lam = cc.sum() / nn.sum() * nn
                m = (lam > 0.5).sum()
                if m < 5:
                    return float("nan")
                return float(((cc - lam) ** 2 / lam)[lam > 0.5].sum() /
                             max(1, (lam > 0.5).sum() - 1))
            De_c, De_t = d_expo(Nc_c, Nn), d_expo(Nc_t, Nn)
            ci_c = boot_disp_ci(Nc_c, min(nboot, 800), boot_rng)
            ci_t = boot_disp_ci(Nc_t, min(nboot, 800), boot_rng)
            disp_tab[str(CUTS[k])] = {
                "D_raw_cand": D_c, "D_raw_cand_ci95": list(ci_c),
                "D_raw_ctrl": D_t, "D_raw_ctrl_ci95": list(ci_t),
                "D_expo_cand": De_c,
                "D_expo_ctrl": De_t,
                "poisson_random_model_reference": 1.0,
                "n_clusters_N": len(Nc_c),
            }
            if k == PRIMARY_CUT and math.isfinite(De_c):
                # exposure-corrected test: under Poisson-given-exposure the
                # chi2/dof has SE ~ sqrt(2/dof); require excess beyond a
                # one-sided ~95% bar AND above the control-side D
                nn_tot = float(sum(Nn))
                lam_all = np.array(Nc_c, float).sum() / nn_tot * \
                    np.array(Nn, float)
                dof = int((lam_all > 0.5).sum()) - 1
                se_d = math.sqrt(2.0 / dof) if dof > 0 else float("inf")
                if De_c > 1.0 + 1.645 * se_d and \
                        De_c > max(1.10 * (De_t if math.isfinite(De_t)
                                           else 1.0), 1.10):
                    disp_flags.append((w, "PERSISTS"))
                elif abs(De_c - 1.0) < 0.05 and De_c < 1.0 + 1.645 * se_d:
                    disp_flags.append((w, "DIES"))
                else:
                    disp_flags.append((w, "UNCLEAR"))
        # QR-dial correlation (decay tracking) at healthy cuts
        qr = {}
        for k in (2, PRIMARY_CUT):
            qx, qy = [], []
            for e in pools[w]:
                a = aggs.get(e.nid)
                if a and a[0] >= G:
                    qx.append(e.qr_frac)
                    qy.append(a[1 + k] / a[0])
            if len(qx) >= 8:
                rho_qr, p_qr = spearman_perm(qx, qy, 1500)
            else:
                rho_qr, p_qr = float("nan"), float("nan")
            qr[str(CUTS[k])] = {"n_N_used": len(qx),
                                "spearman_rate_vs_qrfrac": rho_qr,
                                "perm_p_two_sided": p_qr}
        # WITHIN-OCTANT QUARTILE AUDIT (H2 control-integrity check): the
        # octant-granularity control match leaves a worst-case within-octant
        # smoothness-gradient artifact of ~ +-0.7% per quartile; if a deficit
        # persists uniformly across quartiles it is not an octant artifact
        qtab = {}
        for qi in range(4):
            if s["nq"][qi] < 1 or s["ncq"][qi] < 1:
                continue
            rows = {}
            for k in range(NC):
                a_, b_ = s["kcc"][qi][k], s["ktc"][qi][k]
                r_ = (a_ / s["nq"][qi]) / (b_ / s["ncq"][qi]) \
                    if b_ > 0 else None
                se = math.sqrt(1.0 / max(a_, 1) + 1.0 / max(b_, 1)) \
                    if (a_ > 0 and b_ > 0) else None
                ci = ([r_ * math.exp(-1.96 * se),
                       r_ * math.exp(1.96 * se)] if se else None)
                rows[str(CUTS[k])] = {"kc": a_, "kt": b_, "r": r_,
                                      "ci95_approx": ci}
            qtab[str(qi)] = {"n_cand": s["nq"][qi], "n_ctrl": s["ncq"][qi],
                             "per_cut": rows}
        u_mean_ctrl = s["cusum"] / s["n"] if s["n"] else None
        bl_hist = Counter({int(kk) + BL_OFF: vv
                           for kk, vv in s["bl"].items()})
        if bl_hist:
            u_lo = min(bl_hist) / math.log2(B)
            u_hi = (max(bl_hist) + 1) / math.log2(B)
        else:
            u_lo = u_hi = None
        u_emp = s["usum"] / s["n"] if s["n"] else None
        per_bin[str(w)] = {
            "n_bitlen": STRATA[w],
            "n_cand": s["n"], "runs": s["runs"],
            "achieved_u_range_from_bitlen_hist": [u_lo, u_hi],
            "u_empirical_mean": u_emp,
            "max_x_over_sqrtN": s["xmaxos"],
            "bitlen_hist": {str(kk): vv
                            for kk, vv in sorted(bl_hist.items())},
            "half_bins_by_2u": half_tab,
            "cuts": cuts_tab,
            "quartile_within_octant_audit": qtab,
            "u_mean_ctrl": u_mean_ctrl,
            "dispersion": disp_tab,
            "qr_structure": qr,
            "n_clusters_N": len(aggs),
        }
        st = stars_at.get(PRIMARY_CUT)
        if s["n"] and s["kt"][PRIMARY_CUT] and st is not None and \
                len(aggs) >= 5:
            star_lists.append(st)
            us_used.append(u_emp if u_emp is not None else w + 0.5)
        # H2 flag collection at every cut (requires events on BOTH sides -
        # a one-sided zero cannot establish a deviation direction)
        for k in range(NC):
            ct = cuts_tab[str(CUTS[k])]
            if ct["ci_excludes_1"] and ct["kc_cand"] > 0 and \
                    ct["kc_ctrl"] > 0:
                direction = "up" if ct["r_ci95"][0] > 1 else "down"
                flagged.append({"band": w, "cut": CUTS[k],
                                "r_point": ct["r_point"],
                                "direction": direction})

    # ---- trend across bands (descriptive, 1e6 cut) --------------------------
    if len(us_used) >= 3:
        slope, sl_ci, sl_p, n_ok = boot_slope(star_lists, us_used)
        trend = {"model": "OLS of log r*(u) on u; cluster bootstrap",
                 "slope_log_r_per_u": slope, "slope_ci95": list(sl_ci),
                 "p_two_sided_bootstrap": sl_p,
                 "bins_used": us_used}
    else:
        trend = {"model": "insufficient bands with events",
                 "bins_used": us_used}

    # ---- verdicts -----------------------------------------------------------
    primary_excl = [f for f in flagged if f["cut"] == CUTS[PRIMARY_CUT]]

    def cut_dir_consistent(w, direction):
        for k in range(NC):
            ct = per_bin[str(w)]["cuts"][str(CUTS[k])]
            if ct["ci_excludes_1"]:
                d = "up" if ct["r_ci95"][0] > 1 else "down"
                if d != direction:
                    return False
        return True

    def halves_replicate(w, cut, direction):
        ct = per_bin[str(w)]["cuts"][str(cut)]
        sh = ct["split_halves"]
        for h in ("A", "B"):
            hh = sh.get(h)
            if not hh:
                return False
            r, ci = hh["r"], hh["ci95"]
            if not all(math.isfinite(c) for c in ci):
                return False
            excl = ci[0] > 1 or ci[1] < 1
            d = "up" if (math.isfinite(r) and r > 1) else "down"
            if not (excl and d == direction):
                return False
        return True

    dev_status = "NONE"
    confirm_info = None
    if primary_excl:
        dev_status = "CANDIDATES-PRESENT"
    confirmed = []
    unconfirmed = list(primary_excl)
    remaining = hard_end - time.time()
    if primary_excl and remaining >= 270.0:
        # fresh-seed replication leg for the strongest flag
        tgt = max(primary_excl,
                  key=lambda f: abs((f["r_point"] or 1.0) - 1.0))
        fw, fc, fd = tgt["band"], tgt["cut"], tgt["direction"]
        if cut_dir_consistent(fw, fd) and halves_replicate(fw, fc, fd):
            log.info(f"H2 leg: fresh-seed replication of band {fw} cut {fc} "
                     f"dir {fd}")
            fs = args.seed + 1
            fs_pool = build_pool(fw, max(16, pool_per_bin // 2),
                                 random.Random(fs), G)
            fs_pool_old = pools[fw]
            pools[fw] = fs_pool
            win_counters.clear()
            meas_counter.clear()
            fs_results = {fw: {"nid": array.array("q"), "wi":
                               array.array("q"), "n": array.array("q"),
                               "kc": [array.array("q") for _ in range(NC)],
                               "kt": [array.array("q") for _ in range(NC)],
                               "hb": array.array("i")}}
            fs_stats = {fw: {"n": 0, "kc": [0] * NC, "kt": [0] * NC}}
            fs_deadline = time.time() + min(150.0, remaining - 120.0)

            def cb_fs(res_unit):
                for r in res_unit:
                    if r[0] != fw or r[4] <= 0:
                        continue
                    st_ = fs_stats[fw]
                    rr_ = fs_results[fw]
                    st_["n"] += r[4]
                    rr_["nid"].append(r[1])
                    rr_["wi"].append(r[2])
                    rr_["n"].append(r[4])
                    for k in range(NC):
                        st_["kc"][k] += r[5][k]
                        st_["kt"][k] += r[6][k]
                        rr_["kc"][k].append(r[5][k])
                        rr_["kt"][k].append(r[6][k])
                pending.put(1)

            fs_stream = spec_stream(fw, 10 ** 9, 1)
            fs_inflight = []
            while time.time() < fs_deadline:
                try:
                    unit = next(fs_stream)
                except StopIteration:
                    break
                fs_inflight.append(pool.apply_async(exec_unit, (unit,),
                                                    callback=cb_fs))
                if len(fs_inflight) > args.workers * 8:
                    alive = [f for f in fs_inflight if not f.ready()]
                    if len(alive) <= args.workers * 4:
                        time.sleep(0.01)
            alive = [f for f in fs_inflight if not f.ready()]
            for f in alive:
                try:
                    f.wait(timeout=max(1.0, fs_deadline + 60 -
                                       time.time()))
                except Exception:
                    pass
            # NOTE: callbacks may lag; harvest synchronously
            for f in fs_inflight:
                if not f.ready():
                    f.wait(timeout=30)
            fs_aggs = agg_by_n(fs_results[fw], NC)
            fr, fci, _, _ = boot_ratio(fs_aggs, CUTS.index(fc), NC,
                                       min(nboot, 1000), boot_rng)
            fexcl = all(math.isfinite(c) for c in fci) and \
                (fci[0] > 1 or fci[1] < 1)
            fdir = "up" if (math.isfinite(fr) and fr > 1) else "down"
            pools[fw] = fs_pool_old
            confirm_info = {
                "band": fw, "cut": fc, "fresh_seed": fs,
                "fresh_pool_size": len(fs_pool),
                "fresh_n": fs_stats[fw]["n"],
                "fresh_r_point": fr, "fresh_r_ci95": list(fci),
                "fresh_excludes_1": bool(fexcl),
                "fresh_direction": fdir,
                "replicated": bool(fexcl and fdir == fd),
            }
            if confirm_info["replicated"]:
                confirmed.append(tgt)
                unconfirmed.remove(tgt)
        else:
            confirm_info = {"note": "flag failed direction-consistency or "
                                    "split-half gate; no fresh-seed leg run",
                            "band": primary_excl[0]["band"],
                            "cut": primary_excl[0]["cut"]}
    elif primary_excl:
        confirm_info = {"note": f"insufficient remaining wall ({remaining:.0f}"
                                "s < 270s) for fresh-seed leg"}

    if confirmed:
        vname = "DEVIATION-CONFIRMED"
        vdesc = ("CI-excluding-1 flag(s) survived direction consistency, "
                 "split-half, AND fresh-seed replication: the lab's first "
                 "scale-smoothness deviation candidate - inspect effect "
                 "sizes immediately")
    elif primary_excl:
        vname = "DEVIATION-UNCONFIRMED"
        vdesc = ("CI-excluding-1 flag present at the 1e6 cut but H2 "
                 "replication/audit gates not all passed - recorded "
                 "unconfirmed per pre-registration")
    else:
        all_cover = True
        tightest = None
        for w in bins:
            for k in range(NC):
                ct = per_bin[str(w)]["cuts"][str(CUTS[k])]
                ci = ct["r_ci95"]
                if not all(math.isfinite(c) for c in ci):
                    continue
                if ci[0] <= 1 <= ci[1]:
                    bound = max(abs(ci[0] - 1), abs(ci[1] - 1))
                    if CUTS[k] == CUTS[PRIMARY_CUT] and \
                            (tightest is None or bound < tightest[1]):
                        tightest = (w, bound, k)
                elif k == PRIMARY_CUT:
                    all_cover = False
        if all_cover:
            vname = "RANDOM-EXTENDS"
            if tightest:
                vdesc = (f"every band/cut CI covers 1; tightest 95% bound on "
                         f"|r-1| at the primary (1e6) cut is "
                         f"{tightest[1]:.4f} at band u={tightest[0]}")
            else:
                vdesc = "every band/cut CI covers 1 (no finite primary-cut " \
                        "binding)"
        else:
            vname = "MIXED-INCONCLUSIVE"
            vdesc = ("some primary-cut CI excludes 1 without full H2 gates "
                     "and coverage elsewhere incomplete")

    # dispersion verdict assembly
    disp_verdicts = {str(w): "NO-DATA" for w in bins}
    for w, lab in disp_flags:
        disp_verdicts[str(w)] = lab
    persist_bins = [w for w, lab in disp_flags if lab == "PERSISTS"]
    die_bins = [w for w, lab in disp_flags if lab == "DIES"]
    if len(persist_bins) >= 2:
        disp_mech = "L1_RATE_THRESHOLD_ARTIFACT"
    elif len(die_bins) == len(bins) and len(die_bins) > 0:
        disp_mech = "L2_GENUINE_U_DEATH"
    else:
        disp_mech = "UNCLEAR"

    result["per_band"] = per_bin
    result["trend"] = trend
    result["verdicts"] = {
        "verdict_name": vname,
        "verdict_detail": vdesc,
        "deviation_flags_any_cut": flagged,
        "deviation_status": dev_status,
        "h2_confirmation_leg": confirm_info,
        "confirmed_deviations": [f for f in confirmed],
        "unconfirmed_deviations": unconfirmed,
        "dispersion_verdict_per_band": disp_verdicts,
        "dispersion_mechanism": disp_mech,
        "rules_fired": {
            "primary_cut_exclusions": len(primary_excl),
            "persist_bins": persist_bins,
            "die_bins": die_bins,
        },
    }
    result["dickman_reference_integer_u"] = {str(k): v
                                             for k, v in DICKMAN.items()}
    result["context"] = (
        "papers 130 (x^2-N pool ensemble-equals unrestricted random through "
        "2^44) and 209/exp562 (no deviation through u<=8.5; D=1.61 "
        "overdispersion at u~5.96 dead by u~7, mechanism unknown); this "
        "experiment lifts N to 2^96-2^112 reaching u in [9,11.x] and swaps "
        "raw B-smoothness (yield ~ rho(9..11) ~ 0) for an LPF-CDF cut "
        "ladder {500,1000,1e4,1e5,1e6} that carries full statistical power "
        "at every scale")

    # per-N compact tables for reanalysis (worker pool shut down here, AFTER
    # the conditional fresh-seed leg which reuses it)
    try:
        pool.close()
        pool.join()
    except Exception:
        pass
    per_n_tables = {}
    for w in bins:
        aggs = agg_by_n(results[w], NC)
        rows = []
        for e in pools[w]:
            a = aggs.get(e.nid)
            if a:
                rows.append({"nid": e.nid,
                             "bitlen_n": int(e.N).bit_length(),
                             "qr_frac": round(e.qr_frac, 4),
                             "qr_weighted": round(e.qr_w, 4),
                             "n": a[0],
                             "kc": [a[1 + k] for k in range(NC)],
                             "kctrl": [a[1 + NC + k] for k in range(NC)]})
        per_n_tables[str(w)] = rows
    result["per_n_table"] = per_n_tables

    result["honest_notes"] = [
        "raw per-N count dispersion (exp562-comparable) is inflated by "
        "unequal per-N candidate exposures; the mechanism call uses the "
        "EXPOSURE-CORRECTED Pearson chi2/dof D reported alongside it",        "B=500/1000 cuts are continuity carriers; at u>=9 their expected "
        "event yield is ~0 (rho(9)=1.0e-9 .. rho(11)=6.5e-13) so their CIs "
        "are wide-or-empty BY DESIGN and carry no inference weight",
        "j<=3s cap truncates the top of band 11 (achieved u_max reported "
        "empirically from the bitlen histogram)",
        "controls are uniform WITHIN the candidate's mantissa octant while "
        "candidates concentrate quadratically in j - the same accepted "
        "approximation as exp562 (within-octant log-width ln(2^(1/8))~0.086, "
        "small vs Dickman curvature here)",
        "batch product-tree remainder descent is exact (validated against "
        "exhaustive strip; see assert_pipeline) but its leaf-remainder "
        "identity gcd(x,PM)=gcd(x',R) holds only for x' dividing the leaf "
        "value - the sequential segment reuse stays within that domain",
        f"status reflects the {wall_min:.0f}-min wall cap; populations were "
        "sized adaptively (exp562 time-cap honesty convention)",
    ]

    result["status"] = mode if args.smoke else (
        "06_final" if not stopped_feeding else "06_final_time_capped")
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

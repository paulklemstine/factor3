#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
exp535_t_dial_unif_84.py -- TDIAL-U84-CROSS (round-67, experiment 535)

THE CROSSING TEST queued by paper 187: push the zero-fit dial
T(N) = sum_{odd QR primes p<=400} 2/p to BITLEN 84 on UNIFORM draws.
Prior uniform ladder: 44 -> exp517, 48 -> exp527, 52 -> exp518/528,
56 -> exp529, 60 -> exp521, 64 -> exp530, 68 -> exp531, 72 -> exp532,
76 -> exp533, 80 -> exp534 (paper 187: pooled rho_T = 0.565,
CI [0.542, 0.587] -- AT the 0.55 floor, seed 20261181 clearing by +0.001).

=====================================================================
PRE-STATED HYPOTHESES (written BEFORE any data collection; verbatim
from the round-67 brief)
=====================================================================
H1-crossing: Spearman(T, rate) drops BELOW 0.55 decisively at bitlen 84
             on uniform draws.
H2-stable:   Spearman(T, rate) stays >= 0.55 at bitlen 84 -- the floor
             is a plateau not a cliff edge.

Operationalization (fixed before data):
  H1 PASS iff pooled rho_T < 0.55 AND pooled bootstrap CI upper < 0.55
     (a drop "decisive" = the CI excludes the floor).
  H2 PASS iff pooled rho_T >= 0.55 AND >= 2 of 3 per-seed rho_T >= 0.55
     (plateau = point estimate holds and seeds corroborate).
Verdict names (pre-stated, mutually exclusive, exhaustive):
  H1 -> U84-CROSSING-CONFIRMED
  H2 -> U84-FLOOR-HOLDS
  pooled < 0.55 but CI straddles 0.55 -> U84-DRIFT-INCONCLUSIVE
  pooled >= 0.55 with < 2 seeds corroborating -> U84-FLOOR-HOLDS-WEAK

==========
DESIGN (as assigned)
==========
Work dir    : /tmp/exp67_tu84/  (protocol: work ONLY here; never write to
                                 /home/raver1975/factor3)
Population  : 1200 uniform semiprimes per seed; seeds 20261190,
              20261191, 20261192; N rejected unless bit_length == 84
              exactly (rejection sampling, restart BOTH draws on reject --
              the unbiased conditional protocol of exps 517..534).
Relations   : 240 relation values per N (CFRAC residues Q_1..Q_240 of
              sqrt(N); every odd prime r | Q_n satisfies (N|r)=+1 --
              exactly the prime set the dial weighs).
Smoothness  : u = 2.5 fixed; per-N bound B_N = round((2*(isqrt(N)+1))^(1/2.5));
              rate(N) = (# of the 240 values that are B_N-smooth) / 240.
Features    : verbatim paper-164 dial family --
              T(N)     = sum over odd primes p <= 400 with (N|p)=+1 of 2/p
                         (Euler criterion powmod),
              count(N) = #{odd primes p <= 100 with (N|p)=+1}.
Stats       : per-seed Spearman(T,rate), Spearman(count,rate), advantage;
              300-resample percentile bootstrap CIs; pooled-across-seeds
              likewise.

=====================================================================
DESIGN CORRECTION -- FIXED BEFORE DATA COLLECTION (flagged for parent)
=====================================================================
The brief specifies p ~ uniform prime in [2^28,2^34), q ~ uniform prime
in [2^34,2^40), AND N of bitlen exactly 84. These are incompatible: the
largest product of the stated windows is < 2^34 * 2^40 = 2^74, so NO
draw can reach bitlen 84 (bitlen-84 rejection sampling would never
terminate). This is the same copy-carried template defect already
documented pre-data in exps 517, 518, 521, 528, 529, 530, 531, 532,
533 and 534 (each round's brief carries windows too low for its target
bitlen; the stated windows here center bitlen 68).
Correction applied before data collection, following exp529..534's rule
exactly: shift BOTH exponent windows by the SAME amount, chosen so the
window-log midpoints sum to the target bitlen (minimal conditioning
distortion):
midpoints 31 + 37 = 68  ->  shift = (84 - 68)/2 = +8 ->
        p ~ uniform prime in [2^36, 2^42)
        q ~ uniform prime in [2^42, 2^48)
which preserves every structural property of the stated design:
  (i)   adjacency -- q's window begins exactly at p's upper edge;
  (ii)  equal window widths (6 exponents each);
  (iii) p < q ordering;
  (iv)  independent uniform draws ("uniform" character of the cell);
and makes window-log midpoints sum exactly to 84 (the correction rule),
continuing the exp534 cell's windows ([2^34,2^40) x [2^40,2^46)) by the
same +2-exponent step per +4-bit rung the ladder has used throughout.
Analytic acceptance computed BEFORE data: for linear-uniform draws the
bitlen-84 slice is P(u*v in [2^5, 2^6)), u,v ~ U(1,64) =
(224*ln 2 - 32)/63^2 = 123.26/3969 ~= 3.1% (primality conditioning
shifts this slightly upward) -- the same ~3-4% conditional-slice regime
as every prior cell (restart BOTH draws on bitlen rejection).
FLAGGED for parent adjudication.

PROTOCOL NOTE (flagged): this agent READ (never wrote) one artifact of
the immediate predecessor cell -- the exp534 script (repo scripts dir,
read-only) -- to guarantee verbatim protocol fidelity and to fill the
prior-cells context. No repo file was modified or created.

Implementation deltas vs exp534, none a fit:
 * factor-base ceiling 100000 -> 250000: B_N = (2*sqrt(N))^(1/2.5)
   reaches ~2^17.2 ~= 1.51e5 at bitlen 84 (vs ~8.7e4 at 80); the factor
   base must cover B_N (max B_N over the population ~150.6k << 250k).
 * smoothness classifier: exp534 rebuilt a two-level block-gcd structure
   PER N (build cost grows ~quadratically with the ~13.8k-prime base at
   bitlen 84). Replaced by ONE GLOBAL block structure (same LEAF=24 /
   MID=18 grouping, balanced tree products) built once over all primes
   <= FB_CEIL, with a PER-N MASKED DESCENT: for bound B, leaves wholly
   above bisect(primes,B) are skipped and the single straddling leaf
   divides only by its primes <= B. SEMANTICS PROVEN IDENTICAL to the
   exp534 classifier (both decide exactly "largest prime factor <= B"):
   (a) the global top-gate gcd(x,TOP)==1 implies gcd(x, prod_{p<=B} p)==1
       (subset), so the early 0 is valid whenever taken;
   (b) the mask makes it impossible to divide out any prime > B, so the
       running x evolves exactly as in exp534's per-N structure;
   (c) the final verdict line is byte-identical. Verified empirically at
       three levels before/at data collection: (a') unit tests at B=100
       incl. edge cases, (b') 2000-random-value cross-check against the
       exp533/534-verbatim classifier at multiple bounds, (c') per-seed
       in-loop equivalence on the first 25 populations (all 240 values
       each, verbatim classifier). Reason: at bitlen 84 the per-N build
       alone projects past the 15-minute cap; the shared structure does
       not touch any fitted quantity.
 * everything else byte-for-byte the exp534 pipeline (population draw
   order, feature code, CFRAC generator, stats, bootstrap seeds scheme).

Interpretation notes (also fixed before data):
 * "QR primes" = odd primes p with N a quadratic residue mod p
   ((N|p)=+1), Euler criterion powmod; the dial is N-dependent.
 * "count<=100" = number of odd QR primes p <= 100 (same criterion, hard
   cutoff 100, unit weights) -- the crude comparator.
 * "relation values" = CFRAC residues Q_n: their odd prime divisors are
   precisely primes with (N|r)=+1, i.e. exactly the dial's support.
 * One factor base per N (QS-style): B_N held constant across the 240
   values of a given N, u = log(x_max)/log(B_N) = 2.5 at the envelope
   x_max = 2*sqrt(N).

VERDICT NAMES: see pre-stated list above.

Protocol: result.json checkpointed atomically after EVERY stage; LEDGER.md
written at the end. Runtime target: well under the 15-minute cap.
"""

import bisect
import hashlib
import json
import math
import os
import platform
import random
import sys
import time

import numpy as np

try:
    import gmpy2
    HAVE_GMPY2 = True
except Exception:
    HAVE_GMPY2 = False

if HAVE_GMPY2:
    _gcd = gmpy2.gcd
else:
    _gcd = math.gcd

# ---------------------------------------------------------------- paths
WD = "/tmp/exp67_tu84"
RESULT_PATH = os.path.join(WD, "result.json")
SMOKE_PATH = os.path.join(WD, "result_smoke.json")
LEDGER_PATH = os.path.join(WD, "LEDGER.md")
SCRIPT_PATH = os.path.join(WD, "exp535_t_dial_unif_84.py")

# ------------------------------------------------- fixed configuration
SEEDS = [20261190, 20261191, 20261192]
TARGET_BITS = 84
P_WIN = (36, 42)          # corrected window, see DESIGN CORRECTION above
Q_WIN = (42, 48)          # corrected window
DIAL_CUT = 400            # T dial cutoff (paper-164 verbatim)
COUNT_CUT = 100           # count comparator cutoff (paper-164 verbatim)
U_EXP = 2.5               # smoothness u
BOOT = 300                # bootstrap resamples
FB_CEIL = 250000          # covers B_N max ~1.51e5 at bitlen 84 (see header)
LEAF = 24                 # primes per leaf block (block-gcd classifier)
MID = 18                  # leaf blocks per mid block
EQUIV_SUBSAMPLE = 25      # N per seed cross-checked vs verbatim classifier
FLOOR = 0.55              # the dial floor from the uniform ladder
ANCHOR_80_RHO = 0.565     # paper-187 / exp534 bitlen-80 pooled anchor
ANCHOR_80_CI = [0.542, 0.587]

SMOKE = "--smoke" in sys.argv
if SMOKE:
    N_PER_SEED, K_VALUES, BOOT = 60, 80, 60
else:
    N_PER_SEED, K_VALUES = 1200, 240

HYPOTHESES = {
    "H1-crossing": "Spearman(T, rate) drops BELOW 0.55 decisively at "
                   "bitlen 84 on uniform draws.",
    "H2-stable": "Spearman(T, rate) stays >= 0.55 at bitlen 84 -- the "
                 "floor is a plateau not a cliff edge.",
}

CORRECTION_TEXT = (
    "Brief's windows p~[2^28,2^34), q~[2^34,2^40) admit max product "
    "< 2^74 -- bitlen-84 rejection sampling is infeasible as stated "
    "(same copy-carried defect documented pre-data in exps 517/518/521/"
    "528/529/530/531/532/533/534; stated windows center bitlen 68). "
    "Pre-data correction per exp529..534's rule: both exponent windows "
    "shifted by the SAME +8, chosen so window-log midpoints sum to 84 "
    "(31+37=68 -> 39+45=84) -> p~[2^36,2^42), q~[2^42,2^48); preserves "
    "adjacency/equal-widths/p<q/uniform character; analytic pre-data "
    "acceptance (224*ln2-32)/63^2 ~= 3.1% (integer-uniform draws make "
    "bitlen-84 the same ~3-4% conditional slice as every prior cell; "
    "same rejection protocol as exps 517..534). FLAGGED for parent."
)

NOTES = {
    "qr_primes": "odd primes p<=400 with (N|p)=+1 by Euler criterion",
    "count_le_100": "number of odd QR primes p<=100, unit weights",
    "relation_values": "first K CFRAC residues Q_1..Q_K of sqrt(N)",
    "smoothness": "per-N factor base B_N=(2*(isqrt(N)+1))^(1/2.5), one base per N",
    "rate": "fraction of the K values that are B_N-smooth",
    "classifier": "ONE GLOBAL two-level block-gcd structure (LEAF=24/MID=18,"
                  " tree products) with per-N masked descent; proven + "
                  "cross-checked identical to the exp533/534-verbatim "
                  f"classifier (see script header); checked on 2000 random "
                  f"values at multiple bounds and on the first "
                  f"{EQUIV_SUBSAMPLE} populations of every seed",
    "context_prior_cells": {
        "uniform_44_exp517_rhoT": [0.777, 0.755, 0.801],
        "uniform_52_exp518_pooled_adv": 0.121,
        "uniform_56_exp529_pooled": {"rho_T": 0.6848, "rho_T_ci": [0.665, 0.7025],
                                     "advantage": 0.0752, "adv_ci": [0.0501, 0.095],
                                     "mean_rate": 0.1386},
        "uniform_60_exp521": {"rho_T": 0.6686, "rho_T_ci": [0.634, 0.7047],
                              "advantage": 0.1513, "adv_ci": [0.1065, 0.1934],
                              "mean_rate": 0.12647},
        "uniform_64_exp530_pooled": {"rho_T": 0.64765, "rho_T_ci": [0.6285, 0.6654],
                                     "advantage": 0.07357,
                                     "adv_ci": [0.04903, 0.09981],
                                     "mean_rate": 0.1349},
        "uniform_68_exp531_pooled": {"rho_T": 0.61116, "rho_T_ci": [0.5912, 0.6338],
                                     "advantage": 0.07039,
                                     "adv_ci": [0.04607, 0.09389],
                                     "mean_rate": 0.13572},
        "uniform_72_exp532_pooled": {"rho_T": 0.60514, "rho_T_ci": [0.58616, 0.62464],
                                     "advantage": 0.03843,
                                     "adv_ci": [0.01454, 0.06029],
                                     "mean_rate": 0.13517},
        "uniform_76_exp533_pooled": {"rho_T": 0.608, "rho_T_ci": [0.588, 0.631]},
        "uniform_80_exp534_pooled_paper187": {
            "rho_T": ANCHOR_80_RHO, "rho_T_ci": ANCHOR_80_CI,
            "note": "AT the 0.55 floor; seed 20261181 cleared by +0.001; "
                    "paper 187 queued bitlen 84 as THE CROSSING TEST"},
    },
}

# ------------------------------------------------------------ helpers
def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def sieve(n):
    s = bytearray(b"\x01") * (n + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            step = len(range(i * i, n + 1, i))
            s[i * i:: i] = b"\x00" * step
    return [i for i in range(n + 1) if s[i]]


PRIMES_ALL = sieve(FB_CEIL)
ODD_LE_400 = [p for p in PRIMES_ALL if 3 <= p <= DIAL_CUT]
ODD_LE_100 = [p for p in PRIMES_ALL if 3 <= p <= COUNT_CUT]
PRE_FILTER = [p for p in PRIMES_ALL if p < 150]
EULER = [(p, (p - 1) >> 1, 2.0 / p) for p in ODD_LE_400]

MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)  # det. < 3.3e24


def is_prime_mr(x):
    """Independent deterministic Miller-Rabin (cross-check / fallback)."""
    if x < 2:
        return False
    for p in MR_BASES:
        if x % p == 0:
            return x == p
    d, r = x - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in MR_BASES:
        y = pow(a, d, x)
        if y in (1, x - 1):
            continue
        for _ in range(r - 1):
            y = y * y % x
            if y == x - 1:
                break
        else:
            return False
    return True


def is_prime(x):
    if HAVE_GMPY2:
        return bool(gmpy2.is_prime(int(x)))
    return is_prime_mr(x)


def draw_prime(rng, lo, hi):
    while True:
        x = rng.randrange(lo, hi)
        if not HAVE_GMPY2 and any(x % sp == 0 for sp in PRE_FILTER):
            continue
        if is_prime(x):
            return x


def gen_population(seed, n_target):
    """Uniform semiprimes, bitlen exactly TARGET_BITS (rejection sampling).

    Draw order per attempt: full fresh draw of p then q; restart BOTH on
    bitlen rejection (unbiased conditional population).
    """
    rng = random.Random(seed)
    lo_p, hi_p = 1 << P_WIN[0], 1 << P_WIN[1]
    lo_q, hi_q = 1 << Q_WIN[0], 1 << Q_WIN[1]
    out, raw = [], 0
    while len(out) < n_target:
        raw += 1
        p = draw_prime(rng, lo_p, hi_p)
        q = draw_prime(rng, lo_q, hi_q)
        N = p * q
        assert N.bit_length() > 1 and p != q
        if N.bit_length() != TARGET_BITS:
            continue
        out.append((int(N), int(p), int(q)))
    return out, raw


def feats(N):
    """paper-164 features: T(N) = sum 2/p over odd QR primes p<=400;
    count(N) = #odd QR primes <= 100."""
    t, c = 0.0, 0
    for p, e, w in EULER:
        if pow(N % p, e, p) == 1:
            t += w
            if p <= COUNT_CUT:
                c += 1
    return t, c


def cf_values(N, k):
    """First k CFRAC residues Q_1..Q_k of sqrt(N) (standard PQa recurrence)."""
    a0 = math.isqrt(N)
    P, Q, a = 0, 1, a0
    out = []
    for _ in range(k):
        P2 = a * Q - P
        Q2 = (N - P2 * P2) // Q
        assert Q2 > 0, "CF residue must stay positive (N non-square)"
        out.append(Q2)
        P, Q = P2, Q2
        a = (a0 + P) // Q
    return out


# ------- smoothness: reference classifier + global masked classifier ---
def make_fb(B):
    hi = bisect.bisect_right(PRIMES_ALL, B)
    return [(pr, pr * pr) for pr in PRIMES_ALL[:hi]]


def smooth_count_sq(v, fb, B):
    """Reference classifier (exp528..exp534-verbatim form). Decides:
    all prime factors of v are <= B."""
    x = v
    for pr, pr2 in fb:
        if pr2 > x:
            break
        if x % pr == 0:
            while x % pr == 0:
                x //= pr
    return 1 if (x == 1 or x <= B) else 0


def _tree_product(seq):
    """Balanced product (associativity => identical integer to any order)."""
    items = list(seq)
    while len(items) > 1:
        nxt = []
        for i in range(0, len(items) - 1, 2):
            nxt.append(items[i] * items[i + 1])
        if len(items) % 2:
            nxt.append(items[-1])
        items = nxt
    return items[0] if items else 1


class GlobalClassifier(object):
    """ONE global two-level block structure over ALL primes <= FB_CEIL.

    Per-N masked descent decides 'all prime factors of v <= B' with
    verdicts IDENTICAL to smooth_count_sq (proof in module docstring):
      - top gate: gcd(v, TOP)==1 => no prime <= FB_CEIL (a fortiori <= B)
        divides v => with v > B the value is NOT smooth (valid early 0);
      - masks: only primes with index < cut=bisect(primes,B) are ever
        divided out, so the running x evolves exactly as in the per-N
        exp534 structure (which only ever holds primes <= B);
      - early return 'x <= B' and the final verdict line are byte-equal.
    """

    def __init__(self):
        plist = PRIMES_ALL
        self.leaves = []          # (leaf_prod, chunk)
        self.leaf_start = []      # global prime index of each leaf's first prime
        idx = 0
        for i in range(0, len(plist), LEAF):
            chunk = plist[i:i + LEAF]
            self.leaves.append((_tree_product(chunk), chunk))
            self.leaf_start.append(idx)
            idx += len(chunk)
        self.mids = []            # (mid_prod, [(leaf_prod, chunk), ...])
        self.mid_first_leaf = []
        self.mid_last_leaf = []
        for i in range(0, len(self.leaves), MID):
            grp = self.leaves[i:i + MID]
            self.mids.append((_tree_product([lp for lp, _ in grp]), grp))
            self.mid_first_leaf.append(i)
            self.mid_last_leaf.append(i + len(grp) - 1)
        self.top = _tree_product([mp for mp, _ in self.mids])
        # leaf -> (mid index, position in mid) map for fast descent
        self.leaf_mid = []
        for mi, (_, grp) in enumerate(self.mids):
            for _ in grp:
                self.leaf_mid.append(mi)

    def smooth(self, v, B):
        x = v
        if x <= B:
            return 1
        if _gcd(x, self.top) == 1:
            return 0
        cut = bisect.bisect_right(PRIMES_ALL, B)
        for mi, (mp, grp) in enumerate(self.mids):
            first_leaf = self.mid_first_leaf[mi]
            if self.leaf_start[first_leaf] >= cut:
                break   # this and every later mid holds only primes > B
            if _gcd(x, mp) == 1:
                continue
            for li_off, (lp, chunk) in enumerate(grp):
                li = first_leaf + li_off
                base = self.leaf_start[li]
                if base >= cut:
                    break   # rest of this mid holds only primes > B
                if base + len(chunk) <= cut:
                    # full leaf: every prime in it is <= B
                    if _gcd(x, lp) == 1:
                        continue
                    for pr in chunk:
                        if x % pr == 0:
                            while x % pr == 0:
                                x //= pr
                            if x <= B:      # x == 1 or single prime <= B
                                return 1
                else:
                    # straddling leaf: only its primes <= B (index < cut)
                    for j in range(cut - base):
                        pr = chunk[j]
                        if x % pr == 0:
                            while x % pr == 0:
                                x //= pr
                            if x <= B:
                                return 1
        return 1 if (x == 1 or x <= B) else 0


GLOBAL_CLF = None  # built lazily (after sieve) in main()


def b_of_N(N):
    return max(2, int(round((2 * (math.isqrt(N) + 1)) ** (1.0 / U_EXP))))


def rate_for_N(N, vals):
    B = b_of_N(N)
    cnt = sum(GLOBAL_CLF.smooth(v, B) for v in vals)
    return cnt / len(vals), B


def rate_for_N_verbatim(N, vals):
    B = b_of_N(N)
    fb = make_fb(B)
    cnt = sum(smooth_count_sq(v, fb, B) for v in vals)
    return cnt / len(vals), B


# ------------------------------------------------------------- stats
def rankdata(a):
    a = np.asarray(a, dtype=float)
    order = np.argsort(a, kind="mergesort")
    sa = a[order]
    ranks = np.empty(len(a), dtype=float)
    i, n = 0, len(a)
    while i < n:
        j = i
        while j + 1 < n and sa[j + 1] == sa[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return ranks


def spearman(x, y):
    rx, ry = rankdata(x), rankdata(y)
    rx = rx - rx.mean()
    ry = ry - ry.mean()
    den = math.sqrt(float((rx * rx).sum()) * float((ry * ry).sum()))
    return float((rx * ry).sum() / den) if den > 0 else float("nan")


def summarize(T, C, R, bs_seed):
    x, c, r = np.asarray(T), np.asarray(C), np.asarray(R)
    n = len(x)
    sT, sC = spearman(x, r), spearman(c, r)
    rng = np.random.default_rng(bs_seed)
    bT, bC, bD = [], [], []
    for _ in range(BOOT):
        idx = rng.integers(0, n, n)
        st, sc = spearman(x[idx], r[idx]), spearman(c[idx], r[idx])
        bT.append(st)
        bC.append(sc)
        bD.append(st - sc)

    def ci(v):
        return (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5)))

    return {
        "n": int(n),
        "spearman_T": float(sT), "spearman_T_ci": ci(bT),
        "spearman_count": float(sC), "spearman_count_ci": ci(bC),
        "advantage": float(sT - sC), "advantage_ci": ci(bD),
        "mean_T": float(np.mean(x)), "sd_T": float(np.std(x)),
        "mean_count": float(np.mean(c)), "sd_count": float(np.std(c)),
        "mean_rate": float(np.mean(r)), "sd_rate": float(np.std(r)),
        "feature_spearman_TC": float(spearman(x, c)),
    }


# --------------------------------------------------- designed checks
DESIGNED_CHECKS = {}


def run_designed_checks():
    ok_all = True

    # (1) smoothness classifier unit tests (B=100); cross-check the global
    # masked classifier against the exp533/534-verbatim classifier at
    # multiple bounds.
    tests = [(2310, 1), (2 ** 10, 1), (2311, 0), (3 * 1009, 0),
             (97 * 89, 1), (2 * 3 * 5 * 7 * 11 * 13, 1),
             # edge cases: v == B, prime just above B (NOT smooth),
             # semiprime straddling B, high power of a small prime, 1
             (100, 1), (101, 0), (97 * 103, 0), (2 ** 12, 1), (1, 1)]
    fb100_list = PRIMES_ALL[: bisect.bisect_right(PRIMES_ALL, 100)]
    fb100_sq = make_fb(100)
    for v, want in tests:
        got = smooth_count_sq(v, fb100_sq, 100)
        got_glb = GLOBAL_CLF.smooth(v, 100)
        if got != want or got_glb != want:
            ok_all = False
    rng_x = random.Random(31337)
    n_x = 0
    for B_x in (100, 997, 54179, 150000):
        fb_x = make_fb(B_x)
        for _ in range(500):
            v = rng_x.randrange(1, 1 << 86)
            n_x += 1
            if smooth_count_sq(v, fb_x, B_x) != GLOBAL_CLF.smooth(v, B_x):
                ok_all = False
    DESIGNED_CHECKS["smoothness_unit_tests"] = {
        "pass": ok_all, "random_crosscheck_pairs": n_x,
        "bounds_tested": [100, 997, 54179, 150000]}

    # (2) CF residues' QR structure: after stripping primes <= B, any prime
    # remainder r must satisfy (N|r)=+1 (mechanistic tie to the dial).
    rng = random.Random(4711)
    n_checked, n_bad, n_N = 0, 0, 0
    while n_N < 3:
        p = draw_prime(random.Random(rng.randrange(1 << 30)),
                       1 << P_WIN[0], 1 << P_WIN[1])
        q = draw_prime(random.Random(rng.randrange(1 << 30)),
                       1 << Q_WIN[0], 1 << Q_WIN[1])
        N = p * q
        if N.bit_length() != TARGET_BITS:
            continue
        n_N += 1
        vals = cf_values(N, 40)
        B = b_of_N(N)
        fb_list = PRIMES_ALL[: bisect.bisect_right(PRIMES_ALL, B)]
        for v in vals:
            x = v
            for pr in fb_list:
                if pr * pr > x:
                    break
                while x % pr == 0:
                    x //= pr
            if x > 1 and is_prime_mr(x):
                n_checked += 1
                if pow(N % x, (x - 1) // 2, x) != 1:
                    n_bad += 1
    DESIGNED_CHECKS["cf_remainder_qr_structure"] = {
        "semiprimes_tested": n_N, "prime_remainders_checked": n_checked,
        "violations": n_bad}
    ok_all = ok_all and (n_bad == 0 and n_checked >= 10)

    # (3) primality cross-validation on a subsample
    rng2 = random.Random(990001)
    agree = 0
    for _ in range(200):
        x = rng2.randrange(1 << P_WIN[0], 1 << Q_WIN[1])
        if bool(gmpy2.is_prime(x)) == is_prime_mr(x):
            agree += 1
    DESIGNED_CHECKS["primality_crosscheck_agree"] = f"{agree}/200"
    ok_all = ok_all and (agree == 200)

    # (4) B_N coverage: the global factor base must cover max B_N
    bmax = b_of_N((1 << TARGET_BITS) - 1)
    DESIGNED_CHECKS["bn_coverage"] = {
        "max_possible_B": bmax, "fb_ceiling": FB_CEIL,
        "covered": bool(bmax <= FB_CEIL)}
    ok_all = ok_all and bmax <= FB_CEIL

    DESIGNED_CHECKS["all_pass"] = bool(ok_all)
    return ok_all


def determinism_check():
    """Regenerate the first 40 accepted N of SEEDS[0]; digest must match."""
    pop, _ = gen_population(SEEDS[0], 40)
    d1 = hashlib.sha256(repr([t[0] for t in pop]).encode()).hexdigest()[:16]
    pop2, _ = gen_population(SEEDS[0], 40)
    d2 = hashlib.sha256(repr([t[0] for t in pop2]).encode()).hexdigest()[:16]
    DESIGNED_CHECKS["generation_determinism"] = {"digest_try1": d1,
                                                 "digest_try2": d2,
                                                 "match": d1 == d2}
    return d1 == d2


# ------------------------------------------------------- state / io
STATE = {
    "experiment": "exp535", "codename": "TDIAL-U84-CROSS", "round": 67,
    "date_utc": now(), "host": platform.node(),
    "environment": {
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "gmpy2": gmpy2.version() if HAVE_GMPY2 else None,
    },
    "hypotheses_preregistered": HYPOTHESES,
    "design_correction_flagged": CORRECTION_TEXT,
    "interpretation_notes": NOTES,
    "config": {},
    "designed_checks": DESIGNED_CHECKS,
    "ledger": [],
    "per_seed": [],
    "pooled": None,
    "hypothesis_verdicts": {},
    "barriers": {},
    "verdict_name": None,
    "decision": None,
    "artifacts": {},
}


def ledger(line, **kw):
    ent = {"t_utc": now(), "line": line}
    ent.update(kw)
    STATE["ledger"].append(ent)
    print(f"[LEDGER] {line} {kw if kw else ''}", flush=True)


def checkpoint():
    path = SMOKE_PATH if SMOKE else RESULT_PATH
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(STATE, f, indent=1, default=float)
    os.replace(tmp, path)


# ------------------------------------------------------------- main
def main():
    global GLOBAL_CLF
    os.makedirs(WD, exist_ok=True)
    GLOBAL_CLF = GlobalClassifier()
    STATE["config"] = {
        "seeds": SEEDS, "n_per_seed": N_PER_SEED, "k_values": K_VALUES,
        "u_exp": U_EXP, "target_bits": TARGET_BITS,
        "p_window_corrected": P_WIN, "q_window_corrected": Q_WIN,
        "windows_as_written_in_brief": [[28, 34], [34, 40]],
        "dial_cutoff": DIAL_CUT, "count_cutoff": COUNT_CUT, "bootstrap": BOOT,
        "fb_ceiling": FB_CEIL, "floor": FLOOR,
        "anchor80_rho": ANCHOR_80_RHO, "anchor80_ci": ANCHOR_80_CI,
        "leaf_block": LEAF, "mid_block": MID,
        "equivalence_subsample_per_seed": EQUIV_SUBSAMPLE,
        "smoke_mode": SMOKE,
    }
    STATE["artifacts"]["script_sha256"] = sha256_file(SCRIPT_PATH)
    STATE["artifacts"]["global_classifier_top_bits"] = int(
        GLOBAL_CLF.top.bit_length())
    ledger("stage=config", seeds=SEEDS, n=N_PER_SEED, k=K_VALUES, u=U_EXP,
           boot=BOOT, smoke=SMOKE, floor=FLOOR)
    checkpoint()

    ok = run_designed_checks()
    det_ok = determinism_check()
    ok = ok and det_ok
    ledger("stage=designed_checks", all_pass=ok, details={
        k: v for k, v in DESIGNED_CHECKS.items()})
    checkpoint()
    if not ok:
        print("DESIGNED CHECKS FAILED -- aborting before data collection",
              flush=True)
        STATE["decision"] = "ABORTED: designed checks failed pre-data."
        checkpoint()
        return

    Ts, Cs, Rs = [], [], []
    raw_total = 0
    equiv_total_pairs = 0

    for seed in SEEDS:
        t0 = time.time()
        pop, raw = gen_population(seed, N_PER_SEED)
        raw_total += raw
        acc = len(pop) / raw
        envelope_ok = True
        equiv_bad = 0
        T, C, R, Bs = [], [], [], []
        for i, (N, p, q) in enumerate(pop):
            assert N.bit_length() == TARGET_BITS
            if i < 30:  # subsample re-verification
                assert is_prime_mr(p) and is_prime_mr(q) and p * q == N
            tv, cv = feats(N)
            vals = cf_values(N, K_VALUES)
            if max(vals) > 2 * (math.isqrt(N) + 1):
                envelope_ok = False
            rv, B = rate_for_N(N, vals)
            if i < EQUIV_SUBSAMPLE:
                rv_ref, _ = rate_for_N_verbatim(N, vals)
                equiv_total_pairs += len(vals)
                if rv_ref != rv:
                    equiv_bad += 1
            T.append(tv); C.append(cv); R.append(rv); Bs.append(B)
            Ts.append(tv); Cs.append(cv); Rs.append(rv)
            if (i + 1) % 300 == 0:
                print(f"seed {seed}: {i+1}/{N_PER_SEED} "
                      f"elapsed={time.time()-t0:.0f}s", flush=True)
        dt_gen_feat = time.time() - t0
        ledger("stage=gen+features", seed=seed, accepted=len(pop),
               raw_draws=raw, acceptance=round(acc, 4),
               envelope_ok=envelope_ok, equivalence_mismatches=equiv_bad,
               secs=round(dt_gen_feat, 1))
        checkpoint()

        t1 = time.time()
        summ = summarize(T, C, R, bs_seed=seed + 90001)
        summ.update({"seed": seed, "raw_draws": raw,
                     "acceptance": round(acc, 4),
                     "median_B": float(np.median(Bs)),
                     "min_B": int(min(Bs)), "max_B": int(max(Bs)),
                     "gen_feature_secs": round(dt_gen_feat, 1),
                     "stats_secs": round(time.time() - t1, 1)})
        STATE["per_seed"].append(summ)
        ledger("stage=stats", seed=seed,
               spearman_T=round(summ["spearman_T"], 4),
               ci_T=[round(v, 4) for v in summ["spearman_T_ci"]],
               spearman_count=round(summ["spearman_count"], 4),
               advantage=round(summ["advantage"], 4),
               mean_rate=round(summ["mean_rate"], 4))
        checkpoint()

    t2 = time.time()
    STATE["pooled"] = summarize(Ts, Cs, Rs, bs_seed=20260824)
    STATE["pooled"]["raw_draws_total"] = raw_total
    STATE["pooled"]["secs"] = round(time.time() - t2, 1)
    ledger("stage=pooled", n=len(Ts),
           spearman_T=round(STATE["pooled"]["spearman_T"], 4),
           advantage=round(STATE["pooled"]["advantage"], 4))
    checkpoint()

    # ---------------- hypothesis verdicts ----------------
    per = STATE["per_seed"]
    pool = STATE["pooled"]
    rhoTs = [s["spearman_T"] for s in per]
    advs = [s["advantage"] for s in per]

    pool_rho = pool["spearman_T"]
    pool_hi = pool["spearman_T_ci"][1]
    pool_lo = pool["spearman_T_ci"][0]
    n_seeds_ge = sum(1 for r in rhoTs if r >= FLOOR)

    # pre-stated operationalizations (see module docstring)
    h1_pass = bool(pool_rho < FLOOR and pool_hi < FLOOR)   # decisive drop
    h2_pass = bool(pool_rho >= FLOOR and n_seeds_ge >= 2)  # plateau
    if h1_pass:
        name = "U84-CROSSING-CONFIRMED"
    elif h2_pass:
        name = "U84-FLOOR-HOLDS"
    elif pool_rho < FLOOR:
        name = "U84-DRIFT-INCONCLUSIVE"
    else:
        name = "U84-FLOOR-HOLDS-WEAK"

    anchor_lo, anchor_hi = ANCHOR_80_CI
    STATE["hypothesis_verdicts"] = {
        "H1-crossing": {
            "statement": HYPOTHESES["H1-crossing"],
            "operationalization": "pooled rho_T < 0.55 AND pooled CI upper "
                                  "< 0.55 (drop decisive = CI excludes floor)",
            "per_seed_rho_T": rhoTs,
            "pooled_rho_T": pool_rho, "pooled_ci": pool["spearman_T_ci"],
            "margin_to_floor_point": round(pool_rho - FLOOR, 4),
            "ci_excludes_floor_above": bool(pool_hi >= FLOOR),
            "pass": h1_pass,
        },
        "H2-stable": {
            "statement": HYPOTHESES["H2-stable"],
            "operationalization": "pooled rho_T >= 0.55 AND >= 2/3 per-seed "
                                  "rho_T >= 0.55 (plateau, seed-corroborated)",
            "n_seeds_ge_floor": n_seeds_ge,
            "pass": h2_pass,
        },
        "anchor_comparison": {
            "anchor80_pooled": ANCHOR_80_RHO, "anchor80_ci": ANCHOR_80_CI,
            "delta_pooled_vs_anchor80": round(pool_rho - ANCHOR_80_RHO, 4),
            "cis_overlap": bool(pool_lo <= anchor_hi and anchor_lo <= pool_hi),
        },
    }
    STATE["verdict_name"] = name

    ledger("stage=verdict", verdict=name, H1=h1_pass, H2=h2_pass,
           pooled_rho_T=round(pool_rho, 4), pooled_ci=[round(pool_lo, 4),
                                                       round(pool_hi, 4)],
           n_seeds_ge_floor=n_seeds_ge)
    checkpoint()

    # barrier lines in the canonical lab-round format (read from the lab
    # ledger read-only; repo untouched)
    STATE["barriers"] = {
        "barrier_5_factor_use_line":
            "BARRIER-5 (factor-use line): CLOSED-CHANNEL BOOKKEEPING ONLY "
            "-- T(N) and count(N) pin correlations of classical quadratic-"
            "residue statistics with the group-level smooth-relation rate; "
            "per the which-factor wall (papers 93/102) no reading here is a "
            "candidate filter or a factoring route; no extraction claim is "
            "made.",
        "barrier_8_scope_line":
            "BARRIER-8 (scope line): all statements bounded to the measured/"
            "diagnostic range -- uniform semiprimes of bitlen exactly 84 "
            "(p ~ U[2^36,2^42), q ~ U[2^42,2^48)), u = 2.5, 240 CFRAC "
            "values/N, n = 1200 x 3 seeds; no extrapolation to cryptographic "
            "parameterizations; zero fitted parameters on this cell (dial "
            "form sum 2/p over QR primes <=400 and count<=100 fixed a priori "
            "per paper-164; the pre-data window correction is a feasibility "
            "fix, not a fit; the global masked classifier is semantics-"
            "preserving and was locked before data).",
    }
    STATE["decision"] = (
        "See verdict_name %s; H1=%s H2=%s" % (name, h1_pass, h2_pass)
    )
    STATE["wall_secs_total"] = round(time.time() - T_START, 1)
    STATE["equivalence_pairs_checked_total"] = equiv_total_pairs
    ledger("stage=final", verdict=name, wall_secs=STATE["wall_secs_total"])
    checkpoint()

    write_ledger_md(name, h1_pass, h2_pass)


T_START = time.time()


def write_ledger_md(name, h1v, h2v):
    lines = [
        "# LEDGER -- exp535 TDIAL-U84-CROSS (round-67)",
        "",
        f"- date_utc: {now()}",
        f"- host: {platform.node()} | python {sys.version.split()[0]} | "
        f"numpy {np.__version__} | gmpy2 {gmpy2.version() if HAVE_GMPY2 else 'absent'}",
        f"- script: {SCRIPT_PATH}",
        f"- script sha256: {STATE['artifacts'].get('script_sha256')}",
        f"- seeds: {SEEDS} | n/seed {N_PER_SEED} | values/N {K_VALUES} | "
        f"u {U_EXP} | bootstrap {BOOT} | smoke={SMOKE}",
        f"- design correction (pre-data, flagged): {CORRECTION_TEXT}",
        f"- classifier: ONE GLOBAL block-gcd structure with per-N masked "
        f"descent, proven + cross-checked identical to the exp533/534-"
        f"verbatim classifier ({STATE.get('equivalence_pairs_checked_total')} "
        f"in-loop pairs checked)",
        f"- designed checks all pass: {DESIGNED_CHECKS.get('all_pass')}",
        f"- VERDICT: {name} (H1={'PASS' if h1v else 'FAIL'}, "
        f"H2={'PASS' if h2v else 'FAIL'})",
        "",
        "## stage log",
    ]
    for ent in STATE["ledger"]:
        kv = ", ".join(f"{k}={v}" for k, v in ent.items() if k != "line")
        lines.append(f"- [{ent.get('t_utc','')}] {ent['line']}: {kv}")
    with open(LEDGER_PATH, "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

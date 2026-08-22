#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
exp543_t_dial_unif_64.py -- TDIAL-U64B (round-62, experiment 543)

FRESH-SEED REPLICATION ("B") of the bitlen-64 UNIFORM-draw cell for the
zero-fit dial  T(N) = sum_{odd QR primes p<=400} 2/p.
Prior cell exp530 (round-60, seeds 20261140-42) returned
U64-DIAL-HOLDS-COUNT-PARITY (H1 pass pooled rho_T = 0.6477 CI [0.6285,
0.6654]; H2 failed -- pooled advantage 0.0736 above bar but per-seed
min 0.0456 and CI lower bound 0.0490 both under +0.05).
This run re-draws the SAME pre-stated cell with independent seeds
20261210-12 to test seed robustness of the bitlen-64 law and to give H2
a second, independent look at the razor-thin count comparison.

=====================================================================
PRE-STATED HYPOTHESES (written BEFORE any data collection)
=====================================================================
H1: Spearman(T, rate) stays within [0.55, 0.85] on uniform draws at
    bitlen 64, u = 2.5.
H2: T beats count<=100 by more than +0.05
    (advantage = rho_T - rho_count > +0.05).

==========
DESIGN (as assigned)
==========
Work dir    : /tmp/exp62_tu64b/   (protocol: work ONLY here; never write to
                                   /home/raver1975/factor3)
Population  : 1200 uniform semiprimes per seed; seeds 20261210, 20261211,
              20261212; N rejected unless bit_length == 64 exactly.
Relations   : 240 relation values per N (CFRAC residues Q_1..Q_240 of
              sqrt(N); every odd prime r | Q_n satisfies (N|r)=+1 -- exactly
              the prime set the dial weighs).
Smoothness  : u = 2.5 fixed; per-N bound B_N = round((2*(isqrt(N)+1))^(1/2.5));
              rate(N) = (# of the 240 values that are B_N-smooth) / 240.
Features    : verbatim paper-164 dial family --
              T(N)     = sum over odd primes p <= 400 with (N|p)=+1 of 2/p
                         (Euler criterion via powmod),
              count(N) = #{odd primes p <= 100 with (N|p)=+1}.
Stats       : per-seed Spearman(T,rate), Spearman(count,rate), advantage;
              300-resample percentile bootstrap CIs (paired resamples for
              the advantage); pooled-across-seeds estimates likewise.

=====================================================================
DESIGN CORRECTION -- FIXED BEFORE DATA COLLECTION (flagged for parent)
=====================================================================
The brief specifies p ~ uniform prime in [2^16,2^22), q ~ uniform prime in
[2^22,2^28), AND N of bitlen exactly 64. These are incompatible: the largest
product of the stated windows is < 2^22 * 2^28 = 2^50, so NO draw can reach
bitlen 64 (bitlen-64 rejection sampling would never terminate). This is the
same copy-carried template defect already documented pre-data in exps 517,
518, 521, 528, 529 and 530 (each round's brief carries windows two octaves
too low for its target bitlen); at bitlen 64 the correction is exactly the
one exp530 applied.
Correction applied before data collection, following exp530's rule exactly:
shift BOTH exponent windows by the SAME amount, chosen so the window-log
midpoints sum to the target bitlen (minimal conditioning distortion):
midpoints 19 + 25 = 44  ->  shift = (64 - 44)/2 = +10 ->
        p ~ uniform prime in [2^26, 2^32)
        q ~ uniform prime in [2^32, 2^38)
which preserves every structural property of the stated design:
  (i)   adjacency -- q's window begins exactly at p's upper edge;
  (ii)  equal window widths (6 exponents each);
  (iii) p < q ordering;
  (iv)  independent uniform draws ("uniform" character of the cell);
and places the product distribution's MODE exactly at 2^64 (window-log
midpoints 29 + 35 = 64). This makes the population identical-in-law to the
round-60 cell being replicated (exp530 used exactly these corrected
windows). Everything else in the brief is implemented verbatim. FLAGGED for
parent adjudication.

PROTOCOL NOTE (flagged): this agent READ (never wrote) two artifacts of the
immediate predecessor cell -- the exp530 script and its /tmp result.json
(both outside this workdir) -- to guarantee verbatim protocol fidelity and
to embed prior-cell context constants. No repo or foreign /tmp file was
modified or created.

Implementation deltas vs exp530: NONE beyond identifiers/seeds/workdir --
population draw order, feature code, CFRAC generator, classifier, stats,
bootstrap seeds scheme are byte-for-byte the exp530 pipeline (itself the
exp529 pipeline with sieve ceiling 20000, which covers B_N ~ 8.9e3 median /
~9.7e3 max at bitlen 64).

Interpretation notes (also fixed before data):
 * "QR primes" = odd primes p with N a quadratic residue mod p ((N|p)=+1),
   Euler criterion powmod; the dial is N-dependent by construction.
 * "count <=100" = number of odd QR primes p <= 100 (same criterion, hard
   cutoff 100, unit weights) -- the crude comparator named in H2.
 * "relation values" = CFRAC residues Q_n: their odd prime divisors are
   precisely primes with (N|r)=+1, i.e. exactly the dial's support, which is
   why this generation matches the paper-164 feature family.
 * One factor base per N (QS-style): B_N held constant across the 240 values
   of a given N, with u = log(x_max)/log(B_N) = 2.5 at the envelope
   x_max = 2*sqrt(N).

VERDICT NAMES (pre-stated):
  H1 pass & H2 pass -> U64B-DIAL-CONFIRMED
  H1 only           -> U64B-DIAL-HOLDS-COUNT-PARITY
  H2 only           -> U64B-DIAL-SHIFT-COUNT-ROBUST
  neither           -> U64B-DIAL-BREAK

Protocol: result.json checkpointed atomically after EVERY stage; ledger.md
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

# ---------------------------------------------------------------- paths
WD = "/tmp/exp62_tu64b"
RESULT_PATH = os.path.join(WD, "result.json")
SMOKE_PATH = os.path.join(WD, "result_smoke.json")
LEDGER_PATH = os.path.join(WD, "LEDGER.md")
SCRIPT_PATH = os.path.join(WD, "exp543_t_dial_unif_64.py")

# ------------------------------------------------- fixed configuration
SEEDS = [20261210, 20261211, 20261212]
TARGET_BITS = 64
P_WIN = (26, 32)          # corrected window, see DESIGN CORRECTION above
Q_WIN = (32, 38)          # corrected window
DIAL_CUT = 400            # T dial cutoff (paper-164 verbatim)
COUNT_CUT = 100           # count comparator cutoff (paper-164 verbatim)
U_EXP = 2.5               # smoothness u
BOOT = 300                # bootstrap resamples
SIEVE_CEIL = 20000        # covers B_N max ~9.7e3 at bitlen 64 (see header)

SMOKE = "--smoke" in sys.argv
if SMOKE:
    N_PER_SEED, K_VALUES, BOOT = 60, 80, 60
else:
    N_PER_SEED, K_VALUES = 1200, 240

HYPOTHESES = {
    "H1": "Spearman(T, rate) stays within [0.55, 0.85] on uniform draws at "
          "bitlen 64, u=2.5.",
    "H2": "T beats count<=100 by > +0.05 (advantage = rho_T - rho_count > 0.05).",
}

CORRECTION_TEXT = (
    "Brief's windows p~[2^16,2^22), q~[2^22,2^28) admit max product < 2^50 -- "
    "bitlen-64 rejection sampling is infeasible as stated (same copy-carried "
    "defect documented pre-data in exps 517/518/521/528/529/530). Pre-data "
    "correction per exp530's rule: both exponent windows shifted by the SAME "
    "+10, chosen so window-log midpoints sum to 64 (19+25=44 -> 29+35=64) -> "
    "p~[2^26,2^32), q~[2^32,2^38); preserves adjacency/equal-widths/p<q/"
    "uniform character; product-mode lands on 2^64; identical-in-law to the "
    "exp530 replication target. FLAGGED for parent."
)

NOTES = {
    "qr_primes": "odd primes p<=400 with (N|p)=+1 by Euler criterion",
    "count_le_100": "number of odd QR primes p<=100, unit weights",
    "relation_values": "first K CFRAC residues Q_1..Q_K of sqrt(N)",
    "smoothness": "per-N factor base B_N=(2*(isqrt(N)+1))^(1/2.5), one base per N",
    "rate": "fraction of the K values that are B_N-smooth",
    "context_prior_cells": {
        "uniform_56_exp529_pooled_rhoT": 0.6848,
        "uniform_56_exp529_pooled_advantage": 0.0752,
        "uniform_64_exp530_pooled": {"rho_T": 0.6477, "rho_T_ci": [0.6285, 0.6654],
                                     "advantage": 0.0736, "adv_ci": [0.0490, 0.0998],
                                     "mean_rate": 0.1349},
        "uniform_64_exp530_per_seed_rho_T": [0.6579, 0.6418, 0.6426],
        "uniform_64_exp530_per_seed_advantage": [0.0960, 0.0794, 0.0456],
    },
}

# ------------------------------------- prior-cell context (read-only source)
PRIOR_CELL = {
    "source": "/tmp/exp60_tu64/result.json (exp530, round-60)",
    "verdict": "U64-DIAL-HOLDS-COUNT-PARITY",
    "seeds": [20261140, 20261141, 20261142],
    "pooled_rho_T": 0.6476530793411688,
    "pooled_rho_T_ci": [0.6285019685484935, 0.6653921355251364],
    "pooled_advantage": 0.07357356422943195,
    "pooled_advantage_ci": [0.049027380243089294, 0.0998146053881807],
    "per_seed_rho_T": [0.6579, 0.6418, 0.6426],
    "per_seed_advantage": [0.09598288210229788, 0.07938646952325168,
                           0.04561502708289089],
    "mean_rate": 0.13494097222222223,
    "note": "context only, not part of this run's data",
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


PRIMES_ALL = sieve(SIEVE_CEIL)
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


def make_fb(B):
    hi = bisect.bisect_right(PRIMES_ALL, B)
    return [(pr, pr * pr) for pr in PRIMES_ALL[:hi]]


def smooth_count_sq(v, fb, B):
    """1 iff v is B-smooth. Invariant: after stripping all primes pr with
    pr*pr <= v, the remainder is 1 or a single prime. (Precomputed squares
    for speed; identical semantics to the exp528/529/530 classifier.)"""
    x = v
    for pr, pr2 in fb:
        if pr2 > x:
            break
        if x % pr == 0:
            while x % pr == 0:
                x //= pr
    return 1 if (x == 1 or x <= B) else 0


def smooth_count(v, fb_list, B):
    """Reference classifier (predecessor-verbatim form), used in unit tests."""
    x = v
    for pr in fb_list:
        if pr * pr > x:
            break
        if x % pr == 0:
            while x % pr == 0:
                x //= pr
    return 1 if (x == 1 or x <= B) else 0


def rate_for_N(N, vals):
    xmax = 2 * (math.isqrt(N) + 1)
    B = max(2, int(round(xmax ** (1.0 / U_EXP))))
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

    # (1) smoothness classifier unit tests (B=100); also cross-check the
    # precomputed-square fast path against the reference classifier.
    tests = [(2310, 1), (2 ** 10, 1), (2311, 0), (3 * 1009, 0),
             (97 * 89, 1), (2 * 3 * 5 * 7 * 11 * 13, 1)]
    fb100_list = PRIMES_ALL[: bisect.bisect_right(PRIMES_ALL, 100)]
    fb100_sq = make_fb(100)
    for v, want in tests:
        got = smooth_count(v, fb100_list, 100)
        got_sq = smooth_count_sq(v, fb100_sq, 100)
        if got != want or got_sq != want:
            ok_all = False
    rng_x = random.Random(31337)
    for _ in range(2000):
        v = rng_x.randrange(2, 1 << 24)
        if smooth_count(v, fb100_list, 100) != smooth_count_sq(v, fb100_sq, 100):
            ok_all = False
    DESIGNED_CHECKS["smoothness_unit_tests"] = ok_all

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
        B = max(2, int(round((2 * (math.isqrt(N) + 1)) ** (1.0 / U_EXP))))
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
    "experiment": "exp543", "codename": "TDIAL-U64B", "round": 62,
    "date_utc": now(), "host": platform.node(),
    "environment": {
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "gmpy2": gmpy2.version() if HAVE_GMPY2 else None,
    },
    "hypotheses_preregistered": HYPOTHESES,
    "design_correction_flagged": CORRECTION_TEXT,
    "interpretation_notes": NOTES,
    "prior_cell_context_read_only": PRIOR_CELL,
    "config": {},
    "designed_checks": DESIGNED_CHECKS,
    "ledger": [],
    "per_seed": [],
    "pooled": None,
    "hypothesis_verdicts": {},
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
    os.makedirs(WD, exist_ok=True)
    STATE["config"] = {
        "seeds": SEEDS, "n_per_seed": N_PER_SEED, "k_values": K_VALUES,
        "u_exp": U_EXP, "target_bits": TARGET_BITS,
        "p_window_corrected": P_WIN, "q_window_corrected": Q_WIN,
        "windows_as_written_in_brief": [[16, 22], [22, 28]],
        "dial_cutoff": DIAL_CUT, "count_cutoff": COUNT_CUT, "bootstrap": BOOT,
        "sieve_ceiling": SIEVE_CEIL, "smoke_mode": SMOKE,
    }
    STATE["artifacts"]["script_sha256"] = sha256_file(SCRIPT_PATH)
    ledger("stage=config", seeds=SEEDS, n=N_PER_SEED, k=K_VALUES, u=U_EXP,
           boot=BOOT, smoke=SMOKE)
    checkpoint()

    ok = run_designed_checks()
    det_ok = determinism_check()
    ok = ok and det_ok
    ledger("stage=designed_checks", all_pass=ok, determinism_match=det_ok,
           details={k: v for k, v in DESIGNED_CHECKS.items()})
    checkpoint()
    if not ok:
        print("DESIGNED CHECKS FAILED -- aborting before data collection",
              flush=True)
        STATE["decision"] = "ABORTED: designed checks failed pre-data."
        checkpoint()
        return

    Ts, Cs, Rs = [], [], []
    raw_total = 0

    for seed in SEEDS:
        t0 = time.time()
        pop, raw = gen_population(seed, N_PER_SEED)
        raw_total += raw
        acc = len(pop) / raw
        envelope_ok = True
        T, C, R, Bs = [], [], [], []
        for i, (N, p, q) in enumerate(pop):
            assert N.bit_length() == TARGET_BITS
            if i < 30:  # subsample re-verification of factorization
                assert is_prime_mr(p) and is_prime_mr(q) and p * q == N
            tv, cv = feats(N)
            vals = cf_values(N, K_VALUES)
            if max(vals) > 2 * (math.isqrt(N) + 1):
                envelope_ok = False
            rv, B = rate_for_N(N, vals)
            T.append(tv); C.append(cv); R.append(rv); Bs.append(B)
            Ts.append(tv); Cs.append(cv); Rs.append(rv)
            if (i + 1) % 300 == 0:
                print(f"seed {seed}: {i+1}/{N_PER_SEED} "
                      f"elapsed={time.time()-t0:.0f}s", flush=True)
        dt_gen_feat = time.time() - t0
        ledger("stage=gen+features", seed=seed, accepted=len(pop),
               raw_draws=raw, acceptance=round(acc, 4),
               envelope_ok=envelope_ok, secs=round(dt_gen_feat, 1))
        checkpoint()

        t1 = time.time()
        summ = summarize(T, C, R, bs_seed=seed + 90001)
        summ.update({"seed": seed, "raw_draws": raw,
                     "acceptance": round(acc, 4),
                     "median_B": float(np.median(Bs)),
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
           spearman_count=round(STATE["pooled"]["spearman_count"], 4),
           advantage=round(STATE["pooled"]["advantage"], 4))
    checkpoint()

    # ---------------- hypothesis verdicts ----------------
    per = STATE["per_seed"]
    pool = STATE["pooled"]
    rhoTs = [s["spearman_T"] for s in per]
    advs = [s["advantage"] for s in per]

    inside = lambda r: 0.55 <= r <= 0.85
    h1_per_inside = all(inside(r) for r in rhoTs)
    h1_pool_inside = inside(pool["spearman_T"])
    h1_margin_low = min(min(rhoTs), pool["spearman_T"]) - 0.55
    h1_margin_high = 0.85 - max(max(rhoTs), pool["spearman_T"])

    adv_lo = pool["advantage_ci"][0]
    h2_point = pool["advantage"] > 0.05
    h2_ci = adv_lo > 0.05
    h2_per_all = all(a > 0.05 for a in advs)

    STATE["hypothesis_verdicts"] = {
        "H1": {
            "statement": HYPOTHESES["H1"],
            "per_seed_rho_T": rhoTs, "pooled_rho_T": pool["spearman_T"],
            "pooled_ci": pool["spearman_T_ci"],
            "per_seed_all_inside": h1_per_inside,
            "pooled_inside": h1_pool_inside,
            "pass": bool(h1_per_inside and h1_pool_inside),
            "margin_to_lower_bound": round(h1_margin_low, 4),
            "margin_to_upper_bound": round(h1_margin_high, 4),
        },
        "H2": {
            "statement": HYPOTHESES["H2"],
            "per_seed_advantage": advs,
            "pooled_advantage": pool["advantage"],
            "pooled_advantage_ci": pool["advantage_ci"],
            "pass_point_estimate": bool(h2_point),
            "pass_ci_lower_bound": bool(h2_ci),
            "per_seed_all_above_005": h2_per_all,
            "pass": bool(h2_point and h2_per_all),
        },
    }

    # replication deltas vs prior cell (context, read-only source)
    STATE["hypothesis_verdicts"]["replication_delta_vs_exp530"] = {
        "delta_pooled_rho_T": round(float(pool["spearman_T"]
                                          - PRIOR_CELL["pooled_rho_T"]), 4),
        "delta_pooled_advantage": round(float(pool["advantage"]
                                              - PRIOR_CELL["pooled_advantage"]), 4),
        "six_seed_combined_note":
            "with exp530, the bitlen-64 uniform cell now has 6 seeds; "
            "combined evidence recorded in the parent ledger",
    }

    h1v = STATE["hypothesis_verdicts"]["H1"]["pass"]
    h2v = STATE["hypothesis_verdicts"]["H2"]["pass"]
    if h1v and h2v:
        name = "U64B-DIAL-CONFIRMED"
    elif h1v and not h2v:
        name = "U64B-DIAL-HOLDS-COUNT-PARITY"
    elif (not h1v) and h2v:
        name = "U64B-DIAL-SHIFT-COUNT-ROBUST"
    else:
        name = "U64B-DIAL-BREAK"
    STATE["verdict_name"] = name

    ledger("stage=verdict", verdict=name, H1=h1v, H2=h2v)
    checkpoint()

    # barrier lines (reconstructed to lab-standard semantics; the repo's
    # canonical barrier table was NOT modified -- read-only protocol note
    # in the script header)
    STATE["barriers"] = {
        "barrier_5_rate_label_wall":
            "BARRIER-5 (rate/label wall; structural orthogonality): T(N) "
            "predicts only the group-level smooth-relation RATE; it carries no "
            "which-factor information and is no candidate filter -- any "
            "Spearman value measured here leaves the which-factor/"
            "symmetric-channel wall untouched (residue dials only).",
        "barrier_8_zero_fit_discipline":
            "BARRIER-8 (zero-fit discipline; classical-invariant ceiling): "
            "dial form sum 2/p over QR primes <=400 and comparator count<=100 "
            "are fixed a priori with zero fitted parameters on this cell; "
            "bitlen-64-uniform fresh-seed replication is an out-of-sample "
            "intersection fill; no form/cutoff/weight was tuned against these "
            "data (the pre-data window correction is a feasibility fix, not a "
            "fit).",
        "note": "wording reconstructed from lab semantics (barrier 5 = "
                "residue-dials-only structural orthogonality, barrier 8 = "
                "classical Galois/reciprocity invariants), consistent with "
                "papers 83/183/184 usage and the exp529/exp530 wording; repo "
                "untouched (read-only).",
    }
    STATE["decision"] = (
        "See verdict_name %s; H1=%s H2=%s; replication deltas vs exp530 "
        "recorded." % (name, h1v, h2v)
    )
    STATE["wall_secs_total"] = round(time.time() - T_START, 1)
    ledger("stage=final", verdict=name)
    checkpoint()

    write_ledger_md(name, h1v, h2v)


T_START = time.time()


def write_ledger_md(name, h1v, h2v):
    lines = [
        "# LEDGER -- exp543 TDIAL-U64B (round-62)",
        "",
        f"- date_utc: {now()}",
        f"- host: {platform.node()} | python {sys.version.split()[0]} | "
        f"numpy {np.__version__} | gmpy2 {gmpy2.version() if HAVE_GMPY2 else 'absent'}",
        f"- script: {SCRIPT_PATH}",
        f"- script sha256: {STATE['artifacts'].get('script_sha256')}",
        f"- seeds: {SEEDS} | n/seed {N_PER_SEED} | values/N {K_VALUES} | "
        f"u {U_EXP} | bootstrap {BOOT} | smoke={SMOKE}",
        f"- design correction (pre-data, flagged): {CORRECTION_TEXT}",
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

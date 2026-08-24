#!/usr/bin/env python3
"""EXP 553 'TDIAL-U116' -- zero-fit dial T(N) pushed to bitlen 116, u=2.5.

PRE-STATED HYPOTHESES (written BEFORE any data generation; also checkpointed
to result.json at stage 00 before any population sampling -- verbatim from the
tasking brief):
  H1: Spearman(T, rate) stays within [0.55, 0.85] on uniform draws at
      bitlen 116, u=2.5.
  H2: T beats count <=100 by > +0.05.
  Carry-in priors (TDIAL-U ladder): pooled Spearman 0.5739 (fixed
      classifier) at bitlen 96; 0.5436, CI [0.4982, 0.5881] at bitlen 100;
      0.5005, CI [0.4557, 0.5454] at bitlen 104
      (TDIAL-U104-CONTINUES-FADE); 0.4880, CI [0.4453, 0.5337] at bitlen 108
      (TDIAL-U108-CONTINUES-FADE); 0.46213, CI [0.41471, 0.50815] at bitlen
      112 (TDIAL-U112-CONTINUES-FADE; step delta -0.0259 re-accelerated vs
      -0.0125). NOTE: H1's validated band [0.55, 0.85] is tested exactly as
      stated even though the last FOUR cells already sit BELOW its lower
      edge 0.55.

DESIGN (fixed before data):
  Population : 1200 uniform semiprimes = 3 seeds x 400
               (seeds 20261210, 20261211, 20261212).
               DESIGN NOTE / BRIEF CORRECTION: the tasking brief said to
               "scale the prime ranges x16 from exp545's U112 config ...
               keeping the same structure" (mentioning "[2^48,2^56]-
               equivalent"). A literal x16 on exp545's windows gives
               [2^54,2^60) x [2^60,2^66): those windows meet at 2^60, NOT at
               2^(B/2)=2^58, and place the accepted log-sum band [115,116)
               at the extreme bottom TAIL of the draw window (mean pair-sum
               exponent 120 vs target ~115.5), i.e. structurally unlike
               every prior rung, whose window mean equals B so accepted
               pairs are centrally sampled. The brief's own binding rule is
               "match the bitlen split used in prior rungs ... keeping the
               same structure": the established TDIAL-ladder convention
               (exp539..exp545, five consecutive cells) is width-6 octave
               windows meeting at 2^(B/2), every bound growing x4 (= +2
               exponent) per +4-bit rung -- the brief's "x16" matches the
               TWO-rung span (e.g. U104 p-low 2^46 -> U112 p-low 2^50).
               Corrected pre-data to HERE [2^52,2^58) x [2^58,2^64) for
               B=116. Same brief-typo family as exp541/exp544/exp545;
               recorded in result.json stage 00 and under barrier (8).
  Relations  : per N, 240 values V = (r + d)^2 - N with r = isqrt(N) and
               d uniform DISTINCT in [1, 256].
  Smoothness : per-N bound B_N = ceil(Vmax^(1/2.5)) where Vmax is the max of
               that N's 240 values, so u := ln(Vmax)/ln(B_N) = 2.5 exactly.
               V counts as smooth iff EVERY prime factor (2 included) <= B_N.
               Smoothness test is EXACT trial division over all primes <= B_N,
               restricted per-row to its OWN bound (exp540-fixed classifier:
               own-bound eligibility masks + expiry parking); no probabilistic
               factoring anywhere.
               CLASSIFIER STORAGE (retained from exp545, re-checked at 116):
               relation values reach 2rd + d^2 < 2^67.001 > 2^64-1, so single-
               uint64 storage would OVERFLOW; values are held as an exact
               34/34 split-word pair (V = VH*2^34 + VL, both uint64; capacity
               2^68 > observed Vmax ~ 2^67.0), every remainder/division step
               the standard exact long-division identity on the split
               (intermediate products bounded < 2^61), predicate bit-identical
               in semantics to exp544's. PLUS an independent Pollard-rho
               (Brent) full-factorization spot-check on a fixed 300-value
               subsample per seed (asserted mismatch-free; smoke checks EVERY
               value).
               NEW AT THIS RUNG (overflow fix, documented pre-data): the q
               draw window's upper bound is now exactly 2^64, so exp545's
               `.astype(np.int64)` post-processing of the raw uint64 draws
               would wrap candidates >= 2^63 NEGATIVE, and gmpy2.is_prime
               returns False for negatives -- silently discarding half the q
               window. Fixed by keeping the candidate array in uint64 and
               taking `.tolist()` (exact unsigned Python ints); the random
               stream itself is byte-identical to the template's.
  Features   : verbatim paper-164 --
               T(N)   = sum over odd primes p <= 400 with Euler criterion
                        powmod(N,(p-1)/2,p) == 1 of 2/p
               cnt(N) = #{odd primes p <= 100 : powmod(N,(p-1)/2,p) == 1}
  Statistics : per-seed Spearman(T,rate), Spearman(cnt,rate), advantage;
               pooled (n=1200) Spearmans with bootstrap CIs (300 resamples);
               paired bootstrap CI for the advantage.
  Verdict    : pre-stated names -- H1 pass -> U116-DIAL-HOLDS; H1 fail and
               |step delta| <= half the prior step (prior step -0.0259,
               half = 0.0130) -> U116-PLATEAU; H1 fail and further decline
               >= the prior step magnitude -> U116-CONTINUES-FADE; else
               U116-MIXED.
  Runtime    : per-seed rate computation parallelized as 3 seeds x 3 row-
               chunks = 9 fork-inherited workers (prime base and per-row
               offset draws made in the PARENT from one deterministic stream
               per seed, so chunking is a pure runtime optimization over
               exp545's sequential-per-seed loop).

BARRIERS (standard lines):
  (5) SCOPE: claims restricted to uniform semiprime draws at bitlen exactly
      116, u = 2.5, and this specific relation-value construction ((r+d)^2-N,
      d in [1,256]); no claim about structured N, neighbouring bitlens, or a
      production sieve.
  (8) MEASUREMENT: rate is a 240-sample smoothness proxy (binomial sigma
      ~= 0.03), not a sieved relation yield; T and cnt are scored against
      IDENTICAL relation values, so the paired advantage is internally
      controlled.  The u=2.5 referencing is per-N max-value based
      (definition-dependence).  Classifier is the exp545 split-word extension
      of the spot-check-asserted exp540-fixed one (re-asserted per seed
      here); the brief's factor-range scaling was corrected to the
      ladder-consistent windows (documented above) BEFORE data generation,
      and the uint64->int64 draw wrap was fixed pre-data (documented above).
"""

import json
import math
import os
import random
import time
import traceback
from math import gcd

import numpy as np
from gmpy2 import mpz, is_prime, isqrt, powmod
from scipy.stats import spearmanr

WORK = "/tmp/exp553_tu116"
RESULT = f"{WORK}/result.json"

SMOKE = os.environ.get("SMOKE", "") == "1"

# ---------------- fixed configuration ----------------
SEEDS = [20261210, 20261211, 20261212]
N_PER_SEED = 50 if SMOKE else 400     # 3 x 400 = 1200 total
LO_P, HI_P = 2**52, 2**58
LO_Q, HI_Q = 2**58, 2**64
BITS_N = 116                     # exact bitlen requirement
N_REL = 240                      # relation values per N
H_OFF = 256                      # offsets d in [1, H_OFF], distinct
UEXP = 2.5                       # smoothness operating point u = ln(Vmax)/ln(B)
DIAL_MAX = 400                   # dial primes p <= 400
CNT_MAX = 100                    # baseline count primes p <= 100
N_BOOT = 30 if SMOKE else 300
BOOT_SEED = 20260822
CHUNKS_PER_SEED = 1 if SMOKE else 3
SPOT_PER_SEED = None if SMOKE else 300   # None => check EVERY value (smoke)
PRIOR_96 = 0.5739                    # fixed-classifier U96 pooled rho(T)
PRIOR_100 = 0.5436                   # U100 pooled rho(T)
PRIOR_104 = 0.5005                   # U104 pooled rho(T)
PRIOR_108 = 0.48802300433331264      # U108 pooled rho(T) (exp544 result.json)
PRIOR_112 = 0.462125678851606        # U112 pooled rho(T) (exp545 result.json)
PRIOR_112_CI = [0.41471196136838256, 0.5081483832982573]
BAND_LO, BAND_HI = 0.55, 0.85    # H1 validated band
ADV_MIN = 0.05                   # H2 advantage threshold

# split-word exact classifier parameters (V = VH * 2**K + VL, VL < 2**K)
KBITS = 34
MASKK = np.uint64((1 << KBITS) - 1)

T_START = time.time()

# fork-inherited globals (built in parent BEFORE Pool creation)
PRIMES_SMALL = None    # list[int], primes <= DIAL_MAX (includes 2)
PRIMES_BIG = None      # np.uint32 array, primes in (DIAL_MAX, Bmax]


def write_result(status, payload):
    doc = {"exp": "553", "codename": "TDIAL-U116", "round": None,
           "smoke": SMOKE,
           "status": status, "wall_s": round(time.time() - T_START, 1)}
    doc.update(payload)
    with open(RESULT, "w") as f:
        json.dump(doc, f, indent=1, default=float)


def sieve_primes(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            s[i * i :: i] = False
    return np.flatnonzero(s)


def draw_uniform_primes(rng, lo, hi, k, small_filter):
    """Uniform primes in [lo, hi): rejection sampling on uniform integers.
    U116 FIX (pre-data): candidates stay uint64 and are converted via
    .tolist(); exp545's .astype(np.int64) would wrap draws >= 2^63 negative
    (hi_Q = 2^64 here) and gmpy2.is_prime(negative) is False -> silent
    rejection of half the q window. Random stream identical to template."""
    out = []
    while len(out) < k:
        m = max(8192, 64 * (k - len(out)))
        v = rng.integers(lo, hi, size=m, dtype=np.uint64)
        mask = np.ones(len(v), dtype=bool)
        for sp in small_filter:            # cheap prefilter (~88% composites)
            mask &= (v % sp) != 0
        for x in v[mask].tolist():         # exact unsigned python ints
            if is_prime(x):
                out.append(x)
                if len(out) == k:
                    break
    return out


def gen_population(seed):
    """Rejection sampling: p,q uniform primes in their ranges (each prime
    equally likely); N kept iff bitlen(N) == BITS_N exactly.
    NOTE measured acceptance ~3-3.5% at bits 100..116 (uniform-over-primes
    tilts both factors to the top octaves, so exact-bitlen products are
    rare) -- hence the adaptive draw loop."""
    rng = np.random.default_rng(seed)
    small = sieve_primes(100)[1:]          # odd small primes for prefilter
    Ns = []
    attempts = 0
    while len(Ns) < N_PER_SEED:
        k = max(512, int((N_PER_SEED - len(Ns)) * 80))
        ps = draw_uniform_primes(rng, LO_P, HI_P, k, small)
        qs = draw_uniform_primes(rng, LO_Q, HI_Q, k, small)
        for p, q in zip(ps, qs):
            attempts += 1
            N = p * q
            if N.bit_length() == BITS_N:
                Ns.append(mpz(N))
                if len(Ns) == N_PER_SEED:
                    break
    assert len(Ns) == N_PER_SEED
    assert all(int(N).bit_length() == BITS_N for N in Ns)
    print(f"    seed {seed}: {attempts} pair-attempts -> {len(Ns)} accepts "
          f"({100.0*len(Ns)/attempts:.1f}%)", flush=True)
    return Ns


ODD_PRIMES_400 = None   # set in main


def features(N_list):
    """T(N) = sum 2/p over odd QR primes <= 400 ; cnt = # QR primes <= 100."""
    T = np.zeros(len(N_list))
    C = np.zeros(len(N_list))
    exps400 = [(p - 1) // 2 for p in ODD_PRIMES_400]
    for i, N in enumerate(N_list):
        t = 0.0
        c = 0
        for p, e in zip(ODD_PRIMES_400, exps400):
            if powmod(N, e, p) == 1:
                t += 2.0 / p
                if p <= CNT_MAX:
                    c += 1
        T[i] = t
        C[i] = c
    return T, C


# ---------- independent full factorization (Pollard rho / Brent) ----------
SMALL_1K = None   # set in main


def _pollard_brent(n):
    """Return a nontrivial factor of composite odd n (no small factors).
    NOTE: n reaches ~1.5e20 at bitlen 116 (> int64 max), so the draws use
    stdlib random.Random.randrange (deterministic, arbitrary precision) --
    numpy Generator.integers is int64-bounded and threw in the exp544-
    inherited version."""
    rnd = random.Random(541001)
    while True:
        y = rnd.randrange(1, n)
        c = rnd.randrange(1, n)
        m = 128
        g = r = q = 1
        x = ys = y
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = gcd(q, n)
                k += m
            r *= 2
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = gcd(abs(x - ys), n)
        if g != n:
            return g


def full_factor(n):
    """Full prime factorization of n >= 1; returns sorted list of primes."""
    fs = []
    for p in SMALL_1K:
        while n % p == 0:
            fs.append(int(p))
            n //= p
        if p * p > n and n > 1:
            break
    stack = [n] if n > 1 else []
    while stack:
        v = stack.pop()
        if v == 1:
            continue
        if v < p * p or is_prime(v):
            fs.append(int(v))
            continue
        d = _pollard_brent(v)
        stack.append(d)
        stack.append(v // d)
    return sorted(fs)


# ---------- exact 34/34 split-word smoothness classifier ----------
def build_relation_values(N_list_ints, tag):
    """PARENT-side, deterministic: per-N offsets from ONE stream per seed
    (rng(tag*7+1), consumed row by row -- exp544 convention), then the 240
    values V=(r+d)^2-N, their per-N bound B_N = ceil(Vmax^(1/u)).
    Returns (vals_per_row list[list[int]], bnds list[int])."""
    rng = np.random.default_rng(tag * 7 + 1)
    vals, bnds = [], []
    for Nmpz in N_list_ints:
        N = int(Nmpz)
        r = int(isqrt(N))
        d = np.sort(rng.choice(H_OFF, N_REL, replace=False)).astype(np.int64) + 1
        row = []
        for dd in d.tolist():
            x = r + dd
            row.append(x * x - N)          # python ints; V reaches ~2^67.0
        vmax = max(row)
        B = int(math.ceil(math.exp(math.log(vmax) / UEXP)))
        vals.append(row)
        bnds.append(B)
    return vals, bnds


def classify_chunk(VHi, VLo, BVb, tag):
    """Exact B-smoothness of flattened relation values (row-major), values
    given as exact 34/34 split words (V = VH*2^34 + VL), per-value own bound
    BV. Semantics identical to exp545's exp540-fixed classifier: each row is
    pulled only by primes <= ITS OWN bound, decided smooth when its residual
    drops to <= its own bound, expired when the loop passes its bound, and
    additionally killed (NOT smooth) as soon as residual < p^2 while residual
    > bound (sound: all prime factors <= bound are stripped, so a residual in
    (bound, p^2) has a prime factor > bound). Returns smooth-flag bool array."""
    VH = np.asarray(VHi, dtype=np.uint64).copy()
    VL = np.asarray(VLo, dtype=np.uint64).copy()
    BVl = np.asarray(BVb, dtype=np.uint64).copy()
    BH = (BVl >> np.uint64(KBITS)).astype(np.uint64)
    BL = (BVl & MASKK).astype(np.uint64)
    n = len(VH)
    Olive = np.arange(n, dtype=np.int64)
    smooth = np.zeros(n, dtype=bool)
    ndead = 0
    KB = np.uint64(KBITS)
    SHIFTS = {}          # per-prime 2^34 mod p cache

    def le_bound(idx):
        return ((VH[idx] < BH[idx])
                | ((VH[idx] == BH[idx]) & (VL[idx] <= BL[idx])))

    def park(rows):
        nonlocal ndead
        if rows.size:
            VH[rows] = np.uint64(0)
            VL[rows] = np.uint64(0)
            BVl[rows] = np.uint64(0)
            Olive[rows] = -1
            ndead += rows.size

    def pull(p):
        """divide out ALL factors of p from ELIGIBLE live values (own bound
        still allows p); return touched index array (current-array coords)."""
        pm = np.uint64(p)
        sh = SHIFTS.get(p)
        if sh is None:
            sh = SHIFTS[p] = np.uint64((1 << KBITS) % p)
        rem = (((VH % pm) * sh + (VL % pm)) % pm)
        hl = np.flatnonzero((BVl >= pm) & (rem == 0))
        if hl.size == 0:
            return hl
        touched = hl.copy()
        while hl.size:
            rh = VH[hl] % pm
            num = rh * np.uint64(1 << KBITS) + VL[hl]     # < 2^61: exact
            qd = num // pm
            VH[hl] = (VH[hl] // pm) + (qd >> KB)          # renormalized split
            VL[hl] = qd & MASKK
            rh = VH[hl] % pm
            rem = (rh * sh + (VL[hl] % pm)) % pm
            hl = hl[(BVl[hl] >= pm) & (rem == 0)]
            if hl.size:
                touched = np.union1d(touched, hl)
        return touched

    def decide(locals_):
        if locals_.size:
            dec = locals_[le_bound(locals_)]
            if dec.size:
                smooth[Olive[dec]] = True
                park(dec)

    def early_kill(pcur):
        """rows whose OWN bound pcur has passed are parked immediately (same
        predicate as exp544's compaction-time expire -- all their remaining
        prime factors exceed their bound -> definitively NOT smooth);
        PLUS residual in (own bound, pcur^2) => has a prime factor > bound.
        Applied on the periodic sweep as a pure runtime cut."""
        live = np.flatnonzero(Olive >= 0)
        if live.size == 0:
            return
        pm = np.uint64(pcur)
        park(live[BVl[live] < pm])
        live = np.flatnonzero(Olive >= 0)                  # fresh after park
        if live.size == 0:
            return
        gt = ((VH[live] > BH[live])
              | ((VH[live] == BH[live]) & (VL[live] > BL[live])))
        cand = live[gt]
        if cand.size == 0:
            return
        psq = pcur * pcur                                  # < 2^55: fits
        ph = np.uint64(psq >> KBITS)
        pl = np.uint64(psq & (1 << KBITS) - 1)
        lt = ((VH[cand] < ph)
              | ((VH[cand] == ph) & (VL[cand] < pl)))
        park(cand[lt])

    def compact():
        nonlocal VH, VL, BVl, BH, BL, Olive, ndead
        keep = Olive >= 0
        VH, VL, BVl = VH[keep], VL[keep], BVl[keep]
        BH, BL = BH[keep], BL[keep]
        Olive = Olive[keep]
        ndead = 0

    t0 = time.time()
    # Stage A: primes <= DIAL_MAX (includes 2) -- factoring only
    for p in PRIMES_SMALL:
        decide(pull(p))
    # required pass (not a no-op): values fully reduced to <= their bound
    decide(np.flatnonzero(Olive >= 0))
    compact()

    nbig = len(PRIMES_BIG)
    SWEEP = 32
    for j in range(nbig):
        p = int(PRIMES_BIG[j])
        decide(pull(p))
        if j % SWEEP == 0:
            early_kill(p)
        if ndead > 0.3 * len(VH):
            compact()
            gone = np.flatnonzero((Olive >= 0)
                                  & (BVl < np.uint64(p)))
            park(gone)
        if j % 200000 == 0:
            print(f"    [{tag}] big-prime {j}/{nbig} (p={p}) "
                  f"live={len(VH)} elapsed={time.time()-t0:.0f}s",
                  flush=True)
    # leftover live values have a prime factor > B -> not smooth
    return smooth


def _chunk_worker(args):
    tag, VHi, VLo, BVb = args
    return tag, classify_chunk(VHi, VLo, BVb, tag)


def boot_ci(a, b, nboot=N_BOOT, seed=BOOT_SEED):
    rng = np.random.default_rng(seed)
    n = len(a)
    out = np.empty(nboot)
    for k in range(nboot):
        ii = rng.integers(0, n, n)
        out[k] = float(spearmanr(a[ii], b[ii])[0])
    return [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))], out


def main():
    global ODD_PRIMES_400, SMALL_1K, PRIMES_SMALL, PRIMES_BIG

    # ---- stage 00: hypotheses/config BEFORE any data ----
    write_result("00_hypotheses_stated", {
        "hypotheses": {
            "H1": "Spearman(T, rate) stays within [0.55, 0.85] on uniform "
                  "draws at bitlen 116, u=2.5",
            "H2": "T beats count <=100 by > +0.05",
        },
        "prior": f"pooled Spearman {PRIOR_96} (fixed classifier) at bitlen 96; "
                 f"{PRIOR_100} CI [0.4982,0.5881] at bitlen 100; "
                 f"{PRIOR_104} CI [0.4557,0.5454] at bitlen 104 "
                 "(TDIAL-U104-CONTINUES-FADE); "
                 f"{PRIOR_108:.4f} CI [0.4453,0.5337] at bitlen 108 "
                 "(TDIAL-U108-CONTINUES-FADE); "
                 f"{PRIOR_112:.5f} CI [{PRIOR_112_CI[0]:.5f},"
                 f"{PRIOR_112_CI[1]:.5f}] at bitlen 112 "
                 "(TDIAL-U112-CONTINUES-FADE, step delta -0.0259)",
        "brief_correction": "brief said to scale exp545's prime ranges x16 "
                            "('keeping the same structure'); literal x16 "
                            "[2^54,2^60)x[2^60,2^66) meets at 2^60 != "
                            "2^(B/2)=2^58 and puts the accepted log-sum band "
                            "[115,116) at the bottom tail of the window "
                            "(mean sum 120), unlike every prior rung whose "
                            "window mean equals B; corrected pre-data to the "
                            "TDIAL-ladder continuation [2^52,2^58)x"
                            "[2^58,2^64) (width-6 octave windows meeting at "
                            "2^(B/2), bounds x4 per +4-bit rung as in "
                            "exp539..exp545; the brief's x16 matches the "
                            "two-rung span). Same brief-typo family as "
                            "exp541/exp544/exp545",
        "classifier_extension": "relation values reach 2rd+d^2 ~ 2^67.0 > "
                            "uint64max at bitlen 116; exp545's 34/34 split "
                            "words retained (capacity 2^68 > Vmax), "
                            "remainder/division exact integer identities, "
                            "predicate semantically identical to exp545's; "
                            "Pollard-rho spot-check asserted per seed",
        "u116_draw_fix": "q window upper bound is exactly 2^64 at this rung; "
                            "template's astype(np.int64) wraps draws >= 2^63 "
                            "negative and gmpy2.is_prime(negative)=False "
                            "-> silent rejection of half the q window; "
                            "fixed pre-data by keeping uint64 + .tolist() "
                            "(random stream unchanged)",
        "config": {"seeds": SEEDS, "n_per_seed": N_PER_SEED,
                    "p_range": [LO_P, HI_P], "q_range": [LO_Q, HI_Q],
                    "bits_n": BITS_N, "n_rel": N_REL, "h_off": H_OFF,
                    "u_exp": UEXP, "dial_max": DIAL_MAX, "cnt_max": CNT_MAX,
                    "n_boot": N_BOOT},
    })
    print(f"[{time.time()-T_START:.0f}s] stage 00 done", flush=True)

    all_primes = sieve_primes(DIAL_MAX)
    ODD_PRIMES_400 = [int(p) for p in all_primes if p > 2]
    SMALL_1K = [int(p) for p in sieve_primes(1000)]

    # ---- stage 01: population ----
    pop = {}
    for s in SEEDS:
        pop[s] = gen_population(s)
        print(f"[{time.time()-T_START:.0f}s] seed {s}: {len(pop[s])} semiprimes",
              flush=True)
    N_all = [N for s in SEEDS for N in pop[s]]
    seed_id = np.array([i // N_PER_SEED for i in range(len(N_all))])
    bl = [int(N).bit_length() for N in N_all]
    assert min(bl) == max(bl) == BITS_N and len(set(map(int, N_all))) == len(N_all)
    with open(f"{WORK}/population.txt", "w") as f:
        for s, N in zip(seed_id, N_all):
            f.write(f"{SEEDS[s]} {N}\n")
    write_result("01_population_done", {
        "population": {"total": len(N_all), "bitlen_min": min(bl),
                        "bitlen_max": max(bl)}})
    print(f"[{time.time()-T_START:.0f}s] stage 01 done", flush=True)

    # ---- stage 02: dial features ----
    T_all, C_all = features(N_all)
    np.savez(f"{WORK}/features.npz", T=T_all, C=C_all, seed=seed_id)
    print(f"[{time.time()-T_START:.0f}s] stage 02 done: "
          f"T mean={T_all.mean():.4f} range=[{T_all.min():.3f},{T_all.max():.3f}]; "
          f"cnt mean={C_all.mean():.2f}", flush=True)
    write_result("02_features_done", {
        "features": {"T_mean": float(T_all.mean()), "cnt_mean": float(C_all.mean())}})

    # ---- stage 03: relation values, exact smoothness rates ----
    # parent builds values/bounds deterministically (one stream per seed)
    vals_by_seed, bnds_by_seed = {}, {}
    for si, s in enumerate(SEEDS):
        sl = slice(si * N_PER_SEED, (si + 1) * N_PER_SEED)
        v, b = build_relation_values(N_all[sl], si)
        vals_by_seed[s] = v
        bnds_by_seed[s] = b
        print(f"[{time.time()-T_START:.0f}s] seed {s}: values+bounds built "
              f"(B~[{min(b)},{max(b)}])", flush=True)
    Bmax = max(max(b) for b in bnds_by_seed.values())
    prim = sieve_primes(Bmax)
    PRIMES_SMALL = [int(p) for p in prim if p <= DIAL_MAX]   # includes 2
    PRIMES_BIG = (prim[prim > DIAL_MAX]).astype(np.uint32)
    print(f"[{time.time()-T_START:.0f}s] prime base: Bmax={Bmax}, "
          f"{len(PRIMES_BIG)} big primes", flush=True)

    # chunk payloads: (tag, VH, VL, BV); tag = si*CHUNKS + ck
    payloads = []
    for si, s in enumerate(SEEDS):
        flat_V = [v for row in vals_by_seed[s] for v in row]
        flat_B = []
        for bb in bnds_by_seed[s]:
            flat_B.extend([bb] * N_REL)
        assert len(flat_V) == len(flat_B) == N_PER_SEED * N_REL
        VHf = np.array([int(v) >> KBITS for v in flat_V], dtype=np.uint64)
        VLf = np.array([int(v) & int(MASKK) for v in flat_V], dtype=np.uint64)
        BVf = np.array(flat_B, dtype=np.uint64)
        n = len(VHf)
        edges = [round(c * n / CHUNKS_PER_SEED) for c in range(CHUNKS_PER_SEED + 1)]
        for ck in range(CHUNKS_PER_SEED):
            a, z = edges[ck], edges[ck + 1]
            payloads.append((si * CHUNKS_PER_SEED + ck,
                             VHf[a:z].copy(), VLf[a:z].copy(), BVf[a:z].copy()))

    rates = {}
    from multiprocessing import get_context
    ctx = get_context("fork")
    smooth_by_tag = {}
    with ctx.Pool(processes=len(payloads)) as pool:
        for tag, sm in pool.map(_chunk_worker, payloads):
            smooth_by_tag[tag] = sm
            print(f"[{time.time()-T_START:.0f}s] chunk {tag} done "
                  f"({int(sm.sum())} smooth)", flush=True)

    for si, s in enumerate(SEEDS):
        nvals = N_PER_SEED * N_REL
        edges = [round(c * nvals / CHUNKS_PER_SEED)
                 for c in range(CHUNKS_PER_SEED + 1)]
        sm = np.concatenate([smooth_by_tag[si * CHUNKS_PER_SEED + ck]
                             for ck in range(CHUNKS_PER_SEED)])
        assert len(sm) == nvals
        np.save(f"{WORK}/smooth_seed{si}.npy", sm)
        G = np.repeat(np.arange(N_PER_SEED), N_REL)
        r = np.bincount(G[sm], minlength=N_PER_SEED) / float(N_REL)
        rates[s] = r
        np.save(f"{WORK}/rate_seed{si}.npy", r)

        # ---- independent spot-check: Pollard-rho full factorization ----
        flat_V = [v for row in vals_by_seed[s] for v in row]
        flat_B = []
        for bb in bnds_by_seed[s]:
            flat_B.extend([bb] * N_REL)
        if SPOT_PER_SEED is None:
            idx = np.arange(nvals)
        else:
            rs = np.random.default_rng(900000 + si)
            idx = np.sort(rs.choice(nvals, SPOT_PER_SEED, replace=False))
        mism = 0
        for i in idx.tolist():
            mx = max(full_factor(int(flat_V[i])))
            if (mx <= int(flat_B[i])) != bool(sm[i]):
                mism += 1
        nchk = len(idx)
        print(f"    [{s}] spot-check {nchk} values vs Pollard-rho full "
              f"factorization: mismatches={mism}", flush=True)
        assert mism == 0, "smoothness classification disagrees with exact factoring"

        del vals_by_seed[s]

    R_all = np.concatenate([rates[s] for s in SEEDS])
    allb = [bb for s in SEEDS for bb in bnds_by_seed[s]]
    write_result("03_rates_done", {
        "rates_done_seeds": SEEDS,
        "spot_check": "pollard-rho mismatch=0 per seed (asserted in-script)",
        "rates_summary": {str(ss): {"mean": float(rates[ss].mean()),
                                     "std": float(rates[ss].std())}
                           for ss in rates},
        "bounds_range": [min(allb), max(allb)]})
    print(f"[{time.time()-T_START:.0f}s] stage 03 done", flush=True)

    # ---- stage 04: statistics ----
    res = {"per_seed": []}
    for si, s in enumerate(SEEDS):
        sl = slice(si * N_PER_SEED, (si + 1) * N_PER_SEED)
        rT = float(spearmanr(T_all[sl], R_all[sl])[0])
        rC = float(spearmanr(C_all[sl], R_all[sl])[0])
        res["per_seed"].append({"seed": s, "n": N_PER_SEED,
                                 "rho_T": rT, "rho_cnt": rC,
                                 "advantage": rT - rC})
    pT = float(spearmanr(T_all, R_all)[0])
    pC = float(spearmanr(C_all, R_all)[0])
    ciT, _ = boot_ci(T_all, R_all)
    ciC, _ = boot_ci(C_all, R_all)
    rngb = np.random.default_rng(BOOT_SEED + 1)
    advs = np.empty(N_BOOT)
    for k in range(N_BOOT):
        ii = rngb.integers(0, len(R_all), len(R_all))
        advs[k] = (float(spearmanr(T_all[ii], R_all[ii])[0])
                   - float(spearmanr(C_all[ii], R_all[ii])[0]))
    ciA = [float(np.percentile(advs, 2.5)), float(np.percentile(advs, 97.5))]
    adv = pT - pC

    h1 = bool(BAND_LO <= pT <= BAND_HI)   # stays within [0.55, 0.85]
    h2 = bool(adv > ADV_MIN)              # beats count by > +0.05
    ci_pos = ("below", "straddles", "above")[
        0 if ciT[1] < BAND_LO else 1 if ciT[0] <= BAND_LO else 2]

    # pre-stated verdict logic (tasking brief, verbatim thresholds):
    #   H1 pass                          -> U116-DIAL-HOLDS
    #   H1 fail, |step delta| <= 0.013   -> U116-PLATEAU
    #     (half of prior step -0.0259)
    #   H1 fail, decline >= 0.0259       -> U116-CONTINUES-FADE
    #   else                             -> U116-MIXED
    step_delta = pT - PRIOR_112
    prior_step = PRIOR_112 - PRIOR_108            # -0.02590 (U108 -> U112)
    half_prior_step = abs(prior_step) / 2.0       # 0.01295 (~brief's 0.013)
    further_decline = bool(step_delta <= -abs(prior_step))
    plateau_zone = bool(abs(step_delta) <= half_prior_step)
    h1_per_seed = all(ps["rho_T"] >= BAND_LO and ps["rho_T"] <= BAND_HI
                      for ps in res["per_seed"])
    if h1:
        verdict = "U116-DIAL-HOLDS"
    elif plateau_zone:
        verdict = "U116-PLATEAU"
    elif further_decline:
        verdict = "U116-CONTINUES-FADE"
    else:
        verdict = "U116-MIXED"

    write_result("04_final", {
        "hypotheses": {
            "H1": "Spearman(T, rate) stays within [0.55, 0.85] on uniform "
                  "draws at bitlen 116, u=2.5",
            "H2": "T beats count <=100 by > +0.05"},
        "config": {"seeds": SEEDS, "n_per_seed": N_PER_SEED,
                    "p_range": [LO_P, HI_P], "q_range": [LO_Q, HI_Q],
                    "bits_n": BITS_N, "n_rel": N_REL, "h_off": H_OFF,
                    "u_exp": UEXP, "dial_max": DIAL_MAX, "cnt_max": CNT_MAX,
                    "n_boot": N_BOOT},
        "population": {"total": len(N_all)},
        "per_seed": res["per_seed"],
        "pooled": {"n": len(R_all), "rho_T": pT, "rho_T_ci95": ciT,
                    "rho_cnt": pC, "rho_cnt_ci95": ciC,
                    "advantage": adv, "advantage_ci95": ciA},
        "rate_summary": {"mean": float(R_all.mean()), "std": float(R_all.std()),
                          "smooth_values": int((R_all * N_REL).sum()),
                          "total_values": len(R_all)},
        "comparisons": {
            "ladder": [
                {"rung": "U96", "exp": 539, "rho_T": PRIOR_96,
                 "ci95": None, "verdict": None,
                 "note": "fixed classifier"},
                {"rung": "U100", "exp": 540, "rho_T": PRIOR_100,
                 "ci95": [0.4982, 0.5881], "verdict": None},
                {"rung": "U104", "exp": 541, "rho_T": PRIOR_104,
                 "ci95": [0.4557, 0.5454],
                 "verdict": "TDIAL-U104-CONTINUES-FADE"},
                {"rung": "U108", "exp": 544, "rho_T": PRIOR_108,
                 "ci95": [0.4453, 0.5337],
                 "verdict": "TDIAL-U108-CONTINUES-FADE"},
                {"rung": "U112", "exp": 545, "rho_T": PRIOR_112,
                 "ci95": PRIOR_112_CI,
                 "verdict": "TDIAL-U112-CONTINUES-FADE"},
                {"rung": "U116", "exp": 553, "rho_T": pT, "ci95": ciT,
                 "verdict": verdict},
            ],
            "prior_rho_96_fixed": PRIOR_96,
            "prior_rho_100": PRIOR_100,
            "prior_rho_104": PRIOR_104,
            "prior_rho_108": PRIOR_108,
            "prior_rho_112": PRIOR_112,
            "step_delta_vs_112": step_delta,
            "prior_step_108_to_112": prior_step,
            "half_prior_step_threshold": half_prior_step,
            "plateau_zone_abs_delta_le_half": plateau_zone,
            "further_decline_vs_112": further_decline,
            "delta_vs_108": pT - PRIOR_108,
            "ci95_vs_band_lower_edge": ci_pos},
        "verdicts": {"H1_pass": h1, "H1_pass_per_seed": h1_per_seed,
                     "H2_pass": h2,
                     "verdict_name": verdict},
    })
    print(f"[{time.time()-T_START:.0f}s] FINAL: pooled rho_T={pT:.4f} "
          f"CI[{ciT[0]:.4f},{ciT[1]:.4f}] rho_cnt={pC:.4f} "
          f"adv={adv:+.4f} CI[{ciA[0]:.4f},{ciA[1]:.4f}] "
          f"H1={h1} H2={h2} VERDICT={verdict}", flush=True)
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

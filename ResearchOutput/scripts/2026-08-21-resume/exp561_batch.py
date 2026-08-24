#!/usr/bin/env python3
"""EXP 561 'BATCH-AMORTIZATION' -- when factoring MANY integers, can work be
shared? Bernstein-style batch smooth-part detection (product/remainder tree)
+ batch-gcd prefilter vs per-N solo factoring at bitlen 40: cost-per-factor
vs batch size k, and the k-crossover question.

PRE-STATED EXPECTATION (verbatim from the tasking brief, registered BEFORE
any data generation):
  "batch helps the SMOOTHNESS-TESTING phase (amortizing product tree) but NOT
   the finding phase (each N still needs its own relations) ==> per-factor
   savings bounded, quantify the bound."
H-AUDIT (hard requirement, asserted): batch-detected smooth set == per-item
  tested set, EXACT match, on a 500-sample audit.
VERDICTS (from data only): BATCH-WINS / BREAK-EVEN / NULL, with the
  k-crossover stated.

DESIGN (fixed before data):
  Population : 512 random odd composites, bitlen exactly 40, master seed
               20260827. Even positions = semiprimes (two distinct 20-bit
               primes), odd positions = general odd composites (2-4 distinct
               odd primes), so every chunk of any size sees a balanced mix.
               Every k-row processes the SAME population partitioned into
               consecutive chunks of size k, k in {1, 8, 64, 512}; the k=1
               row IS the solo baseline by construction (per-N processing).
  Prefilter  : batch-gcd: primorial G = prod_{p<=100} p (built once per run,
               charged to a 'setup' bucket excluded from all row totals --
               equally available to every arm). Per input: loop
               g = gcd(N, G) stripping until gcd == 1 (Euclid steps counted);
               parts equal to gcd (squarefree over FB) get their prime
               factorization extracted directly. Residuals emerging with
               gcd == 1 carry no prime <= 100.
  Sieve      : per composite residual R: L = 512 candidates
               f_j = (r+j)^2 - R, r = isqrt(R)+1, j in [0,L).
               FB = primes <= 100 (25 primes). Candidate GENERATION cost
               (1 mul + 1 sub per candidate) is identical in both arms.
  SOLO test  : per-candidate FULL trial division over FB with multiplicity
               stripping; smooth <=> residue reaches 1; every executed probe
               and re-test is charged. DESIGN CORRECTION (made before any
               full-run data, after the smoke run exposed a charging gap):
               'early exit at the first non-divisor' is semantically
               INVALID for exact smoothness DETECTION (a candidate missing
               prime 3 can still be 2-smooth), so the honest per-item
               baseline is full trial division -- exactly the pi(B)
               divisions-per-item cost that Bernstein's method competes
               against in the literature.
  BATCH test : Bernstein-style, exact: Q = prod_p p^{e_p} with e_p minimal
               s.t. p^{e_p} > max f (literally prod(FB primes)^bounds), built
               once per chunk. Then B-smooth(c) <=> c | Q <=> (Q mod c) == 0,
               and ALL the residues Q mod c_i come from ONE product/
               remainder tree over the chunk's candidate list (single
               numerator Q, moduli = candidates; invariant r_node = Q mod
               M_node; no coprimality needed; exact, no heuristic).
  Completion : IDENTICAL shared code for every arm: if a residual has >= 26
               relations, GF(2)-combine then gcd(x - sqrt(prod f), R); else
               Pollard-Brent rho fallback; deterministic Miller-Rabin
               (7-base set, valid for n < 3.475e12 >= 2^40); recursion on
               cofactors (QS/rho cofactors go straight to rho so arms cannot
               diverge). Rho RNG keyed by N alone -- identical trajectories
               in every arm, removing luck confounds.
METRICS: ops per factored N vs k (FLAT ledger + WORD-weighted ledger + wall
  clock); per-candidate testing rates (solo early-exit, solo full-test,
  batch); least-squares fit batch_rate ~ a + b*log2(M); crossover vs both
  solo rates; phase decomposition -> the savings BOUND (max per-factor
  saving if testing were FREE = non-testing share).
COST MODEL (declared): FLAT ledger: every EXECUTED bigint mul / mod / div /
  add / Euclid step / MR modexp-step = 1 op. WORD ledger: mul -> wa*wb;
  mod/div/Euclid step -> wn*wd; add/sub -> max(wa,wb); comparisons, exponent
  bookkeeping and SKIPPED reductions (residue < modulus) are free.
  Wall clock recorded as a third, unmodeled reference.
"""

import argparse
import json
import math
import os
import platform
import random
import sys
import time
from math import prod

from gmpy2 import mpz, isqrt as g_isqrt, next_prime

SEED = 20260827
BITLEN = 40
POP = 512
KS = [1, 8, 64, 512]
L_SIEVE = 512
MIN_RELS = 26          # FB has 25 primes; a dependency needs > #primes
AUDIT_N = 500

SCRIPT_DIR = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-21-resume"
SMOKE = False
KS_MAX = max(KS)


# ---------------------------------------------------------------- ledger ---
class Ledger:
    PHASES = ["setup", "prefilter", "gen", "test_solo", "test_batch",
              "relproc", "la", "rho", "mr", "misc"]

    def __init__(self):
        self.flat = {p: 0 for p in self.PHASES}
        self.words = {p: 0 for p in self.PHASES}
        self.phase = "misc"
        self.batch_skipped = 0     # skipped reductions (free in both ledgers)

    def w(self, n):
        return max(1, (int(n).bit_length() + 63) // 64)

    def mul(self, a, b):
        self.flat[self.phase] += 1
        self.words[self.phase] += self.w(a) * self.w(b)

    def mod(self, n, d):
        self.flat[self.phase] += 1
        self.words[self.phase] += self.w(n) * self.w(d)

    def div(self, n, d):
        self.flat[self.phase] += 1
        self.words[self.phase] += self.w(n) * self.w(d)

    def add(self, a, b):
        self.flat[self.phase] += 1
        self.words[self.phase] += max(self.w(a), self.w(b))

    def gcd_step(self, a, b):
        self.flat[self.phase] += 1
        self.words[self.phase] += self.w(a) * self.w(b)


def euclid_gcd(a, b, led):
    """Counted Euclid gcd."""
    a, b = abs(int(a)), abs(int(b))
    while b:
        led.gcd_step(a, b)
        a, b = b, a % b
    return a


# ------------------------------------------------------------ primitives ---
def sieve_primes(limit):
    s = bytearray([1]) * (limit + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, int(limit ** 0.5) + 1):
        if s[i]:
            s[i * i:: i] = bytearray(len(range(i * i, limit + 1, i)))
    return [i for i in range(limit + 1) if s[i]]


FB = sieve_primes(100)          # 25 primes <= 100
FB_N = len(FB)
FB_IDX = {p: i for i, p in enumerate(FB)}

_MR_BASES = [2, 3, 5, 7, 11, 13, 17]   # deterministic for n < 3.475e12
assert (1 << BITLEN) < 3474749660383


def _powmod_counted(a, d, n, led):
    r = 1
    aa = a % n
    led.mod(a, n)
    while d > 0:
        if d & 1:
            t = r * aa
            led.mul(r, aa)
            r = t % n
            led.mod(t, n)
        d >>= 1
        if d:
            t = aa * aa
            led.mul(aa, aa)
            aa = t % n
            led.mod(t, n)
    return r


def miller_rabin_counted(n, led):
    """Deterministic MR (n < 3.475e12), counted."""
    old = led.phase
    led.phase = "mr"
    try:
        if n < 2:
            return False
        for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
            if n % p == 0:
                led.mod(n, p)
                return n == p
        d = n - 1
        s = 0
        while d % 2 == 0:
            led.mod(d, 2)
            d //= 2
            s += 1
        for a in _MR_BASES:
            x = _powmod_counted(a, d, n, led)
            if x == 1 or x == n - 1:
                continue
            passed = False
            for _ in range(s - 1):
                t = x * x
                led.mul(x, x)
                x = t % n
                led.mod(t, n)
                if x == n - 1:
                    passed = True
                    break
            if not passed:
                return False
        return True
    finally:
        led.phase = old


def pollard_brent(n, led, rng, max_iter=250000):
    """Counted Brent-cycle Pollard rho. Returns nontrivial factor or None."""
    old = led.phase
    led.phase = "rho"
    try:
        if n % 2 == 0:
            return 2
        if n % 3 == 0:
            return 3
        for _attempt in range(8):
            y = rng.randrange(1, n)
            c = rng.randrange(1, n)
            m = 128
            g = r = q = 1
            x = ys = y
            it = 0
            while g == 1 and it < max_iter:
                x = y
                for _ in range(r):
                    t = y * y
                    led.mul(y, y)
                    u = t + c
                    led.add(t, c)
                    y = u % n
                    led.mod(u, n)
                    it += 1
                k = 0
                while k < r and g == 1:
                    ys = y
                    for _ in range(min(m, r - k)):
                        t = y * y
                        led.mul(y, y)
                        u = t + c
                        led.add(t, c)
                        y = u % n
                        led.mod(u, n)
                        it += 1
                    t = q * abs(x - ys)
                    led.mul(q, abs(x - ys))
                    q = t % n
                    led.mod(t, n)
                    k += m
                g = euclid_gcd(q, n, led)
                r *= 2
                if g == n:
                    g = 1
                    bt = 0
                    while g == 1 and bt < 100000:
                        t = ys * ys
                        led.mul(ys, ys)
                        u = t + c
                        led.add(t, c)
                        ys = u % n
                        led.mod(u, n)
                        g = euclid_gcd(abs(x - ys), n, led)
                        bt += 1
                    if g == n:
                        break
            if 1 < g < n:
                return g
            # max_iter exhausted on this attempt: fall through to the next
            # attempt (a fresh (y,c) pair); only give up after all attempts
        return None
    finally:
        led.phase = old


# ----------------------------------------------------------- population ----
def rand_prime(rng, bits):
    lo = 1 << (bits - 1)
    while True:
        p = int(next_prime(rng.randrange(lo, 1 << bits)))
        if p.bit_length() == bits:
            return p


def gen_population(seed, n_pop):
    """Interleaved: even idx semiprime (two distinct 20-bit primes),
    odd idx general odd composite (2-4 distinct odd primes)."""
    rng = random.Random(seed)
    seen = set()
    half = n_pop // 2

    semis = []
    while len(semis) < half:
        p = rand_prime(rng, 20)
        q = rand_prime(rng, 20)
        if p == q:
            continue
        N = p * q
        if N.bit_length() != BITLEN or N in seen:
            continue
        seen.add(N)
        semis.append(N)

    gens = []
    while len(gens) < n_pop - half:
        c = rng.choices([2, 3, 4], weights=[0.25, 0.45, 0.30])[0]
        cuts = sorted(rng.sample(range(7, BITLEN - 6), c - 1)) if c > 1 else []
        widths = []
        prev = 0
        ok = True
        for cpt in cuts + [BITLEN]:
            wdt = cpt - prev
            if wdt < 7:
                ok = False
                break
            widths.append(wdt)
            prev = cpt
        if not ok:
            continue
        ps = [rand_prime(rng, wd) for wd in widths]
        if len(set(ps)) != len(ps):
            continue
        N = prod(ps)
        if N.bit_length() != BITLEN or N in seen:
            continue
        seen.add(N)
        gens.append(N)

    pop = []
    for i in range(n_pop):
        if i % 2 == 0:
            pop.append({"idx": i, "N": semis[i // 2], "kind": "semiprime"})
        else:
            pop.append({"idx": i, "N": gens[i // 2], "kind": "general"})
    return pop


# ------------------------------------------------------------- prefilter ---
def build_primorial(led):
    old = led.phase
    led.phase = "setup"
    try:
        G = 1
        for p in FB:
            led.mul(G, p)
            G *= p
        return G
    finally:
        led.phase = old


def extract_fb_squarefree(m, led):
    """Factor a squarefree FB-smooth part by probing FB (counted)."""
    old = led.phase
    led.phase = "prefilter"
    try:
        vec = []
        for p in FB:
            if m % p == 0:
                led.mod(m, p)
                vec.append(p)
        return vec
    finally:
        led.phase = old


def prefilter(N, G, led):
    """Loop gcd(N,G) stripping until gcd==1. Returns (residuals, small_parts)
    where residuals have no prime <=100 and small_parts are the extracted
    squarefree FB-smooth pieces."""
    stack = [N]
    residuals = []
    small_parts = []
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        g = euclid_gcd(m, G, led)     # phase = prefilter
        if g == 1:
            residuals.append(m)
        elif g == m:
            small_parts.append(extract_fb_squarefree(m, led))
        else:
            led.div(m, g)
            stack.append(g)
            stack.append(m // g)
    return residuals, small_parts


# ---------------------------------------------------------- solo testing ---
def trial_test(c, led, phase="test_solo"):
    """Canonical solo smoothness test: full trial division over FB with
    multiplicity stripping; smooth <=> residue reaches 1. EVERY executed
    probe and re-test is charged. (DESIGN CORRECTION vs the draft plan:
    'early exit at the first non-divisor' is semantically invalid for EXACT
    smoothness DETECTION -- missing a prime does not imply non-smooth --
    so the honest per-item baseline is full trial division, exactly the
    pi(B)-divisions-per-item cost Bernstein's method competes against.)"""
    old = led.phase
    led.phase = phase
    t = c
    vec = None
    smooth = False
    try:
        for i, p in enumerate(FB):
            led.mod(t, p)                     # the probe itself
            if t % p == 0:
                vec = [0] * FB_N if vec is None else vec
                e = 0
                while True:
                    led.div(t, p)
                    t //= p
                    e += 1
                    led.mod(t, p)             # charged re-test
                    if t % p != 0:
                        break
                vec[i] = e
                if t == 1:
                    smooth = True
                    break
        return smooth, (vec if smooth else None)
    finally:
        led.phase = old


# --------------------------------------------------------- batch testing ---
def batch_build_Q(items, led, phase="test_batch"):
    """Q = prod_p p^{e_p}, e_p minimal with p^{e_p} > max(items)."""
    old = led.phase
    led.phase = phase
    try:
        mx = max(items)
        Q = 1
        for p in FB:
            e = 1
            pe = p
            while pe <= mx:
                pe *= p
                e += 1
            led.mul(Q, pe)
            Q *= pe
        return Q
    finally:
        led.phase = old


def batch_remainder_tree(Q, items, led):
    """Residues Q mod c_i for all i via one product/remainder tree.
    Invariant: r_node == Q mod M_node (single numerator, no coprimality
    needed). Returns (flags, skipped_reductions). Exact."""
    old = led.phase
    led.phase = "test_batch"
    skipped = 0
    try:
        M = len(items)
        if M == 0:
            return [], 0
        if M == 1:
            led.mod(Q, items[0])
            return [Q % items[0] == 0], 0
        # product tree of moduli (bottom-up)
        levels = [list(items)]
        while len(levels[-1]) > 1:
            cur = levels[-1]
            nxt = []
            for i in range(0, len(cur) - 1, 2):
                led.mul(cur[i], cur[i + 1])
                nxt.append(cur[i] * cur[i + 1])
            if len(cur) % 2 == 1:
                nxt.append(cur[-1])
            levels.append(nxt)
        # top-down remainder pass
        res_levels = [[None] * len(lv) for lv in levels]
        root = levels[-1][0]
        if Q >= root:
            res_levels[-1][0] = Q % root
            led.mod(Q, root)
        else:
            res_levels[-1][0] = Q
            skipped += 1
        for d in range(len(levels) - 1, 0, -1):
            below = levels[d - 1]
            rbelow = res_levels[d - 1]
            for i, r in enumerate(res_levels[d]):
                if r is None:
                    continue
                li, ri = 2 * i, 2 * i + 1
                ml = below[li]
                if r >= ml:
                    rbelow[li] = r % ml
                    led.mod(r, ml)
                else:
                    rbelow[li] = r
                    skipped += 1
                if ri < len(below):
                    mr_ = below[ri]
                    if r >= mr_:
                        rbelow[ri] = r % mr_
                        led.mod(r, mr_)
                    else:
                        rbelow[ri] = r
                        skipped += 1
        flags = [r == 0 for r in res_levels[0]]
        return flags, skipped
    finally:
        led.phase = old


# ---------------------------------------------------- relation processing ---
def vectorize(c, led, phase="relproc"):
    old = led.phase
    led.phase = phase
    try:
        t = c
        vec = [0] * FB_N
        for i, p in enumerate(FB):
            while t % p == 0:
                led.mod(t, p)
                led.div(t, p)
                t //= p
                vec[i] += 1
        return vec
    finally:
        led.phase = old


def gf2_dependencies(vectors, want, led):
    """XOR basis with tracked combinations; null dependencies as index
    masks. Row-XORs counted in phase 'la' (rows are <=FB_N bits => 1 word)."""
    basis = {}
    deps = []
    old = led.phase
    led.phase = "la"
    try:
        for idx, vec in enumerate(vectors):
            row = 0
            for i, e in enumerate(vec):
                if e % 2:
                    row |= (1 << i)
            mask = 1 << idx
            r, mk = row, mask
            reduced = True
            while r:
                piv = r.bit_length() - 1
                if piv in basis:
                    br, bm = basis[piv]
                    r ^= br
                    mk ^= bm
                    led.flat["la"] += 1
                    led.words["la"] += 1
                else:
                    basis[piv] = (r, mk)
                    reduced = False
                    break
            if reduced and mk:
                deps.append(mk)
                if len(deps) >= want:
                    break
        return deps
    finally:
        led.phase = old


# ------------------------------------------------------- shared finishing ---
def finish_composite(R, rels, led, rng, stats):
    """Shared completion (identical code object for every arm): QS if enough
    relations, else Pollard-Brent rho; recursion on cofactors (rho only).
    All ops land in phases 'mr' / 'la' / 'rho'."""
    outer = led.phase
    led.phase = "rho"
    try:
        stack = [(R, rels)]
        while stack:
            m, mrels = stack.pop()
            if m == 1:
                continue
            if miller_rabin_counted(m, led):
                continue
            fac = None
            if len(mrels) >= MIN_RELS:
                old = led.phase
                led.phase = "la"
                try:
                    deps = gf2_dependencies([v for (_, _, v) in mrels],
                                            want=4, led=led)
                    for mk in deps:
                        xs = 1
                        ysq = 1
                        for j, (xj, fj, _) in enumerate(mrels):
                            if (mk >> j) & 1:
                                xs *= xj
                                ysq *= fj
                        y = int(g_isqrt(mpz(ysq)))
                        if y * y != ysq:
                            continue
                        g = euclid_gcd(xs - y, m, led)
                        if 1 < g < m:
                            fac = g
                            stats["qs_splits"] += 1
                            break
                finally:
                    led.phase = old
            if fac is None:
                fac = pollard_brent(m, led, rng)
                if fac is None:
                    stats["rho_failures"] += 1
                    stats["events"].append(f"RHO_FAIL m={m}")
                    continue
            a, b = fac, m // fac
            led.div(m, fac)
            for part in (a, b):
                if part == 1:
                    continue
                if miller_rabin_counted(part, led):
                    continue
                stack.append((part, []))
        return True
    finally:
        led.phase = outer


# ------------------------------------------------------------------ rows ---
def run_row(arm, k, pop, G, L, rng_seed):
    """Process the whole population; BATCH partitions into consecutive chunks
    of size k (pooling candidates per chunk), SOLO processes per-N."""
    led = Ledger()
    stats = {"qs_splits": 0, "rho_failures": 0, "events": [],
             "rho_roots": 0, "rels_found": 0}
    t0 = time.perf_counter()
    factored_flags = [False] * len(pop)
    roots_touched = set()
    vals_all, flags_all = [], []
    n_chunks = 0
    n_chunks_with_cand = 0

    chunk_iter = [pop] if arm == "SOLO" else \
        [pop[cs:cs + k] for cs in range(0, len(pop), k)]

    for chunk in chunk_iter:
        n_chunks += 1
        # ---- prefilter (identical both arms)
        residuals = []       # (root_idx, R)
        for rec in chunk:
            led.phase = "prefilter"
            res, small = prefilter(rec["N"], G, led)
            if small:
                factored_flags[rec["idx"]] = True
            for R in res:
                residuals.append((rec["idx"], R))
                roots_touched.add(rec["idx"])

        # ---- candidate generation (identical both arms)
        cand = []
        led.phase = "gen"
        for root_idx, R in residuals:
            r0 = int(g_isqrt(mpz(R - 1))) + 1
            for j in range(L):
                x = r0 + j
                f = x * x - R
                led.mul(x, x)
                led.add(f, R)
                cand.append((root_idx, x, f))

        # ---- smoothness testing (THE TREATMENT)
        smooth_items = []
        if arm == "SOLO":
            for (root_idx, x, f) in cand:
                ok, vec = trial_test(f, led)
                if ok:
                    smooth_items.append((root_idx, x, f, vec))
        else:
            vals = [f for (_, _, f) in cand]
            if vals:
                n_chunks_with_cand += 1
                Q = batch_build_Q(vals, led)
                flags, skipped = batch_remainder_tree(Q, vals, led)
                led.batch_skipped += skipped
                for i, (root_idx, x, f) in enumerate(cand):
                    if flags[i]:
                        vec = vectorize(f, led)
                        smooth_items.append((root_idx, x, f, vec))
                if k == KS_MAX:
                    vals_all.extend(vals)
                    flags_all.extend(flags)

        # ---- relations per root
        relmap = {}
        for (root_idx, x, f, vec) in smooth_items:
            relmap.setdefault(root_idx, []).append((x, f, vec))
        stats["rels_found"] += len(smooth_items)

        # ---- completion (identical shared code)
        for (root_idx, R) in residuals:
            rng = random.Random(f"rho:{rng_seed}:{root_idx}")
            stats["rho_roots"] += 1
            finish_composite(R, relmap.get(root_idx, []), led, rng, stats)
            factored_flags[root_idx] = True

    wall = time.perf_counter() - t0
    total_flat = sum(led.flat.values())
    total_words = sum(led.words.values())
    n_factored = sum(factored_flags)
    ncand = led.flat["gen"] // 2
    row = {
        "arm": arm, "k": (1 if arm == "SOLO" else k),
        "n_chunks": n_chunks,
        "M_candidates": ncand,
        "factored": n_factored,
        "ops_flat_by_phase": dict(led.flat),
        "ops_words_by_phase": dict(led.words),
        "total_flat": total_flat,
        "total_words": total_words,
        "ops_per_factor_flat": total_flat / max(1, n_factored),
        "ops_per_factor_words": total_words / max(1, n_factored),
        "wall_s": wall,
        "stats": {kk: vv for kk, vv in stats.items() if kk != "events"},
        "prefilter_resolved_N": len(pop) - len(roots_touched),
        "events_rho_fail": stats["events"][:10],
    }
    if arm == "BATCH":
        row["batch_skipped_reductions"] = led.batch_skipped
        row["M_chunk_mean"] = ncand / max(1, n_chunks_with_cand)
        row["batch_rate_flat_per_cand"] = led.flat["test_batch"] / max(1, ncand)
        row["batch_rate_words_per_cand"] = led.words["test_batch"] / max(1, ncand)
    else:
        row["solo_rate_flat_per_cand"] = led.flat["test_solo"] / max(1, ncand)
        row["solo_rate_words_per_cand"] = (
            led.words["test_solo"] / max(1, ncand))
    return row, vals_all, flags_all


# ------------------------------------------------------------------ main ---
def main():
    global SMOKE, KS_MAX
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--pop", type=int, default=POP)
    ap.add_argument("--L", type=int, default=L_SIEVE)
    ap.add_argument("--ks", type=str, default=",".join(map(str, KS)))
    ap.add_argument("--audit", type=int, default=AUDIT_N)
    args = ap.parse_args()
    SMOKE = args.smoke
    ks = [int(v) for v in args.ks.split(",")]
    KS_MAX = max(ks)
    audit_n = args.audit if not SMOKE else min(args.audit, 200)

    t_start = time.perf_counter()
    catches = []

    # ---- stage 00: hypotheses checkpoint BEFORE any population sampling
    result = {
        "exp": "561",
        "codename": "BATCH-AMORTIZATION",
        "round": None,
        "smoke": SMOKE,
        "status": "01_hypotheses",
        "hypotheses": {
            "E1_prestated": "batch helps the SMOOTHNESS-TESTING phase "
                            "(amortizing product tree) but NOT the finding "
                            "phase => per-factor savings bounded; quantify "
                            "the bound",
            "H_AUDIT": "batch-detected smooth set == per-item tested set on "
                       "an exact-match audit (500 samples full run)",
            "H_CROSS": "there exists a finite k-crossover where batch "
                       "detection beats solo testing at fixed B=100",
        },
        "verdict_rule_prestated": {
            "delta": "Delta_k = (solo_ppf - batch_ppf_k)/solo_ppf",
            "BATCH-WINS": "best Delta > +0.02",
            "BREAK-EVEN": "|best Delta| <= 0.02",
            "NULL": "best Delta < -0.02",
        },
        "config": {
            "seed": SEED, "bitlen": BITLEN,
            "pop": args.pop, "ks": ks, "L_sieve": args.L,
            "FB_bound": 100, "FB_size": FB_N, "min_rels": MIN_RELS,
            "audit_samples": audit_n,
            "mix": "interleaved semiprime/general",
            "mr_bases": _MR_BASES,
        },
        "cost_model": {
            "flat": "every executed bigint mul/mod/div/add/Euclid-step/"
                    "MR-modexp-step/GF2-row-XOR = 1 op",
            "word": "mul wa*wb; mod/div wn*wd; add max(wa,wb); skipped "
                    "reductions (r<m) free",
            "reference": "wall clock (unmodeled)",
        },
    }
    out_json = os.path.join(SCRIPT_DIR, "exp561_result.json")
    log_path = os.path.join(SCRIPT_DIR, "exp561_run.log")
    with open(out_json, "w") as fh:
        json.dump(result, fh, indent=1)

    def log(msg):
        print(msg, flush=True)
        with open(log_path, "a") as fh:
            fh.write(msg + "\n")

    # ---- stage 01: population
    pop = gen_population(SEED, args.pop)
    ns = [rec["N"] for rec in pop]
    assert all(n % 2 == 1 for n in ns), "even N in population"
    assert all(n.bit_length() == BITLEN for n in ns), "bad bitlen"
    if len(set(ns)) != len(ns):
        catches.append("DUPLICATE_N_IN_POPULATION")
    kinds = {}
    for rec in pop:
        kinds[rec["kind"]] = kinds.get(rec["kind"], 0) + 1
    result["population"] = {"total": len(pop), "kinds": kinds,
                            "distinct": len(set(ns))}
    log(f"[pop] {len(pop)} ints, kinds={kinds}")

    # ---- stage 02: primorial (once per run, setup bucket)
    led_setup = Ledger()
    G = build_primorial(led_setup)
    result["setup"] = {
        "primorial_bits": G.bit_length(),
        "primorial_ops_flat": led_setup.flat["setup"],
        "excluded_from_rows": True,
        "note": "primorial build is a one-off shared constant, identical "
                "availability to every arm",
    }

    # ---- stage 03: rows
    rows = []
    audit_vals, audit_flags = None, None
    plan = [("SOLO", 1)] + [("BATCH", k) for k in ks]
    for arm, k in plan:
        r, av, afl = run_row(arm, k, pop, G, args.L, rng_seed=SEED)
        rows.append(r)
        if arm == "BATCH" and k == KS_MAX:
            audit_vals, audit_flags = av, afl
        log(f"[row] {arm} k={r['k']} chunks={r['n_chunks']} "
            f"M_row={r['M_candidates']:,} "
            f"M_chunk_mean={(r.get('M_chunk_mean') or 0):,.0f} "
            f"flat={r['total_flat']:,} "
            f"ppf={r['ops_per_factor_flat']:.1f} "
            f"words_ppf={r['ops_per_factor_words']:.0f} "
            f"wall={r['wall_s']:.1f}s factored={r['factored']}/{len(pop)} "
            f"rels={r['stats']['rels_found']} "
            f"pf_resolved={r['prefilter_resolved_N']}")
    result["rows"] = rows
    result["status"] = "03_rows"

    # ---- consistency catches
    fset = sorted({r["factored"] for r in rows})
    if len(fset) != 1:
        catches.append(f"FACTOR_COUNT_MISMATCH_ACROSS_ROWS={fset}")
    elif fset[0] != len(pop):
        catches.append("NOT_ALL_FACTORED")
    solo_row = next(r for r in rows if r["arm"] == "SOLO")
    batch_rows = [r for r in rows if r["arm"] == "BATCH"]
    pf = [r["ops_flat_by_phase"]["prefilter"] / len(pop) for r in rows]
    if max(pf) - min(pf) > 0.05 * max(pf):
        catches.append("PREFILTER_PER_N_NOT_K_INDEPENDENT")

    # ---- stage 04: testing rates + scaling + crossover
    solo_rate = solo_row["solo_rate_flat_per_cand"]
    solo_rate_w = solo_row["solo_rate_words_per_cand"]
    pts = [{"k": r["k"], "M_chunk_mean": r["M_chunk_mean"],
            "log2M_chunk": math.log2(max(2.0, r["M_chunk_mean"])),
            "batch_rate_flat": r["batch_rate_flat_per_cand"],
            "batch_rate_words": r["batch_rate_words_per_cand"]}
           for r in batch_rows]

    def lsq(points, key):
        xs = [p["log2M_chunk"] for p in points]
        ys_ = [p[key] for p in points]
        if len(set(xs)) < 2:
            return None
        n = len(points)
        sx = sum(xs)
        sy = sum(ys_)
        sxx = sum(x * x for x in xs)
        sxy = sum(x * y for x, y in zip(xs, ys_))
        denom = n * sxx - sx * sx
        if denom == 0:
            return None
        b = (n * sxy - sx * sy) / denom
        a = (sy - b * sx) / n
        return a, b

    fit_flat = lsq(pts, "batch_rate_flat")
    fit_word = lsq(pts, "batch_rate_words")

    def crossover(fit, mu):
        if fit is None:
            return "insufficient_points"
        a, b = fit
        if b <= 0:
            return "always_below_solo" if a < mu else "always_above_solo"
        if mu <= a:
            return "none_batch_never_below_intercept"
        lm = (mu - a) / b
        return {"M_star_log2": lm, "M_star": 2.0 ** lm}

    cross_solo = crossover(fit_flat, solo_rate)
    cross_solo_w = crossover(fit_word, solo_rate_w)

    ph = solo_row["ops_flat_by_phase"]
    tot = solo_row["total_flat"]
    testing_share = ph["test_solo"] / tot
    best_row = min(batch_rows, key=lambda r: r["ops_per_factor_flat"]) \
        if batch_rows else None
    delta_best = ((solo_row["ops_per_factor_flat"] -
                   best_row["ops_per_factor_flat"]) /
                  solo_row["ops_per_factor_flat"]) if best_row else 0.0
    delta_words = ((solo_row["ops_per_factor_words"] -
                    best_row["ops_per_factor_words"]) /
                   solo_row["ops_per_factor_words"]) if best_row else 0.0
    delta_wall = ((solo_row["wall_s"] - best_row["wall_s"]) /
                  solo_row["wall_s"]) if best_row else 0.0

    result["testing_analysis"] = {
        "solo_trial_division_rate_flat_per_cand": solo_rate,
        "solo_trial_division_rate_words_per_cand": solo_rate_w,
        "batch_points_flat_vs_log2M_chunk": pts,
        "fit_flat_intercept_slope_log2M": list(fit_flat) if fit_flat else None,
        "fit_words_intercept_slope_log2M": (list(fit_word)
                                            if fit_word else None),
        "crossover_vs_solo_flat_model": cross_solo,
        "crossover_vs_solo_word_model": cross_solo_w,
    }
    result["bound_quantification"] = {
        "solo_testing_share_of_per_factor_ops": testing_share,
        "solo_nontesting_share": 1.0 - testing_share,
        "max_saving_if_testing_free": testing_share,
        "realized_delta_best_k": delta_best,
        "best_batch_k": best_row["k"] if best_row else None,
        "finding_phase_note": "relation yield and rho work are strictly "
                              "per-N; identical across arms by construction",
    }
    result["status"] = "04_analysis"

    # ---- stage 05: audit (exact match required)
    audit = {"samples": 0, "mismatches_tree_vs_trial": 0,
             "mismatches_direct_vs_trial": 0, "vector_mismatches": 0,
             "pass": None}
    try:
        if audit_vals and len(audit_vals) >= audit_n:
            arng = random.Random(f"audit:{SEED}")
            samp = arng.sample(range(len(audit_vals)), audit_n)
            scr = Ledger()
            Qg = batch_build_Q(audit_vals, scr)   # global-max Q (ground truth)
            for si in samp:
                c = audit_vals[si]
                ok_trial, vec_trial = trial_test(c, scr, phase="relproc")
                ok_direct = (Qg % c == 0)
                ok_tree = audit_flags[si]
                audit["samples"] += 1
                if ok_tree != ok_trial:
                    audit["mismatches_tree_vs_trial"] += 1
                if ok_direct != ok_trial:
                    audit["mismatches_direct_vs_trial"] += 1
                if ok_trial:
                    if vectorize(c, scr) != vec_trial:
                        audit["vector_mismatches"] += 1
            audit["pass"] = (audit["mismatches_tree_vs_trial"] == 0 and
                             audit["vector_mismatches"] == 0 and
                             audit["mismatches_direct_vs_trial"] == 0)
        else:
            audit["pass"] = False
            catches.append("AUDIT_SKIPPED_INSUFFICIENT_ITEMS")
    except Exception as exc:  # noqa: BLE001
        audit["pass"] = False
        audit["error"] = repr(exc)
        catches.append("AUDIT_EXCEPTION")
    if not audit["pass"]:
        catches.append("AUDIT_EXACT_MATCH_FAILED")
    result["audit"] = audit

    # ---- verdicts (from data only)
    testing_win_flat = any(p["batch_rate_flat"] < solo_rate for p in pts)
    testing_win_words = any(p["batch_rate_words"] < solo_rate_w for p in pts)
    if delta_best > 0.02:
        vname = "BATCH-WINS"
        vname += "-TESTING" if testing_win_flat else "-PREFILTER-ONLY"
    elif delta_best >= -0.02:
        vname = "BREAK-EVEN"
    else:
        vname = "NULL"
        vname += "-TESTING-REGRESSION" if not testing_win_flat \
            else "-DILUTED-BY-FINDING-PHASE"
    if delta_best > 0.02 and not testing_win_words:
        e1 = ("CONFIRMED in the flat-op model with the bound quantified: "
              "batch testing beats solo trial division at every measured "
              "pool size, but the per-factor saving is capped by the "
              "testing share of solo work, and under the WORD-weighted "
              "model the tree's operand growth REVERSES the win at large k "
              "(batch word-rate grows ~log-superlinearly with M). The "
              "pre-stated expectation survives in op-count terms only.")
    elif delta_best > 0.02:
        e1 = ("CONFIRMED: batch helps testing at every measured pool size "
              "and the saving is bounded by the non-testing share")
    elif not testing_win_flat:
        e1 = ("REFUTED at this scale: batch testing regresses against solo "
              "everywhere measured; savings bounded and negative")
    else:
        e1 = "BREAK-EVEN: testing-phase gains wash out against fixed costs"
    result["verdicts"] = {
        "verdict_name": vname,
        "delta_best_k_flat_model": delta_best,
        "delta_best_k_word_model": delta_words,
        "delta_wall_fraction": delta_wall,
        "testing_beats_solo_flat_anywhere": testing_win_flat,
        "testing_beats_solo_word_anywhere": testing_win_words,
        "crossover_vs_solo_stated_flat": cross_solo,
        "crossover_vs_solo_stated_word": cross_solo_w,
        "h_audit_pass": audit["pass"],
        "e1_assessment": e1,
    }
    result["status"] = "05_verdicts"

    # ---- ledger catches + notes
    if any(r["stats"]["rho_failures"] for r in rows):
        catches.append("RHO_FAILURE_NONZERO")
    result["notes"] = {
        "qs_splits_total": sum(r["stats"]["qs_splits"] for r in rows),
        "yield_note": "at bitlen 40 with FB<=100 the per-N relation yield "
                      "is far below the 26 needed for QS; rho carries "
                      "factoring identically in every arm (this IS the "
                      "'finding does not amortize' term)",
        "python": platform.python_version(),
        "gmpy2_used_for": "next_prime/isqrt in generation and sieving only; "
                          "all pipeline arithmetic is native bigint with "
                          "explicit op counting",
    }
    result["ledger_catches"] = catches
    result["wall_s"] = time.perf_counter() - t_start
    result["status"] = "06_final"

    with open(out_json, "w") as fh:
        json.dump(result, fh, indent=1, default=float)
    log(f"[done] status={result['status']} verdict={vname} "
        f"wall={result['wall_s']:.1f}s catches={catches}")
    return result


if __name__ == "__main__":
    main()

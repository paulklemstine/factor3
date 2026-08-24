#!/usr/bin/env python3
"""EXP 556 'TREE-RELATION-SIEVE' -- validity analysis + empirical profile of the
proposal: use Berggren-tree node values a_k = A(m_k,n_k) = m_k^2 - n_k^2 as a
Dixon-style relation pool (store exponent vectors of B-smooth a_k, combine to
Pi a_i = Y^2, output gcd(Pi m_i - Y, N)).

DERIVATION (written BEFORE any simulation; predictions registered pre-data).

SETUP. Berggren tree on (m,n), root (2,1), children
  M1: (m,n) -> (2m-n, m),  M2: (m,n) -> (2m+n, m),  M3: (m,n) -> (m+2n, n).
Node value A(m,n) = m^2 - n^2 = (m-n)(m+n).  Every node keeps m>n>0.

LEMMA 1 (strict monotonicity). A(child) > A(parent):
  M1: A' - A = 2(m-n)^2 > 0.
  M2: A' - A = 2(m+n)^2 > 0   (since A'' = (2m+n)^2 - m^2 = 3m^2+4mn+n^2).
  M3: A' - A = 4n(m+n) > 0    (since A''' = (m+2n)^2 - n^2 = m^2+4mn+3n^2).
Corollary: value-capped traversal never needs to revisit a subtree.

LEMMA 2 (coprime odd split). Inductively every node has gcd(m,n)=1 and
opposite parity: root (2,1) qualifies; gcd(2m+-n,m)=gcd(n,m)=1,
gcd(m+2n,n)=gcd(m,n)=1; parities: 2m+-n has parity of n (m even/n odd ->
odd/even stays opposite; swapped likewise), m+2n has parity of m.  Hence
m-n and m+n are both ODD and gcd(m-n, m+n) divides 2*gcd(m,n)=2 and is odd,
so gcd(m-n, m+n)=1.  Therefore, for every odd prime p<=B,
v_p(a) = v_p(m-n) + v_p(m+n), and
  a is B-smooth  <=>  BOTH m-n and m+n are B-smooth,
the two events factorizing exactly (coprimality kills shared primes; 2 is
absent).  If m-n and m+n behave like independent integers of size ~sqrt(a),
P(a smooth) ~ rho(u/2)^2 with u = log2(a)/log2(B): a LARGE boost over the
matched-size random baseline rho(u) (naive ratio rho(u/2)^2/rho(u) ~ 44x at
u=6).  Nodes with unbalanced splits (m-n ~ 1, the slow spine) degrade to
single-factor behavior, so the realized aggregate boost should land BELOW the
naive value but ABOVE 1 (registered as P2: sign firm, magnitude in [2x, 44x]).

MAIN THEOREM (invalidity of the proposal as stated).  Fix a finite pool T of
tree nodes and any subset S with Pi_{i in S} a_i = Y^2 over Z (found by GF(2)
elimination on exponent-parity vectors).  The proposal outputs
g = gcd(X - Y, N) with X = Pi_{i in S} m_i.  Then:
  (i)  The identity Pi a_i = Y^2 lives entirely in Z; no step of the
       construction reduces anything mod N, so it implies NO congruence mod N.
  (ii) The output splits N iff p | (X-Y) or q | (X-Y); i.e. success <=> the
       congruence X = Y (mod p or q) holds.  Nothing in (i) bears on this.
  (iii) The only square root of Y^2 mod N obtainable without factoring is
       Y itself; choosing X := Y gives g = gcd(0, N) = N, the trivial gcd.
  (iv) For a FIXED pool, the family {(X_S, Y_S)} is independent of N -- the
       entire relation-collection phase references N zero times.  Hence no
       selection of S can correlate X_S with the residues of p,q.  Under the
       (empirically testable) heuristic that X_S mod p is uniform,
       P(success per ticket) = 1/p + 1/q = O(N^{-1/2}): identical to drawing
       a uniform random integer W and testing gcd(W, N).
  (v)  Adaptivity (picking S using past gcd outcomes) buys only extra lottery
       tickets; expected tickets ~ min(p,q).
Equivalence class: {random-gcd} == guessing a nontrivial square root of a
known square mod N, a problem randomized-polytime-equivalent to FACTORING.
Any corrected variant that works must produce u,v with uv = square AND
u = v (mod N) -- i.e. genuine Dixon/QS relations.  Coupling tree values into
such congruences requires either x^2 mod N landing in the (zero-density)
tree-value set, or a modular-square-root oracle (= factoring).  Barrier-8
framing: the proposal is NOT QS-in-disguise (it lacks the defining
congruence); it is a lottery whose only success channel is generic gcd luck.
The tree's ONLY conceivable contribution is as a smooth-integer FARM (yield
question == Part B), which validity-wise is worth nothing beyond lab paper
130's law (smooth integers ensemble-equal to random).

PREDICTIONS (registered before data):
  P1 (spec-BFS starvation): plain 50k-node BFS capped at 2^80 tops out around
      depth 10-12 where typical values are << 2^30; in-window [2^30,2^60]
      yield ~ 0 (value growth needs M2-heavy words; shallow BFS cannot
      accumulate ~30 bits).
  P2 (coprime-split boost): tree B-smoothness rate > matched-bitlen random
      rate for B in {100, 1000}; magnitude between 2x and the naive 44x;
      dose-response: rate increases with balance (m+n)/(m-n).
  P3 (pool-law parity): x^2-N' control vs random control ratio ~ 1.0 in every
      bitlen bucket (paper 130).
  P4 (lottery end-to-end): tree-ticket success rate on 24-bit semiprimes ==
      random-gcd baseline (~1/p + 1/q ~ 5e-4..7e-4 per ticket);
      relations-needed ~ FB dimension + small overhead.

DESIGN (fixed before data):
  Phase 0  numeric lemma checks (Lemmas 1-2 asserted on generated nodes).
  Phase 1  SPEC-FIDELITY BFS: 50000 expanded nodes, cap 2^80, report depth,
           in-window count (tests P1).
  Phase 2  WINDOW COLLECTOR (disclosed deviation; BFS provably cannot harvest
           the window -- see P1): steered random-root-path walker; every
           emitted node carries its true root-to-node word.  Target 50000
           nodes with A in [2^30, 2^60].  NOT uniform over the window
           (disclosed caveat; controls matched per-bitlen, plus a
           balance-stratified dose-response as internal validation).
           Controls drawn with xCTRL_MULT more samples per bitlen bucket
           than the tree sample (baseline rates are tiny); ratios compare
           rates, so the scaling is valid.
  Phase 3  smoothness profiles B in {100,1000} for TREE vs (i) matched
           random ints vs (ii) x^2-N' semiprime control; ratios with
           bootstrap CIs, per-bitlen buckets, dose-response quartiles.
  Phase 4  END-TO-END toy: pool = B-smooth tree values; GF(2) dependencies;
           VERIFY Pi a_i == Y^2 exactly; X = Pi m_i; gcd(X-Y, N) over 300
           fresh 24-bit semiprimes vs random-gcd baseline on the same N.
           Disclosed deviation: the relation pool gets an extra steered pass
           at REDUCED window [2^25, 2^40] because the spec-window B1000-smooth
           yield sits below the FB dimension requirement (validity test is
           indifferent to the size of a); recorded in result json.
"""
import argparse
import json
import math
import os
import random
import sys
import time
from math import gcd, prod

import numpy as np

from gmpy2 import mpz, is_prime, isqrt, next_prime

OUT_DIR = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-21-resume"
SCRIPT = os.path.join(OUT_DIR, "exp556_tree_sieve.py")
RESULT = os.path.join(OUT_DIR, "exp556_result.json")
LOG = os.path.join(OUT_DIR, "exp556_run.log")

ROOT = (2, 1)
CAP_SPEC = 1 << 80          # Part B spec cap
WIN_LO, WIN_HI = 1 << 30, 1 << 60
SEED = 20260823


def moves(m, n):
    return ((2 * m - n, m), (2 * m + n, m), (m + 2 * n, n))


def aval(m, n):
    return (m - n) * (m + n)


# ---------------------------------------------------------------- phase 1
def bfs_spec(budget, cap, win_lo, win_hi):
    """Spec-fidelity BFS: expand `budget` nodes, prune children above cap."""
    from collections import deque
    q = deque([(ROOT, 0)])
    expanded = 0
    max_depth = 0
    max_val = 0
    in_win = 0
    seen = {ROOT}
    dup = 0
    while q and expanded < budget:
        (m, n), d = q.popleft()
        expanded += 1
        max_depth = max(max_depth, d)
        a = aval(m, n)
        if a > max_val:
            max_val = a
        if win_lo <= a <= win_hi:
            in_win += 1
        for cm, cn in moves(m, n):
            ca = aval(cm, cn)
            if ca > cap:
                continue
            if (cm, cn) in seen:
                dup += 1
                continue
            seen.add((cm, cn))
            q.append(((cm, cn), d + 1))
    return dict(expanded=expanded, max_depth=max_depth, max_val=max_val,
                max_val_bits=max_val.bit_length(), in_window=in_win,
                frontier_left=len(q), dup_children=dup, seen_nodes=len(seen))


# ---------------------------------------------------------------- phase 2
def steered_walk(rng, lo=None, hi=None, kappa=1.0, max_steps=240):
    """One walker attempt: steer log2(A) upward to a uniform target in
    [lo,hi] bits; emit first node whose value reaches the target.  Returns
    ((m,n), word) or None."""
    lo = WIN_LO if lo is None else lo
    hi = WIN_HI if hi is None else hi
    cap = hi
    T = rng.randint(lo.bit_length(), hi.bit_length() - 1)
    m, n = ROOT
    word = []
    a = aval(m, n)
    for _ in range(max_steps):
        if a.bit_length() >= T:
            return ((m, n), tuple(word))
        cand = []
        la = math.log2(a)
        for idx, (cm, cn) in enumerate(moves(m, n)):
            ca = aval(cm, cn)
            if ca <= cap:
                cand.append((math.exp(kappa * (math.log2(ca) - la)), cm, cn, idx))
        if not cand:
            return None
        tot = sum(w for w, *_ in cand)
        r = rng.random() * tot
        acc = 0.0
        for w, cm, cn, idx in cand:
            acc += w
            if acc >= r:
                m, n = cm, cn
                a = aval(m, n)
                word.append(idx)
                break
    return None


def collect_window(target, rng, lo=None, hi=None):
    out = []
    tries = 0
    while len(out) < target:
        tries += 1
        r = steered_walk(rng, lo, hi)
        if r is None:
            continue
        (m, n), word = r
        a = aval(m, n)
        if (WIN_LO if lo is None else lo) <= a <= (WIN_HI if hi is None else hi):
            out.append((m, n, a, word))
    return out, tries


# ---------------------------------------------------------------- phase 3
def sieve_primes(limit):
    s = bytearray([1]) * (limit + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, int(limit ** 0.5) + 1):
        if s[i]:
            s[i * i:: i] = bytearray(len(s[i * i:: i]))
    return [i for i in range(limit + 1) if s[i]]


PRIMES_1000 = None
PRIMES_100 = None
PBIG_1000 = None
PBIG_100 = None


def is_b_smooth(v, primes, pbig=None):
    """Exact B-smoothness test.  Primary path: gcd-chain against PBIG =
    prod(primes<=B) -- x //= gcd(x,PBIG) peels one off every multiplicity per
    round, so rounds = max exponent; x==1 iff fully B-smooth.  Exactness was
    verified against an exhaustive SPF-sieve ground truth over [2^20,2^21)
    (24.39% B1000-smooth).
    LEDGER CATCH (found in smoke): the textbook trial-division early-exit
    'if p*p > v: break' is WRONG -- after small primes are stripped the
    remainder can be a PRODUCT of two primes both in (sqrt(v), B], e.g.
    1147 = 31*37 exits at p=37 with v=37 and misclassifies; the sieve showed
    the buggy version undercounts 24.39% -> 0.52%."""
    if v == 1:
        return True
    if pbig is not None:
        x = mpz(v)
        while x > 1:
            d = gcd(x, pbig)
            if d == 1:
                break
            x //= d
        return x == 1
    for p in primes:
        while v % p == 0:
            v //= p
        if v == 1:
            return True
    return v == 1


def rand_int_control(counts, rng):
    out = []
    for b, c in counts.items():
        lo = 1 << (b - 1)
        hi = (1 << b) - 1
        out.extend(rng.randint(lo, hi) for _ in range(c))
    return out


def rand_prime(rng, bits):
    while True:
        c = mpz(rng.getrandbits(bits) | (1 << (bits - 1)) | 1)
        if is_prime(c):
            return int(c)


def xsq_control(counts, rng):
    """Values x^2 - N' for random semiprimes N', regrouped by actual
    bit_length so matching to the other populations is by final size."""
    out = []
    want = dict(counts)
    got = {}
    guard = 0
    glimit = max(60000, 40 * sum(want.values()))
    while any(got.get(b, 0) < c for b, c in want.items()):
        guard += 1
        if guard > glimit:
            break
        b = rng.choice([b for b, c in want.items() if got.get(b, 0) < c])
        h = max(2, b // 2)
        p = rand_prime(rng, h)
        q = rand_prime(rng, b - h)
        N = p * q
        r = isqrt(mpz(N))
        x = rng.randint(int(r) + 1, 2 * int(r))
        v = x * x - N
        bv = v.bit_length()
        if v >= WIN_LO // 4 and got.get(bv, 0) < want.get(bv, 0):
            got[bv] = got.get(bv, 0) + 1
            out.append(v)
    return out


def bucket_counts(vals):
    d = {}
    for v in vals:
        d[v.bit_length()] = d.get(v.bit_length(), 0) + 1
    return d


def boot_ratio(tree_flags, ctl_flags, nboot=20000, seed=1):
    """Ratio of smooth rates; PARAMETRIC bootstrap CI (binomial resampling of
    each rate at its own n -- nonparametric resample was too slow at n=50k;
    disclosed).  Infinite ratios (zero control draws) are dropped before
    percentile extraction; if >5% of boots are infinite the CI is flagged."""
    nt, nc = len(tree_flags), len(ctl_flags)
    rt = sum(tree_flags) / nt
    rc = sum(ctl_flags) / nc
    rs = np.random.default_rng(seed)
    bt = rs.binomial(nt, rt, nboot) / nt
    bc = rs.binomial(nc, rc, nboot) / nc
    with np.errstate(divide="ignore", invalid="ignore"):
        ratios = np.where(bc > 0, bt / np.maximum(bc, 1e-300), np.inf)
    fin = ratios[np.isfinite(ratios)]
    info = dict(inf_frac=float(np.mean(~np.isfinite(ratios))))
    if len(fin) < 100:
        return rt, rc, (float("inf") if rc == 0 else rt / rc), None, None, info
    lo, hi = np.percentile(fin, [2.5, 97.5])
    return rt, rc, float(rt / rc if rc > 0 else math.inf), float(lo), float(hi), info


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    ph = k / n
    d = 1 + z * z / n
    c = ph + z * z / (2 * n)
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n))
    return (max(0.0, (c - h) / d), min(1.0, (c + h) / d))


# ---------------------------------------------------------------- phase 4
class GF2:
    """Incremental GF(2) linear algebra with provenance tracking."""

    def __init__(self, dim):
        self.dim = dim
        self.pivots = {}       # col -> (row_mask, prov_mask)
        self.rows = []         # raw rows
        self.n_dep = 0

    def insert(self, row, idx):
        cur, prov = row, 1 << idx
        while cur:
            c = (cur & -cur).bit_length() - 1
            if c in self.pivots:
                r2, p2 = self.pivots[c]
                cur ^= r2
                prov ^= p2
            else:
                self.pivots[c] = (cur, prov)
                return None
        self.n_dep += 1
        return prov  # bitmask over row indices -> dependent subset


def dependency_masks(rows, dim, want, rng):
    """Collect GF(2) dependency masks (bitmask over row ids whose XOR of rows
    is zero => product of the corresponding a_i is an exact square) by
    incremental insertion over several shuffled orders.  Provenance masks make
    each dependency exact by construction."""
    masks, seenm = [], set()
    rank_rows = None
    for trial in range(8):
        order = list(range(len(rows)))
        rng.shuffle(order)
        pivots = {}
        for idx in order:
            cur, pv = rows[idx], 1 << idx
            while cur:
                c = (cur & -cur).bit_length() - 1
                if c in pivots:
                    r2, p2 = pivots[c]
                    cur ^= r2
                    pv ^= p2
                else:
                    pivots[c] = (cur, pv)
                    break
            if cur == 0 and pv != 0 and (pv & (pv - 1)) == 0:
                # single-row "dependency" impossible for smooth>1 values;
                # means row was zero -- skip defensively
                continue
            if cur == 0:
                if pv not in seenm:
                    seenm.add(pv)
                    masks.append(pv)
                    if len(masks) >= want:
                        break
        rank_rows = len(pivots)
        if len(masks) >= want:
            break
    return masks, rank_rows


def subset_from_mask(mask, items):
    return [items[i] for i in range(mask.bit_length()) if (mask >> i) & 1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    t0 = time.time()
    global PRIMES_1000, PRIMES_100
    rng = random.Random(SEED)

    global WIN_LO, WIN_HI
    if args.smoke:
        # smoke-only: shrink the value window so tiny samples produce smooths
        # (mechanics check; all full-run science uses [2^30, 2^60])
        WIN_LO, WIN_HI = 1 << 16, 1 << 28

    N_BFS = 50_000 // (50 if args.smoke else 1)
    N_WIN = 50_000 // (100 if args.smoke else 1)
    N_NS = 300 // (10 if args.smoke else 1)
    MAX_SUBSETS = 8 if args.smoke else 40
    NBOOT = 5000 if args.smoke else 20000

    res = {"exp": 556, "name": "TREE-RELATION-SIEVE",
           "seed": SEED, "smoke": bool(args.smoke),
           "started": time.strftime("%Y-%m-%d %H:%M:%S")}
    print(f"[exp556] smoke={args.smoke} start", flush=True)

    PRIMES_1000 = sieve_primes(1000)
    PRIMES_100 = [p for p in PRIMES_1000 if p <= 100]
    global PBIG_100, PBIG_1000
    PBIG_100 = prod(PRIMES_100)
    PBIG_1000 = prod(PRIMES_1000)

    # ---------------- phase 0: lemma checks -----------------------------
    chk = {"lemma1_violations": 0, "lemma2_violations": 0, "checked": 0}
    stack = [ROOT]
    while stack and chk["checked"] < 20000:
        m, n = stack.pop()
        a = aval(m, n)
        for cm, cn in moves(m, n):
            if aval(cm, cn) <= a:
                chk["lemma1_violations"] += 1
            if (cn - cm) % 2 == 0 or gcd(cm - cn, cm + cn) != 1 or gcd(cm, cn) != 1:
                chk["lemma2_violations"] += 1
            stack.append((cm, cn))
        chk["checked"] += 1
    res["phase0_lemma_checks"] = chk
    print(f"[phase0] {chk}", flush=True)

    # ---------------- phase 1: spec BFS ---------------------------------
    bfs = bfs_spec(N_BFS, CAP_SPEC, 1 << 30, 1 << 60)  # SPEC window pinned
    res["phase1_spec_bfs"] = bfs
    p1 = "CONFIRMED" if bfs["in_window"] == 0 and bfs["max_val"] < (1 << 30) \
        else "REFUTED"
    res["P1_spec_bfs_starvation"] = dict(
        verdict=p1, detail=f"max_val={bfs['max_val']} ({bfs['max_val_bits']} bits), "
                           f"depth={bfs['max_depth']}, in_window={bfs['in_window']}")
    print(f"[phase1] {bfs} -> P1 {p1}", flush=True)

    # ---------------- phase 2: window collector -------------------------
    nodes, tries = collect_window(N_WIN, rng)
    seen = set()
    uniq = []
    val_dupes = 0
    for m, n, a, w in nodes:
        if (m, n) in seen:
            val_dupes += 1
            continue
        seen.add((m, n))
        uniq.append((m, n, a, w))
    # re-verify lemmas on the harvested population
    lv = sum(1 for m, n, a, w in uniq
             if (m - n) % 2 == 0 or gcd(m - n, m + n) != 1)
    tree_vals = [a for _, _, a, _ in uniq]
    bal = [math.log2((m + n) / (m - n)) for m, n, a, _ in uniq]
    depths = [len(w) for _, _, _, w in uniq]
    res["phase2_collector"] = dict(
        requested=N_WIN, emitted=len(nodes), unique=len(uniq),
        attempts=tries, dup_nodes=val_dupes, lemma2_violations_on_sample=lv,
        depth_min=min(depths), depth_med=sorted(depths)[len(depths) // 2],
        depth_max=max(depths),
        balance_log2_ratio_quartiles=[
            round(sorted(bal)[int(q * len(bal))], 3) for q in (0.25, 0.5, 0.75)])
    print(f"[phase2] unique={len(uniq)} tries={tries} "
          f"depth med={res['phase2_collector']['depth_med']}", flush=True)

    # ---------------- phase 3: smoothness --------------------------------
    # controls are drawn with MORE samples than the tree sample (same bitlen
    # mix, xCTRL_MULT per bucket) because baseline smooth rates are tiny;
    # ratios use rates so scaling is valid.  Disclosed.
    CTRL_MULT = 4 if args.smoke else 8
    counts = bucket_counts(tree_vals)
    counts_c = {b: c * CTRL_MULT for b, c in counts.items()}
    rnd_vals = rand_int_control(counts_c, rng)
    xsq_vals = xsq_control(counts_c, rng)
    res["phase3_design"] = dict(
        tree_n=len(tree_vals), ctrl_mult=CTRL_MULT,
        rand_n=len(rnd_vals), xsq_n=len(xsq_vals),
        bitlen_buckets={str(b): counts[b] for b in sorted(counts)})
    out3 = {}
    for tag, primes, pbig in (("B100", PRIMES_100, PBIG_100),
                              ("B1000", PRIMES_1000, PBIG_1000)):
        ft = [1 if is_b_smooth(v, primes, pbig) else 0 for v in tree_vals]
        fr = [1 if is_b_smooth(v, primes, pbig) else 0 for v in rnd_vals]
        fx = [1 if is_b_smooth(v, primes, pbig) else 0 for v in xsq_vals]
        rt, rr, ratio_tr, lo_tr, hi_tr, info1 = boot_ratio(ft, fr, NBOOT, seed=SEED + 1)
        _, rx, ratio_tx, lo_tx, hi_tx, info2 = boot_ratio(ft, fx, NBOOT, seed=SEED + 2)
        _, rxx, ratio_xx, lo_xx, hi_xx, info3 = boot_ratio(fx, fr, NBOOT, seed=SEED + 3)
        # dose-response: smooth rate by balance quartile (tree only)
        order = sorted(range(len(bal)), key=lambda i: bal[i])
        q = len(order) // 4
        dose = []
        for qi in range(4):
            idx = order[qi * q: (qi + 1) * q] if qi < 3 else order[3 * q:]
            kk = sum(ft[i] for i in idx)
            dose.append(dict(quartile=qi + 1,
                             bal_range=[round(min(bal[i] for i in idx), 2),
                                        round(max(bal[i] for i in idx), 2)],
                             k=kk, n=len(idx),
                             rate=kk / len(idx),
                             ci=list(wilson(kk, len(idx)))))
        out3[tag] = dict(
            tree_rate=rt, rand_rate=rr, xsq_rate=rx,
            k_tree=int(sum(ft)), k_rand=int(sum(fr)), k_xsq=int(sum(fx)),
            tree_vs_rand=dict(ratio=ratio_tr, ci=[lo_tr, hi_tr], inf_frac=info1["inf_frac"]),
            tree_vs_xsq=dict(ratio=ratio_tx, ci=[lo_tx, hi_tx], inf_frac=info2["inf_frac"]),
            xsq_vs_rand=dict(ratio=ratio_xx, ci=[lo_xx, hi_xx], inf_frac=info3["inf_frac"]),
            dose_response=dose)
        fmt = lambda x: "inf" if x is None else f"{x:.2f}"
        print(f"[phase3:{tag}] tree={rt:.5f} rand={rr:.6f} xsq={rx:.6f} "
              f"T/R={ratio_tr:.2f}[{fmt(lo_tr)},{fmt(hi_tr)}] "
              f"T/X={ratio_tx:.2f}[{fmt(lo_tx)},{fmt(hi_tx)}] "
              f"X/R={ratio_xx:.2f}[{fmt(lo_xx)},{fmt(hi_xx)}]", flush=True)
    # sanitize inf/nan for JSON
    def clean(o):
        if isinstance(o, dict):
            return {k: clean(v) for k, v in o.items()}
        if isinstance(o, list):
            return [clean(v) for v in o]
        if isinstance(o, float) and (math.isinf(o) or math.isnan(o)):
            return "inf" if math.isinf(o) else "nan"
        return o

    res["phase3_smoothness"] = clean(out3)
    b1k = out3["B1000"]
    p2_lo = b1k["tree_vs_rand"]["ci"][0]
    p2 = "CONFIRMED" if ((p2_lo is not None and p2_lo > 1.0) or
                         (b1k["k_rand"] == 0 and b1k["k_tree"] >= 5)) else "REFUTED"
    naive = ("below-naive" if b1k["tree_vs_rand"]["ratio"] < 44.0
             else "at/above-naive")
    res["P2_coprime_split_boost"] = dict(verdict=p2,
        tree_vs_rand_ratio=clean(b1k["tree_vs_rand"]), magnitude=naive,
        dose_response_monotone=all(
            b1k["dose_response"][i]["rate"] <=
            b1k["dose_response"][i + 1]["rate"] + 1e-12
            for i in range(3)))
    p3cell = out3["B100"]["xsq_vs_rand"]
    if p3cell["ci"][0] is None:
        p3 = "LOW-POWER(control-zero)"
    else:
        p3 = "CONSISTENT" if p3cell["ci"][0] <= 1.0 <= p3cell["ci"][1] else "DEVIATION"
    res["P3_pool_law_parity"] = dict(verdict=p3, xsq_vs_rand_B100=clean(p3cell),
                                     xsq_vs_rand_B1000=clean(out3["B1000"]["xsq_vs_rand"]))

    # ---------------- phase 4: end-to-end toy ----------------------------
    # Dedicated pool pass at REDUCED window [2^25, 2^40]: at the spec window
    # the expected B1000-smooth yield (~2.5x rho(4.5)*47.7k ~ 130) sits below
    # the FB dimension requirement (168+20); validity of the lottery test is
    # indifferent to the size of a.  Disclosed deviation.
    PH4_LO, PH4_HI = 1 << 25, 1 << 40
    ph4_nodes, ph4_tries = collect_window(N_WIN, rng, PH4_LO, PH4_HI)
    print(f"[phase4-pool] extra nodes={len(ph4_nodes)} tries={ph4_tries}",
          flush=True)
    fb_tag = "B1000"
    fb_primes = PRIMES_1000
    pool = {}
    for m, n, a, w in list(uniq) + ph4_nodes:
        if a in pool:
            continue
        if is_b_smooth(a, fb_primes, PBIG_1000):
            pool[a] = (m, n)
    dim = len(fb_primes)
    pidx = {p: i for i, p in enumerate(fb_primes)}
    res.setdefault("phase4_pool", {})["collector"] = dict(
        note="reduced window [2^25,2^40] extra pass",
        nodes=len(ph4_nodes), tries=ph4_tries,
        window_bits=[PH4_LO.bit_length(), PH4_HI.bit_length()])

    def row_of(a):
        r = 0
        v = a
        for p in fb_primes:
            if p * p > v and v == 1:
                break
            while v % p == 0:
                v //= p
                r ^= 1 << pidx[p]   # toggle: exponent PARITY, not presence
            if v == 1:
                break
        return r

    items = sorted(pool.keys())
    rows = [row_of(a) for a in items]
    # fallback to B100 if pool short of dim+20
    fb_note = f"FB={fb_tag} dim={dim}"
    if len(items) < dim + 20:
        fb_tag = "B100"
        fb_primes = PRIMES_100
        dim = len(fb_primes)
        pidx = {p: i for i, p in enumerate(fb_primes)}
        pool2 = {}
        pb = PBIG_100 if fb_tag == "B100" else None
        for m, n, a, w in list(uniq) + ph4_nodes:
            if a not in pool2 and is_b_smooth(a, fb_primes, pb):
                pool2[a] = (m, n)
        pool = pool2
        items = sorted(pool.keys())
        rows = [row_of(a) for a in items]
        fb_note = f"FALLBACK FB=B100 dim={dim}"
    if "phase4_pool" not in res:
        res["phase4_pool"] = {}
    res["phase4_pool"].update(note=fb_note, pool=len(items), dim=dim)

    # relations needed: 30 random insertion orders, first-dependency count
    rn_rng = random.Random(SEED + 7)
    rel_need = []
    for trial in range(30 if not args.smoke else 5):
        order = list(range(len(rows)))
        rn_rng.shuffle(order)
        g = GF2(dim)
        cnt = 0
        for idx in order:
            cnt += 1
            if g.insert(rows[idx], idx) is not None:
                break
        rel_need.append(cnt)
    res["phase4_relations_needed"] = dict(
        trials=len(rel_need), mean=sum(rel_need) / len(rel_need),
        min=min(rel_need), max=max(rel_need))

    masks, rank = dependency_masks(rows, dim, MAX_SUBSETS * 3, random.Random(SEED + 11))
    rng.shuffle(masks)
    subsets = masks[:MAX_SUBSETS]
    res["phase4_subsets"] = {"rank": rank}
    tickets = []
    for mask in subsets:
        S_items = subset_from_mask(mask, list(enumerate(items)))
        proda = prod(items[i] for i, _ in S_items)
        Y2 = isqrt(mpz(proda))
        assert Y2 * Y2 == proda, "square-root identity failed"  # verified claim
        X = prod(pool[items[i]][0] for i, _ in S_items)
        tickets.append((X, int(Y2), len(S_items)))
    res["phase4_subsets"].update(n=len(tickets),
                                 support_sizes=[t[2] for t in tickets])
    print(f"[phase4] pool={len(items)} dim={dim} deps={len(tickets)}",
          flush=True)

    if not tickets:
        res["phase4_end_to_end"] = dict(skipped=True,
            reason="no GF(2) dependency found in pool (pool too small)")
        res["P4_lottery_end_to_end"] = dict(verdict="SKIPPED")
        res["part_a_verdict"] = (
            "INVALID AS STATED (theory verdict unaffected): identity over Z "
            "never reduces mod N; success requires N | Pi m_i - Y which nothing "
            "supplies; equivalence class is random-gcd.")
        res["runtime_s"] = round(time.time() - t0, 1)
        with open(RESULT, "w") as f:
            json.dump(clean(res), f, indent=1, default=str)
        print("result (phase4 skipped) ->", RESULT, flush=True)
        return
    # fresh toy semiprimes, 24-bit
    Ns = []
    while len(Ns) < N_NS:
        p = rand_prime(rng, 12)
        q = rand_prime(rng, 12)
        if p == q:
            continue
        Ns.append((p * q, p, q))
    succ = triv = fail = 0
    bsucc = bfail = 0
    for N, p, q in Ns:
        for X, Y, _ in tickets:
            g = gcd(X - Y, N)
            if g == N:
                triv += 1
            elif g in (p, q):
                succ += 1
            else:
                fail += 1
        for _ in range(len(tickets)):
            R = rng.getrandbits(256) | 1
            gb = gcd(R, N)
            if gb in (p, q):
                bsucc += 1
            else:
                bfail += 1
    tt = len(tickets) * len(Ns)
    res["phase4_end_to_end"] = dict(
        n_semiprimes=len(Ns), tickets_total=tt,
        tree_success=succ, tree_trivial_gcd_eq_N=triv, tree_fail=fail,
        tree_rate=succ / tt, tree_ci=list(wilson(succ, tt)),
        baseline_success=bsucc, baseline_rate=bsucc / tt,
        baseline_ci=list(wilson(bsucc, tt)),
        heuristic_per_ticket=1 / (sum(p for _, p, _ in Ns) / len(Ns)) +
                             1 / (sum(q for _, _, q in Ns) / len(Ns)))
    p4gap = abs(res["phase4_end_to_end"]["tree_rate"] -
                res["phase4_end_to_end"]["baseline_rate"])
    p4 = "CONSISTENT-LOTTERY" if (
        res["phase4_end_to_end"]["tree_ci"][0] <=
        res["phase4_end_to_end"]["baseline_rate"] <=
        res["phase4_end_to_end"]["tree_ci"][1]) or p4gap < 3e-3 else "ANOMALY"
    res["P4_lottery_end_to_end"] = dict(verdict=p4)

    # ---------------- verdict -------------------------------------------
    res["part_a_verdict"] = (
        "INVALID AS STATED: the identity Pi a_i = Y^2 is over Z and never "
        "reduces mod N; success requires N | Pi m_i - Y, which nothing in the "
        "construction supplies. The only square root of Y^2 mod N available "
        "without factoring is Y itself (X:=Y gives gcd = N, trivial). For a "
        "fixed pool the pairs (X_S, Y_S) are independent of N, so per-ticket "
        "success is the generic-gcd luck 1/p + 1/q = O(N^-1/2) -- the "
        "equivalence class is random-gcd, i.e. guessing a nontrivial square "
        "root mod N, which is polynomial-time equivalent to factoring. Any "
        "corrected variant forcing u = v (mod N) with uv square collapses to "
        "Dixon/QS proper, at which point the tree contributes nothing but a "
        "(possibly boosted-yield, Part B) smooth-integer farm that cannot be "
        "coupled to N without already factoring.")
    res["runtime_s"] = round(time.time() - t0, 1)
    print(f"[done] {res['runtime_s']}s", flush=True)

    with open(RESULT, "w") as f:
        json.dump(clean(res), f, indent=1, default=str)
    print("result ->", RESULT, flush=True)


if __name__ == "__main__":
    main()

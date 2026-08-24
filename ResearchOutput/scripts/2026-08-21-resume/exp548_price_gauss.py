#!/usr/bin/env python3
"""
exp548 PRICE-ENERGY + GAUSS-DIAL-PROOF
======================================

Two parts, write-first:

PART 1 — PRICE TREE ON THE (m,n) PAIR REPRESENTATION
---------------------------------------------------
The Price tree (H.L. Price, "The Pythagorean Tree: A New Species",
arXiv:0809.4324, 2008) is built from Fibonacci boxes [[q,q'],[p,p']] with the
Fibonacci rule p = q+q', p' = p+q.  Reading column 1 bottom-up as the standard
parametrizing pair (m,n) = (p,q), column 1 generates the triple
(a,b,c) = (m^2-n^2, 2mn, m^2+n^2); the hypotenuse is c = m^2+n^2.

DERIVATION OF THE PAIR MAPS (from Price's child box templates):
  parent box [[q,q'],[p,p']], child templates
    K1 = [[2q, q'],[p',  .]]  -> new first column (2q, p') -> pair (p', 2q)
    K2 = [[q',p'],[2p,  .]]  -> new first column (q', 2p) -> pair (2p, q')
    K3 = [[p',q'],[2p,  .]]  -> new first column (p', 2p) -> pair (2p, p')
  In (m,n) = (p,q):
    A: (m,n) -> (m+n, 2n)        det = -2? see below
    B: (m,n) -> (2m, m-n)        det = -2
    C: (m,n) -> (2m, m+n)        det = +2
  A = [[1,1],[0,2]] has det +2.  All |det| = 2 (the "binary-GCD / halving"
  character: B and C children halve their first coordinate on the way down).

Root: box [[1,1],[2,3]] <-> pair (2,1) <-> triple (3,4,5).
Children of (3,4,5): A->(5,12,13), B->(8,15,17), C->(7,24,25), matching the
literature Price matrices (Wikipedia/Price A',B',C' on (a,b,c)).

VALIDATION GATE (before ANY measurement): enumerate ALL primitive triples with
c <= CMAX by brute force over (m,n), then BFS-generate the tree from (2,1).
Every brute-force triple must appear EXACTLY ONCE in the tree.

LETTER CONVENTION (documented): descent from a node toward the root records,
at each step, WHICH forward map's inverse was used: 'A','B','C' (ternary
alphabet, coded 0/1/2).  Strings are stored NODE-FIRST (index 0 = first step
away from the node).  Binary sub-readout: step is a HALVING step iff the
current first coordinate M is even (letters B,C); letter A steps are the
non-halving ones (M odd).  TERMINAL CONDITION: descent stops exactly at the
root pair (2,1) (the (3,4,5) node).

PART 2 — GAUSS-DIAL-PROOF
-------------------------
Show analytically + empirically that pure quadratic Gauss-sum magnitude
families are RESIDUE DIALS: |G(a,b;M)| = |sum_x exp(2*pi*i*(a x^2+b x)/M)|
depends only on (a,b,M); closed forms verified 100% over ALL cells
(a,b) in [0,M)^2 for M in {3,4,5,7,8,9,11,13,16} (+ composite spot-checks);
hence any feature built solely from such magnitudes at fixed small moduli is
a function of N mod lcm(M) — a residue dial already sealed by the standing
no-pinning results.  End-to-end: the |G|-feature vector is proven a pure
function of N mod 720720, and I(features; Y) <= I(N mod 720720; Y) is
verified numerically (equality exactly when Y is measurable w.r.t. the
features — data-processing inequality).

LEDGER (corrections/disclosures):
  1. The prompt's hint "P1=(2c-b, 2a, 2c+b)" is REFUTED programmatically:
     applied to (3,4,5) it yields (6,6,14), which fails a^2+b^2=c^2.
  2. Derivation source: arXiv:0809.4324 (Price 2008) via ar5iv + Wikipedia
     "Formulas for generating Pythagorean triples" (Price section); the pair
     maps were derived here from the box templates and CROSS-CHECKED against
     the literature triple matrices A'B'C'.
  3. MI nuance (corrected framing): I(features;. ) == I(residues;. )
     identically when the label is measurable w.r.t. the features; for
     generic labels the inequality is strict (data processing).  The seal
     claim rests on the inequality direction, verified numerically.
"""

import argparse
import json
import math
import sys
import time
from collections import deque
from math import gcd, isqrt, log2, sqrt

import numpy as np

SEED = 20260823
ROOT = (2, 1)

# ----------------------------------------------------------------------------
# utilities
# ----------------------------------------------------------------------------


def canonical_triple(m, n):
    """Canonical (sorted legs, hypotenuse) representation of pair (m,n)."""
    a = m * m - n * n
    b = 2 * m * n
    c = m * m + n * n
    return (min(a, b), max(a, b), c)


def odd_first(tri):
    """Reorder (legs..., c) so the odd leg comes first (literature order)."""
    lo, hi, c = tri
    return (lo, hi, c) if lo % 2 == 1 else (hi, lo, c)


# ----------------------------------------------------------------------------
# PART 1A: independent brute force enumeration (ground truth)
# ----------------------------------------------------------------------------


def brute_pairs(cmax):
    """All primitive triples c<=cmax via direct (m,n) scan: m>n>=1, gcd=1,
    opposite parity.  Returns dict pair -> c."""
    out = {}
    for m in range(2, isqrt(cmax) + 1):
        for n in range(1, m):
            c = m * m + n * n
            if c > cmax:
                break
            if (m - n) % 2 == 1 and gcd(m, n) == 1:
                out[(m, n)] = c
    return out


# ----------------------------------------------------------------------------
# PART 1A: Price tree construction (pair maps)
# ----------------------------------------------------------------------------


PRICE_MAPS = {
    "A": (lambda m, n: (m + n, 2 * n)),
    "B": (lambda m, n: (2 * m, m - n)),
    "C": (lambda m, n: (2 * m, m + n)),
}
PRICE_DET = {"A": 2, "B": -2, "C": 2}


def build_price_tree(cmax):
    """BFS from root (2,1); every generated pair kept iff c<=cmax.
    Returns (dict pair->depth, duplicate_count)."""
    seen = {ROOT: 0}
    dups = 0
    q = deque([ROOT])
    while q:
        m, n = q.popleft()
        base_c = m * m + n * n
        for L, f in PRICE_MAPS.items():
            cm_, cn_ = f(m, n)
            cc = cm_ * cm_ + cn_ * cn_
            assert cc > base_c, "child hypotenuse must strictly increase"
            if cc <= cmax:
                if (cm_, cn_) in seen:
                    dups += 1
                else:
                    seen[(cm_, cn_)] = seen[(m, n)] + 1
                    q.append((cm_, cn_))
    return seen, dups


# ----------------------------------------------------------------------------
# Price descent (unique inverse; the validation gate proves uniqueness)
# ----------------------------------------------------------------------------


def price_step_down(M, N):
    """One inverse step.  Letter = which forward map's inverse applies."""
    if M % 2 == 1:
        assert N % 2 == 0, f"A-step needs even second coord, got ({M},{N})"
        n = N // 2
        m = M - n
        assert m > n >= 1, f"A-inverse produced invalid parent ({m},{n})"
        return "A", (m, n)
    half = M // 2
    if N < half:
        return "B", (half, half - N)
    if N > half:
        return "C", (half, N - half)
    raise ValueError(f"N == M/2 at ({M},{N}): not a primitive pair")


def price_descend(m, n, max_steps=4096):
    letters = []
    cur = (m, n)
    while cur != ROOT:
        L, cur = price_step_down(*cur)
        letters.append(L)
        if len(letters) > max_steps:
            raise RuntimeError(f"no termination from ({m},{n})")
    return "".join(letters)


def berggren_step_down(M, N):
    if M < 2 * N:
        return "1", (N, 2 * N - M)
    if M > 3 * N:
        return "3", (M - 2 * N, N)
    if M > 2 * N:
        return "2", (N, M - 2 * N)
    raise ValueError(f"Berggren descent undefined at ({M},{N})")


def berggren_descend(m, n, max_steps=2000000):
    # NOTE: Berggren depth is ratio-driven and genuinely unbounded-ish;
    # rare semiprime nodes run into multi-thousand-step corridors
    # (observed dB=4566 and 7230 in this population).
    letters = []
    cur = (m, n)
    while cur != ROOT:
        L, cur = berggren_step_down(*cur)
        letters.append(L)
        if len(letters) > max_steps:
            raise RuntimeError(f"no termination from ({m},{n})")
    return "".join(letters)


# ----------------------------------------------------------------------------
# PART 1A: literature cross-check (triple matrices A'B'C')
# ----------------------------------------------------------------------------


def lit_price_children(tri):
    """Literature Price matrices acting on (a,b,c), a = odd leg first.
    Returns set of canonical children triples."""
    a, b, c = odd_first(tri)
    kids = []
    for mat in (
        ((2, 1, -1), (-2, 2, 2), (-2, 1, 3)),  # A'
        ((2, 1, 1), (2, -2, 2), (2, -1, 3)),  # B'
        ((2, -1, 1), (2, 2, 2), (2, 1, 3)),  # C'
    ):
        na = mat[0][0] * a + mat[0][1] * b + mat[0][2] * c
        nb = mat[1][0] * a + mat[1][1] * b + mat[1][2] * c
        nc = mat[2][0] * a + mat[2][1] * b + mat[2][2] * c
        lo, hi = (na, nb) if abs(na) < abs(nb) else (nb, na)
        kids.append((abs(lo), abs(hi), abs(nc)))
    return set(kids)


def pair_map_children(tri):
    """Children via derived pair maps; input canonical triple from a pair."""
    a, b, c = odd_first(tri)  # a = odd leg = m^2 - n^2
    m2 = (c + a) // 2
    n2 = (c - a) // 2
    m, n = isqrt(m2), isqrt(n2)
    assert m * m == m2 and n * n == n2, "input not a parametrized triple"
    assert m * m - n * n == a and 2 * m * n == b, "leg recovery failed"
    out = set()
    for f in PRICE_MAPS.values():
        M, N = f(m, n)
        ta, tb, tc = M * M - N * N, 2 * M * N, M * M + N * N
        out.add((min(ta, tb), max(ta, tb), tc))
    return out


def hint_check():
    """Refute the prompt hint P1=(2c-b, 2a, 2c+b) programmatically."""
    a, b, c = 3, 4, 5
    na, nb, nc = 2 * c - b, 2 * a, 2 * c + b
    ok = na * na + nb * nb == nc * nc
    return {
        "hint": "P1=(2c-b,2a,2c+b)",
        "root_image": [na, nb, nc],
        "is_pythagorean": bool(ok),
        "verdict": "REFUTED" if not ok else "unexpectedly valid",
    }


# ----------------------------------------------------------------------------
# PART 1B: population, descents, measurements
# ----------------------------------------------------------------------------


def sieve(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, isqrt(n) + 1):
        if s[i]:
            s[i * i :: i] = False
    return np.nonzero(s)[0]


def draw_population(rng, pop):
    allp = sieve(2 ** 21)
    P1 = allp[(allp >= 2 ** 13) & (allp <= 2 ** 17)]
    P2 = allp[(allp >= 2 ** 15) & (allp <= 2 ** 21)]
    ip = rng.choice(P1.size, size=pop, replace=False)
    iq = rng.choice(P2.size, size=pop, replace=False)
    ps = P1[ip].astype(np.int64)
    qs = P2[iq].astype(np.int64)
    n_redraw = 0
    while True:
        bad = ps == qs
        if not bad.any():
            break
        qs[bad] = P2[rng.choice(P2.size, size=int(bad.sum()), replace=False)]
        n_redraw += 1
    swap = ps > qs
    p = np.where(swap, qs, ps)
    q = np.where(swap, ps, qs)
    return p.astype(object), q.astype(object)


def mi_bits(x, y):
    """Plug-in mutual information (bits) between two integer-coded vectors."""
    _, cx = np.unique(x, return_inverse=True)
    _, cy = np.unique(y, return_inverse=True)
    nx, ny = cx.max() + 1, cy.max() + 1
    joint = np.bincount(cx * ny + cy, minlength=nx * ny).astype(float)
    joint = joint.reshape(nx, ny)
    joint = joint / joint.sum()
    px = joint.sum(axis=1, keepdims=True)
    py = joint.sum(axis=0, keepdims=True)
    mask = joint > 0
    return float(np.sum(joint[mask] * np.log2(joint[mask] / (px * py)[mask])))


def perm_mi_z(x, y, perms, rng):
    obs = mi_bits(x, y)
    null = np.empty(perms)
    for i in range(perms):
        null[i] = mi_bits(rng.permutation(x), y)
    mu, sd = null.mean(), null.std(ddof=1)
    z = (obs - mu) / sd if sd > 0 else 0.0
    return {"mi_bits": round(obs, 6), "null_mean": round(mu, 6),
            "null_sd": round(sd, 6), "z": round(z, 3), "perms": perms}


def perm_agreement_z(P, B, valid, perms, rng):
    """Pooled position-aligned agreement rate + re-pairing permutation null."""
    agree = (P == B) & valid
    tot = int(valid.sum())
    obs = float(agree.sum()) / tot
    null = np.empty(perms)
    for i in range(perms):
        pp = rng.permutation(P.shape[0])
        null[i] = float(((P[pp] == B) & valid).sum()) / tot
    mu, sd = null.mean(), null.std(ddof=1)
    z = (obs - mu) / sd if sd > 0 else 0.0
    return obs, null.mean(), null.std(ddof=1), z


def population_letters(seed, pop):
    """Fresh-seed population: returns (N, L0, L1, L2) arrays for
    replication checks."""
    rng = np.random.default_rng(seed)
    p_arr, q_arr = draw_population(rng, pop)
    cmap = {"A": 0, "B": 1, "C": 2}
    Ns, L = [], [[], [], []]
    for p, q in zip(p_arr, q_arr):
        m = (int(p) + int(q)) // 2
        n = (int(q) - int(p)) // 2
        s = price_descend(m, n)
        Ns.append(int(p) * int(q))
        for j in range(3):
            L[j].append(cmap[s[j]])
    return (np.array(Ns, dtype=np.int64),
            np.array(L[0]), np.array(L[1]), np.array(L[2]))


# ----------------------------------------------------------------------------
# PART 2: Gauss sums
# ----------------------------------------------------------------------------


MODS9 = [3, 4, 5, 7, 8, 9, 11, 13, 16]
COMPOSITE_SPOT = [12, 15, 20, 21, 45, 60]


def gauss_numeric(a, b, M):
    x = np.arange(M, dtype=float)
    ph = 2.0 * math.pi * (a * x * x + b * x) / M
    return abs(complex(np.cos(ph).sum(), np.sin(ph).sum()))


def _vp(x, p):
    v = 0
    while x and x % p == 0:
        x //= p
        v += 1
    return v


def _mag_pp_odd(a, b, p, e):
    """|G(a,b;p^e)| closed form, p odd prime, args pre-reduced mod p^e."""
    if e == 0:
        return 1.0
    if a % p != 0:
        return float(p) ** (e / 2.0)  # complete square kills b
    if b % p != 0:
        return 0.0
    return float(p) * _mag_pp_odd(a // p, b // p, p, e - 1)


def _mag_pp_two(a, b, e):
    """|G(a,b;2^e)| closed form."""
    if e == 0:
        return 1.0
    M = 2 ** e
    a %= M
    b %= M
    if a == 0:
        return float(M) if b == 0 else 0.0
    if a % 2 == 1:
        if b % 2 == 1:
            # pairing cancellation holds only for e>=2; at e=1 the summand
            # has period 1 and G(a,b;2)=2
            return 2.0 if e == 1 else 0.0
        return 0.0 if e == 1 else 2.0 ** ((e + 1) / 2.0)
    if b % 2 == 1:
        return 0.0
    return 2.0 * _mag_pp_two(a // 2, b // 2, e - 1)


def factor_pp(M):
    out = []
    m = M
    d = 2
    while d * d <= m:
        if m % d == 0:
            e = 0
            while m % d == 0:
                m //= d
                e += 1
            out.append((d, e))
        d += 1
    if m > 1:
        out.append((m, 1))
    return out


def gauss_mag_closed(a, b, M):
    """Closed-form |G(a,b;M)| for any M (prime-power rules + CRT split)."""
    a %= M
    b %= M
    if a == 0:
        return float(M) if b == 0 else 0.0
    tot = 1.0
    for p, e in factor_pp(M):
        pe = p ** e
        alpha = (a * (M // pe)) % pe
        beta = (b * (M // pe)) % pe
        if p == 2:
            tot *= _mag_pp_two(alpha, beta, e)
        else:
            tot *= _mag_pp_odd(alpha, beta, p, e)
    return tot


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    r = pow(a, (p - 1) // 2, p)
    return 1 if r == 1 else (-1 if r == p - 1 else 0)


def verify_gauss(moduli):
    """Verify closed forms against numeric sums over ALL (a,b,M) cells."""
    total, mism = 0, []
    per_mod = {}
    shift_checks, shift_bad = 0, 0
    for M in moduli:
        mm = 0
        for a in range(M):
            for b in range(M):
                num = gauss_numeric(a, b, M)
                clo = gauss_mag_closed(a, b, M)
                if abs(num - clo) > 5e-9:
                    mism.append({"M": M, "a": a, "b": b,
                                 "num": num, "closed": clo})
                mm += 1
        per_mod[str(M)] = mm
        # named classical check: odd-M shift invariance for gcd(a,M)=1
        if M % 2 == 1:
            for a in range(1, M):
                if gcd(a, M) != 1:
                    continue
                g0 = gauss_mag_closed(a, 0, M)
                for b in range(1, M):
                    if abs(gauss_mag_closed(a, b, M) - g0) > 5e-9:
                        shift_bad += 1
                    shift_checks += 1
    return {"cells_total": total + sum(per_mod.values()),
            "per_modulus_cells": per_mod, "mismatches": mism,
            "n_mismatch": len(mism),
            "shift_invariance_odd_M": {"checks": shift_checks,
                                       "failures": shift_bad}}


def classical_prime_check():
    res = {}
    for p in [3, 5, 7, 11, 13]:
        ok = 0
        for a in range(p):
            pred = float(p) if a == 0 else sqrt(p) * abs(legendre(a, p))
            if abs(gauss_numeric(a, 0, p) - pred) < 5e-9:
                ok += 1
        res[str(p)] = {"cells": p, "matches": ok}
    return res


# ----------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--pop", type=int, default=None)
    ap.add_argument("--perms", type=int, default=None)
    ap.add_argument("--cmax", type=int, default=None)
    args = ap.parse_args()

    t0 = time.time()
    POP = args.pop or (150 if args.smoke else 2000)
    PERMS = args.perms or (40 if args.smoke else 300)
    CMAX = args.cmax or (1500 if args.smoke else 5000)
    MI_SAMPLES = 100 if args.smoke else 500
    DIAL_SAMPLES = 100 if args.smoke else 500

    out = {
        "exp": "548",
        "codename": "PRICE-ENERGY+GAUSS-DIAL-PROOF",
        "smoke": bool(args.smoke),
        "status": "running",
        "config": {
            "seed": SEED, "pop": POP, "perms": PERMS, "cmax_validation": CMAX,
            "p_range": "[2^13, 2^17]", "q_range": "[2^15, 2^21]",
            "mi_samples": MI_SAMPLES, "dial_samples": DIAL_SAMPLES,
            "gauss_moduli": MODS9 + COMPOSITE_SPOT,
        },
        "derivation": {},
        "part1": {},
        "part2": {},
        "ledger": [
            "HINT REFUTED: prompt hint P1=(2c-b,2a,2c+b) sends (3,4,5) to "
            "(6,6,14), not a Pythagorean triple (checked programmatically).",
            "DERIVATION: Price pair maps A/B,C derived from Fibonacci-box "
            "child templates of arXiv:0809.4324; cross-checked against "
            "literature triple matrices on sampled nodes and against an "
            "independent brute-force enumeration (uniqueness+completeness "
            "gate).",
            "CLOSED-FORM CORRECTION: first implementation returned 0 for "
            "|G(a,b;2)| with a,b both odd; pairing-cancellation only holds "
            "for e>=2 — at e=1 G(a,b;2)=2. Fixed; full grid then verifies "
            "100%.",
            "MI NUANCE: I(features;.)==I(residues;.) exactly when the label "
            "is measurable w.r.t. the features; generic labels give the "
            "strict data-processing inequality. Both verified numerically.",
            "EXTREME-dB LEDGER CATCH: initial run aborted on a 4096-step "
            "guard because Berggren descent legitimately takes 4566 and "
            "7230 steps on two population nodes ((583538,455889) and "
            "(505412,404331)) — ratio-driven dB quantitatively contrasts "
            "size-driven dP (<=~40). Guard raised; alignment capped at 64.",
            "WORST-CELL RESOLUTION: primary cell 'N mod 3^1 vs L1' hit "
            "z=4.57 (stable at 4.02 under 5000 perms for THIS draw) but "
            "does NOT replicate on fresh seeds (z = 0.12, -0.17, 2.00); "
            "treated as a seed-specific fluctuation, not 3-adic structure.",
            "dP-LAW DEVIATION: fitted slope of dP on log2(p+q) is "
            "1.21 [CI95 1.12, 1.30], excluding the claimed 1.4; the law "
            "over-predicts depth by ~3.1 steps in this size range while "
            "matching the tight sd (~2.65 vs claimed ~2.4).",
            "CONSTANCY DISCOVERY: on the standard lab range every prime "
            "factor is coprime to lcm 720720, and since |G(a,0;p^e)| "
            "depends only on gcd patterns (never on unit classes), the "
            "|G| feature vector is LITERALLY CONSTANT across all 2000 "
            "semiprimes — zero bits total. Equality case was therefore "
            "re-tested non-degenerately on a mixed small-factor "
            "population.",
        ],
    }

    print(f"[exp548] start  smoke={args.smoke} POP={POP} PERMS={PERMS} "
          f"CMAX={CMAX}")

    # ------------------------------------------------------------------ #
    # DERIVATION RECORD
    # ------------------------------------------------------------------ #
    out["derivation"] = {
        "source": "Price 2008, arXiv:0809.4324 (Fibonacci-box tree)",
        "pair_representation": "(m,n) = first box column read bottom-up; "
                               "triple (m^2-n^2, 2mn, m^2+n^2)",
        "pair_maps": {"A": "(m,n)->(m+n,2n)", "B": "(m,n)->(2m,m-n)",
                      "C": "(m,n)->(2m,m+n)"},
        "determinants": PRICE_DET,
        "root": "(2,1) <-> box [[1,1],[2,3]] <-> (3,4,5)",
        "children_of_root_by_letter": {"A": "(5,12,13)", "B": "(8,15,17)",
                                       "C": "(7,24,25)"},
        "letter_convention": "node-first descent strings; letter = which "
                             "forward map's inverse applied; halving steps = "
                             "{B,C} (first coord even), non-halving = {A}",
        "terminal_condition": "descent stops at root pair (2,1)",
        "hint_refutation": hint_check(),
    }
    print("[derivation] pair maps A/B/C derived; hint refutation recorded")

    # ------------------------------------------------------------------ #
    # PART 1A: VALIDATION GATE
    # ------------------------------------------------------------------ #
    brute = brute_pairs(CMAX)
    tree, dups = build_price_tree(CMAX)
    brute_triples = sorted(canonical_triple(*mn) for mn in brute)
    tree_triples = sorted(canonical_triple(*mn) for mn in tree)
    missing = sorted(set(brute_triples) - set(tree_triples))
    extra = sorted(set(tree_triples) - set(brute_triples))

    # Berggren internal gate: every brute pair descends uniquely to (2,1)
    berg_fail = 0
    for mn in brute:
        try:
            berggren_descend(*mn, max_steps=256)
        except Exception:
            berg_fail += 1

    gate = {
        "cmax": CMAX,
        "brute_count": len(brute),
        "tree_count": len(tree),
        "tree_duplicate_events": dups,
        "missing_from_tree": len(missing),
        "extra_in_tree": len(extra),
        "unique_and_complete": (len(brute) == len(tree) and dups == 0 and
                                not missing and not extra),
        "berggren_descent_failures": berg_fail,
        "sample_tree_nodes": [
            {"pair": list(map(int, mn)), "depth": int(tree[mn]),
             "triple": list(canonical_triple(*mn))}
            for mn in list(tree)[:5]
        ],
    }
    gate["gate_pass"] = bool(gate["unique_and_complete"] and
                             berg_fail == 0)
    out["part1"]["validation_gate"] = gate
    print(f"[gate] brute={len(brute)} tree={len(tree)} dups={dups} "
          f"missing={len(missing)} extra={len(extra)} "
          f"pass={gate['gate_pass']}")

    # literature cross-check on a sample of nodes
    sample_nodes = sorted(tree, key=lambda mn: tree[mn])[:50]
    cross = 0
    for mn in sample_nodes:
        tri = canonical_triple(*mn)
        if lit_price_children(tri) == pair_map_children(tri):
            cross += 1
    out["derivation"]["literature_cross_check"] = {
        "nodes_tested": len(sample_nodes), "agreements": cross,
        "match": cross == len(sample_nodes),
    }

    # HARD GATE: abort measurement if structure invalid
    if not gate["gate_pass"]:
        out["status"] = "aborted_invalid_structure"
        out["ledger"].append("ABORT: validation gate failed; no measurement")
        with open(RESULT_PATH, "w") as fh:
            json.dump(out, fh, indent=1)
        print("[gate] FAILED -> abort")
        return

    if cross != len(sample_nodes):
        out["status"] = "aborted_crosscheck"
        out["ledger"].append("ABORT: literature cross-check failed")
        with open(RESULT_PATH, "w") as fh:
            json.dump(out, fh, indent=1)
        print("[cross-check] FAILED -> abort")
        return
    print(f"[cross-check] pair maps == literature matrices on "
          f"{cross}/{len(sample_nodes)} sampled nodes")

    # ------------------------------------------------------------------ #
    # PART 1B: population + descents
    # ------------------------------------------------------------------ #
    rng = np.random.default_rng(SEED)
    p_arr, q_arr = draw_population(rng, POP)
    rows = []
    emb_fail = term_fail = 0
    min_dp = 10 ** 9
    for p, q in zip(p_arr, q_arr):
        N = p * q
        m = (p + q) // 2
        n = (q - p) // 2
        ok_emb = (m * m - n * n == N) and gcd(m, n) == 1 and \
                 (m - n) % 2 == 1
        if not ok_emb:
            emb_fail += 1
            continue
        try:
            sp = price_descend(int(m), int(n))
            sb = berggren_descend(int(m), int(n))
        except Exception:
            term_fail += 1
            continue
        rows.append({"p": int(p), "q": int(q), "N": int(N),
                     "m": int(m), "n": int(n),
                     "dp_str": sp, "db_str": sb,
                     "dp": len(sp), "db": len(sb)})
        min_dp = min(min_dp, len(sp))

    pop_report = {
        "requested": POP, "embedded": len(rows),
        "embedding_failures": emb_fail,
        "descent_termination_failures": term_fail,
        "price_termination_rate": len(rows) / (POP - emb_fail) if
        (POP - emb_fail) else 0.0,
        "min_dp_observed": min_dp,
    }
    out["part1"]["population"] = pop_report
    print(f"[population] embedded={len(rows)}/{POP} "
          f"emb_fail={emb_fail} term_fail={term_fail} min_dP={min_dp}")
    assert emb_fail == 0, "embedding must be perfect"
    assert term_fail == 0, "termination must be 100%"
    assert min_dp >= 5, "population too shallow for positional analyses"

    dp = np.array([r["dp"] for r in rows])
    db = np.array([r["db"] for r in rows])
    lpq = np.array([log2(r["p"] + r["q"]) for r in rows])
    N_arr = np.array([r["N"] for r in rows], dtype=object)

    # ------------------------------------------------------------------ #
    # PART 1 (a): dP distribution + law check
    # ------------------------------------------------------------------ #
    slope, intercept = np.polyfit(lpq, dp.astype(float), 1)
    pred_fit = intercept + slope * lpq
    ss_res = float(((dp - pred_fit) ** 2).sum())
    ss_tot = float(((dp - dp.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot
    se_slope = math.sqrt(ss_res / (len(dp) - 2) /
                         float(((lpq - lpq.mean()) ** 2).sum()))
    pred_fixed = 1.4 * lpq
    rmse_fixed = float(math.sqrt(((dp - pred_fixed) ** 2).mean()))
    bias_fixed = float((dp - pred_fixed).mean())
    dp_law = {
        "dp_mean": round(float(dp.mean()), 4),
        "dp_sd": round(float(dp.std(ddof=1)), 4),
        "dp_range": [int(dp.min()), int(dp.max())],
        "fit_slope": round(float(slope), 5),
        "fit_slope_ci95": [round(float(slope - 1.96 * se_slope), 5),
                           round(float(slope + 1.96 * se_slope), 5)],
        "fit_intercept": round(float(intercept), 4),
        "fit_r2": round(r2, 5),
        "law_1_4_rmse": round(rmse_fixed, 4),
        "law_1_4_mean_signed_dev": round(bias_fixed, 4),
        "slope_1_4_within_ci95": bool(slope - 1.96 * se_slope <= 1.4 <=
                                      slope + 1.96 * se_slope),
        "db_mean": round(float(db.mean()), 4),
        "db_sd": round(float(db.std(ddof=1)), 4),
        "db_median": round(float(np.median(db)), 4),
        "db_range": [int(db.min()), int(db.max())],
    }
    out["part1"]["dp_law"] = dp_law

    # secondary fits: what DOES dP track?
    c_node = np.array([r["m"] ** 2 + r["n"] ** 2 for r in rows], float)
    m_n = np.array([r["m"] + r["n"] for r in rows], float)
    bigN = np.array([r["N"] for r in rows], float)
    secondary = {}
    for nm, xv in [("log2_cnode", np.log2(c_node)),
                   ("log2_m_plus_n", np.log2(m_n)),
                   ("log2_N", np.log2(bigN))]:
        sl, ic = np.polyfit(xv, dp.astype(float), 1)
        pr = ic + sl * xv
        rr = 1 - float(((dp - pr) ** 2).sum()) / ss_tot
        secondary[nm] = {"slope": round(float(sl), 5), "r2": round(rr, 5)}
    out["part1"]["dp_secondary_fits"] = secondary
    print(f"[dp] mean={dp_law['dp_mean']} sd={dp_law['dp_sd']} "
          f"range={dp_law['dp_range']} slope={dp_law['fit_slope']} "
          f"CI95={dp_law['fit_slope_ci95']} R2={dp_law['fit_r2']} "
          f"fixed1.4 RMSE={dp_law['law_1_4_rmse']} "
          f"| secondary {secondary}")

    # ------------------------------------------------------------------ #
    # PART 1 (b): Price <-> Berggren letter agreement
    # ------------------------------------------------------------------ #
    LMAX = max(dp.max(), db.max())
    Ppad = -np.ones((len(rows), LMAX), dtype=np.int16)
    Bpad = -np.ones((len(rows), LMAX), dtype=np.int16)
    cmap = {"A": 0, "B": 1, "C": 2}
    bmap = {"1": 0, "2": 1, "3": 2}
    for i, r in enumerate(rows):
        for j, ch in enumerate(r["dp_str"]):
            Ppad[i, j] = cmap[ch]
        for j, ch in enumerate(r["db_str"]):
            Bpad[i, j] = bmap[ch]
    lens_min = np.minimum(
        (Ppad >= 0).sum(axis=1), (Bpad >= 0).sum(axis=1))
    ALIGN_CAP = 64
    lens_min = np.minimum(lens_min, ALIGN_CAP)
    valid = np.arange(LMAX)[None, :] < lens_min[:, None]
    obs_rate, null_mu, null_sd, ag_z = perm_agreement_z(
        Ppad, Bpad, valid, PERMS, rng)
    margP = np.array([(Ppad[:, j][valid[:, j]] == c).sum()
                      for j in range(LMAX) for c in (0, 1, 2)
                      if valid[:, j].any()])
    indep_baseline = None
    pos_rows = []
    for j in range(min(8, LMAX)):
        pv = Ppad[valid[:, j], j]
        bv = Bpad[valid[:, j], j]
        if pv.size == 0:
            continue
        fp = np.array([(pv == c).mean() for c in range(3)])
        fb = np.array([(bv == c).mean() for c in range(3)])
        e0 = float((fp * fb).sum())
        acc = float((pv == bv).mean())
        pos_rows.append({"pos": j, "n": int(pv.size), "agree": round(acc, 4),
                         "chance_e0": round(e0, 4)})
    price_berggren = {
        "alphabet_note": "Price letters {A,B,C}->0,1,2; Berggren letters "
                         "{1,2,3}->0,1,2; aligned from node; aligned length "
                         "capped at 64 (max dP in population is below this; "
                         "two rare nodes have dB 4566/7230)",
        "pooled_aligned_agreement": round(obs_rate, 5),
        "independence_chance_mean": round(null_mu, 5),
        "perm_null_sd": round(null_sd, 5),
        "z_vs_repairing_null": round(ag_z, 3),
        "per_position": pos_rows,
        "letter_marginals_price_pos0": {
            str(c): round(float((Ppad[valid[:, 0], 0] == c).mean()), 4)
            for c in range(3)},
        "letter_marginals_berggren_pos0": {
            str(c): round(float((Bpad[valid[:, 0], 0] == c).mean()), 4)
            for c in range(3)},
    }
    out["part1"]["price_berggren"] = price_berggren
    print(f"[P-B] agreement={obs_rate:.4f} chance~{null_mu:.4f} "
          f"z={ag_z:.2f}")

    # ------------------------------------------------------------------ #
    # PART 1 (c): residue dial test (N mod 3^k vs Price letters)
    # ------------------------------------------------------------------ #
    letters0 = Ppad[:, 0].copy()
    letters1 = Ppad[:, 1].copy()
    letters2 = Ppad[:, 2].copy()
    targets = {"L0": letters0, "L1": letters1, "L2": letters2}
    prim_rng = np.random.default_rng(SEED + 1)
    cells_primary = []
    worst = (0.0, None)
    for k in range(1, 7):
        X = (N_arr % (3 ** k)).astype(np.int64)
        for tn, tv in targets.items():
            r = perm_mi_z(X, tv, PERMS, prim_rng)
            r.update({"cell": f"N mod 3^{k} vs {tn}", "family": "primary"})
            cells_primary.append(r)
            if abs(r["z"]) > abs(worst[0]):
                worst = (r["z"], r["cell"])
    ctrl_rng = np.random.default_rng(SEED + 2)
    cells_control = []
    for mname, MX in [("N mod 4", N_arr % 4), ("N mod 8", N_arr % 8)]:
        for tn, tv in targets.items():
            if mname == "N mod 8" and tn != "L0":
                continue
            r = perm_mi_z(MX.astype(np.int64), tv, PERMS, ctrl_rng)
            r.update({"cell": f"{mname} vs {tn}", "family": "control"})
            cells_control.append(r)
    expl_rng = np.random.default_rng(SEED + 3)
    cells_exploratory = []
    for kk in range(1, 5):
        X = (N_arr % (2 ** kk)).astype(np.int64)
        for tn, tv in targets.items():
            r = perm_mi_z(X, tv, PERMS, expl_rng)
            r.update({"cell": f"N mod 2^{kk} vs {tn}",
                      "family": "exploratory"})
            cells_exploratory.append(r)

    def fam_stats(cells):
        zs = [abs(c["z"]) for c in cells]
        return {"n_cells": len(cells), "max_abs_z": round(max(zs), 3),
                "n_abs_z_gt3": int(sum(1 for z in zs if z > 3)),
                "n_abs_z_gt4": int(sum(1 for z in zs if z > 4))}

    # replication check for any primary cell breaching |z|=3: fresh seeds.
    # A breach that fails to replicate is a draw-specific fluctuation.
    repl = []
    if abs(worst[0]) > 3:
        import re
        mm = re.match(r"N mod 3\^(\d+) vs (L\d)", worst[1])
        kk, tt = int(mm.group(1)), mm.group(2)
        for si, sd_ in enumerate([SEED + 1000, SEED + 2000, SEED + 3000]):
            Nr, L0r, L1r, L2r = population_letters(sd_, POP)
            tv = {"L0": L0r, "L1": L1r, "L2": L2r}[tt]
            rz = perm_mi_z(Nr % (3 ** kk), tv, PERMS,
                           np.random.default_rng(SEED + 41 + si))
            repl.append({"seed": sd_, "cell": worst[1],
                         "z": rz["z"]})

    out["part1"]["residue_dial"] = {
        "method": "plug-in MI (bits) + row-shuffle permutation null; "
                  "z = (obs-null_mean)/null_sd",
        "primary_cells": cells_primary,
        "primary_family_stats": fam_stats(cells_primary),
        "worst_primary_cell": {"z": worst[0], "cell": worst[1]},
        "worst_cell_fresh_seed_replication": repl,
        "positive_controls": cells_control,
        "exploratory_2adic_cells": cells_exploratory,
        "exploratory_family_stats": fam_stats(cells_exploratory),
    }
    print(f"[dial] primary worst |z|={abs(worst[0]):.2f} ({worst[1]}); "
          f"controls max|z|="
          f"{fam_stats(cells_control)['max_abs_z']}; replication="
          f"{[r['z'] for r in repl] if repl else 'not needed'}")

    # ------------------------------------------------------------------ #
    # PART 2: Gauss verification
    # ------------------------------------------------------------------ #
    gv = verify_gauss(MODS9 + COMPOSITE_SPOT)
    out["part2"]["gauss_verification"] = gv
    out["part2"]["classical_odd_prime_magnitude"] = classical_prime_check()
    print(f"[gauss] cells={gv['cells_total']} "
          f"mismatches={gv['n_mismatch']} "
          f"shift_failures={gv['shift_invariance_odd_M']['failures']}")

    # ------------------------------------------------------------------ #
    # PART 2: end-to-end dial demonstration
    # ------------------------------------------------------------------ #
    L = 1
    for M in MODS9:
        L = L * M // gcd(L, M)
    feats = lambda NN: tuple(round(gauss_mag_closed(NN % M, 0, M), 9)
                             for M in MODS9)

    def run_demo(Ns_, seed_, labels_):
        """Dial determinism + MI table for an explicit list of N values."""
        rng_ = np.random.default_rng(seed_)
        ks_ = rng_.integers(1, 10 ** 9, size=len(Ns_))
        Fs_, Rs_ = [], []
        d_ok = r_ok = 0
        for i, N_ in enumerate(Ns_):
            N_ = int(N_)
            R_ = N_ % L
            f1 = feats(N_)
            d_ok += int(f1 == feats(N_ + int(ks_[i]) * L))
            r_ok += int(f1 == feats(R_))
            Fs_.append("|".join(str(round(v, 6)) for v in f1))
            Rs_.append(hash(R_))
        Fc_ = np.unique(np.array(Fs_), return_inverse=True)[1].astype(np.int64)
        Rc_ = np.array(Rs_)

        def ent(v):
            _, c = np.unique(v, return_counts=True)
            pr = c / c.sum()
            return float(-(pr * np.log2(pr)).sum())

        lab_out = {}
        dpi_ok = True
        for nm, arr in labels_.items():
            ii, rr = mi_bits(Fc_, arr), mi_bits(Rc_, arr)
            dpi_ok &= bool(ii <= rr + 1e-9)
            lab_out[nm] = {"H": round(ent(arr), 6),
                           "I_features": round(ii, 6),
                           "I_residues": round(rr, 6)}
        return {"n_samples": len(Ns_),
                "n_distinct_feature_cells": int(len(np.unique(Fs_))),
                "dial_equal": int(d_ok), "repr_equal": int(r_ok),
                "labels": lab_out, "dpi_holds_all_labels": bool(dpi_ok)}

    # (a) standard-range semiprimes (same spec as Part 1 population)
    dial_rng = np.random.default_rng(SEED + 4)
    ip2 = dial_rng.choice(len(p_arr), size=min(DIAL_SAMPLES, len(p_arr)),
                          replace=False)
    ps_std = [int(p_arr[i]) for i in ip2]
    qs_std = [int(q_arr[i]) for i in ip2]
    Ns_std = [p_ * q_ for p_, q_ in zip(ps_std, qs_std)]
    labA = {
        "smaller_prime_mod_3": np.array([p_ % 3 for p_ in ps_std]),
        "factor_congruence_agreement_mod4":
            np.array([1 if p_ % 4 == q_ % 4 else 0
                      for p_, q_ in zip(ps_std, qs_std)]),
        "three_divides_N": np.array([1 if n_ % 3 == 0 else 0
                                     for n_ in Ns_std]),
    }
    demo_std = run_demo(Ns_std, SEED + 40, labA)
    demo_std["population_note"] = (
        "standard lab range p in [2^13,2^17], q in [2^15,2^21]: every "
        "factor is coprime to lcm 720720, hence |G| magnitudes see only "
        "gcd patterns -> the feature vector is CONSTANT and carries "
        "exactly zero bits about every label")
    # (b) general odd integers: gcd patterns vary, so the feature vector
    # varies and the equality case is tested non-degenerately
    brng = np.random.default_rng(SEED + 5)
    Ns_b = (2 * brng.integers(50000, 500000, size=DIAL_SAMPLES) + 1)
    labB = {
        "three_divides_N": np.array([1 if int(n_) % 3 == 0 else 0
                                     for n_ in Ns_b]),
        "congruent_1_mod_4": np.array([1 if int(n_) % 4 == 1 else 0
                                       for n_ in Ns_b]),
    }
    demo_mix = run_demo(Ns_b, SEED + 50, labB)
    demo_mix["population_note"] = (
        "general odd integers in [1e5,1e6]: gcd patterns vary -> feature "
        "vector varies; 'three_divides_N' is BOTH genuine factor info AND "
        "measurable w.r.t. the features (the M=3 feature detects it), so "
        "it doubles as the non-degenerate equality case")
    eqB = demo_mix["labels"]["three_divides_N"]
    equality_nondeg = bool(abs(eqB["I_features"] - eqB["I_residues"]) < 1e-9
                           and abs(eqB["I_features"] - eqB["H"]) < 1e-6
                           and eqB["H"] > 0.05)

    e2e = {
        "lcm_moduli": L,
        "standard_range_demo": demo_std,
        "odd_integer_demo": demo_mix,
        "equality_case_label": "Y* = [3 divides N] (function of the M=3 "
                               "feature); exact-equality claim tested on the "
                               "odd-integer population",
        "dial_invariance_all_equal":
            bool(demo_std["dial_equal"] == demo_std["n_samples"] and
                 demo_mix["dial_equal"] == demo_mix["n_samples"]),
        "pure_function_of_residue_all_equal":
            bool(demo_std["repr_equal"] == demo_std["n_samples"] and
                 demo_mix["repr_equal"] == demo_mix["n_samples"]),
        "dpi_holds_all_labels_both_pops":
            bool(demo_std["dpi_holds_all_labels"] and
                 demo_mix["dpi_holds_all_labels"]),
        "equality_exact_nondegenerate": equality_nondeg,
    }
    out["part2"]["end_to_end"] = e2e
    print(f"[e2e] std: cells={demo_std['n_distinct_feature_cells']} "
          f"dial {demo_std['dial_equal']}/{demo_std['n_samples']} | "
          f"odd-int: cells={demo_mix['n_distinct_feature_cells']} "
          f"dial {demo_mix['dial_equal']}/{demo_mix['n_samples']} "
          f"I(F;3|N)={eqB['I_features']} = I(R;3|N) = H = {eqB['H']} "
          f"exact={equality_nondeg}")

    # ------------------------------------------------------------------ #
    # VERDICTS
    # ------------------------------------------------------------------ #
    pd = out["part1"]["residue_dial"]["primary_family_stats"]
    pc = out["part1"]["residue_dial"]["positive_controls"]
    ctrl_max = max(abs(c["z"]) for c in pc)
    repl = out["part1"]["residue_dial"]["worst_cell_fresh_seed_replication"]
    worst_replicates = bool(repl) and all(abs(r["z"]) >= 3 for r in repl)
    ex = out["part1"]["residue_dial"]["exploratory_2adic_cells"]
    ex01 = max(abs(c["z"]) for c in ex if c["cell"].endswith(("L0", "L1"))
               and "2^1" not in c["cell"])
    out["verdicts"] = {
        "structure_gate_pass": gate["gate_pass"],
        "uniqueness_completeness": gate["unique_and_complete"],
        "termination_100pct": term_fail == 0,
        "dp_law_consistent": dp_law["slope_1_4_within_ci95"],
        "price_berggren_beyond_chance":
            bool(ag_z > 3),
        "residue_dial_null_3adics":
            bool(pd["n_abs_z_gt3"] == 0 or
                 (bool(repl) and not worst_replicates)),
        "worst_primary_cell_breach_replicates": worst_replicates,
        "price_letters_2adic_positions01": bool(ex01 > 100),
        "control_detects_signal": bool(ctrl_max > 3),
        "gauss_closed_forms_verified":
            bool(gv["n_mismatch"] == 0 and
                 gv["shift_invariance_odd_M"]["failures"] == 0),
        "gauss_features_are_residue_dials":
            bool(gv["n_mismatch"] == 0 and
                 e2e["dial_invariance_all_equal"] and
                 e2e["pure_function_of_residue_all_equal"]),
        "features_constant_on_standard_range":
            bool(demo_std["n_distinct_feature_cells"] == 1),
        "conclusion_part2":
            "Any factoring feature built solely from quadratic Gauss-sum "
            "magnitudes |G| at fixed small moduli is a pure function of "
            "N mod lcm({3,4,5,7,8,9,11,13,16}) = 720720 (verified: dial "
            "invariance and representative lookup 500/500 on two "
            "populations), hence a residue dial already sealed by the "
            "standing no-pinning results. Sharpenings: (i) |G| magnitudes "
            "are blind even to the quadratic character — they depend only "
            "on gcd patterns with the moduli, so on the standard lab range "
            "the whole feature vector is CONSTANT and carries exactly zero "
            "bits about anything, including the factor-congruence info "
            "[p==q mod 4] that raw residues fully determine; (ii) the "
            "data-processing equality I(features;.) == I(residues;. ) holds "
            "exactly when the label is measurable w.r.t. the features "
            "(verified non-degenerately on a mixed population).",
        "dial_loses_Nmod4_info": {
            "note": "[p==q mod 4] is determined by N mod 4; |G| magnitudes "
                    "are blind to quadratic character",
            "I_residues_agree4_bits":
                demo_std["labels"]["factor_congruence_agreement_mod4"]
                ["I_residues"],
            "I_features_agree4_bits":
                demo_std["labels"]["factor_congruence_agreement_mod4"]
                ["I_features"],
            "H_bits":
                demo_std["labels"]["factor_congruence_agreement_mod4"]["H"]},
    }
    out["status"] = "04_final"
    out["wall_s"] = round(time.time() - t0, 1)

    with open(RESULT_PATH, "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print(f"[done] wall={out['wall_s']}s -> {RESULT_PATH}")


RESULT_PATH = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-21-resume/exp548_result.json"


if __name__ == "__main__":
    main()

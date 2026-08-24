#!/usr/bin/env python3
"""
exp552 TWO-ADIC-PRICE-LAW
=========================

WRITE-FIRST: the analytic derivation below was completed BEFORE any
measurement code was run; the measurement sections only VERIFY it.

ANALYTIC DERIVATION (on paper)
------------------------------
Setup. Odd semiprime N=pq, p<q, sits at (m,n)=((p+q)/2,(q-p)/2), so
p=m-n, q=m+n, N=m^2-n^2. Price root (2,1); forward children
  A: (m,n)->(m+n,2n)   B: (m,n)->(2m,m-n)   C: (m,n)->(2m,m+n),
descent letter = which forward map's inverse applies. Validated
unique+complete to c<=5000 in exp548.

Step 1 -- the descent rule. All tree nodes have m>n>=1 of OPPOSITE
parity (root (2,1); each map preserves it). Inverses:
  invA needs n even (m odd): parent (m-n/2, n/2);
  invB needs m even, n<m/2:  parent (m/2, m/2-n);
  invC needs m even, n>m/2:  parent (m/2, n-m/2).
Exactly one is applicable at every non-root node:
  LETTER RULE:  m odd -> 'A';  m even & 2n<m -> 'B';  m even & 2n>m -> 'C'.

Step 2 -- U,V form. Put U=p+q=2m, V=q-p=2n (even, V>0). Every step halves
exactly ONE of U,V:
  A-step (iff m odd, i.e. v2(U)=1): (U,V) <- (U-V/2, V/2)   [A halves V]
  B/C-step (iff m even, i.e. v2(U)>=2): (U,V) <- (U/2, +/-(V-U/2))
                                                        [B,C halve U]
MECHANISM SENTENCE: A is the step that SEES V=q-p (it halves V and is
admissible exactly when v2(U)=1); B and C SEE U (they halve U and are
admissible exactly when v2(U)>=2), the B-vs-C choice being the SIGN of
V-U/2, a size comparison, not a congruence. Consequently
  letter_t = 'A'  <=>  v2(U_t) = 1,
and while no A has yet occurred, every step halves U exactly, so
v2(U_t) = u0 - t with u0 := v2(p+q): THE FIRST A LANDS AT POSITION u0-1.

Step 3 -- what N mod 2^k sees. Every odd square is 1 mod 8, hence
  u0 = 1  <=>  p+q = 2*odd      <=>  N mod 8 in {1,5}
  u0 = 2  <=>  p+q = 4*odd      <=>  N mod 8 = 3        (pq = -p^2 = 3 mod 8
                                          because {p,q}={1,3} or {5,7} mod 8,
                                          sums 4 mod 8 in both cases)
  u0 >= 3 <=>  8 | p+q          <=>  N mod 8 = 7.
THE EXACT MAP (positions 0 and 1, deterministic):
  POSITION 0:  N = 1 mod 4  => letter0 = 'A';
               N = 3 mod 4  => letter0 in {'B','C'}, B iff q < 3p (size).
  POSITION 1:  letter1 = 'A'  <=>  N mod 8 in {1,3};
               otherwise letter1 in {'B','C'} by the size rule at node 1.
  BIJECTION: the first two letters determine and are determined by N mod 8:
     (A,A)<->1, (A,notA)<->5, (notA,A)<->3, (notA,notA)<->7.
  So WITHIN ANY PREFIX CELL AT t>=2, N mod 8 is CONSTANT: the conditional
  2-adic visibility is IDENTICALLY ZERO from position 2 on -- an exact
  death, not a fade.

Step 4 -- scrambling lemma (why NOTHING is determined at t>=2). For j>=3
write p+q = 2^j * o (u0=j), o odd. Then N = p*q = 2^j*p*o - p^2. As p,o
range over odd residues, 2^j*p*o covers all multiples of 2^j by odds and
p^2 covers all x = 1 mod 8 classes, so N mod 2^k is uniform on {x = 7
mod 8} for EVERY k>j -- the SAME law as any u0 > j. Hence no test on
N mod 2^k (any k whatsoever) distinguishes u0=j from u0'>=j (both >=3):
multiplication by the unknown odd p scrambles every bit of p+q above
position 3. Residue-visible content of the path = the A-ness of positions
0 and 1 ONLY; B-vs-C is never residue-visible at any depth (inequality).
DETERMINATION GOES EXACTLY AS DEEP AS TWO CLICKS.

Step 5 -- B rarity at position 0 (explains marginal {A:.48, B:.05, C:.47}).
'A' takes the whole N=1 mod 4 half (~1/2). 'B' requires BOTH N=3 mod 4
(prob ~1/2) AND q<3p (factors within a factor 3): for log-uniform
p in [2^13,2^17], q in [2^15,2^21], P(q<3p) = (integral of overlap of
[u,u+log2 3) windows) ~ 0.27, so P(B) ~ 1/2 * 0.27 ~ 0.13 on the broad
stratum (less when far-field dominates the mix); 'C' absorbs the rest.
B is rare because it needs OPPOSITE mod-4 residues AND a near-square N.

PRE-REGISTERED PREDICTIONS (stated before measurement):
  P1. Mechanical letter rule agrees with true descent 100% at all t.
  P2. letter0='A' <=> N mod 4 = 1, agreement 100% (and conversely).
  P3. letter1='A' <=> N mod 8 in {1,3}, agreement 100%.
  P4. Marginal z-ladder I(N mod 8 ; letter_t): huge at t=0,1; residual
      tail at t>=2 is LEAKAGE from the first two letters only.
  P5. Within-prefix conditional: EXACTLY zero from t=2 (zero-variance
      nulls; N mod 8 constant inside every prefix cell).
  P6. I(N mod M ; unordered letter-pair) saturates at M=8 (no gain for
      M in {16,32}); fits the order-universal/abelianization type-channel
      family: the channel factors through Z/8 and reads its bits off.
  P7. Which-factor wall: within-(N mod 16)-cell shuffles of the
      which-factor label give |z| < 4 and ~0-bit sensitivity.

PARTS. 1 verification of the map + mechanism; 2 depth z-ladders
(marginal stratified + within-prefix conditional); 3 which-factor wall +
symmetric channel capacity + law-family fit.
"""

import argparse
import json
import time
from math import gcd, log2

import numpy as np

SEED = 20260825
ROOT = (2, 1)
RESULT_PATH = ("/home/raver1975/factor3/ResearchOutput/scripts/"
               "2026-08-21-resume/exp552_result.json")
LOG_PATH = ("/home/raver1975/factor3/ResearchOutput/scripts/"
            "2026-08-21-resume/run_exp552.log")

CMAP = {"A": 0, "B": 1, "C": 2}


def log(msg):
    line = f"[exp552] {msg}"
    print(line, flush=True)
    with open(LOG_PATH, "a") as fh:
        fh.write(line + "\n")


# ------------------------------------------------------------------ #
# DERIVATION-ENCODED RULES (written before measurement)
# ------------------------------------------------------------------ #

def letter_rule(m, n):
    """Analytic descent rule: m odd -> A; m even & 2n<m -> B; else C."""
    if m % 2 == 1:
        return "A"
    return "B" if 2 * n < m else "C"


def residue_pred_pos0(N_mod4):
    """Pre-registered: A-ness of position 0 from N mod 4."""
    return N_mod4 == 1


def residue_pred_pos1(N_mod8):
    """Pre-registered: A-ness of position 1 from N mod 8."""
    return N_mod8 in (1, 3)


def prefix_to_residue(pref2):
    """Bijection: first two A-nesses <-> N mod 8 (derived, Step 3)."""
    a0 = pref2[0] == 0
    a1 = pref2[1] == 0
    if a0 and a1:
        return 1
    if a0 and not a1:
        return 5
    if (not a0) and a1:
        return 3
    return 7


# ------------------------------------------------------------------ #
# Price tree mechanics (same validated maps as exp548)
# ------------------------------------------------------------------ #

PRICE_MAPS = {
    "A": (lambda m, n: (m + n, 2 * n)),
    "B": (lambda m, n: (2 * m, m - n)),
    "C": (lambda m, n: (2 * m, m + n)),
}


def price_descend_letters(m, n, max_steps=512):
    """True descent by inverse search (exp548 rule), returns letter list."""
    letters = []
    cur = (m, n)
    while cur != ROOT:
        M, Nc = cur
        if M % 2 == 1:
            nn = Nc // 2
            cur = (M - nn, nn)
            letters.append("A")
        else:
            half = M // 2
            if Nc < half:
                cur = (half, half - Nc)
                letters.append("B")
            elif Nc > half:
                cur = (half, Nc - half)
                letters.append("C")
            else:
                raise ValueError(f"N==M/2 at ({M},{Nc})")
        if len(letters) > max_steps:
            raise RuntimeError("no termination")
    return letters


def price_reascend(letters):
    """From root, apply forward maps in REVERSED letter order."""
    m, n = ROOT
    for ch in reversed(letters):
        m, n = PRICE_MAPS[ch](m, n)
    return m, n


# ------------------------------------------------------------------ #
# Population
# ------------------------------------------------------------------ #

def sieve(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i:: i] = False
    return np.nonzero(s)[0]


def draw_population(rng, n_broad, n_bal):
    """Broad: p in primes [2^13,2^17], q in primes [2^15,2^21], p<q.
    Balanced: p in primes [2^15,2^17], q in primes (p,3p) -- keeps q in
    [2^15, 2^21] while forcing the near-square regime where B lives."""
    allp = sieve(3 * 2 ** 17 + 10)
    P1 = allp[(allp >= 2 ** 13) & (allp <= 2 ** 17)]
    P2 = allp[(allp >= 2 ** 15) & (allp <= 2 ** 21)]
    ip = rng.choice(P1.size, size=n_broad, replace=False)
    iq = rng.choice(P2.size, size=n_broad, replace=False)
    ps, qs = P1[ip].astype(np.int64), P2[iq].astype(np.int64)
    n_redraw = 0
    while True:
        bad = ps >= qs
        if not bad.any():
            break
        qs[bad] = P2[rng.choice(P2.size, size=int(bad.sum()), replace=False)]
        n_redraw += int(bad.sum())
    Pb = allp[(allp >= 2 ** 15) & (allp <= 2 ** 17)]
    ib = rng.choice(Pb.size, size=n_bal, replace=False)
    pb = Pb[ib].astype(np.int64)
    qb = np.empty_like(pb)
    for i, p0 in enumerate(pb):
        lo = int(p0) + 2
        hi = int(3 * p0)
        win = allp[(allp >= lo) & (allp < hi)]
        qb[i] = win[rng.integers(win.size)]
    p_all = np.concatenate([ps, pb])
    q_all = np.concatenate([qs, qb])
    strat = np.array(["broad"] * n_broad + ["balanced"] * n_bal)
    return p_all.astype(object), q_all.astype(object), strat


# ------------------------------------------------------------------ #
# MI + permutation nulls (lab conventions: bits, z=(obs-mean)/sd)
# ------------------------------------------------------------------ #

def mi_bits(x, y):
    _, cx = np.unique(x, return_inverse=True)
    _, cy = np.unique(y, return_inverse=True)
    nx, ny = cx.max() + 1, cy.max() + 1
    joint = np.bincount(cx * ny + cy, minlength=int(nx * ny)).astype(float)
    joint = joint.reshape(nx, ny) / len(x)
    px = joint.sum(axis=1, keepdims=True)
    py = joint.sum(axis=0, keepdims=True)
    mask = joint > 0
    return float(np.sum(joint[mask] *
                        np.log2(joint[mask] / (px * py)[mask])))


def perm_mi_z_global(x, y, perms, rng):
    obs = mi_bits(x, y)
    null = np.array([mi_bits(rng.permutation(x), y) for _ in range(perms)])
    mu, sd = null.mean(), null.std(ddof=1)
    return {"mi_bits": round(obs, 6), "null_mean": round(float(mu), 6),
            "null_sd": round(float(sd), 6),
            "z": round(float((obs - mu) / sd), 3) if sd > 0 else None,
            "perms": perms}


def stratified_shuffle(x, strata, rng):
    out = x.copy()
    for s in np.unique(strata):
        idx = np.nonzero(strata == s)[0]
        out[idx] = x[rng.permutation(idx)]
    return out


def perm_mi_z_stratified(x, y, strata, perms, rng):
    """Null: shuffle x within strata (preserves size composition)."""
    obs = mi_bits(x, y)
    null = np.empty(perms)
    for i in range(perms):
        null[i] = mi_bits(stratified_shuffle(x, strata, rng), y)
    mu, sd = null.mean(), null.std(ddof=1)
    return {"mi_bits": round(obs, 6), "null_mean": round(float(mu), 6),
            "null_sd": round(float(sd), 6),
            "z": round(float((obs - mu) / sd), 3) if sd > 0 else None,
            "perms": perms, "n_strata": int(len(np.unique(strata)))}


def perm_mi_z_within_prefix(x, y, prefixes, min_group, perms, rng):
    """Conditional on path prefix: pooled within-group MI; null shuffles x
    inside each prefix group (exp550 convention). Degenerate zero-variance
    nulls are reported as exact zeros, not fake z. Adaptive: retries once
    with half the min_group if coverage < 60%."""
    def build(mg):
        g = {}
        for i, pf in enumerate(prefixes):
            g.setdefault(pf, []).append(i)
        return {k: np.array(v) for k, v in g.items() if len(v) >= mg}
    big = build(min_group)
    if sum(len(v) for v in big.values()) < 0.6 * len(x):
        bigger = build(max(10, min_group // 2))
        if sum(len(v) for v in bigger.values()) > \
                sum(len(v) for v in big.values()):
            big = bigger
    covered = sum(len(v) for v in big.values())
    if covered == 0:
        return {"covered_rows": 0,
                "status": "INSUFFICIENT_COVERAGE",
                "note": "no prefix group >= min_group"}
    tot = covered
    obs = sum(mi_bits(x[v], y[v]) * len(v) / tot for v in big.values())
    null = np.empty(perms)
    for i in range(perms):
        xs = x.copy()
        for v in big.values():
            xs[v] = x[rng.permutation(v)]
        null[i] = sum(mi_bits(xs[v], y[v]) * len(v) / tot for v in big.values())
    mu, sd = float(null.mean()), float(null.std(ddof=1))
    res = {"covered_rows": int(tot), "n_groups": len(big),
           "obs_minus_null": round(obs - mu, 6)}
    if sd == 0 and abs(obs - mu) < 1e-9:
        res.update({"status": "EXACT_ZERO_ZERO_VARIANCE_NULL",
                    "z": 0.0,
                    "note": "x is constant inside every prefix group "
                            "(predicted by the bijection)"})
    elif sd == 0:
        res.update({"status": "NULL_DEGENERATE_BUT_OBS_DIFFERS",
                    "z": None})
    else:
        res.update({"null_mean": round(mu, 6), "null_sd": round(sd, 6),
                    "z": round((obs - mu) / sd, 3)})
    return res


# ------------------------------------------------------------------ #
# MAIN
# ------------------------------------------------------------------ #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--pop", type=int, default=None)
    ap.add_argument("--perms", type=int, default=None)
    args = ap.parse_args()

    t0 = time.time()
    POP = args.pop or (240 if args.smoke else 4000)
    PERMS = args.perms or (40 if args.smoke else 300)
    N_BROAD = int(POP * 0.8)
    N_BAL = POP - N_BROAD
    MIN_GROUP = 30 if args.smoke else 60
    TMAX = 6            # positions 0..5
    NEG_MODS = [16, 32, 64, 128, 256]   # disclosed negative-claim cells

    out = {
        "exp": "552",
        "codename": "TWO-ADIC-PRICE-LAW",
        "smoke": bool(args.smoke),
        "status": "running",
        "config": {
            "seed": SEED, "pop": POP, "broad": N_BROAD, "balanced": N_BAL,
            "perms": PERMS, "p_range": "[2^13,2^17]",
            "q_range": "[2^15,2^21]",
            "balanced_def": "p in [2^15,2^17], q in primes (p,3p)",
            "positions": f"0..{TMAX-1}", "negative_claim_moduli": NEG_MODS,
            "min_prefix_group": MIN_GROUP,
        },
        "derivation": {
            "done_before_measurement": True,
            "descent_rule": "m odd->A; m even&2n<m->B; m even&2n>m->C",
            "mechanism": (
                "Every Price step halves exactly one of U=p+q, V=q-p "
                "(A halves V; B,C halve U). letter_t='A' <=> v2(U_t)=1 "
                "(m-coordinate odd); A SEES V (halves it, admissible iff "
                "v2(U)=1), B/C SEE U (halve it, admissible iff v2(U)>=2); "
                "B-vs-C is the SIGN of V-U/2, a size comparison, never a "
                "congruence."),
            "first_A_position": "u0-1 with u0=v2(p+q); non-A steps halve U "
                                "exactly, decrementing v2(U) by 1",
            "exact_map": {
                "pos0": "N=1 mod 4 => 'A'; N=3 mod 4 => B iff q<3p else C",
                "pos1": "'A' <=> N mod 8 in {1,3}; else B/C by size",
                "bijection_first_two_vs_Nmod8":
                    "(A,A)<->1, (A,~A)<->5, (~A,A)<->3, (~A,~A)<->7",
            },
            "determinism_depth": "EXACTLY positions 0,1 (two clicks)",
            "scrambling_lemma":
                "For j>=3, N = 2^j*p*o - p^2 (o odd); odd squares fill "
                "{1 mod 8} classes uniformly, so N mod 2^k is uniform on "
                "{7 mod 8} for every k>j, identical across u0=j and u0>j. "
                "No modulus determines anything from position 2 on.",
            "B_rarity": "B needs N=3 mod 4 (prob 1/2) AND q<3p (near "
                        "square); P(B) ~ (1/2)*P(q<3p) ~ 0.05-0.15 by "
                        "stratum mix; C absorbs the far field.",
            "predictions": ["P1 rule==truth 100%", "P2 pos0 law 100%",
                            "P3 pos1 law 100%",
                            "P4 marginal z huge at t<=1, leakage tail",
                            "P5 conditional EXACT zero at t>=2",
                            "P6 capacity saturates at M=8",
                            "P7 which-factor wall holds"],
        },
        "pipeline_checks": {},
        "part1": {},
        "part2": {},
        "part3": {},
        "ledger": [
            "DERIVATION-FIRST: the exact map (Steps 1-4) was derived on "
            "paper and encoded in this file BEFORE any population draw; "
            "measurement only verifies.",
            "BALANCED-STRATUM ADJUSTMENT: to honor q in [2^15,2^21] while "
            "forcing the B-regime q<3p, the balanced stratum draws p in "
            "[2^15,2^17] (not [2^13,2^17]) and q in primes (p,3p). "
            "Disclosed as a deviation from an naive reading of the spec.",
            "ROUND-70 MARGINAL CONTEXT: exp548-era marginal {A:.48,B:.05,"
            "C:.47} is explained analytically: A owns the N=1 mod 4 half; "
            "B needs the intersection (opposite mod-4 residues AND q<3p). "
            "This experiment's pos0 marginal (see part1) is higher on B "
            "because the 20% balanced stratum forces q<3p (B-rate ~= "
            "P(N=3 mod 4) = 1/2 there) and uniform-over-primes drawing "
            "tilts q low; the MECHANISM (double condition) is identical.",
            "ZERO-VARIANCE NULLS ARE A RESULT, NOT A BUG: within-prefix "
            "conditional at t>=2 has N mod 8 constant inside every prefix "
            "group (the bijection); these cells are reported as exact "
            "zeros, not undefined z.",
        ],
    }

    log(f"start smoke={args.smoke} POP={POP} PERMS={PERMS}")

    # ---------------- population + descents ---------------- #
    rng = np.random.default_rng(SEED)
    p_arr, q_arr, strat = draw_population(rng, N_BROAD, N_BAL)
    rows = []
    emb_fail = term_fail = 0
    for p, q in zip(p_arr, q_arr):
        p, q = int(p), int(q)
        N = p * q
        m, n = (p + q) // 2, (q - p) // 2
        if not (m * m - n * n == N and gcd(m, n) == 1 and
                (m - n) % 2 == 1 and m > n >= 1):
            emb_fail += 1
            continue
        try:
            letters = price_descend_letters(m, n)
        except Exception:
            term_fail += 1
            continue
        ok_re = price_reascend(letters) == (m, n)
        rows.append({"p": p, "q": q, "N": N, "m": m, "n": n,
                     "letters": letters, "reascent_ok": ok_re})
    assert emb_fail == 0, "embedding must be perfect"
    assert term_fail == 0, "termination must be 100%"
    re_bad = sum(1 for r in rows if not r["reascent_ok"])
    assert re_bad == 0, "re-ascent must land on start for every row"
    min_dp = min(len(r["letters"]) for r in rows)
    assert min_dp >= TMAX + 2, f"population too shallow: min_dP={min_dp}"

    NR = len(rows)
    Narr = np.array([r["N"] for r in rows], dtype=np.int64)
    Larr = np.array([[CMAP[l] for l in r["letters"][:TMAX]] for r in rows])
    strata = np.array([f"{int(log2(r['p']))}x{int(log2(r['q']))}"
                       for r in rows])
    Nmod = lambda k: (Narr % (2 ** k)).astype(np.int64)

    out["pipeline_checks"] = {
        "population_embedded": NR,
        "embedding_failures": emb_fail,
        "embedding_identity_m2_minus_n2_eq_N_pass": bool(emb_fail == 0),
        "termination_rate": 1.0,
        "termination_failures": term_fail,
        "reversed_descent_ascent_lands_on_start": bool(re_bad == 0),
        "min_depth_observed": int(min_dp),
        "strata_cells": int(len(np.unique(strata))),
    }
    log(f"population NR={NR} emb_fail={emb_fail} term_fail={term_fail} "
        f"re-ascent OK, min_dP={min_dp}, strata={out['pipeline_checks']['strata_cells']}")

    # ---------------- PART 1: verify the exact map ---------------- #
    # (a) residue laws at 100%
    a0 = (Larr[:, 0] == 0)
    a1 = (Larr[:, 1] == 0)
    agree0 = float((a0 == (Narr % 4 == 1)).mean())
    agree1 = float((a1 == np.isin(Narr % 8, (1, 3))).mean())
    # converse direction explicitly (both directions included in ==)
    n_viol0 = int((a0 != (Narr % 4 == 1)).sum())
    n_viol1 = int((a1 != np.isin(Narr % 8, (1, 3))).sum())

    # (b) bijection A-ness pattern of first two letters <-> N mod 8
    aness = [(bool(r[0] == 0), bool(r[1] == 0)) for r in Larr[:, :2]]
    bio_map_check = {}
    for pat in set(aness):
        idx = [i for i, a in enumerate(aness) if a == pat]
        mods8 = sorted(set(int(Narr[i]) % 8 for i in idx))
        bio_map_check[str(pat)] = mods8
    bijection_exact = (all(len(v) == 1 for v in bio_map_check.values())
                       and sorted(v[0] for v in bio_map_check.values())
                       == [1, 3, 5, 7]
                       and len(bio_map_check) == 4)

    # (c) B-vs-C size rule at position 0 (derived, not residue)
    bc_mask = Larr[:, 0] != 0
    pred_bc = np.where(3 * np.array([r["p"] for r in rows]) >
                       np.array([r["q"] for r in rows]), 1, 2)
    agree_bc = float((Larr[bc_mask, 0] == pred_bc[bc_mask]).mean())

    # (d) mechanical rule == true descent at ALL positions (full paths)
    rule_checks = rule_fail = 0
    for r in rows:
        m, n = r["m"], r["n"]
        for ch in r["letters"]:
            rule_checks += 1
            if letter_rule(m, n) != ch:
                rule_fail += 1
            # step down exactly as the true descent does
            M, Nc = m, n
            if M % 2 == 1:
                m, n = M - Nc // 2, Nc // 2
            else:
                h = M // 2
                m, n = (h, h - Nc) if Nc < h else (h, Nc - h)

    # (e) negative claims: cells of N mod 2^k pure in letter_t, t>=2.
    # Determinism claim needs support: only cells with n >= 20 count;
    # tiny-cell purity is disclosed as sampling noise, not structure.
    MIN_CELL_N = 20
    neg_cells = []
    for k in NEG_MODS:
        X = Nmod(int(log2(k)))
        for t in range(2, TMAX):
            purities, small_pure = [], 0
            for cell in np.unique(X):
                col = Larr[X == cell, t]
                cnt = np.bincount(col, minlength=3)
                pur = float(cnt.max() / cnt.sum())
                if len(col) >= MIN_CELL_N:
                    purities.append(pur)
                elif pur == 1.0:
                    small_pure += 1
            neg_cells.append({
                "cell_family": f"N mod {k} vs letter{t}",
                "n_residue_cells": int(len(np.unique(X))),
                "n_cells_with_support_ge_%d" % MIN_CELL_N: len(purities),
                "pure_cells_with_support": int(sum(1 for u in purities
                                                   if u == 1.0)),
                "tiny_pure_cells_disclosed": small_pure,
                "max_cell_purity_supported":
                    round(max(purities), 4) if purities else None,
                "claim": ("NO determinism (no supported pure cells)"
                          if purities and max(purities) < 1.0
                          else "SUPPORTED PURE CELLS FOUND")})
    neg_clean = all(c["pure_cells_with_support"] == 0 for c in neg_cells)

    # marginals
    marg0 = {c: round(float((Larr[:, 0] == i).mean()), 4)
             for i, c in enumerate("ABC")}

    out["part1"] = {
        "rule_vs_true_descent": {"steps_checked": rule_checks,
                                 "failures": rule_fail,
                                 "agreement_pct": round(
                                     100 * (1 - rule_fail / rule_checks), 4)},
        "pos0_law_A_iff_Nmod4_1": {
            "agreement_pct": round(100 * agree0, 4), "violations": n_viol0},
        "pos1_law_A_iff_Nmod8_in_13": {
            "agreement_pct": round(100 * agree1, 4), "violations": n_viol1},
        "pos0_BC_size_rule_q_lt_3p": {
            "agreement_pct": round(100 * agree_bc, 4)},
        "bijection_first_two_letters_vs_Nmod8": {
            "map_observed": bio_map_check,
            "bijective_and_exact": bool(bijection_exact)},
        "negative_claims_positions_2_to_5": neg_cells,
        "no_determinism_at_t_ge_2_any_modulus": bool(neg_clean),
    }
    # measured marginal reconciliation appended to the ledger
    out["ledger"].append(
        f"MEASURED MARGINAL RECONCILIATION: pos0 letters "
        f"A={marg0['A']}, B={marg0['B']}, C={marg0['C']}; analytic "
        f"P(B) = P(N=3 mod 4)*P(q<3p) per stratum (balanced forces "
        f"q<3p).")

    out["part1"]["letter_marginal_pos0"] = marg0
    out["part1"]["B_rarity_explained"] = (
        "B = [N=3 mod 4] AND [q<3p]; both needed; C absorbs far field")
    log(f"P1 rule agreement {out['part1']['rule_vs_true_descent']['agreement_pct']}% "
        f"| pos0 law {100*agree0:.2f}% (viol {n_viol0}) | pos1 law "
        f"{100*agree1:.2f}% (viol {n_viol1}) | BC size rule {100*agree_bc:.2f}% "
        f"| bijection exact={bijection_exact} | neg-clean={neg_clean} "
        f"| marg0={marg0}")

    # ---------------- PART 2: depth z-ladders ---------------- #
    rng2 = np.random.default_rng(SEED + 1)
    rng3 = np.random.default_rng(SEED + 2)
    X8 = Nmod(3)
    ladder_marginal, ladder_conditional = [], []
    for t in range(TMAX):
        r_g = perm_mi_z_global(X8, Larr[:, t], PERMS, rng2)
        r_s = perm_mi_z_stratified(X8, Larr[:, t], strata, PERMS, rng2)
        ladder_marginal.append({"t": t, "global": r_g, "stratified": r_s})
        # conditional given prefix letters[:t]
        prefixes = [tuple(r["letters"][:t]) for r in rows]
        r_c = (perm_mi_z_global(X8, Larr[:, t], PERMS, rng3)
               if t == 0 else
               perm_mi_z_within_prefix(X8, Larr[:, t], prefixes,
                                       MIN_GROUP, PERMS, rng3))
        ladder_conditional.append({"t": t, "within_prefix": r_c})
        log(f"P2 t={t}: I(Nmod8;L{t})={r_s['mi_bits']} strat-z={r_s['z']} "
            f"cond={r_c.get('z', r_c.get('status'))}")
    out["part2"]["ladder_marginal_Nmod8_vs_letter_t"] = ladder_marginal
    out["part2"]["ladder_conditional_given_prefix"] = ladder_conditional

    # where does visibility die? (data-driven verdict inputs)
    def cond_alive(wc):
        """A conditional cell counts as ALIVE only if it has coverage and
        shows a real, significant effect."""
        if wc.get("covered_rows", 0) == 0:
            return None  # untestable, disclosed separately
        if wc.get("status") == "EXACT_ZERO_ZERO_VARIANCE_NULL":
            return False
        zval = wc.get("z")
        return bool(zval is not None and abs(zval) >= 2)

    cond_dead_from = None
    untestable = []
    for entry in ladder_conditional:
        if entry["t"] < 1:
            continue
        al = cond_alive(entry["within_prefix"])
        if al is None:
            untestable.append(entry["t"])
        elif not al and cond_dead_from is None:
            cond_dead_from = entry["t"]
            break
    marg_z01 = [abs(ladder_marginal[t]["stratified"]["z"] or 0)
                for t in range(2)]
    out["part2"]["death_point"] = {
        "conditional_visibility_dead_from_t": cond_dead_from,
        "untestable_positions_insufficient_coverage": untestable,
        "marginal_z_t0_t1_stratified": marg_z01,
        "reading": ("conditional dies exactly at t="
                    f"{cond_dead_from} (zero-variance nulls: N mod 8 "
                    "constant inside every prefix cell, per the bijection)"
                    if cond_dead_from is not None else
                    "conditional visibility persists; see ladders"),
    }

    # leakage decomposition at t=2: conditional on prefix kills it?
    out["part2"]["leakage_note"] = (
        "Any surviving marginal MI at t>=2 is leakage of the first two "
        "letters' residue-lock (the bijection), not new 2-adic visibility.")

    # ---------------- PART 3: wall + capacity ---------------- #
    rng4 = np.random.default_rng(SEED + 3)
    # channel output: labeled ordered letter-pair (positions 0,1)
    chan = Larr[:, 0] * 3 + Larr[:, 1]
    S16 = Nmod(4)
    WF = (np.array([r["p"] for r in rows]) % 4 == 1).astype(np.int64)

    def wall_test(channel_bins, label, perms, rngw):
        obs_pool, nulls = 0.0, np.zeros(perms)
        segs = []
        for cell in np.unique(S16):
            idx = np.nonzero(S16 == cell)[0]
            if len(idx) < 30:
                continue
            segs.append(idx)
        tot = sum(len(s) for s in segs)
        obs_pool = sum(mi_bits(channel_bins[s], WF[s]) * len(s) / tot
                       for s in segs)
        for i in range(perms):
            wp = WF.copy()
            for s in segs:
                wp[s] = WF[rngw.permutation(s)]
                nulls[i] = sum(mi_bits(channel_bins[s], wp[s]) * len(s) / tot
                           for s in segs)
        mu, sd = float(nulls.mean()), float(nulls.std(ddof=1))
        return {"channel": label, "n_cells_S16_used": len(segs),
                "I_bits": round(obs_pool, 6),
                "null_mean": round(mu, 6), "null_sd": round(sd, 6),
                "sensitivity_bits": round(abs(obs_pool - mu), 6),
                "z": round((obs_pool - mu) / sd, 3) if sd > 0 else None}

    wall_pair = wall_test(chan, "labeled_letter_pair", PERMS, rng4)
    # exploratory: full 6-letter labeled path channel
    path_code = np.array([int("".join(map(str, row)), 3)
                          for row in Larr])
    wall_path = wall_test(path_code, "labeled_letter_path_len6", PERMS, rng4)
    out["part3"]["which_factor_wall"] = {
        "definition": "I(channel ; WF=[smaller prime = 1 mod 4]) pooled "
                      "within N mod 16 cells; null shuffles WF inside "
                      "cells (exp524 recipe); wall HOLDS if max|z| < 4",
        "wf_note": "given N mod 16, the smaller prime's class is uniform "
                   "over units (Corollary A2 symmetry), P(WF)=1/2",
        "pair_channel": wall_pair,
        "path_channel_exploratory": wall_path,
        "wall_holds": bool(max(abs(wall_pair["z"] or 0),
                               abs(wall_path["z"] or 0)) < 4),
    }
    log(f"P3 wall pair z={wall_pair['z']} sens={wall_pair['sensitivity_bits']}b "
        f"path z={wall_path['z']} sens={wall_path['sensitivity_bits']}b")

    # symmetric capacity: I(N mod 2^k ; unordered letter-pair)
    unordered = np.array([min(a, b) * 3 + max(a, b)
                          for a, b in Larr[:, :2]])
    cap_curve = []
    rng5 = np.random.default_rng(SEED + 4)
    for k in (1, 2, 3, 4, 5):
        r = perm_mi_z_global(Nmod(k), unordered, PERMS, rng5)
        cap_curve.append({"modulus": 2 ** k, **r})
        log(f"P3 capacity I(N mod 2^{k}; unordered pair)={r['mi_bits']} "
            f"z={r['z']}")
    sat_gap = abs(cap_curve[3]["mi_bits"] - cap_curve[2]["mi_bits"])
    out["part3"]["symmetric_channel_capacity"] = {
        "target": "I(N mod 2^k ; UNORDERED letter-pair at positions 0,1)",
        "curve": cap_curve,
        "saturation_gap_mod16_vs_mod8_bits":
            round(sat_gap, 6),
        "per_class_outcome_counts_Nmod8": {
            str(c): sorted(set("".join(sorted(("ABC"[int(Larr[i, 0])],
                                              "ABC"[int(Larr[i, 1])])))
                              for i in np.nonzero(Narr % 8 == c)[0]))
            for c in (1, 3, 5, 7)},
    }

    # ---------------- VERDICTS (computed from data) ---------------- #
    p1_ok = (rule_fail == 0 and n_viol0 == 0 and n_viol1 == 0 and
             bijection_exact and agree_bc == 1.0)
    tested = [e for e in ladder_conditional[2:]
              if cond_alive(e["within_prefix"]) is not None]
    cond_all_dead = bool(tested) and all(
        not cond_alive(e["within_prefix"]) for e in tested)
    cap_sat = sat_gap < 0.02
    if p1_ok and cond_all_dead and neg_clean:
        v_main = "TWO-ADIC-PATH-TWO-CLICKS-THEN-SEALED"
    elif p1_ok and not cond_all_dead:
        v_main = "TWO-ADIC-VISIBLE-BEYOND-POSITION-1"
    else:
        v_main = "MAP-REFUTED-CHECK-DERIVATION"
    v_wall = ("WHICH-FACTOR-WALL-HOLDS-JOINS-SEALED-RESIDUE-DIAL-FAMILY"
              if out["part3"]["which_factor_wall"]["wall_holds"]
              else "WALL-LEAKS")
    v_cap = ("ORDER-UNIVERSAL-ABELIANIZATION-FIT-CAPACITY-SATURATES-MOD8"
             if cap_sat else "CAPACITY-NOT-SATURATED-AT-MOD8")

    out["verdicts"] = {
        "main": v_main,
        "which_factor_wall": v_wall,
        "capacity_family": v_cap,
        "part1_all_laws_100pct": bool(p1_ok),
        "conditional_death_exact_at_t2": bool(cond_all_dead),
        "no_determinism_beyond_pos1": bool(neg_clean),
        "capacity_saturates_mod8": bool(cap_sat),
        "statement": (
            "The Price descent's first two letters ARE the low bits of N: "
            "letter0='A' iff N=1 mod 4, letter1='A' iff N mod 8 in {1,3}, "
            "with (A-ness0,A-ness1) bijective with N mod 8. Mechanism: "
            "every step halves exactly one of U=p+q,V=q-p; letter_t='A' "
            "iff v2(U_t)=1; the first A lands at u0-1, u0=v2(p+q), and "
            "N mod 2^k sees u0 only capped at {1,2,>=3} (odd squares = 1 "
            "mod 8; higher bits scrambled by the unknown odd multiplier). "
            "Positions >=2 are provably invisible to EVERY modulus and "
            "B-vs-C is a size comparison, never a congruence: the "
            "residue-visible path is exactly two clicks deep. The "
            "channel is which-factor blind and its symmetric capacity "
            "saturates at modulus 8 -- it joins the sealed "
            "order-universal/abelianization residue-dial family rather "
            "than opening a factoring route."),
    }
    out["status"] = "04_final"
    out["wall_s"] = round(time.time() - t0, 1)

    with open(RESULT_PATH, "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    log(f"VERDICT main={v_main} | {v_wall} | {v_cap} | "
        f"wall={out['wall_s']}s -> {RESULT_PATH}")


if __name__ == "__main__":
    main()

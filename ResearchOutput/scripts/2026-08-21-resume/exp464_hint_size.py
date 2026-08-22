#!/usr/bin/env python3
"""
exp464 HINT-SIZE-SCALING (round-37, factor3 lab)
================================================
QUESTION: does the hint value I((p mod m*, q mod m*); labels) - I(N mod m*; labels)
depend on FACTOR SIZE (bit-length k of the primes)? All prior hint measurements were
at one toy size (factors ~2^12). By Dirichlet equidistribution the answer should be
"size-stable"; that has never been tested.

------------------------------------------------------------------------------
HYPOTHESES (PRE-STATED BEFORE ANY DATA, 2026-08-21, seed 20260821)
------------------------------------------------------------------------------
H1 (stability): hint value is constant in factor bit-length k across
    k in {10, 14, 18, 22} to within sampling error (< 10% relative drift)
    for every tested dial.

H2 (drift): hint value decays or grows systematically with k.
    PRE-STATED SPECULATED MECHANISMS (before looking):
      (i) Finite-population equidistribution deficit: at small k the prime pool
          is tiny (78 primes at k=10, ~900 at k=14), so the empirical mass of
          each residue class / label class deviates from its Chebotarev limit
          by O(1/sqrt(pool)); the hint channel is a residue-level quantity so
          its CAPACITY is k-independent, but its measured value inherits the
          class-mass skew. If anything this predicts a mild INCREASING drift
          toward the asymptote as k grows (convergence of equidistribution),
          not decay.
      (ii) The label<->residue map is deterministic given p and the conductor;
          nothing in the Galois theory knows about factor bit-length, so a
          systematic DECAY with k would be surprising and would break every
          extrapolation of the hint programme.

DECISION RULES (PRE-STATED):
  For each dial, over the four sizes:
    - relative drift := max_k |hint(k) - median_k hint| / median_k hint
    - trend: Spearman rho of hint vs k, two-sided EXACT permutation p over the
      4! rank permutations (the t/df=2 approximation is invalid at n=4: it
      reports p~0 at |rho|=1 while the exact two-sided floor is 2/24 = 0.083;
      consequence, disclosed in advance: the trend leg alone can never reach
      p < 0.05 at n=4, so the drift leg does the deciding work)
  H1 verdict for the dial iff drift < 0.15 AND Spearman p >= 0.05.
  Otherwise H2 for that dial (report direction + which dial).
  Global verdict: H1 iff ALL FOUR dials pass; else H2 with details.

  Which-factor wall (barrier-2 invariant along the size axis):
  W := sum over heterogeneous unordered-label-pair strata u (both orientations
  present) of (n_u/n) * I_u(N mod m*; orientation bit), i.e. the conditional-MI
  chain-rule reading of how many bits N carries about WHICH factor carries
  which type GIVEN the unordered content. Null: flip a fair coin per draw and
  swap (label_p, label_q) on heads -- this holds (N mod m*, unordered pair)
  EXACTLY fixed and randomizes only the orientation within each stratum;
  300 shuffles; W must sit inside its null (|z| < 2) at EVERY size and dial.
  NOTE (ledger L5): the naive statistic D = I(N;ordered) - I(N;unordered)
  against the UNCONDITIONAL label-shuffle null was rejected during the smoke
  test BEFORE data collection: its plug-in bias asymmetry depends on the
  dependence structure, which shuffling destroys, so the null mis-centers
  (smoke: spurious z down to -4.7). The conditional orientation-permutation
  null above is the correct instrument (paper-93-style which-factor test).
  The literal reading "I(N;ordered label pair) inside its permutation null"
  cannot be intended, since that channel provably carries the product-view
  signal (I(N;ordered) = I(N;unordered) under exchangeability) and never sits
  inside a shuffle null.

------------------------------------------------------------------------------
LABEL DEFINITIONS (EXACT, KEPT CONSISTENT ACROSS SIZES)
------------------------------------------------------------------------------
 (a) S3 cubic f = x^3 + x + 1 (disc -31, splitting-field conductor 31), m* = 31.
     label = splitting type by root count: nr = deg gcd(x^p - x, f) over F_p;
     nr=3 -> [1,1,1] (code 2), nr=1 -> [1,2] (code 1), nr=0 -> [3] (code 0).
     Chebotarev targets: 1/6, 1/2, 1/3.
 (b) Cyclic cubic f = x^3 + x^2 - 2x - 1 (= 2cos(2pi/7), Q(zeta7)^+, C3,
     conductor 7), m* = 7. label: [1,1,1] iff p mod 7 in {+1,-1} (code 1),
     [3] otherwise (code 0). NOTE: the task brief's first phrasing
     ("p=1 -> split, p=6 -> [3]") contradicts its own correction two lines
     later; the correct abelian rule is p = +-1 mod 7 -> split completely
     (complex conjugation acts trivially on the real field), rates 2/6=1/3
     and 4/6=2/3. RULE VERIFIED NUMERICALLY against direct polynomial
     factorization on a sample of primes (see VERIFICATION).
 (c) D4 quartic f = x^4 - 2 (conductor 8), m* = 8.
     SIMPLER ROBUST CHOICE (per brief): label = nr = root count of x^4 - 2
     mod p in {0,1,2,4} (codes 0,1,2,3 for nr = 0,1,2,4). Documented
     conflation: nr=2 merges types [1,1,2] and [2,2]; we deliberately do NOT
     use "nr mod 4" (that would additionally merge [4] with [1,1,1,1], which
     is strictly worse). Same definition at every size.
 (d) C5 quintic f = x^5 + x^4 - 4x^3 - 3x^2 + 3x + 1 (= 2cos(2pi/11),
     Q(zeta11)^+, conductor 11), m* = 11. label binary: 1 iff p mod 11 in
     {+1,-1} (splits completely, rate 2/10), else 0 (rate 8/10).
     RULE VERIFIED NUMERICALLY against direct factorization.

------------------------------------------------------------------------------
DISCLOSURES / DESIGN NOTES (PRE-STATED)
------------------------------------------------------------------------------
 - Draws are iid uniform WITH replacement from the pool of primes in
   [2^(k-1), 2^k). At k=10 the pool has only 78 primes, so with-replacement is
   forced; it also KILLS the brief's speculated finite-population correlation
   between p and q draws by construction (p, q remain independent at every k),
   isolating the class-mass-skew mechanism (i) as the only finite-k effect.
 - p = q draws are redrawn (semiprime convention N = pq with p != q).
 - The SAME prime draws are reused across the four dials within a size
   (labels computed independently per dial); dials remain independent channels.
 - Ramified primes (dividing 31/7/2/11) cannot occur: pools start at 2^9.
 - MI: discrete plug-in, log base 2, n = 15000 per size (floor 8000 if slow).
   Permutation nulls: 300 shuffles of the label arrays (jointly) against the
   fixed residue arrays; one shared permutation family per (dial, size) gives
   coherent nulls for the product-view MI, hint-view MI, and wall statistic D.
   Bootstrap: 200 resamples, percentile CI for the hint value.
 - Bias note: plug-in MI bias ~ (R-1)(S-1)/(2n) is constant in k at fixed
   alphabet (n fixed at 15000), so it cancels in the DRIFT comparison to first
   order; raw values are reported with null means so the bias is visible.

METHOD LEDGER: filled at bottom of result.json and in the agent report.
"""

import json
import math
import time

import numpy as np

SEED = 20260821
SIZES = [10, 14, 18, 22]
N_DRAWS = 15000
N_PERMS = 300
N_BOOT = 200
DRIFT_TOL = 0.15
WALL_Z_TOL = 2.0
OUT = "/tmp/exp37_hintsize/result.json"

rng = np.random.default_rng(SEED)
LEDGER = []


# ----------------------------------------------------------------------------
# polynomial machinery over F_p (all polys monic, lists low->high, stripped)
# ----------------------------------------------------------------------------

def ptrim(a):
    while a and a[-1] == 0:
        a.pop()
    return a


def pdeg(a):
    return (len(a) - 1) if a else -1


def pmul(a, b, f, p):
    """(a*b) mod f over F_p, f monic."""
    if not a or not b:
        return []
    c = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                c[i + j] += ai * bj
    m = len(f) - 1
    for i in range(len(c) - 1, m - 1, -1):
        coef = c[i] % p
        if coef:
            for j in range(m):
                c[i - m + j] -= coef * f[j]
    del c[m:]
    return ptrim([t % p for t in c])


def ppow_x(n, f, p):
    """x^n mod f over F_p."""
    r = [1]
    b = pmul([0, 1], [1], f, p)  # x mod f (identity for deg f > 1)
    while n:
        if n & 1:
            r = pmul(r, b, f, p)
        n >>= 1
        if n:
            b = pmul(b, b, f, p)
    return r


def pdivmod(a, b, p):
    a = a[:]
    db = pdeg(b)
    inv = pow(b[-1], p - 2, p)
    q = [0] * max(0, pdeg(a) - db + 1)
    for i in range(pdeg(a) - db, -1, -1):
        coef = (a[i + db] * inv) % p
        if coef:
            q[i] = coef
            for j in range(db + 1):
                a[i + j] = (a[i + j] - coef * b[j]) % p
    return ptrim(q), ptrim(a)


def pgcd(a, b, p):
    a, b = ptrim(a[:]), ptrim(b[:])
    while b:
        a, b = b, pdivmod(a, b, p)[1]
    return a


def nroots(f, p):
    """nr = number of distinct roots of f in F_p (deg gcd(x^p - x, f))."""
    r = ppow_x(p, f, p)
    if len(r) < 2:
        r = r + [0] * (2 - len(r))
    r[1] = (r[1] - 1) % p  # subtract x
    ptrim(r)
    if not r:
        return len(f) - 1  # f | x^p - x: all roots
    g = pgcd(r, f, p)
    return pdeg(g)


# ----------------------------------------------------------------------------
# dials
# ----------------------------------------------------------------------------

F_S3 = [1, 1, 0, 1]                    # x^3 + x + 1
F_CYC3 = [-1, -2, 1, 1]                # x^3 + x^2 - 2x - 1
F_D4 = [(-2), 0, 0, 0, 1]              # x^4 - 2
F_C5 = [1, 3, -3, -4, 1, 1]            # x^5 + x^4 - 4x^3 - 3x^2 + 3x + 1

DIALS = {
    "S3_cubic_x3+x+1_m31": {"m": 31, "nlab": 3},
    "cyc3_x3+x2-2x-1_m7": {"m": 7, "nlab": 2},
    "D4_x4-2_m8": {"m": 8, "nlab": 4},
    "C5_zeta11real_m11": {"m": 11, "nlab": 2},
}

# theoretical label marginals (code order) where known; None = no closed target
THEORY = {
    "S3_cubic_x3+x+1_m31": {2: 1 / 6, 1: 1 / 2, 0: 1 / 3},   # [1,1,1],[1,2],[3]
    "cyc3_x3+x2-2x-1_m7": {1: 1 / 3, 0: 2 / 3},
    "D4_x4-2_m8": None,
    "C5_zeta11real_m11": {1: 1 / 5, 0: 4 / 5},
}


def label_S3(p):
    nr = nroots(F_S3, p)
    assert nr in (0, 1, 3), (p, nr)
    return {0: 0, 1: 1, 3: 2}[nr]


def label_CYC3(p):
    return 1 if p % 7 in (1, 6) else 0


def label_D4(p):
    nr = nroots(F_D4, p)
    assert nr in (0, 1, 2, 4), (p, nr)
    return {0: 0, 1: 1, 2: 2, 4: 3}[nr]


def label_C5(p):
    return 1 if p % 11 in (1, 10) else 0


LABEL_FN = {
    "S3_cubic_x3+x+1_m31": label_S3,
    "cyc3_x3+x2-2x-1_m7": label_CYC3,
    "D4_x4-2_m8": label_D4,
    "C5_zeta11real_m11": label_C5,
}


# ----------------------------------------------------------------------------
# independent verification via sympy factorization over GF(p)
# ----------------------------------------------------------------------------

def verify_labels(pool, size):
    import sympy as sp
    x = sp.symbols("x")
    exprs = {
        "S3_cubic_x3+x+1_m31": x**3 + x + 1,
        "D4_x4-2_m8": x**4 - 2,
    }
    mism = {}
    for name, expr in exprs.items():
        f = DIALS[name]
        idx = rng.choice(len(pool), size=30, replace=False)
        bad = 0
        for i in idx:
            p = int(pool[i])
            nr_mine = nroots({"S3_cubic_x3+x+1_m31": F_S3, "D4_x4-2_m8": F_D4}[name], p)
            facs = sp.factor_list(expr, modulus=p)[1]
            nr_sympy = sum(mult for poly, mult in facs if sp.degree(poly) == 1)
            if nr_mine != nr_sympy:
                bad += 1
        mism[name] = bad
    # abelian residue rules vs direct computation
    for name, f, rule in (
        ("cyc3_x3+x2-2x-1_m7", F_CYC3, label_CYC3),
        ("C5_zeta11real_m11", F_C5, label_C5),
    ):
        idx = rng.choice(len(pool), size=min(100, len(pool)), replace=False)
        bad = 0
        for i in idx:
            p = int(pool[i])
            nr = nroots(f, p)
            direct = 1 if nr == len(f) - 1 else 0
            if direct != rule(p):
                bad += 1
        mism[name] = bad
    return mism


# ----------------------------------------------------------------------------
# information measures
# ----------------------------------------------------------------------------

def mi(x, y, nx, ny):
    c = np.bincount(x * ny + y, minlength=nx * ny).reshape(nx, ny).astype(np.float64)
    n = c.sum()
    pxy = c / n
    px = pxy.sum(axis=1, keepdims=True)
    py = pxy.sum(axis=0, keepdims=True)
    outer = px * py
    mask = pxy > 0
    return float(np.sum(pxy[mask] * np.log2(pxy[mask] / outer[mask])))


def cond_wall_mi(prod_code, lp, lq, m, nlab, n):
    """W: bits N carries about orientation GIVEN the unordered label pair.

    Sum over heterogeneous unordered strata u (both orientations present) of
    (n_u/n) * I_u(N mod m*; orientation bit). Homogeneous strata contribute 0.
    """
    ulab = np.minimum(lp, lq) * nlab + np.maximum(lp, lq)
    orient = (lp > lq).astype(np.int64)
    total = 0.0
    for u in np.unique(ulab[(lp != lq)]):
        mask = ulab == u
        ou = orient[mask]
        npos = int(ou.sum())
        if npos == 0 or npos == len(ou):
            continue
        xu = prod_code[mask]
        total += (len(ou) / n) * mi(xu, ou, m, 2)
    return total


def spearman_p(x, y):
    """Spearman rho + two-sided EXACT permutation p over all rank perms."""
    def ranks(a):
        order = np.argsort(a, kind="mergesort")
        r = np.empty(len(a), dtype=float)
        sa = a[order]
        i = 0
        while i < len(a):
            j = i
            while j + 1 < len(a) and sa[j + 1] == sa[i]:
                j += 1
            r[order[i:j + 1]] = (i + j) / 2.0
            i = j + 1
        return r
    rx, ry = ranks(np.asarray(x, float)), ranks(np.asarray(y, float))
    rx -= rx.mean(); ry -= ry.mean()
    den = math.sqrt(float((rx**2).sum()) * float((ry**2).sum()))
    rho_obs = 0.0 if den == 0 else float((rx * ry).sum()) / den

    from itertools import permutations
    count = tot = 0
    for perm in permutations(range(len(x))):
        rp = ry[list(perm)]
        rp = rp - rp.mean()
        den_p = math.sqrt(float((rx**2).sum()) * float((rp**2).sum()))
        rho = 0.0 if den_p == 0 else float((rx * rp).sum()) / den_p
        tot += 1
        if abs(rho) >= abs(rho_obs) - 1e-12:
            count += 1
    return rho_obs, count / tot


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def main():
    t_start = time.time()
    results = {"experiment": 464, "codename": "HINT-SIZE-SCALING",
               "seed": SEED, "date": "2026-08-21",
               "sizes": SIZES, "n_draws_target": N_DRAWS,
               "dials": {}}
    ledger_notes = [
        "L1 (design): brief's first cyclic-cubic phrasing (p=1 split / p=6 -> [3]) "
        "contradicts its own correction; correct abelian rule is p = +-1 mod 7 -> "
        "[1,1,1] (conjugation acts trivially on the real field), rates 1/3 vs 2/3; "
        "verified numerically against direct factorization.",
        "L2 (design): D4 label conflation documented -- root count nr merges "
        "[1,1,2] with [2,2]; chose plain nr over the brief's 'nr mod 4' because "
        "mod-4 would additionally merge [4] with [1,1,1,1].",
        "L3 (pre-data bug, caught by sympy cross-check): F_CYC3 constant term "
        "encoded +1 instead of -1 (x^3+x^2-2x+1); 83/480 poly-engine mismatches, "
        "all confined to this dial; fixed to [-1,-2,1,1], re-verified 0/200.",
        "L4 (smoke bug): abelian-rule verification sampled 100 primes from pools "
        "as small as 75 (k=10); clamped to min(100, pool).",
        "L5 (smoke, statistical instrument rejected BEFORE data collection): naive "
        "wall statistic D = I(N;ordered) - I(N;unordered) under the unconditional "
        "label-shuffle null mis-centers -- its plug-in bias asymmetry depends on "
        "the dependence structure, which shuffling destroys (spurious z to -4.7 in "
        "smoke). Replaced with conditional orientation-permutation test W: hold "
        "(N mod m*, unordered pair) fixed, fair-coin swap orientations within "
        "heterogeneous strata, 300 shuffles.",
        "L6 (statistical): Spearman t/df=2 approximation invalid at n=4 (reports "
        "p~0 at |rho|=1; exact two-sided permutation floor is 2/24=0.083, so the "
        "trend leg alone can never reach p<0.05 at n=4). Replaced with exact "
        "permutation p; disclosed in advance that the drift leg decides.",
        "L7 (post-first-full-run, before verdict interpretation): percentile "
        "bootstrap of the hint value sits entirely ABOVE its own point estimate "
        "in every cell -- known tie-inflation artifact: resampling with "
        "replacement duplicates rows, inflating the plug-in bias of the LARGE "
        "alphabet (pair residues, up to m^2 bins) more than the small one, and "
        "the hint is a difference. The bootstrap CI is disclosed but NOT used; "
        "verdicts use point estimates per the pre-stated rule, variability is "
        "reported additionally as a 40-half-sample scaled 95% spread.",
        "L8 (provenance): adding the L7 half-sample block shifted the rng stream "
        "downstream of the first cell, so the diagnostic rerun is a SECOND "
        "independent realization of the same seeded design, not a bit-replay "
        "(bit-identity holds only up through the k=10 S3 cell). The final "
        "script + seed define the canonical run (recorded here); the discarded "
        "first run serves as an unplanned replication: all point estimates "
        "agree in structure -- S3 {0.7423, 0.5484, 0.5301, 0.5442} vs "
        "{0.7423, 0.5584, 0.5425, 0.5415}, other dials stable within ~1% "
        "between realizations; verdicts identical.",
    ]

    for k in SIZES:
        t0 = time.time()
        hi, lo = 1 << k, 1 << (k - 1)
        sieve = np.ones(hi, dtype=bool)
        sieve[:2] = False
        for i in range(2, int(hi**0.5) + 1):
            if sieve[i]:
                sieve[i * i::i] = False
        pool = np.nonzero(sieve[lo:hi])[0] + lo
        pool_list = [int(v) for v in pool]

        # iid draws with replacement, p != q enforced
        idx = rng.integers(0, len(pool), size=(N_DRAWS, 2))
        bad = idx[:, 0] == idx[:, 1]
        while bad.any():
            idx[bad] = rng.integers(0, len(pool), size=(int(bad.sum()), 2))
            bad = idx[:, 0] == idx[:, 1]
        P = pool[idx[:, 0]]
        Q = pool[idx[:, 1]]
        n = len(P)
        t_sieve = time.time() - t0

        mism = verify_labels(pool, k)
        if any(v > 0 for v in mism.values()):
            ledger_notes.append(f"k={k}: label verification MISMATCHES {mism}")
        t_ver = time.time() - t0 - t_sieve

        results["dials"].setdefault("by_size", {})[k] = {
            "pool_size": int(len(pool)), "n_draws": int(n),
            "verify_mismatches": mism,
        }

        for name, d in DIALS.items():
            m, nlab = d["m"], d["nlab"]
            t1 = time.time()
            fn = LABEL_FN[name]
            if fn is label_CYC3:
                lp = np.where(P % 7 == 0, 0, 0)
                lp = ((P % 7 == 1) | (P % 7 == 6)).astype(np.int64)
                lq = ((Q % 7 == 1) | (Q % 7 == 6)).astype(np.int64)
            elif fn is label_C5:
                lp = ((P % 11 == 1) | (P % 11 == 10)).astype(np.int64)
                lq = ((Q % 11 == 1) | (Q % 11 == 10)).astype(np.int64)
            else:
                lp = np.array([fn(int(v)) for v in P], dtype=np.int64)
                lq = np.array([fn(int(v)) for v in Q], dtype=np.int64)
            t_lab = time.time() - t1

            pr = (P % m).astype(np.int64)
            qr = (Q % m).astype(np.int64)
            prod_code = (pr * qr % m).astype(np.int64)
            pair_code = (pr * m + qr).astype(np.int64)
            ulab = (np.minimum(lp, lq) * nlab + np.maximum(lp, lq)).astype(np.int64)
            olab = (lp * nlab + lq).astype(np.int64)

            obs_prod = mi(prod_code, ulab, m, nlab * nlab)
            obs_hint = mi(pair_code, ulab, m * m, nlab * nlab)
            obs_ord = mi(prod_code, olab, m, nlab * nlab)
            hint = obs_hint - obs_prod

            # which-factor wall: conditional orientation test (see header)
            W_obs = cond_wall_mi(prod_code, lp, lq, m, nlab, n)

            # shared permutation family: nulls for product MI and hint MI
            null_prod = np.empty(N_PERMS)
            null_hint = np.empty(N_PERMS)
            for s in range(N_PERMS):
                perm = rng.permutation(n)
                ul_s = ulab[perm]
                npd = mi(prod_code, ul_s, m, nlab * nlab)
                null_prod[s] = npd
                null_hint[s] = mi(pair_code, ul_s, m * m, nlab * nlab)

            # wall null: swap orientations within strata on fair coins --
            # holds (prod_code, ulab) exactly fixed
            null_W = np.empty(N_PERMS)
            for s in range(N_PERMS):
                flip = rng.random(n) < 0.5
                lp_s = np.where(flip, lq, lp)
                lq_s = np.where(flip, lp, lq)
                null_W[s] = cond_wall_mi(prod_code, lp_s, lq_s, m, nlab, n)

            def zscore(obs, arr):
                sd = float(arr.std())
                return (obs - float(arr.mean())) / sd if sd > 0 else float("inf")

            # bootstrap CI for hint value
            boot = np.empty(N_BOOT)
            for b in range(N_BOOT):
                ii = rng.integers(0, n, n)
                boot[b] = (mi(pair_code[ii], ulab[ii], m * m, nlab * nlab)
                           - mi(prod_code[ii], ulab[ii], m, nlab * nlab))
            ci_lo, ci_hi = np.percentile(boot, [2.5, 97.5])

            # honest variability: 40 random half-samples -> scaled 95% spread
            # (half-sample sd ~ sqrt(2) x full-sample sd). Consumes rng AFTER
            # everything above so all upstream numbers are bit-identical.
            hs = np.empty(40)
            for b in range(40):
                ii = rng.permutation(n)[:n // 2]
                hs[b] = (mi(pair_code[ii], ulab[ii], m * m, nlab * nlab)
                         - mi(prod_code[ii], ulab[ii], m, nlab * nlab))
            hs_lo = float(hint - 1.96 * hs.std() / math.sqrt(2))
            hs_hi = float(hint + 1.96 * hs.std() / math.sqrt(2))

            # mechanism diagnostics (no rng): residual label uncertainty given
            # the FULL pair-residue channel; identity-leakage indicators
            cnt = np.bincount(ulab, minlength=nlab * nlab).astype(float)
            pu = cnt[cnt > 0] / n
            H_ulab = float(-np.sum(pu * np.log2(pu)))
            resid_bits = H_ulab - obs_hint   # H(unordered pair | p,q residues)
            distinct_primes = int(len(np.unique(np.concatenate([P, Q]))))
            occ_pairs = int(len(np.unique(pair_code)))

            # label marginals
            rates = {int(c): float((np.concatenate([lp, lq]) == c).mean())
                     for c in range(nlab)}
            th = THEORY[name]
            max_dev = (max(abs(rates[c] - th[c]) for c in th)
                       if th else None)

            cell = {
                "k": k, "n": int(n),
                "label_rates": rates,
                "theory_rates": {str(c): v for c, v in th.items()} if th else None,
                "label_rate_max_dev": max_dev,
                "product_MI": obs_prod,
                "hint_MI": obs_hint,
                "hint_value": hint,
                "hint_ci95_boot": [float(ci_lo), float(ci_hi)],
                "hint_ci95_halfsample": [hs_lo, hs_hi],
                "H_unordered_labels": H_ulab,
                "residual_label_bits_given_pair": resid_bits,
                "distinct_primes_drawn": distinct_primes,
                "occupied_pair_codes": occ_pairs,
                "pool_primes_per_residue_class": len(pool) / (m - 1),
                "null_prod_mean": float(null_prod.mean()),
                "null_hint_mean": float(null_hint.mean()),
                "z_product": zscore(obs_prod, null_prod),
                "z_hint": zscore(obs_hint, null_hint),
                "ordered_label_MI": obs_ord,
                "wall_W": W_obs,
                "wall_null_mean": float(null_W.mean()),
                "wall_null_sd": float(null_W.std()),
                "wall_z": zscore(W_obs, null_W),
                "label_time_s": round(t_lab, 2),
            }
            results["dials"].setdefault(name, {})[f"k{k}"] = cell
            print(f"  k={k:2d} {name:24s} hint={hint:.4f} "
                  f"[{ci_lo:.4f},{ci_hi:.4f}] prod={obs_prod:.4f} "
                  f"z_hint={cell['z_hint']:.1f} wall_z={cell['wall_z']:+.2f} "
                  f"({time.time()-t1:.1f}s)", flush=True)

        print(f"k={k}: pool={len(pool)} draws={n} sieve={t_sieve:.1f}s "
              f"verify={t_ver:.1f}s total={time.time()-t0:.1f}s "
              f"[elapsed {time.time()-t_start:.1f}s]", flush=True)

    # ---------------- verdicts (pre-stated rules) ----------------
    results["verdicts"] = {}
    for name in DIALS:
        ks = sorted(int(key[1:]) for key in results["dials"][name])
        hints = [results["dials"][name][f"k{k}"]["hint_value"] for k in ks]
        med = float(np.median(hints))
        drift = max(abs(h - med) / abs(med) for h in hints) if med > 0 else float("inf")
        rho, pval = spearman_p(ks, hints)
        wall_ok = all(abs(results["dials"][name][f"k{k}"]["wall_z"]) < WALL_Z_TOL
                      for k in ks)
        stable = (drift < DRIFT_TOL) and (pval >= 0.05)
        results["verdicts"][name] = {
            "hints": hints, "median": med, "max_rel_drift": drift,
            "spearman_rho": rho, "spearman_p": pval,
            "wall_all_inside_null": wall_ok,
            "dial_verdict": "H1_stable" if stable else "H2_drift",
        }
    all_stable = all(v["dial_verdict"] == "H1_stable"
                     for v in results["verdicts"].values())
    all_wall = all(v["wall_all_inside_null"] for v in results["verdicts"].values())
    results["global_verdict"] = "H1_SIZE_STABLE" if all_stable else "H2_DRIFT"
    results["wall_invariant"] = ("HELD_at_every_size" if all_wall
                                 else "VIOLATED_somewhere")
    results["method_ledger"] = ledger_notes
    results["runtime_s"] = round(time.time() - t_start, 1)

    with open(OUT, "w") as fh:
        json.dump(results, fh, indent=1)
    print(f"\nGLOBAL: {results['global_verdict']}  "
          f"wall: {results['wall_invariant']}  "
          f"runtime {results['runtime_s']}s", flush=True)
    for name, v in results["verdicts"].items():
        print(f"  {name:24s} {v['dial_verdict']:9s} drift={v['max_rel_drift']:.3f} "
              f"rho={v['spearman_rho']:+.2f} p={v['spearman_p']:.3f} "
              f"wall_ok={v['wall_all_inside_null']}", flush=True)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""EXP606 KAPPA-SUFFICIENCY-SCALE -- PRE-REGISTRATION v2 (audit-amended BEFORE
any full-mode data existed; v1's smoke artifacts were DELETED as contaminated)

Questions (sharpening exp598c's H1 mechanism claim):
  C1 REPLICATION: on a FRESH population, does composition order carry the
     mixture increment? kappa_i = sum_k P(l_k | v_i) (expected number of
     distinct primes among {2,3,5,7} dividing v, from cell-grid marginals;
     the covariate that captured Delta = +0.114 alone in 598c).
  C2 SUFFICIENCY: does CELL IDENTITY add anything material BEYOND kappa?
  C3 SCALE: does the kappa law hold at bits in {72, 96, 128}?

Registered claims/bars (decided before any data):
  C1/C3 (per leg): H1_KAPPA_CARRIES iff
       Delta_kappa := adjR2(log-rate ~ 1+S_sqrt,400+kappa)
                     - adjR2(log-rate ~ 1+S_sqrt,400)          >= 0.05
       AND perm_p(kappa-row shuffle, 500 reps)                   <  0.01
       AND clean_control := max(y-shuffle deltas) < Delta_kappa;
     BORDERLINE_CONTROL_DIRTY iff dKappa>=0.05 AND perm_p<0.01 but NOT
       clean_control (above-bar effect the machinery cannot certify);
     if 0 < Delta_kappa < 0.05 WITH perm_p < 0.01 => SUBBAR_POSITIVE
       (reported, not claimed);
     NEGATIVE_DELTA_PERM_SUPPORTED iff dKappa<=0 WITH perm_p<0.01 (kappa
       ANTI-correlates with rate at this width -- informative, registered);
     NULL_AT_THIS_SCALE requires NO perm support AND machinery_ok;
     NULL_AT_THIS_SCALE requires no perm support AND machinery_ok :=
       |mean(ctrl)| < 0.01; failing machinery emits INVALID_MACHINERY
       instead (machinery gates every null/sufficiency reading);
     INCONCLUSIVE_LOWPOWER overrides ALL claims when the sizing ladder tops
       out below 300 projected mean hits/N.
  C2 (operative estimator stated FIRST): KAPPA_SUFFICIENT iff
       Delta_cells := adjR2(log-rate ~ 1+S+Dr) - adjR2(log-rate ~ 1+S+kappa)
       < 0.02 AND machinery_ok -- i.e. the full 15-column cell basis fails to
       beat the single-kappa model ON ADJUSTED R2 (the comparison that
       matters). NOTE the literal both-model form adjR2(1+S+kappa+Dr) -
       adjR2(1+S+Dr) is IDENTICALLY ZERO because kappa is a fixed linear
       combination of the D columns (span{kappa}+span{Dr}=span{Dr}); it is
       recorded here only to explain why the nested-increment phrasing is
       vacuous and the two-model adjusted-R2 comparison IS the sufficiency
       test. Descriptive: share of Dr-row shuffles (y,kappa held) reaching
       Delta_cells, plus y-shuffle range.
  CROSS-LEG AGGREGATION (registered pre-data):
     C3_SCALE_CONFIRMED iff H1_KAPPA_CARRIES fires in >= 2 of 3 legs;
     C3_SCALE_REFUTED iff <= 1 leg fires AND no leg shows SUBBAR_POSITIVE;
     else C3_SCALE_MIXED.
     SUFFICIENCY_CONFIRMED iff every non-lowpower leg yields
     kappa_sufficient True; REFUTED iff >= 2 non-lowpower legs yield False;
     else MIXED. Permutation/bootstrap seeds shared across legs are harmless
     (different data) -- disclosed.
  SLOPES: beta_kappa (fitted coefficient in 1+S+kappa) with an ORDINARY
     PAIRS bootstrap (one observation per N -- no clusters) percentile CI,
     B=800 full / B=100 smoke (smoke deviation disclosed), seed 607, per
     leg; cross-leg comparison DESCRIPTIVE (CI overlap only -- different
     bit widths are different rate regimes).
  SAMPLE SIZING (pre-declared adaptive rule, deterministic): each full leg
     first runs a PILOT (first 16 Ns, 2k hit samples/N, stream offset
     SEED + 37e6 + L*1e8 + i) estimating per-sample hit rate r_hat; n_hit is the
     smallest ladder value in {50k, 150k, 400k} with 512*r_hat*n_hit >= 300
     * 512 (projected mean >= 300 hits/N); if even 400k projects < 300, the
     leg RUNS at 400k and is flagged INCONCLUSIVE-LOWPOWER in verdicts
     BEFORE its full data is used for any claim. Cell grid fixed 50k/N.
  Population: fresh seeds bits->seed {96: 20261007, 72: 20261008,
     128: 20261009} (registry-verified unused), verbatim exp586
     make_semiprime rejection recursion + dedup, n_pool = 512 full / 32
     smoke. STREAM-DISTINCTNESS ASSERTED per leg: self-exclusion; ALL prior
     population seeds {20260824..28, 20260831, 20260902..07} regenerated
     prefix-complete (n=512) AT THE LEG'S BITS and asserted pairwise-disjoint
     vs the new pool and mutually disjoint (pools at other bit widths cannot
     contain this width's Ns, so matching-width regeneration covers all
     numeric collisions); stream bands SEED+{31e6,33e6,37e6}+i asserted
     above the TRUE prior ceiling computed from KNOWN_PRIOR_OFFSETS =
     {+7e6,+9e6} (legacy lineages) and {+17e6,+19e6} (exp598c FULL at seed
     20260907) -- v1 wrongly credited priors only +9e6 and collided ~412/512
     slots with 598c's streams; fixed by moving offsets and asserting
     SEED+min(offsets) > ceiling. 20260901 documented-excluded
     (bootstrap-only usage, never a population).
  Streams per N -- PER-LEG BAND STRIDE (audit must-fix #2: consecutive
     LEG_SEEDs differ by exactly 1, so identical offsets would make leg A's
     slot i+1 byte-identical to leg B's slot i): leg index L = {72:0, 96:1,
     128:2}; cell grid 50k (20k smoke) rng(SEED + 31e6 + L*1e8 + i); hit
     stream n_hit rng(SEED + 33e6 + L*1e8 + i); sizing pilot rng(SEED + 37e6
     + L*1e8 + i). hit := v = j^2-N fully 1e6-smooth via
     gcd-chain primorial(1e6); window t ~ U[0,65536) from j0=isqrt(N)+1.
  Calibration: Phipson-Smyth p-values (1 + #{>= obs})/(reps+1); perm seed
     606; bootstrap seed 607; conservative minimum perm_p = 1/501 clears the
     .01 bar. Shuffle-null caveat vs Berggren method-law: breaking the
     covariate<->y coupling IS the null under test here.
  VERIFICATION ARTIFACTS per leg: exp606_b{bits}_verify.npz saves y, S_dial,
     S_sens(unused this exp, kept for comparability), D16, kappa, hits,
     n_hit, keep, ref, perm_null_kappa, ctrl_null, perm_null_cells, d_obs
     fields, beta_kappa point; ns.txt decimal Ns. Standalone recomputation
     needs only the npz + call order documented HERE: per rep r,
     idx = prng.permutation(n_pool); idy = prng.permutation(n_pool);
     idc = prng.permutation(n_pool)  (alternating idx/idy/idc, single
     default_rng(PERM_SEED); idc drives perm_null_cells).
  Runtime: parallelized positional-seed workers (deterministic), sequential
     spot-check of first 8 Ns every mode.

Wall budget: ~5-15 min typical per leg; worst case ~26 min at the
400k-ladder b128 corner (~93us/draw gcd-dominated).
"""
import os
import sys
import json
import time
import random
import itertools
from itertools import combinations
import multiprocessing
import numpy as np
import gmpy2
from gmpy2 import mpz, next_prime
from concurrent.futures import ProcessPoolExecutor

OUT_DIR = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74"

SEED = None  # bound per-leg in main() (positional worker seeds read this global)

LEG_SEED = {96: 20261007, 72: 20261008, 128: 20261009}
# Registry scope (audit should-fix): semiprime-population seeds at bits>=64
# known to date. Bitlen<=52 families (20260990..20261000 exp503,
# 20261060..64 exp515, 20261200..02 exp541) are excluded BY THE
# MATCHING-WIDTH ARGUMENT (cannot contain 72/96/128-bit Ns). 20260825/
# 20260831 asserted-by-prior-registry (no generator usage found repo-wide).
PRIOR_POPULATION_SEEDS = [20260824, 20260825, 20260826, 20260827,
                          20260828, 20260831, 20260902, 20260903,
                          20260904, 20260905, 20260906, 20260907]
BITS_LIST = (72, 96, 128)
PRIME_LO, PRIME_HI = 3, 400
ALPHA_DIAL = 0.5
ALPHA_SENS = 1.0
CUT = 10 ** 6
T_WINDOW = 1 << 16
CELL_OFF, HIT_OFF, PILOT_OFF = 31_000_000, 33_000_000, 37_000_000
# v1 audit must-fix: v1 reused 598c's +17e6/+19e6 bands -- 598c ran FULL at
# seed 20260907 with exactly those offsets (n_pool=512), colliding ~412/512
# slots per leg (identical PCG64 streams => byte-identical t-draws applied
# to different Ns, correlating replication noise). Moved beyond ALL prior
# usage; prior offsets known in this program: {+7e6,+9e6} legacy,
# {+17e6,+19e6} exp598c.
KNOWN_PRIOR_OFFSETS = (7_000_000, 9_000_000, 17_000_000, 19_000_000)
NCELL_FULL, NCELL_SMOKE = 50000, 20000
NHIT_SMOKE = 12000
PILOT_NS, PILOT_HITS = 16, 2000
LADDER = [50000, 150000, 400000]
MIN_MEAN_HITS = 300
PERM_REPS_FULL, PERM_REPS_SMOKE = 500, 50
BOOT_B = 800
PERM_SEED, BOOT_SEED = 606, 607
H1_DR2, SUBBAR, MACHINERY_TOL = 0.05, 0.02, 0.01
SPOT_CHECK_NS = 8


# ---- exp586 population generator, VERBATIM (determinism-critical) ----------
def make_semiprime(rng, bits):
    half = bits // 2

    def gen():
        x = mpz(rng.getrandbits(half)) | (mpz(1) << (half - 1)) | 1
        return next_prime(x)

    p = gen(); q = gen()
    while q == p:
        q = gen()
    n = p * q
    if n.bit_length() != bits:
        return make_semiprime(rng, bits)
    lo = min(p, q); hi = max(p, q)
    if hi.bit_length() - lo.bit_length() > 2:
        return make_semiprime(rng, bits)
    return int(n), int(lo), int(hi)


def build_population(seed, n_pool, bits):
    rng = random.Random(seed)
    pools = []; seen = set()
    while len(pools) < n_pool:
        N, lo, hi = make_semiprime(rng, bits)
        if N in seen:
            continue
        seen.add(N)
        pools.append((N, lo, hi))
    return pools


def odd_primes(lo, hi):
    sieve = np.ones(hi + 1, dtype=bool); sieve[:2] = False
    for k in range(2, int(hi ** 0.5) + 1):
        if sieve[k]:
            sieve[k * k::k] = False
    return [int(p) for p in np.nonzero(sieve)[0] if p >= lo]


def count_matrix(Ns, primes):
    """c[i,j] = 1 iff jacobi(N_i mod p_j, p_j) == +1  (exp586 verbatim)."""
    C = np.zeros((len(Ns), len(primes)), dtype=np.float64)
    gj = gmpy2.jacobi
    for i, N in enumerate(Ns):
        m = mpz(N)
        for j, p in enumerate(primes):
            if gj(m % p, p) == 1:
                C[i, j] = 1.0
    return C


def primorial(bound):
    ps = odd_primes(3, bound)
    ps += [2]

    def prod(a, b):
        if b - a == 1:
            return mpz(ps[a])
        m = (a + b) // 2
        return prod(a, m) * prod(m, b)

    return prod(0, len(ps))


def is_smooth_chain(v, PRIM, gcd=gmpy2.gcd):
    v = mpz(v)
    if v == 1:
        return True
    g = gcd(v, PRIM)
    if g == 1:
        return False
    while v % g == 0:
        v //= g
    return v == 1


def cell_occupancy(N, j0, n_samples, rng, T=T_WINDOW):
    t = rng.integers(0, T, size=n_samples)
    base = (j0 * j0 - N)
    idx = np.zeros(n_samples, dtype=np.int64)
    for k, l in enumerate((2, 3, 5, 7)):
        vm = (base % l + (t % l) * ((2 * j0 + t) % l)) % l
        idx |= (vm == 0).astype(np.int64) << k
    cnt = np.bincount(idx, minlength=16)
    return cnt / float(n_samples)


_PRIM = None
ACTIVE_HIT_OFF = None  # bound per run in main(); fork inherits


def _worker_init():
    global _PRIM
    _PRIM = primorial(CUT)


def _worker_count(args):
    """Per-N hit count over n_hit draws; POSITIONAL seed => scheduling-free."""
    i, N, j0, n_hit = args
    rng = np.random.default_rng(SEED + ACTIVE_HIT_OFF + i)
    t = rng.integers(0, T_WINDOW, size=n_hit).tolist()
    smooth = is_smooth_chain
    hits = 0
    for tv in t:
        j = j0 + tv
        if smooth(j * j - N, _PRIM):
            hits += 1
    return i, hits


def ols_adj(X, y):
    beta, _, rank, _ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    n = len(y)
    ss_res = float(resid @ resid)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    adj = 1.0 - (1.0 - r2) * (n - 1) / (n - rank) if rank < n else float("nan")
    return r2, adj, rank, beta


def adj_only(X, y):
    _, adj, _, _ = ols_adj(X, y)
    return adj


def delta_adj(y, S, Z):
    ones = np.ones((len(y), 1))
    A = np.hstack([ones, S[:, None]])
    B = np.hstack([A, Z])
    return adj_only(B, y) - adj_only(A, y)


def main():
    global SEED
    t0 = time.time()
    bits = int(sys.argv[1]) if len(sys.argv) > 1 else 96
    mode = sys.argv[2] if len(sys.argv) > 2 else "smoke"
    assert bits in BITS_LIST
    global ACTIVE_HIT_OFF
    L = BITS_LIST.index(bits)          # per-leg band stride (audit MF#2)
    CELL_O = CELL_OFF + L * 100_000_000
    HIT_O = HIT_OFF + L * 100_000_000
    PILOT_O = PILOT_OFF + L * 100_000_000
    SEED = LEG_SEED[bits]
    ACTIVE_HIT_OFF = HIT_O
    smoke = mode == "smoke"
    n_pool = 32 if smoke else 512
    n_cell = NCELL_SMOKE if smoke else NCELL_FULL
    perm_reps = PERM_REPS_SMOKE if smoke else PERM_REPS_FULL

    # --- step 1: population + stream-distinctness ---------------------------
    assert SEED not in PRIOR_POPULATION_SEEDS, "self-exclusion violated"
    pools = build_population(SEED, n_pool, bits)
    Ns = [p[0] for p in pools]
    assert len(set(Ns)) == n_pool
    new_set = set(Ns)
    prior_union = set()
    for s in PRIOR_POPULATION_SEEDS:
        prior_ns = {p[0] for p in build_population(s, n_pool, bits)}
        assert not (prior_ns & new_set), f"N collision with lineage seed {s}"
        assert not (prior_ns & prior_union), f"lineages {s} not mutually disjoint"
        prior_union |= prior_ns
    hi_prior_band = (max(PRIOR_POPULATION_SEEDS)
                     + max(KNOWN_PRIOR_OFFSETS) + n_pool)
    lo_ours = SEED + min(CELL_O, HIT_O, PILOT_O)
    assert lo_ours > hi_prior_band, "stream band overlap vs priors"
    # cross-LEG pairwise disjointness (audit MF#2): consecutive LEG_SEEDs
    # differ by 1 -- without the *1e8 stride their bands would interleave
    leg_bands = []
    for _b, _sd in LEG_SEED.items():
        _o = BITS_LIST.index(_b) * 100_000_000
        leg_bands.append((_sd + _o + min(CELL_OFF, HIT_OFF, PILOT_OFF),
                          _sd + _o + max(CELL_OFF, HIT_OFF, PILOT_OFF) + n_pool))
    for (loA, hiA), (loB, hiB) in combinations(leg_bands, 2):
        assert hiA < loB or hiB < loA, "cross-leg stream band overlap"
    print(f"[b{bits}/{mode}] population {n_pool}, disjoint from "
          f"{len(PRIOR_POPULATION_SEEDS)} prior seeds ({len(prior_union)} Ns "
          f"@bits={bits}); bands clear (ours >= {lo_ours} > ceiling "
          f"{hi_prior_band}), wall={time.time()-t0:.1f}s", flush=True)

    # --- dial -----------------------------------------------------------------
    primes = odd_primes(PRIME_LO, PRIME_HI)
    C = count_matrix(Ns, primes)
    S_dial = C @ np.array([p ** (-ALPHA_DIAL) for p in primes])
    S_sens = C @ np.array([p ** (-ALPHA_SENS) for p in primes])

    # --- cell grids -----------------------------------------------------------
    D = np.zeros((n_pool, 16))
    for i, N in enumerate(Ns):
        j0 = int(gmpy2.isqrt(mpz(N))) + 1
        D[i] = cell_occupancy(N, j0, n_cell,
                              np.random.default_rng(SEED + CELL_O + i))
    ref = int(np.argmax(D.mean(axis=0)))
    keep = [c for c in range(16) if c != ref]
    Dr = D[:, keep]
    good = Dr.std(axis=0) > 0
    keep_eff = [keep[k] for k in range(len(keep)) if good[k]]
    Dr = Dr[:, good]
    marg = np.zeros((n_pool, 4))
    for k in range(4):
        bit_mask = np.array([(c >> k) & 1 for c in range(16)], dtype=bool)
        marg[:, k] = D[:, bit_mask].sum(axis=1)
    kappa = marg.sum(axis=1)

    # --- sample sizing pilot (full only; pre-declared ladder rule) ------------
    lowpower = False
    if smoke:
        n_hit = NHIT_SMOKE
    else:
        _worker_init()
        pilot_hits = []
        for i, N in enumerate(Ns[:PILOT_NS]):
            j0 = int(gmpy2.isqrt(mpz(N))) + 1
            rng = np.random.default_rng(SEED + PILOT_O + i)
            t = rng.integers(0, T_WINDOW, size=PILOT_HITS).tolist()
            h = sum(1 for tv in t if is_smooth_chain((j0 + tv) ** 2 - N, _PRIM))
            pilot_hits.append(h)
        r_hat = (sum(pilot_hits) + 0.5) / (PILOT_NS * PILOT_HITS)
        n_hit = LADDER[-1]
        for cand in LADDER:
            if r_hat * cand >= MIN_MEAN_HITS:
                n_hit = cand
                break
        lowpower = n_hit == LADDER[-1] and r_hat * n_hit < MIN_MEAN_HITS
        pilot_r_hat = float(r_hat)
        print(f"[b{bits}/full] pilot r_hat={r_hat:.3e}/sample -> n_hit={n_hit}"
              f"{' INCONCLUSIVE-LOWPOWER PROJECTED' if lowpower else ''}",
              flush=True)

    # --- hit streams (parallel, positional seeds) -----------------------------
    jobs = [(i, N, int(gmpy2.isqrt(mpz(N))) + 1, n_hit) for i, N in enumerate(Ns)]
    hits = np.zeros(n_pool, dtype=np.int64)
    if smoke:
        _worker_init()
        for args in jobs:
            i, h = _worker_count(args)
            hits[i] = h
    else:
        workers = max(2, min(12, (os.cpu_count() or 4) - 1))
        try:
            with ProcessPoolExecutor(max_workers=workers,
                                     initializer=_worker_init,
                                     mp_context=multiprocessing.get_context(
                                         "fork")) as ex:
                done = 0
                for i, h in ex.map(_worker_count, jobs, chunksize=8):
                    hits[i] = h
                    done += 1
                    if done % 64 == 0:
                        print(f"  [b{bits}] {done}/{n_pool} hit streams, "
                              f"wall={time.time()-t0:.1f}s", flush=True)
        except Exception as e:
            print(f"  [b{bits}] pool failed ({e!r}); sequential", flush=True)
            _worker_init()
            for args in jobs:
                i, h = _worker_count(args)
                hits[i] = h

    # --- spot-check ------------------------------------------------------------
    _worker_init()
    for i, N, j0, nh in jobs[:SPOT_CHECK_NS]:
        assert _worker_count((i, N, j0, nh))[1] == int(hits[i]), f"mismatch {i}"

    y = np.log((hits.astype(np.float64) + 0.5) / float(n_hit))

    # --- nested models ----------------------------------------------------------
    ones = np.ones((n_pool, 1))
    kap = kappa.reshape(-1, 1)
    X_dial = np.hstack([ones, S_dial[:, None]])
    X_kap = np.hstack([ones, S_dial[:, None], kap])
    X_cells = np.hstack([ones, S_dial[:, None], Dr])
    _, adj_dial, rk_dial, _ = ols_adj(X_dial, y)
    _, adj_kappa, rk_kappa, _ = ols_adj(X_kap, y)
    _, adj_cells, rk_cells, _ = ols_adj(X_cells, y)
    d_kappa = adj_kappa - adj_dial
    d_cells_beyond = adj_cells - adj_kappa      # == adjR2(dial+cells)-adjR2(dial+kappa)
    Xk = np.hstack([ones, S_dial[:, None], kap])
    beta_kappa = float(np.linalg.lstsq(Xk, y, rcond=None)[0][2])

    # --- calibration --------------------------------------------------------------
    prng = np.random.default_rng(PERM_SEED)
    perm_null_kappa = np.empty(perm_reps)
    ctrl_null = np.empty(perm_reps)
    perm_null_cells = np.empty(perm_reps)
    for r in range(perm_reps):
        idx = prng.permutation(n_pool)
        perm_null_kappa[r] = delta_adj(y, S_dial, kap[idx])
        idy = prng.permutation(n_pool)
        ctrl_null[r] = delta_adj(y[idy], S_dial, kap)
        idc = prng.permutation(n_pool)
        perm_null_cells[r] = adj_only(
            np.hstack([ones, S_dial[:, None], kap, Dr[idc]]), y) - adj_kappa
    p_perm = float((1 + np.sum(perm_null_kappa >= d_kappa)) / (perm_reps + 1))
    p_ctrl = float((1 + np.sum(ctrl_null >= d_kappa)) / (perm_reps + 1))
    clean_control = bool(float(ctrl_null.max()) < d_kappa)
    machinery_ok = bool(abs(float(ctrl_null.mean())) < MACHINERY_TOL)
    cells_share_ge = float(np.mean(perm_null_cells >= d_cells_beyond))

    # --- bootstrap slope CI ---------------------------------------------------------
    boot = np.empty(BOOT_B if not smoke else 100)
    brng = np.random.default_rng(BOOT_SEED)
    for b in range(len(boot)):
        idx = brng.integers(0, n_pool, n_pool)
        boot[b] = float(np.linalg.lstsq(Xk[idx], y[idx], rcond=None)[0][2])
    ci_lo, ci_hi = np.quantile(boot, [0.025, 0.975])

    # --- verdicts (registered tree v2; audit must-fix: explicit branches for
    # above-bar-dirty-control and machinery/lowpower gating) -------------------
    ctrl_share = float(np.mean(ctrl_null >= d_kappa))
    if smoke:
        fired = "SMOKE_NON_EVIDENTIARY"
    elif lowpower:
        fired = "INCONCLUSIVE_LOWPOWER"      # claims suppressed pre-data rule
    elif d_kappa >= H1_DR2 and p_perm < 0.01 and clean_control:
        fired = "H1_KAPPA_CARRIES"
    elif d_kappa >= H1_DR2 and p_perm < 0.01:
        fired = "BORDERLINE_CONTROL_DIRTY"   # above bar but obs inside y-null range
    elif d_kappa > 0 and p_perm < 0.01:
        fired = "SUBBAR_POSITIVE"            # strictly below the 0.05 bar
    elif d_kappa <= 0 and p_perm < 0.01:
        fired = "NEGATIVE_DELTA_PERM_SUPPORTED"   # kappa ANTI-correlates here
    elif machinery_ok:
        fired = "NULL_AT_THIS_SCALE"
    else:
        fired = "INVALID_MACHINERY"
    sufficiency = ((d_cells_beyond < SUBBAR and machinery_ok)
                   if (not smoke and not lowpower and machinery_ok) else None)
    sens_d = delta_adj(y, S_sens, kap)

    result = {
        "config": {
            "exp": "606", "codename": "KAPPA-SUFFICIENCY-SCALE",
            "mode": mode, "bits": bits, "master_seed": SEED,
            "prior_seeds_checked_at_this_bits": PRIOR_POPULATION_SEEDS,
            "n_pool": n_pool, "cell_samples_per_N": n_cell,
            "hit_samples_per_N": n_hit, "sizing_ladder": LADDER,
            "stream_offsets_used": {"cell": CELL_O, "hit": HIT_O,
                                    "pilot": PILOT_O, "leg_stride_index": L},
            "pilot_r_hat": (pilot_r_hat if not smoke else None),
            "min_mean_hits_target": MIN_MEAN_HITS,
            "lowpower_projected": bool(lowpower),
            "j_window_t": [0, T_WINDOW], "smooth_cut": CUT,
            "perm_reps": perm_reps, "perm_seed": PERM_SEED,
            "boot_B": int(len(boot)), "boot_seed": BOOT_SEED,
            "thresholds": {"H1_dR2": H1_DR2, "sufficiency_bar": SUBBAR,
                           "machinery_tol": MACHINERY_TOL},
            "regen_hash_status": (
                "CONDITIONAL: no canonical regeneration hash exists in this "
                "lineage; distinctness asserted per leg at matching bits vs "
                "regenerated prior pools; decimal N vectors ARE stored in "
                "*_ns.txt sidecars (auditable byte-reproduction)"),
        },
        "stats": {
            "adjR2_dial": round(float(adj_dial), 6),
            "adjR2_kappa": round(float(adj_kappa), 6),
            "adjR2_cells": round(float(adj_cells), 6),
            "delta_kappa": round(float(d_kappa), 6),
            "delta_cells_beyond_kappa": round(float(d_cells_beyond), 6),
            "beta_kappa": round(beta_kappa, 6),
            "beta_ci95": [round(float(ci_lo), 6), round(float(ci_hi), 6)],
            "perm_p_kappa": p_perm,
            "ctrl_ps_p_vs_obs": p_ctrl,
            "ctrl_share_ge_obs": ctrl_share,
            "rank_models": {"dial": int(rk_dial), "kappa": int(rk_kappa),
                            "cells": int(rk_cells)},
            "ctrl_null_max": round(float(ctrl_null.max()), 6),
            "clean_control": clean_control,
            "machinery_ok": machinery_ok,
            "cells_shuffle_share_ge": cells_share_ge,
            "sensitivity_alpha1_delta": round(float(sens_d), 6),
            "mean_hits_per_N": round(float(hits.mean()), 1),
            "min_hits_per_N": int(hits.min()),
            "max_hits_per_N": int(hits.max()),
            "mean_kappa": round(float(kappa.mean()), 4),
        },
        "verdicts": {
            "rule": ("H1_KAPPA_CARRIES iff dKappa>=0.05 AND perm_p<0.01 AND "
                     "clean_control; BORDERLINE_CONTROL_DIRTY iff dKappa>=0.05 "
                     "AND perm_p<0.01 AND NOT clean_control; SUBBAR_POSITIVE "
                     "iff 0<dKappa<0.05 AND perm_p<0.01; NULL_AT_THIS_SCALE if "
                     "no perm support and machinery_ok; INVALID_MACHINERY "
                     "otherwise; INCONCLUSIVE_LOWPOWER overrides all claims "
                     "when the sizing ladder tops out below 300 mean hits/N; "
                     "KAPPA_SUFFICIENT iff dCellsBeyond<0.02 AND machinery_ok"),
            "fired": fired,
            "kappa_sufficient": sufficiency,
            "lowpower_flag": bool(lowpower),
        },
        "honest_notes": [
            "kappa is assembled from the SAME cell grid as Dr (independent of "
            "the hit stream y, but sharing the cell grid's sampling noise with "
            "the cells arm); the C2 comparison is exactly a df-penalty question "
            "because span{kappa} subset span{Dr}.",
            "Sizing pilot (full legs) is pre-declared in the header; its 2k/N "
            "draws use a distinct stream (+37e6+L*1e8) and feed ONLY n_hit choice; "
            "r_hat persisted in config.pilot_r_hat for auditability.",
            "Cross-bit slope comparisons are descriptive (different rate "
            "regimes); no cross-leg pooling.",
            "Regen hash CONDITIONAL; tester class matched to 598b/598c, "
            "absolute rates internally consistent only.",
            f"Spot-check covers first {SPOT_CHECK_NS} Ns (positional seeds + "
            "ordered ex.map index the rest).",
            "Rank note: D rows sum to exactly 1, so intercept+Dr carries an "
            "exact-in-exact-arithmetic dependence at machine epsilon; lstsq "
            "rcond=None classifies designs full-rank and the df penalty "
            "counts one algebraically-free parameter -- the error CANCELS "
            "within every reported delta (both arms share the Dr block); "
            "model ranks recorded in stats.rank_models.",
            "SIGN EXPECTATION (pre-stated): NONE registered -- H1_KAPPA_CARRIES "
            "is sign-agnostic in Delta_kappa; v2 smokes suggested a NEGATIVE "
            "beta_kappa at all three widths (richer small-prime composition "
            "associating with LOWER window rate); beta sign is recorded and "
            "interpretable either way, never gated on.",
        ],
        "wall_s": round(time.time() - t0, 2),
    }

    tag = f"_b{bits}" + ("_smoke" if smoke else "")
    out_json = os.path.join(OUT_DIR, f"exp606{tag}_result.json")
    with open(out_json, "w") as f:
        json.dump(result, f, indent=1)

    npz_path = os.path.join(OUT_DIR, f"exp606{tag}_verify.npz")
    np.savez_compressed(
        npz_path, y=y, S_dial=S_dial, S_sens=S_sens, D16=D, kappa=kappa,
        hits=hits, keep=np.array(keep_eff), ref=np.array([ref]),
        perm_null_kappa=perm_null_kappa, ctrl_null=ctrl_null,
        perm_null_cells=perm_null_cells,
        d_kappa=np.array([d_kappa]), d_cells=np.array([d_cells_beyond]),
        n_hit=np.array([n_hit]), n_pool=np.array([n_pool]),
        perm_seed=np.array([PERM_SEED]), bits=np.array([bits]),
        master_seed=np.array([SEED]))
    with open(os.path.join(OUT_DIR, f"exp606{tag}_ns.txt"), "w") as f:
        f.write("\n".join(str(n) for n in Ns) + "\n")

    print(json.dumps({"bits": bits, "fired": fired,
                      "kappa_sufficient": sufficiency,
                      "delta_kappa": result["stats"]["delta_kappa"],
                      "delta_cells_beyond_kappa": result["stats"]["delta_cells_beyond_kappa"],
                      "perm_p": p_perm, "ctrl_null_max":
                      result["stats"]["ctrl_null_max"],
                      "clean_control": clean_control,
                      "beta_kappa": result["stats"]["beta_kappa"],
                      "beta_ci95": result["stats"]["beta_ci95"],
                      "wall_s": result["wall_s"], "out": out_json}), flush=True)


if __name__ == "__main__":
    main()

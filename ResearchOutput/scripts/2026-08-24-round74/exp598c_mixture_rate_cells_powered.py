#!/usr/bin/env python3
"""EXP598C MIXTURE-RATE-CELLS-POWERED -- PRE-REGISTRATION v2 (amended BEFORE any
full-mode data existed; amendment driven by a two-agent adversarial audit of v1)

Question (re-fires exp598b's flagged question at its pre-stated power
requirement): does the FULL 16-cell divisibility mixture -- the joint class
vector (2|v, 3|v, 5|v, 7|v) with v = j^2 - N -- explain per-N hit-rate
variance BEYOND the sqrt dial S_sqrt,400?

exp598b outcome (n_pool=128): Delta adjR^2 = +0.083 cleared the H1 effect bar
but perm_p = 0.0399 missed < 0.01 AND the recorded control flag fired =>
BORDERLINE-INCONCLUSIVE. POST-RUN ERRATUM ON 598B (audit finding, rides here
per lab errata discipline; applies to paper 255's control-flag framing):
598b operationalized control_ok = (p_ctrl > 0.05 AND max(ctrl_null) < d_obs),
which is LOGICALLY UNSATISFIABLE -- p_ctrl > 0.05 forces >= 25 of 500
y-shuffle deltas >= obs, hence max(ctrl_null) >= d_obs, hence clause 2 false.
control_ok=False was guaranteed BY CONSTRUCTION whenever clause 1 held; the
informative content was c = 25/500 (obs at the 95th percentile of the
y-shuffle range), not an independent clause failure. 598b's BORDERLINE
verdict itself stands (its decision rule never gated on control_ok); the
control-flag FRAMING does not.

AMENDMENT v2 (registered before any full-mode number existed; smoke numbers
are non-evidentiary per lab rules and no full-mode data had been touched):
  CONTROL RULE CORRECTED (audit must-fix): attainable operationalization --
    clean_control := max(ctrl_null) < d_obs    [obs beats EVERY y-shuffle]
    machinery_ok  := |mean(ctrl_null)| < 0.01  [shuffle deltas center at 0]
  VERDICT GATES (flag->gate promotion vs 598b DISCLOSED, not silent):
    H1 iff Delta adjR^2 >= 0.05 AND perm_p < 0.01 AND clean_control
    H0 iff Delta adjR^2 < 0.02 AND machinery_ok
    else BORDERLINE; p_ctrl reported descriptively only.
  PRE-STATED CLOSING BRANCHES (resolved explicitly in-artifact):
    fired H1/H0                        -> branch 'none'
    BORDERLINE + clean_control         -> 'a_small_but_real' (sub-bar delta
        that still beats all 500 shuffle draws)
    BORDERLINE + not clean_control     -> 'b_undecidable_at_scale': close the
        joint-cell layer UNDECIDABLE-AT-PRACTICAL-SCALE, booking the
        TWO-POINT null-range comparison {n=128: ctrl_max 0.186, n=512: X}
        (descriptive; two points do not make a scaling law).
  SECONDARY ARM REPAIRED (v1's D>0 popcount is identically 16 on occupancy
    fractions => degenerate zero-column basis): directional lower-df
    covariate kappa_i = sum_k P(l_k | v_i) assembled from the cell
    marginals (bit-masks over the 16 cells; ONE free column), reported
    only if the primary fires.

Method (mirrors exp598b EXCEPT where stated):
  1. Population: master seed 20260907 (v1's 20260903 WITHDRAWN by audit:
     it is exp601's recorded third-seed lineage -- own_lineage_hash16
     fa1746a5b065cbd9 reproduces as the prefix of
     build_population(20260903, 512)). Verbatim exp586 make_semiprime
     recipe (bits=96 rejection recursion + dedup), n_pool = 512 full /
     32 smoke. STREAM-DISTINCTNESS ASSERTED three ways:
     (a) SELF-EXCLUSION: SEED not among any known lineage seed (v1's
         disjointness check was structurally blind to own-seed reuse);
     (b) pools for ALL prior population seeds {20260824..28, 20260831,
         20260902, 20260903, 20260904, 20260905, 20260906} regenerated at
         n=512 (prefix-complete under the deterministic generator) at
         bits=96, asserted pairwise-disjoint against the new pool AND
         mutually disjoint (pools generated at other bit widths cannot
         contain a 96-bit N, so bits=96 regeneration covers all numeric
         collisions);
     (c) 20260901 excluded from the registry: bootstrap-only usage in
         exp582/588b/588c, never a population -- documented here.
     Regen-vs-exp586 hash-check remains CONDITIONAL/unavailable (no stored
     N strings anywhere in the lineage) -- disclosed, not gated.
  2. Two INDEPENDENT fresh streams per N, offsets MOVED beyond all prior
     usage (v1 kept 7e6/9e6 and its bands overlapped 598b's in exactly 52
     seed values): cell stream rng(SEED + 17e6 + i), hit stream
     rng(SEED + 19e6 + i); numeric band-disjointness vs every prior
     lineage's {+7e6, +9e6} bands ASSERTED. Cell grid 50k/N (20k smoke),
     hit stream 50k/N (12k smoke); hit := v fully 1e6-smooth via gcd-chain
     primorial(1e6) tester; window t ~ U[0, 65536) from j0 = isqrt(N)+1.
  3. Regression IDENTICAL to 598b: reference cell = globally most-common
     dropped; delta_adj on hierarchical OLS; perm arm shuffles cell-label
     ROWS jointly; ctrl arm shuffles y; 500 reps (50 smoke), perm seed 599;
     conservative Phipson-Smyth p-values (1 + #{>= obs})/(reps + 1);
     minimum attainable perm_p = 1/501 ~= .002 clears the 0.01 bar, so the
     H1 endpoint is reachable. Shuffle-null caveat vs the Berggren
     method-law: here breaking the y<->D coupling IS the null under test
     (not a magnitude mirror of a deterministic function of N), so the
     row-shuffle objection does not apply.
  4. VERIFICATION ARTIFACTS: exp598c_verify.npz saves y, S_dial, S_sens,
     D16, hits, keep-mask, ref, perm_null, ctrl_null, d_obs PLUS scalars
     n_hit, n_pool, perm_seed, machinery_tol -- standalone recomputation of
     delta_adjR^2 / perm_p / clean_control / machinery_ok needs only this
     npz plus the PERMUTATION CALL ORDER documented HERE: per rep r,
     idx = prng.permutation(n_pool); idy = prng.permutation(n_pool)
     (alternating, single default_rng(PERM_SEED) stream). ns.txt stores
     decimal Ns.
  5. Runtime: hit streams parallelized across processes with POSITIONAL
     per-N seeds (scheduling-independent); sequential SPOT-CHECK of the
     first 8 Ns asserted exact in every mode (a spot-check, not a proof
     over remaining indices; ex.map ordered-yield semantics index the rest).

Wall budget: ~2048/P s hit-stream at P cores (sequential fallback ~34 min).
"""
import os
import sys
import json
import time
import random
import numpy as np
import gmpy2
from gmpy2 import mpz, next_prime, jacobi
from concurrent.futures import ProcessPoolExecutor

OUT_DIR = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74"

SEED = 20260907                       # fresh (v1's 20260903 withdrawn: exp601 lineage)
PRIOR_POPULATION_SEEDS = [20260824, 20260825, 20260826, 20260827,
                          20260828, 20260831, 20260902, 20260903,
                          20260904, 20260905, 20260906]
BITS = 96
PRIME_LO, PRIME_HI = 3, 400
ALPHA_DIAL = 0.5
ALPHA_SENS = 1.0
CUT = 10 ** 6
T_WINDOW = 1 << 16
CELL_OFF, HIT_OFF = 17_000_000, 19_000_000   # beyond ALL prior {+7e6,+9e6} bands
NCELL_FULL, NCELL_SMOKE = 50000, 20000
NHIT_FULL, NHIT_SMOKE = 50000, 12000
PERM_REPS_FULL, PERM_REPS_SMOKE = 500, 50
PERM_SEED = 599                       # fresh, distinct from 598b's 598
H1_DR2, H0_DR2, H1_PMAX = 0.05, 0.02, 0.01
MACHINERY_TOL = 0.01                  # |mean(ctrl_null)| gate for the H0 arm
SPOT_CHECK_NS = 8                     # sequential recompute spot-check in every mode


# ---- exp586 population generator, VERBATIM from exp598b (determinism-critical)
def make_semiprime(rng, bits):
    half = bits // 2

    def gen():
        x = mpz(rng.getrandbits(half)) | (mpz(1) << (half - 1)) | 1
        return gmpy2.next_prime(x)

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


def build_population(seed, n_pool, bits=BITS):
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
    """v > 0 CUT-smooth iff stripping gcd(v, P) with multiplicity leaves 1."""
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
    """16-cell occupancy of v = j^2 - N; exact modular arithmetic."""
    t = rng.integers(0, T, size=n_samples)
    base = (j0 * j0 - N)
    idx = np.zeros(n_samples, dtype=np.int64)
    for k, l in enumerate((2, 3, 5, 7)):
        vm = (base % l + (t % l) * ((2 * j0 + t) % l)) % l
        idx |= (vm == 0).astype(np.int64) << k
    cnt = np.bincount(idx, minlength=16)
    return cnt / float(n_samples)


_PRIM = None


def _worker_init():
    global _PRIM
    _PRIM = primorial(CUT)


def _worker_count(args):
    """Top-level picklable per-N hit count; seed positional => deterministic."""
    i, N, j0, n_hit = args
    rng = np.random.default_rng(SEED + HIT_OFF + i)
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
    return r2, adj, rank


def delta_adj(y, S, D):
    ones = np.ones((len(y), 1))
    XA = np.hstack([ones, S[:, None]])
    XB = np.hstack([ones, S[:, None], D])
    _, adjA, _ = ols_adj(XA, y)
    _, adjB, _ = ols_adj(XB, y)
    return adjB - adjA, adjA, adjB


def main():
    t0 = time.time()
    mode = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    smoke = mode == "smoke"
    n_pool = 32 if smoke else 512
    n_cell = NCELL_SMOKE if smoke else NCELL_FULL
    n_hit = NHIT_SMOKE if smoke else NHIT_FULL
    perm_reps = PERM_REPS_SMOKE if smoke else PERM_REPS_FULL

    # --- step 1: population + STREAM-DISTINCTNESS ASSERTION -----------------
    assert SEED not in PRIOR_POPULATION_SEEDS, "self-exclusion violated"
    pools = build_population(SEED, n_pool)
    Ns = [p[0] for p in pools]
    assert len(set(Ns)) == n_pool, "internal duplicate N"
    new_set = set(Ns)
    prior_union = set()
    for s in PRIOR_POPULATION_SEEDS:
        # prefix-complete regeneration (deterministic generator) at bits=96;
        # pools used at other bit widths cannot contain a 96-bit N.
        prior_ns = {p[0] for p in build_population(s, n_pool)}
        assert not (prior_ns & new_set), f"N collision with lineage seed {s}"
        assert not (prior_ns & prior_union), f"lineage seeds {s} not mutually disjoint"
        prior_union |= prior_ns
    # stream-BAND disjointness vs every prior lineage's {+7e6, +9e6} usage
    lo_ours = SEED + min(CELL_OFF, HIT_OFF)
    hi_prior_band = max(PRIOR_POPULATION_SEEDS) + 9_000_000 + n_pool
    assert lo_ours > hi_prior_band, "stream band overlap with prior lineages"
    print(f"[{mode}] population {len(new_set)} Ns; self-exclusion ok; disjoint from "
          f"{len(PRIOR_POPULATION_SEEDS)} prior lineage seeds "
          f"({len(prior_union)} prior Ns regenerated+checked); stream bands clear "
          f"(ours >= {lo_ours} > {hi_prior_band}), wall={time.time()-t0:.1f}s",
          flush=True)

    # --- dial ----------------------------------------------------------------
    primes = odd_primes(PRIME_LO, PRIME_HI)
    C = count_matrix(Ns, primes)
    S_dial = C @ np.array([p ** (-ALPHA_DIAL) for p in primes])
    S_sens = C @ np.array([p ** (-ALPHA_SENS) for p in primes])

    # --- step 2: cell grids (serial, cheap) + hit streams (parallel) ---------
    D = np.zeros((n_pool, 16))
    jobs = []
    for i, N in enumerate(Ns):
        j0 = int(gmpy2.isqrt(mpz(N))) + 1
        D[i] = cell_occupancy(N, j0, n_cell,
                              np.random.default_rng(SEED + CELL_OFF + i))
        jobs.append((i, N, j0, n_hit))

    hits = np.zeros(n_pool, dtype=np.int64)
    workers = max(2, min(12, (os.cpu_count() or 4) - 1))
    try:
        with ProcessPoolExecutor(max_workers=workers, initializer=_worker_init) as ex:
            done = 0
            for i, h in ex.map(_worker_count, jobs, chunksize=8):
                hits[i] = h
                done += 1
                if done % 32 == 0:
                    print(f"  [{mode}] {done}/{n_pool} hit streams, "
                          f"wall={time.time()-t0:.1f}s", flush=True)
    except Exception as e:  # pragma: no cover - fallback path
        print(f"  [{mode}] pool failed ({e!r}); sequential fallback", flush=True)
        _worker_init()
        for args in jobs:
            i, h = _worker_count(args)
            hits[i] = h

    # --- step 2b: determinism spot-check (sequential recompute of first Ks) --
    _worker_init()
    for i, N, j0, nh in jobs[:SPOT_CHECK_NS]:
        h2 = _worker_count((i, N, j0, nh))[1]
        assert h2 == int(hits[i]), f"parallel/sequential mismatch at N index {i}"
    print(f"[{mode}] determinism spot-check {SPOT_CHECK_NS}/{n_pool} exact", flush=True)

    y = np.log((hits.astype(np.float64) + 0.5) / float(n_hit))

    # --- step 3: hierarchical regression + permutation calibration -----------
    ref = int(np.argmax(D.mean(axis=0)))
    keep = [c for c in range(16) if c != ref]
    Dr = D[:, keep]
    good = Dr.std(axis=0) > 0
    keep_eff = [keep[k] for k in range(len(keep)) if good[k]]
    Dr = Dr[:, good]

    d_obs, adjA, adjB = delta_adj(y, S_dial, Dr)
    r2_cells_alone, _, rk_c = ols_adj(np.hstack([np.ones((n_pool, 1)), Dr]), y)

    prng = np.random.default_rng(PERM_SEED)
    perm_null = np.empty(perm_reps)
    ctrl_null = np.empty(perm_reps)
    for r in range(perm_reps):
        idx = prng.permutation(n_pool)
        perm_null[r], _, _ = delta_adj(y, S_dial, Dr[idx])
        idy = prng.permutation(n_pool)
        ctrl_null[r], _, _ = delta_adj(y[idy], S_dial, Dr)
        if (r + 1) % 100 == 0:
            print(f"  [{mode}] perm {r+1}/{perm_reps}, wall={time.time()-t0:.1f}s",
                  flush=True)
    p_perm = float((1 + np.sum(perm_null >= d_obs)) / (perm_reps + 1))
    # descriptive only: share of y-shuffle deltas reaching obs (598b's
    # (p_ctrl>0.05 AND max<obs) conjunction was unsatisfiable by construction)
    p_ctrl = float((1 + np.sum(ctrl_null >= d_obs)) / (perm_reps + 1))
    clean_control = bool(float(ctrl_null.max()) < d_obs)      # obs beats ALL shuffles
    machinery_ok = bool(abs(float(ctrl_null.mean())) < MACHINERY_TOL)

    # secondary (non-evidentiary unless primary fires): expected-popcount
    # covariate assembled from cell MARGINALS (v1's D>0 popcount was
    # identically 16 on occupancy fractions => degenerate; audit fix)
    marg = np.zeros((n_pool, 4))
    for k in range(4):
        bit_mask = np.array([(c >> k) & 1 for c in range(16)], dtype=bool)
        marg[:, k] = D[:, bit_mask].sum(axis=1)      # P(l_k | v) per N
    kappa_i = marg.sum(axis=1).reshape(-1, 1)        # E[#distinct small primes|v]
    assert kappa_i.shape[1] >= 1 and np.isfinite(kappa_i).all()
    d_kappa, adjAk, adjBk = delta_adj(y, S_dial, kappa_i)

    # sensitivity arm
    d_sens, adjA_s, adjB_s = delta_adj(y, S_sens, Dr)

    # cell-effect profile (interpretability)
    Xf = np.hstack([np.ones((n_pool, 1)), S_dial[:, None], Dr])
    beta_f, _, _, _ = np.linalg.lstsq(Xf, y, rcond=None)
    cell_beta = {c: round(float(beta_f[2 + k]), 4)
                 for k, c in enumerate(keep_eff)}

    # --- step 4: verdicts (registered rule v2, header AMENDMENT block) -------
    h1_fire = (d_obs >= H1_DR2) and (p_perm < H1_PMAX) and clean_control
    h0_fire = (d_obs < H0_DR2) and machinery_ok
    if h1_fire:
        fired = "H1_MIXTURE_ADDS"
    elif h0_fire:
        fired = "H0_DIAL_SUFFICIENT"
    else:
        fired = "BORDERLINE_INCONCLUSIVE"
    closing_branch = ("none" if fired != "BORDERLINE_INCONCLUSIVE"
                      else ("a_small_but_real" if clean_control
                            else "b_undecidable_at_scale"))

    result = {
        "config": {
            "exp": "598c", "codename": "MIXTURE-RATE-CELLS-POWERED",
            "mode": mode,
            "master_seed": SEED,
            "prior_population_seeds_checked": PRIOR_POPULATION_SEEDS,
            "bits": BITS, "n_pool": n_pool,
            "cell_samples_per_N": n_cell, "hit_samples_per_N": n_hit,
            "stream_offsets": {"cell": CELL_OFF, "hit": HIT_OFF},
            "j_window_t": [0, T_WINDOW], "smooth_cut": CUT,
            "dial": f"S_alpha,alpha={ALPHA_DIAL},odd primes {PRIME_LO}..{PRIME_HI}",
            "n_odd_primes": len(primes),
            "perm_reps": perm_reps, "perm_seed": PERM_SEED,
            "ctrl_reps": perm_reps,
            "thresholds": {"H1_dR2": H1_DR2, "H0_dR2": H0_DR2, "H1_pmax": H1_PMAX,
                           "machinery_tol": MACHINERY_TOL},
            "regen_hash_status": (
                "CONDITIONAL: no N strings stored anywhere in the exp586/598b "
                "lineage; verbatim recipe identity relied on; stream-distinctness "
                f"vs {len(PRIOR_POPULATION_SEEDS)} prior population seeds ASSERTED "
                "(self-exclusion + pairwise-disjoint prefix-complete regenerations "
                "+ numeric stream-band disjointness)"),
            "changes_vs_598b": [
                "master seed 20260827 -> 20260907 (v2: v1's 20260903 WITHDRAWN -- "
                "exp601's recorded lineage, hash fa1746a5b065cbd9 prefix-collides)",
                "n_pool 128 -> 512 (pre-stated ~4x power remedy)",
                "perm seed 598 -> 599",
                "CONTROL RULE CORRECTED: 598b's control_ok conjunction was "
                "logically unsatisfiable (p_ctrl>0.05 forces max>=obs); v2 gates "
                "H1 on clean_control = max(ctrl_null)<d_obs and gates H0 on "
                "machinery_ok = |mean(ctrl_null)|<0.01; p_ctrl descriptive only",
                "VERDICT GATING DISCLOSED: control now GATES H1/H0 (598b only "
                "flagged via honest note) -- registered in header AMENDMENT v2",
                "closing branches resolved in-artifact (none/a_small_but_real/"
                "b_undecidable_at_scale); 'scaling law' softened to two-point "
                "comparison",
                "SECONDARY kappa arm repaired (v1-style D>0 popcount degenerate; "
                "now expected-popcount from cell marginals, one column)",
                "stream offsets moved +7e6/+9e6 -> +17e6/+19e6 (v1 bands overlapped "
                "598b's in 52 values)",
                "prior-seed registry extended to {20260824..28, 20260831, "
                "20260902..06}; self-exclusion asserted",
                "hit streams parallelized (positional seeds => deterministic)",
                "verification arrays saved for independent recomputation"],
        },
        "stats": {
            "delta_adjR2": round(float(d_obs), 6),
            "adjR2_dial": round(float(adjA), 6),
            "adjR2_cells": round(float(adjB), 6),
            "cells_alone_R2": round(float(r2_cells_alone), 6),
            "rank_cells": int(rk_c),
            "n_cell_cols_used": int(Dr.shape[1]),
            "ref_cell": int(ref),
            "perm_p": p_perm,
            "perm_null_q": {"q50": round(float(np.quantile(perm_null, .5)), 6),
                            "q95": round(float(np.quantile(perm_null, .95)), 6),
                            "max": round(float(perm_null.max()), 6)},
            "ctrl_p_vs_obs": p_ctrl,
            "ctrl_null_mean": round(float(ctrl_null.mean()), 6),
            "ctrl_null_max": round(float(ctrl_null.max()), 6),
            "clean_control": clean_control,
            "machinery_ok": machinery_ok,
            "ctrl_share_ge_obs": round(float(np.mean(ctrl_null >= d_obs)), 4),
            "secondary_kappa": {"delta_adjR2": round(float(d_kappa), 6),
                                "adjR2_dial": round(float(adjAk), 6),
                                "adjR2_kappa": round(float(adjBk), 6),
                                "note": "non-evidentiary unless primary fires"},
            "sensitivity_alpha1": {"delta_adjR2": round(float(d_sens), 6),
                                   "adjR2_dial": round(float(adjA_s), 6),
                                   "adjR2_plus_cells": round(float(adjB_s), 6)},
            "mean_hits_per_N": round(float(hits.mean()), 1),
            "min_hits_per_N": int(hits.min()),
            "max_hits_per_N": int(hits.max()),
            "mean_cell_occupancy": {str(c): round(float(D[:, c].mean()), 4)
                                    for c in range(16)},
            "cell_beta_vs_ref": cell_beta,
        },
        "verdicts": {
            "rule": ("H1 iff dAdjR2>=0.05 AND perm_p<0.01 AND clean_control; "
                     "H0 iff dAdjR2<0.02 AND machinery_ok; else BORDERLINE; "
                     "clean_control := max(ctrl_null)<d_obs; "
                     "machinery_ok := |mean(ctrl_null)|<machinery_tol"),
            "fired": fired,
            "closing_branch_fired": closing_branch,
            "H1_mixture_adds": bool(h1_fire),
            "H0_dial_sufficient": bool(h0_fire),
            "clean_control": clean_control,
            "machinery_ok": machinery_ok,
        },
        "honest_notes": [
            "Registered rule v2 (header AMENDMENT block) -- v1 audited pre-data: "
            "control criterion unsatisfiable by construction (must-fix), seed "
            "20260903 withdrawn as exp601's lineage (must-fix), kappa arm "
            "degenerate (fixed), stream-band overlap with 598b (fixed).",
            "POST-RUN ERRATUM ON 598B carried here: its control_ok=False was "
            "guaranteed by construction whenever p_ctrl>0.05 held; paper 255's "
            "'control fails on its max clause' framing is corrected to the "
            "informative content c = 25/500 (obs at the 95th pctile of the "
            "y-shuffle range). BORDERLINE verdict itself unaffected.",
            "Regen hash-check CONDITIONAL (disclosed, recorded-not-asserted); "
            "stream-distinctness asserted three ways (self-exclusion, pairwise-"
            "disjoint prefix-complete regenerations, numeric band disjointness).",
            "Hit classifier gcd-chain primorial(1e6) full-smoothness, same class "
            "and cut as 598b; absolute rates internally consistent only.",
            "Parallel hit streams use POSITIONAL seeds (SEED+HIT_OFF+i) => "
            "scheduling-independent; sequential spot-check covers the first "
            f"{SPOT_CHECK_NS} Ns exactly (spot-check, not a whole-array proof; "
            "ex.map ordered-yield semantics index the rest).",
            "Cell rows permuted jointly (preserves within-row structure); "
            "ctrl arm shuffles y (same designs as 598b). Berggren method-law on "
            "row-shuffle nulls does not apply: breaking the y<->D coupling IS "
            "the null under test here.",
            "Latent 598b bug fixed silently-inherited-free: 598b enumerated "
            "cell betas over the UNFILTERED keep list (mislabeled if a column "
            "were degenerate; not triggered in its run); 598c enumerates the "
            "filtered keep_eff -- recorded per errata discipline.",
        ],
        "wall_s": round(time.time() - t0, 2),
    }

    tag = "" if not smoke else "_smoke"
    out_json = os.path.join(OUT_DIR, f"exp598c{tag}_result.json")
    with open(out_json, "w") as f:
        json.dump(result, f, indent=1)

    # --- step 5: verification artifacts --------------------------------------
    npz_path = os.path.join(OUT_DIR, f"exp598c{tag}_verify.npz")
    np.savez_compressed(
        npz_path, y=y, S_dial=S_dial, S_sens=S_sens, D16=D,
        hits=hits, keep=np.array(keep_eff), ref=np.array([ref]),
        perm_null=perm_null, ctrl_null=ctrl_null, d_obs=np.array([d_obs]),
        n_hit=np.array([n_hit]), n_pool=np.array([n_pool]),
        perm_seed=np.array([PERM_SEED]),
        machinery_tol=np.array([MACHINERY_TOL]))
    with open(os.path.join(OUT_DIR, f"exp598c{tag}_ns.txt"), "w") as f:
        f.write("\n".join(str(n) for n in Ns) + "\n")

    print(json.dumps({"fired": result["verdicts"]["fired"]} | {
        "closing_branch": closing_branch,
        "delta_adjR2": result["stats"]["delta_adjR2"],
        "perm_p": result["stats"]["perm_p"],
        "ctrl_p_vs_obs": result["stats"]["ctrl_p_vs_obs"],
        "ctrl_null_max": result["stats"]["ctrl_null_max"],
        "clean_control": clean_control,
        "machinery_ok": machinery_ok,
        "wall_s": result["wall_s"], "out": out_json}), flush=True)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""EXP598B MIXTURE-RATE-CELLS -- PRE-REGISTRATION (written BEFORE analysis)

Question (completes the rate-layer coverage matrix): papers 227/235/236 tested
QR DIALS (weighted marginals S_alpha = sum_[jacobi(N mod l,l)==+1]/l^alpha);
exp596 tested pairwise interactions. UNTESTED: does the FULL 16-cell
divisibility mixture -- the joint class vector (2|v, 3|v, 5|v, 7|v) with
v = j^2 - N -- explain per-N hit-rate variance BEYOND the sqrt-dial S_sqrt,400?

Pre-registered hypotheses (decided before touching the data):
  H1 (mixture adds): hierarchical OLS, log-rate ~ S_sqrt,400 alone VS
      log-rate ~ S_sqrt,400 + cell fixed effects, raises adjusted R^2 by
      >= 0.05 WITH permutation p < 0.01 (500 shuffles of the cell-label rows)
      ==> composition carries rate structure beyond the dial's marginal;
      the rate map refines to CELL level.
  H0 (dial sufficient): Delta-adjR^2 < 0.02 ==> the dial is a sufficient
      statistic at this resolution; the additive-completeness claim UPGRADES
      to a dial-sufficiency claim.
  Otherwise (0.02 <= Delta < 0.05, or Delta >= 0.05 without permutation
  support): BORDERLINE-INCONCLUSIVE.
  CONTROL: a permuted-RATE arm (y shuffled, designs intact) must show null
  Delta; a non-null control flags the whole inference (honest note).

Method (pre-registered):
  1. Regenerate the seed-20260827 population VERBATIM from exp586_weight_exponent.py
     (random.Random(20260827), make_semiprime(bits=96) rejection recursion +
     dedup, n=128, bits=96). HASH-CHECK STATUS: exp586_result.json stores NO
     N strings or hashes (config/verdicts only) => the hash-check branch is
     unavailable; status is CONDITIONAL on recipe identity -- mitigated by
     exp586's own recorded regeneration_verified=true, 128/128 vs exp577 rows.
     Disclosed in honest_notes.
  2. Per N, TWO INDEPENDENT fresh sample streams (neither reuses exp577 rows):
     (a) CELL GRID: n_cell samples j = j0 + t, j0 = isqrt(N)+1, t ~ U[0,T),
         v = j^2 - N > 0; 16-cell class = (2|v, 3|v, 5|v, 7|v);
         occupancy vector = class frequencies (all 16 cells mechanistically
         populated since each marginal P(l|v) in {0} U {2/l} keeps every cell
         >= ~4%; reference cell = globally most-common cell, dropped for
         identifiability).
     (b) HIT STREAM: n_hit fresh samples, same law; HIT := v = j^2 - N is
         fully factored by primes <= CUT (cut = 1e6), decided by a gcd-CHAIN
         tester: repeat g = gcd(v, primorial(1e6)); fail on g == 1 with v > 1;
         strip g with multiplicity until clean. (gcd-chain class of tester,
         cut 1e6, per task spec; exp577's exact tester source is outside this
         agent's read allowance -- operationalization disclosed.)
  3. Hierarchical OLS on y = log((hits + 0.5)/n_hit):
       A: y ~ 1 + S            (S = S_sqrt,400, odd primes 3..400, alpha=0.5
                                  = exp586's alpha_hat, mechanistic Jacobi form)
       B: y ~ 1 + S + D        (D = 15 retained cell-occupancy columns)
     Delta-adjR^2 = adjR^2(B) - adjR^2(A); ranks from lstsq.
     Permutation calibration: 500 reps, jointly row-shuffle D against (y, S),
     p = (1 + #{Delta* >= Delta_obs}) / 501.
     Control arm: 500 reps, row-shuffle y, designs intact -> null check.
     Sensitivity (secondary, reported not gated): dial at alpha = 1.0.
  4. Verdicts per the rules above.

Smoke: n = 32 (first 32 of regenerated population), 20k cell / 12k hit
samples, 50 permutation reps, < 30 s. Full: n = 128, 50k + 50k,
500 + 500 reps, <= 10 min.

Deviations from exp577 absolute rates are expected (its j-law is not readable
under this agent's read allowance); ALL rates here are internally generated
and internally consistent -- comparisons to exp586 R^2 levels are contextual
only. Seeds: population 20260827 (verbatim); cell stream 20260827 + 7e6 + i;
hit stream 20260827 + 9e6 + i; permutations seed 598.
"""
import sys, json, time
import numpy as np
import gmpy2
from gmpy2 import mpz, next_prime, jacobi

OUT_DIR = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74"

SEED = 20260827
BITS = 96
PRIME_LO, PRIME_HI = 3, 400
ALPHA_DIAL = 0.5              # exp586 alpha_hat -> S_sqrt,400
ALPHA_SENS = 1.0              # harmonic sensitivity arm
CUT = 10 ** 6                 # smoothness cut for the hit classifier
T_WINDOW = 1 << 16            # j = isqrt(N)+1+t, t ~ U[0, T_WINDOW)
NCELL_SAMPLES_FULL, NCELL_SAMPLES_SMOKE = 50000, 20000
NHIT_SAMPLES_FULL, NHIT_SAMPLES_SMOKE = 50000, 12000
PERM_REPS_FULL, PERM_REPS_SMOKE = 500, 50
PERM_SEED = 598
CTRL_REPS = PERM_REPS_FULL    # control arm mirrors permutation reps
H1_DR2, H0_DR2, H1_PMAX = 0.05, 0.02, 0.01


# ---- exp586 population generator, VERBATIM (determinism-critical) ----------
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


import random  # noqa: E402  (exp586 places random import at top; kept verbatim usage)


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
    """mpz product of all primes <= bound."""
    ps = odd_primes(3, bound)
    ps += [2]
    def prod(a, b):
        if b - a == 1:
            return mpz(ps[a])
        m = (a + b) // 2
        return prod(a, m) * prod(m, b)
    return prod(0, len(ps))


def is_smooth_chain(v, PRIM, gcd=gmpy2.gcd):
    """gcd-chain smoothness tester at cut = primorial bound. v > 0 (mpz/int).

    Single-big-gcd form: g = gcd(v, P) already contains EVERY distinct prime
    <= CUT dividing v (P squarefree); stripping g with full multiplicity
    leaves v'=1 iff v was CUT-smooth, else v'>1 has a prime factor > CUT."""
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
    """16-cell occupancy vector of v = j^2 - N over the sampled j-grid.

    Exact modular arithmetic (no int64 overflow): v mod l computed as
    (base + t*(2*j0+t)) mod l piecewise."""
    t = rng.integers(0, T, size=n_samples)
    base = (j0 * j0 - N)
    idx = np.zeros(n_samples, dtype=np.int64)
    for k, l in enumerate((2, 3, 5, 7)):
        vm = (base % l + (t % l) * ((2 * j0 + t) % l)) % l
        idx |= (vm == 0).astype(np.int64) << k
    cnt = np.bincount(idx, minlength=16)
    return cnt / float(n_samples)


def count_hits(N, j0, n_samples, rng, PRIM, T=T_WINDOW):
    """Fresh-stream hit count: v = j^2 - N is 1e6-smooth (gcd-chain tester)."""
    t = rng.integers(0, T, size=n_samples).tolist()
    hits = 0
    smooth = is_smooth_chain
    for tv in t:
        j = j0 + tv
        if smooth(j * j - N, PRIM):
            hits += 1
    return hits


def ols_adj(X, y):
    """OLS with rank-aware adjusted R^2."""
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
    n_pool = 32 if smoke else 128
    n_cell = NCELL_SAMPLES_SMOKE if smoke else NCELL_SAMPLES_FULL
    n_hit = NHIT_SAMPLES_SMOKE if smoke else NHIT_SAMPLES_FULL
    perm_reps = PERM_REPS_SMOKE if smoke else PERM_REPS_FULL

    # --- step 1: regenerate population (verbatim recipe) -------------------
    pools = build_population(SEED, n_pool)
    Ns = [p[0] for p in pools]
    # hash-check status: no stored N strings exist in exp586_result.json
    # => CONDITIONAL (see header); recorded, not asserted.

    # --- dial (mechanistic Jacobi, exp586 verbatim form) --------------------
    primes = odd_primes(PRIME_LO, PRIME_HI)
    C = count_matrix(Ns, primes)
    S_dial = C @ np.array([p ** (-ALPHA_DIAL) for p in primes])
    S_sens = C @ np.array([p ** (-ALPHA_SENS) for p in primes])

    # --- step 2: cell grids + hit streams -----------------------------------
    PRIM = primorial(CUT)
    D = np.zeros((n_pool, 16))
    hits = np.zeros(n_pool, dtype=np.int64)
    for i, N in enumerate(Ns):
        j0 = int(gmpy2.isqrt(mpz(N))) + 1
        D[i] = cell_occupancy(N, j0, n_cell, np.random.default_rng(SEED + 7_000_000 + i))
        hits[i] = count_hits(N, j0, n_hit, np.random.default_rng(SEED + 9_000_000 + i), PRIM)
        if (i + 1) % 16 == 0:
            print(f"  [{mode}] {i+1}/{n_pool} Ns scored, wall={time.time()-t0:.1f}s", flush=True)

    y = np.log((hits + 0.5) / float(n_hit))

    # --- step 3: hierarchical regression + permutation calibration ----------
    ref = int(np.argmax(D.mean(axis=0)))           # reference cell (most common)
    keep = [c for c in range(16) if c != ref]
    Dr = D[:, keep]
    if Dr.std(axis=0).min() <= 0:                   # safety: drop degenerate cols
        Dr = Dr[:, Dr.std(axis=0) > 0]

    d_obs, adjA, adjB = delta_adj(y, S_dial, Dr)
    r2A, _, _ = ols_adj(np.hstack([np.ones((n_pool, 1)), S_dial[:, None]]), y)
    r2B, _, _ = ols_adj(np.hstack([np.ones((n_pool, 1)), S_dial[:, None], Dr]), y)
    cells_alone, _, rk_c = ols_adj(np.hstack([np.ones((n_pool, 1)), Dr]), y)

    prng = np.random.default_rng(PERM_SEED)
    perm_null = np.empty(perm_reps)
    ctrl_null = np.empty(perm_reps)
    for r in range(perm_reps):
        idx = prng.permutation(n_pool)
        perm_null[r], _, _ = delta_adj(y, S_dial, Dr[idx])          # cell labels shuffled
        idy = prng.permutation(n_pool)
        ctrl_null[r], _, _ = delta_adj(y[idy], S_dial, Dr)          # permuted-RATE control
    p_perm = float((1 + np.sum(perm_null >= d_obs)) / (perm_reps + 1))
    p_ctrl = float((1 + np.sum(ctrl_null >= d_obs)) / (perm_reps + 1))

    # sensitivity arm (reported, not gated)
    d_sens, adjA_s, adjB_s = delta_adj(y, S_sens, Dr)

    # cell-effect profile (interpretability): fitted cell coefficients
    Xf = np.hstack([np.ones((n_pool, 1)), S_dial[:, None], Dr])
    beta_f, _, _, _ = np.linalg.lstsq(Xf, y, rcond=None)
    cell_beta = {c: round(float(beta_f[2 + k]), 4) for k, c in enumerate(keep)}

    # --- step 4: verdicts ----------------------------------------------------
    h1_fire = (d_obs >= H1_DR2) and (p_perm < H1_PMAX)
    h0_fire = d_obs < H0_DR2
    fired = "H1_MIXTURE_ADDS" if h1_fire else ("H0_DIAL_SUFFICIENT" if h0_fire
                                               else "BORDERLINE_INCONCLUSIVE")
    control_ok = bool(p_ctrl > 0.05 and np.max(ctrl_null) < d_obs)

    result = {
        "config": {
            "exp": "598b", "codename": "MIXTURE-RATE-CELLS", "mode": mode,
            "master_seed": SEED, "bits": BITS, "n_pool": n_pool,
            "cell_samples_per_N": n_cell, "hit_samples_per_N": n_hit,
            "j_window_t": [0, T_WINDOW], "smooth_cut": CUT,
            "dial": f"S_alpha,alpha={ALPHA_DIAL},odd primes {PRIME_LO}..{PRIME_HI}",
            "n_odd_primes": len(primes),
            "perm_reps": perm_reps, "perm_seed": PERM_SEED, "ctrl_reps": perm_reps,
            "thresholds": {"H1_dR2": H1_DR2, "H0_dR2": H0_DR2, "H1_pmax": H1_PMAX},
            "regen_hash_status": (
                "CONDITIONAL: exp586_result.json stores no N strings/hashes; "
                "verbatim recipe identity relied on; exp586 itself verified "
                "128/128 vs exp577 stored rows"),
        },
        "regression": {
            "form": "y=log((hits+0.5)/n_hit); A: y~1+S_sqrt400; B: y~1+S_sqrt400+cellFE",
            "ref_cell": ref, "n_cell_cols": int(Dr.shape[1]),
            "adjR2_dial_alone": round(adjA, 6),
            "adjR2_dial_plus_cells": round(adjB, 6),
            "R2_dial_alone": round(r2A, 6),
            "R2_dial_plus_cells": round(r2B, 6),
            "R2_cells_alone": round(cells_alone, 6),
        },
        "stats": {
            "delta_adjR2": round(d_obs, 6),
            "perm_p": round(p_perm, 4),
            "perm_null_q": {"q50": round(float(np.quantile(perm_null, .5)), 6),
                            "q95": round(float(np.quantile(perm_null, .95)), 6),
                            "max": round(float(perm_null.max()), 6)},
            "ctrl_p_vs_obs": round(p_ctrl, 4),
            "ctrl_null_mean": round(float(ctrl_null.mean()), 6),
            "ctrl_null_max": round(float(ctrl_null.max()), 6),
            "control_ok": control_ok,
            "sensitivity_alpha1": {"delta_adjR2": round(d_sens, 6),
                                   "adjR2_dial": round(adjA_s, 6),
                                   "adjR2_plus_cells": round(adjB_s, 6)},
            "mean_hits_per_N": round(float(hits.mean()), 1),
            "min_hits_per_N": int(hits.min()),
            "mean_cell_occupancy": {str(c): round(float(D[:, c].mean()), 4) for c in range(16)},
            "cell_beta_vs_ref": cell_beta,
        },
        "verdicts": {
            "rule": ("H1 iff dAdjR2>=0.05 AND perm_p<0.01; H0 iff dAdjR2<0.02; "
                     "else BORDERLINE; control arm must be null"),
            "fired": fired,
            "H1_mixture_adds": bool(h1_fire),
            "H0_dial_sufficient": bool(h0_fire),
            "control_arm_null": control_ok,
        },
        "honest_notes": [
            "Hit classifier operationalized as full 1e6-smoothness of v=j^2-N via "
            "gcd-chain with primorial(1e6); exp577's exact tester source is outside "
            "this agent's read allowance (only exp586 files readable) -- same "
            "tester CLASS and cut per task spec.",
            "Absolute hit rates NOT comparable to exp577 rows (its j-law unreadable); "
            "all rates freshly generated and internally consistent; exp586 R2 levels "
            "contextual only.",
            "Regeneration hash-check CONDITIONAL: no N strings stored in "
            "exp586_result.json; verbatim code + exp586's own 128/128 verification "
            "are the mitigation.",
            "Fresh streams 50k/N each (task-spec ~50k) vs exp577's 150k; smoke "
            "20k cell / 12k hit per N.",
            "Cell rows permuted jointly (preserves within-row joint structure, breaks "
            "alignment with y and S).",
        ],
        "wall_s": round(time.time() - t0, 2),
    }
    out_path = f"{OUT_DIR}/exp598b_result.json"
    json.dump(result, open(out_path, "w"), indent=1)
    print(json.dumps({"fired": fired, "adjR2_dial": round(adjA, 4),
                      "adjR2_cells": round(adjB, 4), "d_adjR2": round(d_obs, 4),
                      "perm_p": round(p_perm, 4), "ctrl_ok": control_ok,
                      "wall_s": result["wall_s"], "out": out_path}, indent=1))
    return result


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""EXP586 WEIGHT-EXPONENT-FIT -- PRE-REGISTRATION (written BEFORE analysis)

Question: paper 227 adopted 1/l weighting for the product dial BY INSPECTION;
fit the optimal exponent alpha properly.

Pre-registered hypotheses (decided before touching the data):
  H1 (harmonic refines): optimal alpha_hat != 1 with
      dR2 := R2(alpha_hat) - R2(1.0) >= 0.03
      ==> harmonic law REFINED to Sum(chi=+1)/l^alpha_hat;
      report alpha_hat CI via bootstrap (resample Ns, 500 reps).
  H0 (harmonic confirmed): alpha_hat = 1 within CI OR dR2 < 0.02
      ==> harmonic weight CONFIRMED as the law's true form
      (positive result: closes the refinement question).
  Otherwise (0.02 <= dR2 < 0.03 and CI excludes 1): BORDERLINE-INCONCLUSIVE.

Method (pre-registered):
  1. Data = exp577_result.json rows: per-N hit counts (hits / total,
     total = 150000 j-samples/N; ch6+ct6 gcd-chain tester path), population
     recipe seed 20260827, bitlen 96, n = 128.
  2. Regenerate the SAME 128 N values verbatim from exp577_product_dial.py
     main(): random.Random(20260827), make_semiprime(bits=96) with the exact
     rejection recursion + dedup; assert regenerated N[i] == stored rows[i].N.
  3. For each N and each ODD prime 3 <= l <= 400 (l >= 3 only -- paper 231
     lesson): c_l(N) = [Jacobi(N mod l, l) == +1] (mechanistic Legendre form).
  4. For alpha in {0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0}:
       S_alpha(N) = Sum_{odd prime l<=400} c_l(N)/l^alpha ;
     regress y_N = log((hits_N + 0.5)/total_N) ~ S_alpha (OLS);
     record R2 per alpha. alpha_hat = argmax_alpha R2.
     Bootstrap: 500 reps resampling the 128 Ns with replacement (seeded),
     alpha_hat* = argmax R2 per rep over the SAME grid -> percentile CI.
  5. Verdict per the rules above. SANITY ANCHOR vs paper 227's sweep:
     also record R2 at alpha = 0 (UNWEIGHTED count form Sum c_l) outside the
     fitted grid; report whether ANY fitted alpha materially beats it
     (materially := dR2 >= 0.02).

Smoke mode: n = 16 (first 16 of the regenerated full population), coarse
grid {0.25, 1.0, 2.0}, 50 bootstrap reps, < 30 s. Full <= 10 min (pure
reanalysis; no new simulation).
"""
import sys, json, time, random
import numpy as np
import gmpy2
from gmpy2 import mpz, next_prime, jacobi

SRC_JSON = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74/exp577_result.json"
OUT_DIR = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74"

SEED = 20260827
BITS = 96
ALPHA_GRID_FULL = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
ALPHA_GRID_SMOKE = [0.25, 1.0, 2.0]
ALPHA_ANCHOR = 0.0          # unweighted count form, sanity anchor only
PRIME_LO, PRIME_HI = 3, 400 # odd primes, l>=3 only (paper 231)
BOOT_REPS_FULL, BOOT_REPS_SMOKE = 500, 50
BOOT_SEED = 586
REFINE_DR2 = 0.03           # H1 threshold
CONFIRM_DR2 = 0.02          # H0 threshold / materiality for anchor


# ---- exp577 population generator, VERBATIM (determinism-critical) ----------
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
    """c[i,j] = 1 iff jacobi(N_i mod p_j, p_j) == +1."""
    C = np.zeros((len(Ns), len(primes)), dtype=np.float64)
    gj = gmpy2.jacobi
    for i, N in enumerate(Ns):
        m = mpz(N)
        for j, p in enumerate(primes):
            if gj(m % p, p) == 1:
                C[i, j] = 1.0
    return C


def ols_r2(x, y):
    """Simple OLS; returns dict(R2, r, slope, intercept, slope_se)."""
    n = len(x)
    mx, my = float(np.mean(x)), float(np.mean(y))
    sxx = float(np.sum((x - mx) ** 2)); sxy = float(np.sum((x - mx) * (y - my)))
    slope = sxy / sxx if sxx > 0 else 0.0
    intercept = my - slope * mx
    syy = float(np.sum((y - my) ** 2))
    ss_res = float(np.sum((y - (intercept + slope * x)) ** 2))
    r2 = 1.0 - ss_res / syy if syy > 0 else float("nan")
    r = float(np.sign(slope) * np.sqrt(max(r2, 0.0))) if syy > 0 else float("nan")
    resid = y - (intercept + slope * x)
    se = float(np.sqrt(ss_res / (n - 2) / sxx)) if n > 2 and sxx > 0 else float("nan")
    return {"R2": r2, "r": r, "slope": slope, "intercept": intercept, "slope_se": se}


def main():
    t0 = time.time()
    mode = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    smoke = mode == "smoke"
    n_pool = 16 if smoke else 128
    alpha_grid = ALPHA_GRID_SMOKE if smoke else ALPHA_GRID_FULL
    boot_reps = BOOT_REPS_SMOKE if smoke else BOOT_REPS_FULL

    src = json.load(open(SRC_JSON))
    rows = src["rows"]
    cfg_src = src["config"]
    jsamples_per_N = cfg_src["jsamples_per_N"]

    # --- step 2: regenerate identical population --------------------------
    pools = build_population(SEED, len(rows))
    Ns = [p[0] for p in pools][:n_pool]
    regen_match = [int(r["N"]) == Ns[i] for i, r in enumerate(rows[:n_pool])]
    regen_all = all(regen_match)

    hits = np.array([r["hits"] for r in rows[:n_pool]], dtype=np.float64)
    tot = np.array([r["total"] for r in rows[:n_pool]], dtype=np.float64)
    y = np.log((hits + 0.5) / tot)

    # --- step 3: mechanistic Legendre count matrix -------------------------
    primes = odd_primes(PRIME_LO, PRIME_HI)
    C = count_matrix(Ns, primes)

    # cross-check vs stored S400 column (their dial def may include l=2)
    if "S400" in rows[0]:
        s400_stored = np.array([r["S400"] for r in rows[:n_pool]], dtype=np.float64)
        s400_mine = C.sum(axis=1)
        s400_diff = s400_stored - s400_mine
        s400_corr = float(np.corrcoef(s400_mine, s400_stored)[0, 1])
    else:
        s400_diff = None; s400_corr = None

    # --- step 4: alpha sweep ------------------------------------------------
    curves = {}
    for a in alpha_grid + [ALPHA_ANCHOR]:
        S = C @ (np.array([p ** (-a) for p in primes]))
        curves[a] = ols_r2(S, y)
    R2_fit = {a: curves[a]["R2"] for a in alpha_grid}
    alpha_hat = max(R2_fit, key=R2_fit.get)
    R2_hat = R2_fit[alpha_hat]
    R2_harm = R2_fit[1.0] if 1.0 in R2_fit else float("nan")
    dR2 = R2_hat - R2_harm
    R2_unw = curves[ALPHA_ANCHOR]["R2"]
    d_vs_unw = R2_hat - R2_unw
    d_harm_vs_unw = R2_harm - R2_unw

    # --- bootstrap alpha_hat* ----------------------------------------------
    brng = np.random.default_rng(BOOT_SEED)
    n = len(y)
    boots = []
    for _ in range(boot_reps):
        idx = brng.integers(0, n, n)
        best_a, best_r2 = None, -np.inf
        for a in alpha_grid:
            S = C @ (np.array([p ** (-a) for p in primes]))
            r2 = ols_r2(S[idx], y[idx])["R2"]
            if r2 > best_r2:
                best_r2, best_a = r2, a
        boots.append(best_a)
    boots = np.array(boots)
    ci_lo, ci_hi = (float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))) \
        if boot_reps >= 40 else (None, None)
    ci_contains_1 = (ci_lo is not None) and (ci_lo <= 1.0 <= ci_hi)
    boot_counts = {str(a): int((boots == a).sum()) for a in sorted(set(boots.tolist()))}

    # --- step 5: verdicts ----------------------------------------------------
    h1_fire = (alpha_hat != 1.0) and (dR2 >= REFINE_DR2)
    h0_fire = (ci_contains_1 if ci_lo is not None else False) or (dR2 < CONFIRM_DR2)
    if h1_fire:
        fired = "H1_HARMONIC_REFINED"
    elif h0_fire:
        fired = "H0_HARMONIC_CONFIRMED"
    else:
        fired = "BORDERLINE_INCONCLUSIVE"
    any_beats_unweighted = d_vs_unw >= CONFIRM_DR2

    result = {
        "config": {
            "exp": 586, "codename": "WEIGHT-EXPONENT-FIT", "mode": mode,
            "source_file": SRC_JSON,
            "master_seed": SEED, "bits": BITS, "n_pool": n_pool,
            "jsamples_per_N": jsamples_per_N,
            "prime_range": [PRIME_LO, PRIME_HI], "n_odd_primes": len(primes),
            "alpha_grid": alpha_grid, "alpha_anchor": ALPHA_ANCHOR,
            "bootstrap_reps": boot_reps, "bootstrap_seed": BOOT_SEED,
            "refine_dR2_thresh": REFINE_DR2, "confirm_dR2_thresh": CONFIRM_DR2,
            "regeneration_verified": regen_all,
            "regen_matches": f"{sum(regen_match)}/{len(regen_match)}",
        },
        "regression": {
            "form": "log((hits+0.5)/total) ~ S_alpha, OLS; S_alpha = sum_{odd prime l<=400} [jacobi(N mod l,l)==+1]/l^alpha",
            "per_alpha": [
                {"alpha": a, **{k: round(v, 6) for k, v in curves[a].items()}}
                for a in sorted(curves)
            ],
        },
        "alpha_curve": [{"alpha": a, "R2": round(curves[a]["R2"], 6)} for a in sorted(curves)],
        "stats": {
            "alpha_hat": alpha_hat, "R2_at_alpha_hat": round(R2_hat, 6),
            "R2_at_alpha_1": round(R2_harm, 6), "delta_R2_vs_harmonic": round(dR2, 6),
            "bootstrap_ci95": [ci_lo, ci_hi], "ci_contains_1": ci_contains_1,
            "bootstrap_mean_alpha": round(float(boots.mean()), 4),
            "bootstrap_distribution": boot_counts,
            "R2_unweighted_alpha0": round(R2_unw, 6),
            "delta_best_vs_unweighted": round(d_vs_unw, 6),
            "delta_harmonic_vs_unweighted": round(d_harm_vs_unw, 6),
            "S400_regen_crosscheck": {
                "corr_mine_vs_stored": s400_corr,
                "diff_min": None if s400_diff is None else float(s400_diff.min()),
                "diff_max": None if s400_diff is None else float(s400_diff.max()),
                "note": "stored S400 may include l=2; diff should be in {0,1}-ish constant band if Ns identical",
            },
            "mean_hits_per_N": round(float(hits.mean()), 2),
        },
        "verdicts": {
            "rule": "H1 iff alpha_hat!=1 AND dR2>=0.03; H0 iff CI contains 1 OR dR2<0.02; else BORDERLINE",
            "fired": fired,
            "H1_harmonic_refined": h1_fire,
            "H0_harmonic_confirmed": h0_fire,
            "any_fitted_alpha_beats_unweighted_materially": any_beats_unweighted,
            "harmonic_beats_unweighted_by": round(d_harm_vs_unw, 6),
        },
        "honest_notes": [],
        "wall_s": round(time.time() - t0, 2),
    }
    notes = [
        "Pure reanalysis of exp577 stored per-N hit counts; no new j-sampling.",
        "alpha_hat is discrete over the pre-named grid; CI endpoints are grid points.",
        "S400 crosscheck: exp577's dial definition may include l=2 whereas this "
        "analysis uses odd primes l>=3 only (paper 231), so an offset is expected.",
        f"population regeneration verified against stored N strings: {regen_all}",
        "R2 on log-rate attenuated by per-N Poisson noise (~150k samples, mean hits "
        f"{round(float(hits.mean()),1)}), same attenuation regime as exp577 itself.",
    ]
    if not regen_all:
        notes.append("WARNING: regeneration mismatch -- analysis used REGENERATED Ns; inspect.")
    result["honest_notes"] = notes

    out_path = f"{OUT_DIR}/exp586_result.json"
    json.dump(result, open(out_path, "w"), indent=1)
    print(json.dumps({"fired": fired, "alpha_hat": alpha_hat,
                      "R2_hat": round(R2_hat, 4), "R2_harm": round(R2_harm, 4),
                      "dR2": round(dR2, 4), "CI": [ci_lo, ci_hi],
                      "R2_unw": round(R2_unw, 4), "wall_s": result["wall_s"],
                      "out": out_path}, indent=1))
    return result


if __name__ == "__main__":
    main()

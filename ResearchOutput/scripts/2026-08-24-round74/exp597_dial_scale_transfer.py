#!/usr/bin/env python3
"""EXP597 DIAL-SCALE-TRANSFER -- PRE-REGISTRATION (written BEFORE analysis)

Question: does the Sum(chi=+1)/l^alpha weight law's advantage over alternative
weightings TRANSFER to larger semiprimes? Paper 223 measured dial tilt at
b=15 only; paper 227's alpha_hat=0.5 came from bitlen-96 rate data (exp577/586).
Test the weight exponent's stability across key sizes.

Pre-registered hypotheses (decided before touching any data):
  H1 (law stable): alpha_hat in [0.35, 0.65] at ALL tested bitlens {48, 72, 96}
      ==> the sqrt-weight is scale-stable; the canonical covariate stands
      without scope restriction.
  H0/H-refine: alpha_hat drifts MONOTONICALLY across 48->72->96 OR leaves the
      band at any bitlen ==> the weight law is scale-dependent; report the
      alpha_hat(bits) curve as the refined law.

Method (pre-registered):
  1. Populations per bitlen in {48, 72, 96}: 96 balanced semiprimes each,
     fresh seeds 20260904/20260905/20260906, exp586 recipe VERBATIM
     (make_semiprime rejection recursion + dedup).
  2. Per N: sample 30000 j positions j ~ U[1, 2^52) (ABSOLUTE range, identical
     at every bitlen, declared a priori so the smoothness regime u=ln(y)/ln(B)
     sits in the measurable band ~4.5-5.2 at all three scales without
     per-bitlen tuning). y = (isqrt(N)+j)^2 - N (QS/Fermat offset value).
     HIT iff y is 1e6-smooth, classified by the gcd-chain tester:
       g = gcd(y, P) with P = primorial(primes <= 1e6);
       if g == 1 -> miss; else cur = y/g; repeat h = gcd(cur, g);
       cur //= h until h == 1 (power stripping along the shrinking chain);
       HIT iff final cur == 1. Exact B-smoothness classifier.
     ALSO compute S_alpha dials for alpha in {0.25, 0.5, 0.75, 1.0} over odd
     primes 3 <= l <= 400: S_alpha(N) = sum [jacobi(N mod l, l)==+1] / l^alpha;
     anchor alpha=0 (unweighted count) recorded outside the fitted grid.
  3. Per bitlen: OLS log((hits+0.5)/30000) ~ S_alpha for each alpha; record
     R2(alpha) curves; alpha_hat(bitlen) = argmax R2 over the fitted grid;
     bootstrap CI per bitlen (resample the 96 Ns with replacement, 500 reps,
     seed 597); compare alpha_hat across bitlens.
  4. Power honesty: n=96 clusters per bitlen; percentile CIs; SINGLE seed per
     bitlen disclosed; Poisson attenuation at ~10 hits/N disclosed.

Tester provenance (disclosed): exp577's script is outside this session's
read permission, so the tester is RECONSTRUCTED to the task spec ("hits at cut
1e6 via gcd-chain tester"). Mechanism coherence check: l | (x0+j)^2 - N has a
solution j mod l iff N is a quadratic residue mod l, i.e. iff
jacobi(N mod l, l) = +1 -- the chi+ dial literally selects the usable factor
base, the same lineage as the per-N yield dial validated across bitlen 40-48
and exp559's QS calibration. Grid caveat: the band [0.35, 0.65] contains only
the grid point 0.5, so H1 effectively requires alpha_hat = 0.5 everywhere.

Smoke mode: bitlen 48 only, n=12, 3000 j-samples, alpha grid {0.25, 0.5, 1.0},
20 bootstrap reps, < 60 s. Full <= 15 min.
"""
import sys, json, time, random
from math import prod as math_prod
import numpy as np
import gmpy2
from gmpy2 import mpz, next_prime, jacobi, isqrt

OUT_DIR = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74"

BITS_LIST = [48, 72, 96]
POP_SEED = {48: 20260904, 72: 20260905, 96: 20260906}
JS_SEED_OFFSET = 597            # j-stream rng = POP_SEED[bits] + JS_SEED_OFFSET
N_POOL_FULL, N_POOL_SMOKE = 96, 12
JSAMPLES_FULL, JSAMPLES_SMOKE = 30000, 3000
JMAX = 1 << 52                  # absolute j range, identical at all bitlens
SMOOTH_CUT = 10 ** 6            # smoothness bound B
DIAL_LO, DIAL_HI = 3, 400       # odd primes for the dial (paper 231: l>=3)
ALPHAS_FULL = [0.25, 0.5, 0.75, 1.0]
ALPHAS_SMOKE = [0.25, 0.5, 1.0]
ANCHOR_ALPHA = 0.0              # unweighted count form, sanity anchor only
BOOT_REPS_FULL, BOOT_REPS_SMOKE = 500, 20
BOOT_SEED = 597
BAND_LO, BAND_HI = 0.35, 0.65   # pre-registered H1 band


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


def primes_upto(hi):
    sieve = np.ones(hi + 1, dtype=bool); sieve[:2] = False
    for k in range(2, int(hi ** 0.5) + 1):
        if sieve[k]:
            sieve[k * k::k] = False
    return np.nonzero(sieve)[0]


def count_matrix(Ns, primes):
    """c[i,j] = 1 iff jacobi(N_i mod p_j, p_j) == +1 (exp586 verbatim)."""
    C = np.zeros((len(Ns), len(primes)), dtype=np.float64)
    gj = gmpy2.jacobi
    for i, N in enumerate(Ns):
        m = mpz(N)
        for j, p in enumerate(primes):
            if gj(m % p, p) == 1:
                C[i, j] = 1.0
    return C


def build_primorial(hi):
    """P = product of all primes <= hi, via chunked math.prod then tree."""
    pr = [int(p) for p in primes_upto(hi)]
    chunks = []
    for k in range(0, len(pr), 512):
        chunks.append(mpz(math_prod(pr[k:k + 512])))
    acc = mpz(1)
    for c in chunks:
        acc *= c
    return acc, len(pr)


_GCD = gmpy2.gcd
def hit_test(y, P):
    """gcd-chain tester: HIT iff y is SMOOTH_CUT-smooth."""
    g = _GCD(y, P)
    if g == 1:
        return 0
    cur = y // g
    for _ in range(200):
        if cur == 1:
            return 1
        h = _GCD(cur, g)
        if h == 1:
            return 0
        cur //= h
    return 0


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


def run_bitlen(bits, n_pool, n_js, alphas, P, dial_primes, log):
    t0 = time.time()
    pools = build_population(POP_SEED[bits], n_pool, bits)
    Ns = [p[0] for p in pools]
    C = count_matrix(Ns, dial_primes)
    rng_j = np.random.default_rng(POP_SEED[bits] + JS_SEED_OFFSET)
    hits = np.zeros(n_pool, dtype=np.float64)
    ybits_sum = 0
    GCD = gmpy2.gcd
    for i, N in enumerate(Ns):
        z = mpz(N)
        x0 = isqrt(z)
        js = rng_j.integers(1, JMAX, size=n_js, dtype=np.uint64)
        h = 0
        for jj in js.tolist():
            y = (x0 + jj) * (x0 + jj) - z
            # inlined gcd-chain tester (hot loop)
            g = GCD(y, P)
            if g != 1:
                cur = y // g
                while True:
                    if cur == 1:
                        h += 1
                        break
                    hh = GCD(cur, g)
                    if hh == 1:
                        break
                    cur //= hh
            ybits_sum += y.bit_length()
        hits[i] = h
        if (i + 1) % 16 == 0:
            log(f"  bits={bits} N {i+1}/{n_pool} hits_so_far={int(hits[:i+1].sum())} "
                f"elapsed={time.time()-t0:.1f}s", flush=True)
    tot = float(n_js)
    ylog = np.log((hits + 0.5) / tot)
    curves = {}
    for a in list(alphas) + [ANCHOR_ALPHA]:
        S = C @ (np.array([p ** (-a) for p in dial_primes]))
        curves[a] = ols_r2(S, ylog)
    R2_fit = {a: curves[a]["R2"] for a in alphas}
    alpha_hat = max(R2_fit, key=R2_fit.get)
    # bootstrap CI over resampled Ns
    brng = np.random.default_rng(BOOT_SEED + bits)
    S_by_a = {a: C @ (np.array([p ** (-a) for p in dial_primes])) for a in alphas}
    boots = []
    for _ in range(BOOT_REPS_SMOKE if n_pool < N_POOL_FULL else BOOT_REPS_FULL):
        idx = brng.integers(0, n_pool, n_pool)
        best_a, best_r2 = None, -np.inf
        for a in alphas:
            r2 = ols_r2(S_by_a[a][idx], ylog[idx])["R2"]
            if r2 > best_r2:
                best_r2, best_a = r2, a
        boots.append(best_a)
    boots = np.array(boots)
    ci_lo, ci_hi = (float(np.percentile(boots, 2.5)),
                    float(np.percentile(boots, 97.5)))
    alt_alphas = [ANCHOR_ALPHA] + [a for a in alphas if a != alpha_hat]
    best_alt = max(alt_alphas, key=lambda a: curves[a]["R2"])
    return {
        "bits": bits, "n_pool": n_pool, "n_js": n_js,
        "hits_total": int(hits.sum()),
        "mean_hits_per_N": round(float(hits.mean()), 2),
        "frac_zero_hit_Ns": round(float((hits == 0).mean()), 4),
        "mean_y_bitlen": round(ybits_sum / (n_pool * n_js), 2),
        "regression": [
            {"alpha": a, **{k: round(v, 6) for k, v in curves[a].items()}}
            for a in sorted(curves)
        ],
        "alpha_curve": [{"alpha": a, "R2": round(curves[a]["R2"], 6)}
                        for a in sorted(curves)],
        "alpha_hat": alpha_hat,
        "R2_at_alpha_hat": round(R2_fit[alpha_hat], 6),
        "R2_at_alpha_half": round(curves[0.5]["R2"], 6) if 0.5 in curves else None,
        "R2_at_alpha_1": round(curves[1.0]["R2"], 6) if 1.0 in curves else None,
        "delta_R2_half_vs_1": (round(curves[0.5]["R2"] - curves[1.0]["R2"], 6)
                               if (0.5 in curves and 1.0 in curves) else None),
        "delta_R2_hat_vs_best_alternative": round(
            R2_fit[alpha_hat] - curves[best_alt]["R2"], 6),
        "best_alternative_alpha": best_alt,
        "bootstrap_ci95": [ci_lo, ci_hi],
        "bootstrap_mean_alpha": round(float(boots.mean()), 4),
        "bootstrap_distribution": {str(a): int((boots == a).sum())
                                   for a in sorted(set(boots.tolist()))},
        "wall_s": round(time.time() - t0, 2),
    }


def _worker_main(job):
    """Module-level worker so ProcessPoolExecutor can pickle it."""
    bits, n_pool, n_js, alphas = job
    Pb, _ = build_primorial(SMOOTH_CUT)
    dp = [int(p) for p in primes_upto(DIAL_HI) if p >= DIAL_LO]
    return run_bitlen(bits, n_pool, n_js, alphas, Pb, dp,
                      lambda m, **k: print(m, flush=True))


def main():
    t0 = time.time()
    mode = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    smoke = mode == "smoke"
    n_pool = N_POOL_SMOKE if smoke else N_POOL_FULL
    n_js = JSAMPLES_SMOKE if smoke else JSAMPLES_FULL
    alphas = ALPHAS_SMOKE if smoke else ALPHAS_FULL
    bits_list = [48] if smoke else BITS_LIST
    boot_reps = BOOT_REPS_SMOKE if smoke else BOOT_REPS_FULL

    def log(msg):
        print(msg, flush=True)

    log(f"[exp597 {mode}] bits={bits_list} n_pool={n_pool} n_js={n_js} "
        f"alphas={alphas} JMAX=2^52 cut={SMOOTH_CUT}")

    tP = time.time()
    dial_primes = [int(p) for p in primes_upto(DIAL_HI) if p >= DIAL_LO]
    P, n_smooth_primes = build_primorial(SMOOTH_CUT)
    log(f"primorial({SMOOTH_CUT}): {n_smooth_primes} primes, "
        f"{P.bit_length()} bits, built in {time.time()-tP:.1f}s")

    def _worker(bits):
        # serial path reuses the parent's primorial
        return run_bitlen(bits, n_pool, n_js, alphas, P, dial_primes, log)

    per_bit = []
    if smoke or len(bits_list) == 1:
        for bits in bits_list:
            log(f"[exp597] bitlen {bits}: population + sampling...")
            res = _worker(bits)
            per_bit.append(res)
    else:
        from concurrent.futures import ProcessPoolExecutor
        jobs = [(b, n_pool, n_js, alphas) for b in bits_list]
        with ProcessPoolExecutor(max_workers=len(jobs)) as ex:
            for res in ex.map(_worker_main, jobs):
                per_bit.append(res)
    for res in sorted(per_bit, key=lambda r: r["bits"]):
        log(f"[exp597] bitlen {res['bits']}: alpha_hat={res['alpha_hat']} "
            f"R2hat={res['R2_at_alpha_hat']} CI95={res['bootstrap_ci95']} "
            f"mean_hits={res['mean_hits_per_N']} wall={res['wall_s']}s")
    per_bit = sorted(per_bit, key=lambda r: r["bits"])

    # ---- cross-bitlen verdict ----
    hats = {r["bits"]: r["alpha_hat"] for r in per_bit}
    in_band = {b: (BAND_LO <= a <= BAND_HI) for b, a in hats.items()}
    all_in = all(in_band.values())
    hv = [hats[b] for b in sorted(hats)]
    monotonic = all(x < y for x, y in zip(hv, hv[1:])) or \
        all(x > y for x, y in zip(hv, hv[1:]))
    if all_in:
        fired = "H1_LAW_STABLE"
    elif monotonic or not all(in_band.values()):
        fired = "HREFINE_SCALE_DEPENDENT"
    else:
        fired = "INCONCLUSIVE"

    result = {
        "config": {
            "exp": 597, "codename": "DIAL-SCALE-TRANSFER", "mode": mode,
            "bits_list": bits_list,
            "pop_seeds": {str(b): POP_SEED[b] for b in bits_list},
            "js_seed_offset": JS_SEED_OFFSET,
            "n_pool": n_pool, "jsamples_per_N": n_js,
            "jmax_absolute": JMAX,
            "smooth_cut": SMOOTH_CUT, "n_smooth_primes": n_smooth_primes,
            "prime_range_dial": [DIAL_LO, DIAL_HI],
            "n_odd_dial_primes": len(dial_primes),
            "alpha_grid": alphas, "alpha_anchor": ANCHOR_ALPHA,
            "bootstrap_reps": boot_reps, "bootstrap_seed_base": BOOT_SEED,
            "band": [BAND_LO, BAND_HI],
            "regression_form": "log((hits+0.5)/n_js) ~ S_alpha, OLS; "
                "S_alpha = sum_{odd prime l<=400} [jacobi(N mod l,l)==+1]/l^alpha",
            "tester": "gcd-chain: g=gcd(y,primorial(1e6)); strip powers by "
                      "iterated gcd along shrinking chain; HIT iff cofactor==1; "
                      "y=(isqrt(N)+j)^2-N, j~U[1,2^52)",
        },
        "per_bitlen": per_bit,
        "comparison": {
            "alpha_hat_by_bits": {str(b): hats[b] for b in sorted(hats)},
            "in_band_by_bits": {str(b): in_band[b] for b in sorted(in_band)},
            "all_in_band": all_in,
            "monotonic_drift": bool(monotonic),
        },
        "verdicts": {
            "rule": "H1 iff alpha_hat in [0.35,0.65] at ALL bitlens; else "
                    "scale-dependent (monotonic drift or band exit) => report "
                    "alpha_hat(bits) curve as refined law",
            "fired": fired,
            "H1_law_stable": all_in,
            "scale_dependent": not all_in,
            "drift_is_monotonic": bool(monotonic),
        },
        "honest_notes": [],
        "wall_s": round(time.time() - t0, 2),
    }

    notes = [
        "Tester RECONSTRUCTED to task spec: exp577 script outside this session's "
        "read permissions. Semantics locked to exact 1e6-smoothness of "
        "y=(isqrt(N)+j)^2-N via iterated-gcd power stripping ('gcd-chain').",
        "Mechanism coherence: l | (x0+j)^2-N solvable iff chi(N mod l)=+1, so the "
        "chi+ dial selects the usable factor base -- same lineage as the per-N "
        "yield dial validated across bitlen 40-48 and exp559 QS calibration.",
        "j ~ U[1, 2^52) ABSOLUTE (identical range at every bitlen), declared a "
        "priori; keeps u=ln(y)/ln(1e6) in the measurable band at all scales; "
        "absolute rates are therefore approximately comparable across bitlens.",
        f"SINGLE seed per bitlen ({', '.join(str(POP_SEED[b]) for b in bits_list)}); "
        f"n={n_pool} clusters per bitlen; CIs are cluster-bootstrap percentiles.",
        "Poisson attenuation: expected ~10-15 hits/N at 30k samples, so per-N log "
        "rates are noisy and R2 attenuated; +0.5 smoothing as exp586; zero-hit "
        "Ns handled by the smoothing and reported per bitlen.",
        "Grid discreteness: band [0.35,0.65] contains only grid point 0.5, so H1 "
        "effectively requires alpha_hat=0.5 everywhere; alpha_hat endpoints are "
        "grid points.",
    ]
    result["honest_notes"] = notes

    out_path = f"{OUT_DIR}/exp597_smoke_result.json" if smoke \
        else f"{OUT_DIR}/exp597_result.json"
    json.dump(result, open(out_path, "w"), indent=1)
    log(json.dumps({
        "mode": mode, "fired": fired,
        "alpha_hat_by_bits": {str(b): hats[b] for b in sorted(hats)},
        "R2_at_alpha_hat": {str(r["bits"]): r["R2_at_alpha_hat"] for r in per_bit},
        "mean_hits": {str(r["bits"]): r["mean_hits_per_N"] for r in per_bit},
        "wall_s": result["wall_s"], "out": out_path,
    }, indent=1))
    return result


if __name__ == "__main__":
    main()

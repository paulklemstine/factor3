#!/usr/bin/env python3
"""exp576 QR-VS-OVERDISPERSION (round-74)

Unifies two recorded threads: papers 136/139 (per-N smoothness variance of x^2-N
pools governed by the small-prime QR dial) and paper 220's gate run / exp569c
(per-N candidate hit-counts at u~10 heavily OVERDISPERSED: top clusters
600/561/540 hits vs control-max 359; exposure-corrected D~29 in exp567).
UNMEASURED QUESTION: does the QR dial EXPLAIN the u~10 overdispersion, or is
there unexplained N-structure?

PRE-REGISTRATION (in file BEFORE any data generation):

  Dial definitions (exact, documented):
    S_indiv (PRIMARY; task-specified paper-139 dial form):
      S_indiv(N) = sum over primes l <= 100 of ( [jacobi(l,lo)==+1] + [jacobi(l,hi)==+1] )
      where lo,hi are the two prime factors of N; indicator terms (+1 -> 1, else 0).
      Implemented with sympy.jacobi_symbol (Euler-criterion fallback if sympy absent;
      identical values for prime arguments -- impl recorded in JSON).
    S_prod (mechanistic variant, secondary):
      S_prod(N) = sum over primes l <= 100 of [ jacobi(l,lo)*jacobi(l,hi) == +1 ]
      i.e. #{l<=100 : N is a QR mod l} -- exactly the primes that CAN divide x^2-N.
    S139 (recorded-form replication, tertiary):
      S139(N) = #{primes r <= 400 : jacobi(r,N) == +1}  -- paper-136/139 dial at its
      recorded bound 400 (memory-recorded fit: rate ~ -0.0035 + 0.01156*QR(<=100)).

  Sign convention (stated up front): dial = COUNT of QR-indicator terms. Expected
  direction POSITIVE slope (more QR primes => higher smooth-hit yield), equivalently
  FEWER QR primes => LOWER yield; consistent with paper-139's recorded positive
  coefficient 0.01156 on QR(<=100).

  H1 (QR explains it): with the PRIMARY dial S_indiv,
       R2_log >= 0.25  AND  D_reduction >= 30%
     where R2_log = OLS R^2 of log((hits+0.5)/total) on standardized dial, and
     D_raw = Var(hits)/mean(hits) across N (index of dispersion);
     D_cond = Var(hits - mu_hat_GLM)/mean(hits) with mu_hat from a Poisson GLM
     (log link, offset log(total), covariate dial); D_reduction = 1 - D_cond/D_raw.
     => verdict QR-DIAL-EXPLAINS-OVERDISPERSION.
  H0 (unexplained): R2_log < 0.10 OR D_reduction < 10% (primary dial)
     => verdict NEW-STRUCTURE-MAP-ENTRY (u~10 overdispersion is structure beyond
     the recorded QR mechanism).
  Otherwise => PARTIAL (report which leg failed/succeeded; secondaries disclosed).

Method:
  1. Population: 128 balanced semiprimes bitlen 96, FRESH MASTER SEED 20260826;
     assert-and-record stream distinctness vs seeds 20260824/20260825 (regenerate
     both prior populations with the identical generator, require pairwise-disjoint
     N sets and distinct orderings; hash all three).
  2. Per N: ~150k j-samples (j uniform in [isqrt(N)+1, 3*isqrt(N)], exp569 path),
     classify hits at cut 1e6 via the exp569 gcd-chain primorial tester (verbatim),
     record per-N hit counts.
  3. Per N: dial scores from (lo,hi) as above.
  4. Regress per-N hits on dial (OLS on log-rates + Poisson GLM IRLS); report R^2,
     slope sign, dispersion before/after conditioning, decile spread of rates,
     top-cluster counts vs paper-220 envelope.

Honest limits disclosed in JSON: per-N expected hits small (Poisson noise
attenuates R2), single fresh seed, primary dial is the task-specified S_indiv
(noisy proxy of the mechanistic S_prod; both reported).
"""
import sys, time, json, random, hashlib, math
from multiprocessing import Pool

SEED = 20260826  # FRESH MASTER SEED (lab rule); distinct from 20260824/20260825
BITS = 96
CUT_SMALL, CUT_BIG = 100000, 1000000
DIAL_PRIMES_LE = 100      # primary/secondary dial bound
S139_BOUND = 400          # recorded paper-136/139 bound
R2_H1, R2_H0 = 0.25, 0.10
DRED_H1, DRED_H0 = 30.0, 10.0

import gmpy2
from gmpy2 import mpz, gcd, next_prime

try:
    from sympy import jacobi_symbol as _jac
    JACOBI_IMPL = "sympy.jacobi_symbol"
except Exception:
    JACOBI_IMPL = "euler_criterion_fallback"
    def _jac(a, n):
        # n an odd prime, a coprime -> Legendre symbol in {+1,-1}
        return 1 if pow(int(a) % int(n), (int(n) - 1) // 2, int(n)) == 1 else -1


def build_primorial(bound):
    p = mpz(1); q = mpz(2)
    while q <= bound:
        p *= q
        q = next_prime(q)
    return p

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
        if N in seen: continue
        seen.add(N)
        pools.append((N, lo, hi))
    return pools

def pop_hash(pools):
    return hashlib.sha256(repr([(n, l, h) for n, l, h in pools]).encode()).hexdigest()[:16]

_G = {}
def init_worker(p5, p6):
    _G["P5"] = mpz(p5); _G["P6"] = mpz(p6)

def classify(v):
    """VERBATIM exp569 tester: strip primes<=1e5 then <=1e6; returns (hit5, hit6)."""
    xx = mpz(v)
    P5, P6 = _G["P5"], _G["P6"]
    while xx > 1:
        g = gcd(xx, P5)
        if g == 1: break
        xx //= g
    hit5 = (xx == 1)
    if hit5:
        return True, True
    xy = xx
    while xy > 1:
        g = gcd(xy, P6)
        if g == 1: break
        xy //= g
    return False, (xy == 1)

def worker(args):
    ns, jsamples, seed = args
    rng = random.Random(seed)
    hits = [0]*len(ns); tot = [0]*len(ns)
    for idx, (N, lo, hi) in enumerate(ns):
        s = int(gmpy2.isqrt(mpz(N)))
        jlo = s + 1; jhi = 3 * s
        for _ in range(jsamples):
            j = rng.randint(jlo, jhi)
            v = j * j - N
            if v <= 1:
                continue
            tot[idx] += 1
            _, h6 = classify(v)
            if h6: hits[idx] += 1
    return hits, tot


def dials(lo, hi, N, pr100, pr400):
    si = 0; sp = 0
    jl = [_jac(l, lo) for l in pr100]
    jh = [_jac(l, hi) for l in pr100]
    for a, b in zip(jl, jh):
        si += (a == 1) + (b == 1)
        sp += (a * b == 1)
    s139 = sum(1 for l in pr400 if _jac(l, N) == 1)
    return si, sp, s139


def ols_r2(x, y):
    n = len(x)
    mx = sum(x)/n; my = sum(y)/n
    sxy = sum((a-mx)*(b-my) for a, b in zip(x, y))
    sxx = sum((a-mx)**2 for a in x); syy = sum((b-my)**2 for b in y)
    slope = sxy/sxx if sxx else float("nan")
    r2 = (sxy*sxy)/(sxx*syy) if sxx*syy else float("nan")
    return r2, slope

def poisson_glm(x, y, off, iters=100):
    # IRLS (Fisher scoring) with deviance step-halving -- cannot diverge.
    # Fit on standardized x internally; returns raw-dial-scale coefficients,
    # mu list, McFadden pseudo-R2, Pearson phi, Wald z for slope.
    import statistics as _st
    n = len(x)
    mx = sum(x)/n; sx = (_st.pvariance(x))**0.5 or 1.0
    z = [(xi-mx)/sx for xi in x]
    a = math.log(sum(y)/sum(math.exp(o) for o in off)) if sum(y) else 0.0
    b = 0.0

    def fdev(a_, b_):
        d = 0.0
        for zi, yi, oi in zip(z, y, off):
            m = math.exp(min(max(a_ + b_*zi + oi, -745), 60))
            t = 0.0 if yi == 0 else yi*math.log(yi/m)
            d += 2*(t - (yi - m))
        return d

    def fisher(a_, b_):
        eta = [min(max(a_ + b_*zi + oi, -60), 20) for zi, oi in zip(z, off)]
        mm = [math.exp(e) for e in eta]
        sa = sum(mm); sc = sum(mi*zi for zi, mi in zip(z, mm)); sbb = sum(mi*zi*zi for zi, mi in zip(z, mm))
        ra = sum(yi-mi for yi, mi in zip(y, mm)); rb = sum(zi*(yi-mi) for zi, yi, mi in zip(z, y, mm))
        det = sa*sbb - sc*sc
        if abs(det) < 1e-300:
            return None, None, (sa, sc, sbb)
        return (sbb*ra - sc*rb)/det, (sa*rb - sc*ra)/det, (sa, sc, sbb)

    cur = fdev(a, b)
    for _ in range(iters):
        da, db, info = fisher(a, b)
        if da is None or not (math.isfinite(da) and math.isfinite(db)):
            break
        t = 1.0; accepted = False; nd = cur
        for _h in range(45):
            nd = fdev(a + t*da, b + t*db)
            if nd <= cur + 1e-12:
                accepted = True; break
            t *= 0.5
        if not accepted:
            break
        moved = t*math.hypot(da, db)
        a += t*da; b += t*db
        if cur - nd < 1e-12 and moved < 1e-10:
            cur = nd; break
        cur = nd
    # back to raw-dial units: b_unit = b_z/sx ; a_unit = a_z - b_unit*mx
    b_unit = b/sx; a_unit = a - b_unit*mx
    mu = [math.exp(min(max(a_unit + b_unit*xi + oi, -745), 700)) for xi, oi in zip(x, off)]
    ll_m = sum(yi*math.log(max(mi, 1e-300)) - mi for yi, mi in zip(y, mu))
    mu0 = sum(y)/n
    ll_0 = sum(yi*math.log(max(mu0, 1e-300)) - mu0 for yi in y)
    pr2 = 1 - ll_m/ll_0 if ll_0 else float("nan")
    pearson = sum((yi-mi)**2/max(mi, 1e-300) for yi, mi in zip(y, mu))
    df = max(n-2, 1)
    sa, sc, sbb = fisher(a, b)[2]
    det = sa*sbb - sc*sc
    se_z = math.sqrt(sbb/det) if det > 0 else float("nan")
    se_unit = se_z/sx if se_z == se_z else float("nan")
    zval = b/se_z if (se_z == se_z and se_z > 0) else float("nan")
    return a_unit, b_unit, mu, pr2, pearson/df, zval


def main():
    t0 = time.time()
    mode = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    smoke = mode == "smoke"
    n_pool = 16 if smoke else 128
    jsamples = 20000 if smoke else (int(sys.argv[2]) if len(sys.argv) > 2 else 150000)

    print(f"[{mode}] building primorials...", flush=True)
    P5 = build_primorial(CUT_SMALL); P6 = build_primorial(CUT_BIG)
    print(f"primorials: bits P5={P5.bit_length()} P6={P6.bit_length()}", flush=True)

    print(f"[{mode}] population: {n_pool} semiprimes bitlen {BITS}, master seed {SEED}", flush=True)
    pops = {s: build_population(s, n_pool) for s in (20260824, 20260825, SEED)}
    ns_set = {s: frozenset(n for n, _, _ in p) for s, p in pops.items()}
    distinct = {
        "pairwise_disjoint_N_sets": bool(
            ns_set[20260824].isdisjoint(ns_set[SEED]) and ns_set[20260825].isdisjoint(ns_set[SEED])
            and ns_set[20260824].isdisjoint(ns_set[20260825])),
        "ordering_differs_vs_20260824": pops[20260824] != pops[SEED],
        "ordering_differs_vs_20260825": pops[20260825] != pops[SEED],
        "hashes": {str(s): pop_hash(p) for s, p in pops.items()},
    }
    assert distinct["pairwise_disjoint_N_sets"], "MASTER-SEED STREAM COLLISION"
    pools = pops[SEED]

    pr100, pr400 = [], []
    q = 2
    while q <= S139_BOUND:
        if q <= DIAL_PRIMES_LE: pr100.append(q)
        pr400.append(q)
        q = int(next_prime(q))

    nchunk = 2 if smoke else 8
    per = n_pool // nchunk
    chunks = [(pools[c*per:(c+1)*per], jsamples, SEED + 7000 + c) for c in range(nchunk)]
    print(f"[{mode}] {nchunk} workers x {per} N x {jsamples} j-samples...", flush=True)
    with Pool(nchunk, initializer=init_worker, initargs=(P5, P6)) as pl:
        res = pl.map(worker, chunks)
    hits = [v for r in res for v in r[0]]
    tots = [v for r in res for v in r[1]]

    rows = []
    for i, (N, lo, hi) in enumerate(pools):
        si, sp, s139 = dials(lo, hi, N, pr100, pr400)
        rows.append({"i": i, "N": str(N), "lo": str(lo), "hi": str(hi),
                     "hits": hits[i], "total": tots[i], "rate": hits[i]/tots[i],
                     "S_indiv": si, "S_prod": sp, "S139": s139})

    # ---- regression / dispersion ----
    import statistics as st
    ys = [r["hits"] for r in rows]
    ts = [r["total"] for r in rows]
    ms = sum(ys)/len(ys)
    var_h = st.pvariance(ys)
    D_raw = var_h/ms if ms else float("nan")
    lr = [math.log((r["hits"]+0.5)/r["total"]) for r in rows]
    off = [math.log(t) for t in ts]
    reg = {"primary_dial": "S_indiv", "per_dial": {}}
    for key in ("S_indiv", "S_prod", "S139"):
        xs = [float(r[key]) for r in rows]
        mx = sum(xs)/len(xs); sx = (st.pvariance(xs))**0.5
        xz = [(x-mx)/sx for x in xs]
        r2, slope_std = ols_r2(xz, lr)
        a, b, mu, pr2, phi, zval = poisson_glm(xs, ys, off)
        resid = [y-m for y, m in zip(ys, mu)]
        D_cond = st.pvariance(resid)/ms if ms else float("nan")
        dred = 100*(1 - D_cond/D_raw) if D_raw == D_raw else float("nan")
        reg["per_dial"][key] = {
            "R2_log_ols": round(r2, 4),
            "slope_sign": "+" if slope_std > 0 else ("- " .strip() if slope_std < 0 else "0"),
            "slope_std_lograte_per_sd": round(slope_std, 4),
            "glm_b_per_dial_unit": round(b, 6),
            "rate_multiplier_per_unit": round(math.exp(b), 4) if b == b else float("nan"),
            "glm_wald_z": round(zval, 3),
            "pseudo_R2_mcfadden": round(pr2, 4),
            "pearson_phi_model": round(phi, 2),
            "D_cond": round(D_cond, 2), "D_reduction_pct": round(dred, 2),
        }

    rates = sorted((r["rate"] for r in rows if r["total"]), reverse=True)
    k = max(len(rates)//10, 1)
    decile = round(rates[0]/rates[-1], 3) if rates[-1] > 0 else float("inf")
    top_dec = sum(rates[:k])/k; bot_dec = sum(rates[-k:])/k
    decile_spread = round(top_dec/bot_dec, 3) if bot_dec > 0 else float("inf")
    stats_out = {
        "mean_hits_per_N": round(ms, 2),
        "var_hits": round(var_h, 2),
        "D_raw_index_of_dispersion": round(D_raw, 2),
        "phi_null_poisson_dispersion": round(
            sum((y-ms)**2 for y in ys)/ms/max(len(ys)-1,1), 2),
        "top3_hits": sorted(ys, reverse=True)[:3],
        "min_hits": min(ys), "max_hits": max(ys),
        "zero_hit_N_count": sum(1 for y in ys if y == 0),
        "rate_min": round(min(rates), 8) if rates else None,
        "rate_max": round(max(rates), 8) if rates else None,
        "rate_extremal_ratio": decile,
        "rate_top_decile_over_bottom_decile": decile_spread,
    }
    # fix dial correlations cleanly (pearson r, signed)
    def pear(x, y):
        n=len(x); mx=sum(x)/n; my=sum(y)/n
        sx=(sum((v-mx)**2 for v in x))**.5; sy=(sum((v-my)**2 for v in y))**.5
        if sx==0 or sy==0: return float("nan")
        return sum((a-mx)*(b-my) for a,b in zip(x,y))/(sx*sy)
    stats_out["dial_correlations"] = {
        f"{a}~{b}": round(pear([float(r[a]) for r in rows], [float(r[b]) for r in rows]), 3)
        for a, b in (("S_indiv","S_prod"),("S_indiv","S139"),("S_prod","S139"))}

    p = reg["per_dial"]["S_indiv"]
    h1 = (p["R2_log_ols"] >= R2_H1) and (p["D_reduction_pct"] >= DRED_H1)
    h0 = (p["R2_log_ols"] < R2_H0) or (p["D_reduction_pct"] < DRED_H0)
    name = ("QR-DIAL-EXPLAINS-OVERDISPERSION" if h1 else
            "NEW-STRUCTURE-MAP-ENTRY" if h0 else "PARTIAL-QR-CAPTURE")
    verdicts = {
        "H1_QR_explains": h1, "H0_unexplained_new_structure": h0,
        "rule": f"H1 iff R2_log>={R2_H1} AND Dred>={DRED_H1}% (primary S_indiv); "
                f"H0/new-structure iff R2_log<{R2_H0} OR Dred<{DRED_H0}%; else PARTIAL",
        "verdict": name,
        "secondary_dial_notes": {k: (reg["per_dial"][k]["R2_log_ols"],
                                     reg["per_dial"][k]["slope_sign"],
                                     reg["per_dial"][k]["D_reduction_pct"])
                                 for k in ("S_prod", "S139")},
        "slope_direction_expected": "POSITIVE on QR-count (fewer QR primes => lower yield)",
    }

    wall = time.time()-t0
    out = {
        "exp": "576", "codename": "QR-VS-OVERDISPERSION", "mode": mode,
        "config": {
            "master_seed": SEED, "bits": BITS, "n_pool": n_pool,
            "jsamples_per_N": jsamples, "cut": CUT_BIG, "tester": "exp569 gcd-chain verbatim",
            "jacobi_impl": JACOBI_IMPL,
            "dial_defs": {
                "S_indiv_PRIMARY": "sum_{l prime<=100} ([jac(l,lo)==1]+[jac(l,hi)==1])",
                "S_prod_secondary": "sum_{l<=100} [jac(l,lo)*jac(l,hi)==1] (=#{l: N QR mod l})",
                "S139_tertiary": "#{primes r<=400: jac(r,N)==1} (paper-136/139 bound)",
            },
            "seed_distinctness": distinct,
        },
        "rows": rows, "regression": reg, "stats": stats_out,
        "verdicts": verdicts,
        "honest_notes": [
            f"expected hits/N ~{round(sum(ys)/max(sum(ts),1)*jsamples,1)} at these rates -> "
            "per-N Poisson noise attenuates R2_log; GLM carries the inference",
            "primary dial S_indiv is the task-specified form; mechanistic S_prod "
            "(=#{l<=100: N QR mod l}, the primes that CAN divide x^2-N) reported alongside",
            "single fresh seed (20260826); no paired controls this pass (question is "
            "cross-N variance of candidate pools, not cand-vs-control drift)",
            "zeros smoothed +0.5 only in the OLS-on-log leg; GLM unsmoothed",
        ],
        "wall_s": round(wall, 1),
    }
    fn = "exp576_smoke_result.json" if smoke else "exp576_result.json"
    with open(fn, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({"stats": stats_out, "verdicts": verdicts,
                      "regression_S_indiv": reg["per_dial"]["S_indiv"]}, indent=1)[:4000], flush=True)
    print(f"[{mode}] distinct={distinct['pairwise_disjoint_N_sets']} wall={wall:.1f}s -> {fn}", flush=True)

if __name__ == "__main__":
    main()

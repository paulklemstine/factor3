#!/usr/bin/env python3
"""EXP 539 'TDIAL-U96' (round-56) -- zero-fit dial T(N) pushed to bitlen 96, u=2.5.

PRE-STATED HYPOTHESES (written BEFORE any data generation; also checkpointed
to result.json at stage 00 before any population sampling):
  H1: Spearman(T, relation_rate) stays within [0.55, 0.85] on uniform draws
      at bitlen 96, u = 2.5.
      Carry-in prior: pooled Spearman 0.563, CI [0.537, 0.585] on uniform
      draws through bitlen 92 (bitlen-88 dip was non-terminal).
  H2: T beats count<=100 by more than +0.05 Spearman.

DESIGN (fixed before data):
  Population : 1200 uniform semiprimes = 3 seeds x 400
               (seeds 20261210, 20261211, 20261212).
               p ~ uniform prime in [2^42, 2^48),
               q ~ uniform prime in [2^48, 2^54),
               rejection-sampled until bitlen(N) == 96 exactly.
  Relations  : per N, 240 values V = (r + d)^2 - N with r = isqrt(N) and
               d uniform DISTINCT in [1, 256].
  Smoothness : per-N bound B_N = ceil(Vmax^(1/2.5)) where Vmax is the max of
               that N's 240 values, so u := ln(Vmax)/ln(B_N) = 2.5 exactly.
               V counts as smooth iff EVERY prime factor (2 included) <= B_N.
               rate_N = #smooth / 240.  Smoothness test is EXACT trial
               division over all primes <= B_N (vectorized, compacted active
               set); no probabilistic factoring anywhere.
  Features   : verbatim paper-164 --
               T(N)   = sum over odd primes p <= 400 with Euler criterion
                        powmod(N,(p-1)/2,p) == 1 of 2/p
               cnt(N) = #{odd primes p <= 100 : powmod(N,(p-1)/2,p) == 1}
  Statistics : per-seed Spearman(T,rate), Spearman(cnt,rate), advantage;
               pooled (n=1200) Spearmans with bootstrap CIs (300 resamples);
               paired bootstrap CI for the advantage.

BARRIERS (standard lines):
  (5) SCOPE: claims restricted to uniform semiprime draws at bitlen exactly
      96, u = 2.5, and this specific relation-value construction; no claim
      about structured N, neighbouring bitlens, or a production sieve.
  (8) MEASUREMENT: rate is a 240-sample smoothness proxy (binomial sigma
      ~ 0.03), not a sieved relation yield; T and cnt are scored against
      IDENTICAL relation values, so the paired advantage is internally
      controlled.  The u=2.5 referencing is per-N max-value based.
"""

import json
import math
import time
import traceback

import numpy as np
from gmpy2 import mpz, is_prime, isqrt, powmod
from scipy.stats import spearmanr

WORK = "/tmp/exp57_tu96"
RESULT = f"{WORK}/result.json"

# ---------------- fixed configuration ----------------
SEEDS = [20261210, 20261211, 20261212]
N_PER_SEED = 400                 # 3 x 400 = 1200 total
LO_P, HI_P = 2**42, 2**48
LO_Q, HI_Q = 2**48, 2**54
BITS_N = 96                      # exact bitlen requirement
N_REL = 240                      # relation values per N
H_OFF = 256                      # offsets d in [1, H_OFF], distinct
UEXP = 2.5                       # smoothness operating point u = ln(Vmax)/ln(B)
DIAL_MAX = 400                   # dial primes p <= 400
CNT_MAX = 100                    # baseline count primes p <= 100
N_BOOT = 300
BOOT_SEED = 20260821

T_START = time.time()


def write_result(status, payload):
    doc = {"exp": "539", "codename": "TDIAL-U96", "round": 56,
           "status": status, "wall_s": round(time.time() - T_START, 1)}
    doc.update(payload)
    with open(RESULT, "w") as f:
        json.dump(doc, f, indent=1, default=float)


def sieve_primes(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            s[i * i :: i] = False
    return np.flatnonzero(s)


def draw_uniform_primes(rng, lo, hi, k, small_filter):
    """Uniform primes in [lo, hi): rejection sampling on uniform integers."""
    out = []
    while len(out) < k:
        m = max(8192, 64 * (k - len(out)))
        v = rng.integers(lo, hi, size=m, dtype=np.uint64).astype(np.int64)
        mask = np.ones(len(v), dtype=bool)
        for sp in small_filter:            # cheap prefilter (~88% composites)
            mask &= (v % sp) != 0
        for x in v[mask].tolist():
            if is_prime(x):
                out.append(x)
                if len(out) == k:
                    break
    return out


def gen_population(seed):
    """Rejection sampling: p,q uniform primes in their ranges (each prime
    equally likely); N kept iff bitlen(N) == BITS_N exactly.
    NOTE measured acceptance ~2%: uniform-over-primes tilts both factors to
    the top octaves, so exact-bitlen-96 products are rare -- hence the
    adaptive draw loop."""
    rng = np.random.default_rng(seed)
    small = sieve_primes(100)[1:]          # odd small primes for prefilter
    Ns = []
    attempts = 0
    while len(Ns) < N_PER_SEED:
        k = max(512, int((N_PER_SEED - len(Ns)) * 80))
        ps = draw_uniform_primes(rng, LO_P, HI_P, k, small)
        qs = draw_uniform_primes(rng, LO_Q, HI_Q, k, small)
        for p, q in zip(ps, qs):
            attempts += 1
            N = p * q
            if N.bit_length() == BITS_N:
                Ns.append(mpz(N))
                if len(Ns) == N_PER_SEED:
                    break
    assert len(Ns) == N_PER_SEED
    assert all(int(N).bit_length() == BITS_N for N in Ns)
    print(f"    seed {seed}: {attempts} pair-attempts -> {len(Ns)} accepts "
          f"({100.0*len(Ns)/attempts:.1f}%)", flush=True)
    return Ns


ODD_PRIMES_400 = None   # set in main
ODD_PRIMES_100 = None


def features(N_list):
    """T(N) = sum 2/p over odd QR primes <= 400 ; cnt = # QR primes <= 100."""
    T = np.zeros(len(N_list))
    C = np.zeros(len(N_list))
    exps400 = [(p - 1) // 2 for p in ODD_PRIMES_400]
    for i, N in enumerate(N_list):
        t = 0.0
        c = 0
        for p, e in zip(ODD_PRIMES_400, exps400):
            if powmod(N, e, p) == 1:
                t += 2.0 / p
                if p <= CNT_MAX:
                    c += 1
        T[i] = t
        C[i] = c
    return T, C


def smooth_rates(N_list, tag):
    """Exact B_N-smoothness of 240 relation values per N; returns rate array."""
    rng = np.random.default_rng(tag * 7 + 1)
    n = len(N_list)
    Vs, Gs, BVs = [], [], []
    bnds = []
    for i, Nmpz in enumerate(N_list):
        N = int(Nmpz)
        r = int(isqrt(N))
        d = np.sort(rng.choice(H_OFF, N_REL, replace=False)).astype(np.int64) + 1
        vals = []
        for dd in d.tolist():
            x = r + dd
            vals.append(x * x - N)     # python ints; V < 2^57 here
        vmax = max(vals)
        B = int(math.ceil(math.exp(math.log(vmax) / UEXP)))
        bnds.append(B)
        Vs.extend(vals)
        Gs.extend([i] * N_REL)
        BVs.extend([B] * N_REL)
    V = np.array(Vs, dtype=np.uint64)
    BV = np.array(BVs, dtype=np.uint64)
    G = np.array(Gs, dtype=np.int64)
    nV = len(V)
    smooth_full = np.zeros(nV, dtype=bool)

    # prime base: everything up to the largest per-N bound
    Bmax = max(bnds)
    prim = sieve_primes(Bmax)
    SMALL = [int(p) for p in prim if p <= DIAL_MAX]     # includes 2
    BIG = [int(p) for p in prim if p > DIAL_MAX]

    # compacted working set
    Valive = V.copy()
    BVlive = BV.copy()
    Olive = np.arange(nV, dtype=np.int64)
    ndead = 0

    def pull(p):
        """divide out ALL factors of p from live values; return touched locals"""
        hl = np.flatnonzero(Valive % np.uint64(p) == 0)
        if hl.size == 0:
            return hl
        touched = hl.copy()
        while hl.size:
            Valive[hl] //= np.uint64(p)
            hl = hl[(Valive[hl] % np.uint64(p)) == 0]
            if hl.size:
                touched = np.union1d(touched, hl)
        return touched

    def decide(locals_):
        nonlocal ndead
        if locals_.size:
            dec = locals_[Valive[locals_] <= BVlive[locals_]]
            if dec.size:
                smooth_full[Olive[dec]] = True
                Valive[dec] = np.uint64(2**63 - 1)   # park dead rows
                BVlive[dec] = np.uint64(0)
                Olive[dec] = -1
                ndead += dec.size

    def compact():
        nonlocal Valive, BVlive, Olive, ndead
        keep = Olive >= 0
        Valive, BVlive, Olive = Valive[keep], BVlive[keep], Olive[keep]
        ndead = 0

    # Stage A: primes <= DIAL_MAX (includes 2) -- factoring only
    for p in SMALL:
        decide(pull(p))
    # required pass (not a no-op): values fully reduced to <= their bound
    decide(np.arange(len(Valive)))
    compact()

    t0 = time.time()
    nbig = len(BIG)
    for j in range(nbig):
        p = BIG[j]
        decide(pull(p))
        if ndead > 0.3 * len(Valive):
            compact()
        if j % 50000 == 0:
            print(f"    [{tag}] big-prime {j}/{nbig} (p={p}) "
                  f"live={len(Valive)} elapsed={time.time()-t0:.0f}s",
                  flush=True)
    # leftover live values have a prime factor > B -> not smooth
    rate = np.zeros(n)
    counts = np.bincount(G[smooth_full], minlength=n)
    rate = counts / float(N_REL)
    return rate, bnds, int(smooth_full.sum())


def boot_ci(a, b, nboot=N_BOOT, seed=BOOT_SEED):
    rng = np.random.default_rng(seed)
    n = len(a)
    out = np.empty(nboot)
    for k in range(nboot):
        ii = rng.integers(0, n, n)
        out[k] = float(spearmanr(a[ii], b[ii])[0])
    return [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))], out


def main():
    global ODD_PRIMES_400, ODD_PRIMES_100

    # ---- stage 00: hypotheses/config BEFORE any data ----
    write_result("00_hypotheses_stated", {
        "hypotheses": {
            "H1": "Spearman(T, rate) within [0.55, 0.85] on uniform draws at bitlen 96, u=2.5",
            "H2": "T beats count<=100 by more than +0.05 Spearman",
        },
        "prior": "pooled Spearman 0.563 CI [0.537,0.585] through bitlen 92",
        "config": {"seeds": SEEDS, "n_per_seed": N_PER_SEED,
                    "p_range": [LO_P, HI_P], "q_range": [LO_Q, HI_Q],
                    "bits_n": BITS_N, "n_rel": N_REL, "h_off": H_OFF,
                    "u_exp": UEXP, "dial_max": DIAL_MAX, "cnt_max": CNT_MAX,
                    "n_boot": N_BOOT},
    })
    print(f"[{time.time()-T_START:.0f}s] stage 00 done", flush=True)

    all_primes = sieve_primes(DIAL_MAX)
    ODD_PRIMES_400 = [int(p) for p in all_primes if p > 2]
    ODD_PRIMES_100 = [p for p in ODD_PRIMES_400 if p <= CNT_MAX]

    # ---- stage 01: population ----
    pop = {}
    for s in SEEDS:
        pop[s] = gen_population(s)
        print(f"[{time.time()-T_START:.0f}s] seed {s}: {len(pop[s])} semiprimes",
              flush=True)
    N_all = [N for s in SEEDS for N in pop[s]]
    seed_id = np.array([i // N_PER_SEED for i in range(len(N_all))])
    bl = [int(N).bit_length() for N in N_all]
    assert min(bl) == max(bl) == BITS_N and len(set(map(int, N_all))) == len(N_all)
    with open(f"{WORK}/population.txt", "w") as f:
        for s, N in zip(seed_id, N_all):
            f.write(f"{SEEDS[s]} {N}\n")
    write_result("01_population_done", {
        "population": {"total": len(N_all), "bitlen_min": min(bl),
                        "bitlen_max": max(bl)}})
    print(f"[{time.time()-T_START:.0f}s] stage 01 done", flush=True)

    # ---- stage 02: dial features ----
    T_all, C_all = features(N_all)
    np.savez(f"{WORK}/features.npz", T=T_all, C=C_all, seed=seed_id)
    print(f"[{time.time()-T_START:.0f}s] stage 02 done: "
          f"T mean={T_all.mean():.4f} range=[{T_all.min():.3f},{T_all.max():.3f}]; "
          f"cnt mean={C_all.mean():.2f}", flush=True)
    write_result("02_features_done", {
        "features": {"T_mean": float(T_all.mean()), "cnt_mean": float(C_all.mean())}})

    # ---- stage 03: relation rates (exact smoothness), per seed ----
    rates = {}
    for si, s in enumerate(SEEDS):
        sl = slice(si * N_PER_SEED, (si + 1) * N_PER_SEED)
        r, bnds, nsm = smooth_rates(N_all[sl], si)
        rates[s] = r
        np.save(f"{WORK}/rate_seed{si}.npy", r)
        print(f"[{time.time()-T_START:.0f}s] seed {s}: rates done "
              f"(mean={r.mean():.4f}, smooth values={nsm}/"
              f"{N_PER_SEED*N_REL}, B~[{min(bnds)},{max(bnds)}])", flush=True)
        write_result("03_rates_in_progress", {
            "rates_done_seeds": SEEDS[: si + 1],
            "rates_summary": {str(ss): {"mean": float(rates[ss].mean()),
                                         "std": float(rates[ss].std())}
                               for ss in rates}})
    R_all = np.concatenate([rates[s] for s in SEEDS])

    # ---- stage 04: statistics ----
    res = {"per_seed": []}
    for si, s in enumerate(SEEDS):
        sl = slice(si * N_PER_SEED, (si + 1) * N_PER_SEED)
        rT = float(spearmanr(T_all[sl], R_all[sl])[0])
        rC = float(spearmanr(C_all[sl], R_all[sl])[0])
        res["per_seed"].append({"seed": s, "n": N_PER_SEED,
                                 "rho_T": rT, "rho_cnt": rC,
                                 "advantage": rT - rC})
    pT = float(spearmanr(T_all, R_all)[0])
    pC = float(spearmanr(C_all, R_all)[0])
    ciT, _ = boot_ci(T_all, R_all)
    ciC, _ = boot_ci(C_all, R_all)
    rngb = np.random.default_rng(BOOT_SEED + 1)
    advs = np.empty(N_BOOT)
    for k in range(N_BOOT):
        ii = rngb.integers(0, len(R_all), len(R_all))
        advs[k] = (float(spearmanr(T_all[ii], R_all[ii])[0])
                   - float(spearmanr(C_all[ii], R_all[ii])[0]))
    ciA = [float(np.percentile(advs, 2.5)), float(np.percentile(advs, 97.5))]
    adv = pT - pC

    h1 = bool(0.55 <= pT <= 0.85)
    h2 = bool(adv > 0.05)
    if h1 and h2:
        verdict = "TDIAL-U96-CONFIRMED"
    elif h1 and not h2:
        verdict = "TDIAL-U96-DIAL-ONLY"
    elif (not h1) and pT < 0.55:
        verdict = "TDIAL-U96-FADES-AT-96"
    else:
        verdict = "TDIAL-U96-OVERSPIKE-CHECK-MEASUREMENT"

    write_result("04_final", {
        "hypotheses": {
            "H1": "Spearman(T, rate) within [0.55, 0.85] on uniform draws at bitlen 96, u=2.5",
            "H2": "T beats count<=100 by more than +0.05 Spearman"},
        "config": {"seeds": SEEDS, "n_per_seed": N_PER_SEED,
                    "p_range": [LO_P, HI_P], "q_range": [LO_Q, HI_Q],
                    "bits_n": BITS_N, "n_rel": N_REL, "h_off": H_OFF,
                    "u_exp": UEXP, "dial_max": DIAL_MAX, "cnt_max": CNT_MAX,
                    "n_boot": N_BOOT},
        "population": {"total": len(N_all)},
        "per_seed": res["per_seed"],
        "pooled": {"n": len(R_all), "rho_T": pT, "rho_T_ci95": ciT,
                    "rho_cnt": pC, "rho_cnt_ci95": ciC,
                    "advantage": adv, "advantage_ci95": ciA},
        "rate_summary": {"mean": float(R_all.mean()), "std": float(R_all.std()),
                          "smooth_values": int((R_all * N_REL).sum()),
                          "total_values": len(R_all)},
        "verdicts": {"H1_pass": h1, "H2_pass": h2, "verdict_name": verdict},
    })
    print(f"[{time.time()-T_START:.0f}s] FINAL: pooled rho_T={pT:.4f} "
          f"CI[{ciT[0]:.4f},{ciT[1]:.4f}] rho_cnt={pC:.4f} "
          f"adv={adv:+.4f} CI[{ciA[0]:.4f},{ciA[1]:.4f}] "
          f"H1={h1} H2={h2} VERDICT={verdict}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        err = traceback.format_exc()
        print(err, flush=True)
        try:
            write_result("ERROR", {"traceback": err})
        except Exception:
            pass
        raise

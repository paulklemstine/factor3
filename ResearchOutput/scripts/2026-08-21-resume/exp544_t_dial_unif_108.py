#!/usr/bin/env python3
"""EXP 544 'TDIAL-U108' (round-69) -- zero-fit dial T(N) pushed to bitlen 108,
u=2.5.

PRE-STATED HYPOTHESES (written BEFORE any data generation; also checkpointed
to result.json at stage 00 before any population sampling -- verbatim from the
tasking brief):
  H1: Spearman(T, rate) stays within [0.55, 0.85] on uniform draws at
      bitlen 108, u=2.5.
  H2: T beats count <=100 by > +0.05.
  Carry-in priors (TDIAL-U ladder): pooled Spearman 0.5739 (fixed
      classifier) at bitlen 96; 0.5436, CI [0.4982, 0.5881] at bitlen 100
      (TDIAL-U100-FADES-AT-100); 0.5005, CI [0.4557, 0.5454] at bitlen 104
      (TDIAL-U104-CONTINUES-FADE). NOTE: the brief quotes the validated-band
      H1 against a carry-in chain whose last two cells already sit BELOW the
      band's lower edge 0.55 -- the hypotheses are tested exactly as stated.

DESIGN (fixed before data):
  Population : 1200 uniform semiprimes = 3 seeds x 400
               (seeds 20261210, 20261211, 20261212).
               DESIGN NOTE / BRIEF CORRECTION: the tasking brief wrote
               "p uniform prime in [2^20,2^26), q uniform prime in
               [2^26,2^32)" -- those ranges cap N < 2^58 and are
               mathematically INCOMPATIBLE with the brief's own binding
               constraint bitlen(N) = 108 (rejection sampling would accept
               nothing). Corrected BEFORE data generation to the established
               TDIAL ladder continuation (88..104 used width-6 octave windows
               meeting at 2^(B/2): bitlen 100 -> [2^44,2^50) x [2^50,2^56);
               bitlen 104 -> [2^46,2^52) x [2^52,2^58)), i.e.
               [2^48,2^54) x [2^54,2^60) for B=108. Everything else is
               verbatim exp541/TDIAL-U104 methodology.
  Relations  : per N, 240 values V = (r + d)^2 - N with r = isqrt(N) and
               d uniform DISTINCT in [1, 256].  (At B=108, V < 2^63.001 --
               still inside the uint64 classifier.)
  Smoothness : per-N bound B_N = ceil(Vmax^(1/2.5)) where Vmax is the max of
               that N's 240 values, so u := ln(Vmax)/ln(B_N) = 2.5 exactly.
               V counts as smooth iff EVERY prime factor (2 included) <= B_N.
               Smoothness test is EXACT trial division over all primes <= B_N,
               restricted per-row to its OWN bound (exp540-fixed classifier:
               mask BVlive >= p + expiry parking); no probabilistic factoring
               anywhere; PLUS an independent Pollard-rho(Brent) full-
               factorization spot-check on a fixed 300-value subsample per
               seed (asserted mismatch-free).
  Features   : verbatim paper-164 --
               T(N)   = sum over odd primes p <= 400 with Euler criterion
                        powmod(N,(p-1)/2,p) == 1 of 2/p
               cnt(N) = #{odd primes p <= 100 : powmod(N,(p-1)/2,p) == 1}
  Statistics : per-seed Spearman(T,rate), Spearman(cnt,rate), advantage;
               pooled (n=1200) Spearmans with bootstrap CIs (300 resamples);
               paired bootstrap CI for the advantage.
  Runtime    : per-seed rate computation runs in a 3-worker process pool
               (deterministic per-tag RNG; pure runtime optimization over
               exp540's sequential loop, identical numbers).

BARRIERS (standard lines):
  (5) SCOPE: claims restricted to uniform semiprime draws at bitlen exactly
      108, u = 2.5, and this specific relation-value construction; no claim
      about structured N, neighbouring bitlens, or a production sieve.
  (8) MEASUREMENT: rate is a 240-sample smoothness proxy (binomial sigma
      ~ 0.02), not a sieved relation yield; T and cnt are scored against
      IDENTICAL relation values, so the paired advantage is internally
      controlled.  The u=2.5 referencing is per-N max-value based
      (definition-dependence).  Classifier is the spot-check-asserted
      exp540-fixed one; the brief's factor-range typo was corrected to the
      ladder-consistent windows (documented above) BEFORE data generation.
"""

import json
import math
import time
import traceback
from math import gcd

import numpy as np
from gmpy2 import mpz, is_prime, isqrt, powmod
from scipy.stats import spearmanr

WORK = "/tmp/exp69_tu108"
RESULT = f"{WORK}/result.json"

# ---------------- fixed configuration ----------------
SEEDS = [20261210, 20261211, 20261212]
N_PER_SEED = 400                 # 3 x 400 = 1200 total
LO_P, HI_P = 2**48, 2**54
LO_Q, HI_Q = 2**54, 2**60
BITS_N = 108                     # exact bitlen requirement
N_REL = 240                      # relation values per N
H_OFF = 256                      # offsets d in [1, H_OFF], distinct
UEXP = 2.5                       # smoothness operating point u = ln(Vmax)/ln(B)
DIAL_MAX = 400                   # dial primes p <= 400
CNT_MAX = 100                    # baseline count primes p <= 100
N_BOOT = 300
BOOT_SEED = 20260822
SPOT_PER_SEED = 300              # independent factorization spot-check size
PRIOR_96 = 0.5739                # fixed-classifier U96 pooled rho(T)
PRIOR_100 = 0.5436               # U100 pooled rho(T) (TDIAL-U100-FADES-AT-100)
PRIOR_104 = 0.5005               # U104 pooled rho(T) (TDIAL-U104-CONTINUES-FADE)
BAND_LO, BAND_HI = 0.55, 0.85    # H1 validated band
ADV_MIN = 0.05                   # H2 advantage threshold

T_START = time.time()


def write_result(status, payload):
    doc = {"exp": "544", "codename": "TDIAL-U108", "round": 69,
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
    NOTE measured acceptance ~3% (as at bits 100/104): uniform-over-primes
    tilts both factors to the top octaves, so exact-bitlen products are rare
    -- hence the adaptive draw loop."""
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


# ---------- independent full factorization (Pollard rho / Brent) ----------
SMALL_1K = None   # set in main


def _pollard_brent(n):
    """Return a nontrivial factor of composite odd n (no small factors)."""
    rng = np.random.default_rng(541001)
    while True:
        y = int(rng.integers(1, n))
        c = int(rng.integers(1, n))
        m = 128
        g = r = q = 1
        x = ys = y
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = gcd(q, n)
                k += m
            r *= 2
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = gcd(abs(x - ys), n)
        if g != n:
            return g


def full_factor(n):
    """Full prime factorization of n >= 1; returns sorted list of primes."""
    fs = []
    for p in SMALL_1K:
        while n % p == 0:
            fs.append(int(p))
            n //= p
        if p * p > n and n > 1:
            break
    stack = [n] if n > 1 else []
    while stack:
        v = stack.pop()
        if v == 1:
            continue
        if v < p * p or is_prime(v):
            fs.append(int(v))
            continue
        d = _pollard_brent(v)
        stack.append(d)
        stack.append(v // d)
    return sorted(fs)


def smooth_rates(N_list_ints, tag):
    """Exact B_N-smoothness of 240 relation values per N; returns rate array,
    the per-N bounds, and the per-value smooth flag vector.
    exp540-FIXED classifier: each row is pulled only by primes <= ITS OWN
    bound (BVlive >= p mask) with expiry parking, so 'smooth' means smooth
    wrt the row's own bound exactly."""
    N_list = [mpz(v) for v in N_list_ints]
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
            vals.append(x * x - N)     # python ints; V < 2^63.001 here
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
        """divide out ALL factors of p from ELIGIBLE live values (own bound
        still allows p); return touched locals"""
        hl = np.flatnonzero((BVlive >= np.uint64(p))
                            & (Valive % np.uint64(p) == 0))
        if hl.size == 0:
            return hl
        touched = hl.copy()
        while hl.size:
            Valive[hl] //= np.uint64(p)
            hl = hl[(BVlive[hl] >= np.uint64(p))
                    & (Valive[hl] % np.uint64(p) == 0)]
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

    def expire(p):
        """park rows whose own bound the loop has passed: all their remaining
        prime factors exceed their bound -> definitively NOT smooth."""
        gone = np.flatnonzero((Olive >= 0) & (BVlive < np.uint64(p)))
        if gone.size:
            Valive[gone] = np.uint64(2**63 - 1)
            BVlive[gone] = np.uint64(0)
            Olive[gone] = -1

    def compact():
        nonlocal Valive, BVlive, Olive, ndead
        keep = Olive >= 0
        Valive, BVlive, Olive = Valive[keep], BVlive[keep], Olive[keep]
        ndead = 0

    t0 = time.time()
    # Stage A: primes <= DIAL_MAX (includes 2) -- factoring only
    for p in SMALL:
        decide(pull(p))
    # required pass (not a no-op): values fully reduced to <= their bound
    decide(np.arange(len(Valive)))
    compact()

    nbig = len(BIG)
    for j in range(nbig):
        p = BIG[j]
        decide(pull(p))
        if ndead > 0.3 * len(Valive):
            compact()
            expire(p)
        if j % 200000 == 0:
            print(f"    [{tag}] big-prime {j}/{nbig} (p={p}) "
                  f"live={len(Valive)} elapsed={time.time()-t0:.0f}s",
                  flush=True)
    # leftover live values have a prime factor > B -> not smooth
    counts = np.bincount(G[smooth_full], minlength=n)
    rate = counts / float(N_REL)

    # ---- independent spot-check: Pollard-rho full factorization ----
    rs = np.random.default_rng(900000 + tag)
    idx = np.sort(rs.choice(nV, SPOT_PER_SEED, replace=False))
    mism = 0
    for i in idx.tolist():
        mx = max(full_factor(int(V[i])))
        if (mx <= int(BV[i])) != bool(smooth_full[i]):
            mism += 1
    print(f"    [{tag}] spot-check {SPOT_PER_SEED} values vs Pollard-rho "
          f"full factorization: mismatches={mism}", flush=True)
    assert mism == 0, "smoothness classification disagrees with exact factoring"
    return rate, bnds, int(smooth_full.sum()), smooth_full, bnds


def _rates_worker(args):
    """Process-pool entry point: (ints, tag) -> smooth_rates."""
    ints, tag = args
    return tag, smooth_rates(ints, tag)


def boot_ci(a, b, nboot=N_BOOT, seed=BOOT_SEED):
    rng = np.random.default_rng(seed)
    n = len(a)
    out = np.empty(nboot)
    for k in range(nboot):
        ii = rng.integers(0, n, n)
        out[k] = float(spearmanr(a[ii], b[ii])[0])
    return [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))], out


def main():
    global ODD_PRIMES_400, SMALL_1K

    # ---- stage 00: hypotheses/config BEFORE any data ----
    write_result("00_hypotheses_stated", {
        "hypotheses": {
            "H1": "Spearman(T, rate) stays within [0.55, 0.85] on uniform "
                  "draws at bitlen 108, u=2.5",
            "H2": "T beats count <=100 by > +0.05",
        },
        "prior": f"pooled Spearman {PRIOR_96} (fixed classifier) at bitlen 96; "
                 f"{PRIOR_100} CI [0.4982,0.5881] at bitlen 100 "
                 "(TDIAL-U100-FADES-AT-100); "
                 f"{PRIOR_104} CI [0.4557,0.5454] at bitlen 104 "
                 "(TDIAL-U104-CONTINUES-FADE)",
        "brief_correction": "brief's literal ranges [2^20,2^26)x[2^26,2^32) "
                            "cap N<2^58, incompatible with bitlen(N)=108; "
                            "corrected pre-data to the TDIAL-ladder windows "
                            "[2^48,2^54)x[2^54,2^60) (width-6 octaves meeting "
                            "at 2^(B/2), as in exp536..541)",
        "config": {"seeds": SEEDS, "n_per_seed": N_PER_SEED,
                    "p_range": [LO_P, HI_P], "q_range": [LO_Q, HI_Q],
                    "bits_n": BITS_N, "n_rel": N_REL, "h_off": H_OFF,
                    "u_exp": UEXP, "dial_max": DIAL_MAX, "cnt_max": CNT_MAX,
                    "n_boot": N_BOOT},
    })
    print(f"[{time.time()-T_START:.0f}s] stage 00 done", flush=True)

    all_primes = sieve_primes(DIAL_MAX)
    ODD_PRIMES_400 = [int(p) for p in all_primes if p > 2]
    SMALL_1K = [int(p) for p in sieve_primes(1000)]

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
    # parallel across seeds (deterministic per-tag RNG; runtime-only change)
    from multiprocessing import get_context
    rates = {}
    try:
        ctx = get_context("fork")
        with ctx.Pool(processes=3) as pool:
            for tag, (r, bnds, nsm, smf, _) in pool.map(
                    _rates_worker,
                    [(N_all[si*N_PER_SEED:(si+1)*N_PER_SEED], si)
                     for si in range(len(SEEDS))]):
                s = SEEDS[tag]
                rates[s] = r
                np.save(f"{WORK}/rate_seed{tag}.npy", r)
                np.save(f"{WORK}/smooth_seed{tag}.npy", smf)
                print(f"[{time.time()-T_START:.0f}s] seed {s}: rates done "
                      f"(mean={r.mean():.4f}, smooth values={nsm}/"
                      f"{N_PER_SEED*N_REL}, B~[{min(bnds)},{max(bnds)}])",
                      flush=True)
    except Exception as exc:                       # pragma: no cover
        print(f"pool failed ({exc!r}); falling back to sequential", flush=True)
        for si, s in enumerate(SEEDS):
            sl = slice(si * N_PER_SEED, (si + 1) * N_PER_SEED)
            r, bnds, nsm, smf, _ = smooth_rates(N_all[sl], si)
            rates[s] = r
            np.save(f"{WORK}/rate_seed{si}.npy", r)
            np.save(f"{WORK}/smooth_seed{si}.npy", smf)
            print(f"[{time.time()-T_START:.0f}s] seed {s}: rates done "
                  f"(mean={r.mean():.4f}, smooth values={nsm}/"
                  f"{N_PER_SEED*N_REL}, B~[{min(bnds)},{max(bnds)}])", flush=True)
    write_result("03_rates_in_progress", {
        "rates_done_seeds": SEEDS,
        "spot_check": "pollard-rho mismatch=0 per seed (asserted in-script)",
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

    h1 = bool(BAND_LO <= pT <= BAND_HI)   # stays within [0.55, 0.85]
    h2 = bool(adv > ADV_MIN)              # beats count by > +0.05
    ci_pos = ("below", "straddles", "above")[
        0 if ciT[1] < BAND_LO else 1 if ciT[0] <= BAND_LO else 2]
    further_decline = bool(pT < PRIOR_104)
    h1_per_seed = all(ps["rho_T"] >= BAND_LO and ps["rho_T"] <= BAND_HI
                      for ps in res["per_seed"])
    if h1:
        verdict = "TDIAL-U108-IN-BAND"
    elif further_decline:
        verdict = "TDIAL-U108-CONTINUES-FADE"
    else:
        verdict = "TDIAL-U108-BELOW-BAND-STABILIZES"

    write_result("04_final", {
        "hypotheses": {
            "H1": "Spearman(T, rate) stays within [0.55, 0.85] on uniform "
                  "draws at bitlen 108, u=2.5",
            "H2": "T beats count <=100 by > +0.05"},
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
        "comparisons": {"prior_rho_96_fixed": PRIOR_96,
                         "prior_rho_100": PRIOR_100,
                         "prior_rho_104": PRIOR_104,
                         "delta_vs_104": pT - PRIOR_104,
                         "ci95_vs_band_lower_edge": ci_pos,
                         "further_decline_vs_104": further_decline},
        "verdicts": {"H1_pass": h1, "H1_pass_per_seed": h1_per_seed,
                     "H2_pass": h2,
                     "verdict_name": verdict},
    })
    print(f"[{time.time()-T_START:.0f}s] FINAL: pooled rho_T={pT:.4f} "
          f"CI[{ciT[0]:.4f},{ciT[1]:.4f}] rho_cnt={pC:.4f} "
          f"adv={adv:+.4f} CI[{ciA[0]:.4f},{ciA[1]:.4f}] "
          f"H1={h1} H2={h2} VERDICT={verdict}", flush=True)
    print("RUN_DONE", flush=True)


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

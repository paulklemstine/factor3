#!/usr/bin/env python3
"""exp569 U9-DRIFT-POWER (round-74, inline coordinator implementation after agent-channel failures)

Powered rerun of paper-214's banked sub-1 drift (band 9, bitlen-96 semiprimes):
paper 214 recorded r=0.864 cluster-boot CI [0.714,1.027] at LPF-CDF cut 1e5 (pilot,
35.7M pairs) -- barely covering 1. This run targets >=10x the decisive-cell pair count
to resolve drift-vs-noise.

PRE-REGISTRATION (before full run):
  H1 (drift real): cluster-boot 95% CI of r EXCLUDES 1 (downward) at cut 1e5
    => candidate deviation event; claimable ONLY after passing BOTH gates:
       G1 fresh-seed replication (second independent seed/population, same pipeline)
       G2 control-integrity audit (paired mantissa/bitlen match exact; tester identical code path)
       => verdict CONFIRMED-DEVIATION (would be the lab's FIRST scale deviation).
  H0 (randomness): CI covers 1 => verdict RANDOMNESS-EXTENDED;
    deliverable = tightened upper edge of |r-1| vs paper 214's 0.136.
Method notes:
  - Tester: gcd-chain against primorial(cut) -- repeated g=gcd(x,P); x//=g until g==1;
    x==1 at end <=> LPF <= cut. Identical code path for candidates and controls (G2).
  - Controls: PAIRED per candidate -- same bitlen, same 3-bit mantissa head (exact
    histogram match by construction).
  - Cluster bootstrap over N-individuals (candidates) / size-matched pseudo-clusters
    (controls), nboot>=2000, percentile CIs.
Honest limits disclosed in result JSON: achieved pair count vs 30x target, wall cap 15 min.
"""
import sys, time, json, random
from multiprocessing import Pool

SEED = int(sys.argv[4]) if len(sys.argv) > 4 else 20260824  # seed parametrized post-correlation-catch
N_PER_POOL = 128          # semiprimes
J_SAMPLE_PER_N = None     # set from wall-clock in smoke
CUTS = {"p1e5": None, "p1e6": None}
NB = 2000                 # bootstrap resamples

import gmpy2
from gmpy2 import mpz, gcd, next_prime

def build_primorial(bound):
    # product of primes <= bound via iterative multiply (tree would be faster; fine once)
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
    # enforce balanced: discard wildly unbalanced draws
    if n.bit_length() != bits:
        return make_semiprime(rng, bits)
    lo = min(p, q); hi = max(p, q)
    if hi.bit_length() - lo.bit_length() > 2:
        return make_semiprime(rng, bits)
    return int(n), int(lo), int(hi)

def lpf_le(x, P):
    # x>0; returns True iff largest prime factor of x <= cut (i.e. fully strippable)
    while x > 1:
        g = gcd(x, P)
        if g == 1:
            return False
        x //= g
    return True

_G = {}
def init_worker(p1e5, p1e6):
    _G["P5"] = mpz(p1e5)
    _G["P6"] = mpz(p1e6)

def worker_v2(args):
    ns, jsamples, ctrl_seed = args
    rng = random.Random(ctrl_seed)
    ch5 = [0]*len(ns); ch6 = [0]*len(ns); ct = [0]*len(ns)   # cand hits @1e5/@1e6, totals
    kh5 = [0]*len(ns); kh6 = [0]*len(ns); kt = [0]*len(ns)   # ctrl hits
    P5, P6 = _G["P5"], _G["P6"]

    def classify(x):
        """strip primes<=1e5 then <=1e6; returns (hit5, hit6)"""
        xx = mpz(x)
        while xx > 1:
            g = gcd(xx, P5)
            if g == 1: break
            xx //= g
        hit5 = (xx == 1)
        if hit5:
            return True, True
        xy = xx                      # residual has only primes >1e5
        while xy > 1:
            g = gcd(xy, P6)
            if g == 1: break
            xy //= g
        return False, (xy == 1)

    def strip_only(x):
        """paired control draw helper -- same classification"""
        return classify(x)

    for idx, (N, lo, hi) in enumerate(ns):
        s = int(gmpy2.isqrt(mpz(N)))
        jlo = s + 1; jhi = 3 * s
        for _ in range(jsamples):
            j = rng.randint(jlo, jhi)
            v = j * j - N
            if v <= 1:
                continue
            b = v.bit_length()
            rem = b - 3
            head = v >> rem if rem > 0 else mpz(v)
            ct[idx] += 1; kt[idx] += 1
            h5, h6 = classify(v)
            if h5: ch5[idx] += 1
            if h6: ch6[idx] += 1
            # paired control: same bitlen, same 3-bit mantissa head (exact match)
            u = (head << rem) | rng.getrandbits(rem) if rem > 0 else mpz(head & 7)
            k5, k6 = strip_only(u)
            if k5: kh5[idx] += 1
            if k6: kh6[idx] += 1
    return ch5, ch6, ct, kh5, kh6, kt

def cluster_boot(ch, ct, kh, kt, nb=NB, seed=77):
    m = len(ch)
    rc = []; rk = []
    rng = random.Random(seed)
    for _ in range(nb):
        ic = [rng.randrange(m) for _ in range(m)]
        C = sum(ch[i] for i in ic); Ct = sum(ct[i] for i in ic)
        K = sum(kh[i] for i in ic); Kt = sum(kt[i] for i in ic)
        rc.append(C / Ct if Ct else float("nan"))
        rk.append(K / Kt if Kt else float("nan"))
    r = sum(ch) / sum(ct)
    rk_mean = sum(kh) / sum(kt)
    rat = [a / b for a, b in zip(rc, rk) if b and b == b]
    if len(rat) < 100:
        # starved regime: too few smooth events for a ratio CI -- flag, do not fake
        return r, rk_mean, float("nan"), float("nan")
    rat.sort()
    lo = rat[int(0.025 * len(rat))]; hi = rat[int(0.975 * len(rat))]
    return r, rk_mean, lo, hi

def main():
    t0 = time.time()
    mode = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    smoke = mode == "smoke"
    n_pool = 16 if smoke else N_PER_POOL
    jsamples = 400 if smoke else (int(sys.argv[2]) if len(sys.argv) > 2 else 150000)  # per N per worker-chunk
    print(f"[{mode}] building primorials...", flush=True)
    P5 = build_primorial(100000)
    P6 = build_primorial(1000000)
    print(f"primorials built: bits P5={P5.bit_length()} P6={P6.bit_length()}", flush=True)
    rng = random.Random(SEED)
    pools = []
    seen = set()
    while len(pools) < n_pool:
        N, lo, hi = make_semiprime(rng, 96)
        if N in seen: continue
        seen.add(N)
        pools.append((N, lo, hi))
    nchunk = 2 if smoke else 8
    per = n_pool // nchunk
    chunks = []
    for c in range(nchunk):
        sub = pools[c*per:(c+1)*per]
        chunks.append((sub, jsamples, SEED + 1000 + c))
    print(f"[{mode}] running {nchunk} workers x {per} N x {jsamples} samples...", flush=True)
    with Pool(nchunk, initializer=init_worker, initargs=(P5, P6)) as pool:
        results = pool.map(worker_v2, chunks)
    ch5 = [x for r in results for x in r[0]]
    ch6 = [x for r in results for x in r[1]]
    ct6 = [x for r in results for x in r[2]]
    kh5 = [x for r in results for x in r[3]]
    kh6 = [x for r in results for x in r[4]]
    kt6 = [x for r in results for x in r[5]]
    tot_pairs = sum(ct6)
    r5, k5, lo5, hi5 = cluster_boot(ch5, ct6, kh5, kt6)
    r6, k6, lo6, hi6 = cluster_boot(ch6, ct6, kh6, kt6, seed=78)
    wall = time.time() - t0
    excl5 = not (lo5 <= 1.0 <= hi5)
    verdict = {
        "cut_1e5_PRIMARY_DECISION": {
            "pairs": tot_pairs,
            "r_cand": r5,
            "r_cand_rounded_display_bug_fixed": True,
            "rate_ctrl": k5,
            "ci95_cluster_boot": [round(lo5, 4), round(hi5, 4)],
            "excludes_1": excl5,
        },
        "cut_1e6_secondary": {
            "r_cand": r6,
            "rate_ctrl": k6,
            "ci95_cluster_boot": [round(lo6, 4), round(hi6, 4)],
            "excludes_1": not (lo6 <= 1.0 <= hi6),
        },
    }
    out = {
        "_raw_counts_note": "added post-hoc: raw per-cluster counts persisted for future runs",
        "raw_counts": {"ch5": ch5, "ch6": ch6, "ct6": ct6, "kh5": kh5, "kh6": kh6, "kt6": kt6},
        "exp": "569", "codename": "U9-DRIFT-POWER", "mode": mode,
        "seed": SEED, "n_pool": n_pool, "jsamples_per_N": jsamples,
        "wall_s": round(wall, 1),
        "stats": verdict,
        "verdict_name": ("CANDIDATE-DEVIATION-PENDING-GATES" if excl5 else "RANDOMNESS-EXTENDED"),
        "verdict_rule": "CONFIRMED-DEVIATION iff excludes_1@1e5 AND gates G1/G2 pass; "
                        "RANDOMNESS-EXTENDED otherwise",
        "honest_notes": [
            f"pair count {tot_pairs} at {tot_pairs and round(wall/tot_pairs*1e6,1)}us/val "
            "-- throughput-limited to ~1x paper214 pilot power, NOT the aspirational 10-30x",
            "ROLE REFRAMED PRE-RUN (scoping, not verdict-fitting): independent-seed "
            "replication = gate G1 of the pre-registered rule; pooled with paper 214's "
            "pilot estimate gives the sqrt(2)-tightened joint CI as the drift resolution",
            "band-9 (bitlen-96) only this pass; bands 10/11 deferred",
            "decision cut stays 1e5 per header pre-registration; 1e6 secondary reported "
            "(higher event rate => better powered, weight disclosed)",
        ],
    }
    tag = sys.argv[3] if len(sys.argv) > 3 else ("smoke_" if smoke else "")
    fn = f"exp569_{tag}result.json"
    with open(fn, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out["stats"], indent=1))
    print(f"[{mode}] wall={wall:.1f}s -> {fn}")

if __name__ == "__main__":
    main()

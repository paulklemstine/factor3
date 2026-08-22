#!/usr/bin/env python3
"""exp512_t_dial_60.py -- round-49 experiment 512, codename T-DIAL-60.

Paper 178 found the paper-177 dial T(N) = sum 2/p over QR primes p <= 400
degrades at bitlen 56 (Spearman(T, rate) = 0.405, down from the validated
[0.55, 0.85] band at bitlen <= 52), attributing the drop to smooth-rate
starvation (rate_mean = 0.89%, 194/1200 zero-hit Ns).  Our job: confirm the
degradation CONTINUES at bitlen 60 and quantify whether it is monotone.

Everything stays inside /tmp/exp49_t60/.  Seed 20261040.  Budget <= 15 min.
"""

import bisect
import json
import math
import random
import statistics
import time
from datetime import datetime, timezone

try:
    import numpy as np
    HAVE_NUMPY = True
except Exception:
    HAVE_NUMPY = False

try:
    import gmpy2
    HAVE_GMPY2 = True
except Exception:
    HAVE_GMPY2 = False

from scipy.stats import spearmanr

# ===================== PRE-STATED HYPOTHESES (written BEFORE any data) ============
# Stated by the round-49 dispatcher BEFORE this script saw any bitlen-60 data:
SEED = 20261040
PRESTATED = {
    "H1": "Spearman(T, rate) < 0.405 at bitlen 60 (monotone continuation of "
          "the bitlen-56 degradation; paper-178 anchor rho_T = 0.4053).",
    "H2": "Spearman(T, rate) >= 0.405 -- the degradation plateaus rather than "
          "continuing.",
    "H3": "Spearman(T, rate) recovers above 0.55 -- the bitlen-56 drop was a "
          "transient.",
    # Decision rules frozen before data generation:
    "decision_rules": {
        "precedence": "H3 checked first, then H1, then H2.",
        "H3_recovery": "PASS iff rho_T > 0.55 -> verdict T-DIAL-60-RECOVERY.",
        "H1_monotone": "PASS iff rho_T < 0.405 AND bootstrap 95% CI upper "
                       "bound < 0.405 -> verdict T-DIAL-60-MONOTONE-CONTINUATION.",
        "H2_plateau": "PASS iff rho_T >= 0.405 -> verdict T-DIAL-60-PLATEAU.",
        "marginal": "if rho_T < 0.405 but CI straddles 0.405 (H1 not decisive, "
                    "H2 excluded by point) -> verdict "
                    "T-DIAL-60-MARGINAL-DEGRADATION (H1 direction, not decisive).",
    },
    # Frozen design decisions (made before data generation):
    "design": {
        "population": "1200 balanced semiprimes; p,q distinct uniform primes in "
                      "[ceil(2^29.5), 2^30-1]; guarantees bitlen(N)=60 exactly.",
        "draws": "per N: 240 relation values v = isqrt(N)+1+offset with offset ~ "
                 "Uniform{0..W-1}, W = round(N**0.25) (QS-style window above sqrt).",
        "dial_B": "B = exp(ln(vmed)/u), u=2.5; vmed = median of that N's 240 v "
                  "values (so u = ln(vmed)/ln(B) exactly on the v scale -- the "
                  "SAME convention as paper-178/exp511, whose 0.4053 is the "
                  "comparator).",
        "hit": "rem = v*v - N; strip primes <= B ascending; HIT iff rem==1 after "
               "strip or leftover prime cofactor <= B (early-break rescue); "
               "maxp<=B checked literally on every hit.",
        "features_paper164_verbatim": (
            "T(N) = sum over odd primes p<=400 with Euler criterion "
            "powmod(N,(p-1)//2,p)==1 of 2/p ; count(N) = #{odd primes q<=100 : "
            "Euler criterion ==1} (odd-only, mirroring T's definition)."),
        "stats": "Spearman rho(T,rate), rho(count,rate), advantage=rho_T-rho_count; "
                 "bootstrap 300 resamples (seed SEED+2), percentile 95% CIs; "
                 "monotonicity quantified as delta = rho_T(bitlen60) - 0.4053 "
                 "(paper-178/exp511 anchor; unpaired, independent seeds).",
        "rng_split": "Random(SEED) population, Random(SEED+1) draw offsets, "
                     "Random(SEED+2) bootstrap, Random(SEED+3) secondary bootstrap.",
        "secondary_arm_posthoc": "same draws, B2 = exp(ln(remmed)/2.5), remmed = "
                                 "median of that N's 240 remainders (u=2.5 realized "
                                 "ON THE REMAINDER scale) -- designed check on "
                                 "whether any continued drop is rate-starvation "
                                 "(primary convention) or genuine dial breakdown; "
                                 "clearly labeled POST-HOC, primary untouched.",
    },
}
# ==================================================================================

N_POP = 1200
N_DRAWS = 240
U_PARAM = 2.5
BITLEN = 60
ANCHOR_RHO_T_B56 = 0.4053          # paper-178 / exp511 point estimate
BOOT = 300
WD = "/tmp/exp49_t60"
RESULT = WD + "/result.json"
LEDGER = WD + "/ledger.md"
CSV = WD + "/relations.csv"
T0 = time.time()

RES = {
    "experiment": "exp512_t_dial_60",
    "codename": "T-DIAL-60",
    "round": 49,
    "seed": SEED,
    "prestated": PRESTATED,
    "have_gmpy2": HAVE_GMPY2,
    "have_numpy": HAVE_NUMPY,
    "stages": {},
}


def ckpt(stage, **kw):
    RES["stages"][stage] = dict(kw, ts=time.time() - T0)
    with open(RESULT, "w") as f:
        json.dump(RES, f, indent=1)
    with open(LEDGER, "a") as f:
        f.write("| %7.1fs | %-10s | %s |\n" % (
            time.time() - T0, stage,
            "; ".join("%s=%s" % kv for kv in kw.items())))
    print("[ckpt] %-10s %5.1fs %s" % (stage, time.time() - T0, kw), flush=True)


def ledger(msg):
    with open(LEDGER, "a") as f:
        f.write("| %7.1fs | action     | %s |\n" % (time.time() - T0, msg))
    print("[ledg] %s" % msg, flush=True)


def sieve(n):
    flags = bytearray([1]) * (n + 1)
    flags[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if flags[i]:
            flags[i * i:: i] = bytearray(len(flags[i * i:: i]))
    return [i for i in range(n + 1) if flags[i]]


PRIMES400 = [p for p in sieve(400) if p > 2]           # odd primes <= 400
PRIMES100 = [q for q in PRIMES400 if q <= 100]         # odd primes <= 100
PRIMES_BIG = sieve(6000)                               # strip-prime pool (primary B)
PRIMES_BIG2 = sieve(600000)                            # strip pool (secondary B2)


def euler(n, p):
    """Euler criterion: +1 iff N is a QR mod p."""
    r = int(gmpy2.powmod(n, (p - 1) // 2, p)) if HAVE_GMPY2 else pow(n, (p - 1) // 2, p)
    return r == 1


_MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)  # deterministic < 3.3e24


def is_prime(n):
    if n < 2:
        return False
    for p in _MR_BASES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _MR_BASES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def next_prime(n):
    c = n | 1
    while not is_prime(c):
        c += 2
    return c


# ---------------- Stage S1: sanity -------------------------------------------------
def stage_sanity():
    assert abs(spearmanr([1, 2, 3, 4], [1, 3, 2, 4])[0] - 0.8) < 1e-12
    t_hi = sum(2.0 / p for p in PRIMES400)
    assert 0 < t_hi < 3.3
    # Euler criterion spot checks: 4=2^2 is a nonzero square mod every odd prime.
    assert all(euler(4, p) for p in PRIMES400)
    assert all(euler((p - 1) ** 2, p) for p in PRIMES400)
    # Non-residue check: find an N that is a non-QR mod some p.
    found = any(not euler(n, 7) for n in range(2, 40))
    assert found
    ckpt("sanity", ok=True, n_primes_le400=len(PRIMES400),
         n_primes_le100=len(PRIMES100))


# ---------------- Stage S2: population ---------------------------------------------
def stage_population():
    rng = random.Random(SEED)
    lo = int(math.ceil(2.0 ** 29.5))          # 759250125
    hi = 2 ** 30 - 1
    primes = set()
    while len(primes) < 2 * N_POP:
        c = next_prime(rng.randrange(lo, hi))
        if c <= hi:
            primes.add(c)
    primes = sorted(primes)
    rng.shuffle(primes)
    rows = []
    seen_N = set()
    for i in range(N_POP):
        p, q = primes[2 * i], primes[2 * i + 1]
        N = p * q
        assert is_prime(p) and is_prime(q) and p != q
        assert lo <= p <= hi and lo <= q <= hi
        assert N.bit_length() == BITLEN, N.bit_length()
        assert N not in seen_N
        seen_N.add(N)
        rows.append({"p": p, "q": q, "N": N})
    RES["population"] = {
        "n": len(rows), "bitlen": BITLEN,
        "prime_range": [lo, hi],
        "distinct_primes": 2 * N_POP,
        "dup_N": 0,
    }
    ckpt("population", n=len(rows), lo=lo, hi=hi,
         bitlen_check="all==%d" % BITLEN)
    return rows


# ---------------- Stage S3: features -----------------------------------------------
def stage_features(rows):
    for r in rows:
        N = r["N"]
        r["T"] = sum(2.0 / p for p in PRIMES400 if euler(N, p))
        r["count"] = sum(1 for q in PRIMES100 if euler(N, q))
    ts = [r["T"] for r in rows]
    cs = [r["count"] for r in rows]
    RES["features"] = {
        "T_min": min(ts), "T_max": max(ts),
        "T_mean": statistics.fmean(ts), "T_sd": statistics.pstdev(ts),
        "count_min": min(cs), "count_max": max(cs),
        "count_mean": statistics.fmean(cs),
        "theoretical_T_ceiling": sum(2.0 / p for p in PRIMES400),
    }
    ckpt("features", T_mean=round(RES["features"]["T_mean"], 4),
         T_range=[round(min(ts), 3), round(max(ts), 3)],
         count_mean=round(RES["features"]["count_mean"], 3))
    return rows


# ---------------- Stage S4: sampling / relation rates ------------------------------
# Primary arm: B keyed to vmed (u=2.5 on the v scale) -- IDENTICAL convention to
# exp511/paper-178 so rho_T is directly comparable against the 0.4053 anchor.
# Secondary arm (POST-HOC, added at design time, run AFTER primary per-N loop):
# B2 keyed to remmed (u=2.5 on the remainder scale), same draws, numpy-vectorized;
# mechanism check: starvation (primary) vs genuine dial breakdown (both arms).
def stage_sampling(rows):
    rng = random.Random(SEED + 1)
    Bs, rates, rem_meds = [], [], []
    Bs2, rates2 = [], []
    total_hits = 0
    total_hits2 = 0
    with open(CSV, "w") as f:
        f.write("idx,p,q,N,T,count,B,vmed,hits,rate,B2,remmed,hits2,rate2\n")
        for k, r in enumerate(rows):
            N = r["N"]
            sq = math.isqrt(N)
            W = max(2, int(round(N ** 0.25)))
            vs = sorted(sq + 1 + rng.randrange(W) for _ in range(N_DRAWS))
            vmed = statistics.median(vs)
            B = max(2, int(math.exp(math.log(vmed) / U_PARAM)))
            pb = PRIMES_BIG[: bisect.bisect_right(PRIMES_BIG, B)]
            hits = 0
            for v in vs:
                rem = v * v - N
                for p in pb:
                    if p * p > rem:
                        break
                    if rem % p == 0:
                        rem //= p
                        while rem % p == 0:
                            rem //= p
                if rem == 1 or (1 < rem <= B):   # leftover cofactor is a prime <= B
                    hits += 1
            rate = hits / N_DRAWS
            total_hits += hits
            Bs.append(B)
            rates.append(rate)
            remmed = statistics.median(v * v - N for v in vs)
            rem_meds.append(remmed)
            # ---- post-hoc secondary arm (same draws; numpy-vectorized strip) ----
            hits2 = None
            if HAVE_NUMPY:
                B2 = max(2, int(math.exp(math.log(remmed) / U_PARAM)))
                pb2 = PRIMES_BIG2[: bisect.bisect_right(PRIMES_BIG2, B2)]
                ra = np.array([v * v - N for v in vs], dtype=np.int64)
                for p in pb2:
                    while True:
                        m = ra % p == 0
                        if not m.any():
                            break
                        ra[m] //= p
                hits2 = int(np.count_nonzero(ra == 1))   # all primes <= B2 tested
                total_hits2 += hits2
                Bs2.append(B2)
                rates2.append(hits2 / N_DRAWS)
            r.update(B=B, vmed=vmed, hits=hits, rate=rate)
            if hits2 is not None:
                r.update(B2=B2, hits2=hits2, rate2=hits2 / N_DRAWS)
                f.write("%d,%d,%d,%d,%.6f,%d,%d,%d,%d,%.6f,%d,%d,%d,%.6f\n" %
                        (k, r["p"], r["q"], N, r["T"], r["count"], B, vmed, hits,
                         rate, B2, remmed, hits2, hits2 / N_DRAWS))
            else:
                f.write("%d,%d,%d,%d,%.6f,%d,%d,%d,%d,%.6f,,,,\n" %
                        (k, r["p"], r["q"], N, r["T"], r["count"], B, vmed, hits, rate))
            if (k + 1) % 200 == 0:
                print("  sampled %d/%d  elapsed %.1fs" % (k + 1, N_POP, time.time() - T0),
                      flush=True)
    u_eff = math.log(statistics.median(rem_meds)) / math.log(statistics.median(Bs))
    RES["sampling"] = {
        "draws_per_n": N_DRAWS, "total_draws": N_POP * N_DRAWS,
        "total_hits": total_hits,
        "rate_mean": statistics.fmean(rates),
        "rate_zero_n": sum(1 for x in rates if x == 0.0),
        "B_median": statistics.median(Bs), "B_min": min(Bs), "B_max": max(Bs),
        "design_u_on_v_scale": U_PARAM,
        "effective_u_on_rem_median": round(u_eff, 3),
        "window_W_median": int(statistics.median(
            [max(2, int(round(r['N'] ** 0.25))) for r in rows])),
    }
    ckpt("sampling", total_hits=total_hits,
         rate_mean=round(RES["sampling"]["rate_mean"], 5),
         zero_hit_Ns=RES["sampling"]["rate_zero_n"],
         B_median=RES["sampling"]["B_median"], u_eff=round(u_eff, 3))
    if HAVE_NUMPY:
        RES["sampling_secondary"] = {
            "note": "POST-HOC: same draws, B2 = exp(ln(remmed)/2.5) -- u=2.5 on the "
                    "remainder scale; not part of the pre-stated primary analysis",
            "total_hits2": total_hits2,
            "rate2_mean": statistics.fmean(rates2),
            "rate2_zero_n": sum(1 for x in rates2 if x == 0.0),
            "B2_median": statistics.median(Bs2),
            "B2_min": min(Bs2), "B2_max": max(Bs2),
        }
        ckpt("sampling_secondary", total_hits2=total_hits2,
             rate2_mean=round(RES["sampling_secondary"]["rate2_mean"], 5),
             zero_hit2_Ns=RES["sampling_secondary"]["rate2_zero_n"],
             B2_median=RES["sampling_secondary"]["B2_median"])
    return rows


# ---------------- Stage S5: stats + verdicts ---------------------------------------
def pct_ci(xs, alpha=0.05):
    xs = sorted(xs)
    m = len(xs) - 1
    def q(a):
        pos = a * m
        fl = int(pos)
        return xs[fl] + (xs[min(fl + 1, m)] - xs[fl]) * (pos - fl)
    return q(alpha / 2), q(1 - alpha / 2)


def stage_stats(rows):
    T = [r["T"] for r in rows]
    C = [float(r["count"]) for r in rows]
    R = [r["rate"] for r in rows]
    n = len(rows)
    rho_T = float(spearmanr(T, R)[0])
    rho_C = float(spearmanr(C, R)[0])
    boot_T, boot_C, boot_D = [], [], []
    rb = random.Random(SEED + 2)
    for _ in range(BOOT):
        idx = rb.choices(range(n), k=n)
        bt = float(spearmanr([T[i] for i in idx], [R[i] for i in idx])[0])
        bc = float(spearmanr([C[i] for i in idx], [R[i] for i in idx])[0])
        boot_T.append(bt)
        boot_C.append(bc)
        boot_D.append(bt - bc)
    ci_T = pct_ci(boot_T)
    ci_C = pct_ci(boot_C)
    adv = rho_T - rho_C
    ci_D = pct_ci(boot_D)

    # ---- pre-stated decision rules (see PRESTATED.decision_rules) ----
    h3_pass = rho_T > 0.55
    h1_pass = (rho_T < ANCHOR_RHO_T_B56) and (ci_T[1] < ANCHOR_RHO_T_B56)
    h2_pass = rho_T >= ANCHOR_RHO_T_B56
    if h3_pass:
        verdict = "T-DIAL-60-RECOVERY"
    elif h1_pass:
        verdict = "T-DIAL-60-MONOTONE-CONTINUATION"
    elif h2_pass:
        verdict = "T-DIAL-60-PLATEAU"
    else:
        verdict = "T-DIAL-60-MARGINAL-DEGRADATION"

    delta = rho_T - ANCHOR_RHO_T_B56
    RES["stats"] = {
        "rho_T": rho_T, "ci_T": list(ci_T),
        "rho_count": rho_C, "ci_count": list(ci_C),
        "advantage": adv, "ci_advantage": list(ci_D),
        "bootstrap_resamples": BOOT,
        "anchor_rhoT_bitlen56": ANCHOR_RHO_T_B56,
        "delta_vs_bitlen56": delta,
        "pearson_T_rate": None,
    }
    try:
        import numpy as np
        RES["stats"]["pearson_T_rate"] = float(np.corrcoef(T, R)[0, 1])
    except Exception:
        pass
    RES["verdicts"] = {
        "H1_monotone_continuation": "PASS" if h1_pass else "FAIL",
        "H2_plateau": "PASS" if h2_pass else "FAIL",
        "H3_recovery": "PASS" if h3_pass else "FAIL",
        "verdict_name": verdict,
    }
    ckpt("stats", rho_T=round(rho_T, 4), ci_T=[round(x, 4) for x in ci_T],
         rho_count=round(rho_C, 4), advantage=round(adv, 4),
         ci_adv=[round(x, 4) for x in ci_D],
         delta_vs_b56=round(delta, 4),
         H1=RES["verdicts"]["H1_monotone_continuation"],
         H2=RES["verdicts"]["H2_plateau"],
         H3=RES["verdicts"]["H3_recovery"], verdict=verdict)

    # ---- post-hoc secondary correlations (clearly labeled; not pre-stated) ----
    if HAVE_NUMPY and all("rate2" in r for r in rows):
        R2 = [r["rate2"] for r in rows]
        rho_T2 = float(spearmanr(T, R2)[0])
        rho_C2 = float(spearmanr(C, R2)[0])
        boot_T2, boot_D2 = [], []
        rb2 = random.Random(SEED + 3)
        for _ in range(BOOT):
            idx = rb2.choices(range(n), k=n)
            boot_T2.append(float(spearmanr([T[i] for i in idx],
                                           [R2[i] for i in idx])[0]))
            boot_D2.append(float(spearmanr([T[i] for i in idx],
                                           [R2[i] for i in idx])[0]) -
                           float(spearmanr([C[i] for i in idx],
                                           [R2[i] for i in idx])[0]))
        ci_T2 = pct_ci(boot_T2)
        RES["stats_secondary"] = {
            "note": "POST-HOC: same draws, B keyed to remainder median "
                    "(u=2.5 on remainder scale); designed check on the "
                    "degradation mechanism",
            "rho_T": rho_T2, "ci_T": list(ci_T2),
            "rho_count": rho_C2,
            "advantage": rho_T2 - rho_C2,
            "anchor_rhoT2_bitlen56": 0.5930,   # exp511 secondary point estimate
        }
        ckpt("stats_secondary", rho_T2=round(rho_T2, 4),
             ci_T2=[round(x, 4) for x in ci_T2], rho_count2=round(rho_C2, 4))


def main():
    with open(LEDGER, "a") as f:
        f.write("# Ledger exp512_t_dial_60 (T-DIAL-60, round-49) -- %s\n"
                % datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
        f.write("| elapsed | stage | detail |\n|---|---|---|\n")
    ledger("launch exp512_t_dial_60 seed=%d gmpy2=%s numpy=%s"
           % (SEED, HAVE_GMPY2, HAVE_NUMPY))
    stage_sanity()
    rows = stage_population()
    stage_features(rows)
    stage_sampling(rows)
    stage_stats(rows)
    RES["runtime_s"] = round(time.time() - T0, 1)
    RES["barrier_lines"] = {
        "(5)": "which-factor wall untouched: T and count are factor-BLIND "
               "relation-rate predictors; no which-factor or symmetric-channel "
               "reading computed anywhere in this experiment.",
        "(8)": "toy-scale scope: bitlen-%d semiprimes only; no poly(log N) or "
               "subexponential route claimed; rank correlations do not "
               "extrapolate beyond the measured regime." % BITLEN,
    }
    RES["caveats"] = [
        "window law W=round(N**0.25) with uniform offsets chosen from the design "
        "line; paper-177's exact draw law was not restatable in isolation, so rate "
        "LEVELS may differ while the rank correlations remain the comparanda",
        "count<=100 excludes p=2, mirroring the odd-only definition of T",
        "u=2.5 realized per design on the v scale (B keyed to vmed), SAME "
        "convention as exp511/paper-178; effective u on the remainder scale is "
        "~3.75 -- see sampling_secondary/stats_secondary (post-hoc) for the "
        "same-draws remainder-scale check",
        "single seed (%d), single window law; the cross-bitlen delta vs 0.4053 is "
        "UNPAIRED (independent seeds and populations)" % SEED,
        "int64 safety: v*v-N < 2^61 fits numpy int64 in the secondary arm; "
        "bitlen >= 63 would overflow and needs the object-dtype fallback",
    ]
    with open(RESULT, "w") as f:
        json.dump(RES, f, indent=1)
    ledger("DONE verdict=%s rho_T=%.4f ci=[%.4f,%.4f] rate_mean=%.5f runtime=%.1fs"
           % (RES["verdicts"]["verdict_name"],
              RES["stats"]["rho_T"], RES["stats"]["ci_T"][0], RES["stats"]["ci_T"][1],
              RES["sampling"]["rate_mean"], RES["runtime_s"]))


if __name__ == "__main__":
    main()

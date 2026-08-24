#!/usr/bin/env python3
"""exp575_generator_tilt.py -- EXP575 GENERATOR-TILT (paper-221 named open item L7-a)

Question: does the within-window divisor-mass tilt (bottom-heavy z<0.45) that makes
window-ascending beat sqrt-descending (1.58x+-0.03 under hard q<2p balance; see
gapL7_extremality.md FAILURE-1 / verifyL7_sim.py) exist in REALISTIC semiprime
generators -- especially RSA-style independent same-bitlength primes?

========================= PRE-REGISTRATION =========================
Fixed BEFORE any data generation (this header precedes this file's first run).

H1 (tilt is real-world): the RSA-style pool (p,q INDEPENDENT uniform primes over
    [2^14,2^15), b=15) shows mean within-window divisor-mass z < 0.45 with 95% CI
    excluding 0.45 from above (bottom-heavy tilt, matching the analytic 0.37-0.41
    band) => Lambda-dominance SCOPE COVERS deployed-like generation; the
    window-ascending gain ~1.5-1.6x is AVAILABLE there (recorded as a scoped
    reorder-class fact, NOT a speed prescription).
H0 (tilt absent): RSA-style z ~= 0.5 with 95% CI covering 0.50 (no bottom-heaviness
    outside hard-balance construction) => Lambda-dominance confined to artificial
    hard-balance pools; paper-221's caveat stands as the final word.
VERDICT RULES (pre-stated):
    H1 confirmed  <=> z_mean(RSA_INDEP) < 0.45 AND CI95_upper(RSA_INDEP) < 0.45
    H0 confirmed  <=> CI95(RSA_INDEP) contains 0.50
    otherwise     => MIXED/PARTIAL (described explicitly).
SECONDARY GATE: under H1 the measured win_asc/descending touch-ratio on the RSA pool
    should exceed 1 significantly (expected ~1.4-1.6x); under H0 it should be ~1.

METHOD
  Populations x4, n>=400 each (full run n=600/pop), fixed seed, b=15:
    HARD_BAL     : p prime U[2^14,2^15); q prime in (p,2p)  [POSITIVE CONTROL:
                   must replicate verifier BAL_prime z~0.41, S(win_asc)~1.58]
    RSA_INDEP    : p,q independent uniform primes over [2^14,2^15), p!=q, sorted
    RATIO4       : p as above; q prime U[3.5p, 4.5p)       [wide-unbalance stratum]
    UNIFORM_WIDE : p,q independent uniform primes over [2^13,2^16), sorted [uniform proxy]
  Tilt statistic REUSED VERBATIM from verifyL7_sim.py:
      z = (p - lo_w) / (M - lo_w),  M = isqrt(N),  lo_w = isqrt(max(2, N//2))
    canonical window = (sqrt(N/2), sqrt(N)].
  WINDOW ADAPTATIONS PER POOL (per gapL7_extremality.md, documented here):
   - HARD_BAL / RSA_INDEP: canonical window PROVABLY contains min(p,q)
     (max/min < 2 by construction: q<2p resp. same-bitlen) -> NO adaptation; the
     empirical in-window fraction is reported as a check (expect 1.0).
   - RATIO4 (ratio support [3.5,4.5)) and UNIFORM_WIDE (support (0.5,8)): canonical
     window does NOT contain the min factor on most draws (md convention: "window
     policy undefined"). We ADD an N-COMPUTABLE ADAPTED window
         lo_a = isqrt(N / r_max),  r_max = 4.5 resp. 8.0,
     with r_max taken from the DECLARED pool support bound (not fitted), and the
     SAME z formula. Canonical z (in-window draws only + miss fraction) and
     adapted z are both reported.
  COSTS (secondary): exact O(1)/draw touch-counts, verifier conventions:
      desc = M - f + 1;  asc_full = f - 1;  win_asc = f - lo_w + 1 (valid draws);
      win_asc_adapted = f - lo_a + 1 (adapted pools, valid draws).
    S = mean(desc)/mean(arm) on the arm's VALID draw subset (desc restricted to the
    same subset), 8-batch bootstrap SE -- verbatim verifyL7_sim.py estimator.
    Pairing column: predicted ratio from tilt, (1 - z_mean)/z_mean.
"""
import json, math, random, statistics, sys, time
from bisect import bisect_left, bisect_right
from math import isqrt

import numpy as np

T0 = time.time()
OUT_DIR = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74"
BASE_SEED = 20260824
B_BITS = 15
PL, PH = 2 ** (B_BITS - 1), 2 ** B_BITS          # [16384, 32768)
WIDE_LO, WIDE_HI = 2 ** 13, 2 ** 16              # uniform-proxy support
SIEVE_LIMIT = 150000                             # covers 4.5*PH < 147456
NBATCH = 8
Z_BAR = 0.45                                     # H1/H0 decision threshold
ADAPT_R = {"RATIO4": 4.5, "UNIFORM_WIDE": 8.0}   # N-computable adapted-window bounds
POOL_DESC = {
    "HARD_BAL":     "p~U primes[2^14,2^15); q~U primes(p,2p)  [positive control]",
    "RSA_INDEP":    "p,q indep U primes[2^14,2^15), p!=q, sorted  [RSA-style]",
    "RATIO4":       "p~U primes[2^14,2^15); q~U primes[3.5p,4.5p)",
    "UNIFORM_WIDE": "p,q indep U primes[2^13,2^16), sorted  [uniform proxy]",
}


def sieve_primes(limit):
    s = np.ones(limit, dtype=bool)
    s[:2] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.flatnonzero(s).tolist()


PRIMES = sieve_primes(SIEVE_LIMIT)


def sample_prime(rng, a, b):
    """Exact-uniform prime in [a, b) by index sampling (no MR-rejection bias)."""
    i, j = bisect_left(PRIMES, a), bisect_right(PRIMES, b - 1)
    if j <= i:
        raise ValueError(f"no primes in [{a},{b})")
    return int(PRIMES[rng.randrange(i, j)])


def gen_pool(name, n, rng):
    """Population machinery adapted from verifyL7_sim.py gen() (bitlen shifted to b=15,
    uniform-over-primes via sieve-index sampling instead of randprime). Returns [(N,f)]."""
    pop = []
    while len(pop) < n:
        if name == "HARD_BAL":
            p = sample_prime(rng, PL, PH)
            q = sample_prime(rng, p + 1, 2 * p)
            f = p
        elif name == "RSA_INDEP":
            p = sample_prime(rng, PL, PH)
            q = sample_prime(rng, PL, PH)
            if p == q:
                continue
            f = min(p, q)
        elif name == "RATIO4":
            p = sample_prime(rng, PL, PH)
            q = sample_prime(rng, (7 * p) // 2, (9 * p + 1) // 2)  # [3.5p, 4.5p)
            f = p
        elif name == "UNIFORM_WIDE":
            p = sample_prime(rng, WIDE_LO, WIDE_HI)
            q = sample_prime(rng, WIDE_LO, WIDE_HI)
            if p == q:
                continue
            f = min(p, q)
        else:
            raise ValueError(name)
        pop.append((p * q, f))
    return pop


def zstats(zs):
    zs = sorted(zs)
    m = len(zs)
    mean = sum(zs) / m
    sd = statistics.pstdev(zs)
    half = 1.96 * sd / math.sqrt(m)

    def q(f):
        return zs[min(m - 1, int(f * (m - 1)))]

    return {"n": m, "mean": round(mean, 4),
            "ci95": [round(mean - half, 4), round(mean + half, 4)],
            "deciles": [round(q(f), 3) for f in (0.1, 0.3, 0.5, 0.7, 0.9)]}


def s_stat(desc_b, arm_b):
    """S = mean(desc)/mean(arm) on common valid subset; batch-bootstrap SE (verbatim)."""
    md = sum(sum(x) for x in desc_b); nd = sum(len(x) for x in desc_b)
    ma = sum(sum(x) for x in arm_b); na = sum(len(x) for x in arm_b)
    sb = [(sum(d) / len(d)) / (sum(a) / len(a))
          for d, a in zip(desc_b, arm_b) if d and a]
    se = statistics.pstdev(sb) / math.sqrt(len(sb)) if len(sb) > 1 else float("nan")
    return {"cost_desc": round(md / nd, 2), "cost_arm": round(ma / na, 2),
            "S": round((md / nd) / (ma / na), 4), "S_se": round(se, 4), "hits": na}


def analyze(name, n, seed_off):
    rng = random.Random(BASE_SEED + seed_off)
    pop = gen_pool(name, n, rng)
    r_max = ADAPT_R.get(name)
    zs_c, zs_a = [], []
    miss_c = 0
    arms = ["asc_full", "win_asc", "win_asc_adapted"]
    B = {k: [[] for _ in range(NBATCH)] for k in arms}
    D = {k: [[] for _ in range(NBATCH)] for k in ["all"] + arms}
    for i, (N, f) in enumerate(pop):
        M = isqrt(N)
        lo_w = isqrt(max(2, N // 2))
        lo_a = isqrt(max(2, int(round(N / r_max)))) if r_max else None
        b = i % NBATCH
        cd = M - f + 1                      # sqrt-descending rank (verbatim)
        D["all"][b].append(cd)
        B["asc_full"][b].append(f - 1)      # full ascending from 2 (verbatim)
        D["asc_full"][b].append(cd)
        if f >= lo_w:                       # canonical window (sqrt(N/2),sqrt(N)]
            zs_c.append((f - lo_w) / (M - lo_w))
            B["win_asc"][b].append(f - lo_w + 1)
            D["win_asc"][b].append(cd)
        else:
            miss_c += 1
        if lo_a is not None and f >= lo_a:  # adapted window (sqrt(N/r_max),sqrt(N)]
            zs_a.append((f - lo_a) / (M - lo_a))
            B["win_asc_adapted"][b].append(f - lo_a + 1)
            D["win_asc_adapted"][b].append(cd)
    row = {"pool": name, "description": POOL_DESC[name], "n_draws": n}
    row["canonical_window"] = {"z": zstats(zs_c) if zs_c else None,
                               "in_window_frac": round((n - miss_c) / n, 4)}
    if zs_a:
        row["adapted_window"] = {"r_max": r_max, "z": zstats(zs_a)}
    row["costs"] = {"asc_full_vs_desc": s_stat(D["asc_full"], B["asc_full"])}
    if any(len(x) for x in B["win_asc"]):
        st = s_stat(D["win_asc"], B["win_asc"])
        st["pred_S_from_z"] = round((1 - row["canonical_window"]["z"]["mean"]) /
                                    row["canonical_window"]["z"]["mean"], 4)
        row["costs"]["win_asc_vs_desc"] = st
    if any(len(x) for x in B["win_asc_adapted"]):
        st = s_stat(D["win_asc_adapted"], B["win_asc_adapted"])
        st["pred_S_from_z"] = round((1 - row["adapted_window"]["z"]["mean"]) /
                                    row["adapted_window"]["z"]["mean"], 4)
        row["costs"]["win_asc_adapted_vs_desc"] = st
    return row


def main(mode):
    n_pop = 40 if mode == "smoke" else 600
    order = ["HARD_BAL", "RSA_INDEP", "RATIO4", "UNIFORM_WIDE"]
    rows = {name: analyze(name, n_pop, i + 1) for i, name in enumerate(order)}

    print("=" * 78)
    print(f"EXP575 GENERATOR-TILT ({mode})  b={B_BITS}  n={n_pop}/pool  "
          f"seed={BASE_SEED}  sieve<={SIEVE_LIMIT}")
    for name in order:
        r = rows[name]
        cz = r["canonical_window"]
        zline = (f"z_mean={cz['z']['mean']} CI95={cz['z']['ci95']} "
                 f"deciles={cz['z']['deciles']} in_win={cz['in_window_frac']}"
                 if cz["z"] else "z: none in window")
        print(f"\n--- {name} ({r['description']}) ---")
        print(f"  CANONICAL  {zline}")
        if "adapted_window" in r:
            az = r["adapted_window"]["z"]
            print(f"  ADAPTED(r_max={r['adapted_window']['r_max']}) "
                  f"z_mean={az['mean']} CI95={az['ci95']} deciles={az['deciles']}")
        for k, v in r["costs"].items():
            print(f"  {k:26s} desc_cost={v['cost_desc']:>8} arm_cost={v['cost_arm']:>8} "
                  f"S={v['S']:>7}(+-{v['S_se']}) hits={v['hits']}"
                  + (f" pred_from_z={v['pred_S_from_z']}" if "pred_S_from_z" in v else ""))

    # ---------------- verdicts (pre-registered rules) ----------------
    rsa = rows["RSA_INDEP"]["canonical_window"]["z"]
    rsa_lo, rsa_hi = rsa["ci95"]
    verdict, consequence = None, None
    if rsa["mean"] < Z_BAR and rsa_hi < Z_BAR:
        verdict = "H1"
        consequence = (
            "Lambda-dominance SCOPE COVERS deployed-like (RSA-style independent "
            "same-bitlen) generation: the within-window divisor-mass tilt is not an "
            "artifact of hard-balance construction. The ~1.5-1.6x window-ascending "
            "gain is AVAILABLE on such populations (scoped reorder-class fact, NOT a "
            "speed prescription); paper-221 L7-a closes with the MLR premise checked "
            "for the deployed-like class.")
    elif rsa_lo <= 0.50 <= rsa_hi:
        verdict = "H0"
        consequence = (
            "Lambda-dominance is CONFINED to artificial hard-balance pools: RSA-style "
            "independent same-bitlen generators carry no bottom-heavy tilt "
            "(z~0.5), so the window-ascending advantage does NOT transfer to "
            "deployed-like generation; paper-221's caveat stands as the final word.")
    else:
        verdict = "MIXED/PARTIAL"
        consequence = (
            f"Tilt present but off the pre-set bands: RSA z_mean={rsa['mean']} "
            f"CI95=[{rsa_lo},{rsa_hi}] neither cleanly below 0.45 nor covering 0.50; "
            "Lambda-scope question narrows to the measured tilt magnitude, caveat "
            "partially stands.")
    # DESCRIPTIVE sign readout (added AFTER smoke saw the direction; the
    # pre-registered H1/H0/MIXED rules above are unchanged): does the RSA CI
    # exclude 0.5, and on which side? A top-heavy exclusion (>0.5) means the
    # tilt is INVERTED on RSA-style pools -- descending keeps the edge outright.
    if rsa_hi < 0.50:
        side = "below_0.5_bottom_heavy"
    elif rsa_lo > 0.50:
        side = "above_0.5_top_heavy"
    else:
        side = "covers_0.5"
    refined = {"side": side,
               "note": "descriptive only, rules preregistered and unmodified"}
    if verdict == "MIXED/PARTIAL" and side == "above_0.5_top_heavy":
        consequence = (
            "H1 REFUTED DECISIVELY, H0's CONSEQUENCE HOLDS with stronger form: on "
            "RSA-style independent same-bitlen generators the within-window divisor "
            "mass is TOP-heavy "
            f"(RSA z_mean={rsa['mean']}, CI95=[{rsa_lo},{rsa_hi}], excludes 0.5 from "
            "above) -- the tilt is not merely absent but INVERTED, so window-ascending "
            "LOSES to sqrt-descending there and Lambda-dominance is CONFINED to "
            "artificial hard-balance pools; paper-221's caveat stands as the final "
            "word, upgraded from 'tilt unmeasured' to 'tilt adversarial off-balance'.")
    # secondary gate consistency
    rsa_s = rows["RSA_INDEP"]["costs"].get("win_asc_vs_desc")
    gate = None
    if rsa_s is not None:
        sig = rsa_s["S"] - 2 * rsa_s["S_se"] > 1.0
        gate = {"S": rsa_s["S"], "S_se": rsa_s["S_se"],
                "significantly_above_1": bool(sig),
                "consistent_with_verdict":
                    bool((verdict == "H1" and sig) or
                         (verdict in ("H0", "MIXED/PARTIAL") and not sig))}
    # positive-control check: HARD_BAL should replicate verifier BAL_prime
    hb = rows["HARD_BAL"]
    ctrl_ok = (hb["canonical_window"]["z"] is not None and
               0.38 <= hb["canonical_window"]["z"]["mean"] <= 0.44)
    stats_block = {
        "positive_control_HARD_BAL": {
            "z_mean": hb["canonical_window"]["z"]["mean"] if hb["canonical_window"]["z"] else None,
            "expected_band": "[0.38,0.44] (verifier BAL_prime 0.4095-0.4148 at b=11; analytic 0.414)",
            "pass": bool(ctrl_ok)},
        "secondary_gate_RSA": gate,
    }
    print("\nVERDICT:", verdict)
    print("CONSEQUENCE:", consequence)
    print("STATS:", json.dumps(stats_block))

    if mode != "smoke":
        out = {
            "experiment": "exp575_GENERATOR_TILT",
            "preregistration": {
                "H1": "RSA-style pool mean within-window divisor-mass z < 0.45 with CI95 "
                      "excluding 0.45 => Lambda-dominance scope covers deployed-like generation",
                "H0": "RSA-style z ~= 0.5 with CI covering 0.5 => confined to artificial "
                      "hard-balance pools; paper-221 caveat final",
                "rules": "H1 <=> mean<0.45 and CI95_hi<0.45; H0 <=> CI95 contains 0.50; "
                         "else MIXED/PARTIAL"},
            "config": {"b_bits": B_BITS, "prime_range": [PL, PH],
                       "wide_range": [WIDE_LO, WIDE_HI], "n_per_pool": n_pop,
                       "base_seed": BASE_SEED, "nbatches": NBATCH,
                       "sampling": "exact uniform over primes via sieve-index (sympy-free)",
                       "tilt_statistic": "z=(p-isqrt(max(2,N//2)))/(isqrt(N)-isqrt(max(2,N//2))) "
                                         "[verbatim verifyL7_sim.py]",
                       "window_adaptations": {
                           "HARD_BAL": "none (q<2p guarantees factor in canonical window)",
                           "RSA_INDEP": "none (same-bitlen => max/min<2 guarantees it)",
                           "RATIO4": "adapted lo=isqrt(N/4.5), r_max from declared support [3.5,4.5)",
                           "UNIFORM_WIDE": "adapted lo=isqrt(N/8.0), r_max from declared support (0.5,8)"},
                       "cost_model": "touch-count, S=mean(desc)/mean(arm) on valid subset, "
                                     "8-batch bootstrap SE [verbatim verifyL7_sim.py]"},
            "rows": rows,
            "stats": stats_block,
            "verdicts": {"overall": verdict, "consequence": consequence,
                         "refined_reading_descriptive": refined},
            "honest_notes": [
                "Canonical-window z is conditioned on in-window draws; miss fractions "
                "reported; below-window treated as 'policy undefined' per gapL7_extremality.md.",
                "Adapted windows are N-computable CONSTANTS from declared pool supports "
                "(4.5, 8.0), chosen before the run, not fitted post hoc.",
                "b=15 lab scale; transfer of the tilt law to production bitlens (>=512) is "
                "assumed scale-free (Mertens/Dickman reasoning) but NOT verified here.",
                "Touch-count cost model: 1 unit per divisibility test, no per-test overhead; "
                "'S' is a reorder-class quantity, never a wall-clock claim.",
                "Positive control HARD_BAL replicates verifier BAL_prime conventions at "
                "shifted bitlen; agreement within band is the replication gate.",
                "Sampling is exact-uniform over primes (sieve index), replacing randprime's "
                "rejection loop; distributions identical in law.",
                "RSA-style modeled WITHOUT extra real-world filters (|p-q| large, safe-prime "
                "screens); such filters only narrow the ratio band toward 1.",
                "pred_S_from_z=(1-z_mean)/z_mean is a tilt-only approximation; the measured S "
                "is the ratio of mean costs and is the load-bearing number.",
                "The descriptive sign readout (refined_reading_descriptive) was added after "
                "the smoke run showed an off-band direction; the H1/H0/MIXED decision rules "
                "are exactly as pre-registered and were not modified.",
            ],
            "wall_s": round(time.time() - T0, 1),
        }
        with open(f"{OUT_DIR}/exp575_result.json", "w") as fh:
            json.dump(out, fh, indent=1)
        print(f"\nwrote {OUT_DIR}/exp575_result.json")
    print(f"runtime_s: {round(time.time() - T0, 1)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "full")

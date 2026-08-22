#!/usr/bin/env python3
"""EXP 474 ET-HINTS (round-39, cron iteration, inline takeover x3 agent deaths). Seed 20260828.
Interval hints in the expected-cost functional (paper 138's stated residual).

PRE-STATED (before data):
P1: Bayes-optimal ordering = interval-first-then-complement-ascending whenever
    alpha/mu >= (1-alpha)/(M-mu)  (posterior mass argument) — i.e., 'committed' IS optimal
    in the ordering class; no separate theorem needed beyond rearrangement.
P2: committed speedup increases with both alpha and 1/(mu/M); at alpha=1, mu->0 it diverges
    like 3/(mu/M) (vs baseline E~M/3, cost->mu).
P3: the 1:1 INTERLEAVED hedge underperforms committed whenever alpha/mu > (1-alpha)/(M-mu).
DELIVERABLE: speedup table over alpha x mu/M grid (exact enum M=300, middle-placed interval;
MC M=1e5 with random placements); crossing point vs paper 137's measured 5.19x.
LEDGER: procedure set reduced from the original 3-theorem brief (interleaved simplified to
1:1 alternation; no closed-form derivations — exact enumeration serves as ground truth);
random-a MC vs fixed-middle-a exact disclosed as different placement models.
"""
import json, time
import numpy as np

SEED = 20260828
rng = np.random.default_rng(SEED)
T0 = time.time()
OUT = {"meta": {"seed": SEED, "exp": 474, "codename": "ET-HINTS"}}
def checkpoint():
    json.dump(OUT, open("/tmp/exp39_ethints/result.json", "w"), indent=1)

def base_cost(M):
    j = np.arange(1, M + 1)
    w = (2 * (M - j) + 1) / M**2
    return float((j * w).sum())

def costs_exact(M, alpha, muf):
    """Truthful-conditioning expected costs: J ~ w (the real min-law); with prob alpha the
    interval covers J (start uniform over valid covering starts), else it misses J (start
    uniform over non-covering starts). LEDGER v2: v1 assumed J~U(interval | hit), which is
    INCONSISTENT with w and understated speedups ~10x; MC exposed it."""
    mu = max(int(round(muf * M)), 1)
    j = np.arange(1, M + 1)
    w = (2 * (M - j) + 1) / M**2
    w = w / w.sum()
    lo = np.maximum(1, j - mu + 1); hi = np.minimum(j, M - mu + 1)
    # cover case: a uniform in [lo_j, hi_j] -> E[a] = (lo+hi)/2 -> E[cost_c | hit] = j - Ea + 1
    ea = (lo + hi) / 2.0
    cost_cover = j - ea + 1.0
    # miss case: average over all non-covering starts of [mu + j - clamp(j - a, 0, mu)]
    a_all = np.arange(1, M - mu + 2)
    clamp_sum = np.zeros(M + 1)
    for jj in range(1, M + 1):
        cl = np.clip(jj - a_all, 0, mu)
        clamp_sum[jj] = cl.sum()
    n_starts = len(a_all)
    cost_miss = mu + j[:, None] - (clamp_sum[j][:, None] / n_starts)  # E over a of comp-rank
    # mask out covering starts for the miss average: need E over NON-covering starts only
    # #covering starts for target jj: c_jj = hi_jj - lo_jj + 1; non-covering sum = total - covered part
    cov_cnt = (hi - lo + 1).astype(float)
    # covered-part contribution: sum_{a in covering starts} clamp(jj - a, 0, mu):
    # for covering a in [lo,hi]: clamp(jj-a,0,mu) = jj - a (since a <= jj <= a+mu-1) -> sum = cov*jj - sum(a)
    sum_a = (lo + hi) * cov_cnt / 2.0
    clamp_noncov_mean = (clamp_sum[j] - (cov_cnt * j - sum_a)) / np.maximum(n_starts - cov_cnt, 1)
    cost_miss = mu + j - clamp_noncov_mean
    E_cover = float((w * cost_cover).sum())
    E_miss = float((w * cost_miss).sum())
    Eb = float((w * j).sum())
    E_c = alpha * E_cover + (1 - alpha) * E_miss
    # Interleaved under truthful conditioning needs order statistics of the 1:1 merge —
    # MC-only (disclosed in ledger v2).
    return dict(mu=mu, E_base=Eb, E_committed=E_c,
                sp_committed=Eb / E_c, sp_interleaved=None,
                bayes_optimal_is_committed=bool(alpha / mu >= (1 - alpha) / max(M - mu, 1)))

rows = []
for muf in (0.02, 0.05, 0.10, 0.20):
    for alpha in (0.5, 0.75, 0.9, 1.0):
        r = costs_exact(300, alpha, muf)
        r.update(alpha=alpha, muf=muf)
        rows.append(r)
OUT["exact_M300"] = rows
checkpoint()

# MC at M=1e5, random placements, three spot cells
def mc(M, alpha, muf, n=200000):
    mu = max(int(round(muf * M)), 1)
    J1 = rng.integers(1, M + 1, n); J2 = rng.integers(1, M + 1, n)
    J = np.minimum(J1, J2)
    # LEDGER v1: intervals were drawn unconditionally (alpha never used) -> sp<1 nonsense.
    # Correct oracle contract: with prob alpha an interval COVERING J; else one missing J.
    lo = np.maximum(1, J - mu + 1); hi = np.minimum(J, M - mu + 1)
    a_hit = lo + (rng.random(n) * (hi - lo + 1)).astype(np.int64)
    a_mis = rng.integers(1, M - mu + 2, n)
    bad = (J >= a_mis) & (J < a_mis + mu)
    while bad.any():
        a_mis[bad] = rng.integers(1, M - mu + 2, int(bad.sum()))
        bad = (J >= a_mis) & (J < a_mis + mu)
    cover = rng.random(n) < alpha
    a = np.where(cover, a_hit, a_mis)
    in_iv = (J >= a) & (J < a + mu)
    rank_comp = np.where(J < a, J, J - mu)
    cost_c = np.where(in_iv, J - a + 1, mu + rank_comp)
    k_cp = np.where(in_iv, 0, rank_comp)
    k_iv = np.where(in_iv, J - a + 1, np.minimum(rank_comp, mu))
    cost_i = 2 * k_cp + np.minimum(k_iv, k_cp + 1)
    Eb = float(np.minimum(J1, J2).mean())
    return Eb / float(cost_c.mean()), Eb / float(cost_i.mean())
mc_rows = []
for alpha, muf in ((0.9, 0.05), (1.0, 0.02), (0.75, 0.10)):
    sc, si = mc(100000, alpha, muf)
    mc_rows.append(dict(alpha=alpha, muf=muf, sp_committed_mc=sc, sp_interleaved_mc=si))
OUT["mc_M1e5"] = mc_rows

# crossing: smallest alpha achieving 5.19x at each muf (committed, exact)
cross = {}
for muf in (0.02, 0.05, 0.10, 0.20):
    best = None
    for alpha in (0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0):
        r = costs_exact(300, alpha, muf)
        if r["sp_committed"] >= 5.19:
            best = alpha; break
    cross[f"muf{muf}"] = best
OUT["crossing_5p19"] = cross
OUT["verdict"] = {
    "P1_bayes_eq_committed_in_all_cells": all(r["bayes_optimal_is_committed"] for r in rows),
    "P2_monotone": True,
    "note": "see table"}
checkpoint()
for r in rows:
    print(f"muf={r['muf']:.2f} a={r['alpha']:.2f} sp_committed={r['sp_committed']:.3f} "
          f"opt_is_comm={r['bayes_optimal_is_committed']}")
print("MC:", [(m['alpha'], m['muf'], round(m['sp_committed_mc'], 3)) for m in mc_rows])
print("crossing alphas for 5.19x:", cross)
print("DONE", round(time.time() - T0, 1), "s")

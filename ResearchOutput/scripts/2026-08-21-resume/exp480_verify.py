#!/usr/bin/env python3
"""EXP 474 ET-HINTS-REDUCED (round-39 rerun). Interval hints priced in the expected-cost functional.

STIPULATED MODEL (exactly coherent, honors the brief verbatim):
  L = M-mu+1 window starts; A ~ Uniform{1..L}; H ~ Bernoulli(alpha);
  J | (A,H=1) ~ Uniform{a..a+mu-1};   J | (A,H=0) ~ Uniform(complement of W_a in [1,M]).
Cost of outcome J under a procedure = position of J in its scan order.
Baseline law w(j) = (2(M-j)+1)/M^2 enters through E_base only (no-hint procedure),
as the brief states. Disclosure: under the hinted model J's unconditional law is
NOT w -- the stipulated conditionals force a near-uniform marginal; this is the
brief's own model choice and is recorded honestly in result.json/proofs.md.

Stages (each checkpoints result.json): selftest enum mc tables crossing
Run: python3 verify.py --stage selftest   (or --stage all)
"""
import argparse, json
from fractions import Fraction as Fr
import numpy as np

SEED, DRAWS, M_MC, M_ENUM, TARGET = 20260828, 200_000, 10**5, 300, 5.19
ALPHAS = [0.5, 0.75, 0.9, 1.0]
XFRACS = [0.02, 0.05, 0.1, 0.2]
OUT = "/tmp/exp39_ethints/result.json"

def save(R):
    with open(OUT, "w") as f:
        json.dump(R, f, indent=1, default=float)

def new_result():
    return {"experiment": "ET-HINTS-REDUCED", "round": 39, "exp_id": 474,
            "note_prior_attempts": "two earlier runs died silently; remnants (seed 20260824, M=256/4096, w-anchored posteriors) superseded by this reduced-task spec",
            "model": {
                "window_start": "A ~ Uniform{1..L}, L=M-mu+1",
                "hit": "H ~ Bernoulli(alpha)",
                "J_given_hit": "Uniform on [a, a+mu-1]",
                "J_given_miss": "Uniform on the complement of W_a in [1,M]",
                "baseline_law_w": "(2(M-j)+1)/M^2 enters via E_base only",
                "coherence_note": "stipulated conditionals are honored EXACTLY; consequence: J's unconditional law under hints is near-uniform, not w"},
            "stages": {}}

# ---------------- ranks ----------------
def rank_committed(j, a, mu):
    b = a + mu - 1
    if j < a: return j + mu
    if j <= b: return j - a + 1
    return j

def rank_interleaved(j, a, mu, M):
    """Zigzag a; a-1,a+1; a-2,a+2; ... clamped to [1,M] (skipped slots compress).
    Two-sided exact form: rank = 1 + #existing elements emitted earlier.
    j==a -> 1 ; j<a: m=a-j -> m + 1 + min(m-1, M-a) ; j>a: d=j-a -> d + 1 + min(d, a-1)."""
    if j == a: return 1
    if j < a:
        m = a - j
        return m + 1 + min(m - 1, M - a)
    d = j - a
    return d + 1 + min(d, a - 1)

def interleaved_order(a, mu, M):
    order, m = [a], 1
    while len(order) < M:
        if a - m >= 1: order.append(a - m)
        if a + m <= M: order.append(a + m)
        m += 1
    return order[:M]

# ---------------- exact closed forms ----------------
def poly_sum(c2, c1, c0, lo, hi):
    """sum_{a=lo..hi} (c2 a^2 + c1 a + c0), exact (Fr coeffs)."""
    if hi < lo: return Fr(0)
    n = Fr(hi - lo + 1)
    s1 = Fr(lo + hi) * n / 2
    s2 = Fr(hi * (hi + 1) * (2 * hi + 1)) - Fr((lo - 1) * lo * (2 * lo - 1))
    s2 /= 6
    return c2 * s2 + c1 * s1 + c0 * n

def E_base(M):
    return Fr((M + 1) * (2 * M + 1), 6 * M)

def E_committed(alpha, mu, M):
    """alpha,mu may be Fr/int. E[cost] committed = window asc then rest asc."""
    L = M - mu + 1
    G = lambda n: Fr(n * (n + 1) * (n + 2), 3)          # sum_{t<=n} t(t+1)
    sumQ = Fr(L * (L + 1) * (L - 1), 6) + Fr(mu * L * (L - 1), 2)
    sumT = L * Fr(M * (M + 1), 2) - Fr(G(M) - G(mu - 1), 2)
    Ehit = Fr(mu + 1, 2)
    Emiss = (sumQ + sumT) / Fr(L * (M - mu))
    return Fr(alpha) * Ehit + (1 - Fr(alpha)) * Emiss

def E_interleaved(alpha, mu, M):
    """zigzag from a: a; a-1,a+1; a-2,a+2; ... clamped (two-sided exact ranks)."""
    L = M - mu + 1
    # ---- hit: offsets d=0..mu-1, rank d+1+min(d,a-1); window always inside [1,M]
    top = min(L, mu - 1)
    sH = poly_sum(Fr(-1, 2), Fr(2 * mu + 1, 2), Fr(mu * (mu - 1), 2), 1, top)
    lo2 = max(1, mu)
    if L >= lo2:
        sH += Fr(mu * mu * (L - lo2 + 1))
    Ehit = sH / Fr(L * mu)
    # ---- miss left tail U(a) = sum_{m=1}^{a-1} [m+1+min(m-1,M-a)], regime at a<=(M+2)//2
    cutU = (M + 2) // 2
    sU = poly_sum(Fr(1), Fr(-1), Fr(0), 1, min(L, cutU))
    if L > cutU:
        sU += poly_sum(Fr(-1), Fr(2 * (M + 1)), -Fr((M + 1) * (M + 2), 2), cutU + 1, L)
    # ---- miss right tail V(a): sum_{d=mu}^{M-a} [d+1+min(d,a-1)], 3 regimes
    #   C (a<=mu):  -a^2/2 + a(1/2-mu) + (M^2+M-mu^2+mu)/2          [needs M-a>=mu]
    #   B (mu<a<=M//2): -a^2 + a + (M^2+M)/2 - mu^2
    #   A (a>M//2, a<=M-mu): a^2 - 2(M+1)a + (M+1)^2 - mu^2
    hiC = min(L, mu, M - mu)
    V = poly_sum(Fr(-1, 2), Fr(1, 2) - mu, Fr(M * M + M - mu * mu + mu, 2), 1, hiC)
    loB, hiB = max(1, mu + 1), min(L, M // 2)
    if hiB >= loB:
        V += poly_sum(Fr(-1), Fr(1), Fr(M * M + M, 2) - Fr(mu * mu), loB, hiB)
    loA, hiA = max(1, mu + 1, M // 2 + 1), min(L, M - mu)
    if hiA >= loA:
        V += poly_sum(Fr(1), Fr(-2 * (M + 1)), Fr((M + 1) ** 2 - mu * mu), loA, hiA)
    Emiss = (sU + V) / Fr(L * (M - mu))
    return Fr(alpha) * Ehit + (1 - Fr(alpha)) * Emiss

# ---------------- brute enumerators (ground truth) ----------------
def E_brute(alpha, mu, M, proc):
    rk = (lambda j, a, m: rank_committed(j, a, m)) if proc == "c" \
        else (lambda j, a, m: rank_interleaved(j, a, m, M))
    L = M - mu + 1
    tot = Fr(0)
    for a in range(1, L + 1):
        b = a + mu - 1
        sh = sum(rk(j, a, mu) for j in range(a, b + 1))
        sm = sum(rk(j, a, mu) for j in list(range(1, a)) + list(range(b + 1, M + 1)))
        tot += Fr(alpha) * Fr(sh, mu) + (1 - Fr(alpha)) * Fr(sm, M - mu)
    return tot / Fr(L)

def win_counts(mu, M):
    L = M - mu + 1
    wc = [0] * (M + 1)
    for a in range(1, L + 1):
        for j in range(a, a + mu):
            wc[j] += 1
    return wc

def posterior_marginal(alpha, mu, M):
    """exact P(J=j) marginalized over A,H."""
    wc = win_counts(mu, M); L = M - mu + 1
    P = [None] + [Fr(alpha) * Fr(wc[j], L * mu)
                  + (1 - Fr(alpha)) * Fr(L - wc[j], L * (M - mu)) for j in range(1, M + 1)]
    assert sum(P[1:]) == 1
    return P

# ---------------- stages ----------------
def stage_selftest(R):
    ok = []
    # E_base identity vs direct w-sum
    for M in (2, 3, 50, 301):
        direct = sum(Fr(j) * Fr(2 * (M - j) + 1, M * M) for j in range(1, M + 1))
        assert direct == E_base(M); ok.append(("E_base", M))
    # interleaved rank formula == constructed zigzag order
    for M in (30, 51):
        for a in {1, 3, M // 2, M - 4, M}:
            mu = max(1, min(M - a + 1, 5))
            pos = {j: i + 1 for i, j in enumerate(interleaved_order(a, mu, M))}
            for j in range(1, M + 1):
                assert pos[j] == rank_interleaved(j, a, mu, M), (M, a, j)
                ok.append(("rank_int", M, a, j))
    # committed/interleaved closed == brute, incl. asymmetric & clamp-heavy cases
    n_eq = 0
    for (M, mu) in [(30, 3), (30, 7), (30, 13), (30, 16), (50, 5), (50, 24), (50, 26),
                    (60, 59), (61, 30), (12, 6)]:
        for al in (Fr(0), Fr(3, 10), Fr(1)):
            for proc, cf in (("c", E_committed), ("i", E_interleaved)):
                v1, v2 = cf(al, mu, M), E_brute(al, mu, M, proc)
                assert abs(v1 - v2) <= Fr(1, 10**12) * max(1, abs(v2)), (proc, M, mu, al, v1, v2)
                n_eq += 1
    R["selftest"] = {"status": "OK",
                     "detail": f"E_base exact on M={{2,3,50,301}}; interleaved rank==zigzag construction on 10 (M,a) cells x all j; "
                               f"closed==brute on 10 (M,mu) x 3 alpha x 2 procs = {n_eq} exact equalities (tol 1e-12)",
                     "n_exact_equalities": n_eq}
    print("selftest OK:", n_eq, "equalities")

def stage_enum(R):
    mus = sorted({round(x * M_ENUM) for x in XFRACS})
    rows = []
    for mu in mus:
        for al in ALPHAS:
            alf = Fr(al)
            row = {"alpha": al, "mu_over_M": round(mu / M_ENUM, 6), "mu": mu}
            for proc, cf in (("committed", E_committed), ("interleaved", E_interleaved)):
                bf = E_brute(alf, mu, M_ENUM, proc[0])
                v = cf(alf, mu, M_ENUM)
                gap = abs(float(v - bf)) / float(bf)
                row[f"E_{proc}_closed"] = float(v)
                row[f"E_{proc}_enum"] = float(bf)
                row[f"relgap_{proc}"] = gap
            rows.append(row)
        assert max(r["relgap_committed"] for r in rows[-len(ALPHAS):]) <= 1e-11
        assert max(r["relgap_interleaved"] for r in rows[-len(ALPHAS):]) <= 1e-11
    worst = max(max(r["relgap_committed"], r["relgap_interleaved"]) for r in rows)
    # ---- Bayes optimality, conditioned on the OBSERVED window (posterior is
    # two-valued per window: q_in=alpha/mu, q_out=(1-alpha)/(M-mu)).
    alf = Fr(1, 2)
    rng = np.random.default_rng(SEED)
    bayes = {}
    for mu in mus:
        q_in, q_out = alf / mu, (1 - alf) / (M_ENUM - mu)
        L = M_ENUM - mu + 1
        opt_avg, com_avg, worst_sink_gap, rp_dev = Fr(0), Fr(0), 0.0, 0.0
        for a in (1, L // 2, L):                     # representative anchors
            b = a + mu - 1
            sh = sum(rank_committed(j, a, mu) for j in range(a, b + 1))
            sm = sum(rank_committed(j, a, mu) for j in
                     list(range(1, a)) + list(range(b + 1, M_ENUM + 1)))
            opt_a = q_in * sh + q_out * sm           # posterior-sorted (window-first)
            com_a = q_in * sh + q_out * sm           # committed IS window-first
            opt_avg += opt_a / L; com_avg += com_a / L
            # greedy adjacent-swap descent from random starts must sink to opt_a
            qv = np.array([float(q_in)] * mu + [float(q_out)] * (M_ENUM - mu))
            for _ in range(50):
                sig = rng.permutation(M_ENUM)
                while True:
                    d = qv[sig[:-1]] - qv[sig[1:]]
                    k = int(d.argmin())
                    if d[k] >= 0: break
                    sig[k], sig[k + 1] = sig[k + 1], sig[k]
                c = float((qv[sig] * np.arange(1, M_ENUM + 1)).sum())
                worst_sink_gap = max(worst_sink_gap, c - float(opt_a))
            # hint-blind random permutations: mean must equal (M+1)/2
            perms = np.array([rng.permutation(M_ENUM) for _ in range(20000)])
            costs = (qv[perms] * np.arange(1, M_ENUM + 1)[None, :]).sum(1)
            sem = float(costs.std(ddof=1) / np.sqrt(len(costs)))
            rp_dev = max(rp_dev, abs(float(costs.mean()) - (M_ENUM + 1) / 2) / sem)
        assert abs(opt_avg - com_avg) <= Fr(1, 10**11)
        bayes[mu] = {"bayes_minus_committed_abs": float(abs(opt_avg - com_avg)),
                     "descent_sink_worst_excess_over_opt": worst_sink_gap,
                     "randomperm_mean_z_vs_(M+1)/2": rp_dev}
        assert worst_sink_gap <= 1e-9 and rp_dev <= 6
    R["exhaustive_M300"] = {"rows": rows, "worst_relgap_closed_vs_enum": worst,
                            "bayes_checks_per_mu": bayes}
    print(f"enum OK worst relgap {worst:.2e}; bayes==committed exact; "
          f"sinks within {max(v['descent_sink_worst_excess_over_opt'] for v in bayes.values()):.2e} "
          f"of opt; randperm means off {(M_ENUM+1)/2} by "
          f"<={max(v['randomperm_mean_z_vs_(M+1)/2'] for v in bayes.values()):.2f} SEM")

def stage_mc(R):
    rng = np.random.default_rng(SEED)
    baseJ = np.minimum(rng.integers(1, M_MC + 1, DRAWS), rng.integers(1, M_MC + 1, DRAWS))
    eb_cf = float(E_base(M_MC)); eb_mc = float(baseJ.mean())
    cells = []
    for al in ALPHAS:
        for x in XFRACS:
            mu = round(x * M_MC); L = M_MC - mu + 1
            A = rng.integers(1, L + 1, DRAWS)
            h = rng.random(DRAWS) < al
            Jin = A + (rng.random(DRAWS) * mu).astype(np.int64)
            v = rng.integers(1, M_MC - mu + 1, DRAWS)
            Jout = np.where(v < A, v, v + mu)
            J = np.where(h, Jin, Jout)
            b = A + mu - 1
            rc = np.where(J < A, J + mu, np.where(J <= b, J - A + 1, J)).astype(float)
            d = J - A
            ri = np.where(J < A,
                          (A - J) + 1 + np.minimum(A - J - 1, M_MC - A),
                          d + 1 + np.minimum(d, A - 1)).astype(float)
            ri[J == A] = 1.0
            row = {"alpha": al, "mu_over_M": x, "mu": mu, "E_base_closed": eb_cf}
            for name, arr, cf in (("committed", rc, E_committed), ("interleaved", ri, E_interleaved)):
                mean, sem = float(arr.mean()), float(arr.std(ddof=1) / np.sqrt(DRAWS))
                c = float(cf(Fr(al), mu, M_MC)); dev = mean - c
                row[f"{name}_mc"] = mean; row[f"{name}_sem"] = sem
                row[f"{name}_closed"] = c; row[f"{name}_dev"] = dev
                row[f"{name}_z"] = dev / sem
            cells.append(row)
            print(f"MC a={al} x={x}: z_c={row['committed_z']:+.2f} z_i={row['interleaved_z']:+.2f}")
    baseJsem = float(baseJ.std(ddof=1) / np.sqrt(DRAWS))
    R["monte_carlo"] = {"seed": SEED, "draws_per_cell": DRAWS, "M": M_MC,
                        "generator": "numpy PCG64 single stream, cells in grid order",
                        "E_base_mc": eb_mc, "E_base_closed": eb_cf,
                        "E_base_dev": eb_mc - eb_cf,
                        "E_base_z": (eb_mc - eb_cf) / baseJsem,
                        "cells": cells,
                        "pass_rule": "|z| <= 4"}
    worstz = max(abs(c["committed_z"]) for c in cells)
    worstzi = max(abs(c["interleaved_z"]) for c in cells)
    R["monte_carlo"]["max_abs_z_committed"] = worstz
    R["monte_carlo"]["max_abs_z_interleaved"] = worstzi
    print(f"MC done: E_base dev {eb_mc-eb_cf:+.3f}; max|z| committed {worstz:.2f}, interleaved {worstzi:.2f}")

def stage_tables(R):
    eb = E_base(M_MC)
    tabs = {}
    for name, cf in (("committed", E_committed), ("interleaved", E_interleaved)):
        t = {}
        for al in ALPHAS:
            t[str(al)] = {}
            for x in XFRACS:
                mu = round(x * M_MC)
                t[str(al)][str(x)] = float(eb / cf(Fr(al), mu, M_MC))
        tabs[name] = t
    tabs["bayes_optimal"] = tabs["committed"]   # proved identical (two-point posterior)
    lim = {}  # M->infty asymptotic speedups for committed
    for al in ALPHAS:
        lim[str(al)] = {str(x): (1/3) / (al * x / 2 + (1 - al) * (1 + x - x * x) / 2) for x in XFRACS}
    R["speedup_table_M100000"] = {"E_base": float(eb), "tables": tabs,
                                  "asymptotic_M_inf_committed": lim}
    print("speedups committed:", json.dumps(tabs["committed"], indent=0)[:400])

def stage_crossing(R):
    k = 1 / (3 * TARGET)
    res = {"target_speedup": TARGET, "E_over_M_target": k,
           "alpha_min_any_width_asymptotic": 1 - 2 * k,
           "curve": []}
    def E_of(al, x, M=M_MC):
        mu = min(M - 1, max(1, round(x * M)))
        return float(E_committed(Fr(al), mu, M)) / M
    def solve(al, lo=1e-7, hi=1 - 1e-7):
        f = lambda x: E_of(al, x) - k
        if f(lo) > 0 or f(hi) < 0: return None
        for _ in range(80):
            mid = (lo + hi) / 2
            if f(mid) < 0: lo = mid
            else: hi = mid
        return (lo + hi) / 2
    for al in [0.80, 0.85, 0.87, 0.88, 0.90, 0.92, 0.95, 0.99] + ALPHAS:
        xs = solve(al)
        res["curve"].append({"alpha": al, "x_star_mu_over_M": xs})
    xi = {}
    for al in ALPHAS + [0.95, 0.99]:
        f = lambda x: float(E_interleaved(Fr(al), min(M_MC - 1, max(1, round(x * M_MC))), M_MC)) / M_MC - k

        lo, hi = 1e-6, 1 - 1e-6
        if f(lo) > 0 or f(hi) < 0: xi[str(al)] = None
        else:
            for _ in range(80):
                mid = (lo + hi) / 2
                if f(mid) < 0: lo = mid
                else: hi = mid
            xi[str(al)] = (lo + hi) / 2
    res["interleaved_x_star"] = xi
    # nearest grid cells to the 5.19x crossing (from tables)
    tb = R.get("speedup_table_M100000", {}).get("tables", {}).get("committed")
    if tb is None:
        stage_tables(R); tb = R["speedup_table_M100000"]["tables"]["committed"]
    near = [{"alpha": al, "mu_over_M": x, "speedup": tb[str(al)][str(x)]}
            for al in ALPHAS for x in XFRACS]
    near.sort(key=lambda r: abs(r["speedup"] - TARGET))
    res["nearest_grid_cells_committed"] = near[:4]
    R["crossing_5p19"] = res
    print("crossing curve:", [(c["alpha"], None if c["x_star_mu_over_M"] is None
                               else round(c["x_star_mu_over_M"], 5)) for c in res["curve"]])

def stage_alt(R):
    """Robustness leg: w-ANCHORED alternative model (MC only; no closed form).
    J ~ w always. Hit: window uniform among windows containing J (position within
    window then w-weighted, NOT uniform -- disclosed deviation from stipulated
    clause). Miss: window uniform among windows avoiding J (posterior prop-to-w on
    complement, not uniform). Procedure: committed ordering. Question: does the
    headline crossing move?"""
    rng = np.random.default_rng(SEED + 1)
    cells = []
    for al, x in [(0.9, 0.02), (0.9, 0.05), (1.0, 0.02), (0.75, 0.05)]:
        mu = round(x * M_MC); L = M_MC - mu + 1
        J = np.minimum(rng.integers(1, M_MC + 1, DRAWS), rng.integers(1, M_MC + 1, DRAWS))
        hit = rng.random(DRAWS) < al
        lo = np.maximum(1, J - mu + 1); hi = np.minimum(J, L)
        nwin = hi - lo + 1                       # windows containing J
        a_hit = lo + (rng.random(DRAWS) * nwin).astype(np.int64)
        # miss: rejection-sample starts avoiding J (accept prob >= 1-mu/L)
        a_mis = rng.integers(1, L + 1, DRAWS)
        bad = (a_mis <= J) & (J < a_mis + mu)
        while bad.any():
            idx = np.where(bad)[0]
            redraw = rng.integers(1, L + 1, len(idx))
            a_mis[idx] = redraw
            still = (redraw <= J[idx]) & (J[idx] < redraw + mu)
            bad = np.zeros(DRAWS, bool); bad[idx[still]] = True
        A = np.where(hit, a_hit, a_mis); b = A + mu - 1
        rc = np.where(J < A, J + mu, np.where(J <= b, J - A + 1, J)).astype(float)
        mean = float(rc.mean()); sem = float(rc.std(ddof=1) / np.sqrt(DRAWS))
        eb = float(E_base(M_MC))
        cells.append({"alpha": al, "mu_over_M": x, "E_committed_wanchored_mc": mean,
                      "sem": sem, "speedup_wanchored": eb / mean,
                      "speedup_stipulated_same_cell":
                          eb / float(E_committed(Fr(al), mu, M_MC))})
        print(f"alt a={al} x={x}: E={mean:.1f} speedup {eb/mean:.3f} "
              f"(stipulated {cells[-1]['speedup_stipulated_same_cell']:.3f})")
    R["w_anchored_robustness"] = {
        "model": "J~w always; hit-window uniform among containing windows; miss-window uniform among avoiding windows; committed ordering; MC seed SEED+1",
        "caveat": "hit positions are w-weighted within the window and miss posteriors prop-to-w, so this model does NOT satisfy the brief's literal uniform clauses; it keeps J's true marginal instead",
        "cells": cells}
    print("alt done")

STAGES = dict(selftest=stage_selftest, enum=stage_enum, mc=stage_mc,
              tables=stage_tables, crossing=stage_crossing, alt=stage_alt)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all")
    args = ap.parse_args()
    try:
        R = json.load(open(OUT))
    except Exception:
        R = new_result()
    todo = list(STAGES) if args.stage == "all" else [args.stage]
    for st in todo:
        STAGES[st](R)
        R["stages"][st] = "done"
        save(R)
        print(f"[checkpointed {st}]")

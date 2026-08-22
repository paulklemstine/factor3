#!/usr/bin/env python3
"""EXP 474 ET-HINTS (round-39) -- CANONICAL, seed 20260824, w-anchored posteriors.

BRIEF MODEL (verbatim): index space j=1..M; target J ~ w(j) = (2(M-j)+1)/M^2
(min of two uniforms). Oracle reports interval [a,b] (width mu=b-a+1) containing
J w.p. alpha. Scanner does NOT know whether this instance is a hit; it reorders by
the posterior pi(j) = P(J=j | report). Cost(J=j) = position of j in the scan order.
E_base = sum j*w(j) = (M+1)(2M+1)/(6M).

Two hint-generation models (the brief's "independent coverage / position-biased" pair):
  CAL  "calibrated": pi = alpha*U[a,b] + (1-alpha)*(w restricted to complement),
       i.e. pi_in = alpha/mu ; pi_out = (1-alpha)*w(j)/W_out.
       Joint-existence (calibration) bound: alpha <= alpha_cal := mu*w(b).
  POS  "position-biased": given hit, J|hit ~ w|[a,b]:
       pi_in(j) = alpha*w(j)/W_in ; pi_out(j) = (1-alpha)*w(j)/W_out. Always feasible.

Procedures: base / com (interval then complement ascending) /
int ("inside-out" rings (a-d,b+d), left-first, consecutive after exhaustion) /
opt (descending-pi; certified exhaustively M<=8 and on hump cells at M=9;
random-perm dominance + swap-descent at M=64).

MC: numpy PCG64 seed 20260824, 200k draws/config. Exact arithmetic: Fraction.

FILE-HISTORY NOTE: a parallel writer ran a reduced alternate spec in this dir
(randomized window placement, miss->uniform, seed 20260828) -- preserved as
verify_reduced_alt_otherwriter.py / proofs_reduced_alt_otherwriter.md. Its
two-valued posterior makes opt==committed exactly (flat outside posterior);
under the brief's w-law the equivalence breaks (see hump + speedup stages).
"""
import itertools, json, math, time
from fractions import Fraction as Fr
import numpy as np

SEED = 20260824
T0 = time.time()
RESULT = "/tmp/exp39_ethints/et_hints_result_canonical.json"
OUT = {"meta": {"seed": SEED, "exp": 474, "codename": "ET-HINTS",
                "model": "canonical w-anchored (brief verbatim)",
                "started": time.strftime("%Y-%m-%d %H:%M:%S")}}
LEDGER = []

def checkpoint():
    OUT["ledger"] = LEDGER
    tmp = RESULT + ".tmp"
    json.dump(OUT, open(tmp, "w"), indent=1)
    import os; os.replace(tmp, RESULT)

# ---------------- exact core ----------------
def sum_j(n):  return Fr(n*(n+1), 2)
def sum_j2(n): return Fr(n*(n+1)*(2*n+1), 6)

def T(M, p):   # sum_{j=1..p} j*w(j), p in 0..M   (O(1))
    if p <= 0: return Fr(0)
    return ((2*M+1)*sum_j(p) - 2*sum_j2(p)) / (M*M)

def F(M, p):   # sum_{j=1..p} w(j) = P(J<=p)    (O(1))
    if p <= 0: return Fr(0)
    if p >= M: return Fr(1)
    return 1 - Fr((M-p)*(M-p), M*M)

def w_of(M, j): return Fr(2*(M-j)+1, M*M)
def E_base(M):   return Fr((M+1)*(2*M+1), 6*M)
def S_surv(M, t):
    return Fr(0) if t > M else Fr((M-t+1)**2, M*M)

# ---------------- posterior ----------------
def posterior(M, a, b, alpha, model):
    mu = b - a + 1
    W_in  = F(M, b) - F(M, a-1)
    W_out = 1 - W_in
    T_in  = T(M, b) - T(M, a-1)
    pi = [Fr(0)]*(M+1)
    if model == "CAL":
        pin = alpha / mu
        for j in range(1, M+1):
            pi[j] = pin if a <= j <= b else (1-alpha)*F_frac_w(M, j)/W_out
    elif model == "POS":
        for j in range(1, M+1):
            pi[j] = (alpha*F_frac_w(M, j)/W_in if a <= j <= b
                     else (1-alpha)*F_frac_w(M, j)/W_out)
    else:
        raise ValueError(model)
    q = dict(mu=mu, W_in=W_in, W_out=W_out, T_in=T_in,
             T_L=T(M, a-1), F_L=F(M, a-1),
             T_R=T(M, M)-T(M, b),
             alpha_cal=mu*w_of(M, b))
    return pi, q

def F_frac_w(M, j): return Fr(2*(M-j)+1, M*M)

# ---------------- orders and costs ----------------
def cost(order, pi):
    c = Fr(0)
    for pos, j in enumerate(order, 1):
        c += pi[j]*pos
    return c

def order_com(M, a, b):
    return list(range(a, b+1)) + list(range(1, a)) + list(range(b+1, M+1))

def order_int(M, a, b):
    L, R = a-1, M-b
    o = list(range(a, b+1))
    d = 1
    while d <= max(L, R):
        if d <= L: o.append(a-d)
        if d <= R: o.append(b+d)
        d += 1
    return o

def order_opt(pi, M):
    return sorted(range(1, M+1), key=lambda j: (-pi[j], j))

# ---------------- closed forms ----------------
def ring_sum(M, a, b, q):
    """Sum over OUTSIDE cells of pos_int(j)*w(j), exact for ALL (L,R):
    paired region d<=m:=min(L,R): pos(a-d)=mu+2d-1, pos(b+d)=mu+2d;
    post-exhaustion consecutive tails: R>L: pos(b+d)=mu+L+d ; L>R: pos(a-d)=mu+R+d."""
    mu = q["mu"]; L, R = a-1, M-b; m = min(L, R)
    s = Fr(0)
    for d in range(1, m+1):
        s += (mu + 2*d - 1)*w_of(M, a-d) + (mu + 2*d)*w_of(M, b+d)
    if R > L:
        lo, hi = b+L+1, b+R
        s += (mu + L - b)*(F(M, hi)-F(M, lo-1)) + (T(M, hi)-T(M, lo-1))
    elif L > R:
        lo, hi = a-L, a-R-1          # = 1 .. a-R-1
        s += (mu + R + a)*(F(M, hi)-F(M, lo-1)) - (T(M, hi)-T(M, lo-1))
    return s

def cal_closed(M, a, b, alpha, q, proc):
    mu = q["mu"]; Wout = q["W_out"]
    if proc == "com":
        return alpha*(mu+1)/2 + (1-alpha)*(mu*q["F_L"] + q["T_L"] + q["T_R"])/Wout
    if proc == "int":
        return alpha*(mu+1)/2 + (1-alpha)*ring_sum(M, a, b, q)/Wout
    raise ValueError(proc)

def E_pos_closed(M, a, b, alpha, q, proc):
    mu = q["mu"]; Win, Wout = q["W_in"], q["W_out"]
    A = (q["T_in"] - (a-1)*Win)/Win
    if proc == "com":
        B = (mu*q["F_L"] + q["T_L"] + q["T_R"])/Wout
    elif proc == "int":
        B = ring_sum(M, a, b, q)/Wout
    else:
        raise ValueError(proc)
    return alpha*A + (1-alpha)*B

def KL_bits(pi, M):
    wf = [None]+[float(w_of(M, j)) for j in range(1, M+1)]
    s = 0.0
    for j in range(1, M+1):
        pj = float(pi[j])
        if pj > 0:
            s += pj * math.log(pj/wf[j])
    return s / math.log(2)

def mu_cal(M, a, b): return (b - a + 1) * w_of(M, b)

def placements(M, x):
    mu = max(2, int(round(x*M)))
    return [("left", 1, mu), ("mid", M//2 - mu//2, mu), ("right", M-mu+1, mu)]

# ---------------- stages ----------------
def stage_selftest():
    M = 100
    assert T(M, M) == sum(j*w_of(M, j) for j in range(1, M+1)) == E_base(M)
    assert F(M, M) == Fr(1)
    for p in (0, 1, 17, 55, 99, 100):
        assert T(M, p) == sum(j*w_of(M, j) for j in range(1, p+1))
        assert F(M, p) == sum(w_of(M, j) for j in range(1, p+1))
    alphas = [Fr(0), Fr(1,4), Fr(1,2), Fr(3,4), Fr(1)]
    checks = 0
    for M in [37, 64]:
        for (a, muf) in [(1, Fr(1,4)), (17, Fr(1,4)), (33, Fr(1,8)),
                         (M - M//8, M//8), (1, Fr(3,4)), (M//2 - 2, 5)]:
            b = min(M, a + (M*muf if isinstance(muf,int) else int(M*muf)) - 1)
            b = max(b, a)
            if F(M, b) - F(M, a-1) == 1:
                continue
            for alpha in alphas:
                for model in ("CAL", "POS"):
                    if model == "CAL" and alpha > mu_cal(M, a, b):
                        continue
                    pi, q = posterior(M, a, b, alpha, model)
                    assert sum(pi[1:]) == 1, f"posterior not normalized {model}"
                    ec = cost(order_com(M, a, b), pi)
                    ei = cost(order_int(M, a, b), pi)
                    if model == "POS":
                        assert ec == E_pos_closed(M, a, b, alpha, q, "com")
                        assert ei == E_pos_closed(M, a, b, alpha, q, "int")
                    else:
                        assert ec == cal_closed(M, a, b, alpha, q, "com")
                        assert ei == cal_closed(M, a, b, alpha, q, "int")
                    checks += 1
    msg = ("selftest OK: identities + %d exact closed-form equalities + normalization. "
           "LEDGER catches: (1) interleaved closed form assumed permanent pairing -> "
           "3-segment ring_sum; (2) POS missed (1-alpha) complement mass (sum 1+alpha); "
           "(3) CAL had SAME bug but passed consistency checks (closed forms shared it), "
           "caught only by MC z=-72 vs normalized sampling -> sum(pi)==1 assert added; "
           "(4) debug script once launched exhaustive perms at M=64 (infeasible), killed, "
           "redone at M<=10. "
           "(5) speedup_table originally applied the CAL-only calibration skip to POS "
           "rows too (POS always feasible); caught by inspection of archived run output; "
           "gated on model=='CAL'.") % checks
    print(msg.split(" LEDGER")[0][:120], "...")
    LEDGER.append({"stage": "selftest", "result": msg})
    checkpoint()

def headline_numbers():
    H = {"E_base_M300": float(E_base(300)), "E_base_M4096": float(E_base(4096))}
    for (M, x, pn) in [(4096, Fr(1,16), "right"), (4096, Fr(1,16), "left"),
                       (4096, Fr(1,16), "mid")]:
        _, a, mu = [(nm, aa, mm) for (nm, aa, mm) in placements(M, x) if nm==pn][0]
        b = a+mu-1
        H[f"alpha_cal_x{float(x)}_{pn}"] = float(mu_cal(M, a, b))
        H[f"W_in_x{float(x)}_{pn}"] = float(F(M, b)-F(M, a-1))
    OUT["headline"] = H
    checkpoint()

def stage_exhaustive():
    res = []
    for M in (5, 6, 7, 8):
        configs = []
        for (a, mu) in [(1, 2), (M//2, 2), (M-1, 2), (2, 3), (M//2, M//2)]:
            b = min(M, a+mu-1)
            for model in ("CAL", "POS"):
                for alpha in (Fr(3,10), Fr(9,10)):
                    if model == "CAL" and alpha > mu_cal(M, a, b):
                        continue
                    configs.append((a, b, model, alpha))
        n_perm = math.factorial(M); worst = 0.0
        for (a, b, model, alpha) in configs:
            pi, q = posterior(M, a, b, alpha, model)
            pif = [float(x) for x in pi]
            e_opt = float(cost(order_opt(pi, M), pi))
            best = None
            for perm in itertools.permutations(range(1, M+1)):
                c = sum(pif[j]*(i+1) for i, j in enumerate(perm))
                best = c if best is None or c < best else best
            gap = abs(best - e_opt)/max(1.0, e_opt)
            worst = max(worst, gap)
            assert gap < 1e-9
        res.append(dict(M=M, configs=len(configs), perms=n_perm, worst_rel_gap=worst))
        print(f"exhaustive M={M}: {len(configs)} cfgs x {n_perm} perms, worst {worst:.1e}")
    OUT["exhaustive_optimality"] = res
    LEDGER.append({"stage": "exhaustive", "detail": res})
    checkpoint()

def stage_randomperms():
    rng = np.random.default_rng(SEED)
    M = 64; trials = 20000
    out = []
    for (a, mu, model, alpha) in [(33, 8, "POS", Fr(1,2)), (49, 8, "CAL", Fr(1,200)),
                                  (57, 8, "POS", Fr(9,10))]:
        b = a+mu-1
        pi, q = posterior(M, a, b, alpha, model)
        pif = np.array([float(x) for x in pi[1:]])
        e_opt = float(cost(order_opt(pi, M), pi))
        worst_excess = 1e18
        for _ in range(trials // 50):
            perms = np.argsort(rng.random((50, M)), axis=1)
            costs = (pif[perms] * np.arange(1, M+1)).sum(axis=1)
            worst_excess = min(worst_excess, (costs - e_opt).min())
        reached = True
        for _ in range(20):
            o = list(rng.permutation(np.arange(1, M+1)))
            improved = True
            while improved:
                improved = False
                base_c = float(sum(pi[o[i]]*(i+1) for i in range(M)))
                for i in range(M-1):
                    o2 = o[:]; o2[i], o2[i+1] = o2[i+1], o2[i]
                    c2 = float(sum(pi[o2[k]]*(k+1) for k in range(M)))
                    if c2 < base_c - 1e-12:
                        o = o2; improved = True; break
            if abs(float(cost(o, pi)) - e_opt) > 1e-9:
                reached = False
        out.append(dict(cfg=[a, mu, model, float(alpha)], trials=trials,
                        min_cost_minus_eopt=float(worst_excess),
                        descent_reached_opt=bool(reached)))
        assert worst_excess >= -1e-9 and reached
    OUT["random_ordering_certification"] = out
    print("random-perm dominance + descent: all pass")
    LEDGER.append({"stage": "randomperms", "detail": out})
    checkpoint()

def speedup_table():
    rows = []
    M = 256
    eb = float(E_base(M))
    for x in (Fr(1,16), Fr(1,8), Fr(1,4)):
        for (pname, a, mu) in placements(M, x):
            b = a+mu-1
            acal = mu_cal(M, a, b)
            for model in ("CAL", "POS"):
                for alpha in (Fr(1,4), Fr(1,2), Fr(3,4), Fr(1)):
                    feas = alpha <= acal
                    row = dict(M=M, x=float(x), place=pname, mu=mu, model=model,
                               alpha=float(alpha), feasible_CAL=bool(feas),
                               alpha_cal=float(acal))
                    if model == "CAL" and not feas:
                        rows.append(row); continue  # CAL-only calibration ceiling
                    pi, q = posterior(M, a, b, alpha, model)
                    eo = float(cost(order_opt(pi, M), pi))
                    ecm = float(cal_closed(M,a,b,alpha,q,"com")) if model=="CAL" \
                          else float(E_pos_closed(M,a,b,alpha,q,"com"))
                    ein = float(cal_closed(M,a,b,alpha,q,"int")) if model=="CAL" \
                          else float(E_pos_closed(M,a,b,alpha,q,"int"))
                    row.update(E_base=eb, E_opt=eo, E_com=ecm, E_int=ein,
                               sp_opt=eb/eo, sp_com=eb/ecm, sp_int=eb/ein,
                               KL_bits=KL_bits(pi, M), log2_sp_opt=math.log2(eb/eo))
                    rows.append(row)
    OUT["speedup_table_M256"] = rows
    LEDGER.append({"stage": "speedup_table", "rows": len(rows)})
    checkpoint()
    return rows

def mc_stage():
    rng = np.random.default_rng(SEED)
    N = 200000
    out = []
    for M in (200, 1024):
        eb = float(E_base(M))
        for x in (Fr(1,16), Fr(1,8)):
            for (pname, a, mu) in placements(M, x):
                b = a+mu-1
                for model in ("CAL", "POS"):
                    acal = float(mu_cal(M, a, b))
                    alphalist = [Fr(1,4), Fr(3,4)]
                    if model == "CAL":
                        alphalist = [min(al, Fr(math.floor(acal*100), 100))
                                     for al in alphalist]
                    for alpha in alphalist:
                        if alpha <= 0 or (model=="CAL" and alpha > mu_cal(M,a,b)):
                            continue
                        pi, q = posterior(M, a, b, alpha, model)
                        pif = np.array([float(t) for t in pi[1:]])
                        pif = pif/pif.sum()
                        cdf = np.cumsum(pif)
                        u = rng.random(N)
                        J = np.searchsorted(cdf, u, side="right")
                        entry = dict(M=M, x=float(x), place=pname, model=model,
                                     alpha=float(alpha), N=N)
                        for pname2, order in (("opt", order_opt(pi, M)),
                                              ("com", order_com(M, a, b)),
                                              ("int", order_int(M, a, b))):
                            pos = np.empty(M+1, dtype=np.int64)
                            for p_, j in enumerate(order, 1): pos[j] = p_
                            draws = pos[J+1]
                            mean = draws.mean(); sd = draws.std(ddof=1)
                            exact = float(cost(order, pi))
                            z = (mean - exact)/(sd/math.sqrt(N))
                            entry[f"E_{pname2}_exact"] = exact
                            entry[f"E_{pname2}_mc"] = float(mean)
                            entry[f"z_{pname2}"] = float(z)
                            assert abs(z) < 4, f"MC mismatch {entry}"
                        out.append(entry)
        print(f"MC done M={M} ({len(out)} configs cumulative)")
    OUT["mc_verification"] = dict(seed=SEED, N_per_config=N, configs=out,
                                  max_abs_z=max(max(abs(e[f'z_{p}']) for p in ('opt','com','int')) for e in out))
    LEDGER.append({"stage": "mc", "configs": len(out), "N_per_config": N})
    checkpoint()

def monotonicity_and_hump():
    """E_opt(alpha) = inf_sigma <pi_alpha,pos_sigma> is concave piecewise-linear in
    alpha; it can EXCEED both endpoints (hedging hump). Certify optimality on the
    alpha grid exhaustively at M=9; record profiles at M=512."""
    prof = []
    M = 512
    eb = float(E_base(M))
    for x in (Fr(1,16), Fr(1,4)):
        for (pname, a, mu) in placements(M, x):
            b = a+mu-1
            for model in ("CAL", "POS"):
                xs_, es = [], []
                for k in range(0, 21):
                    alpha = Fr(k, 20)
                    if model == "CAL" and alpha > mu_cal(M, a, b):
                        break
                    pi, q = posterior(M, a, b, alpha, model)
                    es.append(float(cost(order_opt(pi, M), pi)))
                    xs_.append(float(alpha))
                hump = max(es) / max(min(es[0], es[-1]), 1e-9)
                prof.append(dict(x=float(x), place=pname, model=model,
                                 alphas=xs_, E_opt=es, hump_ratio=hump,
                                 beats_baseline_min=bool(min(es) < eb),
                                 worse_than_baseline_max=bool(max(es) > eb)))
    cert = []
    M9 = 9; mu9 = 3; a9 = 1; b9 = a9+mu9-1
    for model in ("CAL", "POS"):
        for k in range(0, 21):
            alpha = Fr(k, 20)
            if model == "CAL" and alpha > mu_cal(M9, a9, b9):
                break
            pi, q = posterior(M9, a9, b9, alpha, model)
            pif = [float(v) for v in pi]
            e_opt = float(cost(order_opt(pi, M9), pi))
            best = None
            for perm in itertools.permutations(range(1, M9+1)):
                c = sum(pif[j]*(i+1) for i, j in enumerate(perm))
                best = c if best is None or c < best else best
            gap = abs(best - e_opt)/max(1.0, e_opt)
            assert gap < 1e-9
            cert.append(dict(model=model, alpha=float(alpha), E_opt=e_opt,
                             exhaustive_min=best,
                             local_rise=bool(cert and e_opt > cert[-1]["E_opt"]+1e-12)))
    OUT["hump_profiles_M512"] = dict(E_base=eb, profiles=prof)
    OUT["hump_exhaustive_M9"] = cert
    n_rise = sum(1 for c in cert if c["local_rise"])
    print(f"hump: M=9 exhaustive certification passed ({len(cert)} cells, "
          f"{n_rise} local rises); M=512 profiles recorded")
    LEDGER.append({"stage": "hump", "M9_cells": len(cert), "M9_local_rises": n_rise})
    checkpoint()

def solve_alpha_for_speedup(fn, target, lo=Fr(1,10000), hi=Fr(1)):
    slo, shi = fn(lo), fn(hi)
    if shi < target: return None, float(shi)
    if slo >= target: return float(lo), float(slo)
    for _ in range(40):
        mid = (lo+hi)/2
        if fn(mid) < target: lo = mid
        else: hi = mid
    return float((lo+hi)/2), float(fn(hi))

def crossing_stage(target=5.19):
    table = []
    M = 4096
    eb = float(E_base(M))
    xs = [Fr(k,64) for k in (1, 2, 4, 6, 8, 12)]
    for x in xs:
        for (pname, a, mu) in placements(M, x):
            b = a+mu-1
            cap_theory = eb/float((mu+1)/2)
            row = dict(x=float(x), place=pname, mu=mu,
                       speedup_cap_alpha1_any_order=cap_theory)
            for model in ("CAL", "POS"):
                def sp(alpha, proc="opt"):
                    aa = Fr(alpha).limit_denominator(10**6)
                    pi, q = posterior(M, a, b, aa, model)
                    if proc == "opt":
                        e = cost(order_opt(pi, M), pi)
                    else:
                        e = (cal_closed(M,a,b,aa,q,"com") if model=="CAL"
                             else E_pos_closed(M,a,b,aa,q,"com"))
                    return eb/float(e)
                for proc in ("opt", "com"):
                    al, spmax = solve_alpha_for_speedup(lambda t: sp(t, proc), target)
                    row[f"alpha_star{target}_{proc}_{model}"] = al
                    row[f"spmax_{proc}_{model}"] = spmax
                def sp1(alpha):
                    aa = Fr(alpha).limit_denominator(10**6)
                    pi, q = posterior(M, a, b, aa, model)
                    return eb/float(cost(order_opt(pi, M), pi))
                al1, smax1 = solve_alpha_for_speedup(sp1, 1.0)
                row[f"alpha_beat1_{model}"] = al1
            row["W_in_theory"] = float(F(M, b) - F(M, a-1))
            table.append(row)
    OUT["crossing_5p19_M4096"] = dict(target=target, E_base=float(eb), rows=table)
    LEDGER.append({"stage": "crossing", "rows": len(table)})
    checkpoint()
    return table

if __name__ == "__main__":
    stage_selftest()
    headline_numbers()
    stage_exhaustive()
    stage_randomperms()
    monotonicity_and_hump()
    speedup_table()
    crossing_stage()
    mc_stage()
    print(f"ALL STAGES DONE in {time.time()-T0:.1f}s")

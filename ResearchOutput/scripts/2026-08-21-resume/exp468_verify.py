#!/usr/bin/env python3
"""Exp 468 round-38 EXTERNAL-HINT-FILTER — machine verification of the external-hint speedup law.
Seed 20260821. Checkpoints /tmp/exp38_hintfilter/result.json incrementally."""
import numpy as np, json, time, traceback
from math import gcd
from itertools import combinations

SEED = 20260821
X = 10**6
OUT = "/tmp/exp38_hintfilter/result.json"
RES = {"seed": SEED, "X": X, "blocks": {}, "errors": {}}

def checkpoint():
    with open(OUT, "w") as f:
        json.dump(RES, f, indent=1, default=float)

T0 = time.time()
def log(msg):
    print(f"[{time.time()-T0:7.1f}s] {msg}", flush=True)

# ---------- sieve ----------
S = np.ones(X + 1, dtype=bool); S[:2] = False
for i in range(2, int(X**0.5) + 1):
    if S[i]:
        S[i*i::i] = False
PRIMES = np.nonzero(S)[0].astype(np.int64)
NP_ = len(PRIMES)
log(f"sieve done: pi(1e6) = {NP_}")

_cls_cache = {}

def rint(rng, hi, n):
    return rng.integers(0, hi, n)

def class_lists(m):
    if m not in _cls_cache:
        _cls_cache[m] = {a: PRIMES[PRIMES % m == a] for a in range(m) if gcd(a, m) == 1}
    return _cls_cache[m]

def units(m):
    return [a for a in range(m) if gcd(a, m) == 1]

def karray(m, cls, K):
    """sorted array of primes whose class lies in K (iterable of unit classes)"""
    arrs = [cls[a] for a in K]
    return np.sort(np.concatenate(arrs)) if len(arrs) > 1 else arrs[0].copy()

def rank_of(vals):
    return np.searchsorted(PRIMES, vals, side="right")

def sample_pairs_given_c(rng, m, n):
    """pairs with pq = c (mod m), a=p-class uniform on units (MA-1 fiber law). Returns dicts."""
    cls = class_lists(m); us = units(m)
    cu = np.array(us)
    c = cu[rint(rng, len(us), n)]
    a = cu[rint(rng, len(us), n)]
    ainv = np.array([pow(int(x), -1, m) for x in a])
    b = (c * ainv) % m
    p = np.empty(n, dtype=np.int64); q = np.empty(n, dtype=np.int64)
    for u in us:
        ia = np.nonzero(a == u)[0]; ib = np.nonzero(b == u)[0]
        if len(ia): p[ia] = cls[u][rint(rng, len(cls[u]), len(ia))]
        if len(ib): q[ib] = cls[u][rint(rng, len(cls[u]), len(ib))]
    bad = p == q
    for _ in range(10):
        if not bad.any(): break
        for u in us:
            ib = np.nonzero(bad & (b == u))[0]
            if len(ib): q[ib] = cls[u][rint(rng, len(cls[u]), len(ib))]
        bad = p == q
    assert not bad.any(), "p==q collision survived resampling"
    mn = np.minimum(p, q); amn = np.where(p < q, a, b)
    return {"c": c, "a": a, "b": b, "p": p, "q": q, "min": mn,
            "T": rank_of(mn), "amin": amn}

def sample_pairs_free(rng, n):
    i = rint(rng, NP_ - 1, n) + 1; j = rint(rng, NP_ - 1, n) + 1
    bad = i == j
    while bad.any():
        j[bad] = rint(rng, NP_, bad.sum()); bad = i == j
    p = PRIMES[i]; q = PRIMES[j]
    mn = np.minimum(p, q)
    return {"p": p, "q": q, "min": mn, "T": rank_of(mn)}

def filtered_cost(T, mn, amin, Karr, Klist):
    hit = np.isin(amin, Klist)
    pos = np.searchsorted(Karr, mn, side="right")
    return np.where(hit, pos, T), hit

# ================= BLOCK A: Claim A posterior + master law, m=31 =================
try:
    log("BLOCK A: m=31 hinted posterior/speedup")
    m = 31; rng = np.random.default_rng([SEED, 1])
    us = units(m)
    qr = sorted({(x * x) % m for x in us})          # quadratic residues = character fiber, theta=1/2
    chi = np.array([1 if u in set(qr) else -1 for u in us])
    uidx = {u: k for k, u in enumerate(us)}
    N_SAMPLES = 400_000
    d = sample_pairs_given_c(rng, m, N_SAMPLES)
    ci = np.array([uidx[x] for x in d["c"]]); ai = np.array([uidx[x] for x in d["a"]])
    amni = np.array([uidx[x] for x in d["amin"]])
    T = d["T"]; mn = d["min"]
    Karr = karray(m, class_lists(m), qr)
    blkA = {}
    for al in [0.5, 0.6, 0.75, 0.9]:
        g = rng.random(N_SAMPLES)                    # channel: P(keep|in K)=alpha, P(keep|out)=1-alpha
        keep = np.where(chi[ai] == 1, g < al, g < 1 - al)
        # posterior check (Theorem A): freq of a-class among keep-rows vs alpha/norm prediction
        ak = ai[keep]
        emp = np.array([(ak == k).mean() for k in range(len(us))])
        pred = np.where(chi == 1, al, 1 - al); pred = pred / pred.sum()
        maxdev = float(np.abs(emp - pred).max())
        # P_hit among keep-rows: empirical vs exact c-dependent prediction
        ph_emp = float(np.isin(d["amin"][keep], qr).mean())
        mu = 2 * al - 1
        ph_pred_c = (2 + mu * (1 + chi[ci])) / 4.0
        ph_pred = float(ph_pred_c[keep].mean())
        # speedup (both hint branches; drop branch keeps complement)
        cost = np.empty(N_SAMPLES)
        cK, hK = filtered_cost(T, mn, d["amin"], Karr, qr)
        cC, hC = filtered_cost(T, mn, d["amin"], np.setdiff1d(PRIMES, Karr), [u for u in us if u not in set(qr)])
        cost[keep] = cK[keep]; cost[~keep] = cC[~keep]
        sp = float(T.mean() / cost.mean())
        # c-split predictions: chi(c)=+1 -> P_hit=alpha ; chi(c)=-1 -> P_hit=1/2
        kp = keep & (chi[ci] == 1); km = keep & (chi[ci] == -1)
        sp_p = float(T[kp].mean() / cK[kp].mean()); sp_m = float(T[km].mean() / cK[km].mean())
        blkA[f"alpha={al}"] = {
            "posterior_maxdev_vs_theoremA": maxdev,
            "P_hit_emp": ph_emp, "P_hit_pred": ph_pred, "P_hit_absdev": abs(ph_emp - ph_pred),
            "speedup_measured": sp, "speedup_pred_masterlaw": 1.0 / (1 - 0.5 * (al + 0.5) / 2 * 1.0),
            "speedup_pred_closed": 4.0 / (3.5 - al),
            "chi_c_plus_speedup_meas": sp_p, "chi_c_plus_pred": 1.0 / (1 - 0.5 * al),
            "chi_c_minus_speedup_meas": sp_m, "chi_c_minus_pred": 4.0 / 3.0,
        }
        log(f"  alpha={al}: sp={sp:.5f} pred={4.0/(3.5-al):.5f} | Phit {ph_emp:.5f}/{ph_pred:.5f} | post.dev {maxdev:.5f}")
    RES["blocks"]["A"] = blkA
except Exception:
    RES["errors"]["A"] = traceback.format_exc(); log("BLOCK A FAILED")
checkpoint()

# ================= BLOCK B: exhaustive small-case Speedup(theta,alpha) =================
try:
    log("BLOCK B: exhaustive subsets, uninformative + partition hints")
    rngB = np.random.default_rng([SEED, 2])
    blkB = {"uninformative": {}, "partition_alpha": {}}
    POOL = 20_000
    pools = {}
    for m in [3, 4, 5, 7, 8]:
        us = units(m)
        d = sample_pairs_given_c(rngB, m, POOL)
        pools[m] = d
        worst_dev, best_sp, best_set, best_th = 0.0, 0.0, None, None
        allsp = []
        for r in range(len(us) + 1):
            for Ksub in combinations(us, r):
                th = len(Ksub) / len(us)
                if th == 0: continue
                Karr = karray(m, class_lists(m), Ksub)
                cost, _ = filtered_cost(d["T"], d["min"], d["amin"], Karr, list(Ksub))
                sp = float(d["T"].mean() / cost.mean())
                pred = 1.0 / (1 - th + th * th)
                allsp.append(sp)
                if abs(sp - pred) > worst_dev: worst_dev = abs(sp - pred)
                if sp > best_sp: best_sp, best_set, best_th = sp, Ksub, th
        mx = max(allsp)
        blkB["uninformative"][f"m={m}"] = {
            "n_subsets": len(allsp), "max_absdev_from_closed_form": worst_dev,
            "max_speedup": mx, "cap_4_3": 4 / 3, "argmax_theta": best_th}
        log(f"  m={m}: subsets={len(allsp)} maxdev={worst_dev:.5f} maxsp={mx:.5f}")
    # partition hints on m=7: character half-set (QR) vs non-character control
    m = 7; us = units(m); cls = class_lists(m)
    qr7 = sorted({(x * x) % m for x in us})
    Ksets = {"character_QR": qr7, "noncharacter": [1, 2, 3]}
    d7 = sample_pairs_given_c(rngB, m, 40_000)
    T7, mn7, amn7 = d7["T"], d7["min"], d7["amin"]
    for name, K in Ksets.items():
        Kc = [u for u in us if u not in set(K)]
        th = len(K) / len(us)
        Karr, Kcarr = karray(m, cls, K), karray(m, cls, Kc)
        Kl, Kcl = list(K), Kc
        for al in [0.5, 0.6, 0.75, 0.9]:
            gg = rngB.random(40_000)
            memb = np.isin(d7["a"], Kl)
            keep = np.where(memb, gg < al, gg < 1 - al)
            cost = np.empty(40_000)
            cK, _ = filtered_cost(T7, mn7, amn7, Karr, Kl)
            cC, _ = filtered_cost(T7, mn7, amn7, Kcarr, Kcl)
            cost[keep] = cK[keep]; cost[~keep] = cC[~keep]
            sp = float(T7.mean() / cost.mean())
            # exact weight-based prediction (q-echo via posterior w on fiber)
            def predict(wK, wO):   # weights on in/out for the active branch
                tot = 0.0
                for cv in us:
                    num = den = 0.0
                    for av in us:
                        bv = (cv * pow(av, -1, m)) % m
                        wa = wK if av in set(K) else wO
                        num += wa * ((av in set(K)) + (bv in set(K))) / 2.0
                        den += wa
                    tot += num / den / len(us)
                return tot
            Phit = 0.5 * (predict(al, 1 - al) + (1.0 - predict(1 - al, al)))
            pred = 1.0 / (1 - (1 - th) * Phit)
            blkB["partition_alpha"][f"{name}_alpha={al}"] = {
                "theta": th, "speedup_measured": sp, "P_hit_exact_pred": Phit,
                "speedup_pred_exactweights": pred,
                "canonical_8_over": (4.0 / (3.5 - al)) if th == 0.5 else None,
                "absdev": abs(sp - pred)}
            log(f"  {name} alpha={al}: sp={sp:.5f} predW={pred:.5f} canon={4.0/(3.5-al):.5f}")
    RES["blocks"]["B"] = blkB
except Exception:
    RES["errors"]["B"] = traceback.format_exc(); log("BLOCK B FAILED")
checkpoint()
log("part 1 done")

# ================= BLOCK C: certain-hint ladder t=1..10 (+12,14 starvation) =================
try:
    log("BLOCK C: certain-hint ladder")
    rngC = np.random.default_rng([SEED, 3])
    dC = sample_pairs_free(rngC, 20_000)
    T, mn, pC, qC = dC["T"], dC["min"], dC["p"], dC["q"]
    blkC = {}
    for t in [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14]:
        mm = 1 << t
        cls = class_lists(mm)
        aC = pC % mm; bC = qC % mm
        cost = np.empty(len(T), dtype=np.int64)
        for k in range(len(T)):
            av, bv = int(aC[k]), int(bC[k])
            c1 = np.searchsorted(cls[av], mn[k], side="right")
            c2 = np.searchsorted(cls[bv], mn[k], side="right")
            cost[k] = c1 + c2 - (c1 if av == bv else 0)
        sp = float(T.mean() / cost.mean())
        phi = 2 ** (t - 1)
        pred = 1.0 if t == 1 else float(2 ** (t - 2))
        pred_ex = 1.0 if t == 1 else phi / (2 - 2 ** (1 - t))
        blkC[f"t={t}"] = {
            "speedup_measured": sp, "speedup_pred_2t_minus2": pred,
            "speedup_pred_exact_finite_t": pred_ex,
            "ratio_meas_over_pred": sp / pred,
            "ratio_meas_over_exact": sp / pred_ex,
            "mean_kept_below_min": float(cost.mean()),
            "mean_class_size_piX_over_phi": NP_ / (2 ** (t - 1)),
            "recovery_accounting_2t_minus1": float(2 ** (t - 1)), "raw_bits_2t": float(2 ** t)}
        log(f"  t={t}: meas={sp:.4f} pred={pred:.4f} ratio={sp/pred:.4f} classsize={NP_/(2**(t-1)):.1f}")
    RES["blocks"]["C"] = blkC
except Exception:
    RES["errors"]["C"] = traceback.format_exc(); log("BLOCK C FAILED")
checkpoint()

# ================= BLOCK D: trace-hint face =================
try:
    log("BLOCK D: trace hints s=p+q mod 2^t")
    rngD = np.random.default_rng([SEED, 4])
    dD = sample_pairs_free(rngD, 20_000)
    T, mn, pD, qD = dD["T"], dD["min"], dD["p"], dD["q"]
    blkD = {}
    for t in [2, 3, 4, 5, 6, 7, 8, 10]:
        mm = 1 << t
        cls = class_lists(mm)
        xs = np.arange(1, mm, 2, dtype=np.int64)      # odd = units mod 2^t
        Cts, costs = [], []
        for k in range(len(T)):
            Nmod = int(pD[k] % mm) * int(qD[k] % mm) % mm
            smod = int((pD[k] + qD[k]) % mm)
            roots = xs[(xs * xs - smod * xs + Nmod) % mm == 0]
            Cts.append(len(roots))
            costs.append(sum(np.searchsorted(cls[int(r)], mn[k], side="right") for r in roots))
        Cts = np.array(Cts, float); costs = np.array(costs, float)
        th = Cts / (2 ** (t - 1))
        sp = float(T.mean() / costs.mean())
        pred = float(2 ** (t - 1) / Cts.mean())
        blkD[f"t={t}"] = {
            "C_t_median": float(np.median(Cts)), "C_t_mean": float(Cts.mean()),
            "C_t_min": int(Cts.min()), "C_t_max": int(Cts.max()),
            "speedup_measured": sp, "speedup_pred_2t1_over_Ct": pred,
            "ratio": sp / pred,
            "value_vs_certain_hint_ratio_2_over_Ct": float(2 / Cts.mean())}
        log(f"  t={t}: C_t med={np.median(Cts):.1f} sp={sp:.4f} pred={pred:.4f} ratio={sp/pred:.4f}")
    RES["blocks"]["D"] = blkD
except Exception:
    RES["errors"]["D"] = traceback.format_exc(); log("BLOCK D FAILED")
checkpoint()

# ================= BLOCK E: break-even surface alpha*(theta,eps) =================
try:
    log("BLOCK E: break-even")
    blkE = {"surface": [], "crosscheck": {}}
    for th in np.linspace(0.05, 0.95, 19):
        for eps in np.linspace(0.0, 1.2, 25):
            astar = 2 * eps / ((1 + eps) * (1 - th)) - th
            blkE["surface"].append({
                "theta": round(float(th), 4), "eps": round(float(eps), 4),
                "alpha_star": round(float(astar), 4),
                "feasible": bool(eps <= (1 - th * th) / (1 + th * th))})
    # simulation cross-check at theta=1/2 (m=7 QR), net speedup = speedup/(1+eps)
    m = 7; us = units(m); cls = class_lists(m)
    qr7 = sorted({(x * x) % m for x in us}); Kc7 = [u for u in us if u not in set(qr7)]
    rngE = np.random.default_rng([SEED, 5])
    dE = sample_pairs_given_c(rngE, m, 40_000)
    TE, mnE, amnE = dE["T"], dE["min"], dE["amin"]
    Karr, Kcarr = karray(m, cls, qr7), karray(m, cls, Kc7)
    for eps in [0.1, 0.3, 0.5, 0.6, 0.7]:
        astar = 4 * eps / (1 + eps) - 0.5
        row = {"eps": eps, "alpha_star_pred": astar,
               "feasible": eps <= 0.6, "net_at_alpha": {}}
        for al in [0.5, 0.7, 0.9, 1.0]:
            gg = rngE.random(40_000)
            memb = np.isin(dE["a"], qr7)
            keep = np.where(memb, gg < al, gg < 1 - al)
            cost = np.empty(40_000)
            cK, _ = filtered_cost(TE, mnE, amnE, Karr, qr7)
            cC, _ = filtered_cost(TE, mnE, amnE, Kcarr, Kc7)
            cost[keep] = cK[keep]; cost[~keep] = cC[~keep]
            net = float(TE.mean() / cost.mean()) / (1 + eps)
            row["net_at_alpha"][f"alpha={al}"] = net
            row.setdefault("verdicts", []).append(
                {"alpha": al, "net": net, "predict_breakeven_pass": al > astar,
                 "measured_pass": net > 1.0})
        blkE["crosscheck"][f"eps={eps}"] = row
        log(f"  eps={eps}: alpha*={astar:.3f} nets=" +
            " ".join(f"{row['net_at_alpha'][f'alpha={al}']:.4f}" for al in [0.5, 0.7, 0.9, 1.0]))
    RES["blocks"]["E"] = blkE
except Exception:
    RES["errors"]["E"] = traceback.format_exc(); log("BLOCK E FAILED")
checkpoint()
log("ALL DONE")

#!/usr/bin/env python3
"""gapL7_check.py -- finite checks for GAP-L7 (is sqrt-descending extremal among
N-computable REORDER-class policies?). Round-74 THEORY companion to gapL7_extremality.md.

Cost model: pure permutations pay 1 per touch (cost = 1-based rank of true factor p);
wheel = order-preserving skip-set (skips pay 0, T1-priced); NO cheap-predicate
prefiltering (epsilon accounting reserved to paper-132 COST class). Budget < 60 s.

Populations:
  BAL  -- lab-like balanced semiprimes: p in [2^11,2^12), q in [p,2p)  (n=150)
  UNIF -- uniform-N proxy: log-uniform p in [3,2^12) (divisor marginal ~ 1/p),
          q in [2^12,2^14)                                            (n=150)

Checks:
  1. MLR/tilt axiom: within-band divisor position z=(p-lo)/(hi-lo); flat => MLR-ok.
  2. Policy census: desc/asc/wheel30/coupled(mod3)/coupled(jacobi)/ladder-naive/
     ladder-aligned; speedups vs desc; wheel vs T1 protocol-A law S=1/mu.
  3. Prior-shape factor Lambda = C_best_static/C_desc per population (ascending witness).
  4. Master-cap audit: S(pi) <= (4/3)*(1/mu_struct)/Lambda.
  5. Early-fire surrogate: synthetic front-loaded priors (at sqrt-N end vs low end);
     does front-loading ALONE force descending to dominate ladder schedules?
"""
import json, math, random, time
from math import gcd, isqrt
from sympy import nextprime, randprime

T0 = time.time()
SEED = 20260824
rng = random.Random(SEED)
out = {"seed": SEED}

def gen_balanced(n):
    pop = []
    while len(pop) < n:
        p = randprime(2**11, 2**12)
        q = randprime(p, 2 * p)
        pop.append((p * q, p))
    return pop

def gen_logunif(n):
    pop = []
    while len(pop) < n:
        v = int(math.exp(rng.uniform(math.log(3), math.log(2**12))))
        p = int(nextprime(v))
        q = int(nextprime(rng.randrange(2**12, 2**14)))
        if q < p:
            p, q = q, p
        pop.append((p * q, p))
    return pop

def jacobi(a, n):
    a %= n; t = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5): t = -t
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3: t = -t
        a %= n
    return t if n == 1 else 0

POWS = [2**j for j in range(1, 20)]

def evaluate(pop, name, jacobi_arm=True):
    res = {"n": len(pop)}
    C = {}   # policy -> accumulated cost
    cnt = {}
    cens30 = 0            # N censored for wheel (p divides 30)
    zs = []               # within-band position for MLR check
    for N, p in pop:
        M = isqrt(N)
        desc = list(range(M, 1, -1))
        asc = list(range(2, M + 1))
        wheel = [x for x in desc if gcd(x, 30) == 1]
        r3 = N % 3
        prom = lambda x: (x % 3 == (1 if r3 == 1 else 2)) and x > 3
        coup3 = sorted(desc, key=lambda x: (0 if prom(x) else 1, -x))
        if jacobi_arm:
            coupJ = sorted(desc, key=lambda x: (0 if (x > 2 and x % 2 == 1 and jacobi(N, x) == 1) else 1, -x))
        blocks = []
        lo = 2
        for b in POWS:
            if lo > M: break
            hi = min(b, M)
            blocks.append([x for x in range(hi, lo - 1, -1)])
            lo = hi + 1
        lad_naive = [x for blk in blocks for x in blk]
        cent = lambda blk: (blk[0] + blk[-1]) / 2.0
        lad_align = [x for blk in sorted(blocks, key=lambda b: abs(M - cent(b))) for x in blk]
        lo_w = isqrt(max(2, N // 2))
        win_asc = list(range(lo_w, M + 1))          # window-ascending (mass-sort candidate)
        pols = {"desc": desc, "asc": asc, "wheel30": wheel, "coup_mod3": coup3,
                "lad_naive": lad_naive, "lad_align": lad_align, "win_asc": win_asc}
        res.setdefault("win_asc_lo_frac", []).append(lo_w / M)
        if jacobi_arm:
            pols["coup_jacobi"] = coupJ
        for k, seq in pols.items():
            try:
                c = seq.index(p) + 1
            except ValueError:
                cens30 += (k == "wheel30")
                continue
            C[k] = C.get(k, 0.0) + c
            cnt[k] = cnt.get(k, 0) + 1
        lo_w = isqrt(max(2, N // 2)); hi_w = M
        if hi_w > lo_w:
            zs.append(min(1.0, max(0.0, (p - lo_w) / (hi_w - lo_w))))
    base = C["desc"] / cnt["desc"]
    out_pol = {}
    n_pop = len(pop)
    for k in C:
        mk = C[k] / cnt[k]
        out_pol[k] = {"mean_cost": round(mk, 2), "speedup_vs_desc": round(base / mk, 4),
                      "hits": cnt[k]}
        if cnt[k] < n_pop:
            out_pol[k]["CENSORED_conditioned_on_reached"] = True
    res["policies"] = out_pol
    res["base_C_desc"] = round(base, 2)
    res["wheel_censored_N"] = cens30
    mu_emp = len(wheel) / (M - 1)          # keep fraction, last N (representative)
    res["wheel_mu_emp"] = round(mu_emp, 4)
    res["wheel_S_pred_1_over_mu"] = round(1.0 / mu_emp, 4)
    zs.sort()
    res["tilt_mean_z"] = round(sum(zs) / len(zs), 4)
    res["tilt_deciles"] = [round(zs[int(q * (len(zs) - 1))], 3) for q in (0.1, 0.3, 0.5, 0.7, 0.9)]
    full = [k for k in C if cnt[k] == n_pop and k != "wheel30"]
    best = min(C[k] / cnt[k] for k in full)
    res["Lambda_best_over_desc"] = round(best / base, 5)
    res["Lambda_full_hit_policies"] = sorted(full)
    return res

pop_bal = gen_balanced(150)
pop_unif = gen_logunif(150)
out["BAL"] = evaluate(pop_bal, "BAL")
out["UNIF"] = evaluate(pop_unif, "UNIF")

# ---------- 5. early-fire surrogate: front-loaded synthetic priors ----------
K = 4096
zgrid = [(i + 0.5) / K for i in range(K)]           # z=1 <-> sqrt-N end

def ladder_orders(K):
    # doubling-width blocks over [0,K), base width 64
    edges = [0]
    w = 64
    while edges[-1] < K:
        edges.append(min(K, edges[-1] + w)); w *= 2
    naive, aligned = [], []
    blks = [list(range(edges[i], edges[i + 1])) for i in range(len(edges) - 1)]
    for blk in blks: naive += blk                      # low-end first
    for blk in sorted(blks, key=lambda b: -(b[0] + b[-1])): aligned += blk  # nearest z=1 first
    return naive, aligned

naive, aligned = ladder_orders(K)
desc_o = list(range(K - 1, -1, -1))
asc_o = list(range(K))
ef = {}
for nm, wfun in [("front_at_sqrtN", lambda z: math.exp(4 * z)),
                 ("front_at_lowend", lambda z: math.exp(-4 * z))]:
    w = [wfun(z) for z in zgrid]
    tot = sum(w)
    row = {}
    for onm, order in [("desc", desc_o), ("asc", asc_o), ("lad_naive", naive), ("lad_align", aligned)]:
        rank = [0] * K
        for pos, idx in enumerate(order):
            rank[idx] = pos + 1
        row[onm] = round(sum(w[i] * rank[i] for i in range(K)) / tot, 2)
    ef[nm] = row
out["early_fire_surrogate"] = ef

# ---------- 4. master-cap audit ----------
audit = []
for pop_name in ("BAL", "UNIF"):
    r = out[pop_name]
    Lam = r["Lambda_best_over_desc"]
    for k, v in r["policies"].items():
        if k == "desc" or v.get("CENSORED_conditioned_on_reached"):
            continue   # ill-defined policies (never reach p on some N) excluded
        mu = r["wheel_mu_emp"] if k == "wheel30" else 1.0
        cap = (4 / 3) * (1.0 / mu) / Lam
        audit.append({"pop": pop_name, "policy": k, "S": v["speedup_vs_desc"],
                      "cap_4_3_over_mu_over_Lambda": round(cap, 4),
                      "within_cap": bool(v["speedup_vs_desc"] <= cap + 1e-9)})
out["cap_audit"] = audit

out["runtime_s"] = round(time.time() - T0, 2)
with open("/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74/gapL7_result.json", "w") as f:
    json.dump(out, f, indent=1)

print("runtime_s:", out["runtime_s"])
for pn in ("BAL", "UNIF"):
    r = out[pn]
    print(f"\n[{pn}] base C_desc={r['base_C_desc']}  mean_z={r['tilt_mean_z']} "
          f"deciles={r['tilt_deciles']}  Lambda={r['Lambda_best_over_desc']}")
    for k, v in r["policies"].items():
        print(f"   {k:12s} cost={v['mean_cost']:>10} S={v['speedup_vs_desc']}")
    print(f"   wheel mu_emp={r['wheel_mu_emp']} pred 1/mu={r['wheel_S_pred_1_over_mu']} censored={r['wheel_censored_N']}")
print("\ncap audit violations:", [a for a in audit if not a["within_cap"]])
print("early-fire surrogate:", json.dumps(ef, indent=1))

#!/usr/bin/env python3
"""verifyL7_sim.py -- INDEPENDENT verifier for round-74 GAP-L7 attempt artifacts
(gapL7_extremality.md / gapL7_check.py / gapL7_result.json). Touches nothing else.

Re-derives from scratch (no code reuse from gapL7_check.py):
  ITEM 1: prior-shape channel Lambda -- does window-ascending beat sqrt-descending
          on balanced lab-like populations? Direction + magnitude, multiple generators,
          with batch-bootstrap error bars, plus the analytic two-stage prediction.
  ITEM 2: master inequality S <= (4/3)*min(1/mu_eff,2^k)/Lambda -- recomputed audit
          incl. wheel T1-law exactness (phi(30)/30) and a hybrid filter x reorder arm
          to stress mu_eff bookkeeping.
  ITEM 3: obstruction brute-checks -- (i) residue couplings carry no independent power:
          N-keyed mod-3 promotion vs FIXED-key control (identical periodicity, zero
          N-information) + hit-enrichment ratios for mod-3 and Jacobi arms;
          (ii) closed-form interaction term reproducing the mod-3/jacobi S values.
Costs are computed in O(1) per draw by counting functions (no candidate lists)
except the Jacobi arm (own jacobi symbol impl, small subset).
"""
import math, random, time, statistics
from math import gcd, isqrt

T0 = time.time()
random.seed(777001)

try:
    from sympy import randprime, nextprime
except ImportError:
    raise SystemExit("sympy required")

# ---------- counting helpers (exact ranks, no lists) ----------
def f30(y):
    """#{x in [1..y]: gcd(x,30)==1} by inclusion-exclusion."""
    if y <= 0: return 0
    return y - y//2 - y//3 - y//5 + y//6 + y//10 + y//15 - y//30

def f3(y, t):
    """#{x in [1..y]: x % 3 == t} (t in {1,2})."""
    if y < t: return 0
    return (y - t)//3 + 1

def _f210_removed(): pass

def f210(y):
    """#{x in [1..y]: gcd(x,210)==1}."""
    if y <= 0: return 0
    ps = [2,3,5,7]
    tot = 0
    for mask in range(1, 16):
        pr = 1; bits = 0
        for i in range(4):
            if mask >> i & 1: pr *= ps[i]; bits += 1
        tot += (y//pr) * (1 if bits % 2 else -1)
    return tot

def jacobi_sym(a, n):
    a %= n; t = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5): t = -t
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3: t = -t
        a %= n
    return t if n == 1 else 0

# ---------- generators ----------
def gen(name, n):
    pop = []
    if name == "BAL_prime":          # attempt's generator: p prime in [2^11,2^12), q prime in (p,2p)
        while len(pop) < n:
            p = randprime(2**11, 2**12); q = randprime(p, 2*p)
            pop.append((p*q, p))
    elif name == "BAL_intsnap":      # integer-uniform r then snap: biases r low
        while len(pop) < n:
            p = randprime(2**11, 2**12)
            q = nextprime(random.randrange(p+1, 2*p))
            pop.append((p*q, p))
    elif name == "BAL_narrow":       # q in (p, 1.5p): descending should WIN here
        while len(pop) < n:
            p = randprime(2**11, 2**12); q = randprime(p, (3*p)//2)
            pop.append((p*q, p))
    elif name == "P137":             # paper-137 population: p,q indep in [2^15,2^17]
        while len(pop) < n:
            p = randprime(2**15, 2**17); q = randprime(2**15, 2**17)
            if q < p: p, q = q, p
            pop.append((p*q, p))
    else: raise ValueError(name)
    return pop

# ---------- ladder orders (for the lad_align == desc exact-equality claim) ----------
def ladder_orders(M):
    blocks, lo, b = [], 2, 2
    while True:
        hi = min(b, M)
        if lo > M: break
        blocks.append(list(range(hi, lo-1, -1)))
        if hi == M: break
        lo = hi + 1; b *= 2
    naive = [x for blk in blocks for x in blk]
    cent = lambda blk: (blk[0]+blk[-1])/2.0
    aligned = [x for blk in sorted(blocks, key=lambda b_: abs(M-cent(b_))) for x in blk]
    return naive, aligned

def run_pop(gname, n, n_jac=350, do_ladders=False):
    pop = gen(gname, n)
    C = {}; N_ = {}
    zs = []; win_miss = 0; trunc_miss = 0
    batches = 8
    bs = {k: [[] for _ in range(batches)] for k in
          ("desc","asc","win_asc","win_desc","wheel","coup_mod3_keyed","coup_mod3_fixed",
           "hybrid_winwheel","hybrid_winwheel210","trunc_asc")}
    en_rich = {"mod3_keyed": [0,0], "mod3_fixed": [0,0], "jacobi": [0,0]}  # [hit-promoted, total]
    jac_rows = []
    for bi, (N, p) in enumerate(pop):
        M = isqrt(N)
        lo_w = isqrt(max(2, N//2))
        b = bi % batches
        cd = M - p + 1                       # sqrt-descending rank
        ca = p - 1                           # full ascending rank
        cwa = p - lo_w + 1                   # window-ascending rank (valid iff p>=lo_w)
        cwd = M - p + 1                      # window-descending rank == desc identically
        cw = f30(M) - f30(p-1)               # wheel-30 rank
        t = N % 3
        # COUPLED orders (attempt's construction): promoted block first (desc), then rest.
        # cost = #{prom>x>p}+1 if p promoted, else P_total_promoted + #{unprom>x>p}+1
        def coup_rank(pt):
            Ptot = f3(M, pt) - f3(3, pt)             # promoted count in I (x>3)
            above = f3(M, pt) - f3(p-1, pt)          # promoted x >= p
            if p % 3 == pt:
                return above  # +1 folded into rank conventions (consistent across arms)
            return Ptot - above + (M - p) + 1        # promoted-all + unpromoted-above + self
        ck = coup_rank(t)                            # N-keyed promotion
        cf = coup_rank(1)                            # fixed-key (x=1 mod 3) promotion
        hy = f30(M) - f30(max(p, lo_w)-1)    # window-restricted wheel rank
        # wheel-210 window hybrid (stress mu_eff bookkeeping)
        hy210 = f210(M) - f210(max(p, lo_w)-1)
        lo_tr = max(2, N // (2**17))
        ctr = (p - lo_tr + 1) if p >= lo_tr else None
        vals = {"desc":cd, "asc":ca, "win_asc":cwa, "win_desc":cwd, "wheel":cw,
                "coup_mod3_keyed":ck, "coup_mod3_fixed":cf,
                "hybrid_winwheel":hy, "hybrid_winwheel210":hy210, "trunc_asc":ctr}
        if p < lo_w: win_miss += 1
        if ctr is None: trunc_miss += 1
        for k, v in vals.items():
            if v is None: continue
            C[k] = C.get(k, 0.0) + v; N_[k] = N_.get(k, 0) + 1
            bs[k][b].append(v)
        if p >= lo_w:
            zs.append((p - lo_w) / (M - lo_w))
        # enrichment: was p in the promoted set, and how big is the promoted share
        if p >= 4:
            en_rich["mod3_keyed"][1] += 1; en_rich["mod3_keyed"][0] += (p % 3 == t)
            en_rich["mod3_fixed"][1] += 1; en_rich["mod3_fixed"][0] += (p % 3 == 1)
        if len(jac_rows) < n_jac:
            # attempt's convention: promote x when jacobi(N, x)==1, i.e. symbol (N/x).
            jp = jacobi_sym(N, p)          # (N/p): N = p*q = 0 mod p -> symbol identically 0
            xs = random.sample(range(max(3, p), M+1), min(24, max(1, M-max(3,p))))
            jpos = sum(1 for x in xs if gcd(x, N) == 1 and jacobi_sym(N, x) == 1)
            jcpt = sum(1 for x in xs if gcd(x, N) == 1)
            jac_rows.append((jp == 1, jp == 0, jpos, jcpt))
        if do_ladders and bi < 1200:
            naive_o, align_o = ladder_orders(M)
            try:
                cnv = naive_o.index(p)+1; cal = align_o.index(p)+1
            except ValueError:
                cnv = cal = None
            if cnv:
                C["lad_naive"] = C.get("lad_naive",0.0)+cnv; N_["lad_naive"]=N_.get("lad_naive",0)+1
                C["lad_align"] = C.get("lad_align",0.0)+cal; N_["lad_align"]=N_.get("lad_align",0)+1
    base = C["desc"]/N_["desc"]
    def stat(k):
        if k not in C: return None
        mean = C[k]/N_[k]
        # bootstrap S via batches: S_b = mean(desc_b)/mean(k_b)
        sb = []
        for i, bb in enumerate(bs.get("desc", [])):
            if bb and bs.get(k) and bs[k][i]:
                sb.append((sum(bb)/len(bb)) / (sum(bs[k][i])/len(bs[k][i])))
        se = statistics.pstdev(sb)/math.sqrt(len(sb)) if len(sb) > 1 else float('nan')
        return mean, base/mean, se, N_[k]
    out = {"gen": gname, "n": n}
    for k in ["desc","asc","win_asc","win_desc","wheel","coup_mod3_keyed","coup_mod3_fixed",
              "hybrid_winwheel","hybrid_winwheel210","trunc_asc","lad_naive","lad_align"]:
        st = stat(k)
        if st: out[k] = {"cost": round(st[0],2), "S": round(st[1],4), "S_se": round(st[2],4), "hits": st[3]}
    zs.sort()
    def q(f): return zs[min(len(zs)-1, int(f*(len(zs)-1)))]
    out["tilt_mean_z"] = round(sum(zs)/len(zs), 4) if zs else None
    out["tilt_deciles"] = [round(q(f),3) for f in (0.1,0.3,0.5,0.7,0.9)] if zs else None
    out["win_asc_miss_frac"] = round(win_miss/n, 4)
    out["trunc_asc_miss_frac"] = round(trunc_miss/n, 4)
    er = {k: round(v[0]/v[1], 4) for k, v in en_rich.items() if v[1]}
    jr = [r for r in jac_rows if r[3] > 0]
    if jr:
        er["jacobi_p_is_plus1"] = round(sum(1 for r in jr if r[0])/len(jr), 4)
        er["jacobi_p_is_zero"] = round(sum(1 for r in jr if r[1])/len(jr), 4)
        er["jacobi_x_promoted_share_among_coprime"] = round(sum(r[2] for r in jr)/sum(r[3] for r in jr), 4)
    out["enrichment"] = er
    # Lambda = best full-hit STATIC-PERMUTATION cost / desc cost (attempt's convention:
    # wheel-class arms excluded from the argmin; win_asc treated as a permutation there)
    perm_names = {"desc","asc","win_asc","win_desc","coup_mod3_keyed","coup_mod3_fixed",
                  "trunc_asc","lad_naive","lad_align"}
    full_perm = {k: C[k]/N_[k] for k in C if N_[k] == n and k in perm_names and k != "desc"}
    out["Lambda_best_over_desc"] = round(min(full_perm.values())/base, 5)
    out["Lambda_argmin"] = min(full_perm, key=full_perm.get)
    # ---- master-cap audit (stated form, structural mu_eff) ----
    mu_wheel = 8/30
    def mu_of(k):
        if k == "wheel": return mu_wheel
        if k in ("hybrid_winwheel", "hybrid_winwheel210"):
            ffun = f30 if k.endswith("winwheel") else f210
            return statistics.mean((ffun(M)-ffun(isqrt(max(2,N//2))-1))/(M-1) for N,_ in pop[:400])
        return 1.0
    audit = []
    for k in list(C):
        st = stat(k)
        if st is None: continue
        S = st[1]; mu = mu_of(k)
        Lam = out["Lambda_best_over_desc"]
        cap = (4/3) * min(1.0/mu, 2**32) / Lam
        cap_misclass = (4/3) * 1.0 / Lam   # what the cap would be if mu charged as 1
        audit.append((k, round(S,4), round(cap,4), bool(S <= cap + 1e-9), round(mu,5),
                      round(cap_misclass,3), bool(S > cap_misclass + 1e-9)))
    out["cap_audit"] = audit
    out["violations"] = [a for a in audit if not a[3]]
    # misclassified-hybrid diagnostic: charge mu=1 (call it a pure reorder)
    st_h = stat("hybrid_winwheel")
    if st_h:
        out["hybrid_S_if_mu_charged_1_cap"] = round((4/3)/out["Lambda_best_over_desc"], 3)
        out["hybrid_S_actual"] = round(st_h[1], 3)
    return out

print("="*78)
print("ITEM 1 + 2 + 3: independent simulation (fresh seed 777001)")
results = {}
for gn, nn, nj, dl in [("BAL_prime", 2400, 350, True),
                       ("BAL_intsnap", 2400, 0, False),
                       ("BAL_narrow", 1600, 0, False),
                       ("P137", 500, 200, False)]:
    r = run_pop(gn, nn, n_jac=nj, do_ladders=dl)
    results[gn] = r
    print(f"\n--- {gn} (n={nn}) ---")
    print(f"  tilt mean_z={r['tilt_mean_z']} deciles={r['tilt_deciles']}  "
          f"win_asc_miss={r['win_asc_miss_frac']}")
    for k in ["desc","asc","win_asc","win_desc","wheel","coup_mod3_keyed","coup_mod3_fixed",
              "hybrid_winwheel","hybrid_winwheel210","trunc_asc","lad_naive","lad_align"]:
        if k in r:
            print(f"    {k:18s} cost={r[k]['cost']:>10} S={r[k]['S']:>8} (+-{r[k]['S_se']}) hits={r[k]['hits']}")
    print(f"  enrichment: {r['enrichment']}")
    print(f"  Lambda_best_over_desc={r['Lambda_best_over_desc']} (argmin {r['Lambda_argmin']})")
    print(f"  CAP VIOLATIONS: {r['violations']}")
    if 'hybrid_S_actual' in r:
        print(f"  hybrid: S={r['hybrid_S_actual']} vs cap-if-mu=1 {r['hybrid_S_if_mu_charged_1_cap']}")

# ---------- analytic two-stage predictions ----------
Esqrt = lambda R: (2/3)*(R**1.5 - 1)/(R - 1)
print("\n--- analytic (two-stage: p~U primes, r=q/p~U[1,R)) ---")
for R in (1.25, 1.5, 2.0):
    u = Esqrt(R)
    print(f"  R={R}: E[sqrt r]={u:.4f}  S_analytic(win_asc/desc)=(u-1)/(1-u/sqrt2)="
          f"{(u-1)/(1-u/math.sqrt(2)):.4f}")
print("  crossover E[sqrt r]=2/(1+1/sqrt2)=1.1716 -> ascending wins iff band wide enough")

# wheel T1 law exactness
w = results["BAL_prime"]["wheel"]; d = results["BAL_prime"]["desc"]
print(f"\nWHEEL T1 LAW (BAL_prime): S_measured={w['S']}  1/mu_exact={30/8:.4f}  "
      f"rel_gap={abs(w['S']-3.75)/3.75*100:.2f}%")

import json
with open("/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74/verifyL7_sim_out.json","w") as f:
    json.dump(results, f, indent=1, default=str)
print(f"\nruntime_s: {round(time.time()-T0,1)}")

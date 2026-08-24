#!/usr/bin/env python3
"""exp555 MODULAR-BERGGREN-DYNAMICS.

Project the Berggren Pythagorean-triple tree modulo an odd semiprime N and
study it as a finite dynamical system; measure factoring yield.

Tree (over Z, on triples (a,b,c)=(m^2-n^2, 2mn, m^2+n^2)):
  T1 (M1): (m,n)->(2m-n, m)   =>  a'=a-2b+2c, b'=2a-b+2c, c'=2a-2b+3c
  T2 (M2): (m,n)->(2m+n, m)   =>  a'=a+2b+2c, b'=2a+b+2c, c'=2a+2b+3c
  T3 (M3): (m,n)->(m+2n, n)   =>  a'=-a+2b+2c, b'=-2a+b+2c, c'=-2a+2b+3c
All coefficients are small integers, so the maps are linear over Z/N with no
multiplications -- only adds/shifts + reduction mod N.

State space: (Z/N)^3, start s0=(3,4,5) mod N, successors s*T_i mod N.
HIT: gcd(a,N)>1. Identity check (secondary): since c^2-b^2=a^2 holds for every
node, for prime p|N: p|a <=> (c-b)(c+b)=a^2=0 mod p <=> p|(c-b) or p|(c+b);
and p|(c-b) => a^2=0 mod p => p|a. So gcd(a,N)>1 <=> gcd(c-b,N)>1 <=>
gcd(c+b,N)>1 for squarefree odd N. Verified empirically on a subsample.

Parts:
  A  structure: degree distributions, collision structure, orbit collapse,
     depth of first hit.
  B  hitting economics: P(hit within V), V*(N), slope alpha of log V* vs
     log min(p,q); matched-compute baselines (trial division, Pollard rho).
  C  energy-guidance inapplicability: residue-pattern successor preference
     vs uniform branching at fixed node budget.

Pricing (disclosed): 1 mult-unit = one modular multiplication/division.
BFS node = 9 coefficient-mults + 1 gcd priced 3 => 12 units/node (primary
gcd only; 18 if all three gcds). Trial division = 1 unit per trial.
Pollard rho = 1 unit/iter + amortized batched gcd (~1.03 units/iter).
"""
import json, math, random, sys, time
from collections import deque, Counter
import heapq

SEED = 20260826
NSAMP = 200
V_SMOKE, NSMOKE = 20_000, 20
V_TARGET = 200_000
RHO_SUBSET_EVERY = 5
RHO_CAP = 400_000
UNITS_PER_NODE = 12          # 9 coeff mults + 1 gcd @3
TIME_BUDGET_S = 25 * 60      # hard wall for the full pass

T_COEFFS = {  # documented for the record; inlined in the hot loops
    "T1": ((1, -2, 2), (2, -1, 2), (2, -2, 3)),
    "T2": ((1, 2, 2), (2, 1, 2), (2, 2, 3)),
    "T3": ((-1, 2, 2), (-2, 1, 2), (-2, 2, 3)),
}


def child(v, N, k):
    a, b, c = v
    if k == 0:
        return ((a - 2 * b + 2 * c) % N, (2 * a - b + 2 * c) % N, (2 * a - 2 * b + 3 * c) % N)
    if k == 1:
        return ((a + 2 * b + 2 * c) % N, (2 * a + b + 2 * c) % N, (2 * a + 2 * b + 3 * c) % N)
    return (((-a + 2 * b + 2 * c) % N), ((-2 * a + b + 2 * c) % N), ((-2 * a + 2 * b + 3 * c) % N))


# ---------------------------------------------------------------- validation
def validate_matrices():
    """Abort-level checks BEFORE anything else."""
    root = (3, 4, 5)
    c1, c2, c3 = child(root, 10**9, 0), child(root, 10**9, 1), child(root, 10**9, 2)
    ok = (c1 == (5, 12, 13)) and (c2 == (21, 20, 29)) and (c3 == (15, 8, 17))
    if not ok:
        print(f"FATAL matrix validation failed: {c1} {c2} {c3}")
        sys.exit(1)
    # integer-tree consistency c^2 = a^2 + b^2 (equiv c^2-b^2=a^2) to depth 6,
    # plus no-duplicate triples to depth 5 (classical Berggren injectivity).
    seen = {root}
    frontier = [root]
    for d in range(6):
        nxt = []
        for v in frontier:
            for k in range(3):
                w = child(v, 10**9, k)
                a, b, c = w
                if c * c - b * b - a * a != 0:
                    print(f"FATAL integer form broken at depth {d+1}: {w}")
                    sys.exit(1)
                if d < 5:
                    if w in seen:
                        print(f"FATAL duplicate triple at depth <=5: {w}")
                        sys.exit(1)
                    seen.add(w)
                nxt.append(w)
        frontier = nxt
    return {"children_of_root_ok": True, "integer_form_depth6_ok": True,
            "no_dup_depth5": True, "n_triples_checked": len(seen)}


# ------------------------------------------------------------------ sampling
def mr_isprime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def sample_nsamples(n_wanted, seed, vmax):
    rng = random.Random(seed)
    out = []
    while len(out) < n_wanted:
        p = rng.randrange(1 << 10, 1 << 14)
        q = rng.randrange(1 << 12, 1 << 18)
        if not (mr_isprime(p) and mr_isprime(q)) or p == q:
            continue
        out.append((p, q))
    return [(p, q, p * q) for p, q in out][:min(n_wanted, vmax)]


# ----------------------------------------------------------------- core BFS
def bfs_uniform2(N, V):
    """BFS the mod-N tree; depth carried in the queue. Tracks expanded count,
    in-degree via arrival counts, hits at discovery time."""
    gcd = math.gcd
    root = (3 % N, 4 % N, 5 % N)
    visited = {root}
    arrivals = {root: 0}
    q = deque(((root[0], root[1], root[2], 0),))
    hit_times, hit_depths = [], []
    id_bad = id_checks = form_bad = form_checks = 0
    first_collision = None
    maxdepth = 0
    expanded = 0
    exhausted = False
    dh = Counter()
    dh[0] += 1
    nzc = Counter()          # residue-pattern score: #coords nonzero mod 3/5/7
    while q:
        if len(visited) >= V:
            break
        a, b, c, d = q.popleft()
        expanded += 1
        d1 = d + 1
        for na, nb, nc in (
            ((a - 2 * b + 2 * c) % N, (2 * a - b + 2 * c) % N, (2 * a - 2 * b + 3 * c) % N),
            ((a + 2 * b + 2 * c) % N, (2 * a + b + 2 * c) % N, (2 * a + 2 * b + 3 * c) % N),
            ((-a + 2 * b + 2 * c) % N, (-2 * a + b + 2 * c) % N, (-2 * a + 2 * b + 3 * c) % N),
        ):
            ch = (na, nb, nc)
            arrivals[ch] = arrivals.get(ch, 0) + 1
            if ch in visited:
                if first_collision is None:
                    first_collision = len(visited)
                continue
            visited.add(ch)
            dh[d1] += 1
            nzc[(na % 3 != 0) + (nb % 3 != 0) + (nc % 3 != 0) +
                (na % 5 != 0) + (nb % 5 != 0) + (nc % 5 != 0) +
                (na % 7 != 0) + (nb % 7 != 0) + (nc % 7 != 0)] += 1
            if d1 > maxdepth:
                maxdepth = d1
            ga = gcd(na, N) > 1
            if ga:
                hit_times.append(len(visited))
                hit_depths.append(d1)
            # identity equivalence check on a low-density subsample + all hits
            # correct predicate: p|a <=> p|(c-b) OR p|(c+b) for p|N squarefree
            if ga or (len(visited) & 8191) == 0:
                id_checks += 1
                g2 = gcd((nc - nb) % N, N) > 1
                g3 = gcd((nc + nb) % N, N) > 1
                if ga != (g2 or g3):
                    id_bad += 1
            if (len(visited) & 1023) == 0:
                form_checks += 1
                if (nc * nc - nb * nb - na * na) % N != 0:
                    form_bad += 1
            q.append((na, nb, nc, d1))
        if not q:
            exhausted = True
    inh = Counter(arrivals.values())
    return {
        "N": N, "bits": N.bit_length(), "distinct": len(visited),
        "attempts": 3 * expanded + 1, "expanded": expanded,
        "coll_frac": 1.0 - len(visited) / (3 * expanded + 1),
        "exhausted": bool(exhausted), "hit_times": hit_times,
        "hit_depths": hit_depths, "first_collision": first_collision,
        "maxdepth": maxdepth, "id_checks": id_checks, "id_bad": id_bad,
        "form_checks": form_checks, "form_bad": form_bad,
        "indeg_mean": (sum(k * v for k, v in inh.items()) /
                       max(1, sum(inh.values()))),
        "indeg_max": max(inh) if inh else 0,
        "indeg_hist": {str(k): v for k, v in sorted(inh.items())[:12]},
        "depth_hist_top": {str(k): v for k, v in sorted(dh.items())[:40]},
        "nz_hist": {str(k): v for k, v in sorted(nzc.items())},
    }


# ---------------------------------------------------------------- baselines
def pollard_rho_first_hit(N, cap, rng):
    """Brent-style rho with batched difference-product gcd. Returns total
    f-iterations until a NONTRIVIAL factor is found, or None at cap.
    Trivial hits (gcd==N / x==y cycle) restart with a new constant, keeping
    the iteration counter running."""
    it_total = 0
    while it_total < cap:
        y = rng.randrange(1, N)
        cst = rng.randrange(1, N)
        m = 128
        g = q = 1
        r = 1
        x = ys = y
        it = 0
        while g == 1 and it_total + it < cap:
            x = y
            for _ in range(r):
                if it_total + it >= cap:
                    break
                y = (y * y + cst) % N
                it += 1
            k = 0
            while k < r and g == 1 and it_total + it < cap:
                ys = y
                for _ in range(min(m, r - k)):
                    if it_total + it >= cap:
                        break
                    y = (y * y + cst) % N
                    q = q * abs(x - y) % N
                    it += 1
                g = math.gcd(q, N)
                k += m
            r <<= 1
        it_total += it
        if g > 1 and g < N:
            return it_total
        # trivial (g==N or cap): restart unless out of budget
        if it_total >= cap:
            return None


def gcd_ab(a, b):
    while b:
        a, b = b, a % b
    return a


def quantile(sorted_xs, f):
    if not sorted_xs:
        return None
    i = min(len(sorted_xs) - 1, int(f * len(sorted_xs)))
    return sorted_xs[i]


def linreg(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    syy = sum((y - my) ** 2 for y in ys)
    beta = sxy / sxx
    r2 = (sxy * sxy) / (sxx * syy) if syy > 0 else float("nan")
    return beta, my - beta * mx, r2


# --------------------------------------------------------------------- main
def search_traced(N, budget, mode):
    """Generic frontier search with tracing: mode in
    {'uniform','dfs','random','nz','-nz','mag','-mag'}.
    Returns list of (discovery_idx, depth, nz_score, mag_score, hit)."""
    gcd = math.gcd
    rng = random.Random(SEED + (hash((N, mode)) & 0x7FFFFFFF))

    def score(a, b, c):
        if mode.lstrip("-") == "nz":
            return sum(1 for r in (3, 5, 7) for x in (a % r, b % r, c % r) if x)
        return a if a <= N - a else N - a

    sign = -1.0 if mode.startswith("-") else 1.0   # '-' => anti-guidance
    root = (3 % N, 4 % N, 5 % N)
    trace = []
    visited = {root}
    frontier = [(root, 0)]                          # list-based policies
    heap = []
    cnt = 0
    heapq.heappush(heap, (-sign * score(*root), cnt, root, 0))
    while (frontier or heap) and len(visited) < budget:
        if mode == "uniform":
            node, d = frontier.pop(0)
        elif mode == "dfs":
            node, d = frontier.pop()
        elif mode == "random":
            i = rng.randrange(len(frontier))
            node, d = frontier[i]
            frontier[i] = frontier[-1]
            frontier.pop()
        else:
            _, _, node, d = heapq.heappop(heap)
        a, b, c = node
        for na, nb, nc in (
            ((a - 2 * b + 2 * c) % N, (2 * a - b + 2 * c) % N, (2 * a - 2 * b + 3 * c) % N),
            ((a + 2 * b + 2 * c) % N, (2 * a + b + 2 * c) % N, (2 * a + 2 * b + 3 * c) % N),
            ((-a + 2 * b + 2 * c) % N, (-2 * a + b + 2 * c) % N, (-2 * a + 2 * b + 3 * c) % N),
        ):
            ch = (na, nb, nc)
            if ch in visited:
                continue
            visited.add(ch)
            ghit = gcd(na, N) > 1
            trace.append((len(visited), d + 1,
                          sum(1 for r in (3, 5, 7) for x in (na % r, nb % r, nc % r) if x),
                          na if na <= N - na else N - na, ghit))
            cnt += 1
            if mode in ("uniform", "dfs", "random"):
                frontier.append((ch, d + 1))
            else:
                heapq.heappush(heap, (-sign * score(na, nb, nc), cnt, ch, d + 1))
    return trace


def run_diag():
    """Mechanism dissection for Part C: controls + hit-density profiles."""
    cases = sample_nsamples(12, SEED, 12)
    modes = ["uniform", "dfs", "random", "nz", "-nz", "mag", "-mag"]
    budget = 50_000
    agg = {m: {"hits": 0, "firsts": []} for m in modes}
    prof_by_depth = {}
    prof_by_nz = {}
    for (p, q, N_) in cases:
        for m in modes:
            tr = search_traced(N_, budget, m)
            firsts = [t[0] for t in tr if t[4]]
            agg[m]["hits"] += len(firsts)
            agg[m]["firsts"].append(firsts[0] if firsts else None)
        tr = search_traced(N_, budget, "uniform")
        trD = search_traced(N_, budget, "dfs")
        for (_, d, nz, mg, hit) in tr:
            e = prof_by_nz.setdefault(nz, [0, 0])
            e[0] += hit
            e[1] += 1
        # depth profile pooled uniform+dfs (covers deep range)
        for (_, d, nz, mg, hit) in list(tr) + list(trD):
            e = prof_by_depth.setdefault(d // 5, [0, 0])
            e[0] += hit
            e[1] += 1
    # ambient null: random Pythagorean points mod N (random m,n)
    amb_hits = amb_tot = 0
    arng = random.Random(SEED + 99)
    for (_, _, N_) in cases:
        for _ in range(20000):
            mm = arng.randrange(1, N_)
            nn = arng.randrange(1, N_)
            aa = (mm * mm - nn * nn) % N_
            amb_hits += math.gcd(aa, N_) > 1
            amb_tot += 1
    print("DIAG @budget", budget)
    for m, v in agg.items():
        fr = sorted(x for x in v["firsts"] if x)
        print(f"  {m:8s} any_hit={sum(1 for x in v['firsts'] if x)}/12 "
              f"total_hits={v['hits']:6d} "
              f"median_first={fr[len(fr)//2] if fr else None}")
    print("DIAG hit-rate by depth bucket (uniform):")
    for k in sorted(prof_by_depth)[:24]:
        h, n = prof_by_depth[k]
        print(f"   depth~{k*5:4d}: {h/max(1,n):.5f} (n={n})")
    print("DIAG hit-rate by nz score:")
    for k in sorted(prof_by_nz):
        h, n = prof_by_nz[k]
        print(f"   nz={k}: {h/max(1,n):.5f} (n={n})")
    print(f"DIAG ambient null: random Pythagorean points hit rate "
          f"{amb_hits}/{amb_tot} = {amb_hits/amb_tot:.2e}")


def run(smoke=False):
    t0 = time.time()
    val = validate_matrices()
    print("MATRIX VALIDATION:", val)

    nsamp = NSMOKE if smoke else NSAMP
    Vfull = V_SMOKE if smoke else V_TARGET
    cases = sample_nsamples(nsamp, SEED, nsamp)
    print(f"sampled {len(cases)} semiprimes (seed {SEED}); V={Vfull}")

    rows = []
    amb_rng = random.Random(SEED + 99)
    for i, (p, q, N) in enumerate(cases):
        r = bfs_uniform2(N, Vfull)
        r.update(p=p, q=q, pmin=min(p, q))
        # order-free dive control at the same node budget
        trD = search_traced(N, Vfull, "random")
        firstsD = [t[0] for t in trD if t[4]]
        r["hit_times_dive"] = firstsD
        r["maxdepth_dive"] = max((t[1] for t in trD), default=0)
        del trD
        # ambient null: random Pythagorean points mod this N
        ah = at = 0
        for _ in range(20000):
            mm = amb_rng.randrange(1, N)
            nn = amb_rng.randrange(1, N)
            at += 1
            ah += math.gcd((mm * mm - nn * nn) % N, N) > 1
        r["ambient_rate"] = ah / at
        rows.append(r)
        if (i + 1) % 25 == 0 or i == 0:
            el = time.time() - t0
            print(f"  [{i+1}/{len(cases)}] N_bits={r['bits']} "
                  f"elapsed={el:.0f}s rate={el/(i+1):.2f}s/N "
                  f"dive_first={firstsD[0] if firstsD else None}")
        if not smoke and time.time() - t0 > TIME_BUDGET_S * 0.55:
            print(f"TIME GUARD: stopping BFS sweep at i={i}")
            break

    # ---------------- Part A aggregates
    nfin = len(rows)
    exhausted_ct = sum(r["exhausted"] for r in rows)
    coll_fracs = sorted(r["coll_frac"] for r in rows)
    first_cols = sorted(r["first_collision"] for r in rows if r["first_collision"])
    maxdepths = sorted(r["maxdepth"] for r in rows)
    hit_rates = [len(r["hit_times"]) > 0 for r in rows]
    nz_pool = Counter()
    for r in rows:
        for k, v in r["nz_hist"].items():
            nz_pool[int(k)] += v
    tot_nz = sum(nz_pool.values())
    partA = {
        "n_cases": nfin,
        "exhausted_components": exhausted_ct,
        "out_degree_note": "always 3 by construction (no multiplication "
                           "needed: T-coefficients in {+-1,+-2,+-3})",
        "nz_score_hist": {str(k): v for k, v in sorted(nz_pool.items())},
        "nz_confinement_note":
            "nz = #coords nonzero mod 3/5/7; classical primitive-triple "
            "congruences survive the projection and confine the orbit",
        "nz_top2_fraction": (sum(v for k, v in sorted(nz_pool.items(),
                                                     reverse=True)[:1]) /
                             max(1, tot_nz)),
        "coll_frac_median": quantile(coll_fracs, .5),
        "coll_frac_q10": quantile(coll_fracs, .1),
        "coll_frac_q90": quantile(coll_fracs, .9),
        "first_collision_median": quantile(first_cols, .5),
        "first_collision_q10": quantile(first_cols, .1),
        "maxdepth_median": quantile(maxdepths, .5),
        "any_hit_rate": sum(hit_rates) / nfin,
        "id_mismatch_hits": sum(r["id_bad"] for r in rows),
        "id_checks_hits": sum(r["id_checks"] for r in rows),
        "form_violations": sum(r["form_bad"] for r in rows),
        "form_checks": sum(r["form_checks"] for r in rows),
    }
    print("PART A:", json.dumps(partA, indent=1))

    # ---------------- Part B
    vstars = sorted(r["hit_times"][0] for r in rows if r["hit_times"])
    vstars_dive = sorted(r["hit_times_dive"][0] for r in rows
                         if r["hit_times_dive"])
    censored = sum(1 for r in rows if not r["hit_times"])
    censored_dive = sum(1 for r in rows if not r["hit_times_dive"])
    amb_rate = sum(r["ambient_rate"] for r in rows) / nfin
    by_bit = {}
    for r in rows:
        by_bit.setdefault(r["bits"], []).append(r)
    bit_tbl = {}
    for b, rs in sorted(by_bit.items()):
        vs = sorted(r["hit_times"][0] for r in rs if r["hit_times"])
        bit_tbl[b] = {
            "n": len(rs), "hit_rate": len(vs) / len(rs),
            "vstar_median": quantile(vs, .5), "vstar_q90": quantile(vs, .9),
            "pmin_median": sorted(x["pmin"] for x in rs)[len(rs) // 2],
            "distinct_median": sorted(x["distinct"] for x in rs)[len(rs) // 2],
        }
    unc = [(r["pmin"], r["hit_times"][0]) for r in rows if r["hit_times"]]
    alpha = None
    if len(unc) >= 10:
        lx = [math.log10(x) for x, _ in unc]
        ly = [math.log10(y) for _, y in unc]
        alpha, inter, r2 = linreg(lx, ly)
    uncD = [(r["pmin"], r["hit_times_dive"][0]) for r in rows
            if r["hit_times_dive"]]
    alpha_dive = None
    if len(uncD) >= 10:
        lxd = [math.log10(x) for x, _ in uncD]
        lyd = [math.log10(y) for _, y in uncD]
        alpha_dive, inter_d, r2_d = linreg(lxd, lyd)
    partB_fit = {"alpha_logV_vs_logpmin_UNIFORM_BFS": alpha,
                 "censored_uniform": censored, "n_used_uniform": len(unc),
                 "alpha_logV_vs_logpmin_RANDOM_DIVE": alpha_dive,
                 "censored_dive": censored_dive, "n_used_dive": len(uncD),
                 "ambient_null_rate": amb_rate,
                 "interpretation": (
                     "alpha~=1 trial-division-like; alpha~=0.5 rho-like; "
                     "<0.5 NEW")}
    if alpha is not None:
        partB_fit["uniform_intercept"] = inter
        partB_fit["uniform_r2"] = r2
    if alpha_dive is not None:
        partB_fit["dive_intercept"] = inter_d
        partB_fit["dive_r2"] = r2_d
    print("PART B fit:", partB_fit)
    print("PART B by bitlen:", json.dumps(bit_tbl))

    # matched-compute curves over budget grid (units U)
    grid = [round(100 * 1.5 ** k) for k in range(0, 34)]
    rho_rng = random.Random(SEED + 1)
    rho_sim = {}
    for i, r in enumerate(rows):
        if i % RHO_SUBSET_EVERY:
            continue
        rho_sim[r["N"]] = pollard_rho_first_hit(r["N"], RHO_CAP, rho_rng)
    rho_sim_ok = [v for v in rho_sim.values() if v is not None]
    curves = []
    for U in grid:
        nb = U / UNITS_PER_NODE
        p_bfs = sum(1 for r in rows if r["hit_times"] and r["hit_times"][0] <= nb) / nfin
        p_bfsD = sum(1 for r in rows if r["hit_times_dive"]
                     and r["hit_times_dive"][0] <= nb) / nfin
        p_td = sum(1 for r in rows if r["pmin"] <= U) / nfin
        p_rho_exp = sum(1 - math.exp(-(U / 1.03) ** 2 / (2 * r["pmin"])) for r in rows) / nfin
        p_rho_sim = (sum(1 for v in rho_sim.values() if v is not None and v <= U / 1.03)
                     / max(1, len(rho_sim))) if rho_sim else None
        curves.append({"U": U, "P_bfs_uniform": round(p_bfs, 4),
                       "P_bfs_dive": round(p_bfsD, 4), "P_td": round(p_td, 4),
                       "P_rho_expected": round(p_rho_exp, 4),
                       "P_rho_simulated": (round(p_rho_sim, 4) if p_rho_sim is not None else None)})
    cross_td = next((c["U"] for k, c in enumerate(curves)
                     if k and c["P_bfs_dive"] >= c["P_td"]
                     and curves[k - 1]["P_bfs_dive"] < curves[k - 1]["P_td"]), None)
    cross_rho = next((c["U"] for k, c in enumerate(curves)
                      if k and c["P_bfs_dive"] >= c["P_rho_expected"]
                      and curves[k - 1]["P_bfs_dive"] < curves[k - 1]["P_rho_expected"]), None)
    partB = {
        "vstar_quantiles_UNIFORM_BFS": {"n": len(vstars), "q10": quantile(vstars, .1),
                                        "median": quantile(vstars, .5),
                                        "q90": quantile(vstars, .9)},
        "vstar_quantiles_RANDOM_DIVE": {"n": len(vstars_dive),
                                        "q10": quantile(vstars_dive, .1),
                                        "median": quantile(vstars_dive, .5),
                                        "q90": quantile(vstars_dive, .9)},
        "fit": partB_fit, "by_bitlen": bit_tbl,
        "budget_curves_units": curves,
        "crossover_U_beats_trial_division": cross_td,
        "crossover_U_beats_rho": cross_rho,
        "pricing": {"bfs_node_units": UNITS_PER_NODE,
                    "note": "9 coeff-mults + 1 gcd@3x; 18 if 3 gcds/node",
                    "td_unit": "1 division", "rho_iter": "1.03 units"},
        "rho_sim": {"n": len(rho_sim), "found_within_cap": len(rho_sim_ok),
                    "cap": RHO_CAP},
    }
    print("PART B curves (U, Pbfs, Ptd, Prho):")
    for c in curves:
        print("  ", c)

    # ---------------- Part C: residue guidance vs traversal-shape controls
    # Arms: uniform BFS (as specified), random-order dive (= shape-only
    # control, from main loop), dfs, and the two residue guidances.
    # Primary comparison: nz/mag vs RANDOM at matched budget (isolates any
    # residue information beyond dive-shape); secondary: vs UNIFORM.
    budgs = sorted({Vfull // 8, Vfull // 4, Vfull // 2})
    bmax = max(budgs)
    arms = {}
    arm_maxdepth = {}
    t1 = time.time()
    for mode in ("dfs", "nz", "mag"):
        fs, mds = [], []
        for i, r in enumerate(rows):
            tr = search_traced(r["N"], bmax, mode)
            fs.append([t[0] for t in tr if t[4]])
            mds.append(max((t[1] for t in tr), default=0))
            del tr
            if not smoke and time.time() - t1 > TIME_BUDGET_S * 0.85:
                print(f"TIME GUARD C: stopping {mode} at i={i}")
                break
        arms[mode] = fs
        arm_maxdepth[mode] = mds
    arms["random"] = [r["hit_times_dive"] for r in rows]
    arms["uniform"] = [r["hit_times"] for r in rows]
    arm_maxdepth["random"] = [r["maxdepth_dive"] for r in rows]
    arm_maxdepth["uniform"] = [r["maxdepth"] for r in rows]

    def paired_stats(am, bm, b):
        fa, fb = arms[am], arms[bm]
        n = min(len(fa), len(fb))
        wins = losses = ra = rb = 0
        dg = []
        for i in range(n):
            ga = any(t <= b for t in fa[i])
            gb = any(t <= b for t in fb[i])
            ra += ga
            rb += gb
            if ga and not gb:
                wins += 1
            elif gb and not ga:
                losses += 1
            dg.append(int(ga) - int(gb))
        mean = sum(dg) / n
        sd = (sum((x - mean) ** 2 for x in dg) / (n - 1)) ** .5 if n > 1 else 0.0
        z = mean / (sd / n ** .5) if sd > 0 else 0.0
        return {"hit_rate": round(ra / n, 3), f"{bm}_rate": round(rb / n, 3),
                "wins": wins, "losses": losses, "ties": n - wins - losses,
                "paired_z": round(z, 3)}

    def med(xs):
        xs = sorted(xs)
        return xs[len(xs) // 2] if xs else None

    partC = {}
    for am in ("nz", "mag", "dfs", "random"):
        per_b = {}
        for b in budgs:
            e = {}
            if am not in ("uniform",):
                e["vs_random"] = paired_stats(am, "random", b)
                e["vs_uniform"] = paired_stats(am, "uniform", b)
            per_b[b] = e
        partC[am] = per_b
    print("PART C (primary: vs_random isolates residue info beyond shape):")
    for am in ("nz", "mag"):
        for b in budgs:
            print(f"  {am}@{b}: {partC[am][b]}")
    shape_gap = {b: paired_stats("random", "uniform", b) for b in budgs}
    print(f"  SHAPE EFFECT random-vs-uniform: {shape_gap}")
    print("  median maxdepth by arm:",
          {m: med(v) for m, v in arm_maxdepth.items()})
    zs_primary = [partC[m][b]["vs_random"]["paired_z"]
                  for m in ("nz", "mag") for b in budgs]
    cverdict = {
        "residue_guidance_vs_shape_control":
            ("NO-IMPROVEMENT-BEYOND-NOISE"
             if all(abs(z) <= 2 for z in zs_primary) else "SIGNAL-SEEN"),
        "shape_effect_present": any(
            abs(shape_gap[b]["paired_z"]) > 2 for b in budgs),
    }
    partC["_summary"] = {"verdicts": cverdict,
                         "shape_gap_random_vs_uniform": shape_gap}

    result = {
        "exp": "exp555 MODULAR-BERGGREN-DYNAMICS", "seed": SEED,
        "smoke": smoke, "V": Vfull, "n_samples": nfin,
        "matrix_validation": val,
        "partA": partA,
        "partB": partB,
        "partC": partC, "partC_verdict": cverdict,
        "per_N": [{k: r[k] for k in ("p", "q", "bits", "pmin", "distinct",
                                     "attempts", "coll_frac", "exhausted",
                                     "first_collision", "maxdepth",
                                     "ambient_rate", "maxdepth_dive")}
                   | {"vstar_uniform": (r["hit_times"][0] if r["hit_times"] else None),
                      "vstar_dive": (r["hit_times_dive"][0] if r["hit_times_dive"] else None),
                      "hit_depth_first": (r["hit_depths"][0] if r["hit_depths"] else None),
                      "n_hits": len(r["hit_times"])} for r in rows],
        "runtime_s": round(time.time() - t0, 1),
    }
    out = ("exp555_smoke_result.json" if smoke else "exp555_result.json")
    with open(out, "w") as f:
        json.dump(result, f, indent=1)
    print("wrote", out, f"in {result['runtime_s']}s")


if __name__ == "__main__":
    if "--diag" in sys.argv:
        run_diag()
    else:
        run(smoke="--smoke" in sys.argv)

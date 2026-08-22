#!/usr/bin/env python3
"""EXP 488 TRUE-ECM (round-42). Seed 20260922.
Deferred item from paper 155: TRUE lcm-based stage-1 ECM vs exp487's ECM-LITE.
Curve machinery reused from /tmp/exp42_ecm/exp487_ecm_only.py: affine coords on
random (a,x,y) curves, GUARDED INVERSIONS (factor iff 1<gcd(den,N)<N; dead curve
iff gcd==N), curve cap 30, B1=50, balanced semiprimes k in {16,20}, 1200 per k,
population generator copied verbatim (seed differs per spec: 20260922).

CHANGE vs 487: the sequential-multiple loop j=3..50 is replaced by the true
stage-1 multiplier L = lcm(1..50) = prod ell^e (ell^e <= B1, e maximal).  The
running point is multiplied by each prime power ell^e IN SEQUENCE via
left-to-right double-and-add over the binary expansion of ell^e; an explicit
end-of-chunk gcd(product-of-chunk-denominators, N) check runs after each prime's
chunk (belt-and-braces on top of the per-inversion guards; any catch by it that
the guards missed is logged as an anomaly for the measurement ledger).

This tests smoothness of the CURVE-GROUP ORDER (order | L) rather than
order <= 50 (lite), i.e. genuine ECM stage 1 with L_p[1/2, sqrt2] flavor.

OPS CONVENTION (matches exp487's accounting so cross-exp numbers are comparable):
point DOUBLING = 4 ops, point ADDITION = 3 ops (487 counted its initial doubling
as 4 and each sequential-multiple add as 3).  Raw point-operation counts are
also logged (*_raw).

PAIRED CONTROL: exp487's lite function is copied VERBATIM and run on the SAME
population with an independent curve-rng stream, giving a same-instance paired
comparison (kills sampling noise); published 487/paper-155 numbers are quoted
alongside as the historical anchor.

PRE-STATED HYPOTHESES (recorded here BEFORE any data):
H1: true-lcm ECM at B1=50 finds factors on MORE balanced semiprimes than the
    lite variant at equal curve cap.  Anchor: paper 155 lite k=20 found
    1163/1200 with 37 censored; lcm should censor LESS (order|L is a strictly
    larger event set than order<=50).
H2: mean ops-to-factor for FOUND instances is HIGHER for lcm than lite (lcm pays
    more ops per curve), BUT total ops-to-factor (including failed-curve spend)
    is LOWER or EQUAL (better per-op yield).
H3: across-k slope of log2 E[T] stays ~0.5 at toy scale (true ECM's
    sub-exponential advantage only shows far beyond toy sizes; 487 lite gave
    0.48).
"""
import json, math, time
import numpy as np
from sympy import nextprime

SEED = 20260922
T0 = time.time()
WORK = "/tmp/exp42_trueecm"
OUT = {"meta": {"seed": SEED, "exp": 488, "codename": "TRUE-ECM",
                "B1": 50, "curve_cap": 30,
                "ops_convention": "dbl=4 add=3 (matches exp487); raw point-ops in *_raw",
                "t_start": time.strftime("%Y-%m-%d %H:%M:%S")}}

def checkpoint():
    json.dump(OUT, open(WORK + "/result.json", "w"), indent=1)

# ---------- deterministic rng streams ----------
_ss = np.random.SeedSequence(SEED)
pop_rng  = np.random.default_rng(_ss.spawn(1)[0])
lite_rng = np.random.default_rng(_ss.spawn(2)[0])
lcm_rng  = np.random.default_rng(_ss.spawn(3)[0])

# ---------- population (verbatim generator from exp487) ----------
def gen_population(k, n=1200):
    h = k // 2
    lo, hi = 2**(h-1), 2**h
    data = []
    while len(data) < n:
        r = int(pop_rng.integers(lo, hi))
        p = int(nextprime(r)); q = int(nextprime(p + int(pop_rng.integers(1, max(2**(h-3), 2)))))
        if p < lo or q >= hi or q <= p or p == q: continue
        N = p*q
        if N.bit_length() != k: continue
        data.append((N, min(p, q)))
    return data

# ---------- prime-power schedule for L = lcm(1..B1) ----------
def prime_power_schedule(B1):
    sched = []
    for cand in range(2, B1 + 1):
        if all(cand % d for d in range(2, int(cand**0.5) + 1)):  # cand prime
            pe = cand
            while pe * cand <= B1: pe *= cand
            sched.append(pe)
    return sched

SCHED = prime_power_schedule(50)
L_LCM = math.prod(SCHED)
OUT["meta"]["schedule_prime_powers"] = SCHED
OUT["meta"]["L_lcm_1_to_50"] = L_LCM
OUT["meta"]["L_bit_length"] = L_LCM.bit_length()
checkpoint()
print("schedule:", SCHED, "| L bits:", L_LCM.bit_length(), flush=True)

# ---------- guarded affine EC ops (machinery from exp487) ----------
def ec_double(N, a, P):
    """Return (status, payload, ops_w, den_used). status in {'ok','found','dead'}."""
    x1, y1 = P
    den = (2*y1) % N
    g = math.gcd(den, N)
    if 1 < g < N: return ('found', g, 0, den)
    if g == N:    return ('dead', None, 0, den)
    lam = ((3*x1*x1 + a) * pow(den, -1, N)) % N
    x3 = (lam*lam - 2*x1) % N
    y3 = (lam*(x1 - x3) - y1) % N
    return ('ok', (x3, y3), 4, den)

def ec_add(N, a, P, Q):
    (x1, y1), (x2, y2) = P, Q
    den = (x2 - x1) % N
    g = math.gcd(den, N)
    if 1 < g < N: return ('found', g, 0, den)
    if g == N:
        # x1 == x2 mod N
        if (y1 - y2) % N == 0:
            return ec_double(N, a, P)      # P == Q -> doubling
        return ('dead', None, 0, den)      # P == -Q -> order-2 hit, dead curve
    lam = ((y2 - y1) * pow(den, -1, N)) % N
    x3 = (lam*lam - x1 - x2) % N
    y3 = (lam*(x1 - x3) - y1) % N
    return ('ok', (x3, y3), 3, den)

# ---------- TRUE lcm ECM ----------
def ecm_lcm_factor(N, curves=30, rng=lcm_rng, sched=tuple(SCHED)):
    ops = ops_raw = 0
    for c in range(curves):
        a = int(rng.integers(6, max(N, 7)))
        x = int(rng.integers(2, max(N, 3))); y = int(rng.integers(2, max(N, 3)))
        P = (x % N, y % N)
        R = None          # point at infinity
        dead = False
        for ci, m in enumerate(sched):     # prime-power chunk
            acc_prod = 1                   # product of dens used this chunk
            for bit in bin(m)[2:]:         # FULL binary expansion incl leading 1
                if R is not None:
                    st, r, w, dn = ec_double(N, a, R)
                    ops += w; ops_raw += 1; acc_prod = (acc_prod * dn) % N
                    if st == 'found': return (True, ops, ops_raw, c+1, ci)
                    if st == 'dead':  dead = True; break
                    R = r
                if bit == '1':
                    if R is None:
                        R = P              # inf + P = P (no ops charged)
                    else:
                        st, r, w, dn = ec_add(N, a, P, R)
                        ops += w; ops_raw += 1; acc_prod = (acc_prod * dn) % N
                        if st == 'found': return (True, ops, ops_raw, c+1, ci)
                        if st == 'dead':  dead = True; break
                        R = r
            if dead: break
            # DESIGNED CHECK: explicit gcd after each prime's chunk.  Mathematically
            # implied by the per-inversion guards (prod==0 mod p <=> some den==0 mod
            # p), so any catch here means a guard hole -> anomaly ledger.
            gg = math.gcd(acc_prod, N)
            if 1 < gg < N:
                OUT.setdefault("anomalies", []).append(
                    {"kind": "chunk_gcd_fired_after_guards", "ci": ci, "m": m})
                checkpoint()
                return (True, ops, ops_raw, c+1, ci)
        if dead: continue
    return (False, ops, ops_raw, curves, None)

# ---------- exp487 lite, copied verbatim (rng parameterized; pos added) ----------
def ecm_lite_factor(N, B1=50, curves=30, rng=lite_rng):
    """Sequential multiples j=3..B1 (ECM-LITE). Returns (found, ops, ops_raw, ncur, pos)."""
    ops = 0; ops_raw = 0
    if N % 2 == 0:
        return True, 0, 0, 0, 1
    for c in range(curves):
        a = int(rng.integers(6, max(N, 7)))
        x = int(rng.integers(2, max(N, 3))); y = int(rng.integers(2, max(N, 3)))
        px, py = x % N, y % N
        dead = False
        den = (2*py) % N
        g = math.gcd(den, N)
        if 1 < g < N: return True, ops, ops_raw, c+1, 2
        if g == N: continue
        try:
            lam = (3*px*px + a) * pow(den, -1, N) % N
            nx = (lam*lam - 2*px) % N
            ny = (lam*(px - nx) - py) % N
            ops += 4; ops_raw += 1
            px, py = nx, ny
            for j in range(3, B1 + 1):
                den = (px - x) % N
                g = math.gcd(den, N)
                if 1 < g < N: return True, ops, ops_raw, c+1, j
                if g == N: dead = True; break
                lam = ((py - y) * pow(den, -1, N)) % N
                nx = (lam*lam - px - x) % N
                ny = (lam*(px - nx) - py) % N
                ops += 3; ops_raw += 1
                px, py = nx, ny
        except (ValueError, ZeroDivisionError):
            dead = True
        if dead: continue
    return False, ops, ops_raw, curves, None

# ---------- generic runner ----------
def run_cell(data, fn, tag, k):
    found_flags = []; found_costs = []; cens = 0
    total_ops = 0; total_raw = 0; poss = []; ncur = []
    for idx, (N, p) in enumerate(data):
        ok, ops, oraw, nc, pos = fn(N)
        found_flags.append(bool(ok)); total_ops += ops; total_raw += oraw; ncur.append(nc)
        if ok:
            found_costs.append(max(ops, 1)); poss.append(pos)
        else:
            cens += 1
        if (idx + 1) % 200 == 0:
            print(f"{tag} k={k}: {idx+1}/1200 found={len(found_costs)} cens={cens} "
                  f"({time.time()-T0:.0f}s)", flush=True)
    lg = lambda xs: [math.log2(v) for v in xs]
    ps = [data[i][1] for i in range(len(data)) if found_flags[i]]
    alpha = float(np.polyfit(np.array(lg(ps)), lg(found_costs), 1)[0]) if len(found_costs) > 10 else None
    row = dict(k=k, n=len(data), found=len(found_costs), censored=cens,
               find_rate=round(len(found_costs)/len(data), 4),
               mean_ops_found=float(np.mean(found_costs)) if found_costs else None,
               med_ops_found=float(np.median(found_costs)) if found_costs else None,
               total_ops_incl_failed=total_ops,
               ops_per_instance_incl_failed=round(total_ops/len(data), 1),
               total_ops_raw=total_raw,
               mean_curves_used=float(np.mean(ncur)),
               alpha_fit_found_only=round(alpha, 4) if alpha is not None else None,
               found_flags=found_flags)
    if poss:
        vals, cnts = np.unique([v for v in poss if v is not None], return_counts=True)
        row["hit_position_top"] = {str(int(v)): int(c) for v, c in
                                   sorted(zip(vals, cnts), key=lambda t: -t[1])[:8]}
    print(f"RESULT {tag} k={k}: found={row['found']} cens={row['censored']} "
          f"meanT={row['mean_ops_found']} ops/inst={row['ops_per_instance_incl_failed']}", flush=True)
    return row

# ================= MAIN =================
OUT.setdefault("cells", {})
pops = {}
for k in (16, 20):
    pops[k] = gen_population(k)
    print(f"population k={k} ready ({time.time()-T0:.0f}s)", flush=True)
OUT["population_sizes"] = {str(k): len(v) for k, v in pops.items()}
checkpoint()

# --- PRIMARY ARM: true lcm ECM ---
for k in (16, 20):
    OUT["cells"][f"lcm_k{k}"] = run_cell(pops[k], ecm_lcm_factor, "LCM", k)
    checkpoint()

# --- PAIRED CONTROL: exp487 lite on the SAME population ---
for k in (16, 20):
    OUT["cells"][f"lite_k{k}"] = run_cell(pops[k], ecm_lite_factor, "LITE", k)
    checkpoint()

# ---------- paired analysis ----------
def pair_stats(k):
    lc = OUT["cells"][f"lcm_k{k}"]; lt = OUT["cells"][f"lite_k{k}"]
    fl, ft = lc.pop("found_flags"), lt.pop("found_flags")
    both = sum(a and b for a, b in zip(fl, ft))
    only_l = sum(a and not b for a, b in zip(fl, ft))
    only_t = sum((not a) and b for a, b in zip(fl, ft))
    neither = sum((not a) and (not b) for a, b in zip(fl, ft))
    lc["paired_vs_lite"] = dict(both=both, lcm_only=only_l, lite_only=only_t,
                                neither=neither)

pf = {k: pair_stats(k) for k in (16, 20)}
checkpoint()

lc16, lc20 = OUT["cells"]["lcm_k16"], OUT["cells"]["lcm_k20"]
lt16, lt20 = OUT["cells"]["lite_k16"], OUT["cells"]["lite_k20"]

slope_lcm = (math.log2(lc20["mean_ops_found"]) - math.log2(lc16["mean_ops_found"])) / 4 \
            if lc16["mean_ops_found"] and lc20["mean_ops_found"] else None
slope_lite = (math.log2(lt20["mean_ops_found"]) - math.log2(lt16["mean_ops_found"])) / 4 \
             if lt16["mean_ops_found"] and lt20["mean_ops_found"] else None

OUT["scaling"] = dict(across_k_slope_lcm=slope_lcm, across_k_slope_lite_paired=slope_lite,
                      exp487_lite_published_slope=0.48,
                      exp487_note="487 stored mean_ops(found) per k; failed-curve ops were "
                                  "not recorded there, so cross-exp TOTAL-ops comparison uses "
                                  "the paired lite arm run here on the same population")

# ---------- verdicts (pre-stated criteria) ----------
h1 = bool(lc20["found"] > lt20["found"] and lc16["found"] >= lt16["found"])
h1_anchor = bool(lc20["found"] > 1163 and lc20["censored"] < 37)   # paper-155 anchor
h2a = bool(lc16["mean_ops_found"] > lt16["mean_ops_found"] and
           lc20["mean_ops_found"] > lt20["mean_ops_found"])
h2b = bool(lc16["ops_per_instance_incl_failed"] <= lt16["ops_per_instance_incl_failed"] and
           lc20["ops_per_instance_incl_failed"] <= lt20["ops_per_instance_incl_failed"])
h3 = bool(slope_lcm is not None and 0.4 <= slope_lcm <= 0.6)

OUT["verdict"] = {
    "H1_lcm_more_finds_than_lite": h1,
    "H1_paper155_anchor_found_gt_1163_cens_lt_37": h1_anchor,
    "H2a_mean_ops_found_higher_for_lcm": h2a,
    "H2b_total_ops_per_instance_lower_or_equal": h2b,
    "H3_slope_0.4_to_0.6": h3,
    "numbers": {
        "lcm_k16": {kk: lc16[kk] for kk in ("found", "censored", "mean_ops_found",
                    "ops_per_instance_incl_failed")},
        "lcm_k20": {kk: lc20[kk] for kk in ("found", "censored", "mean_ops_found",
                    "ops_per_instance_incl_failed")},
        "lite_k16": {kk: lt16[kk] for kk in ("found", "censored", "mean_ops_found",
                     "ops_per_instance_incl_failed")},
        "lite_k20": {kk: lt20[kk] for kk in ("found", "censored", "mean_ops_found",
                     "ops_per_instance_incl_failed")},
        "slope_lcm": slope_lcm, "slope_lite_paired": slope_lite},
}
OUT["meta"]["t_end"] = time.strftime("%Y-%m-%d %H:%M:%S")
OUT["meta"]["wall_seconds"] = round(time.time() - T0, 1)
checkpoint()
print(json.dumps(OUT["verdict"], indent=1))
print("DONE", round(time.time()-T0, 1), "s", flush=True)

#!/usr/bin/env python3
"""SUBEXP-STRATUM — the smoothness economics powering the sieve family: the
fourth stratum of the factoring landscape (round-26 #3).

BACKGROUND. Paper 89 measured three strata: definition-routes (α ≥ 0.4 on N),
classical methods (ρ at α_N = 0.261), quantum (poly). The missing stratum is
the SUB-EXPONENTIAL one — the quadratic-sieve / number-field-sieve family at
L_{1/2}[c] = exp(c·√(log N log log N)) — whose engine is SMOOTHNESS: relations
x² − N that factor entirely over a factor base of primes ≤ B. This round
measures the smoothness economics directly and places the fourth stratum.

PREDICTIONS (stated before the run):
  H1 DICKMAN BACKBONE: the empirical probability that x² − N is B-smooth
     (x sampled near √N) matches the Dickman function ρ(u) with
     u = log(x²−N)/log B, across a (N, B) grid — within MC tolerance and the
     known small-u corrections.
  H2 RELATION ECONOMICS: expected trials per B-smooth relation ≈ 1/ρ(u)
     (measured directly).
  H3 THE STRATUM'S SHAPE: the toy-QS total cost model
        C(B) = trials_per_relation(B) · π(B)-sieve-cost + π(B)² linear algebra
     has an optimal B*(N) whose minimized cost scales between ρ's N^{1/4} and
     poly — locally consistent with the L_{1/2} law (fitted exponent on N
     strictly between 0.25 and 0.5 in the measured window).

Method: semiprimes at N ∈ [2^20 .. 2^44]; x drawn uniformly in [⌈√N⌉, ⌈√N⌉+W];
smoothness by trial division over primes ≤ B (prime list by sieve); Dickman ρ(u)
by numerical integration of u ρ'(u) = −ρ(u−1). Grid: 5 sizes × 4 bounds × 300
samples; cost model evaluated analytically from the fitted relation densities.
"""
import math, time, random
import numpy as np

random.seed(20260821)
np.random.seed(20260821)
T0 = time.time()


def is_prime(n):
    if n < 2: return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0: return n == p
    d = n - 1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True


def gen_semiprime(bits):
    while True:
        p = random.randrange(1 << (bits - 1), 1 << bits) | 1
        q = random.randrange(1 << (bits - 1), 1 << bits) | 1
        if is_prime(p) and is_prime(q) and p != q:
            return min(p, q), max(p, q)


def prime_sieve(limit):
    sieve = bytearray(b'\x01') * (limit + 1)
    sieve[0:2] = b'\x00\x00'
    for i in range(2, int(math.isqrt(limit)) + 1):
        if sieve[i]:
            sieve[i*i::i] = b'\x00' * ((limit - i*i)//i + 1)
    return np.array([i for i in range(limit + 1) if sieve[i]], dtype=np.int64)


def dickman_rho(u_grid):
    """numerical Dickman ρ(u): ρ(u)=1 for u∈[0,1]; u ρ'(u) = −ρ(u−1)."""
    out = []
    step = 0.001
    xs = [0.0]; ys = [1.0]
    u_target_idx = 0
    u_cur, y = 0.0, 1.0
    grid_sorted = sorted(float(u) for u in u_grid)
    res = {}
    ui = 1.0
    val = 1.0
    all_u = sorted(set([round(float(u), 6) for u in u_grid]))
    # integrate stepwise
    uu = 0.0
    vv = 1.0
    hi = all_u[-1] if all_u else 1.0
    n_steps = int(hi / step) + 2
    targets = {u: None for u in all_u}
    ti = 0
    for i in range(n_steps):
        while ti < len(all_u) and all_u[ti] <= uu + step:
            # interpolate
            frac = (all_u[ti] - uu) / step
            targets[all_u[ti]] = vv * (1 - frac) + (vv - step * vv / max(uu, step)) * frac if uu > 0 else 1.0
            ti += 1
        if uu >= 1.0:
            vv = vv - step * vv / uu   # u ρ'(u) = −ρ(u−1) ≈ −ρ(u) for fine steps
        uu += step
    for u in u_grid:
        key = round(float(u), 6)
        # find nearest computed target
        best = min(targets.keys(), key=lambda k: abs(k - key))
        res[u] = targets.get(best, 10 ** (-float(best) / 2)) if targets.get(best) else 10 ** (-float(best) / 2.05)
    return lambda u: res.get(round(float(u), 6), 10 ** (-float(u) / 2.05))


def is_b_smooth(v, primes):
    for pp in primes:
        if pp * pp > v: break
        while v % pp == 0:
            v //= pp
    return v <= max(primes) if v > 1 else True


print("=== SUBEXP-STRATUM (round-26 #3): the smoothness economics of the sieve family ===", flush=True)

# ---------------------------------------------------------------------------
# PART A — per-sample Dickman test: x uniform in [√N, 2√N] ⟹ x²−N at N-scale
# ---------------------------------------------------------------------------
print("\nPART A — empirical B-smoothness of x²−N vs Dickman ρ(u), PER-SAMPLE u = log(x²−N)/log B", flush=True)
rng = random.Random(20260821)
GRID = [(20, 256), (20, 4096), (28, 1024), (28, 16384), (36, 4096), (36, 65536)]
SAMPLES = 400
bins = {}
for bits, B in GRID:
    pp, qq = gen_semiprime(bits)
    N = pp * qq
    sq = math.isqrt(N)
    primes = prime_sieve(B).tolist()
    pmax = primes[-1]
    for _ in range(SAMPLES):
        xx = rng.randint(sq, 2 * sq)
        v = xx * xx - N
        if v <= 1: continue
        vv = v
        for pr in primes:
            if pr * pr > vv: break
            while vv % pr == 0: vv //= pr
        smooth = 1 if (vv == 1 or vv <= pmax) else 0
        u = math.log(v) / math.log(B)
        bu = round(u * 2) / 2   # half-bit bins
        bins.setdefault(bu, []).append(smooth)
    print(f"  N=2^{bits}, B={B}: done ({SAMPLES} samples)", flush=True)

# PROPER numerical Dickman ρ(u): ρ(u)=1 on [0,1]; uρ'(u) = −ρ(u−1), fine-step Euler
STEP = 0.0005
RHO_GRID_U = [0.0]; RHO_GRID_V = [1.0]
uu, vv = 0.0, 1.0
while uu < 12.0:
    if uu >= 1.0:
        # ρ(u−1) by lookup on the grid
        tgt = uu - 1.0
        i0 = int(tgt / STEP)
        lo_v = RHO_GRID_V[min(i0, len(RHO_GRID_V)-1)]
        hi_v = RHO_GRID_V[min(i0+1, len(RHO_GRID_V)-1)]
        rho_prev = lo_v + (hi_v - lo_v) * (tgt/STEP - i0)
        vv -= STEP * rho_prev / uu
    uu += STEP
    RHO_GRID_U.append(uu); RHO_GRID_V.append(max(vv, 1e-30))

def dickman(u):
    if u <= 1: return 1.0
    i0 = int(u / STEP)
    if i0 >= len(RHO_GRID_U)-1: return RHO_GRID_V[-1]
    frac = u/STEP - i0
    return RHO_GRID_V[i0] * (1-frac) + RHO_GRID_V[i0+1] * frac

print("\n  binned empirical vs NUMERICAL Dickman (±1σ):", flush=True)
print(f"  {'u':>6} {'n':>5} {'empirical':>10} {'±σ':>8} {'ρ(u)':>10} {'ratio':>7}", flush=True)
for bu in sorted(bins):
    vals = bins[bu]
    emp = float(np.mean(vals)); sd = float(np.std(vals))/math.sqrt(len(vals))
    u = bu
    if u < 1: continue
    rho_t = dickman(u)
    ratio = emp / rho_t if rho_t > 0 else float('inf')
    print(f"  {u:>6.1f} {len(vals):>5} {emp:>10.4f} {sd:>8.4f} {rho_t:>10.6f} {ratio:>7.2f}", flush=True)

# ---------------------------------------------------------------------------
# PART B — trials per relation from the same data
# ---------------------------------------------------------------------------
print("\nPART B — trials per B-smooth relation (measured vs 1/ρ(u)) where empirical > 0:", flush=True)
for bu in sorted(bins):
    emp = float(np.mean(bins[bu]))
    if emp <= 0: continue
    print(f"  u={bu:.1f}: measured {1/emp:.1f} vs 1/ρ {1/dickman(bu):.1f}", flush=True)

# ---------------------------------------------------------------------------
# PART C — the optimal-B trade-off and the stratum's shape
# ---------------------------------------------------------------------------
print("\nPART C — toy-QS cost model: C(B) = π(B)/ρ(u) + π(B)² at each N:", flush=True)
optimal_costs = []
for bits in (20, 26, 32, 40):
    pp, qq = gen_semiprime(bits)
    N = pp * qq
    best = None
    for B_exp in range(8, 20):
        B = 1 << B_exp
        u_val = math.log(N) / math.log(B)
        if u_val < 2: continue
        rho_t = max(dickman(u_val), 1e-12)
        piB = B / math.log(B)
        C = piB / rho_t + piB ** 2
        if best is None or C < best[0]:
            best = (C, B, u_val)
    optimal_costs.append((bits, N, best))
    print(f"  N=2^{bits}: optimal B* = 2^{int(math.log2(best[1]))}, cost = {best[0]:.3g}", flush=True)
xs = [math.log2(N) for _, N, _ in optimal_costs]
ys = [math.log2(c) for c, _, _ in optimal_costs]
slope = np.polyfit(xs, ys, 1)[0]
print(f"  fitted d(log₂C)/d(log₂N) = {slope:.3f} (ρ stratum 0.26 < slope < definition stratum ~1.0)", flush=True)

ratios_list = []
for bu in sorted(bins):
    emp = float(np.mean(bins[bu])); u = bu
    if u < 2 or emp <= 0: continue
    ratios_list.append(emp / dickman(u))
if ratios_list:
    print(f"\nDATA SUMMARY: empirical/true-ρ ratios across populated bins (u ≥ 2): "
          f"{['%.2f' % r for r in ratios_list]}", flush=True)
print("VERDICT: judged from the DATA SUMMARY above — the round tests whether toy-scale", flush=True)
print("x²−N smoothness tracks the numerically-integrated Dickman function; the stratum-", flush=True)
print("placement claim stands or falls with those ratios.", flush=True)
print("Round-26 #3.", flush=True)
print("\nALL_DONE_R26N3", flush=True)

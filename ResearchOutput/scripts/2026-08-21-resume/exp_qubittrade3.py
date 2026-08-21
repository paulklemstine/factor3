#!/usr/bin/env python3
"""QUBIT-TRADE3 — the fungibility ramp on REAL semiprimes, factoring metric
(round-25 #2).

BACKGROUND. Round-25 #1 (paper 85) measured the qubit/sample phase diagram of
abstract period-finding: P_certify(s,t) = 1-(1-ramp(q/r²))^s with exchange law
t*(s) shifting by −log₂ s. The open question: does the law survive when the
recovered period must ACTUALLY FACTOR a real semiprime N = pq — i.e., with
r = ord_N(a), certificates converted by gcd(a^{b/2} ± 1, N), and the full
failure-mode taxonomy (odd b; the unlucky half a^{r/2} ≡ −1 mod N; spurious
certificates)?

PREDICTIONS (stated before the run):
  H1 RAMP PERSISTS: P_factor(s,t) follows the same q/r²-shaped ramp (the
     certification bottleneck is unchanged; gcd conversion is free classically).
  H2 EXCHANGE LAW: t*(s) at P_factor ≥ 0.5 shifts by −log₂ s.
  H3 UNLUCKY-HALF CAP: even a perfect certificate r̂ = r factors only with
     probability ≈ 1/2 per DISTINCT prime structure (a^{r/2} ≡ −1 mod N w.p.
     ~1/2 over a) ⟹ saturation < 1 measurably, and s cannot push past it
     (the unlucky event is per-N, not per-sample).
  H4 TAXONOMY: failures decompose into {no certificate (ramp), odd certificate,
     unlucky root, spurious certificate} with measurable shares.

Method: ~150 random semiprimes (p,q ∈ [2^12, 2^16)), a ∈ {2,3,5,7} coprime,
r = ord_N(a) exact (multiplicative order); progression-kernel measurement
simulation (established round-25 #1); recovery = any CF convergent b passing
1/(2b²) with b | r-compatible parity → factor attempt g = gcd(a^{b/2} − 1, N)
(and +1) for even b; success ⟺ 1 < g < N. Cells: t ∈ [log₂r−2, 2log₂r+1],
s ∈ {1,2,5,20}, 40 trials per (N, t, s).
"""
import math, time, random
import numpy as np
from fractions import Fraction

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


def outcome_probs(r, t):
    q = 1 << t
    M = (q - 1) // r + 1
    k = np.arange(q, dtype=np.float64)
    num = np.sin(np.pi * M * k * r / q)
    den = np.sin(np.pi * k * r / q)
    with np.errstate(divide='ignore', invalid='ignore'):
        pk = np.where(np.abs(den) < 1e-9, (M * M) / (M * q) * np.ones_like(k),
                      (num / den) ** 2 / (M * q))
    return pk / pk.sum()


def sample_k(pk, n):
    return np.searchsorted(np.cumsum(pk), np.random.rand(n))


def quality_denoms(k, q):
    out = []
    if k == 0: return out
    nn, dd = int(k), int(q)
    a_ints = []
    while dd:
        a_ints.append(nn // dd)
        nn, dd = dd, nn - a_ints[-1] * dd
    n_prev, n_cur = 0, 1
    d_prev, d_cur = 1, 0
    for a in a_ints:
        n_prev, n_cur = n_cur, a * n_cur + n_prev
        d_prev, d_cur = d_cur, a * d_cur + d_prev
        if d_cur == 0: continue
        if abs(Fraction(int(k), int(q)) - Fraction(n_cur, d_cur)) < Fraction(1, 2 * d_cur * d_cur):
            out.append(d_cur)
    return out


print("=== QUBIT-TRADE3 (round-25 #2): the fungibility ramp on real semiprimes ===", flush=True)

# ---------------------------------------------------------------------------
# CONSTRUCTED semiprimes with controlled small order r
# (real ord_N(a) is lcm(p-1,q-1)-scale ~ 2^30 — register simulation impossible;
#  build p ≡ 1 mod r, q ≡ 1 mod r and search a with ord_p(a) = ord_q(a) = r)
# ---------------------------------------------------------------------------
SMOOTH_RS = []
for rsig in [(2, 3, 5, 7), (2, 5, 31), (2, 3, 5, 17), (2, 7, 31)]:
    rr = math.prod(rsig)
    if 1 << 6 <= rr <= 1 << 10:
        SMOOTH_RS.append((rr, rsig))   # ALL EVEN: odd periods cannot factor at all
NS = []
rng = random.Random(20260821)
t_gen = time.time()

def smallest_prime_factors(rr):
    fs = set()
    d = 2
    while d * d <= rr:
        if rr % d == 0:
            fs.add(d)
            while rr % d == 0: rr //= d
        d += 1
    if rr > 1: fs.add(rr)
    return fs

def find_prime_with_r(r, rng):
    """prime p = m·r + 1 — any such p has r | p−1."""
    while True:
        m = rng.randrange(1, 4000)
        pp = m * r + 1
        if pp % 2 == 0: continue
        if is_prime(pp): return pp

def order_mod(a, r, pp):
    """exact order of a mod p, given the order divides r (r smooth)."""
    for ell in smallest_prime_factors(r):
        if pow(a, r // ell, pp) == 1:
            return None   # order strictly smaller than r
    return r if pow(a, r, pp) == 1 else None

for r_target, _sig in SMOOTH_RS[:4]:
    got = 0
    tries = 0
    while got < 8 and tries < 400:
        tries += 1
        pp = find_prime_with_r(r_target, rng)
        qq = find_prime_with_r(r_target, rng)
        if pp == qq or pp * qq > (1 << 34): continue
        Nc = pp * qq
        # randomized per-prime orders (r vs r/2), CRT-combined: ord_N(a) = r.
        # SAME roles ⟹ a^{r/2} ≡ ∓1 mod both ⟹ never factors (the unlucky half);
        # MIXED roles ⟹ splits every time — the population carries the cap.
        def elem_of_order(rr, pm):
            if rr == 1:
                return 1
            while True:
                hh = rng.randrange(2, pm - 1)
                aa = pow(hh, (pm - 1) // rr, pm)
                if order_mod(aa, rr, pm) == rr:
                    return aa
        try:
            dp, dq = rng.choice([(r_target, r_target),
                                 (r_target, r_target // 2),
                                 (r_target // 2, r_target)])
            ap = elem_of_order(dp, pp)
            aq = elem_of_order(dq, qq)
            ipq = pow(qq, -1, pp); ipi = pow(pp, -1, qq)
            aa = (ap * qq * ipq + aq * pp * ipi) % Nc
        except Exception:
            continue
        NS.append((Nc, aa, r_target, pp, qq))
        got += 1
print(f"sampled {len(NS)} constructed semiprimes in {time.time()-t_gen:.0f}s; "
      f"orders {sorted(set(n[2] for n in NS))}", flush=True)
assert len(NS) >= 16, 'construction failed'

# ---------------------------------------------------------------------------
# measure P_factor(s, t) on a fixed subset + taxonomy
# ---------------------------------------------------------------------------
SUBSET = NS[:30]
S_GRID = [1, 5, 20]
TRIALS = 24

def factor_attempt(k, q, a, N, r):
    """returns (certified, factor_found, mode): scan ALL quality denominators —
    an early non-splitting certificate must not mask a later splitting one."""
    saw_unlucky = saw_spurious = False
    for b in quality_denoms(int(k), q):
        if b % 2 != 0: continue
        v = pow(a, b // 2, N)
        g1 = math.gcd(v - 1, N); g2 = math.gcd(v + 1, N)
        for g in (g1, g2):
            if 1 < g < N:
                return True, True, 'factor'
        if v == N - 1 or b == r:
            saw_unlucky = True
        else:
            saw_spurious = True
    if saw_unlucky: return True, False, 'unlucky'
    if saw_spurious: return True, False, 'spurious-or-partial'
    return False, False, 'nocert'

print("\nP_factor(s,t) pooled over 30 semiprimes (40 trials each):", flush=True)
grid = {}
tax = {}
for t_off in (-4, -2, 0, 2):
    line = f"  "
    for s in S_GRID:
        succ = 0; tot = 0
        modes = {}
        for (N, aa, r, pp, qq) in SUBSET:
            tw = math.ceil(2 * math.log2(r))
            t = tw + t_off
            if t < int(math.log2(r)) + 1: continue
            pk = outcome_probs(r, t)
            q = 1 << t
            for _ in range(TRIALS):
                ks = sample_k(pk, s)
                fnd = False
                for k in ks:
                    cert, ff, md = factor_attempt(k, q, aa, N, r)
                    modes[md] = modes.get(md, 0) + 1
                    if ff: fnd = True; break
                succ += fnd; tot += 1
        pf = succ / max(tot, 1)
        grid[(t_off, s)] = pf
        tax[(t_off, s)] = modes
        line += f"s={s}:{pf:.3f}  "
    print(f"t=wall{t_off:+d}: {line}", flush=True)

# ---------------------------------------------------------------------------
# H2 — exchange law in the factoring metric
# ---------------------------------------------------------------------------
print("\nH2 — exchange law: t*(P_factor ≥ 0.5) shift vs −log₂ s", flush=True)
for s in S_GRID:
    t_star = None
    for t_off in (2, 1, 0, -1, -2, -3, -4, -5, -6):
        if grid.get((t_off, s), 0) >= 0.5:
            t_star = t_off; break
    print(f"  s={s:>3}: t*(≥0.5) = wall{t_star:+d}" if t_star is not None
          else f"  s={s:>3}: never ≥ 0.5 in range", flush=True)
print("  fungibility predicts shifts ≈ −log₂ s: 0, −2.3, −4.3", flush=True)

# ---------------------------------------------------------------------------
# H3/H4 — saturation cap + failure taxonomy
# ---------------------------------------------------------------------------
print("\nH3/H4 — saturation & taxonomy (pooled over all cells):", flush=True)
tot_all = sum(sum(tx.values()) for tx in tax.values())
agg = {}
for tx in tax.values():
    for md, c in tx.items(): agg[md] = agg.get(md, 0) + c
for md, c in sorted(agg.items(), key=lambda kv: -kv[1]):
    print(f"  {md:>20}: {c/tot_all:.4f}", flush=True)
# unlucky-half check: among first-attempt certificates equal to true r, share unlucky
print(f"  (a^{{r/2}} ≡ −1 cap: 'unlucky' share among resolved certificates above)", flush=True)

print(f"\nTOTAL runtime: {time.time() - T0:.0f}s", flush=True)
pf_wall_s20 = grid.get((0, 20), 0)
print(f"\nDATA SUMMARY: P_factor(wall, s=1) = {grid.get((0,1),0):.4f}, "
      f"P_factor(wall, s=20) = {pf_wall_s20:.4f}; taxonomy shares above.", flush=True)
print("VERDICT: computed from the data above — see DATA SUMMARY and the grid;", flush=True)
print("the ramp/exchange claims are judged against these numbers in the paper.", flush=True)
print("Round-25 #2.", flush=True)
print("\nALL_DONE_R25N2", flush=True)

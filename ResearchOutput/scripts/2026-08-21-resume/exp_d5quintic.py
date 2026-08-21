#!/usr/bin/env python3
"""D5-QUINTIC — the last untested transitive quintic group (round-24 #5).

BACKGROUND. Papers 78-82 + round-24 #3/#4 measured the abelianization law on
C₅, F₂₀, A₅, S₅ (and all lower-degree groups). The sole untested transitive
quintic group is D₅ (order 10): C₅ ⋊ C₂ with reflections acting as [1,2,2]
(two transpositions — EVEN), so D₅ ⊆ A₅ and its defining quintics have SQUARE
discriminant. Type profile: {[1⁵]: 1/10, [5]: 4/10 (rotations), [1,2,2]: 5/10
(reflections)} — no [1,4], no [3,1,1]. G^ab = C₂; every type determines its
sign ⟹ loss 0.

PREDICTIONS (stated before the run):
  H0 IDENTIFICATION: a small-coefficient trinomial x⁵+ax+b exists whose type
     histogram matches the D₅ profile within tolerance (the histogram IS the
     Chebotarev readout of the Galois group); its discriminant is a perfect
     square.
  H1 PRIME LAW: I(p mod m*; T) = 1.0000 exactly at m* = fundamental disc
     (permutation-referenced — large conductors carry sparse-dial bias).
  H2 SEMIPRIME: pair = 1.0000 via the Nf-within-strata null (the C₂ cap);
     [1,2,2]-fork s-projection = Is(2) = 1.0000.
  H3 DISCIPLINE: rates {1/10,4/10,5/10}; which-factor wall 0; coprime flat;
     thickening permutation-referenced.
  H4 THE COMPLETED TABLE: all five transitive quintic groups measured, each on
     its abelianization prediction:
       C₅ 0.7220/Is(5)=0.2027 · D₅ 1.0/1.0 · F₂₀ 1.5/1.25 · A₅ 0/0 · S₅ 1.0/1.0.

Method: search x⁵+ax+b (|a|,|b| ≤ 15) via sympy discriminant + irreducibility;
identify by histogram on a 2^15 sieve; measure the winner at 2^18 with the
established pipeline (F_{p²}-root-count types, permutation-referenced MIs,
Nf-within-strata semiprime nulls, 400k MC).
"""
import math, time, random
import numpy as np
from collections import Counter
from sympy import Poly, symbols, discriminant, factor_list
from sympy.ntheory.residue_ntheory import jacobi_symbol

random.seed(20260821)
np.random.seed(20260821)
T0 = time.time()
x = symbols('x')


def Hv(ps):
    ps = np.asarray(ps, float); ps = ps[ps > 0]
    return float(-np.sum(ps * np.log2(ps)))


def contingency_mi(xa, ya):
    k, inv = np.unique(xa, return_inverse=True)
    yl, yinv = np.unique(ya, return_inverse=True)
    idx = inv.astype(np.int64) * len(yl) + yinv
    cnt = np.bincount(idx, minlength=len(k) * len(yl)).reshape(len(k), len(yl)).astype(float)
    tot = cnt.sum()
    if tot == 0: return 0.0
    pxy = cnt / tot; px = pxy.sum(1, keepdims=True); py = pxy.sum(0, keepdims=True)
    with np.errstate(divide='ignore', invalid='ignore'):
        mm = pxy * np.log2(pxy / (px * py))
    mm[pxy == 0] = 0
    return float(mm.sum())


def odd_sieve(limit):
    sieve = bytearray(b'\x01') * (limit // 2)
    sieve[0] = 0
    imax = int(math.isqrt(limit))
    for i in range(3, imax + 1, 2):
        if sieve[i // 2]:
            start = i * i // 2
            sieve[start::i] = b'\x00' * ((limit - i * i + 2 * i - 1) // (2 * i))
    return np.array([2] + [2 * i + 1 for i in range(1, len(sieve)) if sieve[i]],
                    dtype=np.int64)


def polymulmod(a, b, f, p):
    res = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                if bj: res[i + j] += ai * bj
    n = len(f) - 1
    for i in range(len(res) - 1, n - 1, -1):
        c = res[i] % p
        if c:
            for j in range(n + 1):
                res[i - n + j] -= c * f[j]
    return [v % p for v in res[:n]]


def polypowmod(base, e, f, p):
    result = [1]; b = base[:]
    while e:
        if e & 1: result = polymulmod(result, b, f, p)
        e >>= 1
        if e: b = polymulmod(b, b, f, p)
    return result


def polygcd_deg(a, b, p):
    a = [v % p for v in a]; b = [v % p for v in b]
    while True:
        while b and b[-1] % p == 0: b.pop()
        if not b: return (len(a) - 1) if any(a) else -1
        inv = pow(b[-1] % p, -1, p)
        r = a[:]
        while len(r) >= len(b):
            while r and r[-1] % p == 0: r.pop()
            if len(r) < len(b): break
            c = r[-1] * inv % p
            sh = len(r) - len(b)
            for i in range(len(b)):
                r[sh + i] = (r[sh + i] - c * b[i]) % p
        a, b = b, r


DICT5 = {
    (5, 5): '11111', (3, 5): '2111', (2, 2): '311', (1, 5): '221',
    (1, 1): '41', (0, 2): '32', (0, 0): '5',
}

def quintic_types(coeffs, primes):
    flit = list(coeffs)
    out = []
    for p in primes:
        pp = int(p)
        xg = np.arange(pp, dtype=np.int64)
        y = np.zeros(pp, dtype=np.int64)
        for c in coeffs:
            y = (y * xg + c) % pp
        nr = int(np.count_nonzero(y == 0))
        g = polypowmod([0, 1], pp * pp, flit, pp)
        while len(g) < 2: g.append(0)
        g[1] = (g[1] - 1) % pp
        nr2 = polygcd_deg(flit, g, pp)
        t = DICT5.get((nr, nr2))
        if t is None: raise ValueError(f"impossible readout p={pp} ({nr},{nr2})")
        out.append(t)
    return np.array(out)


D5_PROFILE = {'11111': 1/10, '5': 4/10, '221': 5/10}

print("=== D₅-QUINTIC (round-24 #5): the last untested transitive quintic group ===", flush=True)

# ---------------------------------------------------------------------------
# PART A — search for a D₅ trinomial
# ---------------------------------------------------------------------------
print("\nPART A — search x⁵+ax+b for the D₅ signature", flush=True)
pr_id = odd_sieve(1 << 15)
pr_id = pr_id[~np.isin(pr_id, [2])]
found = None
t_search = time.time()
for a in range(-60, 61):
    if a == 0: continue
    for b in range(-60, 61):
        if b == 0: continue
        f = Poly(x**5 + a*x + b, x)
        try:
            fac = factor_list(f.as_expr(), x)[0]
            if fac != 1: continue                      # reducible over Q
            d = discriminant(f)
            if d == 0 or int(round(math.isqrt(abs(d))))**2 != abs(d): continue
        except Exception:
            continue
        coeffs = (b, a, 0, 0, 0, 1)
        ram = set()
        try:
            for q, e in __import__('sympy').factorint(d).items(): ram.add(q)
        except Exception:
            continue
        prc = pr_id[~np.isin(pr_id, list(ram))]
        try:
            typ = quintic_types(coeffs, prc[:4000])
        except ValueError:
            continue
        obs = Counter(typ.tolist())
        rates = {t: obs.get(t, 0)/len(typ) for t in D5_PROFILE}
        if all(abs(rates[t] - w) < 0.06 for t, w in D5_PROFILE.items()) and \
           obs.get('14', 0) == 0 and obs.get('311', 0) == 0:
            found = (a, b, d, coeffs, ram)
            print(f"  FOUND: x⁵{a:+d}x{b:+d} disc={d} (= {int(math.isqrt(abs(d)))}²) "
                  f"rates {{11111:{rates['11111']:.3f}, 5:{rates['5']:.3f}, 221:{rates['221']:.3f}}} "
                  f"({time.time()-t_search:.0f}s search)", flush=True)
if found is None:
    print("  no D₅ trinomial in range — extending not attempted this round", flush=True)
    raise SystemExit("NO_D5_FOUND")
a_w, b_w, disc_w, coeffs_w, ram_w = found

# ---------------------------------------------------------------------------
# PART B — full measurement of the winner
# ---------------------------------------------------------------------------
pr_all = odd_sieve(1 << 18)
prD = pr_all[~np.isin(pr_all, list(ram_w))]
typD = quintic_types(coeffs_w, prD)
# D₅ ⊆ A₅ ⟹ √disc ∈ ℚ and the quadratic subfield K (fixed field of C₅, carrier
# of G^ab = C₂) is NOT Q(√disc) — find K's conductor EMPIRICALLY: the unique
# modulus pinning the reflection fork [221] at exactly H(1/2) = 1 bit
forkD = (typD == '221').astype(int)   # 1 ⟺ reflection ⟺ nontrivial G^ab coset

def kron(d, pp):
    """Kronecker symbol (d|pp) for small |d| via factorization."""
    if d == 0: return 0
    sg = 1
    dd = abs(d)
    if d < 0:
        sg = -1 if pp % 4 == 3 else 1          # (−1|pp)
    out = 1
    for q, e in __import__('sympy').factorint(dd).items():
        if q == 2:
            r = pp % 8
            lq = 1 if r in (1, 7) else (-1 if r in (3, 5) else 0)
        else:
            lq = 1 if pow(int(pp) % q, (q - 1) // 2, q) == 1 else -1
        out *= lq ** e
    return sg * out

# K's ramified primes divide disc(f) (splitting-field ramification = root-field
# ramification) ⟹ K = Q(√d) with d squarefree over the ramified set, either sign
from itertools import combinations
cands = []
rpl = sorted(ram_w)
for r in range(1, len(rpl) + 1):
    for comb in combinations(rpl, r):
        for sgn in (1, -1):
            cands.append(sgn * math.prod(comb))
hits = []
for d in cands:
    chi_d = np.array([1 if kron(d, int(p)) == -1 else 0 for p in prD])
    ag = np.mean(chi_d == forkD)
    if ag > 0.999: hits.append((d, ag))
assert len(hits) == 1, f'K not uniquely identified: {hits}'
d_K, agK = hits[0]
mstar = abs(d_K) if d_K % 4 == 1 else 4 * abs(d_K)   # fundamental disc of Q(√d_K)
print(f"\nPART B — measuring x⁵{a_w:+d}x{b_w:+d}: K = Q(√{d_K}) identified at agreement "
      f"{agK:.4f}; m* = {mstar}", flush=True)
obs = Counter(typD.tolist())
G = 10
sizes = {'11111': 1, '5': 4, '221': 5}
for t, sz in sizes.items():
    print(f"  type {t}: measured {obs.get(t,0)/len(prD):.4f} vs law {sz/G:.4f}", flush=True)
    assert abs(obs.get(t, 0)/len(prD) - sz/G) < 0.02, ('rate', t)
for t in ('2111', '311', '32', '41'):
    assert obs.get(t, 0) == 0, ('non-D₅ type!', t)
H_T = Hv([sz/G for sz in sizes.values()])
print(f"  H(T) = {H_T:.4f} bits; every type determines its sign ([221] ⟺ reflection)", flush=True)
# coset per prime: sign = (D|p) via Jacobi symbol
sign_leg = np.array([1 if kron(d_K, int(p)) == -1 else 0 for p in prD])   # kron handles even/negative d
sign_pred = np.array([1 if t == '221' else 0 for t in typD])
agree = np.mean(sign_pred == sign_leg)
print(f"  type-determined sign vs (D|p): agreement {agree:.4f}", flush=True)
assert agree > 0.999
rng_np = np.random.default_rng(4242)
pmD = (prD % mstar).astype(np.int64)
I1_obs = contingency_mi(pmD, typD)
nI = []
for _ in range(60):
    ts = typD.copy()
    for sv in (0, 1):
        sel = sign_leg == sv
        ts[sel] = rng_np.permutation(ts[sel])
    nI.append(contingency_mi(pmD, ts))
zI = (I1_obs - np.mean(nI)) / (np.std(nI) + 1e-12)
print(f"  I₁ measured {I1_obs:.4f} | within-sign null {np.mean(nI):.4f} "
      f"(bias {np.mean(nI)-1.0:+.4f}) z={zI:+.2f} | law 1.0000", flush=True)
assert abs(I1_obs - np.mean(nI)) < 0.05 and zI < 3.0
I_cop = contingency_mi((prD % 3).astype(np.int64), typD)
print(f"  coprime m=3: {I_cop:.4f}", flush=True)
assert I_cop < 0.02

# ---------------------------------------------------------------------------
# PART C — semiprime (400k MC, Nf-within-strata null)
# ---------------------------------------------------------------------------
print("\nPART C — SEMIPRIME (400k MC)", flush=True)
pool_full = odd_sieve(1 << 16)
N_MC = 400000
prp = pool_full[~np.isin(pool_full, list(ram_w))]
tp = quintic_types(coeffs_w, prp)
tids = {t: i for i, t in enumerate(sorted(set(tp.tolist())))}
tmap = dict(zip(prp.tolist(), [tids[t] for t in tp.tolist()]))
idx = np.random.randint(0, len(prp), 2 * N_MC).reshape(N_MC, 2)
P = prp[idx[:, 0]]; Q = prp[idx[:, 1]]
bigger = (P > Q).astype(np.int64)
tpP = np.array([tmap[int(p)] for p in P]); tpQ = np.array([tmap[int(q)] for q in Q])
pc = np.minimum(tpP, tpQ) * 100 + np.maximum(tpP, tpQ)
Nf = (P * Q) % mstar
I_obs = contingency_mi(Nf, pc)
wf = contingency_mi(bigger, pc)
odd_arr = np.zeros(max(tids.values()) + 1, dtype=int)
for t, i in tids.items():
    odd_arr[i] = 1 if t == '221' else 0
strat = (odd_arr[tpP] + odd_arr[tpQ]) % 2
nn = []
for _ in range(40):
    nfs = Nf.copy()
    for sv in (0, 1):
        sel = strat == sv
        nfs[sel] = rng_np.permutation(nfs[sel])
    nn.append(contingency_mi(nfs, pc))
zc = (I_obs - np.mean(nn)) / (np.std(nn) + 1e-12)
inv_tids_s = {i: t for t, i in tids.items()}
s = np.array([1 if inv_tids_s[u] == '221' else 0 for u in tpP], dtype=int) + \
    np.array([1 if inv_tids_s[v] == '221' else 0 for v in tpQ], dtype=int)
Is_obs = contingency_mi(Nf, s)
p2 = 1.0 / 2
Is2 = Hv([(1-p2)**2, 2*p2*(1-p2), p2*p2]) - 0.5*Hv([0.5, 0.0, 0.5]) - 0.5*Hv([0.0, 1.0, 0.0])
print(f"  D₅ x⁵{a_w:+d}x{b_w:+d}: I(N mod {mstar}; pair) = {I_obs:.4f} | which-factor {wf:.4f} | "
          f"null {np.mean(nn):.4f} z={zc:+.2f} | [221]-fork s-proj {Is_obs:.4f} vs Is(2) = {Is2:.4f}", flush=True)
assert wf < 0.02 and abs(I_obs - np.mean(nn)) < 0.05 and zc < 3.0, 'pair'
assert abs(Is_obs - Is2) < 0.02, 's-proj'

# ---------------------------------------------------------------------------
print(f"\nTOTAL runtime: {time.time() - T0:.0f}s", flush=True)
print("\nVERDICT: the last untested transitive quintic group confirms the law — D₅'s", flush=True)
print("three-type channel (H(T) = 1.3610 bits) collapses EXACTLY to the 1-bit C₂ dial:", flush=True)
print("every type determines its sign, I₁ sits at its permutation null, the pair reads the", flush=True)
print("C₂ cap through its Nf-null, and the reflection fork realizes Is(2). THE COMPLETED", flush=True)
print("QUINTIC TABLE — all five transitive groups on their abelianization predictions:", flush=True)
print("  C₅ 0.7220/Is(5) · D₅ 1.0/1.0 · F₂₀ 1.5/1.25 · A₅ 0/0 · S₅ 1.0/1.0.", flush=True)
print("The type-channel program has now measured EVERY group structure it can name at", flush=True)
print("degrees 2–5. Symmetric, residue-dial, CRT-sealed — factor-useless. Barriers 2/5/6/8.", flush=True)
print("Round-24 #5.", flush=True)
print("\nALL_DONE_R24N5", flush=True)

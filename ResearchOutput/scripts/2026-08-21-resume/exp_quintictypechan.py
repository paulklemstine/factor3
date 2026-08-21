#!/usr/bin/env python3
"""QUINTIC-TYPE-CHANNEL — the abelianization law at degree 5: F₂₀ x⁵−2, the
first C₄-abelianization object (round-24 #3).

BACKGROUND. Paper 80 closed the type-channel program for S₃/S₄/A₄/D₄/V₄/C₄:
I(p mod m*; T) = I(T; coset) = H(T) − H(T|coset) EXACTLY, semiprime pair law
verbatim. The untested non-abelian groups with interesting abelianizations are
the transitive quintic groups. This round tests the FROBENIUS GROUP F₂₀ =
AGL(1,5) (order 20) via its simplest defining polynomial x⁵−2 — the FIRST
object of the program whose abelianization is C₄ (a QUATERNARY dial).

Structure of x⁵−2 mod p (p ∤ 10): Frob_p acts on the 5 roots ζ₅^k·2^{1/5} as
the affine map k ↦ p·k + c on Z/5 — multiplier a = p mod 5, translation c ≠ 0
iff 2 is not a 5th power mod p (only possible when p ≡ 1 mod 5). Types:
  p ≡ 1 mod 5, 2 is a 5th power   → identity        [1,1,1,1,1]  (nr,nr₂)=(5,5)
  p ≡ 1 mod 5, otherwise          → translation     [5]          (0,0)
  p ≡ 2 or 3 mod 5 (order-4 mult) → one fix + 4-cyc [1,4]        (1,1)
  p ≡ 4 mod 5 (multiplier −1)     → one fix + 2+2   [1,2,2]      (1,3)
Class sizes: e(1), translations(4), a=2-family(5), a=3-family(5), a=4-family(5).
G^ab = C₄ (the quartic character mod 5); coset values v: 1→0, 2→1, 4→2, 3→3.

PREDICTIONS (stated before the run):
  H1 PRIME LAW: I(p mod 5; T) = I(T; coset) = 1.5000 EXACTLY.
     H(T) = H(1/20, 4/20, 10/20, 5/20) = 1.6805; H(T|coset) = (1/4)H(1/5,4/5)
     = 0.1805; I₁ = 1.5000. Cross-check via loss form: dial H(coset) = 2.0,
     E[H(coset|T)] = P([1,4])·H({2,3}|T) = (1/2)(1) = 0.5 → I₁ = 1.5 ✓.
     The [1,4] type MERGES the two order-4 cosets {2,3} — loss 0.5 bit.
  H2 SEMIPRIME LAW: I(N mod 5; pair) = class-level enumeration value = 1.2500
     EXACTLY (H(pair) = 2.7160, H(cond) = 1.4660); the [1,2,2]-fork is
     COSET-DETERMINED (⟺ p ≡ 4 mod 5, rate 1/4, order-4 character)
     ⟹ s-projection = Is(4) = 0.2947 exactly.
  H3 C₅ CONTROL (Q(ζ₁₁)+, conductor 11, paper 76/78/79 lineage): T ∈ {1,5}
     rates {1/5, 4/5} (ord₁₁(p)/gcd(ord,2)); I₁ = H(1/5,4/5) = 0.7220;
     pair = Is(5) = 0.2027 (paper-79 f=11 entry reproduced).
  H4 DISCIPLINE: within-coset flatness + m*²-thickening at permutation nulls;
     coprime flat; which-factor walls 0.

Method: quintic types via (nr, nr₂) = (#F_p-roots, #F_{p²}-roots) from
x^(p²) mod f + gcd — dictionary (5,5)→11111, (1,1)→14, (1,5)→122, (0,0)→5
(unique). Sieves 2^18 / 2^16 pools, ramified primes excluded, 400k MC.
"""
import math, time, random
import numpy as np
from collections import Counter

random.seed(20260821)
np.random.seed(20260821)
T0 = time.time()


def Hv(ps):
    ps = np.asarray(ps, float); ps = ps[ps > 0]
    return float(-np.sum(ps * np.log2(ps)))


def contingency_mi(x, y):
    k, inv = np.unique(x, return_inverse=True)
    yl, yinv = np.unique(y, return_inverse=True)
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
    """little-endian (index = degree) poly mulmod, f monic."""
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


def quintic_types(coeffs, primes):
    """type from (nr, nr₂): (5,5)→11111, (1,1)→14, (1,5)→122, (0,0)→5."""
    flit = list(coeffs)                            # const-first IS little-endian
    out = []
    for p in primes:
        pp = int(p)
        x = np.arange(pp, dtype=np.int64)
        y = np.zeros(pp, dtype=np.int64)
        for c in coeffs:
            y = (y * x + c) % pp
        nr = int(np.count_nonzero(y == 0))
        g = polypowmod([0, 1], pp * pp, flit, pp)
        while len(g) < 2: g.append(0)
        g[1] = (g[1] - 1) % pp
        nr2 = polygcd_deg(flit, g, pp)
        if (nr, nr2) == (5, 5):   out.append('11111')
        elif (nr, nr2) == (1, 1): out.append('14')
        elif (nr, nr2) == (1, 5): out.append('122')   # linear + two quadratic pairs (all 4 extra roots in F_{p²})
        elif (nr, nr2) == (0, 0): out.append('5')
        else: raise ValueError(f"impossible quintic readout p={pp} ({nr},{nr2})")
    return np.array(out)


def prime_law(classes):
    G = sum(s for s, _, _ in classes)
    jt = Counter()
    for s, cos, t in classes:
        jt[(t, cos)] += s / G
    tdist = Counter(); cdist = Counter()
    for (t, c), w in jt.items():
        tdist[t] += w; cdist[c] += w
    H_T, H_C = Hv(list(tdist.values())), Hv(list(cdist.values()))
    H_joint = Hv(list(jt.values()))
    I1 = H_T + H_C - H_joint
    return H_T, H_C, H_T - I1, I1, H_C - I1


def pair_law(classes, mstar, chi_of_residue, prod):
    """exact unordered type-pair channel by class-level enumeration.
    chi_of_residue: residue -> coset label; prod: (c1,c2) -> combined label."""
    G = sum(s for s, _, _ in classes)
    units = [a for a in range(1, mstar) if math.gcd(a, mstar) == 1]
    phi = len(units)
    pu = Counter(); pd = Counter()
    for s1, c1, t1 in classes:
        for s2, c2, t2 in classes:
            pu[tuple(sorted((t1, t2)))] += s1 * s2 / (G * G)
            pd[tuple(sorted((c1, c2)))] += s1 * s2 / (G * G)
    H_pair = Hv(list(pu.values()))
    H_cond = 0.0; dial_cond = 0.0
    for cN in units:
        target = prod(chi_of_residue(cN))
        dist = Counter(); distd = Counter(); tot = 0.0
        for s1, c1, t1 in classes:
            for s2, c2, t2 in classes:
                if prod(c1, c2) == target:
                    dist[tuple(sorted((t1, t2)))] += s1 * s2
                    distd[tuple(sorted((c1, c2)))] += s1 * s2
                    tot += s1 * s2
        H_cond += (1.0 / phi) * Hv([v / tot for v in dist.values()])
        dial_cond += (1.0 / phi) * Hv([v / tot for v in distd.values()])
    return H_pair, H_cond, H_pair - H_cond, Hv(list(pd.values())) - dial_cond


def Is_law(n):
    p = 1.0 / n
    Hb_ = Hv([(1 - p) ** 2, 2 * p * (1 - p), p * p])
    H1 = Hv([(n - 1) / n, 0.0, 1 / n]); H2 = Hv([(n - 2) / n, 2 / n, 0.0])
    return Hb_ - (1 / n) * H1 - ((n - 1) / n) * H2


print("=== QUINTIC-TYPE-CHANNEL (round-24 #3): F₂₀ x⁵−2 — the first C₄ abelianization ===", flush=True)

# ---------------------------------------------------------------------------
# PART A — prime level: F₂₀ x⁵−2 and the C₅ control
# ---------------------------------------------------------------------------
pr_all = odd_sieve(1 << 18)

# --- F₂₀ x⁵−2 ---
print("\nPART A1 — F₂₀ x⁵−2 (disc 2⁴·5⁵, G^ab = C₄, conductor 5)", flush=True)
prF = pr_all[(pr_all % 5 != 0) & (pr_all % 2 != 0)]
typF = quintic_types((-2, 0, 0, 0, 0, 1), prF)
G20 = 20
classes_F = [(1, 0, '11111'), (4, 0, '5'), (5, 1, '14'), (5, 3, '14'), (5, 2, '122')]
# coset = C₄ valuation of the multiplier: a=3 = 2³ → 3, a=4 = 2² → 2 (V5 map)
law_rates = {}
for s, _, t in classes_F:
    law_rates[t] = law_rates.get(t, 0.0) + s / G20
obsF = Counter(typF.tolist())
for t, w in law_rates.items():
    print(f"  type {t}: measured {obsF.get(t,0)/len(prF):.4f} vs law {w:.4f}", flush=True)
    assert abs(obsF.get(t, 0) / len(prF) - w) < 0.02, ('rate', t)
# coset per prime: additive C₄ valuation of p mod 5 (1→0, 2→1, 4→2, 3→3)
V5 = {1: 0, 2: 1, 4: 2, 3: 3}
cosF = np.array([V5[int(p % 5)] for p in prF], dtype=np.int64)
pmF = (prF % 5).astype(np.int64)
I1_obs = contingency_mi(pmF, typF)
H_T, H_C, H_TgC, I1_law, loss = prime_law(classes_F)
print(f"  H(T)={H_T:.4f} (pred 1.6805) | I₁ measured {I1_obs:.4f} vs law {I1_law:.4f} "
      f"(PRED 1.5000) | dial H(coset)={H_C:.4f} loss={loss:.4f}", flush=True)
assert abs(H_T - 1.6805) < 0.02 and abs(I1_law - 1.5) < 1e-6 and abs(I1_obs - 1.5) < 0.02
# within-coset flatness (only the p≡1 coset has residual structure: {11111,5})
mask1 = cosF == 0
flat = contingency_mi(pmF[mask1], typF[mask1])
rng_np = np.random.default_rng(999)
nulls = []
tf = typF.copy()
for _ in range(200):
    ts = tf[mask1]
    ts = rng_np.permutation(ts)
    t2 = tf.copy(); t2[mask1] = ts
    nulls.append(contingency_mi(pmF[mask1], t2[mask1]))
zflat = (flat - np.mean(nulls)) / (np.std(nulls) + 1e-12)
print(f"  within-coset flatness (p≡1 stratum): I={flat:.5f} null {np.mean(nulls):.5f} z={zflat:+.2f}", flush=True)
assert zflat < 3.0
# thickening at 25 (permutation-referenced)
pm25 = (prF % 25).astype(np.int64)
obs25 = contingency_mi(pm25, typF)
n25 = []
for _ in range(100):
    ts = typF.copy()
    sel = mask1
    ts[sel] = rng_np.permutation(ts[sel])
    n25.append(contingency_mi(pm25, ts))
z25 = (obs25 - np.mean(n25)) / (np.std(n25) + 1e-12)
print(f"  thickening m*=25: I={obs25:.4f} null {np.mean(n25):.4f} z={z25:+.2f}", flush=True)
assert abs(obs25 - np.mean(n25)) < 0.05 and z25 < 3.0
I_cop = contingency_mi((prF % 3).astype(np.int64), typF)
print(f"  coprime m=3: {I_cop:.4f}", flush=True)
assert I_cop < 0.02

# --- C₅ control: Q(ζ₁₁)+ ---
print("\nPART A2 — C₅ control Q(ζ₁₁)⁺ (conductor 11, paper 79 lineage)", flush=True)
def ordm(a, m):
    x, o = a % m, 1
    while x != 1:
        x = x * a % m
        o += 1
    return o
units11 = [a for a in range(1, 11) if math.gcd(a, 11) == 1]
t_c5 = {a: (1 if ordm(a, 11) in (1, 2) else 5) for a in units11}
classes_C = [(1, a, t_c5[a]) for a in units11]   # coset = residue itself (int)
prC = pr_all[pr_all != 11]
typC = np.array([t_c5[int(a)] for a in (prC % 11)])
I1_C = contingency_mi((prC % 11).astype(np.int64), typC)
H_T5, H_C5, _, I1_C_law, loss5 = prime_law(classes_C)
print(f"  H(T)={H_T5:.4f} (pred H(1/5,4/5)=0.7220) | I₁ measured {I1_C:.4f} vs law {I1_C_law:.4f} "
      f"| dial log₂5={H_C5:.4f} loss={loss5:.4f}", flush=True)
assert abs(H_T5 - 0.72193) < 0.01 and abs(I1_C - 0.7220) < 0.02

# ---------------------------------------------------------------------------
# PART B — semiprime level (400k MC, unramified pools)
# ---------------------------------------------------------------------------
print("\nPART B — SEMIPRIME pair channels (400k MC)", flush=True)
pool_full = odd_sieve(1 << 16)
N_MC = 400000

def run_mc(name, coeffs_or_map, ram, mstar, classes, chi_fn, prod_fn, pinfork, pin_n, readout):
    prp = pool_full[~np.isin(pool_full, ram)]
    if readout == 'poly':
        tp = quintic_types(coeffs_or_map, prp)
    else:
        tp = np.array([coeffs_or_map[int(p % mstar)] for p in prp])
    tids = {t: i for i, t in enumerate(sorted(set(tp.tolist())))}
    tmap = dict(zip(prp.tolist(), [tids[t] for t in tp.tolist()]))
    idx = np.random.randint(0, len(prp), 2 * N_MC).reshape(N_MC, 2)
    P = prp[idx[:, 0]]; Q = prp[idx[:, 1]]
    bigger = (P > Q).astype(np.int64)
    tpP = np.array([tmap[int(p)] for p in P]); tpQ = np.array([tmap[int(q)] for q in Q])
    pc = np.minimum(tpP, tpQ) * 100 + np.maximum(tpP, tpQ)
    Nf = (P * Q) % mstar
    I_obs = contingency_mi(Nf, pc)
    Hp, Hc, Ip, dial_pair = pair_law(classes, mstar, chi_fn, prod_fn)
    wf = contingency_mi(bigger, pc)
    cop = 3 if math.gcd(3, mstar) == 1 else 7
    I_co = contingency_mi((P * Q) % cop, pc)
    inv_tids = {i: t for t, i in tids.items()}
    s = np.array([pinfork(inv_tids[u]) + pinfork(inv_tids[v]) for u, v in zip(tpP, tpQ)], dtype=int)
    Is_obs = contingency_mi(Nf, s)
    print(f"  {name}: I(N mod {mstar}; pair) = {I_obs:.4f} (law {Ip:.4f}) | dial-pair {dial_pair:.4f} | "
          f"which-factor {wf:.4f} | coprime {I_co:.4f} | pinned-fork s-proj {Is_obs:.4f} "
          f"vs Is({pin_n}) = {Is_law(pin_n):.4f}", flush=True)
    assert abs(I_obs - Ip) < 0.02, (name, 'pair')
    assert wf < 0.02 and I_co < 0.02, (name, 'walls')
    assert abs(Is_obs - Is_law(pin_n)) < 0.02, (name, 's-proj')
    return Ip

# F₂₀: cosets are C₄-additive valuations; product = addition mod 4
chiF = lambda r: V5[int(r) % 5]
prodF = lambda *cs: ((sum(cs)) % 4,)
IpF = run_mc("F₂₀ x⁵−2", (-2, 0, 0, 0, 0, 1), [2, 5], 5, classes_F, chiF, prodF,
             lambda t: t == '122', 4, 'poly')
print(f"  pre-stated: F₂₀ [1,2,2]-fork is coset-determined ⟹ Is(4) check above; "
      f"pair law = {IpF:.6f}", flush=True)

# C₅: cosets are residues mod 11; product = multiplication mod 11
chiC = lambda r: int(r) % 11
prodC = lambda *cs: ((math.prod(cs)) % 11,)
IpC = run_mc("C₅ Q(ζ₁₁)⁺", t_c5, [11], 11, classes_C, chiC, prodC,
             lambda t: t == 1, 5, 'map')
print(f"  pre-stated: C₅ pair law = {IpC:.6f} (Is(5) = {Is_law(5):.6f}, paper-79 f=11)", flush=True)
assert abs(IpC - Is_law(5)) < 1e-6

print(f"\nTOTAL runtime: {time.time() - T0:.0f}s", flush=True)
print("\nVERDICT: the abelianization law holds at degree 5 on the FROBENIUS group F₂₀ —", flush=True)
print("the program's first C₄-abelianization object: I(p mod 5; T) = 1.5000 EXACTLY (H(T) =", flush=True)
print("1.6805 collapses through the quartic dial; the [1,4] type merges the two order-4 cosets,", flush=True)
print("loss exactly 0.5 bit); semiprime pair law verbatim with the [1,2,2]-fork realizing", flush=True)
print("Is(4) as an ORDER-4 pinned fork on a non-abelian field. C₅ control reproduces the", flush=True)
print("abelian line (pair = Is(5), paper 79). The type-channel law now spans degrees 2–5 and", flush=True)
print("abelianizations C₂/C₃/C₄/C₂×C₂/Cₙ. Symmetric, residue-dial, CRT-sealed — factor-useless.", flush=True)
print("Barriers 2/5/6/8. Round-24 #3.", flush=True)
print("\nALL_DONE_R24N3", flush=True)

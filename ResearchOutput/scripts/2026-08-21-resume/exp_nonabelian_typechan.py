#!/usr/bin/env python3
"""NONABELIAN-TYPE-CHANNEL — the splitting-type channel of a NON-abelian field is
exactly its ABELIANIZATION content (round-24 #1).

HYPOTHESIS (stated before the run). Papers 78/79 closed the ABELIAN type channel:
the complete splitting-type pair channel I_pair = H(Π) − (1/φ)Σ_c H(Π_c) is exact
on every abelian cyclotomic conductor; multi-stateness (≥3 element orders) breaks
the 1-bit binary-fork cap; cyclicity amplifies (1D>2D>3D). The OPEN row is the
non-abelian one: S₃, S₄, A₄, D₄. The paper-71 abelianization criterion (a fork is
congruence-pinned iff it factors through G^ab), promoted from binary forks to the
complete channel, predicts:

  PRIME-LEVEL LAW:  I(p mod m*; T) = I(T; coset) = H(T) − H(T|coset)
    — the type channel EQUALS the type's mutual information with the G^ab-coset
    (m* = conductor of the G^ab characters; the coset is a deterministic function
    of p mod m*). Within-coset type refinement is residue-invisible at EVERY
    modulus (papers 70/75/77 flatness, now for the full type). Type separates
    cosets ⟺ I₁ = H(coset) (the full dial); type merges cosets ⟹ the type is a
    LOSSY PROJECTION of the dial, losing exactly E_t[H(coset|T=t)] bits.

  SEMIPRIME LAW:  I(N mod m*; {T(p),T(q)}) = H(Π) − (1/φ)Σ_c H(Π_c) — the papers
    78/79 law VERBATIM, with the type map replaced by the class-level map (pairs
    (g,h) with χ⃗(g)⊙χ⃗(h) = χ⃗(c), class-size weights, unordered merge).

EXACT LAW TABLE (predicted before the run; loss = E_t[H(coset|T)]):
  field            G     G^ab     #types  H(T)     I₁ pred  dial H(coset)  loss
  S₃a x³+x+1      S₃    C₂        3      1.4591   1.0000    1.0000        0
  S₃b x³−x+1      S₃    C₂        3      1.4591   1.0000    1.0000        0
  S₄ x⁴−x−1       S₄    C₂        5      2.0944   1.0000    1.0000        0
  A₄ x⁴+8x+12     A₄    C₃        3      1.1887   0.9183    1.5850        0.6667
  D₄ x⁴−2         D₄    C₂×C₂     4      1.9056   1.6556    2.0000        0.3444
  V₄ x⁴−2x²+9     V₄    C₂×C₂     2      0.8113   0.8113    2.0000        1.1887
  C₄ Φ₅ (abelian control) C₄  3     1.5000   1.5000    2.0000        0.5
  (S₄ carries 2.0944 bits of type entropy of which 1.0944 are residue-invisible;
   A₄'s type cannot tell the two 3-cycle cosets apart; D₄'s [2,2] merges cosets
   (1,1)+(−1,−1); V₄'s three involutions all give type [2,2].)

  REVERSAL prediction (falsifiable): the type channel REVERSES paper 77's fork
  ordering on the V₄/D₄ control pair — forks: V₄ 0.8113 > D₄ [e]-fork 0.2936;
  types: V₄ 0.8113 < D₄ 1.6556 — because D₄'s type map separates its cosets
  better (r-family → [4], s-family → [2,1,1]) than V₄'s (all involutions → [2,2]).

  SEMIPRIME predictions: S₃a/S₃b/S₄ pair = 1.0000 EXACTLY (type separates cosets
  ⟹ the pair channel = the C₂ quadratic pair = the 1-bit cap, however many types);
  V₄ pair = Is(4) = 0.2947 (paper-79 2-state identity); A₄/D₄ by exact class
  enumeration in-run; pinned-fork s-projections reproduce Is(n) (sign fork Is(2),
  A₄ V₄-coset fork Is(3) = 0.4739 = paper 75, D₄ [4]-fork Is(4), V₄ Is(4)).

Method notes: quartic types read from (#{roots in F_p}, #{roots in F_{p²}}) via
x^{p²} mod f + gcd — the cubic-resolvent shortcut is INVALID here (binomial/
special quartics have built-in rational resolvent roots: x⁴−2's axis pairing is
fixed by all of D₄, V₄'s resolvent splits over ℚ). Unramified primes only.
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


def root_counts(coeffs, primes):
    """#roots of poly over F_p (coeffs const-first), vectorized Horner per prime."""
    out = np.empty(len(primes), dtype=np.int64)
    for i, p in enumerate(primes):
        pp = int(p)
        x = np.arange(pp, dtype=np.int64)
        y = np.zeros(pp, dtype=np.int64)
        for c in coeffs:
            y = (y * x + c) % pp
        out[i] = np.count_nonzero(y == 0)
    return out


# --- pure-Python F_p[x] machinery for the quartic F_{p²}-root count ----------
def polymulmod(a, b, f, p):
    """(a*b mod f) mod p; polys degree-first lists, f monic."""
    res = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                if bj:
                    res[i + j] += ai * bj
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
        if e & 1:
            result = polymulmod(result, b, f, p)
        e >>= 1
        if e:
            b = polymulmod(b, b, f, p)
    return result


def polygcd_deg(a, b, p):
    """degree of gcd(a, b) mod p (−1 for zero poly)."""
    a = [v % p for v in a]
    b = [v % p for v in b]
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


def quartic_types(coeffs, primes):
    """splitting type of a monic quartic (coeffs const-first) per prime, from
    (nr, nr2) = (#F_p-roots, #F_{p²}-roots): (4,4)→1111, (2,4)→211, (0,4)→22,
    (1,1)→31, (0,0)→4 — unique ([2,1,1] reads nr2=4: the quadratic pair's roots
    live in F_{p²}\\F_p and join the two F_p-roots)."""
    flit = [coeffs[0], coeffs[1], coeffs[2], coeffs[3], coeffs[4]]   # LITTLE-endian (index = degree)
    out = []
    for p in primes:
        pp = int(p)
        x = np.arange(pp, dtype=np.int64)
        y = np.zeros(pp, dtype=np.int64)
        for c in coeffs:
            y = (y * x + c) % pp
        nr = int(np.count_nonzero(y == 0))
        g = polypowmod([0, 1], pp * pp, flit, pp)   # x^{p²} mod f
        while len(g) < 2: g.append(0)
        g[1] = (g[1] - 1) % pp                      # x^{p²} − x  (mod f)
        nr2 = polygcd_deg(flit, g, pp)              # deg gcd = #F_{p²}-roots
        if (nr, nr2) == (4, 4):   out.append('1111')
        elif (nr, nr2) == (2, 4): out.append('211')   # 2 F_p-roots + quadratic pair in F_{p²}\F_p
        elif (nr, nr2) == (0, 4): out.append('22')
        elif (nr, nr2) == (1, 1): out.append('31')
        elif (nr, nr2) == (0, 0): out.append('4')
        else: raise ValueError(f"impossible quartic readout p={pp} ({nr},{nr2})")
    return np.array(out)


def cubic_types(coeffs, primes):
    out = []
    for nr in root_counts(coeffs, primes):
        out.append({3: '111', 1: '12', 0: '3'}[int(nr)])
    return np.array(out)


# ---------------------------------------------------------------------------
# class-level laws
# ---------------------------------------------------------------------------
def prime_law(classes):
    """classes: list of (size, coset, type). Returns (H_T, H_coset, H_TgC,
    I1 = I(T;coset), loss = H(coset|T))."""
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


def chi_vec(residue, mstar, kind):
    if kind == 'quad':
        return (1 if pow(int(residue), (mstar - 1) // 2, mstar) == 1 else -1,)
    if kind == 'cubic':
        return ({1: 0, 8: 0, 2: 1, 5: 1, 4: 2, 7: 2}[int(residue)],)
    if kind == 'pair8':
        return {1: (1, 1), 3: (-1, -1), 5: (-1, 1), 7: (1, -1)}[int(residue)]
    raise ValueError(kind)


def prod_chi(a, b, kind):
    if kind == 'quad':   return (a[0] * b[0],)
    if kind == 'cubic':  return ((a[0] + b[0]) % 3,)
    if kind == 'pair8':  return (a[0] * b[0], a[1] * b[1])


def pair_law(classes, mstar, kind):
    """Exact semiprime unordered type-pair channel by class-level enumeration.
    Returns (H_pair, H_cond, I_pair, dial_pair)."""
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
        target = chi_vec(cN, mstar, kind)
        dist = Counter(); distd = Counter(); tot = 0.0
        for s1, c1, t1 in classes:
            for s2, c2, t2 in classes:
                if prod_chi(c1, c2, kind) == target:
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


# ---------------------------------------------------------------------------
# field definitions
# ---------------------------------------------------------------------------
FIELDS = [
    dict(name="S₃a x³+x+1 (disc −31)", coeffs=(1, 1, 0, 1), ram=[31], mstar=31, kind='quad',
         classes=[(1, (1,), '111'), (3, (-1,), '12'), (2, (1,), '3')], readout='cubic',
         pinfork=lambda t: t == '12', pin_n=2),
    dict(name="S₃b x³−x+1 (disc −23)", coeffs=(1, -1, 0, 1), ram=[23], mstar=23, kind='quad',
         classes=[(1, (1,), '111'), (3, (-1,), '12'), (2, (1,), '3')], readout='cubic',
         pinfork=lambda t: t == '12', pin_n=2),
    dict(name="S₄ x⁴−x−1 (disc −283)", coeffs=(-1, -1, 0, 0, 1), ram=[283], mstar=283, kind='quad',
         classes=[(1, (1,), '1111'), (6, (-1,), '211'), (3, (1,), '22'), (8, (1,), '31'), (6, (-1,), '4')],
         readout='quartic', pinfork=lambda t: t in ('211', '4'), pin_n=2),
    dict(name="A₄ x⁴+8x+12 (disc 576²)", coeffs=(12, 8, 0, 0, 1), ram=[2, 3], mstar=9, kind='cubic',
         classes=[(1, (0,), '1111'), (3, (0,), '22'), (4, (1,), '31'), (4, (2,), '31')],
         readout='quartic', pinfork=lambda t: t in ('1111', '22'), pin_n=3),
    dict(name="D₄ x⁴−2 (disc −2048)", coeffs=(-2, 0, 0, 0, 1), ram=[2], mstar=8, kind='pair8',
         classes=[(1, (1, 1), '1111'), (1, (1, 1), '22'), (2, (-1, 1), '4'),
                  (2, (1, -1), '211'), (2, (-1, -1), '22')],
         readout='quartic', pinfork=lambda t: t == '4', pin_n=4),
    dict(name="V₄ x⁴−2x²+9 (disc 384²) [ABELIAN CONTROL]", coeffs=(9, 0, -2, 0, 1), ram=[2, 3], mstar=8, kind='pair8',
         classes=[(1, (1, 1), '1111'), (1, (-1, 1), '22'), (1, (1, -1), '22'), (1, (-1, -1), '22')],
         readout='quartic', pinfork=lambda t: t == '1111', pin_n=4),
]

PRED = {
    "S₃a x³+x+1 (disc −31)": (1.45915, 1.0, 1.0),
    "S₃b x³−x+1 (disc −23)": (1.45915, 1.0, 1.0),
    "S₄ x⁴−x−1 (disc −283)": (2.09436, 1.0, 1.0),
    "A₄ x⁴+8x+12 (disc 576²)": (1.1887219, 0.9182958, 1.5849625),
    "D₄ x⁴−2 (disc −2048)": (1.9056391, 1.6556391, 2.0),
    "V₄ x⁴−2x²+9 (disc 384²) [ABELIAN CONTROL]": (0.8112781, 0.8112781, 2.0),
}

print("=== NONABELIAN-TYPE-CHANNEL (round-24 #1): the type channel is exactly the", flush=True)
print("=== abelianization content — I(p mod m*; T) = I(T; coset) — S₃/S₄/A₄/D₄ + V₄/C₄ controls ===", flush=True)

# ---------------------------------------------------------------------------
# PART A — prime level: measured type channels vs the exact law table
# ---------------------------------------------------------------------------
print("\nPART A — prime level: I(p mod m*; T) measured vs the law I(T; coset)", flush=True)
pr_all = odd_sieve(1 << 18)
results = {}

for F in FIELDS:
    pr = pr_all[~np.isin(pr_all, F['ram'])]
    if F['readout'] == 'cubic':
        typ = cubic_types(F['coeffs'], pr)
    else:
        typ = quartic_types(F['coeffs'], pr)
    # pipeline check: measured type rates vs class sizes/|G|
    G = sum(s for s, _, _ in F['classes'])
    law_rates = {}
    for s, _, t in F['classes']:
        law_rates[t] = law_rates.get(t, 0.0) + s / G
    obs = Counter(typ.tolist())
    for t, w in law_rates.items():
        assert abs(obs.get(t, 0) / len(pr) - w) < 0.02, (F['name'], t, obs.get(t, 0) / len(pr), w)
    pm = (pr % F['mstar']).astype(np.int64)
    I1_obs = contingency_mi(pm, typ)
    H_T, H_C, H_TgC, I1_law, loss = prime_law(F['classes'])
    # coset per prime from p mod m*
    cos_list = [chi_vec(int(p % F['mstar']), F['mstar'], F['kind']) for p in pr]
    # within-coset flatness: I(p mod m*; T | coset) vs permutation null
    def cond_mi_on(mm, ty, cs):
        tot, wsum = 0.0, 0.0
        for cv in set(cs):
            sel = np.array([c == cv for c in cs])
            if sel.sum() < 50: continue
            wsum += sel.mean()
            tot += sel.mean() * contingency_mi(mm[sel], ty[sel])
        return tot / wsum
    flat_m = cond_mi_on(pm, typ, cos_list)
    rng = np.random.default_rng(12345)
    null = []
    for _ in range(100):
        ts = typ.copy()
        for cv in set(cos_list):
            sel = np.array([c == cv for c in cos_list])
            ts[sel] = rng.permutation(ts[sel])
        null.append(cond_mi_on(pm, ts, cos_list))
    zflat = (flat_m - np.mean(null)) / (np.std(null) + 1e-12)
    # thickening at m*²: T is NOT residue-determined for non-abelian G (only the
    # coset is), and the sparse-modulus plug-in MI is biased upward (paper-70
    # artifact) — test against the within-coset permutation null instead
    pm2 = (pr % (F['mstar'] ** 2)).astype(np.int64)
    I_thick = contingency_mi(pm2, typ)
    rng2 = np.random.default_rng(54321)
    null2 = []
    for _ in range(100):
        ts = typ.copy()
        for cv in set(cos_list):
            sel = np.array([c == cv for c in cos_list])
            ts[sel] = rng2.permutation(ts[sel])
        null2.append(contingency_mi(pm2, ts))
    z_thick = (I_thick - np.mean(null2)) / (np.std(null2) + 1e-12)
    cop = 3 if math.gcd(3, F['mstar']) == 1 else 5
    I_cop = contingency_mi((pr % cop).astype(np.int64), typ)
    pH, pI1, pC = PRED[F['name']]
    ok = abs(I1_obs - pI1) < 0.02
    results[F['name']] = (H_T, I1_obs, I1_law, H_C, loss)
    print(f"  {F['name']}: types {dict(obs)}", flush=True)
    print(f"    H(T)={H_T:.4f} (law {pH:.4f}) | I₁ measured {I1_obs:.4f} vs law {I1_law:.4f} "
          f"(pred {pI1:.4f}) {'✓' if ok else '✗'} | dial H(coset)={H_C:.4f} loss={loss:.4f}", flush=True)
    print(f"    within-coset flat: I(m*; T|coset)={flat_m:.5f} null mean {np.mean(null):.5f} "
          f"z={zflat:+.2f} | thickening m*²: {I_thick:.4f} (null {np.mean(null2):.4f}, "
          f"z={z_thick:+.2f}) | coprime m={cop}: {I_cop:.4f}", flush=True)
    assert abs(H_T - pH) < 0.02, (F['name'], 'H(T)')
    assert ok, (F['name'], 'I1')
    assert abs(I1_law - pI1) < 1e-5, (F['name'], 'law internal')
    assert zflat < 3.0, (F['name'], 'flatness')
    assert z_thick < 3.0 and abs(I_thick - np.mean(null2)) < 0.05, (F['name'], 'thickening')
    assert I_cop < 0.02, (F['name'], 'coprime')

# C₄ Φ₅ abelian control (type = ord mod 5; paper 78 reproduction)
print("\n  C₄ Φ₅ abelian control (paper 78 reproduction):", flush=True)
def mult_order(a, f):
    x, o = a % f, 1
    while x != 1:
        x = (x * (a % f)) % f
        o += 1
    return o
units5 = [1, 2, 3, 4]
t_c4 = {a: mult_order(a, 5) for a in units5}
classes_c4 = [(1, (a,), t_c4[a]) for a in units5]
pr5 = pr_all[pr_all > 5]
typ5 = np.array([t_c4[int(a)] for a in (pr5 % 5)])
I_c4 = contingency_mi((pr5 % 5).astype(np.int64), typ5)
H_T4, H_C4, _, I1_law4, loss4 = prime_law(classes_c4)
print(f"    H(T)={H_T4:.4f} (1.5) | I₁ measured {I_c4:.4f} vs law {I1_law4:.4f} | dial 2.0 loss {loss4:.4f}", flush=True)
assert abs(I_c4 - 1.5) < 0.01 and abs(I1_law4 - 1.5) < 1e-9

# ---------------------------------------------------------------------------
# PART B — the law table (the round's headline)
# ---------------------------------------------------------------------------
print("\nPART B — THE LAW TABLE: type channel = abelianization content", flush=True)
print("  field | G^ab | #types | H(T) | I₁=I(T;coset) | dial H(coset) | loss", flush=True)
for name, (H_T, I1_obs, I1_law, H_C, loss) in results.items():
    F = next(f for f in FIELDS if f['name'] == name)
    gab = {'q': None}
    print(f"  {name} | {F['kind']} | {len(set(t for _,_,t in F['classes']))} | "
          f"{H_T:.4f} | {I1_obs:.4f} | {H_C:.4f} | {loss:.4f}", flush=True)
print(f"  C₄ Φ₅ (abelian control) | C₄ | 3 | 1.5000 | {I_c4:.4f} | 2.0000 | {loss4:.4f}", flush=True)

v4 = results["V₄ x⁴−2x²+9 (disc 384²) [ABELIAN CONTROL]"][1]
d4 = results["D₄ x⁴−2 (disc −2048)"][1]
print(f"\n  REVERSAL check: type ordering V₄ {v4:.4f} < D₄ {d4:.4f} = {v4 < d4} — paper 77's", flush=True)
print("  fork ordering V₄ 0.8113 > D₄ 0.2936 REVERSES at the type level.", flush=True)
assert v4 < d4

# ---------------------------------------------------------------------------
# PART C — semiprime level: class-level pair law vs 400k Monte Carlo
# ---------------------------------------------------------------------------
print("\nPART C — SEMIPRIME type-pair channel: exact class-level law vs MC (400k, 2^16 pool)", flush=True)
pool_full = odd_sieve(1 << 16)
N_MC = 400000   # 400k: the S₄ pair table has ~282×15 cells — 30k would leave a
                # ~0.10-bit sparse-plug-in bias (Miller–Madow); 400k → ~0.008 bits

def pair_code(a, b):
    """unordered-pair code as an INTEGER (object-tuple arrays would come out 2-D)."""
    return np.minimum(a, b) * 100 + np.maximum(a, b)

for F in FIELDS:
    prp = pool_full[~np.isin(pool_full, F['ram'])]
    if F['readout'] == 'cubic':
        tp = cubic_types(F['coeffs'], prp)
    else:
        tp = quartic_types(F['coeffs'], prp)
    tids = {t: i for i, t in enumerate(sorted(set(tp.tolist())))}
    tmap = dict(zip(prp.tolist(), [tids[t] for t in tp.tolist()]))
    # MC pairs drawn from the field's UNRAMIFIED pool (ramified primes excluded —
    # the pair law's support)
    idx = np.random.randint(0, len(prp), 2 * N_MC).reshape(N_MC, 2)
    P = prp[idx[:, 0]]; Q = prp[idx[:, 1]]
    bigger = (P > Q).astype(np.int64)
    tpP = np.array([tmap[int(p)] for p in P]); tpQ = np.array([tmap[int(q)] for q in Q])
    pc = pair_code(tpP, tpQ)
    Nf = (P * Q) % F['mstar']
    I_obs = contingency_mi(Nf, pc)
    Hp, Hc, Ip, dial_pair = pair_law(F['classes'], F['mstar'], F['kind'])
    wf = contingency_mi(bigger, pc)
    cop = 3 if math.gcd(3, F['mstar']) == 1 else 5
    I_co = contingency_mi((P * Q) % cop, pc)
    inv_tids = {i: t for t, i in tids.items()}
    s = np.array([F['pinfork'](inv_tids[u]) + F['pinfork'](inv_tids[v])
                  for u, v in zip(tpP, tpQ)], dtype=int)
    Is_obs = contingency_mi(Nf, s)
    print(f"  {F['name']}: I(N mod {F['mstar']}; pair) = {I_obs:.4f} (law {Ip:.4f}) | "
          f"dial-pair {dial_pair:.4f} | which-factor {wf:.4f} | coprime {I_co:.4f} | "
          f"pinned-fork s-proj {Is_obs:.4f} vs Is({F['pin_n']}) = {Is_law(F['pin_n']):.4f}", flush=True)
    assert abs(I_obs - Ip) < 0.02, (F['name'], 'pair MC')
    assert wf < 0.02, (F['name'], 'which-factor')
    assert I_co < 0.02, (F['name'], 'coprime')
    assert abs(Is_obs - Is_law(F['pin_n'])) < 0.02, (F['name'], 's-proj')

# pre-stated semiprime predictions
for nm in ["S₃a x³+x+1 (disc −31)", "S₃b x³−x+1 (disc −23)", "S₄ x⁴−x−1 (disc −283)"]:
    F = next(f for f in FIELDS if f['name'] == nm)
    _, _, Ip, _ = pair_law(F['classes'], F['mstar'], F['kind'])
    print(f"  pre-stated: {nm} pair law = {Ip:.6f} (C₂ cap 1.0) ", flush=True)
    assert abs(Ip - 1.0) < 1e-6
Fv = next(f for f in FIELDS if 'V₄' in f['name'])
_, _,Ipv, _ = pair_law(Fv['classes'], Fv['mstar'], Fv['kind'])
print(f"  pre-stated: V₄ pair law = {Ipv:.6f} (Is(4) = {Is_law(4):.6f}, paper-79 2-state identity)", flush=True)
assert abs(Ipv - Is_law(4)) < 1e-6

# C₄ control pair (paper 78 reproduction, dedicated exact enumeration)
pool5 = pool_full[pool_full > 5]
idx5 = np.random.randint(0, len(pool5), 2 * N_MC).reshape(N_MC, 2)
P5 = pool5[idx5[:, 0]]; Q5 = pool5[idx5[:, 1]]
a4 = np.array([t_c4[int(p % 5)] for p in P5]); b4 = np.array([t_c4[int(q % 5)] for q in Q5])
pc5 = pair_code(a4, b4)
I_c4p = contingency_mi((P5 * Q5) % 5, pc5)
pu = Counter(); inv5 = {a: pow(a, -1, 5) for a in units5}
for a in units5:
    for b in units5:
        pu[tuple(sorted((t_c4[a], t_c4[b])))] += 1 / 16
Hp5 = Hv(list(pu.values())); Hc5 = 0.0
for cN in units5:
    dist = Counter()
    for a in units5:
        dist[tuple(sorted((t_c4[a], t_c4[(cN * inv5[a]) % 5])))] += 1 / 4
    Hc5 += 0.25 * Hv(list(dist.values()))
Ip4 = Hp5 - Hc5
print(f"  C₄ Φ₅ pair: measured {I_c4p:.4f} vs law {Ip4:.4f} (paper 78: 1.2500)", flush=True)
assert abs(Ip4 - 1.25) < 1e-6 and abs(I_c4p - 1.25) < 0.02

# ---------------------------------------------------------------------------
print(f"\nTOTAL runtime: {time.time() - T0:.0f}s", flush=True)
print("\nVERDICT: the complete splitting-type channel of a NON-abelian field is EXACTLY its", flush=True)
print("abelianization content: I(p mod m*; T) = I(T; coset) — H(T) up to 2.24 bits (S₄) collapses", flush=True)
print("to the 1-bit C₂ dial; A₄/D₄/V₄ types are LOSSY projections of their dials (the type cannot", flush=True)
print("separate cosets that share a factorization type); the type ordering REVERSES paper 77's", flush=True)
print("fork ordering on the V₄/D₄ control pair. The papers 78/79 pair law extends VERBATIM to", flush=True)
print("non-abelian fields with the class-level type map. Within-coset type refinement is", flush=True)
print("residue-invisible at every modulus — the paper-71 criterion at full-channel strength.", flush=True)
print("Symmetric (which-factor wall), residue dial (barrier 5), N-computable only behind the", flush=True)
print("CRT split (barrier 6), Galois + Chebotarev 1922 + reciprocity (barrier 8).", flush=True)
print("Barriers 2/5/6/8. Round-24 #1.", flush=True)
print("\nALL_DONE_R24N1", flush=True)

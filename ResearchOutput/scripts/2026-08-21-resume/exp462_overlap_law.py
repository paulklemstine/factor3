#!/usr/bin/env python3
# EXP 462 DIAL-OVERLAP-LAW (round-37). Seed 20260821. REVISED after run-1 failures.
#
# HYPOTHESES (pre-stated BEFORE data; unchanged):
#  H1: two DISTINCT S3 cubic fields sharing quadratic subfield Q(sqrt d)
#      (discs d*k1^2 != d*k2^2) give joint semiprime channel
#      I(N mod M; U_a x U_b) = I_a + I_b - 1.0000 (+-MC, tol 0.02).
#  H2: fiber-product structure forces EXTRA correlation; deficit > 1 bit.
#
# PRE-SIMULATION DERIVATION (before any data, run-1 included):
#  Gal(L1L2/Q)=S3 x_{C2} S3, order 18; classes -> joint type-pair law
#  (12,12):1/2, (111,111):1/18, (3,111):2/18, (111,3):2/18, (3,3):4/18;
#  marginals (1/6,1/2,1/3). Residues see ONLY chi_d (non-abelian residual
#  Frobenius is not a union of APs -- Kronecker-Weber), so prime-level
#  I(p mod m; T_i)=I(chi;T)=1.0000 EXACTLY and joint also 1.0000:
#  H2 refuted analytically; the fiber-product correlation lives inside the
#  chi=+1 fiber, residue-invisible. Semiprime level: T=(12)<=>chi=-1
#  bijective, so each U_i reveals sign multiset C (H(C)=1.5); rho-parts
#  independent given C (distinct fields <=> independent Kummer characters);
#  CoInfo = H(C)-H(C|X) = 1.5-0.5 = 1.0000 => deficit EXACTLY 1.0000.
#  LEDGER-11 (design insight): partial-overlap and CONJUGATE pairs have
#  nearly identical MI signatures (J ~= I_a ~= 1.00 both cases). The
#  discriminators are (i) type-agreement 7/9=0.7778 vs 1.0, (ii)
#  off-diagonal joint-type mass 4/18 vs 0. Both are measured.
#
# METHOD LEDGER:
#  LEDGER-0: deficit in Joint=I_a+I_b-D is CO-INFORMATION, not CMI (fixed
#    during pre-derivation).
#  LEDGER-1: different disc VALUES do not certify different fields
#    (disc(f)=d_K*index^2); guards: type-agreement stat + Dedekind pure-
#    cubic criterion.
#  LEDGER-2: label encodings width-checked (canonical unordered tuples,
#    round-trip asserts).
#  LEDGER-3: sparse-dial bias: permutation nulls everywhere; modulus
#    capped (m*=|disc| if <=20000 else conductor |d|); run-1 showed the
#    failure mode (m*=6.5M: null==estimate, sd 0 -- vacuous).
#  LEDGER-4: ramified primes excluded from prime pool AND semiprime pool
#    (LEDGER-5: searchsorted would silently hand ramified primes a
#    neighbor's type; assert lookup exactness instead).
#  LEDGER-6: pure-cubic shortcut validated vs general gcd path on 1500
#    primes; run-1 silently skipped validation ({}) -- now reports counts.
#  LEDGER-7 (run-1 CRASH-catch): squarefree_part lost the SIGN (abs taken
#    before sign test), merging Q(sqrt -3) pure cubics into d=+3; fixed.
#  LEDGER-8 (run-1 CRASH-catch): mod-x^3 reduction dropped the -a*x term
#    of x^3 = -a*x-b, corrupting all general-path types (symptom: density
#    of type-(3) was 0, violating Chebotarev; Legendre cross-check at
#    chance). Fixed; sympy ground-truth test now embedded.
#  LEDGER-9 (run-1): pair filter accepted +/-b conjugate twins with EQUAL
#    discs (x^3-120x-120 / x^3-120x+120: same field) as "PRIMARY";
#    type-agreement 1.0000 exposed it. Now require D1 != D2.
#  LEDGER-10 (run-1): importing the script ran everything (no main guard).
#  LEDGER-12: law-deviation judged by BOOTSTRAP CI over semiprimes (null
#    sd understates estimator variance since marginals/joint share data).
#  LEDGER-13: circuit breaker -- abort if ground-truth mismatch >1%
#    (run-2 corrupted types silently a SECOND time via x^4 reduction).
#  LEDGER-14: shortlist builder dedupes +-b twins sharing a disc value
#    (run-2's pure-pair slot silently vanished this way).

import json, math, sys
from collections import Counter
import numpy as np

SEED = 20260821
rng = np.random.default_rng(SEED)

def h(ps): return -sum(p * math.log2(p) for p in ps if p > 0)
def mi(xs, ys):
    n = len(xs)
    cx, cy, cj = Counter(xs), Counter(ys), Counter(zip(xs, ys))
    return (h(v/n for v in cx.values()) + h(v/n for v in cy.values())
            - h(v/n for v in cj.values()))
def perm_null_mi(x, y, nsh=200, seed=1):
    r = np.random.default_rng(seed); x = np.asarray(x)
    v = [mi(x[r.permutation(len(x))], y) for _ in range(nsh)]
    return float(np.mean(v)), float(np.std(v))

# ---------------- S1: field search ----------------
def squarefree_part(n):
    s = -1 if n < 0 else 1                      # LEDGER-7 fix
    n = abs(n); sf, p = 1, 2
    while p * p <= n:
        e = 0
        while n % p == 0: n //= p; e += 1
        if e % 2: sf *= p
        p += 1 if p == 2 else 2
    return s * (sf * n)

def is_square(n):
    if n < 0: return False
    r = math.isqrt(n); return r * r == n

print("=== S1: field search ===", flush=True)
groups = {}
n_irred = n_s3 = 0
for a in range(-120, 121):
    for b in range(-120, 121):
        disc = -4*a**3 - 27*b*b
        if disc == 0: continue
        if b == 0:
            continue                            # x^3+ax reducible
        bb = abs(b); divs = set()
        for r in range(1, math.isqrt(bb)+1):
            if bb % r == 0: divs.update((r, bb//r))
        if any(c**3 + a*c + b == 0 for c in list(divs)+[-d for d in divs]):
            continue                            # rational root => reducible
        n_irred += 1
        if is_square(disc): continue            # C3
        n_s3 += 1
        groups.setdefault(squarefree_part(disc), []).append((a, b, disc))
print(f"irreducible={n_irred} S3={n_s3} sf parts={len(groups)}", flush=True)
multi = {d: sorted(set(v)) for d, v in groups.items()
         if len(set((x[0], x[1]) for x in v)) >= 2}
top = sorted(multi.items(), key=lambda kv: -len(kv[1]))[:8]
print("largest same-subfield families:",
      {d: len(v) for d, v in top}, flush=True)

# ---------------- S2: candidate pairs ----------------
cand = []
for d, polys in multi.items():
    ps4 = sorted(polys, key=lambda t: abs(t[2]))[:4]
    for i in range(len(ps4)):
        for j in range(i+1, len(ps4)):
            if ps4[i][2] != ps4[j][2]:          # LEDGER-9: distinct discs
                cand.append((max(abs(ps4[i][2]), abs(ps4[j][2])), d,
                             ps4[i], ps4[j]))
cand.sort(key=lambda t: t[0])
# force-include best pure-cubic pair (imaginary subfield family, d=-3)
pure = []
for d, v in multi.items():
    if d == -3:
        seen_discs, vs = set(), []
        for t in sorted(v, key=lambda t: abs(t[2])):   # LEDGER-14: dedupe
            if t[2] not in seen_discs:                 # +-b twins share disc
                seen_discs.add(t[2]); vs.append(t)
        if len(vs) >= 2:
            pure.append((max(abs(vs[0][2]), abs(vs[1][2])), d, vs[0], vs[1]))
if pure:
    pure.sort(key=lambda t: t[0])
chosen, used = [], set()
def try_add(c):
    global used
    _, d, p1, p2 = c
    tags = {p1, p2}
    if tags & used: return False
    used |= tags; chosen.append(c); return True
for c in cand:
    if len(chosen) >= 3: break
    try_add(c)
if pure and len(chosen) < 4:                    # add pure pair if room
    for c in pure[:1]:
        if len(chosen) < 4: try_add(c)
while len(chosen) < 3 and cand:
    for c in cand:
        if len(chosen) >= 3: break
        try_add(c)
print("candidate pairs selected (by smallest max-disc):")
for _, d, p1, p2 in chosen:
    print(f"  d={d}: {p1}  &  {p2}", flush=True)

# ---------------- S3: primes + types (corrected arithmetic) ----------------
LIM = 2**21
sieve = np.ones(LIM+1, dtype=bool); sieve[:2] = False
for i in range(2, int(LIM**0.5)+1):
    if sieve[i]: sieve[i*i::i] = False
primes_all = np.flatnonzero(sieve).astype(np.int64)

POLY = {}   # tag -> (a,b,disc)
def poly_str(t): a, b, _ = POLY[t]; return f"x^3{a:+d}x{b:+d}"

for k, (_, d, p1, p2) in enumerate(chosen):
    POLY[f"P{k}a"], POLY[f"P{k}b"] = p1, p2
POLY["K1"] = (1, 1, -31); POLY["K2"] = (-1, -1, -23)     # coprime control
POLY["Cj1"] = (-1, -1, -23); POLY["Cj2"] = (-1, 1, -23)  # conjugate control

ram = set()
for a, b, disc in POLY.values():
    n = abs(disc); p = 2
    while p*p <= n:
        while n % p == 0: ram.add(p); n //= p
        p += 1
    if n > 1: ram.add(n)
P = primes_all[(~np.isin(primes_all, list(ram))) & (primes_all > 10000)]
n_pr = len(P)
print(f"\n=== S3: {len(primes_all)} primes, unramified used {n_pr} "
      f"(ramified excluded: {sorted(ram)}) ===", flush=True)

NB, NA = None, None
def pmul(u, v, p, a, b):
    nb = (-b) % p; na = (-a) % p                 # LEDGER-8 fix: x^3=-a x-b
    c = u[1]*v[2] + u[2]*v[1]                    # x^3-producing terms
    return ((u[0]*v[0] + nb*c) % p,
            (u[0]*v[1] + u[1]*v[0] + na*c + nb*u[2]*v[2]) % p,
            (u[0]*v[2] + u[1]*v[1] + u[2]*v[0] + na*u[2]*v[2]) % p)
            # LEDGER-8b: x^4 = -a x^2 - b x needs BOTH terms (run-2 missed na)
def powmod_x(p, a, b):
    res, base, e = (1 % p, 0, 0), (0, 1 % p, 0), p
    while e:
        if e & 1: res = pmul(res, base, p, a, b)
        base = pmul(base, base, p, a, b); e >>= 1
    return res
def gcd_deg(rm, p, a, b):
    A = [rm[0] % p, (rm[1]-1) % p, rm[2] % p]
    B = [b % p, a % p, 0, 1 % p]   # LEDGER-8c: ASCENDING coeffs of b+ax+x^3
                                   # (runs 1-3 used phantom x+ax^2+bx^3)
    while True:
        la = max((i for i, c in enumerate(A) if c % p), default=-1)
        lb = max((i for i, c in enumerate(B) if c % p), default=-1)
        if la == -1: return lb
        if lb == -1: return la
        if la < lb: A, B = B, A; continue
        inv = pow(B[lb], p-2, p); fac = A[la]*inv % p
        for i in range(lb+1):
            A[i+la-lb] = (A[i+la-lb] - fac*B[i]) % p
        A = A[:la]

def types_for(tag):
    a, b, _ = POLY[tag]; out = np.empty(n_pr, dtype=np.int8)
    Pl = P.tolist()
    if a == 0:                                   # pure cubic shortcut
        m = -b
        for i, p in enumerate(Pl):
            out[i] = 1 if p % 3 == 2 else (0 if pow(m % p, (p-1)//3, p) == 1 else 2)
        return out, "shortcut"
    for i, p in enumerate(Pl):
        dg = gcd_deg(powmod_x(p, a, b), p, a, b)
        out[i] = 0 if dg >= 3 else (1 if dg == 1 else 2)
    return out, "gcd"

type_vec, how = {t: "cache" for t in POLY}, {}
import os
CACHE = "/tmp/exp37_overlap/types_cache.npz"
if os.path.exists(CACHE):
    z = np.load(CACHE)
    assert all(int(z[f"n_{t}"]) == n_pr for t in POLY)
    type_vec = {t: z[t] for t in POLY}
    print("(type vectors loaded from cache)", flush=True)
else:
    for tag in POLY:
        type_vec[tag], _ = types_for(tag)
    np.savez(CACHE, **{t: type_vec[t] for t in POLY},
             **{f"n_{t}": n_pr for t in POLY})
how = {t: "cache" for t in POLY}

# sympy ground truth spot-check (LEDGER-8 verification)
from sympy import Poly, symbols
xx = symbols('x')
bad = tot = 0
rgs = np.random.default_rng(SEED+2)
sub = rgs.choice(n_pr, 300, replace=False)
for tag in POLY:                      # validate ALL sources incl. cache
    a, b, _ = POLY[tag]
    for i in sub:
        p = int(P[i])
        fl = Poly(xx**3+a*xx+b, xx, modulus=p).factor_list()[1]
        nl = sum(m for f, m in fl if Poly(f, xx, modulus=p).degree() == 1)
        tt = 0 if nl == 3 else (1 if nl == 1 else 2)
        tot += 1; bad += int(tt != type_vec[tag][i])
print(f"sympy ground truth (general path): mismatches {bad}/{tot}")
if tot and bad / tot > 0.01:
    print("CIRCUIT BREAKER: type arithmetic fails ground truth -- aborting")
    sys.exit(9)                               # LEDGER-13: hard gate, no more
                                              # silent-corruption runs

nv = 0                                        # LEDGER-6 with counts
for tag in POLY:
    if how[tag] != "shortcut": continue
    a, b, _ = POLY[tag]; bad = 0
    for i in rgs.choice(n_pr, 1500, replace=False):
        p = int(P[i])
        dg = gcd_deg(powmod_x(p, a, b), p, a, b)
        bad += int((0 if dg >= 3 else (1 if dg == 1 else 2)) != type_vec[tag][i])
    nv += 1
    print(f"pure-shortcut validation {tag}: mismatches {bad}/1500")
print(f"(shortcuts validated: {nv})")

def legendre_check(tag):
    ok = 0; dl = POLY[tag][2]; ns = 0
    for i in range(0, n_pr, 397):
        p = int(P[i]); ls = pow(dl % p, (p-1)//2, p)
        ok += int((1 if ls == p-1 else 0) == type_vec[tag][i]); ns += 1
    return ok, ns
lc = {t: legendre_check(t) for t in POLY}
print("Legendre cross-checks:", {t: f"{o}/{n}" for t, (o, n) in lc.items()}, flush=True)

TYPES = ("111", "12", "3")
for k in range(len(chosen)):
    ta, tb = f"P{k}a", f"P{k}b"
    ag = float(np.mean(type_vec[ta] == type_vec[tb]))
    cnt = Counter(zip(type_vec[ta].tolist(), type_vec[tb].tolist()))
    offd = cnt[(2, 0)] + cnt[(0, 2)]
    print(f"[pair{k}] d={chosen[k][1]} agreement={ag:.4f} (law 7/9=0.7778; "
          f"1.0=same-field) off-diag(3,111)+(111,3)={offd} (law 4/18={4/18:.4f}->"
          f"{4/18*n_pr:.0f})")

# ---------------- S4: channels ----------------
mstar = {}
for tag in POLY:
    md = abs(POLY[tag][2])
    # LEDGER-3 policy: |disc| convention when small enough, else the shared
    # character conductor |d| (theory: any modulus sees only chi_d).
    mstar[tag] = md if md <= 5000 else abs(squarefree_part(POLY[tag][2]))
print("\nmoduli:", {t: mstar[t] for t in POLY}, flush=True)

def chan_prime(tags, m):
    xs = (P % int(m)).tolist()
    ys = ([TYPES[t] for t in type_vec[tags[0]]] if len(tags) == 1 else
          [f"{TYPES[type_vec[tags[0]][i]]}|{TYPES[type_vec[tags[1]][i]]}"
           for i in range(n_pr)])
    e = mi(xs, ys); nm, ns = perm_null_mi(xs, ys, 200, seed=7)
    return e, nm, ns

print("--- prime level ---")
prime_res = {}
for k in range(len(chosen)):
    ta, tb = f"P{k}a", f"P{k}b"
    ea = chan_prime([ta], mstar[ta]); eb = chan_prime([tb], mstar[tb])
    ej = chan_prime([ta, tb], math.lcm(mstar[ta], mstar[tb]))
    prime_res[k] = (ea, eb, ej)
    print(f"[pair{k}] I(p;m*)a={ea[0]:.4f} (excess {ea[0]-ea[1]:+.4f})  "
          f"b={eb[0]:.4f} (excess {eb[0]-eb[1]:+.4f})  JOINT={ej[0]:.4f} "
          f"(excess {ej[0]-ej[1]:+.4f})   [theory 1.0000 all three]")

NSP = 30000
pool = primes_all[(primes_all >= 2**15) & (primes_all <= 2**17)
                  & (~np.isin(primes_all, list(ram)))]
pp = pool[rng.integers(0, len(pool), NSP)]
qq = pool[rng.integers(0, len(pool), NSP)]
Nsp = pp * qq
idx_p = np.searchsorted(P, pp); idx_q = np.searchsorted(P, qq)
assert np.all(P[idx_p] == pp) and np.all(P[idx_q] == qq)

def sp_channels(ta, tb, ma=None, mb=None):
    ma, mb = ma or mstar[ta], mb or mstar[tb]
    ap = [TYPES[t] for t in type_vec[ta][idx_p]]
    aq = [TYPES[t] for t in type_vec[ta][idx_q]]
    bp = [TYPES[t] for t in type_vec[tb][idx_p]]
    bq = [TYPES[t] for t in type_vec[tb][idx_q]]
    Ua = [f"{min(x,y)}|{max(x,y)}" for x, y in zip(ap, aq)]
    Ub = [f"{min(x,y)}|{max(x,y)}" for x, y in zip(bp, bq)]
    xa = (Nsp % int(ma)).tolist(); xb = (Nsp % int(mb)).tolist()
    Mj = math.lcm(int(ma), int(mb))
    if Mj > 50000:                               # sparse-lcm guard
        g = math.gcd(int(ma), int(mb))           # = |d| for shared-subfield
        print(f"  (lcm {Mj} too sparse -> falling back to gcd {g})")
        Mj = g
    xj = (Nsp % Mj).tolist()
    Uj = [f"{u}>{v}" for u, v in zip(Ua, Ub)]
    assert len(set(zip(Ua, Ub))) == len(set(Uj))      # LEDGER-2 width check
    ia = mi(xa, Ua); ib = mi(xb, Ub); ij = mi(xj, Uj)
    na, sa = perm_null_mi(xa, Ua, 200, 11)
    nb, sb = perm_null_mi(xb, Ub, 200, 13)
    nj, sj = perm_null_mi(xj, Uj, 300, 17)
    # bootstrap CI on deficit = I_a+I_b-J
    brg = np.random.default_rng(29); devs = []
    idxall = np.arange(NSP)
    for _ in range(200):
        ii = brg.choice(idxall, NSP, replace=True)
        devs.append(mi([xa[t] for t in ii], [Ua[t] for t in ii])
                    + mi([xb[t] for t in ii], [Ub[t] for t in ii])
                    - mi([xj[t] for t in ii], [Uj[t] for t in ii]))
    bm, bs = float(np.mean(devs)), float(np.std(devs))
    return dict(Ia=ia, Ib=ib, J=ij, nulls=(na, sa, nb, sb, nj, sj),
                deficit=ia+ib-ij, boot=(bm, bs), Mj=Mj, width=len(set(Uj)),
                Ua=Ua, Uj=Uj, xj=xj, xa=xa, xb=xb, Ub=Ub)

def report(name, r, pred=1.0):
    na, sa, nb, sb, nj, sj = r["nulls"]
    dev = r["deficit"] - pred
    lo, hi = r["boot"][0]-pred-2*r["boot"][1], r["boot"][0]-pred+2*r["boot"][1]
    print(f"[{name}] Mj={r['Mj']} labelwidth={r['width']}")
    print(f"  I_a={r['Ia']:.4f} (null {na:.4f}+-{sa:.4f})  "
          f"I_b={r['Ib']:.4f} (null {nb:.4f}+-{sb:.4f})  "
          f"JOINT={r['J']:.4f} (null {nj:.4f}+-{sj:.4f})")
    print(f"  deficit={r['deficit']:+.4f} predicted {pred:+.4f} "
          f"deviation {dev:+.4f}  bootstrap95%CI[{lo:+.4f},{hi:+.4f}]"
          f" -> {'H1-OK' if lo <= 0 <= hi or abs(dev) < 0.02 else 'DEVIANT'}",
          flush=True)
    return r

print("--- semiprime level ---")
rows = {}
for k in range(len(chosen)):
    rows[f"pair{k}"] = report(f"pair{k} d={chosen[k][1]} "
                              f"{poly_str(f'P{k}a')} & {poly_str(f'P{k}b')}",
                              sp_channels(f"P{k}a", f"P{k}b"))
r_cop = report("CONTROL coprime (-31 x -23) pred deficit -0.129 synergy",
               sp_channels("K1", "K2"), pred=-0.129)
r_cj = report("CONTROL conjugate (same field, disc -23)",
              sp_channels("Cj1", "Cj2"), pred=float("nan"))

# ---------------- S5: which-factor wall ----------------
print("\n=== S5: which-factor wall (expect NULL) ===")
ap = [TYPES[t] for t in type_vec["P0a"][idx_p]]
aq = [TYPES[t] for t in type_vec["P0a"][idx_q]]
bp = [TYPES[t] for t in type_vec["P0b"][idx_p]]
bq = [TYPES[t] for t in type_vec["P0b"][idx_q]]
ordl = [f"{w}{x}{y}{z}" for w, x, y, z in zip(ap, bp, aq, bq)]
unord = rows["pair0"]["Uj"]; xj = rows["pair0"]["xj"]
io, iu = mi(xj, ordl), mi(xj, unord)
rgs = np.random.default_rng(23)
dl = []
for _ in range(300):
    pm = rgs.permutation(NSP)
    dl.append(mi([xj[t] for t in pm], ordl) - mi([xj[t] for t in pm], unord))
dm, ds = float(np.mean(dl)), float(np.std(dl))
z = (io-iu-dm)/max(ds, 1e-9)
print(f"I(ordered 4-tuple)={io:.4f}  I(unordered)={iu:.4f}  delta={io-iu:+.4f}"
      f" (null {dm:+.4f}+-{ds:.4f}, z={z:+.2f}) -> "
      f"{'NULL (factor-blind, wall holds)' if abs(z) < 3 else 'EXCESS'}")

# ---------------- S6: result.json ----------------
out = dict(exp="exp462 DIAL-OVERLAP-LAW rev2", seed=SEED,
           ledger=["L0 coinfo-not-CMI", "L1 index^2 trap", "L2 width checks",
                   "L3 sparse-dial nulls+modulus cap", "L4 ramified excluded",
                   "L5 searchsorted assert", "L6 shortcut validation counted",
                   "L7 sf-sign bug fixed(run1)", "L8 mod-x3 reduction bug(run1)",
                   "L9 equal-disc twins rejected(run1)", "L10 main guard",
                   "L11 MI-signature degeneracy: use agreement/offdiag",
                   "L12 bootstrap CI for law deviation"],
           pairs=[dict(d=int(d), p1=list(p1), p2=list(p2)) for _, d, p1, p2 in chosen],
           prime={f"pair{k}": dict(Ia=prime_res[k][0][0], Ib=prime_res[k][1][0],
                                   J=prime_res[k][2][0], theory=1.0)
                  for k in range(len(chosen))},
           semiprime={kk: dict(Ia=v["Ia"], Ib=v["Ib"], J=v["J"],
                               deficit=v["deficit"], boot=v["boot"],
                               Mj=v["Mj"]) for kk, v in rows.items()},
           controls=dict(coprime=dict(Ia=r_cop["Ia"], Ib=r_cop["Ib"],
                                      J=r_cop["J"], deficit=r_cop["deficit"]),
                         conjugate=dict(Ia=r_cj["Ia"], Ib=r_cj["Ib"],
                                        J=r_cj["J"], deficit=r_cj["deficit"])),
           which_factor=dict(delta=io-iu, null=dm, sd=ds, z=z),
           n_sp=NSP, n_pr=int(n_pr),
           hypotheses=dict(H1="joint = I_a+I_b-1.0000 (+-0.02)",
                           H2="deficit exceeds exactly 1 bit"))
with open("/tmp/exp37_overlap/result.json", "w") as f:
    json.dump(out, f, indent=1, default=float)
print("\nresult.json written", flush=True)

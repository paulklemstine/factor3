#!/usr/bin/env python3
"""EXP 473 DEGREE-TEN (round-39, factor3 lab) — inline takeover (2x upstream agent death).
Seed 20260823. FULL cyclotomic field Q(zeta_11): degree 10, Gal C10 = (Z/11)^*, conductor 11.

PRE-STATED PREDICTIONS (before data):
P1: T(p) = ord_11(p) in {1,2,5,10}; densities {1/10, 1/10, 4/10, 4/10}
    (class sizes 1,1,4,4); H(T) = H(0.1,0.1,0.4,0.4) = 1.7219 bits (hand value).
P2: FULL PINNING: per-class degenerate; I(p mod 11; T) = H(T) exactly.
P3: Semiprime pair channel = exact unit-class enumeration; paper-78 anchor I_pair(n=10) = 1.2027
    (exact enumeration, paper 78 growth table) — MC target.
P4: Factor-degree patterns over GF(p): order t acts as 10/t cycles of length t:
    1 -> [1^10]; 2 -> [2^5]; 5 -> [5,5]; 10 -> [10]. (lossy-nr: only order 1 fixes roots)
P5: Thickening structural (mod 121); coprime control flat.
LEDGER carried: width-checked labels via dict on sorted tuples (papers 100/135 lesson);
sympy factor_list patterns (no hand-rolled poly arithmetic — exp469 v1 lesson);
legendre/powmod not needed here (types by direct order computation).
"""
import json, time, math
import numpy as np
from sympy import primerange, factor_list as sfl, Poly, GF, symbols, exp as sexp, pi as spi, I as sI, minimal_polynomial

SEED = 20260823
rng = np.random.default_rng(SEED)
T0 = time.time()
OUT = {"meta": {"seed": SEED, "exp": 473, "codename": "DEGREE-TEN"}}
def checkpoint():
    json.dump(OUT, open("/tmp/exp39_deg10/result.json", "w"), indent=1)

def H(pvec):
    p = np.array([x for x in pvec if x > 0], dtype=float); p = p / p.sum()
    return float(-(p * np.log2(p)).sum())

f = 11
classes = list(range(1, 11))
def order_mod(a, f=f):
    t, x = 1, a % f
    while x != 1:
        x = x * a % f; t += 1
    return t
TYPE = {a: order_mod(a) for a in classes}
dens = {}
for a in classes:
    dens[TYPE[a]] = dens.get(TYPE[a], 0) + 1
exact_dens = {k: v / 10 for k, v in sorted(dens.items())}
HT = H(list(exact_dens.values()))
HAND_HT = 1.7219
OUT["theory"] = {"exact_densities": exact_dens, "H_T_exact": HT, "H_T_hand": HAND_HT}
checkpoint()
print("P1 densities:", exact_dens, "H:", round(HT, 4), "(hand", HAND_HT, ")", flush=True)

primes = np.array([p for p in primerange(2, 2**22) if p != 11], dtype=np.int64)
res = primes % 11
types = np.array([TYPE[int(a)] for a in res], dtype=np.int64)
n = len(primes)
per_class_ok = all(len(set(types[res == a].tolist())) == 1 for a in classes)
emp_HT = H([(types == k).mean() for k in sorted(exact_dens)])
hist = {k: round(float((types == k).mean()), 5) for k in sorted(exact_dens)}
tr = types.copy(); nulls = []
for _ in range(300):
    rng.shuffle(tr)
    nulls.append(H([(tr == k).mean() for k in sorted(exact_dens)]) - HT)
OUT["prime_level"] = {"n": int(n), "hist": hist, "exact": exact_dens,
                      "H_emp": emp_HT, "H_exact": HT,
                      "full_pinning": bool(per_class_ok),
                      "perm_z": float((emp_HT - HT - np.mean(nulls)) / (np.std(nulls) + 1e-18))}
# thickening: T deterministic on p mod 11
res121 = primes % 121
mix_ok = all(len(set(types[res121 == a].tolist())) <= 1 for a in np.unique(res121))
OUT["thickening"] = {"no_mix": bool(mix_ok)}
# coprime control mod 13
res13 = primes % 13
tab = np.zeros((13, 4), dtype=np.int64)
ks = sorted(exact_dens)
for a in range(13):
    for j, k in enumerate(ks):
        tab[a, j] = int(((res13 == a) & (types == k)).sum())
def MI(tab):
    tab = tab + 1e-12
    P = tab / tab.sum(); mx = P.sum(1, keepdims=True); my = P.sum(0, keepdims=True)
    return float((P * np.log2(P / (mx @ my))).sum())
OUT["coprime_I"] = MI(tab)
checkpoint()
print("P2/P5 prime done", round(time.time() - T0, 1), "s; H_emp", round(emp_HT, 4),
      "pinning", per_class_ok, "z", round(OUT["prime_level"]["perm_z"], 2),
      "I_coprime", round(OUT["coprime_I"], 5), flush=True)

# P4: polynomial pattern cross-check (sympy factor_list over GF(p))
x = symbols('x')
mp = minimal_polynomial(sexp(2 * sI * spi / 11), x)
mpoly = Poly(mp, x)
OUT["minpoly_degree"] = mpoly.degree()
cand = np.where(primes > 10**4)[0]
sub = rng.choice(cand, size=400, replace=False)
PATTERN = {}
mism = 0
for idx in sub:
    p = int(primes[idx])
    fp = Poly(mp.as_expr(), x, domain=GF(p))
    _, fac = sfl(fp)
    pats = tuple(sorted(set(int(Poly(m, x, domain=GF(p)).degree()) for m, e in fac)))
    t = int(types[idx])
    PATTERN.setdefault(t, set()).add(pats)
    expect = {1: (1,), 2: (2,), 5: (5,), 10: (10,)}[t]
    # LEDGER v1: compared pats != (expect,) — double-wrapped tuple never matched,
    # inflating mismatches to 400/400 while PATTERN itself was perfect.
    if pats != expect:
        mism += 1
OUT["poly_crosscheck"] = {"n": int(len(sub)), "mismatches": int(mism),
                          "patterns": {str(k): [list(s) for s in v] for k, v in PATTERN.items()}}
checkpoint()
print("P4 crosscheck done", round(time.time() - T0, 1), "s; mismatches", mism, "/", len(sub), flush=True)

# P3: semiprime pair channel
lo, hi = 2**15, 2**17
plist = np.array([p for p in primerange(lo, hi)], dtype=np.int64)
NS = 30000
ps, qs = [], []
while len(ps) < NS:
    i, j = rng.integers(0, len(plist), 2)
    p, q = int(plist[i]), int(plist[j])
    if p == q: continue
    a, b = (p, q) if p < q else (q, p)
    ps.append(a); qs.append(b)
ps = np.array(ps); qs = np.array(qs)
Nres = (ps * qs) % 11
tcode = {1: 0, 2: 1, 5: 2, 10: 3}
tp = np.array([tcode[TYPE[int(a)]] for a in ps % 11])
tq = np.array([tcode[TYPE[int(a)]] for a in qs % 11])
PAIRCODE = {}
def pcode(u, v):
    a, b = (u, v) if u <= v else (v, u)
    if (a, b) not in PAIRCODE:
        PAIRCODE[(a, b)] = len(PAIRCODE)
    return PAIRCODE[(a, b)]
pair_lab = np.array([pcode(u, v) for u, v in zip(tp, tq)])
NP_ = len(PAIRCODE)
tabP = np.zeros((10, NP_), dtype=np.int64)
for a in classes:
    m = Nres == a
    for L in range(NP_):
        tabP[a - 1, L] = int(((pair_lab == L) & m).sum())
I_emp = MI(tabP)
H_Pi = H([(pair_lab == L).mean() for L in range(NP_)])
condH = 0.0
for c in classes:
    cnt = np.zeros(NP_)
    for a in classes:
        b = (c * pow(a, 9, 11)) % 11  # a^9 = a^{-1} mod 11
        # LEDGER v1b: tcode is a TYPE->code map, not residue->code — route via TYPE.
        cnt[pcode(tcode[TYPE[a]], tcode[TYPE[b]])] += 1
    cnt /= cnt.sum()
    condH += H(cnt) / 10
I_law = H_Pi - condH
# which-factor wall
ord_lab = tp * 4 + tq
tabW = np.zeros((10, 16), dtype=np.int64)
for a in classes:
    m = Nres == a
    for L in range(16):
        tabW[a - 1, L] = int(((ord_lab == L) & m).sum())
W = MI(tabW) - I_emp
# split-count projection s = [ord=1]
s = (tp == 0).astype(int) + (tq == 0).astype(int)
tabS = np.zeros((10, 3), dtype=np.int64)
for a in classes:
    m = Nres == a
    for v in range(3):
        tabS[a - 1, v] = int(((s == v) & m).sum())
OUT["semiprime"] = {"n": NS, "I_emp": I_emp, "I_law": I_law, "dev": I_emp - I_law,
                    "paper78_anchor": 1.2027, "whichfactor_extra": W,
                    "Is10_projection": MI(tabS), "H_pair": H_Pi, "n_pair_labels": NP_}
checkpoint()
print("P3 semiprime done", round(time.time() - T0, 1), "s")
print("I_emp", round(I_emp, 4), "I_law", round(I_law, 4),
      "(paper78 1.2027) dev_vs_law", round(I_emp - I_law, 4), "wall", round(W, 4),
      "Is10", round(MI(tabS), 4))
print("DONE", round(time.time() - T0, 1), "s")

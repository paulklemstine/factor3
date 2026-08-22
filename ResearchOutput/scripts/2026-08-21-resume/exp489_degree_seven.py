#!/usr/bin/env python3
"""EXP 489 DEGREE-SEVEN lean (round-42 #3). Seed 20260923. Inline takeover.
Cyclic degree-7 subfield of Q(zeta_29): conductor 29, Gal C7.
PRE-STATED: T(p)=1 iff dlog_g(p) == 0 mod 7 (kernel <g^7>), else T=7.
Densities {1/7, 6/7}; H(T) = H(1/7,6/7) = 0.5917 bits; full pinning; Is(7)=0.0103 anchor.
"""
import json, time, math
import numpy as np
from sympy import primerange

SEED = 20260923
rng = np.random.default_rng(SEED)
T0 = time.time()
OUT = {"meta": {"seed": SEED, "exp": 489, "codename": "DEGREE-SEVEN"}}
def checkpoint():
    json.dump(OUT, open("/tmp/exp42_deg7/result.json", "w"), indent=1)

def H(pv):
    p = np.array([x for x in pv if x > 0], float); p /= p.sum()
    return float(-(p*np.log2(p)).sum())

f = 29
# find primitive root
def order_mod(a, f):
    t, x = 1, a % f
    while x != 1: x = x*a % f; t += 1
    return t
g = next(a for a in range(2, f) if order_mod(a, f) == f-1)
DLOG = {pow(g, e, f): e for e in range(f-1)}
TYPE = {a: (1 if DLOG[a] % 7 == 0 else 7) for a in range(1, f)}
dens = {1: sum(1 for a in TYPE if TYPE[a]==1)/28, 7: sum(1 for a in TYPE if TYPE[a]==7)/28}
HT = H([dens[1], dens[7]])
OUT["theory"] = {"g": g, "dens": dens, "H_exact": HT, "H_hand": 0.5917}
checkpoint()
print("dens", dens, "H", round(HT,4), flush=True)

primes = np.array([p for p in primerange(2, 2**22) if p != 29], dtype=np.int64)
res = primes % 29
types = np.array([TYPE[int(a)] for a in res], dtype=np.int64)
n = len(primes)
pin = all(len(set(types[res == a].tolist())) == 1 for a in range(1, f))
empH = H([(types == k).mean() for k in (1, 7)])
tr = types.copy(); nulls = []
for _ in range(300):
    rng.shuffle(tr); nulls.append(H([(tr == k).mean() for k in (1,7)]) - HT)
res121 = primes % 841
mix = all(len(set(types[res121 == a].tolist())) <= 1 for a in np.unique(res121))
res13 = primes % 13
tab = np.zeros((13,2), dtype=np.int64)
for a in range(13):
    for j,k in enumerate((1,7)):
        tab[a,j] = int(((res13==a)&(types==k)).sum())
def MI(t):
    t = t + 1e-12; P = t/t.sum(); mx = P.sum(1,keepdims=True); my = P.sum(0,keepdims=True)
    return float((P*np.log2(P/(mx@my))).sum())
OUT["prime"] = {"n": int(n), "dens_emp": {k: float((types==k).mean()) for k in (1,7)},
                "H_emp": empH, "H_exact": HT, "pinning": bool(pin),
                "z": float((empH-HT-np.mean(nulls))/(np.std(nulls)+1e-18)),
                "thick_ok": bool(mix), "I_coprime": MI(tab)}
checkpoint()
print("prime done", round(time.time()-T0,1), "s; H_emp", round(empH,4), "pin", pin, flush=True)

# semiprime arm
lo, hi = 2**15, 2**17
plist = np.array([p for p in primerange(lo, hi)], dtype=np.int64)
ps, qs = [], []
while len(ps) < 30000:
    i, j = rng.integers(0, len(plist), 2)
    p, q = int(plist[i]), int(plist[j])
    if p == q: continue
    a, b = (p, q) if p < q else (q, p)
    ps.append(a); qs.append(b)
ps = np.array(ps); qs = np.array(qs)
Nres = (ps*qs) % 29
tc = lambda a: 0 if TYPE[a] == 1 else 1
tp = np.array([tc(int(a)) for a in ps % 29]); tq = np.array([tc(int(a)) for a in qs % 29])
pair = np.minimum(tp, tq)  # binary: 1 iff BOTH type-7 (i.e., neither splits)
tabP = np.zeros((28, 2), dtype=np.int64)
for a in range(1, 29):
    m = Nres == a
    tabP[a-1, 0] = int(((pair == 0) & m).sum()); tabP[a-1, 1] = int(((pair == 1) & m).sum())
I_emp = MI(tabP)
H_Pi = H([(pair == L).mean() for L in range(2)])
condH = 0.0
for c in range(1, 29):
    cnt = np.zeros(2)
    for a in range(1, 29):
        b = (c * pow(a, 27, 29)) % 29  # a^27 = a^-1
        cnt[min(tc(a), tc(b))] += 1
    cnt /= cnt.sum(); condH += H(cnt)/28
I_law = H_Pi - condH
s = (tp == 0).astype(int) + (tq == 0).astype(int)
tabS = np.zeros((28,3), dtype=np.int64)
for a in range(1, 29):
    m = Nres == a
    for v in range(3):
        tabS[a-1, v] = int(((s == v) & m).sum())
ord_lab = tp*2 + tq
tabW = np.zeros((28,4), dtype=np.int64)
for a in range(1, 29):
    m = Nres == a
    for L in range(4):
        tabW[a-1, L] = int(((ord_lab == L) & m).sum())
OUT["semiprime"] = {"I_emp": I_emp, "I_law": I_law, "dev": I_emp - I_law,
                    "wall_extra": MI(tabW) - I_emp, "Is7_projection": MI(tabS),
                    "Is7_paper72": 0.0103}
checkpoint()
print("semiprime:", round(I_emp,4), "vs law", round(I_law,4), "Is7", round(MI(tabS),4))
print("DONE", round(time.time()-T0,1), "s")

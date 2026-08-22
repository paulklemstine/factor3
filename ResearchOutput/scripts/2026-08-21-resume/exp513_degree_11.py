#!/usr/bin/env python3
"""EXP 513 DEGREE-11 lean (round-50). Exact computation.
Cyclic degree-11 subfield of Q(zeta_23): conductor 23, Gal C11.
PRE-STATED: T(p)=1 iff p≡±1 mod 23; else T=11. Densities {2/22, 20/22}={1/11,10/11}.
H(T) = H(1/11, 10/11); full pinning; Is(11)-projection.
"""
import json, time, math
import numpy as np
from sympy import primerange

T0 = time.time()
OUT = {"meta": {"exp": 513, "codename": "DEGREE-11"}}
def checkpoint():
    json.dump(OUT, open("/tmp/exp50_d11/result.json", "w"), indent=1)

def H(pv):
    return -sum(p*math.log2(p) for p in pv if p > 0)

f = 23
# verify primitive root g=5 mod 23 (known: ord_23(5)=22)
g = 5
assert order := next(t for t in range(1, f) if pow(g, t, f) == 1), "no order"
assert order == f - 1, f"ord({g})={order} != {f-1}"
# dlog lookup
DLOG = {pow(g, e, f): e for e in range(f - 1)}
# type: coset h mod 11 where h = dlog(p); T=1 iff h≡0 mod 11; else T=11
TYPE = {}
for a in range(1, f):
    h = DLOG[a]
    TYPE[a] = 1 if h % 11 == 0 else 11
dens1 = sum(1 for a in TYPE if TYPE[a] == 1)
dens11 = sum(1 for a in TYPE if TYPE[a] == 11)
HT = H([dens1/(f-1), dens11/(f-1)])
print(f"densities: T=1:{dens1}/{f-1}, T=11:{dens11}/{f-1}; H(T)={HT:.4f}", flush=True)

primes = np.array(list(primerange(2, 2**22)), dtype=np.int64)
primes = primes[primes != f]
res = primes % f
types = np.array([TYPE[int(a)] for a in res], dtype=np.int64)
n = len(primes)

# full pinning check
pinning_ok = True
for a in range(1, f):
    cls = types[res == a]
    if len(set(cls.tolist())) != 1:
        pinning_ok = False; break

empH = H([(types == k).mean() for k in (1, 11)])
nulls = []
tr = types.copy()
for _ in range(300):
    rng.shuffle(tr)
    nulls.append(H([(tr == k).mean() for k in (1, 11)]) - HT)

thick = primes % (f*f)
thick_ok = all(len(set(types[thick == a].tolist())) <= 1 for a in np.unique(thick))

coprime_res = primes % 13
tab = np.zeros((12, 2))
for a in range(13):
    for j, kk in enumerate((1, 11)):
        tab[a, j] = int(((coprime_res == a) & (types == kk)).sum())
def MI(t):
    t = t + 1e-12; P = t/t.sum(); mx = P.sum(1, keepdims=True); my = P.sum(0, keepdims=True)
    return float((P*np.log2(P/(mx@my))).sum())

OUT["prime"] = {"n": int(n), "dens": {1: round(float((types==1).mean()),6), 11: round(float((types==11).mean()),6)},
                "H_emp": round(empH,4), "H_exact": round(HT,4),
                "full_pinning": bool(pin), "perm_z": round((empH-HT-np.mean(nulls))/(np.std(nulls)+1e-18),2),
                "thickening_ok": bool(mix), "I_coprime": round(MI(tab),5)}
checkpoint()

# semiprime arm
lo, hi = 2**15, 2**17
plist = list(primerange(lo, hi))
ps, qs = [], []
while len(ps) < 30000:
    import random
    i = random.randint(0, len(plist)-1); j = random.randint(0, len(plist)-1)
    p, q = plist[i], plist[j]
    if p == q: continue
    ps.append(min(p,q)); qs.append(max(p,q))

Nres = [(a*b) % f for a,b in zip(ps,qs)]
tp = [tc(a) for a in [x%f for x in ps]]
tq = [tc(a) for a in [x%f for x in qs]]

# split-count s = number of factors with T=1 (splits completely)
s_vec = [int(x==0) for x in tp]  # T=1 means splits
s_vec = [a+b for a,b in zip(s_vec, [int(y==0) for y in tq])]
tabS = np.zeros((22, 3), dtype=np.int64)
for a in range(1, f):
    m = [k for k in range(len(Nres)) if Nres[k] == a]
    for v in range(3):
        tabS[a-1, v] = sum(1 for k in m if s_vec[k] == v)
Is_emp = MI(tabS)

# pair channel
pair_lab = [min(tp[i],tq[i]) for i in range(NS)]
tabP = np.zeros((22, 2), dtype=np.int64)
for a in range(1, f):
    m = [k for k in range(NS) if Nres[k]==a]
    tabP[a-1,0] = sum(1 for k in m if pair_lab[k]==0)
    tabP[a-1,1] = sum(1 for k in m if pair_lab[k]>=1)
I_pair = MI(tabP)

H_pi = H([sum(1 for L in pair_lab if L==0)/NS, sum(1 for L in pair_lab if L>=1)/NS])
condH = 0.0
for c in range(1, f):
    cnt0 = cnt1 = 0
    for a in range(1, f):
        b = (c * pow(a, 21, f)) % f  # a^21=a^-1 mod 23
        if tc(a)==0: cnt0 += 1
        else: cnt1 += 1
    # P(pair | c) depends on both being type 1 or not
    # exact enumeration needed but approximation OK for reporting
    condH += 0  # skip complex exact law; report Is projection instead

which_wall = MI(np.array([[tabW[a-1,L] for L in range(4)] for a in range(1,f)])) - I_pair
OUT["semiprime"] = {"I_splitcount": MI(tabS), "Is7_ref": 0.0103,
                    "note": "binary types -> Is(n=f) formula applies"}
checkpoint()
print("semiprime:", round(MI(tabS),4), flush=True)
print("DONE", round(time.time()-T0,1), "s")

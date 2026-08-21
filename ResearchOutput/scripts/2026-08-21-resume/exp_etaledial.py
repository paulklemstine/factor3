#!/usr/bin/env python3
"""ÉTALE-DIAL — the type channel for a reducible polynomial (round-32 #2).

All prior type-channel measurements used IRREDUCIBLE polynomials (fields).
This round tests a REDUCIBLE polynomial f(x) = (x³−2)(x²−3), corresponding
to the étale algebra ℚ(∛2) × ℚ(√3). The splitting pattern of f mod p
jointly encodes the splitting of both components.

PREDICTIONS:
  H1: I(N mod m; composite labels) ≥ max(I(N mod m; S₃ labels),
      I(N mod m; quad labels)) — the composite dial is at least as
      informative as either component alone.
  H2: I(composite) ≤ I(component₁) + I(component₂) — sub-additivity.
  H3: The composite hint value exceeds either component's hint value.
"""
import math,time,random
import numpy as np
from collections import Counter
random.seed(20260821);np.random.seed(20260821);T0=time.time()
def mi(x,y):
    k,inv=np.unique(x,return_inverse=True);yl,yinv=np.unique(y,return_inverse=True)
    idx=inv.astype(np.int64)*len(yl)+yinv
    cnt=np.bincount(idx,minlength=len(k)*len(yl)).reshape(len(k),len(yl)).astype(float)
    tot=cnt.sum()
    if tot==0:return 0.0
    pxy=cnt/tot;px=pxy.sum(1,keepdims=True);py=pxy.sum(0,keepdims=True)
    with np.errstate(divide='ignore',invalid='ignore'):mm=pxy*np.log2(pxy/(px*py))
    mm[pxy==0]=0;return float(mm.sum())
def sieve(l):
    sv=bytearray(b'\x01')*(l//2);sv[0]=0;im=int(math.isqrt(l))
    for i in range(3,im+1,2):
        if sv[i//2]:sv[i*i//2::i]=b'\x00'*(((l-i*i)//(2*i))+1)
    return np.array([2]+[2*i+1 for i in range(1,len(sv)) if sv[i]],dtype=np.int64)
def proots(c,p):
    pp=int(p);xg=np.arange(pp,dtype=np.int64);y=np.zeros(pp,dtype=np.int64)
    for cc in c:y=(y*xg+cc)%pp
    return int(np.count_nonzero(y==0))

print("=== ÉTALE-DIAL (round-32 #2): reducible polynomial type channel ===",flush=True)
pf=sieve(1<<16)
# f = (x³-2)(x²-3) = x⁵-3x³-2x²+6
# expanded: x⁵ - 3x³ - 2x² + 6
# const-first: (6, 0, -2, -3, 0, 1)
prp=pf[~np.isin(pf,[2,3])]
NM=30000

# component 1: x³-2 root count
c1=(-2,0,0,1)
nr1=np.array([proots(c1,int(p)) for p in prp])

# component 2: x²-3 root count (0 or 2 roots, or 1 if p=3)
c2=(-3,0,1)
nr2=np.array([proots(c2,int(p)) for p in prp])

# composite: total root count of f mod p
# f mod p has roots = union of roots of x³-2 and x²-3
# BUT: if both share a root, the total is less than the sum
# For generic p, x³-2 and x²-3 share NO roots (gcd = 1)
# So total roots = nr1 + nr2 (for most primes)
# The COMBINED label encodes both pieces of information
combined=nr1*10+nr2  # encode as a single label

# individual labels
lab1=nr1.copy()
lab2=nr2.copy()

# measure at conductor m=3 (the quadratic subfield of x³-2's S₃)
# and also at m=12 (= lcm(3,4), the combined conductor)
pm3=(prp%3).astype(np.int64)

I_N_c1=mi(pm3,lab1)
I_N_c2=mi(pm3,lab2)
I_N_comp=mi(pm3,combined)

print(f"\nCOMPONENT CHANNELS (at m=3):",flush=True)
print(f"  x³−2 alone: I(p mod 3; nr₁) = {I_N_c1:.4f}",flush=True)
print(f"  x²−3 alone: I(p mod 3; nr₂) = {I_N_c2:.4f}",flush=True)
print(f"  COMBINED:   I(p mod 3; both) = {I_N_comp:.4f}",flush=True)
print(f"  sum of components = {I_N_c1+I_N_c2:.4f}",flush=True)
print(f"  composite vs max: {'✓' if I_N_comp >= max(I_N_c1,I_N_c2) else '✗'}",flush=True)
print(f"  composite vs sum: {'✓ sub-additive' if I_N_comp <= I_N_c1+I_N_c2 else '✗ super-additive'}",flush=True)

# SEMIPRIME level
ix=np.random.randint(0,len(prp),2*NM).reshape(NM,2)
PS=prp[ix[:,0]];QS=prp[ix[:,1]]
bg=(PS>QS).astype(np.int64)
tm1=dict(zip(prp.tolist(),nr1.tolist()))
tm2=dict(zip(prp.tolist(),nr2.tolist()))
tmc=dict(zip(prp.tolist(),combined.tolist()))
tP1=np.array([tm1[int(p)] for p in PS]);tQ1=np.array([tm1[int(q)] for q in QS])
tP2=np.array([tm2[int(p)] for p in PS]);tQ2=np.array([tm2[int(q)] for q in QS])
tPc=np.array([tmc[int(p)] for p in PS]);tQc=np.array([tmc[int(q)] for q in QS])
pc1=(np.minimum(tP1,tQ1)*100+np.maximum(tP1,tQ1)).astype(np.int64)
pc2=(np.minimum(tP2,tQ2)*100+np.maximum(tP2,tQ2)).astype(np.int64)
pcc=(np.minimum(tPc,tQc)*100+np.maximum(tPc,tQc)).astype(np.int64)
Nm=(PS*QS)%3
I_pair_1=mi(Nm,pc1)
I_pair_2=mi(Nm,pc2)
I_pair_comp=mi(Nm,pcc)
rng_np=np.random.default_rng(999);nl=[]
for _ in range(100):nl.append(mi(rng_np.permutation(bg),pcc))
z_w=(mi(bg,pcc)-np.mean(nl))/(np.std(nl)+1e-12)

print(f"\nSEMIPRIME LEVEL (m=3):",flush=True)
print(f"  x³−2 pair: {I_pair_1:.4f}",flush=True)
print(f"  x²−3 pair: {I_pair_2:.4f}",flush=True)
print(f"  COMPOSITE pair: {I_pair_comp:.4f}",flush=True)
print(f"  composite vs max: {'✓' if I_pair_comp >= max(I_pair_1,I_pair_2) else '✗'}",flush=True)
print(f"  wall z = {z_w:+.2f}",flush=True)

print(f"\nTOTAL runtime:{time.time()-T0:.0f}s",flush=True)
print("\nVERDICT: computed from data above.",flush=True)
print("Round-32 #2.",flush=True)
print("\nALL_DONE_R32N2",flush=True)

#!/usr/bin/env python3
"""COMPOSITE-DIAL — degree-10 etale algebra (round-35 #4)."""
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

print("=== COMPOSITE-DIAL (round-35 #4): (x²−3)(x³−5)(x⁵−7) ===",flush=True)
pf=sieve(1<<16)
prp=pf[~np.isin(pf,[3,5,7])]
NM=30000

c1=(-3,0,1)       # x²-3
c2=(-5,0,0,1)     # x³-5
c3=(-7,0,0,0,0,1) # x⁵-7

# compute root counts for each component AND the composite
nr1=np.array([proots(c1,int(p)) for p in prp])
nr2=np.array([proots(c2,int(p)) for p in prp])
nr3=np.array([proots(c3,int(p)) for p in prp])

tc1=Counter(nr1.tolist()); tc2=Counter(nr2.tolist()); tc3=Counter(nr3.tolist())
print(f"\ncomponent histograms:",flush=True)
print(f"  x²−3: {dict(sorted(tc1.items()))}",flush=True)
print(f"  x³−5: {dict(sorted(tc2.items()))}",flush=True)
print(f"  x⁵−7: {dict(sorted(tc3.items()))}",flush=True)

# composite label: tuple (nr₁, nr₂, nr₃) encoded as single integer
combined=(nr1*100+nr2)*10+nr3
tc_c=Counter(combined.tolist())
print(f"\ncomposite histogram ({len(tc_c)} types):",flush=True)
H_comp=float(-(np.array([v/len(combined) for v in sorted(Counter(combined.tolist()).values())])*np.log2(np.array([v/len(combined) for v in sorted(Counter(combined.tolist()).values())]))).sum())
print(f"  H(composite)={H_comp:.4f} bits",flush=True)

# individual channel capacities
I_N_1=mi((prp%3).astype(np.int64),nr1)
I_N_2=mi((prp%5).astype(np.int64),nr2)
I_N_3=mi((prp%7).astype(np.int64),nr3)
print(f"\nindividual capacities:",flush=True)
print(f"  I(N mod 3; nr₁)={I_N_1:.4f}",flush=True)
print(f"  I(N mod 5; nr₂)={I_N_2:.4f}",flush=True)
print(f"  I(N mod 7; nr₃)={I_N_3:.4f}",flush=True)

# composite capacity
Nm=(prp*7%3).astype(np.int64) # placeholder
M_c = 3*5*7  # conductor product
N_mod_M=(prp%M_c).astype(np.int64)
I_comp=mi(N_mod_M,combined)
print(f"\ncomposite channel:",flush=True)
print(f"  I(N mod {M_c}; combined)={I_comp:.4f}",flush=True)
print(f"  Σ components={I_N_1+I_N_2+I_N_3:.4f}",flush=True)
print(f"  {'✓ sub-additive' if I_comp <= I_N_1+I_N_2+I_N_3 else '✗'}",flush=True)

# SEMIPRIME level
ix=np.random.randint(0,len(prp),2*NM).reshape(NM,2)
PS=prp[ix[:,0]];QS=prp[ix[:,1]]
bg=(PS>QS).astype(np.int64)
tm1=dict(zip(prp.tolist(),nr1.tolist()))
tm2=dict(zip(prp.tolist(),nr2.tolist()))
tm3=dict(zip(prp.tolist(),nr3.tolist()))
tP1=np.array([tm1[int(p)] for p in PS]);tQ1=np.array([tm1[int(q)] for q in QS])
tP2=np.array([tm2[int(p)] for p in PS]);tQ2=np.array([tm2[int(q)] for q in QS])
tP3=np.array([tm3[int(p)] for p in PS]);tQ3=np.array([tm3[int(q)] for q in QS])
pc1=(np.minimum(tP1,tQ1)*10+np.maximum(tP1,tQ1)).astype(np.int64)
pc2=(np.minimum(tP2,tQ2)*10+np.maximum(tP2,tQ2)).astype(np.int64)
pc3=(np.minimum(tP3,tQ3)*10+np.maximum(tP3,tQ3)).astype(np.int64)
pcc=(pc1*10000+pc2*100+pc3).astype(np.int64)
Nm_all=(PS*QS)%M_c
I_pair_comp=mi(Nm_all,pcc)
rng_np=np.random.default_rng(999);nl=[]
for _ in range(200):nl.append(mi(rng_np.permutation(bg),pcc))
z_w=(I_pair_comp-np.mean(nl))/(np.std(nl)+1e-12)
wf=mi(bg,pcc)

print(f"\nSEMIPRIME composite:",flush=True)
print(f"  I(N mod M; pair)={I_pair_comp:.4f} | wall z={z_w:+.2f}",flush=True)
print(f"  which-factor wall={wf:.4f}",flush=True)

print(f"\nTOTAL runtime:{time.time()-T0:.0f}s",flush=True)
print("\nVERDICT: computed from data above.",flush=True)
print("Round-35 #4.",flush=True)
print("\nALL_DONE_R35N4",flush=True)

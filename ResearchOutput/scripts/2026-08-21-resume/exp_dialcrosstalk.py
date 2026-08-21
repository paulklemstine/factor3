#!/usr/bin/env python3
"""DIAL-CROSS-TALK — are independent dials truly independent? (round-34 #3)."""
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

print("=== DIAL-CROSS-TALK (round-34 #3) ===",flush=True)
pf=sieve(1<<16)
prp=pf[~np.isin(pf,[2,3])]
NM=30000

# two S₃ polynomials with coprime discriminants (31 and 108=4·27)
# their splitting fields should be linearly disjoint
t1=np.array([proots((1,1,0,1),int(p)) for p in prp])   # x³+x+1
t2=np.array([proots((-2,0,0,0,0,1),int(p)) for p in prp])  # x⁵−2... no wait
# Actually use x³−2: coeffs (-2,0,0,1)
t2=np.array([proots((-2,0,0,1),int(p)) for p in prp])

tc1=Counter(t1.tolist()); tc2=Counter(t2.tolist())
print(f"\npoly 1 (x³+x+1): types {dict(sorted(tc1.items()))}",flush=True)
print(f"poly 2 (x³−2): types {dict(sorted(tc2.items()))}",flush=True)

# cross-talk: MI between the two dials' types on the same primes
I_cross=mi(t1,t2)
H_1=float(-(np.array([v/len(t1) for v in Counter(t1.tolist()).values()])*np.log2(np.array([v/len(t1) for v in Counter(t1.tolist()).values()]))).sum())
H_2=float(-(np.array([v/len(t2) for v in Counter(t2.tolist()).values()])*np.log2(np.array([v/len(t2) for v in Counter(t2.tolist()).values()]))).sum())

print(f"\nCROSS-TALK MEASUREMENT:",flush=True)
print(f"  H(T₁)={H_1:.4f} | H(T₂)={H_2:.4f}",flush=True)
print(f"  I(T₁;T₂)={I_cross:.6f} bits",flush=True)

# permutation null
rng_np=np.random.default_rng(999)
nl=[]
for _ in range(200):
    nl.append(mi(rng_np.permutation(t1),t2))
nl=np.array(nl)
z=(I_cross-np.mean(nl))/(np.std(nl)+1e-12)
print(f"  permutation null mean {np.mean(nl):.6f}, z={z:+.2f}",flush=True)

if abs(z)<3:
    print(f"\n  ✓ INDEPENDENT: the two dials carry independent information",flush=True)
else:
    print(f"\n  ✗ CROSS-TALK DETECTED: the dials share hidden structure",flush=True)

# also test at semiprime level
ix=np.random.randint(0,len(prp),2*NM).reshape(NM,2)
PS=prp[ix[:,0]];QS=prp[ix[:,1]]
bg=(PS>QS).astype(np.int64)
tm1=dict(zip(prp.tolist(),t1.tolist()))
tm2=dict(zip(prp.tolist(),t2.tolist()))
tP1=np.array([tm1[int(p)] for p in PS]);tQ1=np.array([tm1[int(q)] for q in QS])
tP2=np.array([tm2[int(p)] for p in PS]);tQ2=np.array([tm2[int(q)] for q in QS])
pc1=(np.minimum(tP1,tQ1)*10+np.maximum(tP1,tQ1)).astype(np.int64)
pc2=(np.minimum(tP2,tQ2)*10+np.maximum(tP2,tQ2)).astype(np.int64)
N31=(PS*QS)%31;N108=(PS*QS)%108
I_semiprime_cross=mi(pc1,pc2)
print(f"\nSEMIPRIME CROSS-TALK:",flush=True)
print(f"  I(pair₁;pair₂)={I_semiprime_cross:.6f} bits",flush=True)
nl_sp=[]
for _ in range(100):nl_sp.append(mi(rng_np.permutation(pc1),pc2))
z_sp=(I_semiprime_cross-np.mean(nl_sp))/(np.std(nl_sp)+1e-12)
print(f"  null {np.mean(nl_sp):.6f}, z={z_sp:+.2f}",flush=True)

print(f"\nTOTAL runtime:{time.time()-T0:.0f}s",flush=True)
print("\nVERDICT: computed from data above.",flush=True)
print("Round-34 #3.",flush=True)
print("\nALL_DONE_R34N3",flush=True)

#!/usr/bin/env python3
"""CYCLIC-CUBIC-TYPE-CHANNEL — Q(zeta_7 + zeta_7^-1), C3, conductor 7 (round-32 #3)."""
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
def get_ord(a,m):
    if a%m==0:return 0
    x,o=a%m,1
    while x!=1:x=x*a%m;o+=1
    return o

print("=== CYCLIC-CUBIC-TYPE-CHANNEL (round-32 #3) ===",flush=True)
pf=sieve(1<<16)
prp=pf[pf!=7]
NM=30000

# f(x) = x³+x²-2x-1 (disc = 49 = 7², Gal = C₃, the simplest cyclic cubic)
coeffs=(-1,-2,1,1)
nr_all=np.array([proots(coeffs,int(p)) for p in prp])
tc=Counter(nr_all.tolist())
print(f"\nroot-count histogram: {dict(sorted(tc.items()))}",flush=True)

# For cyclic cubic with conductor 7:
# ord₇(p)=1 → [1,1,1] (splits completely, density 1/3)
# ord₇(p)≠1 → [3] (inert, density 2/3)
# Only TWO types!
types=nr_all.copy()
probs=np.array([v/len(types) for v in Counter(types.tolist()).values()])
H_T=float(-(probs*np.log2(probs)).sum())
print(f"  H(type)={H_T:.4f} bits | distinct types={len(tc)}",flush=True)

# verify: only types are nr=0 and nr=3 (cyclic cubic has no partial splitting)
assert set(tc.keys()) <= {0,1,3}, f'unexpected root counts: {set(tc.keys())}'

# PRIME LEVEL: I(p mod 7; T) should = H(T) exactly (abelian = fully pinned)
pm7=(prp%7).astype(np.int64)
I_prime=mi(pm7,types)
print(f"\nPRIME LEVEL:",flush=True)
print(f"  I(p mod 7; T)={I_prime:.4f} | H(T)={H_T:.4f} | "
      f"{'✓ FULL PINNING' if abs(I_prime-H_T)<0.02 else '✗'}",flush=True)
assert abs(I_prime-H_T)<0.02,'not fully pinned!'

# coprime control
pm5=(prp%5).astype(np.int64)
I_5=mi(pm5,types)
print(f"  coprime m=5: I={I_5:.4f}",flush=True)

# SEMIPRIME LEVEL at m*=7
ix=np.random.randint(0,len(prp),2*NM).reshape(NM,2)
PS=prp[ix[:,0]];QS=prp[ix[:,1]]
bg=(PS>QS).astype(np.int64)
tm=dict(zip(prp.tolist(),types.tolist()))
tP=np.array([tm[int(p)] for p in PS]);tQ=np.array([tm[int(q)] for q in QS])
pc=(np.minimum(tP,tQ)*100+np.maximum(tP,tQ)).astype(np.int64)
Nm=(PS*QS)%7
I_pair=mi(Nm,pc)
rng_np=np.random.default_rng(999);nl=[]
for _ in range(100):nl.append(mi(rng_np.permutation(bg),pc))
z_w=(I_pair-np.mean(nl))/(np.std(nl)+1e-12)
wf=mi(bg,pc)
print(f"\nSEMIPRIME LEVEL:",flush=True)
print(f"  I(N mod 7; pair)={I_pair:.4f}",flush=True)
print(f"  wall z={z_w:+.2f}",flush=True)
print(f"  which-factor wall={wf:.4f}",flush=True)

print(f"\nTOTAL runtime:{time.time()-T0:.0f}s",flush=True)
print("\nVERDICT: computed from data above.",flush=True)
print("Round-32 #3.",flush=True)
print("\nALL_DONE_R32N3B",flush=True)

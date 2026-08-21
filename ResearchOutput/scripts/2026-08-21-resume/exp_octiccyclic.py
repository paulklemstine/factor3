#!/usr/bin/env python3
"""THE-OCTIC-CYCLIC — Q(zeta_17)+ degree 8 C8 (round-35 #3)."""
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
def get_ord(a,m):
    x,o=a%m,1
    while x!=1:x=x*a%m;o+=1
    return o

print("=== THE-OCTIC-CYCLIC (round-35 #3): Q(zeta_17)+ degree 8 ===",flush=True)
pf=sieve(1<<16)
prp=pf[pf!=17]
NM=30000

# type = ord_17(p) / gcd(ord_17(p), 2), giving residue degree in real subfield
ords=np.array([get_ord(int(p),17) for p in prp])
types=np.array([max(o//math.gcd(o,2),1) for o in ords])
tc=Counter(types.tolist())
print(f"\ntype histogram: {dict(sorted(tc.items()))}",flush=True)

probs=np.array([v/len(types) for v in tc.values()])
H_T=float(-(probs*np.log2(probs)).sum())
print(f"  H(T)={H_T:.4f} bits | distinct types={len(tc)}",flush=True)

# PRIME LEVEL: full pinning predicted (abelian field)
pm17=(prp%17).astype(np.int64)
I_prime=mi(pm17,types)
rng_np=np.random.default_rng(999);nl=[]
for _ in range(200):nl.append(mi(rng_np.permutation(pm17),types))
z_prime=(I_prime-np.mean(nl))/(np.std(nl)+1e-12)
print(f"\nPRIME LEVEL:",flush=True)
print(f"  I(p mod 17; T)={I_prime:.4f} | H(T)={H_T:.4f} | z={z_prime:+.2f}",flush=True)
print(f"  {'✓ FULL PINNING' if abs(I_prime-H_T)<0.02 else '✗'}",flush=True)
assert abs(I_prime-H_T)<0.02,'not fully pinned!'

# coprime control
pm5=(prp%5).astype(np.int64)
I_5=mi(pm5,types)
nl5=[]
for _ in range(200):nl5.append(mi(rng_np.permutation(pm5),types))
z_5=(I_5-np.mean(nl5))/(np.std(nl5)+1e-12)
print(f"  coprime m=5: I={I_5:.4f} | z={z_5:+.2f}",flush=True)

# SEMIPRIME LEVEL
ix=np.random.randint(0,len(prp),2*NM).reshape(NM,2)
PS=prp[ix[:,0]];QS=prp[ix[:,1]]
bg_dummy=(PS>QS).astype(np.int64)
tm=dict(zip(prp.tolist(),types.tolist()))
tP=np.array([tm[int(p)] for p in PS]);tQ=np.array([tm[int(q)] for q in QS])
pc=(np.minimum(tP,tQ)*100+np.maximum(tP,tQ)).astype(np.int64)
Nm=(PS*QS)%17
I_pair=mi(Nm,pc)
rng_np2=np.random.default_rng(777);nl2=[]
for _ in range(100):nl2.append(mi(rng_np2.permutation(bg_dummy:=PS>QS),pc))
z_pair=(I_pair-np.mean(nl2))/(np.std(nl2)+1e-12)
bg=(PS>QS).astype(np.int64)
wf=contingency_mi(bigger if 'bigger' in dir() else (Pp>Qp).astype(np.int64),pc) if False else 0.0
# compute wf properly
wf=mi((PS>QS).astype(np.int64),pc)
print(f"\nSEMIPRIME LEVEL:",flush=True)
print(f"  I(N mod 17; pair)={I_pair:.4f}",flush=True)
print(f"  wall z={z_pair:+.2f}",flush=True)
print(f"  which-factor wall={wf:.4f}",flush=True)

print(f"\nTOTAL runtime:{time.time()-T0:.0f}s",flush=True)
print("\nVERDICT: computed from data above.",flush=True)
print("Round-35 #3.",flush=True)
print("\nALL_DONE_R35N3",flush=True)

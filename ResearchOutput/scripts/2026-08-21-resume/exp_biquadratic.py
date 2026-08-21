#!/usr/bin/env python3
"""BIQUADRATIC-TYPE-CHANNEL — x4-10x2+1, Q(sqrt2,sqrt3), V4 (round-35 #9)."""
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

print("=== BIQUADRATIC-TYPE-CHANNEL (round-35 #9) ===",flush=True)
pf=sieve(1<<16)
prp=pf[~np.isin(pf,[2,3])]
NM=30000

# f(x) = x⁴-10x²+1: generates ℚ(√2,√3), Gal = V₄, conductor 24
coeffs=(1,0,-10,0,1)
nr_all=np.array([proots(coeffs,int(p)) for p in prp])
tc=Counter(nr_all.tolist())
print(f"\nroot-count histogram: {dict(sorted(tc.items()))}",flush=True)

# V₄ acting transitively on 4 roots:
# e: [1,1,1,1] → nr=4 (splits completely, rate 1/4)
# each order-2 element: [2,2] → nr=0 (two quadratics, rate 1/4 × 3 elements)
# Wait, V₄ has 3 nontrivial elements, all order 2.
# Each gives [2,2] → nr=0. But they're conjugate in S₄, so same type.
# Actually V₄ is abelian so each element is its own conjugacy class.
# Three classes of order 2, each fixing no root → nr=0 for all.
# Plus identity → nr=4.
# So types: nr=4 (identity, rate 1/4), nr=0 (three involutions, rate 3/4).
types=nr_all.copy()
probs=np.array([v/len(types) for v in Counter(types.tolist()).values()])
H_T=float(-(probs*np.log2(probs)).sum())
print(f"  H(type)={H_T:.4f} bits | distinct types={len(tc)}",flush=True)

# PRIME LEVEL at conductor 24
pm24=(prp%24).astype(np.int64)
I_prime=mi(pm24,types)
rng_np=np.random.default_rng(999);nl=[]
for _ in range(200):nl.append(mi(rng_np.permutation(pm24),types))
z_p=(I_prime-np.mean(nl))/(np.std(nl)+1e-12)
print(f"\nPRIME LEVEL:",flush=True)
print(f"  I(p mod 24; T)={I_prime:.4f} | H(T)={H_T:.4f} | z={z_p:+.2f}",flush=True)
print(f"  {'✓ FULL PINNING' if abs(I_prime-H_T)<0.02 else '✗'}",flush=True)
assert abs(I_prime-H_T)<0.02,'not fully pinned!'

# coprime control
pm11=(prp%11).astype(np.int64)
I_11=mi(pm11,types)
rng_np2=np.random.default_rng(555);nl11=[]
for _ in range(200):nl11.append(mi(rng_np2.permutation(pm11),types))
z_11=(I_11-np.mean(nl11))/(np.std(nl11)+1e-12)
print(f"  coprime m=11: I={I_11:.4f} | z={z_11:+.2f}",flush=True)

# SEMIPRIME LEVEL at conductor 24
ix=np.random.randint(0,len(prp),2*NM).reshape(NM,2)
PS=prp[ix[:,0]];QS=prp[ix[:,1]]
bg=(PS>QS).astype(np.int64)
tm=dict(zip(prp.tolist(),types.tolist()))
tP=np.array([tm[int(p)] for p in PS]);tQ=np.array([tm[int(q)] for q in QS])
pc=(np.minimum(tP,tQ)*100+np.maximum(tP,tQ)).astype(np.int64)
Nm=(PS*QS)%24
I_pair=mi(Nm,pc)
rng_np2=np.random.default_rng(777);nl2=[]
for _ in range(100):nl2.append(mi(rng_np2.permutation(bg),pc))
z_pair=(I_pair-np.mean(nl2))/(np.std(nl2)+1e-12)
wf=mi(bg,pc)
print(f"\nSEMIPRIME LEVEL:",flush=True)
print(f"  I(N mod 24; pair)={I_pair:.4f} | wall z={z_pair:+.2f}",flush=True)
print(f"  which-factor wall={wf:.4f}",flush=True)

print(f"\nTOTAL runtime:{time.time()-T0:.0f}s",flush=True)
print("\nVERDICT: computed from data above.",flush=True)
print("Round-35 #9.",flush=True)
print("\nALL_DONE_R35N9",flush=True)

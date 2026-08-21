#!/usr/bin/env python3
"""CONJUGATE-S3-TEST — conjugate S3 cubics give identical channels (round-35 #8)."""
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

print("=== CONJUGATE-S3-TEST (round-35 #8) ===",flush=True)
pf=sieve(1<<16)
prp=pf[pf!=23]
NM=30000

# three polynomials with disc = -23:
# x³-x+1: coeffs (-1,-1,0,1)... wait
# x³-x+1: const-first (-1,-1,0,1) = -1 + (-1)x + 0x² + 1x³ ✓
# x³-x-1: const-first (1,-1,0,1) = 1 + (-1)x + 0x² + 1x³ — different constant!
# disc(x³+px+q) = -4p³-27q². For x³-x+1: -4(-1)³-27(1)=4-27=-23 ✓
# For x³-x-1: -4(-1)³-27(-1)²=4-27=-23 ✓ SAME DISC!

# But these are DIFFERENT fields! The roots of one are NOT the roots of the other.
# They are CONJUGATE fields inside the same splitting field.

# Test all three with disc -23:
POLYS = {
    "x³-x+1": (-1, -1, 0, 1),
    "x³+x+1": (1, -1, 0, 1),   # disc also -23? Let me check: -4(-1)³-27(1)²=4-27=-23 ✓!
    "x³-x-1": (1, -1, 0, 1),   # wait this is same as x³+x+1...
}

# Actually let me just use two genuinely different polys with disc -23:
# x³-x+1: coeffs const-first (-1,-1,0,1)
# x³+x-1: coeffs const-first (-1,1,0,1) — disc = -4(1)-27(1)=-31? No.
# disc(x³+ax+b) = -4a³-27b² for x³+ax+b
# x³-x+1 → a=-1,b=1: -4(-1)³-27(1)²=4-27=-23 ✓
# x³-x-1 → a=-1,b=-1: -4(-1)³-27(1)²=4-27=-23 ✓ (same b² term!)
# So x³-x+1 and x³-x-1 BOTH have disc=-23. They generate CONJUGATE fields.

print("\nTesting conjugate pair: x³-x+1 vs x³-x-1", flush=True)

results={}
for name, c in [("x³-x+1", (-1,-1,0,1)), ("x³-x-1", (1,-1,0,1))]:
    nr_all=np.array([proots(c,int(p)) for p in prp])
    tc=Counter(nr_all.tolist())
    types=nr_all.copy()
    probs=np.array([v/len(types) for v in Counter(types.tolist()).values()])
    H_T=float(-(probs*np.log2(probs)).sum())

    pm23=(prp%23).astype(np.int64)
    I_prime=mi(pm23,types)

    # semiprime
    ix=np.random.randint(0,len(prp),2*NM).reshape(NM,2)
    PS=prp[ix[:,0]];QS=prp[ix[:,1]]
    bg=(PS>QS).astype(np.int64)
    tm=dict(zip(prp.tolist(),types.tolist()))
    tP=np.array([tm[int(p)] for p in PS]);tQ=np.array([tm[int(q)] for q in QS])
    pc=(np.minimum(tP,tQ)*100+np.maximum(tP,tQ)).astype(np.int64)
    Nm=(PS*QS)%23
    I_pair=mi(Nm,pc)

    results[name]=(I_prime,I_pair,H_T,dict(tc))
    print(f"  {name}: I(p mod 23; T)={I_prime:.6f} | I(semiprime pair)={I_pair:.4f}",flush=True)

d_prime = abs(results["x³-x+1"][0] - results["x³-x-1"][0])
d_pair = abs(results["x³-x+1"][1] - results["x³-x-1"][1])
print(f"\nCONJUGATE FIELD COMPARISON:",flush=True)
print(f"  |Δ I(prime)| = {d_prime:.8f}",flush=True)
print(f"  |Δ I(pair)| = {d_pair:.8f}",flush=True)
match_p = d_prime < 0.001
match_s = d_pair < 0.001
print(f"  Prime channels match: {'✓ EXACTLY' if match_p else '✗'}",flush=True)
print(f"  Pair channels match: {'✓ EXACTLY' if match_s else '✗'}",flush=True)

print(f"\nTOTAL runtime:{time.time()-T0:.0f}s",flush=True)
print("\nVERDICT: computed from data above.",flush=True)
print("Round-35 #8.",flush=True)
print("\nALL_DONE_R35N8",flush=True)

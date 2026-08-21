#!/usr/bin/env python3
"""D5-HINT-VALUE — hint value for x5+20x+32 at m*=320 (round-35 #6)."""
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

print("=== D5-HINT-VALUE (round-35 #6): completing the D5 row ===",flush=True)
pf=sieve(1<<16)
prp=pf[~np.isin(pf,[2,5])]
NM=30000

coeffs=(32,20,0,0,0,1)  # x5+20x+32
nr_all=np.array([proots(coeffs,int(p)) for p in prp])
tc=Counter(nr_all.tolist())
print(f"root-count histogram: {dict(sorted(tc.items()))}",flush=True)

# D5 types: nr=5 (splits completely), nr=1 (reflection), nr=0 (rotation)
# root count uniquely determines conjugacy class for D5
types=nr_all.copy()
probs=np.array([v/len(types) for v in Counter(types.tolist()).values()])
H_T=float(-(probs*np.log2(probs)).sum())
print(f"  H(type)={H_T:.4f} bits",flush=True)

ix=np.random.randint(0,len(prp),2*NM).reshape(NM,2)
PS=prp[ix[:,0]];QS=prp[ix[:,1]]
bg=(PS>QS).astype(np.int64)
tm=dict(zip(prp.tolist(),types.tolist()))
tP=np.array([tm[int(p)] for p in PS]);tQ=np.array([tm[int(q)] for q in QS])
pc=(np.minimum(tP,tQ)*100+np.maximum(tP,tQ)).astype(np.int64)

M_STAR=320
Nm=(PS*QS)%M_STAR
sm=((PS+QS)%M_STAR).astype(np.int64)
dm=((QS-PS)%M_STAR).astype(np.int64)
sd_code=(sm*M_STAR+dm).astype(np.int64)

I_N=mi(Nm,pc)
I_sd=mi(sd_code,pc)
I_s=mi(sm,pc)
I_d=mi(dm,pc)
hint=I_sd-I_N
rng_np=np.random.default_rng(999);nl=[]
for _ in range(200):nl.append(mi(rng_np.permutation(bg),pc))
z_wall=(mi(bg,pc)-np.mean(nl))/(np.std(nl)+1e-12)

print(f"\nROUTING TABLE (m*=320):",flush=True)
print(f"  I(N mod 320; pair) = {I_N:.4f} bits",flush=True)
print(f"  sum view alone     = {I_s:.4f}",flush=True)
print(f"  gap view alone     = {I_d:.4f}",flush=True)
print(f"  (s,d) jointly      = {I_sd:.4f}",flush=True)
print(f"  HINT VALUE         = {hint:+.4f} bits",flush=True)
print(f"  which-factor wall  = {mi(bg,pc):.4f}",flush=True)
print(f"  wall z             = {z_wall:+.2f}",flush=True)

print(f"\nTOTAL runtime:{time.time()-T0:.0f}s",flush=True)
print("\nVERDICT: computed from data above.",flush=True)
print("Round-35 #6.",flush=True)
print("\nALL_DONE_R35N6",flush=True)

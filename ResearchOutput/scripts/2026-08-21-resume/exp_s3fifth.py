#!/usr/bin/env python3
"""UNIVERSAL-S3-FIFTH — x3-4x+1, disc = 229 (round-35 #2)."""
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

print("=== UNIVERSAL-S3-FIFTH (round-35 #2): x3-4x+1 ===",flush=True)
pf=sieve(1<<16)
prp=pf[pf!=229]
NM=30000

coeffs=(1,-4,0,1)  # x³-4x+1
nr_all=np.array([proots(coeffs,int(p)) for p in prp])
tc=Counter(nr_all.tolist())
print(f"\nroot-count histogram: {dict(sorted(tc.items()))}",flush=True)
types=nr_all.copy()
probs=np.array([v/len(types) for v in Counter(types.tolist()).values()])
H_T=float(-(probs*np.log2(probs)).sum())
print(f"  H(type)={H_T:.4f} bits",flush=True)

for m in (229,3,5):
    pm=(prp%m).astype(np.int64)
    v=mi(pm,types)
    rng_np=np.random.default_rng(m*100+5)
    nl=[]
    for _ in range(200):nl.append(mi(rng_np.permutation(pm),types))
    z=(v-np.mean(nl))/(np.std(nl)+1e-12)
    print(f"  I(p mod {m}; T)={v:.4f} | z={z:+.2f}",flush=True)

ix=np.random.randint(0,len(prp),2*NM).reshape(NM,2)
PS=prp[ix[:,0]];QS=prp[ix[:,1]]
tm=dict(zip(prp.tolist(),types.tolist()))
tP=np.array([tm[int(p)] for p in PS]);tQ=np.array([tm[int(q)] for q in QS])
pc=(np.minimum(tP,tQ)*100+np.maximum(tP,tQ)).astype(np.int64)
Nm=(PS*QS)%229
I_pair=mi(Nm,pc)
rng_np2=np.random.default_rng(777);nl2=[]
for _ in range(100):nl2.append(mi(rng_np2.permutation(bg),pc))
z_w=(I_pair-np.mean(nl2))/(np.std(nl2)+1e-12)
wf=mi(bg,pc)
print(f"\nSEMIPRIME:",flush=True)
print(f"  I(N mod 229; pair)={I_pair:.4f} | wall z={z_w:+.2f}",flush=True)
print(f"  which-factor wall={wf:.4f}",flush=True)

print(f"\nTOTAL runtime:{time.time()-T0:.0f}s",flush=True)
print("\nVERDICT: computed from data above.",flush=True)
print("Round-35 #2.",flush=True)
print("\nALL_DONE_R35N2",flush=True)

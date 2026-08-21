#!/usr/bin/env python3
"""D5-VERIFICATION SIMPLE — root-count-based type channel for x⁵+20x+32."""
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
        if sv[i//2]: sv[i*i//2::i]=b'\x00'*(((l-i*i)//(2*i))+1)
    return np.array([2]+[2*i+1 for i in range(1,len(sv)) if sv[i]],dtype=np.int64)

def proots(c,p):
    pp=int(p);xg=np.arange(pp,dtype=np.int64);y=np.zeros(pp,dtype=np.int64)
    for c in c_list: y=(y*xg+c)%pp
    return int(np.count_nonzero(y==0))

print("=== D5-VERIFICATION SIMPLE (round-32 #1): root-count channel ===",flush=True)
coeffs=(32,20,0,0,0,1)
c_list=list(coeffs)
pf=sieve(1<<16)
prp=pf[pf!=2]
NM=30000

# compute root counts
print("computing root counts...",flush=True)
t0=time.time()
nr_all=np.array([proots(coeffs,int(p)) for p in prp])
print(f"  done in {time.time()-t0:.0f}s",flush=True)

tc=Counter(nr_all.tolist())
print(f"  root-count histogram: {dict(sorted(tc.items()))}",flush=True)

# D₅ types: nr=5 (splits completely), nr=1 (reflection), nr=0 (rotation)
# For D₅, root count uniquely determines the conjugacy class!
types=nr_all.copy()
tc2=Counter(types.tolist())
rates={k:v/len(types) for k,v in tc2.items()}
print(f"  type rates: {dict(sorted(rates.items()))}",flush=True)

# H(label entropy)
ps_=np.array(list(tc2.values()))/len(types)
H_lab=float(-(ps_*np.log2(ps_)).sum())
print(f"  H(labels)={H_lab:.4f} bits",flush=True)

# pair channel
ix=np.random.randint(0,len(prp),2*NM).reshape(NM,2)
PS=prp[ix[:,0]];QS=prp[ix[:,1]]
bg=(PS>QS).astype(np.int64)
tP=np.array([int(p) for p in PS]) # placeholder
tm=dict(zip(prp.tolist(),types.tolist()))
tpP=np.array([tm[int(p)] for p in PS]); tpQ=np.array([tm[int(q)] for q in QS])
pc=(np.minimum(tpP,tpQ)*100+np.maximum(tpP,tpQ)).astype(np.int64)
Nm=(PS*QS)%4096000001 if False else None
# For D₅, conductor = |disc(K)| where K is the quadratic subfield
# For x⁵+20x+32, disc is a perfect square so K=Q — but that's wrong for D₅
# Actually D₅ has G^ab=C₂, and the quadratic subfield has some conductor m*
# We don't know m* analytically, so measure at multiple small moduli
for m in (3,5,7,11):
    Nm=(PS*QS)%m
    v=mi(Nm,pc)
    print(f"  I(N mod {m}; pair) = {v:.4f}",flush=True)

wf=mi(bg,pc)
print(f"  which-factor wall = {wf:.4f}",flush=True)

print(f"\nTOTAL runtime:{time.time()-T0:.0f}s",flush=True)
print("\nVERDICT: D₅ x⁵+20x+32 type-pair channel measured via root counts.",flush=True)
print("Root count uniquely determines the conjugacy class for D₅.",flush=True)
print("Round-32 #1.",flush=True)
print("\nALL_DONE_R32N1",flush=True)

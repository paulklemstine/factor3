#!/usr/bin/env python3
"""HINT-VALUE-SCALING — does hint synergy compound? (round-35 #5)."""
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

print("=== HINT-VALUE-SCALING (round-35 #5) ===",flush=True)
pf=sieve(1<<16)
RU=[31,23,2,3]
ps=pf[~np.isin(pf,RU)]
NM=30000
ix=np.random.randint(0,len(ps),2*NM).reshape(NM,2)
PS=ps[ix[:,0]];QS=ps[ix[:,1]]
bg=(PS>QS).astype(np.int64)
rng_np=np.random.default_rng(999)

# three S₃ cubics with coprime conductors
DIALS=[("S₃a@31",31,(1,1,0,1)),("S₃b@23",23,(1,-1,0,1)),("S₃c@3",3,(-3,0,0,1))]
codes_list=[]
for nm,m,c in DIALS:
    prp=ps[~np.isin(ps,[m])]
    nr=np.array([proots(c,int(p)) for p in prp])
    _,codes=np.unique(nr,return_inverse=True)
    tm=dict(zip(prp.tolist(),codes.tolist()))
    tP=np.array([tm[int(p)] for p in PS]);tQ=np.array([tm[int(q)] for q in QS])
    pc=(np.minimum(tP,tQ)*100+np.maximum(tP,tQ)).astype(np.int64)
    codes_list.append((nm,m,pc))

# s and d mod each conductor
sds=[]
for nm,m,c in DIALS:
    sm=((PS+QS)%m).astype(np.int64)
    dm=((QS-PS)%m).astype(np.int64)
    sds.append((sm,dm))

print("\nhint values for nested subsets:",flush=True)
hint_vals=[];cap_vals=[]
for kk in range(1,4):
    # product of conductors
    Mj=1
    for i in range(kk):Mj*=codes_list[i][1]
    # joint N mod M
    # CRT combine
    Nj=codes_list and (PS*QS)  # just use direct
    Nj=(PS*QS)
    for m in [codes_list[i][1] for i in range(kk)]:
        pass  # already computed below
    # Actually: N mod M_k = CRT of individual residues; but simpler to compute directly
    mods=[codes_list[i][1] for i in range(kk)]
    Mk=math.prod(mods)
    Nj_mod=(PS*QS)%Mk

    # chain the pair codes for first kk dials
    pj=codes_list[0][2].astype(np.int64)
    for i in range(1,kk):
        pj=pj*(int(max(codes_list[i][2]))+1)+codes_list[i][2]

    I_prod=mi(Nj_mod% Mk,pj)

    # hinted view: (s mod M_k, d mod M_k) jointly
    sd_code=sm13=((PS+QS)%Mk).astype(np.int64)*(Mk//math.gcd(Mk,Mk))+((QS-PS)%Mk).astype(np.int64)
    # simpler: s mod Mk and d mod Mk separately chained
    s_all=((PS+QS)%Mk).astype(np.int64)
    d_all=((QS-PS)%Mk).astype(np.int64)
    sd_chain=s_all.astype(np.int64)*(Mk+1)+d_all
    I_hinted=mi(sd_chain,pj)

    hint=I_hinted-I_prod
    hint_vals.append(hint)
    cap_vals.append(I_prod)
    print(f"  k={kk}: I(product)={I_prod:.4f} | I(s,d)={I_hinted:.4f} | hint={hint:+.4f}",flush=True)

# H2: does hint synergy compound?
if len(hint_vals)>=2:
    syn_12 = hint_vals[1]-hint_vals[0]-hint_vals[0]  # rough
print(f"\nhint value scaling: {['%+.4f'%h for h in hint_vals]}",flush=True)
deltas=[hint_vals[i+1]-hint_vals[i] for i in range(len(hint_vals)-1)]
print(f"  deltas: {['%+.4f'%d for d in deltas]}",flush=True)
print(f"  {'✓ COMPOUNDING' if all(d>0 for d in deltas) else '✗ NOT COMPOUNDING'}",flush=True)

print(f"\nTOTAL runtime:{time.time()-T0:.0f}s",flush=True)
print("\nVERDICT: computed from data above.",flush=True)
print("Round-35 #5.",flush=True)
print("\nALL_DONE_R35N5",flush=True)

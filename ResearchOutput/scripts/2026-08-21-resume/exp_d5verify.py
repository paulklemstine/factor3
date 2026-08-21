#!/usr/bin/env python3
"""D5-VERIFICATION — rigorous Galois group computation for the D₅ quintics (round-32 #1).

Paper 84 found four quintics with the Chebotarev-histogram signature of D₅.
This round verifies them RIGOROUSLY using sympy's galois_group function,
then measures the type-pair channel for the best-verified candidate.
"""
import math, time, random
import numpy as np
random.seed(20260821); np.random.seed(20260821); T0=time.time()

from sympy import Poly, symbols, discriminant
from sympy.combinatorics.galois import *
x = symbols('x')

print("=== D5-VERIFICATION (round-32 #1) ===", flush=True)

CANDIDATES = [
    ("x⁵+11x-44", 11, -44),
    ("x⁵+11x+44", 11, 44),
    ("x⁵+20x-32", 20, -32),
    ("x⁵+20x+32", 20, 32),
]

for name, a, b in CANDIDATES:
    poly = Poly(x**5 + a*x + b, x)
    d = discriminant(poly)
    is_sq = int(round(math.isqrt(abs(d))))**2 == abs(d) if d != 0 else True
    try:
        from sympy import factor_list
        _, facs = factor_list(poly.as_expr())
        n_facs = len(facs)
    except:
        n_facs = -1
    irred = (n_facs == 1)
    gal = None
    try:
        from sympy.polys.numberfields import galois_group
        G, alt = galois_group(poly)
        gal = f"order {G.order()}, alt={alt}"
    except Exception as e:
        gal = f"(galois_group unavailable: {e})"
    print(f"  {name}: disc={d} ({'square ✓' if is_sq else 'NOT square ✗'}), "
          f"irreducible={'✓' if irred else '✗'}, Gal={gal}", flush=True)

# ---------------------------------------------------------------------------
# measure type-pair channel for x⁵+20x+32
# ---------------------------------------------------------------------------
print("\nMeasuring type-pair channel for x⁵+20x+32...", flush=True)

def odd_sieve(limit):
    sv=bytearray(b'\x01')*(limit//2); sv[0]=0; im=int(math.isqrt(limit))
    for i in range(3,im+1,2):
        if sv[i//2]: sv[i*i//2::i]=b'\x00'*(((limit-i*i)//(2*i))+1)
    return np.array([2]+[2*i+1 for i in range(1,len(sv)) if sv[i]],dtype=np.int64)

def proots(c,p):
    pp=int(p); xg=np.arange(pp,dtype=np.int64); y=np.zeros(pp,dtype=np.int64)
    for cc in c: y=(y*xg+cc)%pp
    return int(np.count_nonzero(y==0))

def mi(x,y):
    k,inv=np.unique(x,return_inverse=True); yl,yinv=np.unique(y,return_inverse=True)
    idx=inv.astype(np.int64)*len(yl)+yinv
    cnt=np.bincount(idx,minlength=len(k)*len(yl)).reshape(len(k),len(yl)).astype(float)
    tot=cnt.sum()
    if tot==0: return 0.0
    pxy=cnt/tot; px=pxy.sum(1,keepdims=True); py=pxy.sum(0,keepdims=True)
    with np.errstate(divide='ignore',invalid='ignore'): mm=pxy*np.log2(pxy/(px*py))
    mm[pxy==0]=0; return float(mm.sum())

pool_full=odd_sieve(1<<16)
RAM=[2]
ps=pool_full[~np.isin(pool_full,RAM)]
NM=30000
ix=np.random.randint(0,len(ps),2*NM).reshape(NM,2)
PS=ps[ix[:,0]]; QS=ps[ix[:,1]]
bg=(PS>QS).astype(np.int64)
rng_np=np.random.default_rng(555)

coeffs=(-32 if False else -32,20,0,0,0,1) if False else (-32, 20, 0, 0, 0, 1)
# actually use b=-32? No — use +32 since that's one of our candidates
coeffs=(32, 20, 0, 0, 0, 1)  # x⁵+20x-32... wait

# let me just use x⁵+20x+32
coeffs=(32, 20, 0, 0, 0, 1)  # const-first: 32 + 20x + x⁵

prp=ps[~np.isin(ps,[2])]
types=[]
D5_DICT={(5,5):'11111',(1,1):'14',(1,5):'122',(0,0):'5'}
flit=list(coeffs)[::-1]  # little-endian
def polymulmod(a,b,f,p):
    res=[0]*(len(a)+len(b)-1)
    for i,ai in enumerate(a):
        if ai:
            for j,bj in enumerate(b):
                if bj: res[i+j]+=ai*bj
    n=len(f)-1
    for i in range(len(res)-1,n-1,-1):
        cc=res[i]%p
        if cc:
            for j in range(n+1): res[i-n+j]-=cc*f[j]
    return [v%p for v in res[:n]]

import time as _t
t0=_t.time()
for p in prp:
    pp=int(p)
    nr=proots(coeffs,pp)
    # compute x^{p²} mod f
    result=[1];base=[0,1]
    e=pp*pp
    while e:
        if e&1:
            res=[0]*(len(result)+len(base)-1)
            for i,ai in enumerate(result):
                if ai:
                    for j,bj in enumerate(base):
                        if bj: res[i+j]+=ai*bj
            n=len(flit)-1
            for i in range(len(res)-1,n-1,-1):
                c=res[i]%pp
                if c:
                    for j in range(n+1): res[i-n+j]-=c*flit[j]
            result=[v%pp for v in res[:n]]
        e>>=1
        if e:
            res=[0]*(len(base)+len(base)-1)
            for i,ai in enumerate(base):
                if ai:
                    for j,bj in enumerate(base):
                        if bj: res[i+j]+=ai*bj
            n=len(flit)-1
            for i in range(len(res)-1,n-1,-1):
                c=res[i]%pp
                if c:
                    for j in range(n+1): res[i-n+j]-=cc*flit[j]
            base=[v%pp for v in res[:n]]
    while len(result)<2: result.append(0)
    result[1]=(result[1]-1)%pp
    nr2=polygcd_deg(flit,result,pp)
    t={(5,5):'11111',(1,1):'14',(1,5):'122',(0,0):'5'}.get((nr,nr2))
    if t is None: raise ValueError(f"readout p={pp} ({nr},{nr2})")
    types.append(t)

print(f"  scanned {len(prp)} primes in {_t.time()-t0:.0f}s",flush=True)

tc=Counter(types)
print(f"  type histogram: {dict(tc)}",flush=True)

N_mod=(PS*QS)%5
tP=np.zeros(NM,dtype=np.int64)  # placeholder — need tmap
# Actually build properly
tp_arr=np.array(types)
_,codes=np.unique(tp_arr,return_inverse=True)
tmap=dict(zip(prp.tolist(),codes.tolist()))
tpP=np.array([tmap[int(p)] for p in PS])
tpQ=np.array([tmap[int(q)] for q in QS])
pc=(np.minimum(tpP,tpQ)*1000+np.maximum(tpP,tpQ)).astype(np.int64)
Nm=(PS*QS)%5
I_pair=mi(Nm,pc)
nl=[]
for _ in range(100): nl.append(mi(rng_np.permutation(bg),pc))
z_w=(mi(bg,pc)-np.mean(nl))/(np.std(nl)+1e-12)
print(f"  I(N mod 5; pair) = {I_pair:.4f}",flush=True)
print(f"  wall z = {z_w:+.2f}",flush=True)

print(f"\nTOTAL runtime:{time.time()-T0:.0f}s",flush=True)
print("\nALL_DONE_R32N1",flush=True)

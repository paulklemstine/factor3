#!/usr/bin/env python3
"""HINT-TABLE-COMPLETION (round-30 #1): hint values for all six dials.
SIMPLEST CORRECT: root count (or ord) as the label for each dial."""
import math,time,random
import numpy as np
random.seed(20260821); np.random.seed(20260821); T0=time.time()

def contingency_mi(x,y):
    k,inv=np.unique(x,return_inverse=True)
    yl,yinv=np.unique(y,return_inverse=True)
    idx=inv.astype(np.int64)*len(yl)+yinv
    cnt=np.bincount(idx,minlength=len(k)*len(yl)).reshape(len(k),len(yl)).astype(float)
    tot=cnt.sum()
    if tot==0: return 0.0
    pxy=cnt/tot; px=pxy.sum(1,keepdims=True); py=pxy.sum(0,keepdims=True)
    with np.errstate(divide='ignore',invalid='ignore'): mm=pxy*np.log2(pxy/(px*py))
    mm[pxy==0]=0; return float(mm.sum())

def odd_sieve(limit):
    sv=bytearray(b'\x01')*(limit//2); sv[0]=0; im=int(math.isqrt(limit))
    for i in range(3,im+1,2):
        if sv[i//2]: sv[i*i//2::i]=b'\x00'*(((limit-i*i)//(2*i))+1)
    return np.array([2]+[2*i+1 for i in range(1,len(sv)) if sv[i]],dtype=np.int64)

def poly_roots(coeffs,p):
    pp=int(p); xg=np.arange(pp,dtype=np.int64); y=np.zeros(pp,dtype=np.int64)
    for c in coeffs: y=(y*xg+c)%pp
    return int(np.count_nonzero(y==0))

print("=== HINT-TABLE-COMPLETION (round-30 #1) ===",flush=True)
pool_full=odd_sieve(1<<16)
RAM_UNION=[31,23,2,3,5,11]
pool_shared=pool_full[~np.isin(pool_full,RAM_UNION)]
N_MC=30000
idx=np.random.randint(0,len(pool_shared),2*N_MC).reshape(N_MC,2)
P_SHARED=pool_shared[idx[:,0]]; Q_SHARED=pool_shared[idx[:,1]]
bigger=(P_SHARED>Q_SHARED).astype(np.int64)
rng_np=np.random.default_rng(999)
results=[]

def measure(name,type_fn,mstar,exclude):
    prp=pool_shared[~np.isin(pool_shared,exclude)]
    tp=type_fn(prp)
    _,codes=np.unique(tp,return_inverse=True)
    tmap=dict(zip(prp.tolist(),codes.tolist()))
    tpP=np.array([tmap[int(p)] for p in P_SHARED])
    tpQ=np.array([tmap[int(q)] for q in Q_SHARED])
    pc=(np.minimum(tpP,tpQ)*1000+np.maximum(tpP,tpQ)).astype(np.int64)
    N_mod=(P_SHARED*Q_SHARED)%mstar
    s_mod=((P_SHARED+Q_SHARED)%mstar).astype(np.int64)
    d_mod=((Q_SHARED-P_SHARED)%mstar).astype(np.int64)
    sd_code=(s_mod*mstar+d_mod).astype(np.int64)
    I_N=contingency_mi(N_mod,pc); I_sd=contingency_mi(sd_code,pc)
    hint=I_sd-I_N
    obs_w=contingency_mi(bigger,sd_code); nl=[]
    for _ in range(100): nl.append(contingency_mi(rng_np.permutation(bigger),sd_code))
    z_w=(obs_w-np.mean(nl))/(np.std(nl)+1e-12)
    ntypes=len(set(tp.tolist()))
    print(f"  {name}: I(N)={I_N:.4f} | I(s,d)={I_sd:.4f} | HINT={hint:+.4f} | wall z={z_w:+.2f} | types={ntypes}",flush=True)
    assert abs(z_w)<3 and hint>0
    results.append(dict(name=name,I_N=I_N,hint=hint))

# S₃a@31
prp=pool_shared[pool_shared!=31]
measure("S₃a@31",lambda pr:np.array([poly_roots((1,1,0,1),int(p)) for p in pr]),31,[31])
# S₃b@23
prp=pool_shared[pool_shared!=23]
measure("S₃b@23",lambda pr:np.array([poly_roots((1,-1,0,1),int(p)) for p in pr]),23,[23])
# A₄@9
prp=pool_shared[~np.isin(pool_shared,[2,3])]
measure("A₄@9",lambda pr:np.array([poly_roots((12,8,0,0,0,1),int(p)) for p in pr]),9,[2,3])
# D₄@8
prp=pool_shared[pool_shared!=2]
measure("D₄@8",lambda pr:np.array([int(p)%8 for p in pr]),8,[2])
# F₂₀@5
prp=pool_shared[pool_shared!=5]
measure("F₂₀@5",lambda pr:np.array([poly_roots((-2,0,0,0,0,1),int(p)) for p in pr]),5,[5])
# C₅@11
def ord11(a):
    x,o=a%11,1
    while x!=1: x=x*a%11;o+=1
    return o
prp=pool_shared[pool_shared!=11]
measure("C₅@11",lambda pr:np.array([ord11(int(p)) for p in pr]),11,[11])

print("\nTHE COMPLETED SIX-DIAL HINT-VALUE TABLE:",flush=True)
all_r=sorted(results,key=lambda d:-d['hint'])
for r in all_r:
    print(f"  {r['name']:>8}: hint={r['hint']:+.4f} bits | capacity={r['I_N']:.4f} bits",flush=True)
tot_h=sum(r['hint'] for r in all_r); tot_c=sum(r['I_N'] for r in all_r)
corr=float(np.corrcoef([r['hint'] for r in all_r],[r['I_N'] for r in all_r])[0,1])
print(f"  TOTAL: hint={tot_h:.4f}, capacity={tot_c:.4f}",flush=True)
print(f"  hint-capacity correlation: r={corr:.3f}",flush=True)
assert all(r['hint']>0 for r in results),'negative hint!'
print(f"\nTOTAL runtime:{time.time()-T0:.0f}s",flush=True)
print("\nVERDICT: ALL SIX dials show positive hint values.",flush=True)
print("Round-30 #1.",flush=True)
print("\nALL_DONE_R30N1B",flush=True)

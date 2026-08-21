#!/usr/bin/env python3
"""RAMIFIED-TYPE-CHANNEL — do ramified primes carry extra info? (round-36 #1)."""
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

print("=== RAMIFIED-TYPE-CHANNEL (round-36 #1) ===",flush=True)

# x²−3: ramified at {2,3}, disc = 12
# unramified odd primes ≠ 3: nr = 0 or 2 (split/inert by quadratic character)
# ramified p=2: x²−3 ≡ x²+1 ≡ (x+1)² → nr=1 (double root)
# ramified p=3: x²−3 ≡ x² mod 3 → double root at 0 → nr=1

pf=sieve(1<<16)

# ALL primes including ramified
all_primes=pf[~np.isin(pf,[1])]
nr_all_all=np.array([proots((-3,0,1),int(p)) for p in all_primes])

# unramified only
unram_mask=~np.isin(all_primes,[2,3])
nr_unram=nr_all_all[unram_mask]
pr_unram=all_primes[unram_mask]

# separate ramified
ram_mask=~unram_mask
nr_ram=nr_all_all[ram_mask]
pr_ram=all_primes[ram_mask]

print(f"\nunramified primes: {unram_mask.sum()}",flush=True)
tc_u=Counter(nr_unram.tolist())
print(f"  types: {dict(sorted(tc_u.items()))}",flush=True)
print(f"\nramified primes: {ram_mask.sum()}",flush=True)
tc_r=Counter(nr_all_all[ram_mask].tolist())
print(f"  types: {dict(sorted(tc_r.items()))}",flush=True)

# measure MI for each group separately and combined
pm_all=(all_primes%12).astype(np.int64)
types_all=nr_all_all.copy()

I_all=mi(pm_all,types_all)
I_unram=mi(pm_all[unram_mask],types_all[unram_mask])
I_ram=mi(pm_all[ram_mask],types_all[ram_mask])
H_T_all=float(-(np.array([v/len(types_all) for v in Counter(types_all.tolist()).values()])*np.log2(np.array([v/len(types_all) for v in Counter(types_all.tolist()).values()]))).sum())

print(f"\nCHANNEL CAPACITIES:",flush=True)
print(f"  I(p mod 12; T) all primes = {I_all:.4f}",flush=True)
print(f"  I(p mod 12; T) unramified = {I_unram:.4f}",flush=True)
print(f"  I(p mod 12; T) ramified   = {I_ram:.4f}",flush=True)

# permutation null on the full set
rng_np=np.random.default_rng(999);nl=[]
for _ in range(200):nl.append(mi(rng_np.permutation(pm_all),types_all))
z_all=(I_all-np.mean(nl))/(np.std(nl)+1e-12)
print(f"  wall z (all) = {z_all:+.2f}",flush=True)

# H(T) for reference
probs_t=np.array([v/len(types_all) for v in Counter(types_all.tolist()).values()])
H_T_ref=float(-(probs_t*np.log2(probs_t)).sum())
print(f"  H(T)={H_T_ref:.4f} bits",flush=True)

# SEMIPRIME level with and without ramified primes
ix=np.random.randint(0,len(all_primes),2*30000).reshape(30000,2)
PS_all=all_primes[ix[:,0]];QS_all=all_primes[ix[:,1]]
bg_all=(PS_all>QS_all).astype(np.int64)
tm=dict(zip(all_primes.tolist(),types_all.tolist()))
tP=np.array([tm[int(p)] for p in PS_all]);tQ=np.array([tm[int(q)] for q in QS_all])
pc=(np.minimum(tP,tQ)*100+np.maximum(tP,tQ)).astype(np.int64)
Nm=(PS_all*QS_all)%12

I_pair_with=mi(Nm,pc)
nl_pair=[]
for _ in range(100):nl_pair.append(mi(rng_np.permutation(bg),pc))
z_pair=(I_pair_with-np.mean(nl_pair))/(np.std(nl_pair)+1e-12)
print(f"\nSEMIPRIME:",flush=True)
print(f"  I(N mod 12; pair)={I_pair_with:.4f} | null {np.mean(nl_pair):.4f} | z={z_pair:+.2f}",flush=True)
print(f"  which-factor wall={mi(bg,pc):.4f}",flush=True)

print(f"\nTOTAL runtime:{time.time()-T0:.0f}s",flush=True)
print("\nVERDICT: computed from data above.",flush=True)
print("Round-36 #1.",flush=True)
print("\nALL_DONE_R36N1",flush=True)

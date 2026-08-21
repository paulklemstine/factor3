#!/usr/bin/env python3
"""TRACE-BATTERY — the 6-dial joint trace capacity (round-30 #4).

How much information about the trace s = p+q does the full 6-dial battery
carry jointly, beyond what any single dial provides?
"""
import math,time,random
import numpy as np
random.seed(20260821); np.random.seed(20260821); T0=time.time()
def mi(x,y):
    k,inv=np.unique(x,return_inverse=True); yl,yinv=np.unique(y,return_inverse=True)
    idx=inv.astype(np.int64)*len(yl)+yinv
    cnt=np.bincount(idx,minlength=len(k)*len(yl)).reshape(len(k),len(yl)).astype(float)
    tot=cnt.sum()
    if tot==0: return 0.0
    pxy=cnt/tot; px=pxy.sum(1,keepdims=True); py=pxy.sum(0,keepdims=True)
    with np.errstate(divide='ignore',invalid='ignore'): mm=pxy*np.log2(pxy/(px*py))
    mm[pxy==0]=0; return float(mm.sum())
def sieve(l):
    sv=bytearray(b'\x01')*(l//2); sv[0]=0; im=int(math.isqrt(l))
    for i in range(3,im+1,2):
        if sv[i//2]: sv[i*i//2::i]=b'\x00'*(((l-i*i)//(2*i))+1)
    return np.array([2]+[2*i+1 for i in range(1,len(sv)) if sv[i]],dtype=np.int64)
def proots(c,p):
    pp=int(p); xg=np.arange(pp,dtype=np.int64); y=np.zeros(pp,dtype=np.int64)
    for cc in c: y=(y*xg+cc)%pp
    return int(np.count_nonzero(y==0))

print("=== TRACE-BATTERY (round-30 #4): the 6-dial joint trace capacity ===",flush=True)
pf=sieve(1<<16); RU=[31,23,2,3,5,11]
ps=pf[~np.isin(pf,RU)]; NM=30000
ix=np.random.randint(0,len(ps),2*NM).reshape(NM,2)
PS=ps[ix[:,0]]; QS=ps[ix[:,1]]
bg=(PS>QS).astype(np.int64); rng=np.random.default_rng(555)

# build all six dial codes on the same population
def cubic_codes(coeffs,m,ex):
    prp=ps[~np.isin(ps,ex)]
    tp=np.array([proots(coeffs,int(p)) for p in prp])
    _,codes=np.unique(tp,return_inverse=True)
    tm=dict(zip(prp.tolist(),codes.tolist()))
    tP=np.array([tm[int(p)] for p in PS]); tQ=np.array([tm[int(q)] for q in QS])
    return (np.minimum(tP,tQ)*100+np.maximum(tP,tQ)).astype(np.int64)

codes_a=cubic_codes((1,1,0,1),31,[31])
codes_b=cubic_codes((1,-1,0,1),23,[23])
codes_c=cubic_codes((-2,0,0,0,0,1),5,[5])   # F₂₀ quintic root count @5
codes_d=(PS*QS)%9                             # A₄@9 product residue
codes_e=(PS*QS)%8                             # D₄@8 product residue
codes_f=(PS+QS)%11                            # C₅@11 sum residue

s_mod=(PS+QS)%51336  # M = 31·23·9·8·5·11 / (some factors)... actually use each separately

# per-dial I(s mod mᵢ; codeᵢ)
DIALS=[("S₃a@31",31,codes_a),("S₃b@23",23,codes_b),
       ("A₄@9",9,codes_d),("D₄@8",8,codes_e),
       ("F₂₀@5",5,codes_c),("C₅@11",11,codes_f)]

print("\nper-dial I(s mod mᵢ; codeᵢ):",flush=True)
for nm,m,c in DIALS:
    sm=(PS+QS)%m
    v=mi(sm,c)
    print(f"  {nm}: {v:.4f}",flush=True)

# joint: CRT-combine all six residues into one trace-residue vector
# M_joint = 31·23·9·8·5·11 = 1131755... but we only have 30k samples
# so the joint is EXTREMELY sparse — use a subset of moduli instead
# Use the three largest: 31, 23, and 9 → M = 6417
for mods,names in [([31,23],"S₃a+S₃b"), ([31,23,9],"S₃a+S₃b+A₄"),
                   ([31,23,9,8],"S₃a+S₃b+A₄+D₄")]:
    Mj=1
    joint_codes=[]
    for m in mods:
        Mj*=m
    # CRT-combine the residues
    Nj=PS.copy(); cur=1
    for m in mods:
        # N mod m combined with current N mod cur
        inv=pow(cur,-1,m) if cur>1 else 0
        if cur==1:
            Nj=PS%m
        else:
            pass
        cur*=m
    # simpler: just compute N mod M directly
    if len(mods)==2:
        Mj=mods[0]*mods[1]
        Nj=(PS*QS)%Mj
    elif len(mods)==3:
        Mj=mods[0]*mods[1]*mods[2]
        Nj=(Pp if False else PS)*(QS if False else QS)%Mj if False else (PS if False else PS*QS)%np.prod(mods,dtype=np.int64)
        Mj=int(np.prod(mods))
        Nj=(PS*QS)%np.int64(Mj)
    else:
        Mj=int(np.prod(mods))
        Nj=(PS*QS)%np.int64(Mj)

    # chain all six codes
    lab=codes_a.astype(np.int64)
    for c in (codes_b,codes_d,codes_e,codes_c,codes_f):
        lab=lab*(int(max(c))+1)+c

    I_joint=mi(Nj%np.int64(Mj),lab)
    print(f"\n  joint over moduli {names}: M={Mj}, "
          f"I(N mod M; all codes) = {I_joint:.4f}", flush=True)

# per-dial reference values at their individual moduli
print("\nper-dial reference:",flush=True)
tot_ref=0
for nm,m,c in DIALS:
    sm=(PS+QS)%m
    v=mi(sm,c)
    tot_ref=max(tot_ref,v)
    print(f"  {nm}: I(s mod {m}; code) = {v:.4f}",flush=True)

# the KEY measurement: I(s mod 713; both codes jointly) — extending paper 99's finding
sm713=(PS+QS)%713
I_s_713_both=mi(sm713,np.minimum(codes_a,codes_b).astype(np.int64)*100+
                np.maximum(codes_a,codes_b).astype(np.int64))
print(f"\n  I(s mod 713; S₃a+S₃b codes jointly) = {I_s_713_both:.4f}",flush=True)
print(f"  vs per-dial sum: {mi((PS+QS)%31,codes_a)+mi((PS+QS)%23,codes_b):.4f}",flush=True)

wf_all=mi(bg,lab)
print(f"  which-factor wall (all codes) = {wf_all:.4f}",flush=True)

print(f"\nTOTAL runtime:{time.time()-T0:.0f}s",flush=True)
print("\nVERDICT: computed from data above.",flush=True)
print("Round-30 #4.",flush=True)
print("\nALL_DONE_R30N4",flush=True)

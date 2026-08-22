#!/usr/bin/env python3
# EXP 462 ADDENDUM: clean-modulus channels from cached type vectors.
# LEDGER-15 (resolved scare): ray-class C3 data seemed visible via Artin map
# on principal ideal (p); dihedral cancellation chi(P)*chi(Pbar)^-1 = 1 makes
# it invisible -- theory intact: only the sign character is residue-visible.
# LEDGER-16: rev4's legendre display disagreed with sympy-perfect types;
# rechecked here against cache.
import json, math
import numpy as np
from collections import Counter

SEED = 20260821
def h(ps): return -sum(p*math.log2(p) for p in ps if p>0)
def mi(xs, ys):
    n=len(xs); cx,cy,cj=Counter(xs),Counter(ys),Counter(zip(xs,ys))
    return h(v/n for v in cx.values())+h(v/n for v in cy.values())-h(v/n for v in cj.values())
def nullmi(x,y,nsh,seed):
    r=np.random.default_rng(seed); x=np.asarray(x)
    v=[mi(x[r.permutation(len(x))],y) for _ in range(nsh)]
    return float(np.mean(v)),float(np.std(v))

z = np.load("/tmp/exp37_overlap/types_cache.npz")
POLY = {"P0a":(-5,-5,-175),"P0b":(-3,-5,-567),
        "P1a":(-5,5,-175),"P1b":(-3,5,-567),
        "P2a":(3,-2,-216),"P2b":(-6,-8,-864),
        "P3a":(-6,-6,-108),"P3b":(0,-3,-243),
        "K1":(1,1,-31),"K2":(-1,-1,-23),
        "Cj1":(-1,-1,-23),"Cj2":(-1,1,-23)}
TV={t:z[t] for t in POLY}; n_pr=len(TV["P0a"])

LIM=2**21
sv=np.ones(LIM+1,dtype=bool); sv[:2]=False
for i in range(2,int(LIM**0.5)+1):
    if sv[i]: sv[i*i::i]=False
pr=np.flatnonzero(sv).astype(np.int64)
ram=set()
for a,b,d in POLY.values():
    n=abs(d); q=2
    while q*q<=n:
        while n%q==0: ram.add(q); n//=q
        q+=1
    if n>1: ram.add(n)
P=pr[(~np.isin(pr,list(ram)))&(pr>10000)]
assert len(P)==n_pr

print("Legendre cross-checks (scorer fixed, LEDGER-16):")
for t,(a,b,d) in POLY.items():
    ok=0;n=0
    for i in range(0,n_pr,397):
        p=int(P[i]); ls=pow(d%p,(p-1)//2,p)
        pred12 = (ls==p-1)
        ok += int(pred12 == (TV[t][i]==1)); n+=1
    print(f"  {t}: {ok}/{n}")

TYPES=("111","12","3")
rng=np.random.default_rng(SEED)
pool=pr[(pr>=2**15)&(pr<=2**17)&(~np.isin(pr,list(ram)))]
pp=pool[rng.integers(0,len(pool),30000)]; qq=pool[rng.integers(0,len(pool),30000)]
Nsp=pp*qq
ip=np.searchsorted(P,pp); iq=np.searchsorted(P,qq)

def upair(t,i_,j_):
    x,y=TYPES[TV[t][i_]],TYPES[TV[t][j_]]
    return f"{min(x,y)}|{max(x,y)}"
Ua_of=lambda t:[upair(t,i,j) for i,j in zip(ip,iq)]

def channels(ta,tb,m):
    Ua=Ua_of(ta); Ub=Ua_of(tb)
    Uj=[f"{u}>{v}" for u,v in zip(Ua,Ub)]
    x=[int(v)%m for v in Nsp]
    ia=mi(x,Ua); ib=mi(x,Ub); ij=mi(x,Uj)
    na,sa=nullmi(x,Ua,150,11); nb,sb=nullmi(x,Ub,150,13); nj,sj=nullmi(x,Uj,250,17)
    brg=np.random.default_rng(29); devs=[]
    ar=np.arange(30000)
    for _ in range(200):
        ii=brg.choice(ar,30000,replace=True)
        devs.append(mi([x[t] for t in ii],[Ua[t] for t in ii])
                    +mi([x[t] for t in ii],[Ub[t] for t in ii])
                    -mi([x[t] for t in ii],[f"{Ua[t]}>{Ub[t]}" for t in ii]))
    bm,bs=float(np.mean(devs)),float(np.std(devs))
    return ia,ib,ij,(na,sa,nb,sb,nj,sj),(bm,bs)

print("\n=== CLEAN SIGN-DIAL MODULUS ===")
res={}
pairs={"pair0":("P0a","P0b",7),"pair1":("P1a","P1b",7),
       "pair2_samefield":("P2a","P2b",6),"pair3":("P3a","P3b",3),
       "conjugate_ctrl":("Cj1","Cj2",23)}
for name,(ta,tb,d) in pairs.items():
    m=d
    ia,ib,ij,nulls,(bm,bs)=channels(ta,tb,m)
    dev=(ia+ib-1.0)-ij
    lo,hi=bm-1.0-2*bs,bm-1.0+2*bs
    verdict="H1-OK" if (abs(dev)<0.02 or lo<=0<=hi) else "DEVIANT"
    na,sa,nb,sb,nj,sj=nulls
    print(f"[{name}] m={m}  I_a={ia:.4f}(null {na:.3f}+-{sa:.3f})  "
          f"I_b={ib:.4f}(null {nb:.3f}+-{sb:.3f})  JOINT={ij:.4f}(null {nj:.3f}+-{sj:.3f})")
    print(f"   deficit={ia+ib-ij:+.4f}  pred +1.0000  dev {dev:+.4f}  bootCI[{lo:+.4f},{hi:+.4f}] -> {verdict}",flush=True)
    res[name]=dict(m=m,Ia=ia,Ib=ib,J=ij,deficit=ia+ib-ij,dev=dev,boot=(bm,bs))

# coprime control at its natural lcm 713 (42/cell, healthy)
ia,ib,ij,nulls,(bm,bs)=channels("K1","K2",713)
dev=(ia+ib-(-0.129))-ij
lo,hi=bm+0.129-2*bs,bm+0.129+2*bs
na,sa,nb,sb,nj,sj=nulls
print(f"[coprime_ctrl] m=713  I_a={ia:.4f}  I_b={ib:.4f}  JOINT={ij:.4f}")
print(f"   deficit={ia+ib-ij:+.4f}  pred -0.129  dev {dev:+.4f}  bootCI[{lo:+.4f},{hi:+.4f}]")
res["coprime_ctrl"]=dict(m=713,Ia=ia,Ib=ib,J=ij,deficit=ia+ib-ij,pred=-0.129,boot=(bm,bs))

print("\n=== which-factor wall @ m=3 (pair3) ===")
ap=[TYPES[TV['P3a'][i]] for i in ip]; aq=[TYPES[TV['P3a'][i]] for i in iq]
bp=[TYPES[TV['P3b'][i]] for i in ip]; bq=[TYPES[TV['P3b'][i]] for i in iq]
ordl=[f"{w}{x}{y}{zz}" for w,x,y,zz in zip(ap,bp,aq,bq)]
unord=[f"{min(a,c)}|{max(a,c)}>{min(b,d)}|{max(b,d)}" for a,b,c,d in zip(ap,aq,bp,bq)]
x=[int(v)%3 for v in Nsp]
io,iu=mi(x,ordl),mi(x,unord)
rgs=np.random.default_rng(23); dl=[]
for _ in range(250):
    pm=rgs.permutation(30000)
    dl.append(mi([x[t] for t in pm],ordl)-mi([x[t] for t in pm],unord))
dm,ds=float(np.mean(dl)),float(np.std(dl))
zw=((io-iu)-dm)/max(ds,1e-9)
print(f"I(ord)={io:.4f} I(unord)={iu:.4f} delta={io-iu:+.4f} null {dm:+.4f}+-{ds:.4f} z={zw:+.2f} "
      f"-> {'NULL (factor-blind)' if abs(zw)<3 else 'EXCESS'}")
wf=dict(delta=io-iu,null=dm,sd=ds,z=zw)

with open("/tmp/exp37_overlap/result_addendum.json","w") as f:
    json.dump(dict(sign_modulus=res,which_factor_m3=wf),f,default=float)
print("\naddendum json written")

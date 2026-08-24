#!/usr/bin/env python3
"""exp550 DEPTH-DECAY (round-70 #4, coordinator inline): does the exp546 magnitude
channel see Berggren letters beyond the first step?
Targets: letter at depth t unconditional AND conditioned on the path prefix
(within-prefix permutation shuffles); MI(feature; dB). Data: exp546_data.npz."""
import numpy as np, json, time
from collections import Counter
t0=time.time()
d=np.load('ResearchOutput/scripts/2026-08-21-resume/exp546_data.npz',allow_pickle=True)
P,Q=d['P'],d['Q']
m=(P+Q)//2; n=(Q-P)//2

def letters(mm,nn):
    L=[]
    while not (mm==2 and nn==1):
        r=mm/nn
        if r<2: L.append(1); mm,nn=nn,2*nn-mm
        elif r<3: L.append(2); mm,nn=nn,mm-2*nn
        else: L.append(3); mm,nn=mm-2*nn,nn
    return L
strs=[letters(int(a),int(b)) for a,b in zip(m,n)]
dB=np.array([len(s) for s in strs])
def ascend(s):
    mm,nn=2,1
    for L in reversed(s):
        if L==1: mm,nn=2*mm-nn,mm
        elif L==2: mm,nn=2*mm+nn,mm
        else: mm,nn=mm+2*nn,nn
    return mm,nn
ok=sum(ascend(s)==(int(a),int(b)) for s,(a,b) in zip(strs,zip(m,n)))
print("re-ascent exact:",ok,"/",len(strs))

feat=d['x_f1_w4096_hratio']
def mi(xb,y):
    c_xy=Counter(zip(xb.tolist(),y.tolist())); c_x=Counter(xb.tolist()); c_y=Counter(y.tolist())
    N=len(xb)
    return sum(p*np.log2(p/((c_x[a]/N)*(c_y[b]/N))) for (a,b),k in c_xy.items() for p in [k/N])
bins=np.quantile(feat,np.linspace(0,1,13)); xb=np.clip(np.digitize(feat,bins[1:-1]),0,11)
rng=np.random.default_rng(5)

res={}
print("t | n_rows | MI_uncond | null_z")
for t in range(1,9):
    msk=dB>=t
    y=np.array([s[t-1] for s in strs])[msk]; x=xb[msk]
    I=mi(x,y); nl=[mi(rng.permutation(x),y) for _ in range(150)]
    z=(I-np.mean(nl))/np.std(nl)
    res[t]=(int(msk.sum()),round(I,4),round(float(z),1))
    print(f"{t} | {msk.sum()} | {I:.4f} | {z:+.1f}")

cond={}
print("t | MI_cond_prefix | within-prefix null mean")
for t in range(2,6):
    y=np.array([s[t-1] for s in strs]); x=xb.copy()
    groups={}
    for i,s in enumerate(strs):
        if dB[i]>=t: groups.setdefault(tuple(s[:t-1]),[]).append(i)
    big={k:np.array(v) for k,v in groups.items() if len(v)>=60}
    N=sum(len(v) for v in big.values())
    Ic=sum(mi(x[v],y[v])*(len(v)/N) for v in big.values())
    nulls=[]
    for _ in range(60):
        xs=x.copy()
        for v in big.values(): xs[v]=x[rng.permutation(v)]
        nulls.append(sum(mi(xs[v],y[v])*(len(v)/N) for v in big.values()))
    cond[t]=(round(Ic,4),round(float(np.mean(nulls)),4),round(float((Ic-np.mean(nulls))/max(np.std(nulls),1e-9)),1))
    print(f"{t} | {Ic:.4f} | {np.mean(nulls):.4f} (sd {np.std(nulls):.4f}, z {cond[t][2]:+.1f})")

dbb=np.clip(np.digitize(dB,np.quantile(dB,np.linspace(0,1,13))[1:-1]),0,11)
I=mi(xb,dbb); nl=[mi(rng.permutation(xb),dbb) for _ in range(150)]
z=(I-np.mean(nl))/np.std(nl)
cf=float(np.corrcoef(feat,np.log(dB))[0,1])
print(f"MI(feature; dB 12-bin) = {I:.4f} z={z:+.1f}; corr(feat, log dB) = {cf:.3f}")
json.dump({"reascent_exact":int(ok),"n":len(strs),"seed_pop":"20260823-reuse","feature":"x_f1_w4096_hratio",
 "mi_bt_uncond":{str(k):v for k,v in res.items()},
 "mi_bt_cond_prefix_z":{str(k):v[2] for k,v in cond.items()},
 "mi_bt_cond_prefix_full":{str(k):v for k,v in cond.items()},
 "mi_dB_bin":round(I,4),"mi_dB_bin_z":round(float(z),1),"corr_feat_logdB":round(cf,3),
 "wall_s":round(time.time()-t0,1)},
 open('ResearchOutput/scripts/2026-08-21-resume/exp550_depthdecay.json','w'),indent=1)
print("done -> exp550_depthdecay.json")

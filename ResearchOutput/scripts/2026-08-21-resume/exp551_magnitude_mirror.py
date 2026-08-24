#!/usr/bin/env python3
"""exp551 MAGNITUDE-MIRROR (round-70 #6, coordinator inline): is the exp546 'energy
channel' anything more than N's own magnitude? Decisive controls on exp546_data.npz:
(1) head-to-head vs plain logN / sqrtN-floor / frac(sqrtN) under pooled shuffles;
(2) WITHIN fine joint (log n x log m) cell shuffles;
(3) feature conditioned on logN deciles — if exactly null, the feature is a
deterministic monotone function of |N| (a magnitude mirror carrying ZERO bits)."""
import numpy as np, json
from collections import Counter
d=np.load('ResearchOutput/scripts/2026-08-21-resume/exp546_data.npz',allow_pickle=True)
P,Q,b1=d['P'],d['Q'],d['b1']
m=(P+Q)//2; n=(Q-P)//2
feat=d['x_f1_w4096_hratio']
logN=np.log(P*Q); isq=np.sqrt(P*Q)//1; fr=np.sqrt(P*Q)%1

def mi(xb,y):
    c_xy=Counter(zip(xb.tolist(),y.tolist())); c_x=Counter(xb.tolist()); c_y=Counter(y.tolist())
    N=len(xb)
    return sum(p*np.log2(p/((c_x[a]/N)*(c_y[b]/N))) for (a,b),k in c_xy.items() for p in [k/N])
def qbins(x,k=12): return np.clip(np.digitize(x,np.quantile(x,np.linspace(0,1,k+1))[1:-1]),0,k-1)

rng=np.random.default_rng(9)
out={}
pooled={}
for name,x in [("spectral_hratio",feat),("logN",logN),("sqrtN_floor",isq),("frac_sqrtN",fr)]:
    xb=qbins(x); I=mi(xb,b1)
    nl=[mi(rng.permutation(xb),b1) for _ in range(150)]
    pooled[name]=(round(I,4),round(float((I-np.mean(nl))/np.std(nl)),1))
out["pooled_12q"]=pooled

ln=qbins(np.log(n),12); lm=qbins(np.log(m),12)
cells={}
for i in range(len(b1)): cells.setdefault((int(ln[i]),int(lm[i])),[]).append(i)
big={k:np.array(v) for k,v in cells.items() if len(v)>=40}
cov=sum(len(v) for v in big.values())
cond={}
for name,x in [("spectral_hratio",feat),("logN",logN),("frac_sqrtN",fr)]:
    xs=qbins(x)
    def ws(arr): return sum(mi(arr[v],b1[v])*(len(v)/cov) for v in big.values())
    obs=ws(xs); nulls=[]
    for _ in range(80):
        tmp=xs.copy()
        for v in big.values(): tmp[v]=xs[rng.permutation(v)]
        nulls.append(ws(tmp))
    cond[name]=(round(obs,4),round(float(np.mean(nulls)),4),round(float((obs-np.mean(nulls))/max(np.std(nulls),1e-9)),1))
out["within_fine_nm_cells"]={"cells":len(big),"rows_covered":cov,"results":cond}

dec=qbins(logN,12)
groups={}
for i in range(len(b1)): groups.setdefault(int(dec[i]),[]).append(i)
bigg={k:np.array(v) for k,v in groups.items() if len(v)>=60}
covg=sum(len(v) for v in bigg.values())
xs=qbins(feat)
def ws(arr): return sum(mi(arr[v],b1[v])*(len(v)/covg) for v in bigg.values())
obs=ws(xs); nulls=[]
for _ in range(80):
    tmp=xs.copy()
    for v in bigg.values(): tmp[v]=xs[rng.permutation(v)]
    nulls.append(ws(tmp))
out["feature_given_logN_deciles"]={"MI":round(obs,6),"null_mean":round(float(np.mean(nulls)),6),
  "null_sd":round(float(np.std(nulls)),6),"z":round(float((obs-np.mean(nulls))/max(np.std(nulls),1e-9)),1)}
json.dump(out,open('ResearchOutput/scripts/2026-08-21-resume/exp551_magnitude_mirror.json','w'),indent=1)
print(json.dumps(out,indent=1))

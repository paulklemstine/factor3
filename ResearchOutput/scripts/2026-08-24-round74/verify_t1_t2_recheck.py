#!/usr/bin/env python3
"""Independent re-verification of the barrier-4 positional-converse draft
(barrier4_positional_converse_draft.md) and its finite-check artifact
exp574b_saturation_check.py / exp574b_result.json.

Recomputes everything from scratch (does not import exp574b):
  1. T1(a) algebra: fire-or-silent S_A, announce-always S_B, S_B<=S_A,
     scan-beats-ignore iff P_hit>mu, finite-M rational form.
     Plus the silence-certification reading (fires iff p in R): the committed
     law understates the achievable value there.
  2. T1(b) block-first dominance: exhaustive over ALL orderings for small M
     (both protocols, grid of (mu,P) including P<mu), plus contiguous
     block-insertion sweep at M<=64 (the draft's stated closure).
  3. T2 dyadic identity: independent DP, W in {16,64,256,1024} and all dyadic
     <= 4096; general-L upper-bound property + deepest undercut to 4096;
     spot checks L in {3,5,7,17}; census k_opt at 2^19 / 2^20;
     additive-constant bracket vs log2W; marginal-saving identity.
  4. Conjecture D witness arithmetic: all (mu,P)->S mappings, locus inversion,
     feasibility (P<=1 <=> mu <= 1/S).
  5. Cross-check of every stored number in exp574b_result.json.
"""
import json, math
from itertools import permutations

R = {}

# ---------- 1. T1(a) algebra ----------
S_A = lambda mu, P: 1.0/(1-(1-mu)*P)
S_B = lambda mu, P: 1.0/(1+mu-P)
num_bad = 0
for mu in [i/200 for i in range(1,100)]:
    for P in [i/200 for i in range(1,201)]:
        # denominator identities from direct large-M accounting:
        dA = P*mu + (1-P)*1.0          # E[C_A]/C0 -> P*mu+(1-P)
        dB = P*mu + (1-P)*(1+mu)       # E[C_B]/C0 -> P*mu+(1-P)(1+mu)
        if abs(dA - (1-(1-mu)*P)) > 1e-12*max(1.0,dA): num_bad += 1
        if abs(dB - (1+mu-P))       > 1e-12*max(1.0,dB): num_bad += 1
        if not (S_B(mu,P) <= S_A(mu,P)*(1+1e-12)+1e-300): num_bad += 1
        # equality iff P==1 (relative tolerance: values reach ~200x)
        if ((abs(S_A(mu,P)-S_B(mu,P))<=1e-10*max(S_A(mu,P),S_B(mu,P))) != (abs(P-1)<1e-12)):
            num_bad += 1
# scan-R-first beats ignoring-R iff mu < P (announce-always committed):
for mu in [0.02,0.05,0.1,0.2,0.5]:
    for P in [i/100 for i in range(101)]:
        if (S_B(mu,P) > 1.0) != (P > mu): num_bad += 1
R["T1a_algebra_consistency_failures"] = num_bad

# silence-certification reading: fires IFF p in R => silence proves p notin R,
# optimal post-silence action scans the complement:
def S_cert(mu,P):
    return 1.0/(P*mu + (1-P)*(1-mu))
ex = [(mu,P,S_A(mu,P),S_cert(mu,P)) for mu,P in [(0.05,0.85),(0.05,0.90),(0.02,0.985),(0.115,0.87)]]
R["T1a_silence_certified_alternative"] = [
    {"mu":m,"P":p,"stated_law":round(a,4),"certifying_silence":round(c,4)} for m,p,a,c in ex]

# finite-M rational form vs optimal-ordering closed form (sort weights desc)
def enum_cost(order, w):  # w: list of probs aligned to candidate index; E[C]=sum i*w(pi_i)
    return sum((i+1)*w[c] for i,c in enumerate(order))
def min_cost(w):          # min over ALL orderings = weights sorted descending
    return sum((i+1)*x for i,x in enumerate(sorted(w,reverse=True)))
# sanity anchor: closed form equals brute force on tiny M
import random as _rnd
_rnd.seed(7)
for _M in [4,5,6]:
    for _ in range(20):
        w=[_rnd.random() for _ in range(_M)]
        assert abs(min_cost(w)-min(enum_cost(p,w) for p in permutations(range(_M))))<1e-9
fin_bad = 0
for M in [6,10,20,33,64,129]:
    for nR in range(1,M):
        r = nR/M
        nN = M-nR
        for P in [0.3,0.6,0.85,0.9,1.0]:
            w = [P/nR]*nR + [(1-P)/nN]*nN
            EC = (P*(nR+1)+(1-P)*(M+1))/2.0   # committed R-first expected cost
            S_finite = ((M+1)/2)/EC           # draft's (M+1)/(P(muM+1)+(1-P)(M+1))
            S_pred   = (M+1)/(P*(r*M+1)+(1-P)*(M+1))
            if abs(S_finite-S_pred)>1e-9: fin_bad += 1
            # and R-first attains the descending-sort optimum iff P>=mu
            # (skip the near-tie zone to keep the classifier sharp)
            if abs(P-r) > 0.02:
                d = enum_cost(list(range(nR))+list(range(nR,M)),w)-min_cost(w)
                if (d < 1e-9*max(1.0,M)) != (P>r):
                    fin_bad += 1
R["T1a_finiteM_formula_failures_and_Rfirst_iff_P_ge_mu"] = fin_bad

# ---------- 2. T1(b) dominance ----------
def dom_exhaustive(M, mu_frac, protocol, P):
    """min over ALL orderings of E[C]; returns whether R-block-first attains it."""
    nR = int(round(mu_frac*M)); nN = M-nR
    if protocol == "A_fire":      # posterior given fire: mass on R only
        w = [1.0/nR]*nR + [0.0]*nN
    else:                          # B announced: mixture
        w = [P/nR]*nR + [(1-P)/nN]*nN
    best = min(enum_cost(o,w) for o in permutations(range(M)))
    first = list(range(nR))+list(range(nR,M))  # R members first
    bf = enum_cost(first,w)
    return abs(bf-best)<1e-12, bf, best

dom_rows = []
all_ok_A, fail_B = True, []
for M in [4,5,6,7,8]:
    for mu_frac in [1/M, 2/M, 3/M]:
        if mu_frac >= 0.95: continue
        for P in [mu_frac*0.25, mu_frac*0.75, mu_frac*0.99,
                  mu_frac*1.01, mu_frac*1.5, 0.85, 1.0]:
            okA,_,_ = dom_exhaustive(M,mu_frac,"A_fire",P)
            okB,bf,bst = dom_exhaustive(M,mu_frac,"B_ann",P)
            all_ok_A &= okA
            if not okB: fail_B.append((M,round(mu_frac,4),round(P,4),round(bf,4),round(bst,4)))
R["T1b_exhaustive_orders"] = {
    "protocol_A_blockfirst_always_optimal": bool(all_ok_A),
    "protocol_B_counterexamples_P_lt_mu": fail_B[:12],
    "protocol_B_all_failures_have_P_lt_mu": all(P < f for _,f,P,_,_ in fail_B)}

# contiguous block-insertion sweep at larger M (draft's stated brute force)
sweep_ok = True
for M in [16,33,64]:
    for mu_frac in [0.05,0.1,0.2]:
        nR=int(round(mu_frac*M)); nN=M-nR
        for P in [0.85,0.95,1.0]:
            w=[P/nR]*nR+[(1-P)/nN]*nN
            costs=[]
            for slot in range(nN+1):  # insert contiguous R-block after `slot` N-members
                order=list(range(nR,M))+[]  # placeholder
                Npart=list(range(nR,M)); Rpart=list(range(0,nR))
                order=Npart[:slot]+Rpart+Npart[slot:]
                costs.append(enum_cost(order,w))
            if min(costs)!=costs[0]: sweep_ok=False   # block-first (slot 0) must win
R["T1b_block_insertion_sweep_M16_33_64_first_slot_wins"] = sweep_ok

# ---------- 3. T2 ----------
def dp_all(Lmax):
    V={0:0.0,1:1.0}
    for L in range(2,Lmax+1):
        stop=(L+1)/2.0
        bv=stop
        for x in range(1,L):
            v=1+(x/L)*V[x]+((L-x)/L)*V[L-x]
            if v<bv: bv=v
        V[L]=bv
    return V
V = dp_all(4096)
cf  = lambda L,k: k+(-(-L//(2**k))+1)/2.0        # ceil variant (general L)
cfd = lambda W,k: k+(W/(2**k)+1)/2.0             # real-division variant (dyadic)

dyad = {}
for e in range(1,13):
    W=2**e
    c=min(cfd(W,k) for k in range(e+4))
    ks=[k for k in range(e+4) if abs(cfd(W,k)-c)<1e-12]
    dyad[W]={"dp":V[W],"closed":c,"exact":abs(V[W]-c)<1e-9,"argmin_rel_log2W":[k-e for k in ks]}
R["T2_dyadic"] = {str(W):{k:(round(v,9) if isinstance(v,float) else v) for k,v in d.items()}
                  for W,d in dyad.items()}
R["T2_dyadic_all_exact_2_to_4096"] = all(d["exact"] for d in dyad.values())
R["T2_dyadic_closed_form_V_equals_log2W_plus_half"] = all(
    abs(d["dp"] - (math.log2(W)+0.5))<1e-9 for W,d in dyad.items())

dev=[(V[L]-min(cf(L,k) for k in range(0,2*L.bit_length()+3)),L) for L in range(2,4097)]
R["T2_general_L"]={
    "upper_bound_holds_to_4096": all(d<=1e-9 for d,_ in dev),
    "deepest_undercut_to_4096":{"delta":round(min(dev)[0],6),"at_L":min(dev)[1]},
    "undercut_below_half_count":sum(1 for d,_ in dev if d<-0.499999),
    "spot_L_3_5_7_17":[{"L":L,"V":round(V[L],6),
                        "cf":round(min(cf(L,k) for k in range(0,2*L.bit_length()+3)),6),
                        "undercut":round(V[L]-min(cf(L,k) for k in range(0,2*L.bit_length()+3)),6)}
                       for L in (3,5,7,17)]}

cens={}
for e in (19,20):
    W=2**e
    vals=[(k+(W/(2**k)+1)/2.0,k) for k in range(e+4)]
    c=min(vals); ks=[k for v,k in vals if abs(v-c[0])<1e-12]
    cens[W]={"C_star":c[0],"argmin":ks,"rel_log2W":[k-e for k in ks]}
R["T2_census_2p19_2p20"]={str(W):{"C_star":v["C_star"],
                                  "k_opt_set_rel_log2W":v["rel_log2W"]} for W,v in cens.items()}

const=[(V[L]-math.log2(L),L) for L in range(2,4097)]
kc_off = math.log2(math.log(2)/2)   # continuous optimum location: k_c-log2W
gcont = kc_off + (2/math.log(2)+1)/2  # g(k_c) - log2W ... computed symbolically below
# g(k_c): W*2^-k_c = 2/ln2 ; k_c = log2W + log2(ln2/2)
add_cont = math.log2(math.log(2)/2) + (2/math.log(2)+1)/2
R["T2_additive_constant"]={
    "continuous_relaxed_offset_vs_log2W": round(add_cont,4),
    "discrete_dyadic_offset": 0.5,
    "empirical_min_over_L2_4096": {"val":round(min(const)[0],4),"at_L":min(const)[1]},
    "empirical_max_over_L2_4096": {"val":round(max(const)[0],4),"at_L":max(const)[1]},
    "continuous_kopt_location_offset": round(kc_off,4),
    "discrete_argmin_location_offsets": [-2,-1],
    "note":"draft's '[−0.53,+0.5]' matches neither cost offset bracket; "
           "+0.5288/-0.4712 = |discrete argmin minus continuous k_opt| location wobble"}

# marginal saving identity: cost(k)-cost(k+1) = W/2^(k+2) - 1 (net of the query)
# (gross residual-scan saving is W/2^(k+2); the draft quotes the gross form)
ms_bad=0; ms_tot=0
for e in range(1,21):
    W=2**e
    for k in range(0,e+2):
        ms_tot+=1
        gross = W/(2**(k+2)); net = gross-1.0
        X=(k+(W/(2**k)+1)/2)-(k+1+(W/(2**(k+1))+1)/2)
        if abs(X-net)>1e-9*max(1.0,k): ms_bad+=1
R["T2_marginal_identity"]={"cells":ms_tot,"failures":ms_bad,
    "form":"cost(k)-cost(k+1)=W/2^(k+2)-1 exactly; draft's 'marginal value=W/2^(k+2)' is the GROSS saving"}

# ---------- 4. Conjecture D witnesses ----------
inv=lambda T,mu:(1-1/T)/(1-mu)
wit={}
for name,T,mu,P in [("5.19x",(5.1936,5.19),0.05,0.85),("6.91x",6.91,0.05,0.90),
                    ("4.35x",4.35,0.05,0.81),("29.1x",29.1,0.02,0.985)]:
    Tt=T[0] if isinstance(T,tuple) else T
    Pt=P
    wit[name]={"anchor":Tt,"at_(mu,P)":[mu,P],
               "S_A_at_rounded_P":round(S_A(mu,Pt),4),
               "exact_P_for_anchor":round(inv(Tt,mu),4),
               "feasible_mu_le_1_over_S": mu<=1/Tt+1e-12}
R["D_witnesses"]=wit
feas_bad=[]
for T in (5.19,6.91,4.35,29.1):
    for mu in (0.02,0.03,0.05,0.115):
        p=inv(T,mu)
        if p>1.0000001 and not (T==29.1 and mu in (0.05,0.115)): feas_bad.append((T,mu,p))
        if p>1.0000001: feas_bad.append(("INFEASIBLE",T,mu,round(p,4)))
R["D_locus_infeasible_rows_mu_gt_1_over_S"]=feas_bad

# ---------- 5. cross-check exp574b_result.json ----------
stored=json.load(open("/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74/exp574b_result.json"))
diffs=[]
# A
if abs(stored["A_residue_cap"]["max_speedup"]-4/3)>1e-5: diffs.append("A max")
if abs(stored["A_residue_cap"]["argmax_theta"]-0.5)>1e-3: diffs.append("A argmax")
# C dyadic rows
for row in stored["C_dp_check"]["dyadic_supports"]:
    W=row["W"]; e=int(math.log2(W))
    c=min(cfd(W,k) for k in range(e+4))
    if abs(row["closed"]-c)>1e-9: diffs.append(f"C closed W={W}")
    if abs(row["dp"]-V[W])>1e-6: diffs.append(f"C dp W={W}")
    if row["exact"]!=(abs(V[W]-c)<1e-9): diffs.append(f"C exact flag W={W}")
# C undercut
du=stored["C_dp_check"]["deepest_undercut_of_closed_form"]
my_du_128=min((V[L]-min(cf(L,k) for k in range(0,2*L.bit_length()+3)),L) for L in range(2,129))
if abs(du["delta"]-my_du_128[0])>1e-5 or du["at_L"]!=my_du_128[1]:
    diffs.append(f"C undercut stored {du} mine {my_du_128}")
# B census
for row in stored["B_census"]:
    e=row["log2W"]; W=2**e
    vals=[k+(W/(2**k)+1)/2.0 for k in range(e+4)]
    if abs(row["C_star"]-min(vals))>1e-4: diffs.append(f"B C_star W={W}")
    if row["k_opt_cost"]!=min(range(e+4),key=lambda k:k+(W/(2**k)+1)/2.0): diffs.append(f"B kopt W={W}")
    if row["k_pin_log2W"]!=e: diffs.append(f"B kpin W={W}")
# D examples
for exd in stored["D_t1_protocols"]["example_values"]:
    m,P=exd["mu"],exd["P_hit"]
    if abs(exd["fire_or_silent"]-S_A(m,P))>6e-4: diffs.append(f"D fos {m},{P}")
    if abs(exd["announce_always"]-S_B(m,P))>6e-4: diffs.append(f"D aa {m},{P}")
# D loci inversion
for name,rows in stored["D_t1_protocols"]["anchors_fos_locus_(mu,P)"].items():
    T=float(name.split("x")[0])
    for mu,P in rows:
        if abs(P-inv(T,mu))>6e-4: diffs.append(f"D locus {name} mu={mu}")
R["exp574b_stored_value_discrepancies"]=diffs

with open("/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74/verify_t1_t2_recheck.json","w") as f:
    json.dump(R,f,indent=1,default=str)

print(json.dumps(R,indent=1,default=str))

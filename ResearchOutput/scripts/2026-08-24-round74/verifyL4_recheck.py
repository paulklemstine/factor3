#!/usr/bin/env python3
"""VERIFIER recheck of GAP-L4 artifacts. Touches ONLY verifyL4_* files.
V1 replicate A1/A2/A3 of gapL4_check.py (same seed) WITHOUT rewriting gapL4_result.json.
V2 independent Monte-Carlo test of the rbar identity EC_A = P*rbar_R+(1-P)*rbar_C
   against simulated protocol-A costs (original script builds EC from the identity only).
V3 paper-219 row forensics: which formula/precision reproduces each printed S_A value.
V4 F3 game value under three payoff baselines: full-scan M, uniform (M+1)/2, same-prior C_desc.
Run: python3 verifyL4_recheck.py -> verifyL4_recheck_result.json
"""
import json, numpy as np

RD = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74/"
out = {}

def S_cert(mu, P):   return 1.0 / (mu * P + (1 - P) * (1 - mu))
def S_drafted(mu,P): return 1.0 / (1 - (1 - mu) * P)
def P_implied(S, mu): return (1.0 / S - (1 - mu)) / (2 * mu - 1)

# ---------------- V1: replicate stored results ----------------
stored = json.load(open(RD + "gapL4_result.json"))
diffs = []

anchors = [("5.19x frontier",5.19,0.05,0.85,0.85),
           ("6.91x trunc-high",6.91,0.05,0.9003,0.90),
           ("4.35x trunc-low",4.35,0.05,0.8106,None),
           ("29.1x alpha=1",29.10,0.02,0.9853,0.985)]
a1 = []
for name,S,mu,Phat,Plaw in anchors:
    row = {"anchor": name, "S_cert_at_Phat": round(S_cert(mu,Phat),4)}
    if Plaw is not None:
        row["S_cert_at_Plaw"] = round(S_cert(mu,Plaw),4)
        row["precision_gap"]  = round(row["S_cert_at_Phat"]-row["S_cert_at_Plaw"],4)
    row["P_implied_by_S_at_mu"] = round(P_implied(S,mu),6) if 2*mu!=1 else None
    a1.append(row)
for got, want in zip(a1, stored["A1_anchor_precision"]):
    for k in want:
        if k in got and isinstance(want[k],(int,float)) and got[k] is not None \
           and abs(got[k]-want[k]) > 5e-7:
            diffs.append(f"A1 {want['anchor']}.{k}: stored {want[k]} vs recomputed {got[k]}")
out["V1_A1_replicated"] = a1
out["V1_A1_diffs"] = diffs

# A2 replication
def capture_canon(mu,R):
    c = 1 - R**-0.5
    return min(1.0, mu/c) if c > 0 else 1.0
def R_required(P,mu): return (1 - mu/P)**-2
a2_diffs = []
for muk,d in stored["A2_F2_canonical_measure"]["capture_curve_canon"].items():
    mu = float(muk.split("=")[1])
    for Rk,v in d.items():
        R = float(Rk.split("=")[1])
        if abs(capture_canon(mu,R)-v) > 5e-5:
            a2_diffs.append(f"capture {muk} {Rk}: stored {v} vs {round(capture_canon(mu,R),4)}")
amap = {n:(s,m,ph) for n,s,m,ph,_ in anchors}
for name,v in stored["A2_F2_canonical_measure"]["required_R_per_anchor"].items():
    s_,m_,ph_ = amap[name]
    if abs(R_required(ph_,m_)-v) > 5e-5:
        a2_diffs.append(f"required_R {name}: stored {v} vs {round(R_required(ph_,m_),4)}")
out["V1_A2_diffs"] = a2_diffs

# A3 replication (same seed 74, same loop order)
M = 64
pos = np.arange(1, M+1)
def audit(pi, idx_R):
    P = pi[idx_R].sum()
    maskR = np.zeros(M, bool); maskR[idx_R] = True
    pR = pi[idx_R]; pC = pi[~maskR]
    rR = np.arange(1, len(idx_R)+1); rC = np.arange(1, M-len(idx_R)+1)
    rbar_R = (pR*rR).sum()/P if P > 0 else 0.0
    rbar_C = (pC*rC).sum()/(1-P) if P < 1 else 0.0
    EC = P*rbar_R + (1-P)*rbar_C
    Cdesc = (pi*pos).sum(); Csort = (np.sort(pi)[::-1]*pos).sum()
    lam = Csort/Cdesc
    return P, rbar_R, rbar_C, EC, Cdesc, Csort, lam, len(idx_R)/M

rngA = np.random.default_rng(74)
trials = 4000
viol = 0; ratios = []; viol_by_place = {0:[],1:[],2:[]}
for t in range(trials):
    alpha = float(np.exp(rngA.uniform(np.log(0.05), np.log(5.0))))
    pi = rngA.dirichlet(np.full(M, alpha))
    mu_w = float(rngA.choice([0.02,0.05,0.10]))
    k = max(1,int(round(mu_w*M)))
    place = int(rngA.choice([0,1,2]))
    start = [0,(M-k)//2,M-k][place]
    idx_R = np.arange(start,start+k)
    P,rr,rc,EC,Cd,Cs,lam,mw = audit(pi,idx_R)
    if P <= 0 or P >= 1:
        viol_by_place[place].append(False); continue
    S = Cd/EC; SA = S_cert(mw,P)
    ratios.append(S/SA)
    hit = bool(S > SA); viol += hit; viol_by_place[place].append(hit)
vrate_by_place = {pl: round(float(np.mean(v)),4) for pl,v in viol_by_place.items()}
repl = {
 "violation_rate": round(viol/max(1,len(ratios)),4),
 "max_S_over_SA_observed": round(max(ratios),2),
}
st = stored["A3_F1_shape_audit"]
for k_,v_ in repl.items():
    if abs(st[k_]-v_) > 1e-9:
        diffs.append(f"A3.{k_}: stored {st[k_]} vs replicated {v_}")
out["V1_A3_replication"] = {"recomputed": repl, "stored": {k_: st[k_] for k_ in repl},
                            "violation_rate_by_placement_head_mid_tail": vrate_by_place}

# explicit witness re-check
pi = np.zeros(M); k = int(0.05*M); start = M-k; half = k//2
pi[start:start+half] = 1.0/half
P,rr,rc,EC,Cd,Cs,lam,mw = audit(pi, np.arange(start,start+k))
witness = {"S_measured": round(Cd/EC,2), "S_cert": round(S_cert(mw,P),2),
           "tau_R": round(rr/(mw*M),3),
           "asymptotic_4_over_mu_minus_3_at_mu": round(4/(k/M)-3,2)}
if abs(witness["S_measured"]-stored["A3_explicit_offdiag_witness"]["S_measured"])>1e-9:
    diffs.append("A3 witness mismatch")
out["V1_A3_witness_recheck"] = witness

# ---------------- V2: Monte-Carlo test of the identity ----------------
rngB = np.random.default_rng(20260824)
mc = []
for trial in range(8):
    alpha = float(np.exp(rngB.uniform(np.log(0.1), np.log(4.0))))
    pi = rngB.dirichlet(np.full(M, alpha))
    k = int(rngB.choice([2,4,8])); start = int(rngB.choice([0,(M-k)//2,M-k]))
    idx_R = np.arange(start,start+k)
    P,rr,rc,EC,Cd,Cs,lam,mw = audit(pi,idx_R)
    # simulate protocol A committed policy: draw p~pi; cost = block-local rank if p in R else rank in C
    cum = np.cumsum(pi); draws = rngB.random(200000)
    ps = np.searchsorted(cum, draws)
    pos_of = np.empty(M, int); pos_of[idx_R] = np.arange(1,k+1)
    others = [i for i in range(M) if i not in set(idx_R)]
    pos_of[others] = np.arange(1, M-k+1)
    costs = pos_of[ps]
    mc_sim = float(costs.mean())
    mc.append({"EC_identity": round(EC,4), "EC_simulated": round(mc_sim,4),
               "rel_err": round(abs(EC-mc_sim)/mc_sim,4)})
worst = max(m["rel_err"] for m in mc)
out["V2_identity_montecarlo"] = {"cells": mc, "max_rel_err": worst,
    "verdict": "PASS" if worst < 0.02 else "FAIL"}

# ---------------- V3: paper-219 printed-row forensics ----------------
rows = [
 ("T1-table/D-table 5.19 row", 0.05, 0.8500, 5.1948),
 ("T1-table/D-table 6.91 row", 0.05, 0.9003, 6.91),
 ("T1-table/D-table 4.35 row", 0.05, 0.8106, 4.35),
 ("T1-table/D-table 29.1 row", 0.02, 0.9853, 29.0698),
]
forensics = []
cands = {}
for label,mu,Phat,printed in rows:
    cands = {
      "certified@P_printed": S_cert(mu,Phat),
      "certified@P_round3":  S_cert(mu,round(Phat,3)),
      "certified@P_round2":  S_cert(mu,round(Phat,2)),
      "drafted@P_printed":   S_drafted(mu,Phat),
      "drafted@P_round3":    S_drafted(mu,round(Phat,3)),
      "certified@(0.115,0.87)": S_cert(0.115,0.87),
      "drafted@(0.115,0.87)":   S_drafted(0.115,0.87),
    }
    matches = [n for n,v in cands.items()
               if abs(v-printed)/printed < 0.002 or f"{v:.4f}"==f"{printed:.4f}"
               or abs(round(v,2)-printed)<1e-9]
    forensics.append({"row":label,"mu":mu,"P_printed":Phat,"S_printed":printed,
                      "candidates_rounded4":{n:round(v,4) for n,v in cands.items()},
                      "matches":matches})
out["V3_paper219_row_forensics"] = forensics

# feasibility robustness under corrected values
feas = []
for name,S,mu,Phat,_ in anchors:
    feas.append({"anchor":name, "mu_le_1/S_meas": bool(mu <= 1/S),
                 "S_cert@Phat_ge_S_meas": bool(S_cert(mu,Phat) >= S)})
out["V3_feasibility_under_corrected_values"] = feas

# ---------------- V4: F3 game values under three baselines ----------------
v4 = []
for (k, P) in [(1,0.85),(2,0.85),(3,0.85),(2,0.75),(1,0.985),(2,0.985)]:
    Mm = 12
    if not (1 <= k <= Mm-1): continue
    mu = k/Mm
    EC_corner = P*k + (1-P)*(Mm-k)          # adversary max-EC at tail corner (exact, provable: linear in dist)
    val_fullscanM = Mm/EC_corner
    val_uniformC0 = (Mm+1)/2/EC_corner
    d = mu*P + (1-P)*(1-mu)
    # convention (c): same-prior descending baseline, analytic undercut family:
    # P mass at R's bottom(global M), (1-P) at C's bottom(global rank M-k when R is bottom window)
    S_c = (P*Mm + (1-P)*(Mm-k))/(EC_corner)
    # brute-force adversary search over within-cell distributions (Dirichlet samples)
    rngC = np.random.default_rng(7)
    best_EC = 0; min_S = 1e9
    gR = Mm  # R = bottom window of width k: global ranks Mm-k+1..Mm ; bottom = Mm
    for _ in range(20000):
        wR = rngC.dirichlet(np.ones(k)); wC = rngC.dirichlet(np.ones(Mm-k))
        ranksR = np.arange(Mm-k+1, Mm+1)          # global descending ranks of R members
        ranksC = np.arange(1, Mm-k+1)
        EC   = P*(wR @ (ranksR-(Mm-k))) + (1-P)*(wC @ ranksC)   # block-local ranks
        Cdsc = P*(wR @ ranksR) + (1-P)*(wC @ ranksC)
        best_EC = max(best_EC, EC); min_S = min(min_S, Cdsc/EC)
    # exact corner configuration for convention (c)
    wR = np.zeros(k); wR[-1]=1.0; wC=np.zeros(Mm-k); wC[-1]=1.0
    EC_x = P*k + (1-P)*(Mm-k); Cd_x = P*Mm + (1-P)*(Mm-k)
    v4.append({"k":k,"P":P,"mu":mu,"d_law_denominator":round(d,6),
               "certified_law_1/d":round(1/d,4),
               "value_baseline_fullscan_M":round(val_fullscanM,4),
               "value_baseline_uniform_C0":round(val_uniformC0,4),
               "brute_max_EC":round(best_EC,4),"corner_EC_exact":EC_corner,
               "corner_is_max_EC":bool(best_EC<=EC_corner+1e-6),
               "convention_sameprior_desc_analytic_undercut":round(S_c,4),
               "undercut_beats_claimed_value":bool(S_c < 1/d-1e-12),
               "brute_min_S_sameprior":round(min_S,4)})
out["V4_F3_game_values"] = v4
ok_a  = all(abs(r["value_baseline_fullscan_M"]-r["certified_law_1/d"])<2e-3 for r in v4)
ok_b  = all(abs(r["value_baseline_uniform_C0"]-r["certified_law_1/d"]/2)<2e-3 for r in v4)
out["V4_verdicts"] = {
  "fullscan-M baseline reproduces certified law exactly": ok_a,
  "uniform-C0 baseline gives HALF the certified law": ok_b,
  "same-prior-descending adversary strictly beats claimed value (all cells)": all(r["undercut_beats_claimed_value"] for r in v4)}

with open(RD+"verifyL4_recheck_result.json","w") as f:
    json.dump(out,f,indent=1)
print(json.dumps(out,indent=1)[:6000])

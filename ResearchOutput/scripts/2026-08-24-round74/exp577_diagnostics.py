#!/usr/bin/env python3
"""exp577 POST-HOC DIAGNOSTICS (clearly labeled post-hoc; not pre-registered).

Question raised by the full-run sweep (R2=0.32/D-red 33% at B=400 vs exp576's
measured 0.057-0.078 / 9-14% for its <=100/<=400 dial forms on seed 20260826):

exp576's secondary dials were computed in RECIPROCITY-FLIPPED form:
  S_prod_exp576(N) = #{l<=100 : jac(l,lo)*jac(l,hi)==+1}   (jac(l,factor))
  S139_exp576(N)   = #{r<=400 : jac(r,N)==+1}              (jac(r,N), composite)
By quadratic reciprocity each relates to the MECHANISTIC Legendre form
  C(B) = #{odd prime l<=B : jac(N mod l, l)==+1}   (what governs l | x^2-N)
by an l-dependent sign: jac(r,N) = (-1)^{((r-1)/2)((N-1)/2)} * jac(N mod r, r).
For N == 3 (mod 4) -- exactly the balanced semiprimes with ONE factor 3 mod 4,
expected ~50% of any population -- the flip is ACTIVE on every l == 3 (mod 4).
Prediction: exp576-form dials are PARTIALLY INVERTED mixtures -> attenuated
fits; this run's clean form at B=400 (R2 .32 / D-red 33%) should dominate.

Tests here, all on THIS run's rows (same hits, same GLM machinery):
  T1 cross-validate gmpy dial vs sympy Legendre at B<=100 (impl check).
  T2 recompute exp576-form S_prod@100 and S139@400 (verbatim formulas);
     regress vs hits; compare R2/D-red to clean C400.
  T3 inversion bookkeeping: %N with N==3 mod 4; agreement/inversion rates
     per prime class; corr(exp576-form, clean form).
  T4 (post-hoc, mechanism) 1/l-weighted clean dials W400/W1e6 =
     sum_{QR l<=B} 1/l -- tests whether equal-weight cumulative counting
     (not window location) causes the beyond-400 R2 collapse.
"""
import json, math, sys
sys.path.insert(0, "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74")
from exp577_product_dial import ols_r2, poisson_glm, gen_primes
import statistics as st
from sympy import jacobi_symbol as sjac
from gmpy2 import jacobi as gjac  # Legendre(N mod p, p); used where p=2 would break sympy

rows = json.load(open("exp577_result.json"))["rows"]
primes_le400 = [p for p in gen_primes(400)]
primes_le1e6 = [p for p in gen_primes(1000000)]

# T1 + clean dial recomputed with BOTH impls at the SAME bound (<=100):
# first attempt compared bound-100 vs rows' bound-400 counts (bug, caught);
# correct check is sympy-Legendre vs gmpy-Jacobi on identical prime sets.
C100_sym, t1_diffs = [], []
for r in rows:
    N = int(r["N"])
    cs = sum(1 for p in primes_le400 if p <= 100 and p > 2 and sjac(N, p) == 1)
    cg = sum(1 for p in primes_le400 if p <= 100 and p > 2 and gjac(N % p, p) == 1)
    C100_sym.append(cs)
    t1_diffs.append(abs(cs - cg))
t1_max_diff = max(t1_diffs)

def regress(xs, ys, ts, name):
    ms = sum(ys)/len(ys)
    var_h = st.pvariance(ys)
    D_raw = var_h/ms
    lr = [math.log((y+0.5)/t) for y, t in zip(ys, ts)]
    off = [math.log(t) for t in ts]
    mx = sum(xs)/len(xs); sx = st.pvariance(xs)**0.5 or 1.0
    xz = [(x-mx)/sx for x in xs]
    r2, slope = ols_r2(xz, lr)
    a, b, mu, pr2, phi, z = poisson_glm([float(x) for x in xs], ys, off)
    D_cond = st.pvariance([y-m for y, m in zip(ys, mu)])/ms
    dred = 100*(1-D_cond/D_raw)
    return {"dial": name, "R2_log_ols": round(r2, 4), "slope_sign": "+" if slope > 0 else "-",
            "glm_wald_z": round(z, 2), "D_reduction_pct": round(dred, 2)}

ys = [r["hits"] for r in rows]
ts = [r["total"] for r in rows]

# T2/T3: exp576-form dials
P100, E139, n3mod4, inv_events, agree_events = [], [], 0, 0, 0
for r in rows:
    N, lo, hi = int(r["N"]), int(r["lo"]), int(r["hi"])
    P100.append(sum(1 for l in primes_le400 if l <= 100 and sjac(l, lo)*sjac(l, hi) == 1))
    E139.append(sum(1 for rr in primes_le400 if sjac(rr, N) == 1))
    if N % 4 == 3:
        n3mod4 += 1
        for l in primes_le400:
            if l % 4 == 3:
                mech = (sjac(N, l) == 1)
                e576 = (sjac(l, N) == 1)
                if mech != e576: inv_events += 1
                else: agree_events += 1

# T4: 1/l-weighted clean dials
W400, W1e6 = [], []
for r in rows:
    N = int(r["N"])
    w4 = w6 = 0.0
    for p in primes_le1e6:
        if p == 2:
            continue  # Jacobi undefined at even modulus; clean dial excludes l=2
        if gjac(N % p, p) == 1:
            wl = 1.0/p
            if p <= 400: w4 += wl
            w6 += wl
    W400.append(w4); W1e6.append(w6)

out_regs = [
    regress(C100_sym, ys, ts, "C100_sympy_crosscheck"),
    regress([r["S400"] for r in rows], ys, ts, "C400_clean_gmpy"),
    regress(P100, ys, ts, "S_prod@100_EXP576_FORM"),
    regress(E139, ys, ts, "S139@400_EXP576_FORM"),
    regress(W400, ys, ts, "W400_weighted_1_over_l"),
    regress(W1e6, ys, ts, "W1e6_weighted_1_over_l"),
]
def pearson(a, b):
    n = len(a); ma = sum(a)/n; mb = sum(b)/n
    sa = (sum((x-ma)**2 for x in a))**.5; sb = (sum((x-mb)**2 for x in b))**.5
    return sum((x-ma)*(y-mb) for x, y in zip(a, b))/(sa*sb)

S400_col = [r["S400"] for r in rows]
corr_P_C = round(pearson(P100, S400_col), 3)  # first draft dropped /n -> impossible 7.429; fixed

res = {
    "status": "POST-HOC diagnostics (not pre-registered)",
    "T1_gmpy_vs_sympy_max_abs_diff_at_100": t1_max_diff,
    "T3_pct_N_eq_3_mod_4": round(100*n3mod4/len(rows), 1),
    "T3_reciprocity_flip_events_on_l3mod4_N3mod4": inv_events,
    "T3_agree_events": agree_events,
    "T3_flip_rate_pct": round(100*inv_events/max(inv_events+agree_events, 1), 1),
    "T3_corr_Sprod576_vs_clean_C400_pearson_r": corr_P_C,
    "T4_corr_W400_vs_C400": round(pearson(W400, S400_col), 3),
    "T4_corr_W1e6_vs_W400": round(pearson(W1e6, W400), 3),
    "regressions": out_regs,
}

# ---- REVISION 2026-08-24 (post verifyL7b): variant table settling formA/l=2 ----
# verifyL7b's build_cols implemented its "P100_e576_formA" column as
# gjac(lo%p,p)*gjac(hi%p,p) == (N mod p | p) -- i.e. the CLEAN dial -- while its
# own flip_audit defines form-A as sjac(l,lo)*sjac(l,hi). Its part1c/1d "formA"
# rows (.373/34.45, r .476) therefore belong to clean-C100, not the flipped form.
# These columns settle every variant empirically on THIS population:
pr100 = [p for p in primes_le400 if p <= 100]
V = {"P100flip_with2": [], "P100flip_no2": [], "C100clean_no2": [],
     "SIndiv576_with2": []}
for r in rows:
    N, lo, hi = int(r["N"]), int(r["lo"]), int(r["hi"])
    V["P100flip_with2"].append(sum(1 for l in pr100 if sjac(l, lo)*sjac(l, hi) == 1))
    V["P100flip_no2"].append(sum(1 for l in pr100 if l > 2 and sjac(l, lo)*sjac(l, hi) == 1))
    V["C100clean_no2"].append(sum(1 for p in pr100 if p > 2 and sjac(N, p) == 1))
    si = 0
    for l in pr100:
        si += (sjac(l, lo) == 1) + (sjac(l, hi) == 1)
    V["SIndiv576_with2"].append(si)
rev = {"note": ("verifier's 'formA strong' column is CLEAN C100 (label swap in "
                "verifyL7b build_cols line 'gjac(lo % p, p)*gjac(hi % p, p)'); "
                "flipped forms stay weak with or without l=2 -> the proposed "
                "'l=2 mishandling' leg is REJECTED (bounded +-1 count); "
                "exp576 PRIMARY S_indiv null confirmed here -> remains OPEN"),
       "columns": {}}
for k, v in V.items():
    rr = regress(v, ys, ts, k)
    rr["pearson_vs_C400"] = pearson(v, S400_col)
    rev["columns"][k] = rr
res["revision_2026_08_24_verifyL7b"] = rev
with open("exp577_diagnostics.json", "w") as f:
    json.dump(res, f, indent=1)
print(json.dumps(res, indent=1))

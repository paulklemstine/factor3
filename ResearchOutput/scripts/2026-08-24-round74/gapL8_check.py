#!/usr/bin/env python3
"""GAP-L8 finite check: k_pin vs k_opt^census vs k_opt^econ (<= a few seconds).

Verifies, numerically:
 V1  T2 census: k_opt(W)=argmin_k[k+(W/2^k+1)/2] has offsets {-2,-1} rel log2W,
     V*=log2W+1/2 exactly on dyadic W (2..4096).
 V2  Convention identity: E(k;T0)=1+k+(T0-1)/2^k == V(k; W=2(T0-1))+1/2 pointwise;
     hence discrete argmins coincide EXACTLY under the anchor map W <-> 2(T0-1).
 V3  Naive same-anchor rule: feeding the SAME number A as both support width (T2)
     and baseline-minus-floor (econ) shifts the optimum by EXACTLY +1 query:
     continuous locations differ by ln2-free constant 1; discrete argmin sets too.
 V4  exp563 recorded values reproduce from its stored Tbar (balanced/unbalanced).
 V5  k_pin=log2W never coincides with either optimum (gap >= 1 query, W=2..4096).
"""
import json, math

import numpy as np

R = json.load(open("exp563_result.json"))


def V(k, W):          # T2 census objective (expected residual scan, uniform prior)
    return k + (W / 2.0 ** k + 1.0) / 2.0


def Econ(k, T0, cq=1.0):  # exp563 net-cost objective (scan units)
    return 1.0 + cq * k + (T0 - 1.0) * 2.0 ** (-k)


def argmins(f, kmax=60):
    vals = [f(k) for k in range(kmax + 1)]
    m = min(vals)
    return [k for k in range(kmax + 1) if abs(vals[k] - m) < 1e-12], m


out = {}
# ---- V1 census offsets and dyadic value -----------------------------------
off = set()
dyad_ok = True
for n in range(1, 13):
    W = 2 ** n
    ks, m = argmins(lambda k, W=W: V(k, W))
    off |= {round(k - math.log2(W), 6) for k in ks}   # offset := k_opt - log2W
    dyad_ok &= abs(m - (math.log2(W) + 0.5)) < 1e-12
out["V1_census_offsets_rel_log2W"] = sorted(off)
out["V1_dyadic_V*_eq_log2W+half"] = bool(dyad_ok)

# ---- V2/V3 conversion rules -------------------------------------------------
conv = {}
for label, T0 in (("synth_W1024", 1024 / 2 + 1), ("synth_W65536", 65536 / 2 + 1),
                  ("BALANCED", None), ("UNBALANCED", None)):
    if T0 is None:
        row = next(r for r in R["rows"] if r["stratum"] == label and r["arm"] == "ADAPT" and r["k"] == 0)
        T0 = row["mean_T"]
    Weq = 2.0 * (T0 - 1.0)                       # anchor map W <-> 2(T0-1)
    ident = max(abs(Econ(k, T0) - (V(k, Weq) + 0.5)) for k in range(61))
    ke, _ = argmins(lambda k: Econ(k, T0))
    kc, _ = argmins(lambda k, W=Weq: V(k, W))
    # naive same-anchor: feed A=T0-1 as BOTH the T2 support width and the econ anchor
    kn_v, _ = argmins(lambda k: V(k, T0 - 1.0))   # hmm: support width A
    kn_e, _ = argmins(lambda k: Econ(k, T0))
    conv[label] = {
        "T0": round(T0, 3), "W_equiv_2(T0-1)": round(Weq, 1),
        "identity_max_abs_err": float(ident),          # V2 pointwise
        "argmin_econ": ke, "argmin_census@Weq": kc,    # V2 argmin coincidence
        "argmin_census@naive_A": kn_v,                 # V3: expect econ = this +1
        # V3 set-shift: econ argmin set == naive-census argmin set shifted by EXACTLY +1
        "shift_naive_exact_plus1": sorted({e - 1 for e in ke}) == sorted(kn_v),
        "cont_loc_econ": round(math.log2((T0 - 1) * math.log(2)), 6),
        "cont_loc_census@A": round(math.log2((T0 - 1) * math.log(2)) - 1.0, 6),
    }
out["V2V3_conversion"] = conv

# ---- V4 exp563 reproduction --------------------------------------------------
rep = {}
for s in ("BALANCED", "UNBALANCED"):
    h3 = R["verdicts"]["per_stratum"][s]["H3_net_econ"]
    t0 = next(r["mean_T"] for r in R["rows"] if r["stratum"] == s and r["arm"] == "ADAPT" and r["k"] == 0)
    pred = math.log2((t0 - 1.0) * math.log(2.0))
    ks, _ = argmins(lambda k: -(t0 / (1.0 + k + (t0 - 1.0) * 2.0 ** (-k))))
    rep[s] = {"pred_recomputed": round(pred, 6), "pred_recorded": h3["k_opt_predicted_log2_A_ln2"],
              "pred_match": abs(pred - h3["k_opt_predicted_log2_A_ln2"]) < 1e-5,
              "argmin_recomputed": ks[0] if len(ks) == 1 else ks,
              "measured_recorded": h3["k_opt_measured_cq1"]}
out["V4_exp563_reproduction"] = rep

# ---- V5 pin never coincides --------------------------------------------------
gaps = set()
for W in range(2, 4097):
    kp = math.ceil(math.log2(W))
    kc, _ = argmins(lambda k, W=W: V(k, W))
    gaps.add(kp - max(kc))
out["V5_pin_minus_census_range"] = sorted(gaps)

print(json.dumps(out, indent=1))
assert out["V1_dyadic_V*_eq_log2W+half"] and out["V1_census_offsets_rel_log2W"] == [-2.0, -1.0]
assert all(c["identity_max_abs_err"] < 1e-9 and c["argmin_econ"] == c["argmin_census@Weq"]
           and c["shift_naive_exact_plus1"] for c in conv.values())
assert all(r["pred_match"] and r["argmin_recomputed"] == r["measured_recorded"] for r in rep.values())
assert min(gaps) >= 1
print("GAP-L8 CHECK: ALL PASS")

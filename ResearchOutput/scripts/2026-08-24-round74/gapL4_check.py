#!/usr/bin/env python3
"""GAP L4 finite checks: measure/policy-class for T1 universality on the positional stratum.
Three audits, all <=60s:
  A1 ANCHOR PRECISION: certified-law values at quoted P_hat vs implied-P consistency (paper 219).
  A2 F2 CANONICAL MEASURE: capture curve P(mu)=mu/(1-R^-1/2) for b(r)~r^-3/2 on [1,R];
     required-R inversion per anchor; cross-anchor monotonicity (same-pool) test.
  A3 F1 SHAPE AUDIT at M=64: r-bar decomposition identity EC_A = P*rbar_R+(1-P)*rbar_C;
     uniform-cell diagonal regression (S == finite-M T1a law); off-diagonal closed-form
     violations (S > S_A possible when window sits away from head => closed form NOT an
     upper bound off uniformity); corner values (tail-loaded within-cell arrangement).
Run: python3 gapL4_check.py  -> gapL4_result.json
"""
import json, numpy as np

rng = np.random.default_rng(74)
out = {}

def S_cert(mu, P):   return 1.0 / (mu * P + (1 - P) * (1 - mu))
def S_drafted(mu,P): return 1.0 / (1 - (1 - mu) * P)
def P_implied(S, mu):
    # invert certified law: 1/S = (1-mu) + P(2mu-1)
    return (1.0 / S - (1 - mu)) / (2 * mu - 1)

# ---------- A1 anchor precision ----------
anchors = [  # name, measured S, mu_booked, P_hat_quoted_in_draft/paper219, P_used_for_quoted_law_value
    ("5.19x frontier",  5.19, 0.05, 0.85,   0.85),
    ("6.91x trunc-high",6.91, 0.05, 0.9003, 0.90),
    ("4.35x trunc-low", 4.35, 0.05, 0.8106, None),   # draft computes 4.649 at (.115,.87)
    ("29.1x alpha=1",  29.10, 0.02, 0.9853, 0.985),
]
a1 = []
for name, S, mu, Phat, Plaw in anchors:
    row = {"anchor": name, "S_meas": S, "mu": mu, "P_hat_quoted": Phat,
           "S_cert_at_Phat": round(S_cert(mu, Phat), 4)}
    if Plaw is not None:
        row["P_law_value_computed_at"] = Plaw
        row["S_cert_at_Plaw"] = round(S_cert(mu, Plaw), 4)
        row["precision_gap"] = round(row["S_cert_at_Phat"] - row["S_cert_at_Plaw"], 4)
    row["P_implied_by_S_at_mu"] = None if 2*mu - 1 == 0 else round(P_implied(S, mu), 6)
    a1.append(row)
out["A1_anchor_precision"] = a1

# ---------- A2 canonical measure ----------
# semiprime N=pq, r=q/p>=1, x=p=sqrt(N/r), s=x/sqrt(N)=r^-1/2.
# positional density pi(s) = 2 b(s^-2) s^-3 ; uniform-in-x <=> b(r) ~ r^-3/2.
def capture_canon(mu, R):  # window = top-mu fraction of candidates
    c = 1 - R**-0.5
    return min(1.0, mu / c) if c > 0 else 1.0
def R_required(P, mu):     # invert P = mu/(1-R^-1/2)
    return (1 - mu / P) ** -2

a2 = {"capture_curve_canon": {}, "required_R_per_anchor": {}, "reference_populations": {}}
for mu in (0.02, 0.05, 0.10):
    a2["capture_curve_canon"][f"mu={mu}"] = {f"R={R}": round(capture_canon(mu, R), 4)
                                             for R in (1.042, 1.129, 1.21, 2.0, 4.0, 9.0)}
for name, S, mu, Phat, _ in anchors:
    a2["required_R_per_anchor"][name] = round(R_required(Phat, mu), 4)
# same-pool monotonicity: capture must be nondecreasing in mu; the two extreme anchors pooled:
a2["cross_anchor_monotonicity_violation"] = {
    "P(mu=.02)=0.9853 vs P(mu=.05)=0.85 pooled": 0.9853 > 0.85,
    "verdict": "anchors from DIFFERENT generator settings; pooling into one prior is ill-posed (O2 quantified)"}
for R, lab in [(1.042,"alpha=1-arm implied"), (1.129,"frontier-arm implied"),
               (1.21,"RSA-like r<=1.21"), (2.0,"hard-balance U[1,2]"), (9.0,"wide r<=9")]:
    a2["reference_populations"][lab] = {"P(mu=.05)": round(capture_canon(0.05, R), 4),
                                        "P(mu=.02)": round(capture_canon(0.02, R), 4)}
out["A2_F2_canonical_measure"] = a2

# ---------- A3 F1 shape audit ----------
M = 64
pos = np.arange(1, M + 1)          # descending scan ranks: position 1 = sqrt-N head
def audit(pi, idx_R):
    """r-bar identity + all bookings for prior pi (len M) and window indices idx_R.
    Within-block scan ranks are BLOCK-LOCAL: scanning R top-down visits its members
    in global-descending order, so their costs are 1..|R| regardless of placement."""
    P = pi[idx_R].sum()
    maskR = np.zeros(M, bool); maskR[idx_R] = True
    rR = np.arange(1, len(idx_R) + 1)                          # block-local descending ranks
    rC = np.arange(1, M - len(idx_R) + 1)
    pR = pi[idx_R]; pC = pi[~maskR]
    rbar_R = (pR * rR).sum() / P if P > 0 else 0.0            # mean scan-rank within R
    rbar_C = (pC * rC).sum() / (1 - P) if P < 1 else 0.0
    EC_A = P * rbar_R + (1 - P) * rbar_C                       # protocol-A committed, certifying silence
    C_desc = (pi * pos).sum()
    C_sort = (np.sort(pi)[::-1] * pos).sum()
    lam = C_sort / C_desc                                      # L7 Lambda in (0,1]
    mu_w = len(idx_R) / M
    return P, rbar_R, rbar_C, EC_A, C_desc, C_sort, lam, mu_w

trials = 4000
viol_closedform = 0; diag_err = []; ratios = []; taus = []
for t in range(trials):
    alpha = float(np.exp(rng.uniform(np.log(0.05), np.log(5.0))))
    pi = rng.dirichlet(np.full(M, alpha))
    mu_w = float(rng.choice([0.02, 0.05, 0.10]))
    k = max(1, int(round(mu_w * M)))
    # mix of head / mid / tail window placements (geometry matters off-uniformity)
    start = int(rng.choice([0, (M - k)//2, M - k]))
    idx_R = np.arange(start, start + k)
    P, rr, rc, EC, Cdesc, Csort, lam, mw = audit(pi, idx_R)
    if P <= 0 or P >= 1: continue
    S = Cdesc / EC
    S_A = S_cert(mw, P)
    ratios.append((S, S_A, lam, rr / (mw*M) if mw>0 else 0))
    if S > S_A: viol_closedform += 1
# uniform-diagonal regression: uniform pi forces P=mu; finite-M law must hold EXACTLY
for mw_frac in (0.02, 0.05, 0.10, 0.25, 0.5):
    k = max(1, int(round(mw_frac * M))); pi = np.full(M, 1.0/M)
    for start in {0, (M-k)//2, M-k}:
        idx_R = np.arange(start, start + k)
        P, rr, rc, EC, Cdesc, *_ = audit(pi, idx_R)
        S_finite = (M+1) / (P*(k+1) + (1-P)*(M-k+1))
        diag_err.append(abs(Cdesc/EC - S_finite))
out["A3_F1_shape_audit"] = {
    "M": M, "trials": trials,
    "uniform_diagonal_max_abs_err": float(max(diag_err)),
    "offdiagonal_S_gt_SA_violations": viol_closedform,
    "violation_rate": round(viol_closedform / max(1,len(ratios)), 4),
    "max_S_over_SA_observed": round(max(r[0]/r[1] for r in ratios), 2),
    "note": "closed form in (mu,P) alone is NOT an upper bound off uniform-within-cells "
            "(window-away-from-head priors exceed it unboundedly); the universal object is the "
            "rbar-identity EC_A = P*rbar_R + (1-P)*rbar_C",
}
# explicit 77x-style witness: mass uniform on first half of a BOTTOM window
pi = np.zeros(M); k = int(0.05*M); start = M-k
half = k//2
pi[start:start+half] = 1.0/half
P, rr, rc, EC, Cdesc, Csort, lam, mw = audit(pi, np.arange(start, start+k))
out["A3_explicit_offdiag_witness"] = {
    "S_measured": round(Cdesc/EC, 2), "S_cert(mu,P)": round(S_cert(mw, P), 2),
    "tail_loading_tau_R": round(rr/(mw*M), 3),
    "comment": "single prior drives S far above the booked closed form => any fixed (mu,P) law "
               "needs shape bookkeeping (tau, Lambda); supports F1/F3 framing"}

with open("/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74/gapL4_result.json", "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1)[:3000])

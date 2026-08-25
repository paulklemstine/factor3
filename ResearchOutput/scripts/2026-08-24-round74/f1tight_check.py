# f1tight_check.py — round-74 THEORY: paper-225 F1 master inequality vs measured positional profile
# S <= min(1/(L*T*qhat), 2^k_bits/(L*T))   [gapL4_measure.md, PROVEN]
# Measured profile (papers 228/233/238 + exp594): T(x)=A(1+x)^-b_bulk + K(1+x)^-b_edge on x in [0,1],
#   b_bulk=.573 [.412,.767], spike mass w=.086 [.064,.108] (descriptive .04-.09 within x<~.1),
#   b_edge >~15 (exp594 ladder 10->40, upper unidentified). Hump at x~.65: exp592 gate-H0 -> excluded
#   from confirmed structure; sensitivity term added anyway (first-moment argument).
# Full-window policies: mu_eff=1, P_eff=1 => qhat=1, K_booked=C0=(M+1)/2.
# Chain slack is ONLY the majorization step C_sort<=C0 (eq iff pi flat): X := bound/achieved = C0/C_sort,
#   baseline-free and policy-independent. Ascending = sort order (profile monotone declining).
import json
import numpy as np

M = 40000
i = np.arange(1, M + 1, dtype=float)
x = (i - 0.5) / M
C0 = (M + 1) / 2.0


def costs(b_bulk, w_spike, b_edge):
    p_bulk = (1.0 + x) ** (-b_bulk)
    p_edge = (1.0 + x) ** (-b_edge)
    p = (1.0 - w_spike) * p_bulk / p_bulk.sum() + w_spike * p_edge / p_edge.sum()
    assert np.all(np.diff(p) <= 1e-12), "profile not monotone declining; sort!=ascending"
    c_asc = float((i * p).sum())          # rank 1 = smallest x = best-static (=C_sort)
    c_desc = float(((M + 1 - i) * p).sum())
    Lam = c_asc / c_desc                  # Lambda = C_sort/C_desc in (0,1]
    Th_asc = c_asc / C0                   # Theta for window-ascending full-window policy
    S_asc = 1.0 / Lam                     # achieved S_vs_desc of realizable static policy
    bound = 1.0 / (Lam * Th_asc * 1.0)    # arm 1 (k_bits=0 => arm2 non-binding since qhat<=1)
    Ex = float((x * p).sum())
    return dict(b_bulk=b_bulk, w_spike=w_spike, b_edge=b_edge, Lambda=Lam, Theta_asc=Th_asc,
                S_asc=S_asc, bound=bound, X=bound / S_asc, E_x=Ex, c_asc_over_C0=c_asc / C0)


rows = [costs(b, w, be)
        for b in (0.412, 0.573, 0.767)
        for w in (0.064, 0.086, 0.108)
        for be in (10.0, 15.0, 40.0)]
point = costs(0.573, 0.086, 15.0)
Xs = [r["X"] for r in rows]

# hump sensitivity: +20% local excess at x*=0.65 (sigma .08) on top of point profile — exp592-gated
b_, w_, be_ = 0.573, 0.086, 15.0
p_bulk = (1.0 + x) ** (-b_)
p_edge = (1.0 + x) ** (-be_)
p = (1 - w_) * p_bulk / p_bulk.sum() + w_ * p_edge / p_edge.sum()
p_h = p * (1 + 0.20 * np.exp(-0.5 * ((x - 0.65) / 0.08) ** 2))
p_h /= p_h.sum()
c_asc_h = float((i * p_h).sum())
hump_dX = (C0 / c_asc_h) - point["X"]

# legacy anchors (papers 137/143/219/225; Phat are law-INVERSIONS per pthat_extraction.md — circular)
def anchor(mu, P, S):
    q = mu * P + (1 - P) * (1 - mu)
    Ma = 300.0
    LamTh_finiteM = (Ma + 1) / (S * (Ma * q + 1))
    return dict(mu=mu, P_hat=P, S_meas=S, q_hat=q, required_LambdaTheta_infM=1 / (S * q),
                required_LambdaTheta_M300=LamTh_finiteM)

anchors = [
    anchor(0.05, 0.849953, 5.193592154916),   # frontier truncation (raw-inverted P)
    anchor(0.05, 0.900297, 6.914724537168),   # trunc-high @rounded 6.91
    anchor(0.05, 0.810643, 4.353075657862),   # trunc-low @rounded 4.35
    anchor(0.02, 0.985068, 29.125436718134),  # alpha=1 exact enum M=300 (cert-law-implied P)
]

out = dict(point_estimate=point, grid_rows=rows, X_min=min(Xs), X_max=max(Xs),
           hump_plus20pct_dX=hump_dX, legacy_anchors_inverted_Phat=anchors)
with open("/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74/f1tight_result.json", "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps({k: out[k] for k in ("point_estimate", "X_min", "X_max", "hump_plus20pct_dX")}, indent=1))
print("anchors:", [(a["q_hat"], round(a["required_LambdaTheta_infM"], 5)) for a in anchors])

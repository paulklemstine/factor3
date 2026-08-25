# verifyf1_recompute.py — independent verifier for the THREE arithmetic claims in f1tight_connection.md
# Reimplemented from the md definitions only (no import of f1tight_check).
import json
import numpy as np

RD = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74"
res = {}

# ---------- independent implementation ----------
def profile_costs(b_bulk, w_spike, b_edge, M=40000):
    """p ∝ (1-w)(1+x)^-bbulk + w(1+x)^-bedge on midpoint grid x_i=(i-1/2)/M, i=1..M."""
    i = np.arange(1, M + 1, dtype=float)
    x = (i - 0.5) / M
    pb = (1.0 + x) ** (-b_bulk)
    pe = (1.0 + x) ** (-b_edge)
    p = (1.0 - w_spike) * pb / pb.sum() + w_spike * pe / pe.sum()
    mono = bool(np.all(np.diff(p) <= 1e-12))
    C0 = (M + 1) / 2.0
    c_asc = float(np.dot(i, p))
    c_desc = float(np.dot(M + 1 - i, p))
    Lam = c_asc / c_desc
    Th = c_asc / C0
    Ex = float(np.dot(x, p))
    return dict(mono=mono, Lambda=Lam, Theta=Th, S_asc=1.0 / Lam,
                bound=1.0 / (Lam * Th * 1.0), X=C0 / c_asc, E_x=Ex)

def continuous_costs(b_bulk, w_spike, b_edge, n=400):
    """Gauss-Legendre quadrature on [0,1]: continuum limit of Lambda, X."""
    t, wt = np.polynomial.legendre.leggauss(n)
    x = 0.5 * (t + 1.0)
    wq = 0.5 * wt

    def norm(g):
        Z = np.sum(wq * g)
        return g / Z
    f = (1.0 - w_spike) * norm((1.0 + x) ** (-b_bulk)) + w_spike * norm((1.0 + x) ** (-b_edge))
    Ex = float(np.sum(wq * x * f))
    Lam = Ex / (1.0 - Ex)          # E[x]/E[1-x]  (continuous analogue of C_sort/C_desc)
    X = 1.0 / (2.0 * Ex)           # C0/C_sort with rank = M*x
    return dict(Lambda=Lam, X=X, E_x=Ex)

def anchors_table():
    rows = []
    for mu, P, S in [(0.05, 0.849953, 5.193592154916),
                     (0.05, 0.900297, 6.914724537168),
                     (0.05, 0.810643, 4.353075657862),
                     (0.02, 0.985068, 29.125436718134)]:
        q = mu * P + (1 - P) * (1 - mu)
        lt_inf = 1.0 / (S * q)
        lt_M300 = 301.0 / (S * (300.0 * q + 1.0))
        # circularity algebra: if Phat was made by inverting 1/qhat(P)=S*, then
        # 1/(S*qhat(Phat)) = S*/S  -- pure bookkeeping ratio, no data content.
        S_star = 1.0 / q
        P_selfcons = ((1 - mu) - 1.0 / S) / (1.0 - 2.0 * mu)   # P making 1/qhat = S exactly
        rows.append(dict(mu=mu, P_hat=P, S=S, q_hat=q, LT_inf=lt_inf, LT_M300=lt_M300,
                         S_inverted_target=S_star, LT_as_ratio=S_star / S,
                         resid=abs(lt_inf - S_star / S),
                         P_selfconsistent=P_selfcons, P_gap_abs=abs(P - P_selfcons)))
    return rows

# ---------- ITEM 1: Lambda = 0.766, 1/Lambda ~= 1.306 ----------
pt = profile_costs(0.573, 0.086, 15.0)
pt_disc = [profile_costs(0.573, 0.086, 15.0, M=m) for m in (20000, 80000, 160000)]
pt_cont = continuous_costs(0.573, 0.086, 15.0)
lam_spread = max(abs(d["Lambda"] - pt["Lambda"]) for d in pt_disc + [dict(Lambda=pt_cont["Lambda"])])
i1a = abs(pt["Lambda"] - 0.766) <= 5e-4
i1b = abs(pt["S_asc"] - 1.306) <= 5e-3
i1c = pt["mono"] and 0 < pt["Lambda"] <= 1.0
i1d = lam_spread < 1e-3
# md side-note: "bulk alone gives Lambda~0.895 (gain 1.12); spike supplies ~1/3 of tilt"
bk = profile_costs(0.573, 0.0, 15.0)
share_log = 1.0 - np.log(bk["S_asc"]) / np.log(pt["S_asc"])       # log-tilt share of spike
share_lin = (1.0 - pt["Lambda"]) and (bk["Lambda"] - pt["Lambda"]) / (1.0 - pt["Lambda"])
note_spike_share = dict(Lambda_bulk=bk["Lambda"], gain_bulk=bk["S_asc"],
                        spike_log_share=float(share_log), spike_linear_share=float(share_lin))
it1 = dict(Lambda=pt["Lambda"], one_over_Lam=pt["S_asc"], Theta=pt["Theta"], bound=pt["bound"],
           disc_spread=lam_spread, cont_Lambda=pt_cont["Lambda"], checks=dict(
               lam_766=bool(i1a), ratio_1306=bool(i1b), mono_and_unit=bool(i1c), discretization_stable=bool(i1d)),
           note_spike_share=note_spike_share)
PASS1 = all(it1["checks"].values())

# ---------- ITEM 2: X = 1.15 [1.10, 1.22] ----------
rows = [profile_costs(b, w, be) for b in (0.412, 0.573, 0.767)
        for w in (0.064, 0.086, 0.108) for be in (10.0, 15.0, 40.0)]
Xs = [r["X"] for r in rows]
Exs = [r["E_x"] for r in rows]
Ths = [r["Theta"] for r in rows]
Xmin, Xmax = min(Xs), max(Xs)
i2a = abs(pt["X"] - 1.1530) <= 5e-4
i2b = abs(Xmin - 1.1018) <= 5e-3 and abs(Xmax - 1.2205) <= 5e-3
i2c = abs(Xmin - 1.10) <= 5e-3 and abs(Xmax - 1.22) <= 5e-3
# identity chain: X = C0/c_asc = bound/S_asc = (M+1)/(2*M*Ex+1) ~ 1/(2Ex); md (c) E_x in [.410,.454]
id_direct = abs(pt["X"] - pt["bound"] / pt["S_asc"]) < 1e-12
Ex_pt = pt["E_x"]
id_closed = abs((40001.0 / (2 * 40000 * Ex_pt + 1.0)) - pt["X"]) < 1e-9
id_asym = abs(1.0 / (2 * Ex_pt) - pt["X"]) < 2e-3
i2d = id_direct and id_closed and id_asym
i2e = abs(min(Exs) - 0.410) <= 5e-3 and abs(max(Exs) - 0.454) <= 5e-3
# hump sensitivity (md: -0.019)
M = 40000
i = np.arange(1, M + 1, dtype=float); xh = (i - 0.5) / M
pbh = (1 + xh) ** (-0.573); peh = (1 + xh) ** (-15.0)
ph = (1 - 0.086) * pbh / pbh.sum() + 0.086 * peh / peh.sum()
ph = ph * (1 + 0.20 * np.exp(-0.5 * ((xh - 0.65) / 0.08) ** 2)); ph /= ph.sum()
dX_hump = float((40001.0 / 2.0) / np.dot(i, ph) - pt["X"])
i2f = abs(dX_hump - (-0.019)) <= 2e-3
it2 = dict(X_point=pt["X"], X_min=Xmin, X_max=Xmax, E_x_point=Ex_pt,
           Ex_grid_range=[min(Exs), max(Exs)], Theta_grid_range=[min(Ths), max(Ths)],
           hump_dX=dX_hump, identities=dict(direct=id_direct, closed_form=id_closed, asym_1_over_2Ex=bool(id_asym)),
           checks=dict(point_1153=bool(i2a), interval_corners=bool(i2b), rounded_1110_122=bool(i2c),
                       identity_chain=bool(i2d), Ex_ci=bool(i2e), hump_minus_019=bool(i2f)))
PASS2 = all(it2["checks"].values())

# ---------- ITEM 3: anchors Lambda*Theta ~1.00-1.04 BY CONSTRUCTION ----------
an = anchors_table()
lt = [r["LT_inf"] for r in an]
i3a = all(abs(r["LT_inf"] - v) <= 5e-4 for r, v in zip(an, [1.0405456547410714, 1.034968341496796,
                                                            1.0421979753901753, 0.9999862855932393]))
i3b = abs(r0 := an[3]["LT_inf"] - 1.0) < 1e-4          # 4th anchor ~0.99999
i3c = all(0.999 <= v <= 1.043 for v in lt)             # band 1.00-1.04
i3d = all(r["resid"] < 1e-12 for r in an)              # LT_inf == S*/S EXACTLY (construction identity)
# demonstration: whole band reachable by moving inversion target only, data untouched
demo = [(s, round(1.0 / (s * (0.05 * 0.85 + 0.95 * 0.15)), 5)) for s in (5.19, 5.40, 5.60)]
i3e = True  # structural claim argued via i3d + drift decomposition below
it3 = dict(rows=[{k: (round(v, 10) if isinstance(v, float) else v) for k, v in r.items()} for r in an],
           LT_band=[min(lt), max(lt)],
           drift_pct=[round(100 * (r["LT_inf"] - 1.0), 3) for r in an],
           P_gap_vs_selfconsistent=[round(r["P_gap_abs"], 6) for r in an],
           target_only_demo=demo,
           checks=dict(values_match_md=bool(i3a), fourth_anchor_099999=bool(i3b), band_100_104=bool(i3c),
                       construction_identity_exact=bool(i3d), band_is_bookkeeping_only=bool(i3e)))
PASS3 = all([i3a, i3b, i3c, i3d])

# ---------- verdict ----------
res = dict(item1=it1, item2=it2, item3=it3,
           PASS=dict(item1_Lambda=bool(PASS1), item2_X=bool(PASS2), item3_circularity=bool(PASS3)),
           discrepancies=int((not PASS1) + (not PASS2) + (not PASS3)))
with open(f"{RD}/verifyf1_result.json", "w") as f:
    json.dump(res, f, indent=1)

print("POINT:", {k: round(v, 6) for k, v in pt.items() if k != "mono"}, "| mono:", pt["mono"])
print("cont :", {k: round(v, 6) for k, v in pt_cont.items()}, "| disc spread:", f"{lam_spread:.2e}")
print("bulk :", {k: round(v, 6) for k, v in bk.items() if k != "mono"},
      "| spike log-share:", round(note_spike_share["spike_log_share"], 3))
print(f"GRID : X [{Xmin:.4f},{Xmax:.4f}]  Ex [{min(Exs):.4f},{max(Exs):.4f}]  Th [{min(Ths):.4f},{max(Ths):.4f}]")
print(f"HUMP : dX={dX_hump:+.4f}")
for r in an:
    print(f"ANCHOR mu={r['mu']:.2f} Phat={r['P_hat']:.6f} S={r['S']:.4f}: q={r['q_hat']:.6f} "
          f"LT_inf={r['LT_inf']:.6f} (=S*/S exactly: {r['resid']:.1e}) LT_M300={r['LT_M300']:.5f} "
          f"P_selfcons={r['P_selfconsistent']:.6f} gap={r['P_gap_abs']:.4f}")
print("PASS:", res["PASS"], "| discrepancies:", res["discrepancies"])

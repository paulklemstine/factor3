#!/usr/bin/env python3
"""exp574b: finite checks for the barrier-4 positional-converse draft (T1/T2).

Checks, all < 60 s:
  A. residue cap: max_theta 1/(1-theta+theta^2) = 4/3 at theta=1/2   (paper-132 anchor)
  B. T2 saturation census: k_opt (cost-optimal adaptive stop), k_pin (=log2 W),
     k_marginal (last worthwhile query) -- pins the exp563 "k*=ceil(log2 W)" definition.
  C. exhaustive DP over ALL adaptive comparison policies (uniform prior, supports <=128):
     * dyadic W: V(W) == min_k [k + (W/2^k + 1)/2] EXACTLY (idealized identity holds);
     * general L: closed form min_k [k + (ceil(L/2^k)+1)/2] is an UPPER bound on V,
       undercut by the true optimum by < 1/2 (integrality wobble, measured).
  D. T1 protocol algebra: fire-or-silent law 1/(1-(1-mu)*P_hit) vs announce-always
     law 1/(1+mu-P_hit); locus of (mu,P_hit) reproducing the 5.19x / 6.91x / 4.35x
     / 29.1x anchors.
"""
import json

out = {}

# ---------- A. residue cap ----------
best = max((1.0/(1-t+t*t), t) for t in [i/1000 for i in range(1001)])
assert abs(best[0]-4/3) < 2e-3 and abs(best[1]-0.5) < 0.002, best
out["A_residue_cap"] = {"max_speedup": round(best[0], 6), "argmax_theta": best[1]}

# ---------- C. T2: exhaustive DP ----------
def dp_all(Lmax):
    """V[L] = min expected total cost (query costs 1 trial unit; residual top-down
    scan of support s costs (s+1)/2), uniform prior; also records argmin split."""
    V = {0: 0.0, 1: 1.0}
    choice = {}
    for L in range(2, Lmax+1):
        stop = (L+1)/2.0
        bx, bv = None, stop
        for x in range(1, L):
            val = 1 + (x/L)*V[x] + ((L-x)/L)*V[L-x]
            if val < bv:
                bv, bx = val, x
        V[L] = bv
        choice[L] = bx if bv < stop else 'STOP'
    return V, choice

def cf_upper(L):
    return min(k + (-(-L // (2**k)) + 1)/2.0 for k in range(0, 2*L.bit_length()+3))

V, choice = dp_all(128)
dev = [(V[L] - cf_upper(L), L) for L in range(2, 129)]
min_dev = min(dev)   # deepest undercut: true optimum below naive closed form
dyadic_exact = []
for e in range(1, 8):
    W = 2**e
    cfl = min(k + (W/(2**k) + 1)/2.0 for k in range(0, e+3))
    dyadic_exact.append({"W": W, "dp": round(V[W], 9), "closed": round(cfl, 9),
                         "exact": abs(V[W]-cfl) < 1e-9})
out["C_dp_check"] = {
    "supports_exhaustively_checked": 127,
    "closed_form_is_UPPER_bound": all(d <= 1e-9 for d, _ in dev),
    "deepest_undercut_of_closed_form": {"delta": round(min_dev[0], 6), "at_L": min_dev[1]},
    "dyadic_supports": dyadic_exact,
}

# ---------- B. saturation census ----------
census = []
for e in range(1, 21):
    W = 2 ** e
    k_opt = min(range(0, e+3), key=lambda k: k + (W/(2**k) + 1)/2.0)
    C_star = k_opt + (W/(2**k_opt) + 1)/2.0
    # last worthwhile query: marginal saving of the (k+1)-th is ~W/2^(k+2) >= 1
    k_marg = max(k for k in range(e+3) if W/(2**(k+2)) >= 1.0) if W >= 4 else 0
    census.append({"W": W, "log2W": e, "k_opt_cost": k_opt, "C_star": round(C_star, 4),
                   "k_pin_log2W": e, "k_last_worthwhile": k_marg})
out["B_census"] = census

# ---------- D. T1 protocol laws ----------
sp_fos = lambda mu, P: 1.0/(1 - (1-mu)*P)   # fire-or-silent (= paper-138 master form)
sp_aa  = lambda mu, P: 1.0/(1 + mu - P)     # announce-always
anchors = {}
for name, target in [("5.19x_p137", 5.19), ("6.91x_trunc_hi", 6.91),
                     ("4.35x_trunc_lo", 4.35), ("29.1x_a1", 29.1)]:
    loc = [(round(mu, 3), round((1 - 1/target)/(1 - mu), 4))
           for mu in (0.02, 0.03, 0.05, 0.115)]
    anchors[name] = loc
examples = [{"mu": mu, "P_hit": P, "fire_or_silent": round(sp_fos(mu, P), 4),
             "announce_always": round(sp_aa(mu, P), 4)}
            for mu in (0.02, 0.05) for P in (0.85, 0.90, 1.0)]
out["D_t1_protocols"] = {"anchors_fos_locus_(mu,P)": anchors, "example_values": examples}

with open("/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74/exp574b_result.json", "w") as f:
    json.dump(out, f, indent=1)

print("A:", out["A_residue_cap"])
print("C:", {k: v for k, v in out["C_dp_check"].items() if k != "dyadic_supports"})
print("C dyadic:", [(d["W"], d["exact"]) for d in dyadic_exact])
print("B census head/tail:")
for r in census[:3] + census[-2:]:
    print("  ", r)
print("D anchors:", json.dumps(anchors))
print("D examples:", examples)

#!/usr/bin/env python3
"""EXP 491 TABLE-CLOSURE lean (round-42). Exact g/Is/A/X channels n=2..25.
PRE-STATED: H1 Is >= max(g,A,X) everywhere (A overtakes X from n=8); H2 each channel -> 0;
H3 X/g -> 2 within 10% by n=25.
"""
import json, math
OUT = {}
def H(pv):
    # LEDGER v1: unnormalized input (g's first term sums > 1) -> negative "entropies".
    s = sum(pv)
    pv = [p/s for p in pv]
    return -sum(p*math.log2(p) for p in pv if p > 0)
rows = []
for n in range(2, 26):
    # LEDGER v2: v1's distributions didn't sum to 1 (g's pair, Is's middle element 1/n
    # instead of ((n-1)/n)^2); the v1 'fix' (normalize) silently DISTORTED values instead
    # of erroring. Exact binomial complements below.
    g = H([(2*n-1)/n**2, (n-1)**2/n**2]) - (1/n)*H([1/n, (n-1)/n]) - ((n-1)/n)*H([2/n, (n-2)/n])
    Is = H([(n-1)**2/n**2, 2*(n-1)/n**2, 1/n**2]) - (1/n)*H([(n-1)/n, 0, 1/n]) - ((n-1)/n)*H([(n-2)/n, 2/n, 0])
    A = H([1/n**2, 1-1/n**2]) - (1/n)*H([1/n, (n-1)/n])
    X = H([2*(n-1)/n**2, 1-2*(n-1)/n**2]) - ((n-1)/n)*H([2/n, (n-2)/n])
    rows.append(dict(n=n, g=g, Is=Is, A=A, X=X))
OUT["table"] = rows
# H1 checks
viol_Is = [r["n"] for r in rows if r["Is"] < max(r["g"], r["A"], r["X"]) - 1e-12]
viol_Ag = [r["n"] for r in rows if r["A"] < r["g"] - 1e-12]
xover = next((r["n"] for r in rows if r["A"] > r["X"]), None)
OUT["H1"] = {"Is_dominates": not viol_Is, "violations": viol_Is,
             "A_ge_g_everywhere": not viol_Ag, "A_overtakes_X_at_n": xover}
# H2: all -> 0
r25 = rows[-1]
OUT["H2"] = {k: round(r25[k], 8) for k in ("g","Is","A","X")}
# H3: X/g ratio at n=5,10,15,20,25
OUT["H3"] = {r["n"]: round(r["X"]/r["g"], 4) for r in rows if r["n"] in (5,10,15,20,25)}
json.dump(OUT, open("/tmp/exp42_tables/result.json", "w"), indent=1)
print("H1:", OUT["H1"])
print("H2 n=25 values:", OUT["H2"])
print("H3 X/g ratios:", OUT["H3"])

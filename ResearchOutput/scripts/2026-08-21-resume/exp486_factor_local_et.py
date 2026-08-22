#!/usr/bin/env python3
"""EXP 486 FACTOR-LOCAL-ET lean (round-41 #2). Seed 20260920. Inline takeover.
Unified (alpha, c) expected-cost plane: log2 E[T_M] = alpha*log2(min(p,q)) + c per method.
Methods: trial division, Pollard rho (Floyd), Fermat. ECM DROPPED for budget (disclosed).
H3 predictions: rho ~ (0.5, .); trial div ~ (1.0, .); Fermat ~ (1.0 w/ balance term, .).
Populations: 1500 balanced semiprimes per k in {16,20,24}; censoring at iter caps, disclosed.
"""
import json, time, math
import numpy as np
import gmpy2
from sympy import nextprime, primerange

SEED = 20260920
rng = np.random.default_rng(SEED)
T0 = time.time()
OUT = {"meta": {"seed": SEED, "exp": 486, "codename": "FACTOR-LOCAL-ET-LEAN",
                "ecm": "dropped for budget"}}
def checkpoint():
    json.dump(OUT, open("/tmp/exp41_flet/result.json", "w"), indent=1)

rows = []
for k in (16, 20, 24):
    h = k // 2
    lo, hi = 2**(h-1), 2**h
    data = []
    while len(data) < 1500:
        r = int(rng.integers(lo, hi))
        p = int(nextprime(r)); q = int(nextprime(int(p * 4) if False else p + int(rng.integers(1, max(2**(h-3), 2)))))
        if p < lo or q >= hi or q <= p or p == q: continue
        N = p*q
        if N.bit_length() != k: continue
        data.append((N, min(p, q)))
    res = dict(k=k, n=len(data))
    # trial division: count primes tested until p
    plist = np.array(sorted(primerange(2, 2**h + 10)), dtype=np.int64)
    td_costs, rho_costs, fe_costs, ps = [], [], [], []
    pmax = 2**h
    for N, p in data:
        sq = math.isqrt(N)
        td = int(np.searchsorted(plist[plist <= sq], p) + 1)
        td_costs.append(td)
        # pollard rho floyd on N mod nothing: standard x^2+1
        x, y, d, it = 2, 2, 1, 0
        while d == 1 and it < 100000:
            x = (x*x + 1) % N
            y = (y*y + 1) % N; y = (y*y + 1) % N
            d = math.gcd(abs(x - y), N); it += 1
        ok_rho = (d != N) and it < 100000
        rho_costs.append(it if ok_rho else None)
        # fermat from ceil(sqrt N)
        a = math.isqrt(N)
        if a*a < N: a += 1
        itf = 0
        b2 = a*a - N
        while math.isqrt(b2)**2 != b2 and itf < 2000000:
            a += 1; b2 = a*a - N; itf += 1
        ok_fe = math.isqrt(b2)**2 == b2 and itf < 2000000
        fe_costs.append(itf if ok_fe else None)
        ps.append(float(p))
    res["cens"] = {"rho": sum(c is None for c in rho_costs),
                   "fermat": sum(c is None for c in fe_costs)}
    lg = lambda xs: [math.log2(v) for v in xs]
    def fit(costs):
        cc = [c for c in costs if c is not None and c > 0]
        X = np.array(lg(ps)); Y = np.array([math.log2(c) for c in cc])
        m, b = np.polyfit(X[:len(cc)] if len(X)==len(Y) else X, Y, 1)
        return float(m), float(b), float(np.mean(cc))
    # align lengths: costs lists may be shorter after censoring -> use only non-censored indices
    # LEDGER v1: zero-cost hits (itf=0) dropped from y but kept in x -> length mismatch.
    keep_r = [i for i, c in enumerate(rho_costs) if c is not None and c > 0]
    keep_f = [i for i, c in enumerate(fe_costs) if c is not None and c > 0]
    res["fit_td"] = dict(zip(("alpha","c","meanT"), fit(td_costs)))
    res["fit_rho"] = dict(alpha=float(np.polyfit(np.array(lg(ps))[keep_r], np.log2([rho_costs[i] for i in keep_r]), 1)[0]),
                          meanT=float(np.mean([rho_costs[i] for i in keep_r])))
    res["fit_fermat"] = dict(alpha=float(np.polyfit(np.array(lg(ps))[keep_f], np.log2([fe_costs[i] for i in keep_f]), 1)[0]),
                             meanT=float(np.mean([fe_costs[i] for i in keep_f])))
    rows.append(res)
    OUT.setdefault("cells", []).append(res)
    checkpoint()
    print({kk: (round(vv,3) if isinstance(vv,float) else vv) for kk, vv in
           [("k",k)] + [(f"td_alpha",res["fit_td"]["alpha"]),
                        ("rho_alpha",res["fit_rho"]["alpha"]),
                        ("fe_alpha",res["fit_fermat"]["alpha"]),
                        ("cens",res["cens"]["rho"]) ]}, flush=True)

OUT["verdict"] = {
    "expected": {"trial_division": "alpha~1.0", "rho": "alpha~0.5", "fermat": "alpha~1.0+balance"},
    "note": "per-k alphas averaged; compare vs H3"}
checkpoint()
print("DONE", round(time.time()-T0,1), "s")

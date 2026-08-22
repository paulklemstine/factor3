#!/usr/bin/env python3
"""EXP 487 ECM-COMPLETION lean (round-42). Seed 20260921. Inline takeover.
ECM-only column for paper 154's unified plane: across-k E[T] scaling at fixed B1=50,
curves capped at 30, ops = point additions. Balanced semiprimes, k in {16,20}.
PRE-STATED: H1 alpha_ECM in [0.6, 0.8]; H2 ECM intercept advantage over rho bounded
(log2 meanT ratio < log2(10) = 3.32); H3 censoring < 5% at k=16, < 15% at k=20.
"""
import json, time, math
import numpy as np
import gmpy2
from sympy import nextprime

SEED = 20260921
rng = np.random.default_rng(SEED)
T0 = time.time()
OUT = {"meta": {"seed": SEED, "exp": 487, "codename": "ECM-COMPLETION",
                "B1": 50, "curve_cap": 30}}
def checkpoint():
    json.dump(OUT, open("/tmp/exp42_ecm/result.json", "w"), indent=1)

def ecm_factor(N, B1=50, curves=30):
    """Return (found, total_point_additions). Affine curve attempts a=0..; Suyama-ish param."""
    ops = 0
    if N % 2 == 0:
        return True, 0
    for c in range(curves):
        a = int(rng.integers(6, max(N, 7)))
        x = int(rng.integers(2, max(N, 3))); y = int(rng.integers(2, max(N, 3)))
        # LEDGER v1: at j=2 the running point EQUALS the base -> generic addition had
        # zero denominator -> instant 'degenerate' on every curve (0/1200 found).
        # Fixed: explicit doubling for j=2. SCOPE NOTE: sequential multiples j=3..B1 =
        # ECM-LITE (rho-like scaling expected), NOT lcm-based true ECM.
        px, py = x % N, y % N
        dead = False
        den = (2*py) % N
        g = math.gcd(den, N)
        if 1 < g < N: return True, ops
        if g == N: continue
        try:
            lam = (3*px*px + a) * pow(den, -1, N) % N
            nx = (lam*lam - 2*px) % N
            ny = (lam*(px - nx) - py) % N
            ops += 4
            px, py = nx, ny
            for j in range(3, B1 + 1):
                den = (px - x) % N
                g = math.gcd(den, N)
                if 1 < g < N: return True, ops
                if g == N: dead = True; break
                lam = ((py - y) * pow(den, -1, N)) % N
                nx = (lam*lam - px - x) % N
                ny = (lam*(px - nx) - py) % N
                ops += 3
                px, py = nx, ny
        except (ValueError, ZeroDivisionError):
            dead = True
        if dead: continue
    return False, ops

rows = []
for k in (16, 20):
    h = k // 2
    lo, hi = 2**(h-1), 2**h
    data = []
    while len(data) < 1200:
        r = int(rng.integers(lo, hi))
        p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, max(2**(h-3), 2)))))
        if p < lo or q >= hi or q <= p or p == q: continue
        N = p*q
        if N.bit_length() != k: continue
        data.append((N, min(p, q)))
    found, costs, cens = [], [], 0
    for N, p in data:
        ok, ops = ecm_factor(N)
        if ok:
            costs.append(max(ops, 1))
        else:
            cens += 1
    lg = lambda xs: [math.log2(v) for v in xs]
    keep_p = [math.log2(data[i][1]) for i in range(len(data)) if i < len(costs)]
    alpha = float(np.polyfit(np.array(lg([data[i][1] for i in range(len(costs))])),
                             np.log2(costs), 1)[0]) if len(costs) > 10 else None
    row = dict(k=k, n=len(data), found=len(costs), censored=cens,
               mean_ops=float(np.mean(costs)) if costs else None,
               alpha_ecm=alpha,
               log2_meanT=round(math.log2(np.mean(costs)), 3) if costs else None)
    rows.append(row); OUT.setdefault("cells", []).append(row); checkpoint()
    print(row, round(time.time()-T0,1), "s", flush=True)

if len(rows) == 2 and all(r["log2_meanT"] for r in rows):
    slope = (rows[1]["log2_meanT"] - rows[0]["log2_meanT"]) / 4
    OUT["across_k_slope_per_log2p"] = round(slope, 4)
    OUT["verdict"] = {
        "H1_0.6_to_0.8": bool(0.6 <= slope <= 0.8),
        "H3_note": "intercept comparison needs rho re-run on same pop — deferred"}
checkpoint()
print(json.dumps(OUT.get("verdict", {})))
print("DONE", round(time.time()-T0,1), "s")

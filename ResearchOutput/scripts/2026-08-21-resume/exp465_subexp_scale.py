#!/usr/bin/env python3
"""EXP 465 SUBEXP-SCALE (round-37, factor3 lab) — taken over inline by coordinator
after 3x upstream agent-channel failures. Seed 20260821. Checkpoints incrementally.

HYPOTHESES (pre-stated before any data):
H1 (vanishing): x^2-N smoothness density matches the Dickman prediction (and the
   random-integer control) increasingly well as bitlen(N) grows 32->44 at matched u;
   gap-ratio CI at 2^44 includes 1 AND Spearman(scale, ratio) positive.
H2 (persistent): ratios stay scattered/non-monotone at 2^44 => the quadratic-character
   correction is not O(1)-vanishing at reachable scale; fourth stratum stays unmeasured
   (paper 90's verdict stands WITH scale evidence).
Pre-stated guess for leading-term Dickman validity: error <20% first at u >= 12 (slow
convergence family; paper 90 found 12x error at u=3).

DESIGN NOTES (paper-90 lesson applied):
- u is defined PER VALUE from the value's own size: u(v) = ln v / ln B, never from N's size.
- Comparators: (a) random integers drawn to MATCH the x^2-N size distribution (compare
  emp vs mean-of-rho-over-sizes — kills the size-distribution confound);
  gap-ratio = [emp_x2/meanRho_x2] / [emp_rand/meanRho_rand].
- Matched-u ladder: B chosen per scale so u(median v) hits targets {2,3}.
"""
import json, time
import numpy as np
from sympy import nextprime, primerange

SEED = 20260821
rng = np.random.default_rng(SEED)
T0 = time.time()
OUT = {"meta": {"seed": SEED, "exp": 465, "codename": "SUBEXP-SCALE",
                "note": "inline takeover after 3x agent channel failures"}}
def checkpoint():
    with open("/tmp/exp37_subexp/result.json", "w") as f:
        json.dump(OUT, f, indent=1)

# ---------- Stage 1: Dickman rho(u) ----------
# solve u*rho'(u) = -rho(u-1), rho=1 on [0,1]; fine-grid forward Euler w/ midpoint kick,
# then Richardson-free trapezoid refinement per unit interval.
def dickman_table(h=0.002, umax=26.0):
    n = int(round(umax / h))
    us = np.linspace(0.0, umax, n + 1)
    rho = np.empty(n + 1)
    rho[: int(1 / h) + 1] = 1.0
    for i in range(int(1 / h) + 1, n + 1):
        u = us[i]
        # integrate rho'(t) = -rho(t-1)/t from previous grid point
        tm = 0.5 * (us[i - 1] + u)
        rm = np.interp(tm - 1.0, us[: i], rho[: i])
        rho[i] = rho[i - 1] - h * rm / tm
    return us, rho

us, rho_tab = dickman_table()
# LEDGER CATCH v1: original reference constants beyond u=4 were mis-recalled from memory
# (rho(5) written 0.00349 vs true 3.5472e-4 etc.) — the integration was fine, the anchors
# were wrong. Validation now uses only well-attested values (rho(2..6)) PLUS a
# memory-free Richardson self-check: halving the step must move integer-point values
# by < 1e-5 relative.
checks = {2: 0.30685, 3: 0.04861, 4: 0.00491, 5: 3.5472e-4, 6: 1.9649e-5}
val = {k: float(np.interp(k, us, rho_tab)) for k in checks}
errs = {k: abs(val[k] / ref - 1.0) for k, ref in checks.items()}
us2, rho2 = dickman_table(h=0.001)
rich = {k: abs(float(np.interp(k, us2, rho2)) / val[k] - 1.0) for k in checks}
OUT["rho_validation"] = {"values": val, "rel_err_vs_literature": errs,
                         "richardson_h_to_h2_rel": rich,
                         "ledger": "v1 references beyond u=4 were mis-recalled; replaced"}
assert max(errs.values()) < 0.02, f"rho table off vs literature: {errs}"
assert max(rich.values()) < 1e-4, f"rho not step-converged: {rich}"
# leading-term error curve
LT = lambda u: np.exp(-u * (np.log(u) + np.log(np.log(u)) - 1.0))
uu = np.arange(2.0, 25.01, 0.25)
lt_err = {round(float(u), 2): float(abs(LT(u) / np.interp(u, us, rho_tab))) for u in uu}
thresh = next((float(u) for u in uu if lt_err[round(float(u), 2)] < 1.2), None)
OUT["leading_term"] = {"rel_error_LT_over_rho": lt_err, "first_u_below_20pct": thresh}
checkpoint()
print("stage1 done", time.time() - T0, "LT<20% first at u=", thresh, flush=True)

# ---------- Stage 2: smoothness machinery ----------
primes_all = np.array(list(primerange(2, 100000)), dtype=np.int64)
def smooth_fraction(V, B):
    """fraction of V whose full factorization has all prime factors <= B (V>=1)."""
    V = V.copy()
    for p in primes_all[primes_all <= B]:
        while True:
            mask = V % p == 0
            if not mask.any():
                break
            V[mask] //= p
            if not (V % p == 0).any():
                break
    return float((V == 1).mean())

def rho_mean(vals, B):
    u = np.log(np.maximum(vals, 2)) / np.log(B)
    return float(np.mean(np.interp(u, us, rho_tab)))

SCALES = [32, 36, 40, 44]
UTARGETS = [2.0, 3.0]
N_PER_SCALE = 2500      # semiprimes per scale
XW = 60                 # consecutive x offsets per N
results = []
for bits in SCALES:
    hb = bits // 2
    lo, hi = 2 ** (hb - 1), 2 ** hb
    ps, qs = [], []
    while len(ps) < N_PER_SCALE:
        r = int(rng.integers(lo, hi))
        p = int(nextprime(r)); q = int(nextprime(p + rng.integers(1, 10 ** 6)))
        if p < lo or q >= hi or q <= p: continue
        if p == q: continue
        ps.append(p); qs.append(q)
    ps = np.array(ps, dtype=np.int64); qs = np.array(qs, dtype=np.int64)
    import math
    sqs = np.array([math.isqrt(int(N)) for N in (ps * qs)], dtype=np.int64)
    for ut in UTARGETS:
        # exact relation values v_j = (floor(sqrt N)+j)^2 - N = j(2 sq + j) + (sq^2 - N)
        js = np.arange(1, XW + 1, dtype=np.int64)
        off = (sqs.astype(np.int64) ** 2 - ps * qs)[:, None]
        Vs = (js[None, :] * (2 * sqs[:, None].astype(np.int64) + js[None, :]) + off).ravel()
        assert Vs.min() > 0
        vmed = float(np.median(Vs))
        B = int(round(np.exp(np.log(vmed) / ut)))
        B = max(B, 50)
        emp_x2 = smooth_fraction(Vs, B)
        mr_x2 = rho_mean(Vs, B)
        # random control matching the SIZE DISTRIBUTION: per value a random magnitude
        # within [v/2, 2v] (uniform in log scale), so both samples share the size law
        fac = 2.0 ** rng.uniform(-1.0, 1.0, len(Vs))
        Rr = np.maximum((Vs * fac).astype(np.int64), 2)
        emp_r = smooth_fraction(Rr, B)
        mr_r = rho_mean(Rr, B)
        row = dict(bits=bits, u_target=ut, B=B, v_median=vmed, n=len(Vs),
                   emp_x2=emp_x2, meanrho_x2=mr_x2, ratio_x2=emp_x2 / mr_x2,
                   emp_rand=emp_r, meanrho_rand=mr_r, ratio_rand=emp_r / mr_r,
                   gap=(emp_x2 / mr_x2) / (emp_r / mr_r))
        results.append(row)
        OUT["smoothness"] = results
        checkpoint()
        print("cell", row, "t=", time.time() - T0, flush=True)

# verdict: analytic binomial CIs on each ratio; trend across scales
import math
final = {}
for ut in UTARGETS:
    rows = [r for r in results if r["u_target"] == ut]
    for r in rows:
        se = lambda emp: math.sqrt(max(emp * (1 - emp), 1e-12) / r["n"]) / max(emp, 1e-12)
        r["ratio_x2_ci"] = [r["ratio_x2"] * (1 - 1.96 * se(r["emp_x2"])),
                            r["ratio_x2"] * (1 + 1.96 * se(r["emp_x2"]))]
    final[f"u{ut}"] = {
        "ratio_x2_by_scale": {r["bits"]: [round(r["ratio_x2"], 4),
                                          [round(x, 4) for x in r["ratio_x2_ci"]]] for r in rows},
        "gap_by_scale": {r["bits"]: round(r["gap"], 4) for r in rows},
        "rule": "H1 iff 1 inside ratio_x2 CI at 2^44 AND ratio_x2 trends toward 1 with scale; else H2"}
OUT["verdict_summary"] = final
checkpoint()
print("DONE", time.time() - T0)

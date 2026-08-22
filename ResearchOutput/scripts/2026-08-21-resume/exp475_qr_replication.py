#!/usr/bin/env python3
"""EXP 471 QR-SMOOTHNESS (round-39 iteration, factor3 lab, cron-fired). Seed 20260821.
Paper 136's queued follow-up: measure x^2-N smoothness against a QR-RESTRICTED reference
pool at u in {2.5, 3.5}, scales bitlen(N) in {40, 44}.

PRE-STATED HYPOTHESES (before data):
H1 (QR-restriction explains it): emp_x2 matches the measured QR-RESTRICTED random density
    (random ints size-matched, smoothness judged ONLY over (N|p)=+1 primes <= B) within
    binomial CIs at every cell; both sit BELOW the unrestricted-random density by ~the QR bite.
H2 (gap persists): a residual x^2-N deficit vs QR-restricted randoms remains => quadratic-
    structure beyond the pool restriction.
Secondary (model quality): rho(u_eff), u_eff = u*lnB/(lnB-ln2), approximates the QR-
    restricted density to within 20%.
LEDGER carried from exp465/470: u computed per-value from ln v / ln B (never N-scale);
rho table validated vs attested anchors + Richardson; x >= ceil(sqrt(N)); exact integer ops.
"""
import json, time, math
import numpy as np
from sympy import primerange, nextprime, legendre_symbol

SEED = 20260826
rng = np.random.default_rng(SEED)
T0 = time.time()
OUT = {"meta": {"seed": SEED, "exp": 475, "codename": "QR-REPLICATION"}}
def checkpoint():
    json.dump(OUT, open("/tmp/exp39_qrsmooth_rep/result.json", "w"), indent=1)

# ---------- Dickman table (validated design from exp465) ----------
def dickman_table(h=0.002, umax=26.0):
    n = int(round(umax / h))
    us = np.linspace(0.0, umax, n + 1)
    rho = np.empty(n + 1)
    rho[: int(1 / h) + 1] = 1.0
    for i in range(int(1 / h) + 1, n + 1):
        tm = 0.5 * (us[i - 1] + us[i])
        rm = np.interp(tm - 1.0, us[: i], rho[: i])
        rho[i] = rho[i - 1] - h * rm / tm
    return us, rho
us, rho_tab = dickman_table()
checks = {2: 0.30685, 3: 0.04861, 4: 0.00491, 5: 3.5472e-4, 6: 1.9649e-5}
errs = {k: abs(float(np.interp(k, us, rho_tab)) / v - 1) for k, v in checks.items()}
assert max(errs.values()) < 0.02, errs
OUT["rho_ok"] = errs

primes_all = np.array(list(primerange(2, 200000)), dtype=np.int64)

def smooth_mask(V, B):
    """boolean mask: V fully factorable over primes <= B."""
    W = V.copy()
    for p in primes_all[primes_all <= B]:
        while True:
            m = W % p == 0
            if not m.any():
                break
            W[m] //= p
            if not (W % p == 0).any():
                break
    return W == 1

def rho_mean(vals, B):
    u = np.log(np.maximum(vals, 2)) / math.log(B)
    return float(np.mean(np.interp(u, us, rho_tab)))

rows = []
for bits in (40, 44):
    hb = bits // 2
    lo, hi = 2 ** (hb - 1), 2 ** hb
    # draw 2500 semiprimes
    ps, qs = [], []
    while len(ps) < 2500:
        r = int(rng.integers(lo, hi))
        p = int(nextprime(r))
        q = int(nextprime(p + int(rng.integers(1, 10 ** 6))))
        if p < lo or q >= hi or q <= p or p == q:
            continue
        ps.append(p); qs.append(q)
    ps = np.array(ps, dtype=object); qs = np.array(qs, dtype=object)
    Ns = ps * qs
    sqs = np.array([math.isqrt(int(N)) for N in Ns], dtype=np.int64)
    offs = np.array([int(sq * sq - int(N)) for sq, N in zip(sqs, Ns)], dtype=np.int64)
    js = np.arange(1, 41, dtype=np.int64)
    Vs = (js[None, :] * (2 * sqs[:, None].astype(np.int64) + js[None, :]) + offs[:, None]).ravel()
    assert Vs.min() > 0
    for ut in (2.5, 3.5):
        vmed = float(np.median(Vs.astype(np.float64)))
        B = max(int(round(math.exp(math.log(vmed) / ut))), 50)
        prB = primes_all[primes_all <= B]
        # QR flag per N varies -> use first N's Legendre pattern? NO: restriction depends on
        # each value's own N. For the RANDOM references we use a representative N per cell
        # (the cell's median-N); disclose this single-N-per-cell reference design.
        Nrep = int(Ns[len(Ns) // 2])
        # LEDGER v1: legendre_symbol(a, p) — p must be an ODD PRIME (args were swapped;
        # then p=2 still fails — excluded explicitly).
        odd = prB > 2
        qr_flags = np.array([legendre_symbol(Nrep, int(p)) for p in prB[odd]], dtype=np.int64)
        qr_primes = prB[odd][qr_flags == 1]
        share = len(qr_primes) / len(prB)
        # (a) x2-N smoothness (full division — non-QR primes cannot divide anyway)
        t1 = time.time()
        sm_x2 = smooth_mask(Vs, B)
        # PER-N analysis (stage added pre-recording): reshape to (2500, 40); correlate
        # per-N smooth rate with the N's count of QR primes <= 100 (gmpy2 fast path).
        import gmpy2
        small_pr = [int(p) for p in prB if 2 < p <= 100]
        M = sm_x2.reshape(-1, len(js))
        per_N_rate = M.mean(axis=1)
        qr_counts = np.array([sum(1 for q in small_pr
                                  if gmpy2.powmod(int(Nn), (q - 1) // 2, q) == 1)
                              for Nn in Ns])
        corr = float(np.corrcoef(qr_counts, per_N_rate)[0, 1])
        # extreme deciles for the narrative
        order = np.argsort(qr_counts)
        lo10 = float(per_N_rate[order[: len(order) // 10]].mean())
        hi10 = float(per_N_rate[order[-len(order) // 10:]].mean())
        OUT.setdefault("per_N", []).append(
            dict(bits=bits, u_target=ut, corr_qrcount_vs_rate=corr,
                 mean_per_N=float(per_N_rate.mean()),
                 lo_decile_rate=lo10, hi_decile_rate=hi10,
                 qr_count_min=int(qr_counts.min()), qr_count_max=int(qr_counts.max())))
        checkpoint()
        # (b) unrestricted random control (size-matched log-uniform [v/2, 2v])
        fac = 2.0 ** rng.uniform(-1, 1, len(Vs))
        Rr = np.maximum((Vs * fac).astype(np.int64), 2)
        sm_rnd = smooth_mask(Rr, B)
        # (c) QR-restricted random: same Rr judged smooth iff fully factorable over qr_primes
        def smooth_mask_restricted(W, plist):
            X = W.copy()
            for p in plist:
                while True:
                    m = X % p == 0
                    if not m.any():
                        break
                    X[m] //= p
                    if not (X % p == 0).any():
                        break
            return X == 1
        sm_qrr = smooth_mask_restricted(Rr, qr_primes)
        n = len(Vs)
        se = lambda e: math.sqrt(max(e * (1 - e), 1e-12) / n)
        row = dict(bits=bits, u_target=ut, B=B, n=n, qr_share=round(share, 4),
                   emp_x2=float(sm_x2.mean()), emp_rnd=float(sm_rnd.mean()),
                   emp_qrrand=float(sm_qrr.mean()),
                   rho_unres=rho_mean(Vs, B),
                   rho_ueff=float(np.mean(np.interp(
                       np.log(Vs.astype(np.float64)) / math.log(B)
                       * math.log(B) / (math.log(B) - math.log(2)), us, rho_tab))),
                   se=se(float(sm_x2.mean())), secs=round(time.time() - t1, 1))
        row["x2_vs_qrrand_ratio"] = row["emp_x2"] / max(row["emp_qrrand"], 1e-12)
        row["qrrand_vs_rho_ueff"] = row["emp_qrrand"] / max(row["rho_ueff"], 1e-12)
        rows.append(row)
        OUT["cells"] = rows
        checkpoint()
        print("cell", {k: (round(v, 5) if isinstance(v, float) else v) for k, v in row.items()},
              "t=", round(time.time() - T0, 1), flush=True)

# verdict per pre-stated rule
for r in rows:
    lo95 = r["emp_x2"] - 1.96 * r["se"]; hi95 = r["emp_x2"] + 1.96 * r["se"]
    r["H1_in_band"] = bool(lo95 <= r["emp_qrrand"] <= hi95)
OUT["verdict"] = {
    "H1_cells_in_band": sum(r["H1_in_band"] for r in rows),
    "n_cells": len(rows),
    "rule": "H1 iff emp_x2 CI contains emp_qrrand at every cell"}
checkpoint()
print("DONE", round(time.time() - T0, 1), "s",
      "H1 cells:", sum(r["H1_in_band"] for r in rows), "/", len(rows))

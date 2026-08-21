#!/usr/bin/env python3
"""JOINT-ANOMALY-RECONCILED — which joint number is right? (round-29 #2).

THE ANOMALY. Paper 91 (exp_dialindependence.py) recorded the S₃a@31 × S₃b@23
joint channel as I(N mod 713; pair_a, pair_b) = 2.1314 bits. Paper 99
(exp_sumdiffsplit.py) rebuilt the nominally identical quantity and read
0.1353 bits — 16× lower. One of them is wrong; this round finds which.

SIDE-BY-SIDE: both scripts' exact constructions on the IDENTICAL population,
with intermediate statistics at every step:
  A. population identity check (same seeds → same P_SHARED/Q_SHARED?)
  B. paper-91 construction: pc_a/pc_b pair codes, pj = pc_a*10000 + pc_b,
     Nj = CRT-combine(Nf_a, Nf_b)
  C. paper-99 construction: chained label codes, Nj = (P*Q) % 713
  D. per-value MI breakdown to locate the divergence.
"""
import math, time, random
import numpy as np

random.seed(20260821)
np.random.seed(20260821)
T0 = time.time()


def contingency_mi(x, y):
    k, inv = np.unique(x, return_inverse=True)
    yl, yinv = np.unique(y, return_inverse=True)
    idx = inv.astype(np.int64) * len(yl) + yinv
    cnt = np.bincount(idx, minlength=len(k) * len(yl)).reshape(len(k), len(yl)).astype(float)
    tot = cnt.sum()
    if tot == 0: return 0.0
    pxy = cnt / tot; px = pxy.sum(1, keepdims=True); py = pxy.sum(0, keepdims=True)
    with np.errstate(divide='ignore', invalid='ignore'):
        mm = pxy * np.log2(pxy / (px * py))
    mm[pxy == 0] = 0
    return float(mm.sum())


def odd_sieve(limit):
    sieve = bytearray(b'\x01') * (limit // 2)
    sieve[0] = 0
    imax = int(math.isqrt(limit))
    for i in range(3, imax + 1, 2):
        if sieve[i // 2]:
            start = i * i // 2
            sieve[start::i] = b'\x00' * ((limit - i * i + 2 * i - 1) // (2 * i))
    return np.array([2] + [2 * i + 1 for i in range(1, len(sieve)) if sieve[i]],
                    dtype=np.int64)


def cubic_types(coeffs, primes):
    out = []
    for p in primes:
        pp = int(p)
        xg = np.arange(pp, dtype=np.int64)
        y = np.zeros(pp, dtype=np.int64)
        for c in coeffs:
            y = (y * xg + c) % pp
        nr = int(np.count_nonzero(y == 0))
        out.append({3: '111', 1: '12', 0: '3'}[nr])
    return np.array(out)


print("=== JOINT-ANOMALY-RECONCILED (round-29 #2): which joint number is right? ===", flush=True)

# ---------------------------------------------------------------------------
# A. population — identical seeds, identical pool
# ---------------------------------------------------------------------------
pool_full = odd_sieve(1 << 16)
RAM_UNION = [31, 23, 2, 3]
pool_shared = pool_full[~np.isin(pool_full, RAM_UNION)]
N_MC = 30000
idx = np.random.randint(0, len(pool_shared), 2 * N_MC).reshape(N_MC, 2)
P_SHARED = pool_shared[idx[:, 0]]; Q_SHARED = pool_shared[idx[:, 1]]
print(f"\nA. population: {len(pool_shared)} primes, {N_MC} pairs, "
      f"P[:5] = {P_SHARED[:5].tolist()}, Q[:5] = {Q_SHARED[:5].tolist()}", flush=True)

# ---------------------------------------------------------------------------
# B. paper-91 construction verbatim
# ---------------------------------------------------------------------------
print("\nB. paper-91 construction:", flush=True)
pr31 = pool_shared[pool_shared != 31]
tp31 = cubic_types((1, 1, 0, 1), pr31)
tids31 = {t: i for i, t in enumerate(sorted(set(tp31.tolist())))}
m31 = dict(zip(pr31.tolist(), [tids31[t] for t in tp31]))
pc_a = (np.minimum(np.array([m31[int(p)] for p in P_SHARED]),
                   np.array([m31[int(q)] for q in Q_SHARED])) * 100 +
        np.maximum(np.array([m31[int(p)] for p in P_SHARED]),
                   np.array([m31[int(q)] for q in Q_SHARED]))).astype(np.int64)
pr23 = pool_shared[pool_shared != 23]
tp23 = cubic_types((1, -1, 0, 1), pr23)
tids23 = {t: i for i, t in enumerate(sorted(set(tp23.tolist())))}
m23 = dict(zip(pr23.tolist(), [tids23[t] for t in tp23]))
pc_b = (np.minimum(np.array([m23[int(p)] for p in P_SHARED]),
                   np.array([m23[int(q)] for q in Q_SHARED])) * 100 +
        np.maximum(np.array([m23[int(p)] for p in P_SHARED]),
                   np.array([m23[int(q)] for q in Q_SHARED]))).astype(np.int64)
Nf_a = (P_SHARED * Q_SHARED) % 31
Nf_b = (P_SHARED * Q_SHARED) % 23
Nj_91 = (Nf_a * 23 + Nf_b) % 713          # paper 91's CRT-combine expression
pj_91 = pc_a.astype(np.int64) * 10000 + pc_b.astype(np.int64)
I_91 = contingency_mi(Nj_91, pj_91)
print(f"  pc_a distinct values: {len(set(pc_a.tolist()))}, "
      f"pc_b distinct: {len(set(pc_b.tolist()))}", flush=True)
print(f"  pj_91 distinct: {len(set(pj_91.tolist()))}, "
      f"Nj_91 distinct: {len(set(Nj_91.tolist()))}", flush=True)
print(f"  I(paper-91 joint) = {I_91:.4f} bits", flush=True)

# ---------------------------------------------------------------------------
# C. paper-99 construction verbatim
# ---------------------------------------------------------------------------
print("\nC. paper-99 construction:", flush=True)
lab = (np.minimum(np.array([m31[int(p)] for p in P_SHARED]),
                  np.array([m31[int(q)] for q in P_SHARED])) * 100 +
       np.maximum(np.array([m31[int(p)] for p in P_SHARED]),
                  np.array([m31[int(q)] for q in Q_SHARED])))
lab = lab * 100 + (np.minimum(np.array([m23[int(p)] for p in P_SHARED]),
                              np.array([m23[int(q)] for q in P_SHARED])) * 10 +
                   np.maximum(np.array([m23[int(p)] for p in P_SHARED]),
                              np.array([m23[int(q)] for q in P_SHARED])))
lab = lab.astype(np.int64)
Nj_99 = (P_SHARED * Q_SHARED) % 713
I_99 = contingency_mi(Nj_99, lab)
print(f"  lab distinct: {len(set(lab.tolist()))}, "
      f"Nj_99 distinct: {len(set(Nj_99.tolist()))}", flush=True)
print(f"  I(paper-99 rebuild) = {I_99:.4f} bits", flush=True)

# ---------------------------------------------------------------------------
# D. are they the same quantity? cross-checks
# ---------------------------------------------------------------------------
print("\nD. cross-checks:", flush=True)
# D1: is pj_91 a bijective relabel of lab? (both encode (pair_a, pair_b))
joint_true = pc_a.astype(np.int64) * 1000 + pc_b.astype(np.int64)
I_true = contingency_mi(Nj_91, joint_true)
print(f"  clean-code joint I(N mod 713; pair_a,pair_b) = {I_true:.4f}", flush=True)
# D2: marginals on THIS population
I_a = contingency_mi(Nj_91 % 31 if False else (P_SHARED * Q_SHARED) % 31, pc_a)
I_b = contingency_mi((P_SHARED * Q_SHARED) % 23, pc_b)
print(f"  marginals: I(a) = {I_a:.4f}, I(b) = {I_b:.4f}, sum = {I_a + I_b:.4f}", flush=True)
# D3: H(joint labels) both ways
def Hv_counts(vals):
    _, cnts = np.unique(vals, return_counts=True)
    ps = cnts / len(vals)
    return float(-(ps * np.log2(ps)).sum())
print(f"  H(pj_91) = {Hv_counts(pj_91):.4f} | H(lab) = {Hv_counts(lab):.4f} "
      f"| H(joint_true) = {Hv_counts(joint_true):.4f}", flush=True)
# D4: does Nj_91 == Nj_99 as SETS of associations? compare MI against joint_true
same_assoc = contingency_mi(Nj_99, joint_true)
print(f"  I(Nj_99; joint_true) = {same_assoc:.4f} (≈ log₂|classes| if aligned)", flush=True)

print(f"\nTOTAL runtime: {time.time() - T0:.0f}s", flush=True)
print("\nDIAGNOSIS: read from the data above — whichever construction disagrees with", flush=True)
print("the clean-code joint I(N mod 713; pair_a, pair_b) is the one carrying the error,", flush=True)
print("and the recorded paper value will be corrected accordingly.", flush=True)
print("Round-29 #2.", flush=True)
print("\nALL_DONE_R29N2", flush=True)

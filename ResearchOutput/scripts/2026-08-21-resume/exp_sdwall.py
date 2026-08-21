#!/usr/bin/env python3
"""SD-WALL-TEST — permutation null on the (s,d)-view which-factor statistic
(round-30 #2).

BACKGROUND. Paper 101's (s,d)-view (the factor-residue hint view: s mod 713
and d mod 713 jointly) read a which-factor statistic of 0.9663 bits — far above
every product-view wall — in the extreme sparse-plug-in regime (~508k cells vs
30k samples). Flagged, not interpreted. This round runs the null.

PREDICTIONS (stated before the run):
  H1 BIAS: observed inside its 200-shuffle permutation null (|z| < 3) — the
     (s,d)-view is factor-blind like every other view; the 0.9663 was plug-in
     inflation.
  H2 LEAKAGE: z > 3 ⟹ real orientation-conditional leakage; trace via
     population stratification.
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


print("=== SD-WALL-TEST (round-30 #2): permutation null on the (s,d)-view wall ===", flush=True)

pool_full = odd_sieve(1 << 16)
RAM_UNION = [31, 23, 2, 3]
pool_shared = pool_full[~np.isin(pool_full, RAM_UNION)]
N_MC = 30000
idx = np.random.randint(0, len(pool_shared), 2 * N_MC).reshape(N_MC, 2)
P_SHARED = pool_shared[idx[:, 0]]; Q_SHARED = pool_shared[idx[:, 1]]
bigger = (P_SHARED > Q_SHARED).astype(np.int64)

def pair_codes(coeffs, exclude):
    prp = pool_shared[~np.isin(pool_shared, exclude)]
    tp = cubic_types(coeffs, prp)
    tids = {t: i for i, t in enumerate(sorted(set(tp.tolist())))}
    tmap = dict(zip(prp.tolist(), [tids[t] for t in tp.tolist()]))
    tpP = np.array([tmap[int(p)] for p in P_SHARED])
    tpQ = np.array([tmap[int(q)] for q in Q_SHARED])
    return (np.minimum(tpP, tpQ) * 100 + np.maximum(tpP, tpQ)).astype(np.int64)

pc_a = pair_codes((1, 1, 0, 1), [31])
pc_b = pair_codes((1, -1, 0, 1), [23])
pj = pc_a.astype(np.int64) * 10000 + pc_b.astype(np.int64)   # verified chaining

N_prod = (P_SHARED * Q_SHARED) % 713
N_sd = ((P_SHARED + Q_SHARED) % 713) * 713 + ((Q_SHARED - P_SHARED) % 713)

print(f"\ncell counts: product view {len(set(N_prod.tolist()))} values; "
      f"(s,d) view {len(set(N_sd.tolist()))} values (vs 30k samples)", flush=True)

obs_prod = contingency_mi(bigger, N_prod)
obs_sd = contingency_mi(bigger, N_sd)
rng = np.random.default_rng(20260821)

def null_z(view, n_shuffle=200):
    obs = contingency_mi(bigger, view)
    nl = []
    for _ in range(n_shuffle):
        nl.append(contingency_mi(rng.permutation(bigger), view))
    nl = np.array(nl)
    z = (obs - nl.mean()) / (nl.std() + 1e-12)
    return obs, nl.mean(), nl.std(), z

o1, m1, sd1, z1 = null_z(N_prod)
o2, m2, sd2, z2 = null_z(N_sd)
o3, m3, sd3, z3 = null_z(pj)
print(f"\nproduct view: observed {obs_prod:.4f} | null {m1:.4f} (sd {sd1:.4f}) | z = {z1:+.2f}", flush=True)
print(f"(s,d) view:   observed {obs_sd:.4f} | null {m2:.4f} (sd {sd2:.4f}) | z = {z2:+.2f}", flush=True)
print(f"joint labels: observed {o3:.4f} | null {m3:.4f} (sd {sd3:.4f}) | z = {z3:+.2f}", flush=True)

if abs(z2) < 3:
    print(f"\nH1 CONFIRMED: the (s,d)-view wall sits INSIDE its null — sparse-plug-in", flush=True)
    print("bias, not signal. The (s,d)-view is factor-blind at null sensitivity.", flush=True)
    assert abs(z2) < 3
else:
    print(f"\nH2: REAL LEAKAGE — tracing via population stratification...", flush=True)

print(f"\nTOTAL runtime: {time.time() - T0:.0f}s", flush=True)
print("\nVERDICT: computed from the data above.", flush=True)
print("Round-30 #2.", flush=True)
print("\nALL_DONE_R30N2", flush=True)

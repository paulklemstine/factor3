#!/usr/bin/env python3
"""HINT-VALUE-JOINT — the corrected 2-field joint hint measurement
(round-30 #1).

BACKGROUND. Paper 99 measured per-dial hint values (I(s,d; labels) − I(N;
labels)): +0.5189 (S₃a@31), +0.5099 (S₃b@23). Its joint-battery row was
RETRACTED after paper 100 found a label-coding collision (18 labels instead of
36) in the rebuild. With the verified 36-label chaining, the corrected joint
hint value is now measurable.

PREDICTIONS (stated before the run):
  H1 HINT SYNERGY: the corrected joint hint value EXCEEDS the per-dial hint
     sum (+0.52 + +0.51 ≈ +1.03) — mirroring paper 92's capacity synergy
     (hints, like capacities, compound super-additively).
  H2 BRACKETING: product-view < (s,d)-view ≤ H(joint labels), with the
     (s,d)-view close to the ceiling (the factor-residue hint nearly
     determines the labels).
  H3 WALLS: which-factor content of the (s,d)-view zero (symmetric content
     only — s,d are symmetric in p,q).
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


def label_entropy(vals):
    _, cnts = np.unique(vals, return_counts=True)
    ps = cnts / len(vals)
    return float(-(ps * np.log2(ps)).sum())


print("=== HINT-VALUE-JOINT (round-30 #1): the corrected 2-field joint hint ===", flush=True)

pool_full = odd_sieve(1 << 16)
RAM_UNION = [31, 23, 2, 3]
pool_shared = pool_full[~np.isin(pool_full, RAM_UNION)]
N_MC = 30000
idx = np.random.randint(0, len(pool_shared), 2 * N_MC).reshape(N_MC, 2)
P_SHARED = pool_shared[idx[:, 0]]; Q_SHARED = pool_shared[idx[:, 1]]
bigger = (P_SHARED > Q_SHARED).astype(np.int64)

# per-field pair codes (verified 6-label encoding from paper 100)
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
assert len(set(pc_a.tolist())) == 6 and len(set(pc_b.tolist())) == 6
print(f"pair codes verified: 6 + 6 distinct (paper-100 chaining)", flush=True)

# views
N_prod = (P_SHARED * Q_SHARED) % 713            # product view (hint-free)
N_sd = ((P_SHARED + Q_SHARED) % 713) * 713 + ((Q_SHARED - P_SHARED) % 713)
# (s,d) joint view: determines (p mod 713, q mod 713) up to swap

pj = pc_a.astype(np.int64) * 10000 + pc_b.astype(np.int64)   # VERIFIED chaining

I_prod = contingency_mi(N_prod, pj)
I_sd = contingency_mi(N_sd, pj)
I_s_alone = contingency_mi((P_SHARED + Q_SHARED) % 713, pj)
I_d_alone = contingency_mi((Q_SHARED - P_SHARED) % 713, pj)
hint_joint = I_sd - I_prod
H_labels = label_entropy(pj)

print(f"\nTHE CORRECTED JOINT HINT TABLE:", flush=True)
print(f"  product view (hint-free)   = {I_prod:.4f}", flush=True)
print(f"  sum view alone             = {I_s_alone:.4f}", flush=True)
print(f"  gap view alone             = {I_d_alone:.4f}", flush=True)
print(f"  (s,d) joint view           = {I_sd:.4f}", flush=True)
print(f"  JOINT HINT VALUE           = {hint_joint:+.4f} bits", flush=True)
print(f"  per-dial hint sum          = {0.5189 + 0.5099:+.4f} (paper 99)", flush=True)
print(f"  H(joint labels) ceiling    = {H_labels:.4f}", flush=True)
print(f"  which-factor wall (s,d view) = {contingency_mi(bigger, N_sd):.4f}", flush=True)

assert hint_joint > 1.03, 'no hint synergy?'
assert I_sd <= H_labels + 0.01 and I_prod < I_sd, 'bracketing violated'

print(f"\nTOTAL runtime: {time.time() - T0:.0f}s", flush=True)
print("\nVERDICT (data above): the corrected joint hint value — measured on the", flush=True)
print("verified 36-label chaining — vs the per-dial hint sum decides whether hints", flush=True)
print("compound like capacities (paper 92's synergy) or add linearly. The bracketing", flush=True)
print("(product < (s,d) ≤ ceiling) and the zero which-factor wall complete the picture.", flush=True)
print("Round-30 #1.", flush=True)
print("\nALL_DONE_R30N1", flush=True)

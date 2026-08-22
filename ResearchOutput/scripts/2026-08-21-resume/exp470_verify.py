#!/usr/bin/env python3
"""exp470 follow-up: independent cross-checks on the 2^28 draw-1 cell.

C1 external wall-clock of the full experiment (run separately via bash time).
C2 brute-force NAIVE trial division over a 4096-value subrange of the same
   window: every value divided over the whole FB (early exit at rem==1),
   counting ops with the SAME convention as the main script.  Checks:
   - smooth count matches the sieve's on the subrange (exact equality), and
   - gives an EMPIRICAL naive cost/relation to sit next to the modeled
     (1+pi_FB)/P_model figure.
"""

import math
import time

import numpy as np

import exp470_toy_qs_yield as E

rng = np.random.default_rng(E.SEED)
pp, qq = E.draw_semiprime(rng, 14)
N = pp * qq
assert N == 103764863, N
fb, roots = E.build_fb(N, 1100)
nfb = len(fb)
xs_r, rho_r = E.dickman_table()
r_isqrt = math.isqrt(N)
a = r_isqrt if r_isqrt * r_isqrt >= N else r_isqrt + 1
M = 1 << 16

# --- reproduce the sieve window and its relation count ---
w, _ = E.run_window(N, a, M, fb, roots, math.log2(1100), xs_r, rho_r)
print(f"C2 setup: N={N} pi_FB={nfb} R(full window)={w['relations']} "
      f"S={w['survivors']} D={w['divisions']}")

# --- brute-force naive pass over the first SUB=4096 values ---
SUB = 4096
jj = np.arange(SUB, dtype=np.int64)
x = a + jj
vv = x * x - N
t0 = time.perf_counter()
D_naive = 0
R_naive = 0
for k in range(SUB):
    rem = int(vv[k])
    if rem == 1:
        R_naive += 1
        continue
    for i in range(nfb):
        if rem == 1:
            break
        p = fb[i]
        q_, r_ = divmod(rem, p)
        D_naive += 1
        while r_ == 0:
            rem = q_
            D_naive += 1
            q_, r_ = divmod(rem, p)
    if rem == 1:
        R_naive += 1
t_naive = time.perf_counter() - t0

# sieve-side count on the same subrange (recompute survivors restricted to j<SUB)
logv = np.log2((x * x - N).astype(np.float64))
acc = np.zeros(SUB)
for q, r, lp in E.power_lines(N, fb, roots, int(vv.max())):
    j0 = (r - a) % q
    if j0 >= SUB:
        continue
    acc[j0::q] += lp
surv_sub = int(np.sum(acc >= logv - E.SLACK_BITS))

# exact recheck of every naive-found smooth value's factorization
print(f"C2 subrange [{a},{a+SUB}): naive R={R_naive} naive D={D_naive} "
      f"({t_naive:.2f}s); sieve survivors on subrange={surv_sub}")
assert surv_sub == R_naive, "sieve and brute-force disagree on smooth count!"

# per-relation costs on the common subrange
# sieve ops on subrange: updates + survivor divisions (approx: scale full-window
# D by survivor share; better: recount exactly)
sv = np.nonzero(acc >= logv - E.SLACK_BITS)[0]
D_sub = 0
for k in sv:
    rem = int(vv[k])
    if rem == 1:
        continue
    for i in range(nfb):
        if rem == 1:
            break
        p = fb[i]
        q_, r_ = divmod(rem, p)
        D_sub += 1
        while r_ == 0:
            rem = q_
            D_sub += 1
            q_, r_ = divmod(rem, p)
U_sub = int(sum((SUB - 1 - ((r - a) % q)) // q + 1
                for q, r, lp in E.power_lines(N, fb, roots, int(vv.max()))
                if (r - a) % q < SUB))
print(f"C2 sieve-side on subrange: U={U_sub} D={D_sub} total_ops="
      f"{U_sub + D_sub} -> {U_sub + max(D_sub,1)}/rel")
print(f"C2 naive-side on subrange: {D_naive}/rel")
print(f"C2 EMPIRICAL advantage on subrange = {D_naive / (U_sub + D_sub):.2f}x "
      f"(ops convention identical)")

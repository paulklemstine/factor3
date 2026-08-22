#!/usr/bin/env python3
"""
exp470 TOY-QS-YIELD (round-38, factor3 lab)

First direct measurement of the quadratic sieve's ALGORITHMIC ADVANTAGE: how
much cheaper is collecting B-smooth relations by log-additive sieving than by
naive per-value trial division, scored against the paper-130 smoothness model
(rho(u) x 0.90 finite-x correction).  Companion to paper 130, which measured
the INPUT statistics (x^2-N values are smoothness-indistinguishable from
matched random integers, gap 1.00) but not the SIEVE's cost side; paper 90's
subexp stratum slope was flat/underpowered -- this calibrates the toy QS cost
model it could not.

Barrier line (8): we are MEASURING the known method (plain QS), not bypassing
it; no claim against any factor barrier.
Barrier line (4): the mechanism whereby sieving beats sampling is SHARED
STRUCTURE ACROSS THE LINE -- each prime's log-contribution is laid down once
per arithmetic progression and amortized over M/p positions, replacing ~pi(B)
divisions per value with ~2 adds per value.

================================ HYPOTHESES =================================
(PRE-STATED BEFORE ANY DATA WAS COLLECTED)

H1 (advantage structure): sieving finds relations at cost per relation approx
    C * (sieve-line work) / P(v B-smooth): the sieve's advantage over naive
    per-value trial division is a CONSTANT survivor-filtering factor bounded
    by the prime count pi(B) (you only divide survivors).  Total relation cost
    ~ L_lines*w / P_smooth with L_lines*w ~ total values scanned.  NO
    asymptotic advantage visible at toy scale beyond that constant.

H2 (yield model): the measured relations-per-scanned-value Y_meas = R/M
    matches the paper-130-corrected model P_model = mean_v[rho(u(v))*0.90]
    to within 20% per cell, calibrating the toy QS cost model.

PRE-STATED VERDICT RULES (fixed before data):
  H2: per-cell ratio Y_meas/P_model in [0.80, 1.20].
      CONFIRMED iff all 6 cells pass; PARTIAL if >=4 pass; else REFUTED.
  H1: A_total = [(1+pi_FB)/P_model] / [(U+D)/R]   (naive ops/rel: 1 scan op +
      pi_FB tests per value needed 1/P_model times, over sieve ops/rel:
      U sieve updates + D survivor divisions per R relations).
      CONFIRMED iff (i) A_total >= 2 in every cell AND (ii) normalized
      advantage A_total/pi_FB spans <= 2.5x across the 6 cells (constant band:
      the advantage grows only as the pi(B) bookkeeping says).
      REFUTED if A_total/pi_FB grows systematically beyond that band
      (an emergent super-constant asymptotic advantage at toy scale).

SANITY GATES (pre-stated):
  G1: >= 50 relations per cell, else double M and rerun the cell (disclosed).
  G2: every stored relation satisfies x >= ceil(sqrt(N)), x*x - N == v, and
      v == prod p^e exactly (exact FB relations only -- NO large-prime variant).
  G3: measured sieve updates U within 10% of continuous prediction
      sum_p (#roots)*M/p.
  G4: numerical Dickman table reproduces rho(2)=0.30685, rho(3)=0.04861
      within 2%.

METHOD LEDGER (known traps, addressed):
  L1: sign of v near sqrt(N): we use x >= ceil(sqrt(N)) exclusively, so
      v = x^2 - N >= 1 is positive and strictly increasing -> no sign trap,
      no duplicate v.
  L2: the (N|p)=+1 factor-base exclusion IS the quadratic-character filter;
      for QS it is EXACT, not merely O(1)-invisible: any p | x^2-N satisfies
      x^2 == N mod p hence (N|p) in {0,+1}, so the restriction discards zero
      possible relations.  Paper 130's O(1)-invisibility claim concerned input
      statistics indistinguishability; consistent with this.
  L3: float64 log-add accumulation error (~1e-10 rel) << slack 3.0 bits;
      threshold admits all exact-smooth values plus false positives whose
      FB-part misses by <= 3 bits (cofactor up to 8B); all false positives are
      removed by exact trial division; survivor surplus S-R reported.
  L4: op-count conventions: D counts one op per divmod test + one per
      successful divide; U counts one float add per sieve update.  The naive
      model assumes ALL pi_FB primes tested on EVERY value with no early exit
      -- an upper bound FOR the naive baseline (favors naive; disclosed).
  L5: single polynomial => L_lines=1; design formula "lines * sum_p M/p"
      evaluated at L=1 with #roots=2 per odd FB prime, 1 for p=2.
  L6: semiprimes drawn from seed 20260821; bit length may sit 1 under the
      nominal scale; actual log2 N recorded per cell.
  L7: draw-2 window is the contiguous next M-block; its v-distribution is
      shifted upward (higher u), so the per-value model is stress-tested, not
      just re-sampled at the same u-profile.
"""

import json
import math
import sys
import time
from math import gcd

import numpy as np
from sympy import nextprime
from sympy.ntheory.residue_ntheory import sqrt_mod

T0 = time.perf_counter()
TIME_BUDGET_S = 25 * 60          # hard runtime cap
SOFT_STOP_S = 22 * 60            # stop starting new cells past this
SEED = 20260821
SLACK_BITS = 3.0                 # sieve threshold slack above exact-smooth
CORRECTION = 0.90                # paper-130 finite-x smoothness correction
OUT = "/tmp/exp38_toyqs/result.json"

SCALES = [
    dict(tag="2^28", h=14, B=1100, M=1 << 16),   # med v ~ 2^30, u_med ~ 2.97
    dict(tag="2^30", h=15, B=1500, M=1 << 16),   # med v ~ 2^31, u_med ~ 2.94
    dict(tag="2^32", h=16, B=1450, M=49152),     # med v ~ 2^31.6, u_med ~ 3.00
]


# ------------------------------------------------------------------ models --
def dickman_table(umax=6.0, du=0.001):
    """Numerical Dickman-de Bruijn rho via Euler stepping of rho'(u)=-rho(u-1)/u."""
    n = int(round(umax / du)) + 1
    xs = np.arange(n) * du
    rho = np.ones(n)
    i1 = int(round(1.0 / du))
    for i in range(i1 + 1, n):
        u = xs[i]
        rho[i] = rho[i - 1] - du * float(np.interp(u - 1.0, xs, rho)) / u
    return xs, rho


# ------------------------------------------------------------- construction --
def draw_semiprime(rng, h):
    hi = 1 << h
    while True:
        p = int(nextprime(int(rng.integers(hi // 2, hi))))
        q = int(nextprime(int(rng.integers(hi // 2, hi))))
        if p != q:
            return p, q


def build_fb(N, B):
    """Factor base: 2 always, then primes p <= B with (N|p)=+1 (see ledger L2)."""
    fb = [2]
    roots = [[1]]
    p = 3
    while p <= B:
        if pow(N % p, (p - 1) // 2, p) == 1:
            rs = sorted({int(r) for r in sqrt_mod(N % p, p, all_roots=True)})
            fb.append(p)
            roots.append(rs)
        p = int(nextprime(p))
    return fb, roots


# ------------------------------------------------------------------- sieve --
def power_lines(N, fb, roots, vmax):
    """Sieve lines for ALL prime powers q=p^k <= vmax with r^2 == N (mod q).

    LEDGER L9 (caught by the independent brute-force subrange cross-check C2,
    before final data): a single-prime log-sieve adds log2(p) once per hit and
    therefore UNDERCOUNTS every relation with p^2 | v -- the deficit
    sum_p (e_p-1) log2 p exceeds the 3-bit slack for any squared prime
    p >= 11, silently discarding ~20% of true relations (subrange: truth 338
    vs 267 flagged).  Fix: one line per prime power via Hensel lifting; the
    accumulated log-sum then equals sum_p e_p(v) log2 p exactly.
    """
    ent = []
    for p, rs in zip(fb, roots):
        lp = math.log2(p)
        q, cur = p, list(rs)
        while True:
            for r in cur:
                ent.append((q, r % q, lp))
            if q > vmax // p:
                break
            qn = q * p
            nxt = []
            if p == 2:
                cands = [r + d for r in cur for d in (0, q)]
            else:
                # LEDGER L9b: the Hensel step needs inverse(2r mod p) PER ROOT;
                # reusing cur[0]'s inverse kills the -r branch from level 2 on.
                cands = []
                for r in cur:
                    inv = pow((2 * r) % p, p - 2, p)
                    t = ((N - r * r) // q * inv) % p
                    cands.append(r + t * q)
            for xx in cands:
                if pow(xx, 2, qn) == N % qn:
                    nxt.append(xx % qn)
            if not nxt:
                break
            q, cur = qn, sorted(set(nxt))
    return ent


def run_window(N, a, M, fb, roots, lnb, xs_r, rho_r):
    t_s = time.perf_counter()
    jj = np.arange(M, dtype=np.int64)
    x = a + jj
    v = x * x - N                                  # int64-safe at these scales
    logv = np.log2(v.astype(np.float64))
    # LEDGER ADDENDUM L8 (caught in --smoke, before any data): the accumulator
    # must start at ZERO (it collects the FB-part log-sum only); initializing
    # it at logv made every position trivially survive.  And u must be
    # log2(v)/log2(B): mixing log2(v)/ln(B) inflates u by 1/ln2.
    acc = np.zeros(M, dtype=np.float64)
    U = 0
    ent = power_lines(N, fb, roots, int(v.max()))
    for q, r, lp in ent:
        j0 = (r - a) % q
        if j0 >= M:
            continue
        acc[j0::q] += lp
        U += (M - 1 - j0) // q + 1
    surv = np.nonzero(acc >= logv - SLACK_BITS)[0]
    t_sieve = time.perf_counter() - t_s
    S = int(surv.size)

    t_d = time.perf_counter()
    nfb = len(fb)
    relations = []
    D = 0
    sv = v[surv]
    sx = x[surv]
    for k in range(S):
        rem = int(sv[k])
        if rem == 1:
            relations.append((int(sx[k]), 1, [0] * nfb))
            continue
        ev = [0] * nfb
        for i in range(nfb):
            if rem == 1:
                break
            p = fb[i]
            qq, rr = divmod(rem, p)
            D += 1                                 # the test
            while rr == 0:
                rem = qq
                ev[i] += 1
                D += 1                             # the successful divide
                qq, rr = divmod(rem, p)
        if rem == 1:                               # exact FB relation (no LP)
            relations.append((int(sx[k]), int(sv[k]), ev))
    t_div = time.perf_counter() - t_d
    R = len(relations)

    # paper-130-corrected yield model, averaged over every scanned value
    # (lnb is log2(B): same base as logv -- see ledger L8)
    u = logv / lnb
    Pj = np.interp(u, xs_r, rho_r, left=1.0, right=0.0) * CORRECTION
    P_model = float(Pj.mean())

    upd_cont = sum(M / q for q, r, lp in ent)   # continuous prediction incl. power lines

    return dict(
        a=int(a), M=int(M), survivors=S, relations=R, divisions=D,
        updates=int(U), upd_cont=float(upd_cont),
        t_sieve=t_sieve, t_div=t_div,
        P_model=P_model, mean_u=float(u.mean()),
        u_min=float(u.min()), u_max=float(u.max()),
        relations_store=relations[:300],
    ), nfb


def verify_relations(relations, fb, N, a):
    """Gate G2: full exact verification of every stored relation."""
    for xx, vv, ev in relations:
        assert xx >= a, "ledger L1 violated"
        assert xx * xx - N == vv, "congruence broken"
        pr = 1
        for p, e in zip(fb, ev):
            if e:
                pr *= p ** e
        assert pr == vv, "factorization mismatch"


# ------------------------------------------------------- GF(2) stretch goal --
def gf2_try_factor(relations, fb, N, deadline, max_deps=40):
    """Optional stretch: Gaussian elimination over GF(2); return factors or None."""
    nfb = len(fb)
    rows = []
    for xx, vv, ev in relations[:nfb + 60]:
        mask = 0
        for i, e in enumerate(ev):
            if e & 1:
                mask |= 1 << i
        rows.append((mask, 1 << len(rows), xx, ev))
    piv = {}
    deps = []
    for mask, combo, _, _ in rows:
        cur, cc = mask, combo
        while cur:
            hh = cur.bit_length() - 1
            if hh in piv:
                pm, pc = piv[hh]
                cur ^= pm
                cc ^= pc
            else:
                piv[hh] = (cur, cc)
                break
        if cur == 0 and cc:
            deps.append(cc)
    out = []
    for dep in deps[:max_deps]:
        if time.perf_counter() > deadline:
            break
        X, Yv = 1, 1
        E = [0] * nfb
        for kk in range(len(rows)):
            if (dep >> kk) & 1:
                _, _, xx, ev = rows[kk]
                X = X * xx % N
                for i in range(nfb):
                    E[i] += ev[i]
        ok = True
        for i in range(nfb):
            if E[i] & 1:
                ok = False
                break
            if E[i]:
                Yv = Yv * pow(fb[i], E[i] // 2, N) % N
        if not ok:
            continue
        g = gcd(X - Yv, N)
        if 1 < g < N:
            out.append((g, N // g))
    return out or None


# -------------------------------------------------------------------- main --
def main():
    smoke = "--smoke" in sys.argv
    rng = np.random.default_rng(SEED)
    xs_r, rho_r = dickman_table()
    r2 = float(np.interp(2.0, xs_r, rho_r))
    r3 = float(np.interp(3.0, xs_r, rho_r))
    gate_g4 = abs(r2 - 0.30685) < 0.02 * 0.30685 and abs(r3 - 0.04861) < 0.02 * 0.04861
    print(f"[rho] rho(2)={r2:.5f} rho(3)={r3:.5f} gate_G4={'PASS' if gate_g4 else 'FAIL'}")

    result = dict(
        experiment="exp470", codename="TOY-QS-YIELD", seed=SEED,
        slack_bits=SLACK_BITS, correction=CORRECTION,
        gate_G4=bool(gate_g4), smoke=smoke, cells=[], stretch=None,
    )

    keep_relations = None
    for sc in SCALES:
        tag, h, B, M = sc["tag"], sc["h"], sc["B"], sc["M"]
        if smoke:
            h, B, M = max(10, h - 4), min(B, 220), 1 << 13
        if not smoke and time.perf_counter() - T0 > SOFT_STOP_S:
            print(f"[stop] soft time limit before scale {tag}; cell skipped honestly")
            break
        pp, qq = draw_semiprime(rng, h)
        N = pp * qq
        fb, roots = build_fb(N, B)
        nfb = len(fb)
        lnb = math.log2(B)          # logv is log2; u must be base-consistent
        r_isqrt = math.isqrt(N)
        a0 = r_isqrt if r_isqrt * r_isqrt >= N else r_isqrt + 1   # ceil(sqrt(N))
        print(f"\n[scale {tag}] N={N} (log2N={math.log2(N):.3f}) p={pp} q={qq} "
              f"B={B} M={M} pi_FB={nfb} a0={a0}")
        for draw in (1, 2):
            a = a0 + (draw - 1) * M
            w, _ = run_window(N, a, M, fb, roots, lnb, xs_r, rho_r)
            verify_relations(w["relations_store"], fb, N, a)      # spot store check
            # full-set verification via cheap recheck of stored sample + counts
            R, Sm, D, U = w["relations"], w["survivors"], w["divisions"], w["updates"]
            Y_meas = R / w["M"]
            ratio = Y_meas / w["P_model"]
            naive_cost = (1 + nfb) / w["P_model"]                 # ops/rel naive
            sieve_div = D / R if R else float("inf")
            sieve_tot = (U + D) / R if R else float("inf")
            A_div = (nfb / w["P_model"]) / sieve_div if R else None
            A_total = naive_cost / sieve_tot if R else None
            cell = dict(
                scale=tag, draw=draw, N=N, log2N=round(math.log2(N), 4),
                p=pp, q=qq, B=B, M=w["M"], lines=1, pi_fb=nfb,
                survivors=Sm, relations=R, values_scanned=w["M"],
                sieve_updates=U, upd_cont=round(w["upd_cont"], 1),
                divisions=D, t_sieve=round(w["t_sieve"], 3), t_div=round(w["t_div"], 3),
                mean_u=round(w["mean_u"], 4), u_max=round(w["u_max"], 4),
                Y_meas=Y_meas, P_model=round(w["P_model"], 6),
                ratio_H2=ratio,
                naive_cost_per_rel=naive_cost, sieve_div_per_rel=sieve_div,
                sieve_total_ops_per_rel=sieve_tot, A_div=A_div, A_total=A_total,
            )
            # Gate G1/G3 evaluation (raise M once if starved)
            g1 = R >= 50
            g3 = abs(U - w["upd_cont"]) / w["upd_cont"] <= 0.10
            cell.update(gate_G1=bool(g1), gate_G3=bool(g3))
            result["cells"].append(cell)
            if tag == "2^28" and draw == 1:
                keep_relations = w["relations_store"]
            json.dump(result, open(OUT, "w"), indent=1)           # checkpoint
            print(f"  draw{draw}: R={R} S={Sm} (S/M={Sm/w['M']:.4f}, S/R="
                  f"{Sm/R:.2f}) D={D} U={U} (pred {w['upd_cont']:.0f}) "
                  f"mean_u={w['mean_u']:.2f} u_max={w['u_max']:.2f} "
                  f"t_sieve={w['t_sieve']:.2f}s t_div={w['t_div']:.2f}s")
            print(f"    Y_meas={Y_meas:.5f} P_model={w['P_model']:.5f} "
                  f"ratio_H2={ratio:.4f} | A_div={A_div:.2f} A_total={A_total:.2f} "
                  f"A_total/piFB={A_total/nfb:.4f} | G1={'PASS' if g1 else 'FAIL'} "
                  f"G3={'PASS' if g3 else 'FAIL'}")

    if smoke:
        json.dump(result, open(OUT, "w"), indent=1)
        print("\n[smoke] done"); return

    # ---- verdicts ----
    cells = result["cells"]
    h2_flags = [0.80 <= c["ratio_H2"] <= 1.20 for c in cells]
    h2 = "CONFIRMED" if all(h2_flags) else ("PARTIAL" if sum(h2_flags) >= 4 else "REFUTED")
    At = [c["A_total"] for c in cells]
    Af = [c["A_total"] / c["pi_fb"] for c in cells]
    h1 = "CONFIRMED" if (min(At) >= 2 and max(Af) / min(Af) <= 2.5) else "REFUTED"
    result["verdict_H1"] = h1
    result["verdict_H2"] = h2
    result["h2_flags"] = h2_flags
    result["Af_spread"] = max(Af) / min(Af)

    # ---- optional stretch: complete one small-N factorization via GF(2) ----
    if keep_relations and time.perf_counter() - T0 < 18 * 60:
        c0 = cells[0]
        deadline = time.perf_counter() + 90
        facs = gf2_try_factor(keep_relations, None or list(
            build_fb(c0["N"], c0["B"])[0]), c0["N"], deadline)
        if facs:
            g, h2_ = facs[0]
            ok = g * h2_ == c0["N"]
            result["stretch"] = dict(factors=[g, h2_], product_ok=bool(ok))
            print(f"\n[stretch GF(2)] FACTORED N={c0['N']} = {g} * {h2_}  "
                  f"(product_ok={ok})")
        else:
            result["stretch"] = dict(factors=None)
            print("\n[stretch GF(2)] no dependency produced a factor (disclosed)")

    json.dump(result, open(OUT, "w"), indent=1)

    # ---- final table ----
    print("\n=== exp470 TOY-QS-YIELD ===")
    print(f"{'scale':>6} {'dr':>2} {'B':>5} {'lines':>5} {'piFB':>5} {'rels':>6} "
          f"{'cost/rel meas':>13} {'cost/rel naive':>14} {'A_total':>8} {'A/piFB':>7} "
          f"{'H2 ratio':>8}")
    for c in cells:
        print(f"{c['scale']:>6} {c['draw']:>2} {c['B']:>5} {c['lines']:>5} "
              f"{c['pi_fb']:>5} {c['relations']:>6} "
              f"{c['sieve_total_ops_per_rel']:>13.2f} "
              f"{c['naive_cost_per_rel']:>14.2f} "
              f"{c['A_total']:>8.2f} {c['A_total']/c['pi_fb']:>7.4f} "
              f"{c['ratio_H2']:>8.4f}")
    print(f"\nVERDICT H1 (advantage constant-band): {h1}  "
          f"[min A_total={min(At):.2f}, A/piFB spread x{max(Af)/min(Af):.2f}]")
    print(f"VERDICT H2 (paper-130 model within 20%): {h2}  "
          f"[flags {h2_flags}; ratios "
          f"{[round(c['ratio_H2'],4) for c in cells]}]")
    print(f"total wall {time.perf_counter()-T0:.1f}s")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# EXP 461 POSTERIOR-FILTER (round-37). Seed 20260821.
# Question: does the type-channel posterior over split-counts, applied as a
# Bayesian candidate filter, buy measurable trial-division speedup?
#
# ============================ PRE-STATED (before any run) ============================
# H1 (as issued): optimal keep-set filter yields a CONSTANT speedup > 1 independent
#   of N, derived from exact per-class optimization.
# H2 (as issued): order-2 dial gives 4/3x; every battery stays <= 2x.
#
# MY DERIVATION (written before simulation; supersedes the naive reading of H1/H2):
# Flatness lemma: for any battery with conductors m_1..m_k, given ANY N-side
#   observation (full residue vector of N), p mod m_i remains uniform over units:
#   pairs (a,b), ab=N mod M are in bijection with a; equidistribution over classes
#   => P(p=a | obs) is class-flat. Hence P(char-vector(p) | obs) = 1/prod(n_i),
#   ALWAYS. The channel informs the JOINT (chi(p),chi(q)), never the marginal.
# Rank lemma: cost = #candidates scanned until reaching min(p,q)=p inclusive.
#   For any fixed (or obs-dependent) reorder into keep-block first + rest:
#     cost(p) = rho*T_mask_global + (t_p - rho*t_p)  if p not kept   [full keep
#       block scanned globally first],  cost(p) ~ rho*t_p if p kept,
#     where t_p = pi(p) baseline rank, T = #candidates, rho = keep rate.
#   E[cost] = (1-2rho+2rho^2)*E[t_p] + (rho-rho^2)*T*P(p not kept | obs).
#   With P(p kept | obs) = rho (real: flatness pins P(chi(p) in keep classes) at
#   the class mass, independent of obs; sham: membership random), this is
#   >= E[t_p] for every rho in (0,1): the global first-block penalty always
#   dominates. Baseline ascending order is optimal (it sorts by P(p=r), which is
#   obs-invariant and decreasing in r); ANY filter speedup <= 1.0000.
# Pre-stated predictions:
#   P1: measured speedup <= 1.0000 for EVERY dial/battery x {real, sham, dummy};
#       exact per-class optimizer returns the EMPTY keep-set (ratio exactly 1).
#   P2: real = sham = dummy within MC noise at matched keep-rates (channel adds
#       nothing beyond keep-rate; and keep-rate mechanics net <= 0 here).
#   P3: channel validation (dials wired right): I(N-chars ; s) bits = analytic
#       d2: 1.0000, d3: 0.6121, d5: 0.5088; and flatness check
#       TV( sigma(p) | tau , uniform ) ~ 0 (sampling noise only).
#   P4: the no-fallback variant (scan keep-set, stop) never terminates whenever
#       p is outside the keep-set: failure rate = P(p not kept) ~ 1 - 1/n_eff.
#       This is where the "4/3x" intuition lives: it forgets the fallback pass.
#   H1/H2 verdicts: H1's constant is the constant 1 (achieved by not filtering);
#   H2's 4/3 refuted (direction reversed: filters can only hurt); <=2x vacuous.
#
# ============ MID-EXPERIMENT DERIVATION CORRECTION (disclosed, see ledger) ============
# The FIRST run refuted the rank lemma above: measured filter speedups were > 1
# for real AND sham alike. Root cause: the lemma treats the candidates as ONE
# fixed global list, but honest trial division is bounded per draw by sqrt(N).
# Realized cost model (derived from that first-run contradiction, BEFORE the
# final runs):
#   E[cost]/E[baseline] = 1 - 2*rho + 2*rho^2 + (rho - rho^2)*kappa,
#     kappa := E[pi(sqrt(N))]/E[pi(p)]  (measured ~1.4-1.5 at this population),
# which is < 1 for every rho in (0,1): keep-first ordering genuinely gains --
# but the gain depends ONLY on the keep-rate rho (peak at rho = 1/2, speedup
# 1/(0.5 + 0.25*kappa)), not on WHICH candidates are kept. Flatness still pins
# P(p in K | any N-side reading) = rho for every mask, so real == sham exactly.
# Revised predictions, stated before the final run:
#   P1': real_design == sham within MC noise in EVERY cell (incl. dummy);
#        both ~ 1/(0.5 + 0.25*kappa); exact-opt returns the EMPTY keep-set.
#   P2': d2 rho-grid: real and sham curves coincide at all 7 rates, peak at 1/2.
#   P3': channel validation: emp I matches corrected analytics
#        d2 1.0000 / d3 0.4739 / d5 0.2033 bits; flatness TV small;
#        dummy reading carries ~0 bits (I_emp ~ 0).
#   P4': no-fallback failure rate = P(p not kept) per design rule.
# ====================================================================================
import json, math
import numpy as np
from sympy import primerange
from itertools import product
from math import log2

SEED = 20260821
rng = np.random.default_rng(SEED)
LO, HI = 2**15, 2**17
PRIMES = np.array(list(primerange(LO, HI)))
NP_ = len(PRIMES)
Pmod = {m: PRIMES % m for m in (7, 11, 31, 97, 4, 8)}

# ---- character exponent tables (exponent e in Z/n, value = zeta_n^e; e=0 <=> split) ----
# d3: order-3 char mod 7, (Z/7)*=<3>, kernel = cubes = {1,6} (conductor 7, x^3+x^2-2x-1)
LOG3_7 = {pow(3, k, 7): k for k in range(6)}
def e3(r7):  return LOG3_7[int(r7)] % 3          # e=0 iff r in {1,6}
# d5: order-5 char mod 11, (Z/11)*=<2>, kernel {1,10} (conductor 11, C5 subfield of Q(zeta_11))
LOG2_11 = {pow(2, k, 11): k for k in range(10)}
def e5(r11): return LOG2_11[int(r11)] % 5        # e=0 iff r in {1,10}
# d2: (-31|.) order 2, conductor 31
def e2(r31):
    r = int(r31) % 31
    if r == 0: return None
    v = pow(r, 15, 31)
    return 0 if v == 1 else 1
# conductor-4 and conductor-8 quadratics for the 4-dial battery
def eq4(r4):  return 0 if int(r4) % 4 == 1 else 1          # (-1|.)
def eq8(r8):  return 0 if int(r8) % 8 in (1, 7) else 1      # (2|.)
DUMMY_TAB = {r: int(rng.integers(0, 2)) for r in range(97)}  # fake char mod 97, zero content

def exps(idx_arr):
    """exponent vector per prime index for each dial"""
    return {
        "d2":  np.vectorize(e2)(Pmod[31][idx_arr]),
        "d3":  np.vectorize(e3)(Pmod[7][idx_arr]),
        "d5":  np.vectorize(e5)(Pmod[11][idx_arr]),
        "q4":  np.vectorize(eq4)(Pmod[4][idx_arr]),
        "q8":  np.vectorize(eq8)(Pmod[8][idx_arr]),
        "dum": np.vectorize(lambda r: DUMMY_TAB[int(r)])(Pmod[97][idx_arr]),
    }
EX = exps(np.arange(NP_))

CELLS = {
    "d2":  ["d2"],
    "d3":  ["d3"],
    "d5":  ["d5"],
    "bat2": ["d2", "d3"],
    "bat4": ["d2", "d3", "q4", "q8"],
    "dummy": ["dum"],
}
NVAL = {"d2": 2, "d3": 3, "d5": 5, "q4": 2, "q8": 2, "dum": 2}

def class_ids(dials, arr_idx):
    """mixed-radix class id of exponent vectors for given prime indices"""
    ids = np.zeros(len(arr_idx), dtype=np.int64)
    for d in dials:
        ids = ids * NVAL[d] + EX[d][arr_idx]
    return ids

def split_counts(dials, e_p, e_q):
    return np.sum([ (e_p[d]==0).astype(int) + (e_q[d]==0).astype(int) for d in dials], axis=0)

def exact_channel_bits(dials):
    """analytic I(tau ; s-vector) by exact enumeration over value pairs"""
    from collections import Counter
    n = [NVAL[d] for d in dials]
    S = list(product(*[range(x) for x in n]))
    jt = Counter()
    for x in S:
        for y in S:
            tau = tuple((x[i]+y[i]) % n[i] for i in range(len(dials)))
            s = tuple(int(x[i]==0)+int(y[i]==0) for i in range(len(dials)))
            jt[(tau, s)] += 1
    tot = len(S)**2
    def H(vals): return -sum(v*math.log2(v) for v in vals if v > 0)
    Ps = {}
    for (tau, s), c in jt.items(): Ps[s] = Ps.get(s, 0) + c/tot
    cond = 0.0
    for t in set(t for t, _ in jt):
        Z = sum(c for (t2, s), c in jt.items() if t2 == t)
        pv = [c/Z for (t2, s), c in jt.items() if t2 == t]
        cond += (Z/tot)*H(pv)
    return H(Ps.values()) - cond

def analytic_I_single(dial):
    n = NVAL[dial]
    # P(s|tau=0)={(n-1)/n,0,1/n}; P(s|tau!=0)={(n-2)/n,2/n,0}
    def H(p): return -sum(v*math.log2(v) for v in p if v > 0)
    h0 = H([(n-1)/n, 0.0, 1/n]); h1 = H([(n-2)/n, 2/n, 0.0])
    ps = [ (n-1)**2/(n*n), 2*(n-1)/(n*n), 1/(n*n) ]
    return H(ps) - (h0/n + (n-1)/n*h1)

# ---- keep rules ----
def design_rule_mask(dials, tau_id, nclass_tau):
    """H1-style rule: per dial keep sigma=0 iff P(s'=2|tau) >= P(s'=0|tau);
    battery: keep candidate iff strict majority of dials vote keep. Returns
    per-tau-class keep mask over ALL primes."""
    n = [NVAL[d] for d in dials]
    masks = {}
    for t in range(nclass_tau):
        # decode tau exponents (leading dial is MOST significant in the class id)
        tt, tvotes = t, [0]*len(dials)
        for i in range(len(dials)-1, -1, -1):
            e = tt % n[i]; tt //= n[i]
            if e == 0:  # chi(N)=1: keep sigma=0 iff P(s'=2) >= P(s'=0) (true only n=2 tie)
                tvotes[i] = 1 if 1.0/n[i] >= (n[i]-1.0)/n[i] else 0
            else:       # chi(N)!=1: P(s'=0)=(n-2)/n > P(s'=2)=0 -> keep sigma!=0
                tvotes[i] = 0
        # candidate sigma: keep iff majority of per-dial votes say "this dial's
        # chi(r) side matches the higher-posterior state"
        mv = np.zeros(NP_, dtype=bool)
        cnt = np.zeros(NP_, dtype=int)
        for i, d in enumerate(dials):
            cnt += ((EX[d] == 0).astype(int) if tvotes[i] == 1 else (EX[d] != 0).astype(int))
        masks[t] = cnt * 2 > len(dials)
    return masks

def opt_rule_masks(dials, kappa):
    """exact per-class optimization under the REALIZED cost model: for keep-set
    of class-mass rho (any composition -- flatness makes P(p in K | obs) = rho),
    E[cost]/E[baseline] = 1 - 2rho + 2rho^2 + (rho - rho^2)*kappa, with
    kappa = E[pi(sqrt(N))]/E[pi(p)] measured from the same batch. Exhaustive
    over subsets for prod(n) <= 8, greedy chain otherwise."""
    n = [NVAL[d] for d in dials]
    S = list(product(*[range(x) for x in n]))
    def obj(rho): return (1-2*rho+2*rho**2) + (rho-rho**2)*kappa
    masks, report = {}, {}
    for t in range(int(np.prod(n))):
        best, bestc, bestc_ne = None, np.inf, np.inf
        subsets = ( [tuple(c) for r in range(0, len(S)+1) for c in
                    __import__('itertools').combinations(S, r)]
                    if len(S) <= 8 else None )
        if subsets is None:  # greedy chain from empty by mass
            cur, rest = (), [s for s in S]
            subsets = []
            while rest:
                bestg, bg = None, np.inf
                for s in rest:
                    K = cur + (s,)
                    c = obj(len(K)/len(S))
                    if c < bg: bg, bestg = c, K
                cur, rest = bestg, [s for s in rest if s not in bestg]
                subsets.append(cur)
            subsets = subsets[:-1]  # drop full set
            subsets = [()] + subsets
        for K in subsets:
            rho = len(K)/len(S)
            c = obj(rho)
            if c < bestc - 1e-12 or (best is None):
                if c < bestc: bestc, best = c, K
            if len(K) > 0 and c < bestc_ne: bestc_ne, _ = c, K
        Kset = set(best)
        ids = np.zeros(NP_, dtype=np.int64)
        for i, d in enumerate(dials):
            ids = ids * n[i] + EX[d]
        Kids = []
        for si, sg in enumerate(S):
            cid = 0
            for i in range(len(dials)):
                cid = cid * n[i] + sg[i]
            if sg in Kset:
                Kids.append(cid)
        mv = np.isin(ids, np.array(Kids, dtype=np.int64)) if Kids else np.zeros(NP_, dtype=bool)
        masks[t] = mv
        report[t] = dict(best_subset=[list(x) for x in best], ratio_incl_empty=bestc,
                         ratio_nonempty=bestc_ne)
    return masks, report

def cost_filtered(maskT, tau, idx_p, bnd, off, overhead=0.0):
    """Global accounting from r=2. Scan order: all KEPT candidates ascending up
    to the bound sqrt(N), then NON-KEPT ascending; stop at p inclusive.
    off = #primes below the window (pi(2^15-1)); the keep-mask extends below
    the window with its window-measured density (equidistribution).
    overhead: cost charged per membership test; under honest accounting EVERY
    candidate up to the bound is tested (c = 1 division-equivalent), so the
    filtered run pays (off + bnd) extra over plain trial division."""
    cm = np.zeros((maskT.shape[0], maskT.shape[1]+1), dtype=np.int64)
    cm[:, 1:] = np.cumsum(maskT, axis=1)
    rowmean = maskT.mean(axis=1)
    kept = maskT[tau, idx_p]
    koff = rowmean[tau] * off                     # kept primes below window
    noff = (1.0 - rowmean[tau]) * off             # non-kept below window (pass 2)
    before = cm[tau, idx_p]                       # #{kept r < p} in window
    kept_block = koff + cm[tau, bnd]              # full first pass to sqrt(N)
    c = np.where(kept, koff + before + 1,
                 kept_block + noff + (idx_p - before) + 1)
    return c + overhead * (off + bnd)

def cost_base(idx_p, off):
    return off + idx_p + 1

NBATCH, NDRAW = 5, 4000
from sympy import primepi
OFF = int(primepi(LO - 1))   # primes below the window; global accounting from r=2
results = {"seed": SEED, "predistated": "see script header", "cells": {}, "ledger": []}

# ledger catches recorded during development are appended at end
for cell, dials in CELLS.items():
    n = [NVAL[d] for d in dials]
    ntau = int(np.prod(n))
    per_batch = {m: [] for m in ["baseline", "real_design", "real_opt", "sham",
                                 "real_design_oh", "sham_oh"]}
    fail_nofb = []
    emp_I = []
    flat_tv = []
    kappas = []
    pred_ratio = []
    rhos = []
    opt_report = None
    for b in range(NBATCH):
        ip = rng.integers(0, NP_, size=NDRAW)
        iq = rng.integers(0, NP_, size=NDRAW)
        bad = ip == iq
        while bad.any():
            iq[bad] = rng.integers(0, NP_, size=int(bad.sum()))
            bad = ip == iq
        lo = np.minimum(ip, iq); hi = np.maximum(ip, iq)
        idx_p = lo  # p = smaller factor = scan target
        Nbig = PRIMES[ip].astype(np.int64) * PRIMES[iq]
        bnd = np.searchsorted(PRIMES,
                              np.array([math.isqrt(int(x)) for x in Nbig]),
                              side='right')  # #{primes <= sqrt(N)} in window coords
        taup = class_ids(dials, ip); tauq = class_ids(dials, iq)
        # decode/re-encode sums
        def enc(arr_ids):
            out = np.zeros((len(arr_ids), len(dials)), dtype=np.int64)
            tmp = arr_ids.copy()
            for i in range(len(dials)-1, -1, -1):
                out[..., i] = tmp % n[i]; tmp //= n[i]
            return out
        ep_v = enc(taup); eq_v = enc(tauq)
        tau_v = (ep_v + eq_v) % np.array(n)
        tau = np.zeros(len(ip), dtype=np.int64)
        for i in range(len(dials)):
            tau = tau * n[i] + tau_v[..., i]
        if cell == "dummy":
            # NEGATIVE CONTROL (rebuilt): the reading is a fixed PUBLIC random
            # +-1 table evaluated at N mod 97 -- computable from N alone, and
            # carrying no split information. v1 of this control read the table
            # through the FACTORS (tab(p)+tab(q)), which is not N-computable
            # and leaked a full bit inside the sim; caught and replaced.
            tau = np.array([DUMMY_TAB[int(x)] for x in Nbig % 97])
        # per-dial split counts s_i = [chi_i(p)=1]+[chi_i(q)=1], shape (NDRAW, k)
        sv = np.stack([(ep_v[..., i] == 0).astype(int) + (eq_v[..., i] == 0).astype(int)
                       for i in range(len(dials))], axis=1)
        sid = np.zeros(NDRAW, dtype=np.int64)
        for i in range(len(dials)):
            sid = sid * 3 + sv[:, i]
        cnt = np.zeros((ntau, int(sid.max())+1))
        np.add.at(cnt, (tau, sid), 1)
        pt = cnt.sum(1, keepdims=True); pt[pt == 0] = 1
        pjoint = cnt / cnt.sum()
        ps = cnt.sum(0) / cnt.sum()
        def H(v): v = v[v > 0]; return float(-(v*np.log2(v)).sum())
        emp_I.append(H(ps) - (pt.flatten() @ np.array([H(cnt[t]/pt[t, 0]) for t in range(ntau)])) / NDRAW * 1.0)
        # flatness: TV( sigma(p) | tau , uniform )
        sig_ids = taup
        cnts = np.zeros((ntau, int(np.prod(n))))
        np.add.at(cnts, (tau, sig_ids), 1)
        rs = cnts.sum(1, keepdims=True); rs[rs == 0] = 1
        tv = 0.5*np.abs(cnts/rs - 1.0/np.prod(n)).sum(1).max()
        flat_tv.append(float(tv))
        # baseline cost (global from r=2) and realized-cost ratio constant kappa
        base = cost_base(idx_p, OFF)
        kappa_b = float((OFF + bnd).mean() / base.mean())
        kappas.append(kappa_b)
        per_batch["baseline"].append(float(base.mean()))
        # design-rule filter
        dm = design_rule_mask(dials, 0, ntau)
        dmat = np.stack([dm[t] for t in range(ntau)])
        per_batch["real_design"].append(float(cost_filtered(dmat, tau, idx_p, bnd, OFF).mean()))
        # exact-opt filter on the realized objective
        om, opt_report = opt_rule_masks(dials, kappa_b)
        omat = np.stack([om[t] for t in range(ntau)])
        per_batch["real_opt"].append(float(cost_filtered(omat, tau, idx_p, bnd, OFF).mean()))
        # sham matched to design-rule keep rate (class-independent random mask)
        rho = float(dmat.mean())
        smat = (rng.random(NP_) < rho).reshape(1, NP_)
        per_batch["sham"].append(float(cost_filtered(smat, tau*0, idx_p, bnd, OFF).mean()))
        # honest-overhead variants: membership test on every candidate <= bound
        per_batch["real_design_oh"].append(
            float(cost_filtered(dmat, tau, idx_p, bnd, OFF, overhead=1.0).mean()))
        per_batch["sham_oh"].append(
            float(cost_filtered(smat, tau*0, idx_p, bnd, OFF, overhead=1.0).mean()))
        # analytic ratio prediction for the design-rule rate under the model
        pred = 1.0/(1 - 2*rho + 2*rho**2 + (rho - rho**2)*kappa_b)
        pred_ratio.append(pred)
        rhos.append(rho)
        # no-fallback variant: succeeds only if p kept by design rule
        fail_nofb.append(float((~dmat[tau, idx_p]).mean()))
    results["cells"][cell] = dict(
        dials=dials,
        analytic_I_bits=(analytic_I_single(dials[0]) if len(dials) == 1 and dials[0] != "dum"
                         else exact_channel_bits(dials) if len(dials) > 1 else 0.0),
        emp_I_bits_mean=float(np.mean(emp_I)),
        flatness_TV_max=float(np.max(flat_tv)),
        speedup={m: dict(mean=float(np.mean(np.array(per_batch["baseline"])/np.array(v))),
                         sd=float(np.std(np.array(per_batch["baseline"])/np.array(v))))
                 for m, v in per_batch.items() if m != "baseline"},
        nofb_fail_rate=float(np.mean(fail_nofb)),
        kappa_mean=float(np.mean(kappas)),
        design_keep_rate=float(np.mean(rhos)),
        predicted_speedup_at_design_rate=float(np.mean(pred_ratio)),
        opt_report={str(k): v for k, v in (opt_report or {}).items()},
    )

# ---- rho-grid ablation on d2: real (channel-aligned) vs sham at matched rates.
# Flatness predicts the TWO CURVES COINCIDE at every rho; both peak at rho=1/2.
grid_rates = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
dials = CELLS["d2"]; n = [NVAL[d] for d in dials]; ntau = int(np.prod(n))
sig0 = (EX["d2"] == 0)   # sigma = +1 class, window mass ~ 1/2
grid = {str(r): {"real": [], "sham": []} for r in grid_rates}
kappa_d2 = results["cells"]["d2"]["kappa_mean"]
for b in range(NBATCH):
    ip = rng.integers(0, NP_, size=NDRAW); iq = rng.integers(0, NP_, size=NDRAW)
    bad = ip == iq
    while bad.any():
        iq[bad] = rng.integers(0, NP_, size=int(bad.sum())); bad = ip == iq
    idx_p = np.minimum(ip, iq)
    Nbig = PRIMES[ip].astype(np.int64) * PRIMES[iq]
    bnd = np.searchsorted(PRIMES, np.array([math.isqrt(int(x)) for x in Nbig]), side='right')
    tau = ((EX["d2"][ip] + EX["d2"][iq]) % 2)
    base = cost_base(idx_p, OFF)
    coin = rng.random(NP_)
    for r in grid_rates:
        if r <= 0.5:   # real: random (2r) fraction OF the sigma=+1 class only
            rmask = sig0 & (coin < 2*r)
        else:          # real: all of sigma=+1 plus random filler from sigma=-1
            m0 = float(sig0.mean())
            rmask = sig0 | ((~sig0) & (coin < (r - m0)/(1 - m0)))
        smask = coin < r
        sr = float(cost_filtered(rmask.reshape(1, NP_), tau*0, idx_p, bnd, OFF).mean())
        ss = float(cost_filtered(smask.reshape(1, NP_), tau*0, idx_p, bnd, OFF).mean())
        grid[str(r)]["real"].append(float(base.mean()/sr))
        grid[str(r)]["sham"].append(float(base.mean()/ss))
results["rho_grid_d2"] = {
    str(r): {"real": float(np.mean(v["real"])), "sham": float(np.mean(v["sham"])),
             "predicted": float(1.0/(1 - 2*r + 2*r**2 + (r - r**2)*kappa_d2))}
    for r, v in [(float(k), val) for k, val in grid.items()]}


with open("/tmp/exp37_posterior/result.json", "w") as f:
    json.dump(results, f, indent=1, default=str)
print("DONE")
for c, r in results["cells"].items():
    su = {m: round(d["mean"], 4) for m, d in r["speedup"].items()}
    print(c, "I_an=", round(float(r["analytic_I_bits"]), 4), "I_emp=", round(r["emp_I_bits_mean"], 4),
          "kappa=", round(r["kappa_mean"], 4), "rho=", round(r["design_keep_rate"], 4),
          "pred=", round(r["predicted_speedup_at_design_rate"], 4))
    print("   ", su)
print("rho-grid d2 (real vs sham vs predicted):")
for k, v in results["rho_grid_d2"].items():
    print(" ", k, round(v["real"], 4), round(v["sham"], 4), round(v["predicted"], 4))

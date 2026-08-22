#!/usr/bin/env python3
"""EXP 502 FIXED-BOUND lean (round-45). Base seeds 20260980..20260987.
Paper 168 (exp501): the zero-fit dial T(N) = sum(2/p | QR primes p<=400) loses
~0.064 Spearman when moving from u=2.5 to u=3.5 even at 960 values/N (paired),
read as "mostly intrinsic threshold reweighting" -- with the disclosed caveat
that the convention B = exp(ln vmed/u) makes the STRIP BOUND move with u
(~6510 -> ~529 at the 960 window), changing the strip reach along with the
threshold. This experiment DECOUPLES B FROM VMED: hold the STRIP BOUND fixed
across u and measure the pure reweighting component of paper 168's drop.

Constructions VERBATIM from exp500/exp497/exp499/exp501
(/home/raver1975/factor3/ResearchOutput/scripts/2026-08-21-resume/
exp501_u_harden.py): bitlen-44 balanced window [isqrt(2^43)+1, isqrt(2^44-1))
with exact-bitlen enforcement, inter-prime gap U[1,1e5); sq = isqrt(N);
js = arange(1, 960+1); V = js*(2*sq+js) + (sq*sq - N) (Fermat offsets), SINGLE
window j=1..960 per N; positivity asserted; vmed POOLED per population (median
of the full 1200x960 matrix, as exp501 pooled per arm);
B(u) = max(int(round(exp(ln(vmed)/u))), 50);
T(N) = sum(2.0/q | q in primerange(3, 401), powmod(N mod q, (q-1)//2, q) == 1)
(window-independent, once per population); Spearman via ordinal argsort
(verbatim exp497); bootstrap = 500 resamples of the 8 populations.

ARMS, all on the SAME V (same values, same vmed, same B(u)):
  VAR        paper-168 reproduction: strip primes <= B_u; smooth@u iff residual==1
             (verbatim exp501 smooth_mask semantics: W==1 after full-multiplicity
             strip to B_u).
  FIXED      this experiment: ONE strip to PB = 8000 (u-INDEPENDENT);
             smooth@u iff (rem_PB == 1) & (maxp_PB <= B_u), maxp_PB = largest
             strip prime seen dividing the value, rem_PB = residual after
             stripping all primes <= PB.
  FIXED4000  side cell: the design sheet's literal PB=4000, kept for the record
             (see DEVIATION): smooth@u iff (rem_4000 == 1) & (maxp_4000 <= B_u),
             both frozen at the 4000 checkpoint of the same pass.

DEVIATION (disclosed, forced before any data): the design sheet sets PB=4000
quoting "356 vs 3736" -- those are the 240-WINDOW bounds of exp501. At THIS
experiment's mandated single 960 window, pooled vmed ~ 3.4e9 gives B(2.5) ~
6510 > 4000, violating the sheet's own precondition "(both <= PB)". A PB below
B(2.5) makes the fixed arm strictly TIGHTER than the u=2.5 threshold (blind to
prime factors in (4000, 6510]), re-introducing exactly the visibility confound
the experiment is meant to remove. PB is therefore 8000 (covers max B_u with
headroom, held FIXED across u; asserted per population), and the literal
PB=4000 survives as the FIXED4000 side cell.

PRE-STATED HYPOTHESES (written BEFORE any exp-502 data):
  Sheet H1 (bound-shrinkage): with the strip bound fixed, Delta_fixed =
                     sp(2.5,fixed) - sp(3.5,fixed) is SMALLER than paper 168's
                     variable-B Delta(960) = +0.0636; attribution =
                     (Delta_varB - Delta_fixed)/Delta_varB > 0.5.
  Sheet H2 (intrinsic):     even with fixed bound, residual Delta_fixed >= 0.03.
  Decision rule (sheet, verbatim): H1 iff attribution > 0.5; H2 iff
  Delta_fixed >= 0.03; both can hold.
  PRE-REGISTERED STRUCTURAL PREDICTION (same commit, before data): under the
  rem==1 convention with PB >= max(B_u), the two acceptance rules are
  LOGICALLY IDENTICAL:
     rem_PB==1 & maxp<=B_u  <=>  every prime factor <= B_u
                            <=>  residual after stripping to B_u is 1.
  Prediction: mask_FIXED == mask_VAR elementwise for BOTH u in every
  population; Delta_fixed == Delta_varB to machine precision; attribution = 0.
  I.e. sheet H1 is predicted FALSE *by construction*: the strip bound is
  INVISIBLE to the accepted set under this convention (a compute-cost knob,
  not a measurement knob), so paper 168's entire +0.0636 should be intrinsic
  reweighting (sheet H2 predicted TRUE). Empirical content of this run:
  verify the identity BITWISE on fresh seeds via two independent acceptance
  paths over one shared division engine, and quantify what the LITERAL
  PB=4000 would have distorted (FIXED4000 side cell).

# BARRIERS (standard lines, verbatim exp501/exp500/exp499):
#   Barrier 5 (structural orthogonality): T is an N-only natural coordinate; the
#   dial predicts relation yield (difficulty), not (p,q) - no which-factor claim
#   made or tested.
#   Barrier 8 (known-method-in-disguise): the measured object is the QS/CFRAC
#   relation-yield dial - a cost predictor FOR known methods, not a new
#   factoring route.
"""
import json, time, math, datetime, os
import numpy as np
import gmpy2
from sympy import primerange, nextprime

BASE = 20260980
NSEED = 8
NN = 1200
W = 960
US = (2.5, 3.5)
PB = 8000            # fixed strip bound for the FIXED arm (covers max B_u)
PB_LIT = 4000        # design-sheet literal bound (side cell)
CKPT = PB_LIT
BOOT_N = 500
BOOT_SEED = 20260988
T0 = time.time()
WORK = "/tmp/exp45_fixb"
OUT = {"meta": {"base_seed": BASE, "exp": 502, "codename": "FIXED-BOUND",
                "round": 45,
                "populations": [BASE + k for k in range(NSEED)],
                "Ns_per_population": NN, "window": W, "us": list(US),
                "PB_fixed": PB, "PB_literal_sidecell": PB_LIT,
                "boot_resamples": BOOT_N,
                "constructions": "verbatim exp497/exp499/exp500/exp501 bitlen-44 "
                                 "balanced arm; SINGLE window j=1..960; vmed pooled "
                                 "per population; B(u)=max(int(round(exp(ln vmed/u))),50)",
                "deviation": "design sheet PB=4000 presumed both B_u<=PB (240-window "
                             "numbers 356/3736); at the mandated 960 window B(2.5)~6510 "
                             "> 4000, so PB raised to 8000 to satisfy the sheet's own "
                             "'both <= PB' precondition; literal PB=4000 kept as side cell",
                "prestated": {
                    "H1_sheet_boundshrinkage": "attribution=(dVarB-dFix)/dVarB > 0.5",
                    "H2_sheet_intrinsic": "Delta_fixed >= 0.03",
                    "preregistered_structure": "mask_FIXED==mask_VAR elementwise both u "
                                               "(logical identity under rem==1, PB>=max B_u); "
                                               "predict attribution=0, H1 FALSE, H2 TRUE",
                    "rule": "H1 iff attribution>0.5; H2 iff Delta_fixed>=0.03; "
                            "both->BOTH, neither->NEITHER"}},
        "rows": []}

def ledger(event, **kw):
    rec = {"ts": datetime.datetime.now().isoformat(timespec="seconds"),
           "round": 45, "exp": 502, "codename": "FIXED-BOUND",
           "event": event, "t_s": round(time.time() - T0, 1)}
    rec.update(kw)
    with open(f"{WORK}/ledger_exp502.jsonl", "a") as f:
        f.write(json.dumps(rec, default=float) + "\n")
    return rec

def checkpoint():
    json.dump(OUT, open(f"{WORK}/result.json", "w"), indent=1, default=float)

primes_pb = np.array(list(primerange(2, PB + 1)), dtype=np.int64)

def strip_engine(V, B, ckpt=None):
    """Full-multiplicity trial division of every element by all primes <= B.
    Returns (residual_after_primes_le_B, maxp_largest_prime_seen).
    Semantics match exp501 smooth_mask exactly (its smooth iff residual==1);
    the subset-refined multiplicity loop is an internal speedup with identical
    output. Optional checkpoint: residual snapshot taken after all primes
    <= ckpt are consumed (ckpt < B)."""
    Wk = V.copy()
    flat = Wk.reshape(-1)
    maxp = np.zeros(flat.shape, dtype=np.int64)
    snap = None
    for p in primes_pb[primes_pb <= B]:
        if snap is None and ckpt is not None and p > ckpt:
            snap = Wk.copy()
        m = (flat % p) == 0
        if not m.any():
            continue
        idx = np.flatnonzero(m)
        sub = flat[idx]
        while True:
            ms = (sub % p) == 0
            if not ms.any():
                break
            sub[ms] //= p
        flat[idx] = sub
        maxp[idx] = p          # ascending primes: last writer is the largest
    if snap is None and ckpt is not None:
        snap = Wk.copy()       # B <= ckpt edge (never hit here)
    return Wk, maxp.reshape(V.shape), snap

def spearman(a, b):
    # verbatim exp497/exp500/exp501 (ordinal argsort)
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])

LO = int(gmpy2.isqrt(1 << 43)) + 1
HI = int(gmpy2.isqrt((1 << 44) - 1))

def draw_one(rng):
    # verbatim exp499/exp500/exp501 draw_balanced
    while True:
        r = int(rng.integers(LO, HI))
        p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, 10**5))))
        N = p * q
        if not ((1 << 43) <= N < (1 << 44)):
            continue
        return N, math.isqrt(N)

def fermat_offsets(Ns, sqs, Wmax):
    # verbatim V = js*(2*sq+js) + (sq*sq - N), vectorized over Ns
    js = np.arange(1, Wmax + 1, dtype=np.int64)
    sq = np.asarray(sqs, dtype=np.int64)[:, None]
    N = np.asarray(Ns, dtype=np.int64)[:, None]
    V = js[None, :] * (2 * sq + js[None, :]) + (sq * sq - N)
    assert (V > 0).all(), "positivity violated"
    return V

wr = list(primerange(3, 401))

def t_dial(Ns):
    # verbatim exp497/exp500/exp501 (window-independent, once per population)
    return np.array([sum(2.0/q for q in wr
                         if gmpy2.powmod(int(N) % q, (q - 1) // 2, q) == 1)
                     for N in Ns], float)

os.makedirs(WORK, exist_ok=True)

ledger("start", base_seed=BASE, workdir=WORK, n_populations=NSEED,
       Ns_per_population=NN, window=W, us=list(US), PB=PB, PB_side=PB_LIT,
       constructions=OUT["meta"]["constructions"], deviation=OUT["meta"]["deviation"],
       prestated=OUT["meta"]["prestated"])
checkpoint()

for k in range(NSEED):
    seed = BASE + k
    tp = time.time()
    rng = np.random.default_rng(seed)
    pairs = [draw_one(rng) for _ in range(NN)]
    Ns = [d[0] for d in pairs]
    sqs = [d[1] for d in pairs]
    Ts = t_dial(Ns)
    V = fermat_offsets(Ns, sqs, W)
    vmed = float(np.median(V.astype(float)))
    Bus = {u: max(int(round(math.exp(math.log(vmed) / u))), 50) for u in US}
    assert Bus[2.5] <= PB and Bus[3.5] <= PB, f"B_u exceeds PB: {Bus}"

    # VAR arm (paper-168 reproduction): strip to B_u, smooth iff residual==1
    res25, mp25, _ = strip_engine(V, Bus[2.5])
    res35, mp35, _ = strip_engine(V, Bus[3.5])
    var25 = res25 == 1
    var35 = res35 == 1

    # FIXED arm: ONE strip to PB, acceptance (rem==1)&(maxp<=B_u)
    resPB, mpPB, rem4k = strip_engine(V, PB, ckpt=CKPT)
    fix25 = (resPB == 1) & (mpPB <= Bus[2.5])
    fix35 = (resPB == 1) & (mpPB <= Bus[3.5])

    # FIXED4000 side cell (literal design-sheet bound, frozen at checkpoint)
    fix4k25 = (rem4k == 1) & (mpPB <= Bus[2.5])
    fix4k35 = (rem4k == 1) & (mpPB <= Bus[3.5])

    ident = {"u25_fix_eq_var": bool(np.array_equal(fix25, var25)),
             "u35_fix_eq_var": bool(np.array_equal(fix35, var35))}
    rate = lambda m: m.reshape(NN, W).mean(axis=1)
    r = {"seed": seed, "vmed": round(vmed, 1), "B25": Bus[2.5], "B35": Bus[3.5],
         "sp_var_2.5": spearman(Ts, rate(var25)),
         "sp_var_3.5": spearman(Ts, rate(var35)),
         "sp_fix_2.5": spearman(Ts, rate(fix25)),
         "sp_fix_3.5": spearman(Ts, rate(fix35)),
         "sp_fix4000_2.5": spearman(Ts, rate(fix4k25)),
         "sp_fix4000_3.5": spearman(Ts, rate(fix4k35)),
         "mean_rate_var_2.5": float(rate(var25).mean()),
         "mean_rate_var_3.5": float(rate(var35).mean()),
         "mean_rate_fix_2.5": float(rate(fix25).mean()),
         "mean_rate_fix_3.5": float(rate(fix35).mean()),
         "zero_frac_var_2.5": float((rate(var25) == 0).mean()),
         "zero_frac_var_3.5": float((rate(var35) == 0).mean())}
    r["delta_var"] = r["sp_var_2.5"] - r["sp_var_3.5"]
    r["delta_fix"] = r["sp_fix_2.5"] - r["sp_fix_3.5"]
    r["delta_fix4000"] = r["sp_fix4000_2.5"] - r["sp_fix4000_3.5"]
    r["identity_masks_hold"] = ident["u25_fix_eq_var"] and ident["u35_fix_eq_var"]
    r["bitlen_range"] = [int(min(Ns).bit_length()), int(max(Ns).bit_length())]
    OUT["rows"].append(r)
    checkpoint()
    ledger("population_done", seed=seed, vmed=r["vmed"], B25=r["B25"], B35=r["B35"],
           sp_var_25=round(r["sp_var_2.5"], 4), sp_var_35=round(r["sp_var_3.5"], 4),
           sp_fix_25=round(r["sp_fix_2.5"], 4), sp_fix_35=round(r["sp_fix_3.5"], 4),
           sp_fix4000_25=round(r["sp_fix4000_2.5"], 4),
           sp_fix4000_35=round(r["sp_fix4000_3.5"], 4),
           delta_var=round(r["delta_var"], 4), delta_fix=round(r["delta_fix"], 4),
           delta_fix4000=round(r["delta_fix4000"], 4),
           mean_rates=[round(r[f"mean_rate_{a}_{u}"], 4)
                       for a in ("var", "fix") for u in ("2.5", "3.5")],
           identity_masks_hold=r["identity_masks_hold"],
           pop_seconds=round(time.time() - tp, 1))
    print(seed, "dvar=%+.4f dfix=%+.4f dfix4k=%+.4f" %
          (r["delta_var"], r["delta_fix"], r["delta_fix4000"]),
          "cells var %.3f/%.3f fix %.3f/%.3f" %
          (r["sp_var_2.5"], r["sp_var_3.5"], r["sp_fix_2.5"], r["sp_fix_3.5"]),
          "rates %.4f/%.4f/%.4f/%.4f" %
          (r["mean_rate_var_2.5"], r["mean_rate_var_3.5"],
           r["mean_rate_fix_2.5"], r["mean_rate_fix_3.5"]),
          "ident", ident, round(time.time() - tp, 1), "s", flush=True)

# ---- summary + verdict ----
rows = OUT["rows"]
g = lambda key: [rr[key] for rr in rows]
mean = lambda x: sum(x) / len(x)
sd = lambda x: (sum((v - mean(x))**2 for v in x) / (len(x) - 1))**0.5
boot = np.random.default_rng(BOOT_SEED)
idx = lambda: boot.integers(0, NSEED, NSEED)
def boot_stats(keyfn):
    vals = []
    for _ in range(BOOT_N):
        ii = idx()
        vals.append(keyfn([rows[i] for i in ii]))
    return np.array(vals)
bs_dfix = boot_stats(lambda rs: mean([x["delta_fix"] for x in rs]))
bs_dvar = boot_stats(lambda rs: mean([x["delta_var"] for x in rs]))
bs_attr = boot_stats(lambda rs: (mean([x["delta_var"] for x in rs]) -
                                 mean([x["delta_fix"] for x in rs])) /
                                mean([x["delta_var"] for x in rs]))
ci = lambda a: [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]
m_dfix, m_dvar = mean(g("delta_fix")), mean(g("delta_var"))
m_attr = (m_dvar - m_dfix) / m_dvar if abs(m_dvar) > 1e-12 else float("nan")
paper168_d960 = 0.0636
OUT["summary"] = {
    "cells": {f"{a}_{u}": {"mean": round(mean(g(f"sp_{a}_{u}")), 4),
                           "sd": round(sd(g(f"sp_{a}_{u}")), 4)}
              for a in ("var", "fix", "fix4000") for u in US},
    "delta_fixed": {"mean": round(m_dfix, 4), "sd": round(sd(g("delta_fix")), 4),
                    "bootstrap_CI": [round(v, 4) for v in ci(bs_dfix)]},
    "delta_varB_reproduction": {"mean": round(m_dvar, 4),
                                "sd": round(sd(g("delta_var")), 4),
                                "bootstrap_CI": [round(v, 4) for v in ci(bs_dvar)],
                                "paper168_delta960_reference": paper168_d960},
    "delta_fixed4000_sidecell": {
        "mean": round(mean(g("delta_fix4000")), 4),
        "sd": round(sd(g("delta_fix4000")), 4)},
    "attribution": {"mean": round(m_attr, 4),
                    "bootstrap_CI": [round(v, 4) for v in ci(bs_attr)],
                    "formula": "(Delta_varB - Delta_fixed)/Delta_varB"},
    "mean_rates": {f"{a}_{u}": round(mean(g(f"mean_rate_{a}_{u}")), 5)
                   for a in ("var", "fix") for u in US},
    "zero_fracs": {f"var_{u}": round(mean(g(f"zero_frac_var_{u}")), 4) for u in US},
    "bounds": {"B25_per_population": g("B25"), "B35_per_population": g("B35"),
               "PB_fixed": PB},
    "identity_masks_hold_all": bool(all(x["identity_masks_hold"] for x in rows))}
h1 = bool(m_attr > 0.5)
h2 = bool(m_dfix >= 0.03)
name = "BOTH" if (h1 and h2) else ("H1" if h1 else ("H2" if h2 else "NEITHER"))
OUT["verdict"] = {"H1_bound_shrinkage": h1, "H2_intrinsic_residual": h2,
                  "verdict_name": name,
                  "rule_detail": {"attribution_mean": round(m_attr, 4),
                                  "Delta_fixed_mean": round(m_dfix, 4),
                                  "Delta_varB_mean": round(m_dvar, 4),
                                  "paper168_Delta960": paper168_d960}}
OUT["barrier_lines"] = {
    "barrier_5": "Structural orthogonality: T is an N-only natural coordinate; the "
                 "dial predicts relation yield (difficulty), not (p,q) - no "
                 "which-factor claim made or tested.",
    "barrier_8": "Known-method-in-disguise: the measured object is the QS/CFRAC "
                 "relation-yield dial - a cost predictor FOR known methods, not a "
                 "new factoring route."}
OUT["artifacts"] = [f"{WORK}/exp502_fixed_bound.py", f"{WORK}/result.json",
                    f"{WORK}/ledger_exp502.jsonl"]
checkpoint()
cif = ci(bs_dfix); civ = ci(bs_dvar); cia = ci(bs_attr)
headline = (f"FIXED-BOUND exp502: VERDICT {name}; "
            f"dfix mean={m_dfix:+.4f} CI=[{cif[0]:+.4f},{cif[1]:+.4f}]; "
            f"dvarB mean={m_dvar:+.4f} CI=[{civ[0]:+.4f},{civ[1]:+.4f}] "
            f"(paper168 d960=+0.0636); attribution={m_attr:+.4f} "
            f"CI=[{cia[0]:+.4f},{cia[1]:+.4f}]; "
            f"mask identity 8/8 pops: {OUT['summary']['identity_masks_hold_all']}")
ledger("DONE", seed=BASE, status="DONE", headline=headline, verdict=OUT["verdict"],
       summary=OUT["summary"], barriers=["5", "8"], artifacts=OUT["artifacts"])
print(json.dumps(OUT["summary"]["cells"]))
print(json.dumps(OUT["verdict"]))
print(headline)
print("DONE", round(time.time() - T0, 1), "s")

#!/usr/bin/env python3
"""EXP 523 BALANCED-BKEY lean (round-54). Seeds 20261100..03 per bitlen.

QUESTION (papers 178/179 vs paper 184 author flag): Spearman(T, rate) dropped to
~0.405-0.437 at bitlen 56/60 on balanced draws.  Is that drop an ARTIFACT of the
B-keying convention -- B = exp(ln vmed/u) keyed to the SAME values being tested
(circular dependency manufacturing starvation at high bitlen) -- or INTRINSIC to
the dial at high bitlen?  Test: re-key B to the remainder scale (fixed strip
bound PB=8000) and to a DESIGN-FIXED bound that never touches sampled data.

========================= PRE-STATED HYPOTHESES =========================
(Written BEFORE any bitlen-44/52/56/60 data of this experiment was generated.)

  H1 (convention-dependent): the drop disappears when B is keyed to the
      remainder median instead of vmed --
      sp(T, rate@rem-keyed-B) >= 0.55 at bitlen 56.
  H2 (intrinsic): even with rem-keyed B, the drop persists --
      sp < 0.50 at bitlen 56.

FROZEN DECISION RULES (before data):
  - Primary cell: u = 2.5 (the validated dial setting of papers 164/175),
    statistic = MEAN over the 4 seeds (20261100..03) of scipy.spearmanr(T, rate)
    at bitlen 56.
  - H1 TRUE  iff mean_seed(sp_B) >= 0.55   (convention-dependent).
  - H2 TRUE  iff mean_seed(sp_B) <  0.50   (intrinsic).
  - 0.50 <= mean < 0.55 -> MIXED zone, neither cleanly.
  - Verdict names:
      A-drop reproduced (mean sp_A(56) < 0.50) AND H1 -> BKEY-ARTIFACT-CONFIRMED
      H2                                            -> BKEY-INTRINSIC-DROP
      mixed zone                                    -> BKEY-MIXED-ZONE
      A healthy at 56 (>= 0.50, premise fails to replicate under the
      paper-164 pooled convention)                  -> BKEY-A-HEALTHY-NOREP

FROZEN DESIGN (before data):
  - Populations: 1200 balanced semiprimes per seed-cell; builder VERBATIM
    exp497/exp508 (exp499 window shift): lo = isqrt(2^(L-1))+1,
    hi = isqrt(2^L - 1), r ~ U[lo,hi), p = nextprime(r),
    q = nextprime(p + gap), gap ~ U[1,1e5), N forced to exact bitlen L
    (strays redrawn), V.min()>0 required.
  - Relation values: 240 per N, Fermat offset family VERBATIM exp497:
    js = arange(1,241), V = js*(2*sq+js) + (sq*sq - N) = (sq+j)^2 - N.
  - Convention A (paper-164 verbatim, exp495 line 43): vmed = median of ALL
    pooled values of the seed-cell (1200x240); B_A(u) = max(round(exp(ln(vmed)/u)),50);
    rate = fraction of the N's 240 values FULLY B-smooth (strip primes <= B
    until fixed, smooth iff leftover == 1) -- smooth_mask verbatim exp497.
  - Convention B (remainder-keyed): strip EVERY value once to the FIXED bound
    PB=8000 (independent of any vmed); rem_median = median of ALL pooled
    post-strip remainders (literal, 1s included); B_B(u) = max(round(exp(ln(rem_median)/u)),50).
    Hit rule IDENTICAL to A (full B_B-smoothness) -- only the KEYING changes,
    so any recovery attributes to the keying alone.
  - Sensitivity arm S (labeled): rem_median_excl1 (remainders > 1 only),
    B_S(2.5) -- checks the literal-median choice against the 1s.
  - Convention C (design-fixed bonus arm, task preamble "FIXED bound
    independent of vmed"): B_C(u) = max(round(exp(ln(vm_theory)/u)),50) with
    vm_theory(L) = 240 * isqrt(2^(L-1)) -- pure function of the DESIGN (bitlen),
    zero dependence on sampled data.
  - u grid: {2.0, 2.5, 3.0}; primary decisions at u=2.5.
  - Features VERBATIM paper-164: T(N) = sum(2/p | odd primes p<=400,
    powmod(N mod p,(p-1)//2,p)==1); comparator count = #{odd primes q<=100:
    same Euler criterion}.
  - Stats: scipy.stats.spearmanr (tie-corrected; matches papers 178/179
    anchors) primary; exp497 argsort-rank trick stored alongside (matches
    papers 164/175 lineage).  Bootstrap 300 resamples, percentile 95% CIs.
  - Diagnostics: realized u on remainder scale ln(rem_median)/ln(B_A) per cell
    (paper-178 addendum metric: expect ~2.5 at 44 rising toward ~3.75 at 56 if
    the artifact account replicates); mean_rate, zero-hit Ns per arm.
  - Sweep order: seed-major (seed k=0 covers all 4 bitlens first), so the full
    grid has >=1 seed early; graceful degradation: if elapsed > 600 s, remaining
    cells drop u != 2.5 arms (logged).

# BARRIERS (standard lines):
#   Barrier 5 (structural orthogonality): T is an N-only natural coordinate; the
#   dial predicts relation yield (difficulty), not (p,q) - no which-factor claim
#   made or tested.
#   Barrier 8 (known-method-in-disguise): the measured object is the QS/CFRAC
#   relation-yield dial - a cost predictor FOR known methods, not a new
#   factoring route.
"""
import json, math, time, datetime
import numpy as np
import gmpy2
from sympy import primerange
from scipy.stats import spearmanr

WORK = "/tmp/exp54_bkey"
SEEDS = [20261100, 20261101, 20261102, 20261103]
BITLENS = [44, 52, 56, 60]
U_GRID = [2.0, 2.5, 3.0]
PB = 8000
NPOP = 1200
NOFF = 240
BOOT = 300
TIME_SOFT = 600.0
T0 = time.time()

RES = {"meta": {"exp": 523, "codename": "BALANCED-BKEY", "round": 54,
                "seeds": SEEDS, "bitlens": BITLENS, "u_grid": U_GRID,
                "PB": PB, "n_pop": NPOP, "n_offsets": NOFF,
                "bootstrap": BOOT},
       "prestated": {
           "H1": "convention-dependent: sp(T, rate@rem-keyed-B) >= 0.55 at bitlen 56 "
                 "(mean over seeds 20261100-03, u=2.5)",
           "H2": "intrinsic: sp(T, rate@rem-keyed-B) < 0.50 at bitlen 56 (same cell)",
           "rules": "H1 TRUE iff mean_sp_B >= 0.55; H2 TRUE iff mean_sp_B < 0.50; "
                    "else MIXED. Verdict names: BKEY-ARTIFACT-CONFIRMED / "
                    "BKEY-INTRINSIC-DROP / BKEY-MIXED-ZONE / BKEY-A-HEALTHY-NOREP"},
       "rows": [], "degraded": None}

def ledger(event, **kw):
    rec = {"ts": datetime.datetime.now().isoformat(timespec="seconds"),
           "round": 54, "exp": 523, "codename": "BALANCED-BKEY",
           "event": event, "t_s": round(time.time() - T0, 1)}
    rec.update(kw)
    with open(f"{WORK}/ledger_exp523.jsonl", "a") as f:
        f.write(json.dumps(rec, default=float) + "\n")
    return rec

def checkpoint():
    json.dump(RES, open(f"{WORK}/result.json", "w"), indent=1, default=float)

PRIMES = np.array(list(primerange(2, 1100000)), dtype=np.int64)

def _prime_slice(bound):
    return PRIMES[PRIMES <= bound]

def strip_to(V, bound):
    """Strip all primes <= bound from V (vectorized, exp497 smooth_mask core)."""
    W = V.copy()
    for p in _prime_slice(bound):
        while True:
            m = W % p == 0
            if not m.any(): break
            W[m] //= p
            if not (W % p == 0).any(): break
    return W

def staged_masks(V, bounds):
    """One ascending prime sweep to max(bounds); snapshot W==1 mask at each bound.
    Bounds processed ASCENDING so the mask for bound b is snapshotted exactly
    after all primes <= b have been stripped and before any larger prime.
    Equivalent to independent smooth_mask calls per bound, shared work."""
    bs = sorted(set(int(b) for b in bounds))          # ascending
    W = V.copy()
    out = {}
    primes = _prime_slice(bs[-1])
    bi = 0
    for p in primes:
        while bi < len(bs) and p > bs[bi]:
            out[bs[bi]] = (W == 1)
            bi += 1
        while True:
            m = W % p == 0
            if not m.any(): break
            W[m] //= p
            if not (W % p == 0).any(): break
    while bi < len(bs):
        out[bs[bi]] = (W == 1)
        bi += 1
    return out

def draw_balanced(rng, L):
    """VERBATIM exp508 (exp497 construction, exp499 window shift)."""
    lo = int(gmpy2.isqrt(1 << (L - 1))) + 1
    hi = int(gmpy2.isqrt((1 << L) - 1))
    while True:
        r = int(rng.integers(lo, hi))
        p = int(gmpy2.next_prime(r))    # same math as sympy.nextprime, faster
        q = int(gmpy2.next_prime(p + int(rng.integers(1, 10**5))))
        N = p * q
        if not ((1 << (L - 1)) <= N < (1 << L)):
            continue
        sq = math.isqrt(N)
        js = np.arange(1, NOFF + 1, dtype=np.int64)
        V = js * (2 * sq + js) + (sq * sq - N)
        if V.min() <= 0:
            continue
        return N, sq, V

wr = list(primerange(3, 401))
cnt_primes = list(primerange(3, 101))

def t_dial(Ns):
    return np.array([sum(2.0/q for q in wr
                         if gmpy2.powmod(N % q, (q - 1) // 2, q) == 1)
                     for N in Ns], float)

def qr_count(Ns):
    return np.array([sum(1 for q in cnt_primes
                         if gmpy2.powmod(N % q, (q - 1) // 2, q) == 1)
                     for N in Ns], float)

def spearman_trick(a, b):
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])

def boot_ci(x, y, seed):
    rngb = np.random.default_rng(seed)
    n = len(x); vals = []
    for _ in range(BOOT):
        idx = rngb.integers(0, n, n)
        vals.append(spearmanr(x[idx], y[idx]).statistic)
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]

ledger("start", seeds=SEEDS, bitlens=BITLENS, u_grid=U_GRID, workdir=WORK)
checkpoint()

u_grid_active = list(U_GRID)

for sweep, seed in enumerate(SEEDS):
    for L in BITLENS:
        if RES["degraded"] is not None:
            u_grid_cell = [2.5]
        else:
            u_grid_cell = u_grid_active
        t_cell = time.time()
        rng = np.random.default_rng(seed)
        data = [draw_balanced(rng, L) for _ in range(NPOP)]
        Ns = [d[0] for d in data]
        Vall = np.concatenate([d[2] for d in data])
        t_draw = time.time() - t_cell

        Ts = t_dial(Ns)
        Cs = qr_count(Ns)

        # ---- Convention A keying (paper-164 verbatim, pooled vmed) ----
        vmed = float(np.median(Vall.astype(float)))
        # ---- Convention B keying: fixed strip PB=8000, remainder median ----
        Rem = strip_to(Vall, PB)
        rem_med = float(np.median(Rem.astype(float)))
        pos = Rem[Rem > 1]
        rem_med_excl1 = float(np.median(pos.astype(float))) if pos.size else 1.0
        # ---- Convention C keying: design-fixed, no sampled-data input ----
        vm_theory = 240.0 * float(gmpy2.isqrt(1 << (L - 1)))

        keys = {}
        for u in u_grid_cell:
            keys[f"A{u}"] = max(int(round(math.exp(math.log(vmed) / u))), 50)
            keys[f"B{u}"] = max(int(round(math.exp(math.log(rem_med) / u))), 50)
            keys[f"C{u}"] = max(int(round(math.exp(math.log(vm_theory) / u))), 50)
        if 2.5 in u_grid_cell:
            keys["S2.5"] = max(int(round(math.exp(math.log(rem_med_excl1) / 2.5))), 50)
        masks = staged_masks(Vall, list(keys.values()))

        row = {"bitlen": L, "seed": seed, "sweep": sweep,
               "vmed": round(vmed, 1), "rem_median": round(rem_med, 1),
               "rem_median_excl1": round(rem_med_excl1, 1),
               "vm_theory": round(vm_theory, 1),
               "realized_u_rem_scale_A2.5":
                   round(math.log(rem_med) / math.log(keys["A2.5"]), 3)
                   if "A2.5" in keys else None,
               "t_draw_s": round(t_draw, 1)}
        for key, B in keys.items():
            conv = key[0]
            u = float(key[1:]) if conv != "S" else 2.5
            sm = masks[B].reshape(NPOP, NOFF)
            rate = sm.mean(axis=1)
            sT = float(spearmanr(Ts, rate).statistic)
            sC = float(spearmanr(Cs, rate).statistic)
            ci = boot_ci(Ts, rate, seed=seed + 90000 * L + int(u * 10)) \
                 if u == 2.5 else None
            row[key] = {
                "B": int(B), "mean_rate": round(float(rate.mean()), 5),
                "zero_hit_Ns": int((rate == 0).sum()),
                "sp_T": round(sT, 4), "sp_T_ci": [round(c, 4) for c in ci] if ci else None,
                "sp_T_trick": round(spearman_trick(Ts, rate), 4),
                "sp_count": round(sC, 4), "advantage": round(sT - sC, 4)}

        RES["rows"].append(row)
        checkpoint()
        ledger("cell_done", bitlen=L, seed=seed,
               **{k: (row[k]["sp_T"] if isinstance(row.get(k), dict) else row[k])
                  for k in row
                  if k not in ("t_draw_s", "bitlen", "seed", "sweep")},
               cell_s=round(time.time() - t_cell, 1))
        print(f"[cell] L={L} seed={seed} "
              f"A2.5={row['A2.5']['sp_T']:.4f} B2.5={row['B2.5']['sp_T']:.4f} "
              f"C2.5={row['C2.5']['sp_T']:.4f} rateA={row['A2.5']['mean_rate']:.4f} "
              f"rateB={row['B2.5']['mean_rate']:.4f} u_eff={row['realized_u_rem_scale_A2.5']} "
              f"({time.time()-T0:.0f}s)", flush=True)

        if RES["degraded"] is None and time.time() - T0 > TIME_SOFT \
           and not (sweep == len(SEEDS) - 1 and L == BITLENS[-1]):
            RES["degraded"] = {"at_t_s": round(time.time() - T0, 1),
                               "note": "u grid restricted to [2.5] for remaining cells"}
            ledger("degraded_u_grid", **RES["degraded"])
            checkpoint()

# ---------------- summary + verdicts -------------------------------------------
import collections
cells = collections.defaultdict(list)
for r in RES["rows"]:
    for key in ("A2.0", "A2.5", "A3.0", "B2.0", "B2.5", "B3.0",
                "C2.0", "C2.5", "C3.0", "S2.5"):
        if key in r:
            cells[(key, r["bitlen"])].append(r[key]["sp_T"])
grid = {}
for (key, L), vals in sorted(cells.items()):
    grid[f"{key}@L{L}"] = {"n": len(vals),
                           "mean": round(sum(vals)/len(vals), 4),
                           "min": round(min(vals), 4), "max": round(max(vals), 4)}
RES["summary"] = {"grid_mean_sp_T": grid}

def mean_of(key, L):
    v = cells.get((key, L), [])
    return sum(v)/len(v) if v else None

mB56 = mean_of("B2.5", 56)
mA56 = mean_of("A2.5", 56)
H1 = mB56 is not None and mB56 >= 0.55
H2 = mB56 is not None and mB56 < 0.50
mixed = (not H1) and (not H2)
A_starves = mA56 is not None and mA56 < 0.50

if H2:
    verdict_name = "BKEY-INTRINSIC-DROP"
elif mixed:
    verdict_name = "BKEY-MIXED-ZONE"
elif H1 and A_starves:
    verdict_name = "BKEY-ARTIFACT-CONFIRMED"
elif H1:
    verdict_name = "BKEY-RECOVERED-BUT-A-NOT-STARVED"
else:
    verdict_name = "BKEY-INDETERMINATE"

RES["verdict"] = {
    "verdict_name": verdict_name,
    "H1_convention_dependent": bool(H1), "H1_stat": round(mB56, 4) if mB56 else None,
    "H2_intrinsic": bool(H2), "H2_stat": round(mB56, 4) if mB56 else None,
    "mixed_zone": bool(mixed),
    "A_starves_at_56": bool(A_starves), "A56_stat": round(mA56, 4) if mA56 else None}
RES["barrier_lines"] = {
    "barrier_5": "Structural orthogonality: T is an N-only natural coordinate; the "
                 "dial predicts relation yield (difficulty), not (p,q) - no "
                 "which-factor claim made or tested.",
    "barrier_8": "Known-method-in-disguise: the measured object is the QS/CFRAC "
                 "relation-yield dial - a cost predictor FOR known methods, not a "
                 "new factoring route."}
RES["artifacts"] = [f"{WORK}/exp523_balanced_bkey.py", f"{WORK}/result.json",
                    f"{WORK}/ledger_exp523.jsonl"]
checkpoint()
ledger("verdict", verdict_name=verdict_name, H1=bool(H1), H2=bool(H2),
       mean_sp_B56=round(mB56, 4) if mB56 else None,
       mean_sp_A56=round(mA56, 4) if mA56 else None)
print(json.dumps(RES["summary"]["grid_mean_sp_T"], indent=0))
print(json.dumps(RES["verdict"]))
headline = (f"BALANCED-BKEY exp523: {verdict_name} "
            f"H1={'TRUE' if H1 else 'false'} H2={'TRUE' if H2 else 'false'} "
            f"(mean sp_B@56={mB56}, mean sp_A@56={mA56})")
with open(f"{WORK}/HEADLINE.txt", "w") as f:
    f.write(headline + "\n")
print(headline)
print("DONE", round(time.time() - T0, 1), "s")

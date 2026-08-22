#!/usr/bin/env python3
# =====================================================================
# round-51 / experiment 521 / codename T-DIAL-60-UNIF
# Fill the grid intersection: ZERO-FIT DIAL on UNIFORM draws at BITLEN 60.
#
# Dial        T(N) = sum over odd QR primes d <= 400 of 2/d,
#             QR iff N^((d-1)//2) == 1 (mod d)   [Euler criterion, gmpy2.powmod]
# Comparator  count(N) = #{odd QR primes d <= 100}
# Target      relation rate: fraction of 240 QS relation values smooth at u=2.5
#
# State of the grid entering this run (repo record, read-only):
#   balanced : 44..52 in band (~0.71-0.76); 56 -> 0.405 (paper 178);
#              60 -> 0.437 CI [0.393,0.480] PLATEAU, mean smooth rate 0.89%
#              (starved; paper 179). Uniform x 60 is the open intersection.
#   uniform  : 44 -> 0.777/0.755/0.801 (exp 517); 52 -> 0.793/0.808/0.808,
#              pooled advantage +0.121 CI [0.103,0.140] (exp 518).
#
# ================= PRE-STATED HYPOTHESES (BEFORE ANY DATA) ===================
#  H1 (band): Spearman(T, rate) stays within [0.55, 0.85] on uniform draws at
#             bitlen 60, u = 2.5.
#  H2 (edge): T beats count <= 100 by > +0.05, i.e.
#             Spearman(T, rate) - Spearman(count, rate) > +0.05.
#
# ================ DESIGN DEVIATION (PRE-STATED BEFORE DATA) ==================
#  The assigned windows p in [2^14,2^20), q in [2^20,2^26) cap bitlen(p*q) at
#  46 (max product < 2^46) and are UNSATISFIABLE jointly with the hard
#  constraint "N must be exactly 60 bits": the two clauses contradict, every
#  literal draw would be rejected, the population would be EMPTY. This is the
#  same copy-carried template defect already documented pre-data in exp 517
#  (literal [2^10,2^16)x[2^16,2^22) for a "bitlen 48" cell) and exp 518
#  (literal [2^12,2^18)x[2^18,2^24) for a "bitlen 52" cell). Unlike exp 517 we
#  cannot run a literal arm at all (empty population), so we lock ONE arm,
#  following exp 518's shape-preserving resolution adapted one rung up the
#  uniform ladder, holding the p-exponent SET identical to exp 518 so that the
#  cell bitlen (52 -> 60) is the only moved variable on the uniform line:
#      e ~ U{20..25};  p ~ uniform prime in [2^e,     2^(e+1));
#                      q ~ uniform prime in [2^(59-e), 2^(60-e));
#      reject until bitlen(p*q) == 60 exactly; label p <= q (automatic here).
#  Realized marginals ~ p in [2^20,2^26), q in [2^34,2^40); pre-rejection
#  combined span 12 octaves -- exp 518's stated SHAPE invariant preserved.
#
# ============ RELATION-RATE OPERATIONAL DEFINITION (verbatim paper-164) ======
#  sq = isqrt(N); j = 1..240; V_j = j*(2*sq + j) + (sq^2 - N)  [= (sq+j)^2-N].
#  vmed = median of the POOLED 1200x240 values; B = max(round(exp(ln vmed/u)), 50),
#  u = 2.5. Strip every prime <= B by trial division; relation := residual == 1
#  (residual 1 after stripping primes <= B implies max prime factor <= B).
#  rate(N) = (#smooth of the 240)/240.  No factor of N is ever used inside
#  measurement; oracle primes are used ONLY to construct N.
#
# ===================== VERDICT NAMES (PRE-STATED) ============================
#  H1 pass & H2 pass -> CELL-CLOSED-DIAL-HOLDS-60
#  H1 pass only      -> DIAL-HOLDS-NO-EDGE-OVER-COUNT-60
#  H2 pass only      -> BAND-BREAK-EDGE-PERSISTS-60
#  neither           -> DOUBLE-BREAK-60-UNIFORM
#
# Barriers appended as standard lines (5)/(8). Ledger mandatory (jsonl).
# Runtime budget <= 15 min. Work confined to /tmp/exp51_t60u/. Seed 20261050.
# =====================================================================
import json, math, os, time
import numpy as np
import gmpy2
from scipy.stats import spearmanr

WORK = "/tmp/exp51_t60u"
SCRIPT_PATH = os.path.join(WORK, "exp521_t_dial_60_unif.py")
RESULT_PATH = os.path.join(WORK, "result.json")
LEDGER_PATH = os.path.join(WORK, "ledger_exp521.jsonl")

EXP, CODENAME, ROUND = 521, "T-DIAL-60-UNIF", 51
SEED = 20261050
POP_N = 1200          # uniform semiprimes
NV = 240              # relation values per N (j = 1..240)
U_PAR = 2.5
BITS = 60
TPMAX, CNTMAX = 400, 100
BOOT = 300
E_LO, E_HI = 20, 25   # locked p-exponent set (see deviation block)

T0 = time.time()
state = {"experiment": EXP, "codename": CODENAME, "round": ROUND,
         "date": time.strftime("%Y-%m-%d"), "seed": SEED,
         "prestated": {
             "H1": "Spearman(T,rate) within [0.55,0.85] on uniform draws, bitlen 60, u=2.5",
             "H2": "Spearman(T,rate) - Spearman(count<=100,rate) > +0.05"},
         "design_deviation": (
             "assigned windows p in [2^14,2^20) x q in [2^20,2^26) cap bitlen(p*q)<=46, "
             "contradicting 'exactly 60 bits' (same copy-carry defect as exp517/518, "
             "documented pre-data there too; literal arm impossible here -- empty "
             "population). Locked resolution extends exp518's shape-preserving rule one "
             "rung up, holding exp518's p-exponent set fixed so bitlen is the only moved "
             f"variable: e~U{{{E_LO}..{E_HI}}}, p in [2^e,2^(e+1)), q in [2^(59-e),2^(60-e)), "
             "reject until bitlen(N)==60, p<=q.")}

def ledger(stage, note, extra=None):
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "t_s": round(time.time() - T0, 1),
           "round": ROUND, "exp": EXP, "codename": CODENAME, "stage": stage, "note": note}
    if extra:
        rec.update(extra)
    with open(LEDGER_PATH, "a") as f:
        f.write(json.dumps(rec, default=float) + "\n")
    return rec

def checkpoint():
    state["elapsed_s"] = round(time.time() - T0, 1)
    tmp = RESULT_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=1, default=float)
    os.replace(tmp, RESULT_PATH)

def sieve(n):
    s = bytearray([1]) * (n + 1)
    s[0:2] = b"\x00\x00"
    i = 2
    while i * i <= n:
        if s[i]:
            s[i*i::i] = b"\x00" * len(s[i*i::i])
        i += 1
    return [i for i in range(n + 1) if s[i]]

PRIMES_DIAL = sieve(TPMAX)                      # dial/comparator + fallback support
ODD_400 = [p for p in PRIMES_DIAL if p > 2]     # dial support
ODD_100 = [p for p in PRIMES_DIAL if 2 < p <= CNTMAX]
W400 = {p: 2.0 / p for p in ODD_400}
STRIP_PRIMES = None                             # sieved to B after vmed is known

def prime_in_range(rng, lo, hi):
    while True:
        c = rng.randrange(lo, hi) | 1
        p = int(gmpy2.next_prime(c))
        if p < hi:
            return p

def draw_uniform(rng):
    """Locked uniform-arm draw (deviation block): exact bitlen 60."""
    while True:
        e = rng.randint(E_LO, E_HI)
        p = prime_in_range(rng, 1 << e, 1 << (e + 1))
        q = prime_in_range(rng, 1 << (59 - e), 1 << (60 - e))
        N = p * q
        if N.bit_length() == BITS:
            return p, q, N

def dial_and_count(N):
    t = cnt = 0
    for p in ODD_400:
        if gmpy2.powmod(N % p, (p - 1) // 2, p) == 1:
            t += W400[p]
            if p <= CNTMAX:
                cnt += 1
    return t, cnt

def strip_and_mask(Vall, B):
    """Strip ALL primes <= B (vectorized); smooth := residual == 1."""
    global STRIP_PRIMES
    if STRIP_PRIMES is None:
        STRIP_PRIMES = sieve(B)
    W = Vall.copy()
    for p in STRIP_PRIMES:
        while True:
            m = W % p == 0
            if not m.any():
                break
            W[m] //= p
    return W == 1

def smooth_bf(v, B):
    """Brute-force reference: strip every prime <= B; True iff residual == 1.
    No early break: a residual prime <= B must still be removed."""
    for p in STRIP_PRIMES:
        while v % p == 0:
            v //= p
            if v == 1:
                return True
    return v == 1

# ------------------------------------------------------------------ STAGE 0
ledger("init", f"dial primes: {len(ODD_400)} odd <= {TPMAX} ({len(ODD_100)} odd <= "
               f"{CNTMAX}); strip support sieved to B after vmed; deviation locked "
               f"pre-data; hypotheses pre-stated")
checkpoint()

rng = np.random.default_rng(SEED)
import random
pyrng = random.Random(SEED)

# ------------------------------------------------------------------ STAGE 1
rows = []
ebins = {}
t_draw = time.time()
for idx in range(POP_N):
    p, q, N = draw_uniform(pyrng)
    rows.append({"p": p, "q": q, "N": N})
    ebins[p.bit_length() - 1] = ebins.get(p.bit_length() - 1, 0) + 1
    if (idx + 1) % 300 == 0:
        print(f"draw {idx+1}/{POP_N} elapsed={time.time()-T0:.0f}s", flush=True)

Ns = np.array([r["N"] for r in rows], dtype=object)
pbs = [r["p"].bit_length() for r in rows]
qbs = [r["q"].bit_length() for r in rows]
assert len(set(id(r["N"]) for r in rows)) == POP_N
assert min(qbs) >= max(pbs)          # p <= q labeling holds by construction
state["population"] = {
    "n": POP_N, "bits_exact": BITS, "seed": SEED,
    "mean_p_bits": round(sum(pbs) / POP_N, 2), "min_p_bits": min(pbs), "max_p_bits": max(pbs),
    "mean_q_bits": round(sum(qbs) / POP_N, 2), "min_q_bits": min(qbs), "max_q_bits": max(qbs),
    "distinct_N": len(set(int(n) for n in Ns)),
    "p_exponent_bin_counts": {str(k): v for k, v in sorted(ebins.items())}}
ledger("population", "1200 uniform semiprimes drawn, all exactly 60 bits",
       state["population"])
checkpoint()
print("population done", flush=True)

# ------------------------------------------------------------------ STAGE 2
sq = [int(gmpy2.isqrt(int(n))) for n in Ns]
js = np.arange(1, NV + 1, dtype=np.int64)
Vall = np.empty((POP_N, NV), dtype=np.int64)
for i in range(POP_N):
    Vall[i] = js * (2 * sq[i] + js) + (sq[i] * sq[i] - int(Ns[i]))
assert Vall.min() > 0

vmed = float(np.median(Vall.astype(float)))
B = max(int(round(math.exp(math.log(vmed) / U_PAR))), 50)
mask = strip_and_mask(Vall, B)
rate = mask.mean(axis=1)

Ts, Cs = [], []
for n in Ns:
    t, c = dial_and_count(int(n))
    Ts.append(t); Cs.append(c)
Ts = np.array(Ts); Cs = np.array(Cs, float)

zero_hit = int((rate == 0).sum())
state["features"] = {
    "vmed": round(vmed, 1), "B": B, "u": U_PAR,
    "mean_rate": round(float(rate.mean()), 5),
    "sd_rate": round(float(rate.std()), 5),
    "frac_zero_hit_N": round(zero_hit / POP_N, 4),
    "max_rate": round(float(rate.max()), 4),
    "smooth_total": int(mask.sum()),
    "mean_T": round(float(Ts.mean()), 4), "sd_T": round(float(Ts.std()), 4),
    "mean_count": round(float(Cs.mean()), 3)}
ledger("features", f"vmed={vmed:.1f} B={B} strip_primes={len(STRIP_PRIMES)} "
                   f"mean_rate={rate.mean():.5f} zero_hit={zero_hit}/{POP_N}",
       state["features"])
checkpoint()
print("features done", flush=True)

# ------------------------------------------------------- STAGE 2b (audit)
# Designed check: vectorized strip vs brute-force reference on a fixed
# subsample (200 values spanning the smooth/unsmooth boundary).
arng = np.random.default_rng(SEED + 424242)
aidx = arng.choice(Vall.size, size=200, replace=False)
mism = sum(int(mask.flat[i]) != int(smooth_bf(int(Vall.flat[i]), B)) for i in aidx)
state["audit_smoothness"] = {"checked": 200, "mismatches": mism,
                             "pass": bool(mism == 0)}
ledger("audit", f"vectorized-vs-bruteforce smoothness: {mism}/200 mismatches",
       state["audit_smoothness"])
checkpoint()

# ------------------------------------------------------------------ STAGE 3
spT = float(spearmanr(Ts, rate).statistic)
spC = float(spearmanr(Cs, rate).statistic)
adv = spT - spC
spTC = float(spearmanr(Ts, Cs).statistic)

def boot_ci(kind, seed_off):
    rb = np.random.default_rng(SEED + seed_off)
    vals = []
    idx = np.arange(POP_N)
    for _ in range(BOOT):
        smp = rb.choice(idx, size=POP_N, replace=True)
        if kind == "T":
            vals.append(float(spearmanr(Ts[smp], rate[smp]).statistic))
        elif kind == "C":
            vals.append(float(spearmanr(Cs[smp], rate[smp]).statistic))
        else:
            vals.append(float(spearmanr(Ts[smp], rate[smp]).statistic)
                        - float(spearmanr(Cs[smp], rate[smp]).statistic))
    vals = np.asarray(vals)
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return [round(float(lo), 4), round(float(hi), 4)]

ciT = boot_ci("T", 70001)
ciC = boot_ci("C", 80002)
ciA = boot_ci("A", 90003)

state["stats"] = {
    "spearman_T": round(spT, 4), "ci_T": ciT,
    "spearman_count": round(spC, 4), "ci_count": ciC,
    "advantage": round(adv, 4), "ci_advantage": ciA,
    "spearman_T_vs_count": round(spTC, 4), "bootstrap_resamples": BOOT}
ledger("stats", f"spT={spT:.4f} CI{ciT} spC={spC:.4f} CI{ciC} adv={adv:+.4f} CI{ciA}",
       state["stats"])
checkpoint()
print("stats done", flush=True)

# ------------------------------------------------------------------ STAGE 4
h1_pass = bool(0.55 <= spT <= 0.85)
h2_pass = bool(adv > 0.05)
if h1_pass and h2_pass:
    verdict_name = "CELL-CLOSED-DIAL-HOLDS-60"
elif h1_pass:
    verdict_name = "DIAL-HOLDS-NO-EDGE-OVER-COUNT-60"
elif h2_pass:
    verdict_name = "BAND-BREAK-EDGE-PERSISTS-60"
else:
    verdict_name = "DOUBLE-BREAK-60-UNIFORM"

state["verdict"] = {
    "H1_band_pass": h1_pass, "H2_edge_pass": h2_pass,
    "verdict_name": verdict_name,
    "context": {"balanced_56_paper178": 0.405, "balanced_60_paper179": 0.437,
                "balanced_60_count": 0.368, "uniform_52_exp518": [0.793, 0.808, 0.808],
                "uniform_48_exp517": [0.777, 0.755, 0.801]},
    "descriptive": {"distance_to_balanced60_plateau_0.437": round(abs(spT - 0.437), 4)}}
state["barriers"] = [
    "(5) WHICH-FACTOR WALL: T(N), count(N) and relation-rate(N) are symmetric functions "
    "of the composite alone -- every channel reported here is which-factor blind; nothing "
    "in this experiment reads which factor, consistent with the wall.",
    "(8) KNOWN-METHOD-IN-DISGUISE / TOY-SCOPE: the measured object is the QS relation-yield "
    "dial -- a cost predictor FOR known methods, not a new factoring route; oracle primes "
    "were used only to CONSTRUCT the semiprimes, never inside measurement; single-toy-seed "
    "at bitlen 60, no scaling claim beyond the tested regime."]
state["artifacts"] = [SCRIPT_PATH, RESULT_PATH, LEDGER_PATH]
checkpoint()
ledger("verdict", f"H1={'PASS' if h1_pass else 'FAIL'} H2={'PASS' if h2_pass else 'FAIL'} "
                  f"VERDICT={verdict_name}")
headline = (f"T-DIAL-60-UNIF exp521: H1={'TRUE' if h1_pass else 'REFUTED'} "
            f"H2={'TRUE' if h2_pass else 'REFUTED'} VERDICT={verdict_name} "
            f"spT={spT:.4f} CI{ciT} spC={spC:.4f} adv={adv:+.4f} CI{ciA} "
            f"B={B} mean_rate={rate.mean():.5f}")
with open(os.path.join(WORK, "HEADLINE.txt"), "w") as f:
    f.write(headline + "\n")
print(headline, flush=True)
print("DONE", round(time.time() - T0, 1), "s", flush=True)

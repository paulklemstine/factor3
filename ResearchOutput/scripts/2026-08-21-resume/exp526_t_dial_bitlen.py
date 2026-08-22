#!/usr/bin/env python3
# =====================================================================
# round-56 / experiment 526 / codename TDIAL-BITLEN
# Fill the grid intersection: ZERO-FIT DIAL on UNIFORM draws at EXACT BITLEN 48.
#
# Dial        T(N) = sum over odd QR primes d <= 400 of 2/d
#                   QR iff N^((d-1)//2) == 1 (mod d)   [Euler criterion, gmpy2.powmod]
# Comparator  count(N) = #{odd QR primes d <= 100}     (bare QR-count)
# Target      relation rate: fraction of 240 QS relation values smooth at u=2.5
#
# State of the grid entering this run (repo record, read-only):
#   balanced : 44..52 in band, bitlen-48 cells rho_T = 0.6916/0.7279/0.7125,
#              advantage +0.092/+0.145/+0.126 (exp 508 / paper 175);
#              56 -> 0.405 (starved; paper 178), 60 -> 0.437 plateau (paper 179).
#   uniform  : exp 517 "UNIF-48" OFFICIAL arm was the parent's literal windows
#              p in [2^10,2^16) x q in [2^16,2^22) -> N at 26..38 BITS (rho_T =
#              0.777/0.755/0.801); its scaled sensitivity arm spanned 44..52 bits.
#              So the EXACT-bitlen-48 uniform cell has never been measured.
#              exp 518 closed exact-52: rho_T = 0.793/0.808/0.808, pooled
#              advantage +0.121 CI [0.103,0.140].
# THIS RUN therefore provides the first exact-bitlen-48 uniform measurement,
# placed on the exp518/exp521 uniform ladder with the cell bitlen as the ONLY
# moved variable.
#
# ================= PRE-STATED HYPOTHESES (BEFORE ANY DATA) ===================
#  H1 (band): Spearman(T, rate) stays within [0.60, 0.85] on uniform draws at
#             bitlen 48, u = 2.5 -- ALL 3 seeds inside the band.
#  H2 (edge): T beats count <= 100 by > +0.05, i.e. mean over seeds of
#             Spearman(T,rate) - Spearman(count<=100,rate) > +0.05 AND >= 2/3
#             individual seeds show advantage > +0.05.
#
# ================ DESIGN RESOLUTION (PRE-STATED BEFORE DATA) =================
#  Parent spec gives no factor windows, only "uniform semiprimes bitlen 48".
#  Locked operationalization, extending exp518's shape-preserving rule one rung
#  DOWN the uniform line so that bitlen is the only moved variable vs exp 518:
#      e ~ U{20..25};  p ~ next_prime(uniform int in [2^e,     2^(e+1)))
#                      q ~ next_prime(uniform int in [2^(47-e), 2^(48-e)))
#      reject octave overflow after next_prime, p == q, and bitlen(N) != 48;
#      label p <= q.
#  Pre-rejection product span [2^47, 2^49); realized marginals p in [2^20,2^26),
#  q in [2^22,2^28) -- combined span 12 octaves, exp518/521 shape preserved.
#  Relation-rate features VERBATIM paper-164 (as implemented in exp508/exp521):
#    sq = isqrt(N); j = 1..240; V_j = j*(2*sq + j) + (sq^2 - N) [= (sq+j)^2-N];
#    vmed = median of the POOLED 1200x240 values per population;
#    B = max(round(exp(ln(vmed)/u)), 50), u = 2.5;
#    strip every prime <= B by trial division (vectorized);
#    relation := residual == 1; rate(N) = (#smooth)/240.
#  No factor of N is ever used inside measurement; oracle primes construct N only.
#  Smoothness audit: vectorized strip cross-checked against a brute-force
#  reference on 200 random values per seed cell (designed check).
#
# ===================== VERDICT NAMES (PRE-STATED) ============================
#  H1 pass & H2 pass -> CELL-CLOSED-DIAL-HOLDS-UNIF-48
#  H1 pass only      -> DIAL-HOLDS-NO-EDGE-OVER-COUNT-48
#  H2 pass only      -> BAND-BREAK-EDGE-PERSISTS-48
#  neither           -> DOUBLE-BREAK-48-UNIFORM
#
# Barriers appended as standard lines (5)/(8). Ledger mandatory (jsonl).
# Runtime budget <= 12 min. Work confined to /tmp/exp56_tbl/. Seeds 20261110-12.
# =====================================================================
import json, math, os, time
import numpy as np
import gmpy2
from scipy.stats import spearmanr

WORK = "/tmp/exp56_tbl"
SCRIPT_PATH = os.path.join(WORK, "exp526_t_dial_bitlen.py")
RESULT_PATH = os.path.join(WORK, "result.json")
LEDGER_PATH = os.path.join(WORK, "ledger_exp526.jsonl")

EXP, CODENAME, ROUND = 526, "TDIAL-BITLEN", 56
SEEDS = [20261110, 20261111, 20261112]
POP_N = 1200          # uniform semiprimes per seed
NV = 240              # relation values per N (j = 1..240)
U_PAR = 2.5
BITS = 48
TPMAX, CNTMAX = 400, 100
BOOT = 300
E_LO, E_HI_EXCL = 20, 26   # e ~ U{20..25}, locked p-exponent set of exp518/521

T0 = time.time()
state = {
    "experiment": EXP, "codename": CODENAME, "round": ROUND,
    "date": time.strftime("%Y-%m-%d"), "seeds": SEEDS,
    "prestated": {
        "H1": "Spearman(T,rate) within [0.60,0.85] on uniform draws at bitlen 48, "
              "u=2.5, ALL 3 seeds",
        "H2": "mean advantage Spearman(T)-Spearman(count<=100) > +0.05 and >= 2/3 "
              "individual seeds > +0.05"},
    "design_resolution": (
        "parent gave no factor windows; locked ladder-shape operationalization "
        f"e~U{{{E_LO}..{E_HI_EXCL-1}}}, p~nextprime(U[2^e,2^(e+1))), "
        f"q~nextprime(U[2^(47-e),2^(48-e))), reject overflow/p==q/bitlen!=48, "
        "p<=q labeled; extends exp518 one rung down, bitlen the only moved variable; "
        "note exp517's official 'unif-48' arm actually measured N at 26..38 bits"),
    "verdict_names": {
        "both": "CELL-CLOSED-DIAL-HOLDS-UNIF-48",
        "h1_only": "DIAL-HOLDS-NO-EDGE-OVER-COUNT-48",
        "h2_only": "BAND-BREAK-EDGE-PERSISTS-48",
        "neither": "DOUBLE-BREAK-48-UNIFORM"},
}

def log(*a):
    print(f"[{time.strftime('%H:%M:%S')}]", *a, flush=True)

def ledger(stage, note, extra=None):
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "t_s": round(time.time() - T0, 1),
           "round": ROUND, "exp": EXP, "codename": CODENAME, "stage": stage,
           "note": note}
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

# ---------------------------------------------------------------- primes
def sieve(n):
    m = np.ones(n + 1, dtype=bool); m[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if m[i]:
            m[i * i::i] = False
    return [int(i) for i in np.nonzero(m)[0]]

ODD_400 = [p for p in sieve(TPMAX) if p > 2]           # dial support
ODD_100 = [p for p in ODD_400 if p <= CNTMAX]          # comparator support
W400 = {p: 2.0 / p for p in ODD_400}
STRIP_PRIMES = None                                    # sieved to B once vmed known

# ---------------------------------------------------------------- population
def draw_uniform(rng):
    """Locked ladder-shape draw (design resolution): exact bitlen 48."""
    while True:
        e = int(rng.integers(E_LO, E_HI_EXCL))
        eq = (BITS - 1) - e
        pc = int(rng.integers(1 << e, 2 << e))
        qc = int(rng.integers(1 << eq, 2 << eq))
        p = int(gmpy2.next_prime(pc)); q = int(gmpy2.next_prime(qc))
        if p >= (2 << e) or q >= (2 << eq):            # octave overflow after next_prime
            continue
        if p == q:
            continue
        N = p * q
        if N.bit_length() != BITS:
            continue
        if p > q:
            p, q = q, p
        return p, q, N

# ---------------------------------------------------------------- features
def dial_and_count(N):
    t = c = 0
    for pr in ODD_400:
        if gmpy2.powmod(N % pr, (pr - 1) // 2, pr) == 1:
            t += W400[pr]
            if pr <= CNTMAX:
                c += 1
    return t, c

def strip_and_mask(Vall, B):
    """Strip ALL primes <= B (vectorized); smooth := residual == 1."""
    global STRIP_PRIMES
    if STRIP_PRIMES is None:
        STRIP_PRIMES = sieve(int(math.ceil(B)) + 1)
    W = Vall.copy()
    for pr in STRIP_PRIMES:
        while True:
            m = W % pr == 0
            if not m.any():
                break
            W[m] //= pr
    return W == 1

def smooth_bf(v, B):
    """Brute-force reference: strip every prime <= B ascending; residual==1."""
    for pr in STRIP_PRIMES:
        while v % pr == 0:
            v //= pr
            if v == 1:
                return True
    return v == 1

def boot_ci(kind, seed, Ts, Cs, rate, seed_off):
    rb = np.random.default_rng(seed + seed_off)
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
    lo, hi = np.percentile(np.asarray(vals), [2.5, 97.5])
    return [round(float(lo), 4), round(float(hi), 4)]

# ================================================================== STAGE 0
ledger("init", f"dial primes {len(ODD_400)} odd<={TPMAX}, comparator {len(ODD_100)} "
               f"odd<={CNTMAX}; hypotheses pre-stated; design resolution locked pre-data")
checkpoint()

rows = []

for seed in SEEDS:
    seed_key = seed
    # ---------------------------------------------------------- STAGE 1: draw
    t_draw = time.time()
    rng = np.random.default_rng(seed)
    pops = [draw_uniform(rng) for _ in range(POP_N)]
    assert len(set(n for _, _, n in pops)) == POP_N
    assert all(pq[0] <= pq[1] for pq in [(a, b) for a, b, _ in pops])
    Ns_obj = [n for _, _, n in pops]
    pbs = [p.bit_length() for p, _, _ in pops]
    qbs = [q.bit_length() for _, q, _ in pops]
    ebins = {}
    for p, _, _ in pops:
        ebins[p.bit_length() - 1] = ebins.get(p.bit_length() - 1, 0) + 1
    pop_info = {
        "seed": seed, "n": POP_N, "bits_exact": BITS,
        "mean_p_bits": round(sum(pbs) / POP_N, 2),
        "min_p_bits": min(pbs), "max_p_bits": max(pbs),
        "mean_q_bits": round(sum(qbs) / POP_N, 2),
        "min_q_bits": min(qbs), "max_q_bits": max(qbs),
        "distinct_N": len(set(Ns_obj)),
        "p_exponent_bin_counts": {str(k): v for k, v in sorted(ebins.items())},
        "draw_s": round(time.time() - t_draw, 1)}
    state.setdefault("populations", []).append(pop_info)
    ledger("population", f"seed={seed}: 1200 uniform semiprimes, all exactly 48 bits",
           pop_info)
    checkpoint()
    log(f"seed {seed} population done ({pop_info['draw_s']}s)")

    # --------------------------------------------- STAGE 2: relation features
    sqs = [int(gmpy2.isqrt(n)) for n in Ns_obj]
    js = np.arange(1, NV + 1, dtype=np.int64)
    Vall = np.empty((POP_N, NV), dtype=np.int64)
    for i in range(POP_N):
        Vall[i] = js * (2 * sqs[i] + js) + (sqs[i] * sqs[i] - Ns_obj[i])
    assert Vall.min() > 0

    vmed = float(np.median(Vall.astype(float)))
    B = max(int(round(math.exp(math.log(vmed) / U_PAR))), 50)
    mask = strip_and_mask(Vall, B)
    rate = mask.mean(axis=1)

    Ts = np.empty(POP_N); Cs = np.empty(POP_N)
    for i, n in enumerate(Ns_obj):
        t, c = dial_and_count(n)
        Ts[i] = t; Cs[i] = c

    zero_hit = int((rate == 0).sum())
    feat_info = {
        "vmed": round(vmed, 1), "B": B, "u": U_PAR,
        "strip_primes": len(STRIP_PRIMES),
        "mean_rate": round(float(rate.mean()), 5),
        "sd_rate": round(float(rate.std()), 5),
        "frac_zero_hit_N": round(zero_hit / POP_N, 4),
        "max_rate": round(float(rate.max()), 4),
        "smooth_total": int(mask.sum()),
        "mean_T": round(float(Ts.mean()), 4), "sd_T": round(float(Ts.std()), 4),
        "mean_count": round(float(Cs.mean()), 3)}
    ledger("features", f"seed={seed}: vmed={vmed:.1f} B={B} mean_rate="
                       f"{rate.mean():.5f} zero_hit={zero_hit}/{POP_N}", feat_info)

    # ------------------------------------------------------- STAGE 2b: audit
    arng = np.random.default_rng(seed + 424242)
    aidx = arng.choice(Vall.size, size=200, replace=False)
    mism = sum(int(mask.flat[i]) != int(smooth_bf(int(Vall.flat[i]), B))
               for i in aidx)
    audit = {"checked": 200, "mismatches": mism, "pass": bool(mism == 0)}
    ledger("audit", f"seed={seed}: vectorized-vs-bruteforce {mism}/200 mismatches",
           audit)
    checkpoint()

    # ---------------------------------------------------- STAGE 3: statistics
    spT = float(spearmanr(Ts, rate).statistic)
    spC = float(spearmanr(Cs, rate).statistic)
    adv = spT - spC
    spTC = float(spearmanr(Ts, Cs).statistic)
    ciT = boot_ci("T", seed, Ts, Cs, rate, 70001)
    ciC = boot_ci("C", seed, Ts, Cs, rate, 80002)
    ciA = boot_ci("A", seed, Ts, Cs, rate, 90003)
    row = {"seed": seed, "spearman_T": round(spT, 4), "ci_T": ciT,
           "spearman_count": round(spC, 4), "ci_count": ciC,
           "advantage": round(adv, 4), "ci_advantage": ciA,
           "spearman_T_vs_count": round(spTC, 4),
           "B": B, "mean_rate": round(float(rate.mean()), 5),
           "audit_mismatches": mism}
    rows.append(row)
    state["rows"] = rows
    ledger("stats", f"seed={seed}: spT={spT:.4f} CI{ciT} spC={spC:.4f} CI{ciC} "
                    f"adv={adv:+.4f} CI{ciA}", row)
    checkpoint()
    log(f"seed {seed} stats done: sT={spT:.4f} sC={spC:.4f} adv={adv:+.4f}")

# ================================================================== STAGE 4
spTs = [r["spearman_T"] for r in rows]
advs = [r["advantage"] for r in rows]
summary = {
    "mean_T": round(sum(spTs) / len(spTs), 4),
    "min_T": min(spTs), "max_T": max(spTs),
    "per_seed_T": spTs,
    "mean_advantage": round(sum(advs) / len(advs), 4),
    "min_advantage": min(advs), "max_advantage": max(advs),
    "wins_gt_0.05": int(sum(a > 0.05 for a in advs)),
    "mean_rate_over_seeds": round(sum(r["mean_rate"] for r in rows) / len(rows), 5)}

h1_pass = bool(all(0.60 <= s <= 0.85 for s in spTs))
h2_pass = bool(summary["mean_advantage"] > 0.05 and summary["wins_gt_0.05"] >= 2)
if h1_pass and h2_pass:
    verdict_name = "CELL-CLOSED-DIAL-HOLDS-UNIF-48"
elif h1_pass:
    verdict_name = "DIAL-HOLDS-NO-EDGE-OVER-COUNT-48"
elif h2_pass:
    verdict_name = "BAND-BREAK-EDGE-PERSISTS-48"
else:
    verdict_name = "DOUBLE-BREAK-48-UNIFORM"

state["summary"] = summary
state["verdict"] = {
    "H1_band_all_seeds_pass": h1_pass, "H2_edge_pass": h2_pass,
    "verdict_name": verdict_name,
    "context": {
        "balanced_48_exp508_rhoT": [0.6916, 0.7279, 0.7125],
        "balanced_56_paper178_rhoT": 0.405,
        "balanced_60_paper179_rhoT": 0.437,
        "uniform_52_exp518_rhoT": [0.793, 0.808, 0.808],
        "exp517_official_armA_note": "measured N at 26..38 bits, not 48",
        "descriptive_dist_to_balanced48_mean_0.7107":
            round(abs(summary["mean_T"] - 0.7107), 4)}}
state["barriers"] = [
    "(5) WHICH-FACTOR WALL / STRUCTURAL ORTHOGONALITY: T(N), count(N) and "
    "relation-rate(N) are symmetric functions of the composite alone -- every "
    "channel reported here is which-factor blind; nothing reads which factor, "
    "consistent with the wall.",
    "(8) KNOWN-METHOD-IN-DISGUISE / TOY-SCOPE: the measured object is the QS "
    "relation-yield dial -- a cost predictor FOR known methods, not a new factoring "
    "route; oracle primes were used only to CONSTRUCT the semiprimes, never inside "
    "measurement; three-toy-seed at bitlen 48, no scaling claim beyond the tested regime."]
state["artifacts"] = [SCRIPT_PATH, RESULT_PATH, LEDGER_PATH,
                      os.path.join(WORK, "HEADLINE.txt")]
checkpoint()
ledger("verdict", f"H1={'PASS' if h1_pass else 'FAIL'} "
                  f"H2={'PASS' if h2_pass else 'FAIL'} VERDICT={verdict_name}",
       {"H1": h1_pass, "H2": h2_pass, "verdict_name": verdict_name})

headline = (f"TDIAL-BITLEN exp526: H1={'TRUE' if h1_pass else 'REFUTED'} "
            f"H2={'TRUE' if h2_pass else 'REFUTED'} VERDICT={verdict_name} "
            f"T per seed {spTs} mean {summary['mean_T']}; "
            f"advantage per seed {[round(a,4) for a in advs]} mean "
            f"{summary['mean_advantage']}; B={[r['B'] for r in rows]}; "
            f"mean_rate={summary['mean_rate_over_seeds']}")
with open(os.path.join(WORK, "HEADLINE.txt"), "w") as f:
    f.write(headline + "\n")
log(headline)
log("DONE", round(time.time() - T0, 1), "s")

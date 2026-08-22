#!/usr/bin/env python3
"""EXP 508 T-DIAL-BITLEN lean (round-47). Seeds 20261010..12 per bitlen.
Paper 164/165/166: zero-fit dial T(N) = sum(2/p | QR primes p<=400) predicts per-N
relation yield at Spearman ~0.73 at bitlen 44, balanced draws, u=2.5, seed-stable
(paper 165 band [0.71,0.76]) and regime/u invariant (paper 166).
OPEN QUESTION: does the dial hold at HIGHER bitlens (48, 52)?

PRE-STATED HYPOTHESES (written BEFORE any data was generated):
  H1 (band):  Spearman(T, rate) stays within [0.60, 0.85] at bitlen 48 AND bitlen 52
              at u=2.5 balanced draws -- ALL 3 seeds per bitlen inside the band.
  H2 (advantage): the dial beats the bare QR-count comparator at BOTH higher
              bitlens: per bitlen b in {48,52}, mean_b(Spearman T) - mean_b(Spearman
              count<=100) > +0.05 AND >= 2/3 individual seeds show advantage > +0.05.
  H3 (graceful degradation): across bitlen means m44 -> m48 -> m52,
              (a) monotone non-increasing, (b) total drop m44 - m52 <= 0.15,
              (c) no adjacent-bitlen drop > 0.10.  A CLIFF is any adjacent drop
              > 0.15 or total drop > 0.20.

DESIGN: 3 bitlens x 3 seeds x 1200 balanced semiprimes; N forced to exact bitlen
L in {44, 48, 52} via the exp499 shifted window of the exp497 construction
(factors drawn in [isqrt(2^(L-1))+1, isqrt(2^L - 1)], nextprime, inter-prime gap
uniform in [1, 1e5), stray rejects redrawn).
Feature construction VERBATIM paper-164/exp497: sq = isqrt(N); js = arange(1, 241);
V = js*(2*sq+js) + (sq*sq - N)  (= (sq+j)^2 - N, Fermat offset family);
rate(N) = fraction of the 240 offsets that are B-smooth (strip primes <= B);
vmed pooled over the population's 1200x240 values; B(u) = max(round(exp(ln vmed/u)), 50),
u = 2.5.
T(N) = sum(2.0/q for q in primerange(3, 401) if Legendre(N mod q, q) == +1)
       (gmpy2.powmod Euler criterion);
comparator C(N) = QR-indicator COUNT over primerange(3, 101).
CIs: bootstrap 300 resamples per cell, percentile [2.5, 97.5].

# BARRIERS (standard lines):
#   Barrier 5 (structural orthogonality): T is an N-only natural coordinate; the
#   dial predicts relation yield (difficulty), not (p,q) - no which-factor claim
#   made or tested.
#   Barrier 8 (known-method-in-disguise): the measured object is the QS/CFRAC
#   relation-yield dial - a cost predictor FOR known methods, not a new
#   factoring route.
"""
import json, time, math, datetime
import numpy as np
import gmpy2
from sympy import primerange, nextprime

BASE_SEEDS = [20261010, 20261011, 20261012]
BITLENS = [44, 48, 52]
T0 = time.time()
WORK = "/tmp/exp47_tblen"
OUT = {"meta": {"base_seeds": BASE_SEEDS, "bitlens": BITLENS, "exp": 508,
                "codename": "T-DIAL-BITLEN", "round": 47,
                "n_semiprimes_per_cell": 1200, "offsets_per_relation": 240,
                "u": 2.5, "bootstrap_resamples": 300,
                "prestated": {
                    "H1": "Spearman(T,rate) in [0.60,0.85] at bitlen 48 AND 52, all 3 seeds each",
                    "H2": "mean(T)-mean(count) > +0.05 at bitlen 48 and 52, >=2/3 seeds each",
                    "H3": "monotone mild decline: total drop <=0.15, adjacent drop <=0.10"}},
        "rows": []}

def ledger(event, **kw):
    rec = {"ts": datetime.datetime.now().isoformat(timespec="seconds"),
           "round": 47, "exp": 508, "codename": "T-DIAL-BITLEN",
           "event": event, "t_s": round(time.time() - T0, 1)}
    rec.update(kw)
    with open(f"{WORK}/ledger_exp508.jsonl", "a") as f:
        f.write(json.dumps(rec, default=float) + "\n")
    return rec

def checkpoint():
    json.dump(OUT, open(f"{WORK}/result.json", "w"), indent=1, default=float)

primes_all = np.array(list(primerange(2, 200000)), dtype=np.int64)

def smooth_mask(V, B):
    # verbatim exp497
    W = V.copy()
    for p in primes_all[primes_all <= B]:
        while True:
            m = W % p == 0
            if not m.any(): break
            W[m] //= p
            if not (W % p == 0).any(): break
    return W == 1

def spearman(a, b):
    # verbatim exp497
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])

def draw_balanced(rng, L):
    """exp497 construction (exp499 window shift), N exact bitlen L."""
    lo = int(gmpy2.isqrt(1 << (L - 1))) + 1
    hi = int(gmpy2.isqrt((1 << L) - 1))
    while True:
        r = int(rng.integers(lo, hi))
        p = int(nextprime(r)); q = int(nextprime(p + int(rng.integers(1, 10**5))))
        N = p * q
        if not ((1 << (L - 1)) <= N < (1 << L)):
            continue
        sq = math.isqrt(N)
        js = np.arange(1, 241, dtype=np.int64)
        V = js * (2 * sq + js) + (sq * sq - N)
        if V.min() <= 0: continue
        return N, sq, V

wr = list(primerange(3, 401))          # T-dial support, odd primes <= 400
cnt_primes = list(primerange(3, 101))  # comparator support, odd primes <= 100

def t_dial(Ns):
    return np.array([sum(2.0/q for q in wr
                         if gmpy2.powmod(N % q, (q - 1) // 2, q) == 1)
                     for N in Ns], float)

def qr_count(Ns):
    return np.array([sum(1 for q in cnt_primes
                         if gmpy2.powmod(N % q, (q - 1) // 2, q) == 1)
                     for N in Ns], float)

def boot_ci(x, y, n_boot=300, seed=12345):
    rngb = np.random.default_rng(seed)
    n = len(x); vals = []
    for _ in range(n_boot):
        idx = rngb.integers(0, n, n)
        vals.append(spearman(np.asarray(x)[idx], np.asarray(y)[idx]))
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]

ledger("start", base_seeds=BASE_SEEDS, bitlens=BITLENS, workdir=WORK)
checkpoint()

for L in BITLENS:
    for k, seed in enumerate(BASE_SEEDS):
        rng = np.random.default_rng(seed)
        t_draw = time.time()
        data = [draw_balanced(rng, L) for _ in range(1200)]
        Ns = [d[0] for d in data]
        Vall = np.concatenate([d[2] for d in data])
        vmed = float(np.median(Vall.astype(float)))
        B = max(int(round(math.exp(math.log(vmed) / 2.5))), 50)
        sm = smooth_mask(Vall, B).reshape(len(data), 240)
        rate = sm.mean(axis=1)
        Ts = t_dial(Ns)
        Cs = qr_count(Ns)
        sT = spearman(Ts, rate)
        sC = spearman(Cs, rate)
        ciT = boot_ci(Ts, rate, 300, seed=seed + 70000 * L)
        ciC = boot_ci(Cs, rate, 300, seed=seed + 80000 * L)
        row = {"bitlen": L, "seed": seed, "R2_base_seed": seed,
               "spearman_T": round(sT, 4), "ci_T": [round(ciT[0], 4), round(ciT[1], 4)],
               "spearman_count": round(sC, 4), "ci_count": [round(ciC[0], 4), round(ciC[1], 4)],
               "advantage": round(sT - sC, 4),
               "vmed": round(vmed, 1), "B": B,
               "mean_rate": round(float(rate.mean()), 5),
               "draw_s": round(time.time() - t_draw, 1)}
        OUT["rows"].append(row)
        checkpoint()
        ledger("cell_done", bitlen=L, seed=seed, spearman_T=row["spearman_T"],
               spearman_count=row["spearman_count"], advantage=row["advantage"],
               B=B, mean_rate=row["mean_rate"])
        print(f"bitlen={L} seed={seed} sT={sT:.4f} sC={sC:.4f} adv={sT-sC:+.4f} "
              f"B={B} rate={rate.mean():.4f} [{row['draw_s']}s]", flush=True)

# ---- summary + verdicts ----
import collections
by_bl = collections.defaultdict(list)
for r in OUT["rows"]:
    by_bl[r["bitlen"]].append(r)
means = {L: {"mean_T": sum(r["spearman_T"] for r in by_bl[L]) / len(by_bl[L]),
             "mean_C": sum(r["spearman_count"] for r in by_bl[L]) / len(by_bl[L]),
             "min_T": min(r["spearman_T"] for r in by_bl[L]),
             "max_T": max(r["spearman_T"] for r in by_bl[L]),
             "mean_adv": sum(r["advantage"] for r in by_bl[L]) / len(by_bl[L])}
         for L in BITLENS}
for L in BITLENS:
    means[L]["mean_adv"] = means[L]["mean_T"] - means[L]["mean_C"]
    means[L] = {kk: round(vv, 4) for kk, vv in means[L].items()}

# H1: all 3 seeds in band at bitlen 48 AND bitlen 52
inband = lambda s: 0.60 <= s <= 0.85
h1_cells = {L: [inband(r["spearman_T"]) for r in by_bl[L]] for L in (48, 52)}
H1 = all(all(v) for v in h1_cells.values())

# H2: mean advantage > +0.05 at both bitlens, >=2/3 seeds with adv > +0.05 each
h2_detail = {}
for L in (48, 52):
    wins = sum(1 for r in by_bl[L] if r["advantage"] > 0.05)
    h2_detail[L] = {"mean_adv": means[L]["mean_adv"], "wins_gt_0.05": wins}
H2 = all(h2_detail[L]["mean_adv"] > 0.05 and h2_detail[L]["wins_gt_0.05"] >= 2
         for L in (48, 52))

# H3: monotone mild decline, no cliff
drops_adj = [means[BITLENS[i]]["mean_T"] - means[BITLENS[i+1]]["mean_T"]
             for i in range(len(BITLENS) - 1)]
total_drop = means[44]["mean_T"] - means[52]["mean_T"]
monotone = all(d >= -1e-9 for d in drops_adj)
H3_graceful = bool(monotone and total_drop <= 0.15 and max(drops_adj) <= 0.10)
CLIFF = bool(any(d > 0.15 for d in drops_adj) or total_drop > 0.20)

OUT["summary"] = {"by_bitlen": means,
                  "adjacent_drops": [round(d, 4) for d in drops_adj],
                  "total_drop_44_to_52": round(total_drop, 4),
                  "monotone": bool(monotone)}
OUT["verdict"] = {
    "H1_band_48_and_52_all_seeds": bool(H1),
    "H2_advantage_at_higher_bitlens": bool(H2),
    "H3_graceful_monotone_mild_decline": H3_graceful,
    "H3_cliff": CLIFF,
    "h1_cells_in_band": {str(L): sum(v) for L, v in h1_cells.items()},
    "h2_detail": h2_detail}
OUT["barrier_lines"] = {
    "barrier_5": "Structural orthogonality: T is an N-only natural coordinate; the "
                 "dial predicts relation yield (difficulty), not (p,q) - no "
                 "which-factor claim made or tested.",
    "barrier_8": "Known-method-in-disguise: the measured object is the QS/CFRAC "
                 "relation-yield dial - a cost predictor FOR known methods, not a "
                 "new factoring route."}
OUT["artifacts"] = [f"{WORK}/exp508_t_dial_bitlen.py", f"{WORK}/result.json",
                    f"{WORK}/ledger_exp508.jsonl"]
checkpoint()
ledger("verdict", H1=bool(H1), H2=bool(H2), H3_graceful=H3_graceful, cliff=CLIFF,
       **{f"mean_T_{L}": means[L]["mean_T"] for L in BITLENS})
print(json.dumps(OUT["summary"]))
print(json.dumps(OUT["verdict"]))
headline = (f"T-DIAL-BITLEN exp508: H1={'TRUE' if H1 else 'REFUTED'} "
            f"H2={'TRUE' if H2 else 'REFUTED'} "
            f"H3={'GRACEFUL' if H3_graceful else ('CLIFF' if CLIFF else 'NONMONOTONE')} "
            f"(mean T: " + ", ".join(f"{L}:{means[L]['mean_T']}" for L in BITLENS) + ")")
print(headline)
with open(f"{WORK}/HEADLINE.txt", "w") as f:
    f.write(headline + "\n")
print("DONE", round(time.time() - T0, 1), "s")

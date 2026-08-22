#!/usr/bin/env python3
"""
round-53 / experiment 518 / codename T-DIAL-UNIF-52
Fill the last empty cell of the zero-fit dial grid: UNIFORM draws at BITLEN 52.

Dial          T(N) = sum over odd QR primes d <= 400 of 2/d,
              where d is a QR prime for N iff N^((d-1)//2) == 1 (mod d)
              [Euler criterion via gmpy2.powmod]
Baseline      count(N) = #{odd QR primes d <= 100}
Target        relation rate: fraction of 240 QS relation values smooth at u = 2.5

======================== PRE-STATED HYPOTHESES (BEFORE DATA) =========================
H1: Spearman(T, rate) on uniform draws at bitlen 52 stays within [0.55, 0.85] at u=2.5.
    Pre-stated decision rule: primary statistic = Spearman pooled over the 3 seeds
    (3600 Ns); PASS iff the pooled estimate lies in [0.55, 0.85]; per-seed spread
    reported alongside.
H2: T beats count<=100 by > +0.05, i.e.
    pooled Spearman(T, rate) - pooled Spearman(count, rate) > +0.05.

===================== DESIGN DEVIATION (PRE-STATED BEFORE DATA) ======================
The assigned windows p in [2^12,2^18), q in [2^18,2^24) cap bitlen(p*q) at 42
(max product < 2^18 * 2^24 = 2^42) and are UNSATISFIABLE jointly with the hard
constraint "N must be exactly 52 bits". We preserve the windows' SHAPE -- a
12-octave combined span with the q/p exponent gap uniform in (0,12), q the larger
factor -- while enforcing bitlen(N) == 52 exactly:
    e uniform in {20..25};  p ~ uniform prime in [2^e,   2^(e+1));
                            q ~ uniform prime in [2^(51-e), 2^(52-e));
    reject until bitlen(p*q) == 52; label so that p <= q.
Marginals realised: p in [2^20,2^26), q in [2^25,2^32), exponent gap in {1..11}.

=================== RELATION-RATE OPERATIONAL DEFINITION (PRE-STATED) ================
For j = 1..240:  v_j = (isqrt(N)+j)^2 - N   (standard QS polynomial, window start).
Strip every prime d <= 400 by trial division (only QR primes can divide Q(x);
non-QR primes never hit). Relation := residual cofactor c == 1 OR c <= B, with
B = floor(N^(1/u)), u = 2.5. Composite residuals above B score NOT smooth even when
further splittable -- conservative and N-independent, hence unbiased for ranks.

Verdict names (pre-stated):
  H1 pass & H2 pass   -> CELL-CLOSED-DIAL-HOLDS
  H1 pass only        -> DIAL-HOLDS-NO-EDGE-OVER-COUNT
  H2 pass only        -> BAND-BREAK-EDGE-PERSISTS
  neither             -> DOUBLE-BREAK-52-UNIFORM
"""
import json
import math
import os
import time

import numpy as np

try:
    import gmpy2
    HAVE_GMPY = True
except Exception:
    HAVE_GMPY = False

WORK = "/tmp/exp53_tu52"
SCRIPT_PATH = os.path.join(WORK, "exp518_t_dial_unif_52.py")
RESULT_PATH = os.path.join(WORK, "result.json")
LEDGER_PATH = os.path.join(WORK, "ledger.jsonl")

EXP = 518
CODENAME = "T-DIAL-UNIF-52"
ROUND = 53
SEEDS = [20261090, 20261091, 20261092]
POP_N = 1200          # semiprimes per seed
N_VALS = 240          # relation values per N
U_PAR = 2.5           # smoothness parameter
BITS = 52
BOOT = 300            # bootstrap resamples


# ---------------------------------------------------------------- utilities
def log(msg):
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def ledger(stage, note, extra=None):
    rec = {"ts": time.time(), "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "exp": EXP, "codename": CODENAME, "stage": stage, "note": note}
    if extra:
        rec.update(extra)
    with open(LEDGER_PATH, "a") as fh:
        fh.write(json.dumps(rec) + "\n")


def checkpoint(state):
    tmp = RESULT_PATH + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(state, fh, indent=1)
    os.replace(tmp, RESULT_PATH)


def primes_upto(n):
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    return [int(i) for i in np.nonzero(sieve)[0]]


PR400 = primes_upto(400)                      # includes 2 (used for stripping)
PR400_ODD = [p for p in PR400 if p > 2]       # dial support (odd QR primes <= 400)
PR100_ODD = [p for p in PR400_ODD if p <= 100]

_MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)  # deterministic < 3.3e24


def is_prime_int(n):
    if n < 2:
        return False
    if HAVE_GMPY:
        return bool(gmpy2.is_prime(n))
    for p in _MR_BASES:
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in _MR_BASES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def next_prime_int(n):
    if HAVE_GMPY:
        return int(gmpy2.next_prime(n))
    m = n + 1 if n % 2 == 0 else n + 2
    while not is_prime_int(m):
        m += 2
    return m


def euler_symbol_one(N, d):
    """1 iff N is a quadratic residue mod prime d (and d does not divide N)."""
    if HAVE_GMPY:
        return int(gmpy2.powmod(N, (d - 1) // 2, d))
    return pow(N, (d - 1) // 2, d)


def fifth_root_floor(n):
    """floor(n^(1/5)) exact."""
    if n <= 0:
        return 0
    x = int(round(n ** 0.2))
    while x ** 5 > n:
        x -= 1
    while (x + 1) ** 5 <= n:
        x += 1
    return x


# ---------------------------------------------------------------- features
def dial_features(N):
    """T(N) = sum 2/d over odd QR primes d<=400; count = #odd QR primes d<=100."""
    T = 0.0
    cnt = 0
    for d in PR400_ODD:
        if euler_symbol_one(N, d) == 1:
            w = 2.0 / d
            T += w
            if d <= 100:
                cnt += 1
    return T, cnt


def relation_rate(N):
    """Fraction of 240 QS values v_j = (isqrt(N)+j)^2 - N smooth at u=2.5."""
    B = fifth_root_floor(int(N) * int(N))       # B = floor(N^(2/5)) = floor(N^(1/2.5))
    f0 = math.isqrt(int(N))
    s = 0
    for j in range(1, N_VALS + 1):
        base = f0 + j
        v = base * base - N
        if v <= 1:
            s += 1
            continue
        for d in PR400:
            if v % d == 0:
                while v % d == 0:
                    v //= d
                if v == 1:
                    break
        if v == 1 or v <= B:
            s += 1
    return s / float(N_VALS)


def gen_one(rng):
    """Uniform-draw 52-bit semiprime preserving the assigned window shape."""
    while True:
        e = int(rng.integers(20, 26))
        eq = 51 - e
        pc = int(rng.integers(1 << e, 2 << e))
        qc = int(rng.integers(1 << eq, 2 << eq))
        p = next_prime_int(pc)
        q = next_prime_int(qc)
        if p >= (2 << e) or q >= (2 << eq):     # octave overflow after next_prime
            continue
        if p == q:
            continue
        N = p * q
        if N.bit_length() != BITS:
            continue
        if p > q:
            p, q = q, p
        return p, q, N


# ---------------------------------------------------------------- statistics
def avg_ranks(x):
    x = np.asarray(x, dtype=float)
    order = np.argsort(x, kind="mergesort")
    sx = x[order]
    r = np.empty(len(x), dtype=float)
    i = 0
    n = len(x)
    while i < n:
        j = i
        while j + 1 < n and sx[j + 1] == sx[i]:
            j += 1
        r[order[i:j + 1]] = 0.5 * (i + j) + 1.0
        i = j + 1
    return r


def spearman(x, y):
    rx, ry = avg_ranks(x), avg_ranks(y)
    vx, vy = rx - rx.mean(), ry - ry.mean()
    den = math.sqrt(float((vx * vx).sum()) * float((vy * vy).sum()))
    if den == 0.0:
        return float("nan")
    return float((vx * vy).sum() / den)


def boot_ci(aT, aC, aR, seed=987654321):
    rng = np.random.default_rng(seed)
    n = len(aR)
    bT, bC, bA = [], [], []
    rT, rC = avg_ranks(aT), avg_ranks(aC)
    rR = avg_ranks(aR)

    def sp(rx, ry):
        vx, vy = rx - rx.mean(), ry - ry.mean()
        den = math.sqrt(float((vx * vx).sum()) * float((vy * vy).sum()))
        return float("nan") if den == 0.0 else float((vx * vy).sum() / den)

    for _ in range(BOOT):
        idx = rng.integers(0, n, n)
        sT = sp(rT[idx], rR[idx])
        sC = sp(rC[idx], rR[idx])
        bT.append(sT)
        bC.append(sC)
        bA.append(sT - sC)

    def ci(a):
        return [round(float(np.percentile(a, 2.5)), 4),
                round(float(np.percentile(a, 97.5)), 4)]

    return {"spm_T_ci95": ci(bT), "spm_count_ci95": ci(bC), "advantage_ci95": ci(bA)}


def block(T, C, R):
    sT = spearman(T, R)
    sC = spearman(C, R)
    out = {
        "spm_T": round(sT, 4),
        "spm_count": round(sC, 4),
        "advantage": round(sT - sC, 4),
        "mean_T": round(float(np.mean(T)), 4),
        "mean_count": round(float(np.mean(C)), 4),
        "mean_rate": round(float(np.mean(R)), 4),
        "sd_rate": round(float(np.std(R)), 4),
    }
    out.update(boot_ci(np.asarray(T, float), np.asarray(C, float),
                       np.asarray(R, float)))
    return out


# ---------------------------------------------------------------- main
DEV_NOTE = ("assigned windows p in [2^12,2^18), q in [2^18,2^24) cap bitlen(p*q) "
            "at 42 -- unsatisfiable jointly with 'N exactly 52 bits'. Preserved the "
            "windows' SHAPE (12-octave span, q/p exponent gap ~ U(0,12), q larger) "
            "while enforcing bitlen==52: e~U{20..25}, p prime ~U[2^e,2^(e+1)), "
            "q prime ~U[2^(51-e),2^(52-e)), reject to bitlen 52, p<=q.")


def main():
    os.makedirs(WORK, exist_ok=True)
    t_start = time.time()

    state = {
        "exp": EXP, "codename": CODENAME, "round": ROUND,
        "date": time.strftime("%Y-%m-%d"),
        "script": SCRIPT_PATH,
        "preregistered_before_data": True,
        "hypotheses": {
            "H1": "pooled Spearman(T, rate) in [0.55, 0.85] at u=2.5",
            "H2": "pooled Spearman(T) - Spearman(count) > +0.05",
            "decision_rules": "primary = pooled-across-seeds estimate; per-seed reported",
            "verdict_names_pre_stated": {
                "both": "CELL-CLOSED-DIAL-HOLDS",
                "H1_only": "DIAL-HOLDS-NO-EDGE-OVER-COUNT",
                "H2_only": "BAND-BREAK-EDGE-PERSISTS",
                "neither": "DOUBLE-BREAK-52-UNIFORM"}},
        "config": {
            "seeds": SEEDS, "pop_per_seed": POP_N,
            "relation_values_per_N": N_VALS, "u_smooth": U_PAR, "bits": BITS,
            "bootstrap_resamples": BOOT,
            "dial": "T = sum_{odd QR primes d<=400} 2/d (Euler powmod)",
            "baseline": "count of odd QR primes d<=100",
            "design_deviation": DEV_NOTE},
        "seeds_data": {}, "stats": {}, "verdicts": {},
    }
    checkpoint(state)
    ledger("A-config", "preregistered hypotheses + design (+ deviation note) checkpointed")
    log("stage A: config checkpointed")

    for sd in SEEDS:
        rng = np.random.default_rng(sd)
        Ps, Qs, Ts, Cs, Rs = [], [], [], [], []
        t0 = time.time()
        for i in range(POP_N):
            p, q, N = gen_one(rng)
            T, c = dial_features(N)
            Ps.append(p)
            Qs.append(q)
            Ts.append(round(T, 6))
            Cs.append(c)
            Rs.append(relation_rate(N))
            if (i + 1) % 300 == 0:
                log("seed %d: %d/%d Ns (%.1fs)" % (sd, i + 1, POP_N, time.time() - t0))
        state["seeds_data"][str(sd)] = {
            "p": Ps, "q": Qs, "T": Ts, "count": Cs, "rate": Rs}
        checkpoint(state)
        ledger("B-seed-%d" % sd, "%d uniform 52-bit semiprimes: features + rates done"
               % POP_N, {"elapsed_s": round(time.time() - t0, 1)})
        log("stage B: seed %d done (%.1fs)" % (sd, time.time() - t0))

    # ---- stats
    stats = {}
    allT, allC, allR = [], [], []
    for sd in SEEDS:
        d = state["seeds_data"][str(sd)]
        allT += d["T"]
        allC += d["count"]
        allR += d["rate"]
        stats["seed_%d" % sd] = block(d["T"], d["count"], d["rate"])
        log("stats seed %d: Spm(T)=%.4f Spm(cnt)=%.4f adv=%+.4f rate_mean=%.4f"
            % (sd, stats["seed_%d" % sd]["spm_T"], stats["seed_%d" % sd]["spm_count"],
               stats["seed_%d" % sd]["advantage"], stats["seed_%d" % sd]["mean_rate"]))
    stats["pooled"] = block(allT, allC, allR)
    state["stats"] = stats
    checkpoint(state)
    ledger("E-stats", "per-seed + pooled Spearmans, advantages, bootstrap CIs (300)")
    log("stage E: stats done; pooled Spm(T)=%.4f Spm(cnt)=%.4f adv=%+.4f"
        % (stats["pooled"]["spm_T"], stats["pooled"]["spm_count"],
           stats["pooled"]["advantage"]))

    # ---- verdicts
    pooled = stats["pooled"]
    per_seed_T = [stats["seed_%d" % sd]["spm_T"] for sd in SEEDS]
    h1 = 0.55 <= pooled["spm_T"] <= 0.85
    h1_all_seeds = all(0.55 <= v <= 0.85 for v in per_seed_T)
    h2 = pooled["advantage"] > 0.05
    if h1 and h2:
        vn = "CELL-CLOSED-DIAL-HOLDS"
    elif h1:
        vn = "DIAL-HOLDS-NO-EDGE-OVER-COUNT"
    elif h2:
        vn = "BAND-BREAK-EDGE-PERSISTS"
    else:
        vn = "DOUBLE-BREAK-52-UNIFORM"
    state["verdicts"] = {
        "verdict_name": vn,
        "H1": {"pass": h1, "pooled_in_band": h1,
               "all_seeds_in_band": h1_all_seeds,
               "per_seed": {str(sd): per_seed_T[k] for k, sd in enumerate(SEEDS)}},
        "H2": {"pass": h2, "pooled_advantage": pooled["advantage"],
               "advantage_ci95": pooled["advantage_ci95"],
               "note": "CI lower edge reported alongside point rule"},
        "elapsed_total_s": round(time.time() - t_start, 1),
    }
    checkpoint(state)
    ledger("F-verdict", "VERDICT %s | H1=%s H2=%s" % (vn, h1, h2))
    log("stage F: VERDICT %s (H1=%s, H2=%s); total %.1fs"
        % (vn, h1, h2, time.time() - t_start))
    print("DONE", flush=True)


if __name__ == "__main__":
    main()

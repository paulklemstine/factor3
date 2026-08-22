#!/usr/bin/env python3
# =====================================================================
# round-57 / experiment 527 / codename TDIAL-U48B
# Fill the previously-unmeasured cell: ZERO-FIT DIAL on UNIFORM draws at
# EXACT BITLEN 48 -- variant B (independent window resolution vs exp 526).
#
# Dial        T(N) = sum over odd QR primes d <= 400 of 2/d,
#                   QR iff N^((d-1)//2) == 1 (mod d)   [Euler criterion,
#                   gmpy2.powmod]                      (features VERBATIM paper-164)
# Comparator  count(N) = #{odd QR primes d <= 100}     (bare QR-count)
# Target      relation rate: fraction of 240 QS relation values smooth at u=2.5
#
# State of the grid entering this run (repo record, read-only):
#   balanced : bitlen-48 cells rho_T = 0.6916/0.7279/0.7125 (exp 508 / paper 175);
#              44..52 in band; 56 starved (paper 178); 60 plateau (paper 179).
#   uniform  : exp 517 official arm actually measured N at 26..38 bits
#              (scaled sensitivity arm spanned 44..52, NOT exact);
#              exp 518 closed exact-52 (rho_T = 0.793/0.808/0.808);
#              exp 521 closed exact-60 (0.669);
#              exp 526 closed exact-48 under the LOCKED-LADDER window
#              resolution (e~U{20..25}, realized exponent gap 2..7 octaves):
#              rho_T = 0.7192/0.7202/0.7198, adv +0.098..+0.145, rate 12.5%.
# THIS RUN (variant B) re-measures the SAME cell under the PARENT'S OWN window
# shape instead of the ladder shape: concordance => the closure is robust to
# the window-resolution choice; discordance => window-shape sensitivity of the
# dial, which would be new. Seeds differ from nothing prior (assigned here):
# 20261110-12 (same seed set as 526 by assignment -- populations regenerate
# identically only if the generator matches, which it deliberately does NOT;
# the draw geometry differs, so these are fresh draws under a new resolution).
#
# ================= PRE-STATED HYPOTHESES (BEFORE ANY DATA) ===================
#  H1 (band): Spearman(T, rate) stays within [0.55, 0.85] on uniform draws at
#             exact bitlen 48, u = 2.5 -- ALL 3 seeds inside the band
#             (decision rule mirrors exp 526's all-seeds rule; pooled estimate
#             reported alongside; PARTIAL if pooled in band but some seed out).
#  H2 (edge): T beats count <= 100 by > +0.05, i.e. MEAN OVER SEEDS of
#             Spearman(T,rate) - Spearman(count<=100,rate) > +0.05 AND >= 2/3
#             individual seeds show advantage > +0.05 (mirrors exp 526).
#
# ================ DESIGN RESOLUTION (PRE-STATED BEFORE DATA) =================
#  The assigned windows p in [2^14,2^16), q in [2^16,2^18) cap bitlen(p*q) at
#  34 (max product < 2^34) and are UNSATISFIABLE jointly with the hard clause
#  "N must have bitlen exactly 48": the two clauses contradict, every literal
#  draw would be rejected, the population would be EMPTY. This is the same
#  copy-carried template defect documented pre-data in exp 517 ([2^10,2^16)x
#  [2^16,2^22)), exp 518 ([2^12,2^18)x[2^18,2^24)), exp 521 ([2^14,2^20)x
#  [2^20,2^26)). Resolution HERE (unlike 526's ladder adaptation): preserve the
#  LITERAL windows' own SHAPE -- two ADJACENT 2-octave windows, q's floor =
#  p's ceiling, q the larger factor -- shifted +8 octaves so that exact-48 is
#  interior to the product span (pre-rejection span [2^46,2^50)):
#      p ~ uniform prime in [2^22, 2^24);  q ~ uniform prime in [2^24, 2^26);
#      reject until bitlen(p*q) == 48 exactly; label so that p <= q.
#  Prime draws are UNBIASED rejection samples (uniform int, Miller-Rabin
#  accept, gmpy2.is_prime(n,25)). Realized marginals: p bitlen 23-24,
#  q bitlen 25-26, log2(q/p) in (0,4) octaves (mean 2) -- a genuinely
#  unbalanced regime, geometrically DISTINCT from exp 526's realized
#  gap-in-{2..7}-with-wider-marginals populations. Acceptance ~ 35-40%.
#
# ============ RELATION-RATE OPERATIONAL DEFINITION (verbatim paper-164,
#              as implemented in exp 508 / 521 / 526) =======================
#  sq = isqrt(N); j = 1..240; V_j = j*(2*sq + j) + (sq^2 - N)  [= (sq+j)^2-N].
#  vmed = median of the POOLED 1200x240 values per seed population;
#  B = max(round(exp(ln(vmed)/u)), 50), u = 2.5 (one global B per population).
#  Strip every prime <= B by trial division (vectorized);
#  relation := residual == 1; rate(N) = (#smooth of 240)/240.
#  SECONDARY SENSITIVITY readout (clearly labelled, non-decisional): the
#  exp 518 conservative convention -- strip primes <= 400 only, relation :=
#  cofactor == 1 OR cofactor <= floor(N^(2/5)).
#  No factor of N is ever used inside measurement; oracle primes construct N
#  only.
#
# ===================== VERDICT NAMES (PRE-STATED) ============================
#  H1 pass & H2 pass -> CELL-CLOSED-DIAL-HOLDS-UNIF-48B
#  H1 pass only      -> DIAL-HOLDS-NO-EDGE-OVER-COUNT-48B
#  H2 pass only      -> BAND-BREAK-EDGE-PERSISTS-48B
#  neither           -> DOUBLE-BREAK-48B-UNIFORM
#
# Barriers appended as standard lines (5)/(8). Ledger mandatory (jsonl).
# Runtime budget <= 15 min. Work confined to /tmp/exp57_tu48b/. Seeds 20261110-12.
# =====================================================================
import json, math, os, time
import numpy as np
import gmpy2
from scipy.stats import spearmanr

WORK = "/tmp/exp57_tu48b"
SCRIPT_PATH = os.path.join(WORK, "exp527_t_dial_unif_48.py")
RESULT_PATH = os.path.join(WORK, "result.json")
LEDGER_PATH = os.path.join(WORK, "ledger_exp527.jsonl")

EXP, CODENAME, ROUND = 527, "TDIAL-U48B", 57
SEEDS = [20261110, 20261111, 20261112]
POP_N = 1200          # uniform semiprimes per seed
NV = 240              # relation values per N (j = 1..240)
U_PAR = 2.5
BITS = 48
TPMAX, CNTMAX = 400, 100
BOOT = 300
P_LO_EXP, P_HI_EXP = 22, 24   # literal shape preserved, shifted +8 octaves
Q_LO_EXP, Q_HI_EXP = 24, 26

T0 = time.time()
state = {
    "experiment": EXP, "codename": CODENAME, "round": ROUND,
    "date": time.strftime("%Y-%m-%d"), "seeds": SEEDS,
    "prestated": {
        "H1": "Spearman(T,rate) within [0.55,0.85] on uniform draws at exact "
              "bitlen 48, u=2.5, ALL 3 seeds (pooled alongside)",
        "H2": "mean-over-seeds advantage Spearman(T)-Spearman(count<=100) "
              "> +0.05 AND >= 2/3 individual seeds > +0.05"},
    "design_resolution": (
        "assigned windows [2^14,2^16)x[2^16,2^18) cap N below 2^34 -- "
        "unsatisfiable jointly with exact bitlen 48; preserved literal SHAPE "
        "(adjacent 2-octave windows, q floor = p ceiling, q larger) shifted "
        "+8 octaves: p~Uprime[2^22,2^24), q~Uprime[2^24,2^26), reject until "
        "bitlen(N)==48, label p<=q; unbiased rejection prime draws"),
    "verdict_names": {
        "both": "CELL-CLOSED-DIAL-HOLDS-UNIF-48B",
        "h1_only": "DIAL-HOLDS-NO-EDGE-OVER-COUNT-48B",
        "h2_only": "BAND-BREAK-EDGE-PERSISTS-48B",
        "neither": "DOUBLE-BREAK-48B-UNIFORM"},
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

# ---------------------------------------------------------------- population
def rand_prime(rng, lo, hi):
    """Unbiased: rejection-sample uniform ints in [lo,hi), MR accept."""
    while True:
        n = int(rng.integers(lo, hi))
        if gmpy2.is_prime(n, 25):
            return n

def gen_one(rng):
    while True:
        p = rand_prime(rng, 1 << P_LO_EXP, 1 << P_HI_EXP)
        q = rand_prime(rng, 1 << Q_LO_EXP, 1 << Q_HI_EXP)
        if p == q:
            continue
        N = p * q
        if N.bit_length() != BITS:
            continue
        return p, q, N          # q > p structurally (disjoint windows)

# ---------------------------------------------------------------- features
def dial_and_count(N):
    t = c = 0
    for pr in ODD_400:
        if gmpy2.powmod(N % pr, (pr - 1) // 2, pr) == 1:
            t += W400[pr]
            if pr <= CNTMAX:
                c += 1
    return t, c

# ---------------------------------------------------------------- relations
def build_V(Ns):
    n = len(Ns)
    V = np.empty((n, NV), dtype=np.int64)
    for i, N in enumerate(Ns):
        sq = math.isqrt(int(N))
        base = sq * sq - int(N)
        two_sq = 2 * sq
        for j in range(1, NV + 1):
            V[i, j - 1] = j * (two_sq + j) + base
    return V

def strip_full(Vall, B):
    """Paper-164 convention: strip ALL primes <= B (one global B); smooth := residual==1."""
    primes = sieve(int(math.ceil(B)) + 1)
    W = Vall.copy()
    for pr in primes:
        while True:
            m = (W % pr == 0) & (W > 1)
            if not m.any():
                break
            W[m] //= pr
    return W == 1

def strip_400_cofactor(Vall, Ns):
    """exp518 conservative convention (SECONDARY): strip primes<=400 only;
    relation := cofactor==1 OR cofactor <= floor(N^(2/5))."""
    W = Vall.copy()
    for pr in sieve(TPMAX):
        while True:
            m = (W % pr == 0) & (W > 1)
            if not m.any():
                break
            W[m] //= pr
    ok = W == 1
    for i, N in enumerate(Ns):
        B_N = int(round(float(N) ** 0.4))       # N^(2/5)
        row = W[i]
        ok[i] |= row <= B_N
    return ok.mean(axis=1)

def smooth_audit_reference(v, B):
    """Pure-python reference smoothness test for designed-check audits."""
    if v == 1:
        return True
    for pr in sieve(int(math.ceil(B)) + 1):
        while v % pr == 0:
            v //= pr
            if v == 1:
                return True
    return v == 1

# ---------------------------------------------------------------- stats
def boot_ci(aT, aC, aR, seed):
    rng = np.random.default_rng(seed)
    n = len(aR)
    bT, bC = np.empty(BOOT), np.empty(BOOT)
    for b in range(BOOT):
        idx = rng.integers(0, n, n)
        bT[b] = spearmanr(aT[idx], aR[idx]).statistic
        bC[b] = spearmanr(aC[idx], aR[idx]).statistic
    bA = bT - bC
    def ci(x):
        return [round(float(np.percentile(x, 2.5)), 4),
                round(float(np.percentile(x, 97.5)), 4)]
    return {"spm_T_ci95": ci(bT), "spm_count_ci95": ci(bC), "advantage_ci95": ci(bA)}

def block(T, C, R, boot_seed):
    sT = float(spearmanr(T, R).statistic)
    sC = float(spearmanr(C, R).statistic)
    out = {"spm_T": round(sT, 4), "spm_count": round(sC, 4),
           "advantage": round(sT - sC, 4),
           "mean_T": round(float(np.mean(T)), 4),
           "mean_count": round(float(np.mean(C)), 4),
           "mean_rate": round(float(np.mean(R)), 4),
           "sd_rate": round(float(np.std(R)), 4)}
    out.update(boot_ci(np.asarray(T, float), np.asarray(C, float),
                       np.asarray(R, float), boot_seed))
    return out

# ---------------------------------------------------------------- main
def main():
    os.makedirs(WORK, exist_ok=True)
    state["config"] = {
        "seeds": SEEDS, "pop_per_seed": POP_N, "relation_values_per_N": NV,
        "u_smooth": U_PAR, "bits_exact": BITS, "bootstrap_resamples": BOOT,
        "windows": {"p": "[2^%d,2^%d)" % (P_LO_EXP, P_HI_EXP),
                    "q": "[2^%d,2^%d)" % (Q_LO_EXP, Q_HI_EXP)},
        "dial": "T = sum_{odd QR primes d<=400} 2/d (Euler powmod)",
        "baseline": "count of odd QR primes d<=100",
        "rate_convention": "paper-164 verbatim: global B=max(round(exp(ln vmed/u)),50); "
                           "strip primes<=B; smooth := residual==1",
        "secondary_rate": "exp518 convention (strip<=400, cofactor<=floor(N^(2/5)))",
    }
    checkpoint()
    ledger("A-config", "preregistered hypotheses + design resolution checkpointed")
    log("stage A: config checkpointed")

    per_seed_stats = {}
    allT, allC, allR = [], [], []
    for k, sd in enumerate(SEEDS):
        rng = np.random.default_rng(sd)
        Ps, Qs, Ts, Cs, Rs2 = [], [], [], [], []
        t0 = time.time()
        draws = 0
        for i in range(POP_N):
            p, q, N = gen_one(rng)
            draws += 1
            assert N.bit_length() == BITS                     # designed check: EVERY N
            T, c = dial_and_count(N)
            Ps.append(p); Qs.append(q); Ts.append(round(T, 6)); Cs.append(c)
            Rs2.append((p, q, N))
            if (i + 1) % 600 == 0:
                log("seed %d: %d/%d Ns (%.1fs)" % (sd, i + 1, POP_N, time.time() - t0))
        Ns = [t[2] for t in Rs2]

        # ---- designed check: semiprime integrity on every 97th + first/last
        idxs = list(range(0, POP_N, 97)) + [POP_N - 1]
        for i in idxs:
            p, q, N = Rs2[i]
            assert gmpy2.is_prime(p) and gmpy2.is_prime(q)
            assert N % p == 0 and N % q == 0 and p != q
            assert (1 << P_LO_EXP) <= p < (1 << P_HI_EXP)
            assert (1 << Q_LO_EXP) <= q < (1 << Q_HI_EXP)

        # ---- designed check: Euler criterion cross-checked against Jacobi symbol
        rng_chk = np.random.default_rng(sd + 555)
        for _ in range(50):
            i = int(rng_chk.integers(0, POP_N))
            N = Ns[i]
            pr = ODD_400[int(rng_chk.integers(0, len(ODD_400)))]
            # Euler criterion vs Legendre/Jacobi symbol: residue -> 1/1,
            # non-residue -> jacobi -1 / powmod pr-1; 0 impossible here
            # (every dial prime <= 400 < 2^22 <= min factor of N).
            r = gmpy2.powmod(N % pr, (pr - 1) // 2, pr)
            j = gmpy2.jacobi(N % pr, pr)
            assert (j == 1 and r == 1) or (j == -1 and r == pr - 1)

        pb = [int(x).bit_length() for x in Ps]
        qb = [int(x).bit_length() for x in Qs]
        gaps = [math.log2(q / p) for p, q, _ in Rs2]
        state["seed_%d_pop" % sd] = {
            "n": POP_N, "draw_attempts": draws,
            "bitlen_min": min(int(x).bit_length() for x in Ns),
            "bitlen_max": max(int(x).bit_length() for x in Ns),
            "p_bitlens": {b: pb.count(b) for b in sorted(set(pb))},
            "q_bitlens": {b: qb.count(b) for b in sorted(set(qb))},
            "gap_oct_mean": round(float(np.mean(gaps)), 3),
            "gap_oct_min": round(min(gaps), 3), "gap_oct_max": round(max(gaps), 3),
            "T_mean": round(float(np.mean(Ts)), 4), "T_sd": round(float(np.std(Ts)), 4),
            "count_mean": round(float(np.mean(Cs)), 4),
        }
        checkpoint()
        ledger("B%d-pop" % k, "%d exact-48-bit uniform semiprimes + dial features done"
               % POP_N, {"draws": draws})
        log("stage B: seed %d population+features done (%.1fs)" % (sd, time.time() - t0))

        # ---- stage C: relations + smoothness rates
        t1 = time.time()
        V = build_V(Ns)
        vmed = float(np.median(V.astype(np.float64)))
        B = max(round(math.exp(math.log(vmed) / U_PAR)), 50)
        smooth = strip_full(V, B)
        rate = smooth.mean(axis=1)
        rate_sec = strip_400_cofactor(V, Ns)

        # ---- designed check: brute-force smoothness audit, 200 random spots
        rng_aud = np.random.default_rng(sd + 777)
        for _ in range(200):
            i = int(rng_aud.integers(0, POP_N)); j = int(rng_aud.integers(0, NV))
            ref = smooth_audit_reference(int(V[i, j]), B)
            assert ref == bool(smooth[i, j])

        state["seed_%d_rate" % sd] = {
            "vmed": vmed, "B": B,
            "rate_mean": round(float(rate.mean()), 5),
            "rate_sd": round(float(rate.std()), 5),
            "rate_min": round(float(rate.min()), 5),
            "rate_max": round(float(rate.max()), 5),
            "zero_rate_Ns": int((rate == 0).sum()),
            "secondary_exp518_rate_mean": round(float(rate_sec.mean()), 5),
            "audit_checks": 200,
        }
        del V
        checkpoint()
        ledger("C%d-rate" % k, "relation rates done (B=%d, mean rate %.4f; secondary %.4f)"
               % (B, rate.mean(), rate_sec.mean()))
        log("stage C: seed %d rates done (%.1fs)" % (sd, time.time() - t1))

        # ---- stage D: per-seed stats
        st = block(np.array(Ts), np.array(Cs, float), rate, sd + 90000 + k)
        st["secondary_spm_T_vs_exp518rate"] = round(
            float(spearmanr(Ts, rate_sec).statistic), 4)
        per_seed_stats["seed_%d" % sd] = st
        allT += list(Ts); allC += list(Cs); allR += list(rate)
        state["stats"] = per_seed_stats
        checkpoint()
        ledger("D%d-stats" % k, "spm_T=%.4f spm_cnt=%.4f adv=%+.4f"
               % (st["spm_T"], st["spm_count"], st["advantage"]))
        log("seed %d: Spm(T)=%.4f Spm(cnt)=%.4f adv=%+.4f rate=%.4f (%.1fs)"
            % (sd, st["spm_T"], st["spm_count"], st["advantage"], st["mean_rate"],
               time.time() - t0))

    # ---- stage E: pooled stats
    pooled = block(np.array(allT), np.array(allC, float), np.array(allR), 424242)
    state["pooled"] = pooled
    checkpoint()
    ledger("E-pooled", "pooled spm_T=%.4f spm_cnt=%.4f adv=%+.4f"
           % (pooled["spm_T"], pooled["spm_count"], pooled["advantage"]))
    log("POOLED: Spm(T)=%.4f Spm(cnt)=%.4f adv=%+.4f"
        % (pooled["spm_T"], pooled["spm_count"], pooled["advantage"]))

    # ---- stage F: verdicts
    lo, hi = 0.55, 0.85
    per_T = [per_seed_stats["seed_%d" % s]["spm_T"] for s in SEEDS]
    per_adv = [per_seed_stats["seed_%d" % s]["advantage"] for s in SEEDS]
    in_band = [lo <= v <= hi for v in per_T]
    h1_all = all(in_band)
    h1_pooled = lo <= pooled["spm_T"] <= hi
    h1 = h1_all and h1_pooled
    h1_partial = (not h1) and (h1_pooled or any(in_band))
    mean_adv = float(np.mean(per_adv))
    n_adv = sum(a > 0.05 for a in per_adv)
    h2 = (mean_adv > 0.05) and (n_adv >= 2)
    if h1 and h2:
        vn = "CELL-CLOSED-DIAL-HOLDS-UNIF-48B"
    elif h1 or h1_pooled:
        vn = "DIAL-HOLDS-NO-EDGE-OVER-COUNT-48B"
    elif h2:
        vn = "BAND-BREAK-EDGE-PERSISTS-48B"
    else:
        vn = "DOUBLE-BREAK-48B-UNIFORM"
    state["verdicts"] = {
        "verdict_name": vn,
        "H1": {"pass": bool(h1), "pass_pooled_only": bool(h1_pooled),
               "partial": bool(h1_partial),
               "band": [lo, hi],
               "per_seed_in_band": {str(SEEDS[i]): bool(in_band[i]) for i in range(3)},
               "per_seed_spm_T": {str(SEEDS[i]): per_T[i] for i in range(3)},
               "pooled_spm_T": pooled["spm_T"], "pooled_ci95": pooled["spm_T_ci95"]},
        "H2": {"pass": bool(h2), "mean_over_seeds_advantage": round(mean_adv, 4),
               "n_seeds_adv_gt_005": n_adv,
               "per_seed_advantage": {str(SEEDS[i]): per_adv[i] for i in range(3)},
               "pooled_advantage": pooled["advantage"],
               "pooled_advantage_ci95": pooled["advantage_ci95"]},
        "barrier_lines": {
            "(5)": "Barrier 5 (structural orthogonality, unchanged): T and count are "
                   "computable from N alone and predict relation-yield variation across "
                   "same-band semiprimes; they carry NO which-factor information -- "
                   "consistent with the which-factor wall (papers 93/102).",
            "(8)": "Barrier 8 (known-method-in-disguise, unchanged): the QS relation "
                   "polynomial and trial-division target are the classical sieve "
                   "machinery; the dial only re-weights candidate yield, it is not a "
                   "new factoring route."},
        "elapsed_total_s": round(time.time() - T0, 1),
    }
    checkpoint()
    ledger("F-verdict", "VERDICT %s | H1=%s H2=%s (n_adv>0.05: %d/3)"
           % (vn, h1, h2, n_adv))
    log("VERDICT: %s | H1=%s H2=%s | total %.1fs" % (vn, h1, h2, time.time() - T0))

if __name__ == "__main__":
    main()

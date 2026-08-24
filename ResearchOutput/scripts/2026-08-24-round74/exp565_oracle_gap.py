#!/usr/bin/env python3
# =============================================================================
# exp565 ORACLE-REALIZATION-GAP  (2026-08-24, round-74)
#
# QUESTION: is the 0.4798-bit oracle peak I(1{d<=B}; b1) at B~=22758 (papers
# 193->197, exp549's factor-derived diagnostic) realizable by ANY N-computable
# query policy over the same navigation/query frame -- or does realizing it
# require factor-conditioned posteriors (circularity, barrier 6)?
#
# FRAME (reused EXACTLY from exp549_window_frontier.py -- not a new one):
#   population: 3 strata x NS semiprimes ('indep','unilog','ratio'), p in
#   [2^14,2^18], q in [2^16,2^22]; Fermat pair M=(p+q)/2, n=(q-p)/2; Berggren
#   descent via the parent-interval law; target b1 = first descent letter
#   (= ratio band: b1=1 iff q>3p, 2 iff 2p<q<3p, 3 iff q<2p); d = M - isqrt(N)
#   (FACTOR-DERIVED); oracle hint = 1{d<=B}; budget B = parabola-probe count,
#   same cost accounting as exp546/549.
#
# DELIVERABLE A (reproduction): recompute the fine-grid oracle curve on the
#   SAME seed-20260824 population and verify peak ~= 0.479797 @ B=22758 against
#   the published exp549_result.json fine_grid (hardcoded comparison points).
#
# POLICIES (all output a discrete hint H; realized MI = plug-in I(H;b1) bits
# on the HELD-OUT eval split; dual permutation nulls: pooled row-shuffle AND
# within-logN-decile shuffle per the round-70 METHOD LAW):
#   ORACLE-IND   cheating anchor: H = 1{d<=B} (factor-conditioned feature;
#                touches p,q of the TEST N). Realizes the bound by construction.
#   FULL-ORACLE  ceiling anchor: H = b1 itself. Shows the peak is NOT even the
#                factor-knowledge ceiling.
#   ADAPTIVE-NB  N-only: exact per-query greedy entropy minimization under a
#                naive-Bayes posterior over b1 fitted on the TRAIN split.
#                Each round every sample picks its highest-dH unqueried menu
#                item (answers are deterministic functions of N and known to
#                the policy in advance -- disclosed ledger L2), applies it,
#                updates. Snapshots at each budget rung.
#   BATTERY      N-only non-adaptive comparator: ONE pooled greedy order
#                (train cross-entropy reduction), applied identically to all
#                samples; snapshots at rungs.
#   BESTSINGLE   best single menu item (selected by TRAIN MI, evaluated on eval).
#   BASE-RATE    posterior = P(b1 | logN-decile) only -- the |N|-mirror class
#                ceiling (magnitude as sole feature).
#   SHAM         identical pipeline/cost, answers replaced by seeded iid draws
#                independent of N -- must realize ~0 bits (estimator control).
#
# QUERY MENU (pre-stated, 295 distinct N-computable queries; class exhausted
# at 295 -> budgets above are flat BY CLASS EXHAUSTION, ledger L3; ramp
# designs beyond the menu were already proven blind/mirror in exp549 D1-D4):
#   MOD(r)  N mod r, r in {3,4,5,7,8,9,11,13,16,17,19,23,25,27,29,31}
#           (sealed 2-adic/3-adic families + small primes + 5^2)
#   PAR(j)  E(isqrt(N)+j) = (isqrt+j)^2 - N, j in {0} u {2^k,k=0..22} u
#           {1..263} (deduped) -- the ascent window at all scales
#   FRAC    frac(sqrt(N)), quantile-binned
#   Parabola/frac features: 8 train-quantile bins; residues natural cardinality.
#
# REALIZED-MI CREDITING RULE (pre-stated, conservative, method-law-compliant):
#   credited_MI(policy) = pooled eval MI if (z_pooled>=3 AND z_within>=3)
#   else 0 -- an association that dies within logN strata is the known-N
#   magnitude artifact (paper 197), not extractable information.
#
# PRE-REGISTERED VERDICT RULES (strings COMPUTED from data):
#   fraction_of_peak(policy) = credited_MI / reproduced_oracle_peak.
#   H1 CONFIRMED ("REALIZATION-GAP-CONFIRMED"): max fraction over ALL N-only
#      policies {ADAPTIVE-NB, BATTERY, BESTSINGLE, BASE-RATE} < 0.25 on BOTH
#      seeds, AND sham credited = 0 on both.
#   H2 EVENT ("ORACLE-REALIZED-BY-NONLY"): some N-only policy reaches
#      fraction >= 0.50 on BOTH seeds (same family) AND sham clean.
#   else "GAP-PARTIAL" / "INCONCLUSIVE" mapping reported with numbers.
#   REPRODUCTION gate (full run only): |peak - 0.479797| <= 0.005 and every
#   published fine-grid point matched within 0.01 -- else ABORT before verdicts.
#
# PIPELINE CHECKS (abort on failure): Fermat identity m^2-n^2==pq; reversed-
# string ascent lands on (m,n) 100%; ratio-band == b1; E(isqrt)<0<E(isqrt+1)
# for every sample (structural sign constancy context, exp549 L9); sham MI
# within its own null; determinism spot-check of menu answers.
#
# LEDGER (disclosures):
#   L1: discriminative policies are naive-Bayes models FIT on a labeled TRAIN
#       population (standard lab hint-predictor framing); at test time they
#       touch only N. The ORACLE arms differ categorically: they touch the
#       FACTORS of the test N.
#   L2: menu answers are deterministic functions of N; the adaptive policy
#       reads its candidate answers without cost before choosing (the probe
#       action itself carries no extra information -- exp549 L9 corollary);
#       budget therefore measures DISTINCT INFORMATION-BEARING QUERIES, the
#       same currency as exp549's probe count under structural blindness.
#   L3: query class capped at the 295 pre-stated items; no filler ramps
#       (exp549 already proved anchored-ramp families structurally blind /
#       magnitude mirrors; a flat-by-extrapolation marker is recorded instead).
#   L4: plug-in MI bias at n=1500, 3x3 table ~ 0.001 bits; bootstrap CIs
#       reported; permutation z's are the significance instrument.
#   L5: b1 is p<->q SYMMETRIC (a function of the unordered pair via max/min),
#       so barrier-2 symmetry does NOT seal it a priori -- the residue/
#       magnitude null measured here is EMPIRICAL, extending paper 81's
#       letter-blindness to this menu class and target.
#   L6: fresh-seed replication uses seed 20260825; fractions must agree in
#       regime (<0.25 both / >=0.50 both) for the respective verdicts.
#
# AMENDMENT (declared AFTER the first full run of 2026-08-24; POST-HOC block):
#   The first full run showed ADAPTIVE-NB/BATTERY realizing 0.171/0.172 bits on
#   seed A -- numerically IDENTICAL to I(b1; logN 8-bin) of the same population
#   (0.1724 full-pop): the entire realized signal is N's OWN MAGNITUDE PRIOR
#   (population support-edge/truncation coupling between size and ratio),
#   available at ZERO query cost. Amendments, all labeled post-hoc:
#   (i) the published-constants reproduction gate applies to the SEED-A
#       population ONLY (seed B is a fresh-seed phenomenon replication --
#       reported, not gated);
#   (ii) added cost-0 MAGPRIOR-16/64 arms, a stricter z_within at 32 logN bins,
#       bias-corrected MI (observed minus pooled-null mean), a WITHIN-STRATUM
#       component decomposition (oracle vs policies), and battery-pick
#       composition logging;
#   (iii) the PRE-REGISTERED rules above are still evaluated VERBATIM on the
#       original crediting (zp>=3 & zw(8-bin)>=3) and reported unchanged;
#       post-hoc conclusions carry the POST-HOC label.
# =============================================================================
import argparse, json, math, os, random, sys, time
import numpy as np
from sympy import isprime

T0 = time.time()
PUBLISHED_FINE = [  # (B, I_oracle) from exp549_result.json oracle_diagnostic.fine_grid
    (1000, 0.124777), (2184, 0.206473), (4771, 0.324654), (10420, 0.436505),
    (22758, 0.479797), (49708, 0.461006), (108571, 0.348257),
    (237137, 0.235377), (517947, 0.128237), (1131283, 0.031323),
    (2470911, 0.0)]
PEAK_B_PUBLISHED, PEAK_I_PUBLISHED = 22758, 0.479797

ap = argparse.ArgumentParser()
ap.add_argument('--n-stratum', type=int, default=1000)
ap.add_argument('--perms', type=int, default=200)
ap.add_argument('--boots', type=int, default=1000)
ap.add_argument('--seed-a', type=int, default=20260824)
ap.add_argument('--seed-b', type=int, default=20260825)
ap.add_argument('--smoke', action='store_true')
ap.add_argument('--outdir', type=str,
                default='/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74')
args = ap.parse_args()
NS = args.n_stratum
if args.smoke:
    NS = min(NS, 120)
    PERMS, BOOTS = 40, 100
    LADDER = (16, 256, 4096)
else:
    PERMS, BOOTS = args.perms, args.boots
    LADDER = (16, 64, 256, 1024, 4096, 16384, 22758)

RESIDUES = (3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25, 27, 29, 31)
JPOOL = sorted(set([0] + [2 ** k for k in range(0, 23)] + list(range(1, 264))))
MENU = [('mod', r) for r in RESIDUES] + [('par', j) for j in JPOOL] + [('frac', None)]
M = len(MENU)
VMAX = 32
SMOKE = args.smoke

VERDICT_RULES = {
    "crediting": "credited_MI = pooled eval MI if (z_pooled>=3 and z_within>=3) else 0",
    "fraction_of_peak": "credited_MI / reproduced_oracle_peak(full population)",
    "H1_REALIZATION-GAP-CONFIRMED":
        "max fraction over {ADAPTIVE-NB,BATTERY,BESTSINGLE,BASE-RATE} < 0.25 on BOTH seeds AND sham credited==0 both",
    "H2_ORACLE-REALIZED-BY-NONLY":
        "some N-only policy fraction >= 0.50 on BOTH seeds (same family) AND sham clean",
    "reproduction_gate_full": "|peak-0.479797|<=0.005 and all published fine points within 0.01, else ABORT",
}
prereg = {"experiment": 565, "codename": "ORACLE-REALIZATION-GAP", "round": 74,
          "date_preregistered": "2026-08-24", "smoke": SMOKE,
          "purpose": "Is the 0.4798-bit oracle peak I(1{d<=B};b1) @ B~=22758 realizable by any "
                     "N-computable query policy, or only by factor-conditioned posteriors (barrier 6)?",
          "hypotheses_stated_before_data": {
              "H1": "Every N-computable policy realizes <25% of the oracle peak (artifact-controlled); "
                    "the realizing posteriors are factor-conditioned.",
              "H2_barrier_event": "Some N-only policy exceeds 50% of the peak AND survives fresh-seed "
                                  "replication + sham control."},
          "verdict_rules": VERDICT_RULES,
          "config": {"n_stratum": NS, "perms": PERMS, "boots": BOOTS, "ladder": list(LADDER),
                     "menu_size": M, "residues": list(RESIDUES), "seeds": [args.seed_a, args.seed_b],
                     "frame": "exp549 verbatim (population/descent/oracle definition)"}}
with open(os.path.join(args.outdir, 'exp565_prereg.json'), 'w') as f:
    json.dump(prereg, f, indent=1)


def log(msg):
    print(msg, flush=True)


def rand_prime(lo, hi, rng):
    while True:
        c = rng.randint(lo, hi)
        if isprime(c):
            return c


def next_odd_prime_from(x):
    c = max(int(math.ceil(x)), 3)
    if c % 2 == 0:
        c += 1
    while not isprime(c):
        c += 2
    return c


def descend(m, n):
    """node->root letters via parent-interval law (exp549 verbatim)."""
    L = []
    steps = 0
    while not (m == 2 and n == 1):
        steps += 1
        if steps > 2_000_000:
            raise RuntimeError("descent overflow")
        if m < 2 * n:
            L.append(1); m, n = n, 2 * n - m
        elif m < 3 * n:
            L.append(2); m, n = n, m - 2 * n
        else:
            L.append(3); m, n = m - 2 * n, n
    return L


def ascend(letters_node_to_root):
    m, n = 2, 1
    for letter in reversed(letters_node_to_root):
        if letter == 1:
            m, n = 2 * m - n, m
        elif letter == 2:
            m, n = 2 * m + n, m
        else:
            m, n = m + 2 * n, n
    return m, n


def gen_population(seed, ns):
    """exp549 generation loop verbatim (parameterized seed)."""
    rng = random.Random(seed)
    STRATA = ['indep', 'unilog', 'ratio']
    P, Q, STRAT = [], [], []
    for kind in STRATA:
        got = 0
        while got < ns:
            if kind == 'indep':
                p = rand_prime(2 ** 14, 2 ** 18, rng)
                q = rand_prime(2 ** 16, 2 ** 22, rng)
            elif kind == 'unilog':
                lp = 14.0 + 4.0 * rng.random()
                lq = 16.0 + 6.0 * rng.random()
                p = next_odd_prime_from(2.0 ** lp)
                q = next_odd_prime_from(2.0 ** lq)
                if not (2 ** 14 <= p <= 2 ** 18 and 2 ** 16 <= q <= 2 ** 22):
                    continue
            else:
                lr = math.log(1.02) + rng.random() * (math.log(60.0) - math.log(1.02))
                p = rand_prime(2 ** 14, 2 ** 18, rng)
                qt = p * math.exp(lr)
                lo_q = max(2 ** 16, int(math.ceil(qt * 0.98)))
                hi_q = min(2 ** 22, int(qt * 1.02) + 1)
                if lo_q >= hi_q:
                    continue
                q = rand_prime(lo_q, hi_q, rng)
            if p == q:
                continue
            if p > q:
                p, q = q, p
            P.append(p); Q.append(q); STRAT.append(kind)
            got += 1
    return np.array(P, dtype=np.int64), np.array(Q, dtype=np.int64), np.array(STRAT)


def mi_bits(xc, yc, K, C):
    T = np.zeros((K, C))
    np.add.at(T, (xc, yc), 1.0)
    tot = T.sum()
    Pxy = T / tot
    Px = T.sum(1, keepdims=True) / tot
    Py = T.sum(0, keepdims=True) / tot
    E = Px * Py
    mk = Pxy > 0
    return float((Pxy[mk] * np.log2(Pxy[mk] / E[mk])).sum())


def confusion(xb, yb, K, C):
    T = np.zeros((K, C))
    np.add.at(T, (xb, yb), 1.0)
    return T


def boot_ci(T, nb=BOOTS, seed=12345):
    """bootstrap CI of plug-in MI from a fixed confusion table."""
    rngb = np.random.default_rng(seed)
    n = T.sum()
    Pxy = T / n
    vals = np.empty(nb)
    flatP = Pxy.ravel()
    for i in range(nb):
        draw = rngb.multinomial(int(n), flatP).reshape(T.shape).astype(float)
        Px = draw.sum(1, keepdims=True); Py = draw.sum(0, keepdims=True)
        E = Px * Py / n
        mk = draw > 0
        vals[i] = (draw[mk] / n * np.log2((draw[mk] / n) / E[mk])).sum()
    return float(np.quantile(vals, 0.025)), float(np.quantile(vals, 0.975))


def dual_perm_test(xb, yb, binid, nperm=PERMS):
    """observed MI + pooled row-shuffle null + within-logN-bin shuffle null."""
    n = len(yb)
    K = int(xb.max()) + 1
    C = int(yb.max()) + 1
    obs = mi_bits(xb, yb, K, C)
    rp = np.random.default_rng(777)
    nul_p = np.empty(nperm); nul_w = np.empty(nperm)
    for i in range(nperm):
        nul_p[i] = mi_bits(xb, yb[rp.permutation(n)], K, C)
        yw = yb.copy()
        for b in np.unique(binid):
            ix = np.flatnonzero(binid == b)
            if len(ix) > 1:
                yw[ix] = yb[ix[rp.permutation(len(ix))]]
        nul_w[i] = mi_bits(xb, yw, K, C)
    mp, sp = float(nul_p.mean()), float(nul_p.std(ddof=0) + 1e-12)
    mw, sw = float(nul_w.mean()), float(nul_w.std(ddof=0) + 1e-12)
    return obs, mp, sp, (obs - mp) / sp, mw, sw, (obs - mw) / sw


def xlogx_sum(p):
    with np.errstate(divide='ignore', invalid='ignore'):
        t = np.where(p > 0, p * np.log2(np.maximum(p, 1e-300)), 0.0)
    return -t.sum(-1)


# ===========================================================================
# one full pipeline pass on one population seed
# ===========================================================================
def run_seed(seed, tag):
    log(f"\n===== seed {seed} ({tag}) =====")
    TG = time.time()
    P, Q, STRAT = gen_population(seed, NS)
    NP_ = len(P)
    TD = time.time()
    Mm = (P + Q) // 2
    Nn = (Q - P) // 2
    ok = bool(np.all(Mm.astype(object) ** 2 - Nn.astype(object) ** 2
                     == P.astype(object) * Q.astype(object)))
    assert ok, "Fermat identity broken"
    letters = [descend(int(Mm[i]), int(Nn[i])) for i in range(NP_)]
    asc_ok = sum(1 for i in range(NP_) if ascend(letters[i]) == (int(Mm[i]), int(Nn[i])))
    assert asc_ok == NP_, "ascent reconstruction failed"
    dB = np.array([len(L) for L in letters], dtype=np.int64)
    b1 = np.array([L[0] for L in letters], dtype=np.int64)
    band = np.where(Mm < 2 * Nn, 1, np.where(Mm < 3 * Nn, 2, 3)).astype(np.int64)
    assert np.array_equal(band, b1), "band!=b1"
    N64 = P * Q
    isq = np.array([math.isqrt(int(v)) for v in N64], dtype=np.int64)
    d_fermat = Mm - isq
    assert np.all(d_fermat >= 1)
    # structural sign constancy (exp549 L9 identity)
    assert np.all(N64 - isq.astype(object) ** 2 >= 0), "E(isqrt)>=0 ?!"
    e0 = isq.astype(object) ** 2 - N64.astype(object)
    e1 = (isq + 1).astype(object) ** 2 - N64.astype(object)
    assert np.all(e0 < 0), "E(isqrt)<0 violated"
    assert np.all(e1 > 0), "E(isqrt+1)>0 violated"
    t_desc = time.time() - TD

    # ---------------- stratified split ----------------
    tr_idx, ev_idx = [], []
    rs = np.random.default_rng(seed + 5)
    for s in ('indep', 'unilog', 'ratio'):
        ix = np.flatnonzero(STRAT == s)
        rs.shuffle(ix)
        h = len(ix) // 2
        tr_idx.extend(ix[:h]); ev_idx.extend(ix[h:])
    tr = np.array(tr_idx); ev = np.array(ev_idx)
    b1z_all = b1 - 1
    logN = np.log(N64.astype(float))
    edges_logn = np.unique(np.quantile(logN[tr], np.linspace(0, 1, 9)[1:-1]))
    bin_all = np.clip(np.searchsorted(edges_logn, logN, side='right'), 0, len(edges_logn))
    NB = int(bin_all.max()) + 1

    # ---------------- DELIVERABLE A: oracle curve ----------------
    TO = time.time()
    grid = sorted(set(int(round(v)) for v in np.logspace(np.log2(8), np.log2(2 ** 22), 57)))
    hin_all = lambda B: (d_fermat <= B).astype(np.int64)
    fine = []
    for B in grid:
        h = hin_all(B)
        fine.append({"B": int(B), "I_oracle": round(mi_bits(h, b1z_all, 2, 3), 6),
                     "hit_rate": round(float(h.mean()), 4)})
    Io = np.array([r["I_oracle"] for r in fine]); Bs_ = np.array([r["B"] for r in fine])
    imax_i = int(np.argmax(Io)); PEAK = float(Io[imax_i]); PEAKB = int(Bs_[imax_i])
    sat = int(np.flatnonzero(Io >= 0.9 * PEAK)[0])
    t_orc = time.time() - TO
    log(f"[oracle] peak I={PEAK:.6f} @ B={PEAKB} (0.9-sat B*={Bs_[sat]}); "
        f"d median={int(np.median(d_fermat))} b1 dist={np.bincount(b1, minlength=4)[1:].tolist()}")
    repro = {"peak_recomputed": round(PEAK, 6), "peak_B_recomputed": PEAKB,
             "peak_published": PEAK_I_PUBLISHED, "peak_B_published": PEAK_B_PUBLISHED,
             "delta_peak": round(abs(PEAK - PEAK_I_PUBLISHED), 6),
             "fine_grid_published_vs_recomputed": []}
    for Bp, Ip in PUBLISHED_FINE:
        rec = next((r["I_oracle"] for r in fine if r["B"] == Bp), None)
        repro["fine_grid_published_vs_recomputed"].append(
            {"B": Bp, "published": Ip, "recomputed": rec,
             "delta": None if rec is None else round(abs(rec - Ip), 6)})

    # ---------------- menu answer matrix ----------------
    TF = time.time()
    raw = np.zeros((NP_, M), dtype=np.int64)
    kinds = np.array([k for k, _ in MENU])
    lev = np.zeros(M, dtype=np.int64)
    for i, (kind, prm) in enumerate(MENU):
        if kind == 'mod':
            raw[:, i] = N64 % prm
            lev[i] = prm
        elif kind == 'par':
            a = isq + prm
            raw[:, i] = (a.astype(object) ** 2 - N64.astype(object)).astype(np.int64)
            lev[i] = 8
        else:
            fr = np.sqrt(N64.astype(float)) - np.floor(np.sqrt(N64.astype(float)))
            raw[:, i] = (fr * 1e9).astype(np.int64)
            lev[i] = 8
    codes = np.zeros((NP_, M), dtype=np.int64)
    bin_edges = []
    for i in range(M):
        if kinds[i] == 'mod':
            codes[:, i] = raw[:, i]
        else:
            ed = np.unique(np.quantile(raw[tr, i].astype(float),
                                       np.linspace(0, 1, 9)[1:-1]))
            codes[:, i] = np.searchsorted(ed, raw[:, i].astype(float), side='right')
            bin_edges.append(ed.tolist())
    t_feat = time.time() - TF

    # ---------------- NB tables from train ----------------
    K3 = 3
    counts = np.zeros((M, K3, VMAX))
    for i in range(M):
        for k in range(K3):
            cnt = np.bincount(codes[tr][b1z_all[tr] == k, i], minlength=int(lev[i]))
            counts[i, k, :len(cnt)] = cnt
    Ttab = (counts + 0.5) / (counts.sum(2, keepdims=True) + 0.5 * lev[:, None, None])
    prior = np.bincount(b1z_all[tr], minlength=3).astype(float)
    prior /= prior.sum()
    Vtr = codes[tr]; Vev = codes[ev]
    ytr = b1z_all[tr]; yev = b1z_all[ev]
    btr = bin_all[tr]; bev = bin_all[ev]

    def apply_feature(post, i, vv):
        p = post * Ttab[i, :, vv]
        return p / np.maximum(p.sum(-1, keepdims=True), 1e-300)

    # ---------------- ADAPTIVE-NB: exact per-query greedy ----------------
    TA = time.time()
    BCAP = M
    post_ad = np.tile(prior, (len(ev), 1))
    picked = np.zeros((len(ev), M), dtype=bool)
    yhat_rungs = {}
    rung_list = sorted(LADDER)
    arangeM = np.arange(M)[None, :]
    done = 0
    ri = 0
    while done < BCAP and ri < len(rung_list):
        act = np.flatnonzero(~picked.all(axis=1))
        if act.size == 0:
            break
        pa = post_ad[act]
        Hc = xlogx_sum(pa)
        Tv = Ttab[arangeM, :, Vev[act]]              # (Sa,M,3)
        num = pa[:, None, :] * Tv
        Z = np.maximum(num.sum(2, keepdims=True), 1e-300)
        Hp = xlogx_sum(num / Z)
        sc = Hc[:, None] - Hp
        sc[picked[act]] = -np.inf
        fid = np.argmax(sc, axis=1)
        vv = Vev[act, fid]
        post_ad[act] = apply_feature(pa, fid, vv)
        picked[act, fid] = True
        done += 1
        while ri < len(rung_list) and rung_list[ri] <= done:
            yhat_rungs[rung_list[ri]] = np.argmax(post_ad, axis=1).copy()
            ri += 1
    for B in rung_list:
        yhat_rungs.setdefault(B, np.argmax(post_ad, axis=1).copy())
    t_adapt = time.time() - TA
    log(f"[adaptive] queries executed={done} (class exhaustion at M={M}) in {t_adapt:.1f}s")

    # ---------------- BATTERY: pooled greedy order ----------------
    TB = time.time()
    ppost_tr = np.tile(prior, (len(tr), 1))
    Tv_tr = Ttab[arangeM, :, Vtr]                    # (Str,M,3)
    bpicked = np.zeros(M, dtype=bool)
    order = []
    for _ in range(M):
        num = ppost_tr[:, None, :] * Tv_tr
        Z = np.maximum(num.sum(2, keepdims=True), 1e-300)
        Hm = xlogx_sum(num / Z).mean(axis=0)
        Hm[bpicked] = np.inf
        mm = int(np.argmin(Hm))
        order.append(mm); bpicked[mm] = True
        ppost_tr = apply_feature(ppost_tr, mm, Vtr[:, mm])
    post_bat = np.tile(prior, (len(ev), 1))
    yhat_bat = {}
    ri = 0
    for t, mm in enumerate(order, start=1):
        post_bat = apply_feature(post_bat, mm, Vev[:, mm])
        while ri < len(rung_list) and rung_list[ri] <= t:
            yhat_bat[rung_list[ri]] = np.argmax(post_bat, axis=1).copy()
            ri += 1
    for B in rung_list:
        yhat_bat.setdefault(B, np.argmax(post_bat, axis=1).copy())
    t_batt = time.time() - TB

    # ---------------- composition controls (AMENDMENT, post-hoc) ------------
    def battery_subset(idx_subset):
        """pooled greedy order restricted to a menu subset; eval posterior."""
        if len(idx_subset) == 0:
            return np.tile(prior, (len(ev), 1))
        pp = np.tile(prior, (len(tr), 1))
        ar = np.arange(len(idx_subset))[None, :]
        Tvtr = Ttab[idx_subset][ar, :, Vtr[:, idx_subset]]
        picked = np.zeros(len(idx_subset), dtype=bool)
        for _ in range(len(idx_subset)):
            num = pp[:, None, :] * Tvtr
            Z = np.maximum(num.sum(2, keepdims=True), 1e-300)
            Hm = xlogx_sum(num / Z).mean(axis=0)
            Hm[picked] = np.inf
            mm = int(np.argmin(Hm))
            picked[mm] = True
            pp = apply_feature(pp, idx_subset[mm], Vtr[:, idx_subset[mm]])
        pe = np.tile(prior, (len(ev), 1))
        for mm in idx_subset[picked]:
            pe = apply_feature(pe, mm, Vev[:, mm])
        return np.argmax(pe, axis=1)

    par_idx = np.array([i for i, (k, _) in enumerate(MENU) if k in ('par', 'frac')])
    mod_idx = np.array([i for i, (k, _) in enumerate(MENU) if k == 'mod'])
    yhat_paronly = battery_subset(par_idx)
    yhat_modonly = battery_subset(mod_idx)
    t_batt = time.time() - TB

    # ---------------- BASE-RATE + BESTSINGLE candidates ----------------
    cntb = np.zeros((NB, K3))
    np.add.at(cntb, (btr, ytr), 1.0)
    Tb = (cntb + 0.5) / (cntb.sum(1, keepdims=True) + 1.5)
    pb = Tb[bev]
    base_hat = np.argmax(pb, axis=1)
    tr_mi_single = []
    for i in range(M):
        tr_mi_single.append(mi_bits(Vtr[:, i], ytr, int(lev[i]), 3))
    top5 = np.argsort(tr_mi_single)[::-1][:5]
    t_misc = time.time() - TB - t_batt

    # ---------------- MAGPRIOR arms (AMENDMENT: cost-0 magnitude priors) ----
    mag_hats = {}
    for KB in (16, 64):
        edm = np.unique(np.quantile(logN[tr], np.linspace(0, 1, KB + 1)[1:-1]))
        bm_tr = np.clip(np.searchsorted(edm, logN[tr], side='right'), 0, len(edm))
        bm_ev = np.clip(np.searchsorted(edm, logN[ev], side='right'), 0, len(edm))
        cm = np.zeros((len(edm) + 1, K3))
        np.add.at(cm, (bm_tr, ytr), 1.0)
        Tm = (cm + 0.5) / (cm.sum(1, keepdims=True) + 1.5)
        mag_hats[KB] = {"hat": np.argmax(Tm[bm_ev], axis=1), "nlev": len(edm) + 1}

    # stricter within-strata id (32 logN bins, train edges) for AMENDED stats
    ed32 = np.unique(np.quantile(logN[tr], np.linspace(0, 1, 33)[1:-1]))
    bin32_all = np.clip(np.searchsorted(ed32, logN, side='right'), 0, len(ed32))
    bev32 = bin32_all[ev]

    def within_component(xb, ycode, K, C, binid, nperm=60):
        """magnitude-stratified MI component + its own within-shuffle null."""
        def wc(yv):
            tot = 0.0
            n = len(yv)
            for b in np.unique(binid):
                msk = binid == b
                if msk.sum() > 10 and len(np.unique(yv[msk])) > 1 \
                        and len(np.unique(xb[msk])) > 1:
                    tot += msk.sum() / n * mi_bits(xb[msk], yv[msk],
                                                   int(xb[msk].max()) + 1, C)
            return tot
        obs = wc(ycode)
        rp = np.random.default_rng(4242)
        nul = np.empty(nperm)
        for i in range(nperm):
            yw = ycode.copy()
            for b in np.unique(binid):
                ix = np.flatnonzero(binid == b)
                if len(ix) > 1:
                    yw[ix] = ycode[ix[rp.permutation(len(ix))]]
            nul[i] = wc(yw)
        return obs, float(nul.mean()), float((obs - nul.mean()) / (nul.std(ddof=0) + 1e-12))

    # ---------------- SHAM ----------------
    rs2 = np.random.default_rng(seed + 999)
    sham_codes = np.zeros_like(Vev)
    for i in range(M):
        support = np.unique(Vtr[:, i])
        sham_codes[:, i] = support[rs2.integers(0, len(support), size=len(ev))]
    psh = np.tile(prior, (len(ev), 1))
    yhat_sham = {}
    ri = 0
    for t, mm in enumerate(order, start=1):
        psh = apply_feature(psh, mm, sham_codes[:, mm])
        while ri < len(rung_list) and rung_list[ri] <= t:
            yhat_sham[rung_list[ri]] = np.argmax(psh, axis=1).copy()
            ri += 1
    for B in rung_list:
        yhat_sham.setdefault(B, np.argmax(psh, axis=1).copy())

    # ---------------- stats assembly ----------------
    TS = time.time()

    def dual_perm_test3(xb, yb, bin1, bin2, nperm=PERMS):
        """pooled + within-bin1 + within-bin2 nulls in one permutation loop."""
        n = len(yb)
        K = int(xb.max()) + 1
        C = int(yb.max()) + 1
        obs = mi_bits(xb, yb, K, C)
        rp = np.random.default_rng(777)

        def wshuffle(binid):
            yw = yb.copy()
            for b in np.unique(binid):
                ix = np.flatnonzero(binid == b)
                if len(ix) > 1:
                    yw[ix] = yb[ix[rp.permutation(len(ix))]]
            return yw

        nul_p = np.empty(nperm); nul_1 = np.empty(nperm); nul_2 = np.empty(nperm)
        for i in range(nperm):
            nul_p[i] = mi_bits(xb, yb[rp.permutation(n)], K, C)
            nul_1[i] = mi_bits(xb, wshuffle(bin1), K, C)
            nul_2[i] = mi_bits(xb, wshuffle(bin2), K, C)
        m1, s1 = float(nul_p.mean()), float(nul_p.std(ddof=0) + 1e-12)
        ma, sa = float(nul_1.mean()), float(nul_1.std(ddof=0) + 1e-12)
        mb, sb = float(nul_2.mean()), float(nul_2.std(ddof=0) + 1e-12)
        return obs, m1, s1, (obs - m1) / s1, ma, sa, (obs - ma) / sa, (obs - mb) / sb

    def stat_row(hint_codes, ycode, K, label):
        o, mp, sp, zp, mw, sw, zw, zw32 = dual_perm_test3(hint_codes, ycode, bev, bev32)
        lo, hi = boot_ci(confusion(hint_codes, ycode, K, 3))
        return {"row": label, "MI_bits": round(o, 6),
                "MI_bias_corrected": round(o - mp, 6),
                "z_pooled": round(zp, 3),
                "z_within": round(zw, 3), "z_within32": round(zw32, 3),
                "ci95": [round(lo, 6), round(hi, 6)],
                "credited_bits": round(o, 6) if (zp >= 3 and zw >= 3) else 0.0,
                "credited_strict": round(o, 6) if (zp >= 3 and zw >= 3 and zw32 >= 3) else 0.0}

    rows = {"oracle_ind": {}, "full_oracle": {}, "adaptive_nb": {}, "battery": {},
            "base_rate": None, "bestsingle": {}, "sham": {},
            "magprior16": None, "magprior64": None,
            "paronly_battery": None, "modonly_battery": None}
    for B in rung_list:
        h = (d_fermat[ev] <= B).astype(np.int64)
        rows["oracle_ind"][str(B)] = stat_row(h, yev, 2, f"ORACLE-IND B={B}")
        rows["adaptive_nb"][str(B)] = stat_row(yhat_rungs[B], yev, 3, f"ADAPTIVE-NB B={B}")
        rows["battery"][str(B)] = stat_row(yhat_bat[B], yev, 3, f"BATTERY B={B}")
        rows["sham"][str(B)] = stat_row(yhat_sham[B], yev, 3, f"SHAM B={B}")
    rows["full_oracle"] = stat_row(b1z_all[ev], yev, 3, "FULL-ORACLE (hint=b1)")
    rows["base_rate"] = stat_row(base_hat, yev, 3, "BASE-RATE logN-decile(8)")
    for KB in (16, 64):
        rows[f"magprior{KB}"] = stat_row(mag_hats[KB]["hat"], yev,
                                         mag_hats[KB]["nlev"], f"MAGPRIOR-{KB} cost0")
    Blast = rung_list[-1]
    rows["paronly_battery"] = stat_row(yhat_paronly, yev, 3, "PARONLY-BATTERY (mirrors only)")
    rows["modonly_battery"] = stat_row(yhat_modonly, yev, 3, "MODONLY-BATTERY (residues only)")
    best_i = int(top5[0])
    rows["bestsingle"]["item"] = f"{MENU[best_i][0]}:{MENU[best_i][1]}"
    rows["bestsingle"]["stat"] = stat_row(Vev[:, best_i], yev, int(lev[best_i]),
                                          f"BESTSINGLE {rows['bestsingle']['item']}")
    rows["bestsingle"]["top5_trainMI_items"] = [
        {"item": f"{MENU[i][0]}:{MENU[i][1]}", "train_MI": round(tr_mi_single[i], 6)}
        for i in top5]
    # AMENDMENT: battery pick composition + within-stratum component decomposition
    rows["battery"]["first12_picks"] = [f"{MENU[mm][0]}:{MENU[mm][1]}" for mm in order[:12]]
    wdec = {}
    wdec["oracle_at_22758"] = within_component((d_fermat[ev] <= 22758).astype(np.int64),
                                               yev, 2, 3, bev32)
    wdec["adaptive_last"] = within_component(yhat_rungs[rung_list[-1]], yev, 3, 3, bev32)
    wdec["battery_last"] = within_component(yhat_bat[rung_list[-1]], yev, 3, 3, bev32)
    wdec["paronly_last"] = within_component(yhat_paronly, yev, 3, 3, bev32)
    wdec["modonly_last"] = within_component(yhat_modonly, yev, 3, 3, bev32)
    wdec["magprior64"] = within_component(mag_hats[64]["hat"], yev,
                                          mag_hats[64]["nlev"], 3, bev32)
    rows["within_decomp_32bin"] = {
        k: {"within_bits": round(v[0], 6), "null_mean": round(v[1], 6),
            "z": round(v[2], 3), "excess_bits": round(v[0] - v[1], 6)}
        for k, v in wdec.items()}
    t_stat = time.time() - TS

    popstats = {"n_total": int(NP_), "n_train": int(len(tr)), "n_eval": int(len(ev)),
                "b1_dist": np.bincount(b1, minlength=4)[1:].tolist(),
                "H_b1_eval_bits": round(mi_bits(yev, yev.copy(), 3, 3), 6),
                "d_median": int(np.median(d_fermat)), "d_mean": round(float(d_fermat.mean()), 1),
                "dB_median": int(np.median(dB))}
    timing = {"gen": round(time.time() - TG, 1), "descend_checks": round(t_desc, 1),
              "oracle_curve": round(t_orc, 2), "features": round(t_feat, 1),
              "adaptive": round(t_adapt, 1), "battery_order": round(t_batt, 1),
              "stats": round(t_stat, 1)}

    # verdict inputs (data-driven)
    nonly = ["adaptive_nb", "battery", "base_rate", "bestsingle"]
    out = {"seed": seed, "tag": tag, "oracle": {"peak": round(PEAK, 6), "peak_B": PEAKB,
                                                "sat_B_09": int(Bs_[sat]), "fine": fine},
           "reproduction": repro, "popstats": popstats, "rows": rows, "timing": timing}
    return out


# ===========================================================================
def main():
    results = {}
    for seed, tag in ((args.seed_a, 'repro'), (args.seed_b, 'replica')):
        results[str(seed)] = run_seed(seed, tag)

# ---------------------------------------------------------------------------
# verdicts (computed from data, pre-stated rules)
# ---------------------------------------------------------------------------
    peaks = {s: r["oracle"]["peak"] for s, r in results.items()}
    verdicts = {"per_seed": {}}
    gate_pass = True
    if not SMOKE:
        # AMENDMENT (post-hoc): published-constant gate applies to SEED A ONLY;
        # seed B is a fresh phenomenon replication -- reported, not gated.
        sa = str(args.seed_a)
        dmax = max((x["delta"] or 0)
                   for x in results[sa]["reproduction"]["fine_grid_published_vs_recomputed"])
        dpk = results[sa]["reproduction"]["delta_peak"]
        gate_pass = (dpk <= 0.005) and (dmax <= 0.01)
        verdicts["reproduction_seedA"] = {"pass": bool(gate_pass), "delta_peak": dpk,
                                          "max_delta_fine": dmax}
        sb = str(args.seed_b)
        verdicts["replication_seedB_reported_only"] = {
            "delta_peak_vs_published": results[sb]["reproduction"]["delta_peak"],
            "note": "fresh population; curve need not match seed-A constants"}

    fractions = {}
    posthoc = {}
    for s, r in results.items():
        pk = peaks[s]
        fr = {}
        for pol in ("adaptive_nb", "battery"):
            rr = r["rows"][pol]
            cred = max(v["credited_bits"] for k, v in rr.items() if k.isdigit())
            pooled_max = max(v["MI_bits"] for k, v in rr.items() if k.isdigit())
            strict_max = max(v["credited_strict"] for k, v in rr.items() if k.isdigit())
            fr[pol] = {"credited_bits": cred, "fraction_of_peak": round(cred / pk, 4),
                       "credited_strict": strict_max,
                       "pooled_max_bits": round(pooled_max, 6),
                       "pooled_fraction_of_peak": round(pooled_max / pk, 4)}
        for nm in ("base_rate", "magprior16", "magprior64"):
            br = r["rows"][nm]
            fr[nm] = {"credited_bits": br["credited_bits"],
                      "credited_strict": br["credited_strict"],
                      "fraction_of_peak": round(br["credited_bits"] / pk, 4),
                      "pooled_max_bits": br["MI_bits"],
                      "bias_corrected_bits": br["MI_bias_corrected"],
                      "pooled_fraction_of_peak": round(br["MI_bits"] / pk, 4)}
        fr["bestsingle"] = {"credited_bits": r["rows"]["bestsingle"]["stat"]["credited_bits"],
                            "fraction_of_peak": round(r["rows"]["bestsingle"]["stat"]["credited_bits"] / pk, 4)}
        fr["full_oracle"] = {"bits": r["rows"]["full_oracle"]["MI_bits"],
                             "fraction_of_peak": round(r["rows"]["full_oracle"]["MI_bits"] / pk, 4)}
        fr["sham_max_bits"] = max(rr["MI_bits"] for rr in r["rows"]["sham"].values())
        fr["sham_credited_max"] = max(rr["credited_bits"] for rr in r["rows"]["sham"].values())
        fr["oracle_at_22758"] = (r["rows"]["oracle_ind"].get("22758", {}) or {}).get("MI_bits")
        fractions[s] = fr
        # POST-HOC decomposition: composition controls + within-stratum geometry
        mp64 = fr["magprior64"]["pooled_max_bits"]
        pol_pooled = max(fr[p]["pooled_max_bits"] for p in ("adaptive_nb", "battery"))
        paronly_pooled = r["rows"]["paronly_battery"]["MI_bits"]
        modonly_pooled = r["rows"]["modonly_battery"]["MI_bits"]
        wd = r["rows"]["within_decomp_32bin"]
        orc_w = wd["oracle_at_22758"]["excess_bits"]
        best_pol_w = max(wd["adaptive_last"]["excess_bits"], wd["battery_last"]["excess_bits"],
                         wd["paronly_last"]["excess_bits"], wd["modonly_last"]["excess_bits"])
        posthoc[s] = {
            "magprior64_pooled_bits": mp64,
            "probe_excess_over_magprior64_bits": round(pol_pooled - mp64, 6),
            "paronly_battery_pooled_bits": round(paronly_pooled, 6),
            "modonly_battery_pooled_bits": round(modonly_pooled, 6),
            "oracle_within32_excess_bits": round(orc_w, 6),
            "best_policy_within32_excess_bits": round(best_pol_w, 6),
            "policy_within_fraction_of_oracle_within":
                round(best_pol_w / orc_w, 4) if orc_w > 1e-9 else None,
            "oracle_within_fraction_of_peak": round(orc_w / pk, 4),
            "battery_first12": r["rows"]["battery"]["first12_picks"]}

    nonly_pols = ("adaptive_nb", "battery", "base_rate", "bestsingle")
    if SMOKE:
        verdicts["mode"] = "SMOKE (mechanics only; reproduction gate deferred to full run)"
    else:
        h1 = all(max(fractions[s][p]["fraction_of_peak"] for p in nonly_pols) < 0.25
                 for s in fractions) and \
             all(fractions[s]["sham_credited_max"] == 0.0 for s in fractions)
        h2fam = None
        for p in nonly_pols:
            if all(fractions[s][p]["fraction_of_peak"] >= 0.50 for s in fractions):
                h2fam = p
                break
        h2 = (h2fam is not None) and all(fractions[s]["sham_credited_max"] == 0.0 for s in fractions)
        verdicts["pre_registered_evaluation"] = {}
        verdicts["pre_registered_evaluation"]["H1_confirmed"] = bool(h1)
        verdicts["pre_registered_evaluation"]["H2_event"] = bool(h2)
        if h2:
            verdicts["pre_registered_evaluation"]["family"] = h2fam
        verdicts["reproduction_gate_pass"] = bool(gate_pass)
        verdicts["fractions"] = fractions
        if not gate_pass:
            verdicts["verdict_pre_registered"] = "REPRODUCTION-FAIL"
        elif h2:
            verdicts["verdict_pre_registered"] = "ORACLE-REALIZED-BY-NONLY"
        elif h1:
            verdicts["verdict_pre_registered"] = "REALIZATION-GAP-CONFIRMED"
        else:
            verdicts["verdict_pre_registered"] = "GAP-PARTIAL"
        # ---- POST-HOC block (AMENDMENT) ----
        ph_all = posthoc
        within_zero = all(abs(ph_all[s]["best_policy_within32_excess_bits"]) <= 0.01
                          for s in ph_all)
        par_carries = (
            all(ph_all[s]["paronly_battery_pooled_bits"] >= 0.8 *
                max(fractions[s]["battery"]["pooled_max_bits"], 1e-9) for s in ph_all)
            and all(ph_all[s]["modonly_battery_pooled_bits"]
                    <= 0.25 * ph_all[s]["paronly_battery_pooled_bits"] for s in ph_all))
        verdicts["post_hoc"] = {
            "decomposition": ph_all,
            "nonly_within32_content_zero": bool(within_zero),
            "signal_is_magnitude_ensemble_not_residues": bool(par_carries),
            "strict_crediting_max_fraction_by_seed": {
                s: round(max(fractions[s][p].get("credited_strict", 0)
                             for p in nonly_pols if p in fractions[s]) / peaks[s], 4)
                for s in fractions},
            "reading": ("N-only policies carry ZERO within-magnitude-strata content: their pooled "
                        "signal is the between-strata population magnitude-base-rate channel "
                        "(support-edge coupling of the population design), read out at low variance "
                        "by mirror-feature ensembles; the peak's within-strata GEOMETRIC core "
                        "(~74-77% of peak) is realized ONLY by factor-conditioned posteriors"
                        if within_zero else
                        "some within-strata N-only content remains -- inspect")}

    out_json = {"exp": 565, "codename": "ORACLE-REALIZATION-GAP", "date": "2026-08-24",
                "status": "smoke" if SMOKE else "06_final",
                "question": "Is the 0.4798-bit oracle peak realizable by any N-computable policy?",
                "config": prereg["config"], "preregistered_verdict_rules": VERDICT_RULES,
                "published_reference": {"paper": 197, "source": "exp549_result.json",
                                        "peak": PEAK_I_PUBLISHED, "peak_B": PEAK_B_PUBLISHED},
                "results_by_seed": results, "verdicts": verdicts,
                "honest_notes": [
                    "L1: discriminative policies fit on labeled TRAIN split; test-time N-only.",
                    "L2: menu answers deterministic in N; budget = distinct information-bearing queries.",
                    "L3: query class capped at %d pre-stated items; budgets above flat by class exhaustion." % M,
                    "L4: plug-in MI bias reported corrected (obs minus pooled-null mean); bootstrap CI + perm z.",
                    "L5: b1 is p<->q symmetric; barrier-2 does NOT a-priori seal it -- null is empirical.",
                    "L6: crediting rule zeroes policies failing within-logN-strata control (method law).",
                    "A1 AMENDMENT (post-hoc, declared after first full run): adaptive/battery signal "
                    "= free magnitude prior I(b1;logN); added MAGPRIOR arms, z_within32, bias-corrected MI, "
                    "within-component decomposition; reproduction gate restricted to seed A; pre-registered "
                    "rules still evaluated verbatim."],
                "wall_s": round(time.time() - T0, 1)}
    path = os.path.join(args.outdir, 'exp565_%s.json' % ('smoke' if SMOKE else 'result'))
    with open(path, 'w') as f:
        json.dump(out_json, f, indent=1)
    log(f"\n[done] wrote {path}; wall={out_json['wall_s']}s")
    log(f"[verdicts] {json.dumps(verdicts)}")



if __name__ == "__main__":
    main()

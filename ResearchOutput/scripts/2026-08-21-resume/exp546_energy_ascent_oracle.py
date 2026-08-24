#!/usr/bin/env python3
# =============================================================================
# exp546 ENERGY-ASCENT-ORACLE  (2026-08-23, seed 20260823)
#
# QUESTION: does any CHEAP energy spectrum computed from N ALONE predict the
# Berggren branch letters?  ("energy spectrum" = magnitude/frequency content of
# sequences derived from N -- NOT residue classes.)
#
# BACKGROUND (exp391/exp416/paper81 conventions ADOPTED VERBATIM):
#   - odd semiprime N=pq sits at tree node (m,n)=((p+q)/2,(q-p)/2), m>n>0,
#     m^2-n^2=N, gcd=1, opposite parity.
#   - descent to root (2,1) via parent-interval law, INTEGER comparisons:
#       m < 2n  -> letter 1, parent (n, 2n-m)      [rho in (1,2)]
#       m < 3n  -> letter 2, parent (n, m-2n)      [rho in (2,3)]
#       else    -> letter 3, parent (m-2n, n)      [rho > 3]
#   - b1 := FIRST DESCENT STEP FROM THE NODE (deepest-edge letter) -- the same
#     convention as paper 81 ("the first letter is a deterministic function of
#     the band").  We ALSO record b_root1 = last descent letter (root-side
#     first letter) as an EXTRA target, labelled explicitly.
#   - children: g1=(2m-n,m) g2=(2m+n,m) g3=(m+2n,n)
#
# PIPELINE CHECK (abort on failure): re-ascend from (2,1) applying the descent
#   string REVERSED through the matching generators; must land on (m,n) for
#   100% of nodes.  Plus per-step child-map reconstruction during descent.
#
# PRE-STATED HYPOTHESES / VERDICTS (verdict string COMPUTED from data below,
#   never hardcoded):
#   H1: no N-only feature beats null on b1 (all z<3)          -> ENERGY-ASCENT-NULL
#   H2: some N-only cell z>=3 AND its OOS gate beats chance   -> ENERGY-ASCENT-SIGNAL
#       (gate: 5x stratified 70/30 split, pooled accuracy, Wilson95 lower
#        bound > uniform chance 1/3 (single letters/composition), 1/9 joint,
#        1/4 dB-quartile)
#   H3 controls: POSITIVE ratio-band -> b1 exact (match rate 1.0);
#                NEGATIVE N mod 3, 9, 27 null (replicating paper 81).
#
# STATISTICS (binding lab lessons): MI in bits, coarse quantile bins (<=12) for
#   continuous features; residues kept at NATURAL cardinality (3, 9) except
#   mod-27 which is grouped contiguously to 12 (disclosed deviation);
#   permutation null = SHUFFLE DATA ROWS x{perms}, reuse observed bin edges;
#   EVERY cell tested is reported (no cherry-picking); z>=3 flagged with a
#   multiplicity caveat (expected false flags = n_nonly_cells * P(Z>3)).
#
# INTERPRETIVE NOTES (ledger-seeded):
#   L1: the task formula G(t)=|sum_x exp(2pi i (t x^2 + x)/M')| contains no N;
#       taken literally it is constant across N (zero variance).  To make it
#       the intended "deterministic function of N mod small numbers" negative
#       control we scale the phase index by (N mod M'): phase uses
#       (N*(t x^2+x)) mod M'.  Disclosed here.
#   L2: unilog stratum draws log-uniform reals then rounds UP to the next odd
#       candidate prime (slight discretization, disclosed).
# =============================================================================
import argparse, json, math, random, sys, time
import numpy as np
from sympy import isprime

T0 = time.time()
SEED = 20260823
MAX_STEPS = 2_000_000
WINDOWS = (1024, 4096)
GAUSS_MODULI = (64, 128, 256)
NBINS = 12
FLAGZ = 3.0

ap = argparse.ArgumentParser()
ap.add_argument('--n-stratum', type=int, default=1000)
ap.add_argument('--perms', type=int, default=300)
ap.add_argument('--outdir', type=str,
                default='/home/raver1975/factor3/ResearchOutput/scripts/2026-08-21-resume')
args = ap.parse_args()
NS = args.n_stratum
NPERM = args.perms

rng = random.Random(SEED)                    # python RNG: population draws
rng_perm = np.random.default_rng(SEED + 1)   # permutation nulls
rng_oos = np.random.default_rng(SEED + 2)    # OOS splits

LEDGER = [
    "L1: Gauss-sum phases scaled by (N mod M') -- literal formula has no N and "
    "would be constant across N (see header note).",
    "L2: unilog stratum rounds log-uniform reals up to next odd candidate.",
    f"L3: mod-27 control grouped contiguously to {NBINS} classes to honor the "
    "<=12-bin rule; mod 3 and mod 9 kept at natural cardinality.",
    "L4 (smoke-run catch): letter targets were 1-based and crashed the OOS gate "
    "(IndexError, class index out of bounds); all targets re-coded 0-based.",
    "L5: OOS gate reports BOTH the pre-stated uniform-chance rule AND the empirical "
    "majority-class baseline (skewed letter distributions make 1/3 weak); "
    "beats_majority_ptest is a point-estimate supplement, not the pre-stated gate.",
    "L6: added factor-derived Fermat-hit-distance diagnostic to localize WHERE the "
    "spectral b1 information lives (zero-crossing of E(a) inside the FFT window).",
]

def log(msg):
    print(msg, flush=True)

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def rand_prime(lo, hi):
    """uniform odd-candidate prime draw in [lo,hi], python-rng reproducible."""
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
    """node->root letters via parent-interval law (integer compares).
    Per-step child-map reconstruction asserted.  Returns letters list."""
    L = []
    steps = 0
    while not (m == 2 and n == 1):
        steps += 1
        if steps > MAX_STEPS:
            raise RuntimeError(f"descent exceeded {MAX_STEPS} steps at ({m},{n})")
        if m < 2 * n:      # rho in (1,2) -> letter 1
            letter, pm, pn = 1, n, 2 * n - m
        elif m < 3 * n:    # rho in (2,3) -> letter 2
            letter, pm, pn = 2, n, m - 2 * n
        else:              # rho > 3 -> letter 3
            letter, pm, pn = 3, m - 2 * n, n
        # independent per-step verification: child map applied to the parent
        # must reconstruct the current node (catches sign/order bugs)
        if letter == 1:
            ok = (2 * pm - pn, pm) == (m, n)
        elif letter == 2:
            ok = (2 * pm + pn, pm) == (m, n)
        else:
            ok = (pm + 2 * pn, pn) == (m, n)
        if not ok:
            raise RuntimeError(f"child-map reconstruction failed at ({m},{n}) letter {letter}")
        L.append(letter)
        m, n = pm, pn
    return L

def ascend(letters_node_to_root):
    """re-ascend root->node by applying the REVERSED descent string through
    the matching generators."""
    m, n = 2, 1
    for letter in reversed(letters_node_to_root):
        if letter == 1:
            m, n = 2 * m - n, m
        elif letter == 2:
            m, n = 2 * m + n, m
        else:
            m, n = m + 2 * n, n
    return m, n

# ---------------------------------------------------------------------------
# population: 3 strata x NS  (indep-uniform / uniform-log / ratio-stratified)
# ---------------------------------------------------------------------------
log(f"=== exp546 ENERGY-ASCENT-ORACLE ===")
log(f"config: NS/stratum={NS} (x3 strata), perms={NPERM}, windows={WINDOWS}, "
    f"gauss={GAUSS_MODULI}, bins<={NBINS}, seed={SEED}")

TG = time.time()
STRATA = ['indep', 'unilog', 'ratio']
P = []; Q = []; STRAT = []
for kind in STRATA:
    got = 0
    while got < NS:
        if kind == 'indep':
            p = rand_prime(2**14, 2**18)
            q = rand_prime(2**16, 2**22)
        elif kind == 'unilog':
            lp = 14.0 + 4.0 * rng.random()
            lq = 16.0 + 6.0 * rng.random()
            p = next_odd_prime_from(2.0 ** lp)
            q = next_odd_prime_from(2.0 ** lq)
            if not (2**14 <= p <= 2**18 and 2**16 <= q <= 2**22):
                continue
        else:  # ratio-stratified: log-rho ~ U(ln 1.02, ln 60)
            lr = math.log(1.02) + rng.random() * (math.log(60.0) - math.log(1.02))
            p = rand_prime(2**14, 2**18)
            qt = p * math.exp(lr)
            lo_q = max(2**16, int(math.ceil(qt * 0.98)))
            hi_q = min(2**22, int(qt * 1.02) + 1)
            if lo_q >= hi_q:
                continue
            q = rand_prime(lo_q, hi_q)
        if p == q:
            continue
        if p > q:
            p, q = q, p
        P.append(p); Q.append(q); STRAT.append(kind)
        got += 1
P = np.array(P, dtype=np.int64); Q = np.array(Q, dtype=np.int64)
STRAT = np.array(STRAT)
NP_ = len(P)
t_gen = time.time() - TG
log(f"[gen] {NP_} semiprimes in {t_gen:.1f}s")

# Fermat pairs + descent + pipeline check
TD = time.time()
M = (P + Q) // 2
Nn = (Q - P) // 2
assert np.all(M * M - Nn * Nn == P * Q), "Fermat identity broken"
letters_list = []
max_depth = 0
for i in range(NP_):
    L = descend(int(M[i]), int(Nn[i]))
    letters_list.append(L)
    max_depth = max(max_depth, len(L))

# PIPELINE CHECK: reversed-string ascent must land back on (m,n), 100%
asc_ok = 0
for i in range(NP_):
    if ascend(letters_list[i]) == (int(M[i]), int(Nn[i])):
        asc_ok += 1
log(f"[pipeline] ascent matches: {asc_ok}/{NP_}")
if asc_ok != NP_:
    log("PIPELINE CHECK FAILED -- ABORTING")
    sys.exit(1)

dB = np.array([len(L) for L in letters_list], dtype=np.int64)
b1 = np.array([L[0] for L in letters_list], dtype=np.int64)          # deepest-edge letter (paper-81 convention)
broot1 = np.array([L[-1] for L in letters_list], dtype=np.int64)     # root-side first letter (EXTRA target)
mask_d2 = dB >= 2
joint12 = np.full(NP_, -1, dtype=np.int64)
joint12[mask_d2] = np.array([(L[0] - 1) * 3 + (L[1] - 1) for L in letters_list if len(L) >= 2])
# composition-majority class (ties -> lowest letter id)
comp = np.empty(NP_, dtype=np.int64)
comp_frac = np.zeros((NP_, 3))
for i, L in enumerate(letters_list):
    c = np.bincount(np.array(L), minlength=4)[1:4]
    comp_frac[i] = c / len(L)
    comp[i] = int(np.argmax(c))  # 0-based letter-1..3
t_desc = time.time() - TD
log(f"[descend] depths: mean={dB.mean():.1f} median={np.median(dB):.0f} "
    f"range=[{dB.min()},{dB.max()}]; {t_desc:.1f}s")

# ratio band (POSITIVE control feature) -- needs factors, NOT N-only
band = np.where(M < 2 * Nn, 1, np.where(M < 3 * Nn, 2, 3)).astype(np.int64)
assert np.array_equal(band, b1), "band!=b1: descent law inconsistent"

log("[pop] per-stratum dB:")
for s in STRATA:
    sel = STRAT == s
    log(f"   {s:6s}: n={sel.sum()} dB mean={dB[sel].mean():.1f} med={np.median(dB[sel]):.0f} "
        f"max={dB[sel].max()} rho=[{(M[sel]/Nn[sel]).min():.3f},{(M[sel]/Nn[sel]).max():.1f}]")
log(f"   b1 dist: {np.bincount(b1, minlength=4)[1:].tolist()}  "
    f"depth>=2: {int(mask_d2.sum())}")

# ---------------------------------------------------------------------------
# FEATURES (all N-only, cheap)
# ---------------------------------------------------------------------------
TF = time.time()

def spectrum_summaries(x, W, prefix):
    xc = x - x.mean()
    F = np.fft.rfft(xc)
    Pw = np.abs(F) ** 2
    s = Pw.sum()
    Pn = Pw / s if s > 0 else Pw
    f = np.arange(len(Pn))
    nz = slice(1, None)
    Pf = Pn[nz]
    ent = float(-(Pf * np.log2(Pf + 1e-300)).sum())
    cent = float((f[nz] * Pf).sum() / Pf.sum())
    order = np.argsort(Pf)[::-1]
    p1 = float(f[nz][order[0]]) / W           # normalized freq (cycles/sample)
    p2 = float(f[nz][order[1]]) / W
    hr = float(Pf[order[0]] / (Pf[order[1]] + 1e-300))
    K = len(Pn) - 1
    lo = float(Pn[1:K // 3 + 1].sum())
    mid = float(Pn[K // 3 + 1:2 * K // 3 + 1].sum())
    hi = float(Pn[2 * K // 3 + 1:].sum())
    A = np.vstack([f[nz], np.ones(K)]).T
    slope = float(np.linalg.lstsq(A, np.log2(Pf + 1e-300), rcond=None)[0][0])
    return {f"{prefix}_ent": ent, f"{prefix}_cent": cent,
            f"{prefix}_p1": p1, f"{prefix}_p2": p2, f"{prefix}_hratio": hr,
            f"{prefix}_third_lo": lo, f"{prefix}_third_mid": mid,
            f"{prefix}_third_hi": hi, f"{prefix}_slope": slope}

feat_rows = [dict() for _ in range(NP_)]
for i in range(NP_):
    n_i = int(P[i]) * int(Q[i])               # exact python int (< 2^44)
    a0 = math.isqrt(n_i)
    ni64 = np.int64(n_i)                      # < 2^53: int64-exact throughout
    for W in WINDOWS:
        j = np.arange(W, dtype=np.int64)
        a = a0 + j
        E = a * a - ni64                      # exact in int64 (values < 2^41)
        Ef = E.astype(np.float64)             # lossless: |E| < 2^53
        feat_rows[i].update(spectrum_summaries(Ef, W, f"f1_w{W}"))
        feat_rows[i].update(spectrum_summaries(np.abs(Ef), W, f"f2_w{W}"))
    for Mp in GAUSS_MODULI:
        xx = np.arange(Mp, dtype=np.int64)
        tt = np.arange(1, Mp, dtype=np.int64)
        base = (np.outer(tt, xx * xx % Mp) + xx[None, :]) % Mp
        idx = (base * (n_i % Mp)) % Mp            # NOTE L1: N enters via N mod M'
        ph = np.exp(2j * np.pi * idx / Mp)
        G = np.abs(ph.sum(axis=1))
        Gn = G / G.sum()
        feat_rows[i][f"g{Mp}_max"] = float(G.max())
        feat_rows[i][f"g{Mp}_argmax"] = float(int(np.argmax(G)) + 1)
        feat_rows[i][f"g{Mp}_ent"] = float(-(Gn * np.log2(Gn + 1e-300)).sum())

FEATS_NONLY = [k for k in feat_rows[0].keys()]
X = {k: np.array([r[k] for r in feat_rows], dtype=np.float64) for k in FEATS_NONLY}
NEG = {"mod3": (P.astype(object) * Q.astype(object)) % 3,
       "mod9": (P.astype(object) * Q.astype(object)) % 9}
Nall = (P.astype(object) * Q.astype(object))
NEG["mod27g"] = np.array([min(int((int(v) * NBINS) // 27), NBINS - 1) for v in Nall % 27])
t_feat = time.time() - TF
log(f"[features] {len(FEATS_NONLY)} N-only features + 3 negative controls in {t_feat:.1f}s")

# ---------------------------------------------------------------------------
# MI machinery (bits; quantile bins <=12; row-shuffle permutation null)
# ---------------------------------------------------------------------------
def bin_quantile(x, nbins=NBINS):
    qs = np.linspace(0, 1, nbins + 1)[1:-1]
    edges = np.unique(np.quantile(x, qs))
    return np.searchsorted(edges, x, side='right'), len(edges) + 1

def mi_bits(xc, yc, K, C):
    T = np.zeros((K, C))
    np.add.at(T, (xc, yc), 1.0)
    tot = T.sum()
    Pxy = T / tot
    Px = T.sum(1, keepdims=True) / tot
    Py = T.sum(0, keepdims=True) / tot
    E = Px * Py
    m = Pxy > 0
    return float((Pxy[m] * np.log2(Pxy[m] / E[m])).sum())

# LEDGER L4 (smoke-run catch): letter targets must be 0-based for the shared
# MI/OOS machinery -- 1-based codes silently over-sized contingency tables and
# crashed the OOS gate with IndexError.
b1z = b1 - 1
broot1z = broot1 - 1
TARGETS = {
    "b1":      (b1z, 3, 1.0 / 3),
    "joint12": (joint12[mask_d2], 9, 1.0 / 9),
    "dbq":     (None, 4, 0.25),   # filled after quartiles
    "comp":    (comp, 3, 1.0 / 3),
    "broot1":  (broot1z, 3, 1.0 / 3),
}
qs_db = np.unique(np.quantile(dB.astype(float), np.linspace(0, 1, 5)[1:-1]))
dbq_all = np.searchsorted(qs_db, dB.astype(float), side='right')
TARGETS["dbq"] = (dbq_all, 4, 0.25)

cells = []

def perm_test(xb, yb, nperm=NPERM):
    n = len(yb)
    K = int(xb.max()) + 1
    C = int(yb.max()) + 1
    obs = mi_bits(xb, yb, K, C)
    null = np.empty(nperm)
    for i in range(nperm):
        null[i] = mi_bits(xb[rng_perm.permutation(n)], yb, K, C)
    mu, sd = float(null.mean()), float(null.std(ddof=0) + 1e-12)
    return obs, mu, sd, (obs - mu) / sd

def oos_gate(xraw, ycodes, ncls, chance, reps=5, frac=0.7):
    """5x stratified-in-effect random 70/30 splits; pooled bin-posterior
    predictions.  Reports Wilson95 CI vs UNIFORM CHANCE (pre-stated gate) AND
    vs the EMPIRICAL MAJORITY-CLASS baseline (supplementary honesty check --
    skewed targets make the 1/3 gate weak)."""
    n = len(ycodes)
    maj_rate = float(np.bincount(ycodes, minlength=ncls).max() / n)
    correct = 0; tot = 0; reps_acc = []
    for _ in range(reps):
        idx = rng_oos.permutation(n)
        ntr = int(round(frac * n))
        tr, te = idx[:ntr], idx[ntr:]
        e = np.unique(np.quantile(xraw[tr], np.linspace(0, 1, NBINS + 1)[1:-1]))
        btr = np.searchsorted(e, xraw[tr], side='right')
        Kb = int(btr.max()) + 1
        bte = np.minimum(np.searchsorted(e, xraw[te], side='right'), Kb - 1)
        cnt = np.zeros((Kb, ncls))
        np.add.at(cnt, (btr, ycodes[tr]), 1.0)
        post = (cnt + 1.0) / (cnt.sum(1, keepdims=True) + ncls)
        pred = post[bte].argmax(1)
        c = int((pred == ycodes[te]).sum())
        correct += c; tot += len(te); reps_acc.append(c / max(1, len(te)))
    acc = correct / tot
    zz = 1.959964
    den = 1 + zz * zz / tot
    ctr = (acc + zz * zz / (2 * tot)) / den
    hw = zz * math.sqrt(acc * (1 - acc) / tot + zz * zz / (4 * tot * tot)) / den
    ci = (ctr - hw, ctr + hw)
    passed = ci[0] > chance
    beats_maj = acc > maj_rate  # point estimate only (supplementary)
    return acc, ci, passed, tot, maj_rate, beats_maj

TS = time.time()
# --- N-only cells -----------------------------------------------------------
for fname in FEATS_NONLY:
    x = X[fname]
    xb, K = bin_quantile(x)
    for tname, (yarr, ncls, chance) in TARGETS.items():
        if tname == "joint12":
            xb_t, y_t = xb[mask_d2], yarr
        else:
            xb_t, y_t = xb, yarr
        I, mu, sd, z = perm_test(xb_t, y_t)
        cell = {"role": "nonly", "feature": fname, "target": tname,
                "n": int(len(y_t)), "bins": int(K), "I": round(I, 6),
                "null_mean": round(mu, 6), "null_sd": round(sd, 6),
                "z": round(z, 3), "flag_z3": bool(z >= FLAGZ)}
        if z >= FLAGZ:  # OUT-OF-SAMPLE GATE (only for flagged cells)
            xr = x[mask_d2] if tname == "joint12" else x
            acc, ci, passed, tot, maj_rate, beats_maj = oos_gate(xr, y_t, ncls, chance)
            cell["oos"] = {"acc": round(acc, 4), "ci95": [round(ci[0], 4), round(ci[1], 4)],
                           "chance": chance, "pass": bool(passed), "n_test": int(tot),
                           "majority_baseline": round(maj_rate, 4),
                           "beats_majority_ptest": bool(beats_maj)}
        cells.append(cell)
    done = FEATS_NONLY.index(fname) + 1
    if done % 9 == 0:
        log(f"[stats] {done}/{len(FEATS_NONLY)} N-only features scanned ({time.time()-TS:.0f}s)")

# --- NEGATIVE controls: N mod 3^k ------------------------------------------
neg_worst_z = -1e9
for cname, cres in NEG.items():
    yc = cres.astype(np.int64)
    for tname, (yarr, ncls, chance) in TARGETS.items():
        if tname == "joint12":
            xc_, y_t = yc[mask_d2], yarr
        else:
            xc_, y_t = yc, yarr
        I, mu, sd, z = perm_test(xc_, y_t)
        neg_worst_z = max(neg_worst_z, z)
        cells.append({"role": "negctrl", "feature": cname, "target": tname,
                      "n": int(len(y_t)), "bins": int(xc_.max() + 1), "I": round(I, 6),
                      "null_mean": round(mu, 6), "null_sd": round(sd, 6),
                      "z": round(z, 3), "flag_z3": bool(z >= FLAGZ)})
neg_pass = neg_worst_z < FLAGZ

# --- POSITIVE control: factor-derived ratio band -> b1 ----------------------
Hb1 = float(-(np.bincount(b1, minlength=4)[1:] / NP_ *
              np.log2(np.bincount(b1, minlength=4)[1:] / NP_ + 1e-300)).sum())
I_band = mi_bits(band - 1, b1 - 1, 3, 3)
match_rate = float(np.mean(band == b1))
pos_pass = (match_rate == 1.0) and (I_band >= 0.999 * Hb1)
cells.append({"role": "posctrl", "feature": "ratio_band", "target": "b1",
              "n": NP_, "bins": 3, "I": round(I_band, 6), "null_mean": None,
              "null_sd": None, "z": None,
              "note": f"deterministic control: match_rate={match_rate:.4f}, H(b1)={Hb1:.4f}"})
log(f"[controls] POSITIVE band->b1 match={match_rate:.4f} I={I_band:.4f} vs H(b1)={Hb1:.4f} -> {'PASS' if pos_pass else 'FAIL'}")
log(f"[controls] NEGATIVE mod-3^k worst z={neg_worst_z:+.2f} -> {'PASS (null)' if neg_pass else 'FAIL'}")

# --- MECHANISM PROBE (factor-derived, DIAGNOSTIC ONLY, not an N-only cell) ---
# Fermat hit distance d = m - isqrt(N).  E(a)=a^2-N crosses zero at j=d: if the
# zero falls inside the FFT window it reshapes the spectrum.  Probe whether the
# b1 information carried by F1 tracks hit-in-window geometry.
d_fermat = M - np.array([math.isqrt(int(v)) for v in P * Q], dtype=np.int64)
mech = {}
for W in WINDOWS:
    hin = (d_fermat < W)
    rates = [float(hin[b1 == k].mean()) for k in (1, 2, 3)]
    I_h, mu_h, sd_h, z_h = perm_test(hin.astype(np.int64), b1z)
    mech[f"W{W}"] = {"hit_in_window_rate_by_b1": {str(k): round(v, 4) for k, v in zip((1, 2, 3), rates)},
                     "I_hit_b1": round(I_h, 4), "z": round(z_h, 3)}
r_dB_d = float(np.corrcoef(np.log1p(dB), np.log1p(np.maximum(d_fermat, 0)))[0, 1])
log(f"[mech] Fermat-hit-in-window rate by b1 (factor-derived diagnostic): "
    + "; ".join(f"W{W}: " + str(mech[f'W{W}']['hit_in_window_rate_by_b1']) for W in WINDOWS))
log(f"[mech] I(hit_in_window@4096 ; b1)={mech['W4096']['I_hit_b1']} z={mech['W4096']['z']}; "
    f"corr(log dB, log d_fermat)={r_dB_d:+.3f}")

t_stats = time.time() - TS

# ---------------------------------------------------------------------------
# VERDICT (computed from data, never hardcoded)
# ---------------------------------------------------------------------------
nonly_cells = [c for c in cells if c["role"] == "nonly"]
flagged = [c for c in nonly_cells if c["flag_z3"]]
gated_pass = [c for c in flagged if c.get("oos", {}).get("pass", False)]
signal = len(gated_pass) > 0
verdict = "ENERGY-ASCENT-SIGNAL" if signal else "ENERGY-ASCENT-NULL"
h1_all_b1_null = all(not c["flag_z3"] for c in nonly_cells if c["target"] == "b1")
best = max(nonly_cells, key=lambda c: c["z"])
mult_expect = len(nonly_cells) * 0.0013498980316301035  # P(one-sided Z>=3)

log("\n================ DIGEST ================")
log(f"VERDICT: {verdict}")
log(f"H1 (no N-only feature beats null on b1): {'CONFIRMED' if h1_all_b1_null else 'REFUTED'}")
log(f"flagged z>={FLAGZ} N-only cells: {len(flagged)} / {len(nonly_cells)} "
    f"(multiplicity: expected-by-chance ~= {mult_expect:.2f}); OOS-passed: {len(gated_pass)}")
for c in flagged:
    o = c.get("oos")
    extra = (f" OOS acc={o['acc']} CI95=[{o['ci95'][0]},{o['ci95'][1]}] chance={round(o['chance'],3)} "
             f"pass={o['pass']} | majority_base={o['majority_baseline']} beats_maj={o['beats_majority_ptest']}") if o else ""
    log(f"  FLAG {c['feature']} x {c['target']}: I={c['I']} z={c['z']}{extra}")
log(f"BEST N-only cell overall: {best['feature']} x {best['target']} "
    f"I={best['I']} z={best['z']}")
log(f"CONTROLS: positive band->b1 {'PASS' if pos_pass else 'FAIL'} "
    f"(match {match_rate:.4f}); negative mod3^k {'PASS' if neg_pass else 'FAIL'} (worst z={neg_worst_z:+.2f})")
log(f"POPULATION: n={NP_} (3 strata x {NS}); dB mean={dB.mean():.2f} median={np.median(dB):.0f} "
    f"range=[{dB.min()},{dB.max()}]")
log(f"RUNTIME: total={time.time()-T0:.0f}s (gen {t_gen:.0f} | descend {t_desc:.0f} | "
    f"features {t_feat:.0f} | stats {t_stats:.0f})")
log("LEDGER:")
for entry in LEDGER:
    log(f"  - {entry}")

result = {
    "exp_id": 546,
    "name": "ENERGY-ASCENT-ORACLE",
    "date": "2026-08-23",
    "seed": SEED,
    "question": "does any cheap energy spectrum computed from N alone predict Berggren branch letters?",
    "convention": {"b1": "first descent step FROM THE NODE (deepest-edge letter; paper-81 convention)",
                   "broot1": "root-side first letter (extra target)",
                   "descent_order": "letters collected node->root"},
    "config": {"n_per_stratum": NS, "strata": STRATA, "windows": list(WINDOWS),
               "gauss_moduli": list(GAUSS_MODULI), "nbins": NBINS,
               "perms": NPERM, "flag_z": FLAGZ,
               "p_range": [2**14, 2**18], "q_range": [2**16, 2**22]},
    "population_stats": {
        "n": int(NP_), "dB_mean": round(float(dB.mean()), 2),
        "dB_median": float(np.median(dB)), "dB_min": int(dB.min()), "dB_max": int(dB.max()),
        "per_stratum": {s: {"n": int((STRAT == s).sum()),
                            "dB_mean": round(float(dB[STRAT == s].mean()), 2),
                            "dB_median": float(np.median(dB[STRAT == s])),
                            "dB_max": int(dB[STRAT == s].max()),
                            "rho_min": round(float((M[STRAT == s] / Nn[STRAT == s]).min()), 4),
                            "rho_max": round(float((M[STRAT == s] / Nn[STRAT == s]).max()), 2)}
                       for s in STRATA},
        "b1_counts": np.bincount(b1, minlength=4)[1:].tolist(),
        "depth_ge2": int(mask_d2.sum()),
    },
    "pipeline_check": {"ascent_matches": f"{asc_ok}/{NP_}", "pass": asc_ok == NP_,
                       "fermat_identity": True, "per_step_childmap": True},
    "controls": {"positive_band_to_b1": {"match_rate": match_rate, "I": round(I_band, 6),
                                          "H_b1": round(Hb1, 6), "pass": bool(pos_pass)},
                 "negative_mod3k_worst_z": round(neg_worst_z, 3), "pass": bool(neg_pass)},
    "mechanism_probe": {"note": "factor-derived DIAGNOSTIC ONLY (not an N-only cell); "
                                "d_fermat = m - isqrt(N) is where E(a) crosses zero",
                        "fermat_hit_in_window": mech,
                        "corr_logdB_logd": round(r_dB_d, 4)},
    "verdict": {"name": verdict,
                "rule": "SIGNAL iff some N-only cell z>=3 AND OOS Wilson95-low > chance",
                "h1_all_b1_cells_null": bool(h1_all_b1_null),
                "n_flagged": len(flagged), "n_oos_passed": len(gated_pass),
                "multiplicity_expected_false_at_z3": round(mult_expect, 2),
                "basis": "computed from data"},
    "best_cell": best,
    "flagged_cells": flagged,
    "cells": cells,
    "timing_s": {"total": round(time.time() - T0, 1), "gen": round(t_gen, 1),
                  "descend": round(t_desc, 1), "features": round(t_feat, 1),
                  "stats": round(t_stats, 1)},
    "ledger": LEDGER,
}
outpath = f"{args.outdir}/exp546_result.json"
with open(outpath, "w") as fh:
    json.dump(result, fh, indent=1)
np.savez_compressed(f"{args.outdir}/exp546_data.npz",
                    P=P, Q=Q, stratum=STRAT, dB=dB, b1=b1, broot1=broot1,
                    joint12=joint12, comp=comp, band=band,
                    **{f"x_{k}": v for k, v in X.items()})
log(f"\nwrote {outpath} and exp546_data.npz")

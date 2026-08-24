#!/usr/bin/env python3
# =============================================================================
# exp549 WINDOW-FRONTIER  (2026-08-24, seed 20260824)
#
# QUESTION: at a FIXED probe budget B (#evaluations of a^2 - N, the only real
# cost), what is the maximal MI(feature-set ; b1) achievable by N-computable
# window placement/content, and what does the bits-per-probe frontier look
# like?
#
# BACKGROUND (exp546, recorded this session): the magnitude spectrum of
# E(a)=a^2-N on the isqrt-anchored window W=4096 carries MI ~= 0.184 bits
# about the first Berggren branch letter b1 (permutation z ~= 110; survives
# within-log-n-bin shuffles z ~= 100).  exp546's mechanism note said "E(a)
# crosses zero at j=d=m-isqrt(N)" and measured the FACTOR-DERIVED indicator
# I(1{d<W}; b1) = 0.3035 bits at W=4096.
#
# CORRECTION CAUGHT BY THIS EXPERIMENT'S PIPELINE CHECKS (ledger L9):
#   E(a)=a^2-N crosses ZERO at a=sqrt(N), i.e. between j=0 and j=1 of ANY
#   isqrt-anchored window -- E(isqrt)<0 and E(isqrt+1)=(isqrt+1)^2-N>0 hold
#   for EVERY N (N-isqrt^2 <= 2*isqrt).  What sits at a=m (step d) is the
#   FERMAT HIT: a^2-N = n^2 becomes a perfect square.  exp546's wording
#   conflated zero-crossing with Fermat hit; its 0.3035-bit figure is an
#   ORACLE bound carried by the factor-derived indicator 1{d<=W}, which NO
#   isqrt-anchored SIGN probe can realize: the sign pattern of any anchored
#   window is fixed up to frac(sqrt(N)) in [0,1), so sign-count/bracket
#   features are STRUCTURALLY d-BLIND.  d can enter N-only features only
#   through magnitudes (chirp slope ~2*isqrt, offset r=N-isqrt^2).
#   This experiment keeps ALL specified sign features and lets the data show
#   the gap (probe-layer exactness asserts below PROVE the constancy).
#
# DESIGNS (ALL disclosed; budget = parabola probes ONLY):
#   D1  contiguous isqrt-anchored ramp   j = 0..B-1             (exp546 baseline)
#   D1b centered variant                 j = -B/2 .. B/2-1
#   D2  log-spaced probes                STRICT integer-geometric grid on
#        [0, JMAX], JMAX = 2^21 PRE-STATED (covers d <=~ n/2 <= 2^20.5 for the
#        q-range; not tuned on outcomes).  Grid strictly increasing (rounded
#        geometric; collisions forced +1; disclosed).
#   D3  strided/decimated ramp           j = 0,64,...,64*(B-1)  (stride 64 ->
#        coverage 64B; task-text reading disclosed as ledger L1)
#   D4  multi-window                     4 sub-windows of B/4 probes at
#        isqrt + {0, B, 4B, 16B}, concatenated into one length-B sequence
#
# FEATURES per (design, B) -- ALL disclosed, no cherry-picking:
#   hits      # probes with a^2 < N (monotone ramps: = censored d)
#   bracket   window contains the zero crossing (min E < 0 < max E);
#             this is the exp546 "exact zero-crossing bracket indicator"
#   flippos   linear-interpolated zero-crossing position / (B-1),
#             sentinel 1.0 if crossing at/after window end, 0.0 if before
#   spec_s_*  exp546 spectral set on CENTERED SIGNED E (ent, cent, p1, p2,
#             hratio, third_lo/mid/hi, slope)
#   spec_a_*  the same spectral set on CENTERED |E|
#
# STATISTICS (binding lab lessons): MI in bits; quantile bins <=12 for
#   continuous/count features (bracket kept at NATURAL cardinality 2);
#   permutation nulls x200: (i) POOLED row shuffle, (ii) WITHIN-LOG-N-BIN
#   shuffle (8 quantile bins of log N -- size-stratified control; labels
#   permuted within bins).  Every tested cell reported.
#
# PRE-STATED VERDICT RULES (strings COMPUTED from data, never hardcoded):
#   R1 shape:     FRONTIER-MONOTONE-IN-B iff for every ladder step
#                 maxcellMI(B_{k+1}) >= maxcellMI(B_k) - 2*null_sd(at B_k);
#                 else FRONTIER-SATURATING.
#   R2 hit role:  HIT-DOMINANT iff I(bracket;b1) >= 0.9 * maxcellMI at >=3 of
#                 4 budgets; else SPECTRAL-COMPETITIVE.
#   R3 saturate:  B* = smallest oracle-grid B with I(1{d<=B};b1) >= 0.9 * max
#                 over grid (oracle = factor-derived diagnostic, not a cell).
#   R4 approach:  ratio maxcellMI(B=4096) / I_oracle(1{d<=4096};b1).
#
# PIPELINE CHECKS (abort on failure): Fermat identity m^2-n^2==pq; per-step
#   child-map reconstruction during descent; reversed-string re-ascent lands
#   on (m,n) for 100% of nodes; rho-band == b1; PROBE-LAYER EXACTNESS
#   (structural, proves the header CORRECTION):
#       hits == 1 for D1/D2/D3/D4  and  hits == B/2+1 for D1b   (every sample:
#       the sign flip lies strictly between the first two probes);
#       E[:,0] < 0 < E[:,1] (straddle) for every design;
#       flippos*(B-1) == (array index of j=0) + frac(sqrt(N)) to 1e-6;
#   plus strict monotonicity of E along every ramp and probe count == B.
#
# LEDGER (disclosures):
#   L1: task text "every k-th point of a long ramp (k=B coverage 64B)" read as
#       stride 64 -> coverage 64B (B probes spanning 64x their count).
#   L2: D2 grid strictly-increasing rounded geometric; JMAX=2^21 pre-stated.
#   L3: D4 spectra computed on the CONCATENATED length-B sequence; the four
#       sub-windows differ hugely in magnitude and sub-window boundary
#       discontinuities enter the FFT (inherent to the design).
#   L4: budget counts PARABOLA EVALUATIONS ONLY (matches exp546 accounting);
#       FFT/summary compute is not counted as probe cost.
#   L5: bracket := (min E < 0 < max E) over the probe window; for anchored
#       monotone designs this equals 0 < d < coverage.
#   L6: fresh population seed 20260824 (exp546 drew 20260823): comparisons to
#       exp546 numbers are qualitative replications, not paired samples.
#   L7: targets 'dbq' (tree-depth quartile) and 'joint12' are FACTOR-DERIVED
#       (tree descent) -- used as targets only, never claimed as N-only.
#   L8: flippos sentinels: 1.0 = crossing at/after window end, 0.0 = before
#       window start (both unreachable for anchored designs; see L9).
#   L9 (exp549 CATCH): E(a)=a^2-N crosses zero at sqrt(N) -- between j=0 and
#       j=1 of any isqrt-anchored window -- NOT at a=m.  The Fermat hit
#       (a^2-N a perfect square) is at a=m.  exp546's mechanism wording
#       conflated the two; I(1{d<=W};b1)=0.3035 is a factor-derived ORACLE
#       bound.  Probe-layer exactness asserts PROVE anchored sign-count
#       sensors are constant (d-blind).  All specified sign features are kept
#       and reported (no cherry-picking); the D1 hits==clip(d,B) check this
#       experiment was drafted with FAILED in smoke and was replaced by the
#       structural identities above.
#   L10: many spectral summaries are strictly-monotone transforms of one
#       latent scalar per window, so their <=12 quantile bins coincide and
#       their MI values are EXACTLY equal (exp546 showed the same: all f1
#       cells I=0.183601 at both W).  'Best' selection therefore uses the
#       pre-stated deterministic tie-break (max I, then max z_pooled, then
#       lexicographic feature name); z differences among tied-I cells are
#       null noise, not signal.
# =============================================================================
import argparse, json, math, os, random, sys, time
import numpy as np
from sympy import isprime

T0 = time.time()
SEED = 20260824
MAX_STEPS = 2_000_000
BUDGETS = (64, 256, 1024, 4096)
DESIGNS = ('D1', 'D1b', 'D2', 'D3', 'D4')
JMAX_D2 = 2 ** 21          # pre-stated (ledger L2)
STRIDE_D3 = 64             # ledger L1
OFFSETS_D4 = (0, 1, 4, 16)  # x B
NBINS = 12
NPERM_DEFAULT = 200
FLAGZ = 3.0

ap = argparse.ArgumentParser()
ap.add_argument('--n-stratum', type=int, default=1000)
ap.add_argument('--perms', type=int, default=NPERM_DEFAULT)
ap.add_argument('--outdir', type=str,
                default='/home/raver1975/factor3/ResearchOutput/scripts/2026-08-21-resume')
args = ap.parse_args()
NS = args.n_stratum
NPERM = args.perms

rng = random.Random(SEED)                    # python RNG: population draws
rng_perm = np.random.default_rng(SEED + 1)   # permutation nulls

LEDGER = [
    "L1: D3 task text '(k=B coverage 64B)' read as stride 64 -> coverage 64B.",
    "L2: D2 grid strictly-increasing rounded geometric; JMAX=2^21 pre-stated "
    "from the q-range (d <=~ n/2 <= 2^20.5), not tuned on outcomes.",
    "L3: D4 spectra computed on the CONCATENATED length-B sequence; sub-window "
    "boundary discontinuities enter the FFT (inherent to the design).",
    "L4: budget = parabola evaluations only; FFT/summary compute uncounted "
    "(exp546 accounting).",
    "L5: bracket := (min E < 0 < max E); for anchored monotone windows equals "
    "0 < d < coverage.",
    "L6: fresh seed 20260824 vs exp546's 20260823 -- qualitative replication.",
    "L7: dbq/joint12 targets are factor-derived (tree descent), never N-only.",
    "L8: flippos sentinels 1.0 (crossing at/after window) / 0.0 (before).",
]


def log(msg):
    print(msg, flush=True)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def rand_prime(lo, hi):
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
    """node->root letters via parent-interval law (integer compares),
    per-step child-map reconstruction asserted."""
    L = []
    steps = 0
    while not (m == 2 and n == 1):
        steps += 1
        if steps > MAX_STEPS:
            raise RuntimeError(f"descent exceeded {MAX_STEPS} steps at ({m},{n})")
        if m < 2 * n:      # rho in (1,2) -> letter 1, parent (n, 2n-m)
            letter, pm, pn = 1, n, 2 * n - m
        elif m < 3 * n:    # rho in (2,3) -> letter 2, parent (n, m-2n)
            letter, pm, pn = 2, n, m - 2 * n
        else:              # rho > 3 -> letter 3, parent (m-2n, n)
            letter, pm, pn = 3, m - 2 * n, n
        if letter == 1:
            ok = (2 * pm - pn, pm) == (m, n)
        elif letter == 2:
            ok = (2 * pm + pn, pm) == (m, n)
        else:
            ok = (pm + 2 * pn, pn) == (m, n)
        if not ok:
            raise RuntimeError(f"child-map reconstruction failed at ({m},{n})")
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


def geom_grid(B, jmax):
    """strictly increasing rounded-geometric integer grid, B points, g[0]=0,
    g[-1] ~= jmax (ledger L2)."""
    g = [0]
    for t in range(1, B):
        v = math.exp(math.log(jmax) * (t - 1) / max(1, B - 2))
        nxt = max(int(round(v)), g[-1] + 1)
        g.append(nxt)
    return np.array(g, dtype=np.int64)


def spectrum_summaries(x, W, prefix):
    """exp546 spectral set verbatim."""
    xc = x - x.mean(axis=1, keepdims=True)
    F = np.fft.rfft(xc, axis=1)
    Pw = np.abs(F) ** 2
    s = Pw.sum(axis=1, keepdims=True)
    Pn = np.divide(Pw, s, out=np.zeros_like(Pw), where=s > 0)
    f = np.arange(Pn.shape[1])
    nz = slice(1, None)
    Pf = Pn[:, nz]
    Ps = Pf.sum(axis=1)
    ent = -(Pf * np.log2(Pf + 1e-300)).sum(axis=1)
    cent = (f[nz][None, :] * Pf).sum(axis=1) / np.maximum(Ps, 1e-300)
    order = np.argsort(-Pf, axis=1)
    rows = np.arange(len(x))
    p1 = f[nz][order[:, 0]] / W
    p2 = f[nz][order[:, 1]] / W
    hr = Pf[rows, order[:, 0]] / (Pf[rows, order[:, 1]] + 1e-300)
    ent = ent.ravel(); cent = cent.ravel(); p1 = np.atleast_1d(p1)
    p2 = np.atleast_1d(p2); hr = np.atleast_1d(hr).ravel()
    K = Pn.shape[1] - 1
    lo = Pn[:, 1:K // 3 + 1].sum(axis=1)
    mid = Pn[:, K // 3 + 1:2 * K // 3 + 1].sum(axis=1)
    hi = Pn[:, 2 * K // 3 + 1:].sum(axis=1)
    A = np.vstack([f[nz], np.ones(K)]).T
    slope = np.empty(len(x))
    lg = np.log2(Pf + 1e-300)
    coef, *_ = np.linalg.lstsq(A, lg.T, rcond=None)
    slope = coef[0]
    return {f"{prefix}_ent": ent, f"{prefix}_cent": cent,
            f"{prefix}_p1": p1, f"{prefix}_p2": p2, f"{prefix}_hratio": hr,
            f"{prefix}_third_lo": lo, f"{prefix}_third_mid": mid,
            f"{prefix}_third_hi": hi, f"{prefix}_slope": slope}


# ---------------------------------------------------------------------------
# population: 3 strata x NS  (indep-uniform / uniform-log / ratio-stratified)
# ---------------------------------------------------------------------------
log(f"=== exp549 WINDOW-FRONTIER ===")
log(f"config: NS/stratum={NS} (x3 strata), perms={NPERM}, budgets={list(BUDGETS)}, "
    f"designs={list(DESIGNS)}, bins<={NBINS}, seed={SEED}")

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

# ---------------------------------------------------------------------------
# Fermat pairs + tree descent + pipeline checks
# ---------------------------------------------------------------------------
TD = time.time()
M = (P + Q) // 2
Nn = (Q - P) // 2
fermat_ok = bool(np.all(M.astype(object) ** 2 - Nn.astype(object) ** 2
                        == P.astype(object) * Q.astype(object)))
assert fermat_ok, "Fermat identity broken"
letters_list = []
for i in range(NP_):
    letters_list.append(descend(int(M[i]), int(Nn[i])))

asc_ok = sum(1 for i in range(NP_)
             if ascend(letters_list[i]) == (int(M[i]), int(Nn[i])))
log(f"[pipeline] reversed-string ascent matches: {asc_ok}/{NP_}")
if asc_ok != NP_:
    log("PIPELINE CHECK FAILED -- ABORTING")
    sys.exit(1)

dB = np.array([len(L) for L in letters_list], dtype=np.int64)
b1 = np.array([L[0] for L in letters_list], dtype=np.int64)   # deepest-edge letter
mask_d2 = dB >= 2
joint12 = np.full(NP_, -1, dtype=np.int64)
joint12[mask_d2] = np.array([(L[0] - 1) * 3 + (L[1] - 1)
                             for L in letters_list if len(L) >= 2])

band = np.where(M < 2 * Nn, 1, np.where(M < 3 * Nn, 2, 3)).astype(np.int64)
assert np.array_equal(band, b1), "band!=b1: descent law inconsistent"

# Fermat distance d = m - isqrt(N): where E(a) crosses zero (factor-derived)
d_fermat = M - np.array([math.isqrt(int(P[i]) * int(Q[i])) for i in range(NP_)],
                        dtype=np.int64)
assert np.all(d_fermat >= 1), "d must be >=1 (N not a perfect square)"

dq = np.quantile(d_fermat.astype(float), [0.05, 0.25, 0.5, 0.75, 0.9, 0.99])
log(f"[pop] d_fermat: mean={d_fermat.mean():.1f} median={np.median(d_fermat):.0f} "
    f"q05={dq[0]:.0f} q25={dq[1]:.0f} q75={dq[3]:.0f} q90={dq[4]:.0f} q99={dq[5]:.0f} "
    f"max={d_fermat.max()}")
log(f"[pop] dB(tree depth): mean={dB.mean():.1f} median={np.median(dB):.0f} "
    f"range=[{dB.min()},{dB.max()}]")
log(f"[pop] b1 dist: {np.bincount(b1, minlength=4)[1:].tolist()}")
t_desc = time.time() - TD

# ---------------------------------------------------------------------------
# ORACLE (factor-derived DIAGNOSTIC, not an N-only cell):
# I(1{d<=B}; b1) fine grid + ladder, hit rates by letter, Fermat fractions
# ---------------------------------------------------------------------------
TO = time.time()
b1z = b1 - 1
Nall64 = P * Q                                   # < 2^41: int64-exact
logN = np.log(Nall64.astype(float))              # lossless enough for 8-bin cut
logn_bins = np.searchsorted(
    np.unique(np.quantile(logN, np.linspace(0, 1, 9)[1:-1])), logN, side='right')
assert logn_bins.min() == 0 and logn_bins.max() == 7


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


def dual_perm_test(xb, yb, binid, nperm=NPERM):
    """observed MI + pooled-row-shuffle null AND within-log-n-bin-shuffle null."""
    n = len(yb)
    K = int(xb.max()) + 1
    C = int(yb.max()) + 1
    obs = mi_bits(xb, yb, K, C)
    nul_p = np.empty(nperm); nul_w = np.empty(nperm)
    for i in range(nperm):
        nul_p[i] = mi_bits(xb, yb[rng_perm.permutation(n)], K, C)
        yw = yb.copy()
        for b in np.unique(binid):
            idx = np.flatnonzero(binid == b)
            if len(idx) > 1:
                yw[idx] = yb[idx[rng_perm.permutation(len(idx))]]
        nul_w[i] = mi_bits(xb, yw, K, C)
    mp, sp = float(nul_p.mean()), float(nul_p.std(ddof=0) + 1e-12)
    mw, sw = float(nul_w.mean()), float(nul_w.std(ddof=0) + 1e-12)
    return obs, mp, sp, (obs - mp) / sp, mw, sw, (obs - mw) / sw


def bin_quantile(x, nbins=NBINS):
    qs = np.linspace(0, 1, nbins + 1)[1:-1]
    edges = np.unique(np.quantile(x, qs))
    return np.searchsorted(edges, x, side='right'), len(edges) + 1


oracle_grid_Bs = sorted(set(int(round(v)) for v in
                            np.logspace(np.log2(8), np.log2(2 ** 22), 57)))
oracle_fine = []
for B in oracle_grid_Bs:
    hin = (d_fermat <= B).astype(np.int64)
    I_o = mi_bits(hin, b1z, 2, 3)
    oracle_fine.append({"B": int(B), "I_oracle": round(I_o, 6),
                        "hit_rate": round(float(hin.mean()), 4)})
oracle_ladder = {}
for B in BUDGETS:
    hin = (d_fermat <= B).astype(np.int64)
    rates = [float(hin[b1 == k].mean()) for k in (1, 2, 3)]
    xb = hin  # natural binary
    I_o, mp, sp, zp, mw, sw, zw = dual_perm_test(xb, b1z, logn_bins)
    oracle_ladder[str(B)] = {
        "I_oracle": round(I_o, 6), "z_pooled": round(zp, 3), "z_within": round(zw, 3),
        "hit_rate_by_letter": {str(k): round(v, 4) for k, v in zip((1, 2, 3), rates)},
        "coverage_P(d<=B)": round(float(hin.mean()), 4)}
    log(f"[oracle] B={B}: I(1{{d<=B}};b1)={I_o:.4f} zp={zp:+.1f} zw={zw:+.1f} "
        f"rates={[round(r, 3) for r in rates]} cov={hin.mean():.3f}")
Io = np.array([r["I_oracle"] for r in oracle_fine])
Bs_ = np.array([r["B"] for r in oracle_fine])
Imax_o = float(Io.max())
sat_idx = int(np.flatnonzero(Io >= 0.9 * Imax_o)[0])
BSTAR = int(Bs_[sat_idx])
log(f"[oracle] max I={Imax_o:.4f} at B={int(Bs_[int(np.argmax(Io))])}; "
    f"0.9-saturation B*={BSTAR}")
t_oracle = time.time() - TO

# ---------------------------------------------------------------------------
# PROBE DESIGNS x BUDGETS -> features
# ---------------------------------------------------------------------------
TF = time.time()
Nall64 = P * Q                                    # < 2^41: int64-exact
a0_arr = np.array([math.isqrt(int(v)) for v in Nall64], dtype=np.int64)
a0f = a0_arr.astype(np.float64)
r_o = (Nall64 - a0_arr * a0_arr).astype(np.float64)   # r = N - isqrt^2 = -E(isqrt)
FEATS_BY_DB = {}   # (design, B) -> {featname: np.array}
PROBE_CHK = {}

for des in DESIGNS:
    for B in BUDGETS:
        if des == 'D1':
            J = np.arange(B, dtype=np.int64)
        elif des == 'D1b':
            J = np.arange(-(B // 2), -(B // 2) + B, dtype=np.int64)
        elif des == 'D2':
            J = geom_grid(B, JMAX_D2)
        elif des == 'D3':
            J = np.arange(B, dtype=np.int64) * STRIDE_D3
        else:  # D4
            parts = []
            for om in OFFSETS_D4:
                o = om * B
                parts.append(o + np.arange(B // 4, dtype=np.int64))
            J = np.concatenate(parts)
        assert len(J) == B, f"probe count != B for {des}@{B}"
        if des != 'D4':
            assert np.all(np.diff(J) > 0), f"grid not strictly increasing {des}@{B}"

        A = a0_arr[:, None] + J[None, :]
        E = A * A - Nall64[:, None]
        if des != 'D4':
            mono_ok = bool(np.all(E[:, :-1] < E[:, 1:]))
        else:
            mono_ok = bool(np.all(np.diff(E.reshape(NP_, 4, B // 4), axis=2) > 0))
        assert mono_ok, f"E not monotone along ramps {des}@{B}"
        Ef = E.astype(np.float64)     # lossless: |E| < 2^53

        hits = (Ef < 0).sum(axis=1).astype(np.int64)
        bracket = ((Ef.min(axis=1) < 0) & (Ef.max(axis=1) > 0)).astype(np.int64)
        # interpolated crossing position, in j-units, normalized to [0,1] over
        # the grid span (design-generic: uses the local probe spacing)
        i0 = np.clip(hits - 1, 0, B - 2)
        rows = np.arange(NP_)
        E0v = Ef[rows, i0]; E1v = Ef[rows, i0 + 1]
        hstep = (J[i0 + 1] - J[i0]).astype(np.float64)
        root_j = J[i0].astype(np.float64) + hstep * (-E0v) / (E1v - E0v)
        span = float(J[-1] - J[0])
        flippos = np.where(hits >= B, 1.0,
                           np.where(hits <= 0, 0.0,
                                    (root_j - float(J[0])) / span))

        # ---- PROBE-LAYER EXACTNESS CHECKS (structural; header CORRECTION/L9):
        # the sign flip lies strictly between the first two probes of EVERY
        # anchored window for EVERY sample -> sign-count sensors are constant.
        if des == 'D1b':
            idx0 = B // 2                       # array index of probe j=0
            chk_hits = bool(np.all(hits == idx0 + 1))
        else:
            idx0 = 0
            chk_hits = bool(np.all(hits == 1))
        chk_straddle = bool(np.all(bracket == 1))   # every window brackets the zero
        # D1 has unit spacing: interpolated crossing must equal r/(2*isqrt+1)
        if des == 'D1':
            xi = r_o / (2.0 * a0f + 1.0)
            chk_flip = bool(np.max(np.abs(flippos * (B - 1) - xi)) < 1e-6)
        else:
            chk_flip = bool(np.all((flippos > 0.0) & (flippos < 1.0)))
        chk = chk_hits and chk_straddle and chk_flip
        PROBE_CHK[f"{des}@{B}"] = {"hits_constant": chk_hits,
                                   "brackets_zero_all_rows": chk_straddle,
                                   "flip_interior": chk_flip,
                                   "monotone": mono_ok}
        if not chk:
            log(f"PROBE-LAYER EXACTNESS FAILED for {des}@{B} "
                f"(hits_const={chk_hits} straddle={chk_straddle} "
                f"flip={chk_flip}) -- ABORTING")
            sys.exit(1)

        feats = {"hits": hits.astype(np.float64), "bracket": bracket.astype(np.float64),
                 "flippos": flippos}
        feats.update(spectrum_summaries(Ef, B, "spec_s"))
        feats.update(spectrum_summaries(np.abs(Ef), B, "spec_a"))
        FEATS_BY_DB[(des, B)] = feats
        log(f"[probes] {des}@{B}: bracket rate={bracket.mean():.3f} "
            f"hits med={np.median(hits):.0f} (exactness OK)")
    del A, E, Ef
t_feat = time.time() - TF
log(f"[features] {len(FEATS_BY_DB)} (design,budget) blocks in {t_feat:.1f}s")

# ---------------------------------------------------------------------------
# STATS: every (design x B x feature) cell on b1, dual permutation nulls
# ---------------------------------------------------------------------------
TS = time.time()
cells = []
FNAMES = list(next(iter(FEATS_BY_DB.values())).keys())
for des in DESIGNS:
    for B in BUDGETS:
        feats = FEATS_BY_DB[(des, B)]
        for fname in FNAMES:
            x = feats[fname]
            if fname == "bracket":
                xb, K = x.astype(np.int64), 2       # natural cardinality (L5)
            else:
                xb, K = bin_quantile(x)
            I, mp, sp, zp, mw, sw, zw = dual_perm_test(xb, b1z, logn_bins)
            cells.append({"design": des, "budget": int(B), "feature": fname,
                          "target": "b1", "n": int(NP_), "bins": int(K),
                          "I": round(I, 6),
                          "null_mean_pooled": round(mp, 6), "null_sd_pooled": round(sp, 6),
                          "z_pooled": round(zp, 3),
                          "null_mean_within": round(mw, 6), "null_sd_within": round(sw, 6),
                          "z_within": round(zw, 3),
                          "flag_z3": bool(zp >= FLAGZ and zw >= FLAGZ)})
    done = DESIGNS.index(des) + 1
    log(f"[stats] {done}/{len(DESIGNS)} designs x {len(BUDGETS)} budgets x "
        f"{len(FNAMES)} features done ({time.time()-TS:.0f}s)")

# best DESIGN per budget (by z_pooled on b1, max over its features)
best_per_B = {}
for B in BUDGETS:
    bc = [c for c in cells if c["budget"] == B and c["target"] == "b1"]
    # pre-stated deterministic tie-break: max I, then max z_pooled, then
    # lexicographic feature name (ledger L10)
    top = max(bc, key=lambda c: (c["I"], c["z_pooled"], c["feature"]))
    best_des = top["design"]
    best_per_B[B] = {"design": best_des, "feature": top["feature"],
                     "I": top["I"], "z_pooled": top["z_pooled"],
                     "z_within": top["z_within"]}
    # extra targets (factor-derived; L7) for the WHOLE winning design
    extras = {}
    feats = FEATS_BY_DB[(best_des, B)]
    for tname, yarr, ymask in (("joint12", joint12[mask_d2], mask_d2),
                               ("dbq", None, None)):
        if tname == "dbq":
            qs_db = np.unique(np.quantile(dB.astype(float),
                                          np.linspace(0, 1, 5)[1:-1]))
            yarr = np.searchsorted(qs_db, dB.astype(float), side='right')
            ymask = np.ones(NP_, dtype=bool)
        tbest = None
        for fname in FNAMES:
            x = feats[fname]
            if fname == "bracket":
                xb, K = x.astype(np.int64), 2
            else:
                xb, K = bin_quantile(x)
            I, mp, sp, zp, mw, sw, zw = dual_perm_test(xb[ymask], yarr, logn_bins[ymask])
            rec = {"feature": fname, "I": round(I, 6), "z_pooled": round(zp, 3),
                   "z_within": round(zw, 3)}
            if tbest is None or (rec["I"], rec["z_pooled"], rec["feature"]) > \
                    (tbest["I"], tbest["z_pooled"], tbest["feature"]):
                tbest = rec
        extras[tname] = tbest
    best_per_B[B]["extras"] = extras
    log(f"[best@{B}] design={best_des} feat={top['feature']} I={top['I']} "
        f"zp={top['z_pooled']:+.1f} zw={top['z_within']:+.1f} | "
        f"joint12 best I={extras['joint12']['I']} | dbq best I={extras['dbq']['I']}")

# ---------------------------------------------------------------------------
# VERDICT (computed from data; rules R1-R4 pre-stated in header)
# ---------------------------------------------------------------------------
b1_cells = [c for c in cells if c["target"] == "b1"]
maxI = {}; maxcell = {}
for B in BUDGETS:
    bc = [c for c in b1_cells if c["budget"] == B]
    top = max(bc, key=lambda c: (c["I"], c["z_pooled"], c["feature"]))
    maxI[B] = top["I"]; maxcell[B] = top

mono = True
for k in range(len(BUDGETS) - 1):
    Bk, Bk1 = BUDGETS[k], BUDGETS[k + 1]
    sd_ref = maxcell[Bk]["null_sd_pooled"]
    if maxI[Bk1] < maxI[Bk] - 2 * sd_ref:
        mono = False
shape = "FRONTIER-MONOTONE-IN-B" if mono else "FRONTIER-SATURATING"

hit_dom_count = 0
hit_role_cells = {}
for B in BUDGETS:
    bc = [c for c in b1_cells if c["budget"] == B and c["feature"] == "bracket"]
    ib = max(c["I"] for c in bc)
    frac = ib / maxI[B] if maxI[B] > 0 else 0.0
    hit_role_cells[B] = {"I_bracket_best": round(ib, 6),
                         "frac_of_max": round(frac, 4)}
    if frac >= 0.9:
        hit_dom_count += 1
hitrole = "HIT-DOMINANT" if hit_dom_count >= 3 else "SPECTRAL-COMPETITIVE"
verdict_name = f"WINDOW-FRONTIER-{shape.split('FRONTIER-')[1]}-{hitrole}"
I_orc_4096 = oracle_ladder["4096"]["I_oracle"]
approach_ratio = round(maxI[4096] / I_orc_4096, 4) if I_orc_4096 > 0 else None

bpp = [{"B": int(B), "max_I": round(maxI[B], 6),
        "bits_per_probe": float(f"{maxI[B]/B:.3e}"),
        "winning_design": maxcell[B]["design"],
        "winning_feature": maxcell[B]["feature"]} for B in BUDGETS]

scan_mean = float(d_fermat.mean()) + 1.0   # full Fermat scan: isqrt..m inclusive
fermat_fraction = [{"B": int(B), "fraction_of_full_scan": round(B / scan_mean, 6),
                    "coverage_P(d<=B)": oracle_ladder[str(B)]["coverage_P(d<=B)"]}
                   for B in BUDGETS]

log("\n================ DIGEST ================")
log(f"VERDICT: {verdict_name}")
log(f"R1 shape: {shape}")
log(f"R2 hit role: {hitrole} (bracket>=90% of max at {hit_dom_count}/4 budgets)")
log(f"R3 hit-detection saturation B*={BSTAR} (oracle max I={Imax_o:.4f} "
    f"@B={int(Bs_[int(np.argmax(Io))])})")
log(f"R4 maxcellMI(4096)={maxI[4096]:.4f} vs oracle I(1{{d<=4096}})={I_orc_4096:.4f} "
    f"-> ratio {approach_ratio}")
log("BITS-PER-PROBE: " + "; ".join(f"B={r['B']}: {r['bits_per_probe']:.2e} "
                                   f"({r['winning_design']}/{r['winning_feature']})"
                                   for r in bpp))
log(f"FERMAT FRACTION: full scan E[steps]={scan_mean:.1f}; " +
    "; ".join(f"B={r['B']}: {r['fraction_of_full_scan']*100:.2g}% "
              f"(cov {r['coverage_P(d<=B)']*100:.1f}%)" for r in fermat_fraction))
log(f"d_fermat quantiles [5,25,50,75,90,99]%: {[round(float(v),1) for v in dq]}; "
    f"mean={d_fermat.mean():.1f}")
probe_all_ok = all(v for chk in PROBE_CHK.values() for v in chk.values())
log(f"PIPELINE: ascent {asc_ok}/{NP_}; fermat_id={fermat_ok}; "
    f"probe-exactness all OK={probe_all_ok} ({len(PROBE_CHK)} blocks)")
log(f"RUNTIME: total={time.time()-T0:.0f}s (gen {t_gen:.0f} | descend {t_desc:.0f} | "
    f"oracle {t_oracle:.0f} | features {t_feat:.0f} | stats {time.time()-TS:.0f}s)")
log("LEDGER:")
for entry in LEDGER:
    log(f"  - {entry}")

result = {
    "exp_id": 549,
    "name": "WINDOW-FRONTIER",
    "date": "2026-08-24",
    "seed": SEED,
    "question": ("at fixed probe budget B (#evaluations of a^2-N), what is the "
                 "maximal MI(features;b1) achievable by N-computable window "
                 "placement/content, and what does the bits-per-probe frontier "
                 "look like?"),
    "convention": {"b1": "first descent step FROM THE NODE (deepest-edge letter; "
                         "paper-81 convention)",
                   "descent_order": "letters collected node->root"},
    "config": {"n_per_stratum": NS, "strata": STRATA, "budgets": list(BUDGETS),
               "designs": {"D1": "j=0..B-1 (exp546 baseline)",
                           "D1b": "j=-B/2..B/2-1 (centered)",
                           "D2": f"strict integer-geometric grid [0,{JMAX_D2}]",
                           "D3": f"stride {STRIDE_D3}, coverage {STRIDE_D3}B",
                           "D4": "4 sub-windows B/4 at isqrt+{0,B,4B,16B} concatenated"},
               "features_per_block": FNAMES, "nbins": NBINS, "perms": NPERM,
               "flag_z": FLAGZ, "p_range": [2**14, 2**18], "q_range": [2**16, 2**22],
               "within_logn_bins": 8},
    "population_stats": {
        "n": int(NP_),
        "b1_counts": np.bincount(b1, minlength=4)[1:].tolist(),
        "dB_tree_depth": {"mean": round(float(dB.mean()), 2),
                          "median": float(np.median(dB)),
                          "max": int(dB.max())},
        "d_fermat": {"mean": round(float(d_fermat.mean()), 2),
                     "quantiles_05_25_50_75_90_99": [round(float(v), 1) for v in dq],
                     "max": int(d_fermat.max()),
                     "note": "d = m - isqrt(N): where E(a)=a^2-N crosses zero"},
    },
    "pipeline_check": {
        "fermat_identity": fermat_ok,
        "ascent_matches": f"{asc_ok}/{NP_}", "pass": asc_ok == NP_,
        "per_step_childmap": True, "band_equals_b1": True,
        "probe_layer_exactness": PROBE_CHK,
        "pass_all": bool(probe_all_ok and asc_ok == NP_ and fermat_ok),
    },
    "oracle_diagnostic": {
        "note": "FACTOR-DERIVED (d known), NOT an N-only cell; bounds what any "
                "budget-B bracket detector could carry",
        "fine_grid": oracle_fine,
        "ladder_dual_null": oracle_ladder,
        "I_max": round(Imax_o, 6),
        "saturation_B_star_0.9": BSTAR,
    },
    "verdict": {
        "name": verdict_name,
        "rules_pre_stated": {
            "R1_shape": "MONOTONE iff maxcellMI never drops >2 null SDs across ladder",
            "R2_hitrole": "HIT-DOMINANT iff I(bracket)>=0.9*max at >=3/4 budgets",
            "R3_saturation": "smallest oracle B with I>=0.9*oracle max",
            "R4_approach": "maxcellMI(4096)/I_oracle(1{d<=4096})"},
        "shape": shape, "hit_role": hitrole,
        "hit_dom_budgets": hit_dom_count,
        "hit_role_cells": {str(k): v for k, v in hit_role_cells.items()},
        "saturation_B_star": BSTAR,
        "approach_ratio_at_4096": approach_ratio,
        "basis": "computed from data",
    },
    "bits_per_probe": bpp,
    "fermat_fraction": {"full_scan_E_steps": round(scan_mean, 2),
                        "per_budget": fermat_fraction,
                        "note": "hit-count at budget B is exactly B steps of "
                                "Fermat's scan stopped early"},
    "best_per_budget": {str(k): v for k, v in best_per_B.items()},
    "max_cell_per_budget": {str(B): maxcell[B] for B in BUDGETS},
    "cells": cells,
    "timing_s": {"total": round(time.time() - T0, 1), "gen": round(t_gen, 1),
                 "descend": round(t_desc, 1), "oracle": round(t_oracle, 1),
                 "features": round(t_feat, 1), "stats": round(time.time() - TS, 1)},
    "ledger": LEDGER,
}
outpath = f"{args.outdir}/exp549_result.json"
os.makedirs(args.outdir, exist_ok=True)
with open(outpath, "w") as fh:
    json.dump(result, fh, indent=1)

save_feats = {}
for (des, B), feats in FEATS_BY_DB.items():
    for fname, arr in feats.items():
        save_feats[f"{des}_b{B}_{fname}"] = arr
np.savez_compressed(f"{args.outdir}/exp549_data.npz",
                    P=P, Q=Q, stratum=STRAT, dB=dB, d_fermat=d_fermat, b1=b1,
                    joint12=joint12, logn_bins=logn_bins, **save_feats)
log(f"\nwrote {outpath} and exp549_data.npz")

# ---------------- FRONTIER TABLE (all cells, no cherry-picking) --------------
log("\n--- FRONTIER TABLE (design x B, best feature by z_pooled; target b1) ---")
log(f"{'design':5s} {'B':>5s} {'feature':12s} {'I':>8s} {'z_pool':>9s} {'z_within':>9s}")
for des in DESIGNS:
    for B in BUDGETS:
        bc = [c for c in b1_cells if c["budget"] == B and c["design"] == des]
        top = max(bc, key=lambda c: (c["I"], c["z_pooled"], c["feature"]))
        br = [c for c in bc if c["feature"] == "bracket"][0]
        log(f"{des:5s} {B:5d} {top['feature']:12s} {top['I']:8.4f} "
            f"{top['z_pooled']:+9.1f} {top['z_within']:+9.1f}   "
            f"[bracket: I={br['I']:.4f} zp={br['z_pooled']:+.1f} zw={br['z_within']:+.1f}]")
log("--- ALL b1 CELLS (design/B/feature I, zp, zw) ---")
for c in sorted(b1_cells, key=lambda c: (c["design"], c["budget"], c["feature"])):
    log(f"{c['design']:5s} {c['budget']:5d} {c['feature']:12s} I={c['I']:.6f} "
        f"zp={c['z_pooled']:+8.2f} zw={c['z_within']:+8.2f} bins={c['bins']}")

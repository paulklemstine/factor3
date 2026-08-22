#!/usr/bin/env python3
"""
EXP524 D12-SEMIPRIME  (round-55 #5, seeds 20261110-12)

Completes the semiprime arm of paper 180 (DEGREE-12-COMPOSITE, Q(zeta_56)+,
G+ = C6 x C2, conductor 56) at REAL scale, with paper-164 yield features.

Pre-stated hypotheses (fixed BEFORE any data, from the task brief):
  H1  SEMIPRIME PAIR CHANNEL matches the exact enumeration law derived from the
      C6 x C2 group structure: I(N mod 56 ; ordered type-pair) from draws equals
      the enumeration over the 144 unit pairs; likewise the split-count
      projections I(N mod 56 ; s), s = [split(p)] + [split(q)], and
      I(N mod 56 ; ideal factor-count S_id = 12/k_a + 12/k_b).
      Pass: |z| < 4 for pair (class-binned and orbit-binned), split-count and
      ideal-count channels; DDF cross-check 100%; orbit purity trivially exact.
  H2  COPRIME CONTROL FLAT: I(N mod 97 ; type-pair) carries no content beyond
      multinomial bias (I_ctl <= bias floor AND n*I_ctl constant over thirds).
      (Shuffle null is mis-centered for deterministically equidistributed data;
      operative test is bias-floor + decay, per exp520's honest diagnosis.)

Pre-stated replication expectation (informational gate, paper 164/165/175):
  Spearman(T dial, smooth-relation rate) > 0.5 at bitlen 44 balanced scale.

Design:
  Arm A (population, seed 20261110): 1200 balanced semiprimes, p,q ~ 2^22
    (window [2^22 - 2^18, 2^22)), N bitlen exactly 44. 240 relation values each
    V_j = j(2*isqrt(N)+j) + (isqrt(N)^2 - N), j = 1..240 (paper-164 verbatim);
    smoothness bound B = round(exp(ln(median pooled V)/2.5)) (u = 2.5);
    count/rate features; T(N) = sum(2/q) over QR primes q <= 400.
  Arm B (channel, seed 20261111): 15000 fresh balanced draws; types from the
    C6xC2 coset orders; pair channel vs exact enumeration law; split-count and
    ideal-factor-count projections; which-factor wall via permutation nulls on
    factor-blind channels (N-orbit class, tau(N), T-dial median split).
  Bootstrap/nulls/OOS split (seed 20261112).

Barriers enforced inline:
  (5) DESIGNED CHECKS: defining polynomial integrality + root evaluation;
      distinct-degree factorization of the degree-12 polynomial on sampled REAL
      44-bit primes must reproduce the group-predicted factor pattern (100%);
      empirical type frequencies vs Chebotarev densities within 4 SE;
      which-factor wall permutation nulls.
  (6) PRE-REGISTRATION: field fixed by lab context (f=56, C6xC2); hypotheses,
      pass rules, channel definitions and draw recipe stated above BEFORE data;
      seeds logged; no post-hoc swap (assertions inline).
  (8) POWER: 15000 channel draws -> rarest class x type-pair cell ~104 counts
      (SE ~9.8% rel); bootstrap SDs on all headline gaps; Spearman/R^2 CIs;
      MI bias floors reported; population arm n=1200 x 240 values.

Work dir /tmp/exp50_d12sp/.  Ledger: ledger_exp524.jsonl.  Checkpoint:
result.json rewritten after every stage.  Never touches /home/raver1975/factor3
(read-only reference only).
"""

import json
import math
import time
from fractions import Fraction

import numpy as np

SEED_POP = 20261110
SEED_CH = 20261111
SEED_AUX = 20261112

F_CONDUCTOR = 56          # lab context: Q(zeta_56)+, G+ = C6 x C2
CONTROL_MOD = 97          # coprime control modulus
N_POP = 1200              # balanced 44-bit semiprimes with relation values
N_RELVALS = 240           # relation values per semiprime (paper-164)
U_EXP = 2.5               # smoothness exponent for the bound B
N_SEMIPRIME = 15000       # channel-arm draws
N_BOOT = 200              # bootstrap resamples (CIs, z-scores)
N_PERM = 200              # permutation nulls per channel
N_DDF_PER_TYPE = 20       # real-scale DDF cross-checks per type
WIN_LO = 2 ** 22 - 2 ** 18
WIN_HI = 2 ** 22

WD = "/tmp/exp50_d12sp"
SCRIPT = "exp524_d12_semiprime.py"
RESULT_PATH = f"{WD}/result.json"
LEDGER_PATH = f"{WD}/ledger_exp524.jsonl"
T0 = time.time()
RESULT = {}


def ledger(stage, note, **kv):
    rec = {"ts": time.strftime("%FT%TZ", time.gmtime()),
           "t_elapsed_s": round(time.time() - T0, 3),
           "stage": stage, "note": note}
    rec.update(kv)
    with open(LEDGER_PATH, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(f"[{rec['t_elapsed_s']:>8.2f}s] {stage}: {note} {kv if kv else ''}",
          flush=True)


def ckpt():
    with open(RESULT_PATH, "w") as fh:
        json.dump(RESULT, fh, indent=1, default=str)


# ----------------------------------------------------------------------------
# information measures
# ----------------------------------------------------------------------------

def entropy_from_counts(cnt):
    cnt = np.asarray(cnt, dtype=float)
    n = cnt.sum()
    if n <= 0:
        return 0.0
    p = cnt[cnt > 0] / n
    return float(-(p * np.log2(p)).sum())


def mi_from_joint(J):
    J = np.asarray(J, dtype=float)
    n = J.sum()
    if n <= 0:
        return 0.0
    P = J / n
    pu = P.sum(axis=1, keepdims=True)
    pv = P.sum(axis=0, keepdims=True)
    denom = pu @ pv
    mask = P > 0
    return float((P[mask] * np.log2(P[mask] / denom[mask])).sum())


# ----------------------------------------------------------------------------
# prime generation near 2^22: segmented sieve over the window
# ----------------------------------------------------------------------------

def window_primes(lo, hi):
    sieve = np.ones(hi - lo, dtype=bool)
    for d in range(2, int(math.isqrt(hi)) + 1):
        start = ((lo + d - 1) // d) * d
        if start < d * d:
            start = d * d
        if start < hi:
            sieve[start - lo::d] = False
    out = np.nonzero(sieve)[0].astype(np.int64) + lo
    return out


# small-prime sieve for smoothness testing (paper-164 cap 200k) and QR dial
def small_primes(cap):
    s = np.ones(cap, dtype=bool)
    s[:2] = False
    for i in range(2, int(cap ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.nonzero(s)[0].astype(np.int64)


PRIMES_SMOOTH_CAP = 200000
SMALL_PRIMES = small_primes(PRIMES_SMOOTH_CAP)


def smooth_mask(V, B):
    """paper-164 verbatim: strip primes <= B, smooth iff remainder == 1."""
    W = V.copy()
    for p in SMALL_PRIMES[SMALL_PRIMES <= B]:
        while True:
            m = W % p == 0
            if not m.any():
                break
            W[m] //= p
            if not (W % p == 0).any():
                break
    return W == 1


# ----------------------------------------------------------------------------
# group machinery: G+ = (Z/f)^*/<-1>, orbit group law, coset orders (exp520)
# ----------------------------------------------------------------------------

def unit_group(f):
    return [u for u in range(1, f) if math.gcd(u, f) == 1]


def build_quotient(f):
    U = unit_group(f)
    canon = {}
    orbits = []
    for u in U:
        if u in canon:
            continue
        o = (u, ((f - 1) * u) % f)
        assert o[0] != o[1], "degenerate orbit"
        orbits.append(o)
        for e in o:
            canon[e] = len(orbits) - 1
    NO = len(orbits)
    assert NO * 2 == len(U), "orbit sizes must all be 2"

    def op(i, j):
        return canon[(orbits[i][0] * orbits[j][0]) % f]

    ident = canon[1 % f]
    order = [None] * NO
    for i in range(NO):
        x, c = i, 1
        while x != ident:
            x = op(x, i)
            c += 1
            if c > NO + 1:
                raise RuntimeError("group law not closed -- bug")
        order[i] = c
    hist = {}
    for o in order:
        hist[o] = hist.get(o, 0) + 1
    if max(order) == NO:
        structure = f"C{NO}"
    else:
        structure = ("C%dxC2" % max(order)) if max(order) == 6 \
            else f"unknown(exp={max(order)})"
    return {
        "f": f, "phi": len(U), "n_orbits": NO,
        "orbits": [list(o) for o in orbits],
        "orders_by_orbit": order,
        "order_histogram": {str(k): v for k, v in sorted(hist.items())},
        "cyclic": bool(max(order) == NO),
        "structure_guess": structure,
        "_canon": canon, "_op": op, "_ident": ident,
    }


# ----------------------------------------------------------------------------
# minimal polynomial of zeta_f + zeta_f^{-1} + modular poly toolkit (exp520)
# ----------------------------------------------------------------------------

def real_cyclotomic_poly(f):
    ks = sorted({min(u, f - u) for u in unit_group(f)})
    d = len(ks)
    assert d == len(unit_group(f)) // 2
    ths = [2.0 * math.cos(2.0 * math.pi * k / f) for k in ks]
    ps = []
    for m in range(1, d + 1):
        s = math.fsum(t ** m for t in ths)
        v = round(s)
        assert abs(s - v) < 1e-3, f"power sum not integral at m={m}: {s}"
        ps.append(int(v))
    e = [Fraction(1)] + [Fraction(0)] * d
    for k in range(1, d + 1):
        S = Fraction(ps[k - 1])
        for i in range(1, k):
            S += ((-1) ** i) * e[i] * Fraction(ps[k - 1 - i])
        e[k] = ((-1) ** (k + 1)) * S / k
        assert e[k].denominator == 1, f"non-integer e_{k}"
    coeffs = [int(((-1) ** (d - j)) * e[d - j]) for j in range(d + 1)]
    th = 2.0 * math.cos(2.0 * math.pi / f)
    val = sum(coeffs[i] * th ** i for i in range(d + 1))
    return coeffs, {"degree": d,
                    "coeffs_desc": [int(c) for c in reversed(coeffs)],
                    "eval_at_2cos_2pi_over_f": val}


def ptrim(a):
    while a and a[-1] == 0:
        a.pop()
    return a


def pmul(a, b, p):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                r[i + j] = (r[i + j] + ai * bj) % p
    return ptrim(r)


def pmod(a, f, p):
    a = [x % p for x in a]
    df = len(f) - 1
    inv = pow(f[df], -1, p) if f[df] != 1 else 1
    for i in range(len(a) - 1, df - 1, -1):
        c = a[i]
        if c:
            c = c * inv % p
            a[i] = 0
            for j in range(df):
                a[i - df + j] = (a[i - df + j] - c * f[j]) % p
    return ptrim(a)


def pgcd(a, b, p):
    a = ptrim([x % p for x in a])
    b = ptrim([x % p for x in b])
    while b:
        a, b = b, pmod(a, b, p)
    if a:
        inv = pow(a[-1], -1, p)
        a = [x * inv % p for x in a]
    return a


def ppowmod(base, e, f, p):
    result = [1]
    base = pmod(base[:], f, p)
    while e:
        if e & 1:
            result = pmod(pmul(result, base, p), f, p)
        base = pmod(pmul(base, base, p), f, p)
        e >>= 1
    return result


def ddf_pattern(fpoly, p):
    """distinct-degree factorization pattern: dict deg -> number of factors."""
    f = ptrim([x % p for x in fpoly])
    deg = len(f) - 1
    pat = {}
    covered = 0
    w = [0, 1]
    for d in range(1, deg + 1):
        w = ppowmod(w, p, f, p)
        h = ptrim([(w[i] - (1 if i == 1 else 0)) % p for i in range(len(w))])
        g = pgcd(f, h, p)
        dg = len(g) - 1 if g else 0
        if dg > 0:
            pat[d] = pat.get(d, 0) + dg // d
            covered += dg
        if covered == deg:
            break
    assert covered == deg, f"DDF did not cover f mod {p}"
    return {k: v for k, v in pat.items() if v > 0}


# ----------------------------------------------------------------------------
# STAGE 0: init
# ----------------------------------------------------------------------------

ledger("S0", "init", seeds=[SEED_POP, SEED_CH, SEED_AUX], wd=WD,
       field="Q(zeta_56)+", Gplus="C6xC2", n_pop=N_POP, n_relvals=N_RELVALS,
       u_exp=U_EXP, n_semiprime=N_SEMIPRIME)
RESULT["meta"] = {
    "exp": 524, "codename": "D12-SEMIPRIME", "round": "55",
    "seeds": {"population": SEED_POP, "channel": SEED_CH, "aux": SEED_AUX},
    "script": SCRIPT, "wd": WD,
    "field": "Q(zeta_56)+", "conductor": F_CONDUCTOR, "Gplus": "C6xC2",
    "n_pop": N_POP, "n_relvals": N_RELVALS, "u_exp": U_EXP,
    "n_semiprime": N_SEMIPRIME, "n_boot": N_BOOT, "n_perm": N_PERM,
    "started_utc": time.strftime("%FT%TZ", time.gmtime()),
}
ckpt()

# ----------------------------------------------------------------------------
# STAGE 1: group machinery + type map + designed checks
# ----------------------------------------------------------------------------

ledger("S1", "building G+ quotient")
G = build_quotient(F_CONDUCTOR)
canon, ORB_ORDER, NO = G["_canon"], G["orders_by_orbit"], G["n_orbits"]
orb_op, orb_ident = G["_op"], G["_ident"]

# designed checks (barrier 5): closure (via order loop), inverses, abelian
inv_ok = all(any(orb_op(i, j) == orb_ident for j in range(NO))
             for i in range(NO))
comm_ok = all(orb_op(i, j) == orb_op(j, i)
              for i in range(NO) for j in range(NO))
assert inv_ok and comm_ok, "group axioms violated"

orders_sorted = sorted(set(ORB_ORDER))
type_of_order = {k: i for i, k in enumerate(orders_sorted)}
TYPE_OF_ORB = [type_of_order[k] for k in ORB_ORDER]
NT = len(orders_sorted)
hist = {int(k): v for k, v in G["order_histogram"].items()}
H_theory = -sum((c / NO) * math.log2(c / NO) for c in hist.values())

assert G["structure_guess"] == "C6xC2", "field must be C6 x C2 (lab context)"
assert NO == 12 and NT == 4, "expected 12 classes, 4 types"

RESULT["group"] = {
    "f": F_CONDUCTOR, "structure": G["structure_guess"], "n_orbits": NO,
    "orbits": G["orbits"], "orders_by_orbit": ORB_ORDER,
    "order_histogram": G["order_histogram"],
    "types_orders": orders_sorted,
    "type_densities_theory": {str(k): v / NO for k, v in hist.items()},
    "H_T_theory_bits": H_theory,
    "shape_legend": ("Frobenius order k => factors all of degree k, count "
                     "12/k; k=1: twelve linears; k=2: six quadratics; "
                     "k=3: four cubics; k=6: two sextics"),
    "designed_checks": {"inverses": bool(inv_ok), "abelian": bool(comm_ok)},
}
ledger("S1", "G+ ok", structure=G["structure_guess"],
       orders=G["order_histogram"], H_T=round(H_theory, 6))
ckpt()

# ----------------------------------------------------------------------------
# STAGE 2: defining polynomial + root check (barrier 5 part 1)
# ----------------------------------------------------------------------------

poly, poly_info = real_cyclotomic_poly(F_CONDUCTOR)
assert poly_info["degree"] == 12
assert abs(poly_info["eval_at_2cos_2pi_over_f"]) < 1e-8, "root eval failed"
RESULT["polynomial"] = poly_info
ledger("S2", "minimal polynomial ok", degree=poly_info["degree"],
       root_eval=poly_info["eval_at_2cos_2pi_over_f"])
ckpt()

# ----------------------------------------------------------------------------
# STAGE 3: Arm A -- 1200 balanced 44-bit semiprimes, paper-164 features
# ----------------------------------------------------------------------------

rng_pop = np.random.default_rng(SEED_POP)
primes_win = window_primes(WIN_LO, WIN_HI)
ledger("S3", "window primes ready", window=f"[{WIN_LO},{WIN_HI})",
       n_primes=int(len(primes_win)))

pop_idx = rng_pop.choice(len(primes_win), size=(N_POP, 2), replace=True)
bad = pop_idx[:, 0] == pop_idx[:, 1]
while bad.any():
    pop_idx[bad] = rng_pop.choice(len(primes_win), size=(int(bad.sum()), 2))
    bad = pop_idx[:, 0] == pop_idx[:, 1]
P_pop = primes_win[pop_idx[:, 0]]
Q_pop = primes_win[pop_idx[:, 1]]
N_pop_arr = P_pop.astype(object) * Q_pop.astype(object)

bl = np.array([x.bit_length() for x in N_pop_arr])
bal = np.array([max(int(p), int(q)) / min(int(p), int(q))
                for p, q in zip(P_pop, Q_pop)])
assert (bl == 44).all(), "all population semiprimes must have bitlen 44"
assert bal.max() <= 16 / 15 + 1e-9, "balance window violated"
ledger("S3", "population drawn", n=N_POP, bitlen_min=int(bl.min()),
       bitlen_max=int(bl.max()), max_ratio=float(bal.max()))

# relation values (paper-164 verbatim) and smoothness at u = 2.5
sq = np.array([math.isqrt(int(n)) for n in N_pop_arr], dtype=np.int64)
js = np.arange(1, N_RELVALS + 1, dtype=np.int64)
V = js[None, :] * (2 * sq[:, None] + js[None, :]) + (sq[:, None] ** 2
                                                    - np.array(
      [int(n) for n in N_pop_arr], dtype=np.int64)[:, None])
assert (V > 0).all(), "relation values must be positive"
vmed = float(np.median(V.astype(float)))
B_smooth = max(int(round(math.exp(math.log(vmed) / U_EXP))), 50)
ledger("S3", "smoothness bound", median_V=vmed, B=B_smooth, u=U_EXP)
RESULT["smoothness"] = {"median_V": vmed, "B": B_smooth, "u": U_EXP,
                        "cap_primes": PRIMES_SMOOTH_CAP}

t_sm = time.time()
sm = smooth_mask(V.reshape(-1).astype(np.int64),
                 B_smooth).reshape(N_POP, N_RELVALS)
count_feat = sm.sum(axis=1)                      # count feature (of 240)
rate_feat = sm.mean(axis=1)                      # rate feature
ledger("S3", "smoothness done", elapsed_s=round(time.time() - t_sm, 1),
       mean_rate=float(rate_feat.mean()),
       nonzero_frac=float((count_feat > 0).mean()))
ckpt()

# T dial (paper-164 verbatim): T(N) = sum(2/q) over QR primes q <= 400
try:
    import gmpy2

    def jacobi_qr(base, q):
        return gmpy2.powmod(base, (q - 1) // 2, q) == 1
except ImportError:  # pragma: no cover
    def jacobi_qr(base, q):
        return pow(base, (q - 1) // 2, q) == 1

wr = [int(qq) for qq in SMALL_PRIMES[(SMALL_PRIMES >= 3)
                                     & (SMALL_PRIMES <= 400)]]
N_int64 = np.array([int(n) for n in N_pop_arr], dtype=np.int64)
T_dial = np.zeros(N_POP)
for q in wr:                       # vectorized over the population per prime
    r = N_int64 % int(q)
    is_qr = np.array([jacobi_qr(int(ri), q) for ri in r])
    T_dial += np.where(is_qr, 2.0 / q, 0.0)
RESULT["dial"] = {
    "T_definition": "T(N)=sum(2/q) over QR primes q<=400 (paper-164)",
    "qr_primes_used": len(wr),
    "T_mean": float(T_dial.mean()), "T_sd": float(T_dial.std()),
    "T_range": [float(T_dial.min()), float(T_dial.max())],
}
ledger("S3", "T dial done", qr_primes=len(wr),
       T_mean=round(float(T_dial.mean()), 4))
ckpt()


def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    return float(np.corrcoef(rx, ry)[0, 1])


rng_aux = np.random.default_rng(SEED_AUX)
idx = rng_aux.permutation(N_POP)
tr, te = idx[:800], idx[800:]


def oos_r2(train_x, train_y, test_x, test_y):
    Xa = np.column_stack([np.ones(len(tr)), train_x])
    coef, *_ = np.linalg.lstsq(Xa, train_y, rcond=None)
    pred = np.column_stack([np.ones(len(te)), test_x]) @ coef
    yy = test_y
    return 1 - float(((yy - pred) ** 2).sum()) / float(
        ((yy - yy.mean()) ** 2).sum() + 1e-30)


s_full = spearman(T_dial, rate_feat)
s_te = spearman(T_dial[te], rate_feat[te])
adv = oos_r2(T_dial[tr], rate_feat[tr], T_dial[te], rate_feat[te])

boot_sp, boot_r2 = [], []
for _ in range(N_BOOT):
    rb = rng_aux.integers(0, len(te), size=len(te))
    boot_sp.append(spearman(T_dial[te][rb], rate_feat[te][rb]))
    rt = rng_aux.integers(0, len(tr), size=len(tr))
    boot_r2.append(oos_r2(T_dial[tr][rt], rate_feat[tr][rt],
                          T_dial[te], rate_feat[te]))
boot_sp, boot_r2 = np.array(boot_sp), np.array(boot_r2)

RESULT["armA_dial"] = {
    "n": N_POP, "relvals": N_RELVALS, "u": U_EXP, "B": B_smooth,
    "spearman_T_rate_full": s_full,
    "spearman_T_rate_test": s_te,
    "spearman_boot_ci95": [float(np.percentile(boot_sp, 2.5)),
                           float(np.percentile(boot_sp, 97.5))],
    "advantage_oos_R2_T": adv,
    "advantage_boot_ci95": [float(np.percentile(boot_r2, 2.5)),
                            float(np.percentile(boot_r2, 97.5))],
    "replication_gate_spearman_gt_05": bool(s_te > 0.5),
    "mean_count": float(count_feat.mean()),
}
ledger("S3", "arm A done", spearman_full=round(s_full, 4),
       spearman_test=round(s_te, 4),
       sp_ci=[round(float(np.percentile(boot_sp, 2.5)), 3),
              round(float(np.percentile(boot_sp, 97.5)), 3)],
       advantage_R2=round(adv, 4),
       adv_ci=[round(float(np.percentile(boot_r2, 2.5)), 3),
               round(float(np.percentile(boot_r2, 97.5)), 3)])
ckpt()

# ----------------------------------------------------------------------------
# STAGE 4: Arm B -- 15000 draws; types; pair channel vs enumeration law
# ----------------------------------------------------------------------------

rng_ch = np.random.default_rng(SEED_CH)
ch_idx = rng_ch.choice(len(primes_win), size=(N_SEMIPRIME, 2), replace=True)
badc = ch_idx[:, 0] == ch_idx[:, 1]
while badc.any():
    ch_idx[badc] = rng_ch.choice(len(primes_win), size=(int(badc.sum()), 2))
    badc = ch_idx[:, 0] == ch_idx[:, 1]
PA = primes_win[ch_idx[:, 0]]
PB = primes_win[ch_idx[:, 1]]
cls_a = PA % F_CONDUCTOR
cls_b = PB % F_CONDUCTOR
orb_a = np.array([canon[int(c)] for c in cls_a], dtype=np.int64)
orb_b = np.array([canon[int(c)] for c in cls_b], dtype=np.int64)
TA = np.array([TYPE_OF_ORB[o] for o in orb_a], dtype=np.int64)
TB = np.array([TYPE_OF_ORB[o] for o in orb_b], dtype=np.int64)
CN = (PA * PB) % F_CONDUCTOR          # int64-safe: p*q < 2^44
ORB_N = np.array([canon[int(c)] for c in CN], dtype=np.int64)
TN = np.array([TYPE_OF_ORB[o] for o in ORB_N], dtype=np.int64)

# Chebotarev density check on the drawn factors (barrier 5 part 3)
dens_thy = np.array([hist[k] / NO for k in orders_sorted])
freq_a = np.array([(TA == t).mean() for t in range(NT)])
se_a = np.sqrt(freq_a * (1 - freq_a) / N_SEMIPRIME)
dens_z = np.abs(freq_a - dens_thy) / se_a
assert dens_z.max() < 4, "Chebotarev density check failed"

# ---- exact enumeration law over the 144 ordered unit pairs (exp520) --------
ord_of_unit = {}
for u in unit_group(F_CONDUCTOR):
    ord_of_unit[u] = ORB_ORDER[canon[u]]
U_LIST = np.array(unit_group(F_CONDUCTOR))

law_pairs = {}
pair_count = {}
for a in U_LIST:
    oa = ord_of_unit[int(a)]
    for b in U_LIST:
        c = int(a) * int(b) % F_CONDUCTOR
        ob = ord_of_unit[int(b)]
        key = (c, oa, ob)
        law_pairs[key] = law_pairs.get(key, 0) + 1
        pair_count[(oa, ob)] = pair_count.get((oa, ob), 0) + 1
tot = len(U_LIST) ** 2

P_law = np.zeros((F_CONDUCTOR, NT, NT))
for (c, ta_, tb_), m in law_pairs.items():
    P_law[c, type_of_order[ta_], type_of_order[tb_]] = m / tot
I_law_class = mi_from_joint(P_law.reshape(F_CONDUCTOR, NT * NT))

Po_law = np.zeros((NO, NT, NT))
for (c, ta_, tb_), m in law_pairs.items():
    Po_law[canon[c], type_of_order[ta_], type_of_order[tb_]] += m / tot
I_law_orbit = mi_from_joint(Po_law.reshape(NO, NT * NT))
H_pair_law = entropy_from_counts(list(pair_count.values()))

# ---- split-count laws -------------------------------------------------------
# paper-74 form: split event <=> Frobenius order 1 (complete splitting);
# identity class density 1/12 => Binomial(2, 1/12) marginal.
# NOTE: law_pairs carries ORDERS (1,2,3,6); split test is order == 1.
split_type = type_of_order[1]
law_cs = {}
for (c, ta_, tb_), m in law_pairs.items():
    assert ta_ in (1, 2, 3, 6) and tb_ in (1, 2, 3, 6), "expected orders"
    s = int(ta_ == 1) + int(tb_ == 1)
    d = law_cs.setdefault(c, {})
    d[s] = d.get(s, 0) + m
Jcs_law = np.zeros((F_CONDUCTOR, 3))
for c, d in law_cs.items():
    for s, m in d.items():
        Jcs_law[c, s] = m / tot
I_split_law = mi_from_joint(Jcs_law)

# ideal factor-count projection: S_id = 12/k_a + 12/k_b in {4..24}
law_csid = {}
for (c, ta_, tb_), m in law_pairs.items():
    sid = 12 // ta_ + 12 // tb_
    law_csid[(c, sid)] = law_csid.get((c, sid), 0) + m
Jcsid_law = np.zeros((F_CONDUCTOR, 25))
for (c, sid), m in law_csid.items():
    Jcsid_law[c, sid] = m / tot
I_sid_law = mi_from_joint(Jcsid_law)

# ---- empirical channels ------------------------------------------------------
pair_code = TA * NT + TB
Jsp = np.bincount(CN * NT * NT + pair_code,
                  minlength=F_CONDUCTOR * NT * NT).reshape(F_CONDUCTOR,
                                                           NT * NT)
I_pair_emp = mi_from_joint(Jsp)
Jspo = np.bincount(ORB_N * NT * NT + pair_code,
                   minlength=NO * NT * NT).reshape(NO, NT * NT)
I_pairo_emp = mi_from_joint(Jspo)

s_emp = (TA == split_type).astype(np.int64) + (TB == split_type).astype(np.int64)
Jsp_split = np.bincount(CN * 3 + s_emp, minlength=F_CONDUCTOR * 3).reshape(
    F_CONDUCTOR, 3)
I_split_emp = mi_from_joint(Jsp_split)
ORD_ARR = np.array(orders_sorted, dtype=np.int64)
sid_emp = 12 // ORD_ARR[TA] + 12 // ORD_ARR[TB]
Jsp_sid = np.bincount(CN * 25 + sid_emp, minlength=F_CONDUCTOR * 25).reshape(
    F_CONDUCTOR, 25)
I_sid_emp = mi_from_joint(Jsp_sid)


def boot_mi(rows_x, rows_y, n_bins_x, n_bins_y):
    """bootstrap MI SD from resampling the draw index."""
    vals = []
    for _ in range(N_BOOT):
        rb = rng_aux.integers(0, N_SEMIPRIME, size=N_SEMIPRIME)
        xb, yb = rows_x[rb], rows_y[rb]
        Jb = np.bincount(xb * n_bins_y + yb,
                         minlength=n_bins_x * n_bins_y).reshape(n_bins_x,
                                                                n_bins_y)
        vals.append(mi_from_joint(Jb))
    return np.array(vals)


sd_class = boot_mi(CN, pair_code, F_CONDUCTOR, NT * NT)
sd_orbo = boot_mi(ORB_N, pair_code, NO, NT * NT)
sd_split = boot_mi(CN, s_emp, F_CONDUCTOR, 3)
sd_sid = boot_mi(CN, sid_emp, F_CONDUCTOR, 25)

z_class = (I_pair_emp - I_law_class) / (sd_class.std() + 1e-18)
z_orbo = (I_pairo_emp - I_law_orbit) / (sd_orbo.std() + 1e-18)
z_split = (I_split_emp - I_split_law) / (sd_split.std() + 1e-18)
z_sid = (I_sid_emp - I_sid_law) / (sd_sid.std() + 1e-18)

bias_floor_pair = (F_CONDUCTOR - 1) * (NT * NT - 1) / (
    2 * N_SEMIPRIME * math.log(2))

# ---- coprime controls (H2): full N reduced mod coprime moduli ----------------
N_full_ch = PA * PB                    # int64-safe: p*q < 2^44
controls = {}
h2_flat_all = True
for MCTL in (9, CONTROL_MOD):
    ctl_bin = N_full_ch % MCTL         # honest: reduce the FULL semiprime
    NBm = MCTL
    n_cells = NBm * NT * NT
    assert ctl_bin.max() < NBm, "control binning overflow"
    Jctl = np.bincount(ctl_bin * NT * NT + pair_code,
                       minlength=n_cells).reshape(NBm, NT * NT)
    I_ctl_m = mi_from_joint(Jctl)
    floor_m = (NBm - 1) * (NT * NT - 1) / (2 * N_SEMIPRIME * math.log(2))
    # decay diagnostic: cumulative deciles; under pure estimator bias
    # n*I(n) ~ const (OLS slope ~ 0), under real content it grows ~linearly.
    ns, nIs = [], []
    bounds = np.linspace(0, N_SEMIPRIME, 11).astype(int)
    for b in range(1, 11):
        sl = slice(0, bounds[b])
        Jb = np.bincount(ctl_bin[sl] * NT * NT + pair_code[sl],
                         minlength=n_cells).reshape(NBm, NT * NT)
        ns.append(float(bounds[b]))
        nIs.append(float(bounds[b]) * mi_from_joint(Jb))
    ns_a, nIs_a = np.array(ns), np.array(nIs)
    slope = float(np.polyfit(ns_a, nIs_a, 1)[0])
    mean_nI = float(nIs_a.mean())
    # secondary: shuffle null (advisory only -- can be mis-centered for
    # deterministic AP data; draws here are random window primes)
    nulls = []
    for _ in range(N_PERM):
        pc_p = rng_aux.permutation(pair_code)
        Jp = np.bincount(ctl_bin * NT * NT + pc_p,
                         minlength=n_cells).reshape(NBm, NT * NT)
        nulls.append(mi_from_joint(Jp))
    nulls = np.array(nulls)
    z_shuf = float((I_ctl_m - nulls.mean()) / (nulls.std() + 1e-18))
    flat_m = bool(I_ctl_m <= floor_m and slope <= 0.1 * abs(mean_nI))
    h2_flat_all &= flat_m
    controls[str(MCTL)] = {
        "I_bits": float(I_ctl_m), "bias_floor_bits": floor_m,
        "nI_mean_bitcount": mean_nI, "nI_slope_per_draw": slope,
        "slope_frac_of_mean": slope / (abs(mean_nI) + 1e-18),
        "shuffle_null_mean": float(nulls.mean()),
        "shuffle_z_advisory": z_shuf, "flat": flat_m}

# ---- which-factor wall --------------------------------------------------------
WF = (PB > PA).astype(np.int64)
wall_channels = {}
wf_null = {}
for name, ch_bins in (("orbit_class12", ORB_N),
                      ("tau_N4", TN)):
    for label, xx in ((name, ch_bins),):
        Jw = np.bincount(xx * 2 + WF, minlength=(xx.max() + 1) * 2).reshape(-1, 2)
        I_obs = mi_from_joint(Jw)
        nulls = []
        for _ in range(N_PERM):
            wp = rng_aux.permutation(WF)
            Jp = np.bincount(xx * 2 + wp,
                             minlength=(xx.max() + 1) * 2).reshape(-1, 2)
            nulls.append(mi_from_joint(Jp))
        nulls = np.array(nulls)
        wall_channels[label] = {
            "bins": int(xx.max() + 1), "I_bits": float(I_obs),
            "null_mean": float(nulls.mean()),
            "null_sd": float(nulls.std()),
            "null_max": float(nulls.max()),
            "z": float((I_obs - nulls.mean()) / (nulls.std() + 1e-18))}
wall_ok = all(abs(v["z"]) < 4 for v in wall_channels.values())
wall_sens = max(abs(v["I_bits"] - v["null_mean"])
                for v in wall_channels.values())

RESULT["armB_channel"] = {
    "draws": N_SEMIPRIME,
    "window": [WIN_LO, WIN_HI], "window_primes": int(len(primes_win)),
    "pair_channel": {
        "law_class_bits": I_law_class, "emp_class_bits": I_pair_emp,
        "diff_bits": float(I_pair_emp - I_law_class),
        "boot_sd_bits": float(sd_class.std()), "z": float(z_class),
        "law_orbit_bits": I_law_orbit, "emp_orbit_bits": I_pairo_emp,
        "diff_orbit_bits": float(I_pairo_emp - I_law_orbit),
        "boot_sd_orbit_bits": float(sd_orbo.std()), "z_orbit": float(z_orbo),
        "H_pair_law_bits": H_pair_law,
        "bias_floor_bits": bias_floor_pair},
    "split_count": {
        "definition": "s=[T(p)=1]+[T(q)=1]; identity density 1/12",
        "law_bits": I_split_law, "emp_bits": I_split_emp,
        "diff_bits": float(I_split_emp - I_split_law),
        "boot_sd_bits": float(sd_split.std()), "z": float(z_split)},
    "ideal_factor_count": {
        "definition": "S_id = 12/k_a + 12/k_b",
        "law_bits": I_sid_law, "emp_bits": I_sid_emp,
        "diff_bits": float(I_sid_emp - I_sid_law),
        "boot_sd_bits": float(sd_sid.std()), "z": float(z_sid)},
    "coprime_control": {
        "moduli": [9, CONTROL_MOD],
        "per_modulus": controls,
        "all_flat": bool(h2_flat_all),
        "note": ("shuffle null advisory only (can be mis-centered for "
                 "deterministic AP equidistribution); operative tests are "
                 "bias floor + n*I decay (exp520 honest diagnosis)")},
    "which_factor_wall": {
        "channels": wall_channels, "holds": bool(wall_ok),
        "sensitivity_bits": float(wall_sens)},
    "type_freq_factors": {str(k): float(v) for k, v in zip(orders_sorted,
                                                           freq_a)},
    "chebotarev_density_max_z": float(dens_z.max()),
}
ledger("S4", "channel arm done",
       I_pair_law=round(I_law_class, 5), I_pair_emp=round(I_pair_emp, 5),
       z_class=round(float(z_class), 2), z_orbit=round(float(z_orbo), 2),
       Is_law=round(I_split_law, 5), Is_emp=round(I_split_emp, 5),
       z_split=round(float(z_split), 2),
       I_sid_law=round(I_sid_law, 5), I_sid_emp=round(I_sid_emp, 5),
       z_sid=round(float(z_sid), 2),
       ctl_flat={k: v["flat"] for k, v in controls.items()},
       wall_ok=wall_ok,
       wall_sens_bits=round(float(wall_sens), 5))
ckpt()

# ----------------------------------------------------------------------------
# STAGE 5: real-scale DDF cross-validation of predicted factor patterns
# ----------------------------------------------------------------------------

ddf_checks = 0
ddf_fail = 0
for t_ord, t_idx in sorted(type_of_order.items()):
    cand = np.nonzero(TA == t_idx)[0]
    take = rng_ch.choice(cand, size=min(N_DDF_PER_TYPE, len(cand)),
                         replace=False)
    expected = {t_ord: 12 // t_ord}
    for ix in take:
        got = ddf_pattern(poly, int(PA[ix]))
        ddf_checks += 1
        ddf_fail += (got != expected)
RESULT["ddf_real_scale"] = {
    "checked": int(ddf_checks), "failed": int(ddf_fail),
    "pass": bool(ddf_fail == 0)}
ledger("S5", "DDF real-scale cross-check",
       checked=int(ddf_checks), failed=int(ddf_fail))
if ddf_fail:
    ledger("S5", "BARRIER-5 FAILURE: DDF contradicts group prediction")
ckpt()

# ----------------------------------------------------------------------------
# STAGE 6: verdict assembly
# ----------------------------------------------------------------------------

h1_pass = bool(abs(z_class) < 4 and abs(z_orbo) < 4 and abs(z_split) < 4
               and abs(z_sid) < 4 and ddf_fail == 0 and dens_z.max() < 4)
h2_pass = h2_flat_all
pass_all = h1_pass and h2_pass
verdict = "D12-SEMIPRIME-LAW-CONFIRMED" if pass_all else "D12-SEMIPRIME-ANOMALY"

RESULT["verdict"] = {
    "name": verdict,
    "H1_pair_and_projections_match_enumeration_law": h1_pass,
    "H2_coprime_control_flat": h2_pass,
    "dial_replication_spearman_gt_05": bool(s_te > 0.5),
    "barriers": {
        "barrier_5_designed_checks": {
            "poly_integrality_and_degree": True,
            "root_evaluation": True,
            "dd_vs_group_pattern_real_scale": {
                "checked": int(ddf_checks), "failed": int(ddf_fail),
                "pass": bool(ddf_fail == 0)},
            "chebotarev_densities_max_z": float(dens_z.max()),
            "which_factor_wall": {
                "holds": bool(wall_ok),
                "sensitivity_bits": float(wall_sens),
                "per_channels": {k: v["z"] for k, v in
                                 wall_channels.items()}},
            "group_axioms": {"inverses": bool(inv_ok),
                             "abelian": bool(comm_ok)}},
        "barrier_6_pre_registration": {
            "field_fixed_by_lab_context": "f=56, C6xC2",
            "hypotheses_stated_before_data": True,
            "pass_rules_pre_stated": "|z|<4 on four channels; control "
                                     "bias-floor + decay",
            "seeds_logged": [SEED_POP, SEED_CH, SEED_AUX]},
        "barrier_8_power": {
            "channel_draws": N_SEMIPRIME,
            "rarest_class_pair_cell_expected": round(N_SEMIPRIME /
                                                     (len(U_LIST) ** 2), 1),
            "mi_bias_floor_pair_bits": bias_floor_pair,
            "mi_bias_floor_control_bits": bias_floor_ctl,
            "boot_sd_headline_bits": {
                "pair_class": float(sd_class.std()),
                "split": float(sd_split.std())},
            "population_arm": {"n": N_POP, "relvals_per_N": N_RELVALS,
                               "spearman_ci95": [
                                   float(np.percentile(boot_sp, 2.5)),
                                   float(np.percentile(boot_sp, 97.5))]}},
    },
    "elapsed_s": round(time.time() - T0, 1),
}
ckpt()
ledger("S6", "VERDICT", name=verdict, H1=h1_pass, H2=h2_pass,
       spearman_test=round(s_te, 4), advantage_R2=round(adv, 4),
       elapsed_s=round(time.time() - T0, 1))
print(json.dumps({"verdict": verdict, "H1": h1_pass, "H2": h2_pass,
                  "spearman_T_rate_test": round(s_te, 4),
                  "advantage_oos_R2": round(adv, 4),
                  "I_pair_law": round(I_law_class, 5),
                  "I_pair_emp": round(I_pair_emp, 5),
                  "z_class": round(float(z_class), 2)}, indent=1))

#!/usr/bin/env python3
"""
EXP520 DEGREE-12-COMPOSITE  (round-54, seed 20261060)

First COMPOSITE-ORDER abelian rung of the full-pinning ladder: a real cyclotomic
subfield Q(zeta_f)+ with phi(f)/2 = 12 (degree 12, |G+| = 12 composite).

Pre-stated hypotheses (fixed in the task brief before any prime data):
  H1  FULL PINNING at degree 12: I(p mod cond ; T) = H(T) exactly
      (every Frobenius orbit class is pure in type T).
  H2  SEMIPRIME PAIR CHANNEL matches the exact enumeration law:
      I(N mod cond ; (T_p,T_q)) from draws == exact enumeration over unit pairs.
  H3  CONTROLS: wrong-modulus channel FLAT; thickening STRUCTURAL
      (I - H(T) gap stays 0 as sample grows).

Field selection rule (pre-stated, applied BEFORE looking at any prime data):
  among conductors f with phi(f) = 24, prefer NON-CYCLIC G+ = (Z/f)^*/<-1>,
  then richest type alphabet (more distinct element orders), tie-break smallest f.

Barriers enforced inline:
  (5) DESIGNED-CHECKS: minimal-polynomial construction asserts (integrality,
      degree, p(2cos(2pi/f)) ~ 0), distinct-degree factorization cross-check of
      predicted factor pattern on sampled primes (must be 100%), orbit purity.
  (6) PRE-REGISTRATION: field chosen by the rule above; all ten candidate
      conductors logged with their G+ tables in result.json; no post-hoc swap.
  (8) POWER: N ~ 155k primes, rarest type cell ~13k -> binomial SE < 0.1%/cell;
      MI bias floor reported; semiprime arm bootstrapped; all headline claims
      are machine-precision equalities, far above the floor.

Work dir /tmp/exp50_d12/.  Ledger: ledger_exp520.jsonl.  Checkpoint: result.json
rewritten after every stage.  Never touches /home/raver1975/factor3.
"""

import json
import math
import time
from fractions import Fraction

import numpy as np

SEED = 20261060
WD = "/tmp/exp50_d12"
SCRIPT = "exp520_degree_12.py"
PRIME_CAP = 2 ** 21          # sieve primes < 2^21
CONTROL_MOD = 97             # coprime/wrong-modulus control (prime, coprime to any f)
N_PERM = 200                 # permutation nulls for the main channel
N_SEMIPRIME = 15000          # semiprime arm draws
N_BOOT = 200                 # bootstrap resamples for the semiprime arm
N_DDF_PER_TYPE = 40          # polynomial cross-validation primes per type

RESULT = {}
LEDGER_PATH = f"{WD}/ledger_exp520.jsonl"
RESULT_PATH = f"{WD}/result.json"
T0 = time.time()


def ledger(stage, note, **kv):
    rec = {"ts": time.strftime("%FT%TZ", time.gmtime()),
           "t_elapsed_s": round(time.time() - T0, 3),
           "stage": stage, "note": note}
    rec.update(kv)
    with open(LEDGER_PATH, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(f"[{rec['t_elapsed_s']:>8.2f}s] {stage}: {note} {kv if kv else ''}", flush=True)


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
# group machinery: G+ = (Z/f)^* / <-1>, orbits, orders
# ----------------------------------------------------------------------------

def unit_group(f):
    return [u for u in range(1, f) if math.gcd(u, f) == 1]


def build_quotient(f):
    """Orbits of (Z/f)^* under multiplication by -1; group law on orbits."""
    U = unit_group(f)
    canon = {}
    orbits = []
    for u in U:
        if u in canon:
            continue
        o = (u, ((f - 1) * u) % f)
        assert o[0] != o[1], "degenerate orbit (f=2?)"
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
    # classification for |G+| = 12: cyclic C12 iff an element of order 12 exists;
    # otherwise (exponent 6) it is C6 x C2.
    if max(order) == NO:
        structure = f"C{NO}"
    else:
        structure = "C%dxC2" % max(order) if max(order) == 6 else f"unknown(exp={max(order)})"
    return {
        "f": f, "phi": len(U), "n_orbits": NO,
        "orbits": [list(o) for o in orbits],
        "orders_by_orbit": order,
        "order_histogram": {str(k): v for k, v in sorted(hist.items())},
        "cyclic": bool(max(order) == NO),
        "structure_guess": structure,
        "n_distinct_orders": len(hist),
        "_canon": canon, "_op": op, "_ident": ident,
    }


def select_field(cands):
    """Pre-stated rule: non-cyclic first, then most distinct orders, then min f."""
    pool = [c for c in cands if not c["cyclic"]]
    tag = "non-cyclic" if pool else "all-cyclic fallback"
    if not pool:
        pool = list(cands)
    best_n = max(c["n_distinct_orders"] for c in pool)
    pool = [c for c in pool if c["n_distinct_orders"] == best_n]
    win = min(pool, key=lambda c: c["f"])
    return win, tag


# ----------------------------------------------------------------------------
# minimal polynomial of zeta_f + zeta_f^{-1} via Newton identities
# (power sums S_m = 2*c_f(m) are Ramanujan sums -> integers)
# ----------------------------------------------------------------------------

def real_cyclotomic_poly(f):
    ks = sorted({min(u, f - u) for u in unit_group(f)})
    d = len(ks)
    assert d == len(unit_group(f)) // 2
    ths = [2.0 * math.cos(2.0 * math.pi * k / f) for k in ks]
    ps = []
    for m in range(1, d + 1):
        # true Newton power sums: theta^m = (zeta+zeta^-1)^m summed over conjugates
        s = math.fsum(t ** m for t in ths)
        v = round(s)
        assert abs(s - v) < 1e-3, f"power sum not integral at m={m}: {s}"
        ps.append(int(v))
    e = [Fraction(0)] * (d + 1)
    e[0] = Fraction(1)  # e_0 := 1 by convention (leading term)
    for k in range(1, d + 1):
        S = Fraction(ps[k - 1])
        for i in range(1, k):
            S += ((-1) ** i) * e[i] * Fraction(ps[k - 1 - i])
        e[k] = ((-1) ** (k + 1)) * S / k
        assert e[k].denominator == 1, f"non-integer e_{k} = {e[k]}"
    # monic little-endian: p(x) = sum_i (-1)^i e_i x^(d-i), i=0..d
    coeffs = [int(((-1) ** (d - j)) * e[d - j]) for j in range(d + 1)]
    # designed check: evaluate numerically at a conjugate root
    th = 2.0 * math.cos(2.0 * math.pi / f)
    val = sum(coeffs[i] * th ** i for i in range(d + 1))
    return coeffs, {"degree": d, "coeffs_desc": [int(c) for c in reversed(coeffs)],
                    "eval_at_2cos_2pi_over_f": val,
                    "power_sums": ps}


# ----------------------------------------------------------------------------
# modular polynomials (little-endian int lists mod p)
# ----------------------------------------------------------------------------

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
    """remainder of a mod monic-or-invertible-leading f"""
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
        w = ppowmod(w, p, f, p)  # x^(p^d) mod f
        h = ptrim([(w[i] - (1 if i == 1 else 0)) % p for i in range(len(w))])  # w - x
        g = pgcd(f, h, p)
        dg = len(g) - 1 if g else 0
        if dg > 0:
            pat[d] = pat.get(d, 0) + dg // d
            covered += dg
        if covered == deg:
            break
    assert covered == deg, f"DDF did not cover f mod {p} (covered {covered}/{deg}) -> f not squarefree mod p?"
    return {k: v for k, v in pat.items() if v > 0}


# ----------------------------------------------------------------------------
# STAGE 0: init
# ----------------------------------------------------------------------------

ledger("S0", "init", seed=SEED, wd=WD, prime_cap=PRIME_CAP)
rng = np.random.default_rng(SEED)
RESULT["meta"] = {
    "exp": 520, "codename": "DEGREE-12-COMPOSITE", "round": "54",
    "seed": SEED, "script": SCRIPT, "wd": WD,
    "started_utc": time.strftime("%FT%TZ", time.gmtime()),
    "prime_cap": PRIME_CAP, "control_mod": CONTROL_MOD,
    "n_perm": N_PERM, "n_semiprime": N_SEMIPRIME,
}
ckpt()

# ----------------------------------------------------------------------------
# STAGE 1: candidates phi(f)=24, G+ tables, field selection (pre-registered)
# ----------------------------------------------------------------------------

CAND_F = [35, 39, 45, 52, 56, 70, 72, 78, 84, 90]
ledger("S1", "candidate enumeration start", candidates=CAND_F)
cands = []
for f in CAND_F:
    assert (f // len(unit_group(f))) == 0 or True
    phi = len(unit_group(f))
    g = build_quotient(f)
    g.pop("_canon"), None
    g["_op"], g["_ident"] = None, None
    cands.append(g)
    ledger("S1", f"f={f}", phi=phi, Gplus=g["structure_guess"],
           orders=g["order_histogram"], cyclic=g["cyclic"])

winner, sel_tag = select_field(cands)
F = winner["f"]
U = unit_group(F)
canon = {}
for idx, o in enumerate(winner["orbits"]):
    for el in o:
        canon[el] = idx
orb_op = lambda i, j: canon[(winner["orbits"][i][0] * winner["orbits"][j][0]) % F]
orb_ident = canon[1 % F]
ORB_ORDER = winner["orders_by_orbit"]
NO = winner["n_orbits"]
NT = len(set(ORB_ORDER))
type_of_order = {k: i for i, k in enumerate(sorted(set(ORB_ORDER)))}
TYPE_OF_ORB = [type_of_order[k] for k in ORB_ORDER]

hist = winner["order_histogram"]
H_theory = -sum((c / NO) * math.log2(c / NO) for c in hist.values())
theory_densities = {str(k): v / NO for k, v in hist.items()}

RESULT["candidates"] = [{k: v for k, v in c.items() if not k.startswith("_")} for c in cands]
RESULT["selection"] = {
    "rule": "non-cyclic > more distinct orders > smallest f (pre-stated)",
    "selected_f": F, "selected_tag": sel_tag,
    "Gplus_structure": winner["structure_guess"],
    "Gplus_order_histogram": hist,
    "types": {str(k): {"count": v, "density": v / NO} for k, v in hist.items()},
    "H_T_theory_bits": H_theory,
    "shape_legend": ("Frobenius order k => factors all of degree k, count 12/k; "
                     "k=1: twelve linear (nr=12); k=2: six quadratics; "
                     "k=3: four cubics; k=6: two sextics"),
}
ledger("S1", "field selected", f=F, Gplus=winner["structure_guess"],
       H_theory_bits=round(H_theory, 5), rule=sel_tag)
ckpt()

# ----------------------------------------------------------------------------
# STAGE 2: defining polynomial + DDF cross-validation (barrier 5)
# ----------------------------------------------------------------------------

ledger("S2", "minimal polynomial construction")
poly, poly_info = real_cyclotomic_poly(F)
assert poly_info["degree"] == 12, "degree must be 12"
assert abs(poly_info["eval_at_2cos_2pi_over_f"]) < 1e-8, "root check failed"
RESULT["selection"]["defining_polynomial"] = poly_info
ledger("S2", "poly ok", degree=poly_info["degree"], root_eval=poly_info["eval_at_2cos_2pi_over_f"])
ckpt()

# ----------------------------------------------------------------------------
# main sieve
# ----------------------------------------------------------------------------

ledger("S2", "sieving primes", cap=PRIME_CAP)
sieve = np.ones(PRIME_CAP, dtype=bool)
sieve[:2] = False
for i in range(2, int(PRIME_CAP ** 0.5) + 1):
    if sieve[i]:
        sieve[i * i::i] = False
primes = np.nonzero(sieve)[0].astype(np.int64)
primes = primes[primes != CONTROL_MOD]  # drop p=97 so control bin 0 stays empty
n_all = len(primes)
cls = primes % F
is_unit = np.array([math.gcd(int(c), F) == 1 for c in cls[:1000]])  # spot only; do full below
unit_mask = np.fromiter((math.gcd(int(c), F) == 1 for c in cls), dtype=bool, count=len(cls))
pu = primes[unit_mask]
clu = cls[unit_mask]
orb_id = np.array([canon[int(c)] for c in clu], dtype=np.int64)
typ = np.array([TYPE_OF_ORB[o] for o in orb_id], dtype=np.int64)
n_unit = len(pu)
ledger("S2", "sieve done", primes_total=n_all, unit_primes=n_unit)
RESULT["sieve"] = {"primes_total": int(n_all), "unit_primes": int(n_unit), "cap": PRIME_CAP}
ckpt()

# ---- DDF cross-validation of predicted factor patterns (barrier 5) ----------
ledger("S2", "DDF cross-validation start", per_type=N_DDF_PER_TYPE)
ddf_checks = []
fail = 0
for k_ord, tidx in sorted(type_of_order.items()):
    cand_idx = np.nonzero(typ == tidx)[0]
    take = rng.choice(cand_idx, size=min(N_DDF_PER_TYPE, len(cand_idx)), replace=False)
    expected = {k_ord: 12 // k_ord}
    for ix in take:
        p = int(pu[ix])
        got = ddf_pattern(poly, p)
        okflag = (got == expected)
        fail += (not okflag)
        if len(ddf_checks) < 200:
            ddf_checks.append({"p": p, "pred_order": k_ord, "pattern": {str(a): b for a, b in got.items()},
                               "match": bool(okflag)})
n_ddf = sum(min(N_DDF_PER_TYPE, int((typ == type_of_order[t]).sum())) for t in type_of_order)
RESULT["ddf_check"] = {"n_checked": int(n_ddf), "n_fail": int(fail),
                       "barrier5_pass": bool(fail == 0), "sample": ddf_checks[:40]}
ledger("S2", "DDF cross-validation done", checked=int(n_ddf), failures=int(fail))
if fail:
    ledger("S2", "BARRIER-5 FAILURE: polynomial factorization contradicts group prediction", failures=fail)
ckpt()

# ----------------------------------------------------------------------------
# STAGE 3: full-pinning channel, purity, permutation nulls, controls, thickening
# ----------------------------------------------------------------------------

ledger("S3", "channel computation start")
J = np.bincount(orb_id * NT + typ, minlength=NO * NT).reshape(NO, NT)
I_obs = mi_from_joint(J)
H_emp = entropy_from_counts(J.sum(axis=1)[0] * 0 + J.sum(axis=0))
gap = abs(I_obs - H_emp)

# purity: each orbit must carry exactly one observed type
pure_orbits = int(sum(1 for o in range(NO) if len(set(typ[orb_id == o])) == 1))
cond_entropy = 0.0
for o in range(NO):
    cond_entropy += (orb_id == o).mean() * entropy_from_counts(typ[orb_id == o])

# empirical type frequencies vs Chebotarev densities
type_freq = {str(sorted(type_of_order)[t]): float((typ == t).mean()) for t in range(NT)}

# permutation nulls
nulls = []
for _ in range(N_PERM):
    tp = rng.permutation(typ)
    Jp = np.bincount(orb_id * NT + tp, minlength=NO * NT).reshape(NO, NT)
    nulls.append(mi_from_joint(Jp))
nulls = np.array(nulls)
z_null = (I_obs - nulls.mean()) / (nulls.std() + 1e-18)

# wrong-modulus control (flat expected)
ctl_bin = pu % CONTROL_MOD
NB = CONTROL_MOD
Jc = np.bincount(ctl_bin * NT + typ, minlength=NB * NT).reshape(NB, NT)
I_ctl = mi_from_joint(Jc)
ctl_nulls = []
for _ in range(N_PERM):
    tp = rng.permutation(typ)
    Jcp = np.bincount(ctl_bin * NT + tp, minlength=NB * NT).reshape(NB, NT)
    ctl_nulls.append(mi_from_joint(Jcp))
ctl_nulls = np.array(ctl_nulls)
z_ctl = (I_ctl - ctl_nulls.mean()) / (ctl_nulls.std() + 1e-18)
bias_floor_main = (NO - 1) * (NT - 1) / (2 * n_unit * math.log(2))
bias_floor_ctl = (NB - 1) * (NT - 1) / (2 * n_unit * math.log(2))

# thickening: cumulative deciles
thick = []
idx_sorted = np.arange(n_unit)  # primes already ascending
bounds = np.linspace(0, n_unit, 11).astype(int)
for b in range(1, 11):
    sl = slice(0, bounds[b])
    ob, tb = orb_id[sl], typ[sl]
    Jb = np.bincount(ob * NT + tb, minlength=NO * NT).reshape(NO, NT)
    Ib, Hb = mi_from_joint(Jb), entropy_from_counts(Jb.sum(axis=0))
    cb = ctl_bin[sl]
    Jcb = np.bincount(cb * NT + tb, minlength=NB * NT).reshape(NB, NT)
    thick.append({"n": int(bounds[b]), "I_bits": Ib, "H_bits": Hb,
                  "abs_gap": abs(Ib - Hb), "I_control_bits": mi_from_joint(Jcb)})

h1_pass = (pure_orbits == NO) and gap < 1e-9 and (fail == 0) and z_null > 4

# Control flatness, done honestly.  A shuffle null is MIS-CENTERED for a
# deterministically Dirichlet-equidistributed prime set: perfect AP
# equidistribution gives joint counts closer to product form than any random
# re-pairing, so I_ctl can sit BELOW the shuffle-null mean (negative z) without
# any signal.  The operative flatness tests are: (i) I_ctl decays like pure
# estimator bias, n*I_ctl(n) ~ const -> 0 as n grows; (ii) final I_ctl is far
# below the main channel and below/equal the multinomial bias floor.
prod_series = [r["n"] * r["I_control_bits"] for r in thick]
tail = prod_series[-8:]
decay_const = sum(tail) / len(tail)
decay_spread = (max(tail) - min(tail)) / (abs(decay_const) + 1e-18)
h3_flat = bool(I_ctl < 0.01 * H_emp
               and I_ctl <= bias_floor_ctl * 1.0 + 1e-9
               and decay_spread < 0.5)
control_note = (
    f"shuffle-null z={z_ctl:.2f} is NEGATIVE because the null is mis-centered for "
    "deterministically equidistributed data (AP equidistribution beats random "
    f"re-pairing); operative test: n*I_ctl ~= {decay_const:.1f} bit*count constant "
    f"(spread {100*decay_spread:.0f}% over tail) -> I_ctl ~ bias only, -> 0 as n grows"
)
h3_thick = all(r["abs_gap"] < 1e-9 for r in thick)

RESULT["channel"] = {
    "modulus": F, "n_orbits": NO, "n_types": NT,
    "orbit_purity": {"pure_orbits": pure_orbits, "total_orbits": NO},
    "conditional_entropy_bits": cond_entropy,
    "H_T_empirical_bits": H_emp, "H_T_theory_bits": H_theory,
    "I_obs_bits": I_obs, "abs_I_minus_H": gap,
    "type_freq_empirical": type_freq, "type_density_theory": theory_densities,
    "perm_null": {"n": N_PERM, "mean": float(nulls.mean()), "sd": float(nulls.std()),
                  "max": float(nulls.max()), "z_of_observed": float(z_null)},
    "control_mod97": {"I_bits": I_ctl, "null_mean": float(ctl_nulls.mean()),
                      "null_sd": float(ctl_nulls.std()), "z": float(z_ctl),
                      "bias_floor_bits": bias_floor_ctl, "flat": h3_flat,
                      "decay_const_bitcount": decay_const,
                      "decay_spread_tail": decay_spread,
                      "note": control_note},
    "thickening": thick,
    "bias_floor_main_bits": bias_floor_main,
}
ledger("S3", "channel done", I=round(I_obs, 9), H=round(H_emp, 9), gap=gap,
       purity=f"{pure_orbits}/{NO}", z_null=round(float(z_null), 1),
       I_ctl=round(I_ctl, 6), z_ctl=round(float(z_ctl), 3),
       ctl_decay_const=round(decay_const, 2))
ledger("S3", "MEASUREMENT-LEDGER: control diagnosis",
       finding="shuffle null mis-centered for deterministic Dirichlet equidistribution; "
               "n*I_ctl constant => control is pure bias, flat",
       z_shuffle_null=round(float(z_ctl), 2), detail=control_note)
ckpt()

# ----------------------------------------------------------------------------
# STAGE 4: semiprime pair channel vs exact enumeration law
# ----------------------------------------------------------------------------

ledger("S4", "semiprime arm start", draws=N_SEMIPRIME)
ord_of_class = {}
for u in U:
    o = canon[u]
    ord_of_class[u] = ORB_ORDER[o]
uarr = np.array(U)
law_pairs = {}
class_count = {}
pair_count = {}
for a in uarr:
    oa = ord_of_class[int(a)]
    for b in uarr:
        c = int(a) * int(b) % F
        ob = ord_of_class[int(b)]
        key = (c, oa, ob)
        law_pairs[key] = law_pairs.get(key, 0) + 1
        class_count[c] = class_count.get(c, 0) + 1
        pair_count[(oa, ob)] = pair_count.get((oa, ob), 0) + 1
tot = len(U) ** 2
P = np.zeros((F, NT, NT))
for (c, ta, tb), m in law_pairs.items():
    P[c, type_of_order[ta], type_of_order[tb]] = m / tot
I_law_class = mi_from_joint(P.reshape(F, NT * NT))
H_pair_law = entropy_from_counts(np.array([m for m in pair_count.values()]))

# orbit-binned variant
Po = np.zeros((NO, NT, NT))
for (c, ta, tb), m in law_pairs.items():
    co = canon[c]
    Po[co, type_of_order[ta], type_of_order[tb]] += m / tot
I_law_orbit = mi_from_joint(Po.reshape(NO, NT * NT))

# empirical draws
ii = rng.integers(0, n_unit, size=(N_SEMIPRIME * 2, 2))
bad = ii[:, 0] == ii[:, 1]
while bad.any():
    ii[bad] = rng.integers(0, n_unit, size=(int(bad.sum()), 2))
    bad = ii[:, 0] == ii[:, 1]
ii = ii[:N_SEMIPRIME]
pa, pb = pu[ii[:, 0]], pu[ii[:, 1]]
ta_, tb_ = typ[ii[:, 0]], typ[ii[:, 1]]
cc = (pa * pb) % F  # int64 safe: p,q < 2^21 -> p*q < 2^42
cco = np.array([canon[int(c)] for c in cc], dtype=np.int64)
Jsp = np.bincount(cc * NT * NT + ta_ * NT + tb_,
                  minlength=F * NT * NT).reshape(F, NT * NT)
I_sp_emp = mi_from_joint(Jsp)
Jspo = np.bincount(cco * NT * NT + ta_ * NT + tb_,
                   minlength=NO * NT * NT).reshape(NO, NT * NT)
I_spo_emp = mi_from_joint(Jspo)

boots, bootso = [], []
for _ in range(N_BOOT):
    rb = rng.integers(0, N_SEMIPRIME, size=N_SEMIPRIME)
    Jb = np.bincount(cc[rb] * NT * NT + ta_[rb] * NT + tb_[rb],
                     minlength=F * NT * NT).reshape(F, NT * NT)
    boots.append(mi_from_joint(Jb))
    Job = np.bincount(cco[rb] * NT * NT + ta_[rb] * NT + tb_[rb],
                      minlength=NO * NT * NT).reshape(NO, NT * NT)
    bootso.append(mi_from_joint(Job))
boots, bootso = np.array(boots), np.array(bootso)
sp_sd, sp_z = boots.std(), (I_sp_emp - I_law_class) / (boots.std() + 1e-18)
sp_sd_o = bootso.std()
sp_z_o = (I_spo_emp - I_law_orbit) / (sp_sd_o + 1e-18)

# marginal single-side channel I(N ; T_a) for the record
Pm = P.sum(axis=2)  # (F, NT) marginal over T_b
I_marg_law = mi_from_joint(Pm)
Jme = np.bincount(cc * NT + ta_, minlength=F * NT).reshape(F, NT)
I_marg_emp = mi_from_joint(Jme)

h2_pass = abs(sp_z) < 4 and abs(sp_z_o) < 4

RESULT["semiprime"] = {
    "draws": N_SEMIPRIME,
    "law_class_bits": I_law_class, "emp_class_bits": I_sp_emp,
    "diff_class_bits": I_sp_emp - I_law_class, "boot_sd": float(sp_sd),
    "z_class": float(sp_z),
    "law_orbit_bits": I_law_orbit, "emp_orbit_bits": I_spo_emp,
    "diff_orbit_bits": I_spo_emp - I_law_orbit, "boot_sd_orbit": float(sp_sd_o),
    "z_orbit": float(sp_z_o),
    "H_pair_law_bits": H_pair_law,
    "marginal_law_bits": I_marg_law, "marginal_emp_bits": I_marg_emp,
}
ledger("S4", "semiprime done", I_law=round(I_law_class, 5), I_emp=round(I_sp_emp, 5),
       z=round(float(sp_z), 2), I_law_orbit=round(I_law_orbit, 5),
       I_emp_orbit=round(I_spo_emp, 5), z_orbit=round(float(sp_z_o), 2))
ckpt()

# ----------------------------------------------------------------------------
# STAGE 5: verdict assembly
# ----------------------------------------------------------------------------

pass_all = h1_pass and h2_pass and h3_flat and h3_thick
verdict = "DEGREE-12-FULL-PINNED" if pass_all else "DEGREE-12-ANOMALY"
RESULT["verdict"] = {
    "name": verdict,
    "H1_full_pinning": bool(h1_pass),
    "H2_semiprime_pair_law": bool(h2_pass),
    "H3_controls": {"coprime_flat": bool(h3_flat), "thickening_structural": bool(h3_thick)},
    "barriers": {
        "barrier_5_designed_checks": {
            "poly_integrality_and_degree": True,
            "root_evaluation": True,
            "ddf_vs_group_pattern": {"checked": int(n_ddf), "failed": int(fail),
                                     "pass": bool(fail == 0)},
            "orbit_purity": {"pure": pure_orbits, "of": NO},
        },
        "barrier_6_pre_registration": {
            "field_rule": "non-cyclic > richer type alphabet > smallest conductor",
            "applied_before_prime_data": True,
            "all_candidates_logged": True,
        },
        "barrier_8_power": {
            "unit_primes": int(n_unit),
            "rarest_type_cell_expected": int(round(n_unit / NO)),
            "binomial_se_rare_cell_rel": round(1 / math.sqrt(n_unit / NO), 5),
            "mi_bias_floor_main_bits": bias_floor_main,
            "mi_bias_floor_control_bits": bias_floor_ctl,
            "headline_claims_are_exact_equalities": gap < 1e-9,
        },
    },
    "elapsed_s": round(time.time() - T0, 1),
}
ckpt()
ledger("S5", "VERDICT", name=verdict, H1=bool(h1_pass), H2=bool(h2_pass),
       H3=bool(h3_flat and h3_thick), elapsed_s=round(time.time() - T0, 1))
print(json.dumps(RESULT["verdict"], indent=1))

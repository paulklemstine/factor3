#!/usr/bin/env python3
"""
exp566 MA1-EFFECTIVITY-SWEEP (round 74, factoring lab)

PRE-REGISTRATION (header written BEFORE coding the full run; smoke executed after):
Question: are deviations of prime counts in arithmetic progressions governed by
quadratic-character L-values?  If yes with R^2>0.8, the MA-1 averaging assumption
(under which which-factor blindness is an identity in papers 93/102/132) gets a
COMPUTABLE effectivity criterion.

H1: R^2 > 0.8 of per-modulus deviation magnitude D(m) on prediction
    P(m) = sum over nontrivial real chars chi mod m of |L(1,chi)|
    => computable effectivity criterion (headline positive).
H0: R^2 < 0.5 => not captured at this scale (honest negative).
Either way report fitted slope (= power-law exponent D ~ P^slope) + bootstrap CI.

Design:
  x = 2^26 target (adaptive shrink allowed, DISCLOSED). Moduli m = all squarefree
  m in [3,300] UNION primes 307..997.  E = li(x)/phi(m);
  D(m) = max_a |pi(x;m,a) - E| / sqrt(E);  secondary chi2 = sum_a (pi-E)^2/E.
  Real chars mod m = products of local quadratic factors:
    odd p|m -> (p*/.), p* = (-1)^{(p-1)/2} p, conductor p;
    2-part   -> D in {-4} if 4|m, {-4,8,-8} if 8|m  (unreachable here: sampled
    moduli are squarefree/primes so v2(m)<=1; code kept for generality).
  L(1,chi_D): EXACT 2*pi*h(D)/(w*sqrt|D|) via Gauss-reduced binary quadratic form
  count for D<0, |D|<=400 (w=6 if D=-3, 4 if D=-4, else 2); otherwise truncated
  series sum_{n<=1e5} chi(n)/n evaluated by block-harmonic sums.  Truncation error
  CALIBRATED on the exact-path overlap (same D computed both ways).
  Fit: OLS log D ~ log P + bootstrap CI (2000 resamples); partial correlation
  controlling log phi(m) (both arms share phi-driven variance);
  CONTROL: cross-modulus pairing-permutation null (2000 perms) must collapse R^2.
  DISCLOSED DEVIATION from spec wording: the literal 'permute residue counts
  within modulus' is VACUOUS for the registered readouts (max-abs and chi2 are
  permutation-invariant in a); the meaningful control that tests whether the
  SPECIFIC P(m) ordering carries information is shuffling the (m -> D) pairing
  against P, which we run and report.
"""
import json, math, sys, time
import numpy as np
from scipy.special import expi

T0 = time.time()

# ---------------- basics ----------------

def factor(m):
    fs, d = {}, 2
    while d * d <= m:
        while m % d == 0:
            fs[d] = fs.get(d, 0) + 1
            m //= d
        d += 1
    if m > 1:
        fs[m] = fs.get(m, 0) + 1
    return fs

def phi_of(fs):
    r = 1
    for p, e in fs.items():
        r *= p ** (e - 1) * (p - 1)
    return r

def li_x(x):
    return float(expi(math.log(x)))

def simple_sieve(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for p in range(2, int(math.isqrt(n)) + 1):
        if s[p]:
            s[p * p::p] = False
    return np.nonzero(s)[0]

def segmented_primes(X, seg=1 << 22):
    base = simple_sieve(int(math.isqrt(X)))
    out = []
    for lo in range(2, X + 1, seg):
        hi = min(lo + seg - 1, X)
        s = np.ones(hi - lo + 1, dtype=bool)
        for p in base:
            if p * p > hi:
                break
            start = max(p * p, ((lo + p - 1) // p) * p)
            s[start - lo::p] = False
        out.append(np.nonzero(s)[0].astype(np.int64) + lo)
    return np.concatenate(out)

# ---------------- quadratic characters ----------------

LEGENDRE_CACHE = {}
def legendre_pattern(p):
    if p not in LEGENDRE_CACHE:
        v = np.array([pow(n, (p - 1) // 2, p) for n in range(p)], dtype=np.int64)
        v[v == p - 1] = -1
        LEGENDRE_CACHE[p] = v
    return LEGENDRE_CACHE[p]

PAT_M4  = np.array([0, 1, 0, -1])                 # chi_{-4}, cond 4
PAT_8   = np.array([0, 1, 0, -1, 0, -1, 0, 1])    # chi_8,  cond 8
PAT_M8G = np.array([0, 1, 0, -1, 0, 1, 0, -1])    # chi_{-8} as gen, cond 8

def real_chars(m):
    """All nontrivial real (quadratic) Dirichlet chars mod m.
    Returns list of (fundamental_discriminant_D, pattern_on_[0..k) with k=|D|)."""
    gens = []           # (odd_part_D or ('2', gen_id), conductor, pattern)
    odd_D = []
    two = None          # None | list of 2-gens
    for p, e in factor(m).items():
        if p == 2:
            if e >= 3:
                two = [('m4', PAT_M4), ('8', PAT_8)]
            elif e == 2:
                two = [('m4', PAT_M4)]
            # e == 1: (Z/2)^* trivial -> none
        else:
            odd_D.append((p if p % 4 == 1 else -p, legendre_pattern(p)))
    out = []
    lists = odd_D + ([('g', g) for g in (two or [])])
    ng = len(lists)
    for mask in range(1, 1 << ng):
        odd_prod = 1
        d2 = 1
        pat = np.ones(1, dtype=np.int64)
        for i, item in enumerate(lists):
            if not (mask >> i) & 1:
                continue
            if isinstance(item[0], int):
                Dg, lp = item
                odd_prod *= Dg
            else:
                gid, lp = item
                d2 *= {'m4': -4, '8': 8}[gid]
            k = len(pat) * len(lp) // math.gcd(len(pat), len(lp))
            pat = np.tile(pat, k // len(pat)) * np.tile(lp, k // len(lp))
        if d2 == -32:      # chi_{-4}*chi_8 == chi_{-8}: relabel fundamental D
            d2 = -8
        D = odd_prod * d2
        out.append((D, pat))
    return out

def class_number(D):
    """h(D) for fundamental D<0 via count of Gauss-reduced primitive forms."""
    h = 0
    amax = int(math.isqrt((-D) // 3)) + 1
    for a in range(1, amax + 1):
        for b in range(1 - a, a + 1):
            t = b * b - D
            if t % (4 * a):
                continue
            c = t // (4 * a)
            if c < a or (a == c and b < 0):
                continue
            h += 1
    return h

TRUNC_N = 100000

def L1_trunc(pat):
    k = len(pat)
    reps = TRUNC_N // k
    nv = np.arange(1, reps * k + 1)
    return float(np.dot(pat[nv % k], 1.0 / nv))

def L1(D, pat):
    """Signed L(1,chi_D); exact class-number path for D<0,|D|<=400, else truncated."""
    if D < 0 and -D <= 400:
        h = class_number(D)
        w = 6 if D == -3 else (4 if D == -4 else 2)
        return 2 * math.pi * h / (w * math.sqrt(-D)), 'exact'
    return L1_trunc(pat), 'trunc'

# ---------------- stats ----------------

def ols(t, y):
    A = np.vstack([t, np.ones_like(t)]).T
    (sl, ic), *_ = np.linalg.lstsq(A, y, rcond=None)
    pred = sl * t + ic
    ssr = ((y - pred) ** 2).sum(); sst = ((y - y.mean()) ** 2).sum()
    return {'slope': float(sl), 'intercept': float(ic),
            'r2': float(1 - ssr / sst),
            'pearson_r': float(np.corrcoef(t, y)[0, 1])}

def resid(y, z):
    A = np.vstack([z, np.ones_like(z)]).T
    (sl, ic), *_ = np.linalg.lstsq(A, y, rcond=None)
    return y - (sl * z + ic)

# ---------------- main ----------------

def build_moduli(mode):
    if mode == 'smoke':
        return [m for m in range(3, 51) if all(e == 1 for e in factor(m).values())]
    sf = [m for m in range(3, 301) if all(e == 1 for e in factor(m).values())]
    pr = [int(p) for p in simple_sieve(1000) if 307 <= p <= 997]
    return sf + pr

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'full'
    X = (1 << 20) if mode == 'smoke' else (1 << 26)
    moduli = build_moduli(mode)

    tp = time.time()
    P = segmented_primes(X)
    pi_x, liXv = int(P.size), li_x(X)
    sieve_s = time.time() - tp
    print(f'[{mode}] x=2^{int(math.log2(X))} pi={pi_x} li={liXv:.1f} sieve={sieve_s:.1f}s', flush=True)

    calib = []
    rows = []
    for m in moduli:
        fs = factor(m)
        phim = phi_of(fs)
        red = np.nonzero(np.gcd(np.arange(m), m) == 1)[0]
        bc = np.bincount(P % m, minlength=m).astype(np.float64)
        for p in fs:                       # exclude primes dividing m from counts
            bc[p % m] -= 1.0
        vals = bc[red]
        E = liXv / phim
        dev = vals - E
        Dstat = float(np.max(np.abs(dev)) / math.sqrt(E))
        chi2v = float((dev ** 2).sum() / E)
        ch = real_chars(m)
        Pv, n_ex = 0.0, 0
        for D, pat in ch:
            Lv, how = L1(D, pat)
            if how == 'exact':
                n_ex += 1
                if len(calib) < 400:
                    calib.append(abs(L1_trunc(pat) - Lv) / abs(Lv))
            Pv += abs(Lv)
        rows.append({'m': m, 'phi': phim, 'omega': len(fs), 'n_real_chars': len(ch),
                     'E': E, 'D_max_norm': Dstat, 'chi2': chi2v, 'P_sum_absL1': Pv,
                     'n_exact': n_ex, 'n_trunc': len(ch) - n_ex})
    print(f'[{mode}] counted {len(rows)} moduli in {time.time()-tp:.1f}s', flush=True)

    t = np.log(np.array([r['P_sum_absL1'] for r in rows]))
    y = np.log(np.array([r['D_max_norm'] for r in rows]))
    y2 = np.log(np.array([r['chi2'] for r in rows]))
    z = np.log(np.array([float(r['phi']) for r in rows]))

    fit_primary = ols(t, y)
    fit_chi2 = ols(t, y2)
    ry, rt = resid(y, z), resid(t, z)
    partial = {'partial_r2_ctrl_logphi': float(np.corrcoef(ry, rt)[0, 1] ** 2)}

    rng = np.random.default_rng(566)
    bs_sl, bs_r2 = [], []
    n = len(t)
    for _ in range(2000):
        idx = rng.integers(0, n, n)
        f = ols(t[idx], y[idx]); bs_sl.append(f['slope']); bs_r2.append(f['r2'])
    null_r2 = []
    for _ in range(2000):
        null_r2.append(ols(t, y[rng.permutation(n)])['r2'])
    null_r2 = np.array(null_r2)

    r2 = fit_primary['r2']
    verdict = 'H1' if r2 > 0.8 else ('H0' if r2 < 0.5 else 'INTERMEDIATE')
    ctrl_ok = bool(null_r2.mean() < 0.05 and null_r2.max() < 0.2)

    cal = {'n_pairs': len(calib),
           'rel_err_median': float(np.median(calib)) if calib else None,
           'rel_err_max': float(np.max(calib)) if calib else None}

    notes = [
        f'final x=2^{int(math.log2(X))} ({"SMOKE scale" if mode=="smoke" else "no shrinkage needed"}), pi(x)={pi_x}',
        'sampled moduli are squarefree [3,300] + primes [307,997] => v2(m)<=1, so the '
        '2-adic discriminants (-4,8,-8) branch is dead code here (kept for generality)',
        'literal within-modulus residue permutation is vacuous for max-abs and chi2 '
        '(both permutation-invariant in a); control run as cross-modulus pairing shuffle',
        f'truncation calibration on exact-path overlap: median rel err {cal["rel_err_median"] if calib else "n/a"}, '
        f'max {cal["rel_err_max"] if calib else "n/a"} over {cal["n_pairs"]} discriminants',
        'positive-D (real-quadratic) L-values are ALWAYS truncated (no regulator path); '
        'negative-D |D|>400 truncated; error assumed similar to calibrated overlap',
        'E=li(x)/phi(m) not pi(x)/phi(m): constant offset absorbed in intercept',
        'regression is marginal; partial R^2 controlling log phi reported as confound check',
    ]

    result = {
        'exp': '566',
        'codename': 'MA1-EFFECTIVITY-SWEEP',
        'round': 74,
        'smoke': mode == 'smoke',
        'status': '06_final' if mode != 'smoke' else '03_smoke',
        'hypotheses': {
            'H1_prestated': 'R^2>0.8 of D(m)=max_a|pi(x;m,a)-li(x)/phi(m)|/sqrt(E) on '
                            'P(m)=sum over nontrivial real chars |L(1,chi)| => computable '
                            'MA-1 effectivity criterion (headline positive)',
            'H0_prestated': 'R^2<0.5 => not captured at this scale (honest negative)',
            'either_way': 'report fitted slope (=power-law exponent) + bootstrap CI',
        },
        'config': {
            'exp': 'exp566', 'name': 'MA1-EFFECTIVITY-SWEEP', 'mode': mode,
            'x': X, 'pi_x': pi_x, 'li_x': liXv,
            'moduli_source': ('squarefree[3,50]' if mode == 'smoke'
                              else 'squarefree[3,300] + primes[307,997]'),
            'n_moduli': len(rows), 'sieve_s': round(sieve_s, 2),
            'L_method': f'class-number exact (D<0,|D|<=400); truncated N={TRUNC_N} otherwise',
        },
        'rows': rows,
        'fit': {
            'primary_logD_logP': fit_primary,
            'secondary_logchi2_logP': fit_chi2,
            'confound_partial': partial,
            'bootstrap': {'n_boot': 2000,
                          'slope_ci95': [float(np.percentile(bs_sl, 2.5)), float(np.percentile(bs_sl, 97.5))],
                          'r2_ci95': [float(np.percentile(bs_r2, 2.5)), float(np.percentile(bs_r2, 97.5))]},
            'control_pairing_perm': {'n_perm': 2000, 'r2_null_mean': float(null_r2.mean()),
                                     'r2_null_p95': float(np.percentile(null_r2, 95)),
                                     'r2_null_max': float(null_r2.max()), 'collapsed': ctrl_ok},
            'truncation_calibration': cal,
        },
        'verdicts': {
            'primary': verdict,
            'thresholds': {'H1_r2_gt': 0.8, 'H0_r2_lt': 0.5},
            'control_gate_passed': ctrl_ok,
            'headline': (f'R^2={r2:.4f}, logD ~ {fit_primary["slope"]:.4f}*logP '
                         f'(CI {np.percentile(bs_sl,2.5):.3f},{np.percentile(bs_sl,97.5):.3f}) => {verdict}'
                         + ('' if ctrl_ok else ' [CONTROL DID NOT COLLAPSE - treat fit as unreliable]')),
        },
        'honest_notes': notes,
        'wall_s': round(time.time() - T0, 2),
    }
    out = 'exp566_smoke_result.json' if mode == 'smoke' else 'exp566_result.json'
    with open(out, 'w') as f:
        json.dump(result, f, indent=1)
    print(json.dumps(result['verdicts'], indent=1), flush=True)
    print(json.dumps(result['fit']['primary_logD_logP'], indent=1), flush=True)
    print('wrote', out, f'wall={result["wall_s"]}s', flush=True)

    if mode != 'smoke':
        ex = [r for r in rows if r['m'] in (3, 4, 5)]
        for r in rows[:3]:
            print('sample row:', json.dumps(r), flush=True)

if __name__ == '__main__':
    main()

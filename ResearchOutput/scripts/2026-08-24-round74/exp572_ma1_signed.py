#!/usr/bin/env python3
"""
exp572 MA1-SIGNED (round 74, factoring lab)

PRE-REGISTRATION (header written BEFORE any data was produced; smoke executed
immediately after this file was written, per lab rules):

Background. Paper 213 / exp566 bounded the MAGNITUDE route of MA-1 effectivity:
quadratic |L(1,chi)| does not predict |AP deviations| (R^2=0.019, CI [0.001,0.065]).
exp566's scoping caveat preserved the SIGNED route: do signed character
components ALIGN with deviation patterns even though magnitudes don't track?

Identity used (exact, asserted in smoke): with d_a = pi(x;m,a) - li(x)/phi(m)
over unit classes a,
    c_chi = sum_a d_a * chi(a) = sum_{p<=x} chi(p),
because sum_a chi(a)*li(x)/phi(m) = 0 by character orthogonality. Hence the
NAIVE li-based theory character sum vanishes IDENTICALLY and predicts no sign;
the only computable x-independent theory object carried by chi alone is its
signed L(1,chi). For REAL characters arg(L(1,chi)) in {0,pi} carries no
information beyond sign(L(1,chi)), so the single pre-registered theory weight is

    w_chi = L(1,chi)   (signed; exp566 paths reused verbatim: class-number
                        exact for fundamental D<0, |D|<=400; truncated series
                        otherwise; exp566 calibrated median rel err 1.8e-5).

H1 (signed structure): sign pattern s(m,a)=sign(pi(x;m,a)-li(x)/phi(m))
    correlates with the L-value-predicted pattern ABOVE CHANCE across moduli,
    measured by EITHER registered criterion:
      (C1) cell-level sign-agreement rate r = Pr[ sign(c_chi)=sign(w_chi) ]
           over ALL nontrivial-real-char (m,chi) cells has Clopper-Pearson 95%
           CI entirely above 0.5;
      (C2) circular-sum statistic CS = sum_cells sign(w)*sign(c) has
           shuffle-null z = (CS-mean)/sd > 3 (null: d_a shuffled WITHIN each
           modulus, 2000 draws).
    Class-level analogue (per H1 text): agreement of sign(d_a) with
    sign(sum_{chi!=prin} w_chi*chi(a)) over unit classes, same criteria.
H0: agreement <= chance under both criteria at both levels => the signed route
    is dead at this scale too => MA-1 computable-effectivity program CLOSED on
    BOTH routes (honest negative strengthening paper 213).

Direction disclosure: NO theorem forces sign(c_chi(x)) to follow sign(L(1,chi));
the motivation is the Mertens/Euler-product link log L(1,chi) ~ sum_p chi(p)/p
making L(1,chi)'s sign a candidate low-frequency summary of the chi-twisted
prime bias. Registered one-sided (>chance) per the program statement; two-sided
readouts also reported. Within-modulus d-shuffle is MEANINGFUL here (unlike
exp566's max/chi2 readouts): sign(c) is not permutation-invariant in a.

Design (machinery reused VERBATIM from exp566_ma1_effectivity.py):
  x=2^26; moduli = squarefree [3,300] UNION primes [307,997]; segmented sieve;
  E=li(x)/phi(m); deviations over UNIT classes only (non-unit classes contain
  <=1 prime each -- the single-prime artifact -- and carry chi(a)=0 anyway);
  real chars mod m = products of local quadratic factors (exp566 real_chars);
  observed c_chi = CH @ d (asserted == direct prime-twist sum in smoke);
  breakdowns: omega(m)=1 (single Legendre char) vs omega>=2 (product chars);
  exact-path vs truncated-L cells; robustness dropping |w|<1e-3 cells
  (truncation-sign-flip guard, >> calibrated rel err).
Smoke: x=2^22, moduli<=120, <60 s, asserts: orthogonality identity exact,
  L(1,chi_-3)=pi/(3sqrt(3)), L(1,chi_5)=2*log(phi)/sqrt(5)~0.4304.
Full budget: <=12 min wall (analysis-heavy, sieve-bound).
Either verdict closes a named barrier-map question ("MA-1 effectivity",
second/signed route): H1 => first computable handle on AP-deviation STRUCTURE;
H0 => program closed both routes, negative strengthens paper 213.
"""
import json, math, sys, time
import numpy as np
from scipy.special import expi, digamma
from scipy.stats import beta as beta_dist

T0 = time.time()

# ---------------- basics (verbatim from exp566) ----------------

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

# ---------------- quadratic characters (verbatim from exp566) ----------------

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
    gens = []
    odd_D = []
    two = None
    for p, e in factor(m).items():
        if p == 2:
            if e >= 3:
                two = [('m4', PAT_M4), ('8', PAT_8)]
            elif e == 2:
                two = [('m4', PAT_M4)]
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
        if d2 == -32:
            d2 = -8
        D = odd_prod * d2
        out.append((D, pat))
    return out

def class_number(D):
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

# ---------------- exp572-specific ----------------

def clopper_pearson(k, n, alpha=0.05):
    lo = 0.0 if k == 0 else float(beta_dist.ppf(alpha / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta_dist.ppf(1 - alpha / 2, k + 1, n - k))
    return lo, hi

def within_modulus_shuffles(d, S, rng):
    """S row-shuffles of d (permutation within modulus)."""
    return rng.permuted(np.tile(d, (S, 1)), axis=1)

def build_moduli(mode):
    if mode == 'smoke':
        return [m for m in range(3, 121) if all(e == 1 for e in factor(m).values())]
    sf = [m for m in range(3, 301) if all(e == 1 for e in factor(m).values())]
    pr = [int(p) for p in simple_sieve(1000) if 307 <= p <= 997]
    return sf + pr

N_SHUFFLE = 2000

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'full'
    X = (1 << 22) if mode == 'smoke' else (1 << 26)
    moduli = build_moduli(mode)

    tp = time.time()
    P = segmented_primes(X)
    pi_x, liXv = int(P.size), li_x(X)
    sieve_s = time.time() - tp
    print(f'[{mode}] x=2^{int(math.log2(X))} pi={pi_x} li={liXv:.1f} sieve={sieve_s:.1f}s', flush=True)

    # ---- smoke-time verification of the orthogonality identity + L spot checks ----
    if mode == 'smoke':
        Lv3, _ = L1(-3, real_chars(3)[0][1])
        assert abs(Lv3 - math.pi / (3 * math.sqrt(3))) < 1e-9, Lv3
        D5, pat5 = real_chars(5)[0]
        assert D5 == 5
        lv5 = L1_trunc(pat5)
        true5 = 2 * math.log((1 + math.sqrt(5)) / 2) / math.sqrt(5)
        assert abs(lv5 - true5) < 1e-3, (lv5, true5)
        print(f'[smoke] L checks ok: L(1,chi_-3)={Lv3:.6f} exact; L(1,chi_5)={lv5:.6f} '
              f'trunc vs {true5:.6f}', flush=True)

    # ---- per-modulus pass: collect cells + class-level pieces ----
    cells = []          # dict rows: m, omega, D, how, w, c, agree
    class_cells = []    # dict rows: m, a(unit), pred, d, agree
    rng = np.random.default_rng(572)
    cs_null_sum = np.zeros(N_SHUFFLE)      # cell-level circular-sum null
    cl_null_agree = np.zeros(N_SHUFFLE)    # class-level agree-count null
    n_cells_by_m = {}
    n_signflip_smallprime = 0
    max_smallprime_corr = 0
    tp = time.time()

    for m in moduli:
        fs = factor(m)
        phim = phi_of(fs)
        red = np.nonzero(np.gcd(np.arange(m), m) == 1)[0]
        bc = np.bincount(P % m, minlength=m).astype(np.float64)
        for p in fs:
            bc[p % m] -= 1.0
        d = bc[red] - liXv / phim                      # deviation vector, unit classes
        ch = real_chars(m)
        CH = np.vstack([pat[red % len(pat)].astype(np.float64) for D, pat in ch])
        W = np.array([L1(D, pat)[0] for D, pat in ch], dtype=np.float64)
        HOW = [L1(D, pat)[1] for D, pat in ch]
        C = CH @ d                                     # == sum_{p<=x} chi(p)

        if mode == 'smoke':
            # exact identity check: c_chi = sum_{p<=x, p coprime to m} chi_D(p).
            # (Full primitive twist additionally carries +-1 contributions from the
            #  finitely many primes p|m, p∤cond(chi); tracked as smallprime_corr.)
            for j, (D, pat) in enumerate(ch):
                k = len(pat)
                direct = float(np.sum(pat[P % k]))
                corr = sum(int(pat[q % k]) for q in fs if q % k != 0)
                assert abs(C[j] - (direct - corr)) < 1e-9, (m, D, C[j], direct - corr)

        sw = np.sign(W)
        sc = np.sign(C)
        ag = (sw == sc).astype(int)
        for j, (D, pat) in enumerate(ch):
            k = len(pat)
            sp_corr = sum(int(pat[q % k]) for q in fs if q % k != 0)
            if sp_corr and np.sign(C[j]) != np.sign(C[j] + sp_corr):
                n_signflip_smallprime += 1
            max_smallprime_corr = max(max_smallprime_corr, abs(sp_corr))
            cells.append({'m': m, 'omega': len(fs), 'D': int(D), 'how': HOW[j],
                          'w': W[j], 'c': C[j], 'agree': int(ag[j])})

        # class-level predicted pattern
        pred = W @ CH                                  # sum_chi w_chi chi(a)
        sp = np.sign(pred)
        sd = np.sign(d)
        agcl = (sp == sd) & (np.abs(pred) > 1e-12)     # exclude measure-zero ties
        nz = int(agcl.sum())
        for i in np.nonzero(np.abs(pred) > 1e-12)[0]:
            class_cells.append({'m': m, 'a': int(red[i]), 'pred': float(pred[i]),
                                'd': float(d[i]), 'agree': int(sp[i] == sd[i])})

        # ---- shuffle null: permute d WITHIN modulus, recompute both statistics ----
        dshuf = within_modulus_shuffles(d, N_SHUFFLE, rng)     # (S, phi)
        Cs = dshuf @ CH.T                                      # (S, K)
        cs_null_sum += (np.sign(Cs) == sw).sum(axis=1)
        # class level: predictor sign(pred)=sign(W@CH) is FIXED under shuffling d;
        # the null varies sign(d) only (weaker exchangeability; disclosed in notes)
        keepm = np.abs(pred) > 1e-12
        cl_null_agree += ((np.sign(pred)[:, None] == np.sign(dshuf).T)[keepm]).sum(axis=0)
        n_cells_by_m[m] = {'phi': phim, 'K': len(ch), 'n_cells_class_kept': nz}

    loop_s = time.time() - tp
    print(f'[{mode}] {len(cells)} char cells, {len(class_cells)} class cells, '
          f'{len(moduli)} moduli in {loop_s:.1f}s', flush=True)

    # ---- cell-level statistics ----
    cw = np.array([c['w'] for c in cells]); ca = np.array([c['agree'] for c in cells])
    chow = np.array([c['how'] for c in cells]); comega = np.array([c['omega'] for c in cells])

    # cell-level: CS null accumulated as agree-counts over ALL cells per shuffle draw
    obs_CS = 2 * int(ca.sum()) - len(cells)   # sum sign(w)*sign(c) = agree - disagree
    cs_null = cs_null_sum
    cell_all = {
        'n_cells': len(cells), 'n_agree': int(ca.sum()),
        'rate': float(ca.mean()),
        'cp95': list(clopper_pearson(int(ca.sum()), len(cells))),
        'CS_obs_agree_minus_disagree': obs_CS,
        'CS_null_mean': float(cs_null.mean()), 'CS_null_sd': float(cs_null.std()),
        'CS_z': float((obs_CS - cs_null.mean()) / (cs_null.std() + 1e-300)),
    }
    cell_all['CI_excludes_50_above'] = bool(cell_all['cp95'][1] > 0.5 and cell_all['cp95'][0] > 0.5)
    cell_all['criterion_C1'] = cell_all['CI_excludes_50_above']
    cell_all['criterion_C2'] = bool(cell_all['CS_z'] > 3)

    sub_masks = {
        'omega1_prime_moduli': comega == 1,
        'omega_ge2_product_chars': comega >= 2,
        'L_exact_path': chow == 'exact',
        'L_truncated_path': chow == 'trunc',
        'drop_small_w_lt_1e-3': np.abs(cw) >= 1e-3,
    }
    breakdowns = {}
    for nm, msk in sub_masks.items():
        k = int(ca[msk].sum()); n = int(msk.sum())
        if n == 0:
            breakdowns[nm] = {'n_cells': 0}; continue
        lo, hi = clopper_pearson(k, n)
        breakdowns[nm] = {'n_cells': n, 'n_agree': k, 'rate': k / n, 'cp95': [lo, hi],
                          'ci_above_50': bool(lo > 0.5), 'ci_below_50': bool(hi < 0.5)}
        # subset z not registered; report rate + CP CI only (registered criteria are global)
    # two-sided global readout
    lo, hi = cell_all['cp95']
    cell_all['two_sided_ci_excludes_50'] = bool(hi < 0.5 or lo > 0.5)
    # DEGENERACY DIAGNOSTIC (added after smoke, BEFORE full data): L(1,chi)>0 for ALL
    # real non-principal chi (class-number formula), so sign(w)=+1 identically and the
    # cell-level agreement rate equals Pr[c_chi>0]. Report the realized skew directly.
    cell_all['n_cells_w_negative'] = int((cw < 0).sum())
    cell_all['frac_c_negative_chebyshev_skew'] = float(np.mean(
        [1.0 if c['c'] < 0 else 0.0 for c in cells]))
    cp_skew = clopper_pearson(int(sum(1 for c in cells if c['c'] < 0)), len(cells))
    cell_all['chebyshev_skew_cp95'] = list(cp_skew)

    # ---- class-level statistics ----
    pa = np.array([r['agree'] for r in class_cells])
    cls_all = {
        'n_classes': len(class_cells), 'n_agree': int(pa.sum()), 'rate': float(pa.mean()),
        'cp95': list(clopper_pearson(int(pa.sum()), len(class_cells))),
    }
    cls_all['CI_excludes_50_above'] = bool(cls_all['cp95'][0] > 0.5)
    cls_all['criterion_C1_class'] = cls_all['CI_excludes_50_above']
    cls_all['CS_class_obs'] = int((pa * 2 - 1).sum())
    # z computed on a SINGLE scale: agree-counts (null is agree-counts)
    cls_all['agree_z'] = float((int(pa.sum()) - cl_null_agree.mean()) /
                               (cl_null_agree.std() + 1e-300))
    cls_all['CS_class_null_mean'] = float(2 * cl_null_agree.mean() - len(class_cells))
    cls_all['CS_class_null_sd'] = float(2 * cl_null_agree.std())
    cls_all['CS_class_z'] = cls_all['agree_z']
    cls_all['criterion_C2_class'] = bool(cls_all['CS_class_z'] > 3)
    cls_all['two_sided_note'] = ('class predictor sign(pred)=sign(sum w_chi chi(a)) is '
                                 'shuffle-invariant; null varies only sign(d)')

    # ---- verdicts (pre-registered logic) ----
    crit = {
        'cell_C1_CI_gt50': cell_all['criterion_C1'],
        'cell_C2_z_gt3': cell_all['criterion_C2'],
        'class_C1_CI_gt50': cls_all['criterion_C1_class'],
        'class_C2_z_gt3': cls_all['criterion_C2_class'],
    }
    verdict = 'H1' if any(crit.values()) else 'H0'
    which = [k for k, v in crit.items() if v]

    notes = [
        f'final x=2^{int(math.log2(X))}, pi(x)={pi_x}',
        f'orthogonality identity c_chi = sum_a d_a chi(a) = sum_{{p<=x, gcd(p,m)=1}} chi_D(p) '
        f'verified EXACTLY (<1e-9) on every smoke (m,chi) cell; uniform-li theory term vanishes '
        f'identically so the ONLY computable x-independent theory weight is signed L(1,chi)',
        f'small-prime finite-x artifact: c_chi omits +-1 contributions of primes p|m, p|/'
        f'cond(chi); max |corr|={max_smallprime_corr}, cells whose sign would flip under the '
        f'full primitive twist: {n_signflip_smallprime} (disclosed, not corrected - the '
        f'measured AP projection is the registered observation)',
        'arg(L) degenerate for real chars (in {0,pi}) => single registered weight w=L(1,chi)',
        'non-unit residue classes excluded everywhere (contain <=1 prime: single-prime artifact)',
        'within-modulus d-shuffle MEANINGFUL here unlike exp566 (sign(c) not permutation-'
        'invariant in a); 2000 draws, common RNG seed 572',
        'no theorem ties sign(sum chi(p)) to sign(L(1,chi)); Mertens/Euler-product link is '
        'the motivation; registered one-sided per program statement, two-sided also reported',
        'POST-SMOKE DISCLOSURE (before any full data): L(1,chi)>0 for every real '
        'non-principal chi (class-number formula) => sign(w)=+1 identically; the cell-level '
        'agreement rate is EXACTLY Pr[c_chi>0], so criterion C1 as registered can only fire '
        'if prime twists are majority-POSITIVE. The informative content of the cell readout '
        'is the realized skew (Chebyshev-bias direction), reported explicitly; class-level '
        'criterion remains non-degenerate (L-values enter as WEIGHTS)',
        'truncation-sign guard: exp566-calibrated median rel err 1.8e-5; robustness row '
        'drops |w|<1e-3 cells',
        'class-level predictor is shuffle-invariant, so its null varies sign(d) only '
        '(weaker exchangeability than cell-level null)',
    ]
    if verdict == 'H0':
        consequence = ('MA-1 computable-effectivity program CLOSED on BOTH routes '
                       '(magnitude: exp566 R2=0.019; signed: chance-level alignment here) '
                       '=> honest negative strengthening paper 213')
    else:
        consequence = ('first computable handle on AP-deviation STRUCTURE: signed '
                       'character components align with deviation patterns => MA-1 '
                       'effectivity partially armed along the signed route')

    result = {
        'exp': '572',
        'codename': 'MA1-SIGNED',
        'round': 74,
        'smoke': mode == 'smoke',
        'status': '06_final' if mode != 'smoke' else '03_smoke',
        'hypotheses': {
            'H1_prestated': ('sign pattern s(m,a)=sign(pi-li/phi) correlates above chance '
                             'with L(1,chi)-predicted signs: (C1) pooled cell agreement CP95 '
                             'CI wholly >0.5, OR (C2) circular-sum z>3 vs within-modulus '
                             'shuffle null (2000); class-level analogue reported'),
            'H0_prestated': 'agreement <= chance on both criteria => signed route dead too; '
                            'MA-1 computable-effectivity program closed both routes',
        },
        'config': {
            'exp': 'exp572', 'name': 'MA1-SIGNED', 'mode': mode,
            'x': X, 'pi_x': pi_x, 'li_x': liXv,
            'moduli_source': ('squarefree[3,120]' if mode == 'smoke'
                              else 'squarefree[3,300] + primes[307,997]'),
            'n_moduli': len(moduli), 'sieve_s': round(sieve_s, 2),
            'loop_s': round(loop_s, 2), 'n_shuffle': N_SHUFFLE, 'seed': 572,
            'theory_weight': 'w = signed L(1,chi) (exp566 exact/trunc paths)',
        },
        'stats': {
            'cell_level_primary': cell_all,
            'cell_breakdowns': breakdowns,
            'class_level': cls_all,
        },
        'verdicts': {
            'primary': verdict,
            'criteria_met': which,
            'thresholds': {'C1_cp95_wholly_gt_0.5': True, 'C2_z_gt': 3},
            'headline': (f'cell agreement {cell_all["rate"]:.4f} over {cell_all["n_cells"]} '
                         f'cells, CP95 [{lo:.4f},{hi:.4f}], CS_z={cell_all["CS_z"]:.2f}; '
                         f'class agreement {cls_all["rate"]:.4f}/{cls_all["n_classes"]}, '
                         f'CS_z={cls_all["CS_class_z"]:.2f} => {verdict}'),
            'consequence': consequence,
        },
        'honest_notes': notes,
        'wall_s': round(time.time() - T0, 2),
    }
    # per-modulus compact rows (aggregate per modulus)
    rows = []
    for m in moduli:
        info = n_cells_by_m[m]
        mc = [c for c in cells if c['m'] == m]
        rows.append({'m': m, 'phi': info['phi'], 'K': info['K'],
                     'n_agree': int(sum(c['agree'] for c in mc)),
                     'n_cells': len(mc)})
    result['rows'] = rows

    out = 'exp572_smoke_result.json' if mode == 'smoke' else 'exp572_result.json'
    with open(out, 'w') as f:
        json.dump(result, f, indent=1)
    print(json.dumps(result['verdicts'], indent=1), flush=True)
    print(json.dumps(result['stats']['cell_level_primary'], indent=1), flush=True)
    print('wrote', out, f'wall={result["wall_s"]}s', flush=True)

if __name__ == '__main__':
    main()

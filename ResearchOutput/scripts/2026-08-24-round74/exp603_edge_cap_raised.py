#!/usr/bin/env python3
"""
exp603 EDGE-CAP-RAISED (round-74) -- completes paper 245's loose end.

BACKGROUND: exp594 fitted the two-component position-density model
    T(x) = A*(1+x)^(-b_bulk) + K*(1+x)^(-b_edge)
to the pooled normalized hit-position histogram (exp581_regen_positions.npz)
with b_edge confined to [0, CAP].  At CAP=80: point 40.46, CI [15.2, 80.0],
CI upper edge AT THE CAP in 26.7% of refits -- steepness may be capped by the
imposed box, not by the data.

PRE-REGISTRATION (written BEFORE any fitting; nothing downstream may change it):
  H1 (identifiable):  at CAP >= 120 the bootstrap CI upper edge of b_edge stays
      strictly BELOW its cap (interior optimum stable) => b_edge +/- CI is
      reported AS IDENTIFIED.
  H0 (unidentified):  the CI upper edge keeps hitting successive caps =>
      steepness formally UNIDENTIFIABLE at this data size; the lower-bound
      ladder {CAP -> CI lower edge} is recorded as FINAL.
  CONTROL BAR (preregistered): fits on ctl_* positions are KERNEL-FREE iff,
      at every cap, point edge weight w_edge(x=0.9) < 0.10 AND the
      1-comp -> 2-comp relative SSE improvement is < 5%.

METHOD: per-seed normalization x=(v-jlo[i])/(jhi[i]-jlo[i]), clipped to [0,1]
(clips counted); pooled histogram nb=50 over [0,1] (exp581/582 anchor grid);
unweighted NLS on bin densities; (A,K) profiled out linearly (nonneg
2-column LS) over a dense (b_bulk, b_edge) log grid incl. near-cap points,
then multi-start bounded TRF refinement of the POINT fit; cluster bootstrap
over the 128 seeds (resample seeds with replacement, pool, regrid, reprofile);
cap-hit := b_edge_hat >= 0.999*CAP; CI = percentile [2.5, 97.5].
Smoke: --smoke (single cap 40, coarse, <30 s).  Full target <= 8 min.
Touch ONLY exp603_* files.  No commits.  Seed 20260824.
"""
import sys, os, json, time
import numpy as np
from scipy.optimize import least_squares

BASE = os.path.dirname(os.path.abspath(__file__))
NPZ = os.path.join(BASE, 'exp581_regen_positions.npz')
SMOKE = '--smoke' in sys.argv
SEED = 20260824
NB = 50
if SMOKE:
    CAPS = [40]; NBOOT = 50; NBOOT_CTL = 20; G_BULK, G_EDGE = 10, 16
else:
    CAPS = [80, 120, 240]; NBOOT = 1000; NBOOT_CTL = 300; G_BULK, G_EDGE = 20, 52


def load():
    d = np.load(NPZ)
    seeds = sorted(int(k.split('_')[1]) for k in d.files if k.startswith('hit_'))
    xs, xc, nh, nc = [], [], 0, 0
    for i in seeds:
        lo, hi = float(d['jlo'][i]), float(d['jhi'][i])
        h = (d['hit_%d' % i].astype(float) - lo) / (hi - lo)
        nh += int(((h < 0) | (h > 1)).sum()); xs.append(np.clip(h, 0.0, 1.0))
        c = (d['ctl_%d' % i].astype(float) - lo) / (hi - lo)
        nc += int(((c < 0) | (c > 1)).sum()); xc.append(np.clip(c, 0.0, 1.0))
    return seeds, xs, xc, nh, nc


def pooled_hist(xs_list):
    allx = np.concatenate(xs_list)
    cnt, edges = np.histogram(allx, bins=np.linspace(0.0, 1.0, NB + 1))
    x = 0.5 * (edges[:-1] + edges[1:])
    y = cnt.astype(float) / (cnt.sum() * (edges[1] - edges[0]))
    return x, y, cnt.astype(float), int(allx.size)


def per_seed_hist_matrix(xs_list):
    """(S, NB) count matrix, one row per seed."""
    H = np.zeros((len(xs_list), NB))
    for r, v in enumerate(xs_list):
        H[r], _ = np.histogram(v, bins=np.linspace(0.0, 1.0, NB + 1))
    return H


def make_grids(cap, g_bulk, g_edge):
    eb = np.geomspace(0.25, 24.0, g_bulk)
    ee = np.unique(np.concatenate([np.geomspace(0.25, cap, g_edge),
                                   [0.90 * cap, 0.95 * cap, 0.98 * cap, 0.999 * cap]]))
    return eb, ee


def profile_grid(x, yall, cap, g_bulk, g_edge):
    """Vectorized bounded 2-comp profile over the exponent grid.
    yall: (B, NB).  Returns (sse_min, bb_hat, be_hat[nan if pure-bulk wins])."""
    eb, ee = make_grids(cap, g_bulk, g_edge)
    base = (1.0 + x)[:, None]
    colb = base ** (-eb[None, :])          # (NB, Gb)
    cole = base ** (-ee[None, :])          # (NB, Ge)
    B = yall.shape[0]
    yy2 = (yall * yall).sum(1)
    cb = yall @ colb                        # (B, Gb)
    ce = yall @ cole                        # (B, Ge)
    gbd = (colb * colb).sum(0)
    ged = (cole * cole).sum(0)
    best_sse = np.full(B, np.inf)
    best_bb = np.zeros(B)
    best_ee = np.full(B, np.nan)
    lskip = 0.02
    for i1 in range(len(eb)):
        m1 = colb[:, i1]; c1 = cb[:, i1]; g11 = gbd[i1]
        sse_bulk = yy2 - c1 * c1 / g11      # pure-bulk candidate (A>=0 auto)
        upd = sse_bulk < best_sse
        best_sse = np.where(upd, sse_bulk, best_sse)
        best_bb = np.where(upd, eb[i1], best_bb)
        best_ee = np.where(upd, np.nan, best_ee)
        for j1 in range(len(ee)):
            if abs(np.log(ee[j1] / eb[i1])) < lskip:
                continue                    # collinear columns
            m2 = cole[:, j1]
            g12 = float(m1 @ m2); g22 = ged[j1]; c2 = ce[:, j1]
            det = g11 * g22 - g12 * g12
            if det <= 1e-12 * max(g11 * g22, 1e-300):
                continue
            a = (c1 * g22 - c2 * g12) / det
            k = (c2 * g11 - c1 * g12) / det
            sse2 = yy2 - 2.0 * (a * c1 + k * c2) + a * a * g11 + 2.0 * a * k * g12 + k * k * g22
            sse_cand = np.where((a >= 0) & (k >= 0), sse2, sse_bulk)
            upd = sse_cand < best_sse
            best_sse = np.where(upd, sse_cand, best_sse)
            best_bb = np.where(upd, eb[i1], best_bb)
            best_ee = np.where(upd, np.where((a >= 0) & (k >= 0), ee[j1], np.nan), best_ee)
    return best_sse, best_bb, best_ee


def _lin_profile(x, y, bb, be):
    m1 = (1.0 + x) ** (-bb); m2 = (1.0 + x) ** (-be)
    M = np.column_stack([m1, m2])
    try:
        sol = np.linalg.lstsq(M, y, rcond=None)[0]
        r = M @ sol - y
        return float(r @ r), sol
    except np.linalg.LinAlgError:
        return float('inf'), np.array([float(np.max(y)), 1e-9])


def fit_point(x, y, cap, g_bulk, g_edge):
    """Multi-start NLS point fit; returns dict."""
    sse_g, bb_g, be_g = profile_grid(x, y[None, :], cap, g_bulk, g_edge)
    mask = np.isfinite(be_g)
    if mask.any():
        j = int(np.argmin(np.where(mask, sse_g, np.inf)))
        b0, e0 = float(bb_g[j]), float(be_g[j])
        _, sol0 = _lin_profile(x, y, b0, e0)
    else:
        # no viable 2-comp grid cell (control-like: pure bulk wins everywhere)
        b0 = float(bb_g[int(np.argmin(sse_g))]); e0 = max(1.0, 0.5 * cap)
        sol0 = np.array([float(np.max(y)), 1e-9])
    starts = [(b0, e0, max(sol0[0], 1e-9), max(sol0[1], 1e-9)),
              (2.0, min(cap, 20.0), float(np.max(y)) * 0.8, float(np.max(y)) * 0.2),
              (0.7, min(cap, 8.0), float(np.max(y)), 1e-6),
              (5.0, min(cap, 60.0), float(np.max(y)) * 0.9, 1e-6)]
    lo = [0.05, 0.05, 0.0, 0.0]
    hi = [60.0, float(cap), 1e3, 1e3]
    best = None
    for p0 in starts:
        p0 = np.array(p0, float)
        p0 = np.minimum(np.maximum(p0, np.array(lo) + 1e-9), np.array(hi) - 1e-9)
        try:
            res = least_squares(lambda p: p[2] * (1.0 + x) ** (-p[0]) +
                                p[3] * (1.0 + x) ** (-p[1]) - y,
                                p0, bounds=(lo, hi), x_scale='jac', max_nfev=400)
        except Exception:
            continue
        sse = float(res.fun @ res.fun)
        if best is None or sse < best['sse']:
            bb, be, A, K = res.x
            T09 = A * 1.9 ** (-bb) + K * 1.9 ** (-be)
            mb = (1.0 + x) ** (-bb)
            sse1 = float(np.sum((mb * float(y @ mb / (mb @ mb)) - y) ** 2))
            best = dict(b_bulk=float(bb), b_edge=float(be), A=float(A), K=float(K),
                        sse=sse, sse_1comp=sse1,
                        w_edge_x09=float(K * 1.9 ** (-be) / T09) if T09 > 0 else 0.0,
                        rel_sse_improvement=float((sse1 - sse) / sse1) if sse1 > 0 else 0.0,
                        at_cap=bool(be >= 0.999 * cap))
    return best


def boot_yall(H, rng, nboot):
    idx = rng.integers(0, H.shape[0], size=(nboot, H.shape[0]))
    cnt = H[idx].sum(axis=1)                      # (nboot, NB)
    tot = cnt.sum(axis=1, keepdims=True)
    tot[tot == 0] = 1.0
    return cnt / (tot * (1.0 / NB))


def run_arm(name, xs_list, caps, nboot, g_bulk, g_edge, rng):
    x, y, cnt, npts = pooled_hist(xs_list)
    H = per_seed_hist_matrix(xs_list)
    out = {'n_points': npts, 'n_seeds': H.shape[0], 'caps': {}}
    for cap in caps:
        pt = fit_point(x, y, cap, g_bulk, g_edge)
        yall = boot_yall(H, rng, nboot)
        sse_b, bb_b, be_b = profile_grid(x, yall, cap, g_bulk, g_edge)
        fin = be_b[np.isfinite(be_b)]
        ci = (float(np.percentile(fin, 2.5)), float(np.percentile(fin, 97.5))) if fin.size else (float('nan'),) * 2
        out['caps'][str(cap)] = dict(
            point=pt, nboot=nboot,
            n_valid_2comp=int(fin.size),
            frac_purebulk=float(1.0 - fin.size / nboot),
            be_median=float(np.median(fin)) if fin.size else float('nan'),
            be_mean=float(np.mean(fin)) if fin.size else float('nan'),
            ci_lo=ci[0], ci_hi=ci[1],
            cap_hit_frac=float(np.mean(be_b >= 0.999 * cap)),
            bb_boot_median=float(np.median(bb_b)))
    return out


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    seeds, xs, xc, nclip_h, nclip_c = load()
    print('exp603 EDGE-CAP-RAISED smoke=%s caps=%s nboot=%d/%d seed=%d' %
          (SMOKE, CAPS, NBOOT, NBOOT_CTL, SEED))
    print('seeds=%d clip_hits=%d clip_ctl=%d' % (len(seeds), nclip_h, nclip_c))

    hits = run_arm('hits', xs, CAPS, NBOOT, G_BULK, G_EDGE, rng)
    ctl_rng = np.random.default_rng(SEED + 1)
    ctl = run_arm('control', xc, CAPS, NBOOT_CTL, G_BULK, G_EDGE, ctl_rng)

    # control kernel-free bar (preregistered)
    ckf = all(c['point']['w_edge_x09'] < 0.10 and c['point']['rel_sse_improvement'] < 0.05
              for c in ctl['caps'].values())

    # verdicts (preregistered)
    ident = {str(cap): (hits['caps'][str(cap)]['ci_hi'] < cap) for cap in CAPS}
    hi_caps = [c for c in CAPS if c >= 120]
    if hi_caps and all(ident[str(c)] for c in hi_caps):
        verdict = 'H1-IDENTIFIED'
    else:
        verdict = 'H0-UNIDENTIFIED_LADDER_FINAL'

    # sqrt(count+1)-weighted sensitivity at the largest cap (point level only)
    x, y, cnt, _ = pooled_hist(xs)
    sens_cap = max(CAPS)
    sens = fit_point(x, y * np.sqrt(cnt + 1.0), sens_cap, G_BULK, G_EDGE)

    ladder = [dict(source='exp594', cap=80, b_edge_point=40.46, ci_lo=15.2, ci_hi=80.0,
                   cap_hit_frac=0.267, note='historical anchor, prior run')]
    for cap in CAPS:
        h = hits['caps'][str(cap)]
        ladder.append(dict(source='exp603', cap=int(cap),
                           b_edge_point=h['point']['b_edge'],
                           b_bulk_point=h['point']['b_bulk'],
                           ci_lo=h['ci_lo'], ci_hi=h['ci_hi'],
                           cap_hit_frac=h['cap_hit_frac'],
                           frac_purebulk=h['frac_purebulk'],
                           identified=bool(ident[str(cap)])))

    wall = time.time() - t0
    result = dict(
        experiment='exp603_EDGE_CAP_RAISED',
        config=dict(smoke=SMOKE, caps=CAPS, nboot=NBOOT, nboot_control=NBOOT_CTL,
                    nbins=NB, seed=SEED, grid=(G_BULK, G_EDGE),
                    model='T(x)=A(1+x)^-b_bulk + K(1+x)^-b_edge',
                    normalization='x=(v-jlo)/(jhi-jlo) per seed, clip [0,1]',
                    bootstrap='cluster over 128 seeds, percentile CI',
                    cap_hit_def='b_edge_hat >= 0.999*cap'),
        data_summary=dict(n_seeds=len(seeds), n_hit_points=hits['n_points'],
                          n_ctl_points=ctl['n_points'],
                          clipped_hits=nclip_h, clipped_ctl=nclip_c),
        fits={k: v['point'] for k, v in hits['caps'].items()},
        bootstrap={k: {kk: vv for kk, vv in v.items() if kk != 'point'}
                   for k, v in hits['caps'].items()},
        control={k: dict(point=v['point'], frac_purebulk=v['frac_purebulk'])
                 for k, v in ctl['caps'].items()},
        control_kernel_free=bool(ckf),
        sensitivity_sqrtcount=dict(cap=sens_cap, b_edge=sens['b_edge'],
                                   b_bulk=sens['b_bulk'], K=sens['K'],
                                   w_edge_x09=sens['w_edge_x09']),
        ladder=ladder,
        stats=dict(verdict=verdict, per_cap_identified=ident),
        verdicts=dict(primary=verdict, per_cap_identified=ident,
                      control_kernel_free=bool(ckf)),
        honest_notes=[
            'Preregistration (H1/H0 + control bar) written in header BEFORE fitting; unchanged.',
            'Pipeline is self-consistent across caps but not bit-identical to exp594 '
            '(binning nb=50 shared with exp581/582 anchor; exp594 internals unread); '
            'the H1/H0 test is the within-run cap-to-cap comparison.',
            'Bootstrap CIs come from the dense-grid profiled fit (discretized NLS, '
            'no per-boot continuous refine); point estimates are multi-start refined. '
            'Near-cap grid points make cap-hits detectable.',
            'Unweighted density NLS is the preregistered primary; sqrt(count+1) '
            'weighting reported as point-level sensitivity only.',
            'Boots whose best fit is pure bulk (K=0) have undefined b_edge: excluded '
            'from CI, reported as frac_purebulk, never counted as cap-hits.',
            'exp594 cap-80 row quoted as historical anchor for comparability.'],
        wall_s=round(wall, 2))

    if SMOKE:
        print(json.dumps(result['fits'], indent=1))
        print('smoke wall_s=%.2f  OK' % wall)
    else:
        with open(os.path.join(BASE, 'exp603_result.json'), 'w') as f:
            json.dump(result, f, indent=1)

    # ---- findings.md (only in full mode) ----
    L = []
    L.append('# exp603 EDGE-CAP-RAISED (round-74) -- findings')
    L.append('')
    L.append('Question raised by paper 245/exp594: is b_edge interior-optimal, or')
    L.append('just boxed by the cap? Raised caps {80,120,240}, nboot %d cluster' % NBOOT)
    L.append('(over 128 seeds), nb=50 pooled histogram, preregistered H1/H0.')
    L.append('')
    L.append('| cap | b_edge point | 95% CI | cap-hit | pure-bulk | identified |')
    L.append('|-----|--------------|--------|---------|-----------|------------|')
    for e in ladder:
        if e['source'] != 'exp603':
            continue
        L.append('| %d | %.2f | [%.2f, %.2f] | %.1f%% | %.1f%% | %s |' %
                 (e['cap'], e['b_edge_point'], e['ci_lo'], e['ci_hi'],
                  100 * e['cap_hit_frac'], 100 * e['frac_purebulk'],
                  'yes' if e['identified'] else 'NO (hits cap)'))
    L.append('')
    L.append('VERDICT: **%s**' % verdict)
    if verdict == 'H1-IDENTIFIED':
        L.append('At cap >= 120 the CI upper edge detached from the cap: b_edge is')
        L.append('interior-optimal and REPORTED AS IDENTIFIED at this data size.')
    else:
        L.append('CI upper edge keeps pinning to successive caps: steepness formally')
        L.append('unidentifiable here; lower-bound ladder (%s) is FINAL.' %
                 ', '.join('cap %d -> LB %.1f' % (e['cap'], e['ci_lo'])
                           for e in ladder if e['source'] == 'exp603'))
    L.append('Control arm kernel-free: %s (bar w_edge(0.9)<0.10, relSSE<5%%).' % ckf)
    L.append('Sensitivity sqrt(count+1) wgt @ cap %d: b_edge %.2f.' %
             (sens_cap, sens['b_edge']))
    L.append('')
    L.append('Wall %.1fs; seed %d; no commits; only exp603_* touched.' % (wall, SEED))
    if not SMOKE:
        with open(os.path.join(BASE, 'exp603_findings.md'), 'w') as f:
            f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()

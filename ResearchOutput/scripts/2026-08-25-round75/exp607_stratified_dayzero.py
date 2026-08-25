#!/usr/bin/env python3
"""EXP607 STRATIFIED-DAYZERO -- PRE-REGISTERED SCREENING ANALYSIS
(Bet #1 day-zero, Berggren fleet brief; written BEFORE any cell-level number)

STATUS: EXPLORATORY SCREENING on already-recorded data. NO evidentiary claim
either way; output = funding decision + effect-size estimates for the fleet's
main-run design. Any positive here requires the pre-registered fresh-seed
main run before it counts as evidence.

QUESTION: paper-252/exp602's POOLED adjudication (z_cal = 0.65, density-only)
does not exclude cell-wise rate deviations that CANCEL across N-computable
strata. Test: do per-cell standardized excesses of the density-only model show
heterogeneity + sign-alternation beyond what magnitude-conditioned chance
allows?

POPULATIONS (all four independent, fresh-seed, exact Ns in *_ns.txt sidecars;
balanced-distinct-prime semiprimes BY VERBATIM-RECIPE CONSTRUCTION -- recipes
audited twice this session; square-N guarantee inherited from make_semiprime,
NOT from post-hoc factoring):
  A: exp598c_verify.npz  (bits=96,  seed 20260907, n=512, 50k samples/N)
  B: exp606_b96_verify.npz (bits=96, seed 20261007, n=512, 50k)
  C: exp606_b72_verify.npz (bits=72, seed 20261008, n=512, 50k)
  D: exp606_b128_verify.npz (bits=128, seed 20261009, n=512, 150k)

ANALYSIS (registered):
  1. y := log((hits+0.5)/n_hit) per N (as recorded). Density-only model:
     OLS y ~ 1 + S_dial. Residuals e_i. (No kappa in the base model --
     the screen asks whether ANY N-computable cell carries uncaptured
     deviation; kappa-cells are among the tested axes.)
  2. Covariate axes (N-computable, computed HERE from ns.txt Ns -- not
     trusted from any prior artifact except S_dial which is verified below):
       M: ln(N) deciles (10 bins)
       F: frac(sqrt(N)) quintiles (5 bins, gmpy2.isqrt)
       K: kappa = sum_k P(l_k|v) from D16 marginals (terciles; formula =
          repaired exp606 secondary-arm definition)
       S: S_dial terciles (given; cross-checked against count_matrix
          reconstruction on 32 random Ns per population)
  3. Cell grids examined (each analyzed separately, multiplicity handled by
     the calibrated-null requirement + replication rule, NOT by correction):
       G1: M x K (10 x 3 = 30 cells)   <- primary grid
       G2: M x F (10 x 5 = 50 cells)
       G3: S x K (3 x 3 = 9 cells)
  4. Per-cell excess e_c = mean residual; z_c = e_c / SE(e_c).
     Heterogeneity Q = sum_c n_c * e_c^2 (excess-dispersion statistic).
  5. CALIBRATION (METHOD-LAW compliant): row-shuffles are WRONG for
     deterministic functions of N. Null = residuals reshuffled ONLY WITHIN
     fine magnitude-matched strata (M-decile x F-quintile = 50 strata),
     5000 reps per population, rng seed 7000+A. Preserves any pure-magnitude
     structure; breaks covariate-residual coupling beyond it. Report p_Q and
     max|z_c| null quantiles per grid.
  6. PRE-STATED SCREEN DECISION (per population):
       CELL-ALERT(c) := |z_c| >= 2.
       POPULATION-POSITIVE(grid) := p_Q < 0.01 AND >=3 CELL-ALERTs including
       at least one z>0 and one z<0.
       SCREEN-POSITIVE := POPULATION-POSITIVE on the SAME grid family in >=2
       of the 4 independent populations, with sign-alternation (both signs
       present among alerts) in each.
       SCREEN-NEGATIVE := no population positive on any grid -> pooled null
       upgraded to stratified-strength null at this resolution; main run NOT
       funded on this basis.
       else MIXED -> report per-population detail, fund only with a
       mechanism story naming the cancelling pair.
  7. CANCELLATION READOUT (the direct question): pooled z = mean(e)/SE(mean)
     vs the largest |z_c| per grid -- if pooled |z| < 2 while cell alerts
     fire, cancellation is demonstrated at this data's resolution.

POST-RUN ERRATA (adjudicator; recorded in paper 258, code unchanged):
  (a) G2_MxF p-values DEGENERATE BY CONSTRUCTION -- grid axes == null strata
      => Q bitwise permutation-invariant => p is 1.0 or the floor only.
      Recorded G2 p=0.0002 entries are fp-tie noise. G2 p column VOID.
  (b) pooled_z is identically ~0 by intercept-orthogonality: header item 7's
      cancellation readout as written is vacuous; cancellation evidence rests
      on phase1-alerts -> phase2-collapse.
  (c) Permutation streams collide across populations via seed//1000
      (B/C/D share bases); harmless on independent data, hygiene note.
  (d) Literal unamended registration fires SCREEN_POSITIVE on phase 1;
      recorded SCREEN_NEGATIVE exists under the disclosed amendment.

Honest limits (disclosed up front): single snapshot per N (no fresh-stream
replication within this screen -- replication comes from the 4 independent
populations); bits=96 appears twice (different seeds) while 72/128 once;
screen power at 512/population modest -- a NEGATIVE here is weaker than the
main run's would be, and says nothing at u-regimes outside these windows.
"""
import json
import time
import numpy as np
import gmpy2
from gmpy2 import mpz, isqrt, jacobi

IN_DIR = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-24-round74"
OUT_DIR = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-25-round75"
POPS = {
    "A_598c_b96": ("exp598c_verify.npz", "exp598c_ns.txt", 20260907),
    "B_606_b96": ("exp606_b96_verify.npz", "exp606_b96_ns.txt", 20261007),
    "C_606_b72": ("exp606_b72_verify.npz", "exp606_b72_ns.txt", 20261008),
    "D_606_b128": ("exp606_b128_verify.npz", "exp606_b128_ns.txt", 20261009),
}
PERM_REPS = 5000
BASE_SEED = 7000
PRIME_LO, PRIME_HI, ALPHA = 3, 400, 0.5


def odd_primes(lo, hi):
    sieve = np.ones(hi + 1, dtype=bool); sieve[:2] = False
    for k in range(2, int(hi ** 0.5) + 1):
        if sieve[k]:
            sieve[k * k::k] = False
    return [int(p) for p in np.nonzero(sieve)[0] if p >= lo]


def kappa_from_D(D16):
    marg = np.zeros((D16.shape[0], 4))
    for k in range(4):
        mask = np.array([(c >> k) & 1 for c in range(16)], dtype=bool)
        marg[:, k] = D16[:, mask].sum(axis=1)
    return marg.sum(axis=1)


def bins(x, nbins):
    q = np.quantile(x, np.linspace(0, 1, nbins + 1))
    q[-1] += 1e-9
    return np.digitize(x, q[1:-1])


def ols_fit(X, y):
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    return X @ beta


def analyse_pop(tag, npz_f, ns_f, seed):
    d = np.load(f"{IN_DIR}/{npz_f}")
    Ns = [int(l) for l in open(f"{IN_DIR}/{ns_f}")]
    n = len(Ns)
    assert n == d["y"].shape[0]
    y = d["y"]; S = d["S_dial"]; D16 = d["D16"]
    # S_dial spot-verification against mechanistic recomputation (32 Ns)
    primes = odd_primes(PRIME_LO, PRIME_HI)
    w = np.array([p ** (-ALPHA) for p in primes])
    rng_v = np.random.default_rng(seed + 999)
    idx_v = rng_v.choice(n, 32, replace=False)
    for i in idx_v:
        m = mpz(Ns[i])
        s_re = sum(w[j] for j, p in enumerate(primes) if jacobi(m % p, p) == 1)
        assert abs(s_re - S[i]) < 1e-9, f"dial mismatch {tag}[{i}]"
    kap = kappa_from_D(D16)
    lnn = np.log(np.array([float(m) for m in Ns]))
    fr = np.array([float(mpz(Ns[i]) - isqrt(mpz(Ns[i])) ** 2) /
                   float(2 * isqrt(mpz(Ns[i])) + 1) for i in range(n)])
    Mb, Fb, Kb, Sb = bins(lnn, 10), bins(fr, 5), bins(kap, 3), bins(S, 3)

    # PHASE 1 (registered): dial-only residuals
    e1 = y - ols_fit(np.hstack([np.ones((n, 1)), S[:, None]]), y)
    # PHASE 2 AMENDMENT (disclosed as exploratory-amended: phase-1 was seen
    # first and its alerts sat on the K axis == paper 257's recorded graded
    # law; phase 2 asks whether ANYTHING survives once kappa is absorbed --
    # the actual funding question). Same grids, same calibration machinery.
    e2 = y - ols_fit(np.hstack([np.ones((n, 1)), S[:, None],
                                kap.reshape(-1, 1)]), y)

    grids = {"G1_MxK": (Mb, Kb), "G2_MxF": (Mb, Fb), "G3_SxK": (Sb, Kb)}
    strata = Mb.astype(int) * 5 + Fb.astype(int)   # magnitude-matched strata

    def run_phase(e_vec, label):
        sig_v = float(e_vec.std(ddof=1))
        out_p = {"sigma_resid": round(sig_v, 6),
                 "pooled_z": round(float(e_vec.mean() / (sig_v / np.sqrt(n))), 4),
                 "grids": {}}
        for gname, (gA, gB) in grids.items():
            cells = {}
            for a in np.unique(gA):
                for b in np.unique(gB):
                    m = (gA == a) & (gB == b)
                    if m.sum() < 8:
                        continue
                    ec = float(e_vec[m].mean())
                    cells[(int(a), int(b))] = (int(m.sum()), ec,
                                               ec / (sig_v / np.sqrt(m.sum())))
            Q = sum(nn * ec * ec for nn, ec, _ in cells.values())
            prng = np.random.default_rng(
                BASE_SEED + seed // 1000 + (1 if label == "phase2" else 0))
            Q_null = np.empty(PERM_REPS)
            e_perm = e_vec.copy()
            for r in range(PERM_REPS):
                for st in np.unique(strata):
                    ms = strata == st
                    e_perm[ms] = prng.permutation(e_vec[ms])
                Qr = 0.0
                for (a, b), (nn, _, _) in cells.items():
                    m = (gA == a) & (gB == b)
                    Qr += nn * float(e_perm[m].mean()) ** 2
                Q_null[r] = Qr
            pQ = float((1 + np.sum(Q_null >= Q)) / (PERM_REPS + 1))
            alerts = {f"{a}_{b}": dict(n=nn, e=round(ec, 5), z=round(zc, 3))
                      for (a, b), (nn, ec, zc) in cells.items() if abs(zc) >= 2}
            out_p["grids"][gname] = {
                "Q": round(Q, 5), "p_Q": pQ,
                "null_q95": round(float(np.quantile(Q_null, .95)), 5),
                "max_abs_z": round(max(abs(z[2]) for z in cells.values()), 3),
                "n_cells": len(cells),
                "alerts": alerts,
                "population_positive": bool(
                    pQ < 0.01 and len(alerts) >= 3
                    and any(v["z"] > 0 for v in alerts.values())
                    and any(v["z"] < 0 for v in alerts.values())),
            }
        return out_p

    out = {"tag": tag, "n": n,
           "phase1_dial_only": run_phase(e1, "phase1"),
           "phase2_dial_plus_kappa": run_phase(e2, "phase2")}
    return out


def main():
    t0 = time.time()
    results = {}
    PH = "phase2_dial_plus_kappa"      # decision phase (amendment)
    for tag, (npz_f, ns_f, seed) in POPS.items():
        results[tag] = analyse_pop(tag, npz_f, ns_f, seed)
        r1 = results[tag]["phase1_dial_only"]; r2 = results[tag][PH]
        print(f"[{tag}] ph1: " + " ".join(
            f"{g}:p={r1['grids'][g]['p_Q']:.4f},alerts={len(r1['grids'][g]['alerts'])}"
            for g in r1['grids']) + f" | ph2(+kappa): " + " ".join(
            f"{g}:p={r2['grids'][g]['p_Q']:.4f},pos={r2['grids'][g]['population_positive']},"
            f"alerts={len(r2['grids'][g]['alerts'])}" for g in r2['grids']),
            flush=True)
    # screen decision (registered rule applied to PHASE 2 -- the funding
    # question; phase 1 is reported as the paper-257 cell-level replication)
    pos_G1 = [t for t, r in results.items()
              if r[PH]["grids"]["G1_MxK"]["population_positive"]]
    pos_any = [t for t, r in results.items()
               if any(g["population_positive"] for g in r[PH]["grids"].values())]
    alt = all(
        any(v["z"] > 0 for v in results[t][PH]["grids"]["G1_MxK"]["alerts"].values())
        and any(v["z"] < 0 for v in results[t][PH]["grids"]["G1_MxK"]["alerts"].values())
        for t in pos_G1)
    if len(pos_G1) >= 2 and alt:
        decision = "SCREEN_POSITIVE"
    elif not pos_any:
        decision = "SCREEN_NEGATIVE"
    else:
        decision = "SCREEN_MIXED"
    summary = {"decision": decision, "positive_G1_pops": pos_G1,
               "positive_any_grid": pos_any, "wall_s": round(time.time() - t0, 1)}
    json.dump({"summary": summary, "populations": results},
              open(f"{OUT_DIR}/exp607_result.json", "w"), indent=1)
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()

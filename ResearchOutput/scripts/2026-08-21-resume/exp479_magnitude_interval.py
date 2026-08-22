#!/usr/bin/env python3
"""
exp479 MAGNITUDE-INTERVAL (round-40, factor3 lab)
=================================================
COMPOSES paper 137 (descending-from-sqrtN magnitude ordering => ~5.19x trial
division speedup, sham-controlled) with paper 143 (external INTERVAL hint priced
by exactly two numbers: coverage alpha x relative width mu/M; committed scanning
Bayes-optimal; 5.19x corresponds to (alpha~0.9, mu/M~0.02-0.05)).

OPEN QUESTION: when we use N's magnitude information optimally (descending
order), what EFFECTIVE (alpha_eff, mu_eff/M) does that correspond to on paper
143's interval-hint parameter plane?

PRE-STATEMENT OF HYPOTHESES (written BEFORE data, per protocol):
H1: The descending-from-sqrtN procedure is EXACTLY the Bayes-optimal committed
    scan for the magnitude-induced posterior P(J | N's computable features), so
    its speedup can be located as a point (alpha_eff, mu_eff/M) on paper 143's
    grid -- expect mu_eff ~ spread of J's posterior given features, alpha_eff ~
    its total mass within that window; and the committed-interval scan run at
    the extracted parameters should REPRODUCE the observed descending speedup.
H2: The effective parameters are population-dependent (balance-strata
    dependent): near-square Ns map to narrow-high-alpha windows; unbalanced Ns
    to wide-low-alpha.

DESIGN:
  Population: 20k semiprimes, p,q uniform primes in [2^15,2^17], p<q.
  J = pi(p) = rank of the smaller factor among primes <= sqrt(N) ascending.
  M_N = pi(floor(sqrt(N))).  cost_asc = J ; cost_desc = M_N - J + 1.
  Stages:
   1 population + reproduce paper-137 desc speedup on this population;
     DC2 designed check: brute-force verify J and cost_desc on a subsample.
   2 conditional posterior P(J | M_N decile) -> empirical histograms.
   3 smallest window containing >=90% of mass per decile -> (mu/M, alpha)
     points; sensitivity at alpha in {0.5, 0.9, 0.95}.
   4 identity check: paper-143-style COMMITTED interval scan at extracted
     windows vs actual desc costs; closed-form expected cost
     E[cost] = E[J] + mu*beta_below - alpha*(start-1) for ascending-committed
     scan (DC1 designed check of that formula); cost-optimal window as
     secondary diagnostic; order-aware variant (window scanned descending).
   5 balance strata (quintiles of q/p): H2 gradient + translation table;
     locate points vs paper-143's 5.19x band (alpha=0.9, mu/M in [0.02,0.05]).
Barrier notes (protocol): (2) magnitude breaks symmetry at the sqrtN pivot --
this experiment lives entirely on barrier-2's mechanism. (8) Fermat is named:
the balance feature q/p and near-squareness are adjacent to Fermat's
m^2-d^2 identity; we do NOT use any Fermat method here, only stratify reporting
by true balance; M_N itself is Fermat-free.
Seed 20260831. Runtime target < 20 min (actual << 1 min).
"""
import json, math, os, time
import numpy as np

SEED  = 20260831
WD    = "/tmp/exp39_magint"
NPOP  = 20000
P_LO, P_HI = 1 << 15, 1 << 17          # 32768 .. 131072
PAPER137_ANCHOR = 5.19                  # x, sham-controlled desc speedup
P143_BAND = dict(alpha=0.9, mu_over_M=(0.02, 0.05), speedup=5.19)

os.makedirs(WD, exist_ok=True)
RES = os.path.join(WD, "result.json")
rng = np.random.default_rng(SEED)
T0 = time.time()

def checkpoint(stage, data):
    r = {}
    if os.path.exists(RES):
        with open(RES) as f: r = json.load(f)
    r[stage] = data
    r.setdefault("meta", dict(exp="exp479_MAGNITUDE-INTERVAL", seed=SEED,
                              npop=NPOP, plo=P_LO, phi=P_HI,
                              numpy=np.__version__))
    with open(RES, "w") as f: json.dump(r, f, indent=1, default=float)
    print(f"[checkpoint] {stage} written ({time.time()-T0:.1f}s)")

# ---------------------------------------------------------------- prime table
def sieve(limit):
    isp = np.ones(limit + 1, dtype=bool); isp[:2] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if isp[i]: isp[i*i::i] = False
    return np.flatnonzero(isp)

PRIMES = sieve(P_HI)
PI = np.cumsum(np.bincount(PRIMES, minlength=P_HI + 1)).astype(np.int64)  # PI[x]=pi(x)

def pi(x): return int(PI[x])

# ---------------------------------------------------------------- population
LO_IDX = int(np.searchsorted(PRIMES, P_LO))   # first prime >= 2^15

def draw_population(n=NPOP):
    out_p, out_q = [], []
    while len(out_p) < n:
        k = n - len(out_p)
        i = rng.integers(LO_IDX, len(PRIMES), size=k * 2)
        a, b = PRIMES[i[::2]], PRIMES[i[1::2]]
        lo, hi = np.minimum(a, b).astype(np.int64), np.maximum(a, b).astype(np.int64)
        keep = lo < hi                      # enforce strict p<q
        out_p += list(lo[keep]); out_q += list(hi[keep])
    return np.array(out_p[:n]), np.array(out_q[:n])

p_arr, q_arr = draw_population()
N_arr  = p_arr * q_arr
s_arr  = np.array([math.isqrt(int(x)) for x in N_arr])       # floor(sqrt(N))
M_arr  = PI[s_arr].astype(np.int64)                          # M_N
J_arr  = PI[p_arr].astype(np.int64)                          # pi(p)
cd_arr = M_arr - J_arr + 1                                   # cost_desc
ratio  = q_arr / p_arr                                       # true balance

# ---- DC2 designed check: brute-force trial division on a subsample ----------
def brute_costs(Nv):
    s = math.isqrt(Nv); c_asc = c_desc = 0; found_desc = False
    # ascending over primes <= s
    idx = 0
    for k in range(len(PRIMES)):
        pr = int(PRIMES[k])
        if pr > s: break
        c_asc += 1
        if Nv % pr == 0: break
    # descending from floor(sqrt(N)) down to the factor
    k = int(np.searchsorted(PRIMES, s, side="right")) - 1
    while k >= 0:
        c_desc += 1
        if Nv % int(PRIMES[k]) == 0: found_desc = True; break
        k -= 1
    assert found_desc
    return c_asc, c_desc

dc_n = 60
dc_idx = rng.choice(NPOP, size=dc_n, replace=False)
dc_err = 0
for t in dc_idx:
    ca, cd = brute_costs(int(N_arr[t]))
    if ca != int(J_arr[t]) or cd != int(cd_arr[t]): dc_err += 1

# ---------------------------------------------------------------- stage 1
EJ, ECD = float(J_arr.mean()), float(cd_arr.mean())
speedup_desc = EJ / ECD
stage1 = dict(E_J=EJ, E_cost_desc=ECD, speedup_desc=speedup_desc,
              paper137_anchor=PAPER137_ANCHOR,
              reproduction_ratio=speedup_desc / PAPER137_ANCHOR,
              median_M=float(np.median(M_arr)), mean_M=float(M_arr.mean()),
              min_M=int(M_arr.min()), max_M=int(M_arr.max()),
              mean_ratio_q_over_p=float(ratio.mean()),
              DC2_bruteforce_rows=dc_n, DC2_mismatches=int(dc_err))
checkpoint("stage1_population_and_repro", stage1)

# ---------------------------------------------------------------- helpers
def hist_of(mask):
    """counts over absolute positions [lo..hi] for samples in mask."""
    jlo, jhi = int(J_arr[mask].min()), int(M_arr[mask].max())
    cnt = np.bincount(J_arr[mask] - jlo, minlength=jhi - jlo + 1).astype(np.float64)
    return jlo, cnt

def extract_window(cnt, jlo, target_frac):
    """smallest-length contiguous window with mass >= target_frac (leftmost tie).
    returns (a_abs, mu, mass)."""
    tot = cnt.sum()
    target = target_frac * tot
    best = (10**9, 0, 0.0)                       # (len, start_idx, mass)
    l = 0; s = 0.0
    for r in range(len(cnt)):
        s += cnt[r]
        while s >= target and l <= r:
            if r - l + 1 < best[0]:
                best = (r - l + 1, l, s)
            s -= cnt[l]; l += 1
    mu, li, mass = best
    return jlo + li, mu, mass / tot

def prefix(cnt):
    return np.concatenate([[0.0], np.cumsum(cnt)])

def committed_asc_cost(j, a, mu):
    """paper-143 reconstruction: commit to scanning window [a,a+mu-1] ascending
    first; on miss continue ascending from 1 skipping scanned positions."""
    end = a + mu - 1
    return np.where((j >= a) & (j <= end), j - a + 1,
           np.where(j < a, mu + j, j))

def committed_descwin_cost(j, a, mu, Mref):
    """same window but scanned descending (order-aware diagnostic);
    on miss continue descending from M."""
    end = a + mu - 1
    return np.where((j >= a) & (j <= end), end - j + 1,
           np.where(j > end, mu + (Mref - j + 1), Mref - j + 1))

def optimal_window_closed_form(cnt, jlo, step_s=8, step_m=4):
    """minimise E[cost] = E[J] + mu*beta_below - alpha*(start-1) (ascending
    committed). Grid search; secondary diagnostic only."""
    prob = cnt / cnt.sum()                      # counts -> probability masses
    pf = prefix(prob); EJ = float((cnt * (np.arange(len(cnt)) + jlo)).sum() / cnt.sum())
    n = len(cnt); best = (np.inf, None)
    starts = np.arange(0, n, step_s)
    for st in starts:
        maxmu = n - st
        mus = np.arange(1, maxmu + 1, step_m)
        ends = st + mus - 1
        alpha = pf[ends + 1] - pf[st]
        beta  = pf[st]
        cost  = EJ + mus * beta - alpha * (jlo + st - 1)   # absolute start pos
        k = int(np.argmin(cost))
        if cost[k] < best[0]:
            best = (float(cost[k]), (jlo + int(st), int(mus[k])))
    EJ_mean_direct = None
    (a, mu) = best[1]
    return a, mu, best[0]

def group_analysis(mask, label, alphas=(0.5, 0.9, 0.95), main_alpha=0.9):
    """full translation-table row for one stratum."""
    jlo, cnt = hist_of(mask)
    Ej  = float(J_arr[mask].mean())
    Ecd = float(cd_arr[mask].mean())
    spd = Ej / Ecd
    row = dict(label=label, n=int(mask.sum()),
               M_ref=float(np.median(M_arr[mask])),
               E_J=Ej, E_cost_desc=Ecd, desc_speedup_local=spd)
    wins = {}
    for al in alphas:
        a, mu, mass = extract_window(cnt, jlo, al)
        wins[al] = (a, mu, mass)
    a, mu, mass = wins[main_alpha]
    row.update(window_start=a, window_end=a + mu - 1, mu=mu,
               mu_over_M=mu / row["M_ref"], alpha_nominal=main_alpha,
               alpha_eff=mass)
    row["alpha_curve"] = {str(al): dict(start=w[0], mu=w[1],
                           mu_over_M=w[1]/row["M_ref"], mass=w[2])
                          for al, w in wins.items()}
    # committed scans at extracted window (per-sample, this group)
    jj = J_arr[mask]
    c_comm = committed_asc_cost(jj, a, mu)
    c_dwin = committed_descwin_cost(jj, a, mu, int(row["M_ref"]))
    row["committed_asc_speedup"]   = Ej / float(c_comm.mean())
    row["committed_descwin_speedup"] = Ej / float(c_dwin.mean())
    row["identity_gap"]   = row["committed_asc_speedup"] - spd      # H1 literal test
    row["frac_recovered"] = row["committed_asc_speedup"] / spd
    row["corr_desc_vs_committed"] = float(np.corrcoef(cd_arr[mask], c_comm)[0, 1])
    # cost-optimal window (secondary)
    oa, omu, oc = optimal_window_closed_form(cnt, jlo)
    c_opt = committed_asc_cost(jj, oa, omu)
    row["opt_window"] = dict(start=oa, mu=omu,
                             mu_over_M=omu/row["M_ref"])
    row["committed_opt_speedup"] = Ej / float(c_opt.mean())
    # DC1: closed-form vs direct expectation at the extracted window
    pf = prefix(cnt)
    alpha_cf = pf[a + mu - 1 - jlo + 1] - pf[a - jlo]
    beta_cf  = pf[a - jlo]
    cf = Ej + mu * beta_cf - alpha_cf * (a - 1)
    row["DC1_closed_form_Ecost"] = float(cf)
    row["DC1_direct_Ecost"]      = float(c_comm.mean())
    row["DC1_abs_err"]           = abs(cf - float(c_comm.mean()))
    return row, (mask, jj, c_comm)

# ---------------------------------------------------------------- stage 2+3+4
# deciles of M_N
qs = np.quantile(M_arr, np.linspace(0, 1, 11))
dec = np.clip(np.searchsorted(qs, M_arr, side="right") - 1, 0, 9)
rows_dec, carry = [], []
for d in range(10):
    m = dec == d
    if m.sum() < 50: continue
    row, cg = group_analysis(m, f"Mdecile_{d}")
    rows_dec.append(row); carry.append(cg)
checkpoint("stage234_MN_decile_translation", dict(rows=rows_dec))

# pooled single window (no feature info beyond global prior)
row_pool, _ = group_analysis(np.ones(NPOP, dtype=bool), "POOLED")
checkpoint("stage234b_pooled_window", row_pool)

# ---------------------------------------------------------------- stage 5
# balance strata: quintiles of q/p  (true balance -- H2)
bq = np.quantile(ratio, np.linspace(0, 1, 6))
bal = np.clip(np.searchsorted(bq, ratio, side="right") - 1, 0, 4)
rows_bal = []
for b in range(5):
    m = bal == b
    if m.sum() < 50: continue
    row, _ = group_analysis(m, f"balance_Q{b+1}")
    row["ratio_lo"] = float(bq[b]); row["ratio_hi"] = float(bq[b+1])
    row["mean_log_ratio"] = float(np.log(ratio[m]).mean())
    rows_bal.append(row)
# H2 summary: monotonicity of mu_over_M and alpha_eff across balance quintiles
mu_trend  = [r["mu_over_M"] for r in rows_bal]
al_trend  = [r["alpha_eff"]  for r in rows_bal]
spd_trend = [r["desc_speedup_local"] for r in rows_bal]
h2 = dict(mu_over_M_by_balance=mu_trend, alpha_eff_by_balance=al_trend,
          desc_speedup_by_balance=spd_trend,
          mu_monotone_decreasing=all(mu_trend[i] >= mu_trend[i+1] - 1e-12
                                     for i in range(len(mu_trend)-1)),
          alpha_monotone_increasing=all(al_trend[i] <= al_trend[i+1] + 1e-12
                                        for i in range(len(al_trend)-1)),
          speedup_gradient=max(spd_trend)/min(spd_trend))
checkpoint("stage5_balance_strata", dict(rows=rows_bal, h2_summary=h2))

# ---------------------------------------------------------------- stage 6
# locate on paper-143 plane + overall identity verdict
allc = np.empty(NPOP)
for (m, jj, cc) in carry: allc[m] = cc
overall = dict(
    desc_speedup=speedup_desc,
    committed_asc_speedup_at_extracted=EJ / float(allc.mean()),
    frac_of_desc_recovered=(EJ/float(allc.mean())) / speedup_desc,
    spearmanish_corr=float(np.corrcoef(cd_arr, allc)[0, 1]),
    pooled_mu_over_M=row_pool["mu_over_M"], pooled_alpha=row_pool["alpha_eff"],
    p143_band=P143_BAND,
    in_p143_band=bool(row_pool["mu_over_M"] <= P143_BAND["mu_over_M"][1]),
    DC1_max_abs_err=max(r["DC1_abs_err"] for r in rows_dec),
    DC2_mismatches=int(dc_err))
checkpoint("stage6_identity_and_grid_location", overall)

print("\n=== SUMMARY ===")
print(f"pop: {NPOP}, M in [{M_arr.min()},{M_arr.max()}], "
      f"E[J]={EJ:.1f} E[desc]={ECD:.1f}")
print(f"desc speedup = {speedup_desc:.3f}x  (paper137 anchor {PAPER137_ANCHOR}x)")
print(f"POOLED window: a={row_pool['window_start']} mu={row_pool['mu']} "
      f"mu/M={row_pool['mu_over_M']:.3f} alpha={row_pool['alpha_eff']:.3f} "
      f"-> committed {row_pool['committed_asc_speedup']:.3f}x "
      f"(desc {row_pool['desc_speedup_local']:.3f}x)")
print("\nM_N deciles:")
for r in rows_dec:
    print(f" {r['label']}: M~{r['M_ref']:.0f} mu/M={r['mu_over_M']:.3f} "
          f"alpha={r['alpha_eff']:.3f} desc={r['desc_speedup_local']:.2f}x "
          f"comm={r['committed_asc_speedup']:.2f}x "
          f"dwin={r['committed_descwin_speedup']:.2f}x "
          f"opt={r['committed_opt_speedup']:.2f}x")
print("\nBalance quintiles (q/p low->high):")
for r in rows_bal:
    print(f" {r['label']}: q/p[{r['ratio_lo']:.2f},{r['ratio_hi']:.2f}] "
          f"mu/M={r['mu_over_M']:.3f} alpha={r['alpha_eff']:.3f} "
          f"desc={r['desc_speedup_local']:.2f}x comm={r['committed_asc_speedup']:.2f}x")
print(f"\nidentity: recovered {overall['frac_of_desc_recovered']*100:.1f}% of desc "
      f"speedup by committed interval at extracted params; corr="
      f"{overall['spearmanish_corr']:.3f}; DC1err={overall['DC1_max_abs_err']:.2e}; "
      f"DC2 mismatches={overall['DC2_mismatches']}")
worst = max(rows_dec, key=lambda r: r["DC1_abs_err"])
print(f"DC1 worst row {worst['label']}: a={worst['window_start']} mu={worst['mu']} "
      f"cf={worst['DC1_closed_form_Ecost']:.3f} direct={worst['DC1_direct_Ecost']:.3f}")
print(f"H2: mu monotone-decr={h2['mu_monotone_decreasing']} "
      f"alpha monotone-incr={h2['alpha_monotone_increasing']} "
      f"speedup gradient={h2['speedup_gradient']:.1f}x")

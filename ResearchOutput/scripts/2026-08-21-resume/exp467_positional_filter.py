#!/usr/bin/env python3
# EXP 467 "POSITIONAL-FILTER" — round-38. First quantitative measurement of the
# POSITIONAL stratum of paper 132's residual gap: how much expected trial-division
# speedup does N-COMPUTABLE MAGNITUDE information buy, when the test stays
# divisibility and only the ORDER of candidate primes varies?
#
# ============================================================================
# PRE-STATED HYPOTHESES (written BEFORE any data; seed fixed 20260821)
# ============================================================================
# H1 (brief): An ordering of candidates by N-dependent magnitude priors beats
#    ascending by a CONSTANT factor > 1; gain concentrates on balanced N (q/p->1)
#    and vanishes on unbalanced draws.
#
# H2 (brief anchor): The optimal N-computable ordering gain is bounded by a small
#    constant (< 2x) averaged over uniform random semiprimes.
#
# PRE-REGISTERED ANALYTIC DERIVATION (also before data; may put H2 at risk):
#  * Bayes-flavored analysis: for a magnitude feature that pins N to relative
#    precision eps = 2^-k (top-k bits), P(p=r | N_hat) is proportional to
#    #{prime q in [(N_hat-W/2)/r, (N_hat+W/2)/r]} which for k <= ~14 is smooth
#    and ~ W/(r log(N_hat/r)). This posterior is STRICTLY DECREASING in r
#    (since log(N/r) > 1 on our range), so search-theory-optimal ordering by
#    descending posterior COLLAPSES TO ASCENDING ORDER. Consequence: key
#    r*log(N/r) is strictly monotone increasing on r <= sqrt(N), so the
#    analytic Bayes ordering (d1) must equal ascending EXACTLY — we run it as a
#    DESIGNED CHECK (costs must match to machine precision).
#  * Why can anything beat ascending then? Because at FULL N precision the
#    finite-window smoothness breaks: the consistent set {(r, N/r) both prime}
#    is a spiky lattice and P(p=r|N) does not converge to the smooth tilt.
#    A computable heuristic can bet on the JOINT geometry (p near sqrt(N) iff
#    q/p near 1) without resolving the lattice — this is exactly paper 132's
#    residual-gap item (1): magnitude info used beyond residues.
#  * Quantitative pre-diction for balanced-first pruned to r <= floor(sqrt N):
#    cost(b1 | bin) ~ (sqrt(N)-p)/log(sqrt N); baseline ~ p/log p. With mean
#    t=p/sqrt(N) per ratio-bin [t_min = 1/sqrt(ratio_max)]:
#      bin q/p in [1,1.25): t in (0.894,1), pred speedup ~ (0.93*10.8)/(10.6*(1-t))
#        ~ 9-19x   (my integration guess ~15x)
#      bin [1.25,2): t in (0.707,0.894) -> pred ~ 3-5x
#      bin [2,4):    t in (0.5,0.707)   -> pred ~ 1.3-2x
#      bin [4,16):   EMPTY by construction (q/p <= 2^17/2^15 = 4 exactly);
#                    reported as n=0 honestly.
#    Population mass of bin1 under iid uniform draw ~ 0.30, so OVERALL speedup
#    of balanced-first integrates to roughly 4-8x — ABOVE H2's <2x anchor.
#    We therefore pre-register H2 as AT RISK from our own derivation, and let
#    the simulation adjudicate. If overall < 2x, the smooth-posterior collapse
#    wins; if > 2x, position pays beyond the residue cap on this population.
#
# DISCLOSURES / DESIGN DECISIONS (pre-stated):
#  * Candidate universe U(N) = ALL primes <= floor(sqrt(N)) for EVERY ordering,
#    ascending included (r > sqrt(N) can never be p since p < q => p < sqrt N;
#    visiting them is dominated waste — excluded globally, not per-ordering).
#    Every ordering is COMPLETE on U(N).
#  * Cost = number of divisibility tests until hit = rank of p in the ordering
#    (+1). Speedup reported as RATIO OF EXPECTED COSTS E[C_asc]/E[C_ord]
#    (expected cost is trial division's currency), SE over 5 batches.
#  * Ties in an ordering's key are broken ASCENDING r (N-independent rule,
#    disclosed). Cost formula: count(key < kp) + count(key == kp AND r < p)+1.
#  * Train/test split for (c): even-indexed batches (0,2,4) TRAIN, odd (1,3)
#    TEST. No test item contributes to its own scoring table.
#  * Sham control: within-batch random permutation pairing true p with WRONG N
#    features (kills N-dependence, keeps marginal candidate stats). Real
#    orderings must beat their shams or the gain is not positional.
#  * Honest accounting: each N's features (bitlen, top bits, isqrt, logs) are
#    computed ONCE per N, amortized over |U(N)| ~ sqrt(N)/log ~ thousands of
#    tests — negligible (< 1e-4 of one test per candidate); stated, not hidden.
#  * Ordering (b2) |r^2 - N| proximity IS Fermat's visitation intuition applied
#    to divisibility tests: start at floor(sqrt(N)), spiral outward. BARRIER
#    LINE (8) FERMAT-IN-DISGUISE: same start, same balance-bet, different test.
#    BARRIER LINE (2) SYMMETRY: keys are symmetric functions of the pair via N;
#    BARRIER LINE (4) AGGREGATION: expected-cost ratio aggregates per-N ranks.
#
# METHOD LEDGER (bugs/mis-steps caught; appended during run):
#  ML#1 (pre-run, caught by self-review before first execution): d2 window cost
#    arithmetic wrong in first draft (kp_pos-i_lo+1 instead of lenc-ipos);
#    fixed pre-run.
#  ML#2 (pre-run): feats() contained dead conditional-leftover code and
#    batch_costs referenced a `bucket` parameter that was never passed
#    (would NameError); cleaned/fixed pre-run.
#  ML#3 (run-1 finding, not a bug): orderings b1 (log-proximity), b2 (|r^2-N|,
#    the literal Fermat visitation order), and d2 (tuned window w*=2.0) are
#    IDENTICAL procedures on this population: on r <= sqrt(N) both keys are
#    strictly decreasing in r => pure descending-from-floor(sqrt(N)); and
#    q/p <= HI/LO = 4 forces p > sqrt(N)/2, so any w >= 2 window covers all p.
#    Three intended-distinct orderings collapse to one; reported as such.
#  ML#4 (run-1 finding, hypothesis-level refutation of our own derivation):
#    the pre-stated smooth-posterior claim "any magnitude-Bayes ordering
#    collapses to ascending" is WRONG once the finite pool [2^15,2^17] is
#    respected: feasibility truncates r >= N/HI, and N's magnitude reveals
#    that lower bound. The learned top-10-bit posterior (c) exploits exactly
#    this (test-only 3.37x vs predicted ~1.0x). The d1==asc DESIGNED CHECK
#    still passed exactly (it validates only the UNtruncated smooth tilt).
#  ML#5 (run-2 crash -> reasoning error found): f_trunc_desc was misconceived.
#    Truncation cannot shorten a descending scan: everything above p is
#    feasible (p >= ceil(N/HI)), so f == b1 identically. First draft also had
#    a sign error (lenc-ipos-n_below, produced negative costs -> KeyError in
#    aggregation). Fixed to the provably-correct lenc-ipos and demoted to a
#    designed equivalence check; SHAM_f dropped as redundant with SHAM_b1.
#    Also caught: an edit briefly deleted the `w = w_map[t]` line SHAM_d2
#    needs; restored before running.
#  ML#6 (run-4): selector feature bal = N/isqrt(N)^2 is identically
#    1 + O(1/sqrt(N)) — vacuous by definition; all tau tied, g silently
#    collapsed to descending. Replaced by a LEARNED per-top-k-bit-bucket
#    winner between the two orderings (train-only). Structural lesson kept:
#    factor-balance is not an O(1)-computable scalar of N — reading it costs
#    exactly what Fermat's scan costs.
# ============================================================================

import json, math, time
import numpy as np

T0 = time.time()
SEED = 20260821
N_BATCHES, BATCH_N = 5, 6000           # 30k semiprimes total
LO, HI = 1 << 15, 1 << 17              # prime range [2^15, 2^17]
UBINS, TOPBITS_K = 64, 10              # (c): 64 log-p bins x top-10-bit buckets
RATIO_EDGES = [1.0, 1.25, 2.0, 4.0, 16.0]

rng = np.random.default_rng(SEED)

# ---------- primes up to HI (sieve) ----------
def sieve(n):
    m = np.ones(n + 1, dtype=bool); m[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if m[i]: m[i*i::i] = False
    return np.flatnonzero(m)

PRIMES = sieve(HI)
P_LO_IDX = int(np.searchsorted(PRIMES, LO, 'left'))   # first prime >= 2^15
pool = PRIMES[P_LO_IDX:]                              # drawable primes
LOGPOOL = np.log(pool.astype(np.float64))

def gen_batch(n):
    """iid uniform primes p,q from pool, enforce p<q."""
    i = rng.integers(0, len(pool), size=2 * n)
    ps = pool[i]
    p = np.minimum(ps[0::2], ps[1::2])
    q = np.maximum(ps[0::2], ps[1::2])
    keep = p != q
    p, q = p[keep], q[keep]
    while len(p) < n:
        j = rng.integers(0, len(pool), size=2 * n)
        a, b = pool[j[0::2]], pool[j[1::2]]
        a2, b2 = np.minimum(a, b), np.maximum(a, b)
        k = a2 != b2
        p = np.concatenate([p, a2[k]]); q = np.concatenate([q, b2[k]])
    return p[:n].astype(np.int64), q[:n].astype(np.int64)

# vectorized integer sqrt
def vec_isqrt(x):
    r = np.sqrt(x.astype(np.float64)).astype(np.int64)
    r = np.where((r + 1) * (r + 1) <= x, r + 1, r)
    r = np.where(r * r > x, r - 1, r)
    return r

ORDERINGS = ["asc", "b1_logprox_pruned", "b2_fermat_rsq", "c_bayes_train",
             "d1_analytic_check", "d2_tuned_window",
             "e_trunc_asc", "f_trunc_desc", "g_selector",
             "SHAM_b1", "SHAM_c", "SHAM_d2"]
# (g) computable selector: balance is N-computable (N/s^2 ~ (q/p)^2); pick
#     sqrt-descending when N is near-square, trunc-ascending otherwise.
#     tau tuned on TRAIN batches only, grid TAU_GRID, applied to test.
# (e) truncation-pruned ascending: pool range [2^15,2^17] is POPULATION
#     knowledge; given N, feasibility forces r >= N/HI. Posterior under the
#     smooth+TRUNCATED model is 1/(r log(N/r)) on [ceil(N/HI), sqrt(N)] ->
#     ascending within the truncated set, skipping the infeasible tail.
#     This is the corrected Bayes response after ML#4 (see ledger).
# (f) trunc-pruned descending: sqrt-descending restricted to the feasible set;
#     the best simple computable candidate for the positional CAP probe.
W_GRID = [1.05, 1.10, 1.25, 1.50, 2.00, 4.00]   # d2 window, tuned on train
TAU_GRID = [1.3, 1.6, 2.0, 2.5, 3.2, 4.0]       # g balance threshold, train

def ubin_of_logr(lr):
    u = (lr - math.log(2)) / (math.log(HI) - math.log(2))
    return np.clip((u * UBINS).astype(np.int64), 0, UBINS - 1)

results = {"config": {"seed": SEED, "n_batches": N_BATCHES, "batch_n": BATCH_N,
                      "prime_range": [LO, HI], "ratio_edges": RATIO_EDGES,
                      "ubins": UBINS, "topbits_k": TOPBITS_K,
                      "w_grid": W_GRID,
                      "universe": "primes <= floor(sqrt(N))"},
           "batches": []}

# pass 1 over train batches builds (c)'s score table; we generate all batches
# up front (seeded), then do two passes: count pass (train), eval pass (all).
batches = [gen_batch(BATCH_N) for _ in range(N_BATCHES)]
print(f"[{time.time()-T0:6.1f}s] generated {N_BATCHES*BATCH_N} semiprimes", flush=True)

def feats(p, q):
    N = p.astype(np.object_) * q          # python ints, exact
    Ni = np.fromiter((int(x) for x in N), dtype=np.int64, count=len(N))
    Nb = np.array([int(x).bit_length() for x in N], dtype=np.int64)
    s = vec_isqrt(Ni)
    topk = np.array([int(x) >> (int(b) - TOPBITS_K)
                     for x, b in zip(N, Nb)], dtype=np.int64)
    return N, Nb, s, topk

def batch_costs(pi, qi, w_map=None, train_table=None, g_table=None):
    """Return dict ord_name -> per-item cost array; w_map for tuned d2."""
    N_, Nb, sq, topk = feats(pi, qi)
    logN2 = np.log(N_.astype(np.float64)) / 2.0
    hi_idx = np.searchsorted(PRIMES, sq, 'right')     # |U(N)| = hi_idx
    out = {k: np.empty(len(pi), dtype=np.int64) for k in ORDERINGS}
    ratio = qi / pi.astype(np.float64)

    for t in range(len(pi)):
        p = int(pi[t]); NN = int(N_[t]); s = int(sq[t])
        cand = PRIMES[:hi_idx[t]]                     # universe, ascending
        cr = cand.astype(np.float64)
        lenc = len(cand)
        ipos = int(np.searchsorted(cand, p))          # p is in cand
        kp_pos = ipos
        # asc
        out["asc"][t] = ipos + 1
        # b1: |log r - logN/2| asc, ties asc-r
        key = np.abs(np.log(cr) - logN2[t])
        kb = key[ipos]
        out["b1_logprox_pruned"][t] = (np.count_nonzero(key < kb)
                                       + np.count_nonzero((key == kb) & (cand < p))
                                       + 1)
        # b2 Fermat-order: |r^2 - N| asc
        key2 = np.abs(cr * cr - float(NN))
        k2 = key2[ipos]
        out["b2_fermat_rsq"][t] = (np.count_nonzero(key2 < k2)
                                   + np.count_nonzero((key2 == k2) & (cand < p))
                                   + 1)
        # d1 analytic Bayes: key r*log(N/r) asc == descending 1/(r log(N/r))
        kd = cr * np.log(float(NN) / cr)
        kdd = kd[ipos]
        c_d1 = (np.count_nonzero(kd < kdd)
                + np.count_nonzero((kd == kdd) & (cand < p)) + 1)
        out["d1_analytic_check"][t] = c_d1
        if c_d1 != ipos + 1:
            print(f"DESIGNED-CHECK FAIL d1!=asc at t={t}: {c_d1} vs {ipos+1}",
                  flush=True)
        # c bayes (needs table)
        if train_table is not None:
            sc = train_table[topk[t]][ubin_of_logr(np.log(cr))]
            kc = -sc
            kcb = kc[ipos]
            out["c_bayes_train"][t] = (np.count_nonzero(kc < kcb)
                                       + np.count_nonzero((kc == kcb) & (cand < p))
                                       + 1)
        else:
            out["c_bayes_train"][t] = -1
        # d2 tuned window: [sqrt/w, sqrt] desc first, then rest asc
        w = w_map[t]
        lo_cut = max(2, int(s // w))
        i_lo = int(np.searchsorted(cand, lo_cut))
        if ipos >= i_lo:      # p inside window: desc from s down to p
            out["d2_tuned_window"][t] = lenc - ipos
        else:                 # whole window tried, then asc up to p
            out["d2_tuned_window"][t] = (lenc - i_lo) + ipos + 1
        # e/f truncation-pruned orderings
        lo_cut = -(-NN // HI)                      # ceil(N / 2^17)
        n_below = int(np.searchsorted(PRIMES, lo_cut, 'left'))  # primes < lo_cut
        out["e_trunc_asc"][t] = ipos + 1 - n_below
        # f trunc-desc: ML#5 (ledger) — truncation CANNOT shorten a descending
        # scan (everything above p is feasible), so f == b1 by construction;
        # kept as a designed equivalence check, cost = |[p, s]| + 1:
        out["f_trunc_desc"][t] = lenc - ipos
        # g selector: per-bucket winner learned on train batches
        if g_table is not None:
            out["g_selector"][t] = ((lenc - ipos) if
                                    g_table.get(int(topk[t]), True)
                                    else (ipos + 1 - n_below))
        else:
            out["g_selector"][t] = -1   # tuning passes: not yet defined
    # shams: features from permuted items against true p
    perm = rng.permutation(len(pi))
    Np, Nbp, sqp, topp = feats(pi[perm], qi[perm])
    logN2p = np.log(Np.astype(np.float64)) / 2.0
    hi_p = np.searchsorted(PRIMES, sqp, 'right')
    for t in range(len(pi)):
        p = int(pi[t]); s = int(sqp[t]); NN = int(Np[t])
        h = hi_p[t]
        if h < 1:
            out["SHAM_b1"][t] = out["asc"][t]; out["SHAM_d2"][t] = out["asc"][t]
            out["SHAM_c"][t] = out["asc"][t]
            continue
        cand = PRIMES[:h]; cr = cand.astype(np.float64)
        if p > int(sqp[t]):   # p outside sham universe: would never be reached;
            out["SHAM_b1"][t] = h + 1   # complete procedure exhausts universe
            out["SHAM_c"][t] = h + 1
            out["SHAM_d2"][t] = h + 1
            continue
        ipos = int(np.searchsorted(cand, p))
        key = np.abs(np.log(cr) - logN2p[t]); kb = key[ipos]
        out["SHAM_b1"][t] = (np.count_nonzero(key < kb)
                             + np.count_nonzero((key == kb) & (cand < p)) + 1)
        if train_table is not None:
            sc = train_table[topp[t]][ubin_of_logr(np.log(cr))]
            kc = -sc; kcb = kc[ipos]
            out["SHAM_c"][t] = (np.count_nonzero(kc < kcb)
                                + np.count_nonzero((kc == kcb) & (cand < p)) + 1)
        w = w_map[t]
        lo_cut = max(2, int(s // w)); i_lo = int(np.searchsorted(cand, lo_cut))
        if ipos >= i_lo:
            out["SHAM_d2"][t] = h - ipos
        else:
            out["SHAM_d2"][t] = (h - i_lo) + ipos + 1
    return out, ratio

def summarize(costs, ratio):
    res = {}
    bins = np.digitize(ratio, RATIO_EDGES) - 1  # 0..3
    for name, c in costs.items():
        valid = c[c >= 0]
        if valid.size == 0:
            continue
        entry = {"mean": float(valid.mean()), "n": int(valid.size)}
        for b in range(4):
            m = (bins == b) & (c >= 0)
            entry[f"bin{b}"] = {"mean": float(c[m].mean()) if m.any() else None,
                                "n": int(m.sum())}
        res[name] = entry
    return res

# ---- pass A: train (c) table on even batches ----
from collections import defaultdict
counts = defaultdict(lambda: np.zeros(UBINS))
glob = np.zeros(UBINS)
for bi in range(0, N_BATCHES, 2):
    pi, qi = batches[bi]
    _, _, _, topk = feats(pi, qi)
    lr = LOGPOOL[np.searchsorted(pool, pi)]
    ub = ubin_of_logr(lr)
    for tk, u in zip(topk, ub):
        counts[int(tk)][u] += 1
        glob[u] += 1
ALPHA = 20.0
gmarg = (glob + 1e-9) / (glob + 1e-9).sum()
table = {}
for tk, cnt in counts.items():
    tot = cnt.sum()
    table[tk] = (cnt + ALPHA * gmarg) / (tot + ALPHA)
def tab_get(tk):
    return table.get(int(tk), gmarg)
class TableWrap:
    def __getitem__(self, tk): return tab_get(tk)
TT = TableWrap()
print(f"[{time.time()-T0:6.1f}s] bayes table built: {len(table)} buckets "
      f"(train = even batches)", flush=True)

# ---- pass B: tune d2 window on TRAIN batches only ----
w_scores = {w: [] for w in W_GRID}
for bi in range(0, N_BATCHES, 2):
    pi, qi = batches[bi]
    _, _, sq, _ = feats(pi, qi)
    for w in W_GRID:
        wm = np.full(len(pi), w)
        cst, _ = batch_costs(pi, qi, w_map=wm)   # reuse; c-table unused here ok
        w_scores[w].append(cst["d2_tuned_window"].mean())
W_STAR = min(W_GRID, key=lambda w: np.mean(w_scores[w]))
print(f"[{time.time()-T0:6.1f}s] d2 tuned w*={W_STAR} (train-only)", flush=True)

# ---- pass B2: learn (g) per-bucket winner on TRAIN batches only ----
# ML#6 (ledger): first version keyed the selector on bal = N/isqrt(N)^2,
# which is identically ~1.00003 by definition of integer sqrt — vacuous,
# all tau tied. Structural lesson: near-squareness of the FACTORS is not an
# O(1)-computable scalar of N (Fermat's scan is exactly the cost of reading
# it); we therefore let the model CHOOSE per top-k-bit bucket which of the
# two orderings {sqrt-descending, trunc-ascending} had lower TRAIN cost.
_gwin = {}   # bucket -> True if descending wins
_gstats = {}
for bi in range(0, N_BATCHES, 2):
    pi, qi = batches[bi]
    wm = np.full(len(pi), W_STAR)
    cst, _ = batch_costs(pi, qi, w_map=wm)
    _, _, _, topk = feats(pi, qi)
    cd, ce = cst["b1_logprox_pruned"], cst["e_trunc_asc"]
    for tk in np.unique(topk):
        m = topk == tk
        _gstats.setdefault(int(tk), [0.0, 0.0, 0])
        _gstats[int(tk)][0] += float(cd[m].sum())
        _gstats[int(tk)][1] += float(ce[m].sum())
        _gstats[int(tk)][2] += int(m.sum())
for tk, (sd, se_, n_) in _gstats.items():
    _gwin[tk] = sd <= se_
print(f"[{time.time()-T0:6.1f}s] g selector: {len(_gwin)} buckets, "
      f"{sum(_gwin.values())} -> descending (train-only)", flush=True)
results["d2_tuning"] = {str(w): float(np.mean(v)) for w, v in w_scores.items()}
with open("/tmp/exp38_positional/result.json", "w") as f:
    json.dump(results, f, indent=1)   # checkpoint

# ---- pass C: evaluate all batches (test discipline disclosed: (c) trained on
# even batches only; its numbers are reported on ALL batches and on TEST-ONLY
# (odd) batches separately below) ----
for bi in range(N_BATCHES):
    pi, qi = batches[bi]
    _, _, _, topk = feats(pi, qi)
    wm = np.full(len(pi), W_STAR)
    costs, ratio = batch_costs(pi, qi, w_map=wm, train_table=TT,
                               g_table=_gwin)
    summ = summarize(costs, ratio)
    results["batches"].append({"batch": bi, "role": "train" if bi % 2 == 0
                               else "test", "summary": summ})
    with open("/tmp/exp38_positional/result.json", "w") as f:
        json.dump(results, f, indent=1)
    print(f"[{time.time()-T0:6.1f}s] batch {bi} ({'train' if bi%2==0 else 'test'})"
          f" done: asc={summ['asc']['mean']:.1f} "
          f"b1={summ['b1_logprox_pruned']['mean']:.1f}", flush=True)

# ---- aggregate ----
def agg(name, role=None):
    ms, ns = [], []
    for b in results["batches"]:
        if role and b["role"] != role:
            continue
        e = b["summary"].get(name)
        if e and e["n"] > 0:
            ms.append(e["mean"]); ns.append(e["n"])
    return (float(np.mean(ms)), float(np.std(ms, ddof=1) / np.sqrt(len(ms)))
            if len(ms) > 1 else 0.0), sum(ns)

final = {}
for name in ORDERINGS:
    (m, se), n = agg(name)
    final[name] = {"mean_cost": m, "se": se, "n": n}
for name in ORDERINGS:
    if name == "asc":
        continue
    (m, se), _ = agg(name)
    (ma, sea_), _ = agg("asc")
    final[name]["speedup_vs_asc"] = ma / m
# test-only rows for (c) leakage check
(mtest, setest), ntest = agg("c_bayes_train", role="test")
(mtr, setr), ntr = agg("c_bayes_train", role="train")
(final)["c_test_only"] = {"mean_cost": mtest, "se": setest, "n": ntest}
(final)["c_train_only"] = {"mean_cost": mtr, "se": setr, "n": ntr}
(ma, _), _ = agg("asc")
(final)["c_test_only"]["speedup_vs_asc"] = ma / mtest
(final)["c_train_only"]["speedup_vs_asc"] = ma / mtr
# stratified aggregate across batches
strata = {}
bins_names = ["1-1.25", "1.25-2", "2-4", "4-16"]
for name in ORDERINGS:
    strata[name] = {}
    for b in range(4):
        vals = [bb["summary"][name][f"bin{b}"]["mean"]
                for bb in results["batches"]
                if bb["summary"][name][f"bin{b}"]["n"] > 0]
        cnt = sum(bb["summary"][name][f"bin{b}"]["n"]
                  for bb in results["batches"])
        strata[name][bins_names[b]] = {
            "mean_of_batches": float(np.mean(vals)) if vals else None,
            "n": cnt}
final["strata_mean_costs"] = strata
final["runtime_s"] = time.time() - T0
results["final"] = final
with open("/tmp/exp38_positional/result.json", "w") as f:
    json.dump(results, f, indent=1)
print(json.dumps({k: v for k, v in final.items()
                  if not isinstance(v, dict) or "mean_cost" in v}, indent=1),
      flush=True)
print(f"[{time.time()-T0:6.1f}s] DONE", flush=True)

#!/usr/bin/env python3
"""
EXP491 TABLE-CLOSURE (round-42) — close the four character-pinned fork-channel
tables g(n), Is(n), A(n), X(n) (papers 72-74 closed forms) for n = 2..25 in
exact arithmetic, verify their inequality structure, and tie the Is row at
n=17 to a 200k-draw MC simulation of the underlying channel object.

=====================================================================
PRE-STATED HYPOTHESES (recorded BEFORE any data / computation)
=====================================================================
H1 (split-count dominance): Is(n) >= max(g, A, X)(n) for ALL n >= 2 up to 25.
    Known from the lab: A overtakes X from n=8 (A(7) < X(7), A(8) > X(8)).
    Verify no other crossover in {A vs X}, and check A >= g everywhere.

H2 (shapes): g(n) monotone decreasing; A(n) decreasing after its peak;
    X(n) -> log2-ish decay; each channel -> 0 as n -> infinity.

H3 (asymptotics AS STATED IN THE ASSIGNMENT):
    g ~ (2 log2 n)/n^2,  A ~ (2 log2 n)/n^2,  X ~ (4 log2 n)/n^2,
    i.e. X/g -> 2 within 10% by n=25.

---------------------------------------------------------------------
PRE-DATA ANALYTIC DERIVATION (pure symbolics, no numerics run yet;
sharpens what H3 can and cannot mean). With a = 1/n, L = log2 n,
lge = log2 e = 1.4427, Taylor expansion of H(x) at the natural points
gives that the L/n^2 terms CANCEL EXACTLY in g and X:

    g(n)   = (1 + lge)/n^2 + O(a^3 L)      ~= 2.4427/n^2
    X(n)   = 2(1 + lge)/n^2 + O(a^3 L)     ~= 4.8854/n^2
    A(n)   = (L + a*lge)/n^2 + O(a^4)      ~ (log2 n)/n^2
    Is(n)  ~= g + (L + 1)/n^2 = (L + 2 + lge)/n^2 ~ (log2 n)/n^2

PRE-REGISTERED PREDICTIONS from this derivation (to be checked against
the exact table; these are predictions, not data):
    P1: H3's stated functional FORMS are wrong in leading order for all
        three of g, A, X (g and X lose the log entirely -> pure 1/n^2;
        A keeps ONE power of L, not two; X is not 4L/n^2).
    P2: nevertheless X/g -> 2 EXACTLY (ratio of the 1/n^2 constants
        2(1+lge)/(1+lge)), with relative convergence rate O(a*L), so the
        "within 10% by n=25" clause may fail even though the limit is 2.
    P3: Is - A -> (2 + lge)/n^2 = 3.4427/n^2 (strict, positive);
        Is - g -> (L + 1)/n^2; Is - X -> (L - 1.443)/n^2 — H1 holds with
        explicit asymptotic margins; A/g -> L/(1+lge) -> infinity slowly.
Predicted constants to verify on the diagnostic series (n up to 2560):
    lim g(n)*n^2 = 1 + log2(e) = 2.4426950409
    lim X(n)*n^2 = 2 + 2*log2(e) = 4.8853900818
    lim (Is-A)(n)*n^2 = 2 + log2(e) = 3.4426950409
    lim Is*n^2/L = lim A*n^2/L = 1;   lim X/g = 2.

---------------------------------------------------------------------
SEMANTIC MODEL (derived pre-data from the closed forms themselves; used
only for the MC tie-in and an exact enumeration cross-check):
  Draw U, V iid uniform on Z_n; distinguished class S = {0};
    K = 1[U in S] + 1[V in S] ~ Bin(2, 1/n)     (split count)
    W = 1[U == V]                              (class-collision dial)
  Then EXACTLY (Bayes-consistency asserted in-code as rational algebra):
    P(K=(0,1,2) | W=1) = ((n-1)/n, 0, 1/n),  P(W=1) = 1/n
    P(K=(0,1,2) | W=0) = ((n-2)/n, 2/n, 0)
  so Is(n) = I(K; W) = H(Bin(2,1/n)) - (1/n)H((n-1)/n,0,1/n)
                       - ((n-1)/n)H((n-2)/n,2/n,0).
  Likewise g(n) = I(T_OR; W), X(n) = I(T_XOR; W) with T_OR = OR of the
  two hit indicators, T_XOR = exactly-one-hit; and A(n) = I(T_AND; 1[V in S]).
  The enumeration cross-check computes all four MIs from the exact
  n^2-pair joint and asserts agreement with the closed forms.

DECISION RULES (pre-stated):
  H1 PASS iff min over n in [2,25] of Is - max(g,A,X) >= -1e-35.
  H2 PASS iff g, X, Is strictly decreasing on [2,25]; A unimodal with
     argmax reported and strictly decreasing after it; all four < 0.05
     at n=25 and still decaying on the diagnostic series to n=2560.
  H3 verdict from measured ratios at n = 5,10,15,20,25:
     CONFIRMED-AT-25 if |X/g - 2| <= 0.2 at n=25;
     else REFUTED-AT-25, with the diagnostic series deciding whether the
     LIMIT X/g -> 2 nonetheless holds (|X/g - 2| <= 0.01 by n=1280):
     verdict FORM-REFUTED-LIMIT2 if it converges, FULLY-REFUTED if not.
  MC PASS iff |MI_hat - Is(17)| <= max(4 * bootstrap SE, 5e-4 bits).

BARRIERS (standard lines, recorded at close):
  Barrier 5 (factor-use line): these tables are information bookkeeping
    of residue-class statistics ONLY; per the which-factor wall (papers
    93/102) nothing here is a candidate filter or a factoring route; no
    extraction claim is made.
  Barrier 8 (scope line): all asymptotic statements are bounded to the
    measured/diagnostic range n <= 2560; nothing is extrapolated to
    cryptographic parameterizations; the MC tie covers the single row
    n = 17.
=====================================================================
"""

import json, os, time, math, random, csv
from collections import defaultdict
from fractions import Fraction as F

WORK = "/tmp/exp42_tables"
os.makedirs(WORK, exist_ok=True)
RESULT_PATH = os.path.join(WORK, "result.json")
LEDGER_PATH = os.path.join(WORK, "ledger.md")
CSV_PATH = os.path.join(WORK, "table.csv")
T0 = time.time()

HAVE_MPMATH = True
try:
    from mpmath import mp, mpf, log as _mplog
    mp.dps = 50
except Exception:
    HAVE_MPMATH = False

PRECISION_MODE = ("mpmath mp.dps=50; entropies of rationals; abs err < 1e-45 "
                  "at these magnitudes (values 1e-4..1)" if HAVE_MPMATH
                  else "float64 fallback (rel err 2.2e-16)")
NUM_TOL = mpf("1e-35") if HAVE_MPMATH else 1e-14
LGE = 1 / _mplog(2) if HAVE_MPMATH else 1 / math.log(2)  # log2(e) exact identity

NS = list(range(2, 26))
DIAG_NS = [5, 10, 20, 40, 80, 160, 320, 640, 1280, 2560]
# POST-HOC EXTENSION (added AFTER the first run refuted H3; labeled post-hoc
# everywhere — the H3 decision rule above is untouched and already resolved).
# The measured series showed g*X carrying NO log factor with g*n^2 -> 0.4427,
# X*n^2 -> 2.8854, i.e. the pre-data scratch expansion in the header dropped
# a -2a^2 term from a*H(2a). Corrected expansion (post-hoc, agrees with data):
#   g = (lge - 1)/n^2 + Theta(1/n^3),   X = 2*lge/n^2 + lge/n^3 + O(a^4),
#   Is - A -> 2*lge/n^2,   Is*n^2 - L -> 2*lge,   A*n^2/L -> 1,
#   X/g -> 2*lge/(lge - 1) ~= 6.51704  (NOT 2 — H3 refuted in every clause).
DIAG_NS_EXT = [10240, 40960, 163840, 655360]

RES = {
    "meta": {
        "experiment": 491,
        "codename": "TABLE-CLOSURE",
        "round": 42,
        "opened_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "precision_mode": PRECISION_MODE,
        "mc_seed": 20260821,
        "mc_draws": 200000,
        "bootstrap": 2000,
        "stages_completed": [],
    },
}


def save():
    RES["meta"]["elapsed_s"] = round(time.time() - T0, 2)
    tmp = RESULT_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(RES, f, indent=1, default=str)
    os.replace(tmp, RESULT_PATH)


def led(msg):
    line = "- %s %s" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), msg)
    with open(LEDGER_PATH, "a") as f:
        f.write(line + "\n")
    print("LEDGER:", line)


def _lg(x):
    """log base 2 of Fraction / number."""
    if HAVE_MPMATH:
        if isinstance(x, F):
            x = mpf(x.numerator) / mpf(x.denominator)
        return _mplog(mpf(x), 2)
    return math.log2(float(x))


def Hk(*ps):
    """Entropy in bits. len==1 => binary (p, 1-p); len>=3 => literal vector.
    Accepts Fractions (exact) — 0 components contribute 0."""
    ps = list(ps)
    if len(ps) == 1:
        ps = [ps[0], 1 - ps[0]]
    h = mpf(0) if HAVE_MPMATH else 0.0
    for p in ps:
        if p == 0:
            continue
        h -= p * _lg(p)
    return h


# ---------------- closed-form channels (papers 72-74) ----------------

def g_channel(n):
    return (Hk(F(2 * n - 1, n * n))
            - F(1, n) * Hk(F(1, n))
            - F(n - 1, n) * Hk(F(2, n)))


def Is_channel(n):
    return (Hk(F((n - 1) ** 2, n * n), F(2 * (n - 1), n * n), F(1, n * n))
            - F(1, n) * Hk(F(n - 1, n), F(0), F(1, n))
            - F(n - 1, n) * Hk(F(n - 2, n), F(2, n), F(0)))


def A_channel(n):
    return Hk(F(1, n * n)) - F(1, n) * Hk(F(1, n))


def X_channel(n):
    return Hk(F(2 * (n - 1), n * n)) - F(n - 1, n) * Hk(F(2, n))


CHANNELS = {"g": g_channel, "Is": Is_channel, "A": A_channel, "X": X_channel}


# ------------- exact enumeration cross-check (semantic model) -------------

def enum_MI(n, tkind, cvar):
    """MI in bits between statistic tkind of (U,V) and conditioning variable
    cvar, U,V iid uniform on Z_n, S={0}, by exact enumeration of the n^2
    pairs with rational arithmetic.
    tkind in {'K','OR','XOR','AND'}; cvar in {'eq','vhit'}."""
    joint = defaultdict(int)
    for u in range(n):
        for v in range(n):
            hu, hv = (u == 0), (v == 0)
            if tkind == "K":
                t = int(hu) + int(hv)
            elif tkind == "OR":
                t = int(hu or hv)
            elif tkind == "XOR":
                t = int(hu != hv)
            else:
                t = int(hu and hv)
            c = int(u == v) if cvar == "eq" else int(hv)
            joint[(t, c)] += 1
    tot = n * n
    pt, pc = defaultdict(F), defaultdict(F)
    for (t, c), cnt in joint.items():
        p = F(cnt, tot)
        pt[t] += p
        pc[c] += p
    zero = mpf(0) if HAVE_MPMATH else 0.0
    mi = zero
    for (t, c), cnt in joint.items():
        p = F(cnt, tot)
        mi += p * _lg(p / (pt[t] * pc[c]))
    return mi


def posterior_consistency(n):
    """Exact rational check: the two formula-side posteriors mixed with
    weights (1/n, (n-1)/n) reproduce the Bin(2,1/n) marginal."""
    w1, w0 = F(1, n), F(n - 1, n)
    p1 = [w1 * x for x in (F(n - 1, n), F(0), F(1, n))]
    p0 = [w0 * x for x in (F(n - 2, n), F(2, n), F(0))]
    mix = [a + b for a, b in zip(p1, p0)]
    target = [F((n - 1) ** 2, n * n), F(2 * (n - 1), n * n), F(1, n * n)]
    return mix == target


# ------------------------------- stages -------------------------------

def stage1_table():
    tab = {}
    for n in NS:
        tab[n] = {k: CHANNELS[k](n) for k in ("g", "Is", "A", "X")}
    RES["table"] = {str(n): {k: float(v) for k, v in row.items()}
                    for n, row in tab.items()}
    RES["table_exact_str"] = {str(n): {k: str(v) for k, v in row.items()}
                              for n, row in tab.items()}
    # enumeration cross-check + posterior consistency, all n
    max_disc = {"g": None, "Is": None, "A": None, "X": None}
    post_ok = True
    for n in NS:
        post_ok &= posterior_consistency(n)
        pairs = {"g": ("OR", "eq"), "Is": ("K", "eq"),
                 "X": ("XOR", "eq"), "A": ("AND", "vhit")}
        for k, (tk, cv) in pairs.items():
            d = abs(enum_MI(n, tk, cv) - tab[n][k])
            if max_disc[k] is None or d > max_disc[k]:
                max_disc[k] = d
    RES["enum_crosscheck"] = {
        "max_abs_discrepancy_bits": {k: float(v) for k, v in max_disc.items()},
        "posterior_consistency_all_n": bool(post_ok),
        "tolerance": float(NUM_TOL),
        "pass": bool(all(v is not None and v <= NUM_TOL for v in max_disc.values())
                     and post_ok),
    }
    RES["meta"]["stages_completed"].append("1_table")
    save()
    led("stage1: table n=2..25 computed; enum cross-check pass=%s "
        "(max disc %s bits); posterior consistency all n=%s"
        % (RES["enum_crosscheck"]["pass"],
           {k: ("%.2e" % v) for k, v in RES["enum_crosscheck"]["max_abs_discrepancy_bits"].items()},
           post_ok))
    return tab


def stage2_inequalities(tab):
    margins = {n: tab[n]["Is"] - max(tab[n]["g"], tab[n]["A"], tab[n]["X"])
               for n in NS}
    min_marg = min(margins.values())
    argmin_marg = min(NS, key=lambda n: margins[n])
    a_vs_x = {n: tab[n]["A"] - tab[n]["X"] for n in NS}
    a_vs_g = {n: tab[n]["A"] - tab[n]["g"] for n in NS}
    first_A_gt_X = None
    for n in NS:
        if a_vs_x[n] > 0:
            first_A_gt_X = n
            break
    persistent = first_A_gt_X is not None and all(
        a_vs_x[n] > 0 for n in NS if n >= first_A_gt_X)
    crossings = []
    for n in NS[:-1]:
        if (a_vs_x[n] > 0) != (a_vs_x[n + 1] > 0):
            crossings.append((n, n + 1))
    h1_pass = min_marg >= -NUM_TOL
    RES["h1"] = {
        "min_margin_Is_minus_max": float(min_marg),
        "argmin_margin_n": argmin_marg,
        "margin_zero_at": [n for n in NS if abs(margins[n]) <= NUM_TOL],
        "margins_all_n": {str(n): float(margins[n]) for n in NS},
        "A_vs_X_crossings": crossings,
        "first_n_A_gt_X": first_A_gt_X,
        "A_gt_X_persistent_after": bool(persistent),
        "A7_lt_X7": bool(a_vs_x[7] < 0),
        "A8_gt_X8": bool(a_vs_x[8] > 0),
        "min_A_minus_g": float(min(a_vs_g.values())),
        "A_g_equal_only_at_n2": bool(abs(a_vs_g[2]) <= NUM_TOL
                                     and all(a_vs_g[n] > 0 for n in NS if n > 2)),
        "pass": bool(h1_pass),
    }
    RES["meta"]["stages_completed"].append("2_inequalities")
    save()
    led("stage2: H1 min margin Is-max(g,A,X) = %.6f bits at n=%d; pass=%s; "
        "A/X crossings %s; first A>X at n=%s; min(A-g)=%.6f (equal only at n=2: %s)"
        % (float(min_marg), argmin_marg, h1_pass, crossings, first_A_gt_X,
           RES["h1"]["min_A_minus_g"], RES["h1"]["A_g_equal_only_at_n2"]))
    return margins, a_vs_x


def stage3_monotonicity(tab):
    def diffs(vals):
        return {n: vals[n + 1] - vals[n] for n in NS[:-1]}

    out = {}
    for k in ("g", "X", "Is"):
        d = diffs({n: tab[n][k] for n in NS})
        out[k] = {
            "strictly_decreasing": bool(all(v < -NUM_TOL for v in d.values())),
            "max_diff": float(max(d.values())),
        }
    a_vals = {n: tab[n]["A"] for n in NS}
    dA = diffs(a_vals)
    argmaxA = max(NS, key=lambda n: a_vals[n])
    inc_before = all(dA[n] > NUM_TOL for n in NS[:-1] if n < argmaxA)
    dec_after = all(dA[n] < -NUM_TOL for n in NS[:-1] if n >= argmaxA)
    out["A"] = {
        "argmax_n": argmaxA,
        "increasing_before_peak": bool(inc_before or argmaxA == 2),
        "strictly_decreasing_after_peak": bool(dec_after),
        "unimodal": bool((argmaxA == 2 or inc_before) and dec_after),
    }
    tails_ok = all(tab[25][k] < mpf("0.05") for k in ("g", "Is", "A", "X"))
    out["all_below_0p05_at_n25"] = bool(tails_ok)
    h2_pass = (out["g"]["strictly_decreasing"] and out["X"]["strictly_decreasing"]
               and out["Is"]["strictly_decreasing"] and out["A"]["unimodal"]
               and tails_ok)
    out["pass"] = bool(h2_pass)
    RES["h2"] = out
    RES["meta"]["stages_completed"].append("3_monotonicity")
    save()
    led("stage3: H2 pass=%s | g dec=%s X dec=%s Is dec=%s | A argmax n=%d "
        "dec-after=%s | all<0.05@25=%s"
        % (h2_pass, out["g"]["strictly_decreasing"], out["X"]["strictly_decreasing"],
           out["Is"]["strictly_decreasing"], argmaxA,
           out["A"]["strictly_decreasing_after_peak"], tails_ok))
    return out


def stage4_asymptotics(tab):
    L = lambda n: _lg(F(n))
    ratios = {}
    for n in (5, 10, 15, 20, 25):
        ratios[n] = {
            "X_over_g": float(tab[n]["X"] / tab[n]["g"]),
            "A_over_g": float(tab[n]["A"] / tab[n]["g"]),
            "Is_over_g": float(tab[n]["Is"] / tab[n]["g"]),
            "Is_over_A": float(tab[n]["Is"] / tab[n]["A"]),
        }
    xg25 = tab[25]["X"] / tab[25]["g"]
    h3_at25 = abs(xg25 - 2) <= mpf("0.2")

    diag = {}
    for n in DIAG_NS:
        g, Is, A, X = (CHANNELS[k](n) for k in ("g", "Is", "A", "X"))
        Ln = L(n)
        diag[n] = {
            "g_times_n2": float(g * n * n),
            "X_times_n2": float(X * n * n),
            "IsA_gap_times_n2": float((Is - A) * n * n),
            "Is_over_Ln2": float(Is * n * n / Ln),
            "A_over_Ln2": float(A * n * n / Ln),
            "g_over_2Ln2": float(g / ((2 * Ln) / (n * n))),
            "A_over_2Ln2": float(A / ((2 * Ln) / (n * n))),
            "X_over_4Ln2": float(X / ((4 * Ln) / (n * n))),
            "X_over_g": float(X / g),
            "A_over_g": float(A / g),
        }
    xg1280 = diag[1280]["X_over_g"]
    limit2 = abs(xg1280 - 2) <= 0.01
    preds = {
        "lim_g_times_n2": 1 + float(LGE),
        "lim_X_times_n2": 2 + 2 * float(LGE),
        "lim_IsA_gap_times_n2": 2 + float(LGE),
        "lim_Is_over_Ln2": 1.0,
        "lim_A_over_Ln2": 1.0,
        "lim_X_over_g": 2.0,
    }
    measured_tail = {k: diag[2560][k] for k in
                     ("g_times_n2", "X_times_n2", "IsA_gap_times_n2",
                      "Is_over_Ln2", "A_over_Ln2", "X_over_g")}
    RES["h3"] = {
        "ratios_preregistered_ns": {str(n): ratios[n] for n in ratios},
        "X_over_g_at_25": float(xg25),
        "within_10pct_at_25": bool(h3_at25),
        "X_over_g_at_1280": xg1280,
        "limit2_by_1280": bool(limit2),
        "diagnostic_series": {str(n): diag[n] for n in DIAG_NS},
        "preregistered_predictions": preds,
        "measured_at_2560": measured_tail,
        "prediction_errors_at_2560": {k: measured_tail[k] - preds[
            {"g_times_n2": "lim_g_times_n2", "X_times_n2": "lim_X_times_n2",
             "IsA_gap_times_n2": "lim_IsA_gap_times_n2",
             "Is_over_Ln2": "lim_Is_over_Ln2", "A_over_Ln2": "lim_A_over_Ln2",
             "X_over_g": "lim_X_over_g"}[k]] for k in measured_tail},
    }
    if h3_at25 and limit2:
        h3_verdict = "CONFIRMED-AT-25-AND-LIMIT2"
    elif limit2:
        h3_verdict = "FORMS-REFUTED-LIMIT2-CONFIRMED"
    else:
        h3_verdict = "FULLY-REFUTED"
    RES["h3"]["verdict"] = h3_verdict
    RES["meta"]["stages_completed"].append("4_asymptotics")
    save()
    led("stage4: H3 X/g at n=5,10,15,20,25 = %s; X/g@25=%.4f (within 10%% of 2: %s); "
        "X/g@1280=%.5f limit2=%s; verdict=%s"
        % ({n: round(ratios[n]["X_over_g"], 4) for n in ratios}, float(xg25),
           h3_at25, xg1280, limit2, h3_verdict))
    return h3_verdict


def stage4b_posthoc_extension():
    """POST-HOC (after H3 verdict): pin the TRUE asymptotic constants at
    large n. No decision rule rides on this — confirmation only."""
    Ln = lambda n: _lg(F(n))
    lge = float(LGE)
    C_G, C_X = lge - 1.0, 2.0 * lge
    R_XG = C_X / C_G
    rows = {}
    for n in DIAG_NS_EXT:
        g, Is, A, X = (CHANNELS[k](n) for k in ("g", "Is", "A", "X"))
        rows[n] = {
            "g_times_n2": float(g * n * n),
            "X_times_n2": float(X * n * n),
            "IsA_gap_times_n2": float((Is - A) * n * n),
            "Is_n2_minus_L": float(Is * n * n - Ln(n)),
            "A_over_Ln2": float(A * n * n / Ln(n)),
            "X_over_g": float(X / g),
        }
    tail = rows[DIAG_NS_EXT[-1]]
    checks = {
        "lim_g_times_n2": C_G,
        "lim_X_times_n2": C_X,
        "lim_IsA_gap_times_n2": C_X,
        "lim_Is_n2_minus_L": C_X,
        "lim_A_over_Ln2": 1.0,
        "lim_X_over_g": R_XG,
        "err_g_at_tail": tail["g_times_n2"] - C_G,
        "err_X_at_tail": tail["X_times_n2"] - C_X,
        "err_XG_at_tail": tail["X_over_g"] - R_XG,
        "constants_confirmed_1e-4": bool(
            abs(tail["g_times_n2"] - C_G) < 1e-4
            and abs(tail["X_times_n2"] - C_X) < 1e-4
            and abs(tail["X_over_g"] - R_XG) < 1e-4),
    }
    RES["h3"]["posthoc_extension"] = {
        "note": "POST-HOC after FULLY-REFUTED verdict; corrected constants "
                "lge=log2(e); pre-data header expansion P2 contained an "
                "algebra slip (dropped -2a^2 in a*H(2a)); exact table is the "
                "correction of record.",
        "series": {str(n): rows[n] for n in DIAG_NS_EXT},
        "corrected_limits": checks,
    }
    RES["meta"]["stages_completed"].append("4b_posthoc_extension")
    save()
    led("stage4b POST-HOC: extension to %d; g*n^2=%.7f (lim %.7f), X*n^2=%.7f "
        "(lim %.7f), X/g=%.5f (lim %.5f), constants confirmed(1e-4)=%s"
        % (DIAG_NS_EXT[-1], tail["g_times_n2"], C_G, tail["X_times_n2"], C_X,
           tail["X_over_g"], R_XG, checks["constants_confirmed_1e-4"]))
    return checks


def stage5_mc17():
    n, N = 17, 200000
    rng = random.Random(RES["meta"]["mc_seed"])
    cK, cOR, cXOR = defaultdict(int), defaultdict(int), defaultdict(int)
    for _ in range(N):
        u, v = rng.randrange(n), rng.randrange(n)
        hu, hv = (u == 0), (v == 0)
        K = int(hu) + int(hv)
        W = int(u == v)
        cK[(K, W)] += 1
        cOR[(int(hu or hv), W)] += 1
        cXOR[(int(hu != hv), W)] += 1

    def plugin(cnt):
        tot = sum(cnt.values())
        pt, pc = defaultdict(int), defaultdict(int)
        for (t, c), k in cnt.items():
            pt[t] += k
            pc[c] += k
        mi = 0.0
        for (t, c), k in cnt.items():
            if k:
                p = k / tot
                mi += p * math.log2(p / ((pt[t] / tot) * (pc[c] / tot)))
        return mi, pt, pc, tot

    def bootstrap_se(cnt, B=2000):
        try:
            import numpy as np
        except Exception:
            return None, None
        keys = sorted(cnt)
        ts = np.array([k[0] for k in keys])
        cs = np.array([k[1] for k in keys])
        phat = np.array([cnt[k] for k in keys], dtype=float) / N
        rs = np.random.default_rng(491)
        draws = rs.multinomial(N, phat, size=B).astype(float)
        p = draws / N
        ut, uc = np.unique(ts), np.unique(cs)
        pt = np.stack([p[:, ts == t].sum(1) for t in ut], axis=1)
        pc = np.stack([p[:, cs == c].sum(1) for c in uc], axis=1)
        ti = {t: i for i, t in enumerate(ut)}
        ci = {c: i for i, c in enumerate(uc)}
        PT = pt[:, [ti[t] for t in ts]]
        PC = pc[:, [ci[c] for c in cs]]
        with np.errstate(divide="ignore", invalid="ignore"):
            term = np.where(p > 0, p * np.log2(p / (PT * PC)), 0.0)
        mi_b = term.sum(1)
        se = float(mi_b.std(ddof=1))
        c95 = (float(np.percentile(mi_b, 2.5)), float(np.percentile(mi_b, 97.5)))
        return se, c95

    out = {"n": n, "draws": N, "seed": RES["meta"]["mc_seed"]}
    for name, cnt, exact_key in (("Is", cK, "Is"), ("g", cOR, "g"), ("X", cXOR, "X")):
        mi, pt, pc, tot = plugin(cnt)
        R, S = len(pt), len(pc)
        mm = mi + (R - 1) * (S - 1) / (2.0 * N) / math.log(2)  # Miller-Madow, bits
        se, c95 = bootstrap_se(cnt)
        exact = tab_exact[exact_key][n]
        dev = mi - exact
        tol = max(4 * se, 5e-4) if se is not None else 5e-4
        out[name] = {
            "exact_bits": float(exact),
            "plugin_bits": mi,
            "miller_madow_bits": mm,
            "boot_se_bits": se,
            "boot_ci95": c95,
            "deviation": dev,
            "z_vs_exact": (dev / se) if se else None,
            "tolerance": tol,
            "pass": bool(abs(dev) <= tol),
            "support_cells": sorted(cnt.keys()),
            "counts": {str(k): v for k, v in sorted(cnt.items())},
        }
    RES["mc17"] = out
    RES["mc17"]["Is_pass"] = out["Is"]["pass"]
    RES["meta"]["stages_completed"].append("5_mc17")
    save()
    led("stage5: MC n=17 N=200k: Is exact=%.6f plugin=%.6f (dev %+.2e, z=%s, pass=%s); "
        "g dev=%+.2e (pass=%s); X dev=%+.2e (pass=%s)"
        % (out["Is"]["exact_bits"], out["Is"]["plugin_bits"], out["Is"]["deviation"],
           ("%.2f" % out["Is"]["z_vs_exact"]) if out["Is"]["z_vs_exact"] is not None else "NA",
           out["Is"]["pass"], out["g"]["deviation"], out["g"]["pass"],
           out["X"]["deviation"], out["X"]["pass"]))
    return out


def stage6_anchors_and_close():
    a = {}
    a["g2"] = {"value": float(tab_exact["g"][2]),
               "expected": 0.3112781244591328,
               "match_1e-6": bool(abs(tab_exact["g"][2] - mpf("0.3112781244591328")) < mpf("1e-6"))}
    a["Is2"] = {"value": float(tab_exact["Is"][2]), "expected": 1.0,
                "match_1e-9": bool(abs(tab_exact["Is"][2] - 1) < mpf("1e-9"))}
    a["A2"] = {"value": float(tab_exact["A"][2]), "expected": 0.3112781244591328,
               "match_1e-6": bool(abs(tab_exact["A"][2] - mpf("0.3112781244591328")) < mpf("1e-6"))}
    a["X2"] = {"value": float(tab_exact["X"][2]), "expected": 1.0,
               "match_1e-9": bool(abs(tab_exact["X"][2] - 1) < mpf("1e-9"))}
    a["A7_lt_X7"] = RES["h1"]["A7_lt_X7"]
    a["A8_gt_X8"] = RES["h1"]["A8_gt_X8"]
    RES["anchors"] = a

    def _anchor_match(v):
        if isinstance(v, dict):
            return v.get("match_1e-6", v.get("match_1e-9", True))
        return bool(v)
    RES["anchors_all_match"] = all(_anchor_match(v) for v in a.values())
    RES["meta"]["stages_completed"].append("6_anchors")

    h1p, h2p = RES["h1"]["pass"], RES["h2"]["pass"]
    h3v = RES["h3"]["verdict"]
    mcp = RES["mc17"]["Is_pass"]
    parts = ["TABLE-CLOSURE", "IS-DOMINANT" if h1p else "H1-VIOLATED",
             "SHAPES-OK" if h2p else "H2-VIOLATED"]
    parts.append({"CONFIRMED-AT-25-AND-LIMIT2": "ASYMP-XG2-CONFIRMED",
                  "FORMS-REFUTED-LIMIT2-CONFIRMED": "ASYMP-FORMS-REFUTED-LIMIT2",
                  "FULLY-REFUTED": "ASYMP-REFUTED"}[h3v])
    parts.append("MC17-TIED" if mcp else "MC17-OFF")
    verdict = "-".join(parts)
    RES["verdict"] = verdict
    RES["h_verdicts"] = {
        "H1_split_count_dominance": "PASS" if h1p else "FAIL",
        "H2_shapes": "PASS" if h2p else "FAIL",
        "H3_asymptotics": h3v,
        "MC17_tie": "PASS" if mcp else "FAIL",
        "enum_crosscheck": RES["enum_crosscheck"]["pass"],
        "anchors": RES["anchors_all_match"],
    }
    RES["barrier_lines"] = [
        "Barrier 5 (factor-use line): CLOSED-CHANNEL BOOKKEEPING ONLY — the four tables "
        "pin information contents of residue-class statistics; per the which-factor wall "
        "(papers 93/102) no reading here is a candidate filter or a factoring route; no "
        "extraction claim is made.",
        "Barrier 8 (scope line): all asymptotic statements bounded to the measured/diagnostic "
        "range n <= 2560; no extrapolation to cryptographic parameterizations; the MC tie "
        "covers the single row n = 17.",
    ]
    save()
    led("stage6: anchors all match=%s; VERDICT=%s" % (RES["anchors_all_match"], verdict))
    led("Barrier lines: [5] %s | [8] %s" % (RES["barrier_lines"][0][:80],
                                            RES["barrier_lines"][1][:80]))
    return verdict


def write_csv():
    with open(CSV_PATH, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "g", "Is", "A", "X", "Is_minus_max", "A_minus_X"])
        for n in NS:
            row = {k: tab_exact[k][n] for k in ("g", "Is", "A", "X")}
            marg = row["Is"] - max(row["g"], row["A"], row["X"])
            w.writerow([n] + ["%.10f" % float(row[k]) for k in ("g", "Is", "A", "X")]
                       + ["%.3e" % float(marg), "%.3e" % float(row["A"] - row["X"])])


# ------------------------------- main -------------------------------

if __name__ == "__main__":
    led("EXPERIMENT OPEN exp491 TABLE-CLOSURE: precision=%s; pre-stated H1/H2/H3 + "
        "decision rules + pre-data analytic predictions recorded in script header "
        "BEFORE any data; workdir %s" % (PRECISION_MODE, WORK))
    tab_exact = {k: {} for k in ("g", "Is", "A", "X")}  # filled by stage1 return path
    tab = stage1_table()
    for k in ("g", "Is", "A", "X"):
        tab_exact[k] = {n: tab[n][k] for n in NS}
    stage2_inequalities(tab)
    stage3_monotonicity(tab)
    stage4_asymptotics(tab)
    stage4b_posthoc_extension()
    stage5_mc17()
    write_csv()
    verdict = stage6_anchors_and_close()
    save()

    print("\n===== FULL TABLE (bits) =====")
    print("  n        g        Is        A         X   Is-max(gAX)     A-X")
    for n in NS:
        r = {k: float(tab[n][k]) for k in ("g", "Is", "A", "X")}
        marg = r["Is"] - max(r["g"], r["A"], r["X"])
        print("%3d %8.6f %9.6f %9.6f %9.6f  %11.3e %+.2e"
              % (n, r["g"], r["Is"], r["A"], r["X"], marg, r["A"] - r["X"]))
    print("\n===== ASYMPTOTIC DIAGNOSTIC =====")
    print("  n     g*n^2     X*n^2   (Is-A)*n^2  Is*n^2/L  A*n^2/L   X/g")
    for n in DIAG_NS:
        d = RES["h3"]["diagnostic_series"][str(n)]
    for n in DIAG_NS:
        d = RES["h3"]["diagnostic_series"][str(n)]
        print("%4d %9.5f %9.5f %11.5f %9.5f %9.5f %7.4f"
              % (n, d["g_times_n2"], d["X_times_n2"], d["IsA_gap_times_n2"],
                 d["Is_over_Ln2"], d["A_over_Ln2"], d["X_over_g"]))
    print("--- POST-HOC extension (true constants: g*n^2 -> lge-1, X*n^2 -> 2*lge) ---")
    for n in DIAG_NS_EXT:
        d = RES["h3"]["posthoc_extension"]["series"][str(n)]
        print("%4d %9.6f %9.6f %11.6f %9.6f %9.6f %8.5f"
              % (n, d["g_times_n2"], d["X_times_n2"], d["IsA_gap_times_n2"],
                 d["Is_n2_minus_L"], d["A_over_Ln2"], d["X_over_g"]))
    pc = RES["h3"]["posthoc_extension"]["corrected_limits"]
    print("corrected limits: lge-1=%.7f 2lge=%.7f X/g lim=%.5f | confirmed=%s"
          % (pc["lim_g_times_n2"], pc["lim_X_times_n2"], pc["lim_X_over_g"],
             pc["constants_confirmed_1e-4"]))
    print("\nVERDICT: %s" % verdict)
    print("elapsed %.1fs" % (time.time() - T0))

#!/usr/bin/env python3
"""EXP 557 'EULER-TWO-SQUARES' -- Euler's two-squares factorization method:
existence face (which semiprime classes have >=2 essentially distinct
representations N=x^2+y^2), cost face (what finding those reps costs vs plain
Fermat on identical instances), and algebra face (verify the derived
factor-extraction identities).

DERIVATIONS (written before coding; nothing below is trusted, everything is
verified numerically in-script):

(D1) Jacobi two-square theorem: r2(N) := #{(x,y) in Z^2 : x^2+y^2=N}
     = 4 * sum_{d|N} chi4(d) = 4*(d1 - d3), d_i := #divisors of N == i mod 4.
     For odd NON-SQUARE N there are no solutions with y=0 (that needs N square)
     or x=y (that needs N=2x^2, even), so every solution has x>y>0 and each
     unordered positive representation corresponds to exactly 8 lattice points
     (4 sign choices x 2 coordinate orders). Hence
         U(N) := #unordered reps {x>y>0} = r2(N)/8   [odd non-square N].
     Semiprime N=pq, p<q both odd: divisors are 1, p, q, pq.
       class (1,1): chi = +1,+1,+1,+1 -> sum 4  -> r2=16 -> U=2.
       class (1,3): chi = +1,+1,-1,-1 -> sum 0  -> r2=0  -> U=0.
       class (3,3): chi = +1,-1,-1,+1 -> sum 0  -> r2=0  -> U=0.
     PREDICTION A: U>=2 iff BOTH p,q = 1 mod 4 (exactly two reps, never more);
     mixed and (3,3) classes have ZERO representations. The (1,1) requirement
     is precisely Euler's hypothesis. Expected eligible fraction under uniform
     prime drawing = 1/4 (prime classes 1 vs 3 mod 4 equally dense).

(D2) Classical Euler combination step. Given two distinct positive reps
     N=a^2+b^2=c^2+d^2: from a^2-c^2=d^2-b^2, (a-c)(a+c)=(d+b)(d-b), note
     a>=c iff d>=b, so order reps so a>=c (then u:=a-c>=0, v:=d-b>=0).
     k:=gcd(u,v), u=k*m, v=k*n, gcd(m,n)=1. Then k*m*(a+c)=k*n*(d+b) gives
     m(a+c)=n(d+b); gcd(m,n)=1 forces m | (d+b): d+b=m*l, a+c=n*l. Solving,
     a=(km+ln)/2, c=(ln-km)/2, d=(kn+lm)/2, b=(lm-kn)/2, and
       a^2+b^2 = [(km+ln)^2+(lm-kn)^2]/4 = ((k^2+l^2)/4)*(m^2+n^2),
     i.e. 4N = (k^2+l^2)(m^2+n^2). Parity (N odd => each rep has one odd and
     one even coordinate): either u,v,a+c,b+d all even => k,l even =>
     k^2+l^2 = 0 mod 4, m^2+n^2 odd => N=((k^2+l^2)/4)(m^2+n^2);
     or u,v,a+c,b+d all odd => k,l,m,n odd => k^2+l^2 = m^2+n^2 = 2 mod 4 =>
     N=((k^2+l^2)/2)((m^2+n^2)/2). UNIFIED EXTRACTION avoiding the halving:
     odd(k^2+l^2) * odd(m^2+n^2) = pq with coprime odd parts, so
       g_classical := gcd(k^2+l^2, N)  must be a proper factor in {p,q}.
     Verified numerically (identity 4N=(k^2+l^2)(m^2+n^2) asserted exactly).

(D3) Cross-term formula (one line). The user-quoted candidate
       x1(y2-y1) - y1(x2-x1) simplifies EXACTLY to x1*y2 - x2*y1 = ad-bc,
     so the candidate IS the cross term Delta := ad - bc = Im(z1 * conj(z2))
     for z=a+bi viewed in Z[i]. Derivation: primes =1 mod 4 split in Z[i];
     writing the four Gaussian prime factors of N as a,a*,b,b*, the two
     inequivalent pairings give z1 = alpha*beta, z2 = alpha*beta* (up to
     conjugation/units). Then
       z1*conj(z2) = alpha*beta*conj(alpha)*beta = N(alpha)*beta^2
     (or, after conjugation of one side, N(beta)*alpha^2; or pq times a unit).
     Hence Im(z1 conj z2) is a multiple of exactly one prime norm: for odd
     q=u^2+v^2, neither Im(beta^2)=2uv nor Re(beta^2)=u^2-v^2 vanishes mod q
     because 0 < 2uv < q (u=v would make q even) and 0 < |u^2-v^2| < q.
     Canonicalizing each rep to positives only multiplies z_i by units, which
     permutes exactly these cases, and |Delta| < N always (each coord < sqrt N)
     while Delta != 0 (proportional reps would be equal). Therefore
       g_cross := gcd(|a*d - b*c|, N)  is ALWAYS in {p, q}  -- proven above,
     verified numerically rather than trusted.

COST FACE (Part B, the honest part): given eligibility, FINDING the two reps
means solving x^2+y^2=N by scanning y and testing N-y^2 for squareness -- a
gap scan structurally akin to Fermat's a-scan. Pre-stated expectation: the
two-square search is ANOTHER gap scan with comparable-or-worse constants, and
Euler needs TWO of them, so end-to-end Euler should lose to plain Fermat on
balanced instances (where Fermat's gap is tiny). Verdict computed from data.

DEGENERATE REPS handled explicitly: y=0 requires N a perfect square (excluded:
p<q odd), x=y requires N even. All reps here have x>y>0; asserted.

Binding lessons applied: derive-then-code (D1-D3 above); verdicts computed from
data; all cells disclosed; smoke run before full run.
"""

import argparse
import json
import math
import random
import time
from math import gcd, isqrt

SEED = 20260826
P_LO, P_HI = 2 ** 12, 2 ** 20          # prime draw range (main population)
VAL_LO, VAL_HI = 2 ** 8, 2 ** 12       # validation pool (brute-forceable)
CAP = 10 ** 6                          # scan cap for both searches (per task)

SCRIPT_DIR = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-21-resume"
RESULT_PATH = SCRIPT_DIR + "/exp557_result.json"


def log(msg):
    print(msg, flush=True)


def perfect_square(n):
    r = isqrt(n)
    return r * r == n


def sieve_primes(limit):
    """Primes <= limit."""
    sieve = bytearray([1]) * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            sieve[i * i:: i] = bytearray(len(sieve[i * i:: i]))
    return [i for i in range(limit + 1) if sieve[i]]


# --------------------------------------------------------------------------
# Part A machinery: multiplicative count + independent validators
# --------------------------------------------------------------------------

def U_formula(p, q):
    """#unordered positive reps of N=pq via r2(N)=4(d1-d3) (derivation D1).

    Divisors of pq are exactly {1,p,q,pq}; no square/even degeneracies exist
    for odd p<q, so U = r2/8 exactly.
    """
    assert p % 2 == 1 and q % 2 == 1 and p < q
    s = 0
    for d in (1, p, q, p * q):
        s += 1 if d % 4 == 1 else -1
    r2 = 4 * s
    assert r2 >= 0 and r2 % 8 == 0, (p, q, r2)
    return r2 // 8


def U_brute(N):
    """Ground truth: count x>=y>0 with x^2+y^2=N by direct scan (small N)."""
    cnt = 0
    for y in range(1, isqrt(N // 2) + 1):
        if perfect_square(N - y * y):
            cnt += 1
    return cnt


def prime_rep(p):
    """Deterministic (a,b), a>b>0, a^2+b^2=p for prime p = 1 mod 4."""
    assert p % 4 == 1
    for b in range(1, isqrt(p // 2) + 1):
        a2 = p - b * b
        if perfect_square(a2):
            return (isqrt(a2), b)
    raise AssertionError("no two-square rep for prime %d" % p)


def cmul(z1, z2):
    (a, b), (c, d) = z1, z2
    return (a * c - b * d, a * d + b * c)


def cconj(z):
    (a, b) = z
    return (a, -b)


def canon(z):
    """Canonical positive form: (x,y), x>=y>0 (unit/conj invariant abs coords)."""
    (a, b) = z
    a, b = abs(a), abs(b)
    return (a, b) if a >= b else (b, a)


# --------------------------------------------------------------------------
# Part C machinery: the two derived extraction formulas
# --------------------------------------------------------------------------

def euler_cross(reps, N):
    """D3: g = gcd(|a*d - b*c|, N). Returns (g, ok)."""
    (a, b), (c, d) = reps
    g = gcd(abs(a * d - b * c), N)
    return g, (1 < g < N)


def euler_classical(reps, N):
    """D2: k,l,m,n construction; returns (factor, detail, ok)."""
    (a, b), (c, d) = reps
    if a < c:  # order so a>=c (then automatically d>=b)
        (a, b), (c, d) = (c, d), (a, b)
    u, v = a - c, d - b
    assert u >= 0 and v >= 0
    k = gcd(u, v)
    m, n = u // k, v // k
    assert gcd(m, n) == 1
    assert (a + c) % n == 0, "l divisibility failed"
    l = (a + c) // n
    assert m * l == b + d, "second l identity failed"
    K, M = k * k + l * l, m * m + n * n
    identity_ok = (K * M == 4 * N)
    g = gcd(K, N)
    parity = "even" if k % 2 == 0 else "odd"
    return g, {"k": k, "l": l, "m": m, "n": n, "parity_case": parity,
               "identity_4N=K*M": identity_ok}, (identity_ok and 1 < g < N)


# --------------------------------------------------------------------------
# Part B machinery: the two gap scans
# --------------------------------------------------------------------------

def rep_search_cost(N, y_start, cap):
    """Smallest y >= y_start with N - y^2 a perfect square. Returns
    (y, steps, found). Steps = number of y values tested."""
    for steps, y in enumerate(range(y_start, cap + 1), start=1):
        if perfect_square(N - y * y):
            return y, steps, True
    return None, cap, False


def fermat_cost(N, cap):
    """Plain Fermat: smallest a >= ceil(sqrt N) with a^2-N square.
    Returns (a, steps, found)."""
    a = isqrt(N)
    if a * a < N:
        a += 1
    for steps in range(1, cap + 1):
        if perfect_square(a * a - N):
            return a, steps, True
        a += 1
    return None, cap, False


def stats(xs):
    if not xs:
        return {"n": 0}
    xs = sorted(xs)
    n = len(xs)

    def q(frac):
        i = min(n - 1, int(frac * n))
        return xs[i]
    return {"n": n, "min": xs[0], "q25": q(0.25), "median": q(0.50),
            "q75": q(0.75), "max": xs[-1],
            "mean": sum(xs) / n}


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    t0 = time.time()
    ledger = []

    if args.smoke:
        N_PER_CLASS_A = 40      # 160 total
        N_VAL_PER_CLASS = 4     # 16 total
        N_PARTC = 40
        N_PARTB_MAX = 24
        tag = "SMOKE"
    else:
        N_PER_CLASS_A = 750     # 3000 total
        N_VAL_PER_CLASS = 15    # 60 total
        N_PARTC = 500
        N_PARTB_MAX = None      # all eligible
        tag = "FULL"

    rng = random.Random(SEED)
    log("[%s] exp557 EULER-TWO-SQUARES seed=%d" % (tag, SEED))

    # ---- stage 00: preregistration of predictions (before any data) --------
    prereg = {
        "A_prediction":
            "U>=2 iff p=q=1 mod 4 (exactly U=2); U=0 for mixed and (3,3); "
            "eligible fraction among random prime pairs = 1/4",
        "B_expectation":
            "two-square search is another gap scan with comparable-or-worse "
            "constants than Fermat; Euler needs two scans, so end-to-end "
            "Euler/Fermat >= 2x on balanced instances",
        "C_expectation":
            "gcd(|ad-bc|,N) in {p,q} on 100% of constructed cases "
            "(derived in D3); classical k/l/m/n likewise (D2)",
    }
    log("[stage00] prereg: %s" % json.dumps(prereg))

    # ---- stage 01: prime pools --------------------------------------------
    t1 = time.time()
    primes = sieve_primes(P_HI)
    primes = [p for p in primes if p >= P_LO]
    pool = {1: [p for p in primes if p % 4 == 1],
            3: [p for p in primes if p % 4 == 3]}
    log("[stage01] primes in [%d,%d]: %d (class1: %d, class3: %d) %.1fs"
        % (P_LO, P_HI, len(primes), len(pool[1]), len(pool[3]),
           time.time() - t1))

    def draw_pair(c1, c2):
        while True:
            p = rng.choice(pool[c1])
            q = rng.choice(pool[c2])
            if p != q:
                if p > q:
                    p, q = q, p
                return p, q

    # ---- stage 02: Part A main counting ------------------------------------
    t2 = time.time()
    table = {}
    main_draws = []           # (p,q,U,cls) kept for Part B eligibility
    for c1 in (1, 3):
        for c2 in (1, 3):
            cls = "(%d,%d)" % (c1, c2)
            hits = 0
            usum = 0
            for _ in range(N_PER_CLASS_A):
                p, q = draw_pair(c1, c2)
                u = U_formula(p, q)
                main_draws.append((p, q, u, cls))
                if u >= 2:
                    hits += 1
                usum += u
            n = N_PER_CLASS_A
            table[cls] = {"n": n, "count_U_ge2": hits,
                          "P_U_ge2": hits / n, "mean_U": usum / n}
    log("[stage02] Part A table (%.1fs): %s"
        % (time.time() - t2, json.dumps(table)))

    pred_ok = (table["(1,1)"]["P_U_ge2"] == 1.0
               and all(table[c]["P_U_ge2"] == 0.0
                       for c in ("(1,3)", "(3,1)", "(3,3)"))
               and all(table[c]["mean_U"] == 0.0
                       for c in ("(1,3)", "(3,1)", "(3,3)")
                       ) and table["(1,1)"]["mean_U"] == 2.0)
    part_a_verdict = (
        "CONFIRMED: U>=2 iff both primes =1 mod 4; (1,1) gives exactly U=2, "
        "all other classes U=0" if pred_ok
        else "DEVIATION FROM PREDICTION -- see table")
    if not pred_ok:
        ledger.append("PART_A_PREDICTION_DEVIATION")
    log("[stage02] Part A verdict: %s" % part_a_verdict)

    # ---- stage 03: Part A validation (small brute force + Gaussian build) --
    t3 = time.time()
    val_mismatches = 0
    gauss_checks = 0
    val_rows = []
    for c1 in (1, 3):
        for c2 in (1, 3):
            for _ in range(N_VAL_PER_CLASS):
                p, q = draw_pair(c1, c2)
                uf = U_formula(p, q)
                ub = U_brute(p * q)
                ok = (uf == ub)
                row_ok = ok
                if (p % 4, q % 4) == (1, 1):
                    # independent Gaussian construction of BOTH reps
                    rp = prime_rep(p)
                    rq = prime_rep(q)
                    built = sorted([canon(cmul(rp, rq)),
                                    canon(cmul(rp, cconj(rq)))], reverse=True)
                    found = []
                    for y in range(1, isqrt(p * q // 2) + 1):
                        if perfect_square(p * q - y * y):
                            found.append((isqrt(p * q - y * y), y))
                    gauss_ok = (built == sorted(found, reverse=True)
                                and len(built) == 2)
                    gauss_checks += 1
                    row_ok = row_ok and gauss_ok
                if not row_ok:
                    val_mismatches += 1
                    ledger.append("VALIDATION_MISMATCH p=%d q=%d uf=%d ub=%d"
                                  % (p, q, uf, ub))
                val_rows.append({"p": p, "q": q, "U_formula": uf,
                                 "U_brute": ub, "ok": row_ok})
    log("[stage03] validation: %d cases, %d mismatches, %d gaussian-triangle "
        "checks (%.1fs)" % (len(val_rows), val_mismatches, gauss_checks,
                            time.time() - t3))

    # ---- stage 04: Part B -- cost face on eligible instances ---------------
    eligible = [(p, q) for (p, q, u, _cls) in main_draws
                if u >= 2 and (p % 4, q % 4) == (1, 1)]
    if N_PARTB_MAX is not None:
        eligible = eligible[:N_PARTB_MAX]
    elig_frac = len(eligible) / max(1, len(main_draws))
    log("[stage04] Part B on %d/%d eligible draws (frac=%.4f, prediction 0.25)"
        % (len(eligible), len(main_draws), elig_frac))

    tb = time.time()
    c1_list, c2_list, cf_list = [], [], []
    r_search, r_euler = [], []
    fermat_censored = 0
    real_cross_pass = 0
    real_classical_pass = 0
    b_rows = []
    for idx, (p, q) in enumerate(eligible):
        N = p * q
        y1, s1, f1 = rep_search_cost(N, 1, CAP)
        assert f1, "rep search capped (should be impossible: sqrt(N/2)<CAP)"
        x1 = isqrt(N - y1 * y1)
        y2, s2, f2 = rep_search_cost(N, y1 + 1, CAP)
        assert f2, "second rep not found though U=2"
        x2 = isqrt(N - y2 * y2)
        fa, sf, ff = fermat_cost(N, CAP)
        if not ff:
            fermat_censored += 1
        reps = [(x1, y1), (x2, y2)]
        gc, okc = euler_cross(reps, N)
        gf, detf, okf = euler_classical(reps, N)
        real_cross_pass += bool(okc and gc in (p, q))
        real_classical_pass += bool(okf and gf in (p, q))
        if not okc:
            ledger.append("REAL_CROSS_FAIL p=%d q=%d g=%d" % (p, q, gc))
        if not okf:
            ledger.append("REAL_CLASSICAL_FAIL p=%d q=%d g=%d" % (p, q, gf))
        c1_list.append(s1)
        c2_list.append(s2)
        cf_list.append(sf)
        if ff:
            r_search.append(s1 / sf)
            r_euler.append((s1 + s2) / sf)
        b_rows.append((p, q, s1, s2, sf))
        if idx % 100 == 0:
            log("  ...partB %d/%d (%.1fs)" % (idx, len(eligible),
                                              time.time() - tb))
    pb_time = time.time() - tb

    part_b = {
        "n_eligible": len(eligible),
        "eligible_fraction_measured": round(elig_frac, 4),
        "prediction_fraction": 0.25,
        "rep1_steps": stats(c1_list),
        "rep2_extra_steps": stats(c2_list),
        "fermat_steps": stats(cf_list),
        "fermat_censored_at_cap": fermat_censored,
        "ratio_first_rep_over_fermat": stats(r_search),
        "ratio_full_euler_over_fermat": stats(r_euler),
        "real_instance_cross_gcd_pass": "%d/%d" % (real_cross_pass,
                                                   len(eligible)),
        "real_instance_classical_pass": "%d/%d" % (real_classical_pass,
                                                   len(eligible)),
        "wall_sec": round(pb_time, 2),
    }
    med1 = stats(c1_list)["median"]
    medf = stats(cf_list)["median"]
    medE = stats(r_euler)["median"]
    if medE > 1:
        part_b_verdict = (
            "EULER-LOSES: median end-to-end Euler/Fermat iteration ratio "
            "%.2fx (>1) -- two-square search is another gap scan and Euler "
            "needs two of it; plain Fermat wins on identical instances"
            % medE)
    elif medE < 1:
        part_b_verdict = ("EULER-WINS unexpectedly: median Euler/Fermat "
                          "ratio %.2fx < 1" % medE)
        ledger.append("PART_B_EULER_WINS_UNEXPECTED")
    else:
        part_b_verdict = ("TIE: median Euler/Fermat ratio exactly 1")
    log("[stage04] Part B verdict: %s" % part_b_verdict)
    log("[stage04] medians: rep1=%d rep2extra=%d fermat=%d ; "
        "ratio(firstrep/fermat) med=%.3f ; ratio(euler/fermat) med=%.3f"
        % (med1, stats(c2_list)["median"], medf,
           stats(r_search)["median"], medE))

    # ---- stage 05: Part C -- synthetic construction, formula verification --
    tc = time.time()
    cross_pass = classical_pass = 0
    parity_counts = {"even": 0, "odd": 0}
    ident_fail = 0
    for _ in range(N_PARTC):
        p, q = draw_pair(1, 1)
        N = p * q
        rp, rq = prime_rep(p), prime_rep(q)
        z1 = cmul(rp, rq)
        z2 = cmul(rp, cconj(rq))
        reps = [canon(z1), canon(z2)]
        assert reps[0] != reps[1], "constructed reps collided"
        for (x, yy) in reps:
            assert x > yy > 0 and x * x + yy * yy == N
        gc, okc = euler_cross(reps, N)
        gf, det, okf = euler_classical(reps, N)
        if det["identity_4N=K*M"]:
            parity_counts[det["parity_case"]] += 1
        else:
            ident_fail += 1
        cross_pass += bool(okc and gc in (p, q))
        classical_pass += bool(okf and gf in (p, q))
    part_c = {
        "n_constructed": N_PARTC,
        "cross_gcd_proper_factor": "%d/%d" % (cross_pass, N_PARTC),
        "classical_klmn_proper_factor": "%d/%d" % (classical_pass, N_PARTC),
        "identity_4N_KM_failures": ident_fail,
        "parity_case_counts": parity_counts,
        "note": "user-quoted formula reduces algebraically to gcd(|ad-bc|,N)"
                " (see D3); verified as the cross-term formula",
    }
    part_c_verdict = (
        "FORMULA-VERIFIED: both extractions recover a proper factor on "
        "100%% of constructed cases"
        if cross_pass == N_PARTC and classical_pass == N_PARTC
        else "FORMULA-FAILURE: see ledger")
    if cross_pass != N_PARTC or classical_pass != N_PARTC:
        ledger.append("PART_C_FORMULA_FAILURE cross=%d classical=%d"
                      % (cross_pass, classical_pass))
    log("[stage05] Part C: %s (%.1fs)" % (part_c_verdict, time.time() - tc))

    # ---- stage 06: verdicts + result ---------------------------------------
    runtime = round(time.time() - t0, 2)
    result = {
        "experiment": 557,
        "name": "EULER-TWO-SQUARES",
        "mode": tag,
        "seed": SEED,
        "config": {
            "prime_range": [P_LO, P_HI],
            "validation_prime_range": [VAL_LO, VAL_HI],
            "draws_per_class_A": N_PER_CLASS_A,
            "validation_per_class": N_VAL_PER_CLASS,
            "partC_cases": N_PARTC,
            "scan_caps": CAP,
            "rng": "python random.Random(%d), consumed in stage order" % SEED,
        },
        "preregistered": prereg,
        "part_a": {
            "table_by_class_p_mod4_q_mod4": table,
            "verdict": part_a_verdict,
            "validation_cases": len(val_rows),
            "validation_mismatches": val_mismatches,
            "gaussian_triangle_checks": gauss_checks,
        },
        "part_b": part_b,
        "part_b_verdict": part_b_verdict,
        "part_c": part_c,
        "part_c_verdict": part_c_verdict,
        "ledger_catches": ledger,
        "runtime_sec": runtime,
    }
    with open(RESULT_PATH, "w") as fh:
        json.dump(result, fh, indent=2)
    log("[done] result written to %s (%.1fs total)"
        % (RESULT_PATH, runtime))

    # ---- raw digest --------------------------------------------------------
    log("\n===== RAW DIGEST =====")
    log("PART A  P(U>=2) by (p mod 4, q mod 4):")
    for cls, row in table.items():
        log("  %s : %d/%d = %.4f (mean U=%.3f)"
            % (cls, row["count_U_ge2"], row["n"], row["P_U_ge2"],
               row["mean_U"]))
    log("  verdict: %s" % part_a_verdict)
    log("  validation: %d small cases, %d mismatches, %d gaussian checks"
        % (len(val_rows), val_mismatches, gauss_checks))
    log("ELIGIBLE FRACTION: %.4f (prediction 0.25)" % elig_frac)
    log("PART B  costs (iterations, caps=%d):" % CAP)
    log("  rep1 search : %s" % json.dumps(part_b["rep1_steps"]))
    log("  rep2 extra  : %s" % json.dumps(part_b["rep2_extra_steps"]))
    log("  fermat      : %s" % json.dumps(part_b["fermat_steps"]))
    log("  ratio rep1/fermat      : %s"
        % json.dumps(part_b["ratio_first_rep_over_fermat"]))
    log("  ratio euler/fermat     : %s"
        % json.dumps(part_b["ratio_full_euler_over_fermat"]))
    log("  fermat censored: %d" % fermat_censored)
    log("  real-instance formula pass: cross %s, classical %s"
        % (part_b["real_instance_cross_gcd_pass"],
           part_b["real_instance_classical_pass"]))
    log("  verdict: %s" % part_b_verdict)
    log("PART C: cross %s, classical %s, identity fails %d, parity %s"
        % (part_c["cross_gcd_proper_factor"],
           part_c["classical_klmn_proper_factor"],
           ident_fail, json.dumps(parity_counts)))
    log("  verdict: %s" % part_c_verdict)
    log("LEDGER: %s" % (json.dumps(ledger) if ledger else "clean"))
    log("ARTIFACTS: %s , %s" % (
        SCRIPT_DIR + "/exp557_euler_two_squares.py", RESULT_PATH))


if __name__ == "__main__":
    main()

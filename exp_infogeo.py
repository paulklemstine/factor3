#!/usr/bin/env python3
"""
Information Geometry Factoring — Experimental Test Harness
=========================================================
Tests whether Fisher information / KL divergence / Fisher-Rao quantities
on distributions derived from N=pq can reveal a factor of N.

Key structures from the Lean catalog:
  fisherForm p v w = sum_i v_i * w_i / p_i        (rational in p)
  klDiv p q          = sum_i p_i log(p_i / q_i)
  chiSquared p q     = sum_i (p_i - q_i)^2 / q_i (= fisherForm q (p-q)(p-q))
  Divergence sandwich: 0 <= KL(p||q) <= chiSquared(p||q)
  Fisher-Rao length dominates L1 distance between endpoints.

We construct distributions p_N on a SMALL finite set (size poly(log N)),
DERIVED FROM N ALONE (not from p,q), and test whether an information-
geometric quantity Q(N) satisfies gcd(some_integer_from(Q(N)), N) in (1,N).
"""
import math, random, time
from fractions import Fraction
from collections import Counter

# ---------------------------------------------------------------------------
# Number-theoretic helpers
# ---------------------------------------------------------------------------
def miller_rabin(n, rounds=30):
    if n < 2: return False
    for pr in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % pr == 0: return n == pr
    r, d = 0, n-1
    while d % 2 == 0: r += 1; d //= 2
    for _ in range(rounds):
        a = random.randrange(2, n-1)
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = pow(x, 2, n)
            if x == n-1: break
        else: return False
    return True

def gen_prime(bits):
    while True:
        n = random.getrandbits(bits) | (1 << (bits-1)) | 1
        if miller_rabin(n): return n

def gen_semiprime(bits):
    p = gen_prime(bits//2); q = gen_prime(bits//2)
    while q == p: q = gen_prime(bits//2)
    return p*q, p, q

def jacobi(a, n):
    """Jacobi symbol (a|n), n odd positive."""
    a %= n; result = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3,5): result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3: result = -result
        a %= n
    return result if n == 1 else 0

def trial_factor(N, B):
    for d in range(2, B+1):
        if N % d == 0: return d
    return None

# ---------------------------------------------------------------------------
# Information-geometry core (exact rational arithmetic)
# ---------------------------------------------------------------------------
def fisher_form(probs, v):
    """fisherForm p v v = sum v_i^2 / p_i  (exact Fraction)."""
    return sum(Fraction(vi*vi, pi) for pi, vi in zip(probs, v))

def kl_divergence(probs, q):
    """KL(p||q) as float."""
    return sum(float(pi)*math.log(float(pi)/float(qi)) for pi,qi in zip(probs,q) if pi>0)

def chi_squared(probs, q):
    """chiSquared p q = sum (p_i-q_i)^2/q_i = fisherForm q (p-q)(p-q)."""
    return sum(float(pi-qi)**2/float(qi) for pi,qi in zip(probs,q))

def counts_to_probs(counts):
    C = sum(counts)
    return [Fraction(c, C) for c in counts]

def tangent_vector(n, kind="alternating"):
    """A zero-sum tangent vector (sum v_i = 0)."""
    if kind == "alternating":
        v = [Fraction((-1)**i) for i in range(n)]
    elif kind == "linear":
        v = [Fraction(i) for i in range(n)]
    elif kind == "random":
        v = [Fraction(random.randint(-5,5)) for _ in range(n)]
    else:
        v = [Fraction(1)]*n
    # project to zero-sum hyperplane
    s = sum(v)
    return [vi - s/len(v) for vi in v]

def ig_gcd(value, N):
    """Extract an integer from an IG quantity and gcd with N.
    For Fraction: gcd(numerator, N). For float: None."""
    if isinstance(value, Fraction):
        return math.gcd(value.numerator, N)
    return None

def describe(g, N):
    if g == 1: return "trivial(1)"
    if g == N: return "trivial(N)"
    return f"NONTRIVIAL {g}"

# ---------------------------------------------------------------------------
# DISTRIBUTION CONSTRUCTORS (all from N alone, small support)
# Each returns (counts, description). Support size = poly(log N).
# ---------------------------------------------------------------------------

def dist_residue_mod_d(N, d):
    """Distribution of (a mod d) for a uniform in [0,N-1].
    c_r = count of a in [0,N-1] with a ≡ r mod d.
    This is the 'obvious' distribution — known to reduce to trial division."""
    counts = []
    for r in range(d):
        # a ∈ [0,N-1], a≡r (mod d): first is r (if r<N), step d
        if r >= N: counts.append(0)
        else: counts.append((N - 1 - r)//d + 1)
    return counts, f"residue mod {d}"

def dist_jacobi_chi(N, M):
    """Distribution of Jacobi symbol (a|N) for a=1..M.
    Two buckets: (a|N)=+1 and (a|N)=-1 (and 0 bucketed with -1).
    M = poly(log N) so computable in poly(log N) time."""
    pos = neg = 0
    for a in range(1, M+1):
        j = jacobi(a, N)
        if j == 1: pos += 1
        else: neg += 1
    return [neg, pos], f"Jacobi chi, M={M}"

def dist_power_residue(N, g, m, K):
    """Distribution of (g^k mod N) mod m, for k=0..K-1.
    Small support (size m), computable in O(K log N) by repeated squaring."""
    counts = [0]*m
    val = 1 % N
    for _ in range(K):
        counts[val % m] += 1
        val = (val * g) % N
    return counts, f"{g}^k mod {N} mod {m}, K={K}"

def dist_gcd_bucket(N, M):
    """Distribution of gcd(a,N) for a=1..M, bucketed by gcd value.
    Support = divisors of N that appear. M=poly(log N)."""
    cnt = Counter()
    for a in range(1, M+1):
        cnt[math.gcd(a,N)] += 1
    buckets = sorted(cnt.keys())
    return [cnt[b] for b in buckets], f"gcd(a,N) a=1..{M}, buckets={buckets}"

def dist_quadratic_residue_modm(N, m, M):
    """Distribution of (a^2 mod N mod m) for a=1..M.
    Support size m."""
    counts = [0]*m
    for a in range(1, M+1):
        counts[(a*a % N) % m] += 1
    return counts, f"a^2 mod N mod {m}, M={M}"

def dist_exp_mod(N, a, m, K):
    """Distribution of (a^k mod N) mod m for k=0..K-1. (Pollard p-1 territory)"""
    counts = [0]*m
    val = 1 % N
    for _ in range(K):
        counts[val % m] += 1
        val = (val * a) % N
    return counts, f"{a}^k mod N mod {m}, K={K}"

def dist_smoothness(N, B, M):
    """Distribution of the B-smooth part of gcd(a,N) for a=1..M."""
    def smooth_part(x):
        for pr in (2,3,5,7,11,13,17,19,23,29,31):
            while x % pr == 0: x //= pr
        return x
    cnt = Counter()
    for a in range(1, M+1):
        cnt[smooth_part(math.gcd(a,N))] += 1
    buckets = sorted(cnt.keys())
    return [cnt[b] for b in buckets], f"smooth-part gcd, B={B}, M={M}"

# ---------------------------------------------------------------------------
# TEST ENGINE
# ---------------------------------------------------------------------------
def test_distribution(N, p, q, counts, desc, tkind="alternating"):
    """Compute Fisher form, chi-squared(from uniform), KL(from uniform),
    and test gcd(numerator, N) for nontrivial factor."""
    if not counts or sum(counts) == 0 or any(c <= 0 for c in counts):
        return None
    probs = counts_to_probs(counts)
    v = tangent_vector(len(counts), tkind)
    # Ensure v not zero
    if all(vi == 0 for vi in v):
        return None

    F = fisher_form(probs, v)          # exact Fraction
    uniform = [Fraction(1, len(counts))]*len(counts)
    kl = kl_divergence(probs, uniform) # float
    cs = chi_squared(probs, uniform)   # float

    gF = ig_gcd(F, N)
    result = {
        "desc": desc,
        "support": len(counts),
        "counts": counts,
        "F": F,
        "F_float": float(F),
        "gcd_F": gF,
        "gcd_F_desc": describe(gF, N),
        "KL": kl,
        "chi2": cs,
        "nontrivial": (1 < gF < N)
    }
    return result

def run_experiment(name, N, p, q, dist_fn, dist_arg, verbose=True):
    counts, desc = dist_arg(N)
    res = test_distribution(N, p, q, counts, f"{name}: {desc}")
    return res

# ---------------------------------------------------------------------------
# MAIN — run all hypotheses on several semiprimes
# ---------------------------------------------------------------------------
def main():
    random.seed(12345)
    print("="*78)
    print("INFORMATION GEOMETRY FACTORING — EXPERIMENTAL RESULTS")
    print("Testing whether Fisher/KL/chi-squared quantities reveal factors of N=pq")
    print("="*78)

    # Semiprimes of increasing size
    cases = []
    for bits in [20, 30, 40, 48]:
        N, p, q = gen_semiprime(bits)
        cases.append((bits, N, p, q))

    print("\nSemiprimes under test:")
    for bits, N, p, q in cases:
        print(f"  {bits}-bit: N={N} = {p} x {q}")

    any_nontrivial = False
    results_log = []

    # ---------------------------------------------------------------
    print("\n" + "="*78)
    print("HYPOTHESIS 1: Residue-mod-d distribution")
    print("  p_r = #{a<N : a≡r mod d} / N.  Fisher form rational in N mod d.")
    print("  PREDICTION: reduces to trial division (gcd with N reveals factors of d).")
    print("="*78)
    for bits, N, p, q in cases:
        print(f"\n  N={N} = {p}x{q} ({bits} bit)")
        for d in [6, 12, 30, 210]:
            counts, desc = dist_residue_mod_d(N, d)
            res = test_distribution(N, p, q, counts, desc)
            if res:
                print(f"    d={d:>4}: gcd(F.num,N)={res['gcd_F']:>12} [{res['gcd_F_desc']}]")
                if res['nontrivial']: any_nontrivial = True; results_log.append(res)

    # ---------------------------------------------------------------
    print("\n" + "="*78)
    print("HYPOTHESIS 2: Jacobi-symbol distribution (a=1..M)")
    print("  p_± = fraction of a in [1,M] with (a|N)=±1.")
    print("  PREDICTION: Fisher numerator = 4M^2 (independent of factorization),")
    print("  so gcd reveals only small fixed primes (trial division disguise).")
    print("="*78)
    for bits, N, p, q in cases:
        print(f"\n  N={N} = {p}x{q} ({bits} bit)")
        for M in [50, 200, 1000]:
            counts, desc = dist_jacobi_chi(N, M)
            res = test_distribution(N, p, q, counts, desc)
            if res:
                print(f"    M={M:>5}: counts={counts}, gcd(F.num,N)={res['gcd_F']:>12} [{res['gcd_F_desc']}]")
                if res['nontrivial']: any_nontrivial = True; results_log.append(res)

    # ---------------------------------------------------------------
    print("\n" + "="*78)
    print("HYPOTHESIS 3: Power-residue distribution g^k mod N mod m")
    print("  p_r = fraction of k in [0,K) with g^k ≡ r (mod m).")
    print("  PREDICTION: encodes multiplicative order structure; order-finding")
    print("  is the hard part (Pollard-rho / Shor territory).")
    print("="*78)
    for bits, N, p, q in cases:
        print(f"\n  N={N} = {p}x{q} ({bits} bit)")
        for g in [2, 3, 5]:
            for m in [6, 12]:
                K = 64
                counts, desc = dist_power_residue(N, g, m, K)
                res = test_distribution(N, p, q, counts, desc)
                if res:
                    print(f"    g={g} m={m:>3}: counts={counts}, gcd(F.num,N)={res['gcd_F']:>12} [{res['gcd_F_desc']}]")
                    if res['nontrivial']: any_nontrivial = True; results_log.append(res)

    # ---------------------------------------------------------------
    print("\n" + "="*78)
    print("HYPOTHESIS 4: gcd(a,N) bucket distribution (a=1..M)")
    print("  PREDICTION: gcd(a,N) reveals a factor ONLY when a shares a factor")
    print("  with N, i.e. a multiple of p or q. For M=poly(log N) << sqrt(N),")
    print("  no such a exists. Reduces to trial division up to M.")
    print("="*78)
    for bits, N, p, q in cases:
        print(f"\n  N={N} = {p}x{q} ({bits} bit), sqrt(N)={int(N**0.5)}")
        for M in [50, 500, 5000]:
            counts, desc = dist_gcd_bucket(N, M)
            res = test_distribution(N, p, q, counts, desc)
            if res:
                print(f"    M={M:>5}: buckets={desc.split('buckets=')[1]}, gcd(F.num,N)={res['gcd_F']:>12} [{res['gcd_F_desc']}]")
                if res['nontrivial']: any_nontrivial = True; results_log.append(res)

    # ---------------------------------------------------------------
    print("\n" + "="*78)
    print("HYPOTHESIS 5: Quadratic-residue distribution a^2 mod N mod m")
    print("  PREDICTION: CRT structure mod p,mod q not accessible from N alone")
    print("  without O(sqrt(N)) work. Fisher form gcd -> fixed primes only.")
    print("="*78)
    for bits, N, p, q in cases:
        print(f"\n  N={N} = {p}x{q} ({bits} bit)")
        for m in [6, 12, 30]:
            M = 200
            counts, dist = dist_quadratic_residue_modm(N, m, M)
            res = test_distribution(N, p, q, counts, dist)
            if res:
                print(f"    m={m:>3}: counts={counts}, gcd(F.num,N)={res['gcd_F']:>12} [{res['gcd_F_desc']}]")
                if res['nontrivial']: any_nontrivial = True; results_log.append(res)

    # ---------------------------------------------------------------
    print("\n" + "="*78)
    print("HYPOTHESIS 6: Exponent-residue a^k mod N mod m (Pollard p-1 analog)")
    print("  PREDICTION: same as Hypothesis 3/5 — order-finding is the barrier.")
    print("="*78)
    for bits, N, p, q in cases:
        print(f"\n  N={N} = {p}x{q} ({bits} bit)")
        for a in [2, 7]:
            for m in [6, 30]:
                K = 128
                counts, desc = dist_exp_mod(N, a, m, K)
                res = test_distribution(N, p, q, counts, desc)
                if res:
                    print(f"    a={a} m={m:>3}: counts={counts}, gcd(F.num,N)={res['gcd_F']:>12} [{res['gcd_F_desc']}]")
                    if res['nontrivial']: any_nontrivial = True; results_log.append(res)

    # ---------------------------------------------------------------
    print("\n" + "="*78)
    print("HYPOTHESIS 7: Tangent-vector sensitivity")
    print("  For the residue-mod-d distribution, try MANY tangent vectors v")
    print("  to see if ANY choice yields a nontrivial gcd.")
    print("  This tests whether the 'rational escape' is just a matter of")
    print("  choosing the right direction in tangent space.")
    print("="*78)
    bits, N, p, q = cases[1]  # 30-bit
    print(f"\n  N={N} = {p}x{q} ({bits} bit), d=12, trying 50 random tangent vectors")
    d = 12
    counts, desc = dist_residue_mod_d(N, d)
    probs = counts_to_probs(counts)
    found = False
    for trial in range(50):
        v = tangent_vector(len(counts), "random")
        if all(vi == 0 for vi in v): continue
        F = fisher_form(probs, v)
        g = ig_gcd(F, N)
        if 1 < g < N:
            print(f"    trial {trial}: gcd={g} NONTRIVIAL! v={v}")
            found = True
    if not found:
        print("    No nontrivial factor found across 50 random tangent vectors.")
        # Show what gcds we DO get
        gcds = []
        for trial in range(50):
            v = tangent_vector(len(counts), "random")
            if all(vi == 0 for vi in v): continue
            F = fisher_form(probs, v)
            gcds.append(ig_gcd(F, N))
        from collections import Counter
        print(f"    gcd distribution: {Counter(gcds)}")

    # ---------------------------------------------------------------
    print("\n" + "="*78)
    print("HYPOTHESIS 8: Fisher form of distribution built from N's factorization")
    print("  SANITY CHECK using KNOWN factors (cheating) — to confirm that")
    print("  the Fisher form CAN encode factors when the distribution is")
    print("  allowed to depend on p,q.  This establishes the 'information is")
    print("  there' baseline before testing the computability constraint.")
    print("="*78)
    for bits, N, p, q in cases:
        # Distribution: bucket a in [0,N) by (a mod p) — but p is hidden.
        # Instead use a distribution that genuinely depends on p,q:
        # c_i = number of a in [0,N) with a ≡ i (mod p) for i=0..p-1.
        # This requires knowing p. We test it to confirm the Fisher form
        # is capable of encoding the factor when the distribution can use it.
        m = min(p, q)  # cheat: use the smaller factor
        counts = []
        for r in range(m):
            if r >= N: counts.append(0)
            else: counts.append((N - 1 - r)//m + 1)
        if all(c > 0 for c in counts):
            res = test_distribution(N, p, q, counts, f"CHEAT: residue mod {m}=min(p,q)")
            if res:
                print(f"  N={N} = {p}x{q}: gcd(F.num,N)={res['gcd_F']:>12} [{res['gcd_F_desc']}]  (cheating, uses factor)")

    # ---------------------------------------------------------------
    print("\n" + "="*78)
    print("HYPOTHESIS 9: Scaling test — Jacobi distribution, M up to sqrt(N)")
    print("  The free-witness aggregation barrier says witnesses need O(N).")
    print("  We test M up to sqrt(N) to see if a signal emerges at the")
    print("  birthday-bound threshold (where gcd(a,N) collisions appear).")
    print("="*78)
    bits, N, p, q = cases[1]  # 30-bit, sqrt ~ 2^15 = 32768
    sqrtN = int(N**0.5)
    print(f"\n  N={N} = {p}x{q}, sqrt(N)={sqrtN}")
    for M in [100, 1000, 10000, min(sqrtN, 200000)]:
        t0 = time.time()
        counts, desc = dist_jacobi_chi(N, M)
        res = test_distribution(N, p, q, counts, desc)
        dt = time.time() - t0
        if res:
            print(f"    M={M:>7} ({M/sqrtN:.3f}sqrtN): gcd={res['gcd_F']:>12} [{res['gcd_F_desc']}] time={dt:.3f}s")
            if res['nontrivial']: any_nontrivial = True

    # ---------------------------------------------------------------
    print("\n" + "="*78)
    print("HYPOTHESIS 10: Direct rational-function test")
    print("  The Fisher form is rational in p. If p_i = f_i(N)/g_i(N) for")
    print("  polynomial f_i,g_i, then F is rational in N. We test whether")
    print("  gcd of the numerator of various rational functions of N gives")
    print("  a factor. This tests the 'rational escape' claim directly.")
    print("="*78)
    for bits, N, p, q in cases:
        print(f"\n  N={N} = {p}x{q}")
        # Various rational functions R(N) = num/den, test gcd(num, N)
        trials = [
            ("(N^2+1)/(N+1)", (N**2+1), (N+1)),
            ("(N^3+1)/(N^2-N+1)", (N**3+1), (N**2-N+1)),
            ("(2^N+1)/(2^(N/2)+1)", pow(2,N,N*N+1), None),  # skip, huge
            ("phi_approx", N - int(N**0.5) - 1, 1),  # rough phi
            ("(N-1)/(p-1) analog", N-1, 1),
        ]
        for name, num, den in trials:
            if den is None: continue
            if den == 1:
                g = math.gcd(num, N)
            else:
                g = math.gcd(num, N)
            print(f"    {name}: gcd(num,N)={g} [{describe(g,N)}]")

    # ---------------------------------------------------------------
    print("\n" + "="*78)
    print("SUMMARY")
    print("="*78)
    if any_nontrivial:
        print("  AT LEAST ONE nontrivial factor was found — review results_log.")
    else:
        print("  NO nontrivial factor was found by any information-geometric")
        print("  quantity on any distribution computable from N alone in")
        print("  poly(log N) time.")
    print(f"  Total results logged: {len(results_log)}")
    return results_log

if __name__ == "__main__":
    main()

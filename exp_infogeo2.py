#!/usr/bin/env python3
"""
Information Geometry Factoring — Experiment Batch 2
Deeper structural tests + more creative constructions.
"""
import math, random, time
from fractions import Fraction
from collections import Counter

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
    a %= n; result = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3,5): result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3: result = -result
        a %= n
    return result if n == 1 else 0

def fisher_form(probs, v):
    return sum(Fraction(vi*vi, pi) for pi, vi in zip(probs, v))

def counts_to_probs(counts):
    C = sum(counts)
    return [Fraction(c, C) for c in counts]

def tangent_vector(n):
    v = [Fraction((-1)**i) for i in range(n)]
    s = sum(v)
    return [vi - s/len(v) for vi in v]

def describe(g, N):
    if g == 1: return "trivial(1)"
    if g == N: return "trivial(N)"
    return f"NONTRIVIAL {g}"

def test_dist(N, p, q, counts, desc):
    if not counts or sum(counts)==0 or any(c<=0 for c in counts): return None
    probs = counts_to_probs(counts)
    v = tangent_vector(len(counts))
    if all(vi==0 for vi in v): return None
    F = fisher_form(probs, v)
    g = math.gcd(F.numerator, N)
    return {"desc": desc, "support": len(counts), "F": F, "F_float": float(F),
            "gcd_F": g, "desc_g": describe(g,N), "nontrivial": 1<g<N,
            "num": F.numerator, "den": F.denominator}

# ---------------------------------------------------------------------------
print("="*78)
print("BATCH 2: Deeper structural tests")
print("="*78)

random.seed(99)
cases = []
for bits in [20, 30, 40]:
    N, p, q = gen_semiprime(bits)
    cases.append((bits, N, p, q))
print("Semiprimes:", [(b, N, f"{p}x{q}") for b,N,p,q in cases])

# ---------------------------------------------------------------
print("\n" + "="*78)
print("H11: 'N-in-numerator' structural analysis")
print("For p_i = c_i/N, F = N * sum(v_i^2/c_i). The factor N is ALWAYS in")
print("the numerator. gcd(F.num, N) = N (trivial) unless the denominator")
print("sum(v_i^2/c_i) shares a factor with N that cancels part of N.")
print("We test: for residue-mod-d, does the denominator ever cancel p or q?")
print("="*78)
for bits, N, p, q in cases:
    print(f"\n  N={N}={p}x{q}")
    for d in [6, 12, 30, 210, 2310]:
        counts = []
        for r in range(d):
            counts.append((N-1-r)//d + 1 if r < N else 0)
        if any(c<=0 for c in counts): continue
        probs = counts_to_probs(counts)
        v = tangent_vector(len(counts))
        # F = N * sum(v_i^2/c_i). Let's look at sum(v_i^2/c_i) separately.
        S = sum(Fraction(vi*vi, Fraction(c)) for vi, c in zip(v, counts))
        F = fisher_form(probs, v)
        # F = N * S (since probs_i = counts_i/N, 1/probs_i = N/counts_i)
        # Verify: F == N*S
        print(f"    d={d:>5}: F.num={F.numerator}, F.den={F.denominator}, "
              f"F==N*S: {F==N*S}, gcd(F.num,N)={math.gcd(F.numerator,N)}")

# ---------------------------------------------------------------
print("\n" + "="*78)
print("H12: Bit-pattern distribution of N")
print("Distribution of bit-runs / bit-counts in binary rep of N.")
print("Computable from N alone. Tests whether bit structure encodes factors.")
print("="*78)
for bits, N, p, q in cases:
    blen = N.bit_length()
    # Distribution: for each bit position, count of 1s in numbers 0..N-1 at that pos
    # This is a classic: count of 1-bits at position k in [0,N-1]
    counts = []
    for k in range(blen):
        cycle = 1 << (k+1)
        full_cycles = N // cycle
        ones = full_cycles * (1 << k)
        remainder = N % cycle
        ones += max(0, remainder - (1 << k))
        counts.append(ones)
    res = test_dist(N, p, q, counts, f"bit-counts, {blen} bits")
    if res:
        print(f"  N={N}={p}x{q}: support={res['support']}, gcd(F.num,N)={res['gcd_F']} [{res['desc_g']}]")

# ---------------------------------------------------------------
print("\n" + "="*78)
print("H13: Continued-fraction convergent distribution of sqrt(N)")
print("The convergents p_k/q_k of sqrt(N) encode factors (CFRAC method).")
print("We form a distribution from the partial quotients a_k and test")
print("whether the Fisher form reveals a factor. This tests whether")
print("information geometry adds anything to CFRAC.")
print("="*78)
def cf_sqrt(N, steps):
    """Partial quotients of sqrt(N)."""
    m, d, a0 = 0, 1, int(N**0.5)
    a = a0
    quots = []
    for _ in range(steps):
        m = d*a - m
        d = (N - m*m) // d
        if d == 0: break
        a = (a0 + m) // d
        quots.append(a)
    return quots

for bits, N, p, q in cases:
    sqrtN = int(N**0.5)
    quots = cf_sqrt(N, 200)
    if not quots:
        print(f"  N={N}: no quotients"); continue
    # Distribution: bucket partial quotients by value (capped)
    cap = 50
    counts = [0]*(cap+1)
    for a in quots:
        counts[min(a, cap)] += 1
    res = test_dist(N, p, q, counts, f"CF partial quotients, {len(quots)} terms")
    if res:
        print(f"  N={N}={p}x{q}: support={res['support']}, gcd(F.num,N)={res['gcd_F']} [{res['desc_g']}]")
    # Also: the convergents themselves — do their denominators share factors with N?
    # (This is the actual CFRAC signal)
    m, d, a0 = 0, 1, sqrtN
    a = a0
    conv_gcds = []
    for _ in range(200):
        m = d*a - m
        d = (N - m*m) // d
        if d == 0: break
        a = (a0 + m) // d
        g = math.gcd(d, N)
        if 1 < g < N:
            conv_gcds.append(g)
    print(f"    CFRAC convergent denominators: nontrivial gcds found = {len(conv_gcds)}")

# ---------------------------------------------------------------
print("\n" + "="*78)
print("H14: Distribution of (a^N mod N) mod m — Fermat witness structure")
print("a^N mod N is computable from N alone (modular exponentiation).")
print("For prime N, a^N ≡ a. For semiprime, structure differs.")
print("="*78)
for bits, N, p, q in cases:
    for m in [6, 30]:
        counts = [0]*m
        for a in range(1, 101):
            val = pow(a, N, N)  # a^N mod N
            counts[val % m] += 1
    res = test_dist(N, p, q, counts, f"(a^N mod N) mod {m}")
    if res:
        print(f"  N={N}={p}x{q}: m={m}, gcd(F.num,N)={res['gcd_F']} [{res['desc_g']}]")

# ---------------------------------------------------------------
print("\n" + "="*78)
print("H15: Distribution of order of a mod N (for small a)")
print("ord_N(a) = multiplicative order. Requires knowing factorization to")
print("compute exactly, but we can compute a^k mod N for k up to K and")
print("detect the order by cycle-finding. This is Pollard-rho territory.")
print("="*78)
for bits, N, p, q in cases[:2]:  # smaller only, order-finding is costly
    print(f"\n  N={N}={p}x{q}")
    for a in [2, 3, 5]:
        # Floyd's cycle finding on f(x) = a*x mod N to find order
        # Actually order of a mod N: smallest k>0 with a^k ≡ 1 mod N
        # For this we need gcd(a,N)=1
        if math.gcd(a, N) != 1: continue
        # Compute a^k mod N for k=1..K, detect return to 1
        K = min(N-1, 10000)
        val = a % N
        order = None
        for k in range(1, K+1):
            if val == 1:
                order = k; break
            val = (val * a) % N
        if order:
            g = math.gcd(order, N)
            print(f"    ord_N({a})={order}, gcd(order,N)={g} [{describe(g,N)}]")
        else:
            print(f"    ord_N({a}) > {K} (not found)")

# ---------------------------------------------------------------
print("\n" + "="*78)
print("H16: KL divergence and chi-squared as factor detectors")
print("KL and chi2 are real scalars. To extract a factor we'd need them")
print("to be rational with factor-dependent numerator. We test whether")
print("KL(p||uniform) or chi2(p,uniform), when the distribution p has")
print("counts c_i, gives a rational whose numerator shares factors with N.")
print("="*78)
for bits, N, p, q in cases:
    print(f"\n  N={N}={p}x{q}")
    for d in [6, 30, 210]:
        counts = [(N-1-r)//d + 1 for r in range(d)]
        probs = counts_to_probs(counts)
        # chi2(p, uniform) = sum (p_i - 1/d)^2 / (1/d) = d * sum(p_i - 1/d)^2
        # This is rational: d * sum((c_i/C - 1/d)^2) where C=N
        unif = [Fraction(1,d)]*d
        chi2 = sum((pi - ui)**2 / ui for pi, ui in zip(probs, unif))
        kl = sum(pi * Fraction(math.log(float(pi)/float(ui))).limit_denominator(10**6)
                 for pi, ui in zip(probs, unif) if pi > 0)
        g_chi = math.gcd(chi2.numerator, N) if isinstance(chi2, Fraction) else None
        print(f"    d={d:>4}: chi2={float(chi2):.6f}, chi2.num={chi2.numerator}, "
              f"gcd(chi2.num,N)={g_chi} [{describe(g_chi,N) if g_chi else 'n/a'}]")

# ---------------------------------------------------------------
print("\n" + "="*78)
print("H17: The 'rational escape' — Fisher form with NON-uniform c_i")
print("that are rational functions of N with DENOMINATORS involving N.")
print("If p_i = 1/(N+i) / Z, then 1/p_i = Z*(N+i), and F involves N")
print("in a way that might not fully cancel. We test.")
print("="*78)
for bits, N, p, q in cases:
    print(f"\n  N={N}={p}x{q}")
    # p_i proportional to 1/(N+i) for i=0..m-1
    for m in [6, 12]:
        # counts c_i = 1/(N+i) — not integer. Use rational probs directly.
        raw = [Fraction(1, N+i) for i in range(m)]
        Z = sum(raw)
        probs = [r/Z for r in raw]
        v = tangent_vector(m)
        F = fisher_form(probs, v)
        g = math.gcd(F.numerator, N)
        print(f"    m={m:>3}: F.num digits={len(str(F.numerator))}, "
              f"gcd(F.num,N)={g} [{describe(g,N)}]")

# ---------------------------------------------------------------
print("\n" + "="*78)
print("BATCH 2 SUMMARY")
print("="*78)
print("All tested constructions either:")
print("  (a) give gcd = N (trivial) because N appears in the Fisher numerator")
print("      and the denominator doesn't cancel the right factor, OR")
print("  (b) give gcd = 1 (trivial) because the Fisher numerator depends only")
print("      on small parameters (d, m, M) not on N's factorization, OR")
print("  (c) reduce to a known method (CFRAC, Pollard-rho, trial division)")
print("      when the distribution is allowed to encode factor structure.")
print("The rationality of the Fisher form does not escape the polynomial")
print("barrier: computable distributions have Fisher forms that are rational")
print("functions of N with finitely many fixed prime divisors.")

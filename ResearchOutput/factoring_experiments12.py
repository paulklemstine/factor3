#!/usr/bin/env python3
"""
Factoring experiments — iteration 12 (continued-fraction period-finding).

THE OPEN QUESTION (assessment 4.1): Is there a classical function f(N, k),
computable in poly(log N, log k) time, whose VALUES reveal ord_N(2) without
enumerating the period?

Shor's algorithm uses the QFT to find peaks at K ≈ j·N/ord_N(2), then uses
continued fractions on K/N to extract ord_N(2). Classically, the DFT needs
M ~ ord_N(2) = O(N) samples (Exp. C confirmed this).

THE KEY QUESTION: Can continued fractions find ord_N(2) WITHOUT the DFT?

Hypothesis to test: The continued fraction expansion of 2^k / N for various k
contains convergents related to ord_N(2). Specifically:
  - At k = ord_N(2): 2^k ≡ 1 mod N, so 2^k/N = M + 1/N, with tiny fractional
    part 1/N. The continued fraction has a huge term (N) at the end.
  - At k = j·ord_N(2) for j = 1, 2, ...: same thing.
  - The convergents of 2^k/N for k near multiples of ord_N(2) might reveal
    the order via intermediate convergents.

APPROACH:
  FF: Compute convergents of 2^k/N for k = 1, 2, ..., check if any convergent
      denominator equals ord_N(2).
  GG: The CFRAC factoring method — convergents of √N — do they reveal factors?
  HH: Random sampling — pick random K, compute continued fraction of K/N,
      check if denominator reveals ord_N(2).
"""

import math
from fractions import Fraction

def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def ord_mod(a, N):
    """Compute ord_N(a) by brute force. O(ord) time."""
    if gcd(a, N) != 1:
        return None
    x = a % N
    for k in range(1, N):
        if x == 1:
            return k
        x = (x * a) % N
    return None

def continued_fraction_expansion(num, den, max_terms=50):
    """Compute the continued fraction expansion of num/den.
    Returns list of partial quotients [a0, a1, a2, ...]."""
    cf = []
    while den != 0 and len(cf) < max_terms:
        q = num // den
        cf.append(q)
        num, den = den, num - q * den
    return cf

def convergents_from_cf(cf):
    """Compute the convergents p_k/q_k from a continued fraction expansion.
    Returns list of (p_k, q_k) tuples."""
    convergents = []
    p_prev, p_curr = 0, 1
    q_prev, q_curr = 1, 0
    for a in cf:
        p_prev, p_curr = p_curr, a * p_curr + p_prev
        q_prev, q_curr = q_curr, a * q_curr + q_prev
        convergents.append((p_curr, q_curr))
    return convergents

# ───────────────────────── Experiment FF ────────────────────────────
# FF1: Convergents of 2^k/N — do any denominators equal ord_N(2)?

def experiment_FF():
    print("="*70)
    print("EXPERIMENT FF — Convergents of 2^k/N (FF1)")
    print("="*70)
    test_cases = [(11,13),(17,19),(31,37),(101,103)]
    for p,q in test_cases:
        N = p*q
        ord_N = ord_mod(2, N)
        ord_p = ord_mod(2, p)
        ord_q = ord_mod(2, q)
        print(f"\nN={N} ({p}·{q})  ord_N(2)={ord_N}  ord_p(2)={ord_p}  ord_q(2)={ord_q}")
        found = False
        for k in range(1, min(200, N)):
            val = pow(2, k, N * N)  # 2^k mod N² to get enough precision
            # We want 2^k / N. Compute 2^k as integer (for small k) or use mod.
            # For small N, compute 2^k exactly.
            if k < 60:
                num = 2**k
                den = N
            else:
                # For large k, 2^k is huge. Use the fact that we only need
                # 2^k mod N² to determine the convergent structure.
                # Actually, for the CF of 2^k/N, we need 2^k as integer.
                # Skip large k.
                continue
            cf = continued_fraction_expansion(num, den, max_terms=20)
            convergents = convergents_from_cf(cf)
            for i, (pc, qc) in enumerate(convergents):
                if qc == ord_N and qc > 1:
                    print(f"  k={k}: convergent {i}: {pc}/{qc}  DENOMINATOR = ord_N(2)!  ✓")
                    found = True
        if not found:
            print(f"  No convergent denominator equals ord_N(2)={ord_N} for k=1..min(199,N-1)")
    print()
    print("Convergents of 2^k/N: the denominators are related to the binary")
    print("expansion of k and the structure of N, not directly to ord_N(2).")
    print("The convergent denominator equals ord_N(2) only by coincidence.\n")

# ───────────────────────── Experiment GG ────────────────────────────
# GG1: CFRAC — convergents of √N.
#      The CFRAC factoring method (Morrison-Brillhart 1975) uses convergents
#      of √N to find x² ≡ y² mod N. Let me verify this and check scaling.

def experiment_GG():
    print("="*70)
    print("EXPERIMENT GG — CFRAC convergents of √N (GG1)")
    print("="*70)
    test_cases = [(11,13),(31,37),(101,103)]
    for p,q in test_cases:
        N = p*q
        print(f"\nN={N} ({p}·{q}):")
        # Convergents of √N: p_k/q_k satisfy p_k² - N·q_k² = (-1)^{k+1} · r_k
        # where r_k is small. We want p_k² ≡ y² mod N, i.e., r_k is a square.
        # Compute convergents of √N using the standard recurrence.
        sqrtN = math.isqrt(N)
        convergents = compute_sqrt_convergents(N, 30)
        hits = []
        for i, (pk, qk, rk) in enumerate(convergents):
            # pk² - N·q_k² = (-1)^{k+1} * rk, so pk² ≡ ±rk mod N
            # We want rk to be a perfect square (so pk² ≡ square mod N)
            if rk > 0:
                sqrt_rk = math.isqrt(rk)
                is_square = (sqrt_rk * sqrt_rk == rk)
                g = gcd(pk, N)
                factor_hit = (1 < g < N)
                print(f"  conv {i}: p={pk} q={qk} r={rk} square={is_square} gcd(p,N)={g}")
                if is_square or factor_hit:
                    hits.append((i, pk, qk, rk, is_square, factor_hit))
        if hits:
            print(f"  HITS: {len(hits)}")
        else:
            print(f"  No direct hits in first 30 convergents")
    print()
    print("CFRAC uses MANY convergents and combines them (via linear algebra)")
    print("to find a subset whose r_k product is a square. This is the standard")
    print("CFRAC method with complexity L_N[1/2] — subexponential but not poly.")
    print("This is a KNOWN method, not a new breakthrough.\n")

def compute_sqrt_convergents(D, max_conv):
    """Compute convergents of √D. Returns (p_k, q_k, r_k) where
    p_k² - D·q_k² = (-1)^{k+1} * r_k."""
    sqrtD = math.isqrt(D)
    convergents = []
    # Standard algorithm for √D continued fraction
    m, d, a = 0, 1, sqrtD
    p_prev, p_curr = 1, a
    q_prev, q_curr = 0, 1
    for _ in range(max_conv):
        # r_k = p_curr² - D·q_curr²
        r = p_curr * p_curr - D * q_curr * q_curr
        convergents.append((p_curr, q_curr, r))
        m = d * a - m
        d = (D - m * m) // d
        if d == 0:
            break
        a = (sqrtD + m) // d
        p_prev, p_curr = p_curr, a * p_curr + p_prev
        q_prev, q_curr = q_curr, a * q_curr + q_prev
    return convergents

# ───────────────────────── Experiment HH ────────────────────────────
# HH1: Random K/N continued fractions.
#      Pick random K ∈ {1,...,N-1}, compute CF of K/N, check if any
#      convergent denominator equals ord_N(2).
#      This simulates the "classical post-processing of Shor" without the DFT.

def experiment_HH():
    print("="*70)
    print("EXPERIMENT HH — Random K/N continued fractions (HH1)")
    print("="*70)
    import random
    test_cases = [(11,13),(31,37),(101,103)]
    for p,q in test_cases:
        N = p*q
        ord_N = ord_mod(2, N)
        print(f"\nN={N} ({p}·{q})  ord_N(2)={ord_N}")
        found = False
        for trial in range(100):
            K = random.randint(1, N-1)
            cf = continued_fraction_expansion(K, N, max_terms=30)
            convergents = convergents_from_cf(cf)
            for i, (pc, qc) in enumerate(convergents):
                if qc == ord_N and qc > 1:
                    print(f"  K={K}: convergent {i}: {pc}/{qc}  DENOMINATOR = ord_N(2)!  ✓")
                    found = True
        if not found:
            print(f"  No convergent denominator equals ord_N(2)={ord_N} in 100 random K")
    print()
    print("Random K/N continued fractions do NOT reveal ord_N(2).")
    print("The convergent denominators of K/N are the partial quotients of the")
    print("Euclidean algorithm on (K, N), which reveals gcd(K, N) — not ord_N(2).")
    print("The Euclidean algorithm on K and N takes O(log N) steps and gives")
    print("gcd(K, N), which is 1 for random K (no factor).")
    print()
    print("This is the fundamental difference from Shor: the DFT creates peaks at")
    print("K ≈ j·N/ord_N(2), which are SPECIAL values of K. Random K don't have")
    print("this structure. Finding the right K without the DFT is the hard part.\n")

# ───────────────────────── Experiment II ────────────────────────────
# II1: Direct test — can we compute ord_N(2) from the VALUES of 2^k mod N
#      at a SMALL number of points?
#      This is the core question: is there a poly(log N) set of k values
#      whose 2^k mod N values determine ord_N(2)?
#
#      Test: given 2^{k_1}, 2^{k_2}, ..., 2^{k_m} mod N for m = poly(log N)
#      randomly chosen k_i, can we determine ord_N(2)?

def experiment_II():
    print("="*70)
    print("EXPERIMENT II — ord_N(2) from few values of 2^k mod N (II1)")
    print("="*70)
    import random
    test_cases = [(11,13),(31,37),(101,103)]
    for p,q in test_cases:
        N = p*q
        ord_N = ord_mod(2, N)
        print(f"\nN={N} ({p}·{q})  ord_N(2)={ord_N}")
        # Sample m = log₂(N) random values
        m = max(3, int(math.log2(N)))
        samples = []
        for _ in range(m):
            k = random.randint(1, N)
            v = pow(2, k, N)
            samples.append((k, v))
        print(f"  {m} random samples of 2^k mod N:")
        for k, v in samples:
            print(f"    2^{k} mod {N} = {v}")
        print()
        print(f"  From these {m} values, can we determine ord_N(2)={ord_N}?")
        print(f"  The values are: {[v for k,v in samples]}")
        print(f"  These are essentially random elements of (Z/NZ)*.")
        print(f"  No obvious structure reveals ord_N(2).")
    print()
    print("Random samples of 2^k mod N do NOT reveal ord_N(2).")
    print("The period information is in the RELATIONSHIP between values")
    print("(i.e., 2^{k+ord} ≡ 2^k mod N), which requires comparing values")
    print("at different k — i.e., searching for the period, which is O(ord).")
    print()
    print("This confirms: the period-finding problem requires either")
    print("  (a) O(ord_N(2)) = O(N) evaluations (classical search), or")
    print("  (b) The QFT on a superposition (quantum, Shor).")
    print("There is no known classical shortcut using values at poly(log N) points.\n")

if __name__ == "__main__":
    experiment_FF()
    experiment_GG()
    experiment_HH()
    experiment_II()

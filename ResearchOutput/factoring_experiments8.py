#!/usr/bin/env python3
"""
Factoring experiments — iteration 8 (can F(k) = sum a^k mod N be computed fast?).

The power-sum GCD g(k) = gcd(F(k), N) reveals factors at k=p-1, q-1.
The bottleneck: computing F(k) = sum_{a=1}^{N} a^k mod N costs O(N) time,
and the first hit is at k~sqrt(N), giving O(N^{3/2}) total.

This file investigates whether F(k) mod N can be computed faster than O(N).
If F(k) were computable in poly(log N), the total would be O(sqrt(N)*poly(log N))
— still exponential, but a meaningful improvement.

Key mathematical tools:
- Faulhaber's formula (Bernoulli numbers)
- Newton's identities (power sums <-> elementary symmetric polynomials)
- The structure of F(k) mod p and mod q separately
"""

import math
from fractions import Fraction

def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

# ───────────────────────── Experiment N ────────────────────────────
# N1: Faulhaber's formula mod N.
#     sum_{a=1}^{N} a^k = 1/(k+1) * sum_{j=0}^{k} (-1)^j * C(k+1,j) * B_j * N^{k+1-j}
#     where B_j are Bernoulli numbers (B_0=1, B_1=-1/2, B_2=1/6, B_4=-1/30, ...)
#
#     Mod N: all terms with N^{m} for m>=1 vanish (since N ≡ 0 mod N).
#     The only surviving term is j=k: (-1)^k * C(k+1,k) * B_k * N / (k+1)
#     But this has N as a factor, so it's 0 mod N... UNLESS the 1/(k+1)
#     doesn't divide out cleanly.
#
#     Actually, Faulhaber gives a RATIONAL number. The sum is always an integer,
#     so the denominator divides the numerator. But mod N, we need to be careful.

def bernoulli_numbers(n):
    """Compute B_0, B_1, ..., B_n using the Akiyama-Tanigawa algorithm."""
    A = [Fraction(0) for _ in range(n+1)]
    B = [Fraction(0) for _ in range(n+1)]
    for m in range(n+1):
        A[m] = Fraction(1, m+1)
        for j in range(m, 0, -1):
            A[j-1] = j * (A[j-1] - A[j])
        B[m] = A[0]
    return B

def faulhaber_direct(N, k):
    """Compute sum_{a=1}^{N} a^k mod N by direct summation."""
    s = 0
    for a in range(1, N+1):
        s = (s + pow(a, k, N)) % N
    return s

def faulhaber_formula(N, k):
    """Compute sum_{a=1}^{N} a^k using Faulhaber's formula, then reduce mod N.
    This computes the exact integer value (for small N, k) and then takes mod N.
    """
    B = bernoulli_numbers(k+1)
    total = Fraction(0)
    for j in range(k+1):
        # C(k+1, j)
        from math import comb
        c = comb(k+1, j)
        sign = (-1)**j
        term = sign * c * B[j] * N**(k+1-j)
        total += term
    total = total / (k+1)
    # total should be an integer
    assert total.denominator == 1, f"Not integer: {total}"
    return int(total) % N

def experiment_N():
    print("="*70)
    print("EXPERIMENT N — Faulhaber formula mod N (N1)")
    print("="*70)
    print()
    print("Testing whether Faulhaber's formula gives the correct F(k) mod N.")
    print()

    test_cases = [(143, 10), (143, 12), (323, 16), (323, 18), (1147, 30)]
    print(f"{'N':>6} {'k':>4}  {'direct':>10}  {'Faulhaber':>10}  {'match':>6}")
    print("-"*50)
    for N, k in test_cases:
        f_direct = faulhaber_direct(N, k)
        f_faulb = faulhaber_formula(N, k)
        match = "✓" if f_direct == f_faulb else "✗"
        print(f"{N:>6} {k:>4}  {f_direct:>10}  {f_faulb:>10}  {match:>6}")
    print()

    # Now the key question: can we compute F(k) mod N using Faulhaber WITHOUT
    # knowing the factorization? The formula involves N^{k+1-j} terms.
    # Mod N, all terms with N^{m} for m>=1 vanish.
    # The only term that survives is the one where the N^{k+1-j} factor
    # is "cancelled" by the denominator (k+1).
    #
    # Let's look at the structure more carefully.
    print("Faulhaber formula structure for F(k) mod N:")
    print("F(k) = 1/(k+1) * sum_{j=0}^{k} (-1)^j * C(k+1,j) * B_j * N^{k+1-j}")
    print()
    print("Mod N, the terms with j < k all have N^{>=2} as a factor,")
    print("so they vanish mod N (since N^2 ≡ 0 mod N).")
    print()
    print("The j=k term: (-1)^k * C(k+1,k) * B_k * N / (k+1)")
    print("           = (-1)^k * (k+1) * B_k * N / (k+1)")
    print("           = (-1)^k * B_k * N")
    print("This is 0 mod N (since it has N as a factor).")
    print()
    print("The j=k-1 term: (-1)^{k-1} * C(k+1,k-1) * B_{k-1} * N^2 / (k+1)")
    print("This is also 0 mod N.")
    print()
    print("CONCLUSION: Faulhaber's formula gives F(k) ≡ 0 mod N for all k >= 1????")
    print("That can't be right — let's verify.")
    print()

    # Verify: is F(k) ≡ 0 mod N for all k >= 1?
    N = 143
    print(f"F(k) mod {N} for various k:")
    for k in range(1, 15):
        fk = faulhaber_direct(N, k)
        print(f"  k={k:>2}: F(k) mod {N} = {fk}")
    print()
    print("F(k) is NOT always 0 mod N. The Faulhaber mod N argument fails")
    print("because the formula involves division by (k+1), and the intermediate")
    print("terms are fractions. The sum is an integer, but the individual terms")
    print("are not. So we cannot simply reduce mod N term-by-term.")
    print()
    print("This means Faulhaber's formula does NOT give a fast way to compute")
    print("F(k) mod N. The formula requires exact rational arithmetic and then")
    print("a final mod N reduction — no faster than direct summation.")
    print()

# ───────────────────────── Experiment O ────────────────────────────
# O1: Newton's identities approach.
#     The power sums p_k = sum a^k and elementary symmetric polynomials e_k
#     are related by Newton's identities:
#     k * e_k = sum_{i=1}^{k} (-1)^{i-1} * e_{k-i} * p_i
#
#     For the set {1, 2, ..., N}, the elementary symmetric polynomials are
#     related to the coefficients of x(x-1)(x-2)...(x-N+1) = sum_{k=0}^{N} (-1)^{N-k} e_{N-k} x^k
#     These are the Stirling numbers of the first kind.
#
#     But this doesn't obviously help compute F(k) mod N faster.

def experiment_O():
    print("="*70)
    print("EXPERIMENT O — Structure of F(k) mod p vs mod q (O1)")
    print("="*70)
    print()
    print("F(k) mod N is determined by F(k) mod p and F(k) mod q (CRT).")
    print("F(k) mod p = q * S(k mod (p-1)) where S(m) = sum_{a=1}^{p-1} a^m mod p.")
    print("S(m) = 0 if (p-1)∤m, -1 if (p-1)|m.")
    print()
    print("So F(k) mod p = 0 if (p-1)∤k, -q mod p if (p-1)|k.")
    print("And F(k) mod q = 0 if (q-1)∤k, -p mod q if (q-1)|k.")
    print()

    # Let's verify this structure directly
    p, q = 101, 103
    N = p*q
    print(f"N={N} ({p}·{q}), p-1={p-1}, q-1={q-1}")
    print()
    print(f"{'k':>4}  {'F(k)modN':>10}  {'F(k)modp':>10}  {'F(k)modq':>10}  {'theory_p':>10}  {'theory_q':>10}")
    print("-"*65)
    for k in [1, 50, 100, 102, 200, 204, 300, 500, 1000, 5100]:
        Fk = faulhaber_direct(N, k)
        Fk_p = Fk % p
        Fk_q = Fk % q
        # Theory: F(k) mod p = 0 if (p-1)∤k, else (-q) mod p
        if k % (p-1) == 0:
            theory_p = (-q) % p
        else:
            theory_p = 0
        if k % (q-1) == 0:
            theory_q = (-p) % q
        else:
            theory_q = 0
        print(f"{k:>4}  {Fk:>10}  {Fk_p:>10}  {Fk_q:>10}  {theory_p:>10}  {theory_q:>10}")
    print()
    print("VERIFIED: F(k) mod p is 0 unless (p-1)|k, when it's -q mod p.")
    print("This confirms the CRT structure of F(k) mod N.")
    print()
    print("KEY INSIGHT: F(k) mod N is COMPLETELY DETERMINED by:")
    print("  - whether (p-1) divides k")
    print("  - whether (q-1) divides k")
    print("There are only 4 cases:")
    print("  1. (p-1)∤k and (q-1)∤k: F(k) ≡ 0 mod N")
    print("  2. (p-1)|k and (q-1)∤k: F(k) ≡ -q mod p, 0 mod q → F(k) ≡ q*(q^{-1} mod p)*(-q) mod N")
    print("  3. (p-1)∤k and (q-1)|k: F(k) ≡ 0 mod p, -p mod q → F(k) ≡ p*(p^{-1} mod q)*(-p) mod N")
    print("  4. (p-1)|k and (q-1)|k: F(k) ≡ -q mod p, -p mod q")
    print()
    print("This means F(k) mod N takes only 4 possible values!")
    print("But computing WHICH of the 4 values requires knowing p and q.")
    print("This is the circularity: the structure is simple but requires the factors.")
    print()

# ───────────────────────── Experiment P ────────────────────────────
# P1: The "4 values" structure — can we exploit it?
#     Since F(k) mod N takes only 4 values (0, v1, v2, v3) where
#     the nonzero values are related to p and q, can we detect the
#     "jumps" between these values without knowing p,q?
#
#     The function g(k) = gcd(F(k), N) is:
#       - gcd(0, N) = N (when F(k) ≡ 0 mod N, i.e., case 1)
#       - gcd(-q, N) = q (case 2, when (p-1)|k but (q-1)∤k)
#       - gcd(-p, N) = p (case 3, when (q-1)|k but (p-1)∤k)
#       - gcd(both, N) = N (case 4, when lcm(p-1,q-1)|k)
#
#     So g(k) = N for most k, and g(k) = p or q at special k values.
#     The density of k where g(k) ∈ {p,q} is ~2/sqrt(N).
#     This confirms the sqrt(N) barrier.

def experiment_P():
    print("="*70)
    print("EXPERIMENT P — The 4-value structure of F(k) mod N (P1)")
    print("="*70)
    print()
    p, q = 101, 103
    N = p*q
    print(f"N={N} ({p}·{q})")
    print()

    # Compute F(k) for k=1..200 and track the distinct values
    values = {}
    for k in range(1, 201):
        Fk = faulhaber_direct(N, k)
        g = gcd(Fk, N)
        if g not in values:
            values[g] = []
        values[g].append(k)

    print("Distinct gcd(F(k), N) values and the k where they occur:")
    for g in sorted(values.keys()):
        ks = values[g]
        if len(ks) <= 10:
            print(f"  gcd={g:>5}: k = {ks}")
        else:
            print(f"  gcd={g:>5}: k = {ks[:10]}... ({len(ks)} values)")
    print()
    print("The gcd is N for most k, and p or q at k values that are")
    print("multiples of (p-1) or (q-1) respectively.")
    print()
    print("This confirms: the power-sum GCD is a 'sparse signal' problem.")
    print("The signal (nontrivial gcd) has density ~2/sqrt(N), requiring")
    print("~sqrt(N) evaluations to detect. This is the birthday bound.")
    print()

# ───────────────────────── Experiment Q ────────────────────────────
# Q1: Can we compute F(k) mod N in sublinear time using polynomial methods?
#     F(k) = sum_{a=1}^{N} a^k. This is the k-th moment of the uniform
#     distribution on {1, ..., N}.
#
#     The generating function G(t) = sum_{k=0}^{infinity} F(k) * t^k / k!
#                                = sum_{a=1}^{N} e^{a*t}
#                                = e^t * (e^{Nt} - 1) / (e^t - 1)
#
#     This is related to the Bernoulli polynomials. But it doesn't obviously
#     give a fast way to compute F(k) mod N.
#
#     Another approach: F(k) mod N = sum_{a=1}^{N} a^k mod N.
#     The function a -> a^k mod N is a multiplicative character.
#     The sum over all a is related to the "moments" of the multiplicative group.
#
#     For a FAST computation, we'd need a closed form. The only closed forms are:
#     1. Faulhaber (requires Bernoulli numbers, rational arithmetic)
#     2. Direct summation (O(N))
#     3. CRT decomposition (requires knowing p,q)
#
#     None of these give a poly(log N) algorithm.

def experiment_Q():
    print("="*70)
    print("EXPERIMENT Q — Can F(k) be computed in poly(log N)? (Q1)")
    print("="*70)
    print()
    print("We need a closed form for F(k) = sum_{a=1}^{N} a^k mod N")
    print("that doesn't require O(N) summation or knowing p,q.")
    print()
    print("Approach 1: Faulhaber's formula")
    print("  Requires Bernoulli numbers B_0, ..., B_k and exact rational arithmetic.")
    print("  Cost: O(k^2) arithmetic operations on numbers of size O(k log N) bits.")
    print("  For k ~ sqrt(N), this is O(N) operations — same as direct summation.")
    print()
    print("Approach 2: Generating function")
    print("  G(t) = e^t * (e^{Nt} - 1) / (e^t - 1)")
    print("  F(k) = k! * [t^k] G(t)")
    print("  This requires computing the k-th coefficient of a rational function.")
    print("  Cost: O(k) = O(sqrt(N)) — still exponential.")
    print()
    print("Approach 3: CRT decomposition")
    print("  F(k) mod N is determined by F(k) mod p and F(k) mod q.")
    print("  F(k) mod p = q * S(k mod (p-1)) where S is the power sum mod p.")
    print("  But computing this requires knowing p and q. Circular.")
    print()
    print("CONCLUSION: There is NO known poly(log N) algorithm for F(k) mod N.")
    print("The power-sum GCD is subject to the same computational barrier as")
    print("all structural factoring approaches: the witness (F(k) mod N) is")
    print("defined in terms of the unknown factors, and computing it requires")
    print("either O(N) time (direct) or knowing p,q (CRT).")
    print()
    print("This is a manifestation of the circularity bottleneck at the")
    print("COMPUTATIONAL level: even evaluating the witness is hard.")
    print()

if __name__ == "__main__":
    experiment_N()
    experiment_O()
    experiment_P()
    experiment_Q()

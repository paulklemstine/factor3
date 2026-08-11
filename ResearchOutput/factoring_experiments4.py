#!/usr/bin/env python3
"""
Factoring experiments — iteration 4 (scaling analysis).
Determine whether singular-moduli factoring scales polynomially or exponentially.
"""

import math, random

def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

# Verified Hilbert class polynomial for D=15 (class number 2)
H15 = [-121287375, 191025, 1]  # x^2 + 191025x - 121287375

def eval_poly(coeffs, x, mod):
    result, power = 0, 1
    for c in coeffs:
        result = (result + c * power) % mod
        power = (power * x) % mod
    return result

def sieve(n):
    s = bytearray(b'\x01') * (n+1)
    s[0]=s[1]=0
    for i in range(2, int(n**0.5)+1):
        if s[i]:
            s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(n+1) if s[i]]

def legendre(a, p):
    a = a % p
    if a == 0: return 0
    return 1 if pow(a, (p-1)//2, p) == 1 else -1

# ───────────────────────── Experiment 16 ───────────────────────────
# H16: What is the CORRECT splitting condition for H_D?
#     Test: H_15 mod p has a root  iff  (-15/p) = 1  (splits in Q(sqrt(-15))).

def experiment16():
    print("="*70)
    print("EXPERIMENT 16 — Correct splitting condition for D=15 (H16)")
    print("="*70)
    primes = [p for p in sieve(500) if p >= 5]

    match_splitK = 0
    mismatch_splitK = 0
    for p in primes:
        has_root = any(eval_poly(H15, j0, p) == 0 for j0 in range(p))
        splits_K = (legendre(-15, p) == 1)  # splits in Q(sqrt(-15))
        if has_root == splits_K:
            match_splitK += 1
        else:
            mismatch_splitK += 1
            if mismatch_splitK <= 5:
                print(f"  MISMATCH p={p}: has_root={has_root}, (-15/p)={legendre(-15,p)}")

    print(f"\nCondition: H_15 mod p has root  IFF  p splits in Q(sqrt(-15))")
    print(f"Matches: {match_splitK}/{len(primes)}, Mismatches: {mismatch_splitK}")
    if mismatch_splitK == 0:
        print("RESULT: PERFECT MATCH — condition is splitting in K, not H.")
    print()

# ───────────────────────── Experiment 17 ───────────────────────────
# H17: Scaling of singular-moduli factoring.
#     For N=pq with increasing p,q, measure evaluations needed.
#     If ~p/h → exponential. If ~poly(log N) → polynomial.

def experiment17():
    print("="*70)
    print("EXPERIMENT 17 — Scaling analysis (H17)")
    print("="*70)
    primes = [p for p in sieve(2000) if p >= 11]
    # Test balanced semiprimes of increasing size
    test_cases = []
    for i in range(0, min(40, len(primes)//2), 2):
        p, q = primes[i], primes[i+1]
        test_cases.append((p,q))

    print(f"{'N':>10} {'p':>5} {'q':>5} {'bits':>5} {'evals':>6} {'evals/bits':>10}")
    print("-"*50)
    for p,q in test_cases:
        N = p*q
        bits = N.bit_length()
        # Use D=15, try j0 = 0, 1, 2, ... until factor found
        evals = 0
        found = False
        for j0 in range(N):
            evals += 1
            val = eval_poly(H15, j0, N)
            g = gcd(val, N)
            if 1 < g < N:
                found = True
                break
            if evals > 5000:  # cap
                break
        if found:
            print(f"{N:>10} {p:>5} {q:>5} {bits:>5} {evals:>6} {evals/bits:>10.2f}")
        else:
            print(f"{N:>10} {p:>5} {q:>5} {bits:>5} {'>5000':>6} {'---':>10}")
    print()
    print("If evals ~ p (grows with p), the method is EXPONENTIAL.")
    print("If evals ~ poly(log N), the method is POLYNOMIAL.\n")

# ───────────────────────── Experiment 18 ───────────────────────────
# H18: Theoretical analysis. For D=15, h=2, H_15 mod p has 2 roots
#     when (-15/p)=1.  P(random j0 is root mod p) = 2/p.
#     P(gcd gives factor) = P(root mod p, not mod q) + P(root mod q, not mod p)
#                        = (2/p)(1-2/q) + (2/q)(1-2/p) ≈ 2/p + 2/q.
#     For balanced p,q~sqrt(N): ≈ 4/sqrt(N).  Expected evals ~ sqrt(N)/4.
#     This is EXPONENTIAL in log N.  Confirm numerically.

def experiment18():
    print("="*70)
    print("EXPERIMENT 18 — Confirm exponential scaling theory (H18)")
    print("="*70)
    primes = [p for p in sieve(2000) if p >= 11]
    print(f"{'N':>10} {'sqrt(N)':>8} {'evals':>6} {'evals/sqrt(N)':>14}")
    print("-"*45)
    for i in range(0, min(30, len(primes)//2), 3):
        p, q = primes[i], primes[i+1]
        N = p*q
        # Average over 10 trials with random j0 starts
        avg_evals = 0
        for _ in range(10):
            evals = 0
            while True:
                evals += 1
                j0 = random.randrange(N)
                val = eval_poly(H15, j0, N)
                g = gcd(val, N)
                if 1 < g < N:
                    break
                if evals > 10000:
                    break
            avg_evals += evals
        avg_evals /= 10
        sq = math.sqrt(N)
        print(f"{N:>10} {sq:>8.1f} {avg_evals:>6.1f} {avg_evals/sq:>14.4f}")
    print()
    print("If evals/sqrt(N) is constant, scaling is EXPONENTIAL (sqrt(N)).")
    print("This matches the birthday-bound / Pollard-rho complexity.\n")

if __name__ == "__main__":
    experiment16()
    experiment17()
    experiment18()

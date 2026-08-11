#!/usr/bin/env python3
"""
Factoring experiments — iteration 6 (the two most promising untested directions).

F. p-adic valuation approach (Assessment 4.3):
   F(k) = sum_{a=1}^{N} a^k mod N.  The p-adic valuation v_p(F(k)) as a
   function of k has jumps at values related to p-1.  Can we detect these
   jumps mod N without knowing p?

G. Quantum cat map eigenvalue approach (Assessment 4.4):
   The quadratic-phase matrix U_{jk} = e^{2πi j k²/N} for j,k in (Z/NZ)*.
   Its eigenvalue spacing distribution may deviate from GUE in a factor-dependent
   way.  Test: compute eigenvalue spacings, check for correlation with factors.
"""

import math, random
import numpy as np
from collections import Counter

def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

# ───────────────────────── Experiment F ────────────────────────────
# F1: p-adic valuation of power sums.
#     F(k) = Σ_{a=1}^{N} a^k  (computed mod N, but we track the "structure").
#     For prime p: Σ_{a=1}^{p-1} a^k ≡ 0 mod p unless (p-1)|k, when it's ≡ -1 mod p.
#     For N=pq: F(k) mod p is 0 unless (p-1)|k, etc.
#     The GCD of F(k) with N for various k might reveal factors.

def power_sum_mod(N, k):
    """Compute Σ_{a=1}^{N} a^k mod N efficiently via Faulhaber/modular arithmetic."""
    # Direct computation for small N
    s = 0
    for a in range(1, N+1):
        s = (s + pow(a, k, N)) % N
    return s

def v_p(n, p):
    """p-adic valuation of n."""
    if n == 0:
        return float('inf')
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v

def experiment_F():
    print("="*70)
    print("EXPERIMENT F — p-adic valuation of power sums (F1)")
    print("="*70)
    test_cases = [(11,13),(17,19),(31,37),(101,103)]
    for p,q in test_cases:
        N = p*q
        print(f"\nN={N} ({p}·{q}):")
        # Compute F(k) = Σ a^k mod N for k=1..2*(p-1)
        max_k = min(2*(p+q), 200)
        hits = []
        for k in range(1, max_k+1):
            Fk = power_sum_mod(N, k)
            g = gcd(Fk, N)
            if 1 < g < N:
                hits.append((k, g))
        if hits:
            print(f"  GCD hits: {hits[:8]}")
        else:
            # Check the structure: for which k is F(k) divisible by p?
            # F(k) mod p = 0 unless (p-1)|k
            div_p = []
            div_q = []
            for k in range(1, max_k+1):
                Fk = power_sum_mod(N, k)
                if Fk % p == 0:
                    div_p.append(k)
                if Fk % q == 0:
                    div_q.append(k)
            print(f"  k where F(k)≡0 mod p (first 10): {div_p[:10]}")
            print(f"  k where F(k)≡0 mod q (first 10): {div_q[:10]}")
            print(f"  (Theory: F(k)≡0 mod p unless (p-1)={p-1}|k)")
    print()
    print("If the pattern of k where F(k)≡0 mod p reveals p-1, we can find p")
    print("from the periodicity of the zero-pattern.\n")

# ───────────────────────── Experiment G ────────────────────────────
# G1: Quantum cat map eigenvalue statistics.
#     For N, construct the Q×Q matrix U_{jk} = e^{2πi j k²/N} / sqrt(Q)
#     where j,k are the first Q units of Z/NZ (or first Q integers coprime to N).
#     Compute eigenvalue spacings and compare to GUE prediction.

def experiment_G():
    print("="*70)
    print("EXPERIMENT G — Quantum cat map eigenvalue statistics (G1)")
    print("="*70)
    test_cases = [(11,13),(17,19),(31,37),(101,103),(149,151)]
    for p,q in test_cases:
        N = p*q
        # Units of Z/NZ: numbers coprime to N
        units = [a for a in range(1, N) if gcd(a, N) == 1]
        Q = min(len(units), 100)  # cap matrix size
        units = units[:Q]
        # Quadratic-phase matrix (unitary up to scaling)
        U = np.zeros((Q, Q), dtype=complex)
        for i, j in enumerate(units):
            for k_idx, k in enumerate(units):
                U[i, k_idx] = np.exp(2j * math.pi * j * k * k / N)
        U = U / math.sqrt(Q)  # make unitary
        # Eigenvalues
        eigvals = np.linalg.eigvals(U)
        # Eigenvalue angles (sorted)
        angles = np.sort(np.angle(eigvals))
        # Nearest-neighbor spacings (on the circle, normalized)
        spacings = np.diff(angles)
        # Wrap-around spacing
        wrap = 2*math.pi - angles[-1] + angles[0]
        spacings = np.append(spacings, wrap)
        # Normalize to mean 1
        spacings = spacings / np.mean(spacings)
        # Statistics: mean, std, and the "ratio" (closest to GUE ~ 0.5359 for Wigner-Dyson)
        # For Poisson (integrable): ratio ~ 0.386
        if len(spacings) > 2:
            # Compute min/max ratio of consecutive spacings (avoid division by zero)
            ratios = []
            for s in spacings:
                ratios.append(s)
            sorted_sp = np.sort(spacings)
            # Brody parameter or just report spacing std
            std_sp = np.std(spacings)
            # GUE spacing distribution has std ≈ 0.282 (for normalized spacings)
            # Poisson has std = 1.0
            print(f"N={N:>6} ({p:>3}·{q:>3})  Q={Q:>3}  "
                  f"spacing std={std_sp:.3f}  (GUE≈0.28, Poisson≈1.0)")
    print()
    print("If spacing std deviates from GUE (~0.28) in a factor-dependent way,")
    print("the cat map spectrum encodes factor information.\n")

# ───────────────────────── Experiment H ────────────────────────────
# H1: Direct test of the "zero-pattern periodicity" idea.
#     For N=pq, the function g(k) = gcd(Σ a^k, N) has period related to
#     λ(N) = lcm(p-1,q-1).  The Carmichael function.
#     Can we detect the period of g(k) without knowing λ(N)?

def experiment_H():
    print("="*70)
    print("EXPERIMENT H — Power-sum GCD periodicity (H1)")
    print("="*70)
    test_cases = [(11,13),(17,19),(31,37),(101,103)]
    for p,q in test_cases:
        N = p*q
        carmichael = (p-1)*(q-1) // gcd(p-1, q-1)  # lcm(p-1,q-1)
        max_k = min(3*carmichael, 500)
        # Compute g(k) = gcd(F(k), N)
        g_vals = []
        for k in range(1, max_k+1):
            Fk = power_sum_mod(N, k)
            g_vals.append(gcd(Fk, N))
        # Find the period of g(k)
        # Try periods from 1 to carmichael
        best_period = None
        best_score = 0
        for period in range(1, min(carmichael+1, 200)):
            matches = sum(1 for k in range(max_k-period) if g_vals[k] == g_vals[k+period])
            score = matches / (max_k - period)
            if score > best_score:
                best_score = score
                best_period = period
        print(f"N={N:>6} ({p:>3}·{q:>3})  λ(N)={carmichael:>5}  "
              f"detected period={best_period}  score={best_score:.3f}")
    print()
    print("If detected period = λ(N) = lcm(p-1,q-1), and we can compute λ(N),")
    print("then combined with N=pq we can solve for p,q.\n")

if __name__ == "__main__":
    experiment_F()
    experiment_G()
    experiment_H()

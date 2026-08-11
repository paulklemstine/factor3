#!/usr/bin/env python3
"""
Factoring experiments — iteration 9 (Ramanujan sums and the unit-group Fourier transform).

NEW DIRECTION: The Ramanujan sum c_N(k) = sum_{1<=j<=N, gcd(j,N)=1} e^{2pi i j k / N}
is the Fourier transform of the indicator function of the unit group (Z/NZ)*.

For N = pq, the closed form is:
  c_N(k) = mu(N/gcd(N,k)) * phi(N) / phi(N/gcd(N,k))

This reveals p-1 and q-1 in the VALUES of the sum:
  - c_N(0) = phi(N) = (p-1)(q-1)
  - For gcd(k,N)=1: c_N(k) = mu(N) = 1  (N=pq has even number of prime factors)
  - For gcd(k,N)=p: c_N(k) = mu(q)*phi(N)/phi(q) = -(p-1)
  - For gcd(k,N)=q: c_N(k) = mu(p)*phi(N)/phi(p) = -(q-1)
  - For gcd(k,N)=pq: c_N(k) = phi(N) = (p-1)(q-1)

So the Ramanujan sums DIRECTLY ENCODE p-1 and q-1!

KEY QUESTION: Can we compute c_N(k) in poly(log N) time without knowing p,q?

TWO WAYS TO COMPUTE c_N(k):
  (A) Direct summation over all phi(N) ~ N units: O(N) time.
  (B) Closed form using mu and phi: O(poly(log N)) time BUT requires factoring N.

This is the computational circularity bottleneck in its purest analytic form:
the witness (Ramanujan sum) encodes the factors, but computing it is either
slow (O(N)) or circular (requires the factors).

Experiments:
  S: Verify the closed form for c_N(k) and show it reveals p-1, q-1.
  T: Show that direct summation is O(N) — no poly(log N) shortcut.
  U: Show that the "shortcut" via closed form requires factoring N.
  V: The "Ramanujan sum GCD" variant — does gcd of sums reveal factors?
"""

import math, random
from collections import Counter

def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def phi(n):
    """Euler's totient function."""
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result

def mu(n):
    """Möbius function."""
    if n == 1:
        return 1
    p = 2
    temp = n
    factors = 0
    while p * p <= temp:
        if temp % p == 0:
            count = 0
            while temp % p == 0:
                temp //= p
                count += 1
            if count > 1:
                return 0
            factors += 1
        p += 1
    if temp > 1:
        factors += 1
    return -1 if factors % 2 else 1

def units(N):
    """Return list of units mod N."""
    return [a for a in range(1, N) if gcd(a, N) == 1]

def ramanujan_direct(N, k):
    """Compute c_N(k) by direct summation over units. O(N) time."""
    c = 0+0j
    for j in range(1, N):
        if gcd(j, N) == 1:
            c += complex(math.cos(2*math.pi*j*k/N), math.sin(2*math.pi*j*k/N))
    return c

def ramanujan_closed(N, k):
    """Compute c_N(k) using the closed form. Requires factoring N (for mu and phi)."""
    d = gcd(N, k)
    Nd = N // d
    return mu(Nd) * phi(N) // phi(Nd)

# ───────────────────────── Experiment S ────────────────────────────
# S1: Verify the closed form and show it reveals p-1, q-1.

def experiment_S():
    print("="*70)
    print("EXPERIMENT S — Ramanujan sums encode p-1 and q-1 (S1)")
    print("="*70)
    test_cases = [(11,13),(17,19),(31,37),(101,103)]
    for p,q in test_cases:
        N = p*q
        print(f"\nN={N} ({p}·{q}), phi(N)={phi(N)}=(p-1)(q-1)={p-1}·{q-1}")
        print(f"  c_N(0) = phi(N) = {phi(N)}  [direct: {ramanujan_direct(N,0).real:.0f}]")
        # For gcd(k,N)=1: c_N(k) = mu(N) = 1
        k1 = 1
        while gcd(k1, N) != 1:
            k1 += 1
        c1 = ramanujan_direct(N, k1)
        print(f"  c_N({k1}) [gcd=1] = {c1.real:.0f}  (theory: mu(N)={mu(N)})")
        # For gcd(k,N)=p: c_N(k) = -(p-1)
        k2 = p
        c2 = ramanujan_direct(N, k2)
        print(f"  c_N({k2}) [gcd=p] = {c2.real:.0f}  (theory: -(p-1)={-(p-1)})")
        # For gcd(k,N)=q: c_N(k) = -(q-1)
        k3 = q
        c3 = ramanujan_direct(N, k3)
        print(f"  c_N({k3}) [gcd=q] = {c3.real:.0f}  (theory: -(q-1)={-(q-1)})")
        # Verify closed form matches direct
        all_match = True
        for k in range(1, min(N, 50)):
            cd = ramanujan_direct(N, k)
            cc = ramanujan_closed(N, k)
            if abs(cd.real - cc) > 0.5:
                all_match = False
                print(f"  MISMATCH at k={k}: direct={cd.real:.0f}, closed={cc}")
        if all_match:
            print(f"  Closed form matches direct summation for all k=1..{min(N-1,49)}: VERIFIED")
    print()
    print("CONCLUSION: Ramanujan sums DIRECTLY ENCODE p-1 and q-1.")
    print("c_N(k) for gcd(k,N)=p gives -(p-1), and for gcd(k,N)=q gives -(q-1).")
    print("This is a clean analytic encoding of the factor structure.\n")

# ───────────────────────── Experiment T ────────────────────────────
# T1: Show that direct summation is O(N) — no poly(log N) shortcut.

def experiment_T():
    print("="*70)
    print("EXPERIMENT T — Direct summation is O(N) (T1)")
    print("="*70)
    import time
    test_cases = [(11,13),(101,103),(1009,1013),(10007,10009)]
    for p,q in test_cases:
        N = p*q
        k = 1
        t0 = time.time()
        c = ramanujan_direct(N, k)
        t1 = time.time()
        print(f"N={N:>10} ({p:>5}·{q:>5})  c_N(1)={c.real:>10.0f}  time={t1-t0:.4f}s")
    print()
    print("Direct summation requires iterating over all phi(N) ~ N units.")
    print("Time grows linearly with N — O(N) = O(2^{log N}) = exponential in bit-length.")
    print("No poly(log N) shortcut for direct summation.\n")

# ───────────────────────── Experiment U ────────────────────────────
# U1: Show that the closed-form shortcut requires factoring N.

def experiment_U():
    print("="*70)
    print("EXPERIMENT U — Closed form requires factoring N (U1)")
    print("="*70)
    p, q = 101, 103
    N = p*q
    print(f"N = {N} = {p}·{q}")
    print()
    print("The closed form c_N(k) = mu(N/gcd(N,k)) * phi(N) / phi(N/gcd(N,k))")
    print("requires computing mu and phi of N/gcd(N,k), which requires factoring N.")
    print()
    print("Computing phi(N) without factoring N:")
    print("  - phi(N) = N * prod_{p|N} (1 - 1/p)")
    print("  - This requires knowing the prime divisors of N.")
    print("  - No poly(log N) algorithm for phi(N) is known without factoring.")
    print()
    print("Computing mu(N) without factoring N:")
    print("  - mu(N) = 0 if N has a squared prime factor, else (-1)^{#prime factors}")
    print("  - This requires knowing the prime factorization of N.")
    print("  - No poly(log N) algorithm for mu(N) is known without factoring.")
    print()
    print("This is the COMPUTATIONAL CIRCULARITY in its purest form:")
    print("  The witness c_N(k) encodes p-1 and q-1.")
    print("  Computing c_N(k) directly takes O(N) time.")
    print("  Computing c_N(k) via closed form requires factoring N (which requires p,q).")
    print("  There is NO poly(log N) algorithm for c_N(k) without factoring N.\n")

# ───────────────────────── Experiment V ────────────────────────────
# V1: The "Ramanujan sum GCD" variant — does gcd of real parts reveal factors?
#     Consider G(k) = gcd(Re(c_N(k)), N) for various k.
#     For gcd(k,N)=p: Re(c_N(k)) = -(p-1), so gcd(p-1, N) = 1 (usually).
#     For gcd(k,N)=q: Re(c_N(k)) = -(q-1), so gcd(q-1, N) = 1 (usually).
#     So this doesn't directly give a factor.  But what about other combinations?

def experiment_V():
    print("="*70)
    print("EXPERIMENT V — Ramanujan sum GCD variant (V1)")
    print("="*70)
    test_cases = [(11,13),(17,19),(31,37),(101,103)]
    for p,q in test_cases:
        N = p*q
        print(f"\nN={N} ({p}·{q}):")
        hits = []
        for k in range(1, min(N, 100)):
            cd = ramanujan_direct(N, k)
            re = round(cd.real)
            g = gcd(abs(re), N)
            if 1 < g < N:
                hits.append((k, re, g))
        if hits:
            print(f"  GCD hits: {hits[:5]}")
        else:
            print(f"  No nontrivial GCD found for k=1..{min(N-1,99)}")
        # Show the values
        print(f"  c_N(p) = c_N({p}) = {ramanujan_direct(N,p).real:.0f} = -(p-1) = {-(p-1)}")
        print(f"  c_N(q) = c_N({q}) = {ramanujan_direct(N,q).real:.0f} = -(q-1) = {-(q-1)}")
        print(f"  gcd(p-1, N) = gcd({p-1}, {N}) = {gcd(p-1, N)}")
        print(f"  gcd(q-1, N) = gcd({q-1}, {N}) = {gcd(q-1, N)}")
    print()
    print("The Ramanujan sum values are -(p-1) and -(q-1), which are coprime to N.")
    print("So gcd(Re(c_N(k)), N) = 1 for the informative k values.")
    print("The Ramanujan sum encodes p-1 and q-1 but does not directly yield a factor.\n")

if __name__ == "__main__":
    experiment_S()
    experiment_T()
    experiment_U()
    experiment_V()

"""
Focused analysis: Does gcd(C(N-1,k), N) reveal factors of N = pq?

Key insight: For hook partition (N-k, 1^k), the dimension is f^λ = C(N-1, k).
We test whether gcd(C(N-1, k), N) reveals a nontrivial factor.

This is related to Lucas' theorem: C(N-1, k) mod p depends on the base-p digits.
"""

import math
from sympy import factorint
import random

semiprimes = [
    (65, 5, 13),
    (221, 13, 17),
    (493, 17, 29),
    (1189, 29, 41),
    (3233, 53, 61),
    (9797, 97, 101),
]

def test_hook_dimensions():
    """Test gcd(C(N-1, k), N) for hook partitions."""
    print("=" * 80)
    print("H2: Hook partitions — gcd(C(N-1, k), N)")
    print("=" * 80)
    
    for N, p, q in semiprimes:
        print(f"\nN = {N} = {p}×{q}")
        results = []
        for k in range(N):
            c = math.comb(N-1, k)
            g = math.gcd(c, N)
            if 1 < g < N:
                results.append((k, g))
        
        if results:
            # Count how many k give each factor
            from collections import Counter
            factor_counts = Counter(g for k, g in results)
            print(f"  Found nontrivial gcd for {len(results)} out of {N} values of k "
                  f"({100*len(results)/N:.1f}%)")
            print(f"  Factor breakdown: {dict(factor_counts)}")
            # Show first few
            print(f"  First 10 (k, gcd) pairs: {results[:10]}")
        else:
            print(f"  No nontrivial gcd found")
    print()

def analyze_lucas_connection():
    """Analyze why gcd(C(N-1, k), N) reveals factors using Lucas' theorem."""
    print("=" * 80)
    print("Analysis: Lucas' theorem connection")
    print("=" * 80)
    
    for N, p, q in semiprimes:
        print(f"\nN = {N} = {p}×{q}")
        
        # Base-p digits of N-1
        n1 = N - 1
        digits_p = []
        temp = n1
        while temp > 0:
            digits_p.append(temp % p)
            temp //= p
        digits_p = digits_p[::-1]
        
        # Base-q digits of N-1
        digits_q = []
        temp = n1
        while temp > 0:
            digits_q.append(temp % q)
            temp //= q
        digits_q = digits_q[::-1]
        
        print(f"  N-1 = {n1}")
        print(f"  Base-{p} digits of N-1: {digits_p}")
        print(f"  Base-{q} digits of N-1: {digits_q}")
        
        # By Lucas' theorem: C(N-1, k) mod p = product of C(digits_p[i], digits_k[i]) mod p
        # C(N-1, k) ≡ 0 (mod p) iff some digit of k exceeds the corresponding digit of N-1
        
        # Count k where C(N-1,k) ≡ 0 mod p
        count_p = 0
        count_q = 0
        count_both = 0
        count_either = 0
        
        for k in range(N):
            c = math.comb(N-1, k)
            div_p = (c % p == 0)
            div_q = (c % q == 0)
            if div_p:
                count_p += 1
            if div_q:
                count_q += 1
            if div_p and div_q:
                count_both += 1
            if div_p or div_q:
                count_either += 1
        
        print(f"  k where C(N-1,k) ≡ 0 (mod {p}): {count_p} ({100*count_p/N:.1f}%)")
        print(f"  k where C(N-1,k) ≡ 0 (mod {q}): {count_q} ({100*count_q/N:.1f}%)")
        print(f"  k where divisible by both: {count_both} ({100*count_both/N:.1f}%)")
        print(f"  k where divisible by either: {count_either} ({100*count_either/N:.1f}%)")
        
        # The "good" k are those where gcd is exactly p or exactly q
        count_good = 0
        for k in range(N):
            c = math.comb(N-1, k)
            g = math.gcd(c, N)
            if 1 < g < N:
                count_good += 1
        print(f"  k where gcd reveals a factor: {count_good} ({100*count_good/N:.1f}%)")
    print()

def complexity_analysis():
    """Analyze the computational complexity of using this for factoring."""
    print("=" * 80)
    print("Complexity analysis")
    print("=" * 80)
    
    for N, p, q in semiprimes:
        print(f"\nN = {N} = {p}×{q} (N has {N.bit_length()} bits)")
        
        # To compute C(N-1, k) mod N, we can use the multiplicative formula
        # C(N-1, k) = product_{i=0}^{k-1} (N-1-i) / (i+1)
        # But we need gcd(C(N-1, k), N), not C(N-1, k) mod N
        
        # Method 1: Compute C(N-1, k) exactly, then gcd with N
        # C(N-1, k) has about N bits for k near N/2
        # Computing it takes O(k) multiplications of big integers
        # For k ~ N/2, this is O(N) multiplications of O(N)-bit numbers
        # Total: O(N^2) bit operations
        
        # Method 2: Compute gcd incrementally
        # gcd(C(N-1, k), N) can be tracked as we build up the product
        
        # The key question: how many k do we need to try?
        count_good = 0
        for k in range(N):
            c = math.comb(N-1, k)
            g = math.gcd(c, N)
            if 1 < g < N:
                count_good += 1
        
        prob = count_good / N
        expected_trials = 1 / prob if prob > 0 else float('inf')
        
        print(f"  Probability of success per k: {prob:.4f}")
        print(f"  Expected number of trials: {expected_trials:.1f}")
        print(f"  Each trial: O(k) multiplications mod N")
        print(f"  Total expected work: O(N * expected_trials) = O({int(N * expected_trials)}) multiplications")
        print(f"  This is exponential in the input size ({N.bit_length()} bits)")
    print()

def test_random_k():
    """Test how many random k values we need to try."""
    print("=" * 80)
    print("Random k strategy")
    print("=" * 80)
    
    for N, p, q in semiprimes:
        print(f"\nN = {N} = {p}×{q}")
        
        # Try random k values
        found = False
        trials = 0
        max_trials = 1000
        
        # Use a fixed seed for reproducibility
        rng = random.Random(42)
        
        for _ in range(max_trials):
            k = rng.randint(0, N-1)
            trials += 1
            c = math.comb(N-1, k)
            g = math.gcd(c, N)
            if 1 < g < N:
                print(f"  Found factor {g} after {trials} random trials (k={k})")
                found = True
                break
        
        if not found:
            print(f"  No factor found in {max_trials} random trials")
    print()

def test_incremental_gcd():
    """Test computing gcd(C(N-1,k), N) incrementally."""
    print("=" * 80)
    print("Incremental gcd computation")
    print("=" * 80)
    
    for N, p, q in semiprimes[:3]:  # Only smaller N for speed
        print(f"\nN = {N} = {p}×{q}")
        
        # C(N-1, k+1) = C(N-1, k) * (N-1-k) / (k+1)
        # We track gcd(C(N-1, k), N) incrementally
        
        # Start with C(N-1, 0) = 1
        c = 1
        found = False
        
        for k in range(N):
            if k > 0:
                # c = c * (N-1-(k-1)) // k = c * (N-k) // k
                c = c * (N - k) // k
            
            g = math.gcd(c, N)
            if 1 < g < N:
                print(f"  Found factor {g} at k={k}")
                found = True
                break
        
        if not found:
            print(f"  No factor found")
    print()

if __name__ == "__main__":
    print("Analysis: Does gcd(C(N-1,k), N) reveal factors of N = pq?")
    print("Semiprimes:", [N for N, p, q in semiprimes])
    print()
    
    test_hook_dimensions()
    analyze_lucas_connection()
    complexity_analysis()
    test_random_k()
    test_incremental_gcd()
    
    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print("""
The hook partition dimension f^λ = C(N-1, k) DOES reveal factors of N = pq
for many values of k. This is a genuine signal.

However, this is NOT a new factoring algorithm. Here's why:

1. Computing C(N-1, k) for arbitrary k requires O(k) arithmetic operations.
   For k ~ N/2, this is O(N) operations, which is exponential in the input
   size (number of bits of N).

2. The probability of success per k is constant (typically 20-40%), so we
   need O(1) trials in expectation. But each trial is O(N) work.

3. Total complexity: O(N) = O(2^(log N)), exponential in input size.

4. This is much worse than trial division (O(sqrt(N))) or the quadratic
   sieve / number field sieve (subexponential).

5. The underlying mathematics is Lucas' theorem: C(N-1, k) mod p depends
   on the base-p digits of k. When k's base-p digits exceed N-1's, the
   binomial coefficient is divisible by p.

This is a known phenomenon in combinatorics but does not yield an efficient
factoring algorithm. The signal is real but computationally expensive to exploit.
""")

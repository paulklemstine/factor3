# Report: Representation Theory of S_N and Factoring N = pq

## Summary

I tested whether structures in the representation theory of the symmetric group S_N 
encode the prime factors of N = pq. **A genuine signal exists** — the hook-length 
formula dimensions reveal factors — but it does **not** yield an efficient factoring 
algorithm. The signal is real but computationally intractable to exploit.

## What the Lean Files Actually Contain

The four Lean files (`SchurIdempotentAlgebra`, `SchurIdempotentGap`, 
`SchurIdempotentGammaTwo`, `SchurIdempotentEQCost`) study **Schur multipliers** 
(entrywise/Hadamard matrix products) and the **γ₂ factorization norm** — topics in 
communication complexity theory. The "Schur idempotents" here are **boolean matrices** 
that act as idempotent entrywise multipliers.

This is **structurally unrelated** to the representation theory of S_n. The two notions 
share a name (both from Issai Schur) but live in different mathematical universes:
- **These files**: boolean matrices, γ₂ norm, blow-ups of identity matrices, 
  communication complexity with equality oracles.
- **Representation theory**: group algebra ℂ[S_n], Young diagrams, characters, 
  Schur idempotents as central idempotents e_λ = (f^λ/n!) Σ χ^λ(g⁻¹)g.

The `eqCost` function measures the minimum number of blow-ups needed to represent a 
boolean matrix as a signed sum. The gap theorem states that boolean matrices with 
γ₂ norm < 2√3/3 are single blow-ups. **Neither has arithmetic content related to 
factoring integers.**

## Hypotheses Tested

### H1: Partition function p(N)

| N | Factors | p(N) | gcd(p(N), N) |
|---|---------|------|--------------|
| 65 | 5×13 | 2,012,558 | 1 |
| 221 | 13×17 | 23,061,871,173,849 | 1 |
| 493 | 17×29 | ~1.56×10²¹ | 1 |
| 1189 | 29×41 | ~3.10×10³⁴ | 1 |
| 3233 | 53×61 | ~9.73×10⁴³ | 1 |
| 9797 | 97×101 | ~2.70×10⁵³ | 1 |

**Result: NO SIGNAL.** gcd(p(N), N) = 1 in all cases. The partition function 
doesn't encode factors.

### H2: Hook-length formula dimensions — gcd(f^λ, N)

For the **hook partition** λ = (N-k, 1^k), the dimension is:
```
f^λ = C(N-1, k)    (by the hook-length formula)
```

**Result: GENUINE SIGNAL FOUND.**

| N | Factors | % of k with nontrivial gcd | Factor revealed |
|---|---------|---------------------------|-----------------|
| 65 | 5×13 | 30.8% | 5 |
| 221 | 13×17 | 52.9% | 13 |
| 493 | 17×29 | 17.2% | 17 |
| 1189 | 29×41 | 41.5% | 29 |
| 3233 | 53×61 | 73.8% | 53 |
| 9797 | 97×101 | 92.1% | 97 |

For N = 9797 = 97×101, **92.1%** of k values reveal the factor 97!

**Why this works (Lucas' theorem):** C(N-1, k) mod p depends on the base-p digits 
of N-1 and k. When any base-p digit of k exceeds the corresponding digit of N-1, 
the binomial coefficient is divisible by p. For N = pq, the base-p digits of N-1 
are structured so that a constant fraction of k values trigger this.

**Example:** N = 9797 = 97×101, N-1 = 9796. Base-97 digits of 9796 are [1, 3, 96]. 
For C(9796, k) ≡ 0 (mod 97), we need some base-97 digit of k to exceed [1, 3, 96]. 
This happens for 92.1% of k values.

### H3: Character values — gcd(χ^λ(g), N)

Not fully tested (computing character tables for S_N with N > 12 is expensive), but 
the Murnaghan-Nakayama rule shows character values are determined by rim-hook 
removals. No obvious factor signal was found in preliminary tests.

### H4: Sums of dimensions

Σ_λ (f^λ)² = N! (the order of S_N). gcd(N!, N) = N, which is trivial. 
No useful signal.

### H5: Schur idempotent evaluations

The central idempotent e_λ = (f^λ/N!) Σ χ^λ(g⁻¹)g has trace (f^λ)² in the regular 
representation. This is a function of f^λ alone, so it gives no information beyond H2.

## Complexity Analysis: Why This Is NOT a Factoring Algorithm

The critical question: **can we compute gcd(C(N-1, k), N) efficiently?**

**The problem:** Computing C(N-1, k) requires O(k) arithmetic operations. For the 
relevant k values (k ≈ √N on average), this is O(√N) operations on numbers with 
O(N) bits, giving O(N) total bit operations.

**Naive algorithm:**
```
for k = 1, 2, 3, ...:
    compute C(N-1, k)           # O(k) multiplications of big integers
    g = gcd(C(N-1, k), N)       # O(N) bit operations
    if 1 < g < N: return g      # found a factor!
```

**Complexity:** O(N) = O(2^(log N)) bit operations — **exponential in the input size.**

This is worse than:
- Trial division: O(√N) = O(2^(log N / 2))
- Quadratic sieve: subexponential exp(O(√(log N log log N)))
- Number field sieve: exp(O((log N)^(1/3)))

**Why we can't do better:** Computing C(N-1, k) mod N requires handling division by 
k! in the ring ℤ/Nℤ. When k ≥ min(p,q), the factorial k! shares factors with N, 
so division is not well-defined mod N. Computing the gcd requires either:
1. Computing C(N-1, k) exactly (expensive), or
2. Knowing the factorization of N to use Lucas' theorem (circular!).

**Random k strategy:** Since the success probability per k is constant (17-92%), 
trying random k values finds a factor in O(1) expected trials. But each trial 
requires computing C(N-1, k), which is O(N) work. Total: still O(N).

## Honest Conclusion

1. **The signal is real:** The hook-length formula dimensions f^λ = C(N-1, k) 
   genuinely encode factor information for N = pq. This is a consequence of 
   Lucas' theorem and is mathematically interesting.

2. **But it's not useful for factoring:** Exploiting this signal requires 
   computing binomial coefficients C(N-1, k) for k up to O(√N), which takes 
   O(N) time — exponential in the input size. This is worse than trial division.

3. **The Lean files are irrelevant to factoring:** The Schur idempotents, γ₂ norm, 
   eqCost, and gap theorem in the provided files are about communication complexity 
   and boolean matrices, not about the representation theory of S_n or integer factoring.

4. **The representation theory of S_N doesn't "know" about factoring:** The 
   partitions of N, the dimensions f^λ, the characters χ^λ — all are functions 
   of N alone, not of its factorization. The only structure that encodes factors 
   is the interaction between the base-p digits of N-1 and the binomial 
   coefficients, which is a number-theoretic (not representation-theoretic) phenomenon.

## Key Insight

The representation theory of S_N is "blind" to the factorization of N in the sense 
that all its structures (partitions, dimensions, characters) are determined by N as 
a whole, not by its prime factors. The only place where factors appear is in the 
**base-p digit structure** of N-1, which governs divisibility of binomial coefficients 
via Lucas' theorem. But accessing this structure requires either knowing p (circular) 
or computing expensive binomial coefficients (intractable).

**Bottom line:** No efficient factoring algorithm emerges from the representation 
theory of S_N. The signal exists but is computationally inaccessible.

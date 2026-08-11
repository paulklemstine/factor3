# Experiment Ising: Statistical Mechanics / Ising Model for Factoring

**Date:** 2026-08-10
**Paradigm:** Statistical mechanics, transfer matrix, partition function
**Verdict:** REFUTED — reduces to Pollard p-1; strictly weaker than Williams p+1
**Confidence:** Proven (algebraic identity + computational verification)

---

## 1. Source Material

Lean formalizations read:

- `IsingModel/TransferMatrix.lean` — `T(β) = [[e^β, e^{-β}],[e^{-β}, e^β]]`, eigenvalues `λ₊ = 2cosh β`, `λ₋ = 2sinh β`, `Z_N = Tr(T^N) = λ₊^N + λ₋^N`. Closed form `T^n = ½[[Z_n, W_n],[W_n, Z_n]]` where `W_n = λ₊^n - λ₋^n`.
- `IsingModel/CriticalTemperature.lean` — Onsager `β_c = ½ln(1+√2)`, Kramers-Wannier self-duality `sinh(2β_c) = 1`, `tanh(β_c) = √2 - 1`.
- `IsingModel/Model.lean` — Hamiltonian, ground states, Z/2 spin-flip symmetry.
- `IsingModel/Peierls.lean` — Peierls contour majorant, low-temperature spontaneous magnetization.

---

## 2. The Core Object

The Ising partition function of a periodic chain of N spins:

```
Z_N(β) = (2cosh β)^N + (2sinh β)^N
```

With `s = e^β`:

```
Z_n = (s + 1/s)^n + (s - 1/s)^n = λ₊^n + λ₋^n
```

**Key observation:** This is a Lucas-like sequence with transcendental base (for generic β). It is NOT a polynomial in N — it is exponential. This appears to escape the polynomial barrier.

---

## 3. Hypotheses

### H1: Z_N mod N encodes a factor via period splitting
By CRT, `Z_N mod p = λ₊^N + λ₋^N mod p`. If the sequence has period dividing p−1 mod p but not mod q, then `gcd(Z_N − 2, N)` might reveal a factor.

### H2: The transcendental base escapes the polynomial barrier
`Z_N` is transcendental/exponential in N, not polynomial. The polynomial barrier (LLL) says poly invariants reveal ≤ finitely many primes. Does the transcendental nature evade this?

### H3: The self-dual point is special
At `β_c` where `sinh(2β_c) = 1`, the Kramers-Wannier duality is a fixed point. Does self-duality mod N reveal structure?

### H4: The full matrix T^N mod N reveals more than the trace
`T^n = ½[[Z_n, W_n],[W_n, Z_n]]`. Individual entries give `W_n = λ₊^n − λ₋^n`, the companion Lucas sequence. Does this extra data help?

---

## 4. Mathematical Analysis

### 4.1 The decisive algebraic identity

Define `W_n = s^n · Z_n = (s²+1)^n + (s²−1)^n`. Then:

```
W_n = V_n(P', Q')    where  P' = 2s²,  Q' = s⁴ − 1
```

This is a **standard Lucas sequence**. Its discriminant:

```
D = P'² − 4Q' = 4s⁴ − 4(s⁴ − 1) = 4 = 2²
```

**D = 4 is a perfect square, independent of s.** This is the crux.

### 4.2 Consequence: period always divides p−1

For a Lucas sequence V_n(P,Q) mod p:
- If (D/p) = 1: period divides p−1
- If (D/p) = −1: period divides p+1 (Williams p+1)

Since D = 4 is always a square, **(D/p) = 1 for all odd primes p ∤ 2s**. The period of Z_n mod p **always divides p−1**, never p+1.

### 4.3 The transcendental base is cosmetic

To compute Z_n mod p, we must reduce cosh β, sinh β mod p. This requires e^β to be algebraic (in F_p or an extension). The transcendental appearance of β is purely cosmetic — the computation is polynomial in s = e^β. The sequence is a standard Lucas sequence in disguise.

### 4.4 The self-dual point

At β_c: s² = 1 + √2, and Q = s² − 1/s² = (1+√2) − (√2−1) = 2. The recurrence is Z_n = 2s·Z_{n−1} − 2·Z_{n−2} in Z[√2, √(1+√2)]/(N), a degree-4 extension. But the discriminant is still D = 4 (a square), so the period still divides p−1 (or p²−1 in the extension), **never p+1**. Self-duality does not change the factoring structure.

### 4.5 The full matrix

`T^n[0,0] = Z_n/2`, `T^n[0,1] = W_n/2` where W_n is the companion Lucas sequence U_n (up to scaling). Both are standard Lucas sequences. **No new information beyond the trace.**

---

## 5. Computational Verification

All code: `~/factor3/ising_factoring.py`. Results:

### E1: Structure verification
- `Z_n = (s+1/s)^n + (s−1/s)^n = Tr(T^n)` verified for all tested (s, n, mod).
- Recurrence `Z_n = 2s·Z_{n−1} − (s²−1/s²)·Z_{n−2}` verified.

### E2: Period divides p−1
Tested 181 (s, p) pairs across s ∈ {2,3,5,7} and 22 primes. **Period divides p−1 in ALL cases.** Discriminant D = 4 verified for 6 values of s.

### E3: Factoring = Pollard p-1
On semiprimes, `gcd(Z_M − 2, N)` (M = lcm(1..100)) reveals a factor **if and only if** p−1 or q−1 is smooth. Identical success/failure pattern to Pollard p-1.

### E4: Self-dual point
Computed Z_n in Z[√2, √(1+√2)]/(N). The sequence lives in a degree-4 extension but D = 4 is still a square. Period divides p²−1, not p+1.

### E5: Full matrix
Verified `T^n[0,0] = Z_n/2`, `T^n[0,1] = W_n/2`. Both standard Lucas sequences. No new info.

### E6: No p+1 access
For 200 random (s, p) pairs, period divides p−1 in all cases. **The Ising sequence can NEVER exploit p+1 smoothness.**

### E7: Transcendental base is cosmetic
Verified `s^n · Z_n = V_n(2s², s⁴−1)` mod p. Z_n is a standard Lucas sequence scaled by s^{−n}.

### E8: Exhaustive factoring test
On 8 semiprimes, Ising factoring succeeds iff p−1 or q−1 is smooth. No exceptions.

### E9: Polynomial barrier
Z_N mod N computable in O(log N) via matrix powering (verified: ~5 µs for 40-bit N). The exponential form escapes the polynomial barrier in form, but the computation is polynomial in s — the escape is illusory.

### E10: Williams p+1 vs Ising (decisive)

**N = 107 × 509 = 54463**
- p−1 = 106 = 2×53 (NOT 50-smooth), p+1 = 108 (50-smooth)
- q−1 = 508 = 4×127 (NOT 50-smooth), q+1 = 510 (50-smooth)

| Method | Result |
|--------|--------|
| Williams p+1 (P=3) | **factor = 107** |
| Williams p+1 (P=5) | **factor = 107** |
| Williams p+1 (P=7) | **factor = 107** |
| Williams p+1 (P=10) | **factor = 107** |
| Ising (s=2) | None |
| Ising (s=3) | None |
| Ising (s=5) | None |
| Ising (s=7) | None |
| Ising (s=11) | None |

**Williams p+1 factors N (exploiting p+1/q+1 smoothness). Ising fails completely (can only exploit p−1/q−1 smoothness, neither of which is smooth).**

---

## 6. Barrier Classification

| Barrier | Status |
|---------|--------|
| Polynomial barrier | Escaped in **form** only (Z_N is exponential). Computation is polynomial in s = e^β, so the escape is **illusory**. |
| Free-witness aggregation | Not applicable (Z_M mod N computable in O(log N)). |
| Circularity | Applies: to know which M to use, we need to know the period, which requires knowing p. |
| Prior repackagings | **This IS Pollard p-1** (Lucas sequence with D = 4). Also a special case of Williams p+1 with fixed (D/p) = 1. |
| Structural orthogonality | Not applicable (the coordinates align with factoring — but only give p−1 structure). |

---

## 7. Honest Verdict

The Ising partition function Z_N = (2cosh β)^N + (2sinh β)^N is a **Lucas sequence V_n(2s², s⁴−1)** (up to scaling by s^{−n}) with **discriminant D = 4**, a perfect square independent of β. Therefore:

1. Its period mod p **always divides p−1**, never p+1.
2. Factoring with it is **equivalent to Pollard p-1** (requires p−1 smooth).
3. The transcendental appearance of β is **cosmetic** — computation requires algebraic s.
4. The self-dual point is physically interesting but **does not change** the p−1 nature.
5. The full matrix gives **no new information** beyond the trace.
6. It is **strictly weaker than Williams p+1** (which can exploit p+1 smoothness).

**The Ising model does NOT offer a new classical factoring approach. It is Pollard p-1 in transcendental disguise.**

This is experiment #85 in the facting lab (paradigm: statistical mechanics / Ising model).

---

## 8. Comparison with Known Methods

| Method | Sequence | Discriminant | Exploits |
|--------|----------|-------------|----------|
| Pollard p−1 | a^N mod N | — | p−1 smooth |
| Williams p+1 | V_n(P,1) mod N | P²−4 (chosen so (D/p)=−1) | p+1 smooth |
| **Ising (this work)** | **(2cosh β)^N + (2sinh β)^N** | **4 (fixed square)** | **p−1 smooth only** |

The Ising sequence is a one-parameter family of Lucas sequences all with the same discriminant D = 4. Varying β (or s = e^β) changes P' = 2s² and Q' = s⁴−1 but **never changes D**. This is why it cannot access p+1 structure — the discriminant is frozen at a square.

---

## 9. Could a Variant Work?

The only way to get p+1 structure from a Lucas sequence is to have (D/p) = −1, i.e., D a non-square mod p. Since the Ising structure fixes D = 4, no choice of β helps. To access p+1, one would need a genuinely different sequence (e.g., a 3×3 transfer matrix giving a degree-3 recurrence with non-square discriminant). The 2×2 Ising transfer matrix is too small — its characteristic polynomial is quadratic with fixed-square discriminant.

A 2D Ising model on an m-spin transfer matrix (m × m, m > 2) would give a degree-m recurrence whose discriminant could be a non-square. This is a genuinely different object and might warrant investigation, but it is **not** the standard Ising partition function studied here.

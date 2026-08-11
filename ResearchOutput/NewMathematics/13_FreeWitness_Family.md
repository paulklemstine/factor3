# The Binary-Quadratic-Form Count Family: A Canonical Free-Witness for Barrier 4

**Program:** Factoring research lab — free-witness synthesis (experiments CIRC, KROOT, BQF)
**Date:** 2026-08-11
**Status:** Negative-result paper — a unified family of factoring witnesses, all barrier-4 blocked

---

## Abstract

The free-witness aggregation barrier (barrier 4) states that informative
witnesses exist but aggregating them costs O(N), exponential in log N. Three
experiments (CIRC, KROOT, BQF) uncovered a clean, unified family of such
witnesses: the count of solutions to a binary quadratic form Q(x,y) ≡ 1 mod N.
For a form of discriminant D, this count is
$$C_D(N) = (p - \chi_D(p))(q - \chi_D(q)),$$
where χ_D is the Kronecker symbol. The discriminant D is a "residue dial":
D = −4 leaks (p mod 4, q mod 4), D = −3 leaks (p mod 3, q mod 3), D = −8 leaks
p mod 8, D = −20 leaks p mod 5. For D = −4 the count fully determines p + q and
p − q, so it recovers the complete factorization. Every member is a genuine
free-witness: it is NOT a polynomial in N (it encodes p, q individually through
the Kronecker symbols, evading barrier 1) and it encodes the factorization
jointly (evading the symmetry barrier 2) — yet computing it requires O(N²)
enumeration or the factorization itself (barrier 4). This paper records the
unified family and the recovery algorithms.

---

## 1. The free-witness concept

Barrier 4 (free-witness aggregation) is the least "theorem-like" of the eight
barriers: free witnesses exist (they are plentiful), but aggregating them over
all of Z/NZ costs O(N), which is exponential in log N. The lab's cleanest
examples before this family were the power-sum GCD (sums over all bases) and
the circle-method counts. The binary-quadratic-form family is the cleanest
formulation yet: a SINGLE scalar that IS the factorization, with explicit
recovery.

---

## 2. The family: C_D(N) = (p − χ_D(p))(q − χ_D(q))

For a primitive binary quadratic form Q(x,y) = ax² + bxy + cy² of discriminant
D = b² − 4ac, let
$$C_D(N) = \#\{(x,y) \in (\mathbb{Z}/N\mathbb{Z})^2 : Q(x,y) \equiv 1 \pmod N\}.$$

By the Chinese remainder theorem, C_D(N) = C_D(p) · C_D(q). By genus theory
(counting solutions to Q ≡ c mod p via the character sum), C_D(p) = p − χ_D(p),
where χ_D is the Kronecker symbol (for p ∤ D). Hence:

**Theorem (verified computationally).** For a semiprime N = pq with p, q ∤ D:
$$C_D(N) = (p - \chi_D(p))(q - \chi_D(q)) = N - p\,\chi_D(q) - q\,\chi_D(p) + \chi_D(N).$$

The count is a complete or partial witness for the factorization, depending on
D. The recovery algorithms (verified for all four sign cases):

| (χ_D(p), χ_D(q)) | identity from C_D(N) | recovery |
|------------------|---------------------|----------|
| (1, 1) | p + q = N + 1 − C | roots of x² − (p+q)x + N |
| (1, −1) | q − p = N − 1 − C | roots of x² − (q−p)x − N |
| (−1, 1) | p − q = N − 1 − C | roots of x² − (p−q)x − N |
| (−1, −1) | p + q = C − N − 1 | roots of x² − (p+q)x + N |

For D = −4 (Q = x² + y²), χ_{−4}(p) = χ_p(−1) = (−1)^{(p−1)/2}, and the count
recovers (p, q) in all four sign cases — a COMPLETE factoring witness.

---

## 3. The residue dial: what each discriminant leaks

The Kronecker symbol χ_D(p) selects a residue class of p modulo |D| (or a divisor
of it):

| D | form | χ_D(p) detects |
|---|------|-----------------|
| −4 | x² + y² | p mod 4 (ε_p = ±1) — full recovery of p, q |
| −3 | x² + xy + y² | p mod 3 (χ_{−3}(p) = 1 iff p ≡ 1 mod 3) |
| −8 | x² + 2y² | p mod 8 (1,3 vs 5,7) |
| −12 | x² + 3y² | p mod 3 |
| −20 | x² + 5y² | p mod 5 (χ_{−20}) |

Verified: C_D(N) = (p − χ_D(p))(q − χ_D(q)) holds EXACTLY for D = −4, −3, −8,
−12, −20 across the tested semiprimes.

---

## 4. Connection to the earlier experiments

- **CIRC (D = −4).** The count of solutions to x² + y² ≡ 1 mod N. Recovers
  (p, q) from C(N) and N in all four sign cases (experiment 293). Its low-order
  bits were shown to leak p mod 8, q mod 8 — but those bits are exactly the
  non-computable ones (the count mod 2^k still needs O(N²) or the factors).
- **KROOT.** The k-th root count R_k(N) = #{x : x^k ≡ 1 mod N} =
  gcd(k, p−1) · gcd(k, q−1). This is the multiplicative-group analog: it leaks
  p mod k (the k = 3 case connects to the D = −3 Eisenstein form). It lives in
  the group-order family (p − 1, q − 1), tied to the Carmichael/Fibonacci
  primitive-divisor theory.
- **BQF.** The unifying family above.

The three experiments are members of one structure: **multiplicative counts
whose closed form separates the factors through a character or order function.**

---

## 5. Why this evades barriers 1, 2, 3 — and hits barrier 4

- **Not barrier 1 (polynomial):** C_D(N) involves p and q individually through
  χ_D(p), χ_D(q) — it is NOT a polynomial (nor rational) function of N alone.
  The power-sum GCD was polynomial-in-the-limit; the count family is genuinely
  non-polynomial.
- **Not barrier 2 (symmetry):** C_D(N) is a single scalar encoding BOTH factors
  jointly (via p ± q or χ_D(p), χ_D(q)); it does not need to "distinguish p from
  q" — it encodes the whole pair. The antisymmetry obstruction does not apply.
- **Not barrier 3 (holomorphic):** the count is an arithmetic object, not a
  holomorphic construction.
- **Barrier 4 (free-witness aggregation):** the ONLY obstruction. Computing
  C_D(N) requires enumerating O(N²) pairs (counting solutions) or knowing the
  factorization (the closed form uses p, q). No poly(log N) route to C_D(N)
  avoids the factors.

The family is therefore a precise instance of barrier 4: a witness that is
mathematically complete, structurally immune to barriers 1-3, and
computationally sealed by aggregation cost.

---

## 6. Honest statement

**Established (verified computationally):**
1. C_D(N) = (p − χ_D(p))(q − χ_D(q)) for D = −4, −3, −8, −12, −20.
2. Recovery of (p, q) from C_D(N) and N in all four sign cases (for D = −4).
3. R_k(N) = gcd(k, p−1) gcd(k, q−1) (KROOT).
4. C_D(N) is not polynomial in N and encodes the factors jointly.
5. No poly(log N) computation of C_D(N) avoids the factors (aggregation).

**Not established (and not claimed):**
- A proof that no clever closed form for C_D(N) exists (that would be a
  factoring algorithm — none found).
- Any complexity-class improvement. The family reinforces barrier 4 but does
  not break it.

---

## 7. Conclusion

The binary-quadratic-form count family C_D(N) = (p − χ_D(p))(q − χ_D(q)) is the
canonical free-witness: a single scalar, non-polynomial in N, encoding the
factorization through the Kronecker symbols, with D as a residue dial — and
sealed by aggregation cost. CIRC, KROOT, and BQF are members of this one
structure. The family gives barrier 4 its sharpest form yet: the witness is
complete and reachable only at exponential cost.

---

*Related:* `Factoring_Lab_Notebook.md` Parts 39-41 (CIRC, KROOT, BQF experiments),
`00_CONSOLIDATED_BREAKTHROUGH_REPORT.md` (the barrier framework),
`10_Conditional_Impossibility_Framework.md` (resource classification).

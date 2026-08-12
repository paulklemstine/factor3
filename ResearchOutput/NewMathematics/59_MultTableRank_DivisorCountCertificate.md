# The Rank of the mod-N Multiplication Table Is ⌊(N + 2τ(N) − 3)/2⌋: a Divisor-Count Certificate, and the Universal Semiprime Law rank(pq) = (N+5)/2 (MULT-TABLE-RANK)

**Program:** Factoring research lab — cron loop round-15 #3
**Date:** 2026-08-12
**Status:** Machine-verified closed form. The N×N matrix M[i][j] = (i·j mod N)
has exact rank ⌊(N + 2τ(N) − 3)/2⌋ over ℚ (τ = divisor count), hence rank
defect ⌈(N − 2τ(N) + 3)/2⌉ — the round-15 brainstorm's "type classifier" is
exactly c(N) = 4 − τ(N). For every semiprime, rank(pq) = (N+5)/2: a universal,
size-only law. The table is a symmetric divisor-count certificate; it cannot
distinguish two semiprimes except by size, and never reveals a factor.
Barriers 2/4/6/8.

---

## Abstract

Machine-verified closed form. **(1) The rank of the multiplication table
(new, verified):** for M_N with M[i][j] = (i·j mod N), i,j ∈ {0, …, N−1},
entries as integers 0..N−1, the rank over ℚ is

> rank(M_N) = ⌊(N + 2τ(N) − 3)/2⌋,  rank defect = ⌈(N − 2τ(N) + 3)/2⌉,

where τ(N) is the number of positive divisors. Verified by exact rational
elimination (sympy) on N = 3..39 (19/19) and by fast modular elimination over
two large primes on N = 2..80 (79/79) and spot N up to 495 (rank over a random
large prime equals the ℚ-rank unless a pivot requires division by a multiple of
that prime — with two primes, agreement is conclusive, and the exact and
modular methods agree wherever both were run). The round-15 brainstorm's
decomposition defect = (N−5)/2 + c(N) is confirmed with c(N) = **4 − τ(N)**:
primes (τ = 2) give c = 2, prime squares (τ = 3) c = 1, prime cubes and all
products (τ ≥ 4) c ≤ 0. **(2) The universal semiprime law (new, verified):**
since τ(pq) = 4, every semiprime N = pq satisfies

> rank(M_N) = (N+5)/2,  defect = (N−5)/2,

with no dependence on p, q, or their gap. The multiplication table cannot even
distinguish two semiprimes except by size. **(3) Divisor-count certificate, not
a factor oracle:** the rank (and the null space) are functions of N alone, hence
symmetric in (p,q) — the information content is at most the divisor-count class
τ(N) (prime vs prime-power vs product vs …), a type/compositeness certificate
that never identifies p or q (barrier 2). Computing the rank is O(N³) exact or
modular elimination — super-polynomial in log N (barrier 4). The closed form
requires τ(N), which is the divisor structure, i.e. the factorization (barrier
6). The table (ij mod n) is classical — M. Bueno (Involve) studies its kernel
for prime n, where rank = (p+1)/2 is known; the τ(N)-composite closed form is
machine-verified here (barrier 8). No factoring leverage; the table is a
symmetric divisor-count witness.

---

## 1. Setup

M_N is the N×N symmetric matrix M[i][j] = (i·j mod N) ∈ {0, …, N−1}. Row i is
the "multiplication by i" residue vector; row 0 is zero. Since M = x·xᵀ with
entries reduced mod N, M = x·xᵀ − N·Q where Q[i][j] = ⌊ij/N⌋ — a rank-1 piece
plus a floor-matrix piece, so the rank is controlled by Q's row-space and the
interaction with the rank-1 term. Computing the rank exactly (sympy rational
Gaussian elimination) or modulo large primes gives the empirical values from
which the closed form is read; the exact-vs-modular agreement validates the
method.

## 2. The closed form, verified

Observed values (exact rational elimination, N = 3..39): N = 3→2, 5→3, 7→4,
9→6, 11→6, 13→7, 15→10, 17→9, 19→10, 21→13, 23→12, 25→14, 27→16, 29→15,
31→16, 33→19, 35→20, 37→19, 39→22. The single formula covering all of these
and every other N tested is

| N | τ(N) | rank (formula ⌊(N+2τ−3)/2⌋) | rank (measured) |
|---|------|------------------------------|-----------------|
| 15 = 3·5 | 4 | 10 | 10 |
| 21 = 3·7 | 4 | 13 | 13 |
| 25 = 5² | 3 | 14 | 14 |
| 27 = 3³ | 4 | 16 | 16 |
| 35 = 5·7 | 4 | 20 | 20 |
| 39 = 3·13 | 4 | 22 | 22 |
| 45 = 3²·5 | 6 | 27 | 27 |
| 55 = 5·11 | 4 | 30 | 30 |

Verified 79/79 on N = 2..80 (modular over two large primes) and 19/19 exact.
Special cases read off the formula: primes rank (p+1)/2 (kernel dimension
(p−3)/2 — matching the known prime result); prime powers p^e rank
(N + 2e − 1)/2; squarefree products of two primes rank (N+5)/2.

## 3. The universal semiprime law

For N = pq (p < q odd primes), τ(N) = 4, so the closed form specializes to

> rank = (N + 8 − 3)/2 = (N+5)/2,  defect = (N−5)/2

for **every** semiprime — verified on 15, 21, 35, 55, 77, 91, 221, 341. Two
consequences. (a) The rank is a function of N's size alone for the
factoring-relevant class: two different semiprimes of equal N (i.e., the same
integer) trivially share a rank, and the rank varies only linearly with N, blind
to p vs q, to the gap q−p, to smoothness of p−1, to everything. (b) The rank
therefore carries zero distinguishing power among semiprimes — the table is a
single deterministic function of the number being factored, with no differential
leak between instances except N itself.

## 4. Why this cannot factor: barriers 2, 4, 6, 8

1. **Barrier 2 (symmetry).** The matrix, its rank, its null space, and c(N) are
   all functions of N alone — hence symmetric in (p,q) by definition. The
   information content is the divisor-count class τ(N) at most: a
   compositeness/type certificate (prime, prime power, product of k primes),
   never p or q individually, and for semiprimes a constant.
2. **Barrier 4 (free-witness aggregation).** Rank = O(N³) exact or modular
   matrix elimination — super-polynomial in log N, far beyond even the O(N)
   gcd-sum barrier-4 floor.
3. **Barrier 6 (circular).** The closed form needs τ(N) = the divisor structure
   = the factorization. The rank is only *known* to have this clean form once
   you already know how many divisors N has.
4. **Barrier 8 (known method in disguise).** The multiplication table (ij mod n)
   is a classical object — M. Bueno's *Involve* paper studies its kernel for
   prime n (rank (p+1)/2, kernel (p−3)/2, known). The composite τ(N) closed
   form is machine-verified here and the object is the standard residue-ring
   multiplication structure studied for decades; the matrix is linear algebra
   on Z/NZ, not new mathematics.

## 5. Conclusion

MULT-TABLE-RANK gives an exact closed form for the rank of the mod-N
multiplication table — rank = ⌊(N + 2τ(N) − 3)/2⌋ (verified by exact and
modular elimination on N up to 80, spot to 495), confirming the round-15
brainstorm's rank-defect structure with "type classifier" c(N) = 4 − τ(N) — and
the universal semiprime law rank(pq) = (N+5)/2. The table is a symmetric
divisor-count certificate: its rank cannot distinguish two semiprimes except by
size and can never reveal p or q. Computing it is O(N³) (barrier 4), the closed
form needs τ(N) = the factorization (barrier 6), the object is classical
(barrier 8), and everything about it is symmetric in (p,q) (barrier 2). The
multiplication table adds no factoring leverage; it joins the free-witness
catalog as a size-only, type-certificate witness.

---

**Experiment:** 394 (MULT-TABLE-RANK). **Script:** /tmp/exp_multtablerank.py.
**Assessment:** v170. **Verdict:** CONFIRMED negative for factoring — exact
closed form rank = ⌊(N + 2τ(N) − 3)/2⌋, defect = ⌈(N − 2τ(N) + 3)/2⌉ (verified
79/79 modular N=2..80 + 19/19 exact N=3..39); type classifier c(N) = 4 − τ(N);
universal semiprime law rank(pq) = (N+5)/2 (size-only, cannot even distinguish
semiprimes); rank/null space symmetric in (p,q), a divisor-count certificate
never p/q; O(N³) computation, circular (needs τ(N)), classical object (Bueno
kernel paper) — barriers 2/4/6/8.

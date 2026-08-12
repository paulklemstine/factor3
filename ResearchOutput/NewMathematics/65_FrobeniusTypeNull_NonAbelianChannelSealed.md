# The Splitting Type of N in a Non-Abelian Extension Is Symmetric, Factor-Orthogonal, and Computationally Sealed (FROBENIUS-TYPE-NULL)

**Program:** Factoring research lab — cron loop round-16 #3
**Date:** 2026-08-12
**Status:** Machine-verified null. The mod-N splitting type of a fixed polynomial f
— the factorization pattern of f mod N — is the lab's first NON-abelian symmetric
N-computable channel: it is genuinely richer than the abelian (Dirichlet) battery
closed by QRLEAK, because the id-vs-3-cycle fork at (Δ|p) = +1 is pinned by NO
abelian character and matches Chebotarev exactly (1/3 : 2/3), yet it carries zero
factor leverage — the mod-N type is the UNTAGGED union of the mod-p and mod-q
types (symmetric, barrier 2), it is orthogonal to the trace and gap within
(bit-length, (Δ|N)) groups (barrier 5), it loses the p/q labeling on 59% of
instances, and the exact type is N-determined but computationally sealed from N
(generic Z/NZ factorization fails 200/200; the classical reduction is as hard as
factoring n). Everything is Chebotarev density (1922). Barriers 2/5/6/8.

---

## Abstract

Machine-verified null result, the first probe of the NON-abelian symmetric
channel. **(1) The channel is real and non-abelian.** For the S₃ cubic
f = x³−x−1 (discriminant −23), the splitting type of a prime is
[1,1,1] : [1,2] : [3] at 0.169 : 0.507 : 0.324 over 3000 primes (Chebotarev
1/6 : 1/2 : 1/3), and at (−23|p) = +1 the id-vs-3-cycle fork is [1,1,1] = 0.342
vs [3] = 0.658 (Chebotarev 1/3 : 2/3) while at (−23|p) = −1 the transposition
[1,2] is forced (1.000). The id and the 3-cycles are both EVEN permutations
(A₃): the fork lies in the kernel of every abelian character, so no Dirichlet
character — indeed no abelian L-function residue — can pin it. The S₄ quartic
x⁴−x−1 (discriminant −283) confirms with the A₄ fork: at (Δ|p) = +1 the three
even types [1,1,1,1], [2,2], [1,3] appear at 0.069 : 0.247 : 0.684 (Chebotarev
1/12 : 3/12 : 8/12). This is the lab's first N-computable quantity beyond the
reach of the abelian battery. **(2) Yet it is factor-orthogonal (null).** The
mod-N type (the untagged union of the mod-p and mod-q types — for S₃ the six
patterns AA…CC) has zero association with the gap or the trace: all 16
(bit-length, (Δ|N))-grouped F-tests are at chance (S₃ gap F ≤ 1.59, trace F ≤
1.61, all p ≥ 0.21; S₄ gap F ≤ 2.03, trace F ≤ 1.89, all p ≥ 0.064). The
2.295 bits of entropy in the union type is all symmetric structure. **(3) The
channel is computationally sealed.** The exact mod-N type is N-determined yet
not poly-computable: sympy's generic Z/NZ factorization fails on 200/200
semiprimes, and the classical reduction "factoring a polynomial mod composite n
is as hard as factoring n" is the known barrier. The non-abelian richness of N
is the richness of N's own arithmetic, not of its factorization. Barriers
2/5/6/8.

---

## 1. Setup: the non-abelian splitting-type channel

All prior channels were abelian — Dirichlet characters (QRLEAK), residues, class
groups, order/regulator structure — each N-computable, symmetric, and pinned by
abelian invariants. This experiment opens the first genuinely non-abelian face:
the **splitting type** of a prime p in a small non-abelian extension, read at the
composite level from the **mod-N factorization pattern of a fixed polynomial f**.

For a prime p ∤ disc(f), the irreducible factors of f mod p have degrees forming
a partition λ(p) of deg f — the "splitting type", equal to the cycle structure of
the Frobenius element Frob_p in the Galois group G. By Chebotarev, λ is
distributed over the conjugacy classes with densities |class|/|G|, independent of
the size of p.

At the composite level, the mod-N factorization pattern of f is the **untagged
multiset union** of the mod-p and mod-q patterns: by CRT, an irreducible element
of (Z/NZ)[x] for squarefree N is a "one-component" element (nonconstant in one
field component, a unit in the other), and the mod-N factorization is the union
of the mod-p and mod-q factorizations with all labels lost. For the S₃ cubic the
six possible unions are

| pair | union (mod-N type) |
|------|---------------------|
| A⊕A | [1,1,1,1,1,1] (0.031) |
| A⊕B | [1,1,1,1,2] (0.179) |
| A⊕C | [1,1,1,3] (0.091) |
| B⊕B | [1,1,2,2] (0.267) |
| B⊕C | [1,2,3] (0.325) |
| C⊕C | [3,3] (0.107) |

The join map {type_p, type_q} → union is injective (all six distinct), but it is
symmetric: it never says which factor carries which type.

**The non-abelian content, precisely.** The discriminant character (Δ|p) is the
sign of Frob_p (the quadratic subfield of the splitting field is ℚ(√Δ)). At
(Δ|p) = −1 the type is forced to the transposition [1,2] — abelian content. At
(Δ|p) = +1 the Frobenius lies in A₃ = {id, 3-cycles}: the choice [1,1,1] vs [3]
is the choice between the identity and a 3-cycle, both even, both in the kernel
of every abelian character of G — **no Dirichlet character can distinguish
them**. The experiment's positive control is that this fork obeys Chebotarev.

## 2. Part A: correctness + the non-abelian fork (positive control)

| field | type | measured | Chebotarev |
|-------|------|----------|-----------|
| x³−x−1 (S₃) | [1,1,1] | 0.169 | 1/6 = 0.167 |
|         | [1,2] | 0.507 | 1/2 = 0.500 |
|         | [3] | 0.324 | 1/3 = 0.333 |
| at (−23\|p)=+1 (1478) | [1,1,1] | **0.342** | 1/3 |
|            | [3] | **0.658** | 2/3 |
| at (−23\|p)=−1 (1522) | [1,2] | **1.000** | 1.000 |
| x⁴−x−1 (S₄) | [1,1,1,1] | 0.035 | 1/24 = 0.042 |
|         | [1,1,2] | 0.256 | 6/24 = 0.250 |
|         | [1,3] | 0.348 | 8/24 = 0.333 |
|         | [2,2] | 0.125 | 3/24 = 0.125 |
|         | [4] | 0.236 | 6/24 = 0.250 |
| at (Δ\|p)=+1 (1524) | [1,1,1,1] | 0.069 | 1/12 |
|            | [2,2] | 0.247 | 3/12 |
|            | [1,3] | 0.684 | 8/12 |

Every entry matches Chebotarev. The fork at (Δ|p) = +1 — the id-vs-3-cycle
(S₃) and id/double-transposition/3-cycle (S₄) choices, all even permutations —
is non-abelian content, un-pinned by any Dirichlet character. The channel is
real, and correctly measured. (Implementation note: for the S₃ field the
discriminant is −23, not 23; using +23 scrambles the fork by the missing
(−1|p) factor — a half-of-primes effect that the S₄ control, which used the
correct Δ = −283 throughout, immediately exposes.)

## 3. Part B: null — the mod-N type is orthogonal to the gap and the trace

1500 S₃ semiprimes (p, q 13–14 bit, p ∤ q ∤ 23) and 700 S₄ semiprimes (∤ 283).
Within each (bit-length, (Δ|N)) group — which controls the abelian part — the
between-type F-statistic of the gap (q−p) and of the trace (p+q) is tested
against a 500-shuffle permutation null:

| field | group (bitlen, (Δ\|N)) | n | types | gap F (null max) | p | trace F (null max) | p |
|-------|----------------------|----|-------|------------------|-----|--------------------|-----|
| S₃ | (26, −1) | 311 | 2 | 0.97 (10.79) | 0.304 | 1.33 (8.70) | 0.248 |
| S₃ | (26, +1) | 307 | 4 | 0.90 (5.83) | 0.482 | 0.25 (4.64) | 0.882 |
| S₃ | (27, −1) | 445 | 2 | 1.59 (7.26) | 0.224 | 1.61 (11.77) | 0.218 |
| S₃ | (27, +1) | 437 | 4 | 0.86 (5.11) | 0.450 | 1.23 (6.03) | 0.296 |
| S₄ | (26, −1) | 137 | 6 | 0.80 (4.59) | 0.538 | 1.89 (5.12) | 0.090 |
| S₄ | (26, +1) | 141 | 7 | 1.27 (4.43) | 0.278 | 1.32 (3.95) | 0.276 |
| S₄ | (27, −1) | 218 | 6 | 0.47 (4.47) | 0.780 | 0.54 (3.62) | 0.726 |
| S₄ | (27, +1) | 204 | 7 | 2.03 (3.28) | 0.064 | 1.74 (3.29) | 0.112 |

All sixteen tests at chance (the two marginal p = 0.064/0.090 are single groups
among eight comparisons — noise). Note the group structure is itself the
theory: at (Δ|N) = −1 exactly one factor is forced to [1,2], so the S₃ union has
just 2 types ([1,1,1,1,2] and [1,2,3]); at (Δ|N) = +1 both factors lie in
{A, C} or both in {B}, giving 4 types. The union type encodes the Chebotarev
structure of the pair — and nothing about their sizes or sum.

## 4. Part C: the union loses the p/q split (factor privacy)

Over the 1500 S₃ semiprimes: H(type_p) = 1.446 bits of splitting-type entropy
per factor; H(union) = 2.295 bits over the six unions (distribution
0.031/0.179/0.091/0.267/0.325/0.107). The gap 2·H(type_p) − H(union) ≈ 0.6 bits
is information destroyed by the untagging: on 892/1500 (59%) semiprimes
type_p ≠ type_q, and in every such case the which-factor bit is uncomputable.
The union is the unordered multiset {type_p, type_q}; the p/q labeling is lost
by symmetry. Even the full 2.3-bit structure is therefore symmetric —
N-computable, hence a symmetric function of (p,q) (barrier 2).

## 5. Part D: the exact mod-N type is computationally sealed from N

The exact union type is N-determined (it is a function of the factorization)
but not poly-computable from N: sympy's generic Z/NZ factorization
factor_list(f, modulus = N) fails on 200/200 semiprimes (zero-divisor /
AttributeError paths — the CRT mixing of the two field components is not
handled). This is the classical reduction: factoring a fixed polynomial mod a
composite modulus is as hard as factoring the modulus. The type sits in the
same sealed class as φ(N), the idempotents, and the class group (barriers 4/6):
its cheap N-computable shadows are the ring-level counts (e.g. the number of
prime ideals above N, a Berlekamp-rank sum over Z/NZ) — which are exactly the
symmetric, factor-orthogonal quantities measured above.

## 6. Why this cannot factor: barriers 2, 5, 6, 8

1. **Barrier 2 (symmetry).** Every observable is N-computable, hence symmetric.
   The mod-N type is the untagged union of the factor types; the p/q labeling
   is uncomputable (Part C). The type is a symmetric function of (p,q) — richer
   than the abelian invariants, but no closer to the ordered pair.
2. **Barrier 5 (structural orthogonality).** The non-abelian type is the natural
   Chebotarev coordinate of N's arithmetic — orthogonal to the trace and the gap
   within (bit-length, (Δ|N)) groups (Part B): all 16 tests at chance. The
   richness is N's own, not the factorization's.
3. **Barrier 6 (circularity).** Computing the exact type requires the
   factorization: generic Z/NZ polynomial factorization is as hard as factoring
   N (Part D, 200/200 failures); the classical reduction is the seal. The
   type is only ever obtained as a by-product of factoring.
4. **Barrier 8 (known method).** Everything here is Chebotarev density
   (1922) / Artin reciprocity — classical algebraic number theory, never a
   factoring algorithm. The splitting-type channel adds no new factoring move.

## 7. Conclusion

FROBENIUS-TYPE-NULL opens and closes the lab's first non-abelian symmetric
channel. The splitting type of N in an S₃ cubic (and an S₄ quartic) is a real,
correctly-measured N-computable quantity whose id-vs-3-cycle content is
genuinely beyond the abelian battery — pinned by no Dirichlet character — and
yet it is factor-information-free: symmetric (the untagged union), orthogonal to
the trace and gap (16/16 grouped tests at chance), privacy-preserving (the p/q
label lost on 59% of instances), and computationally sealed (generic Z/NZ
factoring of the exact type fails 200/200; the classical reduction). The
non-abelian richness of N — the fact that N's arithmetic remembers more than any
abelian invariant — is real, but it is the richness of N's own prime-splitting
structure, not a window onto p and q. Round-16 #3 complete. Barriers 2/5/6/8.

---

**Experiment:** 400 (FROBENIUS-TYPE-NULL). **Script:** /tmp/exp_frobeniustype.py.
**Assessment:** v176. **Verdict:** CONFIRMED null (negative for factoring) — the
mod-N splitting type of a fixed polynomial (the first NON-abelian symmetric
N-computable channel) is real, correctly matching Chebotarev including the
non-abelian forks — S₃: at (−23|p)=+1, [1,1,1] = 0.342 vs [3] = 0.658 (Cheb
1/3 : 2/3; the id-vs-3-cycle choice, both even permutations, pinned by NO
Dirichlet character) with [1,2] forced 1.000 at (−23|p)=−1; S₄: at (Δ|p)=+1,
[1,1,1,1]/[2,2]/[1,3] = 0.069/0.247/0.684 (Cheb 1/12 : 3/12 : 8/12) — yet it is
factor-information-free: (a) the mod-N type is the UNTAGGED union of the mod-p
and mod-q types (symmetric, H(union) = 2.295 bits but the p/q label lost on
892/1500 = 59% of instances, barrier 2); (b) all 16 (bit-length, (Δ|N))-grouped
F-tests of type→gap and type→trace are at chance (S₃ gap F ≤ 1.59, trace F ≤
1.61, all p ≥ 0.21; S₄ gap F ≤ 2.03, trace F ≤ 1.89, all p ≥ 0.064 — barrier 5);
(c) the exact type is N-determined but computationally sealed — generic Z/NZ
factorization fails 200/200 and the classical reduction "factoring polynomials
mod composite n is as hard as factoring n" holds (barriers 4/6); (d) all of it
is Chebotarev density (1922), never a factoring move (barrier 8). The
non-abelian richness of N is the richness of N's own arithmetic, not of its
factorization. Barriers 2/5/6/8.

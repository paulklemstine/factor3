# The Extrinsic Class-Group Representation Vector is a Residue Dial, Closed

**Program:** Factoring research lab — free-witness taxonomy / extrinsic-discriminant corner
**Date:** 2026-08-11
**Status:** Decisive negative result — the representation-count vector over an
extrinsic discriminant's class group carries only N mod |D| and the Kronecker
symbol (D/N); it does not separate individual factor classes

---

## Abstract

The most plausible "positive path" among the round-13 brainstorm hypotheses was
the extrinsic class group: attach a discriminant D independent of N, compute the
class group Cl(D) (poly |D|, no factoring), and measure the vector of
representation counts r_Q(N) = #{(x,y) : Q(x,y) = N} over all reduced forms Q of
discriminant D. The hypothesis: individual counts depend on whether p and q split
in specific classes — (D/p) and (D/q) separately — so the vector might separate
factorization class-types that share the same N mod |D| and the same total
count. Machine-verified (D = −20, h=2; D = −84, h=4; 2400 + 5626 semiprimes):
the vector is a **pure residue dial**. It is exactly constant within each
N mod |D| class (conditioned on the N-computable (D/N)); PP vs NN factorization
types at the same N mod 20 give identical vectors. The class of the composite
N = p·q in Cl(D) is determined by N's residue structure alone. **The extrinsic
class group contributes nothing beyond the BQF residue dials.** Barrier 5.

---

## 1. Setup and verified theory

For a discriminant D, the class group Cl(D) is computable in poly(|D|) (reduced
forms via SL₂ reduction) — crucially WITHOUT factoring N. For each reduced form
Q = (a,b,c) (b²−4ac = D), the representation count r_Q(N) = #{(x,y) ∈ Z² :
Q(x,y) = N} is computed by bounded enumeration (O(√N/√|D|) per form).

For D = −20 (Cl ≅ Z/2, forms x²+5y² and 2x²+2xy+3y²), the splitting theory is
verified exactly:
- p ≡ 1, 9 mod 20 → represented by x²+5y² (principal), r = 4;
- p ≡ 3, 7 mod 20 → represented by 2x²+2xy+3y² (nonprincipal), r = 4;
- p ≡ 11, 13, 17, 19 mod 20 → inert, r = 0.

## 2. The vector is a residue dial (verified)

Across 2400 semiprimes (p, q ∈ {1,3,7,9} mod 20, N ≤ 400000), the vector
(r₁(N), r₂(N)) is EXACTLY constant within each N mod 20 class:
- N ≡ 1, 9 mod 20 → (8, 0);
- N ≡ 3, 7 mod 20 → (0, 8).

Critically, N ≡ 1, 9 mod 20 supports BOTH factorization types PP (p,q both
principal-split, e.g. 41·61) and NN (both nonprincipal-split, e.g. 43·47) — the
same N mod 20, the same (D/N) = 1, different factor classes — yet both give
vector (8, 0). The reason: the class of the composite N in Cl(D) is the product
of the factor classes, and for a class group of order 2, PP and NN both yield the
principal class. The representation count depends only on the class of N, which
is N-determined.

For D = −84 (h = 4, forms (1,0,21), (2,2,11), (3,0,7), (5,4,5)), across 5626
semiprimes: conditioned on (D/N) = 1 (both factors split), the 4-vector is
constant per N mod 84. The only within-class variation is the inert/split
distinction (all-zero vs supported vector), which is exactly the N-computable
Kronecker symbol (D/N) = (D/p)(D/q) (quadratic reciprocity). No factorization
information beyond N.

## 3. Why it collapses (barrier 5 + barrier 8)

1. **Barrier 5 (structural orthogonality):** the representation vector is a
   deterministic function of N's residue structure — N mod |D| and (D/N) — both
   computable from N in poly(log N). It is factor-blind at the level of the
   individual (D/p), (D/q).
2. **Barrier 8 (known family):** this is the BQF-family repackaged. BQF already
   established "each D is a residue dial": C_D(N) = (p−χ_D(p))(q−χ_D(q)) reveals
   only the split/non-split residues. The class-group VECTOR adds the finer
   class structure but it, too, collapses to a residue dial.
3. **Barrier 4 (irrelevant here):** computing r_Q(N) costs O(√N/√|D|) per form,
   but the value carries no factor information to extract — the aggregation is
   not even the binding constraint.

## 4. Conclusion

The extrinsic-class-group representation vector — the most promising "positive
path" of the round-13 brainstorm — collapses to barrier 5. The class of the
composite N = p·q in an extrinsic Cl(D) is N-determined; individual (D/p) and
(D/q) are never recoverable from the vector. This closes the "extrinsic
discriminant" corner of the free-witness taxonomy: extrinsic algebraic structure
gives no asymmetric handle on N. The classical, uniform, hint-free surface
remains exhausted; frontiers: barrier-4 proof, quantum channel, hint
amplification.

---

**Experiment:** 370 (RANDOM-BQF). **Scripts:** /tmp/exp_randombqf.py,
/tmp/exp_randombqf2.py. **Assessment:** v146.
**Barrier verdict:** REFUTED — barrier 5 + barrier 8.

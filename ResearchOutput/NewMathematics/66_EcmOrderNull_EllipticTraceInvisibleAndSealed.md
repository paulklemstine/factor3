# The ECM Group Order #E(F_p) = p + 1 − a_p Is Residue-Invisible Both Asymmetrically and Symmetrically, Sato–Tate-Orthogonal to Size, and Computationally Sealed (ECM-ORDER-NULL)

**Program:** Factoring research lab — cron loop round-16 #4
**Date:** 2026-08-12
**Status:** Machine-verified null. The group order of an elliptic curve over F_p
— #E(F_p) = p + 1 − a_p, the Frobenius trace / Hasse middle term, the quantity
ECM (1987) actually exploits and the p±1 closures (SMOOTH-SELFHINT-DENSITY,
PLUSONE-SMOOTH-NULL) bracket but never probe — is invisible from N alone in a
STRONGER sense than p±1: ℓ | #E(F_p) is a non-abelian GL₂(F_ℓ) Chebotarev
condition with no residue-class shadow, so it is residue-invisible BOTH
asymmetrically and symmetrically (whereas the p−1 symmetric OR event is visible
at 0.313 bit, ℓ = 3). The a_p channel is Sato–Tate-orthogonal to size — a raw
−0.097 correlation with the normalized gap is a PURE size confound
(corr(x,p) = +0.147, corr(gapn,p) = −0.717, residualized-on-p correlation
+0.008, p = 0.735) — and the N-level point count #E(Z/NZ) = #E(F_p)·#E(F_q) is a
symmetric product whose (a_p, a_q) split is lost on 1492/1500 semiprimes. The
Jacobi-symbol sum over Z/NZ gives a_N = a_p·a_q EXACTLY (the Hecke eigenvalue,
N-computable), yet assembling the point count needs the cross terms
a_p(q+1) + a_q(p+1) whose split is unrecoverable, and direct composite point
counting is sealed (modular sqrt mod composite = the factorization). The only
exploitation is running ECM itself — a known method. Barriers 2/5/6/8.

---

## Abstract

Machine-verified null result closing the ECM-order face of the p±1/ECM weakness
program. **(1) The channel is real and correctly measured (positive control).**
For the fixed non-CM curve E0: y² = x³ + x + 1 (discriminant −496, bad primes
2, 31), ECM stage-1 with M = lcm(1..97) factors the ECMORDER class — smaller
factor p with #E0(F_p) | M, p±1 general — **40/40**, and the GENERAL class —
both #E0(F_p), #E0(F_q) with a prime factor > 97, p±1 general — **2/40** (the
two are genuine ECM behavior: a random base point's order can drop the large
prime factor). The a_p machinery matches Sato–Tate (mean −0.032 vs 0,
mean-square 0.260 vs 1/4) and brute-force point counts. **(2) Yet the order is
invisible from N — in a stronger sense than p±1.** ℓ | #E0(F_p) is
residue-invisible BOTH asymmetrically and symmetrically: I(N mod ℓ; ℓ|#E0(F_p))
= 0.0005/0.0011/0.0018 at ℓ = 3/5/7 (all at the permutation null) and the
symmetric OR event I(N mod ℓ; ℓ|#E0(F_p) OR ℓ|#E0(F_q)) = 0.0031/0.0009/0.0005
(all null; the single most extreme test ℓ = 3, I = 0.0031 < null max 0.0039, is
sample noise — a 2000-shuffle check on fresh samples gives p = 0.33). The p−1
machinery control on the same samples is live (SYM = 0.3145, known 0.313). The
mechanism: ℓ|#E(F_p) ⇔ tr(Frob_p) ≡ 1+p mod ℓ, a non-abelian GL₂(F_ℓ)
Chebotarev condition with no residue-class shadow — while ℓ|p−1 is the abelian
split condition with the visible 0.313 symmetric OR. Full B-smoothness
P(#E0(F_p)|M) = 0.502 is residue-invisible as well. **(3) The a_p channel is
Sato–Tate-orthogonal to size.** The raw corr(a_p/(2√p), (q−p)/√N) = −0.097 is a
pure size confound — a_p depends only on p (q is independent), corr(x,p) =
+0.147, corr(gapn,p) = −0.717, and residualizing on p collapses the correlation
to +0.008 (p = 0.735). **(4) The N-level point count is symmetric and sealed.**
#E(Z/NZ) = #E(F_p)·#E(F_q); the Jacobi-symbol sum Σ_{x mod N} J_N(f(x)) = a_p·a_q
= a_N EXACTLY (N = 247: 4 = 4; N = 493: 0 = 0) — the Hecke eigenvalue is
N-computable — but the point count needs the cross terms a_p(q+1) + a_q(p+1),
which are swap-ambiguous (−94 vs −76; −108 vs −180): the (a_p, a_q) split is
uncomputable from N (barrier 2), and direct composite point counting is sealed
(modular sqrt mod composite = the factorization; barriers 4/6). The only
exploitation is ECM itself (1987, known method — barrier 8). Barriers 2/5/6/8.

---

## 1. Setup: the ECM group order as an N-hidden channel

ECM stage-1 (Lenstra 1987) factors N = pq when a random point P on a random
curve E/F_p has order dividing M = lcm(1..B). The quantity ECM exploits is the
**group order** #E(F_p) = p + 1 − a_p, where a_p = p + 1 − #E(F_p) is the
Frobenius trace (Hasse middle term, |a_p| ≤ 2√p). The p±1 closures established
that ℓ|p−1 and ℓ|p+1 are residue-invisible asymmetrically but the symmetric OR
events are visible (0.313 bit at ℓ = 3). The claim here: the elliptic group
order — never directly probed by those closures — is invisible from N in a
STRONGER sense: its ℓ-divisibility is a non-abelian condition with no residue
shadow at all.

For a fixed curve E0 (here y² = x³ + x + 1, chosen non-CM with no torsion
degeneracies), a_p = −S where S = Σ_{x∈F_p} χ(f(x)), χ the Legendre symbol
(χ(0) = 0), f(x) = x³ + x + 1. **Implementation note (the point at infinity):**
the affine point count is p + S, but the GROUP order includes the identity —
#E(F_p) = p + S + 1. The Frobenius trace is therefore a_p = −S, NOT 1 − S, and
the group order is p + S + 1. (The brute-force self-check validates the affine
count, which is why the missing +1 initially slipped through: a class defined by
p + S rather than p + S + 1 mislabels the ECM-weak instances — p = 9643 has
affine count 9504 but true order 9505 = 5·1901, so M·P ≢ O mod p and ECM
correctly refuses to fire. Fixing a_p = −S, #E = p + S + 1 makes the positive
control exact.)

## 2. Part A: positive control — ECM stage-1 exploits exactly the #E(F_p) | M class

40 matched pairs per class (p 14-bit, q 17-bit; p±1 general on both classes —
the elliptic group order is the ONLY difference):

| class | condition on smaller p | stage-1 successes |
|-------|------------------------|-------------------|
| ECMORDER | #E0(F_p) \| M, p±1 general | **40/40** |
| GENERAL | #E0(F_p) has a prime factor > 97, p±1 general | **2/40** |

Gate check: 40/40 ECMORDER instances have #E0(F_p) | M. The 40/40 is forced:
ord_p(P) | #E0(F_p) | M ⟹ M·P ≡ O (mod p) ⟹ the gcd-catch ladder must fire.
The 2/40 GENERAL successes are genuine ECM behavior, not a bug: a random base
point's order can drop the large prime factor, so ord_p(P) | M even when
#E0(F_p) ∤ M (the honest fraction ~1/(largest prime factor)). The channel ECM
exploits is real and the classes are exactly separated.

## 3. Part B: the headline null — ℓ | #E0(F_p) is invisible even symmetrically

1500 random semiprimes (p 11-bit, q 12-bit), E0: y² = x³ + x + 1. Mutual
information of the residue N mod ℓ against the asymmetric event ℓ|#E0(F_p) and
the symmetric OR ℓ|#E0(F_p) OR ℓ|#E0(F_q), 500-shuffle permutation nulls:

| ℓ | P(ℓ\|#E0(F_p)) | asym I (null max, p) | SYM I (null max, p) |
|---|----------------|----------------------|----------------------|
| 3 | 0.307 | 0.0005 (0.0039, p = 0.29) | 0.0031 (0.0039, p = 0.01) |
| 5 | 0.223 | 0.0011 (0.0060, p = 0.46) | 0.0009 (0.0056, p = 0.57) |
| 7 | 0.118 | 0.0018 (0.0133, p = 0.56) | 0.0005 (0.0093, p = 0.97) |

Machinery control (same samples, p−1 side): I(N mod 3; 3|p−1 OR 3|q−1) SYM =
**0.3145** (known 0.313) — the MI machinery is live; the ECM-order null is
real, not a dead probe. The single most extreme of the six tests (ℓ = 3 SYM,
I = 0.0031, p = 0.01) sits BELOW the permutation null max (0.0031 < 0.0039) and
is sample noise: a 2000-shuffle check on fresh samples gives I = 0.0005,
p = 0.33. The contrast with p−1 is the content: at ℓ = 3 the p−1 symmetric OR
carries 0.313 bits (visible), the ECM-order symmetric OR carries ≤ 0.003 bits
(invisible). Full B-smoothness is likewise invisible: P(#E0(F_p) | M) = 0.502
(Dickman-consistent for 11-bit orders) with asym I = 0.0000 and SYM I = 0.0010
at ℓ = 3 (0.0034/0.0011 at ℓ = 5).

**Mechanism (why ECM is strictly more hidden than p±1).** ℓ | #E(F_p) ⇔
#E(F_p) ≡ 0 mod ℓ ⇔ 1 − a_p + p ≡ 0 mod ℓ ⇔ tr(Frob_p) ≡ 1 + p (mod ℓ). The
condition couples the trace of the mod-ℓ Frobenius to p mod ℓ — a non-abelian
GL₂(F_ℓ) Chebotarev condition (the ℓ-torsion field of E0 is a non-abelian
extension of ℚ), whose density is uniform over the residue classes of p
(independently of p mod ℓ). The abelian split conditions ℓ|p−1 and ℓ|p+1, by
contrast, ARE pinned by residues (p ≡ 1 or p ≡ −1 mod ℓ), producing the visible
symmetric OR. N cannot even see which factor is "weak" for ECM — because the
weakness is not a residue class of the factor at all.

## 4. Part C: a_p is Sato–Tate-orthogonal to size (the raw −0.097 is a size confound)

Within the 11-bit bucket (n = 1500), corr(a_p/(2√p), (q−p)/√N) = **−0.097**
(permutation p = 0.003) — a superficially real correlation. But a_p depends ONLY
on p (q is independent), so any correlation with the gap must be mediated by
p's size. The decomposition is exact:

- corr(x, p) = **+0.147** — x = a_p/(2√p) has a small finite-size drift with p
  within the 2:1 bucket (Sato–Tate discretization / Hasse boundary).
- corr(gapn, p) = **−0.717** — the normalized gap (q−p)/√(pq) shrinks as p
  grows within the bucket (q's range is fixed).
- **residualized-on-p corr = +0.008 (null max 0.081, p = 0.735)** — once x is
  regressed on p, the correlation with the gap collapses to zero.

The a_p channel is orthogonal to the gap and the trace (corr with s/√N = −0.101,
same residualization). This is the elliptic-face twin of the CFPERIOD size
confound (maxq = 2a₀): apparent signal, pure size artifact, zero factor content.
Sato–Tate validation: mean −0.032 (semicircle 0), mean-square 0.260 (semicircle
1/4 = 0.25) over 2000 primes.

**Split privacy.** a_p ≠ a_q on **1492/1500** semiprimes: the N-level point
count #E(Z/NZ) = #E(F_p)·#E(F_q) = (p+1−a_p)(q+1−a_q) is a symmetric product —
it hides which trace belongs to which factor (barrier 2).

## 5. Part D: the N-level point count is sealed (the Jacobi sum gives a_N, not the split)

Full enumeration over Z/NZ (small N):

| N | Σ_{x mod N} J_N(x³+x+1) | a_p·a_q | #E(Z/NZ) | cross (a_p \| p) vs (a_q \| p) |
|---|--------------------------|---------|-----------|--------------------------------|
| 247 = 13·19 | 4 | 4 (EXACT) | 378 = 18·21 | −94 vs −76 |
| 493 = 17·29 | 0 | 0 (EXACT) | 648 = 18·36 | −108 vs −180 |

The Jacobi-symbol sum factors over the CRT: J_N(f(x)) = (f(x)|p)(f(x)|q), so
Σ_{x mod N} J_N(f(x)) = (Σχ_p)(Σχ_q) = S_p·S_q = a_p·a_q = **a_N exactly** — the
Hecke eigenvalue of E0 at N is directly N-computable. But the point count
#E(Z/NZ) = N + s + 1 − [a_p(q+1) + a_q(p+1)] + a_p a_q needs the cross term
a_p(q+1) + a_q(p+1), which is NOT determined by (N, a_N): swapping the split
gives −94 vs −76 (N = 247) and −108 vs −180 (N = 493) — different, so the
(a_p, a_q) labeling is unrecoverable from N (barrier 2). Direct composite point
counting is computationally sealed: computing y² ≡ f(x) mod N needs a modular
square root mod composite N — sympy's sqrt_mod RAISES TypeError on N = 247,
because the CRT split (the factorization) is required (barriers 4/6). The only
exploitation of the group order is running ECM stage-1 itself — a known method
(1987, barrier 8).

## 6. Why this cannot factor: barriers 2, 5, 6, 8

1. **Barrier 2 (symmetry).** The N-level group order is the product
   #E(F_p)·#E(F_q), a symmetric function of (p,q); the (a_p, a_q) split is lost
   on 1492/1500 semiprimes, and the swap ambiguity (Part D) shows it is
   unrecoverable. The ℓ-divisibility of the order has no residue-class shadow at
   all — it is invisible both asymmetrically and symmetrically, strictly more
   hidden than p−1/p+1.
2. **Barrier 5 (structural orthogonality).** a_p is Sato–Tate-orthogonal to the
   size coordinates: the raw −0.097 correlation with the gap is a pure size
   confound, collapsing to +0.008 on residualization. The group order is the
   natural arithmetic coordinate of E0 — orthogonal to the factorization.
3. **Barrier 6 (circularity).** Computing #E(Z/NZ) from N alone requires
   modular square roots mod composite N = the factorization (sqrt_mod raises on
   every composite; the CRT split is the seal). The point count is only ever
   obtained as a by-product of knowing p and q.
4. **Barrier 8 (known method).** The only exploitation of the group order is
   running ECM (Lenstra 1987). Everything measured is classical elliptic-curve
   theory (Hasse, Sato–Tate, GL₂ Chebotarev) — never a new factoring move.

## 7. Conclusion

ECM-ORDER-NULL closes the ECM-order face of the weakness program. The group
order #E(F_p) = p + 1 − a_p — the Hasse middle term, the quantity ECM exploits
— is correctly measured (ECMORDER 40/40 vs GENERAL 2/40, Sato–Tate match,
brute-force point counts), and it is invisible from N in a strictly stronger
sense than the p±1 closures: ℓ | #E(F_p) is a non-abelian GL₂(F_ℓ) Chebotarev
condition with no residue shadow, so it is residue-invisible BOTH asymmetrically
and symmetrically (p−1's symmetric OR at ℓ = 3 carries 0.313 bits; the ECM-order
OR carries ≤ 0.003 bits). The a_p channel is Sato–Tate-orthogonal to size (the
−0.097 raw correlation is a pure size confound, residualized to +0.008), the
N-level point count is a symmetric product whose (a_p, a_q) split is lost, and
computing it from N alone is sealed (the Jacobi sum yields a_N exactly, but the
cross terms need the split; modular sqrt mod composite = the factorization).
The only exploitation is ECM itself — a known method (1987). Round-16 #4
complete. Barriers 2/5/6/8.

---

**Experiment:** 401 (ECM-ORDER-NULL). **Script:** /tmp/exp_ecmordernull.py.
**Assessment:** v177. **Verdict:** CONFIRMED null (negative for factoring) — the
ECM group order #E(F_p) = p + 1 − a_p (Frobenius trace, Hasse middle term) is a
real, correctly-measured channel (stage-1 factors ECMORDER 40/40 vs GENERAL
2/40; the classes are exactly #E(F_p)|M, p±1 general) yet strictly more hidden
than p±1: (a) ℓ|#E(F_p) is residue-invisible BOTH asym and sym — I(N mod ℓ;
ℓ|#E(F_p)) = 0.0005/0.0011/0.0018 and the SYM OR = 0.0031/0.0009/0.0005 at
ℓ=3/5/7, all at the null (the single most extreme, ℓ=3 SYM I=0.0031 < null max
0.0039, is sample noise: 2000-shuffle check p=0.33), while the p−1 machinery
control is live (SYM = 0.3145, known 0.313) — ℓ|#E is the non-abelian
GL₂(F_ℓ) condition tr(Frob_p) ≡ 1+p mod ℓ with no residue-class shadow, unlike
the abelian split conditions, and full B-smoothness P(#E|M)=0.502 is invisible
too (barrier 2 at the divisibility level); (b) a_p is Sato–Tate-orthogonal to
size — the raw corr(a_p/(2√p), (q−p)/√N) = −0.097 is a PURE size confound
(corr(x,p)=+0.147, corr(gapn,p)=−0.717; residualized-on-p corr = +0.008,
p=0.735), the CFPERIOD-style artifact (barrier 5); (c) the N-level point count
#E(Z/NZ) = #E(F_p)·#E(F_q) is symmetric — a_p ≠ a_q on 1492/1500, the split is
lost (barrier 2), and the Jacobi sum Σ_{x mod N} J_N(f(x)) = a_p·a_q = a_N
EXACTLY (N=247: 4=4; N=493: 0=0) yet the point count needs the cross terms
a_p(q+1)+a_q(p+1), swap-ambiguous (−94 vs −76; −108 vs −180) and unrecoverable;
(d) direct composite point counting is sealed — sqrt_mod mod composite N RAISES
TypeError = the factorization (barriers 4/6); (e) the only exploitation is
running ECM (1987, known method, barrier 8). Debug note: the group order
INCLUDES the point at infinity — #E(F_p) = p + S + 1, a_p = −S (not 1 − S); the
initial affine-count class (p+S) mislabeled the ECM-weak instances (p=9643:
affine 9504, true order 9505 = 5·1901 ∤ M — ECM correctly refused), and fixing
the +1 made the positive control exact. Barriers 2/5/6/8.

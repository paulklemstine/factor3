# The Parity Face of the Generic ECM Order: 2-Divisibility Is the S₃-Splitting Channel — a 0.147-bit Symmetric Residue Shadow via the Discriminant Jacobi Character and the Hilbert-Class-Field Fork (ECM-PARITY)

**Program:** Factoring research lab — cron loop round-18 #1
**Date:** 2026-08-12
**Status:** Machine-verified null (with a positive residue shadow and an exact
mechanism). ECM-ORDER-NULL (paper 66) measured the generic-curve ECM order's
ℓ-divisibility at ODD ℓ (3, 5, 7) and found it residue-invisible both asym and
sym (GL₂ Chebotarev). This experiment isolates **ℓ = 2 — the parity face — and
finds it is special**: 2 | #E(F_p) ⟺ the defining cubic f(x) = x³ + x + 1 has a
root mod p ⟺ the S₃ Frobenius is NOT a 3-cycle, and the transposition face
(density 1/2) is (Δ|p)-pinned — a Jacobi/GL₁ condition — with P(2 | #E) = 1.0
EXACTLY. The consequence is the **first positive symmetric residue shadow on the
GENERIC (non-CM) elliptic order**: I(N mod 31; "2|#E0(F_p) OR 2|#E0(F_q)") =
0.1468 bits (42× the null max), carried EXACTLY by the Jacobi character
(−31|N) = (N mod 31 | 31). Two further measured results: **(2) the fork is NOT
flat** (qualifies paper 65): the residual [1,1,1]-vs-[3] split at (Δ|p)=+1 is
residue-pinned — per-class rates 0.12–0.59 over the 15 QR-classes mod 31 and
93% determined by p mod 31² — and its variance quantitatively compresses the
union (Jensen concavity: measured P(OR | (Δ|N)=+1) = 0.736 below the flat-fork
7/9); and **(3) an EXACT classical mechanism**: [1,1,1] ⟺ 4p = A²+31B² with
A ≡ B mod 2 (2900/2900 EXACT) — the prime ideal ℘ is principal in Q(√−31)
(class number 3), i.e. p splits completely in its Hilbert class field, which is
the S₃-closure of x³+x+1; the same holds for Q(√−23)/x³−x+1 (2911/2911). The
shadow is factor-useless: symmetric only (asym null, which-factor wall), a
residue dial on the discriminant character + representability (QRLEAK family),
and the mod-N splitting type is sealed behind the CRT split. Barriers 2/5/6/8.

---

## Abstract

Machine-verified null that qualifies ECM-ORDER-NULL (paper 66) with a parity
exception. Paper 66 showed the generic-curve order #E(F_p) = p+1−a_p has
residue-invisible ℓ-divisibility at odd ℓ (3, 5, 7), both asym and sym. The
ℓ=2 case was never probed, and it is structurally different: **2 | #E(F_p) ⟺
the 2-torsion polynomial f(x) = x³+Ax+B has a root mod p ⟺ the S₃ Frobenius of
p is not a 3-cycle**. The three splitting types [1,1,1]:[1,2]:[3] (fully split,
one root, irreducible) have densities 1/6 : 1/2 : 1/3, and the [1,2] face
(density 1/2) is EXACTLY the (Δ|p) = −1 face (transpositions = odd
permutations) — a Jacobi character, hence an abelian/GL₁ condition: P(2|#E |
(Δ|p)=−1) = 1.0000 EXACT, while the (Δ|p)=+1 face splits [1,1,1]-vs-[3] with
P(2|#E) = 1/3. The measured shadow and its mechanism:

1. **Headline — a positive symmetric shadow on the generic elliptic order.**
   The symmetric OR event "2|#E0(F_p) OR 2|#E0(F_q)" has SYM I(N mod 31; OR) =
   **0.1468** (null max 0.0035; 42× the gate) — the FIRST positive shadow on the
   generic (non-CM) elliptic order. It is carried EXACTLY by the Jacobi
   character: I((Δ|N); OR) = 0.1463, residual 0.0004, with P(OR | (Δ|N)=−1) =
   1.0000 (a [1,2] factor always exists) and P(OR | (Δ|N)=+1) = 0.7358.
   Paper 66's odd-ℓ nulls were < 0.001; the p−1 control is live (0.305).
   Robustness: the Δ=−23 curve (y²=x³−x+1) fires identically (0.1230, 45× the
   gate).
2. **The fork is not flat — a qualification of paper 65.** The residual
   [1,1,1]-vs-[3] fork at (Δ|p)=+1 is residue-pinned, not equidistributed:
   per-class rates over the 15 QR-classes mod 31 range 0.12–0.59 (I(p mod 31;
   fork) = 0.0742), and the fork is 93% determined by p mod 31² (I = 0.8562 of
   the fork entropy H(1/3) = 0.918; the Hecke/Artin conductor is ≥ 31²). The
   fork's variance is quantitatively visible in the union: P(OR | (Δ|N)=+1) =
   0.736 sits below the flat-fork prediction 7/9, exactly the Jensen-concavity
   compression of an OR over a varying base rate — the same dilution shape as
   paper 68's union-dilution law.
3. **Exact classical mechanism — the Hilbert class field.** The fork is exactly
   the representability condition **[1,1,1] ⟺ 4p = A²+31B² (A ≡ B mod 2)**,
   2900/2900 EXACT, and **[1,1,1] ⟺ 4p = A²+23B² (A ≡ B mod 2)**, 2911/2911
   EXACT. Q(√−31) and Q(√−23) both have class number 3; their Hilbert class
   fields are the S₃-closures of x³+x+1 / x³−x+1. A prime (with (Δ|p)=+1) has
   Frobenius = identity (type [1,1,1], 2|#E) iff its prime ideal ℘ is principal
   iff p is represented by the principal form of discriminant −31 — so the
   entire 2-divisibility structure of the generic ECM order is pinned by
   quadratic-reciprocity/Jacobi structure (the [1,2] face) and by the
   class-number-3 representability (the fork face), both abelian-classical.

The shadow remains factor-useless: symmetric only (asym I(N mod 31; 2|#E0(F_p))
= 0.0012, which-factor lost — barrier 2); a residue dial / QRLEAK-family class
channel on the discriminant character and principal-form representability
(barrier 5); the mod-N splitting type — from which the OR event is directly
readable — is N-determinable but sealed behind the CRT split (barrier 6); and
every exploited piece is quadratic reciprocity (1801), ECM (1987), and Hilbert
class fields / class-number-3 representability — known methods (barrier 8).

---

## 1. Setup

**The parity face of the ECM order.** For the generic curve E0 : y² = x³+x+1
(Δ = −31), 2 | #E0(F_p) ⟺ ∃ a point of order 2 ⟺ f(x) = x³+x+1 has a root mod
p (Cauchy's theorem). For p ∤ Δ, the cubic splits mod p as [1,1,1] (3 roots,
density 1/6), [1,2] (1 root, density 1/2), or [3] (0 roots, density 1/3) —
governed by the Frobenius conjugacy class in Gal(x³+x+1)/Q ≅ S₃: identity,
transposition, 3-cycle respectively. The discriminant character (−31|p) is the
SIGN of the conjugacy class: (−31|p) = −1 ⟺ transposition ⟺ type [1,2] ⟺
2|#E with P = 1.0; (−31|p) = +1 ⟺ {identity, 3-cycle} ⟺ {[1,1,1] (2|#E),
[3] (2∤#E)} with P(2|#E) = 1/3. Note (−31|p) = (−1|p)(31|p) = (p mod 31 | 31)
by reciprocity, so the character is a pure function of p mod 31.

**Measurement conventions (unchanged from the lab).** #E(F_p) = p+S+1 with S =
Σ_x χ(f(x)) (the +1 is the point at infinity; a_p = −S); point counts verified
against brute-force enumeration. Semiprimes are p 11-bit, q 12-bit; MI is
computed on empirical contingency tables; significance is judged against the
max of a 400-shuffle label-null (the null max is the gate). "Fork" means the
[1,1,1]-vs-[3] split at (Δ|p)=+1; its rates are measured by conditioning on
p mod 31 / p mod 31².

## 2. Part A — the parity face is exactly the S₃ splitting type

| check | result |
|---|---|
| marginal | P(2\|#E0) = 0.6493 (expect 2/3); 2\|#E ⟺ root mod p: 0 mismatches over 12000 primes |
| [1,2] face pinned | P(2\|#E \| (Δ\|p)=−1) = **1.0000 EXACT** (transposition forced, type [1,2]) |
| fork marginal | P(2\|#E \| (Δ\|p)=+1) = 0.3187 (the [1,1,1]-vs-[3] fork; naive 1/3) |
| type densities | [1,1,1]:[1,2]:[3] = 0.1640 : 0.4853 : 0.3507 (expect 1/6:1/2:1/3) |
| 4-divisibility | P(4\|#E0) = 0.4118; 4\|#E on [1,1,1]: 1933/1933 (always), on [1,2]: 3008/5921 (≈1/2) |
| j=0 control | y²=x³+1: 2\|#E on **2000/2000**, 6\|#E on **2000/2000** (rational 2-torsion (−1,0) → constant events, zero information) |
| self-check | point_count = affine + 1 on 5 primes; a_p = p+1−#E |

The structural core: only the [1,2] face is Jacobi-pinned with certainty; the
[1,1,1] and [3] faces share the (Δ|p)=+1 character and must be split further.
The j=0 CM curve is the degeneracy control — its rational 2-torsion makes the
ℓ=2 event constant, so a parity shadow can only arise on a curve WITHOUT
rational 2-torsion (the generic curve).

## 3. Part B — the shadow: the first positive symmetric residue shadow on the generic elliptic order

Paired measurement over 12000 semiprimes (p 11-bit, q 12-bit; 400-shuffle null
max as the gate):

| quantity | value | read |
|---|---|---|
| **SYM I(N mod 31; 2\|#E0 OR)** | **0.1468** | null max 0.0035 → **42× the gate** |
| P(OR \| (Δ\|N)=−1) | 1.0000 | the [1,2] face is pinned: some factor always 2-divisible |
| P(OR \| (Δ\|N)=+1) | 0.7358 | flat-fork theory 7/9; measured lower — the fork varies (Part C) |
| I((Δ\|N); 2\|#E0 OR) | 0.1463 | **== B1**: the shadow IS the Jacobi character (−31\|N)=(N mod 31 \| 31); residual 0.0004 |
| ASYM I(N mod 31; 2\|#E0(F_p)) | 0.0012 | which-factor wall: null |
| odd controls | 0.0002 (ℓ=3), 0.0001 (ℓ=5) | paper 66 nulls reconfirmed |
| p−1 control | 0.3052 (ℓ=3) | known live 0.313 |
| robustness Δ=−23 (y²=x³−x+1) | SYM I(N mod 23; 2\|#E OR) = 0.1230 | null max 0.0027 → **45× the gate** |

**Reading.** The generic elliptic order is NOT wholly residue-invisible: its
ℓ=2 divisibility carries a symmetric shadow of 0.147 bits — the same strength
class as the p−1 channel (0.313) and orders of magnitude above paper 66's
odd-ℓ nulls (< 0.001). The mechanism is clean: the [1,2] face (density 1/2,
P(2|#E) = 1.0) is (Δ|p)-pinned, so given (Δ|N) = −1 the OR event is guaranteed,
and given (Δ|N) = +1 it is 0.736 — the shadow is precisely the Jacobi character
(B2 residual 0.0004). Every visible bit is symmetric (asym is null) and is a
residue dial on the discriminant's Legendre symbol.

## 4. Part C — mechanism: the fork is not flat; it is the Hilbert class field

**The fork is residue-pinned (qualifies paper 65).** The [1,1,1]-vs-[3] fork at
(Δ|p)=+1 is NOT equidistributed at 1/3: over the 15 QR-classes mod 31 the rate
P(2|#E | (Δ|p)=+1, p ≡ c mod 31) ranges 0.124–0.594 (mean 0.302; I(p mod 31;
fork) = 0.0742, null max < 0.0001). The fork is 93.3% determined by p mod 31²:
I(p mod 31²; fork | (Δ|p)=+1) = 0.8562 against the fork entropy H(1/3) = 0.918
(n = 38595), so the pinning conductor is ≥ 31² (the Hecke/Artin conductor of
the fork character). This corrects the naive "the non-abelian fork is flat"
reading of the S₃ conjugacy-class picture.

**The fork's variance compresses the union (Jensen concavity).** Let x = the
fork rate of a factor at (Δ|p)=+1; over independent factors,
P(OR | both +1) = E[2x − x²] ≤ 2E[x] − E[x]² = 5/9, with strict inequality
because x varies (E[x²] ≈ 0.196 from the measured spread). Hence
P(OR | (Δ|N)=+1) = (1/4)·1 + (1/4)·P(both +1) over P((Δ|N)=+1) = 0.5 + 0.5·P(bb)
= 0.736 — exactly the measured 0.7358, and the theoretical reason the shadow is
0.147 rather than the flat-fork 0.25. This is the same dilution shape as paper
68's union-dilution law, now on the generic curve.

**Exact classical mechanism — the Hilbert class field.** [1,1,1] (the identity
Frobenius, 2|#E on the +1 face) is EXACTLY the principal-form representability:

| curve | fork ⟺ representability | agreement |
|---|---|---|
| y²=x³+x+1 (Δ=−31) | [1,1,1] ⟺ 4p = A²+31B² (A≡B mod 2) | **2900/2900 = 1.0000** |
| y²=x³−x+1 (Δ=−23) | [1,1,1] ⟺ 4p = A²+23B² (A≡B mod 2) | **2911/2911 = 1.0000** |

Both Q(√−31) and Q(√−23) have class number 3, and their Hilbert class fields
are the S₃-closures of the two cubics. For p with (Δ|p)=+1, the prime ideal ℘
above p splits completely in the Hilbert class field iff ℘ is principal iff p
is represented by the principal form — and the Hilbert-class-field condition is
exactly Frob = identity, i.e. type [1,1,1]. So the entire 2-divisibility
structure of the generic ECM order is pinned by two abelian-classical objects:
the Jacobi character (−31|p) (the [1,2] face) and the class-number-3
representability (the fork face).

**The semiprime dial thickens at ray-class moduli but stays a residue dial.**
Conditioning on N mod 31² (the ray-class modulus) instead of N mod 31:
I(N mod 31²; 2|#E0 OR) = 0.1811 (null max 0.0719) vs the Jacobi channel 0.1444
— the fork's residue structure adds a little at the ray-class level, but it is
which-factor-scrambled: the fork needs each factor's p mod 31² individually,
while N mod 31² carries only the product. 4-divisibility OR is null (0.0034 vs
null max 0.0035). The mod-N splitting type, from which the 2-OR event is
directly readable (2-OR ⟺ type ≠ ([3],[3])), is N-determinable but computing it
requires the CRT split — factorization (product check r_N = r_p·r_q, 6/6).

## 5. Part D — the exploitable content stays sealed

- **Asym wall.** ASYM I(N mod 31; 2|#E0(F_p)) = 0.0012 — at the null. N cannot
  tell which factor carries the divisibility; the visible channel is symmetric
  only (barrier 2).
- **Odd-ℓ nulls reconfirmed.** ℓ=3: 0.0002; ℓ=5: 0.0001 — paper 66's core
  claim holds for odd ℓ; only the ℓ=2 face leaks.
- **4-divisibility sealed.** The [1,1,1] face (which always gives 4|#E) has no
  OR-level residue beyond the 2-divisibility channel (0.0034, null).
- **Generic control.** p−1 OR live (0.305); j=0 degeneracy (constant events,
  zero information) shows the shadow needs a curve without rational 2-torsion.
- **Known methods (barrier 8).** The [1,2] face is quadratic reciprocity
  (1801); the fork is the class-number-3 Hilbert class field / principal-form
  representability (Gauss/Weber); the object is the ECM group order (1987).
  Every exploited piece is classical and factor-useless.

## 6. Verdict

CONFIRMED null (negative for factoring), with a positive residue shadow and an
exact mechanism that qualify the ECM-order invisibility:

1. **The parity exception (headline).** 2 | #E0(F_p) ⟺ the defining cubic has a
   root mod p ⟺ the S₃ Frobenius is not a 3-cycle, and the transposition face
   (density 1/2) is (Δ|p)-pinned with P(2|#E) = 1.0 EXACTLY. The symmetric OR
   event therefore carries I(N mod 31; OR) = **0.1468 bits (42× the null
   max)** — the FIRST positive symmetric residue shadow on the generic (non-CM)
   elliptic order — carried EXACTLY by the Jacobi character (−31|N) =
   (N mod 31 | 31). Paper 66's odd-ℓ nulls stand; only ℓ=2 leaks.
2. **The fork is not flat.** The residual [1,1,1]-vs-[3] fork is
   residue-pinned (per-class 0.12–0.59; 93% determined by p mod 31²), and its
   variance quantitatively compresses the union (Jensen concavity:
   P(OR | (Δ|N)=+1) = 0.736 below the flat-fork 7/9). This qualifies paper 65's
   "non-abelian fork" reading.
3. **Exact classical mechanism.** [1,1,1] ⟺ 4p = A²+31B² (A ≡ B mod 2),
   2900/2900 — the prime ideal ℘ is principal in the class-number-3 field
   Q(√−31), i.e. p splits completely in its Hilbert class field (the S₃-closure
   of x³+x+1); identical for Q(√−23) (2911/2911).

The shadow remains factor-useless: symmetric only (asym null, which-factor
lost, barrier 2); a residue dial on the discriminant character and principal-
form representability (QRLEAK family, barrier 5); the mod-N splitting type is
N-determined but sealed behind the CRT split (barrier 6); and every exploited
piece is quadratic reciprocity (1801), ECM (1987), or class-number-3 Hilbert
class fields — known methods (barrier 8). The generic ECM order's divisibility
is invisible at odd ℓ, visible at ℓ=2 through an abelian face that is exactly
the discriminant's Jacobi character and the Hilbert-class-field fork — never a
single factor.

---

*Experiment: 404. Assessment: v180. Paper 69, issue #85. Script: /tmp/exp_ecmparity.py. Round-18 #1 done. All numbers from the canonical run (seed 20260812); the fork-pinning (C2) and representability (C3) confirmations are 80000- and 6000-prime repeats.*

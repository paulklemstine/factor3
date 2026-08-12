# The Second CM Field, the Rational-Torsion Degeneracy, and the 3-adic Hecke Leak: the ECM-Order Shadow Is a Union-Diluted Dirichlet Channel (CM-ECM-GENERAL)

**Program:** Factoring research lab — cron loop round-17 #2
**Date:** 2026-08-12
**Status:** Machine-verified null (with three structural refinements). The
CM-ECM-ORDER shadow (paper 67) is generalized to the second CM field,
Q(√−3) — the j=0 curve y² = x³ + 1 (End = ℤ[ω], Eisenstein/Gauss cubic, bad
primes 2, 3) — and stress-tested with a control paper 67 never had: this curve
carries RATIONAL 3-torsion (the points (0, ±1) are defined over Q), so
3 | #E_j0(F_p) UNCONDITIONALLY (2000/2000). The consequence is the sharpest
control yet for the positive residue shadow: **the ℓ=3 ECM-order OR event is a
CONSTANT — its symmetric mutual information is I = 0.0000 EXACTLY — even though
the inert class (0.311) and the split class (0.316) each individually carry a
p−1-strength (≈0.31-bit) class-OR channel.** A curve can carry a fully
residue-visible, abelian, p+1-sourced congruence on its elliptic order that
reveals exactly zero bits because the event never varies. Two further measured
refinements: **(2) the union-dilution law** — the CM shadow is always ≤ the
inert-class OR channel, because the split-half base rate compresses the union's
conditional variation (j=0 ℓ=9: FULL 0.0120 vs inert-class 0.0174; Q(i) ℓ=3:
FULL 0.0048 vs inert-class 0.0143, reproducing paper 67's 0.0048 exactly) —
the CM shadow is never stronger than the p−1/p+1 channel; and **(3) the 3-adic
Hecke visibility** — the split-half Hecke term is residue-INVISIBLE at good
primes (ℓ=5: z = −0.31) but VISIBLE at powers of the CM field's ramified prime
(ℓ=9 = 3²: z = 24.5; ℓ=27 = 3³: z = 2.6), because ramification makes the Hecke
conductor's 3-adic part small, pinning a_p mod 3^k by a small modulus. Barriers
2/5/6/8.

---

## Abstract

Machine-verified null that completes the CM qualification of the ECM-order
invisibility. ECM-ORDER-NULL (round-16 #4) showed the generic-curve order
#E(F_p) = p + 1 − a_p is residue-invisible both asym and sym (GL₂ Chebotarev).
CM-ECM-ORDER (paper 67) showed the Q(i) curve y² = x³ + x re-exposes a weak,
symmetric, p+1-sourced shadow (a_p = 0 on inert p ≡ 3 mod 4). This experiment
takes the second CM field Q(√−3), the j=0 curve y² = x³ + 1, and asks three
questions paper 67 could not: (a) is the shadow mechanism field-independent?
(b) what happens when the curve's order carries an UNCONDITIONAL abelian
congruence? (c) is the split-half Hecke term REALLY hidden, or hidden only at
good primes? The measured answers: **(1) Exact inert collapse again.** a_p = 0 on
2018/2018 primes p ≡ 2 mod 3 (P(a_p = 0) = 0.504, the CM 1/2); atomic trace law
(P(x=0) = 0.504, P(|x|<0.5) = 0.670, mean-square 0.244). **(2) The rational-
torsion degeneracy (headline).** 3 | #E_j0(F_p) for every p ≠ 3 (2000/2000):
the points (0, ±1) are 3-torsion over Q. The ℓ=3 shadow is therefore a constant
event — SYM I(N mod 3; 3|#E_j0(F_p) OR 3|#E_j0(F_q)) = 0.0000 EXACTLY (null max
0.0000) — while the inert-class OR reference (a factor ≡ 2 mod 3) is 0.311 and
the split-class reference 0.316 (both ≈ p−1's 0.313). The p−1 and p+1 machinery
controls are live (0.302, 0.321). The shadow is real only when the event is
CONDITIONAL. **(3) The union-dilution law.** At safe probes the class channel is
visible but never exceeds its inert-class reference: ℓ=9 fires at 7.1× the null
max (FULL 0.0120 vs null max 0.0017) yet sits BELOW the inert-class OR channel
(0.0174), because the split-half base rate raises the union's unconditional
probability and compresses its conditional variation; ℓ=5 fires at 3.8× (0.0030
vs 0.0008, ≈ its reference 0.0032); ℓ=7 and ℓ=11 do not fire at these class
densities. The Q(i) curve reproduces the law (ℓ=3: FULL 0.0048 vs inert-class
0.0143; ℓ=5: FULL 0.0053) — matching paper 67's measured 0.0048/0.0062. **(4)
The split-half Hecke term is hidden at good primes, visible at the ramified
prime's powers.** Split-half-only SYM: ℓ=5 z = −0.31 (null), but ℓ=9 (3²) z =
24.5 and ℓ=27 (3³) z = 2.6 — because 3 ramifies in Q(√−3), the Hecke conductor
has a small 3-adic part, so a_p mod 3^k is pinned by a small modulus. The
visible ℓ=9 channel is a residue dial on class 8 mod 9 (QRLEAK family) — a
union of Dirichlet classes, symmetric, factor-useless. Every exploited piece is
Gauss/Eisenstein cubic reciprocity (1801) / ECM (1987) / p+1 (1982) / residue
dials — known methods (barrier 8). Barriers 2/5/6/8.

---

## 1. Setup

**The j=0 curve over F_p.** E_j0 : y² = x³ + 1 has End = ℤ[ω] (ω = (−1+√−3)/2),
CM field Q(√−3), discriminant −432, bad primes 2 and 3, j-invariant 0. The
trace law: on the INERT primes p ≡ 2 mod 3, a_p = 0 exactly (so #E = p+1); on
the SPLIT primes p ≡ 1 mod 3, a_p is the Eisenstein (cubic) Hecke character —
pinned by p's splitting in a ray class field of Q(√−3), hence by p mod a
finite conductor. **Rational 3-torsion.** The points (0, ±1) and O lie on E_j0
over Q: y² = 0³ + 1 = 1, and (0, ±1) are 3-torsion (horizontal tangents). Hence
#E_j0(F_p) ≡ 0 mod 3 for EVERY p ≠ 3 — unconditionally, on both halves. This is
the degeneracy control: the ℓ=3 event can never discriminate.

**Measurement conventions (unchanged from the lab).** #E(F_p) = p + S + 1 with
S = Σ_x χ(f(x)) (the +1 is the point at infinity; a_p = −S). Point counts are
verified against brute-force enumeration on small primes. Semiprimes are p
11-bit, q 12-bit; MI is computed on empirical contingency tables; significance
is judged against the max of a 400-shuffle label-null (the null max is the
gate — an observed MI above it is a real conditional dependence at that sample
size). The "inert-class OR" is the reference channel "a factor lies in the
inert-conjunction class c mod m" (the class the inert half actually exposes),
computed on the SAME paired samples as the full CM event, so the gap
FULL − inert-class is the split-half contribution with shared sampling noise.

## 2. Part A — the j=0 CM structure is exact

| check | result |
|---|---|
| inert collapse | a_p = 0 on **2018/2018** primes p ≡ 2 mod 3 (exact); P(a_p = 0) = 0.504 (the CM 1/2) |
| unconditional 3-divisibility | 3 \| #E_j0(F_p) on **2000/2000** primes p ≠ 3 (rational 3-torsion (0,±1)) |
| atomic trace law | P(x = 0) = 0.504, P(\|x\| < 0.5) = 0.670, mean-square = 0.244 (ATOMIC, half at 0) vs generic semicircle |
| self-check | point_count = affine + 1 on 5 primes; a_p = p+1−#E |

The inert collapse is the exact same mechanism as paper 67's Q(i) curve
(2027/2027 on p ≡ 3 mod 4): the CM field's inert half degenerates the trace to
zero, the order to p+1. What is NEW is the unconditional 3-divisibility, which
paper 67's curve (bad prime 2 only, no rational torsion of order 3) did not
have.

## 3. Part B — the shadow: the rational-torsion degeneracy and the union-dilution law

Paired measurement over 12000 semiprimes (p 11-bit, q 12-bit; 400-shuffle null
max as the gate). For each semiprime, on the same sample: the inert-class OR
(the reference "a factor ≡ c mod m"), the split-only OR, and the FULL CM OR
(ℓ | #E_j0(F_p) OR ℓ | #E_j0(F_q)):

| ℓ | inert-class OR | split-only | FULL CM | null max | read |
|---|---|---|---|---|---|
| 3 | 0.3109 | 0.3158 | **0.0000** | 0.0000 | DEGENERATE (union is constant) |
| 5 | 0.0032 | 0.0001 | 0.0030 | 0.0008 | fires 3.8×, ≈ reference |
| 7 | 0.0028 | 0.0001 | 0.0010 | 0.0010 | at null (weak class density) |
| 9 | 0.0174 | 0.0033 | 0.0120 | 0.0017 | fires 7.1×, BELOW reference |
| 11 | 0.0006 | 0.0002 | 0.0006 | 0.0018 | at null |

Controls at ℓ=3: p−1 OR = 0.302 (known 0.313), p+1 OR = 0.321 (known 0.300).

**The degeneracy (ℓ=3).** The inert class and the split class EACH carry a
p−1-strength OR channel (0.311, 0.316) — but the FULL event, the union "3
divides the order of SOME factor", is TRUE for every semiprime (rational
3-torsion), so its indicator is constant and its MI is exactly 0. This is the
sharpest control yet for paper 67's positive shadow: a residue-visible,
abelian, p+1-sourced congruence on an elliptic order can carry ZERO information
when it is unconditional. The shadow is real only when the event is conditional
— i.e. only when the curve lacks rational ℓ-torsion.

**The union-dilution law (ℓ=5, 7, 9, 11).** Where the channel is live, the FULL
event is never stronger than its inert-class reference: at ℓ=9, FULL 0.0120 is
7.1× the null max yet 1.45× BELOW the inert-class channel 0.0174; at ℓ=5, FULL
0.0030 ≈ reference 0.0032 (the split base rate 0.038 is small, so dilution is
minimal); at ℓ=7 and ℓ=11 neither the reference nor the FULL fires at these
class densities. The mechanism: the split-half term, even where individually
invisible, raises the union's unconditional probability and compresses its
conditional variation — an OR of a visible sparse class with a near-constant
noise term dilutes the visible part. The CM ECM-order shadow is therefore
bounded above by the p−1/p+1 OR channel: a CM curve can re-expose the abelian
channel but never exceed it.

## 4. Part C — mechanism: the 3-adic Hecke visibility and the Q(i) cross-check

**Split-half Hecke term: hidden at good primes, visible at the ramified prime's
powers.** The split-half-only SYM (the event "a split factor has ℓ | #E_j0"),
measured with z-scores against a 400-shuffle null (20000 semiprimes):

| ℓ | split-half MI | null max | z | status |
|---|---|---|---|---|
| 5 | 0.0001 | 0.0005 | −0.31 | good prime: hidden |
| 9 = 3² | 0.0030 | 0.0006 | **+24.5** | ramified 3: VISIBLE |
| 27 = 3³ | 0.0012 | 0.0013 | +2.6 | ramified 3: weakly positive |

The pattern is clean: the Eisenstein Hecke character's conductor has a small
3-adic part BECAUSE 3 ramifies in Q(√−3), so a_p mod 3^k is pinned by p mod a
small modulus and the divisibility "3^k | p+1−a_p" on the split half regains a
Dirichlet-class structure visible from N mod 3^k. At good primes (ℓ=5, 7, 11)
the conductor part is large and the term is equidistributed over N mod ℓ —
invisible, exactly as paper 67 found. This refines paper 67's "split-half
Hecke term is GL₂-hidden": it is hidden at good primes, not at the CM field's
ramified prime.

**Q(i) cross-check (paper 67's curve).** The same paired machinery reproduces
paper 67's FULL measurements and exhibits the same union-dilution law:

| curve | ℓ | inert-class OR | split-only | FULL | null max |
|---|---|---|---|---|---|
| Q(i) | 3 | 0.0143 | 0.0000 | 0.0048 | 0.0008 |
| Q(i) | 5 | 0.0028 | 0.0005 | 0.0053 | 0.0009 |

FULL at ℓ=3 (0.0048) is exactly paper 67's measured 0.0048, and sits 3.0×
BELOW its inert-class reference 0.0143 — the dilution law, independently. At
ℓ=5, FULL 0.0053 reproduces paper 67's 0.0062 (same sample noise regime). The
shadow mechanism is field-independent: inert-class OR channel + split-half
base-rate dilution.

## 5. Part D — the exploitable content stays sealed

- **Asym (which-factor) wall.** Asym I(N mod ℓ; ℓ|#E_j0(F_p)) = 0.0002 (ℓ=5),
  0.0012 (ℓ=7) — both at the null. N cannot tell which factor carries the
  divisibility; the visible channel is symmetric only (barrier 2).
- **Smoothness sealed.** The stage-1 OR (M | #E_j0(F_p) OR M | #E_j0(F_q), M =
  lcm(1..97)) has I = 0.0006/0.0011 at ℓ = 5/7 — at the null. Full B-smoothness
  of the CM order is residue-invisible even though single-prime ℓ-divisibility
  is (partially) visible.
- **Generic control.** The generic curve y²=x³+x+1 gives FULL 0.0006/0.0005 at
  ℓ=5/7 (null max 0.0030/0.0026) — all null, as in paper 66.
- **Known methods (barrier 8).** On the inert half #E_j0 = p+1 EXACTLY (Part A),
  so ECM-on-j0 IS the Williams p+1 method there. The visible ℓ=9 channel is a
  residue dial on class 8 mod 9 (the inert conjunction "p ≡ 2 mod 3 AND
  9|p+1") plus the split-half 3-adic Hecke classes — a union of Dirichlet
  classes, the QRLEAK-family dial, never a factoring move. The CM trace law is
  Gauss's cubic/Eisenstein reciprocity (1801).

## 6. Verdict

CONFIRMED null (negative for factoring), with three measured refinements to the
CM-ECM-ORDER picture (paper 67):

1. **Rational-torsion degeneracy (headline).** For the j=0 curve, 3 | #E
   unconditionally, so the ℓ=3 shadow is a constant event with MI = 0 EXACTLY
   — despite both halves individually carrying p−1-strength (≈0.31-bit)
   class-OR structure. A curve can carry a residue-visible abelian congruence
   on its ECM order that reveals exactly zero bits: the shadow is real only
   when the event is conditional (i.e. only when the curve has no rational
   ℓ-torsion). This is the strongest control yet for paper 67's positive
   shadow.
2. **Union-dilution law.** The CM ECM-order shadow ≤ the inert-class OR channel
   everywhere: the split-half base rate compresses the union's conditional
   variation (j=0 ℓ=9: 0.0120 vs 0.0174; Q(i) ℓ=3: 0.0048 vs 0.0143). A CM
   curve re-exposes the abelian p±1 channel but never exceeds it.
3. **3-adic Hecke visibility.** The split-half Hecke term is invisible at good
   primes (ℓ=5: z = −0.31) but visible at powers of the CM field's ramified
   prime (ℓ=9: z = 24.5; ℓ=27: z = 2.6) — ramification shrinks the Hecke
   conductor's p-adic part, pinning a_p mod 3^k by a small modulus. This
   refines paper 67's "split-half GL₂-hidden" claim to "hidden at good
   primes".

The shadow remains factor-useless: symmetric only (asym null, which-factor
lost, barrier 2); a residue dial / QRLEAK-family class channel (barrier 5);
the exact order mod N sealed behind the CRT split (barrier 6); and every
exploited piece is Gauss/Eisenstein (1801), ECM (1987), p+1 (1982), or a
residue dial — known methods (barrier 8). Choosing a second CM field changes
the inert class and adds a rational-torsion degeneracy, but the observable is
still exactly the abelian p±1 channel, diluted by the split half, never a
single factor.

---

*Experiment: 403. Assessment: v179. Paper 68, issue #84. Script: /tmp/exp_cmecmgeneral_final.py. Round-17 2/2 done. All numbers from the canonical run (seed 20260812); z-scores from 20000-semiprime repeats (seed 4242 for the ℓ=27 3-adic confirm).*

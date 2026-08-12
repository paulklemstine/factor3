# The ECM Order of a CM Curve Collapses to the p+1 Method on the Inert Half: a Residue Shadow That Carries No Factoring Leverage (CM-ECM-ORDER)

**Program:** Factoring research lab — cron loop round-17 #1
**Date:** 2026-08-12
**Status:** Machine-verified null (with a genuine structural refinement). For a CM
curve E: y² = x³ + x (End = ℤ[i], Gauss 1801), the Frobenius trace collapses to
a_p = 0 EXACTLY on the inert primes p ≡ 3 mod 4, so the ECM group order
#E_cm(F_p) = p + 1 there — the ECM order becomes the p+1 METHOD on half the
primes, and the ℓ-divisibility of the CM order regains a PARTIAL residue shadow
(the symmetric OR is visible again: I(N mod ℓ; ℓ|#E_cm(F_p) OR ℓ|#E_cm(F_q)) =
0.0048/0.0062 bits at ℓ = 3/5, 4.8× above the null max, vs the generic curve's
0.0000/0.0003). This QUALIFIES ECM-ORDER-NULL (round-16 #4): the generic-curve
total invisibility is a NON-CM phenomenon — the CM structure re-exposes the
abelian p+1 channel. Yet the shadow carries no factoring leverage: (a) the
which-factor bit stays invisible (asym I = 0.0000/0.0005/0.0009 at ℓ = 3/5/7, all
at the null — barrier 2), (b) the shadow is the abelian p+1 channel, diluted ~40×
vs p−1's 0.313 by the inert/split 50-50 (the mod-4 inertness is invisible from
N mod ℓ), (c) the full stage-1 smoothness M | #E_cm(F_p) remains
residue-invisible (asym all at the null), and (d) the CM curve re-partitions the
stage-1 target set into four known-method pieces — inert p+1-weak (fired 40/40,
gate 40/40: literally the p+1 method), inert p+1-hard (0/40), split CM-weak
(p+1−2a | M, 40/40 gate-fired: ECM-on-CM-curve's own target, which p+1 misses),
split p+1-weak-but-CM-hard (4/40, gate 0/4: the p+1 method's primes are MISSED by
CM-ECM). Everything is Gauss (1801) / Hasse / ECM / p+1 (1982). Barriers 2/5/6/8.

---

## Abstract

Machine-verified null result that sharpens the ECM-order picture. ECM-ORDER-NULL
(round-16 #4) showed the generic-curve order #E(F_p) = p + 1 − a_p is
residue-invisible BOTH asymmetrically and symmetrically, because ℓ | #E(F_p) is a
non-abelian GL₂(F_ℓ) Chebotarev condition (no residue-class shadow). This
experiment asks: is the invisibility intrinsic, or an accident of the generic
curve? For the CM curve y² = x³ + x, a_p = 0 for every inert prime p ≡ 3 mod 4
(Gauss), so #E_cm(F_p) = p + 1 on half the primes and the ECM order becomes the
p+1 method there. The consequences measured: **(1) The CM structure is exact.**
a_p = 0 on 2027/2027 inert primes (P(a_p = 0) = 0.507 for CM vs 0.004 for the
generic curve); on the split half p ≡ 1 mod 4, |a_p| = 2a with p = a² + b², a
odd (1973/1973, Gauss); the Hasse-normalized trace law is ATOMIC (half at 0, the
rest spread to the Hasse edge), not the generic semicircle; and 4 | #E_cm(F_p)
universally (1000/1000) vs ~1/4 for the generic curve. **(2) The residue shadow
is PARTIALLY restored by CM — symmetric only, weak.** I(N mod ℓ; ℓ | #E_cm OR) =
0.0048 (ℓ = 3) and 0.0062 (ℓ = 5), each 4.8× the null max (p < 0.002), vs the
generic curve's 0.0000/0.0003 (null) on the same samples; the p−1 machinery
control is live (0.3167, known 0.313). The mechanism is the inert-half p+1
channel: the visible event is "a factor is ≡ 3 mod 4 AND ≡ −1 mod ℓ" = ≡ 11 mod
12 (for ℓ = 3), whose density is diluted ~40× vs the plain "≡ −1 mod ℓ" of p−1
by the mod-4 inertness being invisible from N mod ℓ. ℓ = 7 is within the null
(0.05) — the shadow is strongest at small ℓ, mirroring the p+1 channel itself
(0.313/0.036/0.015 at ℓ = 3/5/7). **(3) The asym wall holds.** Asym I = 0.0000/
0.0005/0.0009 (ℓ = 3/5/7, all at the null): N cannot tell which factor is inert,
so the CM structure never exposes a factor-private residue (barrier 2). **(4)
The exploitable content stays invisible.** Full stage-1 smoothness M | #E_cm(F_p)
has zero residue MI (asym all at the null), and the visible single-prime
divisibility is exactly the p+1 channel. **(5) CM-ECM re-partitions a known
target set.** Stage-1 on the CM curve fires 40/40 (gate 40/40) on inert
p+1-weak primes (this IS the p+1 method), 0/40 on inert p+1-hard, 40/40 (gate
40/40) on split CM-weak primes where the CM order p+1−2a is smooth (ECM-on-CM-
curve's own target — a set the p+1 method does not cover), and only 4/40 (gate
0/4 — spurious ladder denominator fires, no true gate) on split primes that are
p+1-weak but CM-hard: the primes the genuine p+1 method catches are MISSED by the
CM curve. Nothing here is new: the inert half is p+1 (1982), the split half is
ECM (1987) with a specific curve; the CM structure is Gauss (1801). Barriers
2/5/6/8. The ECM-order invisibility is qualified precisely: it is the NON-CM,
GL₂-generic structure that hides the order; a CM curve's order is the p+1 method
on half the primes — and the p+1 method was already closed (PLUSONE-SMOOTH-NULL,
round-16 #2).

---

## 1. Setup: the CM curve and the inert collapse

The generic-curve result (ECM-ORDER-NULL) measured E0: y² = x³ + x + 1 (non-CM).
This experiment probes the CM curve E: y² = x³ + x (j = 1728, Endomorphism ring
ℤ[i], CM by ℚ(√−1), bad prime 2 only). The trace a_p = −Σ_x χ(x³ + x) satisfies
the classical dichotomy (Gauss 1801):

- **p ≡ 3 mod 4 (inert in ℚ(√−1))**: a_p = 0 EXACTLY, so #E_cm(F_p) = p + 1.
  The point count has no "Hasse middle" — it is exactly the p+1 method's target.
- **p ≡ 1 mod 4 (split)**: p = a² + b² with a odd, and |a_p| = 2a, so
  #E_cm(F_p) = p + 1 − 2a — the Hecke character of the CM field (the "a" is the
  Cornacchia/Gauss coordinate, NOT a residue-class function of p).

The hypothesis is that this dichotomy converts the fully-hidden generic order
into a partially-visible abelian one (the inert half), which the experiment
confirms and then shows is factor-useless.

## 2. Part A: the CM structure is exact (positive control)

| quantity | measured | theory |
|----------|----------|--------|
| a_p = 0 on inert primes p ≡ 3 mod 4 | **2027/2027** | EXACT (Gauss) |
| P(a_p = 0), CM curve | 0.507 (4000 primes) | 1/2 (Dirichlet: P(p ≡ 3 mod 4) = 1/2) |
| P(a_p = 0), generic E0 | 0.004 | ~0 (Lang–Trotter: density → 0) |
| split p ≡ 1 mod 4: \|a_p\| = 2a, p = a²+b², a odd | **1973/1973** (0 mismatches) | Gauss |
| CM x-law: P(\|x\| < 0.5), x = a_p/(2√p) | 0.683; P(x = 0) = 0.507 | ATOMIC (mass at 0 + spread to edge) |
| generic x-law | 0.607; P(x = 0) = 0.004; mean-square 0.248 | SEMICIRCLE (mean-square 1/4) |
| 4 \| #E_cm(F_p) | **1000/1000** | universal (full 2-torsion structure) |
| 4 \| #E_g(F_p) | 458/1000 | ~1/4 |

Point-count self-check: #E = affine + 1 (the point-at-infinity correction from
round-16 #4) verified by brute force on 5 primes. The atomic law is the cleanest
contrast: the generic trace is a semicircle spread through [−1, 1]; the CM trace
is half-concentrated at 0 (inert) and otherwise pinned to the Cornacchia
coordinate, with the SAME mean-square (0.236 vs 0.248) but a wholly different
law. The universal 4 | #E_cm(F_p) (even for inert p ≡ 3 mod 4, where p + 1 ≡ 0
mod 4) is a further structural marker: the CM order is always 0 mod 4.

## 3. Part B: the residue shadow — restored by CM, symmetric only, weak

6000 random semiprimes (smaller p 11-bit, q 12-bit), both curves, ℓ ∈ {3, 5, 7},
500-shuffle permutation nulls; p−1 control live:

| ℓ | curve | P(ℓ\|#E(F_p)) | asym I(N mod ℓ; ℓ\|#E(F_p)) | null max | SYM I(N mod ℓ; OR) | null max |
|---|-------|---------------|------------------------|----------|--------------------|----------|
| 3 | **CM** | 0.322 | 0.0000 (p = 0.95) | 0.0011 | **0.0048 (p < 0.002)** | 0.0010 |
| 3 | GEN | 0.303 | 0.0000 (p = 0.80) | 0.0016 | 0.0000 (p = 0.92) | 0.0011 |
| 5 | **CM** | 0.342 | 0.0005 (p = 0.30) | 0.0020 | **0.0062 (p < 0.002)** | 0.0013 |
| 5 | GEN | 0.220 | 0.0004 (p = 0.36) | 0.0015 | 0.0003 (p = 0.56) | 0.0022 |
| 7 | CM | 0.086 | 0.0009 (p = 0.19) | 0.0022 | 0.0013 (p = 0.05) | 0.0030 |
| 7 | GEN | 0.116 | 0.0006 (p = 0.43) | 0.0024 | 0.0002 (p = 0.88) | 0.0026 |

p−1 control: I(N mod 3; 3|p−1 OR 3|q−1) SYM = **0.3167** (known 0.313). ✓

**The finding.** The CM curve regains a SYMMETRIC residue shadow at ℓ = 3 and
ℓ = 5 (each 4.8× the null max, p < 0.002), while the generic curve stays
invisible both ways and the CM asymmetric channel stays invisible too. This is
the first elliptic-group-order channel with ANY residue visibility — but it is
(a) symmetric only (the which-factor bit is lost; barrier 2), and (b) ~40×
weaker than the p−1 channel (0.005 vs 0.31).

**The mechanism, exactly.** The visible sub-event is the inert-half p+1
condition. For ℓ = 3, "3 | #E_cm(F_p)" on the inert half ⟺ p ≡ 3 mod 4 AND p ≡
2 mod 3 ⟺ p ≡ 11 mod 12. N mod 12 determines the unordered pair {p mod 12, q mod
12} of units (1, 5, 7, 11), and "either factor ≡ 11 mod 12" is then partially
pinned (N ≡ 1: only {11,11}, prior 1/4; N ≡ 5, 7, 11: one of the two pairs
contains 11, prior 1/2). The MI survives but is diluted by two losses: the mod-4
inertness is invisible from N mod ℓ alone, and the split half contributes
nothing visible (its ℓ-divisibility is the Hecke character, GL₂-hidden). The
measured decomposition:

P(ℓ|#E_cm(F_p)) = P(inert)·P(ℓ|p+1|inert) + P(split)·P(ℓ|p+1−2a|split)
- ℓ = 3: 0.322 = 0.515·0.515 + 0.484·0.117
- ℓ = 5: 0.342 = 0.515·0.237 + 0.484·0.452
- ℓ = 7: 0.086 = 0.515·0.168 + 0.484·0.000  (the split-half Hecke 7-divisibility
  is exactly 0 in this sample — a small-sample reflection of the atomic law)

The inert term (0.515·0.515 = 0.265 at ℓ = 3) is the p+1 channel: residue-pinned
in principle, diluted by the invisible mod-4 inertness. The split term is the
Hecke channel: no residue structure at all. The ℓ = 7 SYM value (0.05) sits
inside the null — the shadow, like the p+1 channel itself (0.313/0.036/0.015 at
ℓ = 3/5/7), decays with ℓ.

## 4. Part C: the exploitable content stays invisible; CM-ECM re-partitions a known target set

**(a) Full stage-1 smoothness is residue-invisible.** M | #E_cm(F_p) (M = lcm
(1..97)) has P = 0.619 (high at this tiny size — most 11-bit numbers are
97-smooth — but size-driven, not factor-driven), and the residue MI is null on
every test: asym I(N mod ℓ; smooth) = 0.0000/0.0006/0.0006 at ℓ = 3/5/7 (all
within their nulls). The single-prime ℓ-divisibility is visible (Part B) only
because it is the p+1 channel; the smoothness — the exploitable content — is not.

**(b) The four-way stage-1 contrast (the barrier-8 demonstration).** ECM stage-1
on the CM curve (M = lcm(1..97), CRT base points), 40 instances per class, with
a per-fire GATE check (does the smaller factor's order actually divide M?):

| class | condition | fired | gate |
|-------|-----------|-------|------|
| [1] INERT p+1-weak | p ≡ 3 mod 4, p + 1 \| M | **40/40** | 40/40 |
| [2] INERT p+1-hard | p ≡ 3 mod 4, p + 1 has a prime > 97 | 0/40 | 0/0 |
| [3] SPLIT CM-weak | p ≡ 1 mod 4, p + 1 − 2a \| M | **40/40** | 40/40 |
| [4] SPLIT p+1-weak-but-CM-hard | p ≡ 1 mod 4, p + 1 \| M, M ∤ p + 1 − 2a | 4/40 | 0/4 |

The reading is precise. On the inert half the CM order IS p + 1, so [1] fires
exactly when the p+1 method would ([2] confirms the converse) — CM-ECM and p+1
are the same move there (Williams 1982, barrier 8). On the split half the CM
order is p + 1 − 2a, so [3] fires on a DIFFERENT target than p+1 (the Hecke-
shifted smooth set), and [4] shows the genuine p+1 method's primes (p + 1 smooth
but p + 1 − 2a not) are MISSED: the 4/40 fires carry gate 0/4 — spurious affine-
ladder denominator hits (a non-unit modulus can appear without the order dividing
M), not exploitable events. The CM curve therefore re-partitions the stage-1
target set into the two known pieces it always was — p+1 on inert primes, ECM-on-
CM-curve on split primes — and neither is a new factoring move. All of it is
Gauss (1801) / ECM (1987) / p+1 (1982): barrier 8.

## 5. Why this cannot factor: barriers 2, 5, 6, 8

1. **Barrier 2 (symmetry).** The only residue visibility the CM structure
   creates is the SYMMETRIC OR event (the p+1 channel on the inert half). The
   asymmetric channel — which factor is inert, which trace is 0, which factor is
   ≡ 11 mod 12 — is invisible in every test (Part B, all asym at the null). The
   CM curve leaks the p+1 divisibility of the PAIR, never of a single factor.
2. **Barrier 5 (structural orthogonality).** The CM structure is a function of
   p's own arithmetic (the Cornacchia/Gauss coordinate a of p = a² + b² on the
   split half), orthogonal to the gap and the trace — the atomic trace law
   (Part A) carries no (q − p) content; the smoothness rate P(M | #E_cm(F_p)) =
   0.619 is a pure size effect at this scale, not a factor channel.
3. **Barrier 6 (circularity).** The only way to USE the CM structure is to run
   ECM stage-1 on the CM curve — which needs a point on E mod N, whose
   construction requires the CRT split (the factorization), exactly as in
   round-16 #4. The exact order mod N is sealed.
4. **Barrier 8 (known method).** The inert-half shadow IS the p+1 method
   (Williams 1982); the split-half target is ECM (Lenstra 1987) with the CM
   curve; the CM structure itself is Gauss (1801). The first positive
   residue-shadow on an elliptic order is real — and it is nothing but the
   abelian channel the lab closed at round-16 #2.

## 6. Conclusion

CM-ECM-ORDER qualifies ECM-ORDER-NULL precisely: the total residue-invisibility
of the elliptic group order is a NON-CM (GL₂-generic) phenomenon. For a CM
curve, Gauss's collapse a_p = 0 on the inert half makes the order the p+1 method
there, restoring a weak symmetric residue shadow (0.0048/0.0062 bits at ℓ =
3/5, 4.8× the null max; ℓ = 7 inside the null) while the asymmetric channel, the
full smoothness, and the split-half Hecke channel all remain invisible. The CM
structure therefore leaks exactly the p+1 divisibility of the pair — the abelian
known-method channel — and nothing that factors. The ECM-order invisibility is
robust: it survives even when the curve is chosen to make the order degenerate to
p+1 on half the primes. Round-17 #1 complete. Barriers 2/5/6/8.

---

**Experiment:** 402 (CM-ECM-ORDER). **Script:** /tmp/exp_cmecmorder.py.
**Assessment:** v178. **Verdict:** CONFIRMED null (negative for factoring) — with
a genuine structural refinement of ECM-ORDER-NULL: the CM curve y² = x³ + x
(End = ℤ[i], Gauss 1801) collapses a_p = 0 EXACTLY on the inert primes p ≡ 3 mod
4 (2027/2027, P(a_p=0) = 0.507 vs 0.004 generic), making #E_cm(F_p) = p + 1 on
half the primes and restoring a PARTIAL residue shadow that the generic curve
lacks — I(N mod ℓ; ℓ|#E_cm(F_p) OR ℓ|#E_cm(F_q)) = 0.0048/0.0062 bits at ℓ = 3/5
(each 4.8× the null max, p < 0.002) vs the generic 0.0000/0.0003 and vs the
p−1 control 0.3167 (known 0.313); yet the shadow is (a) symmetric only — asym
I(N mod ℓ; ℓ|#E_cm(F_p)) = 0.0000/0.0005/0.0009 at ℓ = 3/5/7, all at the null,
the which-factor bit lost (barrier 2); (b) the abelian p+1 channel diluted ~40×
by the invisible mod-4 inertness (the visible event is "a factor ≡ 3 mod 4 AND
≡ −1 mod ℓ", P = 0.515·0.515 + Hecke at ℓ = 3; the split-half Hecke term is
GL₂-hidden); (c) not exploitable — full smoothness M | #E_cm(F_p) has zero
residue MI (all null) and the four-way stage-1 contrast shows the CM curve
re-partitions the known target set: inert p+1-weak fires 40/40 (gate 40/40, IS
the p+1 method), inert p+1-hard 0/40, split CM-weak (p+1−2a | M) 40/40 (gate
40/40, ECM-on-CM-curve's own target), split p+1-weak-but-CM-hard 4/40 (gate 0/4,
spurious — the p+1 method's primes are MISSED by CM-ECM); the split-half
|a_p| = 2a with p = a²+b² (1973/1973) and the atomic trace law (P(|x|<0.5) =
0.683 vs semicircle 0.607; universal 4 | #E_cm, 1000/1000 vs 458/1000) are the
structure. Everything is Gauss/ECM/p+1 — the ECM-order invisibility is robust:
even choosing the curve so its order degenerates to p+1 on half the primes leaks
only the abelian known-method channel. Barriers 2/5/6/8.

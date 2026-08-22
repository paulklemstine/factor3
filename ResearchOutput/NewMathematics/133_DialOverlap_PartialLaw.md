# Paper 133 — DIAL-OVERLAP-LAW: Partially Overlapping Dials Are Exactly One Bit Redundant

**Verdict name: H1-CONFIRMED-PARTIAL-OVERLAP-LAW.**
Round-37 #5 · exp 462 · assessment v242 · script `ResearchOutput/scripts/2026-08-21-resume/exp462_overlap_law.py` (+ `addendum462.py`, results JSONs) · seed 20260821.

## 1. The open cell of the battery-overlap ladder

Paper 91 measured the two extremes: coprime-conductor dial pairs SYNERGIZE (+0.129 bits) and
shared-disc pairs OVERLAP (−0.99 bits, one channel redundant). The intermediate case — two
GENUINELY DIFFERENT S3 fields sharing their quadratic subfield Q(√d) — was open. Such fields
exist iff two irreducible S3 cubics have discriminants with equal squarefree part but
different values (disc₁ = d·k₁², disc₂ = d·k₂², k₁ ≠ k₂ ⟹ different fields: an S3 cubic's
field determines its discriminant).

Pre-stated derivation, committed before simulation: Gal(L₁L₂/Q) = S₃ ×_{C₂} S₃ (fiber product,
order 18); both sign characters coincide, so both channels read the same input variable; the
co-information collapses to H(C) − H(C|X) = 1.5 − 0.5 = **exactly 1 bit**; all remaining fiber-
product correlation lives in the residue-invisible χ_d = +1 fiber (H2 refuted analytically in
advance).

## 2. Results

Field search: x³+ax+b, |a|,|b| ≤ 120 → 56,410 S3 cubics, 23,481 squarefree parts (largest
families d=−3: 370 fields, d=−11: 72). Primary pairs measured at 154,382 unramified primes <
2²¹ and 30,000 semiprimes:

| pair | polynomials (disc) | type-agreement | I_a | I_b | JOINT | deficit | law dev |
|---|---|---|---|---|---|---|---|
| d=−7 @m=7 | x³−5x−5 (−175=−7·5²) & x³−3x−5 (−567=−7·9²) | 0.7773 (=7/9) | 1.0003 | 1.0002 | **1.0008** | **+0.9998** | −0.0002 |
| twin replica | x³−5x+5 & x³−3x+5 | 0.7773 | 1.0003 | 1.0002 | **1.0008** | **+0.9998** | −0.0002 |
| d=−3 @m=3 | x³−6x−6 (−108=−3·6²) & x³−3 (−243=−3·9²) | 0.7776 | 1.0000 | 1.0000 | **1.0000** | **+1.0000** | −0.0000 |

Prime level: every dial reads I(p mod m*; T) = 1.0000–1.0003 (theory 1.0000); the joint
type-pair Chebotarev distribution matches the order-18 class proportions (1/2, 1/18, 2/18,
2/18, 4/18); off-diagonal mass 34,375 observed vs 4/18·n = 34,307 predicted.

Controls: coprime pair (−31 × −23) synergy reproduced (joint exceeds sum by 0.1300 vs lab's
0.1290); conjugate pair deficit +1.0008 = I_a exactly as the pre-stated degeneracy analysis
demands; which-factor wall on the new partial-overlap joint NULL (Δ = +0.0000, z = −1.94).

## 3. What this decides

The battery-overlap ladder is CLOSED at the pair level:
coprime conductors → +synergy · shared quadratic subfield → EXACTLY −1 bit (the shared sign
character, nothing more) · same field / same disc → full redundancy. Everything beyond the
common C₂ quotient in the fiber product is provably invisible to every residue class.
For the no-pinning scope: partial batteries must be charged their overlap exactly — the
deficit is a computable character-theoretic quantity, not an empirical fudge factor.

Caveats: (i) sparse joint moduli distort plug-in MI (at lcm 14175 ≈ 2.1 samples/cell the
readings swing ±0.4–0.7 bits; clean only at m = |d| or ≥ ~100 samples/cell) — the paper-70
sparse-dial lesson extended to joints. (ii) LEDGER INSIGHT L11: MI signatures CANNOT
distinguish partial-overlap from same-field pairs (~1.00 deficit both) — the honest
discriminators are type-agreement (7/9 vs 1.0) and off-diagonal mass (4/18 vs 0).
(iii) The scan's third candidate "pair" (discs −216/−864) turned out to be ONE field with
different generators — index² caught live: disc-value arguments are not field arguments.
(iv) For d=−6 the character conductor is 24, not 6: readings at m=6 vanish (0.0001).

Method ledger: 16 entries (L0–L16), including the index² trap caught mid-run, a silent
x⁴-reduction corruption killed by a circuit breaker, and a Legendre scorer comparing binary
predictions to 3-valued types (fixed → 389/389 on twelve cross-checks). Full list in the
script header.

Now 465 experiments. Assessment v242.

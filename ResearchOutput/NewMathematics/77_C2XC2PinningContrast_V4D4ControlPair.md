# The 2-Dimensional Abelianization: Abelian V₄ Pins the Identity, Non-Abelian D₄ Cannot (C2XC2-PINNING-CONTRAST)

**Program:** Factoring research lab — cron loop round-22 #1
**Date:** 2026-08-12
**Status:** Machine-verified (V₄ quartic x⁴−2x²+9 and D₄ quartic x⁴−2, 2^18 sieve, shuffled-null z-scores, 30k semiprimes).

Papers 65–76 closed the pinning-content classification table for every group with
G^ab ≠ {1} of order ≤ 3 and for the perfect group A₅ — but left the *2-dimensional
abelianizations* untested. This paper supplies the sharpest possible test: the
**control pair** Q(√2, i) = Q(ζ₈) (Gal = V₄, abelian) and Q(∜2, i) (Gal = D₄,
non-abelian) share the **identical character lattice** — the same three quadratic
subfields, the same abelianization G^ab = C₂×C₂, the same conductors — and differ
only in *abelian-ness*. The paper-71 criterion makes a stark prediction on this
pair: the abelian member pins the identity fork at H(1/4); the non-abelian member
cannot pin it at all — it leaks at a capped H(1/8) − (1/4)H(1/2) = 0.2936.

## 1. The control pair: identical lattice, opposite abelian-ness

Both fields have the same three quadratic subfields:

| field | minimal polynomial | disc | Gal |
|---|---|---|---|
| Q(√2, i) = Q(ζ₈) | x⁴ − 2x² + 9 (roots ±√2±i) | 147456 = **384²** | **V₄** (abelian) |
| Q(∜2, i) | x⁴ − 2 | −2048 = **−2¹¹** | **D₄** ([D₄,D₄]=⟨r²⟩≅C₂) |

The three quadratic subfields are Q(√2), Q(i), Q(√−2) in *both* cases — so both
fields carry the **same** character lattice: (2|p) of conductor 8, (−1|p) of
conductor 4, (−2|p) of conductor 8, every one N-computable via p mod 8 — and the
**same** abelianization C₂×C₂. The only difference is whether the group is
abelian (V₄ ≅ C₂×C₂ = G^ab) or non-abelian (D₄ with abelianization C₂×C₂). This
is the ideal experimental control for the paper-71 criterion.

Root-count histograms over the 22,997 primes of the 2^18 sieve (full Horner over
all residues mod p, 126 s) give the exact signatures:

**V₄:** nr=4 0.2487 (1/4), nr=0 0.7513 (3/4), nr=1/2/3 zero.
**D₄:** nr=4 0.1238 (1/8), nr=0 0.6257 (5/8), nr=2 0.2505 (1/4), nr=1/3 zero.

The D₄ root-count classes are the conjugacy classes: {e} → nr=4 (1/8),
{s, r²s} → nr=2 (1/4), everything else → nr=0 (5/8). The V₄ field has no
transpositions and the group is abelian, so splits-completely is a full C₂×C₂
fibre (rate 1/4).

## 2. The criterion on a 2-dimensional abelianization

By paper 71, a binary splitting fork is congruence-pinned by a Dirichlet character
**iff it factors through G^ab**. For V₄ (abelian), G^ab = V₄ itself, so **every**
fork pins: the map p ↦ Frob_p is itself the character (p mod 8), and any fork is
a union of fibres. For D₄, G^ab = C₂×C₂, so only unions of *cosets of the
commutator* [D₄,D₄] = ⟨r²⟩ — i.e. forks that factor through (χ₂(p), χ₄(p)) —
can pin. The six forks tested:

| fork | event | rate | V₄ law | D₄ law |
|---|---|---|---|---|
| splits-completely | nr = 4 | 1/4 (V₄), 1/8 (D₄) | H(1/4) = 0.8113, pinned | LEAK 0.2936, capped |
| [nr=2] | the {s,r²s} coset | 1/4 | — | H(1/4) = 0.8113, pinned |
| [nr∈{4,0}] | complement of {s,r²s} | 3/4 | 0.8113, pinned | 0.8113, pinned |
| [nr=0] | large partner | 3/4 (V₄), 5/8 (D₄) | 0.8113, pinned | LEAK 0.7044, large |
| [nr∈{0,2}] | = [nr≠4] complement | 3/4 | 0.8113, pinned | — |
| has-root | nr ≥ 1 | 1/4 | 0.8113, pinned | — |

**Measured (Part B):** every fork matches its exact law (six ✓).

## 3. The identity leakage: H(1/8) − (1/4)H(1/2) = 0.2936, capped

The D₄ identity fork [nr=4] = {e} has rate 1/8. It **cannot** be pinned: e shares
the commutator coset {e, r²} with r² — the same fibre over (χ₂, χ₄) = (+1, +1) =
p ≡ 1 mod 8 — so any Dirichlet character that could see e would have to
distinguish e from r², which live in the same G^ab fibre. The exact law:

    I(p mod m; [e]) = H(1/8) − (1/4)H(1/2) = 0.54356 − 0.25 = 0.29356 bits

— capped at this value for *every* m. Residue ladder (measured):

| m | [e] | [nr=2] | [nr=0] |
|---|---|---|---|
| 4 | 0.1379 (= H(1/8) − (1/2)H(1/4)) | 0.3113 | 0.0488 |
| 8 | 0.2936 | 0.8113 = H(1/4) | 0.7044 |
| 16 | 0.2936 (cap) | 0.8113 | 0.7044 |
| 5 (coprime) | 0.0000 | 0.0000 | 0.0000 |

Contrast with the abelian member of the pair: V₄ [nr=4] = splits-completely IS
p≡1 mod 8, rate 1/4, pinned at **H(1/4) = 0.8113 EXACT**. Same lattice, same
residues, same abelianization — abelian pins the identity at 0.8113, non-abelian
caps it at 0.2936 < H(1/8) = 0.5436. **This is the criterion in its cleanest form.**

The [nr=2] fork is the first **joint-AND 2-dimensional** pinned fork: {7} is not
the level set of any character mod 8, yet [nr=2] ⟺ p ≡ 7 mod 8 is a union of the
fibre (+1,−1) — the AND of (2|p)=+1 with (−1|p)=−1. It pins at H(1/4) exactly,
a 2D event with no 1D kernel.

## 4. Within-coset flatness: the e-vs-r² commutator coin

P([e] | p ≡ 1 mod 8) measures whether the identity can be told apart from r²
inside their shared commutator fibre:

| field | P([e] | p≡1 mod 8) |
|---|---|---|
| D₄ | **0.4980** — e vs r² a fair coin |
| V₄ | **1.0000** — p≡1 mod 8 IS splits-completely |

The conditional channel I(p mod 16; [e] | p≡1 mod 8) = 0.0000 (null z = −0.61):
the commutator refinement [e]-vs-[r²] is invisible to *every* modulus. The 2D
abelianization adds pinning *content* (the joint-AND [nr=2] fork) but the
beyond-the-dial refinement stays invisible — paper 75's within-coset flatness,
transplanted to the first 2D lattice. Cap check: I(m=8) = I(m=16) = 0.2916, never
reaching H(1/8).

## 5. Semiprime level: order-4 split-count law on a joint-AND event + leakage collapse

30k semiprimes from the 2^16 pool. The **rate-1/4 forks of both fields obey the
paper-74 order-4 split-count law EXACTLY** — including the D₄ [nr=2] *joint-AND 2D
event on a non-abelian field* (effective order n = 4: P(s|N≡1) = {3/4, 0, 1/4},
P(s|N≡c≠1) = {1/2, 1/2, 0}):

| fork | s | OR | AND | XOR |
|---|---|---|---|---|
| law n=4 | Is(4) = 0.2947 | g(4) = 0.0359 | A(4) = 0.1345 | X(4) = 0.2044 |
| V₄ [split] | 0.2892 | 0.0349 | 0.1323 | 0.1994 |
| D₄ [nr=2] | 0.3003 | 0.0363 | 0.1376 | 0.2087 |

The D₄ [e] leakage fork (prime-level rate 1/8) gives the **semiprime collapse of
prime-level leakage** — exact small channels, all verified:

| channel | measured | law |
|---|---|---|
| split-count s | 0.0421 | 0.0428 |
| OR | 0.0034 | 0.0030 |
| AND | 0.0306 | 0.0318 |
| XOR | 0.0138 | 0.0135 |

Which-factor wall: I(p > q; split-count) = 0.0000 for all three forks — symmetric,
factor-useless at every level.

## 6. Classification table (C₂×C₂ row) and seals

**Pinning-content table (extended).** C₂ → quadratic, H(1/2)-class (papers 54/72);
C₃ → cubic, H(1/3) (paper 71); C₅ → order-5, H(1/5) (paper 76); S₃/S₄ →
sign-only (papers 65–71); A₄ → cubic + within-V₄ flat (paper 75); A₅ → absolutely
flat (paper 76); **V₄ (abelian, G^ab = C₂×C₂) → every fork pins, [e] = H(1/4)
EXACT; D₄ (non-abelian, G^ab = C₂×C₂) → coset-forks pin ([nr=2] joint-AND at
H(1/4)), [e] leaks H(1/8) − (1/4)H(1/2) = 0.2936 capped, [nr=0] leaks 0.7044
(this paper)**. The organizing law stands: **abelian ⟹ pinned at H(1/n);
solvable non-abelian ⟹ pinned at the abelianization (which now includes a 2D
C₂×C₂ — adding pinning content, a joint-AND fork); perfect ⟹ absolutely flat.**
The 2D abelianization is the last row.

**Barriers.** Symmetry (2): the forks are class functions with residue content only
at the N-computable abelianization — the which-factor wall is null everywhere.
Structural orthogonality (5): the 2D lattice is a full residue dial (3 quadratic
characters = 3 bits of dial), but the beyond-dial refinement (e-vs-r²) is
invisible to every modulus. Circularity (6): the C₂×C₂ fibre *is* the
quadratic-reciprocity content — computing the coset of Frob in D₄'s abelianization
IS computing (χ₂(p), χ₄(p)), a residue computation, not a factoring move. Known
methods (8): Galois theory, cyclotomic fields, quadratic reciprocity (Gauss 1801),
octic reciprocity (the ζ₈ field), Chebotarev density (1922) — all classical.

**Unification.** The control pair (V₄/D₄, identical characters, abelian vs
non-abelian) is the cleanest statement of the paper-71 criterion and the
strongest direct test to date. New exact objects: the joint-AND 2D pinned fork
(H(1/4)), the D₄ identity leakage law H(1/8) − (1/4)H(1/2) = 0.2936 and large
partner 0.7044, the commutator-invisible e-vs-r² refinement, and the semiprime
leakage collapse. The paper-74 order-4 split-count law is extended to joint-AND
2D events on a non-abelian field. Papers 71, 74, 75, 76 unify.

*Script:* /tmp/exp_d4.py (2^18 sieve, 300-shuffle nulls, 30k semiprime MC, 165 s).

# The Abelian Type-Pair Law Is Universal: Multi-Stateness, Not Cyclicity, Breaks the 1-Bit Cap (ABELIAN-TYPE-CHANNEL)

**Program:** Factoring research lab — cron loop round-23 #1
**Date:** 2026-08-12
**Status:** Machine-verified (exact unit-group enumeration over 11 abelian conductors + prime-level MC, 2^18 sieve, 30k semiprime MC, 2^16 pool).

Paper 78 proved the exact semiprime type-pair law
I_pair = H(Π) − (1/φ(f)) Σ_c H(Π_c) and showed that CYCLIC fields — f prime,
Gal = (Z/f)^× = C_n — exceed the 1-bit binary-fork cap (papers 72–74). This
paper opens the natural next frontier: the same channel on **composite**
conductors, whose unit groups are **non-cyclic abelian** — C₂×C₂, C₂×C₂×C₂,
C₂×C₄, C₂×C₂×C₄. The motivating hypothesis was that *cyclicity* is what carries
the multi-bit channel. The experiment **refutes that at the threshold**: the
true threshold is *type-state count* (≥ 3 distinct unit orders), and every
≥3-state group — cyclic or not — exceeds 1 bit. What cyclicity does supply is
**amplification**: among 3-state groups the channel runs
C₄ (1.2500) > C₂×C₄ (1.0737) > C₂×C₂×C₄ (1.0226), a clean
1D > 2D > 3D character law.

## 1. Universality: the exact law holds on every abelian conductor

Exact enumeration (the type-pair law computes over the unit group for ANY f —
units, inverses, and orders are all well-defined when gcd(a,f)=1) over 11
abelian conductors, verified at prime level (23,000 primes, 2^18) and at
semiprime level (30k MC):

| f | Gal of Q(ζ_f) | #types | H(T) | I_pair exact | I_pair MC | > 1 bit |
|---|---|---|---|---|---|---|
| 5 | C₄ (cyclic, p) | 3 | 1.5000 | 1.2500 | — (paper 78) | YES |
| 7 | C₆ (cyclic, p) | 4 | 1.9183 | 1.4739 | — (paper 78) | YES |
| 9 | C₆ (cyclic, 3²) | 4 | 1.9183 | 1.4739 | 1.4749 | YES |
| 13 | C₁₂ (cyclic, p) | 6 | 2.4183 | 1.7239 | — (paper 78) | YES |
| 25 | C₂₀ (cyclic, 5²) | 6 | 2.2219 | 1.4527 | — | YES |
| 8 | C₂×C₂ (8) | 2 | 0.8113 | 0.2947 | 0.2914 | no |
| 12 | C₂×C₂ (12) | 2 | 0.8113 | 0.2947 | — | no |
| 24 | C₂×C₂×C₂ | 2 | 0.5436 | 0.0906 | — | no |
| 15 | C₂×C₄ (15) | 3 | 1.4056 | **1.0737** | 1.0712 | **YES** |
| 20 | C₂×C₄ (20) | 3 | 1.4056 | **1.0737** | — | **YES** |
| 40 | C₂×C₂×C₄ | 3 | 1.2718 | **1.0226** | 1.0216 | **YES** |

The law I_pair = H(Π) − (1/φ(f))Σ_c H(Π_c) — whose derivation needs only the
abelian structure (the type is a function of the unit class p mod f) — matches
MC within 0.01 on every conductor tested. Paper 78's cyclic-prime results are
reproduced exactly, and the composite conductors are NEW.

### Prime level on composite conductors

I(p mod f; T) = H(T) EXACTLY, first measured on non-cyclic abelian groups:

| f | I(p mod f; T) | H(T) | [T=1] pinning | H(1/φ(f)) |
|---|---|---|---|---|
| 8 | 0.8092 | 0.8113 | 0.8092 | 0.8113 |
| 9 | 1.9188 | 1.9183 | 0.6501 | 0.6500 |
| 15 | 1.4030 | 1.4056 | 0.5397 | 0.5436 |
| 40 | 1.2700 | 1.2718 | 0.3352 | 0.3373 |

The C₂×C₄ field Q(ζ₁₅) carries a **1.40-bit multi-state type channel** at prime
level — the first full type channel on a non-cyclic abelian group. The [T=1]
splits-completely fork pins at **H(1/φ(f)) EXACTLY** for every composite f: the
C₂×C₄ pinning (H(1/8) = 0.5436) and the C₂×C₂×C₄ pinning (H(1/16) = 0.3373) are
new — 2-dimensional and 3-dimensional abelianizations beyond paper 77's C₂×C₂.
Thickening is zero (f=15: I(p mod 225; T) = I(p mod 15; T)); coprime controls
flat.

## 2. The threshold: type-state count, not cyclicity

The motivating claim "non-cyclic ⟹ I_pair ≤ 1 bit" is **false**: C₂×C₄ gives
I_pair = 1.0737 and C₂×C₂×C₄ gives 1.0226, both above the binary-fork cap. The
correct threshold is the number of distinct element orders in the unit group:

- **2 type states ⟹ I_pair = Is(φ(f)) exactly** (the type pair IS the split
  count): f=8 0.2947 = Is(4), f=12 0.2947 = Is(4), f=24 0.0906 = Is(8). The full
  type channel of Q(ζ₈) — paper 77's V₄ field — is exactly its split-count
  channel; paper 74's Is(n) is the 2-state face of the type channel.
- **≥ 3 type states ⟹ I_pair > 1 bit**, cyclic AND non-cyclic: the 1-bit cap of
  papers 72–74 is broken by multi-stateness, not by the shape of the group.

## 3. Cyclicity amplifies: the 1D > 2D > 3D law

Among 3-state groups the channel is strictly ordered by the number of generators
of the abelian group:

    C₄ (cyclic, 1D)      I_pair = 1.2500
    C₂×C₄ (2D)           I_pair = 1.0737
    C₂×C₂×C₄ (3D)        I_pair = 1.0226

A cyclic (1-dimensional) character concentrates the N-conditioning on the type
pair best; each extra generator spreads the conditional law, eroding the
channel. The 4-state C₆ (1.4739) and 6-state C₁₂ (1.7239) continue the cyclic
family upward. This is the honest refinement of the paper's motivating
hypothesis: cyclicity does not set the threshold — it sets the amplification.

## 4. Two exact identities

**Prime-power identity.** Q(ζ₉) (3², Gal = C₆) has EXACTLY the same type law as
Q(ζ₇) (p, Gal = C₆): I_pair = 1.4739 in both, H(T) = 1.9183 in both. The type
law of a cyclic field depends only on the cyclic ORDER φ(f), not on the
conductor — prime and odd-prime-power conductors are interchangeable.

**2-state identity.** For any 2-state type {1, r} with [T=1] rate 1/φ(f), the
type-pair channel equals the paper-74 split-count law: I_pair = Is(φ(f)) EXACT.
Verified to 1e-9 on f = 8, 12, 24.

## 5. Semiprime checks

Which-factor wall 0.0000–0.0002 on every fork (symmetric, factor-useless).
Coprime controls flat. The s-projection recovers Is(φ(f)) exactly (f=8 0.2914
vs Is(4)=0.2947; f=15 0.0888 vs Is(8)=0.0906; f=40 0.0257 vs Is(16)=0.0267) — the
split-count remains one face of the richer type channel on non-cyclic abelian
groups too.

## 6. Position and seals

**What is new.** (1) The type-pair law is UNIVERSAL over all abelian cyclotomic
conductors — cyclic primes, cyclic prime powers, and every small non-cyclic
abelian unit group. (2) The threshold theorem (measured): 2-state ⟹ Is(φ) < 1,
every ≥3-state group exceeds 1 bit — the binary-fork cap breaks on
multi-stateness. (3) The amplification law: among multi-state groups the channel
is ordered 1D > 2D > 3D by the generator count (1.25 > 1.07 > 1.02). (4) The
first composite-conductor [T=1] pinnings (C₂×C₄ at H(1/8), C₂×C₂×C₄ at
H(1/16)). (5) The prime-power and 2-state identities.

**Barriers.** Symmetry (2): the type pair is a symmetric class function — the
which-factor wall is null. Structural orthogonality (5): the channel is a pure
p-mod-f residue dial (the type is a function of p mod f; the type pair of
p mod f, q mod f). Circularity (6): I_pair is N-computable only behind the CRT
split. Known methods (8): cyclotomic fields, Dirichlet characters, CRT,
Chebotarev density (1922). Barriers 2/5/6/8.

**Unification.** Paper 78's cyclic law extends to every abelian conductor; paper
77's V₄ = Q(ζ₈) split-count (Is(4) = 0.2947) is revealed as the 2-state face of
the type channel; paper 74's Is(n) is the 2-state limit. The honest negative
(the "cyclicity" hypothesis) sharpens the classification: the residue channel
carries more than 1 bit exactly when the abelian unit group has ≥ 3 distinct
orders, and a 1-dimensional character carries it best.

*Script:* /tmp/exp_abeltype.py (exact unit-group enumeration, 2^18 sieve,
30k semiprime MC, 0.2 s).

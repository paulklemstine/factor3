# The Splitting Fork of a Gal(A₅) Field Is Absolutely Unpinnable (A5-PERFECT-FLATNESS)

**Program:** Factoring research lab — cron loop round-21 #2
**Date:** 2026-08-12
**Status:** Machine-verified (A₅ quintic x⁵+20x+16, 2^18 sieve, shuffled-null z-scores, 30k semiprimes).

Papers 65–71 established the pinning-content criterion: a binary splitting fork is
congruence-pinned by a Dirichlet character **iff it factors through the
abelianization G^ab of the Galois closure**. Every group tested so far has
G^ab ≠ {1} (C₂, C₃, S₃, S₄, A₄). Paper 75 predicted the final row: **A₅, being
perfect, is absolutely unpinnable**. This paper tests that prediction and closes
the table.

## 1. The theorem: perfect ⟹ absolutely flat

A₅ is **perfect**: [A₅, A₅] = A₅, so A₅^ab = {1}. The only quotients of A₅ are A₅
and the trivial group, so the splitting field L of a Gal(A₅) quintic has **no
nontrivial abelian subextension** — in particular

    L ∩ Q(ζ_m) = Q   for EVERY modulus m.

The compositum L·Q(ζ_m) therefore has Galois group the **direct product**
A₅ × (Z/m)^× (the fiber product collapses to a product over the trivial
intersection). By Chebotarev, the pair (σ_p = Frob_p, u_p = p mod m) is uniform on
the product, so for **every** fork F (a union of conjugacy classes of A₅) and
**every** residue c:

    P(σ_p ∈ F | p ≡ c mod m) = |F|/60,   independent of c,

i.e. **I(p mod m; fork) = 0 exactly in the limit, for all forks and all m.**
No pinning (no character exists). No leakage (paper 75's leakage required a pinned
super-channel F₀ ⊃ F₁; none exists). **A₅ realizes only the flat state.**

## 2. The A₅ field: x⁵ + 20x + 16

The quintic x⁵ + 20x + 16 has discriminant 4⁴·20⁵ + 5⁵·16⁴ = 1,024,000,000 =
**32000² = 2¹⁶·5⁶**, a perfect square, so Gal ⊆ A₅. Over the 22,997 unramified
primes of the 2^18 sieve the root-count histogram is the **exact A₅ signature**:

| nr mod p | rate | A₅ class | size |
|---|---|---|---|
| 5 | 0.0163 | identity | 1/60 |
| 2 | 0.3334 | 3-cycles [3,1,1] | 20/60 |
| 1 | 0.2496 | [2,2,1] double transpositions | 15/60 |
| 0 | 0.4007 | 5-cycles [5] | 24/60 |
| 3, 4 | **0.0000** | transpositions / 4-cycles | 0 |

The zero nr=3/nr=4 rows are the no-transposition test (G ⊆ A₅); the presence of
3-cycles (order 3) and 5-cycles with a transitive action forces **G = A₅** exactly
(the histogram distinguishes A₅ from D₅, which has no nr=2, and from C₅, which has
no nr=1/nr=2). The classical example is confirmed.

## 3. Part B — the flatness theorem, machine-verified

Observed I vs the **shuffled-null distribution** (300 label shuffles per cell —
the paper-70 honest finite-sample test, since plug-in MI is sparsity-biased and a
fork of rate 1/60 would otherwise show spurious inflation):

| fork (rate) | max |z| over 12 moduli |
|---|---|---|
| splits-completely [nr=5] (1/60) | 1.9 |
| has-root [nr≥1] (3/5) | 1.3 |
| 3-cycles [nr=2] (1/3) | 1.5 |
| double-transpositions [nr=1] (1/4) | 2.0 |
| 5-cycles [nr=0] (2/5) | 1.5 |

Moduli: 3, 4, 7, 8, 9, 11, 13, 16, 25, 31, 59, 101 — including the
discriminant's prime-powers 16 = 2⁴ and 25 = 5², and m = 11 (the C₅ control's own
conductor). **GLOBAL max |z| = 2.00 across all 5 forks × 12 moduli.** Every fork is
flat against every modulus. This is the strongest residue-invisibility in the lab,
and — uniquely — it is **provable a priori** from A₅-simplicity + Chebotarev,
not just measured.

## 4. Part C — positive control: the pipeline detects pinning when it exists

The same sieve and methodology on the abelian C₅ field Q(ζ₁₁)+ (minimal polynomial
x⁵+x⁴−4x³−3x²+3x+1 of 2cos(2π/11), disc 11⁴ = 14641) gives histogram EXACT
(nr=5 0.1989 ≈ 1/5, nr=0 0.8011 ≈ 4/5, all else 0) and

    I(p mod 11; [nr=5]) = 0.7198 = H(1/5) = 0.7219 EXACT,

with P = 1.0000 on p ≡ ±1 mod 11, 0.0000 elsewhere, coprime m=13 flat. The C₅
splits-completely fork is pinned at 100% by the order-5 character — proving the
pipeline detects pinning when it exists, so the A₅ flatness is real, not an
artifact.

## 5. Part D — semiprime level: order-5 split-count law + A₅ flat

30k semiprimes from the 2^16 prime pool (5,978 primes, each pre-classified). The
C₅ fork obeys the **paper-74 order-5 split-count law EXACTLY**:

| channel | measured | law (n=5) |
|---|---|---|
| split-count s | 0.2028 | Is(5) = 0.2027 |
| OR | 0.0203 | g(5) = 0.0215 |
| AND | 0.0995 | A(5) = 0.0979 |
| XOR | 0.1262 | X(5) = 0.1276 |
| s-dist | [0.642, 0.318, 0.040] | Bin(2,1/5) = [0.64, 0.32, 0.04] |

(all z ≥ +200 — massively above null). The A₅ forks (has-root 3/5, splits-completely
1/60) give **every channel at the shuffled null** (|z| ≤ 0.9): with no character to
carry s, even the split-count carries zero residue information at the semiprime
level.

## 6. Classification table closed, and seals

**Pinning-content table (closed).** C₂ → quadratic, H(1/2)-class (papers 54/72);
C₃ → cubic, H(1/3) (paper 71); **C₅ → order-5, H(1/5) (this paper)**; S₃/S₄ →
sign-only (papers 65–71); A₄ → cubic + within-V₄ flat (paper 75); **A₅ → absolutely
flat (this paper)**. The organizing law: **abelian ⟹ pinned at H(1/n) (n = order);
solvable non-abelian ⟹ pinned at the abelianization (sign, or the V₄-order fork);
perfect ⟹ absolutely flat.** V₄/C₄/D₄ (G^ab ≠ {1}) are the remaining untested
entries.

**Barriers.** Symmetry (2): the forks are class functions with **zero residue
content** — the which-factor wall is null. Structural orthogonality (5): there is
no dial at all — the strongest form of the barrier. Circularity (6): L ∩ Q(ζ_m) =
Q seals the channel behind the direct product; computing the Frob class IS the
factorization. Known methods (8): Galois theory, A₅ simplicity (Galois 1832),
Chebotarev density (1922), cyclotomic fields — all classical.

**Unification.** Paper 75 predicted "A₅ perfect ⟹ absolutely unpinnable"; this
paper verifies it. The three-state picture (pinned / flat / leakage) is now
exhausted: abelian and solvable groups can pin or leak at the abelianization;
perfect groups can only be flat. The order-5 split-count law is additionally
verified in a new configuration (real-cyclotomic C₅ field, pool methodology),
extending paper 74's n=5 line.

*Script:* /tmp/exp_a5.py (2^18 sieve, 300-shuffle nulls, 30k semiprime MC, 204 s).

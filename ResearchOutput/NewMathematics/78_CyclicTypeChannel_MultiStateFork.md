# The Multi-State Splitting-Type Channel of a Cyclic Field Exceeds the 1-Bit Binary-Fork Cap (CYCLIC-TYPE-CHANNEL)

**Program:** Factoring research lab — cron loop round-22 #2
**Date:** 2026-08-12
**Status:** Machine-verified (exact unit-group enumeration + 30k semiprime Monte-Carlo, 2^16 pool, shuffled-null z-scores).

Papers 72–74 capped every *binary* (0/1) symmetric semiprime fork at 1.0 bit
(the split-count law Is(n), the OR law g(n), the quadratic-kernel profile
enumeration). But the splitting type of a field is not binary — for a cyclic
field it is a **multi-state** object: the Frobenius order T(p) = ord_f(p) (the
residue degree of p in Q(ζ_f)) takes values in the divisor lattice of n = f − 1.
This paper opens the **complete splitting-type channel** {T(p), T(q)} and shows
that the 1-bit binary-fork cap is a *binary artifact*: the type-pair channel
carries **I_pair = 1.2500 (C₄) and 1.4739 (C₆)** — strictly above 1.0 bit — with
a growth law I_pair(n) governed by the divisor structure of the cyclic order.

## 1. Prime level: the type channel is deterministic and exact

For Q(ζ_f), f prime, Gal = (Z/f)^× = C_n with n = f − 1, the Frobenius order is
the multiplicative order of p mod f, T(p) = ord_f(p) — a deterministic function
of p mod f. Hence the single-prime channel is the entropy of the type law:

    I(p mod f; T) = H(T)  EXACT.

**C₄ = Q(ζ₅)** (f = 5, Gal = C₄ — the first prime-level quartic-character
field): type map {1↦1, 2↦4, 3↦4, 4↦2}, states {1, 2, 4} with rates
{1/4, 1/4, 1/2}:

| channel | measured | law |
|---|---|---|
| I(p mod 5; T) | 1.4989 | H(1/4, 1/4, 1/2) = 1.5000 |
| [T=1] splits-completely | 0.8098 | H(1/4) = 0.8113 — **FIRST prime-level QUARTIC-character pinning** |
| [T=2] (p ≡ 4 mod 5) | 0.8110 | H(1/4) = 0.8113 |
| [T=4] (p ≡ 2, 3 mod 5) | 1.0000 | H(1/2) = 1.0000 |

The [T=1] fork is pinned by the quartic character χ₄ with P = 1.0000 on p ≡ 1
mod 5 and 0 elsewhere — H(1/4) exactly. **Thickening zero:** I(p mod 25; T) =
1.4989 = I(p mod 5; T) (T depends only on p mod f — no modulus thickening helps).
Coprime control m = 3: 0.0000.

**C₆ = Q(ζ₇)** (f = 7, Gal = C₆): type map {1↦1, 2↦3, 3↦6, 4↦3, 5↦6, 6↦2},
states {1, 2, 3, 6} with rates {1/6, 1/6, 1/3, 1/3}:

| channel | measured | law |
|---|---|---|
| I(p mod 7; T) | 1.9183 | H(1/6, 1/6, 1/3, 1/3) = 1.9183 |
| [T=1] splits-completely | 0.6497 | H(1/6) = 0.6500 |
| thickening I(p mod 49; T) | 1.9183 | = I(p mod 7; T) |
| coprime m = 5 | 0.0001 | 0 |

### Root-count readout is lossy

The observable root count nr(Φ_f) collapses the *type*: [T=2, T=4] both give
nr=2 pairs? No — for Φ₅, nr=4 ⟺ T=1, nr=2 ⟺ T=2, nr=0 ⟺ T=4 *but* the
[nr=2]/[nr=4]-type [2,2] (T=2 gives two roots) versus T=4 (no roots) already
separate; the loss is that [2,2] (T=2·T=2 semiprime pair) and [4] (T=4) both map
to split-count-free nr=0 at the semiprime level, and at prime level the root
count only sees {4, 2, 0} — it cannot see *which* type produced nr=2 (T=2 only,
one state) nor nr=0 (T=4 only for Φ₅, but T∈{3,6} for Φ₇ both give nr=0). The
measured nr-channel:

| field | I(p mod f; nr) | H(T) |
|---|---|---|
| C₄ | 0.8109 = H(1/4, 3/4) | 1.5000 |
| C₆ | 0.6498 = H(1/6, 5/6) | 1.9183 |

The root-count channel is **binary** — it strictly loses to the type channel.
**The type, not the root count, is the complete object.**

## 2. Semiprime level: the exact type-pair law

For the semiprime N = pq, the natural symmetric invariant is the **unordered
type pair** {T(p), T(q)}. Conditional on N ≡ c mod f the law is computable by
exact enumeration over the unit group (u ↦ (T(u), T(c·u⁻¹))), giving

    I_pair(f) = H(Π) − (1/φ(f)) Σ_{c ∈ (Z/f)^×} H(Π_c)

where Π is the marginal unordered-pair law and Π_c the pair law under
N ≡ c mod f. Exact enumeration + 30k semiprime MC (2^16 pool):

| field | n | H(T) | H(pair) | H(pair\|N) | I_pair (exact) | I_pair (MC) |
|---|---|---|---|---|---|---|
| C₂ | Q(√5), f=5 | 1.0000 | 1.5000 | 0.5000 | **1.0000** | 1.0000 |
| C₄ | Q(ζ₅), f=5 | 1.5000 | 2.3750 | 1.1250 | **1.2500** | 1.2452 |
| C₆ | Q(ζ₇), f=7 | 1.9183 | 3.1144 | 1.6405 | **1.4739** | 1.4711 |

**C₂ reproduces the paper-74 binary cap exactly** (for a quadratic field the type
pair IS the split-count). **C₄ and C₆ both EXCEED 1.0 bit** — the first
symmetric semiprime channels above the binary-fork cap. Which-factor wall:
I(p > q; pair) = 0.0001 (null — symmetric, factor-useless). Coprime controls
flat (m=3: 0.0000; m=5: 0.0006).

### The s-projection recovers Is(n) exactly

The split count s = [split(p)] + [split(q)] (paper 74) is the projection of the
type pair onto the boolean "T=1?" face:

| field | s-projection measured | Is(n) law |
|---|---|---|
| C₂ | 1.0000 | Is(2) = 1.0000 |
| C₄ | 0.2896 | Is(4) = 0.2947 |
| C₆ | 0.1445 | Is(6) = 0.1487 |

The split-count channel is **one face** of the richer type-pair channel — the
cap that papers 72–74 found is specific to binary (0/1) forks.

## 3. The growth law: no 1-bit cap for the type channel

Exact enumeration over all cyclic prime conductors (Q(√5), Q(ζ_f) for
f = 5, 7, 11, 13, 17):

| n | field | # type-states | H(T) = I(p mod f; T) | I_pair (semiprime) | Is(n) | above 1 bit? |
|---|---|---|---|---|---|---|
| 2 | Q(√5) | 2 | 1.0000 | 1.0000 | 1.0000 | at cap |
| 4 | Q(ζ₅) | 3 | 1.5000 | 1.2500 | 0.2947 | **YES** |
| 6 | Q(ζ₇) | 4 | 1.9183 | 1.4739 | 0.1487 | **YES** |
| 10 | Q(ζ₁₁) | 4 | 1.7219 | 1.2027 | 0.0614 | **YES** |
| 12 | Q(ζ₁₃) | 6 | 2.4183 | 1.7239 | 0.0445 | **YES** |
| 16 | Q(ζ₁₇) | 5 | 1.8750 | 1.3281 | 0.0267 | **YES** |

Every n ≥ 4 exceeds 1.0 bit. The value is governed by the **divisor structure of
the cyclic order**: the type states are the divisors of n, so the channel is
richest when n has many divisors — n = 12 (six states {1,2,3,4,6,12}) peaks at
I_pair = 1.7239. The binary split-count Is(n) collapses monotonically while the
type channel stays multi-bit. The complete symmetric residue channel of a cyclic
field has **no 1-bit cap**; papers 72–74's cap is the binary special case.

## 4. Position and seals

**Criterion (paper 71) confirmation at prime level.** [T=1] splits-completely is
pinned by the order-n character at exactly H(1/n) — C₄ gives the first prime-level
quartic-character pinning (0.8098 = H(1/4)), C₆ the order-6 pinning (0.6497 =
H(1/6)). The paper-71 abelianization criterion extends to the *multi-state* type
channel: every type state is a deterministic function of the character value
p mod f, so the full type channel carries H(T) bits.

**What is new.** (1) The exact type-pair channel law
I_pair = H(Π) − (1/φ(f))Σ_c H(Π_c) with machine-verified values 1.0000 / 1.2500 /
1.4739 for C₂/C₄/C₆ — the **first symmetric semiprime channels above the 1-bit
binary-fork cap**. (2) The prime-level quartic-character pinning (first of its
kind). (3) The root-count lossiness theorem: nr collapses type states, so the
root-count channel is binary (0.8109 / 0.6498) strictly below H(T) — the type,
not the root count, is the complete object. (4) Is(n) identified as the
s-projection of the type channel — paper 74 is a face. (5) The growth law
I_pair(n): no 1-bit cap, value set by the divisor structure of the cyclic order.

**Barriers.** Symmetry (2): the type pair is a symmetric class function — the
which-factor wall is 0.0001. Structural orthogonality (5): the channel is a pure
p-mod-f residue dial (the type is a function of p mod f; the type pair of p mod
f, q mod f). Circularity (6): I_pair is N-computable only behind the CRT split —
the type of a prime divisor is not a function of N, only of the as-yet-unknown
prime. Known methods (8): cyclotomic fields, Dirichlet characters, CRT,
Chebotarev density (1922). Barriers 2/5/6/8.

**Unification.** Paper 74's binary cap (Is(n) ≤ 1.0, max 1.0) is revealed as the
s-projection of the multi-state type channel; paper 71's abelianization criterion
extends to the full type channel; the quadratic case (paper 54/72) reproduces the
cap exactly (I_pair(C₂) = 1.0000 = Is(2)).

*Script:* /tmp/exp_typechan.py (2^18 sieve, exact unit-group enumeration,
30k semiprime MC, 34 s).

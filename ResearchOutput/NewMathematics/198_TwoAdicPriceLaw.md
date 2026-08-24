# Paper 198 — TWO-ADIC-PRICE-LAW: Two Clicks of Visibility, Then Sealed

**Verdict name: TWO-ADIC-PATH-TWO-CLICKS-THEN-SEALED.**
Round-71 #1 · exp 552 · assessment v305 · script `ResearchOutput/scripts/2026-08-21-resume/exp552_two_adic_price.py` (+ `exp552_result.json`, `run_exp552.log`) · seed 20260825 · coordinator fresh-seed replication 1200/1200.

## 1. The exact map (derived before measurement; verified 100%)

With U = p+q, V = q−p and u₀ = v₂(U):

| law | statement | verification |
|---|---|---|
| position 0 | letter₀ = A ⟺ **N ≡ 1 (mod 4)** | 4000/4000 + 1200/1200 fresh |
| position 0, N≡3 | letter₀ = B iff q < 3p else C — a SIZE rule, not residue-determinable | 100% |
| position 1 | letter₁ = A ⟺ **N mod 8 ∈ {1, 3}** | 100% |
| bijection | (A₀, A₁) ↔ N mod 8 exactly: (A,A)↔1, (A,¬A)↔5, (¬A,A)↔3, (¬A,¬A)↔7 | 100% both populations |

## 2. The mechanism

Every Price step halves exactly one of U or V: **A halves V and is admissible iff
v₂(U)=1 (it sees V); B/C halve U, admissible iff v₂(U)≥2 (they see U)**, with B-vs-C
the sign of V−U/2 — a size comparison, never a congruence. Non-A runs decrement v₂(U)
by exactly 1, so **the first A lands at position u₀−1**. N mod 2^k reads u₀ only
capped at {1, 2, ≥3}: higher bits are scrambled by the unknown odd factor
(N = 2^j·po − p²). Hence exactly two residue-visible clicks.

## 3. Death at position 2 — provably

Conditional given the path prefix, permutation nulls have ZERO variance at t=2, 3, 5:
N mod 8 is constant inside every prefix cell by the bijection — an EXACT structural
death, not a statistical fade. Marginal z-ladder: t=0 z=1438, t=1 z=1626, then
leakage tail 0.035/0.003/0.003/0.002 bits (z ≤ 52 decaying to noise). No supported
N mod 2^k cell (k≤8) is pure in any letter_t for t≥2.

## 4. Factor-blindness and family placement

Which-factor wall HOLDS: labeled-letter-pair channel above null by 0.0003 bits
(z=+0.36); exploratory full-path channel z=+1.36 (sensitivity 0.0096 bits) — joins
the sealed residue-dial family (barrier 5), symmetric per standing laws.
Symmetric capacity I(N mod 2^k ; unordered pair) = 0 / 0.524 / 1.523 / 1.524 / 1.525
bits for k=1..5 — **saturates exactly at modulus 8** (+0.00057 from mod 16); best fit
is the order-universal abelianization/type-channel family (the channel factors
through Z/8). Per-class outcomes: 1→{AA}, 3→{AB,AC}, 5→{AB,AC}, 7→{BB,BC,CC}.
B-rarity explained: P(B) = ½·P(q<3p) — round-70's .05 marginal was stratum composition;
mechanism identical.

## 5. The completed two-tree adic map

Berggren letters: sealed at the 3-adic place from position 0 (paper 81) and against
every magnitude probe (papers 196–197). Price letters: visible EXACTLY two clicks at
the 2-adic place (this paper) — then structurally sealed, and factor-blind throughout.
Both trees' cheap descriptions are residue dials; neither offers an ascent route.

Coordinator replication note: fresh seed 777 population, independent descent code,
all three laws + re-ascent exact 1200/1200.

Now 550 experiments (max id). Assessment v305.

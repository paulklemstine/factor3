# Paper 132 — CONVERSE-CAP-THEOREM: The Barrier-4 Converse for the Residue-Dial Stratum

**Verdict name: CONVERSE-CAP-PROVED-STRONGER.**
Round-37 #4 · exp 466 · assessment v241 · proofs `ResearchOutput/scripts/2026-08-21-resume/proofs.md` · verification `verify.py` / `result.json` · seed 20260821.

## 1. The theorem

Frontier (i)'s converse — "factor-revealing ⟹ expensive" — is proved for the entire
congruence stratum. Model: keep-set filters, i.e., complete factorization procedures that
scan candidates in an order determined by an arbitrary function K_c ⊆ (Z/MZ)^× of the joint
residue reading c (any number of composed dials; per-candidate tests = residue evaluation +
division). Under explicit Model Assumption MA-1 (pair-equidistribution of primes among
reduced residue classes; asymptotically unconditional via Siegel–Walfisz), with the ½-split
step exact by exchangeability:

> **Universal exact law (Thms B/C):** Speedup(K, c) = **1/(1 − θ + θ²)**, where
> θ = |K_c|/φ(M) — independent of c, of M's structure, of character content, and of k.
>
> **Universal cap:** max = **4/3**, attained exactly at θ = ½; trivial filters give exactly 1.

Consequences:
- n=2 (quadratic dials): cap 4/3 at the quadratic cosets — the conjecture confirmed.
- n=3/n=5: cap ALSO 4/3 at ANY half-density subset (20 of 64 at m=7; 252 of 1024 at m=11) —
  Lemma B2 [P(min ∈ K | c) = θ identically] kills all internal structure; mixing character
  fibers cannot beat it (cubic-fiber sets give only 9/7 ≈ 1.2857).
- **Batteries compose for free** (CRT: k dials = one dial mod Πmᵢ): battery cap STILL 4/3 < 2.
  **The 12.7235 measured battery bits buy ≤ log₂(4/3) = 0.41504 work-bits** — a constant.
  Capacity bits and work bits are different currencies.
- Corollary A2: which-factor blindness of residues (papers 93/102, z ≈ 0 walls) becomes an
  IDENTITY under MA-1 — the empirical walls were measuring an exact symmetry.

## 2. Machine verification

- Claim-A uniformity: MC 1,065,538 samples at m=31, per-cell max |dev| from 1/30 = 0.000294,
  χ²(30) z = −1.67.
- Exhaustive subset enumeration m = 3/4/7/11 and batteries M = 12/15/21 plus vectorized M = 33
  (all 2²⁰ subsets): EVERY maximum = 1.3333333333, closed-form error 0.0, argmax = exactly the
  half-density subsets; m=31 random-5000 search never exceeds the cap.
- Real-semiprime simulations (20k per config): optimal half-sets 1.3354/1.3336/1.3379
  (pred 4/3); cubic-kernel 1.2821 with size-2 non-character control 1.2873 (pred 9/7 BOTH —
  structure-blindness confirmed); quintic kernel 1.1959 (pred 25/21); battery half-set 1.3334;
  character-aligned battery set 1.1592 (pred 36/31). All within ±0.006.
- Beat-the-cap attempt over the top-40 predicted cap-attaining battery sets: mean 1.3343,
  max 1.3461 (selection-inflated) — nothing approaches 2×.

Cross-check with exp 461 (paper 131): its measured 1.25 at θ=½ sits below the 4/3 cap (the toy
population-window artifact); once membership overhead is priced, both accounts agree every such
filter is a net loss (~0.5×).

## 3. Scope and the residual gap

Sealed: any filter whose scan order is a function of N's residues modulo fixed (even
poly(log N)-bounded) moduli. Open, stated precisely: (1) witnesses whose ordering uses N beyond
fixed residues — interval hints, Coppersmith position conditions, quadratic-form position
information (paper 88 arms these empirically at 2e4–3e5 ops/factor-bit; no theorem yet);
(2) superconstant-cost per-candidate tests — factor-local methods (ρ/ECM) escape scan-order
framing entirely; (3) effectivizing MA-1 (Siegel-zero ineffectivity) for explicit constants at
cryptographic sizes. The full barrier-4 converse is reduced to exactly these three items.

Barriers: (2) the uniformity IS the multiplicative symmetry made algorithmic; (4) aggregation
(batteries, synergy excesses included) is priced by the composition step — capacity compounds,
utility does not; (5) upgraded from which-factor-blindness to POSITION-blindness of residues;
(8) the disguise is priced exactly: reorder value ≤ 4/3, worth 0.415 work-bits.

## Method ledger (self-caught)

(1) First cost model charged phase-1 overshoot → speedups below 1, contradicting the anchor —
replaced with the position-of-min functional; (2) nearly reported the asked "≤2" instead of the
provable 4/3; (3) hand-mislabeled θ for the aligned battery set — machine counting caught it
(err 0.07 → 0.002); (4) finite-pool class imbalance gave χ² z=+5.1 — fixed by per-class pool
trimming → z=−1.67; (5) real-prime half-set speedups sit +0.002..+0.005 above 4/3 (prime-race
scale) — documented as the honest deviation from MA-1/MA-2.

Now 464 experiments. Assessment v241.

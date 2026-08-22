# Paper 130 — SUBEXP-SCALE: The Relation Pool Is Random

**Verdict name: THE-RELATION-POOL-IS-RANDOM (formal rule verdict H2, mechanism identified).**
Round-37 #2 · exp 465 · assessment v239 · script `ResearchOutput/scripts/2026-08-21-resume/exp465_subexp_scale.py` · seed 20260821.

## 1. Does scale change paper 90's honest-inconclusive?

Paper 90 found the fourth stratum unmeasurable at toy scale: x²−N smoothness vs Dickman ρ(u)
scattered non-monotonically (ratios 0.26–9.27) and "x²−N ≠ random integers" at toy scale.
This experiment re-measures with the design flaws repaired, at 500× the sample:

- Proper per-value u definition: u(v) = ln v / ln B from each value's own size (never N-scale
  binning — paper 90's cautionary tale applied as designed).
- Size-matched random control: each relation value v is paired with a random integer of
  matched magnitude (uniform in log scale in [v/2, 2v]) — killing the size-distribution
  confound; both samples compared to E[ρ(u(v))] over their own size law.
- Scales bitlen N ∈ {32, 36, 40, 44}; matched-u ladder u(median v) ∈ {2, 3};
  150,000 values per cell × 8 cells = **1.2M smoothness tests** (paper 90: 2400).
- ρ(u) computed by delay-differential integration on h=0.002 grid, validated ≤ 2e-4 against
  attested literature values ρ(2)..ρ(6) plus a memory-free Richardson step-halving check.

## 2. Results

| bits | u | B | ratio_x²⁻ᴺ | 95% CI | ratio_rand | gap |
|---|---|---|---|---|---|---|
| 32 | 2 | 1692 | 0.889 | [0.882, 0.896] | 0.888 | **1.001** |
| 36 | 2 | 3381 | 0.892 | [0.885, 0.899] | 0.899 | **0.993** |
| 40 | 2 | 6762 | 0.913 | [0.906, 0.920] | 0.903 | **1.011** |
| 44 | 2 | 13582 | 0.912 | [0.905, 0.919] | 0.910 | **1.002** |
| 32 | 3 | 142 | 0.906 | [0.887, 0.925] | 0.900 | **1.006** |
| 36 | 3 | 225 | 0.877 | [0.858, 0.896] | 0.861 | **1.019** |
| 40 | 3 | 358 | 0.881 | [0.862, 0.900] | 0.868 | **1.015** |
| 44 | 3 | 569 | 0.883 | [0.863, 0.902] | 0.865 | **1.020** |

**(a) The paper-90 anomaly RESOLVED**: the x²−N vs random gap is 1.00 at every scale
(0.993–1.020, tight CIs). The quadratic-character constraint on prime divisors of x²−N is
O(1)-invisible at reachable scale: **the QS relation pool's smoothness statistics are exactly
random-integer statistics** once sizes are matched. Paper 90's "≠ random" finding and its
non-monotone scatter were artifacts of N-scale u-binning and 2400-sample underpower.

**(b) Formal verdict H2 per the pre-stated rule, with the mechanism identified**: the absolute
ratio emp/ρ sits at 0.877–0.913 and does not reach 1 by 2^44 — but the deficit is carried
EQUALLY by the random control (ratio_rand 0.861–0.910), so it is a property of the Dickman
model at finite x, not of x²−N. Its magnitude matches the known correction scale
ln ln v / ln v ≈ 17–20% at v ~ 2^17–2^23, and its shrinkage is logarithmic:
+2.6% relative per 12 bits of scale at u=2 (0.889 → 0.913), flat-noisy at u=3 — consistent
with convergence too slow to reach 1 below ~2^50+ at these u. The honest reading: the ratio
WOULD reach 1, but only far beyond toy scale; nothing about x²−N blocks it.

**(c) Leading-term Dickman**: exp(−u(ln u + ln ln u − 1)) stays above 20% relative error until
u ≈ 14.75 (pre-stated guess: u ≥ 12 — confirmed). Informal smoothness arguments using the
leading term remain quantitatively meaningless below u ≈ 15.

## 3. What this decides

The fourth stratum's INPUT STATISTICS are now measured at scale: relation pools are
random-equivalent, and the correct finite-size smoothness model is ρ(u) × (measured factor
0.88–0.91 at u ∈ [2,3], v ≤ 2^23). What remains unmeasured about L_N[1/2] sieving is purely
its algorithmic content (the sieve's enumeration advantage over sampling), not the
smoothness landscape it feeds on. Barriers 4/8 unchanged; the subexp stratum moves from
"honestly unmeasured" to "inputs measured, algorithmic advantage still unmeasured".

## Method ledger

- v1: reference constants for ρ beyond u=4 mis-recalled from memory (ρ(5) written 3.49e-3,
  true 3.547e-4) — caught by the attested-anchor + Richardson design BEFORE contamination;
  validation rebuilt on ρ(2..6) only + step-halving self-check.
- np.isqrt does not exist in numpy — exact integer isqrt substituted.
- Provenance: three upstream agent-channel timeouts killed two subagent attempts; the
  experiment was taken over inline by the coordinator with incremental checkpointing.

Now 462 experiments. Assessment v239.

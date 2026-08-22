# Paper 136 — TOY-QS-YIELD: The Sieve's Advantage Is the Survivor Filter — and the Relation Pool Is QR-Restricted Random

**Verdict name: H1-CONFIRMED_H2-REFUTED (the refutation refines paper 130).**
Round-38 #2 · exp 470 · assessment v245 · scripts `ResearchOutput/scripts/2026-08-21-resume/exp470_toy_qs_yield.py` (+ `exp470_verify.py`, `result.json`) · seed 20260821.

## 1. The sieve's algorithmic advantage, first measured

Paper 130 left the fourth stratum's algorithmic content unmeasured ("inputs measured,
algorithmic advantage still open"). This experiment measures it directly: a minimal plain
QS (log-additive sieving, factor base (N|p)=+1, exact relations) at N ∈ {2^28, 2^30, 2^32},
two windows per scale, compared against naive trial-division cost per relation under
implementation-independent op counts, with an independent brute-force cross-check on a
4096-value subrange.

## 2. Results

**(a) H1 CONFIRMED — no emergent asymptotic advantage at toy scale.** Total advantage
A_total = cost_naive/cost_sieve per relation: 15.29 / 18.63 / 13.68 / 16.33 / 16.90 / 20.51
across the six cells; normalized by factor-base size πFB, A/πFB is FLAT at 0.12–0.22.
Mechanism measured directly: sieving converts ~100 divisibility tests per value into
~2 log-adds per value plus division of survivors only — the shared additive structure along
the line IS the entire advantage, a constant band exactly as pre-stated. Independent
brute-force subrange check: 338/338 smooth values flagged exactly; empirical advantage
14.07× vs full-window 15.29.

**(b) H2 REFUTED, refining paper 130.** The paper-130-corrected yield model ρ(u)×0.90
OVERPREDICTS relation yield by ~1.55×: observed/model ratios 0.540–0.755 (mean
0.645 ± 0.071), 0/6 cells inside the pre-stated [0.80, 1.20] band. Post-hoc reading:
a prime p dividing x²−N must have (N|p) = +1 EXACTLY — B-smoothness of relation values
lives entirely on the QR-restricted prime pool, raising effective-u by ln B/(ln B − ln 2)
≈ 1.06–1.11 and predicting ratios 0.44–0.52 (observed 0.54–0.76; cross-cell correlation
0.72). Paper 130's gap = 1.00 was measured at u ∈ [2,3], v ≤ 2²³, where the QR bite is O(1);
beyond that regime the pool is random-equivalent to **QR-restricted** integers, not
unrestricted ones. Its "relation pool is random" stands as a first-order statement with an
explicit correction term now identified.

**(c) Stretch completed**: GF(2) elimination on the collected relations actually factored
N = 103,764,863 = 9127 × 11369 (product verified) — the pipeline is end-to-end real.

## 3. What this decides

The toy QS cost model paper 90 could not calibrate is calibrated: cost/relation ≈
(lines × U_adds + survivors' divisions)/(yield), yield = ρ(u_eff) with u_eff raised by the
QR restriction ln B/(ln B − ln 2). Follow-up queued: direct smoothness measurement of
x²−N against a QR-restricted reference pool at u ∈ [3,4]. Barrier lines: this MEASURES the
known method (barrier 8); barrier 4 explains why sieving beats sampling without escaping
anything (shared structure, constant band).

Method ledger (9 entries, full text in script docstring): two substantive pre-data bugs were
caught ONLY by the independent brute-force cross-check because the mandated gate's prediction
shared their omission (circularity of self-referential gates): single-prime sieve lines
silently discarded ~20% of true relations with p² | v (fixed by Hensel-lifted prime-power
lines); the lift reused root-0's modular inverse for both roots, killing the −r branch from
level 2 on. Smoke-catch L8: accumulator initialized at log v made everything survive, and u
was computed in mixed bases (log₂(v)/ln B) inflating u by 1/ln2. All fixed before final data.

Now 468 experiments. Assessment v245.

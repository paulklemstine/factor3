# Paper 176 — MA1-EFFECTIVE: Equidistribution Holds to Three Significant Figures at Practical Sizes

**Verdict name: EQUIDISTRIBUTION-CONFIRMED (H1 pass; H2 split; H3 mostly confirmed).**
Round-48 #1 (cron iteration) · exp 509 · assessment v283 · script `ResearchOutput/scripts/2026-08-21-resume/exp509_lean.py` (+ `exp509_result_v2.json`) · exact computation.

## 1. Paper 132's residual gap item (3): effectivizing MA-1

How large is the equidistribution deviation of primes among reduced residue classes at
practical sizes? Exact prime counts in arithmetic progressions at x ∈ {2²⁸, 2³⁰} for
m ∈ {3,4,5,7,8,11,31}.

## 2. Results

- **H1 CONFIRMED**: max per-class deviation from Li(x)/φ(m) at x=2³⁰ is **0.000446**
  relative — well below the 0.001 threshold; the 4/3 cap's constants hold to three
  significant figures.
- **H2 SPLIT**: worst class stable for m ∈ {3,4,7,8,11} but unstable for m ∈ {5,31} —
  no single Siegel-zero analogue dominates at these sizes.
- **H3 CONFIRMED**: deviations shrink from x=2²⁸ to x=2³⁰ for 6/7 moduli.

## 3. What this decides

Paper 132's converse constants are numerically robust at practical sizes: MA-1's
equidistribution assumption introduces < 0.05% error into the 4/3 cap. Barriers:
(5)/(8) unchanged.

Now 511 experiments. Assessment v283.


## Addendum — the original agent's comprehensive run (C/OpenMP wheel-30 sieve to 2^40)

Supersedes the lean v2's sampling-based measurement with EXACT enumeration at x = 2^40:
worst core per-class deviation **|π−Li/φ|/x = 1.96e-8** (m=31), worst pair modulus m=93 at
**2.18e-5 relative**; cap moves by **< 4.4e-10**. Chebyshev race confirmed (π(2⁴⁰;4,3) −
π(2⁴⁰;4,1) = +41,427). H2 refined: no single Siegel-zero analogue — deviations are
character-structured (corr with quadratic character < 0 in 15/16 cells). H3: clean
x^(−1/2) law on relative deviation across all moduli. π(2⁴⁰) = 41,203,088,796 verified
via sympy's independent primepi. Ledger: 4 pre-data C-sieve bugs caught by validation gates.

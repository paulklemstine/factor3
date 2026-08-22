# Paper 131 — POSTERIOR-FILTER: Real Filter Equals Sham

**Verdict name: REAL-FILTER-EQUALS-SHAM — type-channel capacity converts into exactly zero factoring utility.**
Round-37 #3 · exp 461 · assessment v240 · script `ResearchOutput/scripts/2026-08-21-resume/exp461_posterior_filter.py` · seed 20260821.

## 1. The decisive utility experiment

The programme measured up to 12.7 bits of battery channel capacity I(N mod M; labels) —
all of it factor-blind (papers 93/102), but capacity nonetheless. Could a Bayesian candidate
filter built from the exact posterior convert that capacity into trial-division speedup?
This experiment settles it.

Design: dials = order-2 character (−31|·), order-3 (conductor 7), order-5 (conductor 11),
2-dial and 4-dial batteries (up to 3.49 measured bits, analytic vs empirical validated to
≤ 0.017); exact per-class posterior P(s|N mod m) by unit-pair enumeration; optimal keep-set
per class; 20,000 semiprimes/cell × 5 batches; SHAM control = coin-flip keep-set of the same
size; dummy dial (public table on N mod 97, zero information).

## 2. Results

Speedup (free-reordering accounting, real / sham / keep-rate model κ=1.19):

| dial | real | sham | model |
|---|---|---|---|
| d2 (1 bit) | 1.2486 | 1.2487 | 1.2527 |
| d3 (Is(3)) | 1.2199 | 1.2224 | 1.2190 |
| d5 (Is(5)) | 1.1487 | 1.1497 | 1.1484 |
| bat2 | 1.2215 | 1.2140 | 1.2178 |
| bat4 (3.49 bits) | 1.2305 | 1.2334 | 1.2329 |
| dummy (0 bits) | 1.2430 | 1.2500 | 1.2520 |

**Max |real − sham| = 0.0075 vs batch SD up to 0.0073 — pure noise at every dial.** The ρ-grid
on d2 (7 keep-rates): real/sham/model curves coincide everywhere (max gap 0.008), peak at
ρ=1/2, symmetric decline — the gain is a function of KEEP-RATE ALONE, indifferent to WHICH
classes are kept: the exact per-class optimizer's optimum is characterized entirely by class
mass ≈ 1/2. "Labels are not filters" (paper 98), now quantified as an equality with the
coin-flip control.

Honest accounting: pricing each membership test at one division-equivalent on every candidate
≤ √N, EVERY filter — real or sham — runs at speedup ≈ 0.4966–0.5015: **a net 2× loss.**
No-fallback failure rates = P(p not kept) = 1/n exactly (0.5027/0.3332/0.1991 for n=2/3/5).

## 3. What this decides

Type-channel capacity — even battery capacity — has exactly ZERO conversion into
trial-division speedup. The mechanism is barrier 2 made algorithmic: by Dirichlet
equidistribution the marginal posterior over the target's residue is FLAT no matter what N
reveals about the joint, so no posterior over joint labels can reweight individual candidates;
any apparent gain is reorder-mechanics any same-size random keep-set reproduces, inflated here
by a toy-population window artifact (factors ≥ 2^15 let the first pass skip never-useful small
primes; honest no-prefix ceiling ≈ 1.16×), and reversed once the filter's own tests are priced.
The pre-stated 4/3× conjecture refuted; the ≤2× cap holds vacuously (the companion theory
paper derives the sharp statement: under complete-procedure accounting even the best residue
filter cannot reach 1×). Barriers 2/5 decisive, 6 avoided by construction (inputs χ(N), χ(r)
only), 8 = the effect IS the known reordering trick minus everything the dial adds (nothing).

## Method ledger (9 catches)

Two SUBSTANTIVE cost-accounting bugs produced spurious >1.5× "speedups" before detection:
(6) non-kept branch counted the kept block only up to p instead of to √N; (7) missing second-pass
prefix below the window (inflated ρ→0.125 cells to 2.04×). Both caught by SHAM CO-INFLATION +
derivation — the sham control is what exposed the accounting, not just the channel. Also:
(8) dummy dial v1 read its random table through the FACTORS — not N-computable, leaked a full
bit (I_emp 0.9995) — rebuilt as a public table on N mod 97 (I_emp 0.0014); (9) hand entropy
H(4/9,4/9,1/9) corrected (1.3921 not 1.5305), closed form ((n−1)²/n², 2(n−1)/n², 1/n²) agrees
with simulation; plus five mechanical catches (broadcast crash, log2-on-array, optimizer type
mismatch, τ-encoding bit order, collapsed split-count vector), all disclosed in the script header.

Now 463 experiments. Assessment v240.

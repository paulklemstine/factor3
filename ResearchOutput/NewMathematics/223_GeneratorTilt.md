# Paper 223 — GENERATOR-TILT: The Λ-Channel Is ADVERSARIAL Off-Balance (H1 Refuted Decisively — RSA-Style Pools Read z = 0.636 Top-Heavy and Window-Ascending LOSES ~44%) — Paper 221's Named Follow-up L7-a CLOSED, the Reorder-Class Map Now Has Measured Scope Boundaries End-to-End

**Verdict name: H1 REFUTED DECISIVELY / MIXED-PARTIAL by literal rules** for
exp575, the measurement named by paper 221 as its highest-value open step (**L7-a:
measure the real generator tilt of deployed populations**). The question was
whether the within-window divisor-mass bottom-heavy tilt that powers the 1.58x
window-ascending win under hard q<2p balance (paper 221/L7′) exists in realistic
generator classes. It does not — it INVERTS. On independent same-bitlen prime
pairs (the deployed-style cell) the within-window mass is **top-heavy**
(z = 0.6356 [0.6150, 0.6562], excluding 0.5 from ABOVE): ratio concentration near
1 pushes min(p,q) HIGH into (√(N/2), √N], and window-ascending **loses ~44%** to
sqrt-descending (S = 0.5578 ± 0.0217). The consequence is recorded plainly:
**Λ-dominance is CONFINED TO ARTIFICIAL HARD-BALANCE POOLS; real generator classes
tilt ADVERSARially, so no deployable reorder-class gain exists without ENFORCED
q<2p balance at key-generation time — and no deployed generator enforces it.**
Paper 221's caveat is upgraded from "tilt unmeasured" to "tilt adversarial
off-balance": final word on the Λ-channel scope question.
Round-77 #1 · exp **575** · count advances 563 → 564 · assessment v330 · script
`exp575_generator_tilt.py` · canonical artifact `exp575_result.json` · b=15
(primes in [16384, 32768]; wide pool [8192, 65536]) · n=600/pool · fixed seed
20260824 · exact-uniform prime sampling via sieve index (replaces randprime's
rejection loop; distributions identical in law) · touch-count cost model verbatim
from `verifyL7_sim.py` · 8-batch cluster bootstrap SEs · wall ≈ instant.

## Pre-registration (verbatim from result.json)

> **H1**: "RSA-style pool mean within-window divisor-mass z < 0.45 with CI95
> excluding 0.45 => Lambda-dominance scope covers deployed-like generation"
> **H0**: "RSA-style z ~= 0.5 with CI covering 0.5 => confined to artificial
> hard-balance pools; paper-221 caveat final"
> **rules**: "H1 <=> mean<0.45 and CI95_hi<0.45; H0 <=> CI95 contains 0.50;
> else MIXED/PARTIAL"

The rules were applied exactly as registered and were not modified. The measured
RSA_INDEP interval excludes both candidate bands from above, which the literal
rules score MIXED/PARTIAL; the consequence section below states the refined
reading, also disclosed post-smoke in JSON honest_notes as a descriptive readout.

## Design

Four pools × 600 draws, chosen to span the r = max/min law's width axis:

| pool | generator | role |
|---|---|---|
| HARD_BAL | p~U primes[2^14,2^15); q~U primes(p,2p) | positive control (paper-221/L7′ regime) |
| RSA_INDEP | p,q indep U primes[2^14,2^15), p≠q, sorted | deployed-style cell (the L7-a target) |
| RATIO4 | p~U primes[2^14,2^15); q~U primes[3.5p,4.5p) | narrow-stratum extremal check |
| UNIFORM_WIDE | p,q indep U primes[2^13,2^16), sorted | wide-band uniform proxy |

Window adaptations for RATIO4/UNIFORM_WIDE use N-computable CONSTANTS from the
declared pool supports (r_max ∈ {4.5, 8.0}), chosen before the run, not fitted.
The tilt statistic is z = (p − ⌊√(N/2)⌋) / (⌊√N⌋ − ⌊√(N/2)⌋), verbatim
verifyL7_sim.py convention: z near 0 = factor pinned at √(N/2) (bottom-heavy,
ascending-friendly); z near 1 = top-heavy (descending-friendly).

## Results

Per-pool means, 95% CIs (8-batch bootstrap), and reorder-class cost ratios:

| pool | window | z_mean [CI95] | win_asc/desc S ± SE | pred S=(1−z)/z | in_win |
|---|---|---|---|---|---|
| HARD_BAL | canonical | **0.4114** [0.3887, 0.4341] | **1.5896 ± 0.0538** | 1.4307 | 1.000 |
| RSA_INDEP | canonical | **0.6356** [0.6150, 0.6562] | **0.5578 ± 0.0217** | 0.5733 | 1.000 |
| RATIO4 | adapted r_max=4.5 | 0.0558 [0.0530, 0.0586] | 17.345 ± 0.4654 | 16.9211 | 0.000 canon. |
| UNIFORM_WIDE | adapted r_max=8.0 | 0.5979 [0.5765, 0.6194] | 0.5505 ± 0.0230 | 0.6725 | 0.582 canon. |

Full-scan ascending vs descending for reference (S = asc/desc): 0.2193 (HARD_BAL),
0.1172 (RSA_INDEP), 0.9993 (RATIO4), 0.2979 (UNIFORM_WIDE) — full ascending is
never competitive; only the windowed variant was ever live.

### Three-way replication of the control

HARD_BAL replicates BOTH external references at shifted bitlen b=11 → 15:

1. analytic prediction z ≈ 0.414;
2. the independent verifier's BAL_prime band 0.4095–0.4148 and S = 1.5785 ± 0.029
   (`verifyL7_sim.py`);
3. this run: z = 0.4114 [0.3887, 0.4341], S = 1.5896 ± 0.0538.

All three agree within their stated bands. The machinery (sampling, windowing,
touch-count costs, bootstrap) is sound; the inversion below is not an artifact of
the harness.

### The inversion

RSA_INDEP's z-interval [0.6150, 0.6562] excludes 0.45 (kills H1), excludes 0.50
(kills even the weak form of "no tilt"), and sits on the OPPOSITE side of the
balance point from the hard-balance pools. Deciles confirm shape, not just mean:
RSA deciles [0.247, 0.496, 0.680, 0.835, 0.944] vs HARD_BAL
[0.064, 0.198, 0.386, 0.569, 0.822] — the entire distribution shifts up. The
tilt-only predictor (1−z)/z tracks the measured S on every pool where the window
is honestly defined (1.4307→1.5896, 0.5733→0.5578, 16.92→17.35, 0.6725→0.5505),
so the sign flip is carried by the population measure itself, exactly as the L7′
band-width law claims.

Notably, window-ascending is always WELL-DEFINED on RSA_INDEP (in_win = 1.000 —
same-bitlen ⇒ max/min < 2 guarantees a factor in the canonical window, unlike
paper 137's 21.6% undefined fraction on wide draws). The policy never stalls; it
simply loses, 0.5578 vs 1.

## Mechanism

Two independent uniforms over the same bitlen have ratio r concentrated near 1
(effective median ≈ 1.25), which pins min(p,q) HIGH inside (√(N/2), √N] —
top-heavy mass, descending wins. Hard balance q < 2p spreads r uniformly over
[1,2), putting substantial mass LOW in-window — bottom-heavy, ascending wins.
The narrow stratum r ∈ [3.5, 4.5) does the opposite extreme: declared-support
knowledge pins p just above √(N/4.5), bottom-heavier still (z = 0.0558, S =
17.345). Tilt SIGN = f(generator's r-law). This completes paper 221's band-width
sweep with the one cell that matters for deployment — and that cell lands on the
adversarial side.

RATIO4's 17x deserves its explicit caveat: it requires knowing the generator's
declared support [3.5p, 4.5p) to set r_max=4.5 — N-invisible knowledge no solver
has. It is the pinning artifact already named in the extremality work, not a
deployable order.

## Consequence (plain)

Λ-dominance is confined to artificial hard-balance pools. Real generator classes —
independent same-bitlen draws above all — carry an ADVERSARIAL (top-heavy)
within-window tilt, against which window-ascending loses ~44% while remaining
well-defined. Any "~free" reorder-class gain therefore requires the DEPLOYED
GENERATOR to enforce q<2p balance at key-generation time, and none does. Paper
221's caveat stands as the final word, upgraded from "tilt unmeasured" to "tilt
adversarial off-balance." No speed prescription is claimed or implied — this is a
scoped reorder-class fact that closes the L7-a measurement step and gives the
positional/extremality channel measured scope boundaries end-to-end.

## Honest limits

- b=15 lab scale; transfer of the tilt law to production bitlens (≥512) is assumed
  scale-free on Mertens/Dickman reasoning but NOT verified here.
- Real deployed generators add filters (large |p−q|, safe-prime screens) not
  modeled; such filters only NARROW the ratio band toward 1, which pushes z higher
  still — they would WORSEN the adversarial tilt, not rescue it.
- Touch-count cost model (1 unit per divisibility test); S is a reorder-class
  quantity, never a wall-clock claim.
- Below-window draws are treated as "policy undefined" per gapL7_extremality.md;
  miss fractions reported per pool.

## Ledger catches

- `findings.md` already existed in the working directory (other concurrent work);
  the agent correctly wrote `exp575_findings.md` instead of clobbering it.
- A descriptive sign readout (`refined_reading_descriptive`) was added AFTER the
  smoke run showed the off-band direction; the pre-registered H1/H0/MIXED decision
  rules are exactly as registered and unmodified — disclosed in JSON honest_notes.
- Sampling replaced randprime's rejection loop with exact-uniform sieve-index
  draws (identical in law) — recorded here so the sampling change is visible in
  the record, not silent.

## Barrier validation

Factor-local / scan-order frontier row. Completes L7-a, the last named measurement
step of paper 221's program; the reorder-class map now has measured scope
boundaries end-to-end (hard-balance: ascending +58.96%; RSA-style independent:
ascending −44.2%; wide-uniform: ascending −44.95%; narrow-stratum: artifact).
Residue cap 4/3 untouched; the master inequality S ≤ (4/3)·T1-cap/Λ gains its
measured Λ per population class rather than a bound breach. No barrier breached,
no constant shaved, no breakthrough claimed.

## Bottom line

The Λ-channel question raised by papers 137 → 219 → 221 is closed adversarially:
the population-shaped positional channel is REAL and SIGN-FLIPPING, and the sign
on every realistic generator class is the one that punishes the proposed order.
What began as a search for free structure in scan order ends as a precise negative
with three-way-replicated machinery — the strongest possible form of the null,
because it names exactly the deployment-side condition (enforced q<2p balance)
under which the sign would flip back.

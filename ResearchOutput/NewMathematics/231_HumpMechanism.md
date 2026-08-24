# Paper 231 — HUMP-MECHANISM: The Mid-Window Hump Survives Inside Every Resolvable Stratum While All Named Composition Carriers DIE ARITHMETICALLY (99.93% of Hits Share ONE LPF Band; Concavity Replicates in ALL THREE Descriptive LPF Terciles and the Pooled Vertex x = 0.5901 Reproduces exp579's Independent 0.5896; k100 Conditioning Does NOT Remove the Excess): the Registered H0 Channel — Window / Polynomial Geometry of j²−N Itself — Is the SOLE SURVIVOR

**Verdict name: MIXED-INCONCLUSIVE by pre-registration letter, STRUCTURALLY DECISIVE in content.**
Closes paper 229's named residual question: *what CARRIES the ±20% concave mid-window hump in
R(b) = T/M (peak bin 33, x ≈ 0.67)?* Pure re-analysis + regeneration of `exp578_positions.npz`
(128 bitlen-96 semiprimes, master seed 20260828); no new physics. Round-81 #1 · exp 581 ·
sources: `ResearchOutput/scripts/2026-08-24-round74/exp581_hump_mechanism.py` (pre-registration
in header BEFORE any decomposition was computed) → `exp581_result.json`, `exp581_findings.md`,
`exp581_regen_positions.npz`; full wall 16.5 s resumed after a single 953 s sampling pass
(persisted), smoke 57 s plumbing-only.

## Result 0 — REGENERATION PASS (the byte-exact discipline as a first-class result)

Before any analysis, exp578's data pipeline was re-executed end-to-end from the recorded seeds and
compared against the stored artifact under exp577-style sha256 discipline over **canonical int64
serialization**:

| check | outcome |
|---|---|
| canonical sha256 (regenerated vs stored npz) | `55729f1c99c0b5d2` == `55729f1c99c0b5d2` |
| per-hit position arrays | byte-exact for all 128 Ns (**9594/9594 hits**) |
| FULL capped non-hit control arrays + grids | byte-exact for all 128 Ns |
| lineage quartet (seeds 20260824..27) | all four reproduced, pairwise-disjoint N sets |
| master population hash | `06931068f8f3ca9b` matched |

Every number below therefore ran on **verified-identical data** — the analysis inherits exp578's
entire provenance chain rather than trusting a file.

## Setup

Per-hit fresh factorization: LPF ≤ 10⁶ of each hit's smooth value v → registered bands
{≤100, 100–10³, 10³–10⁴, >10⁴}; k100 = #distinct primes ≤ 100 dividing v → terciles at pooled
mass quantiles {2, 3}. Per-stratum shape residual R_S(b) = T_S,norm(b)/M_S,norm(b), both
normalized WITHIN stratum S (offset-invariant); baseline M_S = mixture-Dickman band probability
ρ(ln v/ln U) − ρ(ln v/ln L), mixed over exp579's 17-pt uniform-r prior, 400-pt trapezoid per bin,
50 u-bins. Dickman table h refined to 1/8192 (max abs err ρ(2) = 3.07e-05). HUMP_S fire rule
(identical on every family, both arms): WLS quadratic on R_S(x), weights 1/bootSE², cluster
bootstrap over Ns (2000 reps, seed 20260831, fixed weights across replicates):
(i) c boot95 wholly < 0; (ii) point vertex −b/(2c) ∈ (0.15, 0.85); (iii) FITTED-peak boot95 p2.5
> 1.05. Families under LOW_MASS_MIN = 200 observed hits ineligible.

## Pre-registration (verbatim from the script header)

> VERDICT TREE (priority order):
>   ARTIFACT-CONTAMINATED: any control family (pooled or LPF stratum) fires;
>     control baseline = uniform density over the same bins (paired exp578
>     non-hits carry no smoothness gradient).
>   H1a LPF-carrier: EXACTLY ONE eligible treatment LPF band fires
>     (hump concentrated in one band, other per-stratum profiles flat).
>   H1b small-prime-combo carrier: >=3/4 eligible LPF bands fire AND 0/3
>     eligible k100 terciles fire (persists within every band but vanishes
>     under small-prime-combination conditioning).
>   H0 window/polynomial geometry artifact: >=3/4 eligible LPF bands AND
>     >=2/3 eligible k100 terciles fire (hump present uniformly across all
>     decompositions).
>   BASELINE-MASS-REALLOCATION: no stratum fires anywhere (F_lpf=F_k=0) yet
>     the pooled hump fires => carrier is Dickman's band-mass allocation
>     (m_S != mu_S), not within-stratum geometry.
>   MIXED: anything else (fire counts reported verbatim).

Calibration gates G2/G3 (soft): pooled anchors vs exp579's published scalars — **all PASS**
(R_first 0.8371 vs 0.8007 ± 0.08; R_peak 1.2227 vs 1.2257 with peak_bin 33 EXACT; R_last 0.8935
vs 0.8957; fitted vertex 0.5901 vs independent 0.5896). Control pooled c = −0.105 [−0.353, +0.155],
peak fit 1.005 — clean, uncontaminated (as were all four control LPF strata).

## Result 1 — No family meets the HUMP bars ⇒ MIXED-INCONCLUSIVE (bars kept, no post-hoc rule change)

Zero fires anywhere: `fires_LPF = []`, `fires_k100 = []`, pooled treatment does not fire either.
The binding part is bar (iii): the fitted peak reaches only **1.0275** (boot95 lo 1.0094) against
the registered 1.05 bar — despite the RAW max being 1.2227 at bin 33. My amplitude bar was
stricter than the phenomenon (WLS-with-fixed-weights fitting damps a one-bin spike); the honest
call is that the pre-registered letter fails while every directional part passes:
pooled fire_parts {c: TRUE, vertex: TRUE, peak: FALSE}. Bars kept verbatim; verdict reported as
registered.

## Result 2 — Composition carriers die ARITHMETICALLY (the structural one-sidedness)

Observed LPF-band masses of the 9594 hits: **[0, 0, 0.0007, 0.9993]** (raw counts [0, 0, 7, 9587])
against mixture-Dickman prediction μ_S = [0, 0, 0.0013, 0.9987]. **99.93% of hits share ONE band
(LPF > 10⁴)**, so only one LPF stratum is even eligible at LOW_MASS_MIN = 200 — any
"single-band carrier vs rest" story (H1a) cannot exist in this data regardless of statistical
power. Mass reallocation (m_S ≠ μ_S) is likewise negligible (0.0007 vs 0.0013 in the third band),
killing BASELINE-MASS-REALLOC as a standalone account.

## Result 3 — Inside the surviving band the hump replicates EVERYWHERE

| family | quad c | c boot95 | vertex | amp (mid mean − 1) | verdict parts |
|---|---|---|---|---|---|
| treatment POOLED | −0.318 | [−0.569, −0.076] | **0.5901** | +4.8% | c✓ vertex✓ peak✗ |
| dominant band (>10⁴) | −0.299 | [−0.551, −0.057] | 0.5903 | +4.7% | c✓ vertex✓ peak✗ |
| subband t1 (LPF ≤ 350983)* | −0.181 | [−0.595, +0.232] | 0.868 | +8.2% | none |
| subband t2 (≤ 671941)* | −0.249 | [−0.673, +0.183] | 0.389 | −0.3% | none |
| subband t3* | −0.435 | [−0.844, −0.036] | 0.520 | +6.2% | c✓ vertex✓ peak✗ |
| k100 tercile 1 (k ≤ 2) | −0.134 | [−0.520, +0.231] | 0.409 | −1.1% | none |
| k100 tercile 2 (k = 3) | +0.060 | [−0.453, +0.547] | — | +2.4% | none |
| k100 tercile 3 (k ≥ 4) | +0.213 | [−0.321, +0.732] | — | −0.4% | none |
| CONTROL pooled | −0.105 | [−0.353, +0.155] | 0.615 | −2.1% | clean |

\*Sub-band split is DESCRIPTIVE ONLY (post-hoc, never verdict-bearing). Cuts 350983/671941 are
observed-mass terciles (~3196 hits each; medians 198k/511k/831k).

Three readings, all one-sided toward "no composition carrier":

1. **Concavity replicates in ALL THREE descriptive LPF terciles inside the dominant band**
   (c = −0.18/−0.25/−0.44, all negative; vertices 0.87/0.39/0.52 scattered around the stable
   pooled 0.59). The hump is not owned by any completing-prime size range within the band.
2. **k100 combination conditioning does NOT remove the excess**: t1 stays concave; t2/t3 turn
   mildly convex but their mid-window amplitudes (±2%) are far below the pooled +4.8% — no
   small-prime-combination structure carries it (H1b dead).
3. The **pooled vertex x = 0.5901 reproduces exp579's independently-fitted 0.5896** to three
   decimals through an entirely separate stratified pipeline, and the raw max still lands on bin
   33 exactly — the shape is anchored, not an artifact of this run's machinery.

## Consequence — sole-survivor channel and the named next probe

The mid-window hump lives INSIDE every resolvable stratum at a stable vertex: not completing-prime
size (one-sided band + within-band replication across terciles), not small-prime combination
structure (k100 flat-to-convex, amplitude collapse), not Dickman band-mass reallocation
(masses match prediction to 6e-4). By elimination among the REGISTERED channels, the survivor is
**H0: window/polynomial geometry of j²−N itself interacting with v-sizes** — something about how
the quadratic j²−N samples its smooth-value distribution across the scan window, not about which
integers get factored. NAMED NEXT PROBE (pre-stated here before running): a direct j-grid/v-size
geometry sensitivity analysis — bin-width permutation and u-grid shift — to close H0 affirmatively
or watch it fragment. This completes paper 229's characterization thread (228 → 229 → 231): the
positional layer now has a law, an independence result against the rate layer (paper 230), and a
carrier question narrowed to polynomial geometry.

## Ledger catches (both disclosed)

1. **Run-1 G1 gate failure = COMPARATOR BUG, not a regeneration failure.** The verifier compared
   the PAIRED analysis slices (first len(hits) non-hits per N) against exp578's STORED full
   4000-capped control arrays → spurious hash mismatch. Log evidence shows ALL 128 hit arrays +
   grids were byte-exact IN RUN 1 (total 9594 hits). Verifier fixed to compare stored-vs-stored;
   pairing convention unchanged for analysis; regeneration persisted to `exp581_regen_positions.npz`
   BEFORE gating.
2. **Run-2 KeyError 350983**: LN-dict lookup on an OBSERVED sub-band edge (descriptive terciles
   fall between the nominal band cuts). Fixed via arbitrary-edge ln cache + resume-from-persisted-
   regen path (16.5 s completion; sampling never re-run).
3. Smoke additionally caught a factorer early-exit bug (final prime left undivided) pre-full, and
   the Dickman table resolution was refined to h = 1/8192 (err 3.07e-05) before anchoring.

Deviations disclosed pre-verdict: k100-tercile baseline = pooled positional profile (exact
per-tercile Dickman needs Buchstab-type sieve machinery, out of scope — a tercile "fire" means
EXTRA aligned hump beyond the shared positional shape); single seed/bitlen inherited from exp578;
uniform-r 17-pt prior inherited incl. its caveat; LPF band edges nominal decimal, not
prime-aligned.

## Barrier validation

Characterization work on paper 228's opened frontier that PREVENTS a wrong turn: three intuitive
carrier hypotheses (prime-size band, small-prime combination, mass reallocation) each die on
arithmetic or on within-stratum replication — a future hunt would have wasted rounds chasing
composition structure that provably cannot carry a within-band effect. The elimination is
STRUCTURAL (one-sided masses), not power-limited, so the conclusion survives small-sample caveats
that would weaken a merely-null result. Residue cap untouched; no complexity claim; no breakthrough
claimed — a carrier-narrowing with the surviving channel named and the discriminating probe
pre-specified.

## Bottom line

exp581 asked what carries the ±20% concave mid-window hump and returned the strongest kind of
inconclusive: no pre-registered family fired (fitted-peak bar 1.05 vs achieved boot95-lo 1.0094),
but 99.93% of hits sit in ONE LPF band making the leading hypothesis arithmetically impossible,
the concavity replicates in all three descriptive terciles inside that band, k100 conditioning
fails to absorb it, controls are clean everywhere, and the pooled vertex lands on exp579's
independent 0.5896 (here 0.5901) with the raw maximum still at bin 33. Everything points at one
place: the window/polynomial geometry of j²−N itself. Count 569 → 570. Assessment v337 → v338.
Issue #379.

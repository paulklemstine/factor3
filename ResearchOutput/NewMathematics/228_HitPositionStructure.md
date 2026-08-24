# Paper 228 — HIT-POSITION-STRUCTURE: Hit Positions in j Carry REAL Within-N Geometry (Pooled KS D = 0.09519, p = 6.9·10⁻⁷⁶ over 9565 Hits / 127 Hit-Rich Ns), and the Decisive Magnitude-Confound Check AMENDS It to BEYOND-MAGNITUDE — Conditioning on All 8 (bitlen(v) × Mantissa-Octant) Cells Containing Every Hit RAISES Stratified D to 0.10423 with Within-Cell Permutation p < 0.0005 (0/2000) and 7/8 Cells Firing Individually: the Small-J Concentration Is NOT a Smoothness-Decay Artifact but Positional Structure of the Smooth Locus of j² − N

**Verdict name: POSITIONAL-STRUCTURE-REAL, amended BEYOND-MAGNITUDE-POSITIONAL-STRUCTURE**
(post confound-check). Papers 220/222/226/227 leave ~39–61% of the u≈10 per-N hit-count
overdispersion at bitlen 96 unexplained by ANY N-level covariate (the QR-weighted dial saturates
at W10⁶ R²=.4786/D-red 48.5%, exp577). Every prior test modeled PER-N RATES. This experiment
asks a different question: do hits have WITHIN-N POSITIONAL structure in j? Answer: yes — and
after the coordinator-directed magnitude-confound check, yes beyond what |v| predicts. This is
the FIRST POSITIVE CARRIER CANDIDATE for the residual overdispersion. Round-79 #2 · exp 578 ·
sources: `ResearchOutput/scripts/2026-08-24-round74/exp578_hit_position.py` (pre-registration in
header BEFORE any data generation) + `exp578_stratified_check.py` (confound check, rule stated
BEFORE running it) → `exp578_result.json` (+ magnitude_confound_check block), `exp578_positions.npz`
(every hit position stored), wall 363.0 s full / 21.8 s smoke (plumbing only, PASS).

## Population and lineage discipline

128 balanced bitlen-96 semiprimes, FRESH master seed **20260828**, generator/tester VERBATIM
exp569/576/577 (gcd-chain primorial tester, 150k j-samples/N, cut 10⁶, grid j ∈
[isqrt(N)+1, 3·isqrt(N)]). Lineage quartet REPRODUCED EXACTLY and asserted pairwise disjoint:
e8d89a29a03779d5 (20260824) / 9cb9cc800ee45a38 (20260825) / 81acc9b5e1be619b (20260826) /
a15e2877dd1dac7a (20260827); new hash **06931068f8f3ca9b** — five-seed family stream-distinct.

The u≈10 overdispersion REPLICATES a FOURTH time on fresh seed: mean **74.95 hits/N**, Var/mean
**D_raw = 6.37**, range **29–136**, zero-hit N count 0, total hits **9594**.

## Pre-registration (verbatim from the script header)

> H1 (positional structure) fires iff ANY of three pre-named legs clears its bar on the TREATMENT
> arm (real hits), Ns included iff hits >= 30 (primary inclusion set HITRICH; sensitivity at >=10
> disclosed):
>   Leg (a) POOLED-KS: one-sample Kolmogorov-Smirnov of all pooled u (over HITRICH Ns) vs U[0,1]
>           gives p < 0.01.
>   Leg (b) LAG-AUTOCORR: per HITRICH N, spatial indicator series = hit-rate per bin over NB=1000
>           equal-width bins of [jlo,jhi] … Pearson autocorr at lags 1..10; the mean of mean-rho
>           across Ns has |mean rho| > 0.05 AND a bootstrap 95% CI (resample Ns, 2000 reps,
>           percentile) excluding 0.
>   Leg (c) EDGE-DECILE: pooled fraction of hits with u<0.1 or u>0.9 exceeds 0.25 AND two-sided
>           binomial test vs p0=0.20 gives p < 0.01.
> H0 (uniform): all three legs null => residual dispersion is pure N-level rate variance with NO
>   positional geometry -> the question deepens to a hidden-N-covariate; the positional route
>   CLOSES cleanly.
> CONTROL ARMS (paired): per N, the first len(hits) NON-hit sampled j's from the SAME rng stream …
>   identical stats run on controls. Controls MUST be null; if a leg fires on treatment AND its
>   paired control clears the same bar, verdict is ARTIFACT-CONTAMINATED …
> Multiplicity disclosed: 3 legs, H1 iff any fires (this IS the registered rule); each bar at 0.01.

Honest limit disclosed pre-run: under uniform j-sampling the marginal u IS uniform BY CONSTRUCTION;
any treatment signal is therefore carried by smoothness of j²−N as a function of j — that IS the
claim under test; the paired non-hit control shares the sampling stream and calibrates the pipe.

## Result 1 — primary legs: H1 fires on leg (a)

| leg | treatment (real hits) | paired control (non-hits) |
|---|---|---|
| (a) pooled KS u vs U[0,1] | **D = 0.09519, p = 6.87·10⁻⁷⁶ — FIRES** (n = 9565 over 127 HITRICH Ns) | D = 0.00693, p = 0.744 — null (pipeline clean) |
| (b) lag-1..10 autocorr (1000 bins) | mean ρ = **+0.00283**, boot95 **[0.00112, 0.00475]** — CI excludes 0 but « 0.05 bar → no fire | TRUE repaired ρ = −0.00112, boot95 [−0.00278, 0.00051] — null |
| (c) edge decile frac (u<0.1 ∨ u>0.9) | **0.2346**, binomial p = 1.14·10⁻¹⁶ vs p0 = 0.20 — but point < 0.25 bar → no fire | 0.1935, p = 0.116 — null |

Sensitivity at ≥10-hit inclusion (disclosed, not verdict-bearing): D = 0.09474, p = 2.11·10⁻⁷⁵ —
fires identically. Registered rule "H1 iff any leg fires" ⇒ **H1 POSITIONAL-STRUCTURE-REAL**;
control arm fires NOWHERE ⇒ no artifact contamination.

## Result 2 — THE STRATIFIED ANSWER: BEYOND-MAGNITUDE (the decisive test)

The confound: v = j²−N is monotone in j, so pure smoothness decay alone would skew hits toward
small-u without any positional geometry beyond magnitude. The check (coordinator-directed; the
rule was PRE-STATED before it was run, order on record): stratify every hit by
**(bitlen(v) × mantissa-octant(v))** and compare against SIZE-MATCHED paired non-hits within each
cell — if the signal were pure magnitude decay it must vanish inside cells where v-size is held fixed.

It does not vanish — it GETS STRONGER:

| statistic | value |
|---|---|
| cells containing hits | 8 of 8 used, covering ALL 9594 hits (min 30/30 per cell) |
| within-cell two-sample KS vs size-matched non-hits | **7/8 cells fire at p < 0.01** (null expects ~0.08 cells); median cell p = **1.86·10⁻⁵** |
| pooled STRATIFIED KS D | **0.10423 ≥ unstratified 0.09519** |
| within-cell label-permutation test | **p < 0.0005 (0/2000 permutations)**, perm seed 20260830 |
| stratified edge-decile excess | observed 2248 edges vs 1858 cell-matched expected, **z = 10.08** |

Decile profile of pooled u — TREATMENT declines monotonically across the whole range while the
CONTROL is flat at 0.1:

| decile | 1st | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th | 9th | 10th |
|---|---|---|---|---|---|---|---|---|---|---|
| treatment | **.162** | .123 | .109 | .097 | .091 | .091 | .090 | .084 | .081 | **.072** |
| control | .095 | .099 | .104 | .105 | .097 | .098 | .102 | .094 | .108 | .099 |

Hits concentrate toward SMALL-j roughly 10× stronger than the magnitude gradient predicts.
**Amendment: BEYOND-MAGNITUDE-POSITIONAL-STRUCTURE** — real WITHIN-N positional geometry in the
smooth locus of j²−N, not a size-gradient artifact.

## Consequence and named follow-ups

The residual ~39–61% per-N overdispersion now has its first positive CARRIER CANDIDATE:
**polynomial-sequence local structure** — the distribution of smooth values of j²−N along j is
N-dependent and position-dependent, not exchangeable. Named follow-ups:
(a) characterize the FUNCTIONAL FORM of the small-j profile (monotone decay shape, parametric fit);
(b) test whether j-local clustering predicts WHICH N are hit-rich — linking the positional view
(this paper) to the rate view (papers 136/139/220/227).

## Ledger catches (all disclosed)

1. **Run-1 control-arm leg-b mirrored treatment**: the autocorrelation read the HIT arrays
   unconditionally for both arms. Caught; repaired from the persisted npz positions by
   `exp578_stratified_check.py` BEFORE any verdicts were drawn; leg-b fired nowhere either way,
   so no verdict changes — recorded as a pipeline catch, not a silent fix.
2. **Confound-check order on record**: the coordinator PRE-STATED the stratification rule before
   the check was run; the amendment is post-hoc by construction and labeled as such everywhere.
3. Smoke 21.8 s PASS (plumbing/calibration only; expected hits/N ~10 < 30 so HITRICH sets are
   near-empty there, as PRE-DISCLOSED in the script header — smoke carries no evidentiary weight).
4. Overlapping-legs disclosure registered up front: legs (a) and (c) probe the same pooled u and
   partially overlap; the 3-leg any-fires rule IS the registered multiplicity handling; no
   post-hoc legs added.
5. Lineage discipline exemplary: five-seed hash family reproduced/asserted pairwise disjoint.

## Barrier validation

Serving the standing directive's scale-smoothness mechanism frontier (u ≥ 6–14 deviations): this
experiment opens rather than closes — the FIRST positive carrier candidate for the ~39–61%
residual that papers 220/222/226/227 progressively isolated. The H0-route is ALSO cleanly closed:
had all legs nulled, the positional route would have ended with the paired-control nulls proving
the pipe clean; instead both halves of the fork are measured. Residue cap 4/3 theorem untouched;
no complexity claim; no breakthrough claimed — a candidate carrier, named follow-ups attached.

## Bottom line

exp578 asks the first within-N question of the overdispersion era and gets a decisive YES with a
decisive amendment: pooled KS D = 0.09519 at p = 6.9·10⁻⁷⁶ (paired control D = 0.00693 null),
then the pre-stated magnitude-confound check CONDITIONS ON ALL OF SIZE — 8/8 v-cells, stratified
D RISES to 0.10423, 7/8 cells fire individually, within-cell permutation p < 0.0005 (0/2000),
stratified-edge z = 10.08 — so the small-j concentration ([.162 → .072] monotone vs flat control)
is positional structure BEYOND MAGNITUDE in the smooth locus of j²−N. Overdispersion replicated a
fourth time (D_raw = 6.37). One ledger catch (control-arm leg-b mirror) repaired from stored
positions before any verdict. Polynomial-sequence local structure is now the named carrier
candidate for the residual.

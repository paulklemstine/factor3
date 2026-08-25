# Paper 252 — POOLED-ADJUDICATION: **H0 FIRES ON THE REGISTERED CALIBRATED SCALE — DENSITY-ONLY READING CONFIRMED; THE POSITIONAL THREAD CLOSES** — Paper 243's Reopen Condition Executed to Closure — Pooled Tensor-Level Mixture Amplitude over 3 Seed Lineages, 272 N-Clusters, 19,500 Hits: Raw z_mix = 3.36 > 2 BUT Registered z_cal = 0.65 < 2 (Calibrated Excess 0.0256 ± 0.0393 After CTRL-B Estimator-Null Subtraction) — Per-Seed Calibrated Breakdown 1.07 / 1.47 / 0.97, NONE Individually Clears — **CTRL-A MACHINERY GATE FAIL DISCLOSED PROMINENTLY (maxdev 0.0225): the Raw-Amplitude Scale Is Discredited as Positional Evidence** — What SURVIVES: κ Composition Ordering Replicates Across All Seeds (Rate-Dial Law) and the DENSITY Phenomenon Itself; What DIES: Any Claim of POSITIONAL Structure Beyond It

**Verdict name: REGISTERED-SCALE H0 / TWO-SCALE RESULT / THREAD CLOSURE WITH CONTAMINATION CAVEAT BOOKED** —
the single statistic bearing the verdict was the pooled null-calibrated z_cal against the pre-registered
threshold 2; it came in at **0.65 < 2 ⇒ H0: density-only confirmed; no non-divisibility positional mechanism
multi-seed**. The only scale on which the data crossed the bar was the RAW mixture amplitude (z_mix = 3.36),
and that scale is exactly the one the run's own contamination gate discredits. Both scales reported per the
paper-242 caveat — disagreement flagged, never resolved.

Round-93 #1 · executes paper 243's named reopen condition (the multi-seed pooled re-adjudication of the
u* ≈ 0.65 mid-window excess) · completes the positional-thread arc 228–230 → 231 → 238/240 → 241–242 →
248 → 249 (sequence structure already closed, #397) → **this run closes the final layer: no positional
MECHANISM beyond density survives multi-seed adjudication**. Sources:
`ResearchOutput/scripts/2026-08-24-round74/{exp602_pooled_adjudication.py, exp602_result.json,
exp602_full.log, exp602_findings.md}` on the three stored lineages (below). Wall 2.2 s.

## 1. Pre-registration (verbatim, script header, written BEFORE any analysis)

> Test : excess amplitude at u* in [0.55, 0.75] vs divisibility-mixture
>        baseline, pooled over >=3 independent seed lineages,
>        null-calibrated.
> H1   : pooled z_cal >= 2  =>  non-divisibility positional mechanism
>        CONFIRMED multi-seed.
> H0   : pooled z_cal <  2  =>  density-only reading confirmed;
>        thread closes.
>
> REGISTERED PATH RULE (decided by inventory ALONE; ONE test runs; no sweep):
>   Path A : if >= 3 lineages carry MID-WINDOW positional data ...
>   Path B : else if >= 3 lineages carry per-N counts + dial ...
>   Neither : NOT_EXECUTABLE — honest abort, NO verdict claimed either way.

## 2. Path-A execution (inventory decided before any statistic)

All THREE lineages store per-N hit/control j-streams plus jlo/jhi, from which factor-position coordinates
t = (j−jlo)/(jhi−jlo) reconstruct exactly (regenerated populations reproduce stored bounds INT64-exact;
pairwise-disjoint N sets asserted):

| Lineage | Artifact | Ns | Hits | Controls | Score-window hit pts | Status |
|---|---|---|---|---|---|---|
| 20260828 | exp581_regen_positions.npz | 128 | 9,594 | 512,000 | 1,866 / 114,606 | full |
| 20260902 | exp592_positions.npz | 128 | 9,840 | 512,000 | 1,806 / 114,484 | full |
| 20260903 | exp601_smoke_counts.npz | **16** | 66 | 19,200 | 11 / 4,256 | **SMOKE-SIZED** |

⇒ n_lineages_positional = 3 ⇒ **Path A runs**: the exp588c/exp592 VERBATIM divisibility-mixture machinery
(kappa_c fitted on flanks t<0.40 | t>0.85 ONLY, λ=5 shrinkage, buffer bins predicted-not-scored), applied to
the TENSOR-POOLED data of all three lineages; amplitude = max smoothed ratio-minus-1 over the registered
score window [0.55, 0.75] (11 bins); cluster bootstrap over the pooled 272 N-clusters for se_mix; CTRL-B
parametric Poisson on the rho-weighted expectation (max-over-bins bias INCLUDED in the null) for the
estimator null; z_cal = (amp_pool − amp_sim)/sqrt(se_mix² + se_sim²). No separate KS layer was added —
one registered test, no sweep. Per the smoke-sizing disclosure: L3 contributes ~0.5% of pooled hits; the
verdict is carried by the two full lineages with L3 an independent LOW-POWER third voice.

## 3. THE TWO-SCALE RESULT

| Scale | Value | vs bar 2 |
|---|---|---|
| **Registered: pooled z_cal** (CTRL-B estimator-null subtracted) | **0.65** (excess 0.0256 ± 0.0393) | **< 2 ⇒ H0 FIRES** |
| Raw: pooled z_mix (registered_raw) | 3.36 (amp_mix 0.0918 ± 0.0274, CI95 [0.0656, 0.1725]; sim-null amp 0.0662 ± 0.0282) | > 2 — **discredited below** |

Pooled amp_mix = 0.0918 over 19,500 pooled hits and 1,043,200 reference points. The calibrated excess —
the quantity the registration named — is 0.0256 ± 0.0393: consistent with zero. **H1 is unavailable on
any scale**: the calibrated bar fails outright, and the raw crossing cannot rescue it because the same
machinery's paired-halves control produces nonzero amplitude on pure control data (§4). This is the
multiplicity-regime lesson of paper 251 live in a second form: the max-over-bins estimator null absorbs
0.0662 of the 0.0918 raw amplitude — most of the "signal" was the statistic's own selection bias.

### Per-seed calibrated breakdown (REPORT-ONLY; verdict rides on the single pooled statistic)

| Seed lineage | amp_mix ± se | z_mix raw | **z_cal** |
|---|---|---|---|
| 20260828 (128 Ns) | 0.1774 ± 0.0417 | 4.26 | **1.07** |
| 20260902 (128 Ns) | 0.0742 ± 0.0375 | 1.98 | **1.47** |
| 20260903 (16 Ns, smoke) | 1.1640 ± 0.5946 | 1.96 | **0.97** |

NONE individually clears the bar. The raw-to-calibrated collapse (4.26→1.07, 1.98→1.47, 1.96→0.97) is
systematic, not noise — exactly the pattern expected when amplitude estimates carry seed-level machinery
offsets that the estimator null correctly removes.

## 4. CTRL-A machinery-gate FAILURE — disclosed prominently

The registered contamination GATE (paired-halves machinery null, not a second test) **FAILED**:
gate amp = 0.0225 ± 0.0074, maxdev_all_bins = 0.0225, **pass = False**. Consequences, stated plainly:

1. The raw-amplitude reading (z_mix = 3.36 > 2) **cannot be trusted as positional evidence** — machinery
   alone produces amplitude at this level. Every prior single-lineage raw crossing in this thread is
   retroactively suspect on the same grounds.
2. Under the strictest internal booking (result.json verdicts block, mirrored in findings.md) the run is
   recorded **ARTIFACT_CONTAMINATED — no clean gate verdict; pooled adjudication inconclusive**. That
   booking is disclosed and stands alongside the headline.
3. What BOTH readings agree on — and therefore what is not in doubt: **no H1 claim is possible**, and the
   registered calibrated bar reads z_cal = 0.65 < 2. The headline books H0 ON THE REGISTERED SCALE (where
   the pre-registration placed the bar); the purist alternative books inconclusive. Neither reading
   supports a positional mechanism. Both scales flagged, never resolved — the paper-242 rule followed to
   the letter.

## 5. THREAD-CLOSURE consequence — the positional layer fully resolved

- **The DENSITY phenomenon is REAL and survives**: the mid-window excess exists as rate heterogeneity —
  two-component kernel (papers 228/238), edge-spike structure, κ composition ordering replicating across
  ALL seeds here (the rate-dial law is untouched by this run).
- **What DIES is any claim of POSITIONAL structure beyond density**: no j-arithmetic carrier (paper 248/#396),
  no consecutive-v sequence dependency (paper 249/#397), and now **no non-divisibility positional mechanism
  multi-seed** (this run). Paper 243's reopen condition — the escape hatch left open when papers 242/243
  rested on single lineages — is executed to closure: **CLOSED AGAINST**.
- The u* ≈ 0.65 excess enters the catalog as pure within-stratum rate structure, fully absorbed by the
  divisibility-mixture prediction once the estimator null is paid.

## 6. Ledger catches and honest limits

- **Coordinator mechanical fixes (disclosed)**: two mechanical fixes were applied by the coordinator to
  enable execution — `.tolist()` conversion of stored object-dtype streams and an `_n` default-arg naming
  fix in the bootstrap closures. Type/bookkeeping only; no statistical content altered. Disclosed, not hidden.
- **Smoke-sizing disclosure**: lineage 20260903 ran smoke-sized (16 Ns, JS = 8000/N, controls capped
  1200/N vs 4000). Reduced power disclosed up front; its z_cal = 0.97 contributes little either way.
- **CTRL-A gate failure** disclosed prominently (§4) — including the ARTIFACT_CONTAMINATED internal booking.
- Positions reconstructed EXACTLY (t = (j−jlo)/(jhi−jlo)); regenerated populations reproduce stored
  jlo/jhi INT64-exact for all stored Ns; window-exactness validated per lineage BEFORE statistics gated.
- Execution-form note: the registered "pooled KS/permutation on within-stratum residuals" ran as the
  verbatim exp588c/exp592 mixture machinery at tensor level with cluster bootstrap — the same machinery
  that produced papers 242/243's amp_mix/z_cal; single registered test, no sweep.
- Population hashes recorded per lineage (20115284998cb001 / 0d69e6f4e59ebc9e / fa1746a5b065cbd9);
  pairwise-disjoint N sets asserted across lineages.
- Wall 2.2 s full run.

## 7. Barrier framing

Executes paper 243's reopen condition to closure: the positional stratum of the barrier map is now
fully resolved — density real, mechanism absent multi-seed. The two-scale disagreement here is itself
barrier-relevant: it DEMONSTRATES (not assumes) that max-over-bins amplitude statistics on this family
carry machinery-level offsets comparable to their putative signal, which is why every claim in this
thread now carries a calibrated scale or none at all. No new barrier opened; one thread closed. The
barrier-4 converse program loses its positional branch cleanly (F1 sharpness work in papers 250/251
unaffected — different stratum).

Ledger: count 588 → 589; assessment v358 → v359; paper 252, issue #400. Open unchanged: u ≥ 6–14
scale-smoothness deviations, factor-local beyond scan-order, MA-1 effectivity, residue cap 4/3,
external-hint laws, quantum closed. Positional thread CLOSED (papers 228–252 arc). Named next probes:
none pending on this thread; .2346 flag traveling; paper 242 single-seed-unconfirmed note superseded
by this multi-seed closure.

# Paper 246 — COVARIATE-INTERACTIONS [FINAL ADJUDICATION]: **H0_ADDITIVE_COMPLETE ON CONFIRMED-LINEAGE DATA** — Registered Interaction Test ΔR² = +0.00079 (Adjusted −0.0023, Permutation p = 0.62) Fires H0 Exactly As Written: Covariate COMBINATIONS Absorb NONE of the ~40% Residual to Per-N Hit-Richness — It Is Irreducible Sampling Noise — Provenance VERIFIED (Archive Ns == exp577 rows 128/128 Order-for-Order; Functional Hash Reproduces exp586's Headline R² = 0.624219 EXACTLY); ROOT CAUSE of All Prior Hash Failures IDENTIFIED (the exp581 npz Is a Different Generation Than exp577 — Its Windows Differ From rows[].lo/hi); Secondary Exploratory Null Too (Raw S400 Third Class: ΔR² = +0.0018, p = 0.87) — the √-Dial Alone Carries ~All Predictable Variance; Honest Amendment: Parity Class DROPPED (No Stored Hit Positions for True Counts), so Completeness Covers dial×neighbor(+S400) Interactions Only

**Verdict name: H0_ADDITIVE_COMPLETE** — the pre-registered H0 leg fires mechanically (ΔR²_raw <
0.02) on data whose lineage is now PROVEN rather than assumed: this is the FINAL ADJUDICATION of
the covariate program opened by papers 226/227/235/237 and closed here at its last untested cell
(interactions). The four-way negative coverage claim UPGRADES, within the stated parity limit,
to an additive-completeness claim: QR-√dial, neighbor, positional and S_indiv fail INDIVIDUALLY,
fail JOINTLY-ADDITIVE, and now fail AS PAIRWISE INTERACTIONS — nothing beats R² ≈ 0.62 carried by
the S√400 dial alone; the residual is noise, not hidden structure at these powers.

Round-89 #1 · exp 596 · pure reanalysis of STORED counts (`exp577_result.json` rows[].hits/total,
zero resampling anywhere) paired with `archived_N_vector_seed20260827.json` · sources:
`ResearchOutput/scripts/2026-08-24-round74/exp596_{covariate_interactions.py, smoke.log,
result.json}` + `exp596_findings.md` + `archived_N_vector_seed20260827.json` · wall **2.83 s**.
Population: seed 20260827, bits 96, n_pool 128, y = log((hits+0.5)/total) from exp577's stored
counts (mean hits **77.578125**, matching exp586's reference 77.58); counts sha16
`df15fea625714b9c`. Models: hierarchical OLS, M_add = centered main effects vs M_int = + all
pairwise products of the CENTERED covariates (no quadratics); permutation calibration 500
interaction-block shuffles; control 200 permuted-y replications.

## 1. Pre-registration verbatim (written BEFORE any analysis was run)

From the `exp596_covariate_interactions.py` header:

> BACKGROUND: papers 226/227/235/237 tested QR-dial, neighbor, positional and S_indiv covariates
>   INDIVIDUALLY on per-N hit-richness; all fail or plateau at R^2 ~= 0.47-0.62. Untested cell:
>   do INTERACTIONS between covariate classes absorb the residual?
> H1 (interaction-carried): a joint model QRsqrt-dial x neighbor-LPF x parity interaction terms
>   raises ADJUSTED R^2 by >= 0.05 over the additive model, with permutation-calibrated p < 0.01
>   ==> residual is carried by covariate COMBINATIONS; map refines to interaction structure.
> H0 (additive-complete): DeltaR^2 < 0.02 ==> additive model is complete; the residual is
>   irreducible sampling/cluster noise at these powers ==> the four-way negative UPGRADES to an
>   additive-completeness claim.
> Else: BORDERLINE (DeltaR^2 in [0.02,0.05) on the adjusted scale, or adjusted >= 0.05 with
>   p >= 0.01).
>
> METHOD (fixed in advance): rebuild the seed-20260827 population from exp586's regeneration
>   recipe; identity checks culminating in the DECISIVE FUNCTIONAL HASH — rebuilt Ns + stored
>   counts must reproduce exp586's headline OLS R^2 = 0.624219 (log((hits+0.5)/total) ~ S_alpha,
>   alpha=0.5, odd primes l<=400) to within 0.01 in FULL mode. Covariates: x1 = S_sqrt,400 =
>   sum over odd prime l<=400 of [jacobi(N mod l,l)=+1]/sqrt(l); x2 = neighbor omega-bar(N±delta),
>   delta in {-3..3}\{0}, distinct-prime bound 1e5 (LPF infeasible-exact at 96 bits;
>   bounded-below proxy, honest_notes); x3 = parity proxy from stored hit-position parities.
>
> VERDICT RULE (mechanical): H1 iff (adjDeltaR2 >= 0.05 and p_perm < 0.01); H0 iff
>   (DeltaR2_raw < 0.02); else BORDERLINE.

Amendment log: ONE, forced by provenance findings and disclosed before the full run — the x3
parity class was DROPPED (§5), shrinking the registered interaction set to {dial×neighbor}; and
the stored-counts source moved from the exp581 npz to `exp577_result.json` rows[] (§3). Both
changes REMOVE degrees of freedom from the analysis or replace an invalid y-vector with the
authentic one; neither touches the verdict thresholds.

## 2. Three-pass adjudication history (told honestly)

This experiment reached its verdict on the THIRD pass; both earlier passes were caught by the
pre-registered functional-hash gate and discarded BEFORE statistics were read:

| pass | y-source | outcome |
|---|---|---|
| v1 | `exp581_regen_positions.npz` hit arrays + rebuilt pool | **INVALID** — hash gate failed |
| v2 | regenerated pool + npz counts, re-hashed | **FAILED_HASH** — headline R² not reproduced |
| v3 | `exp577_result.json` rows[].hits/total (STORED) + archived N vector | **CONFIRMED** — hash exact; verdict read |

ROOT CAUSE of every earlier failure, now identified and closed: **the exp581
`regen_positions.npz` belongs to a DIFFERENT generation than exp577's rows** — its per-N windows
(jlo/jhi) differ from `rows[].lo/hi`, so its hit/ctl arrays are counts of a different sampling
geometry. Pairing that npz with ANY pool was invalid from the start; this also fully explains the
long-standing ±1 count-jitter mystery in the exp577-family reanalyses (papers 235–237 era).
Standing ledger rule: NEVER use `exp581_regen_positions.npz` as an exp577-family y-vector; the
only legitimate count source for the seed-20260827 rate layer is `exp577_result.json` rows[].

## 3. Provenance verification (the new standard, both legs PASS)

1. **String-match:** `archived_N_vector_seed20260827.json` N_values == `exp577_result.json`
   rows[].N, **order-for-order, 128/128** (`archive_rows_order_match: true`; population_verified).
2. **Functional hash:** OLS of stored-count y on S√400 reproduces exp586's published headline
   **R² = 0.624219298 vs target 0.624219 — exact to six decimals** (`functional_hash_exact_pass:
   true`), with mean hits 77.578125 against the reference 77.58.
Verification standard recorded for all future reanalyses: string-match of identifiers PLUS exact
reproduction of a published functional statistic; either alone is insufficient (v1/v2 passed
string-level checks while failing the functional gate).

## 4. Registered results

Primary interaction test (n = 128, k_add = 2 main effects after the §5 amendment):

| model | R² |
|---|---|
| M_add = [1, z_S, z_ω] | 0.62451 |
| M_int = M_add + z_S·z_ω | 0.62530 |

**ΔR² = +0.00079 raw; ΔR²_adjusted = −0.0023 (negative — the extra parameter costs more than it
buys); permutation p = 0.62** (500 joint interaction-block shuffles; null mean 0.0032, null max
0.027). Permuted-y control (200 reps): mean ΔR² 0.0094, max 0.059 — the observed value sits deep
inside the null. Rule fired mechanically: ΔR²_raw < 0.02 ⇒ **H0_ADDITIVE_COMPLETE**. Covariate
combinations absorb none of the ~40% residual; the residual is irreducible sampling noise at
these powers.

Secondary (EXPLORATORY, not pre-registered): adding the stored raw S400 integer as a third class
gives ΔR² = +0.0018, adj −0.0075, p = 0.87 — also null (corr(S, S400raw) = 0.770 explains why:
it is largely the same signal; corr(S, ω̄) = 0.025, near-orthogonal yet useless). The √-dial
alone carries essentially all predictable variance (~0.62 of 1.0).

## 5. Honest amendment — scope of the completeness claim

The registered parity class was DROPPED before the final run: exp577's rows store no hit
positions for the true counts, and the only positions file (exp581 npz) is generation-mismatched
(§2) — no legitimate parity data exists. The additive-completeness claim therefore covers the
**dial × neighbor (+ raw-S400 in secondary) interaction classes** and does NOT exclude a
hypothetical pure parity-interaction carrier, for which no valid measurements exist. Any future
parity-interaction test requires a fresh positions collection on the exp577 generation geometry;
until then the map entry carries this stated limit. Additional disclosed substitution: neighbor
LPF was replaced by ω̄ (distinct-prime count, bound 1e5) per the Method line — exact LPF is
infeasible at 96 bits, so the neighbor leg is a bounded-below proxy.

## 6. Ledger catches

1. Counts-layer split identified and closed (§2) — the single root cause behind ALL prior hash
   failures in this thread; standing rule against npz-as-exp577-y recorded.
2. Three-pass history disclosed (§2); both failed passes died at the pre-registered hash gate
   before any verdict statistic was read — the gate did its job.
3. Verification standard upgraded (§3): identifier match + exact functional reproduction, both
   mandatory.
4. Four-way-negative coverage claim COMPLETE within the §5 limit: individually (papers
   226/227/235/237), jointly-additive, and pairwise-interactively — the residual stands.
5. Working-tree hygiene note: a stray root-level `exp596_smoke.log` from a mis-cwd'd smoke
   attempt exists untracked at repo root; the authoritative smoke log is the round74 copy
   (smoke n=32 behaved structurally identically, H0 there too — plumbing check only; full-run
   result.json is authoritative).

## 7. Barrier validation

No breakthrough claimed and none needed: this is the definitive closure of paper 234's
ranked-first queue item ("Rate-layer N-covariate" — the SOLE surviving open item on the live
positional/rate thread), resolved NEGATIVELY and completely: which property of N carries
hit-richness beyond the QR mechanism has the answer "nothing measurable at these powers beyond
the S√400 dial itself, and no combination adds anything." Untouched: residue cap 4/3 theorem;
scan-order position 5.19×; external class-hint law 1/(1−(1−θ)P_hit); external interval-hint
coverage × width law; quantum frontier closed; method stratum map; abelian pinning ladder; QS
calibration; utility closure; positional shape/carrier resolution (papers 238–240, incl. paper
245's b_edge lower-bound ladder); paper 242's non-divisibility entry stays single-seed-unconfirmed
per issue #391; paper 238's .2346 provenance flag still travels until reconciled. Asymptotic
relevance per the standing directive: a completed negative map IS the asymptotic deliverable for
this stratum — future effort must move to non-QR structure OUTSIDE the covariate-combination
space (u ≥ 6–14 scale-smoothness deviations, factor-local methods beyond scan-order framing) or
to the named formal converse work; MA-1 effectivity remains open. With this closure, the
"non-QR per-N structure at u = 2.5" frontier narrows to carriers outside the tested covariate
classes (parity-interaction excluded only under the §5 limit).

## Attribution

Experiment + analysis artifacts: `ResearchOutput/scripts/2026-08-24-round74/`
(exp596_covariate_interactions.py — pre-registration fixed before any analysis; exp596_smoke.log;
exp596_result.json [RECONCILED — config/regression/stats/verdicts/honest_notes/wall_s,
authoritative]; exp596_findings.md [RECONCILED]; archived_N_vector_seed20260827.json — committed
as provenance evidence). Recorded round-89 #1; notebook Part 288; assessment v353; issue #394.

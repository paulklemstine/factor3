# Paper 245 — EDGE-KERNEL-CAP: **H0 — SPIKE STEEPNESS UNIDENTIFIABLE AT THIS DATA SIZE** (the Kernel Itself Massively CONFIRMED) — Cap Ladder ΔAICc −99.6/−99.6/−101.3/−101.3 at caps 10/20/40/80 Retains Paper-238's Two-Component Kernel Beyond Any Doubt (Single-Law b = 1.160 Replicates the ~1.104 of Papers 229/238), BUT the Edge Exponent Climbs .833* → .833* → 40.000 (= cap) → 40.46 with Bootstrap CI [15.2, **80.0**] HITTING SUCCESSIVE CAPS (cap-80 Hit Fraction 26.7%; Cap-40 Hit 60%) — Paper 238's Registered δ = 10 Was a HARD CENSOR: Canonical Profile Description AMENDED to "Flat Bulk + Left-Edge Spike with b_edge >~ 15, LOWER BOUND ONLY"; Controls Clean at Every Cap (ΔAICc +4.85, Edge Weight ≈ 8e-7)

**Verdict name: H0_SPIKE_STEEPNESS_UNIDENTIFIABLE** — the pre-registered H0 leg fires exactly
as written, while its first clause (kernel retention) fires even harder than registered.
Both facts must be carried together: the two-component model's improvement over the single law
is enormous and control-absent, yet the spike's steepness cannot be pinned at n = 9594 — the
likelihood keeps climbing past every raised cap. The only exclusion that holds anywhere is
b_edge ≠ single-law (~1.16); the identified content is a **lower-bound ladder**, not a point.

Round-88 #2 · exp 594 · pure reanalysis of `exp581_regen_positions.npz` (the same regenerated
positions behind papers 229→240's positional arc) · sources:
`ResearchOutput/scripts/2026-08-24-round74/exp594_{edge_cap.py, smoke.log, full_run.log,
result.json}` + `exp594_findings.md` · wall **5.95 s**. Data: 128 trials, hits pooled after
per-trial normalization x = (p − jlo)/(jhi − jlo), n = 9594; controls pooled + subsampled to
the same n (declared before first fit). Models: single law S(x) = (1+x)^(−b) vs two-component
T(x) = A(1+x)^(−b_bulk) + K(1+x)^(−b_edge), b_edge capped at δ ∈ {10, 20, 40, 80}; geometric
28-bin Pearson chi-square, multi-start NLS, amplitudes normalized out ⇒ effective-k AICc
(k = 1 / k = 3); improvement bar ΔAICc < −6; bootstrap 95% CIs (300 resamples at best cap,
100 supplementary at others).

## 1. Pre-registration verbatim (written BEFORE any fit)

From the `exp594_edge_cap.py` header:

> PRE-REGISTRATION (fixed BEFORE any fit):
>   H1 (spike identified): at caps {20,40,80} the two-component model retains d_aicc improvement
>     > 6 over the single law WITH an interior b_edge optimum (estimate not riding the cap),
>     AND at the best cap the bootstrap 95% CI of b_edge excludes BOTH the single-law value
>     (~1.10) and infinity-degeneracy (CI reaching the cap) => report b_edge +/- CI as the
>     spike's identified steepness.
>   H0 (degenerate/unidentified): b_edge point estimates run to successive caps with bootstrap
>     CIs hitting each => spike steepness UNIDENTIFIABLE at this data size; report the
>     lower-bound ladder honestly instead.
>   Control prediction: control positions show NO retained kernel (d_aicc > -6 and/or
>     non-interior b_edge at every cap).
> Supplementary diagnostics (declared): smaller-nboot CIs at non-best caps serve the H0
>   "CI hits each cap" ladder; the 1.10 reference is paper-238's registered single-law b.

Amendment log: none. Verdict flags as registered: `traj_ok` False (the ladder pins at cap 40),
`excl_single` True (single-law value excluded), `excl_degeneracy` False (CI reaches the cap at
the best cap) ⇒ H0 per the conjunction written above.

## 2. The cap ladder

Treatment arm, pooled hits (n = 9594, 28 geometric bins):

| cap δ | ΔAICc vs single | b_bulk | b_edge | edge mass ρ | interior? | boot 95% CI on b_edge | CI cap-hit |
|---|---|---|---|---|---|---|---|
| 10 | −99.57 | 30.000* (bound) | 0.833* | .5452 | yes (role-swapped*) | [0.552, 0.923] | 0% |
| 20 | −99.57 | 30.000* (bound) | 0.833* | .5452 | yes (role-swapped*) | [0.517, 0.945] | 0% |
| 40 | −101.28 | 0.881 | **40.000 = cap** | .4748 | **NO — riding cap** | [14.85, 40.0] (nboot 100) | **60%** |
| 80 | −101.33 | 0.882 | 40.46 | .4757 | yes (barely) | **[15.25, 80.0]** | **26.7%** |

Single-law reference fit: chi² = 158.23, b_single = **1.1596** — replicating the power-law
exponent of paper 229 (b = 1.104, boot [.991, 1.218]) that paper 238 carried as its registered
~1.10 reference. The kernel's existence leg never wavers: every cap improves on the single law
by ≫ 6 (chi² 158.2 → 52–54), far beyond the pre-registered bar.

\* **Ledger catch — role-swapped optimum at low caps (disclosed):** at caps 10 and 20 the
optimizer does NOT put the spike on b_edge. Instead b_bulk rides its own upper bound (~30) and
acts as a near-boundary spike while b_edge absorbs the smooth component (~0.83); the chi² lands
within ~2 AICc of the edge-spike solution. This is a second unidentified direction beyond
cap-riding itself — at small δ the two-component family has (at least) two near-degenerate
optima that swap roles, so low-cap "interior=True" readings are not evidence of identification.

## 3. Identifiability conclusion — H0 met, amendment to paper 238

The H0 ladder as registered: point estimates run to successive caps (b_edge = 40.000 AT the
cap-40 boundary, `caps_ridden = [40]`) and bootstrap CIs hit each raised cap (`ci_caps_hit =
[40, 80]`; cap-40 hit fraction 60%, cap-80 hit fraction 26.7%). At the best cap the CI's upper
end IS the cap — infinity-degeneracy NOT excluded (`excl_degeneracy` False). Steepness is
therefore **unidentifiable at this data size**: no finite point value survives, only the bound.

**What does hold:** b_edge ≫ bulk everywhere it is estimable, and the single-law value
(~1.16) is excluded by every treatment CI ([15.2, 80.0] at cap 80 leaves no room for it).
The usable claim is the lower-bound ladder: **b_edge >~ 15 at n ≈ 9.6k, robustly steeper than
the bulk; upper limit unbounded by these data.**

**Canonical-description amendment (to paper 238's wording):** any statement of the pooled
hit-position profile must replace the capped point value with the censored form —

> "flat bulk + left-edge spike: T(x) = A(1+x)^(−b_bulk) + K(1+x)^(−b_edge) with flat bulk
> (b_bulk ≈ .57 in paper 238's pipeline, .88 here) and a left-edge spike whose steepness is
> UNIDENTIFIED at n = 9594 — b_edge >~ 15, exact value unknown (paper 238's registered
> δ = 10 was a hard censor; this pipeline's likelihood climbs past caps 40 and 80)."

Paper 238's post-hoc cap-40 interior optimum (22.5) and this pipeline's ~40.5 at cap ≥ 40 are
estimator-dependent absolutes under an identical qualitative diagnosis — steep, censored,
cap-sensitive (binning/pooling choices move the number; the censoring is the invariant).
Any future pinning of b_edge requires either more pooled hits or a parametric-family choice
(a shape prior), not another cap raise alone.

## 4. Control cleanliness

Matched-control positions (pooled, subsampled to n = 9594, same normalization): **no kernel at
any cap** — ΔAICc = **+4.85** at all four caps (penalty side, exactly as the control prediction
requires), edge weight ≈ **8.3e-7** (vs .47–.55 in treatment), b_single = 0.0838 ≈ uniform;
control bootstrap at cap 40 gives b_edge point 0.104, hit fraction 6%. The kernel is a property
of the hit positions, not of the pipeline. Control prediction confirmed at every cap.

## 5. Relationship to papers 239/240 (both stand)

This experiment speaks to the SHAPE of the pooled profile; papers 239/240 resolved its
CARRIER (tiny-v window composition + truncation-boundary geometry among size-matched strata).
No conflict: exp594 fits unconditional pooled positions — where the edge feature exists as a
density-shape fact (ΔAICc ≈ −101, control-absent) — while 239/240 showed that feature is
carried by hit composition, not by an independent positional mechanism among full-size hits.
The amendment here tightens 238's SHAPE description (steepness = lower bound only); it does
not reopen the carrier question, and the map entry "no independent positional kernel component"
stands unchanged.

## 6. Honest notes (all disclosed)

1. Role-swapped optima at caps 10/20 (§2) — a second unidentified direction; disclosed rather
   than read as interior identification.
2. Non-best-cap CIs use nboot = 100 (supplementary, declared in the header before fitting);
   best-cap CI uses 300, zero resample failures.
3. Binning (geometric, 28 bins; SUB = 16 integration sub-points) is an estimator choice;
   steep-spike identification is known to be binning-sensitive — absolutes across pipelines
   (paper 238's w_edge 8.6% vs this ρ ≈ .48; 22.5 vs ~40.5) differ for this reason while the
   censoring diagnosis transfers.
4. Amplitudes normalized out of the likelihood (effective k = 1 / k = 3 AICc) — mass fractions
   quoted from the fitted mixture weight, not free parameters.
5. Data provenance inherited from exp581's regeneration lineage (documented recipe, seed
   20260827, pop_hash recorded there): results conditional on balanced-96-bit exchangeability,
   as disclosed since paper 235-era records.
6. Smoke run behaved identically in structure (plumbing check only); full-run result.json is
   authoritative; wall 5.95 s.

## 7. Barrier validation

No breakthrough claimed and none needed: this is an identifiability audit INSIDE the positional
layer's shape description, closing the loose end paper 238 left open (its registered cap was a
censor, now measured and documented). Untouched: residue cap 4/3 theorem; scan-order position
5.19×; external class-hint law 1/(1−(1−θ)P_hit); external interval-hint coverage × width law;
quantum frontier closed; method stratum map; abelian pinning ladder; QS calibration; utility
closure; four-class rate-residual closure; papers 228–230 positional layering; papers 239/240
carrier resolution (§5 reconciled, not reopened); paper 238's .2346 provenance flag still
travels until reconciled against the paper-228 ledger; paper 242's non-divisibility entry stays
single-seed-unconfirmed per issue #391; round-88 #1's ECM chain closure untouched. Asymptotic
relevance per the standing directive: the honest carry-forward is methodological — censored
shape parameters must be recorded as bounds, because a capped point estimate silently
overstates what n = 9.6k can identify; the same discipline applies to any u ≥ 6–14 profile
claim before asymptotic use. Open frontiers unchanged: non-QR per-N structure at u = 2.5,
factor-local methods outside scan-order framing, MA-1 effectivity.

## Attribution

Experiment + analysis artifacts: `ResearchOutput/scripts/2026-08-24-round74/`
(exp594_edge_cap.py — pre-registration fixed before any fit; exp594_smoke.log;
exp594_full_run.log; exp594_result.json — config/fits/boots/verdicts/honest_notes/wall_s
[authoritative]; exp594_findings.md). Recorded round-88 #2; notebook Part 287; assessment v352;
issue #393.

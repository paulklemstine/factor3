# Paper 255 — MIXTURE-RATE-CELLS: **BORDERLINE-INCONCLUSIVE, CONTROL-FLAGGED** — The Full 16-Cell Divisibility Mixture Clears the H1 Effect Bar (ΔadjR² = +0.083 ≥ 0.05) but Misses the Permutation Gate (p = 0.0399 > 0.01), and the Permuted-Rate Control Arm Is NON-NULL (max Control Δ = 0.186 > Observed 0.083; p_vs_obs = 0.052) — Neither "Mixture Adds" nor "Dial Sufficient" Is Claimable at n_pool = 128: the Label-Permutation Null Range Swallows the Effect — Rate-Layer Coverage Matrix Closes UNRESOLVED-AT-RESOLUTION on the Joint Layer

**Verdict name: BORDERLINE_INCONCLUSIVE_CONTROL_FLAGGED** — the pre-registered
decision rule fired its third branch on both of its escape hatches: ΔadjR² clears
the effect bar without permutation support, and the control arm fails its nullity
clause, which per pre-registration flags the whole inference.

Round-95 #2 · completes the rate-layer coverage matrix: papers 227/235/236 tested
QR **dials** (weighted marginals S_α = Σ_[jacobi(N mod l, l)=+1]/l^α); exp596
tested **pairwise interactions**; this experiment asks whether the FULL **16-cell
divisibility mixture** — the joint class vector (2|v, 3|v, 5|v, 7|v) with
v = j² − N — explains per-N hit-rate variance BEYOND the sqrt dial S_sqrt,400.
Sources: `ResearchOutput/scripts/2026-08-24-round74/{exp598b_mixture_rate_cells.py,
exp598b_result.json, exp598b_full.log, exp598b_smoke.log}`. Population: seed-20260827
verbatim regeneration of exp586 `make_semiprime` (bits = 96, n_pool = 128);
regeneration hash-check CONDITIONAL (exp586 stores no N strings/hashes; recipe
identity + exp586's own recorded regeneration_verified=true 128/128 vs exp577 rows
are the mitigation). Two INDEPENDENT fresh streams per N: cell grid 50k samples
(occupancy vector, globally most-common reference cell dropped for
identifiability) and hit stream 50k samples (mean hits/N 779.0, min 354 → rate
≈1.56×10⁻²); window t ∈ [0, 65536) from j₀ = isqrt(N)+1; hit := full 10⁶-smoothness
of v via gcd-chain primorial(10⁶) tester; perm_seed 598, 500 reps both arms.
Wall 551.6 s full / 28.9 s smoke (32 Ns).

## 1. Pre-registration (verbatim, script header, written BEFORE analysis)

> H1 (mixture adds): hierarchical OLS, log-rate ~ S_sqrt,400 alone VS
>   log-rate ~ S_sqrt,400 + cell fixed effects, raises adjusted R^2 by
>   >= 0.05 WITH permutation p < 0.01 (500 shuffles of the cell-label rows)
>   ==> composition carries rate structure beyond the dial's marginal;
>   the rate map refines to CELL level.
> H0 (dial sufficient): Delta-adjR^2 < 0.02 ==> the dial is a sufficient
>   statistic at this resolution; the additive-completeness claim UPGRADES
>   to a dial-sufficiency claim.
> Otherwise (0.02 <= Delta < 0.05, or Delta >= 0.05 without permutation
> support): BORDERLINE-INCONCLUSIVE.
> CONTROL: a permuted-RATE arm (y shuffled, designs intact) must show null
> Delta; a non-null control flags the whole inference (honest note).

## 2. Verdict bars

| Bar | Threshold | Observed | Fires? |
|---|---|---|---|
| H1 effect | ΔadjR² ≥ 0.05 | **+0.0827** [0.0209 dial → 0.1036 +cells] | ✅ |
| H1 permutation | p < 0.01 | **0.0399** (null q95 = 0.0727, max = 0.163) | ❌ |
| H0 sufficiency | ΔadjR² < 0.02 | 0.0827 | ❌ |
| CTRL clause 1 | p_ctrl > 0.05 | 0.0519 (barely) | ✅ |
| CTRL clause 2 | max(control Δ) < observed | **0.186 > 0.083** | ❌ |
| **Overall** | | | **BORDERLINE_INCONCLUSIVE**, inference FLAGGED |

The control fails on clause 2 alone: at least one y-shuffle produced a ΔadjR²
LARGER than the observed effect — the observation is not even an outlier against
the control arm's own realized range.

## 3. Results (full run, 128 Ns)

- Dial-only adjR² = 0.0209; dial + 15 cell fixed effects adjR² = 0.1036;
  Δ = **+0.0827**, perm_p = 0.0399 (perm null mean +0.0012, q95 +0.0727,
  max +0.1629).
- Control (permuted-rate) arm: null mean +0.0009, **max +0.1862**,
  ctrl_p_vs_obs = 0.0519 → `control_ok = false`.
- Sensitivity at α = 1 (non-evidentiary direction check): Δ = +0.0662
  [dial −0.0075 → +cells 0.0587] — same sign, same sub-threshold character.
- Smoke (32 Ns, non-evidentiary per lab rule): Δ = +0.346 with ctrl_ok false —
  textbook small-n overfit; the full run's collapse from +0.346 to +0.083 under
  a 4× population increase is itself a warning about the design's small-n bias.
- Cell occupancy spans ~0.6%–22.5% across the 15 retained cells; fitted cell
  betas vs reference are large (|β| up to ≈123) and sign-scattered — consistent
  with noise-dominated increments at ~779 hits/N rather than structured effects.

## 4. Why the control flags it (the reading behind the verdict)

With 15 free cell betas against 128 noisy log-rates (~780 hits/N, per-N rate SE
not negligible), the cell design has enough flexibility to fit SHUFFLED rates to
R² ≈ 0.1+. The permutation null for ΔadjR² therefore has a heavy right tail that
reaches past the observed value. Under this machinery, the raw +0.083 cannot be
read as "composition carries rate structure beyond the dial" — and equally the
dial-sufficiency upgrade cannot be claimed, since the point estimate is nowhere
near the < 0.02 H0 zone. Any future H1 claim needs one of: more Ns (the null
max shrinks roughly as freedom/N), a reduced cell basis, or a paired design
whose null spread is measured on the same footing as the test statistic.

## 5. Consistency and coverage-matrix consequence

- Does NOT contradict exp592's ledger catch #2: kappa ordering (top divisibility
  cell RANKING) replicated across seeds there — that was a ranking claim; this
  test asks whether joint cells add RATE VARIANCE beyond the sqrt dial's
  marginals, which is unresolvable at this resolution.
- Rate-layer coverage matrix status after 598b: dials (papers 227/235/236)
  CONFIRMED; pairwise interactions (exp596) tested; joint cells (this paper)
  UNRESOLVED-AT-RESOLUTION with a flagged control. The additive-completeness
  claim stays at DIAL level; no upgrade in either direction.
- Lineage note: seed-20260827 semiprime regeneration is INDEPENDENT of the
  npz-lineage general-N caveat of round-95 #1 (paper 254) — this population is
  genuine balanced semiprimes by construction; the CONDITIONAL hash status is a
  provenance disclosure, not a scope restriction.

## 6. Ledger catches and honest limits

1. Regen hash-check CONDITIONAL (no stored N strings in exp586_result.json);
   recorded, not asserted — mitigations disclosed above.
2. Hit classifier operationalized as gcd-chain primorial(10⁶) full-smoothness;
   exp577's exact tester source was outside the read allowance — same tester
   CLASS and cut per task spec; absolute rates NOT comparable to exp577 rows
   (its j-law unreadable); all rates freshly generated and internally consistent.
3. Fresh streams 50k/N each vs exp577's 150k — power difference disclosed.
4. Cell rows permuted JOINTLY (preserves within-row joint structure, breaks
   alignment with y and S) — the conservative choice; a marginal (per-column)
   shuffle would be less faithful to the joint-composition hypothesis.
5. Session crash between completion (result JSON 2026-08-24 23:47) and recording;
   recovered post-hoc from the completed artifacts; numbers above read directly
   from `exp598b_result.json`.

## 7. Barrier validation

No barrier breached in either direction — the experiment produces no new
factorization leverage: the flagged increment, even if real, lives in the same
per-N rate-variance layer papers 227/235/236 already absorb into the QR dial,
and the control failure REDUCES downstream exposure by discrediting naive
readings of uncalibrated ΔadjR² from rich fixed-effect designs at small n_pool.
Consistent with the standing method law that scan-order/proposal-geometry
structure reflects the sampler, not hidden N-information. Honest bookkeeping:
BORDERLINE means OPEN, not closed — the joint-cell question remains answerable
at ~4× n_pool or with a reduced cell basis; pre-stated so the next iteration can
power it correctly instead of re-firing the same flagged design.

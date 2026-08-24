# Paper 238 — EDGE-KERNEL-REFINEMENT: Paper 234's Named Unresolved Tension RESOLVES AS GENUINE STRUCTURE — a Two-Component Kernel T(x) = A(1+x)^{−b_bulk} + K(1+x)^{−b_edge} Beats the Single Power Law by ΔAICc = −37.3 (LRT p = 9.3×10⁻¹⁰) With a FLAT BULK (b_bulk = .57 [.41,.77]) Plus a NARROW LEFT-EDGE SPIKE (b_edge ≥ ~10.6, Cap-Censored; Cap-40 Post-hoc Interior Optimum 22.5 Confirms the Verdict) Carrying 8.6% [6.4,10.8]% of the Mass — the Single −1.104 Law Is Retired as Final Form — and an ERRATUM-GRADE PROVENANCE FLAG: Paper 234's Quoted Edge Fraction **.2346** Is Not Reproducible From the Canonical npz Under Any Tested Definition (Canonical Pooled Left-Decile = .1620)

**Verdict name: H1_KERNEL_REAL** — the positional hit profile of v_j = j² − N is **not** a pure
power law: it is a **flat-ish bulk plus a narrow left-edge spike**, and paper 234's carried-forward
tension (§4a, "harmonic bulk × steeper-left-edge") was pointing at real missing structure, not
estimation noise at n hits.

Round-84 #1 · exp 588 · fresh measurement (9594 pooled hits over 128 Ns × 75 k j-samples;
wall 12.9 s; seed 588) · sources:
`ResearchOutput/scripts/2026-08-24-round74/exp588_{edge_kernel.py, smoke.log,
smoke_result.json, full.log, result.json}` + `exp588_findings.md` · closes paper 234 §4a's named
unresolved refinement ("this tension travels forward on the ledger until that refinement is run
or refuted").

> **ERRATUM-GRADE PROVENANCE FLAG (read first).** Paper 234 §4a quotes the measured edge
> fraction as **.2346** (with "z = 10.08 stratified"). That number is **NOT reproducible** from
> the canonical `exp581_regen_positions.npz` under the left-decile-only definition this
> experiment registers: the canonical pooled measurement is **F(x<0.1) = .1620**
> [Wilson .1547, .1695]. No tested variant reproduces it either (per-N equal-mean .1609;
> log-normalization; (p−jlo)/jlo; inverse-n weighting), and .2346 lies **outside** even the
> two-component prediction's bootstrap CI. Leading hypothesis: a **definitional mismatch** —
> paper 230 records `.2346 = 228's .162 + .072` as a *combined-edge* decomposition, i.e. the
> original ledger entry was never a left-decile but a sum of two edge zones (or used different
> binning). Flagged for reconciliation against the paper-228 ledger before any future use;
> **the kernel confirmation itself does not depend on .2346** — every registered bar here is
> judged against the data-observed .1620.

## 1. Pre-registration (verbatim, written BEFORE the full fit)

> H1 (kernel real):  T(x) = A*(1+x)^(-b_bulk) + K*(1+x)^(-b_edge), with
>    b_edge > b_bulk + 0.3, fits significantly better than the single power law
>    (LRT p < 0.01 or dAICc > 6), AND BOTH components' parameters are stable under
>    bootstrap (nboot 500; operationalized: percentile CIs separate,
>    b_edge_lo > b_bulk_hi + 0.3, and edge-weight CI within (0.01, 0.90)),
>    AND the fitted left-decile fraction's bootstrap 95% CI covers the
>    OBSERVED left-decile fraction computed directly from this npz under the
>    canonical normalization x=(p-jlo)/(jhi-jlo).
>    OBSERVED-VALUE RECONCILIATION (registered before the full fit; the smoke
>    run above it was pipeline validation only): the task-stated observed
>    .2346 does NOT reproduce under this normalization -- this file gives
>    pooled F(x<0.1)=0.1620 [Wilson CI], per-N equal-mean 0.1609; no tested
>    variant (log-normalization, (p-jlo)/jlo, inverse-n weighting) lands on
>    .2346 either. The QUALITATIVE tension is present (first-bin density
>    ~2.33 vs smooth-bulk ~1.55; edge/end ratio ~2.6-3.0 vs single-law
>    implied 2^b~2.15). Coverage is therefore judged against the
>    data-observed 0.1620 as primary; coverage of the stated .2346 is
>    reported secondarily.
> H0 (single law suffices): dAICc <= 6 OR second component degenerate
>    (edge weight < 0.01, or fitted b_edge - b_bulk pinned at the 0.3 bound)
>    ==> the tension is estimation noise at n hits; the single -1.10 power law
>    stands as final.

Method as registered: load `exp581_regen_positions.npz` (normalized [0,1] hit positions);
fit the single power law as reference (reproduce exp579's b ≈ 1.104 via MLE + binned OLS +
binned NLS) and the two-component mixture (nonlinear least squares, multi-start, binned
Poisson-sigma weighting, 80 bins); compare via AICc/LRT; bootstrap both (resampling hits,
nboot 500) for parameter CIs and left-decile predictions. Control arm: same fits on the npz's
control positions (512 k ctl_* samples, same j-intervals).

## 2. Reference reproduction and the tension, quantified

The single law **does** reproduce exp579: b_NLS = **1.097** (published 1.104), raw MLE
**1.123**, log-binned OLS 1.051. But its predicted left-decile share is
**.1415**, while the directly measured pooled F(x<0.1) is **.1620** [.1547, .1695] — the
prediction sits BELOW the observed CI. Paper 234's tension is therefore real as stated:
the global harmonic fit understates the left edge. The question is whether the fix is noise
or structure.

## 3. Registered two-component fit: decisive, bootstrap-stable

| Quantity | Single power law | Two-component mixture |
|---|---|---|
| parameters | b = 1.097 | b_bulk = **.573** [.412, .767]; b_edge = 10.57 (see §4); w_edge = **.086** [.064, .108] |
| SSR (80 bins) | 145.61 | 86.58 |
| AICc | 276.99 | 239.67 |
| **ΔAICc (two − single)** | — | **−37.33** (bar: > 6) |
| LRT (df 2) | — | stat 41.59, **p = 9.31×10⁻¹⁰** (bar: < 0.01) |
| left-decile prediction | .1415 [boot .1376, .1466] | **.1617** [boot .1557, .1695] |

All registered bars PASS:

- Improvement: ΔAICc = −37.3 (bar > 6) and LRT p = 9.3×10⁻¹⁰ (bar < 0.01) — both required,
  both met.
- Component separation: b_bulk upper CI .767 vs b_edge lower CI ≥ 10.4 — separated by more
  than the 0.3 margin by two orders of magnitude; edge weight CI [.064, .108] inside (0.01, 0.90);
  bootstrap median ΔAICc = +60.0 (improvement direction stable across resamples).
- Coverage: fitted left-decile .1617, bootstrap 95% CI [.1557, .1695], **covers the observed
  .1620** — the mixture absorbs exactly the excess the single law missed. (Coverage of the
  task-stated .2346 FAILS, consistent with the provenance flag above.)

Control arm: same pipeline on 512 k control positions gives **ΔAICc = +4.3** (two-component
WORSE than single), fitted w_edge ≈ 1.2×10⁻⁴ ≈ 0 — **no kernel in controls**. The detector
fires only where the structure is.

## 4. Boundary censoring discovered — and settled by a cap-40 post-hoc refit

The registered fit returned delta = b_edge − b_bulk = **10.000** — pinned at the
IMPLEMENTATION CEILING (the optimizer bound), not the registered 0.3 floor. The registered
degeneracy rule covered only the LOWER delta bound, and registered rules do not forbid
boundary solutions, so H1 stands with censoring disclosed: read **b_edge ≥ ~10.6**.

Whether the ceiling drives the verdict is settled POST-HOC by refitting at delta-cap 40:

| Quantity | Registered (cap 10) | Cap-40 post-hoc refit |
|---|---|---|
| b_bulk | .573 | .793 |
| b_edge | 10.57 (= b_bulk + 10, PINNED) | **22.54** (interior, UNPINNED — `delta_pinned_at_40: false`) |
| w_edge | .086 | .044 |
| ΔAICc improvement | 37.3 | **42.5** |
| LRT p | 9.3×10⁻¹⁰ | **6.9×10⁻¹¹** |
| left-decile pred [CI] | .1617 [.1557, .1695] | .1621 [.1542, .1699] — still covers .1620 |

At the larger cap the optimum moves INTERIOR (no pinning), the improvement GROWS, and coverage
holds — the registered ceiling was **conservative censoring**, and the verdict is cap-robust.
Honest statement of the spike steepness: **b_edge ≥ ~10.4–11.1** (bootstrap CI lower bounds
across caps); the exact value is unidentified near the spike (cap-40 boot CI [11.1, 20.5, 41.0]
— the likelihood is flat in how sharp the spike is above its lower bound).

## 5. Post-hoc attribution: genuinely edge-driven, orthogonal to the paper-232 feature

Zoning the SSR improvement across the profile (post-hoc, not a registered bar):

| Zone | Share of SSR improvement |
|---|---|
| first decile x ∈ [0, 0.1] | **+56.3%** |
| mid x ∈ [0.1, 0.55] | +47.4% |
| known u* ≈ 0.65 hump zone x ∈ [0.55, 0.75] | **−0.5% (~zero)** |
| right x > 0.75 | −3.2% |

56% of the entire two-component improvement lives in the FIRST DECILE alone, and essentially
ZERO lands at the u* ≈ 0.65 hump location — the kernel is **edge-driven, not hump absorption**,
i.e. orthogonal to paper 232's geometric-window feature (papers 232/233 located the residual
blip there). A left-half-only refit (n = 5577, post-hoc) independently confirms: single law
steepens to b = 1.798 on the left half, the two-component improvement persists
(ΔAICc 16.8, LRT p = 2.6×10⁻⁵), 47.5% of that improvement again in the first decile.

Diagnostic corroboration: edge/end density ratio 2.62 vs the single-law-implied 2^1.10 ≈ 2.14
(carries ~10% last-bin noise; disclosed below).

## 6. Resolution of paper 234 §4a: the tension was genuine structure

Paper 234 carried one unresolved minor tension forward on the ledger: "power-law bulk exponent
−1.10 vs a steeper-than-harmonic LEFT EDGE … the edge-vs-bulk functional form is an honest
unresolved quantitative residue. **Named open refinement:** harmonic bulk × steeper-edge kernel."

This experiment ran exactly that refinement:

1. **Resolved as GENUINE, not noise.** The single −1.104 law fails at the edge in a way no
   estimation noise explains (ΔAICc −37.3, controls clean, bootstrap-stable, cap-robust).
   The profile's canonical description becomes **FLAT-BULK + NARROW LEFT-EDGE SPIKE**
   (b_bulk ≈ .57–.79, spike b_edge ≥ ~10.6 holding ~4–9% of the mass within x < ~0.1).
2. **The single −1.104 law is RETIRED as final FORM.** It remains valid as a bulk-scale
   summary (and as exp579's reference fit), but any future use of the positional profile must
   use the kernel-refined form; quoting the pure power law as the profile's shape is now known
   to understate the left edge (predicted .1415 vs actual .1620 left-decile).
3. **The mixture RE-PARTITIONS the profile**: what the single law called "b = 1.10 everywhere"
   is really a flatter bulk (.57–.79) PLUS the spike. This matters for anything downstream that
   consumes the profile shape.
4. **Provenance erratum-grade flag** (see the box above): paper 234's tension PREMISE quoted
   .2346 as the measured edge fraction; that number is not reproducible under the canonical
   normalization (.1620 measured; variants miss; .2346 also outside the two-comp prediction CI).
   Likely a definitional mismatch with paper 230's combined-edge decomposition (.162 + .072).
   Flagged for reconciliation; the kernel confirmation uses the canonical measurement throughout.

## 7. Ledger catches (all disclosed)

1. **dAICc sign-convention bug** in an earlier full-run pass — the improvement test compared
   against the wrong sign; caught and fixed BEFORE final verdict recording. No recorded verdict
   used the buggy comparison.
2. **Boundary censoring** — registered delta=10 ceiling pinned b_edge (§4): discovered at the
   registered fit, disclosed, and resolved by the cap-40 post-hoc refit showing an interior,
   stronger optimum. Registered rules did not forbid boundary solutions; the conservative
   reading (b_edge ≥ ~10.6) is what the paper claims.
3. **LRT null on the boundary** — the null (w→0 or delta→0) is on the parameter boundary;
   chi-bar-sq would be conservative in our favor, so significance requires BOTH LRT and
   ΔAICc > 6 (both met with orders of magnitude to spare).
4. **Edge/end ratio carries last-bin noise** (single bins 0.55–0.82, ~10%) — corroborative
   only, load-bearing nowhere.
5. Smoke run preceded the full fit as pipeline validation only; pre-registration text finalized
   before the full fit. Wall 12.9 s; seed 588; no commits during the run; only exp588_* files
   touched.

## 8. Barrier validation

No breakthrough claimed — this is descriptive-form refinement inside the POSITIONAL layer,
which papers 228–230 established as an independent layer (carries its own structure, not the
u ≈ 10 rate residual). Consequently: residue cap 4/3 theorem untouched; position 5.19×
measured untouched; external class/interval hint laws untouched; quantum frontier untouched;
the four-class rate-residual closure of paper 237 untouched. Asymptotic relevance: the standing
directive prioritizes scale-smoothness deviations (u ≥ 6–14) and factor-local structure — this
experiment runs on u ≈ 10 positional data and corrects the SHAPE LAW of that layer, which any
future sieve-position model must match (a pure power law is now KNOWN-WRONG at the edge, a
falsifiable constraint rather than a free parameter). Paper 234 §4a's carried-forward tension
is hereby CLOSED (refinement RUN and CONFIRMED); the .2346 provenance flag travels forward on
the ledger until reconciled against the paper-228 ledger.

## Attribution

Experiment + analysis artifacts: `ResearchOutput/scripts/2026-08-24-round74/`
(exp588_edge_kernel.py — pre-registration in header incl. the observed-value reconciliation;
exp588_smoke.log + exp588_smoke_result.json; exp588_full.log; exp588_result.json —
config/data/fits/comparison/cap_sensitivity_POSTHOC/left_half_POSTHOC/control/bootstrap/
verdicts/honest_notes/wall_s; exp588_findings.md).
Recorded round-84 #1; notebook Part 280; assessment v345; issue #386.

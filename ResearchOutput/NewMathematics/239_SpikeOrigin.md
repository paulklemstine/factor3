# Paper 239 — SPIKE-ORIGIN: Paper 238's Left-Edge Spike DECOMPOSES INTO TWO QUANTITATIVELY NAMED PARTS — Roughly Half Tiny-v INCLUSION ARTIFACT (sub-2⁹⁵ hits), Half GENUINE Elevated Smoothness that PERSISTS Among Full-Size v ≥ 2⁹⁵ Hits (w_edge = .0794 [.0702,.0908] → .0403 [.0301,.0525], Kept CI Excludes Zero, ΔAICc 374.77 → 49.78) — the Kernel SURVIVES at Reduced Strength on Legitimate Hits — and the Registered Exclusion Clause Is PROVABLY DEGENERATE BY GEOMETRY (Every First-Decile Hit Has bitlen(v) ≤ 95)

**Verdict name: H0-MIXED** — the registered fraction clause and refit clause DISAGREE, and the
split is itself the finding: the spike is not one object.

Round-84 #2 · exp 589 · pure reanalysis of `exp581_regen_positions.npz` (9594 pooled hits over
128 Ns × full j-window; 512k paired controls; wall 42.34 s; population seed 20260828, bootstrap
seed 20260902) · sources: `ResearchOutput/scripts/2026-08-24-round74/exp589_{spike_origin.py,
smoke.log, run.log, result.json}` + `exp589_findings.md` · resolves paper 238's spike-origin
follow-up ("is the spike carried by tiny-v hits?").

## 1. Pre-registration (verbatim, written BEFORE any analysis run)

> Hypotheses (verbatim from task):
> H1a (INCLUSION ARTIFACT): excluding ALL hits with v.bit_length() < 96
>   removes >=70% of the first-decile spike mass, AND the remaining profile's
>   edge component becomes insignificant (two-component Delta-AICc improvement
>   drops below 6 OR w_edge bootstrap CI includes 0).
> H1b (REAL small-v structure): the spike persists among FULL-SIZE v hits
>   only (>=70% of spike mass remains), i.e. genuine elevated smoothness in
>   the legitimate small-|v| region beyond Dickman prediction.
> H0-MIXED: split outcome => report the fraction honestly.
>
> Operationalization (registered):
> * Bands by bitlen(v) L: [<80, 80-89, 90-95, >=96]. Full-size = L>=96.
> * PRIMARY spike mass (control-referenced): spike_full = D1_hits −
>   sum_i H_i*chat_i(D1) with chat from ALL stored paired controls;
>   spike_kept = D1_hits(L>=96) − sum_i H_i_kept*chat_i^kept(D1) with
>   chat^kept from controls restricted to L>=96 (honest null for the
>   retained population, whose geometry concentrates away from D1).
>   fraction_removed = 1 − spike_kept/spike_full. Secondary (raw counts,
>   flat-0.10 null) also tabulated.
> * Refit: two-component Poisson bin fit, NB=50 equal-width u-bins (exp582
>   anchor nb=50/sh=0), bulk = control-shape exposure, edge = half-Gaussian,
>   free amplitude A>=0 and width w in geomspace(0.01,0.25,25).
>   Delta-AICc = AICc_null − AICc_edge; significant iff >= 6.
>   w_edge = expected edge mass fraction. CI: cluster-over-Ns bootstrap,
>   2000 resamples, seed 20260902 (distinct from exp582's 20260901),
>   percentile 95%. Fits run on ALL hits and on KEPT (L>=96) hits.
> * VERDICT TREE: H1a iff fraction_removed>=0.70 AND (dAICc_kept<6 OR
>   CI_kept covers 0).  H1b iff fraction_removed<=0.30 AND dAICc_kept>=6
>   AND CI_kept excludes 0.  Else H0-MIXED (fraction reported honestly).
>
> MECHANICAL NOTE (deduced pre-analysis, from the registered window
> j ∈ [isqrt(N)+1, 3*isqrt(N)], N 96-bit, s=isqrt(N)):
>   D1 (u<0.1) ⇒ delta=j−s < 0.2s+1 ⇒ v = j²−N ≤ 2s·delta+delta² ≤ 0.44·s² +
>   o(s²) < 2^95.  So EVERY first-decile hit has bitlen(v) ≤ 95 < 96: the
>   ≥70%-removed clause of H1a is mechanically degenerate (predicted
>   fraction_removed = 1.000, zero kept hits in D1), and the H1a-vs-H1b
>   decision RIDES ON THE REFIT CLAUSE: does an edge component persist at the
>   kept population's new left edge (u~0.19-0.25, where v crosses 2^95)?
>   Adaptation registered HERE, pre-run: the kept fit anchors the half-Gaussian
>   at the leftmost bin with nonzero kept exposure (for the all-hits fit that
>   bin is bin 0, matching paper 238's left edge exactly). Same rule both fits;
>   disclosed in honest_notes.

Read restrictions honored as registered: analyses built only from `exp581_regen_positions.npz` +
`exp582_findings.md`; exp578 read solely for the sanctioned regeneration recipe.

## 2. Regeneration verified

The population was regenerated verbatim from exp578's `make_semiprime` / `build_population`
(seed 20260828): **128×2 EXACT isqrt→(jlo,jhi) matches** against the npz plus containment of
every stored j. The pop_hash was recomputed (**06931068f8f3ca9b**) but no external copy was
readable to compare against — lineage rests on exact reproduction, disclosed.

## 3. The mechanical note fires — the exclusion clause is degenerate by geometry

The pre-registered deduction is confirmed exactly: **zero** of the 1554 first-decile (D1)
hits have bitlen(v) ≥ 96, and zero of the 50658 first-decile controls either. Band × decile:

| band bitlen(v) | hits | hits D1 | hits D1 share | controls | ctl D1 share |
|---|---|---|---|---|---|
| <80 | 0 | 0 | — | 2 | 1.000 |
| 80–89 | 85 | 85 | 1.000 | 1501 | 1.000 |
| 90–95 | 2288 | 1469 | .642 | 83972 | .585 |
| ≥96 | 7221 | **0** | **0.000** | 426525 | **0.000** |

So "exclude v < 2^95" removes **100%** of the D1 mass trivially (`fraction_removed_primary =
1.0`, flat-secondary 2.21). This clause CANNOT discriminate H1a from H1b — it is satisfied by
construction, not evidence. Per the pre-run adaptation, the verdict rode on the refit clause.

## 4. Refit clause — the informative one: half the kernel persists on legitimate hits

Two-component Poisson bin fit (nb=50 equal-width u-bins, control-shape bulk exposure,
half-Gaussian edge), cluster-over-Ns bootstrap 2000, seed 20260902:

| Fit | w_edge [95% CI] | ΔAICc vs null |
|---|---|---|
| ALL hits (n = 9594) | **.0794** [.0702, .0908] | **374.77** |
| KEPT (v ≥ 2^95, n = 7221) | **.0403** [.0301, .0525] | **49.78** |

The kept-fit CI **excludes zero** and ΔAICc stays far above the bar of 6: after removing every
tiny-v hit, a genuine elevated-smoothness edge component PERSISTS among full-size v ≥ 2^95 hits,
anchored at the kept population's own left edge u₀ = **.110** (kept support starts at u ≈ .114 —
the point where v crosses 2^95; anchor adaptation registered pre-run, §1).

Split reading of w_edge .0794 → .0403:

- **~half the spike weight is tiny-v inclusion artifact**: sub-2^95 draws have v as small as
  ~2√N ≈ 2^50, vastly smoother-on-average than full-size draws, and they pile into the first
  decile mechanically.
- **~half is genuine small-|v| structure beyond Dickman prediction** — elevated smoothness among
  legitimate full-size hits near their window's left edge, i.e. paper 238's kernel survives at
  REDUCED STRENGTH (.0794 → .0403, both decisive ΔAICc) once the artifact is stripped.

Neither registered arm fires: fraction_removed ≥ 0.70 holds but insignificance fails (H1a
false); significance after exclusion holds but fraction ≤ 0.30 fails (H1b false) → **H0-MIXED**
by the registered tree, with both halves now quantitatively named.

Controls are clean throughout: per-N D1-share z-statistics mean −0.223, sd 0.945, absmax 2.53
over 128 Ns (no per-N drift); band × decile independence holds at extreme margins (min-cell
counts respected; the <80 arm skipped at n = 2, disclosed).

## 5. Consequence

1. **Paper 238's kernel claim stands, refined.** The two-component description survives on
   legitimate full-size hits alone (w_edge .0403, ΔAICc 49.78, CI excluding 0). Nothing in this
   reanalysis overturns paper 238 — it CORRECTS its interpretation: the 8.6%-mass spike quoted
   there conflates two objects.
2. **The spike is not one object.** Any future positional-shape model needs BOTH the kernel AND
   a bitlen(v)-band stratification at the left edge; fitting one edge component across all v
   sizes mixes an inclusion artifact with genuine structure.
3. **The tiny-v mechanism is arithmetic, not statistical.** Sub-2^95 hits land in D1 by the same
   inequality as §3 — a model-level fact usable downstream (e.g. when simulating hit profiles or
   pricing scan-order advantage), not a data quirk.

## 6. Ledger catches (all disclosed)

1. **Degenerate exclusion clause** — pre-registered mechanical note fired exactly as deduced:
   D1 ⇒ v < 0.44·s² + o(s²) < 2^95 provably; fraction_removed = 1.0-by-geometry, zero evidence
   content; verdict rode on the refit clause per the registered adaptation.
2. **Kept-fit edge anchor adapted** to kept-left-edge u₀ = .110 instead of 0 — registered
   pre-run in the header (§1); without it the kept fit would test no exposed edge at all
   (support truncation).
3. **Own fitter, not paper 238's** — paper-238's b_edge parametrization was unavailable under
   read restrictions; a two-component Poisson bin fit reimplemented here (nb=50 anchor per
   exp582). Amplitudes are NOT numerically comparable to paper 238's scale; the comparison
   quoted above is internal to this experiment's fitter.
4. **Controls = capped first-4000 non-hit j per N**, stream-order independent of position →
   valid uniform-density reference; not the paper-238 control construction.
5. **pop_hash recomputed, no external copy readable** — lineage rests on the 128×2 exact
   isqrt→(jlo,jhi) matches plus containment, not on hash equality with an external record.
6. Smoke run preceded the full run as pipeline validation only; wall 42.34 s; no commits during
   the run; only exp589_* files touched.

## 7. Barrier validation

No breakthrough claimed — this is a reanalysis INSIDE the positional layer (papers 228–230,
238): it refines what that layer's shape law says at the left edge, it does not touch the rate
residual. Consequently: residue cap 4/3 theorem untouched; position 5.19× measured untouched;
external class/interval hint laws untouched; quantum frontier untouched; the four-class
rate-residual closure of paper 237 untouched; abelian pinning ladder, QS calibration, and
utility closure untouched. Asymptotic relevance per the standing directive: the decomposition is
scale-informed (bitlen bands generalize to any bit length; the D1⇒v<0.44s² bound is exact
arithmetic at every scale, so the tiny-v inclusion channel GROWS relatively with the gap
structure at larger N) — a falsifiable constraint any future sieve-position or smoothness model
must carry. Paper 238's erratum-grade .2346 provenance flag still travels forward until
reconciled against the paper-228 ledger.

## Attribution

Experiment + analysis artifacts: `ResearchOutput/scripts/2026-08-24-round74/`
(exp589_spike_origin.py — pre-registration incl. the mechanical note and anchor adaptation in
header; exp589_smoke.log; exp589_run.log; exp589_result.json — config/rows/decomposition/stats/
verdicts/honest_notes/wall_s; exp589_findings.md).
Recorded round-84 #2; notebook Part 281; assessment v346; issue #387.

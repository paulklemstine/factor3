# Paper 240 — SPIKE-ORIGIN [FINAL RESOLUTION]: Paper 238's Left-Edge Spike is TINY-v COMPOSITION ENTIRELY (H1a-INCLUSION-ARTIFACT) — All 1554 First-Decile Hits Have bitlen(v) < 96 by Window Geometry (D1 ⇒ v < 0.44·s² < 2⁹⁵ Provable), Size-Matched Bands Erase the Within-Band Excess (rr_d1 = 1.000 / 1.097; Band-Referenced +130 vs Flat-Null +605), and the Kept-Fit "Persistence" DECOMPOSES ENTIRELY into a Truncation-Boundary Dickman Gradient (bitlen[96,98): ΔAICc 5.94 Sub-Bar; ≥98: −0.40 Absent) — **ERRATUM to Paper 239: "Half Genuine Small-|v| Structure" RETRACTED** — NO Positional Kernel Component Survives: the Profile is Fully Accounted by Magnitude + Tiny-v Window Geometry

**Verdict name: H1a-INCLUSION-ARTIFACT** (authoritative reading, findings.md rev 2026-08-24b) — superseding the
pre-registered-tree letter **H0-MIXED** (paper 239), which stands preserved as the audit record of the intermediate
analysis state.

Round-85 #1 · exp 589 [FINAL RESOLUTION] · pure reanalysis of `exp581_regen_positions.npz` (9594 pooled hits over
128 Ns × full j-window; 512k paired controls; wall_s 45.16; population seed 20260828, bootstrap seed 20260902,
2000 reps) · sources: `ResearchOutput/scripts/2026-08-24-round74/exp589_{spike_origin.py, smoke.log, run.log,
result.json}` + `exp589_findings.md` [FINALIZED rev 2026-08-24b] · completes the papers 228 → 239 → 240
spike-origin arc.

## 1. Pre-registration history, verbatim (written BEFORE any analysis run)

Registered hypotheses and verdict tree (verbatim from `exp589_spike_origin.py` header; full operationalization in
paper 239 §1, unchanged):

> H1a (INCLUSION ARTIFACT): excluding ALL hits with v.bit_length() < 96 removes >=70% of the first-decile
>   spike mass, AND the remaining profile's edge component becomes insignificant (two-component Delta-AICc
>   improvement drops below 6 OR w_edge bootstrap CI includes 0).
> H1b (REAL small-v structure): the spike persists among FULL-SIZE v hits only (>=70% of spike mass remains),
>   i.e. genuine elevated smoothness in the legitimate small-|v| region beyond Dickman prediction.
> H0-MIXED: split outcome => report the fraction honestly.
> VERDICT TREE: H1a iff fraction_removed>=0.70 AND (dAICc_kept<6 OR CI_kept covers 0). H1b iff
>   fraction_removed<=0.30 AND dAICc_kept>=6 AND CI_kept excludes 0. Else H0-MIXED.

Plus the pre-run mechanical note and anchor adaptation, both registered before any run (paper 239 §1): D1 ⇒ v <
0.44·s² + o(s²) < 2⁹⁵ provably under window j ∈ [isqrt(N)+1, 3·isqrt(N)], N 96-bit; kept fit anchors the
half-Gaussian at the leftmost bin with nonzero kept exposure.

**Revision chain (the resolution):**

1. **First pass** ran the registered tree literally: fraction_removed = 1.0 ≥ 0.70 held BY GEOMETRY (degenerate),
   insignificance failed on the kept fit's letter (ΔAICc 49.78, CI [.0301,.0525] excluding 0) → tree output
   **H0-MIXED**, recorded as paper 239 (issue #387) with the split read "half artifact, half genuine."
2. **Rev 2026-08-24b** resolved the split with POST-HOC matched-v diagnostics (band-referenced D1 decomposition +
   within-kept subband refits). The kept-fit "persistence" decomposes ENTIRELY into bitlen[96,98) hits sitting at
   the truncation boundary; no stratum carries a positional edge beyond the bar. Resolution to **H1a** requires NO
   changed bar: the REGISTERED significance threshold (two-component ΔAICc ≥ 6) applied to the matched-v strata is
   exactly what kills the persistence — [96,98) scores 5.94 (below the registered bar of 6), ≥98 scores −0.40
   (component absent). The dated REVISION NOTE lives in `exp589_findings.md`; `result.json` verdicts.verdict keeps
   "H0-MIXED" untouched as audit record. No registered bar was changed post hoc.

Read restrictions honored as registered: analyses built only from `exp581_regen_positions.npz` +
`exp582_findings.md`; exp578 read solely for the sanctioned regeneration recipe.

## 2. Regeneration discipline held throughout the lineage chain

Population regenerated verbatim from exp578's recipe (seed 20260828): **128×2 EXACT isqrt→(jlo,jhi) matches**
against the npz plus containment of every stored j (pop_hash 06931068f8f3ca9b recomputed; no external copy
readable — disclosed, lineage rests on exact reproduction). Upstream, the same chain already carried exp581's
sha256 byte-exact quartet verification (55729f1c99c0b5d2 over all 9594/9594 hits + capped non-hit arrays + grids)
and its two self-caught pipeline fixes (§7 items 6–7). The chain exp578 → exp581-regen → exp589-reanalysis is
verified end to end.

## 3. The mechanical forcing confirmed exactly — D1 mass is tiny-v by arithmetic

All 1554 first-decile (D1, u < 0.1) hits classified by bitlen(v):

| band bitlen(v) | hits | hits in D1 | D1 mass share of band | rr_d1 vs window |
|---|---|---|---|---|
| <80 | 0 | 0 | 0 | — |
| 80–89 | 85 | 85 | 85/85 = 1.000 | **1.000** |
| 90–95 | 2288 | 1469 | .642 | **1.097** |
| ≥96 | 7221 | **0** | **0.000** | — |

**100% of first-decile hit mass has bitlen(v) < 96** — mechanically forced, exactly as the pre-registered bound
predicted: every D1 hit has v < 0.44·s² < 2⁹⁵, so zero full-size (≥96-bit) hits can land in D1. Controls confirm:
zero D1 controls in band ≥96 either; per-N D1-share z-statistics mean −0.223, sd 0.945, absmax 2.53 over 128 Ns;
band × decile independence extreme (ctl in-band D1 shares 1.000 / .585 / .000).

## 4. Size-matched bands erase the within-band excess — composition, not decile-1 rate elevation

Referencing each band's own window-wide rate instead of the flat 0.10 null (POST-HOC, disclosed):

| band | D1 obs | expected (band-referenced) | excess |
|---|---|---|---|
| <80 | 0 | 0.0 | 0 |
| 80–89 | 85 | 85.0 | **0.0** |
| 90–95 | 1469 | 1339.34 | **+129.66** |
| ≥96 | 0 | 0.0 | 0 |

Total D1 excess vs flat-null: **+604.76** (rate_ratio_d1 = 1.637). Band-referenced total: **+129.66**. The
80–89 band shows rr_d1 = 1.000 EXACTLY (all-in-D1 by geometry, no elevation); 90–95 shows rr_d1 = 1.097 (marginal).
Roughly four-fifths of the flat-null "spike" is band COMPOSITION — tiny-v draws piling into D1 because the window
geometry puts them there — not any decile-1 rate elevation.

## 5. The kept-fit "persistence" decomposes entirely — truncation-boundary gradient, not structure

Two-component Poisson bin fits (nb=50 equal-width u-bins, control-shape bulk, half-Gaussian edge; cluster-over-Ns
bootstrap 2000, seed 20260902):

| Fit population | n hits | w_edge [95% CI] | ΔAICc vs null |
|---|---|---|---|
| ALL hits | 9594 | .0794 [.0702, .0908] | 374.77 |
| KEPT (v ≥ 2⁹⁵) | 7221 | .0403 [.0301, .0525] | 49.78 |
| POSTHOC: kept ∩ bitlen[96,98) | 3386 | .0305 | **5.94 — below the registered bar of 6** |
| POSTHOC: kept ∩ bitlen ≥ 98 | 3835 | .0240 | **−0.40 — component absent** |

The kept fit's apparent significance (49.78, CI excluding 0) is carried ENTIRELY by the [96,98) stratum — the two
bit-length bins immediately above the truncation boundary, where the half-Gaussian anchors (u₀ = .110, the point
where v crosses 2⁹⁵). That stratum scores BELOW the registered significance bar once isolated; the genuinely
full-size remainder (≥98) has NO edge component at all. This is the Dickman size gradient re-entering through the
truncation edge — smaller v is smoother by magnitude, and cutting the population at 2⁹⁵ creates a residual
smoothness gradient at the cut — not positional structure. (Subfits carry no bootstrap CI, disclosed; bulk null is
control-shape, NOT Dickman-normalized, so any "beyond Dickman" reading carries that caveat.)

## 6. THE ERRATUM to paper 239 (issue #387)

Paper 239's intermediate H0-MIXED letter is PRESERVED (result.json verdicts.verdict unchanged; findings.md REVISION
NOTE dated 2026-08-24b). The following PRINTED claims of paper 239 are RETRACTED as truncation-boundary gradient:

1. **Title claim**: "Half GENUINE Elevated Smoothness that PERSISTS Among Full-Size v ≥ 2⁹⁵ Hits … the Kernel
   SURVIVES at Reduced Strength." — Retracted. Nothing genuine persists; the kept-fit signal is boundary-stratum
   composition ([96,98) ΔAICc 5.94 sub-bar; ≥98 −0.40).
2. **§4 split reading**: "~half is genuine small-|v| structure beyond Dickman prediction." — Retracted; see §4–§5
   here. The correct partition is: ~100% of the spike is inclusion/composition artifact of window geometry +
   magnitude.
3. **§5 consequences 1–2**: "paper 238's kernel claim stands, refined … the kernel survives at REDUCED STRENGTH"
   and "the spike is not one object … needs BOTH the kernel AND a bitlen(v)-band stratification." — Superseded by
   the map statement below: there is no kernel component to stratify.

PRESERVED from paper 239 (confirmed, some strengthened): §3's mechanical-degeneracy finding (now load-bearing — it
carries the entire explanation); §2's regeneration verification; controls-clean; the honest ledger disclosures;
and the H0-MIXED verdict letter itself as the audit record of the intermediate analysis state. No registered bar
was altered post hoc; the resolution proceeds through the REGISTERED bar applied to matched-v strata.

**Map statement (arc closure, papers 228 → 239 → 240):** NO positional kernel component survives in the left-edge
profile. It is fully accounted by (i) magnitude — Dickman-type smoothness depending on |v| size — plus (ii) tiny-v
window geometry — the D1 ⇒ v < 0.44·s² < 2⁹⁵ inclusion channel, exact arithmetic at every scale.

## 7. What survives elsewhere

- **The overdispersion itself is real**: the first-decile smooth-hit excess (+605 vs flat null, rr 1.637) is a
  genuine feature of the data — this resolution names its origin (composition), it does not delete the phenomenon.
- **The positional layer remains independent** (papers 228–230: scan-order position 5.19×, class structure):
  established against rate, untouched here; this arc concerns the SHAPE of the u-profile among hits, a different
  object.
- **The rate-layer question stays open**: whether any genuine beyond-magnitude rate structure exists (papers
  232/234's u*≈0.65 geometric-window feature, accounted as geometry by exp581/582; the ~31%-above-floor residual
  per-N question) is NOT closed by this result and remains the open front.

## 8. Ledger catches (all disclosed)

1. **Degenerate exclusion clause** — pre-registered mechanical note fired exactly: fraction_removed = 1.0-by-
   geometry; the clause cannot discriminate; resolution therefore rides on matched-v refits, not on the fraction.
2. **Kept-fit edge anchor adapted** to kept-left-edge u₀ = .110 (registered pre-run; support truncation).
3. **Own fitter, not paper 238's b_edge parametrization** — amplitudes not numerically comparable across papers;
   comparisons internal to this fitter.
4. **Controls = capped first-4000 non-hit j per N** (position-uniform reference; not paper 238's construction).
5. **pop_hash recomputed, no external copy readable** — lineage rests on the 128×2 exact isqrt matches +
   containment, atop exp581's sha256 byte-exact verification upstream.
6. **Comparator bug (lineage chain)** — exp581 run-1 G1 "failure" was a comparator bug (paired slices compared vs
   stored full 4000-cap arrays; hits were byte-exact all along); disclosed upstream, inherited knowingly here.
7. **LN-dict crash (lineage chain)** — exp581 run-2 KeyError 350983 (ln-cache lookup on observed sub-band edge);
   fixed upstream with an arbitrary-edge ln cache + resume path; exp589's downstream re-verification passed on top.
8. **POST-HOC labeling** — band-referenced decomposition and subband refits are post-hoc diagnostics, never
   verdict-bearing under the original registration; the resolution's legitimacy comes from applying the REGISTERED
   ΔAICc ≥ 6 bar to them, changing nothing.
9. **Subfits carry no bootstrap CI** (disclosed); bulk null control-shape, not Dickman-normalized.
10. **Wall-time transcription drift** — paper 239 quoted wall 42.34 s; artifacts record wall_s 45.16 (log end
    45.73 s). Cosmetic; noted for the ledger.
11. Smoke preceded full run as pipeline validation only (smoke n=16, boot 200); no commits during runs; only
    exp589_* touched.

## 9. Barrier validation

No breakthrough claimed — final closure of a reanalysis INSIDE the positional layer's shape description. Untouched:
residue cap 4/3 theorem; position 5.19× measured; external class-hint law 1/(1−(1−θ)P_hit); external interval-hint
coverage × width law; quantum frontier; method stratum map; abelian pinning ladder; QS calibration; utility
closure; paper 237's four-class rate-residual closure. Asymptotic relevance per the standing directive: the two
surviving mechanisms are SCALE-CARRYING — the D1 ⇒ v < 0.44·s² bound is exact arithmetic at every bit length, and
magnitude-carried smoothness gradients strengthen relatively wherever windows truncate, so the composition channel
GROWS with scale rather than washing out; both are falsifiable constraints on any future sieve-position or
smoothness model. Paper 238's erratum-grade .2346 provenance flag still travels forward until reconciled against
the paper-228 ledger.

## Attribution

Experiment + analysis artifacts: `ResearchOutput/scripts/2026-08-24-round74/` (exp589_spike_origin.py —
pre-registration incl. mechanical note and anchor adaptation in header; exp589_smoke.log; exp589_run.log;
exp589_result.json — config/rows/decomposition/stats/subband_fits_POSTHOC/verdicts/honest_notes/wall_s;
exp589_findings.md [FINALIZED rev 2026-08-24b, authoritative]; data source exp581_regen_positions.npz).
Recorded round-85 #1; notebook Part 282; assessment v347; issue #388.

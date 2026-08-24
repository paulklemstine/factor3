# exp589 SPIKE-ORIGIN (round-74) -- findings [REVISION 2026-08-24b]
Question: is the paper-238 left-edge spike (8.6% D1 mass) carried by tiny-v
hits (bitlen(v)<96)? Pure reanalysis of exp581 npz; Ns regenerated verbatim
exp578 seed 20260828; lineage = 128x2 exact isqrt->jlo/jhi matches + containment.

AUTHORITATIVE VERDICT (rev 2026-08-24b): **H1a-INCLUSION-ARTIFACT**
(resolved from pre-registered H0-MIXED letter -- see REVISION NOTE)
- D1 hit mass by v-band (all 1554 D1 hits): <80 0, 80-89 85, 90-95 1469, >=96 0
  => 100% of D1 mass has bitlen(v)<96 -- mechanically forced: D1 =>
  delta<0.2s => v<0.44*s^2<2^95 under window [isqrt(N)+1,3*isqrt].
- Size-matched bands erase within-D1 structure: rr_d1 1.000 (80-89), 1.097
  (90-95); band-referenced D1 excess +130 vs +605 flat-null => the spike is
  band COMPOSITION, not decile-1 rate elevation.
- Kept-fit (v>=2^95) significant on its letter (w_edge 0.0403 CI[0.0301,0.0525],
  dAICc 49.78) but decomposes: bitlen[96,98) dAICc 5.94 (sub-bar), bitlen>=98
  dAICc -0.40 (absent) => truncation-boundary Dickman size gradient, not
  positional structure; bulk null is control-shape not Dickman-normalized.
CONSEQUENCE: paper 238 spike = tiny-v INCLUSION ARTIFACT; erratum against
paper 239 "half genuine small-|v| structure". Ref ALL: w_edge 0.0794
CI[0.0702,0.0908] dAICc 374.77.

REVISION NOTE (2026-08-24b): first pass recorded **H0-MIXED** by the
pre-registered tree (degenerate exclusion clause + significant refit clause);
preserved here and as result.json verdicts.verdict="H0-MIXED"; post-hoc
matched-v diagnostics resolve FULLY toward artifact; no registered bar changed.
Numbers: rows.band_table_hits_vs_ctl, decomposition_band_referenced_D1_POSTHOC,
stats.subband_fits_POSTHOC, stats.fit_all/fit_kept + ci_w_edge_*.
Honest: mechanical-degeneracy + kept-anchor adaptations registered pre-run;
own Poisson fitter (nb=50), not paper-238 b_edge; subfits no bootstrap CI;
controls = capped first-4000 non-hits/N, position-uniform.
Wall 45.16s full / smoke n=16; boot 2000 seed 20260902; no commits;
only exp589_* touched.

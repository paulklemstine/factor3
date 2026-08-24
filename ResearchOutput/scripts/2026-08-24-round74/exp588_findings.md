# exp588 EDGE-KERNEL-REFINEMENT -- findings
Question: does T=A(1+x)^{-b_bulk}+K(1+x)^{-b_edge} (b_edge>b_bulk+.3) resolve paper
234's left-edge steepness tension, or is the single -1.104 law final? Bars
pre-registered in script header before the full fit (smoke = pipeline validation).
Data: 9594 pooled hits from exp581_regen npz, x=(p-jlo)/(jhi-jlo), 128 Ns;
controls 512k ctl_* same intervals.
VERDICT: **H1 CONFIRMED -- edge kernel real structure, not noise** (single law
retired as final FORM)
- single law reproduces exp579 (b_nls=1.097; MLE 1.123) but its left-decile pred
  .1415 sits BELOW observed .1620 [.1547,.1695] -> tension real
- registered two-comp fit: dAICc improvement 37.3 (>6), LRT p=9.3e-10; b_bulk=.573
  [.412,.767], edge weight 8.6% [6.4,10.8]%; fitted left-decile .1617 boot CI
  [.1557,.1695] COVERS observed -> all registered bars PASS
- BOUNDARY DISCLOSURE: delta=b_edge-b_bulk=10.000 pins the IMPLEMENTATION CEILING
  (registered degeneracy rule covered only the lower bound; boundary not forbidden);
  read b_edge >= ~10.6. Settled by POST-HOC cap-40 refit: interior optimum b_edge=22.5
  (unpinned), improvement GROWS (dAICc 42.5, p=6.9e-11), left-decile CI still covers ->
  ceiling was conservative CENSORING, verdict cap-robust. Honest statement:
  b_edge >= ~10.4-11.1 (CI lower bounds across caps); exact value unidentified near-spike
  (cap40 boot CI [11.1,20.5,41.0]).
- controls: dAICc -4.3 (two-comp worse), w~1e-4 -> no kernel in controls
- POST-HOC attribution: 56% of SSR improvement in first decile, ~0% at the known u*~.65
  hump -> edge-driven, not hump absorption; left-half refit confirms (dAICc 16.8, p=2.6e-5)
READING: flat-ish bulk (b_bulk~.57-.79) + narrow left-edge spike (~4-9% of mass within
x<~.1). For paper 234: genuine missing left-edge structure; mixture RE-PARTITIONS the
profile (bulk .57-.79, NOT -1.104). Edge/end 2.62 vs single-law-implied 2^1.10=2.14.
Honest: (1) task-stated observed .2346 NOT reproducible under canonical normalization
(.1620 pooled [.1547,.1695]; per-N/log/(p-jlo)/jlo/inv-n variants also miss; .2346 also
outside two-comp prediction CI) -- DEFINITIONAL PROVENANCE GAP vs paper 234, flagged for
reconciliation; all coverage judged against data-observed value. (2) dAICc sign bug caught
and fixed BEFORE full-run verdict recording. (3) LRT null on boundary (chi-bar-sq
conservative); significance required BOTH LRT and dAICc>6. (4) Edge/end ratio has last-bin noise.
Wall 12.9s; nboot 500/300/200; seed 588; no commits; only exp588_* touched.

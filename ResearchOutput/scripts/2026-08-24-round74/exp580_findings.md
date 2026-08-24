# exp580 POSITIONAL-RATE-LINK (round-74, paper-228 follow-up b) — findings
VERDICT (pre-registered): **H0 INDEPENDENT-LAYERS** — hit-rich vs hit-poor
positional profiles do NOT differ at the registered bars; WITHIN-N positional
geometry and BETWEEN-N rate variance enter the map as TWO separate entries.
Setup: exp578_positions.npz verbatim (128 bitlen-96 semiprimes, seed 20260828,
9594 hits); u=(j-jlo)/(jhi-jlo); terciles by per-N hit count (poor<=64, mid
64-80, rich>=80; 42/42/44). Pre-reg families: (A) 3 pairwise pooled KS +
per-decile minima, Bonferroni to p_adj<0.01; (B) logistic hits-in-bin ~ rich +
bin + rich x bin on 50 bins (4300 rows), joint LRT df=49 p<0.01 + permutation
p<0.05. Control arm = paired ctl_* grouped by host-N label, size-matched to hit
counts (constant 4000-count split unusable, pre-disclosed).
RESULTS: (A) NO FIRE — rich-poor KS D=0.0462 raw p=0.0038 -> p_adj=0.049;
per-decile 0 cells p<0.01 raw; control A clean (min p_adj=0.235).
(B) NO FIRE — LRT chi2=51.31/49 p=0.383, perm p=0.34, 0/49 Wald bins;
control B FIRED spuriously (perm p=0.012) — occupancy-regression fragile on
dense size-matched controls (quasi-separation in sparse tail bins; ORs clipped);
treatment was far from the bar so H0 does not rest on it, but treat design-B as
unreliable for control arms.
PROFILES: near-identical shapes; edge-decile frac rich/mid/poor
0.229/0.245/0.230 (all replicate exp578's 0.2346 edge excess); bin-1 mass
0.042/0.047/0.041 with overlapping bootstrap CIs.
POST-HOC DESCRIPTIVE (not confirmatory, chosen after seeing profiles): poor-N
hits sit at larger mean_u (0.4556 vs rich 0.4351); rich-minus-poor -0.0205,
cluster-boot 95% [-0.0337,-0.0075], sign flips (+0.012, CI straddles 0) in the
matched-control arm. Weak directional hint that higher-rate Ns concentrate
slightly harder toward small-j — below every registered bar; candidate motive
only for a powered follow-up (e.g. continuous count ~ mean_u correlation),
NOT a map claim.
CONSEQUENCE: the small-j locus does not preferentially concentrate around
specific N classes at these bars — paper-228's positional entry and the rate
entry stay SEPARATE; the ~39-61% unexplained overdispersion is not carried by
profile-shape heterogeneity across terciles.
Files: exp580_positional_rate_link.py (pre-reg header), exp580_result.json,
this file. Wall 30.5 s, single run after plumbing fixes (no result changed).

# exp598b MIXTURE-RATE-CELLS (round-74) -- findings

Question (completes the rate-layer coverage matrix): papers 227/235/236 tested
QR DIALS (weighted marginals S_alpha); exp596 tested pairwise interactions;
UNTESTED: does the FULL 16-cell divisibility mixture -- the joint class vector
(2|v, 3|v, 5|v, 7|v) with v = j^2 - N -- explain per-N hit-rate variance
BEYOND the sqrt dial S_sqrt,400?

PRE-REGISTRATION in module header BEFORE analysis. Bars fixed:
H1 (mixture adds): hierarchical OLS log-rate ~ S_sqrt,400 alone VS ~
  S_sqrt,400 + cell fixed effects raises adj R^2 by >= 0.05 WITH permutation
  p < 0.01 (500 row-shuffles of the cell labels);
H0 (dial sufficient): Delta adj R^2 < 0.02;
otherwise BORDERLINE-INCONCLUSIVE.
CONTROL: permuted-RATE arm (y shuffled, designs intact) must be null --
operationalized as p_ctrl > 0.05 AND max(control nulls) < observed Delta;
a non-null control FLAGS THE WHOLE INFERENCE.

Population: seed-20260827 VERBATIM regeneration of exp586 make_semiprime
(bits=96, n_pool=128, rejection recursion + dedup). Regen hash-check
CONDITIONAL (exp586_result.json stores no N strings/hashes; recipe identity
+ exp586's own recorded regeneration_verified=true 128/128 vs exp577 rows are
the mitigation). Two INDEPENDENT fresh streams per N (neither reuses exp577
rows): cell grid 50k samples (occupancy vector, reference cell dropped for
identifiability) + hit stream 50k samples (mean hits/N 779.0, min 354 =>
rate ~1.56e-2); window t in [0, 65536) from j0 = isqrt(N)+1; hit := full
1e6-smoothness via gcd-chain primorial(1e6) tester. perm_seed 598, 500 reps
both arms. Wall: smoke 28.9 s (32 Ns), full 551.6 s (128 Ns).

VERDICT: **BORDERLINE-INCONCLUSIVE, CONTROL-FLAGGED.**
Full-run numbers: Delta adj R^2 = **+0.0827** [dial-only 0.0209 ->
dial+cells 0.1036] -- CLEARS the H1 effect bar (>= 0.05); but
perm_p = **0.0399** MISSES the < 0.01 gate (perm null q95 = 0.0727,
max = 0.163 -- observed sits just past the 95th percentile, nowhere near
the 99th), AND the control arm FAILS nullity: ctrl_null_max = **0.186**
> observed 0.083 (ctrl_p_vs_obs = 0.0519 -- barely above the p>0.05 clause,
dead on the max clause). Per pre-registration neither claim is available:
NOT H1 (mixture adds), NOT H0 (dial sufficient). The label-permutation
machinery's own null range swallows the effect at this data size.

Reading: with n_pool = 128 and ~780 hits/N, a y-shuffle can produce
Delta adj R^2 up to 0.19 from pure noise -- the cell-design matrix is rich
enough (15 free betas) to fit shuffled rates to R^2 ~ 0.1+. Any future H1
claim needs more Ns, fewer free cells, or a paired design with tighter null
spread. Direction/sensitivity (NON-evidentiary): alpha = 1 sensitivity same
sign, Delta +0.066 [dial -0.0075 -> +cells 0.0587]; smoke (32 Ns) Delta
+0.346 with ctrl_ok false -- textbook small-n overfit, non-evidentiary per
lab rule. Cell betas vs reference are large and sign-scattered (+/-123
range) consistent with noise-dominated increments.

Consistency: does NOT contradict exp592's ledger catch #2 (kappa ordering
-- top divisibility cell ranking -- replicated across seeds). That was a
top-cell RANKING; this test asks whether the JOINT cells add RATE VARIANCE
beyond the sqrt dial's marginals -- unresolvable here. Rate-layer coverage
matrix (dials 227/235/236 -> pairwise exp596 -> joint cells 598b) CLOSES
UNRESOLVED-AT-RESOLUTION on the joint layer.

Ledger catches / honest limits:
- Regen hash CONDITIONAL (disclosed above; recorded, not asserted).
- Hit classifier operationalized as gcd-chain primorial(1e6) full-smoothness;
  exp577's exact tester source outside read allowance -- same tester CLASS
  and cut per task spec; absolute rates NOT comparable to exp577 rows.
- Control failure is itself the finding: it bounds what this design can
  detect and discredits any naive reading of the raw +0.083 as "mixture adds".
- No commits before crash; this findings file + paper 255 + assessment v362
  + notebook Part 297 written post-recovery from the completed result JSON.

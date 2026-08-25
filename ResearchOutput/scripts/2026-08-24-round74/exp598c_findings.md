# exp598c MIXTURE-RATE-CELLS-POWERED (round-74) -- findings

Question (re-fires exp598b's flagged question at its pre-stated power remedy):
does the FULL 16-cell divisibility mixture -- joint class vector (2|v, 3|v,
5|v, 7|v), v = j^2 - N -- explain per-N hit-rate variance BEYOND the sqrt dial
S_sqrt,400?

PRE-REGISTRATION v2 in module header, amended BEFORE any full-mode data existed
by a two-agent adversarial audit of v1 that caught TWO MUST-FIXES:
(1) 598b's control_ok conjunction (p_ctrl>0.05 AND max(ctrl_null)<d_obs) is
    LOGICALLY UNSATISFIABLE -- p_ctrl>0.05 forces >=25/500 shuffle deltas >= obs,
    which forces max >= obs. control_ok=False was guaranteed BY CONSTRUCTION;
    v2 gates H1 on clean_control := max(ctrl_null)<d_obs and H0 on
    machinery_ok := |mean(ctrl_null)|<0.01; p_ctrl descriptive only.
(2) v1's master seed 20260903 was NOT fresh -- it is exp601's recorded lineage
    (own_lineage_hash16 fa1746a5b065cbd9 reproduces as the prefix of
    build_population(20260903,512)); withdrawn to 20260907 (registry-verified
    unused), self-exclusion asserted. Also fixed: degenerate kappa arm
    (D>0 popcount identically 16 on occupancy fractions -> rebuilt from cell
    marginals), 52-value stream-band overlap with 598b (offsets moved
    +7e6/+9e6 -> +17e6/+19e6, band disjointness asserted numerically),
    undisclosed flag->gate promotion (disclosed), mislabeled raw-R2 key.
Stream discipline: pools for ALL 11 prior population seeds regenerated at
n=512 (prefix-complete), pairwise mutually disjoint vs new pool AND mutually;
20260901 documented-excluded (bootstrap-only usage).

Population: seed-20260907 verbatim make_semiprime (bits=96, n_pool=512);
two INDEPENDENT fresh streams per N (cell grid 50k, hit stream 50k; mean
762.6 hits/N, range [297,1558]); window t~U[0,65536) from j0=isqrt(N)+1;
gcd-chain primorial(1e6) tester; perm seed 599, 500 reps both arms.
Wall 286.5 s full (parallelized, positional-seed deterministic, spot-check 8/8
exact) / smoke 13.5 s.

VERDICT: **H1_MIXTURE_ADDS** (closing branch none).
Delta adjR^2 = **+0.105498** [dial-only 0.051576 -> dial+cells 0.157074]
(clears >= 0.05); perm_p = **1/501 ~= 0.001996** -- ZERO of 500 cell-label
shuffles reached the observed delta (perm null q95 0.0189, max 0.0402);
clean_control TRUE (ctrl null max **0.054872** < 0.1055); machinery_ok TRUE
(|mean| 6.9e-05). All three registered bars pass simultaneously.

THE POWER REMEDY VALIDATED: the y-shuffle null range collapsed from
{n=128: ctrl_max 0.186} to {n=512: ctrl_max 0.0549} (~3.4x, consistent with
the p/(n-p) overfit scaling of a 15-column design at 4x the rows) while the
effect GREW (+0.083 -> +0.105 across independent seeds/populations).
exp598b's BORDERLINE resolves as UNDERPOWERED, not null.

MECHANISM (secondary arm, reportable post-fire): the SINGLE expected-popcount
covariate kappa_i = sum_k P(l_k|v_i) assembled from the cell marginals
captures Delta = **+0.114** alone [0.0516 -> 0.166] -- matching or exceeding
the full 15-cell basis. The increment is not 15 independent cell effects; it
is COMPOSITION ORDER (how many distinct small primes divide v), a graded
one-dimensional structure. alpha=1 sensitivity arm agrees (+0.108).

CONSEQUENCE: papers 227/235/236's additive completeness upgrades from DIAL
level to CELL level -- divisibility composition of v carries per-N rate
structure beyond the QR dial's weighted marginals; the rate map refines to
CELL level with kappa as its dominant axis. Consistent with exp592's
kappa-ordering replication (now understood as the visible tip of this graded
law) and with paper 88's label-composition results. Catalog scan (loop step 2):
no prior work on joint divisibility mixtures or permutation-calibrated
variance increments (closest: our own QR-dial line pkg 882).

VERIFICATION: independent verifier recomputed ALL stats from
exp598c_verify.npz alone with a from-scratch code path -- headline d_obs
EXACT to full float64 precision, perm_p bit-exact, permutation arrays
regenerate bit-exactly from the documented call order, y reconstruction
exact (the +0.5 smoothing is definitional). Adjudication auditor: all
overturn attempts failed (rule-textual, statistical validity, leakage,
multiplicity/forking, worst-case seed-swap); occupancies match closed-form
independence products (cell15 0.0045 vs 1/210). Chain-of-custody caveat:
v1 smoke artifacts were overwritten, so pre-data integrity rests on
filesystem forensics (header ctime predates all data artifacts; wall_s
matches log birth->mtime span) -- ADOPTED PROCESS LAW: future
pre-registrations get committed (or hashed in-repo) BEFORE any
data-producing run.

ERRATA CARRIED (ride here per lab rules): (1) paper 255's "control fails on
its max clause" framing corrected -- the conjunction was unsatisfiable by
construction; informative content was c = 25/500 (obs at the y-shuffle 95th
percentile); 598b's BORDERLINE itself stands (it never gated on control_ok).
(2) 598b latent cell_beta mislabel (enumerated unfiltered keep list over a
possibly-filtered Dr; not triggered in its run) fixed here.

Ledger catches: regen hash still CONDITIONAL (no stored N strings anywhere in
lineage; disclosed). Absolute rates internally consistent only (tester class
matched, not source-verbatim). No commits prior to recording; recovered
pipeline ran clean end-to-end post-audit.

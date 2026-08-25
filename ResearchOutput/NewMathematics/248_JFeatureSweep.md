# Paper 248 — J-FEATURE-SWEEP: **H0_CARRIER_OPEN** — No J-Arithmetic Feature Carries the Mid-Window Hit Excess (All 8 Registered Families Tested on 104,200 Mid-Window Positions; Best Honest Ratio R = 1.11, mod-7 Cell 0, p = 0.36; Every Coarse Family Flat-DiD +0.001–0.002) — F5's Raw Max (j ≡ 73 mod 105, R = 1.558) Sits BELOW the Null's Own Median Max-Ratio (1.633; Global Perm p = 0.754): Textbook Extreme-Value Noise Over 105 Cells — Consequence: the J-Arithmetic Hypothesis Class Is ELIMINATED; Route to CONSECUTIVE-V POLYNOMIAL-SEQUENCE DEPENDENCY STUDY per Pre-Registration

**Verdict name: H0_CARRIER_OPEN** — no registered feature class cleared the bar
(R ≥ 1.15 vs complement in-mid, family-wise max-statistic permutation p < 0.01 ×
Bonferroni K = 8, DiD sign-consistent), so the carrier of paper 242's mid-window
excess remains open AND its j-arithmetic branch is now measured-and-empty: the
excess is real (papers 239/241/242), divisibility-conditioned away as a rate dial
not a position dial (exp 588c), and NOT a property of the scan position j itself.

Round-91 #1 · exp 598 · sources:
`ResearchOutput/scripts/2026-08-24-round74/exp598_{j_feature_sweep.py,
smoke.log, full.log, result.json}` + `exp598_findings.md` · wall **271.3 s**.
Data: `exp581_regen_positions.npz` (sha256 `0b1afa50…36a38`, recorded in config),
128 windows, 521,594 positions / 9,594 hits; mid-window u ∈ [0.55, 0.75] holds
n = 104,200 positions, flanks [0.05, 0.40) ∪ (0.90, 1.00] hold n = 235,003;
rng seed 20260908. Flank window chosen PRE-analysis to avoid hump shoulders and
window-edge behavior.

## 1. Pre-registration verbatim (written BEFORE any analysis was run)

From the `exp598_j_feature_sweep.py` header:

> Question: the exp579/581 mid-window hump survived divisibility-mixture
> conditioning (exp582: stationary geometric feature at u*~=0.65). Is the
> carrier J-ARITHMETIC -- a property of the position j itself?
>
> H1 (j-carrier): at least one REGISTERED j-feature class shows hit-rate ratio
>   R >= 1.15 vs its complement WITHIN the mid-window u in [0.55,0.75],
>   permutation-calibrated (max-statistic, family-wise) p < 0.01 after
>   Bonferroni across registered families, AND corroborated by flanking-window
>   baseline subtraction (DiD sign-consistent, p_did < 0.05).
>   => carrier is j-arithmetic; name the winning class.
> H0: no feature class clears the bar => carrier remains open; route to
>   polynomial-sequence correlation analysis (= consecutive-v dependency study).
>
> Registered feature families (K=8 tested unless skipped):
>   F1 jmod4        : 4 cells {0,1,2,3} mod 4 (= parity x mod 4)
>   F2 jmod3        : 3 cells
>   F3 jmod5        : 5 cells
>   F4 jmod7        : 7 cells
>   F5 jmod105      : 105 joint cells (CRT of mod 3,5,7)
>   F6 omega_ter    : terciles of omega_small(j) = #{distinct primes <= 97 | j}
>                     (thresholds from pooled label-blind quantiles)
>   F7 dsq_smooth   : B-smoothness (exact 1e6) of d = |j - nearest_square(j)|;
>                     SKIP if degenerate (>98% single class or any cell
>                     n<200 or h<15)  [task: "skip if degenerate"]
>   F8 jsmooth_1e6  : exact indicator that j itself is 1e6-smooth
>                     (vectorized prime-strip to 1e6; exact, no heuristic)
> Windows: MID  = u in [0.55, 0.75]
>          FLANK = u in [0.05,0.40) union (0.90,1.00]  (boundary/shoulder margin;
>          registered here before analysis)
> Statistics per family/class c:
>   R_c    = rate_mid(c) / rate_mid(complement)          [PRIMARY]
>   DiD_c  = [rate_mid(c)-rate_flank(c)] - [rate_mid(~c)-rate_flank(~c)]
>   Cell gate: n_mid(c) >= 200 AND h_mid(c) >= 15 else class ineligible.
> Calibration: 500 label shuffles WITHIN window strata (permute y inside mid,
>   independently inside flank); statistic = max_c R_c (resp max DiD_c);
>   p = (#perm >= obs)/500. Family-wise by construction; then xK Bonferroni.
> Control (must be null): 300 fake-hit draws -- labels globally permuted at
>   matched prevalence, identical pipeline incl. bars; report max-R dist and
>   bar-clearing frequency.
>
> Honest notes registered up front:
>  - Positions/hit labels CONSUMED from exp581_regen_positions.npz (the artifact
>    whose seed-20260828 lineage regeneration was hash-proven IN exp581). This
>    script does NOT re-run the generator (generator source outside this task's
>    read allowlist); sha256 of the npz is recorded below for provenance.
>  - Hit labels are the upstream cut-1e6 classify (exp569 path) as frozen in the
>    npz; not recomputed here.
>  - F7's 'v' operationalized as v = j (scan position); nearest square via
>    round(sqrt(j)). If degenerate => skipped with reason, per registration.

*(Recorder note: verbatim transcription complete; authoritative source
`exp598_j_feature_sweep.py` header, lines 4–59.)*

## 2. Results — the eight-family table

Best-cell summary (mid-window; rate = hit rate in the best cell; pR = family-wise
permutation p on max-R; all p_adj = 1.0 after ×8 Bonferroni; no family clears
H1):

| family | best cell | n_mid | h_mid | rate | R | DiD | pR |
|---|---|---|---|---|---|---|---|
| F1 jmod4 | 1 (≡1 mod 4) | 26,091 | 452 | .0173 | 1.0748 | +.00180 | .369 |
| F2 jmod3 | 1 | 34,664 | 581 | .0168 | 1.0314 | +.00066 | .743 |
| F3 jmod5 | 3 | 20,878 | 364 | .0174 | 1.0785 | +.00147 | .475 |
| F4 jmod7 | 0 | 14,980 | 269 | .0180 | 1.1111 | +.00221 | .359 |
| F5 jmod105 | 73 | 1,022 | 26 | .0254 | 1.5578 | +.01249 | **.884** |
| F6 omega_ter | 0 (lowest tercile) | 44,793 | 740 | .0165 | 1.0107 | +.00077 | .978 |
| F7 dsq_smooth | 1 (smooth) | 86,211 | 1,421 | .0165 | 1.0224 | +.00086 | .771 |
| F8 jsmooth_1e6 | 0 (not smooth) | 90,036 | 1,483 | .0165 | 1.0232 | +.00058 | .767 |

Reading: every coarse family sits at R ≤ 1.11 with FLAT difference-in-differences
(+0.001–0.002 on a ~.088 base rate contrast) — parity/mod-3/mod-5/mod-7 residue
classes, ω-richness terciles, distance-to-nearest-square smoothness, and j's own
exact 10⁶-smoothness are ALL carrier-null WITHIN the mid-window. None comes
within reach of the R ≥ 1.15 bar once calibrated; the largest honest pR gap from
the bar is mod-7 cell 0 (R = 1.1111, p = 0.359).

## 3. The extreme-value-noise demonstration (F5 vs the null's own maximum)

F5 (j mod 105, 105 CRT joint cells) produced the sweep's raw maximum: cell 73
(j ≡ 73 mod 105), n = 1,022, 26 hits, rate .0254, **R = 1.558**, DiD +.01249.
This is exactly what a 105-cell lookover should manufacture when nothing is
there, and the run's built-in control says so quantitatively:

- Under 300 globally-permuted fake-hit draws run through the IDENTICAL pipeline
  (same 105 cells, same gates, same max-of-ratios statistic), the null max-R
  distribution is heavy-tailed BY CONSTRUCTION: **median 1.6334, p95 1.8516,
  max 2.0827**.
- The observed global max 1.5578 sits BELOW the null's MEDIAN. 226/300 null
  draws beat it ⇒ **global_perm_p = 0.754**. Its family-wise calibrated pR =
  0.884 agrees.
- So the single most impressive-looking number in the sweep is a below-average
  draw of the noise process that scanning 105 cells necessarily produces. Any
  "j ≡ 73 mod 105" claim would have been pure selection artifact — the
  demonstration is kept here as the canonical local example of why coarse-family
  maxima require max-statistic calibration before they mean anything.

The verdict therefore rests on the calibrated per-family permutation p +
Bonferroni (all p_adj = 1.0), with the pooled global check corroborating.

## 4. Routing consequence (registered H0 route)

Per the pre-registration, H0 routes to the **consecutive-v polynomial-sequence
correlation study**: if j-arithmetic classes do not carry the mid-window excess,
the next candidate carrier is dependence BETWEEN adjacent scan positions — the
sequence y_v = (⌊√N⌋+v)² − N is a degree-2 polynomial in v whose smoothness at
consecutive arguments is correlated through shared small-prime divisibility
patterns, a mechanism invisible to every marginal-on-j test run here. This
completes the paper-242 follow-up chain honestly: the non-divisibility positional
carrier (map entry from exp 588c/#390) is NOT any of {parity, mod-3/5/7 residue,
CRT-joint residues, ω-richness, nearest-square-distance smoothness, exact j
smoothness}.

## 5. Ledger catches

1. **Smoke caught an invalid smoothness early-exit rule**: the first prime-strip
   terminated on prime residuals ≤ 10⁶, misjudging them as smooth; post-fix the
   random-integer 10⁶-smooth fraction is 0.1355, matching Dickman ρ(u ≈ 2.45) ≈
   0.14 — an independent correctness check on the exact tester.
2. **Smoke caught an F5 gate-starve crash** (no eligible cell at smoke scale);
   fixed — F5 runs clean at full scale.
3. **F7 non-degenerate at full scale despite smoke appearance**: |j − nearest
   square| is 10⁶-smooth for 82.7% of positions, so both cells clear the gate
   comfortably (n = 17,989 / 86,211) — the registered skip rule did NOT fire.
4. **Generator not re-run — disclosed consumption**: positions/labels come from
   `exp581_regen_positions.npz`, whose seed-lineage regeneration was hash-proven
   in exp 581; the generator source sat outside this task's read allowlist, so
   the npz sha256 (`0b1afa50…`) is recorded for provenance instead. Hit labels
   consumed as frozen (upstream cut-1e6 classify, exp569 path).
5. **Recorder catch — registered View B not reported**: the header registers a
   second view ("B per-window-rate: per-N enrichment … count-weighted mean") but
   the result JSON contains no View-B computation; only a comment placeholder
   exists in the code. Harmless HERE because View A's verdict is H0 with every
   family far from the bar (a weaker second view could not rescue a bar-clearing
   claim it never supported), but the completeness of the pre-registration was
   not delivered and any future H1-side reuse of this design must implement or
   formally drop View B.

## 6. Barrier validation

No barrier interaction: this is a carrier-identification negative inside the
mapped positional stratum, not a barrier probe. Its map value is elimination —
the u* ≈ 0.65 mid-window excess (paper 242 lineage) now has its j-marginal
closed by measurement, sharpening the routing toward sequence-level (consecutive-v)
mechanisms rather than pointwise-j ones. Consistent with the asymptotic
directive: open frontiers remain u ≥ 6–14 scale-smoothness deviations, factor-local
methods outside scan-order framing, MA-1 effectivity, residue cap 4/3, position
5.19×, external-hint laws, quantum frontier closed. Named next probe (registered):
consecutive-v polynomial-sequence dependency study.

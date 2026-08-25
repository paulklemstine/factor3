# exp598 J-FEATURE-SWEEP (round-74) -- findings
Question: paper-242 mid-window excess survived composition + N-level conditioning
(exp582: stationary geometric feature u*~0.65) -- is the carrier J-ARITHMETIC?
8 registered j-feature families swept on exp581-regen positions (sha 0b1afa50...,
128 windows, 9,594 hits / 512k controls; mid u=[0.55,0.75] n=104,200; flank
[0.05,0.40)+(0.90,1.00] n=235,003). Pre-registration in header BEFORE analysis;
bars: R>=1.15 vs complement in mid, family-wise permutation (500, stratum-
preserving) p<0.01 x Bonferroni K=8, DiD corroboration.
VERDICT: **H0_CARRIER_OPEN** -- no class clears the bar.
family          best cell   n_mid   h_mid   rate     R      DiD      pR
F1_jmod4        1 (%4==1)   26091   452    .0173   1.0748 +.00180  .369
F2_jmod3        1           34664   581    .0168   1.0314 +.00066  .743
F3_jmod5        3           20878   364    .0174   1.0785 +.00147  .475
F4_jmod7        0           14980   269    .0180   1.1111 +.00221  .359
F5_jmod105      73          1022     26    .0254   1.5578 +.01249  .884
F6_omega_ter    0           44793   740    .0165   1.0107 +.00077  .978
F7_dsq_smooth   1           86211  1421    .0165   1.0224 +.00086  .771
F8_jsmooth_1e6  0           90036  1483    .0165   1.0232 +.00058  .767
READING: max raw ratio anywhere = F5 cell 73 (j=73 mod 105) R=1.558, but its
calibrated pR=0.884: under label shuffling the NULL max-of-105-ratios has median
1.633 -- the observed global max sits BELOW the null median (226/300 null draws
beat it, global_perm_p=0.754): textbook extreme-value noise. Every coarse family
R<=1.11 with flat DiD (+0.001-0.002 on a .088 base): parity/mod-3/5/7, omega
richness, distance-to-nearest-square smoothness, and j's exact 1e6-smoothness
are all carrier-null WITHIN mid-window. Consequence (registered H0 route): next
probe = polynomial-sequence correlation analysis = consecutive-v dependency study.
Honest: positions/labels CONSUMED from exp581 npz (lineage hash-proven there);
generator not re-run (outside read allowlist), sha256 recorded. Smoke caught 2
bugs pre-analysis: smoothness early-resolution rule killed prime residuals <=1e6
(fixed; random-int smooth fraction 0.1355 matches Dickman rho(u~=2.45)~=0.14)
and an F5 gate-starve crash. F7 NOT degenerate at full scale (82.7% smooth).
Wall 271 s full / 1.8 s smoke; rng 20260908; no commits; only exp598_* touched.

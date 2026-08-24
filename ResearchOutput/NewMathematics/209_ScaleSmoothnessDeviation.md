# Paper 209 — SCALE-SMOOTHNESS-DEVIATION: x²−N Is Random-Level in B-smoothness through u ≈ 8.3

**Verdict name: RANDOM-AT-SCALE.**
Round-73 #4 · exp 562 · assessment v316 · status 04_FINAL_TIME-CAPPED (disclosed) · script `exp562_scale_smoothness.py` (+ JSON/logs) · seed 20260827.

The standing directive's frontier cell, measured directly for the first time: does
x²−N deviate from size-matched randomness in B-smoothness at u = log v / log B in
{5,6,7,8} — the range where QS's L_N[1/3] exponent lives? This is the properly-
controlled redo of round-26 #3's honest INCONCLUSIVE (SUBEXP-STRATUM was underpowered,
ratios 0.26–9.27 non-monotone). B=1000; bins by ACTUAL candidate magnitude v ∈
[B^w, B^(w+1)); controls EXACTLY histogram-matched on (bitlen, mantissa-octant),
uniform within octant; ONE shared gcd-chain primorial code path for both populations;
assert pipeline 844 cases incl. 24 adversarial vs an exhaustive strip — 0 mismatches;
QR balance verified per bin (qr_weighted_mean = 1.003/0.998/0.997/1.000); priors used
only for time allocation, never results.

**Scale:** ~1.49e9 candidates tested PER ARM (119.6M / 209.3M / 448.5M / 717.6M across
bins 5–8), 4000 N-clusters per bin, cluster bootstrap n=2000, 23-min measurement window
(stopped at deadline). Truncation disclosed: with N ≤ 2^80 and x ≤ 4√N the reachable v
tops out near 15s² ≈ 3.75N — bin 7 tops out ~u 7.9, bin 8 ~u 8.5; achieved ranges
reported empirically.

**Result: NULL at every u ≥ 6.** r(u) = p_cand/p_ctrl = **1.0114 [0.947, 1.075]** at
ū = 5.96; **0.9486 [0.783, 1.152]** at 6.95; **0.900 [0.454, 1.700]** at 7.93;
**1.200 [0.500, 3.000]** at 8.26 — ALL CIs cover 1. Trend slope +0.036 log-r per u,
CI [−0.255, +0.345], bootstrap p = 0.831 — FLAT. Tightest 95% bound |r−1| ≤ **0.2168**
(bin u=6). All pre-stated deviation rules FALSE (trend ns; u6/u7/u8 none exclude 1).

**Secondary structure — real but confined to the low-u face.** N-level overdispersion
vs Poisson D = **1.61 [1.50, 1.73]** PERSISTS at bin 5 then DIES: 1.03 at bin 6, ~1.00
at bins 7–8 (both arms). The QR dial's grip decays with u: Spearman(per-N rate, QR
fraction) = 0.32 (perm p = 7e-4) → 0.14 → 0.04 → 0.04. Smooth hits cluster by N only
while u is small; by u ≈ 7 both the clustering and even the residue-dial correlation
are gone.

**Cross-check vs paper 130 (no novelty conflict):** paper 130 measured candidate/control
ratios 0.88–0.91 at scales to 2^44 (u < 4.75) and attributed them to a finite-x Dickman
correction SHARED WITH CONTROLS ("relation pool ensemble-equals unrestricted random").
This experiment asks whether any O(1) relative deviation EMERGES at u ≥ 5 — answer NO
within bound. CONSISTENT with and EXTENSIVE of paper 130's random-pool claim from
u < 4.75 to u ≤ 8.5.

Honest validation against the frontier map: this is the DIRECT test of the asymptotic-
goal directive's scale-smoothness priority (u ≥ 6), and the result is a bound-carrying
NULL — no O(1) smoothness edge from quadratic-polynomial structure exists at these
scales. What stays open: production-scale u ≥ 9 (unreachable at N ≤ 2^80 under the
j-cap — needs larger N or larger B), and the mechanism of the dispersion death between
u ≈ 6 and 7. Time-cap disclosed: bins 7/8 event counts tiny (18 vs 20, 12 vs 10), CIs
correspondingly wide; allocation fractions 0.08/0.14/0.30/0.48 fixed pre-analysis.
Barriers 4-frontier unchanged (null sharpens it). Now 552 experiments (max id).
Assessment v316.

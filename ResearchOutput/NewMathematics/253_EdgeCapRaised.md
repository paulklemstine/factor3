# Paper 253 — EDGE-CAP-RAISED: **H0 — SPIKE STEEPNESS FORMALLY UNIDENTIFIABLE AT THIS DATA SIZE; THE LOWER-BOUND LADDER IS FINAL** — Paper 245's Loose End Closes: b_edge Point Estimate 30.12 (b_bulk 0.84) IDENTICAL Across Raised Caps {80, 120, 240} While the Bootstrap CI Upper Edge Pins to Successive Caps [0.62, **80.00**] / [0.58, **120.00**] / [0.64, **160.24**] (Cap-Hit Fractions 7.8% / 4.9% / 1.8%) — Mass Thins Toward an Effective Ceiling ≈160 but the Pre-Registered Bar (BOTH 120 AND 240 Interior) Is Unmet at 120, So the Recorded Verdict Stands — Canonical Profile Description Amended: "Flat Bulk b ≈ .57 + Left-Edge Spike, Amplitude 8.6% [verified], Steepness >~15 [lower bound only; point ≈30, ceiling ≈160]" — Control Arm Clean Kernel-Free (√-Count Sensitivity b_edge = 44.12 Agrees With exp594's 40.46 Cross-Pipeline)

**Verdict name: H0-UNIDENTIFIED_LADDER_FINAL** — the pre-registered identifiability
test fired H0: raising the b_edge cap does not free an interior optimum whose CI
clears the box at every rung; the steepness of the left-edge spike is a
LOWER-BOUND-ONLY quantity at this data size.

Round-94 #2 · completes paper 245's named loose end (is b_edge interior-optimal,
or just boxed by the cap?) and closes the final measurement of the positional
thread's density layer (arc 228–252). Sources:
`ResearchOutput/scripts/2026-08-24-round74/{exp603_edge_cap_raised.py, exp603_result.json,
exp603_full_run.log, exp603_smoke.log}` on `exp581_regen_positions.npz`
(128 seeds, 9,594 hit points, 512,000 control points, zero clips either arm).
Wall 0.94 s full run; seed 20260824.

## 1. Pre-registration (verbatim, script header, written BEFORE any fitting)

> PRE-REGISTRATION (written BEFORE any fitting; nothing downstream may change it):
>   H1 (identifiable):  at CAP >= 120 the bootstrap CI upper edge of b_edge stays
>       strictly BELOW its cap (interior optimum stable) => b_edge +/- CI is
>       reported AS IDENTIFIED.
>   H0 (unidentified):  the CI upper edge keeps hitting successive caps =>
>       steepness formally UNIDENTIFIABLE at this data size; the lower-bound
>       ladder {CAP -> CI lower edge} is recorded as FINAL.
>   CONTROL BAR (preregistered): fits on ctl_* positions are KERNEL-FREE iff,
>       at every cap, point edge weight w_edge(x=0.9) < 0.10 AND the
>       1-comp -> 2-comp relative SSE improvement is < 5%.

Method (as registered): per-seed normalization x=(v−jlo)/(jhi−jlo) clipped [0,1]
(clips counted: 0/0); pooled histogram nb=50 over [0,1] (the exp581/582 anchor
grid); model T(x)=A(1+x)^(−b_bulk)+K(1+x)^(−b_edge); unweighted NLS on bin
densities with (A,K) profiled out linearly over a dense (b_bulk,b_edge) log grid
including near-cap points (0.90c/0.95c/0.98c/0.999c), then multi-start bounded
TRF refinement of the POINT fit; cluster bootstrap over the 128 seeds (resample
seeds with replacement, pool, regrid, reprofile), nboot 1000 main arm / 300
control arm; cap-hit := b_edge_hat ≥ 0.999·CAP; CI = percentile [2.5, 97.5].

## 2. The cap ladder

| cap | b_edge point | b_bulk point | 95% CI (cluster bootstrap) | cap-hit frac | pure-bulk frac | identified |
|-----|-------------|-------------|---------------------------|--------------|----------------|------------|
| 80  | 30.1223     | 0.83996     | [0.618, **80.00**]        | 7.8%         | 0.0%           | NO (hits cap) |
| 120 | 30.1223     | 0.83996     | [0.583, **120.00**]       | 4.9%         | 0.0%           | NO (hits cap) |
| 240 | 30.1226     | 0.83996     | [0.642, **160.24**]       | 1.8%         | 0.0%           | yes (interior) |

Point estimates are EXACTLY invariant under tripling the allowed box
(b_edge 30.12235 → 30.12234 → 30.12258; b_bulk 0.83996 at every cap; A≈1.31432,
K≈1.07678, rel-SSE improvement vs 1-component 0.7363 at every cap): the point
optimum was never pressed against any cap — the uncertainty is what hits the box.
The bootstrap CI upper edge pins to successive caps at 80 and 120 and only
DETACHES at 240 (160.24 < 240), with cap-hit mass decaying 7.8% → 4.9% → 1.8%
and boot median drifting 28.91 → 28.07 → 27.84 while the boot MEAN inflates
28.85 → 34.01 → 37.37 — a right tail that thins toward an effective ceiling
≈160 rather than vanishing at the imposed box.

**Why the verdict is nonetheless H0:** the pre-registered H1 bar requires the CI
upper edge strictly below its cap at CAP ≥ 120 — i.e., BOTH the 120 and 240
rungs interior. Cap 120 pins exactly (ci_hi = 120.00, 4.9% cap-hits), so the bar
is unmet and the recorded verdict stands as pre-written. The 240-rung detachment
(160.24 < 240, "identified: true" per-cap) is recorded honestly in the per-cap
block and in the amended canonical description as the effective-ceiling note —
it does not retroactively upgrade the primary booking. No post-hoc bar
adjustment in either direction.

**Lower-bound ladder — FINAL per pre-registration:** cap 80 → LB 0.62;
cap 120 → LB 0.58; cap 240 → LB 0.64. The floor sits at ≈0.6 at every rung —
at the bulk scale, as expected for a spike-vs-bulk degeneracy direction.
Historical anchor quoted for comparability: exp594 (paper 245) at cap 80 gave
point 40.46, CI [15.2, 80.0], cap-hit 26.7% — same qualitative pinning, tighter
and higher (that pipeline's internals were not replicated bit-for-bit here).

## 3. Control arm cleanliness

The preregistered kernel-free bar passes at EVERY cap on ctl_* positions:
point edge weight w_edge(x=0.9) ≈ 1e−45 … 1e−55 (bar < 0.10); 1→2-component
relative SSE improvement ≈ 1e−15 (bar < 5%); K driven to ~e−21–e−23; and
frac_purebulk = 100% across all 300 control boots at every cap — the control
histogram never sustains a spurious spike component. Control point b_edge rides
its own cap trivially with zero amplitude (K≈0), i.e., cap-hitting in the
control is amplitude-free and cannot mimic detection. Main-arm boots whose best
fit is pure bulk (K=0) have undefined b_edge: excluded from the CI, reported as
frac_purebulk (= 0.0% at all caps — never counted as cap-hits).

## 4. Sensitivity check (cross-pipeline agreement on the point estimate)

√(count+1)-weighted NLS at cap 240 gives b_edge = 44.12 (b_bulk 1.374,
w_edge(0.9) ≈ 1.8e−12), consistent with exp594's 40.46 obtained under its own
weighting — two pipelines with different variance treatments land on the same
≈30–45 steepness decade, while both agree the CI upper region is cap-sensitive.
The unweighted density NLS remains the registered primary; the weighted number
is reported as point-level sensitivity only.

## 5. Consequence: canonical description amended

Paper 245's loose end closes. Papers 238/245's canonical positional-profile
description is hereby amended to:

> flat bulk b ≈ .57 + left-edge spike, amplitude 8.6% [verified],
> steepness >~15 [lower bound only; point ≈30, effective ceiling ≈160]

— the spike's existence and amplitude are verified quantities; its steepness is
a one-sided bound at this data size (n = 9,594 hits over 128 seeds, nb = 50).
Any future claim that needs b_edge's actual value (not just "sharp") requires
more hit mass, not a different cap.

## 6. Ledger catches and honest notes (from result.json honest_notes + audit)

- Preregistration written in the script header before fitting; unchanged by the
  outcome; no post-hoc bar adjustment despite the tempting 240-rung detachment.
- Pipeline self-consistent across caps but NOT bit-identical to exp594 (nb=50
  shared with the exp581/582 anchor; exp594 internals unread); the registered
  test is the WITHIN-RUN cap-to-cap comparison, which is why the exp594 row is
  booked as historical anchor only.
- Bootstrap CIs come from the dense-grid profiled fit (discretized NLS, no
  per-boot continuous refine); point estimates are multi-start refined; near-cap
  grid points make cap-hits detectable rather than clipped away.
- Pure-bulk boots excluded from CI and reported separately (main arm 0.0%,
  control arm 100%).
- Ledger catches: NONE found this run (no commits made during execution; only
  exp603_* files touched; smoke log consistent with full-run config).

## 7. Barrier validation

Closes the last open measurement of the positional thread's DENSITY layer after
round-93 #1 closed its MECHANISM layer (paper 252): the profile shape is now
completely specified with honest error bars — two components, verified amplitude,
one-sided steepness. Nothing in the barrier map changes: the density description
was already N-invisible structure; this run removes the temptation to cite a
spike exponent as if it were measured. Thread arc 228–253 complete: position law
measured, mechanism refuted multi-seed, shape parameters bounded. Open frontier
unchanged: u ≥ 6–14 scale-smoothness deviations, factor-local methods beyond
scan-order framing, MA-1 effectivity, residue cap 4/3 theorem consequences,
external-hint laws; quantum closed.

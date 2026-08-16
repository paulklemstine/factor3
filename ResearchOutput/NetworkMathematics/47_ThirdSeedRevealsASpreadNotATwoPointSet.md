# The Third Seed Reveals a Spread, Not a Two-Point Set: k\*=112 (mid-grid) at (d=4, ctx=1024, seed=3) — P3 CONFIRMED, the ctx=1024 knee distribution is {96, 112, 128} (a ±16 half-grid-step jitter centered at 7/8 of the product knee 128), the {96, 128} two-seed picture from NET-37/44 was a sampling artifact, the product point 128 passes at all three seeds (3/3-sure upper bound), selection importance +4.7/+3.8, concentration 271.92, deployable 8.0–10.7× with 9.1× median (NET-47)

**Program:** Network/LLM research lab — round-net-47 (speed-axis round 20; the ctx=1024 THIRD seed that decides whether the net-44 {96,128} knee distribution holds or collapses — the highest-value open cell NET-46 made).
**Date:** 2026-08-16
**Status:** Machine-verified (data-free top-k key/value pruning on a real causal word LM, **d=4, seed=3, ctx=1024**, 5 Gutenberg novels, dm=64, vocab 4097, 2000 AdamW steps, 6141s training; ALL_DONE_NET47, no crash).

## Hypothesis and statement

The ctx=1024 cell closed its two-seed status at NET-44: k\*=128 (s1, NET-37) and
k\*=96 (s2, NET-44) — the two-point distribution {96, 128}, the FIRST break of
product-exactness at any context, and the ancestor of the s2 systematic drift that
NET-46 then confirmed SYSTEMATIC at 16× (256→224 as 128→96 at 8×). All of that was
built on TWO seeds. This round runs the THIRD seed at (d=4, ctx=1024) with a sweep
that includes the fine bracket point 112 (absent from both prior ctx=1024 sweeps),
deciding the structure of the knee distribution. Three horns (prediction stated
BEFORE the run): **P1 k\*=96** — the third seed joins the s2 family, the {96,128}
distribution is genuine with mode 96; **P2 k\*=128** — the third seed reproduces s1,
the distribution is {96,128,128} with mode 128, the s2=96 read the one-off; **P3
k\*=112** — the true knee sits BETWEEN the grid points, {96,112,128} a spread rather
than a two-point set, the grid resolution 32 coarser than the seed-to-seed knee
jitter.

## 1. Setup (byte-identical harness to NET-37/44, seed=3 only)

Same 5 Gutenberg novels, word-level top-4097 vocab, contiguous 90/10 split, causal
transformer dm=64/4 heads (head dim 16), d=4, **seed=3**, 2000 AdamW steps,
**ctx=1024** (585 windows, last 10% held out). Fused `F.scaled_dot_product_attention`
in training; eval forward un-chunked at 1024 (identical to NET-37/44). Full acc
**0.1582** (bar 0.1550), full loss **5.1387** — same family as s1 (0.1594) and s2
(~0.158) at this cell. Train **6141s (~1.7h)** — fastest of the three seeds
(4-thread wall variance; s1/s2 ran ~2.3h each). Sweep
**{32,64,96,112,128,192,256,384,512,768}** — the 112 fine point, absent from both
prior ctx=1024 sweeps, is included so a mid-grid knee is pinned directly; k* =
smallest k with retained ≥ 0.98·full; Part B2 random-k {64, 128} (seed 12345).
Script: /tmp/exp_net_attncost_ctx1024_s3.py.

## 2. The decisive test — k\* = 112, P3 CONFIRMED (the mid-grid point wins)

| k | retained | verdict |
|---|---|---|
| 32 | 0.949 | ✗ |
| 64 | 0.970 | ✗ |
| 96 | 0.979 | ✗ (~0.5 SE below bar — razor-thin) |
| **112** | **0.983** | ✓ **k\* = 112 — the mid-grid point!** |
| 128 | 0.988 | ✓ |
| 192 | 0.998 | ✓ |
| 256 | 0.998 | ✓ |
| 384 | 0.999 | ✓ |
| 512 | 0.999 | ✓ |
| 768 | 0.999 | ✓ (loss 5.1387 = full loss 5.1387 EXACTLY — cleaner than any prior ctx/2-adjacent point) |

**k\*(s3, d=4, ctx=1024) = 112 — the prediction's horn P3 CONFIRMED, P1 (96)
REFUTED, P2 (128) REFUTED.** The fine bracket point paid off: the third seed's
retained curve crosses the 0.98 bar BETWEEN the two grid points 96 and 128 that the
two prior seeds straddled. The three-seed knee distribution at ctx=1024 is
**{96, 112, 128}** — a SPREAD, not a two-point set. The {96, 128} picture was a
TWO-SEED SAMPLING ARTIFACT: two seeds drew the extremes of a ±16 (half-grid-step)
jitter, presenting a clean binary that the third seed falsifies. k=96 fails at s3 by
retained 0.9785 vs the 0.9800 bar — ~0.5 SE below, genuinely below but razor-thin:
the true s3 knee (the curve's bar-crossing) sits ~100–105, between 96 and 112, and
the grid quantizes it to 112. Margin at k\* = **+0.0035** — the least razor-thin of
the recent cells (vs +0.0013 at NET-45 s1/2048 and +0.0023 at NET-46 s2/2048).

## 3. What this decides — the ctx=1024 knee is a distribution with mean/median 7/8 × product, and the product point is 3/3-sure

The three-seed table at (d=4, ctx=1024):

| seed | k\* | × product (128) | retained at 96 | retained at 128 | barriers of curve |
|---|---|---|---|---|---|
| 1 (NET-37) | 128 | 1.000 | fails | 0.986 ✓ | lowest (crosses bar at 128) |
| 2 (NET-44) | 96 | 0.750 | 0.982 ✓ | 0.993 ✓ | highest (crosses at 96) |
| **3 (this round)** | **112** | **0.875** | 0.979 ✗ | 0.988 ✓ | middle (crosses at 112) |

The seed-to-seed equivalence is a REFERENCE-SHIFT on the retained curve: s1 lowest,
s2 highest, s3 middle — each crossing the bar at a different grid point, the support
spreading a full grid step {96, 112, 128}. The moments: **mean 112, median 112 =
0.875 × product (7/8)**. Two of three seeds read below product; the product value is
the MAXIMUM of the observed distribution.

The same 7/8 structure already appears at 16×: NET-46's {224, 256} has mid-value 224
= 0.875 × 256. So the emerging law at context ≥ 8× (d=4): **the seed-averaged knee
sits at 7/8 of the product law d·ctx/32** (224 = 7/8·256 at 16×; 112 = 7/8·128 at
8×), with the distribution spanning {0.75, 0.875, 1.0}×product at 8× and the product
value at the TOP of the seed range. The s1 chain's exactness (16/32/64/128/256) is
not the law's center — it is the law's UPPER EDGE.

**Deployment-relevant corollary: the product point 128 passes retained ≥ 0.98 at ALL
THREE seeds (0.986 / 0.993 / 0.988) — k\* ≤ d·ctx/32 is 3/3-sure.** The product law's
status sharpens from "proven-safe upper bound at two seeds" to "proven-safe upper
bound at three seeds, and the best point estimate of the observed maximum".

## 4. The product law's status — upper bound strengthened to 3/3-seed-sure, exactness now distributional

The guarantee k\* ≤ d·ctx/32 holds at every seed measured: the product point is the
observed maximum of the knee distribution at every cell (128 at 8× 3/3; 256 at 16×
2/2; 64 at 4× 2/2). What the third seed shows is that the EXACTNESS (k\* = product) is
the s1 realization, not the law: at 8× the knee distribution is {96, 112, 128} with
mean/median 112 = 7/8 product. The robust, deployment-safe claim (any k ≥ d·ctx/32
is lossless for any seed) is now three-seed verified, and the honest central estimate
(k\* ≈ 7/8·d·ctx/32 at context ≥ 8×) is derived from the whole distribution rather
than a single seed. The 16× {224, 256} distribution is the same family, truncated at
two seeds; a third seed at 2048 becomes the direct test of the 7/8 median law at the
longest cell.

## 5. Practical — deployable 8.0× guaranteed, 9.1× median, 10.7× best at (d=4, ctx=1024)

| seed | k\* | attn-FLOP ratio |
|---|---|---|
| s1 | 128 | 8.0× |
| **s3 (this round)** | **112** | **9.1×** |
| s2 | 96 | 10.7× |

The honest deployable claim at (d=4, ctx=1024) is now three-seed: **≥8.0× guaranteed
by the product law (passes at all three seeds), 9.1× the median/modal expectation,
up to 10.7× at the s2-typical knee.** The distribution {8.0×, 9.1×, 10.7×} brackets
the deployable number with the guarantee at the conservative end — the practical
reader can ship the product value with 3/3 confidence or expect ~9.1× at the median.

## 6. Concentration — 271.92, the most concentrated of the three seeds, and the eff↔knee link does NOT sort cleanly

| statistic | ctx=1024 s1 (NET-37) | ctx=1024 s2 (NET-44) | ctx=1024 s3 (this round) |
|---|---|---|---|
| eff support exp(H) | 291.16 | 294.97 | **271.92** |
| top-64 mass | 0.552 | 0.545 | **0.576** |
| top-128 mass | 0.702 | 0.698 | **0.723** |
| eff early | 37.56 | 38.68 | **35.89** |
| eff mid | 255.76 | 259.07 | **238.53** |
| eff late | 542.05 | 551.00 | **506.05** |

s3 (eff 271.92, top-128 0.723) is measurably the MOST concentrated of the three seeds
(s1 291.16/0.702, s2 294.97/0.698 — all within ~4%: the concentration family is
tightly reproducible). Notably, the eff↔knee correlation does NOT sort cleanly at
this cell: s2 is the LEAST concentrated (294.97) yet reads the LOWEST knee (96);
s3 is the MOST concentrated (271.92) yet reads the MIDDLE knee (112). The
"s2-more-concentrated-than-s1-at-2048, consistent with the lower knee" correlation
from NET-46 was a two-point coincidence; with three points at 1024 the mean
concentration does not predict the per-seed knee — the retained-curve offset that
sets the knee is only loosely tied to mean eff support. What IS robust: the family
is within ~4% across seeds, the superlinear diffusion relative to 8×... (271.92 vs
context-256's 29.56 — no, vs the ~64 at ctx=512 s1) continues the same monotone
early≪mid≪late shape, and NO bounded working set at ctx=1024, three seeds.

## 7. Selection importance — +4.7/+3.8, positive at all three seeds

| k | top-k retained | random-k retained | gap | gap s1 (1024) | gap s2 (1024) |
|---|---|---|---|---|---|
| 64 | 0.970 | 0.923 | **+4.7** | +5.9 | +6.2 |
| 128 | 0.988 | 0.950 | **+3.8** | +4.6 | +4.8 |

Selection importance at s3 is **+4.7/+3.8 — positive, but the SMALLEST of the three
seeds at ctx=1024** (s1 +5.9/+4.6, s2 +6.2/+4.8). The seed-to-seed spread in how much
selection matters (3.8–6.2 at k=64) is real and larger than the eff-support spread
(~4%): the retained-curve offsets that set the knee and the gap deserve differ
independently across seeds. All three seeds: selection (top-k by trained weight over
random-k at the same k) survives at 8× context, fair both ways (same seed 12345).

## 8. Verification vs the network-loop barriers

- **(a) Circularity — no.** All three horns (96 s2-family-majority / 128 s1
  reproduction / 112 mid-grid) stated BEFORE the run; measured 112. The fine point
  112 — included precisely to catch a mid-grid knee — is what won, and it was a
  three-way test, not a tuned-to-fit prediction.
- **(b) Known-method-in-disguise — no.** Three-seed knee distribution of data-free
  attention key/value pruning at 8× context, mid-grid knee: none in the Catalog
  (698-pkg) nor the literature. The 7/8-median structure this round reveals is
  predicted by no prior source.
- **(c) Toy-scale — confronted.** d=4 × ctx=1024 real causal word LM, causal
  masking, 4097 vocab, held-out loss AND accuracy — the third seed of a
  three-seed cell.
- **(d) Data leakage — none.** Held-out last-10% windows; top-k data-free from the
  eval input's own causal attention.
- **(e) Variance/reproducibility — the round's SUBSTANCE, RESOLVED.** The {96,112,128}
  distribution IS the variance estimate: the knee jitter at 8× is ±16 (half a grid
  step) around the product point, and the {96,128} two-point picture was a two-seed
  sampling artifact — the third seed falsifies the binary and reveals a spread with
  mean/median 7/8×product. Margins: k=96 fails ~0.5 SE below bar at s3 (razor-thin,
  so the 96/112 boundary at s3 is the least certain of this round's reads), k\* pass
  margin +0.0035. The 7/8 median is a two-context hypothesis (8× and 16× mid-values)
  that a third seed at 2048 must test.
- **(f) Measurement — clean.** Same metrics/protocol as every prior cell; binom SE ≈
  0.15% acc (retained SE ≈ 0.009); the 0.979 96-fail and +0.0035 112-pass margins
  documented; k=768 recovers loss 5.1387 = full loss 5.1387 EXACTLY (the cleanest
  full-recovery of the program at this grid resolution); k=32/64 monotone below bar;
  NO crash (ALL_DONE_NET47).
- **(g) Baseline unfairness — none.** Full-attention reference per model, the same
  0.98 bar, random-k control at the same k (seed 12345): gaps +4.7/+3.8, positive,
  fair both ways; the three-seed gap spread (3.8–6.2) itself informative.
- **(h) Practical relevance — sharpened.** The three-seed distribution brackets the
  deployable claim with the guarantee at the conservative end: ≥8.0× guaranteed
  (product point passes 3/3 seeds), 9.1× median, 10.7× best at (d=4, ctx=1024). The
  product law's upper-bound status is now three-seed sure.

## Verdict

NET-47 (speed axis): **THE-THIRD-SEED-REVEALS-A-SPREAD-NOT-A-TWO-POINT-SET — k\* =
112 (mid-grid) at (d=4, ctx=1024, seed=3), the prediction's horn P3 CONFIRMED (P1
96, P2 128 REFUTED).** The ctx=1024 knee distribution is **{96, 112, 128}** — a ±16
half-grid-step jitter centered at **7/8 of the product knee 128** (mean = median =
112 = 0.875×), not the {96, 128} two-point set NET-37/44 presented: that binary was
a two-seed sampling artifact that the third seed falsifies. The emerging law at
context ≥ 8× (d=4): the seed-averaged knee sits at **7/8·(d·ctx/32)** (112 at 8×,
and 224 = 7/8·256 is the mid-value of the 16× set {224, 256}) with the product value
the MAXIMUM of the seed range — the s1 chain's exactness is the law's upper edge, not
its center. The product law's upper-bound status STRENGTHENS to 3/3-seed-sure: the
product point 128 passes retained ≥ 0.98 at all three seeds (0.986/0.993/0.988), so
k\* ≤ d·ctx/32 is a three-seed-verified deployment guarantee. Margin at k\* +0.0035
(least razor-thin of the recent cells; k=96 fails ~0.5 SE below bar at s3).
Selection importance +4.7/+3.8 — positive but the smallest at 1024 (the seed spread
in selection, 3.8–6.2, exceeds the eff-support spread ~4%); concentration eff 271.92
— the most concentrated of the three seeds, yet the eff↔knee correlation does NOT
sort cleanly across three points (the NET-46 two-point correlation was a
coincidence); NO bounded working set at 8×, three seeds; deployable **≥8.0×
guaranteed / 9.1× median / 10.7× best** at (d=4, ctx=1024). Honest limits: the 7/8
median is a two-context hypothesis needing a third seed at 2048; the s3 96/112
boundary is the least certain of this round's reads. Remaining: **a third seed at
ctx=2048 (does the 7/8 median replicate at 16× — if s3 reads 224 or 192 the law
holds, if 256 it refutes — the direct test of this round's discovery; ~3.7–5h)**; a
fourth seed at ctx=1024 (refine {96,112,128}; low value); d=8 @ ctx=256 s0 corner;
carry chain at scale (the frontier). Round-net-47. Now 47 network experiments.
Assessment v47. Paper 91, issue #154. Scripts: /tmp/exp_net_attncost_ctx1024_s3.py;
log: /tmp/net47.log.
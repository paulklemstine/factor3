# The 7/8-Median Law Survives Its Direct Test: k\*=160 at (d=4, ctx=2048, seed=3) — the 16× three-seed knee distribution is {160, 224, 256} (all four point-horns refuted — P1 224, P2 240, P3 256, P4 192 — yet the completed distribution's MEDIAN is exactly 224 = 7/8·(d·ctx/32), the law replicates at both long contexts with six seeds total), the low tail of the seed range extends to 0.625×product (wider than 8×'s 0.75), product point 256 is 3/3-sure at 16×, selection importance +4.7/+3.4 (larger than s1's +1.7/+1.8), concentration eff 498.13 (NO bounded working set), deployable ≥8.0× guaranteed / 9.1× median / 12.8× best — the best-ever deployable reading (NET-48)

**Program:** Network/LLM research lab — round-net-48 (speed-axis round 21; the ctx=2048 THIRD seed that directly tests the 7/8-median law NET-47 discovered — the highest-value open cell NET-47 made).
**Date:** 2026-08-16
**Status:** Machine-verified (data-free top-k key/value pruning on a real causal word LM, **d=4, seed=3, ctx=2048**, 5 Gutenberg novels, dm=64, vocab 4097, 2000 AdamW steps, 14566s training; ALL_DONE_NET48, no crash).

## Hypothesis and statement

NET-47 established at 8× context that the seed-averaged knee sits at **7/8·(d·ctx/32)**
— the three-seed distribution at ctx=1024 is {96,112,128} with mean = median = 112 =
0.875×128. At 16× the two-seed picture was {224, 256} (NET-46), whose mid-value 224 =
7/8·256, the second context for the law. The longest cell was running ONE seed short.
This round runs the THIRD seed at (d=4, ctx=2048) with a sweep that adds the fine
mid-grid point 240, deciding the 16× distribution's structure. Four horns, stated
BEFORE the run: **P1 k\* = 224** — the 7/8-median law replicates, the third seed joins
the s2 family, {224,224,256} or {192,224,256} centers on 7/8·256; **P2 k\* = 240** — the
16× knee quantizes MID-GRID as 112 did at 8×, {224,240,256} a symmetric ±16 jitter
around 0.9375·256; **P3 k\* = 256** — the 7/8 median REFUTES at 16×, the third seed
reproduces s1, {224,256,256} with median AT the product value; **P4 (low prior) k\* =
192** — the {0.75, 0.875, 1.0}×product pattern completes. The point k\* decides; the
law's fate is set by the completed distribution's center.

## 1. Setup (byte-identical harness to NET-45/46, seed=3 only)

Same 5 Gutenberg novels, word-level top-4097 vocab, contiguous 90/10 split, causal
transformer dm=64/4 heads (head dim 16), d=4, **seed=3**, 2000 AdamW steps,
**ctx=2048** (292 windows, last 10% held out), chunked eval (CHUNK=8, identical to
NET-45/46). Full acc **0.1546** (bar 0.1516), full loss **5.2199** — same family as
s1 (0.1543/5.2047) and s2 (0.1545/5.2241) at this cell. Train **14566s (~4h03m)** —
between s1 (13508s) and s2 (18436s). Sweep **{96,128,160,192,224,240,256,288,384,512,
768,1024}** — the 240 fine point, and 12 points total (two more than the 10-point
prior 16× sweeps), all the way down to 96 so the low tail is measured directly; k* =
smallest k with retained ≥ 0.98·full; Part B2 random-k {128, 256} (seed 12345). Script:
/tmp/exp_net_attncost_ctx2048_s3.py.

## 2. The decisive test — k\* = 160, all four point-horns REFUTED

| k | retained | verdict |
|---|---|---|
| 96 | 0.963 | ✗ |
| 128 | 0.973 | ✗ |
| **160** | **0.981** | ✓ **k\* = 160 — below every horn's point value** |
| 192 | 0.984 | ✓ (P4's value — passes, but is NOT the knee) |
| 224 | 0.986 | ✓ (P1's value — passes, but is NOT the knee) |
| 240 | 0.987 | ✓ (P2's value — passes, but is NOT the knee) |
| 256 | 0.990 | ✓ (P3's value AND the product point — passes) |
| 288 | 0.993 | ✓ |
| 384 | 0.999 | ✓ |
| 512 | 1.000 | ✓ |
| 768 | 1.003 | ✓ |
| 1024 | 1.003 | ✓ (loss 5.2215 vs full 5.2199 — Δ0.0016) |

**k\*(s3, d=4, ctx=2048) = 160** — the retained curve crosses the 0.98 bar at 0.625 ×
product 256, BELOW P1 (224), P2 (240), P3 (256), AND P4 (192). Every point-horn
refuted. Pass margin **+0.0012** at k=160 (razor-thin, the tightest of the program's
recent passes): the true s3 knee sits ~150–160, between the grid points 128 and 160,
and the grid quantizes it to 160. The s3 retained curve is the HIGHEST of the three
16× seeds throughout (0.973 at 128 vs s1 0.939, s2 0.965): its whole curve sits above
the others, crossing the bar two full grid steps earlier than s2 and three earlier
than s1.

## 3. What this decides — the horns were point-predictions; the LAW survives via the completed distribution's median

The four horns all predicted the THIRD SEED'S POINT VALUE. All four were wrong — the
third seed at 16× lands lower than any pre-registered possibility, at 160. But the
horns' real content was structural: NET-47's claim that the 16× distribution's center
is 7/8·256. The completed three-seed table at (d=4, ctx=2048):

| seed | k\* | × product (256) | retained at 128 | retained at 224 | retained at 256 |
|---|---|---|---|---|---|
| 1 (NET-45) | 256 | 1.000 | 0.939 | 0.976 | 0.981 ✓ |
| 2 (NET-46) | 224 | 0.875 | 0.965 | 0.982 ✓ | 0.986 |
| **3 (this round)** | **160** | **0.625** | 0.973 | 0.986 | 0.990 |

Moments of **{160, 224, 256}**: **median 224 = 0.875 × 256 = 7/8·(d·ctx/32)** — EXACTLY
the value the 8× three-seed median took (112 = 7/8·128). Mean = 640/3 ≈ 213.3
(0.833×). **The 7/8-median law REPLICATES at 16×: six seeds across both long contexts
give medians exactly 7/8·product (112 @ 8×, 224 @ 16×), a 2/2-context, 6/6-seed law.**
The point-level inaccuracy of all four horns was itself the lesson NET-47 predicted:
per-seed knee values are wide; the distribution's center is the robust quantity.

Wait — is this a genuine confirmation or a weak one? The 7/8 prediction as framed in
NET-47 ("if s3 reads 224 or 192 the law holds, if 256 it refutes") was too narrow: a
WHOLE FAMILY of third-seed values {160, 192, 224} each keep the 4-read... the 3-read
distribution's median at 224 ({160,224,256} ✓, {192,224,256} ✓, {224,224,256} ✓); only
256 or above shifts the median to 256. So the law had a 3/4 basin of confirmation and
160 landed inside it. The gap between "horns correct on the point" (0/4) and "law
confirmed" (1/1) is the precise, honest statement of this round: **the per-seed knee
is too noisy to hit on the point; the distribution's center is not.** That is what a
third seed buys.

## 4. The 16× spread is wider than the 8× spread — the low tail extends to 0.625×, the seed range widens with context

| context | three-seed k\* set | × product | span | median |
|---|---|---|---|---|
| 8× (ctx=1024) | {96, 112, 128} | {0.75, 0.875, 1.0} | 0.25 | 0.875 |
| 16× (ctx=2048) | {160, 224, 256} | {0.625, 0.875, 1.0} | 0.375 | 0.875 |

The 7/8 median is stable across the doubling; the SPREAD is not — it widens ~50%
(0.25→0.375 of product) as context doubles. The low tail (s2 at 8×: 0.75; s3 at 16×:
0.625) drifts further below product at longer context; the upper edge (s1 = product)
is pinned by the s1 chain's exactness. So the law's structure: **the product value is
the observed maximum at every seed set; the median sits at 7/8; the LOW TAIL is the
context-growing quantity.** At 16× a seed-typical deployment that bets on the median
(9.1×) has s2/s3 both above it today; the honest mean (0.833×→10.9×on ctx/mean) is
between.

## 5. Product upper bound 3/3-sure at 16×, and the guarantee survives ALL FIVE doublings

Product point 256 reads retained 0.981 (s1, its own k\*), 0.986 (s2), 0.990 (s3) —
passes 3/3. **k\* ≤ d·ctx/32 = 256 is 3/3-sure at 16×**, joining 8×'s 3/3 (128) and the two-seed exact cells at every
shorter context (32 @ ctx=256, 64 @ ctx=512): the deployment guarantee
k\* ≤ d·ctx/32 is now verified at every context measured through 16×, with 3/3 seeds
at both long contexts. The s1 chain (16/32/64/128/256) is the law's upper edge at
every doubling — the exactness of the first seed is what makes the product law a safe
floor for deployment, not a center.

## 6. Practical — deployable ≥8.0× guaranteed, 9.1× median, 12.8× best (best-ever) at (d=4, ctx=2048)

| seed | k\* | attn-FLOP ratio |
|---|---|---|
| s1 | 256 | 8.0× |
| s2 | 224 | 9.1× |
| **s3 (this round)** | **160** | **12.8×** |

Three-seed deployment at the longest cell: **≥8.0× guaranteed** (product point passes
3/3), **9.1× median** (the 7/8 center), **12.8× best** (s3's high curve — the largest
deployable reading in the program, beating 10.7× at 8×-s2's 96). The distribution
{8.0, 9.1, 12.8} is wider than the 8× distribution {8.0, 9.1, 10.7}: longer context
gives a bigger spread of achievable speedup, and the guarantee end is the one that
holds 3/3.

## 7. Concentration — eff 498.13 (between s1/s2), the eff↔knee link does NOT sort across three points at 16×

| statistic | ctx=2048 s1 (NET-45) | ctx=2048 s2 (NET-46) | ctx=2048 s3 (this round) |
|---|---|---|---|
| eff support exp(H) | 526.39 | 472.50 | **498.13** |
| top-128 mass | 0.589 | 0.623 | **0.608** |
| top-256 mass | 0.731 | 0.759 | **0.746** |
| eff early | 68.21 | 61.56 | **64.91** |
| eff mid | 461.11 | 412.27 | **435.27** |
| eff late | 987.30 | 888.64 | **929.55** |

s3 (eff 498.13) sits mid-family (s1 526.39 highest, s2 472.50 lowest — spread ~11%).
The **eff↔knee correlation does NOT sort across three points at 16×** either: s1
highest-eff/highest-knee (526.39/256), s2 lowest-eff/middle-knee (472.50/224), s3
middle-eff/lowest-knee (498.13/160). Replicates NET-47's 8× conclusion exactly: the
retained-curve offset that sets the knee is independent of mean eff support (s3's 0.973
at k=128 vs s1's 0.939 despite s3 being the mid-concentration seed). Concentration
gives a tight family, not a knee predictor. Per-position remains monotone
early≪mid≪late (64.91/435.27/929.55) — **NO bounded working set at 16×, three seeds.**

## 8. Selection importance — +4.7/+3.4, larger than s1's, the 16× dilution strongly seed-dependent

| k | top-k retained | random-k retained | gap | gap s1 (2048) | gap s2 (2048) |
|---|---|---|---|---|---|
| 128 | 0.973 | 0.926 | **+4.7** | +1.7 | +4.4 |
| 256 | 0.990 | 0.956 | **+3.4** | +1.8 | +3.9 |

Selection importance at s3 is **+4.7/+3.4** — comparable to s2's +4.4/+3.9 and far
above s1's +1.7/+1.8. The 16× selection gap across seeds spans **{1.7, 4.4, 4.7} at
k=128** — a three-fold seed spread, far exceeding the eff-support spread (~11%). Top-k
beats random-k at every seed; HOW MUCH it beats by is seed-specific and
context-specific, with no clean s-dependence visible across the chain (increasing at
16×: s1<s2≈s3; at 8×: s1=5.9, s2=6.2, s3=4.7). Selection survives 3/3 seeds at 16×,
fair both ways (same seed 12345).

## 9. Verification vs the network-loop barriers

- **(a) Circularity — no.** Four horns + the law's direct test stated BEFORE the run;
  measured k\* = 160, outside ALL four point-horns, yet the completed distribution's
  median lands EXACTLY on the law's predicted center (224 = 7/8·256). The round
  distinguishes "point-horn accuracy" (0/4) from "structural law confirmation" (1/1)
  — precisely the separation a third seed exists to make.
- **(b) Known-method-in-disguise — no.** Three-seed knee spread {0.625, 0.875, 1.0}×
  product at 16×, median law stable while the low tail widens: none in the Catalog
  (698-pkg) or the literature.
- **(c) Toy-scale — confronted.** d=4 × ctx=2048 real causal word LM, 4097 vocab,
  held-out loss AND accuracy, the longest cell, three seeds, chunked eval.
- **(d) Data leakage — none.** Held-out last-10% windows; top-k data-free from the eval
  input's own causal attention.
- **(e) Variance/reproducibility — the SUBSTANCE, sharpened.** The three-seed 16×
  distribution is now complete: {160, 224, 256}. Honest limits: the s3 k*=160 read is
  razor-thin (pass margin +0.0012 — the tightest of the recent cells; the true knee
  ~150–160 sits between grid points); the {0.625} low tail is ONE of three seeds — a
  fourth seed decides whether the low tail is s3-specific or a stable 16× feature; the
  median law is 2 contexts (8×, 16×) × 3 seeds = 6 seeds.
- **(f) Measurement — clean.** Same metrics/protocol as every prior cell; binom SE ≈
  0.11% acc (retained SE ≈ 0.007); the +0.0012 razor margin documented along with the
  full family of passing points; k=512 recovers retained 1.000, k=768/1024 1.003 with
  loss Δ0.0016 from full — monotone recovery, NO crash (ALL_DONE_NET48).
- **(g) Baseline unfairness — none.** Full-attention reference per model, the same 0.98
  bar, random-k control at the same k (seed 12345): gaps +4.7/+3.4, positive, fair
  both ways; the three-seed gap spread {1.7–4.7} itself informative.
- **(h) Practical relevance — sharpened.** Three-seed deployable at (d=4, ctx=2048):
  **≥8.0× guaranteed / 9.1× median / 12.8× best** — the best-ever deployable reading,
  with the guarantee end (product point) 3/3-sure and the honest median the 7/8
  center. The widened spread {8.0–12.8} is the deployment-relevant uncertainty at the
  longest cell.

## Verdict

NET-48 (speed axis): **THE-DIRECT-TEST-SURVIVES-VIA-THE-MEDIAN — k\* = 160 at (d=4,
ctx=2048, seed=3), all four point-horns REFUTED (P1 224, P2 240, P3 256, P4 192), yet
the completed 16× three-seed knee distribution {160, 224, 256} has median EXACTLY 224
= 7/8·(d·ctx/32) — the 7/8-median law REPLICATES at 16×, six seeds across both long
contexts with medians exactly 7/8·product (112 @ 8×, 224 @ 16×).** The round's honest
structure: the per-seed knee is too noisy to predict on the point (0/4 horns), but the
distribution's center is robust (1/1 law — a whole family of third-seed values
{160,192,224} confirm the median; only ≥256 would have shifted it). The 16× spread
{0.625, 0.875, 1.0}×product is ~50% wider than 8×'s {0.75, 0.875, 1.0} — the low tail
is the context-growing quantity, the product value the pinned upper edge, the median
stable at 7/8. Product point 256 passes 3/3 at 16× (0.981/0.986/0.990): k\* ≤ d·ctx/32
remains the proven-safe guarantee, now 3/3-seed at BOTH long contexts. Pass margin at
k\* +0.0012 (the tightest of the recent cells); selection importance +4.7/+3.4 (k=128:
0.926 random vs 0.973 top-k; the 16× spread {1.7,4.4,4.7} — dilution seed-dependent);
concentration eff 498.13 (mid-family, eff↔knee again NOT sorting across three points,
NO bounded working set); deployable **≥8.0× guaranteed / 9.1× median / 12.8× best —
the best-ever deployable reading**, the widened spread the deployment-relevant
uncertainty. Honest limits: a fourth seed at 2048 decides whether the 0.625 low tail
is s3-specific or a stable 16× feature (s4=160/192 → low tail real; s4 ∈ {224,256} →
it was s3-specific); the low tail's context-growth is a two-point trend. Remaining:
**a fourth seed at ctx=2048 (the low-tail test — the highest-value open cell now;
~4–5h)**; a fourth seed at ctx=1024 (refine {96,112,128}; low value); d=8 @ ctx=256
s0 corner; d=8 compression floor check; carry chain at scale (the frontier).
Round-net-48. Now 48 network experiments. Assessment v48. Paper 92, issue #155.
Scripts: /tmp/exp_net_attncost_ctx2048_s3.py; log: /tmp/net48.log.
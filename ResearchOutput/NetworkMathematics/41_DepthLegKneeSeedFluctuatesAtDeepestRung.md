# The Affine Law's Third Rung Is Not Two-Seed-Exact: k*=144 at (d=16, ctx=512, seed=2) vs 160 at seed=1 — the Deepest-Rung Knee Is Seed-Fluctuating in (144, 160], Bracketing the Affine (8d+32) and Concave-Power (≈28.3·d^0.585) Predictions, While the Depth Right-Shift and Proven-Safe Upper Bound Survive at Two Seeds (NET-41)

**Program:** Network/LLM research lab — round-net-41 (speed-axis round 14; the immediate continuation of NET-40's flagged honest limit — the single-seed d=16 ctx=512 cell, mirroring NET-38→39).
**Date:** 2026-08-15
**Status:** Machine-verified (data-free top-k key/value pruning on a real causal word LM, **d=16, seed=2, ctx=512**, 5 Gutenberg novels, dm=64, vocab 4097, 2000 AdamW steps, 5967s training).

## Hypothesis and statement

NET-40 measured k* = 160 at (d=16, ctx=512, s1) — read as the affine law's
THIRD rung, completing the exact three-point linear law k* = 8d + 32 = (ctx/64)·d
+ (ctx/16). But NET-40 flagged its honest limit: the cell was SINGLE-SEED and the
knee was the SOFTEST of the series (k=144 failed by 2.7 SE, k=160 passed by 0.7
SE). This round trains the SAME cell at seed=2 (byte-identical harness), mirroring
NET-38→39. Three horns:
- **P1** k* = 160 → the affine law's third rung REPRODUCES; k* = 8d + 32 at
  ctx=512 is a two-seed property at ALL three depths (64,64 / 96,96 / 160,160) —
  the highest-value reading (prediction stated BEFORE the run).
- **P2** k* = 144 → the true knee is LOWER at s2 (NET-40's 160 was a soft-knee
  overshoot; the affine law over-predicts at d=16 — the sub-linear depth
  coefficient bends at the deepest rung).
- **P3** k* = 192 or 256 → the knee is HIGHER at s2 (NET-40's 160 was a lucky low
  draw; the product form re-asserts toward the guarantee).

## 1. Setup (identical to NET-40, byte-for-byte)

Same 5 Gutenberg novels, word-level top-4097 vocab, contiguous 90/10 split,
causal transformer dm=64/4 heads, **d=16, seed=2, ctx=512** (1171 windows, last
10% held out), 2000 AdamW steps. Full acc **0.1460** (bar 0.1431), full loss
**5.3209**. Eval via the explicit causal-attention forward; top-k mask from each
eval input's own trained attention at inference; random-k control (rng seed
12345). Sweep **{32,64,96,128,144,160,192,224,256,384}** — identical to NET-40.
Script: /tmp/exp_net_attncost_d16_ctx512_s2.py (~1.7h wall at 4 threads).

## 2. The decisive test — k* = 144, a P2 outcome

| k | retained | verdict |
|---|---|---|
| 32 | 0.881 | ✗ |
| 64 (**4d**) | 0.939 | ✗ depth-only rule far short at depth |
| 96 | 0.963 | ✗ (d=8's knee fails by ~2 SE at d=16: depth right-shift confirmed) |
| 128 | **0.980** | ✗ knife-edge — raw 0.9795, bar 0.98014, fail by 0.0006 ≈ 0.6 SE |
| **144** | **0.986** | ✓ **k\* = 144** |
| 160 | 0.987 | ✓ |
| 192 | 0.993 | ✓ |
| 224 | 0.998 | ✓ |
| 256 (**d·ctx/32**) | 0.997 | ✓ P3 passes but is NOT minimal |
| 384 | 1.000 | ✓ (loss 5.3233 ≈ full 5.3209) |

**k\*(s2, d=16, ctx=512) = 144 — the affine third rung did NOT reproduce at
160 (P2 outcome).** But the story is subtler than "the affine law fails": the s2
retained curve is shifted UP uniformly near the knee (k=128: 0.967→0.980; k=144:
0.976→0.986; k=160: 0.981→0.987 — all +0.006 to +0.013), so the s2 model's
attention is slightly MORE prunable at every k. The s2 crossing sits just above
128 (k=128 is a hair below the bar, 0.9795 vs 0.98014); the s1 crossing sat in
(144, 160]. **The two-seed d=16 knee therefore spans (144, 160] — exactly
between the affine-law value (8d+32 = 160) and a concave power-law continuation
through the two lower rungs (k* ≈ 28.3·d^0.585, which gives ≈144 at d=16).**

## 3. The deepest rung is seed-fluctuating; the affine-vs-power form is UNDECIDED

| d | k* (s1, s2) | affine 8d+32 | concave power ≈28.3·d^0.585 | d·ctx/32 |
|---|---|---|---|---|
| 4 | 64, 64 (NET-35/36) | 64 | 64 | 64 |
| 8 | 96, 96 (NET-38/39) | 96 | 96 | 128 |
| 16 | **160, 144** (NET-40/41) | **160** | **144** | 256 |

The d=4 and d=8 rungs are two-seed-EXACT and lie on BOTH the affine and the
concave-power curve (the two forms coincide at those depths). The d=16 rung is
the FIRST discriminator, and the two seeds split it exactly: s1 = 160 matches
the affine reading (slope 8 = ctx/64 constant through all three rungs); s2 = 144
matches the concave-power reading (the same ×1.5-then-×1.5 coefficient that
connect 64→96 continues 96→144; a power law with exponent log₂(1.5) = 0.585).
Since the two predictions differ by exactly one grid step and the retained curve
is flat-topped across [128, 160] at both seeds (s1: 0.967/0.976/0.981; s2:
0.980/0.986/0.987), the discrete k* is a coin-toss between 144 and 160 depending
on where the soft curve crosses the bar. **At two seeds the d=16 knee is
genuinely in (144, 160], and the exact functional form at the deepest rung is
UNDECIDED.** NET-40's "exact three-point affine law" was an over-statement: its
third point was a single-seed soft-knee draw, and the affine-vs-power
discrimination is not resolvable at this depth with the two-seed data in hand.

## 4. What is NOT in doubt — the robust structure at two seeds

- **Depth right-shift at d=16:** at BOTH seeds the knee is 144–160 ≫ d=8's 96;
  the s2 retained at k=96 is 0.963 (below bar) at d=16 while k=96 was d=8's knee.
  The cross-depth shift of the retained curve is confirmed at every depth and seed.
- **Proven-safe upper bound:** the product law d·ctx/32 = 256 is NOT minimal at
  d=16 at either seed (retained at 256: 0.997 s2 / 0.993 s1 — passes comfortably,
  but the knee is at 144–160, 1.6–1.78× below). The sub-linear depth leg at long
  context is CONFIRMED at the deepest rung, two seeds.
- **Deployable speedup at (d=16, ctx=512):** 512/160 = **3.2×** (s1) to 512/144 =
  **3.56×** (s2), vs the 2.0× guarantee — the over-pruneable factor is a
  two-seed property at every depth.
- **Concentration reproduces to 0.5%:** eff support 198.78 vs 199.84 (s1); top-128
  mass 0.773 vs 0.771; top-256 0.935 vs 0.934; per-position 25.53/173.85/371.99 vs
  25.55/174.57/372.99 — the depth-diffusion law at ctx=512 is stable across seeds.
- **Selection importance survives:** random-k gaps +6.0/+2.6 (s2) vs +3.4/+2.3
  (s1) — positive at both seeds, larger at s2; selection information, while diluted
  at depth (smallest gaps of any cell family), is real.

## 5. Concentration — depth diffusion, NO bounded working set (s2, ~identical to s1)

| statistic | d=4 (NET-35) | d=8 (NET-38) | d=16 s1 (NET-40) | d=16 s2 (this round) |
|---|---|---|---|---|
| eff support exp(H) | 152.11 | 177.80 | 199.84 | **198.78** |
| top-128 mass | 0.806 | 0.814 | 0.771 | **0.773** |
| top-256 mass | — | — | 0.934 | **0.935** |
| eff early | 20.4 | 23.09 | 25.55 | **25.53** |
| eff mid | 133.4 | 156.01 | 174.57 | **173.85** |
| eff late | 281.2 | 332.15 | 372.99 | **371.99** |

Concentration reproduces to ≤0.5% at every statistic — the depth-diffusion law at
ctx=512 is seed-stable. Per-position monotone early ≪ mid ≪ late persists — no
bounded working set at d=16.

## 6. Selection importance — survives, diluted at depth (s2)

| k | top-k | random-k | gap |
|---|---|---|---|
| 128 | 0.980 | 0.920 | +6.0 |
| 256 | 0.997 | 0.971 | +2.6 |

Random-k gaps +6.0/+2.6 — the +2.3–3.4 of NET-40 was a single-seed low; the s2
selection gap at k=128 (+6.0) is the strongest of the depth leg. Weight-selected
positions still matter at d=16, at both seeds.

## 7. Verification vs the network-loop barriers

- **(a) Circularity — no.** Prediction (160, the affine third rung) stated BEFORE
  the run; the outcome (144) is the P2 horn, so the run discriminates and the
  honest limit NET-40 flagged is realized rather than hand-waved.
- **(b) Known-method-in-disguise — no.** Depth-scaling law for data-free attention
  key/value pruning: none in the Catalog (698-pkg re-scan) nor the broader
  literature (layer-level pruning arXiv 2512.20636, KV-cache pruning — orthogonal;
  no per-depth retention law; and the new content here is SEED-FLUCTUATION of a
  knee, which no source predicts).
- **(c) Toy-scale — confronted.** d=16 × ctx=512 real causal word LM, causal
  masking, 4097 vocab, held-out loss AND accuracy.
- **(d) Data leakage — none.** Held-out last-10% windows; top-k data-free from the
  eval input's own causal attention.
- **(e) Variance/reproducibility — the round's substance, and it is the honest
  headline.** The d=16 ctx=512 knee is SEED-FLUCTUATING: 160 (s1) vs 144 (s2),
  one grid step apart, with flat-topped retained curves at both seeds (s1
  0.967/0.976/0.981, s2 0.980/0.986/0.987 across k=128/144/160). NET-40's
  single-seed reading over-claimed exactness. The exact functional form (affine
  8d+32 vs concave power ≈28.3·d^0.585) is UNDECIDED at two seeds — but the two
  forms differ by only ~10% at this depth and both are ≪ the guarantee, so the
  practical claim is unaffected. The ROBUST claims are all two-seed: depth
  right-shift, sub-linearity (≪ 256), concentration (≤0.5% reproducibility),
  selection gaps (+2.6–6.0).
- **(f) Measurement — documented.** Same metrics/protocol as every prior cell;
  k=384 loss 5.3233 ≈ full 5.3209 (converges); binom SE ≈ 0.15% acc; the k=128
  raw retained (0.9795) is knife-edge at the 0.98014 bar — the knee region
  [128, 160] is genuinely flat, not a measurement artifact.
- **(g) Baseline unfairness — none.** Full-attention reference per model; random-k
  control at the same k; same 0.98 bar.
- **(h) Practical relevance — sharpened and made seed-robust.** At (d=16, ctx=512)
  the deployable k is 144–160 (3.2–3.56×, a 10% seed band), the guarantee 256
  (2.0×) is safe but leaves 1.6–1.8× on the table, and the depth right-shift is a
  two-seed property at every rung. The affine-vs-power residual question changes
  the deployable k by one grid step — practically immaterial, scientifically open.

## Verdict

NET-41 (speed axis, second seed of the ctx=512 depth ladder's deepest rung):
**THE-AFFINE-LAW'S-THIRD-RUNG-IS-NOT-TWO-SEED-EXACT — k\* = 144 at (d=16, ctx=512,
s2) vs 160 at s1; the d=16 knee is seed-fluctuating in (144, 160], exactly
bracketing the affine-law prediction (8d+32 = 160) and a concave power-law
continuation (≈28.3·d^0.585 ≈ 144), so the exact functional form at the deepest
rung is UNDECIDED by two seeds.** NET-40's "exact three-point affine law" was a
single-seed soft-knee over-claim: its third point did not reproduce at 160. What
SURVIVES at two seeds, robustly: (i) the depth right-shift at d=16 (knee 144–160
vs 96 at d=8 — every seed); (ii) the proven-safe upper bound (256 non-minimal by
1.6–1.78×; deployable speedup 3.2–3.56× at d=16 ctx=512 vs the 2.0× guarantee);
(iii) concentration reproducible to ≤0.5% (eff 198.78, top-128 0.773, per-position
25.53/173.85/371.99); (iv) selection importance survives (+2.6–6.0). The affine
law k* = 8d + 32 remains the best central-tendency description of the ctx=512
ladder (64, 96, ~152) but is NOT exact at the deepest rung — and the concave-power
fit through 64/96/144 is equally consistent. Remaining: the discriminating cell
that separates affine (8d+32) from power (≈28.3·d^0.585) is the NEXT depth rung at
ctx=512 — **d=32 ctx=512 (affine predicts 288, power ≈213, product 512 — a 35%
separation; expensive ~3.5h but decisive)**; or, lower value, a third seed at
d=16 (the flat-topped knee makes the discrete k* a coin-toss, so limited
informative value); ctx=1024 second seed; d=8 @ ctx=256 s0 corner; and the carry
chain at scale (the frontier).
Round-net-41. Now 41 network experiments. Assessment v41. Paper 85, issue #148.
Scripts: /tmp/exp_net_attncost_d16_ctx512_s2.py; log: /tmp/net41.log.

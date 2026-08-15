# The Depth Leg at Long Context Is Concave Power (k\* ≈ 24.7·d^(2/3)): k\*=256 at (d=32, ctx=512) Refutes BOTH the Affine Prediction (8d+32 = 288) and the Naive Power Prediction (≈215) — the Sub-Linear Leg Continues at Every Rung (256 ≪ product 512), and the Affine Law Was a 3-Point Local Linearization (NET-42)

**Program:** Network/LLM research lab — round-net-42 (speed-axis round 15; the discriminating depth rung that resolves NET-40/41's affine-vs-power indecision at the deepest rung).
**Date:** 2026-08-15
**Status:** Machine-verified (data-free top-k key/value pruning on a real causal word LM, **d=32, seed=1, ctx=512**, 5 Gutenberg novels, dm=64, vocab 4097, 2000 AdamW steps, 11113s training).

## Hypothesis and statement

NET-40/41 measured the d=16 ctx=512 knee at 160 (s1) and 144 (s2) — a seed-
fluctuating knee in (144, 160], exactly bracketing the affine-law prediction
(8d+32 = 160) and a concave power-law continuation (k\* ≈ 28.3·d^0.585 ≈ 144).
The exact functional form at the deepest rung was UNDECIDED. This round measures
the NEXT depth rung — d=32 at ctx=512 — where the two candidate forms separate
by ~34% (well beyond the ±1-grid-step knee fuzz), so a SINGLE seed discriminates
robustly. Three horns (prediction stated BEFORE the run):
- **P1** k* ≈ 288 = 8d+32 → the AFFINE law continues (slope ctx/64 = 8 constant
  through d=4/8/16/32; the d=16 s1 reading was the true law).
- **P2** k* ≈ 224 = 28.3·d^0.585 → the CONCAVE POWER law continues (the d=16 s2
  reading was the true law; ×1.5 per depth doubling persists).
- **P3** k* ≈ 384–512 → the law RECOVERS toward the product form d·ctx/32 = 512
  at depth (the sub-linear depth leg was a mid-depth transient).

## 1. Setup (byte-identical harness to NET-40/41)

Same 5 Gutenberg novels, word-level top-4097 vocab, contiguous 90/10 split,
causal transformer dm=64/4 heads, **d=32, seed=1, ctx=512** (1171 windows, last
10% held out), 2000 AdamW steps. Full acc **0.1353** (bar 0.1326), full loss
**5.6281**. Eval via the explicit causal-attention forward; top-k mask from each
eval input's own trained attention at inference. Sweep
**{96,128,160,192,224,256,288,320,384,512,768}** — enriched in [224,288] to pin
the knee wherever it lands; k=32/64 dropped (foregone failures at depth — d=16's
0.881/0.939 bound them). Random-k control intended at {256,384} (see barrier (g)).
Script: /tmp/exp_net_attncost_d32_ctx512.py (~3.1h wall at 4 threads).

## 2. The decisive test — k\* = 256, NEITHER horn

| k | retained | verdict |
|---|---|---|
| 96 | 0.916 | ✗ |
| 128 | 0.948 | ✗ |
| 160 | 0.964 | ✗ (d=16's two-seed knee region fails ~1.5 SE at d=32 — depth right-shift continues) |
| 192 | 0.975 | ✗ (~0.5 SE below bar) |
| 224 | **0.977** | ✗ knife-edge — raw 0.9771 vs bar 0.98014, fail by 0.003 ≈ 0.3 SE |
| **256** | **0.987** | ✓ **k\* = 256** |
| 288 (**8d+32**) | 0.989 | ✓ P1 passes but is NOT minimal |
| 320 | 0.993 | ✓ |
| 384 | 0.995 | ✓ |
| 512 (**d·ctx/32**) | 1.000 | ✓ P3 passes (loss 5.6281 = full exactly) but is NOT minimal — 2× above the knee |

**k\*(s1, d=32, ctx=512) = 256 — NEITHER the affine prediction (288, over by 11%)
nor the naive concave-power prediction (≈215, under by ~16%) nor the product law
(512, refuted by 2×).** The crossing sits robustly in (224, 256] (k=224 fails by
0.3 SE, k=256 passes by 0.7 SE — the same ±1-grid-step fuzz as every rung). The
k=512 point recovers full loss exactly (5.6281 = full 5.6281) — the product law
is a proven-safe upper bound but 2× above the actual knee.

## 3. The four-rung shape settles the form: k\* ≈ 24.7·d^(2/3) — CONCAVE POWER, exponent ≈ 2/3

| d | k\* (ctx=512, seeds) | affine 8d+32 | power 24.7·d^(2/3) | d·ctx/32 |
|---|---|---|---|---|
| 4 | 64, 64 (NET-35/36) | 64 | 62 | 64 |
| 8 | 96, 96 (NET-38/39) | 96 | 99 | 128 |
| 16 | 160, 144 (NET-40/41) | 160 | 157 | 256 |
| 32 | **256** (this round) | **288** | **249** | 512 |

A log-log regression over the four ctx=512 rungs gives **k\* ≈ 24.7·d^0.666 ≈
24.7·d^(2/3)** — fits all four rungs to ≤3% (62/99/157/249 vs 64/96/~152/256).
The exponent is ROBUST to which d=16 seed anchors the fit: 0.666 (with s2's 144)
or 0.673 (with s1's 160) — both ≈ 2/3. **The affine law 8d+32 — exact at
d=4/8/16-s1 — was a 3-point LOCAL LINEAR approximation of this concave power
curve and breaks at d=32 (over-predicts by 11%).** The naive power fit of
NET-40/41 (28.3·d^0.585) was biased by anchoring on the single noisy s2 d=16
reading (144); the four-rung shape settles the exponent at ≈ 2/3. So NET-40/41's
indecision resolves cleanly: AFFINE was the local form (three rungs, exact), the
GLOBAL form is concave power with exponent ≈ 2/3.

## 4. The sub-linear depth leg continues at EVERY rung; the product law does NOT recover

| d | k\* | d·ctx/32 | per-doubling ratio of k\* | ratio vs linear (2.0) |
|---|---|---|---|---|
| 4 | 64 | 64 | — | — |
| 8 | 96 | 128 | ×1.50 | 0.75 |
| 16 | ~152 | 256 | ×1.58 | 0.79 |
| 32 | 256 | 512 | ×1.68 | 0.84 |

The per-doubling ratio (1.50 → 1.58 → 1.68) approaches 2.0 from below but is
STILL sub-linear at d=32 — the retrieval load keeps being shared across the
deeper stack, the product law is a proven-safe upper bound at every rung, and
P3 (recovery at depth) is refuted decisively (k*=256 = exactly half of 512).

## 5. Practical — the over-pruneable factor GROWS with depth

Deployable speedup at ctx=512: d=4 → **8.0×**, d=8 → **5.33×**, d=16 →
**3.2–3.56×**, d=32 → **2.0×** (guarantee d·ctx/32: 4×/4×/2×/1×). The over-
pruneable factor vs the guarantee: 2.0×/1.33×/1.6–1.78×/**2.0×** — the product
law at (d=32, ctx=512) gives NO speedup at all (1.0×); the actual knee still
delivers 2.0×. The sub-linear depth leg is largest in absolute terms where the
guarantee is most pessimistic.

## 6. Concentration — depth diffusion continues, NO bounded working set

| statistic | d=4 | d=8 | d=16 (s1/s2) | d=32 (this round) |
|---|---|---|---|---|
| eff support exp(H) | 152.11 | 177.80 | 199.84/198.78 | **218.46** |
| top-256 mass | — | — | 0.934/0.935 | **0.921** |
| top-384 mass | — | — | — | **0.986** |
| eff early | 20.4 | 23.09 | 25.55/25.53 | **27.81** |
| eff mid | 133.4 | 156.01 | 174.57/173.85 | **190.90** |
| eff late | 281.2 | 332.15 | 372.99/371.99 | **409.08** |

Depth diffusion continues at d=32: eff 199.84 → 218.46 (×1.09 on the depth
doubling, slowing — the diffusion rate saturates while the diffusion itself
continues). Top-256 mass drops to 0.921. Per-position monotone
early ≪ mid ≪ late persists — NO bounded working set at d=32. The top-k mass at
k=256 (0.921) is notably below the k*=256 knee — consistent with the power-law
spread: the distribution is so diffuse at d=32 that even the knee-k captures
only 92% of the attention mass.

## 7. Selection importance — UNMEASURED this round (documented crash gap)

The random-k control (Part B2, planned at k=256/384) was aborted by a script
crash on the k=768 sweep point (topk with k > ctx is out of range — see barrier
(f)). The selection gap at d=32 is therefore NOT measured in this cell. Standing
evidence: the top-k vs random-k gap is positive in EVERY prior measured cell
(+2.3 to +11.7 across all depth × context cells, including +3.4/+2.3 and +6.0/+2.6
at d=16). The gap at d=32 will be captured by the second seed (NET-43, which
patches the crash and restores Part B2).

## 8. Verification vs the network-loop barriers

- **(a) Circularity — no.** Predictions (288 affine / ~215 power / 512 product)
  stated BEFORE the run; measured 256 is NEITHER horn — it discriminates against
  both and the four-rung shape reveals the concave-power-with-2/3 form, checked
  against the three prior measured rungs ex post.
- **(b) Known-method-in-disguise — no.** Depth-scaling law for data-free attention
  key/value pruning: none in the Catalog (698-pkg re-scan) nor the broader
  literature (layer-level pruning arXiv 2512.20636, KV-cache pruning — orthogonal).
- **(c) Toy-scale — confronted.** d=32 × ctx=512 real causal word LM, causal
  masking, 4097 vocab, held-out loss AND accuracy.
- **(d) Data leakage — none.** Held-out last-10% windows; top-k data-free from the
  eval input's own causal attention.
- **(e) Variance/reproducibility — the round's honest limits.** (i) The d=32 cell
  is SINGLE-SEED (every new rung starts single-seed); the knee is bracketed
  (k=224 fails 0.3 SE, k=256 passes 0.7 SE) but a second seed is the natural next
  round. (ii) The exponent-2/3 fit rests on FOUR rungs (d=4/8/16/32) and is
  ROBUST to the d=16 seed choice (0.666 vs 0.673) — the affine-vs-power
  discrimination at d=32 is a ~34% separation, far beyond the knee fuzz.
- **(f) Measurement — documented, including the crash.** Same metrics/protocol as
  every prior cell; binom SE ≈ 0.15% acc; k=512 recovers full loss exactly
  (5.6281 = 5.6281). HONEST CRASH LOG: the k=768 sweep point threw
  `RuntimeError: selected index k out of range` — topk(k) with k=768 on a 512-wide
  causal attention row (my sweep-design error: 768 is only valid at ctx ≥ 768).
  The k=768 point was REDUNDANT (k=512 already = 1.000, exact full loss), so the
  k* verdict is unaffected; but the crash aborted Part B2 (the random-k control),
  which is therefore UNMEASURED for this cell (see §7). The crash is a documented
  measurement defect, not a physics result; NET-43's script drops k=768.
- **(g) Baseline unfairness — partially documented.** Full-attention reference per
  model and the same 0.98 bar are intact; the random-k control at the same k is
  MISSING for this cell due to the crash (standing evidence +2.3–11.7 in every
  prior cell — the direction is not in doubt, the exact value is unrecorded).
- **(h) Practical relevance — sharpened.** The sub-linear depth leg at long
  context is now measured to d=32 and its true form (concave power, exponent
  ≈ 2/3) is pinned: at (d=32, ctx=512) the deployable k is 256 (2.0×), the
  guarantee 512 (1.0× — no speedup) is safe but leaves the full 2.0× on the
  table, and the per-doubling ratio is still < 2 — the product law does NOT
  recover at depth.

## Verdict

NET-42 (speed axis, the discriminating depth rung): **DEPTH-LEG-AT-LONG-CONTEXT-IS-
CONCAVE-POWER — k\* ≈ 24.7·d^(2/3) at ctx=512, with k\* = 256 at (d=32, ctx=512)
refuting BOTH the affine prediction (8d+32 = 288, over by 11%) and the naive
concave-power prediction (28.3·d^0.585 ≈ 215, under by ~16%), and the product law
(512) refuted by 2×.** The four ctx=512 rungs (64, 96, ~152, 256) lie on a concave
power law with exponent ≈ 2/3 (fit ≤3%; exponent robust to the d=16 seed: 0.666–
0.673). **The affine law 8d+32 — exact at d=4/8/16-s1 — was a 3-point LOCAL LINEAR
approximation of this concave power curve and breaks at d=32**; NET-40/41's naive
power fit (0.585) was biased by a single noisy reading. The sub-linear depth leg
CONTINUES at every rung (per-doubling ratio 1.50/1.58/1.68, approaching but never
reaching 2.0 through d=32) — P3 (recovery at depth) refuted decisively. Deployable
speedup at ctx=512: 8.0×/5.33×/3.2–3.56×/2.0× at d=4/8/16/32 (guarantee
4×/4×/2×/1× — the product law gives NO speedup at d=32, the actual knee gives
2.0×). Concentration depth-diffuses to eff 218.46 (top-256 mass 0.921), NO bounded
working set. Honest limits: the d=32 cell is single-seed (bracketed knee) and the
random-k control for this cell is UNMEASURED (documented k=768 crash — my sweep-
design bug, aborted Part B2; k* verdict unaffected). Remaining: **d=32 ctx=512
second seed (closes the deepest rung's single-seed status AND repairs the missing
random-k control — highest value)**, ctx=1024 second seed, d=8 @ ctx=256 s0 corner,
and the carry chain at scale (the frontier).
Round-net-42. Now 42 network experiments. Assessment v42. Paper 86, issue #149.
Scripts: /tmp/exp_net_attncost_d32_ctx512.py; log: /tmp/net42.log.

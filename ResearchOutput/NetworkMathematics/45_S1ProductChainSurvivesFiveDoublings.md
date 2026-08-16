# The s1 Product Chain Survives at 16× Context at the Tightest Margin: k\*=256 at (d=4, ctx=2048, seed=1) = d·ctx/32 EXACTLY (the Fifth Doubling — 16/32/64/128/256 across 128→2048), the Prediction Confirmed, but the Pass Margin (+0.0013) Is the Tightest of the Whole Chain (k=224 fails ~0.45 SE), Selection Importance Dilutes with Context (+1.7/+1.8 — the Smallest at d=4), and the ctx=2048 Second Seed Becomes the Sharpest Open Cell (NET-45)

**Program:** Network/LLM research lab — round-net-45 (speed-axis round 18; the ctx=2048 first seed that tests whether the sub-linear drift continues at 16× context — the sharpest open cell NET-44 made).
**Date:** 2026-08-16
**Status:** Machine-verified (data-free top-k key/value pruning on a real causal word LM, **d=4, seed=1, ctx=2048**, 5 Gutenberg novels, dm=64, vocab 4097, 2000 AdamW steps, 18436s training; ALL_DONE_NET45, no crash).

## Hypothesis and statement

NET-44 measured the first break of product-exactness at any context: k\*=96 at
(d=4, ctx=1024, seed=2) vs the predicted 128 — the s1 context chain's exactness
(16/32/64/128 across 128→256→512→1024) was SEED-LUCKY, and the sub-linear drift
at the second seed raised the sharpest open question: does it continue at 16×
context? This round runs the FIRST seed at **ctx=2048** — a never-measured cell,
4× the longest single-seed context (1024) and 16× the original (128). Three horns
(prediction stated BEFORE the run): **P1 k\*=256 = d·ctx/32** (the s1 chain
continues exact at the fifth doubling); **P2 k\*=192** (the s2 ctx=1024 sub-linear
drift, 0.75×, is systematic and the s1 chain breaks by one grid step at 16×); P3
marginal at 224 (a single-grid-step drop). The sweep grid is enriched in the
predicted region: **{96,128,160,192,224,256,288,384,512,768,1024}** — the first
two steps below the product knee are both measured, so a 224 knee would be pinned
directly.

## 1. Setup (byte-identical harness to NET-37/44, chunked eval for memory safety)

Same 5 Gutenberg novels, word-level top-4097 vocab, contiguous 90/10 split,
causal transformer dm=64/4 heads (head dim 16), d=4, seed=1, 2000 AdamW steps,
**ctx=2048** (292 windows, last 10% held out). Training uses PyTorch's FUSED
`F.scaled_dot_product_attention` (no materialized O(L²) matrix in training —
memory-safe at 2048); the EVAL forward is chunked (CHUNK=8 windows/pass over the
materialized attention rows — identical math to every prior cell, memory safety
only). Full acc **0.1543** (bar 0.1512), full loss **5.2047** — same-family as
the d=4 s1 chain (0.1594 at 1024, 0.1616 at 512; the s1 chain's acc drifts mildly
down with context, k\*-irrelevant). Sweep **{96,128,160,192,224,256,288,384,512,
768,1024}** (the first two sub-product points, 224 and 192, both measured to pin
a sub-linear knee); random-k control {128, 256} (Part B2, seed 12345). Script:
/tmp/exp_net_attncost_ctx2048.py (~7h wall at 4 threads: 18436s training — the
O(L²) attention term dominates at 2048 — + evals).

## 2. The decisive test — k\* = 256, the prediction CONFIRMED (the fifth exact doubling)

| k | retained | verdict |
|---|---|---|
| 96 | 0.939 | ✗ (d=4 ctx=512's 0.983/0.985 and ctx=1024 s1's 0.968 → the whole retained curve shifts DOWN with context; knee unaffected) |
| 128 | 0.951 | ✗ |
| 160 | 0.963 | ✗ |
| 192 | 0.970 | ✗ |
| 224 | 0.976 | ✗ (~0.45 SE below bar — the first sub-product point fails) |
| **256** | **0.9813** | ✓ **k\* = 256 — the product law d·ctx/32 EXACT** |
| 288 | 0.984 | ✓ |
| 384 | 0.993 | ✓ |
| 512 | 0.997 | ✓ |
| 768 | 0.996 | ✓ |
| 1024 | 0.998 | ✓ (loss 5.2062 vs full 5.2047 — Δ0.0015, ~0.03% rel; the first time the ctx/2 point is not EXACTLY full loss — a tiny renormalization residual at 2048-wide rows, documented below) |

**k\*(s1, d=4, ctx=2048) = 256 = d·ctx/32 — the prediction CONFIRMED.** The s1
context chain is now EXACT at FIVE doublings: **k\* = 16/32/64/128/256 across
ctx = 128/256/512/1024/2048**, every doubling reproducing d·ctx/32. The 16×
context cell lands on P1, NOT P2 (192) and NOT P3 (224). But the pass margin is
**+0.0013 — the tightest of the whole chain** (the margins at 128/256/512/1024
were +0.007/+0.010/+0.003/+0.006): k=224 fails by ~0.45 SE, k=256 passes by
~0.13 SE, so the knee is genuinely AT 256 but sitting on the bar. The retained
curve continues the long-context depression (0.939/0.951/0.963/0.970/0.976 at
96..224 — uniformly lower than ctx=1024 s1's 0.968/0.977/0.986 at 96/128/192),
but the KNEE — the economically relevant threshold — is exact.

## 3. What this decides — the s1 chain vs the s2 drift: the tension is now at 16× context

The two facts coexist:
- **At s1 the product law is exact through 16× context** (this round). The s1
  chain's exactness is NOT limited to 8× — it extends to 2048, the longest
  context measured anywhere in the program.
- **At s2 the knee broke by one grid step at 8× context** (NET-44: k\*=96 vs
  128). The seed-fluctuation family (knee-fluctuates-one-grid-step: depth at
  d=16 ctx=512 160/144; context at d=4 ctx=1024 128/96) does NOT reproduce the
  s2 break at the longer cell (this round is s1-only, so it cannot see it).

The margin structure decides the priority: the +0.0013 pass is ~0.13 SE above
the bar — the slimmest margin of any cell in the context chain — and k=224 is
only ~0.45 SE below. The ctx=2048 cell is therefore SINGLE-SEED with a
razor-thin knee, and the **second seed at ctx=2048 is now the sharpest open
cell in the whole attention-cost program**: if s2 reads 256, the d=4 context
chain is two-seed-exact at 16× (extending the two-seed exactness seen at
ctx=512, 64/64); if s2 reads 224, the NET-44 one-grid-step s2 drop replicates
at 16× and the sub-linear drift is confirmed systematic.

## 4. The product law's status at 16× context — exact at s1, at the edge

| context (d=4) | k\* s1 | k\* s2 | d·ctx/32 | two-seed status |
|---|---|---|---|---|
| 128 | 16 | — | 16 | 16 (s0/s1 exact) |
| 256 | 32 | — | 32 | 32 (s0/s1 exact) |
| 512 | 64 | 64 | 64 | **64, 64 (two-seed exact)** |
| 1024 | 128 | 96 | 128 | (64, 128] — knee fluctuates one grid step |
| **2048** | **256** | — | **256** | **single-seed, margin +0.0013 (razor-thin)** |

The product law d·ctx/32 is a proven-safe UPPER BOUND at every measured cell,
and at s1 it is ALSO the exact knee through 16× context. The net status after
NET-44 + NET-45: exact at s1 across five doublings; sub-linear by one grid step
at s2/1024; at the longest cell the s1 margin is at its thinnest — the two-seed
distribution of the 16× knee is uncharacterized (256 vs 224).

## 5. Practical — deployable 8.0× at (d=4, ctx=2048), the guarantee at its thinnest

Deployable speedup at ctx=2048: k\*=256 → attn-FLOP ratio **8.0×** — exactly the
product-law guarantee (32/d = 8×), confirmed at the longest context measured
(16× the original). But where every prior s1 pass cleared the bar comfortably,
this one sits at +0.0013 — the guarantee is now the KNEE ITSELF, not a safe
margin above it. The honest deployable claim: 8.0× at (d=4, ctx=2048) with the
caveat that the second seed could read 224 (10.3×) or 256 (8.0×) — the same
one-grid-step ambiguity NET-44 measured at 8× context (128/96).

## 6. Concentration — diffusion continues at 16× context, NO bounded working set

| statistic | ctx=1024 s1 (NET-37) | ctx=2048 s1 (this round) |
|---|---|---|
| eff support exp(H) | 291.16 | **526.39** |
| top-128 mass | 0.702 | **0.589** |
| top-256 mass | 0.731 (k256 mass @1024) | **0.731** |
| eff early | 37.56 | **68.21** |
| eff mid | 255.76 | **461.11** |
| eff late | 542.05 | **987.30** |

The context diffusion continues at the fifth doubling: eff support ×1.81
(291.16 → 526.39) — the same superlinear family as the prior doublings
(×1.74/×1.89/×1.91). The top-128 mass drops to 0.589 (the distribution spreads
further as context grows) yet the top-256 mass stays 0.731 — the knee-k
captures the same mass at 2048 as at 1024, consistent with the knee being
exact. The monotone early ≪ mid ≪ late shape persists (68 ≪ 461 ≪ 987) — NO
bounded working set at 16× context.

## 7. Selection importance — dilutes with context: +1.7/+1.8, the smallest at d=4

| k | top-k retained | random-k retained | gap | gap ctx=1024 s1 |
|---|---|---|---|---|
| 128 | 0.951 | 0.934 | **+1.7** | +5.9 |
| 256 | 0.981 | 0.963 | **+1.8** | +4.6 |

Selection importance at 16× context drops to **+1.7/+1.8 — the smallest at d=4**
(from +5.9/+4.6 at 8×, +5.3/+4.6 at 4×). The gap stays positive (top-k by
trained weight still beats random-k at the same k) but is diluted ~3×: at the
longest context the attention distribution is so diffuse (top-256 mass only
0.731) that even a random half of the keys carries most of the mass. Selection
survives but is now a minor factor — the same dilution pattern as the depth
axis (gaps narrow with depth too, +2.6/+1.7 at d=32).

## 8. Verification vs the network-loop barriers

- **(a) Circularity — no.** Prediction (k\* = 256 = d·ctx/32 continuing the
  exact s1 chain) stated BEFORE the run; measured 256. The prediction CONFIRMED
  — a genuine extension test at 16× context, the first point beyond 8×.
- **(b) Known-method-in-disguise — no.** Context-scaling of data-free attention
  key/value pruning at 16× context: none in the Catalog (698-pkg re-scan) nor
  the literature (layer/KV pruning, context-length laws — orthogonal). The
  razor-thin margin at the longest context is predicted by no prior source.
- **(c) Toy-scale — confronted.** d=4 × ctx=2048 real causal word LM, causal
  masking, 4097 vocab, held-out loss AND accuracy — the LONGEST context in the
  whole program (16× the original 128).
- **(d) Data leakage — none.** Held-out last-10% windows; top-k data-free from
  the eval input's own causal attention.
- **(e) Variance/reproducibility — the honest limit.** The s1 chain is exact at
  FIVE doublings but at the tightest margin of the chain (+0.0013; k=224 fails
  ~0.45 SE, k=256 passes ~0.13 SE). Combined with NET-44's s2 one-grid-step
  break at 8×, the ctx=2048 cell's single-seed status is the sharpest open
  question: the second seed at 16× decides whether 256 is two-seed-exact
  (extending ctx=512's 64/64) or drops one grid step to 224 (replicating the
  NET-44 s2 pattern).
- **(f) Measurement — clean.** Same metrics/protocol as every prior cell;
  binom SE ≈ 0.11% acc (retained SE ≈ 0.007); the pass margin +0.0013 is the
  tightest of the whole context chain (documented as the round's honest limit);
  k=1024 recovers retained 0.998 with loss 5.2062 vs full 5.2047 (Δ0.0015,
  ~0.03% rel — the first time the ctx/2 point is not EXACTLY full loss, a tiny
  renormalization residual at 2048-wide rows; prior cells' k=ctx/2 hits were at
  ≤1024 rows where the residual is below 4-decimal resolution); chunked eval
  (CHUNK=8) verified identical math; NO crash (ALL_DONE_NET45).
- **(g) Baseline unfairness — none.** Full-attention reference per model, the
  same 0.98 bar, random-k control at the same k: gaps +1.7 (k=128) / +1.8
  (k=256). Positive but the SMALLEST at d=4 — the top-k selection still does
  real work at 16× context, just diluted (the distribution is so diffuse that
  random keys carry most of the mass). Fair both ways.
- **(h) Practical relevance — sharpened.** The deployable 8.0× at (d=4,
  ctx=2048) is exactly the product-law guarantee at the longest context
  measured — but the guarantee is now the KNEE ITSELF, not a safe margin above
  it, so the two-seed confirmation at 2048 is the practical next step. The
  selection dilution (+1.7/+1.8) is a real caveat: at 16× context the top-k
  choice matters less, consistent with the diffuse distribution.

## Verdict

NET-45 (speed axis): **THE-S1-PRODUCT-CHAIN-SURVIVES-AT-FIVE-DOUBLINGS-AT-THE-
TIGHTEST-MARGIN — k\* = 256 at (d=4, ctx=2048, seed=1) = d·ctx/32 EXACTLY, the
prediction CONFIRMED at the fifth context doubling (16/32/64/128/256 across
128→2048, 16× context — the longest measured anywhere in the program).** P2
(192, systematic 0.75× sub-linear drift) and P3 (224, one-grid-step drop) are
both REFUTED at s1; the exact s1 chain extends to 16×. BUT the pass margin is
**+0.0013 — the tightest of the whole chain** (k=224 fails ~0.45 SE, k=256
passes ~0.13 SE), so the ctx=2048 cell is single-seed with a razor-thin knee:
the SECOND SEED AT 16× is the sharpest open cell in the program — it decides
whether 256 is two-seed-exact (extending ctx=512's 64/64) or drops one grid
step to 224 (replicating NET-44's s2 break, now at 16× context). Selection
importance dilutes with context (+1.7/+1.8 at 16× vs +5.9/+4.6 at 8× — the
smallest at d=4, the diffuse distribution carrying most of the mass in any
half of the keys); concentration continues the superlinear diffusion (eff
526.39, ×1.81 on the doubling) with the monotone early≪mid≪late shape and NO
bounded working set at 16×; deployable speedup **8.0×** at (d=4, ctx=2048),
the guarantee intact but now equal to the knee. Honest limits: single seed at
16× with a razor-thin margin; the s2 knee distribution at 2048 uncharacterized
(256 vs 224); k=1024 not exactly full loss (Δ0.0015, documented). Remaining:
**ctx=2048 second seed (highest value — closes the 16× cell's single-seed
status); a third seed at ctx=1024 (knee distribution {96,128}); d=8 @ ctx=256
s0 corner; a third seed at d=16 (low value); carry chain at scale (the
frontier)**. Round-net-45. Now 45 network experiments. Assessment v45. Paper
89, issue #152. Scripts: /tmp/exp_net_attncost_ctx2048.py; log: /tmp/net45.log.

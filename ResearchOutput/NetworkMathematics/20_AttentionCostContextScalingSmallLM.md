# k* Is NOT Context-Independent: Lossless-k Grows with Context, the Attention-FLOP Lever Is Context-Constant (8× at d=4, Not 64×) (NET-20)

**Program:** Network/LLM research lab — round-net-20 (speed-axis round 5; the context-scaling check of the attention-cost law k* = 4·d)
**Date:** 2026-08-13
**Status:** Machine-verified (data-free top-k key/value pruning on a real causal word LM, **ctx=256** — the first point of the context ladder, d=4, 5 Gutenberg novels, dm=64, vocab 4097, 2000 AdamW steps).

## Hypothesis and statement

NET-15 (d=4, ctx=128) found data-free top-k key/value pruning LOSSLESS at
k=16 (8× attention-core FLOPs); NET-16/17 established k* = 4·d at fixed
ctx=128 (k*=16/32/64 across d=4/8/16), with the cost law **speedup ≈ ctx/(4d)**.
That law carries an UNTESTED assumption — flagged in NET-17's barrier (h) —
that k* does NOT grow with context: the projected 64× attention-core
reduction at ctx=4096, d=16 rests on k* staying at 4d while ctx grows. This
round tests that assumption directly: train the SAME d=4 model on the SAME
Gutenberg corpus at **ctx=256 (2× the NET-15 context)**, 2000 steps, then
measure the top-k knee. Three horns:
- **P1** k* stays ≈16 → per-layer retention r(k) is context-independent; the
  lever grows with context (16× at ctx=256; the 64× @ 4096 projection holds).
- **P2** k* grows sublinearly (≈24–32) → mild context dependence, needs a
  correction k* = 4d·f(ctx).
- **P3** k* grows ~proportionally (≈32 = 0.125·ctx) → top-k is a "top
  fraction", the lever is context-CONSTANT, the 64× projection is REFUTED.

## 1. Setup (identical to NET-15 family, context doubled)

Same 5 Gutenberg novels, word-level top-4097 vocab, contiguous 90/10 split,
causal transformer (is_causal=True) dm=64/4 heads (head dim 16), **d=4**, seed
0, 2000 AdamW steps, but **ctx=256** (2,343 contiguous windows; 2× the tokens
per step of NET-15). Full acc **0.1612** (NET-15 ctx=128 d=4: 0.1571; the
family scale 0.1571–0.1619), bar 0.98·full = **0.1579**, full loss **5.0877**
(NET-15: 5.1188). Eval via the explicit causal-attention forward (k=192
recovers the full loss exactly, 5.0877). The top-k mask is computed from each
eval input's own trained attention weights at inference — no calibration, no
training labels, no leakage. All evals joint on the held-out split. Script:
/tmp/exp_net_ctx256.py (~25 min wall on CPU at 4 threads).

## 2. Part A — the concentration law is context-DEPENDENT (more diffuse at longer context)

Per-query effective support exp(H) at ctx=256 (uniform-causal baseline ≈128):
overall mean **82.94** — vs 46.6 at ctx=128. Relative to uniform, attention is
LESS concentrated at longer context: eff/ctx = 0.36 (ctx=128) → **0.65**
(ctx=256). Top-k mass fractions fall below the ctx=128 values at every fixed k:
top-8 0.450 → **0.363**, top-16 0.617 → **0.503**, top-32 0.795 → **0.662**,
top-64 → 0.823.

**Per-position breakdown (new):** effective support grows monotonically with
how much past is available — early queries (positions 0–31, ≤32 past tokens):
**11.3**; mid (96–127, ≈128 past): **72.3**; late (224–255, ≈256 past):
**155.4**. There is NO bounded working set: attention spreads over roughly a
large fraction of whatever context is present. This is the direct
concentration-side signature of why k* must grow with context.

## 3. Part B — the decisive test: k* doubles when context doubles

Data-free top-k key/value pruning (per-query, per-head, by trained weight,
renormalized), joint eval on held-out, ctx=256:

| k | retained acc | loss | Δloss | attn-core FLOP ratio | verdict |
|---|---|---|---|---|---|
| 8 | 0.947 ✗ | 5.1658 | +0.078 | 32× | |
| 16 | 0.971 ✗ | 5.1285 | +0.041 | 16× | was LOSSLESS at ctx=128 (0.984 ✓) |
| **32** | **0.989 ✓** | 5.1041 | +0.016 | 8× | **the knee** |
| 64 | 0.996 ✓ | 5.0919 | +0.004 | 4× | |
| 128 | 1.000 ✓ | 5.0882 | +0.001 | 2× | |
| 192 | 0.999 ✓ | 5.0877 | +0.000 | 1.3× | exact loss match |

**k* = 32 at ctx=256 — EXACTLY DOUBLE the ctx=128 knee (16).** k=16, lossless
at ctx=128 (0.984), FAILS at ctx=256 (0.971 < 0.98 bar); the knee moves to
k=32 (0.989). At d=4, k* is proportional to context in the tested range:
k* = ctx/8 (16 @ 128, 32 @ 256).

## 4. The corrected cost law — the lever is context-CONSTANT

Combining NET-16/17 (k* = 4d at ctx=128) with this point (k* = 32 at
ctx=256, d=4), the unified two-parameter law across all four measurements is

**k* = d·ctx/32** (= 4d · (ctx/128)), i.e. **speedup = ctx/k* = 32/d** —
**independent of context length.**

| | ctx=128 | ctx=256 |
|---|---|---|
| d=4 | k*=16, 8× | k*=32, 8× |
| d=8 | k*=32, 4× | — |
| d=16 | k*=64, 2× | — |

**NET-17's projected "speedup ≈ ctx/(4d) → 64× at ctx=4096, d=16" is REFUTED.**
The lever does NOT grow with context; it is a **depth-only property (32/d)**: 8×
at d=4, 4× at d=8, 2× at d=16, at ANY context length within the tested range.
Long context buys no additional relative saving, because the lossless window
scales with it (k* ∝ ctx). The honest surviving claim: at d=4 the 8× lever is
robust at both 128 and 256 (it neither decays nor grows with context in this
range).

## 5. Part B2 — random-k control: selection still matters at 2× context

| k | top-k | random-k | gap |
|---|---|---|---|
| 16 | 0.971 | 0.884 | **+8.7 pts** |
| 32 | 0.989 | 0.929 | **+6.0 pts** |

Weight-selected positions beat random at the same k; the gap (+6.0–8.7 pts) is
the same magnitude as at ctx=128 (+4.8–6.2). The selection information is real
and does not disappear with more context.

## 6. Verification vs the network-loop barriers

- **(a) Circularity — no.** Top-k mask from the eval input's own causal
  attention at inference; joint evals; k=192 recovers the full loss exactly
  (5.0877 = 5.0877). Nothing injected.
- **(b) Known-method-in-disguise — the context-scaling is the content.** Top-k
  sparse attention is known; the specific result — k* ∝ ctx at fixed depth on a
  real causal word LM, the context-CONSTANT lever (32/d), and the
  concentration-side diffusion with context (eff 46.6→82.9, per-position
  growth) — is new. Catalog scan (698 packages): no context-scaling law of
  sparse-attention pruning on a real small causal LM.
- **(c) Toy-scale — confronted.** Real causal LM, real text, causal masking,
  4097 vocab, 2× context, held-out loss AND accuracy.
- **(d) Data leakage — none.** Top-k data-free from the eval input's own causal
  attention; contiguous no-overlap split; held-out eval.
- **(e) Variance — honest limits.** One seed; the context ladder is TWO points
  (128, 256) at d=4 — the k* ∝ ctx proportionality is a 2-point claim, exact
  at this resolution but not extrapolated. The unified law k* = d·ctx/32 fits
  all four measurements (3 depths @ 128 + 1 depth @ 256) with one 2× context
  step. A ctx=512 point or a seed-1 ctx=256 re-run would strengthen; within the
  tested range the qualitative claim is robust (k=16 clearly fails at 256 vs
  clearly passing at 128; k=32 clearly passes).
- **(f) Measurement — documented.** 0.98·full bar AND raw loss; 6-point sweep +
  2-point random control (fixed seed 12345); k=192 exact numerics; eval noise
  ≈0.15% ≪ the k=32 margin (0.989 vs 0.98, margin 0.009); the ctx=128
  reference (k=16 lossless) is the exact NET-15 reproduction on the same
  testbed.
- **(g) Baseline fairness.** Full-attention reference (0.1612 / 5.0877);
  random-k at the same k (+8.7/+6.0 pts); same bar.
- **(h) Practical relevance — REFRAMED NEGATIVE, and the honest consequence.**
  The 64× long-context projection is refuted: the top-k lever does not compound
  with context (8× at d=4 at both 128 and 256). The surviving, now
  better-characterized claim is the depth-only lever 32/d (8× at d=4, robust in
  context). This is the more honest cost model for deployments: at small depth
  the saving is real but flat in context; deep models get little regardless of
  context. k*'s proportionality is measured at one 2× step — the boundary of
  the claim is ctx ∈ [128, 256].

**Verdict.** NET-20 (speed axis, context-scaling of the attention-cost law):
**k* is NOT context-independent.** At d=4, doubling context doubled the
lossless window (16 → 32, exactly proportional at this resolution), so the
attention-FLOP lever is **context-CONSTANT — speedup ≈ 32/d (8× at d=4 at both
128 and 256)** — refuting NET-17's projected 64× at ctx=4096. Unified law:
**k* = d·ctx/32**, lever = 32/d (a depth-only property). The concentration law
is context-DEPENDENT: attention is more diffuse at longer context (eff support
46.6 → 82.9; per-fixed-k mass lower; late queries eff≈155 — no bounded working
set), which is exactly why the lossless window must grow. Random-k gap survives
at 2× context (+6.0–8.7 pts). DIFFUSE-BUT-PRUNABLE survives, now with a
context-constant lever instead of a context-growing one. Round-net-20.
Now 19 network experiments. Assessment v19. Paper NET-20, issue #114.
Scripts: /tmp/exp_net_ctx256.py.

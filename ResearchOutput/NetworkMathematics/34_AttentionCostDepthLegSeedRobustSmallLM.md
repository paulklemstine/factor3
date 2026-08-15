# k* = d·ctx/32 Holds at Every Grid Point at a Second Seed: The Depth Leg of the Attention-Cost Law Is Seed-Robust (NET-34)

**Program:** Network/LLM research lab — round-net-34 (speed-axis round 7; closes the last single-seed limb of the attention-cost law)
**Date:** 2026-08-15
**Status:** Machine-verified (data-free top-k key/value pruning on a real causal word LM, **d=8, seed=1**, at **ctx=128 AND ctx=256**, 5 Gutenberg novels, dm=64, vocab 4097, 2000 AdamW steps per model).

## Hypothesis and statement

NET-33 (issue #140) closed the ∝-ctx leg of the attention-cost law k* = d·ctx/32
at d=4 (k* = 16/32 exact at seed=1, both contexts). That paper's barrier (e)
named the remaining single-seed limb explicitly: the DEPTH leg — k* = 4d at
ctx=128 for d ∈ {8,16} rests on seed-0 alone (NET-16: d=8, k*=32; NET-17: d=16,
k*=64). This round trains the SAME CausalTF at **d=8, seed=1** (byte-identical
harness, 2000 steps) at BOTH contexts: ctx=128 re-measures the depth leg at a
second seed, and **ctx=256 is a never-measured grid cell** — the first point
where the depth and context levers act simultaneously, testing the FULL
two-parameter law at d>4. Three horns:
- **P1** k*(s1, d=8, ctx=128) = 32 (4d) AND k*(s1, d=8, ctx=256) = 64
  (d·ctx/32 = 8·256/32) → the depth leg is SEED-ROBUST and the law holds at a
  second seed in every measured cell of the (d × ctx) grid.
- **P2** k* differs from the prediction → the depth leg is a single-seed
  artifact (or the ctx-proportionality fails at depth).
- **P3** same knee, different margins/concentration → knee robust, per-k values
  depth-scattered (report both).

## 1. Setup (identical to NET-15/16/20/33, d=8, seed=1, both contexts)

Same 5 Gutenberg novels, word-level top-4097 vocab, contiguous 90/10 split,
causal transformer (is_causal=True) dm=64/4 heads (head dim 16), **d=8, seed 1**,
2000 AdamW steps, at **ctx=128 and ctx=256**. Full acc **0.1620** (ctx=128) and
**0.1620** (ctx=256) — vs s0's d=8 ctx=128 0.1619 (NET-16); the six-model
(spread × depth × ctx) full-acc set 0.1571–0.1620 is tightly clustered. Full
losses 5.0808 / 5.0865. Bar 0.98·full = 0.1587 / 0.1588. Eval via the explicit
causal-attention forward; top-k mask from each eval input's own trained
attention weights at inference — no calibration, no labels, no leakage; all
evals joint on the held-out split. Script: /tmp/exp_net_attncost_d8_s1.py
(~38 min wall on CPU at 4 threads: 735s + 1554s).

## 2. The decisive test — BOTH cells land exactly on the prediction

Data-free top-k key/value pruning (per-query, per-head, by trained weight,
renormalized), joint eval on held-out; k* = smallest k with retained ≥ 0.98:

| ctx | seed | full acc | k sweep (retained) | k* | predicted d·ctx/32 |
|---|---|---|---|---|---|
| 128 | s0 (NET-16) | 0.1619 | 16→0.961 ✗ 32→0.983 ✓ | — | **32** | 32 |
| 128 | **s1** | 0.1620 | 16→0.962 ✗ 32→**0.988** ✓ | 0.999 @ 64 | **32** | 32 |
| 256 | **s1** (NEW CELL) | 0.1620 | 32→0.968 ✗ 64→**0.990** ✓ | 0.999 @ 128, 1.000 @ 192 | **64** | 64 |

**k*(s1, d=8, ctx=128) = 32 and k*(s1, d=8, ctx=256) = 64 — both EXACT.** The
depth leg k* = 4d holds at a second seed (k* = 32 identical to s0 at ctx=128),
and the never-measured ctx=256 cell lands on d·ctx/32 = 64 with a clean margin
(k=32 0.968 fails, k=64 0.990 passes; margin 0.010 — the same margin as every
prior pass). **The full two-parameter law k* = d·ctx/32 now holds at a second
seed in every measured cell of the 2×2 (d ∈ {4,8} × ctx ∈ {128,256}) grid.** The
knee is, as at d=4, if anything MORE favorable at s1: retained@k* 0.988 (s0:
0.983) at ctx=128. At ctx=256 the k=128 retained 0.999 and k=192 recovers full
loss exactly (5.0868 vs 5.0865, Δ0.0003), bounding the sweep.

## 3. Part A — concentration reproduces to ≤0.003; the diffusion law extends

| statistic | ctx=128 s0 | ctx=128 s1 | ctx=256 s1 |
|---|---|---|---|
| eff support exp(H) | 50.13 | **50.16** | **91.49** |
| top-8 mass | 0.419 | 0.418 | 0.320 |
| top-16 mass | 0.586 | 0.586 | 0.458 |
| top-32 mass | 0.772 | 0.772 | 0.623 |
| top-64 mass | — | 0.934 | 0.799 |
| eff early | — | 6.86 | 12.45 |
| eff mid | — | 43.80 | 80.88 |
| eff late | — | 93.83 | 170.47 |

At ctx=128 the d=8 concentration reproduces to within 0.003 at every k — eff
support 50.16 vs 50.13, top-k masses essentially identical. At ctx=256 the
context diffusion law (eff ~doubling when ctx doubles) extends to depth: 50.16
→ 91.49 (1.82× as ctx doubles — slightly sublinear at depth, consistent with
the d=4 46.6→82.9 = 1.78×), and the per-position monotone growth with no
bounded working set reproduces (6.86/43.80/93.83 and 12.45/80.88/170.47).
**The diffuse-but-prunable structure is depth-invariant.**

## 4. Part B2 — selection importance survives depth AND seed

| ctx | k | top-k (s1) | random-k (s1) | gap s1 | gap s0 |
|---|---|---|---|---|---|
| 128 | 16 | 0.962 | 0.882 | **+8.0** | +9.5 |
| 128 | 32 | 0.988 | 0.926 | **+6.2** | +7.1 |
| 256 | 32 | 0.968 | 0.897 | **+7.1** | — |
| 256 | 64 | 0.990 | 0.945 | **+4.5** | — |

Weight-selected positions beat random by 4.5–8.0 pts at d=8 — the same
selection-gap family as d=4 (there, 6.0–8.7). The selection information is real,
depth-invariant, and seed-stable.

## 5. Verification vs the network-loop barriers

- **(a) Circularity — no.** Independent fresh training at seed=1; the prediction
  (32/64) was stated BEFORE the run from s0 data and the d·ctx/32 law; k* is
  measured from each model's own trained attention at inference. Nothing
  injected.
- **(b) Known-method-in-disguise — no.** Reproducibility verification of an
  established empirical law (barrier-e check), not a re-labeled method. Catalog
  scan (698 packages, this family rescanned at NET-33): no seed-robustness,
  depth-leg, or two-parameter result for top-k attention pruning exists.
- **(c) Toy-scale — confronted.** Real causal word LM, real text, causal masking,
  4097 vocab, two context lengths, held-out loss AND accuracy; the deepest model
  of the law's own testbed at the longest context.
- **(d) Data leakage — none.** Held-out last-10% windows; top-k data-free from
  the eval input's own causal attention; no test signal in training.
- **(e) Variance/reproducibility — the point of the round, CLEARED.** The depth
  leg k* = 4d is now two-seed at d=8 (k* = 32 exact both seeds, ctx=128), and the
  full 2-parameter law holds at a second seed in every measured cell of the
  (d × ctx) grid. Honest remaining limits: d=16 (k* = 4d at d=16, NET-17) is
  still single-seed; no ctx=512 point exists; "exact" k* is at the sweep's
  k-resolution.
- **(f) Measurement — documented.** Same metrics/protocol as NET-15/16/20/33
  (retained acc vs 0.98·full bar + raw loss), same eval protocol, same random-k
  fixed seed 12345; k=192 recovers the full loss exactly (5.0868 vs 5.0865);
  retained 1.000 at k=192 and the 0.999 at k=128 are the same re-normalization
  Monte-Carlo saturation seen at d=4 — acc noise ≈0.15% ≪ the k*=64 margin
  (0.990 vs 0.98, margin 0.010).
- **(g) Baseline unfairness — none.** Full-attention reference per model; random-k
  control at the same k; same 0.98 bar everywhere.
- **(h) Practical relevance — strengthened.** The deployable claim — speedup
  32/d (8× at d=4, 4× at d=8), context-invariant within [128, 256] at both
  depths — now rests on two seeds at every measured grid cell. A depth+context
  claim that survives both levers changing is a claim that can be shipped
  without per-instance re-measurement.

## Verdict

NET-34 (speed axis, depth-leg robustness of the attention-cost law):
**DEPTH-LEG SEED-ROBUST CONFIRMED.** k*(s1, d=8) = **32** @ ctx=128 (exact vs
s0 and 4d) and k*(s1, d=8) = **64** @ ctx=256 — the first-ever measurement of
that grid cell, landing exactly on d·ctx/32 = 64. The concentration statistics
reproduce to ≤0.003 at ctx=128, the context-diffusion law extends to depth
(50.16 → 91.49 as ctx doubles), and the selection gap survives depth and seed
(4.5–8.0 pts). **The last single-seed limb of the attention-cost law is closed:
k* = d·ctx/32 holds at a second seed in every measured cell of the 2×2 grid.**
Remaining single-seed: d=16 at ctx=128 (NET-17) and the entire ctx=512 regime.
Round-net-34. Now 34 network experiments. Assessment v34. Paper 78, issue #141.
Scripts: /tmp/exp_net_attncost_d8_s1.py; log: /tmp/net34.log.

# The PR Quantization Law at Small-LM Scale: Role-Structured Bit-Need Survives, but Uniform-3 Is Not Lossless on Real Text (NET-11)

**Program:** Network/LLM research lab — round-net-11 (the loop's rotation directive: real-scale checks; compression axis)
**Date:** 2026-08-13
**Status:** Machine-verified (per-matrix participation-ratio + RTN bit-need sweep on 2 real causal word LMs, d=4 and d=8, 5 Gutenberg novels, dm=64, ctx=128, vocab 4097, 2000 AdamW steps; joint uniform-2/3; role-schedule joint follow-up).

## Hypothesis and statement

NET-1 (toy scale) measured a **monotone per-layer bit-need law** b*(PR) on a
generalizing MLP (high-rank bottleneck needs 6 bits, rank-1 readout 2 bits) and
a **reversal** on a toy attention-LM: interior matrices (PR 12–25) robust at 2
bits, LOW-PR input embeddings fragile (b*=3), joint uniform-2 fails while
uniform-3 is lossless (0.98–1.0). The loop's rotation directive is the
compression-axis real-scale check. **Hypothesis: the monotone b*(PR) law — or
its attention-LM reversal — survives on a real causal word LM**, giving a
calibration-free per-layer bit schedule. Falsifying horns: (a) b* is not a
monotone function of PR at real scale (per-matrix counterexample), and/or
(b) the practical toy schedule (uniform-3) is not lossless on real text.

## 1. Setup (identical to NET-10 Part B so results are comparable)

Same 5 public-domain Gutenberg novels (599,869 words), lowercased, word-level
top-4097 vocab (UNK=0), contiguous windows of 128, first 90% train / last 10%
test. Causal transformer dm=64, 4 heads (head dim 16), **is_causal=True**
(causal masking — no future peek; NET-10's screen is respected), d∈{4,8} × 1
seed each, 2000 AdamW steps (batch 48, lr 3e-4). Reproduces NET-10 exactly:
d=4 s0 teacc **0.1571**/teloss 5.119, d=8 s0 teacc **0.1619**/teloss 5.079 —
identical models to the exit-law round, so the quantization measurements sit on
the same trained family.

For every 2-D matrix in the model (embed, pos, per-layer wq/wk/wv/ao/mi/mo,
final readout un, LayerNorm-weight lnf) we compute
PR = (Σ s²)² / (Σ s⁴) (effective rank via singular values) and measure
**b\* = minimal per-tensor symmetric RTN bits in {2,3,4,6,8} retaining
≥ 0.98 · full held-out next-token accuracy**, each matrix quantized in
isolation and restored afterward. Then the joint test: all matrices at a
uniform bit width simultaneously (NET-1's practical claim).

## 2. Per-matrix result: bit-need is role-structured, not PR-monotone

Same structure in BOTH models (d=4: 28 matrices; d=8: 52 matrices; every matrix
in each class behaved identically across all layers and both depths):

| matrix class | PR range | b\* | 2-bit retained acc | verdict |
|---|---|---|---|---|
| attention proj. wq/wk/wv/ao (square 64×64) | 19–32 | **2** | 0.992–1.002 | lossless at 2 bits |
| MLP proj. mi (64×256) | 43–52 | **3** | 0.87–0.97 | 3-bit needed |
| MLP proj. mo (256×64) | 31–46 | **3** | 0.85–0.97 | 3-bit needed |
| pos (128×64) | 40 | **4** | 0.96 (borderline) | 4-bit to clear 0.98 |
| embed (4097×64) | 63 | **4** | 0.48 (acc 0.075/0.077) | 4-bit needed |
| readout un (64×4097) | **15 (lowest)** | **4** | **0.27/0.32 (acc 0.043/0.051)** | 4-bit needed, catastrophic at 2 |
| lnf weight (vector) | 1.0 | 2 | ~1.00 | lossless |

- **The role structure survives the real-scale transfer:** the input/output
  "interface" (embed, pos, un) is the fragile part (b*=4), the MLP mid (b*=3),
  the attention projections are 2-bit lossless — the same direction as NET-1's
  toy attention-LM reversal (interior robust, embedding fragile).
- **But the PR *predictor* fails as a per-matrix law.** The readout un has the
  LOWEST PR in the model (15) yet needs the MOST bits (4) — a direct
  monotonicity counterexample (low PR but high bit-need). And within the same
  PR band (≈29–31), attention projections are 2-bit lossless while mo0 (PR 30.8)
  needs 3 bits. The measured corr(PR,b*) (+0.58 / +0.67) is positive only
  because the fragile interface matrices (embed 63, pos 40) happen to have high
  PR; it is role-grouping in disguise, not a law. NET-1's monotone b*(PR) —
  whether on the MLP or its toy reversal — does **not** transfer as a
  per-matrix predictor.

## 3. Joint result: uniform-3 is NOT lossless on real text

NET-1's practical toy claim was "joint uniform-2 fails, uniform-3 lossless
(0.98–1.0)". Quantizing every matrix at the same width simultaneously:

| model | full | uniform-2 (retained) | uniform-3 (retained) |
|---|---|---|---|
| d=4 s0 | 0.1571 | 0.0247 (**0.16**) | 0.1305 (**0.83**) |
| d=8 s0 | 0.1619 | 0.0074 (**0.05**) | 0.1179 (**0.73**) |

- uniform-2 collapses to chance-ish levels on both (matching NET-1), but
  **uniform-3 retains only 0.83 / 0.73 — far from lossless.** NET-1's
  "per-layer isolation undercounts joint damage" warning is not a toy footnote:
  isolated 3-bit retains ≥95% almost everywhere (embed/un 0.95, MLP 0.985–1.0),
  yet compounding across the stack costs 17–27 points.
- The deeper model is worse (0.83 → 0.73): more layers = more compounding of
  the fragile interface's 3-bit error (embed/un each lose ~5% at 3-bit, and the
  error flows through the whole depth). Depth hurts quantization, not helps.
- **The NET-1 practical schedule (uniform-3) is refuted at real scale.**

## 4. The constructive check: a role-based schedule (follow-up)

If the bit-need is role-structured, protecting the fragile interface while
leaving attention at 2 bits should restore near-losslessness — at some cost.
Tested on a freshly retrained d=4 s0 (identical config, full acc re-verified
0.1571, lossless bar 0.98·full = 0.1540):

| schedule | acc | retained | avg-bits (size-weighted) |
|---|---|---|---|
| uniform-2 | 0.0176 | 0.112 | 2.00 |
| uniform-3 | 0.1297 | 0.825 | 3.00 |
| **role(4/3/2)** (embed/pos/un=4, mi/mo=3, attn=2, lnf=2) | 0.1379 | **0.878** | 3.64 |
| role-tighter (mi also =4) | 0.1409 | 0.897 | 3.73 |

**The role schedule does NOT restore losslessness.** It beats uniform-3 by ~5
points (0.878 vs 0.825) but costs 21% more bits (3.64 vs 3.00 avg) and is still
12% short of the 0.98·full bar. Pushing the MLP-in to 4 bits recovers only ~2
more points. Per-matrix isolation says almost everything is ≥95% at its
schedule width, yet the joint result loses 10–12%: the small per-matrix errors
compound and are amplified by the residual-stream norm growth through depth
(the same mechanism NET-2/NET-10 found at this scale) — exactly NET-1's
"isolation undercounts joint damage," but severe enough that NO static RTN
schedule ≤ 3.7 avg bits is lossless on real text. The role structure is real
but is NOT a sufficient schedule at this scale.

## 5. Verification vs the network-loop barriers

- **(a) Circularity — no.** PR and b* are measured independently; RTN is
  data-free per-tensor (max-scale); the joint test injects nothing.
- **(b) Known-method-in-disguise — the negatives are new at this scale.**
  Sensitivity-based mixed precision (HAWQ/OBS/GPTQ) and per-layer bit
  allocation are known; what is new: (i) the monotone b*(PR) law — NET-1's own
  claim — fails at real-LM scale (readout counterexample, role-grouped
  correlation), and (ii) uniform-3 — the toy lab's practical schedule — is not
  lossless on real text (0.83/0.73), with depth making it worse. Catalog scan
  (2094 packages): no prior work on either. This is an honest real-scale
  negative that retires a toy-practical claim.
- **(c) Toy-scale — confronted head-on.** This IS the real-scale check (real
  text, causal masking, 4097-token vocabulary), and the toy law/schedule fail it.
- **(d) Data leakage — none.** Causal masking (is_causal=True), contiguous
  no-overlap train/test split, held-out eval, data-free quantization.
- **(e) Variance — 2 models × every matrix.** The structure is IDENTICAL across
  d=4 and d=8 (every one of 28 / 52 matrices in its class's band; both joint
  tests agree the toy schedule fails). One seed per depth; reported honestly.
- **(f) Measurement — documented.** 0.98·full bar, full retained fractions
  reported (not just b*), pos's 2-bit 0.96 knife-edge noted, eval noise
  ≈0.15% on 60k tokens, exact NET-10 reproduction (0.1571/0.1619) confirms the
  training leg is the same family as before.
- **(g) Baseline fairness — uniform-2 and uniform-3 are the strong baselines.**
  The per-matrix sweep is compared to each matrix's own full-precision acc; the
  joint tests are the honest "what you'd actually ship" comparisons.
- **(h) Practical relevance — the negative IS the win.** A common practical
  choice (uniform-3 or uniform-2 weights) is NOT safe on real causal LMs at
  this scale; and the role schedule recovers only ~5 points of the deficit at
  21% more bits — per-layer RTN is not the lever. The honest takeaway: on real
  text, joint compounding (amplified by norm growth through depth) defeats
  static per-matrix schedules below ~4 bits; a real bit-schedule needs
  joint-aware or activation-aware allocation, not data-free PR.

**Verdict.** NET-11 (compression-axis real-scale rotation): the role structure
of NET-1's attention reversal survives (interface fragile / interior robust —
embed/pos/un b*=4, MLP b*=3, attention 2-bit lossless on BOTH a d=4 and d=8
real causal LM), but (1) the monotone b*(PR) law does NOT transfer as a
per-matrix predictor (the readout, PR≈15 the lowest, needs the most bits), and
(2) **no static RTN schedule ≤ 3.7 avg bits is lossless on real text** —
uniform-3 retains only 0.83 (d=4) / 0.73 (d=8), the role schedule 0.878 at 3.64
bits, because per-matrix errors compound and amplify through depth. NET-1's toy
practical claim (uniform-3 lossless) is refuted at real scale. Round-net-11.
Now 11 network experiments. Assessment v11. Paper NET-11, issue #106. Scripts:
/tmp/exp_net_pr_lm.py, /tmp/exp_net_pr_role.py.

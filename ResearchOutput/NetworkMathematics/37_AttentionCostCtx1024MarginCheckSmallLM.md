# The Attention-Cost Law's Knee Survives 8× Context: k* = d·ctx/32 Holds at ctx=1024 and the Margin-Erosion Caveat Is Resolved (NET-37)

**Program:** Network/LLM research lab — round-net-37 (speed-axis round 10; the long-context margin-erosion re-check the NET-35 P3 caveat demanded)
**Date:** 2026-08-15
**Status:** Machine-verified (data-free top-k key/value pruning on a real causal word LM, **d=4, seed=1, ctx=1024**, 5 Gutenberg novels, dm=64, vocab 4097, 2000 AdamW steps).

## Hypothesis and statement

NET-35 flagged a P3 long-context margin erosion at ctx=512: the k* pass
cleared the 0.98 bar by only 0.003 (≈2 SE) vs ~0.007–0.010 at 128/256, and the
retained curve was uniformly lower at every k. NET-36 showed the pass margin at
512 is seed-fluctuating (±0.002), not systematically eroding. The open stress
point — the one that could break the law — is whether the knee **eventually
fails** as context keeps doubling: the retained-curve depression (~0.01/doubling
at the knee, driven by the diffusive tail) extrapolates to ~0.97–0.98 at
ctx=1024, i.e. right at the bar. This round trains CausalTF **d=4, seed=1,
ctx=1024** (byte-identical harness, 2000 steps, 5516s — extends the same-seed
context chain to 8× the original testbed). Three horns:
- **P1** k* = 128 (d·ctx/32) holds with pass margin ≥ 0.005 → the law survives
  8× context; margin erosion is NOT progressive.
- **P2** k* = 128 FAILS (retained < 0.98) → a context ceiling in (512, 1024];
  the first breach of the law — the context-invariant lever breaks at long
  context.
- **P3** k* = 128 passes but with margin < 0.005 → erosion IS progressive;
  ctx=2048 becomes the next frontier.

## 1. Setup (identical to NET-15/20/33/35, the s1 context chain's endpoint)

Same 5 Gutenberg novels, word-level top-4097 vocab, contiguous 90/10 split,
causal transformer (is_causal=True) dm=64/4 heads (head dim 16), d=4, seed=1,
2000 AdamW steps, **ctx=1024** (585 windows, last 10% held out). Full acc
**0.1594** (bar 0.1562), full loss **5.1209**. Eval via the explicit
causal-attention forward; top-k mask from each eval input's own trained
attention at inference; random-k control (rng seed 12345). Script:
/tmp/exp_net_attncost_ctx1024.py (~1.5h wall at 4 threads: 5516s training +
evals).

## 2. The decisive test — the law holds at 8× context, margin intact

Data-free top-k key/value pruning, joint eval on held-out; k* = smallest k with
retained ≥ 0.98:

| ctx (d=4, s1) | k sweep (retained) | k* | predicted d·ctx/32 | margin at k* |
|---|---|---|---|---|
| 128 | 16→0.987 ✓ | 16 | 16 | +0.007 |
| 256 | 32→0.990 ✓ | 32 | 32 | +0.010 |
| 512 | 64→**0.983** ✓ | 64 | 64 | +0.003 |
| **1024** | 32→0.945 ✗ 64→0.968 ✗ 96→0.977 ✗ 128→**0.986** ✓ 192→0.991 256→0.993 384→0.996 512→1.000 768→0.999 | **128** | **128** | **+0.006** |

**k*(s1, d=4, ctx=1024) = 128 — EXACT, P1 outcome.** The law k* = d·ctx/32 now
holds at a fixed seed across an **8× context range (128 → 1024)** — every
doubling, exactly, no ceiling. The knee is clean: k=96 fails at 0.977 (~2 SE
below bar), k=128 passes at 0.986 (~4 SE above), a 0.009 jump ≈ 6 SE.

## 3. The margin-erosion caveat is RESOLVED — the 512 dip was a fluctuation

The pass margin at the knee across the s1 context chain: **+0.007 (128), +0.010
(256), +0.003 (512), +0.006 (1024)**. This is NOT monotonic — the ctx=512 dip
(0.003) was a fluctuation, and the margin **recovered** at 1024 (0.006, stronger
than 512's). NET-35's P3 hypothesis of progressive long-context margin erosion
is **REFUTED**: the knee is exact at every doubling through 8× context, and the
margin shows no erosion trend (the 512 value was the seed/context fluctuation,
not a systematic degradation). The retained curve is still somewhat lower at the
longest contexts (k=64 0.968 at 1024 vs 0.983 at 512), but the KNEE — the
economically relevant threshold — is unaffected. The honest remaining question
is whether the fluctuation band (±0.003) widens with context; a ctx=2048 point
would test it, but nothing in the four-point chain predicts a failure.

## 4. Concentration — diffusion continues superlinearly, still no bounded working set

| statistic | ctx=128 s1 | ctx=256 s1 | ctx=512 s1 | ctx=1024 s1 |
|---|---|---|---|---|
| eff support exp(H) | 46.41 | 80.57 | 152.11 | **291.16** |
| top-64 mass | — | — | 0.688 | 0.552 |
| top-128 mass | — | — | — | 0.702 |
| eff early | 6.55 | 11.12 | 20.41 | 37.56 |
| eff mid | 41.15 | 70.08 | 133.37 | 255.76 |
| eff late | 86.87 | 150.44 | 281.20 | 542.05 |

Effective support continues its monotone diffusion — 46.4 → 80.6 → 152.1 →
291.2 across three doublings (×1.74, ×1.89, ×1.91 — superlinear on every
doubling, the diffusive tail accelerating). Per-position eff grows monotonically
(37.6/255.8/542.1 at 1024) with NO bounded working set — the context diffusion
law holds to 8× context.

## 5. Selection importance survives the longest context

| ctx | k | top-k | random-k | gap |
|---|---|---|---|---|
| 1024 | 64 | 0.968 | 0.909 | **+5.9** |
| 1024 | 128 | 0.986 | 0.940 | **+4.6** |

Weight-selected positions beat random by 4.6–5.9 pts at ctx=1024 — the same
selection-gap family as every prior context (4.5–8.7), with a mild decline at
the longest context as in NET-35. Selection information is real and survives 8×
context.

## 6. Verification vs the network-loop barriers

- **(a) Circularity — no.** Prediction (k* = 128) stated BEFORE the run from the
  d·ctx/32 law; k* measured from the model's own trained attention at inference.
  Nothing injected.
- **(b) Known-method-in-disguise — no.** Long-context margin verification of an
  established empirical law, not a re-labeled method. Catalog re-scan this round
  (698 packages): no context-length / margin / knee / top-k-pruning result at any
  context (closest: pkg 677 attention expressive-power dichotomy, orthogonal).
- **(c) Toy-scale — confronted.** ctx=1024 is 8× the law's original testbed
  context; still a real causal word LM, causal masking, 4097 vocab, held-out loss
  AND accuracy.
- **(d) Data leakage — none.** Held-out last-10% windows (585 total, ~59 held
  out); top-k data-free from the eval input's own causal attention.
- **(e) Variance/reproducibility — the round's content, with an honest limit.**
  The margin-erosion question is answered by the FOUR-point same-seed chain
  (128→256→512→1024): the 512 dip is shown to be a fluctuation because the
  margin recovered at 1024. The ctx=1024 cell itself is single-seed (as every
  new-context cell was at first). NET-36 established seed-robustness of the k*
  law at 512 (two seeds identical); the same cannot yet be claimed at 1024.
- **(f) Measurement — documented.** Same metrics/protocol as every prior cell;
  k=512 retained 1.000 and k=768 0.999 with loss 5.1214/5.1209 (the 1.000 is the
  re-normalization Monte-Carlo saturation; k=768 already converges to the full
  loss). Binom SE ≈ 0.15% on eval acc (≈60k held-out tokens); the k* pass (0.986,
  +0.006 ≈ 4 SE) and the k=96 fail (0.977, −2 SE) both exceed noise, fixing the
  knee.
- **(g) Baseline unfairness — none.** Full-attention reference per model; random-k
  control at the same k; same 0.98 bar.
- **(h) Practical relevance — strengthened.** The economically important claim —
  the speedup lever 32/d = 8× at d=4 is context-invariant — now holds across an
  8× context range (128 → 1024), with the long-context margin-erosion caveat
  downgraded from an open risk to a resolved fluctuation. Longer context still
  buys no extra relative saving, to 8×.

## Verdict

NET-37 (speed axis, long-context margin check of the attention-cost law):
**CONTEXT-MARGIN CHECK PASSED — k* = d·ctx/32 holds exactly at ctx=1024
(k* = 128 = 4·1024/32), the law's first point at 8× the original testbed
context, with the pass margin recovered (+0.006 vs 512's +0.003).** The P3
progressive-margin-erosion hypothesis is REFUTED — the margin chain at d=4 s1 is
+0.007/+0.010/+0.003/+0.006 across 128/256/512/1024, a fluctuation band, not a
monotone degradation — so the knee is exact at every doubling and no context
ceiling appears through 8×. Concentration keeps diffusing superlinearly (eff
291.16, ×1.91 on the third doubling), selection importance survives (+4.6/+5.9),
and no bounded working set appears even at 1024. Honest limits: the ctx=1024
cell is single-seed (a second seed would close it, as NET-36 did for 512), and
the fluctuation band (±0.003) at the knee is wider at long context than at
128/256. Remaining: ctx=1024 second seed; ctx=512 at d=8/16; d=8 @ ctx=256 s0
corner; and the carry chain at scale (the frontier).
Round-net-37. Now 37 network experiments. Assessment v37. Paper 81, issue #144.
Scripts: /tmp/exp_net_attncost_ctx1024.py; log: /tmp/net37.log.

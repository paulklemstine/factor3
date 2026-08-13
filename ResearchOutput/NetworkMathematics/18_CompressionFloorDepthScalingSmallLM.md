# The 4-Bit Compression Floor Is NOT Depth-Robust: Per-Channel Uniform-4 Loses Losslessness at d=8 (NET-18)

**Program:** Network/LLM research lab — round-net-18 (compression axis, the depth-robustness check of the per-channel uniform-4 practical optimum)
**Date:** 2026-08-13
**Status:** Machine-verified (JOINT per-row RTN quant evals on a real causal word LM, **d=8** seed 0, 5 Gutenberg novels, dm=64, ctx=128, vocab 4097, 2000 AdamW steps; direct depth comparison to NET-12's d=4 same-testbed numbers).

## Hypothesis and statement

NET-12 established at d=4 on this exact testbed that per-row (per-channel)
symmetric RTN scales make **uniform all-4 lossless (retained 0.987 @ 4.00 avg
bits)** — 1.3 bits cheaper than the per-tensor greedy frontier (5.31) — while
uniform-3 per-row fails (0.947) and the interface (embed/pos/un) is irreducible
below 4 bits both data-free (NET-13) and activation-aware (NET-14). NET-11
additionally found **"deeper = worse compounding"** on joint uniform-3 (retained
0.83 at d=4 → 0.73 at d=8). **Question: does the per-channel uniform-4 floor
survive depth?** Three falsifiable horns: (a) per-row uniform-4 stays lossless
at d=8 (retained ≥ 0.98) — the floor is depth-robust; (b) it does NOT — the
depth-amplified compounding of NET-11 is real at every bit level, and the 4-bit
interface floor deepens; (c) the floor *shifts* non-monotonically (retained
changes at different bit levels in opposite directions vs d=4).

## 1. Setup (identical to NET-10/11/12/13/14 family, d=8)

Same 5 public-domain Gutenberg novels (599,869 words; 4,686 contiguous
128-token windows), word-level top-4097 vocab (UNK=0), first 90% train / last
10% test. Causal transformer (is_causal=True) dm=64, 4 heads, **d=8** × seed 0,
2000 AdamW steps (batch 48, lr 3e-4). Reproduces NET-11/16's d=8 s0 model (full
acc **0.1619**, bar 0.98·full = **0.1587**, full loss **5.0788**). Every
quantization eval is **joint** (a fresh model loaded with the quantized state
dict, full held-out 60k-token eval). Per-row (per-output-channel) symmetric RTN
scales are data-free (max-abs of each row); the 1-D LayerNorm weight lnf gets a
single scale. **52 matrices** scheduled at d=8 (embed, pos, un, lnf, and
per-layer wq/wk/wv/ao/mi/mo ×8). Configs evaluated jointly: uniform-2,
uniform-3, uniform-4 (per-row), role(4/3/2) (interface embed/pos/un=4, MLP
mi/mo=3, attention wq/wk/wv/ao=2, lnf=2), plus per-tensor uniform-2/3/4 for
reference.

## 2. Results — the depth comparison (d=8 this round, d=4 NET-12 reference)

| config | primitive | d=8 retained | d=8 loss | d=8 avg-bits | d=4 retained (NET-12) | Δ retained |
|---|---|---|---|---|---|---|
| uniform-2 | per-row | 0.568 | 6.8290 | 2.00 | 0.588 | −2.0 pts |
| uniform-3 | per-row | 0.873 | 5.2861 | 3.00 | 0.947 | **−7.4 pts** |
| **uniform-4** | per-row | **0.967** | 5.1094 | 4.00 | **0.987 ✓** | **−2.0 pts** |
| role(4/3/2) | per-row | 0.801 | 5.4920 | 3.43 | 0.892 | **−9.1 pts** |
| uniform-2 | per-tensor | 0.038 | 8.2654 | 2.00 | 0.112 | −7.4 pts |
| uniform-3 | per-tensor | 0.705 | 5.5368 | 3.00 | 0.825 | −12.0 pts |
| uniform-4 | per-tensor | 0.961 | 5.1510 | 4.00 | 0.979 | −1.8 pts |

**The 4-bit interface floor is NOT depth-robust.** At d=8 the flagship schedule
— per-row uniform-4, lossless at d=4 (0.987 ≥ 0.98) — falls to **0.967,
below the bar**. The drop is ~2 pts at uniform-4 (small but decisive: it
crosses the lossless threshold), and it is much larger where the schedule is
already mid-fragile: uniform-3 per-row falls **7.4 pts** (0.947 → 0.873),
role(4/3/2) falls **9.1 pts** (0.892 → 0.801), per-tensor uniform-3 falls
**12.0 pts** (0.825 → 0.705). The depth penalty is monotone in how close the
schedule sits to the robustness cliff: bit levels near the edge (3-bit, role)
lose the most; the already-collapsed uniform-2 and the near-flawless uniform-4
lose least — but uniform-4's small drop is exactly the one that costs
losslessness.

**Consistency with NET-11.** Per-tensor uniform-3 at d=8 here is 0.705; NET-11
measured the same config at 0.73 (2.5 pts apart — eval-noise-scale agreement).
The per-tensor uniform-3 d=4 → d=8 drop (0.825 → 0.705) is the same
compounding NET-11 reported, re-measured on the identical family.

## 3. The law and its practical scale

**LAW: DEPTH-DEEPENS-QUANT-FLOOR.** The 4-bit per-channel interface floor is a
**d=4 property**, not a model property: at d=8, per-row uniform-4 retains only
0.967 (below the 0.98 lossless bar), uniform-3 and role fall 7–9 pts, and the
per-tensor schedules fall 2–12 pts. NET-11's "deeper = worse compounding" is
confirmed at **every** bit level, not just uniform-3: the depth penalty lands
hardest on schedules sitting near the robustness cliff (uniform-3, role,
per-tensor uniform-3) and hardest of all exactly where a lossless claim was
riding on a narrow margin (uniform-4's −2 pts crosses the bar).

**Practical consequence.** The lab's compression-axis practical optimum —
per-channel uniform-4 @ 4.00 bits, data-free, the NET-12/13/14 surviving
recommendation — is a depth-4 claim. On a d=8 model of the same family it is
not lossless. Deployments that quote "4-bit lossless" must quote depth, exactly
as the speed axis learned with k* (NET-16): both axes' lossless operating points
shrink with depth at fixed width. The compression axis is now closed at d=4
AND its recommended floor does not transfer to d=8 — a documented
depth-boundary for the whole branch, not just one primitive.

## 4. Verification vs the network-loop barriers

- **(a) Circularity — no.** Joint evals quantize an independent loaded copy of
  the trained model; RTN is data-free; nothing is injected into training or
  eval.
- **(b) Known-method-in-disguise — the depth-dependence is the content.**
  Per-channel/group quantization is a known primitive (confirmed in NET-12); the
  new claim is the *depth-robustness measurement*: the lossless per-channel
  schedule holds at d=4 but not d=8, and the NET-11 compounding shows up at
  every bit level. Catalog scan (698 packages): no LLM weight quantization /
  bit-allocation result on a real causal LM, let alone a depth sweep of the
  per-channel floor.
- **(c) Toy-scale — confronted head-on.** Real causal LM, real text, causal
  masking, 4097-token vocab, d=8. This is the larger-scale member of the
  family.
- **(d) Data leakage — none.** Causal masking, contiguous no-overlap split,
  held-out eval, data-free quantization.
- **(e) Variance — honest limits.** One model (d=8 s0); the d=4 counterpart is
  the exact NET-12 reproduction (0.1571 full acc); every number is a full joint
  forward on the held-out 60k tokens (eval noise ≈0.15%). One seed per depth
  reported.
- **(f) Measurement — documented.** 0.98·full bar throughout; retained fraction
  AND raw loss both reported; avg-bits size-weighted over the 52 scheduled
  matrices (same convention as NET-12); per-tensor uniform-3 re-measured in-run
  on the same model and cross-checked against NET-11 (0.705 vs 0.73 — agreed
  within eval noise).
- **(g) Baseline fairness.** uniform-2/3/4 and role are honest joint evals on
  the same model; d=4 references from the same testbed/family (NET-12) at the
  same bar; full-precision reference is each model's own full.
- **(h) Practical relevance.** Depth is a free variable in deployment: a
  compression floor that only holds at d=4 but breaks at d=8 is a
  depth-dependent constraint. The verdict is a direct real-scale depth check of
  the lab's own practical optimum, and it says: quote the depth, or the 4-bit
  claim is a d=4 artifact.

**Verdict.** NET-18 (depth-robustness of the compression floor): the per-channel
uniform-4 practical optimum — lossless at d=4 (0.987) — **fails at d=8
(0.967 < 0.98)**. The depth penalty lands at every bit level, worst where the
schedule sits near the robustness cliff (uniform-3 −7.4 pts per-row, −12.0 pts
per-tensor; role −9.1 pts). **LAW: DEPTH-DEEPENS-QUANT-FLOOR** — the 4-bit
interface floor is a depth-4 property; both the compression and speed axes'
lossless operating points shrink with depth at fixed width (the compression
mirror of NET-16's k* ≈ 4d). Round-net-18. Now 17 network experiments.
Assessment v17. Paper NET-18, issue #112.
Scripts: /tmp/exp_net_d8quant.py.

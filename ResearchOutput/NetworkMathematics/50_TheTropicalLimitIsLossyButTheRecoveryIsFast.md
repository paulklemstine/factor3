# The Tropical Limit Is Lossy but the Recovery Is Fast: on pretrained Qwen2.5-0.5B pure argmax attention (k=1) retains only {0.364, 0.289, 0.250} at ctx = {512, 1024, 2048}, yet k=2 already recovers to ~0.70–0.79 and k=4 to ~0.88–0.91; the knee chain {16, 32, 24} replicates NET-49 EXACTLY (deterministic cross-session reproduction); the Maslov gap (LSE − max) has bulk-layer medians 0.17–1.9 nats with the DIFFUSE TAIL (L22/L23, medians 2.3–2.7) the only far-from-tropical region; crystallization loss Σp(1−p) runs 0.43–0.97 — real attention carries heavy soft mass that is individually tiny but collectively load-bearing (NET-50)

**Program:** Network/LLM research lab — round-net-50 (LIMITED-MEMORY AXIS, iteration 2; mined
from the Lean catalogue's tropical cluster: the Maslov sandwich, softmax→argmax concentration,
and crystallized-attention TV budgets).
**Date:** 2026-08-21
**Status:** Machine-verified (same harness/gates as NET-49: forward validated vs HF eager before
measurement, held-out last 10%, 40 disjoint windows, fp32, GTX 1060; ALL_DONE_NET50, no crash).

## Hypothesis and pre-registered predictions

NET-49 measured lossless knees {16, 32, 24} but stopped above k=16. The catalogue's tropical
results license hard attention within log 2 nats per row (Maslov sandwich) and bound soft-vs-hard
TV distance by crystallization loss Σp(1−p). Three horns stated BEFORE the run:
**P1 TROPICAL-CLIFF** — pure argmax attention (k=1) is catastrophic: retained < 0.5 at every
context (the tropical limit is lossy); **P2 SMALL-K-RECOVERY** — a handful of keys repairs most of
the damage: k=4 ≥ 0.90 retained at ctx=512 AND k=8 ≥ 0.90 at ctx=2048;
**P3 NEAR-TROPICAL-SOFTMAX** — median per-row Maslov gap (LSE − max over causal keys) ≤ log 8 ≈
2.08 nats everywhere AND median crystallization loss ≤ 0.25.

## Results

**Part B — the sub-16 sweep (retained accuracy):**

| k | 512 | 1024 | 2048 |
|---|---|---|---|
| 1 | 0.3637 | 0.2885 | **0.2503** |
| 2 | 0.7865 | 0.7398 | 0.7002 |
| 4 | 0.9097 | 0.8906 | 0.8762 |
| 8 | 0.9617 | 0.9485 | 0.9408 |
| 16 | **0.9834 ✓** | 0.9771 ✗ | 0.9708 ✗ |
| 24 | — | — | **0.9818 ✓** |
| 32 | 0.9931 | **0.9912 ✓** | 0.9867 |

Full acc 0.4460 / 0.4612 / 0.4787; knee chain **{16, 32, 24}** — an EXACT replication of NET-49
by a different script in a different session (deterministic-eval reproducibility confirmed).

**Scorecard: P1 CONFIRMED at all three contexts** (k=1 declines monotonically with context,
0.364 → 0.289 → 0.250 — longer context makes pure argmax WORSE); **P2 CONFIRMED** (k=4@512 =
0.9097, a razor-thin +0.01 clearance; k=8@2048 = 0.9408); **P3 SPLIT** — the Maslov-gap half
holds for the BULK of layers (medians 0.17–1.86 nats ≤ log 8 at 512/1024; at 2048 all bulk
layers ≤ 1.46) but is REFUTED by the diffuse tail: L22/L23 medians reach 2.33/2.16 @512,
2.55/2.37 @1024, **2.69/2.52 @2048 with p90 ≈ 3.4** — and the crystallization half is REFUTED
decisively (per-layer means 0.34–0.97, nothing like ≤ 0.25).

**Part A — tropical budgets per layer:** the Maslov-gap map reproduces NET-49's depth map
independently: L22/L23 are the ONLY far-from-tropical layers, L16 the closest to tropical
(median gap 0.17–0.29). Crystallization loss is HIGH everywhere (bulk 0.43–0.85, tail 0.86–0.97):
real attention rows carry heavy soft mass spread thin — yet top-k to 24 keys retains ≥98%. The
soft tail is therefore INDIVIDUALLY TINY but COLLECTIVELY LOAD-BEARING: each dropped key costs
little, and the aggregate cost stays inside the 2% accuracy budget down to remarkably small k.

## Verdict

THE-TROPICAL-LIMIT-IS-LOSSY-BUT-THE-RECOVERY-IS-FAST — argmax-only attention destroys a real LM
(0.25–0.36 retained, worse at long context), two keys recover ~0.70–0.79, four recover ~0.88–0.91;
the knee chain replicates exactly; and the catalogue's tropical picture needs one correction from
measurement: pretrained softmax attention is near-tropical in its BULK layers (median LSE−max
< 1.9 nats) but carries a genuinely non-tropical two-layer diffuse tail, and its crystallization
loss is large — the practical regime is "tropical plus a thin soft correction", which is exactly
what a small-k oracle (and any future eviction policy) must preserve.

Barriers: (a) clean — horns about the position of the cliff/recovery/budgets stated pre-run;
(b) clean — argmax-limit sweeps + Maslov/crystallization budget measurements on a pretrained LM
are not in Catalog or literature as measured laws; (c) confronted — real-scale pretrained model,
natural text; limit: ONE model; (d) clean — held-out data, data-free selection; (e) SUBSTANCE +
limits — deterministic replication of the NET-49 knee chain cross-session is the round's strongest
reproducibility evidence; P3's crystallization half REFUTED honestly; single model/corpus; (f)
clean — same validation gate (exact forward match), fp32, no crash; (g) fair — full reference +
same bar; controls inherited from NET-49 (random-k/local-window dominated there; not re-run here —
noted); (h) DIRECT — the k↦retained curve below k=16 is the deployment-relevant region for
aggressive KV compression; the fast recovery from k=1 to k=8 says pointer-style caches have a
quantified path between the extremes.
Open: per-layer pruning ablation (does quantizing/pruning ONLY the L22/L23 tail close the
remaining gap?); size transfer; oracle-to-policy gap; corpus robustness; weight quantization
(NET-52 next). Paper 135, issue #237. Now 50 network experiments. Assessment v50.

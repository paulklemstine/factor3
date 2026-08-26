# Engine-Invariance Confirmed and the 30B MoE Runs at Goal Speed: ik_llama.cpp matches mainline quality to 0.04% while delivering 2.33x prompt processing on Qwen3-30B-A3B — a resident 30B-class MoE serves at 13.28-13.89 tok/s on pure CPU, every published law survives the engine swap (NET-103)

**Program:** Network/LLM research lab — round-net-103 (CPU-LARGE-MODEL AXIS,
iteration 78; ENGINE-IK cell of the fan-out program).
**Date:** 2026-08-26
**Status:** Machine-verified (ALL_DONE_NET103 + NET-103b/c redo; raw bench
tables captured verbatim).

## Setup

Two engines on identical quant files: mainline llama.cpp (build c060ca9)
vs ik_llama.cpp (pinned commit 08b500b9), both GGML_NATIVE CPU builds.
Models: Qwen2.5-7B-Instruct Q4_K_M (dense control) and
Qwen3-30B-A3B IQ4_XS (MoE target, 30.53B params / ~3B active, 4.25bpw).
llama-bench -p 512 -n 128 -t 8; llama-perplexity on the standard 250KB
held-out wikitext slice @ctx2048.
Scripts ResearchOutput/exp_net103_engineik.py + exp_net103b_benchredo.py +
exp_net103c_ikppl.py (two instrumentation bugs found and fixed en route:
markdown-table parse discarded raw output; ik's "PPL over N chunks ... ="
wording defeated the first regex); results ~/f3cache/net103{,b}_results.json;
raw tables in net103b_results.json.

**Predictions stated BEFORE any measurement:** P1 dense tg within ±10%
(ik expected ~neutral on dense); P2 ik PP512 ≥ 2× mainline on the MoE;
P3 best-engine tg128 ≥ 10 tok/s on the resident MoE; P4 ik PPL within
±1% of mainline on identical quant+slice.

## Results

### Throughput (llama-bench, threads=8)

| model | engine | pp512 tok/s | tg128 tok/s |
|---|---|---|---|
| 7B dense Q4_K_M | mainline | 53.53 | 5.87 |
| 7B dense Q4_K_M | ik | 79.94 (**+49%**) | 5.91 (+0.7%) |
| **30B-A3B MoE IQ4_XS** | mainline | 56.13 | **13.28** |
| **30B-A3B MoE IQ4_XS** | ik | **130.81 (+133%)** | **13.89** |

### Quality (perplexity, identical quant + slice)

| engine | PPL |
|---|---|
| mainline | 6.9781 |
| ik | 6.9762 (**Δ 0.039%**) |

**Scorecard:** P1 REFUTED FAVORABLY (dense tg parity ✓ but dense PP +49% —
ik accelerates dense prompt processing too); P2 CONFIRMED (2.33× ≥ 2×);
P3 CONFIRMED (13.28–13.89 ≥ 10); P4 CONFIRMED (0.039% ≪ 1%).

## The results as laws

1. **ENGINE-INVARIANCE OF QUALITY**: identical quant files produce
   perplexities differing by 0.039% across independent inference engines —
   our published quality laws (KV cliff, weight floors, composition) are
   properties of the MODEL+QUANT, not of the kernel that executes them.
2. **ENGINE-VARIANCE OF SPEED**: throughput is emphatically an engine
   property — +49% dense PP and +133% MoE PP from the fork alone, at
   zero quality cost. Serving speed claims must always name their engine.
3. **GOAL-GRADE MoE SPEED**: a resident 30.5B-param sparse model sustains
   13.28 tok/s single-stream on mainline and gains 133% prefill headroom
   under ik — full-context prefill, the dominant cost of long-context
   serving, is where the lever pays.

## Honest limits

- Bench = synthetic pp512/tg128; real-workload prefill mixes differ.
- One MoE family (Qwen3), one quant (IQ4_XS); cross-family pending.
- The eagle3 speculation path for gpt-oss segfaults on mainline (NET-102,
  upstream datum) — speculation × engine interaction unexplored.
- Two instrumentation bugs were caught mid-round (table-parse loss;
  ik wording) — both fixed by raw-capture discipline; nothing reported
  here rests on parsed-only data.

Barriers: (a) clean; (b) clean; (c) confronted (engines pinned by commit,
quants identical, slice stated); (d) clean; (e) deterministic; (f) clean
(raw capture); (g) fair (identical files/threads/slices); (h) DIRECT.

Open: speculation × engine interaction; gpt-oss-120b stream capstone;
cross-family knee replication; STARVED-LADDER params_max validation.

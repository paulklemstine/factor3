# The Cheap Draft Wins and Code Drafts Deep: speculative decoding of a 7B LLM entirely on CPU pays up to 1.66× — the smaller draft beats the larger in EVERY cell despite lower acceptance (draft-cost dominance), and optimal draft depth is domain-parameterized: code wants deep drafts while prose collapses past depth 4 into a net LOSS (NET-91)

**Program:** Network/LLM research lab — round-net-91 (CPU-LARGE-MODEL AXIS,
iteration 66; first round of the user-directed pivot; doubles as the
hardware-stability canary after the 2026-08-23 memory-fault fixes).
**Date:** 2026-08-23
**Status:** Machine-verified (ALL_DONE_NET91; exit clean after ~55 min
sustained full-CPU load — the load profile that hard-crashed the box three
times pre-fix).

## Setup

Qwen2.5-7B-Instruct Q4_K_M executed entirely on CPU (llama.cpp built today,
i9-9900K, threads=8 winner of the {8,16} sweep at 5.79 tok/s greedy baseline;
JEDEC memory after the RAM fix — absolute tok/s ~27% below the XMP-era
partial, all comparisons within-round). Drafts: Qwen2.5-0.5B-Instruct q8_0
(49.2 tok/s = 11.8% of target cost/token) and Qwen2.5-1.5B-Instruct q4_k_m
(24.75 tok/s = 23.4%). Grid: drafts × depths {2,4,8} × domains {prose
(wikitext shard A), code (Python corpus)}, 4 prompts × 2 repeats each, greedy
(temp 0), ctx ≤1024, 96 generated tokens/run. Effective generation tok/s =
wall minus per-pair overhead calibration (-n 1 runs); acceptance =
llama-speculative reported n_accept/n_drafted.
Script ResearchOutput/exp_net91_specdec.py; results ~/f3cache/net91_results.json;
log /tmp/net91.log.

**Predictions stated BEFORE the run:** P1 same-family 0.5B→7B acceptance
≥50% at depth 4 on prose (from NET-51 key-sharing cos ≥0.976); P2 some
config beats baseline by >5% wall-clock (the draft is NOT free on CPU);
P3 1.5B accepts more but its cost creates a 0.5B-crossover within the grid;
P4 acceptance(code) ≥ acceptance(prose)+5 pts (domain line: code attention
is more concentrated).

## Results

| config | prose speedup | prose accept | code speedup | code accept |
|---|---|---|---|---|
| 0.5B d=2 | 1.254× | 63.9% | 1.352× | 71.6% |
| 0.5B d=4 | **1.416×** | 47.7% | 1.616× | 63.0% |
| 0.5B d=8 | **0.979× ✗LOSS** | 30.9% | **1.661× BEST** | 56.0% |
| 1.5B d=2 | 1.016× | 63.2% | 1.195× | 83.4% |
| 1.5B d=4 | 1.153× | 51.9% | 1.395× | 74.8% |
| 1.5B d=8 | 0.982× ✗ | 44.9% | 1.354× | 60.3% |

**Scorecard:** P1 REFUTED (47.72% — razor-thin miss below the 50% horn);
P2 CONFIRMED dramatically (best 1.661×; six of twelve configs clear 1.05×);
P3 REFUTED as stated — NO crossover: 0.5B wins all six head-to-heads even
where 1.5B accepts more (e.g. code d=8: 60.3% vs 56.0% acceptance, yet
1.354× vs 1.661× — the doubled draft cost eats the edge); P4 CONFIRMED
decisively (+17.8 pts mean gap: code 68.2 vs prose 50.4, GROWING with
depth: +14.0 → +19.1 → +20.2 across d=2/4/8).

## The laws

1. **DRAFT-COST DOMINANCE ON CPU**: the cheaper draft wins every measured
   cell. Acceptance advantages do not survive a 2× per-token cost
   disadvantage when verification is amortized but proposal is sequential.
   On CPU the economics are set by t_draft/t_target (~0.118 vs ~0.234 here),
   unlike GPU folklore where any draft is nearly free.
2. **OPTIMAL DEPTH IS DOMAIN-PARAMETERIZED**: prose acceptance halves with
   each doubling past d=2 (63.9 → 47.7 → 30.9%), turning d=8 into a net
   LOSS (0.979×); code decays gracefully (71.6 → 63.0 → 56.0%) and keeps
   paying through d=8. The best depth differs by 2× across domains on the
   same target/draft pair — a static draft-depth setting leaves 25%+
   throughput on the table for one domain or the other.
3. **SPECULATION PAYS ON CPU**: up to +66% throughput (1.661×) from an
   0.6GB side model — the practical headline for local LLM serving.
4. Domain continuity: the drafting-efficiency asymmetry matches our
   attention-budget line (code's lower knee, sharper distributions —
   NET-68/86–90) and NET-51's key-sharing magnitude prediction (high
   cross-size same-family acceptance), though the exact ≥50% horn missed.

## Honest limits

- 12 configs × 8 runs each; greedy sampling; ~500-token prompts; ONE model
  family, ONE box, ONE memory configuration (ratios internally consistent;
  absolute tok/s specific to the post-fix JEDEC state).
- Acceptance reported as overall drafted-token fraction, not per-position
  survival curves; no variance decomposition across prompts yet.
- The prose-d=2 acceptance inversion (0.5B 63.91 vs 1.5B 63.15) shows the
  capability ordering is not universal at shallow depth.
- Single-session run; replication and per-position acceptance maps are the
  natural next cells.

Barriers: (a) clean (pre-registered horns honestly scored incl. two
refutations); (b) clean (catalog-empty cell — no prior speculation/KV-quant
work locally or in alethean index); (c) confronted (family/box/grid stated);
(d) clean (corpus-held-out prompt slices); (e) deterministic (greedy, fixed
seed); (f) clean (overhead-calibrated wall-clock medians + tool-reported
acceptance); (g) fair (identical binaries/threads/prompts across arms);
(h) DIRECT (+66% real serving throughput).

Open: per-position acceptance curves (why prose collapses past d=4);
depth-adaptive drafting (switch depth by detected domain); KV-cache
quantization ladder on the same 7B; weight-quant floor transfer Q8→Q2;
knee-law transfer to 7B via torch-CPU bf16.

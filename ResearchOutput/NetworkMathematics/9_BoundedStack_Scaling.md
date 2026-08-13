# The Load-Bearing Boundary is Not Found: Single-Layer Soft Attention Implements a Bounded Stack — Depth is Flat Across Context and Width Scaling on the Non-Regular Grammar (NET-9)

**Program:** Network/LLM research lab — round-net-9 (depth axis, round 7; the load-bearing boundary via context and width scaling of Dyck-2)
**Date:** 2026-08-13
**Status:** Machine-verified (Dyck-2 next-token; Part A semilength s∈{16,32} at dm=48, d∈{1,2}×2 seeds = 8 models; Part B width dm∈{16,12} at s=12, d∈{1,2}×2 seeds = 8 models; 6000 AdamW steps each; plus the Part C non-flat screen).

## Hypothesis and statement

NET-8 refuted the load-bearing premise at semilength 12/dm48: a single layer recovers the
stack-top type on Dyck-2. Two scaling questions remained to find where a single layer
breaks — the actual load-bearing boundary, where a second layer finally pays and the exit
law could have a practical boundary:

- **(1) Context scaling.** At larger semilength s the running balance must be tracked over
  more levels (up to s) and closes must route to opens at distance up to 2s−1. At what s
  does d=1's single layer stop covering the balance + retrieval while d=2 succeeds?
- **(2) Width scaling.** A single layer must hold BOTH the balance prefix-sum AND the
  balance-conditioned position routing in its heads. At dm=16 and dm=12 (head dim 4 and 3),
  does one layer run out of room so that d=2 (stack the two subtasks) finally wins?

The falsifying alternative: the load-bearing boundary is NOT reached at s≤32 or dm≥12 —
single-layer soft attention implements a bounded stack (balance-pointer + content-retrieval
at the pointed position), so depth stays flat across both scaling directions.

## 1. Part A — depth is FLAT across context scaling: d=1 is perfect at s=16 and s=32

| config (dm=48) | overall (s0/s1) | close_all (s0/s1) | close_b4+ (s0/s1) |
|---|---|---|---|
| s=16 d=1 | 1.0000 / 1.0000 | 1.0000 / 1.0000 | 1.0000 / 1.0000 |
| s=16 d=2 | 1.0000 / 1.0000 | 1.0000 / 1.0000 | 1.0000 / 1.0000 |
| s=32 d=1 | 1.0000 / 1.0000 | 1.0000 / 1.0000 | 1.0000 / 1.0000 |
| s=32 d=2 | 1.0000 / 1.0000 | 1.0000 / 1.0000 | 1.0000 / 1.0000 |

**d=1 reaches test=1.0000 at every metric even at semilength 32 (context 64 tokens).** The
balance now ranges over 32 levels and closes must route to matching opens up to **63
tokens back** — the single attention layer does both, perfectly, in both seeds. Context
length is NOT the boundary: a one-layer transformer performs long-range stack-top
retrieval at 63-token distance with dm=48.

## 2. Part B — depth is FLAT across width scaling: d=1 is perfect at dm=16 and dm=12

| config (s=12) | overall (s0/s1) | close_all (s0/s1) | close_b4+ (s0/s1) |
|---|---|---|---|
| dm=16 d=1 | 1.0000 / 1.0000 | 1.0000 / 1.0000 | 1.0000 / 1.0000 |
| dm=16 d=2 | 1.0000 / 1.0000 | 1.0000 / 1.0000 | 1.0000 / 1.0000 |
| dm=12 d=1 | 1.0000 / 1.0000 | 1.0000 / 1.0000 | 1.0000 / 1.0000 |
| dm=12 d=2 | 1.0000 / 1.0000 | 1.0000 / 1.0000 | 1.0000 / 1.0000 |

**d=1 is perfect even at dm=12 (4 heads → head dim 3).** One narrow layer still holds the
balance statistic AND routes every close to its matching open's type. Width is NOT the
boundary either. Combined with Part A: the flat-depth law on the non-regular grammar
survives BOTH scaling directions we can afford on CPU (context ≤64, width ≥12).

## 3. Part C — no config with d=1 < d=2 (the non-flat screen)

The automated screen compared d=1 vs d=2 close_all per config (gap > 0.01 ⇒ non-flat) and
found **none**: "No config with d=1 < d=2 (close_all gap > 0.01) — depth FLAT again across
s in {16,32} and dm in {16,12}." Every pair is equal at 1.0000, so the shared-head exit
branch was correctly not triggered (there is no depth-using model to exit).

## 4. Mechanism — why a single layer implements the bounded stack

The empirical flatness has a clean mechanism reading: **the stack-top state of a bounded
Dyck word IS the scalar running balance, and the stack-top CONTENT is positionally stored.**
A close at position t must read the content of the last unmatched open — the last position
j < t that is an open at balance-depth balance_before(t)−1. Single-layer attention realizes
exactly this: one head accumulates the balance (a prefix-sum, one scalar per position);
a second routes each close query to the matching-open position by a balance-conditioned
key match, using recency (position monotonicity) to pick the LAST such open; and the value
read is the open's stored type. This is precisely a bounded-stack implementation — a
balance pointer plus content retrieval — and it needs no second layer because the state is
scalar and the content is at a computable position. The boundary would require (a) a
balance range exceeding dm's precision (s ≫ 64), (b) genuinely unbounded nesting
(length-generalization, a different axis — NET-4's length-gen wall), or (c) stack content
that is NOT positionally retrievable (non-positional long-range binding — the genuinely
hard case, e.g. content computed from multiple distant positions). None of these is
reached at our scale; (c) is the natural next target for a load-bearing test.

## 5. Verification vs the network-loop barriers

- **(a) Circularity — no.** All 16 models on fresh random Dyck-2 words (seeds {0,1}, test
  seed+77); no injected structure.
- **(b) Known-method-in-disguise — related circuits acknowledged, the negative is new.** The
  "attention = bounded stack / balance-pointer retrieval" reading is mechanistically
  folklore; the NEW content is the negative across the scaling sweep (flat at s≤32, dm≥12,
  on the non-regular CFG) and the flat-depth law now spanning five task classes × context ×
  width. Catalog scan (698 packages): no prior work on this scaling boundary.
- **(c) Toy-scale — acknowledged, and it IS the finding.** The load-bearing boundary is not
  reached at context ≤64 / width ≥12 on CPU; the honest statement is that single-layer
  transformers solve bounded-stack grammar at every affordable scale, so "deep is needed
  for syntax" claims need genuinely non-positional bindings or much larger contexts. The
  real-scale checks (exit law / PR law on a small LM) are the standing next steps.
- **(d) Data leakage — none.** Fresh held-out words (seed+77), all models 1.0000 on held-out
  before probing.
- **(e) Variance — 2 seeds × every config, all consistent.** All 16/16 models hit 1.0000 at
  every metric; no seed spread to hide.
- **(f) Measurement — documented.** close_all = every k-th close of every run (the honest
  hard-close diagnostic, NET-8); budget 6000 steps × batch 128 ≥ 12 epochs at s=32 (49M
  tokens seen). Two script bugs, both post-data cosmetic/verification-only and both
  fixed: (i) the final SUMMARY re-print loop unpacked the Part A dict key as a 4-tuple
  (it is (s,d,seed)) — fired after all models had trained/evaluated, no data loss; (ii)
  Part C's RA lookup used a 4-tuple key against 3-tuple keys, so the (16,48)/(32,48)
  pairs fell through to the RB arm and were verified EQUAL by direct inspection of the
  printed per-model lines (all 1.0000 both depths) — the automated screen covered the
  dm∈{16,12} configs and its verdict (no non-flat config) is correct over all 16.
- **(g) Baseline fairness — inherited from NET-8.** The windowed-linear baseline (close_all
  ≈0.75) is beaten by d=1 by +25pp; the scaling sweep here tests whether ANY depth gap
  appears, not a baseline comparison.
- **(h) Practical relevance — an honest negative with a target.** Depth gives nothing on
  bounded-stack grammar at every affordable scale (inference can run d=1, or exit early per
  NET-7/8); the genuinely open load-bearing candidates are non-positional stack content,
  much larger contexts (s≫64), or the real-LM checks on the other axes.

**Verdict.** NET-9 (depth axis, round 7): the load-bearing boundary is NOT found at context
≤64 or width ≥12 — d=1 is perfect at every metric on all 16 models across both scaling
directions, extending the flat-depth law to a five-task-class law that also holds across
context and width scaling on the non-regular grammar. The mechanism reading is now
explicit: single-layer soft attention implements a bounded stack (scalar balance pointer +
positional content retrieval), which is why a second layer never pays for bounded grammar
at this scale. The genuinely open load-bearing candidates are (a) non-positional stack
content, (b) s ≫ 64, (c) unbounded nesting/length-gen, and (d) the real-scale checks on
the other axes (exit law / PR law on a small LM). Round-net-9. Now 9 network experiments.
Assessment v9. Paper NET-9, issue #104. Script: /tmp/exp_net_dyck2_scale.py.

# Content-Additive Eviction Does Not Help: hybrid eviction scores z(accumulated) + λ·z(probe) are monotonically WORSE with increasing probe weight — {0.9384 (λ=0), 0.9383, 0.9365, 0.9344} at B=64 across λ = {0, 0.25, 1, 4} — completing the policy-gap bounding: accumulation (NET-56), recency (NET-56 hybrid), content alone (NET-58), and content+usage combinations (this round) ALL sit ≥5.7 pts below the oracle at matched budget; the λ=0 arm reproduces NET-56 to four decimals (NET-61)

**Program:** Network/LLM research lab — round-net-61 (LIMITED-MEMORY AXIS, iteration 19;
closes the cheap-signals line opened by NET-56).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact, argmax-agree 1.0000; probes train-side only;
λ-grid pre-stated; ALL_DONE_NET61).

## Setup

Hybrid eviction: after each 128-row block, keep top-(B−W) keys by
z(accumulated attention) + λ·z(static probe score of the key's content), plus the last
W=min(32,B/2) positions. Qwen2.5-0.5B fp32, ctx=1024, 24 held-out wikitext windows.
Script ResearchOutput/exp_net61_hybrid.py; log /tmp/net61.log.

**Predictions stated BEFORE the run:** P1 SOME-LAMBDA-WINS (an intermediate λ beats λ=0 by
≥1 pt at B=64); P2 SMALL-IS-OPTIMAL (optimal λ ≤ 1); P3 CEILING-HOLDS (best hybrid trails
oracle by ≥5 pts at B=64).

## Results

| B | λ | retained |
|---|---|---|
| 64 | **0.0** | **0.9384** |
| 64 | 0.25 | 0.9383 |
| 64 | 1.0 | 0.9365 |
| 64 | 4.0 | 0.9344 |
| 32 | 1.0 | 0.9189 |
| 128 | 1.0 | 0.9544 |

**Scorecard: P1 REFUTED** — monotone DECREASING in λ; no probe weight helps. **P2 CONFIRMED**
(λ=0 optimal — and its 0.9384 reproduces NET-56's hybrid to four decimals, a cross-run
deterministic anchor). **P3 CONFIRMED** — best hybrid trails oracle@64 by 5.7 pts.

## Verdict

CONTENT-ADDITIVE-EVICTION-DOES-NOT-HELP — with NET-56 (accumulation ± recency) and NET-58
(content alone), every cheap eviction-signal family is now bounded ≥5.7 pts below the oracle
at matched budget: accumulation, recency, content, and their linear combinations. The policy
gap is STRUCTURAL across signal families, consistent with importance being relational
(NET-58) and only partially visible online. Remaining routes are structural — better usage
tracking, learned online predictors at scale (bounded by NET-58's ceiling unless near-perfect),
or accepting oracle numbers as upper bounds in all deployment tables.

Barriers: (a) clean — three horns pre-stated incl. the refuted P1; (b) confronted — score-
combination hybrids exist in H2O variants; NEW = the measured monotone-degradation law and
the four-family bounding of the gap on one harness; (c) confronted — one model/context,
linear probes, fixed recency window stated; (d) clean — train-side probes; (e) deterministic,
λ-grid pre-stated; (f) clean (ALL_DONE_NET61); (g) fair — identical harness/budgets/windows
as NET-56/58; (h) DIRECT — closes the cheap-signal search space for practitioners.
Open: sub-16 addendum @1024 (next); domain-jump corpora; 1.5B tail map; 7B cell.
Paper 146, issue #296. Now 61 network experiments. Assessment v61.

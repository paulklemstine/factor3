# The Oracle Overstates the Deployable Win: a causally-honest streaming KV policy (accumulated-score heavy-hitters, block-128) retains only {0.863, 0.882, 0.919} at budgets {32, 64, 128} where the omniscient oracle posts {0.991, 0.995} at {32, 64} — an 11-point gap at matched budget; recency helps (+4–6 pts, the fixed hybrid) but even a 128-key cache (12.5% of context) reaches only 0.961 — the knee collapse of NET-49/55 is real for hindsight but does NOT transfer to online eviction: trained attention is prunable in retrospect, not predictable in advance (NET-56)

**Program:** Network/LLM research lab — round-net-56 (LIMITED-MEMORY AXIS, iteration 9; cell (4)
of the catalogue mining queue: oracle-to-policy gap).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact: own forward == HF forward, argmax-agree 1.0000; oracle
arms cross-replicate NET-49's knee to four decimals — 0.9913 at B=32 vs NET-49's 0.9912 at k=32;
all streaming arms inside the (0,1) sanity band with monotone budget response; ALL_DONE_NET56).

## Setup

Qwen2.5-0.5B fp32, ctx=1024, 24 held-out wikitext windows. Streaming policy: process rows in
blocks of 128; after each block, per layer/head keep the top-(B−W) keys by ACCUMULATED
attention probability received so far, plus always the last W=min(32, B/2) positions (hybrid)
or pure top-B (HH); the current block is always fully cached (faithful server semantics);
strict per-row causal masking including self. Budgets B ∈ {32, 64, 128} = {3.1%, 6.3%, 12.5%}
of context. Script ResearchOutput/exp_net56_policy.py (committed); log /tmp/net56.log.

**Predictions stated BEFORE the run:** P1 POLICY-GAP-IS-REAL (streaming ≥2% below oracle at
matched B=64); P2 RECENCY-MATTERS (HYB > HH at same B); P3 STILL-LARGE-WIN (best policy at
B=64 ≥ 0.95 while touching ≤12% of KV).

## Results

| arm | B=32 | B=64 | B=128 |
|---|---|---|---|
| ORACLE (per-row top-k) | **0.9913 ✓** | **0.9953 ✓** | — |
| HH (accumulated, pure) | 0.8633 | 0.8822 | 0.9189 |
| HYB (HH + recency) | 0.9205 | 0.9384 | 0.9605 |
| (full reference) | 0.4627 acc | | |

**Scorecard: P1 CONFIRMED emphatically** — the gap is 11.3 points at B=64 (0.882 vs 0.995), not
the ≥2% floor; even at B=128 the best policy sits below the oracle at B=32. **P2 CONFIRMED** —
recency adds +5.7/+5.6/+4.2 points at every budget. **P3 REFUTED** — best-at-64 = 0.938 < 0.95;
the deployable win at honest budgets is bounded by ~0.94–0.96, roughly the NET-50 recovery
curve's k≈8–16 region, not the oracle's k≈32.

## Verdict

THE-ORACLE-OVERSTATES-THE-DEPLOYABLE-WIN — the programme's knee laws measure what an omniscient
selector can do; a causally-honest accumulator pays ~7–11 accuracy points at matched budgets,
and recency — not accumulated mass — is the cheaper signal (the fixed hybrid dominates pure HH
everywhere). The concentration structure that makes trained attention prunable IN RETROSPECT
does not make it PREDICTABLE ONLINE: accumulated attention is a biased estimator of future
importance, exactly the gap the catalogue's min-plus decoder-reliability theorems anticipate
(no exponential-reliability bound without assumptions). Deployment reading for the 6 GB host:
budget ~B=128 (12.5%) with the hybrid policy for ≥0.96 retained, or accept oracle-only claims
as upper bounds; the honest serving table is policy-adjusted, not oracle-quoted.

Barriers: (a) clean — three horns pre-stated incl. the refuted P3; (b) confronted — H2O/
heavy-hitter literature exists; NEW content = the oracle-to-policy gap QUANTIFIED on the same
harness that measured the knees (matched protocol, exact oracle replication as anchor) + the
recency-dominates-accumulation ordering; (c) confronted — real model, natural text; limits:
ONE model, ONE context, block-128 policy granularity, no learned importance heads; (d) clean —
held-out data, no training; (e) deterministic; SEVEN implementation variants were caught and
rejected by sanity gates before recording (scatter/gather shape bugs; stale kept-set starving
local context → 0.35–0.46; per-block causal leak → retained 2.06 > 1 impossible; strict-mask
NaN; duplicate recency; unbound variable) — the two invalid variants are retained in git
history as bracketing negative controls, and the recorded run passes retained∈(0,1) + monotone
budget response + exact oracle replication; (f) clean (ALL_DONE_NET56); (g) fair — oracle
anchor on the identical harness/data, budgets matched exactly; (h) DIRECT — this IS the
deployment table's policy adjustment.
Open: learned importance heads (can a tiny predictor close the gap?); per-layer budgets
(tail layers may need more); 1.5B replication; block-size sensitivity; corpus robustness
(next cell). Paper 141, issue #287. Now 56 network experiments. Assessment v56.

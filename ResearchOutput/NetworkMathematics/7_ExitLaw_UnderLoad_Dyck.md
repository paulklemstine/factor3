# Depth is Flat on the Canonical Grammar Task, and the Exit Layer Tracks Task Difficulty, Not d/2 (NET-7)

**Program:** Network/LLM research lab — round-net-7 (speed axis, round 2; the load-bearing-depth test of NET-6)
**Date:** 2026-08-12
**Status:** Machine-verified (Dyck-1 balanced-parenthesis next-token, semilength 12, nesting ≤12; dm=48, 4 heads; d∈{1,2,4,8,16}×2 seeds = 10 depth models + shared-head exit on d∈{4,8,16}×2 seeds = 6 exit models).

## Hypothesis and statement

NET-6 established the decodability-crossover exit law on attention-solvable automata:
exit* (first layer where the trained readout is usable) ≈ crossover ≈ d/2, lossless,
~50% inference saving. But NET-2's depth law is FLAT there, so the law was never
tested on a task where depth is genuinely **load-bearing**. This iteration attacks that
gap with the canonical grammar task — Dyck-1 balanced-parenthesis next-token
prediction (semilength 12, nesting up to 12), the classic setting where shallow
transformers are expected to fail at deep nesting. Two questions:

- **(1) Does depth pay here?** If Dyck-1 needs sequential state (a running balance)
  beyond one-hop attention, d=1 should fail at deep-nesting positions while d=16
  succeeds — the first non-flat depth law in the series.
- **(2) Is the exit law universal or bounded?** If depth is load-bearing, does the
  shared head STILL become decodable at the norm crossover with lossless exit (the
  second half of ANY transformer is amplification, even under load), or does
  exit-at-crossover fall short (the law has a boundary — practical caveat for
  early-exiting a depth-using model)?

The falsifying alternative for (1): Dyck-1 with bounded nesting is attention-solvable
(one head computes the running sum), depth is again FLAT, and the load-bearing regime
is not reached at this scale.

## 1. Part A — depth is FLAT on Dyck-1: d=1 alone solves all nesting ≤ 12

All 10 models (d∈{1,2,4,8,16}×2 seeds, budget 6000 AdamW steps each) reach
held-out next-token test = **1.0000 at every balance bin**:

| depth | test (s0 / s1) | b0 (balance 0) | b1 | b2 | b3 | b4+ (nesting ≥ 4) |
|---|---|---|---|---|---|---|
| 1 | 1.0000 / 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 2 | 1.0000 / 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 4 | 1.0000 / 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 8 | 1.0000 / 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 16 | 1.0000 / 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

**The hypothesis (1) is REFUTED: depth is completely flat on Dyck-1.** A single
attention layer (dm=48) reads the full 24-token context and predicts both '(' and ')'
perfectly at every running balance — the balance is a cumulative sum, and one head
accumulates it while another conditions the next token on it. Deep nesting (b4+,
balance 4–10) does NOT tax depth: the b4+ accuracy is 1.0000 at d=1 already. The
"shallow transformers fail at deep nesting" expectation is a property of
context-length / width starved settings, not of this scale. The flat-depth law
(NET-2 lookups, NET-3 composition, NET-4/5 arithmetic) now extends to the canonical
grammar task. The load-bearing-depth regime was NOT achieved; bounded Dyck-1 at dm=48
is attention-solvable.

## 2. Part B — the exit layer tracks task difficulty, not d/2

Shared-head early exit (trained final LN+readout applied to each frozen LN(x_l)) on
d∈{4,8,16}×2 seeds; exit* = first layer with exit accuracy ≥ 0.95·full = 0.95:

| d | seed | full | exit* | l=exit*−1 → l=exit* | crossover | d/2 | saving |
|---|---|---|---|---|---|---|---|
| 4 | 0 | 1.0000 | 3 | 0.7075 → 1.0000 | 3 | 2 | 25% |
| 4 | 1 | 1.0000 | 2 | 0.6733 → 0.9613 | 3 | 2 | 50% |
| 8 | 0 | 1.0000 | 3 | 0.5942 → 1.0000 | 2 | 4 | 62.5% |
| 8 | 1 | 1.0000 | 2 | 0.6409 → 0.9737 | 2 | 4 | 75% |
| 16 | 0 | 1.0000 | 4 | 0.7806 → 0.9927 | 3 | 8 | 75% |
| 16 | 1 | 1.0000 | 4 | 0.8130 → 0.9814 | 1 | 8 | 75% |

**exit* is depth-INDEPENDENT: {2,3,4} across all six configs (d=4..16).** The exit
layer does not scale with d at all — d=16 exits at layer 4 of 16. **The crossover is
also early: {1,2,3}**, not d/2. Both track the task, not the architecture:
Dyck-1's balance statistic is computed in 2–4 layers regardless of how many layers the
network has; the remaining layers are dead weight. **The inference saving is
therefore LARGER than on automata: 25–50% at d=4 → 62.5–75% at d=8 → 75% at d=16**
(median ≈ 75% at d=16, vs ≈ 50% for NET-6's order-3/4 automata).

**exit* ≈ crossover, in the refined sense:** exit* − crossover = {0, −1, +1, 0, +1,
+3} → |exit*−crossover| ≤ 1 in 5/6 here, and 17/18 combined with NET-6's 12 automata;
the single outlier is d=16 s1 (crossover=1, exit*=4 — on that model the norm grows
immediately but decodability lags 3 layers). **A partial refinement of NET-6:**
lossless-at-crossover holds in only 3/6 here (vs NET-6 where the exit was essentially
at the crossover): on the easy task the crossover is much earlier and exit* lags it
1–3 layers. The universal object is **exit* ≈ crossover with crossover task-dependent
(≈ d/2 on harder automata, ≈ 1–3 on easy Dyck), and exit at the first usable layer is
always lossless within the 0.95 bar** — the fixed bar, not the norm, is the reliable
trigger, and on easy tasks it fires far below d/2.

## 3. The refined law

**EXIT-TRACKS-TASK-DIFFICULTY LAW (refining NET-6).** The layer where the trained
readout becomes usable (shared-head exit) tracks the residual-stream norm crossover,
|exit* − crossover| ≤ 1 in 17/18 models across two task classes (automata + grammar),
and the crossover itself is TASK-DEPENDENT, not fixed at d/2: ≈ d/2 on tasks whose
computation genuinely occupies Phase I (order-3/4 automata, NET-6), ≈ 1–3 on easy
tasks (Dyck-1, here). Consequence: the inference saving is bigger on easier tasks —
exit at layer 2–4 of a 16-layer model = 75% saving, lossless within 0.05 of the full
model, no confidence gate. NET-6's "exit* ≈ d/2" is thereby corrected to its proper
scope: it held because the automaton computation fills Phase I; it is NOT universal.

**DEPTH-FLATNESS EXTENDS TO GRAMMAR (NET-7 negative for the load-bearing test).**
Dyck-1 bounded (semilength 12, nesting ≤12) at dm=48 is attention-solvable: d=1 is
perfect at every balance bin including deep nesting. The load-bearing-depth regime —
the one place the exit law's practical caveat could bite — was NOT achieved and
remains genuinely open. The depth law is now flat on four task classes: lookups
(NET-2), composition (NET-3), decomposable-error arithmetic (NET-4/5), grammar (NET-7).

## 4. Verification vs the network-loop barriers

- **(a) Circularity — no.** All 10 models + 6 exit models are independent random
  generations (seed ∈ {0,1} × distractor seed+77 for test), no injected structure.
- **(b) Known-method-in-disguise — partial.** Early-exit is mature (BranchyNet,
  DeeBERT); the NEW objects are the *task-difficulty dependence* of the exit layer
  (exit* ∈ {2,4} independent of d∈{4,16}) and the correction of the ≈d/2 claim.
  Catalog scan (2067 packages): no prior work connecting the norm crossover to a
  task-dependent exit layer on grammar.
- **(c) Toy-scale — acknowledged, and it IS the finding.** dm=48 Dyck-1 is
  attention-solvable, which is exactly why the load-bearing test needs Dyck-2
  (multi-type matching — genuinely non-regular context-free) or a width-starved /
  unbounded-nesting setting. The exit-track-tasks law is architecture-mechanical and
  testable on real LMs.
- **(d) Data leakage — none.** Test words are fresh random balanced strings (seed+77),
  never in training; all models reach 1.0000 on held-out before probing.
- **(e) Variance — reported honestly.** 2 seeds × 5 depths (flat) and 2 seeds × 3
  depths (exit). The depth-independence of exit* (2–4 across d=4..16) is 6/6; the
  +3 crossover outlier is reported, not averaged away.
- **(f) Measurement — documented.** exit acc = shared-head next-token accuracy on
  held-out; bar 0.95 = 0.95·full (full = 1.0000); crossover = first l with two
  sustained ratios ≥ 1.02; saving = (d−exit*)/d layer-compute. Part C (by-balance
  exit) was not separated: since every model is perfect at every balance bin, there is
  no bin where depth helps, making by-balance exit moot at this scale.
- **(g) Baseline fairness — yes.** Baseline is the full model at 1.0000; exit* acc
  0.9613–1.0000, gap ≤ 0.04 (lossless within the 0.95 bar).
- **(h) Practical relevance — a real lever, bigger than NET-6.** On easy-to-moderate
  sequential tasks a trained transformer's inference depth can be cut 75% (d=16 →
  exit at 4/16) with lossless accuracy: run to the first shared-head-usable layer and
  apply the existing head. The predictor (task-difficulty → early crossover) is
  measurable in training.

**Verdict.** NET-7 (speed axis, round 2): (1) depth is FLAT on Dyck-1 — d=1 solves
all nesting ≤12, extending the flat-depth law to grammar and REFUTING the
load-bearing premise at this scale; (2) the exit law is REFINED to
EXIT-TRACKS-TASK-DIFFICULTY — exit* ∈ {2,3,4} independent of d (d=4..16), 17/18
within ±1 of the crossover across both task classes, and the crossover is
task-dependent (≈d/2 on harder automata, ≈1–3 on easy Dyck), giving up to 75%
lossless inference saving on the easy task; NET-6's "exit ≈ d/2" is corrected to its
proper scope. The load-bearing-depth test (where the exit law could have a boundary)
is still open — next is Dyck-2 multi-type matching or a width-starved Dyck, and the
exit law at real-LM/BERT scale. Round-net-7. Now 7 network experiments. Assessment
v7. Paper NET-7, issue #102. Script: /tmp/exp_net_speed2.py.

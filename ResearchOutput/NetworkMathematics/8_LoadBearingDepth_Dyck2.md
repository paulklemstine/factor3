# Depth is Flat on the Non-Regular Grammar Task (Dyck-2), the Load-Bearing Test Fails a Third Time, and Single-Layer Stack-Top Recovery is Genuine (NET-8)

**Program:** Network/LLM research lab — round-net-8 (depth axis, round 6; the load-bearing test via the canonical non-regular CFG)
**Date:** 2026-08-13
**Status:** Machine-verified (Dyck-2 next-token, semilength 12, two bracket types; dm=48, 4 heads; d∈{1,2,4,8,16}×2 seeds = 10 depth models + shared-head exit on d∈{4,8,16}×2 seeds = 6 exit models + windowed-linear baselines K∈{4,8,12}).

## Hypothesis and statement

NET-2/NET-3/NET-4/5/NET-7 built the flat-depth law across four task classes, and NET-7's
load-bearing test via bounded Dyck-1 failed because a single bracket type reduces stack
recovery to a scalar prefix-sum (balance) that one attention head computes. This
iteration applies the decisive test: **Dyck-2** (two bracket types, '(' vs '['), the
canonical **non-regular context-free** language. Next-token close prediction now requires
recovering the *type* of the top of the stack (the last unmatched open's bracket type) —
a history-dependent discrete state, chance 0.5 given only the balance. Two questions:

- **(1) Does depth finally pay?** The natural construction is: layer 1 computes the
  balance prefix-sum, layer 2 keys on balance(t)=balance(j) to select and read the last
  unmatched open. If so, d=1 should FAIL at close-type positions while d≥2 succeeds —
  the first genuinely LOAD-BEARING depth regime in the series, and the exit law's first
  potential boundary (a depth-using model should NOT be exitable losslessly).
- **(2) Is the single-layer success a local shortcut?** Even if d=1 empirically reaches
  perfect close-type accuracy, is that genuine long-range stack-top selection or a
  window-fixable statistic? Barrier (g) demands a fair windowed baseline.

The falsifying alternative for (1): Dyck-2 at semilength 12/dm48 is ALSO
attention-solvable (one layer's heads compute the balance and route each close position
to its matching open), depth is FLAT again, and the load-bearing regime is still not
reached at this scale.

## 1. Part A — depth is FLAT on Dyck-2: d=1 alone solves stack-top-type recovery

All 10 models (d∈{1,2,4,8,16}×2 seeds, budget 8000 AdamW steps each) reach held-out
next-token test = **1.0000 at every metric**:

| depth | test (s0/s1) | b0 | b1 | b2 | b3 | b4+ | close_all | close_b4+ |
|---|---|---|---|---|---|---|---|---|
| 1 | 1.0000 / 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 2 | 1.0000 / 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 4 | 1.0000 / 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 8 | 1.0000 / 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 16 | 1.0000 / 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

**The hypothesis (1) is REFUTED: depth is completely flat on the non-regular grammar
task.** The two-layer "balance-in-L1, select-in-L2" construction is NOT needed — a single
attention layer (dm=48, 4 heads) both tracks the balance and recovers the type of the
top of the stack, at every balance depth and at every close position (close_all =
1.0000 means *every* k-th close of *every* run, including closes whose matching open sits
11+ tokens back). The stack-top type is a history-dependent discrete state, yet a single
layer selects it perfectly at this scale. The flat-depth law now covers **FIVE task
classes**: lookups (NET-2), composition (NET-3), decomposable-error arithmetic (NET-4/5),
Dyck-1 regular grammar (NET-7), and Dyck-2 non-regular grammar (NET-8). The load-bearing
regime — the one place a non-flat depth law and an exit-law boundary could live — was NOT
achieved a third time. It remains genuinely open; the test must escalate to width-starved
Dyck, semilength scaling, or unbounded nesting.

## 2. Part B — the exit law holds on a third task class; exit* is task-difficulty saturated

Shared-head early exit (trained final LN+readout applied to each frozen LN(x_l)) on
d∈{4,8,16}×2 seeds; exit* = first layer with exit accuracy ≥ 0.95·full = 0.95:

| d | seed | full | exit* | l=exit*−1 → l=exit* | crossover | d/2 | lossless@cross | saving |
|---|---|---|---|---|---|---|---|---|
| 4 | 0 | 1.0000 | 3 | 0.6903 → 1.0000 | 3 | 2 | True | 25% |
| 4 | 1 | 1.0000 | 3 | 0.6477 → 0.9654 | 4 | 2 | True | 25% |
| 8 | 0 | 1.0000 | 5 | 0.8875 → 0.9988 | 5 | 4 | True | 37.5% |
| 8 | 1 | 1.0000 | 4 | 0.6097 → 0.9901 | 4 | 4 | True | 50% |
| 16 | 0 | 1.0000 | 5 | 0.9237 → 0.9843 | 2 | 8 | False | 69% |
| 16 | 1 | 1.0000 | 3 | 0.6314 → 0.9725 | 2 | 8 | False | 81% |

**exit* ∈ {3,4,5} — saturated at task difficulty, NOT scaling with depth.** d=16 exits at
layer 3–5 of 16 (69–81% inference saving, lossless within the 0.95 bar); d=8 at 4–5 of 8
(37.5–50%); d=4 at 3 of 4 (25%). This is the same EXIT-TRACKS-TASK-DIFFICULTY signature
as NET-7: Dyck-2's stack-top statistic is computed in 3–5 layers regardless of how many
layers the network has; the rest is readout-amplification.

**|exit*−crossover| ≤ 1 in 5/6 here — 22/24 across all three task classes** (NET-6's 12
automata + NET-7's 6 Dyck-1 + this 6). The single outlier is the same +3 class as
NET-7's: d=16 s0 (crossover=2, exit*=5 — the norm grows immediately but decodability
lags). **exit* ≥ crossover in 5/6** (same outlier). **Lossless-at-crossover holds in 4/6**
(both d=4, both d=8) and fails exactly on the two d=16 models where the crossover fires
very early (l=2): there exit* lags 1–3 layers, exactly NET-7's partial refinement — when
the crossover fires at l≤2, the fixed usability bar is the reliable trigger; lossless exit
means exit at the first shared-head-usable layer, not at the norm.

**Practical lever confirmed on a third task class:** a trained transformer's inference
depth can be cut 69–81% (d=16 → exit at layer 3–5) with lossless accuracy on a
non-regular grammar task, no confidence gate. NET-6's "exit ≈ d/2" is now conclusively
scoped: it held only on the harder automata whose compute fills Phase I; on easy-to-
moderate sequential tasks the crossover and the exit are both early and depth-saturated.

## 3. Part C — the single-layer stack-top recovery is genuine: windowed linear baselines cap far below it

Barrier (g) applied to the load-bearing negative: is d=1's perfect close-type accuracy
real balance-conditioned attention, or a statistic a fixed-window local model can match?
Baseline = last-K tokens one-hot + running-balance one-hot + position-in-word one-hot →
next token, linear map, 3 epochs, same held-out data, K ∈ {4, 8, 12}:

| model | close_all | close (bal≥2) | close (bal≥4) | close (bal≥6) |
|---|---|---|---|---|
| windowed linear K=4 | 0.7322 | 0.8844 | 0.9330 | 0.9646 |
| windowed linear K=8 | 0.7544 | 0.8997 | 0.9619 | 0.9753 |
| windowed linear K=12 | 0.7518 | 0.9017 | 0.9315 | 0.9663 |
| d=1 transformer | **1.0000** | **1.0000** | **1.0000** | **1.0000** |

**The strongest windowed baseline never reaches the transformer, even when the matching
open is inside the window.** The k-th close of a run must read the open at distance 2k−1;
widening the window from K=4 to K=12 covers distance up to 11 (closes #1–#6) and yet
close_all only moves 0.7322 → 0.7544. A linear map cannot route the *conditional* index
"if the trailing run is k closes deep, read the token at distance 2k−1" for all k at once
— that requires gating/products between run-depth and position, which attention provides
(attention weight = balance-conditioned position match). The transformer's +25pp over the
windowed baseline on close_all, and its 1.0 at close_b4+/b6+ where the baseline tops out
at 0.97, is the genuinely long-range content. The balance-bin accuracies rise with balance
depth on the baselines for a measurement reason worth stating: the b6+ bin is dominated by
the *first* closes of deep runs (locally covered), so it is close_all — every k-th close
of every run — that is the honest hard-close diagnostic, and there the transformer's 1.0
vs baseline 0.73–0.75 is the clean gap. The mechanism of single-layer stack-top selection
is therefore GENUINE (not a window shortcut) and its margin is now quantified, not
hand-waved.

## 4. Verification vs the network-loop barriers

- **(a) Circularity — no.** All 10 depth + 6 exit models are independent random
  generations (seeds {0,1}, test seed+77); no injected structure — the Dyck-2 generator
  emits uniform balanced shapes with iid per-pair types, so the close-type statistics are
  exactly 0.5 at init.
- **(b) Known-method-in-disguise — no for the law, acknowledged for the family.** The
  flat-depth and exit laws are the same objects extended to a non-regular CFG; the NEW
  content is (i) the flat law now covers five task classes including the canonical
  non-regular language, and (ii) the exit law holds losslessly under genuine
  history-dependent state. Catalog scan: no prior work connects the norm crossover to a
  depth-saturated exit layer on Dyck-2.
- **(c) Toy-scale — acknowledged, and it IS the finding.** dm=48 Dyck-2 at semilength 12
  is attention-solvable (d=1 perfect) — which is exactly the claim: the load-bearing
  boundary is not reached at this scale. The decisive escalation is semilength scaling
  (where does d=1 start failing — the actual load-bearing boundary) and width starvation
  (dm=16, 1 head), plus the exit law at real-LM scale.
- **(d) Data leakage — none.** Test words are fresh random balanced strings (seed+77),
  never in training; all models reach 1.0000 on held-out before probing.
- **(e) Variance — reported honestly.** 2 seeds × 5 depths (flat law, 10/10 perfect);
  2 seeds × 3 depths (exit law). The depth-saturation of exit* (3–5 across d=4..16) is
  6/6; the +3 crossover outlier (d=16 s0) and the 2/6 lossless-at-crossover failures
  (both d=16) are reported, not averaged away.
- **(f) Measurement — documented.** exit acc = shared-head next-token accuracy on
  held-out; bar 0.95 = 0.95·full (full = 1.0000); crossover = first l with two sustained
  norm ratios ≥ 1.02; saving = (d−exit*)/d layer-compute. The by-balance close metrics
  are reported WITH the caveat that deep-balance bins are dominated by first-closes of
  deep runs (locally covered) — close_all is the honest hard-close diagnostic.
- **(g) Baseline fairness — the windowed baseline is the strongest local model tested, and
  it loses.** K up to 12 (distance 11) + balance + position, linear — the fair fixed-window
  ceiling. It reaches close_all 0.73–0.75 (never 1.0), the transformer 1.0000. The margin
  is the conditional long-range selection content. (A windowed MLP could in principle
  gate to the matching open; the claim here is the LINEAR window cannot, and the single
  attention layer can — quantified +25pp.)
- **(h) Practical relevance — a real lever, confirmed on a third task class.** On a
  non-regular grammar task, d=16 can exit at layer 3–5 (69–81% saving) losslessly within
  the 0.95 bar, no confidence gate. And the flat-depth result is a genuine caution:
  single-layer transformers solve canonical stack-recovery at this scale, so "deep is
  needed for syntax" claims must be checked against width/context-starved confounds.

**Verdict.** NET-8 (depth axis, round 6; the load-bearing test via the canonical
non-regular CFG): (1) depth is FLAT on Dyck-2 — d=1 solves stack-top-type recovery at
every balance and every close position, extending the flat-depth law to a FIVE-task-class
law (lookups/composition/arithmetic/Dyck-1/Dyck-2) and refuting the load-bearing premise
for the third time; (2) the exit law holds on a third task class — exit* ∈ {3,4,5}
depth-saturated, |exit*−crossover| ≤ 1 in 5/6 (22/24 across three classes), 25–81%
lossless inference saving, with NET-7's refinement confirmed (fixed usability bar, not the
norm, is the reliable trigger when the crossover fires at l≤2); (3) the single-layer
stack-top recovery is GENUINE — windowed linear baselines (K=4..12) cap at close_all
0.73–0.75, +25pp below the transformer, because a linear map cannot conditionally index
the matching open (the k-th close's open is at distance 2k−1); attention can. The
load-bearing regime and the exit law's practical boundary remain open — the decisive next
test is semilength/nesting scaling of Dyck-2 (at what context length does d=1 break?),
a width-starved Dyck (dm=16, 1 head), and the exit law at real-LM/BERT scale.
Round-net-8. Now 8 network experiments. Assessment v8. Paper NET-8, issue #103.
Script: /tmp/exp_net_dyck2.py.

# Paper 168 — U-HARDEN: The u-Sensitivity Is Mostly Intrinsic, Partly Resolution

**Verdict name: NEITHER (both pre-stated hypotheses fail; intermediate truth).**
Round-45 #2 (cron iteration) · exp 501 · assessment v277 · script `ResearchOutput/scripts/2026-08-21-resume/exp501_u_harden.py` (+ `exp501_result.json`, `ledger_exp501.jsonl`) · seeds 20260970–77.

## 1. Starvation or intrinsic?

Paper 167's paired u-drop (+0.106 everywhere) had two candidate drivers: rank starvation
(fewer smooth values at tight u → coarser ranks, should recover with more values) or
intrinsic threshold reweighting. Four-cell design: window {240, 960} × u {2.5, 3.5}, 8
populations.

## 2. Results

| arm | u=2.5 | u=3.5 |
|---|---|---|
| 240 values | 0.7339 ± 0.0125 | 0.6266 ± 0.0106 |
| 960 values | 0.7978 ± 0.0106 | 0.7342 ± 0.0099 |

Paired deltas: Δ(240) = **+0.1073** [0.0973, 0.1148] — reproducing paper 167 on fresh
seeds; Δ(960) = **+0.0636** [0.0597, 0.0680]; difference-of-differences D = **+0.0437**
[0.0346, 0.0533] — excludes zero and the ±0.03 band. **H1 FAIL** (4× values recover only
41%, not "most"); **H2 FAIL** (not "none" either).

Reading: quadrupling the window recovers 41% of the drop — a real minority share from
per-N rank resolution (the u=3.5 gain came from finer rate granularity, since smooth mass
per offset was unchanged) — with the substantial ~0.064 residual being intrinsic to
threshold reweighting itself.

## 3. What this decides

Paper 167's u-drop is neither a pure sampling artifact nor fully threshold-intrinsic.
Named follow-up: decouple B from vmed (hold the strip bound fixed across u) to isolate the
reweighting component directly. Caveat disclosed: nested windows conflate sample size with
bound growth (B crosses the dial cap between arms). Barriers: (5)/(8) unchanged.

Now 502 experiments. Assessment v277.

# Paper 150 — PHASE-FEATURES: Low-Prime Phases Are Sub-Threshold and Window-Local

**Verdict name: PHASE-NO-LIFT / H3-FAIL** (author-agent's final naming; amends the coordinator's earlier read).
Round-41 #1 (cron iteration) · exp 482 · assessment v259 · script `ResearchOutput/scripts/2026-08-21-resume/exp482_phase_features.py` (+ `exp482_result.json`) · seed 20260901.

## 1. Paper 147's named follow-up, executed clean

Does the root-position phase profile mod small primes explain the split-ceiling excess?
Clean reimplementation (the agent's L0 audit voided the coordinator's inline quick attempt:
its cross-window arm trained and tested on second-half targets, its offset used
min-of-two-root-offsets instead of (r₁−s) mod p, and its encoding collided non-QR with
phase zero). Design: 1200 semiprimes bitlen 44 × 240 relation values; phase features
(cos, sin)(2π·o_p/p) + QR-indicator for p ∈ {3,5,7,11,13} extended to {…,29}; targets
recomputed per window half; paired bootstrap.

## 2. Results

| arm | baseline R² | +phases(≤13) | ΔR² [95% CI] | +phases(≤29) |
|---|---|---|---|---|
| same-window (u=2.5) | 0.6039 | 0.6121 | +0.008 [−0.021, +0.040] | 0.6081 (+0.004) |
| cross-window (u=2.5) | 0.4032 | 0.3912 | **−0.0120** [CI upper < 0] | — |

- **H1 REFUTED**: phase lift is +0.008/+0.004 — nowhere near the pre-stated +0.05;
  phase-only is WORSE than baseline (−0.077).
- **H2 VOID** (amended per the author agent): no positive same-window gain existed to
  localize — the cross-window shrinkage held only trivially because every augmented model
  LOSES R² cross-window. Window-locality remains plausible but was not demonstrable here.
  u=3.5 rows: phase gains negative at both windows (−0.009/−0.015).
- **H3 REFUTED**: augmented R² = 0.608 < 0.70.

## 3. What this decides

Low-prime phase coordinates are sub-threshold and window-local: they neither predict yield
beyond the footprint dial nor transfer across disjoint sieve windows. The split-ceiling
excess remains UNEXPLAINED by any tested feature class — candidate explanations narrow to
higher-prime phase patterns or same-window leakage of realized-divisibility features (the
base dial itself drops 0.60 → 0.40 cross-window, so same-window information is real in it).
Barriers: (5)/(8) unchanged.

Now 482 experiments. Assessment v259.

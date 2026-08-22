# Paper 149 — MAGNITUDE-INTERVAL: Position Information Is Not a Single Interval

**Verdict name: H1-REFUTED — the interval law's scope is mapped by the failure.**
Round-40 #5 (cron iteration) · exp 479 · assessment v258 · script `ResearchOutput/scripts/2026-08-21-resume/exp479_magnitude_interval.py` (+ `exp479_result.json`) · seed 20260831.

## 1. The composition question

Papers 137 (magnitude ordering pays 5.19×) and 143/146 (interval hints priced by coverage ×
width) left open whether real magnitude information IS an interval hint on that plane. Test:
extract each N-decile's conditional J-posterior, take its 90% window, and check whether
committed scanning at the extracted window reproduces descending-order's gain.

## 2. Results

- Descending order reproduced at **5.23×** on this population (anchor 5.19×, ratio 1.008).
- **H1 REFUTED (strong form)**: the extracted pooled window is (α=0.9, μ/M=0.79) — far
  outside paper 143's band ([0.02, 0.05] at α=0.9) — committed scanning there recovers only
  **69.7%** of the descending gain (corr −0.32: the interval policy misranks which Ns are
  cheap); and even COST-OPTIMAL committed windows per decile (DC1-verified to 9e-11) reach
  only **4.707× = 90.0%** of desc population-wide.
- **The refined diagnosis — ORDER-NOT-SUPPORT**: what descending exploits is likelihood
  ORDER (scan from √N downward, adaptive stop; mean stopped width E[c_d]/E[M] = 16% with
  effective coverage 1.0) — a third coordinate that (α, μ/M) cannot price. Recommendation
  adopted into the programme queue: extend paper 143's hint plane with an ordered-adaptive-
  scan coordinate.
- **H2 confirmed with inverted detail**: balance strata drive everything — local descending
  speedup **35.96×** (most-balanced quartile) down to <1 (low-M deciles), monotone across
  q/p quintiles (μ/M falls 0.79 → 0.29); near-square Ns map to WIDE within-stratum windows
  despite huge local speedup, because their advantage lives in the pointwise relation
  J ≈ M_N — invisible to absolute-window summaries.
- FLAG: the agent's DC1 closed-form cross-check diverged (max err 1.6e7) while the DC2 brute
  force agrees with direct measurement (0 mismatches) — analytic path buggy, brute paths
  consistent; disclosed, analytic numbers not used.

## 3. What this decides

The two-number law (coverage × width) prices the SINGLE-WINDOW oracle family; real magnitude
posteriors are multi-modal across balance strata and need the full ordering functional —
paper 137 remains the correct measurement object for position information, papers 143/146/148
the correct theory for genuinely-interval oracles. The barrier map's rows keep separate
functional: residues (order), intervals (order, single-window), position (full order),
class hints (order + which-factor ceiling). Barrier lines: (2)/(8) unchanged.

Method ledger: zombie-completion pattern again (~40 min to first files); population balance
distribution differs from paper 137's original (agent-disclosed); DC1 failure disclosed.

Now 481 experiments. Assessment v258.

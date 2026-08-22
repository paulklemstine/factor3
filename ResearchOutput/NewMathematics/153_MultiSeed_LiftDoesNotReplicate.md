# Paper 153 — MULTISEED-PHASE: The Lift Class Does Not Replicate

**Verdict name: LIFT-DOES-NOT-REPLICATE (the +0.03 readings were population luck).**
Round-41 #4 (cron iteration) · exp 485 · assessment v262 · script `ResearchOutput/scripts/2026-08-21-resume/exp485_multiseed_phase.py` (+ `exp485_result.json`) · seeds 20260910–14.

## 1. The gating replication

Paper 152's amendment named seed variance the dominant uncertainty: identical ph13 features
read +0.0082 (exp 482) vs +0.0310 (exp 484). Resolution: 5 fully independent populations
(seeds 20260910–14; 1200 Ns × 240 values each), identical feature constructions, shared
protocol.

## 2. Results

| seed | R²_base | ΔR²(ph13) | ΔR²(pair) |
|---|---|---|---|
| 20260910 | 0.5624 | −0.0046 | +0.0070 |
| 20260911 | 0.5948 | +0.0072 | −0.0182 |
| 20260912 | 0.6226 | −0.0020 | +0.0079 |
| 20260913 | 0.6044 | −0.0023 | +0.0108 |
| 20260914 | 0.5902 | +0.0057 | +0.0073 |

- **mean ΔR²(ph13) = +0.0008 ± 0.0053 — zero within noise.**
- **mean ΔR²(pair) = +0.0030 ± 0.0119; pair-vs-phase difference = +0.0022 ± 0.0160 —
  indistinguishable.** Paper 152's "first positive lever" does not survive.
- H3 refuted: corr(ΔR², R²_base) = 0.06 / 0.09 — no concentration structure.
- Note: base R² itself spans 0.56–0.62 across these same seeds — population luck moves
  everything together.

## 3. What this decides

The phase/coincidence programme resolves completely: singleton phases (low and high prime),
and pair coincidences all add ≈ nothing beyond the footprint dial once population variance is
averaged out. The split-ceiling excess remains unexplained by every tested encoding and may
be intrinsic to the dial family's same-window realized-divisibility information. **The
footprint dial of paper 145 stands as the final form**: rate(N) ≈ β₀ + β₁·w(N) + β₂·d(N),
~200 Euler tests per candidate, R² ≈ 0.59 at u=2.5. Barriers: (5)/(8) unchanged.

Now 485 experiments. Assessment v262.

# Paper 173 — PPOW-MULTISEED: The Prime-Power Lift Replicates Across Seeds and Grows with Window Length

**Verdict name: PPOW-LIFT-REPLICATES-AND-GROWS.**
Round-46 #2 · exp 506 · assessment v281 · script `ResearchOutput/scripts/2026-08-21-resume/exp506_ppow_multiseed.py` (+ `exp506_result.json`) · seeds 20260940–44.

## 1. The mandatory replication

Paper 172's prime-power lift (+0.089 at one seed) required multi-seed confirmation per
papers 150/152's lesson. Five fully independent populations bitlen 44 × two windows
(240/960) × two smoothness thresholds (u ∈ {2.5, 3.5}), paired bootstrap CIs throughout.

## 2. Results

Per-seed ΔR²(pp_sum over base) at (u=3.5, w=240): +0.055/+0.049/+0.051/+0.050/+0.048 —
**all five above 0.03**, cross-seed sd **0.0025**, SE(mean) **0.0011**. CI excludes zero
on 5/5 cells at BOTH u. Lift GROWS with window length: mean ΔR² rises 240→960 at both u
(u=3.5: 0.051→0.058; u=2.5: 0.058→0.082). The prime-power term is REAL, seed-stable, and
window-robust.

## 3. What this decides

Paper 172's discovery is confirmed as a genuine structural component of the per-N dial,
not a population artifact. Barriers: (5)/(8) unchanged.

Now 506 experiments. Assessment v281.

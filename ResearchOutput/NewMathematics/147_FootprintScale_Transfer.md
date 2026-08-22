# Paper 147 — FOOTPRINT-SCALE: The Dial Transfers Across Scale and Grows With Relation Count

**Verdict name: DIAL-TRANSFERS (H1/H3 confirmed; H2 raw facts recorded, ceiling column not adopted).**
Round-40 #3 (cron iteration) · exp 478 · assessment v256 · script `ResearchOutput/scripts/2026-08-21-resume/exp478_footprint_scale.py` (+ `exp478_result.json`) · seed 20260830.

## 1. Does the footprint dial leave its birth scale?

Paper 145 fitted the footprint-weighted yield dial at one scale (bitlen 44). Transfer test:
fit at 44, predict held-out Ns at bitlen 48 and 52, at 80 and 240 relation values per N,
u ∈ {2.5, 3.5} — calibration slope bands [0.8, 1.25], bootstrap CIs.

## 2. Results

- **H1 CONFIRMED (post-reconciliation)**: transfer slopes 0.8955 / 0.8341 (80 values/N,
  bl 48/52) and 0.9124 / 0.8335 (240 values/N) — all four cells inside the band.
- **H3 CONFIRMED**: the direct divisibility feature d(N) stays independently significant in
  **12/12 cells** (min |t| = 3.92) after the footprint mass.
- **H2 raw facts**: R² rises substantially with relation count — 0.41 → 0.60 (u=2.5/bl48),
  0.40 → 0.57, 0.32 → 0.49, 0.27 → 0.42 from 80 to 240 values/N. The agent's ceiling COLUMN
  is definition-inconsistent with the lab's convention (measured R² exceeds it by >2×), so it
  is NOT adopted; only the raw R²-vs-n facts are cited. A dedicated ceiling re-derivation is
  deferred.

## 3. What this decides

The footprint dial is a stable, scale-transferring calibration object: fit once at bitlen 44,
deploy across the toy range with in-band calibration; more relations per N buy real R²
(≈ +0.15–0.19 for 3× the values). Practical QS triage form stands. Barrier lines: (5)/(8)
unchanged (method-input residue dials).

Method ledger: the duplicated-u-block assembly bug was caught by coordinator review of the
agent's result.json and fixed by the agent on demand (surgical re-analysis, no data
re-collection); pre-reconciliation read had one cell out of band and identical u rows.

Now 479 experiments. Assessment v256.

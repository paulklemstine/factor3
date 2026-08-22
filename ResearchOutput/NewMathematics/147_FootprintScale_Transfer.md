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
- **H2 REFUTED as stated, replaced by a sharper finding**: every ceiling measure rises
  80→240 (~2×; the binomial floor quarters), and the dial's R² rises in step (8/8) — but it
  does NOT converge to the leak-free split ceiling: it EXCEEDS it 1.6–2.1× at both arms.
  Interpretation: residue symbols encode N-dependent window-phase structure of the
  deterministic divisibility pattern (which j-slots hit which roots), which does not
  replicate across disjoint j-subsets — so the split ceiling caps only the replicating rate
  component, not this dial family. Against the fit-based π̂ yardstick the dial sits at
  ~0.95–1.00× at n=80 and ~0.85–0.90× at n=240. Next experiment named: a phase-aware feature
  (root-position profile mod p) rather than more values per N.

**Correction note (amended post-recording)**: the duplicated-u-blocks bug was UPSTREAM in
the build stage — the trial-division strip ran only to B(3.5) < B(2.5), making the u=2.5
target byte-identical to u=3.5; fixed surgically in `build_bitlen` (strip once to the larger
bound, derive both targets from remainder + largest-found-prime). Secondary u=3.5 transfer is
3/4 cells (bl52@240 slips to 0.770 [0.714, 0.827]); d(N)'s marginal R² contribution is small
(+0.01–0.03 over qrc+w) though consistently significant.

## 3. What this decides

The footprint dial is a stable, scale-transferring calibration object: fit once at bitlen 44,
deploy across the toy range with in-band calibration; more relations per N buy real R²
(≈ +0.15–0.19 for 3× the values). Practical QS triage form stands. Barrier lines: (5)/(8)
unchanged (method-input residue dials).

Method ledger: the duplicated-u-block assembly bug was caught by coordinator review of the
agent's result.json and fixed by the agent on demand (surgical re-analysis, no data
re-collection); pre-reconciliation read had one cell out of band and identical u rows.

Now 479 experiments. Assessment v256.

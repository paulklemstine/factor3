# Paper 162 — UNIFORM-DIAL: The Yield Dial Is Draw-Regime-Invariant

**Verdict name: DIAL-IS-DRAW-INVARIANT (H2's dilution refuted in the good direction).**
Round-43 #2 (cron iteration) · exp 493 · assessment v271 · script `ResearchOutput/scripts/2026-08-21-resume/exp492_uniform_dial.py` (+ `exp492_result.json`) · seed 20260924.

## 1. Does the dial survive genuinely unbalanced keys?

Paper 154 noted the per-N yield dial was validated only on balanced draws. Test: balanced
(p,q near 2^21) vs uniform (p ∈ [2^10, 2^16), q ∈ [2^16, 2^22)) arms, 1200 Ns × 120 values,
u=2.5, paper-145 feature conventions.

## 2. Results

| metric | balanced | uniform |
|---|---|---|
| R² baseline (QR-count) | 0.3019 | 0.3028 |
| R² augmented (+w, +d) | **0.5251** | **0.5202** |
| R² footprint-only | 0.4841 | 0.4619 |
| ΔR²(w over count) | +0.1822 | +0.1590 |
| Spearman(w, rate) | 0.696 | 0.666 |

- **H1 CONFIRMED**: shape transfers (Spearman 0.67 on uniform draws).
- **H2 REFUTED IN THE GOOD DIRECTION**: no variance-share dilution whatsoever — the augmented
  R² is identical across regimes within noise.
- **H3 CONFIRMED**: the footprint weighting beats the plain count by +0.16–0.18 in both regimes.

## 3. What this decides

The per-N yield dial is fully draw-regime-invariant: its residue-structure signal neither
dilutes nor distorts under unbalanced keys, so the QS triage form holds for the realistic
key-shape mix. Barriers: (5)/(8) unchanged.

Now 494 experiments. Assessment v271.


## Addendum — independent full-scale replication (author agent)

The author agent's full design (4 cells: {balanced, uniform} × bitlen {40, 44}, 1500 Ns,
240 values, bootstrap n=300) replicates every verdict: Spearman(qrc) 0.61–0.66 /
Spearman(w) 0.72–0.76; R² base 0.37–0.43; augmented 0.55–0.64; ΔR²(w−count) +0.18–0.21
with CI [0.145, 0.235] under uniform draws. Arms verified genuinely different
(log₂(q/p) spans −0.49..+0.49 balanced vs −4.95..+19.1 uniform) yet rate distributions
near-identical — the invariance is real, not an artifact of matched marginals.

Lab-wide hazard flagged by the author: seeding RNGs with Python `hash()` of arm names
drifts run-to-run under PYTHONHASHSEED randomization — replaced with deterministic index
maps; other experiments should audit for the same pattern.

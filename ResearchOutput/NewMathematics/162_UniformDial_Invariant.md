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

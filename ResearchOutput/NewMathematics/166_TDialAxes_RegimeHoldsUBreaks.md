# Paper 166 — T-DIAL-AXES: Regime Holds, u Breaks

**Verdict name: REGIME-HOLDS-U-BREAKS.**
Round-44 #2 (cron iteration) · exp 499 · assessment v275 · script `ResearchOutput/scripts/2026-08-21-resume/exp499_t_dial_axes.py` (+ `exp499_result.json`, ledger jsonl) · seeds 20260940–44.

## 1. The adopted dial's two validation axes

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 (papers 164/165) validated on its two
remaining axes: the uniform-draw regime and the u=3.5 smoothness threshold. 20-cell grid
(5 populations × {balanced, uniform} × {u=2.5, u=3.5}), determinism verified (two
byte-identical runs).

## 2. Results

Spearman(T, rate) grid:

| seed | bal@2.5 | bal@3.5 | uni@2.5 | uni@3.5 |
|---|---|---|---|---|
| mean (min–max) | **0.717** (.649–.764) | **0.598** (.487–.651) | **0.713** (.649–.746) | 0.641 (.594–.674) |

- **H1 CONFIRMED**: the uniform regime is fully in-band on 5/5 populations — statistically
  indistinguishable from balanced despite N spanning 2²⁷–2³⁸.
- **H2 REFUTED**: u=3.5 degrades SYSTEMATICALLY — every seed drops from u=2.5→3.5 (sign
  test 5/5, p ≈ 0.03), one seed breaching deeply at 0.4866; column mean sits below the band floor.
- **H3 REFUTED**: 4/5 populations pass both axes jointly.

## 3. What this decides

**Adopted**: deploy the zero-fit dial for uniform/heterogeneous draws at the paper-165
operating point u=2.5; do NOT deploy at tighter thresholds (u ≳ 3.5) without recalibration.
Queued: a multi-seed balanced@u=3.5 sweep to localize whether the degradation's center or
only its tail breaches. Barriers: (5)/(8) unchanged.

Now 500 experiments. Assessment v275.

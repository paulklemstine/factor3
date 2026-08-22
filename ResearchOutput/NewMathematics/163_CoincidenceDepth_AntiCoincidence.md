# Paper 163 — COINCIDENCE-DEPTH: The Pair Features Measure Anti-Coincidence

**Verdict name: ANTI-COINCIDENCE (H1 refuted at ~26% of independence; H2 refuted).**
Round-43 #3 (cron iteration) · exp 494 · assessment v272 · script `ResearchOutput/scripts/2026-08-21-resume/exp494_coincidence_depth.py` (+ `exp494_result.json`) · seed 20260925.

## 1. The mechanism question behind paper 152's pair features

Pair-coincidence counts c_pq = #{j: p | v_j AND q | v_j} lifted the yield dial by +0.031
(paper 152). What do they measure? Under independent root positions, the expectation is
240·(2/p)(2/q) per pair.

## 2. Results

- **H1 REFUTED across all ten pairs**: measured coincidences run at **23.5–28.4% of the
  independence prediction** (e.g., 3×11: 1.79 vs 6.71 predicted). The same N's root
  structures across different small primes are COUPLED through N itself — v_j's residue
  pattern is one object, not independent per-prime draws, and joint hits are strongly
  SUPPRESSED relative to independence. The pair features are joint-absence /
  anti-coincidence statistics, not coincidence statistics.
- **H2 REFUTED**: per-prime hit-gap variance adds nothing over pairs (ΔR² = −0.001).
- Pairs lift on this population: +0.0152 (direction consistent with paper 152).

## 3. What this decides

The dial's second-order features work through SUB-INDEPENDENT structure: knowing one small
prime's hit pattern suppresses another's, because a single N determines all root positions
jointly. The "coincidence" framing of paper 152 is retired — these are coupling gauges.
Barriers: (5)/(8) unchanged.

Now 495 experiments. Assessment v272.

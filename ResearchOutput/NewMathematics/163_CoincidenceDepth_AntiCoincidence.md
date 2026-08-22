# Paper 163 — COINCIDENCE-DEPTH: The Pair Features Measure Anti-Coincidence

**Verdict name: PHASE-ARITHMETIC / MARGINALS-CONTAIN-PAIRS** (amended per the original agent's
clean run + coordinator diagnostic; supersedes the interim ANTI-COINCIDENCE read).
Round-43 #3 (cron iteration) · exp 494 · assessment v272 · script `ResearchOutput/scripts/2026-08-21-resume/exp494_coincidence_depth.py` (+ `exp494_result.json`) · seed 20260925.

## 1. The mechanism question behind paper 152's pair features

Pair-coincidence counts c_pq = #{j: p | v_j AND q | v_j} lifted the yield dial by +0.031
(paper 152). What do they measure? Under independent root positions, the expectation is
240·(2/p)(2/q) per pair.

## 2. Results

- **H1 RESOLVED — the ~0.26 ratios were a coordinator bookkeeping error, not physics**:
  the original agent's clean run shows measured c_pq EQUALS the exact CRT count on all
  8000 (N, pair) points (corr 1.000000). The unconditional expectation is
  240·4/(pq)·P(both QR) = 240/(pq) (the QR lottery costs factor 4); the coordinator had
  compared the conditional-on-both-QR prediction against unconditional measurements.
  Diagnostic confirmed: single-prime hit counts follow CRT exactly (96 = 240·2/5 for
  p=5), and zero-hit primes are simply non-QRs.
- **H2 REFUTED**: per-prime hit-gap variance adds nothing over pairs (ΔR² = −0.001).
- Pairs lift on this population: +0.0152 (direction consistent with paper 152).

## 3. What this decides

The dial's second-order features work through SUB-INDEPENDENT structure: knowing one small
prime's hit pattern suppresses another's, because a single N determines all root positions
jointly. The "coincidence" framing of paper 152 is retired — these are coupling gauges.
Barriers: (5)/(8) unchanged.

Now 495 experiments. Assessment v272.


## Addendum — the original agent's decisive run

Measured c_pq = exact CRT count on all 8000 points; calibration vs the unconditional form
within [0.980, 1.127] and vs the both-QR-conditional form within [0.994, 1.006]; the crt
feature arm reproduces the measured-pair lift EXACTLY (+0.0349). Marginals alone (5
per-prime hit fractions) lift +0.0376 ≥ pairs' +0.0349; pairs add nothing beyond marginals
(ΔR² = −0.0027, CI straddles 0). Clumping variance adds nothing (H2 fail stands).

**Adopted**: retire the 10 pair features for the 5 marginal per-prime hit fractions (same
lift, half the columns); record that c_pq is an exact CRT function of root phases whose
entire dial content is the per-prime QR lottery — no clustering structure exists at this
scale. Ledger: directory collision with the coordinator's inline variant documented; both
artifact sets preserved.
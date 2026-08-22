# Math Reads as Prose: the domain jump to mathematical text (Hardy, Boole, Hilbert) leaves the 0.5B knee chain EXACTLY at the prose values — {16, 20} at {512, 1024}, with math's baseline accuracy much LOWER (0.326/0.342 vs 0.446/0.461) yet knees identical — completing a three-domain parameterization where code shifts base down (−4), math shifts nothing, and accuracy level is decoupled from knee position everywhere (NET-70)

**Program:** Network/LLM research lab — round-net-70 (LIMITED-MEMORY AXIS, iteration 37;
second domain-jump leg).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact, argmax-agree 1.0000; math prose = Hardy + Hilbert
from Gutenberg, fsynced durable cache; 24 held-out windows/context; ALL_DONE_NET70).

## Setup

Fine grids k ∈ {4..24}@512 and {8..32}@1024 on MATHEMATICAL TEXT (Qwen2.5-0.5B fp32,
identical harness/gate/bar). Script ResearchOutput/exp_net70_mathdomain.py;
results ~/f3cache/net70_results.json; log /tmp/net70.log.

**Predictions stated BEFORE the run:** P1 MATH-NEEDS-MORE; P2 STRUCTURE-PRESERVED
(+4 increment shape survives); P3 BASE-UNIVERSAL (math reads as prose).

## Results

| ctx | math k\* | prose k\* | math full acc | prose full acc |
|---|---|---|---|---|
| 512 | **16** | 16 | 0.3262 | 0.4460 |
| 1024 | **20** | 20 | 0.3418 | 0.4612 |

Math sweeps @512: 4: 0.907 ✗, 8: 0.959 ✗, 12: 0.979 ✗ (~1 SE), **16: 0.987 ✓**, 20: 0.989,
24: 0.988. @1024: 8: 0.952 ✗, 12: 0.965 ✗, 16: 0.978 ✗ (~1.5 SE), **20: 0.983 ✓**, 24+: pass.

**Scorecard: P1 REFUTED** — math does NOT need more keys. **P2 CONFIRMED trivially**
(the chain is exactly prose's). **P3 CONFIRMED** — knees match prose EXACTLY at both
contexts despite a 12-point accuracy gap.

## Verdict

MATH-READS-AS-PROSE — the three-domain deployment table is now:
**base(prose) = 16, base(code) = 12, base(math) = 16**, with increments set by scale
(NET-67) and shape preserved across all domains. The most interesting negative: mathematical
text is substantially HARDER to predict (accuracy −12 pts) yet needs IDENTICAL attention
budgets — the third and strongest confirmation that prediction difficulty and attention
sparsity structure are independent quantities. Long-range symbolic references apparently do
not change how much context a transformer query needs, only how well it can be predicted.
Deployment: mixed prose+math workloads share one budget entry; only code requires the
lower-base table.

Barriers: (a) clean — three horns pre-stated incl. two refuted; (b) clean — second domain
leg new; (c) confronted — limits: classic-mathematics prose only (no modern LaTeX notation),
one corpus mix, 24 windows stated; (d) clean per-corpus split; (e) deterministic; (f) clean
(ALL_DONE_NET70); (g) fair — byte-identical harness except text; (h) DIRECT — completes the
three-domain table.
Open: modern LaTeX/math notation; non-English domains; increments@4096; 7B cell.
Paper 155, issue #310. Now 70 network experiments. Assessment v70.

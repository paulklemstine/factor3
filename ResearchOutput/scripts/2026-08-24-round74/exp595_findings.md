# exp595 LARGER-P-ECM-TRACE — findings

**Verdict: H1 TRUE / H0 refuted. The exp570 picture (collision floor subdominant; order-hits
fire early) HOLDS at bitlen 32, fresh seed 20260903, n=40/bitlen × 3 B1fracs × 3 curves.**

## Rates by cell (found_p cell rate, Wilson CI)
| bitlen | 0.125 | 0.5 | 0.9 |
|---|---|---|---|
| 26 | 0.65 [0.50,0.78] | 0.75 [0.60,0.86] | 0.60 [0.45,0.74] |
| 32 | 0.75 [0.60,0.86] | 0.775 [0.63,0.88] | 0.75 [0.60,0.86] |

- Scale-stability: 26-vs-32 z-tests p=0.33 / 0.79 / 0.15 at fracs 0.125/0.5/0.9, all CIs overlap.
- KS-vs-uniform REJECTS in ALL SIX cells (p<=0.002); medians 0.073–0.293, tail(norm>=0.8) <=13%
  — early-fire geometry preserved at bitlen 32 (pre-reg gate: median<0.5, tail<0.3, p<0.01).
- Collision-floor subdominance quantified: first-curve rate at (32, 0.125) = 0.425 = 2.6x the
  per-curve baseline 1-exp(-1.44*0.125)=0.165; pure-collision found_q counts are 9–16 per cell
  vs found_p 24–31 — order-hits carry the excess, not luck.
- Rates are FLAT in B1frac (0.60–0.775 across 0.125→0.9): no dose-response of the collision term.

## Consequence
Papers 215→236→238 chain COMPLETE: guarded-affine low-B1 success is scale-stable and
mechanism-attributed (order-completion firing early in the trace, not random collisions);
no scale-dependent collapse toward 1-exp(-1.44*B1/p) through bitlen 32.

## Honest notes
- Early-fire operationalization (median<0.5, tail<0.3) fixed pre-data from exp570's qualitative
  result only; raw norms shipped in exp595_result.json ks_stats for re-reads.
- Cells with <10 hits excluded from geometry gate (none excluded in full run; smoke had none>=10).
- Deaths unbucketed (inherited exp568/exp570 behavior); KS asymptotic p; ec_add rare recursive
  double not idx-counted (tiny found_at bias).
- Wall 1.5 s full (240 cells) — far under budget; artifacts: exp595_largep_trace.py,
  exp595_smoke.log, exp595_smoke_result.json, exp595_result.json.

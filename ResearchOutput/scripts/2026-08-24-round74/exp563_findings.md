# exp563 SEQHINT-COMPOUND-LAW (round-74)

VERDICT: COMPOUND-CONFIRMED-HALVING-FAIL (UNBALANCED stratum alone = GEOMETRIC-COMPOUND-ISOLATION-CAPPED).
H1 confirmed on all three pre-registered predictions; only the strict pooled −ln2 slope constant misses,
marginally and in one stratum.

- Compounding real + superlinear: s_adapt(12)/s_adapt(3) = 239× unbalanced, 20.8× balanced
  (CI excludes linear 4×).
- Hard isolation cap everywhere: 100% of N pinned at k=20 = ⌈log₂W⌉; s(≥20)=T₀ exactly
  (1072 balanced / 2.86e5 unbalanced); max s never exceeds T₀×1.01 → NO barrier event,
  consistent with barriers 4/8 (external position info pays ISOLATION-COST/query;
  prime-oracle bound ≈17).
- Pure adaptivity premium at k=12: 240× [220,261] unbalanced, 20.8× [19.5,22.3] balanced;
  r(1)=1.00 exactly both pairs.
- Aligned halving slope: −0.659 PASS unbalanced; −0.584 balanced, 16% off target —
  band-entry phase correlation, width law itself exact (V2a).
- Headline surprise (ledger catch A5): balanced semiprimes pin min(p,q) at √N → uniform fixed
  battery carries LITERALLY ZERO BITS (s≡1.00 all k≤24); adaptivity is waste-proof.
- Net economics: k_opt = 10/18 vs predicted log₂((T₀−1)ln2) = 9.54/17.60. Sham gate passed both strata.

Reconciliation with prior law: paper-138 linear no-synergy pricing holds for NON-adaptive batteries;
sequential ADAPTIVE hints compound superlinearly but saturate EXACTLY at the ISOLATION-COST ceiling —
the two results are consistent faces of one pricing structure.

Ledger catches: uniform-prior battery zero-bit collapse; even-median bisection stall (fixed via lower
median); V5 expectation-vs-bound constant fix; sham luck/inflation clause split.

Files: exp563_seqhint_compounding.py, exp563_result.json, exp563_run.log, exp563_smoke.{log,json}.
Wall ~2 s full run (cap 20 min). Notebook/git untouched by experimenter.
Digest persisted by coordinator (subagent file-write guardrail).

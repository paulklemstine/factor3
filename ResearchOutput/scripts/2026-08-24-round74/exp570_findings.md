# exp570 COLLISION-VS-ORDER-TRACE (round-75)

VERDICT: H1 and H2 BOTH REFUTED — with inverted geometry; trace still separates
mechanisms; paper 215 NO-WALL account stands; paper 159 amendment-candidate
REJECTED as stated (collision floor real but subdominant); NEW TRACE LAW added.

Headline numbers (wall 1.3 s full, 240 cells):
- B1/p=0.125 found_p rates vs collision baseline 1-exp(-1.44*B1/p)=16.5%:
  bitlen-26 65.0% [CI .495-.779]; bitlen-32 62.5% [.470-.758] — far above
  baseline, cross-bitlen z p=0.82 (scale-stable, NO drop toward floor => H2 dead;
  collisions not dominant at low B1).
- H1's predicted geometry INVERTED: KS rejects uniformity even at low B1
  (p=0.017/0.045); at B1/p=0.9 hits concentrate near ZERO (median normalized
  step-index 0.09-0.10; final-20% tail 0/55, binom p~0.004). Order-completion
  marks EARLY — empirical law: hit position ~ max-prime-power(ord)/B1
  (Golomb/Dickman-low flavor), NOT the pre-registered final-20%.

Amendment chain status: paper 159 wall sentence -> rejected as stated (paper 215);
collision-baseline confound -> real but subdominant (this run); new early-fire
trace law -> added to the factor-local map as a measured regularity.

Honest caveats: true ops = 2.59*B1 (not the 1.44 constant used in baselines —
both baselines recomputed and reported); measured cell rates coincidentally near
3-curve exact-op collision arithmetic, but per-curve excess + KS + empty tail
rule out collision dominance; found_q censoring disclosed.

Ledger catches: closed-form step counter initially wrong (later chunks do len
doubles/popcount adds) — caught by traced-vs-closed assert BEFORE data, fixed,
verified 29/29; smoke regenerated after fix.

Files: exp570_collision_trace.py, exp570_smoke.{log,json}, exp570_result.json,
exp570_full.log. Digest persisted by coordinator (subagent write guardrail).

# Paper 155 — ECM-COMPLETION: The Lite Variant Scales Like ρ

**Verdict name: ECM-LITE-BIRTHDAY-SCALING (true lcm-based ECM still deferred).**
Round-42 #1 (cron iteration) · exp 487 · assessment v264 · script `ResearchOutput/scripts/2026-08-21-resume/exp487_ecm_only.py` (+ `exp487_result.json`) · seed 20260921.

## 1. Paper 154's deferred arm, as ECM-lite

Sequential multiples j = 3..B1 (B1 = 50) of a random point on random curves, 30-curve cap,
ops = point additions — explicitly NOT lcm-based true ECM: the lite structure tests
ρ-like birthday reachability, not L_{1/2} smoothness.

## 2. Results

| k | found | censoring | mean ops | log₂ meanT |
|---|---|---|---|---|
| 16 | 1200/1200 | 0% | 305 | 8.25 |
| 20 | 1163/1200 | 3.1% | 1160 | 10.18 |

Across-k slope = **(10.18 − 8.25)/4 = 0.48 per log₂ p** — birthday-bound scaling exactly as
the lite structure predicts; H1's [0.6, 0.8] band refuted FOR THE LITE VARIANT (true
lcm-based ECM's faster scaling remains deferred). Within-k α unstable (censored tail), not
cited. The unified plane now holds FOUR methods on one population:
td **0.84** / ρ **0.52** / Fermat **0.50** / ECM-lite **0.48**.

## 3. What this decides

The unified plane's fourth column lands where its structure says it must: sequential-multiple
curve arithmetic inherits ρ's √p scaling. Completing the plane with true lcm-based ECM is the
remaining deferred item. Barriers: (8) measuring known methods.

Method ledger: v1 instant-degenerate bug — at j=2 the running point equals the base point,
so generic addition had a zero denominator and every curve died (0/1200 found); fixed with an
explicit doubling step.

Now 487 experiments. Assessment v264.

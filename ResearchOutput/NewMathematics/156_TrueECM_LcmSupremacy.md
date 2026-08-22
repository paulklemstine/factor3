# Paper 156 — TRUE-ECM: The LCM Arm Strictly Dominates

**Verdict name: LCM-SUPERSET-DOMINANCE.**
Round-42 #2 (cron iteration) · exp 488 · assessment v265 · script `ResearchOutput/scripts/2026-08-21-resume/exp488_true_ecm.py` (+ `exp488_result.json`, `exp488_LEDGER.md`) · seed 20260922.

## 1. The deferred true-lcm arm, paired against its lite sibling

Paper 155's ECM-lite (sequential multiples) left true lcm-based stage-1 unmeasured. Paired
design on identical populations (1200 balanced semiprimes per k ∈ {16, 20}), same op-count
convention (dbl=4/add=3), independent curve-RNG streams.

## 2. Results

| cell | found | censored | meanT(found) | ops/instance | mean curves |
|---|---|---|---|---|---|
| LCM k=16 | **1200/1200** | 0 | 216.9 | 216.9 | 1.16 |
| LCM k=20 | **1200/1200** | 0 | 654.1 | 654.1 | 2.01 |
| lite k=20 | 1155/1200 | 45 | 1134.5 | 1258.5 | 8.99 |

- **Strict superset pairing**: all 45 lite-censored instances rescued by lcm, zero lost —
  the strongest possible form of dominance.
- Per-curve success ~4.8× higher; found-only meanT LOWER despite ~2.3× more ops per curve
  (~4.4× fewer curves needed); total-ops-to-factor advantage confirmed (1.92× at k=20).
- Across-k slope 0.398 — birthday-class, marginally below lite's 0.463; no toy-scale
  separation from L_p[1/2,√2], as expected.

## 3. What this decides

True-lcm stage-1 is adopted as the lab's canonical ECM operator: it strictly dominates the
lite variant on find rate AND total cost at equal curve cap. Paper 155's across-k birthday
law re-attributed: 0.48 was the lite reach set's property; true-lcm sits slightly below.
Barriers: (8) consistent — toy scale separates constants only.

Now 488 experiments. Assessment v265.

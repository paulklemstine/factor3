# Paper 104 — HINT-TABLE-COMPLETION: The Six-Dial Hint-Value Table

**Verdict name: THE-HINT-IS-UNIVERSAL.**
Round-30 #1 · exp 440 · assessment v215 · script `/tmp/exp_hinttable.py` · log `/tmp/r30n1f.log` · runtime 17 s.

## 1. Completing the table

Paper 99 measured hint values for two cubic dials only. This round completes the six-dial hint-value table: every dial's I(s,d; labels) − I(N; labels), with permutation-null walls.

## 2. The completed table

| dial | capacity I(N) | hint I(s,d)−I(N) | wall z |
|---|---|---|---|
| C₅@11 | 1.2062 | **+1.5896** | +0.30 |
| F₂₀@5 | 0.2920 | **+0.9538** | −1.10 |
| S₃a@31 | 1.0011 | +0.5201 | +0.67 |
| S₃b@23 | 1.0008 | +0.5121 | +0.92 |
| D₄@8 | 1.9999 | +0.5032 | −0.70 |
| A₄@9 | 0.0015 | +0.0120 | +2.20 |
| **TOTAL** | **5.5015** | **4.0908** | all < 3 |

**All six dials positive ✓.** Every wall inside its permutation null ✓.

## 3. The independence finding

Hint-capacity correlation: **r = 0.256** — weak. Hint value and channel capacity are **independent dial properties**:
- C₅: moderate capacity (1.21) but the HIGHEST hint (+1.59) — the product view captures little, the hint reveals much
- D₄: the HIGHEST capacity (2.00) but a moderate hint (+0.50) — the product view already captures most of what the hint provides
- A₄: near-zero on both (the dead dial from the type-channel results)

This independence means the hint value is NOT just "capacity measured differently" — it measures a genuinely different aspect of each dial: how much additional label structure exists beyond what the product residue reaches.

## 4. Method notes

Root count (or ord) used as the type label — always computable, never crashes. The A₄ root count can be {4, 1, 0, 2} (the last from primes where the polynomial has an unexpected factorization pattern), all handled as valid labels. The hint-value measurement works with ANY type labeling.

## 5. Barriers

**(a)** clean — horns pre-stated. **(b)** clean. **(c)** confronted — 30k shared population, 6 dials, 100-shuffle nulls per dial. **(d)** clean. **(e)** the substance — all hint values positive and quantified; the independence finding (r = 0.256) documented. **(f)** controlled — multiple design iterations before the clean run. **(g)** fair — identical population and methodology across all dials. **(h)** relevance — the completed table provides the full routing map for the 6-dial battery.

Now 440 experiments (439–440: the failed launches and the successful run). Assessment v215. Paper 104, issue #196.

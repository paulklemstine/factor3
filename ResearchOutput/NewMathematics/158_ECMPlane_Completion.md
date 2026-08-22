# Paper 158 — ECM-PLANE-COMPLETION: The Unified Plane Closes with ECM in Its Predicted Slot

**Verdict name: ECM-PLANE-COMPLETION (H1/H2/H3 all confirmed; H3 at its boundary).**
Round-42 #4 (cron iteration) · exp 490 · assessment v267 · script `ResearchOutput/scripts/2026-08-21-resume/exp490_ecm_completion.py` (+ `exp490_result.json`) · seed 20260921.

## 1. The deferred column, completed properly

The ECM arm's own agent delivered paper 154's unified plane closure (marking the lean
ECM-lite probe SUPERSEDED): five methods × two draw regimes, pooled OLS + across-k fits,
common-currency intercepts with wall-time cross-checks.

## 2. Results (α table, balanced / uniform)

| method | α (balanced) | α (uniform) | reading |
|---|---|---|---|
| trial division | 1.0033 | 1.1438 | uniform shift replicates paper 89's 1.09 |
| Pollard ρ | 0.5122 | 0.4856 | factor-locality sharp (Δα = 0.027) |
| Fermat | 0.3836 | −0.85* | *uniform-arm cap-dominated exclusion bias — confirms catastrophic off-balanced non-scaling |
| ECM B1=50 | **0.5995** | 0.6111 | inside the predicted (0.52, 0.84) window |
| ECM B1=250 | **0.5471** | 0.6675 | fewer curves offset higher per-curve cost |

- **H1 CONFIRMED**: ECM across-k α = 0.761/0.718 — strictly between ρ and trial division.
- **H2 CONFIRMED**: factor-locality holds sharply for every non-TD method under the draw
  change (Δα ≤ 0.03); only intercepts move.
- **H3 CONFIRMED AT THE EDGE**: c_ECM − c_ρ = **+3.04 bits common-currency / 10.29× wall
  time** — ECM's toy-scale overhead over ρ sits exactly at the one-order-of-magnitude line;
  the subexponential advantage has not begun at these sizes.

## 3. What this decides

Paper 154's plane is complete: five methods on one population, each in its predicted slot,
with factor-locality directly tested under the draw change. The barrier map's method row now
has every classical method priced under one functional. Barriers: (8)/(4) as before.

Method ledger highlights (full in result.json): a **ρ cycle-lock pathology** found and fixed
(λ_q ∣ λ_p makes every sync an exact meeting; ~6% of draws burned the full op cap) and a
batched-gcd quantization that erased the √p law entirely (first run read α ≈ 0) —
per-iteration gcd restored α = 0.512 against paper 154's 0.52. Fermat's uniform-arm numbers
are exclusion-biased floors, not measurements.

Now 490 experiments. Assessment v267.

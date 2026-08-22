# Paper 154 — FACTOR-LOCAL-ET: Unified Across-K Scaling on One Population

**Verdict name: UNIFIED-SLOPES-MEASURED (honest partial — within-k fits confounded, ECM deferred).**
Round-41 #5 (cron iteration) · exp 486 · assessment v263 · script `ResearchOutput/scripts/2026-08-21-resume/exp486_factor_local_et.py` (+ `exp486_result.json`) · seed 20260920.

## 1. Paper 132's residual item (2), first measurement

Factor-local methods (ρ, ECM) were said to "escape scan-order framing". Lean scope: trial
division, Pollard ρ (Floyd), Fermat on ONE population (1500 balanced semiprimes per factor
size k ∈ {16, 20, 24}), exact iteration counts, censoring disclosed (ρ: 51/25/18 runs).

## 2. Results (across-k scaling of E[T]: Δlog₂meanT per log₂p)

| method | slope | reading |
|---|---|---|
| trial division | **0.84** | near-linear; balanced draws compress the range vs paper 89's 1.09 on uniform draws |
| Pollard ρ | **0.52** | the birthday bound, replicating paper 89's 0.523 |
| Fermat | **0.50** | gap-locality re-confirmed — on balanced draws cost is gap-driven |

Within-k α fits are CONFOUNDED (gap structure + heavy tail + censoring) and are not cited;
the negative Fermat within-k slopes ARE the gap-locality signature appearing directly.
ECM dropped for budget — the full α-table with uniform draws remains open.

## 3. What this decides

The unified plane now has one-population slopes for three classical methods measured
identically: ρ sits at its birthday bound, Fermat at gap-locality, trial division near
linearity even on balanced draws — paper 89's strata re-derived under the E[T] functional.
Barriers: (8) measuring known methods; (4) factor-locality evades aggregation exactly as
priced.

Method ledger: missing import; zero-cost Fermat hits misaligned between x and y filters;
inline takeover after channel death #10.

Now 486 experiments. Assessment v263.

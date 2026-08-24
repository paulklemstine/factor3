# Paper 203 — MULTI-TARGET: Relaxing the Exact Target Buys Trial Division, Nothing Better

**Verdict name: BUDGET-DOMINATED-BLIND / VALUE-SWEEP-GUIDED (α=1.087 = TD-class; no sub-linear regime).**
Round-72 #3 · exp 558 · assessment v310 · script `exp558_multi_target.py` (+ JSON/CSV/logs) · seed 20260826 · embedding asserted 1500/1500.

## 1. Blind multi-target BFS stays broken

FIFO integer-tree search for {nodes : gcd(a,N)>1}, 200k-visit budget: **55% of Ns
censored**; hits sit at the budget frontier (depth 11, median +6 past first
value-crossing; typical hit a/trigger-prime median 2401). Finished-subset α=1.169
(selection-biased) — trial-division-class or worse (~230× TD's median cost).
"Many targets ≈ modular luck" FAILS as a model of depth-ordered search: FIFO
first-hits exceed the uniform-random prediction pq/(p+q) by median +3.74 log₂ (~13×)
— small-a nodes are overrepresented near the root.

## 2. Value-guided expansion: helps enormously, but it IS trial division

Priority dist(a, nearest multiple of N) best-first (cap 4N): guided wins **1500/1500**
paired vs FIFO (z=38.7), median visit ratio 0.111, ZERO censoring — stated plainly
AGAINST the pre-stated magnitude-mirror expectation. Mechanism nailed by data:
**100% of guided first-hits land exactly at a = min(p,q)** (dist is monotone in a on
[0,N/2] ⟹ best-first degenerates into an ascending-value sweep over tree-enumerated
odd-leg values until divisibility territory). Cost α = **1.087 with r²=1.000** — dead
center of the TD band [0.84, 1.14]. The magnitude-mirror seal concerned energy
spectra; this guidance senses no modular structure — it sweeps values.

## 3. The honest headline for the proposal

| method | median mul-equiv | α | finish |
|---|---|---|---|
| blind exact a=N (analytic (3^{dB+1}−1)/2) | 2^56.5 | erratic | ~0% |
| blind multi-target FIFO | 2^18.8 | 1.17 | 45% |
| value-guided multi-target | 2^16.3 | **1.087** | 100% |
| trial division | 2^10.9 | 0.88 | 100% |
| Pollard ρ Brent | 2^8.1 | 0.458 | 100% |

Relaxing exact-N turns an uncomputable search into a ~10^12× better one — but the
landing spot is trial-division-class: every route through the tree's integer face
ends in a known method (barrier 8), and ρ dominates all of them. Triggers are almost
purely p-side (17,892 p / 72 q); K=cap irrelevant within budget.

Ledger: q<p normalization bug caught by climb assertion on the full population;
pricing conventions disclosed. Now 550 experiments (max id). Assessment v310.

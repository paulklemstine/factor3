# Paper 206 — PORTFOLIO: No Universal Winner, No Dial Edge; the Regret Tail Is N-Invisible

**Verdict name: PORTFOLIO-RHO-UNIVERSAL+H3-FAIL.**
Round-73 #1 · exp 560 · assessment v313 · script `exp560_portfolio.py` (+ JSON/CSVs/logs) · seed 20260827 · wall 6.4 s, no censoring.

Oracle winner shares across 600 semiprimes (bitlen 32–40): ρ 58.0%, p−1@256 34.5%,
p−1@1024 4.5%, Fermat 2.8%, TD 0.17% — flat across bitlen bins AND all five balance
quintiles: **the organizing axis is p−1/q−1 powersmoothness, an N-INVISIBLE channel**
(the lab's self-hint closure replicated inside a scheduling frame). ρ succeeds
600/600 (median 534 units); p−1's cheap-win pool hits at median 261 when it hits;
Fermat wins almost never even balanced (median success cost 44,998).

Scheduling regret (test half, n=300): static order mean regret 3.117 vs oracle;
**dial rule tuned itself to "do nothing" (Δ=0.000)**; ML rule significantly WORSE
(4.683, Δ CI [+0.59,+2.88]) — depth-4 trees overfit and Fermat's asymmetric miss-cap
punishes false positives. Median regret 1.000 for every strategy: the fat tail lives
entirely in the smoothness-carried minority that no tested N-only dial reaches.
Named next cell: PAID smoothness probes (short-capped p−1 as observation, not
prediction) — the recoverable pool is real but invisible to free classifiers.

Ledger: method set/pricing frozen pre-data (brief under-specified); H3's mean-vs-
constant elimination refuted by distributional overlap (TD variance-tail wins,
PM1_1024 4.5%) — eliminations need dominance-in-distribution arguments. Barriers
2/5/8 unchanged; consistent with SMOOTH-SELFHINT-DENSITY. Now 550 experiments
(max id). Assessment v313.

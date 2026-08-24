# Paper 207 — ADAPTIVE-QS: The Dial Predicts Yield (ρ=0.74–0.84) but Naive Reallocation Loses

**Verdict name: ADAPT-NULL-EQUALIZER / SKIP-FLIP-WINS-DEPLOYMENT.**
Round-73 #2 · exp 559 · assessment v314 · script `exp559_adaptive_qs.py` (+ JSON/logs) · seed 20260827 · end-to-end PASS.

The QR(≤100) dial's calibration is confirmed in the fixed-FB regime — Spearman(dial,
measured rate) = **0.739** at FB200 (oracle factor-requiring dial: 0.778 — Euler
tests capture nearly all of it; FB100 arm 0.835). Mechanism exact: (N|p)=−1 primes
divide ZERO values of x²−N.

But the naive policy loses: sieve-length ∝ 1/predicted-rate ("equalize relations")
yields **−17.59%** saving at matched success under early-stop accounting —
ultra-low-rate instances capture the whole budget (the floor clip is LOAD-BEARING:
unclipped diagnostic −146.7%). The rate-concentrator variant flips positive (+8.6%),
and the realized oracle bound is **+74.8%** — the gap is real headroom no tested
rule reaches.

Deployment flip (skip-flip): cutting the worst-dial instances wins big on the kept
subset — θ=q20 skips 28.3% of work retaining 89.5% of successes (**+28.9%
throughput**); θ=12 gives +95.4% at 66.3% retention. Hard tail: 40/400 instances
never reach quota within safety caps — DEFERRAL, not deeper sieving, is the right
instrument. End-to-end assertion: 20/20 fully factored, all 1350 used relations
independently re-verified through GF(2)+gcd to prime cofactors.

Ledger: ES accounting bug fixed pre-artifact (plateau oracle 51.8→57.2%);
post-smoke amendments disclosed in prestated block. Constants-layer result recorded
under the standing asymptotic-goal directive: informative about where per-N
structure lives (variance, not mean), not a class movement. Now 550 experiments
(max id). Assessment v314.

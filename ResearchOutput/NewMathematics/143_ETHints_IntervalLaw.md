# Paper 143 — ET-HINTS: External Interval Hints Are Priced by Coverage × Width

**Verdict name: INTERVAL-HINTS-TWO-NUMBERS.**
Round-39 #5 (cron iteration) · exp 474 · assessment v252 · script `ResearchOutput/scripts/2026-08-21-resume/exp474_et_hints.py` (+ `exp474_result.json`) · seed 20260828.

## 1. Paper 138's stated residual, priced

The barrier-map triptych left external SIZE/POSITION hints unpriced ("they attack E[T], not
the order"). Model: candidates indexed j = 1..M with the true min-law w(j) = (2(M−j)+1)/M²;
an oracle names a μ-wide interval containing J with probability α (start uniform over
covering starts; else uniform non-covering). Procedure priced exactly under truthful
conditioning: COMMITTED (interval-first then complement ascending), which is Bayes-optimal
whenever the interval's posterior-mass density exceeds the complement's — true in every cell.

## 2. Results

Exact grid (M=300) × MC (M=10⁵, 200k draws) agree:

| | α=0.5 | α=0.75 | α=0.9 | α=1.0 |
|---|---|---|---|---|
| μ/M = 0.02 | 1.86× | 3.50× | 7.41× | **29.13×** |
| μ/M = 0.05 | 1.70× | 3.01× | 5.59× | 13.12× |
| μ/M = 0.10 | 1.48× | 2.45× | 4.04× | 7.11× |
| μ/M = 0.20 | 1.19× | 1.83× | 2.70× | 3.96× |

(MC spot cells: 5.70 vs 5.59; 33.99 vs 29.13 — gap = M-difference + miss-tail noise, disclosed.)

**Crossing**: paper 137's magnitude-ordering gain (5.19×) equals an oracle that knows p's
position within a **2–5%-wide window at ~90% reliability** (or 99% within 10%). Position
information behaves like a moderately-reliable narrow interval hint; the two-number law
(coverage × width) prices the whole external-positional stratum.

## 3. What this decides

The barrier map gains its fourth row: external INTERVAL hints are priced by coverage and
width alone in the expected-cost functional — no residue content required, no which-factor
ceiling (unlike paper 138's class hints), diverging as width→0 at fixed coverage. Barrier
lines: (2) intervals correlate with J directly — outside the uniform-marginal lemma's scope;
(8) interval-first scanning near √N IS Fermat's start — named and priced.

Method ledger: v1 MC drew intervals without using α (speedups < 1 — nonsense); v2's exact
grid assumed J ~ U(interval | hit), INCONSISTENT with w — exposed by model-vs-MC disagreement,
the disagreement itself acting as detector; interleaved procedure dropped from exact grid
(MC-only); inline takeover after three agent deaths on this task.

Now 475 experiments. Assessment v252.

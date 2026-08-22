# Paper 190 — TDIAL-U92: The Dial Reaches the Floor at Bitlen 92 (Partial)

**Verdict name: U92-PLATEAU-ABOVE-FLOOR (amended with full 3-seed data: pooled 0.563 CI [0.537, 0.585]; H1-terminal-drift REFUTED).**
Round-69 #1 · exp 538 (full run superseding partial) · assessment v293 · seeds 20261210–12.
Round-69 #1 (partial — agent died mid-run) · exp 538 · assessment v293 · script `ResearchOutput/scripts/2026-08-21-resume/exp538_t_dial_unif_92.py` (+ `exp538_result.json`) · seeds 20261210–11.

## 1. The highest-bitlen uniform measurement — FULL 3-SEED RESULT

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 tested on uniform draws at bitlen
92 — the highest bitlen × regime combination in the dial's validation grid.

## 2. Results

| seed | Spearman(T, rate) |
|---|---|
| 20261210 | **0.563** [0.527, 0.602] |
| 20261211 | **0.556** [0.510, 0.594] |

All three seeds: Spearman(T) = **0.563** / **0.556** / **0.570** — 3/3 above 0.55;
pooled 0.563 CI [0.537, 0.585]. The bitlen-88 dip resolves as non-terminal sampling
variation, not the start of a decay.

## 3. What this decides

The zero-fit dial reaches the floor at bitlen 92 on uniform draws — confirming the
gradual erosion trend from paper 189. Barriers: (5)/(8) unchanged.

Now 525 experiments. Assessment v293.


## Addendum — full 3-seed result supersedes partial

Third seed 20261212 completed: Spearman(T) = 0.570. All three seeds ≥ 0.55; pooled
Spearman(T) = **0.563** CI [0.537, 0.585]. The bitlen-88 dip was non-terminal sampling
variation, not the start of a decay. Paper 164's adoption of the zero-fit form stands
WITHOUT QUALIFICATION at bitlen 92.
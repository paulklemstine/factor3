# Paper 170 — TIGHT-U-RECAL: Reweighting Cannot Recover the Tight-u Drop

**Verdict name: NO-RECAL-RECOVERY (H1/H3 refuted; H2 confirmed as annotation — the fitted weights are consistent but informationally empty).**
Round-45 #3 (cron iteration) · exp 503 · assessment v279 · script `ResearchOutput/scripts/2026-08-21-resume/exp503_tight_u_recal.py` (+ `exp503_result.json`, `ledger_exp503.jsonl`) · seeds 20260990–99 + 20261000.

## 1. Paper 169's named follow-up: can refitting recover the drop?

Fit per-prime coefficients β̂ₚ on hit fractions n_p (odd p ≤ 29; 6000 pooled train rows,
5 held-out populations) at u=3.5 and test whether the recalibrated dial T′ = Σβ̂ₚ·nₚ
recovers the tight-u drop toward the 0.73 anchor.

## 2. Results

| metric | value | verdict |
|---|---|---|
| OOS sp(3.5) of T′ | **0.6050** [0.581, 0.626] | H1 REFUTED (< 0.70) |
| unrefit zero-fit dial | **0.6288** ± 0.0253 | T′ lands BELOW it |
| paired gain vs dial | **−0.0238** [−0.030, −0.016], 5/5 negative | recovery = −24% |
| β rank-stability (split-half / LOPO) | 0.869 / min 0.85, mean 0.9433 | H2 CONFIRMED |
| bitlen-48 transfer sp | 0.5693 < 0.60 | H3 REFUTED |

The fitted β-vector is ANTI-correlated −0.93 with the theory 2/p profile — the
hit-fraction encoding forces weights that grow with p to compensate the 2/p base rate;
the structure is real but carries no new ordering information.

## 3. What this decides

Reweighting the small-prime footprint recovers NONE of the tight-u drop — paper 164's
adoption of the zero-fit form stands WITHOUT QUALIFICATION. The lost content sits beyond
the p ≤ 29 footprint: mid primes (31–356) and/or non-footprint structure. Combined with
paper 169 (~9% bound shrinkage), the drop is now doubly localized as genuine threshold
reweighting whose content is not capturable by small-prime footprint features of any
weighting. Barriers: (5)/(8) unchanged.

Method ledger: two pre-launch catches (a generalized-bitlen redraw check that would have
infinite-looped; a ledger kwarg collision after population 0).

Now 504 experiments. Assessment v279.

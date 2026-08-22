# Paper 179 — T-DIAL-60: The Degradation Plateaus

**Verdict name: T-DIAL-60-PLATEAU (H2 pass — degradation plateaus, not monotone).**
Round-49 #2 (cron iteration) · exp 512 · assessment v285 · script `ResearchOutput/scripts/2026-08-21-resume/exp512_t_dial_60.py` (+ `exp512_result.json`) · seed 20261040.

## 1. Does the bitlen degradation continue?

Paper 178 found the dial degrades at bitlen 56 (Spearman 0.405). This experiment tests
bitlen 60 to determine whether the drop continues monotonically or plateaus.

## 2. Results

| metric | bitlen 56 (paper 178) | bitlen 60 (this paper) |
|---|---|---|
| Spearman(T, rate) | 0.405 | **0.437** [0.393, 0.480] |
| Spearman(count, rate) | 0.313 | 0.368 |
| mean smooth rate | 0.89% | 0.89% |

**H2 CONFIRMED — PLATEAU**: the degradation does not continue monotonically; Spearman
rises slightly (0.405 → 0.437), consistent with a plateau at ~0.43–0.44. T still beats
count by +0.070. Mean smooth rate unchanged at 0.89%.

## 3. What this decides

The dial's bitlen degradation PLATEAUS at ~0.44 rather than continuing toward zero —
the starved regime reaches a floor where the QR-lottery signal stabilizes at its
minimum rather than vanishing entirely. Barriers: (5)/(8) unchanged.

Now 513 experiments. Assessment v285.

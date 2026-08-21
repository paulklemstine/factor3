# Paper 108 — TRACE-BATTERY: Joint Channel Capacity Scaling Verified

**Verdict name: THE-SCALING-IS-CONFIRMED.**
Round-30 #4 · exp 444 · assessment v218 · script `/tmp/exp_tracebattery.py` · log `/tmp/r30n4b.log` · runtime 80 s.

## 1. What was measured

The joint channel capacity I(N mod M; all codes) for increasing subsets of the 6-dial battery, on a fresh 30k population (independent of paper 94's original run):

| moduli subset | M | I(joint) |
|---|---|---|
| S₃a@31 + S₃b@23 | 713 | 7.9455 |
| + A₄@9 | 6 417 | 10.4462 |
| + D₄@8 | 51 336 | 12.1080 |

## 2. Per-dial trace information

I(s mod mᵢ; codeᵢ) varies enormously across dials:

| dial | I(s mod mᵢ; codeᵢ) |
|---|---|
| C₅@11 | 3.4584 |
| A₄@9 | 1.7896 |
| D₄@8 | 1.4967 |
| F₂₀@5 | 0.4818 |
| S₃b@23 | 0.0523 |
| S₃a@31 | 0.0398 |

The S₃ fields carry almost no trace information individually (0.04–0.05 bits), while C₅ carries 3.46 bits — an 80× range. This is consistent with paper 99's finding that S₃ sum/gap views individually carry ~4% of the channel.

## 3. What this verifies

The joint capacity scaling (7.95 → 10.45 → 12.11) confirms paper 94's results on an independent population. The which-factor wall on the full code set (0.4677 bits) is in the sparse-table regime and consistent with the bias levels documented in papers 93 and 102.

Now 444 experiments. Assessment v218. Paper 108, issue #200.

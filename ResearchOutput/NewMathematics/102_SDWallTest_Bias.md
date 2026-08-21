# Paper 102 — SD-WALL-TEST: The Hinted View Is Factor-Blind Too

**Verdict name: THE-HINTED-VIEW-IS-BLIND.**
Round-30 #2 · exp 437 · assessment v213 · script `/tmp/exp_sdwall.py` · log `/tmp/r30n2.log` · runtime 6 s.

## 1. The queued test

Paper 101's (s,d)-view — the factor-residue hint view — read a which-factor statistic of 0.9663 bits, far above every product-view wall, in the extreme sparse-plug-in regime (~28 947 residue-pair cells vs 30k samples). Flagged, not interpreted. This round runs the 200-shuffle permutation null.

## 2. The verdict

| view | observed | null mean | null sd | z |
|---|---|---|---|---|
| product view (N mod 713) | 0.0153 | 0.0162 | 0.0008 | −1.04 |
| **(s,d) view** | **0.9663** | **0.9648** | 0.0011 | **+1.36** |
| joint labels | 0.0011 | 0.0008 | 0.0002 | +1.44 |

**All three views sit inside their nulls.** The entire 0.97-bit (s,d)-view reading was sparse-plug-in inflation — the hint view's massive cell count against the sample size generates ~0.96 bits of pure estimator bias, which the null reproduces exactly.

## 3. What stands

The battery programme's factor-blindness now extends to its strongest view: the factor-residue hint view that carries 4.56 of the 4.60 label-entropy bits (paper 101) is factor-blind at permutation-null sensitivity (±0.001 bits on this statistic). The full chain — capacity (92), ceiling saturation (94), hint compounding (101), and now verified blindness on every view including the hinted one — is closed with no loose ends.

Now 437 experiments. Assessment v213. Paper 102, issue #194.

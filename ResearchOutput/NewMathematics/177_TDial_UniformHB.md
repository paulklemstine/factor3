# Paper 177 — T-DIAL-UNIF-HB: The Dial Holds at the Intersection of Regime and Bitlen

**Verdict name: DIAL-HOLDS-UNIFORM-HB (+ K-WASHOUT pilot lesson).**
Round-48 #2 (cron iteration) · exp 510 · assessment v284 · script `ResearchOutput/scripts/2026-08-21-resume/exp510_t_dial_unif_hb.py` (+ `exp510_result.json`) · seeds 20261020–23.

## 1. The intersection cell

Paper 175 confirmed bitlen-stability on balanced draws; paper 166 confirmed regime-invariance at bitlen 44. The intersection — uniform draws × bitlen {44, 48} — was the open cell.

## 2. Results

Spearman(T, rate) = 0.686/0.656/0.553/0.561 across the four cells (balanced/uniform × 44/48); T beats count by +0.06–0.10 everywhere, CI excludes zero in all cells. H1/H2 pass.

**K-WASHOUT pilot**: multiplier-randomized relation samplers destroy the QR dial channel entirely (averaging over k equidistributes the characters, canceling N-dependence). Fixed k=1 CFRAC ladder required.

## 3. What this decides

The zero-fit dial survives the intersection of both axes. Barriers: (5)/(8) unchanged.

Now 512 experiments. Assessment v284.

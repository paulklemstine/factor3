# Paper 195 — DEPTH-DECAY: The Magnitude Channel Sees Only the First Steps

**Verdict name: DEPTH-DECAY-TO-NULL-BY-T5 (per-step information real through b₃, marginal at b₄, gone by b₅).**
Round-70 #4 · exp 550 (coordinator inline reanalysis) · assessment v302 · script `ResearchOutput/scripts/2026-08-21-resume/exp550_depthdecay.py` (+ `exp550_depthdecay.json`) · population reuse seed 20260823 (disclosed).

## 1. Question

Paper 193 established that the Fermat-window magnitude spectrum carries 0.184 bits about
the first Berggren branch letter b₁. Does the channel persist along the descent — could
it guide ascent beyond one step?

## 2. Unconditional decay

MI(x_f1_w4096_hratio ; b_t), 12 feature bins, 150-shuffle nulls, all rows with depth ≥ t:

| t | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| MI | .1836 | .1433 | .0940 | .0777 | .0540 | .0404 | .0322 | .0192 |
| z | +114 | +81 | +50 | +43 | +30 | +20 | +16 | +9 |

Roughly halving every two levels. Re-ascent pipeline check exact 3000/3000.

## 3. The honest conditional test

Unconditional MI overstates persistence (marginals co-vary through ρ). Conditioning on
the path prefix — shuffle WITHIN each prefix group (≥60 rows), weighted MI — gives the
true per-step information:

| t | MI cond | within-prefix null | z |
|---|---|---|---|
| 2 | 0.0900 | 0.0124 | **+32.3** |
| 3 | 0.0646 | 0.0335 | **+6.7** |
| 4 | 0.0640 | 0.0490 | +2.7 (edge) |
| 5 | 0.0487 | 0.0473 | **+0.2 (null)** |

Depth itself is also visible: MI(feature ; dB 12-bin) = 0.1106 (z=+19.6), though
corr(feature, log dB) = −0.13 is weak.

## 4. Mechanism coherence

A fixed W-probe window resolves the Fermat distance d ≈ n/(2ρ) only to O(W) resolution
— i.e., it reads the COARSE Gauss-map digits of the ratio ρ. The first 2–3 branch
letters ARE those coarse digits; deeper letters encode progressively finer digits no
fixed-budget window can see. The channel is a coarse Gauss-prefix sensor, exactly as
the positional mechanism predicts.

## 5. Round synthesis (papers 193–195)

The energy-ascent question is now closed at three strengths, mirroring the original
Berggren closure: (i) the channel EXISTS (non-residue magnitude family, joins paper
137's position row); (ii) its ASCENT VALUE is priced below breakeven (paper 194: even
α-persistent oracles need α*≥0.85 vs exact Fermat); (iii) it is DEPTH-LIMITED (this
paper: per-step info dies by depth 4–5). The Pythagorean tree remains factoring-sealed
in practice: any N-computable window sensor sees the first few ratio digits and nothing
more; recovering the full path string from magnitudes would require resolving Gauss
digits at every depth — the scan cost again.

Ledger: population reused from exp546 (disclosed); unconditional-vs-conditional gap
itself is a finding (marginal co-variation inflates naive depth persistence claims).

Now 550 experiments. Assessment v302.

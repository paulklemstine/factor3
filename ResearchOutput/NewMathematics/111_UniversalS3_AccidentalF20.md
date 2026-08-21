# Paper 111 — UNIVERSAL-S₃-TEST: An Accidental Measurement of x⁵−2 at Small Conductors

**Verdict name: THE-WRONG-POLYNOMIAL-STILL-INFORMS.**
Round-32 #2 · exp 444 · assessment v222 · script `/tmp/exp_universals3.py` · log `/tmp/r32n2b.log` · runtime 5 s.

## 1. What happened

The round intended to verify the type-channel law for x³−2 (S₃, disc −108). Instead, the coefficient vector `(-2, 0, 0, 0, 0, 1)` encodes **x⁵−2** (degree 5), not x³−2 (degree 3). The measurements are valid for x⁵−2 but don't test the universal-S₃ hypothesis.

## 2. What was measured (and what it tells us)

x⁵−2's type channel at small conductors:

| modulus | I(p mod m; T) | interpretation |
|---|---|---|
| 3 | **0.0000** | conductor ≠ 3 confirmed |
| 7 | 0.0005 | negligible |
| 9 | 0.0004 | negligible |
| 13 | 0.0015 | negligible |

Root-count histogram {0: 1306, 1: 4915, 5: 319} — consistent with F₂₀'s expected splitting behavior (paper 82).

The zero MI at all tested moduli confirms that x⁵−2's splitting type is invisible from small-conductor residues — consistent with paper 82's finding that the F₂₀ dial's conductor is m\* = 5 (not 3, 7, 9, or 13).

## 3. The universal-S₃ hypothesis remains untested

The x³−2 verification requires the CORRECT coefficients `(−2, 0, 0, 0, 1)` (degree 3). This remains open for a future round.

Now 444 experiments. Assessment v222.

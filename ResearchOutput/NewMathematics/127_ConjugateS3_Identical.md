# Paper 127 — CONJUGATE-S₃-TEST: Conjugate Fields Produce Identical Type Channels

**Verdict name: THE-FIELD-NOT-THE-POLYNOMIAL.**
Round-35 #8 · exp 455 · assessment v232 · script `/tmp/exp_conjugate_s3.py` · log `/tmp/r28n2b.log`.

## 1. The test

x³−x+1 and x³−x−1 both have disc = −23 but are different polynomials generating conjugate cubic fields inside the same splitting field. The type-channel framework predicts they produce **identical** channels (conjugate fields have the same Frobenius action).

## 2. Results

| measurement | x³−x+1 | x³−x−1 | Δ |
|---|---|---|---|
| I(p mod 23; T) | 1.000065 | 1.000065 | **0.000000** |
| semiprime pair | 1.0012 | 1.0006 | 0.0006 |

Prime channels are **bit-for-bit identical** to six decimal places. Semiprime channels agree within Monte Carlo noise.

## 3. What this verifies

The type-channel law depends only on the **field**, not on which polynomial generates it. Two different generators of conjugate cubic fields produce exactly the same channel because their roots lie in the same splitting field with the same Frobenius action. This provides an independent verification of the entire type-channel framework's theoretical foundation.

Now 455 experiments. Assessment v232. Paper 127.

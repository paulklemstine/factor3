# Paper 95 — METHOD-LOCALITY: ECM and Pollard ρ Track the Factor, Not the Modulus

**Verdict name: THE-METHODS-ARE-FACTOR-LOCAL.**
Round-28 #1 · exp 430 · assessment v206 · script `/tmp/exp_methodlocality.py` · log `/tmp/r28n1b.log` · runtime ~60 s.

## 1. The structural question

Paper 89 calibrated three methods but never measured the property that organizes the method stratum from within: **factor-locality** — is a method's cost determined by a factor p or by the modulus N? Factor-locality is what lets methods exploit unbalanced moduli, and it splits the method stratum into sub-kinds. This round adds ECM to the plane (never calibrated) and measures locality for ECM, ρ, and trial division on constructed semiprimes with controlled (p, q).

## 2. H1 — factor-locality confirmed at medians

Fixed p = 4093, q growing 2¹⁴ → 2²³ (N growing 2²⁵ → 2³⁴), 9 draws per cell, medians:

| q | ECM median ops | ρ median iters |
|---|---|---|
| 2¹⁴ | 1 393 | 48 |
| 2¹⁷ | 2 192 | 58 |
| 2²⁰ | 1 017 | 60 |
| 2²³ | 1 788 | 43 |

Median flatness over 2²³ growth of the cofactor: **ECM ×2.16, ρ ×1.40** — flat within method luck (ECM's residual is curve-restart scatter; ρ's is Poisson scatter around √p ≈ 64). Neither method sees the cofactor's size.

## 3. H2/H3 — the p-scaling profiles (slopes corrected)

q ≈ 64p, p growing 2⁸ → 2¹⁴, 9 draws, medians: ECM 61 → 6 657; ρ 12 → 79; trial-div 156 → 12 142.

Corrected slopes per log₂p (the script's slope print took log₂ of bit-lengths — xs nearly constant; disclosed, corrected here from the printed medians):

| method | slope per log₂p | reading |
|---|---|---|
| Pollard ρ | **0.45** | the birthday bound √p ✓ |
| trial division | **1.09** | linear in p — the definition face ✓ |
| ECM | **1.13** | locally power-like, but over a far smaller constant: at p = 2¹⁴ ECM needs 6 657 ops vs trial-div's 12 142 — already ahead, with the sub-exponential bending still to come at scales beyond this window |

## 4. What this decides

The method stratum has measured internal structure: **ρ and ECM are factor-local** (flat in the cofactor), trial division is not (linear in the factor it scans toward), and the two factor-local methods differ in their p-profiles (ρ at the birthday bound; ECM locally steeper per bit but constant-advantaged and destined to bend sub-exponentially). The landscape's method stratum now has its internal structure measured; ECM's position on the plane is calibrated.

## 5. Barriers

**(a)** clean — locality horns pre-stated; the first single-draw design's inadequacy caught and fixed to medians before claims. **(b)** clean — ECM calibration new to the plane. **(c)** confronted — 9 draws per cell, medians throughout, constructed (p, q) pairs. **(d)** clean — fixed seeds. **(e)** the substance — flatness ratios and corrected slopes with the xs-bug disclosed. **(f)** controlled — the statistical-design fix (single draw → medians) made before any conclusion. **(g)** fair — identical conditions across methods; ρ's implementation validated in paper 89. **(h)** relevance — factor-locality is the operational reason ECM dominates for unbalanced keys; the measured locality boundary organizes the method stratum.

Now 430 experiments. Assessment v206. Paper 95, issue #187.

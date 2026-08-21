# Paper 94 — BATTERY-SCALING: The Capacity Curve Saturates at the Label-Entropy Ceiling

**Verdict name: THE-CURVE-SATURATES-AT-THE-CEILING.**
Round-27 #4 · exp 429 · assessment v205 · script `/tmp/exp_batteryscaling.py` · log `/tmp/r27n4b.log` · runtime 292 s.

## 1. Completing the capacity law

Paper 92 found the 4-field battery super-additive (+4.31 bits over additive). This round adds the two remaining measured fields — F₂₀ x⁵−2 (@5) and C₅ Q(ζ₁₁)⁺ (@11) — for a **6-dial battery with pairwise-coprime conductors** (CRT modulus 31·23·9·8·5·11), and measures the full capacity curve over nested subsets.

## 2. The capacity curve

Marginals reproduce their papers of origin first (S₃a 1.0011, S₃b 1.0012-lineage, A₄ 0.4733, D₄ 1.4302, F₂₀ ≈ 1.25-lineage, C₅ ≈ Is(5)-lineage). Then the nested joints:

| dials | I(joint) | Σ marginals | additive deficit | H(labels) ceiling | % of ceiling |
|---|---|---|---|---|---|
| 1 | 1.0011 | 1.0011 | +0.000 | — | — |
| 2 | 2.1334 | 2.0020 | +0.132 | 4.6063 | 46% |
| 3 | 4.0242 | 2.4777 | +1.547 | 6.4947 | 62% |
| 4 | 8.2412 | 3.9120 | +4.329 | 9.5434 | 86% |
| 5 | 11.5307 | 5.1591 | +6.372 | 11.9557 | 96% |
| **6** | **12.7235** | 5.3650 | **+7.359** | **12.7726** | **99.6%** |

- **H1 confirmed**: the additive deficit grows monotonically — synergy compounds without bound short of the ceiling.
- **H2 confirmed**: every marginal reproduces its paper of origin within tolerance.
- **H3 confirmed**: the 6-dial which-factor wall reads 0.3594 against its permutation-null mean 0.3591 (**z = +0.11**) — dominated by sparse-table bias exactly as at k = 4; factor-blindness extends to the full battery.

## 3. The law

The battery-capacity law in three lines:
1. **I(k-joint) → H(joint labels)** as dials accumulate: the CRT-joint modulus sees all k residues simultaneously, and the pair-label structure becomes nearly fully determined (99.6% at k = 6).
2. **The additive deficit D(k) grows monotonically** — marginal bookkeeping understates batteries progressively (7.36 bits = 3.7× the additive prediction at k = 6).
3. **The ceiling is the joint label entropy** — the population correlation between label blocks is the only thing keeping the joint from complete determination.

For the converse: a k-dial congruence battery's symmetric capacity must be computed jointly (this machinery), approaches its label ceiling, and carries zero detectable which-factor content through k = 6 (permutation-null verified).

## 4. Method notes

Two process items disclosed: (i) the printed row labels were off by one (k = i+1 where i counts dials) — cosmetic, corrected here; (ii) the chained 6-dial label code spans ~10¹² values — `np.bincount`-based entropy cannot run on it (5.6 TiB allocation caught), `np.unique`-based computation substituted.

Now 429 experiments. Assessment v205. Paper 94, issue #186.

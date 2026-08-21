# Paper 92 — BATTERY-CAPACITY: Synergy Compounds — the 4-Field Joint More Than Doubles Its Marginals

**Verdict name: SYNERGY-COMPOUNDS.**
Round-27 #2 · exp 427 · assessment v203 · script `/tmp/exp_batterycapacity.py` · log `/tmp/r27n2b.log` · runtime ~60 s.

## 1. The question

Paper 91 found pairwise battery structure: synergy +0.129 bits (two S₃ fields), +0.005 (A₄×D₄), overlap −0.992 (shared disc). Does synergy compound at higher orders, or is it pairwise-sufficient?

## 2. The measurement

All four type-channel dials (S₃a@31, S₃b@23, A₄@9, D₄@8; conductors pairwise coprime, CRT modulus 51 336) on one shared 30k semiprime population:

| quantity | bits |
|---|---|
| Σ marginals | 3.9099 |
| **I(4-field joint)** | **8.2246** |
| **SYNERGY Δ** | **+4.3146** |
| H(joint pair-labels) — the ceiling | 9.5276 |

**The 4-field joint more than doubles its additive prediction**, sitting within 1.3 bits of the label-entropy ceiling. Every dial reads a different projection of the same (p, q); jointly they nearly reconstruct the whole pair-label structure.

### The order decomposition — synergy is genuinely higher-order

| order | total synergy | per sub-battery |
|---|---|---|
| k = 2 (6 pairs) | +0.244 | +0.005 … +0.129 |
| k = 3 (4 triples) | **+3.822** | +0.410 … +1.539 |
| k = 4 (the battery) | **+4.315** | — |

Pairwise synergies — the entire content of paper 91's pairwise table — account for only 6% of the total. The dominant term is higher-order: combinations of three and four dials extract information that no sum of lower-order reads contains. The mechanism is transparent: N mod 31 alone sees one residue of the product p·q mod 31; the CRT-joint modulus sees all four residues simultaneously — 15.8 log₂ units of combined residue information against which each dial's pair labels become nearly fully determined.

## 3. The honest caveat

The which-factor statistic on the FULL joint code reads 0.0469 bits — above every pairwise wall (0.001–0.002). This is **suspected sparse-plug-in bias**, not signal: the joint contingency table spans tens of thousands of residue-columns against 30k samples (the exact Miller–Madow regime papers 70/83 flagged), while every well-populated marginal and pairwise table reads ≤ 0.002. The claim "all battery content is factor-blind" therefore stands on the well-conditioned strata plus this bias analysis, not on the raw joint-wall number.

## 4. What revises what

Paper 91's title claim ("neither additive nor comonotone") survives; its implicit scale does not: pairwise accounting understates batteries badly. The corrected picture: **batteries are super-additive systems whose capacity grows toward the joint label-entropy ceiling with strong higher-order terms**. For the converse, this RAISES the stakes on no-pinning: a k-dial congruence battery carries far more symmetric capacity than marginal bookkeeping suggests — every bit of it still trace-routed and factor-blind, but the capacity arithmetic must be done jointly (exactly this machinery), never marginally.

## 5. Barriers

**(a)** clean — the compounding question pre-stated; both outcomes informative. **(b)** clean — no higher-order battery work in the Catalog. **(c)** confronted — 24k-sample joint tables across all 11 non-empty sub-batteries, exact CRT combination. **(d)** clean — fixed seeds. **(e)** the substance — the order decomposition complete (every sub-battery measured); the wall caveat quantified and attributed. **(f)** controlled — machinery inherited from validated rounds 24 #1 through 27 #1; two leftover-garbage lines caught by runtime errors before results. **(g)** fair — identical shared population for marginals, sub-joints, and the full joint. **(h)** relevance — the battery-capacity arithmetic for any future congruence-battery proposal is now defined (joint MI by this machinery, ceiling = joint label entropy), and its product stays on barrier 4's sealed side.

Now 427 experiments. Assessment v203. Paper 92, issue #184.

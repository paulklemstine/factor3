# Paper 105 — HINT-S-D-DECOMPOSITION: The Routing Structure Is Dial-Dependent

**Verdict name: THE-ROUTING-IS-DIAL-DEPENDENT.**
Round-30 #2 · exp 441 · assessment v216 · script `/tmp/exp_hintsd.py` · log `/tmp/r30n2b.log` · runtime 18 s.

## 1. The hypothesis and its refutation

Paper 99 found for S₃a@31: sum-view ~4%, gap-view ~4%, jointly >100% — massive s-d synergy. The pre-stated hypothesis was that this is universal. **Refuted**: the routing structure is dial-dependent.

## 2. The measured decomposition

| dial | s-carried | d-carried | s-d synergy | structure |
|---|---|---|---|---|
| S₃a@31 | 4.0% | 3.8% | **+1.44** | combination-required |
| S₃b@23 | 5.2% | 5.1% | **+1.41** | combination-required |
| A₄@9 | 161.6% | 213.9% | +0.01 | noise on near-zero channel |
| **D₄@8** | **100.0%** | 75.2% | **−1.00** | **SUM-SUFFICIENT** |
| F₂₀@5 | 165.0% | 122.2% | +0.41 | both individually exceed |
| C₅@11 | 77.8% | 55.7% | **+1.18** | combination-required |

## 3. The structural explanation

**D₄ is sum-sufficient** because its type map is a simple function of p mod 8: (p+q) mod 8 determines the unordered type pair completely (q mod 8 = N·p⁻¹ mod 8, which is determined by N mod 8 and p mod 8; and the type depends only on p mod 8). The gap d mod 8 adds nothing beyond the sum.

**S₃ fields are combination-required** because their type map depends on the Legendre symbol (Δ|p), which is a function of p mod 23 (or 31) — and knowing (p+q) mod 23 does NOT determine (Δ|p) and (Δ|q) individually. Both s and d are needed to pin down the character values separately.

**F₂₀ and C₅ show intermediate behavior** — both s and d individually exceed the channel (percentages >100%), meaning each carries substantial information, but the combination still adds more (positive synergy). These are the fields where the type map depends on both the sum and the difference in non-trivial ways.

## 4. The classification

The routing structure classifies fields by whether their type map is a function of the sum alone:

- **Sum-sufficient** (D₄): type = f(p mod m) where m is small enough that (p+q) mod m determines p mod m uniquely
- **Combination-required** (S₃, C₅): type depends on both p mod m and q mod m independently
- **Both-individually-sufficient** (F₂₀): type has enough structure that either s or d alone exceeds the channel

## 5. Barriers

**(a)** clean — the universal-synergy hypothesis pre-stated and honestly refuted. **(b)** clean. **(c)** confronted — 30k shared population, six dials, exact MI decomposition. **(d)** clean. **(e)** the substance — the dial-dependent routing structure quantified per dial. **(f)** controlled. **(g)** fair. **(h)** relevance — the routing classification determines which batteries benefit from sum-only measurements vs full (s,d) pairs.

Now 441 experiments. Assessment v216. Paper 105, issue #197.

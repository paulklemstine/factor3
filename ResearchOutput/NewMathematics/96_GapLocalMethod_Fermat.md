# Paper 96 — THE-GAP-LOCAL-METHOD: Fermat Completes the Locality Taxonomy

**Verdict name: THE-TAXONOMY-IS-COMPLETE.**
Round-28 #2 · exp 431 · assessment v207 · script `/tmp/exp_gaplocal.py` · log `/tmp/r28n2d.log` · runtime 1 s.

## 1. The missing member

Paper 95 split the method stratum by factor-locality: trial division p-linear, ρ and ECM factor-local (√p). The remaining classical method — **Fermat** — is neither: its iteration count is exactly **(p+q)/2 − √N**, a function of the *gap* q − p. This round verifies that identity and measures Fermat's interpolation between the locality classes.

## 2. Results

### H1 — the identity, exact
Fermat iterations = (p+q)/2 − ⌊√N⌋-based count verified on **24/24** constructed draws (per-draw instrumentation; e.g. draw 0: p=2371, q=7121, predicted = measured = 637).

### H2 — gap-local interpolation
Fixed p = 4093, balance ratio r = q/p swept:

| r | Fermat iterations | in √p units | in p units |
|---|---|---|---|
| 2 | 352 | 5.59 | 0.09 |
| 4 | 2 049 | 32.52 | 0.50 |
| 8 | 6 844 | 108.63 | 1.67 |
| 16 | 18 422 | 292.41 | 4.50 |
| 32 | 44 384 | 704.51 | 10.84 |
| 64 | 100 282 | 1 591.78 | 24.50 |

Cost grows linearly toward the cofactor scale: at r = 64 the measured 100 282 is 0.78 of the cofactor-linear limit p·(r−1)/2 — Fermat degrades toward "linear in the larger factor" exactly as the gap formula predicts, interpolating between the factor-local methods (flat in r) and the cofactor-scale regime.

### The degenerate square case (bonus finding)
The r = 1 row of the first grid exposed a structural degeneracy: when q lands on p itself (N = p²), Fermat's target a = (p+p)/2 = p lies **below** its starting point ⌊√N⌋ + 1 = p + 1 — the algorithm has no true stopping point and only exits by accidentally hitting an unrelated square (here after 8 372 232 iterations). Perfect-square-of-prime moduli are a structural blind spot of plain Fermat — worth knowing wherever Fermat-style walks are embedded (e.g., CFRAC's continued-fraction generalization does not share it).

## 3. The completed locality table

| method | locality class | cost |
|---|---|---|
| trial division | p-linear | p |
| Pollard ρ | factor-local | √p |
| ECM | factor-local | sub-exp in p |
| **Fermat** | **gap-local** | **(p+q)/2 − √N** |

Four methods, three locality classes. Which methods see the factor (ρ, ECM), which see the gap (Fermat), and which see nothing but the scan (trial division) — the method stratum's internal structure is fully mapped.

## 4. Method ledger

Two process catches: (i) the round's first launch hung for 7+ minutes inside H1 — root cause found by faulthandler stack dump: **the fermat loop lacked its increment** (`a += 1` lost between drafts), spinning on a constant value; the standalone control that caught it ran the identical body with the increment present; (ii) the instrumented rerun asserted `ok == 40` against a 24-draw loop — stale constant, fixed. Also disclosed: the r = 1 row measures N = p² (construction lets q land on p) — reported as the degenerate finding above rather than silently dropped.

## 5. Barriers

**(a)** clean — horns pre-stated; the hang investigated to root cause rather than worked around. **(b)** clean. **(c)** confronted — exact identity on 24 draws, seven-point interpolation, exact σ₁-style checks. **(d)** clean — fixed seeds. **(e)** the substance — per-draw instrumentation, the degenerate case documented. **(f)** controlled — faulthandler diagnosis; both catches before claims. **(g)** fair — ρ-scale reference (√p) computed identically. **(h)** relevance — completes the method stratum's internal map (papers 89 + 95 + this): every classical method now has a measured locality class, and the gap-local class's degradation path is quantified.

Now 431 experiments. Assessment v207. Paper 96, issue #188.

# factor3 — Factoring Research Lab

Computational investigation into integer factorization complexity: testing whether
any naturally-defined invariant computable from `N = pq` alone can reveal `p` and
`q` in polynomial time.

**Status:** 284 computational experiments across sixty-plus mathematical paradigms.
All novel classical factoring hypotheses were refuted. The investigation produced a
barrier framework (8 structural barriers, 3 proven as theorems) and 11 research papers
of independent mathematical interest.

## Research papers (`ResearchOutput/NewMathematics/`)

| # | Paper | Status |
|---|-------|--------|
| 01 | [Power-Sum GCD Factoring & Carmichael Periodicity](ResearchOutput/NewMathematics/01_PowerSum_GCD_Factoring.md) | Proven; O(N^{3/2}) |
| 02 | [Three Structural Barrier Theorems](ResearchOutput/NewMathematics/02_Structural_Barrier_Theorems.md) | Proven theorems; polynomial barrier machine-checked in Lean |
| 03 | [The "Only Bad Primes" Conjecture is False](ResearchOutput/NewMathematics/03_Denominator_Primes_EC.md) | Conjecture refuted |
| 04 | [Jacobi Gauss-Sum Phase Collapse](ResearchOutput/NewMathematics/04_Gauss_Sum_Phase_Collapse.md) | Proven (1 bit) |
| 05 | [The 3SUM–Birthday-Bound Hierarchy](ResearchOutput/NewMathematics/05_ThreeSUM_Birthday_Bound.md) | Proven scaling |
| 06 | [A Knot–Number Theory Bridge](ResearchOutput/NewMathematics/06_Knot_Number_Theory_Bridge.md) | Proven; exponential cost |
| 07 | [Singular Moduli Factoring and the √N Barrier](ResearchOutput/NewMathematics/07_Singular_Moduli_Scaling.md) | Works; √N scaling |
| 08 | [The Structural Orthogonality Framework](ResearchOutput/NewMathematics/08_Structural_Orthogonality_Framework.md) | 8-barrier synthesis |
| 09 | [The Quantum-Classical Boundary](ResearchOutput/NewMathematics/09_Quantum_Classical_Boundary.md) | Two independent classical barriers to period-finding |
| 10 | [A Conditional-Impossibility Framework](ResearchOutput/NewMathematics/10_Conditional_Impossibility_Framework.md) | Conditional impossibility schema |
| 11 | [The CRT-Split No-Go](ResearchOutput/NewMathematics/11_CRT_Split_Iteration_NoGo.md) | N-alone iteration cannot factor in poly(log N) |
| 00 | [Consolidated Breakthrough Report](ResearchOutput/NewMathematics/00_CONSOLIDATED_BREAKTHROUGH_REPORT.md) | Synthesis of all papers |
| 12 | [Subagent Batch Closures](ResearchOutput/NewMathematics/12_Subagent_Batch_Closures.md) | 8 novel hypotheses tested and closed (experiments 285-292) |
| 13 | [The Free-Witness Family](ResearchOutput/NewMathematics/13_FreeWitness_Family.md) | CIRC/KROOT/BQF — the binary-quadratic-form count family (barrier 4) |

The consolidated report is the authoritative record of all novel mathematics from
the 292-experiment investigation.

## Contents

- `ResearchOutput/NewMathematics/` — the 13 papers + consolidated report
- `ResearchOutput/Factoring_Lab_Notebook.md` — the master experiment record (284 experiments)
- `ResearchOutput/Factoring_Assessment_Genuine_Breakthrough.md` — honest assessment (v61)
- `ResearchOutput/Factoring_Brainstorm_Unconventional.md`, `Factoring_Research_Synthesis.md` — planning documents
- `ResearchOutput/Exp_*.md` — individual experiment reports (Donoho-Stark, factorial number system, hypercomputation, information geometry, Ising, Langlands, Navier-Stokes, solenoid)
- `ResearchOutput/Lean/PolynomialBarrier.lean` — the polynomial barrier theorem, machine-checked in Lean 4
- `REPORT_*.md`, `TROPICAL_FACTORING_REPORT.md` — experiment reports
- `*.py` — experiment scripts (donoho-stark, hypercomputation, information
  geometry, Ising, Langlands, Navier-Stokes, solenoid, tropical, rep-theory, ...)
- `ResearchOutput/factoring_experiments*.py` — the experiment harness scripts

## Honest bottom line

No classical polynomial-time factoring algorithm was found. The barrier framework
explains why every tested classical approach fails; the only poly(log N) factoring
known is Shor's (quantum). The papers document genuine new mathematics discovered
along the way — theorems, refutations, and structural classifications — without
claiming a classical factoring breakthrough that does not exist.

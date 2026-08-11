# Round-7 Hypothesis Closures: Scoping the Noise-Floor Principle and the Trace-Lemma Frontier

**Program:** Factoring research lab — round-7 subagent batch synthesis
**Date:** 2026-08-11
**Status:** Negative-results synthesis — round-7 attacks closed; the framework's scope made precise

---

## Abstract

A seventh brainstorm subagent attacked the framework's remaining precise gaps:
barrier-2-invariant character aggregates, the noise-floor principle's scope,
structural (non-numeric) witnesses, and geometry-of-numbers on N's digits. All
four were tested and closed (experiments 325-328). The round produced two
important refinements: the noise-floor principle is a bound on ATOMIC UNIFORM
primitives (not correlated/derived samples), and structural witnesses lie
outside the trace lemma's numeric scope but are sealed by aggregation and
circularity. Seven subagent rounds (~36 hypotheses) are now closed.

---

## 1. The batch at a glance

| # | Hypothesis | Attack | Verdict |
|---|-----------|--------|---------|
| 1 | AGREEMENT | Legendre-agreement count (barrier-2 invariant) | refuted — collapses to phi(N)/2 by character orthogonality |
| 2 | STATICRHO | rho-sample collision density vs noise floor | refuted-with-refinement — principle scoped to atomic-uniform primitives |
| 3 | ZDG | zero-divisor graph structural witness | refuted — structural, outside trace-lemma numeric scope, sealed by 4/6 |
| 4 | DIGITLATTICE | digit-convolution lattice (geometry-of-numbers) | refuted — target at Gaussian heuristic; carry constraint = BDPC |

---

## 2. AGREEMENT (experiment 325): barrier-2-invariant aggregates collapse

A(N) = #{a in (Z/NZ)* : (a/p)_2 = (a/q)_2} is invariant under BOTH barrier-2
symmetries (p<->q swap, conjugation). Verified: A(N) = phi(N)/2 exactly for all
tested semiprimes, and the agreement set IS the quadratic-residue set mod N —
the aggregate collapses by character orthogonality ((a/p)(a/q) = (a/N)_2) to the
N-computable quadratic character. Barrier 2 holds in its sharpest form: no
both-symmetries-invariant character aggregate escapes the residue/order
classification (barrier 6/5).

---

## 3. STATICRHO (experiment 326): scoping the noise-floor principle

The static rho sample set x_{t+1} = x_t^2 + 1 mod N has factor-bearing density
~N^{-1/4} (at T ~ sqrt p) or ~1 (when the walk cycles) — ABOVE the noise-floor
N^{-1/2}. Measured: fraction 0.999/0.997/0.985 at T=5000. So the rho SAMPLE SET
(correlated) escapes the density form of the principle. But exploiting it
requires the pairwise-gcd aggregation (O(T^2) = trial-division floor, barrier 4)
or the rho shortcut (known method, barrier 8). REFINEMENT: the noise-floor
principle is a bound on the ATOMIC UNIFORM primitive (ADAPT: each query succeeds
with probability <= 1/p), NOT a density theorem over derived/correlated samples.
The sqrt(p)-vs-sqrt(N) gap is the known-method exception.

---

## 4. ZDG (experiment 327): structural witnesses outside the trace lemma

The zero-divisor graph of Z/NZ (vertices = nonzero zero-divisors, edge x~y iff
xy == 0 mod N) has |V| = p+q-2 with wings of sizes {q-1, p-1} — its isomorphism
class determines {p,q}. Verified: the two wings recover the factors, all
cross-wing edges present. This is a STRUCTURAL witness (a combinatorial object,
not a number) — outside the trace lemma's numeric scope (p+q, max(p,q),
residue/order vector). But building it costs O(N) gcd tests = trial division
(barrier 4), and the vertex set IS the divisor structure (barrier 6). The lemma
survives if 'witness' means a numeric value; structural witnesses are sealed by
4/6 circularity, not the trace classification itself.

---

## 5. DIGITLATTICE (experiment 328): geometry-of-numbers fails at the Gaussian heuristic

The digit-convolution equations, linearized via w_ij = p_i q_j, form a lattice L
built from N's digits. Verified: the target (p otimes q, c) satisfies the
equations, but its norm (2.4-7.5) is COMPARABLE to the Gaussian heuristic
sqrt(dim) (6.4-7.5) — the target sits AT the heuristic, so LLL returns a generic
short vector, not the factorization. The rank-1 + carry-integrality constraint
is the Theta(N)-state de-carrying DP (BDPC, closed). Factor-bearing lattice
points occur at density <= c/sqrt(N). Barrier 4 + noise floor.

---

## 6. Meta-lessons

1. **The noise-floor principle is precisely scoped.** It bounds atomic-uniform
   primitives, not correlated/derived samples. The rho walk's higher density is
   real but is the known-method exception (barrier 8), sealed by aggregation.
2. **Structural witnesses are a genuine gap in the trace lemma's letter.** The
   zero-divisor graph determines {p,q} as a combinatorial object — outside the
   lemma's numeric scope — but sealed by O(N) aggregation and circularity.
3. **Barrier 2 survives in its sharpest form.** Both-symmetries-invariant
   character aggregates collapse to the quadratic character (phi(N)/2).
4. **Digit-coordinates do not escape the floor.** The lattice relaxation loses
   the carry information; the target sits at the Gaussian heuristic.
5. **Seven rounds, ~36 hypotheses, 328 experiments.** The framework is intact
   and its claims are now precisely scoped. No poly(log N) algorithm emerged.

---

*Related:* `16_FreeWitness_Classification.md`, `20_Round6_Closures.md`,
`21_Program_Synthesis.md`, `Factoring_Lab_Notebook.md` Parts 72-75.

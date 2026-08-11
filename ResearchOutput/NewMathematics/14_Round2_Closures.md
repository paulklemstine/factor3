# Round-2 Hypothesis Closures: Six Novel Classical Factoring Hypotheses, Tested and Closed

**Program:** Factoring research lab — round-2 subagent batch synthesis
**Date:** 2026-08-11
**Status:** Negative-results synthesis — 6 hypotheses closed, 3 subagent claims corrected

---

## Abstract

A second brainstorm subagent proposed six novel hypotheses targeting genuinely
less-mined territory (finite groups, modular groups, Hensel towers,
quantum-information analogs, Kolmogorov structure, cyclotomic towers). All six
were implemented, run, and closed (experiments 296-301). Five collapsed to the
known barriers as predicted; three of the subagent's load-bearing mathematical
claims were DISPROVEN by the experiments (the cusp-count formula, the Wigner
flatness, and the Wigner CRT factorization) — a reminder that computational
verification is essential. Combined with round 1, the barrier framework has
now survived 301 experiments.

---

## 1. The batch at a glance

| # | Hypothesis | Object | Verdict |
|---|-----------|--------|---------|
| 1 | HEISENBERG-CLASS | conjugacy classes of the Heisenberg group over Z/NZ | refuted — group-theoretic free-witness (barrier 4) |
| 2 | CUSP-INDEX | Gamma_0(N) index and cusp count | refuted — modular free-witness; cusp formula CORRECTED |
| 3 | TOWER-LIFT | Hensel lifting over N^k | refuted — no branching (unique lifts) |
| 4 | WIGNER-CUBIC | cubic-phase Wigner function | refuted — both claims DISPROVEN |
| 5 | STRUCT-KOLM | Kolmogorov structure function | refuted — no compression gap (vacuous) |
| 6 | CYCLOTOWER | gcd(N, Phi_m(2)) tower | refuted — Pollard p-1 in cyclotomic dress (barrier 8) |

---

## 2. HEISENBERG-CLASS (experiment 296): a group-theoretic free-witness

The discrete Heisenberg group H_N = {[[1,a,c],[0,1,b],[0,0,1]] : a,b,c mod N}
has a conjugacy class count K = sum_{a,b mod N} gcd(a,b,N). Verified:
K = N^2 + 3N + 1 + (N-1)(p+q) - (p+q)^2, and from K alone p,q are recovered
(solve the quadratic, then x^2 - sx + N). This is a NEW free-witness in
REPRESENTATION-THEORETIC form: symmetric in p<->q (dodges barrier 2),
non-polynomial (dodges barrier 1), sealed by O(N^2) aggregation cost
(barrier 4).

---

## 3. CUSP-INDEX (experiment 298): modular free-witness + a correction

Gamma_0(N)'s index in SL(2,Z) is psi(N) = N * prod_{l|N}(1+1/l) = (p+1)(q+1)
= N + p + q + 1. Verified; from the index, p+q = psi(N) - N - 1 recovers p,q.
Computing psi(N) needs the prime divisors (circular) or ~N coset enumeration
(barrier 4). CORRECTION: the subagent's cusp-count formula (p-1)(q-1)+3 is
WRONG — the correct count is sum_{d|N} phi(gcd(d, N/d)) = 4 for semiprimes
(verified). The claimed (p-1)(q-1)+3 is the cusp count of a different
subgroup, not Gamma_0(pq).

---

## 4. TOWER-LIFT (experiment 299): the Hensel tower is a no-op

For f(x) = x^2 - 1 over Z/N^kZ, the solution count c_k(N) is CONSTANT in k
(= 4 = gcd(2,p-1)gcd(2,q-1), the level-1 KROOT value): f'(u) = 2u is a unit
mod N, so every Hensel lift is unique — no branching, no per-prime signature.
For f with double roots (x^2 = N mod N^2), zero solutions lift. The tower
carries nothing beyond level 1.

---

## 5. WIGNER-CUBIC (experiment 300): both load-bearing claims DISPROVEN

The subagent's discrete Wigner function of a cubic-phase state, W(x,u) =
(1/N) sum_y omega^{2y^3 + 2(u+3x^2)y}, was claimed to have flat magnitude
|W| = 1/sqrt(N) and a CRT factorization W = (1/N) G_p(c) G_q(c). BOTH claims
are FALSE:
- |W| is NOT flat: at N=143 the sample magnitudes are {0.00, 0.02, 0.19, 0.13,
  0.06} (the cubic state is non-stabilizer; non-flatness is expected).
- The CRT factorization FAILS for N=143: exponential phase functions
  e^{2 pi i f(y)/N} do NOT decompose as products of mod-p and mod-q sums —
  only GROUP CHARACTERS factor through CRT, and a polynomial phase is not a
  character. (For N with p=3 the check "passed" only because both sides
  vanished.)
The object, correctly interpreted, is an O(N) free-witness aggregate (barrier 4)
that is N-only (barrier 5) — no factor-visible structure.

---

## 6. STRUCT-KOLM (experiment 301): no compression gap

The Kolmogorov structure function of N=pq has its knee at m = bitlen(p) +
bitlen(q). Verified: for balanced p,q, bitlen(p)+bitlen(q) == bitlen(N)
within O(1) (gap 0 or -1 bits across all tested) — the minimal sufficient
statistic (the factorization) costs as much as N itself, so the knee is
vacuous. Balanced semiprimes are incompressible; finding the pair costs
~sqrt(N) trial divisions (barrier 4).

---

## 7. CYCLOTOWER (experiment 297): Pollard p-1 in cyclotomic dress

The tower gcd(N, Phi_m(2)) for m = 1,2,3,... reveals a factor at the first
level m0 = min(ord_p(2), ord_q(2)) (verified exactly for all tested). Since
ord_p(2) ~ p ~ sqrt(N) for random p, the tower needs depth ~sqrt(N) — this is
exactly Pollard p-1, with the cyclotomic polynomials refining the exponent
ladder to extract the exact order instead of a multiple. Barrier 8 (known
method); subexponential only when p-1 is smooth.

---

## 8. Meta-lessons

1. **The free-witness theme dominates.** Across both rounds, the most common
   collapse is barrier 4: a scalar that encodes the factorization but costs
   O(N) or O(N^2) to aggregate. The free-witness family now spans norm-counts
   (CIRC), group-order counts (KROOT), binary-quadratic-form counts (BQF),
   group-class counts (HEISENBERG), and modular indices (CUSP-INDEX) — five
   structurally distinct settings, one mechanism.
2. **Computational verification catches subagent errors.** Three of the six
   round-2 hypotheses carried mathematical claims that the experiments
   DISPROVED (CUSP-INDEX cusp formula; WIGNER-CUBIC flatness and factorization).
   The experiment is the arbiter.
3. **Non-abelian and quantum-informational structures do not escape.** The
   Heisenberg group's class count is a free-witness; the cubic Wigner function
   has no factor-visible structure. The symmetries of every N-computable datum
   (p<->q swap, conjugation) persist across these settings.
4. **Iwasawa/cyclotomic towers reduce to known methods.** The level at which a
   factor appears is the multiplicative order — Pollard p-1 territory.
5. **The honest frontier.** 301 experiments, two subagent rounds, and a
   self-invented free-witness family later: the barrier framework is intact.
   Every novel classical hypothesis — algebraic, group-theoretic, modular,
   quantum-informational, information-theoretic — collapses to a known barrier.

---

*Related:* `12_Subagent_Batch_Closures.md` (round 1), `13_FreeWitness_Family.md`,
`Factoring_Lab_Notebook.md` Parts 42-47 (per-experiment records),
`00_CONSOLIDATED_BREAKTHROUGH_REPORT.md`.

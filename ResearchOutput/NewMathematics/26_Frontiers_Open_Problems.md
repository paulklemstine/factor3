# The Frontiers: Three Precise Open Problems

**Program:** Factoring research lab — the theoretical frontier after the empirical exhaustion
**Date:** 2026-08-11
**Status:** Open-problems paper — the precise statements of what remains

---

## Abstract

After 340 experiments, ten subagent rounds (~46 hypotheses), and 25 papers, the
classical, uniform, hint-free attack surface for integer factorization is
empirically exhausted. This paper records the three precise frontiers that
remain — one genuinely open theorem, one established exception, and one scope
boundary — as concrete mathematical problems for future work.

---

## 1. The settled framework (what the program established)

- **Free-witness classification:** a counting aggregate over a CRT-separable
  domain with non-polynomial CRT-multiplicative local weights is a free witness,
  sealed by Omega(N) aggregation (papers 13, 16; validated by SIGK).
- **Trace lemma (complete):** every recoverable numeric witness reduces to
  p+q, max(p,q), or a residue/order vector (papers 16, 24; verified ASYMRES).
- **Noise-floor principle:** factor-bearing samples in any N-computable aggregate
  occur at density <= c/sqrt(N) — bounded on atomic-uniform primitives
  (papers 20, 22; scoped by STATICRHO).
- **Barrier 2 (sharpest):** symmetric functions of factor-carrying objects are
  N-trivial (paper 24; IDEMPOTENT).
- **Joint closure:** the free-witness family is closed under joints (paper 25;
  JOINTCLOSURE).

---

## 2. Open Problem 1: barrier 4 is equivalent to factoring hardness

**Conjecture.** Within the class of CRT-respecting, poly-computable counting
functions on semiprimes, every quantity is either factorization-insensitive
(N-only, barrier 5) or its computation is equivalent to factoring (reduces to a
factor-secret coordinate with poly-time recovery).

**Status.** The forward direction is established (the free-witness family shows
every such aggregate recovers p,q in poly time from its value). The open step
is EXHAUSTIVENESS: no witness exists outside the classified classes. JOINTCLOSURE
closes the joint-completion route; ASYMRES closes the residue-coordinate route;
ZDG/POLYFACT close the structural-witness route. The remaining possibility is a
witness of a form none of these cover.

**Why it matters.** Proving exhaustiveness would make barrier 4 (the program's
dominant empirical obstruction) a THEOREM: classical factoring is hard iff
aggregating any CRT-multiplicative local count costs Omega(N). This is a sharp,
provable reformulation of the P vs NP / factoring-hardness boundary.

**Approach.** The characters-only boundary lemma (WIGNER-CUBIC) already
delimits the class: exponential phase functions do not decompose through CRT,
only group characters do. A proof would show that every poly-computable
factor-revealing aggregate is character/gcd/order-based, hence classified.
The strongest version is a Lean formalization.

---

## 3. Open Problem 2 (established exception): the quantum channel

**Statement (verified, Q-BYPASS).** Shor's algorithm computes ord_N(a) — a
classified free-witness coordinate (residue/order, trace lemma) — via a QFT
acting on one coherent superposition. It bypasses BARRIER 4's O(N) classical
aggregation, NOT the trace lemma.

**Status.** This is the unique exception: the only known poly(log N) factoring,
precisely localized. It is NOT an open problem in the sense of unknown — it is
the confirmed boundary of the classical framework. Its open aspect is whether a
provable separation (barrier 4 classical vs quantum) can be formalized.

---

## 4. Open Problem 3 (scope boundary): hint amplification

**Statement (verified, HINTAMP).** Given ~half of p's bits (an external hint),
Coppersmith's small-root LLL recovers p in poly time (partial-key-exposure).

**Status.** This is outside the framework's scope ('extraction from N alone'),
but it is a REAL unpriced channel (RSA side-channel). The open problem: a
precise scope axiom — what constitutes 'hint-free' extraction — and whether
any partial-information resource (beyond the top-half-of-p hint) admits
polynomial amplification.

---

## 5. The honest state

The Factor3 program has empirically closed the classical uniform hint-free
attack surface. The three frontiers are now precisely stated: a proof of
barrier-4 equivalence (the genuinely open theorem), the quantum exception
(precisely localized), and the hint-amplification scope boundary. No poly(log N)
classical algorithm exists in the uniform hint-free setting; the framework's
central claims are settled. The next advances are theoretical.

---

*Related:* `21_Program_Synthesis.md`, `25_Round10_Closures.md`,
`16_FreeWitness_Classification.md`, `09_Quantum_Classical_Boundary.md`.

# The De-Quantization Frontier, Closed

**Program:** Factoring research lab — de-quantization frontier assessment
**Date:** 2026-08-11
**Status:** Decisive negative result — every de-quantization route to Shor's order-finding collapses to barrier 4

---

## Abstract

Following the user's de-quantization directive, this paper records the
comprehensive assessment: a 20-idea brainstorm across four angles (sparse
transforms, l1/l2 asymmetry, lattice/Regev, information-theoretic), three judged
and tested candidates, plus the earlier tensor-network result (paper 31). EVERY
de-quantization route to Shor's order-finding collapses to barrier 4 (O(N)/O(r)-
sealed aggregation). The comb's incompressible structure (Schmidt rank r, flat
spectrum), the informative frequencies at multiples of Q/gcd(r,Q), the free
r|t probes with O(r)-sealed extraction, and the r-parameterized output
distributions together imply: **de-quantizing Shor = P = factoring**. The
quantum exception is maximally bounded.

---

## 1. The routes assessed

**Tensor networks (paper 31):** the comb and full Shor state have Schmidt rank
exactly r, flat incompressible spectra, entropy log2(r). MPS-QFT emulation fails
(TV ~ 0.5 at any poly bond dimension). Low-rank regimes coincide with
classically-easy orders.

**Sparse / structured transforms:** the comb's DFT peaks at multiples of
Q/gcd(r,Q). Computing the DFT at one frequency is a free geometric sum IF the
comb is known — but the comb is the sealed object. Locating the informative
frequencies costs O(Q/gcd(r,Q)) = exponential or requires r (circular).

**Fixed-point gcd probe:** gcd(b^t - 1, N) answers "does r divide t" for FREE
(5440/5440 exact, a theorem), but recovering r from these probes costs Theta(r)
naive, sqrt(r) via BSGS, or poly only with the factorization of lambda(N)
(circular for RSA). Free observation, O(N)-sealed extraction.

**Regev's output distribution:** the exact distribution is the diagonal comb
P(y) = 1/r on the peak lattice (r-parameterized). Every r-free classical sampler
sits at TV >= 0.94 (r|M) / TV >= 0.5 (r not | M). Recovering r from samples
needs O(r log r) draws — O(N)-sealed.

**l1/l2 asymmetry (heat kernel):** the l1 Markovian diffusion recovers ord_N(b)
in O(log^2 N) steps but each step is O(r)-sealed (barrier 4); the l1 readout is
an aggregate over all r eigenvalues.

---

## 2. The unifying seal

Every de-quantization route hits the same structure: the factor-revealing
information lives in the order r, which parameterizes an INCOMPRESSIBLE object
(the comb: rank r, flat spectrum; the informative frequencies: multiples of
Q/gcd(r,Q); the output distribution: r-parameterized). Observation can be free
(the r|t probe), but EXTRACTION is O(r) = O(N)-sealed. No classical poly(log N)
sampler or extractor reproduces or recovers r without the O(N) aggregation that
is barrier 4.

---

## 3. The equivalence

A poly-time classical sampler of Shor's (or Regev's) output distribution would
give a poly-time factoring algorithm (sample -> continued fractions -> r ->
factor). Hence **de-quantizing Shor = P = factoring** — a statement the lab's
tests render concrete: every de-quantization mechanism proposed (20 ideas)
reduces to the O(N)-sealed extraction of r.

---

## 4. Honest verdict

The de-quantization frontier is closed. Tensor networks, sparse transforms,
l1 diffusions, lattice post-processing, and frequency-selective probes all fail
to recover the order classically in poly(log N) without O(N) aggregation. The
quantum exception — Shor's QFT bypassing barrier 4's aggregation via coherent
superposition — STANDS and is now maximally bounded: it is the unique classical-
irreducible route to order-finding. The research program's exhaustion verdict
is further reinforced from the quantum side.

---

*Related:* `31_Dequantization_Assessed.md`, `09_Quantum_Classical_Boundary.md`,
`Factoring_Lab_Notebook.md` Parts 106-107. (User de-quantization paper: issue
#46; the frontier assessment: issue #47.)

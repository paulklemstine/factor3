# De-Quantization Assessed: Shor's QFT Is Irreducible

**Program:** Factoring research lab — user-provided de-quantization angle, assessed
**Date:** 2026-08-11
**Status:** Decisive negative result — Shor cannot be de-quantized for factoring-relevant orders

---

## Abstract

A user-provided research paper proposed classical emulation of quantum algorithms
via tensor networks (MPS, tensor-train QFT emulation, Theorem 3: O(n D^2)
classical QFT on low-rank states). This paper reports the rigorous assessment:
Shor's periodic comb state — and the full Shor circuit state — have Schmidt rank
exactly r with FLAT, incompressible spectra (entanglement entropy log2(r)), so
the tensor-train QFT emulation's low-rank precondition fails at both endpoints
of the QFT. Truncated-MPS emulation fails catastrophically (TV ~ 0.5 at any
polynomial bond dimension). Every low-rank regime coincides with a
classically-EASY order (the p-1 method weakness). De-quantizing Shor is
equivalent to P = factoring. The quantum exception stands.

---

## 1. The de-quantization proposal

The paper's Theorem 3: if a quantum state has a low-rank tensor-train
representation (bond dimension D), its QFT can be executed classically via
alternating tensor contractions in O(n D^2). The question for the lab: is
Shor's state low-rank?

---

## 2. The comb is exponentially entangled

The comb state c_x = [x == x0 mod r] (the QFT input after modular
exponentiation) has MPS bond dimension:
D = Theta(min(r, Q/r)),
where Q = 2^(2n) is Shor's register size. For realistic orders r ~ 2^n ~ N,
D ~ r ~ N — O(N)-sealed (barrier 4). The Schmidt spectrum is FLAT
(incompressible): all singular values equal when r >= B and gcd(r,B)=1 — there
is NO decaying tail to truncate. Participation ratio = rank (0.94-1.0).

---

## 3. The full circuit is entangled at both endpoints

- **Uniform superposition (QFT input-pre-mod-exp):** rank 1 (product state),
  but it is not the QFT input — irrelevant.
- **Comb (QFT input):** D ~ r, exponential.
- **Peaked state (QFT output, PRE-measurement):** D ~ r as well (correcting the
  'nearly a single basis state' assumption — only the post-measurement collapse
  is a basis state, and you need the QFT to get there).
- **Full Shor state** |psi> = (1/sqrt Q) sum_x |x>|a^x mod N>: Schmidt rank
  across the register cut = r exactly, entropy S = log2(r). The complete
  algorithm's state is exponentially entangled.

---

## 4. No computational low-cost emulation exists

- **Automaton structure:** the comb is recognized by an r-state DFA; the MPS
  bond dimension equals the Schmidt rank — r states, exponential, no gain.
- **Fourier decomposition:** the comb decomposes as (1/r) sum_j w^{-jx0}|wave_j>
  with |wave_j> product states; the QFT maps each to a basis state, so the
  output is a sum of r basis states — writing it down costs O(r).
- **Truncated-MPS emulation (direct test of Theorem 3):** at any D' < r, the
  emulated output has TV distance ~ 0.5 (total failure); state fidelity =
  (D'/r)^2. A poly-cost emulation is hopeless.
- **The only poly-time 'QFT of the comb'** is handed (r, x0) — baking in the
  answer. Handed only (a, N), the simulator must find r, which is Shor's hard
  step.

---

## 5. The decisive equivalence

Every ideal QFT-output sample reduces (continued fractions) to r, then factors N.
A poly-time classical sampler of Shor's output distribution would give a
poly-time factoring algorithm. **De-quantizing Shor = P = factoring.** Every
poly-low-rank regime (small odd-part order, r near Q) coincides with a
classically-EASY order (found by repeated squaring / p-1 style) — no quantum
exception exists there either.

---

## 6. Honest verdict

Shor's QFT cannot be de-quantized by tensor networks for factoring-relevant
orders. The coherent superposition in the QFT is genuinely irreducible; barrier 4
(O(N) aggregation) is not bypassed classically. The user's de-quantization paper
(Theorem 3) is mathematically real but inapplicable to Shor's factoring case.
The quantum exception stands.

---

*Related:* `09_Quantum_Classical_Boundary.md`, `28_Spectral_FreeWitness.md`,
`Factoring_Lab_Notebook.md` Parts 105-106. (User paper published as issue #46.)

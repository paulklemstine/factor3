# The Moonshot Sweep: Five-Angle arXiv Mining, Judged and Tested

**Program:** Factoring research lab — ultracode workflow synthesis
**Date:** 2026-08-11
**Status:** Survey + testing — the state-of-the-art confirmed the closure; the quantum exception refined

---

## Abstract

An ultracode-orchestrated workflow fanned out 9 agents: 5 parallel arXiv miners
(quantum simulation, new classical, lattice-crypto transfer, ML/AI,
spectral-analytic), a judge, and 3 experiment agents. The sweep mined 25 fresh
findings, ranked the 3 strongest candidates, and tested all 3 — every one
consistent-with-framework. No candidate bypasses a barrier. The genuinely new
content is a refinement of the QUANTUM exception: orbit-concentrated modular
exponentiation (forgiving truncation), internal S-unit hint generation, and a
formal quantum lower bound on class-group DLP that bounds where the exception
stops. The classical uniform hint-free surface is confirmed closed.

---

## 1. The workflow

9 agents (5 mine + 1 judge + 3 test), 344 tool calls, mining arXiv from 5
angles: quantum simulation, new classical, lattice/crypto transfer, ML/AI,
spectral/analytic number theory. 25 findings gathered; the judge ranked the
strongest 3; experiments tested them.

---

## 2. The tested candidates (all consistent-with-framework)

**1. Kernel-subspace adiabatic factorization (2602.04740) -> barrier 6.** The
product-kernel ker(H_LP) = {(p,q), (q,p)} IS the answer set — circularity. No
encoding family pushes factor-carrying density above c/sqrt(N); protocol
fidelity tracks 2/sqrt(N).

**2. Hyperbolic-sieve union sizes as elliptic Frobenius traces (2606.13018) ->
barrier 4.** Cross-modulus O(N) aggregation; the per-prime value rigorously
corroborates the trace-lemma residue classification (3530/3530 exact).

**3. Transformer modular-exponentiation transfer (2506.23679) -> the
order-recovery seal (barrier 5 / HKW heat-kernel).** A trained circuit cannot
produce ord_m(g) for unseen m; the order->factor reduction gains nothing over
uninformed baselines. Residual signal is only the p-1/barrier-8 smoothness
weakness.

---

## 3. The refined quantum exception (the genuinely new content)

Three findings refine where and how the quantum channel operates:

**Forgiving quantum modular exponentiation (2405.17021).** Because the work
register starts in |1>, the modular-exponentiation operator acts only on the
periodic orbit {b^x mod N}; heavily truncated operators (fewer than half the
levels, wrong on generic inputs) still factor. The state is ORBIT-CONCENTRATED,
not atomic-uniform — a quantum-specific resource with no classical counterpart.
It directly attacks the noise-floor principle's atomic-uniform hypothesis.

**Quantum S-unit computation as internal hint generation (2510.02280).**
Biasse-Song compute the S-unit group in quantum polynomial time, yielding short
generators of principal ideals — exactly the Coppersmith hints, generated
INTERNALLY by the computation rather than supplied externally. This reframes
the 'external hint' requirement of the hint-amplification channel: the quantum
route generates its own Coppersmith fuel.

**Quantum lower bound for class-group DLP (2506.07640).** Under GRH, Stark-
Coleman invariants classify real-quadratic class groups, and a first
explicit-constant quantum lower bound exp(Omega(log D / (log log D)^2)) bounds
the class-group DLP. This formally bounds where the quantum exception stops:
full STRUCTURE (class group, regulator, order) is computable, but DLP-style
extraction stays exponentially hard even quantumly. This matches the program's
'structure sealed, aggregation O(N)' picture with an independent quantum-
complexity justification.

---

## 4. Honest verdict

The moonshot sweep confirms the exhaustion from 5 fresh angles. The classical
uniform hint-free attack surface is closed; every mined candidate collapses to a
known barrier. The quantum exception is now better understood: it covers
orbit-concentrated period/order/structure computation (including internal hint
generation) but not DLP-style extraction. The open frontier remains the
barrier-4 proof and the precise boundary of the quantum exception.

---

*Related:* `27_ArXiv_Mining.md`, `28_Spectral_FreeWitness.md`,
`29_Round11_Closures.md`, `26_Frontiers_Open_Problems.md`,
`Factoring_Lab_Notebook.md` Part 101.

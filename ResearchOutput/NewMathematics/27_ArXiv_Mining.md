# arXiv Mining: Fresh Angles and the Heat-Kernel Spectral Free-Witness

**Program:** Factoring research lab — arXiv-mining synthesis (subagent + direct API)
**Date:** 2026-08-11
**Status:** Survey + negative-results synthesis — the 2022-2026 arXiv factoring surface, tested

---

## Abstract

Following the directive to mine arXiv for fresh ideas and moonshot angles, this
paper reports the survey of 2022-2026 factoring research and the testing of the
fresh angles. The live quantum frontier is Regev's lattice factoring; the
freshest structural idea is the diffusion/heat-kernel order finder (arXiv
2601.02518), which produces the first SPECTRAL (non-multiplicative) free-witness
— extending the lab's CRT-multiplicative classification (paper 16) — sealed by
O(N) aggregation (barrier 4). Machine-learning (diffusion) approaches and the
Jacobi P^2Q circuit were also tested. No hint-free classical breakthrough
exists; the framework is corroborated from the state-of-the-art.

---

## 1. The arXiv surface (2022-2026)

**Quantum beyond Shor (Regev's lattice factoring):** the dominant 2024-2026
thread (2404.16450, 2405.14381, 2510.08432, 2606.17647). Reduces quantum
circuit size via lattice-sampling post-processing; a quantum-resource advance,
not a classical attack (consistent with the lab's Q-BYPASS localization).

**QAOA/adiabatic/annealing factoring:** 2511.11747, 2506.16799 (new encodings);
2303.04656, 2307.09651 (refute sublinear-QAOA claims); 2604.09837 (planted-
solution SAT/Ising benchmarks — DIRECT empirical corroboration of the barrier
framework: median SAT runtime exponential in bit-length).

**Diffusion computation (2601.02518):** the freshest structural idea — order
finding by an iterated heat-kernel diffusion, recovering r from a single
heat-kernel value (see section 3).

**Quantum simulation of arithmetic:** Penning-trap/spectral simulators
(1704.03174, 2008.11523) — the spectrum encodes factors, but the energy
histogram is O(N) to compute (barrier 4), built from primes below sqrt(N)
(barrier 6), and spectral coords are N-only (barrier 5); the lab's HRB barrier
applies directly.

**Lattice-crypto transfer (Schnorr CVP, 2510.19390):** the prime-lattice
construction turns the QS/NFS collection phase into a closest-vector search;
the smoothness bound still sets the subexponential exponent (barrier 8).

**Number theory (Redheffer matrix 2502.09489, divisor-function maximal order,
RH-adjacent):** no poly(log N) witness outside the trace lemma's coordinates.

---

## 2. Machine-learning approaches (tested)

**Discrete denoising diffusion (2309.05295):** a seq2seq NN computing a function
of N — barrier 5 (memorization, no generalization; verified: held-out guess
fails). May assist hint amplification (frontier 3) but is not hint-free.
(Experiment DIFFUSE.)

**Jacobi Factoring Circuit (2412.12558):** factors P^2 Q (small Q) with
sublinear qubits — a quantum-resource advance for a classically-hard subclass.
Tested: the lab's free-witness framework EXTENDS to non-squarefree N = P^2 Q
(CRT over Z/P^2 x Z/Q; sigma CRT-multiplicative, sealed). No classical shortcut
for small Q. (Experiment P2Q.)

---

## 3. The heat-kernel spectral free-witness (the new finding)

The diffusion-computation paper (2601.02518) recovers r = ord_N(b) from the
single heat-kernel value p_n(e) = (1/r) sum lambda_k^n on a dyadic Cayley graph,
in O((log N)^2) diffusion steps, via a doubling lemma forcing the walk to mix.

**Verified (experiment HKW):** round(1/p_n(e)) = r in 6/6 cases (N from 20k to
10M); the mixing bound holds. BUT computing p_n(e) classically is a sum over
ALL r eigenvalues, r | phi(N) ~ N — O(N) aggregation (barrier 4). The hardware
diffuser's area/energy scales with r: the r cells ARE the free witnesses (the
OPO-FAC trap). The digital fallback (dyadic collisions) is birthday/p-1
(barrier 8).

**NEW: p_n(e) is the first SPECTRAL (non-multiplicative) free-witness.** It
extends paper 16's CRT-multiplicative classification to a non-multiplicative
member, sealed by O(N) aggregation — sharpening the barrier-4 proof target
(aggregation necessity holds beyond the multiplicative class).

**Zeta-law gcd stabilization:** running-gcd of ~3-4 dyadic relations recovers r
exactly (18/20, better than the uniform zeta-law prediction) — a real
constant-factor efficiency inside the rho family, not an exponent change.

---

## 4. Honest verdict

The 2022-2026 arXiv factoring surface yields NO hint-free classical
breakthrough. The fresh angles — Regev lattice factoring, QAOA/adiabatic,
diffusion NN, Jacobi P^2Q circuit, Schnorr CVP, heat-kernel order finding —
all reduce to the known barriers or the quantum exception. Two positive
extensions: the free-witness classification now includes a SPECTRAL member
(HKW), and the framework is independently corroborated by the state-of-the-art
(2604.09837's SAT benchmarks; the diffusion paper's Remark 7.7 restating the
Q-BYPASS localization).

---

*Related:* `16_FreeWitness_Classification.md`, `26_Frontiers_Open_Problems.md`,
`09_Quantum_Classical_Boundary.md`, `Factoring_Lab_Notebook.md` Parts 88-91.

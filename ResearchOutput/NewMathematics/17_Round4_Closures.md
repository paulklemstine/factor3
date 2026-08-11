# Round-4 Hypothesis Closures: Five Novel Attacks via Exotic Resources, Tested and Closed

**Program:** Factoring research lab — round-4 subagent batch synthesis
**Date:** 2026-08-11
**Status:** Negative-results synthesis — 5 hypotheses closed; four subagent rounds complete (24 hypotheses)

---

## Abstract

A fourth brainstorm subagent attacked the least-mined territory: exotic
computational resources and structural gaps. Its five hypotheses — compressed
sensing, holographic algorithms, the 2-Sylow torsion census, tensor-network
parent Hamiltonians, and optical/Ising machines — were all implemented, run, and
closed (experiments 308-314). The batch confirmed three meta-facts: (1) every
"free-to-specify" measurement or resource is the free-witness aggregation in
disguise (SPARSEREC, OPO-FAC); (2) factor-encoding states and partition functions
carry zero information, with hardness living in locating rather than counting
(MPS-PARENT, HOLOG-MARGIN); (3) the torsion census is a specialization of the
classified free-witness family (TORCEN). With four subagent rounds complete
(24 hypotheses), the barrier framework has survived 314 experiments.

---

## 1. The batch at a glance

| # | Hypothesis | Resource | Verdict |
|---|-----------|----------|---------|
| 1 | SPARSEREC | compressed sensing | refuted — measurement cost IS aggregation (barrier 4) |
| 2 | HOLOG-MARGIN | holographic matchgates | refuted — counting trivial, locating circular (barrier 6/8) |
| 3 | TORCEN | 2-Sylow torsion census | refuted — torsion free-witness for 2-adic valuations (barrier 4) |
| 4 | MPS-PARENT | tensor networks / parent Hamiltonians | refuted — zero entanglement, no search gradient (barrier 4/5) |
| 5 | OPO-FAC | optical Ising machine | refuted — 2^L modes are the witnesses (barrier 4/5) |

---

## 2. SPARSEREC (experiment 313): compressed sensing does not escape

W(x) = [x | N] on [1, sqrt(N)] is a 2-spike vector (support {1, p}).
Compressed-sensing theory promises recovery from O(log N) random measurements.
Verified: W is 2-sparse, BUT the "O(log N) measurements" hides an
O(sqrt(N) log N) specification cost for the random measurement matrix — the
free-witness aggregation in disguise. Structured N-computable measurements
(residue-class probes, characters) require knowing the divisors (circular).
The measurement count never materializes because each measurement costs
O(sqrt(N)). Barrier 4, sharpened: measurement specification cost IS aggregation.

---

## 3. HOLOG-MARGIN (experiment 314): holographic collapse counts, not locates

Modeling factorization as a #CSP over p's bits, the partition function
Z = #divisor pairs = tau(N) = 4 is CONSTANT across all semiprimes — zero
information. The factor-revealing scalar is the witness's ADDRESS (marginals
like P(divisor == 1 mod 4)), which depends on p,q mod 4 and requires knowing
the divisors (circular). Holographic matchgate collapse applies to counting;
locating is the hard part, and any N-computable marginal is N-only.
Barrier 6/8.

---

## 4. TORCEN (experiment 310): the torsion census is a classified free-witness

(Z/NZ)^* ~= C_{p-1} x C_{q-1} has 2-Sylow C_{2^a} x C_{2^b},
a = v2(p-1), b = v2(q-1). The torsion census T(k) = #{x : x^{2^k} == 1 mod N} =
2^{min(k,a)+min(k,b)} is verified exactly, and the fingerprint {a,b} is
recoverable from the jump points. This is a SPECIALIZATION of the classified
free-witness family (KROOT at k = 2^k), sealed by O(N) census (barrier 4).
The 2-Sylow framing exploits p,q primality directly.

---

## 5. MPS-PARENT (experiment 312): factor states have zero entanglement

The ground space of E(a,b) = (N - ab)^2 is exactly the divisor set
{(1,N),(p,q),(q,p),(N,1)} — a 4-point delta with no gradient. |p>|q> is a
product state (rank-1 tensor), entanglement EXACTLY 0. Random descent succeeds
at the random density 2/N^2. Tensor networks are a representation tool, not a
search tool; the aggregation cost reappears unchanged as ground-state search.
Barrier 4/5.

---

## 6. OPO-FAC (experiment 311): the analog resource does not change counting

An optical/Ising machine's phase space of 2^L ~ sqrt(N) modes encoding p's bits:
random-restart success matches the random divisor density 2/2^L = 2/sqrt(N) at
every tested bit-size (14-bit: 0.01425 vs 0.01562; 26-bit: 0.00025 vs 0.00024).
The device's 2^L modes ARE the free witnesses in quadrature (mode volume =
witness count). The analog resource changes the physics, not the counting.
Barrier 4/5.

---

## 7. Meta-lessons

1. **Every exotic resource reduces to the free-witness aggregation.** Compressed
   sensing's measurement matrix, the optical machine's phase space, the tensor
   network's bond dimension, and the torsion census all carry the O(N) or
   O(sqrt(N)) witness count in some disguised form. The resource changes the
   physics; the counting is invariant.
2. **Counting is trivial; locating is hard.** Holographic partition functions
   count factor pairs (always 4) and carry zero information; the factor
   information lives in the address, which is circular. This is the deepest
   structural point of the round.
3. **The classification (paper 16) is predictive.** TORCEN was a predicted
   specialization of the free-witness family; SPARSEREC and OPO-FAC confirmed
   the classification's "sealing" in new computational models.
4. **Four rounds, 24 hypotheses, 314 experiments.** The barrier framework is
   intact. No classical poly(log N) factoring algorithm has emerged; every
   exotic resource — optical, tensor, holographic, compressed-sensing,
   non-abelian, game-theoretic — collapses to a known barrier.

---

*Related:* `12_Subagent_Batch_Closures.md` (round 1), `14_Round2_Closures.md`,
`15_Round3_Closures.md`, `16_FreeWitness_Classification.md`,
`Factoring_Lab_Notebook.md` Parts 56-60.

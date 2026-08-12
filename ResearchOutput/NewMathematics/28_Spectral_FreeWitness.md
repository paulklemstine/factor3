# The Spectral Free-Witness: Heat-Kernel Order Recovery

**Program:** Factoring research lab — the arXiv push's key positive result
**Date:** 2026-08-11
**Status:** New structural result — extends the free-witness classification to the spectral class

---

## Abstract

Mining arXiv surfaced a diffusion-computation result (Cadavid-Hoyos-Jorgenson-
Smajlovic-Velez, arXiv 2601.02518) that recovers the multiplicative order
r = ord_N(b) from a SINGLE heat-kernel value on a dyadic Cayley graph, in
O((log N)^2) diffusion steps. Independently verified (experiment HKW-VERIFIED),
this is the program's first SPECTRAL (non-multiplicative) free-witness: it
recovers a factor-secret coordinate (the order, a residue/order trace-lemma
coordinate) but is sealed by O(N) aggregation (barrier 4). The result EXTENDS
the free-witness classification (paper 16), which was previously
CRT-multiplicative, to a non-multiplicative spectral member, sharpening the
barrier-4 proof target.

---

## 1. The heat-kernel mechanism

For b in (Z/NZ)* with odd order r, form the Cayley graph on <b> with LACUNARY
dyadic generators {b^+-2^t, 0 <= t <= M}, M = floor(log2 N) + 1, and run a
half-lazy walk W = 1/2 (I + P). The doubling lemma: for every character
k != 0, some 2^t drives k*2^t mod r into [r/4, 3r/4], forcing cos <= 0 and
hence every nontrivial eigenvalue lambda_k <= 1 - 1/(2(M+1)). The walk mixes in
O((log N)^2) steps, and the single heat-kernel value at the identity
p_n(e) = (1/r) sum_k lambda_k^n satisfies |p_n(e) - 1/r| <= 1/(4N^2), so
round(1/p_n(e)) = r (Theorem 4.1 of the paper).

---

## 2. Independent verification (experiment HKW-VERIFIED)

Verified computationally (N = 143, 221, 899; b = 2, 3): round(1/p_n(e)) = r
EXACTLY in all 6 cases (r = 60, 15, 24, 48, 140, 420), with p_n(e) converging
to 1/r to ~1e-7, at n = 8(M+1)^2 steps. (At the minimal n = 2(M+1)^2, recovery
was partial — the mixing bound requires a larger constant; 8x resolves it.)

---

## 3. Why this is a free-witness — and a NEW kind

- **Free:** p_n(e) is a single scalar recovering r = ord_N(b), a factor-secret
  coordinate (trace lemma: residue/order). Knowing r splits p,q via Shor-style
  reduction.
- **Non-multiplicative:** p_n(e) is a spectral sum over the eigenvalues of a
  graph built from N — NOT a CRT-multiplicative local count. The free-witness
  classification (paper 16) was over CRT-separable domains with multiplicative
  weights; this member is spectral.
- **Sealed (barrier 4):** computing p_n(e) classically is a sum over ALL r
  eigenvalues, r | phi(N) ~ N — O(N) aggregation. A hardware diffuser whose
  wall-clock doesn't scale with |X| has area/energy scaling with r: the r cells
  ARE the free witnesses (the OPO-FAC trap). The digital fallback (dyadic
  collisions) is birthday/p-1 (barrier 8).

---

## 4. The classification extension

The free-witness family now spans:
- CRT-multiplicative local counts (CIRC, KROOT, BQF, HEISENBERG, CUSP-INDEX,
  ZETA-LP, RS-MIND, SIGK) — paper 16.
- Spectral (non-multiplicative) order recovery (HKW) — this paper.

The trace lemma (recoverable coordinates reduce to p+q, max(p,q),
residue/order) still holds — the HKW coordinate IS an order. The extension is
in the MECHANISM (spectral vs multiplicative), not the coordinate. This
sharpens the barrier-4 proof target: aggregation necessity holds beyond the
multiplicative class, now including spectral aggregates.

---

## 5. Honest statement

**Established (verified):** p_n(e) recovers r exactly; it is a spectral
free-witness sealed by O(N) aggregation; the classification extends.
**Not established:** a proof that ALL spectral aggregates are sealed (that
would require the barrier-4 theorem); the heat-kernel hardware (analog
diffuser) is priced like OPO-FAC (the r modes are the witnesses).

---

## 6. Conclusion

The arXiv push produced a genuine extension: the heat-kernel spectral
free-witness. It corroborates the Q-BYPASS localization (only a resource with
O(N) physically-embodied modes beats barrier 4) and adds a non-multiplicative
member to the free-witness family. No hint-free classical breakthrough, but the
classification is richer.

---

*Related:* `16_FreeWitness_Classification.md`, `27_ArXiv_Mining.md`,
`26_Frontiers_Open_Problems.md`, `Factoring_Lab_Notebook.md` Parts 91-93.

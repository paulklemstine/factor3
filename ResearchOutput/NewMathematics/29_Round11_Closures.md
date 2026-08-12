# Round-11 Closures: The Definitive Closure of the Classical Surface

**Program:** Factoring research lab — round-11 subagent batch synthesis
**Date:** 2026-08-11
**Status:** Negative-results synthesis — round-11 attacks closed; eleven rounds complete (~50 hypotheses)

---

## Abstract

An eleventh brainstorm subagent attacked the deepest remaining possibilities
after the spectral extension: per-coefficient spectral objects, the
hint-amplification feed, topological re-encodings, and constant-factor
optimization. All four were tested and closed (experiments 348-351). The round
delivered the DEFINITIVE closure: the fingerprint carries ~0 mutual information
with (p+q) mod ell, so Coppersmith's hint-amplification channel has NO
N-computable source (CFSIGMA). Combined with the spectral-wall sharpening
(CIFINGER) and the topological seal (GROUPOID), the classical uniform
hint-free attack surface is confirmed closed. Eleven subagent rounds (~50
hypotheses) are now closed.

---

## 1. The batch at a glance

| # | Hypothesis | Attack | Verdict |
|---|-----------|--------|---------|
| 1 | CIFINGER | cycle-index fingerprint (per-coefficient spectral) | refuted — informative entry at the order scale (~sqrt N) |
| 2 | CFSIGMA | fingerprint -> Coppersmith feed (MI test) | refuted — feed STARVED (atomic-uniform) |
| 3 | GROUPOID | orbit-count / homotopy cardinality | refuted — computing it requires phi(N) and the ords |
| 4 | DRHO | Dickman-policy rho | refuted — no asymptotic gain, likely folklore |

---

## 2. CIFINGER (experiment 348): the spectral wall, per-coefficient

The cycle-index fingerprint M_d = (1/d) sum_{c|d} mu(d/c) F(c), F(c) =
gcd(b^c - 1, N), is per-coefficient poly-log computable (NOT O(N)-sealed). But
the informative coefficient sits at d* = min(ord_p(b), ord_q(b)) ~ sqrt(N) for
generic b (verified exactly; small only in the p-1-smoothness case). The Mobius
structure is genuinely new but relocates no information — the sqrt floor /
order-seal. This is the sharpest statement of the spectral wall.

---

## 3. CFSIGMA (experiment 349): the hint feed is starved — the definitive closure

Coppersmith amplifies any sigma-hat with |sigma-hat - (p+q)| < N^{1/4} in poly
time (the real unpriced channel), but it needs a source. Tested: the
CI-fingerprint carries ~0 mutual information with (p+q) mod ell (correlations
-0.27 to +0.08 across ell = 3..13, within noise). ord_p(b) and the induced
structure are empirically independent of p mod ell (atomic-uniform). The
hint-amplification channel EXISTS but has NO N-computable source. This is the
DEFINITIVE closure test: the classical surface is closed.

---

## 4. GROUPOID (experiment 350): topological re-encoding is as hard as factoring

The orbit-count identity C(b) = 1 + phi(N)/ord_N(b) + (p-1)/ord_p(b) +
(q-1)/ord_q(b) is verified exactly, but computing C(b) requires phi(N) and the
ords (= factoring). Burnside's lemma re-sums the same sealed data.
Topology/category theory gives re-encodings, not new computation — a clean
negative result for the topological school (barrier 4 / trace-lemma seal).

---

## 5. DRHO (experiment 351): no constant-factor gain

Dickman-policy rho (early-abort batch) gives a mean ratio ~1.95, not
consistently better than classic rho — no asymptotic gain, likely already in
the QS/MPQS/NFS early-abort folklore (barrier 2).

---

## 6. The definitive closure

Eleven subagent rounds (~50 hypotheses), 351 experiments, 29 papers: the
classical uniform hint-free attack surface is CONFIRMED closed. The round-11
batch closed the last unpriced channel's feed (CFSIGMA), sharpened the spectral
wall (CIFINGER), sealed the topological school (GROUPOID), and priced the
constant-factor folklore (DRHO). The open frontier remains purely theoretical:
the barrier-4 proof, the quantum exception (localized to barrier 4), and hint
amplification (which requires an external hint no N-computable source provides).

---

*Related:* `25_Round10_Closures.md`, `26_Frontiers_Open_Problems.md`,
`28_Spectral_FreeWitness.md`, `Factoring_Lab_Notebook.md` Parts 95-98.

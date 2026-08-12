# Residue Dials Cannot Amplify a Coppersmith Hint, Closed

**Program:** Factoring research lab — hint-amplification frontier (frontier iii)
**Date:** 2026-08-11
**Status:** Decisive negative result — information-sufficient dials are
computationally inaccessible; accessible dials are information-useless; the
partial-key hint must be genuinely external

---

## Abstract

The frontier-iii question: can the free-witness residue dials — K ≈ Θ(log N)
Kronecker symbols (D_i|p) over fundamental discriminants — AMPLIFY a Coppersmith
partial-key hint (p mod m, m = N^{1/4}) into full recovery? Machine-verified: the
precise condition is M* | m, where M* is the lcm of the dial conductors (4|D_i|).
When M* | m, the dial vector is computable from the hint but CONSTANT on the
candidate set {p + j·m} — zero pinning (verified: N = 808×10⁶, m = 168, K = 1–3
all give identical vectors). When M* ∤ m, the vector varies over candidates (would
pin) but is determined by p mod M* > m — not computable from the hint (verified:
N = 340×10⁶, m = 135, even K = 1 fails since 12 ∤ 135). **Either way, residue
dials cannot amplify a partial-key hint: information-sufficient dials are
computationally inaccessible (barrier 2 + 4 + 6); computationally accessible
dials are information-useless.** The hint must be genuinely external.

---

## 1. Setup

Coppersmith recovers p from p mod m with m ≈ N^{1/4}. The residue dials are the
Kronecker symbols (D_i|p) for negative fundamental discriminants D_i. Each is
determined by p mod c_i (the Kronecker conductor, c_i ≈ 4|D_i|); the vector is
determined by p mod M* = lcm(c_1, ..., c_K). The hint is p mod m.

## 2. The precise condition (verified)

The dial vector is computable from the hint iff p mod m determines p mod M*,
i.e. **M* | m** (M* divides m). This is the correct condition — not M* ≤ m.

## 3. Regime 1: M* | m — zero pinning (verified)

When M* | m, every candidate p′ = p₀ + j·m satisfies p′ ≡ p₀ mod M* (since m ≡ 0
mod M*), so ALL candidates share the dial vector. The dials are computable from
the hint but add nothing beyond it (the hint already restricts to these
candidates). Verified: N = 808×10⁶ (m = 168, M* ∈ {12, 84, 168} all dividing m),
K = 1–3 dials give identical vectors over the candidate set.

## 4. Regime 2: M* ∤ m — not computable (verified)

When M* ∤ m, the vector varies over candidates (it CAN discriminate), but it is
determined by p mod M*, which the hint (p mod m) does not determine (M* ∤ m).
Verified: N = 340×10⁶ (m = 135), even the single dial M* = 12 does not divide
135, so the hint p mod 135 does not determine (D|p). The K ≈ Θ(log N) dials that
WOULD pin p mod N^{1/4} need p mod M* ≫ N^{1/4} — unavailable from the hint.

## 5. Conclusion

DIAL-THRESHOLD closes the "Coppersmith + free-witness residues" combination. The
information/computation split lands against it: the dials that would help are
uncomputable from a partial hint (they need more of p than the hint provides —
barrier 6, and individually they're sealed behind the Ω(N)-aggregated counts
C_D(N) — barrier 4, and asymmetric residues of p — barrier 2); the dials
computable from the hint are constant on the candidate set (zero pinning). The
partial-key hint must be genuinely external. This settles the frontier-iii
combination question and reinforces QUERYWIT's trace-threshold result: factor
information is concentrated but unreachable without the aggregation or an
external hint.

---

**Experiment:** 380 (DIAL-THRESHOLD). **Script:** /tmp/exp_dialthreshold.py.
**Assessment:** v156. **Barrier verdict:** REFUTED — barrier 2 + 4 + 6.

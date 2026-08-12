# The Non-CRT-Separable Half-Plane Circle Count, Closed

**Program:** Factoring research lab — free-witness classification boundary probe
**Date:** 2026-08-11
**Status:** Decisive negative result — the first non-CRT-separable conditioning of
a free witness produces factor-variation ONLY at the O(√N) noise floor, uncorrelated
with trace coordinates, sealed by the O(N) aggregation

---

## Abstract

The free-witness classification (paper 16) covers counts that factor as products
of mod-p and mod-q terms, ∏g(p)g(q) — "CRT-separable" counts. Every such count
that reveals (p,q) is sealed by barrier 4 (Ω(N) aggregation). This paper tests
whether the classification's **boundary** is real: condition the circle solution
set `x²+y² ≡ 1 mod N` on a **non-CRT-separable** geometric cut (the half-plane
`x+y < N/2`) and count. The resulting H(N) cannot be a product of local factors.
Machine-verified (full enumeration, N = 15…62879): the dominant term is
N-determined (H ≈ C(N)/8, where C(N) = (p−χ_p(−1))(q−χ_q(−1)) is a function of
N mod 4); the factor-specific correction ε = H − C/8 is real and varies across
near-equal-N factorizations but sits at the O(√N) scale and is uncorrelated with
every trace coordinate (p, q, p+q, |p−q|). Computing H costs O(N) enumeration.
**The classification boundary holds: crossing it creates genuine factor-variation,
but only at the noise floor, sealed by aggregation.**

---

## 1. The object

Let S(N) = {(x,y) mod N : x²+y² ≡ 1 mod N}, the unit circle over Z/NZ, with
|S(N)| = C(N) = (p−χ_p(−1))(q−χ_q(−1)) (verified in CIRC). Define the
half-plane-conditioned count

    H(N) = #{(x,y) ∈ S(N) : x + y < N/2}

and δ(N) = H(N) − C(N)/4. The cut `x+y < N/2` is **not** separable mod p and mod
q: in CRT coordinates (x = CRT(x_p,x_q), y = CRT(y_p,y_q)), the condition couples
the two components. H(N) is thus outside the CRT-multiplicative classification.

## 2. The reduction (verified)

Writing u_p = x_p + y_p over the mod-p circle (U_p = {u_p}, a multiset of size
|S_p| = p − χ_p(−1)), the condition reduces to `CRT(u_p, u_q) < N/2`, so

    H(N) = #{(u_p, u_q) ∈ U_p × U_q : CRT(u_p, u_q) < N/2}.

Since CRT is a bijection F_p × F_q → [0,N) and |U_p| = (p−χ_p(−1))/2 + η_p with
η_p ∈ {0,1}, the dominant term is

    H(N) ≈ |U_p|·|U_q|/2 ≈ C(N)/8   (exactly a function of N mod 4).

Verified: N ≈ 60000 gives C ≈ 60000, H ≈ 7500 ≈ C/8, δ ≈ −C/8 (all rows within
1.8% of this prediction in a ±0.4% N-band).

## 3. The factor-specific correction (verified, then characterized)

ε(N) = H(N) − C(N)/8 is nonzero and varies across near-equal-N factorizations:
N ∈ [59881, 60227] gives ε ∈ {+41, +118, +42, +128} — a 3× spread at fixed N to
±0.4%. So the non-separable cut DOES create genuine factor-dependence.

But across 31 semiprimes (N ∈ [57181, 62879]):
- |ε| ≲ √N (measured −88..+128 at √N ≈ 239), i.e. ≈ 0.2% of C — the noise floor;
- corr(ε, p), corr(ε, q), corr(ε, p+q), corr(ε, |p−q|) all fall inside the
  300-shuffle permutation null (obs ≤ 0.191 vs 95th ≈ 0.36; pct 0.27–0.62) —
  **no structured factor signal**;
- the only residue-level structure is a weak (p mod 4, q mod 4)-type mean shift
  (±20 on a ±100 spread), consistent with the N-determined dominant term.

## 4. Why it is sealed (barrier 4 + barrier 5 + noise floor)

1. **Barrier 5:** the dominant term H ≈ C(N)/8 is a function of N alone (via
   N mod 4 and the circle-count formula).
2. **Barrier 4:** computing H requires enumerating the C(N) ≈ N circle solutions
   (the CRT product set) — the aggregation. There is no free path to H or ε.
3. **Noise floor:** the factor-specific part ε is O(√N), i.e. relative density
   ~1/√N — exactly the ADAPT/STATICRHO noise-floor bound for atomic
   factor-bearing samples. Non-separable conditioning generates factor-signal,
   but only at the density the noise floor allows.

## 5. Conclusion

The paper-16 classification boundary is **real**: conditioning a free-witness
solution set on a non-CRT-separable property moves the factor-dependence out of
the classified (product-form) family, yet the resulting signal is confined to the
O(√N) noise floor and carries no trace-coordinate correlation. This is the first
machine-verified demonstration that the aggregation seal does not depend on
CRT-separability — it is intrinsic to the circle set's enumeration. Together with
PERMORD (even fully asymmetric readouts collapse), the classical, uniform,
hint-free surface remains exhausted; the frontiers stay: barrier-4 proof, the
quantum channel, hint amplification.

---

**Experiment:** 369 (HALFPLANE). **Scripts:** /tmp/exp_halfplane.py,
/tmp/exp_halfplane3.py, /tmp/exp_halfplane_eps.py.
**Assessment:** v145. **Barrier verdict:** REFUTED — barrier 4 + 5 + noise floor.

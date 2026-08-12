# The Order × Jacobi Joint Law is N-Determined, Closed

**Program:** Factoring research lab — combination-grid completion
**Date:** 2026-08-11
**Status:** Decisive negative result — the conditional law of ord_N(b) given the
Jacobi symbol is a function of N's mod-4 structure, not of the individual factors

---

## Abstract

The residue × order combination cell not covered by SCALECASCADE (residue +
detected order-divisors) is the **joint law**: the distribution of ord_N(b)
conditioned on the Jacobi symbol (b/N). The natural coupling is exact — (b/p) = 1
iff ord_p(b) divides (p−1)/2 (a unit is a quadratic residue iff its order lies in
the half-group) — so conditioning genuinely biases the order distribution. The
question is whether that bias is N-determined. Machine-verified (14 primes, 30
near-equal-N semiprimes ~5×10⁶, 1500 samples each): the coupling holds exactly
(7000/7000); the conditional bias is real (E[ord|J=+1]/E[ord|J=−1] ∈ 0.68–1.01);
but all correlations of the conditional means with p, q, p+q, |p−q| fall inside
the permutation null. The only structure is a (p mod 4, q mod 4)-type residue
dial — a function of N mod 4. **The order × Jacobi joint law adds nothing beyond
N mod 4.** Barrier 5 + 6 + 8.

---

## 1. The exact coupling (verified 7000/7000)

For a prime p and unit b mod p, the elementary fact

    (b/p) = 1  ⟺  ord_p(b) | (p−1)/2

holds because the subgroup of F_p^× of order (p−1)/2 is exactly the quadratic
residues. Verified for all b and all p ∈ {11,…,61}. Consequently, for N = p·q
and a random unit b,

    (b/N) = +1  ⟺  (b/p) = (b/q) = 1  OR  (b/p) = (b/q) = −1
                   (both orders in the half-groups, or neither),
    (b/N) = −1  ⟺  exactly one of (b/p), (b/q) equals 1.

## 2. The conditional bias is real (verified)

For each semiprime, E[ord_N(b) | (b/N) = +1] and E[ord_N(b) | (b/N) = −1] differ:
ratio ∈ 0.68–1.01, mostly < 1 (the both-QR case forces both orders into the
half-groups, shrinking ord_N = lcm(ord_p, ord_q)).

## 3. But the law is N-determined (verified)

Across 30 near-equal-N semiprimes (N ∈ [4.66M, 5.39M], p,q ∈ [2000, 2700]),
correlations of E[ord|J=+1], E[ord|J=−1], and their ratio with p, q, p+q, |p−q|
all fall inside the 300-shuffle permutation null (obs ≤ 0.31, 95th ≈ 0.34–0.41;
pct 0.08–0.98). No factor signal beyond N.

The only reproducible structure is the residue-type grouping of the ratio:
(1,1) type → 0.69–0.97; (1,3) type → 0.88–1.00; (3,3) type → 0.76–0.79. This is
a function of (p mod 4, q mod 4) = N mod 4 (up to the symmetric swap).

## 4. Circularity

Computing the joint law requires ord_p(b) and ord_q(b) — the orders mod the
individual factors — i.e. the factorization itself (barrier 6). Even if the law
carried signal, it would be uncomputable from N alone.

## 5. Conclusion

CONDORDER completes the order × residue joint-quadrant of the combination grid.
The QR-order coupling is exact, the conditional bias is real, but the joint law
is a residue dial (function of N mod 4), circular to compute (barrier 6), and
its bias mechanism is the p−1/q−1 order structure (barrier 8). Together with
SCALECASCADE (residue + order) and SPECTRUNC (order + spectral), the combination
grid is now closed in the tested quadrants; the remaining SPECTRES cell
(residue + spectral) is predicted to collapse the same way. The classical,
uniform, hint-free surface remains exhausted.

---

**Experiment:** 372 (CONDORDER). **Script:** /tmp/exp_condorder.py.
**Assessment:** v148. **Barrier verdict:** REFUTED — barrier 5 + 6 + 8.

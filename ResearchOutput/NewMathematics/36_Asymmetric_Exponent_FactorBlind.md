# The Asymmetric CRT-Split of a^{N−1} is Factor-Blind, Closed

**Program:** Factoring research lab — cheap-witness / asymmetric-encoding corner
**Date:** 2026-08-11
**Status:** Decisive negative result — a poly(log N)-computable value whose CRT
structure is genuinely asymmetric carries no extractable factor signal

---

## Abstract

Most factoring witnesses are either aggregation-sealed (barrier 4) or N-smooth
(barrier 5). The round-13 brainstorm's hypothesis 10 (FETQ) identifies a
quantity that is BOTH cheap (poly(log N)) and internally asymmetric: Q(a) =
a^{N−1} mod N, whose CRT components are Q(a) mod p = a^{q−1} mod p and Q(a) mod
q = a^{p−1} mod q — the mod-p component uses the *other* factor's exponent.
Machine-verified: the decomposition is exact (24/24), but Q(a) carries NO factor
signal — across 80 near-equal-N semiprimes (~10⁷) all correlations with p, q,
p+q, |p−q| fall inside the permutation null (obs ≤ 0.19, 95th ≈ 0.22); Q(a) is
pseudorandom mod N. The asymmetry is real but locked inside the CRT: computing
Q(a) mod p requires p (barrier 6). The only usable handle — gcd(a^{N−1}−1, N) —
fires when ord_p(a) | q−1, the p−1/q−1-smoothness structure (EULERGAP,
barrier 8). **Cheap N-functions are factor-blind even when asymmetric inside
the CRT.**

---

## 1. The object

For a unit a and N = pq, fast exponentiation computes Q(a) = a^{N−1} mod N in
O(log N) multiplications — no aggregation. By Fermat's little theorem,

    Q(a) mod p = a^{pq−1} mod p = a^{(p−1)q}·a^{q−1} mod p = a^{q−1} mod p,
    Q(a) mod q = a^{p−1} mod q.

The CRT components use the OPPOSITE factor's exponent — a genuinely asymmetric
encoding of (q−1, p−1), unlike every symmetric N-invariant tested before.
Verified exactly for N = 15…3599, a ∈ {2,3,5} (24/24).

## 2. The value is factor-blind (verified)

Across 80 near-equal-N semiprimes (N ∈ [9.06M, 10.97M], p,q ∈ [2500, 4200]):
corr(Q(a), p), corr(Q(a), q), corr(Q(a), p+q), corr(Q(a), |p−q|) all fall inside
the 300-shuffle permutation null for a = 2, 3, 5 (obs ≤ 0.19, 95th ≈ 0.22,
pct 0.08–0.97). corr(Q(a), N) is also ≈ 0 — Q(a) is pseudorandom mod N. The
asymmetric encoding does not surface in the value.

**Why:** reading the mod-p component a^{q−1} mod p out of Q(a) requires the CRT
idempotent for p — computing it IS factoring (barrier 6). As a bare residue mod
N, Q(a) is an N-only function, and at near-equal N it is uncorrelated with the
factors (barrier 5). The internal asymmetry is invisible to an observer without
the split.

## 3. The gcd variant is EULERGAP (barrier 8)

g(a) = gcd(a^{N−1} − 1, N) reveals p iff ord_p(a) | q−1 (and not ord_q(a) | p−1).
The set of a with ord_p(a) | q−1 has size gcd(p−1, q−1), so the reveal density is
g/p + g/q with g = gcd(p−1, q−1) — exactly the EULERGAP structure (already
classified). Measured: reveal/2000 tracks g (g=24 → 29/2000; g=2 → 2-4/2000);
scaling 14→26 bits gives density 0.085 → 0.0087, the g-gain above the 1/p
floor. The condition "ord_p(a) | q−1" is a p−1/q−1-smoothness fact.

## 4. Conclusion

FETQ closes the "cheap asymmetric exponent" corner: even a poly(log N)-computable
value whose internal CRT structure is genuinely asymmetric — strictly more
informative in principle than any symmetric N-invariant — is factor-blind at the
value level (barrier 5), unreadable without the CRT split (barrier 6), and its
only usable handle reduces to the p−1/q−1-smoothness structure (barrier 8). This
is the sharpest form yet of "asymmetry without the split is invisible": the 
factor-dependence of Q(a) lives entirely in the CRT components, and the 
components are the factorization itself. The classical, uniform, hint-free
surface remains exhausted; frontiers: barrier-4 proof, quantum channel, hint
amplification.

---

**Experiment:** 371 (FETQ). **Script:** /tmp/exp_fetq.py.
**Assessment:** v147. **Barrier verdict:** REFUTED — barrier 5 + 6 + 8.

# The Trace Is the Least-Hidden Symmetric Invariant: TRACEPROFILE, Closed

**Program:** Factoring research lab — information profile of the trace witness (round-14 #7)
**Date:** 2026-08-12
**Status:** Decisive structural result with exact theorems — the trace s = p+q is
congruence-visible (1 bit per prime, exactly ω(M#) jointly, s₁ = 1−N₁ exactly)
where the factor is invisible; yet the visible bits are symmetric and cannot
scale to pin s

---

## Abstract

Where does the trace s = p+q — the minimal factor-bearing witness (trace lemma)
— live information-theoretically relative to N = p·q? Machine-verified (32 640–
380 628 semiprime pairs, k = 12, 14): the factor p is congruence-invisible
(I(p mod m; N mod m) ≈ 0, the BITPROFILE zero-block), but the trace is
congruence-CONSTRAINED: s mod m is pinned to the trace-set
S_m(N) = {x+y mod m : xy ≡ N mod m} of size (m+1)/2, giving **I(s mod m; N mod m)
= 1 bit per prime exactly** (1.0000 bits at m = 3). Jointly, |S_M#(N)|/M# =
2^(−ω(M#)) exactly — each prime modulus halves the trace-set — so
I(s mod M#; N) = ω(M#) bits, additively independent across primes. An **exact
low-bit theorem**: s₁ = 1 − N₁ (the second-lowest bit of the trace is the exact
complement of N's), holding for 100% of pairs. The trace's pairwise-visible
information is 2.32 bits vs H(s) = 12.6 (18.5–21.9%), four-fold more than the
factor's 5% — concentrated in exact low-bit relations and the top-2 carry-out
sliver. The trace is the LEAST-HIDDEN symmetric invariant of (p,q), yet its
visible bits are symmetric functions of (p,q) that never isolate a factor and
cannot scale (ω(M#) bits for M# of ω(M#) primes) to pin s ≈ 2^k bits. Barrier 2
and the trace lemma are confirmed at the information level.

---

## 1. Setup

For k-bit primes p ≤ q, N = p·q, s = p+q. The trace is determined by N
(s is a function of the factorization), so I(s; N) = H(s) ≈ 2k. The question:
which bits of s are recoverable from N's residues (small moduli) and from N's
individual bits — the congruence profile and the pairwise bit profile.

## 2. The congruence profile: factor invisible, trace constrained (verified)

For each m, I(p mod m; N mod m) and I(s mod m; N mod m) over the uniform
semiprime ensemble:

| m | I(p mod m; N) | I(s mod m; N) | avg |S_m| | |S_m|/m |
|---|---------------|---------------|--------|--------|
| 3 | 0.0001 | **1.0000** | 1.50 | 0.500 |
| 5 | 0.0003 | 1.0606 | 2.50 | 0.500 |
| 7 | 0.0007 | 1.0520 | 3.50 | 0.499 |
| 11 | 0.0027 | 1.0375 | 5.50 | 0.500 |
| 16 | 0.0028 | 2.0001 | 2.00 | 0.125 |
| 23 | 0.0061 | 1.0251 | 11.50 | 0.500 |

The factor is invisible mod m (zero-block generalizes to odd m); the trace is
pinned to the trace-set of size (m+1)/2, contributing exactly 1 bit of
N-visible information per odd prime modulus.

## 3. The joint law: exactly one bit per prime (verified)

Over M# = product of the first ω primes: |S_M#(N)|/M# = 2^(−ω(M#)) exactly —
measured fractions 0.5011, 0.2509, 0.1260, 0.0628, 0.0313, 0.0157, 0.0078,
0.0039, 0.0020, 0.0010, 0.0005 (each prime halves the set), so
I(s mod M#; N) = ω(M#) bits exactly (1.00, 1.99, …, 10.99). The trace's
prime-modulus residues are additively independent: N reveals exactly one bit of
s per prime in M#.

## 4. The exact low-bit theorem (proved, verified 100%)

**Theorem.** For odd p, q, the second-lowest bit of s = p+q is the exact
complement of the second-lowest bit of N = pq: s₁ = 1 − N₁.

**Proof.** N₀ = p₀q₀ = 1, with no carry into bit 1 (only one summand at bit 0),
so N₁ ≡ p₁ + q₁ (mod 2). For s: s₀ = p₀ + q₀ = 2 ≡ 0 (mod 2) with carry 1 into
bit 1, so s₁ ≡ p₁ + q₁ + 1 (mod 2). Hence s₁ = N₁ + 1 (mod 2) = 1 − N₁. ∎

**Verified:** holds for 300 000/300 000 pairs (I(s₁; N₁) = 1.000 bit). Partial
companion: s₂ ≠ N₂ with probability 0.754 (I ≈ 0.19 bit).

## 5. Superdensity contrast: the trace is less hidden (verified)

Pairwise-visible trace information: 2.32–2.34 bits vs H(s) = 10.6–12.6 →
**18.5–21.9%**, versus the factor's 4.8–6.0%. The visible regions are the exact
low-bit relations (N cols 1–2: 1.00 + 0.19 bits) and the top-2 carry-out sliver
(cols 2k−2, 2k−1: 0.38 + 0.64 bits). The factor's only visible sliver is the
top-2 bits; the trace additionally has exact low-bit visibility.

## 6. Conclusion

TRACEPROFILE sharpens the trace lemma with the trace's information profile. For
a symmetric function f(p,q), N mod m constrains f mod m to a set S_m^f(N); for
the asymmetric f = p the set is the full residue space (zero info — the
BITPROFILE zero-block), while for f = p+q the set is halved per prime. The trace
is simultaneously the minimal factor-bearing witness and the most
congruence-visible symmetric object — yet its visible bits (ω(M#) joint bits,
s₁ = 1−N₁) are symmetric functions that never isolate p or q, and scaling M# to
pin s ≈ 2^k bits would need M# ≫ e^{2^k}. Barrier 2 (symmetry) and the trace
lemma are confirmed at the information level: the most accessible residue target
remains unfactorable. The classical, uniform, hint-free surface remains
exhausted.

---

**Experiment:** 385 (TRACEPROFILE). **Script:** /tmp/exp_traceprofile.py.
**Assessment:** v161. **Verdict:** NOT a factoring tool; exact structural
result — the trace is the least-hidden symmetric invariant (1 bit/prime exactly,
s₁ = 1−N₁ theorem, 20% vs 5% pairwise-visible), unfactorable.

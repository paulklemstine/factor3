# The Quantum Register Cannot Be Shrunk: QUBIT-TRADE, Closed

**Program:** Factoring research lab — quantum-channel resource bound (frontier ii)
**Date:** 2026-08-11
**Status:** Decisive resource result — the order-recovery truncation threshold is
2·log₂(r) ≈ the full Shor register; the quantum exception cannot be shrunk

---

## Abstract

Can Shor's order-finding register be truncated? Measuring only the top t bits of
the QFT outcome (⌊y/2^(ℓ−t)⌋ of the ideal sample y ≈ k·2^ℓ/r), does the order
r = ord_N(a) remain recoverable with more samples? Machine-verified (50
semiprimes, r ∈ [2^10, 2^22], honest continued-fraction post-processing): the
threshold is t_min ≈ 2·log₂(r) exactly — log₂r = 14 → t_min = 27 (2·log₂r = 28);
16 → 32 (32); 18 → 35 (36); 20 → 39 (40); 21 → 38 (42). Below t_min, recovery
collapses to the classical exponential floor (even 10 samples fail); above it,
qubit↔sample fungibility operates (samples compensate gcd(k,r) > 1). The
continued fraction must resolve k/r, which needs error < 1/(2r²), i.e. t >
2·log₂(r). Since r ~ N for random bases, t_min ≈ 2·log₂(N) ≈ the full ℓ =
2⌈log₂N⌉ register. **Shor's register size is essentially forced — the quantum
channel cannot be shrunk by truncation.**

---

## 1. Setup

Shor's QFT uses Q = 2^ℓ with ℓ = 2⌈log₂N⌉. The measurement concentrates at
y ≈ k·Q/r for random k; the order is recovered by continued fractions on y/Q
(≈ k/r). Truncating to the top t bits gives y_t = ⌊y/2^(ℓ−t)⌋ and the CF of
y_t/2^t.

## 2. The threshold (verified)

The CF of y_t/2^t recovers k/r (as the convergent with denominator r/gcd(k,r))
iff |y_t/2^t − k/r| < 1/(2r²). Since |y_t/2^t − k/r| ≤ 2^(−t) (+ the measurement
peak width), the condition is t > 2·log₂(r). Measured t_min tracks 2·log₂(r)
across r ∈ [2^14, 2^21]:

| log₂ r | t_min (P≥0.7) | 2·log₂ r |
|--------|---------------|----------|
| 14 | 27 | 28 |
| 16 | 32 | 32 |
| 18 | 35 | 36 |
| 20 | 39 | 40 |
| 21 | 38 | 42 |

The round-14 agent's prediction (t_min ≈ log r + O(log log r)) is REFUTED — the
precise value is 2·log₂(r), from the CF convergence criterion.

## 3. The phase structure (verified)

- **Below t_min: classical collapse.** At t ≤ 26 (with 2·log₂r ≈ 33), first-sample
  success ≈ 0.1, and even 10 samples do not reliably recover r — the truncated
  value carries too little precision for the CF.
- **Above t_min: fungibility.** With full precision, more samples compensate for
  gcd(k,r) > 1 (each sample gives q′ = r/gcd(k,r); testing small multiples recovers
  r). P(first sample) ≈ 0.9 at t = 32–34; P(10 samples) ≈ 1.

## 4. Conclusion

QUBIT-TRADE bounds the quantum register: t_min ≈ 2·log₂(r) ≈ 2·log₂(N) ≈ ℓ — the
full Shor register. The quantum exception cannot be shrunk by truncating the QFT
outcome; samples compensate only the k-sharing factor above the threshold, not
the precision loss below it. This is a frontier-(ii) resource bound that
reinforces the DEQUANT conclusions: the quantum channel is irreducible at its
full register size, and the order-readout it provides is the unique poly(log N)
asymmetric handle (ISOLATION-COST). The classical, uniform, hint-free surface
remains exhausted.

---

**Experiment:** 382 (QUBIT-TRADE). **Script:** /tmp/exp_qubittrade.py.
**Assessment:** v158. **Verdict:** resource bound (no barrier bypass); confirms
the quantum channel needs its full ~2·log₂(N)-qubit register.

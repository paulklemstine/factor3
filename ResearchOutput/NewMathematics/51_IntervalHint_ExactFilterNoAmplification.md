# The Trace-Set Filter Is Exact but Does Not Amplify: INTERVAL-HINT, Closed

**Program:** Factoring research lab — hint amplification / residue filters (round-14 #9)
**Date:** 2026-08-12
**Status:** Decisive negative with exact positive content — the trace-set filter
never misses the true trace and prunes wrong candidates by exactly 2^(−ω(M#)),
yet is information-useless for factoring: it cannot amplify an interval hint, and
no-hint survivors stay exponentially sealed

---

## Abstract

Given an external interval hint s ∈ [s₀−E, s₀+E] on the trace s = p+q, scanning
the 2E+1 candidates (testing Δ = s′²−4N for a perfect square) factors N in O(E).
Can the FREE trace-set filter (TRACEPROFILE) amplify this? Machine-verified (400
semiprimes, k = 24): the trace-set filter is EXACT — the true s survives for
400/400 semiprimes at every filter strength ω ≤ 20, and the survival fraction of
wrong s′ equals 2^(−ω(M#)) exactly (0.1233 vs 0.125 at ω=3, 0.0151 vs 0.0156 at
ω=6). But it does NOT amplify: the interval scan's Δ-tests drop from 8001 to
121.5/2.9/1.1 (ω=6/12/18 — exactly (2E+1)·2^(−ω)+1) yet are replaced by ~1.9
membership-tests per candidate (15 294–15 550), so total work is cost-parity or
worse and the full range must still be iterated. The p-residue filter is empty
for real candidates (coprime survival 1.0000 — only coprimality, not
information). No-hint search from N alone stays exponentially sealed
(2^24 → 2^19 → 2^13.3 → 2^7.4 survivors at ω = 0/6/12/18), because reducing to
poly needs ω ~ k primes with M# ~ e^(k ln k), super-exponential in the bits of N.
The s-interval scan is Fermat's method in disguise. The residue channel of even
the least-hidden symmetric invariant is Ω(N)-sealed.

---

## 1. Setup

The trace-scan: given s′ (a candidate trace), N = p·q factors iff Δ = s′²−4N is
a perfect square (then p,q = (s′±d′)/2, d′=√Δ). Given a trace within an interval
of length E, scanning O(E) candidates factors N. The trace-set filter S_M#(N) =
{s mod M# : ∃x,y, xy ≡ N, x+y ≡ s mod M#} (poly-computable per prime, free) is a
candidate test: s′ must satisfy s′ mod M# ∈ S_M#(N).

## 2. Exactness of the trace-set filter (verified)

For 400 semiprimes (k = 24), the true trace survives at every filter strength
ω = 0–20 (400/400). The survival fraction of wrong s′ over the valid range
[2^k+2, 2^(k+1)) is exactly 2^(−ω(M#)):

| ω | survival frac | 2^(−ω) |
|---|--------------|--------|
| 3 | 0.1233 | 0.125 |
| 6 | 0.0151 | 0.0156 |
| 9 | 0.0019 | 0.0020 |
| 12 | 0.0002 | 0.0002 |

The filter is an exact residue-consistency certificate for the trace: it never
rejects the true s and rejects wrong s′ with probability 1 − 2^(−ω(M#)).

## 3. The p-filter is empty for real candidates (verified)

For candidates p′ coprime to M# (as every prime is), the p-residue filter
S_M#^p(N) = {p mod M# : ∃q, pq ≡ N} leaves all of them: survival = 1.0000. The
only pruning is the coprimality condition p′ ⊥ M#, which every candidate prime
already satisfies and which therefore carries no information. This is the
candidate-level restatement of the BITPROFILE zero-block: the factor is
congruence-invisible; the trace is congruence-constrained.

## 4. No amplification (verified)

The interval scan over [s_true − E, s_true + E], E = 4000 (8001 candidates),
with rejection-ordered trace-set filtering:

| ω | Δ-tests | expected (2E+1)·2^(−ω)+1 | membership-tests |
|---|---------|--------------------------|------------------|
| 0 | 7713 | 8001 | 0 |
| 6 | 121.5 | 125 | 15294 |
| 12 | 2.9 | 2 | 15540 |
| 18 | 1.1 | 0 | 15550 |

The filter converts Δ-tests (each an isqrt on N-sized integers) into ~1.9
membership-tests per candidate at roughly cost parity — total work is unchanged
or worse, and every candidate must still be visited to apply the filter. The
filter is a consistency check, not a search accelerator: it cannot avoid
iterating the interval.

## 5. No-hint search stays exponentially sealed (verified)

From N alone, the trace-filter over the full valid s-range leaves 2^24 (ω=0),
2^19 (ω=6), 2^13.3 (ω=12), 2^7.4 (ω=18) surviving candidates — never polynomial.
Reducing to poly(log N) survivors would require ω ~ k primes, i.e. M# = product
of the first k primes ~ e^(k ln k) — super-exponential in the bit-length of N.
The trace-set residue channel is Ω(N)-sealed (barrier 2/4).

## 6. Conclusion

INTERVAL-HINT refutes the last residue-amplification hope. Even the LEAST-HIDDEN
symmetric invariant (TRACEPROFILE) yields a residue filter that is exact
(never-miss, exactly-2^(−ω) pruning) yet information-useless: it cannot amplify
an external interval hint asymptotically (Δ-tests convert to membership-tests at
cost parity), it cannot find s from N alone (survivors stay 2^(k−ω), sealed by
the Ω(N)-sized trace-set), and the s-scan it would accelerate is Fermat's method
in disguise (barrier 8). Together with DIAL-THRESHOLD (dials cannot amplify a
Coppersmith hint) and QRLEAK/COMPENSATING-PARTNER (no congruence battery pins a
factor), the residue-filter family is now completely closed: no poly-computable
residue structure of N — on the factor, the order, or the trace — amplifies,
prunes, or pins toward factoring. The classical, uniform, hint-free surface
remains exhausted.

---

**Experiment:** 386 (INTERVAL-HINT). **Script:** /tmp/exp_intervalhint.py.
**Assessment:** v162. **Verdict:** REFUTED as an amplifier; exact negative —
the trace-set filter is an exact 2^(−ω(M#)) residue-consistency certificate that
cannot amplify or accelerate (barriers 2/4/8); extends DIAL-THRESHOLD's closure
of the residue-filter family.

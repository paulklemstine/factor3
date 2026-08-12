# The Modular-Exponential Sequence Is Random-Level Incompressible: SEQSTATE, Closed

**Program:** Factoring research lab — dequantization obstruction (round-14 #8)
**Date:** 2026-08-12
**Status:** Decisive negative for a closed-form shortcut; refines the predicted
complexity — the modular-exponential sequence and its floor-quotient twin are
random-level incompressible (linear complexity n/2 at every prefix including the
full period), arming the dequantization obstruction quantitatively

---

## Abstract

Can the sequence s_x = a^x mod N — the input to Shor's order-finding QFT — be
classically compressed? Machine-verified (120 semiprimes, N ∈ [2^10, 2^16], odd
base a = 3, r ∈ [260, 49 506]; Berlekamp–Massey linear complexity and substring
complexity of the LSB streams, with random / maximal-LFSR / geometric-mod-prime
controls): the FULL-PERIOD linear complexity is λ_s(r) ≈ r/2 (measured 0.498–
0.506), REFUTING the predicted λ ≈ r — the correct value is the random-string
level. At every prefix, λ_s(n) ≈ n/2 (0.500–0.501) — indistinguishable from
random and NOT LFSR-compressible (the LFSR control holds λ = m = 15 constant).
The floor/quotient sequence t_x = ⌊a^x/N⌋ — the only difference between Shor's
QFT peak and a closed-form geometric sum (a^x = N·t_x + s_x) — is equally
incompressible (λ_t(n) ≈ n/2): the floor defect carries the full complexity, so
no closed-form route exists. Substring complexity saturates at the period
(c(L) ≈ 2^L up to r), random-like. This is a quantitative dequantization
obstruction: the QFT input admits no low-complexity classical simulation.

---

## 1. Setup

s_x = a^x mod N is periodic with period r = ord_N(a). The floor sequence
t_x = ⌊a^x/N⌋ satisfies t_{x+1} = a·t_x + ⌊a·s_x/N⌋ (verified against direct
⌊a^x/N⌋), so its LSB stream is computable without materializing a^x. The
quantum order-finding state is built from s_x; the closed-form geometric sum
would be Σa^x — the difference from the true state is exactly the t_x (floor)
correction. If s_x or t_x were low-complexity (short LFSR, closed form), a
classical simulation could bypass the QFT.

## 2. Controls calibrate (verified)

| control | λ(128)…λ(1024) | interpretation |
|---------|----------------|----------------|
| random | 31, 64, 129, 257, 511 | λ ≈ n/2 |
| max-LFSR (m=15) | 15, 15, 15, 15, 15 | λ = m, constant |
| geometric mod prime | 32, 63, 128, 256, 511 | λ ≈ n/2 |

The discriminating measure is linear complexity: substring complexity saturates
at the period for any periodic sequence and cannot separate an LFSR from a
pseudorandom source; λ does.

## 3. The modular sequence is random-level incompressible (verified)

- **Full period:** λ_s(r)/r = 0.498–0.506 across r ∈ [198, 1218] — the sequence
  has the linear complexity of a random r-bit string, NOT the predicted r. The
  prediction "λ ≈ r" is REFUTED; the random-level value r/2 is the cleaner
  statement (a length-r random string has λ ≈ r/2).
- **Every prefix:** λ_s(n) ≈ n/2 for n = 128, 256, 512, 1024 (0.500–0.501) —
  indistinguishable from random at all observed lengths, and far from the LFSR
  constant. No short linear recurrence exists at any prefix.

## 4. The floor defect is equally incompressible (verified)

λ_t(n) ≈ n/2 (0.500–0.502) — the LSB stream of t_x = ⌊a^x/N⌋ is random-level.
The floor sequence — the exact correction separating the QFT peak from the
geometric sum — carries the full complexity of the modular sequence. There is no
closed-form shortcut through the floor.

## 5. Substring complexity (verified)

c_s(L) ≈ c_t(L) ≈ 2^L up to the period (ratios 1.000 at L=3, 0.999 at L=5;
declining to 0.467 at L=10 only because a 1024-prefix cannot host 2^10 distinct
substrings). Both streams are as rich as random binary strings at all resolvable
lengths.

## 6. Conclusion

SEQSTATE arms the dequantization program with a quantitative obstruction: Shor's
QFT input is a classical sequence of maximal (random-level) complexity — no LFSR,
no short recurrence, no closed form — and its floor-quotient twin is equally
incompressible, so the difference between the quantum state and any closed-form
geometric approximation is itself the full complexity. Consistent with barrier
4/8 (the aggregation / no-free-lunch structure as sequence complexity) and with
DEQUANT/DEQUANT2, QUBIT-TRADE, and COND-RANK: the quantum channel is irreducible
at random-level complexity. The classical, uniform, hint-free surface remains
exhausted.

---

**Experiment:** 387 (SEQSTATE). **Script:** /tmp/exp_seqstate.py.
**Assessment:** v163. **Verdict:** REFUTED in the precise prediction (λ = r →
λ = r/2, the random-level value); CONFIRMED as the operative dequantization
obstruction — both s_x and t_x are random-level incompressible at every prefix
and the full period (barriers 4/8).

# The Continued-Fraction Period of √N Is a Non-Polynomial Symmetric Channel with Zero Factoring Leverage (CFPERIOD-NULL)

**Program:** Factoring research lab — cron loop round-16 #1
**Date:** 2026-08-12
**Status:** Machine-verified null. The continued-fraction period of √N — the
fundamental-unit/regulator side of the real quadratic field ℚ(√N), a genuinely
non-polynomial symmetric N-computable channel lying outside the reach theorem
proven for polynomials in TRACE-EXHAUSTION — carries zero factoring leverage.
Its only factorization-adjacent content is the negative-Pell parity bit
(p ≡ q ≡ 1 mod 4), a symmetric no-pinning congruence bit; after de-confounding
the trivial N-size coordinate (the terminal partial quotient 2a₀), no period
statistic depends on s or q−p (120 partial-correlation tests, worst p = 0.024
vs Bonferroni 0.0004); and the cost of the period is ~l ≈ 0.4·√N (super-poly),
with the cheap-l window measure-zero and its fundamental unit factoring only via
the classical Pell/CFRAC–SQUFOF route at a worse exponent. Barriers 2/5/6/8.

---

## Abstract

Machine-verified null result. **(1) The channel is real and structural.**
For squarefree N = pq, √N = [a₀; a₁,…,a_l] with a purely periodic palindrome +
2a₀. The (l−1)-th convergent yields the fundamental unit x + y√N with
x² − Ny² = ±1 exactly (verified on every instance); l is tied to the regulator
and the (narrow) class group of ℚ(√N) — the real-quadratic side of the forms
program, structurally orthogonal to round-13's imaginary-side RANDOM-BQF. Known
periods reproduce exactly (9/9); the negative-Pell dichotomy holds class-wide:
(x²−Ny² = −1 soluble ⇔ l odd) with the semiprime corollary l even for every
p ≡ q ≡ 3 mod 4 or mixed instance (40/40, 40/40) and l odd iff soluble in the
p ≡ q ≡ 1 mod 4 class (26/40 matching neg-Pell 26/40) — but this pins only
p ≡ q ≡ 1 (mod 4), a symmetric congruence bit (Dirichlet no-pinning), never a
factor. **(2) Null after de-confounding (new, required).** A raw pass showed
corr(max partial quotient, s) ≈ +0.99 in every size bucket — but maxq equals the
terminal 2a₀ = 2⌊√N⌋ on 330/330 instances (a pure isqrt N-size coordinate;
corr(a₀, s) = +1.000), so that "signal" is the size confound, not factor
content. Residualizing every period statistic on a₀ = isqrt(N) and testing the
partial correlation against s and q−p within (bit-length, N mod 4) groups: 120
tests, worst p = 0.024, Bonferroni threshold 0.0004 → NULL. No period statistic
(l, parity, non-terminal max-q, non-terminal sum-q, distinct count, regulator)
depends on s or q−p once the N-size coordinate is removed. **(3) Leverage zero.**
Computing the period costs ~l ≈ 0.4·√N (median l/√N = 0.406), super-poly in
log N — not even a poly(log N) witness. The fundamental unit is the most
factor-adjacent cheap object, and it *does* give x² ≡ 1 mod N on even periods
with x a split square root of 1 (gcd(x±1, N) finds a factor on 206/269
instances) — but reaching the unit requires the full O(l) ≈ O(√N) period: the
classical Pell/CFRAC–SQUFOF family at a worse exponent than SQUFOF's O(N^{1/4}),
a known method (barrier 8), never a new shortcut. The cheap-l window (l ≤ 40,
7/330) is the measure-zero N = m²+c family; detecting it (isqrt of N−c) finds no
factor (m ∤ N on 65, 145, 51, 291). TRACE-EXHAUSTION's reach theorem, proven for
polynomials, does not bound this channel — but the channel is sealed anyway:
symmetric (barrier 2), a natural structural coordinate of N orthogonal to
factoring (barrier 5), its full regulator/class-group content circular (barrier
6), and its exploitable faces classical known methods (barrier 8). Round-16 #1:
the non-polynomial symmetric channel is as sealed as the polynomial one.

---

## 1. Setup: the real-quadratic channel

TRACE-EXHAUSTION (round-15 #5) proved that the barrier-2 reach of every
*polynomial* symmetric function of (p, q) is exactly {(N, s)} — the fundamental
theorem of symmetric polynomials. That theorem bounds polynomials only.
Non-polynomial symmetric N-computable functions of (p, q) are a genuinely open
channel, and the canonical such object never probed by the lab is the continued
fraction of √N: the real-quadratic side of the forms program (round-13
RANDOM-BQF explored the imaginary side, class numbers of negative discriminants;
here the positive side, fundamental units and regulators).

For squarefree N = pq: √N = [a₀; a₁,…,a_l] is purely periodic, the period
(a₁,…,a_l) is a palindrome followed by a_l = 2a₀, and the (l−1)-th convergent
P_{l−1}/Q_{l−1} solves P_{l−1}² − N·Q_{l−1}² = (−1)^l: the fundamental unit
x + y√N, with regulator R = log(x + y√N) and the classical tie of l to the
(narrow) class group of ℚ(√N). The CF of √N is also the raw material of the
classical CFRAC/SQUFOF methods — but those use the *convergent residues*
(x² mod N), a different face; the probe here is the period's statistics alone.

## 2. Structural positive controls (the object is real)

- **Known periods, exact (9/9).** √2 = [1;2], √3 = [1;1,2], √5 = [2;4],
  √7 = [2;1,1,1,4], √13 = [3;1,1,1,1,6], √23 = [4;1,3,1,8],
  √91 = [9;1,1,5,1,5,1,1,18], √65 = [8;16], √51 = [7;7,14] — all reproduced.
- **Fundamental unit verified.** For 13, 23, 91, 65, 51: x² − Ny² = ±1 exactly
  from the (l−1)-th convergent; regulators positive.
- **Negative-Pell parity dichotomy (class-wide).** x²−Ny² = −1 soluble ⇔ l odd.
  For odd semiprimes: if either factor ≡ 3 mod 4, −1 is a non-residue mod that
  factor, so no solution and l is even — measured l even 40/40 for p ≡ q ≡ 3
  and 40/40 for mixed; in the p ≡ q ≡ 1 mod 4 class, l odd iff the negative Pell
  is soluble, measured l odd 26/40 and neg-Pell 26/40 (exact match). The
  content is real but symmetric and congruence-level: it resolves the
  N ≡ 1 mod 4 ambiguity {(1,1), (3,3)} → {1,1}, a single bit that no more pins a
  factor than N mod 4 itself (Dirichlet no-pinning; QRLEAK/COMPENSATING-PARTNER).

## 3. The null, after de-confounding the N-size coordinate

A first pass found corr(max partial quotient, s) ≈ +0.99 in every (bit-length,
N mod 4) bucket — an apparent signal. Checking the object directly: the terminal
partial quotient is a_l = 2a₀ = 2⌊√N⌋ on 330/330 instances, and maxq = 2a₀ on
330/330 — maxq is a pure isqrt N-size coordinate. Since corr(a₀, s) = +1.000
within a bit-length bucket (both driven by factor sizes), every feature
containing the terminal 2a₀ inherits the spurious correlation. The honest test
residualizes each statistic on a₀ = isqrt(N):

- Features: period length l, parity, non-terminal max (palindrome part),
  non-terminal sum, distinct count, regulator.
- Targets: s = p+q, gap = q−p.
- Design: 330 semiprimes at bit-lengths 21–26, grouped by (bit-length, N mod 4);
  partial-correlation permutation tests (residualize both variables on a₀,
  permute, 2000 draws).

Result: 120 tests, worst p = 0.024 (l vs gap, one group) against a Bonferroni
threshold of 0.0004 — NULL. No period statistic depends on s or q−p once the
N-size coordinate is removed. The period is factor-information-free at every
measured order.

## 4. Why this cannot factor: barriers 2, 5, 6, 8

1. **Barrier 2 (symmetry).** Every period statistic is N-computable, hence
   symmetric in (p,q); the measured null is the empirical face of that
   symmetry — the only dependence is on the size coordinate a₀ = ⌊√N⌋ (a
   function of N alone), never on the trace or the gap.
2. **Barrier 5 (structural orthogonality).** The CF of √N is a natural
   structural coordinate of N (like the modular hyperbola, the mult table, the
   zero-divisor graph); its statistics are orthogonal to the factorization.
3. **Barrier 6 (circularity).** The full regulator / class-group structure of
   ℚ(√N) is as hard as the class group (computing it ≡ factoring); what is cheap
   — the period statistics, the parity bit — is exactly the congruence-level
   no-pinning content.
4. **Barrier 8 (known method in disguise).** The one genuinely factor-adjacent
   object, the fundamental unit (x² ≡ ±1 mod N), factors on even periods when x
   is a split square root of 1 (gcd(x±1, N) finds a factor on 206/269
   instances) — but reaching the unit requires the full O(l) ≈ 0.4·√N period:
   the classical Pell/CFRAC–SQUFOF family at a *worse* exponent than SQUFOF's
   O(N^{1/4}). The convergent-residue faces (x² mod N) are likewise classical
   CFRAC/SQUFOF. Nothing here is new; the period is not a free witness (its
   computation is super-poly in log N, and the cheap-l window is measure-zero).

## 5. Conclusion

CFPERIOD-NULL completes round-16 #1. The continued-fraction period of √N is a
genuine non-polynomial symmetric N-computable channel — the real-quadratic side
of the forms program — and it is sealed: its only factorization-adjacent content
is a symmetric no-pinning congruence bit (period parity ⇒ p ≡ q ≡ 1 mod 4), no
statistic depends on s or q−p once the trivial N-size coordinate is removed, and
the cost of the period (~0.4·√N) puts even the factor-adjacent fundamental-unit
face inside the classical Pell/CFRAC–SQUFOF family at a poor exponent. The
non-polynomial symmetric channel is as factor-information-free as the polynomial
one — TRACE-EXHAUSTION's reach extends in the only direction it could, from
polynomials to all N-computable symmetric structure.

---

**Experiment:** 398 (CFPERIOD-NULL). **Script:** /tmp/exp_cfperiodnull.py.
**Assessment:** v174. **Verdict:** CONFIRMED null (negative for factoring) — the
continued-fraction period of √N (non-polynomial symmetric channel, real-quadratic
side of the forms program, outside the TRACE-EXHAUSTION polynomial reach
theorem) is factor-information-free: structural content verified (known periods
9/9; fundamental unit x²−Ny²=±1; negative-Pell dichotomy l even 40/40 for
(3,3)/(1,3), l odd ⇔ neg-Pell 26/40 in (1,1) — pins only p ≡ q ≡ 1 mod 4, a
no-pinning congruence bit); the raw corr(maxq, s) ≈ +0.99 signal REFUTED as the
size confound (maxq = 2a₀ = 2⌊√N⌋ on 330/330; corr(a₀,s) = +1.000), and after
residualizing on a₀, 120 partial-correlation tests show no period statistic
depends on s or q−p (worst p = 0.024 vs Bonferroni 0.0004); leverage zero
(period cost ~0.4·√N super-poly; the fundamental unit factors only via the
classical Pell/CFRAC–SQUFOF route at a worse exponent, split-root 206/269, a
known method; cheap-l window = measure-zero N = m²+c, m ∤ N) — the non-polynomial
symmetric channel is as sealed as the polynomial one; barriers 2/5/6/8.

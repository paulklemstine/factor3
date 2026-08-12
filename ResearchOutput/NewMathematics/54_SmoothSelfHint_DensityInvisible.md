# The p−1 / ECM Weakness Is Residue-Invisible: SMOOTH-SELFHINT-DENSITY, Closed

**Program:** Factoring research lab — self-hint / instance-class probe (round-14 #10)
**Date:** 2026-08-12
**Status:** Decisive negative with sharp positive content — the B-smoothness of
p−1 (the structural weakness Pollard's p−1 method and ECM exploit) is
undetectable from N alone in every tested form, and the reason is quantified by
a new asymmetric-vs-symmetric divisibility dichotomy: N's residues reveal the
symmetric "a factor is ≡ 1 mod ℓ" event (0.31 bits at ℓ = 3) but carry zero
asymmetric information about which factor — the divisibility-level face of
barrier 2

---

## Abstract

Machine-verified on random k-bit semiprimes (k = 14, 16, 18; m up to 200 000):
whether the smaller factor p has p−1 B-smooth (L(p−1) ≤ B) — the instance
weakness that makes Pollard's p−1 method or ECM succeed — is invisible from N
alone. (1) **Asymmetric residue leak is zero:** I(N mod ℓ; ℓ | p−1) = 0.0000–
0.0005 bits at the shuffled-null level for ℓ = 3, 5, 7, 11 at every k — from N's
residues one cannot tell which factor is ≡ 1 mod ℓ. (2) **The symmetric event
leaks strongly:** I(N mod ℓ; ℓ | p−1 OR ℓ | q−1) = 0.313, 0.036, 0.015, 0.005
bits at ℓ = 3, 5, 7, 11 — stable across k; N ≡ 2 mod 3 forces one factor ≡ 1
mod 3 (P = 1.000) while the asymmetric P(p ≡ 1 | N mod 3) stays at the base
0.499. The QRLEAK/COMPENSATING-PARTNER no-pinning structure, stated at the
divisibility level: symmetry is visible, asymmetry is not. (3) **The joint
residue vector does not detect full B-smoothness:** I(S_1000; N mod 1155) =
0.006 bits ≈ shuffled null 0.005. (4) **No instance-class self-hint:** the
N-computable smoothness events "N−1 is B-smooth" and "N+1 is B-smooth" do not
predict p−1 smoothness (correlation ≤ 0.014, MI ≤ 0.0001 bits). (5) **The
smoothness density is conditioning-invariant and fully explained:** P(L(p−1) ≤
B) matches the parity-adjusted Dickman baseline ρ_even(log(2^k/2)/log B)
within ~0.04 (the residual is the powers-of-2 effect, an N-independent property
of shifted primes), and P(L(p−1) ≤ B | N mod ℓ = n) equals the base for every
n. The p−1/ECM-weak instance class is undetectable from N: the weakness is an
asymmetric property of a specific factor, and asymmetry is uncomputable from N
(barriers 2/5), so no self-generated hint toward a known method exists
(frontier-iii statement now complete — hints must be genuinely external).

---

## 1. Setup

Random k-bit semiprimes N = p·q, p ≤ q, both primes in [2^(k−1), 2^k). For each:
L(p−1) = largest prime factor of p−1 (sympy.factorint), the smoothness events
S_B = [L(p−1) ≤ B] for B = 100, 1000, 10^4, and the per-prime divisibility
events ℓ | p−1. Features: N mod ℓ, N mod M# (coarse primorial 3·5·7·11 = 1155),
and the N-computable smoothness events [L(N−1) ≤ B], [L(N+1) ≤ B]. Metrics:
empirical mutual information I(S; F) with shuffled-label nulls, and conditional
densities. Baseline: Dickman ρ(u) computed numerically (ρ′ = −ρ(t−1)/t) for the
unconditioned and even-restricted (p−1 is even) versions.

## 2. The asymmetric/symmetric divisibility dichotomy (verified, new)

| ℓ | I(N mod ℓ; ℓ|p−1) | shuffled null | I(N mod ℓ; ℓ|p−1 OR ℓ|q−1) |
|---|------------------|---------------|-----------------------------|
| 3 | 0.0000 (k=16) | 0.0000 | 0.3123 |
| 5 | 0.0001 | 0.0000 | 0.0363 |
| 7 | 0.0001 | 0.0001 | 0.0150 |
| 11 | 0.0002 | 0.0001 | 0.0050 |

(k = 16, m = 80 000; k = 14 and 18 give the same pattern — the asymmetric leak
stays at the null at every size.) The mechanism is exact at ℓ = 3: N mod 3 = 2
forces p·q ≡ 2, so (p,q) ≡ (1,2) or (2,1) mod 3 — one factor is always ≡ 1, and
N reveals this with certainty (P(OR | N ≡ 2) = 1.000, P(OR | N ≡ 1) = 0.497 =
P(both ≡ 1)). But P(p ≡ 1 | N mod 3 = n) = 0.497 / 0.501 for n = 1 / 2, equal to
the base rate 0.499: the identity of the ≡ 1 factor is uncomputable from N.
N's residues expose the symmetric divisibility profile of the factor pair and
nothing asymmetric.

## 3. Full B-smoothness is undetectable (verified)

- **Joint residue vector:** I(S_1000; N mod 1155) = 0.0059 bits (k=14), 0.0090
  (k=16) vs shuffled nulls 0.0052 / 0.0094 — noise-level. Aggregating the
  per-prime symmetric leaks cannot detect the conjunction "all of p−1's prime
  factors ≤ B", because the symmetric picture never identifies the factor and
  the per-prime events are individually weak.
- **Instance-class (N-computable smoothness):** corr([L(p−1) ≤ B], [L(N−1) ≤ B])
  = +0.009, MI 0.0001 bits; corr with [L(N+1) ≤ B] ≈ 0. The smoothness of
  N−1/N+1 (checkable from N alone) carries no information about the smoothness
  of p−1 — the p−1-weak instances form no N-detectable class.
- **Conditional density:** P(L(p−1) ≤ 1000 | N mod 3 = 1) = 0.7776 vs
  P(| N mod 3 = 2) = 0.7787 vs base 0.7781 (k=14); 0.638 / 0.633 vs 0.635 (k=16).
  The smoothness density does not move under N's residues.

## 4. The density baseline is fully understood (verified)

P(L(p−1) ≤ B) matches the parity-adjusted Dickman value ρ(log(2^k/2)/log B):

| k | B | observed | ρ(u) (all) | ρ_even (p−1 even) |
|---|-----|----------|-----------|-------------------|
| 14 | 100 | 0.368 | 0.258 | 0.329 |
| 14 | 1000 | 0.764 | 0.660 | 0.735 |
| 16 | 100 | 0.236 | 0.154 | 0.200 |
| 16 | 1000 | 0.625 | 0.527 | 0.591 |

The residual ~0.03–0.04 excess over ρ_even is the higher-powers-of-2 effect
(p−1 is often ≡ 0 mod 4, 8, …), an N-independent property of shifted primes.
The base weakness rate is high at these sizes (≈ 60–78% of semiprimes are
1000-weak) — which is exactly why p−1 works at all (barrier 8: a known method)
— yet the weak instances cannot be flagged from N: one must simply run p−1.

## 5. Conclusion

SMOOTH-SELFHINT-DENSITY refutes the last untested self-hint direction: the
statistical/instance-class smoothness hint. The p−1 / ECM weakness of an
instance is an asymmetric property of a specific factor, and the experiment
shows N carries zero asymmetric divisibility information (I(N mod ℓ; ℓ|p−1) = 0
at the null level) while fully revealing the symmetric profile (I(N mod ℓ;
ℓ|p−1 OR ℓ|q−1) = 0.31 bits at ℓ=3) — the divisibility-level statement of
barrier 2 (symmetry: any N-computable quantity is symmetric in (p,q); the
identity of the smooth factor is uncomputable from N). The joint residue vector,
the N−1/N+1 smoothness events, and the conditional density all confirm: the
weakness is invisible, and the density is fully explained by the parity-adjusted
Dickman baseline. Together with QRLEAK/COMPENSATING-PARTNER (no congruence
battery pins a factor), DIAL-THRESHOLD (dials cannot amplify a hint), and
INTERVAL-HINT (residue filters cannot amplify), the self-hint program is now
fully closed — no residue, dial, filter, or statistical smoothness self-hint
exists, and hints must be genuinely external (frontier iii complete). Barriers
2/5/8.

---

**Experiment:** 389 (SMOOTH-SELFHINT-DENSITY). **Scripts:**
/tmp/exp_smoothselfhint.py, /tmp/exp_smoothselfhint2.py.
**Assessment:** v165. **Verdict:** REFUTED as a self-hint in every tested form
— the p−1/ECM weakness is residue-invisible, instance-class-invisible, and the
smoothness density is conditioning-invariant at the parity-adjusted Dickman
baseline; CONFIRMED a sharp positive: the asymmetric/symmetric divisibility
dichotomy (I(N mod ℓ; ℓ|p−1) = 0 vs I(N mod ℓ; ℓ|p−1 OR ℓ|q−1) = 0.31 bits at
ℓ=3) — the divisibility-level face of barrier 2 (barriers 2/5/8).

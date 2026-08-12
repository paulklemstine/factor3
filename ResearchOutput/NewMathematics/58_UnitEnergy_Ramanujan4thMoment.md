# The Additive Energy of the Units Is the Ramanujan 4th Moment, Pointwise-Flat on gcd-Level Sets: a Symmetric Trace-Witness, Never a Factor (UNIT-ENERGY)

**Program:** Factoring research lab — cron loop round-15 #2
**Date:** 2026-08-12
**Status:** Decisive confirmation. The additive energy of the unit group
U = (Z/NZ)^×, E(U) = #{(u₁,u₂,u₃,u₄) ∈ U⁴ : u₁+u₂ ≡ u₃+u₄}, is the Ramanujan
4th moment with an exact closed semiprime form E(U) = ((p−1)(q−1)/N)(1+(p−1)³)
(1+(q−1)³) — a symmetric polynomial in (p,q), a function of (N, s=p+q) alone —
and the pointwise unit-pair-sum profile r_A(x) depends only on gcd(x,N) (flat on
the 4 gcd-level sets). Even the full additive distribution of the units carries
zero asymmetric factor content. Barriers 2/4/6/8.

---

## Abstract

Machine-verified on random semiprimes (10/10 three-way) and generic N (14/14),
plus symbolic expansion. **(1) The identity:** the additive energy of the unit
group equals the Ramanujan 4th moment, E(U) = (1/N) Σ_{x=0}^{N−1} |c_N(x)|⁴
where c_N(x) = Σ_{u∈U} e^{2πixu/N} is the Ramanujan sum (the |Â|⁴ face of the
Fourier transform of U's indicator). **(2) Exact closed semiprime form (new,
verified):** for N = pq, with a = p−1, b = q−1,

> E(U) = (ab/N)(1 + a³)(1 + b³) = ((p−1)(q−1)/N)·(1+(p−1)³)(1+(q−1)³),

and via the elementary symmetric σ₁ = a+b = s−2, σ₂ = ab = N−s+1 = φ(N),
E(U)·N = σ₂(1 + σ₁³ − 3σ₁σ₂ + σ₂³) — a symmetric polynomial in (p,q), i.e. a
function of **(N, s) alone** (barrier 2). **(3) Pointwise flatness (new, the
sharpest statement of the family):** the unit-pair-sum profile r_A(x) =
#{(u,v) ∈ U² : u+v ≡ x} depends only on gcd(x,N) — it is constant on each
gcd-level set {x : gcd(x,N)=d}, d ∈ {1, p, q, N} (verified FLAT on all levels,
and E-from-levels equals the direct count exactly). Since the Fourier transform
r̂_A = c_N² is gcd-invariant, the inverse transform r_A is gcd-invariant too:
**even pointwise, the additive structure of the units is N-symmetric.** No
asymmetric residue x, however chosen, distinguishes a factor. **(4) Recovery is
the cleanest of the family:** E·N − P(s) = 0 is a CUBIC in s (the quartic
leading terms σ₂⁴ and σ₂σ₁³ cancel), and s = p+q is its UNIQUE real root
(verified 15/15 semiprimes — no spurious real roots at all, unlike the
gcd-moments' {N−1−s, N−1, N+1} shadow roots). Yet s is symmetric and does not
factor. **(5) Barriers:** computing E(U) is Ω(N) aggregation — the Ramanujan
sweep or FFT — (barrier 4), the divisor-level form needs the factorization
(barrier 6), and E(U) = (1/N)Σ|c_N|⁴ is the classical Fourier/Ramanujan identity
with the modular-hyperbola literature studying exactly the unit-pair-sum counts
(barrier 8). The additive-combinatorics/Fourier lens adds no factoring leverage.

---

## 1. Setup

U = (Z/NZ)^×, |U| = φ(N). Additive energy E(U) = #{(u₁,u₂,u₃,u₄) ∈ U⁴ :
u₁+u₂ ≡ u₃+u₄ (mod N)}. With r_A(x) = #{(u,v) ∈ U² : u+v ≡ x}, E(U) =
Σ_x r_A(x)². Fourier: r̂_A(y) = Σ_x r_A(x)e^{2πixy/N} = (Σ_{u∈U} e^{2πiyu/N})² =
c_N(y)², and by Parseval E(U) = (1/N)Σ_y |r̂_A(y)|² = (1/N)Σ_y |c_N(y)|⁴. The
Ramanujan sum has the closed form c_N(y) = μ(N/gcd(N,y))·φ(N)/φ(N/gcd(N,y)).

## 2. Closed form, verified three ways

For N = pq, y ranges over gcd-level sets d = gcd(N,y) ∈ {1, p, q, N}: |c_N| = 1
(count φ(N)), p−1 (count q−1), q−1 (count p−1), φ(N) (count 1). Hence

E(U) = (1/N)[φ(N)·1 + (q−1)(p−1)⁴ + (p−1)(q−1)⁴ + φ(N)⁴]
     = (ab/N)(1 + a³)(1 + b³),  a = p−1, b = q−1.

Verified: direct count = Ramanujan moment = closed form on 10/10 semiprimes
(N up to ~2^10), and direct = Ramanujan on 14/14 generic N (including
squarefree 3-prime N and prime powers; e.g. E(30) = 312, E(9) = 162, E(105) =
58,032 — the generic form needs no semiprime assumption). Symbolically, with
σ₁ = s−2, σ₂ = ab = N−s+1: (1+a³)(1+b³) = 1 + (a³+b³) + a³b³ = 1 + (σ₁³ −
3σ₁σ₂) + σ₂³, so E·N = σ₂(1 + σ₁³ − 3σ₁σ₂ + σ₂³) = N⁴ − 4N³s + 4N³ + 6N²s² −
15N²s + 12N² − 3Ns³ + 12Ns² − 18Ns + 9N. Every term is a power of N and s —
**a function of (N, s) alone**; p and q appear only through s and N. This is
barrier 2 in exact form: the additive energy is a symmetric free witness of the
trace and nothing more.

## 3. Pointwise flatness: r_A(x) depends only on gcd(x, N)

r̂_A = c_N² is a function of gcd(y, N) only. The inverse Fourier transform
r_A(x) = (1/N)Σ_y c_N(y)² e^{2πixy/N} groups over gcd-level sets; each partial
sum Σ_{y: gcd(y,N)=d} e^{2πixy/N} = c_{N/d}(x) is itself a Ramanujan sum in the
lower modulus, a function of gcd(x, N/d) ⊆ a function of gcd(x, N). So r_A is
constant on each gcd-level set. Measured (N = 899 = 29·31, p = 29, q = 31):

| gcd(x,N) | count (φ(N/d)) | r_A(x) |
|----------|----------------|--------|
| 1  | 840 | 783 |
| 29 | 30  | 812 |
| 31 | 28  | 810 |
| 899| 1   | 840 |

FLAT on all four levels (all samples), and Σ_d φ(N/d)·r_d² = the direct E(U)
exactly. **Consequence:** every individual unit-pair sum count — the entire
distribution of how the units add — is determined by (gcd(x,N), N, s), i.e.
N-symmetric. There is no residue x at which "the units sum more than expected"
that could expose p or q. The additive structure of the unit group is factor-
blind not merely in aggregate but pointwise.

## 4. Trace recovery: unique real root of a cubic

E·N − P(s) = 0 with P(s) = σ₂(1+σ₁³−3σ₁σ₂+σ₂³) in s. Despite four σ-factors,
P is a CUBIC in s (the s⁴ coefficients of σ₂⁴ = (N−s+1)⁴ and σ₂σ₁³ =
(N−s+1)(s−2)³ cancel). Its roots on samples:

| N | p,q | s = p+q | real roots of P(s) − E·N |
|---|-----|---------|--------------------------|
| 3233 | 53,61 | 114 | {114} |
| 2021 | 43,47 | 90  | {90} |
| 2537 | 43,59 | 102 | {102} |
| 3127 | 53,59 | 112 | {112} |

s is the unique real root in **15/15** samples — the cleanest trace recovery in
the free-witness family (the gcd-moments carried spurious real roots N−1−s,
N−1, N+1; the additive energy has none). The recovered s is symmetric and does
not factor; the recovery is academic because computing E(U) itself is Ω(N).

## 5. Why this cannot factor: barriers 2, 4, 6, 8

1. **Barrier 2 (symmetry).** E(U) = F(N, s) — symmetric in (p,q) — and the
   pointwise profile r_A(x) is flat on gcd-level sets. No asymmetric content,
   even at the level of individual residues; s alone cannot split N.
2. **Barrier 4 (free-witness aggregation).** Computing E(U) is the O(N) Ramanujan
   sweep (or FFT at O(N log N)); any estimate by sampling suffers the same
   Ω(N) floor (the 1/φ(N) measure of large |c_N| values dominates).
3. **Barrier 6 (circular).** The closed form needs s; the gcd-level grouping
   needs the divisor set {1, p, q, N} = the factorization.
4. **Barrier 8 (known method in disguise).** E(U) = (1/N)Σ|c_N|⁴ is the classical
   Fourier identity for additive energy; the Ramanujan sum is classical; and the
   unit-pair-sum distribution is exactly what the modular-hyperbola /
   Cilleruelo–Garaev–Shparlinski line studies. Nothing here is new mathematics;
   the semiprime closed form is a routine specialization.

## 6. Conclusion

UNIT-ENERGY closes the additive-combinatorics angle with exact statements. The
additive energy of the unit group is the Ramanujan 4th moment, with the closed
semiprime form E(U) = ((p−1)(q−1)/N)(1+(p−1)³)(1+(q−1)³) = F(N, s) — symmetric
in (p,q). Its pointwise unit-pair-sum profile is flat on the gcd-level sets:
the full additive distribution of the units is N-symmetric, factor-blind even
at individual residues. The trace s = p+q is recovered as the unique real root
of a cubic — the cleanest recovery of the family — but s is symmetric and
unfactorable. Computation is Ω(N) (barrier 4), the closed form circular (barrier
6), the identity classical (barrier 8). The additive-energy lens adds no
factoring leverage; it reconfirms that the trace is the ceiling of what a
symmetric free witness — aggregate or pointwise — can carry.

---

**Experiment:** 393 (UNIT-ENERGY). **Script:** /tmp/exp_unitenergy.py.
**Assessment:** v169. **Verdict:** CONFIRMED negative for factoring — E(U) =
(1/N)Σ|c_N|⁴ (Ramanujan 4th moment) with exact closed form ((p−1)(q−1)/N)
(1+(p−1)³)(1+(q−1)³) = F(N, s) alone (verified 10/10 three-way, 14/14 generic);
pointwise profile r_A(x) flat on the 4 gcd-level sets (additive structure of the
units N-symmetric, not even pointwise); recovery cubic in s with s the unique
real root (15/15); Ω(N) aggregation, circular, classical identity —
barriers 2/4/6/8.

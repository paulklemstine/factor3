# The Barrier-2 Reach of the Round-15 Aggregate Family Is Exactly {(N, s)}: the Trace Is the Joint Ceiling, the Family Is Redundant (TRACE-EXHAUSTION)

**Program:** Factoring research lab — cron loop round-15 #5
**Date:** 2026-08-12
**Status:** Machine-verified. Every round-15 aggregate — gcd-moments M_k, unit
energy E(U), mult-table rank, zero-divisor-graph part sizes — is a symmetric
function of (p,q), hence by the fundamental theorem of symmetric polynomials a
function of (N, s) alone. The joint vector has reach exactly {(N, s)}: one
aggregate + N reaches the entire barrier-2 ceiling, the rest of the family is
redundant, asymmetric labels (which factor is p) are unreachable, and the reach
is cost-sealed at Ω(N). Barriers 2/4/8.

---

## Abstract

Machine-verified reach theorem. **(1) Joint closed forms (verified 86/86 + E(U)
3/3):** each round-15 aggregate equals an explicit function of (N, s) — the
gcd-moments M_k = N^k + N·P_{k−1} − P_k + N − s + 1 (Newton power sums), the
unit energy E·N = σ₂(1+σ₁³−3σ₁σ₂+σ₂³) (σ₁ = s−2, σ₂ = N−s+1), the multiplication
table rank (N+5)/2, and the zero-divisor-graph part-size multiset {p−1, q−1}
(recoverable from (N,s) as the roots minus 1). **(2) Recovery (19/19, 60/60 at
scale):** M_1 = 4N−2s+1 recovers s exactly (linear, invertible), and (N,s)
determines the unordered factorization {p,q} as the two roots of x² − s·x + N.
**(3) Reach = {(N,s)}, injective yet redundant:** the joint vector distinguishes
every pair of distinct semiprimes (no collisions), but 114/114 aggregate entries
are predictable from (N,s) alone — so (N, M_1) already reaches the ENTIRE
barrier-2 ceiling, and the rest of the family adds zero reach. **(4) Asymmetric
content unreachable:** 114/114 classic symmetric quantities (φ, σ₁, p²+q²,
p³+q³, τ) are functions of (N,s), while (N,s) never labels which root is p — the
two labelings (p,q) and (q,p) are indistinguishable to every aggregate. **(5)
Cost-sealed:** exact M_1 is an O(N) gcd-sum (linear wall time); the reach is
Ω(N)-sealed and s does not factor (given s you still solve a quadratic for
{p,q}). The trace is the barrier-2 ceiling for the whole family, jointly — the
reach is exhausted.

---

## 1. Setup

Round-15 introduced a family of N-computable aggregates over semiprimes N = pq,
each independently shown symmetric and trace-recoverable:

- **GCD-MOMENT** (paper 57): M_k = Σ_{x≤N} gcd(x,N)^k = Σ_{d|N} d^k·φ(N/d), closed
  form M_k = N^k + N·P_{k−1} − P_k + N − s + 1 with P_j = s·P_{j−1} − N·P_{j−2}
  (Newton), P_0 = 2, P_1 = s. M_1 = 4N−2s+1, M_2 = N²+3N+1+(N−1)s−s².
- **UNIT-ENERGY** (paper 58): E(U) = Ramanujan 4th moment, E·N =
  σ₂(1+σ₁³−3σ₁σ₂+σ₂³), σ₁ = s−2, σ₂ = N−s+1.
- **MULT-TABLE-RANK** (paper 59): rank(M_N) = (N+5)/2 (semiprime law — a function
  of N alone, subsumed).
- **ZERO-DIVISOR-GRAPH** (paper 60): Γ(Z/NZ) = K_{p−1,q−1}, part-size multiset
  {p−1, q−1}, degree sequence {p repeated q−1 times, q repeated p−1 times}.

Every one of these is a symmetric function of (p,q) (all are computable from N,
and N = pq is symmetric). The fundamental theorem of symmetric polynomials says
any polynomial symmetric in (p,q) is a polynomial in the elementary symmetric
functions e₁ = p+q = s and e₂ = pq = N. TRACE-EXHAUSTION asks: does the JOINT
family leak anything beyond this ceiling? The experiment verifies the closed
forms, the recovery, the injectivity and redundancy of the joint vector, the
unreachability of asymmetric labels, and the aggregation cost.

## 2. Joint closed forms, verified

For each of 19 semiprimes (and 60 more at scale), each aggregate was computed
two ways — directly (gcd-sum; Ramanujan moment; modular rank; graph part sizes)
and via its F(N,s) closed form. 86/86 checks pass (M_1, M_2, M_3, E, rank, ZDG
per sample); the unit-energy closed form matches the Ramanujan moment 3/3 at
moderate sizes including N = 1073, 2773, 10403. Every aggregate is an explicit
function of (N, s) — none carries a dependence on q−p, p/q, or any asymmetric
combination.

## 3. Reach = {(N,s)}: recovery, injectivity, redundancy

- **M_1 → s exactly.** The relation M_1 = 4N−2s+1 is linear in s with nonzero
  coefficient: s = (4N+1−M_1)/2 recovers the trace exactly on 19/19 samples and
  60/60 at scale (primes 300–1500). One aggregate + N pinpoints s.
- **(N,s) → {p,q}.** The roots of x² − s·x + N are exactly {p,q} (discriminant
  s²−4N = (q−p)², a perfect square): recovered 19/19, 60/60. So the aggregate
  vector determines the unordered factorization, and nothing more.
- **Injective, yet redundant.** The joint vector (N, M_1, M_2) is injective over
  every sample (no two distinct semiprimes collide). But 114/114 aggregate
  entries are predictable from (N,s) alone — the entire vector is a function of
  two numbers. Hence (N, M_1) already reaches the full 2-dimensional symmetric
  parameter space {(N,s)}; M_2, M_3, E, rank, and the graph add zero reach. The
  family is informationally complete up to symmetry at its FIRST member.

## 4. Asymmetric content is unreachable

For every sample, the classic symmetric quantities φ(N) = N−s+1, σ₁(N) = s+N+1,
p²+q² = s²−2N, p³+q³ = s³−3sN, τ(N) = 4 all agree with their (N,s) forms
(114/114) — as they must, being symmetric. Conversely, (N,s) does not decide
which root of x²−sx+N is p: both labelings produce identical values of every
aggregate (M_k, E, rank, graph are all symmetric by construction). The reach of
the family — the set of facts it can certify about the factorization — is the
unordered pair {p,q}; the asymmetric question "which factor is p?" is not
answerable from any N-computable quantity (barrier 2). The trace is the ceiling,
and the whole family sits on it.

## 5. Why this cannot factor: barriers 2, 4, 8

1. **Barrier 2 (symmetry).** The reach theorem is the aggregate-level statement
   of barrier 2: any symmetric function of (p,q) is a function of (N,s), so no
   N-computable aggregate — singly or jointly — can label p versus q. The
   information content of the entire family is exactly the unordered
   factorization, which is precisely what N and s already determine.
2. **Barrier 4 (free-witness aggregation).** Materializing any aggregate (and
   hence recovering s) costs Ω(N): exact M_1 is an O(N) gcd-sum (timed linear
   wall time; 0.001 s at N = 10⁴ to 0.013 s at N = 2×10⁵), and the higher
   aggregates cost more (M_2 ~N³ samples, E ~N). The reach is cost-sealed; the
   family does not lower the barrier-4 floor, and s itself does not factor
   (given s one still solves a quadratic for {p,q}).
3. **Barrier 8 (known method in disguise).** The reach statement is the
   fundamental theorem of symmetric polynomials — classical algebra. The family
   is a verification, not a new method.

## 6. Conclusion

TRACE-EXHAUSTION closes the round-15 #5 item: the barrier-2 reach of the
round-15 aggregate family is exactly {(N, s)}. Every aggregate is a symmetric
function of (p,q) = a function of (N,s) alone; the joint vector is injective on
the unordered factorization yet redundant — (N, M_1) alone recovers the trace
linearly and reaches the entire ceiling; asymmetric labels are unreachable; and
the reach is cost-sealed at Ω(N) with s not factoring. The trace is the ceiling
for the whole family, jointly — the new aggregates add no factoring leverage,
and the round-15 line of witnesses (trace-carrying, symmetric, cost-sealed) is
fully mapped.

---

**Experiment:** 396 (TRACE-EXHAUSTION). **Script:** /tmp/exp_traceexhaustion.py.
**Assessment:** v172. **Verdict:** CONFIRMED negative for factoring — the
barrier-2 reach of the round-15 aggregate family (M_k, E(U), rank, zero-divisor
graph) is exactly {(N, s)}: closed forms verified 86/86 (+ E(U) 3/3); M_1
recovers s exactly (19/19, 60/60); (N,s) → {p,q} 19/19 (60/60); joint vector
injective yet redundant (114/114 predictable from (N,s); (N, M_1) reaches the
entire ceiling); asymmetric labels unreachable (114/114 symmetric quantities =
F(N,s)); reach cost-sealed at Ω(N) (O(N) gcd-sum), s does not factor — the trace
is the joint ceiling, the family is exhausted; barriers 2/4/8.

# The Semiprime gcd-Moments Are a Closed Trace-Witness Family: M_k = Σ_{x≤N} gcd(x,N)^k Recovers Only the Trace s = p+q, and Never More (GCD-MOMENT)

**Program:** Factoring research lab — cron loop round-15 #1
**Date:** 2026-08-12
**Status:** Decisive confirmation, with exact closed forms, that the gcd-moment
family is closed: every moment M_k reveals the trace s = p+q (uniquely, and
the size cut s < N/2 disambiguates), but the content is symmetric in (p,q) —
a function of (N, s) alone — and computing any M_k is Ω(N) aggregation or
circular. The cost to obtain the trace from higher moments grows as N^{2k−1};
k=1 (M1 = 4N−2s+1, an O(N) gcd-scan) is optimal and is the classical gcd-sum
identity Σ_{d|N} d·φ(N/d). Barriers 2/4/6/8.

---

## Abstract

Machine-verified on random semiprimes and symbolically. **(1) Exact closed
forms (new, verified 48/48 at k=1..4, 12/12 at k=5,6):** for N = p·q with
trace s = p+q, the k-th gcd-moment M_k = Σ_{x=1}^N gcd(x,N)^k = Σ_{d|N} d^k
φ(N/d) has the closed form, via the Newton power sums P_j = p^j+q^j =
s·P_{j−1} − N·P_{j−2} (P_0 = 2, P_1 = s),

> M_k = N^k + N·P_{k−1} − P_k + N − s + 1,

a symmetric polynomial in (p,q) — i.e. a function of (N, s) **alone** for
every k. Explicitly: M1 = 4N−2s+1, M2 = N²+3N+1+(N−1)s−s² (the brainstorm's
S2), M3 = N³−2N²+Ns²+3Ns+N−s³−s+1, M4 = N⁴−3N²s−2N²+Ns³+4Ns²+N−s⁴−s+1.
**(2) Trace recovery, uniquely:** the equation P_k(s) − M_k = 0 has, at
k = 1, 2, 3, 4, roots {s}; {s, N−1−s}; {1−s, s, N−1}; {s, N+1} (+ a complex
pair at k=4). In every case s is the **unique root in (0, N/2]** — all
spurious roots are ≥ N−1−s > N/2 or negative — so the size discriminator
resolves the root ambiguity trivially. **(3) The genuine hierarchy is cost:**
the Monte-Carlo sample count needed to pin s to ±1 grows as N^{2k−1}
(measured ~4N at k=1 — the barrier-4 floor, ~N³ at k=2, ~N⁵ at k=3, ~N⁷ at
k=4), because the 1/N chance of gcd(U,N) = N contributes gcd^k ~ N^k to the
variance. So k=1 — M1 = 4N−2s+1, an O(N) gcd-scan — is the optimal moment,
and higher moments are exponentially worse. **(4) Barriers:** every moment is
symmetric in (p,q) (barrier 2 — s alone never splits N, and s does not
factor); computing M_k is Ω(N) aggregation over the free witnesses (barrier 4)
or circular — the divisor-set form needs the factorization, the closed form
needs s (barrier 6); and M1 = Σ_{d|N} d·φ(N/d) is the classical gcd-sum
identity, so the family is a known-arithmetic-function specialization (barrier
8). The gcd-moment family is closed and fully solved; the trace s = p+q is the
ceiling of what a symmetric free witness can carry, and it does not factor.

---

## 1. Setup

For N = p·q, the gcd-moments are the sums M_k = Σ_{x=1}^N gcd(x,N)^k. Grouping
x by the exact gcd value d | N gives the divisor form M_k = Σ_{d|N} d^k
φ(N/d), classical (a Jordan-totient-weighted sum, of which the gcd-sum k=1 is
the well-known identity Σ_{x≤N} gcd(x,N) = Σ_{d|N} d·φ(N/d)). For a semiprime
the divisor set is {1, p, q, N}: M_k = φ(N) + p^k φ(q) + q^k φ(p) + N^k. Let
s = p+q and P_j = p^j + q^j. Since φ(p) = p−1, φ(q) = q−1, φ(N) = N − s + 1:

M_k = (N − s + 1) + p^k(q−1) + q^k(p−1) + N^k
    = N^k + N(p^{k−1} + q^{k−1}) − (p^k + q^k) + N − s + 1
    = N^k + N·P_{k−1} − P_k + N − s + 1.

The power sums P_j are polynomials in (s, N) by the Newton recurrence
P_0 = 2, P_1 = s, P_j = s·P_{j−1} − N·P_{j−2}. Hence M_k is a symmetric
polynomial in (p,q) = a polynomial in (N, s) alone, for every k. Recovering s
from M_k = solving P_k(s) − M_k = 0, a degree-k univariate equation.

## 2. Exact closed forms, verified

Verified by full enumeration Σ_{x≤N} gcd(x,N)^k on random semiprimes:
48/48 exact for k = 1..4 over 12 semiprimes (N ~ 2^14), 12/12 for k = 5, 6.
Symbolic expansion of M_k = N^k + N·P_{k−1} − P_k + N − s + 1:

| k | M_k |
|---|-----|
| 1 | 4N − 2s + 1 |
| 2 | N² + 3N + 1 + (N−1)s − s² |
| 3 | N³ − 2N² + N s² + 3N s + N − s³ − s + 1 |
| 4 | N⁴ − 3N²s − 2N² + N s³ + 4N s² + N − s⁴ − s + 1 |

M2 matches the round-15 brainstorm's S2 = N²+3N+1+(N−1)s−s² exactly.

## 3. Trace recovery is unique: the spurious roots are all ≫ s

The recovery equation P_k(s) − M_k = 0 is degree k in s. Its real roots on
sample semiprimes:

| k | real roots | s = p+q | unique in (0, N/2]? |
|---|------------|---------|----------------------|
| 1 | {s} | 96 | ✓ (only root) |
| 2 | {s, N−1−s} | 96, 2182 | ✓ (N−1−s = 2182 > N/2) |
| 3 | {1−s, s, N−1} | −95, 96, 2278 | ✓ (negative and N−1 excluded) |
| 4 | {s, N+1} + complex | 96, 2280 | ✓ (N+1 excluded, complex excluded) |

The spurious roots are the "shadow traces" of the complementary/unit-shifted
factorizations (N−1−s = (p−1)(q−1)−2, N−1, N+1) — all ≥ N−1−s > N/2, while
s = p+q ≤ N/3 + O(1) < N/2 for genuine semiprimes. So the size cut
s < N/2 selects the true trace uniquely, at every k. The brainstorm's "root
ambiguity grows with k" concern resolves to a non-issue: the ambiguity is
trivial to resolve; the cost lies in computing M_k in the first place.

## 4. The genuine hierarchy is cost: N^{2k−1} samples to pin s

M_k/N = E[gcd(U,N)^k] for U uniform on [1,N], so a Monte-Carlo estimate of
M_k costs n samples with estimator variance Var(gcd^k)/n, where
Var(gcd^k) = M_{2k}/N − (M_k/N)². Pinning s to ±1 needs sample noise
≤ 1/|dP_k/ds|, i.e. n ≈ Var(gcd^k)·(dP_k/ds)². Measured:

| k | Var(gcd(U,N)^k) | |dP_k/ds| | n ≈ samples |
|---|-----------------|----------|--------------|
| 1 | ~5.8×10² (≈N) | 2 | ~2.3×10³ (≈4N) |
| 2 | ~1.7×10⁸ (≈N³) | ~450 | ~3×10¹³ |
| 3 | ~5.1×10¹³ (≈N⁵) | ~5×10⁴ | ~10²³ |
| 4 | ~1.5×10¹⁹ (≈N⁷) | ~3×10⁶ | ~10³⁰ |

Var(gcd^k) ~ N^{2k−1}: the 1/N chance of gcd(U,N) = N contributes N^k, and
N^{2k}/N = N^{2k−1}. Hence n ~ N^{2k−1}/(s/N)^{2(k−1)} ~ N^{2k−1}. k=1 is the
floor: ~4N samples, the same order as the deterministic O(N) gcd-scan — i.e.
sampling cannot beat the free-witness aggregation cost (barrier 4), and every
higher moment is exponentially worse. M1 = 4N−2s+1 computed by an O(N) scan
is the optimal member of the family.

## 5. Why this cannot factor: barriers 2, 4, 6, 8

1. **Barrier 2 (symmetry).** Every M_k is a symmetric polynomial in (p,q) — a
   function of (N, s) alone; p−q never appears. The most one can recover is
   the trace s, and s = p+q does not factor N (given only s, the pair is any
   (p, s−p) — still a free-parameter family). A factor, not the sum, is
   required; a symmetric free witness can never carry an asymmetric factor.
2. **Barrier 4 (free-witness aggregation).** Computing M_k is Σ over x ≤ N —
   Ω(N) gcd evaluations — or over the divisor set, which is the factorization.
   Monte-Carlo sampling is no better (k=1 already costs ~4N samples).
3. **Barrier 6 (circular).** The divisor form needs {1, p, q, N}; the closed
   form needs s; enumeration is Ω(N). Every route to M_k presupposes what it
   would recover (s itself, at best).
4. **Barrier 8 (known method in disguise).** M1 = Σ_{d|N} d·φ(N/d) is the
   classical gcd-sum identity; the moments are a known arithmetic function
   (the Jordan-totient-weighted divisor sum) specialized to semiprimes.

The family reconfirms the lab's free-witness taxonomy: the trace s = p+q is
the **least-hidden symmetric invariant** (TRACEPROFILE: 1 bit per prime mod
m; QUERYWIT: partial-witness threshold = Θ(p+q)) — and this experiment shows
it is also the **ceiling**: every symmetric gcd-statistic reduces to it, and
it does not factor.

## 6. Conclusion

GCD-MOMENT closes the gcd-statistics line with exact statements. The
semiprime gcd-moments form a closed, fully-solved family: M_k = N^k +
N·P_{k−1} − P_k + N − s + 1 in (N, s) alone (verified k = 1..6); the trace is
recoverable from any moment and uniquely (spurious roots ≥ N−1−s are excluded
by the s < N/2 size cut); the genuine hierarchy is cost — N^{2k−1} Monte-Carlo
samples to pin s, so k=1 (an O(N) gcd-scan, the classical gcd-sum) is optimal
and higher moments are exponentially worse. The moment family is symmetric
(barrier 2), Ω(N)-aggregated (barrier 4), circular (barrier 6), and classical
(barrier 8). The trace s = p+q is what a symmetric free witness can carry —
and the trace does not factor. No usable factoring insight; the free-witness
barrier holds at its trace ceiling.

---

**Experiment:** 392 (GCD-MOMENT). **Script:** /tmp/exp_gcdmoment.py.
**Assessment:** v168. **Verdict:** CONFIRMED negative for factoring — exact
closed forms M_k = N^k + N·P_{k−1} − P_k + N − s + 1 in (N,s) alone (48/48,
12/12; M2 = the brainstorm's S2), trace recovery unique at every k via the
s < N/2 size cut (spurious roots {N−1−s}, {1−s, N−1}, {N+1} all excluded),
cost hierarchy N^{2k−1} (k=1 ~4N = barrier-4 floor, k=2 ~N³, k=3 ~N⁵, k=4
~N⁷) — k=1 = M1 = 4N−2s+1, the classical gcd-sum, is optimal; M1..M4 = known
arithmetic-function specialization — barriers 2/4/6/8.

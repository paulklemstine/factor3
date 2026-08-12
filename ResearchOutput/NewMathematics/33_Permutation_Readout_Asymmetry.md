# The Permutation Readout of Individual Orders, Closed

**Program:** Factoring research lab — permutation-theoretic free-witness assessment
**Date:** 2026-08-11
**Status:** Decisive negative result — a fully asymmetric combinatorial readout
of ord_p(a) and ord_q(a) (strictly more informative than their lcm) still
collapses to barrier 4 because the readout IS the O(N) aggregation

---

## Abstract

The free order-probes of the previous cycle (ORDDIV, PROBESMOOTH, SMOOTHCLASS)
only ever observe `ord_N(a) = lcm(ord_p(a), ord_q(a))` — a symmetric data loss:
knowing the lcm of two orders tells you neither individually. This paper tests
whether the *permutation* `x ↦ a·x mod N` on the additive group Z/NZ escapes that
loss. It does not. The cycle decomposition of this permutation has a precise,
verified structure: for each divisor d of N, the stratum `S_d = {x : gcd(x,N)=d}`
has size φ(N/d) and every element of it lies on an orbit of length `ord_{N/d}(a)`.
For N = p·q this yields cycle lengths `{ord_N(a), ord_p(a), ord_q(a), 1}` on
strata of sizes `{φ(N), q−1, p−1, 1}` — so **ord_p(a) and ord_q(a) are encoded as
distinct cycle lengths**, an asymmetric readout strictly richer than the lcm.
For a primitive root a the recovered unordered pair {p−1, q−1} factors N (machine
verified). But the extraction is sealed: computing the cycle structure of a
permutation on N elements requires visiting all N elements (measured cost ≈ φ(N)),
and one cannot even *start* on a non-unit cycle without already knowing a multiple
of p or q. The readout is a genuine free-witness — non-CRT-multiplicative,
non-numeric, in the spirit of the zero-divisor graph — but its aggregation is the
enumeration itself, and individual order-finding is classically exponential
(paper 9's DFT sample bound). **Even fully separating ord_p(a) from ord_q(a)
does not help.** Barrier 4 (aggregation IS the readout) + barrier 2 (length
multiset is symmetric under (p,q) swap) + barrier 8 (= trial division; exponential
order-finding).

---

## 1. The lcm-blindness loophole

The order probes `gcd(b^t − 1, N)` detect exactly the divisibility `ord_N(a) | t`,
i.e. `lcm(ord_p(a), ord_q(a)) | t`. A lcm is a commutative collapse: from the
sequence of successful probes one recovers at best the smooth part of the lcm
(SMOOTHCLASS), never `ord_p(a)` or `ord_q(a)` individually. If some computable
object of Z/NZ separated the two orders, it would give a handle strictly better
than the entire order-probe family. The permutation `x ↦ a·x mod N` is the
natural candidate: its cycle structure is defined by the additive dynamics, which
decomposes along the gcd strata.

## 2. The exact cycle structure (verified 35/35)

**Theorem (machine-verified).** For a unit a mod N, write `S_d = {x : gcd(x,N)=d}`
for d | N. Multiplication by a preserves each S_d, and every element of S_d lies
on a cycle of length `ord_{N/d}(a)`.

*Proof sketch.* For `x = d·y ∈ S_d` with `gcd(y, N/d) = 1`, the cycle length is
the least k > 0 with `a^k x ≡ x (mod N)`, i.e. `(a^k − 1)·y ≡ 0 (mod N/d)`, which
holds iff `ord_{N/d}(a) | k`. ∎

For N = p·q this specializes to:

| stratum | elements | size | cycle length |
|---------|----------|------|--------------|
| S_1 (units) | gcd(x,N)=1 | φ(N) | ord_N(a) |
| S_p (multiples of p) | gcd(x,N)=p | q−1 | ord_q(a) |
| S_q (multiples of q) | gcd(x,N)=q | p−1 | ord_p(a) |
| S_N | {0} | 1 | 1 |

Total cycle count = `1 + φ(N)/ord_N(a) + (q−1)/ord_q(a) + (p−1)/ord_p(a)` —
exact on all 35 (N, a) pairs tested (N = 15…3127, a = 2,3,5,7).

**Corollary (asymmetric readout is real).** When ord_p(a) ≠ ord_q(a), the two
orders appear as distinct non-trivial cycle lengths in the decomposition —
verified directly in 28/35 cases; the remaining 7 are length-coincidences
(ord_p(a) | ord_q(a) = ord_N(a)) recoverable from multiplicity + stratum-size
data. The multiset of cycle lengths is a function of N alone (symmetric), but it
contains *both* ord_p(a) and ord_q(a), not merely their lcm.

## 3. It is a valid factoring algorithm

For a primitive root a (ord_p(a) = p−1, ord_q(a) = q−1), the recovered unordered
pair {p−1, q−1} determines {p, q} — both CRT assignments of the pair give the
same factor set. Verified: N=143, a=2 → {10,12} → {11,13}; N=221, a=7 →
{12,16} → {13,17}; N=899, a=3 → {28,30} → {29,31}; N=3127, a=2 → {52,58} →
{53,59}. This is a *bona fide* factorization: a permutation-theoretic witness,
outside the CRT-multiplicative classification of paper 16, that recovers the
factor pair.

## 4. Why it collapses: the readout IS the aggregation

Three independent seals:

1. **O(φ(N)) enumeration.** The cycle structure of a permutation on N elements
   cannot be computed without visiting every element (measured scan cost:
   N=3127 → 3018 ≈ φ(N)=3016; N=34571 → 34202). This is *worse* than trial
   division's √N, and strictly worse than Pollard rho's N^{1/4} — the readout
   gains information (individual orders) at the price of the full enumeration.
2. **Circular entry.** One cannot begin a cycle on S_p ∪ S_q without knowing an
   element of it — a multiple of p or q. The moment one has such an element,
   gcd(x,N) factors N directly. The non-unit strata are exactly the prize, and
   finding them is the search.
3. **Exponential order-finding.** Reading ord_p(a) "by itself" (without the
   enumeration) is the classical order-finding problem, which requires Ω(r) DFT
   samples (paper 9). The cycle structure provides no shortcut to the order
   without paying the aggregation.

## 5. Relation to the barrier framework

- **Barrier 4 (aggregation):** the witness's value is sealed behind O(φ(N))
  enumeration. In its sharpest form here, the *readout path itself* is the
  enumeration — there is no free part to skim.
- **Barrier 2 (symmetry):** the cycle-length multiset is a symmetric function of
  N; breaking the (p,q) tie requires an element (the aggregation). The "asymmetry"
  of individual orders is only visible to a reader who already holds a factor.
- **Barrier 8 (known method):** the resulting algorithm = scan-to-first-non-unit
  = trial division; the order extraction = exponential order-finding.
- **Trace lemma consistency:** ord_p(a) is a legitimate order coordinate; the
  lemma says it is unreachable from N in poly(log N) — here confirmed from the
  permutation side.

## 6. Conclusion

The lcm-blindness loophole is **closed**. Even a fully asymmetric combinatorial
readout that separates ord_p(a) from ord_q(a) — strictly more informative than
everything the order-probe family can see — cannot escape barrier 4, because the
object that carries the asymmetry is exactly the O(N)-enumeration of the ring.
This completes the order-family characterization (ORDDIV → PROBESMOOTH →
SMOOTHCLASS → PERMORD): orders are free *as probes*, partial *as smooth-part
constraints*, and sealed *as readouts*. The classical, uniform, hint-free surface
remains exhausted; the quantum exception and hint amplification remain the only
frontiers.

---

**Experiment:** 368 (PERMORD). **Scripts:** /tmp/exp_permord.py.
**Assessment:** v144. **Barrier verdict:** REFUTED — barrier 4 + 2 + 8.

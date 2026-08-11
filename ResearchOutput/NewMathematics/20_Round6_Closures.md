# Round-6 Hypothesis Closures: The Noise-Floor Principle and the Trace-Lemma Frontier

**Program:** Factoring research lab — round-6 subagent batch synthesis
**Date:** 2026-08-11
**Status:** Negative-results synthesis — round-6 attacks closed; the framework's sharpest statement

---

## Abstract

A sixth brainstorm subagent attacked the deepest remaining gaps: the carry
sequence of the factorization (digit-polynomial escape), exact-arithmetic
elliptic point counts (noise-floor immunity), iterated aggregation
(spectral-sequence escape), and a meta-level trace-dichotomy formalization.
Together with the results-analysis subagent's RES-LIFT experiment, the round
produced the framework's sharpest quantitative statement yet: **factor-bearing
samples in any N-computable aggregate occur at density <= c/sqrt(N) — the
free-witness aggregation barrier and the trial-division birthday bound are the
same obstruction.** This paper records the closures and the noise-floor
principle.

---

## 1. The batch at a glance

| # | Hypothesis | Attack | Verdict |
|---|-----------|--------|---------|
| 1 | CARRYTRACE | factorization carry sequence (digit-polynomial) | refuted — linear complexity ~n/2 (random-like) |
| 2 | RINGFROB | exact composite Frobenius point count | refuted — immune to noise-floor but sealed by CRT/order-finding |
| 3 | DIRICHLET | iterated aggregation (spectral sequence) | refuted — E1-collapse: free-witness class closed under Dirichlet convolution |
| 4 | RES-LIFT | 2-adic residue-depth of the TRUNC leak | refuted — depth-k but ambiguous (not a complete witness) |
| 5 | Trace-Dichotomy | barrier 4 + trace lemma == factoring hardness | formalization — open step is trace-lemma exhaustiveness |

---

## 2. CARRYTRACE (experiment 321): the carry sequence is random-like

The carry sequence of the bit-convolution of p, q (a function of N's bits alone)
has linear complexity ~n/2 (0.44-0.52 of length across 16-28 bit semiprimes) —
exactly the value for a random binary sequence. "Bit k of p+q" is not a low-degree
polynomial of N's bits. The low-bit equations triangulate to only p+q mod 2^k
(a residue free-witness); the middle carries are maximally mixed. The
digit-polynomial escape route is sealed by pseudorandomness. (Honest caveat:
proving no low-degree digit-polynomial is a circuit lower bound.)

---

## 3. RINGFROB (experiment 324): exact arithmetic, but still sealed

For E: y^2 = x^3 + Nx + 1, #E(Z/NZ) = (p+1-a_p)(q+1-a_q) with a_p, a_q the
Frobenius traces — verified EXACTLY for N = 77, 143, 221. This is exact
arithmetic, IMMUNE to every noise-floor argument in the framework, and the
expansion contains p+q. But computing it requires the CRT split (the factors) or
O(N^2) enumeration — a free witness (barrier 4). The N-power map 'trace' on
E[l] requires order-finding (q's discrete-log class mod l) — the CRT-split
no-go (barrier 8). Exactness bypasses the noise floor, not barrier 4.

---

## 4. DIRICHLET (experiment 322): the classification is E1-closed

For multiplicative w, D(w)(N) = sum_{d|N} w(d) = prod_{p^e||N}(1 + w(p) + w(p^2)
+ ...) is again multiplicative — and is ITSELF a free witness (D(chi_-4) is a
character divisor-sum; D(id) = sigma, D(id^2) = sigma_2 from SIGK). Every finite
iteration of aggregation over the divisor lattice remains free: the spectral-
sequence escape route collapses at the E1 page. (A recorded imprecision: the
claim 'D(chi_-4) IS the CIRC count' was corrected — they are related but
distinct witnesses.)

---

## 5. RES-LIFT (experiment 323): the truncated leak is depth-k but ambiguous

The TRUNC result is quantified: C(N) mod 2^k is determined by (p,q) mod 2^k
(depth exactly k, with a 2-bit slack from C's 16-divisibility), but
(N mod 2^k, C mod 2^k) does NOT uniquely determine (p,q) mod 2^k (e.g. key
(23,48) admits (p,q) mod 64 in {(11,37), (27,53), (51,13)}). The truncated
free-witness leaks factor residues partially, not as a complete witness. Every
leaked bit is sealed behind O(N) enumeration.

---

## 6. The noise-floor principle (the sharpest statement)

Across SCHINZEL (density ~4/sqrt(N) leak), PRIMEDOM (Povlya-Vinogradov error),
DIVSUM (divisor error), and the birthday bound, the unifying principle: the
p+q coordinate is an O(sqrt N)-amplitude component of any N-computable
aggregate; the character/divisor error that dominates it is O(sqrt N log N) or
O(N^theta). The relative signal density is always <= c/sqrt(N), and sub-sqrt(N)
sampling has zero expected signal. **The aggregation barrier and the
trial-division birthday bound are the same obstruction.**

The Trace-Dichotomy (round-6 subagent): within the class of CRT-respecting
poly-computable functions, every quantity is either factorization-insensitive
(free) or IS factoring (p+q => x^2 - sx + N = 0). The open step: proving the
trace lemma is exhaustive — precisely the frontier the round-7 attacks
stress-test.

---

## 7. Honest verdict

Six rounds, ~32 subagent hypotheses, 324 experiments, 19 papers: the barrier
framework is intact and now quantitatively sharp. The free-witness aggregation
barrier and the birthday bound are the same obstruction; the classification is
closed under iterated aggregation; exact-arithmetic and digit-based escapes fail.
The open frontier is the trace lemma's exhaustiveness — a theorem that would
make barrier 4 equivalent to factoring hardness. No classical poly(log N)
factoring algorithm has emerged.

---

*Related:* `16_FreeWitness_Classification.md`, `18_Schinzel_Circle.md`,
`19_Round5_Closures.md`, `Factoring_Lab_Notebook.md` Parts 68-71.

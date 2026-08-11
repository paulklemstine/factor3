# REPORT: Factorial Number System (Factoradic) Factoring Experiment

**Date:** 2026-08-11   **Experiment:** BBB   **Verdict: REFUTED**

---

## Question

Does the factorial number system — the unique mixed-radix representation $N = \sum c_i
\cdot i!$ with $0 \le c_i \le i$ — offer a new classical factoring approach?

## Answer

**No.** The factoradic representation is *structurally blind* to the factors of a
balanced semiprime.  The only factor-revealing factorial construction is trial division
in disguise (experiment CCC).

## The structural barrier (one-line proof)

For $N = pq$ balanced, the factoradic length $k$ satisfies $k! > N$, hence $k \sim \log N
/ \log \log N$.  But $p \sim \sqrt{N}$.  Therefore $k \ll p$: **every** factoradic digit
has index $i \le k < p$, so $c_i \le i < p$, and $\gcd(c_i, N) = 1$.  The digits live at
a scale far below the smallest prime factor and cannot encode it.

## Hypotheses tested (all negative)

| # | Hypothesis | Result |
|---|-----------|--------|
| H1 | $\gcd(c_i, N) > 1$ for some digit | REFUTED — $c_i < p$, so always 1 |
| H2 | $\gcd(\text{linear combo of digits}, N) > 1$ | REFUTED — no signal |
| H3 | $\gcd(N \bmod i!, N)$ reveals factor | **= trial division** (first hit at $i=p$) |
| H4/H8 | Wilson's theorem $(p-1)! \equiv -1$ via factoradic | REFUTED — index $p-1 \gg k$, unreachable |
| H5 | Permutation order in $S_k$ (Lehmer code) | REFUTED — order $\ll p$, gcd = 1 |
| H6 | $N \bmod i!$ residues | = H3 (trial division) |
| H7 | CRT / ring decomposition | REFUTED — radices $1,2,3,\dots$ not coprime |
| H9 | Digit statistics mod small primes | REFUTED — no correlation with $p,q$ |
| HD | Subset sums of $\{c_i \cdot i!\}$ | REFUTED — exhaustive $2^k$, no factor |

## Scaling

Tested up to 20-digit semiprimes ($k \le 22$).  No construction revealed a factor within
the factoradic range.  The scale mismatch $k \ll p$ grows with $N$.

## Verdict

The factorial number system is a mathematically elegant *representation* (and the Lean
uniqueness proof is clean), but it is **structurally orthogonal to factoring**: it encodes
$N$ at scale $\log N/\log\log N$, far below the factor scale $\sqrt{N}$.  Every
factor-revealing construction either (a) is bounded by $k$ and sees nothing, or (b) must
reach index $\sim p$ and becomes trial division.  **Subsumed under the CCC barrier
(factorial-GCD = trial division).**

**Files:**
- Full report: `~/lean/Catalog/ResearchOutput/Exp_FactorialNS.md`
- Lean source: `~/lean/Catalog/Computation/FactorialNumberSystem/FactorialNumberSystem.lean`

# Experiment BBB: Factorial Number System (Factoradic) Factoring

**Date:** 2026-08-11
**Paradigm:** Combinatorial number systems / mixed-radix representations
**Verdict:** **REFUTED** — structural blindness theorem; the only factor-revealing construction reduces to trial division (experiment CCC).

---

## 1. Mathematical background

The **factorial number system** (factoradic) represents every integer $N$ uniquely as

$$N = c_0 \cdot 0! + c_1 \cdot 1! + c_2 \cdot 2! + \dots + c_{k-1} \cdot (k-1)!$$

with digit bounds $0 \le c_i \le i$ (the `Valid` condition).  The representation is a
**mixed-radix** system with radices $1,2,3,4,\dots$ — the $i$-th digit has radix $i+1$.

The Lean formalization (`FactorialNumberSystem.lean`) proves uniqueness directly:
`value_unique` shows that two valid digit functions with the same value agree on every
digit, using only the digit-bound estimate `value_lt` (a valid length-$k$ value is
$< k!$) and the splitting identities `splitting_div`/`splitting_mod`.

The digits are extracted by the greedy algorithm
$c_i(N) = \lfloor N / i!\rfloor \bmod (i+1)$, and the **factoradic length** $k(N)$ is the
smallest $k$ with $k! > N$.

The factoradic digits of $N$ are the **Lehmer code** of a permutation in $S_k$
(the permutation of rank $N$ in lexicographic order).  This connects the representation
to the symmetric group.

---

## 2. The central structural observation

**Lemma (scale mismatch).** For a balanced semiprime $N = pq$ with $p \approx q \approx
\sqrt{N}$, the factoradic length satisfies

$$k! > N \quad\Longrightarrow\quad k \sim \frac{\log N}{\log\log N} \quad \text{(by Stirling)}.$$

| $N$ size | factoradic length $k$ | $\sqrt{N} \sim p$ | ratio $p/k$ |
|----------|----------------------|-------------------|-------------|
| $10^{10}$ | 14 | $10^5$ | ~7,000 |
| $10^{15}$ | 18 | $10^7.5$ | ~1,700,000 |
| $10^{20}$ | 22 | $10^{10}$ | ~500,000,000 |
| $10^{30}$ | 29 | $10^{15}$ | ~$10^{13}$ |
| $10^{50}$ | 42 | $10^{25}$ | ~$10^{23}$ |

**The factoradic digits live at indices $i \le k \ll p$.**  Every digit position is far
below the smallest prime factor.  This single fact is the root cause of all negative
results below.

**Structural Theorem (factoradic blindness).** *Let $N = pq$ be a balanced semiprime and
$k$ its factoradic length. Then for every digit index $i \le k$ we have $i < p$, hence
$c_i \le i < p$, and therefore $\gcd(c_i, N) = 1$.  No individual factoradic digit shares
a nontrivial factor with $N$.*

The factoradic representation is "blind" to the factors: it is a deterministic encoding
of $N$ at a scale ($\sim \log N/\log\log N$ digits) that does not reach the factor scale
($\sim\sqrt{N}$).

---

## 3. Hypotheses tested

### H1. $\gcd(c_i, N)$ — do any digits share a factor with $N$?

**Prediction:** By the structural theorem, $\gcd(c_i, N) = 1$ for all $i$ (except the
trivial $c_0 = 0$ giving $\gcd(0,N) = N$).

**Result: REFUTED (as predicted).**  Across 20/30/40-bit semiprimes, the only "hits" were
$c_0 = 0$ (always, by the radix-1 digit).  No nonzero digit shared a factor with $N$.

### H2. Linear combinations $\gcd(\sum \alpha_i c_i, N)$

Tested: pairwise sums, weighted sums with weights $i!$, $i+1$, $(-1)^i$, and small primes.
All combinations of the form $\gcd(\sum \alpha_i c_i, N)$.

**Result: REFUTED.** No nontrivial factor in any test (30-bit, 40-bit).

### H3. Factorial-residue GCD — $\gcd(N \bmod i!, N)$

This is the natural "factoradic GCD" construction.  Since the factoradic digits determine
$N \bmod i!$ for each $i$, we ask: does $\gcd(N \bmod i!, N)$ reveal a factor?

**Key identity:** $\gcd(N \bmod m, N) = \gcd(m, N)$ is **false in general**, but for
$m = i!$ and semiprime $N$ we have:
- For $i < p$: $\gcd(i!, N) = 1$ (all prime factors of $i!$ are $< p$).
- For $p \le i < q$: $\gcd(i!, N) = p$.
- For $i \ge q$: $\gcd(i!, N) = N$.

**Result: KNOWN METHOD (= trial division, experiment CCC).**  The first $i \ge 2$ with
nontrivial $\gcd(i!, N)$ is exactly $i = p$.  Finding it requires scanning $i = 2, 3,
\dots, p$, i.e. $O(p) = O(\sqrt{N})$ steps.  This is **trial division in factorial
clothing** — precisely the method already refuted as experiment CCC ("factorial-GCD:
first $n$ with $\gcd(n!, N) > 1$ = trial division").

The factoradic digits $c_i = \lfloor N/i!\rfloor \bmod (i+1)$ are a *refinement* of the
residues $N \bmod i!$, but for $i < p$ this refinement carries no factor information
(residues are already coprime to $N$), and for $i \ge p$ the factoradic representation
has already ended ($k \ll p$).

### H4/H8. Wilson's theorem — $(p-1)! \equiv -1 \pmod p$

Wilson's theorem gives $\gcd((p-1)! + 1, N) = p$ (when $p \nmid W_p$).  Could the
factoradic representation let us compute $(p-1)! \bmod N$ cheaply?

**Result: REFUTED (circular + out of range).**  Wilson's theorem operates at index
$p-1 \approx \sqrt{N}$, but the factoradic representation only has $k \sim
\log N/\log\log N \ll p$ digits.  We cannot even *represent* $(p-1)!$ in the factoradic
system of $N$, let alone compute it without knowing $p$.

### H5. Lehmer-code permutation — does $\operatorname{ord}(\sigma_N)$ reveal a factor?

The factoradic digits of $N$ are the Lehmer code of the permutation $\sigma_N \in S_k$
of rank $N$.  Tested $\gcd(\operatorname{ord}(\sigma_N), N)$.

**Result: REFUTED.**  The order of any element of $S_k$ divides $\operatorname{lcm}(1,
\dots, k) \ll p$ (for our range, orders were 9–42 while $p \sim 10^3$–$10^6$).  Hence
$\gcd(\operatorname{ord}(\sigma_N), N) = 1$ always.  The symmetric group $S_k$ is too
small to "see" the factors.

### H6. $N \bmod i!$ residues (reexamination)

Direct computation confirms: for $i < p$, $\gcd(N \bmod i!, N) = 1$; the first nontrivial
value occurs at $i = p$.  Same conclusion as H3.

### H7. Ring homomorphism / CRT decomposition

A residue number system with *coprime* moduli gives a ring isomorphism (CRT).  The
factoradic radices $1,2,3,\dots$ are **not coprime**, so factoradic is a mixed-radix
*representation*, **not** a ring homomorphism.

**Result: REFUTED.**  Componentwise product of the digit vectors of $p$ and $q$ bears no
relation to the digit vector of $pq$.  Multiplication carries across all positions; there
is no componentwise factorization.

### H9. Digit statistics / distribution

Tested whether factoradic digits of semiprimes are distinguishable from random integers,
or whether $c_i \bmod \ell$ correlates with $p \bmod \ell$ or $q \bmod \ell$.

**Result: REFUTED.**  No correlation between digit patterns mod small primes and the
factors.  The digit distribution is governed by the mixed-radix structure, not by
factor structure.

### H-D. Subset sums of $\{c_i \cdot i!\}$

Exhaustively tested all $2^k$ subset sums $\gcd(\sum_{i \in S} c_i \cdot i!, N)$.

**Result: REFUTED.**  No subset sum revealed a factor (tested on 20-bit semiprime,
$k=10$, all 1024 subsets).

---

## 4. Scaling tests (15–20 digit semiprimes)

| $N$ | digits | $p$ | $q$ | factoradic $k$ | cheap factor? |
|-----|--------|-----|-----|----------------|---------------|
| 430708185189011 | 15 | 19809773 | 21742207 | 18 | No |
| 807639645384858613 | 18 | 983274437 | 821377649 | 20 | No |
| 65010193123260526397 | 20 | 9142366279 | 7110871643 | 22 | No |

No factor revealed by any factorial-residue GCD within the factoradic range.

---

## 5. Honest verdict

### What the factoradic representation IS
- A **unique**, **complete**, **efficient** mixed-radix encoding of integers.
- A bijection $\mathbb{N} \leftrightarrow \{(c_i) : 0 \le c_i \le i\}$.
- The natural language for ranking/unranking permutations (Lehmer codes).
- A clean setting for a direct uniqueness proof (as the Lean file demonstrates).

### What the factoradic representation is NOT (for factoring)
- It is **not** a ring homomorphism (radices share factors), so multiplication does not
  decompose.
- It does **not** reach the factor scale: $k \sim \log N/\log\log N \ll \sqrt{N} \sim p$.
- It does **not** make Wilson's theorem, factorial residues, or permutation structure
  computationally accessible at the factor scale.

### The classification

| Construction | Reduces to | Complexity |
|-------------|-----------|------------|
| $\gcd(c_i, N)$ | trivial ($c_i < p$) | — (always 1) |
| $\gcd(N \bmod i!, N)$, $\gcd(i!, N)$ | **trial division** | $O(\sqrt{N})$ |
| Linear combos of digits | no signal | — |
| Permutation order in $S_k$ | trivial ($\operatorname{ord} < p$) | — |
| Wilson quotient | circular (needs $p$) | — |
| CRT / ring decomposition | impossible (radices not coprime) | — |

### Bottom line

The factorial number system does **not** offer a new classical factoring approach.  The
**structural blindness theorem** — $k \ll p$, so every digit is smaller than the smallest
factor — is a clean, general, and (to my knowledge) precisely-stated barrier.  The only
factor-revealing factorial construction is $\gcd(i!, N)$ at $i = p$, which is trial
division (experiment CCC).  The factoradic angle adds nothing beyond what CCC already
covered; it is a mathematically elegant representation that is structurally orthogonal to
factoring, in the same sense as the Berggren-tree orthogonality result (memory:
slope coordinates $\perp$ norm coordinates).

**This experiment is classified REFUTED and subsumed under the CCC (factorial-GCD = trial
division) barrier.**

---

## 6. Lean connection

The Lean file `FactorialNumberSystem.lean` establishes the *uniqueness* of factoradic
representations via a direct proof (`value_unique`) that avoids surjectivity/cardinality.
The structural blindness theorem proved here is a *separate* arithmetic observation:
the digit bound $c_i \le i$ combined with $k! > N \Rightarrow k \ll p$ implies
$\gcd(c_i, N) = 1$.  This could be formalized as a Lean theorem connecting
`value_lt` (valid value $< k!$) to the statement that no digit of a semiprime's
factoradic representation shares a factor with the semiprime — a "blindness" theorem
worthy of formalization if the catalog aims for completeness on this point.

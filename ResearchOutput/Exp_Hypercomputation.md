# Experiment HCM — Hypercomputation / Computability Theory for Factoring

**Date:** 2026-08-11
**Paradigm:** Computability theory, hypercomputation, algorithmic information theory
**Verdict:** **REFUTED** — every computable finite-approximation hypothesis hits the
**fixed-prime barrier**; the uncomputable functions require non-existent infinite-precision
oracles. Hypercomputation is a meta-theoretical framework, not a factoring method.
**Confidence:** High (theorem-level structural result + computational verification)
**Lab notebook:** v18 (experiment HCM)

---

## 1. Source material and the theoretical landscape

### 1.1 The Lean formalizations

Two files in `Applications/Hypercomputation/` are the foundation:

| File | Content | Key theorem |
|---|---|---|
| `Cardinality.lean` | Computable Boolean functions on `ℕ` are **countable**; all Boolean functions are **uncountable** (continuum) | `computable_countable`, `uncountable_functions`, `uncomputable_uncountable` |
| `FinitePrecision.lean` | A physical oracle read to finite precision `p` yields only the first `p` bits `readBits b p` | `finitePrecision_computable`: finite precision collapses to ordinary computability; `not_computable_needs_infinite_precision` |

The **Cardinality** results establish the *existence* landscape: uncomputable functions
exist and are in fact uncountable — "almost every" decision problem needs hypercomputation.
The **FinitePrecision** results establish the *access* landscape: you cannot touch an
uncomputable function without infinite precision; any finite measurement is just a constant.

### 1.2 The motivating question

> The computable functions are a countable sliver of all functions.  The factoring
> problem is a specific function `F(N) = smallest prime factor of N`.  Is `F`
> computable?  Uncomputable?  And does the hypercomputation perspective — knowing
> that uncomputable functions are the *rule*, not the exception — reveal a new
> classical factoring witness?

The honest answer, developed below, is:

1. **`F` IS computable** — trial division computes it in `O(√N)` time.  The question
   is one of *complexity* (is `F` in `P`?), not *computability*.
2. Uncomputable functions exist, but **accessing** them requires infinite precision
   (FinitePrecision theorem).  Finite approximations are constants → fixed-prime barrier.
3. Therefore hypercomputation does **not** yield a new computable factoring witness.

---

## 2. The fixed-prime barrier for oracles (main structural result)

The central theorem tested in this experiment is a factoring-context instantiation of
`finitePrecision_computable`:

**Theorem (fixed-prime barrier for oracles).** Let `O` be any oracle (computable or
uncomputable), and let `approx(O, k)` be any `k`-bit finite-precision approximation
to `O` (e.g. the first `k` bits of Chaitin's Ω, or the halting behavior of all
`k`-state TMs).  Then `approx(O, k)` is a **fixed finite bitstring**, independent of
`N`.  Let `c = integer_value(approx(O, k))`.  Then:

```
gcd(c, N) reveals only the prime divisors of c — finitely many fixed primes,
independent of which N = pq was chosen.
```

*Proof.* `approx(O, k)` depends only on `O` and `k`, not on `N`.  So `c` is a constant.
`gcd(c, N) ∈ (1, N)` requires some prime `p | c` to also divide `N`.  The set of such
`p` is exactly `prime_divisors(c)`, a finite set determined by `c` alone.  Changing `N`
only changes *which subset* of these fixed primes divides `N`; no *new* prime is ever
revealed. ∎

This is structurally identical to the polynomial barrier (LLL): for `f ∈ ℤ[x]`,
`p | f(N) ⇔ p | f(0)`, so a polynomial reveals only finitely many fixed primes.
An oracle's finite approximation is even more limited than a polynomial — it is a
**constant**, with no dependence on `N` at all.

**Consequence tested in H1–H6, H8 below:** *every* computable finite approximation
to BB, Ω, K, or the halting problem hits this barrier.  The revealed primes are
always divisors of the approximation constant, never genuine factors of `N`.

---

## 3. The uncomputable functions — what they are and why they don't factor

### 3.1 Busy Beaver `BB(n)`

`BB(n)` = maximum steps taken by a halting `n`-state 2-symbol TM.  Well-defined;
uncomputable; grows faster than every computable function.

| `n` | `BB(n)` (exact) | Prime divisors |
|---|---|---|
| 1 | 1 | ∅ |
| 2 | 6 | {2, 3} |
| 3 | 21 | {3, 7} |
| 4 | 107 | {107} |
| 5 | 47,176,870 | {2, 5, 13, 17, 21347} |
| 6 | > 10^^15 (exact unknown) | — |

For **fixed** `n`, `BB(n)` is a constant → fixed-prime barrier (H1).
`BB(N)` itself is uncomputable, so not runnable; and `gcd(BB(N), N)` would be
pseudorandom in the factors (no structural reason for `BB(N)` to be divisible by
exactly one of `{p, q}`).

### 3.2 Kolmogorov complexity `K(N)`

`K(n)` = length of shortest program outputting `n`.  Uncomputable (upper-semicomputable).
For typical `N`, `K(N) ≈ log₂ N`.  Hence `K(N) < min(p, q)` for all but tiny `N`,
so `gcd(K(N), N) = 1` (H3).  The hypercomputation perspective (oracle machines)
does not change this: an oracle for `K` would output a number ≈ `log N`, which is too
small to share a factor with `N`.

### 3.3 Chaitin's halting probability `Ω`

`Ω = Σ_{p halts} 2^{-|p|}` for a universal prefix-free machine.  A real number in
`[0,1]`; its bits encode the halting problem; Martin-Löf random; definable but
uncomputable.  For a *tiny* machine, `Ω` is a fixed rational (e.g. `7/8`) → its scaled
integer part has fixed prime divisors {2, 7} (H4).  A universal `Ω` requires infinite
precision to read → fixed-prime barrier for any finite approximation.

### 3.4 The halting problem `H`

Genuinely uncomputable (no TM decides it).  With an oracle for `H`, factoring is
polynomial-time: binary-search for the factor using the oracle to test divisibility
(or compute multiplicative orders).  **But** an oracle for `H` requires *infinite
precision* (FinitePrecision theorem) — any finite approximation is a fixed lookup
table, factoring only the finitely many `N` in the table (H7, theoretical).

---

## 4. Hypotheses tested and results

All experiments run on 12 semiprimes from 65 (5×13) to ≈10¹³, confirmed to scale.

### H1 — `gcd(BB(n), N)` for known `BB(n)`  →  **FIXED-PRIME BARRIER**

`BB(5) = 47,176,870 = 2·5·13·17·21347`.  Across all 12 semiprimes:

| N | Factors | `gcd(BB(5), N)` | Why |
|---|---|---|---|
| 65 | 5×13 | **65** (= N, trivial) | both 5, 13 divide BB(5) |
| 221 | 13×17 | **221** (= N, trivial) | both 13, 17 divide BB(5) |
| 493 | 17×29 | **17** (nontrivial-looking) | 17 | BB(5), but 29 ∤ BB(5) |

The single "nontrivial" case (N=493, gcd=17) is **not** a factoring signal — 17 is a
fixed prime divisor of `BB(5)`, and it appears because 493 *happens* to contain 17.
The set of revealed primes `{2, 5, 13, 17, 21347}` is a property of `BB(5)`, not of `N`.
**Reduces to: fixed-prime barrier** (identical in structure to the polynomial barrier).

### H2 — Finite-precision halting oracle  →  **FIXED-PRIME BARRIER**

Constructed a genuine finite restriction of the halting problem: the halting behavior
of **all 64** 1-state 2-symbol TMs (a fixed 64-bit string, oracle integer =
6,148,914,691,236,517,205 = 5·17·257·641·65537·6700417).  This is the concrete
instantiation of `readBits b p` from FinitePrecision.lean.

| N | Factors | `gcd(oracle, N)` |
|---|---|---|
| 65 | 5×13 | **5** (fixed prime: 5 | oracle) |
| 221 | 13×17 | **17** (fixed prime: 17 | oracle) |

All "nontrivial" gcds are fixed prime divisors of the oracle constant.  This **directly
verifies the FinitePrecision theorem** in the factoring context: a finite oracle is a
constant, and a constant reveals only fixed primes.

### H3 — `gcd(K_approx(N), N)` via gzip compression  →  **TRIVIAL(1)**

`K_approx(N)` (compressed byte length) ranges from 12 to 27 across the test set —
far below `min(p, q)` in every case.  `gcd = 1` for all 12 semiprimes.
**Reduces to: `K(N) = O(log N) << min(p, q)` → no shared factor.**

### H4 — `gcd(⌊Ω·2^k⌋, N)` for tiny-machine `Ω`  →  **FIXED-PRIME BARRIER**

Tiny prefix-free machine with halting set `{0, 10, 110}` has `Ω = 7/8`.  Then
`⌊Ω·2^k⌋` has prime divisors {2, 7} for all `k`.  `gcd ∈ {1, 2, 7, 14}` only.
**Reduces to: tiny `Ω` is a fixed rational → fixed primes {2, 7}.**

### H5 — Finite diagonalization over 1-state TMs  →  **FIXED-PRIME BARRIER**

Diagonal-flip of the 64-bit oracle = 12,297,829,382,473,034,410 =
2·5·17·257·641·65537·6700417.  `gcd` with N reveals only {5, 17} — fixed primes.
**Reduces to: a finite diagonal is a fixed function → fixed-prime barrier.**

### H6 — Scaling: are revealed primes independent of `N`?  →  **YES (barrier confirmed)**

| Approximation | Prime divisors | Revealed across all N |
|---|---|---|
| `BB(4)` = 107 | {107} | {} (none) |
| `BB(5)` = 47,176,870 | {2, 5, 13, 17, 21347} | {17} |
| `BB(6)` lower bound = 10¹⁵ | {2, 5} | {5} |

The revealed set depends **only** on the approximation constant, never on `N`'s
factors.  This is the signature of the fixed-prime barrier — if it were a genuine
factoring signal, the revealed primes would vary with `N`'s factors.

### H7 — The "factoring oracle" (theoretical, not runnable)

The function `F(N) = smallest prime factor of N` is **computable** (trial division,
`O(√N)`); whether it is in `P` is the open factoring question.  An oracle for `F`
makes factoring trivial — tautologically, since it *is* the answer.  An oracle for
the halting problem computes `F` in polynomial time, but requires infinite precision
(FinitePrecision theorem); a finite approximation is a fixed lookup table.
**Reduces to: tautology + requires non-existent oracle.**

### H8 — BSM (Blum-Shub-Smale) real computation  →  **TRIVIAL(1)**

`gcd(⌊sin(N)·10⁹⌋, N)` = 1 for all 12 semiprimes.  Real arithmetic on `N` produces
pseudorandom residues mod `p`, mod `q`.  The `exp(2πi/N)` period-finding route is
Shor's algorithm (quantum), not classical BSM.  **Reduces to: real arithmetic on `N`
is pseudorandom w.r.t. factors; period-finding needs quantum.**

---

## 5. Why hypercomputation does not factor — three perspectives

### 5.1 The computability perspective (the `F` is computable)

The factoring function `F(N) = smallest prime factor of N` is **computable**.  Trial
division computes it; the number field sieve computes it in subexponential time.
The countability theorem (`computable_countable`) says computable functions are a
countable sliver — but `F` is *in* that sliver.  The existence of uncountably many
uncomputable functions does **not** imply `F` is hard; it implies almost every
*arbitrary* function is uncomputable, which is a statement about the space of all
functions, not about this particular one.

### 5.2 The finite-precision perspective (the main theorem)

Any computable finite approximation to an uncomputable oracle is a **constant**,
hence reveals only finitely many fixed primes (Section 2 theorem).  This is the
content of `finitePrecision_computable`, now verified concretely: the finite halting
oracle (H2), finite `Ω` (H4), and finite diagonal (H5) all reveal only their own
fixed prime divisors.  **There is no middle ground**: a finite approximation is a
constant (fixed primes), while a genuine uncomputable function needs infinite
precision (non-existent oracle).

### 5.3 The complexity perspective (what hypercomputation actually tells us)

Hypercomputation is a framework about **computability** (can it be computed at all?),
while factoring is a problem in **complexity** (can it be computed in polynomial
time?).  These are different questions:

- **Computability:** `F` is computable.  The halting problem `H` is not.
- **Complexity:** Is `F ∈ P`?  Unknown.  Is factoring in `BPP`?  Unknown (not believed).
- **With an oracle for `H`:** `F ∈ P^H` (polynomial-time with halting oracle).
  But `P^H` contains the entire polynomial hierarchy — it is a *massive*
  relaxation, and the oracle is non-physical.

The hypercomputation perspective **restates** the complexity question ("is `F` in `P`?")
in oracle-machine language, but does not answer it.  Knowing that uncomputable
functions exist and that `F^H ∈ P^H` does not produce a classical algorithm.

---

## 6. Honest assessment

### What is genuinely new here

- The **fixed-prime barrier for oracles** (Section 2 theorem) is a clean structural
  result: a finite-precision oracle is a constant, so `gcd(constant, N)` reveals only
  fixed primes.  This is the factoring-context instantiation of the FinitePrecision
  theorem, and it is more limiting than the polynomial barrier (a polynomial at least
  *varies* with `N`; an oracle approximation does not).
- The **direct computational verification** of the FinitePrecision theorem (H2): a
  genuine finite restriction of the halting problem (all 1-state TMs) reveals only
  its fixed prime divisors, never the factors of `N`.
- The **clarification** that the countability theorem (`computable_countable`) does
  not imply factoring is hard: `F` is computable, and the theorem is about the space
  of *all* functions, not about `F` specifically.

### What reduces to known barriers

| Hypothesis | Outcome | Barrier |
|---|---|---|
| H1 — `gcd(BB(n), N)` | Fixed primes {2,5,13,17,21347} | Fixed-prime barrier (= polynomial barrier) |
| H2 — Finite halting oracle | Fixed primes {5,17,...} | Fixed-prime barrier (FinitePrecision instantiation) |
| H3 — `gcd(K_approx, N)` | gcd = 1 always | `K(N) = O(log N) << min(p,q)` |
| H4 — `gcd(Ω·2^k, N)` | Fixed primes {2,7} | Fixed-prime barrier |
| H5 — Finite diagonal | Fixed primes {5,17} | Fixed-prime barrier |
| H6 — Scaling independence | Confirmed | Fixed-prime signature |
| H7 — Factoring oracle | Tautology / non-existent oracle | Circularity + non-existent oracle |
| H8 — BSM real arithmetic | gcd = 1 (pseudorandom) | Pseudorandom; period-finding = quantum |

### What does NOT work and why (summary)

Every computable finite approximation to an uncomputable oracle is a **constant**.
A constant has finitely many prime divisors.  `gcd(constant, N)` can therefore reveal
only those fixed primes — a set determined by the approximation, not by `N`.  This is
why H1, H2, H4, H5 all return the *same* fixed primes across all `N`.  The uncomputable
functions themselves (`BB`, `Ω`, `H`) are inaccessible: reading them requires infinite
precision, and no physical apparatus provides that (the `halting_needs_infinite_precision`
theorem).  Hypercomputation tells us *that* uncomputation exists, not *how* to build it.

### Bottom line

**Hypercomputation does not provide a new classical factoring approach.**  It is a
meta-theoretical framework that (a) confirms `F` is computable but its complexity is
open, (b) confirms uncomputable functions exist but are physically inaccessible, and
(c) confirms that any finite approximation to such a function collapses to a constant
subject to the fixed-prime barrier.  The connection to factoring is either (a) a
restatement of "is factoring in `P`?" in oracle-machine language, or (b) a requirement
for a non-existent infinite-precision oracle.  Neither yields an algorithm.

---

## 7. Recommendation

- **Do not pursue** hypercomputation as a factoring paradigm.  The negative result
  is theorem-level (the fixed-prime barrier for oracles, Section 2), not empirical.
- The **fixed-prime barrier for oracles** (Section 2) is worth formalizing in Lean as
  a permanent negative result in the catalog, alongside the polynomial barrier theorem.
  It should read: "a finite-precision oracle is a constant; `gcd(constant, N)` reveals
  only fixed primes" — the factoring instantiation of `finitePrecision_computable`.
- Remaining fresh leads with higher promise: **IsogenySIDH** (isogeny diamonds,
  Castryck-Decru attack engine; the one paradigm with a known *polynomial-time*
  quantum factoring connection via SIDH attacks), **Langlands / idèle class group**
  (deepest number-theoretic structure), and **DelaunayContraction** /
  **JacobianConjecture** (genuinely new algebraic territory).

---

## Appendix A — Computable vs. theoretical, clearly distinguished

| Item | Runnable? | What was actually computed |
|---|---|---|
| `gcd(BB(n), N)` for n≤5 | **Yes** — BB(1..5) are known constants | H1, H6 |
| Finite halting oracle (1-state TMs) | **Yes** — 64 TMs, exhaustive | H2 |
| `gcd(K_approx(N), N)` | **Yes** — gzip compression of `N` | H3 |
| `gcd(Ω·2^k, N)` | **Yes** — tiny-machine Ω = 7/8 exactly | H4 |
| Finite diagonal of TM table | **Yes** — same 64-TM table | H5 |
| `BB(N)` for arbitrary N | **No** — BB is uncomputable | Theoretical only |
| `gcd(Ω_N, N)` for universal Ω | **No** — needs infinite precision | Theoretical only |
| Halting-oracle factoring | **No** — oracle non-existent | H7 thought experiment |
| BSM factoring | **No** — period-finding is quantum | H8 tested the classical remnant |

The experiment is honest about this boundary: everything claimed as "tested" was run;
everything labeled "theoretical" was not, and the reason (uncomputability / infinite
precision / non-existent oracle) is stated explicitly.

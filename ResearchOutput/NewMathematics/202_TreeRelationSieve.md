# Paper 202 — TREE-SIEVE: The Combining Proposal Is a Random-GCD Lottery

**Verdict name: INVALID-AS-STATED / CONSISTENT-LOTTERY (smoothness boost real but unusable without N-coupling).**
Round-72 #2 · exp 556 · assessment v309 · script `exp556_tree_sieve.py` (+ JSON/logs) · seed 20260826.

## 1. Theory (Part A): the proposal never touches N

The identity Π(mᵢ−nᵢ)(mᵢ+nᵢ) = Y² lives entirely in ℤ; no step reduces mod N, so
the required condition N | Πmᵢ − Y is supplied by nothing. The only square root of
Y² mod N constructible without factoring is Y itself (gcd = N, trivial). For any
fixed pool the candidate pairs are INDEPENDENT of N ⟹ per-ticket success is generic
gcd luck O(N^{−1/2}). Any corrected variant forcing u ≡ v (mod N) collapses to
Dixon/QS proper (barrier 8); coupling tree values into real congruences needs either
a zero-density x² mod N ∈ tree-values hit or a modular-sqrt oracle (= factoring).
Verified numerically: all 40 GF(2) dependency subsets satisfy Πaᵢ=Y² exactly.

## 2. Smoothness: real boost, far off the naive prediction

50k window values (steered walker; BFS starves — reaches depth 10 / 27-bit max in
50k nodes, zero in-window values): B=1000-smooth rates tree 3.648% vs random 0.499%
vs x²−N′ 0.514% → **T/R = 7.31 [6.86, 7.78]**, T/X = 7.10 — the product structure
(m−n)(m+n) smooths, but ~6× BELOW the naive two-independent-factor ≈44× prediction;
balance dose-response flat (walker funnels to the Pell attractor).

## 3. End-to-end: indistinguishable from the lottery

300 fresh 24-bit semiprimes × 40 verified-square tickets: tree gcd splits 8/12000 =
6.67e-4 [3.4e-4, 1.3e-3] vs random-gcd baseline 4/12000 = 3.3e-4 vs heuristic
1/p+1/q = 6.55e-4 → **CONSISTENT-LOTTERY**. Relations-needed mean 120 < FB dim 168
explained by rank-153 parity space (some FB primes never occur to odd power).

Ledger: trial-division early-exit bug caught vs exhaustive SPF sieve (24.4%→0.5%
undercount), exponent-parity |= vs ^= caught by exact-square assertion, value-level
node collisions documented (multiple nodes share a-values via multiple factor pairs).
Barriers: 8 unchanged — not QS-in-disguise; a lottery whose only success channel is
generic gcd luck. Now 550 experiments (max id). Assessment v309.

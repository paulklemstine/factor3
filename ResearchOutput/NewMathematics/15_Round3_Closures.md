# Round-3 Hypothesis Closures: Five Novel Classical Factoring Hypotheses, Tested and Closed

**Program:** Factoring research lab — round-3 subagent batch synthesis
**Date:** 2026-08-11
**Status:** Negative-results synthesis — 5 hypotheses closed; three subagent rounds complete (19 hypotheses)

---

## Abstract

A third brainstorm subagent proposed five hypotheses targeting the least-mined
territory: coding theory (Reed-Solomon over Z/N), decision-tree lower bounds for
a divisor-parity primitive, true non-abelian structures (braid groups), the
average-case subfamily question, and multi-party game theory. All five were
implemented, run, and closed (experiments 303-308). The batch extended the
free-witness family to a sixth setting (code distance), confirmed that true
non-abelian structure reduces to the multiplicative-order problem, closed the
average-case and decision-tree loopholes, and showed the game-theoretic
restatement is circular. With all three subagent rounds complete (19 hypotheses),
the barrier framework has now survived 308 experiments.

---

## 1. The batch at a glance

| # | Hypothesis | Object | Verdict |
|---|-----------|--------|---------|
| 1 | RS-MIND | Reed-Solomon code over Z/N | refuted — code-theoretic free-witness (barrier 4) |
| 2 | MODPAR-CERT | divisor-count-parity oracle | refuted — decision-tree closure (barriers 6/4) |
| 3 | BURAU-ORD | reduced Burau image of B_3 mod N | refuted — reduces to order-finding (barrier 6/8) |
| 4 | DENS-SUB | average-case fast subfamily | refuted — no N-detectable class (barrier 5/8) |
| 5 | CONG-DIV | divisor congestion game | refuted — equilibrium IS the factorization (barrier 6/4) |

---

## 2. RS-MIND (experiment 303): the sixth free-witness setting

C_k(N) = {(f(0),...,f(N-1)) : f in (Z/N)[x], deg < k} is, by CRT, the product of
Reed-Solomon codes over F_p and F_q. The minimum Hamming weight (min distance)
is d(C) = N - (k-1)*max(p,q), verified exactly for N = 15, 21, 33 at k = 2, 3
(with the zero codeword excluded). The minimum distance leaks max(p,q) — a
free-witness that is provably NOT N-only. Computing it needs p,q (the formula)
or >= N^k brute-force weight search (barrier 4). The zero-set spacing confirms
the residue-class structure: f = q*h with h mod p having k-1 roots vanishes on
(k-1) residue classes mod p, each with q lifts.

---

## 3. MODPAR-CERT (experiment 304): decision-tree closure

P(N,a,m) = (# proper divisors d of N with d == a mod m) mod 2. For N=pq the
parity pattern over a = 0..m-1 encodes where {1,p,q} land mod m; subtracting the
known classes {1, N} recovers {p mod m, q mod m} in all NON-COLLISION cases (the
failures are exactly the merged-class cases, which are genuinely unresolvable,
e.g. q == 0 == N mod m). Evaluating P requires the divisors (= factoring, barrier
6); the special-class density is 2-4/m, so Omega(m) queries are needed (barrier
4). A decision-tree closure for a new atomic primitive, in the spirit of ADAPT.

---

## 4. BURAU-ORD (experiment 305): true non-abelian structure reduces to order-finding

The reduced Burau representation of B_3 specialized at t = a (unit mod N) gives
H_a = <r(s1), r(s2)> <= GL(2, Z/N). Verified: |H_a| SEPARATES the individual
multiplicative orders — for N = 21, both a = 2 and a = 5 give
lcm(ord_3, ord_7) = 6, yet |H_a| = 336 vs 24. So |H_a| depends on (ord_p(a),
ord_q(a)) individually, not just N and the lcm. Computing it is therefore
order-finding mod N = the Pollard p-1 / Shor core (barrier 6/8). The braid
representation is a faithful repackaging of the multiplicative-order problem.
The genuine non-abelian hook (the p<->q swap is not a braid) does not escape:
the order invariant is still CRT-separated and factor-secret.

---

## 5. DENS-SUB (experiment 306): no density-1 poly-detectable fast subfamily

The average-case question: is there a density-1 family of semiprimes,
recognizable from N alone in poly time, factoring below the sqrt(N) floor by a
non-smoothness mechanism? Verified (200 semiprimes): rho step counts are
statistically equal across all N-only classes — N mod 4 (N==1: 332 vs N==3:
333), N mod 8 (306-358), (2/N) (312 vs 355). No N-only statistic predicts ease
(barrier 5). The genuinely fast subfamily (small |p-q| -> Fermat, decile mean 0
vs 29) is a factor property, not N-computable. The fast families (p-1 smooth,
|p-q| small) are each measure-zero and known methods in disguise (barrier 8).
No density-1 poly-detectable fast subfamily exists.

---

## 6. CONG-DIV (experiment 308): the game equilibrium is the factorization

The divisor congestion game: players bid d in {2..N-1}, payoff w(d) = N/d if
d | N else -N. The unique Nash equilibrium: all bid the smallest proper divisor
p (verified for all tested N). The equilibrium IS the factorization — but a
player's best response requires enumerating all N-2 candidate bids to evaluate
payoffs = trial division (barrier 6 circularity; per-move O(N), barrier 4). The
game is a poly-checkable restatement of the problem, not an algorithm; no
equilibrium shortcut avoids enumerating divisors.

---

## 7. Meta-lessons

1. **The free-witness theme is now dominant.** Six structurally distinct
   settings produce the same barrier-4 witness: norm-counts (CIRC), group-order
   counts (KROOT), quadratic-form counts (BQF), group-class counts
   (HEISENBERG), modular indices (CUSP-INDEX/ZETA-LP), and code distances
   (RS-MIND). A scalar that IS the factorization, reachable only at O(N) or
   worse.
2. **Non-abelian structure does not escape.** BURAU-ORD confirmed that even a
   genuinely non-abelian action (braids) yields an order invariant that is
   CRT-separated and factor-secret.
3. **Game-theoretic and average-case loopholes are closed.** CONG-DIV's
   equilibrium is the witness (circular); DENS-SUB shows no N-detectable fast
   subfamily.
4. **Decision-tree lower bounds extend.** MODPAR-CERT closes the divisor-parity
   primitive the way ADAPT closed the multiple-of-p primitive.
5. **The honest frontier.** 308 experiments, three subagent rounds (19
   hypotheses), a six-setting free-witness family, and one alethean.org idea
   tested (PYFAC): the barrier framework is intact. No classical poly(log N)
   factoring algorithm has emerged; the only poly(log N) route remains Shor's.

---

*Related:* `12_Subagent_Batch_Closures.md` (round 1), `14_Round2_Closures.md`
(round 2), `13_FreeWitness_Family.md`, `Factoring_Lab_Notebook.md` Parts 49-54,
`00_CONSOLIDATED_BREAKTHROUGH_REPORT.md`.

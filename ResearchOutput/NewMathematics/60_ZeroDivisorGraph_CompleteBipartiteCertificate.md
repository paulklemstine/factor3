# The Zero-Divisor Graph of Z/pq is Exactly K_{p−1,q−1}: a Complete-Bipartite Certificate Whose Bipartition Is the Factorization (ZERO-DIVISOR-GRAPH)

**Program:** Factoring research lab — cron loop round-15 #4
**Date:** 2026-08-12
**Status:** Machine-verified exact structure. Γ(Z/NZ) — vertices the nonzero
zero-divisors of Z/NZ, edge x~y iff xy ≡ 0 mod N — is exactly the complete
bipartite graph K_{p−1,q−1} for every semiprime N = pq: the parts are the q−1
multiples of p and the p−1 multiples of q, every cross pair multiplies to 0 and
no within-part pair does. The bipartition IS the factorization, and
reconstructing it from N is an Ω(N) gcd-scan whose first hit is the smallest
prime factor. Barriers 2/4/8.

---

## Abstract

Machine-verified exact structure. **(1) The graph (new, verified):** for a
semiprime N = pq, the zero-divisor graph Γ(Z/NZ) (vertex set = {x ∈ {1,…,N−1} :
gcd(x,N) > 1}, edge x~y iff x·y ≡ 0 mod N) is exactly the complete bipartite
graph K_{p−1,q−1}: |V| = p+q−2, |E| = (p−1)(q−1), the bipartition is the q−1
multiples of p (residues with x ≡ 0 mod p, gcd = p) on one side and the p−1
multiples of q on the other, every cross pair is an edge, and no within-part pair
is. Verified in full on 10/10 semiprimes (15, 21, 35, 55, 77, 91, 221, 341, 703,
899). **(2) The degree identity (new, verified):** for every zero-divisor x of a
squarefree N, graph-degree(x) = gcd(x,N) − 1 (62/62 verified) — so the graph's
degree sequence over the zero-divisors is the multiset {p, …, p, q, …, q} (p
repeated q−1 times, q repeated p−1 times) = the two factors written twice.
**(3) The general-N classification (verified):** with a proper bipartiteness
test, Γ(Z/n) is complete bipartite exactly for products of two primes — the
semiprime case (including even 2p, where it is the star K_{p−1,1}) — with the
small prime-power exceptions n = 8 (K_{1,2}) and n = 9 (K_2); for prime squares
n = p² the graph is the complete graph K_{p−1}; for p³, p⁴, and products of ≥ 3
primes it is neither complete nor bipartite. This matches the classical
Anderson–Livingston classification of zero-divisor graphs. **(4) Why this cannot
factor:** the bipartition is exactly the factorization — knowing which vertices
lie in which part is knowing which residues are ≡ 0 mod p versus ≡ 0 mod q.
Reconstructing the graph from N requires finding the zero-divisors, an Ω(N)
gcd-scan, and that scan's first hit is the smallest prime factor: the
reconstruction is trial division in disguise. Everything about the graph is
N-computable hence symmetric in (p,q) — swapping p and q merely swaps the two
parts of K_{p−1,q−1}. Barriers 2/4/8.

---

## 1. Setup

For a commutative ring R, the **zero-divisor graph** Γ(R) (Beck 1988;
Anderson–Livingston, *J. Algebra* 217 (1999)) has vertices the nonzero
zero-divisors of R and an edge between distinct x, y iff xy = 0. For R = Z/NZ a
residue x (with 1 ≤ x ≤ N−1) is a zero-divisor iff gcd(x, N) > 1. By the CRT,
Z/pq ≅ Z/p × Z/q, so an element is the pair (x mod p, x mod q); it is a
zero-divisor iff at least one coordinate is 0, and the two classes are the
p-multiples {p, 2p, …, (q−1)p} (size q−1, first coordinate 0) and the
q-multiples {q, 2q, …, (p−1)q} (size p−1, second coordinate 0).

## 2. The exact structure, verified

For each of 10 semiprimes the graph was built exhaustively (vertex set by a gcd
scan, edges by pairwise products mod N) and every structural datum checked:

| N | p·q | |V| = p+q−2 | |E| = (p−1)(q−1) | parts (q−1, p−1) | cross-all | within-none | degdist {p−1:q−1, q−1:p−1} |
|---|-----|-----------|-----------------|-------------------|----------|-------------|-------------------------------|
| 15 | 3·5 | 6 ✓ | 8 ✓ | 4,2 ✓ | ✓ | ✓ | {2:4, 4:2} ✓ |
| 21 | 3·7 | 8 ✓ | 12 ✓ | 6,2 ✓ | ✓ | ✓ | {2:6, 6:2} ✓ |
| 35 | 5·7 | 10 ✓ | 24 ✓ | 6,4 ✓ | ✓ | ✓ | {4:6, 6:4} ✓ |
| 55 | 5·11 | 14 ✓ | 40 ✓ | 10,4 ✓ | ✓ | ✓ | {4:10, 10:4} ✓ |
| 77 | 7·11 | 16 ✓ | 60 ✓ | 10,6 ✓ | ✓ | ✓ | {6:10, 10:6} ✓ |
| 91 | 7·13 | 18 ✓ | 72 ✓ | 12,6 ✓ | ✓ | ✓ | {6:12, 12:6} ✓ |
| 221 | 13·17 | 28 ✓ | 192 ✓ | 16,12 ✓ | ✓ | ✓ | {12:16, 16:12} ✓ |
| 341 | 11·31 | 40 ✓ | 300 ✓ | 30,10 ✓ | ✓ | ✓ | {10:30, 30:10} ✓ |
| 703 | 19·37 | 54 ✓ | 648 ✓ | 36,18 ✓ | ✓ | ✓ | {18:36, 36:18} ✓ |
| 899 | 29·31 | 58 ✓ | 840 ✓ | 30,28 ✓ | ✓ | ✓ | {28:30, 30:28} ✓ |

**Exact, 10/10.** "cross-all" = every pair with one vertex in each part is an
edge (product ≡ 0 mod N); "within-none" = no edge whose two endpoints lie in the
same part. Together they are exactly the definition of a complete bipartite
graph, so Γ(Z/pq) ≅ K_{p−1,q−1} with the parts identified.

## 3. The degree identity: degree(x) = gcd(x,N) − 1

For a zero-divisor x of a squarefree N, its graph degree is #{zero-divisors
y ≠ x : N | xy}. Over *all* residues y ∈ {0,…,N−1}, the count of solutions to
xy ≡ 0 mod N is gcd(x, N) (the solutions are the multiples of N/gcd(x,N)). The
excluded elements are y = 0 and y = x; for squarefree N no zero-divisor x ≠ 0
satisfies N | x², so both are excluded and the graph degree is exactly
gcd(x,N) − 1. Verified on 62/62 zero-divisors across 15, 35, 91, 221.

**Consequence.** The degree sequence of Γ(Z/pq) is the multiset {gcd(x,N) − 1 :
x a zero-divisor} = {p−1, …, p−1, q−1, …, q−1} — the two factors written twice
(p−1 occurs q−1 times, q−1 occurs p−1 times). The whole degree sequence is
computable from N in O(N) gcd operations, and it directly lists the factors.
This is the free-witness aggregation face of the graph: the object carries
exactly the factorization, and its cost to materialize is Ω(N).

## 4. The general-N classification

Using a proper bipartiteness test (a 2-coloring with no monochromatic edge, plus
completeness of the cross set):

| n | structure | Γ(Z/n) |
|---|-----------|--------|
| p² (n=4, 9, 25, 49) | complete graph K_{p−1} (all pairs of p-multiples multiply to 0) | complete; bipartite only for the tiny K_2 (n=9) |
| 2p (n=6, 10, …) | star K_{p−1,1}: {2,4,…} ∪ {p}, all cross edges | complete bipartite |
| pq, p<q odd distinct (15, 21, …) | K_{p−1,q−1} | complete bipartite |
| p³, p⁴ (8, 27, 16, 125) | neither complete nor bipartite | neither |
| pqr, p²q, … (30, 42, 45, 63, 70, 105, 210, 231, 385) | neither complete nor bipartite | neither |

Small exceptions: n=8 gives K_{1,2} and n=9 gives K_2 (complete, hence also
bipartite) — consistent with the classical classification, where Γ(Z/n) is
complete bipartite precisely for products of two primes (up to these trivial
sizes). The semiprime case — the factoring-relevant class — is exactly the clean
complete-bipartite case.

## 5. Why this cannot factor: barriers 2, 4, 8

1. **Barrier 2 (symmetry).** The graph, its isomorphism class, its degree
   sequence, its invariants (clique number max(p,q)−1, independence number
   min(p,q)−1, diameter 2, chromatic number 2) are all N-computable and hence
   symmetric in (p,q): swapping p and q merely swaps the two parts of
   K_{p−1,q−1}. The asymmetric information — *which* residues are ≡ 0 mod p
   versus ≡ 0 mod q — is exactly the bipartition, and that is the factorization,
   not a quantity computable from N without it.
2. **Barrier 4 (free-witness aggregation).** Finding any zero-divisor requires
   the gcd scan; the first hit is the smallest prime factor, at cost = that
   factor (trial division at its cheapest: 19 gcds for 703, 29 for 899, 53 for
   3127). Materializing the full graph or degree sequence is O(N) gcd
   operations — the Ω(N) aggregation floor, not a shortcut.
3. **Barrier 8 (known method in disguise).** The graph is a classical object of
   commutative algebra — the Anderson–Livingston classification of zero-divisor
   graphs, complete-bipartite for products of two primes, is standard. And the
   reconstruction is trial division in disguise: the O(N) gcd-scan that builds
   the vertex set is exactly the naive factoring scan.

## 6. Conclusion

ZERO-DIVISOR-GRAPH confirms the round-15 brainstorm's claim exactly: for every
semiprime N = pq, Γ(Z/NZ) = K_{p−1,q−1}, with the parts being the p-multiples
and q-multiples — a complete, machine-verified description whose bipartition is
the factorization itself. The degree identity degree(x) = gcd(x,N) − 1 turns the
whole degree sequence into the factors written twice, computable only at Ω(N)
aggregation cost whose first hit already factors. The structure is symmetric in
(p,q) (barrier 2), Ω(N)-sealed (barrier 4), and classical (barrier 8). The
zero-divisor graph adds no factoring leverage: like the other free-witness
catalog entries, it is a complete description of an N-built object whose
asymmetric content coincides with the answer.

---

**Experiment:** 395 (ZERO-DIVISOR-GRAPH). **Script:** /tmp/exp_zerodivisorgraph.py.
**Assessment:** v171. **Verdict:** CONFIRMED exact structure, negative for
factoring — Γ(Z/NZ) = K_{p−1,q−1} exactly (10/10 semiprimes: |V| = p+q−2, |E| =
(p−1)(q−1), bipartition = {p-multiples} ∪ {q-multiples}, all cross edges, no
within-part edges, degdist {p−1:q−1, q−1:p−1}); degree(x) = gcd(x,N) − 1
(62/62, squarefree N) — degree sequence = the factors twice; classification
complete-bipartite exactly for two-prime products (stars for 2p, exceptions 8, 9),
complete K_{p−1} for p², neither for p³/p⁴/multi-prime — matches
Anderson–Livingston; bipartition IS the factorization, reconstruction = Ω(N)
gcd-scan whose first hit is the smallest factor — barriers 2/4/8.

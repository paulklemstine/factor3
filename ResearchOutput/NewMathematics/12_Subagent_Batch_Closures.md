# Eight Novel Classical Factoring Hypotheses, Tested and Closed

**Program:** Factoring research lab — subagent batch synthesis
**Date:** 2026-08-11
**Status:** Negative-results synthesis — 8 novel hypotheses, all closed, all consistent with the barrier framework

---

## Abstract

A brainstorming subagent proposed seven ranked novel classical factoring
hypotheses targeting specific gaps in the eight-barrier framework, plus one
combination-loophole test. All eight were implemented, run, and closed
(experiments 285-292). Each is a genuinely new mathematical object or argument
not present in the prior 284 experiments; each collapses to one of the known
barriers, but the collapses themselves are informative: they convert the
barriers into precise, sometimes geometric, form. This paper records the batch:
the hypotheses, their mechanisms, their verdicts, and the meta-lessons for the
barrier framework.

---

## 1. The batch at a glance

| # | Hypothesis | Novel object / attack | Barrier | Verdict |
|---|-----------|----------------------|---------|---------|
| PAIR | combinations of N-only invariants | closure of the combination loophole | 5 | refuted (permutation null) |
| BDPC | carryless-convolution blind deconvolution | bit-polynomial recovery, C(2)=N | 4/6 | refuted (state space Θ(N)) |
| FOU | Ramanujan-sum / factor-indicator DFT | spike structure of ĝ(t) = -c_N(t) | 6 | refuted (spike = gcd) |
| BPPF | F₂[x] bit-polynomial factorization | last digit-coordinate object | 5 | refuted (within null) |
| HCOM | hidden CRT lattices of S = {(x,y): x²≡y²} | geometric form of circularity | 6 | refuted (escape = 0) |
| SEMI | numerical semigroup ⟨p,q⟩ Frobenius fingerprint | NON-orthogonal coordinate | 6 | refuted (F = φ(N)-1) |
| NSPLIT | biquadratic reciprocity in ℤ[i] | symmetry breaking in higher reciprocity | 2 | refuted (S₂ + conj) |
| ADAPT | adaptive-query lower bound | closure of the adaptivity loophole | 4 | confirmed (slope 0.99) |

---

## 2. The two "loophole closures" (PAIR, ADAPT)

**PAIR (experiment 285).** The near-equal-N test validated barrier 5 per
invariant, leaving open whether TWO N-only invariants could jointly reveal
factors. Tested 72 semiprimes × 12 invariants × 66 pairs × 8 combining
functions. Raw |corr| reached 0.87 but is the within-band N-confound
(corr(p,N) ≈ 0.8 since p ≈ √N varies with N); after control corr(I,p) ≈ corr(I,N).
A permutation null (300 shuffles) places the observed max residual |corr| = 0.30
at the 82nd percentile (95th = 0.371) — within chance. **Combinations of
N-only invariants are N-only**, closing the combination loophole.

**ADAPT (experiment 292).** The atomic primitive under barriers 4 and the
CRT-split no-go: find x with p | x by adaptive queries. Multiples of p form an
arithmetic progression of density 1/p ≈ 1/√N in ℤ/Nℤ; every failure answers
"gcd = 1" and gives no directional information. Measured queries-to-factor for
uniform, sequential, gcd-peel, and powers (Pollard p−1) strategies on 14-34 bit
semiprimes: the first three sit at log-log slope 0.99 vs √N (the N^{1/2} line);
the powers strategy's 0.89 is smoothness of p−1 (the known p−1 method), not
adaptivity. **No adaptive strategy beats √N** — the information-theoretic
sibling of the DFT sample bound (paper 09) and CRT-split birthday bound
(paper 11), now confirmed by measurement.

---

## 3. The three "coordinate-system" attacks (BDPC, BPPF, SEMI)

**BDPC (experiment 286).** Let p(x), q(x) ∈ ℤ[x] be the 0/1 bit-polynomials of
p, q and C(x) = p(x)·q(x) their carryless convolution. Verified: C(2) = N, and
(p,q) → C is injective up to swap (only divisor pairs have C(2) = N). So
factoring ⟺ recovering C from the single value N — a bilinear inverse problem
with a provably small hidden variable (the carry sequence, O(log N) integers).
The decisive experiment: the forward de-carrying DP (choose p_k, q_k ∈ {0,1},
track carry via c_k + carry = N_k + 2·carry') has state space = 2^(bits−1) =
**Θ(N)** (measured 8→128, 18→131072). The carry constraint prunes nothing: the
middle convolution coefficients couple the ENTIRE prefix, so no state
aggregation exists. **The unique solution is real but its search is Θ(N)** —
worse than the √N line. Barriers 4/6 hold even in this novel coordinate system.

**BPPF (experiment 288).** N(x) = the binary string of N over F₂[x], factored
by Berlekamp. Six factorization statistics tested on 48 near-equal-N semiprimes
(14-26 bits); residual correlations with p, q after regressing out N all ≤ 0.30,
and the max sits at the 82nd percentile of the permutation null. **The F₂
bit-polynomial factorization type is N-only** — the last digit-coordinate
object carries no factor signal, consistent with BDPC's finding that carry noise
couples the full prefix.

**SEMI (experiment 290).** The numerical semigroup ⟨p,q⟩ = {ap + bq} is the
FIRST object in the whole program whose natural coordinate is genuinely
non-orthogonal to factoring: its Frobenius number F = N − p − q is one lift
from the target p+q. Verified: |G| = φ(N)/2, max(G) = F = N − p − q = φ(N) − 1,
and from F alone p, q are recovered by solving x² − (N−F)x + N = 0. **The
semigroup's defining invariants are φ(N)-equivalent, and computing φ(N) IS
factoring.** This is a clean instance of barrier 6: a legitimate barrier-5
attack (the coordinate is NOT orthogonal) that collapses on circularity because
its handle is the prize itself.

---

## 4. The two "readout" attacks (FOU, HCOM)

**FOU (experiment 287).** The factor-indicator function g(x) = [gcd(x,N) > 1]
on ℤ/Nℤ has DFT ĝ(t) = −c_N(t) (Ramanujan sum) for t ∈ (0,N). The informative
spikes: t a multiple of p (not q) → ĝ = p−1; t a multiple of q (not p) → ĝ = q−1;
all other t → ĝ = −1 (coprime t gives c_N(t) = μ(N) = 1). The closed form
c_N(t) = μ(N/g)·φ(N)/φ(N/g) requires φ(N) whenever g is a proper divisor.
**Informative spikes exist exactly where gcd(t,N) already IS the factor** —
the readout is circular in the sharpest possible sense. A tight, publishable
negative result.

**HCOM (experiment 289).** S = {(x,y) ∈ (ℤ/Nℤ)² : x² ≡ y² mod N} splits via
(x−y)(x+y) ≡ 0 into four CRT lattices: two VISIBLE (L_N = {(x,x)}, L_- =
{(x,−x)}) and two HIDDEN (mixed sign patterns). Verified |S| = 4N − 2(p+q) + 1,
and that any hidden point factors N (gcd(x−y,N) = p). The N-computable ± moves
(sign flips, the only square-preserving roots computable from N) never leave the
visible set — escape probability exactly 0. Entering a hidden component requires
the CRT idempotent, which IS factoring. **HCOM converts barrier 6 into precise
geometric form**: factoring == reaching a hidden CRT lattice point, and every
N-computable move preserves visibility.

---

## 5. The reciprocity attack (NSPLIT)

**NSPLIT (experiment 291).** The Jacobi symbol (u/N) = (u/p)(u/q) is the
S₂-symmetric datum (barrier 2). Can 4th-order biquadratic reciprocity in ℤ[i]
split it? For N = p·q, p ≡ q ≡ 1 (mod 4), p = (a+bi)(a−bi), q = (c+di)(c−di),
the biquadratic symbols (u/π₁)₄ and (u/π₂)₄ see each Gaussian prime separately.
Computed (u/π₁)₄, (u/π₂)₄ for N = 629 = 17·37 (p = 1²+4², q = 1²+6²): the
PRODUCT is relabeling-invariant (an N-computable datum), but the INDIVIDUAL
symbols swap under the p↔q relabeling — which is exactly the unknown
factorization. Every N-computable datum is invariant under both the S₂ swap and
complex conjugation (π ↔ π̄, i ↔ −i); the individual symbols are not. **Barrier 2
holds in every abelian reciprocity law** (all of class-field-theoretic
reciprocity), as predicted. Non-abelian reciprocity could in principle
distinguish primes, but no non-abelian reciprocity law is N-computable either.

---

## 6. Meta-lessons for the barrier framework

1. **Barrier 5 is robust to combinations.** Not just individual invariants, but
   arbitrary functions of them, remain N-only (PAIR, BPPF).
2. **Novel coordinate systems collapse to known barriers.** Carryless
   convolution (BDPC), F₂[x] bit-polynomials (BPPF), and numerical semigroups
   (SEMI) all introduced genuinely new coordinates; all collapsed — to
   aggregation cost (4), N-drift (5), or circularity (6).
3. **The circularity barrier has geometric and algebraic precision.** HCOM shows
   it as "hidden CRT lattices unreachable by N-computable moves"; SEMI shows it
   as "the defining invariant equals φ(N)". Both are sharp, non-heuristic forms.
4. **Barrier 2 extends to abelian reciprocity.** The S₂ swap and complex
   conjugation exhaust the symmetries of N-computable data in number-field
   lifts; only non-abelian laws could break them, and those are not
   N-computable.
5. **Adaptivity is closed.** The atomic "find a multiple of p" primitive sits on
   the √N line for every genuinely adaptive strategy.
6. **The honest frontier.** Every one of the eight hypotheses was a legitimate
   attack on a real gap in the framework's empirical coverage; each closure
   sharpened the framework. No classical poly(log N) factoring algorithm emerged.
   The barrier framework remains intact at 292 experiments.

---

## 7. Honest bottom line

Eight novel hypotheses, each a genuine mathematical object or argument outside
the prior 284 experiments, were all closed consistently with the barrier
framework. Two produced tight, publishable negative results (FOU, HCOM); one
(SEMI) identified the first genuinely non-orthogonal coordinate and pinned its
failure to circularity; one (ADAPT) confirmed the adaptive-query lower bound by
measurement. None beat GNFS. The frontier of classical factoring remains the
barrier framework; the only poly(log N) route known is Shor's quantum algorithm.

---

*Related:* `00_CONSOLIDATED_BREAKTHROUGH_REPORT.md`, `09_Quantum_Classical_Boundary.md`
(DFT barrier), `11_CRT_Split_Iteration_NoGo.md` (iteration no-go), the lab
notebook Parts 31-38 (per-experiment records).

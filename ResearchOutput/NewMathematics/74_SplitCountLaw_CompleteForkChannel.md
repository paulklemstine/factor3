# The Complete Symmetric Fork Channel Is the Split-Count: I(N mod f; s) = Is(n) (SPLIT-COUNT-LAW)

**Program:** Factoring research lab — cron loop round-20 #2
**Date:** 2026-08-12
**Status:** Machine-verified exact law (8 fields, MC + exhaustive enumeration).

Papers 71–73 characterized the OR projection of a character-pinned fork — the
semiprime OR collapse I(N mod f; [split(p) OR split(q)]) = g(n) with the global
cap g(2) = 0.3113 over every class-rate profile (paper 73). This paper closes
the question at the FULL-channel level: the ordered pair of split-events
(E(p), E(q)) is two independent Bernoulli(1/n) draws (χ(p), χ(q) independent
uniform over the n character values), so the entire symmetric information of a
fork at the semiprime level is carried by the **split-count**

    s = [split(p)] + [split(q)] ∈ {0, 1, 2},   s ~ Binomial(2, 1/n),

and the full channel obeys the exact, order-universal law

    I(N mod f; s) = Is(n) = H(Bin(2,1/n)) − (1/n)H((n−1)/n, 0, 1/n)
                             − ((n−1)/n)H((n−2)/n, 2/n, 0).

Every Boolean projection is a function of s, so Is(n) dominates them all — and
**paper 73's OR cap is a projection artifact: the full channel reaches
Is(2) = 1.0000 bits (the p−1 ℓ=3 story's complete content, vs its celebrated
0.313 OR projection) and Is(3) = 0.4739 bits, the largest nondeterministic
residue channel in the lab.** Over ALL class-rate profiles the full channel is
capped at 1.0 bit, attained exactly by the quadratic characters. Factor-useless
— barriers 2/5/6/8.

## 1. The split-count channel

Let E(p) = [split(p)] = [χ(p) = 1] for an order-n Dirichlet character χ of
conductor f (P(split) = 1/n; paper 71's abelianization criterion). For a
semiprime N = pq with gcd(N, f) = 1, χ(N) = χ(p)χ(q). The pair (χ(p), χ(q))
is two independent uniform draws from the n character values (by
equidistribution), so (E(p), E(q)) is two independent Bernoulli(1/n) and
s = E(p)+E(q) ~ Binomial(2, 1/n) unconditionally:

    P(s=0,1,2) = ((n−1)/n)², 2(n−1)/n², 1/n².

The unordered pair is determined by s (s=0 ⟺ (0,0); s=1 ⟺ one split factor;
s=2 ⟺ (1,1)); the which-factor label given s=1 is symmetric and carries zero
channel (barrier 2). Conditioning on the residue class (unit pairs ab ≡ N):

    P(s | χ(N)=1)   = {(n−1)/n, 0, 1/n}       (both-split only when both are 1;
                                                 exactly-one impossible)
    P(s | χ(N)≠1)   = {(n−2)/n, 2/n, 0}       (both-split impossible; exactly-one
                                                 on the two values χ(a)=1, χ(a)=c)

so the full channel is

    Is(n) = H(Bin(2,1/n)) − (1/n)H((n−1)/n, 0, 1/n) − ((n−1)/n)H((n−2)/n, 2/n, 0).

Each Boolean projection is a deterministic function of s (OR ⟺ s ≥ 1, AND ⟺ s = 2,
XOR ⟺ s = 1), hence by data processing Is(n) ≥ I_OR, I_AND, I_XOR, with the
exact projection laws g(n) (paper 72), A(n) = H(1/n²) − (1/n)H(1/n) (AND,
round-20 #1), and X(n) = H(2(n−1)/n²) − ((n−1)/n)H(2/n) (XOR, derived here).

## 2. The law on 8 fields (Part A)

2^22 prime sieve; 30,000 semiprimes at 23/25-bit factors per field; split sets
empirically confirmed (nroots == deg on 6,541 primes per field); s, OR, AND,
XOR measured against the closed forms:

| field | n | cond | Is measured | Is(n) | OR vs g(n) | AND vs A(n) | XOR vs X(n) | wall |
|---|---|---|---|---|---|---|---|---|
| Q(√5): x²−x−1 | 2 | 5 | **1.0000** | 1.0000 | 0.3076/0.3113 | 0.3156/0.3113 | 1.0000/1.0000 | 0.0001 |
| p−1 ℓ=3: Q(√−3) | 2 | 3 | **1.0000** | 1.0000 | 0.3131/0.3113 | 0.3096/0.3113 | 1.0000/1.0000 | 0.0000 |
| cyclic cubic | 3 | 7 | **0.4731** | 0.4739 | 0.0711/0.0728 | 0.1993/0.1972 | 0.3769/0.3789 | 0.0002 |
| cyclic cubic 3² | 3 | 9 | 0.4718 | 0.4739 | 0.0775/0.0728 | 0.1906/0.1972 | 0.3802/0.3789 | 0.0002 |
| Q(ζ₁₆)+ (C₂×C₄) | 4 | 16 | 0.2894 | 0.2947 | 0.0383/0.0359 | 0.1289/0.1345 | 0.2026/0.2044 | 0.0001 |
| Q(ζ₁₁)+ | 5 | 11 | 0.2060 | 0.2027 | 0.0202/0.0215 | 0.1014/0.0979 | 0.1281/0.1276 | 0.0002 |
| Φ₇ | 6 | 7 | 0.1482 | 0.1487 | 0.0128/0.0144 | 0.0763/0.0748 | 0.0851/0.0872 | 0.0001 |
| cyclic cubic (C₂×C₆) | 3 | 21 | 0.4755 | 0.4739 | 0.0719/0.0728 | 0.2000/0.1972 | 0.3794/0.3789 | 0.0003 |

All eight fields match the four closed forms to Monte-Carlo noise. The split-count
distribution matches Bin(2, 1/n) on every field (e.g. f=7 n=3: [0.442, 0.447,
0.111] vs [4/9, 4/9, 1/9]). The which-factor wall is 0.0000–0.0003 everywhere
(barrier 2): no factor label leaks.

## 3. Exact tables and the corrected hierarchy (Part B)

| n | Is(n) | X(n) | A(n) | g(n) |
|---|---|---|---|---|
| 2 | 1.0000 | 1.0000 | 0.3113 | 0.3113 |
| 3 | 0.4739 | 0.3789 | 0.1972 | 0.0728 |
| 4 | 0.2947 | 0.2044 | 0.1345 | 0.0359 |
| 5 | 0.2027 | 0.1276 | 0.0979 | 0.0215 |
| 6 | 0.1487 | 0.0872 | 0.0748 | 0.0144 |
| 7 | 0.1141 | 0.0633 | 0.0592 | 0.0103 |
| 8 | 0.0906 | 0.0480 | 0.0482 | 0.0077 |
| 9 | 0.0738 | 0.0377 | 0.0401 | 0.0060 |
| 10 | 0.0614 | 0.0303 | 0.0339 | 0.0048 |
| 11 | 0.0519 | 0.0250 | 0.0291 | 0.0040 |
| 12 | 0.0445 | 0.0209 | 0.0253 | 0.0033 |

**Honest hierarchy correction.** The naive chain Is ≥ X ≥ A ≥ g FAILS from n=8:
X(8) = 0.0480 < A(8) = 0.0482 (the AND face overtakes the XOR face slightly for
n ≥ 8). The correct universal statements are: (i) **Is(n) ≥ each Boolean
projection at every order** (data processing — the split-count determines all
three); (ii) **A(n) ≥ g(n) at every order** (AND beats OR for all n, not just
n ≥ 3); (iii) X(n) ≥ A(n) ⟺ n ≤ 7, a single crossing near n ≈ 7.6. The naive
4-term chain is superseded by the single dominance of the split-count.

## 4. The full channel's global cap (Part C) — exact enumeration

Enumerating ALL 2^φ 0/1 profiles on the nine moduli (m = 3,4,5,7,8,9,11,16,21 —
prime/composite conductors, cyclic and non-cyclic unit groups C₂×C₂, C₂×C₄,
C₂×C₆), the split-count functional and the XOR functional are both evaluated
exactly:

| m | unit group | profiles | max Is | max I_XOR | argmax |
|---|---|---|---|---|---|
| 3, 4, 5, 7 | C₂/C₄/C₆ | 4–64 | **1.0000** | 1.0000 | QR kernels + complements (2/2 quadratic) |
| 8 | C₂×C₂ | 16 | **1.0000** | 1.0000 | three quadratic chars of cond 8 (6/6) |
| 9, 11 | C₆/C₁₀ | 64–1024 | **1.0000** | 1.0000 | QR kernels + complements |
| 16, 21 | C₂×C₄/C₂×C₆ | 256–4096 | **1.0000** | 1.0000 | three index-2 kernels each (6/6) |

**The full symmetric fork channel is capped at 1.0 bit over every class-rate
profile, attained EXACTLY by the quadratic-character kernels.** Paper 73's
0.3113 cap was the OR projection's cap; the full channel's cap is 1.0 — larger,
but the maximizer is the same family (the quadratic characters), and the
channel remains a symmetric residue dial, factor-useless.

## 5. Controls and the unification (Part D)

- **Coprime modulus flat:** I(N mod m′; s) = 0.0001–0.0003 for every m′
  coprime to f (f=3→5, f=5→7, f=7→5, f=9→5).
- **m = f² invariant:** I(N mod f²; s) = Is(n) exactly (f=5: 1.0003; f=7:
  0.4692; f=9: 0.4755 vs Is(3) = 0.4739).
- **Unification — the p−1 ℓ=3 channel is complete.** f=3, n=2, split = p ≡ 1
  mod 3: I(N mod 3; s) = **1.0000 bits**, with P(s | N≡1) = [1/2, 0, 1/2] and
  P(s | N≡2) = [0, 1, 0] EXACT (measured [0.503, 0.000, 0.497] and
  [0.000, 1.000, 0.000]). Paper 54's celebrated I(N mod 3; OR) = 0.313 is one
  Boolean projection of this 1-bit channel; the XOR face (also 1 bit) is the
  deterministic indicator χ(N) = −1.

## 6. Seals / barriers

- **Symmetry (barrier 2):** s is symmetric in (p,q); the which-factor label
  given s=1 is independent of N's class (wall 0.0000–0.0003 on every field).
- **Structural orthogonality (barrier 5):** the whole channel is a residue dial
  (Dirichlet characters + the class-pair convolution + binomial), N-only.
- **Circularity (barrier 6):** s is N-computable from the CRT/character
  structure; recovering a factor from the split-count IS the factorization.
- **Known methods (barrier 8):** quadratic reciprocity (Gauss 1801), cubic
  reciprocity (Eisenstein 1844), Dirichlet characters, CRT, binomial
  equidistribution — all classical; the law is a counting/entropy identity.

**Unification (corrective ledger).** Paper 54's p−1 ℓ=3 channel (0.313 OR) is
the OR projection of a 1.0000-bit split-count channel at n=2, f=3; papers
71–72's OR collapse g(n) is the OR projection of Is(n) at every order; paper
73's global OR cap g(2) = 0.3113 is the OR projection's cap — the FULL
symmetric fork channel is larger (Is(2) = 1.0, Is(3) = 0.4739) yet still
capped (1.0 bit, at the quadratic characters) and still factor-useless. The
residue-fork line is closed at the full-channel level: **the split-count s is
the complete N-level information content of any character-pinned fork.**

*Script:* /tmp/exp_splitcount.py (MC + exact enumeration, 30 s).

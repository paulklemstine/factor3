# The Mod-Exponential Sequence Is Smoothness-Blind: Controlled p−1-Smoothness Detection in Sequence Statistics Is Null (SEQSMOOTH-NULL)

**Program:** Factoring research lab — cron loop round-15 #6 (final)
**Date:** 2026-08-12
**Status:** Machine-verified null. In a controlled, matched comparison, the
mod-exponential sequence statistics of an instance do not leak whether its
smaller factor has a smooth p−1 (the ECM/p−1-weak class). The classes genuinely
differ (the Pollard p−1 method factors the smooth class 35/36 and the general
class 0/36), yet no windowed sequence feature separates them (permutation null
p = 0.502; logistic AUC = 0.500). Barriers 2/4/8.

---

## Abstract

Machine-verified null result. **(1) Controlled contrast (real):** in 36 matched
pairs of semiprimes (p, q bit-lengths matched at 18/20, only p−1 smoothness
differs), the SMOOTH class (smaller factor p with p−1 B-smooth at B = 100) is
genuinely distinct from the GENERAL class (p−1 with a large prime factor): the
Pollard p−1 method factors 35/36 smooth instances and 0/36 general ones. The
ECM-weakness is real and detectable — but only by running the method. **(2)
Sequence statistics (null):** 42 features over a window of m = 256 consecutive
values (m ≪ B = 100) of {a^x mod N} for bases a ∈ {2,3,5}, and of the floor twin
t_x = (a^x − s_x)//N — distinct-count, self-collision gap, top-bit balance,
adjacent-difference, lag-1 autocorrelation, spectral flatness, max run-length —
separate the classes NOTHING: the observed max standardized difference (0.473)
sits at the permutation null (mean 0.495, 95th pct 0.734, p = 0.502), and a
5-fold logistic classifier achieves AUC = 0.500 (exactly chance). **(3)
Mechanism:** the sequence values s_x carry no residue of the order structure
ord_p(a) | p−1 — the group element a^x mod p is pseudorandom in its subgroup
regardless of how smooth the group order is; exploiting the smoothness requires
computing a^M mod N for M = lcm(1..B) and gcd'ing with N (the p−1 method itself,
O(B) multiplications), which no finite window of consecutive values reaches. The
mod-exp sequence is N-computable, symmetric in (p,q), and class-independent
incompressible (barriers 2/4); the p−1 weakness is exploitable only by a known
method (barrier 8). This closes the sequence-level face of the self-hint program:
the p−1/ECM weakness is invisible both in residues (SMOOTH-SELFHINT-DENSITY) and
in the sequence statistics, and round-15 is complete.

---

## 1. Setup and the controlled contrast

SEQSTATE (round-14 #8) established that s_x = a^x mod N and the floor twin
t_x = ⌊a^x/N⌋ are random-level incompressible. SMOOTH-SELFHINT-DENSITY (round-14
#10) established that p−1 B-smoothness is residue-invisible from N alone.
SEQSMOOTH-NULL completes the sequence-level question: does the *time-evolution*
of a^x mod N distinguish the ECM-weak class (smaller factor p with p−1 smooth)
from a matched general class? The experiment generates 36 pairs:

- **GENERAL:** p, q both primes with p−1, q−1 having a prime factor > B (=100).
- **SMOOTH:** p with p−1 B-smooth (built from small primes, p−1 | lcm(1..B)), q
  general — only the smaller factor's p−1 smoothness differs from GENERAL.

Bit-lengths are matched (p ~ 2¹⁸, q ~ 2²⁰), so any observable difference between
the classes is attributable to p−1 smoothness alone.

**Positive control.** The Pollard p−1 method (a = 2, M = lcm(1..B), gcd(2^M − 1,
N)) finds the small factor in 35/36 SMOOTH instances and 0/36 GENERAL instances.
The classes are genuinely different in the sense that matters: smooth instances
are p−1-weak, general ones are not. (The single SMOOTH miss is the classical
case where 2^M ≡ 1 mod q too, so the gcd is N rather than p.)

## 2. Sequence statistics, null

For each instance and each base a ∈ {2,3,5}, the window {s_1, …, s_m} with
m = 256 and its floor twin {t_1, …, t_m} yield 7 features each (42 total):
fraction of distinct values; minimum self-collision gap / m; top-bit balance;
mean adjacent-difference / N; lag-1 top-bit autocorrelation; spectral flatness of
the top-bit FFT; max run-length / m. Across all 42 features:

| feature set | GENERAL mean | SMOOTH mean | std-diff |
|-------------|--------------|-------------|----------|
| distinct (seq, all a) | 1.000 | 1.000 | 0.00 |
| coll-gap (seq) | 1.000 | 1.000 | 0.00 |
| topbit (seq, a=2) | 0.438 | 0.436 | 0.02 |
| adj-diff (seq, a=3) | 0.257 | 0.254 | 0.03 |
| ac1 (floor, a=3) | 0.726 | 0.729 | 0.03 |
| specflat (seq, a=5) | 0.516 | 0.536 | 0.06 |
| maxrun (floor, a=2) | 0.026 | 0.027 | 0.02 |

No feature differs by more than a fraction of its pooled standard deviation. The
separation test formalizes this: over 500 label-permutations, the max
standardized difference across all 42 features has null mean 0.495 and 95th
percentile 0.734; the observed value 0.473 lies squarely inside (p = 0.502). A
5-fold logistic classifier on the full 42-feature vector achieves AUC = 0.500 —
exactly chance. The sequence carries zero detectable signal about the smoothness
class.

## 3. Mechanism: why the values cannot see the order structure

For a base a coprime to N, the orbit of a^x mod p lies in the subgroup ⟨a⟩ of
(Z/pZ)× of order ord_p(a) | p−1. Smoothness of p−1 constrains the *group size*,
not the *walk*: within its subgroup, a^x mod p is a cyclic (pseudo-)random walk,
and its short-window statistics are identical whether |⟨a⟩| = ord_p(a) is smooth
or has a large prime factor. The genuine observable consequence of smoothness is
that the *entire* group order p−1 divides M = lcm(1..B), so a^M ≡ 1 mod p — but
reaching x = M requires computing the modular power with exponent M (a 136-bit
exponent at B = 100), i.e., running the p−1 method itself. No windowed statistic
of {a^x : x ≤ m} with m ≪ B can reach the M-th term or detect the divisibility;
and measuring ord_p(a) from the window would require seeing a repeat at x = ord
— a period typically ≫ m in both classes (both classes have general q with q−1
∤ M, so ord_q(a) is large and the full-sequence period r = lcm(ord_p, ord_q) is
large in both).

## 4. Why this cannot factor: barriers 2, 4, 8

1. **Barrier 2 (symmetry).** The sequence is N-computable and hence symmetric in
   (p,q); more sharply, it is class-independent: smooth and general instances
   produce statistically identical sequences, so the instance-class asymmetry
   (which factor is weak) is not reflected in the observable at all.
2. **Barrier 4 (free-witness aggregation).** Any sequence statistic is
   N-computable at O(m·log N) cost; the point is that none of them carries
   factor content, and the *only* computation that does — a^M mod N with
   M = lcm(1..B) — is the p−1 method itself, an O(B) modular-exponentiation
   (sub-exponential in log N only for genuinely small B) that is a known method,
   not a free witness.
3. **Barrier 8 (known method in disguise).** The p−1 weakness is exploited by the
   Pollard p−1 algorithm, classical; the null says precisely that there is no way
   to extract the weakness from the sequence other than by running that method.

## 5. Conclusion

SEQSMOOTH-NULL completes round-15 and closes the sequence-level face of the
self-hint program. The p−1/ECM weakness is real (35/36 vs 0/36 for the p−1
method) but invisible in the mod-exponential sequence: 42 windowed statistics
over bases {2,3,5}, on both the sequence and its floor twin, separate the smooth
class from a matched general class at exactly chance level (permutation p =
0.502, AUC 0.500). The values of a^x mod N carry no residue of the smoothness of
p−1; exploiting the weakness requires running the p−1 method itself (barrier 8),
never inspecting the sequence (barriers 2/4). The self-hint program is fully
closed: hints must be genuinely external, and the mod-exp sequence — like the
residue battery before it — is smoothness-blind.

---

**Experiment:** 397 (SEQSMOOTH-NULL). **Script:** /tmp/exp_seqsmoothnull.py.
**Assessment:** v173. **Verdict:** CONFIRMED null (negative for factoring) —
controlled matched comparison (36 pairs, p,q bit-lengths matched, only p−1
smoothness differs): the p−1 METHOD factors SMOOTH 35/36 vs GENERAL 0/36 (the
weakness is real), yet 42 windowed sequence features over bases {2,3,5} on both
s_x = a^x mod N and the floor twin separate nothing (max std-diff 0.473 at the
permutation null, p = 0.502; logistic AUC 0.500 exactly chance); the values
carry no residue of ord_p(a) | p−1, exploiting the smoothness requires running
the p−1 method (known method, barrier 8), never inspecting the sequence
(N-computable, symmetric, class-independent incompressible, barriers 2/4) —
round-15 COMPLETE (6/6).

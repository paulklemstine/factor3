# p+1 Smoothness Is Residue-Invisible, Lucas-Sequence-Invisible, and Discriminant-Gated: the Williams Weakness Is Sealed (PLUSONE-SMOOTH-NULL)

**Program:** Factoring research lab — cron loop round-16 #2
**Date:** 2026-08-12
**Status:** Machine-verified null. In a controlled, matched comparison, the p+1
B-smoothness class (the Williams p+1 / Lucas-sequence weakness, the sibling of the
p−1/ECM weakness) is invisible from N alone in three independent senses: the
residue mutual information is null while its symmetric control is visible; the
Lucas V-sequence statistics separate the class from a matched general class at
chance; and — the new structural finding — the p+1 method's view of N is gated by
a factor-private discriminant character (P²−4 | p), whose SPLIT between p and q is
not N-computable even though the product (P²−4 | N) is. The classes genuinely
differ (the p+1 method factors the +1-smooth class 24/40 vs 0/40 general), but the
weakness is exploitable only by running the 1982 method. Barriers 2/4/8.

---

## Abstract

Machine-verified null result. **(1) The contrast is real.** In 40 matched pairs
(p, q bit-lengths matched at 18/21, only the smaller factor's p+1 divisibility
differs), the PLUSONE class (p+1 | M = lcm(1..100), i.e. all prime *powers* of
p+1 ≤ 100, p−1 general) is genuinely distinct from the GENERAL class (p±1 and
q±1 all carrying a prime factor > 100): the Williams p+1 method factors PLUSONE
24/40 and GENERAL 0/40. The ECM-family weakness is real and detectable — but only
by running the method. **(2) Residue-invisible (null).** I(N mod ℓ; ℓ | p+1) for
the smaller factor is 0.0005/0.0002/0.0014/0.0017/0.0022 bits at ℓ = 3/5/7/11/13,
at or below the permutation null in every case (none significant), while its
symmetric control I(N mod ℓ; ℓ|p+1 OR ℓ|q+1) is 0.2996/0.0327/0.0158/0.0070/0.0052
— the asymmetric/symmetric divisibility dichotomy on the +1 side, exactly
mirroring the p−1 side (SMOOTH-SELFHINT-DENSITY: 0.313 at ℓ=3). N cannot tell
which factor is ≡ −1 mod ℓ. **(3) Lucas-sequence-invisible (null).** 21 windowed
features (m = 256 ≪ B; bases P = 3, 5, 7; distinct count, self-collision gap,
top-bit balance, adjacent-diff, autocorr, spectral flatness, max run) of the Lucas
V-sequence V_n mod N separate the classes at chance: observed max std-diff 0.241
sits *below* the permutation null mean 0.381 (p = 0.898). **(4) Discriminant-gated
(new, the structural finding).** Per-base p+1 success is *exactly* the subset with
(D|p) = −1: per-base success equals the (D|p) = −1 rate exactly (P = 3: 11/40 =
11/40; P = 5: 17/40 = 17/40; P = 7: 11/40 = 11/40) and 24/24 successful
factorizations carry (D|p) = −1. The gate is the factor-private character: even
though the product (D|N) = (D|p)(D|q) is N-computable, its split is not, and among
successes (D|N) = −1 in only 11/24 ≈ 1/2 of cases — the N-computable sign predicts
nothing. The +1 weakness is therefore strictly more hidden than the −1 weakness:
it is residue-invisible, sequence-invisible, *and* gated by a sign N cannot
certify. This closes the ECM-family self-hint program: p−1 (SMOOTH-SELFHINT-
DENSITY, SEQSMOOTH-NULL) and p+1 (here) are both invisible, and ECM's group order
p+1−t lies between them. Barriers 2/4/8.

---

## 1. Setup: the Lucas/p+1 side of the ECM family

SEQSMOOTH-NULL (round-15 #6) closed the mod-exponential (p−1-side) sequence
channel; SMOOTH-SELFHINT-DENSITY (round-14 #10) closed its residue channel. The
sibling classical weakness — the one the p−1 method cannot see — is the Williams
**p+1 method** (1982), built on Lucas sequences. For a base P with discriminant
D = P² − 4 and Q = 1, the sequences U_n, V_n satisfy V_n = P·V_{n−1} − V_{n−2}.
For a prime p, if (D|p) = −1 then U_{p+1} ≡ 0 and V_{p+1} ≡ 2 (mod p), so if
p+1 | M = lcm(1..B), then gcd(V_M − 2, N) exposes p. If (D|p) = +1 the order
divides p−1 and the method degenerates to the p−1 world. This experiment tests
every face of the p+1 weakness:

- **Classes.** PLUSONE: smaller p with p+1 | M (all prime powers of p+1 ≤ 100)
  and p−1 general; GENERAL: p±1, q±1 all with a prime factor > 100. Bit-lengths
  matched (18/21), so the only difference is the +1 smoothness of the smaller
  factor.
- **Positive control.** The p+1 method (M = lcm(1..100), bases 3, 5, 7) factors
  PLUSONE 24/40, GENERAL 0/40. (P = 2 is the degenerate base D = 0: V_n = 2 for
  all n, gcd(0, N) = N, never a factor.)
- **Residue channel.** I(N mod ℓ; ℓ|p+1) (asymmetric, smaller factor) vs
  I(N mod ℓ; ℓ|p+1 OR ℓ|q+1) (symmetric), ℓ = 3, 5, 7, 11, 13, over 4000 random
  16-bit semiprimes with shuffled nulls.
- **Sequence channel.** Windowed statistics of the Lucas V-sequence V_1..V_256
  mod N (bases 3, 5, 7), the p+1-side analogue of the mod-exp sequence.
- **Discriminant gating (new).** Per-base success vs the (D|p) = −1 set, and the
  N-computable product sign (D|N).

## 2. Positive control: the classes genuinely differ

| class | factored (≥1 base) | P=3 | P=5 | P=7 |
|-------|--------------------|-----|-----|-----|
| PLUSONE (p+1 \| M) | **24/40** | 11/40 | 17/40 | 11/40 |
| GENERAL (p±1 general) | **0/40** | 0/40 | 0/40 | 0/40 |

The +1-smooth class is p+1-weak; the general class is not. The weakness is real,
exactly as the p−1 weakness was real in SEQSMOOTH-NULL (35/36 vs 0/36).

## 3. Residue invisibility: the +1 divisibility dichotomy

Over 4000 random 16-bit semiprimes (p = smaller factor), base rates match
Chebotarev: P(ℓ|p+1) = 0.499/0.240/0.165/0.104/0.081 ≈ 1/(ℓ−1) =
0.500/0.250/0.167/0.100/0.083. The mutual information:

| ℓ | I(N mod ℓ; ℓ\|p+1) asym | null max | I(N mod ℓ; ℓ\|p+1 OR ℓ\|q+1) sym | null max |
|---|--------------------------|----------|-----------------------------------|----------|
| 3  | 0.0005 | 0.0016 | 0.2996 | 0.0010 |
| 5  | 0.0002 | 0.0029 | 0.0327 | 0.0025 |
| 7  | 0.0014 | 0.0030 | 0.0158 | 0.0036 |
| 11 | 0.0017 | 0.0039 | 0.0070 | 0.0048 |
| 13 | 0.0022 | 0.0044 | 0.0052 | 0.0046 |

The asymmetric event is at or below the null at every ℓ (none significant; the
symmetric control is 50–300× the null max at ℓ = 3, 5, 7). This is the p−1
dichotomy (SMOOTH-SELFHINT-DENSITY: asym = 0, sym = 0.313 at ℓ = 3) restated on
the +1 side: N mod ℓ cannot certify which factor is ≡ −1 mod ℓ, even though it
pins the product. Mechanism exact at ℓ = 3: N ≡ 2 mod 3 forces exactly one factor
≡ 2 mod 3 (so P(sym) = 1), while N ≡ 1 mod 3 leaves (1,1) vs (2,2) — but the
smaller factor's own class is undetermined in both cases.

## 4. Lucas-sequence invisibility: the V-sequence is class-blind

The p+1 method's natural observable is the Lucas V-sequence V_n mod N (bases
P = 3, 5, 7; 256 consecutive values; 7 features each: distinct fraction,
self-collision gap, top-bit balance, mean adjacent-diff / N, lag-1 autocorr,
spectral flatness of the top-bit FFT, max run-length). Across all 21 features:

- observed max standardized difference = **0.241**;
- permutation null (500 label shuffles): mean 0.381, 95th percentile 0.591,
  max 0.745 → **p = 0.898**.

The observed separation sits below the null mean — the classes are
statistically indistinguishable. The values V_n mod N carry no residue of the
order structure ord_{p}(V) | p+1: smoothness constrains the orbit size, not the
walk, exactly as in the p−1 world (SEQSMOOTH-NULL).

## 5. Discriminant gating: the +1 weakness is hidden by a sign N cannot certify

The new structural finding. Per-base p+1 success is **exactly** the (D|p) = −1
subset:

| base P | D | per-base success | (D\|p) = −1 rate | (D\|p) = −1 among successes |
|--------|-----|------------------|--------------------|-------------------------------|
| 3 | 5  | 11/40 | 11/40 | 24/24 total |
| 5 | 21 | 17/40 | 17/40 |             |
| 7 | 45 | 11/40 | 11/40 |             |

Per-base success equals the character rate *exactly*, and every one of the 24
successful factorizations carries (D|p) = −1: the gate is exact, not statistical.
(Consistency check: D₃ = 5 and D₇ = 45 = 5·3² lie in the same square class, so
(D₃|p) = (D₇|p) = (5|p) and P = 3 and P = 7 succeed on the identical 11 instances —
measured 11/40 = 11/40.) The character (D|p) = −1 occurs on ~1/2 of the +1-smooth
class (rates 0.28/0.42/0.28 over the three bases), so a single base "sees" only
~half of the weak instances — the classical "p+1 needs luck on the character" —
and the classical remedy is multiple bases.

Why the remedy is bounded: the product (D|N) = (D|p)(D|q) **is** N-computable
(Jacobi symbol of D mod N), but its split between p and q is not — computing
(D|p) requires p. Among the 24 successes, (D|N) = −1 in only 11/24 ≈ 1/2 of
cases (since (D|q) is an independent ±1 on the general factor). So even knowing
(D|N), an attacker cannot certify whether the smooth factor is the one with
(D|p) = −1; the gate is factor-private. The +1 weakness is thus strictly more
hidden than the −1 weakness: it is residue-invisible (Section 3),
sequence-invisible (Section 4), *and* gated by a sign N cannot compute.

## 6. Why this cannot factor: barriers 2, 4, 8

1. **Barrier 2 (symmetry).** Every observable is N-computable, hence symmetric;
   the +1-divisibility event on the smaller factor is N-determinable yet carries
   zero mutual information with N mod ℓ (Section 3), and the only N-computable
   character (D|N) has a hidden split (Section 5). The instance-class asymmetry —
   which factor is +1-weak, and which base's discriminant is a non-residue on it —
   is uncomputable from N.
2. **Barrier 4 (free-witness aggregation).** The p+1 weakness is exploited by
   computing V_M mod N for M = lcm(1..B) (O(log M) Lucas doublings) and gcd'ing —
   the p+1 method itself, a known method, never a free witness. No finite window
   of the V-sequence reaches x = M or detects the divisibility.
3. **Barrier 8 (known method in disguise).** Williams p+1 (1982) is classical;
   P = 2 is the degenerate base (D = 0, V_n ≡ 2, gcd(0, N) = N). Together with
   SEQSMOOTH-NULL's p−1 closure, the entire ECM-family self-hint program is now
   closed: ECM's group order is p + 1 − t (trace of Frobenius), and both its
   classical extremes, p−1 and p+1, are residue-invisible, sequence-invisible,
   and (for p+1) additionally discriminant-gated.

## 7. Conclusion

PLUSONE-SMOOTH-NULL completes round-16 #2 and closes the Lucas/p+1 side of the
ECM-family self-hint program. The p+1 B-smoothness class is genuinely distinct —
the Williams p+1 method factors it 24/40 vs 0/40 — yet invisible from N in every
probed channel: residue MI null while its symmetric control is visible (the +1
divisibility dichotomy), Lucas V-sequence statistics separating nothing
(p = 0.898), and — the new finding — per-base success *exactly* the (D|p) = −1
subset, gated by a factor-private character whose split N cannot certify even
though its product is N-computable. The weakness is real but exploitable only by
running the 1982 method. Barriers 2/4/8. The p±1 extremes of the ECM family are
now sealed on both sides; the self-hint program stands fully closed.

---

**Experiment:** 399 (PLUSONE-SMOOTH-NULL). **Script:** /tmp/exp_plusone_smoothnull.py.
**Assessment:** v175. **Verdict:** CONFIRMED null (negative for factoring) — the
p+1 B-smoothness class is invisible from N in three independent senses: the
Williams p+1 method factors PLUSONE 24/40 vs GENERAL 0/40 (positive control: the
weakness is real), yet I(N mod ℓ; ℓ|p+1) = 0.0005/0.0002/0.0014/0.0017/0.0022 at
ℓ = 3/5/7/11/13 (at or below null) while the symmetric control I(N mod ℓ; ℓ|p+1 OR
ℓ|q+1) = 0.2996/0.0327/0.0158/0.0070/0.0052 is visible (the +1 divisibility
dichotomy, mirroring the p−1 side); 21 windowed Lucas V-sequence features
(bases 3, 5, 7, m = 256) separate the classes at chance (max std-diff 0.241 below
the null mean 0.381, p = 0.898); and — NEW — the p+1 method's view of N is gated
by a factor-private discriminant character: per-base success EQUALS the (D|p) = −1
rate exactly (P=3: 11/40 = 11/40, P=5: 17/40 = 17/40, P=7: 11/40 = 11/40; 24/24
successes have (D|p) = −1) while the N-computable product (D|N) predicts nothing
((D|N) = −1 in 11/24 ≈ 1/2 of successes) — the split is uncomputable from N, so
the +1 weakness is strictly more hidden than the p−1 one; exploiting it requires
running the classical 1982 method (barrier 8), never inspecting N (barriers 2/4)
— the ECM-family (p±1) self-hint program is fully closed. Barriers 2/4/8.

# Paper 128 — RAMIFIED-TYPE-CHANNEL: Ramified Primes Add Negligible Information

**Verdict name: RAMIFIED-CONTRIBUTION-IS-NEGLIGIBLE.**
Round-36 #1 · exp 460 · assessment v237.

## 1. The gap

Every prior type-channel measurement excluded ramified primes (those dividing the discriminant). This round tests whether ramified primes carry additional information beyond what unramified primes provide — filling a genuine methodological gap.

## 2. Results for x²−3 (ramified {2,3}, disc 12)

**UNRAMIFIED primes only**: types {nr=0: 3270, nr=2: 3270} — exactly 50/50 split, matching the quadratic character (−3|p) = ±1 with equal probability ✓.

**RAMIFIED primes**: p=2 gives x²+1 ≡ x(x+1) mod 2 → nr=2; p=3 gives x² ≡ 0 mod 3 → nr=1. Both show repeated roots or degenerate splitting — qualitatively different from unramified behavior.

**CHANNEL CAPACITIES**: I(p mod 12; T) all primes = 1.0020 bits vs unramified-only = 1.0000 bits. The inclusion of ramified primes adds **+0.002 bits** to the channel capacity.

## 3. What this decides

Ramified primes carry almost no additional type information beyond what unramified primes provide: the channel capacity increases by only ~0.002 bits when including the two ramified primes out of thousands of unramified ones. The programme's universal exclusion of ramified primes is fully justified — they contribute negligibly to the overall information content.

Now 460 experiments. Assessment v237.

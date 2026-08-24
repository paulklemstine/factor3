# exp588b U065-FEATURE-MECHANISM (round-74) -- findings
Question: name the ARITHMETIC carrier of the shift-invariant u*~0.65 hump of j^2-N smoothness.

REGEN (post-amendment A3): exp578 lineage reproduced EXACTLY -- population+window int64-equal
(jlo=isqrt(N)+1, jhi=3*isqrt(N)); stream replay (ONE rng/chunk, sequential 150k draws/N)
order-walk EXACT on all 128 samples; verbatim exp569 tester re-validates stored hits smooth /
controls non-smooth under exact N. B=1e6 known -> Dickman rho(ln v/ln 1e6) baseline, alpha
flank-fit. Pre-amendment blind arm was NO_MATCH (13 recipes); its statistical-inference labels
retained as DEGRADED arm in json. First-run surrogate-baseline numbers VOIDed pre-verdict (A2).

VERDICT: **MIXED-PARTIAL** (hump amp 0.116 +/- 0.036, z=3.23 over exact Dickman baseline;
paired-random control null, amp_ctl 0.027)
- H1 REJECTED in strong form: no candidate achieves removal>=60% with all strata flat.
  removal_pct = 0.0 for ALL candidates (worst stratum always retains significant excess):
  - (a) parity: z = 3.51 / 4.16 (both persist)
  - (b) 3|v: 4.36 / 2.38 ; 5|v: 4.56 / 1.84 ; 7|v: 3.91 / 2.44
  - (c) omega_100(v) terciles: 4.14 / 2.49 / 4.19
  - (d) gcd(j,N)>1: stratum EMPTY -- structurally vacuous at bitlen 96 (p~2^48 cannot divide
    j<=8.4e14); recorded as vacuous, not tested
- H0 strict letter also unmet: 5|v yes-stratum dips to z=1.84 (<2 bar).

READING: the hump is NOT carried by j parity, NOT by omega_100 richness tercile, NOT by any
single small-prime divisibility flag alone. But conditioning on m|v CONSISTENTLY absorbs part
of it (amplitude drops ~45-60% in each yes-stratum point estimate) while parity/omega absorb
none -> the excess is DISTRIBUTED ACROSS THE SMALL-PRIME DIVISIBILITY STRUCTURE of v=j^2-N
(arithmetic-internal), not a single-flag geometric artifact. Consequence: paper 232's mechanism
question routes to a divisibility-mixture/baseline-refinement model (mixture over v mod
small primes), not to a per-hit binary covariate.

Honest: verdict rules fixed pre-analysis; amendment log A1-A3 timed in json; est-arm labels
noisy (attenuate removal); omega100 ignores factors >100 by definition; full 150k-draw
rescan-and-reclassify not rerun (equivalence via window/stream/smoothness checks, disclosed).

Wall 15.1s; boot seed 20260901; only exp588b_* files touched; no commits.

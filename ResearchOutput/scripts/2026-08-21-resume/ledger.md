# Ledger entry — Round-68 / Experiment 541 "TDIAL-U104" (2026-08-22)

**Question.** Does the zero-fit dial's fade at the bitlen-100 frontier
(pooled Spearman 0.5436, CI [0.4982, 0.5881]; TDIAL-U100-FADES-AT-100 — first
cell below the validated band [0.55, 0.85]) CONTINUE at bitlen 104
(pre-stated H1: pooled < 0.53) or STABILIZE (pre-stated H2: pooled >= 0.53)?

**Design note / brief correction (made BEFORE any data generation).** The
tasking brief specified factor ranges "p in [2^16,2^22), q in [2^22,2^28)".
Those ranges cap N < 2^50 and are mathematically incompatible with the same
brief's binding constraint bitlen(N) = 104 (rejection sampling would accept
nothing). Corrected pre-data to the established TDIAL ladder windows — width-6
octave ranges meeting at 2^(B/2), as in exp536..540 (bitlen 96:
[2^42,2^48)x[2^48,2^54); bitlen 100: [2^44,2^50)x[2^50,2^56)) — giving
[2^46,2^52) x [2^52,2^58) for bitlen 104. Everything else verbatim
exp540/TDIAL-U100 methodology, including the exp540-FIXED own-bound smoothness
classifier and its independent Pollard-rho(Brent) spot-check (asserted
mismatch-free per seed).

**Pre-stated hypotheses (recorded before any data; result.json stage 00).**
- H1: fade CONTINUES at bitlen 104 — pooled Spearman(T, relation rate) < 0.53.
- H2: fade STABILIZES — pooled Spearman(T, relation rate) >= 0.53.

**Design.**
- Population: 1200 uniform semiprimes = 3 seeds x 400 (seeds 20261210-12);
  p uniform prime in [2^46, 2^52), q uniform prime in [2^52, 2^58),
  rejection-sampled to bitlen(N) = 104 exactly.
- Relations: per N, 240 values V = (r+d)^2 - N, r = isqrt(N), d uniform
  distinct in [1, 256].
- Smoothness (exp540-fixed classifier): per-N bound B_N = ceil(Vmax^(1/2.5))
  so u = ln(Vmax)/ln(B_N) = 2.5 exactly; V smooth iff every prime factor
  (2 included) <= B_N; EXACT vectorized trial division restricted per-row to
  its own bound (BVlive >= p mask + expiry parking); PLUS independent
  Pollard-rho(Brent) spot-check on a fixed 300-value subsample per seed
  (asserted mismatch-free in-script).
- Features verbatim paper-164: T(N) = sum 2/p (odd QR p <= 400); cnt(N) =
  #QR odd primes <= 100.
- Stats: per-seed + pooled (n=1200) Spearman, bootstrap CIs (300 resamples,
  seed 20260822), paired bootstrap CI on the advantage.
- Runtime only: per-seed rate computation parallelized across a 3-worker
  process pool (deterministic per-tag RNG; identical numbers to sequential).

**Results (all three seed spot-checks 300/300 clean vs Pollard-rho full
factorization; wall 408 s).**
- Pooled (n=1200): rho(T, rate) = **0.5005**, CI95 [0.4557, 0.5454].
  Ladder: 0.5739 (bitlen 96, fixed classifier) -> 0.5436 (100) -> 0.5005
  (104): delta -0.0431 vs bitlen 100 — the fade CONTINUES, near-linear
  (-0.0303 then -0.0431 per 4-bit step).
- Per-seed rho(T): 0.4927 / 0.4993 / 0.5089 — all three below the 0.53
  threshold AND below every prior cell; no outlier seed.
- Baseline: rho(cnt) = 0.3748, CI [0.3182, 0.4240] (was 0.4461 at 100).
- Advantage rho(T) - rho(cnt) = **+0.1257**, paired CI [+0.0821, +0.1686];
  per-seed +0.1294 / +0.0779 / +0.1653. NOTE: the dial's RELATIVE edge over
  count WIDENED (+0.1257 vs +0.0975 at 100) because cnt degrades faster than
  T even as T's absolute channel fades.
- Rates: mean 0.1365 +- 0.0274; 39324/288000 relation values smooth;
  B_N range [19254386, 22123851]. T mean 1.5658, range [0.532, 2.747];
  cnt mean 11.95 of 25 primes <= 100. Population acceptance 3.3-3.6%.

**Verdicts.**
- H1 PASS (pooled point 0.5005 < 0.53; all three seeds also < 0.53; bootstrap
  CI straddles 0.53, [0.4557, 0.5454]).
- H2 FAIL (the complementary stabilization clause).
- VERDICT-NAME: **TDIAL-U104-CONTINUES-FADE**.

**Barriers.**
- (5) SCOPE: claims restricted to uniform semiprime draws at bitlen exactly
  104, u = 2.5, and this relation-value construction ((r+d)^2-N, d in
  [1,256]); no claim about structured N, neighbouring bitlens, or a
  production sieve.
- (8) MEASUREMENT: rate is a 240-sample smoothness proxy (binomial sigma
  ~= 0.03), not a sieved relation yield; T and cnt scored against IDENTICAL
  values so the paired advantage is internally controlled; u-referencing is
  per-N max-value based (definition-dependence). Classifier is the
  spot-check-asserted exp540-fixed one. DESIGN NOTE: the brief's literal
  factor ranges were internally contradictory (cap N < 2^50 vs required
  bitlen 104) and were corrected pre-data to the ladder-consistent windows;
  recorded here so the cell is auditable against the brief.

**Decision.** The fade is REAL and MONOTONE through bitlen 104
(0.5739 -> 0.5436 -> 0.5005; every seed in every fading cell below the cell
above), with no stabilization plateau at 104: treat the zero-fit dial T as
VALID-BUT-DECAYING, now ~0.07 bits-of-rank below its 96-bit calibration and
outside the validated band [0.55, 0.85] for a second consecutive cell.
The dial still dominates count<=100 everywhere (advantage +0.1257, CI lower
bound +0.0821 > +0.05), so it remains the best cheap prior — but at the
current near-linear rate (~ -0.037/4 bits) it would cross rho ~ 0.40 around
bitlen 112-116. Next cell should be bitlen 108 to test linearity vs
acceleration of the fade, and/or a widened dial (more QR primes) to test
whether capacity recovers the band; both are cheap at this scale.

**Caveats.** (i) Bootstrap CI straddles the pre-stated 0.53 threshold
([0.4557, 0.5454]) — H1's pass is on the point estimate, not CI-separated;
the all-seed consistency (3/3 < 0.53) is the stronger evidence. (ii) The
brief's literal factor ranges were internally contradictory (cap N < 2^50 vs
required bitlen(N) = 104) and were corrected pre-data to the ladder-consistent
windows [2^46,2^52) x [2^52,2^58); recorded in result.json stage 00 and under
barrier (8) for auditability. (iii) Rate remains a 240-sample smoothness proxy
at u = 2.5 with per-N max-value referencing, not a sieved yield.

**Artifacts.** /tmp/exp68_tu104/{exp541_t_dial_unif_104.py, result.json,
run.log, population.txt, features.npz, rate_seed{0,1,2}.npy,
smooth_seed{0,1,2}.npy}

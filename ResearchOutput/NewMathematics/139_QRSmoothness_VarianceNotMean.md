# Paper 139 — QR-SMOOTHNESS: The QR Bite Is Variance, Not Mean

**Verdict name: THE-QR-BITE-IS-VARIANCE (paper 136's mean-shift story retired).**
Round-39 #1 (cron iteration) · exp 471 · assessment v248 · script `ResearchOutput/scripts/2026-08-21-resume/exp471_qr_smoothness.py` (+ `exp471_result.json`) · seed 20260821.

## 1. Paper 136's queued question, answered against its own post-hoc story

Paper 136 observed QS relation yields at 0.54–0.76 of the ρ(u)×0.90 model and post-hoc
blamed the quadratic-residue restriction: primes dividing x²−N must have (N|p) = +1, so the
relation pool draws on ~half the primes, "raising effective-u by lnB/(lnB−ln2)". This
experiment tests that directly at 2500 Ns per cell (100,000 relation values per cell,
bitlen N ∈ {40, 44}, u(median v) ∈ {2.5, 3.5}).

## 2. Results

**(a) Ensemble: the QR restriction carries NO penalty.** x²−N smoothness equals
UNRESTRICTED-random smoothness at every cell (emp_x2 0.12673 vs emp_rnd 0.12754; 0.01966 vs
0.01948; 0.12855 vs 0.12664; 0.02015 vs 0.01915), sitting at 0.871–0.985 of mean-ρ — exactly
paper 130's finite-x factor. Mechanism: a prime p with (N|p) = +1 divides x²−N for TWO
residue classes of x mod p (double the random-integer rate) on the halved pool — the two
effects compensate, quantifying the classical QS smoothness heuristic. The pre-stated H1
(x²−N matches QR-pool-restricted randoms) is REFUTED SPECTACULARLY: random integers judged
over the QR pool alone run 21–56× LOWER (a single small non-residue prime excludes its
entire divisibility class). Paper 136's effective-u story is retired.

**(b) Per-N variance is the real mechanism.** Correlation of per-N smooth rate with
#{odd primes ≤ 100 that are QRs of N}: 0.504 / 0.452 / 0.483 / 0.401 across the four cells.
Decile spread: 0.077 vs 0.188 at u=2.5 (2.4×); 0.0047 vs 0.0441 at u=3.5 (9.3×). A FIXED N's
relation yield swings enormously with whether 3, 5, 7, … happen to be residues of it —
while the ensemble mean stays pinned at the unrestricted value.

**(c) Resolves paper 136's anomaly.** Exp 470 used ONE N per scale: its yield ratios
0.54–0.76 were a sample of this per-N variance, not a systematic deficit. The QS cost model
correction: use ρ(u) × (finite-x factor ≈ 0.87–0.93) for the ENSEMBLE; for a SPECIFIC N,
adjust by its small-prime QR pattern — cheaply computable a priori from ~20 Euler-criterion
tests.

## 3. What this decides

The relation-pool statistics are now fully characterized: ensemble-random-equivalent with an
explicit finite-x factor, per-N rates governed by the small-prime QR pattern with measured
decile spreads. Barrier lines: (8) QS calibration continues to measure the known method;
(5) the per-N QR pattern is a residue dial — it predicts SIEVE YIELD (the method's own
input statistics), not factor information.

Method ledger: legendre_symbol arguments swapped (sympy wants (a, p)); then p = 2 crash
(sympy demands odd primes — excluded explicitly); gmpy2 powmod Euler path added for the
per-N stage; ρ anchors validated as in exp 465.

Now 471 experiments. Assessment v248.

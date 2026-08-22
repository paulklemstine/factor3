# Paper 144 — PER-N-PREDICTOR-FULL: The Shape Transfers Perfectly; the Level Tracks Each Population

**Verdict name: PER-N-PREDICTOR-REPLICATED.**
Round-39 #6 (cron iteration) · exp 476 · assessment v253 · script `ResearchOutput/scripts/2026-08-21-resume/exp476_per_n_predictor_full.py` (+ `exp476_result.json`) · seed 20260827.

## 1. The full-scale version of paper 142

Superset of the lean validation: three scales (bitlen 40/44/48, 3000 Ns each, 60 relations/N),
weighted-feature branch, logistic cross-check, independent verification path.

## 2. Results

- **Base effect replicates at all three scales**: Pearson r(QR-count ≤ 100, per-N rate) =
  0.514/0.521/0.497 at u=2.5 and 0.463/0.446/0.431 at u=3.5 — inside paper 139's claimed band.
- **H1 CONFIRMED**: scale-40 test R² = 0.3041, calibration slope 1.128 (u=2.5); R² = 0.2525,
  slope 1.100 (u=3.5) — both bands pass here (the lean version's hair-width misses were
  population-construction and split-protocol differences, disclosed on both sides).
- **Transfer shape PERFECT**: transfer R² equals the target scale's own correlation squared
  almost exactly (0.5214² = 0.2719 vs measured 0.2717 at k=44) — the predictor's shape carries
  over intact; its R² level simply tracks each population's own correlation. Calibration slopes
  in-band in 4/4 transfer cells.
- **Weighted feature NULL**: Σ log p over QR primes ≤ 200 lifts R² by only +0.009 (collinear
  with the count) — dropped.
- **Floor attribution**: residual variance = 1.31× the 60-draw binomial floor at u=2.5
  (genuine per-N structure beyond QR-count remains there — the honest target for richer
  features at higher relation counts) and 1.05× at u=3.5 (noise-bound; at the ceiling).

## 3. What this decides

The per-N yield dial is validated end-to-end: rate(N) ≈ −0.0035 + 0.01156·QR(≤100), calibrated
at scale, shape-transferring across bitlen 40→48, with its residual decomposed into sampling
noise (dominant at u=3.5) and a measured 31%-above-floor structure at u=2.5. Practical form
for QS calibration: candidate triage by ~20 Euler-criterion tests. Barriers: (5) residue dial
predicting a METHOD'S input statistics — zero factor information; (8) calibration context.

Method ledger: sympy.factorint hung on the verification path — replaced by the primorial-gcd
identity + pure-pow Euler checks (108 smoothness classifications, 4 QR counts PASS); OLS
primary and weighted-IRLS logistic secondary agree (R² 0.3041/0.3011).

Now 476 experiments. Assessment v253.

# Paper 140 — QR-REPLICATION: The Variance Law Is Seed-Robust

**Verdict name: SEED-ROBUST (paper 139 stands without qualification).**
Round-39 #2 (cron iteration) · exp 475 · assessment v249 · script `ResearchOutput/scripts/2026-08-21-resume/exp475_qr_replication.py` (+ `exp475_result.json`) · seed 20260826.

## 1. Fresh-seed audit, one firing after a seed-luck embarrassment

Paper 136's yield anomaly was recently traced to single-N seed luck (corrected by paper 139).
The audit discipline (papers 97/103) applied to paper 139 itself: identical design, fresh seed
20260826 (original: 20260821), four cells × 100,000 values.

## 2. Results

**Ensemble equality replicates**: emp_x2 vs emp_rnd = 0.12859/0.12786, 0.02004/0.02023,
0.12854/0.12585, 0.02004/0.01869 — x²−N ≈ unrestricted random at every cell;
QR-restricted randoms 32–200× lower (as before).

**Per-N correlation replicates**: corr(per-N smooth rate, QR-count of odd primes ≤ 100)
= 0.503 / 0.415 / 0.480 / 0.403 vs the original 0.504 / 0.452 / 0.483 / 0.401 — max drift
0.037. Decile spreads replicate (low/high): 0.076–0.082 / 0.186–0.188 at u=2.5;
0.006–0.008 / 0.039–0.043 at u=3.5.

## 3. Verdict

THE-QR-BITE-IS-VARIANCE is seed-robust: ensemble-random-equivalence with per-N rates
governed by the small-prime QR pattern stands without qualification. The per-N yield
predictor's training target (paper 139 → exp 472's in-flight validation) is a stable object.

Now 472 experiments. Assessment v249.

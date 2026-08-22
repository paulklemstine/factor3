# Paper 189 — TDIAL-U88: The Dial Drops Below the Floor at Bitlen 88

**Verdict name: DRIFT-INCONCLUSIVE (pooled 0.534 below 0.55 for the first time; CI straddles).**
Round-68 #1 (cron iteration) · exp 536 · assessment v287 · script `ResearchOutput/scripts/2026-08-21-resume/exp536_t_dial_unif_88.py` (+ `exp536_result.json`, `LEDGER.md`) · seeds 20261200–02.

## 1. The first band-miss

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 tested on uniform draws at bitlen
88 — the pooled Spearman drops below the 0.55 floor for the first time.

## 2. Results

| seed | Spearman(T, rate) | CI95 |
|---|---|---|
| 20261200 | **0.516** [0.474, 0.562] | below floor |
| 20261201 | **0.555** [0.512, 0.589] | straddles |
| 20261102 | **0.532** [0.490, 0.574] | below floor |
| pooled | **0.534** [0.509, 0.555] | straddles |

H1 band-miss: pooled below 0.55; only 1/3 seeds above floor. H2 PASS: T beats count by
+0.059 CI [0.032, 0.083]. Ladder: 0.78 (44) → ~0.81 (52) → ~0.69 (56) → ~0.65 (64) →
~0.61 (68) → ~0.61 (72) → ~0.61 (76) → ~0.57 (80) → ~0.56 (84) → **~0.53 (88)**.

## 3. What this decides

The dial's signal degrades through the floor at bitlen 88 — the first band-miss in the
uniform-ladder series. DRIFT-INCONCLUSIVE: the CI straddles the floor, so this cell alone
cannot separate continued slow drift from noise around a plateau. Barriers: (5)/(8)
unchanged.

Now 537 experiments. Assessment v287.

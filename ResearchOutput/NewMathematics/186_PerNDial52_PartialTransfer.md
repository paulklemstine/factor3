# Paper 186 — PERNDIAL-48-52: The Per-N Dial Transfers to Bitlen 52 with Partial Degradation

**Verdict name: PERNDIAL-52-PARTIAL-TRANSFER (H2 pass; H1/H3 marginal).**
Round-60 #2 (cron iteration) · exp 541 · assessment v294 · script `ResearchOutput/scripts/2026-08-21-resume/exp541_perndial_48_52.py` (+ `exp541_result.json`) · seeds 20261200–02.

## 1. Completing the transfer validation

The per-N yield dial tested for transfer from bitlen 44 (training) to bitlen 52 (test),
with the full augmented feature set.

## 2. Results

| metric | value | verdict |
|---|---|---|
| transfer slope (bitlen 52) | **0.811** | H2 PASS (in [0.8, 1.25]) |
| R² at bitlen 52 | 0.405 | below 0.45 target |
| pp_sum increment | +0.018 CI [0.011, 0.023] | just under +0.02 bar |

## 3. What this decides

The dial transfers with in-band calibration slope but absolute R² degrades at higher
bitlen — consistent with the sampling-noise floor rising as values grow larger relative
to B. Barriers: (5)/(8) unchanged.

Now 528 experiments. Assessment v294.

# Paper 190 — TDIAL-U64B: Fresh-Seed Replication Confirms the Dial at Bitlen 64

**Verdict name: U64B-DIAL-HOLDS-COUNT-PARITY (H1 pass; H2 fail — count parity).**
Round-68 #3 (cron iteration) · exp 543 · assessment v298 · script `ResearchOutput/scripts/2026-08-21-resume/exp543_t_dial_unif_64.py` (+ `exp543_result.json`) · seeds 20261210–12.

## 1. Fresh-seed replication of paper 184's bitlen-64 uniform cell

1200 uniform semiprimes at bitlen 64 × 3 seeds; T and count features; smoothness u=2.5.

## 2. Results

| metric | value |
|---|---|
| pooled ρ(T, rate) | **0.641** [0.619, 0.660] — in band |
| pooled advantage over count | **+0.044** [0.022, 0.066] — below +0.05 bar |
| per-seed advantage > +0.05 | 1/3 |

Six-seed combined (with paper 184): ρT mean **0.644**, advantage mean +0.059 / median
+0.058, only 3/6 above the bar.

## 3. What this decides

The bitlen-64 zero-fit dial law replicates cleanly on fresh uniform seeds and H1 stands,
but H2's point estimate flips below the bar — record the T-over-count advantage at
bitlen 64 as MARGINAL/count-parity, a clear decay from bitlen 56's solid margin.
Barriers: (5)/(8) unchanged.

Now 528 experiments. Assessment v298.

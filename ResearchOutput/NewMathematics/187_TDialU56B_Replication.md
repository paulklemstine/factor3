# Paper 187 — TDIAL-U56B: Fresh-Seed Replication Confirms Validity but Edge Not Established

**Verdict name: U56B-DIAL-HOLDS-COUNT-PARITY (H1 pass; H2 fail — edge not established).**
Round-61 #2 (cron iteration) · exp 542 · assessment v296 · script `ResearchOutput/scripts/2026-08-21-resume/exp542_t_dial_unif_56.py` (+ `exp542_result.json`) · seeds 20261140–42.

## 1. Fresh-seed replication of paper 184's bitlen-56 uniform cell

1200 uniform semiprimes at bitlen 56 × 3 seeds; T and count features; smoothness u=2.5.

## 2. Results

| metric | value |
|---|---|
| pooled ρ(T, rate) | **0.669** [0.650, 0.690] — in band |
| pooled advantage over count | **+0.045** [0.021, 0.070] — below +0.05 bar |
| per-seed advantage > +0.05 | 1/3 |

The dial replicates (H1 pass) but its weighted edge is NOT ESTABLISHED at this cell.

## 3. What this decides

The zero-fit dial's validity replicates but the +0.05 edge over count should be treated
as NOT ESTABLISHED at bitlen 56 — count catches up in this batch. Barriers: (5)/(8)
unchanged.

Now 526 experiments. Assessment v296.

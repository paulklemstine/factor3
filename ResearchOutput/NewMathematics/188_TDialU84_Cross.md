# Paper 188 — TDIAL-U84-CROSS: Approaching but Not Yet Crossed

**Verdict name: APPROACHING-NOT-CROSSED (pooled 0.558, margin to floor +0.008).**
Round-67 #1 (cron iteration) · exp 535 · assessment v294 · script `ResearchOutput/scripts/2026-08-21-resume/exp535_t_dial_unif_84.py` (+ `exp535_result.json`) · seeds 20261190–92.

## 1. The crossing test paper 187 queued

Does Spearman(T, rate) drop decisively below 0.55 at bitlen 84 on uniform draws? Pooled = **0.558** [0.536, 0.581] — still above the floor by +0.008; per-seed 0.572/0.578/0.522.

## 2. Results

| seed | Spearman(T, rate) |
|---|---|
| 20261190 | **0.572** [0.542, 0.601] |
| 20261191 | **0.578** [0.550, 0.606] |
| 20261192 | **0.522** [0.491, 0.553] |

Pooled CI [0.536, 0.581]; margin to floor +0.008. The dial's signal degrades toward the
floor on a gradual erosion path, not a cliff.

## 3. What this decides

The dial does NOT drop decisively below 0.55 at bitlen 84 — the erosion is gradual.
Barriers: (5)/(8) unchanged.

Now 525 experiments. Assessment v294.

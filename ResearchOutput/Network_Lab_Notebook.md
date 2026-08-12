# Network/LLM Research Lab — Notebook

Programmatic exact-law experiments on neural networks and LLMs, in the same
rigorous style as the factoring lab. Each Part is one experiment of the
network research loop. Assessment file: Network_Assessment.md.

## Part 1 — SPECTRAL-QUANTIZATION (round-net-1 #1, network exp 1, v1, paper NET-1)

**The per-layer bit-need law b*(PR) holds exactly on a generalizing MLP and does NOT transfer to a tiny attention LM — a law with a documented domain.** Hypothesis (compression axis): a trained net's per-layer sensitivity to low-bit post-training quantization is governed by its weight participation ratio PR = (Σσᵢ²)²/Σσᵢ⁴ (effective rank), giving (1) a monotone minimal-bits b*(layer) function of PR, (2) corr(PR, damage) strongly negative, (3) PR-proportional equal-budget allocation beating uniform. Experiment (CPU, PyTorch 2.3.1): two models chosen to GENERALIZE reliably (no grokking) — a 5-layer MLP on a smooth 2D classification task (sin·cos boundary, 30k pts, 70/30 split) and a 2-layer transformer LM (d=48, d_mlp=64, 4 heads) on next-token prediction of a 2nd-order deterministic automaton (25-state rule, 25% held-out sequences) — 3 seeds each; per-layer RTN (round-to-nearest per-row symmetric) quantization at 2/3/4/6 bits with held-out test retention.

**MLP (5 layers, 3 seeds):** bit-need b* is a monotone step of PR — the high-rank bottleneck (PR≈5.4) needs 6 bits in EVERY seed, the rank-1 readout (PR=1.0) needs 2 bits in EVERY seed, mid-rank layers sit between; corr(PR, 3-bit damage) = −0.80/−0.92/−0.90 (mean −0.875); corr(PR, b*) = +0.87/+0.58/+0.94 (mean +0.80). PR-proportional allocation (floor 3 bits) beats uniform-4 at an equal total-bit budget on 2/3 seeds (+2.9/+3.5 pp, and −96/−1120 bits; seed-2 overshoots budget ~8% for +2.1 pp — reported).

**Transformer LM (2 layers, 3 seeds, test 1.0000 — perfectly generalizing):** the law REVERSES — every interior matrix (PR 12–25) is robust at 2 bits (b*=2), while the LOW-PR input embeddings (embed PR 4.4, pos PR 9.4) are the fragile layers (b*=3). Mechanism: per-row RTN at 2 bits has 1 level, collapsing the 5-row embedding to ±max sign patterns. Joint quantization compounds: uniform-2 fails (0.887/0.912/0.589), uniform-3 is essentially lossless (0.996/1.000/0.982) — per-layer isolated sensitivity undercounts joint damage (measurement caveat, barrier f).

**Verdict.** CONFIRMED within class (MLP: exact monotone b*(PR), data-free PR sensitivity estimate, equal-budget allocation win); REFUTED as a blanket transfer (transformer embedding fragility reverses the ordering). New objects: the monotone b*(PR) law, the data-free PR sensitivity estimate, the equal-budget allocation win, and the documented domain boundary + joint-vs-isolated compounding. Barriers (b) acknowledged (sensitivity-based mixed precision is a known family — HAWQ/OBS/GPTQ; the PR-only data-free law and the domain reversal are new), (c) toy-scale acknowledged — real-scale (small BERT) is the next step, (d) clean held-out, (e) 3 seeds × 2 classes, (f) joint-compounding documented, (g) equal-bit budgets (1 overshoot reported), (h) +2–3.5 pp at equal budget on MLP, no win on toy LM.
Now 1 network experiment. Assessment v1. Paper NET-1, issue #96.
Script: /tmp/exp_net_quant.py.

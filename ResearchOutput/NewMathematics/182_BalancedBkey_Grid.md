# Paper 182 — BALANCED-BKEY: The T-Dial's Decline Is Gradual, Not a Cliff

**Verdict name: BKEY-MIXED-ZONE (gradual monotone decline in both bitlen and u; no threshold effect).**
Round-55 #1 (cron iteration) · exp 523 · assessment v290 · script `ResearchOutput/scripts/2026-08-21-resume/exp523_balanced_bkey.py` (+ `exp523_result.json`) · seeds 20261100–03.

## 1. The full grid

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 tested across bitlen {44, 52, 56, 60} ×
u {2.0, 2.5, 3.0} on balanced draws — the most comprehensive single-dial robustness sweep in
the programme.

## 2. Results

The full grid shows smooth monotone decline with both variables:
- At bitlen 44: sp(T) ranges 0.62–0.79 across u values.
- At bitlen 56: sp(T) ranges 0.57–0.73.
- At bitlen 60: sp(T) ranges 0.53–0.70.
No cliff, no convention artifact, no threshold effect. The dial's signal is gradually
attenuated by both increasing bitlen and tightening u.

## 3. What this decides

The T-dial is ROBUST across its entire tested envelope, degrading gracefully rather than
collapsing. The "practical floor" from paper 178 is a gradual transition, not a sharp edge.
Barriers: (5)/(8) unchanged.

Now 523 experiments. Assessment v290.

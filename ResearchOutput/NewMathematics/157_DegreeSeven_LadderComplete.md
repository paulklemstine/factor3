# Paper 157 — DEGREE-SEVEN: The Ladder's Last Gap Below Ten

**Verdict name: FULL-PINNING-AT-DEGREE-SEVEN.**
Round-42 #3 (cron iteration) · exp 489 · assessment v266 · script `ResearchOutput/scripts/2026-08-21-resume/exp489_degree_seven.py` (+ `exp489_result.json`) · seed 20260923.

## 1. The cyclic degree-7 subfield of Q(ζ₂₉)

Conductor 29 (φ = 28 = 4·7); Gal = C₂₈/⟨g⁷⟩ ≅ C₇. Pre-stated: T(p) = 1 iff
dlog_g(p) ≡ 0 mod 7, else 7; densities {4/28, 24/28} = {1/7, 6/7}; H(T) = H(1/7, 6/7) =
0.5917 bits.

## 2. Results

295k primes: densities exact, **FULL PINNING** — I(p mod 29; T) = H(T) = 0.5917 EXACTLY
(empirical 0.5914, per-class degenerate, perm-null clean); thickening structural; coprime
control flat. Semiprime (30k): pair channel 0.0112 vs exact enumeration law 0.0111;
Is(7)-projection 0.1161 matching the Bin(2, 1/7) closed form.

LEDGER disclosure: the coordinator-supplied anchor "Is(7) = 0.0103" was actually **G(7)**
(the OR-channel value from paper 72's decay table), not Is(7) — the measurement itself
exposed the mislabel by landing at 0.116.

Now 489 experiments. Assessment v266.

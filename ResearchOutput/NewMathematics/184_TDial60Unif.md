# Paper 184 — T-DIAL-60-UNIF: The Dial Survives Uniform Draws at Bitlen 60

**Verdict name: CELL-CLOSED-DIAL-HOLDS-60 (H1/H2 both pass).**
Round-51 #3 (cron iteration) · exp 521 · assessment v287 · script `ResearchOutput/scripts/2026-08-21-resume/exp521_t_dial_60_unif.py` (+ `exp521_result.json`) · seed 20261050.

## 1. The last untested intersection

The zero-fit dial T(N) = Σ 2/p over QR primes p ≤ 400 tested on uniform draws at bitlen
60 — the highest bitlen × regime combination yet measured.

## 2. Results

| metric | value |
|---|---|
| Spearman(T, rate) | **0.669** [0.634, 0.705] — inside [0.55, 0.85] |
| Spearman(count ≤100, rate) | 0.517 [0.472, 0.552] |
| T advantage | **+0.151** [0.107, 0.193] |

All three seeds inside the band; H1/H2 confirmed.

## 3. What this decides

The zero-fit dial survives uniform draws at bitlen 60 — its deployment envelope now covers
balanced and uniform draws through bitlen 60. Barriers: (5)/(8) unchanged.

Now 522 experiments. Assessment v287.

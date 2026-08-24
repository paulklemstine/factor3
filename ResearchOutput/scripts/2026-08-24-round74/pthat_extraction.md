# pthat_extraction — raw P̂ re-extraction for paper 225's erratum action (a)

Sources: `2026-08-21-resume/exp467_positional_filter.py` + `/tmp/exp38_positional/result.json`
(paper 137 raw), `exp474_et_hints.py` + `exp474_result.json` (paper 143 raw); papers 137/143/219/225;
`gapL4_result.json` §A1; `verifyL4_verdict.md`. No recorded file modified.

## Headline: NO hits/trials exist in any artifact

- exp467: orderings are full REORDERINGS of the candidate list (no committed window R);
  result stores per-ordering/per-stratum mean costs only — no hit indicator, no window counts.
- exp474: EXACT enumeration (M=300) under a DESIGNED oracle contract "interval covers J w.p. α"
  — P_hit ≡ α by construction (= **1.000000 exactly** at the 29.1× cell); no sampling, no trials.
- All four booked P̂ are DRAFTED-law inversions of speedups (raw or rounded), recovered here to ≤2e-4.

## Raw cells → full precision

| anchor | raw cell (source) | S_meas | P̂ booked | P̂ cert-law-implied | P̂ drafted-inv | S_A@booked | p225 printed |
|---|---|---|---|---|---|---|---|
| 5.19× frontier | asc 6441.7067 / trunc_desc 1240.3181667, n=30000, s20260821 | 5.193592154916 | 0.8500 | 0.841617 | 0.849953 (raw) | 5.405405405… | 5.4054 |
| 6.91× trunc-high | stratum r∈[2,4]: 4524.2355344/654.2900603, n=6732 | 6.914724537168 | 0.9003 | 0.894868 | 0.900297 (@rounded 6.91) | 7.156659271 | 7.1567 |
| 4.35× trunc-low | stratum r∈[1,1.25): 8021.1223969/1842.6333534, n=9651 | 4.353075657862 | 0.8106 | 0.800308 | 0.810643 (@rounded 4.35) | 4.535970244 | 4.536 |
| 29.1× α=1 | exact enum M=300 μ=6 α=1: E_base 100.500555556/E_committed 3.450611111 | 29.125436718134 | 0.9853 | **0.985068** | 0.985373 (raw) / 0.985343 (@rounded 29.1) | 29.315196998 | 29.3152 |

S_A = 1/[μP̂+(1−P̂)(1−μ)], μ=0.05 (rows 1–3), 0.02 (row 4); P̂_implied = [(1−μ) − 1/S]/(1−2μ).

## Verdicts

- **Arithmetic**: paper 225's corrected column is EXACT at the booked loci — all four recomputed
  values match to ≥6 decimals (5.405405, 7.156659, 4.535970, 29.315197).
- **Feasibility**: intact at full precision. μ ≤ 1/S_raw true ×4 (0.05≤0.1925/0.1446/0.2297; 0.02≤0.03433);
  S_A@booked ≥ S_raw true ×4 (margins +0.212/+0.242/+0.183/+0.190).
- **Premise fails**: "stored P̂=0.9853" does not exist. The 29.1× cell's design value is α=1 exactly;
  the certified-law-consistent P̂ at full precision is 0.985068 (p225's own 0.98504 used the ROUNDED 29.1;
  true input 29.125437 shifts it by +3.1e-5). Booked 0.9853 overstates by ~2.3e-4 → 29.3152 overstates the
  certified reading by ~0.19. Same provenance caveat for rows 1–3 (inverted witnesses, ±2e-4 spread).
- Note: exp474's committed protocol pays the miss branch (interval scanned even on miss), matching NEITHER
  pure protocol-A nor the drafted form — the (μ,P̂) mapping is an effective convention, per p225's own F1/F3 lesson.
- Recommendation: book all four anchors "at resolution limit" per p225's admissibility rule (raw-P̂ stored = NOT met);
  corrected table stands as arithmetic, loci carry inversion provenance.

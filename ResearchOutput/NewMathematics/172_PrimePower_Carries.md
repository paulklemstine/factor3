# Paper 172 — MID-PRIME-HUNT: Prime-Power Hits Carry the Tight-u Residual

**Verdict name: PRIME-POWER-CARRIES (H1/H2 fail; H3's alternative confirmed decisively).**
Round-46 #1 (cron iteration) · exp 505 · assessment v280 · script `ResearchOutput/scripts/2026-08-21-resume/exp505_mid_prime_hunt.py` (+ `exp505_result.json`) · seed 20260927.

## 1. Hunting the tight-u residual directly

Paper 170's open question: what carries the ~0.064 Spearman drop at u=3.5 that small-prime
reweighting cannot recover? Three candidates tested with nested-model bootstrap CIs:
mid-prime hit fractions (31–97), QR-density terms, and prime-power hits (p² | v_j).

## 2. Results

| feature increment | ΔR² [95% CI] | verdict |
|---|---|---|
| + mid n_p (31..97) | +0.019 [−0.017, +0.031] | H1 FAIL |
| + PC1 of mid block | +0.0002 [−0.006, +0.003] | — |
| + QR-density ρ_mid linear/squared | +0.004 / +0.0005 | H2 FAIL |
| **+ prime-power hits (p² | v_j, p ≤ 13)** | **+0.0892 [+0.041, +0.125]** | **DECISIVE** |

The tight-u residual is carried by SQUAREFULL divisibility: at smaller B, a value with p² | v
has its smoothness budget disproportionately consumed by small-prime powers — structure that
marginal squarefree-hit features cannot see. The per-N dial gains a prime-power term.

## 3. What this decides

The residual-hunt arc (papers 167–172) closes constructively: the tight-u content exists,
is real (+0.089 CI-excluded-zero), and is captured by prime-power divisibility — completing
the dial's final form as {footprint mass w, divisibility fraction d, prime-power hits}.
Barriers: (5)/(8) unchanged.

Now 505 experiments. Assessment v280.

# Paper 194 — ASCENT-COST: The Exact Economics of Berggren Branch Oracles

**Verdict name: ASCENT-COST-LAW (effective-branching REFUTED — base pinned at 3; master-law mapping REFUTED — sequential hints compound).**
Round-70 #3 · exp 547 · assessment v301 · script `ResearchOutput/scripts/2026-08-21-resume/exp547_ascent_cost.py` (+ `exp547_result.json`, `run.log`) · seed 20260823.

## 1. Setup

2500 odd semiprimes (1875 main p∈[2^13,2^17]/q∈[2^15,2^21]; 625 balanced q/p∈[1.0001,1.01]).
Search semantics DISCLOSED: end-verification-only (no cheap ancestor test exists in
factoring terms); oracle names the correct branch w.p. α else uniform among wrong
untried; cost = node entries, backtracks free. Validations asserted: re-ascent exact
2500/2500; α=1 gives exactly dB steps; MC vs closed form <2% on every α×h cell;
slope(log E, dB)=ln3 to 6 decimals for every α<1.

## 2. Two exact cost laws

- **DFS-with-backtrack:** E[visits] = h·(1−K/2) + K·(3^(h+1)−3)/4, K=(1−α)(2−α).
- **Restart-from-root:** E[visits] = h·α^(−h) — dominates DFS in **99.0%** of
  (α, instance) cells (a wrong subtree costs ~3^h/2 to exhaust; a failed restart only h).
- Beam search never wins (w8 strictly dominated by w2; P(success) only 3.5%/3.9% at
  α=0.9, median dB≈50; astronomically dead below).

**Effective branching REFUTED:** the rate base stays pinned at exactly 3 for EVERY
α<1 — accuracy enters only through the prefactor K(α); "effective branching b(α)<3"
exists solely as the α→1 exponential-to-polynomial PHASE TRANSITION.

## 3. The breakeven phase diagram

Against BLIND tree search any α>1/3 wins trivially. Against the EXACT Fermat scan
(median 183k steps here):

| constraint | value |
|---|---|
| majority-win region survives to | **c ≤ 3000** visit-equivalents per step |
| α\* at c=0 → c=3000 | 0.85 → 0.96 |
| balanced stratum | NEVER wins at any (α,c) — Fermat already costs 1–100s of steps |
| deep-dB tail | unwinnable even at α=0.9999 — the depth TAIL governs feasibility |
| known-dB sensitivity (α=0.9) | assuming a 1.5×/2× depth bound raises median cost ×20/×280 |

**Barrier-8 honesty probe (computed):** wins require c≤3000; a √N-costing per-step
feature (~10^5.2 ops here) is excluded by only ~1.7 orders of magnitude — a spectrum-style
feature at √N cost IS Fermat-in-disguise, and the margin is thin because the skewed
stratum's Fermat cost is huge.

## 4. Master-law mapping REFUTED — a new hint type

Paper 138's class-hint law Speedup=1/(1−(1−θ)P_hit) saturates at its cap 1/θ=3. The
empirical branch-oracle speedup DIVERGES: **1.01 / 1.30 / 1.98 / 3.56 / 10.10** at
α = 1/3 / 0.45 / 0.6 / 0.75 / 0.9 (medians). Branch hints compound sequentially — joint
path success α^dB — a phase-changing, qualitatively stronger value type than one-shot
class hints. NEW ENTRY in the hint taxonomy: **sequential/geometric hints**, priced by
E = h·α^(−h), not by the master law.

## 5. Snaps together with exp546

The measured magnitude channel (paper 193: ~19% of b₁ entropy; raw-b₁ OOS accuracy
only matches the majority baseline) sits FAR BELOW the breakeven α* ≥ 0.85 — the
channel exists but buys no ascent win today; the gap is now quantified from both ends.

## 6. dB distribution and a stratum-dependent reversal

All: mean 442, median 50, range [14, 8469] (balanced design forces ρ≥201, depth =
heavy-tailed sum of Gauss-map partial quotients). Main-only: mean 59.6, median 39,
max 2600; balanced: median 971. **Spearman(dB, Fermat-steps) = −0.364 pooled but
+0.443 within the main stratum** — exp 391's anti-correlation claim is STRATUM-
DEPENDENT, not universal (ledger).

Ledger: agent's result JSON left `status:"running"` post-completion (wall clock +
validation blocks confirm final — disclosed, not edited); path-reversal smoke bug
caught by assert V1; float64 overflow at dB~4000 forced full log10 accounting;
log-sum-exp correction found by analytic comparison. Barriers: 4/8 unchanged and now
priced for the tree stratum; hint taxonomy extended (sequential compounding class).

Now 547 experiments. Assessment v301.

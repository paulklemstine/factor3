# Paper 148 — ET-HINTS-FULL: The Hedging Hump and Placement-Structured Ceilings

**Verdict name: HEDGE-AND-CAPACITY.**
Round-40 #4 (cron iteration) · exp 481 · assessment v257 · proofs `ResearchOutput/scripts/2026-08-21-resume/exp481_proofs.md` (+ `exp481_verify.py`, `exp481_result.json`) · seed 20260824.

## 1. The third and deepest of three mutually-consistent interval-hint results

Paper 143 measured the grid (inline); paper 146 derived closed forms and the crossing law
(reduced agent); this paper — the original theory agent, completed after ~70 minutes of
channel-stalled work — adds the full theorem suite. All three agree where they overlap:
matching paper 137's 5.19× requires **narrow AND near-certain** coverage.

## 2. Theorems

- **T7 (HEDGING HUMP)**: E_opt(α) is concave piecewise-linear in α — intermediate trust can
  be WORSE than both endpoints AND than the no-hint baseline (measured: 196.09 vs baseline
  171.17 at M=512, x=1/4 right-placed POS, α=0.20). Partial trust is the most expensive regime.
- **T8 (placement-structured ceilings)**: the attainable cap is 2/(3x) for centered/uniform/
  left-placed windows but **→ 1/x for RIGHT-placed windows** — truncated w reproduces the
  min-of-two-uniforms law inside the interval, so A_in → μ/3. Placement doubles what width buys.
- **Calibration gate**: uniform-given-hit joints exist only at α ≤ μ(2(M−b)+1)/M² ≈ 2x(1−x)
  (left) or x/M → 0 (right) — that family can NEVER reach magnitude-ordering gains; POS is
  containment-calibrated yet unconstrained.
- Best measured cell: right-placed x = 1/16, α = 1 → **14.69×**, spending KL = log₂(1/W_in) =
  8 bits for log₂(sp) = 3.877.
- Crossing table for s = 5.19×: α* = 0.832 (x=1/64) → 0.904 (1/16) → 0.992 (1/8); POS-right
  systematically earlier.

## 3. Scope insight

Interval hints escape paper 138's 2×/dial which-factor ceiling because they act on ORDER via
direct J-correlation (barrier 2) while carrying MI(hint; factor) = 0 — the two functionals
price orthogonally, so pure-position hints dominate under E[T] yet stay factor-blind.
Fermat named precisely: "start at √N" commits to a rightmost interval whose CAL capacity
x/M → 0 — which is why it carries almost no exploitable coverage yet still wins on position.
Isolation-cost breakeven per oracle query = E_base − E_hint (negative inside the hump band).

Verification: exhaustive all-permutations M=5–8 (worst gap 1.3e-16); M=9 hump cells 31/31;
MC 200k × 40 configs × 3 procedures max |z| = 2.343.

Method ledger (7): complement-mass bug (Σ = 1+α) invisible to consistency checks — caught
only by MC z = −72, fixed by a Σ(π)==1 assert; Thm 8 refuted by own data and corrected to
placement-structured caps; two infra kills plus concurrent writers replaced deliverables
twice mid-run — all runs preserved and cross-referenced (`et_hints_*_canonical.*` vs
`*_reduced_alt_otherwriter.*`).

Now 480 experiments. Assessment v257.

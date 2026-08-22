# Paper 146 — ET-HINTS-THEORY: The Crossing Law — Width Can Never Substitute for Reliability

**Verdict name: HINT-COST-PRICED (closed forms; Bayes ≡ Committed proven; hard reliability gate).**
Round-40 #2 (cron iteration) · exp 480 · assessment v255 · proofs `ResearchOutput/scripts/2026-08-21-resume/exp480_proofs.md` (+ `exp480_verify.py`, `exp480_result.json`) · seed 20260828.

## 1. Paper 143's grid, promoted to closed form

The companion measurement paper (143) priced external interval hints on a numerical grid
under truthful conditioning. This paper derives the same object in closed form and adds
what a grid cannot: exact optimality, a proven crossing law, and a conservative-pricing bound.

## 2. Results

- **Closed forms** for baseline E_base = (M+1)(2M+1)/(6M), COMMITTED (window-first then
  complement ascending), and INTERLEAVED (rank lemma with two-sided min); closed = brute-force
  exact at M=300 under Fraction arithmetic (relgap 0.0); MC at M=10⁵ passes all 16 cells
  (max |z| = 1.52).
- **Bayes ≡ COMMITTED, proven**: the observed-window posterior is two-valued
  (q_in = α/μ vs q_out = (1−α)/(M−μ)); by the rearrangement inequality any optimal order puts
  the window first. Every hint-blind ordering costs exactly (M+1)/2 — the hint's entire value
  is the gap below that floor. INTERLEAVED is strictly dominated everywhere.
- **THE CROSSING LAW**: reaching speedup s requires α > α_min(s) = 1 − 2/(3s) — for the lab's
  measured magnitude gain s = 5.19×, the hard gate is **α > 0.87155 regardless of width**.
  Above the gate the crossing obeys the linear law **μ/M = α − 0.87155** (bisection:
  0.88 → 0.0085, 0.90 → 0.0285, 0.95 → 0.0785, 1.00 → 0.1285). Paper 137's magnitude-ordering
  therefore corresponds to effective interval quality (α ≈ 0.90, μ/M ≈ 0.028), matching
  exp 474's numerical estimate. **Width alone can never substitute for reliability.**
- **Conservative pricing**: under w-anchored conditioning (J keeps its true min-law rather
  than the brief's uniform clauses) speedups move UP (7.62× vs 5.56× at the same cell) —
  the stipulated pricing understates what a real oracle of stated quality would buy.

## 3. What this decides

The barrier map's fourth row now has its theorem: interval hints are priced by two numbers,
with a proven optimality identity, a hard reliability gate at α = 1 − 2/(3s), and a linear
width law above it. Barrier lines unchanged from paper 143 ((2) position escapes the
uniform-marginal lemma; (8) window-first near √N is Fermat).

Method ledger (7 machine-caught): V_A constant off-by-μ caught over 12 anchors; Bayes block
marginalized instead of conditioning (degenerated to (M+1)/2); enumeration compared mixed α's
(relgap 0.955 → recomputed per cell 0.0); plus four more, all in proofs.md.

Now 478 experiments. Assessment v255.

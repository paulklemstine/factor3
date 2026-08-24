# Paper 221 — GAP-L7 FALSIFICATION AND REPLACEMENT (L7′): Extremality of Sqrt-Descending Among N-Computable Reorders Is FALSE-IN-PRINCIPLE; Replaced by the Λ-Channel Mass-Sort Law (Window-Ascending Beats Descending 1.58×±0.03 Under Hard Balance, Sign Flips at E[√r]=1.1716) plus the Master Inequality S ≤ (4/3)·T1-cap/Λ — Finite-Verified at ZERO Violations Across Policy Arms × Four Pools

> **STATUS: PROVEN-SKETCH (L7′), FALSIFICATION COMPLETE (L7-as-drafted).** L7 of
> paper 219's roadmap is false as drafted — not under-refined, but wrong in
> principle: no population measure on lab generators makes sqrt-descending the
> extremal N-computable order. Its replacement is stated, checked, and carries an
> explicit load-bearing caveat (μ_eff booking). Every number below was independently
> re-derived (`verifyL7_sim_out.json`, n=2400/1600/500 across four pools, zero
> violations; `verifyL7_unif.py` for the uniform proxy).

**Verdict name: extremal order = POPULATION MASS-SORT, not sqrt-descending.**
Paper 219 left L7 open ("sqrt-descending maximizes S among all orders computable
from N alone, per stratum") as the formal home of paper 137's honest frontier.
The round-74 attempt to close it (`gapL7_extremality.md`) drafted the proof and its
own author-finite-checks returned figures that the INDEPENDENT verification set
showed to be sampling-inflated while confirming the falsification itself. Net
result: the conjecture dies, a sharper true statement replaces it, and one recorded
paper (137) is REFINED, not contradicted.

Round-76 #1 · THEORY deliverable (no new experiment id; experiment count unchanged
at 562 by papers-only convention, same convention as paper 219) · assessment v327→v328 ·
companion to paper 219 (barrier-4 positional converse: T1/T2/Conjecture D),
papers 132 (residue cap 4/3), 137/143 (position measured), 138 (class hints),
212/exp563 (adaptive magnitude), exp570 (early-fire trace law) · artifacts:
`gapL7_extremality.md` (post-revision), `gapL7_check.py` → `gapL7_result.json`
(author first pass, n=150/pop, 0.99 s), `verifyL7_sim.py` → `verifyL7_sim_out.json`
(independent verifier, re-derived from scratch, batch-bootstrap error bars),
`verifyL7_unif.py` (uniform-proxy cross-check) — all under
`ResearchOutput/scripts/2026-08-24-round74/`.

## 1. The action space, precisely (what "N-computable reorder" means)

Fix N odd composite, candidate space I(N) = {2..⌊√N⌋}, p = min-factor, baseline
σ₀ = sqrt-descending, touch = full divisibility test = 1 unit, skip pays 0 with its
keep-set T1-priced (μ = keep fraction); cheap predicates are paper-132 COST-class
at ε > 0 each.

**DEF (REORDER-class policy).** Π emits an enumeration a₁, a₂, … of I(N),
a_k = f(k,N), where f satisfies:

1. **UNIFORMITY**: one fixed computable f serves all N (no per-N hardcoding).
2. **TEST-BLINDNESS**: a_k independent of the outcomes of tests a_i|N for i < k —
   the order commits ex ante. Interleaved comparison queries ("p ≤ x?") are admitted
   only at T2 pricing (1 unit, truthful).
3. **OVERHEAD CHARGING**: f's own work t_f(N) enters the ledger; extremality claims
   are relative to a budget class for t_f — here polylog|N| per emitted candidate.

N-independent orders (ascending, wheels, ladders) satisfy all three clauses — this
is exactly the corner L7-as-drafted missed by restricting to magnitude-monotone
orders. **Where barriers bite:** clause 3 unrestricted is VACUOUS (f may factor N
internally and put p first — circular); under a polylog budget it is morally safe
but NOT unconditionally provable (needs a sublinear-time factoring separation — none
exists, likely permanent; lemma L7-e). Clause 2 + touch-floor is where barrier-1
(paper-132's 4/3 COST cap) attaches: residue-guided δ's are test-blind but pay ε or
appear as T1-priced skip-sets. Barrier-2 territory: |x−√N| remains the only known
polylog-computable feature of N with nonzero mutual information with divisor
position (type-channel = abelianization everywhere tested; batteries factor-blind);
every other N-feature is residue-like and COST-capped.

## 2. The falsification

Two independent failures kill strict extremality of σ₀:

**FAILURE 1 — the prior-shape channel Λ (kills extremality even per-stratum).**
Static-order optimality is mass-sorting: adjacent transpositions improve
E[cost] = Σ_v m(v)·rank(v) iff they sort by descending divisor-mass m(v); for per-N
families condition on p = v and minimize c_π(v) = E[rank | p=v]. Whether the
mass-sort IS sqrt-descending is then a POPULATION property: m must be MLR in
−|x−√N|. For arithmetic-uniform N the Mertens/Dickman tilt gives m(v) ~ 1/v —
ANTI-monotone, ascending wins outright (S = 2.13 on the uniform proxy,
growing ~ H_M). For hard-balanced generators (q < 2p ⇒ p ∈ (√(N/2), √N]
guaranteed) the within-window mass is bottom-heavy — measured tilt mean z =
0.4095–0.4148 against the analytic 0.414 for r = q/p ~ U[1,2] — and window-ascending
beats plain sqrt-descending by **S = 1.58×±0.03** (BAL_prime 1.5785±0.029,
BAL_intsnap 1.6114±0.033, n=2400 each; analytic two-stage prediction 0.138v/0.219v
= 1.587 — matches).

**FAILURE 2 — the interaction term kills S(π) = S(σ)·S(δ).** A canonical factorization
π = σ_B∘δ_B EXISTS for any N-computable window partition (σ_B block order, δ_B
within-block permutation), but is VACUOUS for singleton blocks and has content only
for coarse windows — where non-residue δ's live. Coupled orders (residue promotion
inside a magnitude scan) show apparent gains ONLY off-MLR (uniform proxy 1.40×),
and the gains are PRIOR-SHAPE LEAKAGE, not residue information (Section 4).
Multiplicative factorization fails both ways; the σ∘δ decomposition is definitional,
not explanatory.

**Therefore L7-as-drafted is FALSE-IN-PRINCIPLE**: (i) the mass-sort channel beats
sqrt-descending under hard-balance populations (1.58×±0.03) and unboundedly (~log M)
on non-MLR/uniform marginals; (ii) "extremal" without excluding T1-priced filters
fails via wheels (3.75×), so extremality was only ever meaningful per-component.

## 3. The replacement: Λ-channel + master inequality (L7′)

**Λ(pop) := C_best-static / C_desc** — the ratio of the best static order's cost to
sqrt-descending's, computed under the population prior. Λ = 1 iff within-stratum
divisor-mass is MLR in −|x−√N| (descending IS the mass-sort); Λ < 1 means a
population-shaped order beats descending.

**Sign-flip law (the channel has two directions):** the tilt direction is set by the
band width of r = q/p. Analytic crossover at **E[√r] = 2/(1+1/√2) = 1.1716**;
ascending wins iff the band is wide enough. Measured: hard q<2p balance
(r ~ U[1,2], E[√r] ≈ 1.14 < 1.1716) ⇒ bottom-heavy tilt (z = 0.41), ascending wins
1.58×; narrow bands (E[√r] above crossover) ⇒ top-heavy tilt (z = 0.6466),
DESCENDING is extremal (Λ = 1.0, argmin = win_desc; window-ascending LOSES at
S = 0.57); paper-137's own pool sits between (z = 0.5588) with descending winning —
see Section 5. One dial (band width), two regimes, clean analytic crossover.

**MASTER INEQUALITY (L7′):** for every well-defined test-blind N-computable reorder Π,

  **S(Π) ≤ (4/3) · min( 1/μ_eff(Π), 2^{k_bits}(Π) ) / Λ(pop)**

where μ_eff is STRUCTURAL (keep-fraction of skip-sets; 1 for pure permutations) and
k_bits any truthful comparison budget. Finite audit: **ZERO violations** across all
policy arms × four pools (BAL_prime, BAL_intsnap, BAL_narrow, P137; verifier
recomputation including a hybrid filter×reorder arm designed to stress the
bookkeeping). Wheel calibration: the wheel is an order-preserving skip-set with
keep fraction μ = φ(30)/30 = 4/15, so the T1 protocol-A law at P_hit = 1 predicts
S = 30/φ(30) = 3.750; measured 3.7331–3.7496 across pools (headline cell 3.741 vs
3.750), gap **0.25–0.31%** — the wheel hits the T1 law exactly up to censoring, which
is the inequality's T1 component validating against a known-closed case.

**CAVEAT (load-bearing): μ_eff booking.** Pure-permutation cells satisfy the cap
TAUTOLOGICALLY at μ_booked = 1, and win_asc is booked μ = 1 though structurally a
window filter — conservative direction, but composites expose the gap: the
window+wheel hybrid reaches **S = 4.06 on the P137 pool against a 1.77 cap if its μ
were booked as 1**; only structural μ extraction (lemma L7-d, below) makes the cap
non-vacuous. Until L7-d closes, L7′'s inequality is proven-shape with a tautology
risk in the pure-permutation slice, honestly flagged rather than hidden.

## 4. Obstruction witnesses, corrected

The round-74 draft carried a witness that the verification killed; recorded here as
a ledger item so the correction propagates.

- **JACOBI WITNESS RETRACTED (algebraic degeneracy, not evidence).** The draft read
  Jacobi-promotion behavior as prior-shape signal. It is nothing of the sort:
  (N|x) = 0 IDENTICALLY at x = p because N ≡ 0 mod p — 100% of draws
  (`jacobi_p_is_zero = 1.0` both pools carrying the arm). Conditioned on coprime x,
  the promoted share is 0.5036 / 0.5015 — a fair coin. The witness was measuring
  "p divides N", i.e., the answer, not a usable pre-hit signature. DROPPED.
- **REPLACEMENT WITNESS — keyed-vs-fixed mod-3 control.** The proper test of whether
  residue couplings carry independent power: compare N-keyed promotion (residue of N
  mod 3 selects the key) against FIXED-key promotion (same periodicity, zero
  N-information). Result: statistically identical speedups (BAL_prime 0.6366 vs
  0.6537; BAL_intsnap 0.6456 vs 0.6560; P137 pool 0.6836 vs 0.6595) and hit-enrichment
  ≈ 1/2 BOTH arms (keyed 0.4342/0.4383/0.516, fixed 0.4512/0.4537/0.496). **Residue
  couplings carry zero information**; their apparent gains on some marginals
  (uniform proxy 1.40×) are PRIOR-SHAPE LEAKAGE present only off-MLR. This is the
  factor-blind law replicated with a proper control — strengthening papers 130/136's
  QR-bite result and closing the last apparent counterexample face.
- **exp570 early-fire transfer, bounded honestly.** Early-fire is an ECM
  ord-completion law (hit position ~ max-prime-power(ord)/B1); TD hits have NO
  completion structure, so no literal transfer. What transfers is FRONT-LOADING ⇒
  HEAD-DOMINATION: surrogate check (K=4096 grid, exp-shaped priors) gives
  front-loaded-at-√N ⇒ descending 948 < ladder-aligned 1493 < asc/naive 3149, and
  front-loaded-at-low-end ⇒ ascending = naive-ladder 948 ≪ descending 3149.
  Front-loading alone does NOT imply sqrt-descending dominates fixed B1-ladder
  schedules; dominance needs the centering axiom (mass at √N) too. Under centering,
  ladder-aligned ≈ descending up to block granularity (S = 0.990; first block holds
  essentially all mass) while ladder-naive collapses (S = 0.27). This bounds what
  exp570's trace law can say about trial division.

## 5. Paper-137 REFINED, not contradicted

Paper 137 recorded descending winning on its pool (asc/desc ≈ 1.08×). The verifier's
replication on 137's OWN generator pool: trunc-pruned ascending S = 0.9278, i.e.
asc/desc = **1/0.9278 = 1.078× vs the recorded 1.08×** — replicated. The Λ-channel
does NOT overturn 137: on that pool the window policy is UNDEFINED on 21.6% of draws
(win_asc_miss_frac = 0.216 — p falls below the window) and the tilt z = 0.5588 does
not clear the ascending side decisively (win_asc 1.3312±0.1176 conditional on the
78.4% where defined, which is not a deployable statement). **Refinement, precisely:
descending wins on 137's population; Λ-dominance exists ONLY under hard q<2p
balance; any deployable "~free" gain therefore requires FIRST verifying the deployed
generator enforces that balance — the policy is undefined otherwise.** This converts
137's honest frontier from a conjecture about orders into a measurement program about
generators (L7-a).

## 6. Sampling correction on record

The attempt's quoted window-ascending figures (1.71–1.91) came from its own
n=150-per-population first pass (`gapL7_result.json`: BAL win_asc 1.9105) — sampling
inflation at small n. The independent verification at n=2400 corrects to
**1.58×±0.03**, matching the attempt's OWN analytic prediction of 1.587. The analytic
core was right; the Monte-Carlo dressing was not. Recorded so no future session cites
1.71–1.91 or the raw n=150 table.

## 7. Verification census

- **Author first pass**: `gapL7_check.py` → `gapL7_result.json` (seed 20260824,
  n=150/pop, BAL + UNIF, 0.99 s). Directionally correct on Λ < 1 for BAL
  (Λ = 0.5234) but magnitude-inflated on win_asc (1.9105); UNIF arm correctly showed
  ascending winning outright (2.1325) and win_asc ill-defined there (only 3/150 hits
  — censored), which the draft initially under-weighted.
- **Independent verifier** (`verifyL7_sim.py` → `verifyL7_sim_out.json`; re-derived
  from scratch, no code reuse; seeds distinct from the author run):
  - ITEM 1 (Λ-channel): four pools — BAL_prime n=2400 (win_asc 1.5785±0.029, tilt
    z = 0.4148), BAL_intsnap n=2400 (1.6114±0.033, z = 0.4095), BAL_narrow n=1600
    (0.5682, z = 0.6466, sign flip, Λ = 1.0 argmin desc), P137 n=500 (miss 21.6%);
    analytic two-stage formula (u−1)/(1−u/√2) and crossover 1.1716 printed and
    matched.
  - ITEM 2 (master inequality): recomputed audit incl. wheel-vs-T1-law exactness
    (φ(30)/30) and the hybrid filter×reorder arm exposing the μ_eff booking gap
    (hybrid S = 3.741 actual vs 2.105 cap-if-μ=1 on BAL; 4.062 vs 1.775 on P137);
    **violations: [] in all four pools**.
  - ITEM 3 (obstructions): keyed-vs-fixed mod-3 arms + closed-form interaction term
    reproducing both S values; Jacobi degeneracy quantified (p_is_zero = 1.0,
    coprime promoted share 0.5036/0.5015).
- **Uniform proxy cross-check** (`verifyL7_unif.py`): independent implementation of
  the UNIF claims — asc S ≈ 2.13 outright, win_asc undefined on the overwhelming
  majority of draws (attempt: 147/150).
- Corrections accepted by the author file post-hoc (revision block at top of
  `gapL7_extremality.md`): headline 1.71–1.91 → 1.58×±0.03; Jacobi witness dropped;
  137 restated refined-not-contradicted; ladder-aligned ≈ descending (S = 0.990);
  wheel-vs-1/μ gap 0.25–0.31%; μ_eff caveat added.

## 8. L7′ status and the ranked remaining program

**L7′ = master inequality + mass-sort characterization: PROVEN-SKETCH** —
finite-verified at zero violations, analytic core classical (exchange argument +
Mertens/Dickman tilt), contingent on:

- **L7-a (hours; HIGHEST VALUE, named next step): measure the DEPLOYED generator.**
  Extract the production r-law and decide whether any deployable gain exists; restate
  L7′ with measured Λ_lab. The verifier's sweep already shows the sign of Λ flips
  with band width (hard q<2p ⇒ bottom-heavy, ascending 1.58×; narrow ⇒ top-heavy,
  descending extremal; P137 ⇒ descending wins, ascending undefined 21.6%) — without
  L7-a, Λ is unmeasured and the MLR premise unchecked for every real population.
- **L7-b (hours): write out the exchange theorem** (mass-sort optimality via adjacent
  transpositions + conditional version c_π(v) = E[rank|p=v]).
- **L7-c (1–2 sessions): master inequality proof** from touch-floor accounting
  (needs draft-L1); couplings are Λ-leakage, not factors (keyed-vs-fixed).
- **L7-d (1 session): structural μ_eff/k_bits extraction** for arbitrary π, defined
  without reference to achieved speedup — LOAD-BEARING NOW (hybrid cells breach any
  μ=1 booking).
- **L7-e (OPEN, likely permanent): unconditional factor-blindness** of
  polylog-computable f — equivalent to a sublinear-time factoring separation. Adopt
  as hardness-relative axiom or oracle-relativize; never claim unconditionally.

Draft edits required downstream (recorded so they propagate): paper 219's L7 entry
rewrites to L7′; Conjecture D's SET-component gains Λ (loses equality); O1/O2
sharpened — the population measure SELECTS the extremal order.

## Bottom line

Barrier validation: barrier-4's positional stratum now has its converse made precise
AND its extremality claim corrected — position works through a population-shaped
channel whose sign is measurable (band width ⇒ tilt direction ⇒ which order is
extremal), the residue cap 4/3 survives untouched (couplings carry zero information,
now with a proper control), and the master inequality unifies both caps with the Λ
correction. No breakthrough claimed: this is a falsification-and-replacement inside
the existing map, closing one named GAP by killing its conjecture and replacing it
with a verified weaker truth whose remaining risk is concentrated in one named
measurement step (L7-a).

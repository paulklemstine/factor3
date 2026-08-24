# GAP L7 — EXTREMALITY OF SQRT-DESCENDING AMONG N-COMPUTABLE REORDERS (round-74 THEORY)

Companion to `barrier4_positional_converse_draft.md` (T1/T2, Conjecture D) and paper 132/137/143.
New leverage: exp570 early-fire trace law; Conjecture D cost/set split. Checks: `gapL7_check.py` ->
`gapL7_result.json` (0.99 s, n=150/pop) + independent `verifyL7_sim.py`/`verifyL7_sim_out.json` (n=2400/pop).

> **REVISION (2026-08-24, post-verifier)** — repairs per independent check `verifyL7_sim_out.json`:
> (1) headline window-ascending speedup corrected to **1.58×±0.03** (BAL_prime 1.5785±0.029,
> BAL_intsnap 1.6114±0.033, n=2400 each); this file's original n=150 figures (1.71–1.91) were
> sampling inflation — the analytic prediction 1.59 was right. (2) The Jacobi witness is
> RETRACTED: (N|x)=0 identically at x=p since N≡0 mod p (100% of draws; promoted share among
> coprime x = 0.504/0.502) — algebraic degeneracy, not prior-shape evidence; replaced by the
> keyed-vs-fixed mod-3 control: S 0.637/0.654 (BAL_prime), 0.684/0.660 (P137 pool);
> hit-enrichment ≈1/2 BOTH arms — keying adds zero information. (3) Paper-137 stated as
> REFINES-not-contradicts (see (b)). (4) Minor fixes: ladder-aligned ≈ descending at S=0.990;
> wheel-vs-1/μ gap 0.25–0.31%; μ_eff-booking caveat added (master-inequality paragraph).

## (a) Action space, precisely

Fix N (odd composite), candidate space I(N)={2..⌊√N⌋}, true factor p=min-factor, baseline σ₀ =
sqrt-descending. Cost model: touch = full divisibility test = 1 unit; skip pays 0 but its keep-set
is T1-priced (μ = keep fraction); cheap predicates are paper-132 COST-class at ε>0 each (O3).

**DEF (REORDER-class policy).** Π emits an enumeration a₁,a₂,… of I(N), a_k = f(k,N), where f satisfies:
1. UNIFORMITY: one fixed computable f serves all N (no per-N hardcoding).
2. TEST-BLINDNESS: a_k is independent of the outcomes of the tests a_i|N for i<k (order commits
   ex ante). Interleaved comparison queries ("p≤x?") admitted only at T2 pricing (1 unit, truthful).
3. OVERHEAD CHARGING: f's own work t_f(N) enters the ledger; extremality claims are relative to
   a budget class for t_f — here polylog|N| per emitted candidate.
N-INDEPENDENT orders (ascending, wheels) satisfy all three — the corner L7-as-drafted misses.
**Where barriers bite:** clause 3 unrestricted is VACUOUS (f may factor N internally and put p
first — circular); under a polylog budget it is morally safe but NOT unconditionally provable
(needs a sublinear-time factoring separation — none exists, likely permanent; see L7-e). Clause 2 +
touch-floor is where barrier-1 (paper-132 4/3 COST cap) attaches: residue-guided δ's are test-blind
but pay ε or appear as T1-priced skip-sets. Barrier-2 territory: magnitude |x−√N| is the only known
polylog-computable feature of N with nonzero mutual information with divisor position
(type-channel=abelianization; batteries factor-blind) — every other N-feature is residue-like and
COST-capped.

## (b) Exchange argument: π = σ∘δ — decomposition verdict

Canonical factorization EXISTS for any N-computable window partition B: π = σ_B∘δ_B, σ_B =
block order (magnitude content), δ_B = within-block permutation. Vacuous for singleton blocks,
so δ has content only for COARSE windows — which admit non-residue δ's. Two failures:

**FAILURE 1 — prior-shape channel Λ (kills strict extremality even per-stratum).**
Static-order optimality is mass-sorting: adjacent transpositions improve E[cost]=Σ_v m(v)·rank(v)
iff they sort by descending divisor-mass m(v); for per-N families condition on p=v and minimize
c_π(v)=E[rank|p=v]. Whether the mass-sort IS sqrt-descending is a POPULATION property:
m must be MLR in −|x−√N|. For arithmetic-uniform N, Mertens/Dickman tilt gives m(v)~1/v —
ANTI-monotone — ascending wins (witness below). For hard-balanced generators (q<2p, so
p∈(√(N/2),√N] guaranteed) the within-window mass is bottom-heavy: tilt mean z at scale
0.4095–0.4148 vs analytic 0.414 for r=q/p~U[1,2]; consequence **window-ascending beats plain
sqrt-descending by S=1.58×±0.03 at n=2400** (analytic 0.138v/0.219v = 1.587 — matches); on a
uniform-N proxy ascending wins outright S=2.13 (growing ~H_M). Dominance is NOT universal:
under NARROW bands the tilt flips top-heavy (z=0.647) and DESCENDING is extremal (Λ=1.0,
win-ascending 0.568×); on 137's own pool the window policy is undefined on 21.6% of draws
(p below window) and trunc-pruned ascending LOSES (S=0.928 = 137's recorded 4.80/5.19 ratio;
verifier 1/0.928 = 1.078× vs recorded 1.08×) — **REFINES-not-contradicts paper-137: descending
replicated winning on 137's population; Λ-dominance exists ONLY under hard q<2p balance, and any
deployable "~free" gain first requires verifying the deployed generator enforces that balance
(policy undefined otherwise).**

**FAILURE 2 — interaction term kills S(π)=S(σ)·S(δ).** Coupled orders (residue promotion inside a
magnitude scan): N-keyed mod-3 promotion vs FIXED mod-3 promotion are statistically identical
(S 0.637/0.654 BAL; 0.684/0.660 P137 pool; hit-enrichment ≈1/2 both arms — the key carries zero
information), and both LOSE on balanced populations while showing apparent gains only off-MLR
(uniform proxy 1.40×). Reading: residue couplings have NO independent power (factor-blind law,
replicated with a proper keyed-vs-fixed control); their apparent gains are PRIOR-SHAPE LEAKAGE,
present only on non-MLR marginals. Multiplicative factorization fails both ways; the correct object:

**MASTER INEQUALITY (L7′):** for every well-defined test-blind N-computable reorder Π,
  S(Π) ≤ (4/3) · min(1/μ_eff(Π), 2^{k_bits}(Π)) / Λ(pop),
Λ(pop) = C_best-static/C_desc (Λ=1 iff within-stratum MLR), μ_eff STRUCTURAL (keep-fraction of
skip-sets; 1 for pure permutations). Finite audit: ZERO violations across policy arms × 4 pools;
wheel lands ON T1 protocol-A P_hit=1 (gap 0.25–0.31%). CAVEAT (load-bearing): pure-permutation cells
satisfy the cap TAUTOLOGICALLY at μ_booked=1, and win_asc is booked μ=1 though structurally a window
filter — conservative direction, but composites expose the gap: the window+wheel hybrid reaches
S=4.06 on the P137 pool against a 1.77 cap if its μ were booked as 1 — only structural μ extraction
(L7-d) makes the cap non-vacuous.

## (c) exp570 early-fire: what it does and doesn't give

Early-fire is an ECM ord-completion law (hit position ~ max-prime-power(ord)/B1); TD tests are
independent events with NO completion structure — no literal transfer. What transfers is
FRONT-LOADING: hits concentrate in the schedule head ⇒ expected cost is head-dominated ⇒ ordering
THE HEAD is where leverage sits. Surrogate check (K=4096 grid, exp-shaped priors):
front-loaded-at-√N ⇒ descending 948 < aligned-ladder 1493 < asc/naive 3149; front-loaded-at-low-end
⇒ ascending = naive-ladder 948 ≪ descending 3149 (aligned 3012, wrong end). **Verdict: front-loading
alone does NOT imply sqrt-descending dominates fixed B1-ladder schedules — it implies
HEAD-DOMINATION; dominance needs the centering axiom (mass at √N) as well. Under centering,
ladder-aligned ≈ descending up to block granularity (S=0.990 at scale; first block holds
essentially all mass) while ladder-naive collapses (S=0.27).**

## (d) Verdict + ranked remaining lemmas

**L7 AS DRAFTED: FALSE-IN-PRINCIPLE** — (i) the mass-sort channel beats sqrt-descending under
hard-balance populations (1.58×±0.03) and unboundedly (~log M) on non-MLR/uniform marginals; (ii)
"extremal" without excluding T1-priced filters fails via wheels (3.75×), so extremality was only
ever meaningful per-component. **CORRECTED L7′ (master inequality + mass-sort characterization):
PROVEN-SKETCH**, finite-verified at zero violations, analytic core classical, contingent on:
- **L7-a (hours, HIGHEST value): measure the DEPLOYED generator.** Verifier's sweep already shows
  the sign of Λ flips with band width (hard q<2p ⇒ bottom-heavy, window-ascending wins 1.58×;
  narrow ⇒ top-heavy, descending extremal; P137 pool ⇒ descending wins, asc undefined 21.6%).
  Extract the production generator's r-law and decide whether any deployable gain exists; restate
  L7′ with measured Λ_lab. Without this, Λ is unmeasured and the MLR premise unchecked.
- **L7-b (hours): write out the exchange theorem.** Mass-sort optimality for static orders
  (adjacent transpositions) + conditional version c_π(v)=E[rank|p=v] for per-N families.
- **L7-c (1–2 sessions): master inequality proof.** Interaction bound S ≤ (4/3)·T1-cap/Λ from
  touch-floor accounting (needs draft-L1); couplings are Λ-leakage, not factors (keyed-vs-fixed).
- **L7-d (1 session): structural μ_eff/k_bits extraction** for arbitrary π, defined without
  reference to achieved speedup — load-bearing NOW (hybrid cells breach any μ=1 booking).
- **L7-e (OPEN, likely permanent): unconditional factor-blindness** of polylog-computable f —
  equivalent to a sublinear-time factoring separation. Adopt as a hardness-relative axiom or
  oracle-relativize; never claim unconditionally.

Provenance: this file + `gapL7_check.py`/`gapL7_result.json` (first pass) + `verifyL7_sim.py`/
`verifyL7_sim_out.json` (independent scale check; source of revised numbers). Round74 dir; not committed.
Draft edits required: L7 rewrite (extremal = population mass-sort); Conjecture D gains Λ, loses
equality; O1/O2 sharpened (the population measure SELECTS the extremal order).

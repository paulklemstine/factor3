# BARRIER-4 CONVERSE — POSITIONAL/MAGNITUDE STRATUM: theorem candidates T1/T2, lemma census, and the SET/COST dichotomy

Round 74 THEORY draft. Companion to paper 132 (residue cap), 137/143 (position measured),
138 (class hints), 212/exp563 (adaptive magnitude). Finite checks: `exp574b_saturation_check.py`
→ `exp574b_result.json`; independent recheck artifact: `verify_t1_t2_recheck.json`.

> **VERIFICATION (2026-08-24)** — independently rechecked per `verify_t1_t2_recheck.json`:
> exp574b stored values reproduce (zero discrepancies); tags upgraded PROVEN→VERIFIED where
> the recheck covers them (T1a finite-M formula + R-first-iff-P≥μ: 0 failures; T1b exhaustive
> orders + insertion sweep M∈{16,33,64}; T2 dyadic identity exact W=2..4096; general-L upper
> bound to 4096; census argmin offsets {−2,−1} everywhere).
> **REVISION 2026-08-24**: (1) T1a law replaced by CERTIFIED-SILENCE form
> S_A=1/[μP+(1−P)(1−μ)]; drafted form 1/(1−(1−μ)P) kept below as SUPERSEDED (14 algebra
> failures); witness story survives via feasibility μ≤1/S. (2) T1b restricted: protocol-B
> dominance holds iff P≥μ (all counterexamples P<μ); protocol A unconditional. (3) T2: cost
> offset bracket corrected to [0.414,0.501] (location wobble −1.5288, discrete {−2,−1});
> marginal-value identity DELETED (231 gross/net failures); added dyadic V=log₂W+½ exact
> 2..4096, deepest general-L undercut −0.4993@L=3073 (never crosses −½), census C*=19.5/20.5.

## 0. Setup; the two action classes

Candidate space I(N)={2..⌊√N⌋}, M=|I| (or W=π(√N)−1 after sieving). Baseline σ₀ = plain
sqrt-descending. Prior π_N over positions induced by the lab N-population. Cost = candidates
touched (full trial = 1 unit; cheap residue predicate = ε). Speedup(Π) = E C[σ₀]/E C[Π].

AXIOM (touch-floor) [SKETCH — must be stated as a cost-model axiom, verified against 132's
M=33 accounting]: every touched candidate pays ≥ε>0; untouched pay 0. This splits ALL actions:

- **COST-class** (paper-132 stratum): alters per-touch cost (residue filters/keep-sets);
  touches every candidate. Savings bounded by ε·M floor.
- **SET-class** (positional/magnitude stratum): alters WHICH candidates are touched and in
  what order (permutations, windows, truncation); per-touch cost fixed. Savings come from the
  untouched tail, size O(M) — unbounded in principle.

## T1 — Fixed-window oracle exact law (generalizes 138+143)

Protocol A (fire-or-CERTIFIED-silent): oracle announces R⊆I, width μM, iff p∈R (fires w.p.
P_hit); SILENCE CERTIFIES p∉R, so fallback scans only I\R — R never re-touched. Protocol B
(announce-always): R always announced, P[p∈R]=P_hit, silence carries no information.
Committed policy: scan R top-down, then the remainder.

**Theorem T1.** Under uniform π on I, for ANY fixed measurable R and ANY response policy:
(a) [VERIFIED — supersedes drafted form] Protocol A committed policy: E C = P_hit(μM+1)/2 +
(1−P_hit)((1−μ)M+1)/2 over C₀=(M+1)/2, giving the exact large-M law
    **S_A = 1 / [ μ·P_hit + (1−P_hit)(1−μ) ]  (CERTIFIED-SILENCE law)**
(finite-M rational (M+1)/[P(μM+1)+(1−P)((1−μ)M+1)]; recheck 0 failures). The DRAFTED form
1/(1−(1−μ)P_hit) — whose silent-fallback wastefully re-scans R — is SUPERSEDED (14 algebra
consistency failures); it models non-certifying silence, strictly weaker: (μ=.05,P=.85) →
5.4054 certified vs 5.1948 drafted; (.02,.985) → 29.0698 vs 28.8184. Protocol B optimal
response: S_B = 1/(1+μ−P_hit) ≤ S_A; R-first beats ignoring R iff P_hit ≥ μ [VERIFIED].
(b) [VERIFIED] Block-first dominance: protocol A unconditional (exhaustive over all orders);
protocol B iff P_hit ≥ μ — all 12 recheck counterexamples have P<μ; insertion sweep M∈{16,33,64}:
first slot always wins. Mechanism: advancing R-members never delays another R-member.
(c) [PROVEN, uniform prior] Universality GEOMETRY-FREE: value depends only on (μ,P_hit), not
on where R sits or its shape — positional analogue of 132's θ-only law.
(d) [PROVEN arithmetic] Cap is S ≤ 1/μ (attained at P_hit=1): **no constant cap exists** in
T1; the exact law itself is the cap; sup over μ→0 diverges — correct, see verdict (e).

Witness numbers: anchors survive the law replacement via FEASIBILITY μ ≤ 1/S (all four
anchors feasible; only infeasible locus rows demand P_hit>1): 5.19× frontier ↔ (0.05,0.85)
→ 5.4054; 6.91× trunc-high ↔ (0.05,0.9003) → 7.1429; 4.35× low ↔ (0.05,0.8106) → 4.649;
29.1× (α=1) ↔ (0.02,0.9853) → 29.0698. GAP: not yet fitted to 137's sham strata (needs L4).

## T2 — Adaptive saturation identity (formalizes 212's k*=⌈log₂W⌉)

Model: truthful comparison queries "p ≤ x?" at cost 1 trial-unit each; residual top-down
scan of support s costs (s+1)/2; uniform prior. Value function V(L)=min( (L+1)/2,
1+min_x[(x/L)V(x)+((L−x)/L)V(L−x)] ).

**Theorem T2.**
(a) [VERIFIED] Dyadic supports: V(W)=min_{k≥0}[k+(W/2^k+1)/2] EXACTLY, attained by median
bisection; equivalently **V(W)=log₂W+½ EXACTLY for every W=2..4096** (recheck table). Relaxed
continuous optimum at 2^(k+1)=W·ln2 (location −1.5288 rel log₂W); verified COST-offset bracket
**[0.414, 0.501]** (min 0.415@L=3, max 0.5011@L=2129, dyadic exactly ½) — supersedes the
draft's "[−0.53,+0.5]", which conflated cost offset with LOCATION wobble {0.4712, 0.5288}.
(b) [VERIFIED to 4096] General L: min_k[k+(⌈L/2^k⌉+1)/2] is an UPPER bound on V(L); deepest
undercut −0.499349 at L=3073, NEVER crossing −½ (0 crossings to 4096). Exact integrality
constant open beyond the verified range (extension trivial).
(c) [REVISED] Gain SATURATION: support fully pinned at k_pin=log₂W; beyond k_pin speedup is
EXACTLY flat (zero bits remain — the balanced-stratum zero-bit result is the k=0 slice). The
drafted marginal-value identity "value of (k+1)-th query = W/2^(k+2)" is DELETED (231
gross/net recheck failures); only qualitative declining-marginal-gain survives [SKETCH].
(d) [VERIFIED census] Cost-optimal stop k_opt = argmin_k[k+(W/2^k+1)/2]: offset {−2,−1} rel
log₂W at EVERY W checked (C*=19.5@2^19, 20.5@2^20) — NOT k_pin. **Definitional reconciliation
required**: exp563's "k*=⌈log₂W⌉" is the saturation/pinning point (c); the work-minimizing
stop (d) sits 1–2 queries earlier. Both true; paper must name which.
(e) [SKETCH] Non-adaptive batteries cannot compound: expected posterior mass is a martingale
under non-adaptive partitions, so fixed batteries leave E[residual scan] unchanged unless
ordered by posterior mass — recovering 138's linear-in-bits law and 212's zero-bit balanced
result. Adaptivity is precisely what converts bits into multiplicative halving.

## Lemmas needed to close remaining gaps

- L1 Touch-floor decomposition ⇒ recovery of 132's 1/(1−θ+θ²) from COST-class accounting
  [analytic; recheck vs 132's M=33 exhaustive table]. Feasibility: hours.
- L2 Factorization S(R∘F)=S(R)·S(F): independent thinning commutes with rank statistics
  [analytic + Monte Carlo permutations×thinnings at M=33..129]. Feasibility: hours.
- L3 Block-first dominance for arbitrary R (T1b) [VERIFIED computationally at M∈{16,33,64};
  analytic exchange proof for general M still SKETCH]. Feasibility: hours.
- L4 Selection-effect correction Δ(π,R): under stratified π_N, conditional baseline cost
  E[C₀|p∈R] ≠ C₀; exact under uniform-within-stratum priors, correction bounded by stratum
  variance [GAP — needs explicit stratum measure extracted from 137's q/p data]. 1–2 sessions.
- L5 Integrality constant of T2(b) [VERIFIED to L=4096: bound never crosses −½, deepest
  −0.4993@3073; exact constant open beyond]. Extend range as needed.
- L6 Protocol A/B algebra (T1a) [VERIFIED — 0 recheck failures].
- L7 Extremal N-COMPUTABLE order: sqrt-descending maximizes S among all orders computable
  from N alone, per stratum (monotone likelihood ratio of π_N in |p−√N| within strata)
  [GAP — conjectural; formalizes 137's "honest frontier"]. Hard analytically; finite check
  possible on lab population samples.
- L8 Pin exp563's k* definition against T2(c)/(d) census [read exp563 logs; minutes].

## Obstructions

- O1 Siegel-type ineffectivity: NO uniform-in-N SET-class constant exists — pointwise N with
  p≈√N gives unbounded ratio; any cap is per-stratum or mixture-weighted. Exceptional balance
  tails enter via distribution of √N−p (primes in short intervals territory — genuinely open;
  constants inevitably ineffective).
- O2 Balance-stratum coupling: 137's opposite gradients (20.67×↔1.97×) nearly cancel to 5.19×;
  wrong mixture weight flips the truncation gradient (4.35 vs 6.91). Universal statements must
  carry the population measure explicitly — a law "averaged over N" without it is ill-posed.
- O3 Axiom-dependence: the 4/3 cap needs touch-floor ε>0; ε=0 collapses COST into SET and the
  cap dissolves. The dichotomy is axiomatic, not free — state the cost model in the paper.
- O4 Regime boundary: 138-linear (non-adaptive bits) vs 212-multiplicative (adaptive halving)
  — T2(e)'s martingale argument draws the line; conflating them manufactures fake contradictions.
- O5 k* naming (L8) before writing the identity into a paper record.

## (e) Verdict + CONJECTURE D

**Verdict: no TRUE constant cap exists for the positional stratum — and this is consistent,
not contradictory.** Paper 132's 4/3 caps COST-class actions: they touch every candidate
(floor ε·M persists) and only downgrade touches, giving exactly 1/(1−θ+θ²) ≤ 4/3 (exp574b-A).
Positional information acts in SET-class: savings come from never touching an O(M) tail, so
the cap attaches instead to the exact laws T1 (geometry: ≤1/μ) and T2 (information: 2^k
halvings, saturating at k_pin=log₂W). 5.19× > 4/3 is class-crossing, not cap-breaking:
sqrt-descending carries no filter — it is a pure SET-action whose gain sits inside T1's
certified-silence law near (μ,P)=(0.05,0.85) (5.4054 ≥ 5.19; feasibility μ≤1/S). Residues
and position are orthogonal factors, so both laws coexist inside one procedure.

**CONJECTURE D (SET/COST dichotomy).** Every N-computable or hint-conditioned trial-division
speedup procedure Π factors as Π = R∘F with R a SET-action (order/truncation choice) and F a
COST-action (order-preserving keep-set); moreover
  S(Π) = S(R)·S(F),   sup_F S(F) = 4/3 (attained θ=1/2),   S(R) ≤ min(1/μ_eff, 2^{k_bits}),
with equality cases: plain sqrt-descending (pure R, no filter), residue dial at θ=1/2 (pure F),
committed window oracle (R saturated by T1), median bisection (R saturated by T2).
Witnesses: 4/3 (132); 5.19× feasible at (0.05,0.85) [certified-silence 5.4054] and 29.1× at
(0.02,0.985) [29.0698] (137/138/143; recheck D_witnesses all feasible μ≤1/S); k_pin=log₂W
saturation, 165–239× compounding ≤ 2^{k} scale, zero-bit balanced batteries (212/exp563).
Falsifier: COST-component alone exceeding 4/3; SET-gain exceeding min(1/μ_eff, 2^{bits})
given its budget. Status: L1+L2 make D PROVEN-shaped; L4 (stratum measure) is load-bearing.

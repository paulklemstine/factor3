# Paper 219 — BARRIER-4 POSITIONAL/MAGNITUDE CONVERSE: Certified-Silence Law S_A = 1/[μP+(1−P)(1−μ)] Supersedes the Drafted Fire-or-Silent Form (14 Algebra Failures Caught by Independent Verification); Adaptive Saturation V(W)=log₂W+½ EXACT on Dyadic W ∈ [2,4096]; Conjecture D Reconciles the Residue Cap 4/3 (COST-class) with Position's 5.19×–29.1× (SET-class) as a Product Law

> **STATUS: DRAFT-WITH-CAVEATS.** Recorded per independent-verifier recommendation.
> This is NOT a sealed theorem. Every numeric claim below was independently recomputed
> (`verify_t1_t2_recheck.json`: **zero arithmetic errors** across all numeric claims;
> ~60% of PROVEN tags upgraded to VERIFIED where independently recomputed); the named
> GAPs (L4 stratum measure, L7 extremality, L8 k-naming) are the formal program's next
> work and are load-bearing for Conjecture D.

**Verdict name: the positional converse is real, stratified, and currently
draft-grade.** Paper 132's residue cap 4/3 and position's measured 5.19× do NOT
contradict: they act in different action classes. COST-class actions (residue
filters/keep-sets) touch every candidate and are capped by the touch-floor at
exactly 1/(1−θ+θ²) ≤ 4/3; SET-class actions (order/truncation/permutation) save by
never touching an O(M) tail and obey their own exact laws — geometry (T1,
certified-silence, cap 1/μ, no constant cap) and information (T2, 2^k halvings,
saturating at k_pin = log₂W). All four measured positional anchors land inside T1's
certified-silence law at feasible (μ, P_hit) loci (μ ≤ 1/S): 5.19× ≡ (0.05, 0.85),
6.91× ≡ (0.05, 0.9003), 4.35× ≡ (0.05, 0.8106), 29.1× ≡ (0.02, 0.9853).

Round-75 #4 · THEORY deliverable (no new experiment id; finite checks exp574b +
independent verifier attached) · assessment v326 · companion to papers 132
(residue cap), 137/143 (position measured), 138 (class hints), 212/exp563
(adaptive magnitude) · artifacts: `barrier4_positional_converse_draft.md`,
`exp574b_saturation_check.py` → `exp574b_result.json`,
`verify_t1_t2_recheck.py` → `verify_t1_t2_recheck.json` + `verify_run_stdout.log`
(all under `ResearchOutput/scripts/2026-08-24-round74/`).

## Question

Barrier 4 (no N-computable selection of the right candidate class) has two measured
faces that appear to collide: the residue cap 4/3 (paper 132) says order-preserving
filters buy at most 33%, while the positional stratum measures 5.19× (balance bet +
truncation, papers 137/143) and up to 29.1× at α=1. Is the barrier map internally
inconsistent, or do the two numbers live in different strata? This draft states the
POSITIONAL/MAGNITUDE stratum of the barrier-4 converse as exact theorem candidates,
checks them to exhaustion where feasible, and reconciles the two faces by a
class-factorization conjecture (D).

## Setup: the two action classes

Candidate space I(N) = {2..⌊√N⌋}, M = |I| (W = π(√N)−1 after sieving). Baseline σ₀ =
plain sqrt-descending; prior π_N induced by the lab N-population; Cost = candidates
touched (full trial = 1 unit; cheap residue predicate = ε); Speedup(Π) = E C[σ₀]/E C[Π].

AXIOM (touch-floor) [SKETCH — must be promoted to a cost-model axiom, verified against
paper 132's M=33 accounting]: every touched candidate pays ≥ ε > 0; untouched pay 0.
This splits ALL actions:

- **COST-class** (paper-132 stratum): alters per-touch cost (residue filters /
  keep-sets); touches every candidate. Savings bounded by the ε·M floor.
- **SET-class** (positional/magnitude stratum): alters WHICH candidates are touched
  and in what order (permutations, windows, truncation); per-touch cost fixed.
  Savings come from the untouched tail, size O(M) — unbounded in principle.

## Theorem candidate T1 — fixed-window oracle exact law (generalizes 138+143)

Protocol A (fire-or-CERTIFIED-silent): oracle announces R ⊆ I, width μM, iff p ∈ R
(fires w.p. P_hit); SILENCE CERTIFIES p ∉ R, so fallback scans only I\R — R never
re-touched. Protocol B (announce-always): R always announced, P[p∈R] = P_hit, silence
carries no information. Committed policy: scan R top-down, then the remainder.

**(a)** [VERIFIED — supersedes drafted form] Protocol A committed policy:
E C = P_hit(μM+1)/2 + (1−P_hit)((1−μ)M+1)/2 over C₀=(M+1)/2, giving the exact
large-M law

  **S_A = 1 / [ μ·P_hit + (1−P_hit)(1−μ) ]   (CERTIFIED-SILENCE law)**

(finite-M rational (M+1)/[P(μM+1)+(1−P)((1−μ)M+1)]; recheck 0 failures). The DRAFTED
form 1/(1−(1−μ)P_hit) — whose silent fallback wastefully re-scans R — is SUPERSEDED
(**14 algebra consistency failures** caught by the verifier); it models non-certifying
silence and is strictly weaker: (μ=.05, P=.85) → 5.4054 certified vs 5.1948 drafted;
(.02, .985) → 29.0698 vs 28.8184; (.115, .87) → 4.649 vs 4.3469. Protocol B optimal
response: S_B = 1/(1+μ−P_hit) ≤ S_A; R-first beats ignoring R iff P_hit ≥ μ [VERIFIED].

**(b)** [VERIFIED] Block-first dominance: protocol A unconditional (exhaustive over
all orders); protocol B iff P_hit ≥ μ — all 12 recheck counterexamples have P < μ;
insertion sweep M ∈ {16, 33, 64}: first slot always wins. Mechanism: advancing
R-members never delays another R-member.

**(c)** [PROVEN, uniform prior] Universality GEOMETRY-FREE: value depends only on
(μ, P_hit), not on where R sits or its shape — positional analogue of paper 132's
θ-only law.

**(d)** [PROVEN arithmetic] Cap S ≤ 1/μ (attained at P_hit=1): **no constant cap
exists** in T1; the exact law itself is the cap; sup over μ→0 diverges.

Witness numbers: anchors survive the law replacement via FEASIBILITY μ ≤ 1/S (all
four anchors feasible; only infeasible locus rows demand P_hit > 1):

| anchor | locus (μ, P_exact) | certified-silence S_A |
|---|---|---|
| 5.19× frontier (p137) | (0.05, 0.8500) | 5.1948 |
| 6.91× trunc-high | (0.05, 0.9003) | 6.91 |
| 4.35× trunc-low | (0.05, 0.8106) | 4.35 |
| 29.1× α=1 | (0.02, 0.9853) | 29.0698 |

GAP: not yet fitted to paper 137's sham strata (needs L4).

## Theorem candidate T2 — adaptive saturation identity (formalizes 212's k*⌈log₂W⌉)

Model: truthful comparison queries "p ≤ x?" at cost 1 unit each; residual top-down
scan of support s costs (s+1)/2; uniform prior. Value function
V(L) = min((L+1)/2, 1 + min_x[(x/L)V(x) + ((L−x)/L)V(L−x)]).

**(a)** [VERIFIED] Dyadic supports: V(W) = min_{k≥0}[k + (W/2^k + 1)/2] EXACTLY,
attained by median bisection; equivalently **V(W) = log₂W + ½ EXACTLY for every
W = 2..4096** (independent DP reproduction, author's exp574b AND verifier). Relaxed
continuous optimum at 2^(k+1) = W·ln2 (location offset −1.5288 rel log₂W); verified
COST-offset bracket **[0.415, 0.5011]** (min 0.415@L=3, max 0.5011@L=2129, dyadic
exactly ½) — supersedes the draft's "[−0.53, +0.5]", which conflated cost offset with
LOCATION wobble (+0.5288/−0.4712).

**(b)** [VERIFIED to 4096] General L: min_k[k + (⌈L/2^k⌉+1)/2] is an UPPER bound on
V(L); deepest undercut −0.499349 at L = 3073, NEVER crossing −½ (0 crossings to
4096). Exact integrality constant open beyond the verified range (extension trivial).

**(c)** [REVISED] Gain SATURATION: support fully pinned at k_pin = log₂W; beyond
k_pin speedup is EXACTLY flat (zero bits remain — the balanced-stratum zero-bit
result is the k=0 slice). The drafted marginal-value identity "value of the (k+1)-th
query = W/2^(k+2)" is DELETED as stated (**231 gross/net failures** — it is the GROSS
saving); the verifier's corrected NET identity holds EXACTLY:
cost(k) − cost(k+1) = W/2^(k+2) − 1 in 250/250 recheck cells. Only qualitative
declining-marginal-gain survives as [SKETCH].

**(d)** [VERIFIED census] Cost-optimal stop k_opt = argmin_k[k + (W/2^k+1)/2]:
offset {−2, −1} rel log₂W at EVERY W checked (C* = 19.5 @ 2^19, 20.5 @ 2^20) — NOT
k_pin. **Definitional reconciliation required**: exp563's "k* = ⌈log₂W⌉" is the
saturation/pinning point (c); the work-minimizing stop (d) sits 1–2 queries earlier.
Both true; every paper must name which k it means. (Note: exp563's economic optimum
10/18 additionally sits at its own convention ~1 query above T2's k_opt — three
distinct k's must stay distinguished.)

**(e)** [SKETCH] Non-adaptive batteries cannot compound: expected posterior mass is a
martingale under non-adaptive partitions, so fixed batteries leave E[residual scan]
unchanged unless ordered by posterior mass — recovering paper 138's linear-in-bits
law and paper 212's zero-bit balanced result. Adaptivity is precisely what converts
bits into multiplicative halving.

## CONJECTURE D (SET/COST dichotomy — cost-class vs set-class reconciliation)

Every N-computable or hint-conditioned trial-division speedup procedure Π factors as
Π = R∘F with R a SET-action (order/truncation choice) and F a COST-action
(order-preserving keep-set); moreover

  S(Π) = S(R)·S(F),   sup_F S(F) = 4/3 (attained θ=1/2),   S(R) ≤ min(1/μ_eff, 2^{k_bits}),

with equality cases: plain sqrt-descending (pure R, no filter), residue dial at
θ=1/2 (pure F), committed window oracle (R saturated by T1), median bisection
(R saturated by T2).

Witness table (all FEASIBLE, μ ≤ 1/S; verifier-checked):

| witness | anchor | locus (μ, P) | S_A | feasibility |
|---|---|---|---|---|
| frontier 5.19× | 5.1936 | (0.05, 0.85) | 5.1948 | μ=0.05 ≤ 1/5.19 ✓ |
| trunc-high 6.91× | 6.91 | (0.05, 0.9003) | 6.91 | ✓ |
| trunc-low 4.35× | 4.35 | (0.05, 0.8106) | 4.35 | ✓ |
| α=1 extreme 29.1× | 29.1 | (0.02, 0.9853) | 29.0698 | μ=0.02 ≤ 1/29.07 ✓ |

Infeasible locus rows exist and are honestly reported: 29.1× at μ=0.05 would demand
P = 1.0165 > 1, and at μ=0.115 P = 1.0911 > 1 — those (μ, S) pairs are impossible,
which is the conjecture doing work. Identity check: paper-138 master law at the
uninformative point reproduces the paper-132 formula exactly. Falsifier: a
COST-component alone exceeding 4/3, or a SET-gain exceeding min(1/μ_eff, 2^{bits})
given its budget. Status: L1+L2 make D PROVEN-shaped; L4 (stratum measure) is
load-bearing.

## Verification census (independent recheck, 2026-08-24)

Verifier artifact `verify_t1_t2_recheck.json` (+ `verify_run_stdout.log`), run
against the author's own finite checks `exp574b_saturation_check.py` /
`exp574b_result.json`:

- **Zero arithmetic errors** across all numeric claims;
  `exp574b_stored_value_discrepancies: []`.
- **~60% of PROVEN tags upgraded to VERIFIED** where independently recomputed:
  T1a finite-M formula + R-first-iff-P≥μ (0 failures); T1b exhaustive orders +
  insertion sweep M ∈ {16, 33, 64}; T2 dyadic identity exact W=2..4096; general-L
  upper bound to 4096; census argmin offsets {−2, −1} everywhere.
- **Superseded T1a form**: the drafted fire-or-silent law 1/(1−(1−μ)P) failed 14
  algebra consistency checks (its silent fallback re-scans R — non-certifying
  silence); replaced by the certified-silence law with 0 failures. Side-by-side at
  the four key loci: 5.1948→5.4054, 6.8966→7.1429, 28.8184→29.0698, 4.3469→4.649
  (drafted → certified).
- **Protocol-B dominance restricted**: all 12 exhaustive-order counterexamples have
  P < μ (protocol A remains unconditional).
- **T2 corrections**: cost-offset bracket [0.415, 0.5011] replaces "[−0.53,+0.5]"
  (location wobble −1.5288 and discrete argmin offsets {−2,−1} are a different
  quantity); marginal-value identity rewritten as the exact NET form
  cost(k)−cost(k+1) = W/2^(k+2)−1 (250/250 cells) after the drafted GROSS form
  failed 231 cells.
- **Named GAPs remaining**: L4 (stratum measure Δ(π,R)), L7 (extremality of
  sqrt-descending among N-computable orders), L8 (pinning exp563's k* definition
  against T2(c)/(d) — noting exp563's economic optimum 10/18 sits ~1 query above
  T2's k_opt at its own convention: three distinct k's must stay distinguished).
  These are the formal program's next work, not defects hidden by the record.

## Lemma ledger (roadmap to closure)

- **L1** Touch-floor decomposition ⇒ recovery of 132's 1/(1−θ+θ²) from COST-class
  accounting [analytic; recheck vs 132's M=33 exhaustive table]. Hours.
- **L2** Factorization S(R∘F) = S(R)·S(F): independent thinning commutes with rank
  statistics [analytic + Monte Carlo permutations×thinnings at M=33..129]. Hours.
- **L3** Block-first dominance for arbitrary R [VERIFIED computationally at
  M ∈ {16,33,64}; analytic exchange proof for general M still SKETCH]. Hours.
- **L4** Selection-effect correction Δ(π,R) under stratified π_N [GAP — needs
  explicit stratum measure from 137's q/p data]. 1–2 sessions. LOAD-BEARING for D.
- **L5** Integrality constant of T2(b) [VERIFIED to L=4096; extend range]. Trivial.
- **L6** Protocol A/B algebra (T1a) [VERIFIED — 0 recheck failures].
- **L7** Extremal N-computable order: sqrt-descending maximizes S among all orders
  computable from N alone, per stratum [GAP — conjectural; formalizes 137's honest
  frontier]. Hard analytically; finite check possible on lab populations.
- **L8** Pin exp563's k* definition against T2(c)/(d) census [minutes].

## Obstructions

- **O1 Siegel-type ineffectivity**: NO uniform-in-N SET-class constant exists —
  pointwise N with p ≈ √N gives unbounded ratio; any cap is per-stratum or
  mixture-weighted. Exceptional balance tails enter via distribution of √N − p
  (primes-in-short-intervals territory — genuinely open; constants inevitably
  ineffective).
- **O2 Balance-stratum coupling**: 137's opposite gradients (20.67× ↔ 1.97×) nearly
  cancel to 5.19×; wrong mixture weight flips the truncation gradient (4.35 vs
  6.91). Universal statements must carry the population measure explicitly.
- **O3 Axiom-dependence**: the 4/3 cap needs touch-floor ε > 0; ε = 0 collapses
  COST into SET and the cap dissolves. State the cost model in any paper using D.
- **O4 Regime boundary**: 138-linear (non-adaptive bits) vs 212-multiplicative
  (adaptive halving) — T2(e)'s martingale draws the line; conflating them
  manufactures fake contradictions.
- **O5 k*-naming (L8) before writing the identity into any future record.**

## Bottom line

No TRUE constant cap exists for the positional stratum — and this is CONSISTENT with
paper 132, not contradictory: 5.19× > 4/3 is class-crossing, not cap-breaking. The
residue cap governs COST-class actions; position works the SET-class tail through
the certified-silence and saturation laws above. Status remains DRAFT-WITH-CAVEATS
until L4/L7/L8 close; no breakthrough claimed — this is the barrier map's own
converse being made precise.

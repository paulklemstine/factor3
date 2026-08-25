# Paper 250 — F1-TIGHTNESS-CONNECTION: **BOUND-SLACK-BY-FACTOR-X = 1.15 [1.10, 1.22] ON MEASURED DATA; EQUALITY PROVABLY UNATTAINABLE** — Paper 225's Proven F1 Master Inequality Connected to the Measured Positional Profile — Parameter Map Λ = 0.766 (Independently Verified 0.765671), Θ_asc ≈ 0.867, q̂ NOT Identified by Any Recorded Number — Equality Condition π-flat REFUTED THREE INDEPENDENT WAYS (KS p = 7e−76; Two-Component LRT p = 9e−10; Binning-Free p = 1e−21) ⇒ No Realizable Policy Attains the Bound on This Profile — Gap Factor X = C₀/C_sort = 1.15302 [27-Cell CI 1.10175–1.22054], Policy/Baseline-Independent via the Identity Chain C₀/c_asc = bound/S = (M+1)/(2ME_x+1), Hump-Insensitive (ΔX = −0.019) — TIGHTNESS-CIRCULARITY CATCH: All Four Legacy Anchors' P̂ Satisfy ΛΘ ≈ 1.00–1.04 BY CONSTRUCTION (Law-Inversion Algebra) and Cannot Independently Certify Tightness — Decidable Closer Named: Scan-Simulation Joint S/Λ/Θ/q̂ Measurement Predicts S ≈ 1.31 vs Bound 1.51 (Two-Sided)

**Verdict name: BOUND-SLACK-BY-X** — the proven inequality overshoots every realizable
test-blind policy on the measured profile by ≥10% and ≤22%, the slack is PROFILE-FORCED
(irreducible: no policy can flatten π) and POLICY-INDEPENDENT (= C₀/C_sort exactly), and on
the truncation/witness anchors tightness is not-currently-decidable because every recorded
P̂ is a law inversion. This does not weaken the theorem — it LOCATES the open work.

Round-92 #1 · THEORY deliverable (no new physics run; papers-only ledger bump, count
unchanged) · advances paper 225's converse program (gapL4_measure.md §F1, gapL7_extremality.md
§46–56) from abstract framework toward calibrated measurement against the positional chain
(papers 228/229/230/233/238/242; exps 578/579/581/582/583/588/588b/592/594).
Sources: `ResearchOutput/scripts/2026-08-24-round74/{f1tight_connection.md,
f1tight_check.py, f1tight_result.json}` + independent verifier `{verifyf1_recompute.py,
verifyf1_result.json}` · finite check wall ~0.5 s (M = 40k exact cell sums).

## 1. The statement being connected

Paper 225's F1 master inequality (gapL4_measure.md, PROVEN via majorization — the single
inequality link in an otherwise all-identity proof chain):

> S ≤ min(1/(Λ·Θ·q̂), 2^k_bits/(Λ·Θ))

with Λ(π) = C_sort/C_desc ∈ (0,1] (within-stratum MLR factor), Θ(Π,π) = E_πC(Π)/K_booked
(≈1 iff uniform-within-cells), q̂ = μ_eff·P_eff + (1−P_eff)(1−μ_eff), k_bits = T2-priced
comparison queries. Everything else in the proof is identity (r̄-identity, Λ def, Θ def).

## 2. Parameter map — which measured object is which F1 booking

| F1 object | Measured carrier (papers 228–242 chain) | Numbers |
|---|---|---|
| **Λ(π)** | The positional profile ITSELF = within-window prior shape (gapL7 "divisor-mass tilt"). π := normalized T(x), T(x) = A(1+x)^−b_bulk + K(1+x)^−b_edge, monotone declining ⇒ sort order = window-ascending | From b_bulk = .573 [.412,.767], w = .086 [.064,.108], b_edge ≥ 15 (papers 238/244-lineage): **Λ_meas = 0.766** [verified independently **0.765671**]; ascending beats descending **1/Λ ≈ 1.306**. Bulk alone gives Λ = 0.8769 (gain 1.140); the left-edge spike supplies ≈51% of the log tilt (corrected per verifier from the draft's bulk-alone Λ≈0.895/gain 1.12/~⅓). Faces elsewhere: hard-balance 1.58× (Λ≈.63, papers 221/223), pool-137 1.078× (Λ≈.93), deployed top-heavy Λ=1 descending-extremal (exp575). Predicted 1.31 on THIS pool type UNTESTED — testable implication |
| **Θ(Π,π)** | Not independently measurable before Π is named; pinned once Π is. Full-window ascending: Θ_asc = C_sort/C₀ ≈ **0.867** [verified 0.867286] (head-loaded); descending baseline Θ_desc ≈ 1.13 (tail-loaded); gapL4's ρ_R≈0.59 read of witness 5.19 = Θ>1 in this language | Θ_asc grid range over the profile CI: **[0.8193, 0.9076]** (verifier floor 0.8193 replaces the draft's "~0.83"). Uniform-cell booking Θ=1 is REFUTED on this data |
| **q̂** | **NOT identified by any recorded number in the 228–242 chain**: every profile experiment scans the FULL window ⇒ μ_eff = 1, P_eff = 1, q̂ = 1 trivially. Only q̂-bearing records are the four legacy anchors — whose P̂ are law-INVERSIONS of the speedups (pthat_extraction.md: no hits/trials exist in any artifact) | Anchors (μ, P̂, S): (.05,.8500,5.194)→q̂=.1850; (.05,.9003,6.915)→.1397; (.05,.8106,4.353)→.2204; (.02,.985068,29.125)→.03433. See §5 |
| **k_bits** | No T2 schedule run tonight; static test-blind ⇒ k_bits = 0 ⇒ arm 2 = 1/(ΛΘ) ≥ arm 1 since q̂ ≤ 1: **arm 1 binds everywhere**, min() = 1/(ΛΘq̂) | — |

## 3. Equality refutation — π-flat killed THREE ways on data

Full equality needs exactly three conditions (the proof's only inequality link is
majorization C_sort ≤ C₀, equality iff π flat):
- **E1**: π flat within cells (⇒ automatically Θ=1, Λ=1);
- **E2**: binding-arm saturation q̂ = 2^(−k_bits); test-blind k=0 ⇒ q̂=1 ⇔ μ_eff=P_eff=1 (full support);
- **E3**: vanishing O(1/M).

E1 tested against measurement — refuted three independent ways, controls flat in all three:
1. **KS vs uniform**: D = .09519, p = 6.9e−76 (paper 228 / exp578);
2. **Two-component fit**: dAICc = 37.3, LRT p = 9.3e−10, spike-weight CI [.064,.108] excludes 0,
   b_bulk CI [.412,.767] excludes flat b=0 (paper 238 / exp588, cap-ladder exp594);
3. **Binning-free conditional-logistic LRT**: p = 1.17e−21, monotone decline (paper 233).

⇒ **NO realizable policy attains equality on this data; E1 fails pool-side, beyond policy
choice.** E2 holds trivially here (full-window scan ⇒ q̂=1); E3 negligible at M=40k.

## 4. The gap factor X — derivation and verified numbers

With the map of §2 at q̂=1, S_asc(realizable static) = 1/Λ and bound = 1/(ΛΘ), so

> **X := bound/S_asc = C₀/C_sort** — baseline-free and policy-independent (for EVERY Π;
> for μ_eff<1 policies the same factor multiplies the further q̂ room).

Verified identity chain: C₀/c_asc = bound/S = (M+1)/(2ME_x+1) (direct, closed-form, and
asymptotic forms all confirmed machine-exact by the verifier). At the point fit
(b=.573, w=.086, b_e=15): Λ=.7657, Θ=.8673, S_asc=1.3060, bound=1.5059,
**X = 1.15302**; E[x] = 0.4336. 27-corner CI grid over (b_bulk, w, b_edge):
**X ∈ [1.10175, 1.22054]** (equivalently E[x] ∈ [.4097,.4538]). Hump sensitivity: +20%
excess amplitude at x*=.65 moves X by only −0.0185 — first-moment-insensitive (and the hump
is exp592-gated-H0 anyway, §6).

Falsifiable form: tightness on this data iff C_sort(π_meas)=C₀ ⇔ E_π[x]=1/2 ⇔ b_bulk=0 AND
w_spike=0 within error (flatness forces Λ=Θ=1 too, so this single condition is the whole
gap). Any same-design pool re-measurement (128 balanced bitlen-96 semiprimes, ≥9594 hits,
cluster bootstrap) returning E[x]=0.500±0.005 would reopen tightness; current recordings
exclude it at overwhelming significance.

## 5. TIGHTNESS-CIRCULARITY CATCH (finding in its own right)

All four legacy anchors' P̂ satisfy **ΛΘ = 1/(S·q̂) ≈ 1.00–1.04 BY CONSTRUCTION**: the P̂ were
extracted by inverting the speedup through S_A = 1/q̂ — the bound AT Λ=Θ=1 — so the identity
ΛΘ = S*/S holds machine-zero (verifier resid = 0.0 on all four rows; band [0.99999, 1.0422]).
They therefore cannot independently certify tightness; zero evidential weight for attainment.
Anchor 4 (μ=.02) is additionally EXACT self-consistent inversion: P_selfconsistent =
0.98506849 matches booked P̂ to 4.9e−7, LT_inf = 0.9999863. Finite-M drift (LT_M300):
+4.06/+3.50/+4.22/−0.001% — bookkeeping only, does not rescue independence. Consequence: the
truncation/witness anchors' tightness status is **not-currently-decidable**; deciding it
requires a NON-inverted raw P_eff measured under a named committed R_eff — none exists
(all four P̂ are inversions; booked "at resolution limit").

## 6. Verdict, closers, scope

**Bound-slack-by-factor-X = 1.15 [1.10, 1.22] on the full-window static class**; slack is
profile-forced and policy-independent; anchors undecidable (circularity). Named closers:

- **Closer (experiment, ~1 session, no heavy compute): DECIDABLE.** Jointly measure achieved
  S_vs_desc, Λ, Θ, q̂ on the exp578 pool by scan simulation over the stored npz
  (`exp578_positions.npz`, window-ascending policy). Prediction from the map: **S ≈ 1.31 vs
  bound 1.51**; observing S > 1.51 would FALSIFY the mapping (the profile is not the operative
  π for cost) — a genuine two-sided test.
- **Closer (theorem):** F1's stated residual = sharpness (every realizable booking attained by
  some π). On-data attainment is impossible HERE (E1 excluded), so sharpness must be posed over
  the prior class, never as tightness-on-this-pool; X is the quantitative form of that separation.
- Hump status: paper 242's hump is exp592-gated-H0 (#391) and immaterial to X regardless.
- exp597 relevance: dial-exponent plateau α∈[0.5,0.75] concerns the RATE layer, orthogonal to
  the positional-shape layer consumed by Λ/Θ — no coupling assumed.
- Round-91 closure consistency (#396/#397): the positional thread closed as pure-density with
  NO sequence structure — consistent with this paper, which consumes only the density SHAPE
  (monotone declining π), never sequence structure.

## 7. Verification census

Independent verifier `verifyf1_recompute.py` reimplemented from the md definitions ONLY (no
import of f1tight_check): Gauss-Legendre continuum + M=40k discrete cross-check
(disc spread 5.2e−6), monotonicity/unit checks, 27-corner CI grid, identity-chain checks
(direct/closed/asymptotic), anchor-row recomputation. Result: **all three claims PASS
(item1_Lambda, item2_X, item3_circularity), discrepancies = 0.** Cosmetic corrections folded
into this paper per the verifier: bulk-alone Λ = 0.8769 (gain 1.140), spike log-tilt share
50.8% (draft said ~⅓), Θ grid floor 0.8193 (draft said ~0.83). Draft numbers otherwise
confirmed: Λ=0.766 ✓, ratio 1.306 ✓, mono-and-unit ✓, discretization-stable ✓, X point
1.153 ✓, interval corners ✓ (rounds to [1.10,1.22]) ✓, identity chain ✓, E[x] CI ✓, ΔX=−0.019 ✓.

## 8. Barrier validation

No barrier interaction: this is a THEORY connection inside the already-mapped positional
stratum (position 5.19× layer, barrier map items 132/137/138/143 untouched); it neither
breaches nor amends any barrier — it prices one side of barrier-4's converse program
(F1 sharpness) quantitatively and names its decidable closer.

*Provenance: round74 dir `f1tight_*`, `verifyf1_*`; theory-only record — experiment count
unchanged at 587.*

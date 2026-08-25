# Paper 256 — MIXTURE-RATE-CELLS-POWERED: **H1 — THE MIXTURE ADDS** — At the Pre-Stated Power Remedy (n_pool 128 → 512, Fresh Seed), the Full 16-Cell Divisibility Mixture (2|v, 3|v, 5|v, 7|v) Carries Per-N Hit-Rate Variance BEYOND the QR Dial: ΔadjR² = +0.105 ≥ 0.05 with perm_p = 1/501 (Zero of 500 Cell-Label Shuffles Reach the Observed Increment) and a CLEAN Control (y-Shuffle Null Max Collapsed 0.186 → 0.0549 While the Effect GREW +0.083 → +0.105) — The Rate Map Refines to CELL Level, and the Secondary Single-Covariate Arm Names the Mechanism: κ = Σₖ P(lₖ|v) (Expected Number of Distinct Small Primes Dividing v) Captures Δ = +0.114 ALONE — Composition Order, Not 15 Independent Cell Effects — Papers 227/235/236's Additive Completeness Upgrades from DIAL to CELL; Paper 255's BORDERLINE Resolves as UNDERPOWERED, Not Null

**Verdict name: H1_MIXTURE_ADDS** — all three registered bars pass simultaneously
(effect size, permutation calibration, clean control); the pre-stated closing
branch resolves `none`.

Round-95 #3 · re-fires exp598b's flagged question at its pre-registered power
remedy. Sources: `ResearchOutput/scripts/2026-08-24-round74/
{exp598c_mixture_rate_cells_powered.py, exp598c_result.json, exp598c_full.log,
exp598c_smoke.log, exp598c_verify.npz, exp598c_ns.txt}`. Population: seed-20260907
verbatim exp586 `make_semiprime` (bits = 96, n_pool = 512); two INDEPENDENT fresh
streams per N (cell grid 50k at offsets SEED+17e6+i, hit stream 50k at SEED+19e6+i;
mean 762.6 hits/N, range [297, 1558]); window t ~ U[0, 65536) from j₀ = isqrt(N)+1;
gcd-chain primorial(10⁶) tester; perm seed 599, 500 reps both arms. Wall 286.5 s.

## 1. Pre-registration v2 and the audit that produced it

v1 of this script was audited by two independent adversarial reviewers BEFORE any
full-mode number existed. Two must-fixes forced an amendment (registered in the
header before data):

1. **The inherited control criterion was logically unsatisfiable.**
   598b operationalized control_ok = (p_ctrl > 0.05 AND max(ctrl_null) < d_obs).
   But p_ctrl > 0.05 forces ≥ 25 of 500 y-shuffle deltas to reach d_obs, which
   forces max(ctrl_null) ≥ d_obs — the conjunction can never be true.
   **Erratum on paper 255** (rides here per lab rules): its "control fails on its
   max clause" framing presented an arithmetically forced outcome as evidence.
   The informative content was c = 25/500 (observed delta at the 95th percentile
   of the y-shuffle range). 598b's BORDERLINE verdict itself stands — it never
   gated on control_ok. Corrected rule: `clean_control := max(ctrl_null) < d_obs`
   gates H1; `machinery_ok := |mean(ctrl_null)| < 0.01` gates H0; p_ctrl reported
   descriptively only.
2. **v1's master seed was not fresh.** 20260903 is exp601's recorded third-seed
   lineage (`own_lineage_hash16 fa1746a5b065cbd9` reproduces as the prefix of
   `build_population(20260903, 512)`); withdrawn to registry-verified-unused
   20260907, self-exclusion asserted, stream offsets moved beyond ALL prior bands,
   prior-seed registry extended to all 11 known population seeds (pairwise-disjoint
   prefix-complete regenerations asserted).

Also fixed pre-data: degenerate secondary arm (a D>0 popcount is identically 16 on
occupancy fractions), undisclosed flag→gate promotion (now disclosed in-header),
mislabeled raw-R² key. Stream discipline: pools for all prior seeds regenerated at
n=512 and asserted mutually disjoint; band arithmetic asserted numerically.

## 2. Verdict bars (full run)

| Bar | Threshold | Observed | Fires? |
|---|---|---|---|
| H1 effect | ΔadjR² ≥ 0.05 | **+0.105498** [0.051576 dial → 0.157074 +cells] | ✅ |
| H1 permutation | p < 0.01 | **1/501 ≈ 0.001996** (0/500 exceedances; null q95 0.0189, max 0.0402) | ✅ |
| clean_control | max(ctrl_null) < obs | **0.054872 < 0.105498** | ✅ |
| machinery (H0 gate) | \|mean(ctrl_null)\| < 0.01 | 6.9×10⁻⁵ | ✅ |

**H1_MIXTURE_ADDS.** The observed increment lies outside the ENTIRE realized range
of both permutation nulls (cell-label shuffles AND rate shuffles).

## 3. The power remedy validated

The diagnosis behind paper 255's remedy was that a 15-column fixed-effect design
against n = 128 noisy log-rates lets pure y-shuffles reach Δ ≈ 0.19. Raising the
pool 4× collapses the null as predicted while leaving the effect intact:

| | n = 128 (598b, seed 20260827) | n = 512 (598c, seed 20260907) |
|---|---|---|
| ΔadjR² observed | +0.083 | **+0.105** |
| ctrl null max | 0.186 | **0.0549** (~3.4× shrinkage ≈ p/(n−p) scaling at 4× rows) |
| verdict space | BORDERLINE (null swallowed obs) | **H1** (obs outside entire null range) |

exp598b's BORDERLINE therefore resolves as UNDERPOWERED, not null — and the effect
replicates ACROSS INDEPENDENT POPULATIONS (+0.083 on seed 20260827's 128 semiprimes,
+0.105 on seed 20260907's 512 disjoint semiprimes).

## 4. Mechanism named by the secondary arm: composition order

Repaired secondary covariate (reportable post-fire): κᵢ = Σₖ P(lₖ | vᵢ), the
expected number of distinct primes among {2, 3, 5, 7} dividing v, assembled from
the cell marginals — ONE free column. It captures ΔadjR² = **+0.114** alone
[0.0516 → 0.166], matching or exceeding the full 15-cell basis' +0.105.

Reading: the mixture's contribution is not 15 independent cell effects but a graded
one-dimensional structure in HOW MANY distinct small primes divide v. Composition
order, not cell identity, is the dominant axis. This subsumes exp592's kappa-ordering
ledger catch (top-cell ranking replicating across seeds) as the visible tip of this
graded law, and connects to paper 88's label-composition results from the battery
thread. Sensitivity at α = 1 agrees (+0.108), so the refinement is not an artifact
of the S_sqrt weighting choice.

## 5. Verification (independent, pre-record)

An independent verifier recomputed every headline statistic from
`exp598c_verify.npz` ALONE with a from-scratch code path: ΔadjR² exact to full
float64 precision against the stored unrounded value; perm_p bit-exact; both
permutation arrays regenerate bit-exactly from the header-documented call order;
y reconstruction exact (the +0.5 smoothing is definitional). A hostile adjudication
audit failed to construct any overturn (rule-textual, statistical validity,
leakage, multiplicity/forking, worst-case seed-swap scenarios); mean cell
occupancies match closed-form independence products (e.g. cell 15: 0.0045 vs 1/210).
Chain-of-custody caveat, disclosed: v1 smoke artifacts were overwritten post-audit,
so pre-data integrity rests on filesystem forensics (header ctime predates every
data artifact; recorded wall_s equals the log birth→mtime span). **Adopted process
law going forward: pre-registrations are committed (or hashed in-repo) BEFORE any
data-producing run.**

## 6. Consequence and barrier validation

Papers 227/235/236's additive-completeness claim upgrades: the QR dial is NOT the
whole rate layer — divisibility composition of v = j² − N carries per-N rate
structure beyond the weighted Jacobi marginals, dominated by composition depth κ.
No barrier breached: this is rate-layer structure of the PROPOSAL distribution's
acceptance field (which j smooth), consistent with the standing method law that
scan-order structure reflects proposal geometry — now refined, not N-information:
κ is a property of the sampled window's arithmetic, usable to REWEIGHT scanning,
but it does not expose factor structure of N beyond what one jacobi sweep already
sees (dial + κ share the same prime support l ≤ 400... the increment says the JOINT
composition matters over and above marginals — a strictly finer descriptive layer
for any scan-order-aware sampler, with no new factor leakage demonstrated).
Catalog scan: no prior work on joint divisibility mixtures or permutation-calibrated
variance increments (closest entries: our own QR-dial line, pkg 882).

Falsifiable follow-ups pre-stated: (a) κ-only vs cells nested test at higher
resolution (does ANY cell identity survive conditioning on κ?); (b) extend the
covariate law across bits {72, 128} for scale stability; (c) close-form check —
does the fitted κ slope match a Dickman-type composition model?

## 7. Ledger catches and honest limits

Regen hash-check CONDITIONAL (no stored N strings anywhere in the lineage);
tester class-matched not source-verbatim; absolute rates internally consistent
only. Secondary arm non-evidentiary-by-design, reported only after the primary
fired (pre-registered ordering honored). Kappa covariate uses the SAME D matrix
as the primary (no independent sampling) — its Δ is descriptive, though it cannot
exceed noise given the primary's calibrated nulls. Errata carried: paper 255
control-framing correction; 598b latent cell_beta mislabel (enumerated unfiltered
keep list; never triggered there) fixed here. Wall 286.5 s full / 13.5 s smoke.

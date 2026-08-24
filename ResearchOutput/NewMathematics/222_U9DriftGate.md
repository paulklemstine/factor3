# Paper 222 — U9-DRIFT-GATE: The Fresh-Seed Arbiter Kills the Sub-1 Candidate by SIGN FLIP (Seed 20260825 Reads r = 1.15 SURPLUS Where the Entire 20260824 Family Read Deficit) — Randomness Stands Through u ≈ 11 Now Carrying a Measured ±5–15% Single-Run Fluctuation Envelope

**Verdict name: RANDOMNESS-EXTENDED / GATE REJECTED** for exp569c, the decisive
arbiter leg queued by paper 220. The twice-gated sub-1 candidate deviation is
**DEAD**: the only run uncontaminated by the 20260824 seed family returns point
estimates on the OPPOSITE side of unity, with nominally excluding-upward
intervals of the same size the deficit side used to argue candidacy. Directional
instability across seeds is the signature of seed-level fluctuation, not of an
effect; gate **G1 fails by sign**, which is stronger than failing by magnitude.
No replacement deviation is banked from the surplus either — it is a single seed
inside the very fluctuation envelope this run measures. The night's tension
(papers 214→216→220) closes cleanly: the correlated-family deficit was one
seed's shared fluctuation, and the honesty arc (bank → gate → clean rejection)
is complete.
Round-76 #2 · exp **569c** (id convention per papers 219/220: letter-sub-id
under the exp569 script lineage; count advances, max id does not) · assessment
v329 · script `exp569_u9_drift_power.py` (seed-parametrized version committed
with the exp569b artifacts, reused unchanged) · canonical artifact
`exp569_c_result.json` (full-precision rates + raw per-cluster counts persisted)
· **seed 20260825** — the ONLY run of the series whose master stream is disjoint
from every prior leg (pilot/G1/B all drew from 20260824; paper 220's ledger) ·
128 band-9 semiprimes, bitlen-96 balanced · 600,000 samples/N × 128 =
**76,800,000 pairs** · wall 5296.9 s (88 min).

## Question

Paper 220 left exactly one live branch: every dataset from master seed 20260824
— pilot (paper 214), G1 (exp569), B (exp569b) — jointly pointed 3–5% below 1,
but they were ONE seed's evidence; the corrected pilot×B joint (0.9596
[0.9226, 0.9966]) carried 19%-shared population and was explicitly barred from
confirmation-grade use. The pre-stated arbiter: rerun the identical pipeline at
a genuinely fresh stream, seed 20260825. Decision rule, registered in advance
(paper 220 §Result 3): land below 1 with pooled exclusion downward ⇒ the
candidate passes G1 (modulo G2) and the lab claims its first scale-smoothness
deviation; return to 1 ⇒ the pooled exclusion was shared-seed fluctuation and
randomness stands tightened. Exp569c is that run.

## Pre-registration status

Script header unchanged from exp569/exp569b: H1 (drift real) requires the
cluster-boot 95% CI of r to EXCLUDE 1 **downward** at cut 1e5, then gates G1
(fresh-seed replication) and G2 (control-integrity audit). H0 (randomness) is
the complement. The paired-control design (same bit length + 3-bit mantissa
head), cumulative segment-primorial gcd-chain tester, and NB=2000 percentile
cluster bootstrap are unchanged; decision cut 1e5, 1e6 secondary (better powered,
weight disclosed).

## Result 1 — the arbiter numbers (from persisted raw counts)

| quantity | cut 1e5 (PRIMARY) | cut 1e6 (secondary) |
|---|---|---|
| pairs | 76,800,000 | 76,800,000 |
| candidate events / rate | 2,598 / 3.38281 × 10⁻⁵ | 40,617 / 5.28867 × 10⁻⁴ |
| control events / rate | 2,252 / 2.93229 × 10⁻⁵ | 38,594 / 5.02526 × 10⁻⁴ |
| ratio r | **1.1536** | **1.0524** |
| cluster-boot CI95 (stored, in-run NB=2000) | [1.0541, 1.2686] | [1.0042, 1.1018] |
| CI95 (independent 4000-replicate rebootstrap from raw counts) | [1.0540, 1.2611] | [1.0051, 1.1016] |
| excludes 1 | YES — **upward** | YES — upward |

Both cuts read ABOVE unity, the 1e5 primary at +15.4%. Every arithmetic claim
above recomputes exactly from the raw per-cluster counts persisted in
`exp569_c_result.json` (sums 2598/2252 and 40617/38594 over 128 × 600,000).

## Result 2 — GATE REJECTED by sign flip

The gate G1 asked one question: does a genuinely independent seed REPLICATE the
sub-1 drift? It did the opposite:

| leg | seed family | cut 1e6 r | direction |
|---|---|---|---|
| pilot (paper 214) | 20260824 | 0.9468 | deficit |
| G1 (exp569) | 20260824 | 0.988 | deficit |
| B (exp569b) | 20260824 | 0.9623 | deficit |
| **C (exp569c, this)** | **20260825** | **1.0524** | **surplus** |

The three correlated legs' shared deficit (−1% to −5%) and the clean seed's
surplus (+5% at 1e6, +15% at 1e5) cannot both be signal; under any model with a
seed-stable effect they contradict. The pre-registered confirmation branch
required below-1 replication; what arrived is an above-1 non-replication of
larger magnitude. **H1 fails at G1 by sign** — no G2 audit is even reached, and
the once-banked drift, twice-gated candidate, and corrected-joint exclusion all
collapse into "fluctuation of one seed family."

## Disposition of the surplus (symmetric skepticism)

The fresh seed's own intervals nominally exclude 1 upward. This is **not**
re-banked as a new candidate: it is a SINGLE seed, the exclusion edge sits
inside the ±5–15% per-run envelope quantified below, and banking it would
repeat — in mirrored form — exactly the error the lab-wide seed-distinctness
rule was written to prevent (treating one seed's draw as evidence). At face
value a real surplus would mean x²−N candidates SMOOTHer than matched randoms
at u ≈ 10 in this seed; recorded as fluctuation, not claimed as an effect.

## Audit trail (both pre-disposition alarms resolved; ledger-grade)

1. **Coordinator false alarm — terminal-formatting display artifact.** On first
   read, the stored point looked OUTSIDE its own CI. Cause: a `:.5f` terminal
   print collapsed the candidate rate 3.3828125 × 10⁻⁵ to "0.00003", and the
   ratio was mentally formed from the rounded string. The persisted full-precision
   rates recompute cleanly; the point sits inside its interval everywhere. No
   script defect — the paper-220 precision patch demonstrably worked (the JSON
   carries exact rates; the display layer, not the storage, rounded).
2. **Independent rebootstrap reproduces the stored CI.** A fresh 4000-replicate
   percentile cluster bootstrap run directly on the persisted raw counts gives
   [1.0540, 1.2611] at cut 1e5 vs the stored in-run [1.0541, 1.2686] — lower
   edges agree to 4 decimals, upper edges differ by percentile-ordering noise;
   both exclude 1 identically. The stored inference is reproducible from raw data
   alone, closing the loop opened by exp569's unrecoverable-display defect.
3. **Cluster structure honest — the overdispersion is real and quantified.** Top
   candidate-N clusters carry 600/561/540 hits vs a control-side maximum of 359:
   genuine per-N heterogeneity, the mechanism behind the ±5–15% single-run CI
   widths. Consequence, stated as law for this frontier: ANY single run at this
   power (~77M pairs, 128 Ns) cannot resolve a few-percent smoothness deviation;
   the b/c contrast measures that resolution floor directly.

## Final synthesis — the u ≈ 10 question closes (papers 214→216→220→this)

- **No deviation survives.** The once-banked sub-1 drift failed its fresh-seed
  gate by sign; the correlated-family deficit is explained as one seed's shared
  fluctuation; the clean seed returns an equally-sized opposite-signed draw.
  The two genuinely distinct seed-families BRACKET 1 from opposite sides —
  which is precisely the randomness result.
- **Randomness STRENGTHENED, now with a noise floor.** The papers
  130/209/214/216 null line extends through u ≈ 11 carrying a MEASURED per-run
  fluctuation envelope (roughly ±5–15% at these powers). Any future deviation
  claim at this frontier must beat that envelope by multi-seed pooling under
  the seed-distinctness rule — a single-run CI, however narrow it looks, is
  structurally incapable of resolving few-percent effects here.
- **Named follow-up condition (only if reopened):** ≥ 3 truly distinct master
  seeds pooled inverse-variance (σ_joint ≈ 0.02 achievable), WITH the burden of
  explaining why seed-family a/b saw deficit while seed-family c saw surplus.
  Absent a mechanism for sign-stable selection of runs, the null stands.

## Mechanism note (interpretive, held at zero evidential weight)

Direction matters for the archive: paper 136's sieve-advantage direction has QR
restriction compensating x²−N pools (SMOOTHER candidates); the dead candidate
was a DEFICIT (opposite sign, hence "new weak effect" if real); this run's
surplus points back toward the compensation direction but at u ≈ 10 rather than
the QR regime, single-seeded, inside the envelope. Nothing to attach it to. The
sign instability ACROSS seeds is itself informative: whatever small wobble
exists in the b/c contrast is dominated by which-N clustering, not by any
N-invariant smoothness coupling.

## Ledger

1. **Coordinator display-formatting false alarm** (audit item 1): `:.5f`
   collapsing 3.38e-05 → "0.00003" manufactured an out-of-CI appearance during
   triage. Resolved against persisted raw counts; lesson generalized — ratio
   checks must read the JSON's stored fields, never terminal renderings.
2. **pkill self-match killed the first c-launch.** A cleanup pkill matched the
   launcher's own process name; relaunch clean, documented in-session. No data
   contamination (the killed process had emitted nothing).
3. **Seed parameterization provenance.** The `--seed` argument was added to
   `exp569_u9_drift_power.py` after paper 220's shared-stream catch and committed
   with the exp569b artifacts; exp569c reused it unchanged — the first run of the
   lineage born seed-distinct rather than patched after the fact.
4. **Script verdict_name vs recorded verdict.** `exp569_c_result.json` carries
   `"verdict_name": "CANDIDATE-DEVIATION-PENDING-GATES"` — the correct
   STANDALONE label (its own 1e5 CI excludes 1) under the header rule, written
   before any cross-seed knowledge exists. The pre-registered gate structure of
   paper 220 then consumes it: G1 requires downward replication, which failed by
   sign. Recorded verdict RANDOMNESS-EXTENDED governs; the JSON field is kept as
   an honest snapshot of the within-run state.

## Barrier validation

Scale-smoothness frontier u ≥ 6–14 (standing asymptotic directive): this is a
NULL that strengthens the map. Size-matched-random smoothness now holds through
u ≈ 11 with a quantified noise floor (±5–15% per run at 77M pairs), converting
"no deviation found" into "no deviation of less than X could have been seen" —
the honest deliverable the H0 branch always promised. No barrier breached, no
method proposed, no constant shaved; the rejection retires a candidate, it does
not open a channel.

## Conclusion

The arbiter spoke and killed the candidate: seed 20260825 reads 1.1536
[1.0540, 1.2611] at the decision cut where the entire 20260824 family read
deficit — a sign flip, which is gate failure at its most decisive. The
twice-gated sub-1 drift dies; the corrected joint that nominally excluded 1
downward is fully explained as one seed's fluctuation; no surplus is banked in
its place. What remains is stronger than a bare null: a mapped fluctuation
envelope (±5–15% per run, cluster-overdispersion-driven, top-N clusters
600/561/540 vs control-max 359) that future deviation claims must beat with
multi-seed pooling under the seed-distinctness rule. The complete honesty arc —
bank (214), powered-null downgrade (216), letter-of-rule null with independence
audit (220), clean sign-flip rejection (this) — is closed. Id convention:
recorded as experiment **569c** under the exp569 script lineage (sub-experiment
letters denote reruns reusing the parent pipeline unchanged; the experiment
COUNT advances, the max-id tracker does not). Now 563 experiments (max id 572).
Assessment v329. Paper 222, issue #368.

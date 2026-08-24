# Paper 220 — U9-DRIFT-POWER-B: Letter-of-Rule Null at 76.8M Pairs; Both Cross-Run Poolings Fail Independence (Shared Stream Swallows G1; Pilot's Whole Band-9 Pool Sits Inside B) — the Sub-1 Signal Becomes a Twice-Gated Candidate Awaiting Seed 20260825

**Verdict name: RANDOMNESS-EXTENDED** for exp569b as run, per the pre-registered
rule's letter — neither cut's standalone cluster-boot CI excludes 1, so no gate
armed. But the headline is the honest two-sided state this run leaves behind: a
**letter-of-rule null** alongside a **sharpened cross-run sub-1 signal
(~4% deficit, ~2.1σ nominal) whose CONFIRMED status is BLOCKED**, because every
available pooling fails an independence requirement — the original three-seed
joint was retracted before publication (runs G1 and B share one RNG stream), and
the corrected pilot×B pooling fails a second, newly verified dependence defect
(paper 214's pilot population is generated from the *same* master seed and is a
literal subset of B's). The single clean arbiter is the relaunched fresh-stream
run at seed **20260825**, queued as the named decisive step.
Round-75 #3 · exp **569b** · assessment v327 · script `exp569_u9_drift_power.py`
(precision-patched; canonical artifact `exp569_b_result.json` stores FULL-precision
rates + raw per-cluster counts — the exp569 display defect cannot recur) ·
seed family 20260824 (+1000+c per worker chunk) · 128 band-9 semiprimes,
bitlen-96 balanced · 600,000 samples/N × 128 = **76,800,000 pairs** (2.15× the
paper-214 pilot, 4× exp569) · wall 5233.6 s (87 min) at 68.1 µs/value.
Recorded after round-75 #4 due to compute wall-clock (rounds may record out of
numeric order).

## Question

Papers 214→216 left the band-9 x²−N smoothness question exactly poised: the
pilot banked direction-stable sub-1 drift (−5.3% @ 1e6, −13.6% @ 1e5, all CIs
covering 1), the powered replication exp569 returned null and downgraded the
tension to "open at reduced weight", with the joint point near −3%. Exp569b is
the third leg: another long run at matched conditions (band 9 only; bands 10/11
still deferred) intended as one more independent seed to tighten the joint and,
per the pre-registration, decide drift-vs-noise.

## Pre-registration (script header, carried unchanged into this run)

- "H1 (drift real): cluster-boot 95% CI of r EXCLUDES 1 (downward) at cut 1e5 =>
  … CONFIRMED-DEVIATION (would be the lab's FIRST scale deviation)" — claimable
  ONLY after BOTH gates: **G1** fresh-seed replication (second independent
  seed/population, same pipeline); **G2** control-integrity audit (paired
  mantissa/bitlen match exact; tester identical code path).
- "H0 (randomness): CI covers 1 => verdict RANDOMNESS-EXTENDED; deliverable =
  tightened upper edge of |r−1|."
- Design unchanged from exp569/paper 216: cumulative segment-primorial gcd-chain
  tester (`classify`), PAIRED controls (same bit length + 3-bit mantissa head),
  cluster bootstrap NB = 2000 percentile CIs over N-individuals; decision cut 1e5,
  1e6 secondary with better power (weight disclosed).

## Result 1 — standalone (this run): both cuts cover 1 ⇒ H0 by the letter

| quantity | cut 1e5 (PRIMARY) | cut 1e6 (secondary) |
|---|---|---|
| pairs | 76,800,000 | 76,800,000 |
| candidate events / rate | 2,280 / 2.96875 × 10⁻⁵ (full precision, stored) | 37,255 / 4.85091 × 10⁻⁴ |
| control events / rate | 2,348 / 3.05729 × 10⁻⁵ | 38,718 / 5.04141 × 10⁻⁴ |
| ratio r | **0.9710** | **0.9623** |
| cluster-boot CI95 | **[0.8976, 1.0521]** | **[0.9224, 1.004]** |
| excludes_1 | FALSE ⇒ H0 | FALSE |

(Recorder correction: `exp569b_findings.md` prints the 1e5 point ratio as 0.981
via a rounded numerator "3.00e-5"; the exact stored rates give 0.9710. Verdict
unaffected — see Ledger 3.) Point ratios sit 2.9–3.8% below 1, both intervals
comfortably covering unity: no deviation flag, no gate arms, verdict
RANDOMNESS-EXTENDED stands for this run exactly as registered.

## Result 2 — POOLING AUDIT: both joints fail independence; the sub-1 signal is sharpened AND gated

**Retracted before publication (coordinator self-catch).** The working three-seed
inverse-variance joint at cut 1e6 — pilot 0.9468±.0449 × G1(exp569) 0.988±.0232 ×
B(this) 0.9623±.0208 ⇒ r ≈ 0.971, CI [0.942, 1.000] — treated G1 and B as
independent. They are not: **B is a strict superset of G1's draws.** Same fixed
SEED = 20260824, same per-chunk ctrl seeds SEED+1000+c, and the per-worker RNG
consumption is a deterministic function of the sample index, so B's first
150,000 samples per N replay G1's draws exactly (candidates and paired controls
alike). Pooling them separately double-counts one dataset. Retracted; no number
from that joint is cited anywhere here as evidence.

**Corrected joint (only two estimates, but still not clean).** Over the nominally
independent pair pilot × B at cut 1e6:
r_joint = (0.9468/0.0449² + 0.9623/0.0208²)/(1/0.0449² + 1/0.0208²) =
**0.9596, σ ≈ 0.0189, 95% CI [0.9226, 0.9966] — excludes 1 downward**
(deficit ≈ 4.0%, z ≈ 2.14). Taken at face value this is the sharpest sub-1
statement of the whole 214→216→220 arc. It is NOT confirmation, for a reason
found during recording (coordinator-directed verification):

**Defect 2 — the pilot population is not seed-distinct from B either.** Paper
214's script (`exp567_scale_u9_lift.py`) carries the SAME `DEFAULT_SEED =
20260824`. Its main RNG is unconsumed before pool building (the tester-validation
leg runs on a separate `val_rng = Random(seed+1)`), and its prime-start primitive
(`getrandbits(48) | (1<<47) | 1` → `next_prime`) is byte-identical to exp569's
`make_semiprime`. Reconstructing both pools from the pristine `Random(20260824)`
stream reproduces **identical opening draws and ALL 24 pilot band-9 semiprimes
inside B's 128-N pool (24/24 membership, zero feasibility rejects)**. So the
corrected joint shares 24 of B's 128 clusters (19%) with the pilot's entire
population: its nominal σ understates the true uncertainty by an unquantified
intra-N correlation. Mitigation, stated honestly: the shared Ns were *measured*
by disjoint machinery (phase-split windows + batch-strip tester in the pilot vs
uniform-j + gcd-chain paired controls here), so measurement noise is largely
distinct and the weighted-average POINT ≈ 0.96 remains meaningful — but the
EXCLUDES-1 edge of the corrected interval cannot be taken as clean evidence.

**Disposition (two-sided, both branches stated):**

1. **Letter of rule:** exp569b's own registered decision — standalone CIs cover
   1 at both cuts, no gate armed, verdict RANDOMNESS-EXTENDED.
2. **Cross-run signal:** a CANDIDATE DEVIATION (~4% deficit, ~2.1σ nominal)
   whose CONFIRMED status is **BLOCKED twice over**: gate G1's fresh-seed
   requirement was silently violated by the shared-stream design (Ledger 1), and
   the remaining pooling partner shares the population itself (Ledger 2). Under
   maximal skepticism the correct reading is: *every dataset drawn from seed
   20260824 — pilot, G1, B — points 3–5% below 1 jointly, but they are one
   seed's worth of evidence, not three.*

## Result 3 — named decisive next step: the genuinely fresh stream

The arbiter is the relaunched run at **seed 20260825** (`exp569_u9_drift_power.py
full 600000 c_ … 20260825`, background, ~87 min): a different master seed gives a
disjoint stream, disjoint populations, and the first fully independent estimate
of the arc. Decision rule, stated in advance: if the 20260825 estimate lands
below 1 such that the pooled independent set excludes 1 downward ⇒ the
CONFIRMED-DEVIATION candidate passes G1 (modulo the standing G2 audit) and the
lab claims its first positive scale-smoothness deviation at u ≈ 9–10; if it
returns to 1 ⇒ the pooled exclusion was shared-seed fluctuation and randomness
stands with the tightened null. No 20260825 numbers are cited in this paper.

## Mechanism note (interpretive, held at full skepticism)

The sign matters: a candidate-side DEFICIT (j²−N values less smooth than
size-matched randoms) is OPPOSITE to paper 136's sieve-advantage direction, where
QR restriction compensates for x²−N pools. If the ~3–4% is real it is therefore
a NEW, weak, u ≈ 10-scale effect — not the known QR-compensation mechanism
re-emerging — and it earns belief only when the fresh seed lands below 1.

## Ledger

1. **SHARED-STREAM DESIGN FLAW (coordinator self-catch, before publication).**
   Runs G1(exp569) and B share SEED = 20260824 end-to-end; B ⊃ G1 strictly. The
   three-seed joint built on their independence was retracted pre-record. Root
   cause: the script's SEED constant was never varied across the "replication"
   legs — "fresh seed" was claimed by population re-draw within a fixed stream,
   which the superset relation defeats.
2. **PILOT POPULATION OVERLAP (found during recording, coordinator-directed
   verification).** Paper 214's generator uses the same master-seed literal, an
   unconsumed-until-pools main RNG, and the identical prime-start primitive;
   stream reconstruction shows 24/24 pilot Ns inside B's pool. The corrected
   pilot×B joint inherits correlated clusters; its excludes-1 edge is reported
   but not trusted as confirmation-grade. Consequence adopted lab-wide going
   forward: **any "independent replication" leg must vary the master seed, and
   scripts must assert seed distinctness in-output.**
3. **Findings-file rounding slip (recorder correction).** `exp569b_findings.md`
   computes the 1e5 point ratio from a rounded numerator (3.00e-5 → "0.981");
   exact stored rates give 0.9710. Both readings cover 1; the primary verdict is
   untouched. The canonical JSON's full-precision rates govern.
4. **Precision patch verified in production.** `exp569_b_result.json` persists
   full-precision rates AND all raw per-cluster counts (ch5/ch6/ct6/kh5/kh6/kt6)
   — exp569's unrecoverable-display-defect class is closed for this lineage
   (patch flagged in-output: `r_cand_rounded_display_bug_fixed: true`).
5. **Wall accounting.** 5233.6 s (87 min) for 76.8M pairs at 68.1 µs/value;
   overshoot vs the naive pre-run estimate is documented as candidate-strip cost
   drift (j²−N residuals survive more gcd rounds than randoms), consistent with
   exp569's catch 2, partially offset by better amortization at 600k samples/chunk.

## Barrier validation

Scale-smoothness frontier u ≥ 9–14 (standing asymptotic directive): at the
letter-of-rule level this run STRENGTHENS the randomness line of papers
130/209/214/216 — size-matched-random smoothness now holds through a 76.8M-pair
band-9 cell, and the H0-branch deliverable (tightened |r−1| upper edge) improves
to 0.102 at the 1e5 cut and 0.078 at the powered 1e6 cut on this run alone. No
barrier breached, no method proposed, no constant shaved. The residual sub-1
tension is quantified honestly as a twice-gated candidate signal, not banked as
a feature and not dismissed: the seed-independence audit this run forced is
itself a permanent methodological gain for every future deviation claim.

## Conclusion

A 76.8M-pair third leg returns the pre-registered null (0.9710 [0.8976, 1.0521]
at the decision cut; 0.9623 [0.9224, 1.004] at the powered cut) while the
pooling layer beneath the program was audited and found wanting twice: the
three-seed joint died of a shared RNG stream, and the corrected two-estimate
joint (0.9596 [0.9226, 0.9966], nominally excluding 1) dies of population
overlap with the same master seed. Everything drawn from 20260824 is one seed's
evidence; it points 3–4% below 1 together, and only seed 20260825 can say
whether that is the lab's first scale deviation or the last breath of the
banked drift. Id convention: recorded as experiment **569b** under the exp569
script lineage (sub-experiment letters denote reruns reusing the parent pipeline
unchanged; the experiment COUNT advances, the max-id tracker does not). Now 562
experiments (max id 572). Assessment v327. Paper 220, issue #366.

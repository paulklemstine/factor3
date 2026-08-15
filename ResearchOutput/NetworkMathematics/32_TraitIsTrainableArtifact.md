# THE-INTERNALIZATION-TRAIT-IS-A-TRAINING-SOLUTION-PROPERTY-NOT-SEED-INTRINSIC — A No-Boundary Final Fine-Tune Converts 4/4 Known-Dependent Seeds to Self-Sufficient, With an Exact Same-Seed Replication Control and a Measured Reorganization Dip (NET-32)

**Program:** Network/LLM research lab — round-net-32 (mechanism axis; the constructive test that NET-31's "seed-fixed trait" and loop candidate (1b) both pointed at: is the eval-load-bearingness of the exclusive boundary block INTRINSIC to the seed, or a TRAINING ARTIFACT — a converged solution that gates on the block and was never weaned off it?)
**Date:** 2026-08-15
**Status:** Machine-verified (ALL_DONE_NET32). Six arms at E=23 (k=3), byte-identical EOSWidthGRU: the COMPLETE known-dependent population {13, 14, 15, 17} plus two known-self-sufficient controls {16, 18}. Each arm: standard 12000-step training (byte-identical to NET-29/30/31) → stage-0 (T=0) ctl+zeroN eval (doubling as an exact same-seed replication of the NET-31 labels) → fine-tune T extra steps with the EXCLUSIVE BLOCK ZEROED at the EOS step (the exact zeroN eval condition made a TRAINING condition), T ∈ {300, 1000, 3000} cumulative, eval ctl+zeroN at each stage and zero1@0/flip1@0/scale0.1 at T=3000. Fresh AdamW (lr 1e-3) for the fine-tune; fresh eval draws per (stage, manipulation).
- The four dependent seeds' stage-0 zeroN costs reproduce NET-31 to 4 decimals (0.7041/0.9014/0.7104/0.7437); the controls reproduce too (0.9932/0.9995). The conversion is therefore measured on the IDENTICAL solutions NET-31 labeled.
- The no-boundary fine-tune makes the exclusive block INERT in every arm: at T=3000, ctl, zeroN, zero1@0, flip1@0, and scale0.1 are all 1.0000 at n=8 in all six arms, and ctl (the block-present path at full trained magnitude) ends at 1.0000 in 6/6.

## Hypothesis and statement

NET-31 established the internalization law: at k≥2, the same four seeds {13, 14, 15, 17} build boundary-DEPENDENT recoveries (zeroN cost 9–30% at n=8) at BOTH k=2 and k=3, the same seven seeds self-sufficient ones, ~60/40, and the split is width-independent — no weight-based predictor was found (magnitude and sign structure refuted). The trait "seed-fixed" framing left open the constructive question: is the dependence a property of the SEED's optimization landscape (intrinsic), or of the SPECIFIC CONVERGED SOLUTION (a training artifact — a solution the search happened to find that leans on the block's aggregate norm and was never forced to operate without it)?

The cleanest discriminator is a TRAINING-TIME intervention: after standard training, fine-tune the trained model with the exclusive block ZEROED at the EOS step — the zeroN condition made a training condition. If the trait is a training artifact, the model can (re)organize a no-block solution and become self-sufficient; if it is intrinsic (the seed's landscape cannot reach a no-block solution from this starting point), the fine-tune should fail to convert it.

- **TRAINING-ARTIFACT:** the fine-tune converts all four dependent seeds to self-sufficient (zeroN becomes a no-op), the cure is preserved (ctl stays ~1.0), and — because zero1@0 was 0% (broke the cure) in EVERY trained k≥2 arm — after conversion ALL exclusive interventions are no-ops, proving the block is INERT (the block-gated solution path is gone), not merely compensated.
- **INTRINSIC-TRAIT:** at least one dependent seed cannot be converted (zeroN stays collapsed after the fine-tune), or the conversion trades the cure away (ctl collapses).

## Results

All numbers are n=8 full (all digits exact; chance 1e-9); n=5/6/7 shown where they differ. Binom. SE at 2048 draws: ≤0.5% at p≈1, ~0.9% at p≈0.7–0.9. "no-op" = |Δ| ≤ 1.2 SE; "converted" = zeroN within ~2 SE of ctl. Exclusive coords at T=0: |max| 0.562–0.670, mean|eos[0:20]| 0.146–0.200 — the trained solutions reproduce NET-31's (see the stage-0 column).

### Stage-0 replication (T=0, untouched trained arms) — n=8 full

| seed | NET-31 label | exclusive coords | ctl | zeroN | replication |
|---|---|---|---|---|---|
| 13 | DEPENDENT | +0.648 −0.651 −0.661 | 1.0000 | **0.7041** | exact (NET-29/30/31) |
| 14 | DEPENDENT | +0.581 +0.580 +0.571 | 1.0000 | **0.9014** | exact (NET-31) |
| 15 | DEPENDENT | −0.618 +0.655 +0.670 | 1.0000 | **0.7104** | exact (NET-31) |
| 16 | self-sufficient | −0.562 −0.533 +0.562 | 0.9985 | 0.9932 | exact (NET-31) |
| 17 | DEPENDENT | +0.588 −0.580 +0.529 | 1.0000 | **0.7437** | exact (NET-31) |
| 18 | self-sufficient | +0.627 −0.605 +0.606 | 1.0000 | 0.9995 | exact (NET-31) |

### The conversion curve — zeroN n=8 full as a function of no-boundary fine-tune steps T (ctl shown in parens)

| seed | T=0 | T=300 | T=1000 | T=3000 |
|---|---|---|---|---|
| 13 | **0.7041** (1.0000) | 0.9980 (0.9980) | 0.9746 (0.9785) | **1.0000** (1.0000) |
| 14 | **0.9014** (1.0000) | 1.0000 (1.0000) | 1.0000 (1.0000) | **1.0000** (1.0000) |
| 15 | **0.7104** (1.0000) | 1.0000 (1.0000) | 0.9390 (0.9351) | **1.0000** (1.0000) |
| 16 | 0.9932 (0.9985) | 0.7163 (0.7178) | 0.6763 (0.6924) | **1.0000** (1.0000) |
| 17 | **0.7437** (1.0000) | 1.0000 (1.0000) | 0.9980 (0.9980) | **1.0000** (1.0000) |
| 18 | 0.9995 (1.0000) | 1.0000 (1.0000) | 0.9150 (0.9263) | **1.0000** (1.0000) |

### T=3000 final state — all interventions, n=8 full

| seed | ctl | zeroN | zero1@0 | flip1@0 | scale0.1 | verdict |
|---|---|---|---|---|---|---|
| 13 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | **converted** |
| 14 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | **converted** |
| 15 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | **converted** |
| 16 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | (control, stable) |
| 17 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | **converted** |
| 18 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | (control, stable) |

## The law

**THE-INTERNALIZATION-TRAIT-IS-A-TRAINING-SOLUTION-PROPERTY, NOT-SEED-INTRINSIC — A NO-BOUNDARY FINAL FINE-TUNE CONVERTS 4/4 KNOWN-DEPENDENT SEEDS TO SELF-SUFFICIENT; THE CONVERSION IS FAST (≤300 steps in 5/6), CURE-PRESERVING (ctl ends at 1.0000 in 6/6), CAN BE NON-MONOTONE (a mid-fine-tune n=8 reorganization dip in 4/6 arms, always recovering by T=3000), AND LEAVES THE EXCLUSIVE BLOCK INERT (zero1/flip/scale — never training conditions — become exact no-ops).**

1. **The trait is a property of the converged SOLUTION, not the seed.** All four seeds in the complete known-dependent population {13, 14, 15, 17} convert to fully self-sufficient (zeroN n=8: 0.7041/0.9014/0.7104/0.7437 → 1.0000) after ≤3000 steps of fine-tuning under the zeroN training condition. The NET-31 "seed-fixed trait" is therefore not an optimization-landscape property — the no-block solution is reachable from every trained dependent solution, in ≤2.5% of the original training budget.
2. **Exact same-seed replication is the control.** Stage-0 zeroN reproduces NET-29/30/31 to 4 decimals in all six arms, and ctl is 1.0000 (0.9985 for s=16) exactly as published. The conversion is measured on the IDENTICAL trained solutions that NET-31 labeled dependent/self-sufficient — no re-labeling, no distribution shift.
3. **The conversion is fast:** zeroN reaches ≥0.99 (essentially converted) at T=300 in 5/6 arms (s=13 0.9980, s=14/15/17/18 1.0000), i.e. 300 steps = 2.5% of the 12000-step training budget. Only s=16 lags (0.7163 at T=300).
4. **The conversion CAN be non-monotone — the reorganization dip.** 4/6 arms show a transient n=8 dip at an intermediate stage (s=13 T=1000: 0.9746; s=15 T=1000: 0.9390; s=16 T=300: 0.7163 and T=1000: 0.6763; s=18 T=1000: 0.9150), always fully recovering by T=3000. The dip affects ctl and zeroN equally (the block is already inert by then), so it is a length-generalization reorganization of the no-block solution, not a boundary artifact. s=14 and s=17 convert cleanly (1.0000 at every stage). Design rule: fine-tune to full convergence; never deploy a mid-fine-tune state.
5. **The cure is preserved through conversion.** ctl (the block-PRESENT path at full trained magnitude) ends at 1.0000 in 6/6 arms at T=3000, and never falls below 0.6924 at any stage (s=16 T=1000, the dip). The fine-tune does not trade zeroN robustness for a broken cure.
6. **Post-conversion the block is INERT, not compensated.** At T=3000, ALL exclusive interventions — zeroN, zero1@0, flip1@0, scale0.1 — are exact no-ops (n=8 = 1.0000) in all six arms. This is decisive because zero1@0 cost 0% in EVERY trained k≥2 arm (NET-29/30/31): the trained block-gated solution required the FULL collective block (removing one coord broke it), so a no-op zero1@0 after conversion proves that block-gated solution path is GONE — the model switched entirely to the no-block path. The exclusive block is present at (near-)full trained magnitude yet has zero effect on the answer.
7. **Mechanism — dynamic stop-routing, NOT coord decay (honest correction).** The EOSCOORD-AFTER readout in the log (|excl| ≈ 0.06) is a MEASUREMENT ARTIFACT: it printed the eos buffer after the final scale0.1 eval without restoring it (scale0.1 multiplies the trained coords by exactly 0.1, and every arm shows exactly ×0.10 — 0.648→0.065, 0.581→0.058, …). The true post-fine-tune coords were not measured. Weight-decay math bounds them: under the zeroN training condition the exclusive coords receive ZERO gradient (they are excluded from the computation), so the only update is AdamW's decoupled decay (wd 0.01, lr 1e-3 → ~3% over 3000 steps) — the coords stay near ~0.97× trained magnitude (~0.6), not 0.06. Combined with Law 6, the mechanism is a DYNAMIC STOP-ROUTING: the recurrent dynamics cease to route the exclusive input into the answer path while the coords remain at training magnitude. A clean post-fine-tune coord readout is an open follow-up.

**Mechanism statement (supported at the behavioral level):** the dependent seeds' answer paths lean on the aggregate exclusive-block norm because standard training found a block-gated solution and never forced a no-block one; a ≤3000-step final fine-tune under the zeroN condition lets the model reorganize a no-block solution (reorganization is transient — it can pass through a length-gen dip), after which the exclusive block is present-but-inert: zeroing it, zeroing or flipping any single coord, or attenuating it ×0.1 all leave the answer unchanged, and the block-present path (ctl) is preserved. The seed trait is real at standard training (NET-31) but NOT intrinsic — it is a feature of the converged solution that a boundary-absent final phase removes, seed-independently.

## Verdict on the hypothesis

**TRAINING-ARTIFACT: CONFIRMED.** The complete known-dependent population {13, 14, 15, 17} converts 4/4 to self-sufficient under a ≤3000-step no-boundary fine-tune, with exact same-seed replication (stage-0), cure preservation (ctl 1.0000 in 6/6), and full block-inertness (all five interventions no-op). The trait is a property of the trained solution, not the seed's landscape: the no-block solution is reachable from every dependent starting point in ≤2.5% of the original training budget. **INTRINSIC-TRAIT: REFUTED** — no dependent seed resisted conversion. The NET-31 design rule sharpens from "≥3 exclusive dims ⇒ reliable success but ~60% self-sufficient internalization — keep re-serving the boundary token or verify per instance" to "**≥3 exclusive dims for reliable success, then a short (≤3000-step) no-boundary final fine-tune makes the block OPTIONAL, seed-independently** — one training-time protocol removes the internalization lottery." The seed-trait was never about the seed: it was about the search's default converged solution.

## Verification vs the network-loop barriers

- **(a) Circularity — clean, with the controls carrying the load.** The headline "zeroN becomes a no-op" is partially trained-in (zeroN IS the fine-tune condition). Non-circular because: (i) ctl — the block-PRESENT path at FULL trained magnitude (true coords ~0.6) — is preserved at 1.0000 (the fine-tune didn't collapse ctl to match zeroN); (ii) zero1@0/flip1@0/scale0.1 are NEVER training conditions, and all become exact no-ops — the training condition (all-zero block) does not by itself force invariance to sign-flipping or single-coord removal of a full-magnitude block; (iii) n=6/7/8 length-gen is perfect post-conversion though training is n=5-only — the no-block solution generalizes.
- **(b) Known-method-in-disguise — confronted.** "Fine-tune without the special/boundary token" is a known qualitative family (special-token-removal fine-tuning in LLM practice). Novel content: the EXACT law — the ≤300-step (2.5% of budget) onset, the 4/6 non-monotone reorganization dip (a specific deployability warning), full convergence by 3000 steps, cure preservation quantified, and Law 6's inertia result (the trained block-gated path is fully switched off, proven via the zero1-0%-at-k≥2 fact). The reframing of NET-31's "seed-fixed trait" as a solution property is the lab's own construction. Catalog re-checked — no prior on boundary/special-token deletion-robustness of length-general recurrences (closest: pkg 693/35 certified adversarial robustness via sheaf cohomology, input-space robustness — orthogonal).
- **(c) Toy-scale — confronted.** Same toy carry task (n=5 train, n=5–8 eval). The protocol (a final-phase boundary-absent fine-tune) is architecture-agnostic and is the natural real-scale recipe, but untested at scale; REAL-SCALE transfer remains the frontier.
- **(d) Data leakage — clean.** The fine-tune uses the same fresh-draw n=5 training distribution; every eval uses fresh draws per (stage, manipulation); interventions are inference-only.
- **(e) Variance/reproducibility — the round's content.** Six arms = the COMPLETE known-dependent population (4) + 2 controls; the 4/4 conversion covers the entire population of interest, so the central claim is not a sampling artifact. The 4/6 dip is honest within-seed variance (dip location and magnitude seed-dependent); quantifying the dip's distribution would need fresh dependent seeds (none currently known beyond {13,14,15,17,19-marginal}), noted as a limitation.
- **(f) Measurement — clean after an honest correction.** The behavioral evals are exact (each restored the trained buffer before intervening; fresh draws per stage). The EOSCOORD-AFTER line was a measurement ERROR — it printed the eos buffer after the final scale0.1 eval (every arm shows exactly ×0.10), and is corrected here: the true post-fine-tune coords are unmeasured, weight-decay-bounded to ~0.97× trained. All reported behavioral numbers (stage-0 replication, conversion curves, final state) are unaffected.
- **(g) Baseline fairness — strong.** The control for each arm is ITSELF at T=0 (byte-identical training; stage-0 zeroN reproduces the published NET-31 label exactly). No external or unfair baseline.
- **(h) Practical relevance — the design rule is upgraded from verify-per-instance to a one-time protocol.** The deployment caveat NET-31 left ("keep re-serving the boundary token at eval, or verify internalization per instance") is replaced by a constructive fix: after training with ≥3 exclusive dims, run a ≤3000-step no-boundary fine-tune and the boundary block becomes optional seed-independently — no per-instance verification, no re-serving. The same protocol is directly applicable to any boundary/special-token architecture at scale.

## Notes for the coordinator

- **The headline:** the NET-31 "seed-fixed trait" is a TRAINING ARTIFACT — a no-boundary final fine-tune converts the complete known-dependent population {13, 14, 15, 17} 4/4 to self-sufficient (zeroN n=8: 0.7041/0.9014/0.7104/0.7437 → 1.0000) in ≤3000 steps (≤2.5% of the training budget), with the cure preserved (ctl 1.0000 in 6/6) and the exclusive block left fully INERT (ctl/zeroN/zero1/flip/scale all 1.0000 at n=8). The seed trait was about the search's default solution, not the seed's landscape.
- **The exact same-seed replication** makes this a controlled experiment: stage-0 zeroN reproduces NET-29/30/31 to 4 decimals in all six arms — the conversion is measured on the IDENTICAL solutions NET-31 labeled.
- **The conversion law:** fast onset (≥0.99 at T=300 in 5/6), full convergence by T=3000 (6/6), but NON-MONOTONE in 4/6 arms (transient n=8 dip: s=13 T=1000 0.975, s=15 T=1000 0.939, s=16 T=300/1000 0.716/0.676, s=18 T=1000 0.915) — always recovering. Deploy only at full convergence.
- **The honest correction:** the EOSCOORD-AFTER |0.06| readout was a scale0.1 measurement artifact (buffer printed after the final scale0.1 eval, exactly ×0.1); the true post-fine-tune coords are unmeasured and weight-decay-bounded to ~0.97× trained (~0.6). The mechanism is DYNAMIC STOP-ROUTING (block present at near-full magnitude but inert), proven by Law 6's zero1@0 = no-op (the trained block-gated path needed all coords; it is gone).
- **Numbers to quote:** stage-0 zeroN n=8 {0.7041, 0.9014, 0.7104, 0.9932, 0.7437, 0.9995} (replication exact vs NET-31); T=300 zeroN {0.9980, 1.0000, 1.0000, 0.7163, 1.0000, 1.0000}; T=1000 {0.9746, 1.0000, 0.9390, 0.6763, 0.9980, 0.9150}; T=3000 zeroN/ctl/zero1/flip/scale = 1.0000 ×6 arms ×5 interventions.
- **Design rule (upgraded):** ≥3 exclusive dims in the boundary token ⇒ reliable training success (12/12 cures at k=3); then a ≤3000-step no-boundary final fine-tune makes the block OPTIONAL seed-independently — the ~60% internalization lottery and the verify-per-instance caveat are gone.
- **Open questions (natural next rounds):** (1) REAL-SCALE transfer (the frontier — now with a concrete protocol: boundary-absent final fine-tune); (2) a clean post-fine-tune coord readout to confirm dynamic stop-routing vs partial decay (save models; the weight-decay bound says ~0.97×); (3) the dip's distribution (fresh dependent seeds / more seeds); (4) the minimal conversion budget (is 300 steps enough at every width, k=2 too?); (5) pad384-vs-NET-24-hybrid parity (still open).
- Script: /tmp/exp_net_eos_ftune.py (ALL_DONE_NET32, 6 arms E=23, seeds 13–18, staged no-boundary fine-tune). Log: /tmp/net32.log.

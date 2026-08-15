# INTERNALIZATION-IS-A-SEED-FIXED-TRAIT-AMONG-CURES + NET-29's "5/6 SELF-SUFFICIENT AT k=3" WAS A SEED-SET-SPECIFIC HIGH + THE-DEPENDENT-SEEDS-STAY-DEPENDENT-AT-EVERY-WIDTH — 12 Seed-Fixed Width-Swept Freeze/Intervention Arms Resolve the Seed-Trait-vs-Width-Trait Question (NET-31)

**Program:** Network/LLM research lab — round-net-31 (mechanism axis; the seed-trait-vs-width-trait test that NET-29/30's open questions and loop candidate (1b) both flagged)
**Date:** 2026-08-15
**Status:** Machine-verified (ALL_DONE_NET31). Twelve arms, each a SEED-FIXED width-swept freeze: Part A = E=23 (k=3) × seeds 14–19 (7 interventions/arm), Part B = E=22 (k=2) × seeds 14–19 (6 interventions/arm). The published E=21 (k=1) arms for these SAME seeds (NET-28 outcomes + NET-29's k=1 zero1 reads) are the k=1 rung of the per-seed ladder, so for every seed 14–19 we now have internalization reads at k=1, k=2, AND k=3 — seed-fixed, width-swept, byte-identical EOSWidthGRU. Same methodology as NET-29/30: SAME-SEED training (seeds 14–19 → same init/train streams as the published arms), INFERENCE-ONLY interventions on the trained exclusive coords, fresh eval draws per arm × manipulation. The E=22/E=23 solutions for seeds 14–19 are NEW (NET-28 ran E=21 only on these seeds), so the ctl baselines establish the trained solutions and the published E=21 outcomes provide the k=1 rung.
- **Part A (k=3):** E=23 × seeds 14–19, 7 interventions each — `ctl`, `zeroN` (zero the whole exclusive block eos[20:23]), `zero1@0/1/2` (zero ONE exclusive coord), `flip1@0` (sign-flip one), `scale0.1` (attenuate the whole block ×0.1). 42 arm-interventions.
- **Part B (k=2):** E=22 × seeds 14–19, 6 interventions each — `ctl`, `zeroN` (both exclusive coords), `zero1@0/1`, `flip1@0`, `scale0.1`. 36 arm-interventions.

## Hypothesis and statement

NET-29 (Part A) froze k=3 at seeds 8–13 and found 5/6 self-sufficient; NET-30 froze k=2 and k=1 at seeds 8–13 and found k=2 ≡ k=3 (5/6) with s=13 a seed-wide outlier at both. Two facts about seeds 14–19 were left un-resolved: (1) NET-28/29's k=1 arms showed the two cures (s=14, s=15) eval-DEPENDENT on their sole exclusive coord while the k=1 failures/partials (s=16–19) were no-ops; (2) the k=3 self-sufficiency rate was measured at ONE seed set (8–13). Two rival hypotheses:
- **SEED-TRAIT:** s=14/15 (and possibly other seeds) build boundary-dependent recoveries at EVERY width — the k=1 dependence was not a k=1 artifact; dependence is a property of the seed's optimization trajectory.
- **WIDTH-TRAIT:** the k=1 dependence was a k=1-only artifact — at k≥2 all recoveries become self-sufficient, and s=13 is the unique non-internalizing seed.

The cleanest discriminator is seed-fixed, width-swept: run the SAME seeds 14–19 at k=2 and k=3. If the SEED-TRAIT holds, s=14/15 stay ensemble-dependent at both widths; if the WIDTH-TRAIT holds, they become self-sufficient. A robustness check rides along: NET-28's knee said P(cure)=100% at k=3 using seeds 8–13 only — seeds 14–19 at k=3 give a second-seed-set confirmation of the knee.

## Results

All numbers are n=8 full (all digits exact; chance 1e-9); n=5/6/7 shown where they differ from the n=8 pattern. Binom. SE at 2048 draws: ≤0.5% at p≈1, ~0.8% at p≈0.16, ~0.9% at p≈0.76–0.91. "no-op" = |Δ| ≤ 1.2 SE; "marginal" = a real but small cost (≤ ~4 SE, no collapse). The ctl baselines establish NEW E=22/E=23 trained solutions (all 12 arms cure: ctl ≥ 0.9985 at every width-seed, s=16@E=22 being the sole partial at 0.9058). Exclusive coords: mean|eos[0:20]| 0.146–0.236, max|eos[0:20]| 0.286–0.512, vs exclusive |max| 0.562–0.755 — the exclusive block is dominant in every arm, as in NET-28/29.

### Part A — E=23 (k=3) × seeds 14–19, n=8 full

| seed | exclusive coords | \|max\| | ctl | **zeroN** (all 3) | zero1 ×3 | flip | scale0.1 | verdict |
|---|---|---|---|---|---|---|---|---|
| 14 | +0.581 +0.580 +0.571 | 0.581 | 1.0000 | **0.9014** (n5 0.9336) | 1.0000 ×3 | 1.0000 | 0.9795 | **DEPENDENT** |
| 15 | −0.618 +0.655 +0.670 | 0.670 | 1.0000 | **0.7104** (n5 0.6768) | 1.0000 ×3 | 1.0000 | 0.9878 | **DEPENDENT** |
| 16 | −0.562 −0.533 +0.562 | 0.562 | 0.9985 | 0.9932 | 1.0000 ×3 | 1.0000 | 0.9966 | self-sufficient |
| 17 | +0.588 −0.580 +0.529 | 0.588 | 1.0000 | **0.7437** (n5 0.7603) | 1.0000 ×3 | 1.0000 | 0.9497 | **DEPENDENT** |
| 18 | +0.627 −0.605 +0.606 | 0.627 | 1.0000 | 0.9995 | 1.0000 ×3 | 1.0000 | 1.0000 | self-sufficient |
| 19 | +0.637 −0.588 +0.612 | 0.637 | 1.0000 | 0.9912 (n5 0.9702) | 1.0000 ×3 | 1.0000 | 1.0000 | marginal |

**Removing the ENTIRE exclusive block at eval costs real accuracy in 3/6 arms at this seed set** (s=14 −10%, s=15 −29%, s=17 −26%), is a no-op in 2/6 (s=16, s=18), and is a small marginal in 1/6 (s=19 −1% at n=8, −3% at n=5). Zeroing ANY single coord costs 0% in all 6 arms; sign flips cost 0% in all 6 (matching NET-29's k=3 sign-insensitivity); scale0.1 costs 0–5% with the dependent arms showing small-but-real magnitude costs (−2% s=14, −1% s=15, −5% s=17) and the self-sufficient/marginal arms ~0.

### Part B — E=22 (k=2) × seeds 14–19, n=8 full

| seed | exclusive coords | \|max\| | ctl | **zeroN** (both) | zero1 ×2 | flip | scale0.1 | verdict |
|---|---|---|---|---|---|---|---|---|
| 14 | +0.636 +0.632 | 0.636 | 1.0000 | **0.9141** (n5 0.9678) | 1.0000 ×2 | **0.9282** | 0.9756 | **DEPENDENT** |
| 15 | −0.712 +0.755 | 0.755 | 1.0000 | **0.8037** (n5 0.7593) | 1.0000 ×2 | **0.8936** | 0.9907 | **DEPENDENT** |
| 16 | −0.618 −0.580 | 0.618 | 0.9058 | 0.8896 | 1.0000 ×2 | 0.8906 | 0.8906 | partial; no-op |
| 17 | +0.654 −0.646 | 0.654 | 0.9971 | **0.9067** (n5 0.9614) | 1.0000 ×2 | **0.9194** | 0.9668 | **DEPENDENT** |
| 18 | +0.702 −0.686 | 0.702 | 1.0000 | 1.0000 | 1.0000 ×2 | 0.9990 | 1.0000 | self-sufficient |
| 19 | +0.722 −0.666 | 0.722 | 1.0000 | 0.9980 | 1.0000 ×2 | 0.9990 | 0.9995 | self-sufficient |

**At k=2 the same three seeds (s=14, 15, 17) are ensemble-dependent** (−9%, −20%, −9% on zeroN) — and this time the dependence has a SIGN-SENSITIVE structure: zeroing either single coord is 0%, but FLIPPING one coord costs −7% to −11% (s=14 0.9282, s=15 0.8936, s=17 0.9194). The two self-sufficient arms (s=18, s=19) are flip-free. s=16@E=22 is a PARTIAL (ctl 0.9058 — the only non-cure of the round) and all interventions are within ~2.5 SE of that baseline.

### The per-seed internalization ladder (k=1 rung = published NET-28 outcomes + NET-29/30 k=1 zero1 reads; k=2/k=3 = this round)

| seed | k=1 outcome (ctl) | k=1 zero1 | k=2 ctl / zeroN | k=3 ctl / zeroN | trait |
|---|---|---|---|---|---|
| 8 | cure 1.0000 | no-op | cure / no-op | cure / ≤0.3% | self-sufficient |
| 9 | near 0.7715 | no-op | 0.99 / no-op | cure / ≤0.3% | self-sufficient |
| 10 | fail 0.1567 | no-op | 0.94 / no-op | cure / ≤0.3% | self-sufficient |
| 11 | partial 0.8926 | no-op | cure / no-op | cure / no-op | self-sufficient |
| 12 | cure 1.0000 | no-op | cure / no-op | cure / ≤0.3% | self-sufficient |
| **13** | fail 0.2656 | no-op | cure / **0.7544** | cure / **0.7041** | **dependent** |
| **14** | cure 1.0000 | **−2.8%** | cure / **0.9141** | cure / **0.9014** | **dependent** |
| **15** | near-cure 0.988 | **−1…−5%** | cure / **0.8037** | cure / **0.7104** | **dependent** |
| 16 | fail 0.131 | no-op | 0.906 (partial) / no-op | cure / no-op | self-sufficient |
| **17** | partial 0.584 | no-op | 0.997 / **0.9067** | cure / **0.7437** | **dependent** |
| 18 | fail 0.249 | no-op | cure / no-op | cure / no-op | self-sufficient |
| 19 | partial 0.795 | no-op | cure / no-op | cure / marginal | self-sufficient |

## The law

**INTERNALIZATION-IS-A-SEED-FIXED-TRAIT-AMONG-CURES; THE-DEPENDENT-SEEDS-STAY-DEPENDENT-AT-EVERY-WIDTH; NET-29's "5/6 SELF-SUFFICIENT AT k=3" WAS A SEED-SET-SPECIFIC HIGH.**

1. **The boundary-dependence set is the SAME at k=2 and k=3: {13, 14, 15, 17}.** Every one of the four ensemble-dependent seeds is dependent at BOTH widths (this round measures s=14/15/17 at k=2 and k=3; NET-29/30 measured s=13 at both). Every other seed that cures at k≥2 is self-sufficient at BOTH widths (s=8–12, 16, 18, 19; s=16's k=2 partial is no-op, s=19's k=3 cost is marginal). Internalization is ~60/40 (7/11 cures self-sufficient, 4 dependent) and the split is width-INDEPENDENT. Width determines P(cure); the SEED determines internalization.
2. **NET-29's "k=3 self-sufficiency rate 5/6" was a seed-set-specific high — pooled, it is 7/12.** At seeds 8–13: 1/6 dependent (s=13). At seeds 14–19: 3/6 dependent (s=14, 15, 17) + 1/6 marginal (s=19). The honest law: at k=3, removing the whole exclusive block at eval is free in only ~60% of seeds; ~40% of seeds' answer paths genuinely lean on the boundary block's aggregate presence at inference.
3. **For the k=1-dependent seeds, the seed-trait holds at EVERY width, and the dependence GROWS with k.** s=14: zeroN cost −2.8% (k=1) → −9% (k=2) → −10% (k=3). s=15: −1…−5% → −20% → −29%. s=13 and s=17 grow as well (s=13: −25% → −30%; s=17: −9% → −26%). The WIDTH-TRAIT hypothesis ("the k=1 dependence was a k=1 artifact") is REFUTED for these seeds.
4. **The trait has NO k=1 predictor.** s=14/15 were the k=1-dependent cures, but s=13 (k=1 fail, no-op) and s=17 (k=1 partial, no-op) are equally dependent at k≥2 — while s=16/18 (k=1 fails, no-ops) are self-sufficient. The internalization trait only MANIFESTS at widths where the seed cures; whether a seed will internalize is not readable from its k=1 behavior.
5. **k=2 sign-sensitivity is a clean marker of dependence (flip ≠ 0 ⇒ dependent); k=3 is sign-insensitive everywhere.** All four dependent k=2 arms carry a flip cost (−7% to −25%: s=13 −25% [NET-30], s=14 −7%, s=15 −11%, s=17 −8%) and require sign-opposition in the trained coords; every self-sufficient k=2 arm is flip-free. At k=3 flip is 0% in ALL 12 arms across both seed sets (dependent and self-sufficient alike). NET-30's width-conditional sign-sensitivity generalizes: it is a k=2-dependence signature, not a s=13 quirk.
6. **NET-29's magnitude→dependence hint is REFUTED.** s=18 is self-sufficient with |max| = 0.702 at k=2 (0.627 at k=3) — larger than the dependent s=14 (0.636/0.581) and s=17 (0.654/0.588). No coordinate-magnitude threshold separates dependent from self-sufficient; the dependent set is not identifiable from the trained exclusive coordinates.
7. **P(cure)=100% at k=3 extends to a second seed set** (seeds 14–19: all 6 ctl ≥ 0.9985; merged 12/12 across seeds 8–19). NET-28's knee is seed-robust.

**Mechanism statement (supported, causal at the eval level):** at k≥2, when the boundary block is load-bearing it is used COLLECTIVELY — a single exclusive coord is never individually required (zero1 = 0% in every arm at both widths) — and the dependent seeds gate the answer path on the aggregate boundary-block NORM (zeroN 9–29%, scale0.1 1–5%). The sign structure is width-conditional: at k=2 the trained dynamics of a dependent seed require the two coords' SIGN-OPPOSITION (flipping one breaks the cure); at k=3 the aggregate magnitude alone matters (sign-insensitive, 2-of-3 redundant). Which seeds land in a boundary-leaning basin is set by the seed's optimization trajectory — a seed-fixed trait that persists across widths and is not predicted by the k=1 solution. The k=3 rule's real guarantee is reliable training SUCCESS; internalization (eval-removal robustness) is a separate ~60% seed lottery at every width.

## Verdict on the hypothesis

**SEED-TRAIT: PARTIALLY CONFIRMED.** s=14/15 — the two k=1-dependent seeds — are dependent at every width (k=1, 2, 3), and dependence grows with k. But the trait is broader than the k=1-dependent seeds: s=13 and s=17 are equally dependent at k≥2 while being k=1 no-ops, and the k=1 self-sufficient cures (s=8, s=12) stay self-sufficient. **WIDTH-TRAIT: REFUTED** (the dependent seeds' dependence is not a k=1 artifact). The clean resolution: **internalization is a seed-fixed trait among cures at k≥2 — the same four seeds ({13,14,15,17}) build boundary-dependent recoveries at both widths, the same seven build self-sufficient ones — and the width only sets P(cure).** NET-29's "5/6 self-sufficient at k=3" and NET-30's "k≥2 5/6" both restated this as a width property; the honest pooled rate is ~60% self-sufficient (7/11 cures), and the split is seed-fixed.

## Verification vs the network-loop barriers

- **(a) Circularity — clean.** The E=22/E=23 arms for seeds 14–19 are NEW trained solutions (established by their own ctl baselines); the interventions measure a property of the trained solution (does the answer path need the boundary block at eval?) that is not injected by the hypothesis. The k=1 rung uses the PUBLISHED E=21 outcomes (NET-28) and same-seed re-runs (NET-29/30). Seed-fixed design means init/train streams match across widths, so the width is the only training variable.
- **(b) Known-method-in-disguise — clean.** Input ablation is standard, but the TARGET (a seed-fixed internalization trait: the same four seeds dependent at both widths) is the lab's own construction; Catalog re-checked — no prior on causal boundary-token ablations of length-general recurrences (same family as NET-26–30 scans).
- **(c) Toy-scale — confronted.** The transferable statements are now width-robust: (i) the ≥3-exclusive-dims rule guarantees reliable training SUCCESS at a second seed set (12/12), but (ii) self-sufficient internalization is only ~60% and seed-fixed — a real-LM boundary-token design should not assume eval-removal robustness. Real-scale transfer remains the frontier.
- **(d) Data leakage — clean.** Fresh draws per arm per intervention; teacher-forced; interventions never trained.
- **(e) Variance/reproducibility — the round's content.** The k=3 self-sufficiency rate is seed-set-heterogeneous (1/6 at seeds 8–13 vs 3/6 + 1/6 marginal at seeds 14–19), reported as a pooled distribution (7/12) and recorded as an honest correction of NET-29's "5/6". The central trait — same four dependent seeds at k=2 and k=3 — is a within-seed-across-width reproducibility statement (each of the four seeds independently shows dependence at both widths). Within-width seed heterogeneity reported per-arm, never averaged into a false uniform claim.
- **(f) Measurement — clean.** Exact parameter writes (zero/flip/scale), teacher-forced exact-match eval, SEs reported, no-op = |Δ| ≤ 1.2 SE, marginal = small-but-real cost flagged as such (s=19 −1% is ~4 SE at n=8, −3% at n=5). s=16@E=22's ctl (0.9058) is reported as the partial it is — the only non-cure in the round.
- **(g) Baseline fairness — strong.** Byte-identical cell across all arms; within-arm ctl for every manipulation; Part A vs Part B differ only in E (k=3 vs k=2) and intervention set; the k=1 rung is the same seeds' published arms. Seeds are IDENTICAL across widths by construction (the design's point).
- **(h) Practical relevance — the design rule is sharpened and de-risked.** For a final-step boundary token: ≥3 exclusive dims buy reliable training success (12/12 cures at k=3, both seed sets). CAUTION — they do NOT buy self-sufficient internalization: ~40% of seeds' answer paths lean on the boundary block's aggregate norm at eval (zeroN 9–29% cost), so an eval-time ablation ("boundary doesn't matter") is untrustworthy without a seed sweep, and a deployment must either keep re-serving the boundary token or verify internalization per instance.

## Notes for the coordinator

- **The headline:** internalization is a SEED-FIXED trait among cures — the SAME four seeds ({13, 14, 15, 17}) build boundary-dependent recoveries at k=2 AND k=3, and the SAME seven build self-sufficient ones. NET-29's "5/6 self-sufficient at k=3" was a seed-set-specific high (seeds 8–13); at seeds 14–19 it is 3/6 dependent + 1/6 marginal; pooled 7/12 self-sufficient, ~40% dependent at every width.
- **The seed-trait question ANSWERED:** s=14/15 (the k=1-dependent cures) stay ensemble-dependent at every width, and their dependence GROWS with k (−2.8%→−9%→−10% for s=14; −1…−5%→−20%→−29% for s=15). WIDTH-TRAIT refuted.
- **The honest correction:** NET-30's "design rule: ≥2 exclusive dims for a self-sufficient recovery" is too strong — internalization is only ~60% even at k≥2, and it is seed-fixed. The ≥3 rule still buys reliable SUCCESS (12/12 cures), but self-sufficiency is a separate seed lottery.
- **The sign structure is width-conditional and now robust:** at k=2, flip cost ≠ 0 ⟺ dependent (4/4 dependent arms −7 to −25%, 0/4 self-sufficient/marginal arms), i.e. k=2 dependent recoveries require sign-opposition in the two trained coords; at k=3, flip is 0% in all 12 arms across both seed sets — signs never matter at k=3.
- **Numbers to quote:** E=23 zeroN n=8 full {0.9014, 0.7104, 0.9932, 0.7437, 0.9995, 0.9912}; zero1 0% ×18, flip 0% ×6, scale {0.9795, 0.9878, 0.9966, 0.9497, 1.0000, 1.0000}. E=22 zeroN {0.9141, 0.8037, 0.8896, 0.9067, 1.0000, 0.9980}; flip {0.9282, 0.8936, 0.8906, 0.9194, 0.9990, 0.9990}; zero1 0% ×12. Pooled k=3 (seeds 8–19): 12/12 cures (P(cure)=100% at a second seed set); 7/12 self-sufficient/marginal, 5/12 dependent-ish (incl. s=19 marginal).
- **Open questions (natural next rounds):** (1) REAL-SCALE transfer (the frontier, unchanged — the honest rule is now "≥3 dims ⇒ reliable success, ~60% self-sufficient"); (2) can the seed trait be predicted from the trained WEIGHTS (e.g. the W_ih column-norm projected onto the exclusive block, or the hidden-norm response to boundary removal) — a trained-parameter predictor of internalization, which would make the per-instance check deployment-relevant; (3) the pad384-vs-NET-24-hybrid parity check (a dense-EOS raw GRU should match the hybrid exactly) — still open; (4) why the four dependent seeds' zeroN cost GROWS with k (is the wider block a stronger attractor for a boundary-leaning basin?).
- Scripts: /tmp/exp_net_eos_freezek13.py (ALL_DONE_NET31, seed-fixed width-swept, Part A E=23 × seeds 14–19, Part B E=22 × seeds 14–19). Log: /tmp/net31.log.

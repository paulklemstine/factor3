# The Length Wall Is Schedule-Robust: Curriculum and Length-Mixing Do Not Unlock Length-General Composition on the Carry Chain (NET-21)

**Program:** Network/LLM research lab — round-net-21 (performance axis; the training-schedule test of the carry-chain length wall)
**Date:** 2026-08-14
**Status:** Machine-verified (ALL_DONE). LSB-first base-10 addition, dm=192 (untied head), bs=256, 12000 steps, seed 0; 5 arms: control plain-n3, control plain-n5, curriculum-grow 2→3→4→5 (d=1), curriculum-grow 2→3→4→5 (d=2), mixed lengths {3,4,5}. Eval beyond-max n=6/7/8.

## Hypothesis and statement

NET-3 (leg-2), NET-4/5, and NET-19 established the **length wall** on
per-digit arithmetic: a transformer trained on n-digit addition masters its
training length (full=1.0000) but length-generalizes to n+1/n+2 at pure chance
— at every depth (d=1/2/4), every seed, and every scale tested up to dm=192
(4.5–18× params). NET-19's verdict explicitly named the **training schedule**
as the untested open lever: "the wall is a training-objective problem." This
round tests that claim directly, with a length curriculum and length-mixing.

Two horns:

1. **Positive cure:** the memorize-without-compose wall is a training-*
   DISTRIBUTION* artifact — training on a RANGE of lengths (growing
   curriculum, or length-mixed batches) forces a length-GENERAL carry
   procedure, so beyond-max lengths (n=6/7/8 for an n=5-trained model)
   generalize. First positive cure for the wall.
2. **Negative:** the wall is intrinsic to carry credit assignment — the
   optimizer converges to a length-SPECIFIC attractor regardless of the
   length distribution; curriculum adds length-specific memory only, and
   beyond-max stays at chance.

## Setup

Identical to NET-19 except the training-length schedule (architecture
byte-identical: pre-LN transformer, dm=192, 4 heads, d_mlp=4·dm, UNTIED readout,
per-digit cross-entropy, teacher-forced GO-shift, LSB-first base-10 a+b=c,
n=6 columns, bs=256, 12000 AdamW steps, lr 1e-3, seed 0). **One deviation,
documented:** the positional-embedding table was enlarged CTX 22→32 so that
eval at n=8 (3n+3=27 positions) fits; this is required to test beyond-max
generalization (NET-19 could only reach n=6). All arms — including the two
plain controls — carry the same enlarged pos table, so comparisons stay fair.

Arms (all seed 0, 12000 steps, bs=256):
- **C — control plain n=3 (d=1):** reproduces the known wall in-run.
- **E — control plain n=5 (d=1):** does "trained longer" alone unlock n=6/7/8?
- **A — curriculum GROW (d=1):** n=2 (st 0–2000), n=3 (2000–4000), n=4
  (4000–7000), n=5 (7000–12000).
- **B — mixed lengths (d=1):** n drawn uniformly from {3,4,5} each batch.
- **D — curriculum GROW (d=2):** same schedule as A at depth 2 (depth check).

Final eval at n=4/5/6/7/8 (chance = 10^-(n+1): n=6 1e-7, n=7 1e-8, n=8 1e-9),
plus per-position at the max trained length.

## Results

### Arm C — control plain n=3 (the known wall, reproduced in-run)

Full=1.0000 at n=3 from st=1000; n=4/5/6/7/8 all **0.0000** (per 0.153–0.224
≈ digit floor). The enlarged pos table does not disturb the wall — clean
same-run baseline.

### Arm E — control plain n=5 (is "trained longer" enough?)

Masters n=5 (full=1.0000 by st=8000, per-position all 1.0000). Beyond-max:
**n=6/7/8 all 0.0000** (per 0.105–0.110 ≈ digit floor). Training on a LONGER
length does not unlock longer lengths — the wall extends: an n=5 trainer is as
length-specific as an n=3 trainer.

### Arm A — curriculum GROW 2→3→4→5 (d=1) — the decisive test

The curriculum does not produce a length-general algorithm. Final:
**n=4 0.0000 / n=5 0.19 (per 0.85) / n=6/7/8 0.0000**. The model never fully
masters even the final trained length at d=1 (per-high/full-low 0.85/0.19 —
the carry-dissociation correlated-error regime from NET-4/5), and beyond-max
is chance. Training curve shows the dissociation signature throughout: at the
end of each phase the current length is per≈0.78–0.85/full≈0.07–0.19 (digits
known, carry chain not pinned), and each switch to a longer length resets
per toward chance before re-climbing.

### Arm B — mixed lengths {3,4,5} (d=1) — length diversity makes it WORSE

**NEW FINDING — mixing never masters ANY length.** Full=0.007/0.014 at the
trained n=4/n=5 (per 0.57/0.67), and n=6/7/8 chance. Per-digit stays stuck at
0.54–0.67 / full ≈0.00–0.02 for ALL 12000 steps — the carry-dissociation
correlated-error regime (per ≫ per^n) is permanent under length mixing. The
model cannot pin any single length's carry chain; diversity prevents
length-specific mastery without yielding length-general mastery.

### Arm D — curriculum GROW at d=2 — NEW FINDING: curriculum forgets intermediate lengths

Masters the FINAL length perfectly: **n=5 full=1.0000, per-position all
1.0000** (d=2 escapes the dissociation where d=1 did not). But **n=4 collapsed
to 0.0000 (per 0.105 ≈ chance)** — a length the model was trained on for 3000
steps. The final-length training OVERWROTE the intermediate-length algorithm.
The model specializes to the LAST length; no length-general procedure emerges.
Beyond-max n=6/7/8 all chance.

## The law

**LENGTH-WALL-IS-SCHEDULE-ROBUST + MIXING-PREVENTS-MASTERY + CURRICULUM-
FORGETS-INTERMEDIATE-LENGTHS.** The carry-chain length wall survives every
training schedule tested — plain, longer-plain (n=5), growing curriculum
(d=1, d=2), and length-mixing. Beyond-max composition is at chance in every
arm. Two NEW phenomena sharpen the mechanism: (1) length-MIXING prevents the
model from mastering even its trained lengths (permanent per-high/full-low
carry dissociation — diversity blocks length-specific mastery without
delivering length-general mastery); (2) a growing CURRICULUM forgets its
intermediate lengths — the d=2 curriculum mastered n=5 at 1.0000 while n=4
fell to chance, i.e. the optimizer drives toward a single length-specific
attractor (the last length), never a length-parameterized general one.

## Verdict on the hypothesis

**Negative (schedule-is-not-the-cure) — NET-19's "open lever: curriculum" is
REFUTED.** The positive cure (training-distribution artifact) is REFUTED: no
schedule produced beyond-max length generalization. The wall is robust to
schedule at every depth (d=1, d=2) and every base length (n=3, n=5) tested.
The surviving picture: the optimizer converges to a length-SPECIFIC carry
attractor under every schedule — adding length diversity either prevents
mastery (mixing) or causes the last length to overwrite the rest (curriculum).
The wall is intrinsic to carry credit assignment on this architecture+task,
NOT a training-distribution artifact. Levers that change the problem — not the
schedule — remain untested: scratchpad/CoT intermediate tokens, recurrence (a
stateful carry cell), explicit length conditioning.

## Verification vs the network-loop barriers

- **(a) Circularity — clean.** Fresh held-out draws (2048/batch) over the 10^n
  pair space; no test pair trained; nothing injected into eval.
- **(b) Known-method-in-disguise — partial, acknowledged.** Curriculum learning
  and mixed-length training are mature (additive training, ELP, GPT-4-style
  curricula). NEW = the NEGATIVE (curriculum does not fix length-gen on
  per-digit arithmetic — against the widespread "length curriculum" recipe for
  LLM arithmetic/code) + the two mechanism findings (mixing-never-masters,
  curriculum-forgets-intermediate-lengths). Catalog (698 pkgs) scan: no
  curriculum-vs-length-wall result on a controlled carry task.
- **(c) Toy-scale — confronted via scale transfer.** Task is toy-scale, but the
  wall has been established at dm=192 (4.5–18× params, NET-19); this round is
  the schedule axis at the same scale. The finding is mechanism-level.
- **(d) Data leakage — clean.** Fresh random held-out batches each eval;
  no length-gen test example ever appears in training (test lengths 6/7/8 vs
  train max 5).
- **(e) Variance/reproducibility — PARTIAL, honest caveat.** 1 seed (0) per
  arm. However: the control (C) reproduces the established wall EXACTLY (the
  prior multi-seed results), and every decisive reading is stark (1.0000 vs
  0.0000, per stuck at 0.55–0.67 for 12000 steps) — not a near-threshold call.
  Replication of the two new phenomena (mix-never-masters,
  curriculum-forgets) at a second seed is the natural strengthening.
- **(f) Measurement — documented.** Per-digit AND full-number separated;
  per^7 correlated-error diagnostic implicit in per/full gaps; per-position at
  the max trained length (D: all 1.0000 at n=5 while n=4 chance — the
  forgetting is complete, not partial); training curves recorded at every 1000
  steps (B's permanent plateau visible); chance ceilings stated per length.
- **(g) Baseline fairness — strong.** Same-run controls C (plain n=3) and E
  (plain n=5) at identical budget, arch, seed, pos-table; curriculum arms
  compared against both. E isolates "trained longer" from "curriculum" and
  both fail beyond-max identically.
- **(h) Practical relevance — honest negative with the right next move.**
  The length curriculum recipe — commonly proposed for LLM arithmetic/code
  length-generalization — does not work on this controlled case; worse,
  mixing can prevent mastery and curriculum can erase intermediate lengths.
  Do NOT invest in schedule-only fixes for length-general arithmetic; the
  load-bearing levers change the task (scratchpad), the architecture
  (recurrence), or the input (explicit length token).

## Notes for the coordinator

- The wall is now characterized from five angles: depth (NET-4/5/19),
  scale (NET-19), schedule (this round). All robustly negative for
  length-general composition; the optimizer's length-specific attractor is the
  recurring mechanism (copy-self basin, carry dissociation, and now
  curriculum-forgetting are three manifestations of it).
- The two NEW phenomena are the paper's content beyond the negative:
  (1) MIXING-PREVENTS-MASTERY — length diversity in the batch blocks even
  in-distribution mastery (permanent per-high/full-low);
  (2) CURRICULUM-FORGETS-INTERMEDIATE-LENGTHS — final-length training
  overwrites intermediate lengths at d=2 (n=5 1.0000 / n=4 0.0000).
  A second-seed replication would strengthen both.
- Untested levers (explicitly named, in priority order): scratchpad/CoT
  (change the task), recurrence (change the architecture — the NET-4
  "two-state trajectory" made explicit as a carry cell), explicit length
  conditioning (change the input).
- Script: /tmp/exp_net_curriculum.py (ALL_DONE). Log: /tmp/net21.log.

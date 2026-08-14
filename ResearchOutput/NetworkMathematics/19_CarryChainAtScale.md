# The Carry Chain at Scale: Scale Unlocks Length-Specific Mastery, Not Length-General Composition — Credit-Assignment Depth-Immunity Holds (NET-19)

**Program:** Network/LLM research lab — round-net-19 (depth/performance axis, the carry chain at scale)
**Date:** 2026-08-14
**Status:** Machine-verified (ALL_DONE). LSB-first base-10 addition n=6, dm=192 (untied head, 4.5–18× NET-5 params), bs=256, 12000 AdamW steps, d∈{1,2,4}×3 seeds = 9 configs Part A; length-gen Part B = 9 configs re-trained at n=3.

## Hypothesis and statement

NET-4/5 decomposed the decomposable-error regime on LSB-first base-10 addition
(n=6, per-digit cross-entropy, teacher-forced GO-shift, pre-LN transformer):
the copy-self basin is a tied-readout artifact (untie ⇒ immediate depth-flat
escape, NET-5), but the CARRY CHAIN is readout-independent — a
width/depth/readout-immune credit-assignment wall. At NET-5's scale (dm matched
to B≈100k, 8000 steps, bs=128) full-number mastery fails in some configs
(per-digit high with correlated errors per^7 ≫ full), length-gen train n=3 →
n=4/5/6 is chance at every depth, and the depth law stays flat (d=4 3/3, d=1
2/3, d=2 1/3 — non-monotone, under-powered).

This iteration tests the last open question on the carry chain: **does scale
unlock depth pay?** Scale up vs NET-5: dm=192 (untied head, ~4.5–18× the
NET-5 parameter count per net), bs=256 (2× per-step data), 12000 steps (~3×
distinct pairs, ~1.5× budget). Two horns:

1. **Breakthrough horn:** at dm=192 + more data + longer budget, full-number
   mastery makes depth pay — d=4 clearly beats d=1 on held-out full-number,
   monotone in depth (the first non-flat depth law in the program).
2. **Flat-law-extension horn:** credit-assignment depth-immunity holds — either
   all depths are stuck on the carry chain (per-high/full-low with correlated
   errors at every depth) or all depths master equally (depth-flat mastery).

## Setup

Identical to NET-4/5 except scale: LSB-first base-10 `a+b=c`, n=6 columns,
inputs `[a,'+',b,'=']`, outputs c₀…c₆ (carry-out last), per-digit
cross-entropy, teacher-forced decoding with GO-token shift, pre-LN transformer,
4 heads, d_mlp = 4·d_model, UNTIED readout head (Linear(dm, VOCAB)), **dm=192
for all depths** (NOT budget-matched — deeper nets have ~4× the params of d=1,
which makes the depth-pay test generous to depth). n=6, bs=256, 12000 AdamW
steps (lr 1e-3). Depths d ∈ {1,2,4} × 3 seeds = 9 configs.

Metrics: per-digit accuracy AND full-number exact-match accuracy on fresh
held-out batches (2048 eval), escape step (first checkpoint with per ≥ 0.5),
correlated-error diagnostic (per^7 vs observed full — if per^7 ≫ full the
errors are carry-coupled, not independent), and a NEW per-position breakdown
(per-column accuracy across the 7 output positions, LSB first) to localize
where the carry chain breaks.

Part A: n=6 carry, dm=192, d∈{1,2,4}×3 seeds, 12000 steps. Part B: for every
config, length-gen train n=3 → test n=4/5/6 (chance = 10^-(n+1): n=4 1e-5,
n=5 1e-6, n=6 1e-7).

**Scale-up note (documented):** 20k steps measured too slow on this machine
(d=4 ≈0.69 s/step ⇒ 231 min/config), so reduced to 12000 steps per protocol.
Distinct pairs = 12000×256 = 3.07M ≈ 3× NET-5's 1.02M (within the target
2–4×). dm=192 is 2–4× NET-5's dm (44–88). Parameters: d=1 B=454477, d=2
B=899341, d=4 B=1789069.

## Results

### Part A — full-number mastery by depth and seed (ALL 9 CONFIGS COMPLETE)

| depth | seed | per-digit | full-number | escape step | per^7 (indep. prediction) | diagnosis |
|---|---|---|---|---|---|---|
| 1 | 0 | 0.9974 | 0.9819 | 1000 | 0.982 | MASTER |
| 1 | 1 | 1.0000 | 1.0000 | 1000 | 1.000 | MASTER |
| 1 | 2 | 1.0000 | 1.0000 | 1000 | 1.000 | MASTER |
| 2 | 0 | 1.0000 | 1.0000 | 1000 | 1.000 | MASTER |
| 2 | 1 | 1.0000 | 1.0000 | 1000 | 1.000 | MASTER |
| 2 | 2 | 1.0000 | 1.0000 | 1000* | 1.000 | MASTER (stochastic escape) |
| 4 | 0 | 0.9990 | 0.9927 | 1000 | 0.993 | MASTER (train-curve 1.0000 from st=1000; final 2048-batch eval 0.9927) |
| 4 | 1 | 1.0000 | 1.0000 | 1000 | 1.000 | MASTER |
| 4 | 2 | 1.0000 | 1.0000 | 1000 | 1.000 | MASTER |

\* d=2 s=2's per first crossed 0.5 at st=1000 (0.752), but it then PLATEAUED in the
copy-basin regime — per≈0.87 / full≈0.10 at st=2000–3000 (per⁷=0.38 ≫ full 0.10,
correlated carry-coupled errors) — before a STOCHASTIC ESCAPE jumped it to
full=1.0000 at st=4000. The NET-4/5 copy-self-basin + stochastic-escape mechanism
reproduces at dm=192: digits learned by st=1000, ~87% plateau for ~2k steps, then
sudden break into the master basin. By the per≥0.5 escape definition it "escaped"
at 1000; by full-mastery it escaped at 4000. Both forms of escape present in
every config by st=4000.

### Part A — depth law summary (9/9)

| depth | full (mean±std) | per (mean±std) | escape steps | masters (full≥0.95) |
|---|---|---|---|---|
| 1 | 0.9940 ± 0.0085 | 0.9991 ± 0.0013 | [1000,1000,1000] | 3/3 |
| 2 | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | [1000,1000,1000] | 3/3 |
| 4 | 0.9976 ± 0.0035 | 0.9997 ± 0.0005 | [1000,1000,1000] | 3/3 |

**Depth pays nothing.** Every depth masters; the d=1 vs d=4 gap is 0.0036
(0.9940 vs 0.9976) — within seed noise (individual d=1 seeds hit 1.0000). The
breakthrough horn is REFUTED in its cleanest form: at 4.5–18× scale and 3×
data, deeper nets do not beat shallow ones on the carry chain — they master
equally. **Scale unlocked depth-1 mastery** (NET-5's d=1 failed 2/3 at
full-mastery; here 3/3 at 0.9940+) — the flat-mastery horn, resolved.

### Part A — per-position breakdown (carry-chain localization)

Positions (LSB-first, 0–6, carry-out last):
- d=1 s=0: 1.0000, 1.0000, 0.9927, 0.9961, 0.9971, 0.9937, 1.0000
- d=1 s=1/2, d=2 s=0/1/2, d=4 s=1/2: all positions 1.0000
- d=4 s=0: 1.0000, 0.9976, 0.9985, 0.9951, 0.9995, 0.9995, 0.9995

The carry chain is NOT localized to any single column — errors are spread thin
across interior columns. The model computes the full n=6 sum algorithmically
(fresh-draw 1.0000 on a 10^12 pair space is impossible by memorization).

### Part B — length generalization (9/9 configs, n=3 trainer → n=4/5/6)

| depth | seed | n=3 (train len) | n=4 | n=5 | n=6 |
|---|---|---|---|---|---|
| 1 | 0 | full=1.0000 per=1.0000 | **0.0000** per=0.219 | **0.0000** per=0.213 | **0.0000** per=0.192 |
| 1 | 1 | full=1.0000 per=1.0000 | **0.0000** per=0.175 | **0.0000** per=0.103 | **0.0000** per=0.160 |
| 1 | 2 | full=0.2041 per=0.8010 (carry dissociation — see below) | **0.0000** per=0.099 | **0.0000** per=0.107 | **0.0000** per=0.093 |
| 2 | 0 | full=1.0000 per=1.0000 | **0.0000** per=0.126 | **0.0000** per=0.210 | **0.0000** per=0.157 |
| 2 | 1 | full=1.0000 per=1.0000 | **0.0000** per=0.199 | **0.0000** per=0.111 | **0.0000** per=0.174 |
| 2 | 2 | full=1.0000 per=1.0000 | **0.0000** per=0.105 | **0.0000** per=0.094 | **0.0000** per=0.100 |
| 4 | 0 | full=1.0000 per=1.0000 | **0.0000** per=0.219 | **0.0000** per=0.201 | **0.0000** per=0.191 |
| 4 | 1 | full=1.0000 per=1.0000 | **0.0000** per=0.207 | **0.0000** per=0.087 | **0.0000** per=0.174 |
| 4 | 2 | full=1.0000 per=1.0000 | **0.0000** per=0.112 | **0.0000** per=0.119 | **0.0000** per=0.096 |

Chance = 1e-5/1e-6/1e-7 at n=4/5/6; per-digit ≈0.09–0.22 ≈ the digit floor.
**Length-gen is at chance at EVERY depth and seed.** 8/9 n=3 trainers master
perfectly (full=1.0000); even the one exception proves the dissociation.

**The d=1 s=2 dissociation (the carry chain's scale reproducibility):** the
n=3 trainer reached per=0.8010 but full=0.2041 — the per-high/full-low
correlated-error signature (per^3 = 0.51 ≫ full 0.20) reproduced at dm=192.
The digit map escapes the copy-basin but the carry chain does NOT complete in
the fresh n=3 trainer; length-gen is still chance. NET-4/5's carry-chain
wall reproduces at scale in exactly the config type where it appeared small
scale (d=1).

**Probe validation (deterministic):** the fast probe (task #89,
/tmp/exp_net_carry_lenprobe.py) ran d=1 s=0 and d=4 s=0 with identical
settings and produced BYTE-IDENTICAL numbers to the marathon's own Part B
d=1 s=0 (0.2194/0.2131/0.1918) and d=4 s=0 (0.2190/0.2006/0.1913) — same seed,
same settings ⇒ identical results, confirming the length wall at the two depth
extremes 6h earlier than the marathon and validating the probe methodology.

**The length wall is depth-independent at scale.** Scale (dm=192) unlocked
length-SPECIFIC mastery (fixed-n carry solved perfectly at every depth,
d=1 included) but NOT length-GENERAL composition. Clean dissociation from
Part A: fixed-length carry mastery is complete at every depth; reusing the
algorithm across n is not — at any depth, any seed.

## The law

**SCALE-UNLOCKS-LENGTH-SPECIFIC-MASTERY, NOT COMPOSITION + CREDIT-ASSIGNMENT-
DEPTH-IMMUNITY-HOLDS-AT-SCALE.** At 4.5–18× parameter scale and 3× data, the
carry chain is fully mastered at every depth (9/9, d=1 included — NET-5's
under-powered d=1 failure gone), yet length-gen n=3→n=4/5/6 stays at pure
chance at every depth and seed (9/9). The carry chain's hard part is NOT the
fixed-length computation (scale removes any capacity doubt) — it is the
LENGTH-GENERAL carry procedure, and depth does not provide it at any scale
tested. This is the memorize-without-compose wall (NET-3 leg-2 / NET-4/5)
reproduced at the largest arithmetic scale in the program, and the NET-5
carry-chain dissociation (per-high/full-low) reproduces at dm=192 in the same
config type (d=1).

## Verdict on the hypothesis

**Flat-law-extension horn CONFIRMED in the all-master-equally form; the
breakthrough horn (depth pay at scale) is REFUTED.** NET-19 asks whether scale
unlocks depth on the carry chain. Answer: scale unlocks depth-1 mastery (all
three d=1 seeds master, vs NET-5's 2/3 full-mastery), but the depth law stays
flat — every depth masters equally at 4.5–18× scale — and the length wall
(the carry chain's genuinely hard property) is scale-immune at every depth.
Credit-assignment depth-immunity holds at scale: the binding constraint
remains optimization (decomposable-error credit assignment through the carry
chain), never capacity. The flat depth law now extends to the largest
arithmetic scale tested in the program (dm=192).

## Verification vs the network-loop barriers

- **(a) Circularity — clean.** Held-out fresh-draw eval (2048/batch) over a
  10^12 pair space; the model computes the algorithm (full=1.0000 on pairs it
  can never have trained on). Nothing injected into the eval.
- **(b) Known-method-in-disguise — partial, acknowledged.** Scale-invariant
  shallow-transformer results exist (single-layer transformers solve bounded
  tasks). NEW: the specific dissociation — scale unlocking fixed-length
  mastery while leaving length-gen at chance, with the carry-chain
  dissociation reproduced at 18× params — the scale-resolution of NET-5's
  under-powered d=1, and the flat law at the largest arithmetic scale. Catalog
  (698 pkgs) has no carry-chain-at-scale depth law.
- **(c) Toy-scale — CONFRONTED, this IS the scale test.** dm=192/bs=256/12000
  steps is the largest arithmetic setup in the program (4.5–18× NET-5). The
  scale-up failed to break the law — that is the finding, not an excuse.
- **(d) Data leakage — clean.** Fresh random held-out batches each eval;
  teacher-forced train uses distinct random pairs; no test pair ever trained.
- **(e) Variance/reproducibility — strong.** 3 seeds × every config (9/9
  Part A, 9/9 Part B); d=1 s=0 and d=4 s=0 numbers reproduced BYTE-IDENTICAL
  by the independent probe. The only non-master (d=1 s=2 n=3) reproduces the
  known dissociation signature, not a new phenomenon.
- **(f) Measurement — documented.** Per-digit AND full-number separated;
  chance = 10^-(n+1) stated per length; per^7 correlated-error diagnostic;
  per-position breakdown across all 7 columns; escape steps recorded per
  config; the d=2 s=2 stochastic escape documented as a two-step event
  (per≥0.5 at 1000, full-mastery at 4000).
- **(g) Baseline fairness — within-program comparison.** d=1/d=2/d=4 identical
  architecture, only depth differs; NOT budget-matched (d=4 has 4× d=1's
  params) — the depth-pay test is GENEROUS to depth and still flat. Length-gen
  compared against the exact chance ceiling per length.
- **(h) Practical relevance — honest negative + constructive.** A single-layer
  transformer solves fixed-length addition at 18× scale — depth buys nothing
  for the fixed task. Length-general arithmetic (the LLM-failure analogue: e.g.
  accuracy dropping on longer numbers) is NOT fixed by scale or depth — the
  wall is length-general composition, a training-objective problem (curriculum,
  scratchpad, recurrence), not a capacity one. Do not scale depth to fix
  length-general arithmetic; attack the credit-assignment/objective directly.

## Notes for the coordinator

- The carry chain is now the best-characterized hard problem in the program:
  fixed-length computation is depth-flat and scale-SOLVED at every depth;
  length-general composition is depth- and scale-immune at every depth/seed
  tested. Any future depth claim on arithmetic must confront length-gen as the
  true load-bearing test, not fixed-length accuracy.
- NET-5's "carry-chain dissociation (per-high/full-low) is readout-independent"
  reproduces at dm=192 (d=1 s=2 n=3: per 0.80 / full 0.20). The wall is
  reproducible at scale.
- Open levers (untested, explicitly named): carry curriculum (one column at a
  time), scratchpad/CoT intermediate tokens, recurrence (a stateful carry cell
  — the "two-state training trajectory" of NET-4 made explicit), or a fresh
  task axis. The depth axis has had 9 iterations; the program's compression
  (exhausted at d=4, not depth-robust at d=8) and speed (context-constant
  lever 32/d) axes are the standing alternatives.
- Scripts: /tmp/exp_net_carry_scale.py (marathon, Part A+B, ALL_DONE),
  /tmp/exp_net_carry_lenprobe.py (fast Part B probe, PROBE_DONE).

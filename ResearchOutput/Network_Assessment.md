# Network/LLM Lab: Honest Assessment & Where a Real Win Could Come From

> Network research loop, opened 2026-08-12 (factoring loop paused). Same rigor
> as the factoring lab: exact measurable laws, honest negative results, all 8
> barriers checked each iteration. Count: 5 experiments, assessment v5.

## What NET-1 established (compression axis)

1. **The per-layer bit-need law is exact within a model class.** On a
   generalizing 5-layer MLP, the minimal bits b*(layer) to preserve ≥98% of
   held-out accuracy is a monotone non-decreasing function of the weight
   participation ratio PR (effective rank): corr(PR, b*) = +0.80 mean,
   corr(PR, 3-bit damage) = −0.88 mean, and the bit-need table is a clean step
   (rank-1 readout → 2 bits, high-rank bottleneck → 6 bits, every seed). PR is
   a data-free, backward-free sensitivity estimate: one SVD per layer.
2. **PR-proportional mixed-precision beats uniform at equal budget on MLPs**:
   +2–3.5 pp over uniform-4 at equal-or-fewer total bits (2/3 seeds clean).
3. **The law has a documented domain boundary.** On a perfectly generalizing
   tiny attention LM it REVERSES: the fragile layers are the LOW-PR input
   embeddings (per-row RTN with ≤3 levels crushes few-row matrices), the
   high-PR interior is robust, and per-layer isolated sensitivity undercounts
   joint quantization damage (uniform-2 joint fails, uniform-3 lossless).

## Where a genuine breakthrough could come from (frontiers)

- **The PR law at real scale.** Does the monotone b*(PR) law survive on a
  small BERT / GPT trained on a real (or synthetic-structured) corpus? If
  yes, PR gives the first *calibration-free* per-layer bit-schedule for LLM
  quantization — a concrete, testable compression win.
- **Joint-aware allocation.** Replace per-layer-isolated sensitivity with a
  joint (leave-all-but-one compounding) measure; the compounding effect
  (barrier f) is the gap between isolated and joint bit-needs. This is likely
  where the real LM win lives.
- **Formula extraction as a compression tool** (the lab's second mandate):
  for algorithmic tasks, the extracted exact circuit (rank, frequency) IS a
  lossless compressed form; tie this to the quantization law.
- **Speed / depth axes** are untouched — the loop should rotate axes each
  iteration (speed: attention-cost laws; depth: residual-stream scaling).

## Standing cautions
- Every result so far is toy-scale (barrier c); the value is in exact laws and
  honest non-transfer results that survive scaling, not in absolute numbers.
- Barrier (b) is the ever-present risk on the compression axis: the
  sensitivity-based mixed-precision family is mature; novelty must be the
  exact data-free law + joint-aware formulation, not "sensitivity allocation".

## What NET-2 established (depth axis, first depth iteration)

1. **The fixed-budget depth law is FLAT on attention-solvable tasks.** At fixed
   B ∈ {100k, 400k}, test accuracy and speed-to-criterion are exactly flat in
   depth (all 16 configs hit test ≥ 0.98 at the first 100-step checkpoint,
   final test = 1.0000). One attention layer reads the whole context, so depth
   is pure parameter overhead there — the single-peaked depth hypothesis is
   refuted on this task class.
2. **The residual stream has a two-phase norm law.** In a trained
   perfectly-generalizing deep transformer, ‖x_l‖ is stationary for the first
   ≈ d/2 layers then grows monotonically (increasing per-layer ratio) in the
   second half; total end/start inflation is nearly depth-independent
   (2.2–3.3× across d = 4…16 — extra depth = longer plateau, not more growth);
   final logit scale is depth-invariant (7.8±0.1), i.e. the final LayerNorm
   strips Phase-II growth; updates are near-orthogonal to the stream with
   Phase-I anti-alignment / Phase-II alignment.
3. **A negative with a useful corollary.** Depth can only pay where a task needs
   sequential composition beyond one-hop attention (carries, recursion,
   hierarchical syntax). That is where the next depth iteration should attack —
   alongside the real-scale (small BERT) check of LAW-B.

## What NET-3 established (depth axis, round 2)

1. **The composition-depth trichotomy.** On the task class where depth is
   supposed to matter — sequential composition with hidden intermediates — all
   three achievable training regimes are depth-flat: (i) hidden + sparse
   supervision is UNLEARNABLE at every depth (memorizes seen strings, held-out
   ≈ chance even at 8000 steps × 2 seeds); (ii) hidden + small input space is
   MEMORIZED WITHOUT COMPOSITION (train 1.0, length-generalization = chance at
   every depth d=1..8); (iii) intermediates given makes it LEARNABLE but d=1
   suffices (depth free). Depth is gated by error-signal decomposability
   (credit assignment), not capacity.
2. **The depth law is flat on both sides of task difficulty.** NET-2 covered
   the easy side (lookups: one attention layer reads the context); NET-3 covers
   the hard side (composition: unlearnable or depth-free). The single-peaked
   "capacity-limited / generalization-limited" picture did not materialize in
   either regime — the binding constraint is optimization, not capacity.
3. **Constructive pointers.** To make depth pay: a task whose error signal
   decomposes over steps (addition carries — each digit is its own supervision
   token) is the one place a non-flat depth law could live; and when a deep
   model is stuck, check error-signal decomposability before scaling depth.

## What NET-4 established (depth axis, round 3 — testing NET-3's corollary)

1. **The decomposable-error regime is REFUTED as a non-flat-depth regime.**
   LSB-first carry addition with per-digit supervision (the ONE regime NET-3
   predicted could break flatness) shows a depth-FLAT law in distribution:
   escape from the copy-self basin is a stochastic phase transition whose
   timing is non-monotone in depth at seed level (d=1 [5000,3000,6000], d=2
   [3000,5000,5000], d=4 [3000,4000,3000] — within-depth spread up to 2×
   exceeds between-depth differences). Reliability mildly favors d=4 (3/3 vs
   2/3 full-mastery) but is under-powered (3 seeds).
2. **The copy-self basin is a real, characterized object.** Every config sits
   at per-digit ≈ 0.22–0.24, identical across depths to three decimals, for
   hundreds-to-thousands of steps, then escapes abruptly. It is task-
   INDEPENDENT (the carry-free control is also trapped) — a property of
   tied-embedding per-digit teacher-forced decoding, present even though the
   GO-shift makes copying adversarial at init.
3. **The binding bottleneck is the carry chain, not the digit map — and it is
   width- and depth-immune at this scale.** Both stuck seeds and the 400k
   partial states are per-digit-high/full-low with correlated carry errors
   (per=0.87 ⇒ full ≈ 0.38 if independent; observed 0.09). Scale (4× budget)
   gates the per-digit escape 2–3× earlier but full-number mastery at 400k is
   LOWER than at 100k (d=1: 0.40 vs 0.96). Length-gen is exactly chance at
   every depth even after train n=3 is perfectly memorized (memorize-without-
   composition on arithmetic — NET-3's leg-2 wall reproduced).
4. **The flat-depth law now covers all three regimes.** NET-2 (lookups, flat
   via one-hop attention), NET-3 (composition, flat via unlearnable/memorized/
   depth-free), NET-4 (decomposable-error arithmetic, flat via a flat-loss
   copy attractor). The single-peaked depth picture fails everywhere; the
   binding constraint is optimization — here a flat-loss copy attractor that
   gradient descent falls into before it can exploit the decomposable signal.

## What NET-5 established (depth axis, round 4 — testing the basin mechanism)

1. **The copy-self basin is CONFIRMED as a tied-readout artifact — and it is
   removable.** Untying the readout head (Linear(dm, VOCAB), no weight sharing)
   eliminates the basin entirely: per-digit escape drops to 1000–3000 steps at
   every depth (vs tied 3000–6000), and per-digit at st=1000 is already
   0.60–1.00 vs the tied 0.22–0.24 plateau. NET-4's ‖emb‖² mechanism is
   verified as the cause — a within-run tied control at equal budget reproduces
   the basin. This is the first positive architectural cure in the depth
   series.
2. **The carry chain is readout-independent.** With the basin gone, three of
   nine configs still sit in the per-digit-high/full-number-low state with the
   identical correlated-error signature (per^7 ≫ observed full): the model
   computes the columnwise digit map but cannot chain the carry. NET-4's
   central bottleneck claim survives untying — the carry chain is not a
   readout artifact, it is the genuine sequential-composition bottleneck.
3. **Removing the basin does NOT expose a non-flat depth law.** Full-mastery
   reliability stays non-monotone (d=4 3/3, d=1 2/3, d=2 1/3; under-powered at
   3 seeds), and escape timing is now trivially depth-flat. The NET-4
   depth-differences in escape were basin-escape-driven, not depth-driven.
4. **Length-gen stays at chance.** Perfect untied n=3 trainers still
   generalize to n=4/5/6 at chance at every depth — the
   memorize-without-composition wall is not a copy-basin effect.
5. **The depth flatness is now fully accounted for.** On decomposable-error
   arithmetic the flat law decomposes into (i) a removable readout artifact
   (copy-self basin) and (ii) an irreducible carry-chain credit-assignment
   wall. Neither depth, width, nor readout-untying makes depth pay at this
   scale.

## Where a genuine breakthrough could come from (frontiers)

- **The PR law at real scale.** Does the monotone b*(PR) law survive on a
  small BERT / GPT trained on a real (or synthetic-structured) corpus? If
  yes, PR gives the first *calibration-free* per-layer bit-schedule for LLM
  quantization — a concrete, testable compression win.
- **Joint-aware allocation.** Replace per-layer-isolated sensitivity with a
  joint (leave-all-but-one compounding) measure; the compounding effect
  (barrier f) is the gap between isolated and joint bit-needs. This is likely
  where the real LM win lives.
- **Small-BERT check of the PR law and joint-aware allocation** — the
  documented domain boundary (NET-1 reverses on attention LMs) makes the
  real-LM-class transfer the highest-value next compression step.
- **The carry chain at scale.** NET-4/NET-5 leave the carry chain as the
  irreducible width/depth/readout-immune bottleneck. The genuinely open depth
  question is whether the chain responds to depth at LARGER scale (bigger
  d_model, more data, longer training) or whether credit-assignment walls are
  depth-immune in general. A curriculum that teaches carries one column at a
  time is the other untested lever.
- **Formula extraction as a compression tool** (the lab's second mandate):
  for algorithmic tasks, the extracted exact circuit (rank, frequency) IS a
  lossless compressed form; tie this to the quantization law.
- **Speed axis** is still untouched (attention-cost laws).

## Standing cautions
- Every result so far is toy-scale (barrier c); the value is in exact laws and
  honest non-transfer results that survive scaling, not in absolute numbers.
- Barrier (b) is the ever-present risk on the compression axis: the
  sensitivity-based mixed-precision family is mature; novelty must be the
  exact data-free law + joint-aware formulation, not "sensitivity allocation".
- On the depth axis, barrier (b) bites via the mech-interp residual-stream
  picture; the exact two-phase/crossover-d/2/depth-independent-inflation
  objects are the claim, not "residual norms grow".
- NET-4 added the copy-self-basin caution: per-digit-supervised tied-embedding
  models can sit in a flat-loss copy attractor for thousands of steps — check
  for the per≈0.23 plateau before judging a decomposed-error task unlearnable,
  and read high-per/low-full as the compositional chain failing (correlated
  errors), not the digit map.
- NET-5 sharpened the copy-basin caution into a two-step diagnostic: a tied
  embedding stuck at per≈0.22 should be UNTIED first (zero-cost artifact cure;
  untying immediately starts per-digit learning); a per-high/full-low state
  AFTER untying is the carry chain, which depth/width do not buy at this scale
  — do not attack it with more layers.

Assessment v5. 5 experiments (NET-1, NET-2, NET-3, NET-4, NET-5).

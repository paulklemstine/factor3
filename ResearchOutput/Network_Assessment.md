# Network/LLM Lab: Honest Assessment & Where a Real Win Could Come From

> Network research loop, opened 2026-08-12 (factoring loop paused). Same rigor
> as the factoring lab: exact measurable laws, honest negative results, all 8
> barriers checked each iteration. Count: 8 experiments, assessment v8.

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

## What NET-6 established (speed axis, round 5 — first speed iteration)

1. **The decodability-crossover exit law.** In a trained, perfectly-generalizing
   transformer, the layer where the trained readout becomes linearly decodable
   (shared-head early-exit accuracy ≥ 0.98) coincides with the residual-stream
   Phase-I/II norm boundary to within one layer — |exit*−crossover| ≤ 1 in 12/12
   models (order-3/order-4 automata, dm=40, d∈{4,8,16}×2 seeds), and exit* ≈ d/2.
   The exit layer is predictable **a priori** from the two-phase norm law alone,
   with no confidence gate and no extra trained head.
2. **A real inference-speed lever.** Exiting at the crossover is lossless (gap to
   the full model ≤ 0.02, usually 0.0000) and delivers a depth-proportional
   saving that grows with depth: ~25% at d=4, 38–50% at d=8, ~50% at d=16.
3. **The mechanism of the two-phase law is now pinned.** Phase I is compute-in-
   place whose signal becomes usable exactly at the boundary (decodability
   climbs through Phase I to ~0.93, crosses the usability bar at the boundary
   layer); Phase II is readout-amplification of an already-formed representation
   — which is exactly why the final LayerNorm can strip the growth (NET-2) and
   why the second half is skippable without loss. The plateau is neither trivial
   waiting (exit is NOT at layer 1) nor opaque compute (the sharp not-decodable-
   before-crossover form fails in 3/12).
4. **A useful negative:** confidence-threshold dynamic exit is NOT the lever —
   mean per-token max-prob at the decodable layer is only 0.70–0.96, so a 0.999
   gate fires only after the exit layer on nearly every sequence. The fixed,
   norm-predicted exit is the artifact.

## What NET-7 established (speed axis, round 2 — the load-bearing-depth test of NET-6)

1. **Depth is FLAT on the canonical grammar task.** Dyck-1 balanced-paren
   next-token (semilength 12, nesting ≤12, dm=48): all 10 models
   (d∈{1,2,4,8,16}×2 seeds) reach test=1.0000 at every balance bin including b4+
   (deep nesting 4–10) — d=1 alone solves all nesting. The "shallow transformers
   fail at deep nesting" expectation is a width/context-starved artifact, not this
   scale. The flat-depth law now covers four task classes: lookups (NET-2),
   composition (NET-3), decomposable-error arithmetic (NET-4/5), grammar (NET-7).
   The load-bearing-depth regime was NOT achieved — it remains genuinely open.
2. **The exit law is corrected to EXIT-TRACKS-TASK-DIFFICULTY.** exit* is
   depth-INDEPENDENT: {2,3,4} across d=4..16 (d=16 exits at layer 4/16 = 75%
   saving, lossless within the 0.95 bar), vs ≈50% on NET-6's automata. The
   universal object is exit* ≈ crossover with the crossover TASK-DEPENDENT
   (≈d/2 on harder automata whose compute fills Phase I, ≈1–3 on easy grammar);
   |exit*−crossover| ≤ 1 in 17/18 across both task classes (one +3 outlier).
   NET-6's "exit* ≈ d/2" was an automaton-specific value, not universal.
3. **A partial refinement of the lossless claim.** Lossless-at-crossover holds only
   3/6 on Dyck (vs essentially all in NET-6): on easy tasks the crossover is much
   earlier and exit* lags it 1–3 layers; the reliable trigger is the fixed
   usability bar, which fires far below d/2 on easy tasks.
4. **The practical consequence is bigger, not smaller.** On easy-to-moderate
   sequential tasks a trained transformer's inference depth can be cut ~75%
   (exit at layer 2–4 of 16) losslessly with no confidence gate. The one regime
   where the exit law could have a boundary (genuine load-bearing depth) remains
   open — the next test is Dyck-2 multi-type matching, a width-starved Dyck, or
   unbounded nesting.

## What NET-8 established (depth axis, round 6 — the load-bearing test via the non-regular CFG)

1. **Depth is FLAT on Dyck-2 (the canonical non-regular context-free language) —
   the load-bearing test fails a THIRD time.** Two bracket types '(' vs '[',
   semilength 12, dm=48: all 10 models (d∈{1,2,4,8,16}×2 seeds) reach test=1.0000
   at every balance bin AND every close-position diagnostic (close_all=1.0000,
   close_b4+=1.0000). d=1 alone recovers the TYPE of the top of the stack (chance
   0.5 given only the balance) at every depth and every close number — including
   closes whose matching open sits 11+ tokens back. The two-layer
   "balance-in-L1/select-in-L2" construction is NOT needed. The flat-depth law now
   covers FIVE task classes: lookups (NET-2), composition (NET-3), decomposable-
   error arithmetic (NET-4/5), Dyck-1 regular grammar (NET-7), Dyck-2 non-regular
   CFG (NET-8).
2. **The exit law holds on a THIRD task class, and exit* is depth-saturated.**
   exit* ∈ {3,4,5} for d∈{4,8,16} (does not scale with d): 25% saving at d=4,
   37.5–50% at d=8, 69–81% at d=16, all lossless within the 0.95 bar (exit* acc
   0.9654–1.0000 vs full 1.0000). |exit*−crossover| ≤ 1 in 5/6 → 22/24 across all
   three task classes; exit* ≥ crossover in 5/6 (one +3 outlier d=16 s0, same class
   as NET-7's). Lossless-at-crossover 4/6 — fails exactly on the two d=16 models
   whose crossover fires at l=2 — confirming NET-7's refinement: the fixed 0.95
   usability bar, not the norm, is the reliable trigger when the crossover fires
   very early. NET-6's "exit ≈ d/2" is now conclusively scoped to hard automata
   whose compute fills Phase I.
3. **The single-layer stack-top recovery is GENUINE (barrier g, quantified).**
   Windowed linear baselines (last-K tokens + balance + position, K∈{4,8,12}, 3
   epochs) cap at close_all 0.7322/0.7544/0.7518 — never reaching 1.0 even when the
   matching open is inside the window — because a linear map cannot route the
   CONDITIONAL index "if the trailing run is k closes deep, read the open at
   distance 2k−1" for all k at once (needs gating/products); attention can
   (balance-conditioned position match). Transformer beats the strongest windowed
   baseline by +25pp on close_all (1.0 vs 0.7544), the honest hard-close
   diagnostic (the deep-balance bins rise on the baselines only because they are
   dominated by first-closes of deep runs, locally covered).

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
- **The exit law at real scale.** Does the decodability-crossover law survive on
  a real small LM / BERT (does the norm crossover predict the per-layer
  decodability cliff there too)? If yes, it gives a calibration-free dynamic
  depth schedule for inference — the strongest speed candidate now on the table.
- **The load-bearing-depth test.** NET-7 failed to reach it (bounded Dyck-1 is
  attention-solvable). Dyck-2 (multi-type bracket matching — genuinely
  non-regular context-free), a width-starved Dyck, or unbounded nesting is the
  natural next test of both the flat-depth law and the exit law's boundary.
- **Formula extraction as a compression tool** (the lab's second mandate):
  for algorithmic tasks, the extracted exact circuit (rank, frequency) IS a
  lossless compressed form; tie this to the quantization law.
- **Speed axis** is now open (NET-6 opened it with the exit law); attention-cost
  laws remain untouched.

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
- NET-6 added the exit-law caution: on sequential tasks the norm crossover
  (where ‖x_l‖ starts growing) predicts where a transformer becomes decodable —
  use it as a fixed inference-exit point (≈d/2, lossless) rather than a
  confidence gate, whose thresholds misfire because correct models keep
  probability spread.
- NET-7 sharpened the exit-law caution: the crossover is TASK-dependent, not d/2
  — on easy tasks (Dyck-1) it fires at layers 1–3 regardless of depth, so exit
  at the first usable layer (the fixed 0.95 bar), not at a depth-dependent rule;
  and bounded Dyck at dm=48 is attention-solvable (d=1 perfect), so it does NOT
  test load-bearing depth — use Dyck-2/width-starved/unbounded nesting for that.
- NET-8 confirmed the exit-law caution on a non-regular CFG and sharpened the
  flat-depth caution: single-layer transformers solve canonical stack-top recovery
  (Dyck-2 close-type, chance 0.5) at this scale — "deep is needed for syntax"
  claims must be checked against width/context-starved confounds; and the honest
  hard-close diagnostic is close_all (every k-th close of every run), NOT the
  deep-balance bins (which are dominated by first-closes of deep runs, locally
  predictable by windowed baselines).

Assessment v8. 8 experiments (NET-1, NET-2, NET-3, NET-4, NET-5, NET-6, NET-7, NET-8).

# Network/LLM Lab: Honest Assessment & Where a Real Win Could Come From

> Network research loop, opened 2026-08-12 (factoring loop paused). Same rigor
> as the factoring lab: exact measurable laws, honest negative results, all 8
> barriers checked each iteration. Count: 20 experiments, assessment v20.

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

- **The PR law at real scale — TESTED, does NOT transfer (NET-11); see the
  bottom frontiers block for the full update.** The monotone b*(PR) per-layer
  law fails on a real causal LM; only the coarse role structure (interface
  fragile / interior robust) survives.
- **Joint-aware allocation** — now the CONFIRMED real target (NET-11): per-layer
  isolation wildly undercounts joint damage on real text (isolated ≥95%
  everywhere at 3 bits vs joint 0.73–0.83), and depth amplifies it. A
  joint/activation-aware measure, not data-free per-matrix PR, is where the real
  LM win lives.
- **Formula extraction as a compression tool** (the lab's second mandate):
  for algorithmic tasks, the extracted exact circuit (rank, frequency) IS a
  lossless compressed form; tie this to the quantization law.
- **Speed / depth axes** — speed has the exit-law real-scale negative (NET-10)
  AND its first positive real-scale law (NET-15: attention is diffuse but
  top-k pruning is lossless at 8× — the DIFFUSE-BUT-PRUNABLE law); attention-cost
  laws at larger scale (d=8 / longer ctx) are the open next step; depth has had
  8 iterations.

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

## What NET-9 established (depth axis, round 7 — the load-bearing boundary via context and width scaling)

1. **The load-bearing boundary is NOT found at context ≤64 or width ≥12.** d=1
   reaches test=1.0000 at every metric on all 16 models — Part A semilength
   s∈{16,32} (context 32/64, matching opens up to 63 tokens back) at dm=48,
   d∈{1,2}×2 seeds; Part B width dm∈{16,12} (head dim 4 and 3) at s=12, d∈{1,2}×2
   seeds. The non-flat screen found NO config with d=1 < d=2. The flat-depth law
   now covers five task classes AND holds across context and width scaling on the
   non-regular grammar.
2. **The mechanism reading is now explicit: single-layer soft attention implements
   a bounded stack.** The stack-top STATE of a bounded Dyck word IS the scalar
   running balance (one head's prefix-sum); the stack-top CONTENT is positionally
   stored (attention routes each close query to the matching open at
   balance-depth balance_before−1 via balance-conditioned key match + recency, and
   reads the stored type). No second layer is needed because the state is scalar
   and the content is at a computable position. The boundary would need: balance
   range exceeding dm precision (s≫64), unbounded nesting/length-gen (a different
   axis — NET-4's wall), or NON-POSITIONAL stack content (content computed from
   multiple distant positions — the genuinely hard case and the natural next
   load-bearing target).

## What NET-10 established (real-scale rotation — the causality screen and the exit law on a real LM)

1. **The toy depth line's perfect scores were a full-attention future-peek
   artifact (proven, not argued).** The TF class uses FULL (bidirectional)
   attention on next-token tasks, so at position t the model attends to position
   t+1 — the answer token — and a copy-the-future circuit gives 100% on any
   deterministic next-token task. The leak is airtight via an information bound:
   on Dyck-2, new-open types are iid random and 47.8% of next-tokens are opens,
   so the causal ceiling is 0.7609 overall < the recorded full-attention 1.0000.
   Causal re-runs at the same architecture/budget confirm it: Dyck-2 d=1
   overall 0.557 / close_all 0.917 (d=2: 0.563/0.926) vs the recorded 1.0000;
   extended budget asymptotes close_all near 0.92 (0.9105→0.9135→0.9207 at
   6k/12k/18k). Causal lookup (deterministic, ceiling 1.0): ~0.89 vs NET-2's
   1.0000 — the artifact is NOT limited to random-type tasks.
2. **What survives the honesty fix:** (i) the flat-depth SHAPE — causal
   d=1 ≈ d=2 within noise on both a deterministic and a random-type task; (ii)
   transformer-beats-linear on close recovery, now fairly compared — causal
   transformer 0.917 close_all vs causal windowed-linear 0.75 (+17pp; the NET-8
   +25pp mixed a causal baseline with a full-attention transformer). Corrected:
   NET-8/9's "d=1 = 1.0000 / load-bearing-boundary-not-found" absolute claims
   are withdrawn as measurement artifacts — d=1 is 0.92/0.89, not perfect.
3. **The exit law does NOT transfer to a real LM (0/4 lossless at crossover).**
   Real causal GPT on 5 Gutenberg novels (dm=64, vocab 4097, ctx 128, d∈{4,8}×2
   seeds, teacc 0.157–0.162): the norm profile is reset-then-grow (dip then
   monotone growth, crossover at l=2–4), NOT the toy's flat-≈d/2-then-grow;
   shared-head acc climbs monotonically through the full depth — crossover marks
   the ONSET of decodability growth, not its completion. |exit*−cross|=2/2/5/3,
   lossless@cross=False in 4/4. The calibration-free dynamic-depth-schedule idea
   is not supported at real-LM scale (bar sensitivity: the 0.95-bar needs full
   depth; a 0.80-bar would exit at crossover on d=8 s0 with 63% saving — but
   that is not lossless).

## What NET-11 established (compression-axis real-scale rotation — the PR law on a real LM)

1. **The role structure of NET-1's attention reversal survives the real-scale
   transfer, but the monotone b*(PR) law does NOT transfer as a per-matrix
   predictor.** On a real causal word LM (same 5 Gutenberg novels, dm=64,
   vocab 4097, ctx 128, d=4 and d=8, full acc exactly reproduces NET-10:
   0.1571/0.1619), per-matrix RTN bit-need is IDENTICAL across both depths:
   attention projections (PR 19–32) are 2-bit lossless (retained 0.99–1.0);
   MLP projections (PR 31–52) need 3 bits; embed (PR 63) and pos (PR 40) need
   4 bits; the readout un (PR 14.9–15.3 — the LOWEST PR in the model) needs 4
   bits with a catastrophic 2-bit collapse (acc 0.043/0.051, 27–32% retained);
   LayerNorm weight (PR=1) is 2-bit lossless. The counterexample is decisive:
   lowest-PR readout needs the most bits, and within the PR≈29–31 band attention
   is 2-bit lossless while mo0 (PR 30.8) needs 3. corr(PR,b*) = +0.58/+0.67 is
   role-grouping in disguise, not a law. Interface-fragile / interior-robust
   survives; PR-as-predictor does not.
2. **NET-1's practical schedule is REFUTED at real scale: no static RTN
   schedule ≤3.7 avg bits is lossless on real text.** Joint uniform-2 collapses
   (retained 0.16 d=4 / 0.05 d=8); joint uniform-3 is NOT lossless (retained
   0.83 d=4 / 0.73 d=8, WORSE with depth — per-layer isolation says almost
   everything is ≥95% at 3 bits, yet compounding costs 17–27 points, amplified
   by residual-stream norm growth through depth, the NET-2/NET-10 mechanism).
   The role-schedule follow-up (d=4 retrained, full acc re-verified 0.1571):
   role(4/3/2) retains 0.878 at 3.64 avg bits (+5pts over uniform-3 at +21%
   bits, still 12% short of lossless); role-tighter (mi=4) 0.897 at 3.73.
   NET-1's toy "uniform-3 lossless (0.98–1.0)" does not hold on real text.

## What NET-12 established (compression-axis rotation — joint-aware allocation on the real LM)

1. **The joint-marginal map quantifies the wall — and shows "attention is
   free" is an operating-point artifact.** With all other matrices pinned at the
   role schedule, attention projections (all 16) are exactly indifferent at 2
   bits (retained flat at 0.878), while embed and un are jointly far more
   fragile than isolation suggested: embed 3-bit jointly retains **0.849**
   (isolation ≈0.95), un (readout) 2-bit collapses to **0.280**. The interface
   is the wall; the interior is cheap — *at a degraded operating point*.
2. **The per-tensor greedy strict-lossless frontier is ~5.3 avg bits, and
   even all-4 misses the bar.** Greedy from all-6 down, keeping retained ≥
   0.98·full, lands at **5.31 avg bits / retained 0.982** with the interface
   (embed/pos/un — 73% of params) pinned at 6. Baseline joint evals: uniform-3
   0.825, role(4/3/2) 0.878, **all-4 0.979 (misses by one point)**, all-6 0.999.
   Per-tensor static RTN cannot get under ≈5.3 bits losslessly on real text.
3. **Per-channel (per-row) RTN is the fix: uniform all-4 is lossless at 4.00
   bits (0.987), 1.3 bits below the per-tensor frontier.** Per-row uniform-3
   still fails (0.947) — the 4-bit interface is irreducible even per-channel;
   uniform-2 remains hopeless (0.588). The per-tensor-optimized frontier does
   NOT transfer per-row (0.973) — allocation must be tuned to the primitive.
4. **The rotation's literal question is answered no.** Per-row "4-bit interface
   + all interior 2" retains 0.733 @ 3.46 bits; "4-bit interface + MLP 4 +
   attention 2" retains 0.907 @ 3.82 bits; uniform-4 is 0.987. The 8-point gap
   between the last two is almost all attention 2→4 — so NET-11's "attention
   is 2-bit lossless" is corrected: true in isolation and at a degraded
   operating point, but 2-bit attention costs ~8 points in a clean joint net.

**Corrections to NET-11:** "no static RTN schedule ≤3.7 avg bits is lossless"
was about the *per-tensor* primitive; with per-channel scales a uniform-4
schedule IS lossless (4.0 bits). And "attention projections 2-bit lossless"
does not survive a clean joint network. **NET-12's practical lever: the
per-channel primitive + uniform 4-bit, data-free — not smarter per-tensor
allocation.**

## What NET-13 established (compression-axis rotation — activation-aware/outlier allocation on the real LM)

1. **The quantization axis is not the lever.** Per-column (input-channel)
   symmetric RTN — the standard group-quant axis — is WORSE than per-row at
   this scale (uniform-2 0.413 vs 0.588, uniform-3 0.900 vs 0.947); per-row
   (output-channel) remains the better primitive. The axis does not break the
   4-bit interface floor.
2. **The interface has only MILD outlier structure (the key diagnostic).**
   Top-1% of magnitude holds only ~3.5% of the mass in EVERY matrix (embed
   3.6%, un 3.5%, interior 3.0–3.4%); row-norm max/mean 1.1–1.9; the heaviest
   tail is un (kurtosis 9.1) — nowhere near the 30–70% outlier concentration
   of larger-LM regimes. This small real causal LM is NOT in the outlier regime
   that LLM.int8/AWQ/SmoothQuant target.
3. **Magnitude split fails — the need is distributed.** Interface rows at top-k
   ∈ {0..256} promoted to 6-bit, rest 2-bit: k=256 (top-6%) reaches only
   **0.819** at 2.74 bits — sublinear, saturating, 16 points short of lossless.
   Magnitude-aware allocation cannot shrink the schedule below ~4 bits.
4. **Outlier clipping is a no-op.** SmoothQuant/AWQ-style percentile-scaled
   per-row RTN (99.9th/99.0th percentile) changes nothing: uniform-3 stays
   0.944–0.948 (under bar), uniform-4 stays lossless (0.982–0.985). Consistent
   with point 2 — no outlier mass to clip.

**Correction to the NET-12 frontier note:** the "activation-aware (outlier)
allocation" lever — the last data-free compression idea — is now TESTED and
fails: the 4-bit interface floor survives every standard data-free
weight-quantization primitive (axis, magnitude-split, clipping) because the
small causal LM lacks the outlier regime those methods exploit. The interface's
bit-need is distributed and the floor is structural at this scale. The honest
remaining lever is genuinely activation-aware quantization (SmoothQuant-style
per-channel activation scales from calibration passes) — the one thing not
data-free.

## What NET-14 established (compression-axis rotation — activation-aware quantization WITH calibration passes)

1. **The last lever is a no-op-to-negative.** AWQ/SmoothQuant-style per-channel
   activation scales (calibration on 512 training sequences) absorbed into the
   weight quantizer do NOT break the per-row uniform-3 floor: best α=0.5
   retains **0.943** vs plain per-row 0.947 (marginally worse), α=1.0 collapses
   to 0.888; uniform-4 stays identically lossless (0.987) both ways. The
   calibration pass buys nothing.
2. **The mechanism fails because the activation scales are nearly FLAT.**
   Mean per-channel activation max across the model: un 2.130 / wq0 2.116 /
   mi0 2.117 / mo0 1.820, max/mean ratios 1.07–1.24. AWQ's absorption only pays
   when some channels carry 10–100× the activation magnitude of others; at this
   scale there is no channel heterogeneity to exploit — the activation-side
   mirror of NET-13's flat weight-outlier structure.
3. **The interface-at-3 probe still fails.** Interface (embed/pos/un) at 3 with
   AWQ scales, interior clean: **0.958 @ 3.18 bits** — 2.2 points short of
   lossless. Calibration applied directly to the interface does not make 3-bit
   lossless.
4. **Activation-informed allocation is a BAD signal.** 25 Linears ranked by mean
   per-channel act max, terciles 4/3/2: **0.828 @ 3.69** (0.841 with AWQ) — far
   worse than the weight-based role schedule (0.892 @ 3.64) and 16 pts below
   uniform-4 (0.987). The ranking only re-discovers the interface is fragile; it
   cannot allocate below 4 bits.

**Correction to the NET-13 frontier note:** the last remaining compression
lever — activation-aware quantization with calibration passes — is now TESTED
and also fails. The 4-bit interface floor is not just data-free-irreducible
(NET-13) but **activation-irreducible** (NET-14) at this scale: even calibration
passes don't buy sub-4-bit lossless weight quantization on a small causal LM,
because the per-channel activation scales are near-uniform (max/mean ≈ 1.2).
**The compression axis at small real-LM scale is EXHAUSTED** — per-channel
uniform-4 (4.00 bits, 0.987, data-free) is the practical optimum. Remaining
compression options are strictly larger-scale (d=8 / bigger dm) or the speed
axis.

## What NET-15 established (speed-axis rotation — the attention-cost law, FIRST POSITIVE REAL-SCALE SPEED RESULT)

1. **Trained causal attention is DIFFUSE, not concentrated.** Per-query effective
   support exp(H) mean **46.6 of 128** (uniform-causal baseline ≈64.5; only ~28%
   more concentrated), per-head 39.5–54.7; top-8 mass only 0.450, top-32 0.795.
   The "attention concentrates on a few tokens" premise is refuted at this scale
   (dm=64, 4 heads).
2. **Yet data-free top-k key/value pruning is LOSSLESS at 12.5% of context.**
   k=16 retains **0.984** (≥0.98 bar) with loss 5.1370 vs full 5.1188 (+0.36%
   rel) at an **8× attention-core FLOP reduction**; k=32 → 0.998 at 4×; k=64/96
   → exact (verifies the explicit-attention eval path). Knee between k=8
   (0.971, fails) and k=16.
3. **The selection is genuine.** Random-k control: 0.922/0.950 at k=16/32 vs
   top-k 0.984/0.998 (−4.8 to −6.2 pts); random-16 is even worse than top-8 —
   the best 8 positions by weight beat any 16 at random.
4. **The cost law is nearly total.** At ctx 128/dm 64 the attention core is ~95%
   of inference FLOPs, so the L/k ratio is the total-model law: **8× attention
   ≈ 5–6× total-model speedup, data-free, no retraining, no calibration, no
   concentration assumption.**

**DIFFUSE-BUT-PRUNABLE law:** attention need not be sharply concentrated for
lossless top-k pruning at ~12% of context on real text — the mass beyond the
top-k is low-information and renormalization concentrates the retained mass
onto informative positions. First positive real-scale speed result (NET-6/7/8
toy positives; NET-10 real-scale negative). Open: does the concentration law /
lossless-k shift at larger scale (d=8 / bigger dm / bigger vocab)?

## What NET-16 established (depth-scaling of the attention-cost law — k* ≈ 4d, concentration depth-independent)

1. **The concentration law is DEPTH-INDEPENDENT.** At d=8 on the same real
   causal LM (full acc 0.1619, loss 5.0788; d=4 0.1571/5.1188), effective
   support mean **50.1 of 128** (d=4: 46.6) — if anything slightly MORE diffuse
   with depth; top-k mass fractions lower at every level (top-16 0.586 vs
   0.617). The diffuse regime is a stable property of this model scale.
2. **Lossless-k GROWS with depth — k* ≈ 4·d.** The lossless knee moves from
   k=16 (d=4, retained 0.984) to **k=32 (d=8, retained 0.983)**: k=16 FAILS at
   d=8 (0.961 < 0.98). Every retained fraction drops and Δloss roughly doubles
   at each k — per-layer top-k error compounding through the residual stream,
   the speed-axis mirror of NET-11's compression compounding. The practical
   lever decays: 8× attention-core at d=4 → 4× at d=8.
3. **Selection importance GROWS with depth.** Random-k gap: +6.2 → **+9.5 pts**
   (k=16) and +4.8 → **+7.1 pts** (k=32) from d=4 to d=8 — the deeper model
   relies more on the trained selection information.
4. **The d=16 prediction is under test (round-net-17, running):** if k* ≈ 4d
   continues, k*=64 at d=16 (only 2× attention-core) — the lever nearly gone at
   depth. The attention-cost law is real but its leverage is a shallow-depth
   property at fixed ctx.

**LAWS:** CONCENTRATION-LAW-DEPTH-INDEPENDENT + LOSSLESS-K-SCALES-WITH-DEPTH
(k* ≈ 4d at fixed ctx) + SELECTION-IMPORTANCE-GROWS-WITH-DEPTH. DIFFUSE-BUT-
PRUNABLE survives with a documented depth boundary.

## What NET-18 established (compression-axis rotation — the depth-robustness check of the per-channel uniform-4 practical optimum)

1. **The 4-bit interface floor is NOT depth-robust.** At d=8 on the same real
   causal LM (full acc 0.1619, loss 5.0788), the flagship per-row uniform-4 —
   lossless at d=4 (0.987 ≥ 0.98) — falls to **0.967, below the bar**. The
   depth penalty lands at every bit level, worst where the schedule sits near
   the robustness cliff: uniform-3 per-row −7.4 pts (0.947 → 0.873), role −9.1
   pts (0.892 → 0.801), per-tensor uniform-3 −12.0 pts (0.825 → 0.705, agreeing
   with NET-11's d=8 0.73 within eval noise).
2. **The drop that matters is the small one.** Uniform-4 loses only ~2 pts at
   d=8 — but that is exactly the margin that cost it losslessness. NET-11's
   "deeper = worse compounding" is confirmed at EVERY bit level, not just
   uniform-3.
3. **The compression axis is now closed at d=4 AND its floor does not transfer
   to d=8.** Both axes' lossless operating points shrink with depth at fixed
   width — the compression mirror of NET-16's k* ≈ 4d. Any 4-bit lossless claim
   must quote the depth.

**LAW:** DEPTH-DEEPENS-QUANT-FLOOR. The per-channel uniform-4 practical
optimum is a depth-4 property.

## What NET-17 established (speed-axis rotation, round 4 — k* = 4·d confirmed across three depths)

1. **The k* = 4·d law is CONFIRMED across {4,8,16}.** At d=16 on the same real
   causal LM (full acc 0.1610, loss 5.0830, bar 0.1578), data-free top-k
   key/value pruning requires **k*=64** (retained 0.995 ≥ 0.98, Δloss +0.006);
   k=32 fails (0.972). The three-depth ladder k*=16/32/64 is exact.
2. **The mechanism is per-layer compounding: retained(k,d) ≈ r(k)^d.** The
   d=8 per-layer retentions predict the d=16 totals within 0.006 (k=16 pred
   0.924 vs 0.929; k=32 0.966 vs 0.972; k=64 0.994 vs 0.995). The knee is
   where r(k)^d crosses 0.98, giving a linear-in-depth kept window.
3. **The concentration law is corrected: diffuse but mildly depth-DRIFTING.**
   Effective support 46.6 → 50.1 → **53.3** (+14% relative across depth) and
   top-16 mass 0.617 → 0.586 → 0.556; attention remains diffuse at every
   depth (53.3 ≪ 64.5 uniform-causal), but "depth-independent" is refuted in
   the strict sense (NET-16 overstated it).
4. **The random-k selection gap WIDENS with depth:** +6.2/+4.8 (d=4) →
   +9.5/+7.1 (d=8) → **+11.7/+9.8 pts (d=16)** — the compounding signature
   (each layer's low-information-tail error multiplies through the stack).
5. **The cost law is `speedup ≈ ctx/(4d)`.** At fixed ctx=128 the lever decays
   8×→4×→**2×** with depth; but k* grows linearly in depth, NOT in context, so
   at long context the lever grows (projected **64×** at ctx=4096, d=16 —
   k*'s context-independence untested, the natural next speed check).

**LAW:** LOSSLESS-K-SCALES-WITH-DEPTH, now exact across three depths — k* = 4·d,
per-layer compounding r(k)^d, selection gap widening with depth.

## What NET-20 established (speed-axis rotation, round 5 — the context-scaling check of the attention-cost law)

1. **k* is NOT context-independent.** At d=4, doubling ctx (128→256) doubled
   the lossless window — k*=16 (0.984 ✓ at 128) FAILS at 256 (0.971 ✗); the
   knee moves to k*=32 (0.989 ✓). Exactly proportional at this resolution
   (k* = ctx/8 at d=4).
2. **The lever is context-CONSTANT — speedup ≈ 32/d.** Unified across
   NET-16/17/20: **k* = d·ctx/32** (fits all four measurements), so
   **speedup = ctx/k* = 32/d**, independent of context: 8× at d=4 at BOTH 128
   and 256, 4× at d=8, 2× at d=16. **NET-17's projected 64× at ctx=4096 is
   REFUTED** — long context buys no additional relative saving because the
   lossless window scales with it.
3. **The concentration law is context-DEPENDENT.** Eff support 46.6 → **82.9**
   (relative to uniform: 0.36 → 0.65 — MORE diffuse at longer context);
   per-fixed-k mass lower at every k; per-position breakdown (new): eff grows
   with past available (early 11.3 / mid 72.3 / late 155.4) — **no bounded
   working set**, the concentration-side reason k* must grow.
4. **Selection still matters at 2× context:** random-k gap +8.7/+6.0 pts
   (same magnitude as ctx=128).

**LAW:** LOSSLESS-K-SCALES-WITH-CONTEXT (k* ∝ ctx at fixed depth) ⇒ the
attention-FLOP lever is **context-constant: speedup = 32/d** (a depth-only
property), unifying the depth and context dependence as k* = d·ctx/32.

## What NET-19 established (depth-axis rotation, round 9 — the carry chain at scale, dm=192)

1. **Scale unlocks length-SPECIFIC mastery, not composition.** At 4.5–18×
   NET-5's parameter count (dm=192, bs=256, 12000 steps), the n=6 carry chain
   is mastered by ALL 9/9 configs (d=1 0.9940±0.0085, d=2 1.0000, d=4
   0.9976±0.0035) — including all three d=1 seeds (NET-5's under-powered d=1
   failed 2/3). Fixed-length addition is scale-SOLVED at every depth.
2. **The depth law stays flat — depth pays nothing even at scale.** The d=1 vs
   d=4 gap is 0.0036, within seed noise. Credit-assignment depth-immunity holds
   at 18× scale and 3× data: the carry chain's binding constraint is
   optimization (decomposable-error credit assignment), never capacity.
3. **The length wall is depth- and scale-immune — 9/9 at chance.** Every
   mastered config re-trained at n=3 (8/9 full=1.0000; d=1 s=2 reached
   per=0.8010/full=0.2041 — the NET-5 carry-chain dissociation, per-high/
   full-low correlated errors, reproduced at dm=192) then tested n=4/5/6:
   **full=0.0000 at every depth and seed** (per ≈ 0.09–0.22 ≈ digit floor vs
   chance 1e-5/1e-6/1e-7). The memorize-without-compose wall (NET-3 leg-2 /
   NET-4/5) survives the largest arithmetic scale tested in the program.
4. **Deterministic replication confirmed.** The fast probe (task #89) matched
   the marathon's d=1 s=0 and d=4 s=0 Part B numbers BYTE-IDENTICAL (same
   seed/settings ⇒ identical results) — the length wall at the two depth
   extremes was confirmed 6h before the marathon finished.
5. **The carry chain is now the best-characterized hard problem in the
   program.** Fixed-length = depth-flat and scale-solved; length-gen = depth-
   and scale-immune. Do not scale depth (or width) to fix length-general
   arithmetic — attack the objective (carry curriculum, scratchpad/CoT
   intermediates, a stateful carry cell / recurrence).

**LAW:** SCALE-UNLOCKS-LENGTH-SPECIFIC-MASTERY-NOT-COMPOSITION +
CREDIT-ASSIGNMENT-DEPTH-IMMUNITY-HOLDS-AT-SCALE. The depth axis has had 9
iterations; compression (exhausted at d=4, not depth-robust at d=8) and speed
(context-constant lever 32/d) are the standing axes.

## Where a genuine breakthrough could come from (frontiers)

- **The PR law at real scale — tested, does NOT transfer (NET-11).** The
  monotone b*(PR) per-layer law fails as a per-matrix predictor on a real
  causal LM (readout PR≈15 lowest → needs the most bits; same-PR attention vs
  MLP differ); the surviving object is the coarse role structure (interface
  fragile / interior robust). PR is not a calibration-free bit-schedule at this
  scale.
- **Joint-aware allocation — tested (NET-12/13/14), answer by primitive, and
  the compression axis is EXHAUSTED at this scale.** Per-tensor greedy floor
  ~5.3 avg bits; per-channel uniform-4 is lossless at 4.00 bits (0.987) with
  the 4-bit interface irreducible even per-channel (uniform-3 0.947). NET-13
  tested every data-free lever (per-column axis, magnitude-split, clipping —
  all fail; small LM lacks the outlier regime, top-1% share ~3.5%). NET-14
  tested the last lever, activation-aware quantization WITH calibration passes
  (AWQ/SmoothQuant per-channel activation scales): no-op-to-negative at
  uniform-3 (α=0.5: 0.943 vs 0.947), interface-at-3 still 2.2pts short (0.958),
  activation-informed allocation far worse than weight-based (0.828 vs 0.892)
  — because the activation scales are near-uniform (max/mean ≈ 1.2). The 4-bit
  interface floor is both data-free-irreducible AND activation-irreducible at
  this scale; the practical optimum is per-channel uniform-4 (4.00 bits,
  data-free). **NET-18 answered the d=8 check: the floor is NOT depth-robust —
  uniform-4 falls to 0.967 at d=8 (below bar), uniform-3/role fall 7–9 pts, so
  the practical optimum is a d=4 claim and the depth must be quoted.**
- **Small-BERT check of the PR law and joint-aware allocation** — the
  documented domain boundary (NET-1 reverses on attention LMs) makes the
  real-LM-class transfer the highest-value next compression step.
- **The carry chain at scale.** NET-4/NET-5 leave the carry chain as the
  irreducible width/depth/readout-immune bottleneck. The genuinely open depth
  question is whether the chain responds to depth at LARGER scale (bigger
  d_model, more data, longer training) or whether credit-assignment walls are
  depth-immune in general. A curriculum that teaches carries one column at a
  time is the other untested lever.
- **The exit law at real scale — tested, does NOT transfer (NET-10).** The
  norm crossover marks the ONSET of shared-head decodability growth on a real
  causal LM, not its completion: 0/4 models are lossless (0.95·full) at the
  crossover; the toy's flat-≈d/2-then-grow norm profile is replaced by
  reset-then-grow. The calibration-free dynamic-depth-schedule idea is not
  supported at real-LM scale. Remaining speed candidates: PR-based layer
  dropping informed by actual per-layer loss, or depth-4-8 model families where
  the 0.80-bar early-exit (≈63% saving on d=8 s0, non-lossless) is acceptable —
  an explicitly lossy inference cut, not the calibration-free law we hoped for.
- **The load-bearing-depth boundary — and the toy line must be re-screened
  causally.** NET-10 proved the toy 1.0000s were full-attention future-peek
  artifacts (ceiling 0.7609 on Dyck-2; causal lookup 0.89). The load-bearing
  hunt now has honest targets: NON-POSITIONAL stack content, s≫64, unbounded
  nesting — tested causally from the start. NET-7's Dyck-1 and the
  arithmetic/composition tasks are deterministic (ceiling 1.0) and so not
  refuted by the bound, but their absolute scores still need the causal screen
  (only lookup and Dyck-2 have been re-run so far).
- **Formula extraction as a compression tool** (the lab's second mandate):
  for algorithmic tasks, the extracted exact circuit (rank, frequency) IS a
  lossless compressed form; tie this to the quantization law.
- **Speed axis — TESTED with positives (NET-15/16/17): the attention-cost law.**
  Trained causal attention is DIFFUSE (effective support ≈46.6–53.3/128 across
  d=4/8/16, only ~17–28% more concentrated than uniform; the mild upward drift
  with depth does NOT change the diffuse verdict) yet data-free top-k key/value
  pruning is LOSSLESS at k*=16 (d=4: 0.984 ≥ 0.98 bar, 8× attention-core, loss
  +0.36% rel; ≈5–6× total at ctx 128 where attention is ~95% of FLOPs);
  weight-selected positions beat random by +4.8–11.7 pts (the gap GROWS with
  depth). Lossless-k scales with depth — **k* = 4·d, CONFIRMED across
  {4,8,16}** (k*=16/32/64), mechanism per-layer compounding retained(k,d) ≈
  r(k)^d. **NET-20 added the context point and refuted the growth-with-context
  projection: k* also scales with context (k*=16→32 at d=4 when ctx doubles),
  and the unified law is k* = d·ctx/32 — so the lever is context-CONSTANT,
  speedup = 32/d** (8× at d=4 at any ctx, 4× d=8, 2× d=16; the projected 64×
  at ctx=4096 is refuted — long context buys no extra relative saving). The
  exit law (NET-6/7/8 toy, NET-10 real-scale negative) and the attention-cost
  law are the speed results so far.

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
- NET-9 pushed the load-bearing boundary past context 64 and width 12 without
  finding it: single-layer soft attention implements a bounded stack (scalar
  balance pointer + positional content retrieval), so bounded grammar gives depth
  nothing at any affordable scale — the next load-bearing test must use
  NON-POSITIONAL stack content (content computed from multiple distant
  positions), much larger contexts, or unbounded nesting; and the depth axis has
  had 7 iterations — rotate to the real-scale checks on the speed/compression
  axes (exit law / PR law on a small LM).
- NET-10 added the two most important cautions of the lab: (1) the TF-class
  full-attention/next-token framing put the answer in the input — check EVERY
  next-token toy experiment for the copy-the-future shortcut (causal ceiling
  bound before trusting 1.0000s); the toy depth line's absolute 1.0000s are
  withdrawn, the flat-depth SHAPE and transformer-beats-linear comparisons
  survive. (2) The exit-law cautions above (NET-6/7/8) are TOY-SCALE: on a real
  causal LM the norm crossover marks the onset of decodability, not a lossless
  exit (0/4 lossless at crossover) — do not build dynamic-depth inference on the
  toy crossover; and real-LM norm profiles are reset-then-grow, not
  flat-then-grow.
- NET-11 added the compression-axis real-scale caution: per-matrix RTN
  isolation is a poor predictor of joint behavior on real text (isolated ≥95%
  at 3 bits almost everywhere vs joint uniform-3 retaining only 0.73–0.83, and
  deeper = worse); no static RTN schedule ≤3.7 avg bits is lossless at this
  scale. Do not ship uniform-2/3 weights for a real causal LM on the strength of
  toy/isolated measurements, and do not trust PR as a per-matrix bit-need
  predictor (the low-PR readout is the most fragile matrix). The interface
  (embed/pos/un) needs ≥4 bits; joint/activation-aware allocation is the only
  live compression lever.
- NET-12 refined that caution into a primitive split: per-tensor RTN has a
  strict-lossless floor of ~5.3 avg bits (interface pinned at 6 — even all-4
  misses the bar by one point), but the PER-CHANNEL primitive + uniform-4 is
  lossless at 4.00 bits. Two traps remain: (1) "attention is 2-bit free" —
  TRUE in isolation and at degraded operating points (it is masked by bigger
  errors), but 2-bit attention costs ~8 points in an otherwise-clean joint
  network — do not trust cheap-layer "wins" measured on a degraded baseline;
  (2) a schedule optimized for one quantization primitive does not transfer to
  another (the per-tensor greedy frontier scores WORSE per-row than uniform-4).
  The 4-bit interface (embed/pos/un) is the irreducible floor at this scale
  under both primitives.
- NET-13 closed the last data-free compression lever: activation-agnostic
  outlier methods (per-column axis, magnitude-split, percentile-clipping) do
  NOT break the 4-bit interface floor on a real causal LM — the small LM is
  NOT in the outlier regime (top-1% magnitude share ~3.5% everywhere, vs
  30–70% for larger LMs), so the floor is structural, not an outlier artifact.
  Do not expect AWQ/SmoothQuant-style weight-side fixes to buy sub-4-bit
  lossless quantization at this scale.
- NET-14 closed the compression axis itself at this scale: activation-aware
  quantization WITH calibration passes (the one non-data-free lever NET-13
  left open) is ALSO a no-op-to-negative — AWQ per-channel activation scales
  are near-uniform (max/mean ≈ 1.2 across the model), so the absorption has no
  channel heterogeneity to exploit; interface-at-3 stays 2.2pts short (0.958),
  and activation-informed allocation is far worse than weight-based (0.828 vs
  role 0.892). The 4-bit interface floor is both data-free-irreducible AND
  activation-irreducible here. Do not expect even calibration-based methods to
  beat per-channel uniform-4 (4.00 bits, data-free) on a small causal LM; the
  only remaining compression question is whether the floor shifts at larger
  scale (d=8 / bigger dm).
- NET-15 added the first positive real-scale speed caution: trained attention is
  DIFFUSE (effective support ≈47/128), yet data-free top-k key/value pruning is
  LOSSLESS at k=16 (0.984 ≥ 0.98 bar, +0.018 loss, 8× attention-core FLOPs). The
  caveat is scale: this is measured at dm=64/ctx 128 — the concentration law and
  the lossless-k may shift at larger scale (d=8, bigger dm, longer contexts), so
  the practical 5–6× speedup claim is scale-contingent. Two standing traps from
  the result: (1) concentration is NOT the justification for sparsity here —
  "attention is focused" is empirically false at this scale even though pruning
  works; (2) random-k loses 4.8–6.2 pts to weight-selected top-k, so the
  selection information is the content, not merely the reduced support. Do not
  build top-k inference without the weight-selected mask, and do not generalize
  the diffuse regime to larger models without re-measuring effective support.
- NET-16 added the depth boundary of the attention-cost law: lossless-k scales
  with depth (k* ≈ 4d at fixed ctx 128: k*=16 at d=4, k*=32 at d=8) — a
  k* measured at one depth does NOT transfer to another; per-layer top-k error
  compounds through the residual stream (the speed-axis mirror of NET-11's
  compression compounding). The concentration law IS depth-independent (eff
  support ≈47–50), but lossless-k and the selection gap both grow with depth.
  Do not quote the NET-15 8× lever without its depth: at d=8 it is 4×, and the
  d=16 prediction (k*=64, 2×) is under test.

Assessment v20. 20 experiments (NET-1, NET-2, NET-3, NET-4, NET-5, NET-6, NET-7, NET-8, NET-9, NET-10, NET-11, NET-12, NET-13, NET-14, NET-15, NET-16, NET-18, NET-17, NET-20, NET-19).

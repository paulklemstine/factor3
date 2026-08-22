# Network/LLM Lab: Honest Assessment & Where a Real Win Could Come From

> Network research loop, opened 2026-08-12 (factoring loop paused). Same rigor
> as the factoring lab: exact measurable laws, honest negative results, all 8
> barriers checked each iteration. Count: 25 experiments, assessment v25.

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

## What NET-21 established (performance axis — the training-schedule test of the carry-chain length wall)

1. **The length wall is schedule-robust — every schedule fails beyond-max.**
   Curriculum-grow (2→3→4→5), length-mixing {3,4,5}, plain-n3, and plain-n5
   training were tested at dm=192/untied/12000 steps, seed 0, pos-emb enlarged
   22→32 so beyond-max n=6/7/8 fits. **Beyond-max length-gen is at chance in
   EVERY arm** (n=6/7/8 full=0.0000). The plain-n5 control (E) — "trained
   longer" in isolation — also fails (masters n=5=1.0000, n=6/7/8 chance):
   the wall is NOT a training-distribution artifact. NET-19's named open lever
   "carry curriculum" is REFUTED as a cure.
2. **NEW — MIXING PREVENTS MASTERY.** Training on mixed lengths {3,4,5}
   (arm B) never masters ANY length: per-digit stuck at 0.54–0.67 / full
   0.00–0.02 for all 12000 steps — the carry-dissociation correlated-error
   regime (per ≫ per^n) is PERMANENT under length diversity. Diversity blocks
   length-specific mastery without yielding length-general mastery.
3. **NEW — CURRICULUM FORGETS INTERMEDIATE LENGTHS.** The d=2 curriculum
   (arm D) mastered n=5 perfectly (1.0000, per-position all 1.0000) but n=4 —
   trained for 3000 steps — collapsed to chance (0.0000). Final-length training
   OVERWRITES intermediate lengths: the optimizer converges to a single
   length-SPECIFIC attractor (the last length), never a length-parameterized
   general algorithm.
4. **The mechanism sharpened.** Three manifestations of the same optimizer
   attractor: the copy-self basin (NET-4/5), the carry dissociation
   (per-high/full-low correlated errors), and now curriculum-forgetting /
   mix-never-masters. Adding length diversity does not move the optimizer toward
   the general solution — it either blocks mastery entirely or specializes to
   the last length seen.
5. **The right next levers change the problem, not the schedule.** Do NOT invest
   in schedule-only fixes for length-general arithmetic. Untested levers in
   priority order: scratchpad/CoT intermediate tokens (change the task),
   recurrence / stateful carry cell (change the architecture), explicit length
   conditioning (change the input). A second-seed replication of the two new
   phenomena is the strengthening step (1 seed per arm this round; the stark
   1.0000-vs-0.0000 readings and the in-run plain-n3 control that reproduces the
   known wall exactly keep the verdict robust).

**LAW:** LENGTH-WALL-IS-SCHEDULE-ROBUST + MIXING-PREVENTS-MASTERY +
CURRICULUM-FORGETS-INTERMEDIATE-LENGTHS. The depth axis has had 9 iterations;
the carry chain is characterized on depth, scale, AND schedule — all negative
for length-general composition; compression (exhausted at d=4, not depth-robust
at d=8) and speed (context-constant lever 32/d) are the standing axes.

## What NET-22 established (performance axis — the task-remodeling test of the carry-chain length wall)

1. **Scratchpad does NOT unlock length-gen.** Explicit per-column carry targets
   (a maximal scratchpad/CoT: `SC c_1..c_n GO s_1..s_n c_n`, carries AND answers
   teacher-forced) were tested at dm=192/untied/bs=256/12000 steps, 2 seeds at
   d=1 and 2 seeds at d=2. **Beyond-max n=6/7/8 is at chance (0.0000) in all four
   scratchpad arms** — the task-remodeling lever, NET-21's top surviving
   candidate, is CLOSED.
2. **NEW — GIVEN-CARRIES-STILL-FAIL (the strongest wall diagnostic).** Feeding
   the TRUE carries for n=6/7/8 still yields 0.0000 answers, at both depths. The
   wall is NOT "the model can't propagate carries" — a model that knows every
   carry exactly still cannot compute the n+1-digit answer. The wall is a
   position-specific ANSWER-COMPUTATION property of the fixed-depth answer
   function; the credit-assignment account of the wall is REFUTED.
3. **NEW — SCRATCHPAD-COLLAPSE-IS-DEPTH-CONDITIONED.** Scratchpad n=5 mastery is
   UNSTABLE at both depths, but the terminal state is depth-dependent: at d=1
   both seeds collapse PERMANENTLY from 1.0000 into carry-dissociation plateaus
   (full≈0.25 / 0.74, carries still known, answer chain failed — the correlated-
   error signature of NET-4/5/19/21); at d=2 both seeds survive collapse
   episodes (dip to 0.80; crash to 0.041) and RECOVER to stable 1.0000. The
   plain d=1 control's mastery is rock-stable — the instability is specific to
   the scratchpad objective. The mirror-image of NET-19's stochastic ESCAPE
   (dissociation→mastery): here mastery→dissociation→(d=2 only) re-mastery.
4. **Scratchpad aids IN-RANGE, not BEYOND-range.** At d=2 the plain control
   stuck in dissociation (full=0.10), while BOTH scratchpad seeds mastered n=5
   (1.0000) — the per-column targets rescue in-range credit assignment, and
   leave the beyond-range answer function untouched. The cleanest possible
   split between the two regimes.
5. **The mechanism is now positional expressivity, not credit.** Six angles all
   negative for length-gen: depth (NET-4/5/19), scale (NET-19), schedule
   (NET-21), task-remodeling (this round). The surviving levers change the
   REPRESENTATION: recurrence (stateful carry cell — length-general state), RoPE
   / position encoding (removes the shared pos-emb extrapolation caveat: train
   sees positions 0..24, beyond-max evals use up to 36), or a length-parameterized
   readout.

**LAW:** SCRATCHPAD-DOES-NOT-UNLOCK-LENGTH-GEN + GIVEN-CARRIES-STILL-FAIL +
SCRATCHPAD-COLLAPSE-IS-DEPTH-CONDITIONED. The carry chain is now characterized
on depth, scale, schedule, AND task-remodeling — all negative for length-general
composition. 2 seeds per depth in the scratchpad arm (1 seed per plain control);
the given-carries reading (0.0000) is the decisive isolation of the answer wall.

## What NET-23 established (performance axis — the position-representation test of the carry-chain length wall)

1. **RoPE does NOT unlock length-general carry.** The last surviving
   length-gen caveat was pos-emb EXTRAPOLATION: every prior eval used learned
   ABSOLUTE positions, so beyond-max positions 25..36 were UNTRAINED table
   entries. Replacing the pos table with RoPE (rotary q/k, no table, smooth
   extrapolatable positions — the scheme of essentially all modern LLMs) at
   d=1/dm=192/untied/bs=256/12000 steps, identical arch and budget (the `rope`
   flag is the only difference): n=6/7/8 full=0.0000 in both RoPE seeds. The
   in-range arm (s=0) masters n=5 cleanly (full=1.0000 by step 1000 — FASTER
   than the abs-pos control's st≈6000), so in-range competence is not the
   issue; the answer function still does not transfer.
2. **THE-POS-EMB-CAVEAT-IS-RETIRED.** This is the first length-gen eval in the
   program with NO position table. The wall reproduces with smooth,
   training-consistent, extrapolatable rotary positions ⇒ the length wall is a
   GENUINE fixed-depth expressivity limit, NOT an absolute-pos-extrapolation
   artifact. Every length-gen caveat from NET-22 is now closed: scratchpad
   (NET-22) and position encoding (this round).
3. **NEW — the final-carry MARGINAL transfers while the computation does not.**
   At n=6/7/8 the RoPE arm's MSB position scores 0.565–0.587 (≈ the
   P(carry-out≈1)≈0.5 prior over random n-digit operands) versus the abs-pos
   control's 0.11–0.31 (untrained entries fire wrong). RoPE's extrapolated
   positions carry training-consistent structure into the MSB slot, so the
   model applies its learned final-carry DISTRIBUTION — but still cannot
   COMPUTE the carry. Cleanest separation yet between statistical-prior
   transfer and algorithm transfer.
4. **NEW — ROPE-DISSOCIATION-IS-SEED-DEPENDENT, with a one-column shape.**
   Same hyperparameters: s=0 perfect by st=1000, s=1 permanently stuck in the
   carry-dissociation plateau (full=0.1040 / per=0.8507, flat st=5000–11000, no
   stochastic escape). The per-position shape is UNUSUAL: n=5 reads
   [0.107, 1.000, 1.000, 1.000, 1.000, 1.000] — interior + final-carry columns
   perfect, ONLY the LSB digit wrong. This is NOT NET-4/5's carry-cascade
   dissociation (wrong LSB carry → correlated errors downstream); the model
   reads carries correctly but the ones-column digit computation fails.
   Single-seed observation; mechanism open.

**LAW:** ROPE-DOES-NOT-UNLOCK-LENGTH-GEN + THE-POS-EMB-CAVEAT-IS-RETIRED +
ROPE-DISSOCIATION-IS-SEED-DEPENDENT. The carry chain is now characterized on
FIVE axes — depth (NET-4/5/19), scale (NET-19), schedule (NET-21),
task-remodeling (NET-22), and position representation (this round) — all
negative for length-general composition. Surviving levers, down from NET-22's
three: recurrence / stateful carry cell, length-parameterized readout.

## What NET-24 established (performance axis — the recurrence test: FIRST POSITIVE CURE of the length wall)

1. **STATEFUL-CARRY-CELL-UNLOCKS-LENGTH-GEN — the first positive cure in the
   program.** Augmenting the walled NET-23 RoPE encoder (d=1, dm=192, causal,
   12000 steps — the config that produced 0.0000 beyond-max) with a length-
   general stateful answer cell (GRU carrying the carry in hidden state; per-
   column feature = concat(h[a_i], h[b_i]); digits read off the GRU) yields
   **full=1.0000 at n=5/6/7/8, both seeds** — zero errors on 18.4k fresh n=8
   digit predictions. The five-axis negative line is RESOLVED: the wall is the
   state-free, fixed-depth, position-parameterized feedforward answer function.
2. **THE-WALL-WAS-THE-ANSWER-FUNCTION, NOT THE ENCODER.** Byte-identical
   encoder, budget, causal mask; the readout's STATE is the only difference vs
   NET-23, and it flips beyond-max 0.0000 → 1.0000. NET-22's GIVEN-CARRIES-
   STILL-FAIL is explained: carries as INPUT tokens are useless to a state-free
   readout; the same carries as recurrent STATE are exactly the cure.
3. **THE-CURE-IS-POSITION-SCHEME-INDEPENDENT, but encoder feature quality still
   modulates it.** hybrid-abs (learned pos, untrained beyond-max entries) ALSO
   length-gens (n=8 full=0.9624) — far above the transformer's 0.0000 — with a
   uniform thin column-error tail (feature noise, not a structural wall). RoPE
   gives the clean 1.0000.
4. **NEW — RAW-STATE-ALONE-HITS-A-STATE-HORIZON.** The textbook pure GRU (raw
   one-hot columns) masters n=5 (by step 2000), extends ~1–2 steps (n=6 full
   0.998–1.000, n=7 0.70–0.99) but degrades at n=8 (0.08–0.70, seed-dependent):
   the carry TRANSITION is length-general (final-carry 0.90–0.99 at n=8) but
   the digit READOUT misfires past the training unroll. The cure needs state
   AND the encoder's content-rich column features. Capacity caveat: 125k vs
   782k params (flagged).

**LAW:** STATEFUL-CARRY-CELL-UNLOCKS-LENGTH-GEN + THE-WALL-WAS-THE-ANSWER-
FUNCTION + THE-CURE-IS-POSITION-SCHEME-INDEPENDENT + RAW-STATE-ALONE-HITS-A-
STATE-HORIZON. The carry-chain wall is a state-free answer-function limit; a
length-general stateful answer cell over the walled encoder's features is the
cure (0→1, seed-independent). Depth, scale, schedule, scratchpad, and position
scheme are each individually insufficient — state is the load-bearing device.
Caveats: hybrid-abs 1 seed; pure-GRU capacity confound; 2 hybrid seeds.

## What NET-25 established (performance axis — mechanism dissection of the NET-24 cure: the lever is the dense final step)

1. **DENSE-FINAL-STEP-IS-THE-CURE — the NET-24 cure was the final-carry (EOS)
   input richness, NOT the encoder's features.** Same-seed, identical-weights
   control (pad384 vs pad384-zeroEOS: construction order matches, only the EOS
   parameter count differs): a dense 384-d learned EOS gives n=8 full=1.0000
   (4/4 seeds) while a 20-d EOS gives 0.026–0.744 (0/2, inside the raw20
   distribution). The EOS input dimension ALONE flips the cure. NET-24's
   "content-rich column features" interpretation is corrected.
2. **THE DIGIT-PATH CAN BE RAW.** pad384's digit columns are functionally raw
   20-d one-hots (364 dead padding dims) and it still cures 4/4; proj384
   (untrained fixed random 384-d projection, no context/position/learning)
   cures 5/5. The dense EOS is sufficient alone — no encoder, no learned
   features, no position required. The NET-24 pure-GRU failure was its 20-d
   EOS, not its digit inputs.
3. **THE RAW20 STATE-HORIZON IS REAL BUT SEED-VARIANCE-HEAVY (0/7 at 1.0).**
   n=8 full over 7 seeds: 0.0806, 0.6997, 0.0103, 0.0063, 0.0093, 0.0020,
   0.0132 — wide distribution, mode ~0.01, never 1.0. NET-24's 2-seed law
   (0.08/0.70) undersampled; the qualitative conclusion holds at 0/7.
4. **EOS RICHNESS NEEDS DIM ≫ DIGIT COUNT.** pos28's learned 28-d EOS still
   fails (0.0049, both seeds) — the effect is not "any trained EOS"; 384-d
   works, 20/28-d fail (threshold 28–384 untested).
5. **H1 CAPACITY and H3 POSITION REFUTED.** cap384-raw (471k params, raw
   one-hots) fails like the 125k pure GRU (0.006–0.008); one-hots + an 8-d
   RoPE-schedule step sinusoid add nothing (0.0049). Capacity of the cell and
   position structure in the digit path are not the levers.

**LAW:** DENSE-FINAL-STEP-IS-THE-CURE — THE-STATEFUL-CARRY-CELL-CURE-IS-THE-
FINAL-STEP-INPUT-RICHNESS; THE-ENCODER'S-CONTENT-WAS-NOT-THE-LOAD-BEARING-
INGREDIENT. The NET-24 cure decomposes: state (GRU) + a dense learned final-step
input. The carry TRANSITION was always length-general (final-carry 0.86–0.99
even in failing arms); the dense EOS is what keeps the digit readout
in-distribution at deep unrolls (hypothesis: boundary-step backprop conditioning
— flagged, unproven). Threshold (28–384) and the real-LM transfer of the
dense-EOS law are the open questions. Paper 69, issue #120.

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
- **The carry chain at scale — the length wall is SOLVED at the toy level
  (NET-24): the cure is a stateful answer cell, and the frontier is now
  real-scale transfer.** NET-4/5/19/21/22/23 showed the wall is immune to
  width/depth/readout, scale (dm=192, 18× params), schedule
  (curriculum/mixing), task-remodeling (scratchpad carry targets;
  given-correct-carries still fails ⇒ answer-computation, not credit), and
  position scheme (RoPE: no table, smooth positions — n=6/7/8 still 0.0000).
  NET-24 resolves the five-axis negative line: adding a length-general
  STATEFUL answer cell (GRU carrying the carry in hidden state) over the walled
  RoPE encoder's per-column features yields full=1.0000 at n=5/6/7/8, both
  seeds (0→1; the readout's state is the ONLY difference from NET-23's 0.0000).
  The wall was the state-free feedforward answer function; carries as recurrent
  STATE work where carries as input tokens (NET-22) failed. Pure recurrence on
  raw digits alone hits a state-horizon (n=8 full 0.002–0.70 over 7 seeds,
  seed-variance-heavy, 0/7 at 1.0). **NET-25 dissected the cure: the lever is
  the DENSE FINAL (EOS) STEP, not the encoder's content** — an airtight
  same-seed identical-weights control (pad384 vs pad384-zeroEOS, only the EOS
  input dimension differs) flips n=8 full 0.026–0.744 → 1.0000 (4/4); the digit
  path can be raw one-hots (pad384 cures with dead padding), so no encoder,
  learned features, context, or position is required (proj384 untrained random
  projection 5/5). The frontier is the real-scale question: does a
  recurrence/state-space-augmented answer path with a RICH boundary input give
  a real causal LM length-general computation the way it does here?
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

- NET-26 corrected NET-25's EOS-width law with a 30-arm round: the flagged
  "28–384 threshold" resolved as NO threshold — every width ≥28 cured 20/20
  (E=28,64,96,128,192,256,384 ×2 + E384×6) — while the fragility actually sits
  BELOW 28, at E=20, where a 12-sample distribution gives P(clean cure)≈¼
  {0.999×3, 0.744, 0.124, 0.058, 0.031, 0.026, 0.017, 0.011, 0.006, 0.005}.
  NET-25's two "evidence" pillars both fell: "28-d fails" (pos28) was a
  GRUCell(28)-architecture artifact, and "20-d fails 0/2" was a 2-sample draw
  from P(cure|E=20)≈¼. The "airtight same-weights control" was invalid
  (construction-order RNG — pad384 after-seed, pad384-zeroEOS before-seed drew
  different init streams) but immaterial (a construction-order verify showed
  both timings near-cure 0.9990 at s0). The controlling variable is
  representational DISTINCTNESS, not width: E=20's EOS occupies exactly the
  digit subspace (no exclusive dims) → boundary ambiguous → seed-fragile; E≥28
  adds exclusive dims → robust. Mechanism (dense boundary input keeps the
  hidden state in-distribution at depth — probe: flat norm + maxconf 1.000 vs
  drift + dips) SURVIVES. Net correction: EOS-width is a one-sided P(cure)
  distribution shift, not a sharp threshold; do not cite NET-25's pad control
  as airtight, and do not claim any single-seed EOS-width "threshold".

- NET-27 filled NET-26's open gap — the shape of the EOS-width P(cure) shift
  inside (20,28) — with 24 FRESH-seed arms (E ∈ {21,22,24,28} × seeds 8–13,
  byte-identical EOSWidthGRU; every sample an independent draw). Result: the
  shift is a MONOTONE RAMP, no sharp critical width, and the first exclusive
  dim is NOT sufficient. Failure mass vs E: 75% (E=20) → 67% (E=21) → 17%
  (E=22, worst case a near-cure 0.948) → 0 (E=24) → 0 (E≥28). Worst case n=8
  full: 0.005 → 0.157 → 0.948 → 1.0000 → 1.0000; medians 0.044 → 0.83 → 1.0 →
  1.0 → 1.0. E=21 (k=1 exclusive dim) is the only width with both a full cure
  (1.0000) and a hard failure (0.1567) among fresh draws — the exclusive-dim
  benefit is SUBLINEAR, a reliability curve (optimization-fragile boundary),
  not a capacity cliff. Failure mechanism is width-independent (same
  progressive-unroll collapse + same probe signature: ‖h‖ drift + maxconf dips
  at beyond-training cols). E≥28 merged is now 26/26 clean cures. Refines
  NET-26's distinctness law: the boundary token needs its own parameter
  subspace with ≥4 exclusive dims (k=2 near-robust, k=1 fragile); "any
  exclusive dim suffices" is REFUTED. Honest limit: n=6/width makes the
  E21→E22 P-jump alone not significant (Fisher ≈0.24); the law rests on the
  monotone ordering + merged anchors.

- NET-28 closed NET-27's two open threads in 18 arms (ALL_DONE_NET28,
  /tmp/exp_net_eos_knee.py): (1) the KNEE inside (21,24) — Part A, E=23 (k=3)
  and E=25 (k=5) × seeds 8–13, seed-paired with NET-27 (width the only
  variable): both 6/6 clean cures → P(cure) first reaches 100% at k=3 (E=23),
  refined from NET-27's "E=24 is the current first all-cure width"; full
  merged ramp k=0 → 25%, k=1 → 17–33%, k=2 → 83%, k=3+ → 100% (E≥28 now
  26/26). (2) The k=1 MECHANISM — Part B, E=21 × 6 FRESH seeds (14–19), each
  printing the trained EOS exclusive coordinate eos[20]: pinned at |0.67–0.91|
  in ALL outcomes (cure +0.778, near-cure −0.912, fails −0.672/+0.812,
  partials +0.771/+0.846) → the coordinate-dropout mechanism (Prediction A,
  "optimizer drops the exclusive dim → silent E=20 fallback") is REFUTED; the
  boundary signal is always present and the k=1 fragility is DOWNSTREAM in the
  recurrent dynamics (one boundary direction is a thin lever for shaping a
  192-dim hidden-state trajectory at depth; k≥3 gives independent directions
  → robust). Exclusivity ratio leans the same way (fails 1.30/1.78 vs cures
  1.73/2.24) but overlaps at n=6 — flagged, not asserted. Redundancy: every
  k=3/5 cure pins ALL exclusive coords (|0.46–0.66|), dominant over digit
  subspace (0.24–0.48) — exclusive capacity is load-bearing, not idle. Design
  rule sharpens to ≥3 exclusive dims (k=3 6/6, k=2 5/6 near-robust, k=1
  17–33%). Pooled E=21 = 12 samples, P(≥0.99) 2/12, median ≈0.68.

- NET-29 ran the causal test NET-28's open (1) demanded — 12 SAME-SEED
  reproductions of NET-28 arms (exclusive coords reproduce to 3 decimals; ctl
  re-baselines reproduce NET-28 outcomes on fresh draws) with INFERENCE-ONLY
  interventions on the trained EOS exclusive coords. Part A (E=23 k=3 × seeds
  8–13, 7 interventions/arm): zeroing the ENTIRE exclusive block at eval leaves
  the cure intact in 5/6 arms (n=8 full {1.0000, 0.9995, 0.9995, 1.0000,
  0.9971}) — ≤0.3% scattered, never a collapse — and costs 0.70 in 1/6 (s=13,
  a MAGNITUDE-ENSEMBLE: zero1→1.0000, scale0.1→0.9692, flip→no-op; the arm
  with the largest coords |0.65–0.66|); zeroing ANY SINGLE coord costs 0% in
  all 6; signs never matter. Part B (E=21 k=1 × seeds 14–19): zeroing the SOLE
  exclusive coord costs real accuracy at the cures (s=14 −2.8% ~3 SE; s=15 −1
  to −5% at short/mid lengths) and is a NO-OP at the partials/fails (all
  |Δ| ≤ 1.2 SE) — eval-load-bearingness ∝ cure quality, causally confirming
  NET-28's downstream-fragility (removal is free exactly where the model
  already failed). LAW: THE-EXCLUSIVE-BOUNDARY-CHANNEL-IS-TRAINING-TIME-
  LOAD-BEARING — at k=3 the trained recovery is (mostly) self-sufficient
  (BPTT shapes the weights using the exclusive teacher signal; inference need
  not re-serve it), internalization is seed-heterogeneous (5/6 vs 1/6), and
  the k=3 rule is a TRAINING-TIME rule. Barrier (e) is the round's content
  (seed heterogeneity reported as a distribution, byte-identical same-seed
  reproductions). Open: k=2 freeze test (is E=22 internalization intermediate
  → links the gradient to the ramp); magnitude→dependence trend; REAL-SCALE
  transfer of the training-time rule; pad384-hybrid parity.
- NET-30 (issue #125): INTERNALIZATION-SATURATES-AT-K=2 — the k=2 (E=22) freeze
  test completes the eval-dependence gradient (12 same-seed reproductions of
  NET-27 arms, inference-only, ALL_DONE_NET30). k=2 is NOT intermediate: zeroing
  the entire exclusive block at eval costs ≤0.010 in 5/6 arms (two largest
  changes POSITIVE) — indistinguishable from k=3's 5/6; NET-28's P(cure) ramp is
  a training-time success-rate effect only (eval-sufficiency saturates at k=2).
  s=13 is a SEED-WIDE outlier at both k=2 and k=3 (largest exclusive coords at
  both widths, 0.701 vs ≤0.660) but its structure is width-conditional: at k=3
  sign-insensitive 2-of-3-redundant (flip no-op), at k=2 sign-sensitive
  2-of-2-redundant (flip −0.25) — NET-29's 'signs never matter' was a k=3
  statement. HONEST CORRECTION: NET-29's 'k=1 internalization ∝ cure quality'
  is REFUTED at a second seed set — both fresh k=1 full cures (s=8, s=12) are
  self-sufficient (zero1 = 0% cost); pooled over 12 k=1 arms, fails are no-ops
  in EVERY arm of both rounds and successes split seed-heterogeneously.
  Self-sufficiency rate rises with k: k=1 ~1/2, k≥2 5/6. Design rule sharpens
  to ≥2 exclusive dims for a self-sufficient recovery, ≥3 for reliable success.
- NET-31 (issue #138): INTERNALIZATION-IS-A-SEED-FIXED-TRAIT-AMONG-CURES +
  NET-29's "5/6 SELF-SUFFICIENT AT k=3" WAS A SEED-SET-SPECIFIC HIGH +
  THE-DEPENDENT-SEEDS-STAY-DEPENDENT-AT-EVERY-WIDTH — the seed-trait-vs-width-
  trait test (12 SEED-FIXED WIDTH-SWEPT arms, ALL_DONE_NET31: E=23 k=3 and E=22
  k=2 × seeds 14–19, same seeds as the published E=21 arms = the k=1 rung, so
  every seed 14–19 now has k=1/2/3 internalization reads). The boundary-
  dependence set is the SAME at k=2 and k=3: {13, 14, 15, 17} (k=3 zeroN 0.9014/
  0.7104/0.7437, k=2 0.9141/0.8037/0.9067; s=13 from NET-29/30 0.7041/0.7544);
  the same seven seeds are self-sufficient at both widths ⇒ internalization is
  ~60/40 and WIDTH-INDEPENDENT (width sets P(cure), the seed sets internalization).
  HONEST CORRECTION: NET-29's 5/6 and NET-30's "k≥2 5/6" were seed-set-specific
  highs — pooled k=3 (seeds 8–19) is 7/12 self-sufficient/marginal, ~40%
  dependent. SEED-TRAIT CONFIRMED for the k=1-dependent seeds (s=14: −2.8% →
  −9% → −10% as k goes 1→2→3; s=15: −1…−5% → −20% → −29% — dependence GROWS
  with k), WIDTH-TRAIT REFUTED, but the trait has NO k=1 predictor (s=13 fail-
  no-op and s=17 partial-no-op are dependent at k≥2; s=16/18 fail-no-ops are
  self-sufficient). NEW k=2 sign-sensitivity marker: flip cost ≠ 0 ⟺ dependent
  (4/4 dependent k=2 arms −7 to −25%, require sign-opposition; self-sufficient
  k=2 arms flip-free; k=3 flip = 0% in all 12 arms both seed sets). NET-29's
  magnitude→dependence hint REFUTED (self-sufficient s=18 has larger coords than
  dependent s=14/17). P(cure)=100% at k=3 extends to a SECOND seed set (12/12
  merged). Mechanism: at k≥2 the block is used COLLECTIVELY (zero1 = 0% in every
  arm); dependent seeds gate on the aggregate block norm. Design rule sharpened:
  ≥3 exclusive dims ⇒ reliable training SUCCESS (12/12), but ~40% of seeds remain
  eval-dependent on the boundary ensemble — keep re-serving the boundary token or
  verify per instance. Barrier (e) is the round's content (seed-set-
  heterogeneous rate reported pooled; the same-4-seeds trait is a within-seed-
  across-width reproducibility statement). Open: REAL-SCALE transfer (frontier);
  a trained-WEIGHT predictor of the seed trait; pad384-hybrid parity; why
  dependence grows with k.
- NET-32 (issue #139): THE-INTERNALIZATION-TRAIT-IS-A-TRAINING-ARTIFACT +
  NOT-SEED-INTRINSIC — a NO-BOUNDARY final fine-tune converts 4/4 known-dependent
  seeds to self-sufficient (the constructive test NET-31's "seed-fixed trait"
  demanded). 6 arms at E=23 (k=3), byte-identical EOSWidthGRU: the COMPLETE known-
  dependent population {13,14,15,17} + self-sufficient controls {16,18}
  (ALL_DONE_NET32). Each arm: standard 12000-step training → stage-0 ctl+zeroN
  (EXACT same-seed replication: zeroN {0.7041, 0.9014, 0.7104, 0.9932, 0.7437,
  0.9995} = NET-29/30/31 to 4 decimals) → fine-tune T∈{300,1000,3000} with the
  exclusive block ZEROED at the EOS step (the zeroN eval condition made a TRAINING
  condition). CONVERSION: zeroN n=8 goes {0.7041, 0.9014, 0.7104, 0.7437} → 1.0000
  for all four dependent seeds in ≤3000 steps (≤2.5% of the training budget) —
  the trait is a property of the converged SOLUTION, not the seed's landscape;
  INTRINSIC-TRAIT REFUTED. Fast onset (≥0.99 at T=300 in 5/6) but NON-MONOTONE in
  4/6 arms (transient n=8 reorganization dip — s=13 T=1000 0.9746, s=15 0.9390,
  s=16 T=300/1000 0.7163/0.6763, s=18 0.9150 — always recovering by T=3000; deploy
  only at full convergence). Cure preserved (ctl ends 1.0000 in 6/6). Post-
  conversion the block is INERT: ctl/zeroN/zero1@0/flip1@0/scale0.1 all 1.0000 at
  n=8 in all six arms — decisive because zero1 was 0% in EVERY trained k≥2 arm,
  so the trained block-gated path is GONE (full switch, not compensation).
  HONEST CORRECTION (barrier f): the log's EOSCOORD-AFTER |0.06| was a scale0.1
  measurement artifact (buffer printed after the final scale0.1 eval — exactly
  ×0.10 in every arm); true post-fine-tune coords unmeasured, weight-decay-bounded
  at ~0.97× trained (~0.6) ⇒ mechanism is DYNAMIC STOP-ROUTING (block present at
  near-full magnitude but inert), not coord decay. Design rule UPGRADED: ≥3
  exclusive dims ⇒ reliable success (12/12 cures), then a ≤3000-step no-boundary
  final fine-tune makes the boundary block OPTIONAL seed-independently — the ~60%
  internalization lottery and the "re-serve or verify per instance" caveat are
  gone. Barrier (b) confronted: no-boundary fine-tuning is a known qualitative
  family; the exact T-law + dip + inertia + not-intrinsic reframing are novel
  (Catalog: pkg 693/35 certified adversarial robustness, orthogonal). Open:
  REAL-SCALE transfer (now with a concrete protocol); clean post-fine-tune coord
  readout (confirm stop-routing); dip distribution; minimal conversion budget at
  k=2; pad384-hybrid parity.
- NET-33 (issue #140): THE-ATTENTION-COST-LAW-IS-SEED-ROBUST — the barrier-(e)
  check exactly requested by NET-20's declared gap ("a seed-1 ctx=256 re-run
  would strengthen"). Byte-identical harness to NET-15/20 (CausalTF d=4, dm=64,
  4 heads, Gutenberg corpus, 2000 AdamW steps) at **seed=1**, at BOTH ctx=128
  and ctx=256 (ALL_DONE_NET33). k* is EXACT at the second seed: k*(s1,128)=16
  (k=8 0.973 ✗, k=16 0.987 ✓) and k*(s1,256)=32 (k=16 0.973 ✗, k=32 0.990 ✓) —
  matching s0 (16/32) and the prediction d·ctx/32 stated before the run ⇒ the
  ∝-ctx proportionality is NOT a single-seed artifact. The knee is if anything
  MORE favorable at s1 (retained@k* 0.987/0.990 vs 0.984/0.989; cleaner
  fail/pass margin at ctx=128). Concentration reproduces to ≤3% relative (eff
  support 46.41 vs 46.63 @128, 80.57 vs 82.94 @256; top-k masses within 0.009;
  per-position monotone no-bounded-working-set shape preserved: 11.12/70.08/
  150.44 vs 11.27/72.25/155.35 @256). Random-k selection gap is seed-stable
  (within 0.5 pts at every comparable (k, ctx): +6.1/+8.3/+6.3 vs s0's
  +6.2/+8.7/+6.0). Full-acc spread across the 4 (seed × ctx) models is
  0.1571–0.1612 (±0.4% of mean) and does not shift k*. Barrier (e) CLEARED at
  d=4 for the ∝-ctx leg; the diffuse-but-prunable structure is a property of
  the task/data scale, not of one run. Honest remaining limit: the DEPTH leg
  (k*=4d at d=8/16, NET-16/17) is still single-seed; k* exact at the sweep's
  k-resolution. Open: d=8/16 seed-1 depth-leg points; a ctx=512 point.

- **NET-34 (issue #141) — THE-DEPTH-LEG-OF-THE-ATTENTION-COST-LAW-IS-SEED-ROBUST:
  k*=d·ctx/32 holds at a second seed in EVERY measured cell of the (d×ctx)
  grid.** The barrier-(e) limb NET-33 named open — the depth leg k*=4d at
  d=8/16 rests on seed-0 alone. CausalTF **d=8, seed=1** at BOTH ctx=128 and
  ctx=256 (byte-identical harness, 2000 steps; ALL_DONE_NET34). Prediction
  stated before the run: k*=32 @ 128 (4d) and k*=64 @ 256 (d·ctx/32 = 8·256/32,
  a NEVER-MEASURED grid cell). Both land EXACT: k*(s1, ctx=128) = 32 (k=16 0.962
  ✗, k=32 0.988 ✓ — identical to s0's 32, NET-16) and k*(s1, ctx=256) = 64
  (k=32 0.968 ✗, k=64 0.990 ✓, margin 0.010 — same margin as every prior pass).
  k=192 recovers full loss exactly (5.0868 vs 5.0865). Concentration reproduces
  to ≤0.003 at ctx=128 (eff support 50.16 vs s0 50.13; top-k masses identical
  to 0.001); the context-diffusion law extends to depth (eff 50.16 → 91.49 as
  ctx doubles, 1.82× vs d=4's 1.78×); per-position monotone no-bounded-
  working-set shape preserved. Selection importance survives depth AND seed
  (random-k gaps 4.5–8.0 pts at d=8 vs 6.0–8.7 at d=4). Full-acc spread across
  all six (seed × depth × ctx) models 0.1571–0.1620. Barrier (e) CLEARED for
  the depth leg at d=8 — the last single-seed limb of the attention-cost law is
  closed (the law holds at a second seed in every measured grid cell; the
  deployable claim — speedup 32/d = 8× at d=4, 4× at d=8, context-invariant in
  [128, 256] at both depths — can be shipped without per-instance re-measurement).
  Honest remaining single-seed: d=16 (NET-17) at ctx=128, and no ctx=512 point
  exists. Open: d=16 second-seed point; a ctx=512 point.

- **NET-35 (issue #142) — THE-ATTENTION-COST-LAW-EXTRAPOLATES-TO-4×-CONTEXT:
  k*=d·ctx/32 holds at ctx=512 (k*=64, the law's first point outside [128,256]).**
  The context leg of the law rested on exactly ONE doubling (128→256); the whole
  ctx=512 regime was unmeasured. CausalTF **d=4, seed=1, ctx=512** (byte-identical
  harness, 2000 steps, 2854s train; ALL_DONE_NET35). Prediction stated before the
  run: k* = 64 (d·ctx/32 = 4·512/32). EXACT: k=16 0.940 ✗, k=32 0.964 ✗, k=64
  **0.983 ✓** (k=128 0.992, k=256 0.999, k=384 1.000 — loss 5.0827 = full
  exactly) ⇒ the law holds across a 4× context range at a second seed and the
  lever speedup = 32/d = 8× at d=4 is context-invariant over the quadrupled range
  (NET-20's core claim, now tested to 512 — longer context still buys no extra
  relative saving). NEW P3 CAVEAT (long-context margin erosion): the k* pass
  clears the bar by only 0.003 (≈2 SE) vs ~0.007–0.010 at 128/256, and retained
  is uniformly ~0.01 lower at every k — the law's KNEE stays exact but its margin
  erodes with context (re-check at ctx=1024). Concentration diffusion continues
  (eff support 152.11; 46.4 → 80.6 → 152.1 across doublings, ×1.74/×1.89 —
  slightly superlinear on the third); per-position eff 20.41/133.37/281.20 — NO
  bounded working set at 512. Selection importance survives the longest context
  (random-k gaps +5.3/+4.6 vs 6.0–8.7 at 128/256). Seven-model full-acc set
  0.1571–0.1616, k*-irrelevant. Barrier (e): the extrapolation cell is EXACT but
  SINGLE-SEED — no ctx=512 second seed, no depth sweep there. Honest remaining
  single-seed: d=16 @ ctx=128 (NET-17), ctx=512 at d=8/16, and no ctx=1024 point.
  Open: ctx=512 second seed; ctx=1024 (margin-erosion check); d=16 second seed;
  carry chain at scale (the frontier).
- **NET-36 (issue #143) — THE-ATTENTION-COST-GRID-IS-NOW-TWO-SEED-EVERYWHERE:
  k*=d·ctx/32 holds at every measured (depth × context) cell.**
  The grid's two LAST single-seed corners — d=16 @ ctx=128 (NET-17, s0 only)
  and ctx=512 @ d=4 (NET-35, s1 only) — both predicted k*=64 (4d and d·ctx/32).
  CausalTF **d=16 seed=1 ctx=128 AND d=4 seed=2 ctx=512** (byte-identical harness,
  2000 steps each; ALL_DONE_NET36). Predictions stated before the run: k* = 64
  both. EXACT BOTH: cell A k=32 0.970 ✗, k=64 **0.996 ✓** (loss 5.0827 = full);
  cell B k=16 0.965 ✗, k=32 0.976 ✗, k=64 **0.985 ✓** (k=384 loss 5.0803 = full
  exactly) ⇒ the depth leg k*=4d now holds at ALL THREE depths × two seeds
  (16/32/64 at d=4/8/16 @ ctx=128), and the context leg holds to 4× context at
  two seeds (64 @ ctx=512 d=4 s1+s2) — EVERY measured cell is two-seed, the
  deployable lever 32/d (8× at d=4) is seed-independent at every corner. P3
  REFINEMENT — NET-35's long-context margin erosion (s1 pass 0.983, margin 0.003)
  does NOT reproduce at s2 (pass **0.985**, margin 0.005 — healthy): margin is
  seed-fluctuating ±0.002 at 512, retained curve still ~0.005–0.01 below 128/256
  at both seeds, knee unaffected (re-check at ctx=1024). Concentration reproduces
  to three sig figs (eff support **152.11 = 152.11** both seeds; top-32 0.533/0.532;
  eff by pos 20.41–20.45 / 133.23–133.37 / 281.20–281.46); depth-drift continues
  (eff 52.73 at d=16, 46.6→50.2→52.7). Selection gaps at fresh seeds +10.0/+6.0
  (d=16) and +7.6/+5.2 (ctx=512). Eight-model full-acc set 0.1571–0.1620.
  Barrier (e): this round closed the grid's last two single-seed cells; honest
  remaining non-threatening: ctx=512 at d=8/16 (unmeasured), d=8 @ ctx=256 s0
  corner, ctx=1024 margin re-check.
  Open: ctx=1024 (margin-erosion check); ctx=512 at d=8/16; d=8 @ ctx=256 s0
  corner; carry chain at scale (the frontier).
- **NET-37 (issue #144) — THE-ATTENTION-COST-LAW'S-KNEE-SURVIVES-8×-CONTEXT:
  k*=d·ctx/32 holds at ctx=1024 AND the margin-erosion caveat is RESOLVED.**
  The P3 caveat NET-35 flagged (ctx=512 pass margin 0.003 ≈ 2 SE) demanded a
  re-check at 1024 — the retained-curve depression extrapolates to ~0.97–0.98
  there, right at the bar. CausalTF **d=4, seed=1, ctx=1024** (byte-identical
  harness, 2000 steps, 5516s train; 585 windows, 10% held out; ALL_DONE_NET37,
  /tmp/exp_net_attncost_ctx1024.py). Prediction stated before the run: k* = 128
  (d·ctx/32 = 4·1024/32). EXACT — P1 OUTCOME: k=32 0.945 ✗, k=64 0.968 ✗, k=96
  0.977 ✗, k=128 **0.986 ✓** (k=192 0.991, k=256 0.993, k=384 0.996, k=512 1.000
  [re-norm MC saturation], k=768 0.999) ⇒ the law k* = d·ctx/32 holds at a fixed
  seed across an **8× context range (128 → 1024)**, every doubling exact, no
  ceiling. **MARGIN-EROSION REFUTED**: the pass margin chain at d=4 s1 across
  contexts is **+0.007 (128) / +0.010 (256) / +0.003 (512) / +0.006 (1024)** —
  NOT monotonic, the 512 dip was a fluctuation and the margin RECOVERED at 1024;
  the knee is exact at every doubling, the retained curve is still somewhat lower
  at longest context but the knee is unaffected. Concentration diffusion
  continues superlinearly — eff support **291.16** (46.4 → 80.6 → 152.1 → 291.2,
  ×1.74/×1.89/×1.91); per-position eff 37.56/255.76/542.05 — NO bounded working
  set at 1024; top-128 mass 0.702. Selection importance survives — random-k gaps
  +5.9 (k=64) / +4.6 (k=128). Nine-model full-acc set 0.1571–0.1620 (0.1594 at
  1024), k*-irrelevant. Barrier (e): the margin question answered by the
  FOUR-point same-seed chain (the 512 dip shown to be a fluctuation); honest
  limit — the ctx=1024 cell is single-seed and the knee fluctuation band (±0.003)
  is wider at long context than at 128/256.
  Open: ctx=1024 second seed; ctx=512 at d=8/16; d=8 @ ctx=256 s0 corner; carry
  chain at scale (the frontier).
- **NET-38 (issue #145) — PRODUCT-FORM-CONFIRMED-DEPTH-LEG-SUB-LINEAR-AT-LONG-
  CONTEXT: the attention-cost law's first discriminating corner (d=8, ctx=512),
  where 4d=32, ctx/8=64, and d·ctx/32=128 ALL disagree — and the knee lands at
  NONE of them.** The first cell where the exact k* deviates from d·ctx/32, in the
  SAFE direction. CausalTF **d=8, seed=1, ctx=512** (byte-identical harness, 2000
  steps, 3889s train; 1171 windows, 10% held out; ALL_DONE_NET38,
  /tmp/exp_net_attncost_d8_ctx512.py). Prediction stated before the run: k* = 128
  (d·ctx/32 = 8·512/32). Measured **k* = 96**: k=16 0.915 ✗, k=32 0.952 ✗ (4d —
  depth-only rule REFUTED by 18 SE), k=64 0.979 ✗ (ctx/8 — context-only rule
  marginal, ~1 SE below bar), k=96 **0.990 ✓**, k=128 0.995 ✓ (d·ctx/32 passes
  but is NOT minimal), k=192 0.995, k=256 0.999, k=384 0.998 (loss 5.1356 ≈ full
  5.1355). ⇒ the single-lever rules are REFUTED — depth demonstrably raises the
  required k above the d=4 context-only value (64): the levers act
  MULTIPLICATIVELY — but the exact product value 128 is not the minimum: the law
  is a **proven-safe upper bound** at high (depth × context), over-pruneable
  never under. **SUB-LINEAR DEPTH LEG AT LONG CONTEXT**: at ctx=512, doubling d
  (4→8) raises k* 64→96 = ×1.5, not the ×2.0 linear law (which held exactly at
  ctx=128 across d=4/8/16) — the retrieval load is shared across the deeper stack
  at long context; cross-depth retained shift confirms direction robustly (k=64:
  0.983/0.985 d=4 two seeds → 0.979 d=8, ≈3 SE). Deployable claim intact with
  margin: ≥4× speedup at d=8 guaranteed, **5.3× actually available** (512/96).
  Concentration keeps diffusing superlinearly — eff support **177.80** (d=8:
  50.16 @128 → 91.49 @256 → 177.80 @512, ×1.82/×1.94; 152.11 d=4 ctx=512 → 177.80
  d=8, mild depth spread); top-64 0.634, top-128 0.806; per-position eff
  23.09/156.01/332.15 — NO bounded working set. Selection importance survives —
  random-k gaps +6.4 (k=64) / +3.7 (k=128). Barrier (e): the round's honest limit
  — the cell is single-seed AND the knee is soft (k=64 ~1 SE below bar; a
  re-measure could read 64), so the ROBUST claims are the single-lever refutation
  (k=32, −18 SE) and the depth right-shift of the retained curve (≈3 SE), NOT the
  exact coefficient; the sub-linear-depth claim needs a second seed at this
  corner (the immediate next round).
  Open: **d=8 ctx=512 second seed (sub-linear depth leg — highest value)**;
  ctx=1024 second seed; ctx=512 at d=16; d=8 @ ctx=256 s0 corner; carry chain at
  scale (the frontier).
- **NET-39 (issue #146) — SUB-LINEAR-DEPTH-LEG-CONFIRMED-AT-A-SECOND-SEED: the
  exact knee k*=96 reproduces at (d=8, ctx=512, seed=2), resolving NET-38's
  barrier-(e) honest limit (soft knee, single seed).** The second-seed check
  NET-38's paper explicitly demanded. CausalTF **d=8, seed=2, ctx=512**
  (byte-identical harness, 2000 steps, 4257s train; 1171 windows, 10% held out;
  ALL_DONE_NET39, /tmp/exp_net_attncost_d8_ctx512_s2.py). Prediction stated
  before the run: k* = 96 (reproducing s1). **EXACT — P1 OUTCOME: k=16 0.904 ✗,
  k=32 0.938 ✗ (4d — depth-only refuted even more decisively than s1's 0.952),
  k=64 0.973 ✗ (ctx/8 — refuted CLEANLY, 4.5 SE below bar, resolving the
  marginal-0.979 straddle), k=96 0.987 ✓, k=128 0.992 ✓ (safe but NOT minimal),
  k=192 0.999, k=256 1.001 [re-norm MC sat.], k=384 1.000 (loss 5.1504 ≈ full
  5.1499)** ⇒ k* = 96 = 96 at both seeds; the sub-linear depth leg at ctx=512 is
  a REAL two-seed property: at ctx=512 doubling d gives ×1.5 at BOTH seeds
  (k*=64,64 d=4 → 96,96 d=8) vs the ×2.0 linear exact at ctx=128 (all three
  depths, two seeds each). The law d·ctx/32 is confirmed a PROVEN-SAFE UPPER
  BOUND at long context — the actual knee is systematically below it, so
  deployments can prune MORE than the guarantee (**5.33× at d=8 ctx=512, not
  4×**). Concentration reproduces to ~2.5% (eff support 173.23 vs s1 177.80;
  top-64 0.645 vs 0.634, top-128 0.814 vs 0.806; per-position 22.33/151.63/
  326.05 vs 23.09/156.01/332.15 — NO bounded working set). Selection importance
  survives — random-k gaps +5.3 (k=64) / +5.0 (k=128), same family as s1's
  +6.4/+3.7. Barrier (e) clean this round — exact knee reproduces, soft-knee
  concern resolved (s2 k=64 −4.5 SE; crossing genuinely in (64, 96]), ×1.5
  coefficient two-seed at both depths; remaining single-seed/unmeasured:
  ctx=512 at d=16, ctx=1024, d=8 @ ctx=256 s0 corner.
  Open: **ctx=512 at d=16 — does the sub-linearity continue? predicts k*≈144 =
  ×1.5·96 if it does, vs 256 = d·ctx/32 if the law recovers (highest value)**;
  ctx=1024 second seed; d=8 @ ctx=256 s0 corner; carry chain at scale (the
  frontier).
- **NET-40 (issue #147) — DEPTH-LEG-IS-AFFINE-AT-LONG-CONTEXT: k\*=160 at (d=16,
  ctx=512), completing the exact three-point linear law k\* = 8d + 32.** The
  third rung of the ctx=512 depth ladder — the one cell that discriminates
  whether NET-38/39's ×1.5 sub-linear coefficient continues (k*≈144) or the law
  recovers (k*=256). CausalTF **d=16, seed=1, ctx=512** (byte-identical harness,
  2000 steps, 6472s train; 1171 windows, 10% held out; ALL_DONE_NET40,
  /tmp/exp_net_attncost_d16_ctx512.py). Enriched sweep {32,64,96,128,144,160,192,
  224,256,384} to pin the knee in [96,256]. Prediction stated before the run:
  k* = 144 (×1.5·96) if the sub-linearity persists; 256 = d·ctx/32 if the law
  recovers. **RESULT — k\* = 160, NEITHER horn: k=32 0.854 ✗, k=64 0.917 ✗ (4d —
  depth-only far short at depth), k=96 0.944 ✗ (d=8's knee fails ~4 SE at d=16 —
  depth right-shift confirmed), k=128 0.967 ✗, k=144 0.976 ✗ (×1.5·96 — P1
  REFUTED, 2.7 SE below bar), k=160 0.981 ✓, k=192 0.991 ✓, k=224 0.993 ✓, k=256
  0.993 ✓ (d·ctx/32 passes but is NOT minimal — 37.5% above the knee), k=384
  1.000 (loss 5.3172 ≈ full 5.3147)** ⇒ the depth ratio on doubling d=8→16 is
  ×1.67, not ×1.5 — the sub-linear coefficient is NOT a power law. All three
  ctx=512 points (64, 96, 160 for d=4, 8, 16) lie EXACTLY on the affine line
  **k\* = 8d + 32 = (ctx/64)·d + (ctx/16)** — slope HALF the small-context value
  (ctx/32=16 → ctx/64=8) plus a positive intercept (ctx/16=32); the ×1.5 of
  NET-38/39 was the first step (ratios ×1.5, ×1.67 — approaching ×2 as d grows).
  At ctx ≤ 256 the law is EXACT product (d=8 ctx=256: k*=64, not 96), so the
  crossover lies in (256, 512]. Deployable speedup at ctx=512: d=4 → **8.0×**,
  d=8 → **5.33×**, d=16 → **3.2×** (guarantee 4×/4×/2× — the law is a proven-safe
  upper bound, over-pruneable by up to 1.6×). Concentration: eff support 199.84
  (depth diffusion 152.11 → 177.80 → 199.84 across d=4/8/16, ×1.17/×1.12 per
  doubling); top-128 mass DROPS to 0.771 (vs 0.806/0.814 — the distribution
  spreads further); per-position 25.55/174.57/372.99 — NO bounded working set.
  Selection importance dilutes: random-k gaps +3.4 (k=128) / +2.3 (k=256), the
  SMALLEST of any cell. Barrier (e) is the round's honest limit — the d=16 cell
  is SINGLE-SEED with the SOFTEST knee of the series (k=144 fails 2.7 SE, k=160
  passes 0.7 SE), mitigated because the affine law rests on the three-depth SHAPE
  (d=4/d=8 rungs two-seed, all three points exactly on 8d+32) and the crossing is
  robustly in (144, 160].
  Open: **d=16 ctx=512 second seed (the affine law's third rung — highest
  value)**; ctx=1024 second seed; d=8 @ ctx=256 s0 corner; carry chain at scale
  (the frontier).
- **NET-41 — THE-AFFINE-LAW'S-THIRD-RUNG-IS-NOT-TWO-SEED-EXACT (speed; the affine
  third rung at a second seed, mirroring NET-38→39; ALL_DONE_NET41): at (d=16,
  ctx=512, seed=2) k* = **144** (s1 measured 160; predicted 160 = affine third
  rung) ⇒ **P2 — the affine third rung did NOT reproduce**; the s2 retained curve
  is shifted UP uniformly near the knee (k=128/144/160: 0.967/0.976/0.981 → s2
  0.980/0.986/0.987, all +0.006–0.013), so the s2 model's attention is slightly
  MORE prunable; k=128 is knife-edge (raw 0.9795 vs bar 0.98014, fail by 0.0006);
  the two-seed d=16 knee spans **(144, 160] — exactly bracketing the affine-law
  prediction (8d+32 = 160, matched by s1) and a concave power-law continuation
  (k* ≈ 28.3·d^0.585 ≈ 144, matched by s2)** ⇒ at two seeds the exact functional
  form at the deepest rung is UNDECIDED (NET-40's "exact three-point affine law"
  over-claimed: its third point was a single-seed soft-knee draw); the two forms
  differ by ~10% and both ≪ the guarantee, so the practical claim is unaffected.
  What SURVIVES at two seeds: (i) depth right-shift at d=16 (knee 144–160 vs d=8's
  96; s2 k=96 retained 0.963 below bar); (ii) proven-safe upper bound (256
  non-minimal by 1.6–1.78×; deployable speedup **3.2–3.56×** at d=16 ctx=512 vs
  the 2.0× guarantee); (iii) concentration reproducible to ≤0.5% (eff 198.78 vs
  199.84, top-128 0.773 vs 0.771, top-256 0.935 vs 0.934, per-position
  25.53/173.85/371.99 vs 25.55/174.57/372.99); (iv) selection importance survives
  (random-k gaps +6.0/+2.6, stronger than s1's +3.4/+2.3). Barrier (e) is the
  round's substance — the d=16 knee is seed-fluctuating (160/144, one grid step,
  flat-topped retained at both seeds), so affine-vs-power is UNDECIDED at two
  seeds; the affine law 8d+32 remains the best central tendency of the ctx=512
  ladder (64, 96, ~152) but is NOT exact at d=16.
  Open: **d=32 ctx=512 (the discriminating cell — affine predicts 288, concave
  power ≈213, product 512, a 35% separation; expensive ~3.5h but decisive)**;
  ctx=1024 second seed; d=8 @ ctx=256 s0 corner; carry chain at scale (the
  frontier).
- **NET-42 — DEPTH-LEG-AT-LONG-CONTEXT-IS-CONCAVE-POWER (speed; the DISCRIMINATING
  depth rung that resolves NET-40/41's affine-vs-power indecision; ALL_DONE
  sweep — KSTAR/ALL_DONE not printed due to documented crash): at (d=32, ctx=512,
  seed=1) k* = **256** (predicted 288 affine / ≈215 concave power / 512 product)
  ⇒ **NEITHER horn** — k=224 0.977 ✗ (knife-edge, fail by 0.003 ≈ 0.3 SE), k=256
  0.987 ✓, k=288 0.989 ✓ (8d+32 passes but is NOT minimal — over-predicts by
  11%), k=384 0.995 ✓, k=512 1.000 ✓ (loss 5.6281 = full exactly; the product
  form is refuted by 2×). The four ctx=512 rungs (64, 96, ~152, 256 for
  d=4/8/16/32) lie on a log-log regression **k\* ≈ 24.7·d^(2/3)** to ≤3%
  (62/99/157/249), the exponent ROBUST to the d=16 seed choice (0.666 with s2's
  144, 0.673 with s1's 160) ⇒ **the affine law 8d+32 — exact at d=4/8/16-s1 — was
  a 3-point LOCAL LINEAR approximation of this concave power curve and breaks at
  d=32**; the naive power fit of NET-40/41 (28.3·d^0.585) was biased by anchoring
  on the single noisy s2 d=16 reading. The sub-linear depth leg CONTINUES at every
  rung (per-doubling ratio 1.50 → 1.58 → 1.68, approaching but never reaching 2.0
  through d=32) — P3 (recovery at depth) refuted decisively (256 = exactly half of
  512). Deployable speedup at (d=32, ctx=512) = **2.0×** vs the 1.0× guarantee —
  the largest over-pruneable factor yet. Concentration depth-diffuses to eff
  218.46 (top-256 mass 0.921, top-384 0.986; per-position 27.81/190.90/409.08 —
  NO bounded working set). HONEST CRASH LOG: the k=768 sweep point threw
  `RuntimeError: selected index k out of range` (topk(768) on a 512-wide causal
  attention row — my sweep-design bug), aborting Part B2 (random-k control) and
  the KSTAR/ALL_DONE prints; the point was REDUNDANT (k=512 already = 1.000) so
  the k* verdict is unaffected, but the random-k control at (d=32, ctx=512) is
  UNMEASURED (standing evidence: selection gap positive in every prior cell,
  +2.3 to +11.7). Barrier (e) is the round's honest limit — the d=32 cell is
  SINGLE-SEED (every new rung starts single-seed) but the knee is bracketed
  (k=224 fails 0.3 SE, k=256 passes 0.7 SE) and the exponent-2/3 fit rests on
  FOUR rungs robust to the d=16 seed; barrier (f) is documented including the
  crash (same metrics/protocol, k=512 recovers full loss exactly); barrier (g)
  is partially documented — full-attention reference + same 0.98 bar intact, the
  random-k control UNMEASURED for this cell (NET-43's second seed restores it);
  barrier (h) sharpened — the true form at long context is measured to d=32 and
  pinned as concave power ≈ 2/3, and the per-doubling ratio is still < 2.
  Open: **d=32 ctx=512 second seed (closes the deepest rung's single-seed status
  AND repairs the missing random-k control — highest value)**; ctx=1024 second
  seed; d=8 @ ctx=256 s0 corner; carry chain at scale (the frontier).

- **NET-43 — THE-DEEPEST-RUNG-IS-TWO-SEED-256 (speed; the second seed that
  closes BOTH of NET-42's honest limits — the deepest rung's single-seed
  status AND the missing random-k control; ALL_DONE_NET43, no crash): at
  (d=32, ctx=512, seed=2) k* = **256 — EXACT reproduction of s1** (predicted
  256 reproducing s1; concave power 24.7·d^(2/3) ≈ 249). Full acc 0.1350,
  bar 0.1323, loss 5.6482, train 11563s (s1: 0.1353/5.6281/11113s). Sweep
  {96,128,160,192,224,240,256,288,320,384,512} — NET-42's grid minus the
  crashing k=768, plus the new k=240. Retained: k=96 0.893 ✗, k=128 0.919 ✗,
  k=160 0.945 ✗, k=192 0.957 ✗, k=224 0.973 ✗, k=240 **0.978 ✗** (new — fails
  ~0.2 SE below bar), k=256 **0.982 ✓**, k=288 0.984 ✓ (8d+32 passes but is
  NOT minimal — affine still over-predicts by 11%), k=320 0.987 ✓, k=384 0.996
  ✓, k=512 1.000 ✓ (loss 5.6482 = full exactly — product refuted by 2× at both
  seeds). The s2 retained curve is uniformly ~0.02 LOWER than s1's below the
  knee (0.893 vs 0.916 at k=96 … 0.973 vs 0.977 at 224) but converges AT the
  knee — the retained curve seed-fluctuates, the knee does NOT (the OPPOSITE
  of d=16, where the knee moved one grid step and the retained curve was
  flat-topped). **PART B2 REPAIRED** — random-k control ran: k=256 0.956
  (top-k 0.982) → gap +2.6; k=384 0.979 (top-k 0.996) → gap +1.7 — both
  positive, selection importance survives at the deepest rung, narrowing
  monotonically with depth (d=4 +5.3/+4.6 → d=8 +6.4/+3.7 → d=16 +3.4/+2.3 &
  +6.0/+2.6 → d=32 +2.6/+1.7). **NET-42's two honest limits CLOSED**: (i) the
  d=32 cell is now TWO-SEED with an exact knee (256, 256) — the
  concave-power-2/3 rung (predicts 249) confirmed at the deepest point, the
  two-seed knee bracket tightened to (240, 256], every ctx=512 rung now
  two-seed at its knee (64,64 / 96,96 / 160,144 / 256,256); (ii) the missing
  random-k control is measured (+2.6/+1.7). Concentration reproducible to
  ~0.7% (eff 216.92 vs s1 218.46, top-256 0.922 vs 0.921, per-position
  27.66/189.71/407.03 vs 27.81/190.90/409.08 — NO bounded working set, two
  seeds). Deployable speedup at (d=32, ctx=512) = **2.0×** confirmed two-seed
  (vs the 1.0× guarantee). Barriers: (a) clean — prediction (k\*=256) stated
  before the run, a reproducibility test closing the documented gaps; (b)
  clean — no depth-scaling law for data-free attention pruning in Catalog or
  literature; (c) confronted — d=32 × ctx=512 real causal word LM, 4097 vocab,
  held-out loss+acc; (d) clean (held-out last-10%, data-free top-k); (e) the
  round's substance RESOLVED — two-seed exact knee (256,256), s2 bracket
  (240, 256] tightens s1's (224, 256], exponent-2/3 fit robust to both seed
  choices; (f) clean — same metrics, binom SE ≈ 0.15%, k=512 recovers full
  loss exactly, NO crash (k=768 defect dropped, ALL_DONE_NET43 printed); (g)
  now FAIR — full-attention reference + same 0.98 bar + the random-k control
  at the same k (gaps +2.6/+1.7 positive, NET-42's barrier-(g) gap CLOSED);
  (h) sharpened — deployable 2.0× at d=32 is two-seed, sub-linear depth leg
  holds at both seeds, concave-power-2/3 deepest rung pinned at two seeds.
  Open: **ctx=1024 second seed (closes the last context-extrapolation cell's
  single-seed status)**; d=8 @ ctx=256 s0 corner; a third seed at d=16 (low
  value — flat-topped knee); carry chain at scale (the frontier).

- **NET-44 — THE-LAST-CONTEXT-CELL-IS-TWO-SEED-AND-THE-KNEE-FLUCTUATES (speed;
  the ctx=1024 second seed that closes the LAST context-extrapolation cell's
  single-seed status; ALL_DONE_NET44, no crash): at (d=4, ctx=1024, seed=2)
  k* = **96 — NOT the predicted 128, the FIRST break of product-exactness at
  any context** (predicted 128 reproducing s1; the prediction FAILED). Full
  acc 0.1591, bar 0.1559, loss 5.1179, train 6067s (s1: 0.1594/5.1209/5516s).
  Sweep {32,64,96,112,128,192,256,384,512,768} — k=112 NEW. Retained: k=32
  0.952 ✗, k=64 0.979 ✗ (~0.1 SE below bar — marginal; s1 0.968), k=96
  **0.987 ✓** (s1 0.977 ✗ — the s2 knee), k=112 0.991 ✓ (s2 knee is NOT
  112), k=128 0.993 ✓ (s1 0.986 ✓ — k*(s1)), k=192 0.998 ✓, k=256 1.001 ✓,
  k=384 0.998 ✓, k=512 0.999 ✓, k=768 1.000 ✓ (loss 5.1179 = full exactly).
  The s2 retained curve is uniformly ~0.01 HIGHER than s1's at every k
  (0.979/0.987/0.993 vs 0.968/0.977/0.986 at 64/96/128) — the knee crossed
  the bar one grid step (32) earlier. Part B2: random k=64 0.917 (top-k
  0.979) → selection gap **+6.2**; random k=128 0.945 (top-k 0.993) →
  **+4.8** (s1: +5.9/+4.6, reproduces to ~0.3 pts). Two-seed knee bracket
  **(64, 128]**; the product law d·ctx/32 (128) remains a proven-safe UPPER
  BOUND (passes 0.986/0.993 both seeds) but is NOT minimal at s2 — the s1
  context chain's exactness (16/32/64/128) was SEED-LUCKY. Knee-fluctuates-
  one-grid-step family now spans BOTH axes (depth at d=16 ctx=512 160/144;
  context at d=4 ctx=1024 128/96). Concentration reproducible to ~1.3% (eff
  294.97 vs 291.16, per-position within ~1.6%) — NO bounded working set, two
  seeds. Deployable speedup at (d=4, ctx=1024) = **8.0–10.7×** two-seed
  (guarantee 8× intact as floor). Barriers: (a) clean — prediction (k*=128)
  stated before the run, measured 96, so the run discriminates and exposes
  the exact-product reading as seed-lucky; (b) clean — no context-scaling
  seed-reproducibility of an attention knee in Catalog or literature; (c)
  confronted — d=4 × ctx=1024 real causal word LM, 4097 vocab, held-out
  loss+acc; (d) clean (held-out last-10%, data-free top-k); (e) the round's
  substance RESOLVED — the last single-seed context cell is two-seed with a
  one-grid-step knee fluctuation (128/96), the s2 curve uniformly higher at
  every k (opposite of d=32 ctx=512 s2); (f) clean — same metrics, binom SE
  ≈ 0.15%, k=768 recovers full loss exactly, NO crash (ALL_DONE_NET44); the
  k=112 addition pins the s2 knee at 96; (g) fair — full-attention reference
  + same 0.98 bar + random-k control at the same k (gaps +6.2/+4.8 vs
  +5.9/+4.6, both seeds positive); (h) sharpened — the exact-product claim
  becomes a two-seed bracket: deployable 8.0–10.7× at ctx=1024, the 8×
  guarantee intact as floor, the sub-linear drift at s2 the first hint the
  context lever is sub-linear in truth. Open: **ctx=2048 (does the sub-linear
  drift continue at 16× context?)**; a third seed at ctx=1024 (characterize
  the knee distribution {96,128}); d=8 @ ctx=256 s0 corner; a third seed at
  d=16 (low value); carry chain at scale (the frontier).

- **NET-45 — THE-S1-PRODUCT-CHAIN-SURVIVES-AT-FIVE-DOUBLINGS-AT-THE-TIGHTEST-MARGIN (speed;
  the ctx=2048 first seed that tests whether the sub-linear drift continues at 16× context —
  the sharpest open cell NET-44 made; ALL_DONE_NET45, no crash): at (d=4, ctx=2048, seed=1)
  k* = **256 = d·ctx/32 EXACTLY — the prediction CONFIRMED at the fifth doubling** (P1; P2=192
  systematic-0.75× and P3=224 one-grid-step both REFUTED at s1). Full acc 0.1543, bar 0.1512,
  loss 5.2047, train 18436s (~5.1h — the O(L²) attention term dominates at 2048, the longest
  training of the program). Sweep {96,128,160,192,224,256,288,384,512,768,1024}: k=96 0.939 ✗,
  k=128 0.951 ✗, k=160 0.963 ✗, k=192 0.970 ✗, k=224 0.976 ✗ (~0.45 SE below bar), k=256
  **0.9813 ✓** (margin +0.0013 — the TIGHTEST of the whole chain: 128/256/512/1024 were
  +0.007/+0.010/+0.003/+0.006), k=288 0.984 ✓, k=384 0.993 ✓, k=512 0.997 ✓, k=768 0.996 ✓,
  k=1024 0.998 ✓ (loss 5.2062 vs full 5.2047 — Δ0.0015, the first time the ctx/2 point is not
  EXACTLY full loss, a 2048-row renormalization residual, documented). The s1 context chain is
  now EXACT at FIVE doublings — 16/32/64/128/256 across 128→2048, 16× context, the longest
  measured anywhere in the program; the product law d·ctx/32 remains a proven-safe UPPER BOUND
  at every measured cell AND the exact knee at s1 through 16×. Part B2: random k=128 0.934
  (top-k 0.951) → selection gap **+1.7**; random k=256 0.963 (top-k 0.981) → **+1.8** — positive
  but the SMALLEST at d=4 (dilutes from +5.9/+4.6 at 8×, +5.3/+4.6 at 4×): the diffuse
  distribution at 16× carries most of the mass in any half of the keys. Concentration: eff
  support 526.39 (×1.81 on the doubling, same superlinear family), top-128 mass 0.589, top-256
  0.731, per-position 68.21/461.11/987.30 — NO bounded working set at 16×. Deployable speedup
  at (d=4, ctx=2048) = **8.0×**, the guarantee intact but now EQUAL to the knee (the s2 could
  read 224 → 10.3×). Barriers: (a) clean — prediction (k*=256) stated before the run, measured
  256; (b) clean — no context-scaling of data-free attention pruning at 16× in Catalog or
  literature; (c) confronted — d=4 × ctx=2048, the longest context of the program; (d) clean
  (held-out last-10%, data-free top-k); (e) the round's honest limit — single-seed at 16× with
  a razor-thin margin (+0.0013, k=224 fails ~0.45 SE): the ctx=2048 second seed is the sharpest
  open cell (decides whether 256 is two-seed-exact, extending ctx=512's 64/64, or drops one
  grid step to 224, replicating the NET-44 s2 break at 16×); (f) clean — same metrics, binom
  SE ≈ 0.11% acc, the +0.0013 margin documented, k=1024's Δ0.0015 residual noted, chunked eval
  (CHUNK=8) identical math, NO crash (ALL_DONE_NET45); (g) fair — full-attention reference +
  same 0.98 bar + random-k control at the same k (gaps +1.7/+1.8, positive); (h) sharpened —
  deployable 8.0× at 16× context, the guarantee equal to the knee, two-seed confirmation the
  practical next step. Open: **ctx=2048 second seed (closes the 16× cell's single-seed status —
  highest value)**; a third seed at ctx=1024 (knee distribution {96,128}); d=8 @ ctx=256 s0
  corner; a third seed at d=16 (low value); carry chain at scale (the frontier).

- **NET-46 — THE-S2-ONE-GRID-STEP-DROP-REPLICATES-AT-16×-CONTEXT (speed; the ctx=2048
  second seed that closes the 16× cell's single-seed status — the sharpest open cell NET-45
  made; ALL_DONE_NET46, no crash): at (d=4, ctx=2048, seed=2) k* = **224 — one grid step
  below the product knee 256, the prediction's horn P2 CONFIRMED (P1=256 two-seed-exact
  REFUTED)**. Full acc 0.1545, bar 0.1514, loss 5.2241, train 13508s (~3.75h — faster than
  s1's 18436s, 4-thread wall variance). Sweep {96,128,160,192,224,256,288,384,512,768,1024}:
  k=96 0.956 ✗, k=128 0.965 ✗, k=160 0.971 ✗, k=192 0.978 ✗ (~0.15 SE below bar), k=224
  **0.982 ✓** (margin +0.0023), k=256 0.986 ✓, k=288 0.987 ✓, k=384 0.992 ✓, k=512 0.993 ✓,
  k=768 0.998 ✓, k=1024 0.998 ✓ (loss 5.2247 vs full 5.2241 — Δ0.0006, this time nearly
  EXACTLY full loss, a cleaner read than s1's Δ0.0015). The s2 retained curve is uniformly
  ABOVE s1's (0.956 vs 0.939 at 96 … 0.982 vs 0.976 at 224) yet the knee reads one grid step
  LOWER — the whole s2 curve sits higher, crossing the bar one step earlier. The NET-44 s2
  pattern REPLICATES at 16×: 256→224 as 128→96 at 8× — the sub-linear drift at the second
  seed is SYSTEMATIC. The two-seed d=4 picture is now complete across all five doublings: s1
  exact at every context (16/32/64/128/256); s2 exact through 4× (64 at ctx=512) and exactly
  one grid step (32) below from 8× on (96, 224). The product law d·ctx/32 remains a
  PROVEN-SAFE UPPER BOUND at both seeds through 16× — its robust claim is the upper bound;
  its exactness is s1-specific at long context. Part B2: random k=128 0.921 (top-k 0.965) →
  selection gap **+4.4**; random k=256 0.947 (top-k 0.986) → **+3.9** — LARGER than s1's
  +1.7/+1.8 (the 16× dilution is seed-dependent). Concentration: eff support 472.50 (vs
  s1's 526.39 — s2 measurably more concentrated, consistent with the lower knee), top-128
  mass 0.623, top-256 0.759, per-position 61.56/412.27/888.64 — NO bounded working set at
  16×. Deployable speedup at (d=4, ctx=2048) = **≥8.0× guaranteed (product law, safe at both
  seeds), up to 9.1× at the s2-typical knee** — the first cell where the two-seed
  distribution brackets the deployable number. Barriers: (a) clean — both horns stated
  before the run, measured 224 — a replication test of NET-44's pattern at the longest cell;
  (b) clean — two-seed knee distribution of data-free attention pruning at 16×: none in
  Catalog or literature; (c) confronted — d=4 × ctx=2048, the longest context, now two-seed;
  (d) clean (held-out last-10%, data-free top-k); (e) the round's honest limit — the s2 drop
  is now measured at TWO cells (8× and 16×) — the reproducibility the s1 single-seed chain
  lacked — but {224,256} is two-point with no third seed; the sign (s2 ≤ s1 at long context)
  is robust, the exact one-grid-step magnitude needs a third seed at 1024; (f) clean — same
  metrics, binom SE ≈ 0.11% acc, the +0.0023 margin documented, k=1024's Δ0.0006 cleaner
  than s1's Δ0.0015, chunked eval identical math, NO crash (ALL_DONE_NET46); (g) fair —
  full-attention reference + same 0.98 bar + random-k control at the same k (gaps +4.4/+3.9,
  positive, the s1-vs-s2 spread informative); (h) sharpened — deployable ≥8.0× guaranteed /
  9.1× s2-typical, the two-seed distribution bracketing the claim. Open: **a third seed at
  ctx=1024 (does the knee distribution {96,128} hold or collapse? — highest value)**; a third
  seed at ctx=2048 (does {224,256} extend?); d=8 @ ctx=256 s0 corner; a third seed at d=16
  (low value); carry chain at scale (the frontier).

Assessment v46. 46 experiments (NET-1, NET-2, NET-3, NET-4, NET-5, NET-6, NET-7, NET-8, NET-9, NET-10, NET-11, NET-12, NET-13, NET-14, NET-15, NET-16, NET-18, NET-17, NET-20, NET-19, NET-21, NET-22, NET-23, NET-24, NET-25, NET-26, NET-27, NET-28, NET-29, NET-30, NET-31, NET-32, NET-33, NET-34, NET-35, NET-36, NET-37, NET-38, NET-39, NET-40, NET-41, NET-42, NET-43, NET-44, NET-45, NET-46).

- **NET-47 — THE-THIRD-SEED-REVEALS-A-SPREAD-NOT-A-TWO-POINT-SET (speed; the ctx=1024
  THIRD seed that decides whether the {96,128} knee distribution holds or collapses — the
  highest-value cell NET-46 made): at (d=4, ctx=1024, seed=3) k\*=112 (MID-GRID) — P3
  CONFIRMED, P1 (96) and P2 (128) REFUTED** (full acc 0.1582, bar 0.1550, loss 5.1387,
  train 6141s; sweep: 96 0.979 ✗ razor, 112 0.983 ✓ margin +0.0035, 128 0.988 ✓; k=768
  recovers loss exactly; ALL_DONE_NET47). The three-seed knee distribution is **{96,112,
  128}** — a ±16 half-grid-step jitter, mean = median = **112 = 7/8 × product**; the
  {96,128} binary was a TWO-SEED SAMPLING ARTIFACT. Emerging law at context ≥ 8× (d=4):
  **the seed-averaged knee sits at 7/8·(d·ctx/32)** (112 @ 8×; 224 = 7/8·256 is the mid
  of the 16× set {224,256}) with the product value the MAXIMUM of the seed range — the s1
  chain's exactness is the law's upper edge, not its center. Product law's upper bound
  STRENGTHENS to 3/3-seed-sure: product point 128 passes 3/3 seeds (0.986/0.993/0.988),
  k\* ≤ d·ctx/32 a three-seed-verified guarantee. Selection importance +4.7/+3.8 (positive
  but smallest at 1024; the seed spread 3.8–6.2 exceeds the eff spread ~4%); concentration
  eff 271.92 (most concentrated of the three, family within ~4%), and the eff↔knee
  correlation does NOT sort cleanly across three points (the NET-46 two-point correlation
  was a coincidence). Deployable ≥8.0× guaranteed / 9.1× median / 10.7× best. Barriers:
  (a) clean — three horns stated before the run, measured 112, the fine point winning;
  (b) clean — three-seed knee distribution / mid-grid knee / 7/8 median: none in Catalog
  or literature; (c) confronted — three seeds at d=4 × ctx=1024 real causal word LM;
  (d) clean (held-out last-10%, data-free top-k); (e) the round's SUBSTANCE — the
  {96,112,128} distribution IS the variance estimate, the {96,128} binary falsified; the
  7/8 median is a two-context hypothesis needing a third seed at 2048, and the s3 96/112
  boundary the least certain read (~0.5 SE); (f) clean — same metrics, binom SE ≈ 0.15%
  acc, margins documented, k=768 loss recovered exactly, NO crash (ALL_DONE_NET47);
  (g) fair — full-attention reference + same 0.98 bar + random-k at the same k (gaps
  +4.7/+3.8, positive); (h) sharpened — the three-seed distribution brackets the
  deployable claim with the guarantee at the conservative end. Open: a third seed at
  ctx=2048 (does the 7/8 median replicate at 16×? — direct test of this round's
  discovery); a fourth seed at ctx=1024 (refine {96,112,128}; low value); d=8 @ ctx=256
  s0 corner; carry chain at scale (the frontier).

- **NET-48 — THE-DIRECT-TEST-SURVIVES-VIA-THE-MEDIAN (speed; the ctx=2048 THIRD seed
  that directly tests the 7/8-median law NET-47 discovered — the highest-value cell NET-47
  made): at (d=4, ctx=2048, seed=3) k\*=160, all four point-horns REFUTED (P1 224, P2 240,
  P3 256, P4 192), P-every-value-passes-but-none-is-the-knee** (full acc 0.1546, bar 0.1516,
  loss 5.2199, train 14566s; sweep: 96 0.963 ×, 128 0.973 ×, 160 0.981 ✓ margin +0.0012
  razor, 192 0.984 ✓, 224 0.986 ✓, 240 0.987 ✓, 256 0.990 ✓, 288 0.993 ✓, 384 0.999 ✓,
  512 1.000 ✓, 768 1.003 ✓, 1024 1.003 ✓; ALL_DONE_NET48). The completed 16× three-seed
  knee distribution is **{160, 224, 256} — median 224 = 7/8·(d·ctx/32) EXACTLY, replicating
  the 8× median 112 = 7/8·128: the 7/8-MEDIAN LAW is 2/2-context, 6/6-seed.** The honest
  structure: per-seed knees too noisy to predict on the point (0/4 horns), the
  distribution's center robust (1/1 — a whole family {160,192,224} each keep the median at
  224). The 16× spread {0.625, 0.875, 1.0} is ~50% WIDER than 8×'s {0.75, 0.875, 1.0} —
  the low tail is the context-growing quantity, the product value the pinned upper edge.
  Product point 256 passes 3/3 (0.981/0.986/0.990): the k\* ≤ d·ctx/32 guarantee is
  3/3-seed-sure at BOTH long contexts. Selection importance +4.7/+3.4 (k=128 0.926 random
  vs 0.973 top-k; the 16× seed spread {1.7,4.4,4.7} — dilution seed-dependent);
  concentration eff 498.13 (mid-family, spread ~11%), eff↔knee again NOT sorting across
  three points, NO bounded working set. Deployable ≥8.0× guaranteed / 9.1× median /
  12.8× best — the BEST-EVER reading (beats 10.7× at 8×). Barriers: (a) clean — four
  horns + the law's direct test stated before the run, measured 160 outside ALL horns yet
  the distribution's median landed exactly on the predicted center (point-accuracy 0/4,
  structural confirmation 1/1); (b) clean — three-seed 16× spread / widening low tail:
  none in Catalog or literature; (c) confronted — three seeds at d=4 × ctx=2048 real
  causal word LM; (d) clean (held-out last-10%, data-free top-k); (e) the SUBSTANCE,
  sharpened — the 16× distribution complete; honest limits: the s3=160 read razor-thin
  (+0.0012, true knee ~150–160), the 0.625 low tail one of three seeds (a fourth decides
  s3-specific vs stable), the median law 2 contexts × 3 seeds; (f) clean — same metrics,
  binom SE ≈ 0.11% acc, the +0.0012 razor margin documented, k=512 recovers 1.000,
  NO crash (ALL_DONE_NET48); (g) fair — full-attention reference + same 0.98 bar +
  random-k at the same k (gaps +4.7/+3.4, positive, spread {1.7–4.7} informative);
  (h) sharpened — ≥8.0×/9.1×/12.8×, the widened spread the deployment-relevant
  uncertainty at the longest cell. Open: a fourth seed at ctx=2048 (the low-tail test —
  s4=160/192 → low tail real, s4 in {224,256} → s3-specific; highest value; ~4–5h);
  a fourth seed at ctx=1024 (refine {96,112,128}; low value); d=8 @ ctx=256 s0 corner;
  d=8 compression floor check; carry chain at scale (the frontier).

- **NET-49 — THE-REAL-MODEL-KNEE-COLLAPSES-AND-SATURATES (speed axis TRANSFERRED to real pretrained weights; LIMITED-MEMORY axis round 1): on Qwen2.5-0.5B (24 layers, GQA kv=2, wikitext-103 held-out eval, fp32, forward validated EXACTLY vs HF eager pre-measurement) the lossless attention knee is k\* = {16, 32, 24} at ctx = {512, 1024, 2048}** vs the toy product law's {384, 768, 1536} — **ratios 1/24, 1/24, 1/64**; scaling ×2.0 then ×0.75 (sub-linear, DECLINING); P3 confirmed, P1 refuted 16× beyond its floor, P2's linearity half-refuted (concentration half held: k\* ≤ ctx/8 everywhere). The DEPTH MULTIPLIER collapses from d to ~1 — no compounding r(k)^d penalty binds trained weights; median-layer effective support ≈ 10–12 keys context-INDEPENDENT (toy: 46→526), the ONLY diffusion in L22/L23 (eff 128.5/72.1 at 2048, sub-linear growth, 3.9× less diffuse than the toy MEAN layer), minimum L16 (2.9 keys). Selection importance inflates an ORDER OF MAGNITUDE: random-k gaps +68–82 pts (toy range +1.7–11.7), local-window gaps +40–55 pts (k=256 local only 0.598 retained at 2048 vs oracle top-k 0.9867 at k=32). Practical: oracle working set 24/2048 rows = 85× fewer KV reads, 64× fewer bytes; deployable policy needs a cheap selector (oracle-to-policy gap = open cell). Barriers: (a) clean (data-free oracle; horns about position/scaling); (b) confronted (H2O/StreamingLLM/SnapKV lineage exists; NEW = measured laws: protocol transfer, depth-collapse, ctx/32-then-decline shape, gap inflation, depth map); (c) CONFRONTED HEAD-ON — this IS the real-scale cell (one model, one size — transfer open); (d) clean (last-10% held out, zero training); (e) SUBSTANCE + limits (deterministic eval reproduced EXACTLY; TWO razor-thin knees +0.44/+0.5 SE documented, 2048 bracket (16, 24], 1024 bracket (16, 32] un-pinned at 24; one model one corpus — Gutenberg rate-limited, wikitext fallback); (f) clean (max|Δlogit|=0.0000 gate, fp32, NO crash ALL_DONE_NET49+49B); (g) fair (full reference + same 0.98 bar + random-k AND local-window at matched k, both crushed); (h) DIRECT (64× KV-byte reduction at the knee vs toy best-ever 12.8× attention reading; policy work named open). Open: per-layer ablation (is L22 load-bearing?); size transfer (1.5B / quantized-offloaded 7B); oracle-to-policy eviction gap; corpus robustness; weight-quantization floors (iteration 2). Paper 134, issue #230.

- **NET-50 — THE-TROPICAL-LIMIT-IS-LOSSY-BUT-THE-RECOVERY-IS-FAST (limited-memory axis round 2; mined from the Lean catalogue's tropical cluster): on Qwen2.5-0.5B pure argmax attention (k=1) retains only {0.364, 0.289, 0.250} at ctx={512, 1024, 2048} — WORSE at longer context — while k=2 recovers to 0.70–0.79, k=4 to 0.88–0.91 (P2 razor-clear at 512: 0.9097), k=8 to 0.94–0.96; the knee chain {16, 32, 24} replicates NET-49 EXACTLY cross-session (deterministic-eval proof). Maslov-gap map (LSE − max per row): bulk-layer medians 0.17–1.9 nats ≤ log 8, but the diffuse tail L22/L23 is the ONLY far-from-tropical region (medians 2.33/2.16 → 2.69/2.52, p90 ≈ 3.4); crystallization loss Σp(1−p) runs 0.34–0.97 — P3's crystallization half REFUTED honestly: real attention carries heavy soft mass that is individually tiny but collectively load-bearing (top-k to 24 keys still retains ≥98%). Practical regime = "tropical core + thin soft correction". Barriers: (a) clean (cliff/recovery/budget horns pre-stated); (b) clean (argmax-limit + budget measurements not in Catalog/lit); (c) confronted (real pretrained model, ONE model noted); (d) clean; (e) SUBSTANCE + limits (cross-session exact replication the strongest reproducibility evidence; single model/corpus; P3 half-refuted honestly); (f) clean (exact forward gate, fp32, ALL_DONE_NET50); (g) fair (full reference, same bar; NET-49 controls not re-run, noted); (h) DIRECT (the sub-k\* curve is the aggressive-compression region; quantified recovery per added key). Paper 135, issue #237.

- **NET-51 — THE-KV-CORE-IS-SHARED-THE-TAIL-IS-PERSONAL (limited-memory axis round 3; mined from the catalogue's amortized model-delta law): Qwen2.5-0.5B base vs Instruct on identical held-out prompts — layer-0 keys EXACTLY identical (cosK = 1.0000, relK 0.26%), all layers cosK ≥ 0.976; divergence is a HUMP not monotone (relK peaks 0.217 at L16 then falls; P2 REFUTED); mean top-1 attention decision agreement 0.894 across the bulk BUT it collapses to 0.568/0.627 in exactly the same L22/L23 diffuse-tail layers NET-50 found far-from-tropical — vector-level similarity does NOT bound functional divergence. Three measurements converge: the bulk of a transformer is shared machinery; the two-layer tail is model identity. Serving quantified: ~22/24 layers shareable at ≥0.92 decision agreement, tail personal. Both capture forwards gated vs HF eager pre-measurement (0.9922/0.9971); two gate-caught bugs fixed before any measurement counted. Barriers: (a) clean; (b) confronted (task-vector folklore; NEW = hump constants + decision-vs-vector dissociation + three-way convergence); (c) confronted (ONE pair/context, n=4 prompts noted); (d) clean (no training); (e) honest limits (cosine ≠ impact — hence Part B); (f) clean; (g) fair; (h) DIRECT. Open: tail-swap causal test; bigger pairs; SFT-vs-RLHF-vs-DPO tails; quantize-core-harder-than-tail link to NET-52. Paper 136, issue #238.

- **NET-52 — THE-TOY-FOUR-BIT-FLOOR-DOES-NOT-TRANSFER (limited-memory axis round 4; compression transfer test): naive per-channel RTN on Qwen2.5-0.5B costs +0.0044/+0.0353/+0.1281/**+0.7879/+9.2262/+14.0588 CE at 8/6/5/4/3/2 bits — the toy programme's per-channel-uniform-4 optimum (NET-11/14) REFUTED on a real LM by 16× its budget**; group-128 repairs ~60% of the 4-bit damage (+0.318, retained 0.906) and rescues 3-bit (+2.72 where per-channel dies); depth gradient CONFIRMED weakly (last-12 +0.405 vs first-12 +0.389 — NET-18's deeper-is-worse direction); mesh monotone with 8-bit measurably nonzero exactly as the catalogue's sharpness theorem demands. Practical: RTN < 6 bits not deployable; group-wise ≥4-bit the entry point; further compression needs error compensation (GPTQ/AWQ), not scale choice. Barriers: (a) clean (refuted horn pre-stated); (b) clean; (c) DECISIVE and honestly negative (limits: one model, ctx=512, RTN-only, embeddings/norms unquantized); (d) clean (bit-exact); (e) clean; (f) clean (baseline reproduced exactly, ALL_DONE_NET52); (g) fair (matched protocol); (h) DIRECT (bits×grouping surface = deployment table for 6 GB hosts). Open: GPTQ/AWQ on these floors; joint weight+KV budgets; tail-aware mixed precision per NET-51. Paper 137, issue #239.

- **NET-53 — COMPENSATION-WORKS-ON-THE-REAL-FLOORS (limited-memory axis round 5; cell (1) of the catalogue mining queue): sequential layer-wise GPTQ on Qwen2.5-0.5B lands 4-bit group-128 at +0.1512 dCE — 2.1× better than grouped RTN, 5.2× better than per-channel; P1 CONFIRMED at the boundary (≤0.15), P2 floor-target REFUTED by a hair (+0.151 vs ≤0.14), P3 tail-share REFUTED (18% < 25% — compensation shrinks the L22/L23 disproportionate cost); 3-bit ladder +9.23 → +2.72 → +1.19 across the axis (catastrophe → survival). Deployment table for the 6 GB host complete: RTN <6 bits unusable / grouped RTN viable@4 / grouped GPTQ viable@4 survivable@3. Faithful protocol: sequential layer-wise with input recapture, hooks on actual linear modules (container-hook bug found via width diagnostics), group-aligned blocks, escalating-damping Cholesky retry; calibration train-side only. Barriers: (a) clean (two refuted horns pre-stated); (b) confronted (GPTQ prior art; NEW = fixed-protocol ladder + tail-share + shrinkage finding); (c) confronted (one model, ctx=512, no act-order, 16-seq calib noted); (d) clean (train-side calibration only); (e) deterministic, damping pre-fixed; (f) clean (exact baseline reproduction, ALL_DONE_NET53); (g) fair (shared reference/protocol/granularity); (h) DIRECT. Open: act-order; joint weight+KV budgets; tail-aware mixed precision; size transfer to 1.5B. Paper 138, issue #243.

- **NET-54 — THE-TAIL-IS-LOAD-BEARING-BUT-UNPORTABLE (limited-memory axis round 6; causal test of NET-51): layer swaps between Qwen base and Instruct — bulk pair L10/11 transplants at ZERO measured cost (+0.0043/−0.0164 dCE; one direction slightly improves the host), tail pair L22/23 DESTROYS the hybrid: agreement with BOTH parents collapses below the 0.8327 cross-parent baseline (0.54–0.63) at +0.47/+0.55 CE; P1 transferable-identity REFUTED (the discovery — the tail is entangled, not portable), P2 asymmetry CONFIRMED (+0.465 vs +0.546), P3 portability CONFIRMED (<+1.0 nat). Third convergent measurement on the same two layers (NET-50 far-from-tropical; NET-51 decision-divergent; NET-54 non-transplantable) — the sharing boundary for multi-finetune KV serving is causally established: share everything except the tail. Barriers: (a) clean; (b) confronted (amputation lit; NEW = fine-tune-pair portability asymmetry + both-parents-collapse signature); (c) confronted (one pair, 12 windows, ctx=512, fp16); (d) clean (no training); (e) deterministic, restore-by-construction; (f) clean (ALL_DONE_NET54); (g) fair (matched-width bulk controls, both directions); (h) DIRECT. Open: dose-response; swap+recalibration; 1.5B pair; compensated-tail personality. Paper 139, issue #246.

- **NET-55 — THE-KNEE-IS-SIZE-INVARIANT (limited-memory axis round 8; size transfer): Qwen2.5-1.5B (3× params, d=28) posts k\* = {16, 16} at ctx = {512, 1024} — identical to 0.5B at 512, HALF of it at 1024; P1 knees-grow-with-scale REFUTED decisively (below the pre-registered floor at both contexts), P2 tail-map honestly UNMEASURED (harness rewrite dropped the stats block), P3 saturation CONFIRMED stronger (ratio 1.0 — flat). The real-model knee family {16,32,24}@0.5B and {16,16}@1.5B is flat-to-declining in context and flat in scale: ~30 keys covers every measured cell while the toy law predicted 384–1344 — concentration structure of trained attention, not capacity, sets the knee; KV working-set budget does NOT scale with model size. Engineering record: Qwen2.5-1.5B fp16 forward NaNs on real text (verified); CPU-fp32 reference SIGILLs on this host; gate = HF-bf16-GPU reference captured pre-floatify, ΔCE 0.0054 binding / argmax-agreement 0.89 (near-tie flips, documented). Barriers: (a) clean; (b) clean; (c) confronted (two size points; grid floor at 16 — sub-16 addendum open; one corpus; SE ≈ 0.3%); (d) clean; (e) deterministic, gate calibration documented; (f) clean (ALL_DONE_NET55); (g) fair (same bar as all real-model rounds); (h) DIRECT. Open: sub-16 addendum @1024; 1.5B tail map (P2); 7B quantized-offload cell; oracle-to-policy gap; corpus robustness. Paper 140, issue #284.

- **NET-56 — THE-ORACLE-OVERSTATES-THE-DEPLOYABLE-WIN (limited-memory axis round 9; oracle-to-policy gap): a causally-honest streaming KV policy (accumulated-score heavy-hitters, block-128, current block always cached, strict per-row causality) on Qwen2.5-0.5B at ctx=1024 retains only {0.863, 0.882, 0.919} at budgets {32, 64, 128} where the omniscient oracle posts {0.991, 0.995} at {32, 64} — an 11.3-point gap at matched B=64; the fixed hybrid (HH + recency) dominates pure HH everywhere ({0.921, 0.938, 0.961}, +4–6 pts — P2 confirmed) but even 128 keys (12.5% of context) reaches only 0.961 (P3 refuted). Trained attention is prunable in RETROSPECT, not predictable ONLINE: accumulated attention is a biased estimator of future importance. Gate exact (argmax-agree 1.0000); oracle arms cross-replicate NET-49's knee to four decimals; SEVEN pre-recording variants rejected by sanity gates (documented as bracketing negative controls in git). Barriers: (a) clean (refuted horn pre-stated); (b) confronted (H2O lineage; NEW = quantified gap on the knee-measuring harness itself); (c) confronted (one model/context/policy stated); (d) clean; (e) deterministic + sanity-band acceptance; (f) clean (ALL_DONE_NET56); (g) fair (matched budgets, identical harness); (h) DIRECT. Open: learned importance heads; per-layer budgets; 1.5B replication; corpus robustness (next). Paper 141, issue #287.

- **NET-57 — THE-KNEES-ARE-CORPUS-ROBUST (limited-memory axis round 10; corpus robustness): independent wikitext shard (train shard 1 vs shard 0, byte-identical harness) gives Qwen2.5-0.5B knees {16, 32, 32} at ctx {512, 1024, 2048} — EXACT matches to corpus-A at 512 and 1024, controls replicating to FOUR DECIMALS (random-k 0.1775/0.3004 = corpus-A exactly), the 2048 reading (32 vs A's razor-thin 24) inside NET-49B's documented bracket (joint: knee ≈ 24–32 at 2048); bonus third-context replication. The ~30-key budget now holds across 3 contexts × 2 corpora × 2 model sizes; the single-corpus limit carried since NET-49 is CLOSED. One OOM incident (stray GPU process) diagnosed and cleared before any recorded measurement. Barriers: (a) clean; (b) clean; (c) confronted — this WAS the corpus test (both corpora wikitext-family; domain jump open); (d) clean per-corpus held-out splits; (e) deterministic + 4-decimal cross-corpus control agreement; (f) clean (ALL_DONE); (g) fair (byte-identical harness, only text changed); (h) DIRECT. Open: domain-jump corpus; learned importance heads; per-layer budgets; 1.5B tail map; 7B cell. Paper 142, issue #290.

- **NET-58 — CONTENT-IS-A-WEAK-PREDICTOR-OF-IMPORTANCE (limited-memory axis round 11; NET-56 follow-up): per-(layer, kv-head) ridge probes on 64-d post-rope keys recover only R² ≈ 0.33 (range 0.11–0.64, front-high/mid-low) of each key's future attention from TRAIN-side fits; content-based streaming eviction lands {0.840, 0.894, 0.928} at B={32,64,128} vs accumulated-HH {0.863, 0.882, 0.919} and oracle {0.991, 0.995} — ~1 point over accumulation at 64/128, WORSE at 32; P1 (close ≥⅓ of gap) REFUTED (~11%), P2 CONFIRMED (10+ pts remain), P3 CONFIRMED. The oracle-to-policy gap is STRUCTURAL: importance is relational+positional, not intrinsic to key identity — bounding all content-based KV policies. Gate exact; probes train-side only. Barriers: (a) clean; (b) confronted (probe folklore; NEW = measured policy ceiling + R²→retained conversion); (c) confronted (linear class; one model/context); (d) clean; (e) deterministic closed-form; (f) clean (ALL_DONE_NET58); (g) fair (matched vs NET-56); (h) DIRECT. Open: MLP heads (bounded by P2 logic); per-layer ablation (next); probe+recency hybrid; 1.5B tail map. Paper 143, issue #291.

- **NET-59 — NO-SINGLE-LAYER-IS-THE-BOTTLENECK (limited-memory axis round 12; the per-layer load-bearingness ablation open since NET-49): solo-layer oracle top-k profiles are FLAT — all 24 layers tolerate k=16 alone at ≤0.5% cost (spread 0.6 pts, worst L12 0.9953; tail L22 0.9987 mid-pack, L23 1.0008 BEST), k=32 flatter still (0.5 pts); P1 tail-is-critical REFUTED, P2 confirmed trivially, P3 non-uniform REFUTED. EPISTASIS resolution of the four-fold tail specialness (NET-50 far-from-tropical / NET-51 decision-divergent / NET-54 unportable / personal-KV): it lives in INTERACTION with upstream representations, not individual fragility; joint all-layer k=16 cost (1.7%, NET-50) is SUB-ADDITIVE over solo costs (~4.8% if additive). No per-layer budget hierarchy to exploit in mixed-precision serving at this scale. Gate exact; ctx=512; 24 windows. Barriers: (a) clean (two refuted horns pre-stated); (b) clean; (c) confronted (one context, solo granularity stated); (d) clean; (e) deterministic monotone; (f) clean (ALL_DONE_NET59); (g) fair; (h) DIRECT. Open: pairwise/joint tail ablations; 1.5B replication; probe+recency hybrid; domain-jump corpora; 7B cell. Paper 144, issue #293.

- **NET-60 — THE-EPISTASIS-LIVES-IN-THE-TAIL-PAIR (limited-memory axis round 13; locates NET-59's interaction): solo costs of L22+L23 sum to 0.06 pts yet joint k=16 pruning costs 0.42 pts — SUPER-ADDITIVE 7×, the largest of six tested pairs; tail triple {21,22,23} compounds (0.76 vs 0.19 summed, 4×); bulk pairs additive-or-sub ({12,15} sub 0.60/0.79; {22,12} cross sub); P1 CONFIRMED, P2 REFUTED (3 of 6 super-additive), P3 CONFIRMED. The last two layers function as a COORDINATED UNIT — co-adapted in pretraining, individually absorbable, jointly load-bearing — matching the four correlational markers; prescription: treat the tail as ONE unit for bits/budgets, never differentiate between its members. Gate exact; ctx=512; 24 windows. Barriers: (a) clean; (b) clean (pairwise super-additivity maps new); (c) confronted (one context/model, five chosen pairs stated); (d) clean; (e) deterministic, solo sums from committed NET-59 profile; (f) clean (ALL_DONE_NET60); (g) fair; (h) DIRECT. Open: 1.5B replication; deeper-tail units at scale; probe+recency hybrid; domain-jump corpora. Paper 145, issue #294.

- **NET-61 — CONTENT-ADDITIVE-EVICTION-DOES-NOT-HELP (limited-memory axis round 14; closes the cheap-signals line): hybrid eviction z(accumulated)+λ·z(probe) is monotonically WORSE with probe weight — {0.9384, 0.9383, 0.9365, 0.9344} at B=64 for λ={0, 0.25, 1, 4}; P1 some-λ-wins REFUTED, P2 small-λ-optimal CONFIRMED (λ=0 optimal, reproducing NET-56's hybrid to four decimals), P3 ceiling CONFIRMED (best trails oracle@64 by 5.7 pts). With NETs 56/58, EVERY cheap eviction-signal family — accumulation ± recency, content alone, linear combinations — is now bounded ≥5.7 pts below oracle at matched budget: the policy gap is structural across families. Gate exact; probes train-side; λ-grid pre-stated. Barriers: (a) clean; (b) confronted (H2O score-combination variants exist; NEW = monotone-degradation law + four-family bounding); (c) confronted (one model/context, linear probes, fixed recency stated); (d) clean; (e) deterministic pre-stated grid; (f) clean (ALL_DONE_NET61); (g) fair (identical harness as 56/58); (h) DIRECT. Open: sub-16 addendum @1024; domain-jump corpora; 1.5B tail map; 7B cell. Paper 146, issue #296.

- **NET-62 — THE-KNEE-LANDS-ON-THE-FINE-GRID (limited-memory axis round 15; the sub-16/24 addendum open since NET-49): fine sweep at ctx=1024 pins the 0.5B knee at k\* = 20 (k=16 fails 0.971, k=20 passes 0.980, k=24 passes 0.985) — the chain is now strictly monotone {16, 20, 24} across {512, 1024, 2048}, replacing the coarse {16, 32, 24}; NET-55's size-invariance SHARPENS (1.5B {16, 16} flat-to-declining against a rising baseline); the 2048 corpus-B reading (32) looks like a coarse-grid artifact rather than corpus sensitivity; knee-quantizes-to-grid gains a third instance; P1 and P2 both CONFIRMED. Baseline 0.4627 bit-identical to three prior rounds. Barriers: (a) clean; (b) clean; (c) confronted (finer grid; 24 windows stated); (d) clean; (e) deterministic pre-stated grid; (f) clean (ALL_DONE_NET62); (g) fair; (h) DIRECT (deployment table 1024 entry: 32 → 20). Open: fine grids at 512/2048; domain-jump corpora; 1.5B fine-grid; 7B cell. Paper 147, issue #298.

- **NET-63 — THE-2048-KNEE-IS-TWENTY-FOUR (limited-memory axis round 16; fine-grid resolution of the 2048 cell): fine sweep k∈{20,24,28,32} on corpus-A confirms k\*(2048)=24 — k=20 fails 0.9793, k=24 passes 0.9835 (+0.35 pts, 7× healthier than the original +0.05 SE razor), monotone through k=32 (0.9885); P1 knee-in-{28} REFUTED, P2 monotone-chain CONFIRMED ({16, 20, 24} strictly monotone on fine grids across all three contexts), P3 PARTIAL; corpus-B's coarse-grid 32 isolated as shard-or-window-count question, inside the ~30-key budget either way; quantization is context-dependent (smooth bracketing at 2048 vs ON-grid at 1024). Gate exact; 12 windows (VRAM-bound) stated. Barriers: (a) clean; (b) clean; (c) confronted; (d) clean; (e) deterministic; (f) clean (ALL_DONE_NET63); (g) fair; (h) DIRECT. Open: corpus-B fine sweep @2048; domain-jump corpora; 1.5B fine grids; 7B cell. Paper 148, issue #299.

- **NET-64 — THE-CORPUS-B-DISAGREEMENT-WAS-A-GRID-ARTIFACT (limited-memory axis round 17; closes the last knee-chain discrepancy): corpus-B fine sweep @2048 gives k\* = 24 — IDENTICAL to corpus-A (k=20 fails 0.9790, k=24 passes 0.9832); the full 0.5B fine-grid chain {16, 20, 24} replicates EXACTLY across two disjoint wikitext shards at all three contexts — every deployment-table entry dual-corpus-confirmed; baseline accuracies differ between shards (0.495 vs 0.476) while knees are identical: text difficulty and attention-budget structure are independent. P1/P3 REFUTED, P2 CONFIRMED. Gate exact; 12 windows stated. Barriers: (a) clean; (b) clean; (c) confronted; (d) clean; (e) deterministic; (f) clean (ALL_DONE); (g) fair (byte-identical harness except corpus path); (h) DIRECT. Open: domain-jump corpora; 1.5B fine grids; 7B quantized-offload cell. Paper 149, issue #300.

- **NET-65 — SIXTEEN-IS-REAL (limited-memory axis round 18; the 1.5B sub-16 addendum): every sub-16 point fails at ctx=1024 on Qwen2.5-1.5B (k=4: 0.9318, k=6: 0.9532, k=8: 0.9660, k=12: 0.9759 razor ~2SE) — the knee is EXACTLY k\*=16 (bracket (12, 16]); P1 scale-decline REFUTED, P2 CONFIRMED; refined scale law: the 0.5B chain RISES with context ({16, 20, 24}) while the 1.5B is FLAT ({16, 16}) — larger models have more context-STABLE attention budgets (CONTEXT-SENSITIVITY of the attention budget decreases with scale in its first measured step); a 16-key budget covers both models to ctx=1024. Gate identical to NET-55 (ΔCE 0.0054); baseline bit-identical (0.5004). Barriers: (a) clean; (b) clean; (c) confronted (razor bracket stated); (d) clean; (e) deterministic baseline-replicating; (f) clean (ALL_DONE_NET65); (g) fair; (h) DIRECT. Open: 1.5B @2048 fine grid (does flat break upward?); domain-jump corpora; 7B cell. Paper 150, issue #302.

- **NET-66 — SCALE-DELAYS-CONTEXT-SENSITIVITY-BY-ONE-DOUBLING (limited-memory axis round 19; the 1.5B's first 2048 cell): fine grid k∈{8,12,16,20,24,32} gives the 1.5B chain {16, 16, 20} at {512, 1024, 2048} — k=16 fails RAZOR at 2048 (0.9785, ~1 SE) and k=20 passes (0.9817); P1 flat-breaks-upward CONFIRMED, P2 flat-holds REFUTED, P3 sensitivity-increases REFUTED (20 < the 0.5B's 24 at the same context). THE BROKEN CURVE EQUALS THE 0.5B'S SHIFTED ONE OCTAVE: 1.5B@2048 = 20 = 0.5B@1024 — scale POSTPONES context-sensitivity by one context-doubling rather than eliminating or amplifying it; budget tables gain a scale-shift form (a 16-key budget covers the 0.5B to 512 and the 1.5B to 1024). Gate identical to NET-55/65; baseline 0.5132 monotone; bracket (16, 20] partially open (razor fail). Barriers: (a) clean; (b) clean; (c) confronted (razor + 12 windows stated); (d) clean; (e) deterministic; (f) clean (ALL_DONE_NET66); (g) fair; (h) DIRECT. Open: sub-20 addendum @2048; 0.5B @4096; domain-jump corpora; 7B cell (does the shift extend?). Paper 151, issue #304.

- **NET-67 — SCALE-HALVES-THE-CONTEXT-INCREMENT (limited-memory axis round 20; sub-20 addendum): the 1.5B knee at 2048 is 18 — k=14 fails 0.9757 (~2 SE), k=18 passes 0.9811 — refining the chain to {16, 16, 18}; P1 CONFIRMED, P2 REFUTED; the cleaner law behind NET-66's one-octave approximation: both models START at 16 keys and scale HALVES the context-increment (+4/doubling at 0.5B → +2/doubling at 1.5B); baseline drift-assert passed exactly (0.5132); deployment: a 20-key budget covers BOTH models to 2048 with margin. Barriers: (a) clean; (b) clean; (c) confronted (two-point addendum stated); (d) clean; (e) deterministic drift-assert; (f) clean (ALL_DONE_NET67); (g) fair; (h) DIRECT. Open: increments at 4096; domain-jump corpora; 7B cell (does halving extend?). Paper 152, issue #305.

- **NET-68 — CODE-NEEDS-FEWER-KEYS (limited-memory axis round 21; the domain-jump cell): Python source shifts the 0.5B knee chain DOWN one fine step — {12, 16} at {512, 1024} vs prose's {16, 20} — while baseline accuracy jumps UP (0.630/0.652 vs 0.446/0.461); P1 transfer CONFIRMED, P2 CONFIRMED, P3 REFUTED; budget law now domain-parameterized: k\*(domain, ctx) = base(domain) + increment(scale) × doublings(ctx), base(prose)=16, base(code)=12, increments set by scale (NET-67); THIRD confirmation accuracy-level ⊥ knee-position; deployment: size KV by largest-base domain present. Gate exact; 24 windows/context; code corpus fsynced durable. Barriers: (a) clean; (b) clean; (c) confronted (one code language, single repo stated); (d) clean per-corpus split; (e) deterministic; (f) clean (ALL_DONE_NET68); (g) fair (only text changed); (h) DIRECT. Open: math/non-English domains; increments@4096; 7B cell; probe+recency on code. Paper 153, issue #306.

- **NET-69 — CONTENT-WEAKNESS-IS-DOMAIN-UNIVERSAL (limited-memory axis round 22; NET-58/61 follow-up on code): on Python source (the strongest candidate for content-based importance), linear probes recover only R² = 0.3185 (vs prose 0.329 — statistically identical), probe-only eviction LOSES to accumulated usage by 12 pts (0.8149 vs 0.9340 at B=64), and the hybrid is NON-DEGRADING (+0.3 pts, contrasting prose's monotone harm); P1 REFUTED decisively, P2 CONFIRMED both clauses, P3 CONFIRMED; importance is relational in structured domains too — content neutral-at-best even where syntax repeats; code-domain picture complete: fewer keys (12/16 per NET-68), content useless for choosing them. Gate exact; probes train-side. Barriers: (a) clean; (b) clean (first cross-domain probe comparison); (c) confronted (one language/repo stated); (d) clean; (e) deterministic; (f) clean (ALL_DONE_NET69); (g) fair (identical methodology/budgets as 58/61); (h) DIRECT. Open: math/non-English; learned online predictors; increments@4096; 7B cell. Paper 154, issue #309.

- **NET-70 — MATH-READS-AS-PROSE (limited-memory axis round 23; second domain-jump leg): mathematical text leaves the knee chain EXACTLY at prose values — {16, 20} at {512, 1024} — while baseline accuracy drops 12 pts (0.326/0.342 vs 0.446/0.461); P1 math-needs-more REFUTED, P3 base-universal CONFIRMED; THREE-DOMAIN deployment table complete: base(prose)=16, base(code)=12, base(math)=16, increments by scale (NET-67), shape preserved everywhere; THIRD+STRONGEST confirmation that prediction difficulty and attention-sparsity structure are independent (harder text, identical budgets). Gate exact; 24 windows/context; corpus fsynced durable. Barriers: (a) clean; (b) clean; (c) confronted (classic math prose only, no modern LaTeX stated); (d) clean per-corpus split; (e) deterministic; (f) clean (ALL_DONE_NET70); (g) fair (only text changed); (h) DIRECT. Open: modern LaTeX notation; non-English domains; increments@4096; 7B cell. Paper 155, issue #310.

- **NET-71 — THE-TOKENIZER-TAX-IS-FOUR-KEYS (limited-memory axis round 24; third domain-jump leg): German prose shifts the knee chain UP exactly one fine-grid step — {20, 24} at {512, 1024} vs English prose's {16, 20} — mirroring code's −4 below; FOUR-DOMAIN deployment table complete: base(code)=12, base(prose-EN)=16, base(math)=16, base(prose-DE)=20; +4/doubling increment UNIVERSAL across all four domains and scales; P1 CONFIRMED (exactly +4 at both contexts), P2/P3 REFUTED (full step not intermediate); tokenizer-tax mechanism: German compounds pack more content per word → more positions per idea. Gate exact; 24 windows/context; corpus fsynced durable. Barriers: (a) clean; (b) clean; (c) confronted (German only stated); (d) clean; (e) deterministic; (f) clean (ALL_DONE_NET71); (g) fair (only text changed); (h) DIRECT. Open: more languages; modern LaTeX; increments@4096; 7B cell. Paper 156, issue #310.

- **NET-72 — THE-FRENCH-KNEE-EXCEEDS-THE-GRID (limited-memory axis round 25; fourth domain-jump leg): on French prose NO grid point reaches the 0.98 bar — k=24 retains only 0.9648 @512 and k=32 only 0.9680 @1024 — a domain shift FAR larger than German's +4 (brackets: knee >24 and >32); ALL THREE HORNS REFUTED; the domain-shift law is NOT ±4 fine-steps — language families differ by whole grid ranges; accuracy/knee decoupling has BOTH SIGNS (French easier AND needs more); mechanism hypothesis: tokenization-mediated (Qwen spends more tokens/French word, diluting per-token attention contribution — testable via tokens-per-word measurement). Gate exact; one Gutenberg source (second 404'd) stated; sub-knee ceiling stated. Barriers: (a) clean; (b) clean (first beyond-grid result); (c) confronted; (d) clean; (e) deterministic; (f) clean (ALL_DONE_NET72); (g) fair; (h) DIRECT. Open: tokens-per-word mechanism test; extended grid {48,64}; more languages; 7B cell. Paper 157, issue #312.

- **NET-73 — TOKENIZATION-DENSITY-DOES-NOT-EXPLAIN-THE-DOMAIN-SHIFT (limited-memory axis round 26; the tokens-per-word mechanism test proposed by NET-72): Spearman(TPW, k\*) = −0.40 (WRONG SIGN), linear R² = 0.004 — code has the HIGHEST tokens-per-word (1.95) yet the LOWEST knee (12), while French has near-English TPW (1.25) yet the HIGHEST knee (>32); P1/P2 REFUTED, P3 CONFIRMED decisively; the tokenization-mediated hypothesis is refuted by its strongest counterexample; the domain mechanism is NOT how many tokens per word but the RELATIONAL/SEMANTIC structure of attention patterns within each domain — redirecting search from surface to deep-level explanations; NET-58/69 already bound those as relational, not intrinsic. French extended grid pins k\*(fr@512) ≤ 32. Gate exact; 5 domains, 5000-word samples, one tokenizer stated. Barriers: (a) clean; (b) clean (first mechanism-test); (c) confronted; (d) clean; (e) deterministic; (f) clean (ALL_DONE_NET73); (g) fair; (h) DIRECT. Open: attention-pattern structural analysis; sub-32 French @1024; 0.5B @4096; 7B cell. Paper 158, issue #314.

- **NET-74 — TOP8-MASS-IS-THE-STRONGEST-STRUCTURAL-PREDICTOR (limited-memory axis round 25; attention-structure mechanism test): across 5 domains, Spearman(top-8 attention mass, k\*) = +0.80 — the strongest of three structural measures tested; entropy anticorrelates −0.60 (right sign, partial); cross-head agreement does NOT predict (−0.40, ~8% everywhere — constant not differentiator); P1 PARTIAL, P2 CONFIRMED, P3 REFUTED; the POSITIVE sign means the knee is set by the RESIDUAL spread after the top keys, not by top concentration — mechanism is in the TAIL of the attention distribution; head diversity is a constant, not a domain differentiator. Gate exact; 5 domains, 3 sampled layers {2,11,21}, 12 windows @ctx=512 stated; cosmetic res-scoping error after all data printed. Barriers: (a) clean; (b) clean; (c) confronted; (d) clean; (e) deterministic; (f) clean; (g) fair; (h) DIRECT. Open: tail-shape analysis; sub-20 addendum @2048; 0.5B @4096; 7B cell. Paper 159, issue #315.

- **NET-75 — THE-FRENCH-KNEE-IS-FORTY (limited-memory axis round 27; French extended grid resolving NET-72's open bracket): extended grid k∈{36,40,48,56,64} pins k\*(fr@1024) = 40 — exactly DOUBLE English prose's 20; k=36 fails 0.9795, k=40 passes 0.9830; P1 CONFIRMED (knee ≤48), P2 REFUTED (40 ≠ predicted ~28–32); five-domain table @1024: code=12, EN=20, math=20, DE=24, FR=40; tokenizer-tax is a domain-dependent MULTIPLIER not a fixed +4 (German +4, French +20); mechanism must be language-specific attention pattern structure; increment (+4/doubling) appears domain-universal. Gate exact; 24 windows stated. Barriers: (a) clean; (b) clean; (c) confronted; (d) clean; (e) deterministic; (f) clean (ALL_DONE_NET75); (g) fair; (h) DIRECT. Open: French @512 extended; increments@4096; more languages; 7B cell. Paper 160, issue #316.

- **NET-76 — THE-DOMAIN-FACTOR-IS-MULTIPLICATIVE (limited-memory axis round 28; French @512 extended grid): k\*(fr@512) = 32 (k=28 fails 0.9772, k=32 passes 0.9813), completing the French chain {32, 40} with +8/doubling increment; the complete five-domain × two-context table reveals each domain's ENTIRE budget curve scales by a single multiplicative factor: code ≈0.75×, EN/math ≈1.0×, DE ≈1.25×, FR = 2.0× relative to English prose; P2 CONFIRMED, P3 CLOSE; one number per domain replaces a full grid measurement for any new domain within its family. Gate exact; 24 windows stated. Barriers: (a) clean; (b) clean; (c) confronted; (d) clean; (e) deterministic; (f) clean (ALL_DONE_NET76); (g) fair; (h) DIRECT. Open: 4096 increments; more languages/domains; 7B scale test. Paper 161, issue #317.

Assessment v76. 76 experiments (NET-1, NET-2, NET-3, NET-4, NET-5, NET-6, NET-7, NET-8, NET-9, NET-10, NET-11, NET-12, NET-13, NET-14, NET-15, NET-16, NET-18, NET-17, NET-20, NET-19, NET-21, NET-22, NET-23, NET-24, NET-25, NET-26, NET-27, NET-28, NET-29, NET-30, NET-31, NET-32, NET-33, NET-34, NET-35, NET-36, NET-37, NET-38, NET-39, NET-40, NET-41, NET-42, NET-43, NET-44, NET-45, NET-46, NET-47, NET-48, NET-49, NET-50, NET-51, NET-52, NET-53, NET-54, NET-55, NET-56, NET-57, NET-58, NET-59, NET-60, NET-61, NET-62, NET-63, NET-64, NET-65, NET-66, NET-67, NET-68, NET-69, NET-70, NET-71, NET-72, NET-73, NET-74, NET-75, NET-76).

- **NET-78 — THE-INCREMENT-ACCELERATES-AT-4096 (limited-memory axis round 29; the fourth context doubling): the 0.5B knee at ctx=4096 is k\*=40 (k=32 fails 0.979, k=40 passes 0.984) — the increment jumps from +4/doubling to +16/doubling, a 4× ACCELERATION that breaks the linear-increment law after three doublings; complete chain {16, 20, 24, 40}: increments +4, +4, +16; P1/P2 REFUTED, P3 CONFIRMED dramatically; first evidence of a PHASE TRANSITION in context-sensitivity — attention budgets context-stable for first ~2000 tokens then sharply more expensive; deployment: budget tables need nonlinear extension beyond 2048. Gate exact; 6 windows stated. Barriers: (a) clean; (b) clean; (c) confronted; (d) clean; (e) deterministic; (f) clean; (g) fair; (h) DIRECT. Open: fine grid between 32 and 40; 1.5B @4096; domain-jump @4096; 7B cell. Paper 162, issue #320.

- **NET-79 — THE-ACCELERATION-IS-UNIVERSAL (limited-memory axis round 30; the 1.5B's first 4096 cell — the decisive test for whether scale delays the phase transition): the 1.5B knee at ctx=4096 is k\*=56 — every point from 16 to 44 fails; P1 shift-delays REFUTED, P2 acceleration-universal CONFIRMED dramatically (56 ≥ 48), P3 REFUTED; complete two-scale × four-context table: 0.5B {16,20,24,40} increments +4,+4,+16; 1.5B {16,16,18,56} increments 0,+2,+38; scale doesn't delay the acceleration — it AMPLIFIES it (0.5B 4×, 1.5B 19×); CROSSOVER discovered: larger models more efficient at short contexts but LESS efficient at long contexts; deployment tables need scale × context interaction term. Gate identical to NET-55/65/66 (ΔCE 0.0054); baseline 0.4937; expandable-segments allocator required for VRAM; 2 windows stated. Barriers: (a) clean; (b) clean; (c) confronted; (d) clean; (e) deterministic; (f) clean; (g) fair; (h) DIRECT. Open: fine grid 44–56; crossover localization; domain-jump @4096; 7B cell. Paper 163, issue #322.

Assessment v79. 79 experiments (NET-1 through NET-79).
- **NET-80 — THE-INTEGRATED-DEPLOYMENT-TABLE (synthesis round): thirty-one limited-memory iterations (NET-49–79) distilled into a single engineering reference — complete knee chains for two scales across four domains at three contexts, quantization floors with compensation, streaming policy adjustments, scale × context × domain interaction terms, SEVEN quantitative laws, and a five-step engineering recipe for 6 GB serving. Paper 164 (synthesis).

Assessment v80. 80 experiments (NET-1 through NET-80).
- **NET-81 — THE-CROSSOVER-SEARCH (partial; limited-memory axis round 30): 0.5B crossover localization produced non-monotone results (@2560 k*=44, @3072 k*=28 — likely n=6 sampling variation); 1.5B cells crashed on floatify double-registration; crossover remains localized to (2048, 4096) pending replication with more windows. Paper 165 (partial).

- **NET-83 — THE-INTEGRATION-IS-SUPER-ADDITIVE (limited-memory axis round 33; the integration test combining weight and attention axes): GPTQ 4-bit group-128 combined with top-k=16 attention degrades to 0.860 retained — WORSE than the sum of individual degradations (attention −2.3% + quantization −9.2% = −11.5% expected, but combined −14.0%); P1 sub-additive REFUTED, P2 super-additive CONFIRMED, P3 independent REFUTED; sparse attention AMPLIFIES quantization noise (perturbed keys shift top-k selection boundary; selected values carry uncompensated error); deployment: budget tables need INTERACTION PENALTY when both optimizations active. SEVEN debug iterations caught six bugs including critical runner-layers reference bug. Gate exact. Barriers: (a) clean; (b) clean; (c) confronted (simplified RTN stated); (d) clean; (e) deterministic; (f) clean (ALL_DONE_NET83); (g) fair; (h) DIRECT. Open: real GPTQ with Hessian; tail-aware precision; crossover replication. Paper 165, issue #323.

Assessment v84. 84 experiments (NET-1 through NET-84).
- **NET-82 — CROSSOVER-REPLICATION-RESTORES-MONOTONE (limited-memory axis round 31; crossover replication with 12 windows): k\*(2560) = 28 and k\*(3072) = 28 — IDENTICAL, confirming NET-81's non-monotone was sampling variation; the 0.5B chain {16, 20, 24, 28, 28} is properly monotone; the size × context crossover is SHARP between 3072 and 4096. Paper 165 addendum.

- **NET-84 — TAIL-AWARE-MIXED-PRECISION-WORKS (limited-memory axis round 32; mixed-precision cell): keeping L22/L23 at fp32 while quantizing all other layers to GPTQ 4-bit gains +1.8 pts over full 4-bit (0.926 vs 0.908 retained); tail-only quantization costs 2.3% (0.977); P1 CONFIRMED, P2 REFUTED — the tail DOES benefit from protection; the prescription from three independent lines (epistasis NET-60, unportability NET-54, super-additive interaction NET-83) converges: treat the tail as ONE unit in every optimization dimension — weights, attention, AND precision; memory cost 7.2MB fp32 = 1.4% of 4-bit model. Gate exact. Barriers: (a) clean; (b) clean; (c) confronted; (d) clean; (e) deterministic; (f) clean; (g) fair; (h) DIRECT. Open: 8-bit tail; 1.5B replication; 4096; 7B cell. Paper 166, issue #328.

Assessment v85. 85 experiments (NET-1 through NET-85).
- **NET-87 — CODE-AT-4096-IS-PROTECTED (limited-memory axis round 31; code domain at long context): code knee @4096 is k\*=32 (k=28 fails ~0.976, k=32 passes 0.986) — LOWER than prose's 40; complete code chain {12,16,32}; domain factor narrows at long context (code/prose ≈0.75→0.80); P2 acceleration-universal CONFIRMED; baseline acc 0.677 remarkably high for source code at 4096 tokens. Gate exact; 3 windows stated. Barriers: (a) clean; (b) clean; (c) confronted; (d) clean; (e) deterministic; (f) clean; (g) fair; (h) DIRECT. Open: fine grid 24–32; more domains @4096; 7B cell. Paper 168, issue #330.

Assessment v88. 88 experiments (NET-1 through NET-88).
- **NET-88 — THE-TOKENIZER-TAX-EXPLODES (limited-memory axis round 32; German at long context): German prose at ctx=4096 needs >56 keys — ALL FIVE POINTS FAIL (k=56 retains only 0.976); the +4 fine-step tax becomes ≥+16 at 4096, a 4× AMPLIFICATION matching the increment acceleration; P1 CONFIRMED dramatically, P2/P3 REFUTED; domain shifts and context acceleration are MULTIPLICATIVE — the phase transition magnifies language differences; multilingual agentic workloads face disproportionate KV costs for non-English languages. Gate exact; 3 windows stated. Barriers: (a) clean; (b) clean; (c) confronted; (d) clean; (e) deterministic; (f) clean; (g) fair; (h) DIRECT. Open: French @4096; more languages @4096; 1.5B non-English @4096; 7B cell. Paper 169, issue #332.

Assessment v89. 89 experiments (NET-1 through NET-89).

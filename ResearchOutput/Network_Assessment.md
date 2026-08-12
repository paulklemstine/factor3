# Network/LLM Lab: Honest Assessment & Where a Real Win Could Come From

> Network research loop, opened 2026-08-12 (factoring loop paused). Same rigor
> as the factoring lab: exact measurable laws, honest negative results, all 8
> barriers checked each iteration. Count: 2 experiments, assessment v2.

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

## Where a genuine breakthrough could come from (frontiers)

- **The PR law at real scale.** Does the monotone b*(PR) law survive on a
  small BERT / GPT trained on a real (or synthetic-structured) corpus? If
  yes, PR gives the first *calibration-free* per-layer bit-schedule for LLM
  quantization — a concrete, testable compression win.
- **Joint-aware allocation.** Replace per-layer-isolated sensitivity with a
  joint (leave-all-but-one compounding) measure; the compounding effect
  (barrier f) is the gap between isolated and joint bit-needs. This is likely
  where the real LM win lives.
- **Depth benefit tasks.** Build a task that genuinely needs sequential
  composition (digit addition with carries, recursion) and test whether the
  fixed-budget depth law becomes single-peaked there (and whether LAW-B's
  Phase-I plateau position tracks the task's required compute-in-place).
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

Assessment v2. 2 experiments (NET-1, NET-2).

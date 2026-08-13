# The Toy Depth Law's Perfect Scores Were a Future-Peek Artifact, and the Exit Law Does Not Transfer to a Real LM: A Causality Screen and the First Real-Scale Check (NET-10)

**Program:** Network/LLM research lab — round-net-10 (the loop's rotation directive: real-scale checks; speed axis)
**Date:** 2026-08-13
**Status:** Machine-verified (Part A: ceiling computation on 12k test words; causal re-runs of Dyck-2 s=12/dm48 d∈{1,2}×2 seeds at 6000 steps + extended-budget d=1 through 18k steps; causal re-runs of the order-4 lookup automaton d∈{1,2}×2 seeds; Part B: 4 real causal LMs on 5 Gutenberg novels, dm=64, vocab 4097, ctx 128, 2000 AdamW steps).

## Hypothesis and statement

Two things happened this round, and both came from the same realization while
building the first real-LM experiment:

1. **The toy TF class uses FULL (bidirectional) attention on next-token tasks.**
   At position `t` the model attends to position `t+1` — the very token it must
   output. The answer is literally in the input, so a trivial *copy-the-future*
   circuit (attend to t+1, read its value, map back through the readout) yields
   100% on any deterministic next-token task, and beats the causal ceiling on
   any task with a random next-token component. Every toy "1.0000" — in
   particular the flat-depth-law's load-bearing claim "d=1 = 1.0000 on
   Dyck-2" (NET-8/9) — is suspect as a measurement artifact. **Hypothesis A:
   re-framed causally, the toy depth law's absolute ceilings collapse; the
   flat-depth SHAPE may survive, the 1.0000s were future-peeking.**
2. The loop's rotation directive calls for the **exit law at real small-LM
   scale** (does the norm crossover predict shared-head decodability on a real
   LM, calibration-free dynamic depth schedule?). A real next-token LM REQUIRES
   causal masking. **Hypothesis B: the toy exit law (exit* ≈ crossover, lossless
   early exit at the norm crossover) transfers to a real LM.**

The falsifying horns: (A) causal re-runs reach ~1.0000 anyway (flat-depth is
genuine at the same absolute level); (B) the law holds at real scale
(0.95·full shared-head accuracy at the crossover layer, saving ≈ 50%).

## 1. Part A — the ceiling argument makes the leak airtight

On Dyck-2 the type of a NEW open pair is iid random (uniform over the two open
types). So at any position whose next token is a new open, no causal model can
do better than chance (0.5) on the type. Measured on the 12k test words
(seed 77): **47.8% of next-tokens are opens** ⇒ the best possible causal
accuracy is

  **ceiling = 0.478·0.5 + 0.522·1.0 = 0.7609** (overall).

Full-attention models reached **1.0000 overall**. 1.0 > 0.7609 ⇒ it is
*information-theoretically impossible* for a causal model to match them ⇒ the
full-attention models MUST have read the answer from the input. This is not a
behavioral argument; it is a bound. The future-peek is confirmed.

## 2. Part A — causal re-runs: absolute ceilings collapse, the flat shape survives

Same architecture and budget as NET-8/9 (pre-LN transformer, dm=48, 4 heads,
`is_causal=True`, 6000 AdamW steps), fresh held-out words (seed+77):

| config (Dyck-2, s=12, dm=48) | overall | close_all |
|---|---|---|
| causal d=1 (seeds 0,1) | 0.5572 / 0.5581 | 0.9173 / 0.9180 |
| causal d=2 (seeds 0,1) | 0.5635 / 0.5633 | 0.9258 / 0.9204 |
| **full-attn d=1 (NET-8/9)** | **1.0000** | **1.0000** |

- **The absolute 1.0000 is gone.** Causal d=1 overall is 0.557 (close to but
  below the 0.7609 ceiling: it is imperfect on closes too), close_all 0.917.
- **Extended budget (causal d=1 s0):** close_all 0.9105 → 0.9135 → 0.9207 at
  6k/12k/18k steps — climbing ~1 point per 6000 steps, asymptoting near 0.92,
  still 8 points short of 1.0000 even at **3× the NET-9 budget**. The causal
  deficit is a genuine optimization/scale limitation, not a budget accident.
- **The flat-depth SHAPE survives:** causal d=1 ≈ causal d=2 (0.917 vs 0.926
  close_all; overall 0.557 vs 0.563). Depth still gives nothing — but "nothing"
  is now measured honestly at ~0.56/0.92, not at a copy-inflated 1.0000.

**Deterministic control — the order-4 lookup automaton** (next token fully
determined by the past ⇒ causal ceiling = 1.0; NET-2 reported 1.0000 under
full attention):

| config (lookup, ntok=6, order=4, L=24) | acc |
|---|---|
| causal d=1 (seeds 0,1) | 0.8906 / 0.8807 |
| causal d=2 (seeds 0,1) | 0.8912 / 0.8912 |
| **full-attn (NET-2)** | **1.0000** |

Even where the ceiling permits 1.0, the causal model reaches only ~0.89 at the
same budget — full attention inflated this deterministic task by ~11 points.
Flat-depth survives (d≈1 ≈ d≈2 ≈ 0.89); the absolute ceiling was inflated
there too. So the artifact is NOT limited to random-type tasks: full attention
gave the toy models a shortcut on every next-token task, and the honest causal
re-runs reset the absolute claims.

## 3. Part A — what survives and what is corrected in the toy depth line

- **Corrected:** "d=1 = 1.0000, load-bearing boundary not found" (NET-8/9) was
  a measurement artifact. Causally, d=1 is 0.92 close_all / 0.89 lookup — an
  impressive single layer, but NOT perfect, and the "perfect" framing that
  powered the load-bearing-depth-refutation is withdrawn.
- **Corrected:** the NET-8 transformer-vs-baseline comparison was unfair —
  the windowed-linear baseline was causal (close_all ≈ 0.75) while the
  transformer was full-attention (1.0). With the causal transformer (0.917),
  the comparison is apples-to-apples and **the genuine result survives:
  causal transformer still beats the causal linear baseline by +17pp on
  close_all.** The single-layer stack-top recovery being better than linear
  baselines was real; the "perfect" absolute was not.
- **Survives (shape):** depth-flatness holds causally on both a deterministic
  (lookup) and a random-type (Dyck-2) task — d=1 ≈ d=2 within noise.
- **Survives (mechanism, refined):** close recovery is deterministic given the
  past, so the balance-conditioned retrieval reading still applies to closes;
  the random open-type positions are the part only full attention could score,
  which the toy overall-1.0000 never flagged. NET-7 (Dyck-1) and the
  arithmetic/composition tasks are deterministic (ceiling 1.0) so they are not
  refuted by the ceiling bound, but their absolute scores need the same causal
  screen (only lookup and Dyck-2 have been re-run here).

## 4. Part B — the exit law at real small-LM scale: crossover ≠ decodability

Setup: 5 public-domain Gutenberg novels (Pride & Prejudice, Moby Dick,
Frankenstein, Alice in Wonderland, A Tale of Two Cities; 599,869 words),
lowercased, word-level top-4097 vocab (UNK=0), contiguous windows of 128,
first 90% train / last 10% test. Causal transformer dm=64, 4 heads (head dim
16), d∈{4,8} × 2 seeds, 2000 AdamW steps (batch 48, lr 3e-4). Probe: per-layer
residual-stream norm ‖x_l‖ and shared-head (final untied readout after final
LayerNorm) next-token accuracy on 256 test windows; `crossover_layer` = first l
with two consecutive ≥2% norm growths; `exit*` = first l with shared-head acc
≥ 0.95·full; `lossless@cross` = acc[crossover] ≥ 0.95·full.

| model | teacc | teloss | cross | exit* | \|exit*−cross\| | lossless@cross | saving |
|---|---|---|---|---|---|---|---|
| d=4 s0 | 0.1571 | 5.119 | 2 | 4 | 2 | No | 0% |
| d=4 s1 | 0.1577 | 5.106 | 2 | 4 | 2 | No | 0% |
| d=8 s0 | 0.1619 | 5.079 | 3 | 8 | 5 | No | 0% |
| d=8 s1 | 0.1620 | 5.081 | 4 | 7 | 3 | No | 12% |

**exit-law-at-real-scale |exit*−cross| ≤ 1 in 0/4.** The toy law does NOT
transfer.

- **Norm profile is reset-then-grow, not flat-then-grow.** On the real LM the
  norm DIPS in the first layers (e.g. d=8 s0: 10.98 → 8.41) then grows
  monotonically (→ 14.95). The toy two-phase law (flat ≈ d/2 then growth)
  does not describe real-text training at this scale; the crossover detector
  fires early (l=2–4) on the dip-recovery growth.
- **Crossover = onset, not completion.** Shared-head acc climbs monotonically
  through the full depth in all 4 models (e.g. d=8 s0: 0.025→0.038→0.053→0.133
  →0.133→0.137→0.142→0.150→0.164). The big jump lands AT the crossover layer
  (0.053→0.133 at l=3 = cross), but accuracy keeps rising, and the 0.95·full
  bar is only crossed at (or one from) the final layer. Every layer contributes
  to next-token quality on real text — there is no free early-exit plateau.
- **Bar sensitivity (measurement honesty):** at a 0.90·full bar, d=8 s0 gives
  exit*=7 (still 4 past crossover); at 0.80·full it gives exit*=3 (≈ crossover,
  saving 63%). So the crossover does mark where decodability starts, but
  "lossless" (95%) early exit is a toy-scale phenomenon. The
  calibration-free-dynamic-depth-schedule idea is not supported at real-LM
  scale: the toy crossover is not a usable trigger for a lossless inference cut.
- **The LM is real but small.** teacc 0.157–0.162 (chance ≈ 0.0002, loss 5.08
  vs ~8.3 random) — a genuinely functional word-level model, and the exit-law
  negative is measured where it matters (real text, causal masking), with the
  caveat that dm=64 is far below production scale.

## 5. Verification vs the network-loop barriers

- **(a) Circularity — no.** The ceiling bound (0.7609) is computed from the
  generator's randomness on fresh test words; the causal re-runs inject nothing.
- **(b) Known-method-in-disguise — the leakage finding is a measurement
  correction, and the real-LM negative is new.** Catalog scan (698 packages,
  alethean.org/package_index.js): no prior work on the full-vs-causal
  attention confound for next-token toy tasks, nor on the exit law at real-LM
  scale; "causal" and "depth" packages exist but none cover this angle.
- **(c) Toy-scale — confronted head-on.** Part B IS the real-scale check; the
  first one fails the toy law. Part A's ceiling argument is scale-free.
- **(d) Data leakage — the finding.** The toy models were trained/evaluated
  with the answer token in the input (full attention on next-token); proven by
  the ceiling bound and confirmed by the causal re-runs. All NET-10 measurements
  use causal masking and contiguous (no-overlap) train/test splits.
- **(e) Variance — 2 seeds × every config.** Causal Dyck-2: 4/4 models in the
  same band (0.557–0.564 / 0.917–0.926); causal lookup: 0.881–0.891; Part B:
  all four agree the law fails (0/4 within ±1).
- **(f) Measurement — documented.** Ceiling computed on the actual test-set
  token mix; extended-budget curve (6k/12k/18k) shows the close_all asymptote;
  Part B bar sensitivity reported at 0.95/0.90/0.80. One harness anomaly
  noted (a monitor delivered a phantom d=8 s0 event with wrong numbers; the
  real line in the log was used — no data affected).
- **(g) Baseline fairness — corrected, and the genuine part survives.**
  NET-8's +25pp vs the windowed-linear baseline mixed a causal baseline with a
  full-attention transformer; re-run causally the transformer still wins +17pp
  on close_all (0.917 vs 0.75) — now a fair comparison.
- **(h) Practical relevance — the negative is the win.** The toy depth line's
  load-bearing claim was running against a self-made-easy task; correcting it
  redirects effort to honestly hard targets (causal close recovery at scale,
  non-positional bindings). And the exit-law negative retires the
  calibration-free dynamic-depth-schedule idea at real-LM scale before anyone
  builds on the toy version.

**Verdict.** NET-10 (real-scale rotation): (1) the toy depth line's perfect
scores were a full-attention future-peek artifact — proven by an information
bound (Dyck-2 causal ceiling 0.7609 < 1.0000) and confirmed by causal re-runs
on two task classes (lookup 1.0→0.89, Dyck-2 1.0→0.92 close_all), while the
flat-depth SHAPE and the transformer-beats-linear-baseline result survive the
honesty fix; NET-8/9's "d=1 = 1.0000 / load-bearing-boundary-not-found"
claims are revised. (2) The exit law does not transfer to a real causal LM:
the norm crossover marks the onset of shared-head decodability, not its
completion — 0/4 models are lossless (0.95·full) at the crossover, and the
toy's ≈d/2 flat-then-grow norm profile is replaced by reset-then-grow on real
text. Round-net-10. Now 10 network experiments. Assessment v10. Paper NET-10,
issue #105. Scripts: /tmp/exp_net_lm.py, /tmp/exp_net_lookup_causal.py.

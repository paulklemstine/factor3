# Network/LLM Research Lab — Notebook

Programmatic exact-law experiments on neural networks and LLMs, in the same
rigorous style as the factoring lab. Each Part is one experiment of the
network research loop. Assessment file: Network_Assessment.md.

## Part 1 — SPECTRAL-QUANTIZATION (round-net-1 #1, network exp 1, v1, paper NET-1)

**The per-layer bit-need law b*(PR) holds exactly on a generalizing MLP and does NOT transfer to a tiny attention LM — a law with a documented domain.** Hypothesis (compression axis): a trained net's per-layer sensitivity to low-bit post-training quantization is governed by its weight participation ratio PR = (Σσᵢ²)²/Σσᵢ⁴ (effective rank), giving (1) a monotone minimal-bits b*(layer) function of PR, (2) corr(PR, damage) strongly negative, (3) PR-proportional equal-budget allocation beating uniform. Experiment (CPU, PyTorch 2.3.1): two models chosen to GENERALIZE reliably (no grokking) — a 5-layer MLP on a smooth 2D classification task (sin·cos boundary, 30k pts, 70/30 split) and a 2-layer transformer LM (d=48, d_mlp=64, 4 heads) on next-token prediction of a 2nd-order deterministic automaton (25-state rule, 25% held-out sequences) — 3 seeds each; per-layer RTN (round-to-nearest per-row symmetric) quantization at 2/3/4/6 bits with held-out test retention.

**MLP (5 layers, 3 seeds):** bit-need b* is a monotone step of PR — the high-rank bottleneck (PR≈5.4) needs 6 bits in EVERY seed, the rank-1 readout (PR=1.0) needs 2 bits in EVERY seed, mid-rank layers sit between; corr(PR, 3-bit damage) = −0.80/−0.92/−0.90 (mean −0.875); corr(PR, b*) = +0.87/+0.58/+0.94 (mean +0.80). PR-proportional allocation (floor 3 bits) beats uniform-4 at an equal total-bit budget on 2/3 seeds (+2.9/+3.5 pp, and −96/−1120 bits; seed-2 overshoots budget ~8% for +2.1 pp — reported).

**Transformer LM (2 layers, 3 seeds, test 1.0000 — perfectly generalizing):** the law REVERSES — every interior matrix (PR 12–25) is robust at 2 bits (b*=2), while the LOW-PR input embeddings (embed PR 4.4, pos PR 9.4) are the fragile layers (b*=3). Mechanism: per-row RTN at 2 bits has 1 level, collapsing the 5-row embedding to ±max sign patterns. Joint quantization compounds: uniform-2 fails (0.887/0.912/0.589), uniform-3 is essentially lossless (0.996/1.000/0.982) — per-layer isolated sensitivity undercounts joint damage (measurement caveat, barrier f).

**Verdict.** CONFIRMED within class (MLP: exact monotone b*(PR), data-free PR sensitivity estimate, equal-budget allocation win); REFUTED as a blanket transfer (transformer embedding fragility reverses the ordering). New objects: the monotone b*(PR) law, the data-free PR sensitivity estimate, the equal-budget allocation win, and the documented domain boundary + joint-vs-isolated compounding. Barriers (b) acknowledged (sensitivity-based mixed precision is a known family — HAWQ/OBS/GPTQ; the PR-only data-free law and the domain reversal are new), (c) toy-scale acknowledged — real-scale (small BERT) is the next step, (d) clean held-out, (e) 3 seeds × 2 classes, (f) joint-compounding documented, (g) equal-bit budgets (1 overshoot reported), (h) +2–3.5 pp at equal budget on MLP, no win on toy LM.
Now 1 network experiment. Assessment v1. Paper NET-1, issue #96.
Script: /tmp/exp_net_quant.py.

## Part 2 — RESIDUAL-STREAM TWO-PHASE LAW (round-net-2 #1, network exp 2, v2, paper NET-2)

**The fixed-budget depth law is FLAT on attention-solvable tasks, and a trained deep transformer's residual stream obeys a two-phase norm law: flat for the first ≈d/2 layers, then bounded growth.** Hypothesis (depth axis, first depth iteration): at fixed total budget B, held-out accuracy is single-peaked in depth. Experiment (CPU, PyTorch 2.3.1): transformer next-token model (pre-LN, 4 heads, d_mlp=4·d_model) on deterministic automata — Part A: order-4 (6⁴=1296 states), 2 budgets × 4 depths × 2 seeds, exact parameter match (within ±2% of B); Part B: order-3 (216 states), dm=40, depths 4/8/12/16, all trained to test=1.0000, then per-layer stream-norm measurement on held-out sequences.

**Part A — LAW-A (flat depth law):** every one of the 16 (B,d,seed) configs reaches test ≥ 0.98 at the first checkpoint (≤100 steps) and ends at test=1.0000 — even the narrowest deepest (dm=32, 8 layers) ties the widest shallow (dm=180, 1 layer). The single-peaked depth hypothesis is REFUTED: one layer of full attention already reads the whole context, so at fixed budget depth is pure parameter overhead on attention-solvable tasks. A negative law with a useful corollary: depth can only pay where tasks need sequential composition beyond one-hop attention.

**Part B — LAW-B (two-phase residual-stream law):** per-layer ‖x_l‖ is STATIONARY for the first ≈d/2 layers (d=16: 8.3→7.9 over layers 0–6; d=8: 7.9→7.0 over 0–3), then grows monotonically with an *increasing* per-layer ratio in the second half (d=16: 1.06→1.20 across layers 8–15); crossover at l≈d/2 in every seed. Total end/start inflation is nearly depth-INDEPENDENT (2.2–3.3× across d=4…16) — extra depth is absorbed as a longer plateau, not more growth; exponent fits ‖x_l‖≈A·l^a give a≈0.3–0.4 (sub-exponential). Final logit scale is depth-invariant (7.8±0.1 across d=4…16) — the final LayerNorm strips Phase-II growth (readout is numerically depth-safe). Update cosine cos(x_{l-1},dx_l)≈0 (Phase I slightly anti-aligned = holds the norm; Phase II aligned = drives growth); accumulation ratio ‖x_end‖²/Σ‖dx‖² grows 1.27→2.59 with depth (a coherent component beyond random walk). The common "residual norm grows exponentially with depth" intuition is WRONG on this class: growth is bounded, sub-exponential, and positioned at the end of the network.

**Verdict.** The single-peaked fixed-budget depth law is REFUTED on attention-solvable tasks (exactly flat, LAW-A); the depth axis still yields a positive exact law — the two-phase residual-stream norm law with bounded depth-independent inflation and logit-scale invariance (LAW-B1–B4). New objects: the flat-depth negative and the four norm laws. Barriers (b) partial (residual-stream norms studied in mech-interp; the two-phase/depth-independent-inflation/logit-invariance objects are new; Catalog scan 2067 packages found no prior work), (c) toy-scale — real-scale next, (d) clean held-out, (e) 2 seeds Part A / 3 seeds Part B, (f) 100-step speed resolution + batch-mean norms documented, (g) exact parameter match, (h) negative LAW-A (don't buy depth at fixed budget on lookup tasks) + norm-budget diagnostic.
Now 2 network experiments. Assessment v2. Paper NET-2, issue #97.
Scripts: /tmp/exp_net_depth.py, /tmp/exp_net_depth_b.py, /tmp/exp_net_depth_c.py.

## Part 3 — COMPOSITION-DEPTH TRICHOTOMY (round-net-3 #1, network exp 3, v3, paper NET-3)

**On the task class where depth is supposed to matter — sequential composition with hidden intermediates — all three achievable training regimes are depth-FLAT: unlearnable, memorized-without-composition, or solvable at d=1. Depth is gated by error-signal decomposability (credit assignment), not capacity.** Hypothesis (depth axis, follow-up to NET-2's flat law): on a task requiring genuine sequential composition, the fixed-budget depth law becomes non-flat — depth buys steps width cannot. Experiment (CPU, PyTorch 2.3.1): permutation-composition task — input `[x₀, o₁…o_k, END]`, predict `x_k = op_{o_k}∘…∘op_{o_1}(x₀)`, 3 fixed random op-permutations over a 64-alphabet, intermediates x₁…x_{k−1} NOT in context, test = held-out op-strings × fresh x₀ (only a stepwise solution generalizes).

**Leg 1 (hidden + sparse, k=6, 529 train/200 held-out strings):** UNLEARNABLE — d=6 reaches train 0.90–0.94 at 8000 steps (2 seeds) by *memorizing seen strings*, held-out-string test stays at chance (0.023/0.028 vs 0.0156); more training buys memorization, not composition. The final-token loss doesn't decompose over the 6 random-permutation steps.

**Leg 2 (hidden + small, train k≤3 → test k=6 length-gen):** MEMORIZED WITHOUT COMPOSITION — every depth d=1…8 reaches train(k≤3)=1.0000 but length-generalization to k=6 is exactly chance (0.0156) at every depth; the model fits the 39-string lookup and never learns per-op maps.

**Leg 3 (intermediates given, chain-in-context, k=6):** LEARNABLE AND DEPTH-FLAT — d=1 alone reaches held-out-string test=1.0000 (both seeds; d=2/4 also 1.0); once intermediates are context tokens, composition is one-step-per-token and depth is free.

**Verdict.** The depth-benefit hypothesis is REFUTED in the cleanest form: the trichotomy extends NET-2's flat depth law to BOTH sides of task difficulty (easy lookups flat via attention-reading-context; hard composition flat via unlearnable/memorized/depth-free regimes), and the binding constraint is optimization (credit assignment), not capacity. Constructive corollary: to make depth pay, a task whose error signal decomposes over steps (addition carries — next target) is the one regime where a non-flat depth law could live; and when a deep model is stuck, check error-signal decomposability before buying more depth. Barriers (b) partial (memorize-without-compose and length-gen failure known; the trichotomy-as-depth-law, the credit-assignment mechanism, the both-sides framing are new; Catalog scan no prior work), (c) toy-scale → real-scale next, (d) clean held-out strings, (e) 2 seeds on decisive runs / 5-depth chance wall in leg 2, (f) final-token accuracy + chance=1/64 documented, (g) regime comparison only, (h) honest negative + credit-assignment diagnostic + decomposable-error pointer.
Now 3 network experiments. Assessment v3. Paper NET-3, issue #98.
Scripts: /tmp/exp_net_comp.py, /tmp/exp_net_comp2.py, /tmp/exp_net_comp3.py, /tmp/exp_net_comp4.py.

## Part 4 — COPY-SELF BASIN + STOCHASTIC ESCAPE (round-net-4 #1, network exp 4, v4, paper NET-4)

**On LSB-first carry addition with per-digit supervision — the ONE regime NET-3's credit-assignment mechanism predicted could break the flat depth law — the depth law is FLAT in distribution: escape from a depth-independent copy-self basin is a stochastic phase transition gated by scale, not depth; the carry chain is a width/depth-immune bottleneck; length-gen is chance at every depth.** Hypothesis (depth axis, testing NET-3's constructive corollary): at fixed budget B, deeper beats shallower on carry addition (decomposable per-digit error → stepwise solution discoverable → depth finally pays). Experiment (CPU, PyTorch 2.3.1): pre-LN transformer (4 heads, d_mlp=4·d_model, tied embedding, d_model matched per depth to B≈100k±6%), LSB-first base-10 `a+b=c`, n=6 columns, per-digit cross-entropy, teacher-forced decoding with a GO-token shift (copy shortcut adversarial at init: untrained per-digit ≈0.08 < chance 0.1). Part A: d∈{1,2,4}×3 seeds, 8000 steps. Part C: carry-free control. Part D: width rescue (4× budget). Part B: length-gen (train n=3 → test n=4/5/6).

**Part A — the copy-self basin and the flat escape law:** every config sits in the same basin (per-digit ≈ 0.22–0.24, full 0.0, loss ≈ 2.0), identical across depths to three decimals (d=1: 0.2263/0.2252/0.2210; d=2: 0.2294/0.2249/0.2455; d=4: 0.2291/0.2182/0.2257 at st=1000) — a shared attractor where the tied-embedding readout reproduces the previous teacher-forced digit. Escape is abrupt (per-digit 0.23→0.98 within one 1000-step interval) and stochastic. Depth law: FLAT in distribution — escape steps d=1 [5000,3000,6000] median 5000, d=2 [3000,5000,5000] median 5000, d=4 [3000,4000,3000] median 3000; non-monotone at seed level (d=1 s1 escapes at 3000, earlier than d=4 s1's 4000), within-depth spread up to 2× exceeds between-depth differences. Full-mastery reliability mildly favors d=4 (3/3 vs 2/3 for d=1,d=2) but is under-powered (3 seeds). The decisive failure is the CARRY CHAIN, not the digit map: both stuck seeds are per-digit-high/full-low (d=1 s2: per 0.7402/full 0.0068; d=2 s0: per 0.8663/full 0.0991) with correlated errors (per=0.87 ⇒ full would be ≈0.38 if independent; observed 0.09).

**Part C (carry-free control) — the control failed its job, informatively:** carry-free is ALSO basin-trapped (d=2 both seeds per 0.4874/full≈0; d=1 s0 per 0.6062/full 0.0039; d=4 s1 per 0.3195/full 0.0). The basin is not about carries — it is a property of tied-embedding per-digit teacher-forced decoding itself, refuting the "carries are the depth-relevant ingredient" isolation.

**Part D (width rescue) — scale gates escape, not mastery:** 4× budget moves the per-digit escape 2–3× earlier (d=1@400k: st=1000 per 0.24–0.36, st=3000 0.87–0.94, vs 3000–6000 at 100k) but full-number mastery at 400k is LOWER (d=1: 0.4011±0.31 vs 0.9553±0.04 at 100k; d=2 s0: 0.1069), again with correlated carry errors (d=1 s1@400k: per 0.8703/full 0.0923; 0.8703⁷≈0.38≫0.09). Width rescues the digit map, not the carry chain — and can even settle the model INTO the digit-map-without-carry state. Scale is a gate on basin escape, not on the carry-chain bottleneck.

**Part B (length-gen) — the memorize-without-composition wall on arithmetic:** d=2 and d=4 reach train n=3 full=1.0000 (both seeds) yet test n=4/5/6 full=0.0000, per-digit ≈ 0.09–0.16 ≈ chance (1/10) at EVERY depth. Carries do not rescue length generalization; the net memorizes the 1000-pair n=3 space and never learns the carry algorithm. NET-3's leg-2 wall reproduced on the task class that was supposed to break it.

**Verdict.** NET-3's clean prediction — decomposable error makes depth pay — is REFUTED in its clean form: the addition-carry regime is flat in depth in distribution, dominated by a depth-independent copy-self basin and a scale-gated stochastic escape; the carry chain is width/depth-immune; length-gen is chance at every depth. The flat depth law now covers attention-solvable lookups (NET-2), sequential composition (NET-3), and decomposable-error arithmetic (NET-4) — the single-peaked depth picture fails everywhere, and the binding constraint is optimization (here, a flat-loss copy attractor), never capacity. New objects: the copy-self basin (exact plateau, depth- and task-independent), the phase-transition escape, the per-digit/carry-chain dissociation (correlated-error diagnostic per^n ≫ full), and scale-gates-escape-not-mastery. Practical: check for the per≈0.23 plateau before judging a decomposed-error task unlearnable; high-per/low-full = the compositional chain is the failure; train-mastery + chance length-gen = memorize-without-compose regardless of task complexity. Barriers (b) partial (copy shortcuts known; the per-digit copy-self basin, the escape law, and the dissociation are new; Catalog no prior work), (c) toy-scale acknowledged, (d) clean held-out batches, (e) 3/2/2/2 seeds with escape-spread reported, (f) per/full separated, chance=0.1, correlated-error diagnostic, (g) carry-free + width + length-gen controls, (h) honest negative + three diagnostics.
Now 4 network experiments. Assessment v4. Paper NET-4, issue #99.
Script: /tmp/exp_net_add.py (parts A–D; a summary-print variable-shadowing bug — `B` reused as budget int in the PART-D summary loop — was fixed after the run; all data was already in the log, no re-run needed).

## Part 5 — READOUT-UNTIE: THE COPY-SELF BASIN IS A READOUT ARTIFACT; THE CARRY CHAIN IS READOUT-INDEPENDENT (round-net-5 #1, network exp 5, v5, paper NET-5)

**Untying the readout head removes the copy-self basin entirely (escape becomes immediate and depth-flat, 1000–3000 steps vs tied 3000–6000) — confirming NET-4's ‖emb‖² mechanism — but the carry chain is readout-independent (per-high/full-low with correlated errors persists with an untied head), the depth law stays flat even without the basin (full-mastery d=4 3/3, d=1 2/3, d=2 1/3 — non-monotone, under-powered), and length-gen is still chance at every depth.** Hypothesis (depth axis, NET-4 follow-up): if the copy-self basin is caused by the tied readout's ‖emb‖²-dominated logit for the current teacher-forced token, an UNTIED head (Linear(dm, VOCAB), no weight sharing) removes it; then the decomposable-error depth law becomes measurable without the stochastic-escape confound — and either depth finally pays, or the carry chain is confirmed as the true bottleneck. Experiment (CPU, PyTorch 2.3.1): identical to NET-4 except the readout — pre-LN transformer (4 heads, d_mlp=4·d_model, UNTIED head), LSB-first base-10 `a+b=c` n=6, per-digit cross-entropy, GO-shift teacher forcing, d_model matched to B≈100k±6% accounting for the extra head weights (untied d=1: dm=88 B=98.5k; d=2: dm=64 B=103.2k; d=4: dm=44 B=97.4k). Part A: untied, d∈{1,2,4}×3 seeds, 8000 steps. Part B: tied control (4000 steps, same seeds) to confirm the basin reproduces. Part C: untied length-gen (train n=3 → test n=4/5/6).

**Part A — untying eliminates the basin (mechanism confirmed):** escape steps (per-digit ≥ 0.5): d=1 [1000,1000,1000], d=2 [2000,2000,1000], d=4 [2000,3000,2000] — every untied seed escapes at st ≤ 3000 vs tied 3000–6000; per-digit at st=1000 is already 0.60–1.00 vs the tied 0.22–0.24 plateau at every depth. The ‖emb‖² copy shortcut is broken by untying — per-digit learning starts immediately. NET-4's mechanism is CONFIRMED: the copy-self basin is a tied-readout artifact.

**Part A — the carry chain is readout-independent (the bottleneck persists):** removing the basin does not rescue the full-number solution. Three of nine untied configs sit in the same per-high/full-low state with the identical correlated-error signature: d=1 s0 per 0.8735/full 0.1143 (per^7=0.3880 ≫ 0.1143), d=2 s0 per 0.7499/full 0.0112 (per^7=0.1334 ≫ 0.0112), d=2 s2 per 0.8727/full 0.1089 (per^7=0.3855 ≫ 0.1089). The model learns the columnwise digit map (per ≈ 0.75–0.87) and cannot chain the carry — the carry chain is the genuine sequential-composition bottleneck, unchanged by untying.

**Part A — the depth law stays flat even with the basin removed:** full-mastery at 8000 steps: d=1 2/3 (s1, s2 = 1.0; s0 = 0.1143), d=2 1/3 (s1 = 1.0; s0 = 0.0112, s2 = 0.1089), d=4 3/3. Escape timing is now trivially depth-flat (all depths 1000–3000 — the NET-4 depth differences in escape were basin-escape-driven). Full-mastery reliability is still NOT a clean depth law: d=4 3/3 but d=1 2/3, d=2 1/3 — non-monotone, under-powered at 3 seeds. Removing the basin did NOT expose a clean non-flat depth law; it exposed that the remaining failure — the carry chain — is equally depth-immune.

**Part B (tied control) — the basin reproduces:** at 4000 steps the tied readout at the same seeds shows the basin again (d=1 [inf, 3000], d=2 [3000, inf] with final per 0.4964 ≈ plateau, d=4 [3000, inf]) — the untie treatment is the only difference at equal budget.

**Part C (length-gen) — chance at every depth, basin gone:** untied d=2 and d=4 reach train n=3 full=1.0000 (both seeds) but test n=4/5/6 full=0.0000, per ≈ 0.09–0.18 ≈ chance at every depth — the memorize-without-composition wall reproduced with the basin removed. d=1 untied does not even master train n=3 (full 0.0981/0.0996; per 0.77 — the carry-chain dissociation, exactly Part A's d=1 s0). Removing the basin does not help the model learn or extrapolate the carry algorithm.

**Verdict.** The mechanism hypothesis is CONFIRMED (the copy-self basin is a tied-readout artifact; untying removes it — the first positive architectural cure in the depth series) and the deeper hope behind it is REFUTED (with the basin gone, escape is trivially depth-flat and the carry chain, not the basin, was the binding constraint all along). NET-4's central claim survives and sharpens: the decomposable-error regime is now fully decomposed — a removable readout basin (copy-self) layered on an irreducible carry-chain credit-assignment wall, and neither depth, width, nor readout-untying makes depth pay at this scale. Practical diagnostics: a per-digit-supervised tied-embedding model stuck at a per≈0.22 plateau should try an untied head FIRST (zero-cost artifact cure, and untying immediately starts per-digit learning); a per-high/full-low state AFTER untying is the carry chain, which depth/width do not buy — do not attack it with more layers. Barriers (b) partial (untied embeddings standard; the cure-for-copy-basin, the readout-independence of the carry dissociation, and the negative that untying does not unlock depth are new; Catalog no prior work), (c) toy-scale acknowledged, (d) clean held-out batches, (e) 3/2/2 seeds with escape-spreads reported, (f) per/full separated, chance=0.1, correlated-error diagnostic per^7 vs full, budget matched WITH extra head weights ±6%, (g) within-run tied control at equal budget/same seeds, (h) real diagnostic + honest negative.
Now 5 network experiments. Assessment v5. Paper NET-5, issue #100.
Script: /tmp/exp_net_untie.py.

## Part 6 — DECODABILITY-CROSSOVER EXIT LAW (round-net-6 #1, network exp 6, v6, paper NET-6, speed axis)

**The layer where a trained transformer's final readout becomes linearly decodable (shared-head exit accuracy ≥ 0.98) coincides with the residual-stream Phase-I/II norm boundary to within one layer — |exit*−crossover| ≤ 1, exit* ≈ d/2 — so the network can be exited at the norm-predicted crossover with zero accuracy loss, a depth-proportional ~50% inference saving, no confidence gate, and the saving grows with depth.** Hypothesis (speed axis — first speed iteration, untouched until now): NET-2's two-phase law (‖x_l‖ stationary for l < ≈d/2, then growth; final LayerNorm strips the growth) marks a compute/amplify boundary — Phase I is compute-in-place (NOT yet decodable by the trained head), Phase II is amplification (decodable from the crossover on); hence exit at the crossover is lossless and the exit layer is predictable a priori (≈ d/2). Falsifying horn: if Phase I is already decodable, the plateau is trivial waiting and you could exit near layer 1. Experiment (CPU, PyTorch 2.3.1): NET-2 automata — order-4 (1296 states) and order-3 (216 states), dm=40, 4 heads, ctx=12, d∈{4,8,16}×2 seeds each = 12 models, all trained to held-out test 1.0000. For each: per-layer stream norms, Phase-II onset (crossover), and shared-head exit accuracy (trained final lnf+un applied to each frozen LN(x_l)); exit* = first layer ≥ 0.98.

**Part A/B — the exit law (12/12 within one layer of the boundary):** exit*−crossover ∈ {−1, 0, +1} in ALL 12 (mean −0.25); exit*−d/2 ∈ {−1, 0, +1} (mean +0.5). The decodability cliff is sharp: l=exit*−1 acc 0.767–0.978 (mean 0.926, always < 0.98), l=exit* acc 0.980–1.000; accuracy climbs from near-chance at the embedding to fully usable across the single boundary step. Representative rows: o4 d=8 s0 exit*=5 (l=4 0.9371→0.9967) crossover=6; o4 d=16 s0 exit*=7 (l=6 0.9224→0.9815) crossover=8; o3 d=16 s0 exit*=9 (l=8 0.9780→0.9989) crossover=8.

**Part C — the saving is real, grows with depth, and fixed exit beats dynamic exit:** compute fraction exit*/d: d=4 → 0.75 (25% saving), d=8 → 0.62/0.50 (38–50%), d=16 → 0.44–0.56 (44–56%, median ≈ 50%). Exiting at exit* is lossless (exit* acc ≥ 0.98 vs full test 1.0000; gap ≤ 0.02, usually 0.0000–0.0002). NEW NEGATIVE: confidence-threshold dynamic exit does NOT capture the saving — mean per-token max-softmax-prob at the decodable layer is 0.70–0.96 (mean 0.80), so a 0.999 gate would fire only after the exit layer on nearly every sequence. The fixed, architecturally-predicted exit (no confidence gate, no extra head) is the artifact.

**Verdict.** CONFIRMED in usable form, REFUTED at both sharp extremes. (i) exit* is a-priori predictable ≈ d/2 (12/12 within ±1), lossless, saving 25%→50% with depth. (ii) the two-phase boundary marks decodability (|exit*−crossover| ≤ 1, 12/12). (iii) REFUTED "Phase I not decodable": exit* < crossover in 3/12; exit*−1 acc 0.77–0.98 — the signal forms THROUGH Phase I and crosses the usability bar exactly at the boundary. (iv) REFUTED "Phase I already decodable": exit* ≈ d/2, never near layer 1 — the plateau is not trivial waiting. (v) NEW NEGATIVE: confidence-gated dynamic exit is not the lever; the fixed norm-predicted exit is. MECHANISM pinned: Phase I = compute-in-place whose output becomes usable exactly at the boundary; Phase II = readout-amplification of an already-formed representation — which is exactly why the final LayerNorm can strip the growth (NET-2) and the second half is skippable. Barriers (b) partial (early-exit nets/probes known; exit-predicted-by-norm-crossover + fixed-beats-dynamic + depth-scaling new; Catalog 2067 packages no prior work), (c) toy-scale → real-LM next, (d) clean held-out 20%, all test 1.0, (e) 2×2×3 with the ±1 spread reported honestly, (f) exit acc = shared-head next-token acc, 0.98 bar consistent with NET-2, crossover = sustained-2 transitions ≥1.02, saving = layer-compute fraction, (g) full-model baseline + measured confidence-gate baseline that fails, (h) real lever: halve inference depth on sequential tasks with zero adaptation, predictor computable in training.
Now 6 network experiments. Assessment v6. Paper NET-6, issue #101.
Script: /tmp/exp_net_speed.py (imports NET-2's TF/aut_data via importlib so part_a/part_b do not re-run; initial exec-based draft re-ran NET-2 and was killed).

## Part 7 — EXIT-TRACKS-TASK-DIFFICULTY: DEPTH FLAT ON GRAMMAR, EXIT FAR BELOW d/2 (round-net-7 #1, network exp 7, v7, paper NET-7, speed axis)

**The load-bearing-depth test of NET-6 FAILED at this scale — Dyck-1 (balanced-paren next-token, semilength 12, nesting ≤12) is attention-solvable: d=1 reaches test=1.0000 at EVERY balance bin including b4+ (deep nesting 4–10), so depth is FLAT on the canonical grammar task too. The exit law is REFINED: exit* is depth-INDEPENDENT ({2,3,4} across d=4..16) and tracks task difficulty, not d/2 — d=16 exits at layer 4/16 (75% saving, lossless within the 0.95 bar), vs ≈50% on NET-6's automata; |exit*−crossover| ≤ 1 in 17/18 across both task classes, but lossless-at-crossover holds only 3/6 here (the crossover is much earlier on easy tasks and exit* lags it 1–3 layers).** Hypothesis (speed axis round 2, testing NET-6's open question): NET-6's exit*≈crossover≈d/2 was measured on attention-solvable automata (flat depth) — does the law hold, or fail (lossless exit impossible), on a task where depth is genuinely load-bearing? Task: Dyck-1 next-token prediction — the classic grammar where sequential stack state must be tracked and shallow transformers are supposed to fail at deep nesting. (1) Does depth pay? (2) Is the exit law universal or bounded? Experiment (CPU, PyTorch 2.3.1): pre-LN transformer (dm=48, 4 heads, untied readout), uniform random balanced strings semilength 12, 100k train/20k held-out (fresh seed), budget 6000 AdamW steps; next-token accuracy overall + by running-balance bin (b0..b4+); shared-head exit (trained final lnf+un on frozen LN(x_l)), exit* = first layer ≥ 0.95 (=0.95·full since all full=1.0); crossover = first l with two sustained norm ratios ≥ 1.02.

**Part A — depth is FLAT on Dyck-1 (grammar):** all 10 models (d∈{1,2,4,8,16}×2 seeds) reach test=1.0000 at every balance bin, including b4+ (nesting up to 10). d=1 alone solves all nesting — the balance is a cumulative sum and one attention head computes it while another conditions the next token. The "shallow fails at deep nesting" expectation is a width/context-starved artifact, not this scale. The flat-depth law now covers FOUR task classes: lookups (NET-2), composition (NET-3), decomposable-error arithmetic (NET-4/5), grammar (NET-7). The load-bearing-depth premise REFUTED at this scale — genuinely open.

**Part B — the exit layer tracks task difficulty, not d/2:** exit* ∈ {2,3,4} for all six configs (d=4..16): d=4 s0 3 (l=2 0.7075→1.0000), d=4 s1 2 (0.6733→0.9613), d=8 s0 3 (0.5942→1.0000), d=8 s1 2 (0.6409→0.9737), d=16 s0 4 (0.7806→0.9927), d=16 s1 4 (0.8130→0.9814). exit* is depth-INDEPENDENT (does not scale with d at all) and ≪ d/2 (d/2 = 2/4/8); crossover ∈ {1,2,3} (also ≪ d/2). The computation finishes in 2–4 layers regardless of total depth — the rest is dead weight. SAVING: 25–50% at d=4, 62.5–75% at d=8, 75% at d=16 (median ≈ 75% vs NET-6's ≈ 50%). exit*−crossover = {0,−1,+1,0,+1,+3} → |·| ≤ 1 in 5/6 (17/18 combined with NET-6); one +3 outlier (d=16 s1: crossover=1, exit*=4 — norm grows immediately but decodability lags). REFINEMENT of NET-6: lossless-at-crossover holds only 3/6 here (vs essentially all in NET-6) — on the easy task the crossover is much earlier and exit* lags it 1–3 layers; the reliable trigger is the fixed 0.95 bar (exit at the first usable layer), which fires far below d/2 on easy tasks.

**Verdict.** NET-6's "exit* ≈ d/2" is CORRECTED to its proper scope: the universal object is **exit* ≈ crossover with the crossover TASK-DEPENDENT** (≈d/2 on harder automata whose compute fills Phase I, ≈1–3 on easy grammar) — EXIT-TRACKS-TASK-DIFFICULTY. And the load-bearing-depth test where the exit law could have had a boundary was NOT achieved: bounded Dyck-1 at dm=48 is attention-solvable (depth flat, d=1 perfect at all nesting). Practical consequence is bigger, not smaller: on easy-to-moderate sequential tasks a trained transformer's inference depth can be cut ~75% (exit at layer 2–4 of 16) losslessly, no confidence gate. Barriers (b) partial (early-exit known; task-difficulty dependence of the exit layer + the correction of the ≈d/2 claim + grammar-flatness are new; Catalog no prior work), (c) toy-scale AND the finding — the load-bearing test needs Dyck-2 (multi-type) / width-starved / unbounded nesting, (d) fresh held-out strings seed+77, all 1.0000 before probing, (e) 2 seeds × 5 depths + 2×3 exit, +3 outlier reported not averaged, (f) exit acc shared-head next-token, bar 0.95 = 0.95·full (full=1.0), crossover sustained-2 ≥1.02, saving = layer-compute fraction, by-balance exit (Part C) moot since every bin is 1.0000 at every depth, (g) full-model baseline at 1.0000, exit* gap ≤ 0.04, (h) real lever: up to 75% lossless inference-depth cut on easy sequential tasks, predictor measurable in training.
Now 7 network experiments. Assessment v7. Paper NET-7, issue #102.
Script: /tmp/exp_net_speed2.py.

## Part 8 — DEPTH FLAT ON NON-REGULAR GRAMMAR (Dyck-2): LOAD-BEARING TEST FAILS A THIRD TIME; EXIT LAW HOLDS ON A THIRD TASK CLASS; SINGLE-LAYER STACK-TOP RECOVERY IS GENUINE (round-net-8 #1, network exp 8, v8, paper NET-8, depth axis)

**The load-bearing-depth test of NET-7 via the canonical NON-REGULAR CFG FAILED — Dyck-2 (two bracket types '(' vs '[', next-token, semilength 12, dm=48) is attention-solvable: d=1 reaches test=1.0000 at EVERY balance bin AND every close-position diagnostic (close_all=1.0000, close_b4+=1.0000), i.e. a single layer recovers the TYPE of the top of the stack (the last unmatched open's bracket type; chance 0.5 given only the balance) at every depth and every close number — the two-layer "balance-in-L1/select-in-L2" construction is NOT needed. The exit law holds on a THIRD task class: exit* ∈ {3,4,5} depth-saturated (d=16 exits at 3–5/16 = 69–81% lossless saving, d=8 at 4–5/8 = 37.5–50%, d=4 at 3/4 = 25%), |exit*−crossover| ≤ 1 in 5/6 (22/24 across all three classes; one +3 outlier d=16 s0 cross=2 exit*=5), exit* ≥ crossover in 5/6, lossless-at-crossover 4/6 (both d=4, both d=8) failing exactly on the two d=16 models whose crossover fires at l=2 — confirming NET-7's refinement that the FIXED 0.95 usability bar, not the norm, is the reliable trigger when the crossover fires ≤2. Mechanism (barrier g): windowed linear baselines (last-K tokens + balance + position, K∈{4,8,12}, 3 epochs) cap at close_all 0.7322/0.7544/0.7518 — never reaching 1.0 even when the matching open is inside the window — because a linear map cannot route the CONDITIONAL index "if the trailing run is k closes deep, read the open at distance 2k−1" for all k at once (needs gating/products); attention can (balance-conditioned position match). Transformer beats the strongest windowed baseline by +25pp on close_all and is 1.0 vs 0.97 at close_b6+. The deep-balance bins rise on the baselines for a measurement reason (the b6+ bin is dominated by FIRST closes of deep runs, locally covered) — close_all is the honest hard-close diagnostic.** Hypothesis (depth axis round 6): Dyck-2's stack-top type is a history-dependent discrete state, so recovering it should need layer 2 (L1 computes balance, L2 selects+reads the last open) — the first genuinely LOAD-BEARING depth regime, and the exit law's first potential boundary (a depth-using model should NOT be exitable losslessly). Falsifying horn: single layer both tracks balance and routes each close to its matching open. Experiment (CPU, PyTorch 2.3.1): pre-LN transformer (dm=48, 4 heads, untied readout) on uniform Dyck-2 words (rejection-sample uniform balanced ±1 shape, iid per-pair round/square types; tokens 0='(' 1=')' 2='[' 3=']'), 100k train/20k fresh held-out, 8000 AdamW steps; next-token acc overall + by-balance bin + close-position diagnostics (close_all, close_b4+); shared-head exit on d∈{4,8,16}×2 seeds, exit* = first layer ≥ 0.95·full.

**Part A — depth is FLAT on Dyck-2 (non-regular grammar):** all 10 models (d∈{1,2,4,8,16}×2 seeds) reach test=1.0000 at every metric: overall, b0–b4+, close_all, close_b4+, open_all. d=1 alone solves stack-top-type recovery — one attention layer computes the balance AND selects the last unmatched open's type for every close, including closes whose matching open sits 11+ tokens back (close_all=1.0 = every k-th close of every run). The flat-depth law now covers FIVE task classes: lookups (NET-2), composition (NET-3), decomposable-error arithmetic (NET-4/5), Dyck-1 regular grammar (NET-7), Dyck-2 non-regular CFG (NET-8). The load-bearing-depth premise REFUTED a third time at this scale — genuinely open; next escalation = semilength scaling / width-starved Dyck / unbounded nesting.

**Part B — the exit law holds on a third task class:** exit* = {3,3,5,4,5,3} for (d,s)∈{4,8,16}×{0,1}: d=4 s0 3 (l=2 0.6903→1.0000), d=4 s1 3 (0.6477→0.9654), d=8 s0 5 (0.8875→0.9988), d=8 s1 4 (0.6097→0.9901), d=16 s0 5 (0.9237→0.9843), d=16 s1 3 (0.6314→0.9725). crossover = {3,4,5,4,2,2}; d/2 = {2,2,4,4,8,8}. exit* is depth-SATURATED (does not scale with d): 25% saving at d=4, 37.5–50% at d=8, 69–81% at d=16, all lossless within the 0.95 bar (exit* acc 0.9654–1.0000 vs full 1.0000). |exit*−crossover| ≤ 1 in 5/6 → 22/24 across NET-6 (12 automata) + NET-7 (6 Dyck-1) + this (6 Dyck-2); the +3 outlier (d=16 s0 cross=2 exit*=5) is the same class as NET-7's. exit* ≥ crossover in 5/6. lossless-at-crossover 4/6: True for all four d∈{4,8} models, False for both d=16 (crossover at 2, exit* lags 3) — exactly NET-7's refinement: the fixed 0.95 bar, not the norm, is the reliable trigger when the crossover fires very early. NET-6's "exit ≈ d/2" is now conclusively scoped — it held only on the harder automata whose compute fills Phase I.

**Part C — the single-layer success is genuine (barrier g):** windowed linear baseline (last-K tokens + balance + position → next token, linear, 3 epochs, same held-out data): K=4 close_all 0.7322 / b5+ 0.9330 / b6+ 0.9646; K=8 0.7544 / 0.9619 / 0.9753; K=12 0.7518 / 0.9315 / 0.9663. Widening the window from K=4 to K=12 (covers matching opens up to distance 11 = closes #1–#6) barely moves close_all — a linear map cannot conditionally index the matching open for varying run depth; attention's balance-conditioned position selection can. Transformer 1.0000 at every metric vs baseline max 0.7544 close_all: +25pp genuine long-range content. Honest caveat: the deep-balance bins rise on the baselines because they are dominated by FIRST closes of deep runs (locally covered) — close_all is the honest hard-close diagnostic, and there the gap is clean.

**Verdict.** NET-8 (depth axis round 6): (1) the load-bearing test fails a THIRD time — depth is FLAT on the canonical non-regular CFG (d=1 perfect at every balance and every close position; flat-depth law now five task classes); (2) the exit law holds on a THIRD task class — exit* depth-saturated {3,4,5}, |exit*−crossover| ≤ 1 in 22/24 across three classes, 69–81% lossless inference saving at d=16, NET-7's fixed-bar refinement confirmed; (3) single-layer stack-top recovery is GENUINE — the strongest windowed linear baseline (K=12) caps at close_all 0.75 vs the transformer 1.0, because the conditional index "k-th close → open at distance 2k−1" needs gating that a linear map lacks and attention provides. The load-bearing regime and the exit law's practical boundary remain open — decisive next = semilength scaling (where does d=1 break?), width-starved Dyck (dm=16/1 head), unbounded nesting, exit law at real-LM/BERT scale. Barriers (b) partial (stack-recovery in one layer related to known circuits; the five-class flat law + depth-saturated exit + quantified baseline margin are new; Catalog no prior work), (c) toy-scale AND the finding, (d) fresh held-out seed+77, all 1.0000 before probing, (e) 2 seeds × 5 depths + 2×3 exit, +3 outlier and 2/6 lossless-at-cross failures reported not averaged, (f) exit acc shared-head next-token, bar 0.95·full (full=1.0), crossover sustained-2 ≥1.02, saving = layer-compute fraction, close bins reported WITH the first-close-of-deep-run caveat, (g) strongest windowed linear baseline (K up to 12 + balance + pos) loses by +25pp, (h) real lever: 69–81% lossless inference-depth cut on non-regular grammar + a genuine caution that single-layer transformers solve canonical stack recovery at this scale.
Now 8 network experiments. Assessment v8. Paper NET-8, issue #103.
Script: /tmp/exp_net_dyck2.py.

## Part 9 — THE LOAD-BEARING BOUNDARY IS NOT FOUND: DEPTH FLAT ACROSS CONTEXT AND WIDTH SCALING OF Dyck-2; SINGLE-LAYER SOFT ATTENTION IMPLEMENTS A BOUNDED STACK (round-net-9 #1, network exp 9, v9, paper NET-9, depth axis)

**Following NET-8's flatness on Dyck-2 at semilength 12/dm48, the load-bearing boundary (where a single layer breaks and d=2 finally pays) is NOT found across either scaling direction: d=1 reaches test=1.0000 at every metric on all 16 models — Part A semilength s∈{16,32} (context 32/64 tokens, matching opens up to 63 tokens back) at dm=48, d∈{1,2}×2 seeds; Part B width dm∈{16,12} (head dim 4 and 3) at s=12, d∈{1,2}×2 seeds. The non-flat screen found NO config with d=1 < d=2 (close_all gap > 0.01), so the shared-head exit branch was correctly not triggered (there is no depth-using model to exit).** Hypothesis (depth axis round 7): at larger semilength the balance spans more levels and closes route to opens at distance up to 2s−1 — at some s one layer runs out of capacity; and at dm=16/dm=12 a single layer must hold BOTH the balance prefix-sum AND the balance-conditioned position routing, so d=2 (stack the subtasks) should win. Falsifying horn: single-layer soft attention implements a bounded stack — balance-pointer + content-retrieval at the pointed position — so depth stays flat across both scaling directions at our scale. Experiment (CPU, PyTorch 2.3.1): pre-LN transformer TFX(4, dm, 4, d, 2·s), uniform Dyck-2 words (rejection sampling, iid per-pair types), 60k train/12k fresh held-out (seed+77), 6000 AdamW steps (≥12 epochs at s=32, 49M tokens), diagnostics overall + close_all (every k-th close of every run — the honest hard-close diagnostic) + close_b4+.

**Part A — depth FLAT across context scaling:** all 8 models (s∈{16,32} × d∈{1,2} × 2 seeds) test=1.0000 at overall/close_all/close_b4+. d=1 is perfect even at semilength 32: the balance ranges over 32 levels and closes route to matching opens up to 63 tokens back — single-layer long-range stack-top retrieval at dm=48. Context length is NOT the boundary. **Part B — depth FLAT across width scaling:** all 8 models (dm∈{16,12} × d∈{1,2} × 2 seeds) test=1.0000 at every metric. d=1 is perfect even at dm=12 (4 heads → head dim 3): one narrow layer still holds the balance AND routes every close to its matching open's type. Width is NOT the boundary either. Combined: the flat-depth law on the non-regular grammar survives BOTH scaling directions affordable on CPU (context ≤64, width ≥12). **Part C — the non-flat screen:** "No config with d=1 < d=2 (close_all gap > 0.01) — depth FLAT again across s in {16,32} and dm in {16,12}." Every pair equal at 1.0000.

**Mechanism — why a single layer implements the bounded stack:** the stack-top STATE of a bounded Dyck word IS the scalar running balance, and the stack-top CONTENT is positionally stored. A close at t must read the last open at balance-depth balance_before(t)−1; single-layer attention realizes this: one head accumulates the balance (prefix-sum), a second routes each close query to the matching-open position by balance-conditioned key match + recency (last such open), and reads the stored type. A balance pointer plus content retrieval — no second layer needed because the state is scalar and the content is at a computable position. The boundary would need (a) balance range exceeding dm precision (s≫64), (b) unbounded nesting / length-gen (a different axis — NET-4's wall), or (c) stack CONTENT that is NOT positionally retrievable (non-positional long-range binding — content computed from multiple distant positions; the genuinely hard case and the natural next load-bearing target).

**Verdict.** NET-9 (depth axis round 7): the load-bearing boundary is NOT found at context ≤64 / width ≥12 — the flat-depth law now covers five task classes AND holds across context and width scaling on the non-regular grammar; the explicit mechanism reading is single-layer soft attention = bounded stack (scalar balance pointer + positional content retrieval). Genuinely open load-bearing candidates: non-positional stack content, s≫64, unbounded nesting, and the real-scale checks on the other axes (exit law / PR law on a small LM). Barriers (b) related circuits acknowledged (attention-as-bounded-stack is mech-interp folklore; the scaling-sweep negative + five-class × context × width flatness are new; Catalog 698 packages no prior work), (c) toy-scale AND the finding, (d) fresh held-out seed+77, all 1.0000 before probing, (e) 2 seeds × every config, 16/16 consistent, (f) documented diagnostics + budget (≥12 epochs at s=32); two script bugs both post-data and fixed (SUMMARY re-print 4-vs-3 tuple unpack fired after all models done, no data loss; Part C RA 4-tuple lookup fell to RB arm so the (16,48)/(32,48) pairs were verified EQUAL by direct inspection of printed lines — all 1.0000 both depths, automated screen covered dm∈{16,12}, verdict correct over all 16), (g) inherited from NET-8 (windowed linear baseline −25pp, no depth gap appears here), (h) honest negative with a target: depth gives nothing on bounded-stack grammar at every affordable scale; non-positional bindings / much larger context / real-LM checks are the standing candidates.
Now 9 network experiments. Assessment v9. Paper NET-9, issue #104.
Script: /tmp/exp_net_dyck2_scale.py.

## Part 10 — THE TOY DEPTH LAW'S PERFECT SCORES WERE A FUTURE-PEEK ARTIFACT (CAUSALITY SCREEN), AND THE EXIT LAW DOES NOT TRANSFER TO A REAL LM (round-net-10 #1, network exp 10, v10, paper NET-10, real-scale rotation)

**Building the first real-LM experiment exposed a confound in every toy depth result: the TF class uses FULL (bidirectional) attention on next-token tasks, so at position t the model attends to position t+1 — the very token it must output. The answer is in the input; a copy-the-future circuit yields 100% on any deterministic next-token task. The leakage is PROVEN by an information bound: on Dyck-2, new-open types are iid random and 47.8% of next-tokens are opens, so the best causal accuracy is ceiling = 0.478·0.5 + 0.522·1.0 = 0.7609 overall — full-attention's 1.0000 is impossible causally, QED.** Part A re-ran the toy tasks with `is_causal=True` at the same architecture/budget (6000 steps, dm=48, fresh held-out seed+77): causal Dyck-2 d=1 reaches overall 0.557 / close_all 0.917 (d=2: 0.563 / 0.926) vs the recorded full-attention 1.0000; extended budget shows close_all 0.9105→0.9135→0.9207 at 6k/12k/18k — asymptoting ~0.92, still 8 points short at 3× budget. Causal lookup (deterministic, ceiling 1.0): d≈1≈d≈2 ≈ 0.89 vs full-attention NET-2's 1.0000 — the artifact is NOT limited to random-type tasks; every next-token task got the shortcut. **What survives the honesty fix:** the flat-depth SHAPE (d=1 ≈ d=2 within noise on both classes — depth genuinely gives nothing); and the transformer-beats-linear result, now fairly compared (causal transformer 0.917 close_all vs causal windowed-linear 0.75, +17pp — the NET-8 +25pp mixed a causal baseline with a full-attention transformer). **What is corrected:** NET-8/9's "d=1 = 1.0000 / load-bearing-boundary-not-found" absolute claims — withdrawn as measurement artifacts; the random open-type positions were the part only full attention could score, which the toy overall-1.0000 never flagged.

**Part B — the exit law at real small-LM scale (the rotation directive's first real-scale check) does NOT transfer.** Real causal GPT on 5 Gutenberg novels (599,869 words, top-4097 word vocab, dm=64, 4 heads, ctx 128, contiguous 90/10 split, d∈{4,8}×2 seeds, 2000 AdamW steps; teacc 0.157–0.162, loss 5.08 vs 8.3 random — a genuinely functional small LM). Per-layer probe: norms show **reset-then-grow** (dip in early layers then monotone growth) — NOT the toy's flat-≈d/2-then-grow; crossover fires early (l=2–4); shared-head acc climbs monotonically through the full depth, with the big jump landing AT the crossover (onset) but the 0.95·full bar crossed only at/near the final layer. |exit*−cross| = 2/2/5/3, **lossless@cross = False in 4/4**, exit-law at real scale 0/4 within ±1. The toy calibration-free dynamic-depth-schedule idea is not supported at real-LM scale: crossover marks where decodability starts growing, not where it's usable (at a 0.80·full bar d=8 s0 would exit at l=3 ≈ crossover, saving 63% — but "lossless" at the honest 95% bar requires full depth).

**Verdict.** NET-10 (real-scale rotation, speed axis): the toy depth line's 1.0000s were a full-attention future-peek artifact (airtight ceiling bound + causal re-runs on two task classes), and the exit law does not transfer to a real causal LM (0/4 lossless at crossover; norm profile reset-then-grow). Barriers: (a) no injection — the ceiling is computed from generator randomness on fresh test words; (b) Catalog (698 packages) has no work on the full-vs-causal next-token confound or the real-LM exit law; (c) confronted head-on — Part B IS the real-scale check and it fails the toy law; (d) the finding — full attention put the answer in the input, proven by 0.7609 < 1.0000; NET-10 uses causal masking and contiguous splits; (e) 2 seeds × every config, all bands consistent; (f) documented — extended-budget asymptote, bar sensitivity (0.95/0.90/0.80), one harness phantom-monitor event ignored (real log line used); (g) corrected — transformer-vs-linear now apples-to-apples (+17pp survives); (h) the negative is the win — it redirects the load-bearing hunt to honestly hard targets (causal close recovery at scale, non-positional bindings) and retires the dynamic-depth-schedule idea at real scale.
Now 10 network experiments. Assessment v10. Paper NET-10, issue #105.
Scripts: /tmp/exp_net_lm.py, /tmp/exp_net_lookup_causal.py.

## Part 11 — THE PR QUANTIZATION LAW DOES NOT TRANSFER TO A REAL LM: ROLE-STRUCTURED BIT-NEED SURVIVES, BUT NO STATIC RTN SCHEDULE ≤3.7 BITS IS LOSSLESS (round-net-11, network exp 11, v11, paper NET-11, compression-axis real-scale rotation)

**Setup (identical to NET-10 Part B so it sits on the same trained family):** 5 Gutenberg novels, word-level top-4097 vocab, ctx 128, contiguous 90/10 split, causal transformer (is_causal=True) dm=64/4 heads, d∈{4,8}, 2000 AdamW steps — full held-out acc reproduces NET-10 exactly (d=4 s0 0.1571, d=8 s0 0.1619). For every 2-D matrix compute PR=(Σs²)²/Σs⁴ and b* = min per-tensor symmetric RTN bits in {2,3,4,6,8} retaining ≥0.98·full (isolated, restored each time); then joint uniform-2/3 and role-schedule joint tests.

**Per-matrix result — role-structured, not PR-monotone (identical on BOTH models; 28/52 matrices):** attention projections wq/wk/wv/ao (PR 19–32) are **2-bit lossless** (retained 0.992–1.002); MLP projections mi/mo (PR 31–52) need **3 bits** (2-bit retained 0.85–0.97); embed (PR 63) and pos (PR 40) need **4 bits** (embed 2-bit collapses to 0.075 ≈ 48% retained); the readout **un (PR 14.9–15.3 — the LOWEST PR in the model) needs 4 bits with a catastrophic 2-bit collapse (acc 0.043/0.051, 27–32% retained)**; lnf (PR=1) is 2-bit lossless. The NET-1 attention reversal direction survives (interface fragile / interior robust), but **the monotone b*(PR) law fails as a per-matrix predictor**: lowest-PR readout needs the most bits, and within the PR≈29–31 band attention is 2-bit lossless while mo0 (PR 30.8) needs 3. corr(PR,b*) = +0.58/+0.67 is role-grouping in disguise, not a law.

**Joint result — NET-1's practical schedule REFUTED:** uniform-2 collapses (retained 0.16 d=4 / 0.05 d=8); **uniform-3 is NOT lossless** (retained **0.83 d=4 / 0.73 d=8**, worse with depth — per-layer isolation says almost everything is ≥95% at 3 bits, yet compounding costs 17–27 points; errors amplified by residual-stream norm growth through depth, the NET-2/NET-10 mechanism). Role-schedule follow-up (d=4 retrained, full acc re-verified 0.1571): **role(4/3/2)** (embed/pos/un=4, mi/mo=3, attn=2, lnf=2) retains **0.878 at 3.64 avg bits** — +5pts over uniform-3 at +21% bits, still 12% short of lossless; role-tighter (mi=4) 0.897 at 3.73. **No static RTN schedule ≤3.7 avg bits is lossless on real text.**

**Verdict.** NET-11 (compression-axis real-scale rotation): the role structure survives (interface fragile / interior robust on both a d=4 and d=8 real causal LM), but (1) the monotone b*(PR) law does NOT transfer as a per-matrix predictor (readout counterexample), and (2) no static RTN schedule ≤3.7 avg bits is lossless on real text — uniform-3 (the toy lab's practical claim) retains only 0.83/0.73, and even role-protection reaches 0.878. Per-matrix isolation undercounts joint damage severely at real scale; a real bit-schedule needs joint-aware or activation-aware allocation, not data-free PR. Barriers: (a) PR and b* measured independently, RTN data-free — no injection; (b) sensitivity-based mixed precision is known but the real-scale negatives (uniform-3 not lossless, PR non-monotone via readout, depth-worsening) are new; Catalog (2094 packages) no prior work; (c) confronted — this IS the real-scale check and the toy law/schedule fail it; (d) causal masking + contiguous split + data-free quantization, no leakage; (e) 2 models × every matrix, identical structure both depths; (f) 0.98·full bar with full retained fractions, pos knife-edge noted, exact NET-10 reproduction, eval noise ≈0.15%; (g) uniform-2/3 + full-precision are the strong baselines; (h) the negative is the win — uniform-2/3 weights are not safe at this scale and PR-based schedules don't fix it; joint/activation-aware allocation is the real target.
Now 11 network experiments. Assessment v11. Paper NET-11, issue #106.
Scripts: /tmp/exp_net_pr_lm.py, /tmp/exp_net_pr_role.py.

## Part 12 — JOINT-AWARE BIT ALLOCATION ON A REAL LM: PER-TENSOR FLOOR ~5.3 BITS, PER-CHANNEL UNIFORM-4 IS LOSSLESS, AND "ATTENTION IS 2-BIT FREE" WAS AN OPERATING-POINT ARTIFACT (round-net-12, network exp 12, v12, paper NET-12, compression-axis joint-allocation rotation)

**Setup (identical to NET-10/11 family):** 5 Gutenberg novels, top-4097 word vocab, ctx 128, contiguous 90/10 split, causal transformer (is_causal=True) dm=64/4 heads, d=4, 2000 AdamW steps — full acc reproduces **0.1571** (a third time), lossless bar 0.98·full = 0.1540. Every quantization eval is JOINT (fresh model loaded with quantized state dict, full held-out eval) — the honest "what you'd ship" numbers. Three parts plus a targeted follow-up.

**Part A — the joint-marginal map (all others at the role schedule 4/3/2, one matrix varies):** attention projections wq/wk/wv/ao (all 16) are EXACTLY indifferent at 2 bits (retained flat at 0.878 to the third decimal). embed is jointly fragile: 3-bit retains **0.849** (≈11 pts off baseline) where isolation said ≈0.95; un (readout) 2-bit collapses to **0.280** — the most fragile matrix, jointly; MLP 2-bit 0.80–0.85, 3-bit fine; lnf indifferent; pos mildly fragile but tiny (128×64). The role structure is real at the joint margin and *sharpened*: the interface is the wall, the interior is cheap.

**Part B — per-tensor greedy strict-lossless frontier: 5.31 avg bits.** Greedy downward from all-6 (0.999), each step lowering the matrix whose down-step costs least, keeping retained ≥ 0.98·full (stopping condition verified exhaustively). Baselines: uniform-3 0.825, role(4/3/2) 0.878, all-4 **0.979 (misses the bar by one point)**, all-6 0.999. The greedy lands at **5.31 avg bits, retained 0.982**, with **embed/pos/un pinned at 6** (73% of params — 262k+262k+8k of ≈724k), MLP mostly 4, attention 2–3, lnf 2. Per-tensor static RTN cannot go under ≈5.3 bits losslessly on real text; all-4 — the config isolation makes look nearly safe — misses by one point.

**Part C — per-channel (per-row) RTN, data-free, is the fix:** on a fresh retrain (0.1571 re-verified), per-row scales give uniform-2 0.588 (vs 0.112), uniform-3 **0.947** (vs 0.825 — still 3 pts under bar), role 0.892, **all-4 0.987 ✓ (lossless @ 4.00 bits, 1.3 bits cheaper than the per-tensor frontier)**, and the per-tensor-optimized greedy frontier scores WORSE per-row (0.973 at 5.31 bits) — allocation is primitive-dependent. The 4-bit interface is irreducible even per-row (uniform-3 fails).

**Part C2 — the rotation's literal question answered no:** per-row "4-bit interface + ALL interior 2" retains **0.733** @ 3.46 bits; "4-bit interface + MLP 4 + attention 2" retains **0.907** @ 3.82 bits; uniform-4 is **0.987** @ 4.00. The 8-point gap between the last two is essentially all attention 2→4 (lnf indifferent) — **"attention is 2-bit lossless" was operating-point-dependent**: invisible in isolation and at the degraded 0.878 role operating point (Part A), but 2-bit attention costs ~8 pts once the rest of the net is clean. NET-11's 2-bit-lossless-attention claim is thereby corrected in exactly the direction NET-1 warned: isolation (and degraded operating points) undercount joint damage.

**Verdict.** NET-12 (joint-aware allocation, the confirmed compression target): (1) the joint-marginal map quantifies the wall (embed/un jointly 2–3× more fragile than isolation; attention indifferent only at a degraded operating point); (2) the per-tensor greedy strict-lossless frontier is **5.31 avg bits (interface at 6)**; (3) **per-channel RTN + uniform-4 is lossless at 4.00 bits** — 1.3 bits below the per-tensor frontier, answering "any data-free schedule reach lossless?" YES, and "4-bit interface + 2-bit interior enough?" NO (0.733/0.907). NET-11's "no static schedule ≤3.7 bits lossless" is corrected: per-tensor ~5.3 bits, per-channel uniform 4.0. Barriers: (a) joint evals on an independent loaded copy, greedy a pure allocation search over measured retention — no injection; (b) per-channel/group quantization is standard (the rescue is a confirmation of a known primitive), but the joint-damage quantification (embed 3-bit 0.849 vs 0.95 isolated; attention-free as operating-point artifact; per-tensor floor 5.3 vs per-channel 4.0) is new — Catalog (2094 packages) no prior work on any of these on a real causal LM; (c) confronted — real causal LM, real text, causal masking, 4097 vocab, the toy uniform-3 claim fails again; (d) causal masking + contiguous split + data-free quantization; (e) one seed, 4 config families × 4–5 bit levels × up to 51 greedy steps each a full joint eval; training leg reproduced 0.1571 exactly three times; (f) 0.98·full bar throughout, all-4 knife-edge (0.979 vs 0.980) called out, eval noise ≈0.15%, greedy stopping condition verified, PART C initial crash (1-D lnf, dim=1) fixed and re-run clean; (g) uniform-2/3, role, all-4/6, and full-precision are the baselines — the greedy is compared at the same bar; (h) the practical lever is the per-channel primitive (uniform-4, data-free) over smarter per-tensor allocation — and a warning that 2-bit-attention "wins" measured at degraded operating points do not survive a clean network.
Now 12 network experiments. Assessment v12. Paper NET-12, issue #107.
Scripts: /tmp/exp_net_joint.py, /tmp/exp_net_joint_partC.py, /tmp/exp_net_joint_partC2.py.

## Part 13 — ACTIVATION-AWARE (OUTLIER) QUANTIZATION ON A REAL LM: THE 4-BIT INTERFACE FLOOR IS NOT AN OUTLIER ARTIFACT — IT SURVIVES THE AXIS, MAGNITUDE-SPLIT, AND CLIPPING LEVERS (round-net-13, network exp 13, v13, paper NET-13, compression-axis activation-aware rotation)

**Setup (identical to NET-10/11/12 family):** 5 Gutenberg novels, top-4097 word vocab, ctx 128, contiguous 90/10 split, causal transformer (is_causal=True) dm=64/4 heads, d=4 s0, 2000 AdamW steps — full acc reproduces **0.1571** a fourth time, bar 0.98·full = 0.1540. All evals JOINT (independent loaded copy). Hypothesis: the NET-12 4-bit interface floor (per-row uniform-3 = 0.947 fails) is an outlier artifact — activation-aware/outlier-aware primitives should break it below 4 bits.

**Part A — quantization axis does not break the floor:** per-COLUMN (input-channel) symmetric RTN — the standard group-quant axis — is WORSE than per-row (uniform-2 0.413 vs 0.588; uniform-3 0.900 vs 0.947; role 0.923 vs 0.892). Per-row (output-channel) remains the better primitive at this scale; the axis is not the lever.

**Part B — the interface has only MILD outlier structure (the key diagnostic):** top-1% of magnitude holds only ~3.5% of the mass in EVERY matrix (embed 3.6%, un 3.5%, interior 3.0–3.4%); row-norm max/mean 1.1–1.9; the heaviest tail is un (kurtosis 9.1, max/mean 1.9) but this is nowhere near the 30–70% outlier concentration of larger-LM regimes. There is no catastrophic outlier mass to exploit — the 4-bit need is distributed, not concentrated.

**Part C — magnitude split fails:** interface rows at top-k ∈ {0..256} to 6-bit, rest to 2-bit (interior clean 4/3/2): k=0 0.636 → k=8 0.693 → k=64 0.724 → k=128 0.791 → k=256 **0.819** (2.74 bits) — sublinear and saturating, 16 points short of lossless even with top-6% promoted. Magnitude-aware allocation cannot shrink the schedule below ~4 bits.

**Part D — outlier clipping is a no-op:** SmoothQuant/AWQ-style per-row scales from the 99.9th/99.0th percentile of |W| (clipping outliers) change nothing: uniform-3 stays 0.944–0.948 (3 points under bar), uniform-4 stays lossless (0.982–0.985). Consistent with Part B — no outlier mass to clip.

**Verdict.** NET-13 (compression-axis activation-aware rotation): the 4-bit interface floor from NET-12 survives EVERY standard data-free weight-quantization primitive at this scale — axis (per-column no better), magnitude-split (0.819 at top-6% promoted), and clipping (no-op). Part B explains why: the small real causal LM is NOT in the outlier regime the bigger-model methods (LLM.int8/AWQ/SmoothQuant) target — top-1% share ~3.5% vs 30–70% — so the interface's bit-need is genuinely distributed and the floor is structural here. The honest remaining lever is activation-aware quantization with calibration passes (SmoothQuant-style activation scales), the one thing not data-free and not tested. Barriers: (a) joint evals on independent loaded copies, data-free transforms — no injection; (b) all three primitives are standard LLM-quant methods, but the NEGATIVE (none breaks the 4-bit floor on a real causal LM, because the outlier regime is absent) is new; Catalog (698 packages) no prior work on outlier/activation-aware tests on a real small causal LM; (c) confronted — real causal LM, real text, causal masking, 4097 vocab; Part B quantifies why this model is NOT in the target regime; (d) causal masking + contiguous split + data-free quantization; (e) one model, reproduced exactly 4×, every eval a full joint held-out forward; (f) 0.98 bar throughout, outlier stats raw (max/mean, top-1% share, kurtosis), 7-point k-sweep exhaustive, first-launch script bug (function-name collision) crashed before data and was fixed + re-run clean; (g) per-row/per-tensor references from the same family (NET-12), uniform-2/3/4 + role honest joint baselines; (h) the negative closes a branch — practitioners should not expect AWQ-style weight fixes to beat 4-bit lossless on a small causal LM; the distributed interface sensitivity is structural, and only activation-calibration-based methods are left.
Now 13 network experiments. Assessment v13. Paper NET-13, issue #108.
Scripts: /tmp/exp_net_outlier.py, /tmp/exp_net_outlier_partD.py.

## Part 14 — ACTIVATION-AWARE QUANTIZATION WITH CALIBRATION PASSES: THE 4-BIT INTERFACE FLOOR IS ACTIVATION-IRREDUCIBLE AT THIS SCALE (round-net-14, network exp 14, v14, paper NET-14, compression-axis last-lever rotation)

**Setup (identical to NET-10/11/12/13 family):** 5 Gutenberg novels, top-4097 word vocab, ctx 128, contiguous 90/10 split, causal transformer (is_causal=True) dm=64/4 heads, d=4 s0, 2000 AdamW steps — full acc reproduces **0.1571 a fifth time**, bar 0.98·full = 0.1540. All evals JOINT (independent loaded copy). Hypothesis: NET-13's last open lever — activation-aware quantization WITH calibration passes (AWQ/SmoothQuant per-channel activation scales absorbed into the weight quantizer) — breaks the 4-bit interface floor, either by making per-row uniform-3 lossless or via activation-informed allocation below uniform-4's 4.00 bits.

**Calibration diagnostic (the smoking gun):** forward pass on 512 TRAINING sequences (held-out eval never sees calibration). Mean per-channel activation max is nearly FLAT across every matrix: un 2.130 (max 2.574, max/mean 1.21), wq0 2.116 (1.07), mi0 2.117 (1.09), mo0 1.820 (1.24). AWQ's absorption only pays when some channels carry 10–100× the activation magnitude of others; at this scale the activation profile is flat — no channel heterogeneity to exploit. Same "not in the target regime" story as NET-13's weight outliers, now on the activation side.

**Part A — AWQ absorption does NOT break the per-row uniform-3 floor:** α=0.25 0.938, **α=0.50 0.943** (vs plain per-row 0.947 — marginally WORSE, no help), α=1.00 0.888 (much worse); uniform-4 identically lossless both ways (0.987). The calibration pass buys nothing.

**Part A2 — interface-at-3 probe:** interface (embed/pos/un) at 3 with AWQ scales, interior clean (mi/mo=4, attn=3, lnf=2): **0.958 @ 3.18 avg bits** — better than full-model uniform-3 (cleaner interior) but still **2.2 points short of the 0.98 bar**. The interface's irreducible 3-bit cost survives calibration applied directly to it.

**Part B — activation-informed allocation is a BAD signal here:** 25 Linears ranked by mean per-channel act max, bits 4/3/2 by tercile (embed/pos pinned at 4 = NET-11 b*): **0.828 @ 3.69** (0.841 with AWQ scales) — far worse than the weight-based role schedule (0.892 @ 3.64) and 16 pts below uniform-4 (0.987 @ 4.00). The ranking just re-discovers the interface is fragile but can't allocate below 4 bits; 2-bitting deeper interior costs ~8 pts. Activation scale is not a usable allocation signal at this scale.

**Verdict.** NET-14 (compression-axis, the LAST lever): activation-aware quantization WITH calibration passes does NOT break the 4-bit interface floor. AWQ absorption no-op-to-negative (α=0.5: 0.943 vs 0.947; α=1.0: 0.888), interface-at-3 stays 2.2pts short, activation-informed allocation much worse than weight-based. Mechanism: per-channel activation scales are near-uniform (max/mean ≈ 1.2), so there is no channel heterogeneity for AWQ to exploit — mirroring NET-13's flat weight-outlier structure. **The compression axis at small real-LM scale is now EXHAUSTED**: every primitive (per-tensor 5.31, per-row/per-column uniform-4 = 4.00 lossless floor, magnitude-split, percentile-clip, activation-calibration) leaves the interface irreducible below 4 bits. Practical optimum: per-channel uniform-4 (4.00 bits, 0.987), data-free. Barriers: (a) joint evals, AWQ = standard data-free-of-test transform, calibration on train only; (b) AWQ/SmoothQuant mature methods, the NEGATIVE (doesn't transfer to a small causal LM because activation heterogeneity is absent) is the content; Catalog 698 pkgs no prior activation-calibration test on a real small causal LM; (c) confronted — real causal LM, real text, causal masking, 4097 vocab; (d) calibration = training sequences only, eval = held-out; (e) 1 model reproduced exactly 5×, every eval a full joint held-out forward; (f) 0.98 bar, 3-value α-sweep, raw activation stats (mean/max act max, max/mean), plain per-row refs re-verified in-run; hook-closure bug (per-module accumulator never updated) crashed the first launch before data, fixed + re-run clean; (g) plain per-row uniform-3/4 re-measured same model + role/uniform-4 refs from NET-12; (h) negative closes the compression axis at this scale — only larger-scale checks (d=8/bigger dm) or the speed axis remain.
Now 14 network experiments. Assessment v14. Paper NET-14, issue #109.
Scripts: /tmp/exp_net_act.py.

## Part 15 — ATTENTION-COST LAW: DIFFUSE-BUT-PRUNABLE — TOP-K KEY/VALUE PRUNING IS LOSSLESS AT 8× ON A REAL CAUSAL LM (round-net-15, network exp 15, v15, paper NET-15, speed-axis rotation — FIRST POSITIVE REAL-SCALE SPEED RESULT)

**Setup (identical to NET-10/11/12/13/14 family):** 5 Gutenberg novels, top-4097 word vocab, ctx 128, contiguous 90/10 split, causal transformer (is_causal=True) dm=64/4 heads, d=4 s0, 2000 AdamW steps — full acc reproduces **0.1571 a sixth time**, bar 0.98·full = 0.1540, full loss 5.1188. Explicit causal-attention eval (verified: k=96 recovers full loss exactly). Top-k mask computed from each eval input's own attention weights at inference — data-free, no leakage, joint evals.

**Part A — attention is DIFFUSE, not concentrated (premise REFUTED):** per-query effective support exp(H) mean **46.6 of 128** (uniform-causal baseline ≈64.5 — only ~28% more concentrated); per-head 39.5–54.7, deeper layers more diffuse. Top-k mass: top-4 0.311, top-8 0.450, top-16 0.617, top-32 0.795. The "attention concentrates on a few tokens" picture does NOT hold at this scale.

**Part B — yet top-k key/value pruning is LOSSLESS at 12.5% of context:** k=4 0.940✗ (loss +0.084), k=8 0.971✗ (+0.043), **k=16 0.984 ✓** (loss 5.1370, +0.018 = +0.36% rel, **8× attention-core FLOP ratio**), k=32 0.998 ✓ (+0.005, 4×), k=64 1.001 ✓ (+0.001), k=96 1.000 ✓ (exact). Knee between k=8 and k=16.

**Part B2 — the selection is genuine (barrier g):** random-k k=16 0.922 (vs top-k 0.984, −6.2pts), k=32 0.950 (vs 0.998, −4.8pts). Random-16 even worse than top-8 (0.922 < 0.971) — the best 8 positions by weight beat any 16 at random. The pruning exploits the trained attention's selection information.

**Cost law:** at ctx 128/dm 64, the attention core (QK^T+softmax+AV ≈ 260·L²/token/layer) is ~95% of inference FLOPs vs projections+MLP — so the L/k ratio is nearly the total-model law: k=16 → **8× attention-core ≈ 5–6× total-model speedup**, data-free, no retraining, no calibration, no concentration assumption.

**Verdict.** NET-15 (speed-axis rotation): attention is DIFFUSE (eff support ≈ 0.36·ctx) yet lossless top-k pruning works at k=0.125·ctx because the mass beyond top-k is low-information and renormalization concentrates the retained mass onto informative positions. **LAW: DIFFUSE-BUT-PRUNABLE** — concentration is NOT required for lossless top-k pruning at real-LM scale. First positive real-scale speed result (NET-6/7/8 toy positives, NET-10 real-scale negative). Barriers: (a) top-k from the eval input's own attention at inference, joint evals, k=96 exact-loss match confirms numerics; (b) top-k sparse attention a known family, but "lossless at 12.5% ctx DESPITE diffuse attention" is new — Catalog 698 pkgs no attention-cost law on a real small causal LM; (c) real causal LM, real text, causal masking, 4097 vocab, held-out loss+acc; (d) top-k data-free (eval-input attention, no training signal), contiguous split; (e) 1 model reproduced exactly 6×, monotone k-sweep with clean knee; (f) 0.98 bar + raw loss, 6-point sweep + 2-point random control (fixed seed), explicit-attention numerics verified (k=96 exact), eval noise 0.15% ≪ margin; (g) full-attention ref + random-k control same bar (+6.2pts top-k); (h) 8× attention-core / ~5–6× total speedup lossless by acc bar, data-free; caveat — measured at small-LM scale, concentration and lossless-k may shift at larger scale (natural next speed check). Scripts: /tmp/exp_net_attncost.py.
Now 15 network experiments. Assessment v15. Paper NET-15, issue #110.
Scripts: /tmp/exp_net_attncost.py.

---

## Part 16 — NET-16 (round-net-16, speed axis): attention-cost law scales with depth — k* ≈ 4d, concentration depth-independent

**Hypothesis.** NET-15's DIFFUSE-BUT-PRUNABLE law (d=4: eff support 46.6/128, top-k lossless at k*=16 = 8× attention FLOPs) has a stated scale caveat. This round tests DEPTH: does lossless-k / the concentration law shift at d=8 on the same real causal LM (5 Gutenberg novels, dm=64, 4 heads, vocab 4097, ctx 128, causal, 2000 steps)? Outcome (1) concentration depth-independent, (2) lossless-k grows with depth (per-layer compounding — speed mirror of NET-11's compression compounding), (3) exact reproduction.

**Setup.** Identical to NET-15, d=8 s0. Full acc **0.1619** (d=4 0.1571 — deeper trains slightly better), bar 0.98·full=**0.1587**, full loss **5.0788** (d=4 5.1188). Same explicit causal-attention eval (k=96 recovers full loss exactly, 5.0789). Top-k mask from each eval input's own causal attention at inference — data-free.

**Part A — concentration law DEPTH-INDEPENDENT.** Eff support per head 43.3–56.3, **mean 50.1/128** (d=4 46.6) — if anything slightly MORE diffuse with depth. Top-k mass: top-4 0.285 (d=4 0.311), top-8 0.419 (0.450), top-16 0.586 (0.617), top-32 0.772 (0.795). The diffuse regime is stable at this scale.

**Part B — lossless-k GROWS with depth: k* ≈ 4d.** Sweep (d=8, d=4 in parens): k=4 0.873✗ (0.940), k=8 0.919✗ (0.971), k=16 **0.961✗ (0.984✓)** Δloss +0.047 (+0.018), k=32 **0.983✓ (0.998)** Δloss +0.015 (+0.005), k=64 0.997✓ (1.001), k=96 0.999✓ (1.000). **k=16 lossless at d=4, FAILS at d=8** — the knee moves to k=32. Every retained fraction lower, Δloss roughly doubled at each k (per-layer top-k error compounding through the residual stream — NET-11's compression compounding mirrored on the speed axis).

**Part B2 — selection importance GROWS with depth.** Random-k gap: k=16 top-k 0.961 vs random 0.866 = **+9.5 pts** (d=4 +6.2); k=32 0.983 vs 0.912 = **+7.1 pts** (d=4 +4.8). Deeper model relies more on trained selection.

**Cost law.** Attention ≈95% of inference FLOPs at ctx 128; lever (L/k*) shrinks with depth: 8× at d=4 → 4× at d=8 → (predicted 2× at d=16, under test). Total-model ~5–6× at d=4 falling to ~3–4× at d=8.

**Verdict.** NET-16: **CONCENTRATION-LAW-DEPTH-INDEPENDENT** (eff support ≈47–50 both depths) + **LOSSLESS-K-SCALES-WITH-DEPTH (k* ≈ 4d)** + **SELECTION-IMPORTANCE-GROWS-WITH-DEPTH**. DIFFUSE-BUT-PRUNABLE survives with a documented depth boundary. Barriers: (a) top-k from eval-input causal attention, joint evals, k=96 exact-loss match — nothing injected; (b) top-k a known family, the k*≈4d depth-scaling + flat concentration law new; Catalog 698 pkgs no depth-scaling attention-cost law; (c) real causal LM, real text, causal masking, 4097 vocab; (d) top-k data-free, contiguous split, held-out eval; (e) 1 model/depth, reproduced exactly 6×, monotone sweep with a knee that MOVED (16→32) in the direction consistent with NET-11's both-depth compounding; (f) 0.98 bar + raw loss, 6-pt sweep + 2-pt random control, k=96 exact numerics, retained fractions against each model's own full (full loss 5.1188→5.0788 reported); (g) full ref at each depth + random-k control, same bar; (h) lever real (4× at d=8) but depth-scaling is the honest caveat for scale-up claims. Script: /tmp/exp_net_attncost_d8.py.
Now 16 network experiments. Assessment v16. Paper NET-16, issue #111.
Scripts: /tmp/exp_net_attncost_d8.py.

## Part 17 — NET-18 (round-net-18, compression axis): the 4-bit floor is NOT depth-robust — per-channel uniform-4 loses losslessness at d=8

**Hypothesis.** NET-12's per-channel practical optimum (per-row uniform-4,
lossless 0.987 @ 4.00 bits at d=4) has a stated scale caveat. Does it survive
d=8 on the same real causal LM (d=8 s0, 5 Gutenberg novels, dm=64, vocab 4097,
ctx 128, causal, 2000 steps; full acc 0.1619, bar 0.98·full=0.1587, loss
5.0788)? Horns: (a) uniform-4 stays lossless at d=8 — floor depth-robust;
(b) NOT — NET-11's depth compounding at every bit level, floor deepens;
(c) non-monotone shift.

**Setup.** Identical to NET-10/11/12/13/14 family at d=8. 52 matrices, per-row
symmetric RTN, every eval JOINT (fresh model with quantized state dict, full
held-out 60k forward).

**Results (d=8; d=4 NET-12 refs in parens).** uniform-2 per-row 0.568 (0.588);
uniform-3 per-row **0.873 (0.947)** — Δ−7.4 pts; **uniform-4 per-row 0.967
(0.987)** — Δ−2.0 pts, **BELOW the 0.98 bar at d=8**; role(4/3/2) 0.801
(0.892) — Δ−9.1 pts; per-tensor uniform-3 **0.705 (0.825)** — Δ−12.0 pts
(cross-check vs NET-11's d=8 0.73, agreed within eval noise); per-tensor
uniform-4 0.961 (0.979); per-tensor uniform-2 0.038 (0.112).

**LAW: DEPTH-DEEPENS-QUANT-FLOOR.** The 4-bit per-channel interface floor is a
d=4 property: at d=8 the flagship uniform-4 drops below the lossless bar by
~2 pts, and the depth penalty is largest exactly where the schedule sits near
the robustness cliff (uniform-3 −7.4/−12.0, role −9.1) and smallest where the
schedule is already collapsed (uniform-2) or near-flawless (uniform-4) — but
uniform-4's small drop is the one that costs losslessness. NET-11's "deeper =
worse compounding" confirmed at EVERY bit level. Both axes' lossless operating
points shrink with depth at fixed width (the compression mirror of NET-16's
k*≈4d): quote the depth, or the 4-bit claim is a d=4 artifact.

**Barriers.** (a) joint evals on independent loaded copies, RTN data-free — no
injection; (b) per-channel quant known, the depth-dependence of the floor is
the content; Catalog 698 pkgs no depth sweep of the per-channel floor on a real
causal LM; (c) confronted — real causal LM, real text, causal masking, 4097
vocab, d=8; (d) causal masking + contiguous split + held-out + data-free quant;
(e) 1 model/depth, exact family reproduction (0.1571/0.1619), every eval a full
joint held-out forward, eval noise ≈0.15%; (f) 0.98 bar + raw loss both
reported, per-tensor uniform-3 cross-checked vs NET-11 (0.705 vs 0.73), avg-bits
size-weighted over 52 matrices (NET-12 convention); (g) uniform-2/3/4 + role
honest joint baselines, d=4 refs from same family at same bar; (h) real
consequence: deployment depth must be quoted with any 4-bit lossless claim —
the compression axis is now closed at d=4 AND its floor does not transfer to
d=8.

**Verdict.** NET-18: **DEPTH-DEEPENS-QUANT-FLOOR** — per-channel uniform-4
(0.987 lossless at d=4) FAILS at d=8 (0.967 < 0.98); depth penalty at every bit
level, worst near the robustness cliff. The compression axis's surviving
recommendation is a depth-4 claim; scale-up must re-measure the floor per depth.
Round-net-18. Now 17 network experiments. Assessment v17. Paper NET-18, issue
#113.
Scripts: /tmp/exp_net_d8quant.py.

## Part 18 — NET-17 (round-net-17, speed axis): k* = 4·d CONFIRMED across three depths — d=16 needs k*=64, per-layer compounding r(k)^d

**Hypothesis.** NET-15 (d=4) found lossless top-k pruning at k=16; NET-16
(d=8) moved the knee to k=32. The pattern **k* = 4·d** predicts d=16 → k*=64
(only 2× attention-core at fixed ctx=128). This round takes the third point of
the depth ladder on the same real causal LM (d=16 s0, 5 Gutenberg novels,
dm=64, vocab 4097, ctx 128, causal, 2000 steps; full acc 0.1610, bar
0.98·full=0.1578, loss 5.0830).

**Part A — concentration law: still diffuse, NOT strictly depth-independent.**
Effective support mean **53.28/128** (uniform-causal ≈64.5) — attention is
diffuse at every depth, but the drift 46.6 → 50.1 → **53.3** (d=4/8/16) is
real (+14% relative, ~0.3/layer), and top-k mass falls monotonically (top-16
0.617 → 0.586 → **0.556**). Within the d=16 model the later layers are
themselves more diffuse (early 45–52, late 52–58) — a within-model analogue.

**Part B — k* = 64 = 4·16 CONFIRMED.** Sweep: k=4 0.808✗ / k=8 0.877✗ / k=16
0.929✗ / k=32 0.972✗ / **k=64 0.995✓** (Δloss +0.006) / k=96 1.000✓ (exact
loss match). The knee is at k*=64; the attention-FLOP reduction at fixed
ctx=128 has decayed to **2×**.

**Mechanism — per-layer compounding explains the law exactly:**
retained(k,d) ≈ r(k)^d, with r(k) a depth-independent per-layer retention.
The d=8 per-layer retentions predict the d=16 totals within 0.006 (k=16 pred
0.924 vs 0.929, k=32 0.966 vs 0.972, k=64 0.994 vs 0.995).

**Part B2 — selection gap WIDENS with depth:** random-16 0.812 (top-k 0.929,
**+11.7 pts**), random-32 0.874 (0.972, **+9.8 pts**) — monotone +6.2/+4.8
(d=4) → +9.5/+7.1 (d=8) → +11.7/+9.8 (d=16).

**Cost law — speedup ≈ ctx/(4d).** At fixed ctx=128 the lever decays
8×→4×→2× with depth; but k* grows only LINEARLY in depth (4d), NOT in context
— so at real-LM context the law is favorable: ctx=4096, d=16 → k*=64 → **64×**
attention-core reduction (projected; k*'s ctx-independence untested, the
natural next speed check).

**Verdict.** NET-17: **k* = 4·d CONFIRMED across {4,8,16}** (k*=16/32/64) with
a per-layer compounding mechanism r(k)^d; concentration law corrected to
"diffuse but mildly depth-drifting" (46.6→53.3); random-k gap widens with
depth. DIFFUSE-BUT-PRUNABLE survives, now quantified as linear-in-depth
lossless-k. Barriers (a) top-k from eval-input causal attention, joint evals,
k=96 exact loss match — nothing injected; (b) top-k sparse attention known,
the k*=4d three-depth law + r(k)^d mechanism + depth-widening gap + eff-support
drift new; Catalog 698 pkgs no attention-cost law on a real small causal LM;
(c) real causal LM, real text, causal masking, 4097 vocab; (d) top-k data-free,
contiguous split, held-out; (e) 1 seed/depth, every eval full joint held-out
60k, monotone sweep with clean knee at each depth, compounding model predicts
d=16 from d=8 within 0.006; (f) 0.98 bar + raw loss, 6-pt sweep + 2-pt random
control, k=96 exact numerics, eval noise ≈0.15% ≪ k*=64 margin; (g) full
reference + random-k control (+11.7/+9.8 pts), same bar; (h) lever is
ctx/(4d) — decays with depth at fixed ctx (2× at d=16) but grows with context
(projected 64× at ctx=4096); caveat: k*'s ctx-independence untested. Script
/tmp/exp_net_attncost_d16.py.
Now 18 network experiments. Assessment v18. Paper NET-17, issue #113.
Scripts: /tmp/exp_net_attncost_d16.py.

## Part 19 — NET-20 (round-net-20, speed axis): k* is NOT context-independent — the attention-FLOP lever is context-CONSTANT (8× at d=4), refuting the 64× long-context projection

**Hypothesis.** NET-16/17 established k* = 4·d at fixed ctx=128 (k*=16/32/64
across d=4/8/16) with cost law speedup ≈ ctx/(4d). That law's UNTESTED
assumption — flagged in NET-17 barrier (h) — is that k* does not grow with
context; the projected 64× @ ctx=4096, d=16 depends on it. This round tests it
directly: the SAME d=4 model, SAME Gutenberg corpus, SAME 2000 steps, at
**ctx=256** (2× NET-15's 128; 2,343 contiguous windows). Full acc **0.1612**
(family scale 0.1571–0.1619), bar 0.1579, full loss **5.0877**.

**Part A — concentration law is context-DEPENDENT (more diffuse at longer
context).** Eff support mean **82.94/256** vs 46.6/128 (relative to uniform:
0.36 → 0.65 — LESS concentrated with more context). Top-k mass at fixed k
falls below ctx=128 everywhere (top-8 0.363 vs 0.450, top-16 0.503 vs 0.617,
top-32 0.662 vs 0.795). **Per-position (new):** eff support grows with past
available — early(0-31) **11.3**, mid(96-127) **72.3**, late(224-255)
**155.4** — NO bounded working set; attention spreads over most of whatever
context is present (the concentration-side reason k* must grow).

**Part B — the decisive test: k* doubles when context doubles.** k=8 0.947✗ /
k=16 0.971✗ (was LOSSLESS at ctx=128: 0.984✓) / **k=32 0.989✓** / k=64 0.996✓ /
k=128 1.000✓ / k=192 0.999✓ (exact loss match). **k* = 32 at ctx=256 = exactly
2× the ctx=128 knee (16): at d=4, k* ∝ ctx in the tested range (k* = ctx/8).**

**Corrected cost law — the lever is context-CONSTANT.** Unified across
NET-16/17/20 (3 depths @ 128 + this point): **k* = d·ctx/32 ⇒ speedup = 32/d**,
INDEPENDENT of context. | | ctx=128 | ctx=256 |: d=4 k*=16,8× / k*=32,8×; d=8
k*=32,4× / —; d=16 k*=64,2× / —. **NET-17's projected 64× @ ctx=4096 is
REFUTED** — long context buys no additional relative saving because the
lossless window scales with it (k* ∝ ctx). The surviving claim is the
depth-only lever 32/d: 8× at d=4 robust at both 128 and 256.

**Part B2 — selection still matters at 2× context:** random-16 0.884 (top-k
+8.7 pts), random-32 0.929 (+6.0) — same gap magnitude as ctx=128.

**Verdict.** NET-20 (speed-axis round 5): **k* is NOT context-independent** —
doubling ctx doubled the lossless window (16→32, exactly proportional at this
resolution), so the attention-FLOP lever is context-constant, **speedup ≈ 32/d**
(a depth-only property), refuting the 64× long-context projection. Concentration
law corrected to context-DEPENDENT (more diffuse with context, no bounded
working set). DIFFUSE-BUT-PRUNABLE survives with a context-constant lever.
Barriers (a) top-k from eval-input causal attention, joint evals, k=192 exact
loss match — nothing injected; (b) k* ∝ ctx proportionality + context-constant
lever + concentration diffusion with context new; Catalog 698 pkgs no
context-scaling sparse-attention law on a real small causal LM; (c) real causal
LM, real text, causal masking, 4097 vocab, 2× context; (d) data-free, contiguous
split, held-out; (e) 1 seed, context ladder = 2 points (128/256) — the
proportionality is exact at this resolution but not extrapolated; a ctx=512 or
seed-1 point would strengthen; k=16 clearly fails vs clearly passes at 128,
k=32 clearly passes; (f) 0.98 bar + raw loss, 6-pt sweep + 2-pt random control,
k=192 exact numerics, eval noise ≈0.15% ≪ k=32 margin (0.989 vs 0.98); (g) full
ref + random-k at same k (+8.7/+6.0 pts), same bar; (h) reframed negative: the
64× hope is dead, the real lever is depth-only 32/d, boundary ctx∈[128,256].
Script /tmp/exp_net_ctx256.py.
Now 19 network experiments. Assessment v19. Paper NET-20, issue #114.
Scripts: /tmp/exp_net_ctx256.py.

## Part 20 — NET-19 (round-net-19, depth axis): scale unlocks LENGTH-SPECIFIC mastery but NOT length-general composition — the carry chain is solved at every depth, the length wall is depth- and scale-immune (credit-assignment depth-immunity holds at scale)

**Hypothesis.** NET-4/5 decomposed the decomposable-error regime: the copy-self
basin is a tied-readout artifact (untie ⇒ escape, NET-5), but the CARRY CHAIN is
readout-independent — a width/depth/readout-immune credit-assignment wall. At
NET-5's scale full-mastery fails in some configs and the depth law is flat but
under-powered (d=4 3/3, d=1 2/3, d=2 1/3). This round asks the last open
question: **does scale unlock depth pay?** Scale up vs NET-5 — dm=192 (untied,
4.5–18× params), bs=256 (2×), 12000 steps (~3× distinct pairs).

**Setup.** Identical to NET-4/5 except scale: LSB-first base-10 a+b=c, n=6,
inputs `[a,'+',b,'=']`, outputs c₀…c₆ (carry-out last), per-digit CE,
teacher-forced GO-shift, pre-LN, 4 heads, d_mlp=4·dm, UNTIED head, dm=192 for
all depths (NOT budget-matched — generous to depth). d∈{1,2,4}×3 seeds = 9
configs, B = 454477/899341/1789069.

**Part A — ALL 9/9 MASTER, depth pays NOTHING (flat-mastery horn).**
d=1 full=0.9940±0.0085, d=2 1.0000±0.0000, d=4 0.9976±0.0035 — masters 3/3 at
every depth; the d=1 vs d=4 gap (0.0036) is within seed noise (individual d=1
seeds hit 1.0000). **Scale unlocked depth-1 mastery** (NET-5's d=1 failed 2/3;
here 3/3) — but deeper nets do NOT beat shallow ones at 4.5–18× params and 3×
data. The copy-self-basin + stochastic-escape mechanism reproduces at dm=192
(d=2 s=2: per≈0.87/full≈0.10 plateau st=2000–3000, per⁷=0.38≫full, jump to
full=1.0000 at st=4000). Per-position: errors spread thin across interior
columns, never localized — the model computes the full n=6 sum algorithmically
(fresh-draw 1.0000 on a 10¹² pair space rules out memorization).

**Part B — the length wall survives scale: 9/9 at chance.** Every mastered
config re-trained at n=3 (8/9 full=1.0000; d=1 s=2 reached per=0.8010 but
full=0.2041 — the NET-5 carry-chain dissociation, per-high/full-low correlated
errors, reproduced at dm=192 in the same config type), then tested n=4/5/6:
**full=0.0000 at every depth and seed** (per ≈0.09–0.22 ≈ digit floor vs
chance 1e-5/1e-6/1e-7). The probe (task #89) reproduced the marathon's d=1 s=0
and d=4 s=0 numbers BYTE-IDENTICAL (same seed/settings ⇒ identical results),
validating the length wall at the two depth extremes 6h early.

**Verdict.** Flat-law-extension horn CONFIRMED (all-master-equally form);
breakthrough horn REFUTED. Scale unlocks length-SPECIFIC mastery at every
depth, NOT length-general composition — the memorize-without-compose wall
(NET-3 leg-2 / NET-4/5) reproduced at the largest arithmetic scale in the
program (dm=192). Credit-assignment depth-immunity holds at scale: the binding
constraint is optimization (decomposable-error credit assignment), never
capacity. The carry chain is now the best-characterized hard problem in the
program: fixed-length = depth-flat and scale-solved; length-gen = depth- and
scale-immune. Open levers (untested): carry curriculum, scratchpad/CoT
intermediates, recurrence (a stateful carry cell). Depth axis has had 9
iterations; compression (exhausted at d=4, not depth-robust at d=8) and speed
(context-constant lever 32/d) are the standing axes. Barriers all checked —
clean held-out, 3 seeds×every config, per^7 diagnostic, per-position
localization, chance ceilings per length, deterministic probe replication.
Paper 63, issue #115.
Now 20 network experiments. Assessment v20. Paper NET-19, issue #115.
Scripts: /tmp/exp_net_carry_scale.py, /tmp/exp_net_carry_lenprobe.py.

---

# Part 21 — NET-21: The Length Wall Is Schedule-Robust (Curriculum and Length-Mixing Do Not Unlock Length-General Composition)

**Program:** Network/LLM lab — round-net-21 (performance axis; training-schedule test of the carry-chain length wall)
**Date:** 2026-08-14
**Script:** /tmp/exp_net_curriculum.py (ALL_DONE). **Log:** /tmp/net21.log.

**Question.** NET-19 (dm=192, 9/9 fixed-length masters, 9/9 length-gen at chance)
named the TRAINING SCHEDULE as the untested lever on the memorize-without-compose
wall. Does a length curriculum — or length-mixing — force a length-GENERAL carry
procedure (positive horn), or is the wall intrinsic to carry credit assignment
(negative)? Decisive test: does beyond-max n=6/7/8 generalize for a model whose
curriculum ends at n=5?

**Setup.** Byte-identical to NET-19 (pre-LN transformer, dm=192, 4 heads,
d_mlp=4·dm, UNTIED readout, per-digit cross-entropy, teacher-forced GO-shift,
LSB-first base-10 a+b=c, bs=256, 12000 AdamW steps, seed 0). ONE documented
deviation: pos-embedding CTX 22→32 so eval at n=8 (3n+3=27 positions) fits;
all 5 arms — including the two plain controls — carry the same enlargement, so
comparisons stay fair. Arms: C (control plain n=3, d=1), E (control plain n=5,
d=1), A (curriculum GROW 2→3→4→5, d=1), B (mixed lengths {3,4,5} each batch,
d=1), D (curriculum GROW, d=2). Final eval at n=4/5/6/7/8 (chance 10^-(n+1)),
per-position at the max trained length.

**Results (full=per-digit in parens):**

| arm | schedule | n=4 | n=5 | n=6 | n=7 | n=8 |
|---|---|---|---|---|---|---|
| C control | plain n=3 | 0.0000 (.224) | 0.0000 (.211) | 0.0000 (.153) | 0.0000 (.158) | 0.0000 (.163) |
| E control | plain n=5 | — | **1.0000** | 0.0000 (.110) | 0.0000 (.106) | 0.0000 (.105) |
| A | cur grow, d=1 | 0.0000 (.107) | 0.1929 (.854) | 0.0000 (.099) | 0.0000 (.133) | 0.0000 (.110) |
| B | mixed {3,4,5} | 0.0068 (.572) | 0.0142 (.670) | 0.0000 (.099) | 0.0000 (.107) | 0.0000 (.114) |
| D | cur grow, d=2 | **0.0000** (.105) | **1.0000** | 0.0000 (.129) | 0.0000 (.111) | 0.0000 (.116) |

- **C** masters n=3 (1.0000) from st=1000; n=4/5/6/7/8 all chance. The known wall
  reproduced in-run (enlarged pos table does not disturb it).
- **E** masters n=5 (1.0000 by st=8000, per-position all 1.0000); n=6/7/8 all
  chance (per ≈0.105–0.110 ≈ digit floor). "Trained longer" is NOT the cure — a
  plain-n5 trainer is as length-specific as a plain-n3 trainer.
- **A** (curriculum, d=1): n=5 stuck in carry dissociation (per 0.85/full 0.19);
  n=4 0.0000; n=6/7/8 chance. Never even masters the final trained length at d=1.
- **B** (mixed): NEW — NEVER masters ANY length. per stuck 0.54–0.67 / full
  0.00–0.02 for ALL 12000 steps (permanent per-high/full-low correlated-error
  regime). Diversity blocks length-specific mastery, delivers no general mastery.
- **D** (curriculum, d=2): NEW — curriculum FORGETS intermediate lengths. Masters
  n=5 perfectly (per-position all 1.0000) but n=4 — trained 3000 steps — is
  chance (0.0000). The final-length training OVERWROTE the n=4 algorithm. The
  model specializes to the LAST length; no length-parameterized general
  procedure emerges. Beyond-max n=6/7/8 all chance.

**Verdict.** Negative — the schedule-cure is REFUTED. Beyond-max length-gen is
at chance under every schedule tested (curriculum at d=1 and d=2, mixing, plain
n=3, plain n=5). The wall is robust to the training DISTRIBUTION: the optimizer
converges to a length-SPECIFIC carry attractor under every schedule — adding
diversity either blocks mastery (mixing) or erases intermediate lengths
(curriculum). Two NEW phenomena recorded: MIXING-PREVENTS-MASTERY and
CURRICULUM-FORGETS-INTERMEDIATE-LENGTHS — a third and fourth manifestation of
the optimizer attractor mechanism (after the copy-self basin and the carry
dissociation). Surviving levers change the problem, not the schedule:
scratchpad/CoT (task), recurrence/stateful carry cell (architecture), explicit
length token (input). Caveat: 1 seed per arm (the stark 1.0000-vs-0.0000
readings and the in-run plain-n3 control that reproduces the known wall keep
the verdict robust; a second-seed replication of the two new phenomena is the
strengthening step). All 8 barriers checked (see paper). Paper 65, issue #116.
Now 21 network experiments. Assessment v21. Paper NET-21, issue #116.
Script: /tmp/exp_net_curriculum.py.

---

## Part 22 — Round-net-22: Scratchpad vs the carry-chain length wall (task-remodeling axis)

**Date:** 2026-08-14. **Hypothesis:** NET-4's credit-assignment account says the
carry-chain length wall (master training length, chance beyond-max) is a credit
shortfall; exposing the carry state as explicit per-column targets (scratchpad)
should give the chain per-step credit and unlock length-gen — the first positive
cure. **Setup:** LSB-first a+b=c, dm=192, untied, bs=256, 12000 steps, VOCAB=14
(+SC/GO), CTX=40 (n=8 scratchpad seq 4n+5=37 fits). Scratchpad target sequence
`SC c_1..c_n GO s_1..s_n c_n` (carries + answers both teacher-forced at train).
Eval fully autoregressive (model generates its own carries, then answers) plus a
given-correct-carries diagnostic (feeds true carries, isolates answer-computation
from carry-generation). Arms: d=1 plain control + scratchpad s0/s1; d=2 plain
control + scratchpad s0/s1.

**d=1 results (2 seeds).** Control masters n=5 (1.0000 stable), n=6/7/8 0.0000
(wall reproduced). Scratchpad s=0: tf 1.0000@st1000 → collapse 0.008@st2000 →
plateau full≈0.25/per≈0.87 for 9000 steps (carries still known); n=6/7/8 all
0.0000, carry_per 0.29–0.38 (at/below chance). Scratchpad s=1: tf 1.0000@
st1000–3000 → collapse to full≈0.74/per≈0.96 from st4000; n=6/7/8 all 0.0000,
carry_per 0.32–0.48. **Given-correct-carries: n=6/7/8 answers still 0.0000 in
both seeds** — the wall is a position-specific answer-COMPUTATION failure, not
carry propagation.

**d=2 results (2 seeds).** Control plain n=5 (s=0) did NOT master (full=0.1016/
per=0.8503, stuck dissociation), n=6/7/8 0.0000. Scratchpad s=0: tf 1.0000@
st1000, transient dip 0.80@st2000, RECOVERED to 1.0000 held st5000→end; n=6/7/8
all 0.0000; given-carries 0.0000. Scratchpad s=1: tf 1.0000@st1000–2000, violent
crash to 0.041@st3000, recovered 0.949@st4000, held 1.0000 st5000→end; n=6/7/8
all 0.0000; given-carries 0.0000.

**Findings.** (1) SCRATCHPAD-DOES-NOT-UNLOCK-LENGTH-GEN — all 4 scratchpad arms
0.0000 at n=6/7/8; the task-remodeling lever is CLOSED. (2) GIVEN-CARRIES-STILL-
FAIL — the strongest wall diagnostic: perfect carries still give 0.0000 beyond-
max answers; the wall is a positional/representational expressivity property of
the fixed-depth answer function, not a credit shortfall. (3) NEW SCRATCHPAD-
COLLAPSE-IS-DEPTH-CONDITIONED — scratchpad mastery is unstable at both depths,
but absorbing at d=1 (permanent plateaus 0.25/0.74) and restorative at d=2
(recoveries to stable 1.0000): the mirror of NET-19's stochastic escape. Plus:
scratchpad rescued IN-RANGE mastery at d=2 (both seeds 1.0000 where the d=2
plain control stuck at 0.10) — clean split between in-range credit (helped) and
beyond-range answer function (untouched). Caveat shared with the length-gen
line: pos-emb extrapolation beyond trained positions 0..24 is a factor in all
beyond-max evals; RoPE is a surviving lever. **Verdict:** negative — the
credit-assignment horn is refuted; the wall is positional expressivity. Surviving
levers: recurrence/stateful carry cell, RoPE/position encoding, length-parameterized
readout. All 8 barriers checked (see paper). Paper 66, issue #117. Now 22
network experiments. Assessment v22. Script: /tmp/exp_net_scratchpad.py.

## Part 23 — Round-net-23: RoPE vs the carry-chain length wall (position-representation axis)

**Hypothesis.** NET-22's GIVEN-CARRIES-STILL-FAIL proved the wall is a
position-specific answer-COMPUTATION failure — but every length-gen eval used
LEARNED ABSOLUTE pos embeddings, so beyond-max positions (25..36) were UNTRAINED
table entries. Test: RoPE (rotary q/k, no table, smooth extrapolatable
positions) removes the confound. Positive: RoPE unlocks length-gen (first cure;
the whole line was pos-emb-confounded). Negative: wall survives → genuine
fixed-depth expressivity limit; caveat retired; recurrence is the sole lever.

**Setup.** Plain n=5 LSB-first a+b=c, dm=192/untied/bs=256/12000 steps, d=1;
arms: abs-pos control (s=0) + rope (s=0, s=1). The `rope` flag is the ONLY
difference (same task/arch/budget/eval). VOCAB=13, CTX=40 (abs-pos table only;
RoPE arm has no table). Eval n=5/6/7/8 teacher-forced, 2048 fresh draws, with
per-position breakdown. Script /tmp/exp_net_rope.py, log /tmp/net23.log.

**Results.** abs-pos control (s=0): masters n=5 (full=1.0000, late jump
st=5000–6000), n=6/7/8 full=0.0000, per 0.11/0.13/0.10 ≈ digit floor; MSB
position 0.20/0.31/0.11 (untrained entry fires wrong). **rope s=0:** n=5
full=1.0000/per=1.0000 BY STEP 1000 (fastest in-range arm); n=6/7/8 full=0.0000,
per 0.166/0.156/0.146; **MSB position 0.587/0.571/0.565** (final-carry marginal
≈0.5 prior transferred — abs-pos got 0.11–0.31). **rope s=1:** n=5
full=0.1040/per=0.8507, PERMANENTLY dissociated (flat full≈0.10/per≈0.85
st=5000–11000, no escape); per-position shape [0.107, 1,1,1,1,1] — the model
computes all interior + final-carry columns perfectly and fails ONLY the LSB
digit; n=6/7/8 full=0.0000, per 0.156/0.157/0.113.

**Findings.** (1) ROPE-DOES-NOT-UNLOCK-LENGTH-GEN — beyond-max 0.0000 in both
RoPE seeds despite in-range mastery (s=0). (2) THE-POS-EMB-CAVEAT-IS-RETIRED —
the first length-gen eval with NO position table; the wall reproduces with
smooth, extrapolatable, training-consistent rotary positions ⇒ the length wall
is NOT an absolute-pos-extrapolation artifact. (3) NEW MSB-MARGINAL-TRANSFERS —
the final-carry DISTRIBUTION transfers beyond-max with RoPE (0.565–0.587 ≈ 0.5
prior) while the computation does not: statistical prior vs algorithm transfer
cleanly separated. (4) NEW ROPE-DISSOCIATION-IS-SEED-DEPENDENT — s=0 perfect by
st=1000, s=1 permanently dissociated; per-position shape is a ONE-COLUMN
failure (interior + final-carry 1.000, LSB 0.107) — distinct from NET-4/5's
carry-cascade shape, single-seed. **Verdict:** negative — the positive horn is
refuted; carry wall characterized on depth, scale, schedule, task-remodeling,
AND position representation, all negative for length-gen. Surviving levers
(down from NET-22's list of 3): recurrence / stateful carry cell, length-
parameterized readout. RoPE speeds IN-RANGE learning and transfers the beyond-
max MARGINAL but not the composition. All 8 barriers checked (see paper). Paper
67, issue #118. Now 23 network experiments. Assessment v23. Script:
/tmp/exp_net_rope.py.

---

## Part 24 — STATEFUL CARRY CELL vs THE LENGTH WALL (the recurrence test — FIRST POSITIVE CURE)

**Hypothesis:** the carry-chain length wall is a fixed-depth, STATE-FREE,
position-parameterized ANSWER-FUNCTION expressivity limit — not a task limit and
not an input-representation limit. A length-general stateful answer device (GRU
carrying the carry in hidden state; step count = column index) unlocks length-gen
on the exact task family that walls the feedforward transformer.

**Setup:** plain n=5 LSB-first a+b=c, dm=192, bs=256, 12000 AdamW steps, lr 1e-3,
teacher-forced eval n=5/6/7/8 (2048 fresh draws each). Five arms: pure GRU (raw
one-hot columns → GRUCell 20→192 → per-column digits; EOS step → final carry) s=0,
s=1; hybrid-RoPE (the NET-23 walled encoder on a|+|b|=, VOCAB=12, per-column
feature = concat(h[a_i], h[b_i]), GRUCell 384→192 readout, jointly trained) s=0,
s=1; hybrid-abs (same, learned pos table) s=0. Encoder causal mask verified
identical to the walled model (on-the-fly triu for any T).

**Results (full/per at n=5/6/7/8):** pure GRU s=0: 1.0000/1.0000, 0.9980/0.9997,
0.7021/0.9625, 0.0806/0.8584. pure GRU s=1: 1.0000/1.0000, 1.0000/1.0000,
0.9854/0.9982, 0.6997/0.9648. **hybrid-RoPE s=0 and s=1: 1.0000/1.0000 at ALL of
n=5/6/7/8.** hybrid-abs s=0: 1.0000/1.0000, 0.9834/0.9976, 0.9634/0.9951,
0.9624/0.9957. Reference (NET-23 state-free readout, same encoder/budget):
0.0000 at n=6/7/8.

**Findings:**
1. **STATEFUL-CARRY-CELL-UNLOCKS-LENGTH-GEN — the FIRST positive cure in the
   program.** The walled RoPE encoder + GRU carry-cell readout computes the carry
   chain PERFECTLY beyond its training length (full=1.0000 at n=5/6/7/8, both
   seeds, zero errors on 18.4k fresh n=8 digit predictions).
2. **THE-WALL-WAS-THE-ANSWER-FUNCTION, NOT THE ENCODER.** Byte-identical
   encoder, budget, causal mask; the readout's STATE is the only difference vs
   NET-23 and it flips beyond-max 0.0000 → 1.0000. NET-22's GIVEN-CARRIES-STILL-
   FAIL is explained: carries as INPUT tokens are useless to a state-free
   readout; the same carries as recurrent STATE are exactly the cure.
3. **THE-CURE-IS-POSITION-SCHEME-INDEPENDENT, but encoder feature quality still
   modulates it.** hybrid-abs ALSO length-gens (n=8 full=0.9624) — far above the
   transformer's 0.0000 — with a uniform, thin per-column error tail (0.986–1.000,
   feature-quality noise from untrained table entries), not a structural wall.
   RoPE gives the clean 1.0000.
4. **NEW — RAW-STATE-ALONE-HITS-A-STATE-HORIZON.** The textbook pure GRU masters
   n=5 (fastest arm: by step 2000), extends ~1–2 steps, but degrades at n=8
   (full 0.08–0.70, seed-dependent) with the carry TRANSITION length-general
   (final-carry 0.90–0.99 at n=8) while the digit READOUT misfires past the
   training unroll. The cure needs state AND the encoder's content-rich column
   features. Capacity caveat: 125k vs 782k params (flagged).

**Verdict:** CONFIRMED — first positive cure. The five-axis negative line is
resolved: the wall is the state-free feedforward answer function; adding a
length-general stateful carry cell unlocks exact, seed-independent length-gen.
Recurrence/state was the surviving lever, and the controlled toggle is
unambiguous. All 8 barriers checked (see paper); caveats: hybrid-abs 1 seed,
pure-GRU capacity, 2 hybrid seeds. Paper 68, issue #119. Now 24 network
experiments. Assessment v24. Script: /tmp/exp_net_stateful.py; log:
/tmp/net24.log.

---

## Part 25 — Stateful-Carry-Cell Cure, Mechanism Dissection (round-net-25, NET-25)

**Date:** 2026-08-14. **Status:** Machine-verified (ALL_DONE_NET25 / _PAD / _SWEEP / _EOS).
**Hypothesis:** NET-24's cure (GRU carry cell over encoder features → n=5/6/7/8
full=1.0000) is dissected: which ingredient of the answer-side features is
load-bearing? Three mutually-exclusive hypotheses — H1 CAPACITY (raw-GRU
state-horizon = too-small cell; test: hidden=384, 471k params on raw one-hots),
H2 REPRESENTATION (high-dim well-separated digit features cure; test: UNTRAINED
fixed random 384-d projection of the one-hots), H3 POSITION (encoder's RoPE-style
step signal is load-bearing; test: one-hots + 8-d step sinusoid).

**Setup:** all arms plain n=5, LSB-first, per-digit CE, bs=256, 12000 AdamW steps,
lr 1e-3, eval n=5/6/7/8 (2048 fresh, teacher-forced). Reuses GRUCarry/make_cols
from the NET-24 script. The round grew: a pad-to-384 control (barrier-e forced,
after verifying GRUCell inits all params from U(±1/sqrt(hidden)), in_dim-
independent), a 13-seed variance sweep, and an EOS-density control (pad384 vs
pad384-zeroEOS: SAME seed → IDENTICAL GRUCell/head weights; only the EOS input
dimension differs, 384-d dense-learned vs 20-d).

**Results** (n=8 full):
- cap384-raw (471k, raw one-hots): 0.0078 / 0.0063 → **H1 CAPACITY REFUTED**.
- proj384 (untrained random 384-d projection): 1.0000, 5/5 seeds → H2-strong
  (learned features needed) REFUTED; high-dim features (untrained) cure.
- pos28 (one-hots + 8-d RoPE sinusoid, 28-d EOS): 0.0049 / 0.0049 → **H3
  POSITION REFUTED**.
- pad384 (one-hots zero-padded to 384-d, DENSE 384-d learned EOS): 1.0000, 4/4.
- pad384-zeroEOS (identical weights, 20-d EOS): 0.7441 / 0.0259 → raw20-range.
- raw20-192 variance (7 seeds): 0.0806, 0.6997, 0.0103, 0.0063, 0.0093, 0.0020,
  0.0132 → **0/7 at 1.0** (state-horizon real but seed-variance-heavy; NET-24's
  2-seed law undersampled, conclusion holds).

**Findings:**
1. **DENSE-FINAL-STEP-IS-THE-CURE.** The NET-24 cure is the dense learned
   final-carry (EOS) input, NOT the encoder's features. Same-seed identical-
   weights control: dense 384-d EOS → 1.0000 (4/4); 20-d EOS → 0.026–0.744
   (raw-range). NET-24's "content-rich column features" interpretation corrected.
2. **THE DIGIT-PATH CAN BE RAW.** pad384's digit columns are functionally raw
   20-d one-hots and it still cures 4/4; the dense EOS is sufficient alone. The
   pure-GRU failure was its 20-d EOS, not its digit inputs.
3. **EOS RICHNESS NEEDS DIM ≫ DIGIT COUNT.** pos28's 28-d learned EOS still fails
   (0.0049); 384-d works. Threshold (28–384) untested.
4. **CARRY TRANSITION ALWAYS LENGTH-GENERAL** (final-carry 0.86–0.99 even in
   failing arms); the digit READOUT was the fragile part; the dense EOS keeps it
   in-distribution at depth (hypothesis: boundary-step backprop conditioning).

**Verdict:** all three original hypotheses REFUTED; the lever is the final-step
input richness. Airtight control (same-weights, EOS dim only) flips the cure.
Corrects NET-24; strengthens the round via the seed distributions (barrier e
bit hard and was addressed). All 8 barriers checked (see paper); flagged: EOS
threshold untested, mechanism hypothesis unproven. Paper 69, issue #120. Now 25
network experiments. Assessment v25. Scripts: /tmp/exp_net_stateful_ctrl.py,
_pad.py, _sweep.py, _eosctrl.py; logs: /tmp/net25.log, _pad.log, _sweep.log,
_eos.log.

## Part 26 — EOS-Width Is a Distribution Shift, Not a Sharp Threshold (round-net-26, NET-26)

**Date:** 2026-08-14. **Status:** Machine-verified (ALL_DONE_NET26 / _VER / _DIST).
**Hypothesis:** NET-25 flagged an EOS-width threshold (28–384 untested) and an
"identical-weights airtight control" (pad384 vs pad384-zeroEOS). Both are
attacked: (1) is the EOS-width effect a SHARP critical width or a
seed-dependent probability? (2) is NET-25's control valid (the two arms were
constructed before vs after `torch.manual_seed` → different init streams)?

**Setup:** new EOSWidthGRU(eos_width): GRUCell(384→192) on zero-padded raw
one-hot digit columns, learned E-d EOS zero-padded to 384, n GRU steps + one
EOS step, Linear(192→10) head. Fixed cell — only trainable EOS width varies.
Same task/budget/eval as NET-25. Three script families: sweep (E × 2 seeds),
verify (after-seed vs before-seed construction, E=20, s=0), dist (E=20/384 ×
seeds 2–7). 30 arms total.

**Results:**
- Sweep n=8 full: **E=20 → 0.9990 / 0.0166** (fragile); **E≥28 → 1.0000 in all
  14/14 arms** (E=28,64,96,128,192,256,384 × 2). No threshold inside the tested
  band — the fragility sits below 28, at E=20.
- E20 s1 failure trajectory: n=5 1.0000 → n=6 0.9556 → n=7 0.1445 → n=8 0.0166
  — smooth progressive-unroll collapse, not a cliff.
- Verify: after-seed s0 = 0.9990, before-seed s0 = 0.9990 (deterministic: same
  value as sweep E20 s0). Construction-order RNG does NOT explain NET-25's 0/2;
  both timings near-cure at s0 → the 0/2 was two unlucky draws from a wide
  distribution.
- Dist: E=20 seeds 2–7 → 0.0107, 0.1240, 0.0576, 0.0054, 0.0063, 0.0308; E=384
  → 1.0000 ×6.
- **Merged E=20 (12 samples): {0.999×3, 0.744, 0.124, 0.058, 0.031, 0.026,
  0.017, 0.011, 0.006, 0.005}** — P(clean cure) = 3/12 = 25%, median 0.044,
  P(≤0.75) = 75%. **Merged E≥28 (20 samples): all 1.0000, 0/20 failures.**
- Probe: cure = hidden-norm FLAT through cols 6–8 (Δ+0.1–0.15) + maxconf 1.000;
  E20 failure = norm DRIFT (Δ+2.2 → 12.44) + maxconf dips 0.945–0.984 at
  beyond-training columns. The boundary input keeps the hidden state
  in-distribution at depth.

**Findings:**
1. **EOS-WIDTH-DISTRIBUTION-SHIFT.** The EOS width gates P(cure) as a one-sided
   distribution shift, not a sharp boundary. E=20 fragile (P≈¼, wide
   continuum); E≥28 robust (19/19). NET-25's "28-d fails (pos28)" was a
   GRUCell(28)-architecture artifact; its "20-d fails 0/2" was a small draw.
2. **THE CONTROLLING VARIABLE IS REPRESENTATIONAL DISTINCTNESS, NOT WIDTH PER
   SE.** E=20's EOS occupies exactly the digit subspace (dims 0–19, no exclusive
   dims) → boundary ambiguous with a digit step → seed-fragile. E≥28's EOS has
   exclusive dims 20..E−1 no digit column activates → unambiguous boundary →
   robust. pos28 (full-input-width EOS, no exclusive dims) is consistent.
3. **CONSTRUCTION-ORDER RNG RULED OUT.** Both after-seed and before-seed
   constructions near-cure at s0 (0.9990). NET-25's "airtight control" was
   invalid (different init streams) but immaterial (both timings → same result);
   the corrected evidence is stronger: 20/20 vs 3/12.
4. **FAILURE = PROGRESSIVE-OOD HIDDEN-STATE DRIFT.** Per/full gap (0.879 per vs
   0.124 full ≪ per⁹≈0.31) shows column-clustered errors; probe shows ‖h‖ drift
   + maxconf dip at beyond-training columns.

**Verdict:** NET-25's sharp-threshold law REFUTED; its mechanism (dense EOS →
boundary conditioning) SURVIVES on stronger ground. Barrier (e) closed: 12- and
19-sample distributions + determinism check. Open: shape of the 20→28 shift
(E=24 untested), real-scale transfer of the cure. Paper 70, issue #121. Now 26
network experiments. Assessment v26. Scripts: /tmp/exp_net_eos_sweep.py,
_verify.py, _dist.py; logs: /tmp/net26.log, _verify.log, _dist.log.

## Part 27 — EOS-Width Shift Is a Monotone Ramp, Not a Threshold (round-net-27, NET-27)

**Date:** 2026-08-14. **Status:** Machine-verified (ALL_DONE_NET27).
**Hypothesis:** NET-26 left the shape of the EOS-width P(cure) shift inside
(20,28) open ("E=24 would resolve") and proposed representational distinctness
as the control variable — implying the naive reading "any exclusive dim
suffices". Two questions: (1) sharp critical width vs gradual ramp? (2) is the
FIRST exclusive dim (E=21, exactly one) sufficient?

**Setup:** byte-identical NET-26 EOSWidthGRU (GRUCell(384→192), learned E-d EOS
zero-padded to 384, only E varies; same task/budget/eval). 24 arms: E ∈
{21,22,24,28} × 6 FRESH seeds (8–13, all new to the program, so every sample
is an independent draw and the merged E=20 / E≥28 anchors stay independent).

**Results (n=8 full, seeds 8–13):**
- **E=21:** 1.0000, 0.7715, 0.1567, 0.8926, 1.0000, 0.2656 — P(≥0.99) = 2/6,
  median ≈0.83, min 0.157. The ONLY width with both a full cure and a hard
  failure among fresh draws.
- **E=22:** 1.0000, 0.9912, 0.9482, 1.0000, 1.0000, 0.9990 — P(≥0.99) = 5/6,
  min 0.948 (no hard failure).
- **E=24:** 1.0000 ×6 — 6/6 clean.
- **E=28:** 1.0000 ×6 — 6/6 (combined with NET-26's E=28 ×2 → 8/8; E≥28 total
  26/26).
- Failure signature (E21 s10/s13): n=5 1.0000 → n=6 0.9995 → n=7 0.8203/0.8096
  → n=8 0.1567/0.2656 — same progressive-unroll collapse as NET-26's E20 s1.
- Probe reproduces NET-26 line-for-line: failures show hidden-norm DRIFT
  (cols 5→8 Δ+1.9~2.0) + maxconf dips (0.919/0.935, 0.929/0.899); all cures
  show flat norm (Δ<0.2) + maxconf 1.000, EOS-step norm settles.

**Findings:**
1. **EOS-WIDTH-SHIFT-IS-A-MONOTONE-RAMP — NO SHARP CRITICAL WIDTH IN (20,28].**
   Failure mass vs E: 75% (E=20) → 67% (E=21) → 17% (E=22, worst case a
   near-cure 0.948) → 0 (E=24) → 0 (E≥28). Worst case: 0.005 → 0.157 → 0.948 →
   1.0 → 1.0. Every width contributes to the ordering; no single width carries
   it.
2. **THE FIRST EXCLUSIVE DIM IS NOT SUFFICIENT** (naive distinctness reading
   REFUTED). E=21 (k=1) is still seed-fragile; the benefit is SUBLINEAR in k.
   Medians: 0.044 → 0.83 → 1.0 → 1.0 → 1.0.
3. **THE FAILURE MECHANISM IS WIDTH-INDEPENDENT.** Same progressive-unroll
   collapse, same clustered-column errors, same probe signature as E=20 —
   exclusive dims raise P(working boundary), not the boundary's kind.
4. **SATURATION BY E=24.** k=2 near-robust (no hard failure), k=4 certain
   (6/6), k≥8 stays certain (26/26 merged). Honest limit: n=6/width makes the
   E21→E22 P-jump alone not significant (Fisher ≈0.24); the law rests on the
   monotone ordering + merged anchors.

**Verdict:** gradual ramp, not a cliff — both sharp-threshold readings refuted.
NET-26's distinctness law refined: the boundary token needs its OWN parameter
subspace with ≥4 exclusive dims (k=2 near, k=1 fragile), a *reliability*
statement rather than a *capacity* one. Barrier (e) is the round's content
(E=21's 0.157-vs-1.0 spread is seed variance). Open: knee inside (21,24) —
E=23/25; mechanistic read of k=1 (measure the learned EOS exclusive-dim
coordinate at cure vs fail); real-scale transfer. Paper 71, issue #122. Now 27
network experiments. Assessment v27. Script: /tmp/exp_net_eos_shape.py; log:
/tmp/net27.log.

---

## Part 28 — NET-28: EOS-Width Knee at k=3 + Boundary Signal Is Not the Failure Locus

**Round-net-28.** Two open threads from NET-27, both closed in 18 arms
(ALL_DONE_NET28, /tmp/exp_net_eos_knee.py, log /tmp/net28.log): (1) the knee
inside (21,24) — Part A, E=23 (k=3) and E=25 (k=5) × seeds 8–13, seed-paired
with NET-27 (width the only variable); (2) the mechanistic read of the k=1
fragility — Part B, E=21 × 6 FRESH seeds (14–19), each printing the trained
EOS exclusive coordinate eos[20] (EOSCOORD). Architecture byte-identical to
NET-26/27 (EOSWidthGRU, GRUCell(384→192), only trainable EOS width varies).

**Part A — the knee.** E=23 **6/6** and E=25 **6/6** clean cures (all n=8 full
= 1.0000). P(cure) first reaches 100% at **k=3 (E=23)** — refined from NET-27's
"E=24 is the current first all-cure width". Full merged ramp: k=0 → 25% (12
samples), k=1 → 17–33% (12 samples), k=2 → 83%, **k=3 → 100%**, k=4 → 100%,
k=5 → 100%, k≥8 → 100% (E≥28 now 26/26).

**Part B — the k=1 mechanism (coordinate-dropout REFUTED).** eos[20] across
the 6 fresh E=21 arms: {cure +0.778, near-cure −0.912, FAIL −0.672, partial
+0.771, FAIL +0.812, partial +0.846}. **Pinned at |0.67–0.91| in ALL outcomes,
cure and fail alike** — an order above the mean digit-subspace coordinate
(0.17–0.25), ~3–5× the digit max. Prediction A ("the optimizer drops the
exclusive coordinate → silent E=20 fallback") is REFUTED: the boundary signal
is always present. The k=1 fragility is DOWNSTREAM of the EOS parameter — with
one exclusive dim the boundary step perturbs the hidden state along a single
direction, and whether BPTT-through-time shapes W_hh/W_ih so that direction
drives the hidden state back into the generalizing manifold at depth is
seed-fragile. k≥3 gives three+ independent boundary directions → robust
recovery (a *dimensionality of the boundary lever*). Exclusivity ratio leans
the same way (fails 1.30/1.78 vs cures 1.73/2.24) but overlaps at n=6 —
flagged, not asserted.

**Redundancy picture.** Every cure at k≥3 pins ALL its exclusive coords
(E=23: |0.52–0.66|; E=25: |0.46–0.55|), dominant over the digit subspace
(0.24–0.48). Exclusive capacity is used, not idle.

**Findings:**
1. **THE KNEE IS AT k=3.** P(cure) first reaches 100% at E=23; confirmed at
   k=4/5/8. No width in (20,23] is a sharp threshold — a crossing of a
   monotone curve.
2. **THE BOUNDARY SIGNAL IS PRESENT IN FAILURES (coordinate-dropout REFUTED).**
   eos[20] pinned |0.67–0.91| in all 6 fresh E=21 arms regardless of outcome;
   failures do NOT fall back to the E=20 input.
3. **THE FAILURE LOCUS IS DOWNSTREAM OF THE EOS PARAMETER.** k=1 = one boundary
   direction the recurrence must learn to use for depth-recovery — a
   dimensionality/fragility statement, not a presence/absence one. k=3+ =
   reliable.
4. **ALL EXCLUSIVE CAPACITY IS USED IN CURES** (k=3/5 cures pin every coord,
   dominant over digit subspace) — redundant boundary channels are
   load-bearing.

**Verdict:** NET-27's two open questions answered. Knee: k=3 (E=23). Mechanism:
Prediction B — the k=1 fragility is in the recurrent dynamics, not the EOS
parameter; the design rule sharpens to ≥3 exclusive dims (k=3 6/6, k=2 5/6
near-robust, k=1 17–33%). Barrier (e) is handled two ways (paired seeds 8–13
for the knee vs NET-27; fresh seeds 14–19 for the mechanism). Open: a causal
freeze-eos[20] test at a k=3 cure; k=3 rule transfer to the real causal LM;
~24 more E=21 arms for the exclusivity-ratio trend. Paper 72, issue #123. Now
28 network experiments. Assessment v28. Script: /tmp/exp_net_eos_knee.py; log:
/tmp/net28.log.

---

## Part 29 — NET-29: Causal Freeze — the Exclusive Boundary Channel Is Training-Time Load-Bearing (Internalization ∝ Cure Quality)

**Round-net-29.** The causal test NET-28's open (1) demanded. 12 arms, each a
SAME-SEED reproduction of a NET-28 arm (byte-identical EOSWidthGRU; trained
exclusive coords reproduce NET-28 to 3 decimals — every intervention attaches
to the exact published solutions). Inference-only manipulations of the trained
EOS exclusive coords at n=5/6/7/8 (fresh draws per arm × intervention,
teacher-forced; ctl re-baselines reproduce NET-28 outcomes). Part A: E=23
(k=3) × seeds 8–13, 7 interventions — ctl / zero3 (zero all 3 excl) / zero1@0/1/2 /
flip1 / scale0.1 (42 arm-interventions). Part B: E=21 (k=1) × seeds 14–19,
ctl / zero1 (12).

**Part A — the k=3 cures (n=8 full):** zero3 → {1.0000, 0.9995, 0.9995,
1.0000, 0.9971, **0.7041**} — the k=3 cure SURVIVES complete removal of the
exclusive block in 5/6 arms (≤0.3% scattered, never a collapse); s=13 is the
outlier (0.70, per 0.967 — partial degradation, not the E=20 hard-fragile
regime). zero1 (any single coord) → 0% in ALL 6; flip1 → 0% in all 6; scale0.1
→ 0% in 5/6 and 3% at s=13. s=13 = MAGNITUDE-ENSEMBLE dependence: collective
(2-of-3 suffices, full strength needs all three), magnitude-sensitive,
sign-insensitive, never individually load-bearing.

**Part B — the k=1 arms under zero1:** s=14 (cure) → 0.9717 vs 1.0000 (−2.8%,
~3 SE, uniform); s=15 (near-cure) → n5 0.9531 vs 1.0000 (−1 to −5% at short/
mid lengths); s=16/17/18/19 (fails/partials) → no-op (all |Δ| ≤ 1.2 SE).
**Eval-load-bearingness of the sole exclusive coord is PROPORTIONAL TO CURE
QUALITY**: it costs real accuracy where the recurrence internalized it, and is
a no-op where it failed — causally confirming NET-28 (the k=1 failure was
downstream).

**Findings:**
1. **THE EXCLUSIVE BOUNDARY CHANNEL IS (MOSTLY) TRAINING-TIME LOAD-BEARING.**
   At k=3 the trained recovery is self-sufficient: zero3 at eval costs ≤0.3%
   in 5/6; zero1 costs 0% in all 6; signs never matter; magnitude second-order.
   BPTT, seeing an unambiguous boundary every EOS step, shapes the weights so
   the depth-recovery no longer needs the exclusive input at inference — the
   k≥3 benefit is realized as SELF-SUFFICIENT DYNAMICS, not held at the input.
2. **INTERNALIZATION IS SEED-HETEROGENEOUS (1/6 stay eval-dependent).** s=13
   leans on the exclusive block as a magnitude-ensemble (zero3 0.70 / scale0.1
   0.97 / zero1 1.0000 / flip no-op); it has the LARGEST coords (|0.65–0.66|)
   — a magnitude→dependence hint, FLAGGED (n=6, 1 outlier). A single-seed
   "boundary doesn't matter at eval" claim is untrustworthy.
3. **AT k=1 THE SOLE COORD IS EVAL-LOAD-BEARING IN PROPORTION TO THE CURE.**
   Significant cost at cures (−1 to −5%), no-op at partials/fails. The k=1
   cure holds a thinner margin: its recovery needs the single channel at
   inference.
4. **THE k=3 RULE IS A TRAINING-TIME RULE.** The exclusive dims are a boundary
   teacher signal for the optimizer; an internalized k=3 answer path need not
   re-serve the exclusive token at inference.

**Verdict:** Prediction 2 (optimization-load-bearing) holds in the majority at
k=3 but not uniformly (1/6 ensemble-dependent); at k=1 the interaction is
monotone — eval-dependence ∝ internalization. The cleanest causal statement:
removal of the whole exclusive block costs ≤0.3% at 5/6 k=3 cures, and removal
of the sole coord is a no-op exactly where the k=1 model already failed
(causal confirmation of downstream-fragility). Barrier (e) is the round's
content (seed-heterogeneous internalization reported as a distribution, every
arm a byte-identical same-seed reproduction). Open: k=2 freeze test (is E=22
internalization intermediate — links the eval-dependence gradient to the
P(cure) ramp); magnitude→dependence trend (~24 more E=23 arms); REAL-SCALE
transfer of the training-time ≥3-exclusive-dims rule; pad384-hybrid parity.
Paper 73, issue #124. Now 29 network experiments. Assessment v29. Script:
/tmp/exp_net_eos_freeze.py; log: /tmp/net29.log.

---

## Part 30 — NET-30: INTERNALIZATION-SATURATES-AT-K=2 (k=2 freeze test; the missing middle)

**Hypothesis (round-net-30):** is k=2 (E=22, P(cure)=83%) internalization
INTERMEDIATE between k=1 (cures eval-dependent per NET-29) and k=3 (5/6
self-sufficient)? Secondary: within-width internalization ∝ cure quality (the
E=22 near-cures s=9/s=10 depend more than the full cures?).
**Design:** 12 same-seed reproductions of NET-27 arms, inference-only
interventions on the trained exclusive coords, fresh eval draws per arm ×
manipulation (ALL_DONE_NET30, /tmp/exp_net_eos_freezek2.py). Part A: E=22 ×
seeds 8–13, 6 interventions (ctl/zeroN/zero1@0/zero1@1/flip1@0/scale0.1).
Part B: E=21 × seeds 8–13, 2 interventions (ctl/zero1) — includes the TWO
NET-27 k=1 full cures (s=8, s=12). All ctl baselines reproduce the published
NET-27 outcomes on fresh draws (Part A {1.0000, 0.9888, 0.9399, 1.0000,
1.0000, 0.9980} vs {1.0, 0.991, 0.948, 1.0, 1.0, 0.999}; Part B {1.0000,
0.7622, 0.1606, 0.8892, 1.0000, 0.2734} vs {1.0000, 0.7715, 0.1567, 0.8926,
1.0000, 0.2656}).

### Findings

1. **k=2 is NOT intermediate — it matches k=3 (5/6 self-sufficient).** Zeroing
   the ENTIRE exclusive block at eval costs ≤0.010 in 5/6 E=22 arms (s=8/9/10/
   11/12; the two largest changes are POSITIVE — removal *helps* the imperfect
   s=10 arm, never breaks it). The 6th (s=13) is the SAME seed as the k=3
   outlier, with the same ensemble dependence (zeroN 0.7544, flip 0.7505,
   scale0.1 0.9067, zero1 no-ops) and the LARGEST coords of its width (0.701 vs
   ≤0.660). Eval-sufficiency of the boundary channel collapses between k=1 and
   k=2; NET-28's P(cure) ramp is a TRAINING-TIME success-rate effect only.
2. **The within-width ∝-quality prediction is REFUTED.** The worst E=22 arm
   (s=10, ctl 0.9399) is as self-sufficient as the full cures (zeroN +0.005,
   no-op; its only ~2 SE swings are positive). No internalization-vs-quality
   slope at fixed k=2.
3. **NET-29's "k=1 ∝-quality" law is REFUTED (honest correction).** Both fresh
   k=1 full cures (s=8, s=12) are fully self-sufficient — zero1 costs 0% at
   every length. Pooled over 12 k=1 arms (NET-29 seeds 14–19 + NET-30 seeds
   8–13): the dependences NET-29 reported (s=14 −2.8%, s=15 −1 to −5%) do not
   reproduce at a second seed set; fails are no-ops in EVERY arm of both rounds;
   successes split seed-heterogeneously (~1/2–2/3 self-sufficient).
4. **s=13 is a SEED-WIDE outlier, and its internal structure is
   width-conditional.** The same seed builds a boundary-dependent recovery at
   both k=2 and k=3, with the largest exclusive coords at both widths. But at
   k=3 it is sign-INSENSITIVE (flip no-op, 2-of-3-redundant) while at k=2 it is
   sign-SENSITIVE (flip −0.25; 2-of-2-redundant) — NET-29's "signs never
   matter" was a k=3 statement, not general.

**Verdict:** the round's hypothesis is REFUTED (k=2 is indistinguishable from
k=3), and so is the secondary ∝-quality prediction at fixed k. The honest
correction: NET-29's k=1 ∝-quality law was a 6-seed observation; the robust
invariant over 12 k=1 arms is that fails are always no-ops and successes are
seed-heterogeneous, with self-sufficiency rate rising with k (k=1 ~1/2,
k≥2 5/6). Barrier (e) is the round's content (seed-heterogeneity as a
distribution; the NET-29 refutation recorded as a correction). Open: REAL-SCALE
transfer of the training-time ≥2/≥3-exclusive-dims rule (frontier);
magnitude→dependence trend at ~24 more arms/width; the seed-trait-vs-width-trait
test (run NET-29's dependent k=1 seeds s=14/15 at E=23 — are they
ensemble-dependent there too?); pad384-hybrid parity. Paper 74, issue #125.
Now 30 network experiments. Assessment v30. Script: /tmp/exp_net_eos_freezek2.py;
log: /tmp/net30.log.

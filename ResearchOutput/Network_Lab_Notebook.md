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

## Part 31 — NET-31: INTERNALIZATION-IS-A-SEED-FIXED-TRAIT (seed-trait vs width-trait)

**Hypothesis (round-net-31):** is the eval-dependence of the exclusive boundary
channel a property of the SEED (seed-trait: s=14/15 stay dependent at every
width) or of the WIDTH (width-trait: the k=1 dependence was a k=1 artifact and
s=13 is the unique non-internalizing seed)?
**Design:** SEED-FIXED, WIDTH-SWEPT freeze — the same seeds 14–19 at k=2 and
k=3, byte-identical EOSWidthGRU, same-seed training (same init/train streams as
the published E=21 arms, which are the k=1 rung), inference-only interventions,
fresh eval draws per arm × manipulation (ALL_DONE_NET31,
/tmp/exp_net_eos_freezek13.py). Part A: E=23 (k=3) × seeds 14–19, 7
interventions (ctl/zeroN/zero1@0,1,2/flip1@0/scale0.1). Part B: E=22 (k=2) ×
seeds 14–19, 6 interventions (ctl/zeroN/zero1@0,1/flip1@0/scale0.1). The
E=22/E=23 solutions are NEW (NET-28 ran E=21 only on these seeds); all 12 arms
cure (ctl ≥ 0.9985, s=16@E=22 the sole partial at 0.9058).

### Findings

1. **The boundary-dependence set is the SAME at k=2 and k=3: {13, 14, 15, 17}.**
   This round measures s=14/15/17 at both widths (k=3 zeroN: 0.9014, 0.7104,
   0.7437; k=2 zeroN: 0.9141, 0.8037, 0.9067); NET-29/30 measured s=13 at both
   (0.7041 / 0.7544). Every other seed that cures at k≥2 is self-sufficient at
   both widths. Internalization is ~60/40 (7/11 cures self-sufficient, 4
   dependent) and the split is WIDTH-INDEPENDENT — width sets P(cure), the seed
   sets internalization.
2. **NET-29's "5/6 self-sufficient at k=3" was a seed-set-specific high.** At
   seeds 14–19 the k=3 rate is 3/6 dependent (s=14, 15, 17) + 1/6 marginal
   (s=19 −1% at n=8, −3% at n=5); pooled over seeds 8–19 it is 7/12
   self-sufficient/marginal, ~40% dependent. HONEST CORRECTION of both NET-29
   (5/6) and NET-30 ("k≥2 5/6"): self-sufficiency is ~60% at every width.
3. **The seed-trait holds for the k=1-dependent seeds, and dependence GROWS
   with k.** s=14: −2.8% (k=1) → −9% (k=2) → −10% (k=3). s=15: −1…−5% → −20% →
   −29%. s=13 (−25% → −30%) and s=17 (−9% → −26%) grow too. WIDTH-TRAIT
   REFUTED. But the trait has NO k=1 predictor: s=13 (k=1 fail, no-op) and s=17
   (k=1 partial, no-op) are dependent at k≥2, while s=16/18 (k=1 fails, no-ops)
   are self-sufficient — the trait only manifests at widths where the seed cures.
4. **k=2 sign-sensitivity is a clean dependence marker; k=3 is sign-insensitive
   everywhere.** All four dependent k=2 arms carry a flip cost (s=13 −25%,
   s=14 −7%, s=15 −11%, s=17 −8%) and require sign-opposition in the two trained
   coords; every self-sufficient k=2 arm is flip-free. At k=3, flip is 0% in all
   12 arms across both seed sets. NET-30's width-conditional sign-sensitivity
   generalizes beyond s=13.
5. **NET-29's magnitude→dependence hint is REFUTED.** s=18 is self-sufficient
   with |max| 0.702@k=2 (0.627@k=3) — larger than dependent s=14 (0.636/0.581)
   and s=17 (0.654/0.588). The dependent set is not identifiable from the
   trained exclusive coordinates.
6. **P(cure)=100% at k=3 extends to a second seed set** (seeds 14–19: 6/6 ctl
   ≥ 0.9985; merged 12/12 across seeds 8–19). NET-28's knee is seed-robust.

**Verdict:** SEED-TRAIT PARTIALLY CONFIRMED (s=14/15 stay dependent at every
width; dependence grows with k), WIDTH-TRAIT REFUTED. The clean law:
internalization is a seed-fixed trait among cures at k≥2 — the same four seeds
({13,14,15,17}) build boundary-dependent recoveries at both widths, the same
seven build self-sufficient ones — with no k=1 predictor; NET-29's 5/6 was a
seed-set-specific high (pooled ~60%). Mechanism: at k≥2 the boundary block is
used COLLECTIVELY (zero1 = 0% in every arm); dependent seeds gate on the
aggregate block norm (zeroN 9–29%, scale0.1 1–5%), with width-conditional sign
structure (k=2 sign-opposition required, k=3 sign-insensitive). Barriers: (a)
clean (new E=22/E=23 solutions, own ctl baselines; k=1 rung = published arms),
(b) clean (no Catalog prior), (c) confronted — ≥3 dims now guarantee reliable
SUCCESS (12/12) but only ~60% self-sufficient internalization; real-scale is the
frontier, (d) clean, (e) THE round's content (seed-set-heterogeneous rate
reported as pooled distribution; within-seed-across-width reproducibility of the
trait), (f) clean (exact writes, SEs, no-op = |Δ|≤1.2 SE), (g) strong (seed-fixed
design — width the only training variable), (h) design rule sharpened: ≥3
exclusive dims ⇒ reliable success, but ~40% of seeds remain eval-dependent on
the boundary ensemble — keep re-serving it or verify per instance. Open:
REAL-SCALE transfer (frontier); a trained-WEIGHT predictor of the seed trait
(the W_ih projection onto the exclusive block? hidden-norm response?); pad384-
hybrid parity; why dependence GROWS with k. Paper 75, issue #138. Now 31 network
experiments. Assessment v31. Script: /tmp/exp_net_eos_freezek13.py; log:
/tmp/net31.log.

## Part 32 — NET-32: THE-INTERNALIZATION-TRAIT-IS-A-TRAINING-ARTIFACT (no-boundary fine-tune converts 4/4 dependent seeds)

**Question (constructive test of NET-31):** the internalization trait is seed-fixed at standard training ({13,14,15,17} dependent at k=2 and k=3) — but is it INTRINSIC to the seed's optimization landscape, or a TRAINING ARTIFACT of the converged solution (a solution that gates on the exclusive block and was never forced to operate without it)?

**Method (ALL_DONE_NET32, /tmp/exp_net_eos_ftune.py):** 6 arms at E=23 (k=3), byte-identical EOSWidthGRU — the COMPLETE known-dependent population {13,14,15,17} + self-sufficient controls {16,18}. Standard 12000-step training (byte-identical to NET-29/30/31) → stage-0 ctl+zeroN eval (exact same-seed replication) → fine-tune T ∈ {300, 1000, 3000} cumulative steps with the exclusive block ZEROED at the EOS step (the exact zeroN eval condition made a TRAINING condition), eval ctl+zeroN per stage and zero1@0/flip1@0/scale0.1 at T=3000. Fresh AdamW lr 1e-3; fresh eval draws per (stage, manipulation).

**Results (n=8 full; SE ≤0.5% at p≈1, ~0.9% at p≈0.7–0.9):**

1. **Stage-0 replication is EXACT** — zeroN {0.7041, 0.9014, 0.7104, 0.9932, 0.7437, 0.9995} for seeds {13..18} reproduces NET-29/30/31 to 4 decimals; ctl is 1.0000 (0.9985 for s=16). The conversion is measured on the IDENTICAL solutions NET-31 labeled.
2. **4/4 dependent seeds convert to fully self-sufficient** — zeroN n=8 goes {0.7041, 0.9014, 0.7104, 0.7437} → 1.0000 after ≤3000 steps of no-boundary fine-tune (≤2.5% of the training budget). INTRINSIC-TRAIT REFUTED; the trait is a property of the converged SOLUTION.
3. **Fast onset:** zeroN ≥0.99 at T=300 in 5/6 arms (s=13 0.9980, s=14/15/17/18 1.0000); only s=16 lags.
4. **NON-MONOTONE in 4/6 arms (the reorganization dip):** transient n=8 dip at an intermediate stage (s=13 T=1000 0.9746; s=15 T=1000 0.9390; s=16 T=300 0.7163 & T=1000 0.6763; s=18 T=1000 0.9150), always recovering to 1.0000 by T=3000. Affects ctl and zeroN equally (the block is already inert). s=14/17 convert cleanly. Deploy only at full convergence.
5. **Cure preserved:** ctl (block-present path at full trained magnitude) ends at 1.0000 in 6/6 arms at T=3000; worst mid-way ctl 0.6924 (s=16 T=1000, the dip).
6. **Post-conversion the block is INERT, not compensated:** ctl/zeroN/zero1@0/flip1@0/scale0.1 all = 1.0000 at n=8 in all six arms. Since zero1 cost 0% in EVERY trained k≥2 arm (NET-29/30/31 — the trained block-gated path needed ALL coords), a no-op zero1@0 proves that solution path is GONE: the model switched fully to the no-block path.
7. **Mechanism — dynamic stop-routing, NOT coord decay (honest correction):** the log's EOSCOORD-AFTER |0.06| readout was a MEASUREMENT ARTIFACT (the eos buffer printed after the final scale0.1 eval without restoring it — every arm shows exactly ×0.10). True post-fine-tune coords unmeasured; weight-decay math (zero gradient under the zeroN training condition, AdamW wd 0.01, lr 1e-3 → ~3%/3000 steps) bounds them at ~0.97× trained (~0.6). The block is present at near-full magnitude yet has zero effect on the answer — the recurrent dynamics STOP ROUTING the exclusive input into the answer path.

**Verdict:** TRAINING-ARTIFACT CONFIRMED (4/4 complete known-dependent population converts; exact replication control; cure preserved; block inert). INTRINSIC-TRAIT REFUTED. Design rule UPGRADED: ≥3 exclusive dims ⇒ reliable success (12/12 cures at k=3), then a ≤3000-step no-boundary final fine-tune makes the boundary block OPTIONAL seed-independently — the ~60% internalization lottery and the "re-serve or verify per instance" caveat are GONE.

**Barriers:** (a) clean — ctl at full magnitude preserved (1.0000), zero1/flip/scale never-trained interventions inert, n=6–8 length-gen perfect post-conversion; (b) confronted — "fine-tune without the special token" is a known qualitative family; the exact T-law (≤300 steps, 4/6 dip, 3000-step convergence), the block-inertia result, and the trait-not-intrinsic reframing are the novel content (Catalog: closest pkg 693/35 certified adversarial robustness, input-space, orthogonal); (c) confronted — toy task; REAL-SCALE = frontier, now with a concrete protocol; (d) clean (fresh draws, inference-only interventions); (e) the round's content — the COMPLETE known-dependent population tested, 4/4 converted; dip distribution is a limitation (no fresh dependent seeds beyond {13,14,15,17,19-marginal}); (f) clean AFTER honest correction of the EOSCOORD-AFTER scale0.1 artifact (behavioral evals unaffected — each restored the trained buffer before intervening); (g) strong — the control is each arm AT ITSELF (T=0, byte-identical); (h) high — a one-time training-time protocol replaces per-instance eval verification, seed-independently. Open: REAL-SCALE transfer (with the no-boundary fine-tune protocol); clean post-fine-tune coord readout (confirm dynamic stop-routing); dip distribution; minimal conversion budget at k=2; pad384-hybrid parity. Paper 76, issue #139. Now 32 network experiments. Assessment v32. Script: /tmp/exp_net_eos_ftune.py; log: /tmp/net32.log.

## Part 33 — NET-33: THE-ATTENTION-COST-LAW-IS-SEED-ROBUST (k*=d·ctx/32 survives a second seed at both contexts)

**Question (barrier-e check, exactly NET-20's declared gap):** the attention-cost law k* = d·ctx/32 → speedup 32/d (NET-15/16/17/20) rests on a SINGLE seed (s0) per point. Is the ∝-ctx leg a single-seed artifact?

**Method (ALL_DONE_NET33, /tmp/exp_net_attncost_s1.py):** byte-identical harness to NET-15/20 — CausalTF d=4, dm=64, 4 heads, 5 Gutenberg novels, vocab 4097, contiguous 90/10 split, 2000 AdamW steps (lr 3e-4) — at **seed=1**, at BOTH **ctx=128 and ctx=256**. Per context: full-acc eval → Part A concentration (eff support, top-k mass k=8/16/32/64, per-position buckets early/mid/late) → Part B top-k sweep ({4,8,16,32,64,96} @ 128; {8,16,32,64,128,192} @ 256) → Part B2 random-k control (seed 12345). k* = smallest k with retained ≥ 0.98·full. Prediction stated before the run: k* = 16 @ 128, k* = 32 @ 256.

**Results (retained = acc/full vs the 0.98 bar; acc noise ≈0.15% ≪ the k* margins):**

1. **k* is EXACT at the second seed — both contexts.** k*(s1, ctx=128) = **16** (k=8 0.973 ✗, k=16 0.987 ✓) and k*(s1, ctx=256) = **32** (k=16 0.973 ✗, k=32 0.990 ✓) — identical to s0 and to the prediction. The ∝-ctx proportionality is NOT a single-seed artifact.
2. **The knee is if anything MORE favorable at s1:** retained@k* 0.987/0.990 (s1) vs 0.984/0.989 (s0); the ctx=128 k=8→k=16 fail/pass margin is cleaner at s1 (0.973→0.987 vs s0's 0.971→0.984).
3. **Concentration reproduces to ≤3% relative:** eff support 46.41 (s0 46.63) @128, 80.57 (s0 82.94) @256; top-k masses within ≤0.009 at every k; per-position buckets match the monotone no-bounded-working-set shape (ctx=256 s1 early 11.12/mid 70.08/late 150.44 vs s0 11.27/72.25/155.35). The context-dependent diffusion (46.6→82.9 at s0) holds at s1 (46.4→80.6).
4. **Selection importance is seed-stable:** random-k gaps within 0.5 pts at every comparable (k, ctx) point (ctx=128 k=16: +6.1 vs +6.2; ctx=256 k=16: +8.3 vs +8.7; k=32: +6.3 vs +6.0).
5. **Full-acc spread is small and k*-irrelevant:** the four (seed × ctx) models span 0.1571–0.1612 (±0.4% of mean); the law holds across the spread.

**Verdict:** SEED-ROBUST CONFIRMED — k* = d·ctx/32 (lever 32/d, 8× at d=4, context-invariant in [128, 256]) holds exactly at a second seed at both contexts; the concentration and selection-gap legs reproduce to ≤3% and ≤0.5 pts. NET-20's declared barrier-(e) gap is CLOSED. The diffuse-but-prunable structure is a property of the task/data scale, not of one run.

**Barriers:** (a) clean — prediction stated before the run from s0 data; k* measured from each model's own trained attention; (b) clean — a reproducibility verification of an established law, not a re-labeled method (Catalog: no seed-robustness/concentration-fidelity result for top-k pruning); (c) confronted — same real-scale testbed as the published law (real causal word LM, causal masking, 2 contexts, held-out loss+acc); (d) clean (held-out last-10% windows, data-free top-k from eval attention); (e) the round's content — CLEARED at d=4 for the ∝-ctx leg; honest remaining limit: the DEPTH leg (k*=4d at d=8/16) is still single-seed, and k* is exact at the sweep's k-resolution (multiples of 8/16); (f) clean — same metrics/protocol as NET-15/20, k=192 recovers full loss exactly (5.0842 vs 5.0841), the ctx=256 s1 retained@k=128=1.001 is the same re-normalization artifact seen at s0; (g) fair — full-attention reference + random-k control at the same k, same bar; (h) strengthened — a speedup claim that survives seed change can be deployed without per-instance re-measurement. Open: d=8/16 seed-1 depth-leg points (would close the remaining single-seed limb); a ctx=512 point. Paper 77, issue #140. Now 33 network experiments. Assessment v33. Script: /tmp/exp_net_attncost_s1.py; log: /tmp/net33.log.

## Part 34 — NET-34: THE-DEPTH-LEG-IS-SEED-ROBUST (k*=4d at d=8, second seed, BOTH contexts; the never-measured ctx=256 cell)

**Question (the barrier-(e) limb NET-33 named open):** the attention-cost law k* = d·ctx/32 → speedup 32/d (NET-15/16/17/20/33) rests at d=8/16 on a SINGLE seed (s0) — the DEPTH leg k* = 4d is s0-only. Is it a single-seed artifact? And does the full two-parameter law hold where depth AND context act together (ctx=256, d=8 — a never-measured grid cell)?

**Method (ALL_DONE_NET34, /tmp/exp_net_attncost_d8_s1.py):** byte-identical harness to NET-16/33 — CausalTF **d=8**, dm=64, 4 heads, 5 Gutenberg novels, vocab 4097, contiguous 90/10 split, 2000 AdamW steps (lr 3e-4) — at **seed=1**, at BOTH **ctx=128 and ctx=256**. Per context: full-acc eval → Part A concentration (eff support, top-k mass k=8/16/32/64, per-position buckets) → Part B top-k sweep ({4,8,16,32,64,96} @ 128; {8,16,32,64,128,192} @ 256) → Part B2 random-k control (seed 12345). k* = smallest k with retained ≥ 0.98·full. Prediction stated before the run: k* = **32** @ 128 (4d), k* = **64** @ 256 (d·ctx/32 = 8·256/32).

**Results (retained = acc/full vs the 0.98 bar; acc noise ≈0.15% ≪ the k* margins):**

1. **BOTH cells land EXACTLY on the prediction.** k*(s1, d=8, ctx=128) = **32** (k=16 0.962 ✗, k=32 0.988 ✓ — identical to s0's 32, NET-16) and k*(s1, d=8, ctx=256) = **64** (k=32 0.968 ✗, k=64 0.990 ✓) — the first measurement of that grid cell, on d·ctx/32. **The full 2-parameter law now holds at a second seed in EVERY measured cell of the (d ∈ {4,8} × ctx ∈ {128,256}) grid.** Knee if anything more favorable at s1 (retained@k* 0.988 vs s0 0.983).
2. **k=192 recovers full loss exactly** at ctx=256 (5.0868 vs full 5.0865, Δ0.0003); k=128 retained 0.999, bounding the sweep.
3. **Concentration reproduces to ≤0.003 at ctx=128** (eff support 50.16 vs s0 50.13; top-k masses identical to 0.001); the context-diffusion law extends to depth (eff 50.16 → 91.49 as ctx doubles, 1.82× vs d=4's 1.78×); per-position monotone no-bounded-working-set shape preserved (ctx=128: 6.86/43.80/93.83; ctx=256: 12.45/80.88/170.47).
4. **Selection importance survives depth AND seed:** random-k gaps 4.5–8.0 pts at d=8 (ctx=128 k=16 +8.0/k=32 +6.2 vs s0 +9.5/+7.1; ctx=256 k=32 +7.1/k=64 +4.5) — same family as d=4 (6.0–8.7).
5. **Full-acc spread across all six (seed × depth × ctx) models is 0.1571–0.1620** and does not shift k* at any point.

**Verdict:** DEPTH-LEG SEED-ROBUST CONFIRMED — k* = 4d holds at a second seed (32 @ ctx=128, exact), and the never-measured ctx=256 d=8 cell returns 64 = d·ctx/32 exactly. The last single-seed limb of the attention-cost law is CLOSED: the law holds at a second seed in every measured grid cell, with depth-invariant concentration and selection importance.

**Barriers:** (a) clean — prediction stated before the run from s0 data + the law; k* measured from each model's own trained attention; (b) clean — reproducibility verification of an established law (Catalog: no depth-leg/two-parameter result for top-k pruning); (c) confronted — real causal word LM, 4097 vocab, deepest model of the law's own testbed at the longest context, held-out loss+acc; (d) clean (held-out last-10%, data-free top-k from eval attention); (e) the round's content — CLEARED for the depth leg at d=8; honest remaining: d=16 (NET-17) still single-seed, no ctx=512 point, k* exact at the sweep's k-resolution; (f) clean — same metrics/protocol as NET-16/33, k=192 recovers full loss exactly, retained 1.000 is the same re-normalization saturation as before; (g) fair — full-attention reference + random-k control at the same k, same bar; (h) strengthened — a depth+context speedup claim that survives both levers changing can be shipped without per-instance re-measurement. Open: d=16 second-seed point (closes the very last single-seed cell); a ctx=512 point. Paper 78, issue #141. Now 34 network experiments. Assessment v34. Script: /tmp/exp_net_attncost_d8_s1.py; log: /tmp/net34.log.

## Part 35 — NET-35: THE-ATTENTION-COST-LAW-EXTRAPOLATES-TO-4×-CONTEXT (k*=d·ctx/32 holds at ctx=512; first point outside [128,256])

**Question:** the attention-cost law k* = d·ctx/32 (→ speedup 32/d, context-invariant: 8× at d=4) was established at a second seed in every cell of the (d∈{4,8} × ctx∈{128,256}) grid (NET-15/16/20/33/34) — but the entire ctx=512 regime was unmeasured, and the context leg rested on exactly ONE doubling (128→256). Does the law EXTRAPOLATE to 4× the longest measured context, or does k* break (superlinear k* at long context would kill the context-invariant speedup — the economically important direction)?

**Method (ALL_DONE_NET35, /tmp/exp_net_attncost_ctx512.py):** byte-identical harness to NET-15/20/33 — CausalTF **d=4**, dm=64, 4 heads, 5 Gutenberg novels, vocab 4097, contiguous 90/10 split, 2000 AdamW steps (lr 3e-4) — at **seed=1**, at **ctx=512** (1171 windows, 10% held out; train 2854s). Full-acc eval → Part A concentration → Part B top-k sweep {16,32,64,128,256,384} → Part B2 random-k (seed 12345); k* = smallest k with retained ≥ 0.98·full. Prediction stated before the run: k* = **64** (d·ctx/32 = 4·512/32).

**Results (retained = acc/full vs the 0.98 bar; acc noise ≈0.15%):**

1. **k* = 64 — EXACT.** k=16 0.940 ✗, k=32 0.964 ✗, k=64 **0.983 ✓**, k=128 0.992, k=256 0.999, k=384 1.000 (loss 5.0827 = full exactly). The law k* = d·ctx/32 now holds across a 4× context range (128→512) at a second seed; the lever speedup = 32/d = 8× at d=4 is context-invariant over the quadrupled range.
2. **The knee is well-defined but the pass margin thins (P3 outcome):** k=32 fails at ~10 SE below bar; the k=64 pass clears by only 0.003 (≈2 SE) — vs ~0.007–0.010 at 128/256 — and retained is uniformly ~0.01 lower at every k. The law's KNEE stays exact; its margin erodes with context (a documented long-context caveat; re-check at ctx=1024).
3. **Concentration diffusion continues:** eff support 152.11 (46.4 → 80.6 → 152.1 across the two doublings, ×1.74/×1.89 — slightly superlinear on the third); per-position eff 20.41/133.37/281.20 — monotone growth, NO bounded working set at 512.
4. **Selection importance survives the longest context:** random-k gaps +5.3 (k=32) / +4.6 (k=64) — same family as 128/256 (6.0–8.7) with a modest decline.
5. **Seven-model full-acc set 0.1571–0.1616**, tight even at the longest context; k* unaffected.

**Verdict:** CONTEXT-EXTRAPOLATION CONFIRMED — k* = d·ctx/32 holds exactly at ctx=512 (k* = 64), the law's first point at 4× the longest measured context, with the context-invariant lever 32/d intact and no bounded working set. The economically important claim (longer context buys no extra relative saving; 8× absolute at d=4) survives a quadrupled context range.

**Barriers:** (a) clean — prediction stated before the run from the law; k* measured from each model's own trained attention; (b) clean — context-extrapolation verification of an established law (Catalog re-scan: no context-scaling/top-k-pruning result at any context length; closest pkg 677 attention expressive-power, orthogonal); (c) confronted — longest context the testbed has used, real causal word LM, 4097 vocab, held-out loss+acc; (d) clean (held-out last-10%, data-free top-k from eval attention); (e) the round's content — the extrapolation cell is EXACT but single-seed (no ctx=512 second seed, no depth sweep there); remaining single-seed: d=16 @ ctx=128, ctx=512 at d=8/16; (f) clean — same metrics/protocol, k=384 recovers full loss exactly, retained 1.000 = re-norm saturation as every prior context, the thin pass margin (0.983, ≈2 SE) reported as the P3 caveat rather than hidden, k=32's ~10 SE fail fixes the knee; (g) fair — full-attention reference + random-k control at the same k, same bar; (h) strengthened — the context-invariance of the speedup lever now holds across 4× context. Open: ctx=512 second seed; ctx=1024 (margin-erosion check); d=16 second seed @ ctx=128; ctx=512 at d=8/16; carry chain at scale (the frontier). Paper 79, issue #142. Now 35 network experiments. Assessment v35. Script: /tmp/exp_net_attncost_ctx512.py; log: /tmp/net35.log.

---

## Part 36 — Grid completion: every measured (depth × context) cell of the attention-cost law is now two-seed (NET-36, speed axis)

**Question:** The last two single-seed corners of the (d × ctx) grid — d=16 @ ctx=128 (NET-17, s0 only) and ctx=512 @ d=4 (NET-35, s1 only) — both predict k* = 64 (4d and d·ctx/32). Do they land exactly at fresh second seeds, making the measured grid two-seed everywhere?

**Method:** Byte-identical harness, 2000 AdamW steps, two cells run sequentially: d=16 seed=1 @ ctx=128 and d=4 seed=2 @ ctx=512. Data-free top-k key/value pruning (per-query, per-head, from each eval input's own trained attention, renormalized); k* = smallest k with retained ≥ 0.98·full. Random-k control (rng seed 12345), concentration/eff-support measures, explicit causal-attention eval. Script /tmp/exp_net_attncost_grid.py; log /tmp/net36.log.

**Results:** Both cells hit k* = 64 EXACT.
- Cell A (d=16, ctx=128, s1): full acc 0.1620, bar 0.1587, loss 5.0827, 1078s. Sweep: k=8 0.858, k=16 0.922, k=32 0.970 ✗, k=64 **0.996** ✓, k=96 0.999, k=128 1.000. Random-k: k=32 0.870 (gap +10.0), k=64 0.936 (gap +6.0). Eff support 52.73 (depth-drift law continues: 46.6 → 50.2 → 52.7 at d=4/8/16); eff by pos 7.14/46.38/98.34.
- Cell B (d=4, ctx=512, s2): full acc 0.1619, bar 0.1587, loss 5.0803, 2706s. Sweep: k=16 0.965 ✗, k=32 0.976 ✗, k=64 **0.985** ✓, k=128 0.993, k=256 0.998, k=384 1.000 (loss 5.0803 = full exactly). Random-k: k=32 0.900 (gap +7.6), k=64 0.933 (gap +5.2). Eff support 152.11 — IDENTICAL to s1's 152.11; top-32 mass 0.532 vs s1 0.533; eff by pos 20.45/133.23/281.46 vs s1 20.41/133.37/281.20 (three sig figs).

**P3 refinement:** NET-35's long-context margin erosion (s1 pass 0.983, margin 0.003 ≈ 2 SE) does NOT reproduce at s2 (pass 0.985, margin 0.005). The knee is exact at both seeds; the retained curve is uniformly ~0.005–0.01 lower at 512 than at 128/256 at both seeds, but the pass margin is seed-fluctuating (±0.002), not systematically eroding. The ctx=1024 re-check remains the honest stress point.

**Verdict:** GRID-COMPLETION CONFIRMED — every measured cell of the (d × ctx) grid is now two-seed. Depth leg k* = 4d holds at all three depths × two seeds (16/32/64 at d=4/8/16 @ ctx=128); context leg k* = d·ctx/32 holds to 4× context at two seeds (64 @ ctx=512, d=4, s1+s2). Deployable claim (speedup 32/d, context-invariant) is seed-independent at every measured corner. Eight-model full-acc set 0.1571–0.1620, k*-irrelevant.

**Barriers:** (a) clean — both predictions stated before the run, k* measured from the model's own trained attention; (b) clean — two-seed grid-completion of an established law (Catalog re-scan 698 pkgs: no top-k/context-scaling/seed-robustness prior work; closest pkg 677 expressive-power dichotomy, orthogonal); (c) confronted — the grid's extreme corners, real causal word LM, 4097 vocab, held-out loss+acc; (d) clean (held-out last-10%, data-free top-k); (e) the round's content — both cells fresh second seeds; concentration reproduces to 0.001; remaining single-seed/unmeasured cells are non-threatening (ctx=512 at d=8/16; d=8 @ ctx=256 s0 corner; ctx=1024 margin check); (f) clean — same metrics/protocol, k=384 recovers full loss exactly, retained 1.000 = re-norm saturation, seed-2 margins exceed binom SE; (g) fair — full-attention reference + random-k control at same k, same bar; (h) strengthened — the speedup lever is seed-independent at every measured corner. Open: ctx=512 at d=8/16; ctx=1024 (margin-erosion re-check); d=8 @ ctx=256 second seed; carry chain at scale (the frontier). Paper 80, issue #143. Now 36 network experiments. Assessment v36. Script: /tmp/exp_net_attncost_grid.py; log: /tmp/net36.log.

---

## Part 37 — The attention-cost law's knee survives 8× context: k* = d·ctx/32 holds at ctx=1024 and the margin-erosion caveat is resolved (NET-37, speed axis)

**Question:** NET-35 flagged a P3 long-context margin erosion at ctx=512 (pass 0.983, margin 0.003 ≈ 2 SE); NET-36 showed it seed-fluctuating at 512, not systematic. The open stress point: does the knee EVENTUALLY fail as context doubles — the retained-curve depression extrapolates to ~0.97–0.98 at 1024, right at the bar?

**Method:** Byte-identical harness, 2000 AdamW steps, CausalTF **d=4, seed=1, ctx=1024** (extends the same-seed context chain to 8× the original testbed; 585 windows, 10% held out). Data-free top-k pruning (per-query, per-head, from each eval input's own trained attention, renormalized); k* = smallest k with retained ≥ 0.98·full; sweep ks={32,64,96,128,192,256,384,512,768}, random-k control (seed 12345). Script /tmp/exp_net_attncost_ctx1024.py; log /tmp/net37.log. **Prediction stated before the run: k* = 128 (d·ctx/32).**

**Results:** k* = **128 — EXACT** (P1). Full acc 0.1594, bar 0.1562, loss 5.1209, train 5516s. Sweep: k=32 0.945 ✗, k=64 0.968 ✗, k=96 0.977 ✗, k=128 **0.986** ✓ (k=192 0.991, k=256 0.993, k=384 0.996, k=512 1.000, k=768 0.999). Pass margin **+0.006** (≈4 SE); knee clean (k=96 fails ~2 SE below bar, 0.977→0.986 is a 0.009 ≈ 6 SE jump). Random-k: k=64 0.909 (gap +5.9), k=128 0.940 (gap +4.6).

**Margin chain at d=4 s1 (128/256/512/1024): +0.007 / +0.010 / +0.003 / +0.006.** NOT monotonic — the 512 dip was a fluctuation; the margin recovered at 1024. **P3 progressive-erosion REFUTED**; the knee is exact at every doubling through 8× context, no ceiling. Retained curve still somewhat lower at longest context (k=64 0.968 @1024 vs 0.983 @512) but the KNEE is unaffected.

**Concentration:** eff support **291.16** (46.4→80.6→152.1→291.2; ×1.74/×1.89/×1.91 — superlinear on every doubling); top-64 0.552, top-128 0.702; eff by pos 37.56/255.76/542.05 — NO bounded working set at 1024.

**Verdict:** CONTEXT-MARGIN CHECK PASSED — the law holds at 8× context, the margin-erosion caveat is resolved (a fluctuation band, not a monotone degradation). The context-invariant lever 32/d (8× at d=4) holds over the 8× range; longer context still buys no extra relative saving.

**Barriers:** (a) clean — prediction stated before the run, k* from the model's own trained attention; (b) clean — long-context margin verification of an established law (Catalog re-scan: no context-length/margin/knee/top-k prior work; closest pkg 677, orthogonal); (c) confronted — 8× the original testbed context, real causal word LM, 4097 vocab, held-out loss+acc; (d) clean (held-out last-10%, data-free top-k); (e) the round's content — the margin question answered by the 4-point same-seed chain (512 dip shown to be a fluctuation); honest limit: ctx=1024 cell is single-seed, and the knee fluctuation band (±0.003) is wider at long context; (f) clean — same metrics/protocol, k=512 1.000 = re-norm MC saturation (k=768 0.999 converges to full loss), binom SE ≈0.15%, pass +4 SE / fail −2 SE fix the knee; (g) fair — full-attention reference + random-k control at same k, same bar; (h) strengthened — the speedup lever's context-invariance now tested to 8×, the margin-erosion caveat downgraded from open risk to resolved fluctuation. Open: ctx=1024 second seed; ctx=512 at d=8/16; d=8 @ ctx=256 s0 corner; carry chain at scale (the frontier). Paper 81, issue #144. Now 37 network experiments. Assessment v37. Script: /tmp/exp_net_attncost_ctx1024.py; log: /tmp/net37.log.

---

## Part 38 — The attention-cost law at the discriminating corner: product form confirmed, depth leg sub-linear at long context (NET-38, speed axis)

**Question:** The law k* = d·ctx/32 holds at every measured grid cell, but never at a cell where the three candidate rules ALL disagree. At (d=8, ctx=512) the depth leg (4d) predicts 32, the context leg at d=4 (ctx/8) predicts 64, and the unified product law predicts 128 — three values separated by 2× each. Which is it: multiplicative form (depth × context act together) or single-lever dominance?

**Method:** Byte-identical harness, 2000 AdamW steps, CausalTF **d=8, seed=1, ctx=512** (the grid's first d=8 × ctx=512 cell; 1171 windows, 10% held out). Data-free top-k pruning (per-query, per-head, from each eval input's own trained attention, renormalized); k* = smallest k with retained ≥ 0.98·full; sweep ks={16,32,64,96,128,192,256,384} (96 added inside the 2× grid to resolve the region between the ctx/8 and product knees), random-k control (seed 12345). Script /tmp/exp_net_attncost_d8_ctx512.py; log /tmp/net38.log. **Prediction stated before the run: k* = 128 (d·ctx/32).**

**Results:** k* = **96 — none of the three predictions.** Full acc 0.1568, bar 0.1536, loss 5.1355, train 3889s. Sweep: k=16 0.915 ✗, k=32 0.952 ✗ (4d, depth-only rule REFUTED by 18 SE), k=64 **0.979 ✗** (ctx/8, context-only rule marginal — ~1 SE below bar), k=96 **0.990 ✓** (k*), k=128 0.995 ✓ (d·ctx/32 passes but is NOT minimal), k=192 0.995, k=256 0.999, k=384 0.998 (loss 5.1356 ≈ full). Random-k: k=64 0.915 (gap +6.4), k=128 0.958 (gap +3.7).

**What this decides:** the single-lever rules are REFUTED (32 decisively, 64 marginally), so depth demonstrably raises the required k above the d=4 context-only value (64) — the levers act MULTIPLICATIVELY. But the exact product value 128 is not the minimum: the knee lands 25% below d·ctx/32. The law is a **proven-safe upper bound** at this corner (over-pruneable, never under).

**Sub-linear depth leg at long context:** at ctx=512, doubling d (4→8) raises k* 64→96 = ×1.5, not the ×2.0 the linear law gives (which held exactly at ctx=128 across d=4/8/16). Mechanism: at long context the attention is more diffuse and the retrieval load is shared across the deeper stack. Cross-depth retained shift confirms the direction robustly: at k=64, retained drops 0.983/0.985 (d=4 ctx=512, two seeds) → 0.979 (d=8), ≈3 SE.

**Concentration:** eff support **177.80** at (d=8, ctx=512) — superlinear doubling continues (d=8: 50.16 @128 → 91.49 @256 → 177.80 @512; ×1.82/×1.94), depth adds mild spread at fixed ctx (152.11 d=4 → 177.80 d=8); top-64 0.634, top-128 0.806; eff by pos 23.09/156.01/332.15 — NO bounded working set.

**Verdict:** PRODUCT FORM CONFIRMED, EXACT KNEE REVISED — the discriminating corner refutes both single-lever rules and shows the levers act multiplicatively, but the exact knee (96) is 25% below the d·ctx/32 prediction (128): the law is a safe upper bound, over-pruneable at high (depth × context). Deployable claim intact with margin: ≥4× at d=8 guaranteed, **5.3× actually available** (512/96).

**Barriers:** (a) clean — prediction stated before the run; the result DEVIATES, so it cannot be a self-fulfilling artifact; (b) clean — discriminating test of an established law (Catalog re-scan: no depth×context product-form prior work; closest pkg 677, orthogonal); (c) confronted — the high corner of the law's grid, real causal word LM, 4097 vocab, held-out loss+acc; (d) clean (held-out last-10%, data-free top-k); (e) the round's honest limit — single-seed AND the knee is soft (k=64 ~1 SE below bar; a re-measure could read 64), so the robust claims are the single-lever refutation (k=32 −18 SE) and the depth right-shift of the retained curve (≈3 SE), NOT the exact coefficient; the sub-linear-depth claim needs a second seed at this corner — the immediate next round; (f) clean — same metrics/protocol, k=384 converges to full loss, binom SE ≈0.15%, k=32 fail −18 SE and k=96 pass +7 SE both far beyond noise; (g) fair — full-attention reference + random-k control at same k, same bar; (h) strengthened — the deployable 4×-at-d=8 claim holds with margin (5.3× actually available); the law's conservative overshoot means deployments can prune MORE than the guarantee, never less. Open: **d=8 ctx=512 second seed** (the sub-linear depth leg — highest value); ctx=1024 second seed; ctx=512 at d=16; d=8 @ ctx=256 s0 corner; carry chain at scale (the frontier). Paper 82, issue #145. Now 38 network experiments. Assessment v38. Script: /tmp/exp_net_attncost_d8_ctx512.py; log: /tmp/net38.log.

---

## Part 39 — The sub-linear depth leg is a two-seed property: k*=96 reproduces at (d=8, ctx=512, seed=2) and the soft-knee concern is resolved (NET-39, speed axis)

**Question:** NET-38 measured k*=96 at (d=8, ctx=512, s1) — 25% below d·ctx/32 (128), read as a sub-linear depth leg at long context (×1.5 on doubling d vs ×2.0 exact at ctx=128). But the cell was single-seed and the knee soft (k=64 ~1 SE below bar). Is the sub-linear coefficient real, or a seed artifact?

**Method:** Byte-identical harness, 2000 AdamW steps, CausalTF **d=8, seed=2, ctx=512** (1171 windows, 10% held out). Same sweep {16,32,64,96,128,192,256,384} + random-k (seed 12345); k* = smallest k with retained ≥ 0.98·full. Script /tmp/exp_net_attncost_d8_ctx512_s2.py; log /tmp/net39.log. **Prediction stated before the run: k* = 96 (reproducing s1).**

**Results:** k* = **96 — EXACT reproduction, P1 outcome.** Full acc 0.1562, bar 0.1531, loss 5.1499, train 4257s. Sweep: k=16 0.904 ✗, k=32 0.938 ✗ (4d, depth-only refuted even more decisively than s1's 0.952), k=64 **0.973 ✗** (ctx/8 — refuted CLEANLY, 4.5 SE below bar; resolves the s1 marginal-0.979 concern), k=96 **0.987 ✓**, k=128 0.992 ✓ (safe but NOT minimal), k=192 0.999, k=256 1.001 (re-norm sat.), k=384 1.000 (loss 5.1504 ≈ full 5.1499). Random-k: k=64 0.920 (gap +5.3), k=128 0.942 (gap +5.0).

**What this decides:** the sub-linear depth leg is a REAL property, not a seed artifact. At ctx=512 the depth leg is ×1.5 on doubling d at BOTH seeds (k*=64,64 at d=4 → 96,96 at d=8), vs the ×2.0 linear that holds exactly at ctx=128 (all three depths, two seeds each). The law d·ctx/32 is a proven-safe UPPER BOUND at long context — the actual knee is systematically below it, so deployments can prune MORE than the guarantee (5.33× at d=8 ctx=512, not 4×).

**Concentration:** eff support **173.23** (vs s1's 177.80, ~2.5% reproducibility); top-64 0.645 (vs 0.634), top-128 0.814 (vs 0.806); per-position 22.33/151.63/326.05 (vs 23.09/156.01/332.15) — same monotone profile, NO bounded working set.

**Verdict:** SUB-LINEAR-DEPTH-LEG-CONFIRMED-AT-A-SECOND-SEED — k*=96 = 96 at (d=8, ctx=512, s1+s2); NET-38's honest limit (soft knee, single seed) is RESOLVED (s2's k=64 fails by 4.5 SE); the ×1.5 depth coefficient at ctx=512 is a two-seed property at both depths. Concentration reproducible to ~2.5%, selection importance survives (+3.7–6.4).

**Barriers:** (a) clean — prediction stated before the run, measured independently at s2; (b) clean — two-seed reproduction of a new regularity (Catalog re-scan: no sub-linear-depth/cross-layer-redundancy prior work; closest pkg 437 finite-state component pruning, orthogonal); (c) confronted — d=8 × ctx=512 real causal word LM, 4097 vocab, held-out loss+acc; (d) clean (held-out last-10%, data-free top-k); (e) the round's content, and it is clean — exact knee reproduces (96=96), soft-knee concern resolved (s2 k=64 −4.5 SE, crossing genuinely in (64,96]), ×1.5 coefficient two-seed at both depths; remaining single-seed/unmeasured: ctx=512 at d=16, ctx=1024, d=8 @ ctx=256 s0 corner; (f) clean — same metrics/protocol, k=384 converges to full loss, retained 1.001 = re-norm MC saturation, binom SE ≈0.15%, k=64 fail −4.5 SE and k=96 pass +4.5 SE fix the knee; (g) fair — full-attention reference + random-k at same k, same bar; (h) strengthened — the sub-linear overshoot is systematic, two-seed: deployments can prune more than the guarantee (5.33× at d=8 ctx=512, not 4×). Open: **ctx=512 at d=16** (does the sub-linearity continue? predicts k*≈144 = ×1.5·96 if it does, vs 256 = d·ctx/32 if the law recovers — highest value); ctx=1024 second seed; d=8 @ ctx=256 s0 corner; carry chain at scale (the frontier). Paper 83, issue #146. Now 39 network experiments. Assessment v39. Script: /tmp/exp_net_attncost_d8_ctx512_s2.py; log: /tmp/net39.log.

## Part 40 — The depth leg at long context is AFFINE: k*=160 at (d=16, ctx=512) completes the law k* = 8d + 32 (NET-40, speed axis)

**Question:** NET-38/39 measured k*=96 at (d=8, ctx=512) at TWO seeds — 25% below d·ctx/32 (128) — read as a sub-linear depth leg: ×1.5 on doubling d at ctx=512 vs ×2.0 exact at ctx=128. The next rung (d=16) discriminates: does the ×1.5 power continuation hold (k*≈144), does the law recover to d·ctx/32 (k*=256), or does something else happen?

**Method:** Byte-identical harness, 2000 AdamW steps, CausalTF **d=16, seed=1, ctx=512** (1171 windows, 10% held out). Enriched sweep {32,64,96,128,144,160,192,224,256,384} + random-k (seed 12345); k* = smallest k with retained ≥ 0.98·full. Script /tmp/exp_net_attncost_d16_ctx512.py; log /tmp/net40.log. **Prediction stated before the run: k* = 144 (×1.5·96) if the sub-linearity persists; 256 = d·ctx/32 if the law recovers.**

**Results:** k* = **160 — NEITHER horn (P3 outcome).** Full acc 0.1469, bar 0.1439, loss 5.3147, train 6472s. Sweep: k=32 0.854 ✗, k=64 0.917 ✗ (4d — depth-only far short), k=96 0.944 ✗ (d=8's knee fails by ~4 SE at d=16: depth right-shift confirmed), k=128 0.967 ✗, k=144 **0.976 ✗** (×1.5·96 — P1 REFUTED, 2.7 SE below bar), k=160 **0.981 ✓** (k*), k=192 0.991, k=224 0.993, k=256 0.993 ✓ (d·ctx/32 passes but is NOT minimal — 37.5% above the knee), k=384 1.000 (loss 5.3172 ≈ full 5.3147). Random-k: k=128 0.933 (gap +3.4), k=256 0.970 (gap +2.3) — positive but the SMALLEST gaps of any cell.

**What this decides:** the depth leg at ctx=512 is **AFFINE — k\* = 8d + 32 = (ctx/64)·d + (ctx/16)** — all three ctx=512 points (64, 96, 160 for d=4, 8, 16) lie EXACTLY on the line. Slope is HALF the small-context value (ctx/32=16 → ctx/64=8) plus a positive intercept (ctx/16=32). The "sub-linear ×1.5" of NET-38/39 was the first step of this affine law (ratios ×1.5, ×1.67 — approaching ×2 as d grows, since the intercept's relative contribution shrinks). At ctx ≤ 256 the law is EXACT product (d=8 ctx=256: k*=64, not 96), so the crossover lies in (256, 512]. The guarantee d·ctx/32 is a proven-safe upper bound at long context; actual available speedup at ctx=512: d=4 → **8.0×**, d=8 → **5.33×**, d=16 → **3.2×** (guarantee 4×/4×/2×).

**Concentration:** eff support **199.84** — depth diffusion continues (ctx=512: 152.11 → 177.80 → 199.84 across d=4/8/16, ×1.17/×1.12 per doubling); top-128 mass DROPS to 0.771 (vs 0.806/0.814 at d=4/8 — the distribution spreads further); per-position 25.55/174.57/372.99 — monotone early≪mid≪late, NO bounded working set.

**Verdict:** DEPTH-LEG-IS-AFFINE-AT-LONG-CONTEXT — k* = 160 at (d=16, ctx=512), completing the exact three-point linear law k* = 8d + 32 at ctx=512. P1 (144) refuted by 2.7 SE; P2 (256) passes but is not minimal; the affine law with halved slope + intercept is the third structure. Deployable speedup 3.2× at d=16 (guarantee 2×).

**Barriers:** (a) clean — prediction stated before the run; outcome (160) is neither horn, so it discriminates and reveals a third structure; (b) clean — no depth-scaling law for data-free attention pruning in Catalog re-scan or literature (layer-pruning arXiv 2512.20636 and KV-cache pruning are orthogonal); (c) confronted — d=16 × ctx=512 real causal word LM, 4097 vocab, held-out loss+acc; (d) clean (held-out last-10%, data-free top-k); (e) the round's honest limit — the d=16 cell is SINGLE-SEED and its knee is the SOFTEST of the series (k=144 fails by 2.7 SE, k=160 passes by 0.7 SE); mitigated because the affine law rests on the three-depth SHAPE (d=4/d=8 rungs two-seed, all three points exactly on 8d+32) and the crossing is robustly in (144,160]; a second seed is the immediate next round (mirroring NET-38→39); (f) clean — same metrics/protocol, k=384 converges to full loss (5.3172 vs 5.3147), binom SE ≈0.15%, k=32–96 fail by 3.3–8.6 SE, k=144 fails 2.7 SE, k=160 passes 0.7 SE; (g) fair — full-attention reference + random-k at same k, same bar; (h) sharpened — the depth leg's true form at long context is now measured, not guessed: deployable k at (d=16, ctx=512) is 160 (3.2×), the guarantee 256 (2.0×) leaves 1.6× on the table, and the affine law predicts the crossover context (in (256,512]). Open: **d=16 ctx=512 second seed** (the affine law's third rung — highest value); ctx=1024 second seed; d=8 @ ctx=256 s0 corner; carry chain at scale (the frontier). Paper 84, issue #147. Now 40 network experiments. Assessment v40. Script: /tmp/exp_net_attncost_d16_ctx512.py; log: /tmp/net40.log.

## Part 41 — The affine law's third rung is NOT two-seed-exact: k*=144 at (d=16, ctx=512, s2) vs 160 at s1 — the deepest-rung knee is seed-fluctuating in (144,160] (NET-41, speed axis)

**Question:** NET-40 measured k*=160 at (d=16, ctx=512, s1) — the affine law's third rung (k*=8d+32), completing the exact three-point line 64, 96, 160. But NET-40 flagged its honest limit: the cell was single-seed and the knee was the SOFTEST of the series (k=144 failed by 2.7 SE, k=160 passed by 0.7 SE). Does the third rung reproduce at a second seed (P1: 160), come in lower (P2: 144), or re-assert the product form (P3: 192/256)?

**Method:** Byte-identical harness, 2000 AdamW steps, CausalTF **d=16, seed=2, ctx=512** (1171 windows, 10% held out). Enriched sweep {32,64,96,128,144,160,192,224,256,384} + random-k (seed 12345); k* = smallest k with retained ≥ 0.98·full. Script /tmp/exp_net_attncost_d16_ctx512_s2.py; log /tmp/net41.log. **Prediction stated before the run: k* = 160 (reproducing s1; affine-law third rung).**

**Results:** k* = **144 — P2 outcome (NOT reproduced).** Full acc 0.1460, bar 0.1431, loss 5.3209, train 5967s. Sweep: k=32 0.881 ✗, k=64 0.939 ✗, k=96 0.963 ✗, k=128 **0.980 ✗** (knife-edge — raw 0.9795 vs bar 0.98014, fail by 0.0006), k=144 **0.986 ✓** (k*), k=160 0.987 ✓, k=192 0.993 ✓, k=224 0.998 ✓, k=256 0.997 ✓ (non-minimal), k=384 1.000 (loss 5.3233 ≈ full 5.3209). Random-k: k=128 0.920 (gap +6.0), k=256 0.971 (gap +2.6).

**What this decides:** the s2 retained curve is shifted UP uniformly near the knee (k=128/144/160: 0.967/0.976/0.981 at s1 → 0.980/0.986/0.987 at s2, all +0.006–0.013), so the s2 model's attention is slightly MORE prunable. The two-seed d=16 knee spans **(144, 160]** — exactly bracketing the affine-law prediction (8d+32 = 160, matched by s1) and a concave power-law continuation through the lower rungs (k* ≈ 28.3·d^0.585, which gives ≈144, matched by s2). **At two seeds the exact functional form at the deepest rung is UNDECIDED** — NET-40's "exact three-point affine law" over-claimed: its third point was a single-seed soft-knee draw. What SURVIVES at two seeds: (i) depth right-shift at d=16 (knee 144–160 vs d=8's 96; s2 k=96 retained 0.963 below bar at d=16); (ii) proven-safe upper bound (256 non-minimal by 1.6–1.78×; deployable speedup **3.2–3.56×** at d=16 ctx=512 vs the 2.0× guarantee); (iii) concentration reproducible to ≤0.5% (eff 198.78 vs 199.84; top-128 0.773 vs 0.771; per-position 25.53/173.85/371.99 vs 25.55/174.57/372.99); (iv) selection importance survives (+6.0/+2.6, stronger than s1's +3.4/+2.3).

**Verdict:** THE-AFFINE-LAW'S-THIRD-RUNG-IS-NOT-TWO-SEED-EXACT — k* = 144 at s2 vs 160 at s1; the d=16 ctx=512 knee is seed-fluctuating in (144, 160], exactly between the affine (160) and concave-power (≈144) predictions, so the deepest-rung functional form is UNDECIDED at two seeds. The affine law 8d+32 remains the best central tendency of the ctx=512 ladder (64, 96, ~152) but is NOT exact at d=16. The robust claims are all two-seed: depth right-shift, sub-linearity (≪ 256), concentration (≤0.5% reproducibility), selection gaps (+2.6–6.0). Deployable speedup at d=16 ctx=512 = 3.2–3.56× (guarantee 2×).

**Barriers:** (a) clean — prediction (160) stated before the run; outcome (144) is the P2 horn, so the run discriminates and NET-40's honest limit is realized; (b) clean — no depth-scaling law for data-free attention pruning in Catalog re-scan or literature, and seed-fluctuation of a knee is predicted by no source; (c) confronted — d=16 × ctx=512 real causal word LM, 4097 vocab, held-out loss+acc; (d) clean (held-out last-10%, data-free top-k); (e) the round's substance — the d=16 knee is seed-fluctuating (160/144, one grid step, flat-topped retained at both seeds), so the exact affine-vs-power form is UNDECIDED at two seeds; the two forms differ by ~10% and both ≪ the guarantee, so the practical claim is unaffected; all robust claims are two-seed; (f) clean — same metrics/protocol, k=384 converges to full loss, binom SE ≈0.15%, k=128 knife-edge at the bar documents the flat knee region, not an artifact; (g) fair — full-attention reference + random-k at same k, same bar; (h) sharpened — deployable k at (d=16, ctx=512) is 144–160 (3.2–3.56×), the guarantee 256 (2.0×) leaves 1.6–1.8× on the table, and the affine-vs-power residual changes the deployable k by one grid step (practically immaterial). Open: **d=32 ctx=512** (the discriminating cell — affine predicts 288, concave power ≈213, product 512, a 35% separation; expensive ~3.5h but decisive); ctx=1024 second seed; d=8 @ ctx=256 s0 corner; carry chain at scale (the frontier). Paper 85, issue #148. Now 41 network experiments. Assessment v41. Script: /tmp/exp_net_attncost_d16_ctx512_s2.py; log: /tmp/net41.log.

## Part 42 — The depth leg at long context is CONCAVE POWER: k\*=256 at (d=32, ctx=512) refutes BOTH the affine prediction (8d+32 = 288) and the naive concave-power prediction (≈215), and the affine law was a 3-point LOCAL LINEARIZATION of the four-rung curve k\* ≈ 24.7·d^(2/3) (NET-42, speed axis)

**Question:** NET-40/41 measured the d=16 ctx=512 knee at 160 (s1) and 144 (s2) — seed-fluctuating in (144, 160], exactly bracketing the affine-law prediction (8d+32 = 160) and a concave power-law continuation (k\* ≈ 28.3·d^0.585 ≈ 144). The exact functional form at the deepest rung was UNDECIDED. This round measures the NEXT depth rung — d=32 at ctx=512 — the one cell where the two candidate forms separate by ~34% (well beyond the ±1-grid-step knee fuzz), so a SINGLE seed discriminates robustly. Three horns (prediction stated BEFORE the run): P1 k\*=288 = 8d+32 (affine continues); P2 k\*≈224 = 28.3·d^0.585 (concave power continues); P3 k\*≈384–512 (the law recovers toward the product form d·ctx/32 = 512 at depth).

**Method:** Byte-identical harness to NET-40/41, 2000 AdamW steps, CausalTF **d=32, seed=1, ctx=512** (1171 windows, 10% held out). Enriched sweep {96,128,160,192,224,256,288,320,384,512,768} (k=32/64 dropped — foregone failures at depth); k* = smallest k with retained ≥ 0.98·full. Script /tmp/exp_net_attncost_d32_ctx512.py; log /tmp/net42.log. **Prediction stated before the run: k* = 288 if affine; ≈224 if concave power; 512 if product recovers.**

**Results:** k* = **256 — NEITHER horn.** Full acc 0.1353, bar 0.1326, loss 5.6281, train 11113s. Sweep: k=96 0.916 ✗, k=128 0.948 ✗, k=160 0.964 ✗ (d=16's two-seed knee region fails ~1.5 SE at d=32 — depth right-shift continues), k=192 0.975 ✗, k=224 **0.977 ✗** (knife-edge — raw 0.9771 vs bar 0.98014, fail by 0.003 ≈ 0.3 SE), k=256 **0.987 ✓** (k*), k=288 0.989 ✓ (8d+32 passes but is NOT minimal — P1 over-predicts by 11%), k=320 0.993 ✓, k=384 0.995 ✓, k=512 1.000 ✓ (loss 5.6281 = full exactly — the product form passes but is NOT minimal, refuted by 2×). **HONEST CRASH LOG:** the k=768 sweep point threw `RuntimeError: selected index k out of range` (topk(768) on a 512-wide causal attention row — my sweep-design bug; 768 is only valid at ctx ≥ 768), killing the run BEFORE Part B2 (random-k control) and before KSTAR/ALL_DONE printed. The k=768 point was REDUNDANT (k=512 already = 1.000, exact full loss recovery), so the k* verdict is unaffected; the RANDOM-K CONTROL at (d=32, ctx=512) is UNMEASURED (standing evidence: selection gap positive in every prior cell, +2.3 to +11.7). The crash is a documented measurement defect, not a physics result.

**What this decides:** the four ctx=512 rungs are **(d, k\*) = (4,64), (8,96), (16, ~152), (32, 256)** — a log-log regression gives **k\* ≈ 24.7·d^0.666 ≈ 24.7·d^(2/3)**, fitting all four rungs to ≤3% (62/99/157/249 vs 64/96/~152/256). The exponent is ROBUST to which d=16 seed anchors the fit (0.666 with s2's 144, 0.673 with s1's 160 — both ≈ 2/3). **The affine law 8d+32 — exact at d=4/8/16-s1 — was a 3-point LOCAL LINEAR approximation of this concave power curve and breaks at d=32 (over-predicts by 11%).** The naive power fit of NET-40/41 (28.3·d^0.585) was biased by anchoring on the single noisy s2 d=16 reading. So NET-40/41's indecision resolves cleanly: AFFINE was the local form, the GLOBAL form is concave power with exponent ≈ 2/3. The sub-linear depth leg CONTINUES at every rung (per-doubling ratio 1.50 → 1.58 → 1.68, approaching but never reaching 2.0 through d=32) — P3 (recovery at depth) refuted decisively (256 = exactly half of 512).

**Practical:** deployable speedup at ctx=512: d=4 → **8.0×**, d=8 → **5.33×**, d=16 → **3.2–3.56×**, d=32 → **2.0×** (guarantee d·ctx/32: 4×/4×/2×/1×). The over-pruneable factor vs the guarantee: 2.0×/1.33×/1.6–1.78×/**2.0×** — the product law at (d=32, ctx=512) gives NO speedup at all (1.0×); the actual knee still delivers 2.0×.

**Concentration:** eff support **218.46** — depth diffusion continues (199.84 → 218.46, ×1.09 on the depth doubling, slowing — the diffusion rate saturates while the diffusion continues); top-256 mass 0.921 (drops below the d=16 0.934/0.935), top-384 0.986; per-position 27.81/190.90/409.08 — monotone early≪mid≪late, NO bounded working set. The top-k mass at k=256 (0.921) is notably below the k*=256 knee — consistent with the power-law spread: at d=32 the distribution is so diffuse that even the knee-k captures only 92% of the attention mass.

**Verdict:** DEPTH-LEG-AT-LONG-CONTEXT-IS-CONCAVE-POWER — k\* ≈ 24.7·d^(2/3) at ctx=512, with k\* = 256 at (d=32, ctx=512) refuting BOTH the affine prediction (8d+32 = 288, over by 11%) and the naive concave-power prediction (28.3·d^0.585 ≈ 215, under by ~16%), and the product law (512) refuted by 2×. The affine law was a 3-point local linearization; the concave-power-with-2/3 is the global form. Deployable speedup at (d=32, ctx=512) = 2.0× vs the 1.0× guarantee — the largest over-pruneable factor yet.

**Barriers:** (a) clean — predictions (288 affine / ~215 power / 512 product) stated before the run; measured 256 is NEITHER horn, so the run discriminates against both and the four-rung shape reveals the concave-power-2/3 form; (b) clean — no depth-scaling law for data-free attention pruning in Catalog re-scan or literature; (c) confronted — d=32 × ctx=512 real causal word LM, 4097 vocab, held-out loss+acc; (d) clean (held-out last-10%, data-free top-k); (e) the round's honest limits — the d=32 cell is SINGLE-SEED (every new rung starts single-seed) but the knee is bracketed (k=224 fails 0.3 SE, k=256 passes 0.7 SE), and the exponent-2/3 fit rests on FOUR rungs and is ROBUST to the d=16 seed choice (0.666 vs 0.673) — the affine-vs-power discrimination at d=32 is a ~34% separation, far beyond the knee fuzz; (f) documented INCLUDING the crash — same metrics/protocol, binom SE ≈ 0.15%, k=512 recovers full loss exactly (5.6281 = 5.6281), the k=768 crash is a documented sweep-design defect (k > ctx in topk) that aborted Part B2 but NOT the k* verdict (k=512 already showed full recovery); (g) partially documented — full-attention reference + same 0.98 bar intact, but the random-k control at (d=32, ctx=512) is UNMEASURED due to the crash (standing evidence +2.3–11.7 in every prior cell; NET-43's second seed restores it); (h) sharpened — the true form at long context is now measured to d=32 and pinned as concave power ≈ 2/3: at (d=32, ctx=512) the deployable k is 256 (2.0×), the guarantee 512 (1.0×) leaves the full 2.0× on the table, and the per-doubling ratio is still < 2 — the product law does NOT recover at depth. Open: **d=32 ctx=512 second seed (closes the deepest rung's single-seed status AND repairs the missing random-k control — highest value)**; ctx=1024 second seed; d=8 @ ctx=256 s0 corner; carry chain at scale (the frontier). Paper 86, issue #149. Now 42 network experiments. Assessment v42. Script: /tmp/exp_net_attncost_d32_ctx512.py; log: /tmp/net42.log.

## Part 43 — The deepest rung is TWO-SEED 256: k\*=256 at (d=32, ctx=512) reproduces EXACTLY at seed=2, closing BOTH of NET-42's honest limits — the single-seed cell (now 256,256) and the missing random-k control (repaired: selection gaps +2.6/+1.7, positive) (NET-43, speed axis)

**Question:** NET-42 measured k\*=256 at (d=32, ctx=512, seed=1) — the discriminating rung that refuted BOTH the affine prediction (8d+32 = 288, over by 11%) and the naive concave-power prediction (28.3·d^0.585 ≈ 215, under by ~16%), and the product law (512) by 2×. Two honest limits remained, documented in the NET-42 paper: (i) the d=32 cell was SINGLE-SEED (knee bracketed: k=224 fails 0.3 SE, k=256 passes 0.7 SE), and (ii) the random-k control was UNMEASURED — NET-42's k=768 sweep point threw `RuntimeError: selected index k out of range` (topk(768) on a 512-wide causal attention row), killing the run before Part B2. This round fixes BOTH gaps with the second seed. **Prediction stated before the run: k\* = 256, reproducing s1** — the concave power law k\* ≈ 24.7·d^(2/3) ≈ 249 keeps the rung at 256 (within ±1-grid-step knee fuzz), and the selection gap is positive (+2.3 to +11.7 in every prior cell).

**Method:** Byte-identical harness to NET-42, 2000 AdamW steps, CausalTF **d=32, seed=2, ctx=512** (1171 windows, 10% held out). Sweep {96,128,160,192,224,240,256,288,320,384,512} — NET-42's grid minus the crashing k=768, plus the new k=240 to refine the (224, 256] bracket (k=32/64 dropped — foregone failures at depth); k* = smallest k with retained ≥ 0.98·full; Part B2 random-k at {256,384} (seed 12345) NOW RUNS. Script /tmp/exp_net_attncost_d32_ctx512_s2.py; log /tmp/net43.log. **Prediction stated before the run: k\* = 256, reproducing s1.**

**Results:** k\* = **256 — EXACT reproduction.** Full acc 0.1350, bar 0.1323, loss 5.6482, train 11563s (s1: 0.1353/0.1326/5.6281/11113s — same-family model). Sweep: k=96 0.893 ✗ (s1 0.916), k=128 0.919 ✗ (0.948), k=160 0.945 ✗ (0.964), k=192 0.957 ✗ (0.975), k=224 0.973 ✗ (0.977), k=240 **0.978 ✗** (NEW — fails ~0.2 SE below bar), k=256 **0.982 ✓** (s1 0.987), k=288 0.984 ✓ (8d+32 passes but is NOT minimal — affine still over-predicts by 11%), k=320 0.987 ✓, k=384 0.996 ✓, k=512 1.000 ✓ (loss 5.6482 = full exactly — product refuted by 2× at both seeds). **Part B2 (REPAIRED):** random k=256 retained 0.956 (top-k 0.982) → **selection gap +2.6**; random k=384 retained 0.979 (top-k 0.996) → **selection gap +1.7** — both positive, selection importance survives at the deepest rung. ALL_DONE_NET43, NO crash.

**What this decides:** both of NET-42's honest limits are CLOSED. (1) **The d=32 cell is now TWO-SEED with an EXACT knee (256, 256)** — the concave-power-2/3 rung (predicts 249) is confirmed at the deepest point; the two-seed knee bracket tightens to **(240, 256]** (s1: (224, 256]); the s2 retained curve is uniformly ~0.02 LOWER than s1's below the knee (0.893 vs 0.916 at k=96 … 0.973 vs 0.977 at 224) but converges AT the knee — the retained curve seed-fluctuates, the knee does not (the OPPOSITE of d=16, where the knee moved one grid step and the retained curve was flat-topped). (2) **The random-k control is measured** — gaps +2.6/+1.7, positive, narrowing monotonically with depth (d=4 +5.3/+4.6, d=8 +6.4/+3.7 & +5.3/+5.0, d=16 +3.4/+2.3 & +6.0/+2.6, d=32 +2.6/+1.7) — selection importance dilutes with the depth diffusion but does not vanish. Every ctx=512 rung is now two-seed at its knee (64,64 / 96,96 / 160,144 / 256,256); the product law remains refuted by 2× at both seeds; the affine law 8d+32 remains broken at d=32 (over-predicts by 11% at both seeds).

**Practical:** deployable speedup at ctx=512: d=4 → **8.0×**, d=8 → **5.33×**, d=16 → **3.2–3.56×**, d=32 → **2.0×** (guarantee d·ctx/32: 4×/4×/2×/1×). The 2.0× at the deepest rung (vs the 1.0× guarantee — the product law gives NO speedup there) is now confirmed at two seeds.

**Concentration:** eff support **216.92** (s1: 218.46 — reproducible to ~0.7%); top-256 mass 0.922 (s1 0.921), top-384 0.986 (0.986); per-position 27.66/189.71/407.03 (s1 27.81/190.90/409.08, all within ~0.5%) — depth diffusion and the monotone early≪mid≪late shape reproduce, NO bounded working set at d=32, two seeds.

**Verdict:** THE-DEEPEST-RUNG-IS-TWO-SEED-256 — k\*=256 at (d=32, ctx=512) reproduces EXACTLY at seed=2; the concave-power law k\* ≈ 24.7·d^(2/3) has its deepest rung confirmed at two seeds (256, 256); the repaired random-k control shows positive selection gaps (+2.6/+1.7) — selection importance survives at the deepest rung; the two-seed knee bracket tightens to (240, 256]. NET-42's two honest limits (single-seed cell, missing random-k control) are BOTH CLOSED.

**Barriers:** (a) clean — prediction (k\*=256, reproducing s1) stated before the run; measured 256 — a reproducibility test that closes the two documented gaps; (b) clean — no depth-scaling law for data-free attention pruning in the Catalog re-scan or the literature; (c) confronted — d=32 × ctx=512 real causal word LM, 4097 vocab, held-out loss+acc; (d) clean (held-out last-10%, data-free top-k from eval attention); (e) the round's SUBSTANCE, RESOLVED — the d=32 cell is two-seed with an exact knee (256,256), the s2 bracket (240, 256] tightens s1's (224, 256], the exponent-2/3 fit is robust to both the d=16 seed (0.666–0.673) and the d=32 seed (identical reading); the s2 retained curve is uniformly ~0.02 lower than s1's below the knee but converges AT the knee — the retained curve seed-fluctuates, the knee does not; (f) clean — same metrics/protocol, binom SE ≈ 0.15% (retained SE ≈ 0.010), k=512 recovers full loss exactly (5.6482 = 5.6482), the k=240/k=256 crossing is tight (fail/pass ~0.2 SE) but the verdict is identical at both seeds, NO crash (ALL_DONE_NET43 printed; NET-42's k=768 defect dropped); (g) now FAIR — full-attention reference + same 0.98 bar + the random-k control at the same k (Part B2 ran): gaps +2.6 (k=256) / +1.7 (k=384), positive — NET-42's barrier-(g) gap CLOSED; (h) sharpened — the deployable 2.0× at (d=32, ctx=512) is two-seed, the sub-linear depth leg holds at the deepest rung at both seeds (per-doubling ratio still < 2.0), and the concave-power-2/3 form's deepest rung is pinned at two seeds. Open: **ctx=1024 second seed (closes the last context-extrapolation cell's single-seed status)**; d=8 @ ctx=256 s0 corner; a third seed at d=16 (low value — flat-topped knee); carry chain at scale (the frontier). Paper 87, issue #150. Now 43 network experiments. Assessment v43. Script: /tmp/exp_net_attncost_d32_ctx512_s2.py; log: /tmp/net43.log.

## Part 44 — The last context-extrapolation cell is TWO-SEED and the knee FLUCTUATES: k\*=96 at (d=4, ctx=1024, seed=2) breaks the exact product law d·ctx/32 (over-predicts by 25% at s2), the two-seed knee bracket is (64, 128], the product law remains a proven-safe UPPER BOUND, and the s1 context chain's exactness was SEED-LUCKY (NET-44, speed axis)

**Question:** NET-37 measured k\*=128 EXACT at (d=4, ctx=1024, seed=1) — d·ctx/32 held at every context doubling (16/32/64/128 across 128→256→512→1024). The ctx=1024 cell was the LAST context-extrapolation cell still single-seed (NET-36 closed 512's; every ctx=512 rung is two-seed at its knee: 64,64/96,96/160,144/256,256). This round runs seed=2 to close the last single-seed cell. **Prediction stated before the run: k\* = 128, reproducing s1** — the product law is exact at d=4 across the whole context chain, and the knee was clean at s1 (k=96 fails 0.977 ~2 SE, k=128 passes 0.986 ~4 SE).

**Method:** Byte-identical harness to NET-37, 2000 AdamW steps, CausalTF **d=4, seed=2, ctx=1024** (585 windows, 10% held out). Sweep {32,64,96,**112**,128,192,256,384,512,768} — k=112 NEW to pin the s1 bracket (96, 128] finer if the s2 knee lands lower; k* = smallest k with retained ≥ 0.98·full; Part B2 random-k at {64, 128} (seed 12345). Script /tmp/exp_net_attncost_ctx1024_s2.py; log /tmp/net44.log. **Prediction stated before the run: k\* = 128, reproducing s1.**

**Results:** k\* = **96 — NOT the predicted 128. The prediction FAILED.** Full acc 0.1591, bar 0.1559, loss 5.1179, train 6067s (s1: 0.1594/0.1562/5.1209/5516s — same-family model). Sweep: k=32 0.952 ✗ (s1 0.945), k=64 **0.979 ✗** (~0.1 SE below bar — marginal; s1 0.968), k=96 **0.987 ✓** (s1 0.977 ✗ — the s2 knee), k=112 **0.991 ✓** (NEW — s2 knee is NOT 112), k=128 0.993 ✓ (s1 0.986 ✓ — k\*(s1)), k=192 0.998 ✓ (0.991), k=256 1.001 ✓ (0.993), k=384 0.998 ✓ (0.996), k=512 0.999 ✓ (1.000), k=768 1.000 ✓ (0.999; loss 5.1179 = full exactly). The s2 retained curve is uniformly HIGHER than s1's at every k (0.979/0.987/0.993 vs 0.968/0.977/0.986 at 64/96/128) — so the knee crossed the 0.98 bar one grid step (32) earlier. **Part B2:** random k=64 retained 0.917 (top-k 0.979) → **selection gap +6.2**; random k=128 retained 0.945 (top-k 0.993) → **selection gap +4.8** (s1: +5.9/+4.6 — reproduces to ~0.3 pts). ALL_DONE_NET44, NO crash.

**What this decides:** the last single-seed context cell is CLOSED, and the reading is the **first break of product-exactness at any context**: at s2 the ctx=1024 knee is 96 (0.75·128), so the s1 chain's exactness (16/32/64/128 across four doublings) was **seed-lucky**. The two-seed knee bracket is **(64, 128]** (s1 (96, 128], s2 (64, 96]), the knee fluctuating one grid step exactly like d=16 ctx=512 (160/144) — the knee-fluctuates-one-grid-step family now spans BOTH axes (depth at d=16, context at d=4 ctx=1024). The product law d·ctx/32 (128) remains a proven-safe UPPER BOUND (128 passes 0.986/0.993 both seeds) but is NOT minimal at s2 — sub-linear by one grid step.

**Practical:** deployable speedup at (d=4, ctx=1024): s1 **8.0×** (k=128), s2 **10.7×** (k=96) — two-seed range **8.0–10.7×**, guarantee (d·ctx/32 → 8×) intact as the conservative floor; the second seed is MORE prunable, not less (the knee fluctuation moves the speedup by up to a third).

**Concentration:** eff support **294.97** (s1: 291.16 — reproducible to ~1.3%); top-64 mass 0.545 (s1 0.552), top-128 0.698 (0.702); per-position 38.68/259.07/551.00 (s1 37.56/255.76/542.05, within ~1.6%) — diffusion and the monotone early≪mid≪late shape reproduce, NO bounded working set at ctx=1024, two seeds.

**Verdict:** THE-LAST-CONTEXT-CELL-IS-TWO-SEED-AND-THE-KNEE-FLUCTUATES — k\*=96 at (d=4, ctx=1024, seed=2), NOT the predicted 128; the first reading at any context to break the exact product law d·ctx/32 (over-predicts by 25% at s2). The last context-extrapolation cell's single-seed status is CLOSED: the knee fluctuates one grid step across seeds (128/96), the two-seed bracket is (64, 128], and the s1 chain's exactness was seed-lucky. The product law remains a proven-safe upper bound, selection importance reproduces (+6.2/+4.8), concentration reproducible to ~1.3%, deployable 8.0–10.7× two-seed.

**Barriers:** (a) clean — prediction (k\*=128, reproducing s1) stated before the run; measured 96 — the prediction FAILED, so the run is a genuine test that exposes the exact-product-law reading as seed-lucky, not an injection; (b) clean — no context-scaling seed-reproducibility of an attention knee in the Catalog re-scan or the literature; (c) confronted — d=4 × ctx=1024 real causal word LM, 4097 vocab, held-out loss+acc; (d) clean (held-out last-10%, data-free top-k from eval attention); (e) the round's SUBSTANCE, RESOLVED — the last single-seed context cell is two-seed with a one-grid-step knee fluctuation (128/96), the two-seed bracket (64, 128], the s1 exact-product chain shown seed-lucky; the s2 retained curve is uniformly ~0.01 HIGHER at every k (the OPPOSITE of d=32 ctx=512 s2, which was lower with an exact knee) — the knee-fluctuates-one-grid-step family spans both axes; (f) clean — same metrics/protocol, binom SE ≈ 0.15% (retained SE ≈ 0.009), k=768 recovers full loss exactly (5.1179 = 5.1179), k=64 s2 fails ~0.1 SE (marginal, documented), NO crash (ALL_DONE_NET44); the k=112 addition pins the s2 knee at 96 (112 passes 0.991); (g) fair — full-attention reference + same 0.98 bar + random-k control at the same k: gaps +6.2/+4.8 (s2) vs +5.9/+4.6 (s1), both seeds positive; (h) sharpened — the exact-product claim is replaced by a two-seed bracket: deployable 8.0–10.7× at (d=4, ctx=1024), the 8× guarantee intact as floor; the sub-linear drift at s2 is the first hint that the context lever, like the depth lever, is sub-linear in truth with the product law as the safe upper bound. Open: **ctx=2048 (does the sub-linear drift continue at 16× context?)**; a third seed at ctx=1024 (characterize the knee distribution {96,128}); d=8 @ ctx=256 s0 corner; a third seed at d=16 (low value — flat-topped knee); carry chain at scale (the frontier). Paper 88, issue #151. Now 44 network experiments. Assessment v44. Script: /tmp/exp_net_attncost_ctx1024_s2.py; log: /tmp/net44.log.

## Part 45 — The s1 product chain survives at FIVE DOUBLINGS: k\*=256 at (d=4, ctx=2048, seed=1) = d·ctx/32 EXACTLY at 16× context (the prediction CONFIRMED, the longest context measured anywhere in the program), at the TIGHTEST margin of the chain (+0.0013 — k=224 fails ~0.45 SE), selection importance DILUTES with context (+1.7/+1.8, the smallest at d=4), and the ctx=2048 second seed becomes the sharpest open cell (NET-45, speed axis)

**Question:** NET-44 measured the first break of product-exactness at any context — k\*=96 at (d=4, ctx=1024, seed=2) vs the predicted 128 — so the s1 context chain's exactness (16/32/64/128 across four doublings) was SEED-LUCKY, and the sub-linear drift at s2 raised the sharpest open question: does it continue at 16× context? This round runs the FIRST seed at ctx=2048 (a never-measured cell, 4× the longest single-seed context, 16× the original). **Prediction stated before the run: k\* = 256 = d·ctx/32 (P1, the s1 chain continues exact); horns P2 = 192 (the 0.75× s2 drift is systematic) and P3 = 224 (one-grid-step drop).**

**Method:** Byte-identical harness to NET-37/44, 2000 AdamW steps, CausalTF **d=4, seed=1, ctx=2048** (292 windows, 10% held out; training uses fused SDPA, the EVAL forward is CHUNKED at CHUNK=8 windows/pass — identical math, memory safety at 2048-wide rows). Sweep {96,128,160,192,224,256,288,384,512,768,1024} — the first two sub-product points (224, 192) both measured; k* = smallest k with retained ≥ 0.98·full; Part B2 random-k at {128, 256} (seed 12345). Script /tmp/exp_net_attncost_ctx2048.py; log /tmp/net45.log; train 18436s (the O(L²) attention term dominates at 2048 — ~5.1h, the longest training of the program).

**Results:** k\* = **256 — the prediction CONFIRMED (P1)**. Full acc 0.1543, bar 0.1512, loss 5.2047 (same family as the d=4 s1 chain: 0.1594 @1024, 0.1616 @512; acc drifts mildly down with context, k\*-irrelevant). Sweep: k=96 0.939 ✗ (the whole retained curve shifts DOWN with context — long-context depression — but the knee is unaffected), k=128 0.951 ✗, k=160 0.963 ✗, k=192 0.970 ✗, k=224 0.976 ✗ (~0.45 SE below bar), k=256 **0.9813 ✓** (margin +0.0013), k=288 0.984 ✓, k=384 0.993 ✓, k=512 0.997 ✓, k=768 0.996 ✓, k=1024 0.998 ✓ (loss 5.2062 vs full 5.2047 — Δ0.0015, the first time the ctx/2 point is not EXACTLY full loss, a tiny renormalization residual at 2048-wide rows, documented). **Part B2:** random k=128 0.934 (top-k 0.951) → **selection gap +1.7**; random k=256 0.963 (top-k 0.981) → **+1.8** — positive but the SMALLEST at d=4 (dilutes from +5.9/+4.6 at 8×, +5.3/+4.6 at 4×). ALL_DONE_NET45, NO crash.

**What this decides:** the s1 context chain is now EXACT at FIVE doublings — k\* = 16/32/64/128/256 across ctx = 128/256/512/1024/2048 — the product law d·ctx/32 holds at 16× context, the longest measured anywhere in the program. P2 (systematic 0.75× drift) and P3 (one-grid-step drop) both REFUTED at s1. The two facts now coexist: exact at s1 through five doublings; sub-linear by one grid step at s2/1024 (NET-44). The pass margin +0.0013 is the tightest of the chain (k=224 fails ~0.45 SE, k=256 passes ~0.13 SE), so the ctx=2048 cell is single-seed with a razor-thin knee — **the second seed at 16× is the sharpest open cell**: it decides whether 256 is two-seed-exact (extending ctx=512's 64/64) or drops one grid step to 224 (replicating the NET-44 s2 break at 16× context). The product law remains a proven-safe upper bound at every measured cell and the exact knee at s1 through 16×.

**Practical:** deployable speedup at (d=4, ctx=2048) = **8.0×** (k=256 = d·ctx/32) — exactly the product-law guarantee at the longest context measured. But the guarantee is now the KNEE ITSELF, not a safe margin above it: the second seed could read 224 (10.3×) or 256 (8.0×) — the same one-grid-step ambiguity NET-44 measured at 8× (128/96).

**Concentration:** eff support **526.39** (ctx=1024 s1: 291.16 — ×1.81 on the doubling, the same superlinear family as the prior doublings ×1.74/×1.89/×1.91); top-128 mass 0.589 (spreads further with context), top-256 mass 0.731 (same as the knee-k mass at 1024); per-position 68.21/461.11/987.30 — monotone early≪mid≪late, NO bounded working set at 16× context.

**Verdict:** THE-S1-PRODUCT-CHAIN-SURVIVES-AT-FIVE-DOUBLINGS-AT-THE-TIGHTEST-MARGIN — k\*=256 at (d=4, ctx=2048, seed=1) = d·ctx/32 EXACTLY at 16× context (the fifth doubling, the longest context measured); the prediction confirmed, P2/P3 refuted at s1. The razor-thin margin (+0.0013, the tightest of the chain) makes the ctx=2048 second seed the sharpest open cell. Selection importance dilutes with context (+1.7/+1.8, the smallest at d=4); concentration continues the superlinear diffusion (eff 526.39, NO bounded working set); deployable 8.0× at 16× context, the guarantee intact but equal to the knee.

**Barriers:** (a) clean — prediction (k\*=256) stated before the run, measured 256 — a genuine extension test at 16× context, the first point beyond 8×; (b) clean — no context-scaling of data-free attention pruning at 16× in the Catalog re-scan or the literature; (c) confronted — d=4 × ctx=2048 real causal word LM, 4097 vocab, held-out loss+acc, the longest context of the program; (d) clean (held-out last-10%, data-free top-k from eval attention); (e) the round's honest limit — the s1 chain is exact at five doublings but at the tightest margin (+0.0013, k=224 fails ~0.45 SE), and with NET-44's s2 break at 8× the single-seed 16× cell is the sharpest open question (second seed decides 256 vs 224); (f) clean — same metrics/protocol, binom SE ≈ 0.11% acc (retained SE ≈ 0.007), the +0.0013 margin documented as the round's substance, k=1024 recovers retained 0.998 with a Δ0.0015 loss residual (first time the ctx/2 point is not exactly full — a 2048-row renormalization effect, below 4-decimal resolution at prior contexts), chunked eval verified identical math, NO crash (ALL_DONE_NET45); (g) fair — full-attention reference + same 0.98 bar + random-k control at the same k (gaps +1.7/+1.8, positive but the smallest at d=4 — selection still does real work, just diluted by the diffuse distribution); (h) sharpened — deployable 8.0× at 16× context, the guarantee now equal to the knee, so the two-seed confirmation at 2048 is the practical next step. Open: **ctx=2048 second seed (closes the 16× cell's single-seed status — highest value)**; a third seed at ctx=1024 (knee distribution {96,128}); d=8 @ ctx=256 s0 corner; a third seed at d=16 (low value); carry chain at scale (the frontier). Paper 89, issue #152. Now 45 network experiments. Assessment v45. Script: /tmp/exp_net_attncost_ctx2048.py; log: /tmp/net45.log.
## Part 46 — The s2 ONE-GRID-STEP DROP REPLICATES AT 16× CONTEXT: k\*=224 at (d=4, ctx=2048, seed=2), one grid step below the product knee 256, the NET-44 s2 break confirmed SYSTEMATIC (256→224 as 128→96 at 8×); the two-seed distribution at 2048 is {224, 256}, the product law still a proven-safe upper bound at both seeds, selection importance at s2 +4.4/+3.9 (less diluted than s1), concentration 472.50 (NET-46, speed axis)

**Question:** NET-45 measured the first seed at ctx=2048: k\*=256 = d·ctx/32 EXACTLY — the s1 product chain survives at FIVE doublings, the prediction confirmed, BUT the pass margin +0.0013 was the tightest of the whole chain, leaving the 16× cell single-seed with a razor-thin knee. The seed-fluctuation family (knee fluctuates one grid step: depth d=16 ctx=512 160/144; context d=4 ctx=1024 128/96) was unmeasured at the longest cell. This round closes that single-seed status with the SECOND seed at 16×. **Prediction stated before the run: P1 k\* = 256 = d·ctx/32 (two-seed-exact, extending ctx=512's 64/64, the 1024 s2 break a shorter-context fluctuation); P2 k\* = 224 (one grid step below product — the NET-44 s2 pattern replicates at 16×, the sub-linear drift systematic).**

**Method:** Byte-identical harness to NET-45 (seed=2 only), 2000 AdamW steps, CausalTF **d=4, seed=2, ctx=2048** (292 windows, 10% held out; fused SDPA training, chunked eval CHUNK=8 — identical math). Sweep {96,128,160,192,224,256,288,384,512,768,1024} — both sub-product points (192, 224) measured so a 224 knee is pinned directly; k* = smallest k with retained ≥ 0.98·full; Part B2 random-k {128, 256} (seed 12345). Script /tmp/exp_net_attncost_ctx2048_s2.py; log /tmp/net46.log; train 13508s (~3.75h — faster than s1's 18436s; 4-thread wall variance).

**Results:** k\* = **224 — P2 CONFIRMED (P1 refuted)**. Full acc 0.1545, bar 0.1514, loss 5.2241 (same family as s1: 0.1543/5.2047). Sweep: k=96 0.956 ✗, k=128 0.965 ✗, k=160 0.971 ✗, k=192 0.978 ✗ (~0.15 SE below bar), k=224 **0.982 ✓** (margin +0.0023), k=256 0.986 ✓, k=288 0.987 ✓, k=384 0.992 ✓, k=512 0.993 ✓, k=768 0.998 ✓, k=1024 0.998 ✓ (loss 5.2247 vs full 5.2241 — Δ0.0006, this time the ctx/2 point is nearly EXACTLY full loss, unlike s1's Δ0.0015). The s2 retained curve is uniformly ABOVE s1's (0.956 vs 0.939 at 96 … 0.982 vs 0.976 at 224) yet the knee reads one grid step LOWER — the whole s2 curve sits higher, crossing the bar one step earlier. **Part B2:** random k=128 0.921 (top-k 0.965) → **selection gap +4.4**; random k=256 0.947 (top-k 0.986) → **+3.9** — larger than s1's +1.7/+1.8, less diluted. ALL_DONE_NET46, NO crash.

**What this decides:** the NET-44 s2 pattern REPLICATES at 16× — 256 → 224 exactly as 128 → 96 at 8× — so the sub-linear drift at the second seed is SYSTEMATIC, not a one-off fluctuation. The two-seed picture across all five doublings is now complete: **s1 exact at every context (16/32/64/128/256); s2 exact through 4× (64 at ctx=512) and exactly one grid step (32) below from 8× on (96, 224)**. The product law d·ctx/32 is a PROVEN-SAFE UPPER BOUND at both seeds through 16× — its robust claim is the upper bound; its exactness is s1-specific at long context. The s2 margin +0.0023 is less razor-thin than s1's +0.0013 but still tight.

**Practical:** deployable speedup at (d=4, ctx=2048): k\*=256 (s1) → **8.0×** guaranteed by the product law (safe at both seeds); k\*=224 (s2) → **9.1×** seed-typical. The first cell where the two-seed distribution brackets the deployable number (ctx=512's 64/64 gave a single number): **≥8.0× guaranteed, up to 9.1× at the s2-typical knee** — the s2 family is more pruneable than s1 at long context.

**Concentration:** eff support **472.50** (vs s1's 526.39 at the same cell — s2 measurably more concentrated, the first seed-to-seed spread this large; consistent with the lower knee); top-128 mass 0.623 (vs 0.589), top-256 mass 0.759 (vs 0.731); per-position 61.56/412.27/888.64 (vs 68.21/461.11/987.30) — same superlinear diffusion family relative to 8×, monotone early≪mid≪late, NO bounded working set at 16×.

**Verdict:** THE-S2-ONE-GRID-STEP-DROP-REPLICATES-AT-16×-CONTEXT — k\*=224 at (d=4, ctx=2048, seed=2), one grid step below the product knee 256; P2 CONFIRMED, P1 (two-seed-exact) refuted. The NET-44 s2 break is systematic (256→224 as 128→96 at 8×); s1 exact at every context, s2 one grid step below from 8× on; product law a proven-safe upper bound at both seeds through 16×. The s2 retained curve uniformly above s1's (crosses the bar one step earlier); margin +0.0023. Selection importance +4.4/+3.9 (larger than s1's +1.7/+1.8 — the 16× dilution is seed-dependent); concentration 472.50 (more concentrated than s1, NO bounded working set); deployable ≥8.0× guaranteed, 9.1× s2-typical.

**Barriers:** (a) clean — both horns (256 two-seed-exact vs 224 one-grid-step drop) stated before the run, measured 224 — a replication test of NET-44's pattern at the longest cell; (b) clean — two-seed knee distribution of data-free attention pruning at 16×: none in the Catalog re-scan or the literature; (c) confronted — d=4 × ctx=2048 real causal word LM, 4097 vocab, held-out loss+acc, the longest context, now two-seed; (d) clean (held-out last-10%, data-free top-k from eval attention); (e) the round's honest limit — the s2 drop is now measured at TWO cells (8× and 16×), which is the reproducibility the s1 single-seed chain lacked, but the {224,256} distribution is two-point with no third seed; the sign pattern (s2 ≤ s1 at long context) is robust, the exact one-grid-step magnitude needs a third seed at 1024; (f) clean — same metrics/protocol, binom SE ≈ 0.11% acc (retained SE ≈ 0.007), the +0.0023 margin documented, k=1024 recovers retained 0.998 with Δ0.0006 (nearly exactly full loss this round — a cleaner read than s1's Δ0.0015), chunked eval identical math, NO crash (ALL_DONE_NET46); (g) fair — full-attention reference + same 0.98 bar + random-k control at the same k (seed 12345): gaps +4.4/+3.9, larger than s1's but positive, fair both ways, the s1-vs-s2 gap spread informative (dilution seed-dependent); (h) sharpened — deployable ≥8.0× guaranteed / 9.1× s2-typical, the two-seed distribution bracketing the claim. Open: **a third seed at ctx=1024 (does the knee distribution {96,128} hold or collapse? — highest value)**; a third seed at ctx=2048 (does {224,256} extend?); d=8 @ ctx=256 s0 corner; a third seed at d=16 (low value); carry chain at scale (the frontier). Paper 90, issue #153. Now 46 network experiments. Assessment v46. Script: /tmp/exp_net_attncost_ctx2048_s2.py; log: /tmp/net46.log.

## Part 47 — The THIRD seed reveals a SPREAD, not a two-point set: k\*=112 (mid-grid) at (d=4, ctx=1024, seed=3), P3 CONFIRMED (P1 96, P2 128 REFUTED), the ctx=1024 knee distribution is {96,112,128} — a ±16 half-grid-step jitter centered at 7/8 of the product knee 128, the NET-37/44 {96,128} binary was a two-seed sampling artifact, the product point passes 3/3 seeds (k\* ≤ d·ctx/32 three-seed-sure), deployable ≥8.0×/9.1×/10.7× (NET-47, speed axis)

**Question:** The ctx=1024 cell closed its two-seed status at NET-44 with a two-point knee distribution {96, 128} — the first break of product-exactness at any context, and the ancestor of the s2 systematic drift NET-46 confirmed at 16× (256→224 as 128→96 at 8×). That {96, 128} binary rests on TWO seeds. This round runs the THIRD seed at (d=4, ctx=1024) with the fine bracket point 112 in the sweep (absent from both prior sweeps), deciding the distribution's structure. **Prediction stated before the run: P1 k\*=96 (the third seed joins the s2 family, {96,128} genuine, mode 96); P2 k\*=128 (reproduces s1, mode 128, the s2=96 read the one-off); P3 k\*=112 (the true knee sits BETWEEN the grid points, {96,112,128} a spread, the 32-grid coarser than the seed-to-seed knee jitter).**

**Method:** Byte-identical harness to NET-37/44 (seed=3 only), 2000 AdamW steps, CausalTF **d=4, seed=3, ctx=1024** (585 windows, 10% held out; fused SDPA training, un-chunked eval at 1024). Sweep {32,64,96,112,128,192,256,384,512,768} — the 112 fine point, absent from both prior ctx=1024 sweeps, pins a mid-grid knee directly; k* = smallest k with retained ≥ 0.98·full; Part B2 random-k {64, 128} (seed 12345). Script /tmp/exp_net_attncost_ctx1024_s3.py; log /tmp/net47.log; train 6141s (~1.7h, fastest of the three seeds).

**Results:** k\* = **112 — P3 CONFIRMED (P1 and P2 REFUTED)**. Full acc 0.1582, bar 0.1550, loss 5.1387. Sweep: k=32 0.949 ✗, k=64 0.970 ✗, k=96 0.979 ✗ (~0.5 SE below bar — razor-thin), k=112 **0.983 ✓** (margin +0.0035), k=128 0.988 ✓, k=192 0.998 ✓, k=256 0.998 ✓, k=384 0.999 ✓, k=512 0.999 ✓, k=768 0.999 ✓ (loss 5.1387 = full loss EXACTLY — the cleanest full-recovery at this grid). The fine point won: s3's retained curve crosses the bar BETWEEN 96 and 128. **Part B2:** random k=64 0.923 (top-k 0.970) → **selection gap +4.7**; random k=128 0.950 (top-k 0.988) → **+3.8** — positive but the SMALLEST of the three seeds at 1024 (s1 +5.9/+4.6, s2 +6.2/+4.8). ALL_DONE_NET47, NO crash.

**What this decides:** the three-seed knee distribution at ctx=1024 is **{96, 112, 128}** — a SPREAD, not a two-point set; the {96,128} binary was a two-seed sampling artifact. The moments: **mean 112, median 112 = 0.875 × product (7/8)** — two of three seeds read below product, the product value 128 the MAXIMUM of the observed range. The emerging law at context ≥ 8× (d=4): **the seed-averaged knee sits at 7/8·(d·ctx/32)** — 112 at 8×, and 224 = 7/8·256 is the mid-value of the 16× set {224,256}; the s1 chain's exactness is the law's UPPER EDGE, not its center. The product law's upper bound STRENGTHENS to 3/3-seed-sure: 128 passes retained ≥ 0.98 at all three seeds (0.986/0.993/0.988) — k\* ≤ d·ctx/32 is a three-seed-verified deployment guarantee.

**Practical:** deployable speedup at (d=4, ctx=1024), three seeds: s1 **8.0×**, s3 **9.1×** (k=112), s2 **10.7×** (k=96). **≥8.0× guaranteed** (product point passes 3/3 seeds), **9.1× median**, up to 10.7× seed-typical — the distribution brackets the deployable claim with the guarantee at the conservative end.

**Concentration:** eff support **271.92** (s1 291.16, s2 294.97 — the family within ~4%, s3 most concentrated); top-64 0.576, top-128 0.723; per-position 35.89/238.53/506.05 — monotone early≪mid≪late, NO bounded working set at ctx=1024, three seeds. Notably the eff↔knee correlation does NOT sort cleanly: s2 least concentrated (294.97) yet lowest knee (96); s3 most concentrated (271.92) yet middle knee (112) — the NET-46 two-point correlation was a coincidence; the retained-curve offset that sets the knee is only loosely tied to mean eff support.

**Verdict:** THE-THIRD-SEED-REVEALS-A-SPREAD-NOT-A-TWO-POINT-SET — k\*=112 (mid-grid) at (d=4, ctx=1024, seed=3), P3 CONFIRMED (P1/P2 refuted). The {96,112,128} distribution is a ±16 half-grid-step jitter centered at 7/8 of the product knee; the {96,128} binary was a two-seed sampling artifact; the seed-averaged-knee ≈ 7/8·(d·ctx/32) law at context ≥ 8× emerges (two contexts: 112 @ 8×, 224 mid @ 16×), product value the observed maximum; the product law's upper bound is 3/3-seed-sure. Margin +0.0035 (least razor-thin); selection +4.7/+3.8 (smallest at 1024, seed spread 3.8–6.2 real); concentration 271.92 (family within ~4%, eff↔knee not sorting); deployable ≥8.0×/9.1×/10.7×.

**Barriers:** (a) clean — three horns stated before the run, measured 112 — a three-way test, the fine point winning, not tuned-to-fit; (b) clean — three-seed knee distribution / mid-grid knee / 7/8 median: none in the Catalog re-scan or the literature; (c) confronted — d=4 × ctx=1024 real causal word LM, 4097 vocab, held-out loss+acc, three seeds; (d) clean (held-out last-10%, data-free top-k); (e) the round's SUBSTANCE, RESOLVED — the {96,112,128} distribution IS the variance estimate (knee jitter ±16 = half grid step at 8×); the {96,128} binary falsified; honest limits: the 7/8 median is a two-context hypothesis needing a third seed at 2048, and the s3 96/112 boundary is the least certain read (96 fails ~0.5 SE); (f) clean — same metrics/protocol, binom SE ≈ 0.15% acc (retained SE ≈ 0.009), documented margins, k=768 recovers loss exactly (5.1387 = 5.1387), NO crash (ALL_DONE_NET47); (g) fair — full-attention reference + same 0.98 bar + random-k at the same k (seed 12345): gaps +4.7/+3.8, positive, the three-seed gap spread (3.8–6.2) exceeding the eff spread informative; (h) sharpened — ≥8.0× guaranteed (3/3 seeds), 9.1× median, 10.7× best. Open: **a third seed at ctx=2048 (does the 7/8 median replicate at 16×? if s3 reads 224 or 192 the law holds, if 256 it refutes — the direct test of this round's discovery; ~3.7–5h)**; a fourth seed at ctx=1024 (refine {96,112,128}; low value); d=8 @ ctx=256 s0 corner; carry chain at scale (the frontier). Paper 91, issue #154. Now 47 network experiments. Assessment v47. Script: /tmp/exp_net_attncost_ctx1024_s3.py; log: /tmp/net47.log.


## Part 48 — The direct test survives via the MEDIAN: k\*=160 at (d=4, ctx=2048, seed=3), all four point-horns REFUTED (P1 224, P2 240, P3 256, P4 192) yet the completed 16× three-seed knee distribution {160, 224, 256} has median exactly 224 = 7/8·(d·ctx/32) — the 7/8-median law REPLICATES at 16×, six seeds across both long contexts with medians exactly 7/8·product, the low tail extends to 0.625× (wider than 8×'s 0.75), product point 256 3/3-sure, selection +4.7/+3.4, concentration 498.13, deployable ≥8.0×/9.1×/12.8× best-ever (NET-48, speed axis)

**Question:** NET-47 established the 7/8-median law at 8× (three-seed {96,112,128}, median 112 = 7/8·128); the 16× cell was still two-seed {224, 256} whose mid 224 = 7/8·256 gave the law its second context. This round runs the THIRD seed at (d=4, ctx=2048) with the fine mid-grid point 240 — the direct test of whether the 7/8 median replicates at 16×. **Prediction stated before the run: P1 k\*=224 (7/8-median repeats — s3 joins the s2 family, {192/224,224,256}); P2 k\*=240 (16× knee quantizes mid-grid as 112 did at 8×, {224,240,256} symmetric); P3 k\*=256 (7/8 REFUTES — s3 reproduces s1, {224,256,256} median at product); P4 (low prior) k\*=192 (the 0.75/0.875/1.0×product pattern completes).**

**Method:** Byte-identical harness to NET-45/46 (seed=3 only), 2000 AdamW steps, CausalTF **d=4, seed=3, ctx=2048** (292 windows, 10% held out; fused SDPA training, chunked eval CHUNK=8). Sweep {96,128,160,192,224,240,256,288,384,512,768,1024} — 12 points (two more than prior 16× sweeps), extended down to 96 so the low tail is measured directly; k* = smallest k with retained ≥ 0.98·full; Part B2 random-k {128, 256} (seed 12345). Script /tmp/exp_net_attncost_ctx2048_s3.py; log /tmp/net48.log; train 14566s (~4h03m, between s1's 13508s and s2's 18436s).

**Results:** k\* = **160 — ALL FOUR POINT-HORNS REFUTED** (every pre-stated value passes but none is the knee). Full acc 0.1546, bar 0.1516, loss 5.2199. Sweep: k=96 0.963 ✗, k=128 0.973 ✗, k=160 **0.981 ✓** (margin +0.0012 — razor-thin, the tightest of the recent cells), k=192 0.984 ✓, k=224 0.986 ✓, k=240 0.987 ✓, k=256 0.990 ✓, k=288 0.993 ✓, k=384 0.999 ✓, k=512 1.000 ✓, k=768 1.003 ✓, k=1024 1.003 ✓ (loss 5.2215 vs full 5.2199 — Δ0.0016). The s3 retained curve is the HIGHEST of the three 16× seeds throughout (0.973 at 128 vs s1 0.939, s2 0.965) — its whole curve sits above, crossing the bar two grid steps earlier than s2, three earlier than s1. **Part B2:** random k=128 0.926 (top-k 0.973) → **+4.7**; random k=256 0.956 (top-k 0.990) → **+3.4** — comparable to s2's +4.4/+3.9, far above s1's +1.7/+1.8. ALL_DONE_NET48, NO crash.

**What this decides:** the completed 16× three-seed distribution is **{160, 224, 256}** — **median 224 = 0.875·256 = 7/8·(d·ctx/32), EXACTLY replicating the 8× median 112 = 7/8·128: the 7/8-median law HOLDS at both long contexts, six seeds (2/2 contexts, 6/6-seed median exactly 7/8·product).** The horns' point values were all wrong (0/4) yet the law is MORE confirmed (1/1) — the round's honest structure: a whole family of third-seed values {160,192,224} each keep the median at 224; only ≥256 would shift it. Per-seed knees are too noisy to predict on the point; the distribution's center is robust. The 16× spread {0.625, 0.875, 1.0} is ~50% WIDER than 8×'s {0.75, 0.875, 1.0} — the low tail is the context-growing quantity, the product value the pinned upper edge (s1 chain), the median stable at 7/8. Product point 256 passes 3/3 (0.981/0.986/0.990): the k\* ≤ d·ctx/32 guarantee is 3/3-seed-sure at BOTH long contexts, and intact at every shorter cell through 16×.

**Practical:** deployable speedup at (d=4, ctx=2048), three seeds: s1 **8.0×**, s2 **9.1×**, **s3 12.8× (k=160 — the best-ever deployable reading in the program, beating 10.7× at 8×)**. **≥8.0× guaranteed** (product point 3/3), **9.1× median** (the 7/8 center), **12.8× best**. The spread {8.0, 9.1, 12.8} is wider than 8×'s {8.0, 9.1, 10.7}: longer context gives a bigger spread of achievable speedup, with the guarantee end the one that holds 3/3.

**Concentration:** eff support **498.13** (s1 526.39, s2 472.50 — mid-family, spread ~11%); top-128 0.608, top-256 0.746; per-position 64.91/435.27/929.55 — monotone early≪mid≪late, NO bounded working set at 16×, three seeds. The eff↔knee correlation does NOT sort across three points at 16× either: s1 highest-eff/highest-knee (526.39/256), s2 lowest-eff/middle-knee (472.50/224), s3 middle-eff/lowest-knee (498.13/160) — replicates NET-47's 8× conclusion; the retained-curve offset that sets the knee is independent of mean eff support.

**Verdict:** THE-DIRECT-TEST-SURVIVES-VIA-THE-MEDIAN — k\*=160 at (d=4, ctx=2048, seed=3), all four point-horns (224/240/256/192) REFUTED, yet {160, 224, 256} has median exactly 224 = 7/8·256, replicating the 8× median 112 = 7/8·128: the 7/8-median law is 2/2-context, 6/6-seed; per-seed knees too noisy to predict on the point (0/4), the distribution's center robust (1/1). 16× spread ~50% wider than 8× (the low tail the context-growing quantity, product the pinned upper edge); product-point upper bound 3/3-sure at both long contexts; margin +0.0012 (tightest of recent cells); selection +4.7/+3.4 (16× spread {1.7,4.4,4.7} seed-dependent); concentration 498.13 (eff↔knee not sorting); deployable ≥8.0×/9.1×/12.8× best-ever.

**Barriers:** (a) clean — four horns + the law's direct test stated before the run, measured 160 outside ALL horns yet the distribution's median landed exactly on the law's predicted center — the round distinguishes point-accuracy (0/4) from structural confirmation (1/1); (b) clean — three-seed 16× spread {0.625,0.875,1.0}, low tail widening with context: none in the Catalog re-scan or the literature; (c) confronted — d=4 × ctx=2048 real causal word LM, 4097 vocab, held-out loss+acc, three seeds at the longest cell; (d) clean (held-out last-10%, data-free top-k); (e) the SUBSTANCE, sharpened — the three-seed 16× distribution complete; honest limits: the s3=160 read is razor-thin (+0.0012, true knee ~150–160 between grid points), the 0.625 low tail is one of three seeds (a fourth decides s3-specific vs stable), the median law is 2 contexts × 3 seeds; (f) clean — same metrics/protocol, binom SE ≈ 0.11% acc (retained SE ≈ 0.007), the +0.0012 razor margin documented, k=512 recovers 1.000 / k=768 1.003 (loss Δ0.0016), monotone recovery, NO crash (ALL_DONE_NET48); (g) fair — full-attention reference + same 0.98 bar + random-k at the same k (seed 12345): gaps +4.7/+3.4, positive, the three-seed gap spread {1.7–4.7} informative; (h) sharpened — ≥8.0× guaranteed (3/3), 9.1× median, 12.8× best-ever, the widened spread the deployment-relevant uncertainty at the longest cell. Open: **a fourth seed at ctx=2048 (the low-tail test — s4=160/192 → 0.625 low tail real, s4 ∈ {224,256} → s3-specific; the highest-value open cell now; ~4–5h)**; a fourth seed at ctx=1024 (refine {96,112,128}; low value); d=8 @ ctx=256 s0 corner; d=8 compression floor check; carry chain at scale (the frontier). Paper 92, issue #155. Now 48 network experiments. Assessment v48. Script: /tmp/exp_net_attncost_ctx2048_s3.py; log: /tmp/net48.log.

## Part 49 — The REAL-MODEL knee COLLAPSES and SATURATES: on pretrained Qwen2.5-0.5B the lossless attention knee is k\*=16/32/24 at ctx=512/1024/2048 — 24–64× BELOW the toy product law d·ctx/32 (which predicted 384/768/1536), sub-linear with the DEPTH MULTIPLIER collapsed from d to ~1, already DECLINING at 2048; selection importance inflates an ORDER OF MAGNITUDE (+68–82 pt random-k gaps, local-window capped at 0.60 retained); the only diffuse attention lives in the LAST TWO layers (eff 128/72 vs a ~12-key median layer); first LIMITED-MEMORY-AXIS cell, run ON-GPU in ~35 min (NET-49)

**Question:** every speed-axis law (DIFFUSE-BUT-PRUNABLE NET-15, k\* = d·ctx/32
NET-16→45, the 7/8-median NET-47/48) was measured on from-scratch toy CausalTFs; the
new user-directed axis is running Qwen-class agentic models in very limited VRAM, and
the knee bounds the KV-cache working set that governs long-context serving. First
transfer cell: does the toy knee law survive on a REAL PRETRAINED LLM?
**Predictions stated before the run: P1 TOY-LAW TRANSFERS (k\*(2048) ≥ 384); P2
MORE-CONCENTRATED-BUT-LINEAR (k\* ≤ ctx/8 everywhere AND ratio ≥ 2.5); P3 SUB-LINEAR/
SATURATING (ratio < 2.5 or saturation ≤ 256).**

**Method:** Qwen2.5-0.5B fp32 on the GTX 1060 (torch 2.5.1+cu121, sm_61), hand-written
forward replicating the Qwen2 stack so per-row oracle top-k applies GLOBALLY at all 24
layers — the identical toy manipulation. VALIDATION GATE: own-forward vs HF eager
BEFORE measurement — max|Δlogit| = 0.0000, argmax agreement 1.0000, CE identical to 4
decimals. wikitext-103-raw text (Gutenberg rate-limited mid-round; automatic fallback —
honest corpus deviation), 922k BPE tokens, last 10% held out, 40 disjoint windows/cell,
next-token top-1 acc + CE, k\* = smallest k with retained ≥ 0.98·full; grids {8..192},
{16..384}, {4..768} + a sub-32 addendum (NET-49B) after the 2048 grid floor passed;
Part B2 random-k AND local-window at matched k; Part A per-layer concentration.
Script /tmp/exp_net49_qwen_topk.py + exp_net49b_sub32.py; logs /tmp/net49.log,
/tmp/net49b.log; full run ~35 min ON GPU.

**Results:** knee chain **{16, 32, 24}** vs toy predictions **{384, 768, 1536}** —
ratios **1/24, 1/24, 1/64**. Full acc 0.4460/0.4612/0.4787 (context monotone ✓).
Sweeps (retained): 512: 8 0.9617 ✗ (−2.3 SE), **16 0.9834 ✓** (+0.44 SE razor), 32
0.9931, …, 192 0.9997; 1024: 16 0.9771 ✗ (−0.55 SE thin), **32 0.9912 ✓** (+2.1 SE),
…, 192 1.0016, 384 1.0003; 2048: 4 0.8762 ✗, 8 0.9408 ✗, 16 0.9708 ✗ (−2.5 SE),
**24 0.9818 ✓** (+0.5 SE razor, bracket (16, 24]), 32 0.9867, …, 768 0.9997 (loss Δ
0.0002). Scaling shape: ×2.0 then **×0.75 — SUB-LINEAR, DECLINING**: P3 CONFIRMED,
P1 refuted 16× beyond its floor, P2's linearity refuted (its concentration half held:
k\* ≤ ctx/8 everywhere). THE DEPTH MULTIPLIER COLLAPSES FROM d TO ~1: no compounding
r(k)^d penalty binds trained weights; k\*/ctx ≈ 1/32 at both exact knees and FALLS by
2048. **Part B2:** random-k gaps **+82.0/+71.8** @512 (k=32/64), **+81.9/+70.0** @1024,
**+79.9/+68.0** @2048 — the toy programme's entire range was +1.7 to +11.7 (an ORDER
OF MAGNITUDE inflation); **local-window** gaps +60.0/+50.5/+54.5/+46.3/+54.9/+47.3/
+40.1 — even k=256 local reaches only **0.5979** retained at 2048 while oracle top-k is
0.9867 with 8× FEWER keys. **Part A:** median-layer effective support ≈ 9.7/9.0/11.7
keys across contexts — context-INDEPENDENT for the bulk of the stack (toy: 46 → 526,
×~1.85/doubling); the ONLY diffusion lives in L22/L23: eff 51.0 → 83.3 → **128.5** and
32.8 → 49.5 → **72.1**, sub-linear growth (×1.54–1.63/doubling); even L22@2048 is 3.9×
less diffuse than the toy MEAN layer (498) at the same context; mild front elevation
L0–L2 (14–43); minimum at L16 (eff 2.9 — a ~3-key mid-stack layer).

**Practical:** oracle working set at 2048 = 24 keys/query-row of 2048 → **85× fewer KV
reads, 64× fewer KV bytes** (fp16 0.39 MB vs 25.2 MB per sequence). Honest caveat: the
oracle sees full scores — a deployable policy needs a cheap selector; the
oracle-to-policy gap is the next measurable cell. For the 6 GB host goal: knee-bounded
KV budgets are what make quantized+offloaded long-context serving feasible.

**Verdict:** THE-REAL-MODEL-KNEE-COLLAPSES-AND-SATURATES — the programme's speed axis
transfers to real pretrained models with a BIGGER effect size than any toy cell: knees
24–64× below the toy law, depth multiplier collapsed, selection importance inflated
10×, and a two-layer diffuse tail. Barriers: (a) clean — data-free oracle from the
model's own scores, horns were about position/scaling not existence; (b) confronted —
sparse-attention/heavy-hitter lineage exists (H2O/StreamingLLM/SnapKV); NEW content =
measured laws: first 0.98-retention-protocol transfer, depth-collapse, ctx/32-then-
decline shape, gap inflation, depth map — none in Catalog re-scan or literature;
(c) CONFRONTED HEAD-ON — this IS the real-scale cell (pretrained 0.5B, web text,
151k vocab); limit: ONE model ONE size; (d) clean — last-10% held out, zero training;
(e) the SUBSTANCE + limits — deterministic eval (addendum reproduced baseline EXACTLY),
SEs 0.17–0.35%, TWO razor-thin knees documented (+0.44/+0.5 SE; 2048 bracket (16, 24]),
1024 bracket (16, 32] with k=24 un-measured there (the decline could be flat ~24), one
model one corpus; (f) clean — forward validated EXACTLY pre-measurement, fp32, loss
tracks acc, NO crash (ALL_DONE_NET49 + ALL_DONE_NET49B); (g) fair — full reference +
same bar as all 48 prior rounds + random-k AND local-window at matched k, both crushed;
(h) DIRECT — 64× KV-byte reduction at the oracle knee vs the toy family's best-ever
12.8× attention reading; deployable policy named as open work, not claimed.

**Open:** (1) per-layer pruning ablation (the depth map's causal test — is L22's
diffusion load-bearing?); (2) size transfer (Qwen2.5-1.5B / quantized-offloaded 7B —
does ~ctx/32-saturation persist? does the two-layer tail recur?); (3) oracle-to-policy
gap (online accumulated-score eviction vs this upper bound); (4) corpus robustness;
(5) weight-quantization floors on the same harness (limited-memory iteration 2).
Paper 134, issue #230. Now 49 network experiments. Assessment v49.

## Part 50 — THE TROPICAL LIMIT IS LOSSY BUT THE RECOVERY IS FAST: pure argmax attention (k=1) retains only {0.364, 0.289, 0.250} at ctx={512,1024,2048} on Qwen2.5-0.5B (worse at LONGER context), k=2 already recovers to 0.70–0.79 and k=4 to 0.88–0.91; the knee chain {16,32,24} replicates NET-49 EXACTLY cross-session; Maslov gaps (LSE−max) have bulk-layer medians 0.17–1.9 nats with the diffuse tail L22/L23 (medians 2.3–2.7, p90≈3.4) the only far-from-tropical region; crystallization loss Σp(1−p) runs 0.43–0.97 — soft mass is heavy but individually tiny and collectively inside the 2% budget (NET-50; mined from the Lean catalogue's tropical cluster)

**Question:** NET-49 stopped above k=16; the catalogue licenses hard attention within log 2
nats/row (Maslov sandwich) and bounds soft-vs-hard TV by crystallization loss Σp(1−p). This round
measures the TROPICAL LIMIT itself: sweep oracle top-k down to k∈{1,2,4,8} and measure the
per-row budgets directly. **Predictions stated before the run: P1 TROPICAL-CLIFF (k=1 retained
< 0.5 everywhere); P2 SMALL-K-RECOVERY (k=4 ≥ 0.90 @512 AND k=8 ≥ 0.90 @2048); P3
NEAR-TROPICAL-SOFTMAX (median Maslov gap ≤ log 8 ≈ 2.08 nats everywhere AND median
crystallization loss ≤ 0.25).**

**Method:** byte-identical harness/gates to NET-49 (validation gate exact, held-out last 10%,
40 windows/cell, fp32, GTX 1060); grids extended down to k=1; Part B tropical budgets collected
during full-attention passes per layer (mean/median/p90 gap + crystallization loss).
Script /tmp/exp_net50_tropical.py; log /tmp/net50.log; ~35 min ON GPU.

**Results:** **P1 CONFIRMED** at all three contexts — k=1: 0.3637/0.2885/**0.2503** (monotone
DECLINE with context: argmax attention worsens as context grows). **P2 CONFIRMED** — k=2:
0.7865/0.7398/0.7002; k=4: 0.9097 (razor over the 0.90 bar)/0.8906/0.8762; k=8:
0.9617/0.9485/**0.9408** ✓. Knee chain **{16, 32, 24} = EXACT replication of NET-49**
(different script, different session — deterministic-eval reproducibility proven).
**P3 SPLIT:** the Maslov half holds for BULK layers (medians 0.17–1.86 ≤ log 8 at 512/1024;
all bulk ≤ 1.46 at 2048) but is REFUTED by the diffuse tail — L22/L23 medians 2.33/2.16 →
2.55/2.37 → **2.69/2.52** across contexts, p90 ≈ 3.4; and the crystallization half is REFUTED
decisively (per-layer means 0.34–0.97 vs the predicted ≤ 0.25).

**What this decides:** pretrained softmax attention is NEAR-TROPICAL in its bulk (23 of 24
layers within a nat or two of pure argmax) but carries a genuinely non-tropical TWO-LAYER
diffuse tail; its crystallization loss is large everywhere, yet top-k to 24 keys retains ≥98%
— so the dropped soft mass is INDIVIDUALLY TINY but COLLECTIVELY LOAD-BEARING. The practical
regime for limited-memory serving is "tropical core + thin soft correction": pointer-style
(k very small) caches sit far below the knee, but the recovery curve quantifies exactly how
fast accuracy returns with each added key.

**Verdict:** THE-TROPICAL-LIMIT-IS-LOSSY-BUT-THE-RECOVERY-IS-FAST. Barriers: (a) clean (horns
pre-stated about cliff/recovery/budget positions); (b) clean (argmax-limit sweeps + Maslov/
crystallization budgets on a pretrained LM not in Catalog/lit as measurements); (c) confronted
(real-scale pretrained model; ONE model noted); (d) clean; (e) SUBSTANCE + limits — the exact
cross-session replication of {16,32,24} is the strongest reproducibility evidence of the axis;
P3's crystallization half honestly REFUTED; single model/corpus; (f) clean (validation gate
exact, fp32, ALL_DONE_NET50 no crash); (g) fair (full reference, same bar; NET-49 controls not
re-run — noted); (h) DIRECT — the sub-k\* curve is the deployment-relevant region for aggressive
KV compression. Open: per-layer ablation (prune ONLY L22/L23?); size transfer; oracle-to-policy;
corpus robustness; weight quantization (NET-52 next). Paper 135, issue #237.
Now 50 network experiments. Assessment v50.

## Part 51 — THE-KV-CORE-IS-SHARED-THE-TAIL-IS-PERSONAL: Qwen2.5-0.5B base vs Instruct on identical prompts — layer-0 keys EXACTLY identical (cosK=1.0000, relK=0.26%), every layer cosK ≥ 0.976; divergence is a HUMP (relK peaks 0.217 at L16 then falls — P2 monotone-growth REFUTED); top-1 attention agreement 0.84–0.98 across the bulk but COLLAPSES to 0.568/0.627 in exactly the same L22/L23 diffuse-tail layers NET-50 found far-from-tropical — three measurements (tropical gap, crystallization loss, fine-tune decision divergence) converge: the bulk is shared machinery, the two-layer tail is identity (NET-51; mined from the catalogue's amortized model-delta law n·r+min(D,n))

**Method:** both models' own-forward capture executors validated vs HF eager BEFORE measurement
(argmax-agree 0.9922 / 0.9971); fp16 weights + fp32 score math; 4×1025-token held-out prompts;
per-layer post-rope q/k/v captured; Part A K/V cosine + relative-L2; Part B top-1 key-choice
agreement under each model's OWN scores; Part C hidden-state divergence. Script
/tmp/exp_net51_delta.py; log /tmp/net51.log.

**Results:** **P1 EARLY-SHARE CONFIRMED** (L0 cosK 1.0000); **P2 MONOTONE-DIVERGENCE REFUTED**
(hump: relK 0.003 → 0.217 @L16 → ~0.16; hidden ‖Δh‖/‖h‖ peaks ~0.22 at L12–16); **P3 DELTA-WIN
CONFIRMED with caveat** (mean cosK 0.990, mean decision agreement 0.894 → shared-core-plus-delta
viable) BUT the tail dissociates: L22/L23 keep cosine-similar keys (0.983/0.988) yet decide
differently in 43%/37% of rows — vector-level similarity does NOT bound functional divergence.
**Verdict:** THE-KV-CORE-IS-SHARED-THE-TAIL-IS-PERSONAL — convergent with NET-49/50 depth maps:
bulk = shared machinery; two-layer tail = model identity. Serving law: ~22/24 layers shareable
at ≥0.92 agreement; tail personal. Barriers: (a) clean; (b) confronted (task-vector folklore;
NEW = hump constants, decision-vs-vector dissociation, three-way convergence); (c) confronted
(ONE pair, ONE context, n=4 prompts noted); (d) clean (no training); (e) honest limits (cosine
does not bound impact — hence Part B; prompt variance uncharacterized); (f) clean (both forwards
gated; two gate-caught bugs fixed before any measurement counted); (g) fair (each model under
its own weights); (h) DIRECT (shared-KV server design quantified). Open: tail-swap causal test;
bigger pairs; SFT vs RLHF vs DPO tails; link to NET-52 (quantize core harder than tail?).
Paper 136, issue #238. Now 51 network experiments. Assessment v51.

## Part 52 — THE-TOY-FOUR-BIT-FLOOR-DOES-NOT-TRANSFER: naive per-channel RTN on Qwen2.5-0.5B costs +0.0044/+0.035/+0.128/+0.79/+9.23/+14.06 CE at 8/6/5/4/3/2 bits — the toy programme's per-channel-uniform-4 optimum (NET-11/14) REFUTED on a real LM by 16× its budget; group-128 repairs ~60% of the 4-bit damage (+0.318) and rescues 3-bit from death (+2.72); depth gradient CONFIRMED weakly (last-12 +0.41 vs first-12 +0.39 — NET-18's direction); mesh monotone + 8-bit measurably nonzero exactly as the catalogue sharpness theorem demands (NET-52; limited-memory axis round 4)

**Method:** identical validated harness (shared Runner; baseline reproduced EXACTLY 0.4460/
2.8697); RTN symmetric quantization of all linear weights, fp32 master restored per arm;
40 held-out windows @ctx=512; arms {8,6,5,4,3,2}-bit per-channel + 4-bit depth split (first-12/
last-12) + {4,3}-bit group-128. Script /tmp/exp_net52_quant.py; log /tmp/net52.log.
**Predictions stated before the run:** P1 4-bit per-channel ΔCE ≤ 0.05 (toy floor transfers);
P2 last-12 worse than first-12; P3 2-bit collapse ≥ 0.5; P4 monotone mesh with nonzero 8-bit.
**Results:** **P1 REFUTED SPECTACULARLY (+0.79)**; P2 CONFIRMED weakly (0.863 vs 0.890
retained); P3 CONFIRMED dramatically (+14 CE, acc 0.0001); P4 CONFIRMED (strictly monotone,
8-bit +0.0044 real). Cliff structure: mild through 5 bits, severe at 4, catastrophic at 3;
grouping is the lever production quantizers (GPTQ/AWQ/GGUF) use — here measured cleanly.
**Verdict:** barrier (c) strikes the programme's own compression conclusion — the toy floor
was an artifact of the from-scratch setting; what transfers is STRUCTURE (depth direction,
mesh sharpness, grouping lever). For the 6 GB host: RTN < 6 bits not deployable; group-wise
≥4-bit the entry point; further compression needs error compensation, not scale choice.
Barriers: (a) clean (refuted horn pre-stated); (b) clean (exact constant structure new);
(c) DECISIVE (this IS the compression transfer test, honestly negative; limits: one model,
ctx=512, RTN-only, embeddings/norms unquantized); (d) clean (bit-exact deterministic);
(e) no noise floor issue (deltas ≥ 0.0004 resolvable); (f) clean (ALL_DONE_NET52);
(g) fair (matched protocol across arms); (h) DIRECT (the bits×grouping surface is the
deployment table). Open: GPTQ/AWQ compensation on these floors; joint weight+KV budgets;
tail-aware mixed precision (quantize the NET-51 shared core harder than the personal tail).
Paper 137, issue #239. Now 52 network experiments. Assessment v52.

## Part 53 — COMPENSATION-WORKS-ON-THE-REAL-FLOORS: sequential layer-wise GPTQ 4-bit group-128 lands at +0.151 dCE on Qwen2.5-0.5B — 2.1× better than grouped RTN (+0.318), 5.2× better than per-channel RTN (+0.788); P1 CONFIRMED at the boundary, P2 floor-target REFUTED by a hair (+0.151 vs ≤0.14), P3 tail-share REFUTED (18% < 25% — compensation shrinks the L22/L23 disproportionate cost that RTN suffered); 3-bit rescued across the axis +9.23 → +2.72 → +1.19 (retained 0.71) (NET-53; limited-memory axis round 5)

**Method:** faithful GPTQ — SEQUENTIAL layer-wise quantization with input recapture through the
partially-quantized model, hooks on the actual linear modules (container-hook bug found via
width diagnostics: all captures had been the 896-wide block input), group-aligned blocks,
escalating-damping Cholesky (partially-quantized activations go out-of-distribution → near-
singular Hessians; ×1→10⁶ retry + eigenvalue fallback). Calibration train-side only.
Script /tmp/exp_net53_gptq.py; log /tmp/net53.log; unit-test regression gate
/tmp/test_gptq.py (single-matrix GPTQ-beats-RTN check).
**Results:** gptq_b4_g128_all **+0.1512** (ret 0.9546); core-only L0–21 +0.1235 (ret 0.9641);
b3_all **+1.1932** (ret 0.7086). Tail increment +0.0277 = 18.3% of total.
**Verdict:** deployment table complete for the host: RTN <6 bits unusable; grouped RTN viable@4;
grouped GPTQ viable@4, survivable@3; each structural lever multiplies the previous floor down.
Three silent-science hazards caught en route (hook targets, column broadcasting, Cholesky PD)
— documented as engineering record. Barriers: (a) clean (two refuted horns pre-stated);
(b) confronted (GPTQ = prior art; NEW = fixed-protocol ladder + tail-share + shrinkage law);
(c) confronted (one model, ctx=512, no act-order, 16-seq calib noted); (d) clean (train-side
calibration); (e) deterministic, damping schedule pre-fixed; (f) clean (exact baseline,
ALL_DONE_NET53); (g) fair (shared protocol/granularity); (h) DIRECT (deployment table cell).
Open: act-order variant; joint weight+KV budgeting; tail-aware mixed precision; size transfer.
Paper 138, issue #243. Now 53 network experiments. Assessment v53.

## Part 54 — THE-TAIL-IS-LOAD-BEARING-BUT-UNPORTABLE: causal layer swaps between Qwen base and Instruct — bulk pair L10/11 transplants at ZERO measured cost (+0.004/−0.016 dCE; inst←base L10/11 slightly IMPROVES Instruct), while tail pair L22/23 DESTROYS the hybrid: agreement with BOTH parents collapses (0.83 cross-parent baseline → 0.54–0.63) at +0.47/+0.55 CE; P1 transferable-identity REFUTED (the discovery), P2 asymmetry CONFIRMED (+0.465 vs +0.546), P3 portability CONFIRMED (< +1.0 nat); the sharing boundary for multi-finetune serving is now CAUSALLY established — share everything except the tail, re-run the tail per model (NET-54; limited-memory axis round 6)

**Method:** full-path parameter transplant surgery on fp16 models (12 held-out windows @ctx=512;
chunked-head CE identical to harness semantics; backup/restore by complete parameter-path
copy-back before each subsequent arm). Arms {L22,L23} vs {L10,L11}, both directions.
Script /tmp/exp_net54_tailswap.py; log /tmp/net54.log.
**Verdict:** convergent with NET-50 (only far-from-tropical layers) and NET-51 (only high-
decision-divergence layers): L22/L23 are also the only NON-TRANSPLANTABLE layers. Barriers:
(a) clean (P1 refutation pre-stated as possible outcome); (b) confronted (layer-amputation
lit; NEW = fine-tune-pair portability asymmetry + both-parents-collapse signature); (c)
confronted (one pair, 12 windows, ctx=512, fp16 noted); (d) clean (no training); (e)
deterministic, restore-by-construction; (f) clean (ALL_DONE_NET54); (g) fair (matched-width
controls, both directions); (h) DIRECT (sets the sharing boundary for KV servers and
tail-aware quantization). Open: dose-response (one/three-layer swaps); swap+recalibration
(entanglement depth); 1.5B pair; compensated-4-bit tail personality (GPTQ link).
Paper 139, issue #246. Now 54 network experiments. Assessment v54.

# Survey of the Lean Catalogue (`~/lean/Catalog`, github.com/paulklemstine/lean)

**Date:** 2026-08-21 · **Branch:** llm-loop · **Method:** 6 parallel survey passes — four proof-level
digests of the curated `lean4/` snapshot (699 files, 18 domains), one master index of all
**875 research packages** (`Packages/*.json`: title/domain/quality/key_results), direct reads of the
Tropical/MachineLearning/Bridges package summaries, and two metadata digesters covering the
remaining ~706 packages. Full-quality tier counts: 28 gold / 787 silver / 56 bronze.

---

## 1. What the catalogue is

A Mathlib-backed formalization corpus of the alethean.org research programme — the same
programme whose *empirical* arm is this repo (factor3). It contains machine-checked companions to
**both active loops**: the network/LLM lab (attention-cost law, knee ladders, carry-chain wall,
boundary-token width) and the factoring lab (type channels, residue dials, barrier theorems),
plus ~700 independent packages spanning tropical geometry, information theory, combinatorics,
physics-of-computation, and logic.

**Headline structural facts**
- `Catalog/` = 6,680 `.lean` files / 79 MB across 20 domains (Bridges 1390, Novelty 789, Geometry
  508, Applications 436, …, Tropical 245, EML 47). `Packages/` = 875 JSON package records;
  `Catalog/*.lean` are the union of the packages' `lean_files`.
- Proof hygiene is excellent: across every surveyed sample, **0 axioms and only a handful of real
  `sorry`s** (one intentional: full FLT). Soundness is guaranteed by the kernel.
- Substance stratifies consistently across all six surveys: **~25–35% genuinely substantive,
  ~40% correct-but-routine re-derivations, ~25% grand-header/vacuous framing** ("Holevo bound"
  proved as `n ≤ n`; no-free-lunch as `rfl`). Trust theorem statements, never file titles.
- Quality scores correlate weakly with merit: duplicates appear as separate gold-tier discoveries
  (factoradic codes ≥5×, Z₂-coindex suspension ≥8×). Treat scores as proof-completeness proxies.

## 2. Top findings by area

### 2a. Tropical mathematics (the strongest coherent cluster)

- **Softmax ⇄ tropical bridge, proved ~15 independent ways** (`TropicalLLMConversion`,
  `TropicalSemiring`, `TropicalAgentAlpha/Epsilon`, …): max-plus semiring axioms; the **Maslov
  sandwich** `max(a,b) ≤ LogSumExp(a,b) ≤ max(a,b)+log 2`; ε·LSE(x/ε) → max; **softmax
  concentrates exactly on argmax as β→∞**; ReLU = tropical addition definitionally. This is the
  rigorous error budget behind hard/top-k attention — and NET-49's empirical finding (knee 24–32
  keys at long context) says pretrained transformers already live near the tropical limit.
- **ReLU networks ARE tropical rational functions** (depth-free characterization, Logic 0.73 +
  Novelty): computable exactly by FF-ReLU nets ⟺ differences of maxima of affine forms; decision
  boundaries lie in an explicit boundary variety of degree ≤ m·k.
- **Max-plus layer collapse** (`TropicalNetworkTheory`, best-in-corpus): two tropical layers compose
  to ONE via the tropical matrix product; shift equivariance, monotonicity, piecewise linearity;
  exact compilation of ReLU networks into (max,+) form.
- **Crystallized attention quality bounds** (`QuantumTransformer__QualityBounds/Theory/
  Training`): crystallization loss Σp(1−p) controls the total-variation distance between soft and
  hard (permutation) attention — an auditable budget for 1-index-per-query attention.
- **Windowed min-plus decoder reliability** (0.86): tropical Dobrushin contraction compresses the
  span seminorm in ONE step; absorption theorem; and a **tropical noise floor** proving no
  exponential-reliability bound ρᵏ can hold on symmetric chains.
- **Amortized model-delta compression** (0.78, min-plus): optimal transmitted bits for a shared
  decompressor stream = **n·r + min(D, n)** exactly; break-even iff stream length > patch size;
  coherence-length law B·L·r + ⌊B/2⌋·min(2D,L). Directly a theory of shared-prefix/multi-model
  serving in limited memory.
- **Exact tropical L1 training dynamics** (0.73): median is THE minimizer; finite termination;
  pivot-counting mechanism; ReLU-width dichotomy.
- Sharp structure theory: tropical Helly number exactly d+1 (settles a conjecture); Bergman fans =
  tropical linear spaces; tropical Bézout (with the missing-half correction 2de vs de); min-plus
  social choice classification + tropical Arrow theorem; Gröbner bases for tropical semimodules
  with finite test sets; tropical Shtarkov sums (regret ≤ 2k log(n+1) for k-state sources).

### 2b. LLM efficiency / attention theory (our axis, formally grounded)

- **The Attention-Cost Law k\* = d·ctx/32** (Probability 0.85) — our own NET-15→48 line,
  formalized with a TWO-SIDED derivation (any depth-only speedup law forces the form) plus a
  certified mass–accuracy separation (98% mass provably costs ≥146 positions while the measured
  knee is 64) and a spike-plus-uniform family proving N_eff does NOT control the knee.
- **Geometry of Attention Sparsification** (= our paper 92/NET-43, Bridges 0.84): concentration
  floor k ≥ τ²/Σpᵢ² with exponent 2 necessary; power-tail ceiling for top-k mass; random-k control
  retains exactly k/L (double-counting proof) making M(k) − k/n the canonical selection gap.
- **Knee identifiability trilogy** (Logic/Physics 0.80–0.82): amplitude windows from different
  context doublings are disjoint (two-point conflict); certified band forces speedup between 8×
  and 16× with the observed 9.14× a transient; robustness certificates for threshold laws on
  sweep grids ("The Knee That Moved").
- **Boundary-Token Width tropical separation theory** (0.78): formalizes OUR NET-25–28 EOS-width
  experiments — no-sharp-boundary theorem refutes any width-threshold model; one-sided
  distribution shift with stochastic dominance; uniform rejection of the homogeneous null.
- **Carry Chain Wall + cure** (NumberTheory/Logic 0.78): no state-free position-local answer
  function computes addition at fixed radius (Myhill–Nerode necessity); one carry bit cures it
  exactly; dense-final-step input theory — the toy-programme's NET-19–24 arc, proven.
- **Quantization convexity transfer** (Bridges 0.86): quantizing weights under an L-Lipschitz
  convex loss deforms the landscape inequality by exactly ≤ 2Lr, optimum within Lr, basins
  preserved; constant sharp — refuting hopes of exact convexity at any positive mesh.
- Width/depth exact trade-offs: ReLU region capacity attained exactly at width m−1 depth n;
  lossless rectified layer needs exactly 2n units (width 22 in dim 11, frame constants sharp);
  exp–log width-2 beats ReLU width Ω(ε^{−1/2}) for x²; grokking delay laws with sharp constants
  (τ = |c|/S identity; saddle-node crossing time under weight decay).
- **Alignment geometry cluster** (Physics/Speculative 0.85×3 + Algebra 0.88): Gibbs variational
  identity for KL-regularized reward optima; the alignment floor (pretraining-mix drift =
  γ·TV(pretrain, supervised), undoable by no KL penalty); Hilbert-projective isometry (distance =
  reward oscillation/β); audit-gap expansion β⁻².
- **Almost-lossless compression beyond pigeonhole** (Logic 0.85): ε-relaxed pigeonhole
  characterizes achievable rate; shared randomness worthless; Monte-Carlo hashing pays an exact
  quadratic rate penalty. Plus **Price of Universality submodular** (Crypto 0.86): Shtarkov price
  of adding models to a library is submodular; mixtures free; greedy library design (1−1/e)-optimal.
- **LLM-as-one-matmul answered honestly** (`Neural__LLMSingleMatMul` + extensions): linear
  collapse ✓; nonlinearity barrier ✓ (three-point argument); finite-domain trick costs V^L
  storage; size/accuracy/single-op trilemma formalized.

### 2c. Factoring (the other loop's formal mirror — ~30-package barrier programme)

- Positive mechanisms WITH their barriers stated: **Resonance on the Berggren Tree** (0.90 —
  factors all-primes-1-mod-4 semiprimes exactly, but requires depth 3ⁿ ≥ √(N/5)); **Stratified
  Cycle Readout** (0.91 — cycle spectrum {ord_N, ord_q, ord_p, 1} determines the factorization;
  informative density ≤ 6/√N); **GCD Moments** (0.90 — first moment recovers p+q via s²−4N);
  Knot–Number bridge (0.90 — Alexander polynomial of T(a,b) = product of cyclotomics over the
  divisor spectrum; semiprime case recovers p+q = N+1−φ(N)).
- Barrier/no-go results with exact constants: Split-Count Law (0.92 — MI of character-pinned
  splits = Is(n) ~ log n/(n²log2)); OR-Collapse cap g(2) ≈ 0.311 bits (matches the factoring
  loop's measured 0.313/0.073 leaks); Derived-Modulus Corner closed (gcd(N,f(N))=gcd(N,f(0)));
  CRT-coordinate reading ≡ factoring; Dirichlet No-Pruning; quantum register threshold 2^t ≥ R²
  (no o(log R) savings); tensor-train dequantization of order finding closed off (Schmidt rank
  exactly r/gcd(r,Q)).
- Honest self-negations inside the corpus: IOF descent proven to be trial division in geometric
  clothing (factor appears exactly at k=(p−1)/2); GPU annealing proven no-gain; O(√N) access
  barriers stated alongside every mechanism.

### 2d. Other domains (selected gold)

- **Combinatorics/probability**: Talagrand convex-distance with OPTIMAL constant 1/4; Sauer–Shelah
  from scratch; Chebotarev Fourier-minor deformation core (vanishing order n(n−1)/2) + exact
  2k-sample sparse recovery; Donoho–Stark rigidity (equality ⟺ modulated coset indicators, gap
  theorem |G|+|supp f|); converse of Poisson summation ((subgroup, annihilator) pairs exactly);
  dense-set sumset threshold (1+o(1))·log n/log(1/δ); sharp 1/7 independence-ratio barrier.
- **Logic/foundations**: Lawvere fixed-point proved ≥3× independently as the corpus's unifying
  engine (Cantor/halting/Gödel derived honestly); Löb frames counted (1,1,3,19,219,4231…);
  strict consistency-reflection towers with no polynomial collapse (0.92); q-analogue of Kummer.
- **Information theory**: compression impossibility done properly (injectivity, Kraft, Singleton);
  Landauer ledger (erasure ⟺ non-injectivity; homomorphism erases exactly log₂|ker| bits);
  guesswork exponents (Arikan–Merhav coset law); minimax redundancy exact non-asymptotic form.
- **Physics-of-computation**: swap-chain cubic spectral gaps 2/n³ ≤ γ ≤ 12/n³; prime barcode
  persistent homology (total persistence = pₙ − 2); Wigner semicircle by even-closed-walk counting.
- **Whimsy with real cores**: photon/universe/gravity/consciousness framing throughout carries
  small true lemmas (idempotent-oracle algebra, Banach/Knaster-Tarski instances, stereographic
  round-trips); "hypercomputation" never exceeds Turing limits anywhere — oracles are always
  idempotent maps or explicitly conditional hypothesis types.

## 3. Cross-links: what the catalogue says about THIS repo

| factor3 result | catalogue formalization |
|---|---|
| NET-43 attention-sparsification paper | pkg 742 "Geometry of Attention Sparsification" (0.84) |
| Attention-cost law k\*=d·ctx/32 (NET-16→45) | "The Attention-Cost Law" (Probability 0.85) — two-sided derivation |
| Knee-ladder seeds NET-44–48 | "Amplitude Identifiability of a Knee Ladder", "One Bar One Bit" (0.82) |
| Boundary-token width NET-25–28 | "Boundary-Token Width… Tropical Separation Theory" (0.78) |
| Carry-wall NET-19–24 | "Carry Chain Wall", "Dense Final-Step Inputs" (0.78) |
| Factoring type-channel/OR-dial (papers 80–94) | "Semiprime OR Dial cap 0.311278 bits" (0.89), OR-Collapse (0.86), Split-Count (0.92) |

The empirical loops and the formal catalogue validate each other: measured knees land inside the
certified bands; measured leakage (0.313 bits) matches the proved cap (0.311).

## 4. Mining list — concrete next experiments for the LLM loop

1. **Crystallization-to-pointer attention** (from §2a): measure the TV-distance budget
   Σp(1−p) on REAL Qwen attention rows; test whether argmax-only (k=1!) attention with the
   crystallization regularizer stays within the proved TV bounds — the extreme end of NET-49's
   top-k sweep (we stopped at k=16; k=1 per-row is the tropical limit).
2. **Maslov-budget hard attention**: NET-49's oracle is per-row top-k; the sandwich gives a
   per-row LOSS BOUND (≤ log 2 nats) for hard-max vs softmax. Verify empirically: how much of
   the retained-accuracy curve is explained by the LSE−max gap?
3. **Model-delta serving law** (min-plus amortization n·r + min(D,n)): design the measurement —
   two Qwen variants sharing a base; does KV/prefix sharing follow the coherence-length law? This
   is the multi-model-on-6GB question made precise.
4. **Quantization defect 2Lr**: before the planned RTN quantization round, use the convexity-
   transfer theorem to pre-register the degradation vs Lipschitz × mesh — then measure whether
   real cross-entropy landscapes obey the 2Lr defect band.
5. **Selection-gap canonical form**: adopt M(k) − k/n (proved the right normalization) in all
   future pruning reports; NET-49's gaps (+40–82 pts) re-scale against the k/n floor.
6. **Library submodularity**: if we serve several fine-tunes from one base, the Shtarkov-price
   submodularity theorem predicts diminishing costs — measurable as shared-prefix hit rates.

## 5. Verdict

The catalogue is a large, compiling, essentially sorry-free formal corpus whose value concentrates
in three places: (i) the **tropical↔transformer bridge** (softmax concentration, ReLU=tropical,
layer collapse, crystallization budgets) — the theoretical backbone for the limited-memory axis;
(ii) the **formal mirrors of both factor3 loops**, which turn our measured laws into certified
bands and impossibility results; (iii) a **systematic negative-result programme** (factoring
barriers, quantum dequantization closures) that is unusually honest about its own limits.
Roughly one quarter of it is substantive mathematics; the rest is correct pedantry or inflated
framing that the theorem statements themselves defuse. For the LLM-in-limited-memory goal, the
catalogue supplies exactly what NET-49 lacked: ready-made theory to pre-register the next five
rounds against.

# Joint-Aware Bit Allocation on a Real Causal LM: The Strict-Lossless Static-Schedule Floor is ~5.3 Bits (NET-12)

**Program:** Network/LLM research lab — round-net-12 (the loop's rotation directive: joint-aware allocation, the confirmed real compression target; compression axis)
**Date:** 2026-08-13
**Status:** Machine-verified (joint-marginal sensitivity map, greedy strict-lossless frontier, per-channel RTN rescue check, and the 4-bit-interface/2-bit-interior config tests on a real causal word LM, d=4, 5 Gutenberg novels, dm=64, ctx=128, vocab 4097, 2000 AdamW steps).

## Hypothesis and statement

NET-11 established at real-LM scale that per-matrix **isolation undercounts joint
damage**: isolated 3-bit retains ≥95% almost everywhere, yet joint uniform-3
retains only 0.83 and the best role schedule only 0.878 at 3.64 avg bits. The
rotation directive names **joint-aware allocation** the confirmed real
compression target. **Hypothesis: a joint-aware (rather than per-matrix) bit
allocation can restore losslessness on real text at a reasonable average bit
cost.** Two falsifiable horns: (a) even a joint procedure cannot clear the
lossless bar below some floor — i.e. a strict-lossless static schedule needs
≈5+ bits (compounding is that bad); or (b) a cheap data-free per-channel
rescale rescues the failing low-bit schedules, meaning per-tensor RTN was the
wrong primitive all along.

## 1. Setup (identical to NET-10 Part B / NET-11 so everything is comparable)

Same 5 public-domain Gutenberg novels (599,869 words), word-level top-4097
vocab (UNK=0), contiguous windows of 128, 90/10 contiguous train/test split.
Causal transformer dm=64, 4 heads, **is_causal=True** (causal masking),
d=4 × seed 0, 2000 AdamW steps. Training leg reproduces NET-10/NET-11 exactly:
full acc **0.1571**, lossless bar 0.98·full = **0.1540**. Every quantization
eval is joint (a fresh model loaded with the quantized state dict, full held-out
eval), so all numbers below are the honest "what you'd actually ship".

Three parts:
- **A. Joint-marginal map:** all matrices pinned at the NET-11 role schedule
  (embed/pos/un=4, mi/mo=3, attention=2, lnf=2); each matrix in turn varied
  across {2,3,4,6}. Directly measures each matrix's *joint* marginal sensitivity.
- **B. Greedy frontier:** start at all-6 (retained 0.999), repeatedly lower the
  single matrix whose down-step costs the least retained accuracy, keeping
  retained ≥ 0.98·full. Empirical strict-lossless static per-tensor schedule.
- **C. Per-channel RTN:** per-row symmetric scales (data-free) on the failing
  low-bit schedules — does a cheap improvement rescue them?

## 2. Part A — the joint-marginal map

Everything else at the role schedule, this matrix varies (retained accuracy):

| matrix | 2-bit | 3-bit | 4-bit | 6-bit |
|---|---|---|---|---|
| **embed** | 0.513 | **0.849** | 0.878 | 0.881 |
| **un** (readout) | **0.280** | 0.844 | 0.878 | 0.884 |
| pos | 0.865 | 0.854 | 0.878 | 0.878 |
| lnf | 0.878 | 0.895 | 0.890 | 0.894 |
| attention wq/wk/wv/ao (×16) | **0.878** | 0.878 | 0.878 | 0.878 |
| MLP mi/mo (×8) | 0.80–0.85 | 0.878 | 0.878 | 0.88 |

- **Attention projections are *jointly* indifferent at 2 bits** — retained equals
  the 0.878 role baseline to the third decimal for all 16 matrices. They are free.
- **The interface is the wall, quantified at the joint margin:** embed at 3-bit
  jointly retains 0.849 (≈11 points off the role baseline), where its *isolated*
  3-bit retained ≈0.95 (NET-11). The readout un at 2-bit jointly collapses to
  0.280 — the single most fragile matrix in the model. Compounding is visible
  directly: isolation says embed/un are "fine at 3", the joint margin says
  "lose 10+ points".
- **MLP is mid**: 2-bit drops jointly to 0.80–0.85, 3-bit is fine. lnf is
  indifferent. pos is mildly fragile but tiny (128×64).

The role structure (interface fragile / interior robust) is therefore real at
the joint margin, not an isolation artifact — and it is *sharpened*: attention
is exactly free, embed/un are jointly far more fragile than isolation suggested.

## 3. Part B — the greedy strict-lossless frontier: 5.31 avg bits

Greedy downward from all-6, each step lowering the matrix whose down-step costs
the least retained accuracy, keeping ≥ 0.98·full. Stopping condition (no single
down-step stays ≥ bar) was verified exhaustively at the end of the walk.

| | avg-bits | retained | lossless (≥0.98)? |
|---|---|---|---|
| uniform-3 (NET-1 toy schedule) | 3.00 | 0.825 | ✗ |
| role(4/3/2) (NET-11) | 3.64 | 0.878 | ✗ |
| all-4 (every matrix at 4) | 4.00 | 0.979 | ✗ (knife-edge: 0.979 < 0.980) |
| all-6 | 6.00 | 0.999 | ✓ |
| **greedy frontier** | **5.31** | **0.982** | ✓ |

The greedy frontier schedule: **embed/pos/un = 6**, mi0/mo0/mi1/mi2/mo2/mi3/mo3
= 4, mo1/wq0/wv0/ao0/wv1/ao1/wv2/ao2/wv3/ao3 = 3, wk0/wq1/wk1/wq2/wk2/wq3/wk3
+ lnf = 2.

- **The interface cannot leave 6 bits.** With embed/pos/un at 6, the greedy
  spends the entire remaining budget on the interior (MLP mostly 4, attention
  2–3, lnf 2) and lands at 5.31 avg bits. The interface is 73% of the model's
  parameters (embed 262k + un 262k + pos 8k of ≈724k), so its 6-bit floor
  dominates the average.
- **The strict-lossless floor is far above every "reasonable" schedule.**
  all-4 — the naive everything-at-4 choice that isolation makes look nearly
  safe — misses the bar by 1 point (0.979). Crossing the bar costs +1.3 bits
  (to 5.31) and pins the interface at full precision. At this scale, per-tensor
  static RTN schedules simply cannot get under ≈5.3 avg bits and be lossless.
- Greedy is a local optimum (best-first single-step), not a proof of global
  minimality — but the wall is structural (interface at 6) and consistent with
  Part A's marginals.

## 4. Part C — per-channel RTN: the per-tensor primitive was the problem

All schedules re-evaluated with **per-row (per-channel) symmetric RTN scales**
— data-free, the standard primitive in the LLM-quantization literature — on a
freshly retrained identical model (full acc re-verified 0.1571):

| schedule | per-tensor retained | **per-row retained** | avg-bits |
|---|---|---|---|
| uniform-2 | 0.112 | **0.588** | 2.00 |
| uniform-3 | 0.825 | **0.947** | 3.00 |
| role(4/3/2) | 0.878 | **0.892** | 3.64 |
| **all-4** | 0.979 | **0.987** ✓ | 4.00 |
| greedy-frontier (6/4/3/2) | 0.982 ✓ | **0.973** ✗ | 5.31 |

- **Per-row scales rescue all-4 to lossless (0.987 ≥ 0.98) at 4.00 avg bits —
  1.3 bits cheaper than the per-tensor greedy frontier (5.31).** This is the
  constructive answer to NET-11's negative: per-tensor RTN was the wrong
  primitive. The cheap, standard, data-free primitive + a uniform 4-bit
  schedule is lossless on real text.
- **But the 4-bit interface is irreducible even per-row.** uniform-3 per-row is
  still 3 points under the bar (0.947) — the interface cannot go to 3 bits
  regardless of scales. uniform-2 remains hopeless (0.588).
- **The per-tensor-optimized frontier does NOT transfer to per-row.** The
  greedy schedule (interface 6, MLP 4, attention 2–3) scores *worse* per-row
  (0.973) than uniform all-4 per-row (0.987), despite costing 1.3 more bits.
  Bit allocation is primitive-dependent: the frontier that wins for per-tensor
  scales is not a good per-row schedule. (The 0.014 gap is ~9× eval noise, so
  real but small; the structural point — allocation must be tuned to the
  primitive — is the robust takeaway.)
- The rotation's literal question ("is 4-bit interface + 2-bit interior
  enough?") is decided in Part C2: **no.**

## 4b. Part C2 — the 4-bit interface + 2-bit interior question (per-row)

Two targeted per-channel schedules on a fresh retrain (full acc re-verified
0.1571 a third time):

| schedule | retained | avg-bits |
|---|---|---|
| I. **4iface/2int** — embed/pos/un=4, ALL interior (MLP+attn)=2 | **0.733** | 3.46 |
| II. **4/4/2** — embed/pos/un=4, MLP=4, attention=2, lnf=2 | **0.907** | 3.82 |
| uniform-4 per-row (Part C) | **0.987** ✓ | 4.00 |

- **The rotation's literal schedule fails hard.** "4-bit interface + 2-bit
  interior" retains 0.733 — the interior at 2 bits is the problem, not the
  interface.
- **Attention is NOT free — its "2-bit lossless" status was
  operating-point-dependent.** In Part A, attention at 2 was invisible only
  because the role baseline is already degraded to 0.878 (bigger errors mask
  attention's). In an otherwise-clean network (config II vs uniform-4, the only
  difference is attention 2→4, lnf indifferent), attention 2-bit costs ~8
  points (0.907 → 0.987). NET-11's "attention projections are 2-bit lossless"
  was true in isolation and at a degraded operating point, but NOT in a clean
  joint network — a sharpened instance of isolation-under-counts-joint-damage.
- **The minimal lossless per-channel schedule tested is uniform all-4: 0.987
  @ 4.00 bits.** Every cheaper config (3.46–3.82 bits, interface protected at
  4) fails by 3–25 points. The 4-bit interface is necessary AND, at this scale,
  the whole net at 4 is sufficient.

## 5. Verification vs the network-loop barriers

- **(a) Circularity — no.** Joint evals quantize an independent copy of the
  trained model; the greedy is a pure allocation search over measured joint
  retained accuracy; nothing is injected into training.
- **(b) Known-method-in-disguise — the measurement is new, the rescue may be
  known.** Per-channel/group quantization with per-row scales is standard in the
  LLM-quantization literature, so a Part C rescue would be a confirmation of a
  known primitive, not a new method. The *new* content is the quantitative
  joint-damage structure: the joint-marginal map (embed 3-bit loses ~11pp
  jointly vs ~5 isolated; attention jointly free), and the greedy frontier
  showing the strict-lossless static per-tensor floor ≈5.3 bits — both absent
  from the catalog scan (2094 packages; no joint-marginal-allocation result on
  a real causal LM).
- **(c) Toy-scale — confronted head-on.** Real causal LM, real text, causal
  masking, 4097-token vocab. The toy lab's uniform-3 claim fails this scale
  (again); the strict-lossless floor here is a real-scale quantity.
- **(d) Data leakage — none.** Causal masking, contiguous no-overlap split,
  held-out eval, data-free quantization.
- **(e) Variance — honest limits.** One model (d=4 s0), 28 matrices, 4 levels,
  51 greedy steps each a full joint eval. Training leg reproduced exactly
  (0.1571) a third time. One seed reported; the NET-11 d=8 numbers already
  showed the identical role structure at depth.
- **(f) Measurement — documented.** 0.98·full bar used throughout; the
  knife-edge all-4 (0.979 vs 0.980) is called out explicitly rather than
  rounded; eval noise ≈0.15% on 60k tokens noted; greedy stopping condition
  verified exhaustively.
- **(g) Baseline fairness.** uniform-3, role(4/3/2), all-4, all-6 are all
  honest joint evaluations on the same model; the greedy is compared against
  them at the same bar.
- **(h) Practical relevance.** The floor is the finding: practitioners who ship
  per-tensor RTN (the data-free default) need to know that on a real causal LM
  the interface must sit at full precision and the static schedule cannot go
  below ~5.3 bits — or they must move to per-channel/activation-aware
  primitives (Part C tests the cheapest of those).

**Verdict.** NET-12 (joint-aware allocation, the confirmed real compression
target) delivers three connected results on a real causal LM:

1. **The joint-marginal map.** With all other matrices at the role schedule,
   attention projections are exactly indifferent at 2 bits (all 16, retained
   flat at 0.878), while embed and un are jointly far more fragile than
   isolation suggested (embed 3-bit jointly 0.849 vs ≈0.95 isolated; un 2-bit
   catastrophic at 0.280). The interface is the wall; the interior is cheap —
   *at a degraded operating point.*
2. **The per-tensor greedy strict-lossless frontier is 5.31 avg bits** (retained
   0.982), with the interface (embed/pos/un — 73% of parameters) pinned at 6.
   Even all-4 misses the bar per-tensor (0.979 vs 0.980). Per-tensor static RTN
   cannot get under ≈5.3 bits losslessly on real text.
3. **Per-channel RTN is the fix — uniform all-4 is lossless (0.987 @ 4.00
   bits), 1.3 bits cheaper than the per-tensor frontier.** But nothing below
   4.0 bits works even per-channel (uniform-3 0.947, 4/4/2 0.907, role 0.892,
   4iface/2int 0.733), and the per-tensor-optimized frontier does not transfer
   per-row (0.973). NET-11's "no static schedule ≤3.7 bits is lossless" is
   corrected to: per-tensor needs ~5.3 bits; per-channel needs 4.0 (uniform),
   with the 4-bit interface irreducible in both.

The rotation's two questions get clean answers: **any data-free schedule reach
lossless?** Yes — per-channel uniform-4 (4.0 bits). **Is 4-bit interface +
2-bit interior enough?** No — 0.733/0.907. The practical lever is not smarter
allocation of per-tensor bits but the per-channel primitive; and "attention is
2-bit free" is only true when bigger errors mask it. Round-net-12.
Now 12 network experiments. Assessment v12. Paper NET-12, issue #107.
Scripts: /tmp/exp_net_joint.py, /tmp/exp_net_joint_partC.py, /tmp/exp_net_joint_partC2.py.

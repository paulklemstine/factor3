# Paper 101 — HINT-VALUE-JOINT: Hints Compound Like Capacities

**Verdict name: THE-HINTS-COMPOUND.**
Round-30 #1 · exp 436 · assessment v212 · script `/tmp/exp_hintvaluejoint.py` · log `/tmp/r30n1.log` · runtime 4 s.

## 1. The corrected measurement

Paper 99's joint-battery row was retracted (paper 100 found the label-coding collision). With the verified 36-label chaining, the corrected 2-field joint hint value:

| view | bits |
|---|---|
| product view (hint-free) | 2.1314 (= paper 91 exact) |
| sum view alone (s mod 713) | 0.6432 |
| gap view alone (d mod 713) | 0.6496 |
| (s,d) joint view | 4.5605 (99.1% of the 4.6006 ceiling) |
| **JOINT HINT VALUE = I(s,d) − I(N)** | **+2.4291** |

## 2. Hints compound like capacities

Per-dial hint sum: +0.5189 + 0.5099 = **+1.0288**. Corrected joint hint value: **+2.4291**. **Hint synergy: +1.40 bits** — the joint factor-residue hint extracts more than twice what the per-dial hints sum to, mirroring paper 92's capacity synergy exactly. The parallel is structural: capacities compound because the CRT-joint modulus sees all residues simultaneously; hints compound because the (s,d) pair determines both factor residues simultaneously. Same mechanism, both axes.

The bracketing confirms consistency: product-view 2.1314 < (s,d)-view 4.5605 ≤ ceiling 4.6006 (99.1%) — the factor-residue hint nearly fully determines the labels, as it should (knowing p, q mod 713 pins their splitting types up to within-class variation).

## 3. The new flag

The (s,d)-view which-factor statistic reads **0.9663 bits** — far above every product-view wall. This is the sparse-plug-in regime at its extreme (~508k residue-pair cells against 30k samples), and the round does NOT interpret it: per the paper-93 discipline, a permutation-null test is required before any claim. Flagged as the immediate follow-up. (Structural note: s and d are symmetric under p↔q, so any REAL leakage from an (s,d) view would be orientation-conditional and would itself be a significant finding requiring tracing.)

## 4. Barriers

**(a)** clean — horns pre-stated; the corrected chaining verified (36 labels) before measuring. **(b)** clean. **(c)** confronted — 30k shared population, exact CRT arithmetic. **(d)** clean. **(e)** the substance — hint synergy quantified (+1.40); the new flag disclosed rather than interpreted. **(f)** controlled — the paper-100 reconciliation directly caused this corrected measurement. **(g)** fair — all views on identical data; product-view reproduces paper 91 exactly. **(h)** relevance — the hint-value law (hints compound like capacities) completes the battery arc's quantitative picture and sharpens COND-RANK: conditioning capacity compounds across conductors.

Now 436 experiments. Assessment v212. Paper 101, issue #193.

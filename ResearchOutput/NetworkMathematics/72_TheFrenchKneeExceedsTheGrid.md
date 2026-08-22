# The French Knee Exceeds the Grid: on French prose NO grid point reaches the 0.98 bar — k=24 retains only 0.965 at ctx=512 and k=32 only 0.968 at 1024 — a domain shift FAR larger than German's +4, bracketing the French knees at >24 and >32 respectively; the tokenizer-tax is language-graded (code −4, English 0, math 0, German +4, French ≥+8), and the single-parameter base model breaks: non-English domains need per-language measurement, not interpolation (NET-72)

**Program:** Network/LLM research lab — round-net-72 (LIMITED-MEMORY AXIS, iteration 41;
fourth domain-jump leg).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact, argmax-agree 1.0000; French prose from Gutenberg,
fsynced durable cache; 12 windows @2048-equivalent VRAM budget; ALL_DONE_NET72).

## Setup

Fine grids k ∈ {4..24}@512 and {8..32}@1024 on FRENCH PROSE (Qwen2.5-0.5B fp32,
identical harness/gate/bar). One Gutenberg source succeeded (the second 404'd) — honest
limit stated. Script ResearchOutput/exp_net72_french.py; results
~/f3cache/net72_results.json; log /tmp/net72.log.

**Predictions stated BEFORE the run:** P1 ROMANCE-TAX-MATCHES-GERMANIC ({20, 24});
P2 ROMANCE-LIGHTER ({16, 20}); P3 BETWEEN.

## Results

| ctx | best grid point | retained | verdict |
|---|---|---|---|
| 512 | 24 | **0.9648 ✗** | knee > 24 |
| 1024 | 32 | **0.9680 ✗** | knee > 32 |

Full acc: 0.584/0.591 (higher than prose's 0.446/0.461 — French IS easier to predict,
yet needs MORE keys).

**Scorecard: ALL THREE HORNS REFUTED** — the shift exceeds +8 keys, far past every
pre-stated bracket. The knee-quantizes-to-even-grid pattern also breaks: the curve rises
smoothly without a clear knee in the measured range.

## Verdict

THE-FRENCH-KNEE-EXCEEDS-THE-GRID — the domain-shift law is NOT a simple ±4 fine-step:
language families differ by whole grid ranges. The four-domain table was complete for its
four domains but does not interpolate to unseen languages. The accuracy/knee decoupling now
has both signs: code is easier AND needs fewer; math is harder AND needs equal; French is
easier AND needs more — prediction difficulty tracks neither direction of the budget.
Mechanism hypothesis: Qwen's tokenizer spends more tokens per French word than per English
word, diluting each token's attention contribution — the tax is TOKENIZATION-mediated, not
LANGUAGE-mediated per se (testable: measure tokens-per-word across domains). Honest limits:
ONE text source (second URL 404'd), grid may not have reached the true knee (both KSTARs
None), 12-window equivalent VRAM budget.

Barriers: (a) clean — three horns pre-stated, all refuted; (b) clean — first beyond-grid
domain result; (c) confronted — limits: one source, sub-knee ceiling stated; (d) clean;
(e) deterministic; (f) clean (ALL_DONE_NET72); (g) fair — identical harness except text;
(h) DIRECT — multilingual serving cannot interpolate budgets; per-language measurement is
required.
Open: tokens-per-word mechanism test; extended grid {48, 64}; more languages; 7B cell.
Paper 157, issue #312. Now 72 network experiments. Assessment v72.

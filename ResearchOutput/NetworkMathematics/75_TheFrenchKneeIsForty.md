# The French Knee Is Forty: the extended grid pins k\*(fr@1024) = **40** — k=36 fails (0.980), k=40 passes (0.983) — exactly DOUBLE the English prose knee of 20 at the same context; the tokenizer-tax is NOT a fixed +4 fine-step but a domain-dependent MULTIPLIER, with French requiring 2× the attention budget of English despite only 7% higher tokens-per-word — confirming NET-73's refutation of tokenization density and pointing to language-specific attention pattern structure as the mechanism (NET-75)

**Program:** Network/LLM research lab — round-net-75 (LIMITED-MEMORY AXIS, iteration 47;
the French extended grid resolving NET-72's open bracket).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact, argmax-agree 1.0000; 24 held-out windows @ctx=1024;
ALL_DONE_NET75).

## Setup

Extended grid k ∈ {36, 40, 48, 56, 64} on FRENCH PROSE (corpus-B = wikitext shard 1
French content, Qwen2.5-0.5B fp32, identical harness/gate/bar). Script
ResearchOutput/exp_net75_frenchext.py; results ~/f3cache/net75_results.json;
log /tmp/net75.log.

**Predictions stated BEFORE the run:** P1 GRID-ARTIFACT (k\* ≤ 48); P2 TOKENIZER-TAX-
PROPORTIONAL (~28–32).

## Results

| k | 36 | 40 | 48 | 56 | 64 |
|---|---|---|---|---|---|
| retained | 0.9795 ✗ | **0.9830 ✓** | 0.9855 ✓ | 0.9896 ✓ | 0.9916 ✓ |

Full acc 0.4946 (matches NET-72's corpus-B baseline). **P1 CONFIRMED** — the knee exists
within the extended grid. **P2 REFUTED** — it is 40, not ~28–32.

## Verdict

THE-FRENCH-KNEE-IS-FORTY — exactly 2× English prose's 20 at the same context. The complete
five-domain table @1024: code=12, EN-prose=20, math=20, DE-prose=24, FR-prose=40.
The tokenizer-tax is NOT a constant +4: German pays +4, French pays +20. The tax scales
with the DEPTH of the language shift from English — germanic +4, romance ×2. Combined with
NET-73's TPW refutation, the mechanism must be in HOW attention patterns are structured
within each language, not how many tokens are used. The increment (+4/doubling) appears
domain-universal (French 40@1024 → predicted 44–48@2048 if shape holds), but the BASE is
strongly domain-dependent.

Barriers: (a) clean — two horns pre-stated incl. the refuted P2; (b) clean — first beyond-
coarse-grid French measurement; (c) confronted — limits: one source, one context stated;
(d) clean per-corpus split; (e) deterministic; (f) clean (ALL_DONE_NET75); (g) fair —
byte-identical harness; (h) DIRECT — the deployment table gains its largest entry.
Open: French @512 extended (is base 12 or higher?); increments@4096; more languages;
7B cell. Paper 160, issue #316. Now 75 network experiments. Assessment v75.

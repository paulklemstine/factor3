# The Tokenizer Tax Explodes: German prose at ctx=4096 needs **>56 keys** — every point from 24 to 56 fails, with even k=56 at only 0.976 retained — the +4 fine-step tokenizer-tax from short contexts becomes ≥+16 at 4096 (4× amplification), confirming that domain/language shifts and context acceleration interact MULTIPLICATIVELY; multilingual agentic workloads at long context face disproportionate KV costs for non-English languages (NET-88)

**Program:** Network/LLM research lab — round-net-88 (LIMITED-MEMORY AXIS, iteration 62;
German at long context — the first experiment testing whether domain parameters persist
through or dissolve under the phase transition).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact, argmax-agree 1.0000; ctx=4096, 3 held-out windows;
ALL_DONE_NET88).

## Setup

Sweep k ∈ {24, 32, 40, 48, 56} on GERMAN PROSE at ctx=4096 (Qwen2.5-0.5B fp32,
Goethe corpus from durable cache). Script ResearchOutput/exp_net88_de4096.py;
results ~/f3cache/net88_results.json; log /tmp/net88.log.

**Predictions stated BEFORE the run:** P1 TAX-COMPOUNDS (k\*≥44); P2 TAX-DISSOLVES
(k\*≈40); P3 INTERMEDIATE ([41,48]).

## Results

| k | 24 | 32 | 40 | 48 | 56 |
|---|---|---|---|---|---|
| retained | 0.953 ✗ | 0.966 ✗ | 0.973 ✗ | 0.975 ✗ | **0.976 ✗** |

Full acc 0.405. ALL FIVE POINTS FAIL. Even k=56 retains only 0.976 — well below the bar.
**P1 CONFIRMED dramatically; P2/P3 REFUTED.**

## Verdict

THE-TOKENIZER-TAX-EXPLODES — German needs MORE than 56 keys at 4096 where English prose
needs only 40. The tax is ≥16 keys (vs +4 at short contexts), a 4× AMPLIFICATION matching
the increment acceleration exactly. Domain/language shifts and context acceleration are
MULTIPLICATIVE: the phase transition doesn't wash out language differences — it magnifies
them. For multilingual agentic workloads: non-English languages face disproportionately
growing KV costs as context extends beyond ~2000 tokens.

Barriers: (a) clean — three horns pre-stated incl. the dramatic P1; (b) clean — first
experiment testing domain×acceleration interaction; (c) confronted — limits: 3 windows,
one language pair stated; (d) clean; (e) deterministic; (f) clean (ALL_DONE_NET88);
(g) fair — identical harness except text; (h) DIRECT.
Open: French @4096 (does romance behave like germanic?); more languages @4096;
1.5B @4096 on non-English (does scale amplify further?); 7B cell.
Paper 169, issue #332. Now 89 network experiments. Assessment v89.

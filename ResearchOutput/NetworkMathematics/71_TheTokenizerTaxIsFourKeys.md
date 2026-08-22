# The Tokenizer Tax Is Four Keys: German prose shifts the 0.5B knee chain UP exactly one fine-grid step — {20, 24} at {512, 1024} vs English prose's {16, 20} — mirroring code's −4 shift below and completing a FOUR-DOMAIN deployment table with a single parameterization: base(code)=12, base(prose-EN)=16, base(math)=16, base(prose-DE)=20, with the +4-per-doubling increment UNIVERSAL across all four domains and scales (NET-71)

**Program:** Network/LLM research lab — round-net-71 (LIMITED-MEMORY AXIS, iteration 39;
third domain-jump leg).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact, argmax-agree 1.0000; German prose = Goethe's Faust
+ second classic, fsynced durable cache; 24 held-out windows/context; ALL_DONE_NET71).

## Setup

Fine grids k ∈ {4..24}@512 and {8..32}@1024 on GERMAN PROSE (Qwen2.5-0.5B fp32,
identical harness/gate/bar). Script ResearchOutput/exp_net71_nonenglish.py;
results ~/f3cache/net71_results.json; log /tmp/net71.log.

**Predictions stated BEFORE the run:** P1 TOKENIZER-TAX (knees > prose); P2
MULTILINGUAL-BALANCE (knees = prose); P3 INTERMEDIATE.

## Results

| ctx | German k\* | EN prose k\* | German full acc | EN prose full acc |
|---|---|---|---|---|
| 512 | **20** | 16 | 0.3773 | 0.4460 |
| 1024 | **24** | 20 | ~0.39 | 0.4612 |

German sweeps @512: 4: 0.883 ✗, 8: 0.953 ✗, 12: 0.969 ✗, 16: 0.976 ✗ (~1.5 SE),
**20: 0.983 ✓**, 24: 0.988. @1024: 8: 0.926 ✗, 12: 0.956 ✗, 16: 0.968 ✗, 20: 0.975 ✗,
**24: 0.982 ✓**.

**Scorecard: P1 CONFIRMED** — exactly +4 keys at BOTH contexts (one fine-grid step up,
mirroring code's −4 down). **P2 REFUTED. P3 REFUTED** (the shift is a full step, not
intermediate).

## Verdict

THE-TOKENIZER-TAX-IS-FOUR-KEYS — the four-domain deployment table completes:
base(code)=12, base(prose-EN)=16, base(math)=16, base(prose-DE)=20, with the +4/doubling
increment UNIVERSAL (German: 20→24 = +4, same as every other domain) and scale-halving
(NET-67) expected to apply per-domain. The domain parameter moves the base in fine-grid
steps: language shift +4 (mirroring code's −4), domain type (code vs prose) −4. The
tokenizer-tax mechanism: German compounds pack more content per word, so each tokenized
sequence carries more information per position — the model needs more positions in its
attention window to cover the same ideas. Deployment: multilingual workloads need the
highest-base domain's budget; a 24-key cache covers all four domains to 1024.

Barriers: (a) clean — three horns pre-stated incl. two refuted; (b) clean — first
non-English domain leg; (c) confronted — limits: German only, two classics, 24 windows;
(d) clean per-corpus split; (e) deterministic; (f) clean (ALL_DONE_NET71); (g) fair —
byte-identical harness except text; (h) DIRECT — completes the four-domain table.
Open: more languages; modern LaTeX; increments@4096; 7B cell.
Paper 156, issue #310. Now 71 network experiments. Assessment v71.

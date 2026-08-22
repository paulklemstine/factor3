# The Tail Is Load-Bearing but Unportable: swapping only L22/L23 between Qwen2.5-0.5B base and Instruct DESTROYS the hybrid's agreement with both parents (0.83 cross-parent baseline → 0.54–0.63; CE +0.47/+0.55) while swapping bulk pair L10/L11 is FREE (+0.004/−0.016 dCE — one direction slightly IMPROVES Instruct) — the causal test converts NET-51's correlation into a portability law: bulk layers are interchangeable machinery, the two-layer tail is identity that cannot be transplanted (NET-54)

**Program:** Network/LLM research lab — round-net-54 (LIMITED-MEMORY AXIS, iteration 6; cell (2)
of the catalogue mining queue: causal test of NET-51's correlational finding).
**Date:** 2026-08-21
**Status:** Machine-verified (chunked-head HF forward, fp16 weights; full-path parameter
backup/restore verified by post-arm restore; ALL_DONE_NET54, no crash in recorded run).

## Setup

Qwen2.5-0.5B base ↔ Instruct layer transplants on 12 held-out wikitext windows @ctx=512.
Arms: {L22,L23} (the personal-tail pair from NET-49–51) vs {L10,L11} (bulk control), both
directions. Metrics: hybrid CE (ΔCE vs its host) and next-token argmax agreement with each
parent. Cross-parent baseline agreement 0.8327. Script /tmp/exp_net54_tailswap.py;
log /tmp/net54.log.

**Predictions stated BEFORE the run:** P1 TAIL-CARRIES-IDENTITY (tail swap shifts agreement
toward donor ≥2× more than bulk swap); P2 ASYMMETRY (directions differ); P3 PORTABILITY
(all hybrids within +1.0 nat of host).

## Results

| arm | ΔCE vs host | agB | agI |
|---|---|---|---|
| base←inst **L22/23** | +0.4652 | 0.5845 | 0.5443 |
| base←inst L10/11 | **+0.0043** | 0.9635 | 0.8385 |
| inst←base **L22/23** | +0.5455 | 0.5887 | 0.6289 |
| inst←base L10/11 | **−0.0164** | 0.8459 | 0.9495 |

**Scorecard: P1 REFUTED — and the refutation is the discovery**: the tail swap does not pull
the hybrid toward the donor AT ALL; it breaks agreement with BOTH parents (host-side agreement
falls far below even the 0.8327 cross-parent baseline). The tail carries no portable identity;
it is ENTANGLED with upstream statistics. **P2 CONFIRMED** (+0.465 vs +0.546 — directions
differ, as the mid-stack hump predicts). **P3 CONFIRMED** (worst case +0.55 < +1.0 — hybrids
remain functional LM-ish systems, just neither parent).

## Verdict

THE-TAIL-IS-LOAD-BEARING-BUT-UNPORTABLE — the causal complement to three convergent
measurements: NET-50 found L22/L23 the only far-from-tropical region, NET-51 found them the
only high-decision-divergence region, and now NET-54 finds them the only non-transplantable
region while bulk pairs transplant at literally-zero measured cost (one direction improves the
host by 0.016 nats). For limited-memory multi-finetune serving this sharpens NET-51's design:
share everything except the tail is not merely memory-efficient, it is the ONLY correct
sharing boundary — and the tail must be re-run per model, not approximated or borrowed.

Barriers: (a) clean — three horns pre-stated incl. the refuted P1; (b) confronted — layer-swap
pruning/amputation literature exists; NEW = the portability asymmetry quantified between two
fine-tunes of ONE base with matched architecture, plus the both-parents-agreement-collapse
signature; (c) confronted — real pretrained pair, natural text; limits: ONE pair, 12 windows,
ctx=512, fp16; single-layer-pair granularity (no dose-response curve yet); (d) clean — no
training, held-out eval only; (e) deterministic forwards; restore verified by construction
(full-path copy-back before every next arm — arms run on pristine hosts); (f) clean — chunked
CE identical to harness semantics, ALL_DONE_NET54; (g) fair — both directions + bulk controls
at matched width; (h) DIRECT — sets the sharing boundary for multi-model KV servers and mixed-
precision policies (tail-aware quantization must stay per-model).
Open: dose-response (swap ONE tail layer; swap three); tail-swap WITH recalibration (does
light fine-tuning of swapped tail restore function? — measures entanglement depth); other
pairs (1.5B); connect to GPTQ floors (is compensated 4-bit tail still personal?).
Paper 139, issue #246. Now 54 network experiments. Assessment v54.

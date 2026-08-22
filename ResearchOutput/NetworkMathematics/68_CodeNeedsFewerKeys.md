# Code Needs Fewer Keys: the domain jump to Python source shifts the 0.5B knee chain DOWN one fine step — {12, 16} at {512, 1024} vs prose's {16, 20} — while baseline accuracy jumps UP (0.630/0.652 vs 0.446/0.461); the budget table becomes domain-parameterized with identical structure, and accuracy level is confirmed (third time) independent of knee position: locally-predictable text needs both fewer keys AND is easier to predict (NET-68)

**Program:** Network/LLM research lab — round-net-68 (LIMITED-MEMORY AXIS, iteration 33;
the domain-jump cell).
**Date:** 2026-08-22
**Status:** Machine-verified (gate exact, argmax-agree 1.0000; Python source = 10 CPython
stdlib files, fsynced durable cache; 24 held-out windows/context; ALL_DONE_NET68).

## Setup

Fine grids k ∈ {4..24}@512 and {8..32}@1024 on PYTHON SOURCE CODE (Qwen2.5-0.5B fp32,
identical harness/gate/bar). Script ResearchOutput/exp_net68_domainjump.py;
results ~/f3cache/net68_results.json; log /tmp/net68.log.

**Predictions stated BEFORE the run:** P1 KNEES-TRANSFER (within one coarse step of {16, 20});
P2 CODE-NEEDS-FEWER; P3 CODE-NEEDS-MORE.

## Results

| ctx | code k\* | prose k\* | code full acc | shift |
|---|---|---|---|---|
| 512 | **12** | 16 | 0.6296 | −4 keys |
| 1024 | **16** | 20 | 0.6520 | −4 keys |

Code sweeps @512: 4: 0.930 ✗, 8: 0.969 ✗, **12: 0.981 ✓**, 16: 0.987, 20: 0.988, 24: 0.989.
@1024: 8: 0.960 ✗, 12: 0.976 ✗, **16: 0.981 ✓**, 20: 0.986, 24: 0.987.

**Scorecard: P1 CONFIRMED** — within one fine step. **P2 CONFIRMED** — exactly one fine-grid
step (−4 keys) below prose at BOTH contexts. **P3 REFUTED.**

## Verdict

CODE-NEEDS-FEWER-KEYS — the domain jump shifts the entire knee chain down by a constant
−4 keys while preserving its structure (+4 per doubling increment preserved: 12→16 matches
16→20). The attention-budget law now reads: **k\*(domain, context) = base(domain) +
increment(scale) × doublings(context)**, with base(prose)=16, base(code)=12, and the
increment set by scale (NET-67). Third independent confirmation that accuracy level and
knee position are independent (code is EASIER to predict yet needs FEWER keys). Deployment:
the domain argument of the budget table costs one number per register; serving mixed
workloads should size KV by the largest-base domain present.

Barriers: (a) clean — three horns pre-stated incl. the refuted P3; (b) clean — cross-domain
knee transfer not previously measured in-programme; (c) confronted — limits: ONE code
language, single-repo source, 24 windows; (d) clean — held-out split per corpus; (e)
deterministic; (f) clean (ALL_DONE_NET68); (g) fair — byte-identical harness except text;
(h) DIRECT — parameterizes the deployment table by domain.
Open: more domains (math, non-English); increments-at-4096; 7B cell; probe+recency hybrid
on code (does content help in a structured domain?). Paper 153, issue #306.
Now 68 network experiments. Assessment v68.

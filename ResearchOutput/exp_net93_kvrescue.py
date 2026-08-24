#!/usr/bin/env python3
# NET-93 — RESCUING THE KV CLIFF: BLOCK-SCALED 4-BIT CACHE AND THE K/V ASYMMETRY
# (cpu-large-model axis, iteration 68)
#
# Queue deviation note: the standing queue listed (b) weight-quant floor
# transfer next, but NET-92's verdict created two sharper open cells that
# reuse the identical toolchain at zero download cost, so they jump the queue:
#   (i) does BLOCK SCALING rescue 4-bit KV where raw q4_0 annihilates?
#   (ii) the NET-92-P3 discriminator: at 4 bits (where asymmetry would be
#        visible), does key quantization hurt more than value quantization?
#
# PREDICTIONS STATED BEFORE ANY MEASUREMENT:
#  P1 BLOCK-SCALE-RESCUES-PARTIALLY: q4_1 (per-block scale+offset) lands
#     BETWEEN q8_0 (+0.10%) and q4_0 (+38084%) — predicted dPPL in
#     [+2%, +300%] (wide honest band; direction certain, magnitude not).
#  P2 KEY-SIDE-OWNS-THE-COLLAPSE (P3 discriminator): K4_0/V f16 degrades
#     MORE than K f16/V4_0, by >=5x in dPPL terms (key errors shift softmax
#     selection boundaries and amplify; value errors are linear noise).
#  P3 IMPORTANCE-SCALING-BEATS-UNIFORM: iq4_nl (importance-based block
#     scale) outperforms q4_1 at the same nominal bit width.
import json, os, re, subprocess, time

BIN = os.path.expanduser("~/f3cache/llama.cpp/build/bin/llama-perplexity")
MODEL = os.path.expanduser("~/f3cache/gguf/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf")
SRC = os.path.expanduser("~/f3cache/net49_corpus.txt")
CORPUS = "/tmp/net93_slice.txt"
CTX, THREADS, SLICE_BYTES = 2048, "8", 250_000
RESULTS = os.path.expanduser("~/f3cache/net93_results.json")

ARMS = [("q4_1", "q4_1"), ("iq4_nl", "iq4_nl"), ("q4_0", "f16"), ("f16", "q4_0")]

text = open(SRC, encoding="utf-8", errors="ignore").read()
open(CORPUS, "w", encoding="utf-8").write(text[400_000:400_000 + SLICE_BYTES])
print(f"corpus slice: {os.path.getsize(CORPUS)} bytes", flush=True)

res = {"meta": {"model": MODEL, "ctx": CTX,
                "control_ppl_net92": 7.1093,
                "predictions": "P1 q4_1 dPPL in [+2%,+300%]; "
                               "P2 dPPL(K4_0-only) >= 5x dPPL(V4_0-only); "
                               "P3 iq4_nl > q4_1"},
       "arms": []}

for kt, vt in ARMS:
    t0 = time.time()
    p = subprocess.run([BIN, "-m", MODEL, "-f", CORPUS, "-c", str(CTX),
                        "-t", THREADS, "--cache-type-k", kt,
                        "--cache-type-v", vt], capture_output=True, text=True,
                       timeout=7200)
    out = p.stdout + p.stderr
    m = re.search(r"Final estimate: PPL\s*=\s*([0-9.]+)", out)
    ppl = float(m.group(1)) if m else None
    entry = {"arm": f"K{kt}/V{vt}", "ppl": ppl,
             "wall_s": round(time.time() - t0, 1)}
    res["arms"].append(entry)
    json.dump(res, open(RESULTS, "w"), indent=1)
    print(f"arm K{kt}/V{vt}: ppl={ppl} ({entry['wall_s']}s)", flush=True)

BASE = 7.1093
for a in res["arms"]:
    if a["ppl"]:
        a["d_pct"] = round(100.0 * (a["ppl"] - BASE) / BASE, 3)
json.dump(res, open(RESULTS, "w"), indent=1)
print("\n=== VERDICTS ===", flush=True)
for a in res["arms"]:
    print(f"{a['arm']}: ppl={a['ppl']} dPPL={a.get('d_pct')}%", flush=True)
print("ALL_DONE_NET93", flush=True)

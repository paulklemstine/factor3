#!/usr/bin/env python3
# NET-94 — THE ROLE-SPLIT CACHE: DIRECT K8/V4 CONFIRMATION AND THE 5-BIT KEY PROBE
# (cpu-large-model axis, iteration 69)
#
# NET-93 showed values accept raw 4 bits free while keys collapse in every
# 4-bit format. This cell (a) directly confirms the implied deployment
# configuration K8/V4, and (b) probes whether the key cliff sits between 8
# and 5 bits using q5_1 (the only sub-8 key-capable type besides iq4_nl/q4_x
# llama.cpp offers for KV). Weight-quant floor-transfer ladder deferred until
# its GGUF downloads complete.
#
# PREDICTIONS STATED BEFORE ANY MEASUREMENT:
#  P1 ROLE-SPLIT-WORKS: K8/V4 lands within +-0.5% of f16 control (both
#     halves individually free => combination free; the deployment number).
#  P2 THE-KEY-CLIFF-IS-BELOW-FIVE-BITS: K5_1/V5_1 stays quality-free too
#     (<1%) — the cliff lives strictly between 5 and 4 bits per side.
#     Competing horn (refuting this): K5_1 already collapses (>100%), putting
#     the key floor AT 8 bits practically.
import json, os, re, subprocess, time

BIN = os.path.expanduser("~/f3cache/llama.cpp/build/bin/llama-perplexity")
MODEL = os.path.expanduser("~/f3cache/gguf/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf")
SRC = os.path.expanduser("~/f3cache/net49_corpus.txt")
CORPUS = "/tmp/net94_slice.txt"
CTX, THREADS, SLICE_BYTES = 2048, "8", 250_000
RESULTS = os.path.expanduser("~/f3cache/net94_results.json")

ARMS = [("q8_0", "q4_0"), ("q5_1", "q5_1")]

text = open(SRC, encoding="utf-8", errors="ignore").read()
open(CORPUS, "w", encoding="utf-8").write(text[400_000:400_000 + SLICE_BYTES])
print(f"corpus slice: {os.path.getsize(CORPUS)} bytes", flush=True)

res = {"meta": {"model": MODEL, "ctx": CTX, "control_ppl_net92": 7.1093,
                "predictions": "P1 K8/V4 within +-0.5%; "
                               "P2 K5_1/V5_1 <1% (horn) vs >100% collapse"},
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
print("ALL_DONE_NET94", flush=True)

#!/usr/bin/env python3
# NET-92 — THE KV-CACHE QUANTIZATION LADDER AT 7B (cpu-large-model axis, iteration 67)
#
# Weights are already Q4_K_M; at ctx>=2048 the KV cache is the other half of the
# memory budget. This round measures how far KV precision can drop on the same
# CPU-resident Qwen2.5-7B-Instruct, via llama-perplexity with -ctk/-ctv ladders.
#
# PREDICTIONS STATED BEFORE ANY MEASUREMENT:
#  P1 EIGHT-BIT-KV-IS-NEAR-LOSSLESS: kv=q8_0 degrades perplexity by <1% vs f16
#     (mirrors the weight-side finding that ~8 bits suffices away from the
#     fragile interface/tail structure, NET-84/85).
#  P2 FOUR-BIT-KV-IS-NOT: kv=q4_0 degrades perplexity by >5% (keys are the
#     selection interface NET-52 called fragile; the weight-side 4-bit floor
#     needed group compensation — raw q4_0 KV has none).
#  P3 K-IS-MORE-FRAGILE-THAN-V: at equal bits, quantizing ONLY keys hurts more
#     than quantizing ONLY values (K errors shift the softmax selection
#     boundary and are amplified; V errors are linear content noise — the
#     NET-83 super-additivity mechanism predicts asymmetry).
#
# Arms: {K16/V16 control, K8/V16, K16/V8, K8/V8, K4/V4} @ ctx 2048, threads 8,
# corpus = held-out wikitext slice (~250KB) from the durable net49 cache.
import json, os, re, subprocess, time

BIN = os.path.expanduser("~/f3cache/llama.cpp/build/bin/llama-perplexity")
MODEL = os.path.expanduser("~/f3cache/gguf/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf")
SRC = os.path.expanduser("~/f3cache/net49_corpus.txt")
CORPUS = "/tmp/net92_wiki_slice.txt"
CTX = 2048
THREADS = "8"
SLICE_BYTES = 250_000
RESULTS = os.path.expanduser("~/f3cache/net92_results.json")

ARMS = [("f16", "f16"), ("q8_0", "f16"), ("f16", "q8_0"), ("q8_0", "q8_0"), ("q4_0", "q4_0")]

text = open(SRC, encoding="utf-8", errors="ignore").read()
head = open(CORPUS, "w", encoding="utf-8")
head.write(text[400_000:400_000 + SLICE_BYTES])   # offset slice, disjoint from eval windows used elsewhere
head.close()
print(f"corpus slice: {os.path.getsize(CORPUS)} bytes", flush=True)

res = {"meta": {"model": MODEL, "ctx": CTX, "threads": THREADS,
                "corpus_bytes": SLICE_BYTES,
                "predictions": "P1 q8_0kv dPPL<1%; P2 q4_0kv dPPL>5%; "
                               "P3 K-only worse than V-only at equal bits"},
       "arms": []}

for i, (kt, vt) in enumerate(ARMS):
    t0 = time.time()
    p = subprocess.run([BIN, "-m", MODEL, "-f", CORPUS, "-c", str(CTX),
                        "-t", THREADS, "--cache-type-k", kt,
                        "--cache-type-v", vt], capture_output=True, text=True,
                       timeout=5400)
    out = p.stdout + p.stderr
    m = re.search(r"Final estimate: PPL\s*=\s*([0-9.]+)", out)
    if m:
        ppl = float(m.group(1))
    else:
        chunks = re.findall(r"\[\d+\]([0-9.]+),", out)   # [N]ppl, stream
        ppl = float(chunks[-1]) if chunks else None
    entry = {"arm": f"K{kt}/V{vt}", "ppl": ppl, "wall_s": round(time.time() - t0, 1)}
    res["arms"].append(entry)
    json.dump(res, open(RESULTS, "w"), indent=1)
    print(f"arm K{kt}/V{vt}: ppl={ppl} ({entry['wall_s']}s)", flush=True)

base = next((a["ppl"] for a in res["arms"] if a["arm"] == "Kf16/Vf16" and a["ppl"]), None)
if base:
    for a in res["arms"]:
        if a["ppl"]:
            a["d_pct"] = round(100.0 * (a["ppl"] - base) / base, 3)
    json.dump(res, open(RESULTS, "w"), indent=1)
    print("\n=== VERDICTS ===", flush=True)
    for a in res["arms"]:
        print(f"{a['arm']}: ppl={a['ppl']} dPPL={a.get('d_pct')}%", flush=True)
print("ALL_DONE_NET92", flush=True)

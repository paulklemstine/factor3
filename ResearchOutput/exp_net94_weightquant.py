#!/usr/bin/env python3
# NET-94 — THE WEIGHT-QUANT LADDER AT 7B: DOES THE FLOOR SURVIVE SCALE?
# (cpu-large-model axis, iteration 69)
#
# NET-52/53 established at toy scale that raw sub-6-bit weights are not
# deployable and group-128 repair recovers only part of the damage; NET-84/85
# put the tail layers' precision need at 8 bits. This round tests whether
# those floor structures survive at 14x scale using llama.cpp's CALIBRATED
# k-quants (a stronger quantizer than the toy RTN — so this is a transfer
# test of the floor POSITIONS, not of RTN pathology).
#
# Control: fp16 (the honest anchor). All deltas reported vs fp16 AND vs q8_0
# (the practical-lossless proxy used when fp16 is unavailable elsewhere).
#
# PREDICTIONS STATED BEFORE ANY MEASUREMENT:
#  P1 SIX-BIT-PAST-EVERY-FLOOR: q6_k lands within +-0.5% of fp16 (6 bits
#     clears every floor measured anywhere in the program).
#  P2 THREE-BIT-DISCRIMINATOR: q3_k_m dPPL vs fp16 is between +5% and +30%
#     — scale buys partial rescue below the toy 6-bit floor but does NOT
#     reach losslessness (competing horn "scale erases floors entirely"
#     predicts <2%; refuting it is the point).
#  P3 TWO-BIT-STAYS-UNUSABLE: q2_k dPPL exceeds +50% even at 14x scale —
#     the floor never vanishes with scale, it only moves.
import json, os, re, subprocess, time

BIN = os.path.expanduser("~/f3cache/llama.cpp/build/bin/llama-perplexity")
GG = os.path.expanduser("~/f3cache/gguf")
SRC = os.path.expanduser("~/f3cache/net49_corpus.txt")
CORPUS = "/tmp/net94_slice.txt"
CTX, THREADS, SLICE_BYTES = 2048, "8", 250_000
RESULTS = os.path.expanduser("~/f3cache/net94_results.json")

ARMS = [
    ("fp16", os.path.join(GG, "qwen2.5-7b-instruct-fp16-00001-of-00004.gguf")),
    ("q8_0", os.path.join(GG, "qwen2.5-7b-instruct-q8_0-00001-of-00003.gguf")),
    ("q6_k", os.path.join(GG, "qwen2.5-7b-instruct-q6_k.gguf")),
    ("q5_k_m", os.path.join(GG, "qwen2.5-7b-instruct-q5_k_m.gguf")),
    ("q4_k_m", os.path.join(GG, "qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf")),
    ("q3_k_m", os.path.join(GG, "qwen2.5-7b-instruct-q3_k_m.gguf")),
    ("q2_k", os.path.join(GG, "qwen2.5-7b-instruct-q2_k.gguf")),
]

text = open(SRC, encoding="utf-8", errors="ignore").read()
open(CORPUS, "w", encoding="utf-8").write(text[400_000:400_000 + SLICE_BYTES])
print(f"corpus slice: {os.path.getsize(CORPUS)} bytes", flush=True)

res = {"meta": {"ctx": CTX, "corpus_bytes": SLICE_BYTES,
                "predictions": "P1 q6_k within +-0.5% of fp16; "
                               "P2 q3_k_m dPPL in [+5%,+30%] (scale partially "
                               "rescues, does not erase); "
                               "P3 q2_k dPPL > +50%"},
       "arms": []}

for name, path in ARMS:
    if not os.path.exists(path):
        print(f"SKIP {name}: missing {path}", flush=True)
        res["arms"].append({"arm": name, "ppl": None, "missing": True})
        continue
    t0 = time.time()
    p = subprocess.run([BIN, "-m", path, "-f", CORPUS, "-c", str(CTX),
                        "-t", THREADS], capture_output=True, text=True,
                       timeout=7200)
    out = p.stdout + p.stderr
    m = re.search(r"Final estimate: PPL\s*=\s*([0-9.]+)", out)
    ppl = float(m.group(1)) if m else None
    entry = {"arm": name, "ppl": ppl, "wall_s": round(time.time() - t0, 1)}
    res["arms"].append(entry)
    json.dump(res, open(RESULTS, "w"), indent=1)
    print(f"arm {name}: ppl={ppl} ({entry['wall_s']}s)", flush=True)

fp16 = next((a["ppl"] for a in res["arms"] if a["arm"] == "fp16" and a["ppl"]), None)
for a in res["arms"]:
    if a["ppl"] and fp16:
        a["d_vs_fp16_pct"] = round(100.0 * (a["ppl"] - fp16) / fp16, 3)
json.dump(res, open(RESULTS, "w"), indent=1)
print("\n=== VERDICTS ===", flush=True)
for a in res["arms"]:
    print(f"{a['arm']}: ppl={a['ppl']} dPPL={a.get('d_vs_fp16_pct')}%", flush=True)
print("ALL_DONE_NET94", flush=True)

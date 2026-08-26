#!/usr/bin/env python3
# NET-103b — BENCH REDO WITH RAW CAPTURE + IK PPL REGEX FIX
# (completes NET-103 after two instrumentation bugs: empty-table parse,
#  and ik's "Final estimate: PPL over N chunks ... =" wording)
# Raw llama-bench outputs are dumped verbatim; parsing happens offline.
import json, os, re, subprocess

MAIN = os.path.expanduser("~/f3cache/llama.cpp/build/bin")
IK = os.path.expanduser("~/f3cache/llama.cpp-ik/build/bin")
GG = os.path.expanduser("~/f3cache/gguf")
G30DIR = os.path.expanduser("~/f3cache/gguf30b")
M7B = os.path.join(GG, "qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf")
M30 = os.path.join(G30DIR, "Qwen3-30B-A3B-IQ4_XS.gguf")
Q8 = os.path.join(GG, "qwen2.5-7b-instruct-q8_0-00001-of-00003.gguf")
SLICE = "/tmp/net103_slice.txt"
RESULTS = os.path.expanduser("~/f3cache/net103b_results.json")

res = {"bench_raw": {}, "ppl_ik_7bq8": None}
def save(): json.dump(res, open(RESULTS, "w"), indent=1)
def log(m):
    print(m, flush=True); open("/tmp/net103b.log", "a").write(str(m) + "\n")

for label, bdir, model in [
        ("dense7b_mainline", MAIN, M7B),
        ("dense7b_ik", IK, M7B),
        ("moe30b_mainline", MAIN, M30),
        ("moe30b_ik", IK, M30)]:
    p = subprocess.run([os.path.join(bdir, "llama-bench"), "-m", model,
                        "-t", "8", "-p", "512", "-n", "128"],
                       capture_output=True, text=True, timeout=7200)
    res["bench_raw"][label] = {"stdout": p.stdout[-4000:], "stderr_tail": p.stderr[-2000:]}
    save()
    log(f"bench {label}: captured {len(p.stdout)} bytes")

p = subprocess.run([os.path.join(IK, "llama-perplexity"), "-m", Q8,
                    "-f", SLICE, "-c", "2048", "-t", "8"],
                   capture_output=True, text=True, timeout=14400)
o = p.stdout + p.stderr
m = re.search(r"Final estimate: PPL[^=]*=\s*([0-9.]+)", o)
res["ppl_ik_7bq8"] = float(m.group(1)) if m else None
save()
log(f"ik ppl (fixed regex): {res['ppl_ik_7bq8']}  [mainline anchor: 6.9781]")
log("ALL_DONE_NET103B")

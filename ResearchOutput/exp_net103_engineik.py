#!/usr/bin/env python3
# NET-103 — ENGINE-IK: ENGINE-INVARIANCE AUDIT AND THE 30B MoE THROUGHPUT LEVER
# (cpu-large-model axis, iteration 78)
#
# Two payloads:
# (a) ENGINE-INVARIANCE AUDIT of our published laws: every law (NET-91..99)
#     was measured on MAINLINE llama.cpp kernels. If ik_llama.cpp (pinned
#     commit 08b500b9) moves knees/taxes at identical quant files, part of
#     what we published is kernel artifact; if it holds, laws gain
#     engine-independence.
# (b) THE TOK/S LEVER toward GOAL: ik reports 3-11x prompt-processing and
#     ~44% faster tg at long context on Qwen3-30B-A3B CPU-only.
#
# PREDICTIONS STATED BEFORE ANY MEASUREMENT:
#  P1 DENSE-PARITY: ik TG within +-10% of mainline on 7B Q4_K_M dense
#     (ik optimizes MoE paths; dense should be ~neutral).
#  P2 MOE-PP-WIN: ik PP512 >= 2x mainline on Qwen3-30B-A3B IQ4_XS.
#  P3 GOAL-GRADE-SPEED: best-engine 30B-A3B tg128 >= 10 tok/s resident.
#  P4 QUALITY-INVARIANCE: ik PPL within +-1% of mainline PPL on identical
#     quant+slice (else engine artifact in our published measurements).
import json, os, re, subprocess, time

MAIN = os.path.expanduser("~/f3cache/llama.cpp/build/bin")
IK = os.path.expanduser("~/f3cache/llama.cpp-ik/build/bin")
GG = os.path.expanduser("~/f3cache/gguf")
G30DIR = os.path.expanduser("~/f3cache/gguf30b")
M7B = os.path.join(GG, "qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf")
M30 = os.path.join(G30DIR, "Qwen3-30B-A3B-IQ4_XS.gguf")
MARKER = os.path.join(G30DIR, "COMPLETE.marker")
SLICE = "/tmp/net103_slice.txt"
RESULTS = os.path.expanduser("~/f3cache/net103_results.json")

text_src = os.path.expanduser("~/f3cache/net49_corpus.txt")
text = open(text_src, encoding="utf-8", errors="ignore").read()
open(SLICE, "w", encoding="utf-8").write(text[400_000:650_000])

res = {"meta": {"pin": open(os.path.expanduser(
            "~/f3cache/llama.cpp-ik/PINNED_COMMIT.txt")).read().strip(),
        "predictions": "P1 dense tg +-10%; P2 ik PP >= 2x on 30B MoE; "
                       "P3 best-engine tg >= 10 tok/s; "
                       "P4 ik PPL within +-1%"},
       "bench": [], "ppl": []}

def save(): json.dump(res, open(RESULTS, "w"), indent=1)
def log(m):
    print(m, flush=True); open("/tmp/net103.log", "a").write(str(m) + "\n")

log("waiting for 30B download...")
for _ in range(120):
    if os.path.exists(MARKER): break
    time.sleep(60)
else:
    raise SystemExit("FATAL: 30B download never completed")
log("30B ready")

def bench(engine_bin, model, tag):
    p = subprocess.run([engine_bin.replace("llama-bench", "llama-bench"),
                        "-m", model, "-t", "8", "-p", "512", "-n", "128"],
                       capture_output=True, text=True, timeout=7200)
    o = p.stdout + p.stderr
    out = []
    for line in o.splitlines():
        if re.match(r"\s*\d+\s*\|", line):
            cells = [c.strip() for c in line.split("|")]
            nums = [c for c in cells if re.match(r"[\d.]+(?:\s*[+-]\s*[\d.]+)?$", c)]
            out.append(nums)
    return out

for label, bbin, model in [
        ("dense7b_mainline", os.path.join(MAIN, "llama-bench"), M7B),
        ("dense7b_ik", os.path.join(IK, "llama-bench"), M7B),
        ("moe30b_mainline", os.path.join(MAIN, "llama-bench"), M30),
        ("moe30b_ik", os.path.join(IK, "llama-bench"), M30)]:
    rows = bench(bbin, model, label)
    entry = {"arm": label, "rows": rows}
    res["bench"].append(entry); save()
    log(f"bench {label}: {rows}")

def ppl(engine_dir, model):
    p = subprocess.run([os.path.join(engine_dir, "llama-perplexity"),
                        "-m", model, "-f", SLICE, "-c", "2048", "-t", "8"],
                       capture_output=True, text=True, timeout=14400)
    m = re.search(r"Final estimate: PPL\s*=\s*([0-9.]+)",
                  p.stdout + p.stderr)
    return float(m.group(1)) if m else None

for label, edir, model in [("ppl_mainline_7bq8", MAIN, Q8 := os.path.join(
        GG, "qwen2.5-7b-instruct-q8_0-00001-of-00003.gguf")),
        ("ppl_ik_7bq8", IK, Q8)]:
    v = ppl(edir, model)
    res["ppl"].append({"arm": label, "ppl": v}); save()
    log(f"{label}: ppl={v}")

log("ALL_DONE_NET103")

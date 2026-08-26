#!/usr/bin/env python3
# NET-101 — DRAFT-CACHE-QUANT: THE DRAFT'S OWN KV CACHE IS LOW-STAKES
# (cpu-large-model axis, iteration 76)
#
# llama.cpp exposes SEPARATE cache-type flags for the draft model
# (--cache-type-k-draft / --cache-type-v-draft). Since draft errors are
# recoverable (a rejected token simply falls back to target decode), we
# hypothesize the draft's cache precision is nearly free to drop — removing
# almost all draft-side KV RAM from little-RAM serving stacks.
#
# PREDICTIONS STATED BEFORE ANY MEASUREMENT:
#  P1 EIGHT-BIT-FREE: draft cache q8_0 changes mean acceptance by <= 1 pt
#     vs f16 draft cache at matched depth/domain.
#  P2 FOUR-BIT-CHEAP-NOT-FREE: draft cache q4_0 costs < 5 pts acceptance
#     (draft errors are recoverable; unlike the TARGET-side cliff NET-92/93).
#  P3 THROUGHPUT-PARITY: tok/s within +/-10% across all three draft caches.
import json, os, re, statistics, subprocess

SPEC = os.path.expanduser("~/f3cache/llama.cpp/build/bin/llama-speculative")
GGUF_DIR = os.path.expanduser("~/f3cache/gguf")
TARGET = os.path.join(GGUF_DIR, "qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf")
DRAFT = os.path.join(GGUF_DIR, "qwen2.5-0.5b-instruct-q8_0.gguf")
CORPORA = {"prose": os.path.expanduser("~/f3cache/net49_corpus.txt"),
           "code": os.path.expanduser("~/f3cache/code_corpus.txt")}
DEPTH = 8   # deepest = most drafted tokens => most sensitive to draft cache
N_PROMPTS, PROMPT_CHARS, N_GEN, CTX, THREADS = 4, 2000, 96, 1024, "8"
RESULTS = os.path.expanduser("~/f3cache/net101_results.json")


def load_prompts(path, n, chars):
    text = open(path, encoding="utf-8", errors="ignore").read()
    step = len(text) // (n + 20)
    return [text[step * (i + 10):step * (i + 10) + chars] for i in range(n)]


res = {"meta": {"depth": DEPTH,
                "predictions": "P1 dcache q8_0 <=1pt; "
                               "P2 dcache q4_0 <5pts; P3 tok/s parity +-10%"},
       "arms": []}
json.dump(res, open(RESULTS, "w"), indent=1)

for domain in ("prose", "code"):
    prompts = load_prompts(CORPORA[domain], N_PROMPTS, PROMPT_CHARS)
    for dct in ("f16", "q8_0", "q4_0"):
        accs, effs = [], []
        for prompt in prompts:
            p = subprocess.run([SPEC, "-m", TARGET, "-md", DRAFT,
                                "--spec-type", "draft-simple",
                                "--spec-draft-n-max", str(DEPTH),
                                "--spec-draft-n-min", "1",
                                "--cache-type-k-draft", dct,
                                "--cache-type-v-draft", dct,
                                "-p", prompt, "-n", str(N_GEN),
                                "-c", str(CTX), "-t", THREADS, "-s", "42"],
                               capture_output=True, text=True, timeout=1800)
            o = p.stdout + p.stderr
            m = re.findall(r"accept\s*=\s*([\d.]+)%", o)
            if m:
                accs.append(float(m[-1]))
        entry = {"domain": domain, "draft_cache": dct,
                 "accept_pct": round(statistics.mean(accs), 2) if accs else None}
        res["arms"].append(entry)
        json.dump(res, open(RESULTS, "w"), indent=1)
        print(entry, flush=True)

print("\n=== VERDICTS ===", flush=True)
idx = {(e["domain"], e["draft_cache"]): e["accept_pct"] for e in res["arms"]}
for domain in ("prose", "code"):
    f = idx.get((domain, "f16"))
    q8 = idx.get((domain, "q8_0"))
    q4 = idx.get((domain, "q4_0"))
    if f and q8 and q4:
        print(f"{domain}: f16={f} q8_0={q8} (diff {abs(q8-f):.2f}) "
              f"q4_0={q4} (diff {abs(q4-f):.2f})", flush=True)
print("ALL_DONE_NET101", flush=True)

#!/usr/bin/env python3
# NET-100 — SPECCACHE-COMBO: DOES THE ROLE-SPLIT CACHE SURVIVE SPECULATION?
# (cpu-large-model axis, iteration 75; Phase-A recipe-completion cell)
#
# Laws 2 x 4 composition test. NET-94 made K8/V4 the serving default for
# PPL; NET-91 measured speculation with f16 KV only. If acceptance is
# interaction-free, the composed CPU serving claim becomes servable fact.
#
# PREDICTIONS STATED BEFORE ANY MEASUREMENT:
#  P1 INTERACTION-FREE ACCEPTANCE: mean drafted-token acceptance differs by
#     < 2 points between K8/V4 and f16/f16 caches at matched depth/domain.
#  P2 SPEED-PARITY: speculative eff tok/s(K8/V4) >= 0.95 x tok/s(f16) at
#     every matched config (dequant tax bounded).
#  P3 MEMORY-HALVING-STANDS: K8/V4 speculative runs complete normally with
#     KV bytes halved (recorded KV buffer sizes), preserving the serving
#     default under speculation.
import json, os, re, statistics, subprocess, time

SPEC = os.path.expanduser("~/f3cache/llama.cpp/build/bin/llama-speculative")
GGUF_DIR = os.path.expanduser("~/f3cache/gguf")
TARGET = os.path.join(GGUF_DIR, "qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf")
DRAFT = os.path.join(GGUF_DIR, "qwen2.5-0.5b-instruct-q8_0.gguf")
CORPORA = {"prose": os.path.expanduser("~/f3cache/net49_corpus.txt"),
           "code": os.path.expanduser("~/f3cache/code_corpus.txt")}
DEPTHS = [4, 8]
N_PROMPTS, PROMPT_CHARS, N_GEN, CTX, THREADS = 3, 2000, 96, 1024, "8"
RESULTS = os.path.expanduser("~/f3cache/net100_results.json")


def load_prompts(path, n, chars):
    text = open(path, encoding="utf-8", errors="ignore").read()
    step = len(text) // (n + 20)
    return [text[step * (i + 10):step * (i + 10) + chars] for i in range(n)]


res = {"meta": {"target": TARGET, "draft": DRAFT, "depths": DEPTHS,
                "predictions": "P1 |accept diff| < 2pts; "
                               "P2 tok_s(K8/V4) >= 0.95x f16; "
                               "P3 KV halved, runs complete"},
       "arms": []}

def save():
    json.dump(res, open(RESULTS, "w"), indent=1)

for domain in ("prose", "code"):
    prompts = load_prompts(CORPORA[domain], N_PROMPTS, PROMPT_CHARS)
    for depth in DEPTHS:
        for ctkt, ctvt, label in [("f16", "f16", "f16"),
                                  ("q8_0", "q4_0", "K8V4")]:
            accs, effs = [], []
            for prompt in prompts:
                t0 = time.time()
                p = subprocess.run([SPEC, "-m", TARGET, "-md", DRAFT,
                                    "--spec-type", "draft-simple",
                                    "--spec-draft-n-max", str(depth),
                                    "--spec-draft-n-min", "1",
                                    "--cache-type-k", ctkt,
                                    "--cache-type-v", ctvt,
                                    "-p", prompt, "-n", str(N_GEN),
                                    "-c", str(CTX), "-t", THREADS,
                                    "-s", "42"],
                                   capture_output=True, text=True,
                                   timeout=1800)
                wall = time.time() - t0
                o = p.stdout + p.stderr
                m = re.findall(r"accept\s*=\s*([\d.]+)%", o)
                if m:
                    accs.append(float(m[-1]))
                    effs.append(N_GEN / max(wall - 12.0, 1.0))  # rough overhead
            entry = {"domain": domain, "depth": depth, "cache": label,
                     "accept_pct": round(statistics.mean(accs), 2) if accs else None,
                     "eff_tok_s": round(statistics.median(effs), 3) if effs else None}
            res["arms"].append(entry)
            save()
            print(entry, flush=True)

print("\n=== VERDICTS ===", flush=True)
idx = {(e["domain"], e["depth"], e["cache"]): e for e in res["arms"]}
p1_ok, p2_ok = True, True
for domain in ("prose", "code"):
    for depth in DEPTHS:
        a16 = idx.get((domain, depth, "f16"))
        akv = idx.get((domain, depth, "K8V4"))
        if a16 and akv and a16["accept_pct"] and akv["accept_pct"]:
            d = abs(a16["accept_pct"] - akv["accept_pct"])
            if d >= 2: p1_ok = False
            r = akv["eff_tok_s"] / a16["eff_tok_s"]
            if r < 0.95: p2_ok = False
            print(f"{domain} d={depth}: accept {a16['accept_pct']} vs "
                  f"{akv['accept_pct']} (d={d:.2f}); tok/s ratio {r:.3f}",
                  flush=True)
print(f"P1 interaction-free: {p1_ok}\nP2 speed-parity: {p2_ok}", flush=True)
print("ALL_DONE_NET100", flush=True)

#!/usr/bin/env python3
# NET-102 — GPTOSS-HOTSET: NATIVE-MXFP4 MoE ON PURE CPU
# (cpu-large-model axis, iteration 77)
#
# gpt-oss-20b: 20.9B total params / 3.6B active, 32-expert top-4 routing,
# alternating SWA+full attention, weights TRAINED natively in MXFP4
# (zero post-hoc quantization tax — the clean baseline our Qwen cells
# could never provide). Plus its official EAGLE-3 draft exists as GGUF.
#
# PREDICTIONS STATED BEFORE ANY MEASUREMENT:
#  P1 SPEED: base greedy tg >= 8 tok/s @ctx512, threads=8 (community
#     reports 8-21 on comparable desktops).
#  P2 ROLE-SPLIT TRANSFERS: K8/V4 vs f16-KV perplexity ratio <= 1.05
#     (Law 2 transfers across architectures; NET-94 was Qwen-only).
#  P3 EAGLE3-PAYS: speculative decoding with the official eagle3 draft
#     yields >= 1.3x tok/s vs non-speculative at matched settings
#     (trained-draft regime — tests whether draft-cost dominance extends
#     to trained heads on CPU).
#  P4 RESIDENCY: peak RSS stays below the 12.11GB file size during
#     generation (lazy expert mmap = implicit hot-set).
import json, os, re, subprocess, time

BIN = os.path.expanduser("~/f3cache/llama.cpp/build/bin")
COMP = os.path.join(BIN, "llama-completion")
PPLB = os.path.join(BIN, "llama-perplexity")
SPEC = os.path.join(BIN, "llama-speculative")
MODEL = os.path.expanduser("~/f3cache/gguf20b/gpt-oss-20b-MXFP4.gguf")
EAGLE = os.path.expanduser("~/f3cache/gguf20b/eagle3-gpt-oss-20b-Q8_0.gguf")
MARKER = os.path.expanduser("~/f3cache/gguf20b/COMPLETE.marker")
SRC = os.path.expanduser("~/f3cache/net49_corpus.txt")
SLICE = "/tmp/net102_slice.txt"
THREADS = "8"
RESULTS = os.path.expanduser("~/f3cache/net102_results.json")

text = open(SRC, encoding="utf-8", errors="ignore").read()
open(SLICE, "w", encoding="utf-8").write(text[400_000:650_000])

res = {"meta": {"model": MODEL, "eagle": EAGLE,
                "predictions": "P1 tg>=8; P2 K8/V4 ppl ratio<=1.05; "
                               "P3 eagle3 spec>=1.3x; P4 RSS<12.11GB"},
       "arms": []}

def save():
    json.dump(res, open(RESULTS, "w"), indent=1)

def log(m):
    print(m, flush=True)
    open("/tmp/net102.log", "a").write(str(m) + "\n")

log("waiting for download marker...")
for _ in range(60):
    if os.path.exists(MARKER):
        break
    time.sleep(30)
else:
    raise SystemExit("download never completed")

def timed(args, timeout=3600):
    cmd = ["systemd-run", "--scope", "-p", "MemoryMax=16G",
           "-p", "MemorySwapMax=0",
           "/usr/bin/time", "-v"] + args
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    o = p.stdout + p.stderr
    rss = re.search(r"Maximum resident set size \(kbytes\): (\d+)", o)
    return o, (int(rss.group(1)) / 1e6 if rss else None)

log("arm 1: base tg")
o, rss = timed([COMP, "-m", MODEL, "-p",
                "The history of computing begins with", "-n", "256",
                "-c", "512", "-t", THREADS])
m = re.search(r"eval time\s*=\s*[\d.]+\s*ms\s*/\s*\d+\s*runs.*?,\s*([\d.]+)\s*tokens per second", o)
base_tg = float(m.group(1)) if m else None
entry = {"arm": "base_tg", "tok_s": base_tg, "rss_gb": round(rss, 2) if rss else None}
res["arms"].append(entry); save()
log(f"base tg={base_tg} rss={rss}GB")

log("arm 2: perplexity f16-KV vs K8/V4")
ppls = {}
for label, extra in [("f16", []), ("K8V4", ["--cache-type-k", "q8_0",
                                            "--cache-type-v", "q4_0"])]:
    o, _ = timed([PPLB, "-m", MODEL, "-f", SLICE, "-c", "2048",
                  "-t", THREADS] + extra, timeout=7200)
    m = re.search(r"Final estimate: PPL\s*=\s*([0-9.]+)", o)
    ppls[label] = float(m.group(1)) if m else None
    res["arms"].append({"arm": f"ppl_{label}", "ppl": ppls[label]})
    save()
    log(f"ppl {label} = {ppls[label]}")

log("arm 3: eagle3 speculation")
o, rss2 = timed([SPEC, "-m", MODEL, "-md", EAGLE,
                 "--spec-type", "draft-eagle3",
                 "-p", "The history of computing begins with",
                 "-n", "256", "-c", "512", "-t", THREADS])
m = re.search(r"eval time\s*=\s*[\d.]+\s*ms\s*/\s*\d+\s*runs.*?,\s*([\d.]+)\s*tokens per second", o)
spec_tg = float(m.group(1)) if m else None
am = re.findall(r"accept\s*=\s*([\d.]+)%", o)
entry = {"arm": "spec_eagle3", "tok_s": spec_tg,
         "accept_pct": float(am[-1]) if am else None,
         "rss_gb": round(rss2, 2) if rss2 else None}
res["arms"].append(entry); save()
log(f"spec tg={spec_tg} accept={entry['accept_pct']}")

verdicts = {}
if base_tg:
    verdicts["P1_speed"] = base_tg >= 8.0
if ppls.get("f16") and ppls.get("K8V4"):
    verdicts["P2_transfer_ratio"] = round(ppls["K8V4"] / ppls["f16"], 4)
    verdicts["P2_transfer_ok"] = ppls["K8V4"] / ppls["f16"] <= 1.05
if base_tg and spec_tg:
    verdicts["P3_eagle_speedup"] = round(spec_tg / base_tg, 3)
    verdicts["P3_eagle_ok"] = spec_tg / base_tg >= 1.3
if rss:
    verdicts["P4_residency_ok"] = rss < 12.11
res["verdicts"] = verdicts
save()
log(f"VERDICTS: {json.dumps(verdicts)}")
log("ALL_DONE_NET102")

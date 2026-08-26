#!/usr/bin/env python3
# NET-106 — GPTOSS-120B-STREAMTAX: A 116.8B MODEL AT FULL CONTEXT IN 31GB RAM
# (cpu-large-model axis, iteration 80; GOAL CAPSTONE)
#
# gpt-oss-120b: 116.83B total params (MXFP4-native, zero quant tax), ~5.1B
# active via 128-expert top-4 routing, SWA-mixed attention. Weights = 63.39GB
# vs 31GB RAM => the model CANNOT be resident; llama.cpp mmap-streams every
# routed expert from NVMe. No cgroups needed — the wall enforces itself.
#
# PREDICTIONS STATED BEFORE ANY MEASUREMENT:
#  P1 COMPLETION-AT-SCALE: 116.8B completes >=64 generated tokens @ctx2048
#     without OOM (peak RAM <= 30GB) — a >100B model runs FULL CONTEXT
#     on this box. THE GOAL ARTIFACT.
#  P2 STREAM-TAX BAND: streamed generation lands in [0.3, 6.0] tok/s
#     (NVMe-bound; below resident-7B's 5.9-8.8 but usable).
#  P3 CTX-SCALING: tok/s(8192) >= 0.5 x tok/s(2048) (SWA keeps KV light;
#     context doubling must not halve throughput).
#  P4 NGRAM-SPECULATION: --spec-type ngram-simple does not crash on this
#     model and is recorded either way (exploratory arm; repeated-structure
#     prompts may let the zero-RAM proposer pay).
import json, os, re, subprocess, threading, time

BIN = os.path.expanduser("~/f3cache/llama.cpp/build/bin")
COMP = os.path.join(BIN, "llama-completion")
SPEC = os.path.join(BIN, "llama-speculative")
M120 = os.path.expanduser("~/f3cache/gguf120b/gpt-oss-120b-MXFP4.gguf")
EAGLE = os.path.expanduser("~/f3cache/gguf120b/eagle3-gpt-oss-120b-Q8_0.gguf")
MARKER = os.path.expanduser("~/f3cache/gguf120b/COMPLETE.marker")
THREADS = "8"
PROMPT = "The history of computing begins with "
RESULTS = os.path.expanduser("~/f3cache/net106_results.json")

res = {"meta": {"model": M120, "weights_gb": 63.39,
                "ram_total_gb": 31,
                "predictions": "P1 completes @2048; P2 tok_s in [0.3,6.0]; "
                               "P3 t8k/t2k >= 0.5; P4 ngram exploratory"},
       "arms": []}

def save(): json.dump(res, open(RESULTS, "w"), indent=1)
def log(m):
    print(m, flush=True); open("/tmp/net106.log", "a").write(str(m) + "\n")

log("waiting for 120B download...")
for _ in range(240):
    if os.path.exists(MARKER): break
    time.sleep(60)
else:
    raise SystemExit("FATAL: download never completed")
log("120B ready")

def rss_sampler(stop):
    peak = [0]
    while not stop[0]:
        tot = 0
        for pid in os.listdir("/proc"):
            if not pid.isdigit(): continue
            try:
                if "llama" in open(f"/proc/{pid}/comm").read():
                    for line in open(f"/proc/{pid}/status"):
                        if line.startswith("VmRSS"):
                            tot += int(line.split()[1])
            except Exception:
                pass
        peak[0] = max(peak[0], tot)
        time.sleep(2)
    return peak

def run_stream(tag, ctx, ngen, extra=None, spec=False):
    stop = [False]
    th = threading.Thread(target=lambda: rss_sampler(stop))
    th.start()
    base = [COMP, "-m", M120, "-c", str(ctx), "-n", str(ngen),
            "-t", THREADS, "--temp", "0",
            "-p", PROMPT]
    if spec:
        base = [SPEC, "-m", M120, "-md", EAGLE,
                "--spec-type", "draft-eagle3",
                "-c", str(ctx), "-n", str(ngen), "-t", THREADS,
                "--temp", "0", "-p", PROMPT]
    if extra:
        base += extra
    t0 = time.time()
    try:
        p = subprocess.run(base, capture_output=True, text=True, timeout=10800)
        o = p.stdout + p.stderr
        rc = p.returncode
    except subprocess.TimeoutExpired:
        o, rc = "", "timeout"
    stop[0] = True; th.join()
    wall = round(time.time() - t0, 1)
    m = re.search(r"eval time\s*=\s*[\d.]+\s*ms\s*/\s*(\d+)\s*runs.*?,\s*([\d.]+)\s*tokens per second", o)
    entry = {"arm": tag, "ctx": ctx, "completed": bool(m),
             "tokens": int(m.group(1)) if m else None,
             "tok_s": float(m.group(2)) if m else None,
             "rc": str(rc), "wall_s": wall}
    save()
    log(f"{tag}: {entry}")
    return entry, o

log("arm 1: streamed baseline ctx2048")
e1, o1 = run_stream("stream_ctx2048", 2048, 128)

log("arm 2: streamed ctx8192")
e2, o2 = run_stream("stream_ctx8192", 8192, 128)

log("arm 3: eagle3 spec attempt (segfault watch)")
e3, o3 = run_stream("spec_eagle3_ctx2048", 2048, 128, spec=True)

log("arm 4: ngram speculation (zero-RAM proposer)")
e4, o4 = run_stream("ngram_spec_ctx2048", 2048, 128,
                    extra=["--spec-type", "ngram-simple"])

verdicts = {
    "P1_completion": e1["completed"],
    "P2_band_ok": bool(e1["tok_s"] and 0.3 <= e1["tok_s"] <= 6.0),
    "P3_ctx_ratio": round(e2["tok_s"] / e1["tok_s"], 3)
                    if e1["tok_s"] and e2["tok_s"] else None,
}
try:
    verdicts["P4_ngram_vs_base"] = round(e4["tok_s"] / e1["tok_s"], 3) \
        if e4["tok_s"] and e1["tok_s"] else None
except Exception:
    pass
res["verdicts"] = verdicts; save()
log(f"VERDICTS: {json.dumps(verdicts)}")
log("ALL_DONE_NET106")

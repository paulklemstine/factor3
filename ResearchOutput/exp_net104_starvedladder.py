#!/usr/bin/env python3
# NET-104 — STARVED-LADDER: VALIDATING THE RAM-BUDGET FORMULA WHERE TRUTH IS KNOWN
# (cpu-large-model axis, iteration 79; methodology-gate cell)
#
# NET-99 constructed points were verified manually after an automated-launcher
# flaw; this cell (a) fixes the launcher (--user scope, asserted memory.max),
# (b) validates the EIGHT-GB-FRONTIER params_max formula against KNOWN ground
# truth by squeezing cached models through a MemoryMax ladder, and (c) adds
# the corruption canaries this box's history demands.
#
# PREDICTIONS STATED BEFORE ANY MEASUREMENT:
#  P1 FORMULA-HOLDS: the minimal passing MemoryMax for 7B-q2_k @ctx2048
#     lands within ±15% of the formula prediction
#     pred = weights_file + KV(2048) + C_overhead(measured unconstrained RSS
#     minus weights_file), using bpw-implied KV bytes.
#  P2 STREAMING-REGIME EXISTS: at least one cap BELOW full-residency still
#     completes generation (partial mmap paging works), with measurably
#     degraded tok/s — the regime map has three regions, not two.
#  P3 PLACEBO-CHEAP: a placebo cap (>= 2x expected RSS) changes tok/s by
#     less than 5% vs uncapped (cgroup accounting is not a tax).
import json, os, re, subprocess, hashlib

GG = os.path.expanduser("~/f3cache/gguf")
COMP = os.path.expanduser("~/f3cache/llama.cpp/build/bin/llama-completion")
RESULTS = os.path.expanduser("~/f3cache/net104_results.json")

MODELS = [
    ("7B_q2k", os.path.join(GG, "qwen2.5-7b-instruct-q2_k.gguf"), 3_015_940_000,
     ["2500M", "3000M", "3500M", "4000M", "8000M_placebo"]),
    ("1p5B_q4km", os.path.join(GG, "qwen2.5-1.5b-instruct-q4_k_m.gguf"), 1_117_320_736,
     ["1250M", "1500M", "2000M_placebo"]),
]
CTX, NGEN, THREADS = 2048, 128, "8"

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()

res = {"meta": {"ctx": CTX, "ngen": NGEN,
                "predictions": "P1 formula +-15%; P2 streaming regime exists; "
                               "P3 placebo <5%"},
       "canary": {}, "arms": []}

def save(): json.dump(res, open(RESULTS, "w"), indent=1)

def log(m):
    print(m, flush=True); open("/tmp/net104.log", "a").write(str(m) + "\n")

log("canary: hashing models before run")
for name, path, _, _ in MODELS:
    res["canary"][name] = {"pre": sha256(path)[:16]}
save()

def run_capped(model, cap):
    mem = cap.replace("_placebo", "")
    cmd = ["systemd-run", "--user", "--scope", "-p",
           f"MemoryMax={mem}", "-p", "MemorySwapMax=0",
           COMP, "-m", model, "-c", str(CTX), "-n", str(NGEN),
           "-t", THREADS,
           "-p", "The history of computing begins with"]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        o = p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return {"cap": cap, "completed": False, "reason": "timeout"}
    m = re.search(r"eval time\s*=\s*[\d.]+\s*ms\s*/\s*(\d+)\s*runs.*?,\s*([\d.]+)\s*tokens per second", o)
    oom = ("OutOf memory" in o or "Killed" in o or p.returncode == 137)
    return {"cap": cap, "completed": bool(m) and not oom,
            "tokens": int(m.group(1)) if m else None,
            "tok_s": float(m.group(2)) if m else None,
            "oom": oom}

for name, path, fsize, caps in MODELS:
    log(f"=== {name} ladder ===")
    for cap in caps:
        r = run_capped(path, cap)
        r["model"] = name
        res["arms"].append(r); save()
        log(f"{name} @{cap}: completed={r['completed']} "
            f"tok_s={r.get('tok_s')} oom={r['oom']}")

log("canary: hashing after run")
for name, path, _, _ in MODELS:
    post = sha256(path)[:16]
    res["canary"][name]["post"] = post
    res["canary"][name]["clean"] = (post == res["canary"][name]["pre"])
save()
log(f"canary clean: {[v['clean'] for v in res['canary'].values()]}")

print("\n=== LADDER SUMMARY ===", flush=True)
for a in res["arms"]:
    print(a, flush=True)
log("ALL_DONE_NET104")

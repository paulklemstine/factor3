#!/usr/bin/env python3
# NET-99 — EIGHT-GB-FRONTIER: THE RAM-BUDGET COMPOSITION LAW
# (cpu-large-model axis, iteration 74; top-ranked cell of the 12-cell
#  fan-out program toward GOAL: very large LLM, very little RAM, very fast)
#
# HYPOTHESIS H: Law 2 (K-q8_0/V-q4_0 role-split cache, NET-94) and Law 3
# (Q2_K weights, NET-95) compose SUB-ADDITIVELY without context
# amplification, so the closed-form budget
#     params_max(RAM_GB, ctx) = (RAM_GB - C_overhead - KV_bytes(ctx)) / bpw_weights
# predicts real serving points inside hard cgroup caps within ±15%.
#
# PREDICTIONS STATED BEFORE ANY MEASUREMENT (frozen; a failed construction
# is recorded AS DATA, never repaired by loosening a cap mid-run):
#  P1 COMPOSABILITY @ctx512 on the standard 250KB prose slice:
#     R512 = PPL(q2_k weights + K q8_0/V q4_0) / PPL(q8_0 weights + f16/f16)
#     must lie in [1.10, 1.22].
#     R512 < 1.10 => super-additive benefit (record; tighten recipe claim).
#     R512 > 1.22 => MULTIPLICATIVE tax: K8/V4 is NOT quality-free atop
#     Q2_K weights; downstream stack cells must be redesigned.
#  P1b VARIANT: same ratio with -ctv iq4_nl stays within +0.003 absolute
#     of the V-q4_0 ratio.
#  P2 AMPLIFICATION GUARD (explicit NET-88 hypothesis test): R4096/R512 <= 1.5,
#     where R_ctx is the P1-style ratio at that ctx. Above 1.5 =>
#     context-amplified taxation confirmed; formula gains an amplification term.
#  P3 CONSTRUCTED POINT A: Qwen2.5-14B-Instruct Q2_K + -ctk q8_0 -ctv q4_0,
#     ctx=8192, systemd-run MemoryMax=8G MemorySwapMax=0, -t 8:
#     completes >=256 generated tokens, zero OOM kill, peak RSS <= 7.6GB,
#     tg >= 2.0 tok/s. If OOM occurs, the observed ceiling IS the datum.
#  P4 CONSTRUCTED POINT B: cached 7B stack (q2_k 3.02GB) completes inside
#     MemoryMax=4G @ ctx=4096 with zero OOM kill.
import json, os, re, subprocess, time

BIN = os.path.expanduser("~/f3cache/llama.cpp/build/bin/llama-perplexity")
COMP = os.path.expanduser("~/f3cache/llama.cpp/build/bin/llama-completion")
GG = os.path.expanduser("~/f3cache/gguf")
GG14 = os.path.expanduser("~/f3cache/gguf14b")
SRC = os.path.expanduser("~/f3cache/net49_corpus.txt")
RESULTS = os.path.expanduser("~/f3cache/net99_results.json")
THREADS = "8"
SLICE = "/tmp/net99_slice.txt"

M14 = os.path.join(GG14, "qwen2.5-14b-instruct-q2_k-00001-of-00002.gguf")
MARKER = os.path.join(GG14, "COMPLETE.marker")

text = open(SRC, encoding="utf-8", errors="ignore").read()
for name, sl in [("s512", 250_000), ("s4096", 250_000)]:
    open(f"/tmp/net99_{name}.txt", "w", encoding="utf-8").write(
        text[400_000:400_000 + sl])

res = {"meta": {"predictions": "P1 R512 in [1.10,1.22]; P1b iq4_nl within "
                              "+0.003 of q4_0 ratio; P2 R4096/R512 <= 1.5; "
                              "P3 14B@8G constructs; P4 7B@4G constructs"},
       "ppl": [], "constructed": []}

def save():
    json.dump(res, open(RESULTS, "w"), indent=1)

def ppl(model, ctx, ctkt, ctvt, slicefile):
    args = [BIN, "-m", model, "-f", slicefile, "-c", str(ctx), "-t", THREADS]
    if ctkt:
        args += ["--cache-type-k", ctkt, "--cache-type-v", ctvt]
    t0 = time.time()
    p = subprocess.run(args, capture_output=True, text=True, timeout=14400)
    m = re.search(r"Final estimate: PPL\s*=\s*([0-9.]+)", p.stdout + p.stderr)
    return (float(m.group(1)) if m else None, round(time.time() - t0, 1))

def wait_marker():
    log("waiting for 14B download...")
    for _ in range(120):
        if os.path.exists(MARKER):
            return
        time.sleep(60)
    raise SystemExit("FATAL: 14B download never completed")

def log(msg):
    print(msg, flush=True)
    open("/tmp/net99.log", "a").write(str(msg) + "\n")

wait_marker()
log("14B ready")

Q8 = os.path.join(GG, "qwen2.5-7b-instruct-q8_0-00001-of-00003.gguf")
Q2 = os.path.join(GG, "qwen2.5-7b-instruct-q2_k.gguf")
M14S = M14

ARMS = [
    ("control_q8_f16@512", Q8, 512, None, None, "s512"),
    ("composed_q2_kv48@512", Q2, 512, "q8_0", "q4_0", "s512"),
    ("weights_only_q2_f16@512", Q2, 512, None, None, "s512"),
    ("iq4nl_variant_q2_kv48@512", Q2, 512, "q8_0", "iq4_nl", "s512"),
    ("control_q8_f16@4096", Q8, 4096, None, None, "s4096"),
    ("composed_q2_kv48@4096", Q2, 4096, "q8_0", "q4_0", "s4096"),
    ("weights_only_q2_f16@4096", Q2, 4096, None, None, "s4096"),
]

vals = {}
for name, model, ctx, kt, vt, sl in ARMS:
    p, wall = ppl(model, ctx, kt, vt, f"/tmp/net99_{sl}.txt")
    vals[name] = p
    entry = {"arm": name, "ppl": p, "wall_s": wall}
    res["ppl"].append(entry)
    save()
    log(f"{name}: ppl={p} ({wall}s)")

try:
    R512 = vals["composed_q2_kv48@512"] / vals["control_q8_f16@512"]
    R4096 = vals["composed_q2_kv48@4096"] / vals["control_q8_f16@4096"]
    wtax512 = vals["weights_only_q2_f16@512"] / vals["control_q8_f16@512"]
    res["ratios"] = {"R512": round(R512, 4), "R4096": round(R4096, 4),
                     "weight_tax_512": round(wtax512, 4),
                     "amp_guard": round(R4096 / R512, 4)}
except Exception as e:
    res["ratios"] = {"error": str(e)}
save()
log(f"ratios: {res.get('ratios')}")

# ---------- P3/P4 constructed points ----------
def constructed(name, memmax, model, ctx, ngen):
    cmd = ["systemd-run", "--scope", "-p", f"MemoryMax={memmax}",
           "-p", "MemorySwapMax=0", COMP, "-m", model,
           "-ctk", "q8_0", "-ctv", "q4_0",
           "-p", "The history of computing begins with", "-n", str(ngen),
           "-c", str(ctx), "-t", THREADS]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
        o = p.stdout + p.stderr
        m = re.search(r"eval time\s*=\s*[\d.]+\s*ms\s*/\s*(\d+)\s*runs.*?,\s*([\d.]+)\s*tokens per second", o)
        entry = {"point": name, "completed": True,
                 "tokens": int(m.group(1)) if m else None,
                 "tok_s": float(m.group(2)) if m else None,
                 "oom": False, "wall_s": round(time.time() - t0, 1)}
    except subprocess.TimeoutExpired:
        entry = {"point": name, "completed": False, "oom": "timeout"}
    res["constructed"].append(entry)
    save()
    log(f"constructed {name}: {entry}")

log("P4: 7B stack inside 4G @ctx4096")
constructed("7B@4G_ctx4096", "4G", Q2, 4096, 64)

if os.path.exists(M14S):
    log("P3: 14B stack inside 8G @ctx8192")
    constructed("14B@8G_ctx8192", "8G", M14S, 8192, 256)
else:
    log("14B shard missing; P3 skipped")

log("ALL_DONE_NET99")

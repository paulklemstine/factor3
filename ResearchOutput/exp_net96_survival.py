#!/usr/bin/env python3
# NET-96 — THE SURVIVAL CURVE: PER-POSITION SPECULATIVE ACCEPTANCE BY DOMAIN
# (cpu-large-model axis, iteration 71)
#
# NET-91 found net-speedup-optimal depth is domain-parameterized (code pays
# through d=8; prose collapses past d=4) but left the mechanism unmeasured:
# llama.cpp reports only overall drafted-token acceptance. This cell sweeps
# depth finely {1..8} on the winning 0.5B draft and DIFFERENCES the cumulative
# acceptance to extract the per-position survival probability s_i =
# P(first i drafted tokens all accepted), which fully determines optimal depth.
#
# Identity used: with m(d) = overall accept fraction at max-depth d,
# E[accepted per cycle](d) = d*m(d) = sum_{i=1..d} s_i  =>  s_d = d*m(d) - (d-1)*m(d-1).
#
# PREDICTIONS STATED BEFORE ANY MEASUREMENT:
#  P1 PROSE-POSITION-4-CLIFF: prose survival halves by position 5
#     (s_5 < s_1/2) — the mechanism behind NET-91's d=8 net loss.
#  P2 CODE-DOMINATES-EVERYWHERE: s_i(code) > s_i(prose) for every i in 1..8.
#  P3 COST-LAW-CLOSES-THE-LOOP: predicted-optimal depth from the extracted
#     curve, argmax_d [ sum_i<=d s_i / (1 + d*r) ] with r = draft/target
#     cost ratio (~0.118), reproduces NET-91's measured argmax
#     (code: d=8, prose: d=4) within one grid step.
import json, os, re, statistics, subprocess, time

COMPLETION = os.path.expanduser("~/f3cache/llama.cpp/build/bin/llama-completion")
SPEC = os.path.expanduser("~/f3cache/llama.cpp/build/bin/llama-speculative")
GGUF_DIR = os.path.expanduser("~/f3cache/gguf")
TARGET = os.path.join(GGUF_DIR, "qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf")
DRAFT = os.path.join(GGUF_DIR, "qwen2.5-0.5b-instruct-q8_0.gguf")
CORPORA = {"prose": os.path.expanduser("~/f3cache/net49_corpus.txt"),
           "code": os.path.expanduser("~/f3cache/code_corpus.txt")}
DEPTHS = list(range(1, 9))
N_PROMPTS, PROMPT_CHARS, N_GEN, CTX, THREADS = 4, 2000, 96, 1024, "8"
RESULTS = os.path.expanduser("~/f3cache/net96_results.json")


def load_prompts(path, n, chars):
    text = open(path, encoding="utf-8", errors="ignore").read()
    step = len(text) // (n + 20)
    return [text[step * (i + 10):step * (i + 10) + chars] for i in range(n)]


def save(res):
    json.dump(res, open(RESULTS, "w"), indent=1)


res = {"meta": {"target": TARGET, "draft": DRAFT, "depths": DEPTHS,
                "n_gen": N_GEN, "threads": THREADS,
                "predictions": "P1 prose s_5 < s_1/2; "
                               "P2 s_i(code) > s_i(prose) all i; "
                               "P3 cost-law argmax matches NET-91 "
                               "(code 8, prose 4) within one step"},
       "grid": [], "overhead": {}}

for domain in ("prose", "code"):
    prompts = load_prompts(CORPORA[domain], N_PROMPTS, PROMPT_CHARS)
    # overhead calibration (load+prompt-eval) once per domain
    t0 = time.time()
    subprocess.run([SPEC, "-m", TARGET, "-md", DRAFT, "--spec-type",
                    "draft-simple", "-p", prompts[0], "-n", "1",
                    "-c", str(CTX), "-t", THREADS], capture_output=True)
    res["overhead"][domain] = round(time.time() - t0, 3)
    print(f"overhead[{domain}] = {res['overhead'][domain]}s", flush=True)
    save(res)

    for depth in DEPTHS:
        accs = []
        for prompt in prompts:
            out = subprocess.run([SPEC, "-m", TARGET, "-md", DRAFT,
                                  "--spec-type", "draft-simple",
                                  "--spec-draft-n-max", str(depth),
                                  "--spec-draft-n-min", "1",
                                  "-p", prompt, "-n", str(N_GEN),
                                  "-c", str(CTX), "-t", THREADS, "-s", "42"],
                                 capture_output=True, text=True, timeout=2400)
            o = out.stdout + out.stderr
            m = re.findall(r"accept\s*=\s*([\d.]+)%", o)
            if m:
                accs.append(float(m[-1]))
        med = statistics.median(accs) if accs else None
        entry = {"domain": domain, "depth": depth, "accept_pct": med,
                 "n_ok": len(accs)}
        res["grid"].append(entry)
        save(res)
        print(f"m({domain},{depth}) = {med}", flush=True)

print("\n=== SURVIVAL CURVES ===", flush=True)
curves = {}
for domain in ("prose", "code"):
    ms = {e["depth"]: e["accept_pct"] for e in res["grid"]
          if e["domain"] == domain and e["accept_pct"] is not None}
    s = {}
    prev = 0.0
    for d in sorted(ms):
        cum = d * ms[d] / 100.0
        s[d] = round(cum - prev, 4)
        prev = cum
    curves[domain] = s
    print(f"{domain}: {s}", flush=True)
res["survival"] = curves
save(res)

if curves.get("prose") and curves.get("code"):
    s1p = curves["prose"].get(1, 0)
    print(f"P1 prose s5={curves['prose'].get(5)} vs s1/2={s1p/2:.4f}",
          flush=True)
    dom_all = all(curves["code"].get(i, 0) > curves["prose"].get(i, 0)
                  for i in range(1, 9))
    print(f"P2 code>prose everywhere: {dom_all}", flush=True)
    r = 0.118
    for domain in ("prose", "code"):
        best_d, best_v = None, -1
        for d in range(1, 9):
            v = sum(curves[domain].get(i, 0) for i in range(1, d + 1)) / (1 + d * r)
            if v > best_v:
                best_v, best_d = v, d
        print(f"P3 predicted-optimal depth [{domain}] = {best_d}", flush=True)
print("ALL_DONE_NET96", flush=True)

#!/usr/bin/env python3
# NET-91 — SPECULATIVE DECODING ON CPU: THE DRAFT-IS-NOT-FREE COST LAW
# (cpu-large-model axis, iteration 66)
#
# FIRST round of the CPU-large-model pivot: Qwen2.5-7B-Instruct Q4_K_M executed
# entirely on CPU (llama.cpp, i9-9900K) with same-family draft models proposing
# tokens the target verifies. The lab's unique angle: NET-51 measured
# base-vs-Instruct keys near-identical (cos >= 0.976 everywhere, layer 0 exact)
# -> same-family cross-SIZE key spaces should agree enough for high speculative
# acceptance. No catalog entry (local or alethean.org) covers this cell.
#
# Toolchain (validated by smoke tests): baselines/draft-only via
# llama-completion (raw text completion); speculation via llama-speculative
# (-md DRAFT --spec-type draft-simple, prints accept %). Effective generation
# wall time = full-run wall - overhead run (-n 1) for the same model pair,
# immune to perf-print accounting quirks.
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 KEY-SHARING->ACCEPTANCE: same-family 0.5B->7B mean acceptance at draft
#     depth 4 on prose >= 50% (from NET-51 cos >= 0.976 key sharing).
#  P2 NET-WIN-ON-CPU: at least one (draft, depth) config beats the no-draft
#     greedy baseline by >5% effective tok/s (draft is NOT free on CPU).
#  P3 CROSSOVER: 1.5B accepts MORE per drafted token than 0.5B, but its higher
#     draft cost creates a crossover beyond which 0.5B wins net tok/s;
#     predicted inside the depth grid {2,4,8}.
#  P4 CODE-IS-EASIER-TO-DRAFT: acceptance(code) > acceptance(prose) by >= 5 pts
#     (our domain line: code attention is MORE concentrated — lower knee,
#     sharper next-token distributions).
import json
import os
import re
import statistics
import subprocess
import time

COMPLETION = os.path.expanduser("~/f3cache/llama.cpp/build/bin/llama-completion")
SPEC = os.path.expanduser("~/f3cache/llama.cpp/build/bin/llama-speculative")
GGUF_DIR = os.path.expanduser("~/f3cache/gguf")
TARGET = os.environ.get(
    "NET91_TARGET",
    os.path.join(GGUF_DIR, "qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf"))
DRAFTS = {
    "0.5B": os.path.join(GGUF_DIR, "qwen2.5-0.5b-instruct-q8_0.gguf"),
    "1.5B": os.path.join(GGUF_DIR, "qwen2.5-1.5b-instruct-q4_k_m.gguf"),
}
CORPORA = {
    "prose": os.path.expanduser("~/f3cache/net49_corpus.txt"),
    "code": os.path.expanduser("~/f3cache/code_corpus.txt"),
}
DEPTHS = [2, 4, 8]
N_PROMPTS = 4
PROMPT_CHARS = 2000
N_GEN = 96
CTX = 1024
REPEATS = 2
RESULTS = os.path.expanduser("~/f3cache/net91_results.json")


def save(res):
    json.dump(res, open(RESULTS, "w"), indent=1)


def load_prompts(path, n, chars):
    text = open(path, encoding="utf-8", errors="ignore").read()
    step = len(text) // (n + 20)
    out = []
    for i in range(n):
        s = step * (i + 10)
        chunk = text[s:s + chars]
        if len(chunk.strip()) > chars // 2:
            out.append(chunk)
    return out[:n]


def run(binary, args, timeout=2400):
    t0 = time.time()
    p = subprocess.run([binary] + args, capture_output=True, text=True,
                       timeout=timeout)
    return p.stdout + p.stderr, time.time() - t0


def parse_eval_toks(out):
    """llama-completion perf print: eval tok/s."""
    m = re.search(r"eval time\s*=\s*[\d.]+\s*ms\s*/\s*(\d+)\s*runs.*?,\s*([\d.]+)\s*tokens per second", out)
    return (float(m.group(2)), int(m.group(1))) if m else (None, None)


def parse_spec(out):
    """llama-speculative: acceptance stats."""
    acc = re.findall(r"accept\s*=\s*([\d.]+)%", out)
    nd = re.findall(r"n_drafted\s*=\s*(\d+)", out)
    na = re.findall(r"n_accept\s*=\s*(\d+)", out)
    return (float(acc[-1]) if acc else None,
            int(nd[-1]) if nd else None,
            int(na[-1]) if na else None)


def main():
    res = {"meta": {
        "tool": "llama.cpp (built today, GGML_NATIVE)",
        "target": TARGET,
        "depths": DEPTHS, "n_gen": N_GEN, "ctx": CTX,
        "repeats": REPEATS, "n_prompts": N_PROMPTS,
        "prompt_chars": PROMPT_CHARS,
        "predictions": "P1 0.5B@d4 prose accept>=50%; P2 some config >1.05x "
                       "effective tok/s; P3 0.5B/1.5B crossover in grid; "
                       "P4 code accept > prose accept by >=5 pts",
    }, "baseline": [], "draft_only": [], "overhead": [], "spec": []}

    # ---------- Phase 0: thread sweep on target baseline ----------
    print("=== PHASE 0: baseline thread sweep (7B Q4_K_M, no draft) ===",
          flush=True)
    prompt = load_prompts(CORPORA["prose"], 1, PROMPT_CHARS)[0]
    best_threads, best_ts = None, -1.0
    for th in (8, 16):
        vals = []
        for _ in range(REPEATS):
            out, _ = run(COMPLETION, ["-m", TARGET, "-p", prompt,
                                      "-n", str(N_GEN), "-c", str(CTX),
                                      "-t", str(th)])
            ts, _ = parse_eval_toks(out)
            if ts:
                vals.append(ts)
        ts = statistics.median(vals) if vals else 0.0
        print(f"  threads={th}: {ts:.2f} tok/s", flush=True)
        res["baseline"].append({"threads": th, "tok_s": round(ts, 3)})
        save(res)
        if ts > best_ts:
            best_threads, best_ts = th, ts
    TH = str(best_threads)
    BASE_TS = best_ts
    print(f"PICKED threads={TH} base={BASE_TS:.2f} tok/s", flush=True)

    # ---------- Phase 1: draft-only cost ----------
    print("=== PHASE 1: draft-only tok/s ===", flush=True)
    for name, path in DRAFTS.items():
        vals = []
        for dm in ("prose", "code"):
            p = load_prompts(CORPORA[dm], 1, PROMPT_CHARS)[0]
            out, _ = run(COMPLETION, ["-m", path, "-p", p,
                                      "-n", str(N_GEN), "-c", str(CTX),
                                      "-t", TH])
            ts, _ = parse_eval_toks(out)
            if ts:
                vals.append(ts)
        ts = statistics.median(vals) if vals else 0.0
        ratio = ts / BASE_TS if BASE_TS else None
        print(f"  draft {name}: {ts:.2f} tok/s ({ratio:.3f}x target)",
              flush=True)
        res["draft_only"].append({"draft": name, "tok_s": round(ts, 3),
                                  "cost_ratio_vs_target":
                                      round(ratio, 4) if ratio else None})
        save(res)

    # ---------- Phase 2: overhead runs (load+prompt-eval per pair/domain) --
    print("=== PHASE 2: overhead calibration ===", flush=True)
    overhead = {}
    for name, path in list(DRAFTS.items()) + [("none", None)]:
        for dm in ("prose", "code"):
            p = load_prompts(CORPORA[dm], 1, PROMPT_CHARS)[0]
            args = ["-m", TARGET, "-p", p, "-n", "1", "-c", str(CTX),
                    "-t", TH]
            if path:
                args += ["-md", path, "--spec-type", "draft-simple"]
            _, wall = run(SPEC, args)
            overhead[(name, dm)] = wall
            res["overhead"].append({"draft": name, "domain": dm,
                                    "wall_s": round(wall, 3)})
            print(f"  overhead {name}/{dm}: {wall:.2f}s", flush=True)
    save(res)

    # ---------- Phase 3: speculative grid ----------
    print("=== PHASE 3: speculative grid ===", flush=True)
    for draft_name, draft_path in DRAFTS.items():
        for depth in DEPTHS:
            for domain in ("prose", "code"):
                effs, accs = [], []
                for prompt in load_prompts(CORPORA[domain], N_PROMPTS,
                                           PROMPT_CHARS):
                    for _ in range(REPEATS):
                        out, wall = run(SPEC, [
                            "-m", TARGET, "-md", draft_path,
                            "--spec-type", "draft-simple",
                            "--spec-draft-n-max", str(depth),
                            "--spec-draft-n-min", "1",
                            "-p", prompt, "-n", str(N_GEN), "-c", str(CTX),
                            "-t", TH, "-s", "42"])
                        a, nd, na = parse_spec(out)
                        eff = N_GEN / max(wall - overhead[(draft_name, domain)],
                                          0.5)
                        effs.append(eff)
                        if a is not None:
                            accs.append(a)
                med = statistics.median(effs) if effs else 0.0
                acc_mean = statistics.mean(accs) if accs else None
                sp = med / BASE_TS if BASE_TS else 0.0
                entry = {"draft": draft_name, "depth": depth,
                         "domain": domain,
                         "eff_tok_s": round(med, 3),
                         "speedup_vs_base": round(sp, 4),
                         "accept_pct_mean": round(acc_mean, 2)
                             if acc_mean is not None else None,
                         "n_meas": len(effs)}
                print(f"  {draft_name} d={depth} {domain}: {med:.2f} tok/s "
                      f"({sp:.3f}x) accept={entry['accept_pct_mean']}",
                      flush=True)
                res["spec"].append(entry)
                save(res)

    # ---------- Verdicts ----------
    print("\n=== VERDICTS ===", flush=True)
    spec = res["spec"]
    p1 = [e for e in spec if e["draft"] == "0.5B" and e["depth"] == 4
          and e["domain"] == "prose"]
    print("P1 accept(0.5B,d4,prose) =", p1[0]["accept_pct_mean"] if p1 else "?",
          "(predicted >= 50)", flush=True)
    best = max(spec, key=lambda e: e["speedup_vs_base"]) if spec else None
    print(f"P2 best config: {best} (predicted >1.05x)", flush=True)
    for dom in ("prose", "code"):
        b05 = [e for e in spec if e["draft"] == "0.5B" and e["domain"] == dom]
        b15 = [e for e in spec if e["draft"] == "1.5B" and e["domain"] == dom]
        acc05 = [e["accept_pct_mean"] for e in b05]
        acc15 = [e["accept_pct_mean"] for e in b15]
        print(f"P3[{dom}] accept 0.5B={acc05} 1.5B={acc15}; "
              f"net {[(e['depth'], e['speedup_vs_base']) for e in b05]} vs "
              f"{[(e['depth'], e['speedup_vs_base']) for e in b15]}",
              flush=True)
    pd4 = [e for e in spec if e["domain"] == "prose"]
    pc4 = [e for e in spec if e["domain"] == "code"]
    mp = statistics.mean([e["accept_pct_mean"] for e in pd4
                          if e["accept_pct_mean"] is not None] or [0])
    mc = statistics.mean([e["accept_pct_mean"] for e in pc4
                          if e["accept_pct_mean"] is not None] or [0])
    print(f"P4 mean accept code={mc:.1f} prose={mp:.1f} "
          f"(predicted code >= prose+5)", flush=True)
    print("ALL_DONE_NET91", flush=True)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# NET-70 — THE MATH-DOMAIN KNEE (limited-memory axis, iteration 36)
# Second domain-jump leg: mathematical prose (arXiv-style LaTeX-heavy text). Math has
# long-range symbolic references (equation numbers, theorem labels) — the opposite
# extreme from code's local repetitiveness. Does the knee rise?
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 MATH-NEEDS-MORE: k*(512) > 16 and k*(1024) > 20 (long-range symbolic refs make
#     attention less local — the domain parameter moves UP).
#  P2 STRUCTURE-PRESERVED: whatever the values, the +4/doubling prose increment
#     approximately holds (chain shape domain-independent, only base shifts).
#  P3 BASE-UNIVERSAL: knees match prose exactly ({16, 20}) — math reads as prose.
import json, math, os, time, urllib.request
import torch
import torch.nn.functional as F

src = open("/home/raver1975/factor3/ResearchOutput/exp_net68_domainjump.py").read()
src = src.replace('if __name__ == "__main__":\n    main()', "")
g = {}
exec(compile(src, "e68", "exec"), g)
globals().update(g)

MATH_CACHE = os.path.expanduser("~/f3cache/math_corpus.txt")

def fetch_math():
    if os.path.exists(MATH_CACHE) and os.path.getsize(MATH_CACHE) > 1_000_000:
        return open(MATH_CACHE, encoding="utf-8", errors="ignore").read()
    # arXiv abstracts + intro sections via the export mirror (plain text)
    base = "https://arxiv.org/abs/"
    # fallback: use Project Gutenberg mathematics classics (plain text, reliable)
    gut = ["https://www.gutenberg.org/files/38427/38427-0.txt",  # A Course of Pure Mathematics
           "https://www.gutenberg.org/files/38969/38969-0.txt",  # An Investigation of the Laws of Thought
           "https://www.gutenberg.org/files/25346/25346-0.txt"]  # The Foundations of Geometry
    parts = []
    for u in gut:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "research-loop/1.0"})
            t = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", errors="ignore")
            parts.append(t)
            print(f"[math] {u.split('/')[-1]}: {len(t)} chars", flush=True)
        except Exception as e:
            print(f"[math] FAILED {u}: {e}", flush=True)
    s = "\n\n".join(parts)
    assert len(s) > 500_000, f"math corpus too small: {len(s)}"
    with open(MATH_CACHE, "w", encoding="utf-8") as fh:
        fh.write(s); fh.flush(); os.fsync(fh.fileno())
    return s

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, dtype=torch.float32,
                                                 attn_implementation="eager").cuda().eval()
    runner = Runner(model)
    text = fetch_math()[:4_000_000]
    ids_all = torch.tensor(tok(text, add_special_tokens=False).input_ids, dtype=torch.long)
    split = int(0.9 * len(ids_all))
    held = ids_all[split:].cuda()

    with torch.no_grad():
        vb = held[:128].view(1, -1)
        ref = model(input_ids=vb).logits.float()
        mine = model.lm_head(runner.forward_oracle(vb)).float()
        agree = float((ref.argmax(-1) == mine.argmax(-1)).float().mean())
        print(f"[validate] argmax-agree={agree:.4f}", flush=True)
        assert agree >= 0.999
    del ref, mine
    torch.cuda.empty_cache()

    res = {"domain": "math-prose", "cells": []}
    for ctx in CTXS:
        wl = ctx + 1
        win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]

        @torch.no_grad()
        def ev(k):
            ces, corr, tot = 0.0, 0, 0
            for s in range(0, len(win), BS):
                b = torch.cat(win[s:s+BS], dim=0)
                h = runner.forward_oracle(b, k=k)
                tgt = b[:, 1:]
                n = b.size(0)*(b.size(1)-1)
                V = model.config.vocab_size
                for s2 in range(0, b.size(1)-1, 64):
                    e2 = min(s2+64, b.size(1)-1)
                    lg = model.lm_head(h[:, s2:e2]).reshape(-1, V).float()
                    t = tgt[:, s2:e2].reshape(-1)
                    ces += F.cross_entropy(lg, t, reduction="sum").item()
                    corr += (lg.argmax(-1) == t).sum().item()
                tot += n
            return ces/tot, corr/tot

        full_ce, full_acc = ev(None)
        base = max(full_acc, 1e-9)
        print(f"\n[CTX={ctx}] full acc={full_acc:.4f} ce={full_ce:.4f}", flush=True)
        for k in GRIDS[ctx]:
            ce, acc = ev(k)
            ret = acc/base
            print(f"[k={k:<5}] ret={ret:.4f} {'PASS' if ret>=0.98 else 'fail'} ce={ce:.4f}", flush=True)
            res["cells"].append({"ctx": ctx, "k": k, "retained": round(ret, 5)})
            json.dump(res, open(os.path.expanduser("~/f3cache/net70_results.json"), "w"), indent=1)
            torch.cuda.empty_cache()
        kp = [c["k"] for c in res["cells"] if c["ctx"] == ctx and c["retained"] >= 0.98]
        res[f"kstar_ctx{ctx}"] = min(kp) if kp else None
        json.dump(res, open(os.path.expanduser("~/f3cache/net70_results.json"), "w"), indent=1)
        print(f"[KSTAR ctx={ctx}] k* = {res[f'kstar_ctx{ctx}']}", flush=True)

    print("\nALL_DONE_NET70", flush=True)

if __name__ == "__main__":
    main()

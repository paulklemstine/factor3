#!/usr/bin/env python3
# NET-68 — THE DOMAIN-JUMP TEST (limited-memory axis, iteration 32)
# Every knee so far was measured on prose (wikitext shards). This round jumps domains:
# PYTHON SOURCE CODE as eval text. Does the ~20-key budget survive a register change?
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 KNEES-TRANSFER: k*(512) in {12..24} and k*(1024) in {16..28} — within one coarse
#     step of the wikitext values {16, 20}: budget tables are domain-portable.
#  P2 CODE-NEEDS-FEWER: code is locally repetitive -> knees strictly BELOW the wikitext
#     values (k*(512) < 16).
#  P3 CODE-NEEDS-MORE: long-range identifier references make attention less local ->
#     knees strictly ABOVE (k*(512) > 24).
import json, math, os, time, urllib.request
import torch
import torch.nn.functional as F

src = open("/home/raver1975/factor3/ResearchOutput/exp_net56_policy.py").read()
src = src.replace('if __name__ == "__main__":\n    main()', "")
g = {}
exec(compile(src, "e56", "exec"), g)
Runner = g["Runner"]

MODEL_DIR = os.path.expanduser("~/f3cache/qwen25-05b")
CODE_CACHE = os.path.expanduser("~/f3cache/code_corpus.txt")
CTXS = [512, 1024]
GRIDS = {512: [4, 8, 12, 16, 20, 24], 1024: [8, 12, 16, 20, 24, 32]}
NW, BS = 24, 4

def fetch_code():
    if os.path.exists(CODE_CACHE) and os.path.getsize(CODE_CACHE) > 1_000_000:
        return open(CODE_CACHE, encoding="utf-8", errors="ignore").read()
    base = "https://raw.githubusercontent.com/python/cpython/main/Lib/"
    files = ["asyncio/base_events.py", "asyncio/streams.py", "email/message.py",
             "http/client.py", "json/encoder.py", "logging/handlers.py",
             "unittest/case.py", "xml/etree/ElementTree.py", "dataclasses.py",
             "typing.py"]
    parts = []
    for f in files:
        try:
            req = urllib.request.Request(base + f, headers={"User-Agent": "research-loop/1.0"})
            t = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", errors="ignore")
            parts.append(t)
            print(f"[code] {f}: {len(t)} chars", flush=True)
        except Exception as e:
            print(f"[code] FAILED {f}: {e}", flush=True)
    s = "\n\n".join(parts)
    assert len(s) > 500_000, f"code corpus too small: {len(s)}"
    with open(CODE_CACHE, "w", encoding="utf-8") as fh:
        fh.write(s); fh.flush(); os.fsync(fh.fileno())
    return s

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, dtype=torch.float32,
                                                 attn_implementation="eager").cuda().eval()
    runner = Runner(model)
    text = fetch_code()[:4_000_000]
    ids_all = torch.tensor(tok(text, add_special_tokens=False).input_ids, dtype=torch.long)
    split = int(0.9 * len(ids_all))
    held = ids_all[split:].cuda()

    with torch.no_grad():
        vb = held[:128].view(1, -1)
        ref = model(input_ids=vb).logits.float()
        mine = model.lm_head(runner.forward_oracle(vb)).float()
        agree = float((ref.argmax(-1) == mine.argmax(-1)).float().mean())
        print(f"[validate] argmax-agree={agree:.4f} CE={F.cross_entropy(mine[:, :-1].reshape(-1, mine.size(-1)), vb[:, 1:].reshape(-1)).item():.4f}", flush=True)
        assert agree >= 0.999
    del ref, mine
    torch.cuda.empty_cache()

    res = {"domain": "python-source", "cells": []}
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
            json.dump(res, open(os.path.expanduser("~/f3cache/net68_results.json"), "w"), indent=1)
            torch.cuda.empty_cache()
        kp = [c["k"] for c in res["cells"] if c["ctx"] == ctx and c["retained"] >= 0.98]
        res[f"kstar_ctx{ctx}"] = min(kp) if kp else None
        json.dump(res, open(os.path.expanduser("~/f3cache/net68_results.json"), "w"), indent=1)
        print(f"[KSTAR ctx={ctx}] k* = {res[f'kstar_ctx{ctx}']}", flush=True)

    print("\nALL_DONE_NET68", flush=True)

if __name__ == "__main__":
    main()

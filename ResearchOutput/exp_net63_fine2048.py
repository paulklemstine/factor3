#!/usr/bin/env python3
# NET-63 — THE FINE GRID AT 2048 (limited-memory axis, iteration 22)
# Corpus-A read k*=24 (razor-thin +0.5 SE) at ctx=2048; corpus-B read 32. NET-62 resolved
# the 1024 cell as a coarse-grid artifact (fine knee 20). This round does the same for 2048
# on corpus-A: sweep k in {20, 24, 28, 32}.
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 GRID-ARTIFACT-RESOLVED: a fine point strictly between 24 and 32 passes (knee in
#     {28}), i.e. both prior readings were coarse-grid artifacts.
#  P2 MONOTONE-CHAIN-HOLDS: whatever the fine knee, the chain stays strictly monotone
#     {16, 20, k*(2048)} with k*(2048) > 20.
#  P3 RAZOR-CONFIRMED: k=28 fails and k=24's pass is confirmed non-razor (retained >= 0.985),
#     making corpus-B's 32 reading the true knee and raising questions about cross-shard
#     attention structure instead.
import json, math, os, time
import torch
import torch.nn.functional as F

src = open("/home/raver1975/factor3/ResearchOutput/exp_net56_policy.py").read()
src = src.replace('if __name__ == "__main__":\n    main()', "")
g = {}
exec(compile(src, "e56", "exec"), g)
Runner = g["Runner"]

MODEL_DIR = os.path.expanduser("~/f3cache/qwen25-05b")
CORPUS = os.path.expanduser("~/f3cache/net49_corpus.txt")   # corpus A
CTX, NW = 2048, 12   # VRAM-safe window count at long context

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, dtype=torch.float32,
                                                 attn_implementation="eager").cuda().eval()
    runner = Runner(model)
    text = open(CORPUS, encoding="utf-8").read()[:4_000_000]
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

    wl = CTX + 1
    win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]

    @torch.no_grad()
    def ev(k):
        ces, corr, tot = 0.0, 0, 0
        for s in range(0, len(win), 1):
            b = win[s].cuda()
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
    print(f"[full ] acc={full_acc:.4f} ce={full_ce:.4f} (nw={len(win)})", flush=True)
    res = {"ctx": CTX, "corpus": "A", "nw": len(win), "full_acc": round(full_acc, 5),
           "cells": []}
    json.dump(res, open(os.path.expanduser("~/f3cache/net63_results.json"), "w"), indent=1)
    for k in (20, 24, 28, 32):
        ce, acc = ev(k)
        ret = acc/base
        print(f"[k={k:<5}] ret={ret:.4f} {'PASS' if ret>=0.98 else 'fail'} ce={ce:.4f}", flush=True)
        res["cells"].append({"k": k, "retained": round(ret, 5)})
        json.dump(res, open(os.path.expanduser("~/f3cache/net63_results.json"), "w"), indent=1)
        torch.cuda.empty_cache()
    kp = [c["k"] for c in res["cells"] if c["retained"] >= 0.98]
    res["kstar"] = min(kp) if kp else None
    json.dump(res, open(os.path.expanduser("~/f3cache/net63_results.json"), "w"), indent=1)
    print(f"[KSTAR ctx=2048 fine] k* = {res['kstar']}", flush=True)
    print("\nALL_DONE_NET63", flush=True)

if __name__ == "__main__":
    main()

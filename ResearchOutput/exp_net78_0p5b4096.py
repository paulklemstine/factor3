#!/usr/bin/env python3
# NET-78 — THE 0.5B AT 4096 (limited-memory axis, iteration 51)
# The 0.5B chain is {16, 20, 24} at {512, 1024, 2048} with +4/doubling. This extends to
# the next doubling: does k*(4096) = 28?
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 INCREMENT-HALVING-LAW: k*(4096) = 28 (= 24 + 4, the +4/doubling increment continues).
#  P2 SATURATION: k*(4096) = 24 or below (the increment decays at long context).
#  P3 ACCELERATION: k*(4096) > 28 (the increment grows with context).
import json, math, os, time
import torch
import torch.nn.functional as F

src = open("/home/raver1975/factor3/ResearchOutput/exp_net56_policy.py").read()
src = src.replace('if __name__ == "__main__":\n    main()', "")
g = {}
exec(compile(src, "e56", "exec"), g)
Runner = g["Runner"]

MODEL_DIR = os.path.expanduser("~/f3cache/qwen25-05b")
CORPUS = os.path.expanduser("~/f3cache/net49_corpus.txt")
CTX, NW, BS = 4096, 6, 1

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
        t0 = time.time()
        for b0 in win:
            b = b0.cuda()
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
        return ces/tot, corr/tot, time.time()-t0

    full_ce, full_acc, _ = ev(None)
    base = max(full_acc, 1e-9)
    print(f"[full ] acc={full_acc:.4f} ce={full_ce:.4f} (nw={len(win)})", flush=True)
    res = {"ctx": CTX, "nw": len(win), "full_acc": round(full_acc, 5), "cells": []}
    json.dump(res, open(os.path.expanduser("~/f3cache/net78_results.json"), "w"), indent=1)
    for k in (16, 20, 24, 28, 32, 40):
        ce, acc, dt = ev(k)
        ret = acc/base
        print(f"[k={k:<5}] ret={ret:.4f} {'PASS' if ret>=0.98 else 'fail'} "
              f"ce={ce:.4f} ({dt:.0f}s)", flush=True)
        res["cells"].append({"k": k, "retained": round(ret, 5)})
        json.dump(res, open(os.path.expanduser("~/f3cache/net78_results.json"), "w"), indent=1)
        torch.cuda.empty_cache()
    kp = [c["k"] for c in res["cells"] if c["retained"] >= 0.98]
    res["kstar"] = min(kp) if kp else ">40"
    json.dump(res, open(os.path.expanduser("~/f3cache/net78_results.json"), "w"), indent=1)
    print(f"[KSTAR 0.5B ctx=4096] k* = {res['kstar']}", flush=True)
    print("\nALL_DONE_NET78", flush=True)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# NET-77 — 1.5B FINE GRID @2048: DOES THE SHIFTED CHAIN HOLD? (limited-memory axis,
# iteration 50) NET-66 found the 1.5B knee at 2048 is k*=20 on a coarse grid; NET-67
# refined it to k*=18. But the bracket was (16,20] with k=16 failing razor-thin (~1SE).
# This round adds k=14 to close it and confirms the one-octave shift prediction:
# 1.5B {16,16,18} should have its 2048 knee at 18 (= 0.5B's 1024 value shifted one octave).
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 EIGHTEEN-STANDS: k=14 fails and k=18 passes (already confirmed in NET-67) ->
#     the chain is {16,16,18} with the one-octave shift intact.
#  P2 FOURTEEN-SURPRISES: k=14 passes -> the knee drops below 18, weakening the shift
#     and suggesting the 1.5B is even more context-stable than measured.
import json, math, os, time
import torch
import torch.nn.functional as F

src = open("/home/raver1975/factor3/ResearchOutput/exp_net55_1p5b_knee.py").read()
src = src.replace('if __name__ == "__main__":\n    main()', "")
g = {}
exec(compile(src, "e55", "exec"), globals())

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, dtype=torch.bfloat16,
                                                 attn_implementation="eager").cuda().eval()
    runner = Runner(model)
    text = open(CORPUS, encoding="utf-8").read()[:4_000_000]
    ids_all = torch.tensor(tok(text, add_special_tokens=False).input_ids, dtype=torch.long)
    split = int(0.9 * len(ids_all))
    held = ids_all[split:].cuda()

    with torch.no_grad():
        vb = held[:128].view(1, -1)
        ref = model(input_ids=vb).logits.float()
        assert torch.isfinite(ref).all()
        floatify_linears(model)
        h = runner.forward(vb)
        mine = model.lm_head(h).float()
        agree = float((ref.argmax(-1) == mine.argmax(-1)).float().mean())
        ce_r = F.cross_entropy(ref[:, :-1].reshape(-1, ref.size(-1)), vb[:, 1:].reshape(-1)).item()
        ce_m = F.cross_entropy(mine[:, :-1].reshape(-1, mine.size(-1)), vb[:, 1:].reshape(-1)).item()
        print(f"[validate] argmax-agree={agree:.4f} CE ref={ce_r:.4f} mine={ce_m:.4f}", flush=True)
        assert agree >= 0.85 and abs(ce_r - ce_m) < 0.02
    del ref, mine
    torch.cuda.empty_cache()

    CTX, NW = 2048, 12
    wl = CTX + 1
    win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]

    @torch.no_grad()
    def ev(k):
        ces, corr, tot = 0.0, 0, 0
        for b0 in win:
            b = b0.cuda()
            kw = {"mode": "topk", "k": k} if k is not None else {}
            h = runner.forward(b, **kw)
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
    print(f"[full ] acc={full_acc:.4f} — baseline must match NET-66's 0.5132", flush=True)
    assert abs(full_acc - 0.5132) < 0.002, "baseline drift"
    res = {"ctx": CTX, "nw": len(win), "full_acc": round(full_acc, 5), "cells": []}
    json.dump(res, open(os.path.expanduser("~/f3cache/net77_results.json"), "w"), indent=1)
    for k in (14,):
        ce, acc = ev(k)
        ret = acc/base
        margin_se = abs(ret - 0.98) / 0.005  # rough SE estimate
        print(f"[k={k:<5}] ret={ret:.4f} {'PASS' if ret>=0.98 else 'fail'}", flush=True)
        res["cells"].append({"k": k, "retained": round(ret, 5)})
        json.dump(res, open(os.path.expanduser("~/f3cache/net77_results.json"), "w"), indent=1)
        torch.cuda.empty_cache()
    print(f"[VERDICT] {'P2 confirmed: knee < 18' if res['cells'][-1]['retained'] >= 0.98 else 'P1 confirmed: knee = 18 stands'}", flush=True)
    print("\nALL_DONE_NET77", flush=True)

if __name__ == "__main__":
    main()

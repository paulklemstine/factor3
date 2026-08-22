#!/usr/bin/env python3
# NET-76 — THE FRENCH EXTENDED GRID AT 512 (limited-memory axis, iteration 48)
# NET-72 found knee >24 at 512; NET-75 found knee =40 at 1024. If the +4/doubling
# increment holds for French too, k*(fr@512) should be ~36. But if French has a
# different increment, this cell pins it. Also: NET-72's grid only went to k=24.
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 PROPORTIONAL-TAX: k*(fr@512) = 36 (= 40 − 4, consistent with +4/doubling).
#  P2 HIGHER-BASE-HIGHER-INCREMENT: k*(fr@512) > 32 (French has a steeper context-
#     sensitivity curve because the higher base compounds).
#  P3 SAME-RATIO: k*(fr@512) = 30 (half of 60 ≈ half of 40×1.5 — same ratio to English
#     as at 1024).
import json, math, os, time
import torch
import torch.nn.functional as F

src = open("/home/raver1975/factor3/ResearchOutput/exp_net68_domainjump.py").read()
src = src.replace('if __name__ == "__main__":\n    main()', "")
g = {}
exec(compile(src, "e68", "exec"), g)
globals().update(g)

FR_CACHE = os.path.expanduser("~/f3cache/french_corpus.txt")

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, dtype=torch.float32,
                                                 attn_implementation="eager").cuda().eval()
    runner = Runner(model)
    text = open(FR_CACHE, encoding="utf-8").read()[:4_000_000]
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

    CTX, NW = 512, 24
    wl = CTX + 1
    win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]

    @torch.no_grad()
    def ev(k):
        ces, corr, tot = 0.0, 0, 0
        t0 = time.time()
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
        return ces/tot, corr/tot, time.time()-t0

    full_ce, full_acc, _ = ev(None)
    base = max(full_acc, 1e-9)
    print(f"[full ] acc={full_acc:.4f} ce={full_ce:.4f} (nw={len(win)})", flush=True)
    res = {"domain": "french", "ctx": CTX, "nw": len(win),
           "full_acc": round(full_acc, 5), "cells": []}
    json.dump(res, open(os.path.expanduser("~/f3cache/net76_results.json"), "w"), indent=1)
    for k in (24, 28, 32, 36, 44):
        ce, acc, dt = ev(k)
        ret = acc/base
        print(f"[k={k:<5}] ret={ret:.4f} {'PASS' if ret>=0.98 else 'fail'} "
              f"ce={ce:.4f} ({dt:.0f}s)", flush=True)
        res["cells"].append({"k": k, "retained": round(ret, 5)})
        json.dump(res, open(os.path.expanduser("~/f3cache/net76_results.json"), "w"), indent=1)
        torch.cuda.empty_cache()
    kp = [c["k"] for c in res["cells"] if c["retained"] >= 0.98]
    res["kstar"] = min(kp) if kp else ">44"
    json.dump(res, open(os.path.expanduser("~/f3cache/net76_results.json"), "w"), indent=1)
    print(f"[KSTAR fr@512 extended] k* = {res['kstar']}", flush=True)
    print("\nALL_DONE_NET76", flush=True)

if __name__ == "__main__":
    main()

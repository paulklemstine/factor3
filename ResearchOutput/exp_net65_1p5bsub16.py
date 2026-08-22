#!/usr/bin/env python3
# NET-65 — THE 1.5B SUB-16 ADDENDUM AT 1024 (limited-memory axis, iteration 26)
# NET-55 measured the 1.5B knee at ctx=1024 as k*=16 but the grid FLOOR was 16 — sub-16
# was unmeasured. If any point in {4,8,12} passes, the knee DECLINES with model scale
# (strengthening size-invariance into size-DECREASING); if none passes, 16 is exact.
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 SCALE-DECLINE: some point in {4, 8, 12} passes -> 1.5B knee < 16 < 0.5B's 20
#     (bigger models need FEWER keys).
#  P2 SIXTEEN-IS-REAL: all of {4, 8, 12} fail -> k*(1024)=16 exact, identical to nothing
#     else in the chain (0.5B reads 20) — scale-shifted but not monotone-declining.
import json, math, os, time
import torch
import torch.nn.functional as F

src = open("/home/raver1975/factor3/ResearchOutput/exp_net55_1p5b_knee.py").read()
src = src.replace('if __name__ == "__main__":\n    main()', "")
g = {}
exec(compile(src, "e55", "exec"), globals())
# brings: floatify_linears, Runner, rotate_half, repeat_kv, MODEL_DIR, CORPUS

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

    # gate vs HF bf16 reference captured PRE-floatify (real text)
    with torch.no_grad():
        vb = held[:128].view(1, -1)
        ref = model(input_ids=vb).logits.float()
        assert torch.isfinite(ref).all(), "bf16 HF reference non-finite"
        n_lin = floatify_linears(model)
        print(f"[floatify] replaced {n_lin} linears", flush=True)
        h = runner.forward(vb)
        mine = model.lm_head(h).float()
        agree = float((ref.argmax(-1) == mine.argmax(-1)).float().mean())
        ce_r = F.cross_entropy(ref[:, :-1].reshape(-1, ref.size(-1)), vb[:, 1:].reshape(-1)).item()
        ce_m = F.cross_entropy(mine[:, :-1].reshape(-1, mine.size(-1)), vb[:, 1:].reshape(-1)).item()
        print(f"[validate] argmax-agree={agree:.4f} CE ref={ce_r:.4f} mine={ce_m:.4f}", flush=True)
        assert agree >= 0.85 and abs(ce_r - ce_m) < 0.02, "own forward diverges"
    del ref, mine
    torch.cuda.empty_cache()

    CTX, NW = 1024, 24
    wl = CTX + 1
    win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]

    @torch.no_grad()
    def ev(k):
        ces, corr, tot = 0.0, 0, 0
        t0 = time.time()
        for s in range(0, len(win), 2):
            b = torch.cat(win[s:s+2], dim=0)
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
        return ces/tot, corr/tot, time.time()-t0

    full_ce, full_acc, _ = ev(None)
    base = max(full_acc, 1e-9)
    print(f"[full ] acc={full_acc:.4f} ce={full_ce:.4f} (nw={len(win)})", flush=True)
    res = {"model": "Qwen2.5-1.5B", "ctx": CTX, "nw": len(win),
           "full_acc": round(full_acc, 5), "cells": []}
    json.dump(res, open(os.path.expanduser("~/f3cache/net65_results.json"), "w"), indent=1)
    for k in (4, 6, 8, 12):
        ce, acc, dt = ev(k)
        ret = acc/base
        print(f"[k={k:<5}] ret={ret:.4f} {'PASS' if ret>=0.98 else 'fail'} "
              f"ce={ce:.4f} ({dt:.0f}s)", flush=True)
        res["cells"].append({"k": k, "retained": round(ret, 5)})
        json.dump(res, open(os.path.expanduser("~/f3cache/net65_results.json"), "w"), indent=1)
        torch.cuda.empty_cache()
    kp = [c["k"] for c in res["cells"] if c["retained"] >= 0.98]
    res["kstar"] = min(kp) if kp else None
    json.dump(res, open(os.path.expanduser("~/f3cache/net65_results.json"), "w"), indent=1)
    print(f"[KSTAR 1.5B ctx=1024 sub-16] k* = {res['kstar']} (16 stands if None)", flush=True)
    print("\nALL_DONE_NET65", flush=True)

if __name__ == "__main__":
    main()

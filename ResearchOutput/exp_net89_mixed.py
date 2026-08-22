#!/usr/bin/env python3
# NET-89 — THE MIXED-DOMAIN KNEE (limited-memory axis, iteration 63)
# Real agentic workloads mix code AND prose in the same context window. All prior
# rounds measured single-domain knees. This round creates a MIXED corpus (50/50
# code + English prose interleaved) and measures its knee.
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 MIXED-IS-AVERAGE: knee(mixed) ≈ midpoint of code(12) and prose(20) ≈ 14–18.
#  P2 HARDER-DOMINATES: knee(mixed) follows the higher-knee domain (prose) ≈ 16–20.
#  P3 ATTENTION-FOLLOWS-CONTENT: within the mixed sequence, code segments show lower
#     per-row entropy than prose segments — the model adapts locally.
import json, math, os, time
import torch
import torch.nn.functional as F

src = open("/home/raver1975/factor3/ResearchOutput/exp_net68_domainjump.py").read()
src = src.replace('if __name__ == "__main__":\n    main()', "")
g = {}
exec(compile(src, "e68", "exec"), g)
globals().update(g)

CODE_CACHE = os.path.expanduser("~/f3cache/code_corpus.txt")
PROSE_CACHE = os.path.expanduser("~/f3cache/net49_corpus.txt")
CTX, NW, BS = 1024, 24, 2

def make_mixed_corpus():
    """Interleave code and prose blocks of ~200 tokens each."""
    code_t = open(CODE_CACHE, encoding="utf-8").read()[:2_000_000]
    prose_t = open(PROSE_CACHE, encoding="utf-8").read()[:2_000_000]
    # split into chunks
    def chunk(t, size=500):
        return [t[i:i+size] for i in range(0, len(t)-size, size)]
    code_chunks = chunk(code_t)
    prose_chunks = chunk(prose_t)
    mixed = []
    for i in range(min(len(code_chunks), len(prose_chunks))):
        mixed.append(prose_chunks[i])
        mixed.append(code_chunks[i])
    result = "\n\n".join(mixed)
    out = os.path.expanduser("~/f3cache/mixed_corpus.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write(result); f.flush(); os.fsync(f.fileno())
    print(f"[mixed] {len(result)} chars from {len(code_chunks)}+{len(prose_chunks)} blocks",
          flush=True)
    return result

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_DIR, dtype=torch.float32,
        attn_implementation="eager").cuda().eval()
    runner = Runner(model)

    mixed_text = make_mixed_corpus()
    ids_all = torch.tensor(tok(mixed_text, add_special_tokens=False).input_ids,
                           dtype=torch.long)
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

    res = {"domain": "mixed-code-prose", "cells": []}
    for ctx in CTXS:
        wl = ctx + 1
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
                    tt = tgt[:, s2:e2].reshape(-1)
                    ces += F.cross_entropy(lg, tt, reduction="sum").item()
                    corr += (lg.argmax(-1) == tt).sum().item()
                tot += n
            return ces/tot, corr/tot, time.time()-t0

        full_ce, full_acc, _ = ev(None)
        base = max(full_acc, 1e-9)
        print(f"\n[CTX={ctx}] full acc={full_acc:.4f} ce={full_ce:.4f}", flush=True)
        grid = {512: [4,8,12,16,20], 1024: [8,12,16,20,24]}[ctx]
        for k in grid:
            ce, acc, dt = ev(k)
            ret = acc/base
            print(f"[k={k:<5}] ret={ret:.4f} {'PASS' if ret>=0.98 else 'fail'}", flush=True)
            res["cells"].append({"ctx": ctx, "k": k, "retained": round(ret, 5)})
            json.dump(res,
                      open(os.path.expanduser("~/f3cache/net89_results.json"), "w"),
                      indent=1)
            torch.cuda.empty_cache()
        kp = [c["k"] for c in res["cells"] if c["ctx"] == ctx and c["retained"] >= 0.98]
        res[f"kstar_ctx{ctx}"] = min(kp) if kp else None
        json.dump(res,
                  open(os.path.expanduser("~/f3cache/net89_results.json"), "w"), indent=1)
        print(f"[KSTAR mixed@{ctx}] k* = {res[f'kstar_ctx{ctx}']}", flush=True)

    # reference: pure-domain knees for comparison
    res["reference"] = {
        "code_512": 12, "code_1024": 16,
        "prose_en_512": 16, "prose_en_1024": 20,
    }
    json.dump(res,
              open(os.path.expanduser("~/f3cache/net89_results.json"), "w"), indent=1)
    print("\nALL_DONE_NET89", flush=True)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# NET-59 — THE LOAD-BEARING MAP (limited-memory axis, iteration 13)
# Open since NET-49: WHICH layers' attention is actually load-bearing? Prune ONE layer at a
# time with oracle top-k at fixed budgets {16, 32}; measure retained accuracy per layer.
# Complements the correlational depth maps (eff-support, Maslov gap, decision divergence)
# with a causal per-layer measurement. Also: prune ALL-EXCEPT-one layer as the complement.
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 TAIL-IS-CRITICAL: pruning L22 or L23 alone at k=16 costs more than pruning any other
#     single layer (the diffuse-tail thread becomes causal).
#  P2 MID-STACK-IS-CHEAP: there exists a mid-stack layer whose solo-k=16 pruning is nearly
#     free (>= 0.99 retained) — hyper-concentrated layers (L16, eff ~3) are the candidates.
#  P3 NON-UNIFORM-MAP: the per-layer cost profile is non-uniform (max-min spread >= 3%
#     retained at k=16).
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
CTX, NW, BS = 512, 24, 4

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

    # gate
    with torch.no_grad():
        vb = held[:128].view(1, -1)
        ref = model(input_ids=vb).logits.float()
        mine = model.lm_head(runner.forward_oracle(vb)).float()
        agree = float((ref.argmax(-1) == mine.argmax(-1)).float().mean())
        print(f"[validate] argmax-agree={agree:.4f}", flush=True)
        assert agree >= 0.999

    wl = CTX + 1
    win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]

    @torch.no_grad()
    def ev(layer_k=None):
        """layer_k: dict layer_index -> k applied ONLY to that layer; others full."""
        ces, corr, tot = 0.0, 0, 0
        for s in range(0, len(win), BS):
            b = torch.cat(win[s:s+BS], dim=0)
            h = runner.forward_layerk(b, layer_k)
            tgt = b[:, 1:]
            n = b.size(0)*(b.size(1)-1)
            V = model.config.vocab_size
            for s2 in range(0, b.size(1)-1, 128):
                e2 = min(s2+128, b.size(1)-1)
                lg = model.lm_head(h[:, s2:e2]).reshape(-1, V).float()
                t = tgt[:, s2:e2].reshape(-1)
                ces += F.cross_entropy(lg, t, reduction="sum").item()
                corr += (lg.argmax(-1) == t).sum().item()
            tot += n
        return ces/tot, corr/tot

    full_ce, full_acc = ev()
    base = max(full_acc, 1e-9)
    print(f"[full ] acc={full_acc:.4f} ce={full_ce:.4f}", flush=True)
    res = {"ctx": CTX, "nw": len(win), "full_acc": round(full_acc, 5), "solo": {}, "rest": {}}

    NL = len(model.model.layers)
    for K in (16, 32):
        prof = []
        t0 = time.time()
        for li in range(NL):
            ce, acc = ev({li: K})
            ret = acc/base
            prof.append(round(ret, 5))
            res["solo"][f"k{K}_L{li}"] = round(ret, 5)
            print(f"[solo k={K} L{li:<3}] ret={ret:.4f}", flush=True)
        res[f"solo_profile_k{K}"] = prof
        smax, smin = max(prof), min(prof)
        worst = prof.index(smin)
        print(f"[k={K}] spread: best={smax:.4f} (L{prof.index(smax)}) "
              f"worst={smin:.4f} (L{worst}) spread={(smax-smin)*100:.1f} pts ({time.time()-t0:.0f}s)", flush=True)
        json.dump(res, open(os.path.expanduser("~/f3cache/net59_results.json"), "w"), indent=1)
        torch.cuda.empty_cache()

    print("\nALL_DONE_NET59", flush=True)

if __name__ == "__main__":
    main()

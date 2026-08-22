#!/usr/bin/env python3
# NET-60 — LOCATING THE EPISTASIS (limited-memory axis, iteration 16)
# NET-59: solo-layer top-k is free everywhere (spread 0.6 pts). NET-50: joint all-layer
# costs 1.7%. NET-54: swapping the tail breaks agreement with both parents. WHERE does the
# interaction live? This round prunes PAIRS/triples at k=16/layer and compares against the
# solo profile (~/f3cache/net59_results.json).
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 TAIL-PAIR-IS-SPECIAL: pruning {L22,L23} jointly at k=16 costs MORE than any tested
#     bulk pair at the same budget (the epistasis lives in the tail pair itself).
#  P2 SUB-ADDITIVE-EVERYWHERE: every pair costs less than the sum of its solo costs.
#  P3 TAIL-TRIPLE-COMPOUNDS: adding a third tail layer {L21,L22,L23} costs more than twice
#     the best pair cost (interaction grows with tail depth).
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
    def ev(layer_k):
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

    full_ce, full_acc = ev({})
    base = max(full_acc, 1e-9)
    print(f"[full ] acc={full_acc:.4f}", flush=True)
    res = {"ctx": CTX, "nw": len(win), "full_acc": round(full_acc, 5), "pairs": {}}

    # solo costs from NET-59 (same harness/window count)
    solo = json.load(open(os.path.expanduser("~/f3cache/net59_results.json")))["solo_profile_k16"]

    arms = {
        "tail_22_23": [22, 23],
        "bulk_12_15": [12, 15],      # the two worst solo layers from NET-59
        "front_0_1": [0, 1],
        "mid_10_11": [10, 11],
        "cross_22_12": [22, 12],     # tail + worst bulk
        "triple_21_22_23": [21, 22, 23],
    }
    for name, layers in arms.items():
        lk = {li: 16 for li in layers}
        ce, acc = ev(lk)
        ret = acc/base
        solo_sum_pts = sum((1 - solo[li]) * 100 for li in layers)
        pair_cost_pts = (1 - ret) * 100
        res["pairs"][name] = {"layers": layers, "retained": round(ret, 5),
                              "cost_pts": round(pair_cost_pts, 3),
                              "solo_sum_pts": round(solo_sum_pts, 3),
                              "superadditive": bool(pair_cost_pts > solo_sum_pts)}
        json.dump(res, open(os.path.expanduser("~/f3cache/net60_results.json"), "w"), indent=1)
        sa = "SUPER" if pair_cost_pts > solo_sum_pts else "sub"
        print(f"[{name:<18}] ret={ret:.4f} cost={pair_cost_pts:.2f}pts "
              f"soloSum={solo_sum_pts:.2f}pts [{sa}]", flush=True)
        torch.cuda.empty_cache()

    print("\nALL_DONE_NET60", flush=True)

if __name__ == "__main__":
    main()

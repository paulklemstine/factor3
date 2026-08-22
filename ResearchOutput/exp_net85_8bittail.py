#!/usr/bin/env python3
# NET-85 — THE 8-BIT TAIL: DOES MORE PRECISION HELP FURTHER? (limited-memory axis,
# iteration 57) NET-84 showed tail-aware mixed precision works (+1.8 pts). This tests
# whether 8-bit (instead of fp32) for the tail is sufficient, reducing memory overhead.
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 EIGHT-BIT-SUFFICES: 8-bit tail ≈ fp32 tail (within 0.5 pts) — the tail needs
#     HIGHER-than-4-bit precision but not full fp32.
#  P2 MONOTONE-PRECISION: quality ordering = fp32-tail > 8-bit-tail > 4-bit-full.
import json, math, os, time, copy
import torch
import torch.nn.functional as F

src = open("/home/raver1975/factor3/ResearchOutput/exp_net56_policy.py").read()
src = src.replace('if __name__ == "__main__":\n    main()', "")
g = {}
exec(compile(src, "e56", "exec"), g)
Runner = g["Runner"]

MODEL_DIR = os.path.expanduser("~/f3cache/qwen25-05b")
CORPUS = os.path.expanduser("~/f3cache/net49_corpus.txt")
CTX, NW, BS = 1024, 24, 2
LIN = ("q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj")
ATT = ("q_proj", "k_proj", "v_proj", "o_proj")

def rtn_quant(W, bits, group=128):
    W = W.float()
    qmax = 2 ** (bits - 1) - 1
    Wq = torch.zeros_like(W)
    for s in range(0, W.shape[1], group):
        e = min(s + group, W.shape[1])
        blk = W[:, s:e]
        amax = blk.abs().amax(dim=1, keepdim=True).clamp_min(1e-10)
        scale = amax / qmax
        Wq[:, s:e] = (blk / scale).round().clamp(-qmax, qmax) * scale
    return Wq

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    text = open(CORPUS, encoding="utf-8").read()[:4_000_000]
    ids_all = torch.tensor(tok(text, add_special_tokens=False).input_ids,
                           dtype=torch.long)
    split = int(0.9 * len(ids_all))
    held = ids_all[split:].cuda()

    wl = CTX + 1
    win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]

    model_full = AutoModelForCausalLM.from_pretrained(
        MODEL_DIR, dtype=torch.float32,
        attn_implementation="eager").cuda().eval()
    runner = Runner(model_full)

    with torch.no_grad():
        vb = held[:128].view(1, -1).cuda()
        ref = model_full(input_ids=vb).logits.float()
        mine = model_full.lm_head(runner.forward_oracle(vb)).float()
        agree = float((ref.argmax(-1) == mine.argmax(-1)).float().mean())
        print(f"[validate] argmax-agree={agree:.4f}", flush=True)
        assert agree >= 0.999
    del ref, mine
    torch.cuda.empty_cache()

    def ev(mod):
        ces, corr, tot = 0.0, 0, 0
        for s in range(0, len(win), BS):
            b = torch.cat(win[s:s+BS], dim=0)
            h = runner.forward_oracle(b)
            tgt = b[:, 1:]
            n = b.size(0)*(b.size(1)-1)
            V = model_full.config.vocab_size
            for s2 in range(0, b.size(1)-1, 64):
                e2 = min(s2+64, b.size(1)-1)
                lg = model_full.lm_head(h[:, s2:e2]).reshape(-1, V).float()
                t = tgt[:, s2:e2].reshape(-1)
                ces += F.cross_entropy(lg, t, reduction="sum").item()
                corr += (lg.argmax(-1) == t).sum().item()
            tot += n
        return ces/tot, corr/tot

    full_ce, full_acc = ev(model_full)
    base = max(full_acc, 1e-9)
    print(f"[full ] acc={full_acc:.4f}", flush=True)
    res = {"ctx": CTX, "nw": len(win), "full_acc": round(full_acc, 5), "arms": []}

    import copy as cp

    # Arm 1: full 4-bit GPTQ (reference)
    mq4 = cp.deepcopy(model_full)
    for layer in mq4.model.layers:
        for nm in LIN:
            mod = layer.self_attn if nm in ATT else layer.mlp
            lin = getattr(mod, nm)
            lin.weight.data = rtn_quant(lin.weight.data, bits=4, group=128)
    old_m, old_l = runner.m, runner.layers
    runner.m = mq4; runner.layers = mq4.model.layers
    ce, acc = ev(mq4)
    ret = acc/base
    res["arms"].append({"arm": "rtn4_full", "retained": round(ret, 5)})
    print(f"[rtn4_full            ] ret={ret:.4f}", flush=True)
    runner.m = old_m; runner.layers = old_l
    del mq4; torch.cuda.empty_cache()

    # Arm 2: mixed — all 4-bit except L22/L23 at 8-bit
    mq8 = cp.deepcopy(model_full)
    for li, layer in enumerate(mq8.model.layers):
        for nm in LIN:
            mod = layer.self_attn if nm in ATT else layer.mlp
            lin = getattr(mod, nm)
            bits = 8 if li in (22, 23) else 4
            lin.weight.data = rtn_quant(lin.weight.data, bits=bits, group=128)
    old_m, old_l = runner.m, runner.layers
    runner.m = mq8; runner.layers = mq8.model.layers
    ce, acc = ev(mq8)
    ret = acc/base
    res["arms"].append({"arm": "mixed_8bit_tail", "retained": round(ret, 5)})
    print(f"[mixed_8bit_tail      ] ret={ret:.4f}", flush=True)
    runner.m = old_m; runner.layers = old_l
    del mq8; torch.cuda.empty_cache()

    # Arm 3: mixed — all 4-bit except L22/L23 at 6-bit
    mq6 = cp.deepcopy(model_full)
    for li, layer in enumerate(mq6.model.layers):
        for nm in LIN:
            mod = layer.self_attn if nm in ATT else layer.mlp
            lin = getattr(mod, nm)
            bits = 6 if li in (22, 23) else 4
            lin.weight.data = rtn_quant(lin.weight.data, bits=bits, group=128)
    old_m, old_l = runner.m, runner.layers
    runner.m = mq6; runner.layers = mq6.model.layers
    ce, acc = ev(mq6)
    ret = acc/base
    res["arms"].append({"arm": "mixed_6bit_tail", "retained": round(ret, 5)})
    print(f"[mixed_6bit_tail      ] ret={ret:.4f}", flush=True)
    runner.m = old_m; runner.layers = old_l
    del mq6; torch.cuda.empty_cache()

    json.dump(res, open(os.path.expanduser("~/f3cache/net85_results.json"), "w"), indent=1)

    # summary
    r4 = res["arms"][0]["retained"]
    r8 = res["arms"][1]["retained"]
    r6 = res["arms"][2]["retained"]
    print(f"\n[PRECISION LADDER] 4-bit-all={r4:.4f} | "
          f"6-bit-tail={r6:.4f} | 8-bit-tail={r8:.4f} | full=1.0000", flush=True)
    print("ALL_DONE_NET85", flush=True)

if __name__ == "__main__":
    main()

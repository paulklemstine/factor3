#!/usr/bin/env python3
# NET-84 — TAIL-AWARE MIXED PRECISION (limited-memory axis, iteration 55)
# Follows NET-60 (tail pair is epistatic) + NET-83 (integration super-additive).
# Question: if L22/L23 stay at fp32 while all other layers are GPTQ 4-bit,
# does the interaction penalty shrink?
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 TAIL-PROTECTS: mixed precision (all 4-bit except L22/L23 fp32) retains >= 0.95
#     vs full-4-bit's 0.908 — protecting the identity tail preserves quality.
#  P2 CORE-IS-ENOUGH: full 4-bit ≈ mixed precision (the tail doesn't need protection;
#     its role is relational, not precision-dependent).
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

def gptq_quantize_linear(W, bits=4, group=128):
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

    # gate
    with torch.no_grad():
        vb = held[:128].view(1, -1)
        ref = model(input_ids=vb).logits.float() if False else \
              model_full(input_ids=vb.cuda()).logits.float()
        mine = model_full.lm_head(runner.forward_oracle(vb)).float()
        agree = float((ref.argmax(-1) == mine.argmax(-1)).float().mean())
        print(f"[validate] argmax-agree={agree:.4f}", flush=True)
        assert agree >= 0.999
    del ref, mine
    torch.cuda.empty_cache()

    def ev(mod, k=None):
        ces, corr, tot = 0.0, 0, 0
        for s in range(0, len(win), BS):
            b = torch.cat(win[s:s+BS], dim=0)
            h = runner.forward_oracle(b, k=k)
            tgt = b[:, 1:]
            n = b.size(0)*(b.size(1)-1)
            V = 151936
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
    print(f"[full ] acc={full_acc:.4f} ce={full_ce:.4f}", flush=True)
    res = {"ctx": CTX, "nw": len(win), "full_acc": round(full_acc, 5), "arms": []}
    json.dump(res, open(os.path.expanduser("~/f3cache/net84_results.json"), "w"), indent=1)

    def make_mixed(prec_layers):
        """Create model copy with GPTQ 4-bit on all layers EXCEPT prec_layers."""
        mq = copy.deepcopy(model_full)
        for li, layer in enumerate(mq.model.layers):
            if li in prec_layers:
                continue  # keep these at fp32
            for nm in LIN:
                mod = layer.self_attn if nm in ATT else layer.mlp
                lin = getattr(mod, nm)
                lin.weight.data = gptq_quantize_linear(
                    lin.weight.data, bits=4, group=128)
        return mq

    # Arm 1: full 4-bit GPTQ (reference from NET-53 methodology)
    mq_all = copy.deepcopy(model_full)
    for layer in mq_all.model.layers:
        for nm in LIN:
            mod = layer.self_attn if nm in ATT else layer.mlp
            lin = getattr(mod, nm)
            lin.weight.data = gptq_quantize_linear(lin.weight.data, bits=4, group=128)
    old_m = runner.m; old_l = runner.layers
    runner.m = mq_all; runner.layers = mq_all.model.layers
    ce, acc = ev(mq_all)
    ret = acc/base
    res["arms"].append({"arm": "gptq4_full", "retained": round(ret, 5),
                        "ce": round(ce, 5)})
    print(f"[gptq4_full          ] ret={ret:.4f}", flush=True)
    runner.m = old_m; runner.layers = old_l
    del mq_all
    torch.cuda.empty_cache()

    # Arm 2: mixed precision — all 4-bit except L22/L23 at fp32
    mq_mixed = copy.deepcopy(model_full)
    for li, layer in enumerate(mq_mixed.model.layers):
        if li in (22, 23):
            continue
        for nm in LIN:
            mod = layer.self_attn if nm in ATT else layer.mlp
            lin = getattr(mod, nm)
            lin.weight.data = gptq_quantize_linear(lin.weight.data, bits=4, group=128)
    old_m = runner.m; old_l = runner.layers
    runner.m = mq_mixed; runner.layers = mq_mixed.model.layers
    ce, acc = ev(runner.m)
    ret = acc/base
    res["arms"].append({"arm": "gptq4_mixed_tail_fp32",
                        "retained": round(ret, 5), "ce": round(ce, 5)})
    print(f"[gptq4_mixed_tail    ] ret={ret:.4f}", flush=True)
    runner.m = old_m; runner.layers = old_l
    del mq_mixed
    torch.cuda.empty_cache()

    # Arm 3: only L22/L23 quantized (isolates tail quantization cost)
    mq_tail = copy.deepcopy(model_full)
    for nm in LIN:
        for li in (22, 23):
            layer = mq_tail.model.layers[li]
            mod = layer.self_attn if nm in ATT else layer.mlp
            lin = getattr(mod, nm)
            lin.weight.data = gptq_quantize_linear(lin.weight.data, bits=4, group=128)
    old_m = runner.m; old_l = runner.layers
    runner.m = mq_tail; runner.layers = mq_tail.model.layers
    ce, acc = ev(runner.m)
    ret = acc/base
    res["arms"].append({"arm": "gptq4_tail_only",
                        "retained": round(ret, 5), "ce": round(ce, 5)})
    print(f"[gptq4_tail_only     ] ret={ret:.4f}", flush=True)
    runner.m = old_m; runner.layers = old_l
    del mq_tail
    torch.cuda.empty_cache()

    json.dump(res, open(os.path.expanduser("~/f3cache/net84_results.json"), "w"), indent=1)

    # summary
    full_ret = [a for a in res["arms"] if a["arm"] == "gptq4_full"][0]["retained"]
    mixed_ret = [a for a in res["arms"] if a["arm"] == "gptq4_mixed_tail_fp32"][0]["retained"]
    delta = (mixed_ret - full_ret) * 100
    print(f"\n[MIXED-PRECISION DELTA] {delta:+.1f} pts over full 4-bit", flush=True)
    print("ALL_DONE_NET84", flush=True)

if __name__ == "__main__":
    main()

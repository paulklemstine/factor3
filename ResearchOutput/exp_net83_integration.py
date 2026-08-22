#!/usr/bin/env python3
# NET-83 — THE INTEGRATION TEST (limited-memory axis, iteration 53)
# Combines the two best optimizations into one measurement:
#   Weight axis: GPTQ 4-bit group-128 (+0.15 dCE from NET-53)
#   Attention axis: oracle top-k at k={16, 20, 24} (knees from NET-50/62/63)
# Question: do the degradations add, multiply, or cancel?
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 SUB-ADDITIVE: combined degradation < sum of individual degradations
#     (quantization errors partially absorbed by sparse attention).
#  P2 SUPER-ADDITIVE: combined > sum (sparse attention amplifies quantization noise).
#  P3 INDEPENDENT: combined ≈ sum (the two axes are orthogonal).
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
CTX, NW, BS = 1024, 24, 2
LIN = ("q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj")
ATT = ("q_proj", "k_proj", "v_proj", "o_proj")

def gptq_quantize_linear(W, bits=4, group=128, damp=0.01):
    """Simplified per-group GPTQ on weight tensor."""
    W = W.float()
    out_f, in_f = W.shape
    # approximate Hessian as identity * mean (simplified but captures the spirit)
    qmax = 2 ** (bits - 1) - 1
    Wq = torch.zeros_like(W)
    for s in range(0, in_f, group):
        e = min(s + group, in_f)
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
    model = model_full
    runner = Runner(model_full)

    # gate
    with torch.no_grad():
        vb = held[:128].view(1, -1)
        ref = model_full(input_ids=vb).logits.float()
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
            V = model_full.config.vocab_size
            for s2 in range(0, b.size(1)-1, 64):
                e2 = min(s2+64, b.size(1)-1)
                lg = model.lm_head(h[:, s2:e2]).reshape(-1, V).float()
                t = tgt[:, s2:e2].reshape(-1)
                ces += F.cross_entropy(lg, t, reduction="sum").item()
                corr += (lg.argmax(-1) == t).sum().item()
            tot += n
        return ces/tot, corr/tot

    full_ce, full_acc = ev(model_full)
    base = max(full_acc, 1e-9)
    print(f"[full ] acc={full_acc:.4f} ce={full_ce:.4f}", flush=True)
    res = {"ctx": CTX, "nw": len(win), "full_acc": round(full_acc, 5),
           "full_ce": round(full_ce, 5), "arms": []}
    json.dump(res, open(os.path.expanduser("~/f3cache/net83_results.json"), "w"), indent=1)

    def measure(name, k=None):
        ce, acc = ev(model_full, k=k)
        ret = acc/base
        res["arms"].append({"arm": name, "k": k, "retained": round(ret, 5),
                            "ce": round(ce, 5)})
        json.dump(res, open(os.path.expanduser("~/f3cache/net83_results.json"), "w"),
                  indent=1)
        print(f"[{name:<28}] ret={ret:.4f} ce={ce:.4f}", flush=True)
        torch.cuda.empty_cache()

    # Arm 1: attention-only knees
    for k in (16, 20, 24):
        measure(f"attn_k{k}", k=k)

    # Arm 2: weight-only GPTQ 4-bit (no attention pruning)
    import copy
    mq = copy.deepcopy(model_full)
    for layer in mq.model.layers:
        for nm in LIN:
            mod = layer.self_attn if nm in ATT else layer.mlp
            getattr(mod, nm).weight.data = gptq_quantize_linear(
                getattr(mod, nm).weight.data, bits=4, group=128)
    print(f"[gptq4_only] weights modified", flush=True)
    old_m = runner.m
    old_layers = runner.layers
    runner.m = mq
    runner.layers = mq.model.layers
    ce, acc = ev(mq)
    ret = acc/base
    res["arms"].append({"arm": "gptq4_only", "retained": round(ret, 5),
                        "ce": round(ce, 5)})
    json.dump(res, open(os.path.expanduser("~/f3cache/net83_results.json"), "w"), indent=1)
    print(f"[gptq4_only                 ] ret={ret:.4f} ce={ce:.4f}", flush=True)
    runner.m = old_m
    runner.layers = old_layers
    del mq
    torch.cuda.empty_cache()

    # Arm 3: GPTQ 4-bit + top-k attention (THE INTEGRATION TEST)
    for k in (16, 20, 24):
        mq = copy.deepcopy(model_full)
        w_changed = 0.0
        for layer in mq.model.layers:
            for nm in LIN:
                mod = layer.self_attn if nm in ATT else layer.mlp
                lin = getattr(mod, nm)
                old_w = lin.weight.data.clone()
                lin.weight.data = gptq_quantize_linear(
                    lin.weight.data, bits=4, group=128)
                w_changed += float((lin.weight.data - old_w).abs().sum())
        print(f"  [gptq k={k}] total |dW| = {w_changed:.4f}", flush=True)
        old_m = runner.m
        old_layers = runner.layers
        runner.m = mq
        runner.layers = mq.model.layers
        ce, acc = ev(mq, k=k)
        runner.m = old_m
        runner.layers = old_layers
        ret = acc/base
        res["arms"].append({"arm": f"gptq4_attn_k{k}", "k": k,
                            "retained": round(ret, 5), "ce": round(ce, 5),
                            "w_changed": round(w_changed, 4)})
        json.dump(res, open(os.path.expanduser("~/f3cache/net83_results.json"), "w"),
                  indent=1)
        print(f"[gptq4_attn_k{k:<5}    ] ret={ret:.4f} ce={ce:.4f}", flush=True)
        del mq
        torch.cuda.empty_cache()

    print("\nALL_DONE_NET83", flush=True)

if __name__ == "__main__":
    main()

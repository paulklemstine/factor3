#!/usr/bin/env python3
# NET-52 — QUANTIZATION FLOORS vs THE 2Lr DEFECT BAND (limited-memory axis, iteration 4)
# Mined from the Lean catalogue: "Arithmetic Geometry of Quantized Weight Lattices" —
# quantizing weights under an L-Lipschitz convex loss deforms the landscape inequality by
# at most 2Lr (mesh r), the optimum moves <= Lr, basins preserved, constant SHARP (no
# exact convexity at any positive mesh). This round measures where a REAL LM actually
# sits relative to monotone mesh growth, and whether the toy programme's compression
# floor (per-channel uniform-4 optimal, NOT depth-robust — NET-11/14/18) transfers.
#
# Protocol: RTN symmetric per-output-row quantization of ALL linear weights
# (q/k/v/o/gate/up/down), fp32 master, same eval harness/gates as NET-49/50
# (40 held-out windows, ctx=512, retained-acc + CE).
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 REAL-4-BIT-NEAR-FLOOR: per-channel 4-bit costs DeltaCE <= 0.05 at ctx=512
#     (the toy per-channel-uniform-4 optimum transfers to a real pretrained LM).
#  P2 DEPTH-GRADIENT: quantizing ONLY the last 12 layers hurts MORE than only the
#     first 12 (toy NET-18: deeper = worse compounding; the floor is not depth-robust).
#  P3 TWO-BIT-COLLAPSE: 2-bit DeltaCE >= 0.5 (near-destruction).
#  P4 MONOTONE-MESH: DeltaCE is monotone non-decreasing as mesh grows (8->2 bits),
#     with 8-bit already measurably nonzero (sharpness of the 2Lr band: no flat region).
import copy, json, math, time
import torch
import torch.nn.functional as F

BASE = "/tmp/qwen25-05b"
CTX = 512
NW = 40
LIN = ("q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj")

def rtn_(lin, bits, group=None):
    W = lin.weight.data
    qmax = 2 ** (bits - 1) - 1
    if group is None:
        amax = W.abs().amax(dim=1, keepdim=True)
        scale = (amax / qmax).clamp_min(1e-12)
        lin.weight.data = (W / scale).round().clamp(-qmax, qmax) * scale
    else:
        g = group
        R, C = W.shape
        pad = (g - C % g) % g
        Wp = F.pad(W, (0, pad))
        amax = Wp.abs().view(R, -1, g).amax(dim=2, keepdim=True)
        scale = (amax / qmax).clamp_min(1e-12)
        Wq = ((Wp.view(R, -1, g)) / scale).round().clamp(-qmax, qmax) * scale
        lin.weight.data = Wq.view(R, -1)[:, :C]

def quantize(model, bits, layers=None, group=None):
    ATT = ("q_proj", "k_proj", "v_proj", "o_proj")
    for li, layer in enumerate(model.model.layers):
        if layers is not None and li not in layers:
            continue
        for name in LIN:
            mod = layer.self_attn if name in ATT else layer.mlp
            rtn_(getattr(mod, name), bits, group)

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(BASE)
    master = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.float32,
                                                  attn_implementation="eager").eval()
    text = open("/tmp/net49_corpus.txt", encoding="utf-8").read()[:4_000_000]
    ids_all = torch.tensor(tok(text, add_special_tokens=False).input_ids, dtype=torch.long)
    split = int(0.9 * len(ids_all))
    held = ids_all[split:].cuda()
    wl = CTX + 1
    win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]

    # reuse the validated NET-49 Runner for identical measurement semantics
    src = open("/tmp/exp_net49_qwen_topk.py").read().replace(
        'if __name__ == "__main__":\n    main()', "")
    g = {}
    exec(compile(src, "e49", "exec"), g)
    Runner = g["Runner"]

    def ev(runner):
        ces, corr, tot = 0.0, 0, 0
        for s in range(0, len(win), 4):
            batch = torch.cat(win[s:s+4], dim=0)
            ce, ac = runner.loss_acc(batch)
            n = batch.size(0) * (batch.size(1) - 1)
            ces += ce * n; corr += ac * n; tot += n
        return ces / tot, corr / tot

    mfull = copy.deepcopy(master).cuda()
    full_ce, full_acc = ev(Runner(mfull))
    del mfull; torch.cuda.empty_cache()
    print(f"[full ] acc={full_acc:.4f} ce={full_ce:.4f}", flush=True)
    res = {"ctx": CTX, "nw": len(win), "full_ce": full_ce, "full_acc": full_acc, "arms": []}

    def arm(name, bits, layers=None, group=None):
        t0 = time.time()
        m2 = copy.deepcopy(master).cuda()
        quantize(m2, bits, layers, group)
        ce, acc = ev(Runner(m2))
        row = dict(arm=name, bits=bits, layers=sorted(layers) if layers else None,
                   group=group, ce=round(ce, 5), acc=round(acc, 5),
                   d_ce=round(ce - full_ce, 5), ret_acc=round(acc / full_acc, 5),
                   secs=round(time.time() - t0))
        res["arms"].append(row)
        json.dump(res, open("/tmp/net52_results.json", "w"), indent=1)
        print(f"[{name:<14}] ce={ce:.4f} dCE={ce-full_ce:+.4f} acc={acc:.4f} "
              f"ret={acc/full_acc:.4f} ({row['secs']}s)", flush=True)
        del m2
        torch.cuda.empty_cache()

    for b in (8, 6, 5, 4, 3, 2):
        arm(f"b{b}_perchannel", b)
    arm("b4_first12", 4, layers=set(range(12)))
    arm("b4_last12", 4, layers=set(range(12, 24)))
    arm("b4_group128", 4, group=128)
    arm("b3_group128", 3, group=128)

    print("\nALL_DONE_NET52", flush=True)
    json.dump(res, open("/tmp/net52_results.json", "w"), indent=1)

if __name__ == "__main__":
    main()

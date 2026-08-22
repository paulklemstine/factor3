#!/usr/bin/env python3
# NET-79 — THE 1.5B AT 4096: DOES SCALE DELAY THE PHASE TRANSITION? (limited-memory
# axis, iteration 53) NET-78 found the 0.5B increment accelerates 4× at 4096 (+4→+16).
# NET-66 established that scale delays context-sensitivity by one doubling. If the delay
# applies to the ACCELERATION too, the 1.5B @4096 knee should be ~28 (the delayed +4
# increment), not ~56 (the accelerated +16 applied at 1.5B's scale).
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 SHIFT-DELAYS-ACCELERATION: k*(1.5B@4096) = 28 (= the 0.5B's 1024 value shifted
#     two octaves right; the acceleration is also delayed by scale).
#  P2 ACCELERATION-IS-UNIVERSAL: k*(1.5B@4096) >= 48 (the 4× acceleration hits all
#     scales equally; the one-doubling delay from NET-66 doesn't extend to the
#     acceleration phase).
#  P3 INTERMEDIATE: k*(1.5B@4096) in [32, 44] — partial delay (the acceleration starts
#     but is dampened by scale).
import json, math, os, time
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'
import torch
import torch.nn.functional as F

src = open("/home/raver1975/factor3/ResearchOutput/exp_net55_1p5b_knee.py").read()
src = src.replace('if __name__ == "__main__":\n    main()', "")
g = {}
exec(compile(src, "e55", "exec"), globals())
# Patch Runner.forward to use QC=128 for 4096-context VRAM safety
_orig_forward = Runner.forward
def _patched_forward(self, ids, mode=None, k=None):
    B, L = ids.shape
    dev = ids.device
    m = self.m
    h = m.model.embed_tokens(ids).float()
    pos = torch.arange(L, device=dev)
    causal = torch.ones(L, L, dtype=torch.bool, device=dev).tril()
    neg = float("-inf")
    for layer in self.layers:
        sa = layer.self_attn
        r = h
        x = layer.input_layernorm(h)
        q = sa.q_proj(x).view(B, L, self.H, self.hd).transpose(1, 2)
        kc = sa.k_proj(x).view(B, L, self.KVH, self.hd).transpose(1, 2)
        v = sa.v_proj(x).view(B, L, self.KVH, self.hd).transpose(1, 2)
        rot = getattr(sa, "rotary_emb", None) or self.rotary
        cos, sin = rot(v, pos.unsqueeze(0).expand(B, -1))
        if cos.dim() == 3:
            cos, sin = cos.unsqueeze(1), sin.unsqueeze(1)
        q = q * cos + rotate_half(q) * sin
        kr = repeat_kv(kc * cos + rotate_half(kc) * sin, self.G)
        vr = repeat_kv(v, self.G)
        out = torch.empty(B, self.H, L, self.hd, device=dev)
        QC = 128  # reduced from 256 for 4096-context VRAM safety
        for qs in range(0, L, QC):
            qe = min(qs + QC, L)
            sc = q[:, :, qs:qe] @ kr.transpose(-2, -1) / math.sqrt(self.hd)
            sc = sc.masked_fill(~causal[qs:qe], neg)
            if mode == "topk":
                kk = int(min(k, L))
                thr = sc.topk(kk, dim=-1).values[..., -1:]
                sc = sc.masked_fill(sc < thr, neg)
            p = torch.softmax(sc, dim=-1)
            out[:, :, qs:qe] = p @ vr
            del sc, p
        out = out.transpose(1, 2).reshape(B, L, self.H * self.hd)
        h = r + sa.o_proj(out)
        h = h + layer.mlp(layer.post_attention_layernorm(h))
        del out, kr, vr, q, kc, v
    return m.model.norm(h)
Runner.forward = _patched_forward

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

    CTX, NW = 4096, 2
    wl = CTX + 1
    win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]

    @torch.no_grad()
    def ev(k):
        ces, corr, tot = 0.0, 0, 0
        t0 = time.time()
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
        return ces/tot, corr/tot, time.time()-t0

    full_ce, full_acc, _ = ev(None)
    base = max(full_acc, 1e-9)
    print(f"[full ] acc={full_acc:.4f} ce={full_ce:.4f} (nw={len(win)})", flush=True)
    res = {"model": "Qwen2.5-1.5B", "ctx": CTX, "nw": len(win),
           "full_acc": round(full_acc, 5), "cells": []}
    json.dump(res, open(os.path.expanduser("~/f3cache/net79_results.json"), "w"), indent=1)
    for k in (16, 20, 24, 28, 36, 44, 56):
        ce, acc, dt = ev(k)
        ret = acc/base
        print(f"[k={k:<5}] ret={ret:.4f} {'PASS' if ret>=0.98 else 'fail'} "
              f"ce={ce:.4f} ({dt:.0f}s)", flush=True)
        res["cells"].append({"k": k, "retained": round(ret, 5)})
        json.dump(res, open(os.path.expanduser("~/f3cache/net79_results.json"), "w"), indent=1)
        torch.cuda.empty_cache()
    kp = [c["k"] for c in res["cells"] if c["retained"] >= 0.98]
    res["kstar"] = min(kp) if kp else ">56"
    json.dump(res, open(os.path.expanduser("~/f3cache/net79_results.json"), "w"), indent=1)
    print(f"[KSTAR 1.5B ctx=4096] k* = {res['kstar']}", flush=True)
    print("\nALL_DONE_NET79", flush=True)

if __name__ == "__main__":
    main()

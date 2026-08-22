#!/usr/bin/env python3
# NET-55 — SIZE TRANSFER: THE KNEE AT 1.5B (limited-memory axis, iteration 7)
# Cell (3): do the real-model laws (knee collapse, saturation, diffuse-tail) persist at
# larger scale? Qwen2.5-1.5B (28 layers, GQA kv=2) vs the 0.5B results (knees {16,32,24};
# tail far-from-tropical). Host constraint: GPU power-capped at 96 W.
#
# Engineering findings en route:
#  * 1.5B fp32 = 6.2 GB > free VRAM -> HALF-STORAGE / FP32-COMPUTE (bf16 weights upcast
#    at call time; Pascal fp16/bf16 matmul never used).
#  * Qwen2.5-1.5B's own fp16 forward NaNs on real text (verified pre-wrapper) — bf16
#    storage required; gate references a CPU fp32 pass.
#  * Caches live in ~/f3cache (durable across the /tmp wipes that follow machine crashes).
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 SIZE-SCALING-KNEE: 1.5B knees are HIGHER than 0.5B's {16,32}:
#     k*(512) in [24, 48] and k*(1024) in [32, 96].
#  P2 TAIL-PERSISTS: eff-support jumps again at the LAST TWO layers.
#  P3 SATURATION-FAMILY: ratio k*(1024)/k*(512) <= 2.
import json, math, os, time
import torch
import torch.nn.functional as F

CACHE = os.path.expanduser("~/f3cache")
MODEL_DIR = os.path.join(CACHE, "qwen25-05b-1p5b")
CORPUS = os.path.join(CACHE, "net49_corpus.txt")
CTXS = [512, 1024]
GRIDS = {512: [8, 16, 24, 32, 48, 64],
         1024: [16, 24, 32, 48, 64, 96, 128]}
NW, BS = 24, 2

def rotate_half(x):
    x1, x2 = x.chunk(2, dim=-1)
    return torch.cat((-x2, x1), dim=-1)

def repeat_kv(x, n):
    if n == 1:
        return x
    b, h, l, d = x.shape
    return x[:, :, None].expand(b, h, n, l, d).reshape(b, h * n, l, d)

def floatify_linears(model):
    """fp16/bf16-stored weights, fp32-compute forward; single pass, immediate replacement."""
    import types
    import torch.nn as nn
    done = 0
    for parent in model.modules():
        for name, child in list(parent.named_children()):
            if isinstance(child, nn.Linear):
                w = child.weight.data.clone()
                b = child.bias.data.clone() if child.bias is not None else None
                new = nn.Module()
                new.register_buffer("_w", w, persistent=False)
                if b is not None:
                    new.register_buffer("_b", b, persistent=False)
                else:
                    new._b = None
                def fwd(self, x, _f=F.linear):
                    out = _f(x.float(), self._w.float(),
                             self._b.float() if self._b is not None else None)
                    return out.to(x.dtype)
                new.forward = types.MethodType(fwd, new)
                setattr(parent, name, new)
                done += 1
    return done

class Runner:
    def __init__(self, model):
        self.m = model
        cfg = model.config
        self.layers = model.model.layers
        self.H = cfg.num_attention_heads
        self.KVH = getattr(cfg, "num_key_value_heads", self.H)
        self.G = self.H // self.KVH
        self.hd = getattr(cfg, "head_dim", cfg.hidden_size // self.H)
        self.rotary = getattr(self.m.model, "rotary_emb", None)

    @torch.no_grad()
    def forward(self, ids, mode=None, k=None):
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
            QC = 256
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

    @torch.no_grad()
    def loss_acc(self, ids, **kw):
        B, L = ids.shape
        h = self.forward(ids, **kw)
        tgt = ids[:, 1:]
        n = B * (L - 1)
        ces, corr = 0.0, 0
        LC = 64
        V = self.m.config.vocab_size
        for s in range(0, L - 1, LC):
            e = min(s + LC, L - 1)
            lg = self.m.lm_head(h[:, s:e]).reshape(-1, V).float()
            t = tgt[:, s:e].reshape(-1)
            ces += F.cross_entropy(lg, t, reduction="sum").item()
            corr += (lg.argmax(-1) == t).sum().item()
        return ces / n, corr / n

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, dtype=torch.bfloat16,
                                                 attn_implementation="eager").cuda().eval()
    print(f"[floatify] replaced {floatify_linears(model)} linears", flush=True)
    cfg = model.config
    print(f"[model] d={cfg.num_hidden_layers} H={cfg.num_attention_heads} "
          f"KVH={cfg.num_key_value_heads}", flush=True)
    runner = Runner(model)

    text = open(CORPUS, encoding="utf-8").read()[:4_000_000]
    ids_all = torch.tensor(tok(text, add_special_tokens=False).input_ids, dtype=torch.long)
    split = int(0.9 * len(ids_all))
    held = ids_all[split:].cuda()

    # validation gate: GPU bf16-storage/fp32-compute vs CPU fp32 reference, REAL text
    with torch.no_grad():
        vb = held[:128].view(1, -1)
        ref_m = AutoModelForCausalLM.from_pretrained(MODEL_DIR, dtype=torch.float32).eval()
        ref = ref_m(input_ids=vb.cpu()).logits
        h = runner.forward(vb)
        mine = model.lm_head(h).float().cpu()
        agree = float((ref.argmax(-1) == mine.argmax(-1)).float().mean())
        ce_r = F.cross_entropy(ref[:, :-1].reshape(-1, ref.size(-1)), vb[:, 1:].reshape(-1)).item()
        ce_m = F.cross_entropy(mine[:, :-1].reshape(-1, mine.size(-1)), vb[:, 1:].reshape(-1)).item()
        print(f"[validate] argmax-agree={agree:.4f} CE ref={ce_r:.4f} mine={ce_m:.4f}", flush=True)
        assert agree >= 0.95 and abs(ce_r - ce_m) < 0.03, "own forward diverges from fp32 ref"
        del ref_m
    del ref, mine
    torch.cuda.empty_cache()

    res = {"model": "Qwen2.5-1.5B", "cells": []}
    for ctx in CTXS:
        wl = ctx + 1
        win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]
        def ev(**kw):
            ces, corr, tot = 0.0, 0, 0
            t0 = time.time()
            for s in range(0, len(win), BS):
                b = torch.cat(win[s:s+BS], dim=0)
                ce, ac = runner.loss_acc(b, **kw)
                ntok = b.size(0)*(b.size(1)-1)
                ces += ce*ntok; corr += ac*ntok; tot += ntok
            return ces/tot, corr/tot, time.time()-t0
        full_ce, full_acc, _ = ev()
        print(f"\n===== CTX={ctx} full acc={full_acc:.4f} ce={full_ce:.4f} =====", flush=True)
        base = max(full_acc, 1e-9)
        res["cells"].append({"ctx": ctx, "mode": "full", "acc": round(full_acc, 5)})
        for k in GRIDS[ctx]:
            ce, acc, dt = ev(mode="topk", k=k)
            ret = acc/base
            print(f"[k={k:<5}] ret={ret:.4f} {'PASS' if ret>=0.98 else 'fail'} "
                  f"ce={ce:.4f} ({dt:.0f}s)", flush=True)
            res["cells"].append({"ctx": ctx, "mode": "topk", "k": k, "retained": round(ret, 5)})
            json.dump(res, open(os.path.join(CACHE, "net55_results.json"), "w"), indent=1)
            torch.cuda.empty_cache()
        kp = [c["k"] for c in res["cells"] if c["ctx"]==ctx and c.get("mode")=="topk" and c["retained"]>=0.98]
        res[f"kstar_ctx{ctx}"] = min(kp) if kp else None
        json.dump(res, open(os.path.join(CACHE, "net55_results.json"), "w"), indent=1)
        print(f"[KSTAR ctx={ctx}] k* = {res[f'kstar_ctx{ctx}']}", flush=True)

    print("\nALL_DONE_NET55", flush=True)

if __name__ == "__main__":
    main()

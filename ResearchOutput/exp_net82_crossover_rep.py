#!/usr/bin/env python3
# NET-82 — CROSSOVER REPLICATION WITH MORE WINDOWS (limited-memory axis, iteration 56)
# NET-81 found non-monotone results (@2560 k*=44, @3072 k*=28) at n=6 windows.
# This replication uses n=12 to resolve whether the inversion is real or sampling noise.
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 MONOTONE-RESTORED: with 12 windows, k*(2560) <= k*(3072) — the non-monotone was
#     sampling variation; the chain is properly monotone {16,20,24,...}.
#  P2 NON-MONOTONE-IS-REAL: the inversion persists at n=12 — there is a genuine
#     context-range where more keys are needed at 2560 than 3072.
import json, math, os, time
import torch
import torch.nn.functional as F

MODEL_PATH = os.path.expanduser("~/f3cache/qwen25-05b")
CORPUS_PATH = os.path.expanduser("~/f3cache/net49_corpus.txt")

def rotate_half(x):
    x1, x2 = x.chunk(2, dim=-1)
    return torch.cat((-x2, x1), dim=-1)

def repeat_kv(x, n):
    if n == 1: return x
    b, h, l, d = x.shape
    return x[:, :, None].expand(b, h, n, l, d).reshape(b, h * n, l, d)

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
    def forward_oracle(self, ids, k=None):
        B, L = ids.shape
        dev = ids.device
        h = self.m.model.embed_tokens(ids).float()
        pos = torch.arange(L, device=dev)
        causal = torch.ones(L, L, dtype=torch.bool, device=dev).tril()
        neg = float("-inf")
        QC = 128
        for layer in self.layers:
            sa = layer.self_attn
            r = h
            x = layer.input_layernorm(h)
            q = sa.q_proj(x).view(B, L, self.H, self.hd).transpose(1, 2)
            kc = sa.k_proj(x).view(B, L, self.KVH, self.hd).transpose(1, 2)
            v = sa.v_proj(x).view(B, L, self.KVH, self.hd).transpose(1, 2)
            rot = getattr(sa, "rotary_emb", None) or self.rotary
            cos, sin = rot(v, pos.unsqueeze(0).expand(B, -1))
            if cos.dim() == 3: cos, sin = cos.unsqueeze(1), sin.unsqueeze(1)
            q = q * cos + rotate_half(q) * sin
            kr = repeat_kv(kc * cos + rotate_half(kc) * sin, self.G)
            vr = repeat_kv(v, self.G)
            out = torch.empty(B, self.H, L, self.hd, device=dev)
            for qs in range(0, L, QC):
                qe = min(qs + QC, L)
                sc = q[:, :, qs:qe] @ kr.transpose(-2, -1) / math.sqrt(self.hd)
                sc = sc.masked_fill(~causal[qs:qe], neg)
                if k is not None:
                    kk = int(min(k, L))
                    thr = sc.topk(kk, dim=-1).values[..., -1:]
                    sc = sc.masked_fill(sc < thr, neg)
                p = torch.softmax(sc, dim=-1)
                out[:, :, qs:qe] = p.to(vr.dtype) @ vr
                del sc, p
            out = out.transpose(1, 2).reshape(B, L, self.H * self.hd)
            h = r + sa.o_proj(out)
            h = h + layer.mlp(layer.post_attention_layernorm(h))
            del out, kr, vr, q, kc, v
        return self.m.model.norm(h)

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH, dtype=torch.float32,
        attn_implementation="eager").cuda().eval()
    runner = Runner(model)

    text = open(CORPUS_PATH, encoding="utf-8").read()[:4_000_000]
    ids_all = torch.tensor(tok(text, add_special_tokens=False).input_ids,
                           dtype=torch.long)
    split = int(0.9 * len(ids_all))
    held = ids_all[split:].cuda()

    # gate on real text
    with torch.no_grad():
        vb = held[:128].view(1, -1)
        ref = model(input_ids=vb).logits.float()
        mine = model.lm_head(runner.forward_oracle(vb)).float()
        agree = float((ref.argmax(-1) == mine.argmax(-1)).float().mean())
        print(f"[validate] argmax-agree={agree:.4f}", flush=True)
        assert agree >= 0.999
    del ref, mine
    torch.cuda.empty_cache()

    res = {"replication": True, "nw": 12, "contexts": {}}

    for ctx in (2560, 3072):
        wl = ctx + 1
        win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(12, len(held)//wl))]

        @torch.no_grad()
        def ev(k):
            ces, corr, tot = 0.0, 0, 0
            t0 = time.time()
            for s in range(0, len(win), 2):
                b = torch.cat(win[s:s+2], dim=0).cuda()
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
        base_acc = max(full_acc, 1e-9)
        print(f"\n[ctx={ctx}] full={full_acc:.4f}", flush=True)
        sweeps = []
        for k in (16, 20, 24, 28, 32, 36, 44):
            ce, acc, dt = ev(k)
            ret = acc/base_acc
            sweeps.append({"k": k, "retained": round(ret, 5)})
            print(f"  k={k:<5} ret={ret:.4f} {'PASS' if ret>=0.98 else 'fail'}",
                  flush=True)
        kp = [s["k"] for s in sweeps if s["retained"] >= 0.98]
        kstar = min(kp) if kp else f">{max(s['k'] for s in sweeps)}"
        print(f"  KSTAR = {kstar}", flush=True)
        res["contexts"][str(ctx)] = {"full_acc": round(full_acc, 5),
                                     "kstar": str(kstar), "sweeps": sweeps}
        json.dump(res, open(os.path.expanduser("~/f3cache/net82_results.json"), "w"),
                  indent=1)
        torch.cuda.empty_cache()

    # summary
    c2560 = res["contexts"].get("2560", {}).get("kstar", "?")
    c3072 = res["contexts"].get("3072", {}).get("kstar", "?")
    print(f"\n[SUMMARY] k*(2560)={c2560}, k*(3072)={c3072}")
    print(f"[VERDICT] {'MONOTONE restored' if str(c2560) <= str(c3072) else 'NON-MONOTONE persists'}",
          flush=True)
    print("\nALL_DONE_NET82", flush=True)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# NET-81 — THE CROSSOVER LOCALIZATION (limited-memory axis, iteration 52)
import json, math, os, time
import torch
import torch.nn.functional as F

MODEL_05 = os.path.expanduser("~/f3cache/qwen25-05b")
MODEL_15 = os.path.expanduser("~/f3cache/qwen25-05b-1p5b")
CORPUS_PATH = os.path.expanduser("~/f3cache/net49_corpus.txt")

def rotate_half(x):
    x1, x2 = x.chunk(2, dim=-1)
    return torch.cat((-x2, x1), dim=-1)

def repeat_kv(x, n):
    if n == 1: return x
    b, h, l, d = x.shape
    return x[:, :, None].expand(b, h, n, l, d).reshape(b, h * n, l, d)

def floatify(model):
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
                new._b = None
                if b is not None: new.register_buffer("_b", b, persistent=False)
                def fwd(self, x, _f=F.linear):
                    return _f(x.float(), self._w.float(),
                             self._b.float() if self._b is not None else None).to(x.dtype)
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
    def forward(self, ids, k=None):
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
    text = open(CORPUS_PATH, encoding="utf-8").read()[:4_000_000]
    results = {"crossover_search": []}

    for mname, mpath, dt in [("0.5B", MODEL_05, torch.float32),
                              ("1.5B", MODEL_15, torch.bfloat16)]:
        tok = AutoTokenizer.from_pretrained(mpath)
        ids_all = torch.tensor(tok(text, add_special_tokens=False).input_ids,
                               dtype=torch.long)
        split = int(0.9 * len(ids_all))
        held = ids_all[split:].cuda()

        model = AutoModelForCausalLM.from_pretrained(
            mpath, dtype=dt, attn_implementation="eager").cuda().eval()
        if dt != torch.float32:
            floatify(model)
        runner = Runner(model)

        # gate on real text
        with torch.no_grad():
            vb = held[:128].view(1, -1)
            ref = model(input_ids=vb).logits.float()
            hh = runner.forward(vb)
            mine = model.lm_head(hh).float()
            agree = float((ref.argmax(-1) == mine.argmax(-1)).float().mean())
            print(f"[{mname} gate] agree={agree:.4f}", flush=True)
            assert agree >= (0.999 if dt == torch.float32 else 0.85)
            del ref, mine, hh, vb
        torch.cuda.empty_cache()

        def make_ev(ctx):
            wl = ctx + 1
            w = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(6, len(held)//wl))]
            @torch.no_grad()
            def ev(k):
                ces, corr, tot = 0.0, 0, 0
                for b0 in w:
                    bb = b0.cuda()
                    h = runner.forward(bb, k=k) if k else runner.forward(bb)
                    tgt = bb[:, 1:]
                    nn2 = b0.size(0)*(b0.size(1)-1)
                    V = model.config.vocab_size
                    for s2 in range(0, b0.size(1)-1, 64):
                        e2 = min(s2+64, b0.size(1)-1)
                        lg = model.lm_head(h[:, s2:e2]).reshape(-1, V).float()
                        tt = tgt[:, s2:e2].reshape(-1)
                        ces += F.cross_entropy(lg, tt, reduction="sum").item()
                        corr += (lg.argmax(-1) == tt).sum().item()
                    tot += nn2
                return ces/tot, corr/tot
            return ev

        for ctx in (2560, 3072):
            ev_fn = make_ev(ctx) if False else None
            # rebuild closure per ctx to avoid late binding
            wl2 = ctx + 1
            w2 = [held[i*wl2:(i+1)*wl2].view(1, wl2) for i in range(min(6, len(held)//wl2))]
            @torch.no_grad()
            def ev2(k, w=w2):
                ces, corr, tot = 0.0, 0, 0
                for b0 in w:
                    bb = b0.cuda()
                    h = runner.forward(bb, k=k) if k else runner.forward(bb)
                    tgt = bb[:, 1:]
                    nn2 = b0.size(0)*(b0.size(1)-1)
                    V = model.config.vocab_size
                    for s2 in range(0, b0.size(1)-1, 64):
                        e2 = min(s2+64, b0.size(1)-1)
                        lg = model.lm_head(h[:, s2:e2]).reshape(-1, V).float()
                        tt = tgt[:, s2:e2].reshape(-1)
                        ces += F.cross_entropy(lg, tt, reduction="sum").item()
                        corr += (lg.argmax(-1) == tt).sum().item()
                    tot += nn2
                return ces/tot, corr/tot

            full_ce, full_acc = ev2(None)
            base_acc = max(full_acc, 1e-9)
            entry = {"model": mname, "ctx": ctx, "full_acc": round(full_acc, 5),
                     "sweep": []}
            print(f"[{mname} ctx={ctx}] full={full_acc:.4f}", flush=True)
            for k in (16, 20, 24, 28, 32, 44):
                ce, acc = ev2(k)
                ret = acc / base_acc
                entry["sweep"].append({"k": k, "retained": round(ret, 5)})
                print(f"  k={k:<5} ret={ret:.4f} {'PASS' if ret>=0.98 else 'fail'}",
                      flush=True)
            kp = [s["k"] for s in entry["sweep"] if s["retained"] >= 0.98]
            entry["kstar"] = min(kp) if kp else f">{max(s['k'] for s in entry['sweep'])}"
            print(f"  KSTAR = {entry['kstar']}", flush=True)
            results["crossover_search"].append(entry)
            json.dump(results,
                      open(os.path.expanduser("~/f3cache/net81_results.json"), "w"),
                      indent=1)

        del model, runner
        torch.cuda.empty_cache()

    # summarize
    print("\n===== CROSSOVER SUMMARY =====", flush=True)
    for e in results["crossover_search"]:
        print(f"{e['model']} @{e['ctx']}: k*={e['kstar']}", flush=True)
    print("\nALL_DONE_NET81", flush=True)

if __name__ == "__main__":
    main()

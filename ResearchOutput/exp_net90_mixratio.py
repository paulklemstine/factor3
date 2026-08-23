#!/usr/bin/env python3
# NET-90 — THE MIXING-RATIO SWEEP (limited-memory axis, iteration 65)
# NET-89 found mixed code+prose at 50/50 has knees {12, 20} — starting low and rising
# fast. This round sweeps the mixing ratio: 25/75 (code-dominant), 50/50 (NET-89
# replication), 75/25 (prose-dominant), plus pure endpoints for calibration.
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 LINEAR-INTERPOLATION: knee varies linearly with mixing ratio between the pure
#     endpoints {code@512=12, prose@512=16} and {code@1024=16, prose@1024=20}.
#  P2 NONLINEAR-DIP: the mixed knee dips BELOW both pure domains at intermediate ratios
#     (the cross-domain attention creates locally adaptive structure that is more
#     efficient than either domain alone).
#  P3 MONOTONE-IN-PROSE: knee increases monotonically with prose fraction.
import json, math, os, time
import torch
import torch.nn.functional as F

MODEL_DIR = os.path.expanduser("~/f3cache/qwen25-05b")
CODE_CACHE = os.path.expanduser("~/f3cache/code_corpus.txt")
PROSE_CACHE = os.path.expanduser("~/f3cache/net49_corpus.txt")
CTXS, NW, BS = [512, 1024], 12, 2

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
        self.V = cfg.vocab_size

    @torch.no_grad()
    def forward_oracle(self, ids, k=None):
        B, L = ids.shape
        h = self.m.model.embed_tokens(ids).float()
        pos = torch.arange(L, device=ids.device)
        causal = torch.ones(L, L, dtype=torch.bool, device=ids.device).tril()
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
            out = torch.empty(B, self.H, L, self.hd, device=ids.device)
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
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_DIR, dtype=torch.float32,
        attn_implementation="eager").cuda().eval()
    runner = Runner(model)

    code_t = open(CODE_CACHE, encoding="utf-8").read()[:1_000_000]
    prose_t = open(PROSE_CACHE, encoding="utf-8").read()[:1_000_000]

    def make_mixed(prose_frac):
        """Interleave blocks with approximately prose_frac fraction of prose."""
        def chunk(t, size=500):
            return [t[i:i+size] for i in range(0, len(t)-size, size)]
        cc, pc = chunk(code_t), chunk(prose_t)
        n_pairs = min(len(cc), len(pc))
        mixed = []
        # use deterministic interleaving: every floor(1/prose_frac) blocks insert one prose block
        step = max(int(round(1 / prose_frac)), 1) if prose_frac > 0 else len(cc)+1
        pi = 0
        for i in range(n_pairs):
            if i % step == 0 and pi < len(pc):
                mixed.append(pc[pi])
                pi += 1
            mixed.append(cc[i])
            if prose_frac >= 0.99:
                pass  # pure prose handled separately
        return "\n\n".join(mixed)

    text = open(PROSE_CACHE, encoding="utf-8").read()[:100_000]
    vb_ids = None

    res = {"mixing_sweep": []}

    for ctx in CTXS:
        wl = ctx + 1
        print(f"\n===== CTX={ctx} =====", flush=True)
        for ratio_name, pfrac in [("pure_code", 0.0), ("25/75", 0.25),
                                   ("50/50", 0.5), ("75/25", 0.75),
                                   ("pure_prose", 1.0)]:
            # build corpus for this ratio
            if pfrac == 0.0:
                t = code_t if 'code_t' in dir() else open(CODE_CACHE, encoding='utf-8').read()[:2_000_000]
            elif pfrac == 1.0:
                t = prose_t if 'prose_t' in dir() else open(PROSE_CACHE, encoding='utf-8').read()[:2_000_000]
            else:
                def chunk(t, s=500): return [t[i:i+s] for i in range(0, len(t)-s, s)]
                cc, pc = chunk(code_t), chunk(prose_t)
                mixed_blocks = []
                ni, np_ = 0, 0
                total = min(len(cc) + len(pc), 4000)
                while len("".join(mixed_blocks)) < 2_000_000:
                    if np_ / max(len(mixed_blocks), 1) < pfrac and np_ < len(pc):
                        mixed_blocks.append(pc[np_]); np_ += 1
                    elif ni < len(cc):
                        mixed_blocks.append(cc[ni]); ni += 1
                    else:
                        break
                t = "".join(mixed_blocks)[:2_000_000]

            ids = torch.tensor(tok(t, add_special_tokens=False).input_ids,
                               dtype=torch.long)
            sp = int(0.9 * len(ids))
            hd = ids[sp:].cuda()
            w = [hd[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(hd)//wl))]
            if not w:
                continue

            @torch.no_grad()
            def ev(k, w=w):
                ces, corr, tot = 0.0, 0, 0
                for b0 in w:
                    bb = b0.cuda()
                    h = runner.forward_oracle(bb, k=k)
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

            full_ce, full_acc = ev(None)
            base_acc = max(full_acc, 1e-9)
            entry = {"ctx": ctx, "ratio": ratio_name, "pfrac": pfrac,
                     "full_acc": round(full_acc, 5), "knee": None}
            for k in (8, 12, 16, 20, 24):
                ce, acc = ev(k)
                ret = acc/base_acc
                if ret >= 0.98 and entry["knee"] is None:
                    entry["knee"] = k
                print(f"  [{ratio_name} ctx={ctx} k={k:<3}] ret={ret:.4f}", flush=True)
            knee = None
            for kk in (8,12,16,20,24):
                ce2, acc2 = ev(kk)
                if acc2/base_acc >= 0.98:
                    knee = kk; break
            entry["knee"] = knee or ">24"
            res["mixing_sweep"].append(entry)
            json.dump(res,
                      open(os.path.expanduser("~/f3cache/net90_results.json"), "w"),
                      indent=1)
            print(f"  KNEE[{ratio_name}@{ctx}] = {entry['knee']}", flush=True)
            torch.cuda.empty_cache()

    print("\nALL_DONE_NET90", flush=True)

if __name__ == "__main__":
    main()

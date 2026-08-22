#!/usr/bin/env python3
# NET-51 — THE MODEL-DELTA SERVING LAW (limited-memory axis, iteration 3)
# Mined from the Lean catalogue: "Amortized Model-Delta Compression" (min-plus):
# optimal bits for n messages over a shared decompressor = n*r + min(D, n).
#
# Serving question: two fine-tunes of one base (Qwen2.5-0.5B base vs Instruct) —
# how much of their KV cache is SHARED? If per-layer divergence is small, a server can
# keep ONE base KV cache plus per-model deltas: cost = shared + delta instead of 2x full.
#
# Measurement (same prompts through both models):
#  Part A: per-layer K/V divergence — cosine similarity + relative L2 of post-rope keys
#          and values (GQA: only 2 kv-heads -> cheap), per position third (early/mid/late).
#  Part B: per-layer attention DECISION divergence — fraction of query rows whose top-1
#          key (own scores) agrees between the two models.
#  Part C: hidden-state divergence growth h_inst vs h_base across depth.
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 EARLY-SHARE: layer 0 K/V near-identical (cos > 0.99); fine-tuning touches late
#     layers first -> shared fraction high early.
#  P2 MONOTONE-DIVERGENCE: K/V divergence grows monotonically with depth (upstream
#     differences amplified layer by layer).
#  P3 DELTA-WIN: a base+delta scheme (store base KV once + per-model residuals only
#     where divergence > eps) needs substantially less than 2x single-model KV memory,
#     i.e. the joint cache beats naive duplication.
import json, math, time
import torch
import torch.nn.functional as F

BASE = "/tmp/qwen25-05b"
INST = "/tmp/qwen25-05b-instruct"
CTX = 1024
NPROMPT = 4

def rotate_half(x):
    x1, x2 = x.chunk(2, dim=-1)
    return torch.cat((-x2, x1), dim=-1)

def repeat_kv(x, n):
    if n == 1:
        return x
    b, h, l, d = x.shape
    return x[:, :, None].expand(b, h, n, l, d).reshape(b, h * n, l, d)

class Capture:
    """Own-forward executor that captures per-layer q/k/v (post-rope k)."""
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
    def forward_capture(self, ids):
        B, L = ids.shape
        dev = ids.device
        m = self.m
        cap = {"q": [], "k": [], "v": [], "h": []}
        h = m.model.embed_tokens(ids)
        pos = torch.arange(L, device=dev)
        causal = torch.ones(L, L, dtype=torch.bool, device=dev).tril()
        for layer in self.layers:
            sa = layer.self_attn
            cap["h"].append(h.detach().half().cpu())
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
            kc = kc * cos + rotate_half(kc) * sin
            cap["q"].append(q.detach().half().cpu())     # [B,H,L,hd]
            cap["k"].append(kc.detach().half().cpu())    # [B,KVH,L,hd]
            cap["v"].append(v.detach().half().cpu())
            kr = repeat_kv(kc.float(), self.G)
            vr = repeat_kv(v.float(), self.G)
            out = torch.empty(B, self.H, L, self.hd, device=dev, dtype=torch.float32)
            QC = 256
            for qs in range(0, L, QC):
                qe = min(qs + QC, L)
                sc = q[:, :, qs:qe].float() @ kr.transpose(-2, -1) / math.sqrt(self.hd)
                sc = sc.masked_fill(~causal[qs:qe], float("-inf"))
                p = torch.softmax(sc, dim=-1)
                out[:, :, qs:qe] = p @ vr
                del sc, p
            out = out.transpose(1, 2).reshape(B, L, self.H * self.hd).to(h.dtype)
            h = r + sa.o_proj(out)
            h = h + layer.mlp(layer.post_attention_layernorm(h))
            del out, kr, vr, q, kc, v
        cap["final"] = h.detach()
        return cap

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(BASE)
    print(f"[load] base {BASE}", flush=True)
    mb = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.float16,
                                              attn_implementation="eager").cuda().eval()
    runner_b = Capture(mb)
    # validation gate for own-forward vs HF (fp16 tolerance)
    with torch.no_grad():
        vb = torch.randint(0, mb.config.vocab_size, (1, 128), device="cuda")
        ref = mb(input_ids=vb).logits.float()
        hh = runner_b.forward_capture(vb)
        mine = mb.lm_head(mb.model.norm(hh["final"].cuda())).float()
        agree = float((ref.argmax(-1) == mine.argmax(-1)).float().mean())
        print(f"[validate-base] argmax-agree={agree:.4f}", flush=True)
        assert agree >= 0.90, "capture forward diverges from HF forward"
    del vb, ref, mine, hh
    torch.cuda.empty_cache()

    text = open("/tmp/net49_corpus.txt", encoding="utf-8").read()[:2_000_000]
    ids_all = torch.tensor(tok(text, add_special_tokens=False).input_ids, dtype=torch.long)
    N = len(ids_all); split = int(0.9 * N)
    held = ids_all[split:]
    wl = CTX + 1
    prompts = [held[i * wl:(i + 1) * wl].view(1, wl) for i in range(NPROMPT)]
    batch = torch.cat(prompts, dim=0).cuda()
    print(f"[data] {NPROMPT} prompts x {wl} tokens", flush=True)

    print("[run] capturing base", flush=True)
    cap_b = runner_b.forward_capture(batch)
    del mb; torch.cuda.empty_cache()

    print(f"[load] instruct {INST}", flush=True)
    mi = AutoModelForCausalLM.from_pretrained(INST, dtype=torch.float16,
                                              attn_implementation="eager").cuda().eval()
    runner_i = Capture(mi)
    with torch.no_grad():
        ref = mi(input_ids=batch[:1]).logits.float()
        hh = runner_i.forward_capture(batch[:1])
        mine = mi.lm_head(mi.model.norm(hh["final"].cuda())).float()
        agree = float((ref.argmax(-1) == mine.argmax(-1)).float().mean())
        print(f"[validate-instruct] argmax-agree={agree:.4f}", flush=True)
        assert agree >= 0.90
    del ref, mine, hh
    print("[run] capturing instruct", flush=True)
    cap_i = runner_i.forward_capture(batch)
    del mi; torch.cuda.empty_cache()

    L = len(cap_b["q"])
    B, Hh, Ll, hd = cap_b["q"][0].shape
    res = {"ctx": CTX, "nprompt": NPROMPT, "layers": []}
    print(f"\n{'ly':>3} {'cosK':>7} {'cosV':>7} {'relK':>7} {'relV':>7} "
          f"{'top1ag':>7} {'|dh|/|hb|':>9}", flush=True)
    for li in range(L):
        kb, vi = cap_b["k"][li].float(), cap_i["k"][li].float()
        vb_, vi_ = cap_b["v"][li].float(), cap_i["v"][li].float()
        qb, qi = cap_b["q"][li].float(), cap_i["q"][li].float()

        def cosrel(a, b):
            num = (a * b).sum(-1)
            den = a.norm(dim=-1) * b.norm(dim=-1) + 1e-9
            cos = (num / den).mean().item()
            rel = ((a - b).norm(dim=-1) / (a.norm(dim=-1) + 1e-9)).mean().item()
            return cos, rel

        cosK, relK = cosrel(kb, vi)
        cosV, relV = cosrel(vb_, vi_)
        # top-1 key agreement per query row (each model's own q,k)
        sc_b = torch.einsum("bhqd,bhkd->bhqk", qb, repeat_kv(kb, runner_b.G))
        sc_i = torch.einsum("bhqd,bhkd->bhqk", qi, repeat_kv(vi, runner_b.G))
        mask = torch.ones(Ll, Ll, dtype=torch.bool).tril()
        sc_b = sc_b.masked_fill(~mask, float("-inf"))
        sc_i = sc_i.masked_fill(~mask, float("-inf"))
        top_b = sc_b.argmax(-1)          # [B,H,L] chosen key per query row (causal-masked)
        top_i = sc_i.argmax(-1)
        agree_frac = float((top_b == top_i).float().mean())
        del mask
        dh = (cap_i["h"][li].float() - cap_b["h"][li].float()).norm(dim=-1)
        hb = cap_b["h"][li].float().norm(dim=-1) + 1e-9
        rel_h = (dh / hb).mean().item()
        row = dict(layer=li, cosK=round(cosK, 5), cosV=round(cosV, 5),
                   relK=round(relK, 5), relV=round(relV, 5),
                   top1_agree=round(agree_frac, 5), rel_hidden=round(float(rel_h), 5))
        res["layers"].append(row)
        print(f"{li:>3} {cosK:>7.4f} {cosV:>7.4f} {relK:>7.4f} {relV:>7.4f} "
              f"{agree_frac:>7.4f} {float(rel_h):>9.4f}", flush=True)
        del kb, vi, vb_, vi_, qb, qi, sc_b, sc_i, top_b, top_i

    # summary scalars
    import statistics
    res["summary"] = {
        "mean_cosK": round(statistics.mean(r["cosK"] for r in res["layers"]), 5),
        "mean_top1_agree": round(statistics.mean(r["top1_agree"] for r in res["layers"]), 5),
        "monotone_relK": all(res["layers"][i]["relK"] <= res["layers"][i+1]["relK"] + 0.02
                             for i in range(L - 1)),
    }
    json.dump(res, open("/tmp/net51_results.json", "w"), indent=1)
    print("\n[summary]", res["summary"], flush=True)
    print("ALL_DONE_NET51", flush=True)

if __name__ == "__main__":
    main()

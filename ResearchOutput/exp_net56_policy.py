#!/usr/bin/env python3
# NET-56 — THE ORACLE-TO-POLICY GAP (limited-memory axis, iteration 9)
# Cell (4): NET-49's knees are ORACLE measurements (per-row top-k over full causal scores).
# A streaming server cannot see future rows: it must EVICT keys by ACCUMULATED attention
# statistics. This round measures how much of the oracle's KV win survives a real policy.
#
# Policies at matched budget B (keys kept per layer/head):
#   ORACLE: per-row top-k (upper bound; reuses validated semantics)
#   HH:     accumulated-score top-B, updated every BLOCK=128 rows (pure heavy hitters)
#   HYB:    heavy-hitters + recency (top-(B-W) accumulated + always the last W=32 keys)
# Metrics: retained next-token accuracy vs full, ctx=1024, Qwen2.5-0.5B fp32, 24 windows.
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 POLICY-GAP-IS-REAL: streaming HH retains measurably less than oracle at matched B
#     (>= 2% accuracy gap at B=64).
#  P2 RECENCY-MATTERS: HYB beats HH at the same total budget.
#  P3 STILL-LARGE-WIN: best policy at B=64 retains >= 0.95 while touching <= 12% of KV.
import json, math, os, time
import torch
import torch.nn.functional as F

MODEL_DIR = os.path.expanduser("~/f3cache/qwen25-05b")
CORPUS = os.path.expanduser("~/f3cache/net49_corpus.txt")
CTX, NW, BS, BLOCK, WREC = 1024, 24, 2, 128, 32

def rotate_half(x):
    x1, x2 = x.chunk(2, dim=-1)
    return torch.cat((-x2, x1), dim=-1)

def repeat_kv(x, n):
    if n == 1:
        return x
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

    def _attn_proj(self, layer, x):
        sa = layer.self_attn
        q = sa.q_proj(x).view(x.shape[0], x.shape[1], self.H, self.hd).transpose(1, 2)
        kc = sa.k_proj(x).view(x.shape[0], x.shape[1], self.KVH, self.hd).transpose(1, 2)
        v = sa.v_proj(x).view(x.shape[0], x.shape[1], self.KVH, self.hd).transpose(1, 2)
        rot = getattr(sa, "rotary_emb", None) or self.rotary
        pos = torch.arange(x.shape[1], device=x.device)
        cos, sin = rot(v, pos.unsqueeze(0).expand(x.shape[0], -1))
        if cos.dim() == 3:
            cos, sin = cos.unsqueeze(1), sin.unsqueeze(1)
        q = q * cos + rotate_half(q) * sin
        kr = repeat_kv(kc * cos + rotate_half(kc) * sin, self.G)
        vr = repeat_kv(v, self.G)
        return q, kr, vr

    @torch.no_grad()
    def forward_oracle(self, ids, k=None):
        """Validated full-row computation with optional per-row top-k."""
        B, L = ids.shape
        m = self.m
        h = m.model.embed_tokens(ids).float()
        causal = torch.ones(L, L, dtype=torch.bool, device=ids.device).tril()
        neg = float("-inf")
        for layer in self.layers:
            sa = layer.self_attn
            r = h
            x = layer.input_layernorm(h)
            q, kr, vr = self._attn_proj(layer, x)
            out = torch.empty(B, self.H, L, self.hd, device=ids.device)
            for qs in range(0, L, 256):
                qe = min(qs + 256, L)
                sc = q[:, :, qs:qe] @ kr.transpose(-2, -1) / math.sqrt(self.hd)
                sc = sc.masked_fill(~causal[qs:qe], neg)
                if k is not None:
                    kk = int(min(k, L))
                    thr = sc.topk(kk, dim=-1).values[..., -1:]
                    sc = sc.masked_fill(sc < thr, neg)
                p = torch.softmax(sc, dim=-1)
                out[:, :, qs:qe] = p @ vr
                del sc, p
            out = out.transpose(1, 2).reshape(B, L, self.H * self.hd)
            h = r + sa.o_proj(out)
            h = h + layer.mlp(layer.post_attention_layernorm(h))
            del out, kr, vr, q
        return m.model.norm(h)

    @torch.no_grad()
    def forward_stream(self, ids, B_budget=None, mode="hh"):
        """Block-streaming with KV eviction by accumulated scores.
        mode 'hh': keep top-B by accumulated score. 'hyb': top-(B-W) + last W positions."""
        Bt, L = ids.shape
        m = self.m
        h = m.model.embed_tokens(ids).float()
        neg = float("-inf")
        for layer in self.layers:
            sa = layer.self_attn
            r = h
            x = layer.input_layernorm(h)
            q, kr, vr = self._attn_proj(layer, x)
            out = torch.empty(Bt, self.H, L, self.hd, device=ids.device)
            acc = None          # [B,KVH*G? -> use expanded H for scoring] accumulate probs [B,H,L]
            kept = None         # indices into [L] per (B,H)
            for s0 in range(0, L, BLOCK):
                s1 = min(s0 + BLOCK, L)
                qc = q[:, :, s0:s1]
                # faithful streaming policy: kept keys UNION the whole current block
                # (a real server always has the un-evicted tail in cache)
                if kept is not None:
                    blk = torch.arange(s0, s1, device=ids.device)[None, None].expand(Bt, self.H, -1)
                    allk = torch.cat([kept, blk], dim=-1)   # kept < s0, blk >= s0: disjoint
                    offs = allk.sort(dim=-1).values
                else:
                    offs = torch.arange(s1, device=ids.device)[None, None].expand(Bt, self.H, -1)
                gidx = offs.unsqueeze(-1).expand(-1, -1, -1, self.hd)
                krc = torch.gather(kr, 2, gidx)
                vrc = torch.gather(vr, 2, gidx)
                rp = torch.arange(s0, s1, device=ids.device)
                allow = offs.unsqueeze(2) <= rp.view(1, 1, -1, 1)  # [B,H,q,K] incl. self
                sc = qc @ krc.transpose(-2, -1) / math.sqrt(self.hd)
                sc = sc.masked_fill(~allow, neg)
                p = torch.softmax(sc, dim=-1)
                out[:, :, s0:s1] = p.to(vr.dtype) @ vrc
                # accumulator: true usage of EVERY key so far (policy sees own stats)
                contrib = torch.zeros(Bt, self.H, s1, device=ids.device)
                contrib.scatter_add_(2,
                    (offs * (offs < s1)).clamp_max(s1 - 1).view(Bt, self.H, -1),
                    p.reshape(Bt, self.H, -1))
                acc = contrib if acc is None else torch.cat(
                    [acc, torch.zeros(Bt, self.H, s1 - acc.shape[2], device=ids.device)],
                    dim=2) + contrib
                # eviction at block end
                if s1 < L:
                    W_eff = min(WREC, max(B_budget // 2, 1))
                    Bh = max(B_budget - W_eff, 1)
                    score = acc
                    if mode == "hyb":
                        rm = torch.zeros(s1, dtype=torch.bool, device=ids.device)
                        rm[max(0, s1 - W_eff):s1] = True
                        score = acc.masked_fill(rm[None, None], neg)   # exclude recent from HH pick
                        Bh_eff = min(Bh, max(s1 - W_eff, 1))
                        keptn = score.topk(min(Bh_eff, s1), dim=-1).indices.sort(dim=-1).values
                        ri = torch.arange(max(0, s1 - W_eff), s1, device=ids.device)
                        ri = ri[None, None].expand(Bt, self.H, -1)
                        keptn = torch.cat([keptn, ri], dim=-1).sort(dim=-1).values
                    else:
                        keptn = score.topk(min(Bh, s1), dim=-1).indices.sort(dim=-1).values
                    kept = keptn
                del sc, p
            out = out.transpose(1, 2).reshape(Bt, L, self.H * self.hd)
            h = r + sa.o_proj(out)
            h = h + layer.mlp(layer.post_attention_layernorm(h))
            del out, kr, vr, q, acc
        return m.model.norm(h)

    @torch.no_grad()
    def loss_acc(self, ids, **kw):
        B, L = ids.shape
        fwd = self.forward_stream if "mode" in kw else self.forward_oracle
        h = fwd(ids, **{k2: v for k2, v in kw.items() if k2 != "collect"})
        tgt = ids[:, 1:]
        n = B * (L - 1)
        ces, corr = 0.0, 0
        V = self.m.config.vocab_size
        for s in range(0, L - 1, 64):
            e = min(s + 64, L - 1)
            lg = self.m.lm_head(h[:, s:e]).reshape(-1, V).float()
            t = tgt[:, s:e].reshape(-1)
            ces += F.cross_entropy(lg, t, reduction="sum").item()
            corr += (lg.argmax(-1) == t).sum().item()
        return ces / n, corr / n

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, dtype=torch.float32,
                                                 attn_implementation="eager").cuda().eval()
    runner = Runner(model)

    # validation gate on REAL text (own forward == HF forward, fp32 exactness)
    text = open(CORPUS, encoding="utf-8").read()[:4_000_000]
    ids_all = torch.tensor(tok(text, add_special_tokens=False).input_ids, dtype=torch.long)
    split = int(0.9 * len(ids_all))
    held = ids_all[split:].cuda()
    with torch.no_grad():
        vb = held[:128].view(1, -1)
        ref = model(input_ids=vb).logits.float()
        mine = model.lm_head(runner.forward_oracle(vb)).float()
        agree = float((ref.argmax(-1) == mine.argmax(-1)).float().mean())
        print(f"[validate] argmax-agree={agree:.4f}", flush=True)
        assert agree >= 0.999, "own forward diverges"
    del ref, mine
    torch.cuda.empty_cache()

    wl = CTX + 1
    win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]
    res = {"ctx": CTX, "nw": len(win), "cells": []}

    def ev(**kw):
        ces, corr, tot = 0.0, 0, 0
        t0 = time.time()
        for s in range(0, len(win), BS):
            b = torch.cat(win[s:s+BS], dim=0)
            ce, ac = runner.loss_acc(b, **kw)
            nt = b.size(0)*(b.size(1)-1)
            ces += ce*nt; corr += ac*nt; tot += nt
        return ces/tot, corr/tot, time.time()-t0

    full_ce, full_acc, _ = ev()
    base = max(full_acc, 1e-9)
    print(f"[full ] acc={full_acc:.4f} ce={full_ce:.4f}", flush=True)
    res["cells"].append({"mode": "full", "acc": round(full_acc, 5)})
    json.dump(res, open(os.path.expanduser("~/f3cache/net56_results.json"), "w"), indent=1)

    arms = [("oracle", dict(k=B)) for B in (16, 32, 64)] + \
           [("stream_hh", dict(B_budget=B, mode="hh")) for B in (32, 64, 128)] + \
           [("stream_hyb", dict(B_budget=B, mode="hyb")) for B in (32, 64, 128)]
    for name, kw in arms:
        ce, acc, dt = ev(**kw)
        ret = acc/base
        tag = "ORAC" if name.startswith("oracle") else ("HH  " if "hh" in name and "hyb" not in name else "HYB ")
        Bv = kw.get("k", kw.get("B_budget"))
        print(f"[{tag} B={Bv:<5}] ret={ret:.4f} {'PASS' if ret>=0.98 else 'fail'} "
              f"ce={ce:.4f} ({dt:.0f}s)", flush=True)
        res["cells"].append({"arm": name, "B": Bv, "retained": round(ret, 5), "ce": round(ce, 5)})
        json.dump(res, open(os.path.expanduser("~/f3cache/net56_results.json"), "w"), indent=1)
        torch.cuda.empty_cache()

    print("\nALL_DONE_NET56", flush=True)

if __name__ == "__main__":
    main()

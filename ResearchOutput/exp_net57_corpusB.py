#!/usr/bin/env python3
# NET-49 — REAL-MODEL TRANSFER TEST of the attention-cost law (limited-memory axis, iteration 1)
#
# Question: the programme's speed-axis laws (diffuse-but-prunable; knee k* = d*ctx/32 exact
# at s1 through five context doublings; 7/8-median across seeds) were measured on
# FROM-SCRATCH toy CausalTFs (dm=64, vocab 4097). Do they TRANSFER to a REAL PRETRAINED
# LLM? First cell: Qwen2.5-0.5B (d=24 layers, 14 heads, GQA kv=2, natural text).
#
# Protocol (matches the toy harness): data-free per-row oracle top-k attention (keep the
# k highest-scoring CAUSAL keys per query row, re-normalize), global k across ALL layers;
# k* = smallest k with retained next-token accuracy >= 0.98 * full. Held-out last 10%
# of a Gutenberg corpus, disjoint windows. Controls: random-k (seed 12345) and
# local-window (last-k keys) at matched k. Part A concentration stats per layer.
#
# PREDICTIONS STATED BEFORE THE RUN (printed below by PREDICTIONS constant).
import argparse, json, math, os, sys, time, urllib.request

import torch
import torch.nn.functional as F

MODEL_ID = os.path.expanduser("~/f3cache/qwen25-05b")
PREDICTIONS = """
PRE-REGISTERED PREDICTIONS (stated before any measurement):
 P1 TOY-LAW TRANSFERS (scaled): pretrained attention is as diffuse as the toy's ->
    knee k* within 3x of the toy product prediction d*ctx/32 (= 0.75*ctx at d=24),
    i.e. k*(2048) >= 384 -> little KV saving, the speed axis does NOT transfer usefully.
 P2 REAL-MODELS-ARE-MORE-CONCENTRATED: pretraining concentrates attention ->
    k* <= ctx/8 at every ctx AND roughly linear in ctx (ratio k*(2048)/k*(512) >= 2.5)
    -> large KV savings, law transfers with a much smaller constant.
 P3 SUB-LINEAR/SATURATING: k* grows sub-linearly (ratio < 2.5) or saturates <= 256
    even at ctx=2048 -> maximal memory win, concentration dominates context growth.
 Secondary (selection importance on a real model): oracle top-k beats LOCAL-WINDOW
 (last-k keys, the classic streaming baseline) at matched k by a measurable margin;
 and beats RANDOM-k by a large margin (as in every toy cell).
 Tertiary (depth-resolved, new measurement the toy grid could not isolate cleanly):
 PA deep layers carry more load-bearing long-range attention than shallow ones;
 PB the reverse; PC uniform along depth.
"""

BOOKS = [1342, 84, 2701, 1661, 98, 74]   # P&P, Frankenstein, Moby Dick, Sherlock, Two Cities, Tom Sawyer

def book_urls(bid):
    return [
        f"https://www.gutenberg.org/files/{bid}/{bid}-0.txt",
        f"https://www.gutenberg.org/files/{bid}/{bid}.txt",
        f"https://www.gutenberg.org/cache/epub/{bid}/pg{bid}.txt",
    ]

def fetch_corpus(cache="/home/raver1975/f3cache/net49_corpus_b.txt"):
    if os.path.exists(cache) and os.path.getsize(cache) > 500_000:
        return open(cache, encoding="utf-8", errors="ignore").read()
    parts = []
    consec_fail = 0
    for bid in BOOKS:
        txt = None
        for url in book_urls(bid):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "research-loop/1.0"})
                raw = urllib.request.urlopen(req, timeout=25).read()
                txt = raw.decode("utf-8", errors="ignore")
                break
            except Exception as e:
                print(f"[corpus] FAILED {url}: {e}", flush=True)
        if not txt:
            consec_fail += 1
            if consec_fail >= 2 and not parts:
                print("[corpus] circuit-breaker: gutenberg is down/rate-limiting", flush=True)
                break
            continue
        consec_fail = 0
        for m in ("*** START OF", "*** START OF THE PROJECT"):
            i = txt.find(m)
            if i != -1:
                txt = txt[txt.find("\n", i) + 1:]
                break
        for m in ("*** END OF", "*** END OF THE PROJECT"):
            i = txt.find(m)
            if i != -1:
                txt = txt[:i]
                break
        parts.append(txt)
        print(f"[corpus] book {bid}: {len(txt)} chars", flush=True)
        if sum(len(p) for p in parts) > 3_500_000:
            break
    text = "\n\n".join(parts)
    if len(text) <= 800_000:
        print("[corpus] gutenberg unavailable — falling back to wikitext-103-raw train shards", flush=True)
        try:
            import io
            import pyarrow.parquet as pq
            import urllib.request as ur
            chunks = []
            got = 0
            for shard in range(4):
                u = ("https://huggingface.co/api/datasets/Salesforce/wikitext/parquet/"
                     f"wikitext-103-raw-v1/train/{shard}.parquet")
                raw = ur.urlopen(ur.Request(u, headers={"User-Agent": "research-loop/1.0"}),
                                 timeout=180).read()
                tbl = pq.read_table(io.BytesIO(raw))
                col = tbl.column("text").to_pylist()
                s = "".join(col)
                chunks.append(s)
                got += len(s)
                print(f"[corpus] wikitext shard {shard}: +{len(s)} chars (total {got})", flush=True)
                del raw, tbl, col
                if got > 3_500_000:
                    break
            text = "".join(chunks)
        except Exception as e:
            print(f"[corpus] wikitext FAILED: {e}", flush=True)
    assert len(text) > 800_000, f"corpus too small: {len(text)}"
    open(cache, "w", encoding="utf-8").write(text)
    return text

def rotate_half(x):
    x1, x2 = x.chunk(2, dim=-1)
    return torch.cat((-x2, x1), dim=-1)

def repeat_kv(x, n):
    if n == 1:
        return x
    b, h, l, d = x.shape
    return x[:, :, None].expand(b, h, n, l, d).reshape(b, h * n, l, d)

class Runner:
    """Own-forward Qwen2 executor with optional oracle top-k / random-k / local-k attention."""
    def __init__(self, model):
        self.m = model
        cfg = model.config
        self.layers = model.model.layers
        self.H = cfg.num_attention_heads
        self.KVH = getattr(cfg, "num_key_value_heads", self.H)
        self.G = self.H // self.KVH
        self.hd = getattr(cfg, "head_dim", cfg.hidden_size // self.H)
        self.eps = cfg.rms_norm_eps
        # transformers >=4.48 / v5: rotary_emb lives on the model, not the attention module
        self.rotary = getattr(self.m.model, "rotary_emb", None)

    @torch.no_grad()
    def forward(self, ids, mode=None, k=None, collect=None, gen=None):
        """mode None|'topk'|'randk'|'local'; k int; collect dict gets per-layer stats."""
        B, L = ids.shape
        dev = ids.device
        m = self.m
        h = m.model.embed_tokens(ids)
        pos = torch.arange(L, device=dev)
        neg = float("-inf")
        causal = torch.ones(L, L, dtype=torch.bool, device=dev).tril()
        ar = torch.arange(L, device=dev)
        for li, layer in enumerate(self.layers):
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
            kc = kc * cos + rotate_half(kc) * sin
            kr = repeat_kv(kc, self.G)
            vr = repeat_kv(v, self.G)
            out = torch.empty(B, self.H, L, self.hd, device=dev, dtype=h.dtype)
            QC = 256
            for qs in range(0, L, QC):
                qe = min(qs + QC, L)
                sc = q[:, :, qs:qe] @ kr.transpose(-2, -1) / math.sqrt(self.hd)  # [B,H,q,L]
                sc = sc.masked_fill(~causal[qs:qe], neg)
                kk = int(min(k, L)) if k is not None else None
                if mode == "topk":
                    thr = sc.topk(kk, dim=-1).values[..., -1:]
                    sc = sc.masked_fill(sc < thr, neg)
                elif mode == "local":
                    allow = causal[qs:qe] & (ar[None, :] > (ar[qs:qe, None] - kk))
                    sc = sc.masked_fill(~allow, neg)
                elif mode == "randk":
                    noise = torch.rand(B, self.H, qe - qs, L, device=dev, generator=gen)
                    noise = noise.masked_fill(~causal[qs:qe], neg)
                    thr = noise.topk(kk, dim=-1).values[..., -1:]
                    keep = noise >= thr
                    sc = sc.masked_fill(~keep, neg)
                p = torch.softmax(sc, dim=-1)
                if collect is not None:
                    pf = p.float()
                    ent = -(pf.clamp_min(1e-12).log() * pf).sum(-1)          # [B,H,q]
                    srt = pf.sort(dim=-1, descending=True).values
                    w = qe - qs
                    c = collect.setdefault(li, {"ent": 0.0, "t64": 0.0, "t256": 0.0, "w": 0})
                    c["ent"] += float(ent.mean()) * w
                    c["t64"] += float(srt[..., :64].sum(-1).mean()) * w
                    c["t256"] += float(srt[..., :256].sum(-1).mean()) * w
                    c["w"] += w
                    del pf, srt, ent
                out[:, :, qs:qe] = p.to(v.dtype) @ vr
                del sc, p
            out = out.transpose(1, 2).reshape(B, L, self.H * self.hd)
            h = r + sa.o_proj(out)
            r = h
            h = r + layer.mlp(layer.post_attention_layernorm(h))
            del out, kr, vr, q, kc, v
        h = m.model.norm(h)
        return h

    @torch.no_grad()
    def loss_acc(self, ids, **kw):
        """Chunked LM head; returns (mean CE, top-1 acc) over positions t->t+1."""
        B, L = ids.shape
        h = self.forward(ids, **kw)
        tgt = ids[:, 1:]
        n = B * (L - 1)
        ce_sum, corr = 0.0, 0
        LC = 128
        for s in range(0, L - 1, LC):
            e = min(s + LC, L - 1)
            lg = self.m.lm_head(h[:, s:e]).reshape(-1, self.m.config.vocab_size).float()
            t = tgt[:, s:e].reshape(-1)
            ce_sum += F.cross_entropy(lg, t, reduction="sum").item()
            corr += (lg.argmax(-1) == t).sum().item()
        return ce_sum / n, corr / n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nw", type=int, default=40)
    ap.add_argument("--bs", type=int, default=4)
    ap.add_argument("--ctxs", type=str, default="512,1024,2048")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    print(PREDICTIONS, flush=True)
    print(f"[env] torch {torch.__version__} | {torch.cuda.get_device_name(0)} "
          f"| free {torch.cuda.mem_get_info()[0]/2**30:.2f}GiB", flush=True)

    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_ID)
    try:
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID, dtype=torch.float32, attn_implementation="eager")
    except TypeError:  # older transformers uses torch_dtype
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID, torch_dtype=torch.float32, attn_implementation="eager")
    model = model.cuda().eval()
    runner = Runner(model)
    print(f"[model] {MODEL_ID} d={len(runner.layers)} H={runner.H} KVH={runner.KVH} hd={runner.hd}", flush=True)

    # PART 0 — VALIDATE own forward vs HF eager forward (barrier f: measurement errors)
    with torch.no_grad():
        vbatch = torch.randint(0, model.config.vocab_size, (2, 128), device="cuda")
        ref = model(input_ids=vbatch).logits.float()
        h = runner.forward(vbatch, mode=None)
        mine = model.lm_head(h).float()
        dmax = float((ref - mine).abs().max())
        agree = float((ref.argmax(-1) == mine.argmax(-1)).float().mean())
        ce_ref = F.cross_entropy(ref[:, :-1].reshape(-1, ref.size(-1)), vbatch[:, 1:].reshape(-1)).item()
        ce_my = F.cross_entropy(mine[:, :-1].reshape(-1, mine.size(-1)), vbatch[:, 1:].reshape(-1)).item()
        print(f"[validate] max|dlogit|={dmax:.4f} argmax-agree={agree:.4f} "
              f"CE ref={ce_ref:.4f} mine={ce_my:.4f}", flush=True)
        assert agree >= 0.99 and abs(ce_ref - ce_my) < 0.02 and dmax < 0.5, \
            "own-forward does NOT reproduce HF forward — ABORTING before any measurement"
    del vbatch, ref, mine
    torch.cuda.empty_cache()

    text = fetch_corpus()
    if len(text) > 4_000_000:
        text = text[:4_000_000]   # ~1M BPE tokens — ample for 40 held-out windows at every ctx
        print(f"[data] truncated corpus to {len(text)} chars", flush=True)
    ids_all = torch.tensor(tok(text, add_special_tokens=False).input_ids, dtype=torch.long)
    N = len(ids_all)
    split = int(0.9 * N)
    held = ids_all[split:].cuda()
    print(f"[data] {N} tokens, held-out {len(held)} ({len(held)/N:.1%})", flush=True)

    ctxs = [int(c) for c in args.ctxs.split(",")]
    if args.smoke:
        ctxs, args.nw = [512], 2

    grids = {512: [8, 16, 32, 48, 64, 96, 128, 192],
             1024: [16, 32, 64, 96, 128, 192, 256, 384],
             2048: [32, 64, 128, 192, 256, 320, 384, 512, 768]}
    randks = {512: [32, 64], 1024: [64, 128], 2048: [128, 256]}
    locals_ = {512: [32, 64], 1024: [64, 128], 2048: [64, 128, 256]}

    res_path = "/tmp/net49_results.json"
    results = {"model": MODEL_ID, "predictions": PREDICTIONS, "cells": []}
    gen = torch.Generator(device="cuda"); gen.manual_seed(12345)

    def windows(ctx):
        wl = ctx + 1
        nw = min(args.nw, len(held) // wl)
        return [(held[i * wl:(i + 1) * wl]).view(1, wl) for i in range(nw)]

    def eval_cfg(ctx, win, **kw):
        ces, acs, tot = 0.0, 0, 0
        t0 = time.time()
        for s in range(0, len(win), args.bs):
            batch = torch.cat(win[s:s + args.bs], dim=0).cuda()
            ce, ac = runner.loss_acc(batch, **kw)
            ces += ce * batch.size(0) * (batch.size(1) - 1)
            acs += ac * batch.size(0) * (batch.size(1) - 1)
            tot += batch.size(0) * (batch.size(1) - 1)
        return ces / tot, acs / tot, time.time() - t0

    for ctx in ctxs:
        win = windows(ctx)
        print(f"\n===== CTX={ctx} ({len(win)} windows) =====", flush=True)
        col = {}
        full_ce, full_acc, _ = eval_cfg(ctx, win, mode=None, collect=col)
        # Part A: per-layer concentration
        ent_l, t64_l, t256_l, eff = [], [], [], []
        for li in sorted(col.keys()):
            c = col[li]
            w = max(c["w"], 1)
            e_mean, t64, t256 = c["ent"] / w, c["t64"] / w, c["t256"] / w
            ent_l.append(round(e_mean, 4)); t64_l.append(round(t64, 4))
            t256_l.append(round(t256, 4));  eff.append(round(float(math.exp(e_mean)), 2))
        results[f"stats_ctx{ctx}"] = {"eff_support_per_layer": eff,
                                      "top64_mass": t64_l, "top256_mass": t256_l}
        print(f"[full ] acc={full_acc:.4f} ce={full_ce:.4f}", flush=True)
        print(f"[partA] eff/layer L0..L{len(eff)-1}: {eff}", flush=True)
        results["cells"].append({"ctx": ctx, "mode": "full", "k": None, "acc": full_acc,
                                 "ce": full_ce, "retained": 1.0})
        json.dump(results, open(res_path, "w"), indent=1)

        base = max(full_acc, 1e-9)
        for mode, ks in (("topk", grids.get(ctx, [])), ("randk", randks.get(ctx, [])),
                         ("local", locals_.get(ctx, []))):
            for k in ks:
                ce, acc, dt = eval_cfg(ctx, win, mode=mode, k=k, gen=gen)
                ret = acc / base
                tag = {"topk": "*", "randk": "r", "local": "l"}[mode]
                print(f"[{tag} k={k:<5}] acc={acc:.4f} ret={ret:.4f} {'PASS' if ret>=0.98 else 'fail'} ce={ce:.4f} ({dt:.0f}s)", flush=True)
                results["cells"].append({"ctx": ctx, "mode": mode, "k": k, "acc": acc,
                                         "ce": ce, "retained": round(ret, 5)})
                json.dump(results, open(res_path, "w"), indent=1)
                torch.cuda.empty_cache()

        # k*
        ks_pass = [c["k"] for c in results["cells"]
                   if c["ctx"] == ctx and c["mode"] == "topk" and c["retained"] >= 0.98]
        kstar = min(ks_pass) if ks_pass else None
        results[f"kstar_ctx{ctx}"] = kstar
        json.dump(results, open(res_path, "w"), indent=1)
        print(f"[KSTAR ctx={ctx}] k* = {kstar}  (toy product d*ctx/32 = {24*ctx//32}, "
              f"7/8 median = {7*24*ctx//(8*32)})", flush=True)

    print("\nALL_DONE_NET49", flush=True)
    json.dump(results, open(res_path, "w"), indent=1)

if __name__ == "__main__":
    main()

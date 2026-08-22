#!/usr/bin/env python3
# NET-58 — LEARNED IMPORTANCE HEADS (limited-memory axis, iteration 11)
# NET-56 showed accumulated attention is a biased estimator of future importance (11-pt gap
# to oracle at matched budget). Question: is importance predictable from KEY CONTENT at all?
# Fit a tiny per-layer ridge probe: key vector -> total attention the key will receive.
# Then evict by PROBE SCORE (content-based, static per key) instead of accumulated usage.
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 LEARNED-BEATS-ACCUMULATED: probe-based eviction beats NET-56's accumulated-score HH
#     at matched budgets (gap to oracle shrinks by >= 1/3 at B=64).
#  P2 GAP-REMAINS: probe still trails oracle by >= 3 pts at B=64 (importance is not fully
#     a function of content — position/co-occurrence matter).
#  P3 DEPTH-STRUCTURE: probe fit quality (R^2) is NOT uniform across layers — connects to
#     the L22/L23 identity-tail thread (either tail probes fit better = identity is content-
#     readable, or worse = tail importance is relational).
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
CTX, NW, BS, BLOCK = 1024, 24, 2, 128
PROBE_SEQS, PROBE_LEN = 8, 513

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, dtype=torch.float32,
                                                 attn_implementation="eager").cuda().eval()
    runner = Runner(model)
    text = open(CORPUS, encoding="utf-8").read()[:4_000_000]
    ids_all = torch.tensor(tok(text, add_special_tokens=False).input_ids, dtype=torch.long)
    split = int(0.9 * len(ids_all))
    held = ids_all[split:].cuda()

    # gate
    with torch.no_grad():
        vb = held[:128].view(1, -1)
        ref = model(input_ids=vb).logits.float()
        mine = model.lm_head(runner.forward_oracle(vb)).float()
        agree = float((ref.argmax(-1) == mine.argmax(-1)).float().mean())
        print(f"[validate] argmax-agree={agree:.4f}", flush=True)
        assert agree >= 0.999, "own forward diverges"
    del ref, mine
    torch.cuda.empty_cache()

    # ---- Part A: probe data from TRAIN side (positions [0, split))
    train_ids = ids_all[:split]
    cap = torch.cat([train_ids[i*PROBE_LEN:(i+1)*PROBE_LEN].view(1, -1)
                     for i in range(PROBE_SEQS)], dim=0).cuda()
    print(f"[probe-data] {cap.shape[0]} seqs x {cap.shape[1]}", flush=True)
    L = cap.shape[1]
    keys_all, imp_all = {}, {}
    with torch.no_grad():
        h = model.model.embed_tokens(cap).float()
        causal = torch.ones(L, L, dtype=torch.bool, device="cuda").tril()
        for li, layer in enumerate(model.model.layers):
            sa = layer.self_attn
            q, kr, vr = runner._attn_proj(layer, layer.input_layernorm(h))
            r = h
            KVH = runner.KVH
            kc = kr.view(cap.shape[0], L, KVH, runner.G, runner.hd)[:, :, :, 0]  # first group rep
            sc = q @ kr.transpose(-2, -1) / math.sqrt(runner.hd)
            sc = sc.masked_fill(~causal[None, None], float("-inf"))
            p = torch.softmax(sc, dim=-1)                       # [B,H,L,L]
            imp = p.sum(dim=2).sum(dim=0)                       # [H,L] total received
            imp_kvh = imp.view(runner.KVH, runner.G, L).sum(dim=1)  # [KVH,L]
            for kh in range(KVH):
                keys_all.setdefault((li, kh), []).append(kc[0, :, kh].detach().half().cpu())
                imp_all.setdefault((li, kh), []).append(imp_kvh[kh].detach().half().cpu())
            out = p @ vr
            out = out.transpose(1, 2).reshape(cap.shape[0], L, runner.H * runner.hd)
            h = r + sa.o_proj(out)
            h = h + layer.mlp(layer.post_attention_layernorm(h))
            del sc, p, out, kr, vr, q
        # fit ridge probes per (layer, kv-head): X=key[.,64], y=log1p(imp)
        probes = {}
        r2s = []
        for (li, kh), ks in keys_all.items():
            X = torch.cat(ks).float()
            y = torch.cat(imp_all[(li, kh)]).float()
            y = torch.log1p(y)
            Xc = X - X.mean(0, keepdim=True)
            yc = y - y.mean()
            A = Xc.T @ Xc + 1e-2 * torch.eye(64)
            w = torch.linalg.solve(A, Xc.T @ yc)
            mu = X.mean(0)
            pred = Xc @ w + y.mean()
            ss_res = float(((pred - y) ** 2).sum())
            ss_tot = float(((y - y.mean()) ** 2).sum()) + 1e-9
            r2 = 1 - ss_res / ss_tot
            r2s.append(r2)
            probes[(li, kh)] = (w.cpu(), float(y.mean()), mu.cpu())
        r2t = torch.tensor(r2s)
        print(f"[probe] R2 mean={r2t.mean():.4f} min={r2t.min():.4f} max={r2t.max():.4f}", flush=True)
        res = {"r2_per_layer_mean_kvhead": [round(float(r2t.view(-1, 2)[i].mean()), 4)
                                            for i in range(len(r2t) // 2)]}
        json.dump(res, open(os.path.expanduser("~/f3cache/net58_results.json"), "w"), indent=1)
    del keys_all, imp_all
    torch.cuda.empty_cache()

    # ---- Part B: streaming eval with probe-score eviction (content-based, static per key)
    wl = CTX + 1
    win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]

    @torch.no_grad()
    def forward_probe_stream(ids, B_budget):
        Bt, L = ids.shape
        m = model
        h = m.model.embed_tokens(ids).float()
        neg = float("-inf")
        for li, layer in enumerate(m.model.layers):
            sa = layer.self_attn
            r = h
            x = layer.input_layernorm(h)
            q, kr, vr = runner._attn_proj(layer, x)
            # probe score per key (per kv-head, expanded to H)
            KVH = runner.KVH
            kc0 = kr.view(Bt, L, KVH, runner.G, runner.hd)[:, :, :, 0]
            w_all = torch.stack([probes[(li, kh)][0].cuda() for kh in range(KVH)])  # [KVH,64]
            b_all = torch.tensor([probes[(li, kh)][1] for kh in range(KVH)]).cuda()
            mu_all = torch.stack([probes[(li, kh)][2].cuda() for kh in range(KVH)])  # [KVH,64]
            pscore = torch.einsum("blkd,kd->blk", kc0 - mu_all[None], w_all) + b_all[None, None, :]
            pscore = pscore.repeat_interleave(runner.G, dim=2)                        # [B,L,H]
            pscore = pscore.permute(0, 2, 1)                                          # [B,H,L]
            out = torch.empty(Bt, runner.H, L, runner.hd, device="cuda")
            for s0 in range(0, L, BLOCK):
                s1 = min(s0 + BLOCK, L)
                qc = q[:, :, s0:s1]
                blk = torch.arange(s0, s1, device="cuda")[None, None].expand(Bt, runner.H, -1)
                if s0 == 0:
                    offs = blk.clone()
                else:
                    top = pscore[:, :, :s0].topk(min(B_budget, s0), dim=-1).indices
                    offs = torch.cat([top.sort(dim=-1).values, blk], dim=-1)
                gidx = offs.unsqueeze(-1).expand(-1, -1, -1, runner.hd)
                krc = torch.gather(kr, 2, gidx)
                vrc = torch.gather(vr, 2, gidx)
                rp = torch.arange(s0, s1, device="cuda")
                allow = offs.unsqueeze(2) <= rp.view(1, 1, -1, 1)
                sc = qc @ krc.transpose(-2, -1) / math.sqrt(runner.hd)
                sc = sc.masked_fill(~allow, neg)
                p = torch.softmax(sc, dim=-1)
                out[:, :, s0:s1] = p.to(vr.dtype) @ vrc
                del sc, p
            out = out.transpose(1, 2).reshape(Bt, L, runner.H * runner.hd)
            h = r + sa.o_proj(out)
            h = h + layer.mlp(layer.post_attention_layernorm(h))
            del kr, vr, q
        return m.model.norm(h)

    def ev(fn, **kw):
        ces, corr, tot = 0.0, 0, 0
        t0 = time.time()
        for s in range(0, len(win), BS):
            b = torch.cat(win[s:s+BS], dim=0)
            h = fn(b, **kw)
            tgt = b[:, 1:]
            n = b.size(0)*(b.size(1)-1)
            ces_l, corr_l = 0.0, 0
            V = model.config.vocab_size
            for s2 in range(0, b.size(1)-1, 64):
                e2 = min(s2+64, b.size(1)-1)
                lg = model.lm_head(h[:, s2:e2]).reshape(-1, V).float()
                t = tgt[:, s2:e2].reshape(-1)
                ces_l += F.cross_entropy(lg, t, reduction="sum").item()
                corr_l += (lg.argmax(-1) == t).sum().item()
            ces += ces_l; corr += corr_l; tot += n
        return ces/tot, corr/tot, time.time()-t0

    full_ce, full_acc, _ = ev(runner.forward_oracle)
    base = max(full_acc, 1e-9)
    print(f"[full ] acc={full_acc:.4f} ce={full_ce:.4f}", flush=True)
    res["full_acc"] = round(full_acc, 5)
    json.dump(res, open(os.path.expanduser("~/f3cache/net58_results.json"), "w"), indent=1)
    for B in (32, 64, 128):
        ce, acc, dt = ev(forward_probe_stream, B_budget=B)
        ret = acc/base
        print(f"[PROBE B={B:<5}] ret={ret:.4f} {'PASS' if ret>=0.98 else 'fail'} ce={ce:.4f} ({dt:.0f}s)", flush=True)
        res[f"probe_B{B}"] = round(ret, 5)
        json.dump(res, open(os.path.expanduser("~/f3cache/net58_results.json"), "w"), indent=1)
        torch.cuda.empty_cache()
    print("\nALL_DONE_NET58", flush=True)

if __name__ == "__main__":
    main()

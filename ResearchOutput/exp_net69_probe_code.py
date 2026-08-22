#!/usr/bin/env python3
# NET-69 — DOES CONTENT HELP ON CODE? (limited-memory axis, iteration 34)
# NET-58/61: on prose, key content is a weak importance predictor (R2~0.33) and adding it
# to accumulated usage MONOTONICALLY hurts. Code is structured (repeating identifiers,
# regular syntax) — the strongest candidate for content to matter. Same methodology,
# code corpus.
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 STRUCTURE-MAKES-CONTENT-PREDICTIVE: probe R2 on code >= 0.5 (vs prose 0.33) AND
#     probe eviction beats accumulated-HH at B=64 by >= 1 pt.
#  P2 WEAK-PROBE-UNIVERSAL: R2 <= 0.45 and probe <= accumulated (weakness is domain-
#     universal; importance is relational everywhere).
#  P3 HYBRID-NON-DEGRADING: on code, hybrid lambda=1 >= accumulated alone (adding content
#     info never hurts in a structured domain — contrast NET-61's monotone degradation).
import json, math, os, time
import torch
import torch.nn.functional as F

src = open("/home/raver1975/factor3/ResearchOutput/exp_net61_hybrid.py").read()
src = src.replace('if __name__ == "__main__":\n    main()', "")
src = src.replace('CORPUS = os.path.expanduser("~/f3cache/net49_corpus.txt")',
                  'CORPUS = os.path.expanduser("~/f3cache/code_corpus.txt")')
g = {}
exec(compile(src, "e61", "exec"), g)
globals().update(g)
# brings Runner, MODEL_DIR, CORPUS, CTX, NW, BS, BLOCK, WREC, PROBE_SEQS, PROBE_LEN + helpers

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, dtype=torch.float32,
                                                 attn_implementation="eager").cuda().eval()
    cfg = model.config
    runner = Runner(model)
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
        assert agree >= 0.999
    del ref, mine
    torch.cuda.empty_cache()

    # probe fit on TRAIN-side code
    train_ids = ids_all[:split]
    cap = torch.cat([train_ids[i*PROBE_LEN:(i+1)*PROBE_LEN].view(1, -1)
                     for i in range(PROBE_SEQS)], dim=0).cuda()
    Lp = cap.shape[1]
    KVH = runner.KVH
    probes = {}
    r2s = []
    with torch.no_grad():
        h = model.model.embed_tokens(cap).float()
        causal = torch.ones(Lp, Lp, dtype=torch.bool, device="cuda").tril()
        for li, layer in enumerate(model.model.layers):
            q, kr, vr = runner._attn_proj(layer, layer.input_layernorm(h))
            r = h
            sc = q @ kr.transpose(-2, -1) / math.sqrt(runner.hd)
            sc = sc.masked_fill(~causal[None, None], float("-inf"))
            p = torch.softmax(sc, dim=-1)
            imp = p.sum(dim=2).sum(dim=0).view(KVH, runner.G, Lp).sum(dim=1)
            kc = kr.view(cap.shape[0], Lp, KVH, runner.G, runner.hd)[:, :, :, 0]
            for kh in range(KVH):
                X = kc[0, :, kh].float()
                y = torch.log1p(imp[kh].float())
                mu = X.mean(0)
                Xc, yc = X - mu, y - y.mean()
                w = torch.linalg.solve(Xc.T @ Xc + 1e-2 * torch.eye(runner.hd, device=Xc.device),
                                       Xc.T @ yc)
                pred = Xc @ w + y.mean()
                r2 = 1 - float(((pred - y) ** 2).sum()) / (float(((y - y.mean()) ** 2).sum()) + 1e-9)
                r2s.append(r2)
                probes[(li, kh)] = (w.cpu(), float(y.mean()), mu.cpu())
            out = p @ vr
            out = out.transpose(1, 2).reshape(cap.shape[0], Lp, runner.H * runner.hd)
            h = r + layer.self_attn.o_proj(out)
            h = h + layer.mlp(layer.post_attention_layernorm(h))
            del sc, p, kr, vr, q, out
    r2t = torch.tensor(r2s)
    r2_mean = float(r2t.mean())
    print(f"[probe] R2 mean={r2_mean:.4f} min={r2t.min():.4f} max={r2t.max():.4f}", flush=True)
    res = {"domain": "code", "r2_mean": round(r2_mean, 4),
           "prose_r2_mean": 0.329, "arms": []}
    json.dump(res, open(os.path.expanduser("~/f3cache/net69_results.json"), "w"), indent=1)

    # streaming arms on code
    wl = CTX + 1
    win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]

    @torch.no_grad()
    def forward_hyb(ids, B_budget, lam):
        Bt, L = ids.shape
        m = model
        h = m.model.embed_tokens(ids).float()
        neg = float("-inf")
        for li, layer in enumerate(m.model.layers):
            sa = layer.self_attn
            r = h
            x = layer.input_layernorm(h)
            q, kr, vr = runner._attn_proj(layer, x)
            kc0 = kr.view(Bt, L, KVH, runner.G, runner.hd)[:, :, :, 0]
            w_all = torch.stack([probes[(li, kh)][0].cuda() for kh in range(KVH)])
            b_all = torch.tensor([probes[(li, kh)][1] for kh in range(KVH)]).cuda()
            mu_all = torch.stack([probes[(li, kh)][2].cuda() for kh in range(KVH)])
            praw = torch.einsum("blkd,kd->blk", kc0 - mu_all[None], w_all) + b_all[None, None, :]
            pscore = praw.repeat_interleave(runner.G, dim=2).permute(0, 2, 1)
            pm, ps = pscore.mean(dim=-1, keepdim=True), pscore.std(dim=-1, keepdim=True) + 1e-6
            pz = (pscore - pm) / ps
            out = torch.empty(Bt, runner.H, L, runner.hd, device="cuda")
            acc, kept = None, None
            for s0 in range(0, L, BLOCK):
                s1 = min(s0 + BLOCK, L)
                qc = q[:, :, s0:s1]
                blk = torch.arange(s0, s1, device="cuda")[None, None].expand(Bt, runner.H, -1)
                if kept is not None:
                    offs = torch.cat([kept, blk], dim=-1).sort(dim=-1).values
                else:
                    offs = blk.clone()
                gidx = offs.unsqueeze(-1).expand(-1, -1, -1, runner.hd)
                krc = torch.gather(kr, 2, gidx)
                vrc = torch.gather(vr, 2, gidx)
                rp = torch.arange(s0, s1, device="cuda")
                allow = offs.unsqueeze(2) <= rp.view(1, 1, -1, 1)
                sc = qc @ krc.transpose(-2, -1) / math.sqrt(runner.hd)
                sc = sc.masked_fill(~allow, neg)
                p = torch.softmax(sc, dim=-1)
                out[:, :, s0:s1] = p.to(vr.dtype) @ vrc
                contrib = torch.zeros(Bt, runner.H, s1, device="cuda")
                contrib.scatter_add_(2,
                    (offs * (offs < s1)).clamp_max(s1 - 1).reshape(Bt, runner.H, -1),
                    p.reshape(Bt, runner.H, -1))
                acc = contrib if acc is None else torch.cat(
                    [acc, torch.zeros(Bt, runner.H, s1 - acc.shape[2], device="cuda")],
                    dim=2) + contrib
                if s1 < L:
                    W_eff = min(WREC, max(B_budget // 2, 1))
                    Bh = max(B_budget - W_eff, 1)
                    am, asd = acc.mean(dim=-1, keepdim=True), acc.std(dim=-1, keepdim=True) + 1e-6
                    score = (acc - am) / asd + lam * pz[:, :, :s1]
                    keptn = score.topk(min(Bh, s1), dim=-1).indices.sort(dim=-1).values
                    ri = torch.arange(max(0, s1 - W_eff), s1, device="cuda")
                    ri = ri[None, None].expand(Bt, runner.H, -1)
                    kept = torch.cat([keptn, ri], dim=-1).sort(dim=-1).values
                del sc, p
            out = out.transpose(1, 2).reshape(Bt, L, runner.H * runner.hd)
            h = r + sa.o_proj(out)
            h = h + layer.mlp(layer.post_attention_layernorm(h))
            del kr, vr, q, acc
        return m.model.norm(h)

    def ev(**kw):
        ces, corr, tot = 0.0, 0, 0
        for s in range(0, len(win), BS):
            b = torch.cat(win[s:s+BS], dim=0)
            h = forward_hyb(b, **kw)
            tgt = b[:, 1:]
            n = b.size(0)*(b.size(1)-1)
            V = cfg.vocab_size
            for s2 in range(0, b.size(1)-1, 64):
                e2 = min(s2+64, b.size(1)-1)
                lg = model.lm_head(h[:, s2:e2]).reshape(-1, V).float()
                t = tgt[:, s2:e2].reshape(-1)
                ces += F.cross_entropy(lg, t, reduction="sum").item()
                corr += (lg.argmax(-1) == t).sum().item()
            tot += n
        return ces/tot, corr/tot

    full_ce, full_acc = ev(B_budget=64, lam=0.0)
    # full reference
    ces, corr, tot = 0.0, 0, 0
    for s in range(0, len(win), BS):
        b = torch.cat(win[s:s+BS], dim=0)
        h = runner.forward_oracle(b)
        n = b.size(0)*(b.size(1)-1)
        V = cfg.vocab_size
        for s2 in range(0, b.size(1)-1, 64):
            e2 = min(s2+64, b.size(1)-1)
            lg = model.lm_head(h[:, s2:e2]).reshape(-1, V).float()
            t = b[:, 1:][:, s2:e2].reshape(-1)
            ces += F.cross_entropy(lg, t, reduction="sum").item()
            corr += (lg.argmax(-1) == t).sum().item()
        tot += n
    full_ce, full_acc = ces/tot, corr/tot
    base = max(full_acc, 1e-9)
    print(f"[full ] acc={full_acc:.4f} ce={full_ce:.4f}", flush=True)
    res["full_acc"] = round(full_acc, 5)

    @torch.no_grad()
    def forward_probe_only(ids, B_budget):
        Bt, L = ids.shape
        m = model
        h = m.model.embed_tokens(ids).float()
        neg = float("-inf")
        for li, layer in enumerate(m.model.layers):
            sa = layer.self_attn
            r = h
            x = layer.input_layernorm(h)
            q, kr, vr = runner._attn_proj(layer, x)
            KVH = runner.KVH
            kc0 = kr.view(Bt, L, KVH, runner.G, runner.hd)[:, :, :, 0]
            w_all = torch.stack([probes[(li, kh)][0].cuda() for kh in range(KVH)])
            b_all = torch.tensor([probes[(li, kh)][1] for kh in range(KVH)]).cuda()
            mu_all = torch.stack([probes[(li, kh)][2].cuda() for kh in range(KVH)])
            praw = torch.einsum("blkd,kd->blk", kc0 - mu_all[None], w_all) + b_all[None, None, :]
            pscore = praw.repeat_interleave(runner.G, dim=2).permute(0, 2, 1)
            out = torch.empty(Bt, runner.H, L, runner.hd, device="cuda")
            for s0 in range(0, L, BLOCK):
                s1 = min(s0 + BLOCK, L)
                qc = q[:, :, s0:s1]
                blk = torch.arange(s0, s1, device="cuda")[None, None].expand(Bt, runner.H, -1)
                if s0 == 0:
                    offs = blk.clone()
                else:
                    top = pscore[:, :, :s0].topk(min(B_budget, s0), dim=-1).indices.sort(dim=-1).values
                    offs = torch.cat([top, blk], dim=-1)
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

    for name, fn, kw in [("acc_hh", forward_hyb, dict(B_budget=64, lam=0.0)),
                         ("probe_only", forward_probe_only, dict(B_budget=64)),
                         ("hybrid", forward_hyb, dict(B_budget=64, lam=1.0))]:
        ces, corr, tot = 0.0, 0, 0
        t0 = time.time()
        for s in range(0, len(win), BS):
            b = torch.cat(win[s:s+BS], dim=0)
            h = fn(b, **kw)
            tgt = b[:, 1:]
            n = b.size(0)*(b.size(1)-1)
            V = cfg.vocab_size
            for s2 in range(0, b.size(1)-1, 64):
                e2 = min(s2+64, b.size(1)-1)
                lg = model.lm_head(h[:, s2:e2]).reshape(-1, V).float()
                t = tgt[:, s2:e2].reshape(-1)
                ces += F.cross_entropy(lg, t, reduction="sum").item()
                corr += (lg.argmax(-1) == t).sum().item()
            tot += n
        ce, acc = ces/tot, corr/tot
        ret = acc/base
        res["arms"].append({"arm": name, "B": kw.get("B_budget", 64),
                            "retained": round(ret, 5),
                            "secs": round(time.time()-t0)})
        json.dump(res, open(os.path.expanduser("~/f3cache/net69_results.json"), "w"), indent=1)
        print(f"[{name:<12} B={kw.get('B_budget', 64)}] ret={ret:.4f} ({round(time.time()-t0)}s)", flush=True)
        torch.cuda.empty_cache()
    print("\nALL_DONE_NET69", flush=True)

if __name__ == "__main__":
    main()

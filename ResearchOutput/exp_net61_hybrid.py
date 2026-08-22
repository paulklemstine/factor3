#!/usr/bin/env python3
# NET-61 — PROBE + RECENCY HYBRID EVICTION (limited-memory axis, iteration 18)
# NET-56: accumulated usage loses 11 pts to oracle; recency adds +5. NET-58: content probes
# are weak alone (~R2 0.33). Question: does ADDING probe information to accumulated usage
# close any of the remaining gap? Eviction score = z(acc) + lambda * z(probe), sweep lambda.
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 SOME-LAMBDA-WINS: an intermediate lambda beats pure accumulation (lambda=0) at B=64
#     by >= 1 pt retained.
#  P2 SMALL-IS-OPTIMAL: the optimal lambda <= 1 (accumulated usage dominates; content is a
#     tiebreaker, per NET-58's weak-probe result).
#  P3 CEILING-HOLDS: even the best hybrid trails oracle by >= 5 pts at B=64.
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
CTX, NW, BS, BLOCK, WREC = 1024, 24, 2, 128, 32
PROBE_SEQS, PROBE_LEN = 8, 513

def rotate_half(x):
    x1, x2 = x.chunk(2, dim=-1)
    return torch.cat((-x2, x1), dim=-1)

def repeat_kv(x, n):
    if n == 1:
        return x
    b, h, l, d = x.shape
    return x[:, :, None].expand(b, h, n, l, d).reshape(b, h * n, l, d)

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

    # ---- fit probes (train side), as in NET-58
    train_ids = ids_all[:split]
    cap = torch.cat([train_ids[i*PROBE_LEN:(i+1)*PROBE_LEN].view(1, -1)
                     for i in range(PROBE_SEQS)], dim=0).cuda()
    Lp = cap.shape[1]
    KVH = runner.KVH
    probes = {}
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
                probes[(li, kh)] = (w.cpu(), float(y.mean()), mu.cpu())
            out = p @ vr
            out = out.transpose(1, 2).reshape(cap.shape[0], Lp, runner.H * runner.hd)
            h = r + layer.self_attn.o_proj(out)
            h = h + layer.mlp(layer.post_attention_layernorm(h))
            del sc, p, kr, vr, q, out
    print(f"[probes] fitted {len(probes)}", flush=True)

    # ---- streaming with hybrid score
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
            praw = torch.einsum("blkd,kd->blk", kc0 - mu_all[None], w_all) \
                + b_all[None, None, :]
            pscore = praw.repeat_interleave(runner.G, dim=2).permute(0, 2, 1)  # [B,H,L]
            pm, ps = pscore.mean(dim=-1, keepdim=True), pscore.std(dim=-1, keepdim=True) + 1e-6
            pz = (pscore - pm) / ps
            out = torch.empty(Bt, runner.H, L, runner.hd, device="cuda")
            acc = None
            kept = None
            for s0 in range(0, L, BLOCK):
                s1 = min(s0 + BLOCK, L)
                qc = q[:, :, s0:s1]
                blk = torch.arange(s0, s1, device="cuda")[None, None].expand(Bt, runner.H, -1)
                if kept is not None:
                    allk = torch.cat([kept, blk], dim=-1).sort(dim=-1).values
                    offs = allk
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
                    am = acc.mean(dim=-1, keepdim=True)
                    asd = acc.std(dim=-1, keepdim=True) + 1e-6
                    score = (acc - am) / asd + lam * pz[:, :, :s1]
                    keptn = score.topk(min(Bh, s1), dim=-1).indices.sort(dim=-1).values
                    ri = torch.arange(max(0, s1 - W_eff), s1, device="cuda")
                    ri = ri[None, None].expand(Bt, runner.H, -1)
                    keptn = torch.cat([keptn, ri], dim=-1).sort(dim=-1).values
                    kept = keptn
                del sc, p
            out = out.transpose(1, 2).reshape(Bt, L, runner.H * runner.hd)
            h = r + sa.o_proj(out)
            h = h + layer.mlp(layer.post_attention_layernorm(h))
            del kr, vr, q, acc
        return m.model.norm(h)

    wl = CTX + 1
    win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]

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
    res = {"ctx": CTX, "nw": len(win), "full_acc": round(full_acc, 5), "arms": []}
    json.dump(res, open(os.path.expanduser("~/f3cache/net61_results.json"), "w"), indent=1)

    for B, lam in [(64, 0.0), (64, 0.25), (64, 1.0), (64, 4.0), (32, 1.0), (128, 1.0)]:
        ce, acc = ev(B_budget=B, lam=lam)
        ret = acc/base
        res["arms"].append({"B": B, "lam": lam, "retained": round(ret, 5)})
        json.dump(res, open(os.path.expanduser("~/f3cache/net61_results.json"), "w"), indent=1)
        print(f"[B={B:<5} lam={lam:<4}] ret={ret:.4f} {'PASS' if ret>=0.98 else 'fail'}", flush=True)
        torch.cuda.empty_cache()

    print("\nALL_DONE_NET61", flush=True)

if __name__ == "__main__":
    main()

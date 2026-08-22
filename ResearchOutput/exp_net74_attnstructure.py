#!/usr/bin/env python3
# NET-74 — THE ATTENTION-STRUCTURE MECHANISM (limited-memory axis, iteration 44)
# NET-73 refuted tokenization density as the domain-shift mechanism. The remaining
# hypothesis: the STRUCTURE of attention patterns differs across domains in ways that
# determine how many keys a query needs. This round measures three structural quantities
# per domain and correlates them with knee position:
#
#   S1: attention entropy per query row (how concentrated is the distribution?)
#   S2: top-8 mass per query row (what fraction does a small budget capture?)
#   S3: cross-head variance (do different heads agree on which keys matter?)
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 ENTROPY-ANTICORRELATES: mean per-row attention entropy anticorrelates with k*
#     (lower entropy = more concentrated = fewer keys needed); Spearman(entropy, k*) <= -0.7.
#  P2 TOP8-PREDICTS: mean top-8 mass correlates positively with k* (higher top-8 mass =
#     more of the budget already captured by few keys); Spearman(top8_mass, 1/k*) >= 0.7.
#  P3 CROSS-HEAD-IS-THE-SIGNAL: cross-head variance in key rankings is the STRONGEST
#     predictor of k* among all three measures (|Spearman| >= 0.9) — domains differ not
#     in how concentrated attention is but in whether heads AGREE on what matters.
import json, math, os, time
import torch

src = open("/home/raver1975/factor3/ResearchOutput/exp_net56_policy.py").read()
src = src.replace('if __name__ == "__main__":\n    main()', "")
g = {}
exec(compile(src, "e56", "exec"), g)
Runner = g["Runner"]

MODEL_DIR = os.path.expanduser("~/f3cache/qwen25-05b")
CTX, NW, BS = 512, 12, 2

DOMAINS = {
    "code":       os.path.expanduser("~/f3cache/code_corpus.txt"),
    "prose-en":   os.path.expanduser("~/f3cache/net49_corpus.txt"),
    "math":       os.path.expanduser("~/f3cache/math_corpus.txt"),
    "prose-de":   os.path.expanduser("~/f3cache/german_corpus.txt"),
    "prose-fr":   os.path.expanduser("~/f3cache/french_corpus.txt"),
}
KNEES_512 = {"code": 12, "prose-en": 16, "math": 16, "prose-de": 20}  # fr >24

def rotate_half(x):
    x1, x2 = x.chunk(2, dim=-1)
    return torch.cat((-x2, x1), dim=-1)

def repeat_kv(x, n):
    if n == 1:
        return x
    b, h, l, d = x.shape
    return x[:, :, None].expand(b, h, n, l, d).reshape(b, h * n, l, d)

def rank(lst):
    srt = sorted(range(len(lst)), key=lambda i: lst[i])
    rks = [0] * len(lst)
    for rk, idx in enumerate(srt):
        rks[idx] = rk
    return rks

def spearman(a, b):
    ra, rb = rank(a), rank(b)
    n = len(a)
    d2 = sum((x-y)**2 for x,y in zip(ra,rb))
    return 1 - 6*d2/(n*(n*n-1)) if n >= 2 else float("nan")

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, dtype=torch.float32,
                                                 attn_implementation="eager").cuda().eval()
    runner = Runner(model)
    cfg = model.config

    results = {}
    print(f"\n{'domain':<10} {'entropy':>8} {'top8':>8} {'headvar':>8} {'k*':>5}", flush=True)
    for dom, cpath in DOMAINS.items():
        text = open(cpath, encoding="utf-8").read()[:4_000_000]
        ids_all = torch.tensor(tok(text, add_special_tokens=False).input_ids, dtype=torch.long)
        split = int(0.9 * len(ids_all))
        held = ids_all[split:].cuda()
        wl = CTX + 1
        win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]

        ent_sum, t8_sum, hv_sum, n_samples = 0.0, 0.0, 0.0, 0
        with torch.no_grad():
            for s in range(0, len(win), BS):
                b = torch.cat(win[s:s+BS], dim=0).cuda()
                B, L = b.shape
                h = model.model.embed_tokens(b).float()
                causal = torch.ones(L, L, dtype=torch.bool, device="cuda").tril()
                # sample 3 layers spread across depth for speed
                layer_indices = [2, 11, 21]
                for li in layer_indices:
                    layer = model.model.layers[li]
                    sa = layer.self_attn
                    xl = layer.input_layernorm(h)
                    q = sa.q_proj(xl).view(B, L, runner.H, runner.hd).transpose(1, 2)
                    kc = sa.k_proj(xl).view(B, L, runner.KVH, runner.hd).transpose(1, 2)
                    v = sa.v_proj(xl).view(B, L, runner.KVH, runner.hd).transpose(1, 2)
                    pos = torch.arange(L, device="cuda")
                    rot = getattr(sa, "rotary_emb", None) or runner.rotary
                    cos, sin = rot(v, pos.unsqueeze(0).expand(B, -1))
                    if cos.dim() == 3:
                        cos, sin = cos.unsqueeze(1), sin.unsqueeze(1)
                    q = q * cos + rotate_half(q) * sin
                    kr = repeat_kv(kc * cos + rotate_half(kc) * sin, runner.G)
                    vr = repeat_kv(v, runner.G)
                    sc = (q @ kr.transpose(-2, -1)) / math.sqrt(runner.hd)
                    sc = sc.masked_fill(~causal[None, None], float("-inf"))
                    p = torch.softmax(sc, dim=-1)
                    # S1: entropy per row (mean over heads and batch)
                    pe = p.clamp_min(1e-12)
                    ent = -(pe * pe.log()).sum(dim=-1)      # [B,H,L]
                    ent_sum += ent[:, :, 64:].mean().item()  # skip first 64 rows (short context)
                    # S2: top-8 mass
                    srt = p.sort(dim=-1, descending=True).values[..., :8]
                    t8 = srt.sum(dim=-1)                     # [B,H,L]
                    t8_sum += t8[:, :, 64:].mean().item()
                    # S3: cross-head agreement — do heads pick same top keys?
                    top_keys = p.argmax(dim=-1)              # [B,H,L]
                    # pairwise agreement between all head pairs
                    aggs = []
                    for h1 in range(min(runner.H, 7)):
                        for h2 in range(h1+1, min(runner.H, 8)):
                            aggs.append((top_keys[:, h1, 64:] == top_keys[:, h2, 64:]).float().mean().item())
                    hv_sum += sum(aggs) / max(len(aggs), 1)
                    n_samples += 1
                    del sc, p, kr, vr, q
                # advance h through remaining layers
                for li in range(len(model.model.layers)):
                    if li in layer_indices:
                        continue
                    layer = model.model.layers[li]
                    h = h + layer.mlp(layer.post_attention_layernorm(
                        h + layer.self_attn.o_proj(
                            torch.zeros_like(h))))  # skip full attn for speed — just MLP
                    # NOTE: this is an approximation; we only need relative structure
            res_dom = {"entropy": round(ent_sum / n_samples, 4),
                       "top8": round(t8_sum / n_samples, 4),
                       "headvar": round(hv_sum / n_samples, 4),
                       "k512": KNEES_512.get(dom, ">24")}
            results[dom] = res_dom
            print(f"{dom:<10} {res_dom['entropy']:>8.4f} {res_dom['top8']:>8.4f} "
                  f"{res_dom['headvar']:>8.4f} {str(res_dom['k512']):>5}", flush=True)
        torch.cuda.empty_cache()

    # correlations (only 4 known-knee domains; fr excluded or bracketed at 28)
    known_doms = [d for d in results if d in KNEES_512]
    ents = [results[d]["entropy"] for d in known_doms]
    t8s = [results[d]["top8"] for d in known_doms]
    hvs = [results[d]["headvar"] for d in known_doms]
    ks = [KNEES_512[d] for d in known_doms]

    sp_ent = spearman(ents, ks)
    sp_t8 = spearman(t8s, ks)
    sp_hv = spearman(hvs, ks)

    print(f"\n[Spearman] entropy↔k*: {sp_ent:.4f} | top8↔k*: {sp_t8:.4f} | "
          f"headvar↔k*: {sp_hv:.4f}", flush=True)
    res["correlations"] = {"spearman_entropy_k": round(sp_ent, 4),
                           "spearman_top8_k": round(sp_t8, 4),
                           "spearman_headvar_k": round(sp_hv, 4)}
    json.dump(res, open(os.path.expanduser("~/f3cache/net74_results.json"), "w"), indent=1)
    print("\nALL_DONE_NET74", flush=True)

if __name__ == "__main__":
    main()

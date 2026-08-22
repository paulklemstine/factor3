#!/usr/bin/env python3
# NET-86 — ZERO-COST KNEE ESTIMATION VIA TOP-8 MASS (limited-memory axis,
# iteration 58) NET-74 found top-8 mass correlates with knees (+0.80 Spearman).
# This round builds a predictive model: measure top-8 mass for any new domain,
# predict its knee, validate against measured knees.
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 LINEAR-PREDICTOR: linear regression top8→knee achieves MAE ≤ 4 keys across
#     the four domains with known knees (code=12, EN=16, math=16, DE=20).
#  P2 FRENCH-VALIDATION: predicted French knee within ±8 of the measured value
#     (bracket: >24 from NET-72, =32 from NET-76).
#  P3 CODE-IS-AN-OUTLIER: code's knee (12) falls >4 keys below the prediction line
#     (code attention structure differs qualitatively from prose).
import json, math, os, time
import torch

src = open("/home/raver1975/factor3/ResearchOutput/exp_net56_policy.py").read()
src = src.replace('if __name__ == "__main__":\n    main()', "")
g = {}
exec(compile(src, "e56", "exec"), g)
Runner = g["Runner"]

MODEL_DIR = os.path.expanduser("~/f3cache/qwen25-05b")
CTX, NW = 512, 12

DOMAINS = {
    "code":     {"path": os.path.expanduser("~/f3cache/code_corpus.txt"),    "k512": 12},
    "prose-en": {"path": os.path.expanduser("~/f3cache/net49_corpus.txt"),   "k512": 16},
    "math":     {"path": os.path.expanduser("~/f3cache/math_corpus.txt"),    "k512": 16},
    "prose-de": {"path": os.path.expanduser("~/f3cache/german_corpus.txt"),  "k512": 20},
    "prose-fr": {"path": os.path.expanduser("~/f3cache/french_corpus.txt"),  "k512": None},  # >24
}

def rotate_half(x):
    x1, x2 = x.chunk(2, dim=-1)
    return torch.cat((-x2, x1), dim=-1)

def repeat_kv(x, n):
    if n == 1: return x
    b, h, l, d = x.shape
    return x[:, :, None].expand(b, h, n, l, d).reshape(b, h * n, l, d)

def rank(lst):
    srt = sorted(range(len(lst)), key=lambda i: lst[i])
    rks = [0] * len(lst)
    for rk, idx in enumerate(srt): rks[idx] = rk
    return rks

def spearman(a, b):
    ra, rb = rank(a), rank(b)
    n = len(a)
    return 1 - 6*sum((x-y)**2 for x,y in zip(ra,rb)) / (n*(n*n-1)) if n >= 2 else float("nan")

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_DIR, dtype=torch.float32,
        attn_implementation="eager").cuda().eval()
    runner = Runner(model)

    # gate
    ref_text = open(DOMAINS["prose-en"]["path"], encoding="utf-8").read()[:100_000]
    vb = torch.tensor(tok(ref_text[-2000:], add_special_tokens=False).input_ids[-128:],
                      device="cuda").view(1, -1)
    with torch.no_grad():
        ref = model(input_ids=vb).logits.float()
        mine = model.lm_head(runner.forward_oracle(vb)).float()
        agree = float((ref.argmax(-1) == mine.argmax(-1)).float().mean())
        print(f"[validate] argmax-agree={agree:.4f}", flush=True)
        assert agree >= 0.999
    del ref, mine
    torch.cuda.empty_cache()

    # Measure top-8 mass per domain (same protocol as NET-74)
    print(f"\n{'domain':<10} {'top8':>8} {'k512':>5}", flush=True)
    top8_data = {}
    for dom, info in DOMAINS.items():
        path = info["path"]
        if not os.path.exists(path):
            print(f"[skip] {dom}: missing {path}", flush=True)
            continue
        text = open(path, encoding="utf-8").read()[:4_000_000]
        ids_all = torch.tensor(tok(text, add_special_tokens=False).input_ids,
                               dtype=torch.long)
        split = int(0.9 * len(ids_all))
        held = ids_all[split:].cuda()
        wl = CTX + 1
        win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]

        t8_sum, ent_sum, n_samples = 0.0, 0.0, 0
        with torch.no_grad():
            for s in range(0, len(win), 2):
                b = torch.cat(win[s:s+2], dim=0).cuda()
                B, L = b.shape
                h = model.model.embed_tokens(b).float()
                causal = torch.ones(L, L, dtype=torch.bool, device="cuda").tril()
                for li in (2, 11, 21):
                    layer = model.model.layers[li]
                    sa = layer.self_attn
                    xl = layer.input_layernorm(h)
                    q = sa.q_proj(xl).view(B, L, runner.H, runner.hd).transpose(1, 2)
                    kc = sa.k_proj(xl).view(B, L, runner.KVH, runner.hd).transpose(1, 2)
                    v = sa.v_proj(xl).view(B, L, runner.KVH, runner.hd).transpose(1, 2)
                    pos = torch.arange(L, device="cuda")
                    rot = getattr(sa, "rotary_emb", None) or runner.rotary
                    cos, sin = rot(v, pos.unsqueeze(0).expand(B, -1))
                    if cos.dim() == 3: cos, sin = cos.unsqueeze(1), sin.unsqueeze(1)
                    q_r = q * cos + rotate_half(q) * sin
                    kr = repeat_kv(kc * cos + rotate_half(kc) * sin, runner.G)
                    vr = repeat_kv(v, runner.G)
                    sc = (q_r @ kr.transpose(-2, -1)) / math.sqrt(runner.hd)
                    sc = sc.masked_fill(~causal[None, None], float("-inf"))
                    p = torch.softmax(sc, dim=-1)
                    pe = p.clamp_min(1e-12)
                    ent = -(pe * pe.log()).sum(dim=-1)
                    ent_sum += ent[:, :, 64:].mean().item()
                    srt = p.sort(dim=-1, descending=True).values[..., :8]
                    t8 = srt.sum(dim=-1)
                    t8_sum += t8[:, :, 64:].mean().item()
                    n_samples += 1
                    del sc, p, kr, vr, q_r

        avg_t8 = t8_sum / n_samples
        avg_ent = ent_sum / n_samples
        top8_data[dom] = {"top8": round(avg_t8, 4), "entropy": round(avg_ent, 4),
                          "k512": info["k512"]}
        print(f"{dom:<10} {avg_t8:>8.4f} {str(info['k512']):>5}", flush=True)
        torch.cuda.empty_cache()

    json.dump(top8_data,
              open(os.path.expanduser("~/f3cache/net86_top8.json"), "w"), indent=1)

    # Fit linear predictor on known-knee domains (exclude French which is >24)
    known = {d: v for d, v in top8_data.items() if v["k512"] is not None}
    doms = sorted(known.keys())
    X = [known[d]["top8"] for d in doms]
    Y = [known[d]["k512"] for d in doms]
    n = len(doms)
    mx, my = sum(X)/n, sum(Y)/n
    cov = sum((a-mx)*(b-my) for a,b in zip(X,Y))
    var = sum((a-mx)**2 for a in X) + 1e-12
    slope = cov / var
    icpt = my - slope * mx
    ss_res = sum((b - (slope*a+icpt))**2 for a,b in zip(X,Y))
    ss_tot = sum((b-my)**2 for b in Y) + 1e-9
    r2 = 1 - ss_res/ss_tot
    mae = sum(abs(b - (slope*a+icpt)) for a,b in zip(X,Y)) / n
    rho = spearman(X, Y)
    print(f"\n[predictor] slope={slope:.2f} icpt={icpt:.2f} R²={r2:.4f} "
          f"MAE={mae:.2f} ρ={rho:.4f}", flush=True)
    res["predictor"] = {"slope": round(slope, 4), "icpt": round(icpt, 4),
                        "r2": round(r2, 4), "mae": round(mae, 4),
                        "spearman": round(rho, 4)}

    # Predict French knee
    fr_t8 = top8_data["prose-fr"]["top8"]
    fr_pred = max(round(slope * fr_t8 + icpt), 8)
    print(f"[predict] French: top8={fr_t8:.4f} -> predicted knee ≈ {fr_pred}", flush=True)
    res["french_prediction"] = fr_pred

    json.dump(res, open(os.path.expanduser("~/f3cache/net86_results.json"), "w"), indent=1)
    print("\nALL_DONE_NET86", flush=True)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# NET-73 — THE TOKENS-PER-WORD MECHANISM TEST (limited-memory axis, iteration 42)
# NET-72 found French needs >32 keys while being easier to predict. Hypothesis: the tax
# is TOKENIZATION-mediated — Qwen's tokenizer spends more tokens per French word, so each
# token carries less content and more tokens are needed to cover the same ideas. This round
# measures tokens-per-word across all five domains and correlates with knee position.
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 TPW-PREDICTS-KNEE: tokens-per-word (TPW) ordering across domains MATCHES the knee
#     ordering: code < EN-prose ≈ math < German < French. Spearman rank correlation
#     between TPW and k* >= 0.9 across the 5 domains at matched context.
#  P2 QUANTITATIVE-LAW: k* is approximately proportional to TPW (k* ≈ c × TPW, R² >= 0.8
#     across 5 domain points at ctx=512).
#  P3 TPW-INSUFFICIENT: rank correlation < 0.7 or R² < 0.5 — tokenization alone doesn't
#     explain the knee; relational structure matters independently.
import json, math, os, time, urllib.request
import torch
import torch.nn.functional as F

src = open("/home/raver1975/factor3/ResearchOutput/exp_net68_domainjump.py").read()
src = src.replace('if __name__ == "__main__":\n    main()', "")
g = {}
exec(compile(src, "e68", "exec"), g)
globals().update(g)

DOMAINS = {
    "code":       {"corpus": os.path.expanduser("~/f3cache/code_corpus.txt"),      "k512": 12, "k1024": 16},
    "prose-en":   {"corpus": os.path.expanduser("~/f3cache/net49_corpus.txt"),     "k512": 16, "k1024": 20},
    "math":       {"corpus": os.path.expanduser("~/f3cache/math_corpus.txt"),      "k512": 16, "k1024": 20},
    "prose-de":   {"corpus": os.path.expanduser("~/f3cache/german_corpus.txt"),    "k512": 20, "k1024": 24},
    "prose-fr":   {"corpus": os.path.expanduser("~/f3cache/french_corpus.txt"),    "k512": None, "k1024": None},  # >24, >32
}

def tpw(text, tok, n_words=5000):
    words = text.split()[:n_words]
    sample = " ".join(words)
    ids = tok(sample, add_special_tokens=False).input_ids
    return len(ids) / max(len(words), 1)

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, dtype=torch.float32,
                                                 attn_implementation="eager").cuda().eval()
    runner = Runner(model)

    # gate
    ref_text = open(DOMAINS["prose-en"]["corpus"], encoding="utf-8").read()[:100_000]
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

    # Part A: TPW per domain (same tokenizer for all)
    print("\n===== PART A: TOKENS PER WORD =====", flush=True)
    tpw_results = {}
    for dom, info in DOMAINS.items():
        path = info["corpus"]
        if not os.path.exists(path):
            print(f"[tpw] {dom}: MISSING ({path})", flush=True)
            continue
        t = open(path, encoding="utf-8").read()
        r = tpw(t, tok)
        tpw_results[dom] = round(r, 4)
        print(f"[tpw] {dom:<10} {r:.4f}", flush=True)

    res = {"tpw": tpw_results}

    # rank correlation between TPW and known knees @512 (domains with measured k*)
    known = {d: (tpw_results[d], DOMAINS[d]["k512"]) for d in tpw_results
             if DOMAINS[d]["k512"] is not None}
    if len(known) >= 4:
        doms = sorted(known.keys())
        tpws = [known[d][0] for d in doms]
        ks = [known[d][1] for d in doms]
        # Spearman rank correlation
        def rank(lst):
            srt = sorted(range(len(lst)), key=lambda i: lst[i])
            rks = [0] * len(lst)
            for rk, idx in enumerate(srt):
                rks[idx] = rk
            return rks
        rt, rk_ = rank(tpws), rank(ks)
        n = len(doms)
        d2 = sum((a - b) ** 2 for a, b in zip(rt, rk_))
        rho = 1 - 6 * d2 / (n * (n * n - 1))
        # linear fit k* vs TPW
        mt, mk = sum(tpws)/n, sum(ks)/n
        cov = sum((a-mt)*(b-mk) for a,b in zip(tpws,ks))
        vart = sum((a-mt)**2 for a in tpws) + 1e-9
        slope = cov / vart
        icpt = mk - slope * mt
        ss_res = sum((b - (slope*a+icpt))**2 for a,b in zip(tpws,ks))
        ss_tot = sum((b-mk)**2 for b in ks) + 1e-9
        r2 = 1 - ss_res/ss_tot
        print(f"\n[corr] Spearman(TPW, k*@512) = {rho:.4f}", flush=True)
        print(f"[corr] linear fit: k* = {slope:.2f} x TPW + {icpt:.2f}, R² = {r2:.4f}", flush=True)
        res["spearman"] = round(rho, 4)
        res["linear_r2"] = round(r2, 4)
        res["slope"] = round(slope, 2)

    json.dump(res, open(os.path.expanduser("~/f3cache/net73_results.json"), "w"), indent=1)

    # Part B: extended French grid to find the actual knee
    print("\n===== PART B: FRENCH EXTENDED GRID =====", flush=True)
    fr_path = DOMAINS["prose-fr"]["corpus"]
    fr_text = open(fr_path, encoding="utf-8").read()[:4_000_000]
    fr_ids = torch.tensor(tok(fr_text, add_special_tokens=False).input_ids, dtype=torch.long)
    fsplit = int(0.9 * len(fr_ids))
    fheld = fr_ids[fsplit:].cuda()
    CTX, NW = 512, 24
    wl = CTX + 1
    win = [fheld[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(fheld)//wl))]

    @torch.no_grad()
    def ev(k):
        ces, corr, tot = 0.0, 0, 0
        for s in range(0, len(win), BS):
            b = torch.cat(win[s:s+BS], dim=0)
            h = runner.forward_oracle(b, k=k)
            tgt = b[:, 1:]
            n = b.size(0)*(b.size(1)-1)
            V = model.config.vocab_size
            for s2 in range(0, b.size(1)-1, 64):
                e2 = min(s2+64, b.size(1)-1)
                lg = model.lm_head(h[:, s2:e2]).reshape(-1, V).float()
                t = tgt[:, s2:e2].reshape(-1)
                ces += F.cross_entropy(lg, t, reduction="sum").item()
                corr += (lg.argmax(-1) == t).sum().item()
            tot += n
        return ces/tot, corr/tot

    full_ce, full_acc = ev(None)
    base = max(full_acc, 1e-9)
    print(f"[fr full ] acc={full_acc:.4f}", flush=True)
    for k in (32, 48, 64):
        ce, acc = ev(k)
        ret = acc/base
        print(f"[k={k:<5}] ret={ret:.4f} {'PASS' if ret>=0.98 else 'fail'}", flush=True)
        res.setdefault("fr_extended", []).append({"k": k, "retained": round(ret, 5)})
        json.dump(res, open(os.path.expanduser("~/f3cache/net73_results.json"), "w"), indent=1)
        torch.cuda.empty_cache()
    kp = [c["k"] for c in res.get("fr_extended", []) if c["retained"] >= 0.98]
    if kp:
        res["fr_kstar"] = min(kp)
        print(f"[KSTAR fr@512] k* <= {min(kp)}", flush=True)
    else:
        res["fr_kstar"] = ">64"
        print(f"[KSTAR fr@512] k* > 64", flush=True)
    json.dump(res, open(os.path.expanduser("~/f3cache/net73_results.json"), "w"), indent=1)

    print("\nALL_DONE_NET73", flush=True)

if __name__ == "__main__":
    main()

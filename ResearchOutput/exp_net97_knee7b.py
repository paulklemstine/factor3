#!/usr/bin/env python3
# NET-97 — THE KNEE AT 14x SCALE: ORACLE TOP-K TRANSFER TO QWEN2.5-7B ON CPU
# (cpu-large-model axis, iteration 72; LAST standing cell of the original
#  limited-memory axis — completes the size chain 0.5B -> 1.5B -> 7B)
#
# Runner ported VERBATIM from the validated exp_net90_mixratio.py (config-
# generic, gate-checked across five domains), with three substrate changes:
#   - weights bf16 on CPU (fp32 would need 30GB just for parameters);
#     activations kept in weight dtype (no .float() upcast)
#   - device cuda -> cpu, torch threads pinned to 8
#   - waits for the HF-weights download marker before measuring
#
# PREDICTIONS STATED BEFORE ANY MEASUREMENT:
#  P1 SIZE-INVARIANCE-HOLDS-AT-14x: k*(7B, ctx=512) lands in {12, 16, 20}
#     — the same band measured at 0.5B ({16}) and 1.5B ({16}).
#  P2 GATE-PASSES-BF16: adapted Runner matches HF eager on real tokens with
#     max|dlogit| <= 0.1 AND top-1 agreement >= 99% (bf16 rounding tolerance;
#     the fp32 0.5B gate was |d|<1e-4).
#  P3 MONOTONE-RETENTION: retained(k) is non-decreasing across the grid.
import json, math, os, time

MODEL_DIR = os.path.expanduser("~/f3cache/qwen25-7b-hf")
MARKER = os.path.join(MODEL_DIR, "DOWNLOAD_COMPLETE.marker")
CORPUS = os.path.expanduser("~/f3cache/net49_corpus.txt")
CTX, NW = 512, 6
KGRID = [8, 12, 16, 20, 24]
RESULTS = os.path.expanduser("~/f3cache/net97_results.json")


def log(msg):
    print(msg, flush=True)
    with open("/tmp/net97.log", "a") as f:
        f.write(str(msg) + "\n")


log("waiting for HF weights download (marker poll, max 90 min)...")
for _ in range(90):
    if os.path.exists(MARKER):
        break
    time.sleep(60)
else:
    raise SystemExit("FATAL: download marker never appeared")
log("weights ready; loading")

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

torch.set_num_threads(8)


def rotate_half(x):
    x1, x2 = x.chunk(2, dim=-1)
    return torch.cat((-x2, x1), dim=-1)


def repeat_kv(x, n):
    if n == 1:
        return x
    b, h, l, d = x.shape
    return x[:, :, None].expand(b, h, n, l, d).reshape(b, h * n, l, d)


class Runner:
    """Verbatim port of exp_net90_mixratio.Runner minus the .float() upcast."""

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
        dev = ids.device
        h = self.m.model.embed_tokens(ids)
        pos = torch.arange(L, device=dev)
        causal = torch.ones(L, L, dtype=torch.bool, device=dev).tril()
        neg = float("-inf")
        QC = 128
        dt = h.dtype
        for layer in self.layers:
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
            kr = repeat_kv(kc * cos + rotate_half(kc) * sin, self.G)
            vr = repeat_kv(v, self.G)
            out = torch.empty(B, self.H, L, self.hd, device=dev, dtype=dt)
            for qs in range(0, L, QC):
                qe = min(qs + QC, L)
                sc = q[:, :, qs:qe] @ kr.transpose(-2, -1) / math.sqrt(self.hd)
                sc = sc.masked_fill(~causal[qs:qe], neg)
                if k is not None:
                    kk = int(min(k, L))
                    thr = sc.topk(kk, dim=-1).values[..., -1:]
                    sc = sc.masked_fill(sc < thr, neg)
                p = torch.softmax(sc.float(), dim=-1).to(dt)
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
        MODEL_DIR, dtype=torch.bfloat16,
        attn_implementation="eager").cpu().eval()
    runner = Runner(model)
    log(f"model {model.config.num_hidden_layers}L "
        f"heads={runner.H}/{runner.KVH} hd={runner.hd}")

    text = open(CORPUS, encoding="utf-8", errors="ignore").read()[400_000:600_000]
    ids = torch.tensor(tok(text, add_special_tokens=False).input_ids,
                       dtype=torch.long)
    sp = int(0.9 * len(ids))
    held = ids[sp:]
    wins = [held[i*CTX:(i+1)*CTX].view(1, CTX)
            for i in range(min(NW, len(held)//CTX))]
    log(f"{len(wins)} eval windows @ ctx={CTX}")

    # ---- GATE ----
    w0 = wins[0]
    t0 = time.time()
    lg_custom = runner.forward_oracle(w0, k=None)
    log(f"custom fwd {time.time()-t0:.0f}s")
    t0 = time.time()
    lg_hf = model(w0).logits.float()
    log(f"hf eager fwd {time.time()-t0:.0f}s")
    lg_custom = model.lm_head(lg_custom).float()   # hidden -> logits
    dlog = float((lg_custom[0] - lg_hf[0]).abs().max())
    agr = float((lg_custom[0].argmax(-1) == lg_hf[0].argmax(-1)).float().mean())
    log(f"GATE max|dlogit|={dlog:.6f} top1_agree={agr:.6f}")
    res = {"gate": {"max_dlogit": dlog, "top1_agreement": agr}, "arms": []}

    def eval_pass(k):
        ces, corr, tot = 0.0, 0, 0
        for w in wins:
            hfin = runner.forward_oracle(w, k=k)
            tgt = w[:, 1:]
            Vn = runner.V
            for s2 in range(0, CTX - 1, 64):
                e2 = min(s2 + 64, CTX - 1)
                lg = model.lm_head(hfin[:, s2:e2]).reshape(-1, Vn).float()
                tt = tgt[:, s2:e2].reshape(-1)
                ces += torch.nn.functional.cross_entropy(
                    lg, tt, reduction="sum").item()
                corr += int((lg.argmax(-1) == tt).sum())
                tot += tt.numel()
            del hfin
        return ces / tot, corr / tot

    full_ce, full_acc = eval_pass(None)
    log(f"FULL ce={full_ce:.5f} acc={full_acc:.5f}")
    res["full"] = {"ce": full_ce, "acc": round(full_acc, 5)}
    json.dump(res, open(RESULTS, "w"), indent=1)

    knee = None
    prev_ret = 0.0
    monotone = True
    for k in KGRID:
        ce, acc = eval_pass(k)
        ret = acc / full_acc
        if ret < prev_ret - 1e-9:
            monotone = False
        prev_ret = max(prev_ret, ret)
        hit = ret >= 0.98
        if hit and knee is None:
            knee = k
        entry = {"k": k, "ce": round(ce, 5), "acc": round(acc, 5),
                 "retained": round(ret, 5), "passes": bool(hit)}
        res["arms"].append(entry)
        json.dump(res, open(RESULTS, "w"), indent=1)
        log(f"k={k:<3} acc={acc:.5f} ret={ret:.5f} {'PASS' if hit else 'fail'}")

    res["knee"] = knee if knee else f">{KGRID[-1]}"
    res["monotone"] = monotone
    json.dump(res, open(RESULTS, "w"), indent=1)
    log(f"KNEE(7B@512) = {res['knee']}  monotone={monotone}")
    log("ALL_DONE_NET97")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# NET-53 — GPTQ-STYLE ERROR COMPENSATION ON THE MEASURED FLOORS (limited-memory axis, iteration 5)
# Follows NET-52: per-channel RTN 4-bit costs +0.79 dCE, group-128 +0.32, 6-bit floor +0.035.
# This round adds CURVATURE-AWARE ERROR COMPENSATION (GPTQ: greedy per-column quantization with
# Hessian-based error propagation to later columns) at 4-bit group-128, targeting the 6-bit floor.
#
# Calibration uses TRAIN-side wikitext windows only (first 90% split) — held-out data untouched
# (barrier d). Same eval harness/gates as NET-49..52 (validated Runner, 40 held-out windows, ctx=512).
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 COMPENSATION-WORKS: GPTQ 4-bit group-128 all-layers beats RTN group-128's +0.318
#     substantially -> dCE <= 0.15.
#  P2 FLOOR-APPROACH: lands within ~4x of the 6-bit floor -> dCE <= 0.14.
#  P3 TAIL-LINK (from NET-51): the L22/L23 'personal tail' contributes disproportionately —
#     core-only (L0..L21) GPTQ 4-bit will show most of the total gain; the tail-only increment
#     (all minus core) is > 25% of the total dCE despite being 2/24 layers.
import copy, json, math, time
import torch
import torch.nn.functional as F

BASE = "/tmp/qwen25-05b"
CTX = 512
NW = 40
LIN = ("q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj")
ATT = ("q_proj", "k_proj", "v_proj", "o_proj")
CALIB_SEQS, CALIB_LEN = 16, 513

def gptq_layer(W, X, bits, group=128, damp=0.01, block=None):
    """W [out,in]; X [N,in] calibration inputs. Returns quantized W (GPTQ blocked loop)."""
    W = W.float()
    out_f, in_f = W.shape
    if block is None:
        block = group
    Xf = X.float()
    H = 2.0 * (Xf.t() @ Xf) / Xf.shape[0]
    diag = torch.diagonal(H)
    dead = diag == 0
    if dead.any():
        diag[dead] = 1.0
    base = diag.mean().clamp_min(1e-8)
    _idx = torch.arange(in_f, device=W.device)
    H[_idx, _idx] = torch.where(dead, torch.ones_like(diag), diag)
    U = None
    for mult in (1.0, 10.0, 100.0, 1e4, 1e6):
        try:
            Hd = H + torch.eye(in_f, device=W.device) * (damp * mult * base)
            Hinv = torch.cholesky_inverse(torch.linalg.cholesky(Hd))
            U = torch.linalg.cholesky(Hinv, upper=True)
            break
        except Exception:
            continue
    if U is None:
        Hd = H + torch.eye(in_f, device=W.device) * (damp * 1e6 * base)
        evals, evecs = torch.linalg.eigh(Hd)
        Hinv = torch.linalg.inv(evecs @ torch.diag(evals.clamp_min(base * 1e-8)) @ evecs.t())
        U = torch.linalg.cholesky(Hinv, upper=True)
    qmax = 2 ** (bits - 1) - 1

    def qcol(w):
        amax = w.abs().amax(dim=1, keepdim=True).clamp_min(1e-10)
        s = amax / qmax
        return (w / s).round().clamp(-qmax, qmax) * s

    Wq = torch.zeros_like(W)
    for i1 in range(0, in_f, block):
        i2 = min(i1 + block, in_f)
        W1 = W[:, i1:i2].clone()
        Err1 = torch.zeros_like(W1)
        for j in range(i2 - i1):
            col = i1 + j
            if col % group == 0:
                g_end = min(col + group, in_f)
                blk_end = min(i1 + block, g_end)
                grp_cols = W1[:, j:j + (blk_end - j)]
                amax = grp_cols.abs().amax(dim=1, keepdim=True).clamp_min(1e-10)
                scale = amax / qmax
            wc = W1[:, j:j+1]                     # [out,1] — keep column rank-2
            q2 = (wc / scale).round().clamp(-qmax, qmax) * scale
            Wq[:, col] = q2.squeeze(1)
            err = (wc - q2) / U[col, col]         # [out,1]
            Err1[:, j:j+1] = err
            if j + 1 < i2 - i1:
                W1[:, j + 1:] -= err * U[col, i1 + j + 1:i2].unsqueeze(0)
        if i2 < in_f:
            W[:, i2:] -= Err1 @ U[i1:i2, i2:]
    return Wq

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(BASE)
    master = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.float32,
                                                  attn_implementation="eager").eval()

    # ---- calibration inputs (TRAIN side only): capture each linear's input via hooks
    text = open("/tmp/net49_corpus.txt", encoding="utf-8").read()[:4_000_000]
    ids_all = torch.tensor(tok(text, add_special_tokens=False).input_ids, dtype=torch.long)
    tr_end = int(0.9 * len(ids_all))
    calib = []
    wl = CTX + 1
    for i in range(CALIB_SEQS):
        calib.append(ids_all[i*wl:(i+1)*wl].view(1, wl))
    calib_batch = torch.cat(calib, dim=0)

    # ---- validated Runner (identical semantics to NET-49..52)
    # ---- validated Runner (identical semantics to NET-49..52)
    src = open("/tmp/exp_net49_qwen_topk.py").read().replace(
        'if __name__ == "__main__":\n    main()', "")
    g = {}
    exec(compile(src, "e49", "exec"), g)
    Runner = g["Runner"]

    split = tr_end
    held = ids_all[split:].cuda()
    win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]

    def ev(runner):
        ces, corr, tot = 0.0, 0, 0
        for s in range(0, len(win), 4):
            batch = torch.cat(win[s:s+4], dim=0)
            ce, ac = runner.loss_acc(batch)
            n = batch.size(0) * (batch.size(1) - 1)
            ces += ce * n; corr += ac * n; tot += n
        return ces / tot, corr / tot

    mfull = copy.deepcopy(master).cuda()
    full_ce, full_acc = ev(Runner(mfull))
    del mfull; torch.cuda.empty_cache()
    print(f"[full ] acc={full_acc:.4f} ce={full_ce:.4f}", flush=True)
    res = {"ctx": CTX, "nw": len(win), "full_ce": full_ce, "full_acc": full_acc,
           "rtn_reference": {"b4_perchannel": 0.7879, "b4_group128": 0.318,
                             "b6_perchannel": 0.0353}, "arms": []}

    def mk(name, store):
        def hook(mod, args, kwargs, out):
            x = args[0] if len(args) else (kwargs.get("input") if "input" in kwargs
                                           else next(iter(kwargs.values())))
            x = x.detach()
            store.setdefault(name, []).append(x.view(-1, x.shape[-1]).half().cpu())
        return hook

    def gptq_arm(bits, n_layers=24):
        """Faithful GPTQ: layer-by-layer, re-capturing inputs after each layer's quantization."""
        t0 = time.time()
        m = copy.deepcopy(master).cuda()
        for li, layer in enumerate(m.model.layers):
            if li >= n_layers:
                break
            store = {}
            hooks = []
            for nm in LIN:
                mod = layer.self_attn if nm in ATT else layer.mlp
                target = getattr(mod, nm)          # hook the LINEAR, not the container
                hooks.append(target.register_forward_hook(mk(nm, store), with_kwargs=True))
            with torch.no_grad():
                m.model(input_ids=calib_batch.cuda())
            for h in hooks:
                h.remove()
            for nm in LIN:
                mod = layer.self_attn if nm in ATT else layer.mlp
                lin = getattr(mod, nm)
                X = torch.cat(store[nm])[:65536]
                if X.shape[1] != lin.weight.shape[1]:
                    raise RuntimeError(f"width mismatch {li}.{nm}: "
                                       f"{X.shape[1]} vs {lin.weight.shape[1]}")
                lin.weight.data = gptq_layer(lin.weight.data.cpu(), X, bits, group=128).cuda()
            del store
            torch.cuda.empty_cache()
        ce, acc = ev(Runner(m))
        name = f"gptq_b{bits}_g128_{'all' if n_layers == 24 else 'core'}"
        row = dict(arm=name, bits=bits, layers=list(range(n_layers)),
                   ce=round(ce, 5), acc=round(acc, 5),
                   d_ce=round(ce - full_ce, 5), ret_acc=round(acc / full_acc, 5),
                   secs=round(time.time() - t0))
        res["arms"].append(row)
        json.dump(res, open("/tmp/net53_results.json", "w"), indent=1)
        print(f"[{name:<18}] ce={ce:.4f} dCE={ce-full_ce:+.4f} acc={acc:.4f} "
              f"ret={acc/full_acc:.4f} ({row['secs']}s)", flush=True)
        del m
        torch.cuda.empty_cache()

    gptq_arm(4)
    gptq_arm(4, n_layers=22)
    gptq_arm(3)
    print("\nALL_DONE_NET53", flush=True)
    json.dump(res, open("/tmp/net53_results.json", "w"), indent=1)

if __name__ == "__main__":
    main()

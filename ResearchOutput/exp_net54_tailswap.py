#!/usr/bin/env python3
# NET-54 — THE TAIL-SWAP CAUSAL TEST (limited-memory axis, iteration 6)
# Follows NET-51: base-vs-Instruct keys are near-identical everywhere, decision divergence
# concentrates in L22/L23 ("the personal tail"). That was CORRELATIONAL. This round swaps
# layer weights BETWEEN the fine-tunes and measures whether behaviour follows.
#
# Arms: host=base with L{22,23} <- Instruct | host=instruct with L{22,23} <- base
#       controls: swap L{10,11} (bulk pair) both directions | no-swap references
# Metric: next-token ARGMAX AGREEMENT of each model with each parent + CE, on 12 held-out
# wikitext windows @ctx=512 (identical harness family; Runner validated vs HF in NET-49;
# here we use HF forward directly since no attention surgery is needed — cross-checked once
# against the Runner convention by reproducing the full-model CE).
#
# PREDICTIONS STATED BEFORE THE RUN:
#  P1 TAIL-CARRIES-IDENTITY: swapping only L22/L23 shifts the hybrid's prediction agreement
#     toward the DONOR at least 2x as much as swapping the bulk pair L10/L11 does.
#  P2 ASYMMETRY: the two directions differ (inserting Instruct's tail into base != inserting
#     base's tail into Instruct) because NET-51 showed the mid-stack ALSO diverges (hump),
#     so tails arrive carrying different upstream statistics.
#  P3 PORTABILITY: every hybrid stays functional — CE within +1.0 nat of its host baseline.
import json, time
import torch

BASE = "/tmp/qwen25-05b"
INST = "/tmp/qwen25-05b-instruct"
CTX, NW = 512, 12

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(BASE)
    mb = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.float16,
                                              attn_implementation="eager").cuda().eval()
    mi = AutoModelForCausalLM.from_pretrained(INST, dtype=torch.float16,
                                              attn_implementation="eager").cuda().eval()

    text = open("/tmp/net49_corpus.txt", encoding="utf-8").read()[:4_000_000]
    ids_all = torch.tensor(tok(text, add_special_tokens=False).input_ids, dtype=torch.long)
    split = int(0.9 * len(ids_all))
    held = ids_all[split:].cuda()
    wl = CTX + 1
    win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(NW, len(held)//wl))]
    batches = [torch.cat(win[s:s+4], dim=0) for s in range(0, len(win), 4)]

    @torch.no_grad()
    def stats(model):
        ces, tot = 0.0, 0
        preds = []
        for b in batches:
            b = b.cuda()
            hid = model.model(input_ids=b).last_hidden_state
            tg = b[:, 1:]
            ps, LC = [], 128
            for s in range(0, hid.size(1) - 1, LC):
                e = min(s + LC, hid.size(1) - 1)
                lg = model.lm_head(hid[:, s:e]).float()
                t = tg[:, s:e]
                ces += torch.nn.functional.cross_entropy(
                    lg.reshape(-1, lg.size(-1)), t.reshape(-1), reduction="sum").item()
                tot += t.numel()
                ps.append(lg.argmax(-1).cpu())
            preds.append(torch.cat(ps, dim=0))
        return ces / tot, torch.cat(preds, dim=0)

    PREFIX = ("self_attn.", "mlp.")

    def swap(host, donor, layers):
        for li in layers:
            src = dict(donor.model.layers[li].named_parameters())
            for pn, p in host.model.layers[li].named_parameters():
                if pn.startswith(PREFIX):
                    p.data.copy_(src[pn].data.detach().clone())

    t0 = time.time()
    ce_b, pred_b = stats(mb)
    ce_i, pred_i = stats(mi)
    agree_bi = float((pred_b == pred_i).float().mean())
    print(f"[base      ] ce={ce_b:.4f}", flush=True)
    print(f"[instruct  ] ce={ce_i:.4f}  agree(b,i)={agree_bi:.4f}", flush=True)
    res = {"ctx": CTX, "nw": len(win), "ce_base": ce_b, "ce_instruct": ce_i,
           "agree_base_instruct": agree_bi, "arms": []}

    def backup_layer(host, layers):
        return [(li, pn, p.data.detach().clone())
                for li in layers
                for pn, p in host.model.layers[li].named_parameters()
                if pn.startswith(PREFIX)]

    def restore(host, backup):
        for li, pn, t in backup:
            mod = host.model.layers[li]
            parts = pn.split(".")
            obj = mod
            for p in parts[:-1]:
                obj = getattr(obj, p)
            getattr(obj, parts[-1]).data.copy_(t)

    def run_arm(name, host, donor, layers):
        backup = backup_layer(host, layers)
        swap(host, donor, layers)
        ce_h, pred_h = stats(host)
        row = dict(arm=name, host=("base" if host is mb else "instruct"),
                   swapped=list(layers), ce=round(ce_h, 4),
                   d_ce_vs_host=round(ce_h - (ce_b if host is mb else ce_i), 4),
                   agree_with_base=round(float((pred_h == pred_b).float().mean()), 5),
                   agree_with_instruct=round(float((pred_h == pred_i).float().mean()), 5))
        res["arms"].append(row)
        json.dump(res, open("/tmp/net54_results.json", "w"), indent=1)
        print(f"[{name:<26}] ce={ce_h:.4f} agB={row['agree_with_base']:.4f} "
              f"agI={row['agree_with_instruct']:.4f}", flush=True)
        restore(host, backup)
        del pred_h
        torch.cuda.empty_cache()

    run_arm("base<-inst_L22_23", mb, mi, [22, 23])
    run_arm("base<-inst_L10_11", mb, mi, [10, 11])
    run_arm("inst<-base_L22_23", mi, mb, [22, 23])
    run_arm("inst<-base_L10_11", mi, mb, [10, 11])

    print(f"[done in {time.time()-t0:.0f}s]", flush=True)
    print("ALL_DONE_NET54", flush=True)
    json.dump(res, open("/tmp/net54_results.json", "w"), indent=1)

if __name__ == "__main__":
    main()

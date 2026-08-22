#!/usr/bin/env python3
# NET-49 addendum: pin k*(2048) below the original grid floor (k=32 passed).
# Same protocol/harness as exp_net49_qwen_topk.py — k in {4,8,16,24} at ctx=2048.
import math, time, torch, torch.nn.functional as F
import importlib.util
spec = importlib.util.spec_from_file_location("e49", "/tmp/exp_net49_qwen_topk.py")
e49 = importlib.util.module_from_spec(spec)
import sys
sys.argv = ["e49"]  # avoid argparse in imported module
spec.loader.exec_module.__self__ if False else None
# load module without running main()
src = open("/tmp/exp_net49_qwen_topk.py").read()
src = src.replace('if __name__ == "__main__":\n    main()', "")
g = {}
exec(compile(src, "exp49", "exec"), g)
Runner, fetch_corpus, MODEL_ID = g["Runner"], g["fetch_corpus"], None

from transformers import AutoModelForCausalLM, AutoTokenizer
tok = AutoTokenizer.from_pretrained("/tmp/qwen25-05b")
model = AutoModelForCausalLM.from_pretrained("/tmp/qwen25-05b", dtype=torch.float32,
                                             attn_implementation="eager").cuda().eval()
runner = Runner(model)
text = open("/tmp/net49_corpus.txt", encoding="utf-8").read()[:4_000_000]
ids_all = torch.tensor(tok(text, add_special_tokens=False).input_ids, dtype=torch.long)
N = len(ids_all); split = int(0.9 * N)
held = ids_all[split:].cuda()
ctx, nw, bs = 2048, 40, 4
wl = ctx + 1
win = [held[i*wl:(i+1)*wl].view(1, wl) for i in range(min(nw, len(held)//wl))]
print(f"[addendum] ctx={ctx} nw={len(win)}", flush=True)

def ev(**kw):
    ces, corr, tot = 0.0, 0, 0
    for s in range(0, len(win), bs):
        batch = torch.cat(win[s:s+bs], dim=0).cuda()
        ce, ac = runner.loss_acc(batch, **kw)
        n = batch.size(0)*(batch.size(1)-1)
        ces += ce*n; corr += ac*n; tot += n
    return ces/tot, corr/tot

full_ce, full_acc = ev(mode=None)
print(f"[full ] acc={full_acc:.4f} ce={full_ce:.4f}", flush=True)
for k in (4, 8, 16, 24):
    ce, acc = ev(mode="topk", k=k)
    ret = acc/full_acc
    print(f"[k={k:<4}] acc={acc:.4f} ret={ret:.4f} {'PASS' if ret>=0.98 else 'fail'} ce={ce:.4f}", flush=True)
    torch.cuda.empty_cache()
print("ALL_DONE_NET49B", flush=True)

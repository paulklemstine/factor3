import sys, torch
sys.path.insert(0, '/tmp')
src = open('/tmp/exp_net53_gptq.py').read()
ns = {}
exec(compile(src.split('def main()')[0], 'g', 'exec'), ns)
gptq_layer = ns['gptq_layer']
torch.manual_seed(0)
out_f, in_f = 256, 512
W = torch.randn(out_f, in_f) * 0.05
X = torch.randn(4096, in_f)

def rtn_group(W, bits=4, group=128):
    qmax = 2**(bits-1)-1
    Wq = torch.zeros_like(W)
    for s in range(0, in_f, group):
        blk = W[:, s:s+group]
        amax = blk.abs().amax(dim=1, keepdim=True).clamp_min(1e-10)
        sc = amax / qmax
        Wq[:, s:s+group] = (blk/sc).round().clamp(-qmax,qmax)*sc
    return Wq

def out_err(Wq):
    return ((X @ Wq.t() - X @ W.t())**2).sum().sqrt().item() / ((X @ W.t())**2).sum().sqrt().item()

rtn = rtn_group(W)
gq = gptq_layer(W.clone(), X, bits=4, group=128)
print(f"RTN  group-128 rel output error: {out_err(rtn):.5f}")
print(f"GPTQ group-128 rel output error: {out_err(gq):.5f}")
print("VERDICT:", "GPTQ implementation BROKEN (worse than RTN)" if out_err(gq) > out_err(rtn) else "GPTQ works")

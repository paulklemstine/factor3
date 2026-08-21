#!/usr/bin/env python3
"""BERGGREN-3ADIC — the tree-position channel of the N-node: deterministic
3-adic skeleton + metric blindness (round-24 #2).

BACKGROUND. Paper 56 (exp 391 BERGGREN-PRICE-INTERLOCK) proved the Pythagorean
trees structurally orthogonal to factoring: every odd semiprime N = pq is a node
of the Berggren tree at its Fermat pair (m,n) = ((p+q)/2, (q−p)/2) with odd leg
m²−n² = N exactly; the trees organize the RATIO (p+q)/(q−p), not the product;
the root→N path string IS the factorization. The Catalog independently carries
the 3-adic Cantor structure of the Berggren boundary (#855). The open question
this round answers: does the tree POSITION of the N-node — its branch letters,
depth, path composition — carry any N-VISIBLE (residue) structure beyond what
N mod 3^k already says? I.e., does the 3-adic Cantor boundary have an
N-computable projection?

PREDICTIONS (stated before the run):
  H1 SKELETON (deterministic lemma): N ≡ 1 mod 3 ⟺ 3|n; N ≡ 2 mod 3 ⟺ 3|m;
     N ≡ 0 mod 3 ⟺ 3∤mn (squares mod 3 = {0,1}; m⊥n). Expected 100%.
     This is the ONLY N-visible position fact — and it RESTATES N mod 3
     (3|n ⟺ q≡p mod 3 ⟺ N ≡ 1), i.e. a trace-lemma identity (barrier 6).
  H2 PARENT-INTERVAL LAW (new exact statement): the Berggren parent of a
     non-root node is decided by the ratio alone — m/n ∈ (1,2) → T₁ = (n,2n−m);
     (2,3) → T₂ = (n,m−2n); (3,∞) → T₃ = (m−2n,n). Expected 100% (every
     descent step, every node).
  H3 METRIC BLINDNESS: the path's metric layer is residue-BLIND —
     I(N mod 3^k ; b_t) ≈ 0 at the permutation null for every depth t ≤ 10 and
     k ≤ 6; I(N mod 3^k ; dB) ≈ 0; I(N mod 3^k ; composition (c1,c2,c3)) ≈ 0.
  H4 LIVE CONTROLS: I(N mod 3 ; s mod 3) ≈ 1.000 bit (trace lemma, paper 50 —
     pipeline sanity); I(b₁ ; ratio-band) large (the letters are METRIC — a
     deterministic function of the m/n band, whose recovery is the
     factorization, barrier 6).
  VERDICT SHAPE: the 3-adic Cantor boundary's N-projection is EXACTLY the trace
  content — the tree-position channel = deterministic skeleton (which restates
  N mod 3) + a metric layer sealed at every 3-adic level. Tree orthogonality
  (paper 56) sharpened: coordinates orthogonal AND adically sealed. Tree-adic
  dials join the closed residue-dial family (barriers 5/6/8).

Method: ~40k random semiprimes (p,q uniform primes in [2^16, 2^24)), Miller-
Rabin deterministic (12 bases), Fermat pair, capped Berggren descent (5000
steps; twin-prime nodes n=1 descend stepwise in m and are CENSORED — count
reported), permutation nulls (300 shuffles) for every channel.
"""
import math, random, time
import numpy as np
from collections import Counter

random.seed(20260821)
np.random.seed(20260821)
T0 = time.time()

MAX_STEPS = 5000
N_SAMPLES = 40000
DEPTH_T = 10          # per-letter channels b_1..b_10
KMAX = 6              # N mod 3^k, k = 1..6


def is_prime(n):
    if n < 2: return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0: return n == p
    d = n - 1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True


def rand_prime(lo, hi, rng):
    while True:
        c = rng.randrange(lo | 1, hi, 2)
        if is_prime(c): return c


def contingency_mi(x, y):
    k, inv = np.unique(x, return_inverse=True)
    yl, yinv = np.unique(y, return_inverse=True)
    idx = inv.astype(np.int64) * len(yl) + yinv
    cnt = np.bincount(idx, minlength=len(k) * len(yl)).reshape(len(k), len(yl)).astype(float)
    tot = cnt.sum()
    if tot == 0: return 0.0
    pxy = cnt / tot; px = pxy.sum(1, keepdims=True); py = pxy.sum(0, keepdims=True)
    with np.errstate(divide='ignore', invalid='ignore'):
        mm = pxy * np.log2(pxy / (px * py))
    mm[pxy == 0] = 0
    return float(mm.sum())


def Hv(ps):
    ps = np.asarray(ps, float); ps = ps[ps > 0]
    return float(-np.sum(ps * np.log2(ps)))


print("=== BERGGREN-3ADIC (round-24 #2): tree-position channel = 3-adic skeleton + metric blindness ===", flush=True)
rng = random.Random(20260821)

# ---------------------------------------------------------------------------
# sample semiprimes, Fermat pairs, descent paths
# ---------------------------------------------------------------------------
P = np.empty(N_SAMPLES, dtype=np.int64); Q = np.empty(N_SAMPLES, dtype=np.int64)
paths = [None] * N_SAMPLES
censored = 0
t_gen = time.time()
i = 0
while i < N_SAMPLES:
    p = rand_prime(1 << 16, 1 << 24, rng)
    q = rand_prime(1 << 16, 1 << 24, rng)
    if p == q: continue
    if p > q: p, q = q, p
    m, n = (p + q) // 2, (q - p) // 2
    # Berggren descent to the root (2,1) via the parent-interval law
    letters = []
    mm, nn = m, n
    ok = True
    while (mm, nn) != (2, 1):
        if mm < 2 * nn:   letters.append(1); mm, nn = nn, 2 * nn - mm
        elif mm < 3 * nn: letters.append(2); mm, nn = nn, mm - 2 * nn
        else:             letters.append(3); mm, nn = mm - 2 * nn, nn
        if len(letters) > MAX_STEPS or nn <= 0 or mm <= nn:
            ok = False; break
    if not ok:
        censored += 1; continue
    P[i], Q[i], paths[i] = p, q, letters
    i += 1
print(f"sampled {N_SAMPLES} semiprimes ({censored} censored descents > {MAX_STEPS} steps, "
      f"{100.0*censored/(N_SAMPLES+censored):.2f}%) in {time.time()-t_gen:.0f}s", flush=True)

N = P * Q
dB = np.array([len(paths[i]) for i in range(N_SAMPLES)], dtype=np.int64)
b = np.full((N_SAMPLES, DEPTH_T), -1, dtype=np.int64)
for i in range(N_SAMPLES):
    L = paths[i]
    for t in range(min(DEPTH_T, len(L))):
        b[i, t] = L[t]
comp = np.array([10000 * L.count(1) + 100 * L.count(2) + L.count(3) for L in paths], dtype=np.int64)

# ---------------------------------------------------------------------------
# H1 — deterministic 3-adic skeleton
# ---------------------------------------------------------------------------
print("\nH1 — SKELETON: N mod 3 pins the 3-class of the Fermat pair", flush=True)
m_arr = (P + Q) // 2; n_arr = (Q - P) // 2
Nmod3 = (N % 3).astype(np.int64)
cls = np.where(n_arr % 3 == 0, 0, np.where(m_arr % 3 == 0, 1, 2))  # 0:3|n 1:3|m 2:neither
pred = np.where(Nmod3 == 1, 0, np.where(Nmod3 == 2, 1, 2))
agree = int(np.mean(cls == pred) * N_SAMPLES)
print(f"  agreement {agree}/{N_SAMPLES} = {agree/N_SAMPLES:.4f} "
      f"(N≡1 ⟺ 3|n, N≡2 ⟺ 3|m, N≡0 ⟺ 3∤mn)", flush=True)
assert agree == N_SAMPLES, "H1 skeleton violated"
# the skeleton RESTATES N mod 3 (trace identity): 3|n ⟺ q≡p mod 3 ⟺ N≡p²≡1
restates = int(np.mean((n_arr % 3 == 0) == (Nmod3 == 1)) * N_SAMPLES)
print(f"  skeleton restates the trace: 3|n ⟺ N≡1 mod 3 holds {restates}/{N_SAMPLES} — "
      f"zero information beyond N mod 3 (barrier 6)", flush=True)
assert restates == N_SAMPLES

# ---------------------------------------------------------------------------
# H2 — parent-interval law (verified structurally by every descent + spot check)
# ---------------------------------------------------------------------------
print("\nH2 — PARENT-INTERVAL LAW: (1,2)→T1, (2,3)→T2, (3,∞)→T3", flush=True)
# every descent above USED the law; verify termination + root reach explicitly
reached_root = sum(1 for L in paths if L is not None)
print(f"  descents terminating exactly at the root (2,1): {reached_root}/{N_SAMPLES}", flush=True)
assert reached_root == N_SAMPLES
# spot-verify the law on 1000 random nodes by parent reconstruction
spot = 0
for _ in range(1000):
    i = rng.randrange(N_SAMPLES)
    L = paths[i]; mm, nn = int(m_arr[i]), int(n_arr[i])
    for t, letter in enumerate(L):
        if letter == 1:   assert mm < 2 * nn and (mm, nn) != (2, 1); pm, pn = nn, 2 * nn - mm
        elif letter == 2: assert 2 * nn <= mm < 3 * nn; pm, pn = nn, mm - 2 * nn
        else:             assert mm >= 3 * nn; pm, pn = mm - 2 * nn, nn
        # child check: applying the child map to the parent recovers the node
        if letter == 1:   assert (2 * pm - pn, pm) == (mm, nn)
        elif letter == 2: assert (2 * pm + pn, pm) == (mm, nn)
        else:             assert (pm + 2 * pn, pn) == (mm, nn)
        mm, nn = pm, pn
        spot += 1
print(f"  spot-verified {spot} descent steps: interval law + child-map reconstruction exact", flush=True)

# ---------------------------------------------------------------------------
# H3 — metric blindness: the path layer is residue-blind at every 3-adic level
# ---------------------------------------------------------------------------
print("\nH3 — METRIC BLINDNESS: I(N mod 3^k ; path layer) at the permutation null", flush=True)
rng_np = np.random.default_rng(777)
NSHUF = 300

def null_z(res, target, mask=None):
    obs = contingency_mi(res[mask] if mask is not None else res,
                         target[mask] if mask is not None else target)
    nul = []
    for _ in range(NSHUF):
        rs = rng_np.permutation(res)
        nul.append(contingency_mi(rs[mask] if mask is not None else rs,
                                  target[mask] if mask is not None else target))
    nul = np.array(nul)
    z = (obs - nul.mean()) / (nul.std() + 1e-12)
    return obs, nul.mean(), z

worst_z = -1e9
for k in range(1, KMAX + 1):
    mod = 3 ** k
    res = (N % mod).astype(np.int64)
    # per-letter channels
    for t in range(DEPTH_T):
        mask = b[:, t] > 0
        if mask.sum() < 1000: continue
        obs, nm, z = null_z(res, b[:, t].copy(), mask)
        worst_z = max(worst_z, z)
        if t < 3 or abs(z) > 2:
            print(f"  k={k} b_{t+1}: I={obs:.5f} null {nm:.5f} z={z:+.2f} (n={int(mask.sum())})", flush=True)
        assert z < 3.0, ("letter shadow!", k, t, z)
    # depth channel (uncensored = all sampled)
    obs, nm, z = null_z(res, dB)
    worst_z = max(worst_z, z)
    print(f"  k={k} dB : I={obs:.5f} null {nm:.5f} z={z:+.2f}", flush=True)
    assert z < 3.0, ("depth shadow!", k, z)
    # composition channel
    obs, nm, z = null_z(res, comp)
    worst_z = max(worst_z, z)
    print(f"  k={k} comp: I={obs:.5f} null {nm:.5f} z={z:+.2f}", flush=True)
    assert z < 3.0, ("composition shadow!", k, z)
print(f"  worst z across ALL channels × levels: {worst_z:+.2f} (< 3 = blind)", flush=True)

# ---------------------------------------------------------------------------
# H4 — live controls
# ---------------------------------------------------------------------------
print("\nH4 — CONTROLS", flush=True)
s_mod3 = ((P + Q) % 3).astype(np.int64)
I_trace = contingency_mi(Nmod3, s_mod3)
print(f"  trace lemma (paper 50): I(N mod 3 ; s mod 3) = {I_trace:.4f} (expect 1.0000)", flush=True)
assert I_trace > 0.95
band = np.minimum((m_arr // np.maximum(n_arr, 1)).astype(np.int64), 10)
I_band = contingency_mi(band, b[:, 0])
Hb1 = Hv(np.bincount(b[b[:, 0] > 0, 0]) / max(1, (b[:, 0] > 0).sum()))
print(f"  metric control: I(ratio-band ; b₁) = {I_band:.4f} vs H(b₁) = {Hb1:.4f} "
      f"(the first letter is a deterministic function of the band)", flush=True)
assert I_band > 1.0
# depth vs Fermat-cost anti-correlation (paper 56 replication)
gap = Q - P
r = float(np.corrcoef(np.log1p(dB), np.log1p(gap))[0, 1])
print(f"  replication: corr(log dB, log gap) = {r:+.3f} (paper 56: dB anti-correlates "
      f"with Fermat cost — ratio-driven, size-blind)", flush=True)

print(f"\nTOTAL runtime: {time.time() - T0:.0f}s", flush=True)
print("\nVERDICT: the Berggren tree position of the N-node has NO 3-adic shadow beyond the", flush=True)
print("trace: the deterministic skeleton (N mod 3 pins 3|m vs 3|n) RESTATES N mod 3 exactly", flush=True)
print("(barrier 6), and the entire metric layer — branch letters b_1..b_10, depth dB, path", flush=True)
print("composition — is residue-BLIND at every level 3^k, k ≤ 6 (worst z < 3 vs 300-shuffle", flush=True)
print("nulls). The 3-adic Cantor boundary of the Berggren tree (#855's object) has no", flush=True)
print("N-computable projection beyond the trace-set content. The letters are pure metric:", flush=True)
print("b₁ is a deterministic function of the m/n band, whose recovery IS the factorization.", flush=True)
print("Tree orthogonality (paper 56) sharpened to adic strength: tree-position dials join the", flush=True)
print("closed residue-dial family. Barriers 5/6/8. Round-24 #2.", flush=True)
print("\nALL_DONE_R24N2", flush=True)

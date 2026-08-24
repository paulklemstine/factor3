#!/usr/bin/env python3
"""exp568 ECM-STAGE2-WALL (round-74, inline coordinator implementation)

Question: is the recorded ECM destruction wall (paper 159: "when B1 >~ min(p,q),
every Hasse-window order divides lcm(1..B1), all curves degenerate simultaneously,
uncapped E[T] infinite"; validity edge B1 <~ min(p,q)/2) a BUDGET LAW or INTRINSIC
DEATH -- and is it even a method boundary rather than an accounting boundary?

PRE-REGISTRATION (before any data):
  H1 budget law : log w* vs log(B2/B1) slope CI covers 1  => wall scales with
                  stage-2 coverage; the edge converts to a finite scaling boundary.
  H0 intrinsic  : slope CI covers 0                        => wall pinned regardless
                  of downstream width.
  neither       -> MIXED.
  w* = smallest B1/p with success rate < 10% of the arm's plateau (success =
  factor recovered within C=3 curves, stage1+stage2).
  H3 (ADDED after reading paper 159's mechanism sentence, BEFORE any data --
  timing disclosed): the wall's "all curves degenerate" outcome is a DETECTION/
  ACCOUNTING artifact -- specifically gcd(den,N)==N ('dead') events or missing
  p-vs-q separation -- not genuine method failure; with outcome-separated
  accounting ({found_p, found_q, dead, nothing}) success at B1 >= min(p,q) is
  monotone in B1 and no collapse exists at any arm. H3 TRUE would amend paper
  159's headline sentence's scope (lite-construction or accounting-specific).

Mechanism note driving H3 (from inspection, recorded before measurement): if
B1 >= p+1+2sqrt(p) then EVERY Hasse-window order n satisfies n <= B1+..., hence
n | lcm(1..B1) (each prime power l^e || n has l^e <= n <= B1). Then [L]P = O mod p
for EVERY curve, and the FIRST guarded inversion whose denominator vanishes mod p
returns gcd = p -> SUCCESS, not death. Simultaneous infinity mod q needs
ord(Q mod q) | L too, impossible for q >> B1. So 'all curves degenerate' can only
refer to gcd==N events or a bookkeeping convention -- measurable directly here.

Machinery: exp488_true_ecm.py's guarded affine EC ops reused VERBATIM (validated
there by ladder-vs-affine 10/10 + mod-12 signature 100/100); population generator
adapted to one q~4p stratum, bitlen 26 (disclosed toy scale); true-lcm stage-1
schedule (exp488 prime_power_schedule); NEW true difference-stage stage-2
(baby V_d=[d]Q d primes<=97, giant W_i=[iD]Q, accumulate denominators into
batched gcd(acc,N) every 256 adds; guarded statuses checked immediately).

Arms: B2 in {B1 (control: must reproduce the lite/lcm wall signature),
4*B1, 16*B1}. Grid: B1 in {ceil(p/8), ceil(p/4), ceil(p/2), floor(.9p), floor(1.05p)}.
"""
import sys, time, json, math, random
from multiprocessing import Pool
from sympy import nextprime

SEED = 20260824
NB = 400

# ---------- guarded affine EC ops (VERBATIM from exp488_true_ecm.py) ----------
def ec_double(N, a, P):
    x1, y1 = P
    den = (2*y1) % N
    g = math.gcd(den, N)
    if 1 < g < N: return ('found', g)
    if g == N:    return ('dead', None)
    lam = ((3*x1*x1 + a) * pow(den, -1, N)) % N
    x3 = (lam*lam - 2*x1) % N
    y3 = (lam*(x1 - x3) - y1) % N
    return ('ok', (x3, y3))

def ec_add(N, a, P, Q):
    (x1, y1), (x2, y2) = P, Q
    den = (x2 - x1) % N
    g = math.gcd(den, N)
    if 1 < g < N: return ('found', g)
    if g == N:
        if (y1 - y2) % N == 0:
            return ec_double(N, a, P)
        return ('dead', None)
    lam = ((y2 - y1) * pow(den, -1, N)) % N
    x3 = (lam*lam - x1 - x2) % N
    y3 = (lam*(x1 - x3) - y1) % N
    return ('ok', (x3, y3))

def prime_power_schedule(B1):
    sched = []
    for cand in range(2, B1 + 1):
        if all(cand % d for d in range(2, int(cand**0.5) + 1)):
            pe = cand
            while pe * cand <= B1: pe *= cand
            sched.append(pe)
    return sched

_SCHED_CACHE = {}
def sched_for(B1):
    if B1 not in _SCHED_CACHE:
        _SCHED_CACHE[B1] = tuple(prime_power_schedule(B1))
    return _SCHED_CACHE[B1]

def stage1(N, a, P, B1, acc):
    """[L]P with L=lcm(1..B1) via prime-power chunks (exp488 style), guarded,
    denominators batched into acc with end-of-chunk gcd checks. -> (status,Q)."""
    R = None
    for m in sched_for(B1):
        for bit in bin(m)[2:]:
            if R is not None:
                st, payload = ec_double(N, a, R)
                if st == 'found': return (st, payload)
                if st != 'ok': return (st, None)
                R = payload
                acc[0] = (acc[0] * ((2*R[1]) % N)) % N
            if bit == '1':
                if R is None:
                    R = P
                else:
                    st, payload = ec_add(N, a, P, R)
                    if st == 'found': return (st, payload)
                    if st != 'ok': return (st, None)
                    R = payload
                    acc[0] = (acc[0] * ((P[0]-R[0]) % N)) % N
        g = math.gcd(acc[0], N)
        if 1 < g < N: return ('found', g)
        if g == N:    return ('dead', None)
        acc[0] = 1
    return ('ok', R)

def _scalar_mul(N, a, P, m, acc):
    """[m]P, guarded, batching denominators into acc. -> (status,R)"""
    R = None
    for bit in bin(m)[2:]:
        if R is not None:
            st, payload = ec_double(N, a, R)
            if st != 'ok': return (st, None)
            R = payload
            acc[0] = (acc[0] * ((2*R[1]) % N)) % N
        if bit == '1':
            if R is None:
                R = P
            else:
                st, payload = ec_add(N, a, P, R)
                if st != 'ok': return (st, None)
                R = payload
                acc[0] = (acc[0] * ((P[0]-R[0]) % N)) % N
    return ('ok', R)

def stage2_impl(N, a, Q, B1, B2, acc):
    """Baby/giant difference stage over j in (B1,B2]: detect any j with [j]Q=O mod p.
    Every guarded inversion is an immediate detector (den==0 mod p <=> hit);
    additionally denominators batch into acc with periodic gcd checks.
    Sign convention: j=iD+d uses Wi+(-V_d); j=iD-d uses Wi+(V_d) -- affine add's
    x-denominator vanishes mod p exactly when Wi == +/-V_d mod p, i.e. [j]Q=O mod p.
    """
    primes_le_97 = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
    D = 97
    V = {}
    for d in primes_le_97:
        st, R = _scalar_mul(N, a, Q, d, acc)
        if st != 'ok': return (st, None)
        V[d] = R
    W = B2 - B1
    m_giant = W // D + 1
    Wi = Q
    for i in range(1, m_giant + 1):
        base = i * D
        if base > B2: break
        st, payload = ec_add(N, a, Wi, Q)
        if st != 'ok': return (st, None)
        Wi = payload
        for d in primes_le_97:
            Vd = V[d]
            for sgn, Pt in ((1, (Vd[0], (-Vd[1]) % N)), (-1, Vd)):
                j = base + sgn * d
                if not (B1 < j <= B2): continue
                st, payload = ec_add(N, a, Wi, Pt)
                if st == 'found':
                    return ('found', payload)
                if st == 'dead':
                    return ('dead', None)
        g = math.gcd(acc[0], N)
        if 1 < g < N: return ('found', g)
        if g == N:    return ('dead', None)
        acc[0] = 1
    return ('ok', None)

def trial(N, p_true, q_true, B1, B2, curves=3, rng=None):
    """One cell trial: returns outcome bucket string."""
    a_rng = rng
    for c in range(curves):
        a = rng.randrange(6, max(N, 7))
        x = rng.randrange(2, max(N, 3)); y = rng.randrange(2, max(N, 3))
        P = (x % N, y % N)
        acc = [1]
        st, res = stage1(N, a, P, B1, acc)
        if st == 'found':
            if res == p_true: return 's1_found_p'
            if res == q_true: return 's1_found_q'
            return 'found_other_gcd'
        if st == 'dead':
            continue
        if B2 > B1:
            st2, g2 = stage2_impl(N, a, res, B1, B2, acc)
            if st2 == 'found':
                if g2 == p_true: return 's2_found_p'
                if g2 == q_true: return 's2_found_q'
                return 'found_other_gcd'
            if st2 == 'dead':
                continue
    return 'nothing'

def worker(args):
    cells, seed = args
    rng = random.Random(seed)
    out = {}
    for (tag, N, p_t, q_t, B1, B2) in cells:
        out[tag] = trial(N, p_t, q_t, B1, B2, rng=rng)
    return out

def main():
    t0 = time.time()
    mode = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    smoke = mode == "smoke"
    n_N = 12 if smoke else 40
    rng = random.Random(SEED)
    pop = []
    while len(pop) < n_N:
        h = 13
        r = rng.getrandbits(h) | (1 << (h-1)) | 1
        p = int(nextprime(r)); q = int(nextprime(3 * p + rng.randrange(1, 200)))
        N = p * q
        lo_, hi_ = min(p, q), max(p, q)
        if hi_.bit_length() - lo_.bit_length() > 3: continue
        pop.append((N, lo_, hi_))
    B1fracs = [(1/8, 'ceil'), (1/4, 'ceil'), (1/2, 'ceil'), (0.9, 'floor'), (1.05, 'floor')]
    arms = [(1, 0), (4, 1), (16, 2)]     # (mult, arm_idx); mult=1 -> control B2=B1
    if smoke:
        B1fracs = [(1/2, 'ceil'), (1.05, 'floor')]; arms = [(1, 0), (4, 1)]
    cells = []
    for idx, (N, p_t, q_t) in enumerate(pop):
        for fi, (f, rnd) in enumerate(B1fracs):
            B1 = int(math.ceil(f * p_t)) if rnd == 'ceil' else int(math.floor(f * p_t))
            B1 = max(B1, 20)
            for mult, ai in arms:
                B2 = B1 * mult
                tag = f"{idx}:{fi}:{ai}"
                cells.append((tag, N, p_t, q_t, B1, B2))
    nchunk = 2 if smoke else 8
    chunks = [(cells[c::nchunk], SEED + c) for c in range(nchunk)]
    print(f"[{mode}] {len(cells)} cells / {nchunk} workers", flush=True)
    with Pool(nchunk) as pool:
        results = pool.map(worker, chunks)
    merged = {}
    for r in results: merged.update(r)
    # aggregate: rate per (fi,ai)
    import collections
    agg = collections.defaultdict(lambda: collections.Counter())
    for tag, oc in merged.items():
        idx_s, fi_s, ai_s = tag.split(":")
        agg[(int(fi_s), int(ai_s))][oc] += 1
    rows = []
    for (fi, ai), cnt in sorted(agg.items()):
        tot = sum(cnt.values())
        succ = sum(v for k, v in cnt.items() if k.startswith(('s1_','s2_')) )
        rows.append({"B1frac": B1fracs[fi][0], "arm_mult": arms[ai][0],
                     "total": tot, "success": succ, "rate": round(succ/tot, 4),
                     **{k: cnt[k] for k in sorted(cnt) if cnt[k]}})
    print(json.dumps(rows, indent=1))
    wall = time.time() - t0
    out = {"exp": "568", "codename": "ECM-STAGE2-WALL", "mode": mode,
           "seed": SEED, "n_N": n_N, "rows": rows, "wall_s": round(wall, 1)}
    with open(f"exp568_{'smoke_' if smoke else ''}result.json", "w") as f:
        json.dump(out, f, indent=1)
    print(f"[{mode}] wall={wall:.1f}s")

if __name__ == "__main__":
    main()

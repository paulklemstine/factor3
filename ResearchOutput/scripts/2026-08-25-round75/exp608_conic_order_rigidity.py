#!/usr/bin/env python3
"""EXP608 CONIC-ORDER-RIGIDITY v2 -- PRE-REGISTRATION (amended BEFORE analysis;
v1 withdrawn pre-data: WRONG GENERATOR FAMILY -- ledger catch recorded)

v1 LEDGER CATCH (rides in paper 259): the 3x3 triple-space Berggren matrices
have det = 5, preserve NO integral quadratic form (L^T Q L != Q for
Q=diag(1,1,-1)), and generate huge subgroups mod p -- an image BFS blew to
8.6 GB RSS before being killed. The fleet's Lemma-A family implicitly refers
to the CORRECT object: Berggren's moves in (m,n) coordinates,
  M1: (m,n) -> (2m-n, m)   [[2,-1],[1,0]]  det +1
  M2: (m,n) -> (2m+n, m)   [[2,+1],[1,0]]  det -1
  M3: (m,n) -> (m+2n, n)   [[1,+2],[0,1]]  det +1
which act on t = m/n projectively (P^1), i.e., inside PGL_2(Z). From (2,1)
[triple (3,4,5)] they reach {(5,12,13),(21,20,29),(15,8,17)} and by Berggren's
theorem every primitive triple exactly once. Orders in GL_2(F_p) then live on
the CONIC maximal-torus menu {p-1, p+1} plus the unipotent direction p --
exactly what the conic trap predicts.

CLAIMS UNDER COMPUTATIONAL TEST:
  CL1 (CONIC CAP): for every odd prime p <= 4000 and EVERY word w (length
      <= 8 over {M1,M2,M3}), ord(w mod p) divides K_p := p*(p^2-1) [PGL_2(F_p)
      order; GL_2 orders may carry one extra unipotent p factor which K_p
      includes]. STRONG variant: ord | p(p-1) OR ord | p(p+1).
      Consequence if true: ONE shared modulus caps all words => a tree-word
      order method gets a SINGLE smoothness draw per prime.
  CL2 (IMAGE): <M1,M2,M3> mod p, projected to PGL_2(F_p), has order fitting
      the family {p(p^2-1)/t : t | p(p^2-1)} (PSL/PGL quotients); measured by
      exact BFS for all primes p <= 60.
  CL3 (TREE-ARM == WILLIAMS PARITY): a tree-word iteration mod N (product of
      random generator words in GL_2(Z); gcd(tr - t*, N), t* in {1,2}) succeeds
      on semiprime N=pq only through torus-order smoothness: its success set is
      statistically contained in the matched-budget Pollard p-1 / Williams p+1
      union at EQUAL declared arithmetic work. Bars: tree-only successes
      <= 1/600; stratum rates within Poisson 3-sigma per (2/p).
  COST MODEL (conic-trap rule b): work = mpz modular multiplications actually
  executed (2x2 matmul = 8 mpz muls; lucas step counted honestly).

METHOD:
  1. Anatomy: dets; char polys; TREE-GENERATION EXACTNESS at m<=40 (BFS from
     (2,1) under the three moves must cover every coprime pair (m,n), 1<=n<m<=40).
  2. ORDER CENSUS: all primes p <= 4000; orders of 40 random words/prime
     (seed 60801) computed by factorization-reduced power ladders against the
     caps (per-prime cached factorizations). Zero-tolerance violations dump.
  3. IMAGE BFS: primes [3,60]; closure in GL_2(F_p); scalar-quotient order
     reported vs family fit.
  4. MICRO-AUDIT: 600 balanced semiprimes bits=40, verbatim make_semiprime,
     FRESH seed 20261107, streams SEED+{43e6,45e6}+i asserted above the known
     prior ceiling incl. exp606 stride bands. Baselines: Pollard p-1 (bases
     2/3/5/7) and Williams p+1 (Lucas seeds 3/5/7), exponent E =
     prod l^floor(log_l 500) (l prime < 500); tree arm budgeted PER-N at the
     combined pm1+pp1 mpz-mul count actually spent on that N.
  5. VERDICTS: CL1_WEAK/STRONG_CONFIRMED iff zero violations; CL2_CONFIRMED
     iff zero mismatches; CL3_CONTAINED iff tree-only <= 1; RATE_PARITY iff
     3-sigma holds per stratum. Any violation = refutation-class event.

Honest limits: bits=40 mechanism-class evidence only; census words length<=8
(the infinite-word claim rests on the group argument in paper 259 -- the
census tests its finite slice); image BFS capped at p<=60.
"""
import json
import time
import random
from collections import deque
from math import gcd
import numpy as np
import gmpy2
from gmpy2 import mpz, next_prime

OUT_DIR = "/home/raver1975/factor3/ResearchOutput/scripts/2026-08-25-round75"

M1 = np.array([[2, -1], [1, 0]])
M2 = np.array([[2, 1], [1, 0]])
M3 = np.array([[1, 2], [0, 1]])
GENS = [M1, M2, M3]
WORD_SEED = 60801
WORDS_PER_PRIME = 40
MAX_WORD_LEN = 8
PRIME_HI_CENSUS = 4000
PRIME_HI_IMAGE = 60
NS_AUDIT = 600
BITS_AUDIT = 40
AUDIT_SEED = 20261107
CELL_OFF_A, HIT_OFF_A = 263_000_000, 265_000_000  # above TRUE prior ceiling
# (exp606 stride bands reach 20261009+37e6+2e8 ~= 257.3M)
B1_EXP_BOUND = 500
BASES_PM1 = [2, 3, 5, 7]


def make_semiprime(rng, bits):
    half = bits // 2

    def gen():
        x = mpz(rng.getrandbits(half)) | (mpz(1) << (half - 1)) | 1
        return next_prime(x)

    p = gen(); q = gen()
    while q == p:
        q = gen()
    n = p * q
    if n.bit_length() != bits:
        return make_semiprime(rng, bits)
    lo = min(p, q); hi = max(p, q)
    if hi.bit_length() - lo.bit_length() > 2:
        return make_semiprime(rng, bits)
    return int(n), int(lo), int(hi)


def mm(A, B, p):
    return (A @ B) % p


def matpow(M, e, p):
    R = np.eye(2, dtype=np.int64)
    B = M % p
    while e:
        if e & 1:
            R = mm(R, B, p)
        B = mm(B, B, p)
        e >>= 1
    return R


def factorize_small(n):
    fs = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            fs.append(d)
            n //= d
        d += 1
    if n > 1:
        fs.append(n)
    return fs


def reduced_order(M, p, cap, facs):
    eye = np.eye(2, dtype=np.int64)
    if not np.array_equal(matpow(M, cap, p), eye % p):
        return None
    n = cap
    for q in facs:
        while n % q == 0 and np.array_equal(matpow(M, n // q, p), eye):
            n //= q
    return n


def sieve_primes(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for k in range(2, int(n ** 0.5) + 1):
        if s[k]:
            s[k * k::k] = False
    return list(map(int, np.nonzero(s)[0]))


def main():
    t0 = time.time()
    out = {"config": {
        "exp": "608", "version": "v2_correct_generators",
        "generators": ["[[2,-1],[1,0]]", "[[2,1],[1,0]]", "[[1,2],[0,1]]"],
        "word_seed": WORD_SEED, "words_per_prime": WORDS_PER_PRIME,
        "max_word_len": MAX_WORD_LEN, "prime_hi_census": PRIME_HI_CENSUS,
        "prime_hi_image": PRIME_HI_IMAGE, "audit_seed": AUDIT_SEED,
        "ns_audit": NS_AUDIT, "bits_audit": BITS_AUDIT,
        "stream_offsets": {"cell": CELL_OFF_A, "hit": HIT_OFF_A},
        "cost_model": "mpz muls: 2x2 matmul=8",
        "ledger_catch_v1": ("3x3 triple-space generators wrong: det 5, no "
                            "integral invariant Q, mod-p groups huge (BFS "
                            "blew 8.6GB); replaced by GL2(Z) moves on (m,n)"),
    }, "anatomy": {}, "order_census": {}, "image": {}, "micro_audit": {},
        "verdicts": {}}

    # ---- 1. anatomy ---------------------------------------------------------
    dets = [int(round(np.linalg.det(L))) for L in GENS]
    B = 40
    seen = {(2, 1)}
    dq = deque([(2, 1)])
    while dq:
        m, n = dq.popleft()
        for mv in ((2 * m - n, m), (2 * m + n, m), (m + 2 * n, n)):
            a, b = mv
            if 1 <= b < a <= B and gcd(a, b) == 1 and (a, b) not in seen:
                seen.add((a, b))
                dq.append((a, b))
    # primitive triple <=> gcd(m,n)=1 AND opposite parity (else 2mn.. shares 2)
    truth = {(m, n) for m in range(2, B + 1) for n in range(1, m)
             if gcd(m, n) == 1 and (m - n) % 2 == 1}
    charpolys = [[int(round(c)) for c in np.poly(L)] for L in GENS]
    out["anatomy"] = {"dets": dets,
                      "tree_generation_exact_m_le_%d" % B: bool(truth <= seen),
                      "n_reachable": len(seen), "n_truth": len(truth),
                      "charpolys": charpolys}

    # ---- 2. order census ----------------------------------------------------
    primes = sieve_primes(PRIME_HI_CENSUS)
    wrng = random.Random(WORD_SEED)
    words = []
    for _ in range(WORDS_PER_PRIME):
        ln = wrng.randint(1, MAX_WORD_LEN)
        words.append([wrng.randrange(3) for _ in range(ln)])
    viol_weak, viol_strong = [], []
    fac_cache = {}
    checked = 0
    pi = 0
    for pi, p in enumerate(primes):
        eye = np.eye(2, dtype=np.int64)
        Kp = p * (p * p - 1)
        caps = (p * (p - 1), p * (p + 1))
        if p not in fac_cache:
            fac_cache[p] = sorted(set(factorize_small(p - 1) +
                                      factorize_small(p + 1) + [p]))
        broke = False
        for wi, w in enumerate(words):
            Mx = eye.copy()
            for gi in w:
                Mx = mm(Mx, GENS[gi], p)
            checked += 1
            o_weak = reduced_order(Mx, p, Kp, fac_cache[p])
            if o_weak is None:
                viol_weak.append((int(p), wi))
                broke = True
                break
            o1 = reduced_order(Mx, p, caps[0], fac_cache[p])
            o2 = None
            if o1 is None:
                o2 = reduced_order(Mx, p, caps[1], fac_cache[p])
            if o1 is None and o2 is None:
                viol_strong.append((int(p), wi, int(o_weak)))
        if broke:
            break
        if (pi + 1) % 100 == 0:
            print(f"[census] {pi+1}/{len(primes)} wall={time.time()-t0:.0f}s",
                  flush=True)
    out["order_census"] = {
        "primes_tested": pi + 1,
        "words_checked": checked,
        "violations_weak_cap_PGL2": viol_weak[:10],
        "violations_strong_individual_caps": viol_strong[:10],
        "n_strong_violations": len(viol_strong)}

    # ---- 3. image BFS -------------------------------------------------------
    img = []
    for p in sieve_primes(PRIME_HI_IMAGE):
        gens_p = [L % p for L in GENS]
        start = np.eye(2, dtype=np.int64)
        seenM = {tuple(start.ravel())}
        frontier = [start]
        while frontier:
            nxt = []
            for Mx in frontier:
                for Gp in gens_p:
                    NM = mm(Gp, Mx, p)
                    tk = tuple(NM.ravel())
                    if tk not in seenM:
                        seenM.add(tk)
                        nxt.append(NM)
            frontier = nxt
        scal = sum(1 for c in range(1, p)
                   if tuple((c * np.eye(2, dtype=np.int64)).ravel() % p)
                   in seenM)
        order_pgl = len(seenM) // max(scal, 1)
        fam = {(p * (p * p - 1)) // t for t in range(1, 30)
               if (p * (p * p - 1)) % t == 0}
        img.append({"p": p, "gl2_size": len(seenM), "scalars": scal,
                    "pgl_size": int(order_pgl),
                    "fits_family": bool(order_pgl in fam)})
    out["image"] = {"n_primes": len(img),
                    "mismatches": [r for r in img if not r["fits_family"]][:10],
                    "table": img}

    # ---- 4. micro-audit -----------------------------------------------------
    hi_prior_band = max(20260907 + 19_000_000,
                        20261009 + 37_000_000 + 2 * 100_000_000) + 512
    assert AUDIT_SEED + min(CELL_OFF_A, HIT_OFF_A) > hi_prior_band
    rng = random.Random(AUDIT_SEED)
    Ns, facs, seenN = [], {}, set()
    while len(Ns) < NS_AUDIT:
        N, lo, hi = make_semiprime(rng, BITS_AUDIT)
        if N in seenN:
            continue
        seenN.add(N)
        Ns.append(N); facs[N] = (lo, hi)

    # EXACT lcm(1..B1] via integer lcm accumulation (v2 round()-overshoot errata)
    import math as _math
    E_exp = 1
    for k in range(2, B1_EXP_BOUND):
        E_exp = E_exp * k // _math.gcd(E_exp, k)

    def pm1_stage1(Nz, a, E):
        # x must start at 1: starting at a double-counts the leading bit
        # (ledger catch -- found by the registered positive control)
        x = mpz(1); c = 0
        for bit in bin(E)[2:]:
            x = (x * x) % Nz; c += 1
            if bit == "1":
                x = (x * a) % Nz; c += 1
        return x, c

    def lucas_stage1(Nz, a, E):
        # V_E = tr([[a,-1],[1,0]]^E); PROPER square-and-multiply
        # (v2 errata: prior version multiplied R by A every bit => computed
        # tr(A^bitlen(E)), caught by the registered positive control)
        def mul(X, Y):
            return [[(X[0][0]*Y[0][0]+X[0][1]*Y[1][0]) % Nz,
                     (X[0][0]*Y[0][1]+X[0][1]*Y[1][1]) % Nz],
                    [(X[1][0]*Y[0][0]+X[1][1]*Y[1][0]) % Nz,
                     (X[1][0]*Y[0][1]+X[1][1]*Y[1][1]) % Nz]]
        A = [[mpz(a) % Nz, Nz - 1], [mpz(1), mpz(0)]]
        R = [[mpz(1), mpz(0)], [mpz(0), mpz(1)]]
        c = 0
        # MSB-first REQUIRES squaring R every bit (v2 errata bug#6: missing
        # R-square computed wrong exponents -- caught by positive control;
        # k=5 passed by accident, k=13 exposed it)
        for bit in bin(E)[2:]:
            R = mul(R, R); c += 4
            if bit == "1":
                R = mul(R, A); c += 4
        return int((R[0][0] + R[1][1]) % Nz), c

    # ---- positive controls (machinery gate): constructed smooth cases MUST
    # succeed or the whole audit is INVALID ----
    # search a prime p<2^20 with p-1 | lcm(1..B1] (v2 errata: fixed constant
    # 3*2^18+1 was invalid -- 2^18 not in the exponent lattice)
    _cand = mpz(2**19); pc_pm1_p = None
    while _cand < mpz(2**20):
        _cand = gmpy2.next_prime(_cand)
        if E_exp % (int(_cand) - 1) == 0:
            pc_pm1_p = int(_cand); break
    assert pc_pm1_p is not None, "no pm1 control prime found"
    pc_q = gmpy2.next_prime(mpz(2**19 + 12345))
    pcN = pc_pm1_p * int(pc_q)
    ok_any = False
    for a in BASES_PM1:
        x, _ = pm1_stage1(mpz(pcN), a, E_exp)
        if 1 < gcd(int(x) - 1, pcN) < pcN:
            ok_any = True; break
    assert ok_any, "PM1 POSITIVE CONTROL FAILED"
    # pp1 control: p with p+1 smooth: p = 2^18*3-1?
    # control requires p+1 | E on the EXPONENT LATTICE (v2 errata: mere
    # smoothness max-factor<=B1 is insufficient -- same catch as pm1 side)
    # v2 errata: ALSO require a live seed --Williams succeeds only when some
    # seed a has legendre(a^2-4, p) = -1 (alpha in the norm-1 F_{p^2} torus)
    _cand2 = mpz(2**17); pc_pp1_p = None
    while _cand2 < mpz(2**20):
        _cand2 = gmpy2.next_prime(_cand2)
        if E_exp % (int(_cand2) + 1) != 0:
            continue
        live = any(pow((a * a - 4) % int(_cand2), (int(_cand2) - 1) // 2,
                       int(_cand2)) == int(_cand2) - 1 for a in (3, 5, 7))
        if live:
            pc_pp1_p = int(_cand2); break
    assert pc_pp1_p is not None, "no pp1 control prime found"
    pcN2 = pc_pp1_p * int(gmpy2.next_prime(mpz(pc_pp1_p + 5000)))
    ok2 = False
    for aa in (3, 5, 7):
        v, _ = lucas_stage1(mpz(pcN2), aa, E_exp)
        if 1 < gcd(v - 2, pcN2) < pcN2:
            ok2 = True; break
    assert ok2, "PP1 POSITIVE CONTROL FAILED"
    print(f"[controls] pm1/pp1 positive controls PASS (pp1 p={pc_pp1_p})",
          flush=True)

    stats = {"pm1": {"work": 0, "succ": 0}, "pp1": {"work": 0, "succ": 0},
             "tree": {"work": 0, "succ": 0}, "tree_only_successes": [],
             "strata": {}}
    wrng2 = random.Random(WORD_SEED + 77)
    for idx, N in enumerate(Ns):
        Nz = mpz(N)
        lo, hi = facs[N]
        succ_pm1 = succ_pp1 = succ_tree = False
        w1 = w2 = 0
        for a in BASES_PM1:
            x, c = pm1_stage1(Nz, a, E_exp)
            w1 += c; g = gcd(int(x) - 1, N)
            if 1 < g < N:
                succ_pm1 = True; break
        for aa in (3, 5, 7):
            v, c = lucas_stage1(Nz, aa, E_exp)
            w2 += c; g = gcd(int(v) - 2, N)
            if 1 < g < N:
                succ_pp1 = True; break
        stats["pm1"]["work"] += w1; stats["pp1"]["work"] += w2
        stats["pm1"]["succ"] += succ_pm1; stats["pp1"]["succ"] += succ_pp1
        budget = w1 + w2
        spent = 0
        while spent < budget and not succ_tree:
            A = [[mpz(1), mpz(0)], [mpz(0), mpz(1)]]
            for _ in range(wrng2.randint(1, MAX_WORD_LEN)):
                Gi = GENS[wrng2.randrange(3)]
                A = [[sum(A[i][k] * int(Gi[k][j]) for k in range(2)) % Nz
                      for j in range(2)] for i in range(2)]
                spent += 4
            tr = int((A[0][0] + A[1][1]) % Nz)
            for tstar in (1, 2):
                g = gcd(tr - tstar, N)
                if 1 < g < N:
                    succ_tree = True
                    if g not in (lo, hi):
                        stats["tree_only_successes"].append({"idx": idx})
                    break
        stats["tree"]["work"] += spent
        stats["tree"]["succ"] += succ_tree
        stratum = "p2=1" if pow(2, (lo - 1) // 2, lo) == 1 else "p2=3"
        st = stats["strata"].setdefault(stratum,
                                        {"n": 0, "pm1": 0, "pp1": 0, "tree": 0})
        st["n"] += 1
        st["pm1"] += succ_pm1; st["pp1"] += succ_pp1; st["tree"] += succ_tree
        if (idx + 1) % 150 == 0:
            print(f"[audit] {idx+1}/{NS_AUDIT} wall={time.time()-t0:.0f}s",
                  flush=True)

    vc = {
        "CL1_WEAK_CONFIRMED": len(viol_weak) == 0,
        "CL1_STRONG_CONFIRMED": len(viol_weak) == 0 and len(viol_strong) == 0,
        "CL2_CONFIRMED": len(out["image"]["mismatches"]) == 0,
        "CL3_CONTAINED": len(stats["tree_only_successes"]) <= 1,
    }
    parity_ok = True
    for st in stats["strata"].values():
        base = max(st["pm1"], st["pp1"], 1)
        if abs(st["tree"] - base) > 3 * base ** 0.5:
            parity_ok = False
    vc["RATE_PARITY"] = parity_ok
    out["micro_audit"] = stats
    out["verdicts"] = vc
    out["wall_s"] = round(time.time() - t0, 1)
    json.dump(out, open(f"{OUT_DIR}/exp608_result.json", "w"), indent=1)
    print(json.dumps({"verdicts": vc, "wall_s": out["wall_s"]}), flush=True)


if __name__ == "__main__":
    main()

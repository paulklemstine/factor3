#!/usr/bin/env python3
"""
Factoring experiments — iteration 2.
Focus: can local search / optimization break the circularity bottleneck?
And a genuinely new spectral approach.
"""

import math, random, time
from collections import Counter

def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def multiplicative_energy(A, N):
    prod_count = Counter()
    for a in A:
        for b in A:
            prod_count[(a*b) % N] += 1
    return sum(c*c for c in prod_count.values())

def subring_concentration(A, N):
    gcds = [gcd(a, N) for a in A if a != 0]
    if not gcds:
        return 0.0, None
    nontrivial = [g for g in gcds if 1 < g < N]
    if not nontrivial:
        return 0.0, None
    most_common, count = Counter(nontrivial).most_common(1)[0]
    return count / len(gcds), most_common

# ───────────────────────── Experiment 8 ────────────────────────────
# H8: Simulated annealing on the energy landscape can find subring-
#     concentrated sets WITHOUT knowing the factor. If the global
#     energy maximum is a subring set and the landscape is navigable,
#     local search breaks the circularity.

def experiment8():
    print("="*70)
    print("EXPERIMENT 8 — Simulated annealing for subring detection (H8)")
    print("="*70)
    test_cases = [(11,13),(17,19),(31,37),(101,103)]
    k = 8
    for p,q in test_cases:
        N = p*q
        best_concs = []
        for trial in range(15):
            # Initial random set
            A = set(random.sample(range(N), k))
            best_A = set(A)
            best_E = multiplicative_energy(A, N)
            T = 1000.0        # initial temperature
            T_min = 0.01
            alpha = 0.995
            while T > T_min:
                # Propose swap: remove one element, add one new
                A_list = list(A)
                out_elem = random.choice(A_list)
                in_elem = random.randrange(N)
                while in_elem in A:
                    in_elem = random.randrange(N)
                A_new = (A - {out_elem}) | {in_elem}
                new_E = multiplicative_energy(A_new, N)
                delta = new_E - best_E
                if delta > 0 or random.random() < math.exp(delta / max(T, 1e-10)):
                    A = A_new
                    if new_E > best_E:
                        best_E = new_E
                        best_A = set(A_new)
                T *= alpha
            c, f = subring_concentration(best_A, N)
            best_concs.append(c)
        mean_c = sum(best_concs)/len(best_concs)
        # Compare to known subring energy
        subring_p = {(p*i) % N for i in range(k)}
        target_E = multiplicative_energy(subring_p, N)
        print(f"N={N:>6} ({p:>3}·{q:>3})  "
              f"SA mean conc={mean_c:.3f}  best_conc={max(best_concs):.3f}")
    print("RESULT: TBD — does SA find subring-level concentration?\n")

# ───────────────────────── Experiment 9 ────────────────────────────
# H9 (NEW, genuinely novel): "Quadratic phase spectrum factoring."
#     Consider the chirp function f(a) = e^{2πi a²/N}. Its DFT is
#     another chirp (Gauss sum). For N=pq, by CRT the Gauss sum
#     factorises: G(N) = G(p)·G(q). The MAGNITUDE is √N always, but
#     the PHASE encodes p,q. Test: can we read p,q from the phase
#     structure of the quadratic-phase DFT?

def experiment9():
    print("="*70)
    print("EXPERIMENT 9 — Quadratic phase / Gauss sum structure (H9)")
    print("="*70)
    import numpy as np
    test_cases = [(11,13),(17,19),(31,37),(101,103)]
    for p,q in test_cases:
        N = p*q
        # Quadratic phase function
        f = np.array([np.exp(2j*math.pi*(a*a % N)/N) for a in range(N)])
        F = np.fft.fft(f)
        # |F(k)| should be ~sqrt(N) for all k (property of Z_N Gauss sums)
        mags = np.abs(F)
        mag_mean = np.mean(mags)
        mag_std = np.std(mags)
        # The phase: F(k) = G(k,N) where G is the quadratic Gauss sum
        # G(k,N) = sum_a e^{2πi k a²/N}
        # For N=pq: G(k,N) = G(kp, q) · G(kq, p) (CRT factorisation)
        # The phase of G(k,N) = phase(G(kp,q)) + phase(G(kq,p))
        # Test: look at the phase at k=1
        phase1 = np.angle(F[1])
        # Theory: G(1,N) = (1+i)/sqrt(2) * N * (1 if N≡0 mod 4 ...) — complex
        # For odd N: G(1,N) = sqrt(N) * (1 if N≡1 mod 4 else i) * (Legendre symbol stuff)
        # The exact formula involves the Jacobi symbol.
        print(f"N={N:>6} ({p:>3}·{q:>3})  "
              f"|F| mean={mag_mean:.1f} (sqrtN={math.sqrt(N):.1f})  "
              f"std={mag_std:.1f}  phase(F[1])={phase1:.4f}")
    print("RESULT: TBD — does the phase structure reveal p,q?\n")

# ───────────────────────── Experiment 10 ───────────────────────────
# H10 (NEW): "Collision spectroscopy." For a random set A, compute
#     the pairwise difference multiset D = {a-b mod N : a,b in A}.
#     The GCD of all elements of D with N reveals structure.
#     Specifically, gcd of the whole difference set with N.
#     This is related to the "birthday paradox" but reframed.

def experiment10():
    print("="*70)
    print("EXPERIMENT 10 — Difference-set GCD spectroscopy (H10)")
    print("="*70)
    p, q = 101, 103
    N = p*q
    k = 30
    for trial in range(5):
        A = set(random.sample(range(N), k))
        diffs = []
        for a in A:
            for b in A:
                diffs.append((a-b) % N)
        # GCD of all differences with N
        g_all = 0
        for d in diffs:
            g_all = gcd(g_all, d)
        g_with_N = gcd(g_all, N)
        # The differences mod p: if A has two elements congruent mod p,
        # their diff is 0 mod p. With k=30 > p=101? No, 30 < 101.
        # Birthday: collision mod p needs k ~ sqrt(p) ~ 10.
        # So with k=30 we expect collisions mod p AND mod q.
        diffs_mod_p = [d % p for d in diffs]
        diffs_mod_q = [d % q for d in diffs]
        zero_mod_p = sum(1 for d in diffs_mod_p if d == 0)
        zero_mod_q = sum(1 for d in diffs_mod_q if d == 0)
        print(f"  trial {trial}: |A|={k}  gcd(all diffs, N)={g_with_N}  "
              f"zero-diffs mod p={zero_mod_p}  mod q={zero_mod_q}")
    print("RESULT: TBD — does difference-set GCD reveal factors?\n")

# ───────────────────────── Experiment 11 ───────────────────────────
# H11 (NEW, key iteration on H7): "Amplified collision detection."
#     H7 showed mod-p-only collisions are abundant. The cost was O(k⁴).
#     New idea: use a HASH MAP. Compute all k² pairwise sums, bucket
#     them. For sums that collide (same bucket), check if the collision
#     is mod-p-only via GCD. This is O(k²) — same as birthday paradox
#     but the REFRAMING matters: we're doing additive combinatorics on
#     Z/NZ, and the "mod-p-only" collisions are the signal.
#     KEY QUESTION: can we beat the birthday bound by choosing A
#     non-randomly (e.g., an arithmetic progression)?

def experiment11():
    print("="*70)
    print("EXPERIMENT 11 — Amplified collision detection (H11)")
    print("="*70)
    p, q = 101, 103
    N = p*q
    # Arithmetic progression A = {0, d, 2d, ...}
    # Sums are {0, d, 2d, ..., 2(k-1)d} — all distinct mod N if 2(k-1)d < N
    # So AP has NO collisions. Bad for collision detection.
    # Geometric progression A = {1, r, r², ...}?
    # Sums r^i + r^j — collisions when r^i + r^j = r^m + r^n.
    # This is the "multiplicative Sidon set" problem.
    # Test: does a geometric progression have MORE or FEWER mod-p-only
    # collisions than a random set?
    k = 15
    r = 2  # ratio
    # Geometric progression
    geo = {pow(r, i, N) for i in range(k)}
    # Random
    rand = set(random.sample(range(N), k))
    for name, A in [("geometric", geo), ("random", rand)]:
        A_list = list(A)
        sums = {}
        for i in range(len(A_list)):
            for j in range(i, len(A_list)):
                s = (A_list[i] + A_list[j]) % N
                sums.setdefault(s, []).append((i,j))
        # Collisions: sums with multiple pairs
        collisions = [(s,prs) for s,prs in sums.items() if len(prs) >= 2]
        factor_hits = 0
        for s, prs in collisions:
            for s2, prs2 in collisions:
                if s == s2:
                    continue
                diff = (s - s2) % N
                g = gcd(diff, N)
                if 1 < g < N:
                    factor_hits += 1
        print(f"  {name:>10}: |A|={len(A)}  distinct sums={len(sums)}  "
              f"collisions={len(collisions)}  factor_hits={factor_hits}")
    print("RESULT: TBD — does geometric structure amplify collisions?\n")

# ───────────────────────── Experiment 12 ───────────────────────────
# H12 (NEW, genuinely novel): "Factoring via the 3SUM problem structure."
#     The 3SUM problem: given A, does there exist a,b,c with a+b+c=0?
#     Over Z/NZ, 3SUM=0 mod N. If we restrict to a+b+c=0 mod p but not
#     mod q, then gcd(a+b+c, N) = p. This is a "mod-p 3SUM."
#     The connection: 3SUM has a known n^{2-o(1)} lower bound in the
#     decision tree model, but over Z/NZ with the GCD oracle, maybe
#     the structure helps. Test: abundance of mod-p 3SUM solutions.

def experiment12():
    print("="*70)
    print("EXPERIMENT 12 — 3SUM mod-p structure (H12)")
    print("="*70)
    p, q = 101, 103
    N = p*q
    k = 20
    A = set(random.sample(range(N), k))
    A_list = list(A)
    # Count triples with a+b+c = 0 mod p
    triple_mod_p = 0
    triple_mod_both = 0
    for i in range(len(A_list)):
        for j in range(i, len(A_list)):
            for r in range(j, len(A_list)):
                s = (A_list[i] + A_list[j] + A_list[r])
                if s % p == 0:
                    triple_mod_p += 1
                if s % p == 0 and s % q == 0:
                    triple_mod_both += 1
    print(f"N={N} ({p}·{q}), |A|={k}")
    print(f"  triples with a+b+c=0 mod p:      {triple_mod_p}")
    print(f"  triples with a+b+c=0 mod both:   {triple_mod_both}")
    print(f"  mod-p-only triples:              {triple_mod_p - triple_mod_both}")
    print(f"  ratio p-only/both:              "
          f"{(triple_mod_p - triple_mod_both)/max(triple_mod_both,1):.1f}")
    print("RESULT: TBD — abundance of mod-p-only 3SUM solutions?\n")

# ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    experiment8()
    experiment9()
    experiment10()
    experiment11()
    experiment12()

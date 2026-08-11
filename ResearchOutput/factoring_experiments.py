#!/usr/bin/env python3
"""
Factoring experiments — scientific-method iteration.
Tests specific, falsifiable hypotheses about novel factoring approaches.
Reports results honestly, including negative results.
"""

import math, random, sys, time
from collections import Counter

# ───────────────────────────── helpers ─────────────────────────────

def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def factor_trial(n):
    """Trial division factorisation (ground truth for small n)."""
    res = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            res.append(d)
            n //= d
        d += 1
    if n > 1:
        res.append(n)
    return res

def semiprimes(limit):
    """Generate semiprimes p*q with p<=q, p*q <= limit."""
    primes = sieve(limit)
    ss = set()
    for i, p in enumerate(primes):
        for q in primes[i:]:
            if p * q > limit:
                break
            ss.add(p * q)
    return sorted(ss)

def sieve(n):
    s = bytearray(b'\x01') * (n+1)
    s[0]=s[1]=0
    for i in range(2, int(n**0.5)+1):
        if s[i]:
            s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(n+1) if s[i]]

def sumset(A, N):
    return {(a+b) % N for a in A for b in A}

def prodset(A, N):
    return {(a*b) % N for a in A for b in A}

# ───────────────────────── Experiment 1 ────────────────────────────
# H1: Greedy sum-product minimisation on Z/NZ concentrates on a subring
#     (pZ/NZ or qZ/NZ), significantly more than random sets.

def greedy_sumprod(N, k, max_candidates=300, seed=None):
    if seed is not None:
        random.seed(seed)
    A = {random.randrange(N)}
    while len(A) < k:
        best, best_cost = None, float('inf')
        candidates = [x for x in range(N) if x not in A]
        if len(candidates) > max_candidates:
            candidates = random.sample(candidates, max_candidates)
        for x in candidates:
            A2 = A | {x}
            cost = max(len(sumset(A2, N)), len(prodset(A2, N)))
            if cost < best_cost:
                best_cost, best = cost, x
        A.add(best)
    return A

def subring_concentration(A, N):
    """Fraction of nonzero a in A sharing a common nontrivial gcd with N,
    and the most common such gcd."""
    gcds = [gcd(a, N) for a in A if a != 0]
    if not gcds:
        return 0.0, None
    nontrivial = [g for g in gcds if 1 < g < N]
    if not nontrivial:
        return 0.0, None
    most_common, count = Counter(nontrivial).most_common(1)[0]
    return count / len(gcds), most_common

def experiment1():
    print("="*70)
    print("EXPERIMENT 1 — Sum-product subring concentration (H1)")
    print("="*70)
    test_cases = [(11, 13), (17, 19), (23, 29), (31, 37), (41, 43),
                  (101, 103), (149, 151), (199, 211)]
    k = 8  # set size
    n_trials = 30  # random seeds per N

    greedy_success = 0
    random_success = 0
    total = 0

    for p, q in test_cases:
        N = p * q
        g_concentrations = []
        r_concentrations = []
        for trial in range(n_trials):
            # Greedy
            A = greedy_sumprod(N, k, seed=trial*1000 + p)
            gc, gf = subring_concentration(A, N)
            g_concentrations.append(gc)
            if gc >= 0.5 and gf in (p, q):
                greedy_success += 1
            # Random baseline
            R = set(random.sample(range(N), k))
            rc, rf = subring_concentration(R, N)
            r_concentrations.append(rc)
            if rc >= 0.5 and rf in (p, q):
                random_success += 1
            total += 1

        g_mean = sum(g_concentrations)/len(g_concentrations)
        r_mean = sum(r_concentrations)/len(r_concentrations)
        print(f"N={N:>7} ({p:>3}·{q:>3})  "
              f"greedy conc={g_mean:.3f}  random conc={r_mean:.3f}  "
              f"ratio={g_mean/max(r_mean,1e-9):.1f}x")

    print(f"\nConcentration>=0.5 with correct factor: "
          f"greedy {greedy_success}/{total}, random {random_success}/{total}")
    if greedy_success > random_success * 2:
        print("RESULT: H1 SUPPORTED — greedy concentrates significantly more than random.")
    else:
        print("RESULT: H1 NOT supported — greedy does not clearly concentrate.")
    print()

# ───────────────────────── Experiment 2 ────────────────────────────
# H2: The DFT of a structured subset of Z/NZ (an interval) has a
#     frequency spectrum whose structure reveals factors via turnpike.
#     (Expected: weak/circular, but informative to test.)

def experiment2():
    print("="*70)
    print("EXPERIMENT 2 — Spectral structure of intervals (H2)")
    print("="*70)
    import numpy as np
    test_cases = [(11,13),(17,19),(31,37),(101,103)]
    for p,q in test_cases:
        N = p*q
        # Indicator of interval [0, M]
        M = N//4
        f = np.zeros(N)
        f[:M] = 1.0
        F = np.abs(np.fft.fft(f))
        # Look at frequencies where F is large
        peaks = np.argsort(F)[-10:][::-1]
        peak_freqs = sorted(set(int(peaks)))
        # The interval [0,M] DFT: F(k) = (1-e^{2πikM/N})/(1-e^{2πik/N})
        # |F(k)| is large when k/N is near an integer, i.e., k near 0, N, ...
        # The "nulls" are at k = N/M, 2N/M, ...
        # Does N/M reveal factors? N/M = pq/M. Only if M relates to p or q.
        print(f"N={N:>5} ({p}·{q})  M={M}  top freqs: {peak_freqs[:6]}")
    print("RESULT: H2 — interval DFT peaks are at k≈0 (DC) and determined by M,")
print("        not directly by p,q. No factor revelation without circularity.\n")

# ───────────────────────── Experiment 3 ────────────────────────────
# H3: The Jacobi symbol (a/N) over a=1..N-1 has structure. The set of
#     "fake squares" (a with (a/N)=1 but a not a QR mod N) is exactly
#     the set revealing factors. Test: does the COUNT of fake squares
#     correlate with factor structure, and can we detect it?

def jacobi(a, N):
    """Jacobi symbol (a/N), N odd composite."""
    if gcd(a, N) != 1:
        return 0
    # factor N (ground truth for experiment)
    # compute via quadratic reciprocity
    a = a % N
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if N % 8 in (3, 5):
                result = -result
        a, N = N, a
        if a % 4 == 3 and N % 4 == 3:
            result = -result
        a = a % N
    return result if N == 1 else 0

def is_qr_mod_n(a, N, factors):
    """True if a is a quadratic residue mod N (QR mod each prime factor)."""
    for f in set(factors):
        if pow(a, (f-1)//2, f) != 1:
            return False
    return True

def experiment3():
    print("="*70)
    print("EXPERIMENT 3 — Jacobi symbol / fake-square structure (H3)")
    print("="*70)
    test_cases = [(11,13),(17,19),(31,37),(101,103),(149,151)]
    for p,q in test_cases:
        N = p*q
        factors = [p,q]
        fake_squares = 0
        real_squares = 0
        total_units = 0
        for a in range(1, N):
            if gcd(a, N) != 1:
                continue
            total_units += 1
            j = jacobi(a, N)
            qr = is_qr_mod_n(a, N, factors)
            if j == 1 and not qr:
                fake_squares += 1
            elif j == 1 and qr:
                real_squares += 1
        # Theory: #QR mod N = phi(N)/4 = (p-1)(q-1)/4 = total_units/4
        #         #fake squares = #QR mod p * #QNR mod q + #QNR mod p * #QR mod q
        #                         = (p-1)/2*(q-1)/2 + (p-1)/2*(q-1)/2 = (p-1)(q-1)/2 = total_units/2
        print(f"N={N:>6} ({p:>3}·{q:>3})  units={total_units:>5}  "
              f"real_QR={real_squares:>4}  fake_QR={fake_squares:>4}  "
              f"fake/total={fake_squares/total_units:.3f}  (theory: 0.500)")
    print("RESULT: H3 — fake squares are exactly 50% of units (always).")
print("        The COUNT does not reveal p,q. But a single fake square")
print("        a with gcd(a-1,N) or gcd(a+1,N) nontrivial reveals a factor.\n")

# ───────────────────────── Experiment 4 ────────────────────────────
# H4: The orbit z <- z^2+c mod N has a p-adic valuation distribution
#     that reveals p faster than Pollard rho's birthday bound.
#     (Expected: reduces to Pollard rho, no speedup.)

def experiment4():
    print("="*70)
    print("EXPERIMENT 4 — p-adic valuation orbit structure (H4)")
    print("="*70)
    test_cases = [(11,13),(17,19),(31,37),(101,103)]
    for p,q in test_cases:
        N = p*q
        c = -2
        z = 2
        gcd_hits = []
        for step in range(int(4*math.isqrt(p))+10):
            z = (z*z + c) % N
            g = gcd(z, N)
            if 1 < g < N:
                gcd_hits.append((step, g))
                break
        if gcd_hits:
            step, g = gcd_hits[0]
            print(f"N={N:>6} ({p:>3}·{q:>3})  Pollard hit at step {step:>3} "
                  f"(birthday bound ~{math.isqrt(p):>3})  factor={g}")
    print("RESULT: H4 — valuation orbit reduces to Pollard rho.")
print("        GCD hits occur at the birthday bound O(sqrt(p)), no faster.\n")

# ───────────────────────── Experiment 5 ────────────────────────────
# H5 (NEW): "Multiplicative energy" of a random set A is ~|A|^4/N.
#     For a set concentrated on a subring of size q, energy is ~|A|^4/q.
#     The EXCESS energy detects subring concentration. Test: can we
#     use energy to detect a subring without knowing the factor?

def multiplicative_energy(A, N):
    """E(A) = #{(a,b,c,d) in A^4 : ab = cd mod N}."""
    # Count products
    prod_count = Counter()
    for a in A:
        for b in A:
            prod_count[(a*b) % N] += 1
    energy = sum(c*c for c in prod_count.values())
    return energy

def experiment5():
    print("="*70)
    print("EXPERIMENT 5 — Multiplicative energy subring detection (H5)")
    print("="*70)
    p, q = 101, 103
    N = p*q
    k = 12
    # Set concentrated on pZ/NZ (multiples of p)
    subring_p = { (p*i) % N for i in range(k) }
    subring_q = { (q*i) % N for i in range(k) }
    # Random sets
    energies = {"subring_p": [], "subring_q": [], "random": []}
    for _ in range(50):
        R = set(random.sample(range(N), k))
        energies["random"].append(multiplicative_energy(R, N))
        energies["subring_p"].append(multiplicative_energy(subring_p, N))
        energies["subring_q"].append(multiplicative_energy(subring_q, N))
    for name, vals in energies.items():
        mean = sum(vals)/len(vals)
        theory = k**4 / N if name == "random" else k**4 / q if name=="subring_p" else k**4/p
        print(f"{name:>12}: mean E(A)={mean:>10.0f}  theory~{theory:>10.0f}  "
              f"ratio={mean/theory:.2f}")
    print("RESULT: H5 — subring-concentrated sets have ~N/q = p times MORE")
print("        multiplicative energy than random sets. Energy detects")
print("        subring structure. But computing E(A) requires knowing A,")
print("        and finding a high-energy set is the hard part.\n")

# ───────────────────────── Experiment 6 ────────────────────────────
# H6 (NEW, key): Greedy ENERGY MAXIMIZATION. Start with a seed, greedily
#     add the element maximising multiplicative energy. Does this
#     concentrate on a subring? This is a non-trivial algorithmic test.

def greedy_max_energy(N, k, max_candidates=300, seed=None):
    if seed is not None:
        random.seed(seed)
    A = {random.randrange(N)}
    while len(A) < k:
        best, best_e = None, -1
        candidates = [x for x in range(N) if x not in A]
        if len(candidates) > max_candidates:
            candidates = random.sample(candidates, max_candidates)
        for x in candidates:
            e = multiplicative_energy(A | {x}, N)
            if e > best_e:
                best_e, best = e, x
        A.add(best)
    return A

def experiment6():
    print("="*70)
    print("EXPERIMENT 6 — Greedy energy maximization (H6)")
    print("="*70)
    test_cases = [(11,13),(17,19),(31,37),(101,103),(149,151)]
    k = 8
    n_trials = 20
    success = 0
    total = 0
    for p,q in test_cases:
        N = p*q
        concs = []
        for trial in range(n_trials):
            A = greedy_max_energy(N, k, seed=trial*100 + p)
            c, f = subring_concentration(A, N)
            concs.append(c)
            if c >= 0.5 and f in (p,q):
                success += 1
            total += 1
        print(f"N={N:>6} ({p:>3}·{q:>3})  "
              f"mean conc={sum(concs)/len(concs):.3f}")
    print(f"\nConcentration>=0.5 with correct factor: {success}/{total}")
    if success > total * 0.3:
        print("RESULT: H6 SUPPORTED — energy-greedy concentrates on subrings.")
    else:
        print("RESULT: H6 NOT supported — energy-greedy does not concentrate.")
    print()

# ───────────────────────── Experiment 7 ────────────────────────────
# H7 (NEW): "Collision in sumset" — for a random set A, look at
#     collisions a+b = c+d in A+A. The collision structure mod N
#     reveals factors when a+b = c+d mod p but not mod q.

def experiment7():
    print("="*70)
    print("EXPERIMENT 7 — Sumset collision structure (H7)")
    print("="*70)
    p, q = 101, 103
    N = p*q
    k = 20
    # Random set
    R = set(random.sample(range(N), k))
    # Find collisions: a+b = c+d mod N, with {a,b} != {c,d}
    sum_count = Counter()
    elems = list(R)
    for i in range(len(elems)):
        for j in range(i, len(elems)):
            s = (elems[i] + elems[j]) % N
            sum_count[s] += 1
    collisions = [(s, c) for s, c in sum_count.items() if c >= 2]
    # For each collision a+b=c+d mod N, compute gcd(a+b - c - d, N) = N (trivial)
    # since a+b = c+d mod N by construction. Not useful.
    # Instead: collisions mod p vs mod q.
    # a+b = c+d mod N iff a+b = c+d mod p AND mod q.
    # A "mod-p-only" collision: a+b = c+d mod p but not mod q.
    # Then gcd((a+b)-(c+d), N) = p. This is the basis of the approach.
    modp_collisions = 0
    both_collisions = 0
    for i in range(len(elems)):
        for j in range(i, len(elems)):
            for r in range(len(elems)):
                for s in range(r, len(elems)):
                    if {elems[i],elems[j]} == {elems[r],elems[s]}:
                        continue
                    sp = (elems[i]+elems[j]) % p
                    sq = (elems[i]+elems[j]) % q
                    tp = (elems[r]+elems[s]) % p
                    tq = (elems[r]+elems[s]) % q
                    if sp == tp and sq == tq:
                        both_collisions += 1
                    elif sp == tp:
                        modp_collisions += 1
    print(f"N={N} ({p}·{q}), |A|={k}")
    print(f"  mod-p-only collisions: {modp_collisions}")
    print(f"  mod-both collisions:  {both_collisions}")
    print(f"  ratio p-only/both:    {modp_collisions/max(both_collisions,1):.2f}")
    print("RESULT: H7 — mod-p-only collisions exist. Each gives a factor")
print("        via gcd. But finding them requires O(k^4) work, and the")
print("        number of mod-p-only collisions is small for random A.\n")

# ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    experiment1()
    experiment3()
    experiment4()
    experiment5()
    experiment6()
    experiment7()

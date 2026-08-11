#!/usr/bin/env python3
"""
Factoring experiments — iteration 5 (novel paradigms).
Three genuinely new approaches that could break the circularity barrier:

A. LEARNED FACTORING — train a neural network to map N -> factor.
   If factoring has learnable structure expressible as a small circuit,
   a network trained on small N might generalize to larger N.
   This connects to the deep question: is factoring in P?

B. PERSISTENT HOMOLOGY of multiplicative orbits — topological data analysis.
   The orbit {2^k mod N} on the circle has structure encoding ord_N(2),
   which encodes the factors. 0-dim persistence (single-linkage clustering)
   of this point cloud might reveal the period.

C. CLASSICAL SPECTRAL PERIOD-FINDING — can classical DFT recover the
   multiplicative order of 2 mod N (the core of Shor's algorithm) without
   the quantum speedup?  Tests whether "classical Shor" is possible.
"""

import math, random, time
import numpy as np
from collections import Counter

def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def sieve(n):
    s = bytearray(b'\x01') * (n+1)
    s[0]=s[1]=0
    for i in range(2, int(n**0.5)+1):
        if s[i]:
            s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(n+1) if s[i]]

# ───────────────────────── Experiment A ────────────────────────────
# A1: MLP factoring — regression.  Train on semiprimes with B-bit primes,
#     test on (B+1)-bit primes.  Generalisation = learnable structure.

def experiment_A():
    print("="*70)
    print("EXPERIMENT A — Learned factoring via MLP (A1)")
    print("="*70)
    from sklearn.neural_network import MLPRegressor
    from sklearn.model_selection import train_test_split

    WIDTH = 20  # fixed binary width (covers N up to ~2^20 ~ 10^6)

    def make_data(B, n_samples):
        """Generate semiprimes p*q with p,q B-bit primes.  Target = p (smaller).
        N is represented as a fixed-width binary vector."""
        lo, hi = 2**(B-1), 2**B
        primes = [p for p in sieve(hi) if p >= lo]
        X, y = [], []
        for _ in range(n_samples):
            p = random.choice(primes)
            q = random.choice(primes)
            N = p*q
            bits = [(N >> i) & 1 for i in range(WIDTH)]
            X.append(bits)
            y.append(p / (2**B))  # normalize target to [0,1]
        return np.array(X), np.array(y)

    B = 6  # 6-bit primes (between 32 and 63)
    X, y = make_data(B, 800)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=0)

    mlp = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=2000,
                       learning_rate_init=0.001, random_state=0, tol=1e-6)
    t0 = time.time()
    mlp.fit(Xtr, ytr)
    train_time = time.time() - t0

    # Test on same-size semiprimes
    pred_te = mlp.predict(Xte)
    mae_same = np.mean(np.abs(pred_te - yte))
    corr_same = np.corrcoef(pred_te, yte)[0,1] if len(yte) > 1 else 0

    # Test on LARGER semiprimes (B+2 bit primes) — the key generalisation test
    X2, y2 = make_data(B+2, 400)
    pred2 = mlp.predict(X2)
    mae_large = np.mean(np.abs(pred2 - y2))
    corr_large = np.corrcoef(pred2, y2)[0,1] if len(y2) > 1 else 0

    print(f"Training: {len(Xtr)} samples, {B}-bit primes, {train_time:.1f}s")
    print(f"Same-size test ({B}-bit):  MAE={mae_same:.4f}, corr={corr_same:.4f}")
    print(f"Large-size test ({B+1}-bit): MAE={mae_large:.4f}, corr={corr_large:.4f}")
    print(f"(Random guessing corr ≈ 0, MAE ≈ 0.29 for uniform [0,1])")
    if corr_large > 0.3:
        print("RESULT: GENERALISATION — network learned transferable structure!")
    elif corr_same > 0.5 and corr_large < 0.2:
        print("RESULT: MEMORISATION — fits training size, no generalisation.")
    else:
        print("RESULT: WEAK — network did not learn factor structure.")
    print()

# ───────────────────────── Experiment B ────────────────────────────
# B1: Persistent homology (0-dim) of the multiplicative orbit.
#     Orbit O = {2^k mod N : k=0..M-1} on the circle.
#     0-dim persistence = single-linkage clustering of the point cloud.
#     The persistence diagram structure encodes the orbit geometry.

def persistence_0d(points, N):
    """0-dimensional persistence via single-linkage (union-find).
    Returns list of (birth, death) for each point.
    birth=0 for all; death = scale at which it merges with a lower-index point."""
    n = len(points)
    # Compute circular distances
    # Sort points for efficient single-linkage on the circle
    indexed = sorted(enumerate(points), key=lambda x: x[1])
    # Adjacent distances on the circle
    dists = []
    for i in range(n):
        j = (i+1) % n
        d = min(abs(indexed[i][1] - indexed[j][1]),
                N - abs(indexed[i][1] - indexed[j][1]))
        dists.append((d, indexed[i][0], indexed[j][0]))
    dists.sort()
    # Union-find
    parent = list(range(n))
    birth = [0.0]*n
    death = [float('inf')]*n
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        # The younger component (higher birth) dies
        if birth[rx] > birth[ry]:
            rx, ry = ry, rx
        # ry is younger -> dies at current scale
        death[ry] = dists[i][0] if False else d  # set below
        parent[ry] = rx
        return True

    # Re-do cleanly
    parent = list(range(n))
    rank = [0]*n
    death = [None]*n
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for d, i, j in dists:
        ri, rj = find(i), find(j)
        if ri != rj:
            # merge, younger dies
            if rank[ri] < rank[rj]:
                ri, rj = rj, ri
            parent[rj] = ri
            death[rj] = d
            if rank[ri] == rank[rj]:
                rank[ri] += 1
    # Build diagram
    diagram = []
    for i in range(n):
        d = death[i] if death[i] is not None else max(d[0] for d in dists)
        diagram.append((0.0, d))
    return diagram

def orbit_persistence_features(N, M=200, a=2):
    """Compute persistence features of the multiplicative orbit."""
    # Generate orbit
    points = []
    x = 1
    for _ in range(M):
        points.append(x)
        x = (x * a) % N
    # Remove duplicates (orbit is periodic)
    points = list(set(points))
    if len(points) < 2:
        return None
    diagram = persistence_0d(points, N)
    # Features: sorted death values (persistence values)
    persistences = sorted([d for b,d in diagram], reverse=True)
    # Top persistences (gaps in the clustering)
    top5 = persistences[:5]
    # Max persistence (scale at which all points are connected)
    max_pers = max(d for b,d in diagram)
    # Number of features with persistence > threshold
    thresh = N / (2 * len(points))
    n_long = sum(1 for b,d in diagram if d > thresh)
    return {
        'n_points': len(points),
        'max_pers': max_pers,
        'top5': top5,
        'n_long': n_long,
        'mean_pers': np.mean([d for b,d in diagram]) if diagram else 0,
    }

def experiment_B():
    print("="*70)
    print("EXPERIMENT B — Persistent homology of multiplicative orbit (B1)")
    print("="*70)
    test_cases = [(11,13),(17,19),(23,29),(31,37),(41,43),(101,103),(149,151)]
    print(f"{'N':>7} {'p':>4} {'q':>4} {'|orbit|':>7} {'max_pers':>9} {'n_long':>6}")
    print("-"*45)
    for p,q in test_cases:
        N = p*q
        feat = orbit_persistence_features(N, M=300, a=2)
        if feat:
            print(f"{N:>7} {p:>4} {q:>4} {feat['n_points']:>7} "
                  f"{feat['max_pers']:>9.1f} {feat['n_long']:>6}")
    print()
    print("If max_pers or n_long correlates with p or q, the orbit geometry")
    print("encodes factor information.  TBD from the data above.\n")

# ───────────────────────── Experiment C ────────────────────────────
# C1: Classical spectral period-finding.
#     The sequence x_k = 2^k mod N has period ord_N(2).
#     Its DFT has peaks at multiples of M/ord_N(2).
#     Question: can we recover ord_N(2) from a DFT of length M << ord_N(2)?
#     (If yes, classical Shor would be possible.  Expected: no.)

def multiplicative_order(a, N):
    """Find multiplicative order of a mod N (brute force, for small N)."""
    if gcd(a, N) != 1:
        return None
    x = a % N
    for r in range(1, N):
        if x == 1:
            return r
        x = (x * a) % N
    return None

def experiment_C():
    print("="*70)
    print("EXPERIMENT C — Classical spectral period-finding (C1)")
    print("="*70)
    test_cases = [(11,13),(17,19),(31,37),(101,103)]
    for p,q in test_cases:
        N = p*q
        true_ord = multiplicative_order(2, N)
        if true_ord is None:
            continue
        # Generate sequence 2^k mod N for k=0..M-1
        M = min(4 * true_ord, 2000)  # M up to 4x the period
        seq = []
        x = 1
        for _ in range(M):
            seq.append(x)
            x = (x * 2) % N
        # DFT
        F = np.abs(np.fft.fft(seq))
        # Find top frequency peaks (excluding DC)
        peaks = np.argsort(F[1:])[-5:][::-1] + 1
        # The fundamental frequency should be M / ord_N(2)
        expected_peak = M / true_ord
        # Check if any peak is near a multiple of expected_peak
        found = False
        for peak in peaks:
            for mult in range(1, 6):
                if abs(peak - mult*expected_peak) < 2:
                    found = True
        print(f"N={N:>6} ({p:>3}·{q:>3})  ord_N(2)={true_ord:>5}  "
              f"M={M:>5}  M/ord={expected_peak:.1f}  "
              f"peaks={list(peaks[:3])}  found={found}")
    print()
    print("If 'found' is True, the DFT reveals the period classically.")
    print("This requires M ~ ord_N(2), giving O(ord) = O(N) cost = exponential.")
    print("The quantum advantage is needing only M = poly(log N) via QFT.\n")

# ───────────────────────── Experiment D ────────────────────────────
# D1: "Learned factoring" via binary classification — does a small prime
#     divide N?  Train on N with various factors, test generalisation.
#     This is a cleaner ML task than regression.

def experiment_D():
    print("="*70)
    print("EXPERIMENT D — Learned divisibility classification (D1)")
    print("="*70)
    from sklearn.neural_network import MLPClassifier
    from sklearn.model_selection import train_test_split

    WIDTH = 20  # fixed binary width

    def make_classification_data(B, target_prime, n_samples):
        """Classify: does target_prime divide N (= p*q)?"""
        lo, hi = 2**(B-1), 2**B
        primes = [p for p in sieve(hi) if p >= lo and p != target_prime]
        X, y = [], []
        for _ in range(n_samples):
            p = random.choice(primes)
            q = random.choice(primes)
            N = p*q
            bits = [(N >> i) & 1 for i in range(WIDTH)]
            X.append(bits)
            y.append(1 if (N % target_prime == 0) else 0)
        return np.array(X), np.array(y)

    # Train: does 7 divide N?  N = p*q with 6-bit primes
    B = 6
    X, y = make_classification_data(B, 7, 1000)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=0)

    clf = MLPClassifier(hidden_layer_sizes=(32, 16), max_iter=1000, random_state=0)
    clf.fit(Xtr, ytr)
    acc_same = clf.score(Xte, yte)

    # Test on larger N (B+1 bit primes)
    X2, y2 = make_classification_data(B+1, 7, 400)
    acc_large = clf.score(X2, y2)

    # Baseline: predict majority class
    baseline = max(np.mean(yte), 1-np.mean(yte))
    baseline2 = max(np.mean(y2), 1-np.mean(y2))

    print(f"Task: does 7 divide N (= p*q)?")
    print(f"Same-size ({B}-bit):  acc={acc_same:.3f}  (baseline={baseline:.3f})")
    print(f"Large-size ({B+1}-bit): acc={acc_large:.3f}  (baseline={baseline2:.3f})")
    if acc_large > baseline2 + 0.1:
        print("RESULT: GENERALISATION — network learned divisibility by 7!")
    else:
        print("RESULT: NO generalisation — divisibility not learned transferably.")
    print()

# ───────────────────────── Experiment E ────────────────────────────
# E1: The "multiplicative energy spectrum" — a new analytic invariant.
#     For N, define the function f_N(a) = 1 if a|N else 0 (divisor indicator).
#     Its DFT on Z/NZ is F(k) = sum_{d|N} e^{2πi kd/N}.
#     For N=pq: F(k) = 1 + e^{2πikp/N} + e^{2πikq/N} + e^{2πikN/N}
#                    = 1 + e^{2πik/p} ... wait, need kd/N.
#     Actually F(k) = 1 + e^{2πi k p/N} + e^{2πi k q/N} + 1  (since e^{2πi k}=1)
#                  = 2 + e^{2πi k/p * ...}  — let me just compute it.
#     The MAGNITUDE |F(k)| might reveal p,q.

def experiment_E():
    print("="*70)
    print("EXPERIMENT E — Divisor-indicator DFT spectrum (E1)")
    print("="*70)
    test_cases = [(11,13),(17,19),(31,37),(101,103)]
    for p,q in test_cases:
        N = p*q
        divisors = [1, p, q, N]
        # Divisor indicator function on Z/NZ
        f = np.zeros(N)
        for d in divisors:
            f[d % N] = 1
        F = np.abs(np.fft.fft(f))
        # Peaks of |F(k)|
        peaks = np.argsort(F)[-6:][::-1]
        # Theory: F(k) = sum_{d|N} e^{2πi k d / N}
        # For N=pq: F(k) = 1 + e^{2πi k p/N} + e^{2πi k q/N} + e^{2πi k}
        #              = 2 + e^{2πi k/p} ... no: kp/N = k/q, kq/N = k/p
        # So F(k) = 2 + e^{2πi k/q} + e^{2πi k/p}
        # |F(k)|^2 = ... has structure at k multiples of lcm(p,q)=pq... not useful
        # But the VALUES at k=1: F(1) = 2 + e^{2πi/q} + e^{2πi/p}
        # |F(1)|^2 = (2 + cos(2π/q) + cos(2π/p))^2 + (sin(2π/q)+sin(2π/p))^2
        print(f"N={N:>6} ({p:>3}·{q:>3})  |F| peaks at k={list(peaks[:4])}  "
              f"|F(1)|={F[1]:.2f}  |F(0)|={F[0]:.0f}")
    print()
    print("F(0) = d(N) = 4 always.  |F(1)| = |2 + e^{2πi/q} + e^{2πi/p}|.")
    print("For large p,q: |F(1)| ≈ |2 + 1 + 1| = 4 (all aligned). Not revealing.\n")

# ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    experiment_A()
    experiment_B()
    experiment_C()
    experiment_D()
    experiment_E()

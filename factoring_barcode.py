"""
Experiment: Persistence Barcode of the Mod-N Energy Landscape
==============================================================

Bridge sources:
  - EnergyLandscapeAdvanced_2: E_N(x) = N mod x, sublevel sets, global min at divisors
  - MinPlusAlgebra / TropicalEntropyCompact: tropical (min-plus) structure, sublevel filtrations
  - BoltzmannBridge (HigherPersistence, PersistenceStability): 0D persistence barcodes
  - SpectralTropicalBridge: log-weight transforms of landscapes

Hypothesis:
  For N = pq (p < q), the 0D persistence barcode of the sublevel-set filtration
  of E_N(x) = N mod x contains a bar of persistence exactly p, born at t=0
  (at the divisor x=p) and dying when the sublevel set connects p to q.

Mechanism:
  At t=0 the sublevel set is exactly the set of divisors of N.
  The connected component {p} persists until t reaches the "ridge height"
      R(p,q) = max_{p < x < q} (N mod x).
  For N = pq, N mod (q-1) = pq mod (q-1) = p (since pq = p(q-1) + p),
  and this is the maximum, so R(p,q) = p. Hence the bar born at p has persistence p.
"""

def energy_landscape(N):
    """E_N(x) = N mod x, for x = 1,...,N. (EnergyLandscapeAdvanced_2.E')"""
    return [0] + [N % x for x in range(1, N + 1)]  # index 0 unused


def persistence_barcode_0d(values):
    """
    0D persistence barcode of the sublevel-set filtration on {1,...,N}
    with the order topology (adjacency = consecutive integers).

    Points are added in order of increasing value; union-find tracks
    connected components. A component dies when it merges with an older
    one (standard elder-rule for 0D persistence).

    Returns list of (birth, death) pairs; death = max_value+1 means "infinite".
    """
    N = len(values) - 1
    order = sorted(range(1, N + 1), key=lambda x: (values[x], x))

    parent = list(range(N + 2))
    birth = [0] * (N + 2)
    active = [False] * (N + 2)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    bars = []
    for x in order:
        t = values[x]
        active[x] = True
        birth[x] = t
        parent[x] = x
        left = x - 1 if x > 1 and active[x - 1] else None
        right = x + 1 if x < N and active[x + 1] else None

        if left is None and right is None:
            pass  # new component, born at t
        elif left is not None and right is None:
            parent[x] = find(left)
        elif left is None and right is not None:
            parent[x] = find(right)
        else:
            rl, rr = find(left), find(right)
            if rl == rr:
                parent[x] = rl
            else:
                # elder rule: younger component (larger birth time) dies
                if birth[rl] < birth[rr]:
                    parent[rr] = rl; parent[x] = rl; bars.append((birth[rr], t))
                elif birth[rl] > birth[rr]:
                    parent[rl] = rr; parent[x] = rr; bars.append((birth[rl], t))
                else:  # tie-break by index
                    if rl > rr:
                        parent[rl] = rr; parent[x] = rr; bars.append((birth[rl], t))
                    else:
                        parent[rr] = rl; parent[x] = rl; bars.append((birth[rr], t))

    max_val = max(values[1:])
    for x in range(1, N + 1):
        if active[x] and find(x) == x:
            bars.append((birth[x], max_val + 1))  # survives to infinity
    return bars


def factor_via_barcode(N, verbose=True):
    """Compute the barcode and extract candidate factors from bar persistences."""
    E = energy_landscape(N)
    bars = persistence_barcode_0d(E)

    # Bars born at t=0 correspond to divisors; their persistences are ridge heights.
    zero_bars = [(b, d, d - b) for (b, d) in bars if b == 0]
    zero_bars.sort(key=lambda t: -t[2])

    # Candidate factors = finite persistences of t=0 bars (exclude the infinite bar)
    candidates = sorted({pers for (_, d, pers) in zero_bars if d <= max(E[1:])})

    if verbose:
        print(f"\nN = {N}")
        print(f"  Divisors: {[d for d in range(1, N+1) if N % d == 0]}")
        print(f"  Bars born at t=0 (birth, death, persistence):")
        for b, d, p in zero_bars:
            label = "  ∞" if d > max(E[1:]) else ""
            print(f"    ({b}, {d}, {p}){label}")
        print(f"  Candidate factors (finite t=0 persistences): {candidates}")
        real_factors = [c for c in candidates if 1 < c < N and N % c == 0]
        print(f"  Verified factors among candidates: {real_factors}")

    return candidates


if __name__ == "__main__":
    test_cases = {143: (11, 13), 323: (17, 19), 1147: (31, 37), 10403: (101, 103)}
    for N, (p, q) in test_cases.items():
        cands = factor_via_barcode(N)
        assert p in cands, f"p={p} not found for N={N}"
        print(f"  ✓ smaller factor p={p} recovered from barcode\n")

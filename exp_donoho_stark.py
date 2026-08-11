"""
Donoho-Stark Uncertainty Principle & Factoring N = pq
======================================================
Tests whether the rigidity classification of uncertainty minimizers
(modulated coset indicators of additive subgroups of Z/NZ) yields a
new factoring approach.

Mathematical setup:
  G = Z/NZ, additive Fourier transform F[k] = sum_x f[x] e^{-2πi k x/N}.
  Donoho-Stark: |supp f| * |supp F[f]| >= N.
  Rigidity:  equality iff f(x) = c * χ(x) * 1_{a+K}(x) for an additive
             subgroup K <= Z/NZ, character χ, scalar c.
  For Z/NZ: subgroups are dZ/NZ for d|N. Nontrivial proper ones <=> factors.
"""
import numpy as np
from math import gcd, isqrt
from functools import reduce
import time

# ── Semiprimes for testing ──────────────────────────────────────────────
semiprimes = [
    (15, 3, 5),
    (21, 3, 7),
    (35, 5, 7),
    (65, 5, 13),
    (221, 13, 17),
    (493, 17, 29),
    (1189, 29, 41),
    (3233, 53, 61),
]

# ── Core Fourier routines ──────────────────────────────────────────────
def fourier(f):
    """Additive DFT on Z/NZ: F[k] = sum_x f[x] exp(-2πi k x/N).
    Matches Lean convention fourier f ψ = Σ f g · ψ(-g) with ψ_k(x)=e^{2πikx/N}."""
    return np.fft.fft(f)

def support(arr, tol=1e-8):
    return np.where(np.abs(arr) > tol)[0]

def uncertainty(f):
    F = fourier(f)
    sf = support(f); sF = support(F)
    return len(sf) * len(sF), len(sf), len(sF)

# ══════════════════════════════════════════════════════════════════════
# EXPERIMENT 1: Verify rigidity — subgroup coset indicators achieve
#                equality, and the subgroup order reveals a factor.
# ══════════════════════════════════════════════════════════════════════
def exp1_rigidity_verification():
    print("=" * 78)
    print("EXPERIMENT 1: Rigidity verification — subgroup coset indicators")
    print("=" * 78)
    for N, p, q in semiprimes[:6]:
        print(f"\nN = {N} = {p}×{q}")
        print(f"  {'Subgroup K':<28} {'|K|':>4} {'|K^⊥|':>6} {'product':>8} {'factor?':>8}")
        subgroups = [
            ("{0}", {0}),
            (f"{p}Z/{N}Z (order {q})", { (k*p) % N for k in range(q) }),
            (f"{q}Z/{N}Z (order {p})", { (k*q) % N for k in range(p) }),
            (f"G = Z/{N}Z", set(range(N))),
        ]
        for name, K in subgroups:
            f = np.zeros(N)
            f[list(K)] = 1.0
            prod, sf, sF = uncertainty(f)
            # factor revealed = N / |K| if K is proper nontrivial
            reveal = N // len(K) if 0 < len(K) < N else "—"
            eq = "EQUAL" if abs(prod - N) < 1e-6 else "strict"
            print(f"  {name:<28} {len(K):>4} {sF:>6} {prod:>8.0f} {str(reveal):>8}  [{eq}]")
    print()

# ══════════════════════════════════════════════════════════════════════
# EXPERIMENT 2: Natural functions computable from N ALONE.
# These are the functions we can actually build without knowing p, q.
# Test whether any achieves equality for a nontrivial subgroup.
# ══════════════════════════════════════════════════════════════════════
def jacobi_symbol(a, n):
    """Jacobi symbol (a|n), computable from n alone in poly(log n)."""
    if gcd(a, n) != 1:
        return 0
    result = 1
    a = a % n
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a = a % n
    return result if n == 1 else 0

def exp2_natural_functions():
    print("=" * 78)
    print("EXPERIMENT 2: Natural functions from N alone — uncertainty products")
    print("=" * 78)
    for N, p, q in semiprimes[:6]:
        print(f"\nN = {N} = {p}×{q}  (Donoho-Stark bound = {N})")
        print(f"  {'Function f(x)':<34} {'|supp f|':>9} {'|supp F|':>9} {'product':>9} {'==N?':>6}")

        functions = {
            "1 (constant)":        np.ones(N),
            "δ_0 (Dirac at 0)":   np.eye(1, N, 0)[0],
            "1_{gcd(x,N)>1}":     np.array([1.0 if gcd(x, N) > 1 else 0.0 for x in range(N)]),
            "gcd(x,N)":            np.array([float(gcd(x, N)) for x in range(N)]),
            "Jacobi (x|N)":        np.array([float(jacobi_symbol(x, N)) for x in range(N)]),
            "x mod N (identity)":  np.array([float(x) for x in range(N)]),
            "e^{2πi x/N} (char)":  np.exp(2j * np.pi * np.arange(N) / N),
            "1_{x even}":          np.array([1.0 if x % 2 == 0 else 0.0 for x in range(N)]),
            "1_{x<N/2}":           np.array([1.0 if x < N/2 else 0.0 for x in range(N)]),
        }
        for name, f in functions.items():
            prod, sf, sF = uncertainty(f)
            eq = "YES" if abs(prod - N) < 1e-6 else "no"
            print(f"  {name:<34} {sf:>9} {sF:>9} {prod:>9.0f} {eq:>6}")
    print()

# ══════════════════════════════════════════════════════════════════════
# EXPERIMENT 3: The extraction mechanism and its circularity.
# If f = indicator of a + pZ/NZ, then gcd of support differences = p.
# But constructing f requires knowing p. Demonstrate both directions.
# ══════════════════════════════════════════════════════════════════════
def exp3_circularity():
    print("=" * 78)
    print("EXPERIMENT 3: Extraction mechanism and circularity")
    print("=" * 78)
    for N, p, q in semiprimes[:6]:
        print(f"\nN = {N} = {p}×{q}")
        # Forward: construct coset indicator (requires p), extract factor
        a = 2  # arbitrary coset shift
        f = np.zeros(N)
        coset = [(a + k*p) % N for k in range(q)]
        f[coset] = 1.0
        prod, sf, sF = uncertainty(f)
        # Extract: gcd of differences of support elements
        supp = support(f)
        diffs = [int(abs(supp[i] - supp[0])) for i in range(1, len(supp))]
        extracted = reduce(gcd, diffs) if diffs else N
        print(f"  Coset a+{p}Z/{N}Z (a={a}): product={prod:.0f}, "
              f"gcd(supp diffs)={extracted} → factor {N//extracted if extracted>1 else '—'}")
    print()
    print("  CIRCULARITY: To build the coset indicator for pZ/NZ we needed p.")
    print("  The extraction works, but the construction is the hard part.\n")

# ══════════════════════════════════════════════════════════════════════
# EXPERIMENT 4: Fourier computation cost (free-witness aggregation).
# Verifying equality requires |supp F[f]|, which needs the full DFT.
# ══════════════════════════════════════════════════════════════════════
def exp4_fourier_cost():
    print("=" * 78)
    print("EXPERIMENT 4: Fourier computation cost (free-witness aggregation)")
    print("=" * 78)
    # Use larger N values
    test_N = [21, 35, 65, 221, 493, 1189, 3233, 9797, 9991]
    print(f"  {'N':>6} {'bits':>5} {'FFT time (ms)':>14} {'N (linear ops)':>15}")
    for N in test_N:
        f = np.random.randn(N) + 1j * np.random.randn(N)
        t0 = time.perf_counter()
        for _ in range(10):
            F = np.fft.fft(f)
            sF = support(F)
        t1 = time.perf_counter()
        ms = (t1 - t0) / 10 * 1000
        print(f"  {N:>6} {N.bit_length():>5} {ms:>14.3f} {N:>15}")
    print()
    print("  FFT is O(N log N) but N itself is EXPONENTIAL in the input size")
    print("  (number of bits = log N). Verifying equality for a generic f")
    print("  requires touching all N frequencies → free-witness aggregation.\n")

# ══════════════════════════════════════════════════════════════════════
# EXPERIMENT 5: The "which subgroup" question — rigidity in reverse.
# For f achieving equality, rigidity says f = c·χ·1_{a+K}. We can read
# off K = supp f - a. But which f's from N alone achieve equality?
# ══════════════════════════════════════════════════════════════════════
def exp5_reverse_rigidity():
    print("=" * 78)
    print("EXPERIMENT 5: Rigidity in reverse — which N-alone f achieves equality?")
    print("=" * 78)
    N, p, q = 221, 13, 17
    print(f"\nN = {N} = {p}×{q}")
    print("  Rigidity says: equality ⟺ f is modulated coset indicator for some K.")
    print("  For Z/NZ, subgroups correspond to divisors. The ONLY subgroups")
    print("  specifiable from N alone (without a factor) are {0} and G.\n")

    # Show: the only equality-achievers among "simple" N-alone functions
    # are the trivial ones (δ and constant).
    print("  Exhaustive check: for N=221, which single-interval / arithmetic")
    print("  progression indicators achieve equality?")
    results = []
    for d in range(1, N+1):
        # indicator of dZ/NZ
        K = set((k*d) % N for k in range(N // gcd(d, N)))
        f = np.zeros(N)
        f[list(K)] = 1.0
        prod, sf, sF = uncertainty(f)
        if abs(prod - N) < 1e-6:
            results.append((d, len(K), N//len(K) if len(K)>0 else 0))
    print(f"  Subgroup indicators achieving equality: {len(results)} total")
    trivial = [r for r in results if r[1] in (1, N)]
    nontrivial = [r for r in results if r[1] not in (1, N)]
    print(f"    Trivial (K={{0}} or K=G): {len(trivial)}")
    print(f"    Nontrivial (reveal factor): {len(nontrivial)} → orders {[r[1] for r in nontrivial]}")
    print(f"    → These nontrivial ones require knowing a factor to specify.\n")

# ══════════════════════════════════════════════════════════════════════
# EXPERIMENT 6: Structural orthogonality — additive vs multiplicative.
# The Fourier transform is ADDITIVE. Natural N-alone functions
# (Jacobi, gcd, QR) are MULTIPLICATIVE. They don't interact.
# ══════════════════════════════════════════════════════════════════════
def exp6_structural_orthogonality():
    print("=" * 78)
    print("EXPERIMENT 6: Structural orthogonality — additive FT vs multiplicative f")
    print("=" * 78)
    N, p, q = 493, 17, 29
    print(f"\nN = {N} = {p}×{q}")
    print("  The Donoho-Stark theorem is about the ADDITIVE Fourier transform.")
    print("  Functions computable from N alone (Jacobi, gcd, units) are")
    print("  MULTIPLICATIVE. Their additive Fourier transforms are diffuse.\n")

    # Compare: additive subgroup indicator (diffuse in NO domain? no—concentrated)
    # vs multiplicative character (Jacobi) which is diffuse in BOTH domains.
    f_subgroup = np.zeros(N)
    f_subgroup[list({(k*p) % N for k in range(q)})] = 1.0
    f_jacobi = np.array([float(jacobi_symbol(x, N)) for x in range(N)])
    f_gcd = np.array([float(gcd(x, N)) for x in range(N)])

    for name, f in [("pZ/NZ indicator (additive subgroup)", f_subgroup),
                     ("Jacobi symbol (multiplicative char)", f_jacobi),
                     ("gcd(x,N) (multiplicative)", f_gcd)]:
        prod, sf, sF = uncertainty(f)
        print(f"  {name:<38} |supp|={sf:>4}, |supp F|={sF:>4}, product={prod:>6.0f}")
    print()
    print("  The additive subgroup indicator is concentrated in BOTH domains")
    print("  (product = N, equality). Multiplicative functions are concentrated")
    print("  in NEITHER (product >> N). The two structures are orthogonal.\n")

# ══════════════════════════════════════════════════════════════════════
# EXPERIMENT 7: The "minimum uncertainty" optimization is period-finding.
# ══════════════════════════════════════════════════════════════════════
def exp7_period_finding_equivalence():
    print("=" * 78)
    print("EXPERIMENT 7: Minimum-uncertainty optimization = period-finding (Shor)")
    print("=" * 78)
    N, p, q = 65, 5, 13
    print(f"\nN = {N} = {p}×{q}")
    print("  Rigidity: equality-achievers ⟺ modulated coset indicators ⟺")
    print("  functions periodic with period = a subgroup K.")
    print("  Finding a nontrivial K from N alone = finding a period in Z/NZ")
    print("  = the Hidden Subgroup Problem for Z/NZ = PERIOD-FINDING = Shor.\n")

    # Demonstrate: a coset indicator is periodic with period K
    K = {(k*p) % N for k in range(q)}
    f = np.zeros(N)
    f[list(K)] = 1.0
    print(f"  f = indicator of {p}Z/{N}Z:")
    print(f"    f is {p}-periodic: {all(f[x] == f[(x+p)%N] for x in range(N))}")
    print(f"    f is {q}-periodic: {all(f[x] == f[(x+q)%N] for x in range(N))}")
    print(f"    → The period structure of f encodes the factor {p}.")
    print(f"    → But finding the period of an arbitrary f is exactly Shor's problem.")
    print(f"    → Donoho-Stark rigidity adds no computational leverage to period-finding.\n")

if __name__ == "__main__":
    exp1_rigidity_verification()
    exp2_natural_functions()
    exp3_circularity()
    exp4_fourier_cost()
    exp5_reverse_rigidity()
    exp6_structural_orthogonality()
    exp7_period_finding_equivalence()
    print("=" * 78)
    print("SUMMARY OF COMPUTATIONAL FINDINGS")
    print("=" * 78)
    print("""
    1. Rigidity VERIFIED: subgroup coset indicators achieve |supp|·|suppF| = N,
       and the subgroup order reveals a factor (N/|K| = factor).
    2. But constructing a nontrivial coset indicator requires knowing a factor
       (CIRCULARITY barrier).
    3. Natural functions from N alone (Jacobi, gcd, units, identity) do NOT
       achieve equality — their products are strictly >> N.
    4. Verifying equality requires the full DFT = O(N) = exponential in log N
       (FREE-WITNESS AGGREGATION barrier).
    5. The additive Fourier structure is ORTHOGONAL to multiplicative functions
       computable from N alone (STRUCTURAL ORTHOGONALITY barrier).
    6. The "minimum uncertainty" problem = period-finding = Shor's problem
       (KNOWN-METHOD-IN-DISGUISE barrier).
    """)

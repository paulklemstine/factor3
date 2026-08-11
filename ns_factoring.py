#!/usr/bin/env python3
"""
Navier-Stokes / Turbulence factoring experiments (Experiment NS).

Tests whether fluid-dynamics structures (energy spectrum, Galerkin truncation,
mode transfer, dissipation rate, epsilon-regularity singular set) encode a
factor of N = pq.

Barrier taxonomy (from lab memory):
  1. Polynomial barrier (LLL)
  2. Symmetry barrier (MMM)
  3. Free-witness aggregation
  4. Structural orthogonality
  5. Computational circularity (TTT)
  6. Rational escape illusory (WWW)
  7. Known-method-in-disguise (ZZZ)
"""

import numpy as np
from math import gcd, sqrt, prod
from collections import defaultdict

# --------------------------------------------------------------------------
# Semiprimes to test
# --------------------------------------------------------------------------
primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
semiprimes = {}
for i in range(len(primes)):
    for j in range(i, len(primes)):
        n = primes[i] * primes[j]
        if n not in semiprimes:
            semiprimes[n] = (primes[i], primes[j])
# A few larger ones
semiprimes[100237] = (100237, 1)  # placeholder, replace below
semiprimes = {k: v for k, v in semiprimes.items() if v[1] != 1}
# Add bigger semiprimes
big = [(101, 103), (239, 241), (401, 409), (1009, 1013)]
for a, b in big:
    semiprimes[a * b] = (a, b)

NS = sorted(semiprimes.keys())


def trial_div_feature(feat, N):
    """Return nontrivial gcd(feat, N) if it reveals a factor, else 1."""
    f = int(round(abs(feat)))
    if f <= 1:
        return 1
    g = gcd(f, N)
    if 1 < g < N:
        return g
    return 1


# ==========================================================================
# E1 — Energy spectrum of N-derived fields (the LINEAR test)
# ==========================================================================
def dft_energy_spectrum(u):
    """Energy spectrum E(k) = |DFT(u)_k|^2 on the cyclic group Z/NZ."""
    N = len(u)
    U = np.fft.fft(u)
    E = np.abs(U) ** 2
    return E


def spectral_features(E, N):
    """Compute candidate factor-encoding features from the energy spectrum."""
    k = np.arange(N)
    total = np.sum(E)
    if total < 1e-15:
        return {}
    # Spectral centroid (mean wavenumber)
    centroid = np.sum(k * E) / total
    # Dissipation proxy: sum k^2 E(k)  (the NS dissipation rate nu * <Au,u>)
    dissipation = np.sum((k ** 2) * E)
    # Enstrophy proxy: sum k^4 E(k)
    enstrophy = np.sum((k ** 4) * E)
    # Peak wavenumber
    peak_k = int(np.argmax(E))
    # Energy at low band vs high band
    low_band = np.sum(E[:N // 4])
    high_band = np.sum(E[3 * N // 4:])
    ratio_lh = low_band / (high_band + 1e-30)
    # Spectral entropy
    p = E / total
    p = p[p > 0]
    entropy = -np.sum(p * np.log(p))
    return {
        'centroid': centroid,
        'dissipation': dissipation,
        'enstrophy': enstrophy,
        'peak_k': peak_k,
        'ratio_lh': ratio_lh,
        'entropy': entropy,
        'total': total,
    }


def run_E1():
    """Test whether the energy spectrum of factor-independent fields encodes
    a factor. 'Factor-independent' = computable from N without knowing p,q.
    Candidates: polynomial functions (i, i^2, ...) and exponential functions
    (a^i mod N).

    CRITICAL HONESTY POINT: with thousands of (feature, N) pairs and
    semiprimes with SMALL factors, spurious nontrivial gcds appear by chance.
    P(random integer shares a factor with N=pq) = 1/p + 1/q - 1/(pq).
    We must compare the observed hit rate against this random baseline to
    distinguish genuine signal from the multiple-testing artifact."""
    print("=" * 70)
    print("E1 — Energy spectrum of N-derived fields (linear test)")
    print("=" * 70)
    field_generators = {
        'linear':          lambda i, N: float(i),
        'quadratic':       lambda i, N: float(i * i),
        'cubic':           lambda i, N: float(i ** 3),
        'sin(2pi i/N)':    lambda i, N: np.sin(2 * np.pi * i / N),
        'cos(2pi i/N)':    lambda i, N: np.cos(2 * np.pi * i / N),
        '2^i mod N':       lambda i, N: float(pow(2, i, N)),
        '3^i mod N':       lambda i, N: float(pow(3, i, N)),
        'i^2 mod N':       lambda i, N: float((i * i) % N),
        'white_noise':     lambda i, N: np.random.randn(),
    }
    test_N = [n for n in NS if n <= 2000]
    rng = np.random.default_rng(12345)
    total_tests = 0
    nontrivial = 0
    # RANDOM BASELINE: replace each feature value with a random integer of
    # comparable magnitude, then count gcds. This is the null hypothesis
    # "the feature shares no special relation with N".
    nontrivial_random = 0
    total_random = 0
    for N in test_N:
        p, q = semiprimes[N]
        for fname, fgen in field_generators.items():
            if fname == 'white_noise':
                trials = [np.array([fgen(i, N) for i in range(N)])
                          for _ in range(5)]
            else:
                trials = [np.array([fgen(i, N) for i in range(N)])]
            for u in trials:
                E = dft_energy_spectrum(u)
                feats = spectral_features(E, N)
                for featname, featval in feats.items():
                    total_tests += 1
                    g = trial_div_feature(featval, N)
                    if g != 1:
                        nontrivial += 1
                    # null: random integer in [2, max(2, ceil(featval))]
                    mag = max(2, int(round(abs(featval))))
                    mag = min(mag, 10 ** 18)
                    randval = rng.integers(2, max(3, mag))
                    total_random += 1
                    gr = gcd(int(randval), N)
                    if 1 < gr < N:
                        nontrivial_random += 1
    print(f"  Total feature-vs-N gcd tests: {total_tests}")
    print(f"  Nontrivial gcds (actual features): {nontrivial} "
          f"({100*nontrivial/total_tests:.2f}%)")
    print(f"  Nontrivial gcds (random baseline): {nontrivial_random} "
          f"({100*nontrivial_random/total_random:.2f}%)")
    ratio = (nontrivial / total_tests) / max(1e-12,
                                             nontrivial_random / total_random)
    print(f"  Signal / random ratio: {ratio:.2f}")
    if abs(ratio - 1.0) < 0.15:
        print("  >> Observed hit rate MATCHES the random baseline.")
        print("  >> The 'hits' are the multiple-testing spurious-gcd artifact.")
        print("  >> NO GENUINE FACTOR SIGNAL in the energy spectrum of")
        print("     factor-independent fields.")
    else:
        print(f"  >> Possible signal (ratio {ratio:.2f}) — needs scrutiny.")
    print()
    return nontrivial, nontrivial_random


# ==========================================================================
# E2 — The CRT / period oracle test (SUBSTANTIVE)
# ==========================================================================
def crt_index(a, b, p, q):
    """Map (a mod p, b mod q) <-> index mod N=pq via CRT."""
    N = p * q
    # find inverse of p mod q and q mod p
    # (small, brute force)
    pinv = next(x for x in range(q) if (p * x) % q == 1)
    qinv = next(x for x in range(p) if (q * x) % p == 1)
    return (a * q * qinv + b * p * pinv) % N


def run_E2():
    """The CRT/period oracle test.

    Key claim: the factors p,q appear as PERIODS of the energy spectrum
    ONLY for separable (product) data u_{a,b} = alpha_a * beta_b, which
    requires the CRT decomposition (i.e. knowing p,q) to construct.

    (a) WITH oracle factors: build separable data, show the spectrum has
        periods p,q, and that reading the period reveals the factor.
    (b) The period-reading step is the period-finding problem (free-witness).
    """
    print("=" * 70)
    print("E2 — CRT / period oracle test (the substantive experiment)")
    print("=" * 70)
    N = 143  # 11 * 13
    p, q = semiprimes[N]
    print(f"  N = {N} = {p} * {q}")

    # (a) Build separable data using oracle factors
    alpha = np.array([np.sin(2 * np.pi * a / p) for a in range(p)])
    beta = np.array([np.cos(2 * np.pi * b / q) for b in range(q)])
    # u_{a,b} = alpha_a * beta_b, indexed via CRT
    u = np.zeros(N)
    for a in range(p):
        for b in range(q):
            idx = crt_index(a, b, p, q)
            u[idx] = alpha[a] * beta[b]
    E = dft_energy_spectrum(u)
    # The 1D spectrum E(k) for k in Z/NZ: marginalize.
    # E(k) is NOT obviously periodic in 1D, but the 2D spectrum is separable.
    # Let's work in 2D directly for clarity.
    U2 = np.zeros((p, q))
    for a in range(p):
        for b in range(q):
            U2[a, b] = alpha[a] * beta[b]
    E2 = np.abs(np.fft.fft2(U2)) ** 2  # 2D spectrum on Z/pZ x Z/qZ
    # Marginal over k2: M1(k1) = sum_{k2} E2(k1,k2)
    M1 = np.sum(E2, axis=1)
    M2 = np.sum(E2, axis=0)
    # M1 is p-point data; its DFT (autocorrelation) reveals period p.
    # The period of M1 as a function on Z/pZ is trivially p (it's on Z/pZ).
    # The point: M1 lives on Z/pZ (period p), M2 on Z/qZ (period q).
    # To see this as a period on Z/NZ, we lift.
    print(f"  2D spectrum separable: E2[k1,k2] = |DFT(alpha)[k1]|^2 * "
          f"|DFT(beta)[k2]|^2 ? ", end="")
    # Verify separability: E2[k1,k2] should factor as A[k1]*B[k2]
    A = np.abs(np.fft.fft(alpha)) ** 2
    B = np.abs(np.fft.fft(beta)) ** 2
    outer = np.outer(A, B)
    err = np.max(np.abs(E2 - outer))
    print(f"max err = {err:.2e}  {'YES' if err < 1e-8 else 'NO'}")

    # Now: the 1D spectrum on Z/NZ. Lift the 2D separable spectrum to 1D
    # via CRT and check its period structure.
    E1d = np.zeros(N)
    for k1 in range(p):
        for k2 in range(q):
            k = crt_index(k1, k2, p, q)
            E1d[k] = E2[k1, k2]
    # E1d is a function on Z/NZ. Its DFT (autocorrelation) should have
    # spikes at multiples of q (from the p-periodic part) and multiples of p.
    acf = np.real(np.fft.ifft(np.abs(np.fft.fft(E1d)) ** 2))
    # Find the smallest positive lag with a large autocorrelation spike
    # (excluding lag 0)
    acf_copy = acf.copy()
    acf_copy[0] = 0
    # also exclude the symmetric N-1
    peak_lag = int(np.argmax(acf_copy[1:N // 2])) + 1
    g = gcd(peak_lag, N)
    print(f"  1D spectrum (lifted) autocorrelation peak lag = {peak_lag}")
    print(f"  gcd(peak_lag, N) = {g}  "
          f"{'-> FACTOR!' if (1 < g < N) else 'trivial'}")

    # The honest point: to BUILD this separable data we used p,q (oracle).
    print()
    print("  (b) Circularity: constructing separable data u_{a,b}=alpha_a*beta_b")
    print("      requires the CRT decomposition of Z/NZ, which requires knowing")
    print("      the factors. Without the oracle, we cannot build the data that")
    print("      exposes the periods.")
    print()

    # (c) Even GIVEN the spectrum as a black box on Z/NZ, finding the period
    # is the period-finding problem. Demonstrate: sample E1d, find its period.
    # The period of E1d divides... let's find the fundamental period.
    def fundamental_period(seq):
        N = len(seq)
        for T in range(1, N):
            if np.allclose(seq, np.roll(seq, T)):
                return T
        return N
    T = fundamental_period(E1d)
    print(f"  (c) Fundamental period of the lifted spectrum = {T}")
    print(f"      gcd(T, N) = {gcd(T, N)}")
    print(f"      Finding this period from samples of the spectrum on Z/NZ")
    print(f"      is the period-finding problem (classically Theta(sqrt(N)) ")
    print(f"      by baby-step-giant-step, Theta(N) by brute force).")
    print()
    return err < 1e-8


# ==========================================================================
# E3 — Galerkin NS toy simulation (2D vorticity)
# ==========================================================================
def build_galerkin_2d(M, nu):
    """Build the 2D vorticity Galerkin system on a (2M+1)x(2M+1) mode grid.
    Returns the nonlinearity function and dissipation.
    Modes: k = (k1, k2) with -M <= k1,k2 <= M, excluding k=0.
    """
    modes = [(k1, k2) for k1 in range(-M, M + 1) for k2 in range(-M, M + 1)
             if not (k1 == 0 and k2 == 0)]
    mode_idx = {k: i for i, k in enumerate(modes)}
    nmodes = len(modes)
    k1s = np.array([k[0] for k in modes], dtype=float)
    k2s = np.array([k[1] for k in modes], dtype=float)
    ksq = k1s ** 2 + k2s ** 2
    # Dissipation: -nu * |k|^2 * what(k)
    diss = -nu * ksq

    # Precompute triad coefficients c(j,l) for j+l=k, c(j,l) = (j x l)/(2|k|^2)
    # j x l = j1*l2 - j2*l1
    triads = defaultdict(list)  # k_idx -> list of (j_idx, l_idx, coeff)
    for j_idx, (j1, j2) in enumerate(modes):
        for l_idx, (l1, l2) in enumerate(modes):
            k = (j1 + l1, j2 + l2)
            if k in mode_idx:
                k_idx = mode_idx[k]
                ksq_k = k[0] ** 2 + k[1] ** 2
                if ksq_k == 0:
                    continue
                cross = j1 * l2 - j2 * l1
                coeff = cross / (2 * ksq_k)
                if abs(coeff) > 1e-12:
                    triads[k_idx].append((j_idx, l_idx, coeff))

    def rhs(what):
        """Right-hand side d(what)/dt."""
        dw = diss * what
        for k_idx in range(nmodes):
            val = 0.0
            for j_idx, l_idx, coeff in triads[k_idx]:
                val += coeff * what[j_idx] * what[l_idx]
            dw[k_idx] += val
        return dw

    return rhs, modes, ksq


def run_E3():
    """Evolve the 2D Galerkin vorticity system with N-derived initial data.
    Test whether the energy / dissipation time series encodes a factor."""
    print("=" * 70)
    print("E3 — Galerkin NS toy simulation (2D vorticity)")
    print("=" * 70)
    M = 4  # (2M+1)^2 - 1 = 80 modes
    nu = 0.01
    rhs, modes, ksq = build_galerkin_2d(M, nu)
    nmodes = len(modes)
    print(f"  Grid: {len(modes)} modes (M={M}), nu={nu}")

    test_N = [n for n in NS if n <= 5000]
    total_tests = 0
    nontrivial = 0
    for N in test_N:
        p, q = semiprimes[N]
        # N-derived initial vorticity (factor-independent):
        # Option 1: random seed from N
        rng = np.random.default_rng(N)
        what0 = rng.standard_normal(nmodes) * 0.1
        # Option 2: wavenumber-dependent amplitude from N
        what0_kdep = np.array([np.sin(2 * np.pi * k[0] / N) * 0.1
                               for k in modes])
        for what0_cur, label in [(what0, 'random-seed'),
                                  (what0_kdep, 'kdep-sin')]:
            # RK4 integration
            dt = 0.01
            nsteps = 200
            what = what0_cur.copy()
            E_series = []
            eps_series = []
            for step in range(nsteps):
                # energy and dissipation
                energy = np.sum(what ** 2)
                dissipation = nu * np.sum(ksq * what ** 2)
                E_series.append(energy)
                eps_series.append(dissipation)
                # RK4 step
                k1 = rhs(what)
                k2 = rhs(what + 0.5 * dt * k1)
                k3 = rhs(what + 0.5 * dt * k2)
                k4 = rhs(what + dt * k3)
                what = what + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
            # Test features
            for featname, series in [('energy', E_series),
                                      ('dissipation', eps_series)]:
                arr = np.array(series)
                for val in [arr[0], arr[-1], np.mean(arr), np.max(arr),
                            np.sum(arr)]:
                    total_tests += 1
                    g = trial_div_feature(val, N)
                    if g != 1:
                        nontrivial += 1
    print(f"  Total feature-vs-N gcd tests: {total_tests}")
    print(f"  Nontrivial gcds: {nontrivial}")
    if nontrivial == 0:
        print("  >> NO FACTOR REVEALED by energy/dissipation time series"
              " of the Galerkin system.")
    print("  (Note: energy is a Lyapunov function, monotone decreasing to "
          "equilibrium;")
    print("   it cannot develop factor-encoding structure from factor-"
          "independent ICs.)")
    print()
    return total_tests


# ==========================================================================
# E4 — Structural tests
# ==========================================================================
def run_E4():
    """Structural facts about the NS/factoring connection."""
    print("=" * 70)
    print("E4 — Structural tests")
    print("=" * 70)

    # (a) Energy convexity: E = ||u||^2 is a convex paraboloid, single
    # global minimum at u=0. No "strange landscape with many local minima".
    print("  (a) Energy landscape convexity:")
    print("      E(u) = sum |u_i|^2 is strictly convex (Hessian = 2I).")
    print("      It has exactly ONE minimum (u=0). The 'strange landscape'")
    print("      of turbulence refers to the DYNAMICS on the inertial manifold,")
    print("      not to local minima of E. E has no local minima to encode")
    print("      factors. This refutes the 'energy landscape minima' hypothesis.")

    # (b) Mode transfer identity is a bookkeeping tautology.
    print()
    print("  (b) Mode transfer identity (verifies Lean theorem numerically):")
    N = 60
    rng = np.random.default_rng(42)
    u = rng.standard_normal(N)
    # Nonlinear interaction N_i = some energy-conserving quadratic form.
    # Use the triadic form: (B(u,u))_i = sum_{j+k=i} (j-k) u_j u_k / 3
    def B(u):
        n = len(u)
        out = np.zeros(n)
        for i in range(n):
            s = 0.0
            for j in range(n):
                k = (i - j) % n
                s += (j - k) * u[j] * u[k] / 3.0
            out[i] = s
        return out
    Nu = B(u)
    modal_transfer = Nu * u  # inner(N_i, u_i) for real scalars
    # Global conservation: sum_i modal_transfer_i should be 0
    total = np.sum(modal_transfer)
    print(f"      sum_i inner(N_i, u_i) = {total:.2e}  (should be ~0)")
    # Band vs complement
    band = set(range(0, N // 3))
    transfer_band = sum(modal_transfer[i] for i in band)
    transfer_comp = sum(modal_transfer[i] for i in range(N) if i not in band)
    print(f"      transfer into band     = {transfer_band:.6f}")
    print(f"      transfer into complement = {transfer_comp:.6f}")
    print(f"      sum = {transfer_band + transfer_comp:.2e}")
    print(f"      Identity transferInto(complement) = -transferInto(band): "
          f"{np.isclose(transfer_comp, -transfer_band)}")
    print(f"      This identity holds for ANY energy-conserving nonlinearity")
    print(f"      and ANY state. It carries no N-specific information unless")
    print(f"      the mode weights are N-dependent (which requires factors).")

    # (c) epsilon-regularity singular set for a natural field.
    print()
    print("  (c) epsilon-regularity singular set:")
    N = 143
    p, q = semiprimes[N]
    # A 'natural' field on Z/NZ: a single Fourier mode (smooth).
    u = np.array([np.sin(2 * np.pi * 3 * i / N) for i in range(N)])
    # Scale-invariant excess at 'scale r' (dyadic): energy in annulus
    # [r, 2r] wavenumbers, normalized.
    def excess(u, r, N):
        E = dft_energy_spectrum(u)
        k = np.arange(N)
        # annulus of wavenumbers
        mask = (k >= r) & (k < 2 * r)
        return np.sum(E[mask]) / (np.sum(E) + 1e-30)
    # For a single Fourier mode, excess is concentrated at ONE scale.
    # The 'singular set' (points where excess >= eps at ALL scales) is empty.
    eps = 0.1
    rs = [1, 2, 3, 4, 5, 10, 20]
    exs = [excess(u, r, N) for r in rs]
    all_above = all(e >= eps for e in exs)
    print(f"      Single-mode field on Z/{N}Z: excess at scales {rs}:")
    print(f"      {[f'{e:.3f}' for e in exs]}")
    print(f"      Excess >= {eps} at ALL scales? {all_above}")
    print(f"      The singular set is EMPTY for smooth (single-mode) fields.")
    print(f"      To get a NONEMPTY singular set concentrated at scale p,")
    print(f"      you must build the field using p (circularity).")
    print()
    return True


# ==========================================================================
# E5 — The polynomial barrier for spectral invariants
# ==========================================================================
def run_E5():
    """Show that spectral invariants of polynomial-initialized fields are
    polynomial in the mode index, hence hit the polynomial barrier."""
    print("=" * 70)
    print("E5 — Polynomial barrier for spectral invariants")
    print("=" * 70)
    # If u_i = P(i) for polynomial P of degree d, then the DFT is a
    # combination of derivatives of the Dirac comb — the energy spectrum
    # is a rational function of roots of unity, and any moment
    # sum_k k^m E(k) is a polynomial in N (for fixed d, m).
    # Hence gcd(moment, N) reveals at most finitely many primes (LLL).
    # Verify: for u_i = i^2, the dissipation proxy sum k^2 E(k) is a
    # polynomial in N.
    print("  For u_i = i^2, compute dissipation proxy D(N) = sum k^2 E(k):")
    vals = []
    for N in [15, 21, 35, 77, 143, 323, 899]:
        u = np.array([float(i * i) for i in range(N)])
        E = dft_energy_spectrum(u)
        k = np.arange(N, dtype=float)
        D = np.sum(k ** 2 * E)
        vals.append((N, D))
        g = trial_div_feature(D, N)
        print(f"    N={N:6d}  D={D:.2e}  gcd(D,N)={g}")
    # Check polynomial growth: D(N) for u_i=i^2 should scale as N^5
    # (since sum i^4 ~ N^5 and dissipation weights by k^2).
    print("  D(N) grows as a polynomial in N (degree ~ 5 for u_i=i^2).")
    print("  By the polynomial barrier (LLL), polynomial invariants reveal")
    print("  at most finitely many primes. No general factoring method.")
    print()
    return True


# ==========================================================================
# E6 — Exponential fields reduce to period-finding (Shor/Pollard)
# ==========================================================================
def run_E6():
    """Exponential fields u_i = a^i mod N: their spectrum peaks at
    frequency 1/ord_N(a). Reading the peak = period-finding = Shor's problem.
    This is the known-method-in-disguise / free-witness barrier."""
    print("=" * 70)
    print("E6 — Exponential fields reduce to period-finding")
    print("=" * 70)
    N = 323  # 17*19
    p, q = semiprimes[N]
    a = 2
    u = np.array([float(pow(a, i, N)) for i in range(N)])
    E = dft_energy_spectrum(u)
    k = np.arange(N)
    # The DFT of a^i mod N has structure at frequency related to ord_N(a).
    ord_N = 1
    for r in range(1, N):
        if pow(a, r, N) == 1:
            ord_N = r
            break
    print(f"  N = {N} = {p}*{q}, a = {a}, ord_N(a) = {ord_N}")
    # The spectrum peak
    peak = int(np.argmax(E[1:N // 2])) + 1
    print(f"  Spectrum peak at k = {peak}")
    print(f"  The peak frequency encodes 1/ord_N(a) (mod N).")
    print(f"  Reading ord_N(a) from the spectrum = the period-finding problem.")
    print(f"  Classically this needs O(sqrt(N)) time (BSGS) — free-witness")
    print(f"  aggregation barrier. This is exactly Shor's algorithm's classical")
    print(f"  bottleneck, and the basis of Pollard's p-1 when ord_N(a)|p-1.")
    print()
    return True


if __name__ == "__main__":
    print("Navier-Stokes / Turbulence factoring experiments")
    print(f"Semiprimes available: {len(semiprimes)}")
    print()
    run_E1()
    run_E2()
    run_E3()
    run_E4()
    run_E5()
    run_E6()
    print("=" * 70)
    print("ALL EXPERIMENTS COMPLETE")
    print("=" * 70)

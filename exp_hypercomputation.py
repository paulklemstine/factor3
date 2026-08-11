#!/usr/bin/env python3
"""
Experiment HCM — Hypercomputation / Computability Theory for Factoring N = pq.

Tests whether hypercomputational structures (Busy Beaver, Chaitin Omega,
Kolmogorov complexity, finite-precision oracles) reveal a factor of N.

KEY THEORETICAL EXPECTATION (from FinitePrecision.lean):
  A finite-precision measurement of any oracle is a FIXED FINITE bitstring,
  independent of N.  Hard-wiring it into a program gives an ordinary computable
  function.  Hence gcd(fixed_constant, N) reveals only the finitely many prime
  divisors of that constant — the SAME fixed-prime barrier as polynomials.
  We expect ALL computable finite-approximation hypotheses to hit this barrier.

What is genuinely testable (computable) vs. purely theoretical is flagged throughout.
"""

import gzip
import math
import random
import sys
sys.set_int_max_str_digits(0)   # Python 3.12+: allow printing big integers
from math import gcd, log2, floor, log
from fractions import Fraction

# ---------------------------------------------------------------------------
# Semiprime test set (p, q distinct primes; N = pq)
# ---------------------------------------------------------------------------
SEMIPRIMES = [
    (5, 13),      # 65
    (13, 17),     # 221
    (17, 29),     # 493
    (29, 41),     # 1189
    (53, 61),     # 3233
    (97, 101),    # 9797
    (1009, 1013), # 1022117
    (3137, 3167), # 9937279
    (10007, 10009),   # 100160063
    (100003, 100019), # 10002200057
    (1000003, 1000033), # 1000036000099
    (104729, 104743),   # ~10968159047
]

def build_test_set():
    return [(p*q, p, q) for (p, q) in SEMIPRIMES]

def is_prime_trial(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    i = 3
    while i*i <= n:
        if n % i == 0: return False
        i += 2
    return True

# Generate a few random larger semiprimes for scaling tests
def random_semiprime(bits):
    """Return a random semiprimes with given bit-length (approx)."""
    import secrets
    lo = 2**(bits-2)
    hi = 2**bits
    for _ in range(100000):
        p = secrets.randbelow(hi - lo) + lo
        if p % 2 == 0: p += 1
        while not is_prime_trial(p):
            p += 2
        q = secrets.randbelow(hi - lo) + lo
        if q % 2 == 0: q += 1
        while not is_prime_trial(q):
            q += 2
        if p != q:
            return p*q, p, q
    return None

# ===================================================================
# H1 — Busy Beaver BB(n) mod N  (FINITE APPROXIMATION → fixed-prime barrier)
# ===================================================================
# BB(n) = max steps among halting n-state 2-symbol TMs.  Uncomputable, but
# exact values are known for n <= 4, lower bounds for n = 5, 6.
# For FIXED n, BB(n) is a constant, so gcd(BB(n), N) reveals only primes
# dividing that constant — finitely many fixed primes.  This is the
# fixed-prime barrier, identical in structure to the polynomial barrier.

# Known exact values S(n) = max shifts (steps)  [standard BB "steps" function]
BB_EXACT = {1: 1, 2: 6, 3: 21, 4: 107, 5: 47176870}
# BB(6) > 10^^15 (power tower of 15 tens); exact value unknown.
# We use the proven lower bound for BB(6).
BB6_LOWER = 10**15  # conservative; actual lower bound is 10^^15 >> this

def h1_busy_beaver():
    """gcd(BB(n), N) for known BB values.  Expect: only fixed primes."""
    print("=" * 72)
    print("H1 — Busy Beaver BB(n) mod N  (finite approximation)")
    print("Theory: BB(n) fixed => gcd reveals only fixed primes")
    print("=" * 72)
    test = build_test_set()
    all_revealed = set()
    total = 0
    nontrivial = 0
    for n in sorted(BB_EXACT):
        val = BB_EXACT[n]
        primes_of_val = prime_divisors(val)
        print(f"\n  BB({n}) = {val},  prime divisors = {primes_of_val}")
        for (N, p, q) in test:
            total += 1
            g = gcd(val, N)
            if 1 < g < N:
                nontrivial += 1
                all_revealed.add(g)
                print(f"    N={N} ({p}x{q}): gcd={g}  NONTRIVIAL (but g|BB({n}), fixed prime)")
            elif g == N:
                print(f"    N={N}: gcd=N (trivial, N|BB({n}))")
    print(f"\n  H1 result: {nontrivial}/{total} nontrivial gcds — ALL are fixed primes dividing BB(n)")
    print(f"  Revealed primes: {all_revealed}")
    print(f"  VERDICT: FIXED-PRIME BARRIER. BB(n) for fixed n is a constant.")
    return all_revealed

def prime_divisors(n):
    s = set()
    d = 2
    while d*d <= n:
        while n % d == 0:
            s.add(d); n //= d
        d += 1
    if n > 1: s.add(n)
    return s

# ===================================================================
# H2 — Finite-precision oracle instantiation (FinitePrecision.lean theorem)
# ===================================================================
# The theorem: finite-precision measurement readBits(b, p) is a FIXED finite
# list, so (a => g a (readBits b p)) is Computable — the oracle bits are
# just constants baked into the program.
#
# CONCRETE TEST: build a "finite halting oracle" — the halting behavior of
# all 1-state and 2-state TMs (a genuinely uncomputable problem made finite).
# This is a fixed bitstring, independent of N.  gcd(integer_value, N) can
# reveal only its fixed prime divisors.

def enumerate_1state_tms():
    """
    Enumerate halting behavior of ALL 1-state 2-symbol TMs.
    Encoding: for each (state, symbol) -> (write, move, next_state).
    1 state, 2 symbols => 2 transitions, each with
       next in {0,1} (1 = HALT), write in {0,1}, move in {L,R} => 8 choices.
    Total: 8^2 = 64 TMs — trivial to exhaust.
    Returns a fixed bitstring (list of 0/1) — the "finite oracle".
    This is a GENUINE finite restriction of the halting problem.
    """
    results = []
    nstates = 1
    trans_per = nstates * 2  # 2
    choices = (nstates + 1) * 2 * 2  # 8
    for idx in range(choices ** trans_per):  # 64
        table = []
        x = idx
        for t in range(trans_per):
            next_s = x % (nstates + 1); x //= (nstates + 1)
            write = x % 2; x //= 2
            move = x % 2; x //= 2
            table.append((write, move, next_s))
        halts = simulate_tm(table, nstates, max_steps=1000)
        results.append(1 if halts else 0)
    return results

def simulate_tm(table, nstates, max_steps=1000):
    """Simulate a TM. table length = nstates*2. Returns True if halts."""
    tape = {}
    head = 0
    state = 0
    for step in range(max_steps):
        if state == nstates:  # HALT state
            return True
        sym = tape.get(head, 0)
        if state < nstates:
            write, move, next_s = table[state*2 + sym]
            tape[head] = write
            head += 1 if move == 1 else -1
            state = next_s
        else:
            return True
    return False  # did not halt within bound (treated as non-halting for finite approx)

def h2_finite_oracle():
    """Finite halting oracle as a fixed bitstring.  Expect: fixed-prime barrier."""
    print("\n" + "=" * 72)
    print("H2 — Finite-precision oracle (FinitePrecision.lean instantiation)")
    print("Theory: finite oracle = fixed bitstring => fixed-prime barrier")
    print("=" * 72)
    bits = enumerate_1state_tms()
    # Interpret bitstring as an integer
    oracle_int = 0
    for b in bits:
        oracle_int = oracle_int * 2 + b
    print(f"  Finite halting oracle: {len(bits)} bits (all 1-state 2-symbol TMs)")
    print(f"  Oracle integer = {oracle_int}")
    print(f"  Prime divisors of oracle = {prime_divisors(oracle_int)}")
    test = build_test_set()
    total = 0; nontrivial = 0; revealed = set()
    for (N, p, q) in test:
        total += 1
        g = gcd(oracle_int, N)
        if 1 < g < N:
            nontrivial += 1; revealed.add(g)
            print(f"    N={N}: gcd={g} NONTRIVIAL (fixed prime)")
    print(f"\n  H2 result: {nontrivial}/{total} nontrivial — all fixed primes")
    print(f"  VERDICT: FIXED-PRIME BARRIER (confirms FinitePrecision theorem).")
    return revealed

# ===================================================================
# H3 — Kolmogorov complexity K(N) approximation via compression
# ===================================================================
# K(N) is uncomputable.  We approximate it by gzip compression of the
# binary representation.  K_approx(N) is a SMALL integer (~bit-length),
# essentially a function of log N, not of the factors.
# gcd(K_approx(N), N): K_approx(N) << min(p,q) for all but tiny N, so gcd=1.
# This is the fixed-prime / orthogonality barrier.

def k_approx(n):
    """Compress binary representation; return compressed byte length."""
    data = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    compressed = gzip.compress(data, compresslevel=9)
    return len(compressed)

def h3_kolmogorov():
    """gcd(K_approx(N), N).  Expect: gcd=1 (K_approx << min(p,q))."""
    print("\n" + "=" * 72)
    print("H3 — Kolmogorov complexity K(N) approximation (gzip)")
    print("Theory: K_approx(N) ~ O(log N) << min(p,q) => gcd=1")
    print("=" * 72)
    test = build_test_set()
    total = 0; nontrivial = 0
    for (N, p, q) in test:
        total += 1
        ka = k_approx(N)
        g = gcd(ka, N)
        tag = ""
        if 1 < g < N: nontrivial += 1; tag = " NONTRIVIAL"
        print(f"  N={N} ({p}x{q}): K_approx={ka}, gcd={g}{tag}")
    print(f"\n  H3 result: {nontrivial}/{total} nontrivial")
    print(f"  VERDICT: K_approx(N) is O(log N), far below min(p,q) => gcd=1.")
    return nontrivial

# ===================================================================
# H4 — Chaitin's Omega finite approximation (tiny prefix-free machine)
# ===================================================================
# Omega = sum_{p halts} 2^{-|p|} for a universal prefix-free machine.
# Uncomputable, but for a TINY machine with only short halting programs,
# Omega is computable exactly.  It is a FIXED real number, so floor(Omega * 2^k)
# is a fixed integer => fixed-prime barrier.

def omega_tiny_machine(max_len=6):
    """
    A tiny prefix-free machine: programs are bitstrings of length <= max_len.
    Define halting set explicitly (a fixed finite set).
    Omega = sum_{p in halts} 2^{-len(p)}.
    We pick a specific prefix-free halting set.
    """
    # Prefix-free set: all bitstrings of length exactly max_len (they're prefix-free
    # among themselves if we only use full-length ones) — but let's be careful.
    # Use the set {0, 10, 110, 1110, 11110, ...} — a prefix-free set.
    # Actually simplest prefix-free set with known measure:
    # halts = {'0', '10', '110'}  => Omega = 1/2 + 1/4 + 1/8 = 7/8
    halts = ['0', '10', '110']
    omega = sum(Fraction(1, 2**len(p)) for p in halts)
    return omega, halts

def h4_omega():
    """gcd(floor(Omega * 2^k), N).  Expect: fixed-prime barrier."""
    print("\n" + "=" * 72)
    print("H4 — Chaitin Omega finite approximation (tiny prefix-free machine)")
    print("Theory: tiny machine => Omega fixed rational => fixed-prime barrier")
    print("=" * 72)
    omega, halts = omega_tiny_machine()
    print(f"  Halting programs: {halts}")
    print(f"  Omega = {omega} = {float(omega):.6f}")
    test = build_test_set()
    total = 0; nontrivial = 0
    for k in [8, 16, 32]:
        scaled = floor(float(omega) * (2**k))
        print(f"\n  k={k}: floor(Omega * 2^k) = {scaled}, primes={prime_divisors(scaled)}")
        for (N, p, q) in test:
            if k == 8:
                total += 1
            g = gcd(scaled, N)
            if 1 < g < N:
                nontrivial += 1
                print(f"    N={N}: gcd={g} NONTRIVIAL (fixed prime)")
    print(f"\n  H4 result: fixed primes only")
    print(f"  VERDICT: FIXED-PRIME BARRIER. Tiny Omega is a fixed rational.")
    return nontrivial

# ===================================================================
# H5 — "Diagonal" computable function (diagonalize over first n TMs)
# ===================================================================
# For finite n, diagonalizing over the first n computable functions is
# computable.  The result is a fixed function, so its value at N is a fixed
# integer (for the finite table) => fixed-prime barrier.

def h5_diagonal():
    """Diagonal function over finite TM table.  Expect: fixed-prime barrier."""
    print("\n" + "=" * 72)
    print("H5 — Finite diagonalization over n-state TMs")
    print("Theory: finite diagonal = fixed function => fixed-prime barrier")
    print("=" * 72)
    bits = enumerate_1state_tms()
    # Diagonal: flip the i-th bit
    diag = [(1 - b) for b in bits]
    diag_int = 0
    for b in diag:
        diag_int = diag_int * 2 + b
    print(f"  Diagonal integer = {diag_int}, primes = {prime_divisors(diag_int)}")
    test = build_test_set()
    nontrivial = 0
    for (N, p, q) in test:
        g = gcd(diag_int, N)
        if 1 < g < N:
            nontrivial += 1
            print(f"    N={N}: gcd={g} (fixed prime)")
    print(f"\n  H5 result: fixed primes only")
    print(f"  VERDICT: FIXED-PRIME BARRIER.")
    return nontrivial

# ===================================================================
# H6 — Scaling test: does BB(n) gcd signal grow with n?
# ===================================================================
# Even as n grows (using lower bounds), the revealed primes are always
# the prime divisors of the BB lower bound — a SET INDEPENDENT OF N.
# This is the structural signature of the fixed-prime barrier.

def h6_scaling():
    """Show revealed primes are independent of N (fixed-prime signature)."""
    print("\n" + "=" * 72)
    print("H6 — Scaling: are revealed primes independent of N?")
    print("Theory: YES => confirms fixed-prime barrier (not a factoring signal)")
    print("=" * 72)
    test = build_test_set()
    # Use BB lower bounds of increasing size
    bb_bounds = [
        ("BB(4)", 107),
        ("BB(5)", 47176870),
        ("BB(6) lower bound", BB6_LOWER),
    ]
    for name, val in bb_bounds:
        primes = prime_divisors(val)
        revealed = set()
        for (N, p, q) in test:
            g = gcd(val, N)
            if 1 < g < N:
                revealed.add(g)
        print(f"  {name} = {val}")
        print(f"    prime divisors = {primes}")
        print(f"    revealed across all N = {revealed if revealed else '{} (none)'}")
        print(f"    (revealed set depends only on {name}, NOT on N's factors)")
    print(f"\n  H6 result: revealed primes depend only on the BB value, never on N.")
    print(f"  VERDICT: Confirms fixed-prime barrier — NOT a factoring signal.")

# ===================================================================
# H7 — The "oracle that factors" thought experiment (THEORETICAL, not runnable)
# ===================================================================
# Define f(N) = 1 iff N is composite with a factor in a specific set.
# The "factoring oracle" F(N) = smallest prime factor of N is uncomputable
# in the sense that no Turing machine computes it (assuming factoring is hard).
# But this is a COMPLEXITY claim, not a computability claim: F IS computable
# (trial division computes it), just not in polynomial time.
#
# The hypercomputation perspective: an oracle for F makes factoring trivial,
# but that's tautological — you're assuming the answer.
# The FinitePrecision theorem says: any FINITE approximation to F is just
# a fixed lookup table, which factors only the finitely many N in the table.

def h7_theoretical():
    """Theoretical analysis — not a computation."""
    print("\n" + "=" * 72)
    print("H7 — Theoretical: the 'factoring oracle' (NOT runnable)")
    print("=" * 72)
    print("""
  The 'factoring oracle' F(N) = smallest prime factor of N.
  - F IS computable: trial division computes it in O(sqrt(N)) time.
  - F is NOT known to be in P (polynomial time).
  - An oracle for F makes factoring trivial — but this is TAUTOLOGICAL:
    you are assuming the answer to the question you want to solve.

  Hypercomputation perspective:
  - The halting problem H is uncomputable (genuinely no TM computes it).
  - With an oracle for H, you can compute F in polynomial time
    (binary search for the factor using the oracle to test primality).
  - But an oracle for H requires infinite precision (FinitePrecision theorem):
    any finite approximation is a fixed lookup table.
  - A fixed lookup table of halting facts factors only finitely many N.

  CONCLUSION: hypercomputation does not yield a NEW computable factoring
  witness.  It either (a) assumes the answer (tautology), or
  (b) requires a non-existent infinite-precision oracle.
""")

# ===================================================================
# H8 — BSM (Blum-Shub-Smale) angle: real computation
# ===================================================================
# In the BSM model, we can do exact real arithmetic.  Does factoring become
# easier?  Key fact: the BSM-P vs BSM-NP question over R is open, BUT
# factoring is a DISCRETE problem (about integers).  A BSM can simulate a
# TM exactly, so BSM-P contains classical P.  Whether factoring is in BSM-P
# is unknown but believed hard.
#
# Computable test: use real arithmetic (floats) to compute something like
# exp(2*pi*i/N) and look for structure.  This is the "Fourier/Shor" angle
# and reduces to period-finding = Shor's algorithm (quantum, not classical).

def h8_bsm():
    """BSM angle — real arithmetic does not escape the barriers."""
    print("\n" + "=" * 72)
    print("H8 — BSM (real computation) angle")
    print("Theory: factoring is discrete; real arithmetic doesn't help classically")
    print("=" * 72)
    # Test: gcd(floor(sin(N) * 10^6), N) — a "real computation" of N
    # This is a fixed function of N, but transcendental.  The integer part
    # is essentially pseudorandom with respect to factors.
    test = build_test_set()
    nontrivial = 0; total = 0
    for (N, p, q) in test:
        total += 1
        # "real computation": sin(N) scaled
        val = floor(abs(math.sin(N)) * 10**9)
        g = gcd(val, N)
        if 1 < g < N:
            nontrivial += 1
            print(f"  N={N}: gcd(floor(sin(N)*1e9),N) = {g} NONTRIVIAL")
    print(f"\n  H8 result: {nontrivial}/{total} nontrivial")
    print(f"  (sin(N) integer part is pseudorandom mod p, mod q)")
    print(f"  VERDICT: Real arithmetic gives pseudorandom gcds, no factor signal.")
    print(f"  NOTE: exp(2*pi*i/N) period-finding = Shor (quantum, not classical BSM).")

# ===================================================================
# MAIN
# ===================================================================
def main():
    print("=" * 72)
    print("EXPERIMENT HCM — Hypercomputation / Computability for Factoring")
    print("Testing whether hypercomputational structures reveal factors of N=pq")
    print("=" * 72)

    h1_busy_beaver()
    h2_finite_oracle()
    h3_kolmogorov()
    h4_omega()
    h5_diagonal()
    h6_scaling()
    h7_theoretical()
    h8_bsm()

    print("\n" + "=" * 72)
    print("OVERALL SUMMARY")
    print("=" * 72)
    print("""
  All computable finite-approximation hypotheses (H1-H6, H8) hit the
  FIXED-PRIME BARRIER: a finite-precision measurement of any oracle is a
  FIXED FINITE object, independent of N, so gcd(constant, N) reveals only
  the finitely many prime divisors of that constant.

  This is the content of the FinitePrecision.lean theorem, now verified
  concretely in the factoring context.

  The uncomputable functions (BB, Omega, K, halting problem) DO exist and
  WOULD factor N instantly IF you had infinite-precision oracle access —
  but (a) such oracles don't exist physically, and (b) finite approximations
  collapse to ordinary computability.

  HONEST VERDICT: Hypercomputation is a meta-theoretical framework.  It does
  not yield a new computable factoring witness.  The connection to factoring
  is either (a) restating the complexity question (is factoring in P?), or
  (b) requiring a non-existent infinite-precision oracle.
""")

if __name__ == "__main__":
    main()

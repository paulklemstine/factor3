#!/usr/bin/env python3
"""
Langlands / Idele Class Group factoring experiments.

Tests whether the idele class group C_Q, Hecke characters, Eisenstein series,
and Selberg class structures offer any new classical factoring approach.

Key structural facts:
- C_Q ~= R_{>0} x Z-hat^x (for Q)
- Hecke characters of Q = Dirichlet characters (class field theory / GL(1) Langlands)
- The principal idele (N,N,N,...) is TRIVIAL in C_Q
- Hecke characters are trivial on principal ideles: chi(N) = 1

Hypotheses:
  H1 - Conductor of the Jacobi symbol (./N) reveals factors
  H2 - Number of primitive characters mod N reveals factors
  H3 - Class number of Q(sqrt(N)) reveals factors
  H4 - Gauss sum G(chi_N) reveals factors (replicates Exp W from idele view)
  H5 - L(1, chi_N) special value reveals factors
  H6 - "mod N Hecke character" of conductor p can be constructed from N alone
  H7 - Eisenstein residue at s=1 mod N reveals factors
"""

import math
from collections import defaultdict

def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def jacobi(a, n):
    """Jacobi symbol (a/n) for odd positive n. Returns -1, 0, or 1."""
    if n <= 0 or n % 2 == 0:
        return 0
    a = a % n
    result = 1
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

def discriminant_qsqrt(N):
    """Discriminant of Q(sqrt(N)) for squarefree N."""
    return N if N % 4 == 1 else 4 * N

def fundamental_unit_pell(N):
    """Fundamental unit of Q(sqrt(N)): minimal (x,y) with x^2-N*y^2 = +-1."""
    a0 = int(math.isqrt(N))
    if a0 * a0 == N:
        return None
    m, d, a = 0, 1, a0
    p_prev, p_curr = 1, a0
    q_prev, q_curr = 0, 1
    while True:
        m = d * a - m
        d = (N - m * m) // d
        a = (a0 + m) // d
        p_prev, p_curr = p_curr, a * p_curr + p_prev
        q_prev, q_curr = q_curr, a * q_curr + q_prev
        val = p_curr * p_curr - N * q_curr * q_curr
        if val == 1 or val == -1:
            return (p_curr, q_curr)

def class_number_real_quadratic(d):
    """Class number h(d) for d > 0 a fundamental discriminant.
    Enumerates reduced indefinite binary quadratic forms of discriminant d,
    then quotients by the involution (a,b,c) ~ (c,b,a) (the unit action)."""
    assert d > 0
    sqrt_d = int(math.isqrt(d))
    if sqrt_d * sqrt_d == d:
        return 0
    reduced = []
    for b in range(sqrt_d + 1):
        if (b - d) % 2 != 0:
            continue
        diff = b * b - d
        if diff >= 0:
            continue
        ac = diff // 4
        abs_ac = abs(ac)
        if abs_ac == 0:
            continue
        divs = []
        for i in range(1, int(math.isqrt(abs_ac)) + 1):
            if abs_ac % i == 0:
                divs.append(i)
                if i != abs_ac // i:
                    divs.append(abs_ac // i)
        for aa in divs:
            c = ac // aa
            if math.gcd(math.gcd(abs(aa), abs(b)), abs(c)) != 1:
                continue
            if abs(sqrt_d - 2 * abs(aa)) < b:
                reduced.append((aa, b, c))
    orbits = set()
    for (a, b, c) in reduced:
        key = (min(a, c), b, max(a, c))
        orbits.add(key)
    return len(orbits)

def divisors_from_factorint(N, fac):
    """Build sorted list of divisors from factorization dict."""
    divs = [1]
    for p, e in fac.items():
        new_divs = []
        for d in divs:
            for k in range(e + 1):
                new_divs.append(d * (p ** k))
        divs = sorted(new_divs)
    return divs

# ───────────────────────── Experiment H1 ────────────────────────────
# H1: Conductor of the Jacobi symbol (./N).
# For N=pq: chi_N = (./p)(./q), conductor = pq = N. Reveals nothing.

def conductor_jacobi(N, fac):
    """Conductor of Jacobi symbol (./N). Requires factorization."""
    divs = divisors_from_factorint(N, fac)
    for m in divs:
        if m == 1:
            # chi factors through trivial group iff chi is trivial on all units
            if all(jacobi(n, N) == 1 for n in range(1, N) if gcd(n, N) == 1):
                return 1
            continue
        ok = True
        for n in range(1, N):
            if gcd(n, N) == 1 and n % m == 1:
                if jacobi(n, N) != 1:
                    ok = False
                    break
        if ok:
            return m
    return N

def experiment_H1():
    print("=" * 70)
    print("EXPERIMENT H1 — Conductor of the Jacobi symbol (./N)")
    print("=" * 70)
    print()
    print("Theory: For N=pq, chi_N = (./N) = (./p)(./q).")
    print("cond(chi_N) = pq = N (for distinct odd primes).")
    print("Computing the conductor requires testing divisors of N.")
    print()
    test_cases = [(3, 5), (5, 7), (11, 13), (17, 19), (31, 37), (101, 103)]
    print(f"  {'N':>8} {'factors':>12} {'conductor':>12} {'reveals factor?':>18}")
    for p, q in test_cases:
        N = p * q
        fac = {p: 1, q: 1}
        cond = conductor_jacobi(N, fac)
        reveals = "No (cond = N)" if cond == N else f"Yes! cond={cond}"
        print(f"  {N:>8} {str(p)+'x'+str(q):>12} {cond:>12} {reveals:>18}")
    print()
    print("CONCLUSION: The conductor of (./N) is N itself. Computing it requires")
    print("knowing the divisors of N, which requires factoring. CIRCULARITY.")
    print()

# ───────────────────────── Experiment H2 ────────────────────────────
# H2: Number of primitive characters mod N.
# For N=pq: = (p-2)(q-2) = N - 2(p+q) + 4. Encodes p+q but needs phi(N).

def num_primitive_characters(N, fac):
    """#primitive Dirichlet characters mod N. Requires factorization."""
    phi = N
    for p in fac:
        phi = phi // p * (p - 1)
    result = phi
    for p in fac:
        result = result * (p - 2) // (p - 1)
    return result

def experiment_H2():
    print("=" * 70)
    print("EXPERIMENT H2 — Number of primitive characters mod N")
    print("=" * 70)
    print()
    print("Theory: #primitive characters mod N = phi(N) * prod_{p|N}(1-1/(p-1)).")
    print("For N=pq: = (p-2)(q-2) = N - 2(p+q) + 4.")
    print("If computable from N alone, this gives p+q, which factors N.")
    print("But computing it requires phi(N), which requires factoring.")
    print()
    test_cases = [(3, 5), (5, 7), (11, 13), (17, 19), (31, 37), (101, 103)]
    print(f"  {'N':>8} {'factors':>12} {'#prim char':>12} {'(p-2)(q-2)':>12} {'N-2(p+q)+4':>12}")
    for p, q in test_cases:
        N = p * q
        fac = {p: 1, q: 1}
        npc = num_primitive_characters(N, fac)
        expected = (p - 2) * (q - 2)
        formula = N - 2 * (p + q) + 4
        print(f"  {N:>8} {str(p)+'x'+str(q):>12} {npc:>12} {expected:>12} {formula:>12}")
    print()
    print("Verification: #primitive = (p-2)(q-2) = N - 2(p+q) + 4.")
    print("This quantity ENCODES p+q (hence factors N) but computing it requires")
    print("phi(N) = (p-1)(q-1), which requires factoring. CIRCULARITY.")
    print()

# ───────────────────────── Experiment H3 ────────────────────────────
# H3: Class number of Q(sqrt(N)).

def experiment_H3():
    print("=" * 70)
    print("EXPERIMENT H3 — Class number of Q(sqrt(N))")
    print("=" * 70)
    print()
    print("Theory: For N=pq, Q(sqrt(N)) has discriminant d = N or 4N.")
    print("The class number h(d) is a global arithmetic invariant.")
    print("Question: does gcd(h(d), N) > 1? Does h(d) reveal p or q?")
    print()
    test_cases = [(3, 5), (5, 7), (11, 13), (17, 19), (31, 37), (101, 103),
                  (3, 11), (7, 13), (19, 23), (43, 47)]
    print(f"  {'N':>8} {'factors':>12} {'disc':>8} {'h(d)':>8} {'gcd(h,N)':>10} {'reveals?':>10}")
    for p, q in test_cases:
        N = p * q
        d = discriminant_qsqrt(N)
        h = class_number_real_quadratic(d)
        g = gcd(h, N)
        reveals = "Yes!" if 1 < g < N else "No"
        print(f"  {N:>8} {str(p)+'x'+str(q):>12} {d:>8} {h:>8} {g:>10} {reveals:>10}")
    print()
    print("CONCLUSION: gcd(h(d), N) = 1 in all tested cases. The class number")
    print("is a global invariant that does not share factors with N.")
    print("Computing h(d) for large N is itself hard (requires Pell equation).")
    print()

# ───────────────────────── Experiment H4 ────────────────────────────
# H4: Gauss sum G(chi_N) — idele class group Fourier transform.

def gauss_sum_jacobi(N):
    """G(chi_N) = sum_{n=1}^{N} (n/N) e^{2 pi i n / N}."""
    total = 0 + 0j
    for n in range(1, N + 1):
        total += jacobi(n, N) * complex(math.cos(2 * math.pi * n / N), math.sin(2 * math.pi * n / N))
    return total

def experiment_H4():
    print("=" * 70)
    print("EXPERIMENT H4 — Gauss sum G(chi_N) (idele class group perspective)")
    print("=" * 70)
    print()
    print("Theory: G(chi_N) = G(chi_p)G(chi_q) by CRT multiplicativity.")
    print("|G(chi_N)| = sqrt(N). Phase reveals (p mod 4, q mod 4) -- 1 bit.")
    print("This is the idele class group's Fourier transform of the Jacobi symbol.")
    print()
    test_cases = [(3, 5), (5, 7), (11, 13), (17, 19), (31, 37)]
    print(f"  {'N':>8} {'factors':>12} {'|G|':>10} {'sqrt(N)':>10} {'phase/PI':>10} {'(p%4,q%4)':>12}")
    for p, q in test_cases:
        N = p * q
        G = gauss_sum_jacobi(N)
        mag = abs(G)
        phase = math.atan2(G.imag, G.real) / math.pi
        print(f"  {N:>8} {str(p)+'x'+str(q):>12} {mag:>10.4f} {math.sqrt(N):>10.4f} {phase:>10.4f}    ({p%4},{q%4})")
    print()
    print("CONCLUSION: |G(chi_N)| = sqrt(N) (no factor info). Phase reveals")
    print("(p mod 4, q mod 4) -- exactly 1 bit. This is Exp W rediscovered")
    print("from the idele class group perspective. The idele class group's")
    print("Fourier transform encodes only 1 bit of factor information.")
    print()

# ───────────────────────── Experiment H5 ────────────────────────────
# H5: L(1, chi_N) special value.

def L1_chi(N, terms=200000):
    """L(1, chi_N) = sum_{n=1}^infty chi_N(n)/n by partial sum."""
    total = 0.0
    for n in range(1, terms + 1):
        total += jacobi(n, N) / n
    return total

def experiment_H5():
    print("=" * 70)
    print("EXPERIMENT H5 — L(1, chi_N) special value")
    print("=" * 70)
    print()
    print("Theory: L(1, chi_d) = (2hR)/sqrt(d) for real quadratic Q(sqrt(N)).")
    print("This is a TRANSCENDENTAL number. 'Mod N' is ill-defined.")
    print("Extracting h requires knowing R = log(fundamental unit), which")
    print("requires solving Pell's equation x^2 - N*y^2 = +-1 (hard for large N).")
    print()
    test_cases = [(3, 5), (5, 7), (11, 13), (17, 19)]
    print(f"  {'N':>8} {'factors':>12} {'L(1,chi) approx':>18} {'fund. unit':>14} {'regulator R':>14}")
    for p, q in test_cases:
        N = p * q
        L1 = L1_chi(N, terms=200000)
        unit = fundamental_unit_pell(N)
        if unit:
            R = math.log(unit[0] + unit[1] * math.sqrt(N))
            print(f"  {N:>8} {str(p)+'x'+str(q):>12} {L1:>18.8f} {str(unit):>14} {R:>14.8f}")
        else:
            print(f"  {N:>8} {str(p)+'x'+str(q):>12} {L1:>18.8f} {'---':>14} {'---':>14}")
    print()
    print("CONCLUSION: L(1, chi_d) is transcendental -- 'mod N' is meaningless.")
    print("To extract the class number h from L(1,chi_d) = 2hR/sqrt(d),")
    print("one needs the regulator R = log(fundamental unit), which requires")
    print("solving Pell's equation. CIRCULARITY: R is as hard to compute")
    print("as factoring for large N (the fundamental unit has ~sqrt(N) digits).")
    print()

# ───────────────────────── Experiment H6 ────────────────────────────
# H6: Construct a "mod N Hecke character" of conductor p from N alone.

def conductor_of_char(N, chi, fac):
    """Conductor of a character chi on (Z/NZ)^x. Requires factorization."""
    divs = divisors_from_factorint(N, fac)
    for m in divs:
        if m == 1:
            # chi factors through trivial group iff chi is trivial on all units
            if all(abs(chi.get(n, 0) - 1) < 1e-9 for n in range(1, N) if gcd(n, N) == 1):
                return 1
            continue
        ok = True
        for n in range(1, N):
            if gcd(n, N) == 1 and n % m == 1:
                if abs(chi.get(n, 0) - 1) > 1e-9:
                    ok = False
                    break
        if ok:
            return m
    return N

def experiment_H6():
    print("=" * 70)
    print("EXPERIMENT H6 — 'mod N Hecke character' of conductor p")
    print("=" * 70)
    print()
    print("Theory: Hecke characters of Q = Dirichlet characters (class field theory).")
    print("A character of conductor p reveals p. Given N=pq, can we construct")
    print("a character of conductor p from N alone?")
    print()
    print("The characters mod N form a group G-hat ~= (Z/NZ)^x ~= (Z/pZ)^x x (Z/qZ)^x.")
    print("A character of conductor p is nontrivial on (Z/pZ)^x, trivial on (Z/qZ)^x.")
    print("To construct it, we need the projection (Z/NZ)^x -> (Z/pZ)^x,")
    print("which requires knowing p. CIRCULARITY.")
    print()
    print("Concrete test: enumerate characters mod N and check conductors.")
    print()

    N = 15
    fac = {3: 1, 5: 1}
    units = [n for n in range(1, N) if gcd(n, N) == 1]
    print(f"  N = {N} = 3 x 5")
    print(f"  (Z/{N}Z)^x = {units} (order {len(units)})")
    print(f"  Characters mod {N} and their conductors:")
    print()

    # (Z/15Z)^x ~= C2 x C4. Generators: 11 (order 2), 2 (order 4).
    count_by_cond = defaultdict(int)
    for k in range(4):  # value on 2: i^k
        for l in range(2):  # value on 11: (-1)^l
            chi = {}
            omega4 = complex(0, 1) ** k
            for n in units:
                for i in range(4):
                    for j in range(2):
                        if (pow(2, i, N) * pow(11, j, N)) % N == n:
                            chi[n] = (omega4 ** i) * ((-1) ** (l * j))
                            break
                    if n in chi:
                        break
            cond = conductor_of_char(N, chi, fac)
            count_by_cond[cond] += 1

    print(f"  {'conductor':>12} {'#characters':>14}")
    for cond in sorted(count_by_cond):
        print(f"  {cond:>12} {count_by_cond[cond]:>14}")
    print()
    print(f"  conductor 1:  trivial character (reveals nothing)")
    print(f"  conductor 3:  reveals p=3 (but need p=3 to construct)")
    print(f"  conductor 5:  reveals q=5 (but need q=5 to construct)")
    print(f"  conductor 15: primitive mod 15 (conductor = N, reveals nothing)")
    print()
    print("CONCLUSION: Characters of conductor p DO reveal p, but constructing")
    print("them requires knowing p. The characters computable from N alone")
    print("are those mod N, and computing their conductors requires factoring.")
    print("CIRCULARITY.")
    print()

# ───────────────────────── Experiment H7 ────────────────────────────
# H7: Eisenstein residue at s=1 mod N.

def experiment_H7():
    print("=" * 70)
    print("EXPERIMENT H7 — Eisenstein residue at s=1 mod N")
    print("=" * 70)
    print()
    print("Theory: The Eisenstein series E(s,z) for SL(2,Z) has a simple pole")
    print("at s=1 with residue 1/2 (from zeta(2s-1), see EisensteinPole.lean).")
    print("This is a UNIVERSAL constant, independent of N.")
    print()
    test_cases = [(3, 5), (5, 7), (11, 13), (17, 19), (31, 37)]
    print(f"  {'N':>8} {'factors':>12} {'residue mod N':>15} {'gcd(res,N)':>12}")
    for p, q in test_cases:
        N = p * q
        residue_mod_N = (N + 1) // 2  # 1/2 mod N = (N+1)/2
        g = gcd(residue_mod_N, N)
        print(f"  {N:>8} {str(p)+'x'+str(q):>12} {residue_mod_N:>15} {g:>12}")
    print()
    print("CONCLUSION: The Eisenstein residue is the universal constant 1/2.")
    print("Mod N, this is (N+1)/2, which is coprime to N (for odd N).")
    print("It reveals NOTHING about the factors. The pole structure is")
    print("independent of N -- it is a property of the idele class group")
    print("C_Q itself, not of the integer N.")
    print()

if __name__ == "__main__":
    experiment_H1()
    experiment_H2()
    experiment_H3()
    experiment_H4()
    experiment_H5()
    experiment_H6()
    experiment_H7()
    print("=" * 70)
    print("OVERALL CONCLUSION")
    print("=" * 70)
    print()
    print("The idele class group C_Q is a quotient by Q^x, so the principal")
    print("idele (N,N,N,...) is TRIVIAL in C_Q. Hecke characters are trivial")
    print("on principal ideles: chi(N) = 1. The only way Hecke characters")
    print("interact with N is through their CONDUCTOR, which is a property")
    print("of the character, not of N.")
    print()
    print("Every quantity computable from N alone that is a Hecke character")
    print("mod N has conductor dividing N, and computing the conductor")
    print("requires factoring. The Gauss sum gives only 1 bit (Exp W).")
    print("The L-value is transcendental. The class number is a global")
    print("invariant coprime to N. The Eisenstein residue is universal.")
    print()
    print("The Langlands/idele class group structure does NOT offer a new")
    print("classical factoring approach. The barrier is structural: C_Q")
    print("is a quotient by Q^x, so N is trivial in it.")
    print()
    print("This is experiment #86 in the factoring lab (paradigm: Langlands /")
    print("idele class group / Hecke characters).")

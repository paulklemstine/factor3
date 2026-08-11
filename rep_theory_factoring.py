"""
Test whether representation theory of S_N encodes factors of N = pq.

Hypotheses tested:
  H1: p(N) (number of partitions of N) mod something encodes factors.
  H2: gcd(f^λ, N) for specific partitions λ reveals a factor (hook-length formula).
  H3: gcd(χ^λ(g), N) for specific partitions λ and group elements g reveals a factor.
  H4: Some combination of representation-theoretic data reveals factors.
"""

import math
from sympy import (
    partition, factorial, binomial, gcd, factorint, divisors,

)
from itertools import product as iterproduct
import sys

semiprimes = [
    (65, 5, 13),
    (221, 13, 17),
    (493, 17, 29),
    (1189, 29, 41),
    (3233, 53, 61),
    (9797, 97, 101),
]

def test_h1_partition_function():
    """H1: Does p(N) mod something encode factors?"""
    print("=" * 80)
    print("H1: Partition function p(N)")
    print("=" * 80)
    for N, p, q in semiprimes:
        pN = partition(N)
        g = math.gcd(pN, N)
        print(f"N={N:>6} = {p}×{q}: p(N) = {pN}")
        print(f"           gcd(p(N), N) = {g}  {'*** FACTOR! ***' if 1 < g < N else ''}")
        # Also check p(N) mod p and mod q
        print(f"           p(N) mod {p} = {pN % p}, p(N) mod {q} = {pN % q}")
    print()

def hook_lengths(partition_shape):
    """Compute all hook lengths for a Young diagram of given shape."""
    # partition_shape is a list of row lengths, nonincreasing
    hooks = []
    for i, row_len in enumerate(partition_shape):
        for j in range(row_len):
            # arm = cells to the right in same row
            arm = row_len - j - 1
            # leg = cells below in same column
            leg = sum(1 for k in range(i+1, len(partition_shape)) if partition_shape[k] > j)
            hooks.append(arm + leg + 1)
    return hooks

def dimension_from_hook_formula(partition_shape):
    """Compute f^λ = N! / ∏ hook lengths."""
    N = sum(partition_shape)
    hooks = hook_lengths(partition_shape)
    hook_prod = 1
    for h in hooks:
        hook_prod *= h
    return math.factorial(N) // hook_prod

def generate_partitions(n, max_part=None):
    """Generate all partitions of n as nonincreasing lists."""
    if max_part is None:
        max_part = n
    if n == 0:
        yield []
        return
    for first in range(min(n, max_part), 0, -1):
        for rest in generate_partitions(n - first, first):
            yield [first] + rest

def test_h2_hook_dimensions():
    """H2: Does gcd(f^λ, N) reveal a factor for some partition λ?"""
    print("=" * 80)
    print("H2: Hook-length formula — gcd(f^λ, N)")
    print("=" * 80)
    
    for N, p, q in semiprimes:
        print(f"\nN = {N} = {p}×{q}")
        found_factor = False
        count = 0
        for part in generate_partitions(N):
            count += 1
            f = dimension_from_hook_formula(part)
            g = math.gcd(f, N)
            if 1 < g < N:
                print(f"  Partition {part}: f^λ = {f}, gcd(f^λ, N) = {g}  *** FACTOR! ***")
                found_factor = True
                break
            # For large N, limit computation
            if count > 100000:
                print(f"  (checked {count} partitions, stopping early)")
                break
        if not found_factor and count <= 100000:
            print(f"  No factor found among {count} partitions")
        elif not found_factor:
            print(f"  No factor found in first {count} partitions")
    print()

def test_h2_hook_partitions_only():
    """H2 (refined): Test hook partitions (N-k, 1^k) where f^λ = C(N-1, k)."""
    print("=" * 80)
    print("H2': Hook partitions (N-k, 1^k) — f^λ = C(N-1, k)")
    print("=" * 80)
    
    for N, p, q in semiprimes:
        print(f"\nN = {N} = {p}×{q}")
        found = False
        for k in range(N):
            f = math.comb(N-1, k)
            g = math.gcd(f, N)
            if 1 < g < N:
                print(f"  k={k}: C({N-1},{k}) = {f}, gcd = {g}  *** FACTOR! ***")
                found = True
        if not found:
            print(f"  No factor found among all {N} hook partitions")
    print()

def test_h2_two_row_partitions():
    """H2 (refined): Test two-row partitions (N-k, k)."""
    print("=" * 80)
    print("H2'': Two-row partitions (N-k, k)")
    print("=" * 80)
    
    for N, p, q in semiprimes:
        print(f"\nN = {N} = {p}×{q}")
        found = False
        for k in range(N//2 + 1):
            part = [N-k, k] if k > 0 else [N]
            f = dimension_from_hook_formula(part)
            g = math.gcd(f, N)
            if 1 < g < N:
                print(f"  k={k}: partition ({N-k},{k}), f^λ = {f}, gcd = {g}  *** FACTOR! ***")
                found = True
        if not found:
            print(f"  No factor found among two-row partitions")
    print()

def test_h3_characters():
    """H3: Does gcd(χ^λ(g), N) reveal a factor?"""
    print("=" * 80)
    print("H3: Character values — gcd(χ^λ(g), N)")
    print("=" * 80)
    
    # For small N, we can compute character tables
    from sympy.combinatorics.symmetric_group import SymmetricGroup
    from sympy.combinatorics.group_constructs import DirectProduct
    
    for N, p, q in semiprimes[:4]:  # Only for smaller N (character tables are expensive)
        print(f"\nN = {N} = {p}×{q}")
        try:
            from sympy.combinatorics.symmetric_group import SymmetricGroup
            G = SymmetricGroup(N)
            # Get conjugacy classes
            # This is expensive for large N; we'll use a different approach
            # Use the Murnaghan-Nakayama rule or sympy's character table
            print(f"  (Computing character table for S_{N}...)")
            # sympy has character_table method but it's very slow for N > 10
            # Let's use a more direct approach
            if N <= 12:
                ct = G.conjugacy_classes()
                print(f"  Number of conjugacy classes: {len(ct)}")
            else:
                print(f"  S_{N} is too large for direct character table computation")
                # Use Murnaghan-Nakayama for specific partitions
                break
        except Exception as e:
            print(f"  Error: {e}")
            break
    print()

def murnaghan_nakayama(char_value_cache, partition_shape, cycle_type):
    """
    Compute χ^λ(g) where g has the given cycle type using the
    Murnaghan-Nakayama rule.
    
    char_value_cache: dict for memoization
    partition_shape: list of row lengths (nonincreasing)
    cycle_type: list of cycle lengths (nonincreasing)
    """
    key = (tuple(partition_shape), tuple(cycle_type))
    if key in char_value_cache:
        return char_value_cache[key]
    
    # Base cases
    if sum(partition_shape) != sum(cycle_type):
        return 0
    if not cycle_type:
        # Empty cycle type = identity element
        if not partition_shape or partition_shape == [0]:
            result = 1
        else:
            result = dimension_from_hook_formula(partition_shape)
        char_value_cache[key] = result
        return result
    if not partition_shape:
        char_value_cache[key] = 0
        return 0
    
    # Murnaghan-Nakayama: remove a rim hook of length = largest cycle
    largest_cycle = cycle_type[0]
    remaining_cycles = cycle_type[1:]
    
    total = 0
    # Find all rim hooks of length largest_cycle in the diagram of partition_shape
    rim_hooks = find_rim_hooks(partition_shape, largest_cycle)
    for hook_shape, sign in rim_hooks:
        # hook_shape is the partition after removing the rim hook
        total += sign * murnaghan_nakayama(char_value_cache, hook_shape, remaining_cycles)
    
    char_value_cache[key] = total
    return total

def find_rim_hooks(partition_shape, length):
    """
    Find all rim hooks of given length in the Young diagram.
    Returns list of (resulting_partition, sign) where sign = (-1)^(number of rows spanned - 1).
    """
    results = []
    N = sum(partition_shape)
    if length > N:
        return results
    
    # A rim hook is a connected sequence of cells along the rim of the diagram
    # starting from some cell and moving only right or down, with exactly `length` cells.
    # We need to enumerate all such rim hooks.
    
    # The rim of the diagram consists of cells (i, j) where (i, j+1) is outside
    # or (i+1, j) is outside (i.e., cells on the boundary).
    
    # Actually, let's use a different approach: enumerate all connected sequences
    # of `length` cells along the rim.
    
    # First, identify all rim cells
    rows = len(partition_shape)
    rim_cells = set()
    for i, row_len in enumerate(partition_shape):
        for j in range(row_len):
            # Cell (i, j) is on the rim if (i, j+1) is outside the diagram
            # or (i+1, j) is outside
            is_rim = (j == row_len - 1) or (i + 1 >= len(partition_shape)) or (partition_shape[i+1] <= j)
            if is_rim:
                rim_cells.add((i, j))
    
    # Now find all connected sequences of `length` rim cells that form a valid rim hook.
    # A rim hook is a connected skew shape with no 2x2 block.
    # We'll use DFS.
    
    # Actually, a simpler approach: a rim hook of length L is determined by its starting cell
    # and consists of cells along the rim. Let's enumerate by starting cell.
    
    for start_i, start_j in rim_cells:
        # Try to build a rim hook starting from (start_i, start_j)
        # The rim hook must be connected and lie on the rim.
        # We'll use DFS to find all rim hooks of the right length.
        _enumerate_rim_hooks_from(
            partition_shape, rim_cells, start_i, start_j, length, results
        )
    
    # Deduplicate
    seen = set()
    unique_results = []
    for part, sign in results:
        key = (tuple(part), sign)
        if key not in seen:
            seen.add(key)
            unique_results.append((part, sign))
    
    return unique_results

def _enumerate_rim_hooks_from(partition_shape, rim_cells, si, sj, length, results):
    """Enumerate rim hooks of given length starting from (si, sj)."""
    # Use DFS: at each step, we can move right or down along the rim.
    # The rim hook must be a connected sequence of cells.
    
    # We'll build the hook cell by cell.
    # State: current cell, set of cells in hook, path
    
    rows = len(partition_shape)
    
    def is_in_diagram(i, j):
        return 0 <= i < rows and 0 <= j < partition_shape[i]
    
    def get_neighbors(i, j):
        """Get rim cells adjacent to (i, j) (right or down)."""
        neighbors = []
        for di, dj in [(0, 1), (1, 0)]:
            ni, nj = i + di, j + dj
            if (ni, nj) in rim_cells:
                neighbors.append((ni, nj))
        return neighbors
    
    # DFS
    def dfs(ci, cj, hook_cells, visited):
        if len(hook_cells) == length:
            # Check if this forms a valid rim hook (connected, no 2x2)
            # and compute the resulting partition
            _process_rim_hook(partition_shape, hook_cells, results)
            return
        for ni, nj in get_neighbors(ci, cj):
            if (ni, nj) not in visited:
                visited.add((ni, nj))
                hook_cells.append((ni, nj))
                dfs(ni, nj, hook_cells, visited)
                hook_cells.pop()
                visited.remove((ni, nj))
    
    visited = {(si, sj)}
    dfs(si, sj, [(si, sj)], visited)

def _process_rim_hook(partition_shape, hook_cells, results):
    """Given a set of cells forming a rim hook, compute the resulting partition and sign."""
    # Check connectivity
    if not hook_cells:
        return
    
    # Check that hook_cells form a connected path
    cell_set = set(hook_cells)
    
    # Check no 2x2 block
    for i, j in hook_cells:
        if (i+1, j) in cell_set and (i, j+1) in cell_set and (i+1, j+1) in cell_set:
            return  # Has a 2x2 block, not a valid rim hook
    
    # Compute resulting partition shape
    rows = len(partition_shape)
    new_shape = list(partition_shape)
    for i, j in hook_cells:
        # Remove cell (i, j) from row i
        # This means row i loses one cell at position j
        # But we need to make sure we're removing from the right place
        pass
    
    # Actually, removing a rim hook means removing cells from the diagram.
    # The resulting shape should still be a valid partition (nonincreasing row lengths).
    # Let's compute the new row lengths.
    
    row_decrements = [0] * rows
    for i, j in hook_cells:
        row_decrements[i] += 1
    
    # The cells removed from row i must be the rightmost cells of that row
    # (since it's a rim hook)
    new_shape = []
    for i in range(rows):
        remaining = partition_shape[i] - row_decrements[i]
        if remaining < 0:
            return  # Invalid
        new_shape.append(remaining)
    
    # Remove trailing zeros and ensure nonincreasing
    while new_shape and new_shape[-1] == 0:
        new_shape.pop()
    
    # Check nonincreasing
    for i in range(len(new_shape) - 1):
        if new_shape[i] < new_shape[i+1]:
            return  # Not a valid partition
    
    # Compute sign: (-1)^(number of rows spanned - 1)
    rows_spanned = len(set(i for i, j in hook_cells))
    sign = (-1) ** (rows_spanned - 1)
    
    results.append((new_shape, sign))

def test_h3_murnaghan_nakayama():
    """H3: Use Murnaghan-Nakayama to compute character values and check gcd with N."""
    print("=" * 80)
    print("H3': Murnaghan-Nakayama character values — gcd(χ^λ(g), N)")
    print("=" * 80)
    
    for N, p, q in semiprimes[:4]:  # Only smaller N
        print(f"\nN = {N} = {p}×{q}")
        cache = {}
        found = False
        
        # Test a few specific partitions and cycle types
        test_partitions = []
        # Hook partitions
        for k in range(min(N, 10)):
            part = [N-k] + [1]*k
            test_partitions.append(part)
        # Two-row partitions
        for k in range(min(N//2 + 1, 10)):
            if k == 0:
                test_partitions.append([N])
            else:
                test_partitions.append([N-k, k])
        
        # Test cycle types: identity, transpositions, etc.
        test_cycle_types = [
            [1]*N,           # identity
            [2] + [1]*(N-2), # transposition
            [3] + [1]*(N-3), # 3-cycle
            [N],             # N-cycle
        ]
        if N >= 4:
            test_cycle_types.append([2, 2] + [1]*(N-4))  # double transposition
            test_cycle_types.append([4] + [1]*(N-4))    # 4-cycle
        
        for part in test_partitions:
            for ct in test_cycle_types:
                if sum(ct) != N:
                    continue
                ct_sorted = sorted(ct, reverse=True)
                chi = murnaghan_nakayama(cache, part, ct_sorted)
                g = math.gcd(abs(chi), N)
                if 1 < g < N:
                    print(f"  λ={part}, cycle type {ct_sorted}: χ = {chi}, gcd(|χ|, N) = {g}  *** FACTOR! ***")
                    found = True
        
        if not found:
            print(f"  No factor found")
    print()

def test_h4_sum_of_dimensions():
    """H4: Sum of dimensions, sum of squares, etc."""
    print("=" * 80)
    print("H4: Sums of representation-theoretic quantities")
    print("=" * 80)
    
    for N, p, q in semiprimes[:4]:  # Only smaller N
        print(f"\nN = {N} = {p}×{q}")
        
        # Sum of f^λ over all partitions = number of involutions
        # Sum of (f^λ)^2 = N!
        sum_f = 0
        sum_f2 = 0
        count = 0
        for part in generate_partitions(N):
            f = dimension_from_hook_formula(part)
            sum_f += f
            sum_f2 += f * f
            count += 1
        
        print(f"  Number of partitions: {count}")
        print(f"  Sum of f^λ = {sum_f}")
        print(f"  Sum of (f^λ)^2 = {sum_f2} (should be {math.factorial(N)})")
        print(f"  gcd(sum f^λ, N) = {math.gcd(sum_f, N)}")
        print(f"  gcd(sum (f^λ)^2, N) = {math.gcd(sum_f2, N)}")
    print()

def test_h5_schur_idempotent_trace():
    """H5: The Schur idempotent e_λ = (f^λ/N!) Σ χ^λ(g⁻¹) g.
    Its trace in the regular representation is (f^λ)^2.
    Could some other evaluation encode factors?"""
    print("=" * 80)
    print("H5: Schur idempotent evaluations")
    print("=" * 80)
    
    for N, p, q in semiprimes[:4]:
        print(f"\nN = {N} = {p}×{q}")
        cache = {}
        
        # For each partition, compute the Schur idempotent's "coefficient sum"
        # e_λ = (f^λ/N!) Σ_g χ^λ(g⁻¹) g
        # The sum of coefficients is (f^λ/N!) Σ_g χ^λ(g⁻¹)
        # Σ_g χ^λ(g⁻¹) = |G| χ^λ(1) / f^λ ... no, that's not right.
        # Actually Σ_g χ^λ(g) = |G| δ_{λ, trivial} (orthogonality)
        # So for trivial partition, Σ_g χ(g) = |G|
        # For nontrivial, Σ_g χ(g) = 0
        
        # Let's compute the sum of |χ^λ(g)| over all g, or over conjugacy classes.
        # This is expensive; let's just test a few partitions.
        
        test_partitions = []
        for k in range(min(N, 8)):
            part = [N-k] + [1]*k
            test_partitions.append(part)
        
        for part in test_partitions:
            f = dimension_from_hook_formula(part)
            # Compute sum of |χ^λ(g)| over all conjugacy classes weighted by class size
            # This requires knowing all conjugacy classes, which is expensive.
            # Instead, let's compute the "trace at a specific element" approach.
            
            # The idempotent e_λ evaluated at a specific group element g gives
            # (f^λ/N!) χ^λ(g⁻¹). This is a scalar multiple of the group element.
            # The scalar is (f^λ/N!) χ^λ(g⁻¹).
            # gcd of this with N... but it's a rational number.
            
            # Let's compute (f^λ) * χ^λ(g) for various g and check gcd with N.
            cycle_types = [
                [1]*N,           # identity: χ = f^λ
                [2] + [1]*(N-2), # transposition
                [N],             # N-cycle
            ]
            for ct in cycle_types:
                if sum(ct) != N:
                    continue
                ct_sorted = sorted(ct, reverse=True)
                chi = murnaghan_nakayama(cache, part, ct_sorted)
                val = f * chi
                g = math.gcd(abs(val), N)
                if 1 < g < N:
                    print(f"  λ={part}, ct={ct_sorted}: f^λ·χ = {val}, gcd = {g}  *** FACTOR! ***")
        
        print(f"  (tested hook partitions for S_{N})")
    print()

if __name__ == "__main__":
    print("Testing whether representation theory of S_N encodes factors of N = pq")
    print("Semiprimes to test:", [N for N, p, q in semiprimes])
    print()
    
    test_h1_partition_function()
    test_h2_hook_partitions_only()
    test_h2_two_row_partitions()
    test_h3_murnaghan_nakayama()
    test_h4_sum_of_dimensions()
    test_h5_schur_idempotent_trace()
    
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("See above for detailed results.")

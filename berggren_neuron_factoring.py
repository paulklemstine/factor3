"""
Berggren Neuron Energy Factoring Experiment
============================================

Leverages the EML Berggren Energy Neuron construction from the Lean 4 Catalog
(Pythagorean/EMLBerggrenEnergyNeuron.lean): a single analytic neuron
    emlNeuron(sigma, epsilon, x) = log(2 + sigma * exp(epsilon * x))
with three fixed parameter pairs drives the entire Berggren tree of primitive
Pythagorean triples. The node energy E = log(m/n) is a scalar that encodes the
full root-to-node path, and the three branch neurons partition the energy line
into (0, log 2), (log 2, log 3), (log 3, oo), so the branch is read off by two
comparisons (the "unique descent" theorem, energy_descent_unique).

Factoring connection: for odd N = pq there is a unique primitive Pythagorean
triple with odd leg N, having Euclid parameters m* = (p+q)/2, n* = (q-p)/2,
hence energy E* = log((p+q)/(q-p)). Finding this triple factors N.

This script searches the Berggren tree for the triple with leg = N, using the
neuron branch-partition to decode energies, and recovers p,q from the Euclid
parameters.
"""

import math
from collections import deque

LOG2 = math.log(2.0)
LOG3 = math.log(3.0)

# --- The three EML branch neurons (parent energy -> child energy) ----------
def neuron_A(x): return math.log(2.0 - math.exp(-x))   # image (0, log 2)
def neuron_B(x): return math.log(2.0 + math.exp(-x))   # image (log 2, log 3)
def neuron_C(x): return math.log(2.0 + math.exp(x))    # image (log 3, oo)

# --- Inverse neurons: child energy -> (branch, parent energy) ---------------
def inv_neuron(y):
    """Branch decision via the energy-line partition (the core neuron theorem)."""
    if y < LOG2:
        return 'A', -math.log(2.0 - math.exp(y))
    elif y < LOG3:
        return 'B', -math.log(math.exp(y) - 2.0)
    else:
        return 'C', math.log(math.exp(y) - 2.0)

# --- Decode a scalar energy back to Euclid params (m, n) --------------------
def energy_to_params(E, tol=1e-9):
    """Walk UP the tree from energy E to the root, then reconstruct (m,n)."""
    path = []  # branch sequence, leaf -> root
    E_cur = E
    while abs(E_cur - LOG2) > tol:
        branch, E_parent = inv_neuron(E_cur)
        path.append(branch)
        E_cur = E_parent
        if len(path) > 5000:
            raise ValueError("Path too long — not a Berggren energy?")
    # Reconstruct (m, n) from the root (2,1) by following path root -> leaf
    m, n = 2, 1
    for branch in reversed(path):
        if branch == 'A':   m, n = 2*m - n, m
        elif branch == 'B': m, n = 2*m + n, m
        elif branch == 'C': m, n = m + 2*n, n
    return m, n, path

# --- Odd leg of the triple with Euclid params (m, n) ------------------------
def odd_leg(m, n): return m*m - n*n

# --- BFS over the Berggren tree, pruning branches whose leg exceeds N -------
def berggren_factor(N, max_nodes=500000):
    """
    Search the Berggren tree for the primitive triple whose odd leg equals N.
    Leg increases monotonically along every path, so nodes with leg > N prune
    their entire subtree.
    """
    if N % 2 == 0:
        return None  # odd-leg representation requires odd N
    root_E = LOG2
    queue = deque([(root_E, 2, 1)])   # (energy, m, n)
    nodes = 0
    while queue and nodes < max_nodes:
        E, m, n = queue.popleft()
        nodes += 1
        a = odd_leg(m, n)
        if a == N:
            p, q = m - n, m + n
            return {
                'N': N, 'p': min(p, q), 'q': max(p, q),
                'm': m, 'n': n,
                'energy': E, 'path': ''.join(energy_to_params(E)[2]),
                'depth': len(energy_to_params(E)[2]),
                'nodes_explored': nodes,
            }
        if a > N:
            continue                      # prune: leg only grows downstream
        # Expand the three children via the EML neurons
        queue.append((neuron_A(E), 2*m - n, m))
        queue.append((neuron_B(E), 2*m + n, m))
        queue.append((neuron_C(E), m + 2*n, n))
    return None

# --- Verify the neuron round-trip: (m,n) -> energy -> (m,n) -----------------
def verify_roundtrip(m, n):
    E = math.log(m / n)
    m2, n2, _ = energy_to_params(E)
    return (m, n) == (m2, n2)

# --- Run the test cases -----------------------------------------------------
if __name__ == '__main__':
    test_cases = [143, 323, 1147, 10403]
    print("Berggren Neuron Energy Factoring")
    print("=" * 60)
    for N in test_cases:
        res = berggren_factor(N)
        if res:
            ok = verify_roundtrip(res['m'], res['n'])
            # Sanity: p * q == N
            assert res['p'] * res['q'] == N
            print(f"N = {N:>6}  ->  {res['p']} x {res['q']}"
                  f"    energy={res['energy']:.4f}  path={res['path']}"
                  f"  depth={res['depth']}  nodes={res['nodes_explored']}"
                  f"  roundtrip={'OK' if ok else 'FAIL'}")
        else:
            print(f"N = {N:>6}  ->  NOT FOUND")
    print()
    print("Note: p = m - n,  q = m + n,  energy = log(m/n) = log((p+q)/(q-p))")
